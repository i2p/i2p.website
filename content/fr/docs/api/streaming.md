---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/fr/streaming"
  - "/fr/streaming/"
lastUpdated: "2026-01"
accurateFor: "0.9.68"
---

## Overview

The **I2P Streaming Library** provides reliable, in-order, authenticated transport over I2P’s message layer, similar to **TCP over IP**.   It sits above the [I2CP protocol](/docs/specs/i2cp/) and is used by nearly all interactive I2P applications, including HTTP proxies, IRC, BitTorrent, and email.

This design enables small HTTP requests and responses to complete in a single round-trip.   A SYN packet may carry the request payload, while the responder’s SYN/ACK/FIN may contain the full response body.

---

The Java streaming API mirrors standard Java socket programming:

Full Javadocs are available from the I2P router console or [here](/docs/specs/streaming/).

## API Basics

---

You can pass configuration properties when creating a socket manager via:

Newer features since version 0.9.4 include reject log suppression, DSA list support (0.9.21), and mandatory protocol enforcement (0.9.36).   Routers since 2.10.0 include post-quantum hybrid encryption (ML-KEM + X25519) at the transport layer.

### Core Characteristics

---

Each stream is identified by a **Stream ID**. Packets carry control flags similar to TCP: `SYNCHRONIZE`, `ACK`, `FIN`, and `RESET`.   Packets may contain both data and control flags simultaneously, improving efficiency for short-lived connections.

Because I2P tunnels introduce latency and message reordering, the library buffers packets from unknown or early-arriving streams.   Buffered messages are stored until synchronization completes, ensuring complete, in-order delivery.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.accessList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes used for either access list or blacklist. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.destination.sigType</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The name or number of the signature type for a transient destination. As of release 0.9.12.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.enableAccessList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use the access list as a whitelist for incoming connections. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.enableBlackList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use the access list as a blacklist for incoming connections. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.answerPings</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to respond to incoming pings</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.blacklist</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes to be blacklisted for incoming connections to ALL destinations in the context. This option must be set in the context properties, NOT in the createManager() options argument. Note that setting this in the router context will not affect clients outside the router in a separate JVM and context. As of release 0.9.3.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.bufferSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64K</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How much transmit data (in bytes) will be accepted that hasn't been written out yet.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.congestionAvoidanceGrowthRateFactor</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">When we're in congestion avoidance, we grow the window size at the rate of <code>1/(windowSize*factor)</code>. In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages. A higher number means slower growth.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.connectDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to wait after instantiating a new con before actually attempting to connect. If this is &lt;= 0, connect immediately with no initial data. If greater than 0, wait until the output stream is flushed, the buffer fills, or that many milliseconds pass, and include any initial data with the SYN.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.connectTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5*60*1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on connect, in milliseconds. Negative means indefinitely. Default is 5 minutes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.disableRejectLogging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to disable warnings in the logs when an incoming connection is rejected due to connection limits. As of release 0.9.4.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.dsalist</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes or host names to be contacted using an alternate DSA destination. Only applies if multisession is enabled and the primary session is non-DSA (generally for shared clients only). This option must be set in the context properties, NOT in the createManager() options argument. Note that setting this in the router context will not affect clients outside the router in a separate JVM and context. As of release 0.9.21.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.enforceProtocol</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to listen only for the streaming protocol. Setting to true will prohibit communication with Destinations earlier than release 0.7.1 (released March 2009). Set to true if running multiple protocols on this Destination. As of release 0.9.1. Default true as of release 0.9.36.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.inactivityAction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 (send)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(0=noop, 1=disconnect) What to do on an inactivity timeout - do nothing, disconnect, or send a duplicate ack.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.inactivityTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90*1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle time before sending a keepalive</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialAckDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">750</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Delay before sending an ack</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialResendDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The initial value of the resend delay field in the packet header, times 1000. Not fully implemented; see below.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialRTO</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial timeout (if no <a href="#sharing">sharing data</a> available). As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialRTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial round trip time estimate (if no <a href="#sharing">sharing data</a> available). Disabled as of release 0.9.8; uses actual RTT.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialWindowSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(if no <a href="#sharing">sharing data</a> available) In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.limitAction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reset</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release 0.9.34.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConcurrentStreams</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(0 or negative value means unlimited) This is a total limit for incoming and outgoing combined.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerMinute</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Incoming connection limit (per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerHour</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerDay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxMessageSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The maximum size of the payload, i.e. the MTU in bytes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxResends</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum number of retransmissions before failure.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerMinute</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Incoming connection limit (all peers; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerHour</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(all peers; 0 means disabled) Use with caution as exceeding this will disable a server for a long time. As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerDay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(all peers; 0 means disabled) Use with caution as exceeding this will disable a server for a long time. As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxWindowSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.profile</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 (bulk)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1=bulk; 2=interactive; see important notes <a href="#profile">below</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.readTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on read, in milliseconds. Negative means indefinitely.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.slowStartGrowthRateFactor</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">When we're in slow start, we grow the window size at the rate of 1/(factor). In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages. A higher number means slower growth.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.rttDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.rttdevDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.wdwDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.writeTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on write/flush, in milliseconds. Negative means indefinitely.</td>
    </tr>
  </tbody>
</table>
## Configuration and Tuning

The option `i2p.streaming.enforceProtocol=true` (default since 0.9.36) ensures connections use the correct I2CP protocol number, preventing conflicts between multiple subsystems sharing one destination.

## Protocol Details

### Key Options

---

The streaming protocol coexists with the **Datagram API**, giving developers the choice between connection-oriented and connectionless transports.

### Behavior by Workload

Applications can reuse existing tunnels by running as **shared clients**, allowing multiple services to share the same destination.   While this reduces overhead, it increases cross-service correlation risk—use with care.

Because I2P adds several hundred milliseconds of base latency, applications should minimize round-trips.   Bundle data with connection setup where possible (e.g., HTTP requests in SYN).   Avoid designs relying on many small sequential exchanges.

---

Performance depends heavily on tunnel configuration:   - **Short tunnels (1–2 hops)** → lower latency, reduced anonymity.   - **Long tunnels (3+ hops)** → higher anonymity, increased RTT.

### Connection Lifecycle

---

### Fragmentation and Reordering

---

### Protocol Enforcement

The **I2P Streaming Library** is the backbone of all reliable communication within I2P.   It ensures in-order, authenticated, encrypted message delivery and provides a near drop-in replacement for TCP in anonymous environments.

### Shared Clients

To achieve optimal performance: - Minimize round-trips with SYN+payload bundling.   - Tune window and timeout parameters for your workload.   - Favor shorter tunnels for latency-sensitive applications.   - Use congestion-friendly designs to avoid overloading peers.

La taille maximale par défaut de la fenêtre de transmission et de réception dans l'implémentation Java est de 128 paquets. Les implémentations définissant une taille maximale de fenêtre de transmission supérieure à 128 doivent considérer les problèmes suivants :

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

La taille de tampon minimale recommandée pour les implémentations de récepteur est de 128 paquets ou 232 KB (approximativement 128 * 1812). En raison de la latence du réseau I2P, des pertes de paquets et du contrôle de congestion qui en résulte, un tampon de cette taille est rarement rempli. Le débordement est cependant beaucoup plus susceptible de se produire sur les connexions "local loopback" (même router) à haute bande passante ou lors de tests locaux.

Pour indiquer rapidement et récupérer en douceur des conditions de débordement, il existe un mécanisme simple de contre-pression dans le protocole de streaming. Si un paquet est reçu avec un champ de délai optionnel d'une valeur de 60001 ou plus, cela indique un "étranglement" ou une fenêtre de réception de zéro. Un paquet avec un champ de délai optionnel d'une valeur de 60000 ou moins indique un "déstranglement". Les paquets sans champ de délai optionnel n'affectent pas l'état d'étranglement/déstranglement.

Après avoir été bloqué, aucun paquet contenant des données ne devrait être envoyé jusqu'à ce que le transmetteur soit débloqué, à l'exception de paquets de données "sonde" occasionnels pour compenser d'éventuels paquets de déblocage perdus. Le point de terminaison bloqué devrait démarrer un "minuteur de persistance" pour contrôler le sondage, comme dans TCP. Le point de terminaison qui débloque devrait envoyer plusieurs paquets avec ce champ défini, ou continuer à les envoyer périodiquement jusqu'à ce que des paquets de données soient à nouveau reçus. Le temps maximum d'attente pour le déblocage dépend de l'implémentation. La taille de la fenêtre du transmetteur et la stratégie de contrôle de congestion après déblocage dépendent de l'implémentation.

### Congestion Control

La bibliothèque de streaming utilise les phases standard de démarrage lent (croissance exponentielle de la fenêtre) et d'évitement de congestion (croissance linéaire de la fenêtre), avec un backoff exponentiel. Le fenêtrage et les accusés de réception utilisent le nombre de paquets, pas le nombre d'octets.

### Latency Considerations

Tout paquet, y compris celui avec le flag SYNCHRONIZE défini, peut également avoir le flag CLOSE envoyé. La connexion n'est pas fermée tant que le pair ne répond pas avec le flag CLOSE. Les paquets CLOSE peuvent également contenir des données.

### Ping / Pong {#ping}

Il n'y a pas de fonction ping au niveau de la couche I2CP (équivalent à l'écho ICMP) ou dans les datagrammes. Cette fonction est fournie dans le streaming. Les pings et pongs ne peuvent pas être combinés avec un paquet de streaming standard ; si l'option ECHO est définie, alors la plupart des autres drapeaux, options, ackThrough, sequenceNum, NACKs, etc. sont ignorés.

Un paquet ping doit avoir les drapeaux ECHO, SIGNATURE_INCLUDED et FROM_INCLUDED définis. Le sendStreamId doit être supérieur à zéro, et le receiveStreamId est ignoré. Le sendStreamId peut correspondre ou non à une connexion existante.

Un paquet pong doit avoir le flag ECHO défini. Le sendStreamId doit être zéro, et le receiveStreamId est le sendStreamId du ping. Avant la version 0.9.18, le paquet pong n'inclut aucune charge utile qui était contenue dans le ping.

À partir de la version 0.9.18, les pings et pongs peuvent contenir une charge utile. La charge utile dans le ping, jusqu'à un maximum de 32 octets, est retournée dans le pong.

Le streaming peut être configuré pour désactiver l'envoi de pongs avec la configuration i2p.streaming.answerPings=false.

### Problèmes 0-RTT {#0rtt}

Comme indiqué ci-dessus, contrairement à TCP, le streaming permet la livraison de données en 0-RTT en regroupant les données dans le paquet SYN. C'est l'implémentation préférée. DE PLUS, le streaming permet l'envoi de paquets de données supplémentaires (jusqu'à la taille de fenêtre initiale) après le SYN, avant que le SYN-ACK ne soit reçu. Ces paquets auront un numéro de séquence non nul, n'auront pas le flag SYN activé, et auront un sendStreamID à zéro.

Les récepteurs doivent concevoir leur système pour gérer les paquets désordonnés ou perdus pendant la négociation (handshake), y compris l'arrivée de paquets de données avant le SYN. L'implémentation préférée consiste à mettre en file d'attente, et non à rejeter, les paquets non-SYN pour un ID inconnu, et à les récupérer de la file d'attente après réception du SYN.

Dans le sens inverse, les choses sont similaires. Le destinataire de la connexion (Bob) devrait retarder l'envoi du SYN-ACK (ACK DELAY) et attendre un court moment pour recevoir des données de l'application. Lors de la réception de données de l'application, les placer (jusqu'à la taille maximale du paquet) dans le paquet SYN-ACK et l'envoyer. Des paquets de données supplémentaires, jusqu'à la taille de fenêtre initiale, peuvent également être envoyés, sans attendre un ACK du SYN-ACK.

L'initiateur devrait mettre en mémoire tampon tous les paquets de données reçus avant le SYN-ACK, de la même manière que la gestion des paquets dans le désordre après la completion de la poignée de main.

### Test des bibliothèques de streaming {#testing}

Pour les développeurs testant des bibliothèques de streaming nouvelles ou modifiées, Java I2P fournit un utilitaire de test local simple pour des tests reproductibles de conditions réseau réelles, incluant la latence, la perte de paquets et la gigue de délai. Il s'agit d'un petit stub implémentant uniquement un serveur I2CP pour les connexions locales.

Les développeurs devraient tester avec une large gamme de paramètres typiques, incluant une latence de 10ms à au moins 15s, et une perte de paquets de 0 à 10%. L'ajout de gigue facilite les tests de gestion des paquets dans le désordre.

C'est également une bonne configuration pour tester le débordement de tampon (CHOKE/UNCHOKE) en suspendant manuellement l'une des deux applications.

Depuis le paquet source i2p.i2p :

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### Notes sur i2p.streaming.profile {#profile}

Cette option prend en charge deux valeurs ; 1=bulk et 2=interactive. L'option fournit une indication à la bibliothèque de streaming et/ou au router concernant le modèle de trafic attendu.

"Bulk" signifie optimiser pour une bande passante élevée, possiblement au détriment de la latence. C'est le réglage par défaut. "Interactive" signifie optimiser pour une faible latence, possiblement au détriment de la bande passante ou de l'efficacité. Les stratégies d'optimisation, le cas échéant, dépendent de l'implémentation et peuvent inclure des modifications en dehors du protocole de streaming.

Jusqu'à la version API 0.9.63, Java I2P retournait une erreur pour toute valeur autre que 1 (bulk) et le tunnel échouait à démarrer. À partir de l'API 0.9.64, Java I2P ignore cette valeur. Jusqu'à la version API 0.9.63, i2pd ignorait cette option ; elle est implémentée dans i2pd à partir de l'API 0.9.64.

Bien que le protocole de streaming inclue un champ de drapeau pour transmettre le paramètre de profil à l'autre extrémité, ceci n'est implémenté dans aucun router connu.

### Partage de bloc de contrôle {#sharing}

La bibliothèque streaming prend en charge le partage de blocs de contrôle "TCP". Ceci partage trois paramètres importants de la bibliothèque streaming (taille de fenêtre, temps d'aller-retour, variance du temps d'aller-retour) entre les connexions vers le même pair distant. Ceci est utilisé pour le partage "temporel" au moment de l'ouverture/fermeture de connexion, pas pour le partage "d'ensemble" pendant une connexion (Voir [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Il y a un partage séparé par ConnectionManager (c'est-à-dire par Destination locale) afin qu'il n'y ait aucune fuite d'information vers d'autres Destinations sur le même router. Les données de partage pour un pair donné expirent après quelques minutes. Les paramètres de partage de bloc de contrôle suivants peuvent être définis par router :

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### Autres paramètres {#other}

Les paramètres suivants sont les valeurs par défaut recommandées. Les valeurs par défaut peuvent varier selon l'implémentation :

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### Historique {#history}

La bibliothèque de streaming a évolué de manière organique pour I2P - d'abord mihi a implémenté la "mini bibliothèque de streaming" dans le cadre d'I2PTunnel, qui était limitée à une taille de fenêtre de 1 message (nécessitant un ACK avant d'envoyer le suivant), puis elle a été refactorisée en une interface de streaming générique (reflétant les sockets TCP) et l'implémentation complète de streaming a été déployée avec un protocole de fenêtre glissante et des optimisations pour tenir compte du produit élevé bande passante x délai. Les flux individuels peuvent ajuster la taille maximale des paquets et d'autres options. La taille de message par défaut est sélectionnée pour s'adapter précisément dans deux messages tunnel I2NP de 1K, et constitue un compromis raisonnable entre les coûts de bande passante de retransmission des messages perdus, et la latence et les frais généraux de plusieurs messages.

## Interoperability and Best Practices

Le comportement de la bibliothèque de streaming a un impact profond sur les performances au niveau applicatif, et constitue donc un domaine important pour des analyses plus approfondies.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
