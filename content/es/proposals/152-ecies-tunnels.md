---
title: "Túneles ECIES"
aliases:
  - "/es/proposals/152-ecies-config"
  - "/es/proposals/152-ecies-config/"
  - "/es/proposals/152"
  - "/es/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Nota

Despliegue de red y pruebas en progreso. Sujeto a revisiones menores. Ver [SPEC](/docs/specs/tunnel-implementation/) para la especificación oficial.

## Descripción general

Este documento propone cambios al cifrado de mensajes Tunnel Build utilizando primitivas criptográficas introducidas por [ECIES-X25519](/docs/specs/ecies/). Es una parte de la propuesta general [Proposal 156](/proposals/156-ecies-routers) para convertir los routers de claves ElGamal a ECIES-X25519.

Para los propósitos de transicionar la red de ElGamal + AES256 a ECIES + ChaCha20, son necesarios túneles con routers ElGamal y ECIES mixtos. Se proporcionan especificaciones para manejar saltos de túnel mixtos. No se realizarán cambios al formato, procesamiento o cifrado de los saltos ElGamal.

Los creadores de túneles ElGamal necesitarán crear pares de claves X25519 efímeros por salto, y seguir esta especificación para crear túneles que contengan saltos ECIES.

Esta propuesta especifica los cambios necesarios para la construcción de túneles ECIES-X25519. Para una descripción general de todos los cambios requeridos para routers ECIES, consulte la propuesta 156 [Proposal 156](/proposals/156-ecies-routers).

Esta propuesta mantiene el mismo tamaño para los registros de construcción de tunnel, según se requiere para compatibilidad. Registros de construcción y mensajes más pequeños se implementarán más adelante - ver [Propuesta 157](/proposals/157-new-tbm).

### Cryptographic Primitives

No se introducen nuevas primitivas criptográficas. Las primitivas requeridas para implementar esta propuesta son:

- AES-256-CBC como en [Cryptography](/docs/specs/cryptography/)
- Funciones STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) y DECRYPT(k, n, ciphertext, ad) - como en [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) y [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funciones X25519 DH - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)

Otras funciones Noise definidas en otra parte:

- MixHash(d) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)

### Goals

- Aumentar la velocidad de las operaciones criptográficas
- Reemplazar ElGamal + AES256/CBC con primitivas ECIES para los BuildRequestRecords y BuildReplyRecords del túnel.
- Sin cambios en el tamaño de los BuildRequestRecords y BuildReplyRecords cifrados (528 bytes) para compatibilidad
- Sin nuevos mensajes I2NP
- Mantener el tamaño del registro de construcción cifrado para compatibilidad
- Agregar forward secrecy para los Tunnel Build Messages.
- Agregar cifrado autenticado
- Detectar saltos que reordenen BuildRequestRecords
- Aumentar la resolución de la marca de tiempo para que el tamaño del filtro Bloom pueda reducirse
- Agregar campo para expiración de túnel para que sean posibles tiempos de vida variables de túnel (solo túneles completamente ECIES)
- Agregar campo de opciones extensible para características futuras
- Reutilizar primitivas criptográficas existentes
- Mejorar la seguridad de los mensajes de construcción de túnel donde sea posible manteniendo compatibilidad
- Soportar túneles con peers mixtos ElGamal/ECIES
- Mejorar las defensas contra ataques de "tagging" en mensajes de construcción
- Los saltos no necesitan conocer el tipo de cifrado del siguiente salto antes de procesar el mensaje de construcción,
  ya que pueden no tener el RI del siguiente salto en ese momento
- Maximizar compatibilidad con la red actual
- Sin cambios en el cifrado AES de solicitud/respuesta de construcción de túnel para routers ElGamal
- Sin cambios en el cifrado de "capa" AES del túnel, para eso ver [Propuesta 153](/proposals/153-chacha20-layer-encryption)
- Continuar soportando tanto TBM/TBRM de 8 registros como VTBM/VTBRM de tamaño variable
- No requerir actualización de "día bandera" para toda la red

### Primitivas Criptográficas

- Rediseño completo de los mensajes de construcción de tunnel que requiere un "flag day".
- Reducción de los mensajes de construcción de tunnel (requiere todos los saltos ECIES y una nueva propuesta)
- Uso de opciones de construcción de tunnel según se define en [Proposal 143](/proposals/143-build-message-options), solo requerido para mensajes pequeños
- Tunnels bidireccionales - para eso ver [Proposal 119](/proposals/119-bidirectional-tunnels)
- Mensajes de construcción de tunnel más pequeños - para eso ver [Proposal 157](/proposals/157-new-tbm)

## Threat Model

### Objetivos

- Ningún salto puede determinar el originador del túnel.

- Los saltos intermedios no deben poder determinar la dirección del tunnel
  o su posición en el tunnel.

- Ningún salto puede leer contenidos de otros registros de solicitud o respuesta, excepto
  por el hash de router truncado y la clave efímera para el siguiente salto

- Ningún miembro del túnel de respuesta para construcción saliente puede leer ningún registro de respuesta.

- Ningún miembro del túnel de salida para construcción de entrada puede leer ningún registro de solicitud,
  excepto que OBEP puede ver el hash de router truncado y la clave efímera para IBGW

### No-Objetivos

Un objetivo principal del diseño de construcción de túneles es hacer más difícil que los routers coludidos X e Y sepan que están en un mismo túnel. Si el router X está en el salto m y el router Y está en el salto m+1, obviamente lo sabrán. Pero si el router X está en el salto m y el router Y está en el salto m+n para n>1, esto debería ser mucho más difícil.

Los ataques de etiquetado son donde el router X de salto intermedio altera el mensaje de construcción del túnel de tal manera que el router Y puede detectar la alteración cuando el mensaje de construcción llega allí. El objetivo es que cualquier mensaje alterado sea descartado por un router entre X e Y antes de que llegue al router Y. Para las modificaciones que no son descartadas antes del router Y, el creador del túnel debería detectar la corrupción en la respuesta y descartar el túnel.

Posibles ataques:

- Alterar un registro de construcción
- Reemplazar un registro de construcción
- Agregar o eliminar un registro de construcción
- Reordenar los registros de construcción

TODO: ¿El diseño actual previene todos estos ataques?

## Design

### Noise Protocol Framework

Esta propuesta proporciona los requisitos basados en el Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisión 34, 2018-07-11). En la terminología de Noise, Alice es el iniciador y Bob es el respondedor.

Esta propuesta está basada en el protocolo Noise Noise_N_25519_ChaChaPoly_SHA256. Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Handshake Unidireccional: N
  Alice no transmite su clave estática a Bob (N)

- DH Function: X25519
  X25519 DH con una longitud de clave de 32 bytes según se especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Función de Cifrado: ChaChaPoly
  AEAD_CHACHA20_POLY1305 como se especifica en [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8.
  Nonce de 12 bytes, con los primeros 4 bytes establecidos en cero.
  Idéntico al de [NTCP2](/docs/specs/ntcp2/).

- Función Hash: SHA256
  Hash estándar de 32 bytes, ya utilizado extensamente en I2P.

#### Additions to the Framework

Ninguno.

### Objetivos de Diseño

Los handshakes utilizan patrones de handshake [Noise](https://noiseprotocol.org/noise.html).

Se utiliza la siguiente asignación de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje

La solicitud de construcción es idéntica al patrón Noise N. Esto también es idéntico al primer mensaje (Solicitud de Sesión) en el patrón XK utilizado en [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Ataques de Etiquetado

Los registros de solicitud de construcción son creados por el creador del tunnel y cifrados asimétricamente para el salto individual. Este cifrado asimétrico de los registros de solicitud actualmente es ElGamal como se define en [Criptografía](/docs/specs/cryptography/) y contiene una suma de verificación SHA-256. Este diseño no es forward-secret.

El nuevo diseño utilizará el patrón Noise unidireccional "N" con ECIES-X25519 ephemeral-static DH, con un HKDF, y ChaCha20/Poly1305 AEAD para forward secrecy, integridad y autenticación. Alice es el solicitante de construcción del tunnel. Cada salto en el tunnel es un Bob.

(Propiedades de Seguridad de Payload)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Reply encryption

Los registros de respuesta de construcción son creados por el creador de los saltos y cifrados simétricamente al creador. Este cifrado simétrico de los registros de respuesta es actualmente AES con una suma de verificación SHA-256 antepuesta. y contiene una suma de verificación SHA-256. Este diseño no es forward-secret.

El nuevo diseño utilizará ChaCha20/Poly1305 AEAD para integridad y autenticación.

### Marco de Protocolo Noise

La clave pública efímera en la solicitud no necesita ser ofuscada con AES o Elligator2. El salto anterior es el único que puede verla, y ese salto sabe que el siguiente salto es ECIES.

Los registros de respuesta no necesitan cifrado asimétrico completo con otro DH.

## Specification

### Build Request Records

Los BuildRequestRecords cifrados son de 528 bytes tanto para ElGamal como para ECIES, por compatibilidad.

#### Request Record Unencrypted (ElGamal)

Para referencia, esta es la especificación actual del tunnel BuildRequestRecord para routers ElGamal, tomada de [I2NP](/docs/specs/i2np/). Los datos sin cifrar se anteponen con un byte distinto de cero y el hash SHA-256 de los datos antes del cifrado, como se define en [Cryptography](/docs/specs/cryptography/).

Todos los campos están en big-endian.

Tamaño sin cifrar: 222 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

Para referencia, esta es la especificación actual del BuildRequestRecord del túnel para routers ElGamal, tomada de [I2NP](/docs/specs/i2np/).

Tamaño cifrado: 528 bytes

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

Esta es la especificación propuesta del BuildRequestRecord de túnel para routers ECIES-X25519. Resumen de cambios:

- Eliminar hash de router de 32 bytes no utilizado
- Cambiar tiempo de solicitud de horas a minutos
- Agregar campo de expiración para tiempo de túnel variable futuro
- Agregar más espacio para banderas
- Agregar mapeo para opciones de construcción adicionales
- La clave de respuesta AES-256 y el IV no se utilizan para el registro de respuesta del propio salto
- El registro no cifrado es más largo porque hay menos sobrecarga de cifrado

El registro de solicitud no contiene ninguna clave de respuesta ChaCha. Esas claves se derivan de una KDF. Ver más abajo.

Todos los campos están en big-endian.

Tamaño sin cifrar: 464 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
El campo flags es el mismo que se define en [Tunnel Creation](/docs/specs/tunnel-implementation/) y contiene lo siguiente::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Orden de bits: 76543210 (el bit 7 es MSB)  bit 7: si está establecido, permitir mensajes de cualquiera  bit 6: si está establecido, permitir mensajes a cualquiera, y enviar la respuesta al

bits 5-0: Sin definir, debe establecerse en 0 para compatibilidad con opciones futuras

El bit 7 indica que el salto será un gateway de entrada (IBGW). El bit 6 indica que el salto será un endpoint de salida (OBEP). Si ningún bit está establecido, el salto será un participante intermedio. Ambos no pueden estar establecidos al mismo tiempo.

#### Request Record Encrypted (ECIES)

La expiración de la solicitud es para duración variable futura de tunnel. Por ahora, el único valor soportado es 600 (10 minutos).

Las opciones de construcción del tunnel es una estructura Mapping tal como se define en [Estructuras Comunes](/docs/specs/common-structures/). Esto es para uso futuro. Actualmente no se han definido opciones. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es de 296 bytes, y el valor máximo del campo de longitud del Mapping es 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Patrones de Handshake

Todos los campos son big-endian excepto la clave pública efímera que es little-endian.

#### Reply Record Unencrypted (ElGamal)

Tamaño cifrado: 528 bytes

Los BuildReplyRecords encriptados son de 528 bytes tanto para ElGamal como para ECIES, por compatibilidad.

Las respuestas ElGamal están cifradas con AES.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

Todos los campos están en big-endian.

- Agregar mapeo para opciones de respuesta de construcción
- El registro sin cifrar es más largo porque hay menos sobrecarga de cifrado

Tamaño sin cifrar: 528 bytes

Esta es la especificación propuesta del BuildReplyRecord de túnel para routers ECIES-X25519. Resumen de cambios:

Las respuestas ECIES están cifradas con ChaCha20/Poly1305.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Todos los campos están en big-endian.

Tamaño sin cifrar: 512 bytes

- 0x00 (aceptar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

Las opciones de respuesta de construcción de túnel es una estructura Mapping como se define en [Estructuras Comunes](/docs/specs/common-structures/). Esto es para uso futuro. Actualmente no se definen opciones. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es 511 bytes, y el valor máximo del campo de longitud del Mapping es 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
El byte de respuesta es uno de los siguientes valores según se define en [Tunnel Creation](/docs/specs/tunnel-implementation/) para evitar el fingerprinting:

### Cifrado de solicitudes

Tamaño cifrado: 528 bytes

Después de la transición completa a registros ECIES, las reglas de relleno por rangos son las mismas que para los registros de solicitud.

- "encryption":

- cipher ejecutado en modo de descifrado
- registros de solicitud descifrados preventivamente en preprocesamiento (ocultando registros de solicitud cifrados)

- "descifrado":

- cipher ejecutado en modo de cifrado
- registros de solicitud cifrados (revelando el siguiente registro de solicitud en texto plano) por saltos de participante

- ChaCha20 no tiene "modos", por lo que simplemente se ejecuta tres veces:

- una vez en el preprocesamiento
- una vez por el salto
- una vez en el procesamiento de respuesta final

Los túneles mixtos están permitidos, y son necesarios, para la transición de ElGamal a ECIES. Durante el período de transición, un número creciente de routers tendrán claves bajo claves ECIES.

El preprocesamiento de criptografía simétrica se ejecutará de la misma manera:

Cuando se usan túneles mixtos, los creadores de túneles necesitarán basar el cifrado simétrico del BuildRequestRecord en el tipo de cifrado del salto actual y el anterior.

Cada salto utilizará su propio tipo de cifrado para cifrar BuildReplyRecords, y los otros registros en el VariableTunnelBuildMessage (VTBM).

- Remitente (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

En la ruta de respuesta, el endpoint (remitente) necesitará deshacer el [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), usando la clave de respuesta de cada salto.

Como ejemplo aclaratorio, veamos un túnel de salida con ECIES rodeado por ElGamal:

Todos los BuildRequestRecords están en su estado cifrado (usando ElGamal o ECIES).

El cifrado AES256/CBC, cuando se utiliza, sigue siendo usado para cada registro, sin encadenamiento entre múltiples registros.

- El registro de H3 está "cifrado" usando:

- Clave de respuesta de H2 (ChaCha20)
- Clave de respuesta de H1 (AES256/CBC)

- El registro de H2 está "encriptado" usando:

- Clave de respuesta de H1 (AES256/CBC)

- El registro de H1 sale sin cifrado simétrico

Del mismo modo, ChaCha20 se utilizará para cifrar cada registro, no transmitiendo a través de todo el VTBM.

Los registros de solicitud son preprocesados por el Sender (OBGW):

- El registro de H3 es "descifrado" usando:

- Clave de respuesta de H3 (AES256/CBC)

- El registro de H2 es "descifrado" usando:

- Clave de respuesta de H3 (AES256/CBC)
- Clave de respuesta de H2 (ChaCha20-Poly1305)

- El registro de H1 se "descifra" usando:

- Clave de respuesta de H3 (AES256/CBC)
- Clave de respuesta de H2 (ChaCha20)
- Clave de respuesta de H1 (AES256/CBC)

Solo H2 verifica la bandera de cifrado de respuesta, y ve que está seguida por AES256/CBC.

- El registro de H3 está "encriptado" usando:

- Clave de respuesta de H3 (AES256/CBC)

- El registro de H2 está "encriptado" usando:

- Clave de respuesta de H3 (AES256/CBC)
- Clave de respuesta de H2 (ChaCha20-Poly1305)

- El registro de H1 está "encriptado" usando:

- Clave de respuesta de H3 (AES256/CBC)
- Clave de respuesta de H2 (ChaCha20)
- Clave de respuesta de H1 (AES256/CBC)

### Cifrado de respuesta

Después de ser procesados por cada salto, los registros se encuentran en un estado "descifrado":

El creador del tunnel, también conocido como Inbound Endpoint (IBEP), postprocesa la respuesta:

#### KDF for Initial ck and h

Estas claves se incluyen explícitamente en los ElGamal BuildRequestRecords. Para los ECIES BuildRequestRecords, se incluyen las claves de túnel y las claves de respuesta AES, pero las claves de respuesta ChaCha se derivan del intercambio DH. Consulta la [Propuesta 156](/proposals/156-ecies-routers) para detalles sobre las claves ECIES estáticas del router.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

A continuación se describe cómo derivar las claves transmitidas previamente en los registros de solicitud.

Esto es [NOISE](https://noiseprotocol.org/noise.html) estándar para el patrón "N" con un nombre de protocolo estándar.

Los creadores de tunnel ElGamal generan un par de claves X25519 efímero para cada salto ECIES en el tunnel, y usan el esquema anterior para cifrar su BuildRequestRecord. Los creadores de tunnel ElGamal usarán el esquema anterior a esta especificación para cifrar hacia saltos ElGamal.

Los creadores de túneles ECIES necesitarán encriptar a la clave pública de cada salto ElGamal usando el esquema definido en [Tunnel Creation](/docs/specs/tunnel-implementation/). Los creadores de túneles ECIES usarán el esquema anterior para encriptar a los saltos ECIES.

Esto significa que los saltos de túnel solo verán registros cifrados de su mismo tipo de cifrado.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
Para creadores de túneles ElGamal y ECIES, generarán pares de claves efímeras X25519 únicos por salto para cifrar hacia saltos ECIES.

### Justificación

**IMPORTANTE**: Las claves efímeras deben ser únicas por salto ECIES y por registro de construcción. No usar claves únicas abre un vector de ataque para que los saltos que colaboran puedan confirmar que están en el mismo túnel.

### Reply Record Encryption (ECIES)

``replyKey``, ``layerKey`` y ``layerIV`` aún deben incluirse dentro de los registros ElGamal, y pueden generarse aleatoriamente.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Registros de Solicitud de Construcción

Como se define en [Tunnel Creation](/docs/specs/tunnel-implementation/). No hay cambios en el cifrado para los saltos ElGamal.

### Security Analysis

El registro de respuesta está cifrado con ChaCha20/Poly1305.

Como se define en [Tunnel Creation](/docs/specs/tunnel-implementation/). No hay cambios en el cifrado para los saltos ElGamal.

ElGamal no proporciona secreto hacia adelante para los Mensajes de Construcción de Túnel.

AES256/CBC está en una situación ligeramente mejor, siendo vulnerable únicamente a un debilitamiento teórico de un ataque de `biclique` con texto plano conocido.

El único ataque práctico conocido contra AES256/CBC es un ataque de oráculo de relleno, cuando el IV es conocido por el atacante.

Un atacante necesitaría romper la encriptación ElGamal del siguiente salto para obtener la información de clave AES256/CBC (clave de respuesta e IV).

ElGamal es significativamente más intensivo en CPU que ECIES, lo que conduce a un potencial agotamiento de recursos.

## Modelo de Amenazas

ECIES, utilizado con nuevas claves efímeras por-BuildRequestRecord o VariableTunnelBuildMessage, proporciona confidencialidad hacia adelante.

## Implementation Notes

* Los routers más antiguos no verifican el tipo de cifrado del salto y enviarán
  registros cifrados con ElGamal. Algunos routers recientes tienen errores y enviarán
  varios tipos de registros mal formados. Los implementadores deberían detectar y
  rechazar estos registros antes de la operación DH si es posible, para reducir
  el uso de CPU.

## Issues

## Diseño

ChaCha20Poly1305 proporciona cifrado AEAD, permitiendo que el destinatario verifique la integridad del mensaje antes de intentar el descifrado.

## Referencias

* [Common](/docs/specs/common-structures/)
* [Criptografía](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Creación de tunnel](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Cifrado múltiple](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
