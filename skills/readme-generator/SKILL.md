---
name: readme-generator
description: Use when the user asks to generate, create or improve a README for a project — "hazme un README", "documenta el repo para GitHub", "write a README", onboarding docs for a public or shared repository. Inspects the real project (manifest, scripts, entry points, config) and writes an accurate README with install, usage, configuration and contribution steps. NO inventa funcionalidades ni comandos; no reemplaza las notas internas del proyecto (project-memory) ni AGENTS.md.
---

# README-Generator — el documento que decide si alguien usa tu proyecto

## Overview

El README responde, en menos de un minuto: **qué es esto, para qué sirve, cómo lo pruebo, y qué necesito antes.** Si el lector tiene que leer código para responder eso, el README falló.

Regla absoluta: **cada comando escrito debe existir de verdad en el proyecto.** Un README con comandos inventados es peor que no tener README, porque quema la confianza en el primer intento.

## Proceso

1. **Inspeccionar el proyecto real**: manifiesto y scripts, punto de entrada, estructura de carpetas, variables de entorno usadas, archivos de configuración, licencia, herramientas del gate, archivos de CI.
2. **Verificar lo que vas a escribir**: los comandos de instalación, arranque, pruebas y build salen del proyecto, no de la costumbre del ecosistema.
3. **Detectar lo que falta** y decirlo: sin licencia, sin archivo de ejemplo de variables, sin instrucciones de pruebas. Eso es un hallazgo útil, no un hueco que se rellena con suposiciones.
4. **Escribir corto y verdadero**. Un README que nadie termina de leer es un README que no se lee.

## Secciones (omitir las que no apliquen)

```markdown
# <Nombre>
<Una frase: qué hace y para quién. Sin adjetivos de marketing.>

## Requisitos
<versiones de runtime, servicios externos, cuentas necesarias>

## Instalación
<comandos reales, en orden>

## Configuración
<variables de entorno: nombre, para qué sirve, si es obligatoria. Nunca valores reales>

## Uso
<el caso más común, con un ejemplo ejecutable y su salida esperada>

## Desarrollo
<cómo arrancar en local, cómo correr las pruebas, cómo pasar el gate>

## Estructura
<solo si ayuda a orientarse: 5-10 líneas, no el árbol completo>

## Despliegue
<cómo se publica, si aplica>

## Contribuir
<flujo de ramas, estándar de commits, qué debe pasar antes de un PR>

## Licencia
```

## Reglas

- Ningún comando sin verificar que existe en el proyecto.
- Ninguna funcionalidad inventada ni "próximamente" sin respaldo.
- Nunca valores reales de secretos, ni siquiera de ejemplo si se parecen a los verdaderos.
- Ejemplos ejecutables tal como están escritos, con la salida esperada cuando aporte.
- Capturas o diagramas solo si de verdad explican algo.
- Idioma: el del equipo que lo mantiene; si el repo es público e internacional, inglés, y se puede dejar una versión traducida aparte.
- **No dupliques `AGENTS.md`**: el README es para personas que van a usar o contribuir; `AGENTS.md` es el contexto operativo para agentes y para quien trabaja dentro del repo. Enlázalos entre sí.
- Fecha o versión al pie si el proyecto cambia rápido.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Pongo `npm start` que es lo habitual" | Si el proyecto no lo define, acabas de escribir una mentira en la primera pantalla. |
| "Agrego todas las secciones por completitud" | Secciones vacías o genéricas entrenan al lector a no leer. Omite lo que no aplica. |
| "Describo cada carpeta del árbol" | Eso envejece en una semana. Describe solo lo que ayuda a orientarse. |
| "El README explica la arquitectura completa" | Eso va en las notas del proyecto. El README es la puerta, no el manual. |

## Formato de salida

`README.md` escrito, la lista de comandos verificados (con su resultado), y los huecos encontrados en el proyecto (licencia, ejemplo de variables, instrucciones de pruebas) para que alguien decida.
