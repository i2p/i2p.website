---
title: "I2P Dev Meeting - April 26, 2005"
date: 2005-04-26
author: "@jrandom"
description: "I2P development meeting log for April 26, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bla, duck, jrandom, jrandom2p, laberhorst, Lorie, smeghead</p>

## Meeting Log

<div class="irc-log">
14:10 &lt;@jrandom&gt; 0) hi
14:10 &lt;@jrandom&gt; 1) Net status
14:10 &lt;@jrandom&gt; 2) SSU status
14:10 &lt;@jrandom&gt; 3) Unit test bounty
14:10 &lt;@jrandom&gt; 4) ???
14:10 &lt;@jrandom&gt; 0) hi
14:10  * jrandom waves
14:10 &lt;@jrandom&gt; (late) weekly status notes are up @ http://dev.i2p.net/pipermail/i2p/2005-April/000723.html
14:10 &lt;bla&gt; hi
14:11 &lt;@jrandom&gt; while y'all read that tome, lets jump on into 1) Net status
14:12 &lt;@jrandom&gt; the previous set of problems we saw with some eepsites going offline in 0.5.0.6 seems to be resolved, though there are a few people who have been running into other problems with their sites
14:13 &lt;@jrandom&gt; i've seen some increased torrent activity at some trackers as well, though it hasn't caused any problems on irc from what i can tell
14:13 &lt;laberhorst&gt; net status: fairly well beside the not reachable prob :-)
14:13 &lt;@jrandom&gt; heh
14:13 &lt;@jrandom&gt; yeah, i'm stil not sure whats going on with your site. we can debug further after the meeting
14:14 &lt;@jrandom&gt; other than that, anyone else have any questions/comments/concerns wrt the net status / 0.5.0.7?
14:16 &lt;@jrandom&gt; ok, if not, moving on to 2) SSU status
14:16 &lt;@jrandom&gt; [insert hand waving here]
14:17 &lt;Lorie&gt; Good morning.
14:17 &lt;@jrandom&gt; i know, i'm dragging my heels a bit by not pushing it out faster, and it does perform really well as is.  still, there are some issues i'm not comfortable with yet, so y'all will have to bear with me a bit during this testing
14:18 &lt;@smeghead&gt; i commend you for not foisting crapware on us :)
14:18 &lt;@jrandom&gt; i'm hoping this week we'll have some further live net tests though (fingers crossed)
14:19 &lt;@jrandom&gt; well, i've foisted enough bugs on y'all so far
14:19 &lt;Lorie&gt; you're dragging your heels, are you ?
14:19  * Lorie eyes smeghead
14:19 &lt;bla&gt; jrandom: Just to make things clear: We could even have an intermediate period in which clients can be both UDP and TCP?
14:20 &lt;@jrandom&gt; bla: yes.  i've got a test network now with some TCP-only and some both TCP and UDP.  its kind of neat running the tunnels through both :)
14:20 &lt;@jrandom&gt; the live net will actually handle that as well, ignoring any UDP addresses (for people who don't yet support it)
14:20 &lt;@smeghead&gt; and that's given us lots of protein, but we don't want to over-indulge
14:21 &lt;bla&gt; jrandom: Nice! That's good for the transition
14:23 &lt;@jrandom&gt; aye, thats the hope.  still, there's lots of work to do[/obligatory]
14:23 &lt;@jrandom&gt; while our transport is SSU - "SEMIreliable Secure UDP" - we still need to try to be kind of reliable
14:24 &lt;@jrandom&gt; i've followed a bunch of research out there on the net, watching whats worked best, and while we could just be lazy and fire & forget, there's a lot to be gained by doing some simple tcp-esque reliability, which is what i'm hacking on now
14:25 &lt;@jrandom&gt; otoh, since its just semireliable, if it doesn't get ACKed quickly we can just drop the message, rather than drop the connection
14:26 &lt;Lorie&gt; yes
14:26 &lt;Lorie&gt; do be reliable; time is a luxury one has
14:27 &lt;@jrandom&gt; thats about all i have to bring up for 2) SSU status.  anyone have any questions/comments/concerns, or shall we move on to 3) Unit test bounty?
14:28 &lt;jrandom2p&gt; consider us moved
14:29 &lt;jrandom2p&gt; ok, duck posted up a good summary about whats up and the importance of the unit test bounty the other day, and there's a lot of detail referenced from the site.
14:30 &lt;jrandom2p&gt; this is a good chance for someone to dig into i2p a bit and get a little cash back in the process ;)
14:30 &lt;jrandom2p&gt; but anyway, y'all can read all that stuff.  does anyone have any questions on it?
14:31 &lt;jrandom2p&gt; ok, if not, moving on to 4) ???
14:32 &lt;@smeghead&gt; anyone tried that emma code coverage suite?
14:32 &lt;jrandom2p&gt; there's been a lot of various things going on in the last week, though i'm not sure whats ready for discussion yet.  anyone have anything they want to bring up?
14:33 &lt;jrandom2p&gt; not i
14:33 &lt;@duck&gt; *hick*
14:34 &lt;@smeghead&gt; either duck is inebriated, or he has spotted a redneck
14:34 &lt;@duck&gt; !former
14:35 &lt;jrandom2p&gt; (to evaluate as a shell command or c/java... ;)
14:36 &lt;jrandom2p&gt; anyone else have anything to bring up for the meeting?
14:36  * jrandom2p likes short meetings, leaves more time for coding
14:36 &lt;@smeghead&gt; and drinking apparently :)
14:36 &lt;@duck&gt; & drinking
14:37 &lt;@smeghead&gt; bah lag
14:37 &lt;jrandom2p&gt; heh
14:38 &lt;jrandom2p&gt; ok, time to get back to dri^Wworking
14:38  * jrandom2p winds up
14:38  * jrandom2p *baf*s the meeting closed
</div>
