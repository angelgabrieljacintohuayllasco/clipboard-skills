---
name: ui-design
description: "Any time you create or restyle a user interface (web, desktop, mobile, dashboard, landing, component). Makes it look designed by a professional, not vibecoded: no emojis, no AI clichés, real type/spacing/color system."
---

# UI-Design — que no parezca hecho por una IA en cinco minutos

## Overview

Una interfaz generada por IA se reconoce a un metro: degradado violeta-azul, emojis como iconos, tarjetas con sombra enorme y esquinas de 24 px, un "hero" que dice "Bienvenido a X" con un cohete al lado, tres columnas de "features" con icono, título y dos líneas de relleno, todo centrado, todo del mismo peso. Funciona, pero grita "plantilla" y el cliente lo percibe como barato aunque el backend sea impecable.

La diferencia con un diseño profesional no es talento: son **decisiones explícitas y sostenidas** (una escala tipográfica, una escala de espaciado, una paleta corta, una jerarquía) y **la disciplina de mirar el resultado** y corregirlo antes de entregar.

Esta skill se aplica siempre que se escribe UI. Complementa a `web-app`, `desktop-app` y `mobile-app`, que cubren estados, accesibilidad y entrega; aquí se cubre cómo se ve.

## Regla de hierro

```
CERO EMOJIS EN LA INTERFAZ, EN EL CÓDIGO, EN LOS LOGS, EN LOS COMMITS Y EN LA DOCUMENTACIÓN.
NADA SE ENTREGA SIN HABERLO MIRADO RENDERIZADO (CAPTURA EN MÓVIL Y ESCRITORIO).
```

Iconos: un set SVG coherente (Lucide, Phosphor, Heroicons, Tabler o el nativo de la plataforma: SF Symbols, Material Symbols, Fluent). Un solo set por proyecto, un solo grosor de trazo, tamaños de la escala (16/20/24). Si el usuario pide emojis explícitamente, es la única excepción.

## Paso 0 — Dirección antes de píxeles (2 minutos, no una entrevista)

Antes de escribir CSS, decide y escribe en una línea cada cosa. Si el proyecto ya tiene sistema de diseño, marca o componentes, **se usan esos** y este paso se reduce a leerlos.

| Decisión | Ejemplo de respuesta concreta |
|---|---|
| Tipo de producto y densidad | Panel de operaciones: denso, tablas, poco aire. Landing: aire, una idea por pantalla. |
| Tono | Sobrio / técnico / editorial / cálido-local. Uno. |
| Referencia real | "Como Linear/Stripe/Vercel/Notion/GOV.UK/Basecamp" — un producto existente, no un adjetivo. |
| Color de marca | Uno. Si no hay marca, un neutro + un acento, nada más. |
| Tipografía | Una familia (dos como máximo: una para títulos). |

Nada de preguntar esto al usuario si puede inferirse del proyecto, del rubro o del pedido. Se decide con criterio, se declara en una línea y se sigue.

## El sistema (tokens primero, componentes después)

Define los tokens como variables (CSS custom properties, tema del framework, `tailwind.config`, recursos XAML/QML) **antes** del primer componente. Ningún valor mágico suelto en el código.

### Tipografía
- Escala modular corta: 12 / 14 / 16 / 20 / 24 / 32 / 40 (o equivalente). Nada fuera de la escala.
- Cuerpo 16 px en web y móvil (14 en paneles densos). Interlineado 1.5 en cuerpo, 1.1–1.25 en títulos.
- Jerarquía con **peso y tamaño**, no con color ni con MAYÚSCULAS por todos lados. Dos pesos bastan (400 y 600).
- Largo de línea de texto corrido: 60–75 caracteres (`max-width: 65ch`).
- Números en tablas y métricas con cifras tabulares (`font-variant-numeric: tabular-nums`).
- Fuentes buenas sin pagar: Inter, Geist, IBM Plex Sans, Source Sans 3, Manrope, Public Sans; o la del sistema (`system-ui`), que casi siempre es la opción correcta en apps de escritorio.

### Espaciado y layout
- Escala de 4 px: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64. Cualquier otro número es un error.
- **La proximidad agrupa**: el espacio dentro de un grupo es menor que el espacio entre grupos. Si todo tiene el mismo gap, nada se lee como grupo.
- Alinea a una grilla y a bordes compartidos. Alineación a la izquierda por defecto; centrar solo bloques cortos (un título de hero, un estado vacío).
- Ancho de contenido acotado (1120–1280 px) en web; nada de texto a todo el ancho de un monitor de 27".

### Color
- Neutros hacen el 90 % del trabajo: fondo, superficie, borde, texto primario, texto secundario. Grises con un leve matiz del color de marca, no gris puro.
- Un acento para acciones primarias y estado activo. Un color por estado semántico (éxito, aviso, error, info) usado solo para eso.
- Contraste AA mínimo (4.5:1 texto, 3:1 elementos de UI). Verificarlo, no suponerlo.
- Modo oscuro: tokens propios (no invertir colores). Superficies en gris muy oscuro, no `#000`; texto en gris claro, no `#fff` puro.

### Forma y profundidad
- Un radio para todo el proyecto (4, 6 u 8 px) y uno mayor solo para contenedores grandes. Nada de mezclar 8, 12, 16 y 24.
- Separa con **borde de 1 px o cambio sutil de fondo** antes que con sombra. Sombras solo en capas flotantes (menús, diálogos, popovers), cortas y suaves.
- Sin glassmorphism, sin neón, sin gradientes de fondo salvo que la marca los tenga.

### Movimiento
- Transiciones de 120–200 ms en hover, foco y apertura. Nada que rebote ni que demore la tarea. Respetar `prefers-reduced-motion`.

## Señales de "vibecodeado" — revisa y elimina

| Señal | Qué hacer en su lugar |
|---|---|
| Emojis como iconos, en títulos, botones o toasts | Set de iconos SVG único, o sin icono |
| Degradado violeta/azul/rosa de fondo o en texto | Fondo neutro; el acento de marca solo en acciones |
| "Bienvenido a X" con un cohete al lado, "Potencia tu negocio", "Unlock the power of" | Copy concreto: qué hace, para quién, con un dato real |
| Tres tarjetas de features idénticas con icono en círculo de color | Contenido real con jerarquía; captura del producto; lista simple |
| Todo centrado | Izquierda por defecto, con una grilla |
| Sombras grandes + esquinas de 16–24 px en todo | Borde de 1 px, radio chico y consistente |
| Cinco tamaños de texto parecidos y todos en negrita | Escala corta, dos pesos |
| Botones primarios por todas partes | Un primario por vista; el resto secundario o de texto |
| Lorem ipsum, "John Doe", métricas inventadas (+300 %) | Datos plausibles del dominio del usuario, en su idioma |
| Colores de Tailwind por defecto sin criterio (`indigo-500` en todo) | Paleta propia definida en tokens |
| Iconos de tres librerías distintas | Un set, un grosor |
| Pantalla vacía sin estado vacío diseñado | Estado vacío con explicación y la acción siguiente |
| Tablas convertidas en tarjetas en escritorio | Tabla real con columnas alineadas (números a la derecha) |

## Componentes: las piezas que delatan el oficio

- **Botones**: alturas de la escala (32/36/40), padding horizontal ≥ 2× el vertical, estados hover/active/focus/disabled/loading. El foco se ve siempre.
- **Formularios**: etiqueta encima del campo, ayuda debajo, error en rojo semántico con el texto de cómo arreglarlo. Campos del mismo ancho cuando están en columna.
- **Tablas**: encabezado sticky, texto a la izquierda, números a la derecha y tabulares, filas de 40–48 px, acciones al final de la fila, paginación u orden visibles.
- **Navegación**: donde estoy siempre visible (ítem activo), no más de 7 ítems principales.
- **Diálogos**: título que dice la acción, botón primario con el verbo ("Eliminar cliente", no "OK"), acción destructiva en rojo y separada.
- **Copy**: verbos concretos, frases cortas, sin signos de exclamación, sin jerga de marketing. En el idioma del usuario final, con sus convenciones (moneda, fechas, separador decimal).

## Proceso de verificación (obligatorio)

1. Renderiza la pantalla real (navegador, app corriendo, emulador). No se juzga diseño leyendo código.
2. Captura en **375 px** y en **1280–1440 px** (o la ventana típica de la app de escritorio).
3. Mira la captura con ojo crítico y recorre la tabla de señales. Escribe lo que está mal.
4. Corrige y vuelve a capturar. Mínimo una iteración de crítica antes de entregar; lo normal son dos.
5. Prueba de entrecerrar los ojos: a la distancia, ¿se distingue qué es lo más importante de la pantalla? Si todo pesa igual, falta jerarquía.

Si no hay forma de renderizar en el entorno, se dice explícitamente en la entrega ("no verificado visualmente") y se deja el comando para verlo.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Primero que funcione, el diseño después" | El "después" nunca llega y el cliente juzga por lo que ve el primer día. Con tokens desde el inicio cuesta lo mismo. |
| "Los emojis le dan personalidad" | Le dan cara de plantilla. La personalidad sale del copy, la tipografía y el color de marca. |
| "Es un panel interno, da igual" | Lo usan ocho horas al día. La densidad y la claridad ahí valen más que en la landing. |
| "Así viene el componente de la librería" | Los componentes por defecto se ajustan a los tokens del proyecto, no al revés. |
| "No soy diseñador" | No hace falta: hace falta un sistema chico y respetarlo. Las reglas de arriba son ese sistema. |

## Formato de salida

- Dirección elegida en 3–5 líneas (tipo, tono, referencia, color, tipografía).
- Tokens definidos (archivo y ubicación).
- Capturas móvil y escritorio, o la declaración de que no se pudo verificar visualmente.
- Lista de señales de la tabla revisadas y corregidas.
