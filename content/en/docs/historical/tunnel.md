---
title: "Tunnel Discussion"
description: "Historical exploration of tunnel padding, fragmentation, and build strategies"
slug: "tunnel"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Note: This document contains older information about alternatives to the
current tunnel implementation in I2P,
and speculation on future possibilities. For current information see
[the tunnel page](/docs/specs/tunnel-implementation).

That page documents the current tunnel build implementation as of release 0.6.1.10.
The older tunnel build method, used prior to release 0.6.1.10, is documented on
[the old tunnel page](/docs/historical/tunnel-alt).


### Configuration Alternatives {#config}

Beyond their length, there may be additional configurable parameters
for each tunnel that can be used, such as a throttle on the frequency of
messages delivered, how padding should be used, how long a tunnel should be
in operation, whether to inject chaff messages, and what, if any, batching
strategies should be employed.
None of these are currently implemented.


### Padding Alternatives {#tunnel.padding}

Several tunnel padding strategies are possible, each with their own merits:

- No padding
- Padding to a random size
- Padding to a fixed size
- Padding to the closest KB
- Padding to the closest exponential size (2^n bytes)

These padding strategies can be used on a variety of levels, addressing the
exposure of message size information to different adversaries. After gathering
and reviewing some statistics
from the 0.4 network, as well as exploring the anonymity tradeoffs, we're starting
with a fixed tunnel message size of 1024 bytes. Within this however, the fragmented
messages themselves are not padded by the tunnel at all (though for end to end
messages, they may be padded as part of the garlic wrapping).


### Fragmentation Alternatives {#tunnel.fragmentation}

To prevent adversaries from tagging the messages along the path by adjusting
the message size, all tunnel messages are a fixed 1024 bytes in size. To accommodate
larger I2NP messages as well as to support smaller ones more efficiently, the
gateway splits up the larger I2NP messages into fragments contained within each
tunnel message. The endpoint will attempt to rebuild the I2NP message from the
fragments for a short period of time, but will discard them as necessary.

Routers have a lot of leeway as to how the fragments are arranged, whether
they are stuffed inefficiently as discrete units, batched for a brief period to
fit more payload into the 1024 byte tunnel messages, or opportunistically padded
with other messages that the gateway wanted to send out.


### More Alternatives {#tunnel.alternatives}

#### Adjust Tunnel Processing Midstream {#tunnel.reroute}

While the simple tunnel routing algorithm should be sufficient for most cases,
there are three alternatives that can be explored:

- Have a peer other than the endpoint temporarily act as the termination
  point for a tunnel by adjusting the encryption used at the gateway to give them
  the plaintext of the preprocessed I2NP messages. Each peer could check to see
  whether they had the plaintext, processing the message when received as if they
  did.
- Allow routers participating in a tunnel to remix the message before
  forwarding it on - bouncing it through one of that peer's own outbound tunnels,
  bearing instructions for delivery to the next hop.
- Implement code for the tunnel creator to redefine a peer's "next hop" in
  the tunnel, allowing further dynamic redirection.


#### Use Bidirectional Tunnels {#tunnel.bidirectional}

The current strategy of using two separate tunnels for inbound and outbound
communication is not the only technique available, and it does have anonymity
implications. On the positive side, by using separate tunnels it lessens the
traffic data exposed for analysis to participants in a tunnel - for instance,
peers in an outbound tunnel from a web browser would only see the traffic of
an HTTP GET, while the peers in an inbound tunnel would see the payload
delivered along the tunnel. With bidirectional tunnels, all participants would
have access to the fact that e.g. 1KB was sent in one direction, then 100KB
in the other. On the negative side, using unidirectional tunnels means that
there are two sets of peers which need to be profiled and accounted for, and
additional care must be taken to address the increased speed of predecessor
attacks. The tunnel pooling and building process outlined below should
minimize the worries of the predecessor attack, though if it were desired,
it wouldn't be much trouble to build both the inbound and outbound tunnels
along the same peers.


#### Backchannel Communication {#tunnel.backchannel}

At the moment, the IV values used are random values. However, it is
possible for that 16 byte value to be used to send control messages from the
gateway to the endpoint, or on outbound tunnels, from the gateway to any of the
peers. The inbound gateway could encode certain values in the IV once, which
the endpoint would be able to recover (since it knows the endpoint is also the
creator). For outbound tunnels, the creator could deliver certain values to the
participants during the tunnel creation (e.g. "if you see 0x0 as the IV, that
means X", "0x1 means Y", etc). Since the gateway on the outbound tunnel is also
the creator, they can build a IV so that any of the peers will receive the
correct value. The tunnel creator could even give the inbound tunnel gateway
a series of IV values which that gateway could use to communicate with
individual participants exactly one time (though this would have issues regarding
collusion detection).

This technique could later be used deliver message mid stream, or to allow the
inbound gateway to tell the endpoint that it is being DoS'ed or otherwise soon
to fail. At the moment, there are no plans to exploit this backchannel.


#### Variable Size Tunnel Messages {#tunnel.variablesize}

While the transport layer may have its own fixed or variable message size,
using its own fragmentation, the tunnel layer may instead use variable size
tunnel messages. The difference is an issue of threat models - a fixed size
at the transport layer helps reduce the information exposed to external
adversaries (though overall flow analysis still works), but for internal
adversaries (aka tunnel participants) the message size is exposed. Fixed size
tunnel messages help reduce the information exposed to tunnel participants, but
does not hide the information exposed to tunnel endpoints and gateways. Fixed
size end to end messages hide the information exposed to all peers in the
network.

As always, its a question of who I2P is trying to protect against. Variable
sized tunnel messages are dangerous, as they allow participants to use the
message size itself as a backchannel to other participants - e.g. if you see a
1337 byte message, you're on the same tunnel as another colluding peer. Even
with a fixed set of allowable sizes (1024, 2048, 4096, etc), that backchannel
still exists as peers could use the frequency of each size as the carrier (e.g.
two 1024 byte messages followed by an 8192). Smaller messages do incur the
overhead of the headers (IV, tunnel ID, hash portion, etc), but larger fixed size
messages either increase latency (due to batching) or dramatically increase
overhead (due to padding). Fragmentation helps amortize the overhead, at the
cost of potential message loss due to lost fragments.

Timing attacks are also relevant when reviewing the effectiveness of fixed
size messages, though they require a substantial view of network activity
patterns to be effective. Excessive artificial delays in the tunnel will be
detected by the tunnel's creator, due to periodic testing, causing that entire
tunnel to be scrapped and the profiles for peers within it to be adjusted.


### Building Alternatives {#tunnel.building.alternatives}

Reference:
[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)


#### Old Tunnel Build Method {#tunnel.building.old}

The old tunnel build method, used prior to release 0.6.1.10, is documented on
[the old tunnel page](/docs/historical/tunnel-alt).
This was an "all at once" or "parallel" method,
where messages were sent in parallel to each of the participants.


#### One-Shot Telescopic Building {#tunnel.building.oneshot}

NOTE: This is the current method.

One question that arose regarding the use of the exploratory tunnels for
sending and receiving tunnel creation messages is how that impacts the tunnel's
vulnerability to predecessor attacks. While the endpoints and gateways of
those tunnels will be randomly distributed across the network (perhaps even
including the tunnel creator in that set), another alternative is to use the
tunnel pathways themselves to pass along the request and response, as is done
in [Tor](https://www.torproject.org/). This, however, may lead to leaks
during tunnel creation, allowing peers to discover how many hops there are later
on in the tunnel by monitoring the timing or packet count as
the tunnel is built.


#### "Interactive" Telescopic Building {#tunnel.building.telescoping}

Build the hops one at a time with a message through the existing part of the tunnel for each.
Has major issues as the peers can count the messages to determine their location in the tunnel.


#### Non-Exploratory Tunnels for Management {#tunnel.building.nonexploratory}

A second alternative to the tunnel building process is to give the router
an additional set of non-exploratory inbound and outbound pools, using those for
the tunnel request and response. Assuming the router has a well integrated view
of the network, this should not be necessary, but if the router was partitioned
in some way, using non-exploratory pools for tunnel management would reduce the
leakage of information about what peers are in the router's partition.


#### Exploratory Request Delivery {#tunnel.building.exploratory}

A third alternative, used until I2P 0.6.1.10, garlic encrypts individual tunnel
request messages and delivers them to the hops individually, transmitting them
through exploratory tunnels with their reply coming back in a separate
exploratory tunnel. This strategy has been dropped in favor of the one outlined
above.


#### More History and Discussion {#history}

Before the introduction of the Variable Tunnel Build Message,
there were at least two problems:

1. The size of the messages (caused by an 8-hop maximum, when the typical tunnel length is 2 or 3 hops...
   and current research indicates that more than 3 hops does not enhance anonymity);
2. The high build failure rate, especially for long (and exploratory) tunnels, since all hops must agree or the tunnel is discarded.

The VTBM has fixed #1 and improved #2.

Welterde has proposed modifications to the parallel method to allow for reconfiguration.
Sponge has proposed using 'tokens' of some sort.

Any students of tunnel building must study the historical record leading up to the current method,
especially the various anonymity vulnerabilities that may exist in various methods.
The mail archives from October 2005 are particularly helpful.
As stated on [the tunnel creation specification](/docs/specs/tunnel-creation),
the current strategy came about during a discussion on the I2P mailing list between
Michael Rogers, Matthew Toseland (toad), and jrandom regarding the predecessor attack.


#### Peer Ordering Alternatives {#ordering}

A less strict ordering is also possible, assuring that while
the hop after A may be B, B may never be before A. Other configuration options
include the ability for just the inbound tunnel gateways and outbound tunnel
endpoints to be fixed, or rotated on an MTBF rate.


## Mixing/Batching {#tunnel.mixing}

What strategies should be used at the gateway and at each hop for delaying,
reordering, rerouting, or padding messages? To what extent should this be done
automatically, how much should be configured as a per tunnel or per hop setting,
and how should the tunnel's creator (and in turn, user) control this operation?
All of this is left as unknown, to be worked out for a future release.
