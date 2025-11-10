---
title: "Introduction to I2P"
description: "A less-technical introduction to the I2P anonymous network"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
aliases:
  - /en/docs/how/intro/
  - /docs/how/intro/
---

## What is I2P?

The Invisible Internet Project (I2P) is an anonymous network layer that allows for censorship-resistant, peer-to-peer communication. Anonymous connections are achieved by encrypting the user's traffic and sending it through a distributed network run by volunteers around the world.

## Key Features

### Anonymity

I2P hides both the sender and receiver of messages. Unlike traditional internet connections where your IP address is visible to websites and services, I2P uses multiple layers of encryption and routing to keep your identity private.

### Decentralization

There is no central authority in I2P. The network is maintained by volunteers who donate bandwidth and computing resources. This makes it resistant to censorship and single points of failure.

### End-to-End Encryption

All traffic within I2P is encrypted end-to-end. Messages are encrypted multiple times as they pass through the network, similar to how Tor works but with important differences in implementation.

## How It Works

### Tunnels

I2P uses "tunnels" to route traffic. When you send or receive data:

1. Your router creates an outbound tunnel (for sending)
2. Your router creates an inbound tunnel (for receiving)
3. Messages are encrypted and sent through multiple routers
4. Each router only knows the previous and next hop, not the full path

### Garlic Routing

I2P improves on traditional onion routing with "garlic routing":

- Multiple messages can be bundled together (like cloves in a bulb of garlic)
- This provides better performance and additional anonymity
- Makes traffic analysis more difficult

### Network Database

I2P maintains a distributed network database containing:

- Router information
- Destination addresses (similar to .i2p websites)
- Encrypted routing data

## Common Use Cases

### Anonymous Websites (Eepsites)

Host or visit websites that end in `.i2p` - these are only accessible within the I2P network and provide strong anonymity guarantees for both hosts and visitors.

### File Sharing

Share files anonymously using BitTorrent over I2P. Many torrent applications have I2P support built-in.

### Email

Send and receive anonymous email using I2P-Bote or other email applications designed for I2P.

### Messaging

Use IRC, instant messaging, or other communication tools privately over the I2P network.

## Getting Started

Ready to try I2P? Check out our [downloads page](/downloads) to install I2P on your system.

For more technical details, see the [Technical Introduction](/docs/overview/tech-intro) or explore the full [documentation](/docs).

## Learn More

- [Technical Introduction](/docs/overview/tech-intro) - Deeper technical concepts
- [Threat Model](/docs/overview/threat-model) - Understanding I2P's security model
- [Comparison to Tor](/docs/overview/comparison) - How I2P differs from Tor
- [Cryptography](/docs/specs/cryptography) - Details on I2P's cryptographic algorithms
