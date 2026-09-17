---
name: data-layer
description: Use when designing or changing how data is stored — schema design, tables/collections, relations, migrations, "qué base de datos uso", "cómo modelo esto", "add a column", "migrar datos", backups, imports/exports, data cleanup, or anything that can lose or corrupt records. Covers modeling, safe migrations, integrity, backups and restore drills. NO optimiza consultas lentas (performance) ni diseña la arquitectura general (architecture).
---

# Data-Layer — lo único que no se puede volver a compilar

## Overview

El código se puede reescribir en una tarde. Los datos perdidos no vuelven. Por eso el modelo de datos es la decisión más cara de revertir de todo el proyecto, y una migración mal hecha es el incidente con peor final posible.

Dos reglas cubren la mayor parte del riesgo: **la base de datos defiende sus propias reglas** (no confíes en que la aplicación sea el único camino de entrada) y **ninguna migración destructiva corre sin respaldo verificado y forma de volver atrás**.

## Cuándo usar

- Diseñar el esquema inicial o agregar entidades.
- Cualquier migración: columnas, tipos, índices, renombres, borrados.
- Importar, exportar, limpiar o deduplicar datos.
- Definir respaldos y retención.
- Datos que se corrompieron o se duplicaron.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Consulta lenta, esquema correcto | `performance` |
| Elegir motor como decisión estructural mayor | `architecture` (con ADR) |
| Datos personales y cumplimiento | `app-security` (esta skill cubre la parte técnica) |

## Regla de hierro: nada destructivo sin respaldo probado

```
ANTES DE UNA MIGRACION DESTRUCTIVA: RESPALDO HECHO, RESTAURACION PROBADA, PASO ATRAS ESCRITO.
UN RESPALDO QUE NUNCA SE RESTAURO NO ES UN RESPALDO: ES UN ARCHIVO.
```

## Modelado

- Empieza por las **entidades del negocio y sus reglas**, no por las pantallas. La pantalla cambia cada semana; la entidad, casi nunca.
- Normaliza primero; desnormaliza después con una razón medida (`performance`), documentada como ADR.
- Restricciones en la base: claves foráneas, `NOT NULL`, `UNIQUE`, `CHECK`. Son la última línea de defensa y la única que no se puede saltar desde otro script.
- Claves: identificador estable e interno; nunca uses un dato de negocio (correo, documento) como clave primaria — cambian.
- Tipos honestos: dinero en enteros de centavos o tipo decimal, **jamás flotante**. Fechas con zona horaria explícita, guardadas en UTC. Enumeraciones controladas.
- Marcas de tiempo `creado_en` / `actualizado_en` en todo. Cuestan nada y salvan investigaciones.
- Borrado lógico cuando el dato tenga valor histórico o legal; borrado físico cuando el usuario tiene derecho al olvido. Decide explícitamente: los dos mezclados son bugs asegurados.
- Estados de negocio como máquina de estados explícita, no como banderas booleanas sueltas que se contradicen entre sí.

## Migraciones

1. **Versionadas y en el repo**, nunca cambios a mano en producción. Si se toca a mano, se pierde la reproducibilidad y el próximo despliegue rompe.
2. Cada migración tiene **paso atrás** escrito (o una nota explícita de por qué es irreversible y qué se hace en su lugar).
3. Probar la migración sobre una **copia real** de producción, no sobre datos de juguete: el tiempo y los conflictos de datos solo aparecen con el volumen y la suciedad reales.
4. **Expandir → migrar → contraer** para cambios que rompen: agregar lo nuevo, escribir en ambos, copiar datos, cambiar lecturas, y recién en un despliegue posterior borrar lo viejo. Nunca renombrar o eliminar una columna en el mismo despliegue que cambia el código.
5. Tablas grandes: cuidado con bloqueos largos; índices creados de forma concurrente cuando el motor lo permita; lotes con pausa.
6. Migración de datos (no de esquema): idempotente y reanudable, con registro de progreso. Si se corta a la mitad, debe poder correr otra vez sin duplicar.

## Integridad y concurrencia

- Transacciones para lo que debe ser atómico; nada de secuencias de escrituras "que casi siempre terminan bien".
- Operaciones que pueden repetirse (reintentos, webhooks, doble clic) necesitan **clave de idempotencia** y restricción única que la respalde.
- Condiciones de carrera clásicas: leer-modificar-escribir sin bloqueo, contadores incrementados en código, reservas de stock. Resolver con la base (bloqueo, `UPSERT`, restricción única), no con esperanza.
- Trabajos programados que corren dos veces por solapamiento: candado explícito.

## Respaldos y recuperación

| Pregunta | Respuesta obligatoria |
|---|---|
| ¿Cada cuánto se respalda? | según cuánta pérdida es tolerable |
| ¿Dónde se guarda? | fuera del mismo servidor y del mismo proveedor de cuenta única |
| ¿Está cifrado? | sí, y la clave no vive junto al respaldo |
| ¿Cuánto tarda restaurar? | medido, no estimado |
| ¿Cuándo se probó por última vez? | fecha real. Sin ensayo, el plan es ficción |
| ¿Qué se pierde entre respaldos? | declarado y aceptado por quien paga |

Un ensayo de restauración por trimestre, con cronómetro, anotado en el `runbook.md`.

## Datos personales

- Guardar el mínimo, con propósito declarado y plazo de retención.
- Poder responder: qué guardo de esta persona, cómo lo exporto, cómo lo borro.
- Nunca copiar datos reales a entornos de desarrollo o de prueba sin anonimizar.
- Los volcados de base son la filtración más común: cifrados, con caducidad, jamás en un repositorio ni en un chat.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Las restricciones las maneja la aplicación" | Hasta que alguien corre un script, un import o una segunda app. La base es lo único que nadie se salta. |
| "Es un cambio chico, lo hago directo en producción" | Cambio manual = irreproducible. El siguiente despliegue te lo recuerda. |
| "Después le pongo los índices" | Después la tabla tiene millones de filas y el índice bloquea la tabla en hora pico. |
| "El proveedor hace respaldos" | ¿Restauraste uno alguna vez? ¿Cuánto tarda? ¿Cubre el borrado accidental de ayer? |
| "Uso flotantes para el dinero, es más simple" | Es más simple hasta que el total no cuadra por céntimos y nadie sabe por qué. |
| "Guardo todo por si acaso" | Cada dato extra es riesgo legal, costo y superficie de filtración. |
| "La migración anduvo en mi máquina" | Tu máquina tiene 200 filas limpias. Producción tiene 4 millones sucias. |

## Formato de salida

- Modelo: entidades, relaciones, restricciones y por qué.
- Migración: pasos, paso atrás, tiempo estimado sobre copia real, plan de despliegue (expandir/contraer si aplica).
- Estado de respaldos: frecuencia, destino, cifrado, **fecha del último ensayo de restauración**.
- Riesgos de pérdida de datos identificados y cómo se mitigan.
