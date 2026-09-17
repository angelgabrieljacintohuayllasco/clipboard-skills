---
name: performance
description: Use when something is slow, heavy or expensive — "va lento", "tarda mucho en cargar", "optimize this", "la consulta demora", "se traba con muchos datos", high memory/CPU, slow page loads, growing cloud bills, or setting a performance budget before building. Measures first, finds the real bottleneck, fixes the biggest one, measures again. NO adivina optimizaciones ni reescribe por estética (refactor).
---

# Performance — medir, arreglar lo que domina, volver a medir

## Overview

La intuición sobre rendimiento es mala casi siempre. El código que parece lento rara vez es el que domina el tiempo, y optimizar sin medir agrega complejidad permanente a cambio de una mejora imaginaria.

Tres números mandan: **qué tarda hoy**, **cuánto debería tardar** y **qué porcentaje del total consume la parte que vas a tocar**. Sin los tres, no es optimización: es superstición.

## Cuándo usar

- Algo tarda y afecta a personas reales.
- Crece el costo de infraestructura sin crecer el uso.
- Definir presupuesto de rendimiento antes de construir.
- Consumo de memoria que sube hasta reiniciar.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Está roto, no lento | `fixer` |
| Código enredado sin problema medido de velocidad | `refactor` (por mantenibilidad, no por rendimiento) |
| No se sabe si es lento porque nadie mide | `observability` primero |

## Regla de hierro: sin medición previa no hay optimización

```
PROHIBIDO TOCAR CODIGO POR RENDIMIENTO SIN: MEDICION BASE + OBJETIVO + PERFIL QUE SEÑALE AL CULPABLE.
```

Y después del cambio, la misma medición repetida. "Se siente más rápido" no es un resultado; es un sesgo.

## Proceso

### 1. Definir el objetivo en números
Qué operación, qué percentil, qué condiciones. "Rápido" es inútil; **"el listado de pedidos responde en menos de 400 ms en el percentil 95 con 50.000 registros"** es un objetivo.

Presupuestos razonables para partir:

| Contexto | Presupuesto típico |
|---|---|
| Página web (usuario real, móvil) | Contenido principal visible < 2.5 s; respuesta a interacción < 200 ms; sin saltos de maquetación |
| Endpoint de API | p95 < 300 ms para lectura simple |
| Tarea por lotes | Tiempo por elemento estable a medida que crece el volumen |
| Bot de mensajería | Primera respuesta < 2 s (o acuse inmediato + respuesta luego) |
| Escritorio | Arranque < 3 s; interfaz nunca bloqueada > 100 ms |

### 2. Medir el estado actual
Con datos realistas en volumen. Medir con 10 registros y desplegar con 500.000 es la trampa más frecuente. Mide el sistema completo primero (dónde se va el tiempo: red, base de datos, render, CPU) antes de mirar una función.

### 3. Perfilar, no adivinar
Herramienta de perfilado, traza o registro con tiempos por fase. Busca:

| Sospechoso | Señal |
|---|---|
| **Consultas N+1** | Cientos de consultas iguales con distinto parámetro. La causa número uno en aplicaciones con base de datos. |
| Falta de índice | Escaneo secuencial en el plan de ejecución |
| Traer todo | `SELECT *`, sin paginar, cargar en memoria y filtrar en código |
| Trabajo en el camino crítico | Enviar correos, generar PDFs o llamar a terceros dentro de la petición |
| Serialización | Llamadas independientes hechas en fila en vez de en paralelo |
| Trabajo repetido | El mismo cálculo por cada elemento del bucle |
| Frontend pesado | Paquete gigante, imágenes sin optimizar, render bloqueado, fuentes que trancan |
| Fuga de memoria | Crecimiento que solo baja al reiniciar: temporizadores, listeners y cachés sin límite |

### 4. Arreglar lo que domina
Ley práctica: **si algo consume el 5% del tiempo, optimizarlo al doble ahorra 2,5%**. Ataca lo que consume el 60%. Orden de intervención, de barato a caro:

1. Borrar trabajo innecesario (la optimización perfecta: código que ya no corre).
2. Arreglar la consulta o agregar el índice.
3. Hacer el trabajo en segundo plano (cola) en vez de en la petición.
4. Paralelizar lo independiente.
5. Cachear — **solo después de lo anterior**, con clave clara, caducidad e invalidación pensadas. Una caché mal invalidada es un bug de datos, que es peor que ser lento.
6. Cambiar de algoritmo o estructura de datos.
7. Escalar hardware: es la última, no la primera, y es la única que factura todos los meses.

Un cambio por vez, midiendo entre cada uno. Dos cambios juntos y no sabrás cuál sirvió.

### 5. Verificar y proteger
- Repite la medición base en las mismas condiciones y publica el antes/después.
- El gate no debe empeorar: tamaño del paquete, tiempo del conjunto de pruebas, tiempo del endpoint crítico.
- Registra en `state.md` qué se optimizó y qué quedó identificado para después.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Esto seguro es el cuello de botella" | La intuición acierta poco. Perfila: casi siempre es una consulta, no el algoritmo bonito. |
| "Le pongo caché y listo" | La caché esconde el problema y agrega invalidación, datos viejos y una fuente nueva de bugs. |
| "Optimizo mientras escribo" | Optimización prematura: complejidad segura a cambio de beneficio incierto. Escribe claro, mide, luego optimiza lo que domine. |
| "Con más servidor se arregla" | Escalar un N+1 solo hace que el desastre cueste más por hora. |
| "En mi máquina va rápido" | Tu máquina tiene la base local, datos de juguete y red perfecta. Mide donde duele. |
| "Micro-optimizo este bucle" | Ganancia de microsegundos mientras una consulta se lleva 800 ms. |

## Formato de salida

- Objetivo numérico y condiciones de medición.
- Medición base con la herramienta usada.
- Cuello de botella identificado con evidencia (plan de consulta, perfil, traza).
- Cambio aplicado y medición posterior: antes → después, mismo escenario.
- Lo que se decidió NO optimizar y por qué.
- Protección agregada para que no vuelva a degradarse.
