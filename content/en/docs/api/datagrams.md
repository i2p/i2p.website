---
title: "Datagrams"
description: "Authenticated, repliable, and raw message formats above I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
aliases:
  - /docs/api/datagrams/
---

## Overview

Datagrams provide message-oriented communication above [I2CP](/docs/specs/i2cp/) and parallel to the streaming library.  
They enable **repliable**, **authenticated**, or **raw** packets without requiring connection-oriented streams.  
Routers encapsulate datagrams into I2NP messages and tunnel messages, regardless of whether NTCP2 or SSU2 carries the traffic.

The core motivation is to allow applications (like trackers, DNS resolvers, or games) to send self-contained packets that identify their sender.

> **New in 2025:** The I2P Project approved **Datagram2 (protocol 19)** and **Datagram3 (protocol 20)**, adding replay protection and lower-overhead repliable messaging for the first time in a decade.

---

## 1. Protocol Constants

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>

Protocols 19 and 20 were formalized in **Proposal 163 (April 2025)**.  
They coexist with Datagram1 / RAW for backward compatibility.

---

## 2. Datagram Types

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>

### Typical Design Patterns
- **Request → Response:** Send a signed Datagram2 (request + nonce), receive a raw or Datagram3 reply (echo nonce).  
- **High-frequency/low-overhead:** Prefer Datagram3 or RAW.  
- **Authenticated control messages:** Datagram2.  
- **Legacy compatibility:** Datagram1 still fully supported.

---

## 3. Datagram2 and Datagram3 Details (2025)

### Datagram2 (Protocol 19)
Enhanced replacement for Datagram1.  
Features:
- **Replay prevention:** 4-byte anti-replay token.  
- **Offline signature support:** enables use by offline-signed Destinations.  
- **Expanded signature coverage:** includes destination hash, flags, options, offline sig block, payload.  
- **Post-quantum ready:** compatible with future ML-KEM hybrids.  
- **Overhead:** ≈ 457 bytes (X25519 keys).  

### Datagram3 (Protocol 20)
Bridges gap between raw and signed types.  
Features:
- **Repliable without signature:** contains sender’s 32-byte hash + 2-byte flags.  
- **Tiny overhead:** ≈ 34 bytes.  
- **No replay defense** — application must implement.  

Both protocols are API 0.9.66 features and implemented in the Java router since Release 2.9.0; no i2pd or Go implementations yet (October 2025).

---

## 4. Size and Fragmentation Limits

- **Tunnel message size:** 1 028 bytes (4 B Tunnel ID + 16 B IV + 1 008 B payload).  
- **Initial fragment:** 956 B (typical TUNNEL delivery).  
- **Follow-on fragment:** 996 B.  
- **Max fragments:** 63–64.  
- **Practical limit:** ≈ 62 708 B (~61 KB).  
- **Recommended limit:** ≤ 10 KB for reliable delivery (drops increase exponentially beyond this).

**Overhead summary:**
- Datagram1 ≈ 427 B (minimum).  
- Datagram2 ≈ 457 B.  
- Datagram3 ≈ 34 B.  
- Additional layers (I2CP gzip header, I2NP, Garlic, Tunnel): + ~5.5 KB worst case.

---

## 5. I2CP / I2NP Integration

Message path:
1. Application creates datagram (via I2P API or SAM).  
2. I2CP wraps with gzip header (`0x1F 0x8B 0x08`, RFC 1952) and CRC-32 checksum.  
3. Protocol + Port numbers stored in gzip header fields.  
4. Router encapsulates as I2NP message → Garlic clove → 1 KB tunnel fragments.  
5. Fragments traverse outbound → network → inbound tunnel.  
6. Reassembled datagram delivered to application handler based on protocol number.  

**Integrity:** CRC-32 (from I2CP) + optional cryptographic signature (Datagram1/2).  
There is no separate checksum field within the datagram itself.

---

## 6. Programming Interfaces

### Java API
Package `net.i2p.client.datagram` includes:
- `I2PDatagramMaker` – builds signed datagrams.  
- `I2PDatagramDissector` – verifies and extracts sender info.  
- `I2PInvalidDatagramException` – thrown on verification failure.  

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) manages protocol and port multiplexing for apps sharing a Destination.

**Javadoc access:**
- [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (I2P network only)
- [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (clearnet mirror)
- [Official Javadocs](http://docs.i2p-projekt.de/javadoc/) (official docs)

### SAM v3 Support
- SAM 3.2 (2016): added PORT and PROTOCOL parameters.  
- SAM 3.3 (2016): introduced PRIMARY/subsession model; allows streams + datagrams on one Destination.  
- Support for Datagram2 / 3 session styles added spec 2025 (implementation pending).  
- Official spec: </docs/api/samv3/>

### i2ptunnel Modules
- **udpTunnel:** Fully functional base for I2P UDP apps (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Operational for A/V streaming (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Not functional** as of 2.10.0 (UDP stub only).  

> For general-purpose UDP, use the Datagram API or udpTunnel directly—do not rely on SOCKS UDP.

---

## 7. Ecosystem and Language Support (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>

Java I2P is the only router supporting full SAM 3.3 subsessions and Datagram2 API at this time.

---

## 8. Example Usage – UDP Tracker (I2PSnark 2.10.0)

First real-world application of Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>

Pattern demonstrates mixed use of authenticated and lightweight datagrams to balance security and performance.

---

## 9. Security and Best Practices

- Use Datagram2 for any authenticated exchange or when replay attacks matter.  
- Prefer Datagram3 for fast repliable responses with moderate trust.  
- Use RAW for public broadcasts or anonymous data.  
- Keep payloads ≤ 10 KB for reliable delivery.  
- Be aware that SOCKS UDP remains non-functional.  
- Always verify gzip CRC and digital signatures on receipt.

---

## 10. Technical Specification

This section covers the low-level datagram formats, encapsulation, and protocol details.

### 10.1 Protocol Identification

Datagram formats **do not** share a common header. Routers cannot infer the type from payload bytes alone.

When mixing multiple datagram types—or when combining datagrams with streaming—explicitly set:
- The **protocol number** (via I2CP or SAM)
- Optionally the **port number**, if your application multiplexes services

Leaving the protocol unset (`0` or `PROTO_ANY`) is discouraged and may lead to routing or delivery errors.

### 10.2 Raw Datagrams

Non-repliable datagrams carry no sender or authentication data. They are opaque payloads, handled outside the higher-level datagram API but supported via SAM and I2PTunnel.

**Protocol:** `18` (`PROTO_DATAGRAM_RAW`)

**Format:**
```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```

Payload length is constrained by transport limits (≈32 KB practical max, often much less).

### 10.3 Datagram1 (Repliable Datagrams)

Embeds sender's **Destination** and a **Signature** for authentication and reply addressing.

**Protocol:** `17` (`PROTO_DATAGRAM`)

**Overhead:** ≥427 bytes
**Payload:** up to ~31.5 KB (limited by transport)

**Format:**
```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```

- `from`: a Destination (387+ bytes)
- `signature`: a Signature matching the key type
  - For DSA_SHA1: Signature of the SHA-256 hash of the payload
  - For other key types: Signature directly over the payload

**Notes:**
- Signatures for non-DSA types were standardized in I2P 0.9.14.
- LS2 (Proposal 123) offline signatures are not currently supported in Datagram1.

### 10.4 Datagram2 Format

An improved repliable datagram that adds **replay resistance** as defined in [Proposal 163](/proposals/163-datagram2/).

**Protocol:** `19` (`PROTO_DATAGRAM2`)

Implementation is ongoing. Applications should include nonce or timestamp checks for redundancy.

### 10.5 Datagram3 Format

Provides **repliable but unauthenticated** datagrams. Relies on router-maintained session authentication rather than embedded destination and signature.

**Protocol:** `20` (`PROTO_DATAGRAM3`)
**Status:** Under development since 0.9.66

Useful when:
- Destinations are large (e.g., post-quantum keys)
- Authentication occurs at another layer
- Bandwidth efficiency is critical

### 10.6 Data Integrity

Datagram integrity is protected by the **gzip CRC-32 checksum** in the I2CP layer.
No explicit checksum field exists within the datagram payload format itself.

### 10.7 Packet Encapsulation

Each datagram is encapsulated as a single I2NP message or as an individual clove in a **Garlic Message**.
I2CP, I2NP, and tunnel layers handle length and framing — there is no internal delimiter or length field in the datagram protocol.

### 10.8 Post-Quantum (PQ) Considerations

If **Proposal 169** (ML-DSA signatures) is implemented, signature and destination sizes will rise dramatically — from ~455 bytes to **≥3739 bytes**.
This change will substantially increase datagram overhead and reduce effective payload capacity.

**Datagram3**, which relies on session-level authentication (not embedded signatures), will likely become the preferred design in post-quantum I2P environments.

---

## 11. References

- [Proposal 163 – Datagram2 and Datagram3](/proposals/163-datagram2/)
- [Proposal 160 – UDP Tracker Integration](/proposals/160-udp-trackers/)
- [Proposal 144 – Streaming MTU Calculations](/proposals/144-ecies-x25519-aead-ratchet/)
- [Proposal 169 – Post-Quantum Signatures](/proposals/169-pq-crypto/)
- [I2CP Specification](/docs/specs/i2cp/)
- [I2NP Specification](/docs/specs/i2np/)
- [Tunnel Message Specification](/docs/specs/implementation/)
- [SAM v3 Specification](/docs/api/samv3/)
- [i2ptunnel Documentation](/docs/api/i2ptunnel/)

## 12. Change Log Highlights (2019 – 2025)

| Year | Release | Change |
|------|:-------:|--------|
| 2019 | 0.9.43 | Datagram API stabilization |
| 2021 | 0.9.50 | Protocol port handling reworked |
| 2022 | 2.0.0 | SSU2 adoption completed |
| 2024 | 2.6.0 | Legacy transport removal simplified UDP code |
| 2025 | 2.9.0 | Datagram2/3 support added (Java API) |
| 2025 | 2.10.0 | UDP Tracker implementation released |

---

## 13. Summary

The datagram subsystem now supports four protocol variants offering a spectrum from fully-authenticated to lightweight raw transmission.  
Developers should migrate toward **Datagram2** for security-sensitive use cases and **Datagram3** for efficient repliable traffic.  
All older types remain compatible to ensure long-term interoperability.
