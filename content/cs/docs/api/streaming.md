---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/cs/streaming"
  - "/cs/streaming/"
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

Výchozí maximální velikost vysílacího a přijímacího okna v implementaci Java je 128 paketů. Implementace nastavující maximální velikost vysílacího okna vyšší než 128 musí zvážit následující problémy:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

Doporučená minimální velikost bufferu pro implementace příjemců je 128 paketů nebo 232 KB (přibližně 128 * 1812). Kvůli latenci I2P sítě, ztrátám paketů a výsledné kontrole přetížení se buffer této velikosti zřídka zaplní. Přetečení je však mnohem pravděpodobnější u vysokorychlostních "local loopback" (stejný router) spojení nebo při lokálním testování.

Pro rychlé indikování a plynulé zotavení z přetečení existuje jednoduchý mechanismus pro zpětný tlak ve streamovacím protokolu. Pokud je přijat paket s volitelným polem zpoždění s hodnotou 60001 nebo vyšší, znamená to "dušení" nebo přijímací okno o velikosti nula. Paket s volitelným polem zpoždění s hodnotou 60000 nebo nižší indikuje "ukončení dušení". Pakety bez volitelného pole zpoždění neovlivňují stav dušení/ukončení dušení.

Po zadušení by neměly být odesílány žádné další pakety s daty, dokud není vysílač odblokován, s výjimkou občasných "sondovacích" datových paketů pro kompenzaci možných ztracených odblokujících paketů. Zadušený koncový bod by měl spustit "persist timer" pro řízení sondování, podobně jako v TCP. Odblokující koncový bod by měl odeslat několik paketů s tímto polem nastaveným, nebo je nadále posílat periodicky, dokud nebudou znovu přijaty datové pakety. Maximální čas čekání na odblokování je závislý na implementaci. Velikost okna vysílače a strategie řízení zahlcení po odblokování je závislá na implementaci.

### Congestion Control

Streaming knihovna používá standardní slow-start (exponenciální růst okna) a fáze vyhýbání se přetížení (lineární růst okna) s exponenciálním zpožděním. Okénkování a potvrzování používají počet paketů, ne počet bajtů.

### Latency Considerations

Jakýkoli paket, včetně paketu s nastaveným příznakem SYNCHRONIZE, může mít také nastaven příznak CLOSE. Spojení není uzavřeno, dokud protistrana neodpoví s příznakem CLOSE. Pakety CLOSE mohou také obsahovat data.

### Ping / Pong {#ping}

Na vrstvě I2CP neexistuje žádná ping funkce (ekvivalentní k ICMP echo) ani v datagramech. Tato funkce je poskytována ve streaming. Pingy a pongy nesmí být kombinovány se standardním streaming paketem; pokud je nastavena možnost ECHO, pak jsou ignorovány většina ostatních příznaků, možností, ackThrough, sequenceNum, NACK atd.

Ping paket musí mít nastavené příznaky ECHO, SIGNATURE_INCLUDED a FROM_INCLUDED. SendStreamId musí být větší než nula a receiveStreamId se ignoruje. SendStreamId může nebo nemusí odpovídat existujícímu připojení.

Pong paket musí mít nastaven příznak ECHO. SendStreamId musí být nula a receiveStreamId je sendStreamId z ping paketu. Před verzí 0.9.18 pong paket neobsahoval žádná data, která byla obsažena v ping paketu.

Od verze 0.9.18 mohou ping a pong obsahovat užitečný obsah. Užitečný obsah v ping, až do maxima 32 bajtů, je vrácen v pong.

Streaming může být nakonfigurován tak, aby zakázal odesílání pongů pomocí konfigurace i2p.streaming.answerPings=false.

### Problémy s 0-RTT {#0rtt}

Jak bylo uvedeno výše, na rozdíl od TCP umožňuje streaming 0-RTT doručování dat pomocí zabalení dat do SYN paketu. Toto je preferovaná implementace. TAKÉ streaming povoluje odeslání dalších datových paketů (až do velikosti počátečního okna) po SYN, před přijetím SYN-ACK. Tyto pakety budou mít nenulové pořadové číslo, nebudou mít nastaven příznak SYN a budou mít nulové sendStreamID.

Příjemci by měli navrhovat s ohledem na pakety doručené mimo pořadí nebo ztracené pakety během handshake, včetně situace kdy datové pakety dorazí před SYN. Preferovaná implementace je zařadit do fronty, nikoli zahazovat, non-SYN pakety pro neznámé ID a načíst je z fronty poté, co je přijat SYN.

V opačném směru jsou věci podobné. Příjemce připojení (Bob) by měl zpozdit odeslání SYN-ACK (ACK DELAY) a krátkou dobu počkat na data z aplikace. Po přijetí dat z aplikace je vložit (až do maximální velikosti paketu) do SYN-ACK paketu a odeslat ho. Další datové pakety, až do velikosti počátečního okna, mohou být také odeslány, aniž by se čekalo na ACK pro SYN-ACK.

Původce by měl ukládat do bufferu všechny datové pakety přijaté před SYN-ACK, stejně jako při zpracování pořadí po dokončení handshaku.

### Testování Streaming knihoven {#testing}

Pro vývojáře testující nové nebo změněné streamovací knihovny poskytuje Java I2P jednoduchý místní testovací nástroj pro reprodukovatelné testování skutečných síťových podmínek, včetně latence, ztráty paketů a kolísání zpoždění. Jedná se o malý stub implementující pouze I2CP server pro místní připojení.

Vývojáři by měli testovat s širokou škálou typických parametrů, včetně latence od 10ms do alespoň 15s a ztráty paketů od 0 do 10%. Přidání jitteru usnadňuje testování zpracování neuspořádaných paketů.

Toto je také dobré nastavení pro testování přetečení bufferu (CHOKE/UNCHOKE) manuálním pozastavením jedné ze dvou aplikací.

Ze zdrojového balíčku i2p.i2p:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### i2p.streaming.profile Poznámky {#profile}

Tato možnost podporuje dvě hodnoty; 1=bulk a 2=interactive. Možnost poskytuje nápovědu pro streaming knihovnu a/nebo router ohledně očekávaného vzoru provozu.

"Bulk" znamená optimalizaci pro vysokou šířku pásma, případně na úkor latence. Toto je výchozí nastavení. "Interactive" znamená optimalizaci pro nízkou latenci, případně na úkor šířky pásma nebo efektivity. Strategie optimalizace, pokud nějaké existují, jsou závislé na implementaci a mohou zahrnovat změny mimo streaming protokol.

Do verze API 0.9.63 by Java I2P vrátil chybu pro jakoukoliv hodnotu jinou než 1 (bulk) a tunnel by se nepodařilo spustit. Od verze API 0.9.64 Java I2P tuto hodnotu ignoruje. Do verze API 0.9.63 i2pd tuto možnost ignoroval; je implementována v i2pd od verze API 0.9.64.

Zatímco streaming protokol obsahuje pole pro příznak k předání nastavení profilu na druhý konec, toto není implementováno v žádném známém router.

### Sdílení kontrolního bloku {#sharing}

Streaming knihovna podporuje sdílení "TCP" Control Block. Toto sdílí tři důležité parametry streaming knihovny (velikost okna, doba odezvy, rozptyl doby odezvy) napříč připojeními ke stejnému vzdálenému peer. Toto se používá pro "temporální" sdílení v době otevírání/zavírání připojení, nikoliv pro "ensemble" sdílení během připojení (viz [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Existuje samostatné sdílení pro každý ConnectionManager (tj. pro každou lokální Destination), takže nedochází k úniku informací do jiných Destinations na stejném router. Sdílená data pro daný peer vyprší po několika minutách. Následující parametry Control Block Sharing lze nastavit pro každý router:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### Ostatní parametry {#other}

Následující parametry jsou doporučené výchozí hodnoty. Výchozí hodnoty se mohou lišit v závislosti na implementaci:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### Historie {#history}

Streaming knihovna se pro I2P vyvinula organicky - nejprve mihi implementoval "mini streaming knihovnu" jako součást I2PTunnel, která byla omezena na velikost okna 1 zprávy (vyžadovala ACK před odesláním další), a poté byla refaktorována do generického streaming rozhraní (zrcadlícího TCP sockety) a plná streaming implementace byla nasazena s protokolem posuvného okna a optimalizacemi zohledňujícími vysoký součin šířky pásma x zpoždění. Jednotlivé streamy mohou upravit maximální velikost paketu a další možnosti. Výchozí velikost zprávy je vybrána tak, aby přesně zapadla do dvou 1K I2NP tunnel zpráv, a představuje rozumný kompromis mezi náklady šířky pásma na retransmisi ztracených zpráv a latencí a režijí více zpráv.

## Interoperability and Best Practices

Chování streaming knihovny má zásadní dopad na výkon na úrovni aplikace, a proto je to důležitá oblast pro další analýzu.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
