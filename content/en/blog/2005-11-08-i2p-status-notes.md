---
title: "I2P Status Notes for 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Weekly update covering 0.6.1.4 stability, performance optimization roadmap, I2Phex 0.1.1.35 release, I2P-Rufus BT client development, I2PSnarkGUI progress, and Syndie UI revamps"
categories: ["status"]
---

Hi gang, tuesday again

* Index
1) Net status / short term roadmap
2) I2Phex
3) I2P-Rufus
4) I2PSnarkGUI
5) Syndie
6) ???

* 1) Net status / short term roadmap

0.6.1.4 still seems pretty solid, though there have been some bugfixes in CVS since then. I've also added some optimizations for SSU to transfer data more efficiently, which I hope will have a noticeable impact on the network once its rolled out widely. I'm holding off on 0.6.1.5 for the moment though, as there are a few other things I want to get into the next release. The current plan is to push it out this weekend, so keep an ear out for the latest news.

The 0.6.2 release will include lots of great stuff to face even stronger adversaries, but one thing it won't affect is performance. While anonymity is certainly the entire point of I2P, if the throughput and latency is poor, we won't have any users. As such, my plan is to get performance where it needs to be before proceeding on to implementing the 0.6.2 peer ordering strategies and the new tunnel creation techniques.

* 2) I2Phex

There's been lots of activity on the I2Phex front as of late too, with a new 0.1.1.35 release [1]. There have also been further changes in CVS as well (thanks Legion!), so I wouldn't be suprised to see a 0.1.1.36 later this week.

There has been some good progress on the gwebcache front too (see http://awup.i2p/), though no one to my knowledge has started working on modifying I2Phex to use an I2P-enabled gwebcache (interested? lemmie know!)

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Word on the street is defnax and Rawn have been doing some hacking on the Rufus BT client, merging in some I2P related code from I2P-BT. I don't know the current status of the port, but it sounds like it'll have some nice features. I'm sure we'll hear more when there's more to be heard.

* 4) I2PSnarkGUI

Another rumor going around is Markus has been doing some hacking on a new C# GUI... screenshots on PlanetPeer look pretty cool [2]. There are still plans for a platform independent web interface, but this looks pretty nice. I'm sure we'll hear more from Markus as the GUI progresses.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

There has also been some discussion going on regarding Syndie UI revamps [3], and I expect we'll see some progress on that front fairly soon. dust is also crunching away on Sucker, adding better support for pulling more RSS/Atom feeds into Syndie, as well as some enhancements to SML itself.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Lots and lots going on, as always. Swing on by #i2p in a few minutes for our weekly dev meeting.

=jr