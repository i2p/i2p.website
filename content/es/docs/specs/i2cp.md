---
title: "Protocolo de Cliente de I2P (I2CP)"
description: "Cómo las aplicaciones negocian sesiones, tunnels y LeaseSets con el router de I2P."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

I2CP es el protocolo de control de bajo nivel entre un router de I2P y cualquier proceso cliente. Define una separación estricta de responsabilidades:

- **Router**: Gestiona el enrutamiento, la criptografía, los ciclos de vida de tunnel y las operaciones de la base de datos de la red
- **Cliente**: Selecciona propiedades de anonimato, configura tunnels y envía/recibe mensajes

Toda la comunicación se realiza a través de un único socket TCP (opcionalmente envuelto en TLS), lo que permite operaciones asíncronas y de dúplex completo.

**Versión del protocolo**: I2CP usa un byte de versión de protocolo `0x2A` (42 en decimal) enviado durante el establecimiento inicial de la conexión. Este byte de versión se ha mantenido estable desde el inicio del protocolo.

**Estado actual**: Esta especificación es precisa para la versión del router 0.9.67 (versión de la API 0.9.67), publicada en 2025-09.

## Contexto de implementación

### Implementación en Java

La implementación de referencia está en Java I2P: - SDK del cliente: paquete `i2p.jar` - Implementación del router: paquete `router.jar` - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Cuando el cliente y el router se ejecutan en la misma JVM, los mensajes de I2CP se pasan como objetos de Java sin serialización. Los clientes externos utilizan el protocolo serializado sobre TCP.

### Implementación en C++

i2pd (el router I2P en C++) también implementa I2CP de forma externa para conexiones de clientes.

### Clientes no Java

**No se conocen implementaciones no escritas en Java** de una biblioteca de cliente I2CP completa. Las aplicaciones no escritas en Java deberían usar en su lugar protocolos de nivel superior:

- **SAM (Simple Anonymous Messaging) v3**: Interfaz basada en sockets con bibliotecas para múltiples lenguajes
- **BOB (Basic Open Bridge, puente abierto básico)**: Alternativa más simple a SAM

Estos protocolos de nivel superior gestionan internamente la complejidad de I2CP y también proporcionan la biblioteca de streaming (para conexiones similares a TCP) y la biblioteca de datagramas (para conexiones similares a UDP).

## Establecimiento de conexión

### 1. Conexión TCP

Conéctese al puerto I2CP del router: - Predeterminado: `127.0.0.1:7654` - Configurable mediante la configuración del router - Capa TLS opcional (altamente recomendada para conexiones remotas)

### 2. Negociación del protocolo

**Paso 1**: Enviar el byte de versión del protocolo `0x2A`

**Paso 2**: Sincronización del reloj

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
El router devuelve su marca de tiempo actual y la cadena de versión de la API de I2CP (desde 0.8.7).

**Paso 3**: Autenticación (si está habilitada)

A partir de la 0.9.11, la autenticación puede incluirse en GetDateMessage (mensaje de obtención de fecha) mediante un Mapping (estructura de mapeo) que contenga: - `i2cp.username` - `i2cp.password`

A partir de la 0.9.16, cuando la autenticación está habilitada, **debe** completarse mediante GetDateMessage antes de que se envíe cualquier otro mensaje.

**Paso 4**: Creación de sesión

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Paso 5**: Señal de que el Tunnel está listo

```
Router → Client: RequestVariableLeaseSetMessage
```
Este mensaje indica que los tunnels entrantes se han construido. El router NO enviará esto hasta que haya al menos un tunnel entrante Y un tunnel saliente.

**Paso 6**: Publicación del LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
En este punto, la sesión está plenamente operativa para enviar y recibir mensajes.

## Patrones de flujo de mensajes

### Mensaje saliente (el cliente envía al destino remoto)

**Con i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Con i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Mensaje entrante (Router entrega al cliente)

**Con i2cp.fastReceive=true** (predeterminado desde 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Con i2cp.fastReceive=false** (OBSOLETO):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Los clientes modernos deberían usar siempre el modo de recepción rápida.

## Estructuras de datos comunes

### Encabezado de mensaje de I2CP

Todos los mensajes de I2CP utilizan este encabezado común:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Longitud del cuerpo**: entero de 4 bytes, solo la longitud del cuerpo del mensaje (excluye el encabezado)
- **Tipo**: entero de 1 byte, identificador del tipo de mensaje
- **Cuerpo del mensaje**: 0+ bytes, el formato varía según el tipo de mensaje

**Límite de tamaño del mensaje**: Aproximadamente 64 KB como máximo.

### ID de sesión

Entero de 2 bytes que identifica de forma única una sesión en un router.

**Valor especial**: `0xFFFF` indica "sin sesión" (se usa para la resolución de nombres de host sin una sesión establecida).

### ID de mensaje

Entero de 4 bytes generado por el router para identificar de forma única un mensaje dentro de una sesión.

**Importante**: Los ID de mensaje **no** son globalmente únicos; solo son únicos dentro de una sesión. También son distintos del nonce (número único de un solo uso) generado por el cliente.

### Formato de la carga útil

Las cargas útiles de los mensajes se comprimen con gzip con un encabezado gzip estándar de 10 bytes: - Comienza con: `0x1F 0x8B 0x08` (RFC 1952) - Desde la 0.7.1: Las partes no utilizadas del encabezado gzip contienen información de protocolo, from-port y to-port - Esto permite la transmisión (streaming) y los datagramas en el mismo destino

**Control de compresión**: Configura `i2cp.gzip=false` para desactivar la compresión (establece el esfuerzo de gzip en 0). La cabecera de gzip sigue incluyéndose, pero con una sobrecarga mínima de compresión.

### Estructura de SessionConfig

Define la configuración de una sesión de cliente:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Requisitos críticos**: 1. **El mapeo debe estar ordenado por clave** para la validación de la firma 2. **Fecha de creación** debe estar dentro de ±30 segundos del tiempo actual del router 3. **Firma** es creada por la SigningPrivateKey (clave privada de firma) de la Destination (Destino de I2P)

**Firmas sin conexión** (a partir de la versión 0.9.38):

Si se utiliza la firma fuera de línea, el mapeo debe contener: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

La firma se genera luego con la clave privada de firma transitoria.

## Opciones de configuración del núcleo

### Configuración del Tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Notas**: - Los valores de `quantity` > 6 requieren pares que ejecuten 0.9.0+ y aumentan significativamente el uso de recursos - Establezca `backupQuantity` en 1-2 para servicios de alta disponibilidad - Los tunnels Zero-hop (sin saltos) sacrifican anonimato en favor de la latencia, pero son útiles para pruebas

### Gestión de mensajes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Fiabilidad de los mensajes**: - `None`: Sin acuses de recibo del router (valor predeterminado de la biblioteca de streaming desde la versión 0.8.1) - `BestEffort`: El Router envía aceptación + notificaciones de éxito/fallo - `Guaranteed`: No implementado (actualmente se comporta como BestEffort)

**Anulación por mensaje** (desde 0.9.14): - En una sesión con `messageReliability=none`, establecer un nonce (valor aleatorio único) distinto de cero solicita una notificación de entrega para ese mensaje específico - Establecer nonce=0 en una sesión `BestEffort` desactiva las notificaciones para ese mensaje

### Configuración de LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Etiquetas de sesión heredadas de ElGamal/AES

Estas opciones solo son relevantes para el cifrado ElGamal heredado:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Nota**: Los clientes ECIES-X25519 usan un mecanismo de ratchet (mecanismo de avance criptográfico) diferente e ignoran estas opciones.

## Tipos de cifrado

I2CP admite múltiples esquemas de cifrado de extremo a extremo mediante la opción `i2cp.leaseSetEncType`. Se pueden especificar varios tipos (separados por comas) para admitir tanto pares modernos como heredados.

### Tipos de cifrado admitidos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Configuración recomendada**:

```
i2cp.leaseSetEncType=4,0
```
Esto proporciona X25519 (preferido; intercambio de claves mediante curva elíptica) con un mecanismo de respaldo ElGamal (esquema criptográfico asimétrico) para compatibilidad.

### Detalles del tipo de cifrado

**Tipo 0 - ElGamal/AES+SessionTags (etiquetas de sesión)**: - Claves públicas ElGamal de 2048 bits (256 bytes) - Cifrado simétrico AES-256 - SessionTags de 32 bytes enviadas en lotes - Alta sobrecarga de CPU, ancho de banda y memoria - Se está retirando gradualmente en toda la red

**Tipo 4 - ECIES-X25519-AEAD-Ratchet**: - Intercambio de claves X25519 (claves de 32 bytes) - ChaCha20/Poly1305 AEAD - double ratchet estilo Signal (doble trinquete) - Etiquetas de sesión de 8 bytes (frente a 32 bytes para ElGamal) - Etiquetas generadas mediante PRNG sincronizado (no se envían por adelantado) - Reducción del ~92% en sobrecarga frente a ElGamal - Estándar para el I2P moderno (la mayoría de los routers lo usan)

**Tipos 5-6 - Híbrido poscuántico**: - Combina X25519 con ML-KEM (NIST FIPS 203) - Ofrece seguridad resistente a ataques cuánticos - ML-KEM-768 para seguridad y rendimiento equilibrados - ML-KEM-1024 para máxima seguridad - Tamaños de mensaje mayores debido al material de claves poscuánticas - El soporte en la red aún se está desplegando

### Estrategia de migración

La red I2P está migrando activamente de ElGamal (tipo 0) a X25519 (tipo 4) (curva de clave elíptica): - NTCP → NTCP2 (completado) - SSU → SSU2 (completado) - ElGamal tunnels → X25519 tunnels (completado) - Cifrado de extremo a extremo con ElGamal → ECIES-X25519 (mayoritariamente completado)

## LeaseSet2 y funciones avanzadas

### Opciones de LeaseSet2 (desde 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Direcciones cegadas

A partir de la 0.9.39, los destinos pueden usar direcciones "blinded" (ocultadas) (formato b33) que cambian periódicamente: - Requiere `i2cp.leaseSetSecret` para protección por contraseña - Autenticación por cliente opcional - Consulte las propuestas 123 y 149 para más detalles

### Registros de servicio (desde 0.9.66)

LeaseSet2 admite opciones de registro de servicio (propuesta 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
El formato sigue el estilo de los registros SRV de DNS, pero adaptado para I2P.

## Múltiples sesiones (desde 0.9.21)

Una única conexión I2CP puede mantener múltiples sesiones:

**Sesión primaria**: La primera sesión creada en una conexión **Subsesiones**: Sesiones adicionales que comparten el grupo de tunnel de la sesión primaria

### Características de la subsesión

1. **Tunnels compartidos**: Usa los mismos conjuntos de tunnel entrantes/salientes que la sesión principal
2. **Claves de cifrado compartidas**: Debe usar claves de cifrado de LeaseSet idénticas
3. **Claves de firma diferentes**: Debe usar claves de firma de Destino distintas
4. **Sin garantía de anonimato**: Claramente vinculado a la sesión principal (mismo router, mismos tunnels)

### Caso de uso de Subsession (subsesión)

Permite la comunicación con destinos que usan diferentes tipos de firma:
- Principal: firma EdDSA (moderna)
- Subsession (subsesión): firma DSA (compatibilidad con sistemas heredados)

### Ciclo de vida de la subsesión

**Creación**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Destrucción**: - Destruir una subsesión: deja la sesión principal intacta - Destruir la sesión principal: destruye todas las subsesiones y cierra la conexión - DisconnectMessage: destruye todas las sesiones

### Gestión del ID de sesión

La mayoría de los mensajes de I2CP contienen un campo ID de sesión. Excepciones: - DestLookup / DestReply (obsoleto, use HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (la respuesta no es específica de la sesión)

**Importante**: Los clientes no deberían tener múltiples mensajes CreateSession pendientes simultáneamente, ya que las respuestas no pueden correlacionarse inequívocamente con las solicitudes.

## Catálogo de mensajes

### Resumen de tipos de mensajes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Leyenda**: C = Cliente, R = Router

### Detalles clave del mensaje

#### CreateSessionMessage (Tipo 1)

**Propósito**: Iniciar una nueva sesión de I2CP

**Contenido**: estructura de SessionConfig

**Respuesta**: SessionStatusMessage (mensaje de estado de sesión) (status=Created or Invalid)

**Requisitos**: - La fecha en SessionConfig debe estar dentro de ±30 segundos de la hora del router - El mapeo debe estar ordenado por clave para la validación de la firma - Destination (destino de I2P) no debe tener ya una sesión activa

#### RequestVariableLeaseSetMessage (Tipo 37)

**Propósito**: Router solicita autorización del cliente para tunnels entrantes

**Contenido**: - ID de sesión - Número de leases (concesiones temporales) - Arreglo de estructuras Lease (cada una con expiración individual)

**Respuesta**: CreateLeaseSet2Message

**Importancia**: Esta es la señal de que la sesión está operativa. El router envía esto solo después de: 1. Se ha construido al menos un tunnel entrante 2. Se ha construido al menos un tunnel saliente

**Recomendación de tiempo de espera**: Los clientes deberían finalizar la sesión si este mensaje no se recibe en un plazo superior a 5 minutos desde la creación de la sesión.

#### CreateLeaseSet2Message (Tipo 41)

**Propósito**: El cliente publica el LeaseSet en la base de datos de la red

**Contenido**: - ID de sesión - byte de tipo de LeaseSet (1, 3, 5 o 7) - LeaseSet (estructura de I2P) o LeaseSet2 o EncryptedLeaseSet o MetaLeaseSet - Número de claves privadas - Lista de claves privadas (una por clave pública en LeaseSet, mismo orden)

**Claves privadas**: Necesarias para descifrar los garlic messages (mensajes encapsulados de I2P) entrantes. Formato:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Nota**: Sustituye el CreateLeaseSetMessage obsoleto (tipo 4), que no admite: - Variantes de LeaseSet2 - Cifrado distinto de ElGamal - Múltiples tipos de cifrado - LeaseSets cifrados - Claves de firma sin conexión

#### SendMessageExpiresMessage (Tipo 36)

**Propósito**: Enviar un mensaje al destino con expiración y opciones avanzadas

**Contenido**: - ID de sesión - Destino - Carga útil (comprimida con gzip) - Nonce (4 bytes) - Indicadores (2 bytes) - ver más abajo - Fecha de expiración (6 bytes, truncada de 8)

**Campo de banderas** (2 bytes, orden de bits 15...0):

**Bits 15-11**: No utilizados, deben ser 0

**Bits 10-9**: Anulación de la fiabilidad del mensaje (sin uso, usar nonce (número de un solo uso) en su lugar)

**Bit 8**: No empaquetar LeaseSet - 0: Router puede empaquetar LeaseSet en garlic (técnica de cifrado de I2P) - 1: No empaquetar LeaseSet

**Bits 7-4**: Umbral bajo de etiquetas (solo ElGamal, se ignora en ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bits 3-0**: Etiquetas que enviar si es necesario (solo para ElGamal, se ignora en ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Tipo 22)

**Propósito**: Notificar al cliente sobre el estado de entrega del mensaje

**Contenido**: - ID de sesión - ID de mensaje (generado por el router) - Código de estado (1 byte) - Tamaño (4 bytes, solo relevante para status=0) - Nonce (4 bytes, coincide con el nonce de SendMessage del cliente)

**Códigos de estado** (Mensajes salientes):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Códigos de éxito**: 1, 2, 4, 6 **Códigos de error**: Todos los demás

**Código de estado 0** (EN DESUSO): Mensaje disponible (entrante, recepción rápida deshabilitada)

#### HostLookupMessage (mensaje de búsqueda de host) (Tipo 38)

**Propósito**: Consultar destino por nombre de host o hash (reemplaza DestLookup)

**Contenido**: - ID de sesión (o 0xFFFF si no hay sesión) - ID de solicitud (4 bytes) - Tiempo de espera en milisegundos (4 bytes, mínimo recomendado: 10000) - Tipo de solicitud (1 byte) - Clave de búsqueda (Hash, cadena de nombre de host, o Destino)

**Tipos de solicitud**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Los tipos 2-4 devuelven opciones de LeaseSet (propuesta 167) si están disponibles.

**Respuesta**: HostReplyMessage

#### HostReplyMessage (Tipo 39)

**Propósito**: Respuesta a HostLookupMessage (mensaje de búsqueda de host)

**Contenido**: - ID de sesión - ID de solicitud - Código de resultado (1 byte) - Destino (presente en caso de éxito, a veces en fallos específicos) - Mapeo (solo para tipos de búsqueda 2-4, puede estar vacío)

**Códigos de resultado**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (mensaje de información de blinding) (Tipo 42)

**Propósito**: Informar al router sobre los requisitos de autenticación de blinded destination (destino cegado) (desde 0.9.43)

**Contenido**: - ID de sesión - Indicadores (1 byte) - Tipo de endpoint (extremo) (1 byte): 0=Hash, 1=nombre de host, 2=Destination (destino en I2P), 3=SigType+Key - Tipo de firma ciega (2 bytes) - Expiración (4 bytes, segundos desde la época Unix) - Datos del endpoint (varía según el tipo) - Clave privada (32 bytes, solo si el bit 0 de los indicadores está activado) - Contraseña de consulta (cadena, solo si el bit 4 de los indicadores está activado)

**Indicadores** (orden de bits 76543210):

- **Bit 0**: 0=todos, 1=por cliente
- **Bits 3-1**: Esquema de autenticación (si el bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=se requiere secreto
- **Bits 7-5**: No utilizado, establecer en 0

**Sin respuesta**: El Router procesa en silencio

**Caso de uso**: Antes de enviar a un destino cegado (b33 address), el cliente debe hacer una de las dos cosas: 1. Consultar la dirección b33 mediante HostLookup, O 2. Enviar el mensaje BlindingInfo

Si el destino requiere autenticación, BlindingInfo (información de cegamiento) es obligatorio.

#### ReconfigureSessionMessage (Tipo 2)

**Propósito**: Actualizar la configuración de la sesión después de su creación

**Contenido**: - ID de sesión - SessionConfig (solo se necesitan las opciones cambiadas)

**Respuesta**: SessionStatusMessage (status=Updated o Invalid)

**Notas**: - El router fusiona la nueva configuración con la existente - Las opciones de Tunnel (`inbound.*`, `outbound.*`) se aplican siempre - Algunas opciones pueden ser inmutables después de la creación de la sesión - La fecha debe estar dentro de ±30 segundos del tiempo del router - El mapeo debe estar ordenado por clave

#### DestroySessionMessage (Tipo 3)

**Propósito**: Finalizar una sesión

**Contenido**: ID de sesión

**Respuesta esperada**: SessionStatusMessage (mensaje de estado de la sesión) (status=Destroyed)

**Comportamiento real** (Java I2P hasta la versión 0.9.66): - Router nunca envía SessionStatus(Destroyed) - Si no quedan sesiones: Envía DisconnectMessage - Si quedan subsesiones: Sin respuesta

**Importante**: el comportamiento de Java I2P se desvía de la especificación. Las implementaciones deben ser cautelosas al destruir subsesiones individuales.

#### DisconnectMessage (Tipo 30)

**Propósito**: Notificar que la conexión está a punto de finalizar

**Contenido**: Motivo (cadena)

**Efecto**: Todas las sesiones en la conexión se destruyen, el socket se cierra

**Implementación**: Principalmente router → cliente en Java I2P

## Historial de versiones del protocolo

### Detección de versiones

La versión del protocolo I2CP se intercambia en los mensajes Get/SetDate (desde 0.8.7). Para routers más antiguos, la información de la versión no está disponible.

**Cadena de versión**: Indica la versión de la API "core" (núcleo), no necesariamente la versión del router.

### Cronología de funcionalidades

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Consideraciones de seguridad

### Autenticación

**Predeterminado**: No se requiere autenticación **Opcional**: Autenticación con nombre de usuario/contraseña (desde 0.9.11) **Obligatorio**: Cuando está habilitado, la autenticación debe completarse antes de otros mensajes (desde 0.9.16)

**Conexiones remotas**: Utilice siempre TLS (`i2cp.SSL=true`) para proteger las credenciales y las claves privadas.

### Desfase del reloj

SessionConfig Date debe estar dentro de ±30 segundos de la hora del router, o la sesión será rechazada. Use Get/SetDate para sincronizar.

### Gestión de claves privadas

CreateLeaseSet2Message (mensaje para crear un LeaseSet2) contiene claves privadas para descifrar mensajes entrantes. Estas claves deben ser: - Transmitidas de forma segura (TLS para conexiones remotas) - Almacenadas de forma segura por el router - Rotadas cuando estén comprometidas

### Expiración del mensaje

Utiliza siempre SendMessageExpires (no SendMessage) para establecer una expiración explícita. Esto: - Evita que los mensajes queden en cola indefinidamente - Reduce el consumo de recursos - Mejora la fiabilidad

### Gestión de etiquetas de sesión

**ElGamal** (obsoleto): - Las etiquetas deben transmitirse en lotes - La pérdida de etiquetas provoca fallos de descifrado - Sobrecarga de memoria elevada

**ECIES-X25519** (actual): - Etiquetas generadas mediante un generador de números pseudoaleatorios sincronizado (PRNG) - No se requiere transmisión previa - Resistente a la pérdida de mensajes - Sobrecarga significativamente menor

## Mejores prácticas

### Para desarrolladores de clientes

1. **Usa el modo de recepción rápida**: Establece siempre `i2cp.fastReceive=true` (o confía en el valor predeterminado)

2. **Prefiera ECIES-X25519**: (suite de cifrado ECIES con X25519) Configure `i2cp.leaseSetEncType=4,0` para obtener el mejor rendimiento manteniendo compatibilidad

3. **Establecer expiración explícita**: Usa SendMessageExpires, no SendMessage

4. **Gestiona las Subsessions con cuidado**: Ten en cuenta que las subsessions (subsesiones, sesiones secundarias asociadas a un mismo destino) no ofrecen anonimato entre destinos

5. **Tiempo de espera en la creación de la sesión**: Destruir la sesión si no se recibe RequestVariableLeaseSet en un plazo de 5 minutos

6. **Ordenar mapeos de configuración**: Ordene siempre las claves del Mapping antes de firmar SessionConfig

7. **Usa recuentos de tunnel adecuados**: No configures `quantity` > 6 a menos que sea necesario

8. **Considere SAM/BOB para entornos no Java**: Implemente SAM en lugar de I2CP directamente

### Para desarrolladores del router

1. **Validar fechas**: Aplicar una ventana de ±30 segundos en las fechas de SessionConfig

2. **Limitar el tamaño del mensaje**: Aplicar un tamaño máximo de ~64 KB

3. **Soporte para múltiples sesiones**: Implementar soporte de subsesiones según la especificación 0.9.21

4. **Enviar RequestVariableLeaseSet de inmediato**: Solo después de que existan ambos tunnels, entrantes y salientes

5. **Gestionar mensajes obsoletos**: Aceptar pero desaconsejar ReceiveMessageBegin/End

6. **Soporte para ECIES-X25519 (ECIES con curva X25519)**: Priorizar el cifrado de tipo 4 para nuevos despliegues

## Depuración y solución de problemas

### Problemas comunes

**Sesión rechazada (inválida)**: - Compruebe el desfase del reloj (debe estar dentro de ±30 segundos) - Verifique que el mapeo esté ordenado por clave - Asegúrese de que el Destino no esté ya en uso

**Sin RequestVariableLeaseSet**: - El Router puede estar construyendo tunnels (espere hasta 5 minutos) - Compruebe si hay problemas de conectividad de red - Verifique que haya suficientes conexiones con pares

**Errores en la entrega de mensajes**: - Revise los códigos de MessageStatus para conocer el motivo específico del fallo - Verifique que el LeaseSet remoto esté publicado y actualizado - Asegúrese de que los tipos de cifrado sean compatibles

**Problemas de subsesión**: - Verifica que la sesión primaria se cree primero - Confirma que se usen las mismas claves de cifrado - Comprueba que las claves de firma sean distintas

### Mensajes de diagnóstico

**GetBandwidthLimits**: Consultar la capacidad del router **HostLookup**: Probar la resolución de nombres y la disponibilidad del LeaseSet **MessageStatus**: Rastrear la entrega de mensajes de extremo a extremo

## Especificaciones relacionadas

- **Estructuras comunes**: /docs/specs/common-structures/
- **I2NP (Protocolo de red)**: /docs/specs/i2np/
- **ECIES-X25519 (esquema ECIES con curva X25519)**: /docs/specs/ecies/
- **Creación de tunnel**: /docs/specs/implementation/
- **Biblioteca de streaming**: /docs/specs/streaming/
- **Biblioteca de datagramas**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Propuestas referenciadas

- [Propuesta 123](/proposals/123-new-netdb-entries/): LeaseSets cifrados y autenticación
- [Propuesta 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Propuesta 149](/proposals/149-b32-encrypted-ls2/): Formato de dirección cegada (b33)
- [Propuesta 152](/proposals/152-ecies-tunnels/): Creación de tunnel X25519
- [Propuesta 154](/proposals/154-ecies-lookups/): Búsquedas en base de datos desde destinos ECIES
- [Propuesta 156](/proposals/156-ecies-routers/): Migración del router a ECIES-X25519
- [Propuesta 161](/es/proposals/161-ri-dest-padding/): Compresión del relleno de destino
- [Propuesta 167](/proposals/167-service-records/): Registros de servicio de LeaseSet
- [Propuesta 169](/proposals/169-pq-crypto/): Criptografía híbrida poscuántica (ML-KEM)

## Referencia de Javadocs

- [Paquete de I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [API del cliente](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Resumen de deprecación

### Mensajes obsoletos (No usar)

- **CreateLeaseSetMessage** (tipo 4): Utilice CreateLeaseSet2Message
- **RequestLeaseSetMessage** (tipo 21): Utilice RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (tipo 6): Utilice el modo de recepción rápida
- **ReceiveMessageEndMessage** (tipo 7): Utilice el modo de recepción rápida
- **DestLookupMessage** (tipo 34): Utilice HostLookupMessage
- **DestReplyMessage** (tipo 35): Utilice HostReplyMessage
- **ReportAbuseMessage** (tipo 29): Nunca implementado

### Opciones obsoletas

- Cifrado ElGamal (tipo 0): Migrar a ECIES-X25519 (tipo 4)
- Firmas DSA: Migrar a EdDSA o ECDSA
- `i2cp.fastReceive=false`: Usar siempre el modo de recepción rápida
