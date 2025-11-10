---
title: "I2P Summer Dev 2017: MOAR Speed!"
date: 2017-06-01
author: "str4d"
description: "This year's Summer Dev will be focused on metrics collection and performance improvements for the network."
categories: ["summer-dev"]
---

It's that time of year again! We're embarking on our summer development programme, where we focus on a particular aspect of I2P to push it forward. For the next three months, we'll be encouraging both new contributors and existing community members to pick a task and have fun with it!

Last year, we focused on helping users and developers leverage I2P, by improving API tooling and giving some love to applications that run over I2P. This year, we want to improve the user experience by working on an aspect that affects everyone: performance.

Despite onion-routing networks often being called "low-latency" networks, there is significant overhead created by routing traffic through additional computers. I2P's unidirectional tunnel design means that by default, a round trip between two Destinations will involve twelve participants! Improving the performance of these participants will help to both reduce the latency of end-to-end connections and increase the quality of tunnels network-wide.

## MOAR speed!

Our development programme this year will have four components:

### Measure

We can't tell if we improve performance without a baseline! We'll be creating a metrics system for collecting usage and performance data about I2P in a privacy-preserving way, as well as porting various benchmarking tools to run over I2P (e.g. iperf3).

### Optimise

There's a lot of scope for improving the performance of our existing code, to e.g. reduce the overhead of participating in tunnels. We will be looking at potential improvements to cryptographic primitives, network transports (both at the link-layer and end-to-end), peer profiling, and tunnel path selection.

### Advance

We have several open proposals for improving the scalability of the I2P network (e.g. Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). We will be working on these proposals, and begin implementing the finalised ones in the various network routers.

### Research

I2P is a packet-switched network, like the internet it runs on top of. This gives us significant flexibility in how we route packets, both for performance and privacy. The majority of this flexibility is unexplored! We want to encourage research into how various clearnet techniques for improving bandwidth can be applied to I2P, and how they might affect the privacy of network participants.

## Take part in Summer Dev!

We have many more ideas for things we'd like to get done in these areas. If you're interested in hacking on privacy and anonymity software, designing protocols (cryptographic or otherwise), or researching future ideas - come and chat with us on IRC or Twitter! We are always happy to welcome newcomers into our community. We'll also be sending I2P stickers out to all new contributors taking part!

We'll be posting here as we go, but you can also follow our progress, and share your own ideas and work, with the hashtag #I2PSummer on Twitter. Bring on the summer!
