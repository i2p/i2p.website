---
title: "SOCKS Proxy"
description: "Using I2P's SOCKS tunnel safely (updated for 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /docs/api/socks/
---

> **Caution:** The SOCKS tunnel forwards application payloads without sanitizing them. Many protocols leak IPs, hostnames, or other identifiers. Only use SOCKS with software you have audited for anonymity.

---

## 1. Overview

I2P provides **SOCKS 4, 4a, and 5** proxy support for outbound connections through an **I2PTunnel client**. It enables standard applications to reach I2P destinations but **cannot access clearnet**. There is **no SOCKS outproxy**, and all traffic remains within the I2P network.

### Implementation Summary

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>

**Supported address types:**
- `.i2p` hostnames (addressbook entries)
- Base32 hashes (`.b32.i2p`)
- No Base64 or clearnet support

---

## 2. Security Risks and Limitations

### Application-Layer Leakage

SOCKS operates below the application layer and cannot sanitize protocols. Many clients (e.g., browsers, IRC, email) include metadata that reveals your IP address, hostname, or system details.

Common leaks include:
- IPs in mail headers or IRC CTCP responses  
- Real names/usernames in protocol payloads  
- User-agent strings with OS fingerprints  
- External DNS queries  
- WebRTC and browser telemetry  

**I2P cannot prevent these leaks**—they occur above the tunnel layer. Only use SOCKS for **audited clients** designed for anonymity.

### Shared Tunnel Identity

If multiple applications share a SOCKS tunnel, they share the same I2P destination identity. This enables correlation or fingerprinting across different services.

**Mitigation:** Use **non-shared tunnels** for each application and enable **persistent keys** to maintain consistent cryptographic identities across restarts.

### UDP Mode Stubbed Out

UDP support in SOCKS5 is not implemented. The protocol advertises UDP capability, but calls are ignored. Use TCP-only clients.

### No Outproxy by Design

Unlike Tor, I2P does **not** offer SOCKS-based clearnet outproxies. Attempts to reach external IPs will fail or expose identity. Use HTTP or HTTPS proxies if outproxying is required.

---

## 3. Historical Context

Developers have long discouraged SOCKS for anonymous use. From internal developer discussions and the 2004 [Meeting 81](/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) and [Meeting 82](/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> “Forwarding arbitrary traffic is unsafe, and it behooves us as developers of anonymity software to have the safety of our end users foremost in our minds.”

SOCKS support was included for compatibility but is not recommended for production environments. Nearly every internet application leaks sensitive metadata unsuited to anonymous routing.

---

## 4. Configuration

### Java I2P

1. Open the [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Create a new client tunnel of type **“SOCKS 4/4a/5”**  
3. Configure options:  
   - Local port (any available)  
   - Shared client: *disable* for separate identity per app  
   - Persistent key: *enable* to reduce key correlation  
4. Start the tunnel

### i2pd

i2pd includes SOCKS5 support enabled by default at `127.0.0.1:4447`. Configuration in `i2pd.conf` under `[SOCKSProxy]` allows you to adjust port, host, and tunnel parameters.

---

## 5. Development Timeline

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>

The SOCKS module itself has seen no major protocol updates since 2013, but the surrounding tunnel stack has received performance and cryptographic improvements.

---

## 6. Recommended Alternatives

For any **production**, **public-facing**, or **security-critical** application, use one of the official I2P APIs instead of SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>

These APIs provide proper destination isolation, cryptographic identity control, and better routing performance.

---

## 7. OnionCat / GarliCat

OnionCat supports I2P through its GarliCat mode (`fd60:db4d:ddb5::/48` IPv6 range). Still functional but with limited development since 2019.

**Usage caveats:**
- Requires manual `.oc.b32.i2p` configuration in SusiDNS  
- Needs static IPv6 assignment  
- Not officially supported by the I2P project  

Recommended only for advanced VPN-over-I2P setups.

---

## 8. Best Practices

If you must use SOCKS:
1. Create separate tunnels per application.  
2. Disable shared client mode.  
3. Enable persistent keys.  
4. Force SOCKS5 DNS resolution.  
5. Audit protocol behavior for leaks.  
6. Avoid clearnet connections.  
7. Monitor network traffic for leaks.

---

## 9. Technical Summary

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>

---

## 10. Conclusion

The SOCKS proxy in I2P provides basic compatibility with existing TCP applications but is **not designed for strong anonymity guarantees**. It should only be used for controlled, audited testing environments.

> For serious deployments, migrate to **SAM v3** or the **Streaming API**. These APIs isolate application identities, use modern cryptography, and receive ongoing development.

---

### Additional Resources

- [Official SOCKS Docs](/docs/api/socks/)  
- [SAM v3 Specification](/docs/api/samv3/)  
- [Streaming Library Docs](/docs/specs/streaming/)  
- [I2PTunnel Reference](/docs/specs/implementation/)  
- [I2P Developer Docs](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Community Forum](https://i2pforum.net)

