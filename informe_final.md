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

- `parsear_tokens(...)`: valida la estructura sintáctica y construye el árbol.
- `convertir(...)`: regla semántica principal para convertir entre monedas.
- `analizar_linea(...)`: integra análisis léxico + sintáctico + semántico por línea.
- `analizar_texto(...)`: procesa múltiples instrucciones.

## d) Capturas del programa en ejecución

> Inserte aquí capturas de la app de escritorio:
> - Tabla del analizador léxico.
> - Resultado sintáctico/semántico.
> - Árbol de análisis.

## e) Hoja de desempeño del grupo

| Integrante | Actividad principal | % trabajo |
|---|---|---|
| Integrante 1 | Diseño de gramática y parser | 35% |
| Integrante 2 | Interfaz de escritorio y tabla léxica | 35% |
| Integrante 3 | Semántica de conversión y pruebas | 30% |

## f) Bibliografía base

1. Python `tkinter` Documentation. https://docs.python.org/3/library/tkinter.html
2. Python Regular Expression HOWTO. https://docs.python.org/3/howto/regex.html
3. Python Official Documentation. https://docs.python.org/3/
