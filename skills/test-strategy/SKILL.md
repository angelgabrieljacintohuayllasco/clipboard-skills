---
name: test-strategy
description: "Decide what and how to test: \"no hay tests\", \"qué pruebo\", \"write tests\", flaky or slow suites, useless coverage, legacy characterization tests, mutation testing."
---

# Test-Strategy — la red que permite no leer cada línea

## Overview

Si el humano deja de auditar el código que escribe la IA, **la suite de pruebas es lo único que queda entre el cambio y el usuario**. Eso cambia el criterio de diseño: no se prueba para subir un número, se prueba para poder aceptar código que nadie leyó.

Cobertura alta con tests que no afirman nada es peor que no tener tests: da permiso para confiar. El puntaje de mutación existe justo para medir eso — cuántos fallos inyectados detecta tu suite de verdad.

## Cuándo usar

- Proyecto sin tests, o con tests que no atrapan nada.
- Convertir criterios de aceptación del spec en pruebas ejecutables.
- Antes de refactorizar (tests de caracterización).
- Suite lenta, frágil o intermitente.
- Cobertura alta y aun así se escapan bugs.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Correr y evaluar métricas | `quality-gate` |
| Fijar umbrales por perfil | `constitution` |
| Bug concreto con stack trace | `fixer` (prueba de regresión incluida) |
| Prototipo P1 desechable | 1 smoke test del camino feliz y seguir |

## Regla de hierro: el test se escribe viendo fallar

```
UN TEST QUE NUNCA SE VIO EN ROJO NO PRUEBA NADA.
```

Procedimiento: escribe el test → córrelo y **observa el fallo** → implementa → míralo pasar. Si pasó a la primera, rompe a propósito el código (cambia un `>` por `>=`, devuelve `null`) y confirma que el test se cae. Un test que pasa con el código roto es peor que ningún test.

## Cómo repartir el esfuerzo

| Nivel | Qué prueba | Proporción sugerida | Regla |
|---|---|---|---|
| **Unitario** | Lógica de dominio pura: cálculos, reglas, validaciones, máquinas de estado | ~70% | Sin red, sin disco, sin reloj. Milisegundos. Es donde vive la mutación. |
| **Integración** | Los bordes: base de datos real, cola, sistema de archivos, cliente HTTP contra doble local | ~20% | Un mock del borde no prueba el borde. Al menos uno real por integración. |
| **E2E / aceptación** | Los 3-5 caminos por los que la gente paga | ~10% | Lento y frágil por naturaleza: pocos, estables, sobre los flujos del spec. |
| **Contrato** | Lo que prometes a otros sistemas | según integraciones | Si terceros dependen de tu formato, un cambio silencioso rompe a otros. |

Regla práctica: **cada criterio de aceptación (AC-n) del spec se mapea a un test con su identificador en el nombre.** Así la trazabilidad spec ↔ suite es mecánica:

```
test('AC-3: cliente sin saldo no puede confirmar pedido', ...)
```

## Qué probar primero (orden de valor)

1. **Lo que cuesta dinero o datos si falla**: cobros, permisos, borrados, envíos a terceros.
2. **Lo que ya falló antes**: todo bug arreglado nace con su prueba de regresión. Sin esa prueba, el bug vuelve.
3. **Reglas de negocio con ramas**: descuentos, estados, límites, fechas, impuestos.
4. **Bordes y valores límite**: 0, negativo, vacío, nulo, duplicado, gigante, unicode, zona horaria.
5. **Concurrencia e idempotencia**: doble clic, reintento del webhook, dos procesos a la vez.

## Qué NO probar (YAGNI aplicado a tests)

- Frameworks y librerías de terceros: ya tienen sus tests.
- Getters, setters y DTOs sin lógica.
- Detalles de implementación privados: se rompen con cada refactor y no prueban comportamiento.
- Maquetación pixel a pixel (para eso, pruebas visuales aparte y con criterio).
- El camino feliz repetido diez veces con distintos nombres.

Test que se rompe cada vez que se mueve código sin cambiar comportamiento = test mal escrito. Prueba **comportamiento observable**, no estructura interna.

## Legado sin tests: caracterización

1. Elige la frontera más estrecha que rodee lo que vas a tocar.
2. Escribe tests que capturen lo que el sistema **hace hoy**, no lo que debería hacer (aunque sea feo — el objetivo es detectar cambios, no juzgar).
3. Con la red puesta, recién ahí `refactor`.
4. Cuando descubras que un comportamiento actual está mal, no lo corrijas en el mismo paso: anótalo y decídelo con quien manda.

## Mutación: la prueba de las pruebas

- Mide qué porcentaje de fallos inyectados detecta la suite. Referencia práctica: 75-85% es sólido; por debajo de 60% hay huecos serios; 100% es inalcanzable por mutantes equivalentes.
- Córrela sobre el **núcleo de dominio**, no sobre todo el repo (es cara).
- Incremental sobre archivos cambiados en el día a día; completa de noche o semanal.
- Un mutante sobreviviente es una pregunta honesta: *"si cambio esto y nadie se queja, ¿para qué está esta línea?"* — a veces la respuesta es borrar código, no agregar un test.

## Suites frágiles: causas y arreglo

| Síntoma | Causa típica | Arreglo |
|---|---|---|
| Falla 1 de cada 10 corridas | Esperas por tiempo (`sleep`), orden de tests, estado compartido | Esperar por condición, aislar estado, resetear BD por test |
| Falla solo en CI | Zona horaria, locale, rutas, recursos | Fijar TZ y locale en el entorno de test; rutas relativas al proyecto |
| Falla al cambiar el orden | Tests que dependen unos de otros | Cada test crea su propio dato; nada de fixtures globales mutables |
| Lenta (>5 min) | E2E de más, BD sin transacciones | Bajar de nivel: mover reglas a tests unitarios; transacción por test |
| Fechas rompen en enero | `new Date()` real dentro del dominio | Reloj inyectable; nunca tiempo real en lógica |

Un test intermitente que se ignora entrena al equipo a ignorar el rojo. O se arregla, o se borra: mantenerlo es peor que las dos.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Escribo los tests después" | Después el código ya tiene la forma de lo intestable (dependencias duras, efectos en el constructor). El test escrito antes es también un diseño. |
| "Es muy difícil de testear" | Eso no es un problema del test: es el diseño avisando. Extrae la lógica pura del efecto. |
| "Tengo 90% de cobertura" | ¿Y de mutación? La cobertura dice qué se ejecutó; la mutación dice qué se verificó. |
| "Mockeo todo, es más rápido" | Y no prueba nada real. Los mocks de tus propios bordes se desincronizan con la realidad en silencio. |
| "El E2E cubre todo, no necesito unitarios" | Un E2E rojo dice "algo se rompió". Un unitario rojo dice qué, dónde y por qué. |
| "Ese bug no vuelve a pasar" | Vuelve. Siempre vuelve. Por eso el fix trae su test. |

## Formato de salida

- Plan de pruebas: qué se prueba en cada nivel y por qué, con el mapeo AC-n → test.
- Lista de lo que explícitamente NO se prueba, con motivo.
- Tests escritos (vistos en rojo antes de verlos en verde).
- Puntaje de mutación del núcleo si aplica, con los mutantes sobrevivientes relevantes.
- Deuda de pruebas pendiente, priorizada por riesgo.
