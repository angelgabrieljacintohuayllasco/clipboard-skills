---
name: diff-review
description: Use to review a change before it ships — "revisa este código", "revisa el diff", "review my PR", code written by an AI agent or another dev, changes touching auth/money/personal data/migrations, or when the automatic gate is green but the change is sensitive. Reviews by risk: correctness against acceptance criteria, security, data integrity, blast radius, then style. Produces findings with file:line, severity and concrete fix. NO corre las métricas (quality-gate) ni arregla bugs por su cuenta sin decirlo (fixer).
---

# Diff-Review — leer lo que la máquina no puede ver

## Overview

Las métricas cubren lo detectable: complejidad, cobertura, duplicación, dependencias, secretos. Son ciegas a lo que más caro sale: un permiso invertido, un endpoint que no valida propiedad, un redondeo de dinero, una migración que borra datos, un `await` faltante. Esa es la mitad humana del trato — pocos diffs, leídos de verdad.

Revisión no es opinión de estilo. Es una búsqueda ordenada de fallas por riesgo decreciente.

## Cuándo usar

- Diff que toca zonas sensibles declaradas en la constitución (auth, dinero, datos personales, migraciones, criptografía, envíos a terceros).
- Código generado por un agente que va a producción.
- Antes de un merge en perfil P3, siempre.
- Cuando el gate está verde pero algo no cierra.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Aún no corrieron las verificaciones automáticas | `quality-gate` primero: no gastes lectura humana en lo que un linter detecta |
| Revisión de estilo general del repo | `code-standard` |
| Auditoría de deuda acumulada | `tech-debt` |
| Ya hay un bug confirmado | `fixer` |

## Regla de hierro: el orden de lectura es por riesgo

```
CORRECCION > SEGURIDAD > DATOS > RADIO DE IMPACTO > LEGIBILIDAD > ESTILO.
NUNCA EMPIECES POR EL ESTILO: CONSUME LA ATENCION QUE NECESITA LO GRAVE.
```

## Proceso

### 1. Contexto en dos minutos
Qué criterio de aceptación dice cumplir, qué archivos toca, qué tamaño tiene. Un diff enorme se devuelve para partir: pasadas cierta cantidad de líneas la revisión detecta cada vez menos, y todos lo aprueban igual.

### 2. Corrección — ¿hace lo que dice?
- ¿Cubre el AC completo o solo el camino feliz?
- Bordes: vacío, nulo, cero, negativo, duplicado, muy grande, unicode, zona horaria, concurrencia.
- Condiciones límite: `<` vs `<=`, índices, rangos de fecha inclusivos.
- Asincronía: promesas sin esperar, errores que se pierden, condiciones de carrera, reintentos que duplican efectos.
- ¿Los tests nuevos fallarían si el código estuviera mal? Si pasan con la implementación rota, no prueban nada.

### 3. Seguridad — el guion corto que atrapa casi todo
Basado en las categorías con más incidencia real (OWASP Top 10:2025):

- **Control de acceso roto** (#1 histórico): ¿se verifica que el usuario sea dueño del recurso, o basta con estar autenticado? ¿Se puede cambiar un id en la URL y ver lo ajeno? ¿Se confía en algo que llega del cliente para decidir permisos?
- **Configuración insegura**: depuración activa, CORS abierto, cabeceras faltantes, buckets públicos, valores por defecto.
- **Cadena de suministro**: dependencia nueva sin auditar, versión sin fijar, script de instalación.
- **Criptografía y secretos**: claves en el código, aleatoriedad débil, hashing de contraseñas casero, tokens sin expiración.
- **Inyección**: consultas concatenadas, comandos del sistema con entrada de usuario, plantillas sin escapar.
- **Autenticación**: sesiones que no expiran, recuperación de cuenta débil, sin límite de intentos.
- **Registro**: eventos de seguridad sin traza, o al revés, secretos y datos personales escritos en logs.
- **Manejo de excepciones**: errores tragados, mensajes que filtran internals, caminos de fallo sin probar.

### 4. Datos — lo único irrecuperable
- Migraciones: ¿reversibles? ¿bloquean tabla grande? ¿hay respaldo probado antes?
- Borrados: ¿lógicos o físicos? ¿en cascada sin querer?
- Transacciones: ¿operaciones que deben ser atómicas quedaron sueltas?
- Dinero: ¿decimales exactos y no flotantes? ¿redondeo definido? ¿idempotencia en cobros?
- Datos personales: ¿se guarda lo mínimo? ¿se puede borrar y exportar?

### 5. Radio de impacto
¿Qué más usa lo que cambió? Firma modificada, contrato de API, formato de evento, clave de caché, variable de entorno nueva sin valor por defecto, cambio de comportamiento que otros módulos asumían. Buscar los usos, no suponerlos.

### 6. Legibilidad y estilo (al final, y breve)
Solo lo que encarece el mantenimiento de verdad: nombres que mienten, funciones que hacen tres cosas, olores del catálogo de `code-standard`. El resto lo hace el formateador.

## Severidades

| Nivel | Qué es | Efecto |
|---|---|---|
| **Bloqueante** | Rompe, expone datos, pierde dinero o información | No se entrega. Sin discusión. |
| **Grave** | Falla en un borde previsible, sin prueba de un camino crítico | Se arregla antes del merge |
| **Menor** | Encarece el mantenimiento | Se arregla o se registra como deuda con fecha |
| **Nota** | Preferencia, alternativa | Opcional; no bloquea nada |

Cada hallazgo: **archivo:línea + qué falla + escenario concreto de fallo + corrección propuesta.** Un hallazgo sin escenario de fallo concreto suele ser una opinión disfrazada.

## Revisar código generado por IA: dónde mirar primero

| Patrón típico | Qué buscar |
|---|---|
| Funciones o utilidades duplicadas | Ya existía algo equivalente en el repo con otro nombre |
| Manejo de errores decorativo | `try/catch` que registra y sigue como si nada |
| Dependencia agregada de más | Resuelve en tres líneas lo que ya hacía la librería estándar |
| APIs inventadas | Método o parámetro que no existe en la versión instalada — verificar contra la documentación de esa versión |
| Tests que reafirman el código | Escritos después, calcados de la implementación; no fallan nunca |
| Validación solo en el cliente | El servidor confía |
| Configuración cambiada de paso | Umbral del gate, versión de dependencia o variable tocada sin relación con el objetivo |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "El gate está verde, no hace falta leer" | El gate no ve un permiso invertido ni una migración destructiva. Por eso existen las zonas sensibles. |
| "Es mucho diff, lo apruebo por encima" | Una revisión por encima da permiso sin dar seguridad. Devuelve el diff partido. |
| "Lo escribí yo, ya lo revisé" | Nadie encuentra sus propios puntos ciegos. En P3, revisa alguien que no escribió. |
| "Son nits, mejor no molestar" | Distingue: lo bloqueante se dice sin adornos; lo menor se ofrece. Callar lo grave por cortesía es el peor resultado posible. |
| "La IA lo generó, seguro está bien" | Sale plausible, que no es lo mismo que correcto. Lo plausible es justamente lo difícil de revisar. |

## Formato de salida

```
REVISION: <rama/PR> — <N> hallazgos (<n> bloqueantes)

BLOQUEANTE  src/api/orders.ts:42
  Cualquier usuario autenticado puede leer pedidos ajenos: se valida sesión pero no propiedad.
  Escenario: token de usuario A + GET /orders/<id de B> → 200 con datos de B.
  Fix: filtrar por userId en la consulta y test AC-7 que lo cubra.

GRAVE  src/billing/total.ts:18
  Total con flotantes: 0.1 + 0.2 → 0.30000000000000004 en el cobro.
  Fix: enteros en centavos o tipo decimal.

Veredicto: no entregar hasta resolver los 2 primeros.
```
