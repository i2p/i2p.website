---
title: "NTCP2 Transport"
description: "Noise-based TCP transport for router-to-router links"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Overview

NTCP2 replaces the legacy NTCP transport with a Noise-based handshake that resists traffic fingerprinting, encrypts length fields, and supports modern cipher suites. Routers may run NTCP2 alongside SSU2 as the two mandatory transport protocols in the I2P network. NTCP (version 1) was deprecated in 0.9.40 (May 2019) and completely removed in 0.9.50 (May 2021).

## Noise Protocol Framework

NTCP2 uses the Noise Protocol Framework [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) with I2P-specific extensions:

- **Pattern**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Extended Identifier**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (for KDF initialization)
- **DH Function**: X25519 (RFC 7748) - 32-byte keys, little-endian encoding
- **Cipher**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12-byte nonce: first 4 bytes zero, last 8 bytes counter (little-endian)
  - Maximum nonce value: 2^64 - 2 (connection must terminate before reaching 2^64 - 1)
- **Hash Function**: SHA-256 (32-byte output)
- **MAC**: Poly1305 (16-byte authentication tag)

### I2P-Specific Extensions

1. **AES Obfuscation**: Ephemeral keys encrypted with AES-256-CBC using Bob's router hash and published IV
2. **Random Padding**: Cleartext padding in messages 1-2 (authenticated), AEAD padding in message 3+ (encrypted)
3. **SipHash-2-4 Length Obfuscation**: Two-byte frame lengths XORed with SipHash output
4. **Frame Structure**: Length-prefixed frames for data phase (TCP streaming compatibility)
5. **Block-Based Payloads**: Structured data format with typed blocks

## Handshake Flow

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```

### Three-Message Handshake

1. **SessionRequest** - Alice's obfuscated ephemeral key, options, padding hints
2. **SessionCreated** - Bob's obfuscated ephemeral key, encrypted options, padding
3. **SessionConfirmed** - Alice's encrypted static key and RouterInfo (two AEAD frames)

### Noise Message Patterns

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```

**Authentication Levels:**
- 0: No authentication (any party could have sent)
- 2: Sender authentication resistant to key-compromise impersonation (KCI)

**Confidentiality Levels:**
- 1: Ephemeral recipient (forward secrecy, no recipient authentication)
- 2: Known recipient, forward secrecy for sender compromise only
- 5: Strong forward secrecy (ephemeral-ephemeral + ephemeral-static DH)

## Message Specifications

### Key Notation

- `RH_A` = Router Hash for Alice (32 bytes, SHA-256)
- `RH_B` = Router Hash for Bob (32 bytes, SHA-256)
- `||` = Concatenation operator
- `byte(n)` = Single byte with value n
- All multi-byte integers are **big-endian** unless specified otherwise
- X25519 keys are **little-endian** (32 bytes)

### Authenticated Encryption (ChaCha20-Poly1305)

**Encryption Function:**
```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```

**Parameters:**
- `key`: 32-byte cipher key from KDF
- `nonce`: 12 bytes (4 zero bytes + 8-byte counter, little-endian)
- `associatedData`: 32-byte hash in handshake phase; zero-length in data phase
- `plaintext`: Data to encrypt (0+ bytes)

**Output:**
- Ciphertext: Same length as plaintext
- MAC: 16 bytes (Poly1305 authentication tag)

**Nonce Management:**
- Counter starts at 0 for each cipher instance
- Increments for each AEAD operation in that direction
- Separate counters for Alice→Bob and Bob→Alice in data phase
- Must terminate connection before counter reaches 2^64 - 1

## Message 1: SessionRequest

Alice initiates connection to Bob.

**Noise Operations**: `e, es` (ephemeral key generation and exchange)

### Raw Format

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

**Size Constraints:**
- Minimum: 80 bytes (32 AES + 48 AEAD)
- Maximum: 65535 bytes total
- **Special case**: Max 287 bytes when connecting to "NTCP" addresses (version detection)

### Decrypted Content

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

### Options Block (16 bytes, big-endian)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```

**Critical Fields:**
- **Network ID** (since 0.9.42): Fast rejection of cross-network connections
- **m3p2len**: Exact size of message 3 part 2 (must match when sent)

### Key Derivation Function (KDF-1)

**Initialize Protocol:**
```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```

**MixHash Operations:**
```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```

**MixKey Operation (es pattern):**
```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```

### Implementation Notes

1. **AES Obfuscation**: Used for DPI resistance only; anyone with Bob's router hash and IV can decrypt X
2. **Replay Prevention**: Bob must cache X values (or encrypted equivalents) for at least 2*D seconds (D = max clock skew)
3. **Timestamp Validation**: Bob must reject connections with |tsA - current_time| > D (typically D = 60 seconds)
4. **Curve Validation**: Bob must verify X is a valid X25519 point
5. **Fast Rejection**: Bob may check X[31] & 0x80 == 0 before decryption (valid X25519 keys have MSB clear)
6. **Error Handling**: On any failure, Bob closes with TCP RST after random timeout and random byte read
7. **Buffering**: Alice must flush entire message (including padding) at once for efficiency

## Message 2: SessionCreated

Bob responds to Alice.

**Noise Operations**: `e, ee` (ephemeral-ephemeral DH)

### Raw Format

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

### Decrypted Content

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

### Options Block (16 bytes, big-endian)

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```

### Key Derivation Function (KDF-2)

**MixHash Operations:**
```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```

**MixKey Operation (ee pattern):**
```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```

**Memory Cleanup:**
```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```

### Implementation Notes

1. **AES Chaining**: Y encryption uses AES-CBC state from message 1 (not reset)
2. **Replay Prevention**: Alice must cache Y values for at least 2*D seconds
3. **Timestamp Validation**: Alice must reject |tsB - current_time| > D
4. **Curve Validation**: Alice must verify Y is a valid X25519 point
5. **Error Handling**: Alice closes with TCP RST on any failure
6. **Buffering**: Bob must flush entire message at once

## Message 3: SessionConfirmed

Alice confirms session and sends RouterInfo.

**Noise Operations**: `s, se` (static key reveal and static-ephemeral DH)

### Two-Part Structure

Message 3 consists of **two separate AEAD frames**:

1. **Part 1**: Fixed 48-byte frame with Alice's encrypted static key
2. **Part 2**: Variable-length frame with RouterInfo, options, and padding

### Raw Format

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

**Size Constraints:**
- Part 1: Exactly 48 bytes (32 plaintext + 16 MAC)
- Part 2: Length specified in message 1 (m3p2len field)
- Total maximum: 65535 bytes (part 1 max 48, so part 2 max 65487)

### Decrypted Content

**Part 1:**
```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```

**Part 2:**
```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```

### Key Derivation Function (KDF-3)

**Part 1 (s pattern):**
```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```

**Part 2 (se pattern):**
```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```

**Memory Cleanup:**
```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```

### Implementation Notes

1. **RouterInfo Validation**: Bob must verify signature, timestamp, and key consistency
2. **Key Matching**: Bob must verify Alice's static key in part 1 matches the key in RouterInfo
3. **Static Key Location**: Look for matching "s" parameter in NTCP or NTCP2 RouterAddress
4. **Block Order**: RouterInfo must be first, Options second (if present), Padding last (if present)
5. **Length Planning**: Alice must ensure m3p2len in message 1 exactly matches part 2 length
6. **Buffering**: Alice must flush both parts together as one TCP send
7. **Optional Chaining**: Alice may append a data phase frame immediately for efficiency

## Data Phase

After handshake completion, all messages use variable-length AEAD frames with obfuscated length fields.

### Key Derivation Function (Data Phase)

**Split Function (Noise):**
```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```

**SipHash Key Derivation:**
```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```

### Frame Structure

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```

**Frame Constraints:**
- Minimum: 18 bytes (2 obfuscated length + 0 plaintext + 16 MAC)
- Maximum: 65537 bytes (2 obfuscated length + 65535 frame)
- Recommended: Few KB per frame (minimize receiver latency)

### SipHash Length Obfuscation

**Purpose**: Prevent DPI identification of frame boundaries

**Algorithm:**
```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```

**Decoding:**
```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```

**Notes:**
- Separate IV chains for each direction (Alice→Bob and Bob→Alice)
- If SipHash returns uint64, use least significant 2 bytes as mask
- Convert uint64 to next IV as little-endian bytes

### Block Format

Each frame contains zero or more blocks:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```

**Size Limits:**
- Maximum frame: 65535 bytes (including MAC)
- Maximum block space: 65519 bytes (frame - 16-byte MAC)
- Maximum single block: 65519 bytes (3-byte header + 65516 data)

### Block Types

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>

**Block Ordering Rules:**
- **Message 3 part 2**: RouterInfo, Options (optional), Padding (optional) - NO other types
- **Data phase**: Any order except:
  - Padding MUST be last block if present
  - Termination MUST be last block (except Padding) if present
- Multiple I2NP blocks allowed per frame
- Multiple Padding blocks NOT allowed per frame

### Block Type 0: DateTime

Time synchronization for clock skew detection.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```

**Implementation**: Round to nearest second to prevent clock bias accumulation.

### Block Type 1: Options

Padding and traffic shaping parameters.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```

**Padding Ratios** (4.4 fixed-point float, value/16.0):
- `tmin`: Transmit minimum padding ratio (0.0 - 15.9375)
- `tmax`: Transmit maximum padding ratio (0.0 - 15.9375)
- `rmin`: Receive minimum padding ratio (0.0 - 15.9375)
- `rmax`: Receive maximum padding ratio (0.0 - 15.9375)

**Examples:**
- 0x00 = 0% padding
- 0x01 = 6.25% padding
- 0x10 = 100% padding (1:1 ratio)
- 0x80 = 800% padding (8:1 ratio)

**Dummy Traffic:**
- `tdmy`: Max willing to send (2 bytes, bytes/sec average)
- `rdmy`: Requested to receive (2 bytes, bytes/sec average)

**Delay Insertion:**
- `tdelay`: Max willing to insert (2 bytes, milliseconds average)
- `rdelay`: Requested delay (2 bytes, milliseconds average)

**Guidelines:**
- Min values indicate desired traffic analysis resistance
- Max values indicate bandwidth constraints
- Sender should honor receiver's maximum
- Sender may honor receiver's minimum within constraints
- No enforcement mechanism; implementations may vary

### Block Type 2: RouterInfo

RouterInfo delivery for netdb population and flooding.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```

**Usage:**

**In Message 3 Part 2** (handshake):
- Alice sends her RouterInfo to Bob
- Flood bit typically 0 (local storage)
- RouterInfo NOT gzip compressed

**In Data Phase:**
- Either party may send their updated RouterInfo
- Flood bit = 1: Request floodfill distribution (if receiver is floodfill)
- Flood bit = 0: Local netdb storage only

**Validation Requirements:**
1. Verify signature type is supported
2. Verify RouterInfo signature
3. Verify timestamp within acceptable bounds
4. For handshake: Verify static key matches NTCP2 address "s" parameter
5. For data phase: Verify router hash matches session peer
6. Only flood RouterInfos with published addresses

**Notes:**
- No ACK mechanism (use I2NP DatabaseStore with reply token if needed)
- May contain third-party RouterInfos (floodfill usage)
- NOT gzip compressed (unlike I2NP DatabaseStore)

### Block Type 3: I2NP Message

I2NP message with shortened 9-byte header.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```

**Differences from NTCP1:**
- Expiration: 4 bytes (seconds) vs 8 bytes (milliseconds)
- Length: Omitted (derivable from block length)
- Checksum: Omitted (AEAD provides integrity)
- Header: 9 bytes vs 16 bytes (44% reduction)

**Fragmentation:**
- I2NP messages MUST NOT be fragmented across blocks
- I2NP messages MUST NOT be fragmented across frames
- Multiple I2NP blocks allowed per frame

### Block Type 4: Termination

Explicit connection close with reason code.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```

**Reason Codes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>

**Rules:**
- Termination MUST be last non-padding block in frame
- One termination block per frame maximum
- Sender should close connection after sending
- Receiver should close connection after receiving

**Error Handling:**
- Handshake errors: Typically close with TCP RST (no termination block)
- Data phase AEAD errors: Random timeout + random read, then send termination
- See "AEAD Error Handling" section for security procedures

### Block Type 254: Padding

Random padding for traffic analysis resistance.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```

**Rules:**
- Padding MUST be last block in frame if present
- Zero-length padding is allowed
- Only one padding block per frame
- Padding-only frames are allowed
- Should adhere to negotiated parameters from Options block

**Padding in Messages 1-2:**
- Outside AEAD frame (cleartext)
- Included in next message's hash chain (authenticated)
- Tampering detected when next message AEAD fails

**Padding in Message 3+ and Data Phase:**
- Inside AEAD frame (encrypted and authenticated)
- Used for traffic shaping and size obfuscation

## AEAD Error Handling

**Critical Security Requirements:**

### Handshake Phase (Messages 1-3)

**Known Message Size:**
- Message sizes are predetermined or specified in advance
- AEAD authentication failure is unambiguous

**Bob's Response to Message 1 Failure:**
1. Set random timeout (range implementation-dependent, suggest 100-500ms)
2. Read random number of bytes (range implementation-dependent, suggest 1KB-64KB)
3. Close connection with TCP RST (no response)
4. Blacklist source IP temporarily
5. Track repeated failures for long-term bans

**Alice's Response to Message 2 Failure:**
1. Close connection immediately with TCP RST
2. No response to Bob

**Bob's Response to Message 3 Failure:**
1. Close connection immediately with TCP RST
2. No response to Alice

### Data Phase

**Obfuscated Message Size:**
- Length field is SipHash-obfuscated
- Invalid length or AEAD failure could indicate:
  - Attacker probing
  - Network corruption
  - Desynchronized SipHash IV
  - Malicious peer

**Response to AEAD or Length Error:**
1. Set random timeout (suggest 100-500ms)
2. Read random number of bytes (suggest 1KB-64KB)
3. Send termination block with reason code 4 (AEAD failure) or 9 (framing error)
4. Close connection

**Prevention of Decryption Oracle:**
- Never reveal error type to peer before random timeout
- Never skip length validation before AEAD check
- Treat invalid length same as AEAD failure
- Use identical error handling path for both errors

**Implementation Considerations:**
- Some implementations may continue after AEAD errors if infrequent
- Terminate after repeated errors (suggest threshold: 3-5 errors per hour)
- Balance between error recovery and security

## Published RouterInfo

### Router Address Format

NTCP2 support is advertised through published RouterAddress entries with specific options.

**Transport Style:**
- `"NTCP2"` - NTCP2 only on this port
- `"NTCP"` - Both NTCP and NTCP2 on this port (auto-detect)
  - **Note**: NTCP (v1) support removed in 0.9.50 (May 2021)
  - "NTCP" style is now obsolete; use "NTCP2"

### Required Options

**All Published NTCP2 Addresses:**

1. **`host`** - IP address (IPv4 or IPv6) or hostname
   - Format: Standard IP notation or domain name
   - May be omitted for outbound-only or hidden routers

2. **`port`** - TCP port number
   - Format: Integer, 1-65535
   - May be omitted for outbound-only or hidden routers

3. **`s`** - Static public key (X25519)
   - Format: Base64-encoded, 44 characters
   - Encoding: I2P Base64 alphabet
   - Source: 32-byte X25519 public key, little-endian

4. **`i`** - Initialization Vector for AES
   - Format: Base64-encoded, 24 characters
   - Encoding: I2P Base64 alphabet
   - Source: 16-byte IV, big-endian

5. **`v`** - Protocol version
   - Format: Integer or comma-separated integers
   - Current: `"2"`
   - Future: `"2,3"` (must be in numerical order)

**Optional Options:**

6. **`caps`** - Capabilities (since 0.9.50)
   - Format: String of capability characters
   - Values:
     - `"4"` - IPv4 outbound capability
     - `"6"` - IPv6 outbound capability
     - `"46"` - Both IPv4 and IPv6 (recommended order)
   - Not needed if `host` is published
   - Useful for hidden/firewalled routers

7. **`cost`** - Address priority
   - Format: Integer, 0-255
   - Lower values = higher priority
   - Suggested: 5-10 for normal addresses
   - Suggested: 14 for unpublished addresses

### Example RouterAddress Entries

**Published IPv4 Address:**
```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```

**Hidden Router (Outbound Only):**
```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```

**Dual-Stack Router:**
```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```

**Important Rules:**
- Multiple NTCP2 addresses with the **same port** MUST use **identical** `s`, `i`, and `v` values
- Different ports may use different keys
- Dual-stack routers should publish separate IPv4 and IPv6 addresses

### Unpublished NTCP2 Address

**For Outbound-Only Routers:**

If a router does not accept incoming NTCP2 connections but initiates outbound connections, it MUST still publish a RouterAddress with:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```

**Purpose:**
- Allows Bob to validate Alice's static key during handshake
- Required for message 3 part 2 RouterInfo verification
- No `i`, `host`, or `port` needed (outbound only)

**Alternative:**
- Add `s` and `v` to existing published "NTCP" or SSU address

### Public Key and IV Rotation

**Critical Security Policy:**

**General Rules:**
1. **Never rotate while router is running**
2. **Persistently store key and IV** across restarts
3. **Track previous downtime** to determine rotation eligibility

**Minimum Downtime Before Rotation:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>

**Additional Triggers:**
- Local IP address change: May rotate regardless of downtime
- Router "rekey" (new Router Hash): Generate new keys

**Rationale:**
- Prevents exposing restart times through key changes
- Allows cached RouterInfos to expire naturally
- Maintains network stability
- Reduces failed connection attempts

**Implementation:**
1. Store key, IV, and last-shutdown timestamp persistently
2. At startup, calculate downtime = current_time - last_shutdown
3. If downtime > minimum for router type, may rotate
4. If IP changed or rekeying, may rotate
5. Otherwise, reuse previous key and IV

**IV Rotation:**
- Subject to identical rules as key rotation
- Only present in published addresses (not hidden routers)
- Recommended to change IV whenever key changes

## Version Detection

**Context:** When `transportStyle="NTCP"` (legacy), Bob supports both NTCP v1 and v2 on the same port and must automatically detect the protocol version.

**Detection Algorithm:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```

**Fast MSB Check:**
- Before AES decryption, verify: `encrypted_X[31] & 0x80 == 0`
- Valid X25519 keys have high bit clear
- Failure indicates likely NTCP1 (or attack)
- Implement probing resistance (random timeout + read) on failure

**Implementation Requirements:**

1. **Alice's Responsibility:**
   - When connecting to "NTCP" address, limit message 1 to 287 bytes max
   - Buffer and flush entire message 1 at once
   - Increases likelihood of single TCP packet delivery

2. **Bob's Responsibility:**
   - Buffer received data before deciding version
   - Implement proper timeout handling
   - Use TCP_NODELAY for rapid version detection
   - Buffer and flush entire message 2 at once after version detected

**Security Considerations:**
- Segmentation attacks: Bob should be resilient to TCP segmentation
- Probing attacks: Implement random delays and byte reads on failures
- DoS prevention: Limit concurrent pending connections
- Read timeouts: Both per-read and total ("slowloris" protection)

## Clock Skew Guidelines

**Timestamp Fields:**
- Message 1: `tsA` (Alice's timestamp)
- Message 2: `tsB` (Bob's timestamp)
- Message 3+: Optional DateTime blocks

**Maximum Skew (D):**
- Typical: **±60 seconds**
- Configurable per implementation
- Skew > D is generally fatal

### Bob's Handling (Message 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```

**Rationale:** Sending message 2 even on skew allows Alice to diagnose clock issues.

### Alice's Handling (Message 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```

**RTT Adjustment:**
- Subtract half RTT from calculated skew
- Accounts for network propagation delay
- More accurate skew estimation

### Bob's Handling (Message 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```

### Time Synchronization

**DateTime Blocks (Data Phase):**
- Periodically send DateTime block (type 0)
- Receiver can use for clock adjustment
- Round timestamp to nearest second (prevent bias)

**External Time Sources:**
- NTP (Network Time Protocol)
- System clock synchronization
- I2P network consensus time

**Clock Adjustment Strategies:**
- If local clock bad: Adjust system time or use offset
- If peer clocks consistently bad: Flag peer issue
- Track skew statistics for network health monitoring

## Security Properties

### Forward Secrecy

**Achieved Through:**
- Ephemeral Diffie-Hellman key exchange (X25519)
- Three DH operations: es, ee, se (Noise XK pattern)
- Ephemeral keys destroyed after handshake completion

**Confidentiality Progression:**
- Message 1: Level 2 (forward secrecy for sender compromise)
- Message 2: Level 1 (ephemeral recipient)
- Message 3+: Level 5 (strong forward secrecy)

**Perfect Forward Secrecy:**
- Compromise of long-term static keys does NOT reveal past session keys
- Each session uses unique ephemeral keys
- Ephemeral private keys never reused
- Memory cleanup after key agreement

**Limitations:**
- Message 1 vulnerable if Bob's static key compromised (but forward secrecy from Alice compromise)
- Replay attacks possible for message 1 (mitigated by timestamp and replay cache)

### Authentication

**Mutual Authentication:**
- Alice authenticated by static key in message 3
- Bob authenticated by possession of static private key (implicit from successful handshake)

**Key Compromise Impersonation (KCI) Resistance:**
- Authentication level 2 (resistant to KCI)
- Attacker cannot impersonate Alice even with Alice's static private key (without Alice's ephemeral key)
- Attacker cannot impersonate Bob even with Bob's static private key (without Bob's ephemeral key)

**Static Key Verification:**
- Alice knows Bob's static key in advance (from RouterInfo)
- Bob verifies Alice's static key matches RouterInfo in message 3
- Prevents man-in-the-middle attacks

### Resistance to Traffic Analysis

**DPI Countermeasures:**
1. **AES Obfuscation:** Ephemeral keys encrypted, appears random
2. **SipHash Length Obfuscation:** Frame lengths not plaintext
3. **Random Padding:** Variable message sizes, no fixed patterns
4. **Encrypted Frames:** All payload encrypted with ChaCha20

**Replay Attack Prevention:**
- Timestamp validation (±60 seconds)
- Replay cache of ephemeral keys (lifetime 2*D)
- Nonce increments prevent packet replay within session

**Probing Resistance:**
- Random timeouts on AEAD failures
- Random byte reads before connection close
- No responses on handshake failures
- IP blacklisting for repeated failures

**Padding Guidelines:**
- Messages 1-2: Cleartext padding (authenticated)
- Message 3+: Encrypted padding inside AEAD frames
- Negotiated padding parameters (Options block)
- Padding-only frames permitted

### Denial of Service Mitigation

**Connection Limits:**
- Maximum active connections (implementation-dependent)
- Maximum pending handshakes (e.g., 100-1000)
- Per-IP connection limits (e.g., 3-10 simultaneous)

**Resource Protection:**
- DH operations rate-limited (expensive)
- Read timeouts per-socket and total
- "Slowloris" protection (total time limits)
- IP blacklisting for abuse

**Fast Rejection:**
- Network ID mismatch → immediate close
- Invalid X25519 point → fast MSB check before decryption
- Timestamp out of bounds → close without computation
- AEAD failure → no response, random delay

**Probing Resistance:**
- Random timeout: 100-500ms (implementation-dependent)
- Random read: 1KB-64KB (implementation-dependent)
- No error information to attacker
- Close with TCP RST (no FIN handshake)

### Cryptographic Security

**Algorithms:**
- **X25519**: 128-bit security, elliptic curve DH (Curve25519)
- **ChaCha20**: 256-bit key stream cipher
- **Poly1305**: Information-theoretically secure MAC
- **SHA-256**: 128-bit collision resistance, 256-bit preimage resistance
- **HMAC-SHA256**: PRF for key derivation

**Key Sizes:**
- Static keys: 32 bytes (256 bits)
- Ephemeral keys: 32 bytes (256 bits)
- Cipher keys: 32 bytes (256 bits)
- MAC: 16 bytes (128 bits)

**Known Issues:**
- ChaCha20 nonce reuse is catastrophic (prevented by counter increment)
- X25519 has small subgroup issues (mitigated by curve validation)
- SHA-256 theoretically vulnerable to length extension (not exploitable in HMAC)

**No Known Vulnerabilities (as of October 2025):**
- Noise Protocol Framework widely analyzed
- ChaCha20-Poly1305 deployed in TLS 1.3
- X25519 standard in modern protocols
- No practical attacks on construction

## References

### Primary Specifications

- **[NTCP2 Specification](/docs/specs/ntcp2/)** - Official I2P specification
- **[Proposal 111](/proposals/111-ntcp-2/)** - Original design document with rationale
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Revision 33 (2017-10-04)

### Cryptographic Standards

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Elliptic Curves for Security (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (obsoletes RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 for hash function applications

### Related I2P Specifications

- **[I2NP Specification](/docs/specs/i2np/)** - I2P Network Protocol message format
- **[Common Structures](/docs/specs/common-structures/)** - RouterInfo, RouterAddress formats
- **[SSU Transport](/docs/legacy/ssu/)** - UDP transport (original, now SSU2)
- **[Proposal 147](/proposals/147-transport-network-id-check/)** - Transport Network ID Check (0.9.42)

### Implementation References

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Reference implementation (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Release Notes](/blog/)** - Version history and updates

### Historical Context

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Inspiration for Noise framework
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (SipHash length obfuscation precedent)

## Implementation Guidelines

### Mandatory Requirements

**For Compliance:**

1. **Implement Complete Handshake:**
   - Support all three messages with correct KDF chains
   - Validate all AEAD tags
   - Verify X25519 points are valid

2. **Implement Data Phase:**
   - SipHash length obfuscation (both directions)
   - All block types: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Proper nonce management (separate counters)

3. **Security Features:**
   - Replay prevention (cache ephemeral keys for 2*D)
   - Timestamp validation (±60 seconds default)
   - Random padding in messages 1-2
   - AEAD error handling with random timeouts

4. **RouterInfo Publishing:**
   - Publish static key ("s"), IV ("i"), and version ("v")
   - Rotate keys according to policy
   - Support capabilities field ("caps") for hidden routers

5. **Network Compatibility:**
   - Support network ID field (currently 2 for mainnet)
   - Interoperate with existing Java and i2pd implementations
   - Handle both IPv4 and IPv6

### Recommended Practices

**Performance Optimization:**

1. **Buffering Strategy:**
   - Flush entire messages at once (messages 1, 2, 3)
   - Use TCP_NODELAY for handshake messages
   - Buffer multiple data blocks into single frames
   - Limit frame size to few KB (minimize receiver latency)

2. **Connection Management:**
   - Reuse connections when possible
   - Implement connection pooling
   - Monitor connection health (DateTime blocks)

3. **Memory Management:**
   - Zero sensitive data after use (ephemeral keys, DH results)
   - Limit concurrent handshakes (DoS prevention)
   - Use memory pools for frequent allocations

**Security Hardening:**

1. **Probing Resistance:**
   - Random timeouts: 100-500ms
   - Random byte reads: 1KB-64KB
   - IP blacklisting for repeated failures
   - No error details to peers

2. **Resource Limits:**
   - Max connections per IP: 3-10
   - Max pending handshakes: 100-1000
   - Read timeouts: 30-60 seconds per operation
   - Total connection timeout: 5 minutes for handshake

3. **Key Management:**
   - Persistent storage of static key and IV
   - Secure random generation (cryptographic RNG)
   - Follow rotation policies strictly
   - Never reuse ephemeral keys

**Monitoring and Diagnostics:**

1. **Metrics:**
   - Handshake success/failure rates
   - AEAD error rates
   - Clock skew distribution
   - Connection duration statistics

2. **Logging:**
   - Log handshake failures with reason codes
   - Log clock skew events
   - Log banned IPs
   - Never log sensitive key material

3. **Testing:**
   - Unit tests for KDF chains
   - Integration tests with other implementations
   - Fuzzing for packet handling
   - Load testing for DoS resistance

### Common Pitfalls

**Critical Errors to Avoid:**

1. **Nonce Reuse:**
   - Never reset nonce counter mid-session
   - Use separate counters for each direction
   - Terminate before reaching 2^64 - 1

2. **Key Rotation:**
   - Never rotate keys while router is running
   - Never reuse ephemeral keys across sessions
   - Follow minimum downtime rules

3. **Timestamp Handling:**
   - Never accept expired timestamps
   - Always adjust for RTT when calculating skew
   - Round DateTime timestamps to seconds

4. **AEAD Errors:**
   - Never reveal error type to attacker
   - Always use random timeout before closing
   - Treat invalid length same as AEAD failure

5. **Padding:**
   - Never send padding outside negotiated bounds
   - Always place padding block last
   - Never multiple padding blocks per frame

6. **RouterInfo:**
   - Always verify static key matches RouterInfo
   - Never flood RouterInfos without published addresses
   - Always validate signatures

### Testing Methodology

**Unit Tests:**

1. **Cryptographic Primitives:**
   - Test vectors for X25519, ChaCha20, Poly1305, SHA-256
   - HMAC-SHA256 test vectors
   - SipHash-2-4 test vectors

2. **KDF Chains:**
   - Known-answer tests for all three messages
   - Verify chaining key propagation
   - Test SipHash IV generation

3. **Message Parsing:**
   - Valid message decoding
   - Invalid message rejection
   - Boundary conditions (empty, maximum size)

**Integration Tests:**

1. **Handshake:**
   - Successful three-message exchange
   - Clock skew rejection
   - Replay attack detection
   - Invalid key rejection

2. **Data Phase:**
   - I2NP message transfer
   - RouterInfo exchange
   - Padding handling
   - Termination messages

3. **Interoperability:**
   - Test against Java I2P
   - Test against i2pd
   - Test IPv4 and IPv6
   - Test published and hidden routers

**Security Tests:**

1. **Negative Tests:**
   - Invalid AEAD tags
   - Replayed messages
   - Clock skew attacks
   - Malformed frames

2. **DoS Tests:**
   - Connection flooding
   - Slowloris attacks
   - CPU exhaustion (excessive DH)
   - Memory exhaustion

3. **Fuzzing:**
   - Random handshake messages
   - Random data phase frames
   - Random block types and sizes
   - Invalid cryptographic values

### Migration from NTCP

**For Legacy NTCP Support (now removed):**

NTCP (version 1) was removed in I2P 0.9.50 (May 2021). All current implementations must support NTCP2. Historical notes:

1. **Transition Period (2018-2021):**
   - 0.9.36: NTCP2 introduced (disabled by default)
   - 0.9.37: NTCP2 enabled by default
   - 0.9.40: NTCP deprecated
   - 0.9.50: NTCP removed

2. **Version Detection:**
   - "NTCP" transportStyle indicated both versions supported
   - "NTCP2" transportStyle indicated NTCP2 only
   - Automatic detection via message size (287 vs 288 bytes)

3. **Current Status:**
   - All routers must support NTCP2
   - "NTCP" transportStyle is obsolete
   - Use "NTCP2" transportStyle exclusively

## Appendix A: Noise XK Pattern

**Standard Noise XK Pattern:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```

**Interpretation:**

- `<-` : Message from responder (Bob) to initiator (Alice)
- `->` : Message from initiator (Alice) to responder (Bob)
- `s` : Static key (long-term identity key)
- `rs` : Remote static key (peer's static key, known in advance)
- `e` : Ephemeral key (session-specific, generated on-demand)
- `es` : Ephemeral-Static DH (Alice ephemeral × Bob static)
- `ee` : Ephemeral-Ephemeral DH (Alice ephemeral × Bob ephemeral)
- `se` : Static-Ephemeral DH (Alice static × Bob ephemeral)

**Key Agreement Sequence:**

1. **Pre-message:** Alice knows Bob's static public key (from RouterInfo)
2. **Message 1:** Alice sends ephemeral key, performs es DH
3. **Message 2:** Bob sends ephemeral key, performs ee DH
4. **Message 3:** Alice reveals static key, performs se DH

**Security Properties:**

- Alice authenticated: Yes (by message 3)
- Bob authenticated: Yes (by possessing static private key)
- Forward secrecy: Yes (ephemeral keys destroyed)
- KCI resistance: Yes (authentication level 2)

## Appendix B: Base64 Encoding

**I2P Base64 Alphabet:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```

**Differences from Standard Base64:**
- Characters 62-63: `-~` instead of `+/`
- Padding: Same (`=`) or omitted depending on context

**Usage in NTCP2:**
- Static key ("s"): 32 bytes → 44 characters (no padding)
- IV ("i"): 16 bytes → 24 characters (no padding)

**Encoding Example:**
```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```

## Appendix C: Packet Capture Analysis

**Identifying NTCP2 Traffic:**

1. **TCP Handshake:**
   - Standard TCP SYN, SYN-ACK, ACK
   - Destination port typically 8887 or similar

2. **Message 1 (SessionRequest):**
   - First application data from Alice
   - 80-65535 bytes (typically few hundred)
   - Appears random (AES-encrypted ephemeral key)
   - 287 bytes max if connecting to "NTCP" address

3. **Message 2 (SessionCreated):**
   - Response from Bob
   - 80-65535 bytes (typically few hundred)
   - Also appears random

4. **Message 3 (SessionConfirmed):**
   - From Alice
   - 48 bytes + variable (RouterInfo size + padding)
   - Typically 1-4 KB

5. **Data Phase:**
   - Variable-length frames
   - Length field obfuscated (appears random)
   - Encrypted payload
   - Padding makes size unpredictable

**DPI Evasion:**
- No plaintext headers
- No fixed patterns
- Length fields obfuscated
- Random padding breaks size-based heuristics

**Comparison to NTCP:**
- NTCP message 1 always 288 bytes (identifiable)
- NTCP2 message 1 size varies (not identifiable)
- NTCP had recognizable patterns
- NTCP2 designed to resist DPI

## Appendix D: Version History

**Major Milestones:**

- **0.9.36** (August 23, 2018): NTCP2 introduced, disabled by default
- **0.9.37** (October 4, 2018): NTCP2 enabled by default
- **0.9.40** (May 20, 2019): NTCP deprecated
- **0.9.42** (August 27, 2019): Network ID field added (Proposal 147)
- **0.9.50** (May 17, 2021): NTCP removed, capabilities support added
- **2.10.0** (September 9, 2025): Latest stable release

**Protocol Stability:**
- No breaking changes since 0.9.50
- Ongoing improvements to probing resistance
- Focus on performance and reliability
- Post-quantum cryptography in development (not enabled by default)

**Current Transport Status:**
- NTCP2: Mandatory TCP transport
- SSU2: Mandatory UDP transport
- NTCP (v1): Removed
- SSU (v1): Removed
