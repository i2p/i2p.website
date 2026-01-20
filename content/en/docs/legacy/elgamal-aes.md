---
title: "ElGamal/AES + SessionTag Encryption"
description: "Legacy end-to-end encryption combining ElGamal, AES, SHA-256, and one-time session tags"
slug: "elgamal-aes"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Overview

ElGamal/AES+SessionTags is used for end-to-end encryption.

As an unreliable, unordered, message based system, I2P uses a simple combination
of asymmetric and symmetric encryption algorithms to provide data confidentiality
and integrity to garlic messages. As a whole, the combination is referred
to as ElGamal/AES+SessionTags, but that is an excessively verbose way to describe
the use of 2048bit ElGamal, AES256, SHA256, and 32 byte nonces.

The first time a router wants to encrypt a garlic message to another router,
they encrypt the keying material for an AES256 session key with ElGamal and
append the AES256/CBC encrypted payload after that encrypted ElGamal block.
In addition to the encrypted payload, the AES encrypted section contains the
payload length, the SHA256 hash of the unencrypted payload, as well as a number
of "session tags" - random 32 byte nonces. The next time the sender wants
to encrypt a garlic message to another router, rather than ElGamal encrypt
a new session key they simply pick one of the previously delivered session
tags and AES encrypt the payload like before, using the session key used with
that session tag, prepended with the session tag itself. When a router receives
a garlic encrypted message, they check the first 32 bytes to see if it matches
an available session tag - if it does, they simply AES decrypt the message,
but if it does not, they ElGamal decrypt the first block.

Each session tag can be used only once so as to prevent internal adversaries
from unnecessarily correlating different messages as being between the same
routers. The sender of an ElGamal/AES+SessionTag encrypted message chooses
when and how many tags to deliver, prestocking the recipient with enough tags
to cover a volley of messages. Garlic messages may detect the successful tag
delivery by bundling a small additional message as a clove (a "delivery status
message") - when the garlic message arrives at the intended recipient and
is decrypted successfully, this small delivery status message is one of the
cloves exposed and has instructions for the recipient to send the clove back
to the original sender (through an inbound tunnel, of course). When the original
sender receives this delivery status message, they know that the session tags
bundled in the garlic message were successfully delivered.

Session tags themselves have a short lifetime, after which they are
discarded if not used. In addition, the quantity stored for each key is limited,
as are the number of keys themselves - if too many arrive, either new or old
messages may be dropped. The sender keeps track whether messages using session
tags are getting through, and if there isn't sufficient communication it may
drop the ones previously assumed to be properly delivered, reverting back
to the full expensive ElGamal encryption.
A session will continue to exist until all its tags are exhausted or expire.

Sessions are unidirectional. Tags are delivered from Alice to Bob,
and Alice then uses the tags, one by one, in subsequent messages to Bob.

Sessions may be established between Destinations, between Routers, or
between a Router and a Destination.
Each Router and Destination maintains its own Session Key Manager to
keep track of Session Keys and Session Tags.
Separate Session Key Managers prevents correlation of multiple Destinations
to each other or a Router by adversaries.


## Message Reception

Each message received has one of two possible conditions:

1. It is part of an existing session and contains a Session Tag and an AES encrypted block
2. It is for a new session and contains both ElGamal and AES encrypted blocks

When a router receives a message, it will first assume it is from
an existing session and attempt to look up the Session Tag and decrypt the following data using AES.
If that fails, it will assume it is for a new session and attempt to
decrypt it using ElGamal.


## New Session Message Specification {#new}

A New Session ElGamal Message contains two parts, an encrypted ElGamal block
and an encrypted AES block.

The encrypted message contains:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```


### ElGamal Block

The encrypted ElGamal Block is always 514 bytes long.

The unencrypted ElGamal data is 222 bytes long, containing:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```

The 32-byte [Session Key](/docs/spec/common-structures#type_SessionKey)
is the identifier for the session.
The 32-byte Pre-IV will be used to generate the IV for the AES block that follows;
the IV is the first 16 bytes of the SHA-256 Hash of the Pre-IV.

The 222 byte payload is encrypted
[using ElGamal](/docs/how/cryptography#elgamal)
and the encrypted block is 514 bytes long.

### AES Block {#aes}

The unencrypted data in the AES block contains the following:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```

#### Definition

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```

Minimum length: 48 bytes

The data is then [AES Encrypted](/docs/how/cryptography),
using the session key and IV (calculated from the pre-IV) from the ElGamal section.
The encrypted AES Block length is variable but is always a multiple of 16 bytes.

#### Notes

- Actual max payload length, and max block length, is less than 64 KB; see the [I2NP Overview](/docs/protocol/i2np).
- New Session Key is currently unused and is never present.


## Existing Session Message Specification {#existing}

The session tags delivered successfully are remembered for a
brief period (15 minutes currently) until they are used or discarded.
A tag is used by packaging one in an Existing Session Message that
contains only an AES encrypted block, and is not preceded by an
ElGamal block.

The existing session message is as follows:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```

#### Definition

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```

The session tag also serves as
the pre-IV. The IV is the first 16 bytes of the SHA-256 Hash of the sessionTag.

To decode a message from an existing session, a router looks up the Session Tag to find an
associated Session Key. If the Session Tag is found, the AES block is decrypted using the associated Session Key.
If the tag is not found, the message is assumed to be a [New Session Message](#new).


## Session Tag Configuration Options {#config}

As of release 0.9.2, the client may configure the default number of Session Tags to send
and the low tag threshold for the current session.
For brief streaming connections or datagrams, these options may be used to significantly reduce bandwidth.
See the [I2CP options specification](/docs/protocol/i2cp#options) for details.
The session settings may also be overridden on a per-message basis.
See the [I2CP Send Message Expires specification](/docs/spec/i2cp#msg_SendMessageExpires) for details.


## Future Work {#future}

**Note:**
ElGamal/AES+SessionTags is being replaced with ECIES-X25519-AEAD-Ratchet (Proposal 144).
The issues and ideas referenced below have been incorporated
into the design of the new protocol.
The following items will not be addressed in ElGamal/AES+SessionTags.

There are many possible areas to tune the Session Key Manager's algorithms;
some may interact with the streaming library behavior, or have significant
impact on overall performance.

- The number of tags delivered could depend on message size, keeping in mind
  the eventual padding to 1KB at the tunnel message layer.

- Clients could send an estimate of session lifetime to the router, as an advisory
  on the number of tags required.

- Delivery of too few tags causes the router to fall back to an expensive ElGamal encryption.

- The router may assume delivery of Session Tags, or await acknowledgement before using them;
  there are tradeoffs for each strategy.

- For very brief messages, almost the full 222 bytes of the pre-IV and padding fields in the ElGamal block
  could be used for the entire message, instead of establishing a session.

- Evaluate padding strategy; currently we pad to a minimum of 128 bytes.
  Would be better to add a few tags to small messages than pad.

- Perhaps things could be more efficient if the Session Tag system was bidirectional,
  so tags delivered in the 'forward' path could be used in the 'reverse' path,
  thus avoiding ElGamal in the initial response.
  The router currently plays some tricks like this when sending
  tunnel test messages to itself.

- Change from Session Tags to
  [a synchronized PRNG](/about/performance/future#prng).

- Several of these ideas may require a new I2NP message type, or
  set a flag in the
  [Delivery Instructions](/docs/spec/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  or set a magic number in the first few bytes of the Session Key field
  and accept a small risk of the random Session Key matching the magic number.
