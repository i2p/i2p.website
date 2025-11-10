---
title: "Software Update Specification"
description: "Secure signed update mechanism and feed structure for I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Overview

Routers automatically check for updates by polling a signed news feed distributed through the I2P network. When a newer version is advertised, the router downloads a cryptographically signed update archive (`.su3`) and stages it for installation.  
This system ensures **authenticated, tamper-resistant**, and **multi-channel** distribution of official releases.

As of I2P 2.10.0, the update system uses:
- **RSA-4096 / SHA-512** signatures
- **SU3 container format** (replacing legacy SUD/SU2)
- **Redundant mirrors:** in-network HTTP, clearnet HTTPS, and BitTorrent

---

## 1. News Feed

Routers poll the signed Atom feed every few hours to discover new versions and security advisories.  
The feed is signed and distributed as a `.su3` file, which may include:

- `<i2p:version>` — new version number  
- `<i2p:minVersion>` — minimum supported router version  
- `<i2p:minJavaVersion>` — required minimum Java runtime  
- `<i2p:update>` — lists multiple download mirrors (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — certificate revocation data  
- `<i2p:blocklist>` — network-level blocklists for compromised peers  

### Feed Distribution

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>

Routers prefer the I2P feed but can fall back to clearnet or torrent distribution if necessary.

---

## 2. File Formats

### SU3 (Current Standard)

Introduced in 0.9.9, SU3 replaced the legacy SUD and SU2 formats.  
Each file contains a header, payload, and trailing signature.

**Header Structure**
<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
  </tbody>
</table>

**Signature Verification Steps**
1. Parse header and identify signature algorithm.  
2. Verify hash and signature using stored signer certificate.  
3. Confirm signer not revoked.  
4. Compare embedded version string with payload metadata.

Routers ship with trusted signer certificates (currently **zzz** and **str4d**) and reject any unsigned or revoked sources.

### SU2 (Obsolete)

- Used `.su2` extension with Pack200-compressed JARs.  
- Removed after Java 14 deprecated Pack200 (JEP 367).  
- Disabled in I2P 0.9.48+; now fully replaced by ZIP compression.

### SUD (Legacy)

- Early DSA-SHA1-signed ZIP format (pre-0.9.9).  
- No signer ID or header, limited integrity.  
- Superseded due to weak cryptography and lack of version enforcement.

---

## 3. Update Workflow

### 3.1 Header Verification

Routers fetch only the **SU3 header** to verify the version string before downloading full files.  
This prevents wasting bandwidth on stale mirrors or outdated versions.

### 3.2 Full Download

After verifying the header, the router downloads the complete `.su3` file from:
- In-network eepsite mirrors (preferred)  
- HTTPS clearnet mirrors (fallback)  
- BitTorrent (optional peer-assisted distribution)

Downloads use standard I2PTunnel HTTP clients, with retries, timeout handling, and mirror fallback.

### 3.3 Signature Verification

Each downloaded file undergoes:
- **Signature check:** RSA-4096/SHA512 verification  
- **Version matching:** Header vs. payload version check  
- **Downgrade prevention:** Ensures update is newer than installed version

Invalid or mismatched files are discarded immediately.

### 3.4 Installation Staging

Once verified:
1. Extract ZIP contents to temporary directory  
2. Remove files listed in `deletelist.txt`  
3. Replace native libraries if `lib/jbigi.jar` is included  
4. Copy signer certificates to `~/.i2p/certificates/`  
5. Move update to `i2pupdate.zip` for application on next restart  

The update installs automatically on next startup or when “Install update now” is triggered manually.

---

## 4. File Management

### deletelist.txt

A plaintext list of obsolete files to remove before unpacking new contents.

**Rules:**
- One path per line (relative paths only)
- Lines starting with `#` ignored
- `..` and absolute paths rejected

### Native Libraries

To prevent stale or mismatched native binaries:
- If `lib/jbigi.jar` exists, old `.so` or `.dll` files are deleted  
- Ensures platform-specific libraries are freshly extracted

---

## 5. Certificate Management

Routers can receive **new signer certificates** through updates or news feed revocations.

- New `.crt` files are copied to the certificate directory.  
- Revoked certificates are deleted before future verifications.  
- Supports key rotation without requiring manual user intervention.

All updates are signed offline using **air-gapped signing systems**.  
Private keys are never stored on build servers.

---

## 6. Developer Guidelines

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>

Future releases will explore post-quantum signature integration (see Proposal 169) and reproducible builds.

---

## 7. Security Overview

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>

---

## 8. Versioning

- Router: **2.10.0 (API 0.9.67)**  
- Semantic versioning with `Major.Minor.Patch`.  
- Minimum version enforcement prevents unsafe upgrades.  
- Supported Java: **Java 8–17**. Future 2.11.0+ will require Java 17+.  

---
