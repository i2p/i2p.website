---
title: "Match OBEPs with IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Overview

This proposal adds an I2CP option for outbound tunnels that causes tunnels to be
picked or built when a message is sent such that the OBEP matches one of the
IBGWs from the LeaseSet for the target Destination.


## Motivation

Most I2P routers employ a form of packet-dropping for congestion management. The
reference implementation uses a WRED strategy that takes both message size and
travel distance into account (see [tunnel throttling documentation](/docs/specs/implementation/#tunnelthrottling)). Due to this strategy, the
primary source of packet loss is the OBEP.


## Design

When sending a message, the sender picks or builds a tunnel with an OBEP that is
the same router as one of the recipient's IBGWs. By doing so, the message will
go directly out of one tunnel and into the other, without needing to be sent
across the wire in between.


## Security implications

This mode would effectively mean that the recipient is selecting the sender's
OBEP. In order to maintain current privacy, this mode would cause outbound
tunnels to be built one hop longer than specified by the outbound.length I2CP
option (with the final hop possibly being outside the sender's fast tier).


## Specification

A new I2CP option is added to the [I2CP specification](/docs/specs/i2cp/):

    outbound.matchEndWithTarget
        Boolean

        Default value: case-specific

        If true, the router will pick outbound tunnels for messages sent during
        this session such that the tunnel's OBEP is one of the IBGWs for the
        target Destination. If no such tunnel exists, the router will build one.


## Compatibility

Backwards-compatibility is assured, as routers can always send messages to
themselves.


## Implementation

### Java I2P

Tunnel building and message sending are currently separate subsystems:

- BuildExecutor only knows about the outbound tunnel pool's outbound.* options,
  and has no visibility regarding their use.

- OutboundClientMessageOneShotJob can only select a tunnel from the existing
  pool; if a client message comes in and there are no outbound tunnels, the
  router drops the message.

Implementing this proposal would require designing a way for these two
subsystems to interact.

### i2pd

A test implementation has been completed.


## Performance

This proposal has various effects on latency, RTT and packet loss:

- It is likely that in most cases, this mode would require building a new tunnel
  on first message rather than using an existing tunnel, adding latency.

- For standard tunnels, the OBEP may need to find and connect to the IBGW,
  adding latency that increases the first RTT (as this occurs after the first
  packet has been sent). Using this mode, the OBEP would need to find and
  connect to the IBGW during tunnel building, adding the same latency but
  reducing the first RTT (as this occurs before the first packet has been sent).

- The currently-standard VariableTunnelBuild size is 2641 bytes. Thus it is
  expected that this mode would result in lower packet loss for average message
  sizes larger than this.

More research is necessary to investigate these effects, in order to decide
which standard tunnels would benefit from this mode being enabled by default.


## References

* [Destination](/docs/specs/common-structures/#destination)
* [I2CP-SPEC](/docs/specs/i2cp/)
* [LeaseSet](/docs/specs/common-structures/#leaseset)
* [TUNNEL-THROTTLING](/docs/specs/implementation/#tunnel.throttling)
* [VariableTunnelBuild](/docs/specs/common-structures/#variabletunnelbuild)
