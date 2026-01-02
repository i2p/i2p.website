---
title: "Embedding I2P in Your Application"
description: "Updated practical guidance for bundling an I2P router with your app responsibly"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Bundling I2P with your application is a powerful way to onboard users—but only if the router is configured responsibly. 

## 1. Coordinate with Router Teams

- Contact the **Java I2P** and **i2pd** maintainers before bundling. They can review your defaults and highlight compatibility concerns.
- Choose the router implementation that fits your stack:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Other languages** → bundle a router and integrate using [SAM v3](/docs/api/samv3/) or [I2CP](/docs/specs/i2cp/)
- Verify redistribution terms for router binaries and dependencies (Java runtime, ICU, etc.).

## 2. Recommended Configuration Defaults

Aim for “contribute more than you consume.” Modern defaults prioritize network health and stability.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>

### Participating Tunnels Remain Essential

Do **not** disable participating tunnels.

1. Routers that don’t relay perform worse themselves.  
2. The network depends on voluntary capacity sharing.  
3. Cover traffic (relayed traffic) improves anonymity.

**Official minimums:**
- Shared bandwidth: ≥ 12 KB/s  
- Floodfill auto-opt-in: ≥ 128 KB/s  
- Recommended: 2 inbound / 2 outbound tunnels (Java I2P default)

## 3. Persistence and Reseeding

Persistent state directories (`netDb/`, profiles, certificates) must be preserved between runs.

Without persistence, your users will trigger reseeds at every startup—degrading performance and increasing load on reseed servers.

If persistence is impossible (e.g., containers or ephemeral installs):

1. Bundle **1,000–2,000 router infos** in the installer.  
2. Operate one or more custom reseed servers to offload public ones.

Configuration variables:
- Base directory: `i2p.dir.base`
- Config directory: `i2p.dir.config`
- Include `certificates/` for reseeding.

## 4. Security and Exposure

- Keep router console (`127.0.0.1:7657`) local-only.  
- Use HTTPS if exposing UI externally.  
- Disable external SAM/I2CP unless required.  
- Review included plugins—ship only what your app supports.  
- Always include authentication for remote console access.

**Security features introduced since 2.5.0:**
- NetDB isolation between applications (2.4.0+)  
- DoS mitigation and Tor blocklists (2.5.1)  
- NTCP2 probing resistance (2.9.0)  
- Floodfill router selection improvements (2.6.0+)

## 5. Supported APIs (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>

All official docs are located under `/docs/api/` — the old `/spec/samv3/` path does **not** exist.

## 6. Networking and Ports

Typical default ports:
- 4444 – HTTP Proxy  
- 4445 – HTTPS Proxy  
- 7654 – I2CP  
- 7656 – SAM Bridge  
- 7657 – Router Console  
- 7658 – Local I2P site  
- 6668 – IRC Proxy  
- 9000–31000 – Random router port (UDP/TCP inbound)

Routers select a random inbound port on first run. Forwarding improves performance, but UPnP may handle this automatically.

## 7. Modern Changes (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>

## 8. User Experience and Testing

- Communicate what I2P does and why bandwidth is shared.
- Provide router diagnostics (bandwidth, tunnels, reseed status).
- Test bundles on Windows, macOS, and Linux (low-RAM included).
- Verify interop with both **Java I2P** and **i2pd** peers.
- Test recovery from network drops and ungraceful exits.

## 9. Community Resources

- Forum: [i2pforum.net](https://i2pforum.net) or `http://i2pforum.i2p` inside I2P.  
- Code: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (Irc2P network): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` unverified; may not exist.  
  - Clarify which network (Irc2P vs ilita.i2p) hosts your channel.

Embedding responsibly means balancing user experience, performance, and network contribution. Use these defaults, stay in sync with router maintainers, and test under real-world load before release.
