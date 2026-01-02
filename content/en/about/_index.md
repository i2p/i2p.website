---
title: "About I2P"
description: "Learn about The Invisible Internet Project - a fully encrypted, peer-to-peer overlay network designed for anonymous communication."
tagline: "The Invisible Internet Project"
type: "about"
layout: "about"
established: "2002"
---

The Invisible Internet Project began in 2002. The vision for the project was for the I2P Network "to deliver full anonymity, privacy, and security at the highest level possible. Decentralized and peer to peer Internet means no more worrying about your ISP controlling your traffic. This will allow people to do seamless activities and change the way we look at security and even the Internet, utilizing public key cryptography, IP steganography, and message authentication. The Internet that should have been, will be soon."

Since then I2P has evolved to specify and implement a complete suite of network protocols capable of delivering a high level of privacy, security, and authentication to a variety of applications.

## The I2P Network

The I2P network is a fully encrypted peer-to-peer overlay network. An observer cannot see a message's contents, source, or destination. No one can see where traffic is coming from, where it is going, or what the contents are. Additionally I2P transports offer resistance to recognition and blocking by censors. Because the network relies on peers to route traffic, location-based blocking is a challenge that grows with the network. Every router in the network participates in making the network anonymous. Except in cases where it would be unsafe, everyone participates in sending and receiving network traffic.

## How to Connect to the I2P Network

The core software (Java) includes a router that introduces and maintains a connection with the network. It also provides applications and configuration options to personalize your experience and workflow. Learn more in our [documentation](/docs/).

## What Can I Do On The I2P Network?

The network provides an application layer for services, applications, and network management. The network also has its own unique DNS that allows self hosting and mirroring of content from the Internet (Clearnet). The I2P network functions the same way the Internet does. The Java software includes a BitTorrent client, and email as well as a static website template. Other applications can easily be added to your router console.

## An Overview of the Network

I2P uses cryptography to achieve a variety of properties for the tunnels it builds and the communications it transports. I2P tunnels use transports, [NTCP2](/docs/specs/ntcp2/) and [SSU2](/docs/specs/ssu2/), to conceal the traffic being transported over it. Connections are encrypted from router-to-router, and from client-to-client (end-to-end). Forward-secrecy is provided for all connections. Because I2P is cryptographically addressed, I2P network addresses are self-authenticating and only belong to the user who generated them.

The network is made up of peers ("routers") and unidirectional inbound and outbound virtual tunnels. Routers communicate with each other using protocols built on existing transport mechanisms (TCP, UDP), passing messages. Client applications have their own cryptographic identifier ("Destination") which enables it to send and receive messages. These clients can connect to any router and authorize the temporary allocation ("lease") of some tunnels that will be used for sending and receiving messages through the network. I2P has its own internal network database (using a modification of the Kademlia DHT) for distributing routing and contact information securely.

## About Decentralization and the I2P Network

The I2P network is almost completely decentralized, with exception to what are called Reseed Servers. This is to deal with the DHT (Distributed Hash Table) bootstrap problem. Basically, there is not a good and reliable way to get out of running at least one permanent bootstrap node that non-network participants can find to get started. Once connected to the network, a router only discovers peers by building "exploratory" tunnels, but to make the initial connection, a reseed host is required to create connections and onboard a new router to the network. Reseed servers can observe when a new router has downloaded a reseed from them, but nothing else about traffic on the I2P network.

## Comparisons

There are a great many other applications and projects working on anonymous communication and I2P has been inspired by much of their efforts. This is not a comprehensive list of anonymity resources - both [freehaven's Anonymity Bibliography](http://freehaven.net/anonbib/topic.html) and [GNUnet's related projects](https://www.gnunet.org/links/) serve that purpose well. That said, a few systems stand out for further comparison. Learn more about how I2P compares to other anonymity networks in our [detailed comparison documentation](/docs/overview/comparison/). 