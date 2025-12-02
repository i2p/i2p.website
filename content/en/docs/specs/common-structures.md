---
title: "Common Structures"
description: "Shared data types and serialization formats used across I2P specs"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /en/docs/spec/common-structures
  - /spec/common-structures/
  - /en/docs/how/network-database/
---

## Overview

This document specifies the fundamental data structures used across all I2P protocols, including [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/), and others. These common structures ensure interoperability between different I2P implementations and protocol layers.

### Key Changes Since 0.9.58

- ElGamal and DSA-SHA1 deprecated for Router Identities (use X25519 + EdDSA)
- Post-quantum ML-KEM support in beta testing (opt-in as of 2.10.0)
- Service record options standardized ([Proposal 167](/proposals/167-service-records/), implemented 0.9.66)
- Compressible padding specifications finalized ([Proposal 161](/proposals/161-padding-generation/), implemented 0.9.57)

---

## Common Type Specifications

### Integer

**Description:** Represents a non-negative integer in network byte order (big-endian).

**Contents:** 1 to 8 bytes representing an unsigned integer.

**Usage:** Field lengths, counts, type identifiers, and numeric values throughout I2P protocols.

---

### Date

**Description:** Timestamp representing milliseconds since Unix epoch (January 1, 1970 00:00:00 GMT).

**Contents:** 8-byte Integer (unsigned long)

**Special Values:**
- `0` = Undefined or null date
- Maximum value: `0xFFFFFFFFFFFFFFFF` (year 584,942,417,355)

**Implementation Notes:**
- Always UTC/GMT timezone
- Millisecond precision required
- Used for lease expiration, RouterInfo publication, and timestamp validation

---

### String

**Description:** UTF-8 encoded string with length prefix.

**Format:**
```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```

**Constraints:**
- Maximum length: 255 bytes (not characters - multi-byte UTF-8 sequences count as multiple bytes)
- Length may be zero (empty string)
- Null terminator NOT included
- String is NOT null-terminated

**Important:** UTF-8 sequences can use multiple bytes per character. A string with 100 characters might exceed the 255-byte limit if using multi-byte characters.

---

## Cryptographic Key Structures

### PublicKey

**Description:** Public key for asymmetric encryption. Key type and length are context-dependent or specified in a Key Certificate.

**Default Type:** ElGamal (deprecated for Router Identities as of 0.9.58)

**Supported Types:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>

**Implementation Requirements:**

1. **X25519 (Type 4) - Current Standard:**
   - Used for ECIES-X25519-AEAD-Ratchet encryption
   - Mandatory for Router Identities since 0.9.48
   - Little-endian encoding (unlike other types)
   - See [ECIES](/docs/specs/ecies/) and [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - Legacy:**
   - Deprecated for Router Identities as of 0.9.58
   - Still valid for Destinations (field unused since 0.6/2005)
   - Uses constant primes defined in [ElGamal specification](/docs/specs/cryptography/)
   - Support maintained for backward compatibility

3. **MLKEM (Post-Quantum) - Beta:**
   - Hybrid approach combines ML-KEM with X25519
   - NOT enabled by default in 2.10.0
   - Requires manual activation via Hidden Service Manager
   - See [ECIES-HYBRID](/docs/specs/ecies/#hybrid) and [Proposal 169](/proposals/169-pq-crypto/)
   - Type codes and specifications subject to change

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### PrivateKey

**Description:** Private key for asymmetric decryption, corresponding to PublicKey types.

**Storage:** Type and length inferred from context or stored separately in data structures/key files.

**Supported Types:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>

**Security Notes:**
- Private keys MUST be generated using cryptographically secure random number generators
- X25519 private keys use scalar clamping as defined in RFC 7748
- Key material MUST be securely erased from memory when no longer needed

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### SessionKey

**Description:** Symmetric key for AES-256 encryption and decryption in I2P's tunnel and garlic encryption.

**Contents:** 32 bytes (256 bits)

**Usage:**
- Tunnel layer encryption (AES-256/CBC with IV)
- Garlic message encryption
- End-to-end session encryption

**Generation:** MUST use cryptographically secure random number generator.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Description:** Public key for signature verification. Type and length specified in Key Certificate of Destination or inferred from context.

**Default Type:** DSA_SHA1 (deprecated as of 0.9.58)

**Supported Types:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>

**Implementation Requirements:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - Current Standard:**
   - Default for all new Router Identities and Destinations since late 2015
   - Uses Ed25519 curve with SHA-512 hashing
   - 32-byte public keys, 64-byte signatures
   - Little-endian encoding (unlike most other types)
   - High performance and security

2. **RedDSA_SHA512_Ed25519 (Type 11) - Specialized:**
   - Used ONLY for encrypted leasesets and blinding
   - Never used for Router Identities or standard Destinations
   - Key differences from EdDSA:
     - Private keys via modular reduction (not clamping)
     - Signatures include 80 bytes of random data
     - Uses public keys directly (not hashes of private keys)
   - See [Red25519 specification](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - Legacy:**
   - Deprecated for Router Identities as of 0.9.58
   - Discouraged for new Destinations
   - 1024-bit DSA with SHA-1 (known weaknesses)
   - Support maintained for compatibility only

4. **Multi-element Keys:**
   - When composed of two elements (e.g., ECDSA points X,Y)
   - Each element padded to length/2 with leading zeros
   - Example: 64-byte ECDSA key = 32-byte X + 32-byte Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Description:** Private key for creating signatures, corresponding to SigningPublicKey types.

**Storage:** Type and length specified at creation time.

**Supported Types:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>

**Security Requirements:**
- Generate using cryptographically secure random source
- Protect with appropriate access controls
- Securely erase from memory when finished
- For EdDSA: 32-byte seed hashed with SHA-512, first 32 bytes become scalar (clamped)
- For RedDSA: Different key generation (modular reduction instead of clamping)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Signature

**Description:** Cryptographic signature over data, using the signing algorithm corresponding to the SigningPrivateKey type.

**Type and Length:** Inferred from the key type used for signing.

**Supported Types:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>

**Format Notes:**
- Multi-element signatures (e.g., ECDSA R,S values) are padded to length/2 per element with leading zeros
- EdDSA and RedDSA use little-endian encoding
- All other types use big-endian encoding

**Verification:**
- Use the corresponding SigningPublicKey
- Follow the signature algorithm specifications for the key type
- Check that signature length matches expected length for the key type

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Hash

**Description:** SHA-256 hash of data, used throughout I2P for integrity verification and identification.

**Contents:** 32 bytes (256 bits)

**Usage:**
- Router Identity hashes (network database keys)
- Destination hashes (network database keys)
- Tunnel gateway identification in Leases
- Data integrity verification
- Tunnel ID generation

**Algorithm:** SHA-256 as defined in FIPS 180-4

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Session Tag

**Description:** Random number used for session identification and tag-based encryption.

**Important:** Session Tag size varies by encryption type:
- **ElGamal/AES+SessionTag:** 32 bytes (legacy)
- **ECIES-X25519:** 8 bytes (current standard)

**Current Standard (ECIES):**
```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```

See [ECIES](/docs/specs/ecies/) and [ECIES-ROUTERS](/docs/specs/ecies/#routers) for detailed specifications.

**Legacy (ElGamal/AES):**
```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```

**Generation:** MUST use cryptographically secure random number generator.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Description:** Unique identifier for a router's position in a tunnel. Each hop in a tunnel has its own TunnelId.

**Format:**
```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```

**Usage:**
- Identifies incoming/outgoing tunnel connections at each router
- Different TunnelId at each hop in the tunnel chain
- Used in Lease structures to identify gateway tunnels

**Special Values:**
- `0` = Reserved for special protocol uses (avoid in normal operation)
- TunnelIds are locally significant to each router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Certificate Specifications

### Certificate

**Description:** Container for receipts, proof-of-work, or cryptographic metadata used throughout I2P.

**Format:**
```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```

**Total Size:** 3 bytes minimum (NULL certificate), up to 65538 bytes maximum

### Certificate Types

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>

### Key Certificate (Type 5)

**Introduction:** Version 0.9.12 (December 2013)

**Purpose:** Specifies non-default key types and stores excess key data beyond the standard 384-byte KeysAndCert structure.

**Payload Structure:**
```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```

**Critical Implementation Notes:**

1. **Key Type Order:**
   - **WARNING:** Signing key type comes BEFORE Crypto key type
   - This is counterintuitive but maintained for compatibility
   - Order: SPKtype, CPKtype (not CPKtype, SPKtype)

2. **Key Data Layout in KeysAndCert:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Calculating Excess Key Data:**
   - If Crypto Key > 256 bytes: Excess = (Crypto Length - 256)
   - If Signing Key > 128 bytes: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Examples (ElGamal Crypto Key):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>

**Router Identity Requirements:**
- NULL certificate used until version 0.9.15
- Key Certificate required for non-default key types since 0.9.16
- X25519 encryption keys supported since 0.9.48

**Destination Requirements:**
- NULL certificate OR Key Certificate (as needed)
- Key Certificate required for non-default signing key types since 0.9.12
- Crypto public key field unused since 0.6 (2005) but must still be present

**Important Warnings:**

1. **NULL vs KEY Certificate:**
   - A KEY certificate with types (0,0) specifying ElGamal+DSA_SHA1 is allowed but discouraged
   - Always use NULL certificate for ElGamal+DSA_SHA1 (canonical representation)
   - KEY certificate with (0,0) is 4 bytes longer and may cause compatibility issues
   - Some implementations may not handle (0,0) KEY certificates correctly

2. **Excess Data Validation:**
   - Implementations MUST verify certificate length matches expected length for key types
   - Reject certificates with excess data that doesn't correspond to key types
   - Prohibit trailing garbage data after valid certificate structure

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Mapping

**Description:** Key-value property collection used for configuration and metadata.

**Format:**
```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```

**Size Limits:**
- Key length: 0-255 bytes (+ 1 length byte)
- Value length: 0-255 bytes (+ 1 length byte)
- Total mapping size: 0-65535 bytes (+ 2 size field bytes)
- Maximum structure size: 65537 bytes

**Critical Sorting Requirement:**

When mappings appear in **signed structures** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig), entries MUST be sorted by key to ensure signature invariance:

1. **Sort Method:** Lexicographic ordering using Unicode code point values (equivalent to Java String.compareTo())
2. **Case Sensitivity:** Keys and values are generally case-sensitive (application-dependent)
3. **Duplicate Keys:** NOT allowed in signed structures (will cause signature verification failure)
4. **Character Encoding:** UTF-8 byte-level comparison

**Why Sorting Matters:**
- Signatures are computed over the byte representation
- Different key orders produce different signatures
- Unsigned mappings don't require sorting but should follow the same convention

**Implementation Notes:**

1. **Encoding Redundancy:**
   - Both `=` and `;` delimiters AND string length bytes are present
   - This is inefficient but maintained for compatibility
   - Length bytes are authoritative; delimiters are required but redundant

2. **Character Support:**
   - Despite documentation, `=` and `;` ARE supported within strings (length bytes handle this)
   - UTF-8 encoding supports full Unicode
   - **Warning:** I2CP uses UTF-8, but I2NP historically did not handle UTF-8 correctly
   - Use ASCII for I2NP mappings when possible for maximum compatibility

3. **Special Contexts:**
   - **RouterInfo/RouterAddress:** MUST be sorted, no duplicates
   - **I2CP SessionConfig:** MUST be sorted, no duplicates  
   - **Application mappings:** Sorting recommended but not always required

**Example (RouterInfo options):**
```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```

**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Common Structure Specification

### KeysAndCert

**Description:** Fundamental structure combining encryption key, signing key, and certificate. Used as both RouterIdentity and Destination.

**Structure:**
```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```

**Key Alignment:**
- **Crypto Public Key:** Aligned at start (byte 0)
- **Padding:** In the middle (if needed)
- **Signing Public Key:** Aligned at end (byte 256 to byte 383)
- **Certificate:** Starts at byte 384

**Size Calculation:**
```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```

### Padding Generation Guidelines ([Proposal 161](/proposals/161-padding-generation/))

**Implementation Version:** 0.9.57 (January 2023, release 2.1.0)

**Background:**
- For non-ElGamal+DSA keys, padding is present in the 384-byte fixed structure
- For Destinations, the 256-byte public key field has been unused since 0.6 (2005)
- Padding should be generated to be compressible while remaining secure

**Requirements:**

1. **Minimum Random Data:**
   - Use at least 32 bytes of cryptographically secure random data
   - This provides sufficient entropy for security

2. **Compression Strategy:**
   - Repeat the 32 bytes throughout the padding/public key field
   - Protocols like I2NP Database Store, Streaming SYN, SSU2 handshake use compression
   - Significant bandwidth savings without compromising security

3. **Examples:**

**Router Identity (X25519 + EdDSA):**
```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```

**Destination (ElGamal-unused + EdDSA):**
```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```

4. **Why This Works:**
   - SHA-256 hash of the complete structure still includes all entropy
   - Network database DHT distribution depends only on the hash
   - Signing key (32 bytes EdDSA/X25519) provides 256 bits of entropy
   - Additional 32 bytes of repeated random data = 512 bits total entropy
   - More than sufficient for cryptographic strength

5. **Implementation Notes:**
   - MUST store and transmit the full 387+ byte structure
   - SHA-256 hash computed over complete uncompressed structure
   - Compression applied at protocol layer (I2NP, Streaming, SSU2)
   - Backward compatible with all versions since 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity

**Description:** Uniquely identifies a router in the I2P network. Identical structure to KeysAndCert.

**Format:** See KeysAndCert structure above

**Current Requirements (as of 0.9.58):**

1. **Mandatory Key Types:**
   - **Encryption:** X25519 (type 4, 32 bytes)
   - **Signing:** EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
   - **Certificate:** Key Certificate (type 5)

2. **Deprecated Key Types:**
   - ElGamal (type 0) deprecated for Router Identities as of 0.9.58
   - DSA_SHA1 (type 0) deprecated for Router Identities as of 0.9.58
   - These should NOT be used for new routers

3. **Typical Size:**
   - X25519 + EdDSA with Key Certificate = 391 bytes
   - 32 bytes X25519 public key
   - 320 bytes padding (compressible per [Proposal 161](/proposals/161-padding-generation/))
   - 32 bytes EdDSA public key
   - 7 bytes certificate (3-byte header + 4-byte key types)

**Historical Evolution:**
- Pre-0.9.16: Always NULL certificate (ElGamal + DSA_SHA1)
- 0.9.16-0.9.47: Key Certificate support added
- 0.9.48+: X25519 encryption keys supported
- 0.9.58+: ElGamal and DSA_SHA1 deprecated

**Network Database Key:**
- RouterInfo keyed by SHA-256 hash of complete RouterIdentity
- Hash computed over full 391+ byte structure (including padding)

**See Also:**
- Padding generation guidelines ([Proposal 161](/proposals/161-padding-generation/))
- Key Certificate specification above

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Destination

**Description:** Endpoint identifier for secure message delivery. Structurally identical to KeysAndCert, but with different usage semantics.

**Format:** See KeysAndCert structure above

**Critical Difference from RouterIdentity:**
- **Public key field is UNUSED and may contain random data**
- This field has been unused since version 0.6 (2005)
- Was originally for old I2CP-to-I2CP encryption (disabled)
- Currently only used as IV for deprecated LeaseSet encryption

**Current Recommendations:**

1. **Signing Key:**
   - **Recommended:** EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
   - Alternative: ECDSA types for older compatibility
   - Avoid: DSA_SHA1 (deprecated, discouraged)

2. **Encryption Key:**
   - Field is unused but must be present
   - **Recommended:** Fill with random data per [Proposal 161](/proposals/161-padding-generation/) (compressible)
   - Size: Always 256 bytes (ElGamal slot, even though not used for ElGamal)

3. **Certificate:**
   - NULL certificate for ElGamal + DSA_SHA1 (legacy only)
   - Key Certificate for all other signing key types

**Typical Modern Destination:**
```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```

**Actual Encryption Key:**
- Encryption key for the Destination is in the **LeaseSet**, not the Destination
- LeaseSet contains current encryption public key(s)
- See LeaseSet2 specification for encryption key handling

**Network Database Key:**
- LeaseSet keyed by SHA-256 hash of complete Destination
- Hash computed over full 387+ byte structure

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Network Database Structures

### Lease

**Description:** Authorizes a specific tunnel to receive messages for a Destination. Part of the original LeaseSet format (type 1).

**Format:**
```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```

**Total Size:** 44 bytes

**Usage:**
- Used only in original LeaseSet (type 1, deprecated)
- For LeaseSet2 and later variants, use Lease2 instead

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Type 1)

**Description:** Original LeaseSet format. Contains authorized tunnels and keys for a Destination. Stored in network database. **Status: Deprecated** (use LeaseSet2 instead).

**Structure:**
```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```

**Database Storage:**
- **Database Type:** 1
- **Key:** SHA-256 hash of Destination
- **Value:** Complete LeaseSet structure

**Important Notes:**

1. **Destination Public Key Unused:**
   - The encryption public key field in the Destination is unused
   - Encryption key in the LeaseSet is the actual encryption key

2. **Temporary Keys:**
   - `encryption_key` is temporary (regenerated at router startup)
   - `signing_key` is temporary (regenerated at router startup)
   - Neither key is persistent across restarts

3. **Revocation (Unimplemented):**
   - `signing_key` was intended for LeaseSet revocation
   - Revocation mechanism never implemented
   - Zero-lease LeaseSet was intended for revocation but is unused

4. **Versioning/Timestamp:**
   - LeaseSet has no explicit `published` timestamp field
   - Version is the earliest expiration of all leases
   - New LeaseSet must have earlier lease expiration to be accepted

5. **Lease Expiration Publishing:**
   - Pre-0.9.7: All leases published with same expiration (earliest)
   - 0.9.7+: Actual individual lease expirations published
   - This is an implementation detail, not part of the specification

6. **Zero Leases:**
   - LeaseSet with zero leases is technically allowed
   - Intended for revocation (unimplemented)
   - Unused in practice
   - LeaseSet2 variants require at least one Lease

**Deprecation:** LeaseSet type 1 is deprecated. New implementations should use **LeaseSet2 (type 3)** which provides:
- Published timestamp field (better versioning)
- Multiple encryption key support
- Offline signature capability
- 4-byte lease expirations (vs 8-byte)
- More flexible options

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet Variants

### Lease2

**Description:** Improved lease format with 4-byte expiration. Used in LeaseSet2 (type 3) and MetaLeaseSet (type 7).

**Introduction:** Version 0.9.38 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Format:**
```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```

**Total Size:** 40 bytes (4 bytes smaller than original Lease)

**Comparison with Original Lease:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>

**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### OfflineSignature

**Description:** Optional structure for pre-signed transient keys, allowing LeaseSet publication without online access to the Destination's private signing key.

**Introduction:** Version 0.9.38 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Format:**
```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```

**Purpose:**
- Enables offline LeaseSet generation
- Protects Destination master key from online exposure
- Transient key can be revoked by publishing new LeaseSet without offline signature

**Usage Scenarios:**

1. **High-Security Destinations:**
   - Master signing key stored offline (HSM, cold storage)
   - Transient keys generated offline for limited time periods
   - Compromised transient key doesn't expose master key

2. **Encrypted LeaseSet Publishing:**
   - EncryptedLeaseSet can include offline signature
   - Blinded public key + offline signature provides additional security

**Security Considerations:**

1. **Expiration Management:**
   - Set reasonable expiration (days to weeks, not years)
   - Generate new transient keys before expiration
   - Shorter expiration = better security, more maintenance

2. **Key Generation:**
   - Generate transient keys offline in secure environment
   - Sign with master key offline
   - Transfer only signed transient key + signature to online router

3. **Revocation:**
   - Publish new LeaseSet without offline signature to implicitly revoke
   - Or publish new LeaseSet with different transient key

**Signature Verification:**
```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```

**Implementation Notes:**
- Total size varies based on sigtype and Destination signing key type
- Minimum size: 4 + 2 + 32 (EdDSA key) + 64 (EdDSA signature) = 102 bytes
- Maximum practical size: ~600 bytes (RSA-4096 transient key + RSA-4096 signature)

**Compatible With:**
- LeaseSet2 (type 3)
- EncryptedLeaseSet (type 5)
- MetaLeaseSet (type 7)

**See Also:** [Proposal 123](/proposals/123-new-netdb-entries/) for detailed offline signature protocol.

---

### LeaseSet2Header

**Description:** Common header structure for LeaseSet2 (type 3) and MetaLeaseSet (type 7).

**Introduction:** Version 0.9.38 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Format:**
```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```

**Minimum Total Size:** 395 bytes (without offline signature)

**Flag Definitions (bit order: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>

**Flag Details:**

**Bit 0 - Offline Keys:**
- `0`: No offline signature, use Destination's signing key to verify LeaseSet signature
- `1`: OfflineSignature structure follows flags field

**Bit 1 - Unpublished:**
- `0`: Standard published LeaseSet, should be flooded to floodfills
- `1`: Unpublished LeaseSet (client-side only)
  - Should NOT be flooded, published, or sent in response to queries
  - If expired, do NOT query netdb for replacement (unless bit 2 also set)
  - Used for local tunnels or testing

**Bit 2 - Blinded (since 0.9.42):**
- `0`: Standard LeaseSet
- `1`: This unencrypted LeaseSet will be blinded and encrypted when published
  - Published version will be EncryptedLeaseSet (type 5)
  - If expired, query the **blinded location** in netdb for replacement
  - Must also set bit 1 to 1 (unpublished + blinded)
  - Used for encrypted hidden services

**Expiration Limits:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>

**Published Timestamp Requirements:**

LeaseSet (type 1) did not have a published field, requiring searching for earliest lease expiration for versioning. LeaseSet2 adds explicit `published` timestamp with 1-second resolution.

**Critical Implementation Note:**
- Routers MUST rate-limit LeaseSet publishing to **much slower than once per second** per Destination
- If publishing faster, ensure each new LeaseSet has `published` time at least 1 second later
- Floodfills will reject LeaseSet if `published` time is not newer than current version
- Recommended minimum interval: 10-60 seconds between publications

**Calculation Examples:**

**LeaseSet2 (11-minute max):**
```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```

**MetaLeaseSet (18.2-hour max):**
```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```

**Versioning:**
- LeaseSet is considered "newer" if `published` timestamp is greater
- Floodfills store and flood only the newest version
- Take care when oldest Lease matches previous LeaseSet's oldest Lease

---

### LeaseSet2 (Type 3)

**Description:** Modern LeaseSet format with multiple encryption keys, offline signatures, and service records. Current standard for I2P hidden services.

**Introduction:** Version 0.9.38 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Structure:**
```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```

**Database Storage:**
- **Database Type:** 3
- **Key:** SHA-256 hash of Destination
- **Value:** Complete LeaseSet2 structure

**Signature Computation:**
```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```

### Encryption Key Preference Order

**For Published (Server) LeaseSet:**
- Keys listed in order of server preference (most preferred first)
- Clients supporting multiple types SHOULD honor server preference
- Select first supported type from the list
- Generally, higher-numbered (newer) key types are more secure/efficient
- Recommended order: List keys in reverse order by type code (newest first)

**Example Server Preference:**
```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```

**For Unpublished (Client) LeaseSet:**
- Key order effectively doesn't matter (connections rarely attempted to clients)
- Follow same convention for consistency

**Client Key Selection:**
- Honor server preference (select first supported type)
- Or use implementation-defined preference
- Or determine combined preference based on both capabilities

### Options Mapping

**Requirements:**
- Options MUST be sorted by key (lexicographic, UTF-8 byte order)
- Sorting ensures signature invariance
- Duplicate keys NOT allowed

**Standard Format ([Proposal 167](/proposals/167-service-records/)):**

As of API 0.9.66 (June 2025, release 2.9.0), service record options follow a standardized format. See [Proposal 167](/proposals/167-service-records/) for complete specification.

**Service Record Option Format:**
```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```

**Example Service Records:**

**1. Self-Referencing SMTP Server:**
```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```

**2. Single External SMTP Server:**
```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```

**3. Multiple SMTP Servers (Load Balancing):**
```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```

**4. HTTP Service with App Options:**
```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```

**TTL Recommendations:**
- Minimum: 86400 seconds (1 day)
- Longer TTL reduces netdb query load
- Balance between query reduction and service update propagation
- For stable services: 604800 (7 days) or longer

**Implementation Notes:**

1. **Encryption Keys (as of 0.9.44):**
   - ElGamal (type 0, 256 bytes): Legacy compatibility
   - X25519 (type 4, 32 bytes): Current standard
   - MLKEM variants: Post-quantum (beta, not finalized)

2. **Key Length Validation:**
   - Floodfills and clients MUST be able to parse unknown key types
   - Use keylen field to skip unknown keys
   - Do not fail parsing if key type is unknown

3. **Published Timestamp:**
   - See LeaseSet2Header notes about rate-limiting
   - Minimum 1-second increment between publications
   - Recommended: 10-60 seconds between publications

4. **Encryption Type Migration:**
   - Multiple keys support gradual migration
   - List both old and new keys during transition period
   - Remove old key after sufficient client upgrade period

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease

**Description:** Lease structure for MetaLeaseSet that can reference other LeaseSets rather than tunnels. Used for load balancing and redundancy.

**Introduction:** Version 0.9.38, scheduled working 0.9.40 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Format:**
```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```

**Total Size:** 40 bytes

**Entry Type (flags bits 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>

**Usage Scenarios:**

1. **Load Balancing:**
   - MetaLeaseSet with multiple MetaLease entries
   - Each entry points to different LeaseSet2
   - Clients select based on cost field

2. **Redundancy:**
   - Multiple entries pointing to backup LeaseSets
   - Fallback if primary LeaseSet unavailable

3. **Service Migration:**
   - MetaLeaseSet points to new LeaseSet
   - Allows smooth transition between Destinations

**Cost Field Usage:**
- Lower cost = higher priority
- Cost 0 = highest priority
- Cost 255 = lowest priority
- Clients SHOULD prefer lower-cost entries
- Equal-cost entries may be load-balanced randomly

**Comparison with Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>

**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Type 7)

**Description:** LeaseSet variant that contains MetaLease entries, providing indirection to other LeaseSets. Used for load balancing, redundancy, and service migration.

**Introduction:** Defined 0.9.38, scheduled working 0.9.40 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Status:** Specification complete. Production deployment status should be verified with current I2P releases.

**Structure:**
```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```

**Database Storage:**
- **Database Type:** 7
- **Key:** SHA-256 hash of Destination
- **Value:** Complete MetaLeaseSet structure

**Signature Computation:**
```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```

**Usage Scenarios:**

**1. Load Balancing:**
```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```

**2. Failover:**
```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```

**3. Service Migration:**
```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```

**4. Multi-Tier Architecture:**
```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```

**Revocation List:**

The revocation list allows MetaLeaseSet to explicitly revoke previously published LeaseSets:

- **Purpose:** Mark specific Destinations as no longer valid
- **Contents:** SHA-256 hashes of revoked Destination structures
- **Usage:** Clients MUST NOT use LeaseSets whose Destination hash appears in revocation list
- **Typical Value:** Empty (numr=0) in most deployments

**Example Revocation:**
```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```

**Expiration Handling:**

MetaLeaseSet uses LeaseSet2Header with maximum expires=65535 seconds (~18.2 hours):

- Much longer than LeaseSet2 (max ~11 minutes)
- Suitable for relatively static indirection
- Referenced LeaseSets can have shorter expiration
- Clients must check expiration of both MetaLeaseSet AND referenced LeaseSets

**Options Mapping:**

- Use same format as LeaseSet2 options
- Can include service records ([Proposal 167](/proposals/167-service-records/))
- MUST be sorted by key
- Service records typically describe the ultimate service, not the indirection structure

**Client Implementation Notes:**

1. **Resolution Process:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Caching:**
   - Cache both MetaLeaseSet and referenced LeaseSets
   - Check expiration of both levels
   - Monitor for updated MetaLeaseSet publication

3. **Failover:**
   - If preferred entry fails, try next-lowest cost
   - Consider marking failed entries temporarily unavailable
   - Re-check periodically for recovery

**Implementation Status:**

[Proposal 123](/proposals/123-new-netdb-entries/) notes portions remain "in development." Implementers should:
- Verify production readiness in target I2P version
- Test MetaLeaseSet support before deployment
- Check for updated specifications in newer I2P releases

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Type 5)

**Description:** Encrypted and blinded LeaseSet for enhanced privacy. Only the blinded public key and metadata are visible; actual leases and encryption keys are encrypted.

**Introduction:** Defined 0.9.38, working 0.9.39 (see [Proposal 123](/proposals/123-new-netdb-entries/))

**Structure:**
```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```

**Database Storage:**
- **Database Type:** 5
- **Key:** SHA-256 hash of **blinded Destination** (not original Destination)
- **Value:** Complete EncryptedLeaseSet structure

**Critical Differences from LeaseSet2:**

1. **Does NOT use LeaseSet2Header structure** (has similar fields but different layout)
2. **Blinded public key** instead of full Destination
3. **Encrypted payload** instead of cleartext leases and keys
4. **Database key is hash of blinded Destination**, not original Destination

**Signature Computation:**
```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```

**Signature Type Requirement:**

**MUST use RedDSA_SHA512_Ed25519 (type 11):**
- 32-byte blinded public keys
- 64-byte signatures
- Required for blinding security properties
- See [Red25519 specification](//docs/specs/red25519-signature-scheme/

**Key Differences from EdDSA:**
- Private keys via modular reduction (not clamping)
- Signatures include 80 bytes of random data
- Uses public keys directly (not hashes)
- Enables secure blinding operation

**Blinding and Encryption:**

See [EncryptedLeaseSet specification](/docs/specs/encryptedleaseset/) for complete details:

**1. Key Blinding:**
```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```

**2. Database Location:**
```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```

**3. Encryption Layers (Three-Layer):**

**Layer 1 - Authentication Layer (Client Access):**
- Encryption: ChaCha20 stream cipher
- Key derivation: HKDF with per-client secrets
- Authenticated clients can decrypt outer layer

**Layer 2 - Encryption Layer:**
- Encryption: ChaCha20
- Key: Derived from DH between client and server
- Contains the actual LeaseSet2 or MetaLeaseSet

**Layer 3 - Inner LeaseSet:**
- Complete LeaseSet2 or MetaLeaseSet
- Includes all tunnels, encryption keys, options
- Only accessible after successful decryption

**Encryption Key Derivation:**
```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```

**Discovery Process:**

**For authorized clients:**
```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```

**For unauthorized clients:**
- Cannot decrypt even if they find the EncryptedLeaseSet
- Cannot determine original Destination from blinded version
- Cannot link EncryptedLeaseSets across different blinding periods (daily rotation)

**Expiration Times:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>

**Published Timestamp:**

Same requirements as LeaseSet2Header:
- Must increment by at least 1 second between publications
- Floodfills reject if not newer than current version
- Recommended: 10-60 seconds between publications

**Offline Signatures with Encrypted LeaseSets:**

Special considerations when using offline signatures:
- Blinded public key rotates daily
- Offline signature must be regenerated daily with new blinded key
- OR use offline signature on inner LeaseSet, not outer EncryptedLeaseSet
- See [Proposal 123](/proposals/123-new-netdb-entries/) notes

**Implementation Notes:**

1. **Client Authorization:**
   - Multiple clients can be authorized with different keys
   - Each authorized client has unique decryption credentials
   - Revoke client by changing authorization keys

2. **Daily Key Rotation:**
   - Blinded keys change at UTC midnight
   - Clients must recompute blinded Destination daily
   - Old EncryptedLeaseSets become undiscoverable after rotation

3. **Privacy Properties:**
   - Floodfills cannot determine original Destination
   - Unauthorized clients cannot access service
   - Different blinding periods cannot be linked
   - No cleartext metadata beyond expiration times

4. **Performance:**
   - Clients must perform daily blinding calculation
   - Three-layer encryption adds computational overhead
   - Consider caching decrypted inner LeaseSet

**Security Considerations:**

1. **Authorization Key Management:**
   - Securely distribute client authorization credentials
   - Use unique credentials per client for granular revocation
   - Rotate authorization keys periodically

2. **Clock Synchronization:**
   - Daily blinding depends on synchronized UTC dates
   - Clock skew can cause lookup failures
   - Consider supporting previous/next day's blinding for tolerance

3. **Metadata Leakage:**
   - Published and expires fields are cleartext
   - Pattern analysis might reveal service characteristics
   - Randomize publication intervals if concerned

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router Structures

### RouterAddress

**Description:** Defines connection information for a router through a specific transport protocol.

**Format:**
```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```

**CRITICAL - Expiration Field:**

⚠️ **The expiration field MUST be set to all zeros (8 zero bytes).**

- **Reason:** Since release 0.9.3, non-zero expiration causes signature verification failure
- **History:** Expiration was originally unused, always null
- **Current Status:** Field was recognized again as of 0.9.12, but must wait for network upgrade
- **Implementation:** Always set to 0x0000000000000000

Any non-zero expiration will cause the RouterInfo signature to fail validation.

### Transport Protocols

**Current Protocols (as of 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>

**Transport Style Values:**
- `"SSU2"`: Current UDP-based transport
- `"NTCP2"`: Current TCP-based transport
- `"NTCP"`: Legacy, removed (do not use)
- `"SSU"`: Legacy, removed (do not use)

### Common Options

All transports typically include:
```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```

### SSU2-Specific Options

See [SSU2 specification](/docs/specs/ssu2/) for complete details.

**Required Options:**
```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```

**Optional Options:**
```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```

**Example SSU2 RouterAddress:**
```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```

### NTCP2-Specific Options

See [NTCP2 specification](/docs/specs/ntcp2/) for complete details.

**Required Options:**
```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```

**Optional Options (since 0.9.50):**
```
"caps" = Capability string
```

**Example NTCP2 RouterAddress:**
```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```

### Implementation Notes

1. **Cost Values:**
   - UDP (SSU2) typically lower cost (5-6) due to efficiency
   - TCP (NTCP2) typically higher cost (10-11) due to overhead
   - Lower cost = preferred transport

2. **Multiple Addresses:**
   - Routers may publish multiple RouterAddress entries
   - Different transports (SSU2 and NTCP2)
   - Different IP versions (IPv4 and IPv6)
   - Clients select based on cost and capabilities

3. **Hostname vs IP:**
   - IP addresses preferred for performance
   - Hostnames supported but add DNS lookup overhead
   - Consider using IP for published RouterInfos

4. **Base64 Encoding:**
   - All keys and binary data encoded in Base64
   - Standard Base64 (RFC 4648)
   - No padding or non-standard characters

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**Description:** Complete published information about a router, stored in the network database. Contains identity, addresses, and capabilities.

**Format:**
```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```

**Database Storage:**
- **Database Type:** 0
- **Key:** SHA-256 hash of RouterIdentity
- **Value:** Complete RouterInfo structure

**Published Timestamp:**
- 8-byte Date (milliseconds since epoch)
- Used for RouterInfo versioning
- Routers publish new RouterInfo periodically
- Floodfills keep newest version based on published timestamp

**Address Sorting:**
- **Historical:** Very old routers required addresses sorted by SHA-256 of their data
- **Current:** Sorting NOT required, not worth implementing for compatibility
- Addresses can be in any order

**Peer Size Field (Historical):**
- **Always 0** in modern I2P
- Was intended for restricted routes (unimplemented)
- If implemented, would be followed by that many Router Hashes
- Some old implementations might have required sorted peer list

**Options Mapping:**

Options MUST be sorted by key. Standard options include:

**Capability Options:**
```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```

**Network Options:**
```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```

**Statistical Options:**
```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```

See [Network Database RouterInfo documentation](/docs/specs/common-structures/#routerInfo) for complete list of standard options.

**Signature Computation:**
```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```

**Typical Modern RouterInfo:**
```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```

**Implementation Notes:**

1. **Multiple Addresses:**
   - Routers typically publish 1-4 addresses
   - IPv4 and IPv6 variants
   - SSU2 and/or NTCP2 transports
   - Each address independent

2. **Versioning:**
   - Newer RouterInfo has later `published` timestamp
   - Routers republish every ~2 hours or when addresses change
   - Floodfills store and flood only newest version

3. **Validation:**
   - Verify signature before accepting RouterInfo
   - Check expiration field is all zeros in each RouterAddress
   - Validate options mapping is sorted by key
   - Check certificate and key types are known/supported

4. **Network Database:**
   - Floodfills store RouterInfo indexed by Hash(RouterIdentity)
   - Stored for ~2 days after last publication
   - Routers query floodfills to discover other routers

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Implementation Notes

### Byte Order (Endianness)

**Default: Big-Endian (Network Byte Order)**

Most I2P structures use big-endian byte order:
- All Integer types (1-8 bytes)
- Date timestamps
- TunnelId
- String length prefix
- Certificate types and lengths
- Key type codes
- Mapping size fields

**Exception: Little-Endian**

The following key types use **little-endian** encoding:
- **X25519** encryption keys (type 4)
- **EdDSA_SHA512_Ed25519** signing keys (type 7)
- **EdDSA_SHA512_Ed25519ph** signing keys (type 8)
- **RedDSA_SHA512_Ed25519** signing keys (type 11)

**Implementation:**
```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```

### Structure Versioning

**Never Assume Fixed Sizes:**

Many structures have variable length:
- RouterIdentity: 387+ bytes (not always 387)
- Destination: 387+ bytes (not always 387)
- LeaseSet2: Varies significantly
- Certificate: 3+ bytes

**Always Read Size Fields:**
- Certificate length at bytes 1-2
- Mapping size at beginning
- KeysAndCert always compute as 384 + 3 + certificate_length

**Check for Excess Data:**
- Prohibit trailing garbage after valid structures
- Validate certificate lengths match key types
- Enforce exact expected lengths for fixed-size types

### Current Recommendations (October 2025)

**For New Router Identities:**
```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/proposals/161-padding-generation/)
```

**For New Destinations:**
```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/proposals/161-padding-generation/)
```

**For New LeaseSets:**
```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```

**For Encrypted Services:**
```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```

### Deprecated Features - Do Not Use

**Deprecated Encryption:**
- ElGamal (type 0) for Router Identities (deprecated 0.9.58)
- ElGamal/AES+SessionTag encryption (use ECIES-X25519)

**Deprecated Signing:**
- DSA_SHA1 (type 0) for Router Identities (deprecated 0.9.58)
- ECDSA variants (types 1-3) for new implementations
- RSA variants (types 4-6) except for SU3 files

**Deprecated Network Formats:**
- LeaseSet type 1 (use LeaseSet2)
- Lease (44 bytes, use Lease2)
- Original Lease expiration format

**Deprecated Transports:**
- NTCP (removed 0.9.50)
- SSU (removed 2.4.0)

**Deprecated Certificates:**
- HASHCASH (type 1)
- HIDDEN (type 2)
- SIGNED (type 3)
- MULTIPLE (type 4)

### Security Considerations

**Key Generation:**
- Always use cryptographically secure random number generators
- Never reuse keys across different contexts
- Protect private keys with appropriate access controls
- Securely erase key material from memory when finished

**Signature Verification:**
- Always verify signatures before trusting data
- Check signature length matches key type
- Validate signed data includes expected fields
- For sorted mappings, verify sort order before signing/verifying

**Timestamp Validation:**
- Check that published times are reasonable (not far future)
- Validate lease expirations are not expired
- Consider clock skew tolerance (±30 seconds typical)

**Network Database:**
- Validate all structures before storing
- Enforce size limits to prevent DoS
- Rate-limit queries and publications
- Verify database keys match structure hashes

### Compatibility Notes

**Backward Compatibility:**
- ElGamal and DSA_SHA1 still supported for legacy routers
- Deprecated key types remain functional but discouraged
- Compressible padding ([Proposal 161](/proposals/161-padding-generation/)) backward compatible to 0.6

**Forward Compatibility:**
- Unknown key types can be parsed using length fields
- Unknown certificate types can be skipped using length
- Unknown signature types should be handled gracefully
- Implementers should not fail on unknown optional features

**Migration Strategies:**
- Support both old and new key types during transition
- LeaseSet2 can list multiple encryption keys
- Offline signatures enable secure key rotation
- MetaLeaseSet enables transparent service migration

### Testing and Validation

**Structure Validation:**
- Verify all length fields are within expected ranges
- Check that variable-length structures parse correctly
- Validate that signatures verify successfully
- Test with both minimum and maximum size structures

**Edge Cases:**
- Zero-length strings
- Empty mappings
- Minimum and maximum lease counts
- Certificate with zero-length payload
- Very large structures (near maximum sizes)

**Interoperability:**
- Test against official Java I2P implementation
- Verify compatibility with i2pd
- Test with various network database contents
- Validate against known-good test vectors

---

## References

### Specifications

- [I2NP Protocol](/docs/specs/i2np/)
- [I2CP Protocol](/docs/specs/i2cp/)
- [SSU2 Transport](/docs/specs/ssu2/)
- [NTCP2 Transport](/docs/specs/ntcp2/)
- [Tunnel Protocol](/docs/specs/implementation/)
- [Datagram Protocol](/docs/api/datagrams/)

### Cryptography

- [Cryptography Overview](/docs/specs/cryptography/)
- [ElGamal/AES Encryption](/docs/legacy/elgamal-aes/)
- [ECIES-X25519 Encryption](/docs/specs/ecies/)
- [ECIES for Routers](/docs/specs/ecies/#routers)
- [ECIES Hybrid (Post-Quantum)](/docs/specs/ecies/#hybrid)
- [Red25519 Signatures](/docs/specs/red25519-signature-scheme/)
- [Encrypted LeaseSet](/docs/specs/encryptedleaseset/)

### Proposals

- [Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)
- [Proposal 134: GOST Signature Types](/proposals/134-gost-signature-types/)
- [Proposal 136: Experimental Signature Types](/proposals/136-experimental-sigtypes/)
- [Proposal 145: ECIES-P256](/proposals/145-ecies-p256/)
- [Proposal 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Proposal 161: Padding Generation](/proposals/161-padding-generation/)
- [Proposal 167: Service Records](/proposals/167-service-records/)
- [Proposal 169: Post-Quantum Crypto](/proposals/169-pq-crypto/)
- [All Proposals Index](/proposals/)

### Network Database

- [Network Database Overview](/docs/specs/common-structures/)
- [RouterInfo Standard Options](/docs/specs/common-structures/#routerInfo)

### JavaDoc API Reference

- [Core Data Package](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### External Standards

- **RFC 7748 (X25519):** Elliptic Curves for Security
- **RFC 7539 (ChaCha20):** ChaCha20 and Poly1305 for IETF Protocols
- **RFC 4648 (Base64):** The Base16, Base32, and Base64 Data Encodings
- **FIPS 180-4 (SHA-256):** Secure Hash Standard
- **FIPS 204 (ML-DSA):** Module-Lattice-Based Digital Signature Standard
- [IANA Service Registry](http://www.dns-sd.org/ServiceTypes.html)

### Community Resources

- [I2P Website](/)
- [I2P Forum](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P GitHub Mirror](https://github.com/i2p/i2p.i2p)
- [Technical Documentation Index](/docs/)

### Release Information

- [I2P 2.10.0 Release](/blog/2025-09-08-i2p-2-10-0-release/)
- [Release History](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Changelog](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Appendix: Quick Reference Tables

### Key Type Quick Reference

**Current Standard (Recommended for all new implementations):**
- **Encryption:** X25519 (type 4, 32 bytes, little-endian)
- **Signing:** EdDSA_SHA512_Ed25519 (type 7, 32 bytes, little-endian)

**Legacy (Supported but deprecated):**
- **Encryption:** ElGamal (type 0, 256 bytes, big-endian)
- **Signing:** DSA_SHA1 (type 0, 20-byte private / 128-byte public, big-endian)

**Specialized:**
- **Signing (Encrypted LeaseSet):** RedDSA_SHA512_Ed25519 (type 11, 32 bytes, little-endian)

**Post-Quantum (Beta, not finalized):**
- **Hybrid Encryption:** MLKEM_X25519 variants (types 5-7)
- **Pure PQ Encryption:** MLKEM variants (no assigned type codes yet)

### Structure Size Quick Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>

### Database Type Quick Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>

### Transport Protocol Quick Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>

### Version Milestone Quick Reference

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="/proposals/161-padding-generation/">Proposal 161</a> padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="/proposals/167-service-records/">Proposal 167</a> service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>

---
