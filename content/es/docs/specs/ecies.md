---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Esquema de Cifrado Integrado de Curva Elíptica para el cifrado extremo a extremo de I2P"
slug: "ecies"
aliases:
  - "/es/docs/specs/ecies-x25519-aead-ratchet"
  - "/es/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protocolos"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Nota

Despliegue de red completado. Sujeto a revisiones menores. Ver [Prop144](/proposals/144-ecies-x25519/) para la propuesta original, incluyendo discusión de antecedentes e información adicional.

Las siguientes características no están implementadas a partir de la versión 0.9.66:

- Bloques MessageNumbers, Options y Termination
- Respuestas de capa de protocolo
- Clave estática cero
- Multidifusión

Para la versión híbrida PQ MLKEM de este protocolo, consulta [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Descripción general

Este es el nuevo protocolo de cifrado de extremo a extremo para reemplazar ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Se basa en trabajos previos de la siguiente manera:

- Especificación de estructuras comunes [Common](/docs/specs/common-structures/)
- Especificación [I2NP](/docs/specs/i2np/) incluyendo LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> resumen de criptografía asimétrica nueva
- Resumen de criptografía de bajo nivel [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Nuevas entradas netDB
- 142 Nueva plantilla de criptografía
- Protocolo [Noise](https://noiseprotocol.org/noise.html)
- Algoritmo de doble trinquete de [Signal](https://signal.org/docs/specifications/doubleratchet/)

Admite cifrado nuevo para comunicación extremo a extremo, de destino a destino.

El diseño utiliza un handshake Noise y una fase de datos que incorpora el double ratchet de Signal.

Todas las referencias a Signal y Noise en esta especificación son únicamente para información de contexto. El conocimiento de los protocolos Signal y Noise no es necesario para entender o implementar esta especificación.

Esta especificación es compatible a partir de la versión 0.9.46.

## Especificación

El diseño utiliza un handshake Noise y una fase de datos que incorpora el doble trinquete de Signal.

### Resumen del Diseño Criptográfico

Hay cinco partes del protocolo que deben ser rediseñadas:

- 1\) Los formatos de contenedor de Sesión nueva y Existente son reemplazados con
  nuevos formatos.
- 2\) ElGamal (claves públicas de 256 bytes, claves privadas de 128 bytes) es
  reemplazado con ECIES-X25519 (claves públicas y privadas de 32 bytes)
- 3\) AES es reemplazado con AEAD_ChaCha20_Poly1305 (abreviado como
  ChaChaPoly abajo)
- 4\) SessionTags serán reemplazados con ratchets, que es esencialmente un
  PRNG criptográfico y sincronizado.
- 5\) La carga útil AES, tal como se define en la especificación
  ElGamal/AES+SessionTags, es reemplazada con un formato de bloques similar al de
  NTCP2.

Cada uno de los cinco cambios tiene su propia sección a continuación.

### Tipo de Criptografía

El tipo de crypto (usado en el LS2) es 4. Esto indica una clave pública X25519 de 32 bytes little-endian, y el protocolo extremo a extremo especificado aquí.

El tipo de criptografía 0 es ElGamal. Los tipos de criptografía 1-3 están reservados para ECIES-ECDH-AES-SessionTag, ver propuesta 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Framework del Protocolo Noise

Este protocolo proporciona los requisitos basados en el Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisión 34, 2018-07-11). Noise tiene propiedades similares al protocolo Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), que es la base para el protocolo [SSU](/docs/transport/ssu/). En la terminología de Noise, Alice es el iniciador, y Bob es el receptor.

Esta especificación se basa en el protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256. (El identificador real para la función inicial de derivación de claves es "Noise_IKelg2_25519_ChaChaPoly_SHA256" para indicar las extensiones de I2P - ver la sección KDF 1 a continuación) Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Handshake Interactivo: IK Alice transmite inmediatamente su
  clave estática a Bob (I) Alice ya conoce la clave estática de Bob (K)
- Patrón de Handshake Unidireccional: N Alice no transmite su clave estática a
  Bob (N)
- Función DH: X25519 X25519 DH con una longitud de clave de 32 bytes como se
  especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Función de Cifrado: ChaChaPoly AEAD_CHACHA20_POLY1305 como se especifica en
  [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8. Nonce de 12 bytes, con
  los primeros 4 bytes establecidos en cero. Idéntico al de
  [NTCP2](/docs/specs/ntcp2/).
- Función Hash: SHA256 Hash estándar de 32 bytes, ya ampliamente usado
  en I2P.

#### Adiciones al Framework

Esta especificación define las siguientes mejoras a Noise_IK_25519_ChaChaPoly_SHA256. Estas generalmente siguen las pautas de la sección 13 de [NOISE](https://noiseprotocol.org/noise.html).

1)  Las claves efímeras en texto claro se codifican con

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) La respuesta tiene como prefijo una etiqueta de texto plano. 3) El formato de carga útil está definido para los mensajes 1, 2 y la fase de datos.

    Of course, this is not defined in Noise.

Todos los mensajes incluyen un encabezado de mensaje I2NP [I2NP](/docs/specs/i2np/) Garlic Message. La fase de datos utiliza cifrado similar al de la fase de datos de Noise, pero no es compatible con ella.

### Patrones de Handshake

Los handshakes utilizan patrones de handshake [Noise](https://noiseprotocol.org/noise.html).

Se utiliza la siguiente correspondencia de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje

Las sesiones de un solo uso y sin vincular son similares al patrón Noise N.

```
<- s
...
e es p ->
```
Las sesiones vinculadas son similares al patrón Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Propiedades de Seguridad

Usando la terminología Noise, la secuencia de establecimiento y datos es la siguiente: (Propiedades de Seguridad del Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Diferencias con XK

Los handshakes IK tienen varias diferencias con respecto a los handshakes XK utilizados en [NTCP2](/docs/specs/ntcp2/) y [SSU2](/docs/specs/ssu2/).

- Cuatro operaciones DH en total comparadas con tres para XK
- Autenticación del remitente en el primer mensaje: La carga útil se autentica
  como perteneciente al propietario de la clave pública del remitente, aunque la
  clave podría haber sido comprometida (Autenticación 1) XK requiere otra
  ida y vuelta antes de que Alice sea autenticada.
- Secreto hacia adelante completo (Confidencialidad 5) después del segundo mensaje. Bob
  puede enviar una carga útil inmediatamente después del segundo mensaje con secreto
  hacia adelante completo. XK requiere otra ida y vuelta para el secreto hacia
  adelante completo.

En resumen, IK permite la entrega 1-RTT de la carga útil de respuesta de Bob a Alice con secreto hacia adelante completo, sin embargo la carga útil de solicitud no tiene secreto hacia adelante.

### Sesiones

El protocolo ElGamal/AES+SessionTag es unidireccional. En esta capa, el receptor no sabe de dónde proviene un mensaje. Las sesiones de salida y entrada no están asociadas. Los acuses de recibo se realizan fuera de banda usando un DeliveryStatusMessage (envuelto en un GarlicMessage) en el clove.

Para esta especificación, definimos dos mecanismos para crear un protocolo bidireccional: "emparejamiento" y "enlace". Estos mecanismos proporcionan mayor eficiencia y seguridad.

#### Contexto de Sesión

Al igual que con ElGamal/AES+SessionTags, todas las sesiones entrantes y salientes deben estar en un contexto dado, ya sea el contexto del router o el contexto para un destino local particular. En Java I2P, este contexto se llama Session Key Manager.

Las sesiones no deben compartirse entre contextos, ya que eso permitiría la correlación entre los diversos destinos locales, o entre un destino local y un router.

Cuando un destino dado admite tanto ElGamal/AES+SessionTags como esta especificación, ambos tipos de sesiones pueden compartir un contexto. Ver sección 1c) a continuación.

#### Emparejamiento de Sesiones Entrantes y Salientes

Cuando se crea una sesión saliente en el originador (Alice), se crea una nueva sesión entrante y se empareja con la sesión saliente, a menos que no se espere respuesta (por ejemplo, datagramas sin procesar).

Una nueva sesión entrante siempre se empareja con una nueva sesión saliente, a menos que no se solicite respuesta (por ejemplo, datagramas sin procesar).

Si se solicita una respuesta y está vinculada a un destino o router de extremo remoto, esa nueva sesión saliente se vincula a ese destino o router, y reemplaza cualquier sesión saliente anterior a ese destino o router.

Emparejar sesiones entrantes y salientes proporciona un protocolo bidireccional con la capacidad de renovar las claves DH.

#### Vinculación de Sesiones y Destinos

Solo hay una sesión saliente a un destino o router determinado. Puede haber varias sesiones entrantes actuales desde un destino o router determinado. Generalmente, cuando se crea una nueva sesión entrante y se recibe tráfico en esa sesión (lo que sirve como un ACK), cualquier otra será marcada para expirar relativamente rápido, en un minuto aproximadamente. Se verifica el valor de mensajes enviados anteriormente (PN), y si no hay mensajes no recibidos (dentro del tamaño de ventana) en la sesión entrante anterior, la sesión anterior puede ser eliminada inmediatamente.

Cuando se crea una sesión saliente en el originador (Alice), se vincula al Destination de destino (Bob), y cualquier sesión entrante emparejada también se vinculará al Destination de destino. A medida que las sesiones avanzan, continúan estando vinculadas al Destination de destino.

Cuando se crea una sesión entrante en el receptor (Bob), puede vincularse al Destination del extremo remoto (Alice), a elección de Alice. Si Alice incluye información de vinculación (su clave estática) en el mensaje New Session, la sesión se vinculará a ese destination, y se creará una sesión saliente que se vinculará al mismo Destination. Mientras las sesiones avanzan con ratchet, continúan vinculadas al Destination del extremo remoto.

#### Beneficios del Vinculación y Emparejamiento

Para el caso común de streaming, esperamos que Alice y Bob utilicen el protocolo de la siguiente manera:

- Alice empareja su nueva sesión saliente con una nueva sesión entrante, ambas
  vinculadas al destino del extremo remoto (Bob).
- Alice incluye la información de vinculación y la firma, junto con una solicitud
  de respuesta, en el mensaje New Session enviado a Bob.
- Bob empareja su nueva sesión entrante con una nueva sesión saliente, ambas
  vinculadas al destino del extremo remoto (Alice).
- Bob envía una respuesta (ack) a Alice en la sesión emparejada, con un ratchet
  a una nueva clave DH.
- Alice hace ratchet a una nueva sesión saliente con la nueva clave de Bob, emparejada
  con la sesión entrante existente.

Al vincular una sesión entrante a un Destination de extremo remoto, y emparejar la sesión entrante con una sesión saliente vinculada al mismo Destination, logramos dos beneficios principales:

1) La respuesta inicial de Bob a Alice utiliza DH efímero-efímero

2\) Después de que Alice recibe la respuesta de Bob y hace ratcheting, todos los mensajes posteriores de Alice a Bob utilizan DH efímero-efímero.

#### ACKs de mensajes

En ElGamal/AES+SessionTags, cuando un LeaseSet se empaqueta como un diente de garlic, o se entregan etiquetas, el router emisor solicita un ACK. Este es un diente de garlic separado que contiene un Mensaje DeliveryStatus. Para seguridad adicional, el Mensaje DeliveryStatus se envuelve en un Mensaje Garlic. Este mecanismo está fuera de banda desde la perspectiva del protocolo.

En el nuevo protocolo, dado que las sesiones entrantes y salientes están emparejadas, podemos tener ACKs en banda. No se requiere un clove separado.

Un ACK explícito es simplemente un mensaje de Sesión Existente sin bloque I2NP. Sin embargo, en la mayoría de los casos, se puede evitar un ACK explícito, ya que hay tráfico en sentido inverso. Puede ser deseable que las implementaciones esperen un corto período de tiempo (tal vez unos cien ms) antes de enviar un ACK explícito, para dar tiempo a la capa de streaming o aplicación a responder.

Las implementaciones también necesitarán diferir el envío de cualquier ACK hasta después de que se procese el bloque I2NP, ya que el Garlic Message puede contener un Database Store Message con un lease set. Un lease set reciente será necesario para enrutar el ACK, y el destino del extremo lejano (contenido en el lease set) será necesario para verificar la clave estática de vinculación.

#### Tiempos de Espera de Sesión

Las sesiones de salida siempre deben expirar antes que las sesiones de entrada. Una vez que una sesión de salida expira y se crea una nueva, también se creará una nueva sesión de entrada emparejada. Si había una sesión de entrada antigua, se le permitirá expirar.

### Multicast

Por determinar

### Definiciones

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados.

ZEROLEN

arreglo de bytes de longitud cero

CSRNG(n)

salida de n bytes de un número aleatorio criptográficamente seguro

    generator.

H(p, d)

Función hash SHA-256 que toma una cadena de personalización p y datos

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Función hash SHA-256 que toma un hash anterior h y nuevos datos d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

El AEAD ChaCha20/Poly1305 como se especifica en

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Sistema de acuerdo de claves públicas X25519. Claves privadas de 32 bytes, públicas

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Una función criptográfica de derivación de claves que toma alguna clave de entrada

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Usa HKDF() con una chainKey anterior y nuevos datos d, y establece la nueva

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Formato de mensaje

#### Revisión del Formato de Mensaje Actual

El Garlic Message según se especifica en [I2NP](/docs/specs/i2np/) es el siguiente. Como objetivo de diseño es que los saltos intermedios no puedan distinguir la criptografía nueva de la antigua, este formato no puede cambiar, aunque el campo de longitud sea redundante. El formato se muestra con el encabezado completo de 16 bytes, aunque el encabezado real puede estar en un formato diferente, dependiendo del transporte utilizado.

Cuando se descifra, los datos contienen una serie de Garlic Cloves y datos adicionales, también conocido como un Clove Set.

Consulta [I2NP](/docs/specs/i2np/) para obtener detalles y una especificación completa.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Revisión del Formato de Datos Cifrados

En ElGamal/AES+SessionTags, hay dos formatos de mensaje:

1\) Nueva sesión: - Bloque ElGamal de 514 bytes - Bloque AES (128 bytes mínimo, múltiplo de 16)

2\) Sesión existente: - 32 bytes de Session Tag - Bloque AES (128 bytes mínimo, múltiplo de 16)

Estos mensajes están encapsulados en un mensaje I2NP garlic, que contiene un campo de longitud, por lo que se conoce la longitud.

El receptor primero intenta buscar los primeros 32 bytes como una Session Tag. Si la encuentra, descifra el bloque AES. Si no la encuentra, y los datos tienen al menos (514+16) de longitud, intenta descifrar el bloque ElGamal, y si tiene éxito, descifra el bloque AES.

#### Nuevas Etiquetas de Sesión y Comparación con Signal

En Signal Double Ratchet, el encabezado contiene:

- DH: Clave pública actual del ratchet
- PN: Longitud del mensaje de la cadena anterior
- N: Número de Mensaje

Las "cadenas de envío" de Signal son aproximadamente equivalentes a nuestros conjuntos de etiquetas. Al usar una etiqueta de sesión, podemos eliminar la mayor parte de eso.

En New Session, ponemos solo la clave pública en el encabezado no cifrado.

En Sesión Existente, usamos una etiqueta de sesión para el encabezado. La etiqueta de sesión está asociada con la clave pública ratchet actual y el número de mensaje.

En las sesiones nuevas y existentes, PN y N están en el cuerpo cifrado.

En Signal, las cosas están constantemente rotando. Una nueva clave pública DH requiere que el receptor rote y envíe una nueva clave pública de vuelta, lo cual también sirve como confirmación (ack) para la clave pública recibida. Esto sería demasiadas operaciones DH para nosotros. Por lo tanto, separamos la confirmación de la clave recibida y la transmisión de una nueva clave pública. Cualquier mensaje que use una etiqueta de sesión generada a partir de la nueva clave pública DH constituye una confirmación (ACK). Solo transmitimos una nueva clave pública cuando deseamos reestablecer las claves.

El número máximo de mensajes antes de que el DH deba hacer ratchet es 65535.

Al entregar una clave de sesión, derivamos el "Tag Set" de ella, en lugar de tener que entregar también las etiquetas de sesión. Un Tag Set puede tener hasta 65536 etiquetas. Sin embargo, los receptores deberían implementar una estrategia de "mirar hacia adelante", en lugar de generar todas las etiquetas posibles de una vez. Solo generar como máximo N etiquetas después de la última etiqueta válida recibida. N podría ser como máximo 128, pero 32 o incluso menos puede ser una mejor opción.

### 1a) Nuevo formato de sesión

Clave pública de una sola vez de nueva sesión (32 bytes) Datos cifrados y MAC (bytes restantes)

El mensaje New Session puede contener o no la clave pública estática del remitente. Si se incluye, la sesión inversa se vincula a esa clave. La clave estática debe incluirse si se esperan respuestas, es decir, para streaming y datagramas que admiten respuesta. No debe incluirse para datagramas sin procesar.

El mensaje New Session es similar al patrón unidireccional Noise [NOISE](https://noiseprotocol.org/noise.html) "N" (si la clave estática no se envía), o al patrón bidireccional "IK" (si la clave estática se envía).

### 1b) Nuevo formato de sesión (con vinculación)

La longitud es 96 + longitud de la carga útil. Formato cifrado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key                    +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
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
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nueva Clave Efímera de Sesión

La clave efímera es de 32 bytes, codificada con Elligator2. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo las retransmisiones.

#### Clave Estática

Cuando se descifra, la clave estática X25519 de Alice, 32 bytes.

#### Carga útil

La longitud encriptada es el resto de los datos. La longitud desencriptada es 16 menos que la longitud encriptada. La carga útil debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove. Consulta la sección de carga útil a continuación para el formato y requisitos adicionales.

### 1c) Nuevo formato de sesión (sin vinculación)

Si no se requiere respuesta, no se envía clave estática.

La longitud es 96 + longitud de la carga útil. Formato cifrado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
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
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nueva Clave Efímera de Sesión

Clave efímera de Alice. La clave efímera es de 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo las retransmisiones.

#### Sección de Banderas Datos descifrados

La sección Flags no contiene nada. Siempre son 32 bytes, porque debe tener la misma longitud que la clave estática para los mensajes New Session con vinculación. Bob determina si son una clave estática o una sección flags verificando si los 32 bytes son todos ceros.

TODO ¿se necesitan flags aquí?

#### Carga útil

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. La carga útil debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove. Ver la sección de carga útil a continuación para el formato y requisitos adicionales.

### 1d) Formato de una sola vez (sin vinculación o sesión)

Si solo se espera enviar un único mensaje, no se requiere configuración de sesión ni clave estática.

La longitud es 96 + longitud del payload. Formato encriptado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
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
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nueva Clave de Una Sola Vez de Sesión

La clave de un solo uso es de 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo las retransmisiones.

#### Sección de Banderas Datos descifrados

La sección Flags no contiene nada. Siempre tiene 32 bytes, porque debe tener la misma longitud que la clave estática para los mensajes New Session con binding. Bob determina si se trata de una clave estática o una sección flags probando si los 32 bytes son todos ceros.

TODO ¿algún flag necesario aquí?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Carga útil

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. La carga útil debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove. Consulte la sección de carga útil a continuación para el formato y requisitos adicionales.

### 1f) KDF para Mensaje de Nueva Sesión

#### KDF para ChainKey Inicial

Esto es [NOISE](https://noiseprotocol.org/noise.html) estándar para IK con un nombre de protocolo modificado. Ten en cuenta que usamos el mismo inicializador tanto para el patrón IK (sesiones vinculadas) como para el patrón N (sesiones no vinculadas).

El nombre del protocolo se modifica por dos razones. Primero, para indicar que las claves efímeras están codificadas con Elligator2, y segundo, para indicar que MixHash() se llama antes del segundo mensaje para mezclar el valor de la etiqueta.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF para el Contenido Cifrado de la Sección de Banderas/Clave Estática

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF para la Sección de Carga Útil (con clave estática de Alice)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF para la Sección de Carga Útil (sin clave estática de Alice)

Ten en cuenta que este es un patrón Noise "N", pero usamos el mismo inicializador "IK" que para las sesiones vinculadas.

Los mensajes de Nueva Sesión no pueden identificarse como conteniendo la clave estática de Alice o no hasta que la clave estática sea descifrada e inspeccionada para determinar si contiene solo ceros. Por lo tanto, el receptor debe usar la máquina de estados "IK" para todos los mensajes de Nueva Sesión. Si la clave estática son solo ceros, el patrón de mensaje "ss" debe omitirse.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Formato de respuesta de nueva sesión

Una o más New Session Replies pueden ser enviadas en respuesta a un único mensaje New Session. Cada respuesta está precedida por una etiqueta, que se genera a partir de un TagSet para la sesión.

La New Session Reply está en dos partes. La primera parte es la finalización del handshake Noise IK con una etiqueta antepuesta. La longitud de la primera parte es de 56 bytes. La segunda parte es la carga útil de la fase de datos. La longitud de la segunda parte es de 16 + longitud de la carga útil.

La longitud total es 72 + longitud del payload. Formato cifrado:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
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
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Etiqueta de Sesión

La etiqueta se genera en el Session Tags KDF, como se inicializa en el DH Initialization KDF a continuación. Esto correlaciona la respuesta con la sesión. La Session Key del DH Initialization no se utiliza.

#### Clave Efímera de Respuesta de Nueva Sesión

Clave efímera de Bob. La clave efímera es de 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo retransmisiones.

#### Carga útil

La longitud encriptada es el resto de los datos. La longitud desencriptada es 16 menos que la longitud encriptada. La carga útil generalmente contendrá uno o más bloques Garlic Clove. Consulte la sección de carga útil a continuación para el formato y requisitos adicionales.

#### KDF para Reply TagSet

Se crean una o más etiquetas a partir del TagSet, que se inicializa usando el KDF que se muestra a continuación, utilizando la chainKey del mensaje New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF para Contenidos Cifrados de la Sección de Clave de Respuesta

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF para Contenidos Cifrados de la Sección de Carga Útil

Esto es como el primer mensaje de Sesión Existente, post-división, pero sin una etiqueta separada. Adicionalmente, utilizamos el hash de arriba para vincular la carga útil al mensaje NSR.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Notas

Se pueden enviar múltiples mensajes NSR en respuesta, cada uno con claves efímeras únicas, dependiendo del tamaño de la respuesta.

Alice y Bob deben usar nuevas claves efímeras para cada mensaje NS y NSR.

Alice debe recibir uno de los mensajes NSR de Bob antes de enviar mensajes de Sesión Existente (ES), y Bob debe recibir un mensaje ES de Alice antes de enviar mensajes ES.

El `chainKey` y `k` de la Sección de Carga Útil NSR de Bob se utilizan como entradas para los DH Ratchets ES iniciales (ambas direcciones, ver DH Ratchet KDF).

Bob debe conservar únicamente las Sesiones Existentes para los mensajes ES recibidos de Alice. Cualquier otra sesión entrante y saliente creada (para múltiples NSR) debe ser destruida inmediatamente después de recibir el primer mensaje ES de Alice para una sesión dada.

### 1h) Formato de sesión existente

Etiqueta de sesión (8 bytes) Datos cifrados y MAC (ver sección 3 a continuación)

#### Formato

Cifrado:

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
#### Carga útil

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. Ver la sección de carga útil a continuación para el formato y requisitos.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Formato: claves públicas y privadas de 32 bytes, little-endian.

### 2a) Elligator2

En los handshakes estándar de Noise, los mensajes iniciales del handshake en cada dirección comienzan con claves efímeras que se transmiten en texto plano. Como las claves X25519 válidas son distinguibles de datos aleatorios, un atacante man-in-the-middle puede distinguir estos mensajes de los mensajes de Sesión Existente que comienzan con etiquetas de sesión aleatorias. En [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)), usamos una función XOR de bajo costo usando la clave estática fuera de banda para ofuscar la clave. Sin embargo, el modelo de amenaza aquí es diferente; no queremos permitir que ningún MitM use cualquier medio para confirmar el destino del tráfico, o para distinguir los mensajes iniciales del handshake de los mensajes de Sesión Existente.

Por lo tanto, se utiliza [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) para transformar las claves efímeras en los mensajes New Session y New Session Reply de manera que sean indistinguibles de cadenas aleatorias uniformes.

#### Formato

Claves públicas y privadas de 32 bytes. Las claves codificadas están en formato little endian.

Como se define en [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), las claves codificadas son indistinguibles de 254 bits aleatorios. Necesitamos 256 bits aleatorios (32 bytes). Por lo tanto, la codificación y decodificación se definen de la siguiente manera:

Codificación:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Decodificación:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Notas

Elligator2 duplica en promedio el tiempo de generación de claves, ya que la mitad de las claves privadas resultan en claves públicas que no son adecuadas para codificar con Elligator2. Además, el tiempo de generación de claves no tiene límite con una distribución exponencial, ya que el generador debe seguir intentando hasta encontrar un par de claves adecuado.

Esta sobrecarga puede gestionarse realizando la generación de claves por adelantado, en un hilo separado, para mantener un pool de claves adecuadas.

El generador ejecuta la función ENCODE_ELG2() para determinar la idoneidad. Por lo tanto, el generador debería almacenar el resultado de ENCODE_ELG2() para no tener que calcularlo nuevamente.

Además, las claves no adecuadas pueden añadirse al conjunto de claves utilizadas para [NTCP2](/docs/specs/ntcp2/), donde Elligator2 no se utiliza. Los problemas de seguridad de hacerlo están por determinar.

### 3) AEAD (ChaChaPoly)

AEAD usando ChaCha20 y Poly1305, igual que en [NTCP2](/docs/specs/ntcp2/). Esto corresponde a [RFC-7539](https://tools.ietf.org/html/rfc7539), que también se usa de manera similar en TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Entradas de Nueva Sesión y Respuesta de Nueva Sesión

Entradas a las funciones de cifrado/descifrado para un bloque AEAD en un mensaje de Nueva Sesión:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Entradas de Sesión Existentes

Entradas a las funciones de cifrado/descifrado para un bloque AEAD en un mensaje de Sesión Existente:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Formato Encriptado

Salida de la función de cifrado, entrada de la función de descifrado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Notas

- Dado que ChaCha20 es un cifrado de flujo, los textos planos no necesitan ser rellenados.
  Los bytes adicionales del flujo de claves se descartan.
- La clave para el cifrado (256 bits) se acuerda por medio del
  SHA256 KDF. Los detalles del KDF para cada mensaje están en secciones
  separadas a continuación.
- Los marcos ChaChaPoly son de tamaño conocido ya que están encapsulados en el
  mensaje de datos I2NP.
- Para todos los mensajes, el relleno está dentro del marco de datos autenticados.

#### Manejo de Errores AEAD

Todos los datos recibidos que fallen la verificación AEAD deben ser descartados. No se devuelve ninguna respuesta.

### 4) Ratchets

Todavía usamos session tags, como antes, pero usamos ratchets para generarlas. Los session tags también tenían una opción de regeneración de claves que nunca implementamos. Así que es como un double ratchet pero nunca hicimos el segundo.

Aquí definimos algo similar al Double Ratchet de Signal. Las etiquetas de sesión se generan de manera determinística e idéntica en los lados del receptor y del remitente.

Al usar un ratchet de clave/etiqueta simétrico, eliminamos el uso de memoria para almacenar etiquetas de sesión en el lado del remitente. También eliminamos el consumo de ancho de banda del envío de conjuntos de etiquetas. El uso en el lado del receptor sigue siendo significativo, pero podemos reducirlo aún más ya que reduciremos la etiqueta de sesión de 32 bytes a 8 bytes.

No utilizamos cifrado de encabezados como se especifica (y es opcional) en Signal, en su lugar utilizamos etiquetas de sesión.

Al usar un DH ratchet, logramos el secreto hacia adelante (forward secrecy), que nunca fue implementado en ElGamal/AES+SessionTags.

Nota: La clave pública de un solo uso de Nueva Sesión no es parte del ratchet, su única función es cifrar la clave de ratchet DH inicial de Alice.

#### Números de Mensaje

El Double Ratchet maneja los mensajes perdidos o desordenados incluyendo en cada cabecera de mensaje una etiqueta. El receptor busca el índice de la etiqueta, este es el número de mensaje N. Si el mensaje contiene un bloque de Número de Mensaje con un valor PN, el destinatario puede eliminar cualquier etiqueta superior a ese valor en el conjunto de etiquetas anterior, mientras retiene las etiquetas omitidas del conjunto de etiquetas anterior en caso de que los mensajes omitidos lleguen más tarde.

#### Implementación de Ejemplo

Definimos las siguientes estructuras de datos y funciones para implementar estos ratchets.

TAGSET_ENTRY

Una sola entrada en un TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Una colección de TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) Ratchet DH

Ratchets pero no tan rápido como Signal. Separamos el reconocimiento de la clave recibida de la generación de la nueva clave. En el uso típico, Alice y Bob harán ratchet (dos veces) inmediatamente en una Nueva Sesión, pero no harán ratchet nuevamente.

Ten en cuenta que un ratchet es para una sola dirección, y genera una cadena ratchet de etiqueta de Nueva Sesión / clave de mensaje para esa dirección. Para generar claves para ambas direcciones, tienes que hacer ratchet dos veces.

Avanzas el ratchet cada vez que generas y envías una nueva clave. Avanzas el ratchet cada vez que recibes una nueva clave.

Alice hace un ratchet una vez al crear una sesión saliente no vinculada, no crea una sesión entrante (no vinculada significa que no se puede responder).

Bob hace un ratchet una vez al crear una sesión entrante no vinculada, y no crea una sesión saliente correspondiente (no vinculada significa que no se puede responder).

Alice continúa enviando mensajes New Session (NS) a Bob hasta recibir uno de los mensajes New Session Reply (NSR) de Bob. Luego usa los resultados del KDF de la Sección de Carga Útil del NSR como entradas para los ratchets de sesión (ver DH Ratchet KDF), y comienza a enviar mensajes Existing Session (ES).

Por cada mensaje NS recibido, Bob crea una nueva sesión entrante, utilizando los resultados KDF de la Sección de Carga Útil de respuesta como entradas para el nuevo DH Ratchet ES entrante y saliente.

Para cada respuesta requerida, Bob envía a Alice un mensaje NSR con la respuesta en la carga útil. Es obligatorio que Bob use nuevas claves efímeras para cada NSR.

Bob debe recibir un mensaje ES de Alice en una de las sesiones entrantes, antes de crear y enviar mensajes ES en la sesión saliente correspondiente.

Alice debe usar un temporizador para recibir un mensaje NSR de Bob. Si el temporizador expira, la sesión debe eliminarse.

Para evitar un ataque KCI y/o de agotamiento de recursos, donde un atacante descarta las respuestas NSR de Bob para mantener a Alice enviando mensajes NS, Alice debe evitar iniciar New Sessions hacia Bob después de un cierto número de reintentos debido a la expiración del temporizador.

Alice y Bob realizan cada uno un ratchet DH por cada bloque NextKey recibido.

Alice y Bob generan cada uno nuevos ratchets de conjuntos de etiquetas y dos ratchets de claves simétricas después de cada ratchet DH. Para cada nuevo mensaje ES en una dirección dada, Alice y Bob avanzan los ratchets de etiqueta de sesión y clave simétrica.

La frecuencia de los ratchets DH después del handshake inicial depende de la implementación. Aunque el protocolo establece un límite de 65535 mensajes antes de que se requiera un ratchet, un ratcheting más frecuente (basado en el conteo de mensajes, tiempo transcurrido, o ambos) puede proporcionar seguridad adicional.

Después del KDF de handshake final en las sesiones vinculadas, Bob y Alice deben ejecutar la función Split() de Noise en el CipherState resultante para crear claves simétricas independientes y claves de cadena de etiquetas para las sesiones entrantes y salientes.

##### IDS DE CONJUNTOS DE CLAVES Y ETIQUETAS

Los números de ID de conjuntos de claves y etiquetas se utilizan para identificar claves y conjuntos de etiquetas. Los ID de clave se usan en bloques NextKey para identificar la clave enviada o utilizada. Los ID de conjunto de etiquetas se usan (junto con el número de mensaje) en bloques ACK para identificar el mensaje que se está confirmando. Tanto los ID de clave como los de conjunto de etiquetas se aplican a los conjuntos de etiquetas para una sola dirección. Los números de ID de clave y conjunto de etiquetas deben ser secuenciales.

En los primeros conjuntos de etiquetas utilizados para una sesión en cada dirección, el ID del conjunto de etiquetas es 0. No se han enviado bloques NextKey, por lo que no hay IDs de clave.

Para comenzar un DH ratchet, el remitente transmite un nuevo bloque NextKey con un ID de clave de 0. El receptor responde con un nuevo bloque NextKey con un ID de clave de 0. El remitente entonces comienza a usar un nuevo conjunto de etiquetas con un ID de conjunto de etiquetas de 1.

Los conjuntos de etiquetas posteriores se generan de manera similar. Para todos los conjuntos de etiquetas utilizados después de los intercambios NextKey, el número del conjunto de etiquetas es (1 + ID de clave de Alice + ID de clave de Bob).

Los IDs de conjuntos de claves y etiquetas comienzan en 0 e incrementan secuencialmente. El ID máximo de conjunto de etiquetas es 65535. El ID máximo de clave es 32767. Cuando un conjunto de etiquetas está casi agotado, el remitente del conjunto de etiquetas debe iniciar un intercambio NextKey. Cuando el conjunto de etiquetas 65535 está casi agotado, el remitente del conjunto de etiquetas debe iniciar una nueva sesión enviando un mensaje New Session.

Con un tamaño máximo de mensaje de streaming de 1730, y asumiendo que no hay retransmisiones, la transferencia máxima teórica de datos usando un único conjunto de etiquetas es 1730 * 65536 ~= 108 MB. El máximo real será menor debido a las retransmisiones.

El máximo teórico de transferencia de datos con los 65536 conjuntos de etiquetas disponibles, antes de que la sesión tenga que ser descartada y reemplazada, es 64K * 108 MB ~= 6.9 TB.

##### FLUJO DE MENSAJES DH RATCHET

El siguiente intercambio de claves para un conjunto de etiquetas debe ser iniciado por el remitente de esas etiquetas (el propietario del conjunto de etiquetas salientes). El receptor (propietario del conjunto de etiquetas entrantes) responderá. Para un tráfico HTTP GET típico en la capa de aplicación, Bob enviará más mensajes y hará el ratchet primero al iniciar el intercambio de claves; el diagrama a continuación muestra eso. Cuando Alice hace el ratchet, lo mismo sucede a la inversa.

El primer conjunto de etiquetas utilizado después del handshake NS/NSR es el conjunto de etiquetas 0. Cuando el conjunto de etiquetas 0 está casi agotado, se deben intercambiar nuevas claves en ambas direcciones para crear el conjunto de etiquetas 1. Después de eso, una nueva clave solo se envía en una dirección.

Para crear el conjunto de etiquetas 2, el remitente de la etiqueta envía una nueva clave y el receptor de la etiqueta envía el ID de su clave antigua como confirmación. Ambas partes realizan un DH.

Para crear el conjunto de etiquetas 3, el emisor de etiquetas envía el ID de su clave antigua y solicita una nueva clave del receptor de etiquetas. Ambas partes realizan un DH.

Los conjuntos de etiquetas posteriores se generan como para los conjuntos de etiquetas 2 y 3. El número del conjunto de etiquetas es (1 + ID de clave del remitente + ID de clave del receptor).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
Después de que el ratchet DH esté completo para un tagset saliente, y se cree un nuevo tagset saliente, debe usarse inmediatamente, y el tagset saliente anterior puede eliminarse.

Después de que se complete el ratchet DH para un tagset entrante, y se cree un nuevo tagset entrante, el receptor debe escuchar tags en ambos tagsets, y eliminar el tagset antiguo después de un corto tiempo, aproximadamente 3 minutos.

El resumen de la progresión del conjunto de etiquetas y el ID de clave se encuentra en la tabla a continuación. * indica que se genera una nueva clave.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Los números de ID de conjuntos de claves y etiquetas deben ser secuenciales.

##### KDF DE INICIALIZACIÓN DH

Esta es la definición de DH_INITIALIZE(rootKey, k) para una sola dirección. Crea un tagset y una "clave raíz siguiente" que se usará para un ratchet DH posterior si es necesario.

Utilizamos la inicialización DH en tres lugares. Primero, la utilizamos para generar un conjunto de etiquetas para las Respuestas de Nueva Sesión. Segundo, la utilizamos para generar dos conjuntos de etiquetas, uno para cada dirección, para usar en los mensajes de Sesión Existente. Por último, la utilizamos después de un DH Ratchet para generar un nuevo conjunto de etiquetas en una sola dirección para mensajes adicionales de Sesión Existente.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Esto se usa después de que se intercambien nuevas claves DH en bloques NextKey, antes de que se agote un conjunto de etiquetas.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Trinquete de Etiqueta de Sesión

Ratchets para cada mensaje, como en Signal. El ratchet de etiqueta de sesión está sincronizado con el ratchet de clave simétrica, pero el ratchet de clave del receptor puede "quedarse atrás" para ahorrar memoria.

El transmisor avanza el trinquete una vez por cada mensaje transmitido. No se deben almacenar etiquetas adicionales. El transmisor también debe mantener un contador para 'N', el número de mensaje del mensaje en la cadena actual. El valor 'N' se incluye en el mensaje enviado. Consulte la definición del bloque Message Number.

El receptor debe avanzar el ratchet por el tamaño máximo de ventana y almacenar las etiquetas en un "conjunto de etiquetas", que está asociado con la sesión. Una vez recibida, la etiqueta almacenada puede ser descartada, y si no hay etiquetas anteriores no recibidas, la ventana puede avanzarse. El receptor debe mantener el valor 'N' asociado con cada etiqueta de sesión, y verificar que el número en el mensaje enviado coincida con este valor. Ver la definición del bloque Message Number.

##### KDF

Esta es la definición de RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Trinquete de Clave Simétrica

Ratchets para cada mensaje, como en Signal. Cada clave simétrica tiene un número de mensaje asociado y una etiqueta de sesión. El ratchet de clave de sesión está sincronizado con el ratchet de etiqueta simétrica, pero el ratchet de clave del receptor puede "quedarse atrás" para ahorrar memoria.

Los trinquetes de transmisión avanzan una vez por cada mensaje transmitido. No es necesario almacenar claves adicionales.

Cuando el receptor recibe una etiqueta de sesión, si aún no ha avanzado el ratchet de clave simétrica hasta la clave asociada, debe "ponerse al día" con la clave asociada. El receptor probablemente almacenará en caché las claves para cualquier etiqueta anterior que aún no haya sido recibida. Una vez recibida, la clave almacenada puede descartarse, y si no hay etiquetas anteriores no recibidas, la ventana puede avanzarse.

Por eficiencia, los ratchets de la session tag y la clave simétrica son separados para que el ratchet de session tag pueda adelantarse al ratchet de clave simétrica. Esto también proporciona seguridad adicional, ya que las session tags salen por el cable.

##### KDF

Esta es la definición de RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Carga útil

Esto reemplaza el formato de sección AES definido en la especificación ElGamal/AES+SessionTags.

Esto utiliza el mismo formato de bloque definido en la especificación [NTCP2](/docs/specs/ntcp2/). Los tipos de bloques individuales se definen de manera diferente.

Existen preocupaciones de que alentar a los implementadores a compartir código puede llevar a problemas de análisis sintáctico. Los implementadores deben considerar cuidadosamente los beneficios y riesgos de compartir código, y asegurarse de que las reglas de ordenamiento y bloques válidos sean diferentes para los dos contextos.

#### Sección de Carga Útil Datos descifrados

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. Se admiten todos los tipos de bloques. El contenido típico incluye los siguientes bloques:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Datos sin cifrar

Hay cero o más bloques en el frame cifrado. Cada bloque contiene un identificador de un byte, una longitud de dos bytes y cero o más bytes de datos.

Por extensibilidad, los receptores DEBEN ignorar los bloques con números de tipo desconocidos, y tratarlos como relleno.

Los datos cifrados tienen un máximo de 65535 bytes, incluyendo un encabezado de autenticación de 16 bytes, por lo que los datos sin cifrar tienen un máximo de 65519 bytes.

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
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
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

En el mensaje New Session, el bloque DateTime es obligatorio y debe ser el primer bloque.

Otros bloques permitidos:

- Garlic Clove (tipo 11)
- Opciones (tipo 5)
- Relleno (tipo 254)

En el mensaje New Session Reply, no se requieren bloques.

Otros bloques permitidos:

- Garlic Clove (tipo 11)
- Options (tipo 5)
- Padding (tipo 254)

No se permiten otros bloques. El relleno, si está presente, debe ser el último bloque.

En el mensaje Existing Session, no se requieren bloques, y el orden no está especificado, excepto por los siguientes requisitos:

Termination, si está presente, debe ser el último bloque excepto por Padding. Padding, si está presente, debe ser el último bloque.

Puede haber múltiples bloques Garlic Clove en un solo frame. Puede haber hasta dos bloques Next Key en un solo frame. No se permiten múltiples bloques Padding en un solo frame. Otros tipos de bloques probablemente no tendrán múltiples bloques en un solo frame, pero no está prohibido.

#### FechaHora

Una expiración. Ayuda en la prevención de ataques de repetición. Bob debe validar que el mensaje sea reciente, usando esta marca de tiempo. Bob debe implementar un filtro Bloom u otro mecanismo para prevenir ataques de repetición, si el tiempo es válido. Bob también puede usar una verificación de detección de repetición anterior para una clave efímera duplicada (ya sea antes o después de la decodificación Elligator2) para detectar y descartar mensajes NS duplicados recientes antes del descifrado. Generalmente incluido solo en mensajes New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Un solo Garlic Clove descifrado según se especifica en [I2NP](/docs/specs/i2np/), con modificaciones para eliminar campos que no se usan o son redundantes. Advertencia: Este formato es significativamente diferente al de ElGamal/AES. Cada clove es un bloque de carga útil separado. Los Garlic Cloves no pueden fragmentarse entre bloques o entre marcos ChaChaPoly.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Notas:

- Los implementadores deben asegurar que al leer un bloque, los datos malformados o
  maliciosos no causen que las lecturas se desborden hacia el siguiente bloque.
- El formato Clove Set especificado en [I2NP](/docs/specs/i2np/) no se
  utiliza. Cada clove está contenido en su propio bloque.
- El encabezado del mensaje I2NP tiene 9 bytes, con un formato idéntico al
  usado en [NTCP2](/docs/specs/ntcp2/).
- El Certificate, Message ID y Expiration de la definición de Garlic Message
  en [I2NP](/docs/specs/i2np/) no están incluidos.
- El Certificate, Clove ID y Expiration de la definición de Garlic Clove
  en [I2NP](/docs/specs/i2np/) no están incluidos.

#### Terminación

La implementación es opcional. Descartar la sesión. Este debe ser el último bloque sin relleno en el marco. No se enviarán más mensajes en esta sesión.

No permitido en NS o NSR. Solo incluido en mensajes de Sesión Existente.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Opciones

NO IMPLEMENTADO, para estudio posterior. Pasar opciones actualizadas. Las opciones incluyen varios parámetros para la sesión. Ver la sección Análisis de Longitud de Etiquetas de Sesión a continuación para más información.

El bloque de opciones puede tener longitud variable, ya que more_options puede estar presente.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

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

more_options :: Format undefined, for future use
```
SOTW es la recomendación del remitente al receptor para la ventana de etiquetas entrantes del receptor (el máximo lookahead). RITW es la declaración del remitente de la ventana de etiquetas entrantes (máximo lookahead) que planea usar. Cada lado entonces establece o ajusta el lookahead basándose en algún mínimo o máximo u otro cálculo.

Notas:

- Se espera que nunca se requiera soporte para longitud de etiqueta de sesión no predeterminada.
- La ventana de etiqueta es MAX_SKIP en la documentación de Signal.

Problemas:

- La negociación de opciones está por determinar.
- Los valores por defecto están por determinar.
- Las opciones de relleno y retraso se copian de NTCP2, pero esas opciones
  no han sido completamente implementadas o estudiadas allí.

#### Números de Mensaje

La implementación es opcional. La longitud (número de mensajes enviados) en el conjunto de etiquetas anterior (PN). El receptor puede eliminar inmediatamente las etiquetas superiores a PN del conjunto de etiquetas anterior. El receptor puede hacer expirar las etiquetas menores o iguales a PN del conjunto de etiquetas anterior después de un tiempo breve (por ejemplo, 2 minutos).

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Notas:

- El PN máximo es 65535.
- Las definiciones de PN son iguales a la definición de Signal, menos uno.
  Esto es similar a lo que hace Signal, pero en Signal, PN y N están en
  el encabezado. Aquí, están en el cuerpo del mensaje cifrado.
- No envíes este bloque en el conjunto de etiquetas 0, porque no había un conjunto
  de etiquetas anterior.

#### Siguiente Clave Pública de DH Ratchet

La siguiente clave de ratchet DH está en la carga útil, y es opcional. No hacemos ratchet cada vez. (Esto es diferente que en signal, donde está en el encabezado, y se envía cada vez)

Para el primer ratchet, Key ID = 0.

No permitido en NS o NSR. Solo incluido en mensajes de Sesión Existente.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Notas:

- El ID de clave es un contador incremental para la clave local utilizada para ese conjunto de etiquetas, comenzando en 0.
- El ID no debe cambiar a menos que la clave cambie.
- Puede que no sea estrictamente necesario, pero es útil para depuración. Signal no utiliza un ID de clave.
- El ID de clave máximo es 32767.
- En el caso raro de que los conjuntos de etiquetas en ambas direcciones estén haciendo ratcheting al mismo tiempo, un frame contendrá dos bloques Next Key, uno para la clave forward y uno para la clave reverse.
- Los números de ID de clave y conjunto de etiquetas deben ser secuenciales.
- Ver la sección DH Ratchet arriba para más detalles.

#### Confirmación

Esto solo se envía si se recibió un bloque de solicitud de confirmación. Pueden estar presentes múltiples confirmaciones para confirmar múltiples mensajes.

No permitido en NS o NSR. Solo incluido en mensajes de Sesión Existente.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Notas:

- El ID del conjunto de etiquetas y N identifican de forma única el mensaje que está siendo confirmado.
- En los primeros conjuntos de etiquetas utilizados para una sesión en cada dirección, el ID del conjunto de etiquetas es 0.
- No se han enviado bloques NextKey, por lo que no hay IDs de clave.
- Para todos los conjuntos de etiquetas utilizados después de los intercambios NextKey, el número del conjunto de etiquetas es (1 + ID de clave de Alice + ID de clave de Bob).

#### Solicitud de Confirmación

Solicitar un ack in-band. Para reemplazar el Mensaje DeliveryStatus out-of-band en el Garlic Clove.

Si se solicita un ack explícito, el ID del tagset actual y el número de mensaje (N) se devuelven en un bloque ack.

No permitido en NS o NSR. Solo incluido en mensajes de Sesión Existente.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Relleno

Todo el relleno está dentro de los marcos AEAD. TODO El relleno dentro de AEAD debería adherirse aproximadamente a los parámetros negociados. TODO Alice envió sus parámetros mín/máx de tx/rx solicitados en el mensaje NS. TODO Bob envió sus parámetros mín/máx de tx/rx solicitados en el mensaje NSR. Las opciones actualizadas pueden enviarse durante la fase de datos. Ver información del bloque de opciones arriba.

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
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Notas:

- El relleno de ceros está bien, ya que será encriptado.
- Las estrategias de relleno están por determinar.
- Se permiten tramas que contengan solo relleno.
- El relleno por defecto es de 0-15 bytes.
- Ver bloque de opciones para la negociación del parámetro de relleno
- Ver bloque de opciones para los parámetros de relleno mín/máx
- La respuesta del router ante la violación del relleno negociado depende de la implementación.

#### Otros tipos de bloques

Las implementaciones deberían ignorar los tipos de bloque desconocidos para mantener compatibilidad hacia adelante.

#### Trabajo futuro

- La longitud del relleno debe decidirse por mensaje individual y
  estimaciones de la distribución de longitud, o se deben agregar
  retrasos aleatorios. Estas contramedidas deben incluirse para resistir
  DPI, ya que los tamaños de mensaje revelarían que el tráfico I2P está
  siendo transportado por el protocolo de transporte. El esquema exacto
  de relleno es un área de trabajo futuro, el Apéndice A proporciona
  más información sobre el tema.

## Patrones de Uso Típicos

### HTTP GET

Este es el caso de uso más típico, y la mayoría de los casos de uso de streaming no-HTTP serán idénticos a este caso de uso también. Se envía un pequeño mensaje inicial, sigue una respuesta, y se envían mensajes adicionales en ambas direcciones.

Un HTTP GET generalmente cabe en un solo mensaje I2NP. Alice envía una pequeña solicitud con un único mensaje Session nuevo, incluyendo un leaseset de respuesta. Alice incluye un ratchet inmediato a la nueva clave. Incluye firma para vincular al destino. No se solicita confirmación.

Bob hace ratchet inmediatamente.

Alice hace ratchet inmediatamente.

Continúa con esas sesiones.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice tiene tres opciones:

1)  Enviar solo el primer mensaje (tamaño de ventana = 1), como en HTTP GET. No

    recommended.
2)  Enviar hasta la ventana de streaming, pero usando la misma codificación Elligator2

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Implementación recomendada. Enviar hasta la ventana de streaming, pero usando un

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Flujo de mensajes de la Opción 3:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Datagrama Replicable

Un solo mensaje, con una sola respuesta esperada. Se pueden enviar mensajes o respuestas adicionales.

Similar a HTTP GET, pero con opciones más pequeñas para el tamaño de ventana y tiempo de vida de la etiqueta de sesión. Tal vez no solicitar un ratchet.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Múltiples Datagramas Raw

Múltiples mensajes anónimos, sin esperar respuestas.

En este escenario, Alice solicita una sesión, pero sin vinculación. Se envía un mensaje de nueva sesión. No se incluye un LS de respuesta. Se incluye un DSM de respuesta (este es el único caso de uso que requiere DSMs incluidos). No se incluye una clave siguiente. No se solicita respuesta o ratchet. No se envía ratchet. Las opciones establecen la ventana de etiquetas de sesión en cero.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Datagrama Simple en Bruto

Un solo mensaje anónimo, sin respuesta esperada.

Se envía un mensaje de una sola vez. No se incluyen LS de respuesta o DSM. No se incluye la siguiente clave. No se solicita respuesta o ratchet. No se envía ratchet. Las opciones establecen la ventana de etiquetas de sesión en cero.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Sesiones de Larga Duración

Las sesiones de larga duración pueden realizar ratchet, o solicitar un ratchet, en cualquier momento, para mantener el secreto hacia adelante desde ese punto en el tiempo. Las sesiones deben realizar ratchet cuando se acercan al límite de mensajes enviados por sesión (65535).

## Consideraciones de Implementación

### Defensa

Al igual que con el protocolo existente ElGamal/AES+SessionTag, las implementaciones deben limitar el almacenamiento de etiquetas de sesión y proteger contra ataques de agotamiento de memoria.

Algunas estrategias recomendadas incluyen:

- Límite estricto en el número de etiquetas de sesión almacenadas
- Expiración agresiva de sesiones entrantes inactivas cuando hay presión
  de memoria
- Límite en el número de sesiones entrantes vinculadas a un único
  destino remoto
- Reducción adaptativa de la ventana de etiquetas de sesión y eliminación de etiquetas antiguas no utilizadas cuando hay presión de memoria
- Rechazo a hacer ratchet cuando se solicita, si hay presión de memoria

### Parámetros

Parámetros y tiempos de espera recomendados:

- Tamaño del tagset NSR: 12 tsmin y tsmax
- Tamaño del tagset ES 0: tsmin 24, tsmax 160
- Tamaño del tagset ES (1+): 160 tsmin y tsmax
- Tiempo de espera del tagset NSR: 3 minutos para el receptor
- Tiempo de espera del tagset ES: 8 minutos para el emisor, 10 minutos para el receptor
- Eliminar tagset ES anterior después de: 3 minutos
- Anticipación del tagset del tag N: min(tsmax, tsmin + N/4)
- Recorte del tagset detrás del tag N: min(tsmax, tsmin + N/4) / 2
- Enviar siguiente clave en el tag: 4096
- Enviar siguiente clave después del tiempo de vida del tagset: Por determinar
- Reemplazar sesión si NS recibido después de: 3 minutos
- Desviación máxima del reloj: -5 minutos a +2 minutos
- Duración del filtro de repetición NS: 5 minutos
- Tamaño del padding: 0-15 bytes (otras estrategias por determinar)

### Clasificación

A continuación se presentan recomendaciones para clasificar los mensajes entrantes.

#### Solo X25519

En un tunnel que se usa exclusivamente con este protocolo, realizar la identificación como se hace actualmente con ElGamal/AES+SessionTags:

Primero, trata los datos iniciales como una etiqueta de sesión, y busca la etiqueta de sesión. Si se encuentra, descifra usando los datos almacenados asociados con esa etiqueta de sesión.

Si no se encuentra, trata los datos iniciales como una clave pública DH y un nonce. Realiza una operación DH y el KDF especificado, e intenta descifrar los datos restantes.

#### X25519 Compartido con ElGamal/AES+SessionTags

En un tunnel que admite tanto este protocolo como ElGamal/AES+SessionTags, clasifica los mensajes entrantes de la siguiente manera:

Debido a un defecto en la especificación ElGamal/AES+SessionTags, el bloque AES no se rellena a una longitud aleatoria no-módulo-16. Por lo tanto, la longitud de los mensajes de Sesión Existente módulo 16 es siempre 0, y la longitud de los mensajes de Nueva Sesión módulo 16 es siempre 2 (ya que el bloque ElGamal tiene 514 bytes de longitud).

Si el módulo de longitud 16 no es 0 o 2, trata los datos iniciales como un session tag, y busca el session tag. Si se encuentra, descifra usando los datos almacenados asociados con ese session tag.

Si no se encuentra, y la longitud mod 16 no es 0 o 2, trata los datos iniciales como una clave pública DH y nonce. Realiza una operación DH y el KDF especificado, e intenta descifrar los datos restantes. (basándose en la mezcla relativa de tráfico y los costos relativos de las operaciones DH X25519 y ElGamal, este paso puede realizarse al final en su lugar)

De lo contrario, si la longitud mod 16 es 0, trata los datos iniciales como una etiqueta de sesión ElGamal/AES, y busca la etiqueta de sesión. Si se encuentra, descifra usando los datos almacenados asociados con esa etiqueta de sesión.

Si no se encuentra, y los datos tienen al menos 642 (514 + 128) bytes de longitud, y la longitud mod 16 es 2, trata los datos iniciales como un bloque ElGamal. Intenta descifrar los datos restantes.

Ten en cuenta que si la especificación ElGamal/AES+SessionTag se actualiza para permitir padding no-mod-16, las cosas tendrán que hacerse de manera diferente.

### Retransmisiones y Transiciones de Estado

La capa ratchet no realiza retransmisiones, y con dos excepciones, no utiliza temporizadores para las transmisiones. Los temporizadores también son necesarios para el timeout del tagset.

Los temporizadores de transmisión se usan solo para enviar NSR y para responder con un ES cuando un ES recibido contiene una solicitud de ACK. El tiempo de espera recomendado es de un segundo. En casi todos los casos, la capa superior (datagrama o streaming) responderá, forzando un NSR o ES, y el temporizador puede ser cancelado. Si el temporizador se dispara, enviar una carga útil vacía con el NSR o ES.

#### Respuestas de la capa Ratchet

Las implementaciones iniciales dependen del tráfico bidireccional en las capas superiores. Es decir, las implementaciones asumen que pronto se transmitirá tráfico en la dirección opuesta, lo que forzará cualquier respuesta requerida en la capa ECIES.

Sin embargo, cierto tráfico puede ser unidireccional o de muy poco ancho de banda, de tal manera que no hay tráfico de capas superiores para generar una respuesta oportuna.

La recepción de mensajes NS y NSR requiere una respuesta; la recepción de bloques ACK Request y Next Key también requiere una respuesta.

Las implementaciones deberían iniciar un temporizador cuando se reciba uno de estos mensajes que requiere una respuesta, y generar una respuesta "vacía" (sin bloque Garlic Clove) en la capa ECIES si no se envía tráfico inverso en un período corto de tiempo (por ejemplo, 1 segundo).

También puede ser apropiado un tiempo de espera aún más corto para las respuestas a los mensajes NS y NSR, para cambiar el tráfico a los mensajes ES eficientes tan pronto como sea posible.

#### Vinculación NS Para NSR

En la capa ratchet, como Bob, Alice solo es conocida por su clave estática. El mensaje NS está autenticado (autenticación del remitente [Noise](https://noiseprotocol.org/noise.html) IK 1). Sin embargo, esto no es suficiente para que la capa ratchet pueda enviar algo a Alice, ya que el enrutamiento de red requiere un Destination completo.

Antes de que el NSR pueda ser enviado, el Destination completo de Alice debe ser descubierto ya sea por la capa ratchet o por un protocolo de capa superior que permita respuesta, ya sea [Datagrams](/docs/specs/datagrams/) con respuesta o [Streaming](/docs/specs/streaming/). Después de encontrar el Leaseset para ese Destination, ese Leaseset contendrá la misma clave estática que se encuentra en el NS.

Típicamente, la capa superior responderá, forzando una búsqueda en la base de datos de red del Leaseset de Alice por el Hash de Destino de Alice. Ese Leaseset casi siempre se encontrará localmente, porque el NS contenía un bloque Garlic Clove, que contenía un mensaje Database Store, que contenía el Leaseset de Alice.

Para que Bob esté preparado para enviar un NSR de capa ratchet, y para vincular la sesión pendiente al Destination de Alice, Bob debería "capturar" el Destination mientras procesa la carga útil NS. Si se encuentra un mensaje Database Store que contiene un Leaseset con una clave que coincide con la clave estática en el NS, la sesión pendiente ahora está vinculada a ese Destination, y Bob sabe dónde enviar cualquier NSR si expira el temporizador de respuesta. Esta es la implementación recomendada.

Un diseño alternativo es mantener una caché o base de datos donde la clave estática se mapee a un Destination. La seguridad y practicidad de este enfoque es un tema para estudios futuros.

Ni esta especificación ni otras requieren estrictamente que cada NS contenga el Leaseset de Alice. Sin embargo, en la práctica, debería hacerlo. El tiempo de espera recomendado del remitente del tagset ES (8 minutos) es más corto que el tiempo de espera máximo del Leaseset (10 minutos), por lo que podría haber una pequeña ventana donde la sesión anterior ha expirado, Alice piensa que Bob todavía tiene su Leaseset válido, y no envía un nuevo Leaseset con el nuevo NS. Este es un tema para estudio posterior.

#### Múltiples Mensajes NS

Si no se recibe una respuesta NSR antes de que la capa superior (datagrama o streaming) envíe más datos, posiblemente como una retransmisión, Alice debe componer un nuevo NS, utilizando una nueva clave efímera. No reutilices la clave efímera de ningún NS anterior. Alice debe mantener el estado de handshake adicional y el tagset de recepción derivado, para recibir mensajes NSR en respuesta a cualquier NSR que se haya enviado.

Las implementaciones pueden limitar el número total de mensajes NS enviados, o la tasa de envío de mensajes NS, ya sea poniendo en cola o descartando mensajes de capas superiores antes de que sean enviados.

En ciertas situaciones, cuando está bajo alta carga, o bajo ciertos escenarios de ataque, puede ser apropiado para Bob poner en cola, descartar o limitar los mensajes NS aparentes sin intentar descifrarlos, para evitar un ataque de agotamiento de recursos.

Para cada NS recibido, Bob genera un tagset saliente NSR, envía un NSR, realiza un split(), y genera los tagsets ES entrantes y salientes. Sin embargo, Bob no envía ningún mensaje ES hasta que se reciba el primer mensaje ES en el tagset entrante correspondiente. Después de eso, Bob puede descartar todos los estados de handshake y tagsets para cualquier otro NS recibido o NSR enviado, o permitir que expiren en breve. No use tagsets NSR para mensajes ES.

Es un tema para estudio futuro si Bob puede elegir enviar especulativamente mensajes ES inmediatamente después del NSR, incluso antes de recibir el primer ES de Alice. En ciertos escenarios y patrones de tráfico, esto podría ahorrar un ancho de banda y CPU sustanciales. Esta estrategia puede basarse en heurísticas como patrones de tráfico, porcentaje de ESs recibidos en el tagset de la primera sesión, u otros datos.

#### Múltiples Mensajes NSR

Para cada mensaje NS recibido, hasta que se reciba un mensaje ES, Bob debe responder con un nuevo NSR, ya sea debido a que se envía tráfico de capa superior, o por la expiración del temporizador de envío NSR.

Cada NSR utiliza el estado de handshake y el conjunto de etiquetas correspondiente al NS entrante. Bob debe mantener el estado de handshake y el conjunto de etiquetas para todos los mensajes NS recibidos, hasta que se reciba un mensaje ES.

Las implementaciones pueden limitar el número total de mensajes NSR enviados, o la tasa de envío de mensajes NSR, ya sea poniendo en cola o descartando mensajes de capas superiores antes de que sean enviados. Estos pueden limitarse tanto cuando son causados por mensajes NS entrantes, como por tráfico saliente adicional de capas superiores.

En ciertas situaciones, cuando está bajo alta carga, o bajo ciertos escenarios de ataque, puede ser apropiado para Alice poner en cola, descartar, o limitar mensajes NSR sin intentar descifrarlos, para evitar un ataque de agotamiento de recursos. Estos límites pueden ser totales a través de todas las sesiones, por sesión, o ambos.

Una vez que Alice recibe un NSR, Alice hace un split() para derivar las claves de sesión ES. Alice debería establecer un temporizador y enviar un mensaje ES vacío si la capa superior no envía ningún tráfico, típicamente dentro de un segundo.

Los otros conjuntos de etiquetas NSR entrantes pueden ser eliminados pronto o se les puede permitir expirar, pero Alice debería conservarlos por un corto tiempo, para descifrar cualquier otro mensaje NSR que sea recibido.

### Prevención de Reproducción

Bob debe implementar un filtro Bloom u otro mecanismo para prevenir ataques de repetición NS, si el DateTime incluido es reciente, y rechazar mensajes NS donde el DateTime es demasiado antiguo. Bob también puede usar una verificación de detección de repetición anterior para una clave efímera duplicada (ya sea antes o después de la decodificación Elligator2) para detectar y descartar mensajes NS duplicados recientes antes del descifrado.

Los mensajes NSR y ES tienen prevención de repetición inherente porque la etiqueta de sesión es de un solo uso.

Los mensajes garlic también tienen prevención de reproducción si el router implementa un filtro Bloom a nivel de router basado en el ID del mensaje I2NP.

## Cambios Relacionados

Consultas de base de datos desde destinos ECIES: Ver [Prop154](/proposals/154-ratchet/), ahora incorporada en [I2NP](/docs/specs/i2np/) para la versión 0.9.46.

Esta especificación requiere soporte LS2 para publicar la clave pública X25519 con el leaseset. No se requieren cambios a las especificaciones LS2 en [I2NP](/docs/specs/i2np/). Todo el soporte fue diseñado, especificado e implementado en [Prop123](/proposals/123-new-netdb-entries/) implementado en 0.9.38.

Esta especificación requiere que se establezca una propiedad en las opciones I2CP para ser habilitada. Todo el soporte fue diseñado, especificado e implementado en [Prop123](/proposals/123-new-netdb-entries/) implementado en la versión 0.9.38.

La opción requerida para habilitar ECIES es una única propiedad I2CP para I2CP, BOB, SAM, o i2ptunnel.

Los valores típicos son i2cp.leaseSetEncType=4 solo para ECIES, o i2cp.leaseSetEncType=4,0 para claves duales ECIES y ElGamal.

## Compatibilidad

Cualquier router que soporte LS2 con claves duales (0.9.38 o superior) debería soportar conexión a destinos con claves duales.

Los destinos solo ECIES requieren que la mayoría de los floodfills se actualicen a la versión 0.9.46 para obtener respuestas de búsqueda cifradas. Ver [Prop154](/proposals/154-ratchet/).

Los destinos exclusivamente ECIES solo pueden conectarse con otros destinos que sean exclusivamente ECIES o de clave dual.

## Referencias

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagramas](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Ver también [artículo de Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) y código OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
