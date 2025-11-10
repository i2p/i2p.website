---
title: "SSU2 Specification"
description: "Secure Semi-Reliable UDP Transport Protocol Version 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /en/docs/specs/ssu2
  - /spec/ssu2/
  - /docs/specs/ssu2/
  - /en/spec/ssu2/
---

## Status

This document defines the final SSU2 (Secure Semi-Reliable UDP version 2) protocol as implemented in all current I2P routers. SSU2 has fully replaced SSU1 as of **I2P 0.9.61 (Java)** and **i2pd 2.44.0**, providing improved security, performance, and NAT traversal.

For full technical and security background, refer to [Proposal 159](/proposals/159-ssu2/).

---

## 1. Overview

SSU2 is a UDP-based transport layer protocol used for secure, semi-reliable router-to-router communication in I2P. It is not a general-purpose transport but is specialized for **I2NP message exchange**.

### Core Capabilities

- Authenticated key exchange via Noise XK pattern
- Encrypted headers for DPI resistance
- NAT traversal using relays and hole-punching
- Connection migration and address validation
- Optional path validation
- Forward secrecy and replay protection

### Legacy and Compatibility

| Implementation | SSU2 Default | SSU1 Removed |
|----------------|--------------|--------------|
| i2pd | 2.44.0 | 2.44.0 |
| Java I2P | 0.9.56 | 0.9.61 |

SSU1 is no longer in use across the public I2P network.

---

## 2. Cryptography

SSU2 uses **Noise_XK_25519_ChaChaPoly_SHA256** with I2P-specific extensions.

| Function | Algorithm | Notes |
|-----------|------------|-------|
| Diffie-Hellman | X25519 (RFC 7748) | 32-byte keys |
| Cipher | ChaCha20/Poly1305 (RFC 7539) | AEAD encryption |
| Hash | SHA-256 | Used for key derivation and message integrity |
| KDF | HKDF-SHA256 (RFC 5869) | For session and header keys |

Headers and payloads are cryptographically bound via `mixHash()`.  
All cryptographic primitives are shared with NTCP2 and ECIES for implementation efficiency.

---

## 3. Message Overview

### 3.1 UDP Datagram Rules

- Each UDP datagram carries **exactly one SSU2 message**.  
- Session Confirmed messages may be fragmented across multiple datagrams.

**Minimum size:** 40 bytes  
**Maximum size:** 1472 bytes (IPv4) / 1452 bytes (IPv6)

### 3.2 Message Types

| Type | Message | Header | Description |
|------|----------|---------|-------------|
| 0 | Session Request | 32B | Handshake initiation |
| 1 | Session Created | 32B | Handshake response |
| 2 | Session Confirmed | 16B | Final handshake, may be fragmented |
| 6 | Data | 16B | Encrypted I2NP message blocks |
| 7 | Peer Test | 32B | NAT reachability testing |
| 9 | Retry | 32B | Token or rejection notice |
| 10 | Token Request | 32B | Request for validation token |
| 11 | Hole Punch | 32B | NAT traversal signaling |

---

## 4. Session Establishment

### 4.1 Standard Flow (Valid Token)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```

### 4.2 Token Acquisition

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```

### 4.3 Invalid Token

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```

---

## 5. Header Structures

### 5.1 Long Header (32 bytes)

Used before session establishment (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

| Field | Size | Description |
|--------|------|-------------|
| Destination Connection ID | 8 | Random unique ID |
| Packet Number | 4 | Random (ignored during handshake) |
| Type | 1 | Message type |
| Version | 1 | Always 2 |
| NetID | 1 | 2 = main I2P network |
| Flags | 1 | Reserved (0) |
| Source Connection ID | 8 | Random ID distinct from destination |
| Token | 8 | Token for address validation |

### 5.2 Short Header (16 bytes)

Used during established sessions (SessionConfirmed, Data).

| Field | Size | Description |
|--------|------|-------------|
| Destination Connection ID | 8 | Stable throughout session |
| Packet Number | 4 | Incrementing per message |
| Type | 1 | Message type (2 or 6) |
| Flags | 3 | ACK/fragment flags |

---

## 6. Encryption

### 6.1 AEAD

All payloads are encrypted with **ChaCha20/Poly1305 AEAD**:

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```

- Nonce: 12 bytes (4 zero + 8 counter)
- Tag: 16 bytes
- Associated Data: includes header for integrity binding

### 6.2 Header Protection

Headers are masked using ChaCha20 keystream derived from session header keys. This ensures all Connection IDs and packet fields appear random, providing DPI resistance.

### 6.3 Key Derivation

| Phase | Input | Output |
|--------|--------|---------|
| Initial | introKey + salt | handshake header key |
| Handshake | DH(X25519) | chainKey + AEAD key |
| Data phase | chainKey | TX/RX keys |
| Key rotation | oldKey | newKey |

---

## 7. Security and Replay Prevention

- Tokens are per-IP, expiring in ~60 seconds.  
- Replays are prevented via per-session Bloom filters.  
- Duplicate ephemeral keys are rejected.  
- Headers and payloads are cryptographically tied.  

Routers must discard any packet failing AEAD authentication or with an invalid version or NetID.

---

## 8. Packet Numbering and Session Lifetime

Each direction maintains its own 32-bit counter.  
- Starts at 0, increments per packet.  
- Must not wrap; session rekey or terminate before reaching 2³².  

Connection IDs remain static for the entire session, including during migration.  

---

## 9. Data Phase

- Type = 6 (Data)
- Short header (16 bytes)
- Payload contains one or more encrypted blocks:
  - ACK/NACK lists
  - I2NP message fragments
  - Padding (0–31 bytes random)
  - Termination blocks (optional)

Selective retransmission and out-of-order delivery are supported. Reliability remains “semi-reliable” — missing packets may be dropped silently after retry limits.

---

## 10. Relay and NAT Traversal

| Message | Type | Purpose |
|----------|------|----------|
| Peer Test | 7 | Determines inbound reachability |
| Retry | 9 | Issues new token or rejection |
| Token Request | 10 | Requests new address token |
| Hole Punch | 11 | Coordinates NAT hole punching |

Relay routers assist peers behind restrictive NATs using these control messages.

---

## 11. Session Termination

Either peer may close the session using a **Termination block** within a Data message.  
Resources must be released immediately after receipt.  
Repeat termination packets may be ignored after acknowledgment.

---

## 12. Implementation Guidelines

Routers **MUST**:
- Validate version = 2 and NetID = 2.  
- Drop packets <40 bytes or invalid AEAD.  
- Enforce 120s replay cache.  
- Reject reused tokens or ephemeral keys.  

Routers **SHOULD**:
- Randomize padding 0–31 bytes.  
- Use adaptive retransmission (RFC 6298).  
- Implement per-peer path validation before migration.  

---

## 13. Security Summary

| Property | Achieved By |
|-----------|-------------|
| Forward secrecy | X25519 ephemeral keys |
| Replay protection | Tokens + Bloom filter |
| Authenticated encryption | ChaCha20/Poly1305 |
| KCI resistance | Noise XK pattern |
| DPI resistance | Encrypted headers |
| NAT traversal | Relay + Hole Punch |
| Migration | Static connection IDs |

---

## 14. References

- [Proposal 159 – SSU2](/proposals/159-ssu2/)
- [Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [RFC 9000 – QUIC Transport]
- [RFC 9001 – QUIC TLS]
- [RFC 7539 – ChaCha20/Poly1305 AEAD]
- [RFC 7748 – X25519 ECDH]
- [RFC 5869 – HKDF-SHA256]
