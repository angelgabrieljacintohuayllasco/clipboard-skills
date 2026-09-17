---
name: feature
description: Use to implement new functionality in an existing project — "agrega X", "implementa el login", "haz que ahora también...", "add this feature", "build this endpoint/screen/command", a ticket, or the next slice after intake/architecture. Runs the professional loop: read the project notes, plan a thin vertical slice, tasks, test-first, implement, run the gate, update docs. NO usar para bugs (fixer/triage), reestructuración sin cambio de comportamiento (refactor) ni proyectos desde cero sin spec (intake).
---

# Feature — construir una rebanada, verificada, sin romper lo que ya anda

## Overview

Construir bien no es escribir mucho código: es entregar **la rebanada más delgada que ya sirve a un usuario**, verificada, sin dejar el proyecto peor de lo que estaba. La IA puede generar 800 líneas en un minuto; el oficio está en decidir que solo 120 debían existir y que las 120 entran verdes.

## Cuándo usar

- Funcionalidad nueva en un repo que ya existe.
- La siguiente rebanada de un proyecto en marcha.
- Un ticket, un pedido concreto de usuario, un "ahora también necesito que...".

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Algo está roto | `triage` → `fixer` / `ui-bug` / `agent-debug` |
| Pedido vago o proyecto nuevo sin spec | `intake` |
| No hay restricciones ni gate en el repo | `constitution` primero (una vez, 15 min) |
| Solo mover/limpiar código sin cambiar comportamiento | `refactor` |
| El cambio implica decisión estructural grande | `architecture` primero |

## Regla de hierro: contexto antes de código

```
LEER spec + constitution + state/gotchas ANTES DE ESCRIBIR. SI NO EXISTEN, CREARLOS O DECLARAR QUE NO EXISTEN.
```

Orden de lectura, 5 minutos: `AGENTS.md` → `docs/project/state.md` (zonas rojas) → `gotchas.md` → el módulo que vas a tocar y sus tests. Escribir sin esto es repetir errores que el proyecto ya pagó.

## Proceso

### 1. Acotar la rebanada

Una rebanada vertical atraviesa todas las capas y deja algo usable: datos → lógica → borde (API/UI/comando). Nada de "primero todas las tablas, después toda la lógica": eso solo se puede probar al final, que es cuando ya no hay tiempo.

Criterio de tamaño: **si no cabe en un diff que una persona pueda revisar de una sentada (~400 líneas), pártela.** Si necesitas partirla, la primera parte debe seguir sirviendo para algo.

### 2. Plan corto y explícito (antes de tocar archivos)

- Archivos que se van a crear/modificar y por qué.
- Qué criterios de aceptación cubre (AC-n del spec).
- Qué NO incluye esta rebanada.
- Riesgos: qué se puede romper de lo existente.
- Decisión abierta → pregúntala ahora con recomendación por defecto, no a mitad del código.

Si el plan revela una decisión estructural (nueva dependencia, nuevo servicio, cambio de esquema), pasa por `architecture` y registra un ADR.

### 3. Test primero sobre el comportamiento acordado

Escribe el test del AC, mírelo fallar, implementa lo mínimo, mírelo pasar. Para código de interfaz donde el test-first no rinde, invierte el orden pero **no te saltes el test**: la rebanada no está hecha sin él.

### 4. Implementar bajo la constitución

- Estilo, límites de tamaño y complejidad: `code-standard` + la tabla de la constitución.
- Reusa lo que ya existe en el repo antes de crear paralelos: buscar primero (`grep` del concepto), crear después. La duplicación en proyectos asistidos por IA nace de no mirar si ya estaba.
- Dependencia nueva solo con justificación escrita: qué problema resuelve, qué pesa, qué la mantiene viva, y qué pasa si mañana desaparece.
- Un cambio = un propósito. Si ves un bug al pasar, anótalo; no lo mezcles.

### 5. Gate y cierre

1. `quality-gate` completo. BLOQUEA = no está listo, sin importar cuánto funcione en tu prueba manual.
2. Prueba manual del camino real (una vez, la que el gate no puede replicar: cómo se siente).
3. Actualiza `docs/project/state.md` (qué entró, qué quedó pendiente) y `gotchas.md` si descubriste una trampa.
4. Commit con mensaje que explique el porqué, no el qué del diff.

## Stop-loss

| Señal | Acción |
|---|---|
| 3 intentos y el mismo test sigue rojo | Para. El problema es el diseño o el entendimiento, no el código. Vuelve al plan. |
| El diff creció más de 2x lo planeado | Para y parte la rebanada. |
| Hay que "tocar todo" para agregar algo chico | Es acoplamiento: `tech-debt` / `refactor` antes de seguir. |
| Aparece una decisión de negocio no prevista | Pregunta. No la decidas tú en silencio. |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Ya que estoy, agrego también esto otro" | Alcance no acordado = trabajo no pagado y riesgo no evaluado. Anótalo como propuesta. |
| "Lo hago genérico por si mañana..." | YAGNI. Lo genérico sin segundo caso real es complejidad hoy por un beneficio imaginario. Espera al tercer caso. |
| "Copio este bloque y lo adapto" | Tercera copia = extracción obligatoria. Primera y segunda, aceptables si son de verdad distintas. |
| "Los tests los agrego al final de la feature" | Al final la forma del código ya impide probarlo. El test guía el diseño. |
| "Funciona en mi prueba, listo" | El gate decide. Tu prueba manual cubre un camino de muchos. |
| "No leo las notas, exploro el código" | El código dice qué hace. Las notas dicen por qué, y qué ya explotó antes. |

## Formato de salida

- Rebanada entregada: qué hace ahora el usuario que antes no podía.
- AC cubiertos y sus tests.
- Archivos tocados (ruta:línea de lo importante).
- Salida real del gate.
- Fuera de alcance / pendiente, y decisiones abiertas si quedaron.
- Notas del proyecto actualizadas.
