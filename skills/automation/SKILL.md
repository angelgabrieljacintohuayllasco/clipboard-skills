---
name: automation
description: Use when building unattended automation — scripts, cron jobs, scrapers, ETL/data pipelines, file processing, system integrations, browser automation, bulk operations, "automatiza esto", "un script que cada día...", "scrape this site", "sincroniza X con Y", "procesa estos archivos". Covers idempotency, resumability, rate limits, credentials, failure notification and dry-run. NO para bots conversacionales (bot-dev) ni para APIs que atienden peticiones (api-backend).
---

# Automation — código que corre cuando nadie está mirando

## Overview

Una automatización tiene una propiedad que cambia todas las reglas: **falla sin público**. Si un script de sincronización empieza a fallar el martes, puede seguir fallando hasta que alguien note, semanas después, que los datos están viejos o que se duplicó todo.

Por eso las tres preguntas de diseño no son sobre la lógica, sino sobre el silencio: ¿qué pasa si corre dos veces? ¿qué pasa si se corta a la mitad? ¿cómo me entero de que falló?

## Cuándo usar

- Tareas programadas, scripts de mantenimiento, sincronizaciones.
- Extracción de datos (scraping, APIs), transformación y carga.
- Procesos por lotes: archivos, correos, imágenes, informes.
- Automatización de navegador o de escritorio.
- Operaciones masivas sobre datos existentes.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Conversaciones con usuarios | `bot-dev` |
| Servicio que responde peticiones | `api-backend` |
| El script existe y falla con error concreto | `fixer` |
| Nadie sabe si está corriendo | `observability` |

## Regla de hierro: idempotente, reanudable y ruidosa al fallar

```
SI CORRERLA DOS VECES DUPLICA ALGO, O SI CORTARLA A LA MITAD DEJA UN ESTADO A MEDIAS, O SI FALLA EN SILENCIO — NO ESTA TERMINADA.
```

## Diseño

### Idempotencia
- Toda escritura es "crear o actualizar" con clave estable, no "insertar".
- Marcar lo ya procesado (identificador del origen + marca de tiempo) y saltarlo en la siguiente corrida.
- Los efectos externos (correo enviado, mensaje, cobro) llevan registro previo: se anota la intención, se ejecuta, se confirma. Sin eso, un corte entre ejecutar y confirmar repite el efecto.

### Reanudable
- Procesar por lotes con progreso guardado (última página, último id, último archivo).
- Cada elemento se procesa de forma independiente: un elemento malo no tumba el lote entero — se registra y se sigue.
- Al terminar: resumen con procesados, saltados, fallidos, y **lista de fallidos accionable**.

### Ruidosa
- Estado final reportado siempre, no solo cuando falla (el "no me llegó nada" es ambiguo).
- **Latido**: si no reporta en el plazo esperado, alerta. Es lo único que detecta un trabajo que ni siquiera arrancó.
- Fallos con contexto: qué elemento, qué error, qué se intentó.
- Umbral de anomalía: "procesó 3 elementos cuando siempre procesa ~500" es una falla, aunque termine con éxito.

### Modo simulación
Un interruptor `--dry-run` que muestra exactamente qué haría sin hacerlo. Obligatorio en cualquier automatización destructiva o masiva, y se usa **siempre** en la primera ejecución sobre datos reales.

### Programación
- Un candado para que dos corridas no se solapen (el trabajo de ayer sigue vivo y arranca el de hoy).
- Zona horaria explícita, con cuidado en cambios de horario.
- Reintento del trabajo completo con retardo creciente, con tope.
- Ventana de ejecución conocida: no compita con respaldos ni con la hora pico.

## Extracción de datos (scraping y APIs)

- **Primero la vía legítima**: ¿hay API, exportación o acuerdo? Casi siempre es más barata y estable que raspar.
- Revisar términos del servicio y reglas del sitio. Si el acceso no está permitido, es una decisión del dueño del proyecto y se declara por escrito; si involucra datos personales, hay además obligaciones legales.
- Ritmo humano, identificación honesta, respeto de los límites. Una automatización agresiva es un ataque de denegación de servicio en miniatura.
- Guardar el material crudo tal como llegó, aparte de lo procesado: cuando el análisis cambie, no hay que volver a pedir.
- Los selectores se rompen: aislar la extracción en un módulo, con pruebas contra una copia guardada de la página, y alerta cuando el resultado cambie de forma sospechosa (0 resultados donde siempre hubo 200).
- Nunca guardar datos personales que no necesitas, ni compartirlos, ni dejarlos sin cifrar.

## Credenciales y permisos

- Fuera del script, siempre: variables de entorno o gestor de secretos.
- Permiso mínimo: una automatización que solo lee no necesita credencial de escritura.
- Si automatizas una sesión de usuario, esa sesión tiene todos sus permisos: acota el alcance y registra lo que hace.
- Rotación planificada y prueba de que la automatización sigue viva tras rotar.

## Operaciones masivas sobre datos existentes

1. Contar primero cuántos elementos afecta. Si el número sorprende, parar.
2. Respaldo previo verificado.
3. Simulación completa y revisión de una muestra a mano.
4. Ejecutar sobre un lote pequeño y verificar el resultado real.
5. Continuar por lotes, con posibilidad de detener.
6. Guardar cómo revertir (registro de lo cambiado, no solo "lo hice").

## Gate específico

| Chequeo | Qué verifica |
|---|---|
| Doble ejecución | Correr dos veces = un solo efecto |
| Corte a la mitad | Reanuda sin duplicar ni perder |
| Fuente vacía o caída | Falla ruidosa, no "0 procesados, todo bien" |
| Elemento malformado | Se registra y el lote continúa |
| Simulación | Reporta exactamente lo que haría |
| Latido | La ausencia de corrida dispara alerta |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es un script de una vez" | Los scripts de una vez se ejecutan siete veces, la última por otra persona sin contexto. |
| "Si falla lo veo en los logs" | Nadie lee logs de procesos que "andan bien". El sistema tiene que avisar. |
| "Le pongo `sleep` para no saturar" | Ritmo, sí; pero respeta los límites reales del servicio y maneja el 429. |
| "Los datos son públicos, puedo raspar" | Público ≠ libre de términos ni de ley de datos personales. Es decisión declarada del dueño del proyecto. |
| "Lo corro directo en producción, total es lectura" | Hasta que un parámetro mal puesto convierte la lectura en un borrado. Simulación primero. |
| "El cron está puesto, listo" | Cron sin latido es una tarea que puede llevar meses muerta sin que nadie lo note. |

## Formato de salida

- Qué automatiza, cada cuánto y sobre qué volumen.
- Garantías: idempotencia, reanudación, límites respetados.
- Resultado del modo simulación y de la primera corrida real.
- Cómo se entera alguien de un fallo (canal, umbral, latido).
- Credenciales usadas y con qué permisos (nunca los valores).
- Qué hacer cuando falla: pasos en el runbook.
