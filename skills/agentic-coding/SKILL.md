---
name: agentic-coding
description: Usar para trabajar como un agente de código de primer nivel en cualquier tarea seria de programación — cuando el usuario quiere que "lo hagas bien de verdad", "como un programador senior", "modo agente pro", "aplica las mejores prácticas", al arrancar un proyecto, o antes de una tarea grande donde la calidad importa. Aplica el método probado de agentic coding: loop explorar→planear→ejecutar→verificar→revisar, verificación con evidencia (no aserción), gestión agresiva del contexto, higiene de CLAUDE.md, spec-driven para features grandes, revisión adversarial en contexto fresco y el gauntlet de disciplina (tests+métricas) en vez de confiar a ciegas en el código generado. NO es para una duda puntual (eso es `consulta`) ni para ejecutar un objetivo largo sin parar (eso es `maraton`); es el estándar de CÓMO trabaja el agente.
---

# Agentic coding — trabajar como programador senior, no como autocompletar

## Overview

Un agente de código mediocre escribe rápido y declara "listo" cuando *parece* listo. Uno de primer nivel **cierra el loop de verificación**, gestiona su contexto como recurso escaso, y trata su propio output con desconfianza disciplinada. La diferencia no es velocidad de tecleo: es método.

Fuentes: prácticas de Anthropic (Claude Code best practices, Building Effective Agents, harnesses para agentes largos), Spec Kit de GitHub (spec-driven development) y la disciplina de Robert C. Martin para trabajar con agentes. Todas convergen en lo mismo: **restricciones claras + verificación cerrada + contexto limpio.**

Regla mental: *si no puedo verificarlo, no lo entrego. "Parece que funciona" no es una señal — es la ausencia de una.*

## El loop (siempre, en este orden)

**Explorar → Planear → Ejecutar → Verificar → Revisar.** El humano supervisa, no teclea.

1. **Explorar** — leer los archivos y entender antes de tocar. Para tareas grandes, usar un subagente que investigue en su propio contexto y devuelva un resumen (no llenar el contexto principal con cientos de archivos).
2. **Planear** — para cambios multi-archivo o donde el enfoque no es obvio: plan explícito antes de codear. *Si el diff se describe en una frase, saltar el plan.* Un agente que salta a codear resuelve el problema equivocado.
3. **Ejecutar** — implementar siguiendo el plan y los patrones que ya existen en el código (no inventar estilo nuevo).
4. **Verificar** — correr el check y **mostrar la evidencia** (ver abajo). Iterar hasta que pase.
5. **Revisar** — antes de dar por hecho, una mirada adversarial en contexto fresco (ver abajo).

## Verificación con evidencia (el corazón)

Darse a sí mismo un check que devuelva **pass/fail**: test, build (exit code), linter, script que compara contra un fixture, o screenshot contra un diseño. Sin eso, "parece listo" es la única señal y el usuario se vuelve el loop.

- **Evidencia, no aserción.** Mostrar la salida del comando/test o el screenshot — nunca "los tests pasan" sin la salida. Prohibido decir "listo/todo verde" sin correrlo en esta sesión (igual que `quality-gate`).
- **Atacar la causa raíz, no el síntoma.** "El build falla" → arreglar la causa, no silenciar el error.
- **Verificación visual** para UI: screenshot del resultado vs. el objetivo, listar diferencias, arreglar.
- Si no hay forma de verificar algo, decirlo — no fingir que se comprobó.

## Gestión del contexto (recurso #1)

El rendimiento del modelo **cae cuando el contexto se llena**. Tratar el contexto como el recurso más escaso:

- **`/clear` entre tareas no relacionadas.** Un contexto lleno de basura previa degrada todo.
- **Subagentes para investigar** — leer muchos archivos en un contexto aparte que devuelve solo el resumen.
- **Compactación dirigida** cuando toca (`/compact <foco>`), preservando archivos tocados y comandos de test.
- Tras **corregir 2 veces el mismo error**, el contexto está contaminado con intentos fallidos → `/clear` y reprompt mejor. Un contexto limpio con buen prompt gana casi siempre a uno largo con parches.
- Objetivos largos que cruzan compactaciones → estado en disco, no en la cabeza (ver `maraton` (pack `agent-modes`)).

## CLAUDE.md — higiene

Es lo que Claude lee al arrancar cada sesión. Vale oro si está afinado, estorba si está inflado.
- **Corto** (regla práctica ≤200 líneas). Para cada línea preguntar: *"¿quitar esto haría que Claude se equivoque?"* Si no, cortar.
- Solo lo que **no se infiere** del código: comandos que no se adivinan, estilo que difiere del default, cómo correr los tests, convenciones de repo, gotchas, env vars.
- Fuera: docs de API (enlazar), lo que cambia seguido, obviedades ("escribe código limpio").
- `IMPORTANT` en **pocas** líneas — si todo es importante, nada lo es.
- Lo que aplica **a veces** va en una **skill** (carga bajo demanda), no en CLAUDE.md.
- Lo que debe pasar **siempre, sin excepción** va en un **hook** (determinista), no en una instrucción advisoria.

## Spec-driven para features grandes

Antes de una feature grande: **entrevistar al usuario** (preguntar por implementación, UX, bordes, tradeoffs que no consideró) → escribir **SPEC.md** autocontenido (nombra archivos e interfaces, dice qué queda fuera de alcance, termina con una verificación end-to-end) → **sesión nueva** para implementar con contexto limpio. *El código sirve a la spec, no al revés* (Spec Kit). Es la espina `intake → constitution → feature` del pack.

## Revisión adversarial en contexto fresco

Antes de contar algo como hecho: un revisor en **contexto fresco** (subagente) que solo ve el diff y los criterios juzga mejor que quien lo escribió (no arrastra el razonamiento que produjo el bug). Pedirle **solo huecos de corrección o de requisitos**, no preferencias de estilo (un revisor pedido "encuentra fallas" siempre encuentra → perseguir todo lleva a sobre-ingeniería). Usar `/code-review` o `diff-review`.

## Disciplina sobre el código generado (Uncle Bob tiene razón)

No confiar a ciegas en el código que produce un agente — ni el propio. La disciplina de clean code es **el diferenciador** de trabajar con agentes, no un lujo:
- El código nuevo llega con **tests que fallarían si estuviera mal** (si pasan con la implementación rota, no prueban nada).
- El gate lo forman **métricas medibles**: cobertura de código nuevo, **mutación**, complejidad, tamaño, dependencias, duplicación (ver `constitution` + `quality-gate`).
- Las métricas **no ven** un permiso invertido, dinero mal redondeado ni una migración destructiva → esos diffs se **leen a mano** (ver `diff-review`). Máquina siempre + humano en lo sensible.
- Seguridad del propio proceso agéntico y del código IA: ver `ai-security` (incluye slopsquatting: verificar que los paquetes existan).

## Flujo de referencia (Uncle Bob harness)

Un pipeline concreto y probado que encarna todo lo anterior, con humano en el bucle (no 100% automatizado):

1. **Spec** a mano (humano) → **hard spec**: un agente la formaliza y expande (más casos, más bordes).
2. **Gherkin**: un agente convierte la hard spec en contratos ejecutables (feature + escenarios
   `given/when/then`). **El humano revisa y aprueba spec y Gherkin** — son las puertas de aprobación.
3. **TDD**: implementar desde el Gherkin en rojo→verde→refactor (3 leyes del TDD).
4. **Juez**: un pase que verifica que cada escenario tenga ≥1 test y que se siguieron los ciclos.
5. **Mutation testing**: un agente voltea condiciones (`>=→>`, `==→!=`, `and→or`) e inyecta bugs;
   si los tests **sobreviven**, la suite está incompleta → volver a añadir tests. Automatiza lo que
   Uncle Bob usa como gate real de calidad del código del agente.

**Handoff vía ficheros**: cada etapa la hace un agente distinto que **escribe su resultado en un
`.md` y el siguiente lo lee** (memoria en `current.md` + logs de ciclo). Así cada agente trabaja con
poco contexto en vez de uno solo que se lo come entero — es la misma lógica de `/clear` + subagentes.
Aviso real: los flujos multi-agente **consumen muchos tokens**; y no son para dejar horas sin mirar
(revisar a medida que avanza). Mapea a la espina `intake → constitution → feature → quality-gate`.

## Herramientas

- **CLI antes que API** — `gh`, `aws`, `gcloud` son la forma más eficiente en contexto de tocar servicios externos.
- **Pocas herramientas de alto impacto** bien definidas > envolver todo (Building Effective Agents).
- **Patrones simples y componibles** > frameworks complejos. Empezar por lo más simple; añadir complejidad solo con beneficio medible.
- **Hooks** para lo que debe pasar siempre (lint tras editar, bloquear escrituras a `migrations/`).

## Anti-patrones (reconocerlos temprano)

- **Kitchen sink**: mezclar tareas no relacionadas en una sesión → `/clear`.
- **Corregir en bucle**: tras 2 correcciones fallidas, `/clear` + reprompt.
- **CLAUDE.md inflado**: Claude ignora la mitad → podar sin piedad.
- **Trust-then-verify gap**: implementación plausible que no maneja bordes → siempre dar verificación.
- **Exploración infinita**: "investiga X" sin acotar llena el contexto → acotar o usar subagente.
- Declarar éxito sin evidencia. Saltar el plan en cambios grandes. Confiar en un paquete sin verificar que existe.

## Formato de salida

1. Qué fase del loop se está ejecutando (explorar/planear/ejecutar/verificar/revisar).
2. En verificar: el **comando corrido y su salida** (evidencia), no una afirmación.
3. Al cerrar: qué se verificó, con qué evidencia, y qué quedó pendiente de lectura humana si tocó zona sensible.
