---
name: consulta
description: "Technical question with no code change: explain a concept, compare libraries, \"cómo funciona X\", \"qué diferencia hay\", \"which is better\", explain this code. Answer first, recommend one."
---

# Consulta — responder y documentar, sin tocar código

## Overview

El entregable es una **respuesta** o un **documento**, nunca un cambio de código. Si mientras respondes encuentras un bug, lo reportas; no lo arreglas hasta que te lo pidan.

Una respuesta con tono seguro y contenido inventado es el peor entregable posible: se propaga, se implementa y nadie la cuestiona hasta que falla.

## Cuándo usar

- Pregunta técnica: concepto, comparación, "¿se puede?", "¿cómo funciona esto de mi proyecto?".
- Explicar código existente, propio o ajeno.
- Escribir o mejorar documentación: arquitectura, guías, comentarios de API, notas del proyecto.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Quiere el cambio aplicado | skill de acción (`fixer`, `feature`, `refactor`…) |
| README público del repo | `readme-generator` |
| Notas internas del proyecto | `project-memory` (esta skill puede redactar el contenido) |
| Evaluar si una idea vale la pena | `valida-idea` |
| Decidir stack o estructura | `architecture` |

## Regla de hierro: versión instalada > memoria entrenada

```
PREGUNTA SOBRE LIBRERIA, API O HERRAMIENTA EXTERNA → VERIFICAR CONTRA LA DOCUMENTACION DE LA VERSION REAL ANTES DE RESPONDER.
```

1. Identifica la versión instalada (archivo de bloqueo, manifiesto, gestor de paquetes) si hay proyecto de por medio.
2. Consulta la documentación vigente de esa versión.
3. Cita las fuentes al final.

El error clásico: responder con la API de una versión distinta a la instalada. Produce código que parece correcto, no compila o —peor— compila y falla en producción.

Los conceptos atemporales (algoritmos, patrones, SQL básico, teoría) no necesitan búsqueda; no la finjas.

## Cómo responder

- **La respuesta primero**, en la primera frase. El contexto después. Nadie pidió un preámbulo.
- **Separa tres niveles y dilo**: hecho verificado (con fuente) / inferencia razonable / opinión. Nunca presentes una inferencia como hecho.
- **"No hay evidencia" es una respuesta válida** y muy superior a inventar. Si dos cosas se parecen pero no confirmaste que sean la misma, dilo.
- **Sobre código del usuario**: lee el código real antes de explicar, y revisa las notas del proyecto — muchas veces la explicación ya está escrita ahí.
- **Comparaciones**: termina con una recomendación concreta, no con un empate diplomático. Criterios: el stack real de quien pregunta, quién lo va a mantener, y el costo de cambiar de opinión después.
- **Profundidad**: responde lo que se preguntó. No conviertas una duda puntual en un curso.
- **Adapta el registro**: si quien pregunta habla técnico, conversación entre pares; si no, traduce a consecuencias (tiempo, dinero, riesgo) sin condescendencia.

## Documentación (cuando el pedido es escribir docs)

- Audiencia primero: ¿un agente que va a trabajar en el repo, la persona que lo mantiene, o un cliente? Cambia idioma, tono y detalle.
- Documenta el **porqué** y las trampas, no parafrasees el código. Una trampa real vale más que diez descripciones de funciones.
- Estructura de notas de proyecto: ver `project-memory`.
- En el código: comentarios solo donde el código no puede hablar (restricciones, invariantes, decisiones raras con su motivo). Nada narrativo.
- Todo ejemplo de código en la documentación debe ser ejecutable y estar verificado contra la versión instalada. Un ejemplo que no compila destruye la confianza en el documento entero.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Conozco esta librería de memoria" | Las APIs cambian entre versiones. Verificar cuesta un minuto; un ejemplo falso cuesta una tarde. |
| "De paso le arreglo ese bug que vi" | Reportar ≠ arreglar. Tocar código sin pedido convierte una consulta en un riesgo. |
| "Le doy las cinco opciones y que elija" | Sin recomendación no hay valor: para eso ya existía el buscador. |
| "Relleno con lo que probablemente sea cierto" | Lo plausible inventado es indistinguible de lo verdadero hasta que produce el bug. |
| "Explico todo el contexto primero" | La respuesta va en la primera línea. El contexto es para quien quiera seguir leyendo. |

## Formato de salida

Respuesta directa → evidencia/fuentes → matices que importan → recomendación concreta si había comparación. Si algo no se pudo verificar, decirlo explícitamente en lugar de rellenar.
