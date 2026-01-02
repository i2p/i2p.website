---
title: "Streaming Protocol"
description: "Reliable, TCP-like transport used by most I2P applications"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Overview

The I2P Streaming Library provides reliable, in-order, and authenticated data delivery on top of I2P's unreliable message layer — analogous to TCP over IP. It is used by nearly all interactive I2P applications such as web browsing, IRC, email, and file sharing.

It ensures reliable transmission, congestion control, retransmission, and flow control across I2P’s high-latency anonymous tunnels. Each stream is fully encrypted end-to-end between destinations.

---

## Core Design Principles

The streaming library implements a **one-phase connection setup**, where SYN, ACK, and FIN flags may carry data payloads in the same message. This minimizes round-trips in high-latency environments — a small HTTP transaction can complete in a single round-trip.

Congestion control and retransmission are modeled after TCP but adapted for I2P's environment. Window sizes are message-based, not byte-based, and tuned for tunnel latency and overhead. The protocol supports slow start, congestion avoidance, and exponential backoff similar to TCP's AIMD algorithm.

---

## Architecture

The streaming library operates between applications and the I2CP interface.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>

Most users access it via I2PSocketManager, I2PTunnel, or SAMv3. The library transparently handles destination management, tunnel usage, and retransmissions.

---

## Packet Format

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```

### Header Details

- **Stream IDs**: 32-bit values uniquely identifying local and remote streams.
- **Sequence Number**: Starts at 0 for SYN, increments per message.
- **Ack Through**: Acknowledges all messages up to N, excluding those in the NACK list.
- **Flags**: Bitmask controlling state and behavior.
- **Options**: Variable-length list for RTT, MTU, and protocol negotiation.

### Key Flags

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>

---

## Flow Control and Reliability

Streaming uses **message-based windowing**, unlike TCP's byte-based approach. The number of unacknowledged packets allowed in flight equals the current window size (default 128).

### Mechanisms

- **Congestion control:** Slow start and AIMD-based avoidance.  
- **Choke/Unchoke:** Flow control signaling based on buffer occupancy.  
- **Retransmission:** RFC 6298-based RTO calculation with exponential backoff.  
- **Duplicate filtering:** Ensures reliability over potentially reordered messages.

Typical configuration values:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>

---

## Connection Establishment

1. **Initiator** sends a SYN (optionally with payload and FROM_INCLUDED).  
2. **Responder** replies with SYN+ACK (may include payload).  
3. **Initiator** sends final ACK confirming establishment.

Optional initial payloads allow data transmission before full handshake completion.

---

## Implementation Details

### Retransmission and Timeout

The retransmission algorithm follows **RFC 6298**.  
- **Initial RTO:** 9s  
- **Min RTO:** 100ms  
- **Max RTO:** 45s  
- **Alpha:** 0.125  
- **Beta:** 0.25  

### Control Block Sharing

Recent connections to the same peer reuse previous RTT and window data for faster ramp-up, avoiding “cold start” latency. Control blocks expire after several minutes.

### MTU and Fragmentation

- Default MTU: **1730 bytes** (fits two I2NP messages).  
- ECIES destinations: **1812 bytes** (reduced overhead).  
- Minimum supported MTU: 512 bytes.  

Payload size excludes the 22-byte minimum streaming header.

---

## Version History

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>

---

## Application-Level Usage

### Java Example

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```

### SAMv3 and i2pd Support

- **SAMv3**: Provides STREAM and DATAGRAM modes for non-Java clients.  
- **i2pd**: Exposes identical streaming parameters via configuration file options (e.g. `i2p.streaming.maxWindowSize`, `profile`, etc).

---

## Choosing Between Streaming and Datagrams

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>

---

## Security and Post-Quantum Future

Streaming sessions are end-to-end encrypted at the I2CP layer.  
Post-quantum hybrid encryption (ML-KEM + X25519) is supported experimentally in 2.10.0 but disabled by default.

---

## References

- [Streaming API Overview](/docs/specs/streaming/)  
- [Streaming Protocol Specification](/docs/specs/streaming/)  
- [I2CP Specification](/docs/specs/i2cp/)  
- [Proposal 144: Streaming MTU Calculations](/proposals/144-ecies-x25519-aead-ratchet/)  
- [I2P 2.10.0 Release Notes](/en/blog/2025/09/08/i2p-2.10.0-release/)
