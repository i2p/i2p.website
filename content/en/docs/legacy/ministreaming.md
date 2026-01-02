---
title: "Ministreaming Library"
description: "Historical notes on I2P's first TCP-like transport layer"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Deprecated:** The ministreaming library predates today’s [streaming library](/docs/specs/streaming/). Modern applications must use the full streaming API or SAM v3. The information below is retained for developers reviewing legacy source code shipped in `ministreaming.jar`.

## Overview

Ministreaming sits on top of [I2CP](/docs/specs/i2cp/) to provide reliable, in-order delivery across I2P’s message layer—much like TCP over IP. It was originally factored out of the early **I2PTunnel** application (BSD licensed) so alternative transports could evolve independently.

Key design constraints:

- Classic two-phase (SYN/ACK/FIN) connection setup borrowed from TCP
- Fixed window size of **1** packet
- No per-packet IDs or selective acknowledgements

These choices kept the implementation small but limit throughput—each packet usually waits almost two RTTs before the next is sent. For long-lived streams the penalty is acceptable, but short HTTP-style exchanges suffer noticeably.

## Relationship to the Streaming Library

The current streaming library extends the same Java package (`net.i2p.client.streaming`). Deprecated classes and methods remain in the Javadocs, clearly annotated so developers can identify ministreaming-era APIs. When the streaming library superseded ministreaming it added:

- Smarter connection setup with fewer round trips
- Adaptive congestion windows and retransmission logic
- Better performance over lossy tunnels

## When Was Ministreaming Useful?

Despite its limits, ministreaming delivered reliable transport in the earliest deployments. The API was intentionally small and future-proof so that alternate streaming engines could be swapped in without breaking callers. Java applications linked it directly; non-Java clients accessed the same functionality through [SAM](/docs/legacy/sam/) support for streaming sessions.

Today, treat `ministreaming.jar` as a compatibility layer only. New development should:

1. Target the full streaming library (Java) or SAM v3 (`STREAM` style)  
2. Remove any lingering fixed-window assumptions when modernising code  
3. Prefer higher window sizes and optimised connect handshakes to improve latency-sensitive workloads

## Reference

- [Streaming Library documentation](/docs/specs/streaming/)
- [Streaming Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – includes deprecated ministreaming classes
- [SAM v3 specification](/docs/api/samv3/) – streaming support for non-Java applications

If you encounter code that still depends on ministreaming, plan to port it to the modern streaming API—the network and its tooling expect the newer behaviour.
