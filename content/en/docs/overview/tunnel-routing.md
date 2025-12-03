---
title: "Tunnel Routing"
description: "Overview of I2P tunnel terminology, construction, and lifecycle"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /en/docs/how/tunnel-routing/
---


## Overview

I2P builds temporary, unidirectional tunnels — ordered sequences of routers that forward encrypted traffic.  
Tunnels are classified as **inbound** (messages flow toward the creator) or **outbound** (messages flow away from the creator).  

A typical exchange routes Alice’s message out through one of her outbound tunnels, instructs the outbound endpoint to forward it to the gateway of one of Bob’s inbound tunnels, and then Bob receives it at his inbound endpoint.

![Alice connecting through her outbound tunnel to Bob via his inbound tunnel](/images/tunnelSending.png)

A: Outbound Gateway (Alice)  
B: Outbound Participant  
C: Outbound Endpoint  
D: Inbound Gateway  
E: Inbound Participant  
F: Inbound Endpoint (Bob)

Tunnels have a fixed lifetime of 10 minutes and carry fixed‑size messages of 1024 bytes (1028 bytes including the tunnel header) to prevent traffic analysis based on message size or timing patterns.

## Tunnel Vocabulary

- **Tunnel gateway:** First router in a tunnel. For inbound tunnels, this router’s identity appears in the published [LeaseSet](/docs/specs/common-structures/). For outbound tunnels, the gateway is the originating router (A and D above).  
- **Tunnel endpoint:** Last router in a tunnel (C and F above).  
- **Tunnel participant:** Intermediate router in a tunnel (B and E above). Participants cannot determine their position or tunnel direction.  
- **n‑hop tunnel:** Number of inter‑router hops.  
  - **0‑hop:** Gateway and endpoint are the same router – minimal anonymity.  
  - **1‑hop:** Gateway connects directly to endpoint – low latency, low anonymity.  
  - **2‑hop:** Default for exploratory tunnels; balanced security/performance.  
  - **3‑hop:** Recommended for applications requiring strong anonymity.  
- **Tunnel ID:** 4‑byte integer unique per router and per hop, randomly chosen by the creator. Each hop receives and forwards on different IDs.

## Tunnel Build Information

Routers filling gateway, participant, and endpoint roles receive different records within the Tunnel Build Message.  
Modern I2P supports two methods:  

- **ElGamal** (legacy, 528‑byte records)  
- **ECIES‑X25519** (current, 218‑byte records via Short Tunnel Build Message – STBM)  

### Information Distributed to Participants

**Gateway receives:**  
- Tunnel layer key (AES‑256 or ChaCha20 key depending on tunnel type)  
- Tunnel IV key (for encrypting initialization vectors)  
- Reply key and reply IV (for build reply encryption)  
- Tunnel ID (inbound gateways only)  
- Next hop identity hash and tunnel ID (if non‑terminal)  

**Intermediate participants receive:**  
- Tunnel layer key and IV key for their hop  
- Tunnel ID and next hop info  
- Reply key and IV for build response encryption  

**Endpoints receive:**  
- Tunnel layer and IV keys  
- Reply router and tunnel ID (outbound endpoints only)  
- Reply key and IV (outbound endpoints only)

For full details see the [Tunnel Creation Specification](/docs/specs/implementation/) and [ECIES Tunnel Creation Specification](/docs/specs/implementation/).

## Tunnel Pooling

Routers group tunnels into **tunnel pools** for redundancy and load distribution. Each pool maintains multiple parallel tunnels, allowing failover when one fails. Pools used internally are **exploratory tunnels**, while application‑specific pools are **client tunnels**.

Each destination maintains separate inbound and outbound pools configured by I2CP options (tunnel count, backup count, length, and QoS parameters). Routers monitor tunnel health, run periodic tests, and rebuild failed tunnels automatically to maintain pool size.

## Tunnel Length

### 0‑hop Tunnels
Offer only plausible deniability. Traffic always originates and terminates at the same router — discouraged for any anonymous use.

### 1‑hop Tunnels
Provide basic anonymity against passive observers but are vulnerable if an adversary controls that single hop.

### 2‑hop Tunnels
Include two remote routers and substantially increase attack cost. Default for exploratory pools.

### 3‑hop Tunnels
Recommended for applications requiring robust anonymity protection. Extra hops add latency without meaningful security gain.

### Defaults
Routers use **2‑hop** exploratory tunnels and application‑specific **2 or 3 hop** client tunnels, balancing performance and anonymity.

## Tunnel Testing

Routers periodically test tunnels by sending a `DeliveryStatusMessage` through an outbound tunnel to an inbound tunnel.  
If the test fails, both tunnels receive negative profile weight. Consecutive failures mark a tunnel unusable; the router then rebuilds a replacement and publishes a new LeaseSet. Results feed into peer capacity metrics used by the [peer selection system](/docs/overview/tunnel-routing/).

## Tunnel Creation

Routers construct tunnels using a non‑interactive **telescoping** method: a single Tunnel Build Message propagates hop‑by‑hop.  
Each hop decrypts its record, adds its reply, and forwards the message on. The final hop returns the aggregate build reply via a different path, preventing correlation. Modern implementations use **Short Tunnel Build Messages (STBM)** for ECIES and **Variable Tunnel Build Messages (VTBM)** for legacy paths. Each record is encrypted per‑hop using ElGamal or ECIES‑X25519.

## Tunnel Encryption

Tunnel traffic uses multi‑layer encryption. Each hop adds or removes a layer of encryption as messages traverse the tunnel.   

- **ElGamal tunnels:** AES‑256/CBC for payloads with PKCS#5 padding.  
- **ECIES tunnels:** ChaCha20 or ChaCha20‑Poly1305 for authenticated encryption.  

Each hop has two keys: a **layer key** and an **IV key**. Routers decrypt the IV, use it to process the payload, then re‑encrypt the IV before forwarding. This double IV scheme prevents message tagging.  

Outbound gateways pre‑decrypt all layers so that endpoints receive plaintext after all participants have added encryption. Inbound tunnels encrypt in the opposite direction. Participants cannot determine tunnel direction or length.

## Ongoing Development

- Dynamic tunnel lifetimes and adaptive pool sizing for network load balancing  
- Alternate tunnel testing strategies and individual hop diagnostics  
- Optional proof‑of‑work or bandwidth certificate validation (implemented in API 0.9.65+)  
- Traffic shaping and chaff insertion research for endpoint mixing  
- Continued retirement of ElGamal and migration to ECIES‑X25519  

## See Also

- [Tunnel Implementation Specification](/docs/specs/implementation/)  
- [Tunnel Creation Specification (ElGamal)](/docs/specs/implementation/)  
- [Tunnel Creation Specification (ECIES‑X25519)](/docs/specs/implementation/)  
- [Tunnel Message Specification](/docs/specs/implementation/)  
- [Garlic Routing](/docs/overview/garlic-routing/)  
- [I2P Network Database](/docs/specs/common-structures/)  
- [Peer Profiling and Selection](/docs/overview/tunnel-routing/)  
- [I2P Threat Model](/docs/overview/threat-model/)  
- [ElGamal/AES + SessionTag Encryption](/docs/legacy/elgamal-aes/)  
- [I2CP Options](/docs/specs/i2cp/)
