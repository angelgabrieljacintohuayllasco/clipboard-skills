---
name: triage
description: Use when a bug or problem report arrives and it's unclear whether to patch, refactor, debug the AI agent, or rebuild — especially after previous fix attempts failed, the project feels unmaintainable, or the user says "este proyecto está de basura", "no se puede arreglar", "otra vez el mismo bug", "ya lo intentamos antes", "this codebase is a mess". Read-only diagnosis with metrics, then a verdict and the skill to invoke. NO edita código durante el triage.
---

# Triage — ¿fix, refactor, agent-debug o rebuild?

## Overview

Decide QUÉ tipo de intervención necesita el proyecto ANTES de tocar código. El error más caro no es un mal fix: es aplicar la herramienta equivocada — parchar lo que necesita reestructura, o reescribir lo que necesitaba un cambio de una línea.

**Regla de hierro: cero ediciones de código durante el triage.** Solo lectura, métricas y veredicto.

## Cuándo usar

- Reporte de bug en un proyecto que no conoces o que ya falló antes.
- El mismo síntoma ya se "arregló" 2+ veces y volvió.
- Archivos gigantes, sin tests, historial de fixes que rompen otras cosas.
- Duda entre arreglar y rehacer.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Diagnóstico claro y ruta evidente | invoca directo la skill correspondiente |
| No arranca por entorno | `env-doctor` |
| Pregunta teórica sin proyecto | `consulta` |
| Pedido nuevo, no un bug | `intake` |

## Proceso (30 minutos máximo, solo lectura)

1. **Memoria del proyecto primero**: `AGENTS.md`, `docs/project/state.md`, `bugs.md`, `gotchas.md` (o la bóveda de notas si el proyecto usa una). El historial de bugs es la mejor evidencia de repetición.
2. **Medir el repo**, no opinar:
   - Tamaño de los archivos principales (monolito = un archivo > 1.500 líneas).
   - ¿Hay tests que se puedan ejecutar? ¿Pasan hoy?
   - Cobertura aproximada y complejidad máxima si hay herramienta.
   - `git log` de los últimos 20-30 commits: **cuántos son "fix" sobre el mismo archivo o el mismo síntoma**.
   - Cruce churn × complejidad: qué archivo concentra los cambios recientes.
   - ¿Existe constitución/gate? ¿Corre?
3. **Clasificar el síntoma**: ¿error puntual con traza? ¿comportamiento errático de un agente IA? ¿visual? ¿funciona pero da miedo tocarlo? ¿no arranca?
4. **Veredicto** con la tabla.

## Tabla de ruteo

| Evidencia dominante | Ruta |
|---|---|
| Error puntual, causa localizable, proyecto estructuralmente sano | `fixer` |
| Bot/agente IA decide mal: flujo, estado, prompt, clasificadores, herramientas | `agent-debug` |
| Síntoma visual, de maquetación o de interacción | `ui-bug` |
| Funciona, pero cada cambio rompe otra cosa; monolito; miedo a tocar | `refactor` (antes: `test-strategy` para la red) |
| Sin tests + sin estructura + efectos cruzados + la arquitectura ya no soporta lo pedido + repetición documentada de fixes | `rebuild` |
| No arranca / entorno roto | `env-doctor` |
| Lento pero correcto | `performance` |
| Falla en producción y nadie se entera | `observability` |
| Deuda difusa, hay que priorizar antes de intervenir | `tech-debt` |
| **2+ intentos de fix fallidos sobre el MISMO síntoma** | **prohibido volver a `fixer`** — elegir entre `agent-debug`, `refactor` o `rebuild` según lo de arriba |

Señales combinadas: monolito + comportamiento raro de IA → `agent-debug` primero (encontrar la capa real), `refactor` después como prevención. El fix inmediato y la deuda estructural son dos entregables distintos: nombra los dos.

## Lo que el triage también debe detectar

- **No hay gate ni umbrales** → la falta de verificación es parte del diagnóstico: `constitution`.
- **No hay notas del proyecto** → cada sesión re-explora y repite errores: `project-memory`.
- **No hay tests ejecutables** → cualquier intervención es a ciegas: `test-strategy` antes que nada.
- **El proyecto no tiene dueño claro de la decisión** → decir quién tiene que decidir y qué.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es solo una línea, la arreglo de una" | Si el síntoma ya reapareció antes, la línea no es la causa. |
| "Triage es burocracia" | 30 minutos de lectura contra días de ciclo fix → rompe → fix. |
| "Rebuild es admitir derrota" | La mayoría de los rewrites cuestan mucho más de lo previsto; pero parchar un proyecto inmantenible también es tirar plata. El veredicto honesto gana en ambas direcciones. |
| "No hay notas de este proyecto" | Entonces el triage incluye recomendar crearlas: la falta de memoria escrita **es** parte del diagnóstico. |
| "Miré el código y me parece que..." | Sin métricas, "me parece" es gusto. Cuenta líneas, corre `git log`, mide. |

## Formato de salida

- **Veredicto**: skill a invocar (una principal, opcional una secundaria como deuda).
- **Evidencia**: 3-5 hechos medidos (líneas, tests, repetición en el historial, bugs recurrentes).
- **Qué NO hacer**: la ruta descartada y por qué.
- **Faltantes estructurales**: gate, tests o notas que no existen.
- Si falta información para decidir: decirlo y pedir exactamente qué (log, captura, conversación real). No adivinar.
