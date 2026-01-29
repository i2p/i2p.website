---
title: "I2P Client Protocol (I2CP)"
description: "How applications negotiate sessions, tunnels, and LeaseSets with the I2P router."
slug: "i2cp"
aliases:
  - /docs/specs/i2cp-spec/
category: "Protocols"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Overview

This is the specification of the I2P Control Protocol (I2CP), the
low-level interface between clients and the router. Java clients will
use the I2CP client API, which implements this protocol.

There are no known non-Java implementations of a client-side library
that implements I2CP. Additionally, socket-oriented (streaming)
applications would need an implementation of the streaming protocol, but
there are no non-Java libraries for that either. Therefore, non-Java
clients should instead use the higher-layer protocol SAM
[SAMv3](/docs/api/samv3/), for which libraries exist in several
languages.

This is a low-level protocol supported both internally and externally by
the Java I2P router. The protocol is only serialized if the client and
router are not in the same JVM; otherwise, I2CP message Java objects are
passed via an internal JVM interface. I2CP is also supported externally
by the C++ router i2pd.

More information is on the I2CP Overview page
[I2CP](/docs/specs/i2cp/).

## Sessions

The protocol was designed to handle multiple "sessions", each with a
2-byte session ID, over a single TCP connection, however, Multiple
sessions were not implemented until version 0.9.21. See the
[multisession section below](#multisession). Do not attempt to use
multiple sessions on a single I2CP connection with routers older than
version 0.9.21.

It also appears that there are some provisions for a single client to
talk to multiple routers over separate connections. This is also
untested, and probably not useful.

There is no way for a session to be maintained after a disconnect, or to
be recovered on a different I2CP connection. When the socket is closed,
the session is destroyed.

## Example Message Sequences

Note: The examples below do not show the Protocol Byte (0x2a) that must
be sent from the client to the router when first connecting. More
information about connection initialization is on the I2CP Overview page
[I2CP](/docs/specs/i2cp/).

### Standard Session Establish

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```

### Get Bandwidth Limits (Simple Session)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```

### Destination Lookup (Simple Session)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```

### Outgoing Message

Existing session, with i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```

Existing session, with i2cp.messageReliability=none and nonzero nonce

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```

Existing session, with i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```

### Incoming Message

Existing session, with i2cp.fastReceive=true (as of 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```

Existing session, with i2cp.fastReceive=false (DEPRECATED)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```

### Multisession Notes {#multisession}

Multiple sessions on a single I2CP connection are supported as of router
version 0.9.21. The first session that is created is the "primary
session". Additional sessions are "subsessions". Subsessions are used
to support multiple destinations sharing a common set of tunnels. The
initial application is for the primary session to use ECDSA signing
keys, while the subsession uses DSA signing keys for communication with
old eepsites.

Subsessions share the same inbound and outbound tunnel pools as the
primary session. Subsessions must use the same encryption keys as the
primary session. This applies both to the LeaseSet encryption keys and
the (unused) Destination encryption keys. Subsessions must use different
signing keys in the destination, so the destination hash is different
from the primary session. As subsessions use the same encryption keys
and tunnels as the primary session, it is apparent to all that the
Destinations are running on the same router, so the usual
anti-correlation anonymity guarantees do not apply.

Subsessions are created by sending a CreateSession message and receiving
a SessionStatus message in reply, as usual. Subsessions must be created
after the primary session is created. The SessionStatus response will,
on success, contain a unique Session ID, distinct from the ID for the
primary session. While CreateSession messages should be processed
in-order, there is no sure way to correlate a CreateSession message with
the response, so a client should not have multiple CreateSession
messages outstanding simultaneously. SessionConfig options for the
subsession may not be honored where they are different from the primary
session. In particular, since subsessions use the same tunnel pool as
the primary session, tunnel options may be ignored.

The router will send separate RequestVariableLeaseSet messages for each
Destination to the client, and the client must reply with a
CreateLeaseSet message for each. The leases for the two Destinations
will not necessarily be identical, even though they are selected from
the same tunnel pool.

A subsession may be destroyed with the DestroySession message as usual.
This will not destroy the primary session or stop the I2CP connection.
Destroying the primary session will, however, destroy all subsessions
and stop the I2CP connection. A Disconnect message destroys all
sessions.

Note that most, but not all, I2CP messages contain a Session ID. For the
ones that do not, clients may need additional logic to properly handle
router responses. DestLookup and DestReply do not contain Session IDs;
use the newer HostLookup and HostReply instead. GetBandwidthLimts and
BandwidthLimits do not contain session IDs, however the response is not
session-specific.

### Version Notes {#notes}

The initial protocol version byte (0x2a) sent by the client is not
expected to change. Prior to release 0.8.7, the router's version
information was not available to the client, thus preventing new clients
from working with old routers. As of release 0.8.7, the two parties'
protocol version strings are exchanged in the Get/Set Date Messages.
Going forward, clients may use this information to communicate correctly
with old routers. Clients and routers should not send messages that are
unsupported by the other side, as they generally disconnect the session
upon reception of an unsupported message.

The exchanged version information is the "core" API version or I2CP
protocol version, and is not necessarily the router version.

A basic summary of the I2CP protocol versions is as follows. For
details, see below.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>

## Common structures {#structures}

### I2CP message header {#struct-I2CPMessageHeader}

#### Description

Common header to all I2CP messages, containing the message length and
message type.

#### Contents

1.  4 byte [Integer](/docs/specs/common-structures/#integer) specifying the length of
    the message body
2.  1 byte [Integer](/docs/specs/common-structures/#integer) specifying the message
    type.
3.  The I2CP message body, 0 or more bytes

#### Notes

Actual message length limit is about 64 KB.

### Message ID {#struct-MessageId}

#### Description

Uniquely identifies a message waiting on a particular router at a point
in time. This is always generated by the router and is NOT the same as
the nonce generated by the client.

#### Contents

1.  4 byte [Integer](/docs/specs/common-structures/#integer)

#### Notes

Message IDs are unique within a session only; they are not globally
unique.

### Payload {#struct-Payload}

#### Description

This structure is the content of a message being delivered from one
Destination to another.

#### Contents

1.  4 byte [Integer](/docs/specs/common-structures/#integer) length
2.  That many bytes

#### Notes

The payload is in a gzip format as specified on the I2CP Overview page
[I2CP-FORMAT](/docs/specs/i2cp/#format).

Actual message length limit is about 64 KB.

### Session Config {#struct-SessionConfig}

#### Description

Defines the configuration options for a particular client session.

#### Contents

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) of options
3.  Creation [Date](/docs/specs/common-structures/#date)
4.  [Signature](/docs/specs/common-structures/#signature) of the previous 3 fields,
    signed by the [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Notes

- The options are specified on the I2CP Overview page
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- The [Mapping](/docs/specs/common-structures/#mapping) must be sorted by key so that
  the signature will be validated correctly in the router.
- The creation date must be within +/- 30 seconds of the current time
  when processed by the router, or the config will be rejected.

#### Offline Signatures

- If the [Destination](/docs/specs/common-structures/#destination) is offline signed,
  the [Mapping](/docs/specs/common-structures/#mapping) must contain the three options
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, and
  i2cp.leaseSetOfflineSignature. The
  [Signature](/docs/specs/common-structures/#signature) is then generated by the
  transient [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) and
  is verified with the
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) specified in
  i2cp.leaseSetTransientPublicKey. See
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) for details.

### Session ID {#struct-SessionId}

#### Description

Uniquely identifies a session on a particular router at a point in time.

#### Contents

1.  2 byte [Integer](/docs/specs/common-structures/#integer)

#### Notes

Session ID 0xffff is used to indicate "no session", for example for
hostname lookups.

## Messages

See also the [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Message Types {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#bandwidthlimitsmessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#blindinginfomessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#createleasesetmessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#createleaseset2message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#createsessionmessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#destlookupmessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#destreplymessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#destroysessionmessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#disconnectmessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#getbandwidthlimitsmessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#getdatemessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#hostlookupmessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#hostreplymessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#messagepayloadmessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#messagestatusmessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#receivemessagebeginmessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#receivemessageendmessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#reconfiguresessionmessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#reportabusemessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#requestleasesetmessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#requestvariableleasesetmessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sendmessagemessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sendmessageexpiresmessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionstatusmessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-setdate">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>

### BandwidthLimitsMessage {#msg-BandwidthLimits}

#### Description

Tell the client what the bandwidth limits are.

Sent from Router to Client in response to a
[GetBandwidthLimitsMessage](#getbandwidthlimitsmessage).

#### Contents

1.  4 byte [Integer](/docs/specs/common-structures/#integer) Client inbound limit
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) Client outbound limit
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Router inbound limit
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Router inbound burst limit
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Router outbound limit
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Router outbound burst
    limit (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Router burst time
    (seconds)
8.  Nine 4-byte [Integer](/docs/specs/common-structures/#integer) (undefined)

#### Notes

The client limits may be the only values set, and may be the actual
router limits, or a percentage of the router limits, or specific to the
particular client, implementation-dependent. All the values labeled as
router limits may be 0, implementation-dependent. As of release 0.7.2.

### BlindingInfoMessage {#msg-BlindingInfo}

#### Description

Advise the router that a Destination is blinded, with optional lookup
password and optional private key for decryption. See proposals 123 and
149 for details.

The router needs to know if a destination is blinded. If it is blinded
and uses a secret or per-client authentication, it needs to have that
information as well.

A Host Lookup of a new-format b32 address ("b33") tells the router
that the address is blinded, but there's no mechanism to pass the
secret or private key to the router in the Host Lookup message. While we
could extend the Host Lookup message to add that information, it's
cleaner to define a new message.

This message provides a programmatic way for the client to tell the
router. Otherwise, the user would have to manually configure each
destination.

#### Usage

Before a client sends a message to a blinded destination, it must either
lookup the "b33" in a Host Lookup message, or send a Blinding Info
message. If the blinded destination requires a secret or per-client
authentication, the client must send a Blinding Info message.

The router does not send a reply to this message. Sent from Client to
Router.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Bit order: 76543210
> - Bit 0: 0 for everybody, 1 for per-client
> - Bits 3-1: Authentication scheme, if bit 0 is set to 1 for
>   per-client, otherwise 000
>   - 000: DH client authentication (or no per-client authentication)
>   - 001: PSK client authentication
> - Bit 4: 1 if secret required, 0 if no secret required
> - Bits 7-5: Unused, set to 0 for future compatibility

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Endpoint type

> - Type 0 is a [Hash](/docs/specs/common-structures/#hash)
> - Type 1 is a hostname [String](/docs/specs/common-structures/#string)
> - Type 2 is a [Destination](/docs/specs/common-structures/#destination)
> - Type 3 is a Sig Type and
>   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Expiration Seconds since
    epoch
6.  Endpoint: Data as specified, one of

> - Type 0: 32 byte [Hash](/docs/specs/common-structures/#hash)
>
> - Type 1: host name [String](/docs/specs/common-structures/#string)
>
> - Type 2: binary [Destination](/docs/specs/common-structures/#destination)
>
> 
>
>  - Type 3: 2 byte [Integer](/docs/specs/common-structures/#integer) signature type, followed by
>
>  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (length as
>       implied by sig type)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Decryption key Only present
    if flag bit 0 is set to 1. A 32-byte ECIES_X25519 private key,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Lookup Password Only present if
    flag bit 4 is set to 1.

#### Notes

- As of release 0.9.43.
- The Hash endpoint type is probably not useful unless the router can do
  a reverse lookup in the address book to get the Destination.
- The hostname endpoint type is probably not useful unless the router
  can do a lookup in the address book to get the Destination.

### CreateLeaseSetMessage {#msg-CreateLeaseSet}

DEPRECATED. Cannot be used for LeaseSet2, offline keys, non-ElGamal
encryption types, multiple encryption types, or encrypted LeaseSets. Use
CreateLeaseSet2Message with all routers 0.9.39 or higher.

#### Description

This message is sent in response to a
[RequestLeaseSetMessage](#requestleasesetmessage) or
[RequestVariableLeaseSetMessage](#requestvariableleasesetmessage) and
contains all of the [Lease](/docs/specs/common-structures/#lease) structures that
should be published to the I2NP Network Database.

Sent from Client to Router.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) or 20
    bytes ignored
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notes

The SigningPrivateKey matches the
[SigningPublicKey](/docs/specs/common-structures/#signingpublickey) from within the
LeaseSet, only if the signing key type is DSA. This is for LeaseSet
revocation, which is unimplemented and is unlikely to ever be
implemented. If the signing key type is not DSA, this field contains 20
bytes of random data. The length of this field is always 20 bytes, it
does not ever equal the length of a non-DSA signing private key.

The PrivateKey matches the [PublicKey](/docs/specs/common-structures/#publickey) from
the LeaseSet. The PrivateKey is necessary for decrypting garlic routed
messages.

Revocation is unimplemented. Connection to multiple routers is
unimplemented in any client library.

### CreateLeaseSet2Message {#msg-CreateLeaseSet2}

#### Description

This message is sent in response to a
[RequestLeaseSetMessage](#requestleasesetmessage) or
[RequestVariableLeaseSetMessage](#requestvariableleasesetmessage) and
contains all of the [Lease](/docs/specs/common-structures/#lease) structures that
should be published to the I2NP Network Database.

Sent from Client to Router. Since release 0.9.39. Per-client
authentication for EncryptedLeaseSet supported as of 0.9.41.
MetaLeaseSet is not yet supported via I2CP. See proposal 123 for more
information.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  One byte type of lease set to follow.

> - Type 1 is a [LeaseSet](/docs/specs/common-structures/#leaseset) (deprecated)
> - Type 3 is a [LeaseSet2](/docs/specs/common-structures/#leaseset2)
> - Type 5 is a [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
> - Type 7 is a [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) or
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) or
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) or
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  One byte number of private keys to follow.
5.  [PrivateKey](/docs/specs/common-structures/#privatekey) list. One for each public
    key in the lease set, in the same order. (Not present for Meta LS2)

> - Encryption type (2 byte [Integer](/docs/specs/common-structures/#integer))
> - Encryption key length (2 byte [Integer](/docs/specs/common-structures/#integer))
> - Encryption [PrivateKey](/docs/specs/common-structures/#privatekey) (number of bytes
>   specified)

#### Notes

The PrivateKeys match each of the [PublicKey](/docs/specs/common-structures/#publickey)
from the LeaseSet. The PrivateKeys are necessary for decrypting garlic
routed messages.

See proposal 123 for more information on Encrypted LeaseSets.

The contents and format for MetaLeaseSet are preliminary and subject to
change. There is no protocol specified for administration of multiple
routers. See proposal 123 for more information.

The signing private key, previously defined for revocation and unused,
is not present in LS2.

Preliminary version with message type 40 was in 0.9.38 but the format
was changed. Type 40 is abandoned and is unsupported. Type 41 not valid
until 0.9.39.

### CreateSessionMessage {#msg-CreateSession}

#### Description

This message is sent from a client to initiate a session, where a
session is defined as a single Destination's connection to the network,
to which all messages for that Destination will be delivered and from
which all messages that Destination sends to any other Destination will
be sent through.

Sent from Client to Router. The router responds with a
[SessionStatusMessage](#sessionstatusmessage).

#### Contents

1.  [Session Config](#struct-sessionconfig)

#### Notes

- This is the second message sent by the client. Previously the client
  sent a [GetDateMessage](#getdatemessage) and received a
  [SetDateMessage](#msg-setdate) response.
- If the Date in the Session Config is too far (more than +/- 30
  seconds) from the router's current time, the session will be
  rejected.
- If there is already a session on the router for this Destination, the
  session will be rejected.
- The [Mapping](/docs/specs/common-structures/#mapping) in the Session Config must be
  sorted by key so that the signature will be validated correctly in the
  router.

### DestLookupMessage {#msg-DestLookup}

#### Description

Sent from Client to Router. The router responds with a
[DestReplyMessage](#destreplymessage).

#### Contents

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notes

As of release 0.7.

As of release 0.8.3, multiple outstanding lookups are supported, and
lookups are supported in both I2PSimpleSession and in standard sessions.

[HostLookupMessage](#hostlookupmessage) is preferred as of release
0.9.11.

### DestReplyMessage {#msg-DestReply}

#### Description

Sent from Router to Client in response to a
[DestLookupMessage](#destlookupmessage).

#### Contents

1.  [Destination](/docs/specs/common-structures/#destination) on success, or
    [Hash](/docs/specs/common-structures/#hash) on failure

#### Notes

As of release 0.7.

As of release 0.8.3, the requested Hash is returned if the lookup
failed, so that the client may have multiple lookups outstanding and
correlate the replies to the lookups. To correlate a Destination
response with a request, take the Hash of the Destination. Prior to
release 0.8.3, the response was empty on failure.

### DestroySessionMessage {#msg-DestroySession}

#### Description

This message is sent from a client to destroy a session.

Sent from Client to Router. The router should respond with a
[SessionStatusMessage](#sessionstatusmessage) (Destroyed). However, see
important notes below.

#### Contents

1.  [Session ID](#struct-sessionid)

#### Notes

The router at this point should release all resources related to the
session.

Through API 0.9.66, the Java I2P router and client libraries deviate
substantially from this specification. The router never sends a
SessionStatus(Destroyed) response. If no sessions are left, it sends a
[DisconnectMessage](#disconnectmessage). If there are subsessions or the
primary session is remaining, it does not reply.

The Java client library responds to a SessionStatus message by
destroying all sessions and reconnecting.

Destroying individual subsessions on a connection with multiple sessions
may not be fully tested or working on various router and client
implementations. Use caution.

Implementations should treat a destroy for a primary session as a
destroy for all subsessions, but allow a destroy for a single subsession
and keep the connection open, but Java I2P does not do that now. If Java
I2P behavior is changed in subsequent releases, it will be documented
here.

### DisconnectMessage {#msg-Disconnect}

#### Description

Tell the other party that there are problems and the current connection
is about to be destroyed. This ends all sessions on that connection. The
socket will be closed shortly. Sent either from router to client or from
client to router.

#### Contents

1.  Reason [String](/docs/specs/common-structures/#string)

#### Notes

Only implemented in the router-to-client direction, at least in Java
I2P.

### GetBandwidthLimitsMessage {#msg-GetBandwidthLimits}

#### Description

Request that the router state what its current bandwidth limits are.

Sent from Client to Router. The router responds with a
[BandwidthLimitsMessage](#bandwidthlimitsmessage).

#### Contents

*None*

#### Notes

As of release 0.7.2.

As of release 0.8.3, supported in both I2PSimpleSession and in standard
sessions.

### GetDateMessage {#msg-GetDate}

#### Description

Sent from Client to Router. The router responds with a
[SetDateMessage](#msg-setdate).

#### Contents

1.  I2CP API Version [String](/docs/specs/common-structures/#string)
2.  Authentication [Mapping](/docs/specs/common-structures/#mapping) (optional, as of
    release 0.9.11)

#### Notes

- Generally the first message sent by the client after sending the
  protocol version byte.
- The version string is included as of release 0.8.7. This is only
  useful if the client and router are not in the same JVM. If it is not
  present, the client is version 0.8.6 or earlier.
- As of release 0.9.11, the authentication
  [Mapping](/docs/specs/common-structures/#mapping) may be included, with the keys
  i2cp.username and i2cp.password. The Mapping need not be sorted as
  this message is not signed. Prior to and including 0.9.10,
  authentication is included in the [Session Config](#struct-sessionconfig)
  Mapping, and no authentication is enforced for
  [GetDateMessage](#getdatemessage),
  [GetBandwidthLimitsMessage](#getbandwidthlimitsmessage), or
  [DestLookupMessage](#destlookupmessage). When enabled, authentication
  via [GetDateMessage](#getdatemessage) is required before any other
  messages as of release 0.9.16. This is only useful outside router
  context. This is an incompatible change, but will only affect sessions
  outside router context with authentication, which should be rare.

### HostLookupMessage {#msg-HostLookup}

#### Description

Sent from Client to Router. The router responds with a
[HostReplyMessage](#hostreplymessage).

This replaces the [DestLookupMessage](#destlookupmessage) and adds a
request ID, a timeout, and host name lookup support. As it also supports
Hash lookups, it may be used for all lookups if the router supports it.
For host name lookups, the router will query its context's naming
service. This is only useful if the client is outside the router's
context. Inside router context, the client should query the naming
service itself, which is much more efficient.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) request ID
3.  4 byte [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) request type
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) or host name
    [String](/docs/specs/common-structures/#string) or
    [Destination](/docs/specs/common-structures/#destination)

Request types:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>

Types 2-4 request that the options mapping from the LeaseSet be returned
in the HostReply message. See proposal 167.

#### Notes

- As of release 0.9.11. Use [DestLookupMessage](#destlookupmessage) for
  older routers.
- The session ID and request ID will be returned in the
  [HostReplyMessage](#hostreplymessage). Use 0xFFFF for the session ID
  if there is no session.
- Timeout is useful for Hash lookups. Recommended minimum 10,000 (10
  sec.). In the future it may also be useful for remote naming service
  lookups. The value may be not be honored for local host name lookups,
  which should be fast.
- Base 32 host name lookup is supported but it is preferred to convert
  it to a Hash first.

### HostReplyMessage {#msg-HostReply}

#### Description

Sent from Router to Client in response to a
[HostLookupMessage](#hostlookupmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) request ID
3.  1 byte [Integer](/docs/specs/common-structures/#integer) result code

> - 0: Success
> - 1: Failure
> - 2: Lookup password required (as of 0.9.43)
> - 3: Private key required (as of 0.9.43)
> - 4: Lookup password and private key required (as of 0.9.43)
> - 5: Leaseset decryption failure (as of 0.9.43)
> - 6: Leaseset lookup failure (as of 0.9.66)
> - 7: Lookup type unsupported (as of 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), only present if result
    code is zero, except may also be returned for lookup types 2-4. See
    below.
5.  [Mapping](/docs/specs/common-structures/#mapping), only present if result code is
    zero, only returned for lookup types 2-4. As of 0.9.66. See below.

#### Responses for lookup types 2-4

Proposal 167 defines additional lookup types that return all options
from the leaseset, if present. For lookup types 2-4, the router must
fetch the leaseset, even if the lookup key is in the address book.

If successful, the HostReply will contain the options Mapping from the
leaseset, and includes it as item 5 after the destination. If there are
no options in the Mapping, or the leaseset was version 1, it will still
be included as an empty Mapping (two bytes: 0 0). All options from the
leaseset will be included, not just service record options. For example,
options for parameters defined in the future may be present. The
returned Mapping may or may not be sorted, implementation-dependent.

On leaseset lookup failure, the reply will contain a new error code 6
(Leaseset lookup failure) and will not include a mapping. When error
code 6 is returned, the Destination field may or may not be present. It
will be present if a hostname lookup in the address book was successful,
or if a previous lookup was successful and the result was cached, or if
the Destination was present in the lookup message (lookup type 4).

If a lookup type is not supported, the reply will contain a new error
code 7 (lookup type unsupported).

#### Notes

- As of release 0.9.11. See [HostLookupMessage](#hostlookupmessage)
  notes.
- The session ID and request ID are those from the
  [HostLookupMessage](#hostlookupmessage).
- The result code is 0 for success, 1-255 for failure. 1 indicates a
  generic failure. As of 0.9.43, the additional failure codes 2-5 were
  defined to support extended errors for "b33" lookups. See proposals
  123 and 149 for additional information. As of 0.9.66, the additional
  failure codes 6-7 were defined to support extended errors for type 2-4
  lookups. See proposal 167 for additional information.

### MessagePayloadMessage {#msg-MessagePayload}

#### Description

Deliver the payload of a message to the client.

Sent from Router to Client. If i2cp.fastReceive=true, which is not the
default, the client responds with a
[ReceiveMessageEndMessage](#receivemessageendmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)
3.  [Payload](#struct-payload)

#### Notes

### MessageStatusMessage {#msg-MessageStatus}

#### Description

Notify the client of the delivery status of an incoming or outgoing
message. Sent from Router to Client. If this message indicates that an
incoming message is available, the client responds with a
[ReceiveMessageBeginMessage](#receivemessagebeginmessage). For an
outgoing message, this is a response to a
[SendMessageMessage](#sendmessagemessage) or
[SendMessageExpiresMessage](#sendmessageexpiresmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) generated by the router
3.  1 byte [Integer](/docs/specs/common-structures/#integer) status
4.  4 byte [Integer](/docs/specs/common-structures/#integer) size
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce previously generated
    by the client

#### Notes

Through version 0.9.4, the known status values are 0 for message is
available, 1 for accepted, 2 for best effort succeeded, 3 for best
effort failed, 4 for guaranteed succeeded, 5 for guaranteed failed. The
size Integer specifies the size of the available message and is only
relevant for status = 0. Even though guaranteed is unimplemented, (best
effort is the only service), the current router implementation uses the
guaranteed status codes, not the best effort codes.

As of router version 0.9.5, additional status codes are defined, however
they are not necessarily implemented. See
[MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) for details. For outgoing
messages, the codes 1, 2, 4, and 6 indicate success; all others are
failures. Returned failure codes may vary and are
implementation-specific.

All status codes:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#sendmessagemessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>

When status = 1 (accepted), the nonce matches the nonce in the
[SendMessageMessage](#sendmessagemessage), and the included Message ID
will be used for subsequent success or failure notification. Otherwise,
the nonce may be ignored.

### ReceiveMessageBeginMessage {#msg-ReceiveMessageBegin}

DEPRECATED. Not supported by i2pd.

#### Description

Request the router to deliver a message that it was previously notified
of. Sent from Client to Router. The router responds with a
[MessagePayloadMessage](#messagepayloadmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)

#### Notes

The [ReceiveMessageBeginMessage](#receivemessagebeginmessage) is sent as
a response to a [MessageStatusMessage](#messagestatusmessage) stating
that a new message is available for pickup. If the message id specified
in the [ReceiveMessageBeginMessage](#receivemessagebeginmessage) is
invalid or incorrect, the router may simply not reply, or it may send
back a [DisconnectMessage](#disconnectmessage).

This is unused in "fast receive" mode, which is the default as of
release 0.9.4.

### ReceiveMessageEndMessage {#msg-ReceiveMessageEnd}

DEPRECATED. Not supported by i2pd.

#### Description

Tell the router that delivery of a message was completed successfully
and that the router can discard the message.

Sent from Client to Router.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)

#### Notes

The [ReceiveMessageEndMessage](#receivemessageendmessage) is sent after
a [MessagePayloadMessage](#messagepayloadmessage) fully delivers a
message's payload.

This is unused in "fast receive" mode, which is the default as of
release 0.9.4.

### ReconfigureSessionMessage {#msg-ReconfigureSession}

#### Description

Sent from Client to Router to update the session configuration. The
router responds with a [SessionStatusMessage](#sessionstatusmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Session Config](#struct-sessionconfig)

#### Notes

- As of release 0.7.1.
- If the Date in the Session Config is too far (more than +/- 30
  seconds) from the router's current time, the session will be
  rejected.
- The [Mapping](/docs/specs/common-structures/#mapping) in the Session Config must be
  sorted by key so that the signature will be validated correctly in the
  router.
- Some configuration options may only be set in the
  [CreateSessionMessage](#createsessionmessage), and changes here will
  not be recognized by the router. Changes to tunnel options inbound.\*
  and outbound.\* are always recognized.
- In general, the router should merge the updated config with the
  current config, so the updated config only needs to contain the new or
  changed options. However, because of the merge, options may not be
  removed in this manner; they must be set explicitly to the desired
  default value.

### ReportAbuseMessage {#msg-ReportAbuse}

DEPRECATED, UNUSED, UNSUPPORTED

#### Description

Tell the other party (client or router) that they are under attack,
potentially with reference to a particular MessageId. If the router is
under attack, the client may decide to migrate to another router, and if
a client is under attack, the router may rebuild its routers or banlist
some of the peers that sent it messages delivering the attack.

Sent either from router to client or from client to router.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) abuse severity (0 is
    minimally abusive, 255 being extremely abusive)
3.  Reason [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notes

Unused. Not fully implemented. Both router and client can generate a
[ReportAbuseMessage](#reportabusemessage), but neither has a handler for
the message when received.

### RequestLeaseSetMessage {#msg-RequestLeaseSet}

DEPRECATED. Not supported by i2pd. Not sent by Java I2P to clients
version 0.9.7 or higher (2013-07). Use RequestVariableLeaseSetMessage.

#### Description

Request that a client authorize the inclusion of a particular set of
inbound tunnels. Sent from Router to Client. The client responds with a
[CreateLeaseSetMessage](#createleasesetmessage).

The first of these messages sent on a session is a signal to the client
that tunnels are built and ready for traffic. The router must not send
the first of these messages until at least one inbound AND one outbound
tunnel have been built. Clients should timeout and destroy the session
if the first of these messages is not received after some time
(recommended: 5 minutes or more).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) number of tunnels
3.  That many pairs of:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  End [Date](/docs/specs/common-structures/#date)

#### Notes

This requests a [LeaseSet](/docs/specs/common-structures/#leaseset) with all
[Lease](/docs/specs/common-structures/#lease) entries set to expire at the same time.
For client versions 0.9.7 or higher,
[RequestVariableLeaseSetMessage](#requestvariableleasesetmessage) is
used.

### RequestVariableLeaseSetMessage {#msg-RequestVariableLeaseSet}

#### Description

Request that a client authorize the inclusion of a particular set of
inbound tunnels.

Sent from Router to Client. The client responds with a
[CreateLeaseSetMessage](#createleasesetmessage) or
[CreateLeaseSet2Message](#createleaseset2message).

The first of these messages sent on a session is a signal to the client
that tunnels are built and ready for traffic. The router must not send
the first of these messages until at least one inbound AND one outbound
tunnel have been built. Clients should timeout and destroy the session
if the first of these messages is not received after some time
(recommended: 5 minutes or more).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) number of tunnels
3.  That many [Lease](/docs/specs/common-structures/#lease) entries

#### Notes

This requests a [LeaseSet](/docs/specs/common-structures/#leaseset) with an individual
expiration time for each [Lease](/docs/specs/common-structures/#lease).

As of release 0.9.7. For clients before that release, use
[RequestLeaseSetMessage](#requestleasesetmessage).

### SendMessageMessage {#msg-SendMessage}

#### Description

This is how a client sends a message (the payload) to the
[Destination](/docs/specs/common-structures/#destination). The router will use a
default expiration.

Sent from Client to Router. The router responds with a
[MessageStatusMessage](#messagestatusmessage).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce

#### Notes

As soon as the [SendMessageMessage](#sendmessagemessage) arrives fully
intact, the router should return a
[MessageStatusMessage](#messagestatusmessage) stating that it has been
accepted for delivery. That message will contain the same nonce sent
here. Later on, based on the delivery guarantees of the session
configuration, the router may additionally send back another
[MessageStatusMessage](#messagestatusmessage) updating the status.

As of release 0.8.1, the router does not send either
[MessageStatusMessage](#messagestatusmessage) if
i2cp.messageReliability=none.

Prior to release 0.9.4, a nonce value of 0 was not allowed. As of
release 0.9.4, a nonce value of 0 is allowed, and tells to the router
that it should not send either
[MessageStatusMessage](#messagestatusmessage), i.e. it acts as if
i2cp.messageReliability=none for this message only.

Prior to release 0.9.14, a session with i2cp.messageReliability=none
could not be overridden on a per-message basis. As of release 0.9.14, in
a session with i2cp.messageReliability=none, the client may request
delivery of a [MessageStatusMessage](#messagestatusmessage) with the
delivery success or failure by setting the nonce to a nonzero value. The
router will not send the "accepted"
[MessageStatusMessage](#messagestatusmessage) but it will later send the
client a [MessageStatusMessage](#messagestatusmessage) with the same
nonce, and a success or failure value.

### SendMessageExpiresMessage {#msg-SendMessageExpires}

#### Description

Sent from Client to Router. Same as
[SendMessageMessage](#sendmessagemessage), except includes an expiration
and options.

#### Contents

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 bytes of flags (options)
6.  Expiration [Date](/docs/specs/common-structures/#date) truncated from 8 bytes to 6
    bytes

#### Notes

As of release 0.7.1.

In "best effort" mode, as soon as the SendMessageExpiresMessage
arrives fully intact, the router should return a MessageStatusMessage
stating that it has been accepted for delivery. That message will
contain the same nonce sent here. Later on, based on the delivery
guarantees of the session configuration, the router may additionally
send back another MessageStatusMessage updating the status.

As of release 0.8.1, the router does not send either Message Status
Message if i2cp.messageReliability=none.

Prior to release 0.9.4, a nonce value of 0 was not allowed. As of
release 0.9.4, a nonce value of 0 is allowed, and tells the router that
it should not send either Message Status Message, i.e. it acts as if
i2cp.messageReliability=none for this message only.

Prior to release 0.9.14, a session with i2cp.messageReliability=none
could not be overridden on a per-message basis. As of release 0.9.14, in
a session with i2cp.messageReliability=none, the client may request
delivery of a Message Status Message with the delivery success or
failure by setting the nonce to a nonzero value. The router will not
send the "accepted" Message Status Message but it will later send the
client a Message Status Message with the same nonce, and a success or
failure value.

#### Flags Field

As of release 0.8.4, the upper two bytes of the Date are redefined to
contain flags. The flags must default to all zeros for backward
compatibility. The Date will not encroach on the flags field until the
year 10889. The flags may be used by the application to provide hints to
the router as to whether a LeaseSet and/or ElGamal/AES Session Tags
should be delivered with the message. The settings will significantly
affect the amount of protocol overhead and the reliability of message
delivery. The individual flag bits are defined as follows, as of release
0.9.2. Definitions are subject to change. Use the SendMessageOptions
class to construct the flags.

Bit order: 15...0

Bits 15-11

:   Unused, must be zero

Bits 10-9

:   Message Reliability Override (Unimplemented, to be removed).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>

Bit 8

:   If 1, don't bundle a lease set in the garlic with this message. If
    0, the router may bundle a lease set at its discretion.

Bits 7-4

:   Low tag threshold. If there are less than this many tags available,
    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>

Bits 3-0

:   Number of tags to send if required. This is advisory and does not
    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>

### SessionStatusMessage {#msg-SessionStatus}

#### Description

Instruct the client as to the status of its session.

Sent from Router to Client, in response to a
[CreateSessionMessage](#createsessionmessage),
[ReconfigureSessionMessage](#reconfiguresessionmessage), or
[DestroySessionMessage](#destroysessionmessage). In all cases, including
in response to [CreateSessionMessage](#createsessionmessage), the router
should respond immediately (do not wait for tunnels to be built).

#### Contents

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) status

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#destroysessionmessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#createsessionmessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#reconfiguresessionmessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#createsessionmessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#reconfiguresessionmessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#createsessionmessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>

#### Notes

Status values are defined above. If the status is Created, the Session
ID is the identifier to be used for the rest of the session.

### SetDateMessage {#msg-SetDate}

#### Description

The current date and time. Sent from Router to Client as a part of the
initial handshake. As of release 0.9.20, may also be sent at any time
after the handshake to notify the client of a clock shift.

#### Contents

1.  [Date](/docs/specs/common-structures/#date)
2.  I2CP API Version [String](/docs/specs/common-structures/#string)

#### Notes

This is generally the first message sent by the router. The version
string is included as of release 0.8.7. This is only useful if the
client and router are not in the same JVM. If it is not present, the
router is version 0.8.6 or earlier.

Additional SetDate messages will not be sent to clients in the same JVM.

## References

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP Overview](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
