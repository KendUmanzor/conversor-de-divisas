# Proyecto: Conversor de Divisas con Analizador Léxico y Sintáctico

Este repositorio implementa un **traductor básico** en Python para un mini-lenguaje de conversión de divisas.

## Requisitos

- Python 3.10+
- `lark`

Instalación de dependencia:

```bash
pip install lark
```

## Cómo ejecutar

### 1) Con entradas por defecto (internas en el programa)

```bash
python3 conversor.py
```

### 2) Con archivo de texto

```bash
python3 conversor.py --archivo input_ejemplo.txt
```

## Gramática de entrada

Formato por línea:

```text
convertir <cantidad> <MonedaOrigen> a <MonedaDestino>$
```

Ejemplo:

```text
convertir 1 DolarEstadounidense a LempiraHondureño$
```

> La cadena debe terminar obligatoriamente con `$` para indicar fin de entrada.

## Salida que genera

- Tabla del **analizador léxico**:
  - línea
  - columna
  - tipo de token
  - valor
- Resultado de la operación (analizador sintáctico + semántica)
- Árbol sintáctico generado por **Lark**

## Monedas soportadas

- DolarEstadounidense
- LempiraHondureño
- QuetzalGuatemalteco
- ColonCostarricense
- Peso_Mexicano
- Euro
