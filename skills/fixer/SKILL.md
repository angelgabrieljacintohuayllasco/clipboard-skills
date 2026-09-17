---
name: fixer
description: Use when fixing bugs, resolving errors, diagnosing broken code, repairing imports, correcting config issues, patching production defects, troubleshooting build failures, fixing type errors, or resolving runtime exceptions in existing projects. También cuando el usuario pide corregir, arreglar o reparar código existente sin rehacerlo. Reproduce first, fix the root cause, leave a regression test. NO usar si el síntoma es visual (ui-bug), si el bot responde mal sin stack trace (agent-debug), o si ya fallaron 2 intentos sobre el mismo síntoma (triage).
---

# Fixer — corregir la causa, no callar el síntoma

## Overview

Corriges proyectos que existen. La misión no es rehacer: es **encontrar la causa raíz, arreglarla de forma quirúrgica y dejar una prueba que impida el regreso del bug**, respetando el estilo y la arquitectura que ya están.

Un fix sin prueba de regresión no es un fix: es una pausa. El mismo bug vuelve con otra cara, y la segunda vez cuesta más porque ya nadie recuerda el contexto.

## Cuándo NO usar fixer (rutear a otra skill)

Fixer es para bugs puntuales en proyectos estructuralmente sanos.

| Señal | Skill correcta |
|---|---|
| No está claro si conviene parchar, reestructurar o rehacer | `triage` |
| Bot/agente IA que decide o responde mal (prompt, estado, clasificadores, tools) sin stack trace | `agent-debug` |
| Síntoma visual, de maquetación o de interacción | `ui-bug` |
| Funciona, pero cada cambio rompe otra cosa / monolito inmantenible | `refactor` |
| No da para más y parchar es tirar tiempo | `rebuild` (tras `triage`) |
| No arranca por entorno (versiones, deps, puertos) | `env-doctor` |
| Es lento, no está roto | `performance` |
| No se sabe qué pasa en producción | `observability` |

**Stop-loss obligatorio**: si ya hubo **2 intentos de fix fallidos sobre el mismo síntoma** (en esta sesión o documentados en las notas del proyecto), STOP — prohibido un tercer parche. Invoca `triage`. El tercer parche sobre un síntoma recurrente es el inicio del ciclo fix → rompe → fix.

## Regla de hierro 1: reproducir antes de tocar

```
SI NO LO VISTE FALLAR, NO SABES QUE LO ARREGLASTE.
```

Orden: reproducir el fallo → escribir una prueba que falla por ese motivo → corregir → ver la prueba en verde. Si el bug no se puede reproducir, la primera tarea es conseguir cómo: pasos exactos, datos reales, versión, entorno, log completo. Un fix sobre un bug no reproducido es una apuesta.

## Regla de hierro 2: documentación antes de tocar lo externo

```
SI LA CORRECCION INVOLUCRA ALGO EXTERNO, CONSULTAR SU DOCUMENTACION ES OBLIGATORIO ANTES DE MODIFICAR.
```

"Algo externo" significa: librerías y paquetes de terceros y el código que los usa; dependencias declaradas y lockfiles; configuración de herramientas y frameworks; APIs y servicios remotos; código copiado de otros repositorios.

Antes de modificar una línea relacionada:

1. Identifica la **versión instalada** (lockfile, gestor de paquetes).
2. Busca la **documentación oficial de esa versión**.
3. Si sospechas incompatibilidad, revisa los **cambios que rompen** entre la versión instalada y la que asume el código.
4. Aplica la corrección citando la fuente consultada.

| Excusa | Realidad |
|---|---|
| "Ya conozco esta librería" | El conocimiento entrenado envejece; las APIs cambian entre versiones. |
| "Es un cambio de una línea" | Una línea con una API inexistente rompe el build igual. |
| "No hay tiempo de buscar docs" | Depurar un fix basado en una API imaginaria cuesta mucho más. |
| "La documentación no dirá nada nuevo" | Los cambios que rompen viven exactamente ahí. |

## Proceso

1. **Contexto**: lee las notas del proyecto (`bugs.md`, `gotchas.md`, `state.md`) antes de explorar el código. Puede que este bug ya tenga historia.
2. **Evidencia**: log completo, mensaje exacto, pasos de reproducción, versión, entorno. Nada de parafrasear el error.
3. **Reproducir** y capturar el fallo en una prueba automática.
4. **Causa raíz**: pregunta "¿por qué?" hasta que la respuesta sea una decisión de código, no un síntoma. *"Falla porque el valor es nulo"* no es causa raíz; *"el campo llega nulo porque la migración lo agregó sin valor por defecto y el código asume que existe"* sí lo es.
5. **Radio de impacto**: quién más usa lo que vas a cambiar. Buscar los usos, no suponerlos.
6. **Fix mínimo** en la causa, respetando estilo y arquitectura existentes.
7. **Verificar**: la prueba nueva pasa, el resto sigue pasando, y `quality-gate` completo en verde.
8. **Documentar** en `bugs.md`: síntoma real → causa raíz → fix → prevención.

## Restricciones

- NO reescribas módulos completos; correcciones quirúrgicas.
- NO mezcles fix con refactor ni con features nuevas. Un cambio, un propósito.
- NO agregues dependencias salvo necesidad estricta y justificada.
- NO cambies arquitectura ni reorganices carpetas.
- NO elimines código funcional "de paso".
- NO hagas cambios cosméticos ajenos al bug.
- NO toques nada externo sin consultar su documentación.

## Parches que no son fixes

| Parche | Por qué falla |
|---|---|
| `try/catch` alrededor del error | Silencia el síntoma; la causa sigue corrompiendo datos más adelante |
| Comprobación de nulo donde explotó | Tapa el hueco; el dato sigue llegando mal desde su origen |
| Reintento automático | Convierte un fallo determinista en uno intermitente |
| Aumentar el tiempo límite | Esconde un problema de rendimiento hasta que crezca más |
| Fijar una versión vieja sin entender | Deuda con fecha de explosión y superficie de seguridad |
| Dato corregido a mano en la base | Vuelve a pasar mañana, y ahora sin registro de por qué |

Están permitidos **como mitigación temporal declarada**, con causa raíz identificada y fecha para el arreglo real. Nunca como entrega final silenciosa.

## Señales de alerta — detente y consulta

- Vas a cambiar una llamada a una librería sin haber abierto su documentación en esta sesión.
- Escribes una opción de configuración "porque suena correcta".
- Subes o bajas una versión "a ver si así funciona".
- Pegas una solución de un foro sin contrastarla con la versión instalada.

## Formato de salida

Para cada corrección:

- **Síntoma**: el error real (mensaje textual), cómo se reprodujo.
- **Causa raíz**: la decisión de código que lo provoca.
- **Fix**: archivo:línea, qué cambió y por qué.
- **Prueba de regresión**: cuál, vista en rojo antes de verla en verde.
- **Verificación**: salida real del gate.
- **Documentación consultada**: URLs (obligatorio si se tocó algo externo; "N/A" solo si fue 100% código propio).
- **Notas del proyecto**: entrada agregada en `bugs.md`.
