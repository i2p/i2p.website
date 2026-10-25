---
title: "I2P Client Protocol (I2CP)"
description: "Cómo las aplicaciones negocian sesiones, tunnels y LeaseSets con el router I2P."
slug: "i2cp"
aliases:
  - "/es/docs/api/i2cp"
  - "/es/docs/api/i2cp/"
  - "/es/docs/specs/i2cp-spec"
  - "/es/docs/specs/i2cp-spec/"
category: "Protocolos"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Descripción general

Esta es la especificación del I2CP (Protocolo de Control I2P), la interfaz de bajo nivel entre los clientes y el router. Los clientes Java utilizarán la API de cliente I2CP, que implementa este protocolo.

No existen implementaciones conocidas que no sean en Java de una biblioteca del lado del cliente que implemente I2CP. Además, las aplicaciones orientadas a sockets (streaming) necesitarían una implementación del protocolo de streaming, pero tampoco existen bibliotecas que no sean en Java para eso. Por lo tanto, los clientes que no usan Java deberían utilizar en su lugar el protocolo de capa superior SAM [SAMv3](/docs/api/samv3/), para el cual existen bibliotecas en varios lenguajes.

Este es un protocolo de bajo nivel soportado tanto interna como externamente por el router I2P de Java. El protocolo solo se serializa si el cliente y el router no están en la misma JVM; de lo contrario, los objetos Java de mensajes I2CP se pasan a través de una interfaz JVM interna. I2CP también es soportado externamente por el router de C++ i2pd.

Más información está disponible en la página de Resumen de I2CP [I2CP](/docs/specs/i2cp/).

## Sesiones

El protocolo fue diseñado para manejar múltiples "sesiones", cada una con un ID de sesión de 2 bytes, sobre una única conexión TCP; sin embargo, las sesiones múltiples no fueron implementadas hasta la versión 0.9.21. Consulta la [sección de multisesión más abajo](#multisession). No intentes usar múltiples sesiones en una única conexión I2CP con routers anteriores a la versión 0.9.21.

También parece que hay algunas disposiciones para que un solo cliente se comunique con múltiples routers a través de conexiones separadas. Esto también está sin probar y probablemente no sea útil.

No hay forma de mantener una sesión después de una desconexión, o de recuperarla en una conexión I2CP diferente. Cuando se cierra el socket, la sesión se destruye.

## Secuencias de Mensajes de Ejemplo

Nota: Los ejemplos a continuación no muestran el Byte de Protocolo (0x2a) que debe ser enviado desde el cliente al router al conectarse por primera vez. Más información sobre la inicialización de conexión está en la página de Descripción General de I2CP [I2CP](/docs/specs/i2cp/).

### Establecimiento de Sesión Estándar

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Obtener Límites de Ancho de Banda (Sesión Simple)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Búsqueda de Destino (Sesión Simple)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Mensaje Saliente

Sesión existente, con i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Sesión existente, con i2cp.messageReliability=none y nonce diferente de cero

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Sesión existente, con i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Mensaje Entrante

Sesión existente, con i2cp.fastReceive=true (a partir de 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Sesión existente, con i2cp.fastReceive=false (OBSOLETO)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Notas sobre Multisesión {#multisession}

Se admiten múltiples sesiones en una sola conexión I2CP a partir de la versión 0.9.21 del router. La primera sesión que se crea es la "sesión principal". Las sesiones adicionales son "subsesiones". Las subsesiones se utilizan para admitir múltiples destinos que comparten un conjunto común de túneles. La aplicación inicial es que la sesión principal use claves de firma ECDSA, mientras que la subsesión use claves de firma DSA para la comunicación con eepsites antiguos.

Las subsesiones comparten los mismos pools de túneles de entrada y salida que la sesión primaria. Las subsesiones deben usar las mismas claves de cifrado que la sesión primaria. Esto se aplica tanto a las claves de cifrado del leaseSet como a las claves de cifrado del Destination (no utilizadas). Las subsesiones deben usar diferentes claves de firma en el destination, por lo que el hash del destination es diferente al de la sesión primaria. Como las subsesiones usan las mismas claves de cifrado y túneles que la sesión primaria, es evidente para todos que los Destinations están ejecutándose en el mismo router, por lo que las garantías usuales de anonimato anti-correlación no se aplican.

Las subsesiones se crean enviando un mensaje CreateSession y recibiendo un mensaje SessionStatus como respuesta, como es habitual. Las subsesiones deben crearse después de que se haya creado la sesión principal. La respuesta SessionStatus contendrá, en caso de éxito, un ID de sesión único, distinto del ID de la sesión principal. Aunque los mensajes CreateSession deberían procesarse en orden, no hay una forma segura de correlacionar un mensaje CreateSession con la respuesta, por lo que un cliente no debería tener múltiples mensajes CreateSession pendientes simultáneamente. Las opciones de SessionConfig para la subsesión pueden no ser respetadas cuando difieren de la sesión principal. En particular, dado que las subsesiones usan el mismo conjunto de túneles que la sesión principal, las opciones de túnel pueden ser ignoradas.

El router enviará mensajes RequestVariableLeaseSet separados para cada Destination al cliente, y el cliente debe responder con un mensaje CreateLeaseSet para cada uno. Los leases para los dos Destinations no serán necesariamente idénticos, aunque sean seleccionados del mismo pool de túneles.

Una subsesión puede ser destruida con el mensaje DestroySession como es habitual. Esto no destruirá la sesión principal ni detendrá la conexión I2CP. Sin embargo, destruir la sesión principal sí destruirá todas las subsesiones y detendrá la conexión I2CP. Un mensaje Disconnect destruye todas las sesiones.

Tenga en cuenta que la mayoría, pero no todos, los mensajes I2CP contienen un Session ID. Para aquellos que no lo tienen, los clientes pueden necesitar lógica adicional para manejar adecuadamente las respuestas del router. DestLookup y DestReply no contienen Session IDs; use en su lugar los más recientes HostLookup y HostReply. GetBandwidthLimts y BandwidthLimits no contienen session IDs, sin embargo la respuesta no es específica de la sesión.

### Notas de Versión {#notes}

El byte inicial de versión del protocolo (0x2a) enviado por el cliente no se espera que cambie. Antes de la versión 0.8.7, la información de versión del router no estaba disponible para el cliente, lo que impedía que los nuevos clientes funcionaran con routers antiguos. A partir de la versión 0.8.7, las cadenas de versión del protocolo de ambas partes se intercambian en los mensajes Get/Set Date. En adelante, los clientes pueden usar esta información para comunicarse correctamente con routers antiguos. Los clientes y routers no deben enviar mensajes que no sean compatibles con la otra parte, ya que generalmente desconectan la sesión al recibir un mensaje no compatible.

La información de versión intercambiada es la versión de la API "core" o la versión del protocolo I2CP, y no es necesariamente la versión del router.

Un resumen básico de las versiones del protocolo I2CP es el siguiente. Para más detalles, ver abajo.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Estructuras comunes {#structures}

### Encabezado de mensaje I2CP {#struct-I2CPMessageHeader}

#### Descripción

Encabezado común para todos los mensajes I2CP, que contiene la longitud del mensaje y el tipo de mensaje.

#### Contenidos

1.  4 bytes [Integer](/docs/specs/common-structures/#integer) especificando la longitud del
    cuerpo del mensaje
2.  1 byte [Integer](/docs/specs/common-structures/#integer) especificando el tipo de
    mensaje.
3.  El cuerpo del mensaje I2CP, 0 o más bytes

#### Notas

El límite real de longitud de mensaje es de aproximadamente 64 KB.

### ID del Mensaje {#struct-MessageId}

#### Descripción

Identifica de manera única un mensaje esperando en un router particular en un momento determinado. Esto siempre es generado por el router y NO es lo mismo que el nonce generado por el cliente.

#### Contenidos

1.  4 bytes [Integer](/docs/specs/common-structures/#integer)

#### Notas

Los IDs de mensaje son únicos solo dentro de una sesión; no son globalmente únicos.

### Payload {#struct-Payload}

#### Descripción

Esta estructura es el contenido de un mensaje que se está entregando de un Destination a otro.

#### Contenido

1.  4 bytes [Integer](/docs/specs/common-structures/#integer) longitud
2.  Esa cantidad de bytes

#### Notas

La carga útil está en formato gzip como se especifica en la página de Resumen de I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

El límite real de longitud de mensaje es de aproximadamente 64 KB.

### Configuración de Sesión {#struct-SessionConfig}

#### Descripción

Define las opciones de configuración para una sesión de cliente particular.

#### Contenidos

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) de opciones
3.  [Date](/docs/specs/common-structures/#date) de creación
4.  [Signature](/docs/specs/common-structures/#signature) de los 3 campos anteriores,
    firmada por la [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Notas

- Las opciones se especifican en la página de Descripción General de I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- El [Mapping](/docs/specs/common-structures/#mapping) debe estar ordenado por clave para que
  la firma sea validada correctamente en el router.
- La fecha de creación debe estar dentro de +/- 30 segundos de la hora actual
  cuando sea procesada por el router, o la configuración será rechazada.

#### Firmas sin conexión

- Si el [Destination](/docs/specs/common-structures/#destination) está firmado offline,
  el [Mapping](/docs/specs/common-structures/#mapping) debe contener las tres opciones
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, y
  i2cp.leaseSetOfflineSignature. La
  [Signature](/docs/specs/common-structures/#signature) se genera entonces por la
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) transitoria y
  se verifica con la
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) especificada en
  i2cp.leaseSetTransientPublicKey. Ver
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) para detalles.

### ID de Sesión {#struct-SessionId}

#### Descripción

Identifica de manera única una sesión en un router particular en un momento determinado.

#### Contenidos

1.  2 bytes [Integer](/docs/specs/common-structures/#integer)

#### Notas

El ID de sesión 0xffff se usa para indicar "sin sesión", por ejemplo para búsquedas de nombres de host.

## Mensajes

Consulta también la [documentación de I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Tipos de Mensaje {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Descripción

Informar al cliente cuáles son los límites de ancho de banda.

Enviado desde el Router al Cliente en respuesta a un [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Contenidos

1.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de entrada del cliente
    (KBps)
2.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de salida del cliente
    (KBps)
3.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de entrada del router
    (KBps)
4.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de ráfaga de entrada del router
    (KBps)
5.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de salida del router
    (KBps)
6.  4 bytes [Integer](/docs/specs/common-structures/#integer) Límite de ráfaga de salida del router
    (KBps)
7.  4 bytes [Integer](/docs/specs/common-structures/#integer) Tiempo de ráfaga del router
    (segundos)
8.  Nueve [Integer](/docs/specs/common-structures/#integer) de 4 bytes (indefinido)

#### Notas

Los límites del cliente pueden ser los únicos valores establecidos, y pueden ser los límites reales del router, o un porcentaje de los límites del router, o específicos para el cliente en particular, dependiendo de la implementación. Todos los valores etiquetados como límites del router pueden ser 0, dependiendo de la implementación. A partir de la versión 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Descripción

Advierte al router que un Destino está oculto, con contraseña de búsqueda opcional y clave privada opcional para descifrado. Consulta las propuestas 123 y 149 para más detalles.

El router necesita saber si un destino está cegado. Si está cegado y utiliza una autenticación secreta o por cliente, también necesita tener esa información.

Un Host Lookup de una dirección b32 de nuevo formato ("b33") le dice al router que la dirección está ciega, pero no hay un mecanismo para pasar la clave secreta o privada al router en el mensaje Host Lookup. Aunque podríamos extender el mensaje Host Lookup para agregar esa información, es más limpio definir un nuevo mensaje.

Este mensaje proporciona una forma programática para que el cliente le diga al router. De lo contrario, el usuario tendría que configurar manualmente cada destino.

#### Uso

Antes de que un cliente envíe un mensaje a un destino cegado, debe buscar el "b33" en un mensaje de Host Lookup, o enviar un mensaje de Blinding Info. Si el destino cegado requiere un secreto o autenticación por cliente, el cliente debe enviar un mensaje de Blinding Info.

El router no envía una respuesta a este mensaje. Enviado del Cliente al Router.

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Orden de bits: 76543210 > - Bit 0: 0 para todos, 1 para por-cliente > - Bits 3-1: Esquema de autenticación, si el bit 0 está establecido en 1 para >   por-cliente, de lo contrario 000 >   - 000: Autenticación de cliente DH (o sin autenticación por-cliente) >   - 001: Autenticación de cliente PSK > - Bit 4: 1 si se requiere secreto, 0 si no se requiere secreto > - Bits 7-5: Sin usar, establecer en 0 para compatibilidad futura

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Tipo de endpoint

> - Tipo 0 es un [Hash](/docs/specs/common-structures/#hash) > - Tipo 1 es un nombre de host [String](/docs/specs/common-structures/#string) > - Tipo 2 es un [Destination](/docs/specs/common-structures/#destination) > - Tipo 3 es un Sig Type y >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  [Integer](/docs/specs/common-structures/#integer) de 2 bytes Tipo de Firma Ciega
5.  [Integer](/docs/specs/common-structures/#integer) de 4 bytes Segundos de Expiración desde
    época
6.  Endpoint: Datos como se especifica, uno de

> - Tipo 0: 32 bytes [Hash](/docs/specs/common-structures/#hash) > > - Tipo 1: nombre de host [String](/docs/specs/common-structures/#string) > > - Tipo 2: [Destination](/docs/specs/common-structures/#destination) binario > >  > >  - Tipo 3: 2 bytes [Integer](/docs/specs/common-structures/#integer) tipo de firma, seguido de > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (longitud como >       implica el tipo de firma)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Clave de descifrado Solo presente
    si el bit de bandera 0 está establecido en 1. Una clave privada ECIES_X25519 de 32 bytes,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Contraseña de búsqueda Solo presente si
    el bit de bandera 4 está establecido en 1.

#### Notas

- A partir de la versión 0.9.43.
- El tipo de endpoint Hash probablemente no es útil a menos que el router pueda hacer
  una búsqueda inversa en la libreta de direcciones para obtener el Destination.
- El tipo de endpoint hostname probablemente no es útil a menos que el router
  pueda hacer una búsqueda en la libreta de direcciones para obtener el Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

OBSOLETO. No se puede usar para LeaseSet2, claves fuera de línea, tipos de cifrado que no sean ElGamal, múltiples tipos de cifrado, o LeaseSets cifrados. Use CreateLeaseSet2Message con todos los routers 0.9.39 o superior.

#### Descripción

Este mensaje se envía en respuesta a un [RequestLeaseSetMessage](#RequestLeaseSetMessage) o [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) y contiene todas las estructuras [Lease](/docs/specs/common-structures/#lease) que deben publicarse en la Base de Datos de Red I2NP.

Enviado del Cliente al Router.

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) o 20
    bytes ignorados
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notas

La SigningPrivateKey coincide con la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) del leaseSet, solo si el tipo de clave de firma es DSA. Esto es para la revocación de leaseSet, que no está implementada y es poco probable que se implemente alguna vez. Si el tipo de clave de firma no es DSA, este campo contiene 20 bytes de datos aleatorios. La longitud de este campo es siempre de 20 bytes, nunca es igual a la longitud de una clave privada de firma que no sea DSA.

La PrivateKey coincide con la [PublicKey](/docs/specs/common-structures/#publickey) del LeaseSet. La PrivateKey es necesaria para descifrar mensajes enrutados con garlic encryption.

La revocación no está implementada. La conexión a múltiples routers no está implementada en ninguna biblioteca de cliente.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Descripción

Este mensaje se envía en respuesta a un [RequestLeaseSetMessage](#RequestLeaseSetMessage) o [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) y contiene todas las estructuras [Lease](/docs/specs/common-structures/#lease) que deberían publicarse en la Network Database de I2NP.

Enviado del Cliente al Router. Desde la versión 0.9.39. Autenticación por cliente para EncryptedLeaseSet compatible desde la 0.9.41. MetaLeaseSet aún no es compatible a través de I2CP. Ver propuesta 123 para más información.

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  Un byte tipo de leaseSet a seguir.

> - Tipo 1 es un [LeaseSet](/docs/specs/common-structures/#leaseset) (obsoleto) > - Tipo 3 es un [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Tipo 5 es un [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Tipo 7 es un [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) o
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) o
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) o
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Un byte con el número de claves privadas a continuación.
5.  Lista de [PrivateKey](/docs/specs/common-structures/#privatekey). Una para cada clave
    pública en el lease set, en el mismo orden. (No presente para Meta LS2)

> - Tipo de cifrado (2 bytes [Integer](/docs/specs/common-structures/#integer)) > - Longitud de clave de cifrado (2 bytes [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) de cifrado (número de bytes >   especificado)

#### Notas

Las PrivateKeys coinciden con cada una de las [PublicKey](/docs/specs/common-structures/#publickey) del LeaseSet. Las PrivateKeys son necesarias para descifrar los mensajes enrutados con garlic encryption.

Ver la propuesta 123 para más información sobre LeaseSets cifrados.

El contenido y formato para MetaLeaseSet son preliminares y están sujetos a cambios. No hay un protocolo especificado para la administración de múltiples routers. Consulta la propuesta 123 para más información.

La clave privada de firma, previamente definida para revocación y sin usar, no está presente en LS2.

La versión preliminar con tipo de mensaje 40 estaba en 0.9.38 pero el formato fue cambiado. El tipo 40 está abandonado y no es compatible. El tipo 41 no es válido hasta 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Descripción

Este mensaje es enviado desde un cliente para iniciar una sesión, donde una sesión se define como la conexión de un solo Destination a la red, a la cual todos los mensajes para ese Destination serán entregados y desde la cual todos los mensajes que ese Destination envía a cualquier otro Destination serán enviados.

Enviado del Cliente al Router. El router responde con un [SessionStatusMessage](#SessionStatusMessage).

#### Contenidos

1.  [Configuración de Sesión](#struct-sessionconfig)

#### Notas

- Este es el segundo mensaje enviado por el cliente. Previamente el cliente
  envió un [GetDateMessage](#GetDateMessage) y recibió una
  respuesta [SetDateMessage](#SetDateMessage).
- Si la Fecha en la Configuración de Sesión está demasiado alejada (más de +/- 30
  segundos) de la hora actual del router, la sesión será
  rechazada.
- Si ya existe una sesión en el router para este Destination, la
  sesión será rechazada.
- El [Mapping](/docs/specs/common-structures/#mapping) en la Configuración de Sesión debe estar
  ordenado por clave para que la firma sea validada correctamente en el
  router.

### DestLookupMessage {#DestLookupMessage}

#### Descripción

Enviado del Cliente al Router. El router responde con un [DestReplyMessage](#DestReplyMessage).

#### Contenido

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notas

A partir de la versión 0.7.

A partir de la versión 0.8.3, se admiten múltiples búsquedas pendientes, y las búsquedas son compatibles tanto en I2PSimpleSession como en sesiones estándar.

[HostLookupMessage](#HostLookupMessage) es preferido a partir de la versión 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Descripción

Enviado desde el Router al Cliente en respuesta a un [DestLookupMessage](#DestLookupMessage).

#### Contenidos

1.  [Destination](/docs/specs/common-structures/#destination) en caso de éxito, o
    [Hash](/docs/specs/common-structures/#hash) en caso de fallo

#### Notas

A partir de la versión 0.7.

A partir del lanzamiento 0.8.3, se devuelve el Hash solicitado si la búsqueda falló, para que el cliente pueda tener múltiples búsquedas pendientes y correlacionar las respuestas con las búsquedas. Para correlacionar una respuesta de Destination con una solicitud, toma el Hash del Destination. Antes del lanzamiento 0.8.3, la respuesta estaba vacía en caso de fallo.

### DestroySessionMessage {#DestroySessionMessage}

#### Descripción

Este mensaje es enviado desde un cliente para destruir una sesión.

Enviado desde Cliente a Router. El router debería responder con un [SessionStatusMessage](#SessionStatusMessage) (Destroyed). Sin embargo, consulta las notas importantes a continuación.

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)

#### Notas

En este punto, el router debería liberar todos los recursos relacionados con la sesión.

Hasta la API 0.9.66, el router I2P de Java y las bibliotecas cliente se desvían sustancialmente de esta especificación. El router nunca envía una respuesta SessionStatus(Destroyed). Si no quedan sesiones, envía un [DisconnectMessage](#DisconnectMessage). Si hay subsesiones o la sesión primaria permanece, no responde.

La biblioteca cliente de Java responde a un mensaje SessionStatus destruyendo todas las sesiones y reconectándose.

Destruir subsesiones individuales en una conexión con múltiples sesiones puede no estar completamente probado o funcionando en varias implementaciones de router y cliente. Úselo con precaución.

Las implementaciones deberían tratar una destrucción para una sesión primaria como una destrucción para todas las subsesiones, pero permitir una destrucción para una sola subsesión y mantener la conexión abierta, pero Java I2P no hace eso actualmente. Si el comportamiento de Java I2P cambia en versiones posteriores, se documentará aquí.

### DisconnectMessage {#DisconnectMessage}

#### Descripción

Informa a la otra parte que hay problemas y que la conexión actual está a punto de ser destruida. Esto termina todas las sesiones en esa conexión. El socket se cerrará en breve. Enviado ya sea del router al cliente o del cliente al router.

#### Contenidos

1.  Razón [String](/docs/specs/common-structures/#string)

#### Notas

Solo implementado en la dirección del router al cliente, al menos en Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Descripción

Solicitar que el router indique cuáles son sus límites de ancho de banda actuales.

Enviado del Cliente al Router. El router responde con un [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Contenidos

*Ninguno*

#### Notas

A partir de la versión 0.7.2.

A partir de la versión 0.8.3, compatible tanto en I2PSimpleSession como en sesiones estándar.

### GetDateMessage {#GetDateMessage}

#### Descripción

Enviado del Cliente al Router. El router responde con un [SetDateMessage](#SetDateMessage).

#### Contenidos

1.  Versión de la API I2CP [String](/docs/specs/common-structures/#string)
2.  Autenticación [Mapping](/docs/specs/common-structures/#mapping) (opcional, a partir de
    la versión 0.9.11)

#### Notas

- Generalmente el primer mensaje enviado por el cliente después de enviar
  el byte de versión del protocolo.
- La cadena de versión se incluye a partir de la versión 0.8.7. Esto solo
  es útil si el cliente y el router no están en la misma JVM. Si no está
  presente, el cliente es versión 0.8.6 o anterior.
- A partir de la versión 0.9.11, la autenticación
  [Mapping](/docs/specs/common-structures/#mapping) puede incluirse, con las claves
  i2cp.username e i2cp.password. El Mapping no necesita estar ordenado ya que
  este mensaje no está firmado. Antes y hasta la versión 0.9.10 inclusive,
  la autenticación se incluye en el
  [Session Config](#struct-sessionconfig) Mapping, y no se aplica autenticación para
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), o
  [DestLookupMessage](#DestLookupMessage). Cuando está habilitada, la autenticación
  vía [GetDateMessage](#GetDateMessage) es requerida antes que cualquier otro
  mensaje a partir de la versión 0.9.16. Esto solo es útil fuera del contexto del
  router. Este es un cambio incompatible, pero solo afectará sesiones
  fuera del contexto del router con autenticación, lo cual debería ser raro.

### HostLookupMessage {#HostLookupMessage}

#### Descripción

Enviado del Cliente al Router. El router responde con un [HostReplyMessage](#HostReplyMessage).

Esto reemplaza el [DestLookupMessage](#DestLookupMessage) y añade un ID de solicitud, un tiempo de espera y soporte para búsqueda de nombres de host. Como también soporta búsquedas Hash, puede utilizarse para todas las búsquedas si el router lo admite. Para búsquedas de nombres de host, el router consultará el servicio de nombres de su contexto. Esto solo es útil si el cliente está fuera del contexto del router. Dentro del contexto del router, el cliente debería consultar el servicio de nombres directamente, lo cual es mucho más eficiente.

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  [Integer](/docs/specs/common-structures/#integer) de 4 bytes ID de solicitud
3.  [Integer](/docs/specs/common-structures/#integer) de 4 bytes timeout (ms)
4.  [Integer](/docs/specs/common-structures/#integer) de 1 byte tipo de solicitud
5.  [Hash](/docs/specs/common-structures/#hash) SHA-256 o nombre de host
    [String](/docs/specs/common-structures/#string) o
    [Destination](/docs/specs/common-structures/#destination)

Tipos de solicitud:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Los tipos 2-4 solicitan que el mapeo de opciones del LeaseSet sea devuelto en el mensaje HostReply. Ver propuesta 167.

#### Notas

- A partir de la versión 0.9.11. Usar [DestLookupMessage](#DestLookupMessage) para
  routers más antiguos.
- El ID de sesión y el ID de solicitud se devolverán en el
  [HostReplyMessage](#HostReplyMessage). Usar 0xFFFF para el ID de sesión
  si no hay sesión.
- El timeout es útil para búsquedas de Hash. Mínimo recomendado 10,000 (10
  seg.). En el futuro también puede ser útil para búsquedas de servicio de nombres
  remotos. El valor puede no ser respetado para búsquedas de nombres de host locales,
  que deberían ser rápidas.
- Se admite la búsqueda de nombres de host en Base 32 pero es preferible convertirlo
  a un Hash primero.

### HostReplyMessage {#HostReplyMessage}

#### Descripción

Enviado desde el Router al Cliente como respuesta a un [HostLookupMessage](#HostLookupMessage).

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  4 bytes [Integer](/docs/specs/common-structures/#integer) ID de solicitud
3.  1 byte [Integer](/docs/specs/common-structures/#integer) código de resultado

> - 0: Éxito > - 1: Fallo > - 2: Contraseña de búsqueda requerida (a partir de 0.9.43) > - 3: Clave privada requerida (a partir de 0.9.43) > - 4: Contraseña de búsqueda y clave privada requeridas (a partir de 0.9.43) > - 5: Fallo de descifrado del leaseSet (a partir de 0.9.43) > - 6: Fallo de búsqueda del leaseSet (a partir de 0.9.66) > - 7: Tipo de búsqueda no compatible (a partir de 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), solo presente si el código de resultado
    es cero, excepto que también puede ser devuelto para los tipos de búsqueda 2-4. Ver
    abajo.
5.  [Mapping](/docs/specs/common-structures/#mapping), solo presente si el código de resultado es
    cero, solo devuelto para los tipos de búsqueda 2-4. A partir de 0.9.66. Ver abajo.

#### Respuestas para tipos de búsqueda 2-4

La Propuesta 167 define tipos de búsqueda adicionales que devuelven todas las opciones del leaseSet, si están presentes. Para los tipos de búsqueda 2-4, el router debe obtener el leaseSet, incluso si la clave de búsqueda está en la libreta de direcciones.

Si es exitoso, el HostReply contendrá las opciones Mapping del leaseset, y las incluye como elemento 5 después del destino. Si no hay opciones en el Mapping, o el leaseset era versión 1, aún se incluirá como un Mapping vacío (dos bytes: 0 0). Se incluirán todas las opciones del leaseset, no solo las opciones de registro de servicio. Por ejemplo, pueden estar presentes opciones para parámetros definidos en el futuro. El Mapping devuelto puede o no estar ordenado, dependiente de la implementación.

En caso de fallo en la búsqueda de leaseSet, la respuesta contendrá un nuevo código de error 6 (Fallo en la búsqueda de leaseSet) y no incluirá un mapeo. Cuando se devuelve el código de error 6, el campo Destination puede estar presente o no. Estará presente si una búsqueda de nombre de host en la libreta de direcciones fue exitosa, o si una búsqueda anterior fue exitosa y el resultado fue almacenado en caché, o si el Destination estaba presente en el mensaje de búsqueda (tipo de búsqueda 4).

Si un tipo de búsqueda no es compatible, la respuesta contendrá un nuevo código de error 7 (tipo de búsqueda no compatible).

#### Notas

- A partir de la versión 0.9.11. Ver notas de [HostLookupMessage](#HostLookupMessage).
- El ID de sesión y el ID de solicitud son los del [HostLookupMessage](#HostLookupMessage).
- El código de resultado es 0 para éxito, 1-255 para fallo. 1 indica un fallo genérico. A partir de la versión 0.9.43, se definieron los códigos de fallo adicionales 2-5 para soportar errores extendidos para búsquedas "b33". Ver propuestas 123 y 149 para información adicional. A partir de la versión 0.9.66, se definieron los códigos de fallo adicionales 6-7 para soportar errores extendidos para búsquedas tipo 2-4. Ver propuesta 167 para información adicional.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Descripción

Entregar la carga útil de un mensaje al cliente.

Enviado del Router al Cliente. Si i2cp.fastReceive=true, que no es el valor por defecto, el cliente responde con un [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  [ID de Mensaje](#struct-messageid)
3.  [Carga Útil](#struct-payload)

#### Notas

### MessageStatusMessage {#MessageStatusMessage}

#### Descripción

Notifica al cliente sobre el estado de entrega de un mensaje entrante o saliente. Enviado del Router al Cliente. Si este mensaje indica que hay un mensaje entrante disponible, el cliente responde con un [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Para un mensaje saliente, esta es una respuesta a un [SendMessageMessage](#SendMessageMessage) o [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) generado por el router
3.  1 byte [Integer](/docs/specs/common-structures/#integer) estado
4.  4 byte [Integer](/docs/specs/common-structures/#integer) tamaño
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce generado previamente
    por el cliente

#### Notas

Hasta la versión 0.9.4, los valores de estado conocidos son 0 para mensaje disponible, 1 para aceptado, 2 para mejor esfuerzo exitoso, 3 para mejor esfuerzo fallido, 4 para garantizado exitoso, 5 para garantizado fallido. El Integer de tamaño especifica el tamaño del mensaje disponible y solo es relevante para status = 0. Aunque garantizado no está implementado (mejor esfuerzo es el único servicio), la implementación actual del router usa los códigos de estado garantizado, no los códigos de mejor esfuerzo.

A partir de la versión del router 0.9.5, se definen códigos de estado adicionales, sin embargo no están necesariamente implementados. Consulta los [Javadocs de MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) para más detalles. Para mensajes salientes, los códigos 1, 2, 4 y 6 indican éxito; todos los demás son fallos. Los códigos de fallo devueltos pueden variar y son específicos de la implementación.

Todos los códigos de estado:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Cuando status = 1 (aceptado), el nonce coincide con el nonce en el [SendMessageMessage](#SendMessageMessage), y el Message ID incluido se utilizará para notificaciones posteriores de éxito o fallo. De lo contrario, el nonce puede ser ignorado.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

OBSOLETO. No compatible con i2pd.

#### Descripción

Solicita al router que entregue un mensaje del cual fue previamente notificado. Enviado desde el Cliente al Router. El router responde con un [MessagePayloadMessage](#MessagePayloadMessage).

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  [ID de Mensaje](#struct-messageid)

#### Notas

El [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) se envía como respuesta a un [MessageStatusMessage](#MessageStatusMessage) que indica que hay un nuevo mensaje disponible para recoger. Si el id del mensaje especificado en el [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) es inválido o incorrecto, el router puede simplemente no responder, o puede enviar de vuelta un [DisconnectMessage](#DisconnectMessage).

Esto no se utiliza en el modo "recepción rápida", que es el predeterminado desde la versión 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

OBSOLETO. No soportado por i2pd.

#### Descripción

Informar al router que la entrega de un mensaje se completó exitosamente y que el router puede descartar el mensaje.

Enviado del Cliente al Router.

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  [ID de Mensaje](#struct-messageid)

#### Notas

El [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) se envía después de que un [MessagePayloadMessage](#MessagePayloadMessage) entrega completamente la carga útil de un mensaje.

Esto no se utiliza en el modo "fast receive" (recepción rápida), que es el predeterminado desde la versión 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Descripción

Enviado desde el Cliente al Router para actualizar la configuración de la sesión. El router responde con un [SessionStatusMessage](#SessionStatusMessage).

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  [Configuración de Sesión](#struct-sessionconfig)

#### Notas

- A partir de la versión 0.7.1.
- Si la Fecha en la Configuración de Sesión está muy alejada (más de +/- 30
  segundos) de la hora actual del router, la sesión será
  rechazada.
- El [Mapping](/docs/specs/common-structures/#mapping) en la Configuración de Sesión debe estar
  ordenado por clave para que la firma sea validada correctamente en el
  router.
- Algunas opciones de configuración solo pueden establecerse en el
  [CreateSessionMessage](#CreateSessionMessage), y los cambios aquí no
  serán reconocidos por el router. Los cambios a las opciones de tunnel inbound.\*
  y outbound.\* siempre son reconocidos.
- En general, el router debe fusionar la configuración actualizada con la
  configuración actual, por lo que la configuración actualizada solo necesita contener las
  opciones nuevas o modificadas. Sin embargo, debido a la fusión, las opciones no pueden ser
  eliminadas de esta manera; deben establecerse explícitamente al valor
  predeterminado deseado.

### ReportAbuseMessage {#ReportAbuseMessage}

OBSOLETO, NO UTILIZADO, SIN SOPORTE

#### Descripción

Informar a la otra parte (cliente o router) que está siendo atacada, potencialmente con referencia a un MessageId particular. Si el router está siendo atacado, el cliente puede decidir migrar a otro router, y si un cliente está siendo atacado, el router puede reconstruir sus routers o incluir en la lista de bloqueo algunos de los peers que le enviaron mensajes transmitiendo el ataque.

Enviado ya sea del router al cliente o del cliente al router.

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) severidad del abuso (0 es
    mínimamente abusivo, 255 siendo extremadamente abusivo)
3.  Razón [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notas

Sin usar. No completamente implementado. Tanto el router como el cliente pueden generar un [ReportAbuseMessage](#ReportAbuseMessage), pero ninguno tiene un controlador para el mensaje cuando se recibe.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

OBSOLETO. No soportado por i2pd. No enviado por Java I2P a clientes versión 0.9.7 o superior (2013-07). Usar RequestVariableLeaseSetMessage.

#### Descripción

Solicitar que un cliente autorice la inclusión de un conjunto particular de túneles de entrada. Enviado del Router al Cliente. El cliente responde con un [CreateLeaseSetMessage](#CreateLeaseSetMessage).

El primero de estos mensajes enviados en una sesión es una señal al cliente de que los tunnels están construidos y listos para el tráfico. El router no debe enviar el primero de estos mensajes hasta que al menos un tunnel de entrada Y uno de salida hayan sido construidos. Los clientes deben agotar el tiempo de espera y destruir la sesión si el primero de estos mensajes no se recibe después de cierto tiempo (recomendado: 5 minutos o más).

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) número de tunnels
3.  Ese número de pares de:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  [Date](/docs/specs/common-structures/#date) de finalización

#### Notas

Esto solicita un [LeaseSet](/docs/specs/common-structures/#leaseset) con todas las entradas [Lease](/docs/specs/common-structures/#lease) configuradas para expirar al mismo tiempo. Para versiones de cliente 0.9.7 o superior, se utiliza [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage).

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Descripción

Solicitar que un cliente autorice la inclusión de un conjunto particular de tunnels entrantes.

Enviado del Router al Cliente. El cliente responde con un [CreateLeaseSetMessage](#CreateLeaseSetMessage) o [CreateLeaseSet2Message](#CreateLeaseSet2Message).

El primero de estos mensajes enviados en una sesión es una señal al cliente de que los tunnels están construidos y listos para el tráfico. El router no debe enviar el primero de estos mensajes hasta que al menos un tunnel de entrada Y uno de salida hayan sido construidos. Los clientes deben agotar el tiempo de espera y destruir la sesión si el primero de estos mensajes no se recibe después de cierto tiempo (recomendado: 5 minutos o más).

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  1 byte número [Integer](/docs/specs/common-structures/#integer) de túneles
3.  Esa cantidad de entradas [Lease](/docs/specs/common-structures/#lease)

#### Notas

Esto solicita un [LeaseSet](/docs/specs/common-structures/#leaseset) con un tiempo de expiración individual para cada [Lease](/docs/specs/common-structures/#lease).

A partir de la versión 0.9.7. Para clientes anteriores a esa versión, usa [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Descripción

Así es como un cliente envía un mensaje (la carga útil) al [Destination](/docs/specs/common-structures/#destination). El router utilizará una expiración predeterminada.

Enviado del Cliente al Router. El router responde con un [MessageStatusMessage](#MessageStatusMessage).

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  [Destino](/docs/specs/common-structures/#destination)
3.  [Carga útil](#struct-payload)
4.  4 bytes [Integer](/docs/specs/common-structures/#integer) nonce

#### Notas

Tan pronto como el [SendMessageMessage](#SendMessageMessage) llegue completamente intacto, el router debería devolver un [MessageStatusMessage](#MessageStatusMessage) indicando que ha sido aceptado para entrega. Ese mensaje contendrá el mismo nonce enviado aquí. Más adelante, basándose en las garantías de entrega de la configuración de sesión, el router puede enviar adicionalmente otro [MessageStatusMessage](#MessageStatusMessage) actualizando el estado.

A partir de la versión 0.8.1, el router no envía ningún [MessageStatusMessage](#MessageStatusMessage) si i2cp.messageReliability=none.

Antes de la versión 0.9.4, no se permitía un valor de nonce de 0. A partir de la versión 0.9.4, se permite un valor de nonce de 0, y le dice al router que no debe enviar ningún [MessageStatusMessage](#MessageStatusMessage), es decir, actúa como si i2cp.messageReliability=none solo para este mensaje.

Antes de la versión 0.9.14, una sesión con i2cp.messageReliability=none no podía ser anulada por mensaje individual. A partir de la versión 0.9.14, en una sesión con i2cp.messageReliability=none, el cliente puede solicitar la entrega de un [MessageStatusMessage](#MessageStatusMessage) con el éxito o fallo de la entrega estableciendo el nonce a un valor distinto de cero. El router no enviará el [MessageStatusMessage](#MessageStatusMessage) "aceptado" pero posteriormente enviará al cliente un [MessageStatusMessage](#MessageStatusMessage) con el mismo nonce, y un valor de éxito o fallo.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Descripción

Enviado del Cliente al Router. Igual que [SendMessageMessage](#SendMessageMessage), excepto que incluye una expiración y opciones.

#### Contenidos

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 bytes [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 bytes de flags (opciones)
6.  [Date](/docs/specs/common-structures/#date) de expiración truncada de 8 bytes a 6
    bytes

#### Notas

A partir de la versión 0.7.1.

En modo "mejor esfuerzo", tan pronto como el SendMessageExpiresMessage llegue completamente intacto, el router debería devolver un MessageStatusMessage indicando que ha sido aceptado para entrega. Ese mensaje contendrá el mismo nonce enviado aquí. Más adelante, basándose en las garantías de entrega de la configuración de la sesión, el router puede enviar adicionalmente otro MessageStatusMessage actualizando el estado.

A partir de la versión 0.8.1, el router no envía ningún Message Status Message si i2cp.messageReliability=none.

Antes de la versión 0.9.4, no se permitía un valor de nonce de 0. A partir de la versión 0.9.4, se permite un valor de nonce de 0, e indica al router que no debe enviar ningún Message Status Message, es decir, actúa como si i2cp.messageReliability=none solo para este mensaje.

Antes de la versión 0.9.14, una sesión con i2cp.messageReliability=none no podía ser anulada por mensaje individual. A partir de la versión 0.9.14, en una sesión con i2cp.messageReliability=none, el cliente puede solicitar la entrega de un Message Status Message con el éxito o falla de la entrega estableciendo el nonce a un valor distinto de cero. El router no enviará el Message Status Message "accepted" pero posteriormente enviará al cliente un Message Status Message con el mismo nonce, y un valor de éxito o falla.

#### Campo de Flags

A partir de la versión 0.8.4, los dos bytes superiores del Date se redefinen para contener flags. Los flags deben tener por defecto todos ceros para compatibilidad hacia atrás. El Date no invadirá el campo de flags hasta el año 10889. Los flags pueden ser utilizados por la aplicación para proporcionar pistas al router sobre si un LeaseSet y/o ElGamal/AES Session Tags deben ser entregados con el mensaje. La configuración afectará significativamente la cantidad de overhead del protocolo y la confiabilidad de la entrega de mensajes. Los bits de flag individuales se definen como sigue, a partir de la versión 0.9.2. Las definiciones están sujetas a cambios. Usa la clase SendMessageOptions para construir los flags.

Orden de bits: 15...0

Bits 15-11

:   Sin usar, debe ser cero

Bits 10-9

:   Anulación de Confiabilidad de Mensajes (No implementado, a ser eliminado).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Si es 1, no incluyas un lease set en el garlic con este mensaje. Si

    0, the router may bundle a lease set at its discretion.

Bits 7-4

:   Umbral bajo de etiquetas. Si hay menos etiquetas disponibles que este número,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bits 3-0

:   Número de etiquetas a enviar si es requerido. Esto es consultivo y no

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Descripción

Instruir al cliente sobre el estado de su sesión.

Enviado desde el router al cliente, en respuesta a un [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), o [DestroySessionMessage](#DestroySessionMessage). En todos los casos, incluyendo en respuesta a [CreateSessionMessage](#CreateSessionMessage), el router debe responder inmediatamente (no esperar a que se construyan los tunnels).

#### Contenidos

1.  [ID de Sesión](#struct-sessionid)
2.  1 byte [Entero](/docs/specs/common-structures/#integer) estado

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Notas

Los valores de estado se definen arriba. Si el estado es Created, el ID de sesión es el identificador que se debe usar para el resto de la sesión.

### SetDateMessage {#SetDateMessage}

#### Descripción

La fecha y hora actuales. Enviada desde el Router al Cliente como parte del handshake inicial. A partir de la versión 0.9.20, también puede enviarse en cualquier momento después del handshake para notificar al cliente de un cambio de reloj.

#### Contenidos

1.  [Fecha](/docs/specs/common-structures/#date)
2.  Versión de API I2CP [String](/docs/specs/common-structures/#string)

#### Notas

Este es generalmente el primer mensaje enviado por el router. La cadena de versión se incluye a partir de la versión 0.8.7. Esto solo es útil si el cliente y el router no están en la misma JVM. Si no está presente, el router es de la versión 0.8.6 o anterior.

No se enviarán mensajes SetDate adicionales a los clientes en la misma JVM.

## Referencias

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Resumen de I2CP](/docs/specs/i2cp/)
- [Javadocs de I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Javadocs de MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
