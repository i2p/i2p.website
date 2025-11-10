---
title: "I2P Status Notes for 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Weekly update covering developer return from travel, SSU transport progress, unit test bounty completion, and service outage"
categories: ["status"]
---

Hi y'all, time to start back up our weekly status notes

* Index
1) Dev[eloper] status
2) Dev[elopment] status
3) Unit test bounty
4) Service outage
5) ???

* 1) Dev[eloper] status

After 4 cities in 4 countries, I'm finally getting settled and churning through code again. Last week I got the last of the pieces to a laptop together, I'm no longer couch hopping, and while I don't have net access at home, there are plenty of net cafes around, so access is reliable (just infrequent and expensive).

That last point means that I won't be hanging out on irc as much as before, at least until the fall (I've got a sublet through August or so and will be looking for a place where I can get 24/7 net access). That doesn't, however, mean that I won't be doing as much - I'll just be working largely on my own test network, pushing out builds for live net testing (and, er, oh yeah, releases). It does mean though that we may want to move some discussions that used to go on free form in #i2p onto the list [1] and/or the forum [2] (I do still read the #i2p backlog though). I haven't found a reasonable place where I can go to for our development meetings yet, so I won't be there this week, but perhaps by next week I'll have found one.

Anyway, enough about me.

[1] http://dev.i2p.net/pipermail/i2p/
[2] http://forum.i2p.net/

* 2) Dev[elopment] status

While I've been moving, there have been two main fronts that I've been working on - documentation and the SSU transport (the later only since I got the laptop). The docs are still in progress, with a big ol' scary overview one as well as a series of smaller implementation docs (covering things like source layout, component interaction, etc).

SSU progress is going well - the new ACK bitfields are in place, the communication is dealing with (simulated) loss effectively, rates are appropriate for the various conditions, and I've cleared some of the uglier bugs I had run into previously. I am continuing to test these changes though, and once its appropriate we'll plot out a series of live net tests for which we'll need some volunteers to help out with. More news on that front when its available.

* 3) Unit test bounty

I'm glad to announce that Comwiz has come forward with a series of patches to claim the first phase of the unit test bounty [3]! We are still working through some minor details of the patches, but I've received the updates and generated both the junit and clover reports as necessary. I expect we'll have the patches in CVS shortly, at which point we'll put out Comwiz's testing docs.

As clover is a commercial product (free for OSS developers [4]), only those who have installed clover and received their clover license will be able to generate the clover reports. In any case, we'll be publishing the clover reports on the web periodically, so those who don't have clover installed can still see how well our test suite is doing.

[3] http://www.i2p.net/bounties_unittest
[4] http://www.cenqua.com/clover/

* 4) Service outage

As many have probably noticed, (at least) one of the outproxies is offline (squid.i2p), as is www.i2p, dev.i2p, cvs.i2p, and my blog. These are not unrelated events - the machine hosting them is hosed.

=jr