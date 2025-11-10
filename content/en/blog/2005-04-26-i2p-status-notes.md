---
title: "I2P Status Notes for 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Brief weekly update covering 0.5.0.7 network stability, SSU UDP transport progress with multi-network support, and unit test bounty funding"
categories: ["status"]
---

Hi y'all, brief weekly status notes today

* Index
1) Net status
2) SSU status
3) Unit test bounty
4) ???

* 1) Net status

Most people have upgraded to last weeks 0.5.0.7 release fairly quickly (thanks!) and the overall result seems positive. The net seems fairly reliable and the previous tunnel throttling has been resolved. There are still some intermittent problems reported by some users though, and we're tracking those down.

* 2) SSU status

Most of my time is spent focused on the 0.6 UDP code, and no, its not ready for release, and yes, there is progress ;) Right now it can handle multiple networks, keeping some peers on UDP and others on TCP with fairly reasonable performance. The hard part is working through all the congestion/contention cases, since the live net will be under constant load, but there's been a lot of progress there in the last day or so. More news when there's more news.

* 3) Unit test bounty

As duck mentioned on the list [1], zab has seeded a bounty to help out I2P with a series of testing updates - some funds for anyone who can complete the tasks listed on the bounty page [2]. We've had some further donations to that bounty [3] - it currently stands at $1000USD. While the bounties certainly don't offer "market rate", they are a small token of encouragement for developers who want to help out.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html
[2] http://www.i2p.net/bounty_unittests
[3] http://www.i2p.net/halloffame

* 4) ???

Ok, I'm late for the meeting again... I should probably sign and send this out, 'eh? Swing on by the meeting and we can discuss other issues as well.

=jr