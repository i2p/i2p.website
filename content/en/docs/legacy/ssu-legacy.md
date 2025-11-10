---
title: "SSU Transport (Deprecated)"
description: "Original UDP transport used prior to SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
aliases:
  - /spec/ssu/
reviewStatus: "needs-review"
---

> **Deprecated:** SSU (Secure Semi-Reliable UDP) has been replaced by [SSU2](/docs/specs/ssu2/). Java I2P removed SSU in release 2.4.0 (API 0.9.61) and i2pd removed it in 2.44.0 (API 0.9.56). This document is retained for historical reference only.

## Highlights

- UDP transport providing encrypted, authenticated point-to-point delivery of I2NP messages.
- Relied on a 2048-bit Diffie–Hellman handshake (same prime as ElGamal).
- Each datagram carried a 16-byte HMAC-MD5 (non-standard truncated variant) + 16-byte IV followed by AES-256-CBC encrypted payload.
- Replay prevention and session state tracked within the encrypted payload.

## Message Header

```
[16-byte MAC][16-byte IV][encrypted payload]
```

MAC calculation used: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` with a 32-byte MAC key. Payload length was big-endian 16-bit appended inside the MAC calculation. Protocol version defaulted to `0`; netId defaulted to `2` (main network).

## Session & MAC Keys

Derived from the DH shared secret:

1. Convert the shared value to a big-endian byte array (prepend `0x00` if high bit set).
2. Session key: first 32 bytes (pad with zeros if shorter).
3. MAC key: bytes 33–64; if insufficient, fall back to SHA-256 hash of the shared value.

## Status

Routers no longer advertise SSU addresses. Clients should migrate to SSU2 or NTCP2 transports. Historical implementations can be found in older releases:

- Java sources prior to 2.4.0 under `router/transport/udp`
- i2pd sources prior to 2.44.0

For current UDP transport behaviour, refer to [SSU2 specification](/docs/specs/ssu2/).
