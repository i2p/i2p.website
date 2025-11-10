---
title: "SSU2 Transport"
date: 2022-10-11
author: "zzz"
description: "SSU2 Transport"
categories: ["development"]
---

## Overview

I2P has used a censorship-resistant UDP transport protocol "SSU" since 2005.
We've had few, if any, reports of SSU being blocked in 17 years.
However, by today's standards of security, blocking resistance,
and performance, we can do better. Much better.

That's why, together with the [i2pd project](https://i2pd.xyz/), we have created and implemented "SSU2",
a modern UDP protocol designed to the highest standards of security and blocking resistance.
This protocol will replace SSU.

We have combined industry-standard encryption with the best
features of UDP protocols WireGuard and QUIC, together with the
censorship resistance features of our TCP protocol "NTCP2".
SSU2 may be one of the most secure transport protocols ever designed.

The Java I2P and i2pd teams are finishing the SSU2 transport and we will enable it for all routers in the next release.
This completes our decade-long plan to upgrade all the cryptography from the original
Java I2P implementation dating back to 2003.
SSU2 will replace SSU, our sole remaining use of ElGamal cryptography.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

After the transition to SSU2,
we will have migrated all our authenticated and encrypted protocols to standard [Noise Protocol](https://noiseprotocol.org/) handshakes:

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

All I2P Noise protocols use the following standard cryptographic algorithms:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Goals

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Design

I2P uses multiple layers of encryption to protect traffic from attackers.
The lowest layer is the transport protocol layer, used for point-to-point links between two routers.
We currently have two transport protocols:
NTCP2, a modern TCP protocol introduced in 2018,
and SSU, a UDP protocol developed in 2005.

SSU2, like previous I2P transport protocols, is not a general-purpose pipe for data.
Its primary task is to securely deliver I2P's low-level I2NP messages
from one router to the next.
Each of these point-to-point connections comprises one hop in an I2P tunnel.
Higher-layer I2P protocols run over these point-to-point connections
to deliver garlic messages end-to-end between I2P's destinations.

Designing a UDP transport presents unique and complex challenges not present in TCP protocols.
A UDP protocol must handle security issues caused by address spoofing,
and must implement its own congestion control.
Additionally, all messages must be fragmented to fit within the maximum packet size (MTU)
of the network path, and reassembled by the receiver.

We first relied heavily on our previous experience with our NTCP2, SSU, and streaming protocols.
Then, we carefully reviewed and borrowed heavily from two recently-developed UDP protocols:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

Protocol classification and blocking by adversarial on-path attackers such
as nation-state firewalls is not an explicit part of the threat model for those protocols.
However, it is an important part of I2P's threat model, as our mission is to
provide an anonymous and censorship-resistant communications system to at-risk users around the world.
Therefore, much of our design work involved combining the lessons learned from
NTCP2 and SSU with the features and security supported by QUIC and WireGuard.

## Performance

The I2P network is a complex mix of diverse routers.
There are two primary implementations running all over the world on
hardware ranging from high-performance data center computers to
Raspberry Pis and Android phones.
Routers use both TCP and UDP transports.
While the SSU2 improvements are significant, we do not expect them
to be apparent to the user, either locally or in end-to-end transfer speeds.

Here are some highlights of the estimated improvements for SSU2 vs. SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Transition Plan

I2P strives to maintain backward compatibility, both to ensure network stability,
and to allow older routers to continue to be useful and secure.
However, there are limits, because compatibility increases code complexity
and maintenance requirements.

The Java I2P and i2pd projects will both enable SSU2 by default in their next releases (2.0.0 and 2.44.0) in late November 2022.
However, they have different plans for disabling SSU.
I2pd will disable SSU immediately, because SSU2 is a vast improvement over their SSU implementation.
Java I2P plans to disable SSU in mid-2023, to support a gradual transition
and give older routers time to upgrade.

## Summary

The founders of I2P had to make several choices for cryptographic algorithms and protocols.
Some of those choices were better than others, but twenty years later, most are showing their age.
Of course, we knew this was coming, and we've spent the last decade planning and implementing cryptographic upgrades.

SSU2 was the last and most complex protocol to develop in our long upgrade path.
UDP has a very challenging set of assumptions and threat model.
We first designed and rolled out three other flavors of Noise protocols,
and gained experience and deeper understanding of the security and protocol design issues.

Expect SSU2 to be enabled in the i2pd and Java I2P releases scheduled for late November 2022.
If the update goes well, nobody will notice anything different at all.
The performance benefits, while significant, will probably not be measurable for most people.

As usual, we recommend that you update to the new release when it's available.
The best way to maintain security and help the network is to run the latest release.
