---
name: intake
description: Use when someone asks for software without a written spec — "hazme un CRM de WhatsApp", "quiero una app de X", "necesito un bot que...", "build me a dashboard", a new project, a big vague feature, or a client request. Runs the discovery interview a professional developer runs with a client: clarifies goal, users, scope in/out, data, integrations, constraints, then PROPOSES the quality rules (metrics, tests, processes) and gets explicit sign-off before any code. Produces spec.md with acceptance criteria and an assumptions ledger. NO usar para bugs (triage) ni preguntas teoricas (consulta).
---

# Intake — la entrevista que convierte un deseo en un encargo

## Overview

Un programador profesional no abre el editor cuando un cliente dice "quiero un CRM". Pregunta, acota, propone, deja por escrito y recién ahí construye. Esta skill hace exactamente eso, y suma lo que el cliente nunca pide pero siempre necesita: **las reglas de calidad con las que se va a medir el resultado**.

Sin spec escrita, "listo" es una opinión. Con spec, "listo" es una lista de criterios que se pueden ejecutar.

## Cuándo usar

- Pedido nuevo, vago o grande: app, web, bot, automatización, integración, rediseño.
- Un tercero (cliente, jefe, usuario) pide algo y hay que traducirlo a trabajo.
- Funcionalidad nueva cuyo alcance no cabe en una frase.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Algo existente está roto | `triage` |
| Pregunta técnica sin construir | `consulta` |
| "¿Vale la pena esta idea?" (viabilidad, no alcance) | `valida-idea` |
| Spec ya escrita y aprobada | `constitution` → `architecture` → `feature` |

## Regla de hierro: prohibido inventar lo que no se preguntó

```
TODO HUECO SE MARCA [POR DEFINIR] O SE REGISTRA COMO SUPUESTO EXPLICITO. NUNCA SE RELLENA EN SILENCIO.
```

Un supuesto silencioso es una decisión de negocio tomada por la IA a espaldas de quien paga. Dos formas válidas de cerrar un hueco:

1. **Preguntar** — si la respuesta cambia la arquitectura, el costo o el alcance.
2. **Asumir en voz alta** — recomendación por defecto + consecuencia + registro en la tabla de supuestos: *"Asumo un solo idioma (español). Si hace falta multi-idioma, agrega ~2 días y cambia el modelo de datos."*

## Proceso

### 1. Detecta el registro (una lectura, sin preguntar)

- **Habla técnico** (stacks, versiones, errores) → conversación entre programadores: directo, denso, con nombres propios.
- **Habla de negocio** → traduce todo a tiempo, dinero, riesgo y "qué pasa si esto falla". Nunca ofrezcas opciones que no pueda evaluar; recomienda y explica el costo de equivocarse.

### 2. Ronda de preguntas — máximo 7, priorizadas por impacto

Solo preguntas cuya respuesta **cambia lo que se construye**. Cada una con recomendación por defecto para que se pueda contestar "dale, como dices". Nunca más de 2 rondas antes de entregar el borrador de spec: la tercera ronda ya es procrastinación con forma de diligencia.

**Núcleo (siempre):**

1. **Resultado**: ¿qué tiene que pasar en el mundo real para decir que funcionó? (métrica, no adjetivo)
2. **Usuarios**: ¿quién lo usa, cuántos, con qué dispositivo, qué nivel técnico?
3. **Dentro / fuera**: nombra 3 cosas que SÍ y 3 que NO están en esta versión.
4. **Datos**: ¿qué se guarda, dónde vive hoy, hay datos personales o dinero de por medio?
5. **Integraciones**: ¿con qué sistemas externos habla y quién tiene esas credenciales?
6. **Restricciones duras**: fecha, presupuesto, plataforma obligatoria, quién lo va a mantener.
7. **Fracaso**: ¿qué es lo peor que puede pasar si falla a las 3 AM? (define el perfil de rigor)

**Según el tipo** (añade 2-4, no más):

| Tipo | Preguntas que de verdad cambian el diseño |
|---|---|
| Web / SaaS | ¿Hay cuentas y roles? ¿SEO importa? ¿Pagos? ¿Multi-tenant? ¿Quién sube el contenido? |
| Bot de mensajería | ¿Canal oficial con API o no oficial? ¿Cuántos mensajes/día? ¿Responde IA o reglas? ¿Qué pasa si se cae la sesión? ¿Escala a humano? |
| Automatización / scraping | ¿Cada cuánto corre? ¿Qué pasa si la fuente cambia o bloquea? ¿Es legal el acceso? ¿Quién revisa que corrió? |
| Escritorio | ¿Qué sistemas operativos? ¿Offline? ¿Auto-actualización? ¿Instalador firmado? |
| Móvil / APK | ¿Tienda o APK directo? ¿Android mínimo? ¿Permisos sensibles? ¿Push? ¿Offline? |
| API / backend | ¿Quién la consume? ¿Público o interno? ¿Versionado? ¿Límites de uso? ¿SLA? |

### 3. Propón las reglas de calidad (esto es lo que nadie pide y todos necesitan)

Con el riesgo ya conocido, **recomienda un perfil** y explícalo en consecuencias, no en jerga:

| Perfil | Cuándo | Qué implica en la práctica |
|---|---|---|
| **P1 Prototipo** | Demo, validar una idea, uso personal, datos de mentira | Build + lint + un camino feliz probado a mano. Rápido y desechable. Se declara por escrito que NO va a producción. |
| **P2 Estándar** (por defecto) | Producto real con usuarios reales | Tests automáticos de lo que importa, límites de complejidad y tamaño, gate que corre solo, secretos fuera del repo. |
| **P3 Crítico** | Dinero, salud, datos personales, acciones irreversibles, cumplimiento legal | Todo lo anterior + revisión humana obligatoria del diff sensible, auditoría de seguridad, backups probados, rollback ensayado, registro de auditoría. |

Frase para no técnicos: *"Recomiendo P2. Significa que antes de decir 'listo' se ejecutan pruebas automáticas y el trabajo se rechaza solo si algo falla — no depende de que yo o la IA 'miremos bien'. Sube ~20% el tiempo y baja mucho el riesgo de que se rompa cuando lo esté usando gente."*

Los umbrales concretos los fija `constitution`. Aquí solo se acuerda el nivel.

### 4. Escribe el spec y pide aprobación explícita

`docs/project/spec.md`:

```markdown
# <Proyecto> — Especificación
fecha: YYYY-MM-DD · perfil: P2 · estado: borrador|aprobado

## Problema y resultado esperado
<una frase de problema. Métrica de éxito verificable.>

## Usuarios
<quién, cuántos, contexto de uso>

## Alcance
### Incluido (v1)
- ...
### Excluido explícitamente
- ...  (esto evita el 80% de las peleas de alcance)

## Criterios de aceptación
AC-1 Dado <contexto>, cuando <acción>, entonces <resultado observable>.
AC-2 ...
(Cada AC debe poder convertirse en una prueba automática. Si no se puede, está mal escrito.)

## Datos e integraciones
<qué se guarda, dónde, qué es sensible, con qué sistemas habla>

## Restricciones
<plazo, presupuesto, plataforma, quién mantiene>

## Supuestos (si alguno es falso, avisar antes de construir)
| # | Supuesto | Impacto si es falso |
|---|---|---|

## Huecos abiertos
- [POR DEFINIR] ...

## Reglas de calidad acordadas
Perfil P2 → ver docs/project/constitution.md
```

No se escribe código hasta que exista un "sí" a este documento. Si quien pide no contesta, se construye **solo lo que no depende de los huecos abiertos**, y se dice explícitamente qué quedó bloqueado.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Preguntar hace ver que no sé" | Al revés: el que no pregunta es el que entrega otra cosa. Preguntar bien es la señal más clara de oficio. |
| "Le pregunto todo de una para no molestar" | 20 preguntas de golpe no se contestan. 7 con recomendación se contestan en 2 minutos. |
| "Mejor le muestro algo y de ahí vemos" | Válido solo como prototipo P1 declarado. Si no se declara, ese prototipo termina en producción — siempre. |
| "El cliente no sabe lo que quiere" | Sabe el resultado que necesita; no sabe la forma. Traducir eso es tu trabajo, no su culpa. |
| "Las reglas de calidad las decido yo, no hace falta acordarlas" | Sin acuerdo, cada test extra parece pérdida de tiempo del cliente. Acordadas al inicio, son parte del encargo. |

## Formato de salida

1. Preguntas (≤7) con recomendación por defecto en cada una.
2. Borrador de `spec.md` con criterios de aceptación verificables.
3. Perfil de rigor recomendado + qué implica en tiempo y riesgo.
4. Tabla de supuestos y lista de `[POR DEFINIR]`.
5. Pedido explícito de aprobación y la siguiente skill (`constitution`).
