---
title: "Old Tunnel Implementation (Legacy)"
description: "Archived description of the tunnel design used prior to I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
aliases:
  - /docs/tunnels/old-implementation/
  - /en/docs/tunnels/implementation/
  - /en/docs/tunnels/old-implementation/
reviewStatus: "needs-review"
---

> **Legacy status:** This content is retained for historical reference only. It documents the tunnel system that shipped before I2P&nbsp;0.6.1.10 and should not be used for modern development. Refer to the [current implementation](/docs/specs/implementation/) for production guidance.

The original tunnel subsystem also used unidirectional tunnels but differed in message layout, duplicate detection, and build strategy. Many sections below mirror the structure of the deprecated document to aid comparison.

## 1. Tunnel Overview

- Tunnels were built as ordered sequences of peers selected by the creator.
- Tunnel lengths ranged from 0–7 hops, with several knobs for padding, throttling, and chaff generation.
- Inbound tunnels delivered messages from an untrusted gateway to the creator (endpoint); outbound tunnels pushed data away from the creator.
- Tunnel lifetimes were 10 minutes, after which new tunnels were constructed (often using the same peers but different tunnel IDs).

## 2. Operation in the Legacy Design

### 2.1 Message Preprocessing

Gateways accumulated ≤32&nbsp;KB of I2NP payload, selected padding, and produced a payload containing:

- A two-byte padding-length field and that many random bytes
- A sequence of `{instructions, I2NP message}` pairs describing delivery targets, fragmentation, and optional delays
- Full I2NP messages padded out to a 16-byte boundary

Delivery instructions packed routing information into bit fields (delivery type, delay flags, fragmentation flags, and optional extensions). Fragmented messages carried a 4-byte message ID plus an index/last-fragment flag.

### 2.2 Gateway Encryption

The legacy design fixed tunnel length at eight hops for the encryption phase. Gateways layered AES-256/CBC plus checksum blocks so that each hop could verify integrity without shrinking the payload. The checksum itself was a SHA-256 derived block embedded within the message.

### 2.3 Participant Behaviour

Participants tracked inbound tunnel IDs, verified integrity early, and dropped duplicates before forwarding. Because padding and verification blocks were embedded, the message size remained constant regardless of hop count.

### 2.4 Endpoint Processing

Endpoints decrypted the layered blocks sequentially, validated checksums, and split the payload back into the encoded instructions plus I2NP messages for further delivery.

## 3. Tunnel Building (Deprecated Process)

1. **Peer selection:** Peers were chosen from locally maintained profiles (exploratory vs. client). The original document already emphasised mitigation of the [predecessor attack](https://en.wikipedia.org/wiki/Predecessor_attack) by reusing ordered peer lists per tunnel pool.
2. **Request delivery:** Build messages were forwarded hop-by-hop with encrypted sections for each peer. Alternative ideas such as telescopic extension, midstream rerouting, or removing checksum blocks were discussed as experiments but never adopted.
3. **Pooling:** Each local destination held separate inbound and outbound pools. Settings included desired quantity, backup tunnels, length variance, throttling, and padding policies.

## 4. Throttling and Mixing Concepts

The legacy write-up proposed several strategies that informed later releases:

- Weighted Random Early Discard (WRED) for congestion control
- Per-tunnel throttles based on moving averages of recent usage
- Optional chaff and batching controls (not fully implemented)

## 5. Archived Alternatives

Sections of the original document explored ideas that were never deployed:

- Removing checksum blocks to shrink per-hop processing
- Telescoping tunnels midstream to change peer composition
- Switching to bidirectional tunnels (ultimately rejected)
- Using shorter hashes or different padding regimens

These ideas remain valuable historical context but do not reflect the modern codebase.

## References

- Original legacy document archive (pre-0.6.1.10)
- [Tunnel Overview](/docs/overview/tunnel-routing/) for current terminology
- [Peer Profiling and Selection](/docs/overview/tunnel-routing#peer-selection/) for modern heuristics

