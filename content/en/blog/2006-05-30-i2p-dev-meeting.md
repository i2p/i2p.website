---
title: "I2P Dev Meeting - May 30, 2006"
date: 2006-05-30
author: "jrandom"
description: "I2P development meeting log for May 30, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, cervantes, frosk, green, jrandom, tethrar</p>

## Meeting Log

<div class="irc-log">
16:00 &lt;jrandom&gt; 0) hi
16:00 &lt;jrandom&gt; 1) Net status
16:00 &lt;jrandom&gt; 2) Peer filtering
16:00 &lt;jrandom&gt; 3) Syndie status
16:00 &lt;jrandom&gt; 4) ???
16:00 &lt;jrandom&gt; 0) hi
16:00  * jrandom waves
16:01 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2006-May/001291.html
16:01 &lt;jrandom&gt; (up an hour early, even [or a few weeks late, if you want to pick on me ;])
16:02 &lt;jrandom&gt; ok, lets jump on in to 1) Net status
16:02 &lt;jrandom&gt; things arent in the shape they should be in.  they're better than they were during the congestion collapse, but it should be better than it is now
16:03 &lt;jrandom&gt; i don't have much more to add on that though, unless anyone has any questions/concerns on 1)?
16:03 &lt;@frosk&gt; i get days of irc connection with .19, so no complaints here
16:04 &lt;jrandom&gt; nice
16:04 &lt;jrandom&gt; yeah, its good for some, just not good enough or consistent enough.  stats in the db aren't looking that great either
16:06 &lt;jrandom&gt; ok, anyone have anything else on 1) Net status, or shall we move on over to 2)Peer filtering?
16:07 &lt;jrandom&gt; [insert moving sounds here]
16:09 &lt;jrandom&gt; as mentioned in the mail, the gist of things is to give our peer selection a bit of a boost.  at first, it'll be a bit dangerous, allowing some active partitioning attacks, but if it works as I hope, we can avoid those
16:10 &lt;jrandom&gt; (but avoiding it requires essentially killing all router identities, which would essentially serve as a network reset, so i'd like to avoid that unless its worthwhile)
16:11 &lt;bar&gt; reset them once or repeatedly?
16:11 &lt;bar&gt; s/reset/killing
16:11 &lt;jrandom&gt; at least once, but also on all subsequent drastic config changes
16:12 &lt;jrandom&gt; (aka putting some criteria into the router identity's certificate, which in turn means changing the ident hash, so they can't pretend to push one setting to some people and others to others)
16:13 &lt;bar&gt; gotcha
16:14 &lt;jrandom&gt; ok, i dont think i have anything else on that topic atm, unless anyone has any questions/comments/concerns?
16:15 &lt;jrandom&gt; (hopefully there'll be a build out in the next day or two, release after it stabilizes)
16:17 &lt;jrandom&gt; ok, hitting 3) briefly..
16:18 &lt;jrandom&gt; syndie is coming along, and although the amd64/amd32/x86/swt/gcj battle hasn't always been pretty, we'll have a build ready in june
16:19 &lt;jrandom&gt; (but still don't talk to me about mingw/gcj ;)
16:19 &lt;jrandom&gt; i don't have much more to add on there at the moment though, unless anyone has any questions/concerns re: the syndie revamp?
16:21 &lt;@cervantes&gt; how's mingw/gcj support coming along?
16:21 &lt;@cervantes&gt; *duck*
16:22 &lt;@cervantes&gt; do we get some screenies before the june release? :)
16:23 &lt;jrandom&gt; i'm sure i'll try to rope some eager volunteers into pre-release testing ;)
16:23 &lt;tethrar&gt; count me in ;)
16:23 &lt;jrandom&gt; w3wt
16:24 &lt;jrandom&gt; ok, lets swing over to the bullet point i know y'all have been waiting for: 4) ???
16:24 &lt;jrandom&gt; wazaaaap?
16:24 &lt;green&gt; Is there any plan to have to have a "real" working I2P router with Via C7 ? jbigi give only 30% better than full java
16:25 &lt;jrandom&gt; is 30% still too cpu intensive?  what makes it not "real"?
16:25 &lt;jrandom&gt; but no, i do not have the math or c7 asm skill to make a better libGMP for C7.
16:25 &lt;green&gt; sure too cpu intensive with 100% cpu load :P
16:26 &lt;jrandom&gt; 100% cpu load suggests that the problem isn't jbigi, but the fact that jbigi needs to be used too much
16:26 &lt;jrandom&gt; and for that, yes, there is lots we've got on the way.
16:26 &lt;jrandom&gt; (e.g. reducing the connection reestablishments, improving tunnel build success rates, etc)
16:27 &lt;jrandom&gt; ((and not getting as many tunnel requests if the router is not capable of handling them))
16:29 &lt;green&gt; humm, this is with a dedicated box with 100Mb/s so It should be capable
16:30 &lt;jrandom&gt; no, bandwidth is not the only resource constrained here, cpu obviously is ;)
16:33 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:36 &lt;jrandom&gt; *cough*
16:37  * jrandom winds up
16:37  * jrandom *baf*s the meeting closed
</div>
