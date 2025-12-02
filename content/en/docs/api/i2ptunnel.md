---
title: "I2PTunnel"
description: "Tool for interfacing with and providing services on I2P"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - /docs/api/i2ptunnel/
---

## Overview

I2PTunnel is a core I2P component for interfacing with and providing services on the I2P network. It enables TCP-based and media streaming applications to operate anonymously through tunnel abstraction. A tunnel’s destination can be defined by a [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), or a full destination key. 

Each established tunnel listens locally (e.g., `localhost:port`) and connects internally to I2P destinations. To host a service, create a tunnel pointing to the desired IP and port. A corresponding I2P destination key is generated, allowing the service to become globally reachable within the I2P network. The I2PTunnel web interface is available at [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Default Services

### Server tunnel

- **I2P Webserver** – A tunnel to a Jetty webserver at [localhost:7658](http://localhost:7658) for easy hosting on I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Client tunnels

- **I2P HTTP Proxy** – `localhost:4444` – Used for browsing I2P and the Internet through outproxies.  
- **I2P HTTPS Proxy** – `localhost:4445` – Secure variant of the HTTP proxy.  
- **Irc2P** – `localhost:6668` – Default anonymous IRC network tunnel.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Client tunnel for repository SSH access.  
- **Postman SMTP** – `localhost:7659` – Client tunnel for outgoing mail.  
- **Postman POP3** – `localhost:7660` – Client tunnel for incoming mail.

> Note: Only the I2P Webserver is a default **server tunnel**; all others are client tunnels connecting to external I2P services.

---

## Configuration

The I2PTunnel configuration specification is documented at [/spec/configuration](/docs/specs/configuration/).

---

## Client Modes

### Standard

Opens a local TCP port that connects to a service on an I2P destination. Supports multiple destination entries separated by commas for redundancy.

### HTTP

A proxy tunnel for HTTP/HTTPS requests. Supports local and remote outproxies, header stripping, caching, authentication, and transparent compression.

**Privacy protections:**  
- Strips headers: `Accept-*`, `Referer`, `Via`, `From`  
- Replaces host headers with Base32 destinations  
- Enforces RFC-compliant hop-by-hop stripping  
- Adds support for transparent decompression  
- Provides internal error pages and localized responses  

**Compression behavior:**  
- Requests may use custom header `X-Accept-Encoding: x-i2p-gzip`  
- Responses with `Content-Encoding: x-i2p-gzip` are transparently decompressed  
- Compression evaluated by MIME type and response length for efficiency  

**Persistence (new since 2.5.0):**  
HTTP Keepalive and persistent connections are now supported for I2P-hosted services through the Hidden Services Manager. This reduces latency and connection overhead but does not yet enable full RFC 2616-compliant persistent sockets across all hops.

**Pipelining:**  
Remains unsupported and unnecessary; modern browsers have deprecated it.

**User-Agent behavior:**  
- **Outproxy:** Uses a current Firefox ESR User-Agent.  
- **Internal:** `MYOB/6.66 (AN/ON)` for anonymity consistency.

### IRC Client

Connects to I2P-based IRC servers. Allows a safe subset of commands while filtering identifiers for privacy.

### SOCKS 4/4a/5

Provides SOCKS proxy capability for TCP connections. UDP remains unimplemented in Java I2P (only in i2pd).

### CONNECT

Implements HTTP `CONNECT` tunneling for SSL/TLS connections.

### Streamr

Enables UDP-style streaming via TCP-based encapsulation. Supports media streaming when paired with a corresponding Streamr server tunnel.

![I2PTunnel Streamr diagram](/images/I2PTunnel-streamr.png)

---

## Server Modes

### Standard Server

Creates a TCP destination mapped to a local IP:port.

### HTTP Server

Creates a destination that interfaces with a local web server. Supports compression (`x-i2p-gzip`), header stripping, and DDoS protections. Now benefits from **persistent connection support** (v2.5.0+) and **thread pooling optimization** (v2.7.0–2.9.0).

### HTTP Bidirectional

**Deprecated** – Still functional but discouraged. Acts as both HTTP server and client without outproxying. Primarily used for diagnostic loopback tests.

### IRC Server

Creates a filtered destination for IRC services, passing client destination keys as hostnames.

### Streamr Server

Couples with a Streamr client tunnel to handle UDP-style data streams over I2P.

---

## New Features (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>

---

## Security Features

- **Header stripping** for anonymity (Accept, Referer, From, Via)
- **User-Agent randomization** depending on in/outproxy
- **POST rate limiting** and **Slowloris protection**
- **Connection throttling** in streaming subsystems
- **Network congestion handling** at tunnel layer
- **NetDB isolation** preventing cross-application leaks

---

## Technical Details

- Default destination key size: 516 bytes (may exceed for extended LS2 certificates)  
- Base32 addresses: `{52–56+ chars}.b32.i2p`  
- Server tunnels remain compatible with both Java I2P and i2pd  
- Deprecated feature: `httpbidirserver` only; no removals since 0.9.59  
- Verified correct default ports and document roots for all platforms

---

## Summary

I2PTunnel remains the backbone of application integration with I2P. Between 0.9.59 and 2.10.0, it gained persistent connection support, post-quantum encryption, and major threading improvements. Most configurations remain compatible, but developers should verify their setups to ensure compliance with modern transport and security defaults.
