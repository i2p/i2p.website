---
title: "Academic Research"
description: "Information and guidelines for academic research on the I2P network"
layout: "research"
---

<div id="intro"></div>

## I2P Academic Research

There is a large research community investigating a wide range of aspects of anonymity. For anonymity networks to continue to improve, we believe it is essential to understand the problems that are being faced. Research into the I2P network is still in its infancy, with much of the research work so far focused on other anonymity networks. This presents a unique opportunity for original research contributions.

<div id="notes"></div>

## Notes to Researchers

### Defensive Research Priorities

We welcome research that helps us fortify the network and improve its security. Testing that strengthens I2P infrastructure is encouraged and appreciated.

### Research Communication Guidelines

We strongly encourage researchers to communicate their research ideas early to the development team. This helps:

- Avoid potential overlap with existing projects
- Minimize potential harm to the network
- Coordinate testing and data collection efforts
- Ensure research aligns with network goals

<div id="ethics"></div>

## Research Ethics & Testing Guidelines

### General Principles

When conducting research on I2P, please consider the following:

1. **Assess research benefits vs. risks** - Consider whether the potential benefits of your research outweigh any risks to the network or its users
2. **Prefer test network over live network** - Use I2P's test network configuration whenever possible
3. **Collect minimal necessary data** - Only collect the minimum amount of data required for your research
4. **Ensure published data respects user privacy** - Any published data should be anonymized and respect user privacy

### Network Testing Methods

For researchers who need to test on I2P:

- **Use test network configuration** - I2P can be configured to run on an isolated test network
- **Utilize MultiRouter mode** - Run multiple router instances on a single machine for testing
- **Configure router family** - Make your research routers identifiable by configuring them as a router family

### Recommended Practices

- **Contact I2P team before live network testing** - Reach out to us at research@i2p.net before conducting any tests on the live network
- **Use router family configuration** - This makes your research routers transparent to the network
- **Prevent potential network interference** - Design your tests to minimize any negative impact on regular users

<div id="questions"></div>

## Open Research Questions

The I2P community has identified several areas where research would be particularly valuable:

### Network Database

**Floodfills:**
- Are there any other ways to mitigate network brute-forcing via significant floodfill control?
- Is there any way to detect, flag and potentially remove 'bad floodfills' without actually needing to rely on a form of central authority?

### Transports

- How could packet retransmission strategies and timeouts be improved?
- Is there a way for I2P to obfuscate packets and reduce traffic analysis more efficiently?

### Tunnels and Destinations

**Peer Selection:**
- Is there a way that I2P could perform peer selection more efficiently or securely?
- Would using geoip to prioritize nearby peers negatively impact anonymity?

**Unidirectional Tunnels:**
- What are the benefits of unidirectional tunnels over bidirectional tunnels?
- What are the tradeoffs between unidirectional and bidirectional tunnels?

**Multihoming:**
- How effective is multihoming at load-balancing?
- How does it scale?
- What happens as more routers host the same Destination?
- What are the anonymity tradeoffs?

### Message Routing

- How much is the effectiveness of timing attacks reduced by fragmentation and mixing of messages?
- What mixing strategies could I2P benefit from?
- How can high-latency techniques be effectively employed within or alongside our low-latency network?

### Anonymity

- How significantly does browser fingerprinting impact the anonymity of I2P users?
- Would developing a browser package benefit average users?

### Network Related

- What is the overall impact on the network created by 'greedy users'?
- Would additional steps for encouraging bandwidth participation be valuable?

<div id="contact"></div>

## Contact

For research inquiries, collaboration opportunities, or to discuss your research plans, please contact us at:

**Email:** research@i2p.net

We look forward to working with the research community to improve the I2P network!
