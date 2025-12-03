---
title: "Naming and Address Book"
description: "How I2P maps human-readable hostnames to destinations"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /en/docs/naming
  - /naming/
  - /spec/common-structures/naming/
  - /docs/overview/naming/
  - /en/docs/naming/
---

I2P addresses are long cryptographic keys. The naming system provides a friendlier layer on top of those keys **without introducing a central authority**.  
All names are **local**—each router independently decides which destination a hostname refers to.

> **Need background?** The [naming discussion](/docs/legacy/naming/) documents the original design debates, alternative proposals, and philosophical foundations behind I2P's decentralized naming.

---

## 1. Components

I2P’s naming layer is composed of several independent but cooperating subsystems:

1. **Naming service** – resolves hostnames to destinations and handles [Base32 hostnames](#base32-hostnames).
2. **HTTP proxy** – passes `.i2p` lookups to the router and suggests jump services when a name is unknown.
3. **Host-add services** – CGI-style forms that append new entries into the local address book.
4. **Jump services** – remote helpers that return the destination for a supplied hostname.
5. **Address book** – periodically fetches and merges remote host lists using a locally trusted “web of trust”.
6. **SusiDNS** – a web-based UI for managing address books, subscriptions, and local overrides.

This modular design lets users define their own trust boundaries and automate as much or as little of the naming process as they prefer.

---

## 2. Naming Services

The router’s naming API (`net.i2p.client.naming`) supports multiple backends through the configurable property  
`i2p.naming.impl=<class>`. Each implementation may offer different lookup strategies, but all share the same trust and resolution model.

### 2.1 Hosts.txt (legacy format)

The legacy model used three plain-text files checked in order:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Each line stores a `hostname=base64-destination` mapping.  
This simple text format remains fully supported for import/export, but it’s no longer the default due to poor performance once the host list exceeds a few thousand entries.

---

### 2.2 Blockfile Naming Service (default backend)

Introduced in **release 0.8.8**, the Blockfile Naming Service is now the default backend.  
It replaces flat files with a high-performance skiplist-based on-disk key/value store (`hostsdb.blockfile`) that delivers roughly **10× faster lookups**.

**Key characteristics:**
- Stores multiple logical address books (private, user, and hosts) in one binary database.
- Maintains compatibility with legacy hosts.txt import/export.
- Supports reverse lookups, metadata (added date, source, comments), and efficient caching.
- Uses the same three-tier search order: private → user → hosts.

This approach preserves backwards compatibility while dramatically improving resolution speed and scalability.

---

### 2.3 Alternative Backends and Plug-ins

Developers can implement custom backends such as:
- **Meta** – aggregates multiple naming systems.
- **PetName** – supports petnames stored in a `petnames.txt`.
- **AddressDB**, **Exec**, **Eepget**, and **Dummy** – for external or fallback resolution.
  
The blockfile implementation remains the **recommended** backend for general use due to performance and reliability.

---

## 3. Base32 Hostnames

Base32 hostnames (`*.b32.i2p`) function similarly to Tor’s `.onion` addresses.  
When you access a `.b32.i2p` address:

1. The router decodes the Base32 payload.
2. It reconstructs the destination directly from the key—**no address-book lookup required**.

This guarantees reachability even if no human-readable hostname exists.  
Extended Base32 names introduced in **release 0.9.40** support **LeaseSet2** and encrypted destinations.

---

## 4. Address Book & Subscriptions

The address book application retrieves remote host lists over HTTP and merges them locally according to user-configured trust rules.

### 4.1 Subscriptions

- Subscriptions are standard `.i2p` URLs pointing to `hosts.txt` or incremental update feeds.
- Updates are fetched periodically (hourly by default) and validated before merging.
- Conflicts are resolved **first-come, first-served**, following the priority order:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Since **I2P 2.3.0 (June 2023)**, two default subscription providers are included:
- `http://i2p-projekt.i2p/hosts.txt`
- `http://notbob.i2p/hosts.txt`

This redundancy improves reliability while preserving the local trust model.  
Users may add or remove subscriptions through SusiDNS.

#### Incremental Updates

Incremental updates are fetched via `newhosts.txt` (replacing the older `recenthosts.cgi` concept).  
This endpoint provides efficient, **ETag-based** delta updates—returning only new entries since the last request or `304 Not Modified` when unchanged.

---

### 4.2 Host-Add and Jump Services

- **Host-add services** (`add*.cgi`) allow manual submission of name-to-destination mappings. Always verify the destination before accepting.  
- **Jump services** respond with the appropriate key and can redirect through the HTTP proxy with an `?i2paddresshelper=` parameter.  
  Common examples: `stats.i2p`, `identiguy.i2p`, and `notbob.i2p`.  
  These services are **not trusted authorities**—users must decide which to use.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS is available at:  
`http://127.0.0.1:7657/susidns/`

You can:
- View and edit local address books.
- Manage and prioritize subscriptions.
- Import/export hosts lists.
- Configure fetch schedules.

**New in I2P 2.8.1 (March 2025):**
- Added a “sort by latest” feature.
- Improved subscription handling (fix for ETag inconsistencies).

All changes remain **local**—each router’s address book is unique.

---

## 6. `.i2p.alt` and DNS Leak Prevention

Following RFC 9476, I2P registered **`.i2p.alt`** with the GNUnet Assigned Numbers Authority (GANA) as of **March 2025 (I2P 2.8.1)**.

**Purpose:** Prevent accidental DNS leaks from misconfigured software.

- RFC 9476-compliant DNS resolvers will **not forward** `.alt` domains to the public DNS.
- I2P software treats `.i2p.alt` as equivalent to `.i2p`, stripping the `.alt` suffix during resolution.
- `.i2p.alt` is **not** intended to replace `.i2p`; it’s a technical safeguard, not a rebranding.

---

## 7. Technical Specifications 

- **Destination keys:** 516–616 bytes (Base64)  
- **Hostnames:** Max 67 characters (including `.i2p`)  
- **Allowed characters:** a–z, 0–9, `-`, `.` (no double dots, no uppercase)  
- **Reserved:** `*.b32.i2p`  
- **ETag and Last-Modified:** actively used to minimize bandwidth  
- **Average hosts.txt size:** ~400 KB for ~800 hosts (example figure)  
- **Bandwidth use:** ~10 bytes/sec if fetched every 12 hours  

---

## 8. Security Model and Philosophy

I2P intentionally sacrifices global uniqueness in exchange for decentralization and security—a direct application of **Zooko’s Triangle**.

**Key principles:**
- **No central authority:** all lookups are local.  
- **Resistance to DNS hijacking:** queries are encrypted to destination public keys.  
- **Sybil-attack prevention:** no voting or consensus-based naming.  
- **Immutable mappings:** once a local association exists, it cannot be remotely overridden.

Blockchain-based naming systems (e.g., Namecoin, ENS) have explored solving all three sides of Zooko’s triangle, but I2P intentionally avoids them due to latency, complexity, and philosophical incompatibility with its local trust model.

---

## 9. Compatibility and Stability

- No naming features have been deprecated between 2023–2025.
- Hosts.txt format, jump services, subscriptions, and all naming API implementations remain functional.
- The I2P Project maintains strict **backwards compatibility** while introducing performance and security improvements (NetDB isolation, Sub-DB separation, etc.).

---

## 10. Best Practices

- Keep only trusted subscriptions; avoid large, unknown host lists.
- Back up `hostsdb.blockfile` and `privatehosts.txt` before upgrading or reinstalling.
- Regularly review jump services and disable any you no longer trust.
- Remember: your address book defines your version of the I2P world—**every hostname is local**.

---

### Further Reading

- [Naming Discussion](/docs/legacy/naming/)  
- [Blockfile Specification](/docs/specs/blockfile/)  
- [Configuration File Format](/docs/specs/configuration/)  
- [Naming Service Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
