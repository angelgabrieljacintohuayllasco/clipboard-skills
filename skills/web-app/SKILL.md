---
name: web-app
description: "Build or extend a website or web app: landing, dashboard, SaaS, e-commerce, admin panel, WordPress, React/Next/Vue/Astro/HTML. \"hazme una web\". States, a11y, responsive, SEO, perf. Use with ui-design."
---

# Web-App — lo que separa una web entregable de una demo bonita

## Overview

Una web "terminada" en una demo suele carecer de la mitad de lo que hace que sirva en la realidad: estados vacíos, errores de red, teclado, móvil real, mensajes de validación, carga lenta, y lo que pasa cuando el usuario hace doble clic. Esta skill es la lista de lo que un profesional entrega y un generador rápido olvida.

## Cuándo usar

- Construir o ampliar cualquier interfaz web, con o sin framework.
- Sitios de cliente, paneles internos, tiendas, formularios, CMS.
- Revisar si una web está lista para usuarios reales.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Algo se ve mal o no responde al clic | `ui-bug` |
| Solo la API/servicio detrás | `api-backend` |
| Lento y ya medido | `performance` |
| Pedido grande o de cliente sin spec | `intake` |
| Solo el aspecto visual (se ve genérico, rediseño) | `ui-design` |

## Diseño visual

Toda pantalla nueva o rediseñada aplica `ui-design` antes de darse por terminada: tokens de tipografía, espaciado y color definidos primero, cero emojis, un solo set de iconos SVG, y verificación con capturas en móvil y escritorio. Una interfaz que funciona pero parece plantilla generada por IA no está lista.

## Regla de hierro: no existe "listo" sin los cuatro estados

```
CADA PANTALLA QUE PIDE DATOS TIENE: CARGANDO, VACIO, ERROR Y EXITO. LAS CUATRO, IMPLEMENTADAS.
```

El camino feliz es el 20% del trabajo. Lo que define la calidad percibida es qué pasa cuando no hay datos, cuando la red falla o cuando el usuario escribe cualquier cosa.

## Checklist de entrega

### Estructura y contenido
- HTML semántico: encabezados en orden, listas, `button` para acciones y `a` para navegar (esto sostiene accesibilidad y SEO a la vez).
- Idioma declarado, títulos únicos por página, descripción, favicon, imagen social.
- Metadatos y datos estructurados si el contenido es público e indexable.
- Página 404 y página de error que no dejan al usuario en blanco.

### Formularios (donde se pierden los usuarios)
- Etiquetas asociadas a cada campo; nada de solo marcador de posición.
- Validación en el cliente **y** en el servidor. La del cliente es cortesía; la del servidor es la real.
- Mensajes de error junto al campo, en lenguaje humano, diciendo cómo arreglarlo.
- Estado de envío deshabilitado para evitar doble envío; idempotencia en el servidor.
- No perder lo escrito ante un error. Autocompletado y tipos de teclado correctos en móvil.

### Accesibilidad (mínimo exigible)
- Todo lo que se puede hacer con el ratón se puede hacer con el teclado, y el foco se ve.
- Contraste suficiente; no comunicar solo con color.
- Imágenes con texto alternativo útil (o vacío si son decorativas).
- Diálogos que atrapan el foco y se cierran con Escape; se anuncia lo que cambia dinámicamente.
- Se respeta la preferencia de movimiento reducido.
- Prueba concreta: recorrer la pantalla completa solo con Tab y Enter. Si no se puede completar la tarea, no está lista.

### Responsivo de verdad
- Probado en ancho de móvil real, no solo achicando la ventana.
- Sin desplazamiento horizontal; áreas táctiles cómodas; nada oculto bajo la barra del navegador.
- Imágenes con tamaño reservado para evitar saltos de maquetación.

### Estado y datos
- Un origen de verdad por dato; nada de tres copias sincronizadas a mano.
- Errores de red visibles y recuperables (reintentar sin recargar todo).
- Peticiones canceladas o ignoradas si el usuario navega (evita respuestas fuera de orden).
- Paginar desde el inicio: las listas siempre crecen más de lo previsto.

### Seguridad del lado web
- Ninguna clave secreta en el navegador: todo lo que llega al cliente es público.
- Escapar contenido generado por usuarios; sanitizar cualquier HTML insertado.
- Protección contra falsificación de peticiones en formularios con sesión.
- Autorización verificada en el servidor por recurso; esconder un botón no protege nada.
- Cabeceras de seguridad y política de contenido; cookies con `HttpOnly`, `Secure`, `SameSite`.

### Rendimiento
- Presupuesto declarado: contenido principal visible en menos de ~2,5 s en móvil de gama media con red real.
- Imágenes en formato moderno y del tamaño que se muestra; carga diferida fuera de pantalla.
- Solo el JavaScript necesario; dividir por ruta; evitar dependencias enormes para tareas chicas.
- Fuentes con estrategia de carga que no bloquee el texto.

### CMS / sitios de cliente
- Quien edita debe poder hacerlo sin romper el diseño: campos acotados, no HTML libre.
- Actualizaciones de plataforma y extensiones planificadas; copias de seguridad antes de tocar.
- Caché: entender qué capa cachea qué antes de jurar que "el cambio no se aplicó".
- Entregar con: accesos, respaldo, cómo publicar cambios y a quién llamar. Un sitio entregado sin eso vuelve como soporte gratis eterno.

## Gate específico de web

Suma a la constitución del proyecto:

| Chequeo | Herramienta típica |
|---|---|
| Accesibilidad automática | analizador de accesibilidad (axe/lighthouse) en las pantallas clave |
| Rendimiento y buenas prácticas | auditoría automatizada con presupuesto |
| E2E de los caminos críticos | navegador automatizado (Playwright/Cypress) |
| Tamaño del paquete | límite por ruta, con trinquete |
| Enlaces rotos y consola limpia | verificación en las pantallas principales |

Nota: la accesibilidad automática detecta cerca de un tercio de los problemas reales. El recorrido con teclado es obligatorio igual.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Se ve bien en mi pantalla" | La mayoría del tráfico es móvil y de gama media. Prueba ahí. |
| "La accesibilidad la vemos después" | Se rehace la mitad de los componentes. Sale casi gratis mientras se construye. |
| "Validación en el cliente, es más rápido" | El servidor es el único que no controla el usuario. Las dos, siempre. |
| "El estado vacío no importa, siempre habrá datos" | El primer día de cualquier usuario nuevo es un estado vacío. |
| "La clave de la API la pongo en el front por ahora" | "Por ahora" es para siempre, y ya es pública. |
| "Con el framework ya es rápido" | Los frameworks agregan peso; el presupuesto se mide, no se supone. |

## Formato de salida

- Pantallas entregadas con sus cuatro estados verificados.
- Resultado del recorrido con teclado y de la auditoría automática.
- Medición de rendimiento contra el presupuesto.
- Verificación en móvil real (o emulado declarándolo).
- Pendientes de accesibilidad/SEO/rendimiento con prioridad.
