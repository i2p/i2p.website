---
title: "Old Tunnel Implementation"
description: "Historical documentation of I2P's original tunnel implementation before 0.6.1.10"
slug: "old-tunnel-implementation"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Note: Obsolete - NOT used! Replaced in 0.6.1.10 - see [current implementation](/docs/specs/tunnel-implementation) for the active specification.**


## 1) Tunnel overview {#tunnel.overview}

Within I2P, messages are passed in one direction through a virtual
tunnel of peers, using whatever means are available to pass the
message on to the next hop. Messages arrive at the tunnel's
gateway, get bundled up for the path, and are forwarded on to the
next hop in the tunnel, which processes and verifies the validity
of the message and sends it on to the next hop, and so on, until
it reaches the tunnel endpoint. That endpoint takes the messages
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
data. They may vary in length from 0 hops (where the gateway
is also the endpoint) to 7 hops (where there are 6 peers after
the gateway and before the endpoint). It is the intent to make
it hard for either participants or third parties to determine
the length of a tunnel, or even for colluding participants to
determine whether they are a part of the same tunnel at all
(barring the situation where colluding peers are next to each other
in the tunnel). Messages that have been corrupted are also dropped
as soon as possible, reducing network load.

Beyond their length, there are additional configurable parameters
for each tunnel that can be used, such as a throttle on the size or
frequency of messages delivered, how padding should be used, how
long a tunnel should be in operation, whether to inject chaff
messages, whether to use fragmentation, and what, if any, batching
strategies should be employed.

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


## 2) Tunnel operation {#tunnel.operation}

Tunnel operation has four distinct processes, taken on by various
peers in the tunnel. First, the tunnel gateway accumulates a number
of tunnel messages and preprocesses them into something for tunnel
delivery. Next, that gateway encrypts that preprocessed data, then
forwards it to the first hop. That peer, and subsequent tunnel
participants, unwrap a layer of the encryption, verifying the
integrity of the message, then forward it on to the next peer.
Eventually, the message arrives at the endpoint where the messages
bundled by the gateway are split out again and forwarded on as
requested.

Tunnel IDs are 4 byte numbers used at each hop - participants know what
tunnel ID to listen for messages with and what tunnel ID they should be forwarded
on as to the next hop. Tunnels themselves are short lived (10 minutes at the
moment), but depending upon the tunnel's purpose, and though subsequent tunnels
may be built using the same sequence of peers, each hop's tunnel ID will change.


### 2.1) Message preprocessing {#tunnel.preprocessing}

When the gateway wants to deliver data through the tunnel, it first
gathers zero or more I2NP messages (no more than 32KB worth),
selects how much padding will be used, and decides how each I2NP
message should be handled by the tunnel endpoint, encoding that
data into the raw tunnel payload:

- 2 byte unsigned integer specifying the # of padding bytes
- that many random bytes
- a series of zero or more { instructions, message } pairs

The instructions are encoded as follows:

- 1 byte value:
  ```
  bits 0-1: delivery type
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: delay included?  (1 = true, 0 = false)
     bit 3: fragmented?  (1 = true, 0 = false)
     bit 4: extended options?  (1 = true, 0 = false)
  bits 5-7: reserved
  ```
- if the delivery type was TUNNEL, a 4 byte tunnel ID
- if the delivery type was TUNNEL or ROUTER, a 32 byte router hash
- if the delay included flag is true, a 1 byte value:
  ```
     bit 0: type (0 = strict, 1 = randomized)
  bits 1-7: delay exponent (2^value minutes)
  ```
- if the fragmented flag is true, a 4 byte message ID, and a 1 byte value:
  ```
  bits 0-6: fragment number
     bit 7: is last?  (1 = true, 0 = false)
  ```
- if the extended options flag is true:
  ```
  = a 1 byte option size (in bytes)
  = that many bytes
  ```
- 2 byte size of the I2NP message

The I2NP message is encoded in its standard form, and the
preprocessed payload must be padded to a multiple of 16 bytes.


### 2.2) Gateway processing {#tunnel.gateway}

After the preprocessing of messages into a padded payload, the gateway
encrypts the payload with the eight keys, building a checksum block so
that each peer can verify the integrity of the payload at any time, as
well as an end to end verification block for the tunnel endpoint to
verify the integrity of the checksum block. The specific details follow.

The encryption used is such that decryption
merely requires running over the data with AES in CBC mode, calculating the
SHA256 of a certain fixed portion of the message (bytes 16 through $size-144),
and searching for the first 16 bytes of that hash in the checksum block. There is a fixed number
of hops defined (8 peers) so that we can verify the message
without either leaking the position in the tunnel or having the message
continually "shrink" as layers are peeled off. For tunnels shorter than 8
hops, the tunnel creator will take the place of the excess hops, decrypting
with their keys (for outbound tunnels, this is done at the beginning, and for
inbound tunnels, the end).

The hard part in the encryption is building that entangled checksum block,
which requires essentially finding out what the hash of the payload will look
like at each step, randomly ordering those hashes, then building a matrix of
what each of those randomly ordered hashes will look like at each step. The
gateway itself must pretend that it is one of the peers within the checksum
block so that the first hop cannot tell that the previous hop was the gateway.
To visualize this a bit:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>

In the above, P[7] is the same as the original data being passed through the
tunnel (the preprocessed messages), and V[7] is the first 16 bytes of the SHA256 of eH[0-7] as seen on
peer7 after decryption. For
cells in the matrix "higher up" than the hash, their value is derived by encrypting
the cell below it with the key for the peer below it, using the end of the column
to the left of it as the IV. For cells in the matrix "lower down" than the hash,
they're equal to the cell above them, decrypted by the current peer's key, using
the end of the previous encrypted block on that row.

With this randomized matrix of checksum blocks, each peer will be able to find
the hash of the payload, or if it is not there, know that the message is corrupt.
The entanglement by using CBC mode increases the difficulty in tagging the
checksum blocks themselves, but it is still possible for that tagging to go
briefly undetected if the columns after the tagged data have already been used
to check the payload at a peer. In any case, the tunnel endpoint (peer 7) knows
for certain whether any of the checksum blocks have been tagged, as that would
corrupt the verification block (V[7]).

The IV[0] is a random 16 byte value, and IV[i] is the first 16 bytes of
H(D(IV[i-1], K[i-1]) xor IV_WHITENER). We don't use the same IV along the path, as that would
allow trivial collusion, and we use the hash of the decrypted value to propagate
the IV so as to hamper key leakage. IV_WHITENER is a fixed 16 byte value.

When the gateway wants to send the message, they export the right row for the
peer who is the first hop (usually the peer1.recv row) and forward that entirely.


### 2.3) Participant processing {#tunnel.participant}

When a participant in a tunnel receives a message, they decrypt a layer with their
tunnel key using AES256 in CBC mode with the first 16 bytes as the IV. They then
calculate the hash of what they see as the payload (bytes 16 through $size-144) and
search for that first 16 bytes of that hash within the decrypted checksum block. If no match is found, the
message is discarded. Otherwise, the IV is updated by decrypting it, XORing that value
with the IV_WHITENER, and replacing it with the first 16 bytes of its hash. The
resulting message is then forwarded on to the next peer for processing.

To prevent replay attacks at the tunnel level, each participant keeps track of
the IVs received during the tunnel's lifetime, rejecting duplicates. The memory
usage required should be minor, as each tunnel has only a very short lifespan (10m
at the moment). A constant 100KBps through a tunnel with full 32KB messages would
give 1875 messages, requiring less than 30KB of memory. Gateways and endpoints
handle replay by tracking the message IDs and expirations on the I2NP messages
contained in the tunnel.


### 2.4) Endpoint processing {#tunnel.endpoint}

When a message reaches the tunnel endpoint, they decrypts and verifies it like
a normal participant. If the checksum block has a valid match, the endpoint then
computes the hash of the checksum block itself (as seen after decryption) and compares
that to the decrypted verification hash (the last 16 bytes). If that verification
hash does not match, the endpoint takes note of the tagging attempt by one of the
tunnel participants and perhaps discards the message.

At this point, the tunnel endpoint has the preprocessed data sent by the gateway,
which it may then parse out into the included I2NP messages and forwards them as
requested in their delivery instructions.


### 2.5) Padding {#tunnel.padding}

Several tunnel padding strategies are possible, each with their own merits:

- No padding
- Padding to a random size
- Padding to a fixed size
- Padding to the closest KB
- Padding to the closest exponential size (2^n bytes)

*Which to use? no padding is most efficient, random padding is what
we have now, fixed size would either be an extreme waste or force us to
implement fragmentation. Padding to the closest exponential size (ala Freenet)
seems promising. Perhaps we should gather some stats on the net as to what size
messages are, then see what costs and benefits would arise from different
strategies?*


### 2.6) Tunnel fragmentation {#tunnel.fragmentation}

For various padding and mixing schemes, it may be useful from an anonymity
perspective to fragment a single I2NP message into multiple parts, each delivered
separately through different tunnel messages. The endpoint may or may not
support that fragmentation (discarding or hanging on to fragments as needed),
and handling fragmentation will not immediately be implemented.


### 2.7) Alternatives {#tunnel.alternatives}

#### 2.7.1) Don't use a checksum block {#tunnel.nochecksum}

One alternative to the above process is to remove the checksum block
completely and replace the verification hash with a plain hash of the payload.
This would simplify processing at the tunnel gateway and save 144 bytes of
bandwidth at each hop. On the other hand, attackers within the tunnel could
trivially adjust the message size to one which is easily traceable by
colluding external observers in addition to later tunnel participants. The
corruption would also incur the waste of the entire bandwidth necessary to
pass on the message. Without the per-hop validation, it would also be possible
to consume excess network resources by building extremely long tunnels, or by
building loops into the tunnel.


#### 2.7.2) Adjust tunnel processing midstream {#tunnel.reroute}

While the simple tunnel routing algorithm should be sufficient for most cases,
there are three alternatives that can be explored:

- Delay a message within a tunnel at an arbitrary hop for either a specified
  amount of time or a randomized period. This could be achieved by replacing the
  hash in the checksum block with e.g. the first 8 bytes of the hash, followed by
  some delay instructions. Alternately, the instructions could tell the
  participant to actually interpret the raw payload as it is, and either discard
  the message or continue to forward it down the path (where it would be
  interpreted by the endpoint as a chaff message). The later part of this would
  require the gateway to adjust its encryption algorithm to produce the cleartext
  payload on a different hop, but it shouldn't be much trouble.

- Allow routers participating in a tunnel to remix the message before
  forwarding it on - bouncing it through one of that peer's own outbound tunnels,
  bearing instructions for delivery to the next hop. This could be used in either
  a controlled manner (with en-route instructions like the delays above) or
  probabilistically.

- Implement code for the tunnel creator to redefine a peer's "next hop" in
  the tunnel, allowing further dynamic redirection.


#### 2.7.3) Use bidirectional tunnels {#tunnel.bidirectional}

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


#### 2.7.4) Use smaller blocksize {#tunnel.smallerhashes}

At the moment, our use of AES limits our block size to 16 bytes, which
in turn provides the minimum size for each of the checksum block columns.
If another algorithm was used with a smaller block size, or could otherwise
allow the safe building of the checksum block with smaller portions of the
hash, it might be worth exploring. The 16 bytes used now at each hop should
be more than sufficient.


## 3) Tunnel building {#tunnel.building}

When building a tunnel, the creator must send a request with the necessary
configuration data to each of the hops, then wait for the potential participant
to reply stating that they either agree or do not agree. These tunnel request
messages and their replies are garlic wrapped so that only the router who knows
the key can decrypt it, and the path taken in both directions is tunnel routed
as well. There are three important dimensions to keep in mind when producing
the tunnels: what peers are used (and where), how the requests are sent (and
replies received), and how they are maintained.


### 3.1) Peer selection {#tunnel.peerselection}

Beyond the two types of tunnels - inbound and outbound - there are two styles
of peer selection used for different tunnels - exploratory and client.
Exploratory tunnels are used for both network database maintenance and tunnel
maintenance, while client tunnels are used for end to end client messages.


#### 3.1.1) Exploratory tunnel peer selection {#tunnel.selection.exploratory}

Exploratory tunnels are built out of a random selection of peers from a subset
of the network. The particular subset varies on the local router and on what their
tunnel routing needs are. In general, the exploratory tunnels are built out of
randomly selected peers who are in the peer's "not failing but active" profile
category. The secondary purpose of the tunnels, beyond merely tunnel routing,
is to find underutilized high capacity peers so that they can be promoted for
use in client tunnels.


#### 3.1.2) Client tunnel peer selection {#tunnel.selection.client}

Client tunnels are built with a more stringent set of requirements - the local
router will select peers out of its "fast and high capacity" profile category so
that performance and reliability will meet the needs of the client application.
However, there are several important details beyond that basic selection that
should be adhered to, depending upon the client's anonymity needs.

For some clients who are worried about adversaries mounting a predecessor
attack, the tunnel selection can keep the peers selected in a strict order -
if A, B, and C are in a tunnel, the hop after A is always B, and the hop after
B is always C. A less strict ordering is also possible, assuring that while
the hop after A may be B, B may never be before A. Other configuration options
include the ability for just the inbound tunnel gateways and outbound tunnel
endpoints to be fixed, or rotated on an MTBF rate.


### 3.2) Request delivery {#tunnel.request}

As mentioned above, once the tunnel creator knows what peers should go into
a tunnel and in what order, the creator builds a series of tunnel request
messages, each containing the necessary information for that peer. For instance,
participating tunnels will be given the 4 byte tunnel ID on which they are to
receive messages, the 4 byte tunnel ID on which they are to send out the messages,
the 32 byte hash of the next hop's identity, and the 32 byte layer key used to
remove a layer from the tunnel. Of course, outbound tunnel endpoints are not
given any "next hop" or "next tunnel ID" information. Inbound tunnel gateways
are however given the 8 layer keys in the order they should be encrypted (as
described above). To allow replies, the request contains a random session tag
and a random session key with which the peer may garlic encrypt their decision,
as well as the tunnel to which that garlic should be sent. In addition to the
above information, various client specific options may be included, such as
what throttling to place on the tunnel, what padding or batch strategies to use,
etc.

After building all of the request messages, they are garlic wrapped for the
target router and sent out an exploratory tunnel. Upon receipt, that peer
determines whether they can or will participate, creating a reply message and
both garlic wrapping and tunnel routing the response with the supplied
information. Upon receipt of the reply at the tunnel creator, the tunnel is
considered valid on that hop (if accepted). Once all peers have accepted, the
tunnel is active.


### 3.3) Pooling {#tunnel.pooling}

To allow efficient operation, the router maintains a series of tunnel pools,
each managing a group of tunnels used for a specific purpose with their own
configuration. When a tunnel is needed for that purpose, the router selects one
out of the appropriate pool at random. Overall, there are two exploratory tunnel
pools - one inbound and one outbound - each using the router's exploration
defaults. In addition, there is a pair of pools for each local destination -
one inbound and one outbound tunnel. Those pools use the configuration specified
when the local destination connected to the router, or the router's defaults if
not specified.

Each pool has within its configuration a few key settings, defining how many
tunnels to keep active, how many backup tunnels to maintain in case of failure,
how frequently to test the tunnels, how long the tunnels should be, whether those
lengths should be randomized, how often replacement tunnels should be built, as
well as any of the other settings allowed when configuring individual tunnels.


### 3.4) Alternatives {#tunnel.building.alternatives}

#### 3.4.1) Telescopic building {#tunnel.building.telescoping}

One question that may arise regarding the use of the exploratory tunnels for
sending and receiving tunnel creation messages is how that impacts the tunnel's
vulnerability to predecessor attacks. While the endpoints and gateways of
those tunnels will be randomly distributed across the network (perhaps even
including the tunnel creator in that set), another alternative is to use the
tunnel pathways themselves to pass along the request and response, as is done
in [TOR](https://www.torproject.org/). This, however, may lead to leaks
during tunnel creation, allowing peers to discover how many hops there are later
on in the tunnel by monitoring the timing or packet count as the tunnel is
built. Techniques could be used to minimize this issue, such as using each of
the hops as endpoints (per [2.7.2](#tunnel.reroute)) for a random
number of messages before continuing on to build the next hop.


#### 3.4.2) Non-exploratory tunnels for management {#tunnel.building.nonexploratory}

A second alternative to the tunnel building process is to give the router
an additional set of non-exploratory inbound and outbound pools, using those for
the tunnel request and response. Assuming the router has a well integrated view
of the network, this should not be necessary, but if the router was partitioned
in some way, using non-exploratory pools for tunnel management would reduce the
leakage of information about what peers are in the router's partition.


## 4) Tunnel throttling {#tunnel.throttling}

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


## 5) Mixing/batching {#tunnel.mixing}

What strategies should be used at the gateway and at each hop for delaying,
reordering, rerouting, or padding messages? To what extent should this be done
automatically, how much should be configured as a per tunnel or per hop setting,
and how should the tunnel's creator (and in turn, user) control this operation?
All of this is left as unknown, to be worked out for a future release.
