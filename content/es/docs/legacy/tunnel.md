---
title: "Discusión sobre Tunnel"
description: "Exploración histórica del relleno de tunnel, la fragmentación y las estrategias de construcción"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Nota:** Este archivo recopila trabajo de diseño especulativo anterior a I2P 0.9.41. Para la implementación en producción, consulte la [documentación de tunnel](/docs/specs/implementation/) (túnel de I2P).

## Alternativas de configuración

Entre las ideas consideradas para parámetros futuros de tunnel se incluyeron:

- Limitadores de frecuencia para la entrega de mensajes
- Políticas de relleno (incluida la chaff injection (inyección de tráfico señuelo))
- Controles de vida útil del Tunnel
- Estrategias de procesamiento por lotes y de colas para el envío de cargas útiles

Ninguna de estas opciones venía con la implementación heredada.

## Estrategias de relleno

Enfoques potenciales de relleno discutidos:

- Sin ningún relleno
- Relleno de longitud aleatoria
- Relleno de longitud fija
- Relleno hasta el kilobyte más cercano
- Relleno a potencias de dos (`2^n` bytes)

Las mediciones iniciales (release 0.4) condujeron al tamaño fijo actual de 1024 bytes para los mensajes de tunnel. Los mensajes garlic (técnica de agrupación de mensajes en I2P) de nivel superior pueden añadir su propio relleno.

## Fragmentación

Para evitar ataques de etiquetado basados en la longitud del mensaje, los mensajes de tunnel tienen un tamaño fijo de 1024 bytes. Las cargas útiles I2NP de mayor tamaño son fragmentadas por la puerta de enlace; el extremo reensambla los fragmentos dentro de un breve tiempo de espera. Los Routers pueden reordenar los fragmentos para maximizar la eficiencia de empaquetado antes de enviarlos.

## Alternativas adicionales

### Ajustar el procesamiento del Tunnel a mitad de flujo

Se examinaron tres posibilidades:

1. Permitir que un salto intermedio finalice un tunnel temporalmente al conceder acceso a cargas útiles descifradas.
2. Permitir que los routers participantes “remezclen” mensajes enviándolos a través de uno de sus propios tunnels salientes antes de continuar al siguiente salto.
3. Habilitar al creador del tunnel para redefinir dinámicamente el siguiente salto de un par.

### Tunnels bidireccionales

El uso de tunnels de entrada y salida separados limita la información que cualquier conjunto de pares puede observar (p. ej., una solicitud GET frente a una respuesta grande). Los tunnels bidireccionales simplifican la gestión de pares, pero exponen los patrones de tráfico completos a ambas direcciones simultáneamente. Por lo tanto, los tunnels unidireccionales siguieron siendo el diseño preferido.

### Canales de retorno y tamaños variables

Permitir tamaños variables en los mensajes de tunnel habilitaría canales encubiertos entre pares en colusión (por ejemplo, codificando datos mediante tamaños o frecuencias seleccionados). Los mensajes de tamaño fijo mitigan este riesgo a costa de una sobrecarga adicional de relleno.

## Alternativas de construcción de Tunnel

Referencia: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Método de compilación “paralelo” heredado

Antes de la versión 0.6.1.10, las solicitudes de construcción de tunnel se enviaban en paralelo a cada participante. Este método está documentado en la [antigua página de tunnel](/docs/legacy/old-implementation/).

### Construcción telescópica de una sola vez (método actual)

El enfoque moderno envía mensajes de construcción salto a salto a través del tunnel parcialmente construido. Aunque similar al telescoping de Tor (establecimiento incremental), enrutar los mensajes de construcción a través de tunnels exploratorios reduce la fuga de información.

### Construcción telescópica “interactiva”

Construir un salto a la vez, con idas y vueltas explícitas, permite a los pares contar mensajes e inferir su posición en el tunnel, por lo que este enfoque fue rechazado.

### Tunnels de gestión no exploratorios

Una propuesta consistía en mantener un conjunto separado de tunnels de gestión para el tráfico de construcción. Si bien podría ayudar a routers particionados, se consideró innecesario con una integración de red adecuada.

### Entrega exploratoria (heredada)

Antes de la 0.6.1.10, las solicitudes de tunnel individuales se cifraban con garlic encryption (técnica de cifrado de I2P que agrupa múltiples mensajes) y se entregaban a través de tunnels exploratorios, con las respuestas regresando por separado. Esta estrategia fue reemplazada por el método de telescopado de un solo intento actual.

## Puntos clave

- Los mensajes de tunnel de tamaño fijo protegen contra el marcado basado en el tamaño y los canales encubiertos, a pesar del costo adicional del relleno.
- Se exploraron estrategias alternativas de relleno, fragmentación y construcción, pero no se adoptaron al sopesarlas frente a los compromisos de anonimato.
- El diseño del tunnel sigue equilibrando la eficiencia, la observabilidad y la resistencia a los ataques de predecesor y de congestión.
