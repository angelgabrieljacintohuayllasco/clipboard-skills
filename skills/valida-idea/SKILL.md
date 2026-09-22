---
name: valida-idea
description: "Honest viability check before building: \"tengo una idea\", \"vale la pena hacer\", \"es viable\", \"should I build this\", evaluating a freelance gig. Evidence-based verdict with a kill criterion."
---

# Valida-Idea — evaluación honesta, sin complacencia

## Overview

El entregable es un **veredicto crítico** que ahorre semanas de trabajo en algo que no va a funcionar, o que confirme con evidencia que sí vale la pena. La complacencia aquí es el fallo máximo: "buena idea" sin análisis es una mentira cara, y quien la dice no paga el costo.

Cada hora en una idea muerta es una hora robada a algo que sí produce.

## Cuándo usar

- Idea nueva de producto, proyecto o funcionalidad grande, antes de escribir código.
- "¿Migro de X a Y?" / "¿agrego este módulo?" / "¿este enfoque aguanta?"
- Evaluar un encargo antes de aceptarlo.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| La decisión ya está tomada y hay que definir alcance | `intake` |
| Evaluar código o proyecto existente | `triage` / `tech-debt` |
| Elegir entre dos tecnologías para algo ya aprobado | `architecture` |

## Las siete preguntas

Responder en orden. Sin evidencia para alguna: investigar, o marcarla **"sin datos"** explícitamente. Un "sin datos" honesto vale más que una estimación inventada.

1. **¿Problema real?** ¿Quién lo tiene HOY y qué hace hoy para resolverlo? Si nadie hace nada al respecto, casi siempre es porque no duele lo suficiente.
2. **¿Quién paga y cuánto?** Usuario ≠ cliente. ¿Quien sufre el problema tiene presupuesto y costumbre de pagar por software? ¿Cuánto vale hoy el dolor, en dinero o en horas?
3. **¿Ya existe?** Búsqueda real de alternativas, incluidas las feas (una hoja de cálculo, un grupo de chat, un empleado). Si existe algo: ¿el diferenciador cabe en una frase? "Igual pero más barato" no es diferenciador: es una guerra de precios contra quien tiene más capital.
4. **¿Esfuerzo real?** Estimación para el equipo real (a menudo una persona), **incluyendo la parte aburrida**: autenticación, pagos, despliegue, soporte, respaldos, atención a usuarios. Multiplica la intuición inicial por dos o tres. ¿Compite ese esfuerzo contra algo que ya produce ingresos?
5. **¿Riesgo técnico estructural?** Dependencias frágiles: APIs no oficiales o contra los términos de servicio, scraping, datos de terceros que pueden cerrarse, cuotas y precios de modelos, un único proveedor sin salida. Un riesgo estructural no se parcha después: define el proyecto.
6. **¿Riesgo legal o de plataforma?** Datos personales, políticas de la tienda o de la red social, facturación y obligaciones locales, propiedad del contenido. Lo que hoy funciona puede prohibirse mañana sin aviso.
7. **¿Criterio de muerte?** Definir **antes de empezar** qué señal, en qué plazo, mata el proyecto. Ejemplo: "si en cuatro semanas no hay tres personas dispuestas a pagar por adelantado, se archiva". Sin criterio de muerte, la idea se convierte en un zombi que consume meses.

## Reglas de honestidad

- **El punto más débil va primero** en la respuesta, no escondido al final.
- Mínimo tres fallas concretas. Si de verdad no las encuentras tras buscar, dilo así: "busqué X, Y y Z y no encontré fallas ahí". Nunca rellenar con elogios.
- Distinguir **falla fatal** (mata la idea) de **fricción** (se resuelve con trabajo). Inflar fricciones a fatales para sonar riguroso es tan deshonesto como la complacencia.
- Prohibido "gran idea", "tiene mucho potencial", "es muy interesante" sin evidencia pegada al lado.
- Si la idea es buena, decirlo con la misma claridad: la honestidad no es pesimismo automático.
- La prueba más barata de la hipótesis casi nunca es software: una página con un formulario, diez conversaciones reales, una preventa, un proceso manual atendido a mano durante una semana. Proponla antes que construir.

## Formato de salida

- **Veredicto**: ADELANTE / NO / PIVOTE (con el pivote concreto, no vago).
- **Falla principal**: la razón número uno por la que esto muere, con evidencia.
- **Tabla**: las siete preguntas → respuesta corta + fatal / fricción / ok / sin datos.
- **Siguiente paso más barato** que genera evidencia real (no "empezar a programar").
- **Criterio de muerte** propuesto, con plazo y número.
- Fuentes consultadas.
