---
title: "Protokollstapel"
description: "Überblick über die I2P-Protokollstack-Schichten"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/de/docs/develop/protocol-stack"
  - "/de/docs/develop/protocol-stack/"
---

Der I2P-Stack ist ein geschichtetes Design, das anonyme Kommunikation ermöglicht. Jede Schicht fügt spezifische Fähigkeiten zu denen darunter hinzu. Siehe den [Index der technischen Dokumentation](/docs/develop/overview) für weitere Details zu jeder Komponente.

## Internet-Schicht {#internet}

**IP** - Internet Protocol ermöglicht die Adressierung von Hosts im regulären Internet und das Routing von Paketen über das Internet unter Verwendung von Best-Effort-Zustellung.

## Transport Layer {#transport}

- **TCP** - Transmission Control Protocol ermöglicht zuverlässige, geordnete Zustellung von Paketen
- **UDP** - User Datagram Protocol ermöglicht unzuverlässige, ungeordnete Zustellung von Paketen

## I2P Transport Layer {#i2p-transport}

Verschlüsselte router-zu-router Verbindungen (noch nicht anonym):

- **[NTCP2](/docs/specs/ntcp2)** - NIO-basierter TCP-Transport
- **[SSU2](/docs/specs/ssu2)** - Sicherer semi-zuverlässiger UDP-Transport

## I2P Tunnel Layer {#tunnels}

Bietet vollständig anonyme verschlüsselte tunnel-Verbindungen:

- **[Tunnel messages](/docs/legacy/tunnel-message)** - Verschlüsselte I2NP-Nachrichten und verschlüsselte
  Anweisungen für ihre Zustellung
- **[I2NP messages](/docs/specs/i2np)** - Protokollnachrichten mit geschichteter Verschlüsselung für
  anonymes Multi-Hop-Routing

## I2P Garlic Layer {#garlic}

Bietet verschlüsselte und anonyme Ende-zu-Ende I2P-Nachrichtenübertragung:

- **[Garlic messages](/docs/overview/garlic-routing)** - Verpackte I2NP-Nachrichten für anonyme Zustellung

## I2P Client-Schicht {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol ermöglicht es Anwendungen, auf das I2P-Netzwerk zuzugreifen, ohne die router-API direkt verwenden zu müssen

## I2P Ende-zu-Ende-Transportschicht {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Bietet zuverlässige, geordnete Zustellung
  ähnlich wie TCP
- **[Datagram Library](/docs/api/datagrams)** - Bietet unzuverlässige Zustellung ähnlich wie UDP

## I2P Anwendungsschnittstellenschicht {#app-interface}

Optionale Schnittstellen für Anwendungsentwickler:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Tunnelt TCP-Verbindungen in und aus I2P
- **[SAMv3](/docs/api/samv3)** - Simple Anonymous Messaging-Protokoll für Nicht-Java-Anwendungen

## I2P Anwendungs-Proxy-Schicht {#app-proxy}

Proxies für Standard-Internetprotokolle:

- **HTTP** - Web-Browsing-Proxy
- **IRC** - Internet Relay Chat Proxy
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 Proxy
- **Streamr** - UDP-Streaming-Proxy

## Anwendungen {#applications}

Anwendungen können mit I2P auf verschiedenen Ebenen interagieren:

**Streaming/Datagram-Anwendungen:** - I2P-native Anwendungen, die die Streaming- oder Datagram-Bibliotheken direkt verwenden

**SAM-Anwendungen:** - Anwendungen in jeder Programmiersprache, die das SAM-Protokoll verwenden

**I2P-spezifische Anwendungen:** - Anwendungen, die speziell für I2P entwickelt wurden (I2PSnark, SusiMail, etc.)

**Standard-Internetanwendungen:** - Reguläre Anwendungen, die I2P-Proxies verwenden (Webbrowser, IRC-Clients, etc.)

## Stack-Diagramm {#diagram}

![I2P Protocol Stack](/images/protocol_stack.png)

Hinweis: SAM kann sowohl die Streaming-Bibliothek als auch Datagramme verwenden.
