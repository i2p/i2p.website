---
title: "I2P Status Notes for 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Weekly I2P development status notes covering 0.5 tunnel routing progress, SAM .NET port, GCJ compilation, and UDP transport discussions"
categories: ["status"]
---

Hi y'all, quick weekly status update

* Index
1) 0.5 status
2) sam.net
3) gcj progress
4) udp
5) ???

* 1) 0.5 status

Over the past week, there's been a lot of progress on the 0.5 side.
The issues we were discussing before have been resolved, dramatically
simplifying the crypto and removing the tunnel looping issue.  The
new technique [1] has been implemented and the unit tests are in
place.  Next up I'm putting together more of the code to integrate
those tunnels into the main router, then build up the tunnel
management and pooling infrastructure.  After thats in place, we'll
run it through the sim and eventually onto a parallel net to burn it
in before wrapping a bow on it and calling it 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead has put together a new port of the SAM protocol to .net -
c#, mono/gnu.NET compatible (yay smeghead!).  This is in cvs under
i2p/apps/sam/csharp/ with nant and other helpers - now all y'all
.net devs can start hacking with i2p :)

* 3) gcj progress

smeghead is definitely on a tear - at last count, with some
modifications the router is compiling under the latest gcj [2] build
(w00t!).  It still doesn't work yet, but the modifications to work
around gcj's confusion with some inner class constructs is definitely
progress.    Perhaps smeghead can give us an update?

[2] http://gcc.gnu.org/java/

* 4) udp

Not much to say here, though Nightblade did bring up an interesting
set of concerns [3] on the forum asking why we're going with UDP.  If
you've got similar concerns or have other suggestions on how we can
address the issues I replied with, please, chime in!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Yeah, ok, I'm late with the notes again, dock my pay ;)  Anyway, lots
going on, so either swing by the channel for the meeting, check the
posted logs afterwards, or post up on the list if you've got
something to say.  Oh, as an aside, I've given in and started up a
blog within i2p [4].

=jr
[4] http://jrandom.dev.i2p/ (key in http://dev.i2p.net/i2p/hosts.txt)