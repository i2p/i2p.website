---
title: "Protocol Stack"
description: "Overview of the I2P protocol stack layers"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/docs/develop/protocol-stack/"
---


The I2P stack is a layered design enabling anonymous communication. Each layer adds
specific capabilities on top of those below it. See the
[Technical Documentation Index](/docs/develop/overview) for additional details on each component.


## Internet Layer {#internet}

**IP** - Internet Protocol allows addressing hosts on the regular internet and routing packets
across the internet using best-effort delivery.


## Transport Layer {#transport}

- **TCP** - Transmission Control Protocol allows reliable, in-order delivery of packets
- **UDP** - User Datagram Protocol allows unreliable, out-of-order delivery of packets


## I2P Transport Layer {#i2p-transport}

Encrypted router-to-router connections (not yet anonymous):

- **[NTCP2](/docs/specs/ntcp2)** - NIO-based TCP transport
- **[SSU2](/docs/specs/ssu2)** - Secure Semi-reliable UDP transport


## I2P Tunnel Layer {#tunnels}

Provides full anonymous encrypted tunnel connections:

- **[Tunnel messages](/docs/legacy/tunnel-message)** - Encrypted I2NP messages and encrypted
  instructions for their delivery
- **[I2NP messages](/docs/specs/i2np)** - Protocol messages with layered encryption for
  multi-hop anonymous routing


## I2P Garlic Layer {#garlic}

Provides encrypted and anonymous end-to-end I2P message delivery:

- **[Garlic messages](/docs/overview/garlic-routing)** - Wrapped I2NP messages for anonymous delivery


## I2P Client Layer {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol allows applications to access
  the I2P network without having to use the router API directly


## I2P End-to-End Transport Layer {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Provides reliable, in-order delivery
  similar to TCP
- **[Datagram Library](/docs/api/datagrams)** - Provides unreliable delivery similar to UDP


## I2P Application Interface Layer {#app-interface}

Optional interfaces for application developers:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Tunnels TCP connections into and out of I2P
- **[SAMv3](/docs/api/samv3)** - Simple Anonymous Messaging protocol for non-Java applications


## I2P Application Proxy Layer {#app-proxy}

Proxies for standard internet protocols:

- **HTTP** - Web browsing proxy
- **IRC** - Internet Relay Chat proxy
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 proxy
- **Streamr** - UDP streaming proxy


## Applications {#applications}

Applications can interface with I2P at various layers:

**Streaming/Datagram Applications:**
- I2P-native applications using the streaming or datagram libraries directly

**SAM Applications:**
- Applications in any language using the SAM protocol

**I2P-Specific Applications:**
- Applications designed specifically for I2P (I2PSnark, SusiMail, etc.)

**Standard Internet Applications:**
- Regular applications using I2P proxies (web browsers, IRC clients, etc.)


## Stack Diagram {#diagram}

![I2P Protocol Stack](/images/protocol_stack.png)

Note: SAM can use both the streaming library and datagrams.
