---
title: "I2P Network Protocol (I2NP)"
description: "Router-to-router message formats, priorities, and size limits inside I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---
## Overview

The I2P Network Protocol (I2NP) defines how routers exchange messages, select transports, and mix traffic while preserving anonymity. It operates between **I2CP** (client API) and the transport protocols (**NTCP2** and **SSU2**).

I2NP is the layer above the I2P transport protocols. It is a router-to-router protocol used for:
- Network database lookups and replies
- Creating tunnels
- Encrypted router and client data messages

I2NP messages may be sent point-to-point to another router, or sent anonymously through tunnels to that router.

Routers queue outbound work using local priorities. Higher priority numbers are processed first. Anything above the standard tunnel data priority (400) is treated as urgent.

### Current Transports

I2P now uses **NTCP2** (TCP) and **SSU2** (UDP) for both IPv4 and IPv6. Both transports employ:
- **X25519** key exchange (Noise protocol framework)
- **ChaCha20/Poly1305** authenticated encryption (AEAD)
- **SHA-256** hashing

**Legacy transports removed:**
- NTCP (original TCP) was removed from the Java router in release 0.9.50 (May 2021)
- SSU v1 (original UDP) was removed from the Java router in release 2.4.0 (December 2023)
- SSU v1 was removed from i2pd in release 2.44.0 (November 2022)

As of 2025, the network has fully transitioned to Noise-based transports with zero legacy transport support.

---

## Version Numbering System

**IMPORTANT:** I2P uses a dual versioning system that must be clearly understood:

### Release Versions (User-Facing)

These are the versions users see and download:
- 0.9.50 (May 2021) - Last 0.9.x release
- **1.5.0** (August 2021) - First 1.x release
- 1.6.0, 1.7.0, 1.8.0, 1.9.0 (through 2021-2022)
- **2.0.0** (November 2022) - First 2.x release
- 2.1.0 through 2.9.0 (through 2023-2025)
- **2.10.0** (September 8, 2025) - Current release

### API Versions (Protocol Compatibility)

These are internal version numbers published in the "router.version" field in RouterInfo properties:
- 0.9.50 (May 2021)
- **0.9.51** (August 2021) - API version for release 1.5.0
- 0.9.52 through 0.9.66 (continuing through 2.x releases)
- **0.9.67** (September 2025) - API version for release 2.10.0

**Key Point:** There were NO releases numbered 0.9.51 through 0.9.67. These numbers exist only as API version identifiers. I2P jumped from release 0.9.50 directly to 1.5.0.

### Version Mapping Table

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>

**Upcoming:** Release 2.11.0 (planned December 2025) will require Java 17+ and enable post-quantum cryptography by default.

---

## Protocol Versions

All routers must publish their I2NP protocol version in the "router.version" field in the RouterInfo properties. This version field is the API version, indicating the level of support for various I2NP protocol features, and is not necessarily the actual router version.

If alternative (non-Java) routers wish to publish any version information about the actual router implementation, they must do so in another property. Versions other than those listed below are allowed. Support will be determined through a numeric comparison; for example, 0.9.13 implies support for 0.9.12 features.

**Note:** The "coreVersion" property is no longer published in the router info and was never used for determination of the I2NP protocol version.

### API Version Feature Summary

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>

**Note:** There are also transport-related features and compatibility issues. See the NTCP2 and SSU2 transport documentation for details.

---

## Message Header

I2NP uses a logical 16-byte header structure, while modern transports (NTCP2 and SSU2) use a shortened 9-byte header omitting redundant size and checksum fields. The fields remain conceptually identical.

### Header Format Comparison

**Standard Format (16 bytes):**

Used in legacy NTCP transport and when I2NP messages are embedded within other messages (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```

**Short Format for SSU (Obsolete, 5 bytes):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```

**Short Format for NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves (9 bytes):**

Used in modern transports and ECIES encrypted garlic messages.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```

### Header Field Details

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>

### Implementation Notes

- When transmitted over SSU (obsolete), only type and 4-byte expiration were included
- When transmitted over NTCP2 or SSU2, the 9-byte short format is used
- The standard 16-byte header is required for I2NP messages contained in other messages (Data, TunnelData, TunnelGateway, GarlicClove)
- As of release 0.8.12, checksum verification is disabled at some points in the protocol stack for efficiency, but checksum generation is still required for compatibility
- The short expiration is unsigned and will wrap around on February 7, 2106. After that date, an offset must be added to get the correct time
- For compatibility with older versions, always generate checksums even though they may not be verified

---

## Size Constraints

Tunnel messages fragment I2NP payloads into fixed-size pieces:
- **First fragment:** approximately 956 bytes
- **Subsequent fragments:** approximately 996 bytes each
- **Maximum fragments:** 64 (numbered 0-63)
- **Maximum payload:** approximately 61,200 bytes (61.2 KB)

**Calculation:** 956 + (63 × 996) = 63,704 bytes theoretical maximum, with practical limit around 61,200 bytes due to overhead.

### Historical Context

Old transports had stricter frame size limits:
- NTCP: 16 KB frames
- SSU: approximately 32 KB frames

NTCP2 supports approximately 65 KB frames, but the tunnel fragmentation limit still applies.

### Application Data Considerations

Garlic messages may bundle LeaseSets, Session Tags, or encrypted LeaseSet2 variants, reducing space for payload data.

**Recommendation:** Datagrams should stay ≤ 10 KB to ensure reliable delivery. Messages approaching the 61 KB limit may experience:
- Increased latency due to fragmentation reassembly
- Higher probability of delivery failure
- Greater exposure to traffic analysis

### Fragmentation Technical Details

Each tunnel message is exactly 1,024 bytes (1 KB) and contains:
- 4-byte tunnel ID
- 16-byte initialization vector (IV)
- 1,004 bytes of encrypted data

Within the encrypted data, tunnel messages carry fragmented I2NP messages with fragment headers indicating:
- Fragment number (0-63)
- Whether this is the first or follow-on fragment
- Total message ID for reassembly

The first fragment includes the full I2NP message header (16 bytes), leaving approximately 956 bytes for payload. Follow-on fragments do not include the message header, allowing approximately 996 bytes of payload per fragment.

---

## Common Message Types

Routers use the message type and priority to schedule outbound work. Higher priority values are processed first. The values below match current Java I2P defaults (as of API version 0.9.67).

**Note:** Priorities are implementation-dependent. For authoritative priority values, consult `OutNetMessage` class documentation in the Java I2P source code.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>

**Reserved message types:**
- Type 0: Reserved
- Types 4-9: Reserved for future use
- Types 12-17: Reserved for future use
- Types 224-254: Reserved for experimental messages
- Type 255: Reserved for future expansion

### Message Type Notes

- Control-plane messages (DatabaseLookup, TunnelBuild, etc.) typically travel through **exploratory tunnels**, not client tunnels, allowing independent prioritization
- Priority values are approximate and may vary by implementation
- TunnelBuild (21) and TunnelBuildReply (22) are deprecated but still implemented for compatibility with very long tunnels (>8 hops)
- The standard tunnel data priority is 400; anything above this is treated as urgent
- Typical tunnel length in today's network is 3-4 hops, so most tunnel builds use ShortTunnelBuild (218-byte records) or VariableTunnelBuild (528-byte records)

---

## Encryption and Message Wrapping

Routers frequently encapsulate I2NP messages before transmission, creating multiple encryption layers. A DeliveryStatus message may be:
1. Wrapped in a GarlicMessage (encrypted)
2. Inside a DataMessage
3. Within a TunnelData message (encrypted again)

Each hop only decrypts its layer; the final destination reveals the innermost payload.

### Encryption Algorithms

**Legacy (Being Phased Out):**
- ElGamal/AES + SessionTags
- ElGamal-2048 for asymmetric encryption
- AES-256 for symmetric encryption
- 32-byte session tags

**Current (Standard as of API 0.9.48):**
- ECIES-X25519 + ChaCha20/Poly1305 AEAD with ratcheting forward secrecy
- Noise protocol framework (Noise_IK_25519_ChaChaPoly_SHA256 for destinations)
- 8-byte session tags (reduced from 32 bytes)
- Signal Double Ratchet algorithm for forward secrecy
- Introduced in API version 0.9.46 (2020)
- Mandatory for all routers as of API version 0.9.58 (2023)

**Future (Beta as of 2.10.0):**
- Post-quantum hybrid cryptography using MLKEM (ML-KEM-768) combined with X25519
- Hybrid ratchet combining classical and post-quantum key agreement
- Backward compatible with ECIES-X25519
- Will become default in release 2.11.0 (December 2025)

### ElGamal Router Deprecation

**CRITICAL:** ElGamal routers were deprecated as of API version 0.9.58 (release 2.2.0, March 2023). As the recommended minimum floodfill version to query is now 0.9.58, implementations need not implement encryption for ElGamal floodfill routers.

**However:** ElGamal destinations are still supported for backward compatibility. Clients using ElGamal encryption can still communicate through ECIES routers.

### ECIES-X25519-AEAD-Ratchet Details

This is crypto type 4 in I2P's cryptography specification. It provides:

**Key Features:**
- Forward secrecy through ratcheting (new keys for each message)
- Reduced session tag storage (8 bytes vs. 32 bytes)
- Multiple session types (New Session, Existing Session, One-Time)
- Based on Noise protocol Noise_IK_25519_ChaChaPoly_SHA256
- Integrated with Signal's Double Ratchet algorithm

**Cryptographic Primitives:**
- X25519 for Diffie-Hellman key agreement
- ChaCha20 for stream encryption
- Poly1305 for message authentication (AEAD)
- SHA-256 for hashing
- HKDF for key derivation

**Session Management:**
- New Session: Initial connection using static destination key
- Existing Session: Subsequent messages using session tags
- One-Time Session: Single-message sessions for lower overhead

See [ECIES Specification](/docs/specs/ecies/) and [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/) for complete technical details.

---

## Common Structures

The following structures are elements of multiple I2NP messages. They are not complete messages.

### BuildRequestRecord (ElGamal)

**DEPRECATED.** Only used in the current network when a tunnel contains an ElGamal router. See [ECIES Tunnel Creation](/docs/specs/implementation/) for modern format.

**Purpose:** One record in a set of multiple records to request the creation of one hop in the tunnel.

**Format:**

ElGamal and AES encrypted (528 bytes total):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```

ElGamal encrypted structure (528 bytes):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```

Cleartext structure (222 bytes before encryption):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```

**Notes:**
- The ElGamal-2048 encryption produces a 514-byte block, but the two padding bytes (at positions 0 and 257) are removed, resulting in 512 bytes
- See [Tunnel Creation Specification](/docs/specs/implementation/) for field details
- Source code: `net.i2p.data.i2np.BuildRequestRecord`
- Constant: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 Long)

For ECIES-X25519 routers, introduced in API version 0.9.48. Uses 528 bytes for backward compatibility with mixed tunnels.

**Format:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```

**Total size:** 528 bytes (same as ElGamal for compatibility)

See [ECIES Tunnel Creation](/docs/specs/implementation/) for cleartext structure and encryption details.

### BuildRequestRecord (ECIES-X25519 Short)

For ECIES-X25519 routers only, as of API version 0.9.51 (release 1.5.0). This is the current standard format.

**Format:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```

**Total size:** 218 bytes (59% reduction from 528 bytes)

**Key Difference:** Short records derive ALL keys via HKDF (key derivation function) rather than including them explicitly in the record. This includes:
- Layer keys (for tunnel encryption)
- IV keys (for tunnel encryption)
- Reply keys (for build reply)
- Reply IVs (for build reply)

All keys are derived using the Noise protocol's HKDF mechanism based on the shared secret from the X25519 key exchange.

**Benefits:**
- 4 short records fit in one tunnel message (873 bytes)
- 3 message tunnel builds instead of separate messages for each record
- Reduced bandwidth and latency
- Same security properties as long format

See [Proposal 157](/proposals/157-new-tbm/) for rationale and [ECIES Tunnel Creation](/docs/specs/implementation/) for complete specification.

**Source code:**
- `net.i2p.data.i2np.ShortEncryptedBuildRecord`
- Constant: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal)

**DEPRECATED.** Only used when tunnel contains an ElGamal router.

**Purpose:** One record in a set of multiple records with responses to a build request.

**Format:**

Encrypted (528 bytes, same size as BuildRequestRecord):

```
bytes 0-527 :: AES-encrypted record
```

Unencrypted structure:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```

**Reply Codes:**
- `0` - Accept
- `30` - Reject (bandwidth exceeded)

See [Tunnel Creation Specification](/docs/specs/implementation/) for details on the reply field.

### BuildResponseRecord (ECIES-X25519)

For ECIES-X25519 routers, API version 0.9.48+. Same size as corresponding request (528 for long, 218 for short).

**Format:**

Long format (528 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```

Short format (218 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```

**Cleartext structure (both formats):**

Contains a Mapping structure (I2P's key-value format) with:
- Reply status code (required)
- Bandwidth available parameter ("b") (optional, added in API 0.9.65)
- Other optional parameters for future extensions

**Reply Status Codes:**
- `0` - Success
- `30` - Reject: bandwidth exceeded

See [ECIES Tunnel Creation](/docs/specs/implementation/) for complete specification.

### GarlicClove (ElGamal/AES)

**WARNING:** This is the format used for garlic cloves within ElGamal-encrypted garlic messages. The format for ECIES-AEAD-X25519-Ratchet garlic messages and garlic cloves is significantly different. See [ECIES Specification](/docs/specs/ecies/) for the modern format.

**Deprecated for routers (API 0.9.58+), still supported for destinations.**

**Format:**

Unencrypted:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```

**Notes:**
- Cloves are never fragmented
- When the first bit of the Delivery Instructions flag byte is 0, the clove is not encrypted
- When the first bit is 1, the clove is encrypted (unimplemented feature)
- Maximum length is a function of total clove lengths and maximum GarlicMessage length
- The certificate could possibly be used for HashCash to "pay" for routing (future possibility)
- Messages used in practice: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage
- GarlicMessage can contain GarlicMessage (nested garlic), but this is not used in practice

See [Garlic Routing](/docs/overview/garlic-routing/) for conceptual overview.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

For ECIES-X25519 routers and destinations, API version 0.9.46+. This is the current standard format.

**CRITICAL DIFFERENCE:** ECIES garlic uses a completely different structure based on Noise protocol blocks rather than explicit clove structures.

**Format:**

ECIES garlic messages contain a series of blocks:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```

**Block Types:**
- `0` - Garlic Clove Block (contains an I2NP message)
- `1` - DateTime Block (timestamp)
- `2` - Options Block (delivery options)
- `3` - Padding Block
- `254` - Termination Block (unimplemented)

**Garlic Clove Block (type 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```

**Key Differences from ElGamal format:**
- Uses 4-byte expiration (seconds since epoch) instead of 8-byte Date
- No certificate field
- Wrapped in block structure with type and length
- Entire message encrypted with ChaCha20/Poly1305 AEAD
- Session management via ratcheting

See [ECIES Specification](/docs/specs/ecies/) for complete details on the Noise protocol framework and block structures.

### Garlic Clove Delivery Instructions

This format is used for both ElGamal and ECIES garlic cloves. It specifies how to deliver the enclosed message.

**CRITICAL WARNING:** This specification is for Delivery Instructions inside Garlic Cloves ONLY. "Delivery Instructions" are also used inside Tunnel Messages, where the format is significantly different. See the [Tunnel Message Specification](/docs/specs/implementation/) for tunnel delivery instructions. DO NOT confuse these two formats.

**Format:**

Session key and delay are unused and never present, so the three possible lengths are:
- 1 byte (LOCAL)
- 33 bytes (ROUTER and DESTINATION)
- 37 bytes (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```

**Typical Lengths:**
- LOCAL delivery: 1 byte (flag only)
- ROUTER / DESTINATION delivery: 33 bytes (flag + hash)
- TUNNEL delivery: 37 bytes (flag + hash + tunnel ID)

**Delivery Type Descriptions:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>

**Implementation Notes:**
- Session key encryption is unimplemented and the flag bit is always 0
- Delay is not fully implemented and the flag bit is always 0
- For TUNNEL delivery, the hash identifies the gateway router and the tunnel ID specifies which inbound tunnel
- For DESTINATION delivery, the hash is the SHA-256 of the destination's public key
- For ROUTER delivery, the hash is the SHA-256 of the router's identity

---

## I2NP Messages

Complete message specifications for all I2NP message types.

### Message Type Summary

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>

**Reserved:**
- Type 0: Reserved
- Types 4-9: Reserved for future use
- Types 12-17: Reserved for future use
- Types 224-254: Reserved for experimental messages
- Type 255: Reserved for future expansion

---

### DatabaseStore (Type 1)

**Purpose:** An unsolicited database store, or the response to a successful DatabaseLookup message.

**Contents:** An uncompressed LeaseSet, LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet, or a compressed RouterInfo.

**Format with reply token:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```

**Format with reply token == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**Notes:**
- For security, the reply fields are ignored if the message is received down a tunnel
- The key is the "real" hash of the RouterIdentity or Destination, NOT the routing key
- Types 3, 5, and 7 (LeaseSet2 variants) were added in release 0.9.38 (API 0.9.38). See [Proposal 123](/proposals/123-new-netdb-entries/) for details
- These types should only be sent to routers with API version 0.9.38 or higher
- As an optimization to reduce connections, if the type is a LeaseSet, the reply token is included, the reply tunnel ID is nonzero, and the reply gateway/tunnelID pair is found in the LeaseSet as a lease, the recipient may reroute the reply to any other lease in the LeaseSet
- **RouterInfo gzip format:** To hide the router OS and implementation, match the Java router implementation by setting the modification time to 0 and the OS byte to 0xFF, and set XFL to 0x02 (max compression, slowest algorithm) per RFC 1952. First 10 bytes: `1F 8B 08 00 00 00 00 00 02 FF`

**Source code:**
- `net.i2p.data.i2np.DatabaseStoreMessage`
- `net.i2p.data.RouterInfo` (for RouterInfo structure)
- `net.i2p.data.LeaseSet` (for LeaseSet structure)

---

### DatabaseLookup (Type 2)

**Purpose:** A request to look up an item in the network database. The response is either a DatabaseStore or a DatabaseSearchReply.

**Format:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```

**Reply Encryption Modes:**

**NOTE:** ElGamal routers are deprecated as of API 0.9.58. As the recommended minimum floodfill version to query is now 0.9.58, implementations need not implement encryption for ElGamal floodfill routers. ElGamal destinations are still supported.

Flag bit 4 (ECIESFlag) is used in combination with bit 1 (encryptionFlag) to determine the reply encryption mode:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>

**No Encryption (flags 0,0):**

reply_key, tags, and reply_tags are not present.

**ElG to ElG (flags 0,1) - DEPRECATED:**

Supported as of 0.9.7, deprecated as of 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```

**ECIES to ElG (flags 1,0) - DEPRECATED:**

Supported as of 0.9.46, deprecated as of 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```

The reply is an ECIES Existing Session message as defined in [ECIES Specification](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```

**ECIES to ECIES (flags 1,0) - CURRENT STANDARD:**

ECIES destination or router sends a lookup to an ECIES router. Supported as of 0.9.49.

Same format as "ECIES to ElG" above. The lookup message encryption is specified in [ECIES Routers](/docs/specs/ecies/#routers). The requester is anonymous.

**ECIES to ECIES with DH (flags 1,1) - FUTURE:**

Not yet fully defined. See [Proposal 156](/proposals/156-ecies-routers/).

**Notes:**
- Prior to 0.9.16, the key could be for a RouterInfo or LeaseSet (same key space, no flag to distinguish)
- Encrypted replies are only useful when the response is through a tunnel
- The number of included tags could be greater than one if alternative DHT lookup strategies are implemented
- The lookup key and exclude keys are the "real" hashes, NOT routing keys
- Types 3, 5, and 7 (LeaseSet2 variants) may be returned as of 0.9.38. See [Proposal 123](/proposals/123-new-netdb-entries/)
- **Exploratory lookup notes:** An exploratory lookup is defined to return a list of non-floodfill hashes close to the key. However, implementations vary: Java does look up the search key for an RI and returns a DatabaseStore if present; i2pd does not. Therefore, it is not recommended to use an exploratory lookup for previously-received hashes

**Source code:**
- `net.i2p.data.i2np.DatabaseLookupMessage`
- Encryption: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Type 3)

**Purpose:** The response to a failed DatabaseLookup message.

**Contents:** A list of router hashes closest to the requested key.

**Format:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```

**Notes:**
- The 'from' hash is unauthenticated and cannot be trusted
- The returned peer hashes are not necessarily closer to the key than the router being queried. For replies to regular lookups, this facilitates discovery of new floodfills and "backwards" searching (further-from-the-key) for robustness
- For exploration lookups, the key is usually generated randomly. The response's non-floodfill peer_hashes may be selected using an optimized algorithm (e.g., close but not necessarily closest peers) to avoid inefficient sorting of the entire local database. Caching strategies may also be used. This is implementation-dependent
- **Typical number of hashes returned:** 3
- **Recommended maximum number of hashes to return:** 16
- The lookup key, peer hashes, and from hash are "real" hashes, NOT routing keys
- If num is 0, this indicates no closer peers were found (dead end)

**Source code:**
- `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (Type 10)

**Purpose:** A simple message acknowledgment. Generally created by the message originator and wrapped in a Garlic Message with the message itself, to be returned by the destination.

**Contents:** The ID of the delivered message and the creation or arrival time.

**Format:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```

**Notes:**
- The time stamp is always set by the creator to the current time. However, there are several uses of this in the code, and more may be added in the future
- This message is also used as a session established confirmation in SSU. In this case, the message ID is set to a random number, and the "arrival time" is set to the current network-wide ID, which is 2 (i.e., `0x0000000000000002`)
- DeliveryStatus is typically wrapped in a GarlicMessage and sent through a tunnel to provide acknowledgment without revealing the sender
- Used for tunnel testing to measure latency and reliability

**Source code:**
- `net.i2p.data.i2np.DeliveryStatusMessage`
- Used in: `net.i2p.router.tunnel.InboundEndpointProcessor` for tunnel testing

---

### GarlicMessage (Type 11)

**WARNING:** This is the format used for ElGamal-encrypted garlic messages. The format for ECIES-AEAD-X25519-Ratchet garlic messages is significantly different. See [ECIES Specification](/docs/specs/ecies/) for the modern format.

**Purpose:** Used to wrap multiple encrypted I2NP messages.

**Contents:** When decrypted, a series of Garlic Cloves and additional data, also known as a Clove Set.

**Encrypted Format:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```

**Decrypted Data (Clove Set):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**Notes:**
- When unencrypted, data contains one or more Garlic Cloves
- The AES encrypted block is padded to a minimum of 128 bytes; with the 32-byte Session Tag, the minimum size of the encrypted message is 160 bytes; with the 4-byte length field, the minimum size of the Garlic Message is 164 bytes
- Actual max length is less than 64 KB (practical limit around 61.2 KB for tunnel messages)
- See [ElGamal/AES Specification](/docs/legacy/elgamal-aes/) for encryption details
- See [Garlic Routing](/docs/overview/garlic-routing/) for conceptual overview
- The 128 byte minimum size of the AES encrypted block is not currently configurable
- The message ID is generally set to a random number on transmit and appears to be ignored on receive
- The certificate could possibly be used for HashCash to "pay" for routing (future possibility)
- **ElGamal encryption structure:** 32-byte session tag + ElGamal-encrypted session key + AES-encrypted payload

**For ECIES-X25519-AEAD-Ratchet format (current standard for routers):**

See [ECIES Specification](/docs/specs/ecies/) and [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Source code:**
- `net.i2p.data.i2np.GarlicMessage`
- Encryption: `net.i2p.crypto.elgamal.ElGamalAESEngine` (deprecated)
- Modern encryption: `net.i2p.crypto.ECIES` packages

---

### TunnelData (Type 18)

**Purpose:** A message sent from a tunnel's gateway or participant to the next participant or endpoint. The data is of fixed length, containing I2NP messages that are fragmented, batched, padded, and encrypted.

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```

**Payload Structure (1024 bytes):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```

**Notes:**
- The I2NP message ID for TunnelData is set to a new random number at each hop
- The tunnel message format (within the encrypted data) is specified in [Tunnel Message Specification](/docs/specs/implementation/)
- Each hop decrypts one layer using AES-256 in CBC mode
- The IV is updated at each hop using the decrypted data
- Total size is exactly 1,028 bytes (4 tunnelId + 1024 data)
- This is the fundamental unit of tunnel traffic
- TunnelData messages carry fragmented I2NP messages (GarlicMessage, DatabaseStore, etc.)

**Source code:**
- `net.i2p.data.i2np.TunnelDataMessage`
- Constant: `TunnelDataMessage.DATA_LENGTH = 1024`
- Processing: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Type 19)

**Purpose:** Wraps another I2NP message to be sent into a tunnel at the tunnel's inbound gateway.

**Format:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```

**Notes:**
- The payload is an I2NP message with a standard 16-byte header
- Used to inject messages into tunnels from the local router
- The gateway fragments the enclosed message if necessary
- After fragmentation, the fragments are wrapped in TunnelData messages
- TunnelGateway is never sent over the network; it's an internal message type used before tunnel processing

**Source code:**
- `net.i2p.data.i2np.TunnelGatewayMessage`
- Processing: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Type 20)

**Purpose:** Used by Garlic Messages and Garlic Cloves to wrap arbitrary data (typically end-to-end encrypted application data).

**Format:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```

**Notes:**
- This message contains no routing information and will never be sent "unwrapped"
- Only used inside Garlic messages
- Typically contains end-to-end encrypted application data (HTTP, IRC, email, etc.)
- The data is usually an ElGamal/AES or ECIES-encrypted payload
- Maximum practical length is around 61.2 KB due to tunnel message fragmentation limits

**Source code:**
- `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Type 21)

**DEPRECATED.** Use VariableTunnelBuild (type 23) or ShortTunnelBuild (type 25).

**Purpose:** Fixed-length tunnel build request for 8 hops.

**Format:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```

**Notes:**
- As of 0.9.48, may contain ECIES-X25519 BuildRequestRecords. See [ECIES Tunnel Creation](/docs/specs/implementation/)
- See [Tunnel Creation Specification](/docs/specs/implementation/) for details
- The I2NP message ID for this message must be set according to the tunnel creation specification
- While rarely seen in today's network (replaced by VariableTunnelBuild), it may still be used for very long tunnels and has not been formally deprecated
- Routers must still implement this for compatibility
- Fixed 8-record format is inflexible and wastes bandwidth for shorter tunnels

**Source code:**
- `net.i2p.data.i2np.TunnelBuildMessage`
- Constant: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Type 22)

**DEPRECATED.** Use VariableTunnelBuildReply (type 24) or OutboundTunnelBuildReply (type 26).

**Purpose:** Fixed-length tunnel build reply for 8 hops.

**Format:**

Same format as TunnelBuildMessage, with BuildResponseRecords instead of BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```

**Notes:**
- As of 0.9.48, may contain ECIES-X25519 BuildResponseRecords. See [ECIES Tunnel Creation](/docs/specs/implementation/)
- See [Tunnel Creation Specification](/docs/specs/implementation/) for details
- The I2NP message ID for this message must be set according to the tunnel creation specification
- While rarely seen in today's network (replaced by VariableTunnelBuildReply), it may still be used for very long tunnels and has not been formally deprecated
- Routers must still implement this for compatibility

**Source code:**
- `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Type 23)

**Purpose:** Variable-length tunnel build for 1-8 hops. Supports both ElGamal and ECIES-X25519 routers.

**Format:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```

**Notes:**
- As of 0.9.48, may contain ECIES-X25519 BuildRequestRecords. See [ECIES Tunnel Creation](/docs/specs/implementation/)
- Introduced in router version 0.7.12 (2009)
- May not be sent to tunnel participants earlier than version 0.7.12
- See [Tunnel Creation Specification](/docs/specs/implementation/) for details
- The I2NP message ID must be set according to the tunnel creation specification
- **Typical number of records:** 4 (for a 4-hop tunnel)
- **Typical total size:** 1 + (4 × 528) = 2,113 bytes
- This is the standard tunnel build message for ElGamal routers
- ECIES routers typically use ShortTunnelBuild (type 25) instead

**Source code:**
- `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Type 24)

**Purpose:** Variable-length tunnel build reply for 1-8 hops. Supports both ElGamal and ECIES-X25519 routers.

**Format:**

Same format as VariableTunnelBuildMessage, with BuildResponseRecords instead of BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```

**Notes:**
- As of 0.9.48, may contain ECIES-X25519 BuildResponseRecords. See [ECIES Tunnel Creation](/docs/specs/implementation/)
- Introduced in router version 0.7.12 (2009)
- May not be sent to tunnel participants earlier than version 0.7.12
- See [Tunnel Creation Specification](/docs/specs/implementation/) for details
- The I2NP message ID must be set according to the tunnel creation specification
- **Typical number of records:** 4
- **Typical total size:** 2,113 bytes

**Source code:**
- `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Type 25)

**Purpose:** Short tunnel build messages for ECIES-X25519 routers only. Introduced in API version 0.9.51 (release 1.5.0, August 2021). This is the current standard for ECIES tunnel builds.

**Format:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```

**Notes:**
- Introduced in router version 0.9.51 (release 1.5.0, August 2021)
- May not be sent to tunnel participants earlier than API version 0.9.51
- See [ECIES Tunnel Creation](/docs/specs/implementation/) for complete specification
- See [Proposal 157](/proposals/157-new-tbm/) for rationale
- **Typical number of records:** 4
- **Typical total size:** 1 + (4 × 218) = 873 bytes
- **Bandwidth savings:** 59% smaller than VariableTunnelBuild (873 vs 2,113 bytes)
- **Performance benefit:** 4 short records fit in one tunnel message; VariableTunnelBuild requires 3 tunnel messages
- This is now the standard tunnel build format for pure ECIES-X25519 tunnels
- Records derive keys via HKDF instead of including them explicitly

**Source code:**
- `net.i2p.data.i2np.ShortTunnelBuildMessage`
- Constant: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Type 26)

**Purpose:** Sent from the outbound endpoint of a new tunnel to the originator. For ECIES-X25519 routers only. Introduced in API version 0.9.51 (release 1.5.0, August 2021).

**Format:**

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords instead of ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```

**Notes:**
- Introduced in router version 0.9.51 (release 1.5.0, August 2021)
- See [ECIES Tunnel Creation](/docs/specs/implementation/) for complete specification
- **Typical number of records:** 4
- **Typical total size:** 873 bytes
- This reply is sent from the outbound endpoint (OBEP) back to the tunnel creator through the newly-created outbound tunnel
- Provides confirmation that all hops accepted the tunnel build

**Source code:**
- `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## References

### Official Specifications

- **[I2NP Specification](/docs/specs/i2np/)** - Complete I2NP message format specification
- **[Common Structures](/docs/specs/common-structures/)** - Data types and structures used throughout I2P
- **[Tunnel Creation](/docs/specs/implementation/)** - ElGamal tunnel creation (deprecated)
- **[ECIES Tunnel Creation](/docs/specs/implementation/)** - ECIES-X25519 tunnel creation (current)
- **[Tunnel Message](/docs/specs/implementation/)** - Tunnel message format and delivery instructions
- **[NTCP2 Specification](/docs/specs/ntcp2/)** - TCP transport protocol
- **[SSU2 Specification](/docs/specs/ssu2/)** - UDP transport protocol
- **[ECIES Specification](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet encryption
- **[Cryptography Specification](/docs/specs/cryptography/)** - Low-level cryptographic primitives
- **[I2CP Specification](/docs/specs/i2cp/)** - Client protocol specification
- **[Datagram Specification](/docs/api/datagrams/)** - Datagram2 and Datagram3 formats

### Proposals

- **[Proposal 123](/proposals/123-new-netdb-entries/)** - New netDB entries (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet encryption
- **[Proposal 154](/proposals/154-ecies-lookups/)** - Encrypted database lookup
- **[Proposal 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[Proposal 157](/proposals/157-new-tbm/)** - Smaller tunnel build messages (short format)
- **[Proposal 159](/proposals/159-ssu2/)** - SSU2 transport
- **[Proposal 161](/en/proposals/161-ri-dest-padding/)** - Compressible padding
- **[Proposal 163](/proposals/163-datagram2/)** - Datagram2 and Datagram3
- **[Proposal 167](/proposals/167-service-records/)** - LeaseSet service record parameters
- **[Proposal 168](/proposals/168-tunnel-bandwidth/)** - Tunnel build bandwidth parameters
- **[Proposal 169](/proposals/169-pq-crypto/)** - Post-quantum hybrid cryptography

### Documentation

- **[Garlic Routing](/docs/overview/garlic-routing/)** - Layered message bundling
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Deprecated encryption scheme
- **[Tunnel Implementation](/docs/specs/implementation/)** - Fragmentation and processing
- **[Network Database](/docs/specs/common-structures/)** - Distributed hash table
- **[NTCP2 Transport](/docs/specs/ntcp2/)** - TCP transport specification
- **[SSU2 Transport](/docs/specs/ssu2/)** - UDP transport specification
- **[Technical Introduction](/docs/overview/tech-intro/)** - I2P architecture overview

### Source Code

- **[Java I2P Repository](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Official Java implementation
- **[GitHub Mirror](https://github.com/i2p/i2p.i2p)** - GitHub mirror of Java I2P
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation

### Key Source Code Locations

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):**
- `core/java/src/net/i2p/data/i2np/` - I2NP message implementations
- `core/java/src/net/i2p/crypto/` - Cryptographic implementations
- `router/java/src/net/i2p/router/tunnel/` - Tunnel processing
- `router/java/src/net/i2p/router/transport/` - Transport implementations

**Constants and Values:**
- `I2NPMessage.MAX_SIZE = 65536` - Maximum I2NP message size
- `I2NPMessageImpl.HEADER_LENGTH = 16` - Standard header size
- `TunnelDataMessage.DATA_LENGTH = 1024` - Tunnel message payload
- `EncryptedBuildRecord.RECORD_SIZE = 528` - Long build record
- `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Short build record
- `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Max records per build

---

## Appendix A: Network Statistics and Current State

### Network Composition (as of October 2025)

- **Total routers:** Approximately 60,000-70,000 (varies)
- **Floodfill routers:** Approximately 500-700 active
- **Encryption types:**
  - ECIES-X25519: >95% of routers
  - ElGamal: <5% of routers (deprecated, legacy only)
- **Transport adoption:**
  - SSU2: >60% primary transport
  - NTCP2: ~40% primary transport
  - Legacy transports (SSU1, NTCP): 0% (removed)
- **Signature types:**
  - EdDSA (Ed25519): Vast majority
  - ECDSA: Small percentage
  - RSA: Disallowed (removed)

### Minimum Router Requirements

- **API version:** 0.9.16+ (for EdDSA compatibility with network)
- **Recommended minimum:** API 0.9.51+ (ECIES short tunnel builds)
- **Current minimum for floodfills:** API 0.9.58+ (ElGamal router deprecation)
- **Upcoming requirement:** Java 17+ (as of release 2.11.0, December 2025)

### Bandwidth Requirements

- **Minimum:** 128 KBytes/sec (N flag or higher) for floodfill
- **Recommended:** 256 KBytes/sec (O flag) or higher
- **Floodfill requirements:**
  - Minimum 128 KB/sec bandwidth
  - Stable uptime (>95% recommended)
  - Low latency (<500ms to peers)
  - Pass health tests (queue time, job lag)

### Tunnel Statistics

- **Typical tunnel length:** 3-4 hops
- **Maximum tunnel length:** 8 hops (theoretical, rarely used)
- **Typical tunnel lifetime:** 10 minutes
- **Tunnel build success rate:** >85% for well-connected routers
- **Tunnel build message format:**
  - ECIES routers: ShortTunnelBuild (218-byte records)
  - Mixed tunnels: VariableTunnelBuild (528-byte records)

### Performance Metrics

- **Tunnel build time:** 1-3 seconds (typical)
- **End-to-end latency:** 0.5-2 seconds (typical, 6-8 hops total)
- **Throughput:** Limited by tunnel bandwidth (typically 10-50 KB/sec per tunnel)
- **Maximum datagram size:** 10 KB recommended (61.2 KB theoretical maximum)

---

## Appendix B: Deprecated and Removed Features

### Completely Removed (No Longer Supported)

- **NTCP transport** - Removed in release 0.9.50 (May 2021)
- **SSU v1 transport** - Removed from Java I2P in release 2.4.0 (December 2023)
- **SSU v1 transport** - Removed from i2pd in release 2.44.0 (November 2022)
- **RSA signature types** - Disallowed as of API 0.9.28

### Deprecated (Supported but Not Recommended)

- **ElGamal routers** - Deprecated as of API 0.9.58 (March 2023)
  - ElGamal destinations still supported for backward compatibility
  - New routers should use ECIES-X25519 exclusively
- **TunnelBuild (type 21)** - Deprecated in favor of VariableTunnelBuild and ShortTunnelBuild
  - Still implemented for very long tunnels (>8 hops)
- **TunnelBuildReply (type 22)** - Deprecated in favor of VariableTunnelBuildReply and OutboundTunnelBuildReply
- **ElGamal/AES encryption** - Deprecated in favor of ECIES-X25519-AEAD-Ratchet
  - Still used for legacy destinations
- **Long ECIES BuildRequestRecords (528 bytes)** - Deprecated in favor of short format (218 bytes)
  - Still used for mixed tunnels with ElGamal hops

### Legacy Support Timeline

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>

---

## Appendix C: Future Developments

### Post-Quantum Cryptography

**Status:** Beta as of release 2.10.0 (September 2025), will become default in 2.11.0 (December 2025)

**Implementation:**
- Hybrid approach combining classical X25519 and post-quantum MLKEM (ML-KEM-768)
- Backward compatible with existing ECIES-X25519 infrastructure
- Uses Signal Double Ratchet with both classical and PQ key material
- See [Proposal 169](/proposals/169-pq-crypto/) for details

**Migration Path:**
1. Release 2.10.0 (September 2025): Available as beta option
2. Release 2.11.0 (December 2025): Enabled by default
3. Future releases: Eventually required

### Planned Features

- **IPv6 improvements** - Better IPv6 support and transition mechanisms
- **Per-tunnel throttling** - Fine-grained bandwidth control per tunnel
- **Enhanced metrics** - Better performance monitoring and diagnostics
- **Protocol optimizations** - Reduced overhead and improved efficiency
- **Improved floodfill selection** - Better network database distribution

### Research Areas

- **Tunnel length optimization** - Dynamic tunnel length based on threat model
- **Advanced padding** - Traffic analysis resistance improvements
- **New encryption schemes** - Preparation for quantum computing threats
- **Congestion control** - Better handling of network load
- **Mobile support** - Optimizations for mobile devices and networks

---

## Appendix D: Implementation Guidelines

### For New Implementations

**Minimum Requirements:**
1. Support API version 0.9.51+ features
2. Implement ECIES-X25519-AEAD-Ratchet encryption
3. Support NTCP2 and SSU2 transports
4. Implement ShortTunnelBuild messages (218-byte records)
5. Support LeaseSet2 variants (types 3, 5, 7)
6. Use EdDSA signatures (Ed25519)

**Recommended:**
1. Support post-quantum hybrid cryptography (as of 2.11.0)
2. Implement per-tunnel bandwidth parameters
3. Support Datagram2 and Datagram3 formats
4. Implement service record options in LeaseSets
5. Follow official specifications at /docs/specs/

**Not Required:**
1. ElGamal router support (deprecated)
2. Legacy transport support (SSU1, NTCP)
3. Long ECIES BuildRequestRecords (528 bytes for pure ECIES tunnels)
4. TunnelBuild/TunnelBuildReply messages (use Variable or Short variants)

### Testing and Validation

**Protocol Compliance:**
1. Test interoperability with official Java I2P router
2. Test interoperability with i2pd C++ router
3. Validate message formats against specifications
4. Test tunnel build/tear-down cycles
5. Verify encryption/decryption with test vectors

**Performance Testing:**
1. Measure tunnel build success rates (should be >85%)
2. Test with various tunnel lengths (2-8 hops)
3. Validate fragmentation and reassembly
4. Test under load (multiple simultaneous tunnels)
5. Measure end-to-end latency

**Security Testing:**
1. Verify encryption implementation (use test vectors)
2. Test replay attack prevention
3. Validate message expiration handling
4. Test against malformed messages
5. Verify proper random number generation

### Common Implementation Pitfalls

1. **Confusing delivery instruction formats** - Garlic clove vs tunnel message
2. **Incorrect key derivation** - HKDF usage for short build records
3. **Message ID handling** - Not setting correctly for tunnel builds
4. **Fragmentation issues** - Not respecting 61.2 KB practical limit
5. **Endianness errors** - Java uses big-endian for all integers
6. **Expiration handling** - Short format wraps on February 7, 2106
7. **Checksum generation** - Still required even if not verified

