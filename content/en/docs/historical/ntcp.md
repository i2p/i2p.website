---
title: "NTCP Discussion"
description: "Historical notes comparing NTCP and SSU transports and proposed tuning ideas"
slug: "ntcp"
layout: "single"
aliases:
  - /docs/discussions/ntcp/
  - /docs/legacy/ntcp/
  - /en/docs/ntcp/
reviewStatus: "needs-review"
---



## NTCP vs. SSU Discussion (March 2007)

### NTCP Questions

_Adapted from an IRC conversation between zzz and cervantes._

- **Why does NTCP have priority over SSU when NTCP appears to add overhead and latency?**  
  NTCP generally provides better reliability than the original SSU implementation.
- **Does streaming over NTCP run into classic TCP-over-TCP collapse?**  
  Possibly, but SSU was intended to be the lightweight UDP option and proved too unreliable in practice.

### “NTCP Considered Harmful” (zzz, March 25, 2007)

Summary: NTCP’s higher latency and overhead may cause congestion, yet routing prefers NTCP because its bid scores are hard-coded lower than SSU. The analysis raised several points:

- NTCP currently bids lower than SSU, so routers prefer NTCP unless an SSU session is already established.
- SSU implements acknowledgements with tightly bounded timeouts and statistics; NTCP relies on Java NIO TCP with RFC-style timeouts that may be much longer.
- Most traffic (HTTP, IRC, BitTorrent) uses I2P’s streaming library, effectively layering TCP over NTCP. When both layers retransmit, collapse is possible. Classic references include [TCP over TCP is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Streaming-library timeouts increased from 10 s to 45 s in release 0.8; SSU’s max timeout is 3 s, while NTCP timeouts are presumed to approach 60 s (RFC recommendation). NTCP parameters are hard to inspect externally.
- Field observations in 2007 showed i2psnark upload throughput oscillating, suggesting periodic congestion collapse.
- Efficiency tests (forcing SSU preference) reduced tunnel overhead ratios from roughly 3.5:1 to 3:1 and improved streaming metrics (window size, RTT, send/ack ratio).

#### Proposals from the 2007 thread

1. **Flip transport priorities** so routers prefer SSU (restoring `i2np.udp.alwaysPreferred`).
2. **Tag streaming traffic** so SSU bids lower only for tagged messages, without compromising anonymity.
3. **Tighten SSU retransmission bounds** to reduce collapse risk.
4. **Study semi-reliable underlays** to determine whether retransmissions below the streaming library are a net benefit.
5. **Review priority queues and timeouts**—for example, increasing streaming timeouts beyond 45 s to align with NTCP.

### Response by jrandom (March 27, 2007)

Key counterpoints:

- NTCP exists because early SSU deployments suffered congestion collapse. Even modest per-hop retransmission rates can explode across multi-hop tunnels.
- Without tunnel-level acknowledgements, only a fraction of messages receive end-to-end delivery status; failures may be silent.
- TCP congestion control has decades of optimizations; NTCP leverages those via mature TCP stacks.
- Observed efficiency gains when preferring SSU might reflect router queuing behavior rather than intrinsic protocol advantages.
- Larger streaming timeouts were already improving stability; more observation and data were encouraged before major changes.

The debate helped refine subsequent transport tuning but does not reflect the modern NTCP2/SSU2 architecture.
