---
title: "I2P Mail (Anonymous Email over I2P)"
description: "An overview of email systems inside the I2P network — history, options, and current status"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Introduction

I2P provides private email-style messaging through **Postman's Mail.i2p service** combined with **SusiMail**, a built-in webmail client. This system allows users to send and receive emails both within the I2P network and to/from the regular internet (clearnet) via a gateway bridge.

---

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** is a hosted email provider inside I2P, run by "Postman"
- **SusiMail** is the webmail client integrated in the I2P router console. It is designed to avoid leaking metadata (e.g. hostname) to external SMTP servers.
- Through this setup, I2P users can send/receive messages both within I2P and to/from the clearnet (e.g. Gmail) via the Postman bridge.

### How Addressing Works

I2P email uses a dual-address system:

- **Inside I2P network**: `username@mail.i2p` (e.g., `idk@mail.i2p`)
- **From clearnet**: `username@i2pmail.org` (e.g., `idk@i2pmail.org`)

The `i2pmail.org` gateway allows regular internet users to send emails to I2P addresses, and I2P users to send to clearnet addresses. Internet emails are routed through the gateway before being forwarded through I2P to your SusiMail inbox.

**Clearnet sending quota**: 20 emails per day when sending to regular internet addresses.

### Getting Started

**To register for a mail.i2p account:**

1. Ensure your I2P router is running
2. Visit **[http://hq.postman.i2p](http://hq.postman.i2p)** inside I2P
3. Follow the registration process
4. Access your email through **SusiMail** in the router console

> **Note**: `hq.postman.i2p` is an I2P network address (eepsite) and can only be accessed while connected to I2P. For more information about email setup, security, and usage, visit Postman HQ.

### Privacy Features

- Automatic removal of identifying headers (`User-Agent:`, `X-Mailer:`) for privacy
- Metadata sanitization to prevent leaks to external SMTP servers
- End-to-end encryption for internal I2P-to-I2P emails

### Strengths

- Interoperability with "normal" email (SMTP/POP) via the Postman bridge
- Simple user experience (webmail built into router console)
- Integrated with I2P core distribution (SusiMail ships with Java I2P)
- Header stripping for privacy protection

### Considerations

- The bridge to external email requires trust in Postman infrastructure
- Clearnet bridge reduces privacy compared to purely internal I2P communication
- Reliant on the Postman mail server's availability and security

---

## Technical Details

**SMTP Service**: `localhost:7659` (provided by Postman)
**POP3 Service**: `localhost:7660`
**Webmail Access**: Built into router console at `http://127.0.0.1:7657/susimail/`

> **Important**: SusiMail is only for reading and sending email. Account creation and management must be done at **hq.postman.i2p**.

---

## Best Practices

- **Change your password** after registering your mail.i2p account
- **Use I2P-to-I2P email** whenever possible for maximum privacy (no clearnet bridge)
- **Be mindful of the 20/day limit** when sending to clearnet addresses
- **Understand the tradeoffs**: Clearnet bridging provides convenience but reduces anonymity compared to purely internal I2P communications
- **Keep I2P updated** to benefit from security improvements in SusiMail

---
