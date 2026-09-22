---
name: rebuild
description: "Rebuild a project from a solid base instead of patching: repeated failed fixes, unmaintainable monolith. \"hay que rehacerlo\", \"empezar de cero\", \"rewrite this\". Rescue rules first, run in parallel to parity."
---

# Rebuild — rehacer desde base sólida, sin perder lo aprendido

## Overview

Reconstruir NO es "borrar y escribir lo mismo pero bonito". Es: **rescatar el conocimiento caro** (reglas de negocio, bugs resueltos, datos reales), **diseñar una base que corrija el defecto estructural** del sistema viejo, y **migrar con el viejo vivo** hasta alcanzar paridad verificada.

La mayoría de los rewrites fracasa o cuesta varias veces lo previsto, y casi siempre por la misma razón: tiran las reglas de negocio junto con el código sucio y re-descubren cada caso borde en producción, con usuarios adentro. Este proceso existe para no repetir esa historia.

## Cuándo usar

- `triage` ya dio veredicto de rebuild, o hay evidencia dura: sin tests posibles + sin estructura + efectos cruzados + la arquitectura no soporta lo que se pide + historial documentado de fixes que se pisan.
- El costo acumulado de parchar ya superó el costo estimado de rehacer (mirar el historial: ¿cuántas sesiones se fueron en re-arreglar lo mismo?).

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Nadie hizo triage | `triage` primero. "Está feo" no es evidencia |
| Feo pero estable | `refactor` |
| Solo un módulo está podrido | `refactor` con estrangulamiento de ese módulo |
| La motivación real es probar otro stack | `valida-idea`, con esa honestidad sobre la mesa |
| No se puede mantener el sistema viejo corriendo | Replantear: sin oráculo de comportamiento, el riesgo se dispara |

## Fase 1 — Inventario de rescate (ANTES de escribir código nuevo)

```
LO QUE NO SE INVENTARIA, SE PIERDE Y SE RE-DESCUBRE EN PRODUCCION.
```

Rescatar del sistema viejo, en orden de valor:

1. **Reglas de negocio con evidencia**: las que viven en el código y en la cabeza de alguien. Si no están escritas, entrevistar al código viejo y documentarlas ANTES de rehacer. Una regla perdida es un cliente enojado dentro de tres meses.
2. **Historial de bugs = suite de regresión gratis**: cada bug resuelto (síntoma → causa raíz → prevención) se convierte en un caso de prueba del sistema nuevo. Son la especificación más cara que ya pagaste.
3. **Trampas y zonas rojas**: cada una es un caso del mundo real (formatos raros, nombres que cambian, cuotas de API, datos sucios). El sistema nuevo debe manejarlas desde el día uno.
4. **Datos y configuración reales**: migración o retención con plan explícito. Los datos no se rehacen.
5. **Lo que SÍ funcionaba**: módulos estables con sus pruebas pueden portarse tal cual. No todo es basura.

## Fase 2 — Base nueva

- **Corregir el defecto estructural, no la estética.** Si el viejo era imposible de probar, la base nueva se define por sus costuras de prueba. Ejemplo: un bot que solo podía verificarse contra el canal real → la base nueva necesita una capa de transporte sustituible como **primer** requisito, no como "algún día".
- **Constitución y gate desde el primer commit** (`constitution`): el sistema nuevo nace con umbrales; si no, en seis meses es el sistema viejo con otro nombre.
- Mismo stack salvo razón documentada: cambiar de stack duplica el riesgo del rewrite.
- Módulos chicos; pruebas que corren sin efectos del mundo real (sin API paga, sin mensajes reales, sin datos de producción).
- Los controles críticos de negocio (anti-duplicado, límites, validaciones) viven en código estructural, no en prompts ni en disciplina humana.

## Fase 3 — Paridad y cambio

- **Lista de paridad** generada del inventario: funcionalidades + bugs que no deben volver + trampas cubiertas. Se marca con verificación ejecutada, no con optimismo.
- **El sistema viejo sigue corriendo** hasta paridad verificada. Convivencia (viejo en producción, nuevo en paralelo comparando resultados) es mucho mejor que un salto de golpe.
- Cambio con vuelta atrás definida y ensayada. Después: el código viejo se archiva (no se borra) y las notas del proyecto se actualizan.
- **Funcionalidades nuevas: después del cambio.** Mezclarlas hace imposible saber si el nuevo ya alcanzó al viejo.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Empiezo limpio y migro reglas según me acuerde" | No te vas a acordar. Los casos borde viven en los bugs viejos, no en la memoria. Inventario primero. |
| "Esta vez lo hago rápido porque ya sé cómo va" | Ese exceso de confianza es exactamente por qué los rewrites se desbordan. La lista de paridad manda. |
| "Apago el viejo ya, así me obligo" | Pierdes el oráculo de comportamiento correcto y dejas al negocio sin herramienta mientras tanto. |
| "De paso agrego estas funcionalidades nuevas" | Paridad primero. Si no, el proyecto nunca "termina" y nadie puede decidir el cambio. |
| "El código viejo no sirve para nada" | Sirve como especificación ejecutable. Es lo único que sabe con certeza qué hace el sistema hoy. |

## Formato de salida

Por fase: inventario de rescate (con origen de cada elemento), decisión de base (qué defecto estructural corrige y cómo se verifica), lista de paridad con estado verificado, plan y estado del cambio, y la constitución del sistema nuevo.

Honestidad obligatoria: si durante la fase 1 descubres que con el inventario a la vista un `refactor` alcanzaba, dilo y frena el rebuild. Reconocerlo a tiempo vale más que terminar el proyecto que prometiste.
