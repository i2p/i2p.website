---
title: "I2P Status Notes for 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Weekly update covering 0.5.0.6 netDb fixes, SSU UDP transport progress, Bayesian peer profiling results, and Q development"
categories: ["status"]
---

Hi y'all, update time again

* Index
1) Net status
2) SSU status
3) Bayesian peer profiling
4) Q status
5) ???

* 1) Net status

Last week's 0.5.0.6 release seems to have fixed the netDb issues we were seeing (yay). Sites and services are much more reliable than they were on 0.5.0.5, though there have been some reports of trouble where a site or service would become unreachable after a few days uptime.

* 2) SSU status

There's been lots of progress on the 0.6 UDP code, with the first batch of commits already made to CVS. Its not anything you could actually use yet, but the fundamentals are in place. Session negotiation works well and the semireliable message delivery performs as expected. There's still a lot of work to do though, test cases to write, and oddball situations to debug, but its progress.

If things go well, we may have some alpha testing next week, just for people who can explicitly configure their firewalls/NATs. I'd like to get the general operation hammered out first before adding in the relay handler, tuning up the netDb for faster routerInfo expiration, and selecting relays to publish. I'm also going to take this opportunity to do a whole slew of testing, as there are several critical queueing factors being addressed.

* 3) Bayesian peer profiling

bla has been churning away at some revisions to how we decide what peers to tunnel through, and though bla couldn't make it to the meeting, there's some interesting data to report:

<+bla> I've performed direct node speed measurements: I've profiled
       some 150 nodes by using OB tunnels of length 0, IB tunnels of
       length 1, batching-interval = 0ms
<+bla> In addition, I've just done some _very_ basic and
       _preliminary_ speed estimation using naive Bayesian
       classification
<+bla> The latter was done using the default expl. tunnel lengths
<+bla> The intersection between the set of nodes on which I have
       "ground truth", and the set of nodes in the current
       measurements, is 117 nodes
<+bla> Results are not _that_ bad, but not too impressive either
<+bla> See http://theland.i2p/estspeed.png
<+bla> Basic very-slow/fast separation is ok-ish, but fine-grained
       separation among the faster peers could be much better
<+jrandom2p> hmm, how'd the actual values get calculated - is that
             full RTT or is it RTT/length ?
<+bla> Using the normal expl. tunnels, it's next to impossible to
       prevent batching delays.
<+bla> The actual values are the ground-truth values: those obtained
       using OB=0 and IB=1
<+bla> (and variance=0, and no batching delay)
<+jrandom2p> the results look pretty good from here though
<+bla> The estimated timings are those obtained using Bayesian
       inference from _actual_ expl. tunnels of length 2 +/- 1
<+bla> This is obtained from 3000 RTTs, recorded over a period of
       about 3 hours (that's long)
<+bla> It does assume (for the moment) that peer speed is static.
       I've yet to implement weighting
<+jrandom2p> sounds kickass.  nice work bla
<+jrandom2p> hmm, so the estimate should equal 1/4 actual
<+bla> jrandom: No: All measured RTTs (using the normal expl.
       tunnels), are corrected for the number of hops in the
       round-trip
<+jrandom2p> ah ok
<+bla> Only after that, the Bayesian classifier is trained
<+bla> For now, I bin the measured times-per-hop into 10 classes:
       50, 100, ..., 450 ms, and an additional class >500 ms
<+bla> E.g., small delays-per-hop could be weighted using a larger
       factor, as could complete failures (>60000 ms).
<+bla> Though.... 65% of the estimated timings, fall within 0.5
       standard deviations from the actual node time
<+bla> However, this has to be redone, since the standard deviation
       is influenced heavily by the >60000 ms failures

After further discussion, bla pulled up a comparison against the existing speed calculator, posted @ http://theland.i2p/oldspeed.png
Mirrors of those pngs are up at
http://dev.i2p.net/~jrandom/estspeed.png and
http://dev.i2p.net/~jrandom/oldspeed.png

(for terminology, IB=inbound tunnel hops, OB=outbound tunnel hops, and after some clarification, the "ground truth" measurements were obtained by 1 hop outbound and 0 hop inbound, not the other way around)

* 4) Q status

Aum has been making lots of headway on Q as well, most recently working on a web based client interface. The next Q build will not be backwards compatible, as it includes a whole slew of new features, but I'm sure we'll hear more info from Aum when there's more info to be heard :)

* 5) ???

Thats about it for the moment (gotta wrap this up before meeting time). Oh, as an aside, it looks like I'll be moving earlier than planned, so perhaps some of the dates in the roadmap might shift around while I'm in transit to wherever I end up. Anyway, swing on by the channel in a few minutes to harass us with new ideas!

=jr