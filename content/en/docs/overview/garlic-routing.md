---
title: "Garlic Routing"
description: "Understanding garlic routing terminology, architecture, and modern implementation in I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Overview

**Garlic routing** remains one of I2P’s core innovations, combining layered encryption, message bundling, and unidirectional tunnels.  
While conceptually similar to **onion routing**, it extends the model to bundle multiple encrypted messages (“cloves”) in a single envelope (“garlic”), improving efficiency and anonymity.

The term *garlic routing* was coined by [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) in [Roger Dingledine’s Free Haven Master’s Thesis](https://www.freehaven.net/papers.html) (June 2000, §8.1.1).  
I2P developers adopted the term in the early 2000s to reflect its bundling enhancements and unidirectional transport model, distinguishing it from Tor’s circuit‑switched design.

> **Summary:** Garlic routing = layered encryption + message bundling + anonymous delivery via unidirectional tunnels.

---

## 2. The “Garlic” Terminology

Historically, the term *garlic* has been used in three different contexts within I2P:

1. **Layered encryption** – tunnel‑level onion‑style protection  
2. **Bundling multiple messages** – multiple “cloves” inside a “garlic message”  
3. **End‑to‑end encryption** – formerly *ElGamal/AES+SessionTags*, now *ECIES‑X25519‑AEAD‑Ratchet*

While the architecture remains intact, the encryption scheme has been completely modernized.

---

## 3. Layered Encryption

Garlic routing shares its foundational principle with onion routing:  
each router decrypts only one layer of encryption, learning only the next hop and not the full path.

However, I2P implements **unidirectional tunnels**, not bidirectional circuits:

- **Outbound tunnel**: sends messages away from the creator  
- **Inbound tunnel**: carries messages back to the creator  

A full round trip (Alice ↔ Bob) uses four tunnels:  
Alice’s outbound → Bob’s inbound, then Bob’s outbound → Alice’s inbound.  
This design **halves correlation data exposure** compared to bidirectional circuits.

For tunnel implementation details, see the [Tunnel Operations Guide](/docs/specs/implementation/).

---

## 4. Bundling Multiple Messages (The “Cloves”)

Freedman’s original garlic routing envisioned bundling multiple encrypted “bulbs” within one message.  
I2P implements this as **cloves** inside a **garlic message** — each clove has its own encrypted delivery instructions and target (router, destination, or tunnel).

Garlic bundling allows I2P to:

- Combine acknowledgments and metadata with data messages  
- Reduce observable traffic patterns  
- Support complex message structures without extra connections

![Garlic Message Cloves](/images/garliccloves.png)  
*Figure 1: A Garlic Message containing multiple cloves, each with its own delivery instructions.*

Typical cloves include:

1. **Delivery Status Message** — acknowledgments confirming delivery success or failure.  
   These are wrapped in their own garlic layer to preserve confidentiality.
2. **Database Store Message** — automatically bundled LeaseSets so peers can reply without re‑querying the netDb.

Cloves are bundled when:

- A new LeaseSet must be published  
- New session tags are delivered  
- No bundle has occurred recently (~1 minute by default)

Garlic messages achieve efficient end‑to‑end delivery of multiple encrypted components in a single packet.

---

## 5. Encryption Evolution

### 5.1 Historical Context

Early documentation (≤ v0.9.12) described *ElGamal/AES+SessionTags* encryption:  
- **ElGamal 2048‑bit** wrapped AES session keys  
- **AES‑256/CBC** for payload encryption  
- 32‑byte session tags used once per message  

That cryptosystem is **deprecated**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Between 2019 and 2023, I2P migrated entirely to ECIES‑X25519‑AEAD‑Ratchet. The modern stack standardizes the following components:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>

Benefits of the ECIES migration:

- **Forward secrecy** via per-message ratcheting keys  
- **Reduced payload size** compared to ElGamal  
- **Resilience** against cryptanalytic advances  
- **Compatibility** with future post-quantum hybrids (see Proposal 169)

Additional details: see the [ECIES Specification](/docs/specs/ecies) and [EncryptedLeaseSet specification](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Garlic envelopes frequently include LeaseSets to publish or update destination reachability.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>

All LeaseSets are distributed through the *floodfill DHT* maintained by specialized routers. Publications are verified, timestamped, and rate-limited to reduce metadata correlation.

See the [Network Database documentation](/docs/specs/common-structures) for details.

---

## 7. Modern “Garlic” Applications within I2P

Garlic-based encryption and message bundling are used throughout the I2P protocol stack:

1. **Tunnel creation and usage** — layered encryption per hop  
2. **End-to-end message delivery** — bundled garlic messages with cloned-acknowledgment and LeaseSet cloves  
3. **Network Database publishing** — LeaseSets wrapped in garlic envelopes for privacy  
4. **SSU2 and NTCP2 transports** — underlay encryption using Noise framework and X25519/ChaCha20 primitives  

Garlic routing is thus both a *method of encryption layering* and a *network messaging model*.

---

## 8. Current Documentation and References

I2P's documentation hub is [available here](/docs/), maintained continuously.  
Relevant living specifications include:

- [ECIES Specification](/docs/specs/ecies/) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel Operations Guide](/docs/specs/implementation/) — tunnel creation and encryption
- [I2NP Specification](/docs/specs/i2np/) — I2NP message formats
- [SSU2 Specification](/docs/specs/ssu2) — SSU2 UDP transport
- [Common Structures](/docs/specs/common-structures) — netDb and floodfill behavior

Academic validation:  
Hoang et al. (IMC 2018, USENIX FOCI 2019) and Muntaka et al. (2025) confirm the architectural stability and operational resilience of I2P’s design.

---

## 9. Future Work

Ongoing proposals:

- **Proposal 169:** Hybrid post-quantum (ML-KEM 512/768/1024 + X25519)  
- **Proposal 168:** Transport bandwidth optimization  
- **Datagram and streaming updates:** Enhanced congestion management  

Future adaptations may include additional message delay strategies or multi-tunnel redundancy at the garlic-message level, building on unused delivery options originally described by Freedman.

---

## 10. References

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
