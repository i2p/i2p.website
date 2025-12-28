---
title: "SAM v2"
description: "Legacy Simple Anonymous Messaging protocol"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Deprecated:** SAM v2 shipped with I2P 0.6.1.31 and is no longer maintained. Use [SAM v3](/docs/api/samv3/) for new development. v2’s only improvement over v1 was support for multiple sockets multiplexed over a single SAM connection.

## Version Notes

- Reported version string remains `"2.0"`.
- Since 0.9.14 the `HELLO VERSION` message accepts single-digit `MIN`/`MAX` values and the `MIN` parameter is optional.
- `DEST GENERATE` supports `SIGNATURE_TYPE` so Ed25519 destinations can be created.

## Session Basics

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```

- Each destination may have only one active SAM session (streams, datagrams, or raw).
- `STYLE` selects virtual streams, signed datagrams, or raw datagrams.
- Additional options are passed to I2CP (for example, `tunnels.quantityInbound=3`).
- Responses mirror v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Message Encoding

Line-oriented ASCII with `key=value` pairs separated by spaces (values may be quoted). Communication types are the same as v1:

- Streams via the I2P streaming library
- Repliable datagrams (`PROTO_DATAGRAM`)
- Raw datagrams (`PROTO_DATAGRAM_RAW`)

## When to Use

Only for legacy clients that cannot migrate. SAM v3 offers:

- Binary destination handoff (`DEST GENERATE BASE64`)
- Subsessions and DHT support (v3.3)
- Better error reporting and option negotiation

Refer to:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [Datagram API](/docs/api/datagrams/)
- [Streaming Protocol](/docs/specs/streaming/)
