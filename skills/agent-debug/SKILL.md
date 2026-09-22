---
name: agent-debug
description: "LLM bot or agent behaves wrong: bad replies, ignores prompt, wrong/duplicate tool calls, loops, state bugs. \"el bot responde cualquier cosa\", \"no respeta el prompt\". Not for stack-trace errors (fixer)."
---

# Agent-Debug — cuando el bug vive entre el prompt, el estado y los datos

## Overview

Los bugs de agentes casi nunca están en una línea de código: viven en la interacción entre **prompt**, **máquina de estados**, **clasificadores y extractores**, **definición de herramientas** y **datos reales**. Parchar código sin identificar la capa correcta produce el ciclo infinito: cada ajuste arregla un caso y rompe otro.

Regla de fondo: el modelo ejecuta lo que le das. **Cuatro de las cinco capas son código tuyo.**

## Cuándo usar

- El bot responde o decide mal en conversaciones reales (no se cae: se equivoca).
- Reenvía datos ya rechazados, ignora instrucciones, se salta pasos del flujo, se queda mudo.
- Un clasificador o una expresión regular interpreta mal respuestas humanas.
- Llamadas a herramientas: la equivocada, con argumentos viejos, o dos veces.
- Bucles: repite la misma pregunta o la misma acción.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Traza de error, caída, fallo de compilación | `fixer` |
| Ni conecta (sesión, credenciales, entorno) | `env-doctor` |
| Construir el bot o cambiar de canal | `bot-dev` |
| Rediseñar el flujo completo | acordar rediseño explícito, o `rebuild` |

## Regla de hierro: reproducir desde la conversación real

```
SIN LA CONVERSACION REAL (MENSAJES + ESTADO GUARDADO + REGISTRO), NO HAY DIAGNOSTICO.
```

Consigue: la transcripción o captura del chat, el estado persistido de esa conversación, los registros con marcas de tiempo y la versión que estaba corriendo. Reconstruye la secuencia mensaje a mensaje **antes** de leer código. Prohibido "seguro es el prompt" sin evidencia.

## Diagnóstico por capas (en este orden)

| # | Capa | Pregunta | Trampa típica |
|---|---|---|---|
| 1 | **Estado** | ¿Qué estado tenía la conversación en cada mensaje? ¿La clave del estado es la correcta (por conversación, por usuario, por caso, por sucursal)? | Un dato se captura una sola vez con "si está vacío, pedirlo" y nunca se actualiza → reenvía el valor rechazado. Un veredicto guardado bloquea el reintento legítimo de otro caso. |
| 2 | **Prompt** | ¿Hay **dos fuentes** de instrucciones que se contradicen (una plantilla vieja en configuración y otra generada dinámicamente)? ¿Cuál gana por orden? | El modelo obedece la instrucción vieja que nadie recordaba. Revisar siempre ambos lados y **buscar qué borrar**, no qué agregar. |
| 3 | **Clasificadores y extractores** | ¿La expresión de aprobación coincide dentro de su propia negación? ¿Se evalúa la negación primero? ¿Cubre el vocabulario que la gente usa de verdad? | "NO procede" clasificado como aprobación. Respuestas reales no contempladas: una sola palabra, mayúsculas, con emoji, con falta de ortografía. |
| 4 | **Herramientas** | ¿La herramienta relee estado viejo en vez de recibir argumentos explícitos? ¿Hay dos mecanismos activos a la vez (etiquetas de texto **y** llamadas de función) que ejecutan dos veces? ¿Los controles de negocio están dentro de la herramienta o confiados al modelo? | Doble ejecución por dos caminos paralelos. Controles anti-duplicado escritos en el prompt en vez de en el código. |
| 5 | **Datos del mundo real** | ¿El formato real difiere del asumido? | El operador responde con una foto y el texto en el pie, y el bot solo lee texto. Nombres con espacios dobles, documentos con longitud distinta a la esperada, mensajes reenviados, respuestas a mensajes viejos. |

La capa culpable se confirma reproduciendo: mismo estado + mismo mensaje → mismo mal resultado. **Si no puedes reproducirlo, no encontraste la causa.**

## Después del fix

1. **Caso de regresión** con la frase y la secuencia reales del reporte, en el conjunto de pruebas del proyecto. El historial de bugs es la mejor especificación que tienes.
2. **Verificación de extremo a extremo**: reproducción de la conversación exacta del reporte, más las variantes cercanas (negación, mayúsculas, con emoji).
3. **Controles al código**: si el bug fue que el modelo "no obedeció", la corrección correcta casi nunca es una instrucción más; es mover ese control a código.
4. **Documentar** en `bugs.md`: síntoma real → capa culpable → causa raíz → fix → prevención.
5. **Cuidado con el costo**: iterar contra un modelo de pago quema dinero. Prueba las capas 1, 3 y 4 con pruebas unitarias puras; usa el modelo solo para confirmar.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Ajusto el prompt y listo" | Si la causa es estado o clasificador, el prompt nuevo solo maquilla. El modelo no puede obedecer instrucciones sobre datos que el código le pasa mal. |
| "Agrego una instrucción más" | Los prompts que crecen por acumulación de parches terminan contradiciéndose. Busca primero qué instrucción vieja hay que borrar. |
| "El modelo es tonto" | El modelo ejecuta lo que prompt + estado + herramientas le entregan. Cuatro de cinco capas son tuyas. |
| "Refuerzo el control en el prompt" | Los controles de negocio (no duplicar, no cerrar sin datos, no prometer precios) van en código. Una instrucción es una sugerencia estadística. |
| "Le subo la temperatura / cambio de modelo" | Cambiar el modelo sin entender la capa culpable mueve el bug de lugar y borra tu evidencia. |

## Formato de salida

- **Capa culpable** (1-5) con la evidencia de la conversación real.
- **Fix aplicado** por capa (lo que se borró del prompt cuenta tanto como lo que se agregó).
- **Caso de regresión** agregado + resultado de la reproducción.
- **Qué control se movió a código**, si aplica.
- **Prevención** en una línea para las notas del proyecto.
