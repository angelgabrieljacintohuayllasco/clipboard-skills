---
name: tech-debt
description: Use to inventory, quantify and prioritize technical debt, or to decide whether debt is worth taking — "el proyecto está lleno de parches", "cuánta deuda tenemos", "qué arreglo primero", "assess technical debt", "is this codebase salvageable", legacy audits, code generated fast by AI that now needs cleanup, or before promising a delivery date on a messy repo. Produces a measured debt register with interest cost and a payment plan. NO reestructura código (refactor), no reescribe el proyecto (rebuild), no fija umbrales (constitution).
---

# Tech-Debt — medir lo que el desorden cuesta por mes

## Overview

Deuda técnica no es "código feo": es una **decisión de diseño que acelera hoy y cobra intereses en cada cambio futuro**. La metáfora sirve solo si se usa entera: deuda deliberada y registrada es una herramienta financiera legítima; deuda accidental e invisible es una hemorragia.

El desarrollo asistido por IA cambió la escala del problema. Se produce código más rápido de lo que nadie puede revisar, y si el pipeline no filtra, lo que se acelera es la deuda. Por eso el orden correcto es: medir → registrar → cobrar interés visible → pagar con criterio.

## Cuándo usar

- Heredaste un proyecto y hay que decidir qué hacer con él.
- Cada cambio tarda más que el anterior; el mismo bug vuelve con otra cara.
- Antes de comprometer un plazo sobre un repo desordenado.
- Después de una racha de generación rápida (prototipo que se volvió producto).
- Para decidir conscientemente tomar deuda a cambio de una fecha.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Ya sabes qué reestructurar | `refactor` |
| El proyecto no se puede salvar | `rebuild` (tras evidencia de esta skill) |
| Bug activo | `triage` → `fixer` |
| Definir umbrales nuevos | `constitution` |

## Regla de hierro: deuda sin número es queja

```
CADA ITEM DE DEUDA LLEVA: EVIDENCIA MEDIDA, INTERES (QUE ENCARECE HOY) Y COSTO DE PAGO.
```

"El código está horrible" no es accionable. "El archivo de pedidos tiene 2.100 líneas, complejidad máxima 38, 0% de cobertura, y concentra 14 de los últimos 20 commits de corrección" sí lo es: se puede priorizar, estimar y defender ante quien paga.

## Proceso

### 1. Medir (una pasada, sin tocar nada)

| Señal | Cómo se obtiene | Qué revela |
|---|---|---|
| Archivos más grandes | conteo de líneas ordenado | candidatos a monolito |
| Complejidad máxima y media | linter / analizador | dónde nadie entiende el flujo |
| Cobertura y mutación por módulo | herramientas de test | dónde no hay red |
| **Churn × complejidad** | `git log` por archivo + complejidad | **los puntos calientes: mucho cambio + mucha complejidad = donde duele** |
| Commits "fix" sobre el mismo archivo | `git log --oneline` filtrado | síntomas recurrentes = causa no atacada |
| Duplicación | detector de copias | conocimiento repetido |
| Ciclos de dependencias | detector de ciclos | módulos mal cortados |
| Dependencias sin actualizar / vulnerables | auditoría del gestor | riesgo de seguridad y de bloqueo |
| TODO/FIXME sin fecha | grep | deuda declarada y olvidada |
| Tiempo del gate | cronómetro | fricción que empuja a saltárselo |

El cruce **churn × complejidad** es el que mejor ordena la lista: un archivo complejo que nadie toca puede esperar; uno complejo que se toca cada semana está cobrando interés hoy.

### 2. Clasificar cada item

| Tipo | Ejemplo | Trato |
|---|---|---|
| **Deliberada y registrada** | "Sin caché ahora, lo sabemos, ADR-003" | Aceptable. Revisar en la fecha acordada. |
| **Deliberada y olvidada** | Atajo de hace un año que nadie anotó | Registrar ahora y ponerle fecha |
| **Accidental de diseño** | Se entendió mal el dominio, el modelo no da | Cara: requiere rediseño, no limpieza |
| **De entorno** | Versiones viejas, sin CI, despliegue manual | Suele ser la más barata de pagar y la que más rinde |
| **De conocimiento** | Nadie sabe cómo funciona; sin notas | Pagar con `project-memory`, casi gratis |
| **De pruebas** | Sin red de seguridad | Bloquea todo lo demás: se paga primero |

### 3. Registrar

`docs/project/tech-debt.md`:

```markdown
| # | Deuda | Evidencia | Interés (qué encarece) | Costo de pago | Riesgo si no se paga | Prioridad |
|---|-------|-----------|------------------------|---------------|----------------------|-----------|
| 1 | orders.ts 2.100 LOC, cx 38 | 14/20 fixes recientes | cada cambio ~2 días y rompe otra cosa | 3 días (extraer 4 módulos) | bugs de cobro | ALTA |
```

Prioridad = (interés que cobra hoy) × (riesgo) ÷ (costo de pago). Lo que no se toca, no cobra interés: puede quedar abajo aunque sea horrible.

### 4. Pagar con criterio

- **Primero la red**: sin tests de caracterización, cualquier pago rompe cosas. `test-strategy` antes que `refactor`.
- **Regla del boy scout con límite**: cada feature deja su zona un poco mejor, sin desviarse del alcance.
- **Trinquete**: el gate no permite empeorar. Cobertura y complejidad solo mejoran. Esto detiene la hemorragia aunque no pagues nada más.
- **Pago programado**: un porcentaje fijo de cada ciclo (ej. 20%) dedicado a los puntos calientes. Sin cuota fija, la deuda siempre pierde contra la urgencia.
- **Nunca mezclar** pago de deuda con feature en el mismo diff: si algo se rompe, nadie sabe qué lo rompió.

### 5. Decir la verdad sobre el veredicto

Si la medición muestra: sin pruebas posibles + modelo de dominio equivocado + puntos calientes por todos lados + historial largo de correcciones que se pisan → la respuesta honesta es `rebuild` con inventario de rescate, no diez sesiones de limpieza. Y si la deuda es tolerable, también hay que decirlo: refactorizar por estética es deuda nueva disfrazada de virtud.

## Tomar deuda a propósito (cómo se hace bien)

Está permitido, con tres condiciones: **está escrito**, **tiene fecha de vencimiento** y **quien paga lo sabe**.

> "Para llegar al viernes: sin capa de caché y validación solo en el cliente. Costo: si entran más de 300 usuarios se degrada, y la validación hay que duplicarla en el servidor antes de abrir al público. Fecha de pago: 30/09. ADR-005."

Eso es ingeniería. Lo otro — atajo silencioso, sin fecha, sin aviso — es trasladarle el costo a alguien que no lo aceptó.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Refactorizamos todo y listo" | Sin priorizar por interés, se limpia lo cómodo y queda intacto lo que duele. |
| "No hay tiempo para deuda" | El tiempo ya se está gastando: en cada cambio que tarda el triple. La deuda no espera permiso para cobrar. |
| "Lo reescribo, sale más rápido" | Los rewrites suelen costar varias veces lo previsto y pierden reglas de negocio invisibles. Solo con evidencia dura. |
| "La IA lo limpia en un rato" | La IA limpia lo que se puede verificar. Sin tests, "limpiar" es cambiar bugs conocidos por bugs nuevos. |
| "Esto es deuda, pero funciona" | Funcionar es el mínimo. La pregunta es cuánto cuesta el próximo cambio. |
| "Anoto el TODO y sigo" | TODO sin dueño ni fecha es ruido. Con fecha, es un compromiso. |

## Formato de salida

- Tabla de medición (números reales, comandos usados).
- Registro de deuda priorizado por interés × riesgo ÷ costo.
- Top 3 con plan concreto de pago y su orden.
- Veredicto honesto: pagar por partes, solo trinquete, o reconstruir.
- Deuda deliberada nueva, si se toma: escrita, con fecha y con aviso a quien paga.
