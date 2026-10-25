---
title: "Especificación de Mensajes de Tunnel"
description: "Especificación para el formato de los mensajes de tunnel en I2P"
slug: "tunnel-message"
aliases:
  - "/es/docs/legacy/tunnel-message"
  - "/es/docs/legacy/tunnel-message/"
  - "/es/tunnel_message_spec"
  - "/es/tunnel_message_spec/"
category: "Diseño"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Resumen

Este documento especifica el formato de los mensajes de tunnel. Para información general sobre tunnels, consulte la [documentación de tunnels](/docs/specs/tunnel-implementation).

## Preprocesamiento de Mensajes

Un *tunnel gateway* es la entrada, o primer salto, de un tunnel. Para un tunnel de salida, el gateway es el creador del tunnel. Para un tunnel de entrada, el gateway está en el extremo opuesto al creador del tunnel.

Una puerta de enlace *preprocesa* mensajes [I2NP](/docs/specs/i2np) fragmentándolos y combinándolos en mensajes de tunnel.

Mientras que los mensajes I2NP tienen tamaño variable desde 0 hasta casi 64 KB, los mensajes de tunnel tienen tamaño fijo, aproximadamente 1 KB. El tamaño fijo de los mensajes restringe varios tipos de ataques que son posibles al observar el tamaño de los mensajes.

Después de que se crean los mensajes del tunnel, se encriptan como se describe en la [documentación del tunnel](/docs/specs/tunnel-implementation).

### Mensaje de Tunnel (Cifrado)

Estos son los contenidos de un mensaje de datos de tunnel después del cifrado.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID del Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. El ID del siguiente salto, distinto de cero.

**IV** :: : 16 bytes. El vector de inicialización.

**Datos Cifrados** :: : 1008 bytes. El mensaje de túnel cifrado.

**Tamaño total: 1028 bytes**

### Mensaje de Tunnel (Descifrado)

Estos son los contenidos de un mensaje de datos de tunnel cuando se descifra.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID del Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. El ID del siguiente salto, distinto de cero.

**IV** :: : 16 bytes. El vector de inicialización.

**Checksum** :: : 4 bytes. Los primeros 4 bytes del hash SHA256 de (el contenido del mensaje (después del byte cero) + IV).

**Relleno no nulo** :: : 0 o más bytes. Datos aleatorios no nulos para relleno.

**Cero** :: : 1 byte. El valor 0x00.

**Instrucciones de Entrega** :: TunnelMessageDeliveryInstructions : La longitud varía pero típicamente es de 7, 39, 43, o 47 bytes. Indica el fragmento y el enrutamiento para el fragmento.

**Fragmento de Mensaje** :: : 1 a 996 bytes, el máximo real depende del tamaño de la instrucción de entrega. Un mensaje I2NP parcial o completo.

**Tamaño total: 1028 bytes**

#### Notas

- El relleno, si existe, debe estar antes de los pares instrucción/mensaje. No hay provisión para relleno al final.
- La suma de verificación NO cubre el relleno o el byte cero. Toma el mensaje comenzando en las primeras instrucciones de entrega, concatena el IV, y toma el Hash de eso.

## Instrucciones de Entrega de Mensajes de Tunnel

Las instrucciones están codificadas con un solo byte de control, seguido de cualquier información adicional necesaria. El primer bit (MSB) en ese byte de control determina cómo se interpreta el resto del encabezado: si no está establecido, el mensaje no está fragmentado o este es el primer fragmento del mensaje. Si está establecido, este es un fragmento de continuación.

Esta especificación es solo para Instrucciones de Entrega dentro de Mensajes de Tunnel. Ten en cuenta que las "Instrucciones de Entrega" también se usan dentro de Garlic Cloves, donde el formato es significativamente diferente. Consulta la [documentación I2NP](/docs/specs/i2np#garlicclovedeliveryinstructions) para más detalles. ¡NO uses la siguiente especificación para las Instrucciones de Entrega de Garlic Clove!

### Instrucciones de entrega del primer fragmento

Si el MSB del primer byte es 0, este es un fragmento inicial de mensaje I2NP, o un mensaje I2NP completo (sin fragmentar), y las instrucciones son:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 byte. Orden de bits: 76543210   - bit 7: 0 para especificar un fragmento inicial o un mensaje no fragmentado   - bits 6-5: tipo de entrega

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: ¿retraso incluido? No implementado, siempre 0. Si es 1, se incluye un byte de retraso.
  - bit 3: ¿fragmentado? Si es 0, el mensaje no está fragmentado, lo que sigue es el mensaje completo. Si es 1, el mensaje está fragmentado, y las instrucciones contienen un ID de Mensaje.
  - bit 2: ¿opciones extendidas? No implementado, siempre 0. Si es 1, se incluyen opciones extendidas.
  - bits 1-0: reservados, establecidos en 0 para compatibilidad con usos futuros

**ID de Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. Opcional, presente si el tipo de entrega es TUNNEL. El ID del tunnel de destino, distinto de cero.

**To Hash** :: : 32 bytes. Opcional, presente si el tipo de entrega es ROUTER o TUNNEL. Si es ROUTER, el Hash SHA256 del router. Si es TUNNEL, el Hash SHA256 del router de puerta de enlace.

**Delay** :: : 1 byte. Opcional, presente si está establecida la bandera de retraso incluido. En mensajes de tunnel: No implementado, nunca presente; especificación original: bit 7: tipo (0 = estricto, 1 = aleatorio), bits 6-0: exponente de retraso (2^valor minutos).

**Message ID** :: : 4 bytes. Opcional, presente si este mensaje es el primero de 2 o más fragmentos (es decir, si el bit fragmentado es 1). Un ID que identifica de forma única todos los fragmentos como pertenecientes a un solo mensaje (la implementación actual usa I2NPMessageHeader.msg_id).

**Opciones Extendidas** :: : 2 o más bytes. Opcional, presente si se establece la bandera de opciones extendidas. No implementado, nunca presente; especificación original: Un byte de longitud y luego esa cantidad de bytes.

**size** :: : 2 bytes. La longitud del fragmento que sigue. Valores válidos: 1 a aproximadamente 960 en un mensaje de tunnel.

**Longitud total:** La longitud típica es: - 3 bytes para entrega LOCAL (mensaje de tunnel) - 35 bytes para entrega ROUTER o 39 bytes para entrega TUNNEL (mensaje de tunnel no fragmentado) - 39 bytes para entrega ROUTER o 43 bytes para entrega TUNNEL (primer fragmento)

### Instrucciones de Entrega de Fragmentos de Seguimiento

Si el MSB del primer byte es 1, este es un fragmento de continuación, y las instrucciones son:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte. Orden de bits: 76543210. Binario 1nnnnnnd:   - bit 7: 1 para indicar que este es un fragmento de continuación   - bits 6-1: nnnnnn es el número de fragmento de 6 bits del 1 al 63   - bit 0: d es 1 para indicar el último fragmento, 0 en caso contrario

**Message ID** :: : 4 bytes. Identifica la secuencia de fragmentos a la que pertenece este fragmento. Esto coincidirá con el message ID de un fragmento inicial (un fragmento con el bit de bandera 7 establecido en 0 y el bit de bandera 3 establecido en 1).

**size** :: : 2 bytes. La longitud del fragmento que sigue. Valores válidos: 1 a 996.

**Longitud total: 7 bytes**

## Notas

### Tamaño Máximo del Mensaje I2NP

Aunque el tamaño máximo de mensaje I2NP es nominalmente de 64 KB, el tamaño está aún más restringido por el método de fragmentar mensajes I2NP en múltiples mensajes de tunnel de 1 KB. El número máximo de fragmentos es 64, y el fragmento inicial puede no estar perfectamente alineado al inicio de un mensaje de tunnel. Por lo tanto, el mensaje debe caber nominalmente en 63 fragmentos.

El tamaño máximo de un fragmento inicial es de 956 bytes (asumiendo el modo de entrega TUNNEL); el tamaño máximo de un fragmento de continuación es de 996 bytes. Por lo tanto, el tamaño máximo es aproximadamente 956 + (62 * 996) = 62708 bytes, o 61.2 KB.

### Ordenamiento, Agrupamiento, Empaquetado

Los mensajes de tunnel pueden ser descartados o reordenados. El gateway del tunnel, quien crea los mensajes de tunnel, tiene libertad para implementar cualquier estrategia de agrupación, mezcla o reordenamiento para fragmentar mensajes I2NP y empaquetar eficientemente los fragmentos en mensajes de tunnel. En general, un empaquetado óptimo no es posible (el "problema de empaquetado"). Los gateways pueden implementar varias estrategias de retraso y reordenamiento.

### Tráfico de Cobertura

Los mensajes de tunnel pueden contener solo relleno (es decir, sin instrucciones de entrega o fragmentos de mensaje en absoluto) para tráfico de cobertura. Esto no está implementado.

## Referencias

- **[I2NP]** [Protocolo I2NP](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Implementación de Tunnel](/docs/specs/tunnel-implementation)
