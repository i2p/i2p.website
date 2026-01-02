---
title: "Datagramas"
description: "Formatos de mensaje autenticado, respondible y sin procesar sobre I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Descripción general

Los datagramas proporcionan comunicación orientada a mensajes sobre [I2CP](/docs/specs/i2cp/) y en paralelo a la biblioteca de streaming. Permiten paquetes **respondibles**, **autenticados** o **sin procesar** sin requerir flujos orientados a conexión. Los routers encapsulan los datagramas en mensajes I2NP y mensajes de túnel, independientemente de si NTCP2 o SSU2 transporta el tráfico.

La motivación principal es permitir que las aplicaciones (como trackers, resolvedores DNS o juegos) envíen paquetes autónomos que identifiquen a su remitente.

> **Nuevo en 2025:** El Proyecto I2P aprobó **Datagram2 (protocolo 19)** y **Datagram3 (protocolo 20)**, agregando protección contra replay y mensajería con respuesta de menor sobrecarga por primera vez en una década.

---

## 1. Constantes del Protocolo

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Los protocolos 19 y 20 se formalizaron en la **Propuesta 163 (abril de 2025)**. Coexisten con Datagram1 / RAW para mantener la compatibilidad con versiones anteriores.

---

## 2. Tipos de Datagramas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Patrones de Diseño Típicos

- **Solicitud → Respuesta:** Enviar un Datagram2 firmado (solicitud + nonce), recibir una respuesta raw o Datagram3 (eco del nonce).  
- **Alta frecuencia/baja sobrecarga:** Preferir Datagram3 o RAW.  
- **Mensajes de control autenticados:** Datagram2.  
- **Compatibilidad con versiones anteriores:** Datagram1 aún completamente soportado.

---

## 3. Detalles de Datagram2 y Datagram3 (2025)

### Datagram2 (Protocolo 19)

Reemplazo mejorado para Datagram1. Características: - **Prevención de repetición:** token anti-repetición de 4 bytes. - **Soporte de firma offline:** permite el uso por Destinations firmados offline. - **Cobertura de firma ampliada:** incluye hash de destino, flags, opciones, bloque de firma offline, payload. - **Preparado para post-cuántico:** compatible con futuros híbridos ML-KEM. - **Overhead:** ≈ 457 bytes (claves X25519).

### Datagram3 (Protocolo 20)

Cierra la brecha entre tipos raw y firmados. Características: - **Replicable sin firma:** contiene hash de 32 bytes del remitente + flags de 2 bytes. - **Sobrecarga mínima:** ≈ 34 bytes. - **Sin defensa contra replay** — la aplicación debe implementarla.

Ambos protocolos son características de la API 0.9.66 e implementados en el router Java desde la versión 2.9.0; aún no hay implementaciones en i2pd o Go (octubre de 2025).

---

## 4. Límites de Tamaño y Fragmentación

- **Tamaño del mensaje de tunnel:** 1 028 bytes (4 B Tunnel ID + 16 B IV + 1 008 B payload).  
- **Fragmento inicial:** 956 B (entrega TUNNEL típica).  
- **Fragmento de continuación:** 996 B.  
- **Fragmentos máximos:** 63–64.  
- **Límite práctico:** ≈ 62 708 B (~61 KB).  
- **Límite recomendado:** ≤ 10 KB para entrega confiable (las pérdidas aumentan exponencialmente más allá de este valor).

**Resumen de sobrecarga:** - Datagram1 ≈ 427 B (mínimo).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Capas adicionales (encabezado gzip I2CP, I2NP, Garlic, Tunnel): + ~5.5 KB en el peor caso.

---

## 5. Integración I2CP / I2NP

Ruta del mensaje: 1. La aplicación crea un datagrama (vía API I2P o SAM).   2. I2CP lo envuelve con encabezado gzip (`0x1F 0x8B 0x08`, RFC 1952) y suma de verificación CRC-32.   3. Números de Protocolo + Puerto se almacenan en campos del encabezado gzip.   4. El router encapsula como mensaje I2NP → clove Garlic → fragmentos de tunnel de 1 KB.   5. Los fragmentos atraviesan tunnel de salida → red → tunnel de entrada.   6. El datagrama reensamblado se entrega al manejador de aplicación según el número de protocolo.

**Integridad:** CRC-32 (desde I2CP) + firma criptográfica opcional (Datagram1/2). No hay un campo de suma de verificación separado dentro del datagrama en sí.

---

## 6. Interfaces de Programación

### API de Java

El paquete `net.i2p.client.datagram` incluye: - `I2PDatagramMaker` – construye datagramas firmados.   - `I2PDatagramDissector` – verifica y extrae información del remitente.   - `I2PInvalidDatagramException` – se lanza cuando falla la verificación.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) gestiona la multiplexación de protocolo y puerto para aplicaciones que comparten un Destination.

**Acceso a Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (solo red I2P) - [Espejo de Javadoc](https://eyedeekay.github.io/javadoc-i2p/) (espejo en clearnet) - [Javadocs oficiales](http://docs.i2p-projekt.de/javadoc/) (documentación oficial)

### Soporte para SAM v3

- SAM 3.2 (2016): agregó los parámetros PORT y PROTOCOL.  
- SAM 3.3 (2016): introdujo el modelo PRIMARY/subsession; permite streams + datagramas en un Destination.  
- Soporte para estilos de sesión Datagram2 / 3 agregado a la especificación en 2025 (implementación pendiente).  
- Especificación oficial: [Especificación SAM v3](/docs/api/samv3/)

### Módulos de i2ptunnel

- **udpTunnel:** Base completamente funcional para aplicaciones I2P UDP (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Operativo para transmisión A/V (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **No funcional** a partir de 2.10.0 (solo stub UDP).

> Para UDP de propósito general, utilice la API Datagram o udpTunnel directamente—no dependa de SOCKS UDP.

---

## 7. Ecosistema y Soporte de Idiomas (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P es el único router que admite subsesiones completas de SAM 3.3 y la API Datagram2 en este momento.

---

## 8. Ejemplo de Uso – Rastreador UDP (I2PSnark 2.10.0)

Primera aplicación real de Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
El patrón demuestra el uso mixto de datagramas autenticados y ligeros para equilibrar seguridad y rendimiento.

---

## 9. Seguridad y Mejores Prácticas

- Usa Datagram2 para cualquier intercambio autenticado o cuando los ataques de repetición importen.
- Prefiere Datagram3 para respuestas rápidas replicables con confianza moderada.
- Usa RAW para transmisiones públicas o datos anónimos.
- Mantén las cargas útiles ≤ 10 KB para una entrega confiable.
- Ten en cuenta que SOCKS UDP permanece no funcional.
- Siempre verifica el CRC de gzip y las firmas digitales al recibir.

---

## 10. Especificación Técnica

Esta sección cubre los formatos de datagramas de bajo nivel, la encapsulación y los detalles del protocolo.

### 10.1 Identificación de Protocolo

Los formatos de datagrama **no** comparten un encabezado común. Los routers no pueden inferir el tipo solo a partir de los bytes de carga útil.

Al mezclar múltiples tipos de datagramas, o al combinar datagramas con streaming, configure explícitamente: - El **número de protocolo** (vía I2CP o SAM) - Opcionalmente el **número de puerto**, si su aplicación multiplexa servicios

Dejar el protocolo sin configurar (`0` o `PROTO_ANY`) no es recomendable y puede provocar errores de enrutamiento o entrega.

### 10.2 Datagramas sin procesar

Los datagramas no respondibles no llevan datos del remitente ni de autenticación. Son cargas útiles opacas, manejadas fuera de la API de datagramas de nivel superior pero soportadas a través de SAM e I2PTunnel.

**Protocolo:** `18` (`PROTO_DATAGRAM_RAW`)

**Formato:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
La longitud de la carga útil está limitada por los límites del transporte (≈32 KB máximo práctico, a menudo mucho menos).

### 10.3 Datagram1 (Datagramas con Respuesta)

Incluye el **Destination** del remitente y una **Signature** para autenticación y direccionamiento de respuestas.

**Protocolo:** `17` (`PROTO_DATAGRAM`)

**Sobrecarga:** ≥427 bytes **Carga útil:** hasta ~31.5 KB (limitado por el transporte)

**Formato:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: un Destination (387+ bytes)
- `signature`: una Signature que coincide con el tipo de clave
  - Para DSA_SHA1: Signature del hash SHA-256 de la carga útil
  - Para otros tipos de clave: Signature directamente sobre la carga útil

**Notas:** - Las firmas para tipos que no son DSA se estandarizaron en I2P 0.9.14. - Las firmas offline de LS2 (Propuesta 123) no están actualmente soportadas en Datagram1.

### 10.4 Formato Datagram2

Un datagrama replicable mejorado que añade **resistencia a reproducción** según se define en [Propuesta 163](/proposals/163-datagram2/).

**Protocolo:** `19` (`PROTO_DATAGRAM2`)

La implementación está en curso. Las aplicaciones deben incluir verificaciones de nonce o marca de tiempo para redundancia.

### 10.5 Formato Datagram3

Proporciona datagramas **con capacidad de respuesta pero no autenticados**. Se basa en la autenticación de sesión mantenida por el router en lugar de destino y firma embebidos.

**Protocolo:** `20` (`PROTO_DATAGRAM3`) **Estado:** En desarrollo desde 0.9.66

Útil cuando: - Los destinos son grandes (por ejemplo, claves post-cuánticas) - La autenticación ocurre en otra capa - La eficiencia del ancho de banda es crítica

### 10.6 Integridad de Datos

La integridad del datagrama está protegida por el **checksum gzip CRC-32** en la capa I2CP. No existe un campo de checksum explícito dentro del formato de carga útil del datagrama en sí.

### 10.7 Encapsulación de Paquetes

Cada datagrama se encapsula como un único mensaje I2NP o como un diente individual en un **Garlic Message**. Las capas I2CP, I2NP y de tunnel manejan la longitud y el encuadre — no hay delimitador interno ni campo de longitud en el protocolo de datagramas.

### 10.8 Consideraciones Post-Cuánticas (PQ)

Si se implementa la **Propuesta 169** (firmas ML-DSA), los tamaños de firma y destino aumentarán drásticamente — de ~455 bytes a **≥3739 bytes**. Este cambio incrementará sustancialmente la sobrecarga de datagramas y reducirá la capacidad efectiva de carga útil.

**Datagram3**, que se basa en la autenticación a nivel de sesión (no en firmas embebidas), probablemente se convertirá en el diseño preferido en entornos I2P post-cuánticos.

---

## 11. Referencias

- [Propuesta 163 – Datagram2 y Datagram3](/proposals/163-datagram2/)
- [Propuesta 160 – Integración de UDP Tracker](/proposals/160-udp-trackers/)
- [Propuesta 144 – Cálculos de MTU en Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Propuesta 169 – Firmas Post-Cuánticas](/proposals/169-pq-crypto/)
- [Especificación I2CP](/docs/specs/i2cp/)
- [Especificación I2NP](/docs/specs/i2np/)
- [Especificación de Mensajes de Tunnel](/docs/specs/implementation/)
- [Especificación SAMv3](/docs/api/samv3/)
- [Documentación de i2ptunnel](/docs/api/i2ptunnel/)

## 12. Aspectos Destacados del Registro de Cambios (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Resumen

El subsistema de datagramas ahora admite cuatro variantes de protocolo que ofrecen un espectro desde transmisión completamente autenticada hasta transmisión raw ligera. Los desarrolladores deben migrar hacia **Datagram2** para casos de uso sensibles a la seguridad y **Datagram3** para tráfico eficiente con capacidad de respuesta. Todos los tipos antiguos permanecen compatibles para garantizar la interoperabilidad a largo plazo.
