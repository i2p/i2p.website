---
title: "Protocolo de Streaming"
description: "Transporte tipo TCP utilizado por la mayoría de las aplicaciones I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

La **I2P Streaming Library** proporciona transporte confiable, ordenado y autenticado sobre la capa de mensajes de I2P, similar a **TCP sobre IP**. Se sitúa por encima del [protocolo I2CP](/docs/specs/i2cp/) y es utilizada por casi todas las aplicaciones interactivas de I2P, incluyendo proxies HTTP, IRC, BitTorrent y correo electrónico.

### Características principales

- Configuración de conexión en una fase usando banderas **SYN**, **ACK** y **FIN** que pueden agruparse con datos de carga útil para reducir los viajes de ida y vuelta.
- **Control de congestión de ventana deslizante**, con arranque lento y prevención de congestión ajustados para el entorno de alta latencia de I2P.
- Compresión de paquetes (segmentos comprimidos de 4KB por defecto) que equilibra el costo de retransmisión y la latencia de fragmentación.
- Abstracción de canal completamente **autenticado, cifrado** y **confiable** entre destinos I2P.

Este diseño permite que las solicitudes y respuestas HTTP pequeñas se completen en un solo viaje de ida y vuelta. Un paquete SYN puede transportar la carga útil de la solicitud, mientras que el SYN/ACK/FIN del respondedor puede contener el cuerpo completo de la respuesta.

---

## Conceptos básicos de la API

La API de streaming de Java refleja la programación estándar de sockets de Java:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` negocia o reutiliza una sesión de router mediante I2CP.
- Si no se proporciona ninguna clave, se genera automáticamente un destino nuevo.
- Los desarrolladores pueden pasar opciones I2CP (por ejemplo, longitudes de tunnel, tipos de cifrado o configuraciones de conexión) a través del mapa `options`.
- `I2PSocket` e `I2PServerSocket` reflejan las interfaces estándar de `Socket` de Java, lo que facilita la migración.

Los Javadocs completos están disponibles desde la consola del router I2P o [aquí](/docs/specs/streaming/).

---

## Configuración y Ajuste

Puedes pasar propiedades de configuración al crear un socket manager mediante:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Opciones de Clave

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Comportamiento por Carga de Trabajo

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Las características más recientes desde la versión 0.9.4 incluyen supresión de registros de rechazo, soporte de lista DSA (0.9.21) y aplicación obligatoria de protocolo (0.9.36). Los routers desde la versión 2.10.0 incluyen cifrado híbrido post-cuántico (ML-KEM + X25519) en la capa de transporte.

---

## Detalles del Protocolo

Cada flujo se identifica mediante un **Stream ID**. Los paquetes llevan indicadores de control similares a TCP: `SYNCHRONIZE`, `ACK`, `FIN` y `RESET`. Los paquetes pueden contener tanto datos como indicadores de control simultáneamente, mejorando la eficiencia para conexiones de corta duración.

### Ciclo de vida de la conexión

1. **SYN enviado** — el iniciador incluye datos opcionales.  
2. **Respuesta SYN/ACK** — el respondedor incluye datos opcionales.  
3. **Finalización ACK** — establece la fiabilidad y el estado de la sesión.  
4. **FIN/RESET** — utilizado para cierre ordenado o terminación abrupta.

### Fragmentación y Reordenamiento

Debido a que los túneles I2P introducen latencia y reordenamiento de mensajes, la biblioteca almacena en búfer los paquetes de streams desconocidos o que llegan anticipadamente. Los mensajes almacenados en búfer se guardan hasta que se completa la sincronización, garantizando una entrega completa y en orden.

### Aplicación del Protocolo

La opción `i2p.streaming.enforceProtocol=true` (predeterminada desde la versión 0.9.36) garantiza que las conexiones utilicen el número de protocolo I2CP correcto, evitando conflictos entre múltiples subsistemas que comparten un mismo destino.

---

## Interoperabilidad y Mejores Prácticas

El protocolo de streaming coexiste con la **API de Datagram**, brindando a los desarrolladores la opción entre transportes orientados a conexión y sin conexión.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Clientes Compartidos

Las aplicaciones pueden reutilizar túneles existentes ejecutándose como **clientes compartidos**, permitiendo que múltiples servicios compartan el mismo destino. Si bien esto reduce la sobrecarga, aumenta el riesgo de correlación entre servicios—úselo con precaución.

### Control de Congestión

- La capa de streaming se adapta continuamente a la latencia y el rendimiento de la red mediante retroalimentación basada en RTT.
- Las aplicaciones funcionan mejor cuando los routers son peers contribuyentes (túneles de participación habilitados).
- Los mecanismos de control de congestión similares a TCP previenen la sobrecarga de peers lentos y ayudan a equilibrar el uso del ancho de banda entre túneles.

### Consideraciones de Latencia

Dado que I2P añade varios cientos de milisegundos de latencia base, las aplicaciones deben minimizar los viajes de ida y vuelta. Agrupa datos con la configuración de conexión donde sea posible (por ejemplo, solicitudes HTTP en SYN). Evita diseños que dependan de muchos intercambios secuenciales pequeños.

---

## Pruebas y Compatibilidad

- Siempre prueba con **Java I2P** e **i2pd** para garantizar compatibilidad completa.
- Aunque el protocolo está estandarizado, pueden existir diferencias menores de implementación.
- Maneja routers antiguos con elegancia—muchos peers todavía ejecutan versiones anteriores a la 2.0.
- Monitorea las estadísticas de conexión usando `I2PSocket.getOptions()` y `getSession()` para leer métricas de RTT y retransmisión.

El rendimiento depende en gran medida de la configuración del tunnel:   - **Tunnels cortos (1–2 saltos)** → menor latencia, anonimato reducido.   - **Tunnels largos (3+ saltos)** → mayor anonimato, RTT incrementado.

---

## Mejoras Clave (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Resumen

La **I2P Streaming Library** es la columna vertebral de toda comunicación confiable dentro de I2P. Garantiza la entrega de mensajes cifrados, autenticados y en orden, y proporciona un reemplazo casi directo para TCP en entornos anónimos.

Para lograr un rendimiento óptimo: - Minimice los viajes de ida y vuelta con agrupación SYN+payload.   - Ajuste los parámetros de ventana y tiempo de espera según su carga de trabajo.   - Favorezca tunnels más cortos para aplicaciones sensibles a la latencia.   - Use diseños que respeten la congestión para evitar sobrecargar a los peers.
