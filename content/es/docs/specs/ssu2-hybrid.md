---
title: "PQ Hybrid SSU2"
description: "Variante híbrida post-cuántica del protocolo de transporte SSU2 utilizando ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transportes"
accurateFor: "0.9.71"
---

### Estado

Beta Q2 2026, lanzamiento Q3 2026

## Descripción general

Esta es la variante híbrida post-cuántica del protocolo de transporte SSU2, tal como se diseñó en la Propuesta 169. Consulte dicha propuesta para obtener información adicional de contexto.

PQ Hybrid SSU2 solo se define en la misma dirección y puerto que el SSU2 estándar. No está permitido operar en un puerto diferente ni sin soporte de SSU2 estándar, y no lo estará durante varios años, hasta que el SSU2 estándar sea declarado obsoleto.

Esta especificación documenta únicamente los cambios necesarios en el SSU2 estándar para admitir PQ Hybrid. Consulte la especificación de SSU2 para obtener los detalles de la implementación base.

## Diseño

Soportamos los estándares NIST FIPS 203 y 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que están basados en, pero NO son compatibles con, CRYSTALS-Kyber y CRYSTALS-Dilithium (versiones 3.1, 3 y anteriores).

### Intercambio de claves

PQ KEM proporciona únicamente claves efímeras y no admite directamente handshakes (intercambios de claves iniciales) con claves estáticas, como Noise XK e IK. Los tipos de cifrado son los mismos que se utilizan en PQ Hybrid Ratchet y están definidos en el documento de estructuras comunes [/docs/specs/common-structures/](/docs/specs/common-structures/); tal como ocurre en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), los tipos híbridos solo se definen en combinación con X25519.

Los tipos de cifrado son:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Combinaciones Legales

Los nuevos tipos de cifrado se indican en los RouterAddresses. El tipo de cifrado en el certificado de clave seguirá siendo el tipo 4.

## Especificación

### Patrones de Handshake

Los handshakes (intercambios de autenticación) utilizan patrones de handshake del [Protocolo Noise](https://noiseprotocol.org/noise.html).

Se utiliza el siguiente mapeo de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje
- e1 = clave PQ efímera de un solo uso, enviada de Alice a Bob
- ekem1 = el texto cifrado KEM, enviado de Bob a Alice

Las siguientes modificaciones a XK e IK para secreto de reenvío híbrido (hfs) se especifican en la sección 5 de la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
El patrón e1 se define de la siguiente manera, según lo especificado en la sección 4 de [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
El patrón ekem1 se define de la siguiente manera, tal como se especifica en la sección 4 de la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF del Handshake Noise

#### Descripción general

El protocolo de enlace híbrido se define en la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). El primer mensaje, de Alice a Bob, contiene e1, la clave de encapsulación, antes de la carga útil del mensaje. Esto se trata como una clave estática adicional; se invoca `EncryptAndHash()` sobre ella (como Alice) o `DecryptAndHash()` (como Bob). Luego se procesa la carga útil del mensaje de la manera habitual.

El segundo mensaje, de Bob a Alice, contiene ekem1, el texto cifrado, antes del payload del mensaje. Esto se trata como una clave estática adicional; se llama a EncryptAndHash() sobre él (como Bob) o DecryptAndHash() (como Alice). Luego, se calcula el kem_shared_key y se llama a MixKey(kem_shared_key). A continuación, se procesa el payload del mensaje de la manera habitual.

#### Operaciones ML-KEM definidas

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados según se definen en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Tenga en cuenta que tanto el encap_key como el texto cifrado están encriptados dentro de bloques ChaCha/Poly en los mensajes 1 y 2 del protocolo de enlace Noise. Serán descifrados como parte del proceso de protocolo de enlace.

El kem_shared_key se mezcla en la clave de encadenamiento con MixHash(). Consulte a continuación para más detalles.

#### KDF de Alice para el Mensaje 1

Después del patrón de mensaje 'es' y antes del payload, añadir:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para el Mensaje 1

Después del patrón de mensaje 'es' y antes del payload, añadir:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para el Mensaje 2

Para XK: Después del patrón de mensaje 'ee' y antes del payload (carga útil), añadir:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF de Alice para el Mensaje 2

Después del patrón de mensaje 'ee', añadir:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF para el Mensaje 3

sin cambios

#### KDF para split()

sin cambios

### Detalles del protocolo de enlace

#### Identificadores de Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Tenga en cuenta que MLKEM-1024 NO es compatible con SSU2, ya que las claves son demasiado grandes para caber en un datagrama estándar de 1500 bytes.

#### Encabezado largo

El encabezado largo tiene 32 bytes. Se utiliza antes de que se cree una sesión, para los mensajes Token Request, SessionRequest, SessionCreated y Retry. También se utiliza para los mensajes Peer Test y Hole Punch fuera de sesión.

En los siguientes mensajes, establezca el campo ver (versión) en el encabezado largo en 3 o 4, para indicar MLKEM-512 o MLKEM-768.

- (0) Solicitud de sesión
- (1) Sesión creada
- (9) Reintento
- (10) Solicitud de token
- (11) Hole Punch

En los siguientes mensajes, establezca el campo ver (versión) en la cabecera larga en 2, como de costumbre, incluso si se admite MLKEM-512 o MLKEM-768. Las implementaciones también pueden establecer el valor en 3 o 4, si el otro extremo lo soporta, pero esto no es necesario. Las implementaciones deben aceptar cualquier valor entre 2 y 4.

- (7) Prueba de par (mensajes fuera de sesión 5-7)

Discusión: Establecer el campo de versión en 3 o 4 puede no ser estrictamente necesario para todos los tipos de mensajes, pero hacerlo ayuda a detectar fallos más tempranamente en conexiones post-cuánticas no compatibles. Los mensajes Token Request y Retry (tipos 9 y 10) deberían tener las versiones 3/4 por coherencia. Los mensajes Hole Punch (tipo 11) pueden no requerir este tratamiento, pero seguiremos el mismo patrón por uniformidad. Los mensajes Peer Test (tipo 7) están fuera de sesión y no indican intención de iniciar una sesión.

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

Antes del cifrado del encabezado:

Antes del cifrado de cabecera:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Encabezado corto

sin cambios

#### SessionRequest (Tipo 0)

Cambios: El SSU2 actual contiene únicamente los datos del bloque en la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Cambio en KDF para protección contra suplantación: Para abordar los problemas planteados en la Propuesta 165 [Prop165]_, pero con una solución diferente, modificamos el KDF para Session Request. Esto aplica únicamente a las sesiones PQ. El KDF para las sesiones no PQ permanece sin cambios.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Contenido sin procesar:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Tamaños, sin incluir la sobrecarga de IP:

| Tipo | Código de Tipo | Long. X | Long. Msg 1 | Long. Msg 1 Enc | Long. Msg 1 Dec | Long. clave PQ | Long. pl |
|------|----------------|---------|-------------|-----------------|-----------------|----------------|----------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado grande | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 y 1338 para IPv6. Ver más abajo.

Cambios: El SSU2 actual contiene solo la carga útil en una única sección ChaCha. Con ML-KEM, habrá una nueva sección ChaCha antes de la carga útil, que contendrá el cifrado PQ cifrado.

#### SessionCreated (Tipo 1)

Cambios: El SSU2 actual contiene solo la carga útil en una única sección ChaCha. Con ML-KEM, habrá una nueva sección ChaCha antes de la carga útil, que contendrá el texto cifrado PQ cifrado.

Contenido sin procesar:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tamaños, sin incluir la sobrecarga de IP:

| Tipo | Código de tipo | Longitud Y | Longitud de Msg 2 | Longitud cifrada de Msg 2 | Longitud descifrada de Msg 2 | Longitud de CT PQ | Longitud de pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado grande | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 y 1338 para IPv6. Ver más abajo.

Tamaño máximo: Alice aún no tiene el RouterInfo de Bob y no conoce su MTU publicado. Para este mensaje, utilice un MTU temporal de la siguiente manera. Para MLKEM512_X25519, use el máximo entre 1280 o el tamaño del SessionRequest recibido como MTU. Para MLKEM768_X25519, use el máximo entre (1318 para IPv4 o 1338 para IPv6) o el tamaño del SessionRequest recibido como MTU. La sobrecarga de SessionCreated es menor que la sobrecarga de SessionRequest, porque el texto cifrado MLKEM es más pequeño que la clave pública MLKEM. Esto permite un rango de tamaños de relleno en SessionCreated incluso si hubiera poco o ningún relleno en el SessionRequest.

#### SessionConfirmed (Tipo 2)

sin cambios

#### KDF para la fase de datos

sin cambios

#### Relay y Prueba de Pares

Los siguientes bloques contienen campos de versión. Permanecerán en la versión 2 (para mantener compatibilidad con un Bob no-PQ) y no cambiarán a la versión 3/4 para PQ.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Direcciones Publicadas

En todos los casos, utilice el nombre de transporte SSU2 como de costumbre. MLKEM-1024 no es compatible.

Utilizar la misma dirección/puerto que el modo no-PQ sin firewall. Se admite una o ambas variantes PQ. En la dirección del router, publicar v=2 (como de costumbre) y el nuevo parámetro pq=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Los routers cuyo MTU sea inferior al mínimo especificado más adelante no deben publicar un parámetro "pq" que contenga "4". Publicar 4,3 para indicar preferencia por MLKEM-768, o 3,4 para indicar preferencia por MLKEM-512. La versión real queda a criterio del iniciador y es posible que la preferencia no se respete. Los routers cuyo MTU sea inferior al mínimo especificado más adelante no deben conectarse usando MLKEM768. Los routers más antiguos ignorarán el parámetro pq y se conectarán en modo no-pq de la forma habitual.

No se admite una dirección/puerto diferente al no-PQ, ni PQ exclusivo sin firewall. Esto no se implementará hasta que SSU2 no-PQ sea deshabilitado, lo cual ocurrirá dentro de varios años. Cuando el modo no-PQ sea deshabilitado, se admitirá una o ambas variantes PQ. En la dirección del router, publique v=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Los routers más antiguos verificarán el parámetro v y omitirán esta dirección por no ser compatible.

Direcciones con firewall (sin IP publicada): En la dirección del router, publicar v=2 (como de costumbre). El parámetro pq DEBE publicarse en las direcciones con firewall para admitir relay.

Alice puede conectarse a un Bob con PQ (post-cuántico) utilizando la variante PQ que Bob publica, independientemente de si Alice anuncia soporte PQ en su router info, o de si anuncia la misma variante.

#### MTU

Ten precaución de no superar el MTU con MLKEM768. El MTU mínimo para MLKEM768_X25519 es 1318 para IPv4 y 1338 para IPv6 (asumiendo un payload mínimo de 10 bytes con un bloque DateTime y un bloque Padding o RelayTagRequest). El MTU mínimo para SSU2 en general es 1280, por lo que no todos los peers pueden utilizar MLKEM768. No publiques ni uses MLKEM768 si el MTU real es inferior al mínimo, ya sea localmente o según lo anunciado por el peer. Ten cuidado de no incluir un tamaño de relleno (padding) tal que el mensaje 1 o 2 supere el MTU local o remoto.

## Análisis de Sobrecarga

### Intercambio de claves

Aumento de tamaño (bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Análisis de Seguridad

Las categorías de seguridad del NIST se resumen en la [presentación del NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf), diapositiva 10. Criterios preliminares: nuestra categoría de seguridad mínima del NIST debería ser 2 para protocolos híbridos y 3 para los exclusivamente de criptografía poscuántica (PQ-only).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Handshakes

Todos estos son protocolos híbridos. Las implementaciones deben preferir MLKEM768; MLKEM512 no es suficientemente seguro.

Categorías de seguridad NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Notas de implementación

### Soporte de biblioteca

Las bibliotecas Bouncycastle, BoringSSL y WolfSSL ya admiten MLKEM y MLDSA. La compatibilidad con OpenSSL estará disponible en su versión 3.5 del 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identificación del Tráfico Entrante

Establecemos el MSB (bit más significativo) de la clave efímera (key[31] & 0x80) en la solicitud de sesión para indicar que se trata de una conexión híbrida. Esto nos permite ejecutar tanto NTCP estándar como NTCP híbrido en el mismo puerto. Solo se admite una variante híbrida para conexiones entrantes, que se anuncia en la dirección del router. Por ejemplo, pq=3 o pq=4.

## Compatibilidad del Router

### Nombres de Transporte

Como Alice, para una conexión PQ, antes de la ofuscación, establece X[31] |= 0x80. Esto hace que X sea una clave pública X25519 inválida. Después de la ofuscación, AES-CBC la aleatorizará. El bit más significativo de X será aleatorio tras la ofuscación.

## Referencias

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
