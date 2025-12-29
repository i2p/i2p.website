---
title: "Estructuras comunes"
description: "Tipos de datos compartidos y formatos de serialización utilizados en las especificaciones de I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

Este documento especifica las estructuras de datos fundamentales utilizadas en todos los protocolos de I2P, incluyendo [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) y otros. Estas estructuras comunes garantizan la interoperabilidad entre diferentes implementaciones de I2P y capas de protocolo.

### Cambios clave desde 0.9.58

- ElGamal y DSA-SHA1 en desuso para las identidades del router (usar X25519 + EdDSA)
- Compatibilidad con ML-KEM poscuántico en pruebas beta (opt-in [activación opcional] desde la 2.10.0)
- Opciones de registros de servicio estandarizadas ([Proposal 167](/proposals/167-service-records/), implementado en 0.9.66)
- Especificaciones de relleno compresible finalizadas ([Proposal 161](/es/proposals/161-ri-dest-padding/), implementado en 0.9.57)

---

## Especificaciones comunes de tipos

### Entero

**Descripción:** Representa un entero no negativo en orden de bytes de red (big-endian, endián grande).

**Contenido:** De 1 a 8 bytes que representan un entero sin signo.

**Uso:** Longitudes de campo, cantidades, identificadores de tipo y valores numéricos en todos los protocolos de I2P.

---

### Fecha

**Descripción:** Marca de tiempo que representa milisegundos desde la época Unix (1 de enero de 1970 00:00:00 GMT).

**Contenido:** Entero de 8 bytes (unsigned long)

**Valores especiales:** - `0` = Fecha indefinida o nula - Valor máximo: `0xFFFFFFFFFFFFFFFF` (año 584,942,417,355)

**Notas de implementación:** - Siempre en zona horaria UTC/GMT - Se requiere precisión de milisegundos - Se utiliza para la expiración del lease (período de validez en I2P), la publicación de RouterInfo y la validación de marcas de tiempo

---

### Cadena

**Descripción:** Cadena codificada en UTF-8 con prefijo de longitud.

**Formato:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Restricciones:** - Longitud máxima: 255 bytes (no caracteres - las secuencias UTF-8 de múltiples bytes cuentan como varios bytes) - La longitud puede ser cero (cadena vacía) - El terminador nulo NO está incluido - La cadena NO tiene terminación nula

**Importante:** Las secuencias UTF-8 pueden usar varios bytes por carácter. Una cadena de 100 caracteres podría exceder el límite de 255 bytes si utiliza caracteres multibyte.

---

## Estructuras de claves criptográficas

### Clave pública

**Descripción:** Clave pública para cifrado asimétrico. El tipo y la longitud de la clave dependen del contexto o se especifican en un Key Certificate (certificado de clave).

**Tipo predeterminado:** ElGamal (en desuso para las Identidades de Router a partir de la 0.9.58)

**Tipos admitidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Requisitos de implementación:**

1. **X25519 (Tipo 4) - Estándar actual:**
   - Se utiliza para el cifrado ECIES-X25519-AEAD-Ratchet
   - Obligatorio para las Identidades de router desde la versión 0.9.48
   - Codificación little-endian (a diferencia de otros tipos)
   - Véase [ECIES](/docs/specs/ecies/) y [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - Legado:**
   - Obsoleto para Router Identities desde la 0.9.58
   - Sigue siendo válido para Destinations (campo no utilizado desde 0.6/2005)
   - Utiliza primos constantes definidos en la [especificación de ElGamal](/docs/specs/cryptography/)
   - Se mantiene el soporte por compatibilidad con versiones anteriores

3. **MLKEM (poscuántico) - Beta:**
   - El enfoque híbrido combina ML-KEM con X25519
   - NO está habilitado de forma predeterminada en 2.10.0
   - Requiere activación manual mediante Hidden Service Manager (administrador de servicios ocultos)
   - Consulta [ECIES-HYBRID](/docs/specs/ecies/#hybrid) y [Proposal 169](/proposals/169-pq-crypto/)
   - Los códigos de tipo y las especificaciones están sujetos a cambios

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Clave privada

**Descripción:** Clave privada para descifrado asimétrico, correspondiente a los tipos PublicKey.

**Almacenamiento:** Tipo y longitud inferidos a partir del contexto o almacenados por separado en estructuras de datos/archivos de claves.

**Tipos compatibles:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Notas de seguridad:** - Las claves privadas DEBEN generarse utilizando generadores de números aleatorios criptográficamente seguros - Las claves privadas X25519 usan scalar clamping (restricción del escalar) según lo definido en la RFC 7748 - El material de clave DEBE borrarse de forma segura de la memoria cuando ya no sea necesario

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Clave de sesión

**Descripción:** Clave simétrica para el cifrado y descifrado con AES-256 en el tunnel (túnel) y el garlic encryption (cifrado garlic) de I2P.

**Contenido:** 32 bytes (256 bits)

**Uso:** - Cifrado de la capa de tunnel (AES-256/CBC con IV) - garlic encryption (cifrado por agregación de mensajes) - Cifrado de sesión de extremo a extremo

**Generación:** DEBE usar un generador de números aleatorios criptográficamente seguro.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Descripción:** Clave pública para la verificación de firmas. El tipo y la longitud se especifican en el Certificado de clave del Destino o se infieren del contexto.

**Tipo predeterminado:** DSA_SHA1 (en desuso desde 0.9.58)

**Tipos admitidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Requisitos de implementación:**

1. **EdDSA_SHA512_Ed25519 (Tipo 7) - Estándar actual:**
   - Predeterminado para todas las nuevas Router Identities y Destinations desde finales de 2015
   - Usa la curva Ed25519 con hash SHA-512
   - Claves públicas de 32 bytes, firmas de 64 bytes
   - Codificación little-endian (orden de bytes con el menos significativo primero; a diferencia de la mayoría de los otros tipos)
   - Alto rendimiento y seguridad

2. **RedDSA_SHA512_Ed25519 (Type 11) - Especializado:**
   - Se usa SOLO para leasesets cifrados y blinding (cegamiento)
   - Nunca se usa para Identidades de router ni para Destinos estándar
   - Diferencias clave con respecto a EdDSA:
     - Claves privadas mediante reducción modular (no clamping, recorte de bits)
     - Las firmas incluyen 80 bytes de datos aleatorios
     - Usa las claves públicas directamente (no hashes de las claves privadas)
   - Consulte [Especificación de Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Tipo 0) - Heredado:**
   - Obsoleto para Identidades de router a partir de la 0.9.58
   - Desaconsejado para nuevos Destinos
   - DSA de 1024 bits con SHA-1 (debilidades conocidas)
   - Se mantiene el soporte únicamente por compatibilidad

4. **Claves de múltiples elementos:**
   - Cuando se compone de dos elementos (p. ej., puntos ECDSA X,Y)
   - Cada elemento se rellena hasta length/2 con ceros a la izquierda
   - Ejemplo: clave ECDSA de 64 bytes = 32 bytes X + 32 bytes Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey (clave privada de firma)

**Descripción:** Clave privada para crear firmas, correspondiente a los tipos SigningPublicKey.

**Almacenamiento:** Tipo y longitud especificados en el momento de la creación.

**Tipos admitidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Requisitos de seguridad:** - Generar utilizando una fuente de aleatoriedad criptográficamente segura - Proteger con controles de acceso adecuados - Borrar de la memoria de forma segura al finalizar - Para EdDSA: semilla de 32 bytes con hash SHA-512, los primeros 32 bytes se convierten en el escalar (clamped, acotado) - Para RedDSA: generación de claves diferente (reducción modular en lugar de clamping)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Firma

**Descripción:** Firma criptográfica sobre los datos, usando el algoritmo de firma correspondiente al tipo SigningPrivateKey.

**Tipo y longitud:** Inferidos a partir del tipo de clave utilizado para la firma.

**Tipos admitidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Notas de formato:** - Las firmas de múltiples elementos (p. ej., valores R,S de ECDSA) se rellenan hasta length/2 por elemento con ceros a la izquierda - EdDSA y RedDSA usan codificación little-endian (orden de bytes de menor a mayor) - Todos los demás tipos usan codificación big-endian (orden de bytes de mayor a menor)

**Verificación:** - Use el SigningPublicKey correspondiente - Siga las especificaciones del algoritmo de firma para el tipo de clave - Compruebe que la longitud de la firma coincide con la longitud esperada para el tipo de clave

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Hash (resumen criptográfico)

**Descripción:** hash SHA-256 de datos, utilizado en todo I2P para la verificación de integridad e identificación.

**Contenido:** 32 bytes (256 bits)

**Usos:** - hashes de la Identidad del Router (claves de la base de datos de red) - hashes de destino (claves de la base de datos de red) - identificación de la puerta de enlace del Tunnel en Leases - verificación de la integridad de los datos - generación del ID del Tunnel

**Algoritmo:** SHA-256 según se define en FIPS 180-4

**JavaDoc (documentación de la API de Java):** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Etiqueta de sesión

**Descripción:** Número aleatorio utilizado para la identificación de la sesión y el cifrado basado en etiquetas.

**Importante:** El tamaño de la etiqueta de sesión varía según el tipo de cifrado: - **ElGamal/AES+SessionTag:** 32 bytes (heredado) - **ECIES-X25519:** 8 bytes (estándar actual)

**Estándar actual (ECIES):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Consulte [ECIES](/docs/specs/ecies/) y [ECIES-ROUTERS](/docs/specs/ecies/#routers) para obtener especificaciones detalladas.

**Heredado (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Generación:** DEBE usar un generador de números aleatorios criptográficamente seguro.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Descripción:** Identificador único de la posición que ocupa un router dentro de un tunnel. Cada salto en un tunnel tiene su propio TunnelId (identificador de túnel).

**Formato:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Uso:** - Identifica las conexiones de tunnel entrantes/salientes en cada router - TunnelId diferente en cada salto de la cadena de tunnel - Se utiliza en estructuras Lease (estructura de metadatos de I2P que anuncia tunnel de entrada y su vigencia) para identificar tunnel de puerta de enlace

**Valores especiales:** - `0` = Reservado para usos especiales del protocolo (evitar en operación normal) - Los TunnelIds (identificadores de tunnel) solo tienen significado local para cada router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Especificaciones de certificados

### Certificado

**Descripción:** Contenedor para recibos, prueba de trabajo o metadatos criptográficos utilizados en todo I2P.

**Formato:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Tamaño total:** mínimo 3 bytes (NULL certificate, certificado nulo), hasta 65538 bytes como máximo

### Tipos de certificados

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Certificado de clave (Tipo 5)

**Introducción:** Versión 0.9.12 (diciembre de 2013)

**Propósito:** Especifica tipos de clave no predeterminados y almacena datos de clave adicionales más allá de la estructura estándar KeysAndCert de 384 bytes.

**Estructura de la carga útil:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Notas críticas de implementación:**

1. **Orden de tipos de clave:**
   - **ADVERTENCIA:** el tipo de clave de firma va ANTES que el tipo de clave criptográfica
   - Esto es contraintuitivo, pero se mantiene por compatibilidad
   - Orden: SPKtype, CPKtype (no CPKtype, SPKtype)

2. **Estructura de los datos de clave en KeysAndCert:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Cálculo de datos de clave excedentes:**
   - Si Crypto Key > 256 bytes: Excess = (Crypto Length - 256)
   - Si Signing Key > 128 bytes: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Ejemplos (clave criptográfica ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Requisitos de identidad del router:** - Certificado NULL utilizado hasta la versión 0.9.15 - Certificado de clave requerido para tipos de clave no predeterminados desde la 0.9.16 - Claves de cifrado X25519 compatibles desde la 0.9.48

**Requisitos del destino:** - certificado NULL o certificado de clave (según sea necesario) - Se requiere un certificado de clave para los tipos de clave de firma no predeterminados desde la 0.9.12 - El campo de clave pública criptográfica no se usa desde la 0.6 (2005), pero debe seguir estando presente

**Advertencias importantes:**

1. **Certificado NULL vs KEY:**
   - Un KEY certificate (certificado de tipo KEY) con tipos (0,0) que especifican ElGamal+DSA_SHA1 está permitido pero se desaconseja
   - Use siempre NULL certificate (certificado de tipo NULL) para ElGamal+DSA_SHA1 (representación canónica)
   - Un KEY certificate con (0,0) es 4 bytes más largo y puede causar problemas de compatibilidad
   - Algunas implementaciones pueden no manejar correctamente los KEY certificates con (0,0)

2. **Validación de datos excedentes:**
   - Las implementaciones DEBEN verificar que la longitud del certificado coincida con la longitud esperada para los tipos de clave
   - Rechazar certificados con datos excedentes que no correspondan a los tipos de clave
   - Prohibir datos basura al final de una estructura de certificado válida

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Mapeo

**Descripción:** Colección de propiedades clave-valor usada para configuración y metadatos.

**Formato:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Límites de tamaño:** - Longitud de la clave: 0-255 bytes (+ 1 byte de longitud) - Longitud del valor: 0-255 bytes (+ 1 byte de longitud) - Tamaño total del mapeo: 0-65535 bytes (+ 2 bytes del campo de tamaño) - Tamaño máximo de la estructura: 65537 bytes

**Requisito crítico de ordenación:**

Cuando los mapeos aparecen en **estructuras firmadas** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig), las entradas DEBEN ordenarse por clave para garantizar la invariancia de la firma:

1. **Método de ordenación:** Ordenación lexicográfica usando los valores de los puntos de código Unicode (equivalente a Java String.compareTo())
2. **Sensibilidad a mayúsculas y minúsculas:** Las claves y los valores generalmente distinguen mayúsculas y minúsculas (dependiente de la aplicación)
3. **Claves duplicadas:** NO se permiten en estructuras firmadas (provocan un fallo en la verificación de la firma)
4. **Codificación de caracteres:** Comparación a nivel de bytes en UTF-8

**Por qué importa la ordenación:** - Las firmas se calculan sobre la representación en bytes - Diferentes órdenes de claves producen diferentes firmas - Los mapeos no firmados no requieren ordenación, pero deberían seguir la misma convención

**Notas de implementación:**

1. **Redundancia de codificación:**
   - Están presentes tanto los delimitadores `=` y `;` como los bytes de longitud de la cadena
   - Esto es ineficiente, pero se mantiene por compatibilidad
   - Los bytes de longitud tienen prioridad; los delimitadores son obligatorios pero redundantes

2. **Compatibilidad de caracteres:**
   - A pesar de la documentación, `=` y `;` SÍ se admiten dentro de las cadenas (los bytes de longitud se encargan de esto)
   - La codificación UTF-8 admite todo el conjunto de caracteres Unicode
   - **Advertencia:** I2CP usa UTF-8, pero I2NP históricamente no manejaba UTF-8 correctamente
   - Usa ASCII para las asignaciones de I2NP cuando sea posible para lograr la máxima compatibilidad

3. **Contextos especiales:**
   - **RouterInfo/RouterAddress:** DEBE estar ordenado, sin duplicados
   - **I2CP SessionConfig (configuración de sesión):** DEBE estar ordenado, sin duplicados  
   - **Mapeos de aplicaciones:** Se recomienda ordenar, pero no siempre es obligatorio

**Ejemplo (opciones de RouterInfo (información del router de I2P)):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Especificación de estructura común

### Claves y Certificado

**Descripción:** Estructura fundamental que combina la clave de cifrado, la clave de firma y el certificado. Se utiliza como RouterIdentity (identidad del router) y como Destination (destino).

**Estructura:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Alineación de claves:** - **Clave pública criptográfica:** Alineada al inicio (byte 0) - **Relleno:** En el medio (si es necesario) - **Clave pública de firma:** Alineada al final (del byte 256 al byte 383) - **Certificado:** Comienza en el byte 384

**Cálculo del tamaño:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Directrices para la generación de relleno ([Propuesta 161](/es/proposals/161-ri-dest-padding/))

**Versión de implementación:** 0.9.57 (enero de 2023, lanzamiento 2.1.0)

**Antecedentes:** - Para claves no ElGamal+DSA, el relleno está presente en la estructura fija de 384 bytes - Para los Destinos, el campo de clave pública de 256 bytes no se utiliza desde la 0.6 (2005) - El relleno debe generarse de manera que sea comprimible y, a la vez, siga siendo seguro

**Requisitos:**

1. **Mínimo de datos aleatorios:**
   - Utilice al menos 32 bytes de datos aleatorios criptográficamente seguros
   - Esto proporciona suficiente entropía para la seguridad

2. **Estrategia de compresión:**
   - Repetir los 32 bytes a lo largo de todo el campo de relleno/clave pública
   - Protocolos como I2NP Database Store, Streaming SYN, SSU2 handshake (intercambio inicial) usan compresión
   - Ahorros significativos de ancho de banda sin comprometer la seguridad

3. **Ejemplos:**

**Identidad del Router (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destino (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Por qué esto funciona:**
   - El hash SHA-256 de la estructura completa sigue incluyendo toda la entropía
   - La distribución DHT (tabla hash distribuida) de la base de datos de red depende únicamente del hash
   - La clave de firma (32 bytes EdDSA/X25519) proporciona 256 bits de entropía
   - 32 bytes adicionales de datos aleatorios repetidos = 512 bits de entropía total
   - Más que suficiente para la seguridad criptográfica

5. **Notas de implementación:**
   - DEBE almacenar y transmitir la estructura completa de 387+ bytes
   - Hash SHA-256 calculado sobre la estructura completa sin comprimir
   - Compresión aplicada en la capa de protocolo (I2NP, Streaming, SSU2)
   - Retrocompatible con todas las versiones desde la 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (identidad del router)

**Descripción:** Identifica de forma única un router en la red I2P. Tiene una estructura idéntica a KeysAndCert.

**Formato:** Consulte la estructura KeysAndCert más arriba

**Requisitos actuales (a partir de la versión 0.9.58):**

1. **Tipos de claves obligatorios:**
   - **Cifrado:** X25519 (tipo 4, 32 bytes)
   - **Firma:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes)
   - **Certificado:** Key Certificate (certificado de clave, tipo 5)

2. **Tipos de claves en desuso:**
   - ElGamal (tipo 0) en desuso para las Identidades de Router a partir de la 0.9.58
   - DSA_SHA1 (tipo 0) en desuso para las Identidades de Router a partir de la 0.9.58
   - Estos NO deben usarse para routers nuevos

3. **Tamaño típico:**
   - X25519 + EdDSA con certificado de clave = 391 bytes
   - 32 bytes de clave pública X25519
   - 320 bytes de relleno (compresible según [Propuesta 161](/es/proposals/161-ri-dest-padding/))
   - 32 bytes de clave pública EdDSA
   - 7 bytes de certificado (encabezado de 3 bytes + tipos de clave de 4 bytes)

**Evolución histórica:** - Pre-0.9.16: Siempre NULL certificate (certificado nulo) (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Se añadió soporte para Key Certificate (certificado de clave) - 0.9.48+: Se añadió soporte para claves de cifrado X25519 - 0.9.58+: ElGamal y DSA_SHA1 marcados como obsoletos

**Clave de la base de datos de red:** - RouterInfo (información del router) indexado por el hash SHA-256 de la RouterIdentity (identidad del router) completa - Hash calculado sobre la estructura completa de 391+ bytes (incluyendo el relleno)

**Véase también:** - Directrices para la generación de relleno ([Proposal 161](/es/proposals/161-ri-dest-padding/)) - Especificación del certificado de clave más arriba

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Destino

**Descripción:** Identificador de extremo para la entrega segura de mensajes. Estructuralmente idéntico a KeysAndCert, pero con una semántica de uso diferente.

**Formato:** Consulte la estructura KeysAndCert anterior

**Diferencia crítica con respecto a RouterIdentity:** - **El campo de clave pública NO SE USA y puede contener datos aleatorios** - Este campo no se usa desde la versión 0.6 (2005) - Originalmente era para el cifrado I2CP-to-I2CP antiguo (deshabilitado) - Actualmente solo se usa como IV (vector de inicialización) para el cifrado de LeaseSet en desuso

**Recomendaciones actuales:**

1. **Clave de firma:**
   - **Recomendada:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes)
   - Alternativa: tipos ECDSA para compatibilidad con versiones anteriores
   - Evitar: DSA_SHA1 (obsoleto, desaconsejado)

2. **Clave de cifrado:**
   - El campo no se utiliza, pero debe estar presente
   - **Recomendado:** Rellenar con datos aleatorios según [Proposal 161](/es/proposals/161-ri-dest-padding/) (compresible)
   - Tamaño: Siempre 256 bytes (ranura de ElGamal, aunque no se use para ElGamal)

3. **Certificado:**
   - Certificado NULL para ElGamal + DSA_SHA1 (solo para compatibilidad con versiones anteriores)
   - Certificado de clave para todos los demás tipos de claves de firma

**Destino moderno típico:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Clave de cifrado efectiva:** - La clave de cifrado del Destination (Destino) está en el **LeaseSet**, no en el Destination - LeaseSet contiene las claves públicas de cifrado actuales - Consulta la especificación de LeaseSet2 para la gestión de la clave de cifrado

**Clave de la base de datos de red:** - LeaseSet indexado por el hash SHA-256 del Destino completo - Hash calculado sobre la estructura completa de 387+ bytes

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Estructuras de la base de datos de la red

### Concesión

**Descripción:** Autoriza que un tunnel específico reciba mensajes para un Destino. Parte del formato original de LeaseSet (tipo 1).

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Tamaño total:** 44 bytes

**Uso:** - Se utiliza únicamente en el LeaseSet original (tipo 1, obsoleto) - Para LeaseSet2 y variantes posteriores, utilice Lease2 en su lugar

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Tipo 1)

**Descripción:** Formato original de LeaseSet. Contiene tunnels autorizados y claves para un Destination (destino de I2P). Almacenado en la base de datos de la red. **Estado: Obsoleto** (usa LeaseSet2 en su lugar).

**Estructura:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Almacenamiento de base de datos:** - **Tipo de base de datos:** 1 - **Clave:** hash SHA-256 del Destino - **Valor:** estructura completa de LeaseSet

**Notas importantes:**

1. **Clave pública del Destino no utilizada:**
   - El campo de clave pública de cifrado en el Destino no se utiliza
   - La clave de cifrado en el LeaseSet es la clave de cifrado efectiva

2. **Claves temporales:**
   - `encryption_key` es temporal (se regenera al iniciar el router)
   - `signing_key` es temporal (se regenera al iniciar el router)
   - Ninguna de las dos claves persiste entre reinicios

3. **Revocación (no implementada):**
   - `signing_key` estaba previsto para la revocación de LeaseSet
   - El mecanismo de revocación nunca se implementó
   - Un LeaseSet con cero leases (referencias de tunnel) estaba previsto para la revocación, pero no se utiliza

4. **Versionado/Marca de tiempo:**
   - LeaseSet no tiene un campo de marca de tiempo `published` explícito
   - La versión es el vencimiento más temprano de todos los leases (registros de vigencia de los túneles)
   - El nuevo LeaseSet debe tener un vencimiento de lease más temprano para ser aceptado

5. **Publicación de la expiración de Lease (periodo de validez de un túnel en I2P):**
   - Pre-0.9.7: Todas las leases se publicaban con la misma expiración (la más temprana)
   - 0.9.7+: Se publican las expiraciones reales de las leases individuales
   - Esto es un detalle de implementación, no forma parte de la especificación

6. **Cero Leases:**
   - LeaseSet con cero Leases es técnicamente válido
   - Previsto para revocación (no implementado)
   - No se usa en la práctica
   - Las variantes de LeaseSet2 requieren al menos un Lease (entrada que describe un tunnel entrante y su expiración)

**Obsolescencia:** LeaseSet tipo 1 está obsoleto. Las nuevas implementaciones deberían usar **LeaseSet2 (tipo 3)**, que proporciona: - Campo de marca de tiempo de publicación (mejor control de versiones) - Compatibilidad con varias claves de cifrado - Capacidad de firma sin conexión - Caducidades de lease (registro temporal de túnel) de 4 bytes (frente a 8 bytes) - Opciones más flexibles

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Variantes de LeaseSet

### Lease2 (versión 2 de la entrada con expiración que autoriza el acceso a un tunnel)

**Descripción:** Formato de lease mejorado con expiración de 4 bytes. Se utiliza en LeaseSet2 (tipo 3) y MetaLeaseSet (tipo 7).

**Introducción:** Versión 0.9.38 (véase [Propuesta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Tamaño total:** 40 bytes (4 bytes menos que el Lease original)

**Comparación con el Lease (registro que especifica un tunnel y su expiración en I2P) original:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### OfflineSignature (firma fuera de línea)

**Descripción:** Estructura opcional para claves efímeras prefirmadas, que permite la publicación del LeaseSet sin acceso en línea a la clave privada de firma de Destination (destino en I2P).

**Introducción:** Versión 0.9.38 (véase [Propuesta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Propósito:** - Permite la generación de LeaseSet sin conexión - Protege la clave maestra de la Destination (Destino) contra la exposición en línea - La clave temporal puede revocarse publicando un nuevo LeaseSet sin la firma sin conexión

**Escenarios de uso:**

1. **Destinos de alta seguridad:**
   - Clave maestra de firma almacenada fuera de línea (HSM, almacenamiento en frío)
   - Claves efímeras generadas fuera de línea por períodos de tiempo limitados
   - Una clave efímera comprometida no expone la clave maestra

2. **Publicación de Encrypted LeaseSet:**
   - EncryptedLeaseSet puede incluir firma fuera de línea
   - Clave pública cegada + firma fuera de línea proporcionan seguridad adicional

**Consideraciones de seguridad:**

1. **Gestión de caducidad:**
   - Establecer una caducidad razonable (de días a semanas, no años)
   - Generar nuevas claves efímeras antes de la caducidad
   - Caducidad más corta = mejor seguridad, más mantenimiento

2. **Generación de claves:**
   - Generar claves efímeras sin conexión en un entorno seguro
   - Firmar con la clave maestra sin conexión
   - Transferir únicamente la clave efímera firmada + la firma al router en línea

3. **Revocación:**
   - Publicar un nuevo LeaseSet sin firma fuera de línea para revocar implícitamente
   - O publicar un nuevo LeaseSet con una clave efímera diferente

**Verificación de la firma:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Notas de implementación:** - El tamaño total varía según el tipo de firma y el tipo de clave de firma del Destino - Tamaño mínimo: 4 + 2 + 32 (clave EdDSA) + 64 (firma EdDSA) = 102 bytes - Tamaño máximo práctico: ~600 bytes (clave temporal RSA-4096 + firma RSA-4096)

**Compatible con:** - LeaseSet2 (tipo 3) - EncryptedLeaseSet (tipo 5) - MetaLeaseSet (tipo 7)

**Véase también:** [Propuesta 123](/proposals/123-new-netdb-entries/) para el protocolo de firma sin conexión detallado.

---

### LeaseSet2Header

**Descripción:** Estructura de encabezado común para LeaseSet2 (tipo 3) y MetaLeaseSet (tipo 7).

**Introducción:** Versión 0.9.38 (ver [Propuesta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Tamaño total mínimo:** 395 bytes (sin firma fuera de línea)

**Definiciones de banderas (orden de bits: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Detalles de la bandera:**

**Bit 0 - Claves fuera de línea:** - `0`: Sin firma fuera de línea, use la clave de firma de la Destination (identidad/destino en I2P) para verificar la firma del LeaseSet - `1`: La estructura OfflineSignature sigue al campo de indicadores

**Bit 1 - No publicado:** - `0`: LeaseSet publicado estándar, debe propagarse a los floodfills - `1`: LeaseSet no publicado (solo del lado del cliente)   - NO debe propagarse, publicarse ni enviarse en respuesta a consultas   - Si expira, NO consultar netdb para reemplazo (a menos que el bit 2 también esté establecido)   - Usado para tunnels locales o pruebas

**Bit 2 - Blinded (cegado) (desde 0.9.42):** - `0`: LeaseSet estándar - `1`: Este LeaseSet no cifrado se publicará como blinded y cifrado   - La versión publicada será EncryptedLeaseSet (tipo 5)   - Si caduca, consulta la **ubicación blinded** en netdb para su reemplazo   - También se debe establecer el bit 1 en 1 (unpublished + blinded)   - Se usa para servicios ocultos cifrados

**Límites de expiración:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Requisitos de la marca de tiempo publicada:**

LeaseSet (tipo 1) no tenía un campo published, lo que obligaba a buscar el vencimiento más temprano del lease (concesión de túnel) para el versionado. LeaseSet2 añade una marca de tiempo `published` explícita con resolución de 1 segundo.

**Nota crítica de implementación:** - Routers DEBEN aplicar limitación de tasa a la publicación de LeaseSet a una frecuencia **mucho más baja que una vez por segundo** por Destination (destino en I2P) - Si se publica más rápido, asegúrense de que cada nuevo LeaseSet tenga el campo `published` al menos 1 segundo posterior - Floodfills rechazarán el LeaseSet si el campo `published` no es más reciente que la versión actual - Intervalo mínimo recomendado: 10-60 segundos entre publicaciones

**Ejemplos de cálculo:**

**LeaseSet2 (máximo de 11 minutos):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (máximo de 18,2 horas):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Versionado:** - Se considera "más reciente" un LeaseSet si la marca de tiempo `published` es mayor - Los Floodfills almacenan y propagan únicamente la versión más reciente - Presta atención cuando el Lease (arrendamiento de túnel) más antiguo coincide con el Lease más antiguo del LeaseSet anterior

---

### LeaseSet2 (Tipo 3)

**Descripción:** Formato moderno de LeaseSet con múltiples claves de cifrado, firmas fuera de línea y registros de servicio. Estándar actual para servicios ocultos de I2P.

**Introducción:** Versión 0.9.38 (véase [Propuesta 123](/proposals/123-new-netdb-entries/))

**Estructura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Almacenamiento de la base de datos:** - **Tipo de base de datos:** 3 - **Clave:** hash SHA-256 del Destino - **Valor:** Estructura completa de LeaseSet2

**Cálculo de la firma:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Orden de preferencia de claves de cifrado

**Para LeaseSet Publicado (Servidor):** - Claves listadas en orden de preferencia del servidor (las más preferidas primero) - Los clientes que admitan múltiples tipos DEBERÍAN respetar la preferencia del servidor - Seleccione el primer tipo compatible de la lista - En general, los tipos de clave con numeración más alta (más nuevos) son más seguros/eficientes - Orden recomendado: Enumere las claves en orden inverso por código de tipo (las más nuevas primero)

**Ejemplo de preferencia del servidor:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Para LeaseSet (cliente) no publicado:** - El orden de las claves en la práctica no importa (rara vez se intentan conexiones a clientes) - Sigue la misma convención para mantener la coherencia

**Selección de claves del cliente:** - Respetar la preferencia del servidor (seleccionar el primer tipo admitido) - O usar la preferencia definida por la implementación - O determinar una preferencia combinada en función de las capacidades de ambos

### Asignación de opciones

**Requisitos:** - Las opciones DEBEN estar ordenadas por clave (lexicográfico, orden de bytes UTF-8) - La ordenación garantiza la invariancia de la firma - NO se permiten claves duplicadas

**Formato estándar ([Propuesta 167](/proposals/167-service-records/)):**

A partir de la API 0.9.66 (junio de 2025, versión 2.9.0), las opciones de los registros de servicio siguen un formato estandarizado. Consulta [Propuesta 167](/proposals/167-service-records/) para la especificación completa.

**Formato de la opción del registro de servicio:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Ejemplos de registros de servicio:**

**1. Servidor SMTP autorreferente:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Servidor SMTP externo único:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Varios servidores SMTP (balanceo de carga):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Servicio HTTP con opciones de la aplicación:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Recomendaciones de TTL:** - Mínimo: 86400 segundos (1 día) - Un TTL más largo reduce la carga de consultas de netdb - Equilibrio entre la reducción de consultas y la propagación de actualizaciones del servicio - Para servicios estables: 604800 (7 días) o más

**Notas de implementación:**

1. **Claves de cifrado (a partir de la versión 0.9.44):**
   - ElGamal (tipo 0, 256 bytes): Compatibilidad con versiones anteriores
   - X25519 (tipo 4, 32 bytes): Estándar actual
   - Variantes de MLKEM: Poscuánticas (beta, no finalizadas)

2. **Validación de longitud de clave:**
   - Floodfills (nodos floodfill de I2P) y clientes DEBEN poder analizar tipos de clave desconocidos
   - Utilice el campo keylen para omitir claves desconocidas
   - No falle el análisis si el tipo de clave es desconocido

3. **Marca de tiempo de publicación:**
   - Consulte las notas de LeaseSet2Header sobre limitación de tasa
   - Incremento mínimo de 1 segundo entre publicaciones
   - Recomendado: 10-60 segundos entre publicaciones

4. **Migración del tipo de cifrado:**
   - El uso de múltiples claves permite una migración gradual
   - Enumera tanto las claves antiguas como las nuevas durante el período de transición
   - Elimina la clave antigua tras un período suficiente de actualización de clientes

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (arrendamiento meta)

**Descripción:** Estructura de Lease (registro de túnel con vencimiento) para MetaLeaseSet que puede referenciar otros LeaseSets en lugar de tunnels. Se utiliza para balanceo de carga y redundancia.

**Introducción:** Versión 0.9.38, trabajo programado para la 0.9.40 (véase [Propuesta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Tamaño total:** 40 bytes

**Tipo de entrada (bits de bandera 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Escenarios de uso:**

1. **Balanceo de carga:**
   - MetaLeaseSet con múltiples entradas de MetaLease
   - Cada entrada apunta a un LeaseSet2 diferente
   - Los clientes seleccionan en función del campo de coste

2. **Redundancia:**
   - Varias entradas que apuntan a LeaseSets de respaldo
   - Alternativa si el LeaseSet principal no está disponible

3. **Migración de servicio:**
   - MetaLeaseSet apunta al nuevo LeaseSet
   - Permite una transición fluida entre Destinos

**Uso del campo de coste:** - Menor coste = mayor prioridad - Coste 0 = prioridad más alta - Coste 255 = prioridad más baja - Los clientes DEBERÍAN preferir entradas de menor coste - Las entradas con el mismo coste pueden balancearse de forma aleatoria

**Comparación con Lease2 (segunda versión de Lease en I2P):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Tipo 7)

**Descripción:** Variante de LeaseSet que contiene entradas MetaLease (entradas «meta»), proporcionando indirección hacia otros LeaseSets. Se usa para balanceo de carga, redundancia y migración de servicios.

**Introducción:** Definido en 0.9.38, funcionamiento previsto en 0.9.40 (ver [Propuesta 123](/proposals/123-new-netdb-entries/))

**Estado:** Especificación completa. Debe verificarse el estado del despliegue en producción con las versiones actuales de I2P.

**Estructura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Almacenamiento de base de datos:** - **Tipo de base de datos:** 7 - **Clave:** hash SHA-256 del Destino - **Valor:** estructura MetaLeaseSet completa

**Cálculo de la firma:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Escenarios de uso:**

**1. Balanceo de carga:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Conmutación por error:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Migración del servicio:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Arquitectura de múltiples capas:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Lista de revocación:**

La lista de revocación permite a MetaLeaseSet revocar explícitamente los LeaseSets publicados previamente:

- **Propósito:** Marcar que determinadas Destinations (destinos de I2P) ya no son válidas
- **Contenido:** Hashes SHA-256 de estructuras de Destination revocadas
- **Uso:** Los clientes NO DEBEN usar LeaseSets cuyo hash de Destination aparezca en la lista de revocación
- **Valor típico:** Vacío (numr=0) en la mayoría de los despliegues

**Ejemplo de revocación:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Gestión de caducidad:**

MetaLeaseSet utiliza LeaseSet2Header con un expires máximo de 65535 segundos (~18,2 horas):

- Mucho más largo que LeaseSet2 (máx. ~11 minutos)
- Adecuado para una indirección relativamente estática
- Los LeaseSets referenciados pueden tener un vencimiento más corto
- Los clientes deben comprobar el vencimiento tanto del MetaLeaseSet como de los LeaseSets referenciados

**Asignación de opciones:**

- Utiliza el mismo formato que las opciones de LeaseSet2
- Puede incluir registros de servicio ([Proposal 167](/proposals/167-service-records/))
- DEBE estar ordenado por clave
- Los registros de servicio normalmente describen el servicio final, no la estructura de indirección

**Notas de implementación del cliente:**

1. **Proceso de resolución:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Caché:**
   - Almacenar en caché tanto el MetaLeaseSet (estructura que agrupa varios LeaseSets) como los LeaseSets referenciados
   - Comprobar la caducidad de ambos niveles
   - Supervisar la publicación de un MetaLeaseSet actualizado

3. **Conmutación por error:**
   - Si la entrada preferida falla, prueba con la siguiente de menor costo
   - Considera marcar las entradas fallidas como no disponibles temporalmente
   - Vuelve a comprobar periódicamente por si se recuperan

**Estado de implementación:**

[Propuesta 123](/proposals/123-new-netdb-entries/) indica que algunas partes siguen "en desarrollo". Los implementadores deberían: - Verificar la aptitud para producción en la versión objetivo de I2P - Probar la compatibilidad con MetaLeaseSet (tipo de leaseSet de I2P) antes del despliegue - Comprobar si hay especificaciones actualizadas en versiones más recientes de I2P

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (LeaseSet cifrado) (Tipo 5)

**Descripción:** LeaseSet cifrado y cegado para mayor privacidad. Solo la clave pública cegada y los metadatos son visibles; los leases (entradas de túneles entrantes) reales y las claves de cifrado están cifrados.

**Introducción:** Definido en 0.9.38, operativo desde 0.9.39 (véase [Propuesta 123](/proposals/123-new-netdb-entries/))

**Estructura:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Almacenamiento de base de datos:** - **Tipo de base de datos:** 5 - **Clave:** hash SHA-256 del **Destination cegado** (identificador de destino en I2P) (no del Destination original) - **Valor:** estructura EncryptedLeaseSet completa

**Diferencias clave con respecto a LeaseSet2:**

1. **NO utiliza la estructura LeaseSet2Header** (tiene campos similares pero un formato diferente)
2. **Clave pública cegada** en lugar de Destination (identificador de destino en I2P) completa
3. **Carga útil cifrada** en lugar de leases y claves en texto claro
4. **La clave de base de datos es el hash de la Destination cegada**, no de la Destination original

**Cálculo de la firma:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Requisito del tipo de firma:**

**DEBE usar RedDSA_SHA512_Ed25519 (tipo 11):** - claves públicas cegadas de 32 bytes - firmas de 64 bytes - Necesario para las propiedades de seguridad del cegado - Ver [especificación de Red25519](//docs/specs/red25519-signature-scheme/

**Principales diferencias con EdDSA:** - Claves privadas mediante reducción modular (no clamping (ajuste de bits)) - Las firmas incluyen 80 bytes de datos aleatorios - Usa claves públicas directamente (no hashes) - Permite una operación de blinding (enmascaramiento criptográfico) segura

**Cegado y cifrado:**

Consulte la [Especificación de EncryptedLeaseSet](/docs/specs/encryptedleaseset/) (LeaseSet cifrado) para obtener detalles completos:

**1. Cegado de clave:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Ubicación de la base de datos:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Capas de cifrado (tres capas):**

**Capa 1 - Capa de autenticación (Acceso de cliente):** - Cifrado: cifrado de flujo ChaCha20 - Derivación de claves: HKDF con secretos por cliente - Los clientes autenticados pueden descifrar la capa externa

**Capa 2 - Capa de cifrado:** - Cifrado: ChaCha20 - Clave: Derivada de DH (Diffie-Hellman) entre cliente y servidor - Contiene el LeaseSet2 o MetaLeaseSet propiamente dicho

**Capa 3 - LeaseSet interno:** - LeaseSet2 completo o MetaLeaseSet - Incluye todos los tunnels, claves de cifrado, opciones - Solo accesible tras un descifrado exitoso

**Derivación de la clave de cifrado:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Proceso de descubrimiento:**

**Para clientes autorizados:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Para clientes no autorizados:** - No pueden descifrar incluso si encuentran el EncryptedLeaseSet - No pueden determinar la Destination (destino en I2P) original a partir de la versión cegada - No pueden vincular EncryptedLeaseSets entre diferentes periodos de cegado (rotación diaria)

**Tiempos de expiración:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Marca de tiempo de publicación:**

Los mismos requisitos que LeaseSet2Header (encabezado de LeaseSet2):
- Debe incrementarse en al menos 1 segundo entre publicaciones
- Los Floodfills (routers floodfill) rechazan si no es más reciente que la versión actual
- Recomendado: 10-60 segundos entre publicaciones

**Firmas sin conexión con LeaseSets cifrados:**

Consideraciones especiales al usar firmas fuera de línea: - La clave pública cegada rota diariamente - La firma fuera de línea debe regenerarse diariamente con la nueva clave cegada - O use la firma fuera de línea en el LeaseSet interno, no en el EncryptedLeaseSet externo - Consulte las notas de [Propuesta 123](/proposals/123-new-netdb-entries/)

**Notas de implementación:**

1. **Autorización de clientes:**
   - Se pueden autorizar varios clientes con claves diferentes
   - Cada cliente autorizado tiene credenciales de descifrado únicas
   - Revoque el acceso de un cliente cambiando las claves de autorización

2. **Rotación diaria de claves:**
   - Las claves cegadas cambian a medianoche UTC
   - Los clientes deben recalcular diariamente la Destination cegada (identificador del servicio en I2P)
   - Los EncryptedLeaseSets antiguos dejan de ser descubribles tras la rotación

3. **Propiedades de privacidad:**
   - Los Floodfills no pueden determinar la Destination (destino en I2P) original
   - Los clientes no autorizados no pueden acceder al servicio
   - Los distintos períodos de blinding (cegamiento criptográfico) no pueden vincularse
   - No hay metadatos en claro más allá de los tiempos de expiración

4. **Rendimiento:**
   - Los clientes deben realizar un cálculo diario de cegamiento
   - El cifrado de tres capas añade sobrecarga computacional
   - Considere almacenar en caché el LeaseSet interno descifrado

**Consideraciones de seguridad:**

1. **Gestión de claves de autorización:**
   - Distribuir de forma segura las credenciales de autorización de los clientes
   - Usar credenciales únicas por cliente para una revocación granular
   - Rotar las claves de autorización periódicamente

2. **Sincronización del reloj:**
   - El blinding diario (cegamiento) depende de fechas UTC sincronizadas
   - El desfase del reloj puede causar fallos de búsqueda
   - Considere admitir el blinding del día anterior/siguiente para mayor tolerancia

3. **Filtración de metadatos:**
   - Los campos Published y expires están en texto sin cifrar
   - El análisis de patrones podría revelar características del servicio
   - Aleatoriza los intervalos de publicación si es motivo de preocupación

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Estructuras del Router

### RouterAddress (dirección del router)

**Descripción:** Define la información de conexión para un router mediante un protocolo de transporte específico.

**Formato:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**CRÍTICO - Campo de expiración:**

⚠️ **El campo de expiración DEBE establecerse a cero en todos sus bytes (8 bytes en cero).**

- **Motivo:** Desde la versión 0.9.3, una expiración distinta de cero provoca un fallo en la verificación de la firma
- **Historial:** La expiración originalmente no se usaba, siempre era null
- **Estado actual:** El campo volvió a reconocerse a partir de la versión 0.9.12, pero debe esperar a una actualización de la red
- **Implementación:** Siempre se establece en 0x0000000000000000

Cualquier valor de expiración distinto de cero hará que la firma de RouterInfo no supere la validación.

### Protocolos de transporte

**Protocolos actuales (a partir de la versión 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Valores de estilo de transporte:** - `"SSU2"`: Transporte actual basado en UDP - `"NTCP2"`: Transporte actual basado en TCP - `"NTCP"`: Obsoleto, eliminado (no usar) - `"SSU"`: Obsoleto, eliminado (no usar)

### Opciones comunes

Todos los transportes suelen incluir:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Opciones específicas de SSU2

Consulte la [especificación de SSU2](/docs/specs/ssu2/) (protocolo de transporte de I2P) para obtener todos los detalles.

**Opciones requeridas:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Opciones opcionales:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Ejemplo de RouterAddress SSU2:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Opciones específicas de NTCP2

Consulte la [especificación de NTCP2](/docs/specs/ntcp2/) para obtener todos los detalles.

**Opciones obligatorias:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Opciones opcionales (desde la versión 0.9.50):**

```
"caps" = Capability string
```
**Ejemplo de NTCP2 RouterAddress:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Notas de implementación

1. **Valores de costo:**
   - UDP (SSU2) suele tener menor costo (5-6) debido a su eficiencia
   - TCP (NTCP2) suele tener mayor costo (10-11) debido a la sobrecarga
   - Menor costo = transporte preferido

2. **Múltiples direcciones:**
   - Routers pueden publicar múltiples entradas de RouterAddress (estructura de dirección del router en I2P)
   - Diferentes transportes (SSU2 y NTCP2)
   - Diferentes versiones de IP (IPv4 e IPv6)
   - Los clientes seleccionan en función del coste y las capacidades

3. **Nombre de host vs IP:**
   - Para un mejor rendimiento, se prefieren las direcciones IP
   - Se admiten los nombres de host, pero añaden sobrecarga de resolución DNS
   - Considera usar IP para los RouterInfos (objetos de información del router en I2P) publicados

4. **Codificación Base64:**
   - Todas las claves y los datos binarios codificados en Base64
   - Base64 estándar (RFC 4648)
   - Sin relleno ni caracteres no estándar

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (información del router)

**Descripción:** Información completa publicada sobre un router, almacenada en la base de datos de la red. Contiene identidad, direcciones y capacidades.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Almacenamiento de base de datos:** - **Tipo de base de datos:** 0 - **Clave:** hash SHA-256 de RouterIdentity - **Valor:** estructura completa de RouterInfo

**Marca de tiempo de publicación:** - Fecha de 8 bytes (milisegundos desde la época Unix) - Se usa para el versionado de RouterInfo (información del router) - Los routers publican nuevo RouterInfo periódicamente - Los floodfill mantienen la versión más reciente basándose en la marca de tiempo de publicación

**Ordenación de direcciones:** - **Histórico:** routers muy antiguos requerían que las direcciones estuvieran ordenadas por el SHA-256 de sus datos - **Actual:** La ordenación NO es necesaria, no merece la pena implementarla por compatibilidad - Las direcciones pueden estar en cualquier orden

**Peer Size Field (tamaño de pares) (histórico):** - **Siempre 0** en I2P moderno - Estaba destinado a rutas restringidas (no implementado) - Si se implementara, iría seguido por esa cantidad de Router Hashes - Algunas implementaciones antiguas podrían haber requerido una lista de pares ordenada

**Asignación de opciones:**

Las opciones DEBEN estar ordenadas por clave. Las opciones estándar incluyen:

**Opciones de capacidades:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Opciones de red:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Opciones estadísticas:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Consulta la [documentación de RouterInfo de la base de datos de la red](/docs/specs/common-structures/#routerInfo) para la lista completa de opciones estándar.

**Cálculo de la firma:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**RouterInfo típico moderno (información del router):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Notas de implementación:**

1. **Varias direcciones:**
   - Los routers normalmente publican 1-4 direcciones
   - Variantes IPv4 e IPv6
   - Transportes SSU2 y/o NTCP2
   - Cada dirección es independiente

2. **Versionado:**
   - Un RouterInfo más reciente tiene una marca de tiempo `published` posterior
   - Los Routers vuelven a publicar cada ~2 horas o cuando las direcciones cambian
   - Los Floodfills almacenan y difunden solo la versión más reciente

3. **Validación:**
   - Verificar la firma antes de aceptar RouterInfo (información del router)
   - Comprobar que el campo de expiración contenga únicamente ceros en cada RouterAddress (dirección del router)
   - Validar que el mapeo de opciones esté ordenado por clave
   - Comprobar que los tipos de certificado y de clave sean conocidos y admitidos

4. **Base de datos de red (netDb):**
   - Floodfills almacenan RouterInfo indexado mediante Hash(RouterIdentity)
   - Se conserva durante ~2 días tras la última publicación
   - Los routers consultan los floodfills para descubrir otros routers

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Notas de implementación

### Orden de bytes (Endianness, disposición de los bytes)

**Predeterminado: Big-Endian (orden de bytes de red)**

La mayoría de las estructuras de I2P usan orden de bytes big-endian (byte más significativo primero): - Todos los tipos enteros (1-8 bytes) - Marcas de tiempo de fecha - TunnelId - Prefijo de longitud de cadena - Tipos y longitudes de certificados - Códigos de tipo de clave - Campos de tamaño de mapeo

**Excepción: Little-Endian (orden de bytes con el menos significativo primero)**

Los siguientes tipos de claves utilizan codificación **little-endian** (orden de bytes de menor a mayor): - **X25519** claves de cifrado (tipo 4) - **EdDSA_SHA512_Ed25519** claves de firma (tipo 7) - **EdDSA_SHA512_Ed25519ph** claves de firma (tipo 8) - **RedDSA_SHA512_Ed25519** claves de firma (tipo 11)

**Implementación:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Versionado de estructuras

**Nunca asumas tamaños fijos:**

Muchas estructuras tienen longitud variable: - RouterIdentity: 387+ bytes (no siempre 387) - Destination: 387+ bytes (no siempre 387) - LeaseSet2: Varía significativamente - Certificate: 3+ bytes

**Leer siempre los campos de tamaño:** - Longitud del certificado en los bytes 1-2 - Tamaño del mapeo al principio - KeysAndCert siempre se calcula como 384 + 3 + certificate_length

**Comprobar exceso de datos:** - Prohibir datos basura al final de estructuras válidas - Validar que las longitudes de los certificados coincidan con los tipos de clave - Exigir las longitudes exactas previstas para los tipos de tamaño fijo

### Recomendaciones actuales (octubre de 2025)

**Para nuevas identidades de Router:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/es/proposals/161-ri-dest-padding/)
```
**Para nuevos destinos:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/es/proposals/161-ri-dest-padding/)
```
**Para nuevos LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Para servicios cifrados:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Características obsoletas - No usar

**Cifrado obsoleto:** - ElGamal (tipo 0) para identidades de Router (obsoleto desde 0.9.58) - cifrado ElGamal/AES+SessionTag (utilice ECIES-X25519)

**Firmas obsoletas:** - DSA_SHA1 (tipo 0) para Identidades de Router (en desuso desde 0.9.58) - Variantes ECDSA (tipos 1-3) para nuevas implementaciones - Variantes RSA (tipos 4-6) excepto para archivos SU3

**Formatos de red obsoletos:** - LeaseSet tipo 1 (usar LeaseSet2) - Lease (registro de arrendamiento de túnel) (44 bytes, usar Lease2) - Formato original de expiración de Lease

**Transportes obsoletos:** - NTCP (eliminado en 0.9.50) - SSU (eliminado en 2.4.0)

**Certificados obsoletos:** - HASHCASH (tipo 1) - HIDDEN (tipo 2) - SIGNED (tipo 3) - MULTIPLE (tipo 4)

### Consideraciones de seguridad

**Generación de claves:** - Usa siempre generadores de números aleatorios criptográficamente seguros - Nunca reutilices claves en distintos contextos - Protege las claves privadas con controles de acceso adecuados - Borra de forma segura el material de clave de la memoria al finalizar

**Verificación de firmas:** - Verifica siempre las firmas antes de confiar en los datos - Verifica que la longitud de la firma coincida con el tipo de clave - Verifica que los datos firmados incluyan los campos esperados - Para mapeos ordenados, verifica el orden de clasificación antes de firmar/verificar

**Validación de marca de tiempo:** - Comprueba que los tiempos publicados sean razonables (no muy en el futuro) - Valida que las expiraciones de lease (entrada de tunnel en un leaseSet con vencimiento) no estén vencidas - Considera la tolerancia al desfase del reloj (±30 segundos típico)

**Base de datos de la red:** - Validar todas las estructuras antes de almacenarlas - Aplicar límites de tamaño para evitar ataques DoS - Limitar la tasa de consultas y publicaciones - Verificar que las claves de la base de datos coincidan con los hashes de las estructuras

### Notas de compatibilidad

**Retrocompatibilidad:** - ElGamal y DSA_SHA1 siguen siendo compatibles para routers heredados - Los tipos de clave obsoletos siguen siendo funcionales, pero se desaconsejan - Relleno compresible ([Proposal 161](/es/proposals/161-ri-dest-padding/)) retrocompatible hasta la versión 0.6

**Compatibilidad con versiones futuras:** - Los tipos de clave desconocidos pueden analizarse utilizando campos de longitud - Los tipos de certificado desconocidos pueden omitirse usando la longitud - Los tipos de firma desconocidos deben manejarse de forma adecuada - Los implementadores no deben fallar ante características opcionales desconocidas

**Estrategias de migración:** - Admitir tanto los tipos de claves antiguos como los nuevos durante la transición - LeaseSet2 puede enumerar varias claves de cifrado - Las firmas fuera de línea permiten una rotación de claves segura - MetaLeaseSet permite una migración de servicios transparente

### Pruebas y validación

**Validación de estructuras:** - Verificar que todos los campos de longitud estén dentro de los rangos esperados - Comprobar que las estructuras de longitud variable se analicen correctamente - Validar que las firmas se verifiquen correctamente - Probar con estructuras de tamaño mínimo y máximo

**Casos límite:** - Cadenas de longitud cero - Mapeos vacíos - Número mínimo y máximo de leases (entradas de entrega temporales en I2P) - Certificado con carga útil de longitud cero - Estructuras muy grandes (cerca de los tamaños máximos)

**Interoperabilidad:** - Probar frente a la implementación oficial de Java I2P - Verificar la compatibilidad con i2pd - Probar con diversos contenidos de la base de datos de red - Validar frente a vectores de prueba conocidos como correctos

---

## Referencias

### Especificaciones

- [Protocolo I2NP](/docs/specs/i2np/)
- [Protocolo I2CP](/docs/specs/i2cp/)
- [Transporte SSU2](/docs/specs/ssu2/)
- [Transporte NTCP2](/docs/specs/ntcp2/)
- [Protocolo de Tunnel](/docs/specs/implementation/)
- [Protocolo de datagramas](/docs/api/datagrams/)

### Criptografía

- [Descripción general de la criptografía](/docs/specs/cryptography/)
- [Cifrado ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Cifrado ECIES-X25519](/docs/specs/ecies/)
- [ECIES para Routers](/docs/specs/ecies/#routers)
- [ECIES híbrido (poscuántico)](/docs/specs/ecies/#hybrid)
- [Firmas Red25519](/docs/specs/red25519-signature-scheme/)
- [LeaseSet cifrado (conjunto de concesiones de túnel)](/docs/specs/encryptedleaseset/)

### Propuestas

- [Propuesta 123: Nuevas entradas de netDB](/proposals/123-new-netdb-entries/)
- [Propuesta 134: Tipos de firma GOST](/proposals/134-gost/)
- [Propuesta 136: Tipos de firma experimentales](/proposals/136-experimental-sigtypes/)
- [Propuesta 145: ECIES-P256](/proposals/145-ecies/)
- [Propuesta 156: Routers ECIES](/proposals/156-ecies-routers/)
- [Propuesta 161: Generación de relleno](/es/proposals/161-ri-dest-padding/)
- [Propuesta 167: Registros de servicio](/proposals/167-service-records/)
- [Propuesta 169: Criptografía poscuántica](/proposals/169-pq-crypto/)
- [Índice de todas las propuestas](/proposals/)

### Base de datos de la red

- [Descripción general de la base de datos de la red](/docs/specs/common-structures/)
- [Opciones estándar de RouterInfo](/docs/specs/common-structures/#routerInfo)

### Referencia de la API de JavaDoc

- [Paquete de datos del núcleo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Estándares externos

- **RFC 7748 (X25519):** Curvas elípticas para la seguridad
- **RFC 7539 (ChaCha20):** ChaCha20 y Poly1305 para los protocolos de la IETF
- **RFC 4648 (Base64):** Codificaciones de datos Base16, Base32 y Base64
- **FIPS 180-4 (SHA-256):** Estándar de hash seguro
- **FIPS 204 (ML-DSA):** Estándar de firma digital basado en retículas modulares
- [Registro de servicios de IANA](http://www.dns-sd.org/ServiceTypes.html)

### Recursos de la comunidad

- [Sitio web de I2P](/)
- [Foro de I2P](https://i2pforum.net)
- [GitLab de I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Espejo de GitHub de I2P](https://github.com/i2p/i2p.i2p)
- [Índice de documentación técnica](/docs/)

### Información de la versión

- [Lanzamiento de I2P 2.10.0](/es/blog/2025/09/08/i2p-2.10.0-release/)
- [Historial de lanzamientos](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Registro de cambios](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Apéndice: Tablas de referencia rápida

### Referencia rápida de tipos de clave

**Estándar actual (recomendado para todas las implementaciones nuevas):** - **Cifrado:** X25519 (tipo 4, 32 bytes, little-endian (orden de bytes de menor a mayor)) - **Firma:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes, little-endian)

**Heredado (admitido pero obsoleto):** - **Cifrado:** ElGamal (tipo 0, 256 bytes, big-endian) - **Firma:** DSA_SHA1 (tipo 0, privada de 20 bytes / pública de 128 bytes, big-endian)

**Especializado:** - **Firma (LeaseSet cifrado):** RedDSA_SHA512_Ed25519 (tipo 11, 32 bytes, little-endian (orden de bytes de menor a mayor))

**Poscuántico (Beta, sin finalizar):** - **Cifrado híbrido:** variantes MLKEM_X25519 (tipos 5-7) - **Cifrado poscuántico puro:** variantes MLKEM (esquema de encapsulación de claves poscuántico) (aún sin códigos de tipo asignados)

### Referencia rápida de tamaños de estructuras

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Referencia rápida del tipo de base de datos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Referencia rápida del protocolo de transporte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Referencia rápida de hitos de versión

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/es/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
