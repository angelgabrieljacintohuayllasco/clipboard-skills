---
name: dev-router
description: "Start of any software request when the right skill isn't obvious: \"hazme una app/CRM/web\", \"ayúdame con mi proyecto\", \"build me X\". Picks the skill and how much process the task deserves."
---

# Dev-Router — qué skill toca, en qué orden

## Overview

El error más caro en desarrollo asistido por IA no es escribir mal el código: es **empezar a escribirlo antes de que existan el acuerdo, las restricciones y la forma de verificar**. Sin eso, la IA acelera y lo que acelera es la deuda (DORA 2026: la IA amplifica el sistema que ya tienes — si el pipeline es débil, produce deuda más rápido).

Esta skill decide **qué se hace primero** y delega. No escribe código.

## Regla de hierro: el proceso se ajusta al tamaño, el resultado no se negocia

```
1. ¿QUÉ construimos y cómo sabremos que está bien?   → criterios de aceptación (aunque sean 3 líneas)
2. ¿BAJO QUÉ RESTRICCIONES?                           → constitución (o los defaults del perfil P1)
3. ¿CÓMO SE VERIFICA SIN LEER CADA LÍNEA?             → gate automático + mirar el resultado real
```

Las tres respuestas siempre existen, pero su tamaño es proporcional al pedido. El proceso es un medio: si produce documentos y preguntas en lugar de un resultado bueno, está mal aplicado.

| Tamaño del pedido | Qué se hace |
|---|---|
| **Concreto y chico** (una pantalla, un endpoint, un script, un fix, una web simple) | Se construye YA. Criterios y supuestos en 3–5 líneas al inicio de la respuesta, defaults del perfil P1, gate al final. Cero entrevista. |
| **Mediano** (una feature con varias piezas, una app chica) | Una sola ronda de ≤ 3 preguntas **solo si** la respuesta cambia lo que se construye; si no, supuestos en voz alta y a construir. |
| **Grande o para un cliente** (producto nuevo, semanas de trabajo, dinero de por medio) | `intake` → `constitution` → `architecture` → `feature`, completo. |

Ante la duda, construye con supuestos explícitos: es más fácil corregir algo concreto que discutir algo abstracto. Toda salida con UI pasa por `ui-design`; toda salida pasa por `code-standard`.

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
| "Hazme un X" grande o para un cliente (CRM, plataforma, app completa) | `intake` | Falta spec y acuerdo de restricciones. |
| "Hazme un X" chico y claro (landing, script, pantalla, bot simple) | skill del dominio directo | Construir con supuestos explícitos; no entrevistar. |
| Cualquier interfaz nueva o "se ve feo / genérico / vibecodeado" | `ui-design` | Sistema visual y verificación con capturas. |
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
| Seguridad de IA / agentes / código generado por IA | `ai-security` | OWASP LLM+Agentic, prompt injection, slopsquatting. |
| "Trabaja como programador senior / hazlo bien de verdad" | `agentic-coding` | El método: verificar-primero, contexto limpio, revisión adversarial. |
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
| "El usuario quiere ver algo ya, programo y después ordeno" | En un proyecto grande, "después" nunca llega. En uno chico, construir ya es lo correcto, pero con criterios y gate. |
| "Es un proyecto chico, no necesita proceso" | Usa el perfil P1 (gates mínimos). Perfil bajo ≠ sin proceso, y tampoco ≠ entrevista. |
| "Mejor pregunto todo antes de empezar" | En pedidos chicos, preguntar es trasladar trabajo. Supuestos en voz alta y un resultado concreto que se pueda corregir. |
| "Sé lo que quiere en un proyecto grande, no hace falta preguntar" | Si fallas, perdiste el proyecto entero. Nadie encargó un CRM esperando lo que tú imaginaste. |
| "Cumplí el proceso, así que el resultado está bien" | El proceso no mira la pantalla. Si el resultado se ve genérico o pobre, no está terminado. |
| "Ya hay mucho código, tarde para restricciones" | Se aplican al código NUEVO (clean as you code) y se hace ratchet. Nunca es tarde: es más barato ahora que mañana. |

## Formato de salida

- **Ruta**: skill principal + las 2 siguientes del ciclo.
- **Qué falta**: cuál de las tres respuestas (spec / restricciones / gate) no existe todavía.
- **Preguntas abiertas**: solo las que bloquean; cada una con su recomendación por defecto.
- Esta skill no escribe código: decide y **invoca en el mismo turno** la skill elegida (con la herramienta de skills) para que el trabajo empiece de inmediato, sin devolver solo un plan.
