---
title: "Especificación de creación de túnel (ECIES-X25519)"
description: "Cifrado de mensajes Tunnel Build usando primitivas criptográficas ECIES-X25519 para secreto hacia adelante."
slug: "tunnel-creation-ecies"
aliases:
  - "/es/docs/specs/tunnel-creation-ecies-spec"
  - "/es/docs/specs/tunnel-creation-ecies-spec/"
category: "Protocolos"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Resumen

Este documento especifica el cifrado de mensajes Tunnel Build utilizando primitivas criptográficas introducidas por [ECIES-X25519](/docs/specs/ecies/). Es una parte de la propuesta general [Prop156](/proposals/156/) para convertir routers de claves ElGamal a ECIES-X25519.

Hay dos versiones especificadas. La primera utiliza los mensajes de construcción existentes y el tamaño de registro de construcción actual, para compatibilidad con routers ElGamal. Esta especificación fue implementada a partir de la versión 0.9.48 y ahora está obsoleta. La segunda utiliza dos nuevos mensajes de construcción y un tamaño de registro de construcción más pequeño, y solo puede ser utilizada con routers ECIES. Esta especificación está implementada a partir de la versión 0.9.51.

Para los propósitos de transicionar la red de ElGamal + AES256 a ECIES + ChaCha20, son necesarios los tunnels con routers mixtos ElGamal y ECIES. Se proporcionan especificaciones para manejar saltos de tunnel mixtos. No se realizarán cambios en el formato, procesamiento o cifrado de los saltos ElGamal. Este formato mantiene el mismo tamaño para los registros de construcción de tunnel, como se requiere para la compatibilidad.

Los creadores de tunnel ElGamal generarán pares de claves X25519 efímeras por salto, y seguirán esta especificación para crear tunnels que contengan saltos ECIES.

Este documento especifica la Construcción de Túneles ECIES-X25519. Para una visión general de todos los cambios requeridos para los routers ECIES, consulte la propuesta 156 [Prop156](/proposals/156/). Para información adicional sobre el desarrollo de la especificación de registros largos, consulte la propuesta 152 [Prop152](/proposals/152/). Para información adicional sobre el desarrollo de la especificación de registros cortos, consulte la propuesta 157 [Prop157](/proposals/157/).

### Primitivas Criptográficas

Los primitivos requeridos para implementar esta especificación son:

- AES-256-CBC como en [Criptografía](/docs/specs/cryptography/)
- Funciones STREAM ChaCha20: ENCRYPT(k, iv, plaintext) y DECRYPT(k, iv, ciphertext) - como en [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) y [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funciones STREAM ChaCha20/Poly1305: ENCRYPT(k, n, plaintext, ad) y DECRYPT(k, n, ciphertext, ad) - como en [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), y [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funciones X25519 DH - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)

Otras funciones de Noise definidas en otros lugares:

- MixHash(d) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - como en [NTCP2](/docs/specs/ntcp2/) y [ECIES-X25519](/docs/specs/ecies/)

## Diseño

### Noise Protocol Framework

Esta especificación proporciona los requisitos basados en el Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisión 34, 2018-07-11). En la terminología de Noise, Alice es el iniciador y Bob es el respondedor.

Se basa en el protocolo Noise Noise_N_25519_ChaChaPoly_SHA256. Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Handshake Unidireccional: N - Alice no transmite su clave estática a Bob (N)
- Función DH: X25519 - X25519 DH con una longitud de clave de 32 bytes según se especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Función de Cifrado: ChaChaPoly - AEAD_CHACHA20_POLY1305 según se especifica en [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8. Nonce de 12 bytes, con los primeros 4 bytes establecidos en cero. Idéntico al utilizado en [NTCP2](/docs/specs/ntcp2/)
- Función Hash: SHA256 - Hash estándar de 32 bytes, ya utilizado extensivamente en I2P

### Patrones de Handshake

Los handshakes utilizan patrones de handshake [Noise](https://noiseprotocol.org/noise.html).

Se utiliza la siguiente correspondencia de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje

La solicitud de construcción es idéntica al patrón Noise N. Esto también es idéntico al primer mensaje (Solicitud de Sesión) en el patrón XK usado en [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Cifrado de Solicitudes

Los registros de solicitud de construcción son creados por el creador del túnel y cifrados asimétricamente para cada salto individual. Este cifrado asimétrico de registros de solicitud actualmente es ElGamal como se define en [Cryptography](/docs/specs/cryptography/) y contiene una suma de verificación SHA-256. Este diseño no es forward-secret.

El diseño ECIES utiliza el patrón Noise unidireccional "N" con DH efímero-estático ECIES-X25519, con un HKDF, y ChaCha20/Poly1305 AEAD para secreto hacia adelante, integridad y autenticación. Alice es el solicitante de construcción del tunnel. Cada salto en el tunnel es un Bob.

### Cifrado de Respuesta

Los registros de respuesta de construcción son creados por el creador de los saltos y cifrados simétricamente hacia el creador. Este cifrado simétrico de los registros de respuesta ElGamal es AES con una suma de verificación SHA-256 antepuesta. Este diseño no es forward-secret.

Las respuestas ECIES utilizan ChaCha20/Poly1305 AEAD para integridad y autenticación.

## Especificación de Registro Largo

NOTA: Obsoleto, en desuso. Utilice el formato de Registro Corto especificado a continuación.

### Registros de Solicitud de Construcción

Los BuildRequestRecords cifrados tienen 528 bytes tanto para ElGamal como para ECIES, por compatibilidad.

#### Registro de Solicitud Sin Cifrar

Esta es la especificación del BuildRequestRecord de túnel para routers ECIES-X25519. Resumen de cambios:

- Eliminar hash de router de 32 bytes no utilizado
- Cambiar tiempo de solicitud de horas a minutos
- Añadir campo de expiración para tiempo variable de tunnel futuro
- Añadir más espacio para flags
- Añadir mapeo para opciones de construcción adicionales
- La clave de respuesta AES-256 y el IV no se usan para el registro de respuesta del propio hop
- El registro no cifrado es más largo porque hay menos sobrecarga de cifrado

El registro de solicitud no contiene ninguna clave de respuesta ChaCha. Esas claves se derivan de un KDF. Ver más abajo.

Todos los campos están en big-endian.

Tamaño sin cifrar: 464 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
El campo flags es el mismo que se define en [Tunnel-Creation](/docs/specs/tunnel-creation/) y contiene lo siguiente:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
El bit 7 indica que el salto será un gateway de entrada (IBGW). El bit 6 indica que el salto será un endpoint de salida (OBEP). Si ningún bit está configurado, el salto será un participante intermedio. Ambos no pueden estar configurados al mismo tiempo.

La expiración de la solicitud es para la duración variable futura del tunnel. Por ahora, el único valor soportado es 600 (10 minutos).

Las opciones de construcción de tunnel es una estructura Mapping como se define en [Common](/docs/specs/common-structures/). Las únicas opciones definidas actualmente son para parámetros de ancho de banda, a partir de la API 0.9.65, ver detalles a continuación. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es 296 bytes, y el valor máximo del campo de longitud del Mapping es 294.

#### Registro de Solicitud Encriptado

Todos los campos están en big-endian excepto la clave pública efímera que está en little-endian.

Tamaño cifrado: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Construir Registros de Respuesta

Los BuildReplyRecords cifrados son de 528 bytes tanto para ElGamal como para ECIES, por compatibilidad.

#### Registro de Respuesta Sin Cifrar

Esta es la especificación del tunnel BuildReplyRecord para routers ECIES-X25519. Resumen de cambios:

- Agregar mapeo para las opciones de respuesta de construcción
- El registro no cifrado es más largo porque hay menos sobrecarga de cifrado

Las respuestas ECIES están cifradas con ChaCha20/Poly1305.

Todos los campos están en formato big-endian.

Tamaño sin cifrar: 512 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Las opciones de respuesta de construcción de tunnel son una estructura Mapping como se define en [Common](/docs/specs/common-structures/). Las únicas opciones definidas actualmente son para parámetros de ancho de banda, a partir de la API 0.9.65, consulta los detalles a continuación. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es de 511 bytes, y el valor máximo del campo de longitud del Mapping es 509.

El byte de respuesta es uno de los siguientes valores según se define en [Tunnel-Creation](/docs/specs/tunnel-creation/) para evitar la creación de huellas digitales:

- 0x00 (aceptar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Registro de Respuesta Cifrado

Tamaño cifrado: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Después de la transición completa a registros ECIES, las reglas de padding por rangos son las mismas que para los registros de solicitud.

### Cifrado Simétrico de Registros

Los túneles mixtos están permitidos, y son necesarios, para la transición de ElGamal a ECIES. Durante el período de transición, un número creciente de routers tendrán claves bajo ECIES.

El preprocesamiento de criptografía simétrica se ejecutará de la misma manera:

- "encryption":
  - cipher ejecutado en modo descifrado
  - registros de solicitud descifrados preventivamente en preprocesamiento (ocultando registros de solicitud cifrados)
- "decryption":
  - cipher ejecutado en modo cifrado
  - registros de solicitud cifrados (revelando el siguiente registro de solicitud en texto plano) por saltos participantes
- ChaCha20 no tiene "modos", por lo que simplemente se ejecuta tres veces:
  - una vez en preprocesamiento
  - una vez por el salto
  - una vez en el procesamiento de respuesta final

Cuando se utilizan tunnels mixtos, los creadores de tunnel necesitarán basar el cifrado simétrico del BuildRequestRecord en el tipo de cifrado del salto actual y del anterior.

Cada salto utilizará su propio tipo de cifrado para cifrar BuildReplyRecords, y los otros registros en el VariableTunnelBuildMessage (VTBM).

En la ruta de respuesta, el endpoint (remitente) necesitará deshacer el [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), usando la clave de respuesta de cada salto.

Como ejemplo aclaratorio, veamos un túnel de salida con ECIES rodeado por ElGamal:

- Remitente (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Todos los BuildRequestRecords están en su estado encriptado (usando ElGamal o ECIES).

El cifrado AES256/CBC, cuando se utiliza, aún se usa para cada registro, sin encadenamiento entre múltiples registros.

De igual manera, ChaCha20 se utilizará para cifrar cada registro, no transmitiendo de forma continua a través de todo el VTBM.

Los registros de solicitud son preprocesados por el Remitente (OBGW):

- El registro de H3 es "cifrado" usando:
  - La clave de respuesta de H2 (ChaCha20)
  - La clave de respuesta de H1 (AES256/CBC)
- El registro de H2 es "cifrado" usando:
  - La clave de respuesta de H1 (AES256/CBC)
- El registro de H1 sale sin cifrado simétrico

Solo H2 verifica la bandera de cifrado de respuesta, y ve que está seguida por AES256/CBC.

Después de ser procesados por cada salto, los registros están en un estado "descifrado":

- El registro de H3 es "descifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
- El registro de H2 es "descifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
  - La clave de respuesta de H2 (ChaCha20-Poly1305)
- El registro de H1 es "descifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
  - La clave de respuesta de H2 (ChaCha20)
  - La clave de respuesta de H1 (AES256/CBC)

El creador del tunnel, también conocido como Inbound Endpoint (IBEP), postprocesa la respuesta:

- El registro de H3 está "cifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
- El registro de H2 está "cifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
  - La clave de respuesta de H2 (ChaCha20-Poly1305)
- El registro de H1 está "cifrado" usando:
  - La clave de respuesta de H3 (AES256/CBC)
  - La clave de respuesta de H2 (ChaCha20)
  - La clave de respuesta de H1 (AES256/CBC)

### Claves de Registro de Solicitud

Estas claves se incluyen explícitamente en los ElGamal BuildRequestRecords. Para los ECIES BuildRequestRecords, se incluyen las claves de tunnel y las claves de respuesta AES, pero las claves de respuesta ChaCha se derivan del intercambio DH. Consulta [Prop156](/proposals/156/) para obtener detalles sobre las claves estáticas ECIES del router.

A continuación se describe cómo derivar las claves transmitidas previamente en los registros de solicitud.

#### KDF para ck y h iniciales

Esto es [NOISE](https://noiseprotocol.org/noise.html) estándar para el patrón "N" con un nombre de protocolo estándar.

```
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
#### KDF para Registro de Solicitud

Los creadores de tunnel ElGamal generan un par de claves X25519 efímero para cada salto ECIES en el tunnel, y utilizan el esquema anterior para cifrar su BuildRequestRecord. Los creadores de tunnel ElGamal utilizarán el esquema anterior a esta especificación para cifrar hacia saltos ElGamal.

Los creadores de tunnel ECIES necesitarán cifrar a cada una de las claves públicas de los saltos ElGamal usando el esquema definido en [Tunnel-Creation](/docs/specs/tunnel-creation/). Los creadores de tunnel ECIES usarán el esquema anterior para cifrar a los saltos ECIES.

Esto significa que los saltos de tunnel solo verán registros cifrados de su mismo tipo de cifrado.

Para los creadores de túneles ElGamal y ECIES, generarán pares de claves efímeras X25519 únicos por salto para cifrar hacia los saltos ECIES.

**IMPORTANTE**: Las claves efímeras deben ser únicas por salto ECIES y por registro de construcción. No usar claves únicas abre un vector de ataque para que los saltos que colaboren entre sí confirmen que están en el mismo tunnel.

```
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
`replyKey`, `layerKey` y `layerIV` aún deben incluirse dentro de los registros ElGamal, y pueden generarse aleatoriamente.

### Cifrado de Registro de Respuesta

El registro de respuesta está cifrado con ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Especificación de Registro Corto

Esta especificación utiliza dos nuevos mensajes de construcción de túnel I2NP, Short Tunnel Build Message (tipo 25) y Outbound Tunnel Build Reply Message (tipo 26).

El creador del tunnel y todos los saltos en el tunnel creado deben usar ECIES-X25519, y al menos la versión 0.9.51. Los saltos en el tunnel de respuesta (para una construcción saliente) o el tunnel saliente (para una construcción entrante) no tienen ningún requisito.

Los registros de solicitud y respuesta encriptados serán de 218 bytes, en comparación con los 528 bytes de todos los demás mensajes de construcción.

Los registros de solicitud de texto plano serán de 154 bytes, comparado con 222 bytes para registros ElGamal, y 464 bytes para registros ECIES como se define arriba.

Los registros de respuesta en texto plano serán de 202 bytes, comparados con 496 bytes para registros ElGamal, y 512 bytes para registros ECIES como se define anteriormente.

El cifrado de respuesta será ChaCha20/Poly1305 para el registro del propio salto, y ChaCha20 (NO ChaCha20/Poly1305) para los otros registros en el mensaje de construcción.

Los registros de solicitud se harán más pequeños usando HKDF para crear las claves de capa y respuesta, por lo que no se incluyen explícitamente en la solicitud.

### Flujo de Mensajes

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Notas

El empaquetado garlic de los mensajes los oculta del OBEP (para una construcción entrante) o del IBGW (para una construcción saliente). Esto se recomienda pero no es obligatorio. Si el OBEP y el IBGW son el mismo router, no es necesario.

### Registros de Solicitud de Construcción Cortos

Los BuildRequestRecords cifrados cortos son de 218 bytes.

#### Registro de Solicitud Corta Sin Cifrar

Resumen de cambios de registros largos:

- Cambiar la longitud sin cifrar de 464 a 154 bytes
- Cambiar la longitud cifrada de 528 a 218 bytes
- Eliminar las claves de capa y respuesta y los IVs, se generarán desde un KDF

El registro de solicitud no contiene ninguna clave de respuesta ChaCha. Esas claves se derivan de un KDF. Ver más abajo.

Todos los campos están en formato big-endian.

Tamaño sin cifrar: 154 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
El campo flags es el mismo que se define en [Tunnel-Creation](/docs/specs/tunnel-creation/) y contiene lo siguiente:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
El bit 7 indica que el salto será un gateway de entrada (IBGW). El bit 6 indica que el salto será un endpoint de salida (OBEP). Si ningún bit está configurado, el salto será un participante intermedio. Ambos no pueden estar configurados al mismo tiempo.

Tipo de cifrado de capa: 0 para AES (como en los tunnels actuales); 1 para futuro (¿ChaCha?)

La expiración de la solicitud es para duración variable futura del tunnel. Por ahora, el único valor soportado es 600 (10 minutos).

La clave pública efímera del creador es una clave ECIES, big-endian. Se utiliza para el KDF para la capa IBGW y las claves de respuesta e IVs. Esto solo se incluye en el registro de texto plano en un mensaje Inbound Tunnel Build. Es necesario porque no hay DH en esta capa para el registro de construcción.

Las opciones de construcción de tunnel son una estructura Mapping como se define en [Common](/docs/specs/common-structures/). Las únicas opciones definidas actualmente son para parámetros de ancho de banda, a partir de la API 0.9.65, consulta los detalles a continuación. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es de 98 bytes, y el valor máximo del campo de longitud del Mapping es 96.

#### Registro de Solicitud Corta Cifrado

Todos los campos están en big-endian excepto la clave pública efímera que está en little-endian.

Tamaño cifrado: 218 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Registros de Respuesta de Construcción Corta

Los BuildReplyRecords encriptados cortos tienen 218 bytes.

#### Registro de Respuesta Corta Sin Cifrar

Resumen de cambios de registros largos:

- Cambiar longitud sin cifrar de 512 a 202 bytes
- Cambiar longitud cifrada de 528 a 218 bytes

Las respuestas ECIES están encriptadas con ChaCha20/Poly1305.

Todos los campos están en formato big-endian.

Tamaño sin cifrar: 202 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Las opciones de respuesta de construcción de tunnel son una estructura Mapping como se define en [Common](/docs/specs/common-structures/). Las únicas opciones definidas actualmente son para parámetros de ancho de banda, a partir de la API 0.9.65, ver abajo para más detalles. Si la estructura Mapping está vacía, esto son dos bytes 0x00 0x00. El tamaño máximo del Mapping (incluyendo el campo de longitud) es de 201 bytes, y el valor máximo del campo de longitud del Mapping es 199.

El byte de respuesta es uno de los siguientes valores según se define en [Tunnel-Creation](/docs/specs/tunnel-creation/) para evitar la creación de huellas digitales:

- 0x00 (aceptar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Un valor de respuesta adicional puede definirse en el futuro para representar el rechazo de opciones no compatibles.

#### Registro de Respuesta Corta Cifrado

Tamaño encriptado: 218 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Usamos la clave de encadenamiento (ck) del estado Noise después del cifrado/descifrado del registro de construcción del túnel para derivar las siguientes claves: clave de respuesta, clave de capa AES, clave IV AES y clave/etiqueta de respuesta garlic para el OBEP.

Claves de respuesta: Ten en cuenta que el KDF es ligeramente diferente para los saltos OBEP y no-OBEP. A diferencia de los registros largos, no podemos usar la parte izquierda de ck para la clave de respuesta, porque no es la última y se usará más tarde. La clave de respuesta se usa para cifrar la respuesta de ese registro usando AEAD/ChaCha20/Poly1305 y ChaCha20 para responder a otros registros. Ambos usan la misma clave. El nonce es la posición del registro en el mensaje comenzando desde 0. Ver detalles a continuación.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Nota: La KDF para la clave IV en el OBEP es diferente a la de los otros saltos, incluso si la respuesta no está cifrada con garlic encryption.

#### Cifrado de Registros

El registro de respuesta del propio hop está cifrado con ChaCha20/Poly1305. Esto es lo mismo que para la especificación de registro largo anterior, EXCEPTO que 'n' es el número de registro 0-7, en lugar de ser siempre 0. Ver [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Los otros registros se cifran de forma iterativa y simétrica en cada salto con ChaCha20 (NO ChaCha20/Poly1305). Esto es diferente de la especificación de registros largos anterior, que utiliza AES y no usa el número de registro.

El número de registro se coloca en el IV en el byte 4, porque ChaCha20 usa un IV de 12 bytes con un nonce little-endian en los bytes 4-11. Ver [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

El encapsulado garlic de los mensajes los oculta del OBEP (para una construcción entrante) o del IBGW (para una construcción saliente). Esto es recomendado pero no requerido. Si el OBEP y el IBGW son el mismo router, no es necesario.

El cifrado garlic de un mensaje Short Tunnel Build Message entrante, por el creador, cifrado al ECIES IBGW, utiliza cifrado Noise 'N', como se define en [ECIES-ROUTERS](/docs/specs/ecies-routers/).

El garlic encryption de un Mensaje de Respuesta de Construcción de Túnel de Salida, por el OBEP, cifrado al creador, utiliza mensajes de Sesión Existente con la clave de respuesta garlic de 32 bytes y la etiqueta de respuesta garlic de 8 bytes del KDF anterior. El formato es como se especifica para las respuestas a las Búsquedas de Base de Datos en [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), y [ECIES-X25519](/docs/specs/ecies/).

#### Cifrado por Capas

Esta especificación incluye un campo de tipo de cifrado de capa en el registro de solicitud de construcción. El único cifrado de capa actualmente soportado es el tipo 0, que es AES. Esto no ha cambiado respecto a especificaciones anteriores, excepto que la clave de capa y la clave IV se derivan del KDF anterior en lugar de estar incluidas en el registro de solicitud de construcción.

Agregar nuevos tipos de cifrado de capa, por ejemplo ChaCha20, es un tema para investigación adicional, y actualmente no es parte de esta especificación.

## Notas de Implementación

- Los routers más antiguos no verifican el tipo de cifrado del salto y enviarán registros cifrados con ElGamal. Algunos routers recientes tienen errores y enviarán varios tipos de registros mal formados. Los implementadores deberían detectar y rechazar estos registros antes de la operación DH si es posible, para reducir el uso de CPU.

### Registros de Construcción

El orden de los registros de construcción debe ser aleatorizado, para que los saltos intermedios no conozcan su ubicación dentro del tunnel.

El número mínimo recomendado de registros de construcción es 4. Si hay más registros de construcción que saltos, se deben agregar registros "falsos", que contengan datos aleatorios o específicos de la implementación. Para las construcciones de túneles de entrada, siempre debe haber un registro "falso" para el router originador, con el prefijo hash de 16 bytes correcto y una clave efímera X25519 real, de lo contrario el salto más cercano sabrá que el siguiente salto es el originador.

El resto del registro "falso" puede ser datos aleatorios, o puede estar cifrado en cualquier formato para que el originador se envíe datos a sí mismo sobre la construcción, quizás para reducir los requisitos de almacenamiento para construcciones pendientes.

Los originadores de túneles entrantes deben usar algún método para validar que su registro "falso" no ha sido modificado por el salto anterior, ya que esto también puede ser usado para desanonimización. El originador puede almacenar y verificar una suma de verificación del registro, o incluir la suma de verificación en el registro, o usar una función de cifrado/descifrado AEAD, dependiendo de la implementación. Si el prefijo hash de 16 bytes u otros contenidos del registro de construcción fueron modificados, el router debe descartar el túnel.

Los registros falsos para túneles de salida, y los registros falsos adicionales para túneles de entrada, no tienen estos requisitos y pueden ser datos completamente aleatorios, ya que nunca serán visibles para ningún salto. Aún así, puede ser deseable que el originador valide que no han sido modificados.

## Parámetros de Ancho de Banda del Tunnel

### Descripción general

A medida que hemos aumentado el rendimiento de la red durante los últimos años con nuevos protocolos, tipos de cifrado y mejoras en el control de congestión, aplicaciones más rápidas como la transmisión de video se están volviendo posibles. Estas aplicaciones requieren un ancho de banda alto en cada salto de sus tunnels de cliente.

Los routers participantes, sin embargo, no tienen información sobre cuánto ancho de banda utilizará un tunnel cuando reciben un mensaje de construcción de tunnel. Solo pueden aceptar o rechazar un tunnel basándose en el ancho de banda total actual utilizado por todos los tunnels participantes y el límite total de ancho de banda para tunnels participantes.

Los routers solicitantes tampoco tienen información sobre cuánto ancho de banda está disponible en cada salto.

Además, los routers actualmente no tienen forma de limitar el tráfico entrante en un túnel. Esto sería muy útil durante momentos de sobrecarga o ataques DDoS a un servicio.

Los parámetros de ancho de banda de tunnel en los mensajes de solicitud y respuesta de construcción de tunnel añaden soporte para estas características. Consulta [Prop168](/proposals/168/) para información adicional de contexto. Estos parámetros están definidos a partir de la API 0.9.65, pero el soporte puede variar según la implementación. Son compatibles tanto para registros de construcción ECIES largos como cortos.

### Opciones de Solicitud de Construcción

Las siguientes tres opciones pueden configurarse en el campo de mapeo de opciones de construcción de tunnel del registro: Un router solicitante puede incluir cualquiera, todas o ninguna.

- m := ancho de banda mínimo requerido para este tunnel (entero positivo en KBps como cadena)
- r := ancho de banda solicitado para este tunnel (entero positivo en KBps como cadena)
- l := límite de ancho de banda para este tunnel; solo enviado a IBGW (entero positivo en KBps como cadena)

Restricción: m <= r <= l

El router participante debe rechazar el túnel si se especifica "m" y no puede proporcionar al menos esa cantidad de ancho de banda.

Las opciones de solicitud se envían a cada participante en el registro de solicitud de construcción cifrado correspondiente, y no son visibles para otros participantes.

### Opción de Respuesta de Construcción

La siguiente opción puede establecerse en el campo de mapeo de opciones de respuesta de construcción de tunnel del registro, cuando la respuesta es ACCEPTED:

- b := ancho de banda disponible para este tunnel (entero positivo en KBps como cadena)

Restricción: b >= m

El router participante debe incluir esto si se especificó "m" o "r" en la solicitud de construcción. El valor debe ser al menos el del valor "m" si se especifica, pero puede ser menor o mayor que el valor "r" si se especifica.

El router participante debe intentar reservar y proporcionar al menos este ancho de banda para el tunnel, sin embargo esto no está garantizado. Los routers no pueden predecir las condiciones 10 minutos en el futuro, y el tráfico participante tiene menor prioridad que el propio tráfico y tunnels del router.

Los routers también pueden sobreasignar el ancho de banda disponible si es necesario, y esto probablemente es deseable, ya que otros saltos en el tunnel podrían rechazarlo.

Por estas razones, la respuesta del router participante debe tratarse como un compromiso de mejor esfuerzo, pero no como una garantía.

Las opciones de respuesta se envían al router solicitante en el registro de respuesta de construcción encriptado correspondiente, y no son visibles para otros participantes.

### Notas de Implementación

Los parámetros de ancho de banda se ven como aparecen en los routers participantes en la capa de túnel, es decir, el número de mensajes de túnel de tamaño fijo de 1 KB por segundo. La sobrecarga de transporte (NTCP2 o SSU2) no está incluida.

Este ancho de banda puede ser mucho mayor o menor que el ancho de banda observado en el cliente. Los mensajes de tunnel contienen una sobrecarga sustancial, incluyendo la sobrecarga de capas superiores como ratchet y streaming. Los mensajes pequeños intermitentes como los acks de streaming se expandirán a 1 KB cada uno. Sin embargo, la compresión gzip en la capa I2CP puede reducir sustancialmente el ancho de banda.

La implementación más simple en el router solicitante es usar los anchos de banda promedio, mínimo y/o máximo de los tunnels actuales en el pool para calcular los valores a incluir en la solicitud. Son posibles algoritmos más complejos y dependen del implementador.

No hay opciones I2CP o SAM definidas actualmente para que el cliente le indique al router qué ancho de banda se requiere, y no se proponen nuevas opciones aquí. Las opciones pueden definirse en una fecha posterior si es necesario.

Las implementaciones pueden usar el ancho de banda disponible o cualquier otro dato, algoritmo, política local o configuración local para calcular el valor de ancho de banda devuelto en la respuesta de construcción.

## Referencias

- [Común](/docs/specs/common-structures/)
- [Criptografía](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Cifrado Múltiple](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Creación de Tunnel](/docs/specs/tunnel-creation/)
