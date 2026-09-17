---
name: architecture
description: Use when choosing a stack, structuring a new project, or making a decision that will be expensive to reverse — "qué stack uso", "cómo estructuro esto", "monolito o microservicios", "qué base de datos", "necesito una cola?", "which framework", adding a service/dependency/layer, or documenting an ADR. Picks boring, verifiable options sized to the real load, defines module boundaries and dependency direction, and records the decision. NO implementa la feature (feature) ni reestructura código existente (refactor).
---

# Architecture — decidir lo caro de revertir, y dejarlo escrito

## Overview

La arquitectura es el conjunto de decisiones que **cuestan caro cambiar después**: el modelo de datos, los límites entre módulos, quién depende de quién, dónde vive el estado. Todo lo demás es implementación y se puede rehacer un martes cualquiera.

Dos criterios gobiernan: **elegir aburrido** (tecnología conocida, con documentación abundante y comunidad, que la IA y cualquier reemplazo tuyo ya conocen) y **dimensionar a la carga real**, no a la fantasía de escala.

## Cuándo usar

- Proyecto nuevo, después del `intake`.
- Decisión estructural: nueva dependencia grande, servicio aparte, cola, caché, cambio de base de datos, multi-tenant, autenticación.
- El diseño actual impide una funcionalidad pedida.
- Alguien propone microservicios, event sourcing, CQRS o Kubernetes para 200 usuarios.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Implementar dentro de la estructura existente | `feature` |
| Reorganizar código sin cambiar comportamiento | `refactor` |
| Todavía no está claro qué se construye | `intake` |
| Elegir entre dos librerías chicas e intercambiables | decisión de `feature`, no ADR |

## Regla de hierro: la decisión se escribe o no existe

```
TODA DECISION ESTRUCTURAL PRODUCE UN ADR: CONTEXTO, OPCIONES, ELECCION, CONSECUENCIAS, FECHA.
```

Sin ADR, en tres meses nadie recuerda por qué, y se revierte por gusto o se mantiene por miedo. Ambas salidas son caras.

## Proceso

### 1. Cuantificar antes de diseñar

Números, no adjetivos. Si no se saben, se estiman en voz alta y se anotan como supuesto:

- Usuarios concurrentes reales hoy y en 12 meses (no en el pitch).
- Escrituras y lecturas por segundo; tamaño del dato; crecimiento mensual.
- Tolerancia a caída: ¿minutos, horas, un día? ¿Qué pierde el negocio por hora caída?
- ¿Quién mantiene esto dentro de un año y con qué nivel?

Casi todo lo que la gente pide cabe en **un proceso, una base de datos relacional y un servidor**. La complejidad distribuida se justifica con números, nunca con "por si crece".

### 2. Elegir aburrido, con motivo

| Prefiere | Sobre | Salvo que |
|---|---|---|
| Monolito modular | Microservicios | Equipos independientes o escalado muy asimétrico probado |
| Base relacional (Postgres/SQLite) | NoSQL | Tu dato es realmente sin esquema o es carga masiva de series de tiempo |
| Tabla + índice | Caché nueva | Mediste la consulta y ya está optimizada |
| Cron + cola simple | Orquestador de eventos | Hay reintentos complejos y volumen real |
| Renderizado del servidor | SPA con estado global | La interfaz es de verdad una aplicación, no un sitio |
| Trabajo en proceso | Servicio aparte | Necesita escalar o desplegar por separado |
| Librería conocida | Marco nuevo y brillante | Resuelve un problema tuyo, medido |

Tres preguntas a cualquier tecnología nueva: ¿resuelve un problema que **tengo hoy**? ¿Cuánto cuesta sacarla si falla? ¿Quién la mantiene si desaparece del mapa?

### 3. Definir límites y dirección de dependencias

- Divide por **capacidades de negocio**, no por capas técnicas.
- Regla de dependencias: el dominio (reglas del negocio) no importa nada de infraestructura. La base de datos, el framework web, el proveedor de mensajes y la interfaz dependen del dominio, jamás al revés.
- Cada módulo publica una interfaz chica; lo demás es privado.
- **Cero ciclos.** Un ciclo de dependencias es dos módulos que en realidad son uno mal cortado.
- Estado compartido entre módulos = acoplamiento oculto. Que el dato tenga un dueño claro.
- Diseña para poder probar: si la estructura obliga a levantar todo para verificar una regla, la estructura está mal.

### 4. Escribir el ADR

`docs/project/decisions/ADR-0001-<tema>.md`:

```markdown
# ADR-0001 — <decisión en una frase>
fecha: YYYY-MM-DD · estado: aceptada | reemplazada por ADR-00XX

## Contexto
<qué problema, qué restricciones reales, qué números>

## Opciones consideradas
1. <opción> — pros / contras / costo de salida
2. ...

## Decisión
<la elegida y por qué gana dados los números de arriba>

## Consecuencias
Positivas: ...
Negativas (aceptadas conscientemente): ...
Qué haría falta para revertirla: ...

## Señales de revisión
<qué número, si llega, obliga a reabrir esta decisión>
```

Ese último bloque es lo que separa una decisión profesional de una corazonada: define de antemano **cuándo se revisa**.

### 5. Reflejar en el repo

- Estructura de carpetas que muestre los límites (que la forma del proyecto comunique la arquitectura).
- Reglas de dependencia verificadas por herramienta, no por buena voluntad (detector de ciclos, linter de importaciones, capas declaradas).
- `docs/project/architecture.md` con el mapa: módulos, flujo de datos, integraciones externas, dónde vive cada estado.
- Si la decisión cambia los umbrales o las zonas sensibles: actualizar `constitution`.

## Errores clásicos

| Error | Costo real |
|---|---|
| Microservicios sin necesidad | Multiplicas fallos de red, despliegue y depuración por cada servicio |
| Abstraer la base de datos "por si cambiamos" | Pierdes lo bueno del motor y nunca cambias |
| Capas vacías que solo reenvían llamadas | Cada cambio toca cinco archivos sin ganar nada |
| Elegir por popularidad reciente | Documentación escasa, respuestas inventadas, migración forzada en 2 años |
| Acoplarse a un proveedor sin plan de salida | El día que sube el precio o cierra, el negocio queda de rehén |
| Diseñar para 1M de usuarios con 100 | Pagas complejidad hoy por ingresos hipotéticos |
| Dejar la decisión implícita | Nadie la puede discutir, revisar ni revertir con criterio |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Mejor lo hacemos escalable desde el inicio" | Escalable no es una propiedad que se compra al principio: es límites limpios y medición. Lo demás es complejidad prematura. |
| "Este framework es el estándar ahora" | El estándar de hace dos años hoy es deuda. Elige por ajuste al problema y costo de salida. |
| "Total, si no sirve lo cambiamos" | Eso es verdad para la implementación, no para el modelo de datos ni para los límites de módulos. |
| "No hace falta ADR, es obvio" | Obvio hoy, para ti. El ADR se escribe para el que llegue sin tu contexto — incluido tú en seis meses. |
| "Lo separo en servicios para que sea ordenado" | El orden se consigue con límites de módulo, gratis y sin red de por medio. |

## Formato de salida

- Números que sostienen la decisión (aunque sean estimados declarados).
- Opciones con costo de salida de cada una.
- Decisión + ADR escrito.
- Mapa de módulos, dirección de dependencias y dónde vive el estado.
- Qué se verifica automáticamente (ciclos, capas) y con qué comando.
- Señal concreta que obligaría a revisitar la decisión.
