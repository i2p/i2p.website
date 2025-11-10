---
title: "I2P Status Notes for 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Weekly I2P status update covering development progress, TCP transport improvements, and new userhosts.txt feature"
categories: ["status"]
---

Hi gang, quick update this week

## Index
1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Dev status

The network has been fairly stable over the last week, so I've been able to focus my time on the 0.4.1 release - revamping the TCP transport and adding support for detecting IP addresses and removing that old "target changed identities" thing. This should also get rid of the need for dyndns entries as well.

It won't be the ideal 0-click setup for people behind NATs or firewalls - they'll still need to do the port forwarding so they can receive inbound TCP connections. It should however be less error prone. I'm doing my best to keep it backwards compatible, but I'm not making any promises on that front. More news when its ready.

## 2) New userhosts.txt vs. hosts.txt

In the next release we'll have the oft-requested support for a pair of hosts.txt files - one that is overwritten during upgrades (or from `http://dev.i2p.net/i2p/hosts.txt`) and one that the user can maintain locally. In the next release (or CVS HEAD) you can edit the file "userhosts.txt" which is checked before hosts.txt for any entries - please make your local changes there, since the update process will overwrite hosts.txt (but not userhosts.txt).

## 3) ???

As I mentioned, only a brief set of notes this week. Anyone have anything else they want to bring up? Swing on by the meeting in a few minutes.

=jr