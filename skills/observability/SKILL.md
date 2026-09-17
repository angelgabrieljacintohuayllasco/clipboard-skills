---
name: observability
description: Use when you cannot tell what a running system is doing — "no sé qué pasa en producción", "se cayó y no sé por qué", "add logging", "necesito monitoreo", "cómo me entero si falla", intermittent failures, silent bot/cron/job failures, or before launching anything real. Designs logs, metrics, health checks, alerts and error tracking so failures are noticed by the system, not by the client. NO diagnostica un bug puntual (fixer) ni optimiza velocidad (performance).
---

# Observability — que el sistema avise antes que el cliente

## Overview

El peor estado de un sistema no es caído: es **caído sin que nadie lo sepa**. Un bot que dejó de responder, un cron que falla en silencio desde hace nueve días, una integración que devuelve vacío — todos "funcionan" hasta que alguien reclama.

Observabilidad no es instalar una herramienta cara: es responder tres preguntas en cualquier momento, con datos y no con suposiciones. **¿Está vivo? ¿Está haciendo su trabajo? ¿Cuándo empezó a fallar y qué cambió?**

## Cuándo usar

- Antes de poner algo en manos de usuarios reales.
- Proceso que corre solo: bot, cron, cola, scraper, integración.
- Fallos intermitentes que no se reproducen en local.
- "Se cayó y nos enteramos por el cliente."
- Después de un incidente: qué señal habría avisado antes.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Bug reproducible con stack trace | `fixer` |
| Lento pero funcionando | `performance` |
| Bot que responde mal (lógica, no caída) | `agent-debug` |

## Regla de hierro: cada camino crítico deja rastro

```
SI UN FLUJO PUEDE FALLAR Y NADIE SE ENTERARIA, NO ESTA TERMINADO.
```

Por cada flujo del spec: se registra que empezó, que terminó y con qué resultado. Un proceso que solo escribe cuando todo va bien es un proceso que no avisa cuando va mal.

## Las cuatro señales mínimas

### 1. Logs útiles
- **Estructurados** (clave/valor o JSON): permiten filtrar. Texto libre solo sirve para leer con los ojos, y nadie lee 200 MB.
- Con **identificador de correlación** por petición/mensaje/tarea, propagado a todo lo que dispare. Sin eso, en un sistema concurrente los mensajes son confeti.
- Niveles con criterio: `error` = alguien debe mirar; `warn` = raro pero manejado; `info` = hitos de negocio; `debug` = apagado en producción.
- Cada error incluye: qué se intentaba, con qué entrada (sin datos sensibles), qué excepción y qué se hizo después.
- Nunca: contraseñas, tokens, datos personales completos, contenido íntegro de mensajes privados.
- Rotación y retención definidas: los logs llenan discos, y un disco lleno es una caída nueva.

### 2. Métricas (pocas y que importen)
Cuatro señales estándar bastan para casi todo:

| Señal | Qué responde |
|---|---|
| Tráfico | ¿cuánto trabajo está llegando? |
| Errores | ¿qué proporción falla? |
| Latencia | ¿cuánto tarda? (percentil 95, no promedio: el promedio esconde el dolor) |
| Saturación | ¿cuánto queda de CPU, memoria, disco, conexiones, cola? |

Más una métrica de negocio por proyecto: pedidos creados, mensajes respondidos, archivos procesados. Esa es la que de verdad delata un fallo silencioso: **el sistema vivo que dejó de producir**.

### 3. Chequeo de salud y latido
- Endpoint o marca de salud que verifique dependencias reales (base de datos, cola, proveedor), no solo "el proceso está arriba".
- Para tareas programadas: **latido muerto** — el trabajo reporta "terminé" a cada corrida, y si no lo hace en el plazo esperado, se alerta. Es la única forma de detectar un cron que nunca arrancó.

### 4. Alertas que se pueden atender
- Alerta solo sobre síntomas que afectan al usuario o que exigen acción humana.
- Cada alerta responde: qué pasa, desde cuándo, qué se hace, dónde está el runbook.
- Umbral con duración ("errores >5% por 5 minutos"), no picos instantáneos.
- **La fatiga de alertas mata la observabilidad**: una alerta que se ignora tres veces se ignorará siempre. O se ajusta, o se borra.

## Errores en producción
Captura centralizada de excepciones con agrupación, versión, entorno y contexto de usuario anónimo. Un error nuevo tras un despliegue debe ser visible en minutos, no por reclamo.

## Escalones según tamaño (no te pases de ingeniería)

| Escala | Suficiente |
|---|---|
| Proyecto personal / P1 | Logs a archivo con rotación + una alerta por correo/mensaje si el proceso muere |
| Producto con usuarios / P2 | Logs estructurados + captura de errores + 4 señales + latido de tareas + 3-5 alertas |
| Crítico / P3 | Lo anterior + trazas distribuidas, tableros, objetivos de nivel de servicio y presupuesto de error, guardia definida |

## Después de cada incidente

1. Línea de tiempo con datos reales (no memoria).
2. Causa raíz, no "se cayó el servidor".
3. **¿Qué señal habría avisado antes?** → crear esa señal ahora.
4. Registrar en `bugs.md` y en el `runbook.md`.
5. Sin culpas: se corrigen sistemas, no personas. El objetivo es que el próximo se detecte solo.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Ya pongo console.log si falla algo" | Sin estructura ni correlación, no se puede buscar. Y en producción esos mensajes se pierden. |
| "Me entero si el cliente reclama" | Ese es el peor detector: llega tarde, enojado y con los datos ya perdidos. |
| "El monitoreo es caro" | Un latido y un correo de alerta son gratis. Lo caro es descubrir el viernes que falla desde el lunes. |
| "Logueo todo por si acaso" | Ruido, costo y riesgo de filtrar datos. Registra decisiones y resultados, no cada paso. |
| "Lo agrego después del lanzamiento" | El lanzamiento es exactamente cuando se necesita. Se instala antes. |
| "Con el uptime del proveedor alcanza" | Dice que el proceso responde, no que esté haciendo su trabajo. |

## Formato de salida

- Las tres preguntas respondidas: cómo se sabe que está vivo, que trabaja y desde cuándo falla.
- Qué se registra en cada camino crítico y con qué identificador de correlación.
- Métricas elegidas (4 señales + 1 de negocio) y dónde se ven.
- Alertas con umbral, duración y acción; enlace al runbook.
- Qué quedó sin cubrir y por qué.
