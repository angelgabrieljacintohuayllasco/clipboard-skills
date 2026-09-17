---
name: project-memory
description: Use at the START of work on any project (read the notes before exploring code) and at the END of any session with real progress (bug fixed, decision made, gotcha found) — also on "documenta esto", "guarda lo que aprendimos", "actualiza las notas", "write this down", "update the docs", or when a project has no AGENTS.md / notes at all. Keeps durable engineering memory as plain markdown in the repo (AGENTS.md + docs/project/) with an optional Obsidian vault mirror. NO es el README público (readme-generator) ni la memoria personal del asistente.
---

# Project-Memory — lo que no se escribe se vuelve a pagar

## Overview

Cada sesión de IA empieza en frío. Sin memoria escrita, el agente re-explora el repo, vuelve a proponer lo que ya falló y vuelve a pisar la trampa que costó tres horas el mes pasado. La memoria útil no es el historial de commits (dice **qué** cambió) ni el README (dice cómo instalar): es el registro del **por qué**, de lo que explotó y de lo que no hay que tocar.

El estándar de facto para esto son archivos markdown en el propio repo: `AGENTS.md` en la raíz como punto de entrada para cualquier agente, y un directorio de notas del proyecto. Texto plano, versionado con el código, legible por cualquier herramienta, sin servicio de por medio.

## Cuándo usar

- **Al empezar**: antes de explorar código, leer las notas. Siempre.
- **Al cerrar** una sesión con: bug resuelto, decisión tomada, trampa descubierta, arquitectura cambiada, entrega hecha.
- Proyecto sin notas que va a seguir vivo → crearlas (10 minutos).

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| README público del repo | `readme-generator` |
| Notas de release | `changelog-generator` |
| Cambio trivial sin aprendizaje | no escribir nada; el ruido también cuesta |
| Preferencias personales del usuario, no del proyecto | memoria propia del asistente |

## Regla de hierro: leer antes de explorar, escribir antes de cerrar

```
SESION QUE EMPIEZA SIN LEER LAS NOTAS REPITE ERRORES YA PAGADOS.
SESION QUE CIERRA SIN ESCRIBIRLAS OBLIGA A PAGARLOS OTRA VEZ.
```

## Estructura (portátil, en el repo)

```
AGENTS.md                         # raíz: qué es, comandos, reglas, zonas rojas, enlaces
docs/project/
  spec.md                         # qué se construye y criterios de aceptación
  constitution.md                 # restricciones y umbrales verificables
  architecture.md                 # mapa de módulos, flujo de datos, integraciones
  decisions/ADR-000X-<tema>.md    # decisiones caras de revertir
  state.md                        # estado actual, backlog, "qué NO tocar"
  bugs.md                         # síntoma → causa raíz → fix → prevención
  gotchas.md                      # trampas no obvias del stack o del dominio
  runbook.md                      # cómo desplegar, cómo revertir, qué hacer si se cae
```

Convenciones: fechas absolutas (nunca "ayer"), un tema por archivo, lo nuevo arriba, enlaces relativos entre notas. Escribe denso: el lector es un agente con contexto limitado o tú dentro de tres meses.

### Espejo opcional en Obsidian (u otra bóveda de notas)

Si existe una bóveda personal, replica **una carpeta por proyecto** con los mismos archivos y un índice que enlace a todos los proyectos. Reglas:

- La fuente de verdad es el repo; la bóveda es el índice transversal (lo que cruza proyectos: infraestructura, proveedores, aprendizajes generales).
- La ruta de la bóveda se configura una vez en `AGENTS.md` (`notas_externas: <ruta>`); nunca se asume.
- **Nunca** se copian secretos, tokens, volcados de base ni datos personales a la bóveda ni al repo.
- Si la bóveda se sincroniza a la nube, copiar archivos no es sincronizar: verificar que el cliente terminó de subir.

## Qué escribir dónde

| Aprendizaje | Archivo | Formato mínimo |
|---|---|---|
| Bug resuelto | `bugs.md` | **Síntoma** (log o frase real) → **Causa raíz** → **Fix** (commit) → **Prevención** (el test que ahora lo cubre) |
| Trampa descubierta | `gotchas.md` | Qué engaña, cómo se manifiesta, cómo evitarla |
| Decisión estructural | `decisions/ADR-*.md` + mención en `architecture.md` | contexto, opciones, elección, consecuencias |
| Avance de sesión, pendientes, zonas rojas | `state.md` | fecha, qué entró, qué falta, qué NO tocar y por qué |
| Comandos, reglas, entrada para agentes | `AGENTS.md` | corto: construir, probar, gate, límites |
| Cómo se opera en producción | `runbook.md` | desplegar, revertir, restaurar respaldo, a quién avisar |

**El valor está en la causa raíz y en la evidencia** (el log exacto, la versión exacta, el número medido). Un bug documentado sin causa raíz es ruido con formato.

## Al abrir la sesión (2 minutos)

1. `AGENTS.md` → comandos y reglas.
2. `state.md` → dónde quedó todo y qué no tocar.
3. `gotchas.md` + `bugs.md` si vas a tocar código.
4. `spec.md` + `constitution.md` si vas a construir o verificar.

Di en voz alta lo que encontraste: *"Las notas dicen que el módulo de sesiones ya rompió dos veces por X; lo tengo en cuenta."* Eso demuestra que la memoria se usó, no solo que existe.

## Al cerrar (5 minutos)

Actualiza solo lo que esta sesión tocó. Reescribir notas enteras destruye historial útil. Si no hubo aprendizaje real, dilo y no escribas.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Exploro el código, es más rápido" | El código no guarda por qué se descartó la solución obvia ni qué explotó a las 3 AM. |
| "Lo documento después" | "Después" = nunca, y el contexto ya se evaporó. Cinco minutos ahora valen horas luego. |
| "El commit ya lo dice" | El commit dice qué cambió. No dice el síntoma real ni cómo evitar la recaída. |
| "Es obvio, no hace falta anotarlo" | Obvio para ti, hoy, con el contexto caliente. Esa es exactamente la información que se pierde primero. |
| "Actualizo todo el vault de paso" | Solo lo que la sesión tocó. Las reescrituras masivas borran evidencia. |

## Formato de salida

Al abrir: lista de notas leídas + el hallazgo que cambia el plan.
Al cerrar:

```
Notas actualizadas:
  - docs/project/bugs.md — bug #7 (causa raíz: reloj del contenedor en UTC)
  - docs/project/state.md — sesión 2026-09-16, pendiente: migrar pagos
Espejo externo: sincronizado / no aplica
```
