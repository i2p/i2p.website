---
title: "Tunnel Routing"
description: "Overview of I2P tunnel terminology, construction, and operation"
slug: "tunnel-routing"
lastUpdated: "2011-07"
accurateFor: "0.8.7"
---

## Overview

This page contains an overview of I2P tunnel terminology and operation, with links to more technical pages, details, and specifications.

As briefly explained in the [introduction](/docs/overview/intro/), I2P builds virtual "tunnels" - temporary and unidirectional paths through a sequence of routers. These tunnels are classified as either inbound tunnels (where everything given to it goes towards the creator of the tunnel) or outbound tunnels (where the tunnel creator shoves messages away from them). When Alice wants to send a message to Bob, she will (typically) send it out one of her existing outbound tunnels with instructions for that tunnel's endpoint to forward it to the gateway router for one of Bob's current inbound tunnels, which in turn passes it to Bob.

![Alice connecting through her outbound tunnel to Bob via his inbound tunnel](/images/tunnelSending.png)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```

---

## Tunnel Vocabulary

- **Tunnel gateway** - the first router in a tunnel. For inbound tunnels, this is the one mentioned in the LeaseSet published in the [network database](/docs/overview/network-database/). For outbound tunnels, the gateway is the originating router. (e.g. both A and D above)

- **Tunnel endpoint** - the last router in a tunnel. (e.g. both C and F above)

- **Tunnel participant** - all routers in a tunnel except for the gateway or endpoint (e.g. both B and E above)

- **n-Hop tunnel** - a tunnel with a specific number of inter-router jumps, e.g.:
  - **0-hop tunnel** - a tunnel where the gateway is also the endpoint
  - **1-hop tunnel** - a tunnel where the gateway talks directly to the endpoint
  - **2-(or more)-hop tunnel** - a tunnel where there is at least one intermediate tunnel participant. (the above diagram includes two 2-hop tunnels - one outbound from Alice, one inbound to Bob)

- **Tunnel ID** - A [4 byte integer](/docs/specs/common-structures/#type_TunnelId) different for each hop in a tunnel, and unique among all tunnels on a router. Chosen randomly by the tunnel creator.

---

## Tunnel Build Information

Routers performing the three roles (gateway, participant, endpoint) are given different pieces of data in the initial [Tunnel Build Message](/docs/specs/tunnel-creation/) to accomplish their tasks:

**The tunnel gateway gets:**

- **tunnel encryption key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for encrypting messages and instructions to the next hop
- **tunnel IV key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for double-encrypting the IV to the next hop
- **reply key** - an [AES public key](/docs/specs/common-structures/#type_SessionKey) for encrypting the reply to the tunnel build request
- **reply IV** - the IV for encrypting the reply to the tunnel build request
- **tunnel id** - 4 byte integer (inbound gateways only)
- **next hop** - what router is the next one in the path (unless this is a 0-hop tunnel, and the gateway is also the endpoint)
- **next tunnel id** - The tunnel ID on the next hop

**All intermediate tunnel participants get:**

- **tunnel encryption key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for encrypting messages and instructions to the next hop
- **tunnel IV key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for double-encrypting the IV to the next hop
- **reply key** - an [AES public key](/docs/specs/common-structures/#type_SessionKey) for encrypting the reply to the tunnel build request
- **reply IV** - the IV for encrypting the reply to the tunnel build request
- **tunnel id** - 4 byte integer
- **next hop** - what router is the next one in the path
- **next tunnel id** - The tunnel ID on the next hop

**The tunnel endpoint gets:**

- **tunnel encryption key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for encrypting messages and instructions to the endpoint (itself)
- **tunnel IV key** - an [AES private key](/docs/specs/common-structures/#type_SessionKey) for double-encrypting the IV to the endpoint (itself)
- **reply key** - an [AES public key](/docs/specs/common-structures/#type_SessionKey) for encrypting the reply to the tunnel build request (outbound endpoints only)
- **reply IV** - the IV for encrypting the reply to the tunnel build request (outbound endpoints only)
- **tunnel id** - 4 byte integer (outbound endpoints only)
- **reply router** - the inbound gateway of the tunnel to send the reply through (outbound endpoints only)
- **reply tunnel id** - The tunnel ID of the reply router (outbound endpoints only)

Details are in the [tunnel creation specification](/docs/specs/tunnel-creation/).

---

## Tunnel Pooling

Several tunnels for a particular purpose may be grouped into a "tunnel pool", as described in the [tunnel specification](/docs/specs/tunnel-implementation/#tunnel.pooling). This provides redundancy and additional bandwidth. The pools used by the router itself are called "exploratory tunnels". The pools used by applications are called "client tunnels".

---

## Tunnel Length

As mentioned above, each client requests that their router provide tunnels to include at least a certain number of hops. The decision as to how many routers to have in one's outbound and inbound tunnels has an important effect upon the latency, throughput, reliability, and anonymity provided by I2P - the more peers that messages have to go through, the longer it takes to get there and the more likely that one of those routers will fail prematurely. The less routers in a tunnel, the easier it is for an adversary to mount traffic analysis attacks and pierce someone's anonymity. Tunnel lengths are specified by clients via [I2CP options](/docs/specs/i2cp/#options). The maximum number of hops in a tunnel is 7.

### 0-hop tunnels

With no remote routers in a tunnel, the user has very basic plausible deniability (since no one knows for sure that the peer that sent them the message wasn't simply just forwarding it on as part of the tunnel). However, it would be fairly easy to mount a statistical analysis attack and notice that messages targeting a specific destination are always sent through a single gateway. Statistical analysis against outbound 0-hop tunnels are more complex, but could show similar information (though would be slightly harder to mount).

### 1-hop tunnels

With only one remote router in a tunnel, the user has both plausible deniability and basic anonymity, as long as they are not up against an internal adversary (as described on [threat model](/docs/overview/threat-model/)). However, if the adversary ran a sufficient number of routers such that the single remote router in the tunnel is often one of those compromised ones, they would be able to mount the above statistical traffic analysis attack.

### 2-hop tunnels

With two or more remote routers in a tunnel, the costs of mounting the traffic analysis attack increases, since many remote routers would have to be compromised to mount it.

### 3-hop (or more) tunnels

To reduce the susceptibility to [some attacks](http://blog.torproject.org/blog/one-cell-enough), 3 or more hops are recommended for the highest level of protection. [Recent studies](http://blog.torproject.org/blog/one-cell-enough) also conclude that more than 3 hops does not provide additional protection.

### Tunnel default lengths

The router uses 2-hop tunnels by default for its exploratory tunnels. Client tunnel defaults are set by the application, using [I2CP options](/docs/specs/i2cp/#options). Most applications use 2 or 3 hops as their default.

---

## Tunnel Testing

All tunnels are periodically tested by their creator by sending a DeliveryStatusMessage out an outbound tunnel and bound for another inbound tunnel (testing both tunnels at once). If either fails a number of consecutive tests, it is marked as no longer functional. If it was used for a client's inbound tunnel, a new leaseSet is created. Tunnel test failures are also reflected in the [capacity rating in the peer profile](/docs/overview/peer-selection/#capacity).

---

## Tunnel Creation

Tunnel creation is handled by [garlic routing](/docs/overview/garlic-routing/) a Tunnel Build Message to a router, requesting that they participate in the tunnel (providing them with all of the appropriate information, as above, along with a certificate, which right now is a 'null' cert, but will support hashcash or other non-free certificates when necessary). That router forwards the message to the next hop in the tunnel. Details are in the [tunnel creation specification](/docs/specs/tunnel-creation/).

---

## Tunnel Encryption

Multi-layer encryption is handled by [garlic encryption](/docs/overview/garlic-routing/) of tunnel messages. Details are in the [tunnel specification](/docs/specs/tunnel-implementation/). The IV of each hop is encrypted with a separate key as explained there.

---

## Future Work

- Other tunnel test techniques could be used, such as garlic wrapping a number of tests into cloves, testing individual tunnel participants separately, etc.

- Move to 3-hop exploratory tunnels defaults.

- In a distant future release, options specifying the pooling, mixing, and chaff generation settings may be implemented.

- In a distant future release, limits on the quantity and size of messages allowed during the tunnel's lifetime may be implemented (e.g. no more than 300 messages or 1MB per minute).

---

## See Also

- [Tunnel specification](/docs/specs/tunnel-implementation/)
- [Tunnel creation specification](/docs/specs/tunnel-creation/)
- [Unidirectional tunnels](/docs/legacy/unidirectional/)
- [Tunnel message specification](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP options](/docs/specs/i2cp/#options)
