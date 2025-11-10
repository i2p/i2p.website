---
title: "Address Subscription Feed Commands"
description: "Extension to address subscription feeds enabling hostname holders to update and manage their entries"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Overview

This specification extends the address subscription feed with commands, enabling name servers to broadcast entry updates from hostname holders. Originally proposed in [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (September 2014), implemented in version 0.9.26 (June 2016), and deployed network-wide with status CLOSED.

The system has remained stable and unchanged since its initial implementation, continuing to operate identically in I2P 2.10.0 (Router API 0.9.65, September 2025).

## Motivation

Previously, the hosts.txt subscription servers sent data only in a simple hosts.txt format:

```
example.i2p=b64destination
```

This basic format created several problems:

- Hostname holders cannot update the Destination associated with their hostnames (for example, to upgrade the signing key to a stronger cryptographic type).
- Hostname holders cannot relinquish their hostnames arbitrarily. They must give the corresponding Destination private keys directly to the new holder.
- There is no way to authenticate that a subdomain is controlled by the corresponding base hostname. This is currently enforced only individually by some name servers.

## Design

This specification adds command lines to the hosts.txt format. With these commands, name servers can extend their services to provide additional features. Clients that implement this specification can listen for these features through the regular subscription process.

All command lines must be signed by the corresponding Destination. This ensures that changes are made only at the request of the hostname holder.

## Security Implications

This specification does not affect anonymity.

There is an increase in the risk associated with losing control of a Destination key, as someone who obtains it can use these commands to make changes to any associated hostnames. However, this is no more of a problem than the status quo, where someone who obtains a Destination can impersonate a hostname and (partially) take over its traffic. The increased risk is balanced by giving hostname holders the ability to change the Destination associated with a hostname in the event that they believe the Destination has been compromised. This is impossible with the current system.

## Specification

### New Line Types

There are two new types of lines:

1. **Add and Change commands:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```

2. **Remove commands:**

```
#!key1=val1#key2=val2...
```

#### Ordering

A feed is not necessarily in-order or complete. For example, a change command may appear on a line before an add command, or without an add command.

Keys may be in any order. Duplicate keys are not allowed. All keys and values are case-sensitive.

### Common Keys

**Required in all commands:**

**sig**
: Base64 signature, using signing key from the destination

**References to a second hostname and/or destination:**

**oldname**
: A second hostname (new or changed)

**olddest**
: A second Base64 destination (new or changed)

**oldsig**
: A second Base64 signature, using signing key from olddest

**Other common keys:**

**action**
: A command

**name**
: The hostname, only present if not preceded by `example.i2p=b64dest`

**dest**
: The Base64 destination, only present if not preceded by `example.i2p=b64dest`

**date**
: In seconds since epoch

**expires**
: In seconds since epoch

### Commands

All commands except the "Add" command must contain an `action=command` key/value pair.

For compatibility with older clients, most commands are preceded by `example.i2p=b64dest`, as noted below. For changes, these are always the new values. Any old values are included in the key/value section.

Listed keys are required. All commands may contain additional key/value items not defined here.

#### Add Hostname

**Preceded by example.i2p=b64dest**
: YES, this is the new hostname and destination.

**action**
: NOT included, it is implied.

**sig**
: signature

Example:

```
example.i2p=b64dest#!sig=b64sig
```

#### Change Hostname

**Preceded by example.i2p=b64dest**
: YES, this is the new hostname and old destination.

**action**
: changename

**oldname**
: the old hostname, to be replaced

**sig**
: signature

Example:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```

#### Change Destination

**Preceded by example.i2p=b64dest**
: YES, this is the old hostname and new destination.

**action**
: changedest

**olddest**
: the old destination, to be replaced

**oldsig**
: signature using olddest

**sig**
: signature

Example:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```

#### Add Hostname Alias

**Preceded by example.i2p=b64dest**
: YES, this is the new (alias) hostname and old destination.

**action**
: addname

**oldname**
: the old hostname

**sig**
: signature

Example:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```

#### Add Destination Alias

(Used for crypto upgrade)

**Preceded by example.i2p=b64dest**
: YES, this is the old hostname and new (alternate) destination.

**action**
: adddest

**olddest**
: the old destination

**oldsig**
: signature using olddest

**sig**
: signature using dest

Example:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```

#### Add Subdomain

**Preceded by subdomain.example.i2p=b64dest**
: YES, this is the new subdomain name and destination.

**action**
: addsubdomain

**oldname**
: the higher-level hostname (example.i2p)

**olddest**
: the higher-level destination (for example.i2p)

**oldsig**
: signature using olddest

**sig**
: signature using dest

Example:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```

#### Update Metadata

**Preceded by example.i2p=b64dest**
: YES, this is the old hostname and destination.

**action**
: update

**sig**
: signature

(add any updated keys here)

Example:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```

#### Remove Hostname

**Preceded by example.i2p=b64dest**
: NO, these are specified in the options

**action**
: remove

**name**
: the hostname

**dest**
: the destination

**sig**
: signature

Example:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```

#### Remove All with This Destination

**Preceded by example.i2p=b64dest**
: NO, these are specified in the options

**action**
: removeall

**dest**
: the destination

**sig**
: signature

Example:

```
#!action=removeall#dest=b64dest#sig=b64sig
```

### Signatures

All commands must be signed by the corresponding Destination. Commands with two destinations may need two signatures.

`oldsig` is always the "inner" signature. Sign and verify without the `oldsig` or `sig` keys present. `sig` is always the "outer" signature. Sign and verify with the `oldsig` key present but not the `sig` key.

#### Input for Signatures

To generate a byte stream to create or verify the signature, serialize as follows:

1. Remove the `sig` key
2. If verifying with `oldsig`, also remove the `oldsig` key
3. For Add or Change commands only, output `example.i2p=b64dest`
4. If any keys remain, output `#!`
5. Sort the options by UTF-8 key, fail if duplicate keys
6. For each key/value, output `key=value`, followed by (if not the last key/value) a `#`

**Notes**

- Do not output a newline
- Output encoding is UTF-8
- All destination and signature encoding is in Base 64 using the I2P alphabet
- Keys and values are case-sensitive
- Hostnames must be in lowercase

#### Current Signature Types

As of I2P 2.10.0, the following signature types are supported for destinations:

- **EdDSA_SHA512_Ed25519** (Type 7): Most common for destinations since 0.9.15. Uses a 32-byte public key and 64-byte signature. This is the recommended signature type for new destinations.
- **RedDSA_SHA512_Ed25519** (Type 13): Available for destinations and encrypted leasesets only (since 0.9.39).
- Legacy types (DSA_SHA1, ECDSA variants): Still supported but deprecated for new Router Identities as of 0.9.58.

Note: Post-quantum cryptographic options are available as of I2P 2.10.0 but are not yet the default signature types.

## Compatibility

All new lines in the hosts.txt format are implemented using leading comment characters (`#!`), so all older I2P versions will interpret the new commands as comments and ignore them gracefully.

When I2P routers update to the new specification, they will not re-interpret old comments, but will start listening to new commands in subsequent fetches of their subscription feeds. Thus it is important for name servers to persist command entries in some fashion, or enable ETag support so that routers can fetch all past commands.

## Implementation Status

**Initial deployment:** Version 0.9.26 (June 7, 2016)

**Current status:** Stable and unchanged through I2P 2.10.0 (Router API 0.9.65, September 2025)

**Proposal status:** CLOSED (successfully deployed network-wide)

**Implementation location:** `apps/addressbook/java/src/net/i2p/addressbook/` in the I2P Java router

**Key classes:**
- `SubscriptionList.java`: Manages subscription processing
- `Subscription.java`: Handles individual subscription feeds
- `AddressBook.java`: Core addressbook functionality
- `Daemon.java`: Addressbook background service

**Default subscription URL:** `http://i2p-projekt.i2p/hosts.txt`

## Transport Details

Subscriptions use HTTP with conditional GET support:

- **ETag header:** Supports efficient change detection
- **Last-Modified header:** Tracks subscription update times
- **304 Not Modified:** Servers should return this when content has not changed
- **Content-Length:** Strongly recommended for all responses

The I2P router uses standard HTTP client behavior with proper caching support.

## Version Context

**I2P versioning note:** Starting around version 1.5.0 (August 2021), I2P changed from 0.9.x versioning to semantic versioning (1.x, 2.x, etc.). However, the internal Router API version continues to use 0.9.x numbering for backward compatibility. As of October 2025, the current release is I2P 2.10.0 with Router API version 0.9.65.

This specification document was originally written for version 0.9.49 (February 2021) and remains completely accurate for the current version 0.9.65 (I2P 2.10.0) because the subscription feed system has had no changes since its original implementation in 0.9.26.

## References

- [Proposal 112 (Original)](/proposals/112-addressbook-subscription-feed-commands/)
- [Official Specification](/docs/specs/subscription/)
- [I2P Naming Documentation](/docs/overview/naming/)
- [Common Structures Specification](/docs/specs/common-structures/)
- [I2P Source Repository](https://github.com/i2p/i2p.i2p)
- [I2P Gitea Repository](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Related Developments

While the subscription feed system itself has not changed, the following related developments in I2P's naming infrastructure may be of interest:

- **Extended Base32 Names** (0.9.40+): Support for 56+ character base32 addresses for encrypted leasesets. Does not affect subscription feed format.
- **.i2p.alt TLD Registration** (RFC 9476, late 2023): Official GANA registration of .i2p.alt as an alternative TLD. Future router updates may strip .alt suffix, but no changes to subscription commands are required.
- **Post-Quantum Cryptography** (2.10.0+): Available but not default. Future consideration for signature algorithms in subscription feeds.
