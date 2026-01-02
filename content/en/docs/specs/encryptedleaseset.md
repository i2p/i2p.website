---
title: "Encrypted LeaseSet"
description: "Access-controlled LeaseSet format for private Destinations"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---


## Overview

This document specifies the blinding, encryption, and decryption of encrypted LeaseSet2 (LS2). Encrypted LeaseSets provide access-controlled publication of hidden service information in the I2P network database.

**Key Features:**
- Daily key rotation for forward secrecy
- Two-tier client authorization (DH-based and PSK-based)
- ChaCha20 encryption for performance on devices without AES hardware
- Red25519 signatures with key blinding
- Privacy-preserving client membership

**Related Documentation:**
- [Common Structures Specification](/docs/specs/common-structures/) - Encrypted LeaseSet structure
- [Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/) - Background on encrypted LeaseSets
- [Network Database Documentation](/docs/specs/common-structures/) - NetDB usage

---

## Version History and Implementation Status

### Protocol Development Timeline

**Important Note on Version Numbering:**  
I2P uses two separate version numbering schemes:
- **API/Router Version:** 0.9.x series (used in technical specifications)
- **Product Release Version:** 2.x.x series (used for public releases)

Technical specifications reference API versions (e.g., 0.9.41), while end users see product versions (e.g., 2.10.0).

### Implementation Milestones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>

### Current Status

- ✅ **Protocol Status:** Stable and unchanged since June 2019
- ✅ **Java I2P:** Fully implemented in version 0.9.40+
- ✅ **i2pd (C++):** Fully implemented in version 2.58.0+
- ✅ **Interoperability:** Complete between implementations
- ✅ **Network Deployment:** Production-ready with 6+ years of operational experience

---

## Cryptographic Definitions

### Notation and Conventions

- `||` denotes concatenation
- `mod L` denotes modular reduction by the Ed25519 order
- All byte arrays are in network byte order (big-endian) unless otherwise specified
- Little-endian values are explicitly noted

### CSRNG(n)

**Cryptographically Secure Random Number Generator**

Produces `n` bytes of cryptographically secure random data suitable for key material generation.

**Security Requirements:**
- Must be cryptographically secure (suitable for key generation)
- Must be safe when adjacent byte sequences are exposed on the network
- Implementations should hash output from potentially untrustworthy sources

**References:**
- [PRNG Security Considerations](http://projectbullrun.org/dual-ec/ext-rand.html)
- [Tor Dev Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**SHA-256 Hash with Personalization**

Domain-separated hash function that takes:
- `p`: Personalization string (provides domain separation)
- `d`: Data to hash

**Implementation:**
```
H(p, d) := SHA-256(p || d)
```

**Usage:** Provides cryptographic domain separation to prevent collision attacks between different protocol uses of SHA-256.

### STREAM: ChaCha20

**Stream Cipher: ChaCha20 as specified in RFC 7539 Section 2.4**

**Parameters:**
- `S_KEY_LEN = 32` (256-bit key)
- `S_IV_LEN = 12` (96-bit nonce)
- Initial counter: `1` (RFC 7539 permits 0 or 1; 1 recommended for AEAD contexts)

**ENCRYPT(k, iv, plaintext)**

Encrypts plaintext using:
- `k`: 32-byte cipher key
- `iv`: 12-byte nonce (MUST be unique for each key)
- Returns ciphertext same size as plaintext

**Security Property:** Entire ciphertext must be indistinguishable from random if key is secret.

**DECRYPT(k, iv, ciphertext)**

Decrypts ciphertext using:
- `k`: 32-byte cipher key
- `iv`: 12-byte nonce
- Returns plaintext

**Design Rationale:** ChaCha20 selected over AES because:
- 2.5-3x faster than AES on devices without hardware acceleration
- Constant-time implementation easier to achieve
- Comparable security and speed when AES-NI available

**References:**
- [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 and Poly1305 for IETF Protocols

### SIG: Red25519

**Signature Scheme: Red25519 (SigType 11) with Key Blinding**

Red25519 is based on Ed25519 signatures over the Ed25519 curve, using SHA-512 for hashing, with support for key blinding as specified in ZCash RedDSA.

**Functions:**

#### DERIVE_PUBLIC(privkey)
Returns the public key corresponding to the given private key.
- Uses standard Ed25519 scalar multiplication by base point

#### SIGN(privkey, m)
Returns a signature by the private key `privkey` over message `m`.

**Red25519 Signing Differences from Ed25519:**
1. **Random Nonce:** Uses 80 bytes of additional random data
   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
   This makes every Red25519 signature unique, even for the same message and key.

2. **Private Key Generation:** Red25519 private keys are generated from random numbers and reduced `mod L`, rather than using Ed25519's bit-clamping approach.

#### VERIFY(pubkey, m, sig)
Verifies signature `sig` against public key `pubkey` and message `m`.
- Returns `true` if signature is valid, `false` otherwise
- Verification is identical to Ed25519

**Key Blinding Operations:**

#### GENERATE_ALPHA(data, secret)
Generates alpha for key blinding.
- `data`: Typically contains the signing public key and signature types
- `secret`: Optional additional secret (zero-length if not used)
- Result is identically distributed as Ed25519 private keys (after mod L reduction)

#### BLIND_PRIVKEY(privkey, alpha)
Blinds a private key using secret `alpha`.
- Implementation: `blinded_privkey = (privkey + alpha) mod L`
- Uses scalar arithmetic in the field

#### BLIND_PUBKEY(pubkey, alpha)
Blinds a public key using secret `alpha`.
- Implementation: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)`
- Uses group element (point) addition on the curve

**Critical Property:**
```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```

**Security Considerations:**

From ZCash Protocol Specification Section 5.4.6.1: For security, alpha must be identically distributed as the unblinded private keys. This ensures "the combination of a re-randomized public key and signature(s) under that key do not reveal the key from which it was re-randomized."

**Supported Signature Types:**
- **Type 7 (Ed25519):** Supported for existing destinations (backward compatibility)
- **Type 11 (Red25519):** Recommended for new destinations using encryption
- **Blinded keys:** Always use type 11 (Red25519)

**References:**
- [ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf) - Section 5.4.6 RedDSA
- [I2P Red25519 Specification](/docs/specs/red25519-signature-scheme/)

### DH: X25519

**Elliptic Curve Diffie-Hellman: X25519**

Public key agreement system based on Curve25519.

**Parameters:**
- Private keys: 32 bytes
- Public keys: 32 bytes
- Shared secret output: 32 bytes

**Functions:**

#### GENERATE_PRIVATE()
Generates a new 32-byte private key using CSRNG.

#### DERIVE_PUBLIC(privkey)
Derives the 32-byte public key from the given private key.
- Uses scalar multiplication on Curve25519

#### DH(privkey, pubkey)
Performs Diffie-Hellman key agreement.
- `privkey`: Local 32-byte private key
- `pubkey`: Remote 32-byte public key
- Returns: 32-byte shared secret

**Security Properties:**
- Computational Diffie-Hellman assumption on Curve25519
- Forward secrecy when ephemeral keys are used
- Constant-time implementation required to prevent timing attacks

**References:**
- [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Elliptic Curves for Security

### HKDF

**HMAC-based Key Derivation Function**

Extracts and expands key material from input keying material.

**Parameters:**
- `salt`: 32 bytes maximum (typically 32 bytes for SHA-256)
- `ikm`: Input key material (any length, should have good entropy)
- `info`: Context-specific information (domain separation)
- `n`: Output length in bytes

**Implementation:**

Uses HKDF as specified in RFC 5869 with:
- **Hash Function:** SHA-256
- **HMAC:** As specified in RFC 2104
- **Salt Length:** Maximum 32 bytes (HashLen for SHA-256)

**Usage Pattern:**
```
keys = HKDF(salt, ikm, info, n)
```

**Domain Separation:** The `info` parameter provides cryptographic domain separation between different uses of HKDF in the protocol.

**Verified Info Values:**
- `"ELS2_L1K"` - Layer 1 (outer) encryption
- `"ELS2_L2K"` - Layer 2 (inner) encryption
- `"ELS2_XCA"` - DH client authorization
- `"ELS2PSKA"` - PSK client authorization
- `"i2pblinding1"` - Alpha generation

**References:**
- [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - HKDF Specification
- [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - HMAC Specification

---

## Format Specification

Encrypted LS2 consists of three nested layers:

1. **Layer 0 (Outer):** Plaintext information for storage and retrieval
2. **Layer 1 (Middle):** Client authentication data (encrypted)
3. **Layer 2 (Inner):** Actual LeaseSet2 data (encrypted)

**Overall Structure:**
```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```

**Important:** Encrypted LS2 uses blinded keys. The Destination is not in the header. DHT storage location is `SHA-256(sig type || blinded public key)`, rotated daily.

### Layer 0 (Outer) - Plaintext

Layer 0 does NOT use the standard LS2 header. It has a custom format optimized for blinded keys.

**Structure:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>

**Flags Field (2 bytes, bits 15-0):**
- **Bit 0:** Offline keys indicator
  - `0` = No offline keys
  - `1` = Offline keys present (transient key data follows)
- **Bits 1-15:** Reserved, must be 0 for future compatibility

**Transient Key Data (present if flag bit 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>

**Signature Verification:**
- **Without offline keys:** Verify with blinded public key
- **With offline keys:** Verify with transient public key

The signature covers all data from Type through outerCiphertext (inclusive).

### Layer 1 (Middle) - Client Authorization

**Decryption:** See [Layer 1 Encryption](#layer-1-encryption) section.

**Structure:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>

**Flags Field (1 byte, bits 7-0):**
- **Bit 0:** Authorization mode
  - `0` = No per-client authorization (everybody)
  - `1` = Per-client authorization (auth section follows)
- **Bits 3-1:** Authentication scheme (only if bit 0 = 1)
  - `000` = DH client authentication
  - `001` = PSK client authentication
  - Others reserved
- **Bits 7-4:** Unused, must be 0

**DH Client Authorization Data (flags = 0x01, bits 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>

**authClient Entry (40 bytes):**
- `clientID_i`: 8 bytes
- `clientCookie_i`: 32 bytes (encrypted authCookie)

**PSK Client Authorization Data (flags = 0x03, bits 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>

**authClient Entry (40 bytes):**
- `clientID_i`: 8 bytes
- `clientCookie_i`: 32 bytes (encrypted authCookie)

### Layer 2 (Inner) - LeaseSet Data

**Decryption:** See [Layer 2 Encryption](#layer-2-encryption) section.

**Structure:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>

The inner layer contains the full LeaseSet2 structure including:
- LS2 header
- Lease information
- LS2 signature

**Verification Requirements:**
After decryption, implementations must verify:
1. Inner timestamp matches outer published timestamp
2. Inner expiration matches outer expiration
3. LS2 signature is valid
4. Lease data is well-formed

**References:**
- [Common Structures Specification](/docs/specs/common-structures/) - LeaseSet2 format details

---

## Blinding Key Derivation

### Overview

I2P uses an additive key blinding scheme based on Ed25519 and ZCash RedDSA. Blinded keys are rotated daily (UTC midnight) for forward secrecy.

**Design Rationale:**

I2P explicitly chose NOT to use Tor's rend-spec-v3.txt Appendix A.2 approach. According to the specification:

> "We do not use Tor's rend-spec-v3.txt appendix A.2, which has similar design goals, because its blinded public keys may be off the prime-order subgroup, with unknown security implications."

I2P's additive blinding guarantees that blinded keys remain on the prime-order subgroup of the Ed25519 curve.

### Mathematical Definitions

**Ed25519 Parameters:**
- `B`: Ed25519 base point (generator) = `2^255 - 19`
- `L`: Ed25519 order = `2^252 + 27742317777372353535851937790883648493`

**Key Variables:**
- `A`: Unblinded 32-byte signing public key (in Destination)
- `a`: Unblinded 32-byte signing private key
- `A'`: Blinded 32-byte signing public key (used in encrypted LeaseSet)
- `a'`: Blinded 32-byte signing private key
- `alpha`: 32-byte blinding factor (secret)

**Helper Functions:**

#### LEOS2IP(x)
"Little-Endian Octet String to Integer"

Converts a byte array from little-endian to integer representation.

#### H*(x)
"Hash and Reduce"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```

Same operation as in Ed25519 key generation.

### Alpha Generation

**Daily Rotation:** A new alpha and blinded keys MUST be generated each day at UTC midnight (00:00:00 UTC).

**GENERATE_ALPHA(destination, date, secret) Algorithm:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```

**Parameters Verified:**
- Salt personalization: `"I2PGenerateAlpha"`
- HKDF info: `"i2pblinding1"`
- Output: 64 bytes before reduction
- Alpha distribution: Identically distributed as Ed25519 private keys after `mod L`

### Private Key Blinding

**BLIND_PRIVKEY(a, alpha) Algorithm:**

For the destination owner publishing the encrypted LeaseSet:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```

**Critical:** The `mod L` reduction is essential for maintaining the correct algebraic relationship between private and public keys.

### Public Key Blinding

**BLIND_PUBKEY(A, alpha) Algorithm:**

For clients retrieving and verifying the encrypted LeaseSet:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```

**Mathematical Equivalence:**

Both methods produce identical results:
```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```

This is because:
```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```

### Signing with Blinded Keys

**Unblinded LeaseSet Signing:**

The unblinded LeaseSet (sent directly to authenticated clients) is signed using:
- Standard Ed25519 (type 7) or Red25519 (type 11) signature
- Unblinded signing private key
- Verified with unblinded public key

**With Offline Keys:**
- Signed by unblinded transient private key
- Verified with unblinded transient public key
- Both must be type 7 or 11

**Encrypted LeaseSet Signing:**

The outer portion of encrypted LeaseSet uses Red25519 signatures with blinded keys.

**Red25519 Signing Algorithm:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```

**Key Differences from Ed25519:**
1. Uses 80 bytes of random data `T` (not hash of private key)
2. Uses public key value directly (not hash of private key)
3. Every signature is unique even for same message and key

**Verification:**

Same as Ed25519:
```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```

### Security Considerations

**Alpha Distribution:**

For security, alpha must be identically distributed as unblinded private keys. When blinding Ed25519 (type 7) to Red25519 (type 11), the distributions differ slightly. 

**Recommendation:** Use Red25519 (type 11) for both unblinded and blinded keys to meet ZCash requirements: "the combination of a re-randomized public key and signature(s) under that key do not reveal the key from which it was re-randomized."

**Type 7 Support:** Ed25519 is supported for backward compatibility with existing destinations, but type 11 is recommended for new encrypted destinations.

**Daily Rotation Benefits:**
- Forward secrecy: Compromising today's blinded key doesn't reveal yesterday's
- Unlinkability: Daily rotation prevents long-term tracking via DHT
- Key separation: Different keys for different time periods

**References:**
- [ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf) - Section 5.4.6.1
- [Tor Key Blinding Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
- [Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Encryption and Processing

### Subcredential Derivation

Before encryption, we derive a credential and subcredential to bind encrypted layers to knowledge of the Destination's signing public key.

**Goal:** Ensure only those who know the Destination's signing public key can decrypt the encrypted LeaseSet. The full Destination is not required.

#### Credential Calculation

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```

**Domain Separation:** The personalization string `"credential"` ensures this hash doesn't collide with any DHT lookup keys or other protocol uses.

#### Subcredential Calculation

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```

**Purpose:** The subcredential binds the encrypted LeaseSet to:
1. The specific Destination (via credential)
2. The specific blinded key (via blindedPublicKey)
3. The specific day (via daily rotation of blindedPublicKey)

This prevents replay attacks and cross-day linking.

### Layer 1 Encryption

**Context:** Layer 1 contains client authorization data and is encrypted with a key derived from the subcredential.

#### Encryption Algorithm

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

**Output:** `outerCiphertext` is `32 + len(outerPlaintext)` bytes.

**Security Properties:**
- Salt ensures unique key/IV pairs even with same subcredential
- Context string `"ELS2_L1K"` provides domain separation
- ChaCha20 provides semantic security (ciphertext indistinguishable from random)

#### Decryption Algorithm

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

**Verification:** After decryption, verify Layer 1 structure is well-formed before proceeding to Layer 2.

### Layer 2 Encryption

**Context:** Layer 2 contains the actual LeaseSet2 data and is encrypted with a key derived from the authCookie (if per-client auth enabled) or empty string (if not).

#### Encryption Algorithm

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

**Output:** `innerCiphertext` is `32 + len(innerPlaintext)` bytes.

**Key Binding:**
- If no client auth: Bound only to subcredential and timestamp
- If client auth enabled: Additionally bound to authCookie (different for each authorized client)

#### Decryption Algorithm

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```

**Verification:** After decryption:
1. Verify LS2 type byte is valid (3 or 7)
2. Parse LeaseSet2 structure
3. Verify inner timestamp matches outer published timestamp
4. Verify inner expiration matches outer expiration
5. Verify LeaseSet2 signature

### Encryption Layer Summary

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Decryption Flow:**
1. Verify Layer 0 signature with blinded public key
2. Decrypt Layer 1 using subcredential
3. Process authorization data (if present) to obtain authCookie
4. Decrypt Layer 2 using authCookie and subcredential
5. Verify and parse LeaseSet2

---

## Per-Client Authorization

### Overview

When per-client authorization is enabled, the server maintains a list of authorized clients. Each client has key material that must be securely transmitted out-of-band.

**Two Authorization Mechanisms:**
1. **DH (Diffie-Hellman) Client Authorization:** More secure, uses X25519 key agreement
2. **PSK (Pre-Shared Key) Authorization:** Simpler, uses symmetric keys

**Common Security Properties:**
- Client membership privacy: Observers see client count but cannot identify specific clients
- Anonymous client addition/revocation: Cannot track when specific clients are added or removed
- 8-byte client identifier collision probability: ~1 in 18 quintillion (negligible)

### DH Client Authorization

**Overview:** Each client generates an X25519 keypair and sends their public key to the server via a secure out-of-band channel. The server uses ephemeral DH to encrypt a unique authCookie for each client.

#### Client Key Generation

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```

**Security Advantage:** The client's private key never leaves their device. An adversary intercepting the out-of-band transmission cannot decrypt future encrypted LeaseSets without breaking X25519 DH.

#### Server Processing

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```

**Layer 1 Data Structure:**
```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```

**Server Recommendations:**
- Generate new ephemeral keypair for each published encrypted LeaseSet
- Randomize client order to prevent position-based tracking
- Consider adding dummy entries to hide true client count

#### Client Processing

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```

**Client Error Handling:**
- If `clientID_i` not found: Client has been revoked or never authorized
- If decryption fails: Corrupted data or wrong keys (extremely rare)
- Clients should periodically re-fetch to detect revocation

### PSK Client Authorization

**Overview:** Each client has a pre-shared 32-byte symmetric key. The server encrypts the same authCookie using each client's PSK.

#### Key Generation

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```

**Security Note:** The same PSK can be shared among multiple clients if desired (creates a "group" authorization).

#### Server Processing

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```

**Layer 1 Data Structure:**
```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```

#### Client Processing

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```

### Comparison and Recommendations

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>

**Recommendation:**
- **Use DH authorization** for high-security applications where forward secrecy is important
- **Use PSK authorization** when performance is critical or when managing client groups
- **Never reuse PSKs** across different services or time periods
- **Always use secure channels** for key distribution (e.g., Signal, OTR, PGP)

### Security Considerations

**Client Membership Privacy:**

Both mechanisms provide privacy for client membership through:
1. **Encrypted client identifiers:** 8-byte clientID derived from HKDF output
2. **Indistinguishable cookies:** All 32-byte clientCookie values appear random
3. **No client-specific metadata:** No way to identify which entry belongs to which client

An observer can see:
- Number of authorized clients (from `clients` field)
- Changes in client count over time

An observer CANNOT see:
- Which specific clients are authorized
- When specific clients are added or removed (if count stays same)
- Any client-identifying information

**Randomization Recommendations:**

Servers SHOULD randomize client order each time they generate an encrypted LeaseSet:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```

**Benefits:**
- Prevents clients from learning their position in the list
- Prevents inference attacks based on position changes
- Makes client addition/revocation indistinguishable

**Hiding Client Count:**

Servers MAY insert random dummy entries:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```

**Cost:** Dummy entries increase encrypted LeaseSet size (40 bytes each).

**AuthCookie Rotation:**

Servers SHOULD generate a new authCookie:
- Each time an encrypted LeaseSet is published (every few hours typical)
- Immediately after revoking a client
- On a regular schedule (e.g., daily) even if no client changes

**Benefits:**
- Limits exposure if authCookie is compromised
- Ensures revoked clients lose access quickly
- Provides forward secrecy for Layer 2

---

## Base32 Addressing for Encrypted LeaseSets

### Overview

Traditional I2P base32 addresses contain only the hash of the Destination (32 bytes → 52 characters). This is insufficient for encrypted LeaseSets because:

1. Clients need the **non-blinded public key** to derive the blinded public key
2. Clients need the **signature types** (unblinded and blinded) for proper key derivation
3. The hash alone does not provide this information

**Solution:** A new base32 format that includes the public key and signature types.

### Address Format Specification

**Decoded Structure (35 bytes):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```

**First 3 Bytes (XOR with Checksum):**

The first 3 bytes contain metadata XOR'd with portions of a CRC-32 checksum:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```

**Checksum Properties:**
- Uses standard CRC-32 polynomial
- False negative rate: ~1 in 16 million
- Provides error detection for address typos
- Cannot be used as authentication (not cryptographically secure)

**Encoded Format:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```

**Characteristics:**
- Total characters: 56 (35 bytes × 8 bits ÷ 5 bits per char)
- Suffix: ".b32.i2p" (same as traditional base32)
- Total length: 56 + 8 = 64 characters (excluding null terminator)

**Base32 Encoding:**
- Alphabet: `abcdefghijklmnopqrstuvwxyz234567` (standard RFC 4648)
- 5 unused bits at the end MUST be 0
- Case-insensitive (by convention lowercase)

### Address Generation

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```

### Address Parsing

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```

### Comparison with Traditional Base32

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>

### Usage Restrictions

**BitTorrent Incompatibility:**

Encrypted LS2 addresses CANNOT be used with BitTorrent's compact announce replies:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```

**Problem:** Compact format only contains the hash (32 bytes), with no room for signature types or public key information.

**Solution:** Use full announce replies or HTTP-based trackers that support full addresses.

### Address Book Integration

If a client has the full Destination in an address book:

1. Store full Destination (includes public key)
2. Support reverse lookup by hash
3. When encrypted LS2 is encountered, retrieve public key from address book
4. No need for new base32 format if full Destination already known

**Address book formats that support encrypted LS2:**
- hosts.txt with full destination strings
- SQLite databases with destination column
- JSON/XML formats with full destination data

### Implementation Examples

**Example 1: Generate Address**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```

**Example 2: Parse and Validate**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```

**Example 3: Convert from Destination**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```

### Security Considerations

**Privacy:**
- Base32 address reveals the public key
- This is intentional and required for the protocol
- Does NOT reveal the private key or compromise security
- Public keys are public information by design

**Collision Resistance:**
- CRC-32 provides only 32 bits of collision resistance
- Not cryptographically secure (use only for error detection)
- Do NOT rely on checksum for authentication
- Full destination verification still required

**Address Validation:**
- Always validate checksum before use
- Reject addresses with invalid signature types
- Verify public key is on the curve (implementation specific)

**References:**
- [Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)
- [B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)
- [I2P Naming Specification](/docs/overview/naming/)

---

## Offline Keys Support

### Overview

Offline keys allow the main signing key to remain offline (cold storage) while a transient signing key is used for day-to-day operations. This is critical for high-security services.

**Encrypted LS2 Specific Requirements:**
- Transient keys must be generated offline
- Blinded private keys must be pre-generated (one per day)
- Both transient and blinded keys delivered in batches
- No standardized file format yet defined (TODO in specification)

### Offline Key Structure

**Layer 0 Transient Key Data (when flag bit 0 = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```

**Signature Coverage:**
The signature in the offline key block covers:
- Expires timestamp (4 bytes)
- Transient sig type (2 bytes)  
- Transient signing public key (variable)

This signature is verified using the **blinded public key**, proving that the entity with the blinded private key authorized this transient key.

### Key Generation Process

**For Encrypted LeaseSet with Offline Keys:**

1. **Generate transient keypairs** (offline, in cold storage):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)
       
       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
   # For each day
   for date in future_dates:
       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
   for date in future_dates:
       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
   # For each date
   delivery_package[date] = {
       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
   }
   ```

### Router Usage

**Daily Key Loading:**

```python
# At UTC midnight (or before publishing)
date = datetime.utcnow().date()

# Load keys for today
today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey']
transient_pubkey = today_keys['transient_pubkey']
blinded_privkey = today_keys['blinded_privkey']
blinded_pubkey = today_keys['blinded_pubkey']
offline_sig_block = today_keys['offline_sig_block']

# Use these keys for today's encrypted LeaseSet
```

**Publishing Process:**

```python
# 1. Create inner LeaseSet2
inner_ls2 = create_leaseset2(
    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Encrypt Layer 2
layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Create Layer 1 with authorization data
layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Encrypt Layer 1  
layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Create Layer 0 with offline signature block
layer0 = create_layer0(
    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Sign Layer 0 with transient private key
signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Append signature and publish
encrypted_leaseset = layer0 + signature
publish_to_netdb(encrypted_leaseset)
```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Generate BOTH new transient and new blinded keys each day
for date in future_dates:
    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{
  "version": 1,
  "destination_hash": "base64...",
  "keys": [
    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
  ],
  "signature": "base64..."  // Signature over entire structure
}
```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS
  - Batch of encrypted key material
  - Date range covered

OFFLINE_KEY_STATUS
  - Number of days remaining
  - Next key expiration date

REVOKE_OFFLINE_KEYS  
  - Date range to revoke
  - New keys to replace (optional)
```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)
```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Enable encrypted LeaseSet
i2cp.encryptLeaseSet=true

# Optional: Enable client authorization
i2cp.enableAccessList=true

# Optional: Use DH authorization (default is PSK)
i2cp.accessListType=0

# Optional: Blinding secret (highly recommended)
i2cp.blindingSecret=your-secret-here
```

**API Usage Example:**

```java
// Create encrypted LeaseSet
EncryptedLeaseSet els = new EncryptedLeaseSet();

// Set destination
els.setDestination(destination);

// Enable per-client authorization
els.setAuthorizationEnabled(true);
els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Add authorized clients (DH public keys)
for (byte[] clientPubKey : authorizedClients) {
    els.addClient(clientPubKey);
}

// Set blinding parameters
els.setBlindingSecret("your-secret");

// Sign and publish
els.sign(signingPrivateKey);
netDb.publish(els);
```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service]
type = http
host = 127.0.0.1
port = 8080
keys = my-service-keys.dat

# Enable encrypted LeaseSet
encryptleaseset = true

# Optional: Client authorization type (0=DH, 1=PSK)
authtype = 0

# Optional: Blinding secret
secret = your-secret-here

# Optional: Authorized clients (one per line, base64 encoded public keys)
client.1 = base64-encoded-client-pubkey-1
client.2 = base64-encoded-client-pubkey-2
```

**API Usage Example:**

```cpp
// Create encrypted LeaseSet
auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(
    destination,
    blindingSecret
);

// Enable per-client authorization
encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Add authorized clients
for (const auto& clientPubKey : authorizedClients) {
    encryptedLS->AddClient(clientPubKey);
}

// Sign and publish
encryptedLS->Sign(signingPrivKey);
netdb.Publish(encryptedLS);
```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Test vector 1: Key blinding
destination_pubkey = bytes.fromhex('a' * 64)
sigtype = 7
blinded_sigtype = 11
date = "20251015"
secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret)
print(f"Alpha: {alpha.hex()}")

# Expected: (verify against reference implementation)
```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519 base point (generator)
B = 2**255 - 19

# Ed25519 order (scalar field size)
L = 2**252 + 27742317777372353535851937790883648493

# Signature type values
SIGTYPE_ED25519 = 7    # 0x0007
SIGTYPE_RED25519 = 11  # 0x000b

# Key sizes
PRIVKEY_SIZE = 32  # bytes
PUBKEY_SIZE = 32   # bytes
SIGNATURE_SIZE = 64  # bytes
```

### ChaCha20 Constants

```python
# ChaCha20 parameters
CHACHA20_KEY_SIZE = 32   # bytes (256 bits)
CHACHA20_NONCE_SIZE = 12  # bytes (96 bits)
CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 permits 0 or 1
```

### HKDF Constants

```python
# HKDF parameters
HKDF_HASH = "SHA-256"
HKDF_SALT_MAX = 32  # bytes (HashLen)

# HKDF info strings (domain separation)
HKDF_INFO_ALPHA = b"i2pblinding1"
HKDF_INFO_LAYER1 = b"ELS2_L1K"
HKDF_INFO_LAYER2 = b"ELS2_L2K"
HKDF_INFO_DH_AUTH = b"ELS2_XCA"
HKDF_INFO_PSK_AUTH = b"ELS2PSKA"
```

### Hash Personalization Strings

```python
# SHA-256 personalization strings
HASH_PERS_ALPHA = b"I2PGenerateAlpha"
HASH_PERS_RED25519 = b"I2P_Red25519H(x)"
HASH_PERS_CREDENTIAL = b"credential"
HASH_PERS_SUBCREDENTIAL = b"subcredential"
```

### Structure Sizes

```python
# Layer 0 (outer) sizes
BLINDED_SIGTYPE_SIZE = 2   # bytes
BLINDED_PUBKEY_SIZE = 32   # bytes (for Red25519)
PUBLISHED_TS_SIZE = 4      # bytes
EXPIRES_SIZE = 2           # bytes
FLAGS_SIZE = 2             # bytes
LEN_OUTER_CIPHER_SIZE = 2  # bytes
SIGNATURE_SIZE = 64        # bytes (Red25519)

# Offline key block sizes
OFFLINE_EXPIRES_SIZE = 4   # bytes
OFFLINE_SIGTYPE_SIZE = 2   # bytes
OFFLINE_SIGNATURE_SIZE = 64  # bytes

# Layer 1 (middle) sizes
AUTH_FLAGS_SIZE = 1        # byte
EPHEMERAL_PUBKEY_SIZE = 32  # bytes (DH auth)
AUTH_SALT_SIZE = 32        # bytes (PSK auth)
NUM_CLIENTS_SIZE = 2       # bytes
CLIENT_ID_SIZE = 8         # bytes
CLIENT_COOKIE_SIZE = 32    # bytes
AUTH_CLIENT_ENTRY_SIZE = 40  # bytes (CLIENT_ID + CLIENT_COOKIE)

# Encryption overhead
SALT_SIZE = 32  # bytes (prepended to each encrypted layer)

# Base32 address
B32_ENCRYPTED_DECODED_SIZE = 35  # bytes
B32_ENCRYPTED_ENCODED_LEN = 56   # characters
B32_SUFFIX = ".b32.i2p"
```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Destination public key (Ed25519)
A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
stA = 0x0007  # Ed25519
stA_prime = 0x000b  # Red25519
date = "20251015"
secret = ""  # Empty secret
```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])
# keydata = 36 bytes

salt = SHA256(b"I2PGenerateAlpha" + keydata)
ikm = b"20251015"
info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64)
alpha = LEOS2IP(seed) mod L
```

**Expected Output:**
```
(Verify against reference implementation)
alpha = [64-byte hex value]
```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f
nonce = bytes([i for i in range(12)])  # 0x00..0x0b
plaintext = b"Hello, I2P!"
```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)
```

**Expected Output:**
```
ciphertext = [verify against RFC 7539 test vectors]
```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # All zeros
ikm = b"test input keying material"
info = b"ELS2_L1K"
n = 44
```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)
```

**Expected Output:**
```
keys = [44-byte hex value]
```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bytes
unblinded_sigtype = 11  # Red25519
blinded_sigtype = 11    # Red25519
```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)
```

**Expected Output:**
```
address = [56 base32 characters].b32.i2p
# Verify checksum validates correctly
```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.
