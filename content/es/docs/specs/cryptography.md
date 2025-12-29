---
title: "Criptografía de bajo nivel"
description: "Resumen de las primitivas criptográficas simétricas, asimétricas y de firma utilizadas en todo I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Estado:** Esta página resume la antigua «Low-level Cryptography Specification» (especificación de criptografía de bajo nivel). Las versiones modernas de I2P (2.10.0, octubre de 2025) han completado la migración a nuevas primitivas criptográficas. Utilice especificaciones especializadas como [ECIES](/docs/specs/ecies/), [LeaseSets cifrados](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), y [Tunnel Creation (ECIES)](/docs/specs/implementation/) para detalles de implementación.

## Instantánea de la evolución

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Cifrado asimétrico

### X25519 (intercambio de claves de curva elíptica basado en Curve25519)

- Se utiliza para NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 y la creación de tunnel basada en X25519.  
- Proporciona claves compactas, operaciones en tiempo constante y secreto hacia adelante mediante el Noise protocol framework (marco del protocolo Noise).  
- Ofrece seguridad de 128 bits con claves de 32 bytes e intercambio de claves eficiente.

### ElGamal (heredado)

- Se mantiene por compatibilidad retroactiva con routers más antiguos.  
- Opera sobre el primo de 2048 bits del Grupo 14 de Oakley (RFC 3526) con generador 2.  
- Cifra las claves de sesión AES más los vectores de inicialización (IV) en textos cifrados de 514 bytes.  
- Carece de cifrado autenticado y de secreto hacia adelante; todos los extremos modernos han migrado a ECIES.

## Cifrado simétrico

### ChaCha20/Poly1305 (modo AEAD que combina el cifrado de flujo ChaCha20 con el MAC Poly1305)

- Primitiva de cifrado autenticado predeterminada en NTCP2, SSU2 y ECIES.  
- Proporciona seguridad AEAD y alto rendimiento sin soporte de hardware para AES.  
- Implementada según la RFC 7539 (clave de 256 bits, nonce (número único de uso) de 96 bits, etiqueta de 128 bits).

### AES‑256/CBC (heredado)

- Sigue utilizándose para el cifrado de la capa de tunnel, donde su estructura de cifrado de bloque encaja con el modelo de cifrado por capas de I2P.  
- Utiliza relleno PKCS#5 y transformaciones de IV (vector de inicialización) por salto.  
- Programado para una revisión a largo plazo, pero sigue siendo criptográficamente sólido.

## Firmas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Derivación de hash y de claves

- **SHA‑256:** Se usa para claves DHT, HKDF y firmas antiguas.  
- **SHA‑512:** Utilizado por EdDSA/RedDSA y en derivaciones HKDF de Noise.  
- **HKDF‑SHA256:** Deriva claves de sesión en ECIES, NTCP2 y SSU2.  
- Las derivaciones SHA‑256 con rotación diaria protegen las ubicaciones de almacenamiento de RouterInfo y LeaseSet en la netDb.

## Resumen de la capa de transporte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Ambos transportes proporcionan secreto hacia adelante a nivel de enlace y protección contra ataques de repetición, utilizando el patrón de handshake Noise_XK.

## Cifrado de la capa de Tunnel

- Sigue utilizando AES‑256/CBC para el cifrado en capas por salto.  
- Las puertas de enlace de salida realizan descifrado AES iterativo; cada salto vuelve a cifrar usando su clave de capa y su clave de IV (vector de inicialización).  
- El cifrado con IV doble mitiga ataques de correlación y de confirmación.  
- La migración a AEAD (cifrado autenticado con datos asociados) está en estudio, pero no está prevista actualmente.

## Criptografía poscuántica

- I2P 2.10.0 introduce **cifrado poscuántico híbrido experimental**.  
- Se habilita manualmente a través de Hidden Service Manager (administrador de servicios ocultos) para pruebas.  
- Combina X25519 con un KEM (mecanismo de encapsulación de claves) resistente a ataques cuánticos (modo híbrido).  
- No está habilitado por defecto; destinado a la investigación y la evaluación del rendimiento.

## Marco de extensibilidad

- Los *identificadores de tipo* de cifrado y firma permiten admitir en paralelo múltiples primitivas.  
- Las asignaciones actuales incluyen:  
  - **Tipos de cifrado:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Tipos de firma:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Este marco permite actualizaciones futuras, incluyendo esquemas poscuánticos, sin dividir la red.

## Composición criptográfica

- **Capa de transporte:** X25519 + ChaCha20/Poly1305 (Noise framework).  
- **Capa de tunnel:** Cifrado en capas AES‑256/CBC para el anonimato.  
- **De extremo a extremo:** ECIES‑X25519‑AEAD‑Ratchet para confidencialidad y secreto perfecto hacia adelante.  
- **Capa de base de datos:** Firmas EdDSA/RedDSA para autenticidad.

Estas capas se combinan para proporcionar defensa en profundidad: incluso si una capa se ve comprometida, las demás mantienen la confidencialidad y la no vinculabilidad.

## Resumen

La pila criptográfica de I2P 2.10.0 se centra en:

- **Curve25519 (X25519)** para intercambio de claves  
- **ChaCha20/Poly1305** para cifrado simétrico  
- **EdDSA / RedDSA** para firmas  
- **SHA‑256 / SHA‑512** para hashing y derivación  
- **Modos híbridos poscuánticos experimentales** para compatibilidad futura

Las versiones heredadas de ElGamal, AES‑CBC y DSA se mantienen por compatibilidad con versiones anteriores, pero ya no se utilizan en protocolos de transporte activos ni en rutas de cifrado.
