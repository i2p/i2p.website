---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Nota

Implementación y pruebas de red en progreso. Sujeto a revisiones menores. Consulte [SPEC](/docs/specs/ecies/) para la especificación oficial.

Las siguientes características no están implementadas a partir de la versión 0.9.46:

- Bloques MessageNumbers, Options y Termination
- Respuestas a nivel de protocolo
- Clave estática cero
- Multidifusión

## Descripción general

Esta es una propuesta para el primer nuevo tipo de cifrado de extremo a extremo desde el comienzo de I2P, para reemplazar ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

Se basa en trabajos previos de la siguiente manera:

- Especificación de estructuras comunes [Common Structures](/docs/specs/common-structures/)
- Especificación de [I2NP](/docs/specs/i2np/) incluyendo LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) descripción general de criptografía asimétrica nueva
- Descripción general de criptografía de bajo nivel [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Propuesta 111](/proposals/111-ntcp-2/)
- 123 Nuevas entradas netDB
- 142 Nueva plantilla de criptografía
- Protocolo [Noise](https://noiseprotocol.org/noise.html)
- Algoritmo double ratchet de [Signal](https://signal.org/docs/)

El objetivo es admitir cifrado nuevo para la comunicación extremo a extremo, de destino a destino.

El diseño utilizará un handshake de Noise y una fase de datos que incorpora el double ratchet de Signal.

Todas las referencias a Signal y Noise en esta propuesta son únicamente para información de contexto. No se requiere conocimiento de los protocolos Signal y Noise para entender o implementar esta propuesta.

### Current ElGamal Uses

Como repaso, las claves públicas ElGamal de 256 bytes pueden encontrarse en las siguientes estructuras de datos. Consulte la especificación de estructuras comunes.

- En una Router Identity
  Esta es la clave de cifrado del router.

- En un Destination
  La clave pública del destination se usaba para el cifrado i2cp-a-i2cp anterior
  que fue deshabilitado en la versión 0.6, actualmente no se usa excepto para
  el IV para el cifrado de LeaseSet, que está obsoleto.
  En su lugar se usa la clave pública en el LeaseSet.

- En un LeaseSet
  Esta es la clave de cifrado del destino.

- En un LS2
  Esta es la clave de cifrado del destino.

### EncTypes in Key Certs

Como repaso, agregamos soporte para tipos de cifrado cuando agregamos soporte para tipos de firma. El campo de tipo de cifrado siempre es cero, tanto en Destinations como en RouterIdentities. Si alguna vez cambiar eso está por determinar. Consulta la especificación de estructuras comunes [Common Structures](/docs/specs/common-structures/).

### Usos Actuales de ElGamal

Como repaso, usamos ElGamal para:

1) Mensajes de construcción de tunnel (la clave está en RouterIdentity)    El reemplazo no está cubierto en esta propuesta.    Ver propuesta 152 [Proposal 152](/proposals/152-ecies-tunnels).

2) Cifrado router-a-router de netdb y otros mensajes I2NP (La clave está en RouterIdentity)    Depende de esta propuesta.    Requiere una propuesta para 1) también, o poner la clave en las opciones del RI.

3) Cliente Extremo a extremo ElGamal+AES/SessionTag (la clave está en leaseSet, la clave de Destination no se usa)    El reemplazo SÍ está cubierto en esta propuesta.

4) DH efímero para NTCP1 y SSU    El reemplazo no está cubierto en esta propuesta.    Ver propuesta 111 para NTCP2.    No hay propuesta actual para SSU2.

### EncTypes en Key Certs

- Compatible hacia atrás
- Requiere y se basa en LS2 (propuesta 123)
- Aprovechar nueva criptografía o primitivas añadidas para NTCP2 (propuesta 111)
- No requiere nueva criptografía o primitivas para el soporte
- Mantener el desacoplamiento de criptografía y firmado; soportar todas las versiones actuales y futuras
- Habilitar nueva criptografía para destinos
- Habilitar nueva criptografía para routers, pero solo para mensajes garlic - la construcción de túneles sería una propuesta separada
- No romper nada que dependa de hashes de destino binarios de 32 bytes, ej. bittorrent
- Mantener entrega de mensajes 0-RTT usando DH efímero-estático
- No requiere almacenamiento en buffer / cola de mensajes en esta capa de protocolo; continuar soportando entrega ilimitada de mensajes en ambas direcciones sin esperar una respuesta
- Actualizar a DH efímero-efímero después de 1 RTT
- Mantener manejo de mensajes fuera de orden
- Mantener seguridad de 256 bits
- Añadir forward secrecy
- Añadir autenticación (AEAD)
- Mucho más eficiente en CPU que ElGamal
- No depender de Java jbigi para hacer DH eficiente
- Minimizar operaciones DH
- Mucho más eficiente en ancho de banda que ElGamal (bloque ElGamal de 514 bytes)
- Soportar criptografía nueva y antigua en el mismo túnel si se desea
- El destinatario puede distinguir eficientemente nueva de antigua criptografía llegando por el mismo túnel
- Otros no pueden distinguir criptografía nueva de antigua o futura
- Eliminar clasificación de longitud de sesión nueva vs. existente (soportar padding)
- No requiere nuevos mensajes I2NP
- Reemplazar checksum SHA-256 en payload AES con AEAD
- Soportar vinculación de sesiones de transmisión y recepción para que los acknowledgements puedan ocurrir dentro del protocolo, en lugar de únicamente fuera de banda. Esto también permitirá que las respuestas tengan forward secrecy inmediatamente.
- Habilitar cifrado extremo a extremo de ciertos mensajes (almacenes RouterInfo) que actualmente no ciframos debido a la sobrecarga de CPU.
- No cambiar el formato del Mensaje I2NP Garlic o las Instrucciones de Entrega de Mensaje Garlic.
- Eliminar campos no utilizados o redundantes en los formatos Garlic Clove Set y Clove.

Elimina varios problemas con las etiquetas de sesión, incluyendo:

- Incapacidad de usar AES hasta la primera respuesta
- Falta de confiabilidad y bloqueos si se asume la entrega de etiquetas
- Ineficiente en ancho de banda, especialmente en la primera entrega
- Gran ineficiencia de espacio para almacenar etiquetas
- Enorme sobrecarga de ancho de banda para entregar etiquetas
- Altamente complejo, difícil de implementar
- Difícil de ajustar para varios casos de uso
  (streaming vs. datagramas, servidor vs. cliente, ancho de banda alto vs. bajo)
- Vulnerabilidades de agotamiento de memoria debido a la entrega de etiquetas

### Usos de Criptografía Asimétrica

- Cambios en el formato LS2 (la propuesta 123 está completada)
- Nuevo algoritmo de rotación DHT o generación aleatoria compartida
- Nuevo cifrado para la construcción de túneles.
  Ver propuesta 152 [Proposal 152](/proposals/152-ecies-tunnels).
- Nuevo cifrado para el cifrado de capa de túnel.
  Ver propuesta 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- Métodos de cifrado, transmisión y recepción de mensajes I2NP DLM / DSM / DSRM.
  Sin cambios.
- No se admite comunicación de LS1-a-LS2 o ElGamal/AES-a-esta-propuesta.
  Esta propuesta es un protocolo bidireccional.
  Los destinos pueden manejar la compatibilidad hacia atrás publicando dos leasesets
  usando los mismos túneles, o poniendo ambos tipos de cifrado en el LS2.
- Cambios en el modelo de amenazas
- Los detalles de implementación no se discuten aquí y se dejan a cada proyecto.
- (Optimista) Agregar extensiones o ganchos para soportar multicast

### Objetivos

ElGamal/AES+SessionTag ha sido nuestro único protocolo extremo a extremo durante aproximadamente 15 años, esencialmente sin modificaciones al protocolo. Ahora existen primitivos criptográficos que son más rápidos. Necesitamos mejorar la seguridad del protocolo. También hemos desarrollado estrategias heurísticas y soluciones alternativas para minimizar la sobrecarga de memoria y ancho de banda del protocolo, pero esas estrategias son frágiles, difíciles de ajustar y hacen que el protocolo sea aún más propenso a fallar, causando que la sesión se desconecte.

Durante aproximadamente el mismo período de tiempo, la especificación ElGamal/AES+SessionTag y la documentación relacionada han descrito cuán costoso es en términos de ancho de banda entregar session tags, y han propuesto reemplazar la entrega de session tags con un "PRNG sincronizado". Un PRNG sincronizado genera determinísticamente los mismos tags en ambos extremos, derivados de una semilla común. Un PRNG sincronizado también puede denominarse un "ratchet". Esta propuesta (finalmente) especifica ese mecanismo ratchet, y elimina la entrega de tags.

Al usar un ratchet (un PRNG sincronizado) para generar las etiquetas de sesión, eliminamos la sobrecarga de enviar etiquetas de sesión en el mensaje New Session y en mensajes posteriores cuando sea necesario. Para un conjunto típico de 32 etiquetas, esto representa 1KB. Esto también elimina el almacenamiento de etiquetas de sesión en el lado del remitente, reduciendo así los requisitos de almacenamiento a la mitad.

Se necesita un handshake bidireccional completo, similar al patrón Noise IK, para evitar ataques de Key Compromise Impersonation (KCI). Ver la tabla "Payload Security Properties" de Noise en [NOISE](https://noiseprotocol.org/noise.html). Para más información sobre KCI, consultar el artículo https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### No objetivos / Fuera del alcance

El modelo de amenazas es algo diferente al de NTCP2 (propuesta 111). Los nodos MitM son el OBEP e IBGW y se asume que tienen una visión completa del NetDB global actual o histórico, mediante colusión con floodfills.

El objetivo es evitar que estos MitMs clasifiquen el tráfico como mensajes de Sesión Nueva y Existente, o como criptografía nueva vs. criptografía antigua.

## Detailed Proposal

Esta propuesta define un nuevo protocolo de extremo a extremo para reemplazar ElGamal/AES+SessionTags. El diseño utilizará un handshake Noise y una fase de datos que incorpora el double ratchet de Signal.

### Justificación

Hay cinco partes del protocolo que deben ser rediseñadas:

- 1) Los formatos de contenedor de Sesión nueva y Existente
  son reemplazados con nuevos formatos.
- 2) ElGamal (claves públicas de 256 bytes, claves privadas de 128 bytes) es reemplazado
  con ECIES-X25519 (claves públicas y privadas de 32 bytes)
- 3) AES es reemplazado con
  AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly a continuación)
- 4) Los SessionTags serán reemplazados con ratchets,
  que es esencialmente un PRNG criptográfico y sincronizado.
- 5) La carga útil AES, como se define en la especificación ElGamal/AES+SessionTags,
  es reemplazada con un formato de bloque similar al de NTCP2.

Cada uno de los cinco cambios tiene su propia sección a continuación.

### Modelo de Amenazas

Las implementaciones existentes de router I2P requerirán implementaciones para las siguientes primitivas criptográficas estándar, que no son requeridas para los protocolos I2P actuales:

- ECIES (pero esto es esencialmente X25519)
- Elligator2

Las implementaciones existentes de router I2P que aún no han implementado [NTCP2](/docs/specs/ntcp2/) ([Propuesta 111](/proposals/111-ntcp-2/)) también requerirán implementaciones para:

- Generación de claves X25519 y DH
- AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly a continuación)
- HKDF

### Crypto Type

El tipo de criptografía (usado en el LS2) es 4. Esto indica una clave pública X25519 de 32 bytes en little-endian, y el protocolo extremo a extremo especificado aquí.

El tipo de cifrado 0 es ElGamal. Los tipos de cifrado 1-3 están reservados para ECIES-ECDH-AES-SessionTag, ver propuesta 145 [Proposal 145](/proposals/145-ecies).

### Resumen del Diseño Criptográfico

Esta propuesta proporciona los requisitos basados en el Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisión 34, 2018-07-11). Noise tiene propiedades similares al protocolo Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), que es la base del protocolo [SSU](/docs/legacy/ssu/). En el lenguaje de Noise, Alice es el iniciador, y Bob es el respondedor.

Esta propuesta se basa en el protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256. (El identificador real para la función de derivación de clave inicial es "Noise_IKelg2_25519_ChaChaPoly_SHA256" para indicar extensiones I2P - ver sección KDF 1 más abajo) Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Handshake Interactivo: IK
  Alice transmite inmediatamente su clave estática a Bob (I)
  Alice ya conoce la clave estática de Bob (K)

- Patrón de Handshake Unidireccional: N
  Alice no transmite su clave estática a Bob (N)

- DH Function: X25519
  X25519 DH con una longitud de clave de 32 bytes según se especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Función de Cifrado: ChaChaPoly
  AEAD_CHACHA20_POLY1305 como se especifica en [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8.
  Nonce de 12 bytes, con los primeros 4 bytes establecidos en cero.
  Idéntico al de [NTCP2](/docs/specs/ntcp2/).

- Función Hash: SHA256
  Hash estándar de 32 bytes, ya utilizado extensivamente en I2P.

### Nuevas Primitivas Criptográficas para I2P

Esta propuesta define las siguientes mejoras a Noise_IK_25519_ChaChaPoly_SHA256. Estas generalmente siguen las pautas en [NOISE](https://noiseprotocol.org/noise.html) sección 13.

1) Las claves efímeras en texto claro se codifican con [Elligator2](https://elligator.cr.yp.to/).

2) La respuesta se prefija con una etiqueta en texto plano.

3) El formato de payload se define para los mensajes 1, 2 y la fase de datos. Por supuesto, esto no está definido en Noise.

Todos los mensajes incluyen un encabezado de mensaje garlic [I2NP](/docs/specs/i2np/). La fase de datos utiliza cifrado similar a, pero no compatible con, la fase de datos de Noise.

### Tipo de Criptografía

Los handshakes utilizan patrones de handshake [Noise](https://noiseprotocol.org/noise.html).

Se utiliza el siguiente mapeo de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje

Las sesiones One-time y Unbound son similares al patrón Noise N.

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
### Marco de Protocolo Noise

El protocolo actual ElGamal/AES+SessionTag es unidireccional. En esta capa, el receptor no sabe de dónde proviene un mensaje. Las sesiones de salida y entrada no están asociadas. Los acuses de recibo se realizan fuera de banda usando un DeliveryStatusMessage (envuelto en un GarlicMessage) en el clove.

Existe una ineficiencia sustancial en un protocolo unidireccional. Cualquier respuesta también debe usar un costoso mensaje 'New Session'. Esto causa un mayor uso de ancho de banda, CPU y memoria.

También hay debilidades de seguridad en un protocolo unidireccional. Todas las sesiones se basan en DH efímero-estático. Sin una ruta de retorno, no hay forma de que Bob "ratchet" su clave estática a una clave efímera. Sin saber de dónde proviene un mensaje, no hay manera de usar la clave efímera recibida para mensajes salientes, por lo que la respuesta inicial también usa DH efímero-estático.

Para esta propuesta, definimos dos mecanismos para crear un protocolo bidireccional - "pairing" y "binding". Estos mecanismos proporcionan mayor eficiencia y seguridad.

### Adiciones al Framework

Al igual que con ElGamal/AES+SessionTags, todas las sesiones entrantes y salientes deben estar en un contexto dado, ya sea el contexto del router o el contexto para un destino local particular. En Java I2P, este contexto se llama Session Key Manager.

Las sesiones no deben compartirse entre contextos, ya que eso permitiría la correlación entre los diversos destinos locales, o entre un destino local y un router.

Cuando un destino dado soporta tanto ElGamal/AES+SessionTags como esta propuesta, ambos tipos de sesiones pueden compartir un contexto. Ver sección 1c) a continuación.

### Patrones de Handshake

Cuando se crea una sesión de salida en el originador (Alice), se crea una nueva sesión de entrada y se empareja con la sesión de salida, a menos que no se espere respuesta (p. ej. datagramas en bruto).

Una nueva sesión entrante siempre se empareja con una nueva sesión saliente, a menos que no se solicite respuesta (por ejemplo, datagramas sin procesar).

Si se solicita una respuesta y está vinculada a un destino o router del extremo lejano, esa nueva sesión saliente se vincula a ese destino o router, y reemplaza cualquier sesión saliente previa a ese destino o router.

El emparejamiento de sesiones entrantes y salientes proporciona un protocolo bidireccional con la capacidad de rotar las claves DH.

### Sesiones

Solo hay una sesión saliente hacia un destino o router determinado. Puede haber varias sesiones entrantes actuales desde un destino o router determinado. Generalmente, cuando se crea una nueva sesión entrante y se recibe tráfico en esa sesión (lo cual sirve como ACK), cualquier otra será marcada para expirar relativamente rápido, en un minuto aproximadamente. Se verifica el valor de mensajes previos enviados (PN), y si no hay mensajes no recibidos (dentro del tamaño de ventana) en la sesión entrante anterior, la sesión anterior puede eliminarse inmediatamente.

Cuando se crea una sesión saliente en el originador (Alice), se vincula al Destination del extremo remoto (Bob), y cualquier sesión entrante emparejada también se vinculará al Destination del extremo remoto. A medida que las sesiones avanzan, continúan estando vinculadas al Destination del extremo remoto.

Cuando se crea una sesión entrante en el receptor (Bob), puede vincularse al Destination del extremo remoto (Alice), a opción de Alice. Si Alice incluye información de vinculación (su clave estática) en el mensaje New Session, la sesión se vinculará a ese destination, y se creará una sesión saliente que se vinculará al mismo Destination. A medida que las sesiones hacen ratchet, continúan estando vinculadas al Destination del extremo remoto.

### Contexto de Sesión

Para el caso común de streaming, esperamos que Alice y Bob usen el protocolo de la siguiente manera:

- Alice empareja su nueva sesión saliente con una nueva sesión entrante, ambas vinculadas al destino del extremo remoto (Bob).
- Alice incluye la información de vinculación y la firma, y una solicitud de respuesta, en el
  mensaje New Session enviado a Bob.
- Bob empareja su nueva sesión entrante con una nueva sesión saliente, ambas vinculadas al destino del extremo remoto (Alice).
- Bob envía una respuesta (ack) a Alice en la sesión emparejada, con un ratchet a una nueva clave DH.
- Alice hace ratchet a una nueva sesión saliente con la nueva clave de Bob, emparejada con la sesión entrante existente.

Al vincular una sesión entrante a un Destination del extremo remoto, y emparejar la sesión entrante con una sesión saliente vinculada al mismo Destination, logramos dos beneficios principales:

1) La respuesta inicial de Bob a Alice utiliza DH efímero-efímero

2) Después de que Alice recibe la respuesta de Bob y avanza el ratchet, todos los mensajes subsecuentes de Alice a Bob usan DH efímero-efímero.

### Emparejamiento de Sesiones Entrantes y Salientes

En ElGamal/AES+SessionTags, cuando un LeaseSet se agrupa como un diente de garlic, o se entregan etiquetas, el router emisor solicita un ACK. Este es un diente de garlic separado que contiene un Mensaje DeliveryStatus. Para seguridad adicional, el Mensaje DeliveryStatus se envuelve en un Mensaje Garlic. Este mecanismo está fuera de banda desde la perspectiva del protocolo.

En el nuevo protocolo, dado que las sesiones entrantes y salientes están emparejadas, podemos tener ACKs en banda. No se requiere un clove separado.

Un ACK explícito es simplemente un mensaje de Sesión Existente sin bloque I2NP. Sin embargo, en la mayoría de los casos, se puede evitar un ACK explícito, ya que hay tráfico inverso. Puede ser deseable que las implementaciones esperen un tiempo corto (quizás cien ms) antes de enviar un ACK explícito, para dar tiempo a la capa de streaming o aplicación para responder.

Las implementaciones también necesitarán diferir el envío de cualquier ACK hasta después de que se procese el bloque I2NP, ya que el Garlic Message puede contener un Database Store Message con un lease set. Un lease set reciente será necesario para enrutar el ACK, y el destino del extremo lejano (contenido en el lease set) será necesario para verificar la clave estática de enlace.

### Vinculación de Sesiones y Destinos

Las sesiones de salida siempre deben expirar antes que las sesiones de entrada. Una vez que una sesión de salida expira y se crea una nueva, también se creará una nueva sesión de entrada emparejada. Si había una sesión de entrada antigua, se le permitirá expirar.

### Beneficios del Binding y Pairing

Por determinar

### ACKs de Mensaje

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Tiempos de Espera de Sesión

### Multidifusión

El Garlic Message según se especifica en [I2NP](/docs/specs/i2np/) es el siguiente. Como objetivo de diseño es que los saltos intermedios no puedan distinguir el cifrado nuevo del antiguo, este formato no puede cambiar, aunque el campo de longitud sea redundante. El formato se muestra con el encabezado completo de 16 bytes, aunque el encabezado real puede estar en un formato diferente, dependiendo del transporte utilizado.

Cuando se descifran, los datos contienen una serie de Garlic Cloves y datos adicionales, también conocidos como un Clove Set.

Ver [I2NP](/docs/specs/i2np/) para detalles y una especificación completa.

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
### Definiciones

El formato de mensaje actual, utilizado durante más de 15 años, es ElGamal/AES+SessionTags. En ElGamal/AES+SessionTags, hay dos formatos de mensaje:

1) Nueva sesión: - bloque ElGamal de 514 bytes - bloque AES (128 bytes mínimo, múltiplo de 16)

2) Sesión existente: - 32 bytes Session Tag - Bloque AES (128 bytes mínimo, múltiplo de 16)

El padding mínimo a 128 está implementado como en Java I2P pero no se hace cumplir en la recepción.

Estos mensajes están encapsulados en un mensaje I2NP garlic, que contiene un campo de longitud, por lo que la longitud es conocida.

Nota que no hay padding definido para una longitud no-mod-16, por lo que la New Session siempre es (mod 16 == 2), y una Existing Session siempre es (mod 16 == 0). Necesitamos arreglar esto.

El receptor primero intenta buscar los primeros 32 bytes como una Session Tag. Si la encuentra, descifra el bloque AES. Si no la encuentra, y los datos tienen al menos (514+16) de longitud, intenta descifrar el bloque ElGamal, y si tiene éxito, descifra el bloque AES.

### 1) Formato de mensaje

En Signal Double Ratchet, el header contiene:

- DH: Clave pública actual del ratchet
- PN: Longitud del mensaje de la cadena anterior
- N: Número de mensaje

Las "cadenas de envío" de Signal son aproximadamente equivalentes a nuestros conjuntos de etiquetas. Al usar una etiqueta de sesión, podemos eliminar la mayor parte de eso.

En Nueva Sesión, ponemos solo la clave pública en el encabezado no cifrado.

En Existing Session, utilizamos una etiqueta de sesión para el encabezado. La etiqueta de sesión está asociada con la clave pública del ratchet actual y el número de mensaje.

En tanto Sesión Nueva como Existente, PN y N están en el cuerpo encriptado.

En Signal, las cosas están constantemente avanzando mediante ratcheting. Una nueva clave pública DH requiere que el receptor haga ratcheting y envíe una nueva clave pública de vuelta, lo cual también sirve como el ack para la clave pública recibida. Esto sería demasiadas operaciones DH para nosotros. Así que separamos el ack de la clave recibida y la transmisión de una nueva clave pública. Cualquier mensaje que use una etiqueta de sesión generada desde la nueva clave pública DH constituye un ACK. Solo transmitimos una nueva clave pública cuando deseamos hacer rekey.

El número máximo de mensajes antes de que el DH deba rotar es 65535.

Cuando se entrega una clave de sesión, derivamos el "Tag Set" de ella, en lugar de tener que entregar también las etiquetas de sesión. Un Tag Set puede tener hasta 65536 etiquetas. Sin embargo, los receptores deberían implementar una estrategia de "look-ahead", en lugar de generar todas las etiquetas posibles de una vez. Solo generar como máximo N etiquetas después de la última etiqueta válida recibida. N podría ser como máximo 128, pero 32 o incluso menos puede ser una mejor opción.

### Revisión del Formato Actual de Mensajes

Clave Pública de Una Sola Vez de Nueva Sesión (32 bytes) Datos cifrados y MAC (bytes restantes)

El mensaje New Session puede o no contener la clave pública estática del remitente. Si se incluye, la sesión inversa se vincula a esa clave. La clave estática debe incluirse si se esperan respuestas, es decir, para streaming y datagramas que pueden ser respondidos. No debe incluirse para datagramas sin procesar.

El mensaje New Session es similar al patrón Noise [NOISE](https://noiseprotocol.org/noise.html) unidireccional "N" (si no se envía la clave estática), o al patrón bidireccional "IK" (si se envía la clave estática).

### Revisión del Formato de Datos Cifrados

La longitud es 96 + longitud del payload. Formato encriptado:

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
### Nuevas Etiquetas de Sesión y Comparación con Signal

La clave efímera es de 32 bytes, codificada con Elligator2. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo las retransmisiones.

### 1a) Nuevo formato de sesión

Cuando se descifra, la clave estática X25519 de Alice, 32 bytes.

### 1b) Nuevo formato de sesión (con vinculación)

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. El payload debe contener un bloque DateTime y normalmente contendrá uno o más bloques Garlic Clove. Consulta la sección de payload a continuación para el formato y requisitos adicionales.

### Clave Efímera de Nueva Sesión

Si no se requiere respuesta, no se envía clave estática.

La longitud es 96 + longitud del payload. Formato encriptado:

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
### Clave Estática

Clave efímera de Alice. La clave efímera tiene 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluidas las retransmisiones.

### Carga útil

La sección de Flags no contiene nada. Siempre tiene 32 bytes, porque debe tener la misma longitud que la clave estática para mensajes de Nueva Sesión con vinculación. Bob determina si son una clave estática o una sección de flags probando si los 32 bytes son todos ceros.

TODO ¿se necesitan flags aquí?

### 1c) Nuevo formato de sesión (sin vinculación)

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. La carga útil debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove. Consulte la sección de carga útil a continuación para el formato y requisitos adicionales.

### Clave Efímera de Nueva Sesión

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
### Sección de Flags Datos descifrados

La clave de un solo uso es de 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo las retransmisiones.

### Carga útil

La sección Flags no contiene nada. Siempre son 32 bytes, porque debe tener la misma longitud que la clave estática para los mensajes New Session con binding. Bob determina si es una clave estática o una sección de flags probando si los 32 bytes son todos ceros.

TODO ¿se necesitan flags aquí?

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
### 1d) Formato de una sola vez (sin vinculación o sesión)

La longitud encriptada es el resto de los datos. La longitud desencriptada es 16 menos que la longitud encriptada. La carga útil debe contener un bloque DateTime y usualmente contendrá uno o más bloques Garlic Clove. Ver la sección de carga útil a continuación para el formato y requisitos adicionales.

### Clave de Una Sola Vez de Nueva Sesión

### Sección de Flags Datos descifrados

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
### Carga útil

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
### 1f) KDFs para Mensaje de Nueva Sesión

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
### KDF para ChainKey Inicial

Ten en cuenta que esto es un patrón Noise "N", pero usamos el mismo inicializador "IK" que para las sesiones vinculadas.

Los mensajes de Nueva Sesión no pueden ser identificados como conteniendo la clave estática de Alice o no hasta que la clave estática sea descifrada e inspeccionada para determinar si contiene todos ceros. Por lo tanto, el receptor debe usar la máquina de estados "IK" para todos los mensajes de Nueva Sesión. Si la clave estática contiene todos ceros, el patrón de mensaje "ss" debe ser omitido.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF para el Contenido Cifrado de la Sección de Flags/Clave Estática

Una o más New Session Replies pueden enviarse en respuesta a un único mensaje New Session. Cada respuesta va precedida por una etiqueta, que se genera a partir de un TagSet para la sesión.

La New Session Reply está en dos partes. La primera parte es la finalización del handshake Noise IK con una etiqueta antepuesta. La longitud de la primera parte es de 56 bytes. La segunda parte es la carga útil de la fase de datos. La longitud de la segunda parte es 16 + longitud de la carga útil.

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
### KDF para Sección de Payload (con clave estática de Alice)

La etiqueta se genera en el KDF de Etiquetas de Sesión, como se inicializa en el KDF de Inicialización DH a continuación. Esto correlaciona la respuesta con la sesión. La Clave de Sesión de la Inicialización DH no se utiliza.

### KDF para la Sección de Carga Útil (sin clave estática de Alice)

Clave efímera de Bob. La clave efímera son 32 bytes, codificada con Elligator2, little endian. Esta clave nunca se reutiliza; se genera una nueva clave con cada mensaje, incluyendo retransmisiones.

### 1g) Formato de respuesta de nueva sesión

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. La carga útil generalmente contendrá uno o más bloques Garlic Clove. Consulte la sección de carga útil a continuación para el formato y requisitos adicionales.

### Etiqueta de Sesión

Se crean una o más etiquetas a partir del TagSet, el cual se inicializa usando el KDF que se muestra a continuación, utilizando la chainKey del mensaje New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Clave Efímera de Respuesta de Nueva Sesión

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
### Carga útil

Esto es como el primer mensaje de Sesión Existente, post-división, pero sin una etiqueta separada. Además, usamos el hash de arriba para vincular la carga útil al mensaje NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF para Reply TagSet

Se pueden enviar múltiples mensajes NSR en respuesta, cada uno con claves efímeras únicas, dependiendo del tamaño de la respuesta.

Alice y Bob deben usar nuevas claves efímeras para cada mensaje NS y NSR.

Alice debe recibir uno de los mensajes NSR de Bob antes de enviar mensajes de Sesión Existente (ES), y Bob debe recibir un mensaje ES de Alice antes de enviar mensajes ES.

El ``chainKey`` y ``k`` de la Sección de Payload NSR de Bob se utilizan como entradas para los DH Ratchets ES iniciales (ambas direcciones, ver DH Ratchet KDF).

Bob debe retener únicamente las Sesiones Existentes para los mensajes ES recibidos de Alice. Cualquier otra sesión entrante y saliente creada (para múltiples NSRs) debe ser destruida inmediatamente después de recibir el primer mensaje ES de Alice para una sesión dada.

### KDF para Contenidos Cifrados de la Sección de Clave de Respuesta

Session tag (8 bytes) Datos cifrados y MAC (ver sección 3 a continuación)

### KDF para el Contenido Cifrado de la Sección de Carga Útil

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
### Notas

La longitud encriptada es el resto de los datos. La longitud desencriptada es 16 menos que la longitud encriptada. Ver la sección de payload a continuación para el formato y requisitos.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Formato de sesión existente

Formato: Claves públicas y privadas de 32 bytes, little-endian.

Justificación: Utilizado en [NTCP2](/docs/specs/ntcp2/).

### Formato

En los handshakes estándar de Noise, los mensajes iniciales del handshake en cada dirección comienzan con claves efímeras que se transmiten en texto plano. Como las claves X25519 válidas son distinguibles de datos aleatorios, un man-in-the-middle puede distinguir estos mensajes de los mensajes de Sesión Existente que comienzan con etiquetas de sesión aleatorias. En [NTCP2](/docs/specs/ntcp2/) ([Propuesta 111](/proposals/111-ntcp-2/)), usamos una función XOR de bajo overhead utilizando la clave estática fuera de banda para ofuscar la clave. Sin embargo, el modelo de amenaza aquí es diferente; no queremos permitir que ningún MitM use cualquier medio para confirmar el destino del tráfico, o para distinguir los mensajes iniciales del handshake de los mensajes de Sesión Existente.

Por lo tanto, se utiliza [Elligator2](https://elligator.cr.yp.to/) para transformar las claves efímeras en los mensajes New Session y New Session Reply de modo que sean indistinguibles de cadenas aleatorias uniformes.

### Carga útil

Claves públicas y privadas de 32 bytes. Las claves codificadas están en little endian.

Como se define en [Elligator2](https://elligator.cr.yp.to/), las claves codificadas son indistinguibles de 254 bits aleatorios. Necesitamos 256 bits aleatorios (32 bytes). Por lo tanto, la codificación y decodificación se definen de la siguiente manera:

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
### 2) ECIES-X25519

Requerido para evitar que el OBEP e IBGW clasifiquen el tráfico.

### 2a) Elligator2

Elligator2 duplica en promedio el tiempo de generación de claves, ya que la mitad de las claves privadas resultan en claves públicas que no son adecuadas para codificar con Elligator2. Además, el tiempo de generación de claves no tiene límite superior con una distribución exponencial, ya que el generador debe seguir reintentando hasta que se encuentra un par de claves adecuado.

Esta sobrecarga puede gestionarse realizando la generación de claves por adelantado, en un hilo separado, para mantener un pool de claves adecuadas.

El generador ejecuta la función ENCODE_ELG2() para determinar la idoneidad. Por lo tanto, el generador debería almacenar el resultado de ENCODE_ELG2() para que no tenga que calcularse nuevamente.

Además, las claves inadecuadas pueden agregarse al conjunto de claves utilizadas para [NTCP2](/docs/specs/ntcp2/), donde Elligator2 no se utiliza. Los problemas de seguridad de hacerlo están por determinarse.

### Formato

AEAD usando ChaCha20 y Poly1305, igual que en [NTCP2](/docs/specs/ntcp2/). Esto corresponde a [RFC-7539](https://tools.ietf.org/html/rfc7539), que también se usa de manera similar en TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### Justificación

Entradas para las funciones de cifrado/descifrado para un bloque AEAD en un mensaje New Session:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Notas

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
### 3) AEAD (ChaChaPoly)

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
### Entradas de Nueva Sesión y Respuesta de Nueva Sesión

- Dado que ChaCha20 es un cifrado de flujo, los textos planos no necesitan ser rellenados.
  Los bytes adicionales del flujo de claves se descartan.

- La clave para el cifrado (256 bits) se acuerda mediante el SHA256 KDF.
  Los detalles del KDF para cada mensaje están en secciones separadas a continuación.

- Los frames ChaChaPoly son de tamaño conocido ya que están encapsulados en el mensaje de datos I2NP.

- Para todos los mensajes,
  el relleno está dentro del marco
  de datos autenticados.

### Entradas de Sesión Existentes

Todos los datos recibidos que fallen la verificación AEAD deben ser descartados. No se devuelve respuesta alguna.

### Formato Cifrado

Usado en [NTCP2](/docs/specs/ntcp2/).

### Notas

Seguimos usando session tags, como antes, pero usamos ratchets para generarlas. Los session tags también tenían una opción de rekey que nunca implementamos. Así que es como un double ratchet pero nunca hicimos el segundo.

Aquí definimos algo similar al Double Ratchet de Signal. Las etiquetas de sesión se generan de forma determinística e idéntica en los lados del receptor y del emisor.

Al utilizar un mecanismo de trinquete de clave/etiqueta simétrico, eliminamos el uso de memoria para almacenar etiquetas de sesión en el lado del remitente. También eliminamos el consumo de ancho de banda al enviar conjuntos de etiquetas. El uso en el lado del receptor sigue siendo significativo, pero podemos reducirlo aún más ya que reduciremos la etiqueta de sesión de 32 bytes a 8 bytes.

No utilizamos el cifrado de encabezados como se especifica (y es opcional) en Signal, en su lugar utilizamos etiquetas de sesión.

Al usar un ratchet DH, logramos secreto hacia adelante, lo cual nunca fue implementado en ElGamal/AES+SessionTags.

Nota: La clave pública de un solo uso de Nueva Sesión no es parte del ratchet, su única función es cifrar la clave inicial de ratchet DH de Alice.

### Manejo de Errores AEAD

El Double Ratchet maneja los mensajes perdidos o fuera de orden incluyendo una etiqueta en cada cabecera de mensaje. El receptor busca el índice de la etiqueta, este es el número de mensaje N. Si el mensaje contiene un bloque de Número de Mensaje con un valor PN, el destinatario puede eliminar cualquier etiqueta superior a ese valor en el conjunto de etiquetas anterior, mientras retiene las etiquetas omitidas del conjunto de etiquetas anterior en caso de que los mensajes omitidos lleguen más tarde.

### Justificación

Definimos las siguientes estructuras de datos y funciones para implementar estos ratchets.

ENTRADA_TAGSET

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

CONJUNTO DE ETIQUETAS

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets pero no tan rápido como lo hace Signal. Separamos el reconocimiento de la clave recibida de la generación de la nueva clave. En el uso típico, Alice y Bob harán cada uno un ratchet (dos veces) inmediatamente en una Nueva Sesión, pero no harán ratchet de nuevo.

Ten en cuenta que un ratchet es para una sola dirección, y genera una cadena de ratchet de etiqueta de Nueva Sesión / clave de mensaje para esa dirección. Para generar claves para ambas direcciones, tienes que hacer ratchet dos veces.

Haces ratchet cada vez que generas y envías una nueva clave. Haces ratchet cada vez que recibes una nueva clave.

Alice hace un ratchet una vez al crear una sesión saliente no vinculada, no crea una sesión entrante (no vinculada significa que no se puede responder).

Bob realiza un ratchet una vez al crear una sesión entrante no vinculada, y no crea una sesión saliente correspondiente (no vinculada es no respondible).

Alice continúa enviando mensajes New Session (NS) a Bob hasta recibir uno de los mensajes New Session Reply (NSR) de Bob. Luego utiliza los resultados del KDF de la Sección de Payload del NSR como entradas para los session ratchets (ver DH Ratchet KDF), y comienza a enviar mensajes Existing Session (ES).

Para cada mensaje NS recibido, Bob crea una nueva sesión entrante, usando los resultados del KDF de la Sección de Carga Útil de respuesta como entradas para el nuevo DH Ratchet ES entrante y saliente.

Para cada respuesta requerida, Bob envía a Alice un mensaje NSR con la respuesta en la carga útil. Es obligatorio que Bob use nuevas claves efímeras para cada NSR.

Bob debe recibir un mensaje ES de Alice en una de las sesiones entrantes, antes de crear y enviar mensajes ES en la sesión saliente correspondiente.

Alice debería usar un temporizador para recibir un mensaje NSR de Bob. Si el temporizador expira, la sesión debería eliminarse.

Para evitar un ataque KCI y/o de agotamiento de recursos, donde un atacante descarta las respuestas NSR de Bob para mantener a Alice enviando mensajes NS, Alice debería evitar iniciar New Sessions hacia Bob después de un cierto número de reintentos debido a la expiración del temporizador.

Alice y Bob realizan cada uno un ratchet DH por cada bloque NextKey recibido.

Alice y Bob generan cada uno nuevos ratchets de conjuntos de etiquetas y dos ratchets de claves simétricas después de cada ratchet DH. Para cada nuevo mensaje ES en una dirección dada, Alice y Bob avanzan los ratchets de etiquetas de sesión y claves simétricas.

La frecuencia de los ratchets DH después del handshake inicial depende de la implementación. Aunque el protocolo establece un límite de 65535 mensajes antes de que se requiera un ratchet, el uso más frecuente de ratcheting (basado en el conteo de mensajes, tiempo transcurrido, o ambos) puede proporcionar seguridad adicional.

Después del KDF de handshake final en sesiones vinculadas, Bob y Alice deben ejecutar la función Noise Split() en el CipherState resultante para crear claves simétricas y de cadena de etiquetas independientes para sesiones entrantes y salientes.

#### KEY AND TAG SET IDS

Los números de ID de claves y conjuntos de etiquetas se utilizan para identificar claves y conjuntos de etiquetas. Los IDs de claves se usan en bloques NextKey para identificar la clave enviada o utilizada. Los IDs de conjuntos de etiquetas se usan (con el número de mensaje) en bloques ACK para identificar el mensaje que está siendo confirmado. Tanto los IDs de claves como los de conjuntos de etiquetas se aplican a los conjuntos de etiquetas para una sola dirección. Los números de ID de claves y conjuntos de etiquetas deben ser secuenciales.

En los primeros conjuntos de etiquetas utilizados para una sesión en cada dirección, el ID del conjunto de etiquetas es 0. No se han enviado bloques NextKey, por lo que no hay IDs de clave.

Para comenzar un ratchet DH, el remitente transmite un nuevo bloque NextKey con un ID de clave de 0. El receptor responde con un nuevo bloque NextKey con un ID de clave de 0. El remitente luego comienza a usar un nuevo conjunto de etiquetas con un ID de conjunto de etiquetas de 1.

Los conjuntos de etiquetas subsiguientes se generan de manera similar. Para todos los conjuntos de etiquetas utilizados después de los intercambios NextKey, el número del conjunto de etiquetas es (1 + ID de clave de Alice + ID de clave de Bob).

Los IDs de claves y conjuntos de etiquetas comienzan en 0 e incrementan secuencialmente. El ID máximo de conjunto de etiquetas es 65535. El ID máximo de clave es 32767. Cuando un conjunto de etiquetas está casi agotado, el remitente del conjunto de etiquetas debe iniciar un intercambio NextKey. Cuando el conjunto de etiquetas 65535 está casi agotado, el remitente del conjunto de etiquetas debe iniciar una nueva sesión enviando un mensaje New Session.

Con un tamaño máximo de mensaje de streaming de 1730, y asumiendo que no hay retransmisiones, la transferencia máxima teórica de datos usando un solo conjunto de etiquetas es 1730 * 65536 ~= 108 MB. El máximo real será menor debido a las retransmisiones.

El máximo teórico de transferencia de datos con los 65536 conjuntos de etiquetas disponibles, antes de que la sesión tenga que ser descartada y reemplazada, es 64K * 108 MB ~= 6.9 TB.

#### DH RATCHET MESSAGE FLOW

El siguiente intercambio de claves para un conjunto de etiquetas debe ser iniciado por el remitente de esas etiquetas (el propietario del conjunto de etiquetas salientes). El receptor (propietario del conjunto de etiquetas entrantes) responderá. Para un tráfico HTTP GET típico en la capa de aplicación, Bob enviará más mensajes y hará ratchet primero al iniciar el intercambio de claves; el diagrama a continuación muestra eso. Cuando Alice hace ratchet, sucede lo mismo pero en reversa.

El primer conjunto de etiquetas utilizado después del handshake NS/NSR es el conjunto de etiquetas 0. Cuando el conjunto de etiquetas 0 está casi agotado, se deben intercambiar nuevas claves en ambas direcciones para crear el conjunto de etiquetas 1. Después de eso, una nueva clave solo se envía en una dirección.

Para crear el conjunto de etiquetas 2, el emisor de etiquetas envía una nueva clave y el receptor de etiquetas envía el ID de su clave anterior como confirmación. Ambos lados realizan un DH.

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
Después de que el trinquete DH esté completo para un tagset saliente, y se cree un nuevo tagset saliente, debe usarse inmediatamente, y el tagset saliente antiguo puede eliminarse.

Después de que el ratchet DH se completa para un tagset entrante, y se crea un nuevo tagset entrante, el receptor debería escuchar etiquetas en ambos tagsets, y eliminar el tagset antiguo después de un tiempo corto, aproximadamente 3 minutos.

El resumen de la progresión del conjunto de etiquetas y el ID de clave se encuentra en la tabla siguiente. * indica que se genera una nueva clave.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Los números de ID del conjunto de claves y etiquetas deben ser secuenciales.

#### DH INITIALIZATION KDF

Esta es la definición de DH_INITIALIZE(rootKey, k) para una sola dirección. Crea un tagset y una "clave raíz siguiente" para ser utilizada en un ratchet DH posterior si es necesario.

Utilizamos la inicialización DH en tres lugares. Primero, la usamos para generar un conjunto de etiquetas para las New Session Replies. Segundo, la usamos para generar dos conjuntos de etiquetas, uno para cada dirección, para usar en los mensajes Existing Session. Por último, la usamos después de un DH Ratchet para generar un nuevo conjunto de etiquetas en una sola dirección para mensajes Existing Session adicionales.

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
#### DH RATCHET KDF

Esto se usa después de que se intercambian nuevas claves DH en bloques NextKey, antes de que se agote un tagset.

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
### Números de Mensaje

Ratchets para cada mensaje, como en Signal. El ratchet de etiqueta de sesión está sincronizado with el ratchet de clave simétrica, pero el ratchet de clave del receptor puede "quedarse atrás" para ahorrar memoria.

El transmisor avanza el ratchet una vez por cada mensaje transmitido. No se deben almacenar etiquetas adicionales. El transmisor también debe mantener un contador para 'N', el número de mensaje del mensaje en la cadena actual. El valor 'N' se incluye en el mensaje enviado. Consulte la definición del bloque Message Number.

El receptor debe avanzar el ratchet por el tamaño máximo de la ventana y almacenar las etiquetas en un "conjunto de etiquetas", que está asociado con la sesión. Una vez recibida, la etiqueta almacenada puede ser descartada, y si no hay etiquetas anteriores no recibidas, la ventana puede ser avanzada. El receptor debe mantener el valor 'N' asociado con cada etiqueta de sesión, y verificar que el número en el mensaje enviado coincida con este valor. Ver la definición del bloque Message Number.

#### KDF

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
### Implementación de Ejemplo

Ratchets para cada mensaje, como en Signal. Cada clave simétrica tiene un número de mensaje y una etiqueta de sesión asociados. El ratchet de clave de sesión está sincronizado with el ratchet de etiquetas simétricas, pero el ratchet de clave del receptor puede "quedarse atrás" para ahorrar memoria.

El transmisor hace ratchet una vez por cada mensaje transmitido. No se deben almacenar claves adicionales.

Cuando el receptor obtiene un session tag, si aún no ha avanzado el ratchet de clave simétrica hasta la clave asociada, debe "ponerse al día" con la clave asociada. El receptor probablemente almacenará en caché las claves para cualquier tag previo que aún no haya sido recibido. Una vez recibido, la clave almacenada puede descartarse, y si no hay tags previos no recibidos, la ventana puede avanzarse.

Para mayor eficiencia, los ratchets de etiqueta de sesión y clave simétrica están separados para que el ratchet de etiqueta de sesión pueda adelantarse al ratchet de clave simétrica. Esto también proporciona seguridad adicional, ya que las etiquetas de sesión se transmiten por el cable.

#### KDF

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
### 4a) DH Ratchet

Esto reemplaza el formato de sección AES definido en la especificación ElGamal/AES+SessionTags.

Esto utiliza el mismo formato de bloque definido en la especificación [NTCP2](/docs/specs/ntcp2/). Los tipos de bloques individuales se definen de manera diferente.

Existen preocupaciones de que alentar a los implementadores a compartir código pueda llevar a problemas de análisis sintáctico. Los implementadores deben considerar cuidadosamente los beneficios y riesgos de compartir código, y asegurar que las reglas de ordenamiento y bloques válidos sean diferentes para los dos contextos.

### Payload Section Decrypted data

La longitud cifrada es el resto de los datos. La longitud descifrada es 16 menos que la longitud cifrada. Se admiten todos los tipos de bloque. El contenido típico incluye los siguientes bloques:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Hay cero o más bloques en la trama encriptada. Cada bloque contiene un identificador de un byte, una longitud de dos bytes y cero o más bytes de datos.

Para extensibilidad, los receptores DEBEN ignorar los bloques con números de tipo desconocidos, y tratarlos como relleno.

Los datos cifrados tienen un máximo de 65535 bytes, incluyendo un encabezado de autenticación de 16 bytes, por lo que el máximo de datos sin cifrar es de 65519 bytes.

(Etiqueta de autenticación Poly1305 no mostrada):

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
### Block Ordering Rules

En el mensaje New Session, el bloque DateTime es obligatorio y debe ser el primer bloque.

Otros bloques permitidos:

- Garlic Clove (tipo 11)
- Opciones (tipo 5)
- Relleno (tipo 254)

En el mensaje New Session Reply, no se requieren bloques.

Otros bloques permitidos:

- Garlic Clove (tipo 11)
- Opciones (tipo 5)
- Relleno (tipo 254)

No se permiten otros bloques. El relleno, si está presente, debe ser el último bloque.

En el mensaje de Sesión Existente, no se requieren bloques, y el orden no está especificado, excepto por los siguientes requisitos:

La terminación, si está presente, debe ser el último bloque excepto por el relleno. El relleno, si está presente, debe ser el último bloque.

Puede haber múltiples bloques Garlic Clove en una sola trama. Puede haber hasta dos bloques Next Key en una sola trama. No se permiten múltiples bloques Padding en una sola trama. Otros tipos de bloques probablemente no tendrán múltiples bloques en una sola trama, pero no está prohibido.

### DateTime

Una expiración. Ayuda en la prevención de respuestas. Bob debe validar que el mensaje es reciente, usando esta marca de tiempo. Bob debe implementar un filtro Bloom u otro mecanismo para prevenir ataques de repetición, si el tiempo es válido. Generalmente incluido solo en mensajes New Session.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Trinquete de Etiqueta de Sesión

Un único Garlic Clove descifrado según se especifica en [I2NP](/docs/specs/i2np/), con modificaciones para eliminar campos que no se utilizan o son redundantes. Advertencia: Este formato es significativamente diferente al de ElGamal/AES. Cada clove es un bloque de carga útil separado. Los Garlic Cloves no pueden ser fragmentados entre bloques o entre marcos ChaChaPoly.

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
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Notas:

- Los implementadores deben asegurar que al leer un bloque,
  los datos malformados o maliciosos no provoquen que las lecturas
  se desborden hacia el siguiente bloque.

- El formato Clove Set especificado en [I2NP](/docs/specs/i2np/) no se utiliza.
  Cada clove está contenido en su propio bloque.

- El encabezado del mensaje I2NP tiene 9 bytes, con un formato idéntico
  al utilizado en [NTCP2](/docs/specs/ntcp2/).

- El Certificate, Message ID y Expiration de la
  definición de Garlic Message en [I2NP](/docs/specs/i2np/) no están incluidos.

- El Certificate, Clove ID, y Expiration de la
  definición de Garlic Clove en [I2NP](/docs/specs/i2np/) no están incluidos.

Justificación:

- Los certificados nunca se utilizaron.
- Los ID de mensaje separados y los ID de clove nunca se utilizaron.
- Las expiraciones separadas nunca se utilizaron.
- El ahorro general comparado con los formatos antiguos Clove Set y Clove
  es de aproximadamente 35 bytes para 1 clove, 54 bytes para 2 cloves,
  y 73 bytes para 3 cloves.
- El formato de bloque es extensible y cualquier campo nuevo puede agregarse
  como nuevos tipos de bloque.

### Termination

La implementación es opcional. Descartar la sesión. Este debe ser el último bloque sin relleno en el frame. No se enviarán más mensajes en esta sesión.

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
### 4c) Trinquete de Clave Simétrica

NO IMPLEMENTADO, para estudio posterior. Pasar opciones actualizadas. Las opciones incluyen varios parámetros para la sesión. Consulte la sección Análisis de Longitud de Etiquetas de Sesión a continuación para más información.

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

- El soporte para longitud de etiqueta de sesión no predeterminada esperamos
  que nunca sea necesario.
- La ventana de etiquetas es MAX_SKIP en la documentación de Signal.

Problemas:

- La negociación de opciones está por determinar (TBD).
- Los valores por defecto están por determinar (TBD).
- Las opciones de relleno y retraso se copian de NTCP2,
  pero esas opciones no han sido completamente implementadas o estudiadas allí.

### Message Numbers

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
  Esto es similar a lo que hace Signal, pero en Signal, PN y N están en el encabezado.
  Aquí, están en el cuerpo del mensaje cifrado.
- No envíes este bloque en el conjunto de etiquetas 0, porque no había un conjunto de etiquetas anterior.

### 5) Carga útil

La siguiente clave de ratchet DH está en la carga útil, y es opcional. No hacemos ratchet cada vez. (Esto es diferente a Signal, donde está en el encabezado y se envía cada vez)

Para el primer ratchet, Key ID = 0.

No permitido en NS o NSR. Solo se incluye en mensajes de Sesión Existente.

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

- El Key ID es un contador incremental para la clave local utilizada para ese conjunto de etiquetas, comenzando en 0.
- El ID no debe cambiar a menos que la clave cambie.
- Puede que no sea estrictamente necesario, pero es útil para depuración.
  Signal no utiliza un key ID.
- El Key ID máximo es 32767.
- En el caso raro de que los conjuntos de etiquetas en ambas direcciones estén ratcheting al
  mismo tiempo, un frame contendrá dos bloques Next Key, uno para
  la clave forward y uno para la clave reverse.
- Los números de ID de conjuntos de claves y etiquetas deben ser secuenciales.
- Ver la sección DH Ratchet arriba para detalles.

### Sección de Carga Útil Datos descifrados

Esto solo se envía si se recibió un bloque de solicitud de ack. Pueden estar presentes múltiples acks para confirmar múltiples mensajes.

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

- El ID del conjunto de etiquetas y N identifican de forma única el mensaje que se está confirmando.
- En los primeros conjuntos de etiquetas utilizados para una sesión en cada dirección, el ID del conjunto de etiquetas es 0.
- No se han enviado bloques NextKey, por lo que no hay IDs de clave.
- Para todos los conjuntos de etiquetas utilizados después de los intercambios NextKey, el número del conjunto de etiquetas es (1 + ID de clave de Alice + ID de clave de Bob).

### Datos sin cifrar

Solicitar un ack in-band. Para reemplazar el Mensaje DeliveryStatus out-of-band en el Garlic Clove.

Si se solicita un ack explícito, el ID del tagset actual y el número de mensaje (N) se devuelven en un bloque ack.

No permitido en NS o NSR. Solo se incluye en mensajes de Sesión Existente.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Reglas de Ordenamiento de Bloques

Todo el padding está dentro de las tramas AEAD. TODO El padding dentro de AEAD debería adherirse aproximadamente a los parámetros negociados. TODO Alice envió sus parámetros mín/máx de tx/rx solicitados en el mensaje NS. TODO Bob envió sus parámetros mín/máx de tx/rx solicitados en el mensaje NSR. Las opciones actualizadas pueden enviarse durante la fase de datos. Consulte la información del bloque de opciones arriba.

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

- El relleno de solo ceros está bien, ya que será encriptado.
- Las estrategias de relleno están por definirse.
- Se permiten frames que contengan solo relleno.
- El relleno por defecto es de 0-15 bytes.
- Ver bloque de opciones para la negociación de parámetros de relleno
- Ver bloque de opciones para los parámetros mínimos/máximos de relleno
- La respuesta del router ante la violación del relleno negociado depende de la implementación.

### DateTime

Las implementaciones deben ignorar los tipos de bloques desconocidos para mantener compatibilidad hacia adelante.

### Diente de Ajo Garlic

- La longitud del padding debe decidirse caso por caso según el mensaje y
  estimaciones de la distribución de longitudes, o se deben agregar retrasos
  aleatorios. Estas contramedidas deben incluirse para resistir DPI, ya que
  los tamaños de mensaje revelarían que el tráfico I2P está siendo transportado
  por el protocolo de transporte. El esquema exacto de padding es un área de
  trabajo futuro, el Apéndice A proporciona más información sobre el tema.

## Typical Usage Patterns

### Terminación

Este es el caso de uso más típico, y la mayoría de casos de uso de streaming no-HTTP serán idénticos a este caso de uso también. Se envía un mensaje inicial pequeño, sigue una respuesta, y se envían mensajes adicionales en ambas direcciones.

Un HTTP GET generalmente cabe en un solo mensaje I2NP. Alice envía una solicitud pequeña con un solo mensaje Session nuevo, empaquetando un leaseset de respuesta. Alice incluye ratchet inmediato a nueva clave. Incluye sig para vincular al destino. No se solicita ack.

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
### Opciones

Alice tiene tres opciones:

1) Enviar solo el primer mensaje (tamaño de ventana = 1), como en HTTP GET. No recomendado.

2) Enviar hasta la ventana de streaming, pero usando la misma clave pública en texto claro codificada con Elligator2. Todos los mensajes contienen la misma clave pública siguiente (ratchet). Esto será visible para OBGW/IBEP porque todos comienzan con el mismo texto claro. Las cosas proceden como en 1). No recomendado.

3) Implementación recomendada. Enviar hasta la ventana de streaming, pero usando una clave pública en texto claro codificada con Elligator2 diferente (sesión) para cada una. Todos los mensajes contienen la misma clave pública siguiente (ratchet). Esto no será visible para OBGW/IBEP porque todos comienzan con texto claro diferente. Bob debe reconocer que todos contienen la misma clave pública siguiente, y responder a todos con el mismo ratchet. Alice usa esa clave pública siguiente y continúa.

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
### Números de Mensaje

Un solo mensaje, con una sola respuesta esperada. Se pueden enviar mensajes o respuestas adicionales.

Similar a HTTP GET, pero con opciones más pequeñas para el tamaño de ventana de etiqueta de sesión y tiempo de vida. Tal vez no solicitar un ratchet.

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
### Siguiente Clave Pública del DH Ratchet

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
### Reconocimiento

Un solo mensaje anónimo, sin esperar respuesta.

Se envía un mensaje de una sola vez. No se incluyen LS de respuesta o DSM. No se incluye la siguiente clave. No se solicita respuesta o ratchet. No se envía ratchet. Las opciones establecen la ventana de etiquetas de sesión en cero.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Solicitud de Confirmación

Las sesiones de larga duración pueden realizar ratchet, o solicitar un ratchet, en cualquier momento, para mantener el secreto hacia adelante desde ese punto en el tiempo. Las sesiones deben realizar ratchet cuando se aproximan al límite de mensajes enviados por sesión (65535).

## Implementation Considerations

### Relleno

Como con el protocolo ElGamal/AES+SessionTag existente, las implementaciones deben limitar el almacenamiento de session tag y protegerse contra ataques de agotamiento de memoria.

Algunas estrategias recomendadas incluyen:

- Límite estricto en el número de etiquetas de sesión almacenadas
- Expiración agresiva de sesiones entrantes inactivas cuando hay presión de memoria
- Límite en el número de sesiones entrantes vinculadas a un único destino remoto
- Reducción adaptativa de la ventana de etiquetas de sesión y eliminación de etiquetas antiguas no utilizadas
  cuando hay presión de memoria
- Rechazo a realizar ratchet cuando se solicita, si hay presión de memoria

### Otros tipos de bloques

Parámetros y tiempos de espera recomendados:

- Tamaño de tagset NSR: 12 tsmin y tsmax
- Tamaño de tagset ES 0: tsmin 24, tsmax 160
- Tamaño de tagset ES (1+): 160 tsmin y tsmax
- Tiempo de espera de tagset NSR: 3 minutos para receptor
- Tiempo de espera de tagset ES: 8 minutos para emisor, 10 minutos para receptor
- Eliminar tagset ES anterior después de: 3 minutos
- Anticipación de tagset de tag N: min(tsmax, tsmin + N/4)
- Recorte posterior de tagset de tag N: min(tsmax, tsmin + N/4) / 2
- Enviar siguiente clave en tag: TBD
- Enviar siguiente clave después del tiempo de vida del tagset: TBD
- Reemplazar sesión si NS recibido después de: 3 minutos
- Desfase máximo de reloj: -5 minutos a +2 minutos
- Duración del filtro de repetición NS: 5 minutos
- Tamaño de relleno: 0-15 bytes (otras estrategias TBD)

### Trabajo futuro

A continuación se presentan recomendaciones para clasificar mensajes entrantes.

### X25519 Only

En un túnel que se usa exclusivamente con este protocolo, realizar la identificación como se hace actualmente con ElGamal/AES+SessionTags:

Primero, trata los datos iniciales como una etiqueta de sesión, y busca la etiqueta de sesión. Si se encuentra, descifra usando los datos almacenados asociados con esa etiqueta de sesión.

Si no se encuentra, trate los datos iniciales como una clave pública DH y nonce. Realice una operación DH y el KDF especificado, e intente descifrar los datos restantes.

### HTTP GET

En un túnel que admite tanto este protocolo como ElGamal/AES+SessionTags, clasifica los mensajes entrantes de la siguiente manera:

Debido a un fallo en la especificación ElGamal/AES+SessionTags, el bloque AES no se rellena hasta una longitud aleatoria no-mod-16. Por lo tanto, la longitud de los mensajes Existing Session módulo 16 siempre es 0, y la longitud de los mensajes New Session módulo 16 siempre es 2 (ya que el bloque ElGamal tiene 514 bytes de longitud).

Si la longitud mod 16 no es 0 o 2, trate los datos iniciales como una etiqueta de sesión, y busque la etiqueta de sesión. Si se encuentra, descifre usando los datos almacenados asociados con esa etiqueta de sesión.

Si no se encuentra, y la longitud mod 16 no es 0 o 2, tratar los datos iniciales como una clave pública DH y nonce. Realizar una operación DH y el KDF especificado, e intentar descifrar los datos restantes. (basado en la mezcla de tráfico relativa, y los costos relativos de las operaciones DH X25519 y ElGamal, este paso puede realizarse al final en su lugar)

De lo contrario, si la longitud mod 16 es 0, trata los datos iniciales como un session tag ElGamal/AES, y busca el session tag. Si se encuentra, descifra usando los datos almacenados asociados con ese session tag.

Si no se encuentra, y los datos tienen al menos 642 (514 + 128) bytes de longitud, y la longitud mod 16 es 2, trata los datos iniciales como un bloque ElGamal. Intenta descifrar los datos restantes.

Nota que si la especificación ElGamal/AES+SessionTag se actualiza para permitir relleno no-mod-16, las cosas tendrán que hacerse de manera diferente.

### HTTP POST

Las implementaciones iniciales dependen del tráfico bidireccional en las capas superiores. Es decir, las implementaciones asumen que pronto se transmitirá tráfico en la dirección opuesta, lo que forzará cualquier respuesta requerida en la capa ECIES.

Sin embargo, cierto tráfico puede ser unidireccional o de muy bajo ancho de banda, de tal manera que no hay tráfico de capas superiores para generar una respuesta oportuna.

La recepción de mensajes NS y NSR requiere una respuesta; la recepción de bloques ACK Request y Next Key también requiere una respuesta.

Una implementación sofisticada puede iniciar un temporizador cuando se recibe uno de estos mensajes que requiere una respuesta, y generar una respuesta "vacía" (sin bloque Garlic Clove) en la capa ECIES si no se envía tráfico de retorno en un período corto de tiempo (por ejemplo, 1 segundo).

También puede ser apropiado un timeout aún más corto para las respuestas a mensajes NS y NSR, para cambiar el tráfico a los mensajes ES eficientes tan pronto como sea posible.

## Analysis

### Datagrama Replicable

La sobrecarga de mensajes para los dos primeros mensajes en cada dirección es la siguiente. Esto asume solo un mensaje en cada dirección antes del ACK, o que cualquier mensaje adicional se envíe especulativamente como mensajes de Sesión Existente. Si no hay confirmaciones especulativas de las etiquetas de sesión entregadas, la sobrecarga del protocolo antiguo es mucho mayor.

No se asume relleno para el análisis del nuevo protocolo. No se asume leaseSet agrupado.

### Múltiples Datagramas Raw

Mensaje de nueva sesión, igual en cada dirección:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Mensajes de sesión existentes, iguales en cada dirección:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Datagrama Crudo Único

Mensaje de Nueva Sesión de Alice-a-Bob:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Mensaje de respuesta de nueva sesión de Bob a Alice:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Mensajes de sesión existentes, los mismos en cada dirección:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Sesiones de Larga Duración

Cuatro mensajes en total (dos en cada dirección):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Solo handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Total a largo plazo (ignorando handshakes):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO actualizar esta sección después de que la propuesta sea estable.

Las siguientes operaciones criptográficas son requeridas por cada parte para intercambiar mensajes New Session y New Session Reply:

- HMAC-SHA256: 3 por HKDF, total por determinar
- ChaChaPoly: 2 cada uno
- Generación de claves X25519: 2 Alice, 1 Bob
- X25519 DH: 3 cada uno
- Verificación de firma: 1 (Bob)

Alice calcula 5 ECDHs por sesión enlazada (mínimo), 2 para cada mensaje NS a Bob, y 3 para cada uno de los mensajes NSR de Bob.

Bob también calcula 6 ECDHs por sesión enlazada, 3 para cada uno de los mensajes NS de Alice, y 3 para cada uno de sus mensajes NSR.

Las siguientes operaciones criptográficas son requeridas por cada parte para cada mensaje de Existing Session:

- HKDF: 2
- ChaChaPoly: 1

### Defensa

La longitud actual del tag de sesión es de 32 bytes. Aún no hemos encontrado ninguna justificación para esa longitud, pero continuamos investigando en los archivos. La propuesta anterior define la nueva longitud del tag como 8 bytes. El análisis que justifica un tag de 8 bytes es el siguiente:

El ratchet de etiquetas de sesión se asume que genera etiquetas aleatorias y uniformemente distribuidas. No hay razón criptográfica para una longitud particular de etiqueta de sesión. El ratchet de etiquetas de sesión está sincronizado con, pero genera una salida independiente del, ratchet de claves simétricas. Las salidas de los dos ratchets pueden tener longitudes diferentes.

Por lo tanto, la única preocupación es la colisión de etiquetas de sesión. Se asume que las implementaciones no intentarán manejar colisiones tratando de descifrar con ambas sesiones; las implementaciones simplemente asociarán la etiqueta con la sesión anterior o nueva, y cualquier mensaje recibido con esa etiqueta en la otra sesión será descartado después de que falle el descifrado.

El objetivo es seleccionar una longitud de etiqueta de sesión que sea lo suficientemente grande como para minimizar el riesgo de colisiones, pero lo suficientemente pequeña como para minimizar el uso de memoria.

Esto asume que las implementaciones limitan el almacenamiento de etiquetas de sesión para prevenir ataques de agotamiento de memoria. Esto también reducirá significativamente las posibilidades de que un atacante pueda crear colisiones. Consulta la sección Consideraciones de Implementación a continuación.

Para un caso en el peor escenario, asume un servidor ocupado con 64 nuevas sesiones entrantes por segundo. Asume un tiempo de vida de etiquetas de sesión entrante de 15 minutos (igual que ahora, probablemente debería reducirse). Asume una ventana de etiquetas de sesión entrante de 32. 64 * 15 * 60 * 32 = 1,843,200 etiquetas. El máximo actual de etiquetas entrantes en Java I2P es 750,000 y nunca se ha alcanzado hasta donde sabemos.

Un objetivo de 1 en un millón (1e-6) de colisiones de etiquetas de sesión es probablemente suficiente. La probabilidad de que se descarte un mensaje en el camino debido a la congestión es mucho mayor que esa.

Ref: https://en.wikipedia.org/wiki/Birthday_paradox Sección de tabla de probabilidades.

Con session tags de 32 bytes (256 bits) el espacio de session tag es 1.2e77. La probabilidad de una colisión con probabilidad 1e-18 requiere 4.8e29 entradas. La probabilidad de una colisión con probabilidad 1e-6 requiere 4.8e35 entradas. 1.8 millones de tags de 32 bytes cada uno son aproximadamente 59 MB en total.

Con session tags de 16 bytes (128 bits) el espacio de session tag es de 3.4e38. La probabilidad de una colisión con probabilidad 1e-18 requiere 2.6e10 entradas. La probabilidad de una colisión con probabilidad 1e-6 requiere 2.6e16 entradas. 1.8 millones de tags de 16 bytes cada uno son aproximadamente 30 MB en total.

Con session tags de 8 bytes (64 bits) el espacio de session tag es 1.8e19. La probabilidad de una colisión con probabilidad 1e-18 requiere 6.1 entradas. La probabilidad de una colisión con probabilidad 1e-6 requiere 6.1e6 (6,100,000) entradas. 1.8 millones de tags de 8 bytes cada uno suman aproximadamente 15 MB en total.

6.1 millones de etiquetas activas es más de 3 veces nuestro estimado del peor caso de 1.8 millones de etiquetas. Así que la probabilidad de colisión sería menos de una en un millón. Por lo tanto, concluimos que las etiquetas de sesión de 8 bytes son suficientes. Esto resulta en una reducción de 4x del espacio de almacenamiento, además de la reducción de 2x porque las etiquetas de transmisión no se almacenan. Así que tendremos una reducción de 8x en el uso de memoria de etiquetas de sesión comparado con ElGamal/AES+SessionTags.

Para mantener flexibilidad en caso de que estas suposiciones sean incorrectas, incluiremos un campo de longitud de etiqueta de sesión en las opciones, de modo que la longitud predeterminada pueda anularse por sesión. No esperamos implementar negociación dinámica de longitud de etiquetas a menos que sea absolutamente necesario.

Las implementaciones deberían, como mínimo, reconocer las colisiones de etiquetas de sesión, manejarlas de manera elegante, y registrar o contar el número de colisiones. Aunque siguen siendo extremadamente improbables, serán mucho más probables de lo que eran para ElGamal/AES+SessionTags, y realmente podrían ocurrir.

### Parámetros

Usando el doble de sesiones por segundo (128) y el doble de la ventana de tags (64), tenemos 4 veces los tags (7.4 millones). El máximo para una probabilidad de colisión de uno en un millón es 6.1 millones de tags. Tags de 12 bytes (o incluso de 10 bytes) añadirían un margen enorme.

Sin embargo, ¿es una probabilidad de colisión de uno en un millón un objetivo adecuado? Mucho mayor que la probabilidad de ser descartado en el camino no es de mucha utilidad. El objetivo de falsos positivos para el DecayingBloomFilter de Java es aproximadamente de 1 en 10,000, pero incluso 1 en 1000 no es motivo de gran preocupación. Al reducir el objetivo a 1 en 10,000, hay un margen amplio con etiquetas de 8 bytes.

### Clasificación

El remitente genera etiquetas y claves sobre la marcha, por lo que no hay almacenamiento. Esto reduce los requisitos generales de almacenamiento a la mitad en comparación con ElGamal/AES. Las etiquetas ECIES son de 8 bytes en lugar de 32 para ElGamal/AES. Esto reduce los requisitos generales de almacenamiento por otro factor de 4. Las claves de sesión por etiqueta no se almacenan en el receptor excepto para "huecos", que son mínimos para tasas de pérdida razonables.

La reducción del 33% en el tiempo de expiración de etiquetas crea otro 33% de ahorro, asumiendo tiempos de sesión cortos.

Por lo tanto, el ahorro total de espacio vs. ElGamal/AES es un factor de 10.7, o 92%.

## Related Changes

### Solo X25519

Búsquedas de base de datos desde destinos ECIES: Ver [Propuesta 154](/proposals/154-ecies-lookups), ahora incorporada en [I2NP](/docs/specs/i2np/) para la versión 0.9.46.

Esta propuesta requiere soporte de LS2 para publicar la clave pública X25519 con el leaseset. No se requieren cambios a las especificaciones de LS2 en [I2NP](/docs/specs/i2np/). Todo el soporte fue diseñado, especificado e implementado en la [Propuesta 123](/proposals/123-new-netdb-entries) implementada en 0.9.38.

### X25519 Compartido con ElGamal/AES+SessionTags

Ninguno. Esta propuesta requiere soporte de LS2, y que se establezca una propiedad en las opciones I2CP para habilitarla. No se requieren cambios en las especificaciones de [I2CP](/docs/specs/i2cp/). Todo el soporte fue diseñado, especificado e implementado en la [Propuesta 123](/proposals/123-new-netdb-entries) implementada en la versión 0.9.38.

La opción requerida para habilitar ECIES es una sola propiedad I2CP para I2CP, BOB, SAM, o i2ptunnel.

Los valores típicos son i2cp.leaseSetEncType=4 para ECIES únicamente, o i2cp.leaseSetEncType=4,0 para claves duales ECIES y ElGamal.

### Respuestas de Capa de Protocolo

Esta sección está copiada de [Propuesta 123](/proposals/123-new-netdb-entries).

Opción en el Mapeo de SessionConfig:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Esta propuesta requiere LS2 que es compatible desde la versión 0.9.38. No se requieren cambios en las especificaciones de [I2CP](/docs/specs/i2cp/). Todo el soporte fue diseñado, especificado e implementado en la [Propuesta 123](/proposals/123-new-netdb-entries) implementada en la 0.9.38.

### Sobrecarga

Cualquier router que soporte LS2 con claves duales (0.9.38 o superior) debería soportar conexión a destinos con claves duales.

Los destinos exclusivos de ECIES requerirán que una mayoría de los floodfills se actualicen a 0.9.46 para obtener respuestas de búsqueda encriptadas. Consulte [Propuesta 154](/proposals/154-ecies-lookups).

Los destinos ECIES-only solo pueden conectarse con otros destinos que sean ECIES-only o de clave dual.
