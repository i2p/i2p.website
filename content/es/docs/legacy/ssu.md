---
title: "SSU (UDP Semifiable Seguro)"
description: "Especificación original del protocolo de transporte UDP (obsoleto, reemplazado por SSU2)"
slug: "ssu"
aliases:
  - "/es/docs/transport/ssu"
  - "/es/docs/transport/ssu/"
  - "/es/docs/transports/ssu"
  - "/es/docs/transports/ssu/"
  - "/es/docs/specs/ssu-spec"
  - "/es/docs/specs/ssu-spec/"
  - "/es/udp_spec"
  - "/es/udp_spec/"
category: "Transportes"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Resumen

OBSOLETO - SSU ha sido reemplazado por SSU2. El soporte para SSU fue eliminado de i2pd en la versión 2.44.0 (API 0.9.56) noviembre 2022. El soporte para SSU fue eliminado de Java I2P en la versión 2.4.0 (API 0.9.61) diciembre 2023.

Consulta la [descripción general de SSU](/docs/transport/ssu/) para obtener más información.

## Intercambio de Claves DH {#dh}

El intercambio inicial de claves DH de 2048 bits se describe en la [página de Claves SSU](/docs/transport/ssu/#keys). Este intercambio utiliza el mismo primo compartido que se usa para el [cifrado ElGamal](/docs/specs/cryptography/#elgamal) de I2P.

## Encabezado de Mensaje {#header}

Todos los datagramas UDP comienzan con un MAC (Código de Autenticación de Mensaje) de 16 bytes y un IV (Vector de Inicialización) de 16 bytes seguido por una carga útil de tamaño variable cifrada con la clave apropiada. El MAC utilizado es HMAC-MD5, truncado a 16 bytes, mientras que la clave es una clave AES256 completa de 32 bytes. La construcción específica del MAC son los primeros 16 bytes de:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
donde '+' significa agregar y '^' significa OR exclusivo.

El IV se genera aleatoriamente para cada paquete. El encryptedPayload es la versión cifrada del mensaje que comienza con el byte de bandera (cifrar-luego-MAC). El payloadLength utilizado en el MAC es un entero sin signo de 2 bytes, big endian. Tenga en cuenta que protocolVersion es 0, por lo que el OR exclusivo es una operación sin efecto. El macKey es la clave de introducción o se construye a partir de la clave DH intercambiada (ver detalles a continuación), según se especifica para cada mensaje a continuación.

**ADVERTENCIA** - el HMAC-MD5-128 usado aquí no es estándar, consulta [detalles de HMAC](/docs/specs/cryptography/#udp) para más información.

La carga útil en sí (es decir, el mensaje que comienza con el byte de bandera) está cifrada con AES256/CBC usando el IV y la sessionKey, con la prevención de repetición abordada dentro de su cuerpo, como se explica a continuación.

El protocolVersion es un entero sin signo de 2 bytes, big endian, y actualmente está establecido en 0. Los peers que utilicen una versión de protocolo diferente no podrán comunicarse con este peer, aunque sí podrán hacerlo las versiones anteriores que no utilicen esta bandera.

Se utiliza el OR exclusivo de ((netid - 2) << 8) para identificar rápidamente conexiones entre redes diferentes. El netid es un entero sin signo de 2 bytes, big endian, y actualmente está establecido en 2. A partir de la versión 0.9.42. Consulte la propuesta 147 para más información. Como el ID de red actual es 2, esto es una operación nula para la red actual y es compatible hacia atrás. Cualquier conexión desde redes de prueba debe tener un ID diferente y fallará en el HMAC.

### Especificación HMAC

- Relleno interno: 0x36...
- Relleno externo: 0x5C...
- Clave: 32 bytes
- Función de resumen hash: MD5, 16 bytes
- Tamaño de bloque: 64 bytes
- Tamaño MAC: 16 bytes
- Implementaciones de ejemplo en C:
  - hmac.h en [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp en [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Implementación de ejemplo en Java:
  - I2PHMac.java en [I2P](https://github.com/i2p/i2p.i2p)

### Detalles de la Clave de Sesión

La clave de sesión de 32 bytes se crea de la siguiente manera:

1. Tomar la clave DH intercambiada, representada como un array de bytes
   BigInteger de longitud mínima positiva (complemento a dos big-endian)
2. Si el bit más significativo es 1 (es decir, array[0] & 0x80 != 0),
   anteponer un byte 0x00, como en la representación
   BigInteger.toByteArray() de Java
3. Si el array de bytes es mayor o igual a 32 bytes, usar los
   primeros 32 bytes (más significativos)
4. Si el array de bytes es menor a 32 bytes, agregar bytes 0x00 para
   extender a 32 bytes. *Muy improbable - Ver nota a continuación.*

### Detalles de la Clave MAC

La clave MAC de 32 bytes se crea de la siguiente manera:

1. Tomar el array de bytes de la clave DH intercambiada, con un byte 0x00 añadido al principio si es necesario, del paso 2 en los Detalles de Clave de Sesión anteriores.
2. Si ese array de bytes es mayor o igual a 64 bytes, la clave MAC son los bytes 33-64 de ese array de bytes.
3. Si ese array de bytes es menor a 64 bytes, la clave MAC es el Hash SHA-256 de ese array de bytes. *A partir de la versión 0.9.8. Ver nota a continuación.*

#### Nota importante

El código anterior a la versión 0.9.8 estaba roto y no manejaba correctamente los arrays de bytes de claves DH entre 32 y 63 bytes (pasos 3 y 4 anteriores) y la conexión fallaría. Como estos casos nunca funcionaron, fueron redefinidos como se describe arriba para la versión 0.9.8, y el caso de 0-32 bytes también fue redefinido. Dado que la clave DH intercambiada nominal es de 256 bytes, las posibilidades de que la representación mínima sea menor a 64 bytes es extremadamente pequeña.

### Formato de Cabecera

Dentro de la carga útil cifrada con AES, hay una estructura común mínima para los diversos mensajes: una bandera de un byte y una marca de tiempo de envío de cuatro bytes (segundos desde la época unix).

El formato del encabezado es:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
El byte de bandera contiene los siguientes campos de bits:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Sin rekeying y opciones extendidas, el tamaño del encabezado es de 37 bytes.

### Renovación de claves {#rekey}

Si la bandera de rekey está establecida, 64 bytes de material de claves siguen a la marca de tiempo.

Al hacer el rekeying, los primeros 32 bytes del material de claves se introducen en un SHA256 para producir la nueva clave MAC, y los siguientes 32 bytes se introducen en un SHA256 para producir la nueva clave de sesión, aunque las claves no se usan inmediatamente. El otro lado también debería responder con la bandera de rekey establecida y ese mismo material de claves. Una vez que ambos lados han enviado y recibido esos valores, las nuevas claves deberían usarse y las claves anteriores descartarse. Puede ser útil mantener las claves antiguas durante un breve tiempo, para abordar la pérdida de paquetes y el reordenamiento.

NOTA: El rekeying (regeneración de claves) no está implementado actualmente.

### Opciones Extendidas {#extend}

Si se establece la bandera de opciones extendidas, se añade un valor de tamaño de opción de un byte, seguido de esa cantidad de bytes de opciones extendidas. Las opciones extendidas siempre han sido parte de la especificación, pero no se implementaron hasta la versión 0.9.24. Cuando están presentes, el formato de opción es específico del tipo de mensaje. Consulte la documentación de mensajes a continuación sobre si se esperan opciones extendidas para el mensaje dado, y el formato especificado. Aunque los routers de Java siempre han reconocido la bandera y la longitud de las opciones, otras implementaciones no lo han hecho. Por lo tanto, no envíe opciones extendidas a routers anteriores a la versión 0.9.24.

## Relleno

Todos los mensajes contienen 0 o más bytes de relleno. Cada mensaje debe ser rellenado hasta un límite de 16 bytes, según lo requerido por la [capa de cifrado AES256](/docs/specs/cryptography/#AES).

Hasta la versión 0.9.7, los mensajes solo se rellenaban hasta el siguiente límite de 16 bytes, y los mensajes que no fueran múltiplos de 16 bytes podrían ser inválidos.

A partir de la versión 0.9.7, los mensajes pueden rellenarse a cualquier longitud siempre que se respete el MTU actual. Cualquier byte de relleno adicional de 1-15 más allá del último bloque de 16 bytes no puede ser cifrado o descifrado y será ignorado. Sin embargo, la longitud completa y todo el relleno se incluye en el cálculo del MAC.

A partir de la versión 0.9.8, los mensajes transmitidos no son necesariamente un múltiplo de 16 bytes. El mensaje SessionConfirmed es una excepción, ver más abajo.

## Claves

Las firmas en los mensajes SessionCreated y SessionConfirmed se generan usando la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) de la [RouterIdentity](/docs/specs/common-structures/#routeridentity) que se distribuye fuera de banda al publicarse en la base de datos de la red, y la [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) asociada.

Hasta la versión 0.9.15, el algoritmo de firma siempre era DSA, con una firma de 40 bytes.

A partir de la versión 0.9.16, el algoritmo de firma puede ser especificado por un [KeyCertificate](/docs/specs/common-structures/#key-certificates) en la [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Bob.

Tanto las claves de introducción como las claves de sesión son de 32 bytes, y están definidas por la especificación de Estructuras comunes [SessionKey](/docs/specs/common-structures/#sessionkey). La clave utilizada para el MAC y el cifrado se especifica para cada mensaje a continuación.

Las claves de introducción se entregan a través de un canal externo (la base de datos de red), donde tradicionalmente han sido idénticas al Hash del router hasta la versión 0.9.47, pero pueden ser aleatorias a partir de la versión 0.9.48.

## Notas

### IPv6

La especificación del protocolo permite tanto direcciones IPv4 de 4 bytes como direcciones IPv6 de 16 bytes. SSU-over-IPv6 está soportado desde la versión 0.9.8. Consulta la documentación de los mensajes individuales a continuación para detalles sobre el soporte de IPv6.

### Marcas de tiempo {#time}

Mientras que la mayoría de I2P utiliza marcas de tiempo [Date](/docs/specs/common-structures/#date) de 8 bytes con resolución de milisegundos, SSU utiliza marcas de tiempo de enteros sin signo de 4 bytes con resolución de un segundo. Debido a que estos valores son sin signo, no se reiniciarán hasta febrero de 2106.

## Mensajes

Hay 10 mensajes (tipos de carga útil) definidos:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (tipo 0) {#sessionrequest}

Este es el primer mensaje enviado para establecer una sesión.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Formato del mensaje:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 304 (IPv4) o 320 (IPv6) bytes (antes del relleno no-mod-16)

#### Opciones extendidas

Nota: Implementado en 0.9.24.

- Longitud mínima: 3 (byte de longitud de opción + 2 bytes)
- Longitud de opción: 2 mínimo
- 2 bytes de flags:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Notas

- Se admiten direcciones IPv4 e IPv6.
- Los datos no interpretados podrían usarse en el futuro para desafíos.

### SessionCreated (tipo 1) {#sessioncreated}

Esta es la respuesta a una [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Formato de mensaje:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 368 bytes (IPv4 o IPv6) (antes del relleno no-mod-16)

#### Notas

- Las direcciones IPv4 e IPv6 son compatibles.
- Si la etiqueta de retransmisión (relay tag) es distinta de cero, Bob se ofrece a actuar como introductor para
  Alice. Alice puede posteriormente publicar la dirección de Bob y la etiqueta de retransmisión en la
  base de datos de la red.
- Para la firma, Bob debe usar su puerto externo, ya que eso es lo que Alice
  usará para verificar. Si el NAT/firewall de Bob ha mapeado su puerto interno a un
  puerto externo diferente, y Bob no lo sabe, la verificación por Alice
  fallará.
- Consulta la sección [Keys](#keys) arriba para detalles sobre las firmas. Alice ya tiene
  la clave pública de firma de Bob, de la base de datos de la red.
- Hasta la versión 0.9.15, la firma siempre era una firma DSA de 40 bytes y
  el relleno siempre era de 8 bytes. Desde la versión 0.9.16, el tipo y
  longitud de la firma están implícitos por el tipo de la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) en la
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Bob. El relleno es el necesario para un múltiplo de 16 bytes.
- Este es el único mensaje que usa la clave de introducción del remitente. Todos los demás usan la
  clave de introducción del receptor o la clave de sesión establecida.
- El tiempo firmado parece no usarse o no verificarse en la
  implementación actual.
- Los datos no interpretados posiblemente podrían usarse en el futuro para desafíos.
- Opciones extendidas en el encabezado: No esperadas, indefinidas.

### SessionConfirmed (tipo 2) {#sessionconfirmed}

Esta es la respuesta a un mensaje [SessionCreated](#sessioncreated) y el último paso para establecer una sesión. Puede ser necesario enviar múltiples mensajes SessionConfirmed si la Router Identity debe ser fragmentada.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragmento 0 hasta F-2** (solo si F > 1; actualmente sin usar, ver notas a continuación):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragmento F-1 (último o único fragmento):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamaño típico incluyendo encabezado, en la implementación actual: 512 bytes (con firma Ed25519) o 480 bytes (con firma DSA-SHA1) (antes del relleno no-mod-16)

#### Notas

- En la implementación actual, el tamaño máximo de fragmento es de 512 bytes. Esto
  debería extenderse para que las firmas más largas funcionen sin fragmentación.
  La implementación actual no procesa correctamente las firmas divididas entre
  dos fragmentos.
- El [RouterIdentity](/docs/specs/common-structures/#routeridentity) típico es de 387 bytes, por lo que nunca es
  necesaria la fragmentación. Si la nueva criptografía extiende el tamaño del RouterIdentity, el
  esquema de fragmentación debe ser probado cuidadosamente.
- No existe un mecanismo para solicitar o reenviar fragmentos faltantes.
- El campo de fragmentos totales F debe establecerse de forma idéntica en todos los fragmentos.
- Ver la sección [Keys](#keys) anterior para detalles sobre las firmas DSA.
- El tiempo de firmado parece no utilizarse o no verificarse en la
  implementación actual.
- Como la firma está al final, el padding en el último o único paquete
  debe rellenar el paquete total a un múltiplo de 16 bytes, o la firma no
  se descifrará correctamente. Esto es diferente de todos los otros tipos de
  mensaje, donde el padding está al final.
- Hasta la versión 0.9.15, la firma siempre era una firma DSA de 40 bytes. A
  partir de la versión 0.9.16, el tipo y longitud de la firma están implícitos en el tipo de
  la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) en el [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Alice. El padding es según
  sea necesario a un múltiplo de 16 bytes.
- Opciones extendidas en el header: No esperadas, indefinidas.

### SessionDestroyed (tipo 8) {#sessiondestroyed}

El mensaje SessionDestroyed fue implementado (solo recepción) en la versión 0.8.1, y se envía a partir de la versión 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Este mensaje no contiene datos. Tamaño típico incluyendo encabezado, en la implementación actual: 48 bytes (antes del relleno no-mod-16)

#### Notas

- Los mensajes de destrucción recibidos con la clave de introducción del remitente o del receptor serán ignorados.
- Opciones extendidas en el encabezado: No esperadas, indefinidas.

### RelayRequest (tipo 3) {#relayrequest}

Este es el primer mensaje enviado de Alice a Bob para solicitar una presentación a Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formato de mensaje:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 96 bytes (sin IP de Alice incluida) o 112 bytes (IP de Alice de 4 bytes incluida) (antes del relleno no-mod-16)

#### Notas

- La dirección IP solo se incluye si es diferente a la dirección de origen y puerto del paquete.
- Este mensaje puede enviarse por IPv4 o IPv6.
  Si el mensaje es por IPv6 para una introducción IPv4,
  o (desde la versión 0.9.50) por IPv4 para una introducción IPv6,
  Alice debe incluir su dirección y puerto de introducción.
  Esto es compatible desde la versión 0.9.50.
- Si Alice incluye su dirección/puerto, Bob puede realizar validación adicional
  antes de continuar.
  - Antes de la versión 0.9.24, Java I2P rechazaba cualquier dirección o puerto que fuera
    diferente de la conexión.
- Challenge no está implementado, el tamaño del challenge siempre es cero
- El relaying para IPv6 es compatible desde la versión 0.9.50.
- Antes de la versión 0.9.12, siempre se usaba la clave de introducción de Bob. Desde la versión
  0.9.12, se usa la clave de sesión si hay una sesión establecida entre
  Alice y Bob. En la práctica, debe haber una sesión establecida, ya que Alice
  solo obtendrá el nonce (etiqueta de introducción) del mensaje de creación de sesión,
  y Bob marcará la etiqueta de introducción como inválida una vez que la sesión sea destruida.
- Opciones extendidas en el encabezado: No esperadas, indefinidas.

### RelayResponse (tipo 4) {#relayresponse}

Esta es la respuesta a un [RelayRequest](#relayrequest) y se envía de Bob a Alice.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formato del mensaje:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 64 (Alice IPv4) o 80 (Alice IPv6) bytes (antes del relleno no-mod-16)

#### Notas

- Este mensaje puede ser enviado vía IPv4 o IPv6.
- La dirección IP/puerto de Alice son la IP/puerto aparente que Bob recibió
  en la RelayRequest (no necesariamente la IP que Alice incluyó en la RelayRequest),
  y puede ser IPv4 o IPv6. Alice actualmente ignora estos al recibirlos.
- La dirección IP de Charlie puede ser IPv4, o, desde la versión 0.9.50, IPv6,
  ya que esa es la dirección a la que Alice
  enviará la SessionRequest después del Hole Punch.
- El relaying para IPv6 es compatible desde la versión 0.9.50.
- Antes de la versión 0.9.12, siempre se usaba la clave de introducción de Alice. Desde la versión
  0.9.12, se usa la clave de sesión si hay una sesión establecida entre
  Alice y Bob.
- Opciones extendidas en el encabezado: No se esperan, indefinidas.

### RelayIntro (tipo 5) {#relayintro}

Esta es la introducción para Alice, que es enviada de Bob a Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Formato del mensaje:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 48 bytes (antes del relleno no-mod-16)

#### Notas

- Para IPv4, la dirección IP de Alice siempre tiene 4 bytes, porque Alice está intentando conectarse a Charlie a través de IPv4.
  A partir de la versión 0.9.50, se admite IPv6, y la dirección IP de Alice puede tener 16 bytes.
- Para IPv4, este mensaje debe enviarse a través de una conexión IPv4 establecida,
  ya que esa es la única manera en que Bob conoce la dirección IPv4 de Charlie para devolverla a Alice en el RelayResponse.
  A partir de la versión 0.9.50, se admite IPv6, y este mensaje puede enviarse a través de una conexión IPv6 establecida.
- A partir de la versión 0.9.50, cualquier dirección SSU publicada con introducers debe contener "4" o "6" en la opción "caps".
- Challenge no está implementado, el tamaño del challenge siempre es cero
- Opciones extendidas en el encabezado: No esperadas, indefinidas.

### Datos (tipo 6) {#data}

Este mensaje se utiliza para el transporte de datos y el reconocimiento.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Datos:** 1 byte de flags (ver abajo); si se incluyen ACKs explícitos: 1 byte con el número de ACKs, esa cantidad de MessageIds de 4 bytes siendo completamente confirmados con ACK; si se incluyen campos de bits ACK: 1 byte con el número de campos de bits ACK, esa cantidad de MessageIds de 4 bytes + 1 o más bytes de campo de bits ACK (ver notas); Si se incluyen datos extendidos: 1 byte de tamaño de datos, esa cantidad de bytes de datos extendidos (actualmente no interpretados); 1 byte con el número de fragmentos (puede ser cero); Si es distinto de cero, esa cantidad de fragmentos de mensaje.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Cada fragmento contiene: - messageId de 4 bytes - información del fragmento de 3 bytes:   - bits 23-17: fragmento # 0 - 127   - bit 16: isLast (1 = verdadero)   - bits 15-14: sin usar, establecidos en 0 para compatibilidad con usos futuros   - bits 13-0: tamaño del fragmento 0 - 16383 - esa cantidad de bytes de datos del fragmento

Formato de mensaje:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Notas sobre el Campo de Bits ACK

El bitfield utiliza los 7 bits bajos de cada byte, con el bit alto especificando si le sigue un byte de bitfield adicional (1 = verdadero, 0 = el byte de bitfield actual es el último). Esta secuencia de arrays de 7 bits representa si un fragmento ha sido recibido - si un bit es 1, el fragmento ha sido recibido. Para aclarar, asumiendo que los fragmentos 0, 2, 5, y 9 han sido recibidos, los bytes del bitfield serían los siguientes:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Notas

- La implementación actual añade un número limitado de acks duplicados para
  mensajes previamente confirmados, si hay espacio disponible.
- Si el número de fragmentos es cero, este es un mensaje de solo ack o keepalive.
- La característica ECN no está implementada, y el bit nunca se establece.
- En la implementación actual, el bit want reply se establece cuando el número de
  fragmentos es mayor que cero, y no se establece cuando no hay fragmentos.
- Los datos extendidos no están implementados y nunca están presentes.
- La recepción de múltiples fragmentos es compatible en todas las versiones. La transmisión de
  múltiples fragmentos está implementada en la versión 0.9.16.
- Tal como está implementado actualmente, el máximo de fragmentos es 64 (número máximo de fragmento = 63).
- Tal como está implementado actualmente, el tamaño máximo de fragmento es por supuesto menor que el MTU.
- Ten cuidado de no exceder el MTU máximo incluso si hay un gran número de
  ACKs para enviar.
- El protocolo permite fragmentos de longitud cero pero no hay razón para enviarlos.
- En SSU, los datos usan un header I2NP corto de 5 bytes seguido por la carga útil del
  mensaje I2NP en lugar del header I2NP estándar de 16 bytes. El header I2NP corto
  consiste solo en el tipo I2NP de un byte y la expiración de 4 bytes en
  segundos. El ID del mensaje I2NP se usa como el ID del mensaje para el fragmento. El
  tamaño I2NP se ensambla a partir de los tamaños de los fragmentos. El checksum I2NP no es
  requerido ya que la integridad del mensaje UDP está asegurada por el descifrado.
- Los IDs de mensaje no son números de secuencia y no son consecutivos. SSU no
  garantiza la entrega en orden. Aunque usamos el ID del mensaje I2NP como el
  ID del mensaje SSU, desde la perspectiva del protocolo SSU, son números aleatorios. De hecho,
  dado que el router usa un único filtro Bloom para todos los peers, el ID del mensaje
  debe ser un número realmente aleatorio.
- Debido a que no hay números de secuencia, no hay manera de estar seguro de que un ACK fue
  recibido. La implementación actual rutinariamente envía una gran cantidad de
  ACKs duplicados. Los ACKs duplicados no deben tomarse como una indicación de
  congestión.
- Notas del campo de bits ACK: El receptor de un paquete de datos no sabe cuántos
  fragmentos hay en el mensaje a menos que haya recibido el último fragmento.
  Por lo tanto, el número de bytes del campo de bits enviados en respuesta puede ser menor o mayor
  que el número de fragmentos dividido por 7. Por ejemplo, si el fragmento más alto
  que el receptor ha visto es el número 4, solo se requiere enviar un byte, incluso si puede haber 13 fragmentos en total. Hasta 10 bytes (es decir, (64 / 7)
  + 1) pueden incluirse para cada ID de mensaje confirmado.
- Opciones extendidas en el header: No esperadas, indefinidas.

### PeerTest (tipo 7) {#peertest}

Ver [Pruebas de Pares SSU](/docs/transport/ssu/#peerTesting) para más detalles. Nota: Las pruebas de pares IPv6 son compatibles desde la versión 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Clave criptográfica utilizada (listada en orden de ocurrencia): 1. Cuando se envía de Alice a Bob: sessionKey de Alice/Bob 2. Cuando se envía de Bob a Charlie: sessionKey de Bob/Charlie 3. Cuando se envía de Charlie a Bob: sessionKey de Bob/Charlie 4. Cuando se envía de Bob a Alice: sessionKey de Alice/Bob (o para Bob anterior a 0.9.52, introKey de Alice) 5. Cuando se envía de Charlie a Alice: introKey de Alice, como se recibió en el mensaje PeerTest de Bob 6. Cuando se envía de Alice a Charlie: introKey de Charlie, como se recibió en el mensaje PeerTest de Charlie

Clave MAC utilizada (listada en orden de ocurrencia): 1. Cuando se envía de Alice a Bob: Clave MAC de Alice/Bob 2. Cuando se envía de Bob a Charlie: Clave MAC de Bob/Charlie 3. Cuando se envía de Charlie a Bob: Clave MAC de Bob/Charlie 4. Cuando se envía de Bob a Alice: introKey de Alice, como se recibió en el mensaje PeerTest de Alice 5. Cuando se envía de Charlie a Alice: introKey de Alice, como se recibió en el mensaje PeerTest de Bob 6. Cuando se envía de Alice a Charlie: introKey de Charlie, como se recibió en el mensaje PeerTest de Charlie

Formato del mensaje:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Tamaño típico incluyendo encabezado, en la implementación actual: 80 bytes (antes del relleno no-mod-16)

#### Notas

- Cuando es enviado por Alice, el tamaño de la dirección IP es 0, la dirección IP no está presente, y el puerto es 0, ya que Bob y Charlie no usan los datos; el objetivo es determinar la verdadera dirección IP/puerto de Alice y decírselo a Alice; a Bob y Charlie no les importa qué dirección piensa Alice que tiene.
- Cuando es enviado por Bob o Charlie, la IP y el puerto están presentes, y la dirección IP es de 4 o 16 bytes. Las pruebas IPv6 están soportadas desde la versión 0.9.27.
- Cuando es enviado por Charlie a Alice, la IP y el puerto son como sigue:
  Primera vez (mensaje 5): La IP y puerto solicitados por Alice como se recibieron en el mensaje 2.
  Segunda vez (mensaje 7): La IP y puerto reales de Alice desde donde se recibió el mensaje 6.
- Notas sobre IPv6: Hasta la versión 0.9.26, solo se soporta la prueba de direcciones IPv4. Por lo tanto, toda la comunicación Alice-Bob y Alice-Charlie debe ser vía IPv4. La comunicación Bob-Charlie, sin embargo, puede ser vía IPv4 o IPv6. La dirección de Alice, cuando se especifica en el mensaje PeerTest, debe ser de 4 bytes.
  Desde la versión 0.9.27, las pruebas de direcciones IPv6 están soportadas, y la comunicación Alice-Bob y Alice-Charlie puede ser vía IPv6, si Bob y Charlie indican soporte con una capacidad 'B' en su dirección IPv6 publicada.
  Ver Propuesta 126 para detalles.
- Alice envía la solicitud a Bob usando una sesión existente sobre el transporte (IPv4 o IPv6) que desea probar.
  Cuando Bob recibe una solicitud de Alice vía IPv4, Bob debe seleccionar un Charlie que anuncie una dirección IPv4.
  Cuando Bob recibe una solicitud de Alice vía IPv6, Bob debe seleccionar un Charlie que anuncie una dirección IPv6.
  La comunicación real Bob-Charlie puede ser vía IPv4 o IPv6 (es decir, independiente del tipo de dirección de Alice).
- Un peer debe mantener una tabla de estados de prueba activos (nonces). Al recibir un mensaje PeerTest, buscar el nonce en la tabla. Si se encuentra, es una prueba existente y conoces tu rol (Alice, Bob, o Charlie). De lo contrario, si la IP no está presente y el puerto es 0, esta es una nueva prueba y tú eres Bob.
  De lo contrario, esta es una nueva prueba y tú eres Charlie.
- Desde la versión 0.9.15, Alice debe tener una sesión establecida con Bob y usar la clave de sesión.
- Antes de la versión API 0.9.52, en algunas implementaciones, Bob respondía a Alice usando la clave intro de Alice en lugar de la clave de sesión Alice/Bob, aunque Alice y Bob tuvieran una sesión establecida (desde 0.9.15).
  Desde la versión API 0.9.52, Bob usará correctamente la clave de sesión en todas las implementaciones, y Alice debería rechazar un mensaje recibido de Bob con la clave intro de Alice si Bob es versión API 0.9.52 o superior.
- Opciones extendidas en el encabezado: No se esperan, indefinidas.

### HolePunch {#holepunch}

Un HolePunch es simplemente un paquete UDP sin datos. No está autenticado ni cifrado. No contiene un encabezado SSU, por lo que no tiene un número de tipo de mensaje. Se envía de Charlie a Alice como parte de la secuencia de Introduction.

## Datagramas de Ejemplo {#sampledatagrams}

### Mensaje de datos mínimo

- sin fragmentos, sin ACKs, sin NACKs, etc
- Tamaño: 39 bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Mensaje de datos mínimo con carga útil

- Tamaño: 46+fragmentSize bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Referencias

- [Cifrado AES](/docs/specs/cryptography/#AES)
- [Especificación de Estructuras Comunes](/docs/specs/common-structures/)
- [Fecha](/docs/specs/common-structures/#date)
- [Cifrado ElGamal](/docs/specs/cryptography/#elgamal)
- [Detalles HMAC](/docs/specs/cryptography/#udp)
- [Código Fuente I2P](https://github.com/i2p/i2p.i2p)
- [Código Fuente i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Resumen SSU](/docs/transport/ssu/)
- [Claves SSU](/docs/transport/ssu/#keys)
- [Pruebas de Pares SSU](/docs/transport/ssu/#peerTesting)
