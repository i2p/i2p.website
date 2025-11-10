---
title: "Vulnerability Response Process"
description: "I2P's security vulnerability reporting and response process"
layout: "security-response"
aliases:
  - /en/research/vrp
---

<div id="contact"></div>

## Report a Vulnerability

Discovered a security issue? Report it to **security@i2p.net** (PGP encouraged)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Download PGP Key</a> | GPG Key fingerprint: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Research Guidelines

**Please DO NOT:**
- Exploit the live I2P network
- Conduct social engineering or attack I2P infrastructure
- Disrupt services for other users

**Please DO:**
- Use isolated test networks when possible
- Follow coordinated disclosure practices
- Contact us before live network testing

<div id="process"></div>

## Response Process

### 1. Report Received
- Response within **3 working days**
- Response Manager assigned
- Severity classification (HIGH/MEDIUM/LOW)

### 2. Investigation & Development
- Private patch development via encrypted channels
- Testing on isolated network
- **HIGH severity:** Public notification within 3 days (no exploit details)

### 3. Release & Disclosure
- Security update deployed
- **90-day maximum** timeline to full disclosure
- Optional researcher credit in announcements

### Severity Levels

**HIGH** - Network-wide impact, immediate attention required
**MEDIUM** - Individual routers, targeted exploitation
**LOW** - Limited impact, theoretical scenarios

<div id="communication"></div>

## Secure Communication

Use PGP/GPG encryption for all security reports:

```
Fingerprint: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Include in your report:
- Detailed technical description
- Steps to reproduce
- Proof-of-concept code (if applicable)

<div id="timeline"></div>

## Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial Response | 0-3 days |
| Investigation | 1-2 weeks |
| Development & Testing | 2-6 weeks |
| Release | 6-12 weeks |
| Full Disclosure | 90 days max |

<div id="faq"></div>

## FAQ

**Will I get in trouble for reporting?**
No. Responsible disclosure is appreciated and protected.

**Can I test on the live network?**
No. Use isolated test networks only.

**Can I remain anonymous?**
Yes, though it may complicate communication.

**Do you have a bug bounty?**
Not currently. I2P is volunteer-driven with limited resources.

<div id="examples"></div>

## What to Report

**In Scope:**
- I2P router vulnerabilities
- Protocol or cryptography flaws
- Network-level attacks
- De-anonymization techniques
- Denial of service issues

**Out of Scope:**
- Third-party applications (contact developers)
- Social engineering or physical attacks
- Known/disclosed vulnerabilities
- Purely theoretical issues

---

**Thank you for helping keep I2P secure!**
