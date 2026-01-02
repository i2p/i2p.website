---
title: "SAM v1"
description: "Legacy Simple Anonymous Messaging protocol (deprecated)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Deprecated:** SAM v1 is retained for historical reference only. New applications should use [SAM v3](/docs/api/samv3/) or [BOB](/docs/legacy/bob/). The original bridge only supports DSA-SHA1 destinations and a limited option set.

## Libraries

The Java I2P source tree still includes legacy bindings for C, C#, Perl, and Python. They are no longer maintained and shipped mainly for archival compatibility.

## Version Negotiation

Clients connect via TCP (default `127.0.0.1:7656`) and exchange:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```

As of Java I2P 0.9.14 the `MIN` parameter is optional and both `MIN`/`MAX` accept single-digit forms (`"3"` etc.) for upgraded bridges.

## Session Creation

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```

- `DESTINATION=name` loads or creates an entry in `sam.keys`; `TRANSIENT` always creates a temporary destination.
- `STYLE` selects virtual streams (TCP-like), signed datagrams, or raw datagrams.
- `DIRECTION` applies to stream sessions only; defaults to `BOTH`.
- Additional key/value pairs are passed through as I2CP options (for example, `tunnels.quantityInbound=3`).

The bridge replies with:

```
SESSION STATUS RESULT=OK DESTINATION=name
```

Failures return `DUPLICATED_DEST`, `I2P_ERROR`, or `INVALID_KEY` plus an optional message.

## Message Formats

SAM messages are single-line ASCII with space-delimited key/value pairs. Keys are UTF‑8; values may be quoted if they contain spaces. No escaping is defined.

Communication types:

- **Streams** – proxied through the I2P streaming library
- **Repliable datagrams** – signed payloads (Datagram1)
- **Raw datagrams** – unsigned payloads (Datagram RAW)

## Options Added in 0.9.14

- `DEST GENERATE` accepts `SIGNATURE_TYPE=...` (allowing Ed25519, etc.)
- `HELLO VERSION` treats `MIN` as optional and accepts single-digit version strings

## When to Use SAM v1

Only for interoperability with legacy software that cannot be updated. For all new development use:

- [SAM v3](/docs/api/samv3/) for feature-complete stream/datagram access
- [BOB](/docs/legacy/bob/) for destination management (still limited, but supports more modern features)

## References

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Datagram Specification](/docs/api/datagrams/)
- [Streaming Protocol](/docs/specs/streaming/)

SAM v1 laid the foundation for router-agnostic application development, but the ecosystem has moved on. Treat this document as a compatibility aid rather than a starting point.
