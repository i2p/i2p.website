---
title: "Tunnel Discussion"
description: "Historical exploration of tunnel padding, fragmentation, and build strategies"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
aliases:
  - /docs/discussions/tunnel/
reviewStatus: "needs-review"
---

> **Note:** This archive captures speculative design work predating I2P 0.9.41. For the production implementation, consult the [tunnel documentation](/docs/specs/implementation/).

## Configuration Alternatives

Ideas considered for future tunnel knobs included:

- Frequency throttles for message delivery
- Padding policies (including chaff injection)
- Tunnel lifetime controls
- Batch and queue strategies for payload dispatch

None of these options shipped with the legacy implementation.

## Padding Strategies

Potential padding approaches discussed:

- No padding at all
- Random-length padding
- Fixed-length padding
- Padding to the nearest kilobyte
- Padding to powers of two (`2^n` bytes)

Early measurements (release 0.4) led to the current fixed 1024-byte tunnel message size. Higher-level garlic messages may add their own padding.

## Fragmentation

To prevent tagging attacks via message length, tunnel messages are fixed at 1024 bytes. Larger I2NP payloads are fragmented by the gateway; the endpoint reassembles fragments within a short timeout. Routers may rearrange fragments to maximize packing efficiency before sending.

## Additional Alternatives

### Adjust Tunnel Processing Midstream

Three possibilities were examined:

1. Allow an intermediate hop to terminate a tunnel temporarily by granting access to decrypted payloads.
2. Permit participating routers to “remix” messages by sending them through one of their own outbound tunnels before continuing to the next hop.
3. Enable the tunnel creator to redefine a peer’s next hop dynamically.

### Bidirectional Tunnels

Using separate inbound and outbound tunnels limits the information any single set of peers can observe (e.g., a GET request vs. a large response). Bidirectional tunnels simplify peer management but expose full traffic patterns to both directions simultaneously. Unidirectional tunnels therefore remained the preferred design.

### Backchannels and Variable Sizes

Allowing variable tunnel message sizes would enable covert channels between colluding peers (e.g., encoding data via selected sizes or frequencies). Fixed-size messages mitigate this risk at the cost of additional padding overhead.

## Tunnel Building Alternatives

Reference: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Legacy “Parallel” Build Method

Prior to release 0.6.1.10, tunnel build requests were sent in parallel to each participant. This method is documented on the [old tunnel page](/docs/legacy/old-implementation/).

### One-Shot Telescopic Building (Current Method)

The modern approach sends build messages hop-by-hop through the partially constructed tunnel. Although similar to Tor’s telescoping, routing build messages through exploratory tunnels reduces information leakage.

### “Interactive” Telescoping

Building one hop at a time with explicit round-trips allows peers to count messages and infer their position in the tunnel, so this approach was rejected.

### Non-Exploratory Management Tunnels

One proposal was to maintain a separate pool of management tunnels for build traffic. While it could help partitioned routers, it was deemed unnecessary with adequate network integration.

### Exploratory Delivery (Legacy)

Before 0.6.1.10, individual tunnel requests were garlic-encrypted and delivered via exploratory tunnels, with replies returning separately. This strategy was replaced by the current one-shot telescoping method.

## Takeaways

- Fixed-size tunnel messages guard against size-based tagging and covert channels, despite added padding cost.
- Alternative padding, fragmentation, and build strategies were explored but not adopted when weighed against anonymity trade-offs.
- Tunnel design continues to balance efficiency, observability, and resistance to predecessor and congestion attacks.
