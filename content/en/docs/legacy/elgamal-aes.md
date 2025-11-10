---
title: "ElGamal/AES + SessionTag Encryption"
description: "Legacy end-to-end encryption combining ElGamal, AES, SHA-256, and one-time session tags"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /docs/how/elgamal-aes/
  - /en/docs/specs/elgamal-aes/
reviewStatus: "needs-review"
---

> **Status:** This document describes the legacy ElGamal/AES+SessionTag encryption protocol. It remains supported only for backward compatibility, as modern I2P versions (2.10.0+) use [ECIES‑X25519‑AEAD‑Ratchet](/docs/specs/ecies/). The ElGamal protocol is deprecated and retained solely for historical and interoperability purposes.

## Overview

ElGamal/AES+SessionTag provided I2P’s original end‑to‑end encryption mechanism for garlic messages. It combined:

- **ElGamal (2048‑bit)** — for key exchange  
- **AES‑256/CBC** — for payload encryption  
- **SHA‑256** — for hashing and IV derivation  
- **Session Tags (32 bytes)** — for single‑use message identifiers  

The protocol allowed routers and destinations to communicate securely without maintaining persistent connections. Each session used an asymmetric ElGamal exchange to establish a symmetric AES key, followed by lightweight “tagged” messages referencing that session.

## Protocol Operation

### Session Establishment (New Session)

A new session began with a message containing two sections:

| Section | Size | Contents | Purpose |
|----------|------|-----------|----------|
| **ElGamal‑encrypted block** | 514 bytes | 222 bytes of plaintext encrypted using the recipient’s ElGamal public key | Establishes the AES session key and IV seed |
| **AES‑encrypted block** | Variable (≥ 128 bytes typical) | Payload data, integrity hash, and session tags | Carries the actual message and new tags |

The plaintext inside the ElGamal block consisted of:

| Field | Size | Description |
|--------|------|-------------|
| Session Key | 32 bytes | AES‑256 key for the session |
| Pre‑IV | 32 bytes | Material for deriving the AES initialization vector (`IV = first 16 bytes of SHA‑256(Pre‑IV)`) |
| Random Padding | 158 bytes | Filler to reach required ElGamal plaintext length |

### Existing Session Messages

Once a session was established, the sender could send **existing‑session** messages using cached session tags:

| Field | Size | Description |
|--------|------|-------------|
| Session Tag | 32 bytes | Single‑use identifier tied to the existing session key |
| AES‑Encrypted Block | Variable | Encrypted payload and metadata using the established AES key |

Routers cached delivered tags for about **15 minutes**, after which unused tags expired. Each tag was valid for exactly **one message** to prevent correlation attacks.

### AES‑Encrypted Block Format

| Field | Size | Description |
|--------|------|-------------|
| Tag Count | 2 bytes | Number (0–200) of new session tags included |
| Session Tags | 32 × N bytes | Newly generated single‑use tags |
| Payload Size | 4 bytes | Length of the payload in bytes |
| Payload Hash | 32 bytes | SHA‑256 digest of the payload |
| Flag | 1 byte | `0x00` normal, `0x01` = new session key follows (unused) |
| New Session Key | 32 bytes (optional) | Replacement AES key (rarely used) |
| Payload | Variable | Encrypted message data |
| Padding | Variable (16‑byte aligned) | Random padding to block boundary |

Routers decrypt using the session key and IV derived from either the Pre‑IV (for new sessions) or the session tag (for existing sessions). After decryption, they verify integrity by recomputing the SHA‑256 hash of the plaintext payload.

## Session Tag Management

- Tags are **unidirectional**: Alice → Bob tags cannot be reused by Bob → Alice.  
- Tags expire after approximately **15 minutes**.  
- Routers maintain per‑destination **session key managers** to track tags, keys, and expiration times.  
- Applications can control tag behavior through [I2CP options](/spec/i2cp/#options):  
  - **`i2cp.tagThreshold`** — minimum cached tags before replenishment  
  - **`i2cp.tagCount`** — number of new tags per message  

This mechanism minimized expensive ElGamal handshakes while maintaining unlinkability between messages.

## Configuration and Efficiency

Session tags were introduced to improve efficiency across I2P’s high‑latency, unordered transport. A typical configuration delivered **40 tags per message**, adding about 1.2 KB of overhead. Applications could adjust delivery behavior based on expected traffic:

| Use Case | Recommended Tags | Notes |
|-----------|------------------|-------|
| Short‑lived requests (HTTP, datagrams) | 0 – 5 | Low overhead, may trigger ElGamal fallback |
| Persistent streams or bulk transfer | 20 – 50 | Higher bandwidth use, avoids session re‑establishment |
| Long‑term services | 50 + | Ensures steady tag supply despite loss or delay |

Routers periodically purge expired tags and prune unused session state to reduce memory usage and mitigate tag‑flooding attacks.

## Limitations

| Category | Limitation |
|-----------|-------------|
| **Performance** | 514‑byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each. |
| **Security** | No forward secrecy – compromise of ElGamal private key exposes past sessions. |
| **Integrity** | AES‑CBC requires manual hash verification; no AEAD. |
| **Quantum Resistance** | Vulnerable to Shor’s algorithm – will not survive quantum attacks. |
| **Complexity** | Requires stateful tag management and careful timeout tuning. |

These shortcomings directly motivated the design of the [ECIES‑X25519‑AEAD‑Ratchet](/docs/specs/ecies/) protocol, which provides perfect forward secrecy, authenticated encryption, and efficient key exchange.

## Deprecation and Migration Status

- **Introduced:** Early I2P releases (pre‑0.6)  
- **Deprecated:** With introduction of ECIES‑X25519 (0.9.46 → 0.9.48)  
- **Removed:** No longer default as of 2.4.0 (December 2023)  
- **Supported:** Legacy compatibility only  

Modern routers and destinations now advertise **crypto type 4 (ECIES‑X25519)** instead of **type 0 (ElGamal/AES)**. The legacy protocol remains recognized for interoperability with outdated peers but should not be used for new deployments.

## Historical Context

ElGamal/AES+SessionTag was foundational to I2P’s early cryptographic architecture. Its hybrid design introduced innovations such as one‑time session tags and unidirectional sessions that informed subsequent protocols. Many of these ideas evolved into modern constructions like deterministic ratchets and hybrid post‑quantum key exchanges.

