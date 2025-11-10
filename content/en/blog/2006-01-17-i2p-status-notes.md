---
title: "I2P Status Notes for 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Network status with 0.6.1.9, tunnel creation crypto improvements, and Syndie blog interface updates"
categories: ["status"]
---

Hi y'all, 'tis tuesday again

* Index
1) Net status and 0.6.1.9
2) Tunnel creation crypto
3) Syndie blogs
4) ???

* 1) Net status and 0.6.1.9

With 0.6.1.9 out and 70% of the network upgraded, most of the
bugfixes included seem to be working as expected, with reports are
that the new speed profiling has been picking out some good peers.
I've heard of sustained throughput on fast peers exceeding 300KBps
with 50-70% cpu usage, with other routers in the 100-150KBps range,
tapering down to those pushing 1-5KBps.  There still is substantial
router identity churn though, so it seems the bugfix I thought would
reduce that hasn't (or the churn is legitimate).

* 2) Tunnel creation crypto

In the fall, there was a lot of discussion regarding how we build
our tunnels, along side the tradeoffs between Tor-style telescopic
tunnel creation and I2P-style exploratory tunnel creation [1].
Along the way, we came up with a combination [2] that removes the
problems of Tor-style telescopic creation [3], keeps I2P's
unidirectional benefits, and cuts down on unnecessary failures.  As
there were lots of other things going on at the time, implementing
the new combination was put off, but as we are now approaching the
0.6.2 release, during which we need to revamp the tunnel creation
code anyway, its time to get this hammered out.

I sketched up a draft spec for the new tunnel crypto and posted it
to my syndie blog the other day, and after some minor changes that
came out when actually implementing it, we've got a spec together
in CVS [4].  There is basic code implementing it in CVS too [5],
though it isn't hooked in for actual tunnel building yet.  If anyone
is bored, I'd love some feedback on the spec.  In the meantime, I'll
continue working on the new tunnel building code.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html and
    see the threads relating to the bootstrap attacks
[2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html
[3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html
[4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/
                               tunnel-alt-creation.html?rev=HEAD
[5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/
                       i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

As mentioned before, this new 0.6.1.9 release has some substantial
revamps to the Syndie blog interface, including cervantes' new
styling and each user's selection of blog links and logo (e.g. [6]).
You can control those links on the left by hitting the "configure
your blog" link on your profile page, bringing you to
http://localhost:7657/syndie/configblog.jsp.  Once you make your
changes there, the next time you push a post up to an archive, that
information will be made available to others.

[6] http://syndiemedia.i2p.net/
    blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Seeing as I'm already 20 minutes late for the meeting, I should
probably keep this short.  I know there are a few other things going
on, but rather than out them here, developers who want to discuss
them should swing by the meeting and bring 'em up.  Anyway, thats it
for now, see y'all on #i2p!

=jr