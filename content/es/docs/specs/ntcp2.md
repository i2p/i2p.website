---
title: "Transporte NTCP2"
description: "Transporte TCP basado en Noise para enlaces router a router"
slug: "ntcp2"
category: "Transportes"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Descripción general

NTCP2 es un protocolo de acuerdo de claves autenticado que mejora la resistencia de [NTCP](/docs/transport/ntcp) a varias formas de identificación automatizada y ataques.

NTCP2 está diseñado para flexibilidad y coexistencia con NTCP. Puede ser soportado en el mismo puerto que NTCP, o en un puerto diferente, o sin soporte simultáneo de NTCP en absoluto. Consulte la sección de Información del Router Publicada más abajo para obtener detalles.

Al igual que con otros transportes de I2P, NTCP2 está definido únicamente para el transporte punto a punto (router a router) de mensajes I2NP. No es una tubería de datos de propósito general.

NTCP2 es compatible desde la versión 0.9.36. Ver [Prop111](/proposals/111-ntcp-2) para la propuesta original, incluyendo discusión de antecedentes e información adicional.

## Marco de Protocolo Noise

NTCP2 utiliza el Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisión 33, 2017-10-04). Noise tiene propiedades similares al protocolo Station-To-Station [STS](#references), que es la base del protocolo [SSU](/docs/transport/ssu). En la terminología de Noise, Alice es el iniciador, y Bob es el respondedor.

NTCP2 se basa en el protocolo Noise Noise_XK_25519_ChaChaPoly_SHA256. (El identificador real para la función inicial de derivación de claves es "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" para indicar las extensiones de I2P - ver la sección KDF 1 más abajo) Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Handshake: XK Alice transmite su clave a Bob (X) Alice ya conoce la clave estática de Bob (K)
- Función DH: X25519 X25519 DH con una longitud de clave de 32 bytes según se especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Función de Cifrado: ChaChaPoly AEAD_CHACHA20_POLY1305 según se especifica en [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8. Nonce de 12 bytes, con los primeros 4 bytes establecidos en cero.
- Función Hash: SHA256 Hash estándar de 32 bytes, ya utilizado extensivamente en I2P.

## Adiciones al Framework

NTCP2 define las siguientes mejoras a Noise_XK_25519_ChaChaPoly_SHA256. Estas generalmente siguen las pautas de la sección 13 de [NOISE](https://noiseprotocol.org/noise.html).

1) Las claves efímeras en texto plano se ofuscan con cifrado AES usando una clave e IV conocidos. 2) Se añade relleno aleatorio en texto plano a los mensajes 1 y 2. El relleno en texto plano se incluye en el cálculo del hash del handshake (MixHash). Ver las secciones KDF a continuación para el mensaje 2 y la parte 1 del mensaje 3. Se añade relleno AEAD aleatorio al mensaje 3 y a los mensajes de la fase de datos. 3) Se añade un campo de longitud de trama de dos bytes, como se requiere para Noise sobre TCP, y como en obfs4. Esto se usa solo en los mensajes de la fase de datos. Las tramas AEAD de los mensajes 1 y 2 tienen longitud fija. La trama AEAD de la parte 1 del mensaje 3 tiene longitud fija. La longitud de la trama AEAD de la parte 2 del mensaje 3 se especifica en el mensaje 1. 4) El campo de longitud de trama de dos bytes se ofusca con SipHash-2-4, como en obfs4. 5) El formato de carga útil se define para los mensajes 1, 2, 3 y la fase de datos. Por supuesto, estos no están definidos en el framework.

## Mensajes

Todos los mensajes NTCP2 tienen una longitud menor o igual a 65537 bytes. El formato del mensaje está basado en mensajes Noise, con modificaciones para el enmarcado e indistinguibilidad. Las implementaciones que usen bibliotecas Noise estándar pueden necesitar preprocesar los mensajes recibidos hacia/desde el formato de mensaje Noise. Todos los campos cifrados son textos cifrados AEAD.

La secuencia de establecimiento es la siguiente:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Usando la terminología de Noise, la secuencia de establecimiento y datos es la siguiente: (Propiedades de Seguridad de Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Una vez que se ha establecido una sesión, Alice y Bob pueden intercambiar mensajes de datos.

Todos los tipos de mensaje (SessionRequest, SessionCreated, SessionConfirmed, Data y TimeSync) se especifican en esta sección.

Algunas notaciones:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Cifrado Autenticado

Hay tres instancias separadas de cifrado autenticado (CipherStates). Una durante la fase de handshake, y dos (transmisión y recepción) para la fase de datos. Cada una tiene su propia clave de una KDF.

Los datos cifrados/autenticados se representarán como

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Formato de datos cifrado y autenticado.

Entradas a las funciones de cifrado/descifrado:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Salida de la función de encriptación, entrada de la función de desencriptación:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Para ChaCha20, lo que se describe aquí corresponde a [RFC-7539](https://tools.ietf.org/html/rfc7539), que también se utiliza de manera similar en TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Notas

- Dado que ChaCha20 es un cifrado de flujo, los textos planos no necesitan ser rellenados. Los bytes adicionales del flujo de claves se descartan.
- La clave para el cifrador (256 bits) se acuerda mediante el KDF SHA256. Los detalles del KDF para cada mensaje están en secciones separadas a continuación.
- Los marcos ChaChaPoly para los mensajes 1, 2, y la primera parte del mensaje 3, son de tamaño conocido. Comenzando con la segunda parte del mensaje 3, los marcos son de tamaño variable. El tamaño de la parte 1 del mensaje 3 se especifica en el mensaje 1. Comenzando con la fase de datos, los marcos van precedidos por una longitud de dos bytes ofuscada con SipHash como en obfs4.
- El relleno está fuera del marco de datos autenticados para los mensajes 1 y 2. El relleno se usa en el KDF para el siguiente mensaje, por lo que se detectará cualquier manipulación. Comenzando en el mensaje 3, el relleno está dentro del marco de datos autenticados.

#### Manejo de Errores AEAD

- En los mensajes 1, 2, y partes 1 y 2 del mensaje 3, el tamaño del mensaje AEAD se conoce de antemano. Ante un fallo de autenticación AEAD, el destinatario debe detener el procesamiento posterior de mensajes y cerrar la conexión sin responder. Esto debe ser un cierre anormal (TCP RST).
- Para resistencia al sondeo, en el mensaje 1, después de un fallo AEAD, Bob debe establecer un tiempo de espera aleatorio (rango por determinar) y luego leer un número aleatorio de bytes (rango por determinar) antes de cerrar el socket. Bob debe mantener una lista negra de IPs con fallos repetidos.
- En la fase de datos, el tamaño del mensaje AEAD está "cifrado" (ofuscado) con SipHash. Se debe tener cuidado de evitar crear un oráculo de descifrado. Ante un fallo de autenticación AEAD en la fase de datos, el destinatario debe establecer un tiempo de espera aleatorio (rango por determinar) y luego leer un número aleatorio de bytes (rango por determinar). Después de la lectura, o al agotar el tiempo de espera de lectura, el destinatario debe enviar una carga útil con un bloque de terminación que contenga un código de razón de "fallo AEAD", y cerrar la conexión.
- Tomar la misma acción de error para un valor de campo de longitud inválido en la fase de datos.

### Función de Derivación de Claves (KDF) (para mensaje de handshake 1)

El KDF genera una clave de cifrado de fase de handshake k a partir del resultado DH, utilizando HMAC-SHA256(key, data) como se define en [RFC-2104](https://tools.ietf.org/html/rfc2104). Estas son las funciones InitializeSymmetric(), MixHash(), y MixKey(), exactamente como se definen en la especificación Noise.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice envía a Bob.

Contenido Noise: clave efímera X de Alice Carga útil Noise: bloque de opciones de 16 bytes Carga útil no-noise: Relleno aleatorio

(Propiedades de Seguridad de Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
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
El valor X se cifra para garantizar la indistinguibilidad y unicidad de la carga útil, que son contramedidas DPI necesarias. Utilizamos cifrado AES para lograr esto, en lugar de alternativas más complejas y lentas como elligator2. El cifrado asimétrico a la clave pública del router de Bob sería demasiado lento. El cifrado AES utiliza el hash del router de Bob como clave y el IV de Bob tal como se publica en la base de datos de red.

La encriptación AES es solo para resistencia a DPI. Cualquier parte que conozca el hash del router de Bob, y el IV, que se publican en la base de datos de la red, puede descifrar el valor X en este mensaje.

El relleno no es cifrado por Alice. Puede ser necesario que Bob descifre el relleno, para inhibir ataques de temporización.

Contenido sin procesar:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Bloque de opciones: Nota: Todos los campos están en big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Notas

- Cuando la dirección publicada es "NTCP", Bob soporta tanto NTCP como NTCP2 en el mismo puerto. Por compatibilidad, cuando inicia una conexión a una dirección publicada como "NTCP", Alice debe limitar el tamaño máximo de este mensaje, incluyendo el relleno, a 287 bytes o menos. Esto facilita la identificación automática del protocolo por parte de Bob. Cuando se publica como "NTCP2", no hay restricción de tamaño. Ver las secciones Direcciones Publicadas y Detección de Versión más abajo.

- El valor X único en el bloque AES inicial asegura que el texto cifrado sea diferente para cada sesión.

- Bob debe rechazar las conexiones donde el valor de la marca de tiempo esté demasiado alejado del tiempo actual. Llamemos al delta de tiempo máximo "D". Bob debe mantener una caché local de valores de handshake utilizados anteriormente y rechazar duplicados, para prevenir ataques de repetición. Los valores en la caché deben tener una vida útil de al menos 2*D. Los valores de caché dependen de la implementación, sin embargo se puede usar el valor X de 32 bytes (o su equivalente cifrado).

- Las claves efímeras Diffie-Hellman nunca deben reutilizarse para prevenir ataques criptográficos, y la reutilización será rechazada como un ataque de repetición.

- Las opciones "KE" y "auth" deben ser compatibles, es decir, el secreto compartido K debe tener el tamaño apropiado. Si se agregan más opciones "auth", esto podría cambiar implícitamente el significado de la bandera "KE" para usar un KDF diferente o un tamaño de truncamiento diferente.

- Bob debe validar que la clave efímera de Alice es un punto válido en la curva aquí.

- El relleno debe limitarse a una cantidad razonable. Bob puede rechazar conexiones con relleno excesivo. Bob especificará sus opciones de relleno en el mensaje 2. Las pautas mínimas/máximas están por determinar. ¿Tamaño aleatorio de 0 a 31 bytes como mínimo? (La distribución depende de la implementación) Las implementaciones de Java actualmente limitan el relleno a un máximo de 256 bytes.

- Ante cualquier error, incluyendo AEAD, DH, marca de tiempo, aparente repetición, o falla de validación de clave, Bob debe detener el procesamiento adicional de mensajes y cerrar la conexión sin responder. Esto debe ser un cierre anormal (TCP RST). Para resistencia al sondeo, después de una falla de AEAD, Bob debe establecer un tiempo de espera aleatorio (rango por determinar) y luego leer un número aleatorio de bytes (rango por determinar), antes de cerrar el socket.

- Bob puede hacer una verificación MSB rápida para una clave válida (X[31] & 0x80 == 0) antes de intentar el descifrado. Si el bit alto está establecido, implementar resistencia a sondeo como para fallas AEAD.

- Mitigación de DoS: DH es una operación relativamente costosa. Al igual que con el protocolo NTCP anterior, los routers deben tomar todas las medidas necesarias para prevenir el agotamiento de CPU o conexiones. Establecer límites en las conexiones activas máximas y las configuraciones de conexión máximas en progreso. Aplicar timeouts de lectura (tanto por lectura como total para "slowloris"). Limitar conexiones repetidas o simultáneas desde la misma fuente. Mantener listas negras para fuentes que fallan repetidamente. No responder a fallos de AEAD.

- Para facilitar la detección rápida de versión y el handshaking, las implementaciones deben asegurar que Alice almacene en buffer y luego envíe todo el contenido del primer mensaje de una vez, incluyendo el relleno. Esto aumenta la probabilidad de que los datos estén contenidos en un solo paquete TCP (a menos que sean segmentados por el SO o middleboxes), y sean recibidos de una vez por Bob. Además, las implementaciones deben asegurar que Bob almacene en buffer y luego envíe todo el contenido del segundo mensaje de una vez, incluyendo el relleno, y que Bob almacene en buffer y luego envíe todo el contenido del tercer mensaje de una vez. Esto también es por eficiencia y para asegurar la efectividad del relleno aleatorio.

- Campo "ver": El protocolo Noise general, extensiones y protocolo NTCP incluyendo especificaciones de carga útil, indicando NTCP2. Este campo puede usarse para indicar soporte para cambios futuros.

- Longitud de la parte 2 del mensaje 3: Este es el tamaño del segundo frame AEAD (incluyendo MAC de 16 bytes) que contiene el Router Info de Alice y relleno opcional que será enviado en el mensaje SessionConfirmed. Como los routers regeneran y republican periódicamente su Router Info, el tamaño del Router Info actual puede cambiar antes de que se envíe el mensaje 3. Las implementaciones deben elegir una de dos estrategias:

a\) guardar la información actual del Router para ser enviada en el mensaje 3, así se conoce el tamaño, y opcionalmente agregar espacio para relleno;

b\) aumentar el tamaño especificado lo suficiente para permitir un posible incremento en el tamaño del Router Info, y siempre agregar relleno cuando el mensaje 3 sea realmente enviado. En cualquier caso, la longitud "m3p2len" incluida en el mensaje 1 debe ser exactamente el tamaño de ese frame cuando se envíe en el mensaje 3.

- Bob debe fallar la conexión si queda algún dato entrante después de validar el mensaje 1 y leer el relleno. No debería haber datos adicionales de Alice, ya que Bob aún no ha respondido con el mensaje 2.

- El campo ID de red se utiliza para identificar rápidamente conexiones entre diferentes redes. Si este campo es distinto de cero y no coincide con el ID de red de Bob, Bob debe desconectarse y bloquear conexiones futuras. Cualquier conexión de redes de prueba debe tener un ID diferente y fallará la prueba. A partir de la versión 0.9.42. Ver propuesta 147 para más información.

- Hasta la API 0.9.68 (versión 2.11.0), Java I2P implementó un máximo de 256 bytes de relleno para conexiones no-PQ, sin embargo esto no estaba documentado previamente.
  A partir de la API 0.9.69 (versión 2.12.0), Java I2P implementa el mismo relleno máximo para conexiones no-PQ
  que para MLKEM-512. El relleno máximo es de 880 bytes.

### Función de Derivación de Claves (KDF) (para mensaje de handshake 2 y mensaje 3 parte 1)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob envía a Alice.

Contenido de ruido: clave efímera Y de Bob Carga útil de ruido: bloque de opción de 16 bytes Carga útil sin ruido: Relleno aleatorio

(Propiedades de Seguridad de Carga Útil de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
El valor Y se cifra para garantizar la indistinguibilidad y singularidad de la carga útil, que son contramedidas DPI necesarias. Utilizamos cifrado AES para lograr esto, en lugar de alternativas más complejas y lentas como elligator2. El cifrado asimétrico a la clave pública del router de Alice sería demasiado lento. El cifrado AES utiliza el hash del router de Bob como clave y el estado AES del mensaje 1 (que fue inicializado con el IV de Bob tal como se publicó en la base de datos de red).

El cifrado AES es solo para resistencia a DPI. Cualquier parte que conozca el hash del router de Bob y el IV, que se publican en la base de datos de red, y haya capturado los primeros 32 bytes del mensaje 1, puede descifrar el valor Y en este mensaje.

Contenido sin procesar:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Datos no cifrados (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Notas

- Alice debe validar que la clave efímera de Bob es un punto válido en la curva aquí.
- El padding debe limitarse a una cantidad razonable. Alice puede rechazar conexiones con padding excesivo. Alice especificará sus opciones de padding en el mensaje 3. Pautas mín/máx por determinar. ¿Tamaño aleatorio de 0 a 31 bytes como mínimo? (La distribución depende de la implementación)
- En caso de cualquier error, incluyendo AEAD, DH, timestamp, aparente replay, o falla de validación de clave, Alice debe detener el procesamiento de mensajes adicionales y cerrar la conexión sin responder. Esto debe ser un cierre anormal (TCP RST).
- Para facilitar el handshake rápido, las implementaciones deben asegurar que Bob almacene en buffer y luego descargue todo el contenido del primer mensaje de una vez, incluyendo el padding. Esto aumenta la probabilidad de que los datos estén contenidos en un solo paquete TCP (a menos que sean segmentados por el SO o middleboxes), y sean recibidos todos a la vez por Alice. Esto es también por eficiencia y para asegurar la efectividad del padding aleatorio.
- Alice debe fallar la conexión si quedan datos entrantes después de validar el mensaje 2 y leer el padding. No debe haber datos extra de Bob, ya que Alice aún no ha respondido con el mensaje 3.

Bloque de opciones: Nota: Todos los campos están en big-endian.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Notas

- Alice debe rechazar conexiones donde el valor de marca de tiempo esté demasiado alejado del tiempo actual. Llamemos "D" al delta de tiempo máximo. Alice debe mantener una caché local de valores de handshake previamente utilizados y rechazar duplicados, para prevenir ataques de repetición. Los valores en la caché deben tener una vida útil de al menos 2*D. Los valores de caché dependen de la implementación, sin embargo se puede usar el valor Y de 32 bytes (o su equivalente cifrado).

- Hasta la API 0.9.68 (versión 2.11.0), Java I2P implementaba un máximo de 256 bytes de relleno para conexiones no-PQ, sin embargo esto no estaba documentado previamente.
  A partir de la API 0.9.69 (versión 2.12.0), Java I2P implementa el mismo relleno máximo para conexiones no-PQ
  que para MLKEM-512. El relleno máximo es de 848 bytes.

#### Problemas

- ¿Incluir opciones de relleno mín/máx aquí?

### Cifrado para el mensaje de handshake 3 parte 1, usando KDF del mensaje 2)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Función de Derivación de Claves (KDF) (para la parte 2 del mensaje 3 del handshake)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice envía a Bob.

Contenido Noise: clave estática de Alice Carga útil Noise: RouterInfo de Alice y relleno aleatorio Carga útil no-noise: ninguna

(Propiedades de Seguridad de Carga Útil de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Esto contiene dos tramas ChaChaPoly. La primera es la clave pública estática cifrada de Alice. La segunda es la carga útil de Noise: el RouterInfo cifrado de Alice, opciones opcionales y relleno opcional. Utilizan claves diferentes, porque la función MixKey() es llamada entre ellas.

Contenidos sin procesar:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Datos sin cifrar (etiquetas de autenticación Poly1305 no mostradas):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Notas

- Bob debe realizar la validación habitual del Router Info. Asegurar que el tipo de firma sea compatible, verificar la firma, verificar que la marca de tiempo esté dentro de los límites, y cualquier otra verificación necesaria.

- Bob debe verificar que la clave estática de Alice recibida en el primer frame coincida con la clave estática en la Router Info. Bob debe buscar primero en la Router Info una Router Address NTCP o NTCP2 con una opción de versión (v) coincidente. Ver las secciones de Router Info Publicada y Router Info No Publicada a continuación.

- Si Bob tiene una versión más antigua del RouterInfo de Alice en su netdb, verificar que la clave estática en la información del router sea la misma en ambas, si está presente, y si la versión más antigua es menos de XXX antigua (ver tiempo de rotación de clave abajo)

- Bob debe validar que la clave estática de Alice es un punto válido en la curva aquí.

- Se deben incluir opciones para especificar parámetros de relleno.

- En caso de cualquier error, incluyendo fallos de AEAD, RI, DH, timestamp o validación de clave, Bob debe detener el procesamiento posterior de mensajes y cerrar la conexión sin responder. Este debe ser un cierre anormal (TCP RST).

- Para facilitar el handshaking rápido, las implementaciones deben asegurar que Alice almacene en búfer y luego envíe todo el contenido del tercer mensaje de una vez, incluyendo ambos marcos AEAD. Esto aumenta la probabilidad de que los datos se contengan en un solo paquete TCP (a menos que sean segmentados por el SO o middleboxes), y sean recibidos todos a la vez por Bob. Esto también es por eficiencia y para asegurar la efectividad del relleno aleatorio.

- Longitud del frame de la parte 2 del mensaje 3: La longitud de este frame (incluyendo MAC) es enviada por Alice en el mensaje 1. Ver ese mensaje para notas importantes sobre permitir suficiente espacio para el padding.

- Contenido del marco de la parte 2 del mensaje 3: El formato de este marco es el mismo que el formato de los marcos de la fase de datos, excepto que la longitud del marco es enviada por Alice en el mensaje 1. Ver más abajo el formato del marco de la fase de datos. El marco debe contener de 1 a 3 bloques en el siguiente orden:

1)  Bloque de información del router de Alice (requerido)   2)  Bloque de opciones (opcional)

3\) Bloque de relleno (opcional) Este marco nunca debe contener ningún otro tipo de bloque.

- El relleno de la parte 2 del mensaje 3 no es necesario si Alice añade una trama de fase de datos (opcionalmente conteniendo relleno) al final del mensaje 3 y envía ambos de una vez, ya que aparecerá como un gran flujo de bytes para un observador. Como Alice generalmente, pero no siempre, tendrá un mensaje I2NP para enviar a Bob (por eso se conectó a él), esta es la implementación recomendada, por eficiencia y para asegurar la efectividad del relleno aleatorio.

- La longitud máxima teórica total de ambos marcos AEAD del mensaje 3 (partes 1 y 2) es de 65535 bytes; la parte 1 tiene 48 bytes, por lo que la longitud máxima del marco de la parte 2 es 65487; la longitud máxima de texto claro de la parte 2, excluyendo el MAC, es 65471.
  ADVERTENCIA: Algunas implementaciones imponen longitudes mucho más pequeñas. Actualmente, Java I2P limita la longitud total a 4096 bytes. No agregue relleno excesivo.

### Función de Derivación de Claves (KDF) (para la fase de datos)

La fase de datos utiliza una entrada de datos asociados de longitud cero.

El KDF genera dos claves de cifrado k_ab y k_ba a partir de la clave de encadenamiento ck, utilizando HMAC-SHA256(key, data) según se define en [RFC-2104](https://tools.ietf.org/html/rfc2104). Esta es la función Split(), exactamente como se define en la especificación Noise.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Fase de Datos

Payload de Noise: Como se define a continuación, incluyendo relleno aleatorio Payload sin Noise: ninguno

Comenzando con la segunda parte del mensaje 3, todos los mensajes están dentro de un "marco" ChaChaPoly autenticado y encriptado con una longitud ofuscada de dos bytes antepuesta. Todo el relleno está dentro del marco. Dentro del marco hay un formato estándar con cero o más "bloques". Cada bloque tiene un tipo de un byte y una longitud de dos bytes. Los tipos incluyen fecha/hora, mensaje I2NP, opciones, terminación y relleno.

Nota: Bob puede, pero no está obligado a, enviar su RouterInfo a Alice como su primer mensaje a Alice en la fase de datos.

(Propiedades de Seguridad de Carga Útil de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Notas

- Para eficiencia y minimizar la identificación del campo de longitud, las implementaciones deben asegurar que el remitente almacene en buffer y luego envíe todo el contenido de los mensajes de datos de una vez, incluyendo el campo de longitud y el frame AEAD. Esto incrementa la probabilidad de que los datos estén contenidos en un solo paquete TCP (a menos que sean segmentados por el SO o middleboxes), y recibidos de una vez por la otra parte. Esto también es por eficiencia y para asegurar la efectividad del padding aleatorio.
- El router puede elegir terminar la sesión ante un error AEAD, o puede continuar intentando comunicaciones. Si continúa, el router debería terminar después de errores repetidos.

#### Longitud ofuscada de SipHash

Referencia: [SipHash](https://www.131002.net/siphash/)

Una vez que ambos lados han completado el handshake, transfieren cargas útiles que luego son cifradas y autenticadas en "frames" de ChaChaPoly.

Cada frame está precedido por una longitud de dos bytes, big endian. Esta longitud especifica el número de bytes de frame cifrados que siguen, incluyendo el MAC. Para evitar transmitir campos de longitud identificables en el stream, la longitud del frame se ofusca mediante XOR con una máscara derivada de SipHash, tal como se inicializa desde el KDF de la fase de datos. Nótese que las dos direcciones tienen claves SipHash e IVs únicos del KDF.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
El receptor tiene las claves SipHash y IV idénticos. La decodificación de la longitud se realiza derivando la máscara utilizada para ofuscar la longitud y aplicando XOR al digest truncado para obtener la longitud del frame. La longitud del frame es la longitud total del frame cifrado incluyendo el MAC.

#### Notas

- Si usas una función de biblioteca SipHash que devuelve un entero largo sin signo, usa los dos bytes menos significativos como la Máscara. Convierte el entero largo al siguiente IV como little endian.

#### Contenidos sin procesar

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Notas

- Como el receptor debe obtener toda la trama para verificar el MAC, se recomienda que el emisor limite las tramas a unos pocos KB en lugar de maximizar el tamaño de la trama. Esto minimizará la latencia en el receptor.

#### Datos sin cifrar

Hay cero o más bloques en el frame cifrado. Cada bloque contiene un identificador de un byte, una longitud de dos bytes y cero o más bytes de datos.

Para extensibilidad, los receptores deben ignorar bloques con identificadores desconocidos y tratarlos como relleno.

Los datos cifrados tienen un máximo de 65535 bytes, incluyendo un encabezado de autenticación de 16 bytes, por lo que el máximo de datos sin cifrar es de 65519 bytes.

(etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Reglas de Ordenamiento de Bloques

En la parte 2 del mensaje 3 del handshake, el orden debe ser: RouterInfo, seguido de Options si está presente, seguido de Padding si está presente. No se permiten otros bloques.

En la fase de datos, el orden no está especificado, excepto por los siguientes requisitos: El relleno, si está presente, debe ser el último bloque. La terminación, si está presente, debe ser el último bloque excepto por el relleno.

Puede haber múltiples bloques I2NP en una sola trama. No se permiten múltiples bloques de relleno en una sola trama. Otros tipos de bloques probablemente no tendrán múltiples bloques en una sola trama, pero no está prohibido.

#### FechaHora

Caso especial para sincronización de tiempo:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
NOTA: Las implementaciones deben redondear al segundo más cercano para prevenir sesgos de reloj en la red.

#### Opciones

Pasar opciones actualizadas. Las opciones incluyen: Padding mínimo y máximo.

El bloque de opciones tendrá longitud variable.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Problemas de Opciones

- El formato de opciones está por definir.
- La negociación de opciones está por definir.

#### RouterInfo

Pasar la RouterInfo de Alice a Bob. Se usa en la parte 2 del mensaje 3 del handshake. Pasar la RouterInfo de Alice a Bob, o la de Bob a Alice. Se usa opcionalmente en la fase de datos.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Notas

- Cuando se use en la fase de datos, el receptor (Alice o Bob) debe validar que sea el mismo Router Hash que fue enviado originalmente (para Alice) o enviado a (para Bob). Luego, tratarlo como un Mensaje I2NP DatabaseStore local. Validar la firma, validar la marca de tiempo más reciente y almacenar en la netDb local. Si el bit de bandera 0 es 1, y la parte receptora es floodfill, tratarlo como un Mensaje DatabaseStore con un token de respuesta distinto de cero, y propagarlo a los floodfills más cercanos.
- El Router Info NO está comprimido con gzip (a diferencia de un Mensaje DatabaseStore, donde sí lo está)
- No se debe solicitar propagación a menos que haya RouterAddresses publicadas en el RouterInfo. El router receptor no debe propagar el RouterInfo a menos que tenga RouterAddresses publicadas en él.
- Los implementadores deben asegurar que al leer un bloque, datos malformados o maliciosos no causen que las lecturas se desborden hacia el siguiente bloque.
- Este protocolo no proporciona un reconocimiento de que el RouterInfo fue recibido, almacenado o propagado (ya sea en la fase de handshake o de datos). Si se desea reconocimiento, y el receptor es floodfill, el emisor debe enviar en su lugar un DatabaseStoreMessage I2NP estándar con un token de respuesta.

#### Problemas

- También podría usarse en la fase de datos, en lugar de un I2NP DatabaseStoreMessage. Por ejemplo, Bob podría usarlo para iniciar la fase de datos.
- ¿Está permitido que esto contenga el RI para routers distintos al originador, como un reemplazo general para DatabaseStoreMessages, por ejemplo, para flooding por floodfills?

#### I2NP Message

Un solo mensaje I2NP con un encabezado modificado. Los mensajes I2NP no pueden ser fragmentados a través de bloques o a través de tramas ChaChaPoly.

Esto utiliza los primeros 9 bytes del encabezado I2NP estándar de NTCP, y elimina los últimos 7 bytes del encabezado, de la siguiente manera: acorta la expiración de 8 a 4 bytes (segundos en lugar de milisegundos, igual que para SSU), elimina la longitud de 2 bytes (usa el tamaño del bloque - 9), y elimina el checksum SHA256 de un byte.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Notas

- Los implementadores deben asegurar que al leer un bloque, los datos malformados o maliciosos no causen que las lecturas se desborden hacia el siguiente bloque.

#### Terminación

Noise recomienda un mensaje de terminación explícito. NTCP original no tiene uno. Desconectar la conexión. Este debe ser el último bloque sin relleno en el frame.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Notas

No todas las razones pueden ser utilizadas realmente, depende de la implementación. Los fallos de handshake generalmente resultarán en un cierre con TCP RST en su lugar. Ver las notas en las secciones de mensajes de handshake anteriores. Las razones adicionales listadas son para consistencia, registro, depuración, o si las políticas cambian.

#### Relleno

Esto es para el relleno dentro de los marcos AEAD. El relleno para los mensajes 1 y 2 están fuera de los marcos AEAD. Todo el relleno para el mensaje 3 y la fase de datos están dentro de los marcos AEAD.

El relleno dentro de AEAD debe adherirse aproximadamente a los parámetros negociados. Bob envió sus parámetros mín/máx de tx/rx solicitados en el mensaje 2. Alice envió sus parámetros mín/máx de tx/rx solicitados en el mensaje 3. Las opciones actualizadas pueden enviarse durante la fase de datos. Consulta la información del bloque de opciones arriba.

Si está presente, este debe ser el último bloque en el frame.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Notas

- Se permite tamaño = 0.
- Estrategias de relleno por determinar.
- Relleno mínimo por determinar.
- Se permiten tramas de solo relleno.
- Valores predeterminados de relleno por determinar.
- Ver bloque de opciones para negociación de parámetros de relleno
- Ver bloque de opciones para parámetros de relleno mín/máx
- Noise limita los mensajes a 64KB. Si se necesita más relleno, envía múltiples tramas.
- La respuesta del router ante violación del relleno negociado depende de la implementación.

#### Otros tipos de bloques

Las implementaciones deben ignorar los tipos de bloque desconocidos para compatibilidad futura, excepto en el mensaje 3 parte 2, donde no se permiten bloques desconocidos.

#### Trabajo futuro

- La longitud del relleno debe decidirse por mensaje basándose en estimaciones de la distribución de longitudes, o se deben agregar retrasos aleatorios. Estas contramedidas deben incluirse para resistir DPI, ya que de lo contrario los tamaños de los mensajes revelarían que el protocolo de transporte está llevando tráfico I2P. El esquema exacto de relleno es un área de trabajo futuro.

### 5) Terminación

Las conexiones pueden terminarse mediante el cierre normal o anormal del socket TCP, o, como recomienda Noise, un mensaje de terminación explícito. El mensaje de terminación explícito se define en la fase de datos anterior.

Ante cualquier terminación normal o anormal, los routers deben poner a cero todos los datos efímeros en memoria, incluyendo las claves efímeras de handshake, las claves de cifrado simétricas y la información relacionada.

## Información de Router Publicada

### Capacidades

A partir de la versión 0.9.50, la opción "caps" es compatible en direcciones NTCP2, similar a SSU. Una o más capacidades pueden publicarse en la opción "caps". Las capacidades pueden estar en cualquier orden, pero "46" es el orden recomendado, para mantener consistencia entre implementaciones. Hay dos capacidades definidas:

4: Indica capacidad IPv4 saliente. Si una IP está publicada en el campo host, esta capacidad no es necesaria. Si el router está oculto, o NTCP2 es solo saliente, '4' y '6' pueden combinarse en una sola dirección.

6: Indica capacidad IPv6 saliente. Si se publica una IP en el campo host, esta capacidad no es necesaria. Si el router está oculto, o NTCP2 es solo saliente, '4' y '6' pueden combinarse en una sola dirección.

### Direcciones Publicadas

El RouterAddress publicado (parte del RouterInfo) tendrá un identificador de protocolo de "NTCP" o "NTCP2".

La RouterAddress debe contener las opciones "host" y "port", como en el protocolo NTCP actual.

La RouterAddress debe contener tres opciones para indicar compatibilidad con NTCP2:

- s=(Clave Base64) La clave pública estática Noise actual (s) para esta RouterAddress. Codificada en Base 64 usando el alfabeto Base 64 estándar de I2P. 32 bytes en binario, 44 bytes codificada en Base 64, clave pública X25519 little-endian.
- i=(IV Base64) El IV actual para cifrar el valor X en el mensaje 1 para esta RouterAddress. Codificado en Base 64 usando el alfabeto Base 64 estándar de I2P. 16 bytes en binario, 24 bytes codificado en Base 64, big-endian.
- v=2 La versión actual (2). Cuando se publica como "NTCP", se implica soporte adicional para la versión 1. El soporte para versiones futuras será con valores separados por comas, ej. v=2,3 La implementación debe verificar la compatibilidad, incluyendo múltiples versiones si hay una coma presente. Las versiones separadas por comas deben estar en orden numérico.

Alice debe verificar que las tres opciones estén presentes y sean válidas antes de conectarse usando el protocolo NTCP2.

Cuando se publica como "NTCP" con opciones "s", "i" y "v", el router debe aceptar conexiones entrantes en ese host y puerto para ambos protocolos NTCP y NTCP2, y detectar automáticamente la versión del protocolo.

Cuando se publica como "NTCP2" con las opciones "s", "i" y "v", el router acepta conexiones entrantes en ese host y puerto solo para el protocolo NTCP2.

Si un router admite tanto conexiones NTCP1 como NTCP2 pero no implementa detección automática de versión para conexiones entrantes, debe anunciar tanto direcciones "NTCP" como "NTCP2", e incluir las opciones NTCP2 únicamente en la dirección "NTCP2". El router debería establecer un valor de costo menor (mayor prioridad) en la dirección "NTCP2" que en la dirección "NTCP", para que NTCP2 sea preferido.

Si se publican múltiples NTCP2 RouterAddresses (ya sea como "NTCP" o "NTCP2") en el mismo RouterInfo (para direcciones IP o puertos adicionales), todas las direcciones que especifiquen el mismo puerto deben contener las opciones y valores NTCP2 idénticos. En particular, todas deben contener la misma clave estática e iv.

### Dirección NTCP2 No Publicada

Si Alice no publica su dirección NTCP2 (como "NTCP" o "NTCP2") para conexiones entrantes, debe publicar una dirección de router "NTCP2" que contenga únicamente su clave estática y la versión NTCP2, para que Bob pueda validar la clave después de recibir el RouterInfo de Alice en la parte 2 del mensaje 3.

- s=(Clave Base64) Como se define arriba para las direcciones publicadas.
- v=2 Como se define arriba para las direcciones publicadas.

Esta dirección del router no contendrá las opciones "i", "host" o "port", ya que no son necesarias para las conexiones NTCP2 salientes. El coste publicado para esta dirección no importa estrictamente, ya que es solo de entrada; sin embargo, puede ser útil para otros routers si el coste se establece más alto (menor prioridad) que otras direcciones. El valor sugerido es 14.

Alice también puede simplemente agregar las opciones "s" y "v" a una dirección "NTCP" publicada existente.

### Rotación de Clave Pública e IV

Debido al almacenamiento en caché de RouterInfos, los routers no deben rotar la clave pública estática o el IV mientras el router esté en funcionamiento, ya sea en una dirección publicada o no. Los routers deben almacenar de forma persistente esta clave e IV para reutilizarlos después de un reinicio inmediato, de modo que las conexiones entrantes continúen funcionando y los tiempos de reinicio no queden expuestos. Los routers deben almacenar de forma persistente, o determinar de otra manera, el tiempo del último apagado, para que el tiempo de inactividad previo pueda calcularse al inicio.

Sujeto a preocupaciones sobre exponer los tiempos de reinicio, los routers pueden rotar esta clave o IV al inicio si el router estuvo previamente inactivo por algún tiempo (al menos un par de horas).

Si el router tiene cualquier RouterAddresses NTCP2 publicadas (como NTCP o NTCP2), el tiempo de inactividad mínimo antes de la rotación debería ser mucho más largo, por ejemplo un mes, a menos que la dirección IP local haya cambiado o el router realice un "rekeys".

Si el router tiene direcciones RouterAddresses SSU publicadas, pero no NTCP2 (como NTCP o NTCP2), el tiempo mínimo de inactividad antes de la rotación debería ser más largo, por ejemplo un día, a menos que la dirección IP local haya cambiado o el router haga "rekeys". Esto se aplica incluso si la dirección SSU publicada tiene introducers.

Si el router no tiene ninguna RouterAddress publicada (NTCP, NTCP2, o SSU), el tiempo mínimo de inactividad antes de la rotación puede ser tan corto como dos horas, incluso si la dirección IP cambia, a menos que el router haga "rekeys" (regenere claves).

Si el router "regenera claves" a un Router Hash diferente, también debería generar una nueva clave de ruido e IV.

Las implementaciones deben tener en cuenta que cambiar la clave pública estática o el IV prohibirá las conexiones NTCP2 entrantes de routers que tengan en caché un RouterInfo más antiguo. La publicación de RouterInfo, la selección de peers de túnel (incluyendo tanto OBGW como el salto más cercano IB), la selección de túneles de cero saltos, la selección de transporte y otras estrategias de implementación deben tomar esto en cuenta.

La rotación de IV está sujeta a las mismas reglas que la rotación de claves, excepto que los IV no están presentes salvo en las RouterAddresses publicadas, por lo que no hay IV para routers ocultos o protegidos por firewall. Si algo cambia (versión, clave, opciones?) se recomienda que el IV también cambie.

Nota: El tiempo mínimo de inactividad antes del rekeying puede ser modificado para garantizar la salud de la red y prevenir el reseeding por parte de un router que haya estado inactivo durante un período moderado de tiempo.

## Detección de Versión

Cuando se publica como "NTCP", el router debe detectar automáticamente la versión del protocolo para las conexiones entrantes.

Esta detección depende de la implementación, pero aquí se proporciona una guía general.

Para detectar la versión de una conexión NTCP entrante, Bob procede de la siguiente manera:

- Esperar al menos 64 bytes (tamaño mínimo del mensaje 1 de NTCP2)

- Si los datos iniciales recibidos son de 288 o más bytes, la conexión entrante es versión 1.

- Si es menor de 288 bytes, cualquiera de las siguientes opciones

> - Esperar un poco más de tiempo para recibir más datos (buena estrategia antes de la adopción generalizada de NTCP2) si se han recibido al menos 288 bytes en total, es NTCP 1.   >   > - Intentar las primeras etapas de decodificación como versión 2, si falla, esperar un poco más de tiempo para recibir más datos (buena estrategia después de la adopción generalizada de NTCP2)   >   >   > - Descifrar los primeros 32 bytes (la clave X) del paquete SessionRequest usando AES-256 con la clave RH_B.   >   > - Verificar un punto válido en la curva. Si falla, esperar un poco más de tiempo para recibir más datos para NTCP 1   >   > - Verificar el frame AEAD. Si falla, esperar un poco más de tiempo para recibir más datos para NTCP 1

Ten en cuenta que se pueden recomendar cambios o estrategias adicionales si detectamos ataques activos de segmentación TCP en NTCP 1.

Para facilitar la detección rápida de versión y el handshake, las implementaciones deben asegurar que Alice almacene en búfer y luego envíe todo el contenido del primer mensaje de una vez, incluyendo el relleno. Esto aumenta la probabilidad de que los datos estén contenidos en un solo paquete TCP (a menos que sean segmentados por el SO o middleboxes), y sean recibidos de una sola vez por Bob. Esto también es por eficiencia y para asegurar la efectividad del relleno aleatorio. Esto se aplica tanto a handshakes NTCP como NTCP2.

## Variantes, Alternativas y Problemas Generales

- Si tanto Alice como Bob admiten NTCP2, Alice debería conectarse con NTCP2.
- Si Alice falla al conectarse a Bob usando NTCP2 por cualquier motivo, la conexión falla. Alice no puede reintentar usando NTCP 1.

## Pautas de Desviación de Reloj

Las marcas de tiempo de los peers se incluyen en los primeros dos mensajes de handshake, Session Request y Session Created. Una desincronización de reloj entre dos peers mayor a +/- 60 segundos es generalmente fatal. Si Bob piensa que su reloj local está mal, puede ajustar su reloj usando la desincronización calculada, o alguna fuente externa. De lo contrario, Bob debería responder con un Session Created incluso si se excede la desincronización máxima, en lugar de simplemente cerrar la conexión. Esto permite que Alice obtenga la marca de tiempo de Bob y calcule la desincronización, y tome medidas si es necesario. Bob no tiene la identidad del router de Alice en este punto, pero para conservar recursos, puede ser deseable que Bob prohíba las conexiones entrantes desde la IP de Alice por algún período de tiempo, o después de intentos de conexión repetidos con una desincronización excesiva.

Alice debería ajustar el desfase de reloj calculado restando la mitad del RTT. Si Alice piensa que su reloj local está mal, puede ajustar su reloj usando el desfase calculado, o alguna fuente externa. Si Alice piensa que el reloj de Bob está mal, puede prohibir a Bob por algún período de tiempo. En cualquier caso, Alice debería cerrar la conexión.

Si Alice responde con Session Confirmed (probablemente porque el sesgo es muy cercano al límite de 60s, y los cálculos de Alice y Bob no son exactamente iguales debido al RTT), Bob debería ajustar el sesgo de reloj calculado restando la mitad del RTT. Si el sesgo de reloj ajustado excede el máximo, Bob debería entonces responder con un mensaje Disconnect que contenga un código de razón de sesgo de reloj, y cerrar la conexión. En este punto, Bob tiene la identidad del router de Alice, y puede prohibir a Alice por algún período de tiempo.

## Referencias

- [Estructuras Comunes](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Base de Datos de Red](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
