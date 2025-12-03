---
title: "Performance"
description: "I2P network performance: how it behaves today, historical improvements, and ideas for future tuning"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - "/en/about/performance"
  - "/about/performance"
  - "/en/about/performance/"
  - "/about/performance/"
  - "/en/about/performance/future"
  - "/about/performance/future"
  - "/en/about/performance/future/"
  - "/about/performance/future/"
  - "/en/about/performance/history"
  - "/about/performance/history"
  - "/en/about/performance/history/"
  - "/about/performance/history/"
reviewStatus: "needs-review"
---

## I2P Network Performance: Speed, Connections and Resource Management

The I2P network is fully dynamic. Each client is known to other nodes and tests locally known nodes for reachability and capacity. Only reachable and capable nodes are saved to a local NetDB. During the tunnel building process, the best resources are selected from this pool to build tunnels with. Because testing happens continuously, the pool of nodes changes. Each I2P node knows a different part of the NetDB, meaning that each router has a different set of I2P nodes to be used for tunnels. Even if two routers have the same subset of known nodes, the tests for reachability and capacity will likely show different results, as the other routers could be under load just as one router tests, but be free when the second router tests.

This describes why each I2P node has different nodes to build tunnels. Because every I2P node has a different latency and bandwidth, tunnels (which are built via those nodes) have different latency and bandwidth values. And because every I2P node has different tunnels built, no two I2P nodes have the same tunnel sets.

A server/client is known as a "destination" and each destination has at least one inbound and one outbound tunnel. The default is 3 hops per tunnel. This adds up to 12 hops (12 different I2P nodes) for a full round trip client → server → client.

Each data package is sent through 6 other I2P nodes until it reaches the server:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

and on the way back 6 different I2P nodes:

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Traffic on the network needs an ACK before new data is sent; it needs to wait until an ACK returns from a server: send data, wait for ACK, send more data, wait for ACK. As the RTT (Round Trip Time) adds up from the latency of each individual I2P node and each connection on this round trip, it takes usually 1–3 seconds until an ACK comes back to the client. Because of TCP and I2P transport design, a data package has a limited size. Together these conditions set a limit max bandwidth per tunnel of roughly 20–50 kB/s. However, if only one hop in the tunnel has only 5 kB/s bandwidth to spend, the whole tunnel is limited to 5 kB/s, independent of the latency and other limitations.

Encryption, latency, and how a tunnel is built makes it quite expensive in CPU time to build a tunnel. This is why a destination is only allowed to have a maximum of 6 inbound and 6 outbound tunnels to transport data. With a max of 50 kB/s per tunnel, a destination could use roughly 300 kB/s traffic combined (in reality it could be more if shorter tunnels are used with low or no anonymity available). Used tunnels are discarded every 10 minutes and new ones are built. This change of tunnels, and sometimes clients that shut down or lose their connection to the network, will sometimes break tunnels and connections. An example of this can be seen on the IRC2P Network in loss of connection (ping timeout) or when using eepget.

With a limited set of destinations and a limited set of tunnels per destination, one I2P node only uses a limited set of tunnels across other I2P nodes. For example, if an I2P node is "hop1" in the small example above, it only sees one participating tunnel originating from the client. If we sum up the whole I2P network, only a rather limited number of participating tunnels could be built with a limited amount of bandwidth all together. If one distributes these limited numbers across the number of I2P nodes, there is only a fraction of available bandwidth/capacity available for use.

To remain anonymous, one router should not be used by the whole network for building tunnels. If one router does act as a tunnel router for all I2P nodes, it becomes a very real central point of failure as well as a central point to gather IPs and data from clients. This is why the network distributes traffic across nodes in the tunnel building process.

Another consideration for performance is the way I2P handles mesh networking. Each connection hop‑to‑hop utilizes one TCP or UDP connection on I2P nodes. With 1000 connections, one sees 1000 TCP connections. That is quite a lot, and some home and small office routers only allow a small number of connections. I2P tries to limit these connections to under 1500 per UDP and per TCP type. This limits the amount of traffic routed across an I2P node as well.

If a node is reachable, and has a bandwidth setting of >128 kB/s shared and is reachable 24/7, it should be used after some time for participating traffic. If it is down in between, the testing of an I2P node done by other nodes will tell them it is not reachable. This blocks a node for at least 24 hours on other nodes. So, the other nodes which tested that node as down will not use that node for 24 hours for building tunnels. This is why your traffic is lower after a restart/shutdown of your I2P router for a minimum of 24 hours.

Additionally, other I2P nodes need to know an I2P router to test it for reachability and capacity. This process can be made faster when you interact with the network, for instance by using applications or visiting I2P sites, which will result in more tunnel building and therefore more activity and reachability for testing by nodes on the network.

## Performance History (selected)

Over the years, I2P has seen a number of notable performance improvements:

### Native math

Implemented via JNI bindings to the GNU MP library (GMP) to accelerate BigInteger `modPow`, which previously dominated CPU time. Early results showed dramatic speedups in public‑key cryptography. See: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Previously, replies often required a network database lookup for the sender’s LeaseSet. Bundling the sender’s LeaseSet in the initial garlic improves reply latency. This is now done selectively (start of a connection or when the LeaseSet changes) to reduce overhead.

### More efficient TCP rejection

Moved some validation steps earlier in the transport handshake to reject bad peers sooner (wrong clocks, bad NAT/firewall, incompatible versions), saving CPU and bandwidth.

### Tunnel testing adjustments

Use context‑aware tunnel testing: avoid testing tunnels already known to be passing data; favor testing when idle. This reduces overhead and speeds detection of failing tunnels.

### Persistent tunnel/lease selection

Persisting selections for a given connection reduces out‑of‑order delivery and allows the streaming library to increase window sizes, improving throughput.

### Compress selected data structures

GZip or similar for verbose structures (e.g., RouterInfo options) reduces bandwidth where appropriate.

### Full streaming protocol

Replacement for the simplistic “ministreaming” protocol. Modern streaming includes selective ACKs and congestion control tailored to I2P’s anonymous, message‑oriented substrate. See: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Below are ideas documented historically as potential improvements. Many are obsolete, implemented, or superseded by architectural changes.

### Better peer profiling and selection

Improve how routers choose peers for tunnel building to avoid slow or overloaded ones, while remaining resistant to Sybil attacks by powerful adversaries.

### Network database tuning

Reduce unnecessary exploration when the keyspace is stable; tune how many peers are returned in lookups and how many concurrent searches are performed.

### Session Tag tuning and improvements (legacy)

For the legacy ElGamal/AES+SessionTag scheme, smarter expiration and replenishment strategies reduce ElGamal fallbacks and wasted tags.

### Migrate SessionTag to synchronized PRNG (legacy)

Generate tags from a synchronized PRNG seeded during a new session establishment, reducing per‑message overhead from pre‑delivered tags.

### Longer‑lasting tunnels

Longer tunnel lifetimes coupled with healing can reduce rebuild overheads; balance with anonymity and reliability.

### Efficient transport rejection and testing

Reject invalid peers earlier and make tunnel tests more context‑aware to reduce contention and latency.

### Miscellaneous protocol and implementation tuning

Selective LeaseSet bundling, compressed RouterInfo options, and adoption of the full streaming protocol all contribute to better perceived performance.

---

See also:

- [Tunnel Routing](/docs/overview/tunnel-routing/)
- [Peer Selection](/docs/how/peer-selection/)
- [Transports](/docs/transport/)
- [SSU2 Specification](/docs/specs/ssu2/) and [NTCP2 Specification](/docs/specs/ntcp2/)

