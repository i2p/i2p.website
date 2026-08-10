---
title: "Fast Extension (BEP 6) Allowed Fast with Destination-Hash Peer Identity"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Draft"
toc: true
---


## Overview

BEP 6 (Fast Extension) packages five features: **Have All / Have None**, **Reject
Requests**, **Suggestions**, and **Allowed Fast**. The wire protocol — negotiation bit,
message IDs, and choke semantics — is transport-agnostic and works as-is over I2P
streaming. The one part of BEP 6 that cannot be mapped directly to I2P is the **Allowed
Fast set generation**, because it is defined in terms of the peer's IPv4 address. I2P
peers have no IPs; they are identified by 32-byte destination hashes.

This proposal standardizes an I2P-native Allowed Fast set generation so that all I2P
torrent clients generate *identical* allowed fast sets for the same peer and torrent,
making the feature useful (and verifiable) across implementations.

## Motivation

New peers need the first few pieces before BitTorrent's tit-for-tat can ramp up. On I2P
the ramp is slower than on clearnet: connection setup and piece delivery cross several
hops of high-latency tunnels, so the window between connect and first reciprocal
unchoke is longer. Allowed Fast directly attacks that window — a starting peer is
allowed a small number of pieces even while choked, gets data immediately, and can
begin reciprocating sooner.

The reference BEP 6 computes the allowed fast set from the peer's IPv4 address to
guarantee that the *sender* can pick pieces unique to the *receiver* (one user with
many IPs can't harvest many sets). On I2P, the peer's destination hash serves the same
binding role and is available to both ends of every connection, which makes the set
deterministic *and locally verifiable* — something the IP-based scheme cannot offer.

## Modifications to BEP 6

The Fast Extension negotiation and all four message types are adopted unchanged:

- Negotiation: third least significant bit of the last reserved byte, `reserved[7] |= 0x04`, both ends
- Have All `<len=0x0001><op=0x0E>`, Have None `<len=0x0001><op=0x0F>`
- Suggest Piece `<len=0x0005><op=0x0D><index>`
- Reject Request `<len=0x000D><op=0x10><index><begin><length>`
- Allowed Fast `<len=0x0005><op=0x11><index>`
- Every request results in exactly one response (piece or reject); choke no longer implicitly rejects pending requests

The single deviation is in the Allowed Fast set generation, replacing the IP bytes with
bytes of the peer's destination hash.

### Deviation: hash bytes instead of masked IP

Reference BEP 6, step (1):

```
x = 0xFFFFFF00 & ip
```

That takes three bytes of the peer's IPv4 address and **zeroes the 4th byte**. This is
a subnet heuristic: users who can obtain multiple IPs on the same /24 should not obtain
multiple allowed fast sets.

Our I2P version replaces this with the first four bytes of the peer's 32-byte
destination hash:

```
x = first 4 bytes of peer destination hash
```

The distinction from the reference implementation:

> "That's 3 bytes of the IP followed by a zero. You're 4 bytes of the hash. It's
> different from BEP 6 because there's no IP and it's not zeroing the 4th byte."

Both ends of an I2P connection already know the peer's destination hash (it is the
address the connection was made to/from), so this requires no extra exchange, no NAT
discovery, and no external IP detection — none of which exist on I2P.

### Allowed Fast generation algorithm

Let `hash` be the 32-byte destination hash of the receiving peer, `infohash` the
torrent's 20-byte infohash, `sz` the number of pieces in the torrent, `k` the final
number of pieces in the allowed fast set (10, as in BEP 6), and `a` the output set:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```

Notes:

- 4 bytes of the destination hash replace the 3 masked IP bytes. All four bytes carry
  hash entropy; none is zeroed.
- As in BEP 6, the SHA1 chain produces a long pseudorandom sequence, partitioned into
  piece indices; `k = 10` matches the reference default.
- The Allowed Fast message is advisory: the receiver MUST NOT interpret it as meaning
  the sender has the piece — only that the sender will serve that piece while choked.

## Benefits

| Area             | Benefit                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Start-up latency | New peers pull the first pieces while choked, shortening the tit-for-tat ramp that is slower over multi-hop I2P tunnels                                                                       |
| Determinism      | The set is a pure function of destination hash + infohash, so any implementation computes the same set — unlike IP-based BEP 6, where the sender's view of the receiver's IP may differ (NAT) |
| Verifiability    | The receiving peer knows its own destination hash and can locally recompute and validate the set, detecting misbehaving senders                                                               |
| No IP machinery  | No NAT traversal, external-IP discovery, or subnet heuristics — all of which are impossible or meaningless on I2P                                                                             |
| Identity binding | One allowed fast set per destination. A user with many destinations gets one set each — the same anti-gaming property the IP mask provided on clearnet                                        |
| Privacy          | No IP address is ever transmitted or implied in the computation                                                                                                                               |
| Bandwidth        | Have All / Have None replaces the full bitfield on large torrents; Reject removes redundant re-requests                                                                                       |

## Implementation considerations

- **Peer identity**: the peer's destination hash is obtained from the streaming
  connection (the session's destination), and is the same value both ends use. For
  outbound connections use the destination you connected to; for inbound use the
  destination the connection came from.
- **Negotiation**: send `reserved[7] |= 0x04` in the handshake; only send Fast
  Extension messages if the peer's handshake also set the bit; if a peer sends Fast
  Extension messages without negotiation, close the connection.
- **Have All / Have None**: send exactly one of bitfield / Have All / Have None
  immediately after the handshake. Have All for seeds, Have None until the first piece.
- **Allowed Fast send side**: only advertise pieces you actually have; the receiver
  may request them while choked. Cap the *served* set (e.g., reject allowed-fast
  requests from a peer that already holds more than `k` pieces, per BEP 6 guidance).
- **Allowed Fast receive side**: store the set; allow requests for those pieces while
  choked; optionally verify the set by recomputing it from your own destination hash
  and the infohash, and ignore pieces not in the computed set.
- **Reject**: every request MUST get exactly one response; on choke, reject
  everything not in the allowed fast set rather than silently silencing the peer.
- **Set size**: use `k = 10` for compatibility; peers are free to choose a lower `k`
  under load, but both ends should advertise only what they will serve.
- **Piece bound**: `index = y % sz` must use the torrent's total piece count `sz`;
  ignore indices >= sz (defensive), since a hash chain is not clamped per piece range.
- **Backward compatibility**: clients that do not negotiate the fast bit simply never
  see these messages; no other protocol changes are required.

## Reference implementations

The algorithm is small and self-contained — a few dozen lines in any language. All
three examples below compute the identical set for identical inputs
(`hash[0:4] ++ infohash`, SHA1 chain, `y % sz`, cap `k = 10`).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```

### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```

### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```

## Compatibility

- **Wire compatible**: negotiation bit and message formats are byte-identical to
  clearnet BEP 6; only the set-generation input differs.
- **Not interoperable across networks**: an I2P client and a clearnet client cannot
  connect to each other anyway; the deviation affects only the peer-identity bytes,
  never the wire format.
- **Within I2P**: any client implementing this proposal computes identical allowed
  fast sets and can serve and verify them interchangeably. Clients that ignore
  Allowed Fast simply treat it as a no-op advisory and lose only the start-up
  benefit.

## Open questions

1. Should the set size `k` remain fixed at 10, or be load-adaptive (e.g., fewer under
   heavy request load) as BEP 6 permits?
2. Should receivers verify the set against their own destination hash and drop
   mismatched indices (defense against buggy or malicious senders)? Recommended yes.
3. Pick the 4-byte *prefix* (bytes 0-3) as shown, or the *last* 4 bytes — any fixed
   4-byte window yields the same properties; prefix keeps the reference code's byte
   order natural (`hash[0:4]`).

## Prior art

- Reference: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- I2PSnark reference implementation: `PeerState.sendAllowedFast()` /
  `generateAllowedFastSet()` in
  `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@since 0.9.71+)
- Works in conjunction with BEP 40 (canonical peer priority) and BEP 21 (partial
  seeds), both supported by I2PSnark
