---
title: "PQ Hybrid SSU2"
description: "Post-quantum hybrid variant of the SSU2 transport protocol using ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---



### Status

Beta Q2 2026, release Q3 2026


## Overview

This is the hybrid post-quantum variant of the SSU2 transport protocol,
as designed in Proposal 169.
See that proposal for additional background.

PQ Hybrid SSU2 is only defined on the same address and port as standard SSU2.
Operation on a different port, or without standard SSU2 support, is not permitted,
and will not be for several years, when standard SSU2 is deprecated.

This specification documents only the changes required to standard SSU2 to
support PQ Hybrid. See the SSU2 specification for the baseline implementation details.



## Design

We support the NIST FIPS 203 standard [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
which is based on, but NOT compatible with,
CRYSTALS-Kyber.



### Key Exchange

PQ KEM provides ephemeral keys only, and does not directly support
static-key handshakes such as Noise XK and IK.
The encryption types are the same as used in PQ Hybrid Ratchet and are defined
in the common structures document [/docs/specs/common-structures/](/docs/specs/common-structures/),
as in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf),
Hybrid types are only defined in combination with X25519.

The encryption types are:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>


### Legal Combinations

The new encryption types are indicated in the RouterAddresses.
The encryption type in the key certificate will continue to be type 4.



## Specification


### Handshake Patterns

Handshakes use [Noise Protocol](https://noiseprotocol.org/noise.html) handshake patterns.

The following letter mapping is used:

- e = one-time ephemeral key
- s = static key
- p = message payload
- e1 = one-time ephemeral PQ key, sent from Alice to Bob
- ekem1 = the KEM ciphertext, sent from Bob to Alice

The following modifications to XK and IK for hybrid forward secrecy (hfs) are
as specified in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```

The e1 pattern is defined as follows, as specified in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```


The ekem1 pattern is defined as follows, as specified in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```




### Noise Handshake KDF


#### Overview

The hybrid handshake is defined in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).
The first message, from Alice to Bob, contains e1, the encapsulation key, before the message payload.
This is treated as an additional static key; call EncryptAndHash() on it (as Alice)
or DecryptAndHash() (as Bob).
Then process the message payload as usual.

The second message, from Bob to Alice, contains ekem1, the ciphertext, before the message payload.
This is treated as an additional static key; call EncryptAndHash() on it (as Bob)
or DecryptAndHash() (as Alice).
Then, calculate the kem_shared_key and call MixKey(kem_shared_key).
Then process the message payload as usual.


#### Defined ML-KEM Operations

We define the following functions corresponding to the cryptographic building blocks used
as defined in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()
    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Note that both the encap_key and the ciphertext are encrypted inside ChaCha/Poly
blocks in the Noise handshake messages 1 and 2.
They will be decrypted as part of the handshake process.

The kem_shared_key is mixed into the chaining key with MixHash().
See below for details.


#### Alice KDF for Message 1

After the 'es' message pattern and before the payload, add:


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


#### Bob KDF for Message 1

After the 'es' message pattern and before the payload, add:

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


#### Bob KDF for Message 2

For XK: After the 'ee' message pattern and before the payload, add:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```


#### Alice KDF for Message 2

After the 'ee' message pattern, add:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```


#### KDF for Message 3

unchanged


#### KDF for split()

unchanged



### Handshake Details

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Note that MLKEM-1024 is NOT supported for SSU2, as the keys are too large
to fit within a standard 1500 byte datagram.


#### Long Header

The long header is 32 bytes. It is used before a session is created, for Token Request, SessionRequest, SessionCreated, and Retry.
It is also used for out-of-session Peer Test and Hole Punch messages.

In the following messages,
set the ver (version) field in the long header to 3 or 4, to indidate MLKEM-512 or MLKEM-768.

- (0) Session Request
- (1) Session Created
- (9) Retry (note: Retry with Termination may contain any version 2-4)
- (10) Token Request

In the following message,
set the ver (version) field in the long header to any version 2-4, because the choice of version
is Alice's, not Charlie's. Always setting it to 2 is acceptable.
Implementations should accept any value 2-4.

- (11) Hole Punch

In the following message,
set the ver (version) field in the long header to 2, as usual, even if MLKEM-512 or MLKEM-768 is supported.
Implementations may also set the value to 3 or 4, if the other end supports it, but this is not necessary.
Implementations should accept any value 2-4.

- (7) Peer Test (out of session messages 5-7)

Discussion: Setting the version field to 3 or 4 may not be strictly necessary for all message types,
but doing so aids earlier failure detection for unsupported post-quantum connections.
Token Request and Retry (types 9 and 10) should have versions 3/4 for consistency.
Peer Test messages (type 7) is out-of-session and does not indicate intent to
initiate a session.


Before header encryption:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```


#### Short Header

unchanged


#### SessionRequest (Type 0)

Changes: Current SSU2 contains only the block data in a single ChaCha section.
With ML-KEM, there will be a new ChaCha section before the block data, containing the encrypted PQ public key.

KDF Change for Spoof Protection:
To address the issues raised in Proposal 165 [Prop165]_,
but with a different solution, we modify the KDF for Session Request.
This is only for PQ sessions. The KDF for non-PQ sessions remains unchanged.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```



Raw contents:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Unencrypted data (Poly1305 authentication tag not shown):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```

Sizes, not including IP overhead:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |

Note: Type codes are for internal use only. Routers will remain type 4,
and support will be indicated in the router addresses.

Minimum MTU for MLKEM768_X25519:
1318 for IPv4 and 1338 for IPv6. See below.

Maximum size: Use Bob's MTU as published in his RouterInfo, or the default 1500 if not in the RouterInfo.
Do not use MLKEM768_X25519 if the published MTU is too low.



#### SessionCreated (Type 1)

Changes: Current SSU2 contains only the payload in a single ChaCha section.
With ML-KEM, there will be a new ChaCha section before the payload, containing the encrypted PQ ciphertext.


Raw contents:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Unencrypted data (Poly1305 auth tag not shown):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```

Sizes, not including IP overhead:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |

Note: Type codes are for internal use only. Routers will remain type 4,
and support will be indicated in the router addresses.

Minimum MTU for MLKEM768_X25519:
1318 for IPv4 and 1338 for IPv6. See below.

Maximum size: Alice does not yet have Bob's RouterInfo and does not know his published MTU.
For this message, use a temporary MTU as follows.
For MLKEM512_X25519, use the maximum of 1280 or the received SessionRequest size as the MTU.
For MLKEM768_X25519, use the maximum of (1318 for IPv4 or 1338 for IPv6) or the received SessionRequest size as the MTU.
The SessionCreated overhead is smaller than the SessionRequest overhead, because the 
MLKEM ciphertext is smaller than the MLKEM public key.
This allows for a range of padding sizes in SessionCreated even if there were
little or no padding in the SessionRequest.



#### SessionConfirmed (Type 2)

unchanged



#### KDF for data phase

unchanged



#### Relay and Peer Test

The following blocks contain version fields.
They will remain version 2 (for compatibility with a non-PQ Bob),
and will not change to version 3/4 for PQ.
 
- Relay Request
- Relay Response
- Relay Intro
- Peer Test



#### Published Addresses

In all cases, use the SSU2 transport name as usual.
MLKEM-1024 is not supported.

Use the same address/port as non-PQ, non-firewalled.
One or both PQ variants are supported.
In the router address, publish v=2 (as usual) and the new parameter pq=[3|4|3,4|4,3]
to indicate MLKEM 512/768/both.
Routers with a MTU less than the minimum specified below must not publish
a "pq" parameter containing "4".
Publish 4,3 to indicate a preference for MLKEM-768 or 3,4 to indicate
a preference for MLKEM-512. The actual version is up to the initiator,
and the preference may not be honored.
Routers with a MTU less than the minimum specified below must not connect
using MLKEM768.
Older routers will ignore the pq parameter and connect non-pq as usual.

Different address/port as non-PQ, or PQ-only, non-firewalled is NOT supported.
This will not be implemented until non-PQ SSU2 is disabled, several years from now.
When non-PQ is disabled,
one or both PQ variants are supported.
In the router address, publish v=[3|4|3,4|4,3]
to indicate MLKEM 512/768/both.
Older routers will check the v parameter and skip this address as unsupported.

Firewalled addresses (no IP published):
In the router address, publish v=2 (as usual).
The pq parameter MUST be publised in firewalled addresses, to support relay.

Alice may connect to a PQ Bob using the PQ variant that Bob publishes,
whether or not Alice advertises pq support in her router info, or
whether she advertises the same variant.


#### MTU

Use caution not to exceed the MTU with MLKEM768.
The Minimum MTU for MLKEM768_X25519 is 1318 for IPv4 and 1338 for IPv6
(assuming a min payload of 10 bytes with a DateTime and a Padding or RelayTagRequest block).
The minimum MTU for SSU2 in general is 1280, so not all peers may use MLKEM768.
Do not publish or use MLKEM768 if the actual MTU is less than the minimum,
either locally or as advertised by the peer.
Take care not to include padding size such that message 1 or 2 would exceed
the local or remote MTU.




## Overhead Analysis

### Key Exchange

Size increase (bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>


## Security Analysis

NIST security categories are summarized in [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10.
Preliminary criteria:
Our minimum NIST security category should be 2 for hybrid protocols
and 3 for PQ-only.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>


### Handshakes
These are all hybrid protocols.
Implementations should prefer MLKEM768; MLKEM512 is not secure enough.

NIST security categories [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>



## Implementation Notes

### Library Support

Bouncycastle, BoringSSL, and WolfSSL libraries support MLKEM and MLDSA now.
OpenSSL support is be in their 3.5 release April 8, 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).


### Inbound Traffic Identification

The version field in the long header of the Session Request message
is 2 for non-PQ, 3 for MLKEM-512, and 4 for MLKEM-768.
This allows us to run both standard SSU2 and hybrid SSU2
on the same port, and support both MLKEM variants at once.


## Router Compatibility

### Transport Names

In all cases, use the SSU2 transport name as usual.
Older routers will ignore the pq parameter and connect with standard SSU2 as usual.



## References

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
