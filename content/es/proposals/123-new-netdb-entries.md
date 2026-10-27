---
title: "Nuevas Entradas en netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Abrir"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Estado

Partes de esta propuesta están completas e implementadas en las versiones 0.9.38 y 0.9.39.   Las estructuras comunes, I2CP, I2NP y otras especificaciones   ahora están actualizadas para reflejar los cambios que actualmente se admiten.

Las partes completadas aún están sujetas a revisiones menores.   Otras partes de esta propuesta aún están en desarrollo   y están sujetas a revisiones sustanciales.

La búsqueda de servicios (tipos 9 y 11) tiene baja prioridad,   no está programada y podría separarse en una propuesta distinta.

## Visión general

Esta es una actualización y agregación de las siguientes 4 propuestas:

- 110 LS2
- 120 Meta LS2 para multihoming masivo
- 121 LS2 Cifrado
- 122 Búsqueda de servicio sin autenticación (anycasting)

Estas propuestas son mayormente independientes, pero por coherencia definimos y usamos un   formato común para varias de ellas.

Las siguientes propuestas están relacionadas:

- 140 Multihoming Invisible (incompatible con esta propuesta)
- 142 Nueva Plantilla de Criptografía (para nueva criptografía simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 para LS2 Cifrado
- 150 Protocolo Garlic Farm
- 151 ECDSA Blinding

## Propuesta

Esta propuesta define 5 nuevos tipos de DatabaseEntry y el proceso para   almacenarlos y recuperarlos desde la base de datos de red,   así como el método para firmarlos y verificar esas firmas.

### Objetivos

- Compatibilidad hacia atrás
- LS2 usable con multihoming de estilo antiguo
- No se requiere nueva criptografía ni primitivas para el soporte
- Mantener la desacoplación entre criptografía y firma; soportar todas las versiones actuales y futuras
- Habilitar claves de firma opcionales fuera de línea
- Reducir la precisión de las marcas de tiempo para reducir el rastreo por huellas
- Habilitar nueva criptografía para destinos
- Habilitar multihoming masivo
- Corregir múltiples problemas con el LS cifrado existente
- Ofuscar opcionalmente para reducir la visibilidad por floodfills
- Cifrado soporta tanto claves únicas como múltiples claves revocables
- Búsqueda de servicios para facilitar la búsqueda de outproxies, arranque de DHT de aplicaciones,  
  y otros usos
- No romper nada que dependa de hashes binarios de destino de 32 bytes, por ejemplo bittorrent
- Añadir flexibilidad a leasesets mediante propiedades, como tenemos en routerinfos.
- Poner la marca de tiempo de publicación y expiración variable en el encabezado, para que funcione incluso  
  si el contenido está cifrado (no derivar la marca de tiempo de la primera lease)
- Todos los nuevos tipos viven en el mismo espacio DHT y ubicaciones que los leasesets existentes,  
  para que los usuarios puedan migrar del antiguo LS a LS2,  
  o cambiar entre LS2, Meta y Cifrado,  
  sin cambiar el Destino o el hash.
- Un Destino existente puede convertirse para usar claves fuera de línea,  
  o volver a claves en línea, sin cambiar el Destino o el hash.

### No objetivos / Fuera de alcance

- Nuevo algoritmo de rotación DHT o generación compartida de números aleatorios
- El tipo específico de nueva encriptación y esquema de cifrado extremo a extremo  
  para usar ese nuevo tipo estaría en una propuesta separada.  
  No se especifica ni discute nueva criptografía aquí.
- Nueva encriptación para RIs o construcción de túneles.  
  Eso estaría en una propuesta separada.
- Métodos de encriptación, transmisión y recepción de mensajes I2NP DLM / DSM / DSRM.  
  No cambia.
- Cómo generar y soportar Meta, incluyendo comunicación inter-routers, gestión, conmutación por error y coordinación.  
  El soporte podría añadirse a I2CP, o i2pcontrol, o un nuevo protocolo.  
  Esto podría o no estandarizarse.
- Cómo implementar y gestionar realmente túneles de expiración más larga, o cancelar túneles existentes.  
  Es extremadamente difícil, y sin ello, no puedes tener un apagado ordenado razonable.
- Cambios en el modelo de amenazas
- Formato de almacenamiento fuera de línea, o métodos para almacenar/recuperar/compartir los datos.
- Los detalles de implementación no se discuten aquí y se dejan a cada proyecto.

### Justificación

LS2 añade campos para cambiar el tipo de encriptación y para futuros cambios de protocolo.

LS2 Cifrado corrige varios problemas de seguridad del LS cifrado existente mediante   el uso de encriptación asimétrica de todo el conjunto de leases.

Meta LS2 proporciona multihoming flexible, eficiente, efectivo y a gran escala.

El Registro de Servicio y la Lista de Servicios proporcionan servicios anycast como búsqueda de nombres   y arranque de DHT.

### Tipos de Datos NetDB

Los números de tipo se usan en los mensajes I2NP de Búsqueda/Almacenamiento en la Base de Datos.

La columna de extremo a extremo indica si las consultas/respuestas se envían a un Destino en un mensaje Garlic.

Tipos existentes:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Nuevos tipos:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Notas

- Los tipos de búsqueda actualmente usan los bits 3-2 en el mensaje de Búsqueda en la Base de Datos.  
  Cualquier tipo adicional requeriría el uso del bit 4.

- Todos los tipos de almacenamiento son impares, ya que los bits superiores en el campo de tipo del mensaje de Almacenamiento en la Base de Datos  
  son ignorados por routers antiguos.  
  Preferimos que el análisis falle como un LS que como un RI comprimido.

- ¿Debe el tipo ser explícito, implícito o ninguno en los datos cubiertos por la firma?

### Proceso de Búsqueda/Almacenamiento

Los tipos 3, 5 y 7 pueden devolverse como respuesta a una búsqueda estándar de leaseset (tipo 1).   El tipo 9 nunca se devuelve como respuesta a una búsqueda.   El tipo 11 se devuelve como respuesta a un nuevo tipo de búsqueda de servicio (tipo 11).

Solo el tipo 3 puede enviarse en un mensaje Garlic de cliente a cliente.

### Formato

Los tipos 3, 7 y 9 tienen un formato común::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Encabezado Estándar LS2

Parte Específica del Tipo

### Consideraciones de Privacidad/Seguridad

Firma Estándar LS2:

## Encabezado Estándar LS2

El tipo 5 (Cifrado) no comienza con un Destino y tiene un   formato diferente. Ver más abajo.

### Formato

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Justificación

  - como se define a continuación

  - como se define a continuación en cada parte

  - Longitud según el tipo de firma de la clave de firma

- No publicado/publicado: Para uso al enviar un almacenamiento de base de datos extremo a extremo,  
  el router emisor puede desear indicar que este leaseset no debería enviarse a otros. Actualmente usamos heurísticas para mantener este estado.

### Problemas

- Publicado: Reemplaza la lógica compleja necesaria para determinar la 'versión' del  
  leaseset. Actualmente, la versión es la expiración de la última lease,  
  y un router publicador debe incrementar esa expiración al menos 1ms al  
  publicar un leaseset que solo elimina una lease más antigua.

- Expira: Permite que la expiración de una entrada de base de datos sea anterior a la de  
  su última lease. Puede no ser útil para LS2, donde se espera que los leasesets  
  permanezcan con una expiración máxima de 11 minutos, pero  
  para otros nuevos tipos, es necesario (ver Meta LS y Registro de Servicio más abajo).

- Las claves fuera de línea son opcionales, para reducir la complejidad inicial/obligatoria de implementación.

### Notas

- Podría reducirse aún más la precisión de la marca de tiempo (¿10 minutos?) pero habría que añadir  
  un número de versión. Esto podría romper el multihoming, a menos que tengamos encriptación que preserve el orden?  
  Probablemente no se pueda hacer sin marcas de tiempo.

- Alternativa: marca de tiempo de 3 bytes (época / 10 minutos), versión de 1 byte, expiración de 2 bytes

- ¿Es el tipo explícito o implícito en los datos / firma? ¿Constantes de "dominio" para la firma?

## Nuevos tipos DatabaseEntry

### LeaseSet 2

El tipo 11 (Lista de Servicios) es una agregación de varios Registros de Servicio y tiene un   formato diferente. Ver más abajo.

- Los routers no deberían publicar un LS más de una vez por segundo.  
  Si lo hacen, deben incrementar artificialmente la marca de tiempo publicada en 1  
  sobre el LS publicado anteriormente.

TBD

    Standard LS flag (1)
Los tipos 3, 7 y 9 usan el encabezado estándar LS2, especificado a continuación:

    Standard LS2 type (3)
Cambios respecto al LeaseSet existente:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Buscar con

    10 minutes, as in a regular LS.
Almacenar con

    Destination

### Formato

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Justificación

- Las implementaciones de routers podrían almacenar en caché las claves y firma transitorias para  
  evitar la verificación cada vez. En particular, los floodfills y los routers en  
  ambos extremos de conexiones de larga duración podrían beneficiarse de esto.

- Las claves y firma fuera de línea solo son apropiadas para destinos de larga duración,  
  es decir, servidores, no clientes.

### Discusión

Almacenar en

Expiración típica

Publicado por

- Añadir marca de tiempo de publicación, marca de tiempo de expiración, flags y propiedades
- Añadir tipo de encriptación
- Eliminar clave de revocación

Esta propuesta continúa usando la clave pública en el leaseset para la   clave de encriptación extremo a extremo, y deja el campo de clave pública en el   Destino sin usar, como está ahora. El tipo de encriptación no se especifica   en el certificado de clave del Destino, seguirá siendo 0.

- Propiedades: Expansión futura y flexibilidad.  
  Colocadas primero por si son necesarias para el análisis de los datos restantes.

### Nuevos Problemas de Encriptación

Una alternativa rechazada es especificar el tipo de encriptación en el certificado de clave del Destino,   usar la clave pública en el Destino, y no usar la clave pública   en el leaseset. No tenemos previsto hacer esto.

- Múltiples pares tipo de encriptación/clave pública son  
  para facilitar la transición a nuevos tipos de encriptación. La otra forma de hacerlo  
  es publicar múltiples leasesets, posiblemente usando los mismos túneles,  
  como hacemos ahora para destinos DSA y EdDSA.  
  La identificación del tipo de encriptación entrante en un túnel  
  puede hacerse con el mecanismo existente de etiqueta de sesión,  
  y/o descifrado de prueba usando cada clave. Las longitudes de los mensajes  
  entrantes también pueden proporcionar una pista.

- La ubicación de la clave pública real no cambia.
- El tipo de encriptación o la clave pública pueden cambiar sin cambiar el Destino.
- Elimina el campo de revocación no utilizado
- Compatibilidad básica con otros tipos DatabaseEntry en esta propuesta
- Permite múltiples tipos de encriptación

- La ubicación de la clave pública y el tipo de encriptación difiere de RouterInfo
- Mantiene la clave pública no utilizada en el leaseset
- Requiere implementación en toda la red; en la alternativa, tipos de encriptación experimentales pueden usarse, si los permiten los floodfills  
  (pero ver propuestas relacionadas 136 y 137 sobre soporte para tipos de firma experimentales).  
  La propuesta alternativa podría ser más fácil de implementar y probar para tipos de encriptación experimentales.

### Notas

- El tipo de encriptación representa la combinación  
  de curva, longitud de clave y esquema extremo a extremo,  
  incluyendo KDF y MAC, si los hay.

- Hemos incluido un campo de longitud de clave, para que el LS2 sea  
  analizable y verificable por el floodfill incluso para tipos de encriptación desconocidos.

- El primer nuevo tipo de encriptación que se propondrá será  
  probablemente ECIES/X25519. Cómo se usa extremo a extremo  
  (ya sea una versión ligeramente modificada de ElGamal/AES+SessionTag  
  o algo completamente nuevo, por ejemplo ChaCha/Poly) se especificará  
  en una o más propuestas separadas.  
  Ver también las propuestas ECIES 144 y 145.

### LS2 Cifrado

Beneficios de LS2:

- La expiración de 8 bytes en leases cambia a 4 bytes.

Desventajas de LS2:

Algunas partes están fuera del alcance de esta propuesta,   pero ponemos notas aquí por ahora ya que no tenemos   una propuesta de encriptación separada todavía.   Ver también las propuestas ECIES 144 y 145.

- Si alguna vez implementamos revocación, podemos hacerlo con un campo de expiración de cero,  
  o leases de cero, o ambos. No necesitamos una clave de revocación separada.

Objetivos:

    Standard LS flag (1)
LS2 Cifrado nunca se envía en un mensaje garlic extremo a extremo.   Usa el LS2 Estándar como arriba.

    Encrypted LS2 type (5)
Cambios respecto al LeaseSet cifrado existente:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Buscar con

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Almacenar con

    Destination


### Definiciones

Almacenar en

Expiración típica

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Publicado por

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Definimos las siguientes funciones correspondientes a los bloques criptográficos usados   para LS2 Cifrado:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Formato

SIG

- Las claves de encriptación están en orden de preferencia del servidor, la más preferida primero.  
  El comportamiento predeterminado del cliente es seleccionar la primera clave con  
  un tipo de encriptación soportado. Los clientes pueden usar otros algoritmos de selección  
  basados en soporte de encriptación, rendimiento relativo y otros factores.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

El formato de LS2 cifrado consta de tres capas anidadas:

#### Capa 0 (externa)

El formato general es::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Nota que LS2 cifrado está ofuscado. El Destino no está en el encabezado.   La ubicación de almacenamiento DHT es SHA-256(tipo de firma || clave pública ofuscada), y se rota diariamente.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

NO usa el encabezado LS2 estándar especificado anteriormente.

    Length as implied by sig type

Tipo

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Tipo de Firma de Clave Pública Ofuscada

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Clave Pública Ofuscada

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Marca de tiempo de publicación

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

Expira

    2 bytes, big endian

Flags

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Datos de clave transitoria

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Capa 1 (intermedia)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Firma

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


Flags

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Capa 2 (interna)

Datos de autenticación de cliente DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Datos de autenticación de cliente PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Derivación de Clave Ofuscada

innerCiphertext

Tipo

#### Objetivos

- Añadir ofuscación
- Permitir múltiples tipos de firma
- No requerir nuevas primitivas criptográficas
- Opcionalmente cifrar a cada destinatario, revocable
- Soportar cifrado solo de LS2 Estándar y Meta LS2

#### Seguridad

Datos

#### Definiciones

Usamos el siguiente esquema para ofuscar claves,   basado en Ed25519 y [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   Las firmas Re25519 son sobre la curva Ed25519, usando SHA-512 para el hash.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

No usamos [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3),   que tiene objetivos de diseño similares, porque sus claves públicas ofuscadas   pueden estar fuera del subgrupo de orden primo, con implicaciones de seguridad desconocidas.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

La seguridad de un esquema de ofuscación requiere que la   distribución de alpha sea la misma que las claves privadas sin ofuscar.   Sin embargo, cuando ofuscamos una clave privada Ed25519 (tipo de firma 7)   a una clave privada Red25519 (tipo de firma 11), la distribución es diferente.   Para cumplir con los requisitos de [zcash sección 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   se debería usar Red25519 (tipo de firma 11) también para las claves sin ofuscar, para que   "la combinación de una clave pública realeatorizada y firma(s)   bajo esa clave no revele la clave de la cual fue realeatorizada".   Permitimos el tipo 7 para destinos existentes, pero recomendamos   el tipo 11 para nuevos destinos que serán cifrados.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Cálculos de Ofuscación

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
Una nueva clave secreta alpha y claves ofuscadas deben generarse cada día (UTC).   La clave secreta alpha y las claves ofuscadas se calculan como sigue.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), para todas las partes:

#### Firmado

BLIND_PRIVKEY(), para el propietario que publica el leaseset:

BLIND_PUBKEY(), para los clientes que recuperan el leaseset:

Ambos métodos de cálculo de A' producen el mismo resultado, como se requiere.

El leaseset sin ofuscar está firmado por la clave privada de firma Ed25519 o Red25519 sin ofuscar   y verificado con la clave pública de firma Ed25519 o Red25519 sin ofuscar (tipos de firma 7 u 11) como de costumbre.

#### Cálculos de Firma/Verificación

Si la clave pública de firma está fuera de línea,   el leaseset sin ofuscar está firmado por la clave privada de firma transitoria Ed25519 o Red25519 sin ofuscar   y verificado con la clave pública de firma transitoria Ed25519 o Red25519 sin ofuscar (tipos de firma 7 u 11) como de costumbre.   Ver más abajo para notas adicionales sobre claves fuera de línea para leasesets cifrados.

Para la firma del leaseset cifrado, usamos Red25519, basado en [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   para firmar y verificar con claves ofuscadas.   Las firmas Red25519 son sobre la curva Ed25519, usando SHA-512 para el hash.

Red25519 es idéntico a Ed25519 estándar excepto como se especifica a continuación.

La parte externa del leaseset cifrado usa claves y firmas Red25519.

Red25519 es casi idéntico a Ed25519. Hay dos diferencias:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Las claves privadas Red25519 se generan a partir de números aleatorios y luego deben reducirse mod L, donde L se define arriba.   Las claves privadas Ed25519 se generan a partir de números aleatorios y luego "ajustan" usando   enmascaramiento bit a bit a los bytes 0 y 31. Esto no se hace para Red25519.   Las funciones GENERATE_ALPHA() y BLIND_PRIVKEY() definidas arriba generan claves privadas Red25519 adecuadas usando mod L.

```text
// same as in Ed25519
```
### Encriptación y procesamiento

#### Derivación de subcredenciales

En Red25519, el cálculo de r para la firma usa datos aleatorios adicionales,   y usa el valor de la clave pública en lugar del hash de la clave privada.   Debido a los datos aleatorios, cada firma Red25519 es diferente, incluso   al firmar los mismos datos con la misma clave.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Firmado:

Verificación:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Como parte del proceso de ofuscación, necesitamos asegurar que un LS2 cifrado solo pueda ser   descifrado por alguien que conozca la clave pública de firma del Destino correspondiente.   No se requiere el Destino completo.   Para lograr esto, derivamos una credencial de la clave pública de firma:

#### Encriptación de capa 1

La cadena de personalización asegura que la credencial no colisione con ningún hash usado   como clave de búsqueda DHT, como el hash simple del Destino.

```text
outerInput = subcredential || publishedTimestamp
```
Para una clave ofuscada dada, podemos derivar una subcredencial:

```text
outerSalt = CSRNG(32)
```
La subcredencial se incluye en los procesos de derivación de clave más abajo, lo que enlaza esas   claves al conocimiento de la clave pública de firma del Destino.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Primero, se prepara la entrada para el proceso de derivación de clave:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Descifrado de capa 1

Luego, se genera una sal aleatoria:

```text
outerSalt = outerCiphertext[0:31]
```
Luego, se deriva la clave usada para cifrar la capa 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Finalmente, se cifra y serializa el texto plano de la capa 1:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Encriptación de capa 2

La sal se analiza desde el texto cifrado de la capa 1:

Luego, se deriva la clave usada para cifrar la capa 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Descifrado de capa 2

Finalmente, se descifra el texto cifrado de la capa 1:

Cuando la autorización de cliente está habilitada, se calcula ``authCookie`` como se describe más abajo.   Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el array de bytes de longitud cero.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Autorización por cliente

El cifrado procede de forma similar a la capa 1:

Cuando la autorización de cliente está habilitada, se calcula ``authCookie`` como se describe más abajo.   Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el array de bytes de longitud cero.

#### Autorización de cliente DH

El descifrado procede de forma similar a la capa 1:

Cuando la autorización de cliente está habilitada para un Destino, el servidor mantiene una lista de   clientes a los que autoriza para descifrar los datos del LS2 cifrado. Los datos almacenados por cliente   dependen del mecanismo de autorización, e incluyen alguna forma de material de clave que cada   cliente genera y envía al servidor mediante un mecanismo seguro fuera de banda.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Hay dos alternativas para implementar la autorización por cliente:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Cada cliente genera un par de claves DH ``[csk_i, cpk_i]``, y envía la clave pública ``cpk_i``   al servidor.

Procesamiento del servidor   ^^^^^^^^^^^^^^^^^ El servidor genera un nuevo ``authCookie`` y un par de claves DH efímero:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Luego, para cada cliente autorizado, el servidor cifra ``authCookie`` con su clave pública:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Autorización de cliente con clave precompartida

El servidor coloca cada tupla ``[idCliente_i, cookieCliente_i]`` en la capa 1 del   LS2 cifrado, junto con ``epk``.

Procesamiento del cliente   ^^^^^^^^^^^^^^^^^ El cliente usa su clave privada para derivar su identificador de cliente esperado ``idCliente_i``,   clave de cifrado ``claveCliente_i``, y IV de cifrado ``ivCliente_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Luego, el cliente busca en los datos de autorización de la capa 1 una entrada que contenga   ``idCliente_i``. Si existe una entrada coincidente, el cliente la descifra para obtener   ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Cada cliente genera una clave secreta de 32 bytes ``psk_i``, y la envía al servidor.   Alternativamente, el servidor puede generar la clave secreta, y enviársela a uno o más clientes.

Procesamiento del servidor   ^^^^^^^^^^^^^^^^^ El servidor genera un nuevo ``authCookie`` y una sal:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Luego, para cada cliente autorizado, el servidor cifra ``authCookie`` con su clave precompartida:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Consideraciones de seguridad

El servidor coloca cada tupla ``[idCliente_i, cookieCliente_i]`` en la capa 1 del   LS2 cifrado, junto con ``authSalt``.

Procesamiento del cliente   ^^^^^^^^^^^^^^^^^ El cliente usa su clave precompartida para derivar su identificador de cliente esperado ``idCliente_i``,   clave de cifrado ``claveCliente_i``, y IV de cifrado ``ivCliente_i``:

Luego, el cliente busca en los datos de autorización de la capa 1 una entrada que contenga   ``idCliente_i``. Si existe una entrada coincidente, el cliente la descifra para obtener   ``authCookie``:

Ambos mecanismos de autorización de cliente anteriores proporcionan privacidad para la membresía de clientes.   Una entidad que solo conozca el Destino puede ver cuántos clientes están suscritos en cualquier   momento, pero no puede rastrear qué clientes se están añadiendo o revocando.

- Cifrar todo por seguridad
- Cifrar de forma segura, no solo con AES.
- Cifrar a cada destinatario

Los servidores DEBERÍAN aleatorizar el orden de los clientes cada vez que generen un LS2 cifrado, para   evitar que los clientes aprendan su posición en la lista e infieran cuándo se han añadido o revocado otros clientes.

- Una capa externa que contiene la información en texto claro necesaria para almacenamiento y recuperación.
- Una capa intermedia que maneja la autenticación del cliente.
- Una capa interna que contiene los datos reales de LS2.

Un servidor PUEDE optar por ocultar el número de clientes suscritos insertando entradas aleatorias   en la lista de datos de autorización.

- La clave pública de firma en el destino sin ofuscar debe ser  
  Ed25519 (tipo de firma 7) o Red25519 (tipo de firma 11);  
  no se admiten otros tipos de firma
- Si la clave pública de firma está fuera de línea, la clave pública de firma transitoria también debe ser Ed25519
- La ofuscación es computacionalmente simple
- Usar primitivas criptográficas existentes
- Las claves públicas ofuscadas no pueden desofuscarse
- Las claves públicas ofuscadas deben estar en la curva Ed25519 y en el subgrupo de orden primo
- Debe conocerse la clave pública de firma del destino  
  (no se requiere el destino completo) para derivar la clave pública ofuscada
- Opcionalmente proporcionar un secreto adicional requerido para derivar la clave pública ofuscada

Ventajas de la autorización de cliente DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La seguridad del esquema no depende únicamente del intercambio fuera de banda del material de clave del cliente.  
  La clave privada del cliente nunca necesita salir de su dispositivo, y por tanto un  
  adversario que pueda interceptar el intercambio fuera de banda, pero no pueda romper el algoritmo DH,  
  no puede descifrar el LS2 cifrado, ni determinar cuánto tiempo se le da acceso al cliente.

### LS Cifrado con Direcciones Base 32

Desventajas de la autorización de cliente DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ventajas de la autorización de cliente PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### LS Cifrado con Claves Fuera de Línea

Desventajas de la autorización de cliente PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ver propuesta 149.

No puedes usar un LS2 cifrado para bittorrent, debido a las respuestas compactas de anuncio que son de 32 bytes.   Los 32 bytes contienen solo el hash. No hay espacio para indicar que el   leaseset está cifrado, o los tipos de firma.

### Notas

- Requiere N + 1 operaciones DH en el lado del servidor para N clientes.
- Requiere una operación DH en el lado del cliente.
- Requiere que el cliente genere la clave secreta.

- No requiere operaciones DH.
- Permite que el servidor genere la clave secreta.
- Permite que el servidor comparta la misma clave con múltiples clientes, si se desea.

- La seguridad del esquema depende críticamente del intercambio fuera de banda del material de clave del cliente.  
  Un adversario que intercepte el intercambio para un cliente particular puede descifrar  
  cualquier LS2 cifrado posterior para el cual ese cliente esté autorizado, así como determinar  
  cuándo se revoca el acceso del cliente.

- Un servicio que use leasesets cifrados publicaría la versión cifrada a los  
  floodfills. Sin embargo, por eficiencia, enviaría leasesets sin cifrar a  
  clientes en el mensaje garlic envuelto, una vez autenticado (por ejemplo, mediante lista blanca).

- Los floodfills pueden limitar el tamaño máximo a un valor razonable para prevenir abusos.

### Meta LS2

Para leasesets cifrados con claves fuera de línea, las claves privadas ofuscadas también deben generarse fuera de línea,   una por cada día.

Como el bloque opcional de firma fuera de línea está en la parte en texto claro del leaseset cifrado,   cualquiera que rastree los floodfills podría usar esto para rastrear el leaseset (pero no descifrarlo)   durante varios días.   Para evitar esto, el propietario de las claves debería generar nuevas claves transitorias   para cada día también.   Tanto las claves transitorias como las ofuscadas pueden generarse por adelantado, y entregarse al router   por lotes.

No se define en esta propuesta un formato de archivo para empaquetar múltiples claves transitorias y   ofuscadas y proporcionarlas al cliente o router.   No se define en esta propuesta una mejora del protocolo I2CP para soportar   leasesets cifrados con claves fuera de línea.

Se usa para reemplazar el multihoming. Como cualquier leaseset, está firmado por el   creador. Es una lista autenticada de hashes de destino.

Meta LS2 es la parte superior, y posiblemente nodos intermedios,   de una estructura de árbol.   Contiene un número de entradas, cada una apuntando a un LS, LS2 o otro Meta LS2   para soportar multihoming masivo.   Un Meta LS2 puede contener una mezcla de entradas LS, LS2 y Meta LS2.   Las hojas del árbol siempre son un LS o LS2.   El árbol es un DAG; se prohíben bucles; los clientes que hacen búsquedas deben detectar y   rechazar seguir bucles.

Un Meta LS2 puede tener una expiración mucho más larga que un LS o LS2 estándar.   El nivel superior puede tener una expiración varias horas después de la fecha de publicación.   El tiempo máximo de expiración será aplicado por floodfills y clientes, y está por determinar.

El caso de uso para Meta LS2 es multihoming masivo, pero sin más   protección para la correlación de routers con leasesets (en el reinicio del router) que   la proporcionada actualmente con LS o LS2.   Esto es equivalente al caso de uso de "facebook", que probablemente no necesita   protección contra correlación. Este caso de uso probablemente necesita claves fuera de línea,   que se proporcionan en el encabezado estándar en cada nodo del árbol.

El protocolo de back-end para coordinación entre los routers hoja, firmantes intermedios y maestros de Meta LS   no se especifica aquí. Los requisitos son extremadamente simples: solo verificar que el par está activo,   y publicar un nuevo LS cada pocas horas. La única complejidad es para elegir nuevos   publicadores para los Meta LS de nivel superior o intermedio en caso de fallo.

Leasesets mixtos donde leases de múltiples routers se combinan, firman y publican   en un solo leaseset se documentan en la propuesta 140, "multihoming invisible".   Esta propuesta es inviable tal como está escrita, porque las conexiones de streaming no serían   "pegajosas" a un solo router, ver http://zzz.i2p/topics/2335 .

El protocolo de back-end, y la interacción con los componentes internos del router y cliente, sería   bastante complejo para el multihoming invisible.

    Standard LS flag (1)
Para evitar sobrecargar el floodfill para el Meta LS de nivel superior, la expiración debería   ser de varias horas como mínimo. Los clientes deben almacenar en caché el Meta LS de nivel superior, y   persistirlo entre reinicios si no ha expirado.

    Meta LS2 type (7)
Necesitamos definir algún algoritmo para que los clientes recorran el árbol, incluyendo alternativas,   para que el uso se disperse. Alguna función de distancia de hash, costo y aleatoriedad.   Si un nodo tiene tanto LS o LS2 como Meta LS, necesitamos saber cuándo está permitido   usar esos leasesets, y cuándo seguir recorriendo el árbol.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Buscar con

    Hours. Max 18.2 hours (65535 seconds)
Almacenar con

    "master" Destination or coordinator, or intermediate coordinators

### Formato

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Almacenar en

### Notas

- Después del descifrado, se deben hacer varias comprobaciones, incluyendo que  
  la marca de tiempo interna y la expiración coincidan con las del nivel superior.

- ChaCha20 fue seleccionado sobre AES. Aunque las velocidades son similares si  
  el soporte de hardware AES está disponible, ChaCha20 es 2.5-3 veces más rápido cuando  
  el soporte de hardware AES no está disponible, como en dispositivos ARM de gama baja.

- No nos importa lo suficiente la velocidad como para usar BLAKE2b con clave. Tiene un tamaño de salida  
  lo suficientemente grande para acomodar el mayor n que requerimos (o podemos llamarlo una vez por  
  clave deseada con un argumento contador). BLAKE2b es mucho más rápido que SHA-256, y  
  BLAKE2b con clave reduciría el número total de llamadas a funciones hash.  
  Sin embargo, ver propuesta 148, donde se propone que cambiemos a BLAKE2b por otras razones.  
  Ver [rendimiento de derivación segura de claves](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Registro de Servicio

Expiración típica

Publicado por

Flags y propiedades: para uso futuro

    n/a, see Service List
Este es un registro individual que indica que un destino está participando en un   servicio. Se envía desde el participante al floodfill. Nunca se envía   individualmente por un floodfill, sino solo como parte de una Lista de Servicios. El Registro de Servicio también se usa para revocar la participación en un servicio, estableciendo la   expiración en cero.

    Service Record type (9)
Esto no es un LS2 pero usa el formato estándar de encabezado y firma LS2.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Buscar con

    Hours. Max 18.2 hours (65535 seconds)
Almacenar con

    Destination

### Formato

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notas

- Un servicio distribuido que use esto tendría uno o más "maestros" con la  
  clave privada del destino del servicio. Determinarían (fuera de banda) la  
  lista actual de destinos activos y publicarían el Meta LS2. Para  
  redundancia, múltiples maestros podrían hacer multihoming (es decir, publicar simultáneamente) el  
  Meta LS2.

- Un servicio distribuido podría comenzar con un solo destino o usar multihoming de estilo antiguo,  
  luego pasar a un Meta LS2. Una búsqueda LS estándar podría devolver  
  cualquiera de un LS, LS2 o Meta LS2.

- Cuando un servicio usa un Meta LS2, no tiene túneles (leases).

### Lista de Servicios

Almacenar en

Expiración típica

Publicado por

Esto no es nada parecido a un LS2 y usa un formato diferente.

La lista de servicios es creada y firmada por el floodfill. Es no autenticada   en el sentido de que cualquiera puede unirse a un servicio publicando un Registro de Servicio a un   floodfill.

Una Lista de Servicios contiene Registros de Servicio Cortos, no Registros de Servicio completos. Estos   contienen firmas pero solo hashes, no destinos completos, por lo que no pueden verificarse sin el destino completo.

    Service List lookup type (11)
La seguridad, si la hay, y la conveniencia de las listas de servicios está por determinar.   Los floodfills podrían limitar la publicación y búsquedas a una lista blanca de servicios,   pero esa lista blanca puede variar según la implementación o preferencia del operador.   Puede no ser posible lograr consenso sobre una lista blanca común y básica   entre implementaciones.

    Service List type (11)
Si el nombre del servicio se incluye en el registro de servicio anterior,   entonces los operadores de floodfill pueden objetar; si solo se incluye el hash,   no hay verificación, y un registro de servicio podría "entrar" antes que   cualquier otro tipo netdb y almacenarse en el floodfill.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Buscar con

    Hours, not specified in the list itself, up to local policy
Almacenar con

    Nobody, never sent to floodfill, never flooded.

### Formato

Almacenar en

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Expiración típica

- Si expira es todo cero, el floodfill debería revocar el registro y ya no  
  incluirlo en la lista de servicios.

Publicado por

- Almacenamiento: El floodfill puede limitar estrictamente el almacenamiento de estos registros y  
  limitar el número de registros almacenados por hash y su expiración. También puede usarse  
  una lista blanca de hashes.

NO usa el encabezado LS2 estándar especificado anteriormente.

- Cualquier otro tipo netdb en el mismo hash tiene prioridad, por lo que un registro de servicio nunca puede  
  sobrescribir un LS/RI, pero un LS/RI sobrescribirá todos los registros de servicio en ese hash.

### Notas

- anteponer el hash del nombre del servicio
- eliminar el hash del creador
- Verificar la firma del contenido modificado

- Obtener el destino
- Verificar la firma de (marca de tiempo de publicación + expira + flags + puerto + Hash del  
  nombre del servicio)

- Obtener el destino
- Verificar la firma de (marca de tiempo de publicación + 4 bytes cero + flags + puerto + Hash  
  del nombre del servicio)

## Cambios Requeridos en la Especificación de Estructuras Comunes

### Certificados de Clave

Para verificar la firma de la Lista de Servicios:

### Nuevas Estructuras Intermedias

Para verificar la firma de cada Registro de Servicio Corto:

### Nuevos Tipos NetDB

Para verificar la firma de cada Registro de Revocación:

### Nuevo Tipo de Firma

Fuera del alcance de esta propuesta.   Añadir a las propuestas ECIES 144 y 145.

## Cambios requeridos en la especificación de cifrado

Añadir nuevas estructuras para Lease2, MetaLease, LeaseSet2Header y OfflineSignature.   Efectivo a partir de la versión 0.9.38.

## Cambios requeridos en I2NP

Añadir estructuras para cada nuevo tipo de leaseset, incorporadas de arriba.   Para LeaseSet2, EncryptedLeaseSet y MetaLeaseSet,   efectivo a partir de la versión 0.9.38.   Para Registro de Servicio y Lista de Servicios,   preliminar y no programado.

### Mensaje de búsqueda en la base de datos

Añadir RedDSA_SHA512_Ed25519 Tipo 11.   Clave pública de 32 bytes; clave privada de 32 bytes; hash de 64 bytes; firma de

### Cambios

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Mensaje de almacenamiento de base de datos

Añada todos los nuevos tipos de almacenamiento.

### Cambios

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## Cambios requeridos en I2CP

### Opciones de I2CP

Nuevas opciones interpretadas del lado del router, enviadas en el SessionConfig Mapping:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Nuevas opciones interpretadas del lado del cliente:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Configuración de sesión

Tenga en cuenta que para las firmas offline se requieren las opciones i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey e i2cp.leaseSetOfflineSignature, y la firma la realiza la clave privada de firma transitoria.

### Mensaje de solicitud de leaseSet

Del router al cliente. Sin cambios. Los leases se envían con timestamps de 8 bytes, incluso si el leaseset devuelto será un LS2 con timestamps de 4 bytes. Tenga en cuenta que la respuesta puede ser un mensaje Create Leaseset o Create Leaseset2.

### Mensaje de solicitud de leaseSet variable

Del router al cliente. Sin cambios. Los leases se envían con timestamps de 8 bytes, incluso si el leaseset devuelto será un LS2 con timestamps de 4 bytes. Tenga en cuenta que la respuesta puede ser un mensaje Create Leaseset o Create Leaseset2.

### Crear mensaje Leaseset2

De cliente a router. Mensaje nuevo, para usar en lugar de Create Leaseset Message.

### Justificación

- Usamos longitud de firma en lugar de tipo de firma para soportar tipos de firma desconocidos.

- No hay expiración de una lista de servicios, los receptores pueden tomar su propia  
  decisión según política o la expiración de los registros individuales.

- Las Listas de Servicios no se inundan, solo los Registros de Servicio individuales lo son. Cada  
  floodfill crea, firma y almacena en caché una Lista de Servicios. El floodfill usa su  
  propia política para el tiempo de caché y el número máximo de registros de servicio y revocación.

### Tipo de mensaje

El tipo de mensaje para el mensaje Create Leaseset2 es 41.

### Formato

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Notas

- La versión mínima del router es 0.9.39.
- La versión preliminar con el tipo de mensaje 40 estaba en 0.9.38, pero el formato fue cambiado.
  El tipo 40 está abandonado y no es compatible.

### Problemas

- Se necesitan más cambios para admitir LS cifrados y meta LS.

### Mensaje de información de blinding

Cliente a router. Nuevo mensaje.

### Justificación

- El router necesita saber si un destino está cegado.
  Si está cegado y utiliza autenticación secreta o por cliente,
  también necesita tener esa información.

- Un Host Lookup de una dirección b32 de formato nuevo ("b33")
  indica al router que la dirección está blinded, pero no hay ningún mecanismo para
  pasar la clave secreta o privada al router en el mensaje de Host Lookup.
  Si bien podríamos extender el mensaje de Host Lookup para añadir esa información,
  es más limpio definir un mensaje nuevo.

- Necesitamos una forma programática para que el cliente se lo indique al router. De lo contrario, el usuario tendría que configurar manualmente cada destino.

### Uso

Antes de que un cliente envíe un mensaje a un destino cegado, debe consultar el "b33" en un mensaje Host Lookup o enviar un mensaje Blinding Info. Si el destino cegado requiere un secreto o autenticación por cliente, el cliente debe enviar un mensaje Blinding Info.

El router no envía una respuesta a este mensaje.

### Tipo de mensaje

El tipo de mensaje para el Blinding Info Message es 42.

### Formato

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Notas

- La versión mínima del router es 0.9.43

### Problemas

### Mensaje de respuesta del host (enc)

Para admitir búsquedas de hostnames "b33" y devolver una indicación si el router no dispone de la información requerida, definimos códigos de resultado adicionales para el Host Reply Message, como se indica a continuación:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Los valores 1-255 ya están definidos como errores, por lo que no existe ningún problema de compatibilidad hacia atrás.

### Mensaje de redirección meta

Router a cliente. Mensaje nuevo.

### Justificación

Un cliente no sabe a priori que un Hash dado resolverá a un Meta LS.

Si una búsqueda de leaseset para un Destination devuelve un Meta LS, el router realizará la resolución recursiva. Para los datagramas, el lado del cliente no necesita saberlo; sin embargo, para streaming, donde el protocolo verifica el destino en el SYN ACK, debe saber cuál es el destino "real". Por lo tanto, necesitamos un nuevo mensaje.

### Uso

El router mantiene una caché para el destino real que se utiliza a partir de un meta LS. Cuando el cliente envía un mensaje a un destino que se resuelve a un meta LS, el router comprueba en la caché el último destino real utilizado. Si la caché está vacía, el router selecciona un destino del meta LS y busca el leaseset. Si la búsqueda del leaseset tiene éxito, el router añade ese destino a la caché y envía al cliente un Meta Redirect Message. Esto solo se hace una vez, a menos que el destino caduque y deba cambiarse. El cliente también debe almacenar en caché la información si es necesario. El Meta Redirect Message NO se envía como respuesta a cada SendMessage.

El router solo envía este mensaje a los clientes con versión 0.9.47 o superior.

El cliente no envía una respuesta a este mensaje.

### Tipo de mensaje

El tipo de mensaje para el Meta Redirect Message es 43.

### Formato

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Cambios para admitir Meta

Cómo generar y dar soporte a Meta, incluida la comunicación y coordinación entre routers, está fuera del alcance de esta propuesta. Véase la propuesta relacionada 150.

### Cambios para admitir claves offline

Las firmas offline no se pueden verificar en streaming ni en datagramas repliables. Véanse las secciones siguientes.

## Se requieren cambios en el archivo de clave privada

El formato del archivo de clave privada (eepPriv.dat) no forma parte oficial de nuestras especificaciones, pero está documentado en los [javadocs de Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) y otras implementaciones sí lo admiten. Esto permite la portabilidad de las claves privadas entre distintas implementaciones.

Son necesarios cambios para almacenar la clave pública transitoria y la información de firma sin conexión.

### Cambios

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Cambios necesarios en la CLI del archivo de clave privada

Añada soporte para las siguientes opciones:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Cambios necesarios en streaming

Actualmente, las firmas offline no se pueden verificar en streaming. El cambio siguiente añade el bloque de firma offline a las opciones. Esto evita tener que recuperar esta información mediante I2CP.

### Cambios

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Notas

- La alternativa es simplemente añadir un flag y recuperar la clave pública transitoria mediante I2CP
  (Véanse las secciones Host Lookup / Host Reply Message anteriores)

## Cambios necesarios en los datagramas con respuesta

Las firmas offline no se pueden verificar en el procesamiento de datagramas repliables. Se necesita un flag para indicar que están firmadas offline, pero no hay dónde colocar el flag. Requerirá un número y formato de protocolo completamente nuevos.

### Cambios

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Notas

- La alternativa es simplemente añadir un flag y obtener la clave pública transitoria mediante I2CP
  (Véanse las secciones Host Lookup / Host Reply Message anteriores)
- ¿Alguna otra opción que debamos añadir ahora que tenemos bytes de flag?

## Cambios requeridos en SAM V3

Se debe mejorar SAM para admitir firmas offline en el DESTINATION base 64.

### Cambios

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Tenga en cuenta que las firmas offline solo son compatibles con STREAM y RAW, no con DATAGRAM (hasta que definamos un nuevo protocolo DATAGRAM).

Tenga en cuenta que SESSION STATUS devolverá una Signing Private Key de todos ceros y los datos de Offline Signature exactamente como se suministraron en SESSION CREATE.

Tenga en cuenta que DEST GENERATE y SESSION CREATE DESTINATION=TRANSIENT no pueden usarse para crear un destino firmado offline.

### Problemas

¿Actualizar la versión a 3.4, o dejarla en 3.1/3.2/3.3 de modo que pueda añadirse sin requerir todo lo de 3.2/3.3?

Otros cambios por determinar. Consulte la sección I2CP Host Reply Message anterior.

## Cambios requeridos en BOB

Habría que mejorar BOB para admitir firmas offline y/o Meta LS. Esto es de baja prioridad y probablemente nunca se especifique ni se implemente. SAM V3 es la interfaz preferida.

## Publicación, Migración, Compatibilidad

LS2 (excepto LS2 cifrado) se publica en la misma ubicación de la DHT que LS1. No hay forma de publicar tanto un LS1 como un LS2, a menos que LS2 estuviera en una ubicación diferente.

El LS2 cifrado se publica en el hash del tipo de clave y los datos de clave cegados. Este hash se usa luego para generar la «routing key» diaria, como en LS1.

LS2 solo se usaría cuando se requieran nuevas funcionalidades (nueva criptografía, LS cifrado, metadatos, etc.). LS2 solo se puede publicar en floodfills de una versión especificada o superior.

Los servidores que publican LS2 sabrían que cualquier cliente que se conecte soporta LS2. Podrían enviar LS2 en el garlic.

Los clientes enviarían LS2 en garlics solo si usan criptografía nueva. ¿Los clientes compartidos usarían LS1 indefinidamente? TODO: ¿Cómo tener clientes compartidos que admitan tanto criptografía antigua como nueva?

## Despliegue

0.9.38 incluye soporte floodfill para LS2 estándar, incluidas las claves offline.

0.9.39 incluye soporte de I2CP para LS2 y Encrypted LS2, firma/verificación con sig type 11, soporte de floodfill para Encrypted LS2 (sig types 7 y 11, sin offline keys) y cifrado/descifrado de LS2 (sin autorización por cliente).

Está previsto que la versión 0.9.40 incluya soporte para cifrar/descifrar LS2 con autorización por cliente, soporte de floodfill e I2CP para Meta LS2, soporte para LS2 cifrado con claves offline y soporte de b32 para LS2 cifrado.

## Agradecimientos

El diseño cifrado de LS2 está fuertemente influenciado por [los descriptores de servicios ocultos v3 de Tor](https://spec.torproject.org/rend-spec-v3), que tenían objetivos de diseño similares.

## Referencias

* ["High-speed high-security signatures" de Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe y Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
