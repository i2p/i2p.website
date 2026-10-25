---
title: "Protokolový stack"
description: "Přehled vrstev protokolového zásobníku I2P"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/cs/docs/develop/protocol-stack"
  - "/cs/docs/develop/protocol-stack/"
  - "/cs/protocols"
  - "/cs/protocols/"
---

I2P stack je vrstvená architektura umožňující anonymní komunikaci. Každá vrstva přidává specifické schopnosti na ty pod ní. Pro další podrobnosti o každé komponentě si prohlédněte [Rejstřík technické dokumentace](/docs/develop/overview).

## Internetová vrstva {#internet}

**IP** - Internet Protocol umožňuje adresování hostitelů na běžném internetu a směrování paketů přes internet pomocí best-effort doručování.

## Transportní vrstva {#transport}

- **TCP** - Transmission Control Protocol umožňuje spolehlivé doručování paketů ve správném pořadí
- **UDP** - User Datagram Protocol umožňuje nespolehlivé doručování paketů bez zachování pořadí

## I2P Transport Layer {#i2p-transport}

Šifrovaná připojení router-k-router (zatím ne anonymní):

- **[NTCP2](/docs/specs/ntcp2)** - NIO-založený TCP transport
- **[SSU2](/docs/specs/ssu2)** - Zabezpečený semi-spolehlivý UDP transport

## I2P Tunnel Layer {#tunnels}

Poskytuje plně anonymní šifrované tunnel spojení:

- **[Tunnel messages](/docs/legacy/tunnel-message)** - Šifrované I2NP zprávy a šifrované
  instrukce pro jejich doručení
- **[I2NP messages](/docs/specs/i2np)** - Protokolové zprávy s vrstvovým šifrováním pro
  víceúrovňové anonymní směrování

## I2P Garlic Layer {#garlic}

Poskytuje šifrované a anonymní end-to-end doručování zpráv v I2P:

- **[Garlic zprávy](/docs/overview/garlic-routing)** - Zabalené I2NP zprávy pro anonymní doručení

## I2P Client Layer {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol umožňuje aplikacím přistupovat
  k síti I2P bez nutnosti používat router API přímo

## I2P End-to-End Transport Layer {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Poskytuje spolehlivé doručování v pořadí
  podobné TCP
- **[Datagram Library](/docs/api/datagrams)** - Poskytuje nespolehlivé doručování podobné UDP

## I2P Aplikační Interface Vrstva {#app-interface}

Volitelná rozhraní pro vývojáře aplikací:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Tuneluje TCP spojení do a z I2P
- **[SAMv3](/docs/api/samv3)** - Simple Anonymous Messaging protokol pro non-Java aplikace

## I2P Application Proxy Layer {#app-proxy}

Proxy servery pro standardní internetové protokoly:

- **HTTP** - Proxy pro procházení webu
- **IRC** - Proxy pro Internet Relay Chat
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 proxy
- **Streamr** - Proxy pro UDP streaming

## Aplikace {#applications}

Aplikace se mohou připojit k I2P na různých vrstvách:

**Streaming/Datagram Applications:** - I2P-nativní aplikace používající streaming nebo datagram knihovny přímo

**SAM Aplikace:** - Aplikace v jakémkoliv jazyce využívající SAM protokol

**Aplikace specifické pro I2P:** - Aplikace navržené speciálně pro I2P (I2PSnark, SusiMail, atd.)

**Standardní internetové aplikace:** - Běžné aplikace používající I2P proxy (webové prohlížeče, IRC klienti, atd.)

## Diagram zásobníku {#diagram}

![I2P Protocol Stack](/images/protocol_stack.png)

Poznámka: SAM může používat jak streaming knihovnu, tak datagramy.
