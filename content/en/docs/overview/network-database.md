---
title: "Network Database"
description: "Understanding I2P's distributed network database (netDb) - a specialized DHT for router contact information and destination lookups"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Overview

The **netDb** is a specialized distributed database containing just two types of data:
- **RouterInfos** – router contact information
- **LeaseSets** – destination contact information

All data is cryptographically signed and verifiable. Each entry includes liveliness information for dropping obsolete entries and replacing outdated ones, protecting against certain attack classes.

Distribution uses a **floodfill** mechanism, where a subset of routers maintains the distributed database.

---

## 2. RouterInfo

When routers need to contact other routers, they exchange **RouterInfo** bundles containing:

- **Router identity** – encryption key, signing key, certificate
- **Contact addresses** – how to reach the router
- **Publication timestamp** – when this info was published
- **Arbitrary text options** – capability flags and settings
- **Cryptographic signature** – proves authenticity

### 2.1 Capability Flags

Routers advertise capabilities through letter codes in their RouterInfo:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>

### 2.2 Bandwidth Classifications

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>

### 2.3 Network ID Values

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>

### 2.4 RouterInfo Statistics

Routers publish optional health statistics for network analysis:
- Exploratory tunnel build success/reject/timeout rates
- 1-hour average participating tunnel count

Stats follow the format `stat_(statname).(statperiod)` with semicolon-separated values.

**Example Statistics:**
```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```

Floodfill routers may also publish: `netdb.knownLeaseSets` and `netdb.knownRouters`

### 2.5 Family Options

As of release 0.9.24, routers can declare family membership (same operator):

- **family**: Family name
- **family.key**: Signature type code concatenated with base64-encoded signing public key
- **family.sig**: Signature of family name and 32-byte router hash

Multiple routers in the same family won't be used in single tunnels.

### 2.6 RouterInfo Expiration

- No expiration during first hour of uptime
- No expiration with 25 or fewer stored RouterInfos
- Expiration shrinks as local count grows (72 hours at <120 routers; ~30 hours at 300 routers)
- SSU introducers expire in ~1 hour
- Floodfills use 1-hour expiration for all local RouterInfos

---

## 3. LeaseSet

**LeaseSets** document tunnel entry points for particular destinations, specifying:

- **Tunnel gateway router identity**
- **4-byte tunnel ID**
- **Tunnel expiration time**

LeaseSets include:
- **Destination** – encryption key, signing key, certificate
- **Additional encryption public key** – for end-to-end garlic encryption
- **Additional signing public key** – intended for revocation (currently unused)
- **Cryptographic signature**

### 3.1 LeaseSet Variants

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>

### 3.2 LeaseSet Expiration

Regular LeaseSets expire at their latest lease expiration. LeaseSet2 expiration is specified in the header. EncryptedLeaseSet and MetaLeaseSet expirations may vary with possible maximum enforcement.

---

## 4. Bootstrapping

The decentralized netDb requires at least one peer reference to integrate. **Reseeding** retrieves RouterInfo files (`routerInfo-$hash.dat`) from volunteers' netDb directories. First startup automatically fetches from hardcoded URLs selected randomly.

---

## 5. Floodfill Mechanism

The floodfill netDb uses simple distributed storage: send data to the closest floodfill peer. When non-floodfill peers send stores, floodfills forward to a subset of floodfill peers closest to the specific key.

Floodfill participation is indicated as a capability flag (`f`) in RouterInfo.

### 5.1 Floodfill Opt-In Requirements

Unlike Tor's hardcoded trusted directory servers, I2P's floodfill set is **untrusted** and changes over time.

Floodfill automatically enables only on high-bandwidth routers meeting these requirements:
- Minimum 128 KBytes/sec shared bandwidth (manually configured)
- Must pass additional health tests (outbound message queue time, job lag)

Current automatic opt-in results in approximately **6% network floodfill participation**.

Manually configured floodfills exist alongside automatic volunteers. When floodfill count drops below threshold, high-bandwidth routers automatically volunteer. When too many floodfills exist, they un-floodfill themselves.

### 5.2 Floodfill Roles

Beyond accepting netDb stores and responding to queries, floodfills perform standard router functions. Their higher bandwidth typically means more tunnel participation, but this isn't directly related to database services.

---

## 6. Kademlia Closeness Metric

The netDb uses XOR-based **Kademlia-style** distance measurement. The SHA256 hash of RouterIdentity or Destination creates the Kademlia key (except for LS2 Encrypted LeaseSets, which use SHA256 of type byte 3 plus blinded public key).

### 6.1 Keyspace Rotation

To increase Sybil attack costs, instead of using `SHA256(key)`, the system uses:

```
SHA256(key + yyyyMMdd)
```

where the date is an 8-byte ASCII UTC date. This creates the **routing key**, changing daily at midnight UTC—called **keyspace rotation**.

Routing keys are never transmitted in I2NP messages; they're used only for local distance determination.

---

## 7. Network Database Segmentation

Traditional Kademlia DHTs don't preserve unlinkability of stored information. I2P prevents attacks associating client tunnels with routers by implementing **segmentation**.

### 7.1 Segmentation Strategy

Routers track:
- Whether entries arrived via client tunnels or directly
- If via tunnel, which client tunnel/destination
- Multiple tunnel arrivals are tracked
- Storage vs. lookup replies are distinguished

Both Java and C++ implementations use:
- A **"Main" netDb** for direct lookups/floodfill operations in router context
- **"Client Network Databases"** or **"Sub-Databases"** in client contexts, capturing entries sent to client tunnels

Client netDbs exist for client lifetime only, containing only client tunnel entries. Entries from client tunnels cannot overlap with direct arrivals.

Each netDb tracks whether entries arrived as stores (respond to lookup requests) or as lookup replies (only respond if previously stored to same destination). Clients never answer queries with Main netDb entries, only client network database entries.

Combined strategies **segment** the netDb against client-router association attacks.

---

## 8. Storage, Verification, and Lookup

### 8.1 RouterInfo Storage to Peers

I2NP `DatabaseStoreMessage` containing local RouterInfo exchange during NTCP or SSU transport connection initialization.

### 8.2 LeaseSet Storage to Peers

I2NP `DatabaseStoreMessage` containing local LeaseSet periodically exchange via garlic-encrypted messages bundled with Destination traffic, allowing responses without LeaseSet lookups.

### 8.3 Floodfill Selection

`DatabaseStoreMessage` sends to the floodfill closest to the current routing key. Closest floodfill found via local database search. Even if not actually closest, flooding spreads it "closer" by sending to multiple floodfills.

Traditional Kademlia uses "find-closest" search before insertion. While I2NP lacks such messages, routers may perform iterative search with least significant bit flipped (`key ^ 0x01`) to ensure true closest peer discovery.

### 8.4 RouterInfo Storage to Floodfills

Routers publish RouterInfo by directly connecting to a floodfill, sending I2NP `DatabaseStoreMessage` with nonzero Reply Token. Message isn't end-to-end garlic encrypted (direct connection, no intermediaries). Floodfill replies with `DeliveryStatusMessage` using Reply Token as Message ID.

Routers may also send RouterInfo via exploratory tunnel (connection limits, incompatibility, IP hiding). Floodfills may reject such stores during overload.

### 8.5 LeaseSet Storage to Floodfills

LeaseSet storage is more sensitive than RouterInfo. Routers must prevent LeaseSet association with themselves.

Routers publish LeaseSet via outbound client tunnel `DatabaseStoreMessage` with nonzero Reply Token. Message is end-to-end garlic encrypted using Destination's Session Key Manager, hiding from tunnel's outbound endpoint. Floodfill replies with `DeliveryStatusMessage` returned via inbound tunnel.

### 8.6 Flooding Process

Floodfills validate RouterInfo/LeaseSet before storing locally using adaptive criteria dependent on load, netdb size, and other factors.

After receiving valid newer data, floodfills "flood" it by looking up 3 closest floodfill routers to the routing key. Direct connections send I2NP `DatabaseStoreMessage` with zero Reply Token. Other routers don't reply or re-flood.

**Important constraints:**
- Floodfills must not flood via tunnels; direct connections only
- Floodfills never flood expired LeaseSet or RouterInfo published over one hour ago

### 8.7 RouterInfo and LeaseSet Lookup

I2NP `DatabaseLookupMessage` requests netdb entries from floodfill routers. Lookups send via outbound exploratory tunnel; replies specify inbound exploratory tunnel return.

Lookups generally send to two "good" floodfill routers closest to requested key, in parallel.

- **Local match**: receives I2NP `DatabaseStoreMessage` response
- **No local match**: receives I2NP `DatabaseSearchReplyMessage` with other floodfill router references close to the key

LeaseSet lookups use end-to-end garlic encryption (as of 0.9.5). RouterInfo lookups aren't encrypted due to ElGamal expense, making them vulnerable to outbound endpoint snooping.

As of 0.9.7, lookup replies include session key and tag, hiding replies from inbound gateway.

### 8.8 Iterative Lookups

Pre-0.8.9: Two parallel redundant lookups without recursive or iterative routing.

As of 0.8.9: **Iterative lookups** implemented without redundancy—more efficient, reliable, and suited to incomplete floodfill knowledge. As networks grow and routers know fewer floodfills, lookups approach O(log n) complexity.

Iterative lookups continue even without closer peer references, preventing malicious black-holing. Current maximum query count and timeout apply.

### 8.9 Verification

**RouterInfo Verification**: Disabled as of 0.9.7.1 to prevent attacks described in "Practical Attacks Against the I2P Network" paper.

**LeaseSet Verification**: Routers wait ~10 seconds, then lookup from different floodfill via outbound client tunnel. End-to-end garlic encryption hides from outbound endpoint. Replies return via inbound tunnels.

As of 0.9.7, replies encrypt with session key/tag hiding from inbound gateway.

### 8.10 Exploration

**Exploration** involves netdb lookup with random keys to learn new routers. Floodfills respond with `DatabaseSearchReplyMessage` containing non-floodfill router hashes close to the requested key. Exploration queries set a special flag in `DatabaseLookupMessage`.

---

## 9. MultiHoming

Destinations using identical private/public keys (traditional `eepPriv.dat`) can host on multiple routers simultaneously. Each instance periodically publishes signed LeaseSets; the most recent published LeaseSet returns to lookup requesters. With maximum 10-minute LeaseSet lifetimes, outages last at most ~10 minutes.

As of 0.9.38, **Meta LeaseSets** support large multihomed services using separate Destinations providing common services. Meta LeaseSet entries are Destinations or other Meta LeaseSets with up to 18.2-hour expirations, enabling hundreds/thousands of Destinations hosting common services.

---

## 10. Threat Analysis

Approximately 1700 floodfill routers currently operate. Network growth makes most attacks more difficult or less impactful.

### 10.1 General Mitigations

- **Growth**: More floodfills make attacks harder or less impactful
- **Redundancy**: All netdb entries store on 3 floodfill routers closest to the key via flooding
- **Signatures**: All entries are creator-signed; forgeries are impossible

### 10.2 Slow or Unresponsive Routers

Routers maintain expanded peer profile statistics for floodfills:
- Average response time
- Query answer percentage
- Store verification success percentage
- Last successful store
- Last successful lookup
- Last response

Routers use these metrics when determining "goodness" for selecting closest floodfill. Completely unresponsive routers are quickly identified and avoided; partially malicious routers pose greater challenge.

### 10.3 Sybil Attack (Full Keyspace)

Attackers might create numerous floodfill routers distributed throughout keyspace as an effective DOS attack.

If not misbehaving sufficiently for "bad" designation, possible responses include:
- Compiling bad router hash/IP lists announced via console news, website, forum
- Network-wide floodfill enablement ("fight Sybil with more Sybil")
- New software versions with hardcoded "bad" lists
- Improved peer profile metrics and thresholds for automatic identification
- IP block qualification disqualifying multiple floodfills in single IP block
- Automatic subscription-based blacklist (similar to Tor consensus)

Larger networks make this harder.

### 10.4 Sybil Attack (Partial Keyspace)

Attackers might create 8–15 floodfill routers clustered closely in keyspace. All lookups/stores for that keyspace direct to attacker routers, enabling DOS on particular I2P sites.

Since keyspace indexes cryptographic SHA256 hashes, attackers need brute-force to generate routers with sufficient proximity.

**Defense**: The Kademlia closeness algorithm varies over time using `SHA256(key + YYYYMMDD)`, changing daily at UTC midnight. This **keyspace rotation** forces daily attack regeneration.

> **Note**: Recent research shows keyspace rotation isn't particularly effective—attackers can precompute router hashes, requiring only several routers to eclipse keyspace portions within half-hour post-rotation.

Daily rotation consequence: distributed netdb becomes unreliable for minutes after rotation—lookups fail before new closest router receives stores.

### 10.5 Bootstrap Attacks

Attackers could take over reseed websites or trick developers into adding hostile reseed websites, booting new routers into isolated/majority-controlled networks.

**Implemented Defenses:**
- Fetch RouterInfo subsets from multiple reseed sites rather than single site
- Out-of-network reseed monitoring periodically polling sites
- As of 0.9.14, reseed data bundles as signed zip files with downloaded signature verification (see [su3 specification](/docs/specs/updates))

### 10.6 Query Capture

Floodfill routers might "steer" peers to attacker-controlled routers via returned references.

Unlikely via exploration due to low frequency; routers acquire peer references mainly via normal tunnel building.

As of 0.8.9, iterative lookups implemented. `DatabaseSearchReplyMessage` floodfill references followed if closer to lookup key. Requesting routers don't trust reference closeness. Lookups continue despite no closer keys until timeout/maximum queries, preventing malicious black-holing.

### 10.7 Information Leaks

DHT information leakage in I2P needs further investigation. Floodfill routers observe queries gathering information. At 20% malicious node levels, previously described Sybil threats become problematic for multiple reasons.

---

## 11. Future Work

- End-to-end encryption of additional netDb lookups and responses
- Better lookup response tracking methods
- Mitigation methods for keyspace rotation reliability issues

---

## 12. References

- [Common Structures Specification](/docs/specs/common-structures/) – RouterInfo and LeaseSet structures
- [I2NP Specification](/docs/specs/i2np/) – Database message types
- [Proposal 123: New netDb Entries](/proposals/123-new-netdb-entries) – LeaseSet2 specification
- [Historical netDb Discussion](/docs/netdb/) – Development history and archived discussions
