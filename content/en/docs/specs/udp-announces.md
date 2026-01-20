---
title: "UDP Trackers"
description: "Protocol specification for UDP BitTorrent announces in I2P"
slug: "udp-announces"
category: "Protocols"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Overview

This specification documents the protocol for UDP bittorrent announces in I2P. For the overall specification of bittorrent in I2P, see [BitTorrent over I2P](/docs/applications/bittorrent). For background and additional information on the development of this specification, see [Proposal 160](/proposals/160-udp-trackers).

## Design

This proposal uses repliable datagram2, repliable datagram3, and raw datagrams, as defined in [Datagrams](/docs/specs/datagrams). Datagram2 and Datagram3 are new variants of repliable datagrams, defined in [Proposal 163](/proposals/163-datagram2-datagram3). Datagram2 adds replay resistance and offline signature support. Datagram3 is smaller than the old datagram format, but without authentication.

### BEP 15

For reference, the message flow defined in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) is as follows:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```

The connect phase is required to prevent IP address spoofing. The tracker returns a connection ID that the client uses in subsequent announces. This connection ID expires by default in one minute at the client, and in two minutes at the tracker.

I2P will use the same message flow as BEP 15, for ease of adoption in existing UDP-capable client code bases: for efficiency, and for security reasons discussed below:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```

This potentially provides a large bandwidth savings over streaming (TCP) announces. While the Datagram2 is about the same size as a streaming SYN, the raw response is much smaller than the streaming SYN ACK. Subsequent requests use Datagram3, and the subsequent responses are raw.

The announce requests are Datagram3 so that the tracker need not maintain a large mapping table of connection IDs to announce destination or hash. Instead, the tracker may generate connection IDs cryptographically from the sender hash, the current timestamp (based on some interval), and a secret value. When an announce request is received, the tracker validates the connection ID, and then uses the Datagram3 sender hash as the send target.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) specifies that the connection ID expires in one minute at the client, and in two minutes at the tracker. It is not configurable. That limits the potential efficiency gains, unless clients batched announces to do all of them within a one-minute window. i2psnark does not currently batch announces; it spreads them out, to avoid bursts of traffic. Power users are reported to be running thousands of torrents at once, and bursting that many announces into one minute is not realistic.

Here, we propose to extend the connect response to add an optional connection lifetime field. The default, if not present, is one minute. Otherwise, the lifetime specified in seconds, shall be used by the client, and the tracker will maintain the connection ID for one minute more.

### Compatibility with BEP 15

This design maintains compatibility with [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) as much as possible to limit changes required in existing clients and trackers.

The only required change is the format of peer info in the announce response. The addition of the lifetime field in the connect response is not required but is strongly recommended for efficiency, as explained above.

### Security Analysis

An important goal of a UDP announce protocol is to prevent address spoofing. The client must actually exist and bundle a real leaseset. It must have inbound tunnels to receive the Connect Response. These tunnels could be zero-hop and built instantly, but that would expose the creator. This protocol accomplishes that goal.

### Issues

- This protocol does not support blinded destinations, but may be extended to do so. See below.

## Specification

### Protocols and Ports

Repliable Datagram2 uses I2CP protocol 19; repliable Datagram3 uses I2CP protocol 20; raw datagrams use I2CP protocol 18. Requests may be Datagram2 or Datagram3. Responses are always raw. The older repliable datagram ("Datagram1") format using I2CP protocol 17 must NOT be used for requests or replies; these must be dropped if received on the request/reply ports. Note that Datagram1 protocol 17 is still used for the DHT protocol.

Requests use the I2CP "to port" from the announce URL; see below. The request "from port" is chosen by the client, but should be nonzero, and a different port from those used by DHT, so that responses may be easily classified. Trackers should reject requests received on the wrong port.

Responses use the I2CP "to port" from the request. The request "from port" is the "to port" from the request.

### Announce URL

The announce URL format is not specified in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), but as in clearnet, UDP announce URLs are of the form `udp://host:port/path`. The path is ignored and may be empty, but is typically `/announce` on clearnet. The `:port` part should always be present, however, if the `:port` part is omitted, use a default I2CP port of 6969, as that is the common port on clearnet. There may also be cgi parameters `&a=b&c=d` appended, those may be processed and provided in the announce request, see [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). If there are no parameters or path, the trailing `/` may also be omitted, as implied in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Datagram Formats

All values are sent in network byte order (big endian). Do not expect packets to be exactly of a certain size. Future extensions could increase the size of packets.

#### Connect Request

Client to tracker. 16 bytes. Must be repliable Datagram2. Same as in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). No changes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Offset</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">protocol_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0x41727101980 // magic constant</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">action</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 // connect</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">transaction_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
  </tbody>
</table>

#### Connect Response

Tracker to client. 16 or 18 bytes. Must be raw. Same as in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) except as noted below.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Offset</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">action</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 // connect</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">transaction_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifetime</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">optional // Change from BEP 15</td>
    </tr>
  </tbody>
</table>

The response MUST be sent to the I2CP "to port" that was received as the request "from port".

The lifetime field is optional and indicates the connection_id client lifetime in seconds. The default is 60, and the minimum if specified is 60. The maximum is 65535 or about 18 hours. The tracker should maintain the connection_id for 60 seconds more than the client lifetime.

#### Announce Request

Client to tracker. 98 bytes minimum. Must be repliable Datagram3. Same as in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) except as noted below.

The connection_id is as received in the connect response.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Offset</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">action</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 // announce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">transaction_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-byte string</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">info_hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-byte string</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">peer_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">56</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">downloaded</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">left</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">uploaded</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">event</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 // 0: none; 1: completed; 2: started; 3: stopped</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">84</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP address</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 // default, unused in I2P</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">88</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">92</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">num_want</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1 // default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">// must be same as I2CP from port</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">98</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">options</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">optional // As specified in BEP 41</td>
    </tr>
  </tbody>
</table>

Changes from [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key is ignored
- IP address is unused
- port is probably ignored but must be same as I2CP from port
- The options section, if present, is as defined in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

The response MUST be sent to the I2CP "to port" that was received as the request "from port". Do not use the port from the announce request.

#### Announce Response

Tracker to client. 20 bytes minimum. Must be raw. Same as in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) except as noted below.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Offset</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">action</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 // announce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">transaction_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">interval</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">leechers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">seeders</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 * n 32-byte hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">binary hashes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">// Change from BEP 15</td>
    </tr>
  </tbody>
</table>

Changes from [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Instead of 6-byte IPv4+port or 18-byte IPv6+port, we return a multiple of 32-byte "compact responses" with the SHA-256 binary peer hashes. As with TCP compact responses, we do not include a port.

The response MUST be sent to the I2CP "to port" that was received as the request "from port". Do not use the port from the announce request.

I2P datagrams have a very large maximum size of about 64 KB; however, for reliable delivery, datagrams larger than 4 KB should be avoided. For bandwidth efficiency, trackers should probably limit the maximum peers to about 50, which corresponds to about a 1600 byte packet before overhead at various layers, and should be within a two-tunnel-message payload limit after fragmentation.

As in BEP 15, there is no count included of the number of peer addresses (IP/port for BEP 15, hashes here) to follow. While not contemplated in BEP 15, an end-of-peers marker of all zeros could be defined to indicate that the peer info is complete and some extension data follows.

So that extension is possible in the future, clients should ignore a 32-byte all-zeros hash, and any data that follows. Trackers should reject announces from an all-zeros hash, although that hash is already banned by Java routers.

#### Scrape

Scrape request/response from [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) is not required by this specification, but may be implemented if desired, no changes required. The client must acquire a connection ID first. The scrape request is always repliable Datagram3. The scrape response is always raw.

#### Error Response

Tracker to client. 8 bytes minimum (if the message is empty). Must be raw. Same as in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). No changes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Offset</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">action</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3 // error</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32-bit integer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">transaction_id</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">string</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
  </tbody>
</table>

## Extensions

Extension bits or a version field are not included. Clients and trackers should not assume packets to be of a certain size. This way, additional fields can be added without breaking compatibility. The extensions format defined in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) is recommended if required.

The connect response is modified to add an optional connection ID lifetime.

If blinded destination support is required, we can either add the blinded 35-byte address to the end of the announce request, or request blinded hashes in the responses, using the [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) format (parameters TBD). The set of blinded 35-byte peer addresses could be added to the end of the announce reply, after an all-zeros 32-byte hash.

## Implementation Guidelines

See the design section above for a discussion of the challenges for non-integrated, non-I2CP clients and trackers.

### Clients

For a given tracker hostname, a client should prefer UDP over HTTP URLs, and should not announce to both.

Clients with existing BEP 15 support should require only small modifications.

If a client supports DHT or other datagram protocols, it should probably select a different port as the request "from port" so that the replies come back to that port and are not mixed up with DHT messages. The client only receives raw datagrams as replies. Trackers will never send a repliable datagram2 to the client.

Clients with a default list of opentrackers should update the list to add UDP URLs after the known opentrackers are known to support UDP.

Clients may or may not implement retransmission of requests. Retransmissions, if implemented, should use an initial timeout of at least 15 seconds, and double the timeout for each retransmission (exponential backoff).

Clients must back off after receiving an error response.

### Trackers

Trackers with existing BEP 15 support should require only small modifications. This specification differs from the 2014 proposal, in that the tracker must support reception of repliable datagram2 and datagram3 on the same port.

To minimize tracker resource requirements, this protocol is designed to eliminate any requirement that the tracker store mappings of client hashes to connection IDs for later validation. This is possible because the announce request packet is a repliable Datagram3 packet, so it contains the sender's hash.

A recommended implementation is:

- Define the current epoch as the current time with a resolution of the connection lifetime, `epoch = now / lifetime`.
- Define a cryptographic hash function `H(secret, clienthash, epoch)` which generates an 8 byte output.
- Generate the random constant secret used for all connections.
- For connect responses, generate `connection_id = H(secret, clienthash, epoch)`
- For announce requests, validate the received connection ID in the current epoch by verifying `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## References

- **[BEP15]** [BEP 15 - UDP Tracker Protocol](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]** [BEP 41 - UDP Tracker Protocol Extensions](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]** [Datagrams Specification](/docs/specs/datagrams)
- **[Prop160]** [Proposal 160 - UDP Trackers](/proposals/160-udp-trackers)
- **[Prop163]** [Proposal 163 - Datagram2/Datagram3](/proposals/163-datagram2-datagram3)
- **[SAMv3]** [SAM v3 API](/docs/api/samv3)
- **[SPEC]** [BitTorrent over I2P](/docs/applications/bittorrent)
