---
title: "I2P Status Notes for 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Weekly I2P development status notes covering network status, 0.5 tunnel routing design, i2pmail.v2, and azneti2p_0.2 security fix"
categories: ["status"]
---

Hi y'all, weekly update time

* Index
1) Net status
2) 0.5
3) i2pmail.v2
4) azneti2p_0.2
5) ???

* 1) Net status

Hmm, not much to report here - things still work as they did last
week, size of the net is still pretty similar, perhaps a little
larger.  Some neat new sites are popping up - see the forum [1]
and orion [2] for details.

[1] http://forum.i2p.net/viewforum.php?f=16
[2] http://orion.i2p/

* 2) 0.5

Thanks to the help of postman, dox, frosk, and cervantes (and
everyone who tunneled data through their routers ;), we've
collected a full day's worth of message size stats [3].  There are
two sets of stats there - height and width of the zoom.  This was
driven by the desire to explore the impact of different message
padding strategies on the network load, as explained [4] in one of
the drafts for the 0.5 tunnel routing.  (ooOOoo pretty pictures).

The scary part about what I found digging through those was that by
using some pretty simple hand-tuned padding breakpoints, padding to
those fixed sizes would still ended up with over 25% of the
bandwidth wasted.  Yeah, I know, we're not going to do that.
Perhaps y'all can come up with something better by digging through
that raw data.

[3] http://dev.i2p.net/~jrandom/messageSizes/
[4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/
                                 tunnel.html?rev=HEAD#tunnel.padding

Actually, that [4] link leads us into the state of the 0.5 plans for
the tunnel routing.  As Connelly posted [5], there has been a lot of
discussion lately on IRC about some of the drafts, with polecat,
bla, duck, nickster, detonate and others contributing suggestions
and probing questions (ok, and snarks ;).  After a little more than
a week, we came across a potential vulnerability with [4] dealing
with an adversary who was somehow able to take over the inbound
tunnel gateway who also controlled one of the other peers later in
that tunnel.  While in most cases this by itself wouldn't expose the
endpoint, and would be probabalistically hard to do as the network
grows, it still Sucks (tm).

So in comes [6].  This gets rid of that issue, allows us to have
tunnels of any length, and solves world hunger [7].  It does open
another issue where an attacker could build loops in the tunnel, but
based on a suggestion [8] Taral made last year regarding the session
tags used on ElGamal/AES, we can minimize the damage done by using
a series of synchronized pseudorandom number generators [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html
[6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/
                                            tunnel-alt.html?rev=HEAD
[7] guess which statement is false?
[8] http://www.i2p.net/todo#sessionTag
[9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/
                                tunnel-alt.html?rev=HEAD#tunnel.prng

Don't worry if the above sounds confusing - you're seeing the
innards of some gnarly design issues being wrung out in the open.
If the above *doesnt* sound confusing, please get in touch, as we're
always looking for more heads to hash through this stuff :)

Anyway, as I mentioned on the list [10], next up I'd like to get the
second strategy [6] implemented to hash through the remaining
details.  The plan for 0.5 is currently to get all of the backwards
incompatible changes together - the new tunnel crypto, etc - and
push that as 0.5.0, then as that settles on the net, move on to the
other parts of 0.5 [11], such as adjusting the pooling strategy as
described in the proposals, pushing that as 0.5.1.  I'm hoping we
can still hit 0.5.0 by the end of the month, but we'll see.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html
[11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

The other day postman put out a draft plan of action for the next
generation mail infrastructure [12], and it looks bloody cool.  Of
course, there are always yet more bells and whistles we can dream
up, but its got a pretty nice architecture in many ways.  Check out
what's been doc'ed up so far [13], and get in touch with the postman
with your thoughts!

[12] http://forum.i2p.net/viewtopic.php?t=259
[13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

As I posted to the list [14], the original azneti2p plugin for
azureus had a serious anonymity bug.  The problem was that mixed
torrents where some users are anonymous and others are not, the
anonymous users would contact the non-anonymous users /directly/
rather than through I2P.  Paul Gardner and the rest of the azureus
devs were quite responsive and put out a patch right away.  The
issue I saw is no longer present in azureus v. 2203-b12 +
azneti2p_0.2.

We haven't gone through and audited the code to review any potential
anonymity issues though, so "use at your own risk" (OTOH, we say the
same about I2P, prior to the 1.0 release).  If you're up for it, I
know the azureus devs would appreciate more feedback and bug reports
with the plugin.  We'll of course keep people informed if we find
out about any other issues.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Lots going on, as you can see.  I think thats about all I've got to
bring up, but please swing by the meeting in 40 minutes if there's
something else you'd like to discuss (or if you just want to rant
about the stuff above)

=jr