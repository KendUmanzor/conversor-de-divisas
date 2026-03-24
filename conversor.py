from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Sequence
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


TOKEN_REGEX = re.compile(
    r"(?P<CONVERTIR>\bconvertir\b)|"
    r"(?P<A>\ba\b)|"
    r"(?P<CANTIDAD>\d+(?:\.\d+)?)|"
    r"(?P<MONEDA>[A-Za-zÁÉÍÓÚáéíóúÑñ_]+)|"
    r"(?P<FIN>\$)|"
    r"(?P<SPACE>[ \t]+)|"
    r"(?P<INVALID>.)",
    re.IGNORECASE,
)

TASAS_USD = {
    "dolarestadounidense": 1.0,
    "lempirahondureño": 24.70,
    "quetzalguatemalteco": 7.77,
    "coloncostarricense": 514.20,
    "peso_mexicano": 16.90,
    "euro": 0.92,
}


@dataclass
class TokenInfo:
    linea: int
    columna: int
    tipo: str
    valor: str


@dataclass
class Nodo:
    etiqueta: str
    valor: str | None = None
    hijos: List["Nodo"] = field(default_factory=list)


@dataclass
class ResultadoAnalisis:
    tokens: List[TokenInfo]
    cantidad: float
    origen: str
    destino: str
    convertido: float
    arbol: Nodo


def normalizar_moneda(texto: str) -> str:
    return texto.strip().replace(" ", "").lower()


def lex_linea(linea: str, numero_linea: int) -> List[TokenInfo]:
    tokens: List[TokenInfo] = []
    posicion = 0

    while posicion < len(linea):
        match = TOKEN_REGEX.match(linea, posicion)
        if match is None:
            raise ValueError(f"Error léxico inesperado en línea {numero_linea}, columna {posicion + 1}.")

        tipo = match.lastgroup or "INVALID"
        valor = match.group(0)
        columna = posicion + 1

        if tipo == "SPACE":
            posicion = match.end()
            continue

        if tipo == "INVALID":
            raise ValueError(
                f"Token inválido '{valor}' en línea {numero_linea}, columna {columna}."
            )

        tokens.append(TokenInfo(numero_linea, columna, tipo.upper(), valor))
        posicion = match.end()

    return tokens


def parsear_tokens(tokens: Sequence[TokenInfo]) -> tuple[float, str, str, Nodo]:
    esperados = ["CONVERTIR", "CANTIDAD", "MONEDA", "A", "MONEDA", "FIN"]
    tipos = [t.tipo for t in tokens]

    if tipos != esperados:
        raise ValueError(
            "Error sintáctico. Se esperaba: "
            "convertir <cantidad> <MonedaOrigen> a <MonedaDestino>$"
        )

    cantidad = float(tokens[1].valor)
    origen = tokens[2].valor
    destino = tokens[4].valor

    arbol = Nodo(
        "inicio",
        hijos=[
            Nodo(
                "instruccion",
                hijos=[
                    Nodo("CONVERTIR", tokens[0].valor),
                    Nodo("CANTIDAD", tokens[1].valor),
                    Nodo("MONEDA_ORIGEN", origen),
                    Nodo("A", tokens[3].valor),
                    Nodo("MONEDA_DESTINO", destino),
                ],
            ),
            Nodo("FIN", tokens[5].valor),
        ],
    )

    return cantidad, origen, destino, arbol


def convertir(cantidad: float, origen: str, destino: str) -> float:
    origen_key = normalizar_moneda(origen)
    destino_key = normalizar_moneda(destino)

    if origen_key not in TASAS_USD:
        raise ValueError(f"Moneda origen no soportada: {origen}")
    if destino_key not in TASAS_USD:
        raise ValueError(f"Moneda destino no soportada: {destino}")

    usd = cantidad / TASAS_USD[origen_key]
    return usd * TASAS_USD[destino_key]


def analizar_linea(linea: str, numero_linea: int) -> ResultadoAnalisis:
    tokens = lex_linea(linea.strip(), numero_linea)
    cantidad, origen, destino, arbol = parsear_tokens(tokens)
    convertido = convertir(cantidad, origen, destino)
    return ResultadoAnalisis(tokens, cantidad, origen, destino, convertido, arbol)


def analizar_texto(texto: str) -> List[ResultadoAnalisis]:
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not lineas:
        raise ValueError("No hay entradas para analizar.")

    resultados: List[ResultadoAnalisis] = []
    for i, linea in enumerate(lineas, start=1):
        if not linea.endswith("$"):
            raise ValueError(f"La línea {i} no finaliza en '$'.")
        resultados.append(analizar_linea(linea, i))
    return resultados


def insertar_arbol(treeview: ttk.Treeview, parent: str, nodo: Nodo) -> None:
    texto = nodo.etiqueta if nodo.valor is None else f"{nodo.etiqueta}: {nodo.valor}"
    item_id = treeview.insert(parent, "end", text=texto)
    for hijo in nodo.hijos:
        insertar_arbol(treeview, item_id, hijo)


def ejecutar_gui() -> None:
    root = tk.Tk()
    root.title("Conversor de Divisas - Analizador Léxico/Sintáctico")
    root.geometry("1100x760")

    marco_superior = ttk.Frame(root, padding=10)
    marco_superior.pack(fill="x")

    ttk.Label(
        marco_superior,
        text="Entrada (una instrucción por línea, finalizando con '$'):",
    ).pack(anchor="w")

    txt_entrada = tk.Text(marco_superior, height=7, wrap="word")
    txt_entrada.pack(fill="x", pady=6)
    txt_entrada.insert(
        "1.0",
        "convertir 1 DolarEstadounidense a LempiraHondureño$\n"
        "convertir 1000 LempiraHondureño a DolarEstadounidense$",
    )

    marco_botones = ttk.Frame(marco_superior)
    marco_botones.pack(fill="x")

    def cargar_archivo() -> None:
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de entrada",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not ruta:
            return
        contenido = Path(ruta).read_text(encoding="utf-8")
        txt_entrada.delete("1.0", "end")
        txt_entrada.insert("1.0", contenido)

    ttk.Button(marco_botones, text="Cargar TXT", command=cargar_archivo).pack(side="left")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    tab_lexico = ttk.Frame(notebook)
    tab_sintactico = ttk.Frame(notebook)
    tab_arbol = ttk.Frame(notebook)

    notebook.add(tab_lexico, text="Analizador Léxico")
    notebook.add(tab_sintactico, text="Analizador Sintáctico")
    notebook.add(tab_arbol, text="Árbol")

    tabla = ttk.Treeview(
        tab_lexico,
        columns=("linea", "columna", "tipo", "valor"),
        show="headings",
    )
    tabla.heading("linea", text="Línea")
    tabla.heading("columna", text="Columna")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("valor", text="Valor")
    for col, ancho in [("linea", 90), ("columna", 90), ("tipo", 180), ("valor", 340)]:
        tabla.column(col, width=ancho)
    tabla.pack(fill="both", expand=True)

    txt_resultado = tk.Text(tab_sintactico, wrap="word")
    txt_resultado.pack(fill="both", expand=True)

    arbol_view = ttk.Treeview(tab_arbol)
    arbol_view.pack(fill="both", expand=True)

    def ejecutar_analisis() -> None:
        try:
            resultados = analizar_texto(txt_entrada.get("1.0", "end").strip())
        except Exception as exc:
            messagebox.showerror("Error de análisis", str(exc))
            return

        for row in tabla.get_children():
            tabla.delete(row)
        txt_resultado.delete("1.0", "end")
        for row in arbol_view.get_children():
            arbol_view.delete(row)

        for resultado in resultados:
            for tok in resultado.tokens:
                tabla.insert("", "end", values=(tok.linea, tok.columna, tok.tipo, tok.valor))

            txt_resultado.insert(
                "end",
                (
                    f"Línea {resultado.tokens[0].linea}: "
                    f"{resultado.cantidad:.2f} {resultado.origen} -> "
                    f"{resultado.convertido:.2f} {resultado.destino}\n"
                    f"Función semántica: Conversor:{resultado.origen}To{resultado.destino}\n\n"
                ),
            )

        insertar_arbol(arbol_view, "", resultados[0].arbol)
        for item in arbol_view.get_children():
            arbol_view.item(item, open=True)

    ttk.Button(marco_botones, text="Ejecutar", command=ejecutar_analisis).pack(side="left", padx=8)

    root.mainloop()


def ejecutar_cli(archivo: Path | None = None) -> None:
    if archivo:
        texto = archivo.read_text(encoding="utf-8")
    else:
        texto = (
            "convertir 1 DolarEstadounidense a LempiraHondureño$\n"
            "convertir 1000 LempiraHondureño a DolarEstadounidense$"
        )

    resultados = analizar_texto(texto)
    for res in resultados:
        print(f"Linea {res.tokens[0].linea}: {res.cantidad:.2f} {res.origen} -> {res.convertido:.2f} {res.destino}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Conversor de divisas con app de escritorio (Tkinter).")
    parser.add_argument("--cli", action="store_true", help="Ejecuta en modo terminal (para pruebas).")
    parser.add_argument("--archivo", type=Path, help="Archivo de texto para entrada.")
    args = parser.parse_args()

    if args.cli:
        ejecutar_cli(args.archivo)
    else:
        ejecutar_gui()


if __name__ == "__main__":
    main()
