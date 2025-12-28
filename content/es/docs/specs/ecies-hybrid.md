---
title: "Cifrado híbrido con ECIES-X25519-AEAD-Ratchet"
description: "Variante híbrida poscuántica del protocolo de cifrado ECIES (esquema integrado de cifrado sobre curvas elípticas) usando ML-KEM"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Estado de implementación

**Despliegue actual:** - **i2pd (implementación en C++)**: Implementado por completo en la versión 2.58.0 (septiembre de 2025) con soporte para ML-KEM-512, ML-KEM-768 y ML-KEM-1024. El cifrado de extremo a extremo poscuántico se habilita de forma predeterminada cuando esté disponible OpenSSL 3.5.0 o posterior. - **Java I2P**: Aún no implementado hasta la versión 0.9.67 / 2.10.0 (septiembre de 2025). Especificación aprobada y la implementación planificada para versiones futuras.

Esta especificación describe la funcionalidad aprobada que actualmente está desplegada en i2pd y planificada para implementaciones de Java I2P.

## Descripción general

Esta es la variante híbrida poscuántica del protocolo ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Representa la primera fase de la Propuesta 169 [Prop169](/proposals/169-pq-crypto/) en ser aprobada. Consulte esa propuesta para conocer los objetivos generales, los modelos de amenaza, el análisis, las alternativas y la información adicional.

Estado de la propuesta 169: **Abierta** (primera fase aprobada para la implementación híbrida de ECIES (Esquema de Cifrado Integrado basado en Curvas Elípticas)).

Esta especificación contiene únicamente las diferencias respecto del [ECIES](/docs/specs/ecies/) estándar (Esquema de Cifrado Integrado de Curva Elíptica) y debe leerse junto con esa especificación.

## Diseño

Utilizamos el estándar NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), que está basado en, pero no es compatible con, CRYSTALS-Kyber (esquema de encapsulación de claves poscuántico) (versiones 3.1, 3 y anteriores).

Las negociaciones híbridas combinan Diffie-Hellman X25519 clásico con mecanismos de encapsulación de claves ML-KEM poscuánticos. Este enfoque se basa en conceptos de secreto hacia adelante híbrido documentados en la investigación PQNoise y en implementaciones similares en TLS 1.3, IKEv2 y WireGuard.

### Intercambio de claves

Definimos un intercambio de claves híbrido para Ratchet (mecanismo de avance de claves). Un KEM poscuántico proporciona únicamente claves efímeras y no admite directamente handshakes (negociaciones iniciales) con clave estática, como Noise IK (patrón IK del protocolo Noise).

Definimos las tres variantes de ML-KEM (mecanismo de encapsulación de claves basado en retículas modulares) según lo especificado en [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), para un total de 3 nuevos tipos de cifrado. Los tipos híbridos solo se definen en combinación con X25519.

Los nuevos tipos de cifrado son:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Nota:** MLKEM768_X25519 (Tipo 6) es la variante predeterminada recomendada, que proporciona una sólida seguridad poscuántica con una sobrecarga razonable.

La sobrecarga es considerable en comparación con el cifrado únicamente con X25519. Los tamaños típicos de los mensajes 1 y 2 (para IK pattern (patrón IK)) son actualmente alrededor de 96-103 bytes (antes de la carga útil adicional). Esto aumentará aproximadamente 9-12x para MLKEM512, 13-16x para MLKEM768 y 17-23x para MLKEM1024, según el tipo de mensaje.

### Se requiere nueva criptografía

- **ML-KEM** (anteriormente CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Estándar de mecanismo de encapsulación de claves basado en retículas de módulo
- **SHA3-256** (anteriormente Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Parte del estándar SHA-3
- **SHAKE128 y SHAKE256** (extensiones XOF de SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Funciones de salida extensibles (XOF)

Los vectores de prueba para SHA3-256, SHAKE128 y SHAKE256 están disponibles en el [Programa de Validación de Algoritmos Criptográficos del NIST](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Soporte de bibliotecas:** - Java: La biblioteca Bouncycastle versión 1.79 y posteriores admite todas las variantes de ML-KEM y las funciones SHA3/SHAKE - C++: OpenSSL 3.5 y posteriores incluyen compatibilidad completa con ML-KEM (lanzamiento en abril de 2025) - Go: Varias bibliotecas disponibles para la implementación de ML-KEM y SHA3

## Especificación

### Estructuras comunes

Consulte la [Especificación de Estructuras Comunes](/docs/specs/common-structures/) para conocer las longitudes de las claves y los identificadores.

### Patrones de negociación

Los handshakes usan patrones de handshake del [Noise Protocol Framework](https://noiseprotocol.org/noise.html) (marco del Protocolo Noise) con adaptaciones específicas de I2P para seguridad híbrida poscuántica.

Se utiliza la siguiente asignación de letras:

- **e** = clave efímera de un solo uso (X25519)
- **s** = clave estática
- **p** = carga útil del mensaje
- **e1** = clave PQ (poscuántica) efímera de un solo uso, enviada de Alice a Bob (token específico de I2P)
- **ekem1** = el texto cifrado del KEM (mecanismo de encapsulación de claves), enviado de Bob a Alice (token específico de I2P)

**Nota importante:** Los nombres de patrones "IKhfs" e "IKhfselg2" y los tokens "e1" y "ekem1" son adaptaciones específicas de I2P no documentadas en la especificación oficial del Noise Protocol Framework (marco del Protocolo Noise). Estas representan definiciones personalizadas para integrar ML-KEM en el patrón Noise IK (patrón IK de Noise). Aunque el enfoque híbrido X25519 + ML-KEM está ampliamente reconocido en la investigación de criptografía poscuántica y en otros protocolos, la nomenclatura específica utilizada aquí es propia de I2P.

Se aplican las siguientes modificaciones a IK para lograr secreto hacia adelante híbrido:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
El patrón **e1** se define de la siguiente manera:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
El patrón **ekem1** se define de la siguiente manera:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Operaciones definidas de ML-KEM (mecanismo de encapsulación de claves basado en retículas de módulos)

Definimos las siguientes funciones correspondientes a las primitivas criptográficas según lo especificado en [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice crea las claves de encapsulación y desencapsulación. La clave de encapsulación se envía en el mensaje NS. Tamaños de clave:   - ML-KEM-512: encap_key = 800 bytes, decap_key = 1632 bytes   - ML-KEM-768: encap_key = 1184 bytes, decap_key = 2400 bytes   - ML-KEM-1024: encap_key = 1568 bytes, decap_key = 3168 bytes

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob calcula el texto cifrado y la clave compartida usando la clave de encapsulación recibida en el mensaje NS. El texto cifrado se envía en el mensaje NSR. Tamaños del texto cifrado:   - ML-KEM-512: 768 bytes   - ML-KEM-768: 1088 bytes   - ML-KEM-1024: 1568 bytes

El kem_shared_key siempre tiene **32 bytes** en las tres variantes.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice calcula la clave compartida usando el texto cifrado recibido en el mensaje NSR. La kem_shared_key siempre es de **32 bytes**.

**Importante:** Tanto la encap_key como el texto cifrado están cifrados dentro de bloques de ChaCha20-Poly1305 en los mensajes 1 y 2 del handshake de Noise. Se descifrarán como parte del proceso de handshake.

La kem_shared_key se mezcla en la clave de encadenamiento con MixKey(). Véase más abajo para más detalles.

### KDF (función de derivación de claves) del Handshake de Noise

#### Descripción general

El handshake híbrido combina X25519 ECDH clásico con ML-KEM poscuántico (mecanismo de encapsulación de claves). El primer mensaje, de Alice a Bob, contiene e1 (la clave de encapsulación de ML-KEM) antes de la carga útil del mensaje. Esto se considera material de clave adicional; llama a EncryptAndHash() sobre él (como Alice) o a DecryptAndHash() (como Bob). Luego procesa la carga útil del mensaje como de costumbre.

El segundo mensaje, de Bob a Alice, contiene ekem1 (el texto cifrado ML-KEM (mecanismo de encapsulación de claves poscuántico)) antes de la carga útil del mensaje. Se considera material de clave adicional; llama a EncryptAndHash() sobre él (como Bob) o a DecryptAndHash() (como Alice). Luego calcula kem_shared_key y llama a MixKey(kem_shared_key). Después, procesa la carga útil del mensaje como de costumbre.

#### Identificadores de Noise (marco de protocolo criptográfico)

Estas son las cadenas de inicialización de Noise (específicas de I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### KDF de Alice para el mensaje NS

Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', agrega:

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
#### KDF (función de derivación de claves) de Bob para el mensaje NS

Después del patrón de mensajes 'es' y antes del patrón de mensajes 's', añada:

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
#### KDF (función de derivación de claves) de Bob para el mensaje NSR

Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', añada:

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
#### KDF (función de derivación de claves) de Alice para el mensaje NSR

Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'ss', agregue:

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

La función split() permanece sin cambios con respecto a la especificación estándar de ECIES. Tras completar el handshake (negociación inicial):

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Estas son las claves de sesión bidireccionales para la comunicación en curso.

### Formato del mensaje

#### Formato NS (Nueva sesión)

**Cambios:** El ratchet (mecanismo de avance escalonado) actual contiene la clave estática en la primera sección de ChaCha20-Poly1305 y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene la clave pública de ML-KEM cifrada (encap_key). La segunda sección contiene la clave estática. La tercera sección contiene la carga útil.

**Tamaños de mensajes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Nota:** La carga útil debe contener un bloque DateTime (bloque de fecha y hora) (mínimo 7 bytes: 1 byte de tipo, 2 bytes de tamaño, 4 bytes de marca de tiempo). Los tamaños mínimos de NS pueden calcularse en consecuencia. Por lo tanto, el tamaño mínimo práctico de NS es de 103 bytes para X25519 y oscila entre 919 y 1687 bytes para las variantes híbridas.

Los incrementos de tamaño de 816, 1200 y 1584 bytes para las tres variantes de ML-KEM (mecanismo de encapsulación de claves) se deben a la clave pública de ML-KEM más un Poly1305 MAC (código de autenticación de mensajes) de 16 bytes para cifrado autenticado.

#### Formato de NSR (New Session Reply, respuesta de nueva sesión)

**Cambios:** El ratchet (mecanismo de avance criptográfico) actual tiene una carga útil vacía en la primera sección de ChaCha20-Poly1305 y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene el texto cifrado de ML-KEM, cifrado. La segunda sección tiene una carga útil vacía. La tercera sección contiene la carga útil.

**Tamaños de mensajes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Los incrementos de tamaño de 784, 1104 y 1584 bytes para las tres variantes de ML-KEM se deben al texto cifrado de ML-KEM más un MAC Poly1305 de 16 bytes para cifrado autenticado.

## Análisis de sobrecarga

### Intercambio de claves

La sobrecarga del cifrado híbrido es sustancial en comparación con solo X25519:

- **MLKEM512_X25519**: Aproximadamente un incremento de 9-12x en el tamaño del mensaje de handshake (intercambio inicial) (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Aproximadamente un incremento de 13-16x en el tamaño del mensaje de handshake (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Aproximadamente un incremento de 17-23x en el tamaño del mensaje de handshake (NS: 17.5x, NSR: 23x)

Esta sobrecarga es aceptable por los beneficios adicionales de seguridad poscuántica. Los multiplicadores varían según el tipo de mensaje porque los tamaños base de los mensajes difieren (NS mínimo 96 bytes, NSR mínimo 72 bytes).

### Consideraciones sobre el ancho de banda

Para un establecimiento de sesión típico con cargas útiles mínimas: - X25519 solo: ~200 bytes en total (NS + NSR) - MLKEM512_X25519: ~1,800 bytes en total (incremento de 9x) - MLKEM768_X25519: ~2,500 bytes en total (incremento de 12.5x) - MLKEM1024_X25519: ~3,400 bytes en total (incremento de 17x)

Tras el establecimiento de la sesión, el cifrado de los mensajes en curso utiliza el mismo formato de transporte de datos que las sesiones solo X25519, por lo que no introduce sobrecarga adicional en los mensajes posteriores.

## Análisis de seguridad

### Apretones de manos

El handshake híbrido (negociación inicial) proporciona seguridad tanto clásica (X25519) como poscuántica (ML-KEM). Un atacante debe romper **ambos**, el ECDH clásico y el KEM poscuántico, para comprometer las claves de sesión.

Esto proporciona: - **Seguridad actual**: X25519 ECDH proporciona seguridad frente a atacantes clásicos (nivel de seguridad de 128 bits) - **Seguridad futura**: ML-KEM (mecanismo de encapsulación de claves poscuántico) proporciona seguridad frente a atacantes cuánticos (varía según el conjunto de parámetros) - **Seguridad híbrida**: Ambos deben ser vulnerados para comprometer la sesión (nivel de seguridad = máximo de ambos componentes)

### Niveles de seguridad

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Nota:** El nivel de seguridad híbrido está limitado por el más débil de los dos componentes. En todos los casos, X25519 proporciona seguridad clásica de 128 bits. Si llegara a estar disponible una computadora cuántica relevante desde el punto de vista criptográfico, el nivel de seguridad dependería del conjunto de parámetros de ML-KEM (mecanismo de encapsulación de claves basado en retículos modulares) elegido.

### Secreto hacia adelante

El enfoque híbrido mantiene las propiedades de secreto hacia adelante. Las claves de sesión se derivan de ambos intercambios de claves efímeros: X25519 y ML-KEM. Si se destruyen las claves privadas efímeras de X25519 o de ML-KEM tras el handshake, las sesiones pasadas no pueden descifrarse incluso si las claves estáticas a largo plazo se ven comprometidas.

El IK pattern (patrón IK del protocolo Noise) proporciona secreto hacia adelante completo (Noise Confidentiality level 5) tras el envío del segundo mensaje (NSR).

## Preferencias de tipo

Las implementaciones deberían admitir múltiples tipos híbridos y negociar la variante más fuerte admitida por ambas partes. El orden de preferencia debería ser:

1. **MLKEM768_X25519** (Tipo 6) - Predeterminado recomendado, el mejor equilibrio entre seguridad y rendimiento
2. **MLKEM1024_X25519** (Tipo 7) - Máxima seguridad para aplicaciones sensibles
3. **MLKEM512_X25519** (Tipo 5) - Seguridad poscuántica de nivel básico para escenarios con recursos limitados
4. **X25519** (Tipo 4) - Solo clásico, alternativa de respaldo para compatibilidad

**Justificación:** Se recomienda MLKEM768_X25519 como valor predeterminado porque proporciona seguridad de Categoría 3 de NIST (equivalente a AES-192), considerada una protección suficiente frente a las computadoras cuánticas, manteniendo al mismo tiempo tamaños de mensaje razonables. MLKEM1024_X25519 ofrece mayor seguridad, pero con una sobrecarga sustancialmente superior.

## Notas de implementación

### Soporte de bibliotecas

- **Java**: La biblioteca Bouncycastle, a partir de la versión 1.79 (agosto de 2024), admite todas las variantes de ML-KEM (mecanismo de encapsulación de claves poscuántico de NIST) y las funciones SHA3/SHAKE (familia de funciones hash/derivación de NIST). Use `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` para el cumplimiento de FIPS 203 (estándar de NIST).
- **C++**: OpenSSL 3.5 (abril de 2025) y posteriores incluyen compatibilidad con ML-KEM mediante la interfaz EVP_KEM (interfaz de OpenSSL). Esta es una versión con Soporte de Largo Plazo (LTS) mantenida hasta abril de 2030.
- **Go**: Varias bibliotecas de terceros están disponibles para ML-KEM y SHA3, incluida la biblioteca CIRCL de Cloudflare.

### Estrategia de migración

Las implementaciones deberían: 1. Admitir tanto variantes solo X25519 como variantes híbridas de ML-KEM (mecanismo de encapsulación de claves poscuántico) durante el período de transición 2. Preferir las variantes híbridas cuando ambos pares las admitan 3. Mantener un mecanismo de reserva a solo X25519 para compatibilidad con versiones anteriores 4. Considerar las restricciones de ancho de banda de la red al seleccionar la variante predeterminada

### Tunnels compartidos

Los tamaños de mensajes más grandes pueden afectar el uso compartido de tunnel. Las implementaciones deberían considerar: - Agrupar handshakes (intercambios iniciales de negociación) cuando sea posible para amortizar la sobrecarga - Usar tiempos de expiración más cortos para las sesiones híbridas para reducir el estado almacenado - Supervisar el uso de ancho de banda y ajustar los parámetros en consecuencia - Implementar control de congestión para el tráfico de establecimiento de sesión

### Consideraciones sobre el tamaño de nuevas sesiones

Debido al mayor tamaño de los mensajes de handshake (intercambio inicial), las implementaciones pueden necesitar: - Aumentar el tamaño de los búferes para la negociación de sesión (mínimo 4KB recomendado) - Ajustar los valores de tiempo de espera para conexiones más lentas (tener en cuenta que los mensajes son ~3-17x más grandes) - Considerar la compresión de los datos de carga útil en NS/NSR messages (mensajes de tipo NS/NSR) - Implementar la gestión de fragmentación si la capa de transporte lo requiere

### Pruebas y validación

Las implementaciones deberían verificar: - Generación de claves ML-KEM, encapsulación y desencapsulación correctas - Integración adecuada de kem_shared_key en Noise KDF - Que los cálculos del tamaño de los mensajes coincidan con la especificación - Interoperabilidad con otras implementaciones de I2P router - Comportamiento de respaldo cuando ML-KEM no esté disponible

Los vectores de prueba para las operaciones de ML-KEM (mecanismo de encapsulación de claves basado en retículas modulares) están disponibles en el [Programa de Validación de Algoritmos Criptográficos](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) de NIST.

## Compatibilidad de versiones

**Numeración de versiones de I2P:** I2P mantiene dos números de versión en paralelo: - **Versión de lanzamiento del router**: formato 2.x.x (p. ej., 2.10.0 publicado en septiembre de 2025) - **Versión de la API/protocolo**: formato 0.9.x (p. ej., 0.9.67 corresponde al router 2.10.0)

Esta especificación hace referencia a la versión del protocolo 0.9.67, que corresponde a la versión del router 2.10.0 y posteriores.

**Matriz de compatibilidad:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Referencias

- **[ECIES]**: [Especificación ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Propuesta 169: Criptografía poscuántica](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - Estándar ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - Estándar SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Marco del Protocolo Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Especificación de estructuras comunes](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 y Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Documentación de OpenSSL 3.5 ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Biblioteca criptográfica de Java Bouncycastle](https://www.bouncycastle.org/)

---
