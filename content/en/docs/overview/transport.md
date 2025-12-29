---
title: "Transport Layer"
description: "Understanding I2P's transport layer - point-to-point communication methods between routers including NTCP2 and SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Overview

A **transport** in I2P is a method for direct, point-to-point communication between routers. These mechanisms ensure confidentiality and integrity while verifying router authentication.

Each transport operates using connection paradigms featuring authentication, flow control, acknowledgments, and retransmission capabilities.

---

## 2. Current Transports

I2P currently supports two primary transports:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>

### 2.1 Legacy Transports (Deprecated)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>

---

## 3. Transport Services

The transport subsystem provides the following services:

### 3.1 Message Delivery

- Dependable [I2NP](/docs/specs/i2np/) message delivery (transports handle I2NP messaging exclusively)
- In-order delivery is **NOT guaranteed** universally
- Priority-based message queuing

### 3.2 Connection Management

- Connection establishment and closure
- Connection limit management with threshold enforcement
- Per-peer status tracking
- Automated and manual peer ban list enforcement

### 3.3 Network Configuration

- Multiple router addresses per transport (IPv4 and IPv6 support since v0.9.8)
- UPnP firewall port opening
- NAT/Firewall traversal support
- Local IP detection via multiple methods

### 3.4 Security

- Encryption for point-to-point exchanges
- IP address validation per local rules
- Clock consensus determination (NTP backup)

### 3.5 Bandwidth Management

- Inbound and outbound bandwidth limits
- Optimal transport selection for outgoing messages

---

## 4. Transport Addresses

The subsystem maintains router contact points listing:

- Transport method (NTCP2, SSU2)
- IP address
- Port number
- Optional parameters

Multiple addresses per transport method are possible.

### 4.1 Common Address Configurations

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>

---

## 5. Transport Selection

The system selects transports for [I2NP messages](/docs/specs/i2np/) independently of upper-layer protocols. Selection employs a **bidding system** where each transport submits bids, with the lowest value winning.

### 5.1 Bid Determination Factors

- Transport preference settings
- Existing peer connections
- Current versus threshold connection counts
- Recent connection attempt history
- Message size constraints
- Peer RouterInfo transport capabilities
- Connection directness (direct versus introducer-dependent)
- Peer advertised transport preferences

Generally, two routers maintain single-transport connections simultaneously, though simultaneous multi-transport connections are possible.

---

## 6. NTCP2

**NTCP2** (New Transport Protocol 2) is the modern TCP-based transport for I2P, introduced in version 0.9.36.

### 6.1 Key Features

- Based on the **Noise Protocol Framework** (Noise_XK pattern)
- Uses **X25519** for key exchange
- Uses **ChaCha20/Poly1305** for authenticated encryption
- Uses **BLAKE2s** for hashing
- Protocol obfuscation to resist DPI (Deep Packet Inspection)
- Optional padding for traffic analysis resistance

### 6.2 Connection Establishment

1. **Session Request** (Alice → Bob): Ephemeral X25519 key + encrypted payload
2. **Session Created** (Bob → Alice): Ephemeral key + encrypted confirmation
3. **Session Confirmed** (Alice → Bob): Final handshake with RouterInfo

All subsequent data is encrypted with session keys derived from the handshake.

See the [NTCP2 Specification](/docs/specs/ntcp2/) for full details.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) is the modern UDP-based transport for I2P, introduced in version 0.9.56.

### 7.1 Key Features

- Based on the **Noise Protocol Framework** (Noise_XK pattern)
- Uses **X25519** for key exchange
- Uses **ChaCha20/Poly1305** for authenticated encryption
- Semireliable delivery with selective acknowledgments
- NAT traversal via hole punching and relay/introduction
- Connection migration support
- Path MTU discovery

### 7.2 Advantages over SSU (Legacy)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>

See the [SSU2 Specification](/docs/specs/ssu2/) for full details.

---

## 8. NAT Traversal

Both transports support NAT traversal to allow firewalled routers to participate in the network.

### 8.1 SSU2 Introduction

When a router cannot receive inbound connections directly:

1. Router publishes **introducer** addresses in its RouterInfo
2. Connecting peer sends an introduction request to the introducer
3. Introducer relays connection information to the firewalled router
4. Firewalled router initiates outbound connection (hole punch)
5. Direct communication established

### 8.2 NTCP2 and Firewalls

NTCP2 requires inbound TCP connectivity. Routers behind NAT can:

- Use UPnP to automatically open ports
- Manually configure port forwarding
- Rely on SSU2 for inbound connections while using NTCP2 for outbound

---

## 9. Protocol Obfuscation

Both modern transports incorporate obfuscation features:

- **Random padding** in handshake messages
- **Encrypted headers** that don't reveal protocol signatures
- **Variable-length messages** to resist traffic analysis
- **No fixed patterns** in connection establishment

> **Note**: Transport-layer obfuscation complements but does not replace the anonymity provided by I2P's tunnel architecture.

---

## 10. Future Development

Planned research and improvements include:

- **Pluggable transports** – Tor-compatible obfuscation plugins
- **QUIC-based transport** – Investigation of QUIC protocol benefits
- **Connection limit optimization** – Research into optimal peer connection limits
- **Enhanced padding strategies** – Improved traffic analysis resistance

---

## 11. References

- [NTCP2 Specification](/docs/specs/ntcp2/) – Noise-based TCP transport
- [SSU2 Specification](/docs/specs/ssu2/) – Secure Semireliable UDP 2
- [I2NP Specification](/docs/specs/i2np/) – I2P Network Protocol messages
- [Common Structures](/docs/specs/common-structures/) – RouterInfo and address structures
- [Historical NTCP Discussion](/docs/ntcp/) – Legacy transport development history
- [Legacy SSU Documentation](/docs/legacy/ssu/) – Original SSU specification (deprecated)
