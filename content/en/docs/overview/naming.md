---
title: "Naming and Address Book"
description: "How I2P maps human-readable hostnames to destinations"
slug: "naming"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Overview

I2P ships with a generic naming library and a base implementation designed to work off a local name to destination mapping, as well as an add-on application called the [address book](#address-book). I2P also supports [Base32 hostnames](#base32-names) similar to Tor's .onion addresses.

The address book is a web-of-trust driven secure, distributed, and human readable naming system, sacrificing only the call for all human readable names to be globally unique by mandating only local uniqueness. While all messages in I2P are cryptographically addressed by their destination, different people can have local address book entries for "Alice" which refer to different destinations. People can still discover new names by importing published address books of peers specified in their web of trust, by adding in the entries provided through a third party, or (if some people organize a series of published address books using a first come first serve registration system) people can choose to treat these address books as name servers, emulating traditional DNS.

NOTE: For the reasoning behind the I2P naming system, common arguments against it and possible alternatives see the [naming discussion](/docs/legacy/naming/) page.

---

## Naming System Components

There is no central naming authority in I2P. All hostnames are local.

The naming system is quite simple and most of it is implemented in applications external to the router, but bundled with the I2P distribution. The components are:

1. The local [naming service](#naming-services) which does lookups and also handles [Base32 hostnames](#base32-names).
2. The [HTTP proxy](#http-proxy) which asks the router for lookups and points the user to remote jump services to assist with failed lookups.
3. HTTP [host-add forms](#host-add-services) which allow users to add hosts to their local hosts.txt
4. HTTP [jump services](#jump-services) which provide their own lookups and redirection.
5. The [address book](#address-book) application which merges external host lists, retrieved via HTTP, with the local list.
6. The [SusiDNS](#susidns) application which is a simple web front-end for address book configuration and viewing of the local host lists.

---

## Naming Services

All destinations in I2P are 516-byte (or longer) keys. (To be more precise, it is a 256-byte public key plus a 128-byte signing key plus a 3-or-more byte certificate, which in Base64 representation is 516 or more bytes. Non-null [Certificates](/docs/legacy/naming/#certificates) are in use now for signature type indication. Therefore, certificates in recently-generated destinations are more than 3 bytes.

If an application (i2ptunnel or the HTTP proxy) wishes to access a destination by name, the router does a very simple local lookup to resolve that name.

### Hosts.txt Naming Service

The hosts.txt Naming Service does a simple linear search through text files. This naming service was the default until release 0.8.8 when it was replaced by the Blockfile Naming Service. The hosts.txt format had become too slow after the file grew to thousands of entries.

It does a linear search through three local files, in order, to look up host names and convert them to a 516-byte destination key. Each file is in a simple [configuration file format](/docs/specs/configuration/), with hostname=base64, one per line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

The Blockfile Naming Service stores multiple "address books" in a single database file named hostsdb.blockfile. This Naming Service is the default since release 0.8.8.

A blockfile is simply on-disk storage of multiple sorted maps (key-value pairs), implemented as skiplists. The blockfile format is specified on the [Blockfile page](/docs/specs/blockfile/). It provides fast Destination lookup in a compact format. While the blockfile overhead is substantial, the destinations are stored in binary rather than in Base 64 as in the hosts.txt format. In addition, the blockfile provides the capability of arbitrary metadata storage (such as added date, source, and comments) for each entry to implement advanced address book features. The blockfile storage requirement is a modest increase over the hosts.txt format, and the blockfile provides approximately 10x reduction in lookup times.

On creation, the naming service imports entries from the three files used by the hosts.txt Naming Service. The blockfile mimics the previous implementation by maintaining three maps that are searched in-order, named privatehosts.txt, userhosts.txt, and hosts.txt. It also maintains a reverse-lookup map to implement rapid reverse lookups.

### Other Naming Service Facilities

The lookup is case-insensitive. The first match is used, and conflicts are not detected. There is no enforcement of naming rules in lookups. Lookups are cached for a few minutes. Base 32 resolution is [described below](#base32-names). For a full description of the Naming Service API see the [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). This API was significantly expanded in release 0.8.7 to provide adds and removes, storage of arbitrary properties with the hostname, and other features.

### Alternatives and Experimental Naming Services

The naming service is specified with the configuration property `i2p.naming.impl=class`. Other implementations are possible. For example, there is an experimental facility for real-time lookups (a la DNS) over the network within the router. For more information see the [alternatives on the discussion page](/docs/legacy/naming/#alternatives).

The HTTP proxy does a lookup via the router for all hostnames ending in '.i2p'. Otherwise, it forwards the request to a configured HTTP outproxy. Thus, in practice, all HTTP (I2P Site) hostnames must end in the pseudo-Top Level Domain '.i2p'.

If the router fails to resolve the hostname, the HTTP proxy returns an error page to the user with links to several "jump" services. See below for details.

---

## .i2p.alt Domain

We previously [applied to reserve the .i2p TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) following the procedures specified in [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). However, this application and all others were rejected, and RFC 6761 was declared a "mistake".

After many years of work by the GNUnet team and others, the .alt domain was reserved as a special-use TLD in [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) as of late 2023. While there are no official registrars sanctioned by IANA, we have registered the .i2p.alt domain with the primary unofficial registrar [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). This does not prevent others from using the domain, but it should help discourage it.

One benefit to the .alt domain is that, in theory, DNS resolvers will not forward .alt requests once they update to comply with RFC 9476, and that will prevent DNS leaks. For compatibility with .i2p.alt hostnames, I2P software and services should be updated to handle these hostnames by stripping off the .alt TLD. These updates are scheduled for the first half of 2024.

At this time, there are no plans to make .i2p.alt the preferred form for display and interchange of I2P hostnames. This is a topic for further research and discussion.

---

## Address Book

### Incoming Subscriptions and Merging

The address book application periodically retrieves other users' hosts.txt files and merges them with the local hosts.txt, after several checks. Naming conflicts are resolved on a first-come first-served basis.

Subscribing to another user's hosts.txt file involves giving them a certain amount of trust. You do not want them, for example, 'hijacking' a new site by quickly entering in their own key for a new site before passing the new host/key entry to you.

For this reason, the only subscription configured by default is `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, which contains a copy of the hosts.txt included in the I2P release. Users must configure additional subscriptions in their local address book application (via subscriptions.txt or [SusiDNS](#susidns)).

Some other public address book subscription links:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

The operators of these services may have various policies for listing hosts. Presence on this list does not imply endorsement.

### Naming Rules

While there are hopefully not any technical limitations within I2P on host names, the address book enforces several restrictions on host names imported from subscriptions. It does this for basic typographical sanity and compatibility with browsers, and for security. The rules are essentially the same as those in RFC2396 Section 3.2.2. Any hostnames violating these rules may not be propagated to other routers.

Naming Rules:

- Names are converted to lower case on import.
- Names are checked for conflict with existing names in the existing userhosts.txt and hosts.txt (but not privatehosts.txt) after conversion to lower case.
- Must contain only [a-z] [0-9] '.' and '-' after conversion to lower case.
- Must not start with '.' or '-'.
- Must end with '.i2p'.
- 67 characters maximum, including the '.i2p'.
- Must not contain '..'.
- Must not contain '.-' or '-.' (as of 0.6.1.33).
- Must not contain '--' except in 'xn--' for IDN.
- Base32 hostnames (*.b32.i2p) are reserved for base 32 use and so are not allowed to be imported.
- Certain hostnames reserved for project use are not allowed (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, and others)
- Hostnames starting with 'www.' are discouraged and are rejected by some registration services. Some addressbook implementations automatically strip 'www.' prefixes from lookups. So registring 'www.example.i2p' is unnecessary, and registering a different destination for 'www.example.i2p' and 'example.i2p' will make 'www.example.i2p' unreachable for some users.
- Keys are checked for base64 validity.
- Keys are checked for conflict with existing keys in hosts.txt (but not privatehosts.txt).
- Minimum key length 516 bytes.
- Maximum key length 616 bytes (to account for certs up to 100 bytes).

Any name received via subscription that passes all the checks is added via the local naming service.

Note that the '.' symbols in a host name are of no significance, and do not denote any actual naming or trust hierarchy. If the name 'host.i2p' already exists, there is nothing to prevent anybody from adding a name 'a.host.i2p' to their hosts.txt, and this name can be imported by others' address book. Methods to deny subdomains to non-domain 'owners' (certificates?), and the desirability and feasibility of these methods, are topics for future discussion.

International Domain Names (IDN) also work in i2p (using punycode 'xn--' form). To see IDN .i2p domain names rendered correctly in Firefox's location bar, add 'network.IDN.whitelist.i2p (boolean) = true' in about:config.

As the address book application does not use privatehosts.txt at all, in practice this file is the only place where it is appropriate to place private aliases or "pet names" for sites already in hosts.txt.

### Advanced Subscription Feed Format

As of release 0.9.26, subscription sites and clients may support an advanced hosts.txt feed protocol that includes metadata including signatures. This format is backwards-compatible with the standard hosts.txt hostname=base64destination format. See [the specification](/docs/specs/subscription/) for details.

### Outgoing Subscriptions

Address Book will publish the merged hosts.txt to a location (traditionally hosts.txt in the local I2P Site's home directory) to be accessed by others for their subscriptions. This step is optional and is disabled by default.

### Hosting and HTTP Transport Issues

The address book application, together with eepget, saves the Etag and/or Last-Modified information returned by the web server of the subscription. This greatly reduces the bandwidth required, as the web server will return a '304 Not Modified' on the next fetch if nothing has changed.

However the entire hosts.txt is downloaded if it has changed. See below for discussion on this issue.

Hosts serving a static hosts.txt or an equivalent CGI application are strongly encouraged to deliver a Content-Length header, and either an Etag or Last-Modified header. Also ensure that the server delivers a '304 Not Modified' when appropriate. This will dramatically reduce the network bandwidth, and reduce chances of corruption.

---

## Host Add Services

A host add service is a simple CGI application that takes a hostname and a Base64 key as parameters and adds that to its local hosts.txt. If other routers subscribe to that hosts.txt, the new hostname/key will be propagated through the network.

It is recommended that host add services impose, at a minimum, the restrictions imposed by the address book application listed above. Host add services may impose additional restrictions on hostnames and keys, for example:

- A limit on number of 'subdomains'.
- Authorization for 'subdomains' through various methods.
- Hashcash or signed certificates.
- Editorial review of host names and/or content.
- Categorization of hosts by content.
- Reservation or rejection of certain host names.
- Restrictions on the number of names registered in a given time period.
- Delays between registration and publication.
- Requirement that the host be up for verification.
- Expiration and/or revocation.
- IDN spoof rejection.

---

## Jump Services

A jump service is a simple CGI application that takes a hostname as a parameter and returns a 301 redirect to the proper URL with a `?i2paddresshelper=key` string appended. The HTTP proxy will interpret the appended string and use that key as the actual destination. In addition, the proxy will cache that key so the address helper is not necessary until restart.

Note that, like with subscriptions, using a jump service implies a certain amount of trust, as a jump service could maliciously redirect a user to an incorrect destination.

To provide the best service, a jump service should be subscribed to several hosts.txt providers so that its local host list is current.

---

## SusiDNS

SusiDNS is simply a web interface front-end to configuring address book subscriptions and accessing the four address book files. All the real work is done by the 'address book' application.

Currently, there is little enforcement of address book naming rules within SusiDNS, so a user may enter hostnames locally that would be rejected by the address book subscription rules.

---

## Base32 Names

I2P supports Base32 hostnames similar to Tor's .onion addresses. Base32 addresses are much shorter and easier to handle than the full 516-character Base64 Destinations or addresshelpers. Example: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

In Tor, the address is 16 characters (80 bits), or half of the SHA-1 hash. I2P uses 52 characters (256 bits) to represent the full SHA-256 hash. The form is {52 chars}.b32.i2p. Tor has a [proposal](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) to convert to an identical format of {52 chars}.onion for their hidden services. Base32 is implemented in the naming service, which queries the router over I2CP to lookup the LeaseSet to get the full Destination. Base32 lookups will only be successful when the Destination is up and publishing a LeaseSet. Because resolution may require a network database lookup, it may take significantly longer than a local address book lookup.

Base32 addresses can be used in most places where hostnames or full destinations are used, however there are some exceptions where they may fail if the name does not immediately resolve. I2PTunnel will fail, for example, if the name does not resolve to a destination.

---

## Extended Base32 Names

Extended base 32 names were introduced in release 0.9.40 to support encrypted lease sets. Addresses for encrypted leasesets are identified by 56 or more encoded characters, not including the ".b32.i2p" (35 or more decoded bytes), compared to 52 characters (32 bytes) for traditional base 32 addresses. See proposals 123 and 149 for additional information.

Standard Base 32 ("b32") addresses contain the hash of the destination. This will not work for encrypted ls2 (proposal 123).

You can't use a traditional base 32 address for an encrypted LS2 (proposal 123), as it contains only the hash of the destination. It does not provide the non-blinded public key. Clients must know the destination's public key, sig type, the blinded sig type, and an optional secret or private key to fetch and decrypt the leaseset. Therefore, a base 32 address alone is insufficient. The client needs either the full destination (which contains the public key), or the public key by itself. If the client has the full destination in an address book, and the address book supports reverse lookup by hash, then the public key may be retrieved.

So we need a new format that puts the public key instead of the hash into a base32 address. This format must also contain the signature type of the public key, and the signature type of the blinding scheme.

This section documents a new b32 format for these addresses. While we have referred to this new format during discussions as a "b33" address, the actual new format retains the usual ".b32.i2p" suffix.

### Creation and encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as follows. First, construct the binary data to be base 32 encoded:

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
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients, proxies, or other client-side code that the secret and/or private key will be required to decrypt the leaseset. Particular implementations may prompt the user to supply the required data, or reject connection attempts if the required data is missing.

### Notes

- XORing first 3 bytes with the hash provides a limited checksum capability, and ensures that all base32 chars at the beginning are randomized. Only a few flag and sigtype combinations are valid, so any typo is likely to create an invalid combination and will be rejected.
- In the usual case (1 byte sigtypes, no secret, no per-client auth), the hostname will be {56 chars}.b32.i2p, decoding to 35 bytes, same as Tor.
- Tor 2-byte checksum has a 1/64K false negative rate. With 3 bytes, minus a few ignored bytes, ours is approaching 1 in a million, since most flag/sigtype combinations are invalid.
- Adler-32 is a poor choice for small inputs, and for detecting small changes. We use CRC-32 instead. CRC-32 is fast and is widely available.
- While outside the scope of this specification, routers and/or clients must remember and cache (probably persistently) the mapping of public key to destination, and vice versa.
- Distinguish old from new flavors by length. Old b32 addresses are always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- Tor discussion thread [is here](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Don't expect 2-byte sigtypes to ever happen, we're only up to 13. No need to implement now.
- New format can be used in jump links (and served by jump servers) if desired, just like b32.
- Any secret, private key, or public key longer than 32 bytes would exceed the DNS max label length of 63 chars. Browsers probably do not care.
- No backward compatibility issues. Longer b32 addresses will fail to be converted to 32-byte hashes in old software.
