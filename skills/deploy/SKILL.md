---
name: deploy
description: "Ship to production and be able to roll back: VPS, containers, hosting, stores, CI/CD, env vars, releases. \"sube esto a producción\", \"deploy this\", \"se rompió después de subir\"."
---

# Deploy — publicar de forma que se pueda deshacer

## Overview

Desplegar no es copiar archivos a un servidor: es **cambiar el sistema que la gente está usando ahora mismo**. La pregunta que define si el despliegue es profesional o una apuesta no es "¿funciona?", sino **"¿cuánto tardo en volver atrás si no funciona?"**.

Si esa respuesta supera unos minutos, o no se conoce, el despliegue es un salto al vacío, sin importar cuán verde esté el gate.

## Cuándo usar

- Primera publicación o cada nueva versión.
- Configurar entornos, secretos, CI/CD.
- Después de un despliegue que rompió algo.
- Escribir o actualizar el runbook.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| No arranca en desarrollo | `env-doctor` |
| Falta verificar calidad | `quality-gate` primero |
| No hay forma de saber si quedó bien | `observability` |

## Regla de hierro: rollback ensayado antes del primer despliegue

```
SI NUNCA PROBASTE VOLVER ATRAS, NO TIENES ROLLBACK: TIENES UNA ESPERANZA.
```

Ensáyalo una vez, con cronómetro, antes de que haya usuarios. Anota el tiempo real en el runbook. Ese número es el que autoriza (o no) a desplegar un viernes.

## Antes de publicar

| Chequeo | Criterio |
|---|---|
| Gate completo verde | Salida real pegada, no recordada |
| Migraciones | Probadas sobre copia real, con paso atrás |
| Secretos | En el entorno del servidor, nunca en el repo ni en la imagen |
| Configuración por entorno | Desarrollo / pruebas / producción separados, credenciales distintas |
| Versión | Etiquetada y trazable al commit exacto |
| Respaldo | Reciente y verificado (sobre todo si hay migración) |
| Runbook | Existe y está actualizado |
| Plan de vuelta atrás | Escrito, con tiempo medido |

## Entornos y secretos

- Mínimo dos entornos: uno donde equivocarse sale gratis y producción. Un entorno de pruebas que no se parece a producción da falsa confianza.
- Secretos por entorno, permiso mínimo, rotables sin redesplegar código.
- **Nada de datos reales de usuarios en entornos de prueba** sin anonimizar.
- La configuración se valida al arrancar: si falta una variable, el proceso falla ruidosamente al inicio, no a las tres horas en una ruta poco usada.

## Estrategias de publicación

| Estrategia | Cuándo | Costo |
|---|---|---|
| Reemplazo directo con parada breve | Proyecto chico, usuarios tolerantes | Simple. Hay corte. |
| Dos entornos alternados (azul/verde) | Se quiere volver atrás en segundos | Doble infraestructura |
| Despliegue gradual por porcentaje | Base grande de usuarios | Requiere métricas por versión |
| Interruptor de funcionalidad | Separar "desplegar" de "activar" | La mejor relación costo/beneficio: el código entra apagado y se enciende cuando toca, y se apaga sin redesplegar |

Regla transversal: **desplegar ≠ liberar**. Con interruptores, un problema se apaga en segundos sin tocar servidores.

## Automatizar el camino

Un despliegue manual es un despliegue que algún día se hace mal, de noche, con sueño.

1. Un comando o una acción: `deploy` o el pipeline en CI.
2. El pipeline corre el gate; si falla, no publica. Sin excepciones manuales.
3. Construcción reproducible: mismas versiones fijadas, artefacto identificable.
4. Migraciones como paso explícito, con respaldo previo.
5. Verificación automática tras publicar (humo): si falla, vuelve atrás solo o avisa de inmediato.
6. Registro: quién, qué versión, cuándo, con qué cambios.

## Después de publicar (los primeros 15 minutos)

1. Camino crítico probado a mano, en producción, con datos reales.
2. Tasa de errores y latencia comparadas contra antes del despliegue.
3. Logs mirados en vivo un par de minutos.
4. Si algo se degrada: **volver atrás primero, investigar después**. Investigar con usuarios sufriendo es la decisión equivocada casi siempre.
5. Anotar la versión desplegada en `state.md` y cualquier sorpresa en `gotchas.md`.

## Releases en tiendas y clientes instalables

- Escritorio y móvil no tienen rollback instantáneo: la versión mala queda en manos de la gente. Por eso: publicación escalonada por porcentaje, interruptor remoto para apagar funcionalidades, y compatibilidad hacia atrás obligatoria del servidor con las versiones ya instaladas.
- Firmar los artefactos y **resguardar las claves de firma con respaldo**: perder la clave de publicación puede significar perder la aplicación.
- Las tiendas cambian requisitos (versiones mínimas, permisos, privacidad) con fecha límite: revisar antes de cada envío, no el día que rechazan la actualización.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es un cambio chico, subo directo" | La mayoría de las caídas vienen de cambios chicos que se saltaron el camino normal. |
| "Lo subo y veo si anda" | Los usuarios son tus pruebas, entonces. Humo automático + verificación manual del camino crítico. |
| "El rollback es hacer otro commit" | Eso tarda un ciclo completo de construcción. El rollback es volver al artefacto anterior, en minutos. |
| "Toco el servidor a mano, es más rápido" | Y queda indocumentado. El próximo despliegue automático lo pisa y nadie entiende por qué. |
| "Despliego viernes, total está verde" | Verde significa que no se detectó lo detectable. La pregunta es quién está disponible si falla el sábado. |
| "Los secretos en el .env del servidor y listo" | Bien, siempre que no estén también en el repo, en la imagen, en el historial ni en una captura del chat. |

## Formato de salida

- Checklist previo con resultados reales.
- Estrategia usada y por qué.
- Comando/pipeline ejecutado y versión publicada (etiqueta + commit).
- Verificación posterior: humo automático + camino crítico manual + métricas comparadas.
- **Procedimiento de vuelta atrás con tiempo medido**, escrito en el runbook.
- Notas del proyecto actualizadas.
