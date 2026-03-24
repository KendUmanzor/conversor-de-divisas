# Proyecto: Conversor de Divisas (Aplicación de Escritorio)

Este proyecto implementa un traductor básico en Python para un mini-lenguaje de conversión de divisas, con:

- **Analizador léxico** (línea, columna, tipo, valor).
- **Analizador sintáctico** (validación de gramática).
- **Reglas semánticas** (cálculo de conversión).
- **Árbol sintáctico** visual en la interfaz.

La app es de **escritorio** usando `tkinter`.

## Ejecución

### Modo aplicación de escritorio (recomendado)

```bash
python3 conversor.py
```

Al ejecutar ese comando se abre una ventana con:
- área de entrada,
- botón para cargar TXT,
- botón Ejecutar,
- pestañas para léxico, sintáctico y árbol.

### Modo terminal (opcional para pruebas)

```bash
python3 conversor.py --cli
```

## Formato de entrada

Una instrucción por línea:

```text
convertir <cantidad> <MonedaOrigen> a <MonedaDestino>$
```

Ejemplo:

```text
convertir 1 DolarEstadounidense a LempiraHondureño$
```

> Cada línea debe finalizar con `$`.

## Monedas soportadas

- DolarEstadounidense
- LempiraHondureño
- QuetzalGuatemalteco
- ColonCostarricense
- Peso_Mexicano
- Euro
