---
title: "Especificación de SSU2"
description: "Protocolo de transporte UDP seguro y parcialmente fiable Versión 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Descripción general

SSU2 es un protocolo de la capa de transporte basado en UDP, utilizado para una comunicación segura y con fiabilidad parcial de router a router en I2P. No es un transporte de propósito general, sino que está especializado en el **intercambio de mensajes de I2NP**.

### Capacidades fundamentales

- Intercambio de claves autenticado mediante Noise XK pattern (patrón XK de Noise)
- Encabezados cifrados para resistencia frente a la DPI (inspección profunda de paquetes)
- Atravesamiento de NAT usando relés y hole-punching (perforación NAT)
- Migración de conexiones y validación de direcciones
- Validación de ruta opcional
- Secreto perfecto hacia adelante (PFS) y protección contra ataques de repetición

### Legado y compatibilidad

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2 Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU1 Removed</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.61</td></tr>
  </tbody>
</table>
SSU1 ya no se utiliza en toda la red pública de I2P.

---

## 2. Criptografía

SSU2 usa **Noise_XK_25519_ChaChaPoly_SHA256** con extensiones específicas de I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie-Hellman</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (RFC 7748)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32-byte keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Cipher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (RFC 7539)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD encryption</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Used for key derivation and message integrity</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KDF</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HKDF-SHA256 (RFC 5869)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">For session and header keys</td></tr>
  </tbody>
</table>
Las cabeceras y las cargas útiles están vinculadas criptográficamente mediante `mixHash()`.   Todas las primitivas criptográficas se comparten con NTCP2 y ECIES para mejorar la eficiencia de la implementación.

---

## 3. Descripción general de los mensajes

### 3.1 Reglas de datagramas UDP

- Cada datagrama UDP transporta **exactamente un mensaje SSU2**.  
- Los mensajes Session Confirmed (confirmación de sesión) pueden fragmentarse en varios datagramas.

**Tamaño mínimo:** 40 bytes   **Tamaño máximo:** 1472 bytes (IPv4) / 1452 bytes (IPv6)

### 3.2 Tipos de mensajes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Header</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake initiation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Created</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake response</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Confirmed</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Final handshake, may be fragmented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted I2NP message blocks</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT reachability testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token or rejection notice</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Request for validation token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal signaling</td></tr>
  </tbody>
</table>
---

## 4. Establecimiento de sesión

### 4.1 Flujo estándar (token válido)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.2 Obtención de tokens

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.3 Token no válido

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```
---

## 5. Estructuras de encabezado

### 5.1 Cabecera larga (32 bytes)

Se utiliza antes del establecimiento de la sesión (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random unique ID</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random (ignored during handshake)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Always 2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NetID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2 = main I2P network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved (0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Source Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random ID distinct from destination</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token for address validation</td></tr>
  </tbody>
</table>
### 5.2 Cabecera corta (16 bytes)

Se usa durante sesiones establecidas (SessionConfirmed, Data).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Stable throughout session</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Incrementing per message</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type (2 or 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ACK/fragment flags</td></tr>
  </tbody>
</table>
---

## 6. Cifrado

### 6.1 AEAD (cifrado autenticado con datos asociados)

Todas las cargas útiles están cifradas con **ChaCha20/Poly1305 AEAD** (cifrado autenticado con datos asociados):

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```
- Nonce (número único de uso): 12 bytes (4 ceros + 8 de contador)
- Etiqueta: 16 bytes
- Datos asociados: incluye el encabezado para la vinculación de integridad

### 6.2 Protección del encabezado

Los encabezados se enmascaran utilizando un flujo de claves ChaCha20 derivado de las claves de encabezado de sesión. Esto garantiza que todos los ID de conexión y los campos de los paquetes parezcan aleatorios, proporcionando resistencia al DPI (Deep Packet Inspection, inspección profunda de paquetes).

### 6.3 Derivación de claves

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Phase</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Initial</td><td style="border:1px solid var(--color-border); padding:0.6rem;">introKey + salt</td><td style="border:1px solid var(--color-border); padding:0.6rem;">handshake header key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake</td><td style="border:1px solid var(--color-border); padding:0.6rem;">DH(X25519)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey + AEAD key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Data phase</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">TX/RX keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Key rotation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">oldKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">newKey</td></tr>
  </tbody>
</table>
---

## 7. Seguridad y prevención de ataques de repetición

- Los tokens son por IP y caducan en ~60 segundos.  
- Las repeticiones (ataques de repetición) se previenen mediante filtros de Bloom por sesión.  
- Se rechazan las claves efímeras duplicadas.  
- Los encabezados y las cargas útiles están criptográficamente vinculados.

Los routers deben descartar cualquier paquete que falle la autenticación AEAD o que tenga una versión no válida o un NetID no válido.

---

## 8. Numeración de paquetes y vida útil de la sesión

Cada sentido mantiene su propio contador de 32 bits.   - Empieza en 0, se incrementa con cada paquete.   - No debe hacer wrap (volver a 0); realizar session rekey (rotación de la clave de la sesión) o terminar antes de llegar a 2³².

Los identificadores de conexión permanecen estáticos durante toda la sesión, incluso durante la migración.

---

## 9. Fase de datos

- Tipo = 6 (Datos)
- Encabezado corto (16 bytes)
- La carga útil contiene uno o más bloques cifrados:
  - Listas ACK/NACK
  - Fragmentos de mensajes I2NP
  - Relleno (0–31 bytes aleatorios)
  - Bloques de terminación (opcional)

Se admiten la retransmisión selectiva y la entrega fuera de orden. La fiabilidad sigue siendo “semi-reliable” (semiconfiable) — los paquetes perdidos pueden descartarse silenciosamente después de alcanzar los límites de reintento.

---

## 10. Retransmisión y atravesamiento de NAT

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Determines inbound reachability</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Issues new token or rejection</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Requests new address token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Coordinates NAT hole punching</td></tr>
  </tbody>
</table>
Los routers de retransmisión ayudan a los pares detrás de NATs restrictivos mediante estos mensajes de control.

---

## 11. Terminación de la sesión

Cualquiera de los pares puede cerrar la sesión usando un **Termination block** (bloque de terminación) dentro de un mensaje Data (mensaje de datos).   Los recursos deben liberarse inmediatamente tras la recepción.   Los paquetes de terminación repetidos pueden ignorarse después del acuse de recibo.

---

## 12. Directrices de implementación

Routers **DEBEN**: - Validar versión = 2 y NetID = 2.   - Descartar paquetes <40 bytes o AEAD no válido.   - Aplicar caché de repetición de 120s.   - Rechazar tokens reutilizados o claves efímeras.

Routers **DEBERÍAN**: - Aleatorizar el relleno de 0–31 bytes.   - Usar retransmisión adaptativa (RFC 6298).   - Implementar validación de ruta por par antes de la migración.

---

## 13. Resumen de seguridad

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Achieved By</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Forward secrecy</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 ephemeral keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Replay protection</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tokens + Bloom filter</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated encryption</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KCI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Noise XK pattern</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">DPI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted headers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Relay + Hole Punch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Migration</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Static connection IDs</td></tr>
  </tbody>
</table>
---

## 14. Referencias

- [Propuesta 159 – SSU2](/proposals/159-ssu2/)
- [Marco del protocolo Noise](https://noiseprotocol.org/noise.html)
- [RFC 9000 – Transporte QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9001 – TLS para QUIC](https://datatracker.ietf.org/doc/html/rfc9001)
- [RFC 7539 – ChaCha20/Poly1305 AEAD](https://datatracker.ietf.org/doc/html/rfc7539)
- [RFC 7748 – X25519 ECDH](https://datatracker.ietf.org/doc/html/rfc7748)
- [RFC 5869 – HKDF-SHA256](https://datatracker.ietf.org/doc/html/rfc5869)
