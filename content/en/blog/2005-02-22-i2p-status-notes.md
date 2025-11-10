---
title: "I2P Status Notes for 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Weekly I2P development status notes covering 0.5 release success, upcoming 0.5.0.1 bugfix, tunnel peer ordering strategies, and azneti2p updates"
categories: ["status"]
---

Hi y'all, weekly update time

* Index
1) 0.5
2) Next steps
3) azneti2p
4) ???

* 1) 0.5

As y'all have heard, we finally got 0.5 out the door, and for the
most part, its been doing pretty well.  I really appreciate how
quickly people have updated - within the first day, 50-75% of the
net was up to 0.5!  Because of the fast adoption, we've been able
to see the impact of the various changes more quickly, and in turn
have found a bunch of bugs.  While there are still some outstanding
issues, we will be putting out a new 0.5.0.1 release later this
evening to address the most important ones.

As a side benefit of the bugs, its been neat to see that routers can
handle thousands of tunnels ;)

* 2) Next steps

After the 0.5.0.1 release, there may be another build to experiment
with some changes in the exploratory tunnel building (such as using
only one or two not-failing peers, the rest being high capacity,
instead of all of the peers being not-failing).  After that, we'll
be jumping towards 0.5.1, which will improve the tunnel throughput
(by batching multiple small messages into a single tunnel message)
and allow the user more control over their suceptability to the
predecessor attack.

Those controls will take the form of per-client peer ordering and
selection strategies, one for the inbound gateway and outbound
endpoint, and one for the rest of the tunnel.  Current thumbnail
sketch of strategies I forsee:
 = random (what we have now)
 = balanced (explicitly try to reduce how often we use each peer)
 = strict (if we ever use A-->B-->C, they stay in that order
           during subsequent tunnels [bounded by time])
 = loose (generate a random key for the client, calculate the XOR
          from that key and each peer, and always order the peers
          selected by the distance from that key [bounded by time])
 = fixed (always use the same peers per MBTF)

Anyway, thats the plan, though I'm not sure which strategies will be
rolled out first.  Suggestions more than welcome :)

* 3) azneti2p

The folks over at azureus have been working hard with a slew of
updates, and their latest b34 snapshot [1] seems to have some I2P
related bugfixes.  While I havent had time to audit the source since
that last anonymity issue I raised, they have fixed that particular
bug, so if you're feeling adventurous, go snag their update and give
'er a try!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Lots and lots of stuff going on, and I'm sure I haven't come close
to covering things.  Swing on by the meeting in a few minutes and
see whats up!

=jr