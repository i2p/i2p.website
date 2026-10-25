---
title: "Especificación I2NP"
description: "Formatos de mensajes del Protocolo de Red I2P (I2NP), prioridades y estructuras comunes para la comunicación entre routers."
slug: "i2np"
aliases:
  - "/es/spec/i2np"
  - "/es/spec/i2np/"
category: "Protocolos"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Descripción general

El I2P Network Protocol (I2NP) es la capa por encima de los protocolos de transporte de I2P. Es un protocolo router-a-router. Se utiliza para búsquedas y respuestas de la base de datos de red, para crear tunnels, y para mensajes de datos cifrados de router y cliente. Los mensajes I2NP pueden enviarse punto a punto a otro router, o enviarse de forma anónima a través de tunnels hacia ese router.

## Versiones del Protocolo {#versions}

Todos los routers deben publicar su versión del protocolo I2NP en el campo "router.version" en las propiedades del RouterInfo. Este campo de versión es la versión de la API, indicando el nivel de soporte para varias características del protocolo I2NP, y no es necesariamente la versión real del router.

Si los routers alternativos (no-Java) desean publicar información de versión sobre la implementación real del router, deben hacerlo en otra propiedad. Se permiten versiones distintas a las listadas a continuación. El soporte se determinará mediante una comparación numérica; por ejemplo, 0.9.13 implica soporte para las características de 0.9.12. Nótese que la propiedad "coreVersion" ya no se publica en la información del router, y nunca se utilizó para determinar la versión del protocolo I2NP.

Un resumen básico de las versiones del protocolo I2NP es el siguiente. Para más detalles, ver abajo.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Ten en cuenta que también existen características relacionadas con el transporte y problemas de compatibilidad; consulta la documentación de los transportes NTCP y SSU para más detalles.

## Estructuras Comunes {#structures}

Las siguientes estructuras son elementos de múltiples mensajes I2NP. No son mensajes completos.

### Cabecera de Mensaje I2NP {#struct-I2NPMessageHeader}

#### Descripción

Cabecera común a todos los mensajes I2NP, que contiene información importante como una suma de verificación, fecha de expiración, etc.

#### Contenidos

Se utilizan tres formatos separados, dependiendo del contexto; un formato estándar y dos formatos cortos.

El formato estándar de 16 bytes contiene 1 byte [Integer](/docs/specs/common-structures/#integer) especificando el tipo de este mensaje, seguido por un [Integer](/docs/specs/common-structures/#integer) de 4 bytes especificando el message-id. Después de eso hay una [Date](/docs/specs/common-structures/#date) de expiración, seguida por un [Integer](/docs/specs/common-structures/#integer) de 2 bytes especificando la longitud de la carga útil del mensaje, seguido por un [Hash](/docs/specs/common-structures/#hash), que se trunca al primer byte. Después de eso siguen los datos reales del mensaje.

Los formatos cortos utilizan una expiración de 4 bytes en segundos en lugar de una expiración de 8 bytes en milisegundos. Los formatos cortos no contienen un checksum o tamaño, estos son proporcionados por las encapsulaciones, dependiendo del contexto.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Notas

- Cuando se transmite por [SSU](/docs/transports/ssu/), no se utiliza la cabecera estándar de 16 bytes. Solo se incluye un tipo de 1 byte y una expiración de 4 bytes en segundos. El id del mensaje y el tamaño se incorporan en el formato del paquete de datos SSU. La suma de verificación no es requerida ya que los errores se detectan en el descifrado.

- Cuando se transmite a través de [NTCP2](/docs/specs/ntcp2/) o [SSU2](/docs/specs/ssu2/), no se utiliza el encabezado estándar de 16 bytes. Solo se incluye un tipo de 1 byte, un ID de mensaje de 4 bytes y una expiración de 4 bytes en segundos. El tamaño se incorpora en los formatos de paquete de datos de NTCP2 y SSU2. La suma de verificación no es necesaria ya que los errores se detectan en el descifrado.

- El encabezado estándar también se requiere para los mensajes I2NP contenidos en otros mensajes y estructuras (Data, TunnelData, TunnelGateway y GarlicClove). A partir de la versión 0.8.12, para reducir la sobrecarga, la verificación de checksum está deshabilitada en algunos puntos de la pila de protocolos. Sin embargo, para compatibilidad con versiones anteriores, la generación de checksum sigue siendo requerida. Es un tema de investigación futura determinar puntos en la pila de protocolos donde se conoce la versión del router del extremo lejano y se puede deshabilitar la generación de checksum.

- La expiración corta no está firmada y se reiniciará el 7 de febrero de 2106. A partir de esa fecha, se debe agregar un desplazamiento para obtener la hora correcta.

- Las implementaciones pueden rechazar mensajes con expiraciones demasiado lejanas en el futuro. La expiración máxima recomendada es de 60s en el futuro.

### BuildRequestRecord {#struct-BuildRequestRecord}

OBSOLETO, solo se usa en la red actual cuando un tunnel contiene un router ElGamal. Ver [Creación de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Descripción

Un Record en un conjunto de múltiples records para solicitar la creación de un salto en el tunnel. Para más detalles consulta la [descripción general de tunnels](/docs/specs/tunnel-implementation/) y la [especificación de creación de tunnel ElGamal](/docs/specs/tunnel-creation/).

Para BuildRequestRecords ECIES-X25519, consulta [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

#### Contenidos (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) para recibir mensajes, seguido por el [Hash](/docs/specs/common-structures/#hash) de nuestro [RouterIdentity](/docs/specs/common-structures/#routeridentity). Después siguen el [TunnelId](/docs/specs/common-structures/#tunnelid) y el [Hash](/docs/specs/common-structures/#hash) del [RouterIdentity](/docs/specs/common-structures/#routeridentity) del siguiente router.

Cifrado con ElGamal y AES:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
Cifrado ElGamal:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Texto plano:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Notas

- En el registro cifrado de 512 bytes, los datos ElGamal contienen los bytes 1-256 y 258-513 del bloque cifrado ElGamal de 514 bytes [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Se eliminan los dos bytes de relleno del bloque (los bytes cero en las ubicaciones 0 y 257).

- Consulta la [especificación de creación de tunnel](/docs/specs/tunnel-creation/) para detalles sobre el contenido de los campos.

### BuildResponseRecord {#struct-BuildResponseRecord}

OBSOLETO, solo se usa en la red actual cuando un túnel contiene un router ElGamal. Ver [Creación de Túnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Descripción

Un Record en un conjunto de múltiples records con respuestas a una solicitud de construcción. Para más detalles consulta la [descripción general de tunnels](/docs/specs/tunnel-implementation/) y la [especificación de creación de tunnels ElGamal](/docs/specs/tunnel-creation/).

Para BuildResponseRecords ECIES-X25519, consulta [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

#### Contenidos (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Notas

- El campo de datos aleatorios podría, en el futuro, utilizarse para devolver información de congestión o conectividad de peers al solicitante.

- Consulta la [especificación de creación de túneles](/docs/specs/tunnel-creation/) para obtener detalles sobre el campo de respuesta.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Solo para routers ECIES-X25519, a partir de la versión 0.9.51 de la API. 218 bytes cuando está cifrado. Ver [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Solo para routers ECIES-X25519, a partir de la versión 0.9.51 de la API. 218 bytes cuando está cifrado. Ver [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Advertencia: Este es el formato utilizado para garlic cloves dentro de mensajes garlic encriptados con ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). El formato para mensajes garlic y garlic cloves ECIES-AEAD-X25519-Ratchet es significativamente diferente; consulta [ECIES](/docs/specs/ecies/) para la especificación.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Notas

- Los cloves nunca se fragmentan. Cuando se usa en un Garlic Clove, el primer bit del byte de bandera de Instrucciones de Entrega especifica el cifrado. Si este bit es 0, el clove no está cifrado. Si es 1, el clove está cifrado, y una Session Key de 32 bytes sigue inmediatamente al byte de bandera. El cifrado de clove no está completamente implementado.

- Ver también la [especificación de garlic routing](/docs/overview/garlic-routing/).

- La longitud máxima es una función de la longitud total de todos los cloves y la longitud máxima del GarlicMessage.

- En el futuro, el certificado podría usarse posiblemente para un HashCash para "pagar" por el enrutamiento.

- El mensaje puede ser cualquier mensaje I2NP (incluyendo un GarlicMessage, aunque eso no se usa en la práctica). Los mensajes usados en la práctica son DataMessage, DeliveryStatusMessage y DatabaseStoreMessage.

- El ID del Clove generalmente se establece a un número aleatorio al transmitir y se verifica por duplicados al recibir (mismo espacio de ID de mensaje que los Message IDs de nivel superior)

### Instrucciones de Entrega del Diente de Garlic {#struct-GarlicCloveDeliveryInstructions}

Este es el formato utilizado tanto para dientes de garlic encryption cifrados con ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) como para los cifrados con ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/).

Esta especificación es solo para las Instrucciones de Entrega dentro de Garlic Cloves. Ten en cuenta que las "Instrucciones de Entrega" también se utilizan dentro de los Mensajes de Túnel, donde el formato es significativamente diferente. Consulta la [documentación de Mensajes de Túnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) para obtener más detalles. ¡NO uses la siguiente especificación para las Instrucciones de Entrega de Mensajes de Túnel!

La clave de sesión y el retraso no se usan y nunca están presentes, por lo que las tres longitudes posibles son 1 (LOCAL), 33 (ROUTER y DESTINATION), y 37 (TUNNEL) bytes.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Mensajes

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Descripción

Un almacén de base de datos no solicitado, o la respuesta a un mensaje [DatabaseLookup](#msg-DatabaseLookup) exitoso

#### Contenidos

Un LeaseSet sin comprimir, LeaseSet2, MetaLeaseSet, o EncryptedLeaseset, o un RouterInfo comprimido

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Notas

- Por seguridad, los campos de respuesta se ignoran si el mensaje se recibe a través de un tunnel.

- La clave es el hash "real" del RouterIdentity o Destination, NO la clave de enrutamiento.

- Los tipos 3, 5 y 7 están disponibles desde la versión 0.9.38. Consulta la propuesta 123 para más información. Estos tipos solo deben enviarse a routers con la versión 0.9.38 o superior.

- Como optimización para reducir conexiones, si el tipo es un LeaseSet, se incluye el token de respuesta, el ID del túnel de respuesta es distinto de cero, y el par gateway/tunnelID de respuesta se encuentra en el LeaseSet como un lease, el destinatario puede rerutar la respuesta a cualquier otro lease en el LeaseSet.

- Para ocultar el SO del router y la implementación, coincide con la implementación del router Java de gzip estableciendo el tiempo de modificación en 0 y el byte del SO en 0xFF, y establece XFL en 0x02 (compresión máxima, algoritmo más lento). Ver RFC 1952. Los primeros 10 bytes de la información del router comprimida serán (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Descripción

Una solicitud para buscar un elemento en la base de datos de red. La respuesta es ya sea un [DatabaseStore](#msg-DatabaseStore) o un [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Contenidos

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Cifrado de Respuesta

NOTA: Los routers ElGamal están obsoletos a partir de la API 0.9.58. Como la versión mínima recomendada de floodfill para consultar es ahora la 0.9.58, las implementaciones no necesitan implementar cifrado para routers floodfill ElGamal. Los destinos ElGamal siguen siendo compatibles.

El bit de bandera 4 se usa en combinación con el bit 1 para determinar el modo de cifrado de respuesta. El bit de bandera 4 solo debe establecerse al enviar a routers con versión 0.9.46 o superior. Ver las propuestas 154 y 156 para más detalles.

En la tabla a continuación, "DH n/a" significa que la respuesta no está cifrada. "DH no" significa que las claves de respuesta están incluidas en la solicitud. "DH yes" significa que las claves de respuesta se derivan de la operación DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Sin Cifrado

reply_key, tags y reply_tags no están presentes.

#### ElG a ElG

Compatible desde la versión 0.9.7. Obsoleto desde la versión 0.9.58. El destino ElG envía una consulta a un router ElG.

Generación de clave del solicitante:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Formato del mensaje:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES a ElG

Admitido desde la versión 0.9.46. Obsoleto desde la versión 0.9.58. El destino ECIES envía una consulta a un router ElG. Los campos reply_key y reply_tags se redefinen para una respuesta cifrada con ECIES.

Generación de clave del solicitante:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Formato del mensaje: Redefinir los campos reply_key y reply_tags de la siguiente manera:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
La respuesta es un mensaje ECIES Existing Session, como se define en [ECIES](/docs/specs/ecies/).

#### Formato de respuesta

Este es el mensaje de sesión existente, igual que en [ECIES](/docs/specs/ecies/), copiado a continuación como referencia.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Parámetros AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES a ECIES (0.9.49)

El destino o router ECIES envía una consulta a un router ECIES. Soportado desde la versión 0.9.49.

Los routers ECIES fueron introducidos en la versión 0.9.48, ver [Propuesta 156](/proposals/156/). Los destinos y routers ECIES pueden usar el mismo formato que en la sección "ECIES a ElG" anterior, con las claves de respuesta incluidas en la solicitud. El cifrado del mensaje de búsqueda está especificado en [ECIES-ROUTERS](/docs/specs/ecies-routers/). El solicitante es anónimo.

#### ECIES a ECIES (futuro)

Esta opción aún no está completamente definida. Ver [Propuesta 156](/proposals/156/).

#### Notas

- Antes de la versión 0.9.16, la clave puede ser para un RouterInfo o LeaseSet, ya que están en el mismo espacio de claves, y no había ninguna bandera para solicitar solo un tipo particular de datos.

- Bandera de cifrado, clave de respuesta y etiquetas de respuesta a partir de la versión 0.9.7.

- Las respuestas cifradas solo son útiles cuando la respuesta es a través de un tunnel.

- El número de etiquetas incluidas podría ser mayor que uno si se implementan estrategias alternativas de búsqueda DHT (por ejemplo, búsquedas recursivas).

- La clave de búsqueda y las claves de exclusión son los hashes "reales", NO claves de enrutamiento.

- Los tipos 3, 5 y 7 pueden ser devueltos a partir de la versión 0.9.38. Ver la propuesta 123 para más información.

- Notas de búsqueda exploratoria: Una búsqueda exploratoria se define para devolver una lista de hashes no-floodfill cercanos a la clave. Sin embargo, consulta las notas importantes para DatabaseSearchReply sobre variantes de implementación. Además, esta especificación nunca ha aclarado si el receptor debería buscar la clave de búsqueda para un RI y devolver un DatabaseStore en lugar de un DSRM si está presente. Java sí hace la búsqueda; i2pd no. Por lo tanto, no se recomienda usar una búsqueda exploratoria para hashes recibidos previamente.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Descripción

La respuesta a un mensaje [DatabaseLookup](#msg-DatabaseLookup) fallido

#### Contenidos

Una lista de hashes de router más cercanos a la clave solicitada

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Notas

- El hash 'from' no está autenticado y no se puede confiar en él.

- Los hashes de pares devueltos no están necesariamente más cerca de la clave que el router que está siendo consultado. Para las respuestas a búsquedas regulares, esto facilita el descubrimiento de nuevos floodfills y la búsqueda "hacia atrás" (más lejos de la clave) para mayor robustez.

- La clave para una búsqueda de exploración generalmente se genera aleatoriamente. Por lo tanto, los peer_hashes no-floodfill de la respuesta pueden seleccionarse utilizando un algoritmo optimizado, como proporcionar peers que estén cerca de la clave pero no necesariamente los más cercanos en toda la base de datos de red local, para evitar una ordenación o búsqueda ineficiente de toda la base de datos local. Otras estrategias como el almacenamiento en caché también pueden ser apropiadas. Esto depende de la implementación.

- Número típico de hashes devueltos: 3

- Número máximo recomendado de hashes a devolver: 16

- La clave de búsqueda, hashes de pares y hash de origen son hashes "reales", NO claves de enrutamiento.

### DeliveryStatus {#msg-DeliveryStatus}

#### Descripción

Un reconocimiento de mensaje simple. Generalmente creado por el originador del mensaje, y envuelto en un Garlic Message con el mensaje mismo, para ser devuelto por el destino.

Este mensaje también se utiliza para la prueba de túneles, donde el originador lo envía a través de un túnel saliente, hacia un túnel entrante y de regreso a sí mismo. En esta aplicación, también suele estar envuelto con cifrado garlic. La prueba de túneles es obligatoria a partir de la versión 0.9.68 de la API (2026-02), ya que los routers pueden descartar túneles participantes que no hayan recibido tráfico alguno después de los primeros dos minutos.

#### Contenidos

El ID del mensaje entregado, y la hora de creación o llegada.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Notas

- Parece que la marca de tiempo siempre es establecida por el creador al tiempo actual. Sin embargo, hay varios usos de esto en el código, y pueden agregarse más en el futuro.

- Este mensaje también se usa como confirmación de sesión establecida en SSU [SSU-ED](/docs/transports/ssu/#establishDirect). En este caso, el ID del mensaje se establece a un número aleatorio, y el "tiempo de llegada" se establece al ID actual de toda la red, que es 2 (es decir, 0x0000000000000002).

### Garlic {#msg-Garlic}

Advertencia: Este es el formato utilizado para mensajes de ajo cifrados con ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). El formato para mensajes de ajo y clavos de ajo cifrados con ECIES-AEAD-X25519-Ratchet es significativamente diferente; véase [ECIES](/docs/specs/ecies/) para la especificación.

#### Descripción

Usado para encapsular múltiples mensajes I2NP cifrados

#### Contenidos

Cuando se descifra, una serie de [Clavos de Ajo](#struct-GarlicClove) y datos adicionales, también conocidos como Conjunto de Clavos (Clove Set).

Cifrado:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Datos desencriptados, también conocidos como Conjunto de Clavos:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Notas

- Cuando no está cifrado, los datos contienen uno o más [Garlic Cloves](#struct-GarlicClove).

- El bloque cifrado AES se rellena a un mínimo de 128 bytes; con el Session Tag de 32 bytes el tamaño mínimo del mensaje cifrado es de 160 bytes; con los 4 bytes de longitud el tamaño mínimo del Garlic Message es de 164 bytes.

- La longitud máxima real es menor a 64 KB; ver [I2NP](/docs/protocol/i2np/).

- Ver también la [especificación ElGamal/AES](/docs/specs/elgamal-aes/).

- Ver también la [especificación de enrutamiento garlic](/docs/overview/garlic-routing/).

- El tamaño mínimo de 128 bytes del bloque cifrado AES no es actualmente configurable, sin embargo el tamaño mínimo de un DataMessage en un GarlicClove en un GarlicMessage, con overhead, es de 128 bytes de todos modos. Una opción configurable para aumentar el tamaño mínimo puede ser añadida en el futuro.

- El ID del mensaje generalmente se establece en un número aleatorio al transmitir y parece ser ignorado al recibir.

- En el futuro, el certificado podría usarse posiblemente para un HashCash para "pagar" por el enrutamiento.

### TunnelData {#msg-TunnelData}

#### Descripción

Un mensaje enviado desde la puerta de enlace de un túnel o desde un participante al siguiente participante o destino. Los datos tienen longitud fija y contienen mensajes I2NP que están fragmentados, agrupados, rellenados y cifrados.

#### Contenidos

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Notas

- El ID del mensaje I2NP para este mensaje se establece a un número aleatorio nuevo en cada salto.

- Ver también la [Especificación de Mensajes de Tunnel](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Descripción

Envuelve otro mensaje I2NP para ser enviado a través de un túnel en la puerta de entrada del túnel.

#### Contenidos

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notas

- La carga útil es un mensaje I2NP con un encabezado estándar de 16 bytes.

### Datos {#msg-Data}

#### Descripción

Utilizado por los mensajes Garlic y Garlic Cloves para encapsular datos arbitrarios.

#### Contenidos

Un entero de longitud, seguido de datos opacos.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notas

- Este mensaje no contiene información de enrutamiento y nunca será enviado "sin envolver". Solo se usa dentro de mensajes `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

OBSOLETO, usar [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Notas

- A partir de la versión 0.9.48, también puede contener BuildRequestRecords ECIES-X25519, ver [Creación de túneles ECIES](/docs/specs/tunnel-creation-ecies/).

- Ver también la [especificación de creación de tunnel](/docs/specs/tunnel-creation/).

- El ID del mensaje I2NP para este mensaje debe establecerse de acuerdo con la especificación de creación de túneles.

- Aunque este mensaje rara vez se ve en la red actual, habiendo sido reemplazado por el mensaje `VariableTunnelBuild`, aún puede usarse para tunnels muy largos, y no ha sido deprecado. Los routers deben implementarlo.

### TunnelBuildReply {#msg-TunnelBuildReply}

OBSOLETO, usar [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Notas

- A partir de la versión 0.9.48, también puede contener BuildResponseRecords ECIES-X25519, consulta [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Consulta también la [especificación de creación de tunnel](/docs/specs/tunnel-creation/).

- El ID del mensaje I2NP para este mensaje debe establecerse según la especificación de creación de túneles.

- Aunque este mensaje se ve raramente en la red actual, habiendo sido reemplazado por el mensaje `VariableTunnelBuildReply`, aún puede usarse para tunnels muy largos, y no ha sido deprecado. Los routers deben implementarlo.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Notas

- A partir de 0.9.48, también puede contener BuildRequestRecords ECIES-X25519, ver [Creación de túneles ECIES](/docs/specs/tunnel-creation-ecies/).

- Este mensaje fue introducido en la versión 0.7.12 del router, y puede que no se envíe a participantes del tunnel anteriores a esa versión.

- Consulta también la [especificación de creación de túneles](/docs/specs/tunnel-creation/).

- El ID del mensaje I2NP para este mensaje debe establecerse según la especificación de creación de túnel.

- El número típico de registros en la red actual es 4, para un tamaño total de 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Notas

- A partir de la versión 0.9.48, también puede contener BuildResponseRecords ECIES-X25519, ver [Creación de túneles ECIES](/docs/specs/tunnel-creation-ecies/).

- Este mensaje fue introducido en la versión 0.7.12 del router, y puede no ser enviado a participantes del tunnel anteriores a esa versión.

- Ver también la [especificación de creación de tunnel](/docs/specs/tunnel-creation/).

- El ID de mensaje I2NP para este mensaje debe establecerse según la especificación de creación de túneles.

- El número típico de registros en la red actual es 4, para un tamaño total de 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Descripción

A partir de la versión de API 0.9.51, solo para routers ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Notas

- A partir de 0.9.51. Ver [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

- Este mensaje fue introducido en la versión 0.9.51 del router, y puede no ser enviado a participantes del tunnel con versiones anteriores a esa.

- El número típico de registros en la red actual es 4, para un tamaño total de 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Descripción

Enviado desde el punto final saliente de un túnel nuevo al originador. A partir de la versión 0.9.51 de la API, solo para routers ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Notas

- A partir de la versión 0.9.51. Ver [Creación de Túneles ECIES](/docs/specs/tunnel-creation-ecies/).

- El número típico de registros en la red actual es 4, para un tamaño total de 873.

## Referencias

- **[CRYPTO-ELG]** [Criptografía - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Estructuras Comunes - Fecha](/docs/specs/common-structures/#date)
- **[ECIES]** [Especificación ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Especificación de routers ECIES](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Enrutamiento Garlic](/docs/overview/garlic-routing/)
- **[Hash]** [Estructuras Comunes - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [Protocolo I2NP](/docs/protocol/i2np/)
- **[Integer]** [Estructuras Comunes - Entero](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Especificación NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Propuesta 156](/proposals/156/)
- **[Prop157]** [Propuesta 157](/proposals/157/)
- **[RouterIdentity]** [Estructuras Comunes - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [Transporte SSU](/docs/transports/ssu/)
- **[SSU-ED]** [Transporte SSU - Establecer Directo](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Especificación SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Instrucciones de Entrega de Mensajes de tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Especificación de Creación de tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Creación de tunnel ECIES](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Implementación de tunnel](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Especificación de Mensajes de tunnel](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Estructuras Comunes - TunnelId](/docs/specs/common-structures/#tunnelid)
