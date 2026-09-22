---
name: batch
description: "Apply one repetitive change across many files: rename everywhere, update all imports, add error handling to every endpoint, codebase-wide migration or formatting."
---

# Batch — un cambio, muchos destinos, cero sorpresas

## Overview

Un cambio repetitivo aplicado a mano en 40 archivos produce 40 oportunidades de equivocarse y una revisión imposible. Aplicado sin plan, produce algo peor: un diff enorme donde nadie distingue lo mecánico de lo que cambió de verdad.

La disciplina es simple: **enumerar, definir la transformación, mostrar un ejemplo, aplicar, verificar y reportar lo que se saltó.**

## Proceso

1. **Enumerar destinos.** Búsqueda exhaustiva de todos los archivos o puntos que coinciden. Lista el conteo. Si son muchos (>15) o el criterio es ambiguo, confirma antes de tocar nada.
2. **Definir la transformación con precisión.** Enúnciala como una regla que trate igual a todos los casos (mismo patrón de entrada → mismo patrón de salida). Muestra **un ejemplo real antes/después** y consigue un visto bueno antes de aplicar en masa.
3. **Elegir el modo de ejecución:**
   - **Mecánico e idéntico** (renombrar, cambiar un import, envolver una llamada): edición automatizada, determinista.
   - **Depende del contexto** (cada punto exige criterio, como el manejo de errores adecuado a cada caso): uno por uno, revisando. No es trabajo de sustitución masiva.
4. **Aplicar** llevando una lista de hechos y saltados, con el motivo de cada salto.
5. **Verificar.** `quality-gate` completo: compilación, tipos, tests y linter. Un cambio masivo que rompe la compilación no está hecho. Si hay tests, deben pasar **antes y después** — si no había forma de verificar, dilo como riesgo.
6. **Commit aparte.** Los cambios mecánicos van en su propio commit, separados de cualquier cambio de comportamiento. Así el siguiente lector puede ignorar el ruido y revisar lo que importa.

## Reglas

- Nunca afirmes "aplicado a los N archivos" sin haberlos editado: cuenta y confirma.
- Respeta el estilo de cada archivo (indentación, convenciones). Cambio uniforme, **no** estilo uniforme impuesto a archivos distintos.
- Si un destino no encaja en el patrón, sáltalo y repórtalo: no fuerces una edición mala por consistencia estadística.
- Los fallos parciales se dicen explícitamente: "12 de 14 hechos, 2 saltados porque…".
- Ediciones amplias o difíciles de revertir: muestra el plan y un ejemplo antes de tocar archivos, y trabaja sobre una rama.
- Si la sustitución puede afectar cadenas de texto, comentarios o datos además de código, acota el patrón: los renombrados globales ciegos corrompen contenido.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es un reemplazo simple, va directo" | Los reemplazos simples atrapan coincidencias en comentarios, cadenas y nombres parecidos. Muestra el ejemplo primero. |
| "Reviso el diff al final" | Un diff de 3.000 líneas no se revisa: se aprueba. Por eso el ejemplo va antes. |
| "Aprovecho y de paso formateo todo" | Mezclar formateo con el cambio real hace la revisión imposible. Commits separados. |
| "Si algo se rompe, los tests avisan" | Solo si existen y cubren esa zona. Si no, lo dices como riesgo asumido. |

## Formato de salida

Destinos encontrados (conteo), regla de transformación, ejemplo antes/después, lista de aplicados y saltados con motivo, salida real de la verificación, y commits generados.
