---
name: api-backend
description: Use when building or changing a server, API or backend service — REST/GraphQL endpoints, webhooks, background jobs and queues, authentication, integrations with third-party APIs, "hazme una API", "add an endpoint", "el webhook falla", rate limits, versioning, contracts. Covers contract design, idempotency, error handling, pagination, retries and the backend-specific gate. NO cubre la interfaz (web-app) ni el modelado de datos en profundidad (data-layer).
---

# API-Backend — contratos que otros van a depender de que no cambies

## Overview

Una API es una promesa pública. Desde que alguien la consume, cada cambio de forma silencioso rompe sistemas ajenos que no puedes arreglar. Por eso el backend se diseña al revés que un script: primero el contrato, después la implementación.

Y como todo lo que cruza una red falla a veces, el backend profesional asume tres cosas desde el día uno: **los mensajes llegan repetidos, llegan fuera de orden, y a veces no llegan.**

## Cuándo usar

- Endpoints nuevos, cambios de contrato, versionado.
- Webhooks entrantes o salientes.
- Trabajos en segundo plano, colas, tareas programadas.
- Integración con APIs de terceros.
- Autenticación de servicios y límites de uso.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Interfaz de usuario | `web-app` |
| Esquema, migraciones, integridad | `data-layer` |
| Lentitud medida | `performance` |
| Lógica de conversación de un bot | `bot-dev` |

## Regla de hierro: idempotencia en todo lo que puede repetirse

```
TODA OPERACION QUE CAMBIA ESTADO Y PUEDE REINTENTARSE NECESITA CLAVE DE IDEMPOTENCIA RESPALDADA POR UNA RESTRICCION UNICA.
```

Los reintentos garantizan entrega **al menos una vez**: los duplicados no son una posibilidad remota, son el comportamiento normal. Sin idempotencia, eso significa cobrar dos veces, enviar dos mensajes o crear dos pedidos.

## Diseño del contrato

- Recursos con nombres claros y estables; verbos HTTP con su significado real; códigos de estado honestos (no `200` con `{"error": ...}` adentro).
- **Forma de error única en toda la API**: código legible por máquina, mensaje para humanos, identificador de correlación. Nada de tres formatos según el endpoint.
- Paginación desde el primer día, con límite máximo. Filtros y orden explícitos.
- Validación por esquema en la entrada; rechazar campos desconocidos si el contrato es estricto.
- Versionado: los cambios aditivos no rompen; los que rompen exigen versión nueva y período de convivencia anunciado.
- Contrato documentado y **generado desde el código** cuando se pueda, para que no mienta.
- Tiempo siempre en UTC con formato estándar; dinero en unidades mínimas.

## Resiliencia

| Patrón | Cuándo | Detalle |
|---|---|---|
| Tiempo límite | Toda llamada externa | Sin tiempo límite, un tercero lento congela tu servicio entero |
| Reintento con retardo creciente y **aleatorio** | Fallos transitorios (red, 429, 5xx) | El componente aleatorio evita que mil clientes reintenten al mismo instante |
| Tope de reintentos + cola de fallidos | Siempre que haya reintentos | Lo que agota reintentos va a una cola revisable, no al vacío |
| Interruptor | Dependencia que cae seguido | Dejar de llamar un rato es mejor que acumular peticiones colgadas |
| Degradación elegante | Funcionalidad secundaria caída | Responder con lo esencial antes que fallar entero |
| Límite de uso | API pública o cara | Por clave y por IP, con cabeceras que digan cuánto queda |

Nunca reintentar a ciegas una operación no idempotente: un tiempo límite no significa que no se ejecutó del otro lado.

## Webhooks

**Entrantes:** verificar la firma antes que nada; rechazar lo que llegue sin firma válida. Después: guardar el evento, responder rápido (2xx) y procesar aparte. Un manejador que hace todo el trabajo antes de responder provoca reintentos del proveedor y trabajo duplicado. Deduplicar por identificador de evento con ventana mayor al horizonte de reintentos del proveedor.

**Salientes:** firmar la carga, reintentar con retardo creciente y aleatorio, exponer los intentos, y permitir reenvío manual. Documentar que el receptor debe ser idempotente.

## Trabajos en segundo plano

- Todo lo lento sale del camino de la petición: correos, PDFs, llamadas a terceros, procesamiento pesado.
- Cada trabajo: idempotente, reanudable, con tiempo límite y con registro de resultado.
- Tareas programadas con candado para no solaparse, y latido para detectar que dejaron de correr (`observability`).
- Cola con reintentos y cola de fallidos revisada por alguien; una cola de fallidos que nadie mira es un basurero.

## Seguridad específica

- Autorización **por recurso** en cada endpoint, no solo autenticación.
- Identificadores no adivinables si listarlos filtra información.
- Límite de uso y de tamaño de cuerpo; protección contra cargas maliciosas.
- Nada de secretos en URL (quedan en logs y en el historial del proxy).
- Registrar accesos a datos sensibles; nunca registrar el contenido sensible en sí.

## Gate específico de backend

| Chequeo | Qué verifica |
|---|---|
| Tests de contrato | La forma de respuesta no cambió sin querer |
| Tests de integración con base real | Las consultas y transacciones funcionan de verdad |
| Prueba de idempotencia | Ejecutar dos veces el mismo evento deja un solo efecto |
| Simulación de fallo del tercero | Tiempo límite y reintentos se comportan como se espera |
| Migraciones aplicadas en entorno limpio | El arranque desde cero funciona |
| Verificación de firma de webhook | Firma inválida se rechaza |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "El webhook llega una sola vez" | Llega repetido. Siempre. Es parte del diseño de quien lo envía. |
| "Le pongo reintentos y listo" | Reintentos sin idempotencia multiplican el efecto en vez del éxito. |
| "Sin límite de tiempo por si el tercero tarda" | Ese es el camino más corto a agotar las conexiones y caerte entero. |
| "Cambio el campo, total el front lo actualizo" | Si alguien más consume la API, acabas de romperle el sistema sin avisar. |
| "Devuelvo 200 siempre para que no falle el cliente" | Ocultas errores y obligas a todos a adivinar. Los códigos existen por algo. |
| "Proceso el webhook y después respondo" | El proveedor te marca como caído y te reenvía todo. Responde primero, procesa después. |

## Formato de salida

- Contrato de los endpoints tocados (entrada, salida, errores, códigos).
- Garantías: idempotencia, reintentos, tiempos límite, límites de uso.
- Efectos secundarios y quién los consume.
- Resultado real de los tests de contrato e integración.
- Cambios que rompen compatibilidad y plan de convivencia, si los hay.
