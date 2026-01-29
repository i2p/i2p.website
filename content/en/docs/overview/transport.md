---
title: "Transport Overview"
description: "Overview of I2P's transport layer for point-to-point router communication"
slug: "transport"
lastUpdated: "2018-06"
accurateFor: "0.9.36"
---

## Transports in I2P

A "transport" in I2P is a method for direct, point-to-point communication between two routers. Transports must provide confidentiality and integrity against external adversaries while authenticating that the router contacted is the one who should receive a given message.

I2P supports multiple transports simultaneously. There are three transports currently implemented:

1. [NTCP](/docs/legacy/ntcp/), a Java New I/O (NIO) TCP transport
2. [SSU](/docs/legacy/ssu/), or Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), a new version of NTCP

Each provides a "connection" paradigm, with authentication, flow control, acknowledgments and retransmission.

---

## Transport Services

The transport subsystem in I2P provides the following services:

- Reliable delivery of [I2NP](/docs/specs/i2np/) messages. Transports support I2NP message delivery ONLY. They are not general-purpose data pipes.
- In-order delivery of messages is NOT guaranteed by all transports.
- Maintain a set of router addresses, one or more for each transport, that the router publishes as its global contact information (the RouterInfo). Each transport may connect using one of these addresses, which may be IPv4 or (as of version 0.9.8) IPv6.
- Selection of the best transport for each outgoing message
- Queueing of outbound messages by priority
- Bandwidth limiting, both outbound and inbound, according to router configuration
- Setup and teardown of transport connections
- Encryption of point-to-point communications
- Maintenance of connection limits for each transport, implementation of various thresholds for these limits, and communication of threshold status to the router so it may make operational changes based on the status
- Firewall port opening using UPnP (Universal Plug and Play)
- Cooperative NAT/Firewall traversal
- Local IP detection by various methods, including UPnP, inspection of incoming connections, and enumeration of network devices
- Coordination of firewall status and local IP, and changes to either, among the transports
- Communication of firewall status and local IP, and changes to either, to the router and the user interface
- Determination of a consensus clock, which is used to periodically update the router's clock, as a backup for NTP
- Maintenance of status for each peer, including whether it is connected, whether it was recently connected, and whether it was reachable in the last attempt
- Qualification of valid IP addresses according to a local rule set
- Honoring the automated and manual lists of banned peers maintained by the router, and refusing outbound and inbound connections to those peers

---

## Transport Addresses

The transport subsystem maintains a set of router addresses, each of which lists a transport method, IP, and port. These addresses constitute the advertised contact points, and are published by the router to the network database. Addresses may also contain an arbitrary set of additional options.

Each transport method may publish multiple router addresses.

Typical scenarios are:

- A router has no published addresses, so it is considered "hidden" and cannot receive incoming connections
- A router is firewalled, and therefore publishes an SSU address which contains a list of cooperating peers or "introducers" who will assist in NAT traversal (see [the SSU spec](/docs/legacy/ssu/) for details)
- A router is not firewalled or its NAT ports are open; it publishes both NTCP and SSU addresses containing directly-accessible IP and ports.

---

## Transport Selection

The transport system delivers [I2NP messages](/docs/specs/i2np/) only. The transport selected for any message is independent of the upper-layer protocols and contents (router or client messages, whether an external application was using TCP or UDP to connect to I2P, whether the upper layer was using [the streaming library](/docs/api/streaming/) or [datagrams](/docs/api/datagrams/), etc.).

For each outgoing message, the transport system solicits "bids" from each transport. The transport bidding the lowest (best) value wins the bid and receives the message for delivery. A transport may refuse to bid.

Whether a transport bids, and with what value, depend on numerous factors:

- Configuration of transport preferences
- Whether the transport is already connected to the peer
- The number of current connections compared to various connection limit thresholds
- Whether recent connection attempts to the peer have failed
- The size of the message, as different transports have different size limits
- Whether the peer can accept incoming connections for that transport, as advertised in its RouterInfo
- Whether the connection would be indirect (requiring introducers) or direct
- The peer's transport preference, as advertised in its RouterInfo

In general, the bid values are selected so that two routers are only connected by a single transport at any one time. However, this is not a requirement.

---

## New Transports and Future Work

Additional transports may be developed, including:

- A TLS/SSH look-alike transport
- An "indirect" transport for routers that are not reachable by all other routers (one form of "restricted routes")
- Tor-compatible pluggable transports

Work continues on adjusting default connection limits for each transport. I2P is designed as a "mesh network", where it is assumed that any router can connect to any other router. This assumption may be broken by routers that have exceeded their connection limits, and by routers that are behind restrictive state firewalls (restricted routes).

The current connection limits are higher for SSU than for NTCP, based on the assumption that the memory requirements for an NTCP connection are higher than that for SSU. However, as NTCP buffers are partially in the kernel and SSU buffers are on the Java heap, that assumption is difficult to verify.

Analyze [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) and see how transport-layer padding may improve things.
