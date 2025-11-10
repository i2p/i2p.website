---
title: "I2P Status Notes for 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Weekly I2P development status notes covering 0.5.0.5 release with batching, UDP (SSU) transport protocol, and Q distributed store"
categories: ["status"]
---

Hi y'all, time for the weekly status notes

* Index
1) 0.5.0.5
2) UDP (SSU)
3) Q
4) ???

* 1) 0.5.0.5

Since y'all did such a great job at upgrading to 0.5.0.4 so quickly,
we're going to have the new 0.5.0.5 release come out after the
meeting.  As discussed last week, the big change is the inclusion of
the batching code, bundling multiple small messages together, rather
than giving them each their own full 1KB tunnel message.  While this
alone won't be revolutionary, it should substantially reduce the
number of messages passed, as well as the bandwidth used, especially
for services like IRC.

There will be more info in the release announcement, but two other
important things come up with the 0.5.0.5 rev.  First, we're
dropping support for users before 0.5.0.4 - there are well over 100
users on 0.5.0.4, and there are substantial problems with earlier
releases.  Second, there's an important anonymity fix in the new
build, that while it'd require some development effort to mount, its
not implausible.  The bulk of the change is to how we manage the
netDb - rather than play it fast and loose and cache entries all
over the place, we will only respond to netDb requests for elements
that have been explicitly given to us, regardless of whether or not
we have the data in question.

As always, there are bugfixes and some new features, but more info
will be forthcoming in the release announcement.

* 2) UDP (SSU)

As discussed off and on for the last 6-12 months, we're going to be
moving over to UDP for our interrouter communication once the 0.6
release is out.  To get us further down that path, we've got a first
draft of the transport protocol up in CVS @
http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Its a fairly simple protocol with the goals outlined in the doc, and
exploits I2P's capabilities to both authenticate and secure data, as
well as expose as little external information as possible.  Not even
the first part of a connection handshake is identifiable to someone
that isn't running I2P.  The behavior of the protocol is not fully
defined in the spec yet, such as how the timers fire or how the three
different semireliable status indicators are used, but it does cover
the basics of the encryption, packetization, and NAT hole punching.
None of it has been implemented yet, but will be soon, so feedback
would be greatly appreciated!

* 3) Q

Aum has been churning away on Q(uartermaster), a distributed store,
and the first pass of the docs are up [1].  One of the interesting
ideas in there seems to be a move away from a straight DHT towards
a memcached [2] style system, with each user doing any searches
entirely *locally*, and requesting the actual data from the Q server
"directly" (well, through I2P).  Anyway, some neat stuff, perhaps
if Aum is awake [3] we can wressle an update out of him?

[1] http://aum.i2p/q/
[2] http://www.danga.com/memcached/
[3] damn those timezones!

* 4) ???

Lots more going on, and if there were more than just a few minutes
until the meeting I could go on, but c'est la vie.  Swing on by
#i2p in a few to chat.

=jr