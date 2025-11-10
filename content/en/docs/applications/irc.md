---
title: "IRC over I2P"
description: "Complete guide to I2P IRC networks, clients, tunnels, and server setup (updated 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Overview


**Key points**

- I2P provides **end-to-end encryption** for IRC traffic through its tunnels. **Disable SSL/TLS** in IRC clients unless you are outproxying to clearnet.
- The preconfigured **Irc2P** client tunnel listens on **127.0.0.1:6668** by default. Connect your IRC client to that address and port.
- Do not use the term “router‑provided TLS.” Use “I2P’s native encryption” or “end‑to‑end encryption.”

## Quick start (Java I2P)

1. Open **Hidden Services Manager** at `http://127.0.0.1:7657/i2ptunnel/` and make sure the **Irc2P** tunnel is **running**.
2. In your IRC client, set **server** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **off**.
3. Connect and join channels like `#i2p`, `#i2p-dev`, `#i2p-help`.

For **i2pd** users (C++ router), create a client tunnel in `tunnels.conf` (see examples below).

## Networks and servers

### IRC2P (main community network)

- Federated servers: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- The **Irc2P** tunnel at `127.0.0.1:6668` connects to one of these automatically.
- Typical channels: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Servers: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Primary languages: Russian and English. Web front‑ends exist on some hosts.
## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — strong SOCKS support; easy to script.
- **Pidgin (desktop)** — still maintained; works well for Windows/Linux.
- **Thunderbird Chat (desktop)** — supported in ESR 128+.
- **The Lounge (self‑hosted web)** — modern web client.

### macOS options

- **LimeChat** (free, open source).
- **Textual** (paid on App Store; source available to build).


### Example configurations

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```

#### Pidgin

- Protocol: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- Encryption: **off**
- Username/nick: any

#### Thunderbird Chat

- Account type: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- SSL/TLS: **off**
- Optional: auto‑join channels on connect

#### Dispatch (SAM v3)

`config.toml` defaults example:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```

## Tunnel configuration

### Java I2P defaults

- Irc2P client tunnel: **127.0.0.1:6668** → upstream server on **port 6667**.
- Hidden Services Manager: `http://127.0.0.1:7657/i2ptunnel/`.

### i2pd client tunnels

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```

Separate tunnel for Ilita (example):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```

### SAM‑based apps (advanced)

- **Enable SAM** in Java I2P (off by default) at `/configclients` or `clients.config`.
- Defaults: **127.0.0.1:7656/TCP** and **127.0.0.1:7655/UDP**.
- Recommended crypto: `SIGNATURE_TYPE=7` (Ed25519) and `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 with ElGamal fallback) or just `4` for modern‑only.

### Tunnel quantities

- Java I2P default: **2 inbound / 2 outbound**.
- i2pd default: **5 inbound / 5 outbound**.
- For IRC: **2–3 each** is sufficient; set explicitly for consistent behavior across routers.

## Security guidance

- **Do not enable SSL/TLS** for internal I2P IRC connections. I2P already provides end‑to‑end encryption. Extra TLS adds overhead without anonymity gains.
- Use **persistent keys** for stable identity; avoid regenerating keys on every restart unless testing.
- If multiple apps use IRC, prefer **separate tunnels** (non‑shared) to reduce cross‑service correlation.
- If you must allow remote control (SAM/I2CP), bind to localhost and secure access with SSH tunnels or authenticated reverse proxies.

## Alternative connection method: SOCKS5

Some clients can connect via I2P’s SOCKS5 proxy: **127.0.0.1:4447**. For best results, prefer a dedicated IRC client tunnel on 6668; SOCKS cannot sanitize application‑layer identifiers and may leak info if the client is not designed for anonymity.

## Troubleshooting

- **Cannot connect** — ensure the Irc2P tunnel is running and the router is fully bootstrapped.
- **Hangs at resolve/join** — double‑check that SSL is **disabled** and the client points to **127.0.0.1:6668**.
- **High latency** — I2P is higher‑latency by design. Keep tunnel quantities modest (2–3) and avoid rapid reconnect loops.
- **Using SAM apps** — confirm SAM is enabled (Java) or not firewalled (i2pd). Long‑lived sessions are recommended.

## Appendix: Ports and naming

- Common IRC tunnel ports: **6668** (Irc2P default), **6667** and **6669** as alternates.
- `.b32.i2p` hostnames: 52‑character standard form; extended 56+ character forms exist for LS2/advanced certs. Use `.i2p` hostnames unless you explicitly need b32 addresses.
