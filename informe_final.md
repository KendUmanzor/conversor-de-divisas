# Informe Final - Proyecto Conversor de Divisas

## a) Detalle de tokens, patrones y lexemas

| Token | Patrón | Ejemplo de lexema |
|---|---|---|
| `CONVERTIR` | `(?i)convertir` | `convertir` |
| `CANTIDAD` | `\d+(\.\d+)?` | `1`, `150.75` |
| `MONEDA` | `[A-Za-zÁÉÍÓÚáéíóúÑñ_]+` | `DolarEstadounidense` |
| `A` | `(?i)a` | `a` |
| `FIN` | `$` | `$` |

## b) Reglas de producción y gramática

```ebnf
inicio: instruccion FIN
instruccion: CONVERTIR CANTIDAD MONEDA A MONEDA
```

## c) Funciones (reglas semánticas) usadas

- `instruccion(...)` en `EvaluadorConversor`: valida monedas, aplica conversión y retorna resultado.
- `normalizar_moneda(...)`: transforma texto para mapear tasas.
- `analizar(...)`: integra fase léxica, sintáctica y despliegue del árbol.

## d) Capturas del programa en ejecución

> Inserte aquí capturas de terminal mostrando: tabla léxica, resultado de conversión y árbol de análisis.

## e) Hoja de desempeño del grupo

| Integrante | Actividad principal | % trabajo |
|---|---|---|
| Integrante 1 | Gramática y parser Lark | 35% |
| Integrante 2 | Analizador léxico y tabla | 30% |
| Integrante 3 | Conversión semántica y pruebas | 35% |

## f) Bibliografía base

1. Lark Parser Documentation. https://lark-parser.readthedocs.io/
2. Python Regular Expression HOWTO. https://docs.python.org/3/howto/regex.html
3. Python Official Documentation. https://docs.python.org/3/
