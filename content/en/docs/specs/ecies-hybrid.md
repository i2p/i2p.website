---
title: "ECIES-X25519-AEAD-Ratchet Hybrid Encryption"
description: "Post-quantum hybrid variant of the ECIES encryption protocol using ML-KEM"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Implementation Status

**Current Deployment:**
- **i2pd (C++ implementation)**: Fully implemented in version 2.58.0 (September 2025) with ML-KEM-512, ML-KEM-768, and ML-KEM-1024 support. Post-quantum end-to-end encryption enabled by default when OpenSSL 3.5.0 or later is available.
- **Java I2P**: Not yet implemented as of version 0.9.67 / 2.10.0 (September 2025). Specification approved and implementation planned for future releases.

This specification describes approved functionality that is currently deployed in i2pd and planned for Java I2P implementations.

## Overview

This is the post-quantum hybrid variant of the ECIES-X25519-AEAD-Ratchet protocol [ECIES](/docs/specs/ecies/). It represents the first phase of Proposal 169 [Prop169](/proposals/169-pq-crypto/) to be approved. See that proposal for overall goals, threat models, analysis, alternatives, and additional information.

Proposal 169 status: **Open** (first phase approved for hybrid ECIES implementation).

This specification contains only the differences from standard [ECIES](/docs/specs/ecies/) and must be read in conjunction with that specification.

## Design

We use the NIST FIPS 203 standard [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) which is based on, but not compatible with, CRYSTALS-Kyber (versions 3.1, 3, and older).

Hybrid handshakes combine classical X25519 Diffie-Hellman with post-quantum ML-KEM key encapsulation mechanisms. This approach is based on hybrid forward secrecy concepts documented in PQNoise research and similar implementations in TLS 1.3, IKEv2, and WireGuard.

### Key Exchange

We define a hybrid key exchange for Ratchet. Post-quantum KEM provides ephemeral keys only and does not directly support static-key handshakes such as Noise IK.

We define the three ML-KEM variants as specified in [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), for 3 new encryption types total. Hybrid types are only defined in combination with X25519.

The new encryption types are:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>

**Note:** MLKEM768_X25519 (Type 6) is the recommended default variant, providing strong post-quantum security with reasonable overhead.

Overhead is substantial compared to X25519-only encryption. Typical message 1 and 2 sizes (for IK pattern) are currently around 96-103 bytes (before additional payload). This will increase by approximately 9-12x for MLKEM512, 13-16x for MLKEM768, and 17-23x for MLKEM1024, depending on message type.

### New Crypto Required

- **ML-KEM** (formerly CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Module-Lattice-Based Key-Encapsulation Mechanism Standard
- **SHA3-256** (formerly Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Part of SHA-3 Standard
- **SHAKE128 and SHAKE256** (XOF extensions to SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Extendable-Output Functions

Test vectors for SHA3-256, SHAKE128, and SHAKE256 are available in the [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Library Support:**
- Java: Bouncycastle library version 1.79 and later supports all ML-KEM variants and SHA3/SHAKE functions
- C++: OpenSSL 3.5 and later includes full ML-KEM support (released April 2025)
- Go: Multiple libraries available for ML-KEM and SHA3 implementation

## Specification

### Common Structures

See the [Common Structures Specification](/docs/specs/common-structures/) for key lengths and identifiers.

### Handshake Patterns

Handshakes use [Noise Protocol Framework](https://noiseprotocol.org/noise.html) handshake patterns with I2P-specific adaptations for hybrid post-quantum security.

The following letter mapping is used:

- **e** = one-time ephemeral key (X25519)
- **s** = static key
- **p** = message payload
- **e1** = one-time ephemeral PQ key, sent from Alice to Bob (I2P-specific token)
- **ekem1** = the KEM ciphertext, sent from Bob to Alice (I2P-specific token)

**Important Note:** The pattern names "IKhfs" and "IKhfselg2" and the tokens "e1" and "ekem1" are I2P-specific adaptations not documented in the official Noise Protocol Framework specification. These represent custom definitions for integrating ML-KEM into the Noise IK pattern. While the hybrid X25519 + ML-KEM approach is widely recognized in post-quantum cryptography research and other protocols, the specific nomenclature used here is I2P-specific.

The following modifications to IK for hybrid forward secrecy are applied:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```

The **e1** pattern is defined as follows:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```

The **ekem1** pattern is defined as follows:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```

### Defined ML-KEM Operations

We define the following functions corresponding to the cryptographic building blocks as specified in [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()**
: Alice creates the encapsulation and decapsulation keys. The encapsulation key is sent in the NS message. Key sizes:
  - ML-KEM-512: encap_key = 800 bytes, decap_key = 1632 bytes
  - ML-KEM-768: encap_key = 1184 bytes, decap_key = 2400 bytes
  - ML-KEM-1024: encap_key = 1568 bytes, decap_key = 3168 bytes

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**
: Bob calculates the ciphertext and shared key using the encapsulation key received in the NS message. The ciphertext is sent in the NSR message. Ciphertext sizes:
  - ML-KEM-512: 768 bytes
  - ML-KEM-768: 1088 bytes
  - ML-KEM-1024: 1568 bytes
  
  The kem_shared_key is always **32 bytes** for all three variants.

**kem_shared_key = DECAPS(ciphertext, decap_key)**
: Alice calculates the shared key using the ciphertext received in the NSR message. The kem_shared_key is always **32 bytes**.

**Important:** Both the encap_key and the ciphertext are encrypted inside ChaCha20-Poly1305 blocks in the Noise handshake messages 1 and 2. They will be decrypted as part of the handshake process.

The kem_shared_key is mixed into the chaining key with MixKey(). See below for details.

### Noise Handshake KDF

#### Overview

The hybrid handshake combines classical X25519 ECDH with post-quantum ML-KEM. The first message, from Alice to Bob, contains e1 (the ML-KEM encapsulation key) before the message payload. This is treated as additional key material; call EncryptAndHash() on it (as Alice) or DecryptAndHash() (as Bob). Then process the message payload as usual.

The second message, from Bob to Alice, contains ekem1 (the ML-KEM ciphertext) before the message payload. This is treated as additional key material; call EncryptAndHash() on it (as Bob) or DecryptAndHash() (as Alice). Then calculate the kem_shared_key and call MixKey(kem_shared_key). Then process the message payload as usual.

#### Noise Identifiers

These are the Noise initialization strings (I2P-specific):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### Alice KDF for NS Message

After the 'es' message pattern and before the 's' message pattern, add:

```
This is the "e1" message pattern:
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```

#### Bob KDF for NS Message

After the 'es' message pattern and before the 's' message pattern, add:

```
This is the "e1" message pattern:

// DecryptAndHash(encap_key_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
encap_key = DECRYPT(k, n, encap_key_section, ad)
n++

// MixHash(encap_key_section)
h = SHA256(h || encap_key_section)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```

#### Bob KDF for NSR Message

After the 'ee' message pattern and before the 'se' message pattern, add:

```
This is the "ekem1" message pattern:

(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

// MixKey(kem_shared_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```

#### Alice KDF for NSR Message

After the 'ee' message pattern and before the 'ss' message pattern, add:

```
This is the "ekem1" message pattern:

// DecryptAndHash(kem_ciphertext_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

// MixHash(kem_ciphertext_section)
h = SHA256(h || kem_ciphertext_section)

// MixKey(kem_shared_key)
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```

#### KDF for split()

The split() function remains unchanged from the standard ECIES specification. After handshake completion:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```

These are the bidirectional session keys for ongoing communication.

### Message Format

#### NS (New Session) Format

**Changes:** Current ratchet contains the static key in the first ChaCha20-Poly1305 section and the payload in the second section. With ML-KEM, there are now three sections. The first section contains the encrypted ML-KEM public key (encap_key). The second section contains the static key. The third section contains the payload.

**Message Sizes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>

**Note:** The payload must contain a DateTime block (minimum 7 bytes: 1-byte type, 2-byte size, 4-byte timestamp). The minimum NS sizes may be calculated accordingly. Minimum practical NS size is therefore 103 bytes for X25519 and ranges from 919 to 1687 bytes for hybrid variants.

The size increases of 816, 1200, and 1584 bytes for the three ML-KEM variants account for the ML-KEM public key plus a 16-byte Poly1305 MAC for authenticated encryption.

#### NSR (New Session Reply) Format

**Changes:** Current ratchet has an empty payload for the first ChaCha20-Poly1305 section and the payload in the second section. With ML-KEM, there are now three sections. The first section contains the encrypted ML-KEM ciphertext. The second section has an empty payload. The third section contains the payload.

**Message Sizes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>

The size increases of 784, 1104, and 1584 bytes for the three ML-KEM variants account for the ML-KEM ciphertext plus a 16-byte Poly1305 MAC for authenticated encryption.

## Overhead Analysis

### Key Exchange

The overhead for hybrid encryption is substantial compared to X25519-only:

- **MLKEM512_X25519**: Approximately 9-12x increase in handshake message size (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Approximately 13-16x increase in handshake message size (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Approximately 17-23x increase in handshake message size (NS: 17.5x, NSR: 23x)

This overhead is acceptable for the added post-quantum security benefits. The multipliers vary by message type because base message sizes differ (NS minimum 96 bytes, NSR minimum 72 bytes).

### Bandwidth Considerations

For a typical session establishment with minimal payloads:
- X25519 only: ~200 bytes total (NS + NSR)
- MLKEM512_X25519: ~1,800 bytes total (9x increase)
- MLKEM768_X25519: ~2,500 bytes total (12.5x increase)
- MLKEM1024_X25519: ~3,400 bytes total (17x increase)

After session establishment, ongoing message encryption uses the same data transport format as X25519-only sessions, so there is no overhead for subsequent messages.

## Security Analysis

### Handshakes

The hybrid handshake provides both classical (X25519) and post-quantum (ML-KEM) security. An attacker must break **both** the classical ECDH and the post-quantum KEM to compromise the session keys.

This provides:
- **Current security**: X25519 ECDH provides security against classical attackers (128-bit security level)
- **Future security**: ML-KEM provides security against quantum attackers (varies by parameter set)
- **Hybrid security**: Both must be broken to compromise the session (security level = max of both components)

### Security Levels

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>

**Note:** The hybrid security level is bounded by the weaker of the two components. In all cases, X25519 provides 128-bit classical security. If a cryptographically relevant quantum computer becomes available, the security level would depend on the ML-KEM parameter set chosen.

### Forward Secrecy

The hybrid approach maintains forward secrecy properties. Session keys are derived from both ephemeral X25519 and ephemeral ML-KEM key exchanges. If either the X25519 or ML-KEM ephemeral private keys are destroyed after the handshake, past sessions cannot be decrypted even if long-term static keys are compromised.

The IK pattern provides full forward secrecy (Noise Confidentiality level 5) after the second message (NSR) is sent.

## Type Preferences

Implementations should support multiple hybrid types and negotiate the strongest mutually-supported variant. The preference order should be:

1. **MLKEM768_X25519** (Type 6) - Recommended default, best balance of security and performance
2. **MLKEM1024_X25519** (Type 7) - Highest security for sensitive applications
3. **MLKEM512_X25519** (Type 5) - Baseline post-quantum security for resource-constrained scenarios
4. **X25519** (Type 4) - Classical only, fallback for compatibility

**Rationale:** MLKEM768_X25519 is recommended as the default because it provides NIST Category 3 security (AES-192 equivalent), which is considered sufficient protection against quantum computers while maintaining reasonable message sizes. MLKEM1024_X25519 provides higher security but at substantially increased overhead.

## Implementation Notes

### Library Support

- **Java**: Bouncycastle library version 1.79 (August 2024) and later supports all required ML-KEM variants and SHA3/SHAKE functions. Use `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` for FIPS 203 compliance.
- **C++**: OpenSSL 3.5 (April 2025) and later includes ML-KEM support via EVP_KEM interface. This is a Long Term Support release maintained until April 2030.
- **Go**: Several third-party libraries available for ML-KEM and SHA3, including Cloudflare's CIRCL library.

### Migration Strategy

Implementations should:
1. Support both X25519-only and hybrid ML-KEM variants during transition period
2. Prefer hybrid variants when both peers support them
3. Maintain fallback to X25519-only for backward compatibility
4. Consider network bandwidth constraints when selecting default variant

### Shared Tunnels

The increased message sizes may impact shared tunnel usage. Implementations should consider:
- Batching handshakes when possible to amortize overhead
- Using shorter expiration times for hybrid sessions to reduce stored state
- Monitoring bandwidth usage and adjusting parameters accordingly
- Implementing congestion control for session establishment traffic

### New Session Size Considerations

Due to the larger handshake messages, implementations may need to:
- Increase buffer sizes for session negotiation (minimum 4KB recommended)
- Adjust timeout values for slower connections (account for ~3-17x larger messages)
- Consider compression for payload data in NS/NSR messages
- Implement fragmentation handling if required by transport layer

### Testing and Validation

Implementations should verify:
- Correct ML-KEM key generation, encapsulation, and decapsulation
- Proper integration of kem_shared_key into Noise KDF
- Message size calculations match specification
- Interoperability with other I2P router implementations
- Fallback behavior when ML-KEM not available

Test vectors for ML-KEM operations are available in the NIST [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

## Version Compatibility

**I2P Version Numbering:** I2P maintains two parallel version numbers:
- **Router release version**: 2.x.x format (e.g., 2.10.0 released September 2025)
- **API/protocol version**: 0.9.x format (e.g., 0.9.67 corresponds to router 2.10.0)

This specification references protocol version 0.9.67, which corresponds to router release 2.10.0 and later.

**Compatibility Matrix:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>

## References

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet Specification](/docs/specs/ecies/)
- **[Prop169]**: [Proposal 169: Post-Quantum Cryptography](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM Standard](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3 Standard](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Common Structures Specification](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 and Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM Documentation](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle Java Cryptography Library](https://www.bouncycastle.org/)

---
