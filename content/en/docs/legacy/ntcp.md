---
title: "NTCP (NIO-based TCP)"
description: "Legacy Java NIO-based TCP transport for I2P, replaced by NTCP2"
slug: "ntcp"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

DEPRECATED, NO LONGER SUPPORTED.
Disabled by default as of 0.9.40 2019-05.
Support removed as of 0.9.50 2021-05.
Replaced by [NTCP2](/docs/specs/ntcp2).
NTCP is a Java NIO-based transport introduced in I2P release 0.6.1.22.
Java NIO (new I/O) does not suffer from the 1 thread per connection issues of the old TCP transport.
NTCP-over-IPv6 is supported as of version 0.9.8.

By default, NTCP uses the IP/Port
auto-detected by SSU. When enabled on config.jsp,
SSU will notify/restart NTCP when the external address changes
or when the firewall status changes.
Now you can enable inbound TCP without a static IP or dyndns service.

The NTCP code within I2P is relatively lightweight (1/4 the size of the SSU code)
because it uses the underlying Java TCP transport for reliable delivery.


## Router Address Specification {#ra}

The following properties are stored in the network database.

- **Transport name:** NTCP
- **host:** IP (IPv4 or IPv6).
  Shortened IPv6 address (with "::") is allowed.
  Host names were previously allowed, but are deprecated as of release 0.9.32. See proposal 141.
- **port:** 1024 - 65535


## NTCP Protocol Specification

### Standard Message Format

After establishment,
the NTCP transport sends individual I2NP messages, with a simple checksum.
The unencrypted message is encoded as follows:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```

The data is then AES/256/CBC encrypted. The session key for the encryption
is negotiated during establishment (using Diffie-Hellman 2048 bit).
The establishment between two routers is implemented in the EstablishState class
and detailed below.
The IV for AES/256/CBC encryption is the last 16 bytes of the previous encrypted message.

0-15 bytes of padding are required to bring the total message length
(including the six size and checksum bytes) to a multiple of 16.
The maximum message size is currently 16 KB.
Therefore the maximum data size is currently 16 KB - 6, or 16378 bytes.
The minimum data size is 1.

### Time Sync Message Format

One special case is a metadata message where the sizeof(data) is 0. In
that case, the unencrypted message is encoded as:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```

Total length: 16 bytes. The time sync message is sent at approximately 15 minute intervals.
The message is encrypted just as standard messages are.


### Checksums

The standard and time sync messages use the Adler-32 checksum
as defined in the [ZLIB Specification](http://tools.ietf.org/html/rfc1950).


### Idle Timeout

Idle timeout and connection close is at the discretion of each endpoint and may vary.
The current implementation lowers the timeout as the number of connections approaches the
configured maximum, and raises the timeout when the connection count is low.
The recommended minimum timeout is two minutes or more, and the recommended
maximum timeout is ten minutes or more.


### RouterInfo Exchange

After establishment, and every 30-60 minutes thereafter,
the two routers should generally exchange RouterInfos using a DatabaseStoreMessage.
However, Alice should check if the first queued message is a DatabaseStoreMessage
so as not to send a duplicate message; this is often the case when connecting to a floodfill router.


### Establishment Sequence

In the establish state, there is a 4-phase message sequence to exchange DH keys and signatures.
In the first two messages there is a 2048-bit Diffie Hellman exchange.
Then, signatures of the critical data are exchanged to confirm the connection.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```

```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```

#### DH Key Exchange {#DH}

The initial 2048-bit DH key exchange
uses the same shared prime (p) and generator (g) as that used for I2P's
[ElGamal encryption](/docs/specs/cryptography#elgamal).

The DH key exchange consists of a number of steps, displayed below.
The mapping between these steps and the messages sent between I2P routers,
is marked in bold.

1. Alice generates a secret integer x. She then calculates `X = g^x mod p`.
2. Alice sends X to Bob **(Message 1)**.
3. Bob generates a secret integer y. He then calculates `Y = g^y mod p`.
4. Bob sends Y to Alice. **(Message 2)**
5. Alice can now compute `sessionKey = Y^x mod p`.
6. Bob can now compute `sessionKey = X^y mod p`.
7. Both Alice and Bob now have a shared key `sessionKey = g^(x*y) mod p`.

The sessionKey is then used to exchange identities in **Message 3** and **Message 4**.
The exponent (x and y) length for the DH exchange is documented on the
[cryptography page](/docs/specs/cryptography#exponent).

#### Session Key Details

The 32-byte session key is created as follows:

1. Take the exchanged DH key, represented as a positive minimal-length BigInteger byte array (two's complement big-endian)
2. If the most significant bit is 1 (i.e. array[0] & 0x80 != 0), prepend a 0x00 byte, as in Java's BigInteger.toByteArray() representation
3. If that byte array is greater than or equal to 32 bytes, use the first (most significant) 32 bytes
4. If that byte array is less than 32 bytes, append 0x00 bytes to extend to 32 bytes. *(vanishingly unlikely)*

#### Message 1 (Session Request)

This is the DH request. Alice already has Bob's
[Router Identity](/docs/specs/common-structures#struct_RouterIdentity),
IP address, and port, as contained in his
[Router Info](/docs/specs/common-structures#struct_RouterInfo),
which was published to the
[network database](/docs/overview/network-database).
Alice sends Bob:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```

Contents:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```

**Notes:**

- Bob verifies HXxorHI using his own router hash. If it does not verify, Alice has contacted the wrong router, and Bob drops the connection.


#### Message 2 (Session Created)

This is the DH reply. Bob sends Alice:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```

Unencrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```

Encrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```

**Notes:**

- Alice may drop the connection if the clock skew with Bob is too high as calculated using tsB.


#### Message 3 (Session Confirm A)

This contains Alice's router identity, and a signature of the critical data. Alice sends Bob:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```

Unencrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```

Encrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```

**Notes:**

- Bob verifies the signature, and on failure, drops the connection.
- Bob may drop the connection if the clock skew with Alice is too high as calculated using tsA.
- Alice will use the last 16 bytes of the encrypted contents of this message as the IV for the next message.
- Through release 0.9.15, the router identity was always 387 bytes, the signature was always a 40 byte DSA signature, and the padding was always 15 bytes. As of release 0.9.16, the router identity may be longer than 387 bytes, and the signature type and length are implied by the type of the [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) in Alice's [Router Identity](/docs/specs/common-structures#struct_RouterIdentity). The padding is as necessary to a multiple of 16 bytes for the entire unencrypted contents.
- The total length of the message cannot be determined without partially decrypting it to read the Router Identity. As the minimum length of the Router Identity is 387 bytes, and the minimum Signature length is 40 (for DSA), the minimum total message size is 2 + 387 + 4 + (signature length) + (padding to 16 bytes), or 2 + 387 + 4 + 40 + 15 = 448 for DSA. The receiver could read that minimum amount before decrypting to determine the actual Router Identity length. For small Certificates in the Router Identity, that will probably be the entire message, and there will not be any more bytes in the message to require an additional decryption operation.


#### Message 4 (Session Confirm B)

This is a signature of the critical data. Bob sends Alice:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```

Unencrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```

Encrypted Contents:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```

**Notes:**

- Alice verifies the signature, and on failure, drops the connection.
- Bob will use the last 16 bytes of the encrypted contents of this message as the IV for the next message.
- Through release 0.9.15, the signature was always a 40 byte DSA signature and the padding was always 8 bytes. As of release 0.9.16, the signature type and length are implied by the type of the [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) in Bob's [Router Identity](/docs/specs/common-structures#struct_RouterIdentity). The padding is as necessary to a multiple of 16 bytes for the entire unencrypted contents.


#### After Establishment

The connection is established, and standard or time sync messages may be exchanged.
All subsequent messages are AES encrypted using the negotiated DH session key.
Alice will use the last 16 bytes of the encrypted contents of message #3 as the next IV.
Bob will use the last 16 bytes of the encrypted contents of message #4 as the next IV.


### Check Connection Message

Alternately, when Bob receives a connection, it could be a
check connection (perhaps prompted by Bob asking for someone
to verify his listener).
Check Connection is not currently used.
However, for the record, check connections are formatted as follows.
A check info connection will receive 256 bytes containing:

- 32 bytes of uninterpreted, ignored data
- 1 byte size
- that many bytes making up the local router's IP address (as reached by the remote side)
- 2 byte port number that the local router was reached on
- 4 byte i2p network time as known by the remote side (seconds since the epoch)
- uninterpreted padding data, up to byte 223
- xor of the local router's identity hash and the SHA256 of bytes 32 through bytes 223

Check connection is completely disabled as of release 0.9.12.


## Discussion

Now on the [NTCP Discussion Page](/docs/discussions/ntcp).


## Future Work {#future}

- The maximum message size should be increased to approximately 32 KB.

- A set of fixed packet sizes may be appropriate to further hide the data
  fragmentation to external adversaries, but the tunnel, garlic, and end to
  end padding should be sufficient for most needs until then.
  However, there is currently no provision for padding beyond the next 16-byte boundary,
  to create a limited number of message sizes.

- Memory utilization (including that of the kernel) for NTCP should be compared to that for SSU.

- Can the establishment messages be randomly padded somehow, to frustrate
  identification of I2P traffic based on initial packet sizes?
