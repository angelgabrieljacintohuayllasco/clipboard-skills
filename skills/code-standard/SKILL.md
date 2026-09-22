---
name: code-standard
description: "How to write code well: naming, function size, nesting, duplication, comments, error handling, no emojis in code. \"este código está feo\", \"buenas prácticas\", \"clean code\". Applies to all code you write."
---

# Code-Standard — cómo se escribe el código que nadie va a leer entero

## Overview

En 2026 el código tiene dos lectores: la persona que lo mantendrá dentro de seis meses, y el agente que lo cargará en contexto mañana. Los dos pagan lo mismo por el desorden — la persona en tiempo, el agente en tokens y en errores de comprensión. Código claro no es estética: es la variable que decide cuánto cuesta cada cambio futuro.

Esta skill es el estándar de escritura. Los umbrales medibles viven en `constitution`; aquí está el criterio que ninguna herramienta puede medir.

## Cuándo usar

- Mientras se escribe cualquier código (es el estándar por defecto, no una ceremonia aparte).
- Al juzgar código generado (propio, de otro agente, heredado).
- Cuando algo "se siente enredado" y hay que nombrar por qué.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Mover módulos, partir monolitos | `refactor` |
| Medir y bloquear | `quality-gate` |
| Priorizar y pagar deuda acumulada | `tech-debt` |

## Regla de hierro: optimiza para el lector, no para el que escribe

```
SI ENTENDER UNA FUNCION EXIGE SALTAR A OTRO ARCHIVO, LA FUNCION ESTA MAL ESCRITA.
```

Una unidad de código debe poder leerse de arriba a abajo y entenderse sin abrir nada más. El nivel de detalle dentro de una función debe ser uniforme: no mezclar reglas de negocio con manipulación de strings ni con manejo de conexión.

## Los ocho ejes

### 1. Nombres
- El nombre dice **qué es o qué hace**, no cómo está implementado. `usuariosActivos`, no `arr2`.
- Booleanos afirman: `estaPago`, `tienePermiso`. Funciones empiezan con verbo: `calcularTotal`.
- Sin abreviaturas creativas ni prefijos de tipo. Sin `data`, `info`, `manager`, `helper`, `util` como nombre único: no dicen nada.
- El largo del nombre acompaña al alcance: `i` en un bucle de 3 líneas está bien; `i` como campo de clase, no.
- **Si cuesta nombrarlo, la unidad hace demasiadas cosas.** El problema no es el nombre.

### 2. Funciones
- Un nivel de abstracción por función; una razón para existir.
- Cláusulas de guarda al principio en vez de anidar: validar y salir temprano.
- Máximo ~50 líneas y ~4 parámetros (ver constitución). Muchos parámetros → hay un objeto esperando nacer.
- Sin banderas booleanas que parten el cuerpo en dos comportamientos: son dos funciones.
- Separa **decidir** de **hacer**: la lógica pura se prueba en milisegundos; los efectos (red, disco, reloj, aleatorio) viven en el borde.

### 3. Estado
- Preferir datos inmutables y funciones puras donde se pueda.
- Estado global mutable = la fuente número uno de bugs imposibles de reproducir.
- El alcance más chico posible; nada "por si lo necesito afuera".
- Nada de tiempo real ni aleatoriedad dentro de la lógica de negocio: se inyectan.

### 4. Errores
- Fallar temprano y ruidoso en lo que es un fallo de programación; degradar con elegancia en lo que es una condición esperada del mundo (red caída, archivo ausente).
- **Prohibido el `catch` vacío** y el `catch` que solo imprime. O se maneja, o se enriquece y se re-lanza.
- El mensaje de error dice qué se intentaba, con qué dato y qué hacer. `Error: falló` es un insulto al que debuggea a las 3 AM.
- Nunca filtrar secretos, tokens ni datos personales en mensajes o logs.
- El caso de error se prueba igual que el caso feliz (OWASP 2025 añadió el mal manejo de condiciones excepcionales a su top 10 por algo).

### 5. Dependencias
- Cada dependencia es deuda permanente: superficie de ataque, actualizaciones, ruptura futura.
- Antes de instalar: ¿lo resuelve la librería estándar en 20 líneas? ¿está mantenida? ¿cuánto pesa? ¿cuántas dependencias arrastra?
- Aísla lo externo detrás de tu propia interfaz cuando sea un servicio crítico; así cambiarlo es un archivo, no una cirugía.
- Las dependencias apuntan hacia adentro: el dominio no conoce el framework, la base de datos ni la interfaz.

### 6. Comentarios
- El código dice **qué**; el comentario dice **por qué**. Comentario que parafrasea la línea siguiente es ruido que se desactualiza.
- Vale comentar: decisiones no obvias, trampas de una librería, motivos de negocio raros, enlaces a la incidencia o al ADR.
- Código comentado = borrarlo. Para eso existe el control de versiones.
- `TODO` sin dueño ni fecha es basura. Formato: `TODO(2026-09-30): quitar el fallback cuando migre el proveedor — ADR-004`.

### 7. Estructura
- Organiza por **capacidad de negocio** (pedidos, facturación, usuarios), no por tipo técnico (controllers, services, models). Lo que cambia junto vive junto.
- Público lo mínimo; privado por defecto.
- Un archivo = un tema. Cuando un archivo necesita índice mental, ya se partió solo.

### 8. Sin emojis ni adornos
- Cero emojis en código, comentarios, logs, mensajes de error, salidas de CLI, commits, README y documentación. Tampoco en la UI (ver `ui-design`). Para estados en texto: palabras (`OK`, `FALLA`, `AVISO`), no símbolos decorativos.
- Nada de banners ASCII, separadores `=====` gigantes ni mayúsculas gritonas en logs. Un log profesional es aburrido y parseable.
- Excepción única: el usuario lo pide explícitamente.

## KISS, YAGNI y DRY con criterio operativo

| Principio | Cómo se aplica de verdad | Cómo se abusa |
|---|---|---|
| **KISS** | Elige la solución que puedas explicar completa en dos frases. Entre dos diseños que funcionan, gana el que tiene menos piezas móviles. | Confundir simple con corto. Una línea ilegible no es simple. |
| **YAGNI** | No construyas para requisitos imaginarios. Sin caso real presente, no hay abstracción, ni configuración, ni "capa por si acaso". | Usarlo de excusa para no manejar errores o no validar entradas: eso no es futuro, es hoy. |
| **DRY** | Regla de tres: a la tercera repetición **del mismo conocimiento**, extrae. | Unificar cosas que solo se parecen. Duplicación accidental unificada = acoplamiento que después hay que romper con dolor. Antes de extraer pregunta: ¿estas dos copias van a cambiar siempre juntas? |

Frase de calibración: **duplicación barata es mejor que abstracción equivocada.**

## Catálogo de olores (síntoma → umbral → acción)

| Olor | Señal medible | Qué hacer |
|---|---|---|
| Función larga | > 50 LOC | Extraer pasos con nombre |
| Clase/archivo dios | > 400 LOC, todo lo importa | Partir por capacidad |
| Lista larga de parámetros | > 4 | Objeto de parámetros o partir la función |
| Anidamiento profundo | > 3 niveles | Guardas tempranas, extraer |
| Condicional repetida sobre tipo | mismo `switch` en 3 lugares | Polimorfismo o tabla de despacho |
| Envidia de datos | usa más datos de otro objeto que propios | Mover el método a donde viven los datos |
| Obsesión por primitivos | strings/ints con reglas por todos lados | Tipo propio (Email, Dinero, Id) |
| Código muerto | sin referencias, banderas apagadas | Borrar. El historial lo guarda. |
| Bandera booleana en firma | `hacer(x, true)` | Dos funciones con nombre |
| Cadena de mensajes | `a.b().c().d()` | Ley de Demeter: pedir lo que necesitas |
| Comentario explicativo largo | 10 líneas explicando un bloque | El bloque quiere ser una función con ese nombre |
| Try/catch gigante | un bloque envolviendo todo | Acotar al punto que puede fallar |
| Números y textos mágicos | `if (estado === 3)` | Constantes o enums con nombre |
| Configuración regada | claves leídas en 12 archivos | Un módulo de configuración validado al arrancar |

## Escribir para que la IA también lo entienda

- Módulos chicos y con nombre honesto = el agente carga solo lo que necesita y acierta más.
- Tipos explícitos en los bordes: firman el contrato sin obligar a leer implementaciones.
- Un patrón por problema en todo el repo: dos estilos de acceso a datos conviviendo duplican los errores de cualquier lector, humano o no.
- Los ejemplos y tests son documentación ejecutable: un test bien nombrado enseña el uso mejor que un README.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Funciona, es lo que importa" | Funciona hoy. La pregunta real es cuánto cuesta el próximo cambio, y ese costo lo fija la claridad. |
| "Después lo limpio" | El "después" compite con la siguiente urgencia y pierde siempre. Se limpia antes del commit o no se limpia. |
| "La IA lo entiende igual" | La IA lo entiende peor: infiere lo que falta y su error sale plausible. El desorden se paga en alucinaciones y en tokens. |
| "Es mi estilo" | El estilo del repo gana al estilo personal. Consistencia > preferencia. |
| "Agrego una capa por si cambia el proveedor" | ¿Ya cambió alguna vez? Abstraer sin segundo caso real es adivinar, y se adivina mal. |
| "Lo dejo genérico, total no molesta" | Molesta: cada lector futuro paga entender una generalidad que nunca se usó. |

## Formato de salida

Cuando se usa para juzgar código: lista de olores encontrados con archivo:línea, principio violado y la corrección concreta — ordenados por costo de mantenimiento, no por gusto. Distingue siempre **defecto** (rompe algo) de **olor** (encarece el futuro); no los mezcles en la misma lista.
