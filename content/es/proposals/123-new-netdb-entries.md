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

Partes de esta propuesta están completas e implementadas en 0.9.38 y 0.9.39. Las especificaciones de Common Structures, I2CP, I2NP y otras ahora están actualizadas para reflejar los cambios que se soportan actualmente.

Las partes completadas aún están sujetas a revisiones menores. Otras partes de esta propuesta aún están en desarrollo y sujetas a revisiones sustanciales.

Service Lookup (tipos 9 y 11) son de baja prioridad y no programados, y pueden separarse en una propuesta independiente.

## Resumen

Esta es una actualización y agregación de las siguientes 4 propuestas:

- 110 LS2
- 120 Meta LS2 para multihoming masivo
- 121 LS2 cifrado
- 122 Búsqueda de servicio no autenticada (anycasting)

Estas propuestas son en su mayoría independientes, pero por cordura definimos y utilizamos un formato común para varias de ellas.

Las siguientes propuestas están algo relacionadas:

- 140 Invisible Multihoming (incompatible con esta propuesta)
- 142 New Crypto Template (para nueva criptografía simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Propuesta

Esta propuesta define 5 nuevos tipos de DatabaseEntry y el proceso para almacenarlos y recuperarlos de la base de datos de red, así como el método para firmarlos y verificar esas firmas.

### Goals

- Compatible hacia atrás
- LS2 utilizable con multihoming de estilo antiguo
- No se requieren nuevos primitivos criptográficos o de cifrado para el soporte
- Mantener el desacoplamiento de cifrado y firma; soportar todas las versiones actuales y futuras
- Habilitar claves de firma offline opcionales
- Reducir la precisión de las marcas de tiempo para reducir el fingerprinting
- Habilitar nuevo cifrado para destinos
- Habilitar multihoming masivo
- Corregir múltiples problemas con los LS cifrados existentes
- Blinding opcional para reducir la visibilidad por parte de los floodfills
- El cifrado soporta tanto claves únicas como múltiples claves revocables
- Búsqueda de servicios para facilitar la búsqueda de outproxies, bootstrap de DHT de aplicaciones,
  y otros usos
- No romper nada que dependa de hashes de destino binarios de 32 bytes, ej. bittorrent
- Agregar flexibilidad a los leasesets mediante propiedades, como tenemos en los routerinfos.
- Poner la marca de tiempo publicada y la expiración variable en el encabezado, para que funcione incluso
  si el contenido está cifrado (no derivar la marca de tiempo del lease más temprano)
- Todos los nuevos tipos viven en el mismo espacio DHT y las mismas ubicaciones que los leasesets existentes,
  para que los usuarios puedan migrar del LS antiguo a LS2,
  o cambiar entre LS2, Meta, y Encrypted,
  sin cambiar el Destination o hash.
- Un Destination existente puede ser convertido para usar claves offline,
  o de vuelta a claves online, sin cambiar el Destination o hash.

### Non-Goals / Out-of-scope

- Nuevo algoritmo de rotación DHT o generación aleatoria compartida
- El tipo específico de cifrado nuevo y el esquema de cifrado de extremo a extremo
  para usar ese nuevo tipo estaría en una propuesta separada.
  No se especifica ni se discute criptografía nueva aquí.
- Nuevo cifrado para RIs o construcción de túneles.
  Eso estaría en una propuesta separada.
- Métodos de cifrado, transmisión y recepción de mensajes I2NP DLM / DSM / DSRM.
  No se cambia.
- Cómo generar y soportar Meta, incluyendo comunicación entre routers de backend, gestión, conmutación por error y coordinación.
  El soporte puede agregarse a I2CP, o i2pcontrol, o un nuevo protocolo.
  Esto puede o no estar estandarizado.
- Cómo implementar y gestionar realmente túneles de expiración más larga, o cancelar túneles existentes.
  Eso es extremadamente difícil, y sin ello, no puedes tener un apagado elegante razonable.
- Cambios en el modelo de amenazas
- Formato de almacenamiento sin conexión, o métodos para almacenar/recuperar/compartir los datos.
- Los detalles de implementación no se discuten aquí y se dejan a cada proyecto.

### Justification

LS2 añade campos para cambiar el tipo de cifrado y para futuros cambios de protocolo.

El LS2 cifrado corrige varios problemas de seguridad con el LS cifrado existente mediante el uso de cifrado asimétrico de todo el conjunto de leases.

Meta LS2 proporciona multihoming flexible, eficiente, efectivo y a gran escala.

Service Record y Service List proporcionan servicios anycast como búsqueda de nombres y arranque de DHT.

### Objetivos

Los números de tipo se utilizan en los Mensajes de Búsqueda/Almacenamiento de Base de Datos I2NP.

La columna end-to-end se refiere a si las consultas/respuestas se envían a un Destination en un Garlic Message.

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
### No objetivos / Fuera del alcance

- Los tipos de búsqueda son actualmente los bits 3-2 en el Database Lookup Message.
  Cualquier tipo adicional requeriría el uso del bit 4.

- Todos los tipos de almacén son impares ya que los bits superiores en el campo
  de tipo del Mensaje de Almacén de Base de Datos son ignorados por routers antiguos.
  Preferimos que el análisis falle como un LS que como un RI comprimido.

- ¿Debería el tipo ser explícito o implícito o ninguno de los dos en los datos cubiertos por la firma?

### Justificación

Los tipos 3, 5 y 7 pueden ser devueltos como respuesta a una consulta de leaseSet estándar (tipo 1). El tipo 9 nunca es devuelto como respuesta a una consulta. El tipo 11 es devuelto como respuesta a un nuevo tipo de consulta de servicio (tipo 11).

Solo el tipo 3 puede enviarse en un mensaje Garlic de cliente a cliente.

### Tipos de Datos de NetDB

Los tipos 3, 7 y 9 tienen todos un formato común::

Encabezado LS2 Estándar   - como se define a continuación

Parte Específica del Tipo   - como se define a continuación en cada parte

Firma LS2 Estándar:   - Longitud según el tipo de firma de la clave de firmado

El Tipo 5 (Cifrado) no comienza con un Destination y tiene un formato diferente. Ver más abajo.

El Tipo 11 (Lista de Servicios) es una agregación de varios Registros de Servicio y tiene un formato diferente. Ver más abajo.

### Notas

TBD

## Standard LS2 Header

Los tipos 3, 7 y 9 utilizan el encabezado LS2 estándar, especificado a continuación:

### Proceso de Lookup/Store

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
### Formato

- Unpublished/published: Para uso al enviar un database store de extremo a extremo,
  el router emisor puede desear indicar que este leaseset no debe ser
  enviado a otros. Actualmente usamos heurísticas para mantener este estado.

- Published: Reemplaza la lógica compleja requerida para determinar la 'versión' del
  leaseset. Actualmente, la versión es la expiración del lease que expira más tarde,
  y un router que publica debe incrementar esa expiración por al menos 1ms cuando
  publica un leaseset que solo elimina un lease más antiguo.

- Expires: Permite que la expiración de una entrada netDb sea anterior a la de su leaseSet que expira más tarde. Puede no ser útil para LS2, donde se espera que los leaseSets mantengan una expiración máxima de 11 minutos, pero para otros tipos nuevos, es necesario (ver Meta LS y Service Record más abajo).

- Las claves offline son opcionales, para reducir la complejidad inicial/requerida de implementación.

### Consideraciones de Privacidad/Seguridad

- Podría reducir aún más la precisión del timestamp (¿10 minutos?) pero tendría que agregar
  número de versión. Esto podría romper el multihoming, ¿a menos que tengamos cifrado que preserve el orden?
  Probablemente no se puede hacer sin timestamps en absoluto.

- Alternativa: marca de tiempo de 3 bytes (época / 10 minutos), versión de 1 byte, expira en 2 bytes

- ¿Es el tipo explícito o implícito en los datos / firma? ¿Constantes de "Domain" para la firma?

### Notes

- Los routers no deberían publicar un LS más de una vez por segundo.
  Si lo hacen, deben incrementar artificialmente el timestamp publicado en 1
  sobre el LS previamente publicado.

- Las implementaciones de router podrían almacenar en caché las claves transitorias y la firma para evitar la verificación cada vez. En particular, los floodfills y los routers en ambos extremos de conexiones de larga duración podrían beneficiarse de esto.

- Las claves sin conexión y la firma solo son apropiadas para destinos de larga duración,
  es decir, servidores, no clientes.

## New DatabaseEntry types

### Formato

Cambios desde el LeaseSet existente:

- Agregar marca de tiempo de publicación, marca de tiempo de expiración, flags y propiedades
- Agregar tipo de cifrado
- Eliminar clave de revocación

Buscar con

    Standard LS flag (1)
Almacenar con

    Standard LS2 type (3)
Almacenar en

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiración típica

    10 minutes, as in a regular LS.
Publicado por

    Destination

### Justificación

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
### Problemas

- Properties: Expansión futura y flexibilidad.
  Se coloca primero en caso de que sea necesario para el análisis de los datos restantes.

- Múltiples pares de tipo de cifrado/clave pública son
  para facilitar la transición a nuevos tipos de cifrado. La otra forma de hacerlo
  es publicar múltiples leasesets, posiblemente usando los mismos tunnels,
  como hacemos ahora para destinos DSA y EdDSA.
  La identificación del tipo de cifrado entrante en un tunnel
  puede hacerse con el mecanismo de session tag existente,
  y/o descifrado por prueba y error usando cada clave. Las longitudes de los
  mensajes entrantes también pueden proporcionar una pista.

### Notas

Esta propuesta continúa utilizando la clave pública en el leaseset para la clave de cifrado de extremo a extremo, y deja el campo de clave pública en el Destination sin usar, como está ahora. El tipo de cifrado no se especifica en el certificado de clave del Destination, permanecerá en 0.

Una alternativa rechazada es especificar el tipo de cifrado en el certificado de clave de Destination, usar la clave pública en el Destination, y no usar la clave pública en el leaseset. No planeamos hacer esto.

Beneficios de LS2:

- La ubicación de la clave pública real no cambia.
- El tipo de cifrado, o clave pública, puede cambiar sin modificar el Destination.
- Elimina el campo de revocación no utilizado
- Compatibilidad básica con otros tipos DatabaseEntry en esta propuesta
- Permite múltiples tipos de cifrado

Desventajas de LS2:

- La ubicación de la clave pública y el tipo de cifrado difieren del RouterInfo
- Mantiene una clave pública no utilizada en el leaseset
- Requiere implementación a través de la red; como alternativa, se pueden usar tipos de
  cifrado experimentales, si los floodfills lo permiten
  (pero ver las propuestas relacionadas 136 y 137 sobre el soporte para tipos de firma experimentales).
  La propuesta alternativa podría ser más fácil de implementar y probar para tipos de cifrado experimentales.

### New Encryption Issues

Parte de esto está fuera del alcance de esta propuesta, pero ponemos notas aquí por ahora ya que aún no tenemos una propuesta de encriptación separada. Ver también las propuestas ECIES 144 y 145.

- El tipo de cifrado representa la combinación
  de curva, longitud de clave, y esquema extremo a extremo,
  incluyendo KDF y MAC, si los hay.

- Hemos incluido un campo de longitud de clave, para que el LS2 sea
  analizable y verificable por el floodfill incluso para tipos de cifrado desconocidos.

- El primer nuevo tipo de cifrado que se proponga probablemente
  será ECIES/X25519. Cómo se usa de extremo a extremo
  (ya sea una versión ligeramente modificada de ElGamal/AES+SessionTag
  o algo completamente nuevo, por ejemplo ChaCha/Poly) se especificará
  en una o más propuestas separadas.
  Consulta también las propuestas ECIES 144 y 145.

### LeaseSet 2

- La expiración de 8 bytes en los leases cambió a 4 bytes.

- Si alguna vez implementamos revocación, podemos hacerlo con un campo expires de cero,
  o cero leases, o ambos. No hay necesidad de una clave de revocación separada.

- Las claves de cifrado están en orden de preferencia del servidor, la más preferida primero.
  El comportamiento predeterminado del cliente es seleccionar la primera clave con
  un tipo de cifrado compatible. Los clientes pueden usar otros algoritmos de selección
  basados en el soporte de cifrado, rendimiento relativo y otros factores.

### Formato

Objetivos:

- Agregar ocultación
- Permitir múltiples tipos de firma
- No requiere nuevas primitivas criptográficas
- Opcionalmente cifrar para cada destinatario, revocable
- Compatible con cifrado de Standard LS2 y Meta LS2 únicamente

El LS2 cifrado nunca se envía en un mensaje garlic extremo a extremo. Utiliza el LS2 estándar como se indica arriba.

Cambios respecto al LeaseSet cifrado existente:

- Cifrar todo por seguridad
- Cifrar de forma segura, no solo con AES.
- Cifrar para cada destinatario

Buscar con

    Standard LS flag (1)
Almacenar con

    Encrypted LS2 type (5)
Almacenar en

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Expiración típica

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Publicado por

    Destination

### Justificación

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados para LS2 cifrado:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.

SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

### Discusión

El formato LS2 encriptado consiste en tres capas anidadas:

- Una capa exterior que contiene la información en texto plano necesaria para el almacenamiento y recuperación.
- Una capa intermedia que maneja la autenticación del cliente.
- Una capa interna que contiene los datos LS2 reales.

El formato general se ve así::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Tenga en cuenta que el LS2 encriptado está cegado. El Destination no está en el encabezado. La ubicación de almacenamiento DHT es SHA-256(tipo de sig || clave pública cegada), y se rota diariamente.

NO usa el encabezado LS2 estándar especificado arriba.

#### Layer 0 (outer)

Tipo

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Tipo de Firma de Clave Pública Ciega

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Clave Pública Ciega

    Length as implied by sig type

Marca de tiempo de publicación

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Expira

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Banderas

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Datos de clave transitoria

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

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Firma

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.

#### Layer 1 (middle)

Banderas

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

Datos de autenticación del cliente DH

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

Datos de autenticación de cliente PSK

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

innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.

#### Layer 2 (inner)

Tipo

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Datos

    LeaseSet2 data for the given type.

    Includes the header and signature.

### Nuevos Problemas de Cifrado

Utilizamos el siguiente esquema para el cegado de claves, basado en Ed25519 y [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Las firmas Re25519 son sobre la curva Ed25519, utilizando SHA-512 para el hash.

No utilizamos [el apéndice A.2 de rend-spec-v3.txt de Tor](https://spec.torproject.org/rend-spec-v3), que tiene objetivos de diseño similares, porque sus claves públicas cegadas pueden estar fuera del subgrupo de orden primo, con implicaciones de seguridad desconocidas.

#### Goals

- La clave pública de firma en el destino sin cegar debe ser
  Ed25519 (tipo de firma 7) o Red25519 (tipo de firma 11);
  no se admiten otros tipos de firma
- Si la clave pública de firma está offline, la clave pública de firma transitoria también debe ser Ed25519
- El cegado es computacionalmente simple
- Usa primitivas criptográficas existentes
- Las claves públicas cegadas no pueden ser descegadas
- Las claves públicas cegadas deben estar en la curva Ed25519 y el subgrupo de orden primo
- Debe conocer la clave pública de firma del destino
  (no se requiere el destino completo) para derivar la clave pública cegada
- Opcionalmente proporcionar un secreto adicional requerido para derivar la clave pública cegada

#### Security

La seguridad de un esquema de blinding requiere que la distribución de alpha sea la misma que las claves privadas sin blinding. Sin embargo, cuando aplicamos blinding a una clave privada Ed25519 (tipo de firma 7) para obtener una clave privada Red25519 (tipo de firma 11), la distribución es diferente. Para cumplir con los requisitos de [zcash sección 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), Red25519 (tipo de firma 11) debería usarse también para las claves sin blinding, de modo que "la combinación de una clave pública re-aleatorizada y firma(s) bajo esa clave no revelen la clave de la cual fue re-aleatorizada." Permitimos el tipo 7 para destinos existentes, pero recomendamos el tipo 11 para nuevos destinos que serán cifrados.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce

#### Blinding Calculations

Una nueva clave alfa secreta y claves cegadas deben generarse cada día (UTC). La alfa secreta y las claves cegadas se calculan de la siguiente manera.

GENERATE_ALPHA(destination, date, secret), para todas las partes:

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
BLIND_PRIVKEY(), para el propietario que publica el leaseset:

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
BLIND_PUBKEY(), para los clientes que recuperan el leaseSet:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Ambos métodos para calcular A' producen el mismo resultado, como se requiere.

#### Signing

El leaseSet no cegado es firmado por la clave privada de firma Ed25519 o Red25519 no cegada y verificado con la clave pública de firma Ed25519 o Red25519 no cegada (tipos de firma 7 u 11) como es habitual.

Si la clave pública de firma está desconectada, el leaseset no cegado es firmado por la clave privada de firma transitoria Ed25519 o Red25519 no cegada y verificado con la clave pública de firma transitoria Ed25519 o Red25519 no cegada (tipos de firma 7 u 11) como es habitual. Consulte más abajo las notas adicionales sobre claves desconectadas para leasesets cifrados.

Para la firma del leaseset cifrado, utilizamos Red25519, basado en [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) para firmar y verificar con claves cegadas. Las firmas Red25519 se realizan sobre la curva Ed25519, utilizando SHA-512 para el hash.

Red25519 es idéntico al Ed25519 estándar excepto por lo especificado a continuación.

#### Sign/Verify Calculations

La porción externa del leaseset cifrado utiliza claves y firmas Red25519.

Red25519 es casi idéntico a Ed25519. Hay dos diferencias:

Las claves privadas Red25519 se generan a partir de números aleatorios y luego deben reducirse mod L, donde L se define arriba. Las claves privadas Ed25519 se generan a partir de números aleatorios y luego se "sujetan" usando enmascaramiento bit a bit en los bytes 0 y 31. Esto no se hace para Red25519. Las funciones GENERATE_ALPHA() y BLIND_PRIVKEY() definidas arriba generan claves privadas Red25519 adecuadas usando mod L.

En Red25519, el cálculo de r para la firma utiliza datos aleatorios adicionales, y usa el valor de la clave pública en lugar del hash de la clave privada. Debido a los datos aleatorios, cada firma Red25519 es diferente, incluso al firmar los mismos datos con la misma clave.

Firma:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Verificación:

```text
// same as in Ed25519
```
### Notas

#### Derivation of subcredentials

Como parte del proceso de ofuscación, necesitamos asegurar que un LS2 cifrado solo pueda ser descifrado por alguien que conozca la clave pública de firma del Destination correspondiente. No se requiere el Destination completo. Para lograr esto, derivamos una credencial de la clave pública de firma:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
La cadena de personalización asegura que la credencial no colisione con ningún hash utilizado como clave de búsqueda DHT, como el hash de Destination plano.

Para una clave ciega dada, podemos entonces derivar una subcredencial:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
La subcredencial se incluye en los procesos de derivación de claves a continuación, lo que vincula esas claves al conocimiento de la clave pública de firma del Destination.

#### Layer 1 encryption

Primero, se prepara la entrada para el proceso de derivación de claves:

```text
outerInput = subcredential || publishedTimestamp
```
A continuación, se genera una sal aleatoria:

```text
outerSalt = CSRNG(32)
```
Luego se deriva la clave utilizada para cifrar la capa 1:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Finalmente, el texto plano de la capa 1 es cifrado y serializado:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

La salt se analiza desde el texto cifrado de la capa 1:

```text
outerSalt = outerCiphertext[0:31]
```
Luego se deriva la clave utilizada para cifrar la capa 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Finalmente, el texto cifrado de la capa 1 es descifrado:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Cuando la autorización de cliente está habilitada, ``authCookie`` se calcula como se describe a continuación. Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el arreglo de bytes de longitud cero.

El cifrado procede de manera similar a la capa 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Cuando la autorización de cliente está habilitada, ``authCookie`` se calcula como se describe a continuación. Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el array de bytes de longitud cero.

La descifrado procede de manera similar a la capa 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### LS2 Cifrado

Cuando la autorización de cliente está habilitada para un Destination, el servidor mantiene una lista de clientes a los que está autorizando para descifrar los datos cifrados del LS2. Los datos almacenados por cliente dependen del mecanismo de autorización, e incluyen algún tipo de material de clave que cada cliente genera y envía al servidor a través de un mecanismo seguro fuera de banda.

Existen dos alternativas para implementar la autorización por cliente:

#### DH client authorization

Cada cliente genera un par de claves DH ``[csk_i, cpk_i]``, y envía la clave pública ``cpk_i`` al servidor.

Procesamiento del servidor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El servidor genera una nueva ``authCookie`` y un par de claves DH efímero:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Luego, para cada cliente autorizado, el servidor encripta ``authCookie`` a su clave pública:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
El servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` en la capa 1 del LS2 cifrado, junto con ``epk``.

Procesamiento del cliente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El cliente utiliza su clave privada para derivar su identificador de cliente esperado ``clientID_i``, clave de cifrado ``clientKey_i``, y IV de cifrado ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Luego el cliente busca en los datos de autorización de la capa 1 una entrada que contenga ``clientID_i``. Si existe una entrada coincidente, el cliente la descifra para obtener ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Cada cliente genera una clave secreta de 32 bytes ``psk_i``, y la envía al servidor. Alternativamente, el servidor puede generar la clave secreta y enviarla a uno o más clientes.

Procesamiento del servidor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El servidor genera un nuevo ``authCookie`` y salt:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Luego, para cada cliente autorizado, el servidor encripta ``authCookie`` con su clave pre-compartida:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
El servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` en la capa 1 del LS2 cifrado, junto con ``authSalt``.

Procesamiento del cliente
^^^^^^^^^^^^^^^^^^^^^

El cliente utiliza su clave precompartida para derivar su identificador de cliente esperado ``clientID_i``, clave de cifrado ``clientKey_i``, y IV de cifrado ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Luego el cliente busca en los datos de autorización de capa 1 una entrada que contenga ``clientID_i``. Si existe una entrada coincidente, el cliente la descifra para obtener ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Ambos mecanismos de autorización de cliente anteriores proporcionan privacidad para la membresía de cliente. Una entidad que solo conoce el Destination puede ver cuántos clientes están suscritos en cualquier momento, pero no puede rastrear qué clientes están siendo agregados o revocados.

Los servidores DEBERÍAN aleatorizar el orden de los clientes cada vez que generen un LS2 cifrado, para evitar que los clientes conozcan su posición en la lista e infieran cuándo otros clientes han sido añadidos o revocados.

Un servidor PUEDE elegir ocultar el número de clientes que están suscritos insertando entradas aleatorias en la lista de datos de autorización.

Ventajas de la autorización de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La seguridad del esquema no depende únicamente del intercambio fuera de banda del
  material de clave del cliente. La clave privada del cliente nunca necesita salir de su
  dispositivo, por lo que un adversario que sea capaz de interceptar el intercambio fuera de
  banda, pero no pueda romper el algoritmo DH, no puede descifrar el LS2 cifrado, ni
  determinar por cuánto tiempo se le otorga acceso al cliente.

Desventajas de la autorización de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Requiere N + 1 operaciones DH en el lado del servidor para N clientes.
- Requiere una operación DH en el lado del cliente.
- Requiere que el cliente genere la clave secreta.

Ventajas de la autorización de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- No requiere operaciones DH.
- Permite al servidor generar la clave secreta.
- Permite al servidor compartir la misma clave con múltiples clientes, si se desea.

Desventajas de la autorización de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La seguridad del esquema depende críticamente del intercambio fuera de banda del material de clave del cliente. Un adversario que intercepte el intercambio para un cliente particular puede descifrar cualquier LS2 cifrado posterior para el cual ese cliente esté autorizado, así como determinar cuándo se revoca el acceso del cliente.

### Definiciones

Consulta la propuesta 149.

No puedes usar un LS2 encriptado para bittorrent, debido a las respuestas de anuncio compactas que son de 32 bytes. Los 32 bytes contienen solo el hash. No hay espacio para una indicación de que el leaseset está encriptado, o los tipos de firma.

### Formato

Para leaseSets cifrados con claves offline, las claves privadas cegadas también deben generarse offline, una para cada día.

Como el bloque de firma offline opcional está en la parte de texto claro del leaseset cifrado, cualquiera que rastree los floodfills podría usar esto para rastrear el leaseset (pero no descifrarlo) durante varios días. Para prevenir esto, el propietario de las claves también debería generar nuevas claves transitorias para cada día. Tanto las claves transitorias como las cegadas pueden generarse con anticipación y entregarse al router en un lote.

No se define ningún formato de archivo en esta propuesta para empaquetar múltiples claves transitorias y ciegas y proporcionarlas al cliente o router. No se define ninguna mejora del protocolo I2CP en esta propuesta para soportar leaseSets cifrados con claves sin conexión.

### Notes

- Un servicio que utilice leaseSets cifrados publicaría la versión cifrada a los
  floodfills. Sin embargo, por eficiencia, enviaría leaseSets sin cifrar a los
  clientes en el mensaje garlic envuelto, una vez autenticado (mediante whitelist, por
  ejemplo).

- Los floodfills pueden limitar el tamaño máximo a un valor razonable para prevenir abuso.

- Después del descifrado, se deben realizar varias verificaciones, incluyendo que
  la marca de tiempo interna y la expiración coincidan con las del nivel superior.

- ChaCha20 fue seleccionado en lugar de AES. Aunque las velocidades son similares si el soporte de hardware AES está disponible, ChaCha20 es 2.5-3x más rápido cuando el soporte de hardware AES no está disponible, como en dispositivos ARM de gama baja.

- No nos importa lo suficiente la velocidad como para usar BLAKE2b con clave. Tiene un
  tamaño de salida lo suficientemente grande para acomodar la n más grande que requerimos (o podemos llamarlo una vez por
  clave deseada con un argumento contador). BLAKE2b es mucho más rápido que SHA-256, y
  BLAKE2b con clave reduciría el número total de llamadas a funciones hash.
  Sin embargo, ver propuesta 148, donde se propone que cambiemos a BLAKE2b por otras razones.
  Ver [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Esto se utiliza para reemplazar multihoming. Como cualquier leaseSet, está firmado por el creador. Esta es una lista autenticada de hashes de destino.

El Meta LS2 es la cima de, y posiblemente los nodos intermedios de, una estructura de árbol. Contiene un número de entradas, cada una apuntando a un LS, LS2, o otro Meta LS2 para soportar multihoming masivo. Un Meta LS2 puede contener una mezcla de entradas LS, LS2, y Meta LS2. Las hojas del árbol son siempre un LS o LS2. El árbol es un DAG; los bucles están prohibidos; los clientes que realizan búsquedas deben detectar y rechazar seguir bucles.

Un Meta LS2 puede tener una expiración mucho más larga que un LS o LS2 estándar. El nivel superior puede tener una expiración varias horas después de la fecha de publicación. El tiempo máximo de expiración será aplicado por floodfills y clientes, y está por determinar.

El caso de uso para Meta LS2 es multihoming masivo, pero sin más protección para la correlación de routers con leasesets (en el momento de reinicio del router) de la que se proporciona actualmente con LS o LS2. Esto es equivalente al caso de uso de "facebook", que probablemente no necesita protección contra correlación. Este caso de uso probablemente necesita claves sin conexión, que se proporcionan en el encabezado estándar en cada nodo del árbol.

El protocolo de back-end para la coordinación entre los routers hoja, los firmantes Meta LS intermedios y maestros no se especifica aquí. Los requisitos son extremadamente simples: solo verificar que el peer esté activo y publicar un nuevo LS cada pocas horas. La única complejidad es elegir nuevos publicadores para los Meta LSes de nivel superior o intermedio en caso de falla.

Los leasesets de mezcla y combinación donde las leases de múltiples routers se combinan, firman y publican en un solo leaseset está documentado en la propuesta 140, "multihoming invisible". Esta propuesta es insostenible tal como está escrita, porque las conexiones de streaming no serían "pegajosas" a un solo router, ver http://zzz.i2p/topics/2335 .

El protocolo de back-end, y la interacción con los componentes internos del router y cliente, sería bastante compleja para el multihoming invisible.

Para evitar sobrecargar el floodfill para el Meta LS de nivel superior, la expiración debe ser de al menos varias horas. Los clientes deben almacenar en caché el Meta LS de nivel superior y mantenerlo después de reinicios si no ha expirado.

Necesitamos definir algún algoritmo para que los clientes atraviesen el árbol, incluyendo respaldos, de manera que el uso se disperse. Alguna función de distancia hash, costo y aleatoriedad. Si un nodo tiene tanto LS o LS2 como Meta LS, necesitamos saber cuándo está permitido usar esos leasesets, y cuándo continuar atravesando el árbol.

Buscar con

    Standard LS flag (1)
Almacenar con

    Meta LS2 type (7)
Almacenar en

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiración típica

    Hours. Max 18.2 hours (65535 seconds)
Publicado por

    "master" Destination or coordinator, or intermediate coordinators

### Format

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
Flags and properties: para uso futuro

### Derivación de Clave de Ocultación

- Un servicio distribuido que use esto tendría uno o más "maestros" con la
  clave privada del destino del servicio. Estos determinarían (fuera de banda) la
  lista actual de destinos activos y publicarían el Meta LS2. Para redundancia,
  múltiples maestros podrían hacer multihome (es decir, publicar concurrentemente)
  el Meta LS2.

- Un servicio distribuido podría comenzar con un solo destino o usar
  multihoming de estilo antiguo, luego hacer la transición a un Meta LS2. Una
  búsqueda de LS estándar podría devolver cualquiera de un LS, LS2, o Meta LS2.

- Cuando un servicio utiliza un Meta LS2, no tiene túneles (leases).

### Service Record

Este es un registro individual que indica que un destino está participando en un servicio. Se envía desde el participante al floodfill. Nunca se envía individualmente por un floodfill, sino únicamente como parte de una Lista de Servicios. El Service Record también se utiliza para revocar la participación en un servicio, estableciendo la expiración en cero.

Esto no es un LS2 pero usa el formato estándar de encabezado y firma LS2.

Buscar con

    n/a, see Service List
Almacenar con

    Service Record type (9)
Almacenar en

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Vencimiento típico

    Hours. Max 18.2 hours (65535 seconds)
Publicado por

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Si expires es todo ceros, el floodfill debería revocar el registro y ya no
  incluirlo en la lista de servicios.

- Almacenamiento: El floodfill puede limitar estrictamente el almacenamiento de estos registros y
  limitar el número de registros almacenados por hash y su expiración. También se puede
  usar una lista blanca de hashes.

- Cualquier otro tipo de netdb en el mismo hash tiene prioridad, por lo que un registro de servicio nunca puede
  sobrescribir un LS/RI, pero un LS/RI sobrescribirá todos los registros de servicio en ese hash.

### Service List

Esto no se parece en nada a un LS2 y usa un formato diferente.

La lista de servicios es creada y firmada por el floodfill. No está autenticada en el sentido de que cualquiera puede unirse a un servicio publicando un Registro de Servicio a un floodfill.

Una Lista de Servicios contiene Registros de Servicio Cortos, no Registros de Servicio completos. Estos contienen firmas pero solo hashes, no destinos completos, por lo que no pueden ser verificados sin el destino completo.

La seguridad, si la hay, y la conveniencia de las listas de servicios está por determinar. Los floodfills podrían limitar la publicación, y las búsquedas, a una lista blanca de servicios, pero esa lista blanca puede variar según la implementación o la preferencia del operador. Es posible que no sea posible lograr consenso sobre una lista blanca común base entre implementaciones.

Si el nombre del servicio está incluido en el registro de servicio anterior, entonces los operadores de floodfill pueden objetar; si solo se incluye el hash, no hay verificación, y un registro de servicio podría "colarse" antes que cualquier otro tipo de netdb y almacenarse en el floodfill.

Buscar con

    Service List lookup type (11)
Almacenar con

    Service List type (11)
Almacenar en

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Expiración típica

    Hours, not specified in the list itself, up to local policy
Publicado por

    Nobody, never sent to floodfill, never flooded.

### Format

NO utiliza el encabezado estándar LS2 especificado anteriormente.

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
Para verificar la firma de la Lista de Servicios:

- anteponer el hash del nombre del servicio
- eliminar el hash del creador
- Verificar la firma del contenido modificado

Para verificar la firma de cada Short Service Record:

- Obtener destino
- Verificar firma de (marca de tiempo publicada + expira + flags + puerto + Hash del
  nombre del servicio)

Para verificar la firma de cada Registro de Revocación:

- Obtener destino
- Verificar firma de (marca de tiempo publicada + 4 bytes cero + flags + puerto + Hash
  del nombre del servicio)

### Notes

- Utilizamos la longitud de firma en lugar del tipo de firma para poder soportar tipos de firma desconocidos.

- No hay expiración de una lista de servicios, los destinatarios pueden tomar su propia
  decisión basada en políticas o la expiración de los registros individuales.

- Las Service Lists no se inundan, solo los Service Records individuales. Cada
  floodfill crea, firma y almacena en caché una Service List. El floodfill usa su
  propia política para el tiempo de caché y el número máximo de registros de
  servicio y revocación.

## Common Structures Spec Changes Required

### Cifrado y procesamiento

Fuera del alcance de esta propuesta. Agregar a las propuestas ECIES 144 y 145.

### New Intermediate Structures

Agregar nuevas estructuras para Lease2, MetaLease, LeaseSet2Header y OfflineSignature. Efectivo a partir de la versión 0.9.38.

### New NetDB Types

Agregar estructuras para cada nuevo tipo de leaseset, incorporadas desde arriba. Para LeaseSet2, EncryptedLeaseSet, y MetaLeaseSet, efectivo a partir de la versión 0.9.38. Para Service Record y Service List, preliminar y sin programar.

### New Signature Type

Agregar RedDSA_SHA512_Ed25519 Tipo 11. La clave pública es de 32 bytes; la clave privada es de 32 bytes; el hash es de 64 bytes; la firma es de 64 bytes.

## Encryption Spec Changes Required

Fuera del alcance de esta propuesta. Ver propuestas 144 y 145.

## I2NP Changes Required

Agregar nota: LS2 solo puede ser publicado a floodfills con una versión mínima.

### Database Lookup Message

Agregar el tipo de búsqueda de lista de servicios.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Autorización por cliente

Agregar todos los nuevos tipos de almacén.

### Changes

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
## I2CP Changes Required

### I2CP Options

Nuevas opciones interpretadas del lado del router, enviadas en el Mapeo SessionConfig:

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
### Session Config

Tenga en cuenta que para las firmas offline, las opciones i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, e i2cp.leaseSetOfflineSignature son requeridas, y la firma es realizada por la clave privada de firma transitoria.

### Encrypted LS con Direcciones Base 32

Router a cliente. Sin cambios. Los leases se envían con timestamps de 8 bytes, incluso si el leaseset devuelto será un LS2 con timestamps de 4 bytes. Tenga en cuenta que la respuesta puede ser un mensaje Create Leaseset o Create Leaseset2.

### LS Cifrado con Claves Offline

Router al cliente. Sin cambios. Los leases se envían con marcas de tiempo de 8 bytes, incluso si el leaseset devuelto será un LS2 con marcas de tiempo de 4 bytes. Nota que la respuesta puede ser un mensaje Create Leaseset o Create Leaseset2.

### Notas

Cliente al router. Nuevo mensaje, para usar en lugar del Mensaje de Crear LeaseSet.

### Meta LS2

- Para que el router analice el tipo de almacén, el tipo debe estar en el mensaje,
  a menos que se pase al router de antemano en la configuración de sesión.
  Para el código de análisis común, es más fácil tenerlo en el mensaje mismo.

- Para que el router conozca el tipo y longitud de la clave privada,
  debe estar después del leaseSet, a menos que el parser conozca el tipo de antemano
  en la configuración de sesión.
  Para código de análisis común, es más fácil conocerlo del propio mensaje.

- La clave privada de firma, previamente definida para revocación y sin usar,
  no está presente en LS2.

### I notice that the text you provided only contains the word "Format" and the instruction "" - there doesn't appear to be any actual content to translate.

For the word "Format" by itself, the Spanish translation would be:

Formato

El tipo de mensaje para el Mensaje Create Leaseset2 es 41.

### Notas

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
### Registro de Servicio

- La versión mínima del router es 0.9.39.
- La versión preliminar con tipo de mensaje 40 estaba en 0.9.38 pero el formato fue cambiado.
  El tipo 40 está abandonado y no es compatible.

### Formato

- Se necesitan más cambios para soportar LS cifrados y meta.

### Notas

Cliente a router. Mensaje nuevo.

### Lista de Servicios

- El router necesita saber si un destino está oculto (blinded).
  Si está oculto y utiliza autenticación secreta o por cliente,
  también necesita tener esa información.

- Un Host Lookup de una dirección b32 de nuevo formato ("b33")
  le dice al router que la dirección está ofuscada, pero no hay mecanismo para
  pasar la clave secreta o privada al router en el mensaje Host Lookup.
  Aunque podríamos extender el mensaje Host Lookup para añadir esa información,
  es más limpio definir un nuevo mensaje.

- Necesitamos una forma programática para que el cliente le comunique al router.
  De lo contrario, el usuario tendría que configurar manualmente cada destino.

### Formato

Antes de que un cliente envíe un mensaje a un destino oculto, debe buscar el "b33" en un mensaje Host Lookup, o enviar un mensaje Blinding Info. Si el destino oculto requiere un secreto o autenticación por cliente, el cliente debe enviar un mensaje Blinding Info.

El router no envía una respuesta a este mensaje.

### Notas

El tipo de mensaje para el Blinding Info Message es 42.

### Format

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
### Certificados de Clave

- La versión mínima del router es 0.9.43

### Nuevas Estructuras Intermedias

### Nuevos Tipos de NetDB

Para soportar búsquedas de nombres de host "b33" y devolver una indicación si el router no tiene la información requerida, definimos códigos de resultado adicionales para el Mensaje de Respuesta de Host, como sigue:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Los valores 1-255 ya están definidos como errores, por lo que no hay problema de compatibilidad hacia atrás.

### Nuevo Tipo de Firma

Router al cliente. Nuevo mensaje.

### Justification

Un cliente no sabe a priori que un Hash dado se resolverá en un Meta LS.

Si una búsqueda de leaseset para un Destination devuelve un Meta LS, el router hará la resolución recursiva. Para datagramas, el lado del cliente no necesita saberlo; sin embargo, para streaming, donde el protocolo verifica el destino en el SYN ACK, debe saber cuál es el destino "real". Por lo tanto, necesitamos un nuevo mensaje.

### Usage

El router mantiene una caché para el destino real que se utiliza desde un LS meta. Cuando el cliente envía un mensaje a un destino que se resuelve a un LS meta, el router verifica la caché para el destino real usado por última vez. Si la caché está vacía, el router selecciona un destino del LS meta y busca el leaseSet. Si la búsqueda del leaseSet es exitosa, el router añade ese destino a la caché y envía al cliente un Meta Redirect Message. Esto solo se hace una vez, a menos que el destino expire y deba ser cambiado. El cliente también debe almacenar en caché la información si es necesario. El Meta Redirect Message NO se envía en respuesta a cada SendMessage.

El router solo envía este mensaje a clientes con versión 0.9.47 o superior.

El cliente no envía una respuesta a este mensaje.

### Mensaje de Consulta de Base de Datos

El tipo de mensaje para el Meta Redirect Message es 43.

### Cambios

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
### Mensaje de Almacenamiento de Base de Datos

Cómo generar y soportar Meta, incluyendo la comunicación y coordinación entre routers, está fuera del alcance de esta propuesta. Ver propuesta relacionada 150.

### Cambios

Las firmas offline no pueden ser verificadas en streaming o datagramas respondibles. Ver secciones a continuación.

## Private Key File Changes Required

El formato del archivo de clave privada (eepPriv.dat) no es una parte oficial de nuestras especificaciones, pero está documentado en los [javadocs de Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) y otras implementaciones sí lo admiten. Esto permite la portabilidad de claves privadas a diferentes implementaciones.

Los cambios son necesarios para almacenar la clave pública transitoria y la información de firma fuera de línea.

### Changes

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
### Opciones I2CP

Agregar soporte para las siguientes opciones:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Las firmas offline actualmente no pueden verificarse en streaming. El cambio a continuación agrega el bloque de firmado offline a las opciones. Esto evita tener que recuperar esta información vía I2CP.

### Configuración de Sesión

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
### Mensaje de Solicitud de LeaseSet

- La alternativa es simplemente agregar una bandera y recuperar la clave pública transitoria a través de I2CP
  (Ver las secciones de Mensaje de Búsqueda de Host / Respuesta de Host arriba)

## Cabecera estándar LS2

Las firmas offline no pueden ser verificadas en el procesamiento de datagramas respondibles. Necesita una bandera para indicar firmado offline pero no hay lugar para poner una bandera. Requerirá un número de protocolo y formato completamente nuevos.

### Mensaje de Solicitud de Leaseset Variable

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
### Crear Mensaje Leaseset2

- La alternativa es simplemente agregar una bandera y recuperar la clave pública transitoria a través de I2CP
  (Ver las secciones de Mensaje de Búsqueda de Host / Respuesta de Host arriba)
- ¿Hay alguna otra opción que deberíamos agregar ahora que tenemos bytes de bandera?

## SAM V3 Changes Required

SAM debe ser mejorado para soportar firmas offline en la DESTINATION base 64.

### Justificación

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

Tenga en cuenta que el SESSION STATUS devolverá una Clave Privada de Firma de todos ceros y los datos de Firma Fuera de Línea exactamente como se proporcionaron en el SESSION CREATE.

Tenga en cuenta que DEST GENERATE y SESSION CREATE DESTINATION=TRANSIENT no pueden usarse para crear un destino firmado sin conexión.

### Tipo de Mensaje

¿Actualizar la versión a 3.4, o dejarla en 3.1/3.2/3.3 para que se pueda agregar sin requerir todo el contenido de 3.2/3.3?

Otros cambios por determinar. Ver la sección Mensaje de Respuesta del Host I2CP arriba.

## BOB Changes Required

BOB tendría que ser mejorado para soportar firmas offline y/o Meta LS. Esto es de baja prioridad y probablemente nunca será especificado o implementado. SAM V3 es la interfaz preferida.

## Publishing, Migration, Compatibility

LS2 (excepto LS2 encriptado) se publica en la misma ubicación DHT que LS1. No hay manera de publicar tanto un LS1 como un LS2, a menos que LS2 estuviera en una ubicación diferente.

El LS2 encriptado se publica en el hash del tipo de clave ciega y los datos de la clave. Este hash se utiliza entonces para generar la "clave de enrutamiento" diaria, como en LS1.

LS2 solo se usaría cuando se requieran nuevas características (nueva criptografía, LS cifrado, meta, etc.). LS2 solo puede publicarse en floodfills de una versión especificada o superior.

Los servidores que publican LS2 sabrían que cualquier cliente que se conecte soporta LS2. Podrían enviar LS2 en el garlic.

Los clientes enviarían LS2 en garlics únicamente si usan criptografía nueva. ¿Los clientes compartidos usarían LS1 indefinidamente? TODO: ¿Cómo tener clientes compartidos que soporten tanto criptografía antigua como nueva?

## Rollout

0.9.38 contiene soporte de floodfill para LS2 estándar, incluyendo claves offline.

0.9.39 contiene soporte I2CP para LS2 y Encrypted LS2, firma/verificación de tipo de firma 11, soporte floodfill para Encrypted LS2 (tipos de firma 7 y 11, sin claves offline), y cifrado/descifrado de LS2 (sin autorización por cliente).

0.9.40 está programada para contener soporte para cifrar/descifrar LS2 con autorización por cliente, soporte de floodfill e I2CP para Meta LS2, soporte para LS2 cifrado con claves offline, y soporte b32 para LS2 cifrado.

## Nuevos tipos de DatabaseEntry

El diseño encriptado de LS2 está fuertemente influenciado por los [descriptores de servicios ocultos v3 de Tor](https://spec.torproject.org/rend-spec-v3), que tenían objetivos de diseño similares.
