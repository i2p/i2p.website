---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Variante híbrida post-cuántica del protocolo de cifrado ECIES usando ML-KEM"
slug: "ecies-hybrid"
category: "Protocolos"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Nota

Implementación, pruebas y despliegue en progreso en las diversas implementaciones de router. Consulta la documentación de esas implementaciones para conocer el estado.

## Resumen

Esta es la variante PQ Hybrid del protocolo ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Es la primera fase de la propuesta general PQ [Prop169](/proposals/169-pq-crypto/) que será aprobada. Consulte esa propuesta para objetivos generales, modelos de amenaza, análisis, alternativas e información adicional.

Esta especificación contiene únicamente las diferencias del [ECIES](/docs/specs/ecies/) estándar y debe leerse junto con esa especificación.

## Diseño

Apoyamos el estándar NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) que se basa en, pero NO es compatible con, CRYSTALS-Kyber.

Los handshakes híbridos están especificados según [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Intercambio de Claves

Definimos un intercambio de claves híbrido para Ratchet. PQ KEM proporciona únicamente claves efímeras y no admite directamente intercambios de claves estáticas como Noise IK.

Definimos las tres variantes de ML-KEM como en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para un total de 3 nuevos tipos de cifrado. Los tipos híbridos solo se definen en combinación con X25519.

Los nuevos tipos de cifrado son:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
La sobrecarga será sustancial. Los tamaños típicos de los mensajes 1 y 2 (para IK) son actualmente de alrededor de 100 bytes (antes de cualquier carga útil adicional). Esto aumentará de 8 a 15 veces dependiendo del algoritmo.

### Nueva Criptografía Requerida

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Usado únicamente para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 y SHAKE256 (extensiones XOF para SHA3-128 y SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Los vectores de prueba para SHA3-256, SHAKE128 y SHAKE256 están en [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Ten en cuenta que la biblioteca Java bouncycastle soporta todo lo anterior. El soporte de la biblioteca C++ está en OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Especificación

### Estructuras Comunes

Consulta la especificación de estructuras comunes [COMMON](/docs/specs/common-structures/) para longitudes de clave e identificadores.

### Patrones de Handshake

Los handshakes utilizan patrones de handshake [Noise](https://noiseprotocol.org/noise.html).

Se utiliza el siguiente mapeo de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje
- e1 = clave PQ efímera de un solo uso, enviada de Alice a Bob
- ekem1 = el texto cifrado KEM, enviado de Bob a Alice

Las siguientes modificaciones a XK e IK para secreto hacia adelante híbrido (hfs) están especificadas en [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
El patrón e1 se define de la siguiente manera, como se especifica en [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 4:

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
El patrón ekem1 se define de la siguiente manera, según se especifica en [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 4:

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
### Operaciones ML-KEM Definidas

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados como se define en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice crea las claves de encapsulación y desencapsulación. La clave de encapsulación se envía en el mensaje NS. Los tamaños de encap_key y decap_key varían según la variante ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob calcula el texto cifrado y la clave compartida, usando el texto cifrado recibido en el mensaje NS. El texto cifrado se envía en el mensaje NSR. El tamaño del texto cifrado varía según la variante ML-KEM. La kem_shared_key siempre es de 32 bytes.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice calcula la clave compartida, utilizando el texto cifrado recibido en el mensaje NSR. La kem_shared_key siempre tiene 32 bytes.

Tenga en cuenta que tanto el encap_key como el texto cifrado están encriptados dentro de bloques ChaCha/Poly en los mensajes 1 y 2 del handshake de Noise. Serán descifrados como parte del proceso de handshake.

El kem_shared_key se mezcla en la clave de encadenamiento con MixHash(). Ver detalles a continuación.

### KDF de Handshake Noise

#### Resumen

El handshake híbrido se define en [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). El primer mensaje, de Alice a Bob, contiene e1, la clave de encapsulación, antes de la carga útil del mensaje. Esto se trata como una clave estática adicional; llama a EncryptAndHash() en ella (como Alice) o DecryptAndHash() (como Bob). Luego procesa la carga útil del mensaje como de costumbre.

El segundo mensaje, de Bob a Alice, contiene ekem1, el texto cifrado, antes de la carga útil del mensaje. Esto se trata como una clave estática adicional; llama a EncryptAndHash() en ella (como Bob) o DecryptAndHash() (como Alice). Luego, calcula el kem_shared_key y llama a MixKey(kem_shared_key). Después procesa la carga útil del mensaje como de costumbre.

#### Identificadores de ruido

Estas son las cadenas de inicialización de Noise:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### KDF de Alice para Mensaje NS

Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', añadir:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### KDF de Bob para Mensaje NS

Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', añadir:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### KDF de Bob para Mensaje NSR

Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', añadir:

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
```
#### Alice KDF para Mensaje NSR

Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'ss', añadir:

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
```
#### KDF para split()

sin cambios

### Formato de Mensaje

#### Formato NS

Cambios: El ratchet actual contenía la clave estática en la primera sección ChaCha, y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene la clave pública PQ cifrada. La segunda sección contiene la clave estática. La tercera sección contiene la carga útil.

Formato cifrado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Formato descifrado:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamaños:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Tenga en cuenta que la carga útil debe contener un bloque DateTime, por lo que el tamaño mínimo de la carga útil es 7. Los tamaños mínimos de NS pueden calcularse en consecuencia.

#### Formato NSR

Cambios: El ratchet actual tiene una carga útil vacía para la primera sección ChaCha, y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene el texto cifrado PQ encriptado. La segunda sección tiene una carga útil vacía. La tercera sección contiene la carga útil.

Formato cifrado:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Formato descifrado:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamaños:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Ten en cuenta que aunque NSR normalmente tendrá una carga útil distinta de cero, la especificación del ratchet [ECIES](/docs/specs/ecies/) no lo requiere, por lo que el tamaño mínimo de carga útil es 0. Los tamaños mínimos de NSR pueden calcularse en consecuencia.

## Análisis de Sobrecarga

### Intercambio de Claves

Aumento de tamaño (bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Velocidad:

Velocidades según reporta [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Análisis de Seguridad

Las categorías de seguridad de NIST se resumen en [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) diapositiva 10. Criterios preliminares: Nuestra categoría mínima de seguridad NIST debería ser 2 para protocolos híbridos y 3 para solo-PQ.

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

Estos son todos protocolos híbridos. Probablemente necesitemos preferir MLKEM768; MLKEM512 no es lo suficientemente seguro.

Categorías de seguridad NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Preferencias de Tipo

El tipo recomendado para el soporte inicial, basado en la categoría de seguridad y la longitud de clave, es:

MLKEM768_X25519 (tipo 6)

## Notas de Implementación

### Soporte de Bibliotecas

Las librerías Bouncycastle, BoringSSL y WolfSSL ahora soportan MLKEM. El soporte de OpenSSL está en su versión 3.5 lanzada el 8 de abril de 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tunnels Compartidos

La clasificación/detección automática de múltiples protocolos en los mismos túneles debería ser posible basándose en una verificación de longitud del mensaje 1 (Mensaje de Nueva Sesión). Usando MLKEM512_X25519 como ejemplo, la longitud del mensaje 1 es 816 bytes mayor que el protocolo ratchet actual, y el tamaño mínimo del mensaje 1 (con solo una carga útil DateTime incluida) es de 919 bytes. La mayoría de los tamaños del mensaje 1 con el ratchet actual tienen una carga útil de menos de 816 bytes, por lo que pueden clasificarse como ratchet no híbrido. Los mensajes grandes probablemente sean POSTs que son raros.

Por lo tanto, la estrategia recomendada es:

- Si el mensaje 1 es menor de 919 bytes, es el protocolo ratchet actual.
- Si el mensaje 1 es mayor o igual a 919 bytes, probablemente sea MLKEM512_X25519. Prueba MLKEM512_X25519 primero, y si falla, prueba el protocolo ratchet actual.

Esto debería permitirnos soportar eficientemente el ratchet estándar y el ratchet híbrido en el mismo destino, tal como anteriormente soportamos ElGamal y ratchet en el mismo destino. Por lo tanto, podemos migrar al protocolo híbrido MLKEM mucho más rápidamente que si no pudiéramos soportar protocolos duales para el mismo destino, porque podemos añadir soporte MLKEM a destinos existentes.

Las combinaciones soportadas requeridas son:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Las siguientes combinaciones pueden ser complejas y NO se requiere que sean compatibles, pero pueden serlo, dependiendo de la implementación:

- Más de un MLKEM
- ElG + uno o más MLKEM
- X25519 + uno o más MLKEM
- ElG + X25519 + uno o más MLKEM

No es necesario soportar múltiples algoritmos MLKEM (por ejemplo, MLKEM512_X25519 y MLKEM_768_X25519) en el mismo destino. Elige solo uno. Depende de la implementación.

No es necesario soportar tres algoritmos (por ejemplo X25519, MLKEM512_X25519, y MLKEM769_X25519) en el mismo destino. La clasificación y estrategia de reintentos puede ser demasiado compleja. La configuración y la interfaz de usuario de configuración pueden ser demasiado complejas. Dependiente de la implementación.

No es necesario soportar algoritmos ElGamal e híbridos en el mismo destino. ElGamal está obsoleto, y solo ElGamal + híbrido (sin X25519) no tiene mucho sentido. Además, tanto los Mensajes de Nueva Sesión ElGamal como Híbridos son grandes, por lo que las estrategias de clasificación a menudo tendrían que intentar ambos descifrados, lo cual sería ineficiente. Dependiente de la implementación.

Los clientes pueden usar las mismas claves estáticas X25519 o diferentes para los protocolos X25519 e híbrido en los mismos túneles, dependiendo de la implementación.

### Secreto Perfecto Hacia Adelante

La especificación ECIES permite Garlic Messages en la carga útil del New Session Message, lo que permite la entrega 0-RTT del paquete de streaming inicial, generalmente un HTTP GET, junto con el leaseset del cliente. Sin embargo, la carga útil del New Session Message no tiene forward secrecy (secreto hacia adelante). Como esta propuesta enfatiza el forward secrecy mejorado para ratchet, las implementaciones pueden o deberían diferir la inclusión de la carga útil de streaming, o el mensaje completo de streaming, hasta el primer Existing Session Message. Esto sería a expensas de la entrega 0-RTT. Las estrategias también pueden depender del tipo de tráfico o tipo de tunnel, o en GET vs. POST, por ejemplo. Dependiente de la implementación.

### Nuevo Tamaño de Sesión

MLKEM aumentará dramáticamente el tamaño del Mensaje de Nueva Sesión, como se describe anteriormente. Esto puede disminuir significativamente la confiabilidad de la entrega del Mensaje de Nueva Sesión a través de tunnels, donde deben ser fragmentados en múltiples mensajes de tunnel de 1024 bytes. El éxito de la entrega es proporcional al número exponencial de fragmentos. Las implementaciones pueden usar varias estrategias para limitar el tamaño del mensaje, a expensas de la entrega 0-RTT. Dependiente de la implementación.

## Referencias

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
