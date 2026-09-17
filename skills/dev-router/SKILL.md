---
name: dev-router
description: Use at the START of any software work when the next move isn't obvious — "hazme un CRM de WhatsApp", "quiero una app", "ayúdame con mi proyecto", "build me an app", "add this feature", vague or large requests, unclear if it needs discovery, architecture, a feature slice, a fix, tests, or deploy. Routes to the right skill of the engineering pack and enforces the order of the cycle (intake → constitution → architecture → feature → quality-gate → deploy). NO usar si el pedido ya es concreto y la skill correcta es evidente.
---

# Dev-Router — qué skill toca, en qué orden

## Overview

El error más caro en desarrollo asistido por IA no es escribir mal el código: es **empezar a escribirlo antes de que existan el acuerdo, las restricciones y la forma de verificar**. Sin eso, la IA acelera y lo que acelera es la deuda (DORA 2026: la IA amplifica el sistema que ya tienes — si el pipeline es débil, produce deuda más rápido).

Esta skill decide **qué se hace primero** y delega. No escribe código.

## Regla de hierro: nada de código sin las tres respuestas

```
1. ¿QUÉ construimos y cómo sabremos que está bien?   → spec + criterios de aceptación
2. ¿BAJO QUÉ RESTRICCIONES?                           → constitución (límites + umbrales)
3. ¿CÓMO SE VERIFICA SIN LEER CADA LÍNEA?             → gate automático (comandos que corren)
```

Si falta alguna, la primera tarea es conseguirla, no programar. Un prototipo desechable también las necesita — solo que en su nivel más bajo (perfil P1).

## Mapa del ciclo

```
PEDIDO
  │
  ├─ vago / proyecto nuevo ─────────────► intake ──► constitution ──► architecture ──► feature
  ├─ funcionalidad nueva en repo vivo ──► feature (si no hay constitución: constitution primero)
  ├─ algo está roto ────────────────────► triage ──► fixer / ui-bug / agent-debug / refactor / rebuild
  ├─ "no sé si esto vale la pena" ──────► valida-idea
  ├─ duda técnica, sin tocar código ────► consulta
  └─ terminado, hay que publicarlo ─────► quality-gate ──► deploy ──► project-memory
```

## Tabla de ruteo

| Lo que trae el usuario | Skill | Por qué |
|---|---|---|
| "Hazme un X" (CRM, bot, app, web, script) | `intake` | Falta spec y acuerdo de restricciones. Nunca saltar a código. |
| Proyecto nuevo aprobado, sin repo | `constitution` → `architecture` | Los gates se instalan el día 1, no al final. |
| Repo vivo + funcionalidad nueva | `feature` | Slice vertical bajo la constitución vigente. |
| "¿Qué stack / cómo estructuro esto?" | `architecture` | Decisión con ADR, no gusto personal. |
| "No sé qué probar / no hay tests" | `test-strategy` | Diseñar la red antes de exigir cobertura. |
| "¿Está listo para entregar?" | `quality-gate` | Métricas y comandos, no opinión. |
| "Se ve feo el código / está enredado" | `code-standard` (cómo escribir) o `refactor` (mover código) | Uno norma, el otro ejecuta. |
| "Esto ya no se sostiene" | `tech-debt` → `refactor` / `rebuild` | Inventario antes de intervención. |
| Bug reportado | `triage` | Clasificar antes de parchar. |
| Publicar / servidor / entorno | `deploy` | Release con rollback ensayado. |
| "No sé qué pasa en producción" | `observability` | Sin señales, todo es adivinanza. |
| "Va lento" | `performance` | Medir antes de optimizar. |
| Datos, migraciones, backups | `data-layer` | Los datos son lo único irrecuperable. |
| Seguridad de lo que se construye | `app-security` | Baseline OWASP por tipo de app. |
| Dominio específico | `web-app`, `api-backend`, `bot-dev`, `automation`, `desktop-app`, `mobile-app` | Trampas propias de cada plataforma. |
| Cierre de sesión con avance real | `project-memory` | Lo que no se documenta se vuelve a pagar. |

## Cómo hablarle a quien pide

Detecta el registro en el primer mensaje y adáptate; nunca al revés.

| Señal | Registro | Cómo responder |
|---|---|---|
| Menciona stack, versiones, errores, arquitectura | **Programador** | Conversación entre pares. Directo, técnico, sin explicar lo básico. Propón trade-offs con nombres propios. |
| Habla de resultado de negocio, no de tecnología | **Cliente / vibecoder** | Traduce cada decisión técnica a consecuencia: tiempo, dinero, riesgo, qué se rompe si sale mal. Nunca pidas que elija entre dos cosas que no entiende — recomienda una y explica qué pasa si te equivocas. |

Regla: **toda pregunta lleva recomendación por defecto.** "¿Postgres o SQLite?" sin más es trasladarle tu trabajo. "Recomiendo SQLite porque X; si mañana necesitas Y, migramos, cuesta Z. ¿Vamos así?" es hacer el trabajo.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "El usuario quiere ver algo ya, programo y después ordeno" | "Después" nunca llega y el costo de retrofit de gates crece con cada archivo. 20 minutos de intake y constitución ahorran semanas. |
| "Es un proyecto chico, no necesita proceso" | Entonces usa el perfil P1 (gates mínimos). Perfil bajo ≠ sin proceso. |
| "Sé lo que quiere, no hace falta preguntar" | Si aciertas, perdiste 3 minutos. Si fallas, perdiste el proyecto entero. Nadie encargó un CRM esperando lo que tú imaginaste. |
| "Ya hay mucho código, tarde para restricciones" | Se aplican al código NUEVO (clean as you code) y se hace ratchet. Nunca es tarde: es más barato ahora que mañana. |

## Formato de salida

- **Ruta**: skill principal + las 2 siguientes del ciclo.
- **Qué falta**: cuál de las tres respuestas (spec / restricciones / gate) no existe todavía.
- **Preguntas abiertas**: solo las que bloquean; cada una con su recomendación por defecto.
- Nunca escribas código desde esta skill. Delega e invoca.
