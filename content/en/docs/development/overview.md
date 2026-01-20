---
title: "Technical Documentation Index"
description: "Index to the I2P technical documentation"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/docs/development/overview/"
---


## Overview {#overview}

- [Technical Introduction](/docs/overview/intro)
- [A Less-Technical Introduction](/docs/overview/intro/)
- [Threat model and analysis](/docs/overview/threat-model)
- [Comparisons to other anonymous networks](/docs/overview/comparison)
- [Protocol stack chart](/docs/development/protocol-stack)
- [Papers on I2P](/papers/)
- [Presentations, articles, tutorials, videos, and interviews](/about/media/)
- [Invisible Internet Project (I2P) Project Overview - August 28, 2003 (PDF)](/docs/historical/i2p_philosophy.pdf)


## Application-Layer Topics {#applications}

- [Application Development Overview and Guide](/docs/development/applications)
- [Naming and Address Book](/docs/overview/naming)
- [Address Book Subscription Feed Commands](/docs/specs/subscription)
- [Plugins Overview](/docs/applications/plugins)
- [Plugin Specification](/docs/specs/plugin)
- [Managed Clients](/docs/applications/managed-clients)
- [Embedding the router in your application](/docs/applications/embedding)
- [Bittorrent over I2P](/docs/applications/bittorrent)
- [I2PControl Plugin API](/docs/api/i2pcontrol)
- [hostsdb.blockfile Format](/docs/specs/blockfile)
- [Configuration File Format](/docs/specs/configuration)


## Application Layer API and Protocols {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [I2PTunnel Configuration](/docs/specs/configuration)
- [SOCKS Proxy](/docs/api/socks)
- [SAMv3 Protocol](/docs/api/samv3)
- [SAM Protocol](/docs/legacy/sam) (Deprecated)
- [SAMv2 Protocol](/docs/legacy/samv2) (Deprecated)
- [BOB Protocol](/docs/legacy/bob) (Deprecated)


## End-to-End Transport API and Protocols {#transport-api}

- [Streaming Protocol Overview](/docs/api/streaming)
- [Streaming Protocol Specification](/docs/specs/streaming)
- [Datagrams](/docs/api/datagrams)
- [Datagrams Specification](/docs/specs/datagrams)


## Client-to-Router Interface API and Protocol {#i2cp}

- [I2CP Overview](/docs/specs/i2cp)
- [I2CP Specification](/docs/specs/i2cp)
- [Common Data Structures Specification](/docs/specs/common-structures)


## End-to-End Encryption {#encryption}

- [ECIES-X25519-AEAD-Ratchet encryption for destinations](/docs/specs/ecies)
- [Hybrid ECIES-X25519 encryption](/docs/specs/ecies-hybrid)
- [ECIES-X25519 encryption for routers](/docs/specs/ecies-routers)
- [ElGamal/AES+SessionTag encryption](/docs/legacy/elgamal-aes)
- [ElGamal and AES cryptography details](/docs/specs/cryptography)


## Network Database {#netdb}

- [Network database overview, details, and threat analysis](/docs/overview/network-database)
- [Cryptographic hashes](/docs/specs/cryptography#hashes)
- [Cryptographic signatures](/docs/specs/cryptography#signatures)
- [Red25519 signatures](/docs/specs/red25519)
- [Router reseed specification](/docs/misc/reseed)
- [Base32 Addresses for Encrypted Leasesets](/docs/specs/b32encrypted)


## Router Message Protocol {#i2np}

- [I2NP Overview](/docs/specs/i2np)
- [I2NP Specification](/docs/specs/i2np)
- [Common Data Structures Specification](/docs/specs/common-structures)
- [Encrypted Leaseset Specification](/docs/specs/encryptedleaseset)


## Tunnels {#tunnels}

- [Peer profiling and selection](/docs/overview/peer-selection)
- [Tunnel routing overview](/docs/overview/tunnel-routing)
- [Garlic routing and terminology](/docs/overview/garlic-routing)
- [Tunnel building and encryption](/docs/legacy/tunnel-creation)
- [ElGamal/AES for build request encryption](/docs/legacy/elgamal-tunnel-creation)
- [ElGamal and AES cryptography details](/docs/specs/cryptography)
- [Tunnel building specification (ElGamal)](/docs/legacy/tunnel-creation)
- [Tunnel building specification (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [Low-level tunnel message specification](/docs/legacy/tunnel-message)
- [Unidirectional Tunnels](/docs/legacy/unidirectional-tunnels)
- [Peer Profiling and Selection in the I2P Anonymous Network - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## Transport Layer {#transports}

- [Transport layer overview](/docs/overview/transport)
- [NTCP2 specification](/docs/specs/ntcp2)
- [SSU2 specification](/docs/specs/ssu2)
- [NTCP (Legacy)](/docs/legacy/ntcp)
- [SSU Overview (Legacy)](/docs/legacy/ssu-overview)


## Other Router Topics {#router}

- [Router software updates](/docs/specs/updates)
- [Router reseed specification](/docs/misc/reseed)
- [Performance](/docs/overview/performance)
- [Configuration File Format](/docs/specs/configuration)
- [GeoIP File Format](/docs/legacy/geoip)
- [Ports used by I2P](/docs/overview/ports)


## Developer's Guides and Resources {#develop}

- [New Developer's Guide](/docs/development/new-developers)
- [New Translator's Guide](/docs/development/new-translators)
- [Developer Guidelines](/docs/development/dev-guidelines)
- [Proposals](/proposals/)
- [Embedding the router in your application](/docs/applications/embedding)
- [How to Set up a Reseed Server](/docs/guides/reseed-server)
- [Ports used by I2P](/docs/overview/ports)
- [Project Roadmap](/get-involved/roadmap/)
- [Ancient invisiblenet I2P documents - 2003](/docs/historical/)
