---
title: "20 Years of Privacy: A Brief History of I2P"
date: 2021-08-28
author: "sadie"
description: "A history of I2P As We Know It"
categories: ["general"]
---

## Invisibility is the best defense: building an internet within an internet

> "I believe most people want this technology so they can express themselves freely. It's a comfortable feeling when you know you can do that. At the same time we can conquer some of the problems seen within the Internet by changing the way security and privacy is viewed, as well as the extent to what it is valued."

In October 2001, 0x90 (Lance James) had a dream. It started as a "desire for instant communication with other Freenet users to talk about Freenet issues, and exchange Freenet keys while still maintaining anonymity, privacy and security." It was called IIP — the Invisible IRC Project.

The Invisible IRC Project was based on an ideal and framework behind The InvisibleNet. In an interview from 2002, 0x90 described the project as focused on "the innovation of intelligent network technology" with the goal to "provide the highest standards in security and privacy on the widely used, yet notoriously insecure Internet."

By 2003, several other similar projects had started, the largest being Freenet, GNUNet, and Tor. All of these projects had broad goals to encrypt and anonymize a variety of traffic. For IIP, it became clear that IRC alone was not a big-enough target. What was needed was an anonymizing layer for all protocols.

In early 2003, a new anonymous developer, "jrandom" joined the project. His explicit goal was to broaden the charter of IIP. jrandom wished to rewrite the IIP code base in Java and redesign the protocols based on recent papers and the early design decisions that Tor and Freenet were making. Some concepts like "onion routing" were modified to become "garlic routing".

By late summer 2003, jrandom had taken control of the project and renamed it the Invisible Internet Project or "I2P". He published a document outlining the philosophy of the project, and placed its technical goals and design in the context of mixnets and anonymizing layers. He also published the specification of two protocols (I2CP and I2NP) that formed the basis of the network I2P uses today.

By fall 2003, I2P, Freenet, and Tor were rapidly developing. jrandom released I2P version 0.2 on November 1, 2003, and continued rapid releases for the next 3 years.

In February 2005, zzz installed I2P for the first time. By summer 2005, zzz had set up zzz.i2p and stats.i2p, which became central resources for I2P development. In July 2005, jrandom released version 0.6, including the innovative SSU (Secure Semi-reliable UDP) transport protocol for IP discovery and firewall traversal.

From late 2006 into 2007, core I2P development slowed dramatically as jrandom shifted focus to Syndie. In November 2007, disaster struck when jrandom sent a cryptic message that he would have to take time off for a year or more. Unfortunately, they never heard from jrandom again.

The second stage of the disaster happened on January 13, 2008 when the hosting company for almost all i2p.net servers suffered a power outage and did not fully return to service. Complication, welterde, and zzz quickly made decisions to get the project back up and running, moving to i2p2.de and switching from CVS to monotone for source control.

The project realized it had depended too heavily on centralized resources. Work throughout 2008 decentralized the project and distributed roles to multiple people. Starting with release 0.7.6 on July 31, 2009, zzz would sign the next 49 releases.

By mid-2009, zzz had come to understand the code base much better and identified many scalability issues. The network experienced growth due to both anonymizing and circumvention abilities. In-network auto updates became available.

In Fall 2010, zzz declared a moratorium on I2P development until the website documentation was complete and accurate. It took 3 months.

Beginning in 2010, zzz, ech, hottuna, and other contributors attended CCC (Chaos Communications Congress) annually until COVID restrictions. The project built community and celebrated releases together.

In 2013, Anoncoin was created as the first cryptocurrency with built-in I2P support, with developers like meeh providing infrastructure to the I2P network.

In 2014, str4d began contributing to I2PBote and at Real World Crypto, discussions began on updating I2P's cryptography. By late 2014, most new signing crypto was complete including ECDSA and EdDSA.

In 2015, I2PCon took place in Toronto with talks, community support, and attendees from America and Europe. In 2016 at Real World Crypto Stanford, str4d gave a talk on crypto migration progress.

NTCP2 was implemented in 2018 (release 0.9.36), providing resistance against DPI censorship and reducing CPU load through faster, modern cryptography.

In 2019, the team attended more conferences including DefCon and Monero Village, reaching out to developers and researchers. Hoàng Nguyên Phong's research into I2P censorship was accepted to FOCI at USENIX, leading to the creation of I2P Metrics.

At CCC 2019, the decision was made to migrate from Monotone to GitLab. On December 10, 2020, the project officially switched from Monotone to Git, joining the world of developers using Git.

0.9.49 (2021) started the migration to new, faster ECIES-X25519 encryption for routers, completing years of specification work. The migration would take several releases.

## 1.5.0 — The early anniversary release

After 9 years of 0.9.x releases, the project went straight from 0.9.50 to 1.5.0 as recognition of almost 20 years of work to provide anonymity and security. This release finished implementation of smaller tunnel build messages to reduce bandwidth and continued the transition to X25519 encryption.

**Congratulations team. Let's do another 20.**
