---
title: "I2P: A scalable framework for anonymous communication"
description: "Technical introduction to I2P architecture and operation"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Introduction

I2P is a scalable, self-organizing, resilient packet-switched anonymous network layer, upon which any number of different anonymity or security-conscious applications can operate. Each of these applications may make their own anonymity, latency, and throughput tradeoffs without worrying about the proper implementation of a free route mixnet, allowing them to blend their activity with the larger anonymity set of users already running on top of I2P.

Applications already available provide the full range of typical Internet activities — **anonymous** web browsing, web hosting, chat, file sharing, e-mail, blogging, and content syndication, as well as several other applications under development.

- **Web browsing:** using any existing browser that supports a proxy  
- **Chat:** IRC and other protocols  
- **File sharing:** [I2PSnark](#i2psnark) and other applications  
- **E-mail:** [Susimail](#i2pmail) and other applications  
- **Blog:** using any local web server, or available plugins

Unlike websites hosted within content distribution networks like [Freenet](/docs/overview/comparison#freenet) or [GNUnet](https://www.gnunet.org/), the services hosted on I2P are fully interactive — there are traditional web-style search engines, bulletin boards, blogs you can comment on, database-driven sites, and bridges to query static systems like Freenet without needing to install them locally.

With all of these anonymity-enabled applications, I2P acts as **message-oriented middleware** — applications specify data to send to a cryptographic identifier (a “destination”), and I2P ensures it arrives securely and anonymously. I2P also includes a simple [streaming library](#streaming) to allow I2P’s anonymous best-effort messages to transfer as reliable, in-order streams, offering TCP-based congestion control tuned for the network’s high bandwidth-delay product.

While simple SOCKS proxies have been developed to connect existing applications, their value is limited since most applications leak sensitive information in an anonymous context. The safest approach is to **audit and adapt** the application to use I2P’s APIs directly.

I2P is not a research project — academic, commercial, or governmental — but an engineering effort aimed at providing usable anonymity. It has been in continuous development since early 2003 by a distributed group of contributors worldwide. All I2P work is **open source** on the [official website](https://geti2p.net/), primarily released into the public domain, with some components under permissive BSD-style licenses. Several GPL-licensed client applications are available, such as [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail), and [I2PSnark](#i2psnark).  
Funding comes solely from user donations.

---

## Operation

### Overview

I2P distinguishes clearly between routers (nodes participating in the network) and destinations (anonymous endpoints for applications). Running I2P itself is not secret; what’s hidden is **what** the user is doing and which router their destinations use. End users typically run several destinations (e.g., one for web browsing, another for hosting, another for IRC).

A key concept in I2P is the **tunnel** — a unidirectional encrypted path through a series of routers. Each router only decrypts one layer and only learns the next hop. Tunnels expire every 10 minutes and must be rebuilt.

![Inbound and outbound tunnel schematic](/images/tunnels.png)  
*Figure 1: Two types of tunnels exist — inbound and outbound.*

- **Outbound tunnels** send messages away from the creator.  
- **Inbound tunnels** bring messages back to the creator.

Combining these enables two-way communication. For example, “Alice” uses an outbound tunnel to send to “Bob’s” inbound tunnel. Alice encrypts her message with routing instructions to Bob’s inbound gateway.

Another key concept is the **network database** or **netDb**, which distributes metadata about routers and destinations:

- **RouterInfo:** Contains router contact and key material.  
- **LeaseSet:** Contains information needed to contact a destination (tunnel gateways, expiry times, encryption keys).  

Routers publish their RouterInfo directly to the netDb; LeaseSets are sent through outbound tunnels for anonymity.

To build tunnels, Alice queries the netDb for RouterInfo entries to choose peers, and sends encrypted tunnel build messages hop-by-hop until the tunnel is complete.

![Router information is used to build tunnels](/images/netdb_get_routerinfo_2.png)  
*Figure 2: Router information is used to build tunnels.*

To send to Bob, Alice looks up Bob’s LeaseSet and uses one of her outbound tunnels to route data through to Bob’s inbound tunnel gateway.

![LeaseSets connect inbound and outbound tunnels](/images/netdb_get_leaseset.png)  
*Figure 3: LeaseSets connect outbound and inbound tunnels.*

Because I2P is message-based, it adds **end-to-end garlic encryption** to protect messages even from the outbound endpoint or inbound gateway. A garlic message wraps multiple encrypted “cloves” (messages) to hide metadata and improve anonymity.

Applications can either use the message interface directly or rely on the [streaming library](#streaming) for reliable connections.

---

### Tunnels

Both inbound and outbound tunnels use layered encryption, but differ in construction:

- In **inbound tunnels**, the creator (the endpoint) decrypts all layers.
- In **outbound tunnels**, the creator (the gateway) pre-decrypts layers to ensure clarity at the endpoint.

I2P profiles peers via indirect metrics such as latency and reliability without direct probing. Based on these profiles, peers are grouped dynamically into four tiers:

1. Fast and high capacity  
2. High capacity  
3. Not failing  
4. Failing  

Tunnel peer selection typically prefers high-capacity peers, randomly chosen to balance anonymity and performance, with additional XOR-based ordering strategies to mitigate predecessor attacks and netDb harvesting.

For deeper details, see the [Tunnel Specification](/docs/specs/implementation).

---

### Network Database (netDb)

Routers participating in the **floodfill** distributed hash table (DHT) store and respond to LeaseSet lookups. The DHT uses a variant of [Kademlia](https://en.wikipedia.org/wiki/Kademlia).  
Floodfill routers are selected automatically if they have enough capacity and stability, or may be configured manually.

- **RouterInfo:** Describes a router’s capabilities and transports.  
- **LeaseSet:** Describes a destination’s tunnels and encryption keys.  

All data in the netDb is signed by the publisher and timestamped to prevent replay or stale entry attacks. Timing synchronization is maintained through SNTP and transport-layer skew detection.

#### Additional concepts

- **Unpublished and encrypted LeaseSets:**  
  A destination may remain private by not publishing its LeaseSet, sharing it only with trusted peers. Access requires the appropriate decryption key.

- **Bootstrapping (reseeding):**  
  To join the network, a new router fetches signed RouterInfo files from trusted HTTPS reseed servers.

- **Lookup scalability:**  
  I2P uses **iterative**, not recursive, lookups to improve DHT scalability and security.

---

### Transport Protocols

Modern I2P communication uses two fully encrypted transports:

- **[NTCP2](/docs/specs/ntcp2):** Encrypted TCP-based protocol  
- **[SSU2](/docs/specs/ssu2):** Encrypted UDP-based protocol

Both are built on the modern [Noise Protocol Framework](https://noiseprotocol.org/), providing strong authentication and resistance to traffic fingerprinting. They replaced legacy NTCP and SSU protocols (fully retired since 2023).

**NTCP2** offers encrypted, efficient streaming over TCP.

**SSU2** provides UDP-based reliability, NAT traversal, and optional hole punching.  
SSU2 is conceptually similar to WireGuard or QUIC, balancing reliability and anonymity.

Routers may support both IPv4 and IPv6, publishing their transport addresses and costs in the netDb. A connection’s transport is selected dynamically by a **bidding system** that optimizes for conditions and existing links.

---

### Cryptography

I2P uses layered cryptography for all components: transports, tunnels, garlic messages, and the network database.

Current primitives include:

- X25519 for key exchange  
- EdDSA (Ed25519) for signatures  
- ChaCha20-Poly1305 for authenticated encryption  
- SHA-256 for hashing  
- AES256 for tunnel layer encryption  

Legacy algorithms (ElGamal, DSA-SHA1, ECDSA) remain for backward compatibility.

I2P is currently introducing hybrid post-quantum (PQ) cryptographic schemes combining **X25519** with **ML-KEM** to resist “harvest-now, decrypt-later” attacks.

#### Garlic Messages

Garlic messages extend onion routing by grouping multiple encrypted “cloves” with independent delivery instructions. These allow message-level routing flexibility and uniform traffic padding.

#### Session Tags

Two cryptographic systems are supported for end-to-end encryption:

- **ElGamal/AES+SessionTags (legacy):**  
  Uses pre-delivered session tags as 32-byte nonces. Now deprecated due to inefficiency.

- **ECIES-X25519-AEAD-Ratchet (current):**  
  Uses ChaCha20-Poly1305 and synchronized HKDF-based PRNGs to generate ephemeral session keys and 8-byte tags dynamically, reducing CPU, memory, and bandwidth overhead while maintaining forward secrecy.

---

## Future of the Protocol

Key research areas focus on maintaining security against state-level adversaries and introducing post-quantum protections. Two early design concepts — **restricted routes** and **variable latency** — have been superseded by modern developments.

### Restricted Route Operation

Original restricted routing concepts aimed to obscure IP addresses.  
This need has been largely mitigated by:

- UPnP for automatic port forwarding  
- Robust NAT traversal in SSU2  
- IPv6 support  
- Cooperative introducers and NAT hole-punching  
- Optional overlay (e.g., Yggdrasil) connectivity

Thus, modern I2P achieves the same goals more practically without complex restricted routing.

---

## Similar Systems

I2P integrates concepts from message-oriented middleware, DHTs, and mixnets. Its innovation lies in combining these into a usable, self-organizing anonymity platform.

### Tor

*[Website](https://www.torproject.org/)*

**Tor** and **I2P** share goals but differ architecturally:

- **Tor:** Circuit-switched; relies on trusted directory authorities. (~10k relays)  
- **I2P:** Packet-switched; fully distributed DHT-driven network. (~50k routers)  

I2P’s unidirectional tunnels expose less metadata and allow flexible routing paths, while Tor focuses on anonymous **Internet access (outproxying)**.  
I2P instead supports anonymous **in-network hosting**.

### Freenet

*[Website](https://freenetproject.org/)*

**Freenet** focuses on anonymous, persistent file publishing and retrieval.  
**I2P**, in contrast, provides a **real-time communications layer** for interactive use (web, chat, torrents).  
Together, the two systems complement each other — Freenet provides censorship-resistant storage; I2P provides transport anonymity.

### Other Networks

- **Lokinet:** IP-based overlay using incentivized service nodes.  
- **Nym:** Next-generation mixnet emphasizing metadata protection with cover traffic at higher latency.

---

## Appendix A: Application Layer

I2P itself only handles message transport. Application-layer functionality is implemented externally through APIs and libraries.

### Streaming Library {#streaming}

The **streaming library** functions as I2P’s TCP analog, with a sliding window protocol and congestion control tuned for high-latency anonymous transport.  

Typical HTTP request/response patterns can often complete in a single round-trip due to message bundling optimizations.

### Naming Library and Address Book

*Developed by: mihi, Ragnarok*  
See the [Naming and Address Book](/docs/overview/naming) page.

I2P’s naming system is **local and decentralized**, avoiding DNS-style global names. Each router maintains a local mapping of human-readable names to destinations. Optional web-of-trust-based address books can be shared or imported from trusted peers.

This approach avoids centralized authorities and circumvents Sybil vulnerabilities inherent in global or voting-style naming systems.

### I2PTunnel {#i2ptunnel}

*Developed by: mihi*

**I2PTunnel** is the main client layer interface enabling anonymous TCP proxying.  
It supports:

- **Client tunnels** (outbound to I2P destinations)  
- **HTTP client (eepproxy)** for ".i2p" domains  
- **Server tunnels** (inbound from I2P to a local service)  
- **HTTP server tunnels** (securely proxy web services)  

Outproxying (to the regular Internet) is optional, implemented by volunteer-run “server” tunnels.

### I2PSnark {#i2psnark}

*Developed by: jrandom, et al — ported from [Snark](http://www.klomp.org/snark/)*

Bundled with I2P, **I2PSnark** is an anonymous multi-torrent BitTorrent client with DHT and UDP support, accessible via a web interface.

### I2Pmail / Susimail {#i2pmail}

*Developed by: postman, susi23, mastiejaner*

**I2Pmail** provides anonymous email through I2PTunnel connections.  
**Susimail** is a web-based client built specifically to prevent information leaks common in traditional email clients.  
The [mail.i2p](https://mail.i2p/) service features virus filtering, [hashcash](https://en.wikipedia.org/wiki/Hashcash) quotas, and outproxy separation for additional protection.

---
