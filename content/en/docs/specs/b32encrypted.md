---
title: "B32 for Encrypted Leasesets"
description: "Base 32 address format for encrypted LS2 leasesets"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implemented"
aliases:
  - /en/docs/specs/b32encrypted/
  - /docs/specs/b32-for-encrypted-leasesets/
---

## Overview

Standard Base 32 ("b32") addresses contain the hash of the destination. This will not work for encrypted LS2 (proposal 123).

We cannot use a traditional base 32 address for an encrypted LS2 (proposal 123), as it contains only the hash of the destination. It does not provide the non-blinded public key. Clients must know the destination's public key, signature type, the blinded signature type, and an optional secret or private key to fetch and decrypt the leaseset. Therefore, a base 32 address alone is insufficient. The client needs either the full destination (which contains the public key), or the public key by itself. If the client has the full destination in an address book, and the address book supports reverse lookup by hash, then the public key may be retrieved.

This format puts the public key instead of the hash into a base32 address. This format must also contain the signature type of the public key, and the signature type of the blinding scheme.

This document specifies a b32 format for these addresses. While we have referred to this new format during discussions as a "b33" address, the actual new format retains the usual ".b32.i2p" suffix.

## Implementation Status

Proposal 123 (New netDB Entries) achieved full implementation in version 0.9.43 (October 2019). The encrypted LS2 feature set has remained stable through version 2.10.0 (September 2025) with no breaking changes to the addressing format or cryptographic specifications.

Key implementation milestones:
- 0.9.38: Floodfill support for standard LS2 with offline keys
- 0.9.39: RedDSA signature type 11 and basic encryption/decryption
- 0.9.40: Complete B32 addressing support (Proposal 149)
- 0.9.41: X25519-based per-client authentication
- 0.9.42: All blinding features operational
- 0.9.43: Complete implementation declared (October 2019)

## Design

- New format contains the unblinded public key, unblinded signature type, and blinded signature type.
- Optionally indicates secret and/or private key requirements for private links.
- Uses the existing ".b32.i2p" suffix, but with a longer length.
- Includes a checksum for error detection.
- Addresses for encrypted leasesets are identified by 56 or more encoded characters (35 or more decoded bytes), compared to 52 characters (32 bytes) for traditional base 32 addresses.

## Specification

### Creation and Encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as follows:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```

Post-processing and checksum:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```

Any unused bits at the end of the b32 must be 0. There are no unused bits for a standard 56 character (35 byte) address.

### Decoding and Verification

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients, proxies, or other client-side code that the secret and/or private key will be required to decrypt the leaseset. Particular implementations may prompt the user to supply the required data, or reject connection attempts if the required data is missing.

These bits serve as indicators only. The secret or private key must never be included in the B32 address itself, as that would compromise security.

## Cryptographic Details

### Blinding Scheme

The blinding scheme uses RedDSA based on Ed25519 and ZCash's design, producing Red25519 signatures over the Ed25519 curve using SHA-512. This approach ensures blinded public keys remain on the prime-order subgroup, avoiding the security concerns present in some alternative designs.

Blinded keys rotate daily based on UTC date using the formula:
```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```

The DHT storage location is computed as:
```
SHA256(type_byte || blinded_public_key)
```

### Encryption

The encrypted leaseset uses ChaCha20 stream cipher for encryption, chosen for superior performance on devices lacking AES hardware acceleration. The specification employs HKDF for key derivation and X25519 for Diffie-Hellman operations.

Encrypted leasesets have a three-layer structure:
- Outer layer: plaintext metadata
- Middle layer: client authentication (DH or PSK methods)
- Inner layer: actual LS2 data with lease information

### Authentication Methods

Per-client authentication supports two methods:

**DH Authentication**: Uses X25519 key agreement. Each authorized client provides their public key to the server, and the server encrypts the middle layer using a shared secret derived from ECDH.

**PSK Authentication**: Uses pre-shared keys directly for encryption.

Flag bit 2 in the B32 address indicates whether per-client authentication is required.

## Caching

While outside the scope of this specification, routers and clients must remember and cache (persistently recommended) the mapping of public key to destination, and vice versa.

The blockfile naming service, I2P's default address book system since version 0.9.8, maintains multiple address books with a dedicated reverse-lookup map providing rapid lookups by hash. This functionality is critical for encrypted leaseset resolution when only a hash is initially known.

## Signature Types

As of I2P version 2.10.0, signature types 0 through 11 are defined. Single-byte encoding remains standard, with two-byte encoding available but unused in practice.

**Commonly Used Types:**
- Type 0 (DSA_SHA1): Deprecated for routers, supported for destinations
- Type 7 (EdDSA_SHA512_Ed25519): Current standard for router identities and destinations
- Type 11 (RedDSA_SHA512_Ed25519): Exclusively for encrypted LS2 leasesets with blinding support

**Important Note**: Only Ed25519 (type 7) and Red25519 (type 11) support the blinding necessary for encrypted leasesets. Other signature types cannot be used with this feature.

Types 9-10 (GOST algorithms) remain reserved but unimplemented. Types 4-6 and 8 are marked "offline only" for offline signing keys.

## Notes

- Distinguish old from new flavors by length. Old b32 addresses are always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- The base32 encoding follows RFC 4648 standards with case-insensitive decoding and lowercase output preferred
- Addresses can exceed 200 characters when using signature types with larger public keys (e.g., ECDSA P521 with 132-byte keys)
- New format can be used in jump links (and served by jump servers) if desired, just like standard b32
- Blinded keys rotate daily based on UTC date to enhance privacy
- This format diverges from Tor's rend-spec-v3.txt appendix A.2 approach, which has potential security implications with off-curve blinded public keys

## Version Compatibility

This specification is accurate for I2P version 0.9.47 (August 2020) through version 2.10.0 (September 2025). No breaking changes have occurred to the B32 addressing format, encrypted LS2 structure, or cryptographic implementations during this period. All addresses created with 0.9.47 remain fully compatible with current versions.

## References

**CRC-32**
- [CRC-32 (Wikipedia)](https://en.wikipedia.org/wiki/CRC-32)
- [RFC 3309: Stream Control Transmission Protocol Checksum](https://tools.ietf.org/html/rfc3309)

**I2P Specifications**
- [Encrypted LeaseSet Specification](/docs/specs/encryptedleaseset/)
- [Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)
- [Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)
- [Common Structures Specification](/docs/specs/common-structures/)
- [Naming and Address Book](/docs/overview/naming/)

**Tor Comparison**
- [Tor discussion thread (design context)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Additional Resources**
- [I2P Project](/)
- [I2P Forum](https://i2pforum.net)
- [Java API Documentation](http://docs.i2p-projekt.de/javadoc/)
