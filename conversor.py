from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

GRAMATICA = r"""
    ?inicio: instruccion FIN

    instruccion: CONVERTIR CANTIDAD MONEDA A MONEDA

    CONVERTIR: /(?i)convertir/
    A: /(?i)a/
    CANTIDAD: /\d+(\.\d+)?/
    MONEDA: /[A-Za-zÁÉÍÓÚáéíóúÑñ]+/
    FIN: "$"

    %import common.WS
    %ignore WS
"""


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


class EvaluadorConversor:
    def instruccion(self, items):
        _convertir, cantidad, origen, _a, destino = items
        cantidad_num = float(cantidad)
        origen_txt = str(origen)
        destino_txt = str(destino)

        origen_key = normalizar_moneda(origen_txt)
        destino_key = normalizar_moneda(destino_txt)

        if origen_key not in TASAS_USD:
            raise ValueError(f"Moneda origen no soportada: {origen_txt}")
        if destino_key not in TASAS_USD:
            raise ValueError(f"Moneda destino no soportada: {destino_txt}")

        usd = cantidad_num / TASAS_USD[origen_key]
        convertido = usd * TASAS_USD[destino_key]

        return {
            "cantidad": cantidad_num,
            "origen": origen_txt,
            "destino": destino_txt,
            "resultado": convertido,
            "funcion_semantica": f"Conversor:{origen_txt}To{destino_txt}",
        }


def normalizar_moneda(texto: str) -> str:
    return texto.strip().replace(" ", "").lower()


def cargar_entradas(archivo: Path | None) -> List[str]:
    if archivo is None:
        return [
            "convertir 100 DolarEstadounidense a LempiraHondureño$",
            "convertir 2500 LempiraHondureño a DolarEstadounidense$",
            "convertir 50 Euro a Peso_Mexicano$",
        ]

    return [linea.strip() for linea in archivo.read_text(encoding="utf-8").splitlines() if linea.strip()]


def tokenizar_entrada(texto: str) -> List[TokenInfo]:
    patron = re.compile(
        r"(?P<CONVERTIR>\bconvertir\b)|"
        r"(?P<A>\ba\b)|"
        r"(?P<CANTIDAD>\d+(?:\.\d+)?)|"
        r"(?P<MONEDA>[A-Za-zÁÉÍÓÚáéíóúÑñ_]+)|"
        r"(?P<FIN>\$)",
        re.IGNORECASE,
    )
    encontrados: List[TokenInfo] = []
    for match in patron.finditer(texto):
        tipo = match.lastgroup or "DESCONOCIDO"
        valor = match.group()
        encontrados.append(TokenInfo(linea=1, columna=match.start() + 1, tipo=tipo, valor=valor))
    return encontrados


def construir_cuadro_lexico(tokens: Iterable[TokenInfo]) -> str:
    encabezado = f"{'Línea':<8} {'Columna':<8} {'Tipo':<14} {'Valor':<24}"
    separador = "-" * len(encabezado)
    filas = [encabezado, separador]
    for t in tokens:
        filas.append(f"{t.linea:<8} {t.columna:<8} {t.tipo:<14} {t.valor:<24}")
    return "\n".join(filas)


def analizar(parser, evaluador: EvaluadorConversor, texto: str) -> None:
    print("\n" + "=" * 90)
    print(f"Entrada: {texto}")

    tokens = tokenizar_entrada(texto)
    print("\n[Analizador Léxico] Tabla de tokens")
    print(construir_cuadro_lexico(tokens))

    arbol = parser.parse(texto)
    resultado = evaluador.transform(arbol)

    print("\n[Analizador Sintáctico] Resultado de operación")
    print(
        f"{resultado['cantidad']:.2f} {resultado['origen']} -> "
        f"{resultado['resultado']:.2f} {resultado['destino']}"
    )
    print(f"Regla semántica utilizada: {resultado['funcion_semantica']}")

    print("\n[Árbol de análisis - Lark]")
    print(arbol.pretty())


def main() -> None:
    try:
        from lark import Lark, Transformer
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Dependencia faltante: lark. Instale con `pip install lark` y vuelva a intentar."
        ) from exc

    class EvaluadorConversorLark(Transformer, EvaluadorConversor):
        pass

    parser_cli = argparse.ArgumentParser(
        description="Conversor de divisas con análisis léxico y sintáctico (Lark)."
    )
    parser_cli.add_argument(
        "--archivo",
        type=Path,
        help="Ruta de archivo .txt con una instrucción por línea. Cada instrucción debe finalizar con '$'.",
    )
    args = parser_cli.parse_args()

    entradas = cargar_entradas(args.archivo)
    parser = Lark(GRAMATICA, parser="lalr", maybe_placeholders=False)
    evaluador = EvaluadorConversorLark()

    for idx, entrada in enumerate(entradas, start=1):
        if not entrada.endswith("$"):
            raise ValueError(
                f"La cadena #{idx} no finaliza con '$'. "
                "Cada instrucción debe marcar fin de entrada con ese símbolo."
            )
        analizar(parser, evaluador, entrada)


if __name__ == "__main__":
    main()
