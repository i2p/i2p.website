---
title: "SSU (legacy)"
description: "Original Secure Semireliable UDP transport"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Deprecated:** SSU was superseded by SSU2. Support was removed from i2pd 2.44.0 (API 0.9.56, Nov 2022) and from Java I2P 2.4.0 (API 0.9.61, Dec 2023).

SSU provided UDP-based, semi-reliable delivery with congestion control, NAT traversal, and introducer support. It complemented NTCP by handling routers behind NAT/firewalls and by coordinating IP discovery.

## Address Elements

- `transport`: `SSU`
- `caps`: capability flags (`B`, `C`, `4`, `6`, etc.)
- `host` / `port`: IPv4 or IPv6 listener (optional when firewalled)
- `key`: Base64 introduction key
- `mtu`: Optional; default 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: introducer entries when the router is firewalled

## Features

- Cooperative NAT traversal using introducers
- Local IP detection via peer tests and inspection of inbound packets
- Automatically relayed firewall status to other transports and the router console
- Semireliable delivery: messages retransmitted up to a limit, then dropped
- Congestion control with additive increase / multiplicative decrease and fragment ACK bitfields

SSU also handled metadata tasks such as timing beacons and MTU negotiation. All functionality is now provided (with modern cryptography) by [SSU2](/docs/specs/ssu2/).
