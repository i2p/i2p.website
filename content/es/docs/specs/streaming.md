---
title: "Protocolo de transmisión en continuo"
description: "Transporte fiable, similar a TCP, utilizado por la mayoría de las aplicaciones de I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Descripción general

La Biblioteca de Streaming de I2P proporciona una entrega de datos fiable, en el orden correcto y autenticada sobre la capa de mensajes no fiable de I2P — de forma análoga a TCP sobre IP. La utilizan casi todas las aplicaciones interactivas de I2P, como la navegación web, IRC, el correo electrónico y el intercambio de archivos.

Garantiza la transmisión confiable, el control de congestión, la retransmisión y el control de flujo a través de los tunnels anónimos de alta latencia de I2P. Cada flujo está completamente cifrado de extremo a extremo entre destinos.

---

## Principios de diseño fundamentales

La biblioteca de streaming implementa un **establecimiento de conexión de una sola fase**, donde las banderas SYN, ACK y FIN pueden transportar cargas útiles de datos en el mismo mensaje. Esto minimiza los viajes de ida y vuelta en entornos de alta latencia — una pequeña transacción HTTP puede completarse en un solo viaje de ida y vuelta.

El control de congestión y la retransmisión están inspirados en TCP, pero adaptados al entorno de I2P. Los tamaños de ventana son basados en mensajes, no en bytes, y están ajustados para la latencia del tunnel y la sobrecarga. El protocolo admite arranque lento, evitación de congestión y retroceso exponencial, de forma similar al algoritmo AIMD (Aumento Aditivo, Disminución Multiplicativa) de TCP.

---

## Arquitectura

La biblioteca de streaming opera entre las aplicaciones y la interfaz I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
La mayoría de los usuarios acceden a él a través de I2PSocketManager, I2PTunnel o SAMv3. La biblioteca se encarga de forma transparente de la gestión de destinos, del uso de tunnel y de las retransmisiones.

---

## Formato de paquete

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Detalles del encabezado

- **IDs de flujo**: Valores de 32 bits que identifican de forma única los flujos locales y remotos.
- **Número de secuencia**: Comienza en 0 para SYN y se incrementa por cada mensaje.
- **Ack Through (confirmación hasta)**: Confirma todos los mensajes hasta N, excluyendo los de la lista de NACK.
- **Banderas**: Máscara de bits que controla el estado y el comportamiento.
- **Opciones**: Lista de longitud variable para RTT, MTU y negociación del protocolo.

### Indicadores de clave

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Control de flujo y fiabilidad

Streaming utiliza **control de ventana basado en mensajes**, a diferencia del enfoque basado en bytes de TCP. La cantidad de paquetes sin acuse de recibo permitidos en tránsito equivale al tamaño de la ventana actual (predeterminado 128).

### Mecanismos

- **Control de congestión:** Arranque lento y evitación de congestión basada en AIMD.  
- **Choke/Unchoke:** Señalización de control de flujo basada en la ocupación del búfer (bloqueo/desbloqueo).  
- **Retransmisión:** Cálculo del RTO basado en RFC 6298 con retroceso exponencial.  
- **Filtrado de duplicados:** Garantiza la fiabilidad frente a mensajes potencialmente reordenados.

Valores de configuración típicos:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Establecimiento de la conexión

1. **Iniciador** envía un SYN (opcionalmente con carga útil y FROM_INCLUDED).  
2. **Respondedor** responde con SYN+ACK (puede incluir carga útil).  
3. **Iniciador** envía el ACK final confirmando el establecimiento.

Las cargas útiles iniciales opcionales permiten transmitir datos antes de la finalización completa del handshake (negociación inicial).

---

## Detalles de implementación

### Retransmisión y tiempo de espera

El algoritmo de retransmisión sigue la **RFC 6298**.   - **RTO inicial:** 9s   - **RTO mínima:** 100ms   - **RTO máxima:** 45s   - **Alfa:** 0.125   - **Beta:** 0.25

### Uso compartido del bloque de control

Las conexiones recientes con el mismo par reutilizan el RTT (tiempo de ida y vuelta) y los datos de ventana anteriores para un aumento más rápido, evitando la latencia de “arranque en frío”. Los bloques de control expiran tras varios minutos.

### MTU y fragmentación

- MTU predeterminado: **1730 bytes** (caben dos mensajes I2NP).  
- Destinos ECIES (Esquema de cifrado integrado sobre curvas elípticas): **1812 bytes** (sobrecarga reducida).  
- MTU mínimo admitido: 512 bytes.

El tamaño de la carga útil excluye el encabezado de streaming mínimo de 22 bytes.

---

## Historial de versiones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Uso a nivel de aplicación

### Ejemplo de Java

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Soporte para SAMv3 e i2pd

- **SAMv3**: Proporciona modos STREAM (flujo) y DATAGRAM (datagrama) para clientes no escritos en Java.  
- **i2pd**: Expone parámetros de streaming (transmisión) idénticos mediante opciones del archivo de configuración (p. ej., `i2p.streaming.maxWindowSize`, `profile`, etc).

---

## Elegir entre streaming y datagramas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Seguridad y futuro poscuántico

Las sesiones de streaming están cifradas de extremo a extremo en la capa I2CP.   El cifrado híbrido poscuántico (ML-KEM + X25519) es compatible de forma experimental en la versión 2.10.0, pero está desactivado de forma predeterminada.

---

## Referencias

- [Descripción general de la API de transmisión](/docs/specs/streaming/)  
- [Especificación del protocolo de transmisión](/docs/specs/streaming/)  
- [Especificación de I2CP](/docs/specs/i2cp/)  
- [Propuesta 144: Cálculos de MTU de transmisión](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Notas de la versión de I2P 2.10.0](/es/blog/2025/09/08/i2p-2.10.0-release/)
