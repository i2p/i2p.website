---
title: "Tunnel Implementation"
description: "Specification of I2P tunnel operation, building, and message processing"
slug: "tunnel-implementation"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

This page documents the current tunnel implementation.

## Tunnel Overview {#tunnel.overview}

Within I2P, messages are passed in one direction through a virtual
tunnel of peers, using whatever means are available to pass the
message on to the next hop. Messages arrive at the tunnel's
*gateway*, get bundled up and/or fragmented into fixed-size tunnel messages,
and are forwarded on to the next hop in the tunnel, which processes and verifies
the validity of the message and sends it on to the next hop, and so on, until
it reaches the tunnel endpoint. That *endpoint* takes the messages
bundled up by the gateway and forwards them as instructed - either
to another router, to another tunnel on another router, or locally.

Tunnels all work the same, but can be segmented into two different
groups - inbound tunnels and outbound tunnels. The inbound tunnels
have an untrusted gateway which passes messages down towards the
tunnel creator, which serves as the tunnel endpoint. For outbound
tunnels, the tunnel creator serves as the gateway, passing messages
out to the remote endpoint.

The tunnel's creator selects exactly which peers will participate
in the tunnel, and provides each with the necessary configuration
data. They may have any number of hops.
It is the intent to make
it hard for either participants or third parties to determine the length of
a tunnel, or even for colluding participants to determine whether they are a
part of the same tunnel at all (barring the situation where colluding peers are
next to each other in the tunnel).

In practice, a series of tunnel pools are used for different
purposes - each local client destination has its own set of inbound
tunnels and outbound tunnels, configured to meet its anonymity and
performance needs. In addition, the router itself maintains a series
of pools for participating in the network database and for managing
the tunnels themselves.

I2P is an inherently packet switched network, even with these
tunnels, allowing it to take advantage of multiple tunnels running
in parallel, increasing resilience and balancing load. Outside of
the core I2P layer, there is an optional end to end streaming library
available for client applications, exposing TCP-esque operation,
including message reordering, retransmission, congestion control, etc.

An overview of I2P tunnel terminology is
[on the tunnel overview page](/docs/overview/tunnel-routing).


## Tunnel Operation (Message Processing) {#tunnel.operation}

### Overview

After a tunnel is built, [I2NP messages](/docs/specs/i2np) are processed and passed through it.
Tunnel operation has four distinct processes, taken on by various
peers in the tunnel.

1. First, the tunnel gateway accumulates a number
   of I2NP messages and preprocesses them into tunnel messages for
   delivery.
2. Next, that gateway encrypts that preprocessed data, then
   forwards it to the first hop.
3. That peer, and subsequent tunnel
   participants, unwrap a layer of the encryption, verifying that it isn't
   a duplicate, then forward it on to the next peer.
4. Eventually, the tunnel messages arrive at the endpoint where the I2NP messages
   originally bundled by the gateway are reassembled and forwarded on as
   requested.

Intermediate tunnel participants do not know whether they are in an
inbound or an outbound tunnel; they always "encrypt" for the next hop.
Therefore, we take advantage of symmetric AES encryption
to "decrypt" at the outbound tunnel gateway,
so that the plaintext is revealed at the outbound endpoint.

| Role | Preprocessing | Encryption Operation | Postprocessing |
|------|---------------|---------------------|----------------|
| Outbound Gateway (Creator) | Fragment, Batch, and Pad | Iteratively encrypt (using decryption operations) | Forward to next hop |
| Participant | | Decrypt (using an encryption operation) | Forward to next hop |
| Outbound Endpoint | | Decrypt (using an encryption operation) to reveal plaintext tunnel message | Reassemble Fragments, Forward as instructed to Inbound Gateway or Router |
| | | | |
| Inbound Gateway | Fragment, Batch, and Pad | Encrypt | Forward to next hop |
| Participant | | Encrypt | Forward to next hop |
| Inbound Endpoint (Creator) | | Iteratively decrypt to reveal plaintext tunnel message | Reassemble Fragments, Receive data |


### Gateway Processing {#tunnel.gateway}

#### Message Preprocessing {#tunnel.preprocessing}

A tunnel gateway's function is to fragment and pack
[I2NP messages](/docs/specs/i2np) into fixed-size
[tunnel messages](/docs/specs/tunnel-message)
and encrypt the tunnel messages.
Tunnel messages contain the following:

- A 4 byte Tunnel ID
- A 16 byte IV (initialization vector)
- A checksum
- Padding, if necessary
- One or more { delivery instruction, I2NP message fragment } pairs

Tunnel IDs are 4 byte numbers used at each hop - participants know what
tunnel ID to listen for messages with and what tunnel ID they should be forwarded
on as to the next hop, and each hop chooses the tunnel ID which they receive messages
on. Tunnels themselves are short-lived (10 minutes).
Even if subsequent tunnels are built using the same sequence of
peers, each hop's tunnel ID will change.

To prevent adversaries from tagging the messages along the path by adjusting
the message size, all tunnel messages are a fixed 1024 bytes in size. To accommodate
larger I2NP messages as well as to support smaller ones more efficiently, the
gateway splits up the larger I2NP messages into fragments contained within each
tunnel message. The endpoint will attempt to rebuild the I2NP message from the
fragments for a short period of time, but will discard them as necessary.

Details are in the
[tunnel message specification](/docs/specs/tunnel-message).


### Gateway Encryption

After the preprocessing of messages into a padded payload, the gateway builds
a random 16 byte IV value, iteratively encrypting it and the tunnel message as
necessary, and forwards the tuple {tunnelID, IV, encrypted tunnel message} to the next hop.

How encryption at the gateway is done depends on whether the tunnel is an
inbound or an outbound tunnel. For inbound tunnels, they simply select a random
IV, postprocessing and updating it to generate the IV for the gateway and using
that IV along side their own layer key to encrypt the preprocessed data. For outbound
tunnels they must iteratively decrypt the (unencrypted) IV and preprocessed
data with the IV and layer keys for all hops in the tunnel. The result of the outbound
tunnel encryption is that when each peer encrypts it, the endpoint will recover
the initial preprocessed data.


### Participant Processing {#tunnel.participant}

When a peer receives a tunnel message, it checks that the message came from
the same previous hop as before (initialized when the first message comes through
the tunnel). If the previous peer is a different router, or if the message has
already been seen, the message is dropped. The participant then encrypts the
received IV with AES256/ECB using their IV key to determine the current IV, uses
that IV with the participant's layer key to encrypt the data, encrypts the
current IV with AES256/ECB using their IV key again, then forwards the tuple
{nextTunnelId, nextIV, encryptedData} to the next hop. This double encryption
of the IV (both before and after use) help address a certain class of
confirmation attacks.

Duplicate message detection is handled by a decaying Bloom filter on message
IVs. Each router maintains a single Bloom filter to contain the XOR of the IV and
the first block of the message received for all of the tunnels it is participating
in, modified to drop seen entries after 10-20 minutes (when the tunnels will have
expired). The size of the bloom filter and the parameters used are sufficient to
more than saturate the router's network connection with a negligible chance of
false positive. The unique value fed into the Bloom filter is the XOR of the IV
and the first block so as to prevent nonsequential colluding peers in the tunnel
from tagging a message by resending it with the IV and first block switched.


### Endpoint Processing {#tunnel.endpoint}

After receiving and validating a tunnel message at the last hop in the tunnel,
how the endpoint recovers the data encoded by the gateway depends upon whether
the tunnel is an inbound or an outbound tunnel. For outbound tunnels, the
endpoint encrypts the message with its layer key just like any other participant,
exposing the preprocessed data. For inbound tunnels, the endpoint is also the
tunnel creator so they can merely iteratively decrypt the IV and message, using the
layer and IV keys of each step in reverse order.

At this point, the tunnel endpoint has the preprocessed data sent by the gateway,
which it may then parse out into the included I2NP messages and forwards them as
requested in their delivery instructions.


## Tunnel Building {#tunnel.building}

When building a tunnel, the creator must send a request with the necessary
configuration data to each of the hops and wait for all of them to agree before
enabling the tunnel. The requests are encrypted so that only the peers who need
to know a piece of information (such as the tunnel layer or IV key) has that
data. In addition, only the tunnel creator will have access to the peer's
reply. There are three important dimensions to keep in mind when producing
the tunnels: what peers are used (and where), how the requests are sent (and
replies received), and how they are maintained.


### Peer Selection {#tunnel.peerselection}

Beyond the two types of tunnels - inbound and outbound - there are two styles
of peer selection used for different tunnels - exploratory and client.
Exploratory tunnels are used for both network database maintenance and tunnel
maintenance, while client tunnels are used for end to end client messages.


#### Exploratory Tunnel Peer Selection {#tunnel.selection.exploratory}

Exploratory tunnels are built out of a random selection of peers from a subset
of the network. The particular subset varies on the local router and on what their
tunnel routing needs are. In general, the exploratory tunnels are built out of
randomly selected peers who are in the peer's "not failing but active" profile
category. The secondary purpose of the tunnels, beyond merely tunnel routing,
is to find underutilized high capacity peers so that they can be promoted for
use in client tunnels.

Exploratory peer selection is discussed further on the
[Peer Profiling and Selection page](/docs/overview/peer-selection).


#### Client Tunnel Peer Selection {#tunnel.selection.client}

Client tunnels are built with a more stringent set of requirements - the local
router will select peers out of its "fast and high capacity" profile category so
that performance and reliability will meet the needs of the client application.
However, there are several important details beyond that basic selection that
should be adhered to, depending upon the client's anonymity needs.

Client peer selection is discussed further on the
[Peer Profiling and Selection page](/docs/overview/peer-selection).


#### Peer Ordering within Tunnels {#ordering}

Peers are ordered within tunnels to deal with the
[predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf)
([2008 update](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

To frustrate the predecessor
attack, the tunnel selection keeps the peers selected in a strict order -
if A, B, and C are in a tunnel for a particular tunnel pool, the hop after A is always B, and the hop after
B is always C.

Ordering is implemented by generating a random 32-byte key for each
tunnel pool at startup.
Peers should not be able to guess the ordering, or an attacker could
craft two router hashes far apart to maximize the chance of being at both
ends of a tunnel.
Peers are sorted by XOR distance of the
SHA256 Hash of (the peer's hash concatenated with the random key) from the random key:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```

Because each tunnel pool uses a different random key, ordering is consistent
within a single pool but not between different pools.
New keys are generated at each router restart.


### Request Delivery {#tunnel.request}

A multi-hop tunnel is built using a single build message which is repeatedly
decrypted and forwarded. In the terminology of
[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf),
this is "non-interactive" telescopic tunnel building.

This tunnel request preparation, delivery, and response method is
[designed](/docs/specs/tunnel-creation) to reduce the number of
predecessors exposed, cuts the number of messages transmitted, verifies proper
connectivity, and avoids the message counting attack of traditional telescopic
tunnel creation.
(This method, which sends messages to extend a tunnel through the already-established
part of the tunnel, is termed "interactive" telescopic tunnel building in
the "Hashing it out" paper.)

The details of tunnel request and response messages, and their encryption,
[are specified here](/docs/specs/tunnel-creation).

Peers may reject tunnel creation requests for a variety of reasons, though
a series of four increasingly severe rejections are known: probabilistic rejection
(due to approaching the router's capacity, or in response to a flood of requests),
transient overload, bandwidth overload, and critical failure. When received,
those four are interpreted by the tunnel creator to help adjust their profile of
the router in question.

For more information on peer profiling, see the
[Peer Profiling and Selection page](/docs/overview/peer-selection).


### Tunnel Pools {#tunnel.pooling}

To allow efficient operation, the router maintains a series of tunnel pools,
each managing a group of tunnels used for a specific purpose with their own
configuration. When a tunnel is needed for that purpose, the router selects one
out of the appropriate pool at random. Overall, there are two exploratory tunnel
pools - one inbound and one outbound - each using the router's default configuration.
In addition, there is a pair of pools for each local destination -
one inbound and one outbound tunnel pool. Those pools use the configuration specified
when the local destination connects to the router via [I2CP](/docs/specs/i2cp), or the router's defaults if
not specified.

Each pool has within its configuration a few key settings, defining how many
tunnels to keep active, how many backup tunnels to maintain in case of failure,
how long the tunnels should be, whether those
lengths should be randomized, as
well as any of the other settings allowed when configuring individual tunnels.
Configuration options are specified on the [I2CP page](/docs/specs/i2cp).


### Tunnel Lengths and Defaults {#length}

[On the tunnel overview page](/docs/overview/tunnel-routing#length).


### Anticipatory Build Strategy and Priority {#strategy}

Tunnel building is expensive, and tunnels expire a fixed time after they are built.
However, when a pool that runs out of tunnels, the Destination is essentially dead.
In addition, tunnel build success rate may vary greatly with both local and global
network conditions.
Therefore, it is important to maintain an anticipatory, adaptive build strategy
to ensure that new tunnels are successfully built before they are needed,
without building an excess of tunnels, building them too soon,
or consuming too much CPU or bandwidth creating and sending the encrypted build messages.

For each tuple {exploratory/client, in/out, length, length variance}
the router maintains statistics on the time required for a successful
tunnel build.
Using these statistics, it calculates how long before a tunnel's expiration
it should start attempting to build a replacement.
As the expiration time approaches without a successful replacement,
it starts multiple build attempts in parallel, and then
will increase the number of parallel attempts if necessary.

To cap bandwidth and CPU usage,
the router also limits the maximum number of build attempts outstanding
across all pools.
Critical builds (those for exploratory tunnels, and for pools that have
run out of tunnels) are prioritized.


## Tunnel Message Throttling {#tunnel.throttling}

Even though the tunnels within I2P bear a resemblance to a circuit switched
network, everything within I2P is strictly message based - tunnels are merely
accounting tricks to help organize the delivery of messages. No assumptions are
made regarding reliability or ordering of messages, and retransmissions are left
to higher levels (e.g. I2P's client layer streaming library). This allows I2P
to take advantage of throttling techniques available to both packet switched and
circuit switched networks. For instance, each router may keep track of the
moving average of how much data each tunnel is using, combine that with all of
the averages used by other tunnels the router is participating in, and be able
to accept or reject additional tunnel participation requests based on its
capacity and utilization. On the other hand, each router can simply drop
messages that are beyond its capacity, exploiting the research used on the
normal Internet.

In the current implementation, routers implement a
weighted random early discard (WRED) strategy.
For all participating routers (internal participant, inbound gateway, and outbound endpoint),
the router will start randomly dropping a portion of messages as the
bandwidth limits are approached.
As traffic gets closer to, or exceeds, the limits, more messages are dropped.
For an internal participant, all messages are fragmented and padded and therefore are the same size.
At the inbound gateway and outbound endpoint, however, the dropping decision is made
on the full (coalesced) message, and the message size is taken into account.
Larger messages are more likely to be dropped.
Also, messages are more likely to be dropped at the outbound endpoint than the inbound gateway,
as those messages are not as "far along" in their journey and thus the network cost of
dropping those messages is lower.


## Future Work {#future}

### Mixing/Batching {#tunnel.mixing}

What strategies could be used at the gateway and at each hop for delaying,
reordering, rerouting, or padding messages? To what extent should this be done
automatically, how much should be configured as a per tunnel or per hop setting,
and how should the tunnel's creator (and in turn, user) control this operation?
All of this is left as unknown, to be worked out for a distant future release.


### Padding

The padding strategies can be used on a variety of levels, addressing the
exposure of message size information to different adversaries.
The current fixed tunnel message size is 1024 bytes. Within this however, the fragmented
messages themselves are not padded by the tunnel at all, though for end to end
messages, they may be padded as part of the garlic wrapping.


### WRED

WRED strategies have a significant impact on end-to-end performance,
and prevention of network congestion collapse.
The current WRED strategy should be carefully evaluated and improved.
