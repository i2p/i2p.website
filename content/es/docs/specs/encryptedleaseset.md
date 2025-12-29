---
title: "LeaseSet cifrado"
description: "Formato de LeaseSet con control de acceso para Destinos privados"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

Este documento especifica el blinding (cegado), el cifrado y el descifrado de LeaseSet2 (LS2) cifrados. Los LeaseSets cifrados proporcionan la publicación con control de acceso de la información del servicio oculto en la base de datos de la red de I2P.

**Características clave:** - Rotación diaria de claves para secreto hacia adelante - Autorización de clientes en dos niveles (basada en DH y basada en PSK) - Cifrado ChaCha20 para rendimiento en dispositivos sin hardware AES - Firmas Red25519 con cegamiento de clave - Membresía de clientes que preserva la privacidad

**Documentación relacionada:** - [Especificación de estructuras comunes](/docs/specs/common-structures/) - Estructura de LeaseSet cifrado - [Propuesta 123: nuevas entradas de netDB](/proposals/123-new-netdb-entries/) - Contexto sobre LeaseSets cifrados - [Documentación de la base de datos de red](/docs/specs/common-structures/) - Uso de NetDB

---

## Historial de versiones y estado de implementación

### Cronología del desarrollo del protocolo

**Nota importante sobre la numeración de versiones:**   I2P utiliza dos esquemas de numeración de versiones separados: - **Versión de API/Router:** serie 0.9.x (usada en especificaciones técnicas) - **Versión de lanzamiento del producto:** serie 2.x.x (usada para lanzamientos públicos)

Las especificaciones técnicas hacen referencia a versiones de la API (p. ej., 0.9.41), mientras que los usuarios finales ven versiones del producto (p. ej., 2.10.0).

### Hitos de implementación

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Estado actual

- ✅ **Estado del protocolo:** Estable y sin cambios desde junio de 2019
- ✅ **Java I2P:** Totalmente implementado en la versión 0.9.40+
- ✅ **i2pd (C++):** Totalmente implementado en la versión 2.58.0+
- ✅ **Interoperabilidad:** Completa entre implementaciones
- ✅ **Despliegue en la red:** Listo para producción con más de 6 años de experiencia operativa

---

## Definiciones criptográficas

### Notación y convenciones

- `||` denota concatenación
- `mod L` denota la reducción modular por el orden de Ed25519
- Todos los arreglos de bytes están en orden de bytes de red (big-endian), salvo que se especifique lo contrario
- Los valores en little-endian se indican explícitamente

### CSRNG(n) (generador de números aleatorios criptográficamente seguro)

**Generador de números aleatorios criptográficamente seguro**

Produce `n` bytes de datos aleatorios criptográficamente seguros adecuados para la generación de material de clave.

**Requisitos de seguridad:** - Debe ser criptográficamente seguro (adecuado para la generación de claves) - Debe seguir siendo seguro cuando se expongan en la red secuencias de bytes adyacentes - Las implementaciones deberían aplicar una función hash a la salida proveniente de fuentes potencialmente no confiables

**Referencias:** - [Consideraciones de seguridad sobre PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [Discusión en Tor Dev](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Hash SHA-256 con personalización**

Función hash con separación de dominios que recibe: - `p`: Cadena de personalización (proporciona separación de dominios) - `d`: Datos a los que aplicar el hash

**Implementación:**

```
H(p, d) := SHA-256(p || d)
```
**Uso:** Proporciona separación de dominios criptográfica para impedir ataques de colisión entre distintos usos de SHA-256 a nivel de protocolo.

### FLUJO: ChaCha20 (algoritmo de cifrado de flujo)

**Cifrado de flujo: ChaCha20 como se especifica en RFC 7539 Sección 2.4**

**Parámetros:** - `S_KEY_LEN = 32` (clave de 256 bits) - `S_IV_LEN = 12` (nonce de 96 bits; valor único de uso único) - Contador inicial: `1` (RFC 7539 permite 0 o 1; se recomienda 1 para contextos AEAD)

**CIFRAR(k, iv, plaintext)**

Cifra el texto plano usando: - `k`: clave de cifrado de 32 bytes - `iv`: nonce (número usado una vez) de 12 bytes (DEBE ser único para cada clave) - Devuelve un texto cifrado del mismo tamaño que el texto plano

**Propiedad de seguridad:** Todo el texto cifrado debe ser indistinguible de datos aleatorios si la clave es secreta.

**DESCIFRAR(k, iv, ciphertext)**

Descifra el texto cifrado usando: - `k`: clave de cifrado de 32 bytes - `iv`: nonce (número aleatorio de un solo uso) de 12 bytes - Devuelve el texto plano

**Justificación del diseño:** Se eligió ChaCha20 en lugar de AES porque: - 2.5-3 veces más rápido que AES en dispositivos sin aceleración por hardware - La implementación en tiempo constante es más fácil de lograr - Seguridad y velocidad comparables cuando AES-NI está disponible

**Referencias:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 y Poly1305 para Protocolos IETF

### Firma: Red25519 (algoritmo de firma digital basado en Curve25519)

**Esquema de firma: Red25519 (SigType 11) con cegamiento de clave**

Red25519 se basa en firmas Ed25519 sobre la curva Ed25519, utilizando SHA-512 para el cálculo del hash, con soporte para el cegado de claves según lo especificado en ZCash RedDSA.

**Funciones:**

#### DERIVE_PUBLIC(privkey)

Devuelve la clave pública correspondiente a la clave privada indicada. - Utiliza la multiplicación escalar estándar de Ed25519 por el punto base

#### SIGN(privkey, m)

Devuelve una firma generada con la clave privada `privkey` sobre el mensaje `m`.

**Diferencias de firma de Red25519 (variante de Ed25519) respecto de Ed25519 (algoritmo de firma digital EdDSA sobre Curve25519):** 1. **Nonce aleatorio (valor de un solo uso):** Usa 80 bytes de datos aleatorios adicionales

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Esto hace que cada firma Red25519 sea única, incluso para el mismo mensaje y la misma clave.

2. **Generación de claves privadas:** Las claves privadas de Red25519 se generan a partir de números aleatorios y se reducen `mod L`, en lugar de usar el enfoque de bit-clamping (recorte de bits) de Ed25519.

#### VERIFY(pubkey, m, sig)

Verifica la firma `sig` frente a la clave pública `pubkey` y el mensaje `m`. - Devuelve `true` si la firma es válida, `false` en caso contrario - La verificación es idéntica a Ed25519 (algoritmo de firma digital)

**Operaciones de cegado de claves:**

#### GENERATE_ALPHA(data, secret)

Genera alfa para el cegado de clave. - `data`: Normalmente contiene la clave pública de firma y los tipos de firma - `secret`: Secreto adicional opcional (longitud cero si no se usa) - El resultado sigue la misma distribución que las claves privadas Ed25519 (después de la reducción mod L)

#### BLIND_PRIVKEY(privkey, alpha)

Ciega una clave privada usando el secreto `alpha`. - Implementación: `blinded_privkey = (privkey + alpha) mod L` - Usa aritmética escalar en el campo

#### BLIND_PUBKEY(pubkey, alpha)

Ciega una clave pública usando el secreto `alpha`. - Implementación: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Usa la adición de elementos del grupo (puntos) en la curva

**Propiedad crítica:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Consideraciones de seguridad:**

De la Especificación del Protocolo de ZCash, Sección 5.4.6.1: Por seguridad, alpha debe tener la misma distribución que las claves privadas sin cegar. Esto garantiza que "la combinación de una clave pública re-aleatorizada y de firmas realizadas con esa clave no revele la clave a partir de la cual fue re-aleatorizada."

**Tipos de firma compatibles:** - **Tipo 7 (Ed25519):** Compatible con destinos existentes (compatibilidad retroactiva) - **Tipo 11 (Red25519):** Recomendado para nuevos destinos que usan cifrado - **Claves cegadas:** Use siempre el tipo 11 (Red25519)

**Referencias:** - [Especificación del Protocolo de ZCash](https://zips.z.cash/protocol/protocol.pdf) - Sección 5.4.6 RedDSA (esquema de firma digital) - [Especificación Red25519 de I2P](/docs/specs/red25519-signature-scheme/)

### DH (Diffie-Hellman): X25519

**Diffie-Hellman de curva elíptica: X25519**

Sistema de acuerdo de claves de clave pública basado en Curve25519.

**Parámetros:** - Claves privadas: 32 bytes - Claves públicas: 32 bytes - Resultado del secreto compartido: 32 bytes

**Funciones:**

#### GENERATE_PRIVATE()

Genera una nueva clave privada de 32 bytes usando CSRNG (generador de números aleatorios criptográficamente seguro).

#### DERIVE_PUBLIC(privkey)

Deriva la clave pública de 32 bytes a partir de la clave privada proporcionada. - Utiliza multiplicación escalar en Curve25519 (curva elíptica sobre el campo 2^255−19).

#### DH(privkey, pubkey)

Realiza el acuerdo de claves Diffie-Hellman. - `privkey`: Clave privada local de 32 bytes - `pubkey`: Clave pública remota de 32 bytes - Devuelve: Secreto compartido de 32 bytes

**Propiedades de seguridad:** - Supuesto de Diffie-Hellman computacional en Curve25519 - Secreto hacia adelante cuando se usan claves efímeras - Se requiere una implementación de tiempo constante para prevenir ataques de temporización

**Referencias:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Curvas elípticas para la seguridad

### HKDF (función de derivación de claves basada en HMAC)

**Función de derivación de claves basada en HMAC**

Extrae y expande el material de claves a partir del material de claves de entrada.

**Parámetros:** - `salt`: 32 bytes como máximo (típicamente 32 bytes para SHA-256) - `ikm`: Material de clave de entrada (cualquier longitud, debe tener buena entropía) - `info`: Información específica del contexto (separación de dominios) - `n`: Longitud de salida en bytes

**Implementación:**

Utiliza HKDF (función de derivación de claves basada en HMAC) según lo especificado en RFC 5869 con:
- **Función hash:** SHA-256
- **HMAC:** Según lo especificado en RFC 2104
- **Longitud de la sal:** Máximo 32 bytes (HashLen para SHA-256)

**Patrón de uso:**

```
keys = HKDF(salt, ikm, info, n)
```
**Separación de dominios:** El parámetro `info` proporciona separación de dominios criptográfica entre los distintos usos de HKDF (función de derivación de claves basada en HMAC) en el protocolo.

**Valores de información verificada:** - `"ELS2_L1K"` - cifrado de Capa 1 (externa) - `"ELS2_L2K"` - cifrado de Capa 2 (interna) - `"ELS2_XCA"` - autorización de cliente DH - `"ELS2PSKA"` - autorización de cliente PSK - `"i2pblinding1"` - generación de Alpha (parámetro alpha)

**Referencias:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Especificación de HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Especificación de HMAC

---

## Especificación del formato

El LS2 cifrado consta de tres capas anidadas:

1. **Capa 0 (Externa):** Información en texto plano para almacenamiento y recuperación
2. **Capa 1 (Intermedia):** Datos de autenticación del cliente (cifrados)
3. **Capa 2 (Interna):** Datos reales de LeaseSet2 (conjunto de arrendamientos de I2P de segunda generación) (cifrados)

**Estructura general:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Importante:** El LS2 cifrado utiliza claves cegadas. El Destino no está en la cabecera. La ubicación de almacenamiento en la DHT es `SHA-256(sig type || blinded public key)` y se rota diariamente.

### Capa 0 (Externa) - Texto en claro

La Capa 0 NO utiliza el encabezado LS2 estándar. Tiene un formato personalizado optimizado para claves cegadas.

**Estructura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Campo de banderas (2 bytes, bits 15-0):** - **Bit 0:** Indicador de claves fuera de línea   - `0` = Sin claves fuera de línea   - `1` = Hay claves fuera de línea (siguen datos de clave temporales) - **Bits 1-15:** Reservados, deben ser 0 para compatibilidad futura

**Datos de clave transitorios (presentes si el bit de bandera 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Verificación de firma:** - **Sin claves fuera de línea:** Verificar con clave pública cegada - **Con claves fuera de línea:** Verificar con clave pública temporal

La firma cubre todos los datos desde Type hasta outerCiphertext (inclusive).

### Capa 1 (Intermedia) - Autorización del cliente

**Descifrado:** Consulte la sección [Cifrado de la Capa 1](#layer-1-encryption).

**Estructura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Campo Flags (1 byte, bits 7-0):** - **Bit 0:** Modo de autorización   - `0` = Sin autorización por cliente (todos)   - `1` = Autorización por cliente (sigue la sección de autenticación) - **Bits 3-1:** Esquema de autenticación (solo si el bit 0 = 1)   - `000` = Autenticación de cliente DH   - `001` = Autenticación de cliente PSK   - Otros, reservados - **Bits 7-4:** Sin uso, debe ser 0

**Datos de autorización del cliente DH (flags = 0x01, bits 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrada de authClient (40 bytes):** - `clientID_i`: 8 bytes - `clientCookie_i`: 32 bytes (authCookie cifrada)

**Datos de autorización del cliente PSK (clave precompartida) (indicadores = 0x03, bits 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrada authClient (40 bytes):** - `clientID_i`: 8 bytes - `clientCookie_i`: 32 bytes (authCookie cifrado)

### Capa 2 (interna) - Datos de LeaseSet (registro de túneles de un destino en I2P)

**Descifrado:** Consulte la sección [Cifrado de Capa 2](#layer-2-encryption).

**Estructura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
La capa interna contiene la estructura completa de LeaseSet2, que incluye: - Encabezado de LS2 - Información de Lease - Firma de LS2

**Requisitos de verificación:** Tras el descifrado, las implementaciones deben verificar: 1. La marca de tiempo interna coincide con la marca de tiempo publicada externa 2. La expiración interna coincide con la expiración externa 3. La firma de LS2 es válida 4. Los datos de lease (entrada de túnel con expiración) están bien formados

**Referencias:** - [Especificación de Estructuras Comunes](/docs/specs/common-structures/) - detalles del formato de LeaseSet2

---

## Derivación de la clave de cegado

### Descripción general

I2P utiliza un esquema aditivo de cegamiento de claves basado en Ed25519 y ZCash RedDSA. Las claves cegadas se rotan diariamente (medianoche UTC) para proporcionar secreto hacia adelante.

**Justificación del diseño:**

I2P optó explícitamente por NO usar el enfoque del Apéndice A.2 del rend-spec-v3.txt de Tor. Según la especificación:

> "No usamos el apéndice A.2 de rend-spec-v3.txt de Tor, que persigue objetivos de diseño similares, porque sus claves públicas cegadas podrían quedar fuera del subgrupo de orden primo, con implicaciones de seguridad desconocidas."

El cegamiento aditivo de I2P garantiza que las claves cegadas permanezcan en el subgrupo de orden primo de la curva Ed25519.

### Definiciones matemáticas

**Parámetros de Ed25519:** - `B`: punto base de Ed25519 (generador) = `2^255 - 19` - `L`: orden de Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Variables clave:** - `A`: clave pública de firma no cegada de 32 bytes (en Destination (Destino)) - `a`: clave privada de firma no cegada de 32 bytes - `A'`: clave pública de firma cegada de 32 bytes (usada en LeaseSet cifrado) - `a'`: clave privada de firma cegada de 32 bytes - `alpha`: factor de cegado de 32 bytes (secreto)

**Funciones auxiliares:**

#### LEOS2IP(x)

"Cadena de octetos en orden little-endian a entero"

Convierte un array de bytes en formato little-endian (orden de bytes de menor peso primero) a su representación entera.

#### H*(x)

"Hash y reducción"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
La misma operación que en la generación de claves Ed25519.

### Generación Alfa

**Rotación diaria:** Se DEBEN generar un nuevo alpha y nuevas blinded keys (claves cegadas) cada día a la medianoche UTC (00:00:00 UTC).

**Algoritmo GENERATE_ALPHA(destination, date, secret):**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Parámetros verificados:** - Personalización de la sal: `I2PGenerateAlpha` - Información de HKDF: `i2pblinding1` - Salida: 64 bytes antes de la reducción - Distribución de alfa: Con la misma distribución que las claves privadas de Ed25519 después de `mod L`

### Cegado de clave privada

**Algoritmo BLIND_PRIVKEY(a, alpha):**

Para el propietario del destino al publicar el LeaseSet cifrado:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Crítico:** La reducción `mod L` es esencial para mantener la relación algebraica correcta entre las claves privadas y públicas.

### Cegamiento de clave pública

**Algoritmo BLIND_PUBKEY(A, alpha):**

Para los clientes que recuperan y verifican el LeaseSet cifrado:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Equivalencia matemática:**

Ambos métodos producen resultados idénticos:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Esto se debe a:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Firma con claves cegadas

**Firma de LeaseSet sin ceguera:**

El LeaseSet descegado (enviado directamente a clientes autenticados) se firma mediante: - Firma Ed25519 estándar (tipo 7) o Red25519 (tipo 11) - Clave privada de firma descegada - Verificada con la clave pública descegada

**Con claves sin conexión:** - Firmado por una clave privada temporal descegada - Verificado con una clave pública temporal descegada - Ambas deben ser de tipo 7 o 11

**Firma de LeaseSet cifrado:**

La parte externa del LeaseSet cifrado utiliza firmas Red25519 con claves cegadas.

**Algoritmo de firma Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Diferencias clave respecto a Ed25519:** 1. Usa 80 bytes de datos aleatorios `T` (no el hash de la clave privada) 2. Usa el valor de la clave pública directamente (no el hash de la clave privada) 3. Cada firma es única incluso para el mismo mensaje y la misma clave

**Verificación:**

Igual que Ed25519:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Consideraciones de seguridad

**Distribución alfa:**

Por seguridad, alpha debe tener la misma distribución que las claves privadas sin cegar. Al cegar Ed25519 (esquema de firma Ed25519) (type 7) a Red25519 (variante Red25519) (type 11), las distribuciones difieren ligeramente.

**Recomendación:** Utilice Red25519 (tipo 11) tanto para claves no cegadas como para claves cegadas para cumplir los requisitos de ZCash: "la combinación de una clave pública realeatorizada y firma(s) bajo esa clave no revela la clave a partir de la cual fue realeatorizada."

**Soporte de tipo 7:** Se admite Ed25519 por compatibilidad retroactiva con destinos existentes, pero se recomienda el tipo 11 para nuevos destinos cifrados.

**Beneficios de la rotación diaria:** - Secreto hacia adelante: Comprometer la clave cegada de hoy no revela la de ayer - No vinculabilidad: La rotación diaria evita el rastreo a largo plazo vía DHT (tabla hash distribuida) - Separación de claves: Claves diferentes para distintos periodos de tiempo

**Referencias:** - [Especificación del Protocolo de ZCash](https://zips.z.cash/protocol/protocol.pdf) - Sección 5.4.6.1 - [Discusión sobre el cegado de claves (key blinding) de Tor](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Ticket de Tor #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Cifrado y procesamiento

### Derivación de la subcredencial

Antes del cifrado, derivamos una credencial y una subcredencial para vincular las capas cifradas al conocimiento de la clave pública de firma de Destination (identidad de destino en I2P).

**Objetivo:** Garantizar que solo quienes conocen la clave pública de firma del Destino puedan descifrar el LeaseSet cifrado. No se requiere el Destino completo.

#### Cálculo de credenciales

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Separación de dominios:** La cadena de personalización `"credential"` garantiza que este hash no colisione con ninguna de las claves de búsqueda de la DHT ni con otros usos del protocolo.

#### Cálculo de subcredencial

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Propósito:** La subcredencial vincula el LeaseSet cifrado a: 1. El Destino específico (mediante la credencial) 2. La clave cegada específica (mediante blindedPublicKey) 3. El día específico (mediante la rotación diaria de blindedPublicKey)

Esto previene los ataques de repetición y la vinculación entre días.

### Cifrado de capa 1

**Contexto:** La capa 1 contiene datos de autorización del cliente y está cifrada con una clave derivada de la subcredencial.

#### Algoritmo de cifrado

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Salida:** `outerCiphertext` es `32 + len(outerPlaintext)` bytes.

**Propiedades de seguridad:** - La sal garantiza pares clave/IV únicos incluso con la misma subcredencial - La cadena de contexto `"ELS2_L1K"` proporciona separación de dominios - ChaCha20 proporciona seguridad semántica (texto cifrado indistinguible de datos aleatorios)

#### Algoritmo de descifrado

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Verificación:** Tras el descifrado, verifica que la estructura de la Capa 1 esté bien formada antes de continuar con la Capa 2.

### Cifrado de Capa 2

**Contexto:** La Capa 2 contiene los datos propiamente dichos de LeaseSet2 y está cifrada con una clave derivada de authCookie (si la autenticación por cliente está habilitada) o de una cadena vacía (si no).

#### Algoritmo de cifrado

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Salida:** `innerCiphertext` es de `32 + len(innerPlaintext)` bytes.

**Vinculación de claves:** - Si no hay autenticación de cliente: Vinculado solo a la subcredencial y la marca de tiempo - Si la autenticación de cliente está habilitada: Vinculado además a authCookie (diferente para cada cliente autorizado)

#### Algoritmo de descifrado

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Verificación:** Después del descifrado: 1. Verificar que el byte de tipo de LS2 (LeaseSet versión 2) sea válido (3 o 7) 2. Analizar la estructura de LeaseSet2 3. Verificar que la marca de tiempo interna coincida con la marca de tiempo externa publicada 4. Verificar que la expiración interna coincida con la expiración externa 5. Verificar la firma de LeaseSet2

### Resumen de la capa de cifrado

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Flujo de descifrado:** 1. Verificar la firma de la Capa 0 con la clave pública cegada 2. Descifrar la Capa 1 usando subcredential 3. Procesar los datos de autorización (si están presentes) para obtener authCookie 4. Descifrar la Capa 2 usando authCookie y subcredential 5. Verificar y analizar LeaseSet2

---

## Autorización por cliente

### Descripción general

Cuando la autorización por cliente está habilitada, el servidor mantiene una lista de clientes autorizados. Cada cliente dispone de material de claves que debe transmitirse de forma segura por un canal fuera de banda.

**Dos mecanismos de autorización:** 1. **Autorización de cliente DH (Diffie-Hellman):** Más segura, usa el acuerdo de claves X25519 2. **Autorización PSK (Pre-Shared Key, clave precompartida):** Más simple, usa claves simétricas

**Propiedades de seguridad comunes:** - Privacidad de pertenencia de clientes: Los observadores ven el número de clientes pero no pueden identificar clientes específicos - Adición/revocación anónima de clientes: No se puede rastrear cuándo se agregan o eliminan clientes específicos - Probabilidad de colisión del identificador de cliente de 8 bytes: ~1 en 18 quintillones (insignificante)

### Autorización de cliente DH

**Descripción general:** Cada cliente genera un par de claves X25519 y envía su clave pública al servidor a través de un canal seguro fuera de banda. El servidor utiliza DH efímero para cifrar un authCookie único para cada cliente.

#### Generación de claves del cliente

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Ventaja de seguridad:** La clave privada del cliente nunca sale de su dispositivo. Un adversario que intercepte la transmisión fuera de banda no podrá descifrar futuros LeaseSets cifrados sin romper X25519 DH.

#### Procesamiento del servidor

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Estructura de datos de la capa 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Recomendaciones para el servidor:** - Generar un nuevo par de claves efímero para cada LeaseSet cifrado publicado - Aleatorizar el orden de los clientes para evitar el seguimiento basado en la posición - Considerar añadir entradas ficticias para ocultar el número real de clientes

#### Procesamiento del cliente

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Manejo de errores del cliente:** - Si `clientID_i` no se encuentra: El cliente ha sido revocado o nunca fue autorizado - Si falla el descifrado: Datos corruptos o claves incorrectas (extremadamente raro) - Los clientes deberían volver a obtener los datos periódicamente para detectar la revocación

### Autorización de cliente mediante PSK (clave precompartida)

**Descripción general:** Cada cliente tiene una clave simétrica de 32 bytes precompartida. El servidor cifra el mismo authCookie usando el PSK (clave precompartida) de cada cliente.

#### Generación de claves

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Nota de seguridad:** La misma PSK puede compartirse entre varios clientes si se desea (crea una autorización de "grupo").

#### Procesamiento del servidor

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Estructura de datos de la capa 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Procesamiento del cliente

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Comparación y recomendaciones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Recomendación:** - **Utiliza DH authorization (autorización DH)** para aplicaciones de alta seguridad donde el secreto hacia adelante es importante - **Utiliza PSK authorization (autorización con clave precompartida)** cuando el rendimiento es crítico o cuando se gestionan grupos de clientes - **Nunca reutilices PSKs** entre distintos servicios ni en diferentes períodos de tiempo - **Utiliza siempre canales seguros** para la distribución de claves (p. ej., Signal, OTR, PGP)

### Consideraciones de seguridad

**Privacidad de la membresía del cliente:**

Ambos mecanismos proporcionan privacidad respecto a la pertenencia de clientes mediante: 1. **Identificadores de cliente cifrados:** clientID de 8 bytes derivado de la salida de HKDF 2. **Cookies indistinguibles:** Todos los valores clientCookie de 32 bytes parecen aleatorios 3. **Sin metadatos específicos del cliente:** No hay manera de identificar qué entrada pertenece a qué cliente

Un observador puede ver: - Número de clientes autorizados (del campo `clients`) - Cambios en la cantidad de clientes a lo largo del tiempo

Un observador NO PUEDE ver: - Qué clientes específicos están autorizados - Cuándo se añaden o se eliminan clientes específicos (si el recuento se mantiene igual) - Cualquier información que identifique a un cliente

**Recomendaciones de aleatorización:**

Los servidores DEBERÍAN aleatorizar el orden de los clientes cada vez que generen un LeaseSet cifrado:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Beneficios:** - Evita que los clientes conozcan su posición en la lista - Evita ataques de inferencia basados en cambios de posición - Hace que la adición/revocación de clientes sea indistinguible

**Ocultación del recuento de clientes:**

Los servidores PUEDEN insertar entradas ficticias aleatorias:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Costo:** Las entradas ficticias incrementan el tamaño del LeaseSet cifrado (40 bytes cada una).

**Rotación de AuthCookie:**

Los servidores DEBERÍAN generar un nuevo authCookie: - Cada vez que se publique un LeaseSet cifrado (típicamente cada pocas horas) - Inmediatamente después de revocar a un cliente - En un horario regular (p. ej., diariamente), aunque no cambie ningún cliente

**Beneficios:** - Limita la exposición si se compromete authCookie - Garantiza que los clientes revocados pierdan el acceso rápidamente - Proporciona secreto perfecto hacia adelante para la Capa 2

---

## Direccionamiento Base32 para LeaseSets cifrados

### Descripción general

Las direcciones base32 tradicionales de I2P contienen únicamente el hash del Destino (32 bytes → 52 caracteres). Esto es insuficiente para LeaseSets cifrados porque:

1. Los clientes necesitan la **clave pública no cegada** para derivar la clave pública cegada
2. Los clientes necesitan los **tipos de firma** (no cegada y cegada) para derivar correctamente las claves
3. El hash por sí solo no proporciona esta información

**Solución:** Un nuevo formato base32 que incluye la clave pública y los tipos de firma.

### Especificación del formato de direcciones

**Estructura decodificada (35 bytes):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**Primeros 3 bytes (XOR con suma de verificación):**

Los primeros 3 bytes contienen metadatos combinados mediante XOR con partes de una suma de verificación CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Propiedades de la suma de verificación:** - Usa el polinomio CRC-32 estándar - Tasa de falsos negativos: ~1 en 16 millones - Proporciona detección de errores ante errores tipográficos en direcciones - No puede usarse como autenticación (no es criptográficamente seguro)

**Formato codificado:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Características:** - Total de caracteres: 56 (35 bytes × 8 bits ÷ 5 bits por carácter) - Sufijo: ".b32.i2p" (igual que el base32 tradicional) - Longitud total: 56 + 8 = 64 caracteres (excluyendo el terminador nulo)

**Codificación Base32:** - Alfabeto: `abcdefghijklmnopqrstuvwxyz234567` (estándar RFC 4648) - Los 5 bits no utilizados al final DEBEN ser 0 - No distingue mayúsculas de minúsculas (por convención en minúsculas)

### Generación de direcciones

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Análisis de direcciones

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Comparación con Base32 tradicional

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Restricciones de uso

**Incompatibilidad con BitTorrent:**

Las direcciones LS2 (LeaseSet2, segunda generación de LeaseSet) cifradas NO PUEDEN utilizarse con las respuestas compactas del announce de BitTorrent:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Problema:** El formato compacto solo contiene el hash (32 bytes), sin espacio para tipos de firma ni información de clave pública.

**Solución:** Use respuestas completas de announce (endpoint de anuncio del rastreador) o rastreadores basados en HTTP que admitan direcciones completas.

### Integración de la libreta de direcciones

Si un cliente tiene el Destino completo en una libreta de direcciones:

1. Almacenar el Destination (identificador de destino en I2P) completo (incluye la clave pública)
2. Admitir búsqueda inversa por hash
3. Cuando se encuentre un LS2 (LeaseSet 2, formato de leaseSet de segunda generación) cifrado, recuperar la clave pública desde la libreta de direcciones
4. No es necesario un nuevo formato base32 si el Destination completo ya se conoce

**Formatos de libreta de direcciones que admiten LS2 cifrado:** - hosts.txt con cadenas de destino completas - bases de datos SQLite con columna de destino - formatos JSON/XML con datos de destino completos

### Ejemplos de implementación

**Ejemplo 1: Generar dirección**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Ejemplo 2: Analizar y validar**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Ejemplo 3: Convertir desde Destination (destino de I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Consideraciones de seguridad

**Privacidad:** - La dirección Base32 revela la clave pública - Esto es intencionado y requerido por el protocolo - NO revela la clave privada ni compromete la seguridad - Las claves públicas son información pública por diseño

**Resistencia a colisiones:** - CRC-32 proporciona solo 32 bits de resistencia a colisiones - No es criptográficamente seguro (usar solo para detección de errores) - NO confíe en la suma de verificación para la autenticación - Aún se requiere la verificación completa del destino

**Validación de direcciones:** - Siempre valide la suma de verificación antes de usarla - Rechace direcciones con tipos de firma no válidos - Verifique que la clave pública esté en la curva (específico de la implementación)

**Referencias:** - [Propuesta 149: B32 para LS2 cifrado](/proposals/149-b32-encrypted-ls2/) - [Especificación de direccionamiento B32](/docs/specs/b32-for-encrypted-leasesets/) - [Especificación de nombres de I2P](/docs/overview/naming/)

---

## Soporte para claves sin conexión

### Descripción general

Las claves fuera de línea permiten que la clave de firma principal se mantenga fuera de línea (almacenamiento en frío), mientras se utiliza una clave de firma temporal para las operaciones diarias. Esto es crítico para servicios de alta seguridad.

**Requisitos específicos de LS2 cifrado:** - Las claves transitorias deben generarse sin conexión - Las claves privadas cegadas deben pre-generarse (una por día) - Tanto las claves transitorias como las cegadas se entregan en lotes - Aún no se ha definido un formato de archivo estandarizado (TODO en la especificación)

### Estructura de la clave fuera de línea

**Datos de clave efímera de la capa 0 (cuando el bit 0 de la bandera = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Cobertura de la firma:** La firma en el bloque de clave fuera de línea abarca: - Marca de tiempo de expiración (4 bytes) - Tipo de firma transitoria (2 bytes)   - Clave pública de firma transitoria (variable)

Esta firma se verifica mediante la **clave pública cegada**, lo que demuestra que la entidad con la clave privada cegada autorizó esta clave efímera.

### Proceso de generación de claves

**Para LeaseSet cifrado con claves fuera de línea:**

1. **Generar pares de claves efímeros** (sin conexión, en almacenamiento en frío):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Para cada día    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Para cada fecha    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# A medianoche UTC (o antes de publicar)

date = datetime.utcnow().date()

# Cargar claves para hoy

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Utilice estas claves para el LeaseSet cifrado de hoy

```

**Publishing Process:**

```python
# 1. Crear LeaseSet2 (segunda generación del formato LeaseSet de I2P) interno

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Cifrar la capa 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Crear la Capa 1 con datos de autorización

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Cifrar la capa 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Crear la Capa 0 con un bloque de firma sin conexión

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Firmar la Capa 0 con una clave privada efímera

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Añade la firma y publica

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Generar todos los días tanto nuevas claves temporales como nuevas claves cegadas

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Lote de material de claves cifrado   - Rango de fechas cubierto

OFFLINE_KEY_STATUS   - Número de días restantes   - Próxima fecha de expiración de la clave

REVOKE_OFFLINE_KEYS     - Rango de fechas a revocar   - Nuevas claves para reemplazar (opcional)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Habilitar LeaseSet cifrado

i2cp.encryptLeaseSet=true

# Opcional: Habilitar la autorización de clientes

i2cp.enableAccessList=true

# Opcional: Usar autorización DH (el valor predeterminado es PSK)

i2cp.accessListType=0

# Opcional: Secreto de cegado (altamente recomendado)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// Crear LeaseSet cifrado EncryptedLeaseSet els = new EncryptedLeaseSet();

// Establecer destino els.setDestination(destination);

// Habilitar la autorización por cliente els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Agregar clientes autorizados (claves públicas DH) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Configura los parámetros de blinding (cegado criptográfico) els.setBlindingSecret("your-secret");

// Firmar y publicar els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Habilitar LeaseSet cifrado

encryptleaseset = true

# Opcional: tipo de autorización del cliente (0=DH, 1=PSK)

authtype = 0

# Opcional: Blinding secret (secreto utilizado en blinding, técnica criptográfica de cegado)

secret = tu-secreto-aquí

# Opcional: Clientes autorizados (uno por línea, claves públicas codificadas en base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// Crear LeaseSet cifrado auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Habilitar la autorización por cliente encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Agregar clientes autorizados for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Sign and publish encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Vector de prueba 1: cegado de clave

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Esperado: (verificar frente a la implementación de referencia)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Punto base de Ed25519 (generador)

B = 2**255 - 19

# Orden de Ed25519 (tamaño del campo escalar)

L = 2**252 + 27742317777372353535851937790883648493

# Valores del tipo de firma

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Tamaños de clave

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# Parámetros de ChaCha20

CHACHA20_KEY_SIZE = 32   # bytes (256 bits) CHACHA20_NONCE_SIZE = 12  # bytes (96 bits) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 permite 0 o 1

```

### HKDF Constants

```python
# Parámetros de HKDF

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# Cadenas 'info' de HKDF (separación de dominios)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# Cadenas de personalización de SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Tamaños de la capa 0 (externa)

BLINDED_SIGTYPE_SIZE = 2   # bytes BLINDED_PUBKEY_SIZE = 32   # bytes (para Red25519) PUBLISHED_TS_SIZE = 4      # bytes EXPIRES_SIZE = 2           # bytes FLAGS_SIZE = 2             # bytes LEN_OUTER_CIPHER_SIZE = 2  # bytes SIGNATURE_SIZE = 64        # bytes (Red25519)

# Tamaños de bloques de claves sin conexión

OFFLINE_EXPIRES_SIZE = 4   # bytes OFFLINE_SIGTYPE_SIZE = 2   # bytes OFFLINE_SIGNATURE_SIZE = 64  # bytes

# Tamaños de la capa 1 (intermedia)

AUTH_FLAGS_SIZE = 1        # byte EPHEMERAL_PUBKEY_SIZE = 32  # bytes (autenticación DH) AUTH_SALT_SIZE = 32        # bytes (autenticación PSK) NUM_CLIENTS_SIZE = 2       # bytes CLIENT_ID_SIZE = 8         # bytes CLIENT_COOKIE_SIZE = 32    # bytes AUTH_CLIENT_ENTRY_SIZE = 40  # bytes (CLIENT_ID + CLIENT_COOKIE)

# Sobrecarga del cifrado

SALT_SIZE = 32  # bytes (antepuesto a cada capa cifrada)

# Dirección Base32

B32_ENCRYPTED_DECODED_SIZE = 35  # bytes B32_ENCRYPTED_ENCODED_LEN = 56   # caracteres B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Clave pública del destino (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Secreto vacío

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 bytes

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Verifique frente a la implementación de referencia) alpha = [valor hexadecimal de 64 bytes]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [verificar contra los vectores de prueba del RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # De todos ceros ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [valor hexadecimal de 44 bytes]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bytes unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 caracteres base32].b32.i2p

# Verifique que la suma de verificación sea válida

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.