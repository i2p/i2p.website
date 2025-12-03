---
title: "I2P Threat Model"
description: "Catalogue of attacks considered in I2P’s design and the mitigations in place"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
aliases:
  - /en/docs/how/threat-model
  - /how/threat-model/
  - /docs/overview/threat-model
  - /docs/overview/threat-model/
  - /docs/how/threat-model/
  - /en/docs/how/threat-model/
---

> **Status:**  
> This document supersedes the historical 0.8.x-era threat model.  
> It reflects I2P’s current design as of October 2025.  
> Legacy cryptographic and transport protocols (ElGamal, AES, NTCP1, SSU1) are now fully deprecated.  
> All modern communication is based on the **Noise Protocol Framework** using **X25519 + ChaCha20/Poly1305**.  
> The goal remains unchanged: preserve anonymity and resilience against realistic adversaries while maintaining backward compatibility.

---

## 1  What “Anonymous” Means

I2P provides *practical anonymity*—not invisibility.  
Anonymity is defined as the difficulty for an adversary to learn information you wish to keep private: who you are, where you are, or who you talk to.  
Absolute anonymity is impossible; instead, I2P aims for **sufficient anonymity** under global passive and active adversaries.

Your anonymity depends on how you configure I2P, how you choose peers and subscriptions, and what applications you expose.

---

## 2  Cryptographic and Transport Evolution (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>

**Current cryptographic suite (Noise XK):**
- **X25519** for key exchange  
- **ChaCha20/Poly1305 AEAD** for encryption  
- **Ed25519 (EdDSA-SHA512)** for signatures  
- **SHA-256** for hashing and HKDF  
- Optional **ML-KEM hybrids** for post-quantum testing

All ElGamal and AES-CBC usages have been retired.  
Transport is entirely NTCP2 ( TCP ) and SSU2 ( UDP ); both support IPv4/IPv6, forward secrecy, and DPI obfuscation.

---

## 3  Network Architecture Summary

- **Free-route mixnet:** Senders and receivers each define their own tunnels.  
- **No central authority:** Routing and naming are decentralized; each router maintains local trust.  
- **Unidirectional tunnels:** Inbound and outbound are separate (10 min lifetimes).  
- **Exploratory tunnels:** 2 hops by default; client tunnels 2–3 hops.  
- **Floodfill routers:** ~1 700 of ~55 000 nodes (~6 %) maintain the distributed NetDB.  
- **NetDB rotation:** Keyspace rotates daily at UTC midnight.  
- **Sub-DB isolation:** Since 2.4.0, each client and router use separate databases to prevent linking.

---

## 4  Attack Categories and Current Defenses

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>

---

## 5  Modern Network Database (NetDB)

**Core facts (still accurate):**
- Modified Kademlia DHT stores RouterInfo and LeaseSets.  
- SHA-256 key hashing; parallel queries to 2 closest floodfills with 10 s timeout.  
- LeaseSet lifetime ≈ 10 min (LeaseSet2) or 18 h (MetaLeaseSet).

**New types (since 0.9.38):**
- **LeaseSet2 (Type 3)** – multiple encryption types, timestamped.  
- **EncryptedLeaseSet2 (Type 5)** – blinded destination for private services (DH or PSK auth).  
- **MetaLeaseSet (Type 7)** – multihoming and extended expirations.

**Major security upgrade – Sub-DB Isolation (2.4.0):**
- Prevents router↔client association.  
- Each client and router use separate netDb segments.  
- Verified and audited (2.5.0).

---

## 6  Hidden Mode and Restricted Routes

- **Hidden Mode:** Implemented (automatic in strict countries per Freedom House scores).  
    Routers don’t publish RouterInfo or route traffic.  
- **Restricted Routes:** Partially implemented (basic trust-only tunnels).  
    Comprehensive trusted-peer routing remains planned (3.0+).

Trade-off: Better privacy ↔ reduced contribution to network capacity.

---

## 7  DoS and Floodfill Attacks

**Historical:** 2013 UCSB research showed Eclipse and Floodfill takeovers possible.  
**Modern defenses include:**
- Daily keyspace rotation.  
- Floodfill cap ≈ 500, one per /16.  
- Randomized storage verification delays.  
- Newer-router preference (2.6.0).  
- Automatic enrollment fix (2.9.0).  
- Congestion-aware routing and lease throttling (2.4.0+).  

Floodfill attacks remain theoretically possible but practically harder.

---

## 8  Traffic Analysis and Censorship

I2P traffic is hard to identify: no fixed port, no plaintext handshake, and random padding.  
NTCP2 and SSU2 packets mimic common protocols and use ChaCha20 header obfuscation.  
Padding strategies are basic (random sizes), dummy traffic is not implemented (costly).  
Connections from Tor exit nodes are blocked since 2.6.0 (to protect resources).  

---

## 9  Persistent Limitations (acknowledged)

- Timing correlation for low-latency apps remains a fundamental risk.  
- Intersection attacks still powerful against known public destinations.  
- Sybil attacks lack complete defense (HashCash not enforced).  
- Constant-rate traffic and nontrivial delays remain unimplemented (planned 3.0).  

Transparency about these limits is intentional — it prevents users from over-estimating anonymity.

---

## 10  Network Statistics (2025)

- ~55 000 active routers worldwide (↑ from 7 000 in 2013)  
- ~1 700 floodfill routers (~6 %)  
- 95 % participate in tunnel routing by default  
- Bandwidth tiers: K (<12 KB/s) → X (>2 MB/s)  
- Minimum floodfill rate: 128 KB/s  
- Router console Java 8+ (required), Java 17+ planned next cycle

---

## 11  Development and Central Resources

- Official site: </>  
- Docs: <//en/docs>  
- Debian repository: <https://deb.i2pgit.org> ( replaced deb.i2p2.de in Oct 2023 )  
- Source code: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub mirror  
- All releases are signed SU3 containers (RSA-4096, zzz/str4d keys)  
- No active mailing lists; community via <https://i2pforum.net> and IRC2P.  
- Update cycle: 6–8 weeks stable releases.  

---

## 12  Summary of Security Improvements Since 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>

---

## 13  Known Unsolved or Planned Work

- Comprehensive restricted routes (trusted-peer routing) → planned 3.0.  
- Non-trivial delay/batching for timing resistance → planned 3.0.  
- Advanced padding and dummy traffic → unimplemented.  
- HashCash identity verification → infrastructure exists but inactive.  
- R5N DHT replacement → proposal only.  

---

## 14  Key References

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [I2P Official Documentation](/docs/)  

---

## 15  Conclusion

I2P’s core anonymity model has stood for two decades: sacrifice global uniqueness for local trust and security.  
From ElGamal to X25519, NTCP to NTCP2, and from manual reseeds to Sub-DB isolation, the project has evolved while maintaining its philosophy of defense in depth and transparency.

Many attacks remain theoretically possible against any low-latency mixnet, but I2P’s continuous hardening makes them increasingly impractical.  
The network is larger, faster, and more secure than ever — yet still honest about its limits.
