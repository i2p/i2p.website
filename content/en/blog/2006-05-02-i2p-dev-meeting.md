---
title: "I2P Dev Meeting - May 02, 2006"
date: 2006-05-02
author: "jrandom"
description: "I2P development meeting log for May 02, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> green, jrandom</p>

## Meeting Log

<div class="irc-log">
16:09 &lt;jrandom&gt; 0) hi
16:09 &lt;jrandom&gt; 1) Net status
16:09 &lt;jrandom&gt; 2) Syndie status
16:09 &lt;jrandom&gt; 3) ???
16:09 &lt;jrandom&gt; 0) hi
16:09  * jrandom waves
16:10 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-May/001285.html
16:11 &lt;jrandom&gt; ok, while y'all read through that exciting mail, lets jump on in to 1) Net status
16:13 &lt;jrandom&gt; so far, it seems the whole congestion collapse issue is fixed, yand tunnel creation rates are doing pretty well.  still, there are issues left to be sorted out
16:14 &lt;jrandom&gt; the previously discussed cyclic behavior (often running on 10-12 minute intervals) is still in place,causing rejections inversely.  there's a new fix to the code as of -1 that should get rid of that though
16:15 &lt;jrandom&gt; (namely, randomize the tunnel expirations /correctly/, unlike the broken randomization before)
16:16 &lt;jrandom&gt; that, plus the improved ssu and tunnel test scheduling should help, but to what dgree, i'm not entirely sure yet
16:17 &lt;jrandom&gt; ok, thats about all i have on that at the moment.  anyone have any questions/comments/concerns on 1) Net status?
16:18 &lt;green&gt; humm, max bw limits are never reached and this is really far from previous
16:18 &lt;green&gt; like in 1-7
16:18 &lt;green&gt; s/1-7/.12-7
16:18 &lt;jrandom&gt; how is your bw share percentage set?  thats now a very powerful control
16:19 &lt;green&gt; 80%
16:19 &lt;green&gt; but only about 40% of total bw is used
16:20 &lt;green&gt; this is just a "do nothing router" :P
16:20 &lt;jrandom&gt; hmm, how often does your bw spike up to 80%, and do you often reject tunnel requests (http://localhost:7657/oldstats.jsp#tunnel.reject.30 and tunnel.reject.*)
16:21 &lt;jrandom&gt; the periodicity seen in tunnel requests often causes people to detect overload when it isn't really there
16:21 &lt;jrandom&gt; (because routers have excess capacity at other times, just not when they're being spiked)
16:22 &lt;green&gt; tunnel.reject.30 is very flat like 1,00 over 14 025,00 events
16:22 &lt;jrandom&gt; oh, sorry, its the event count theselves for that stat thats key - you've rejected more than 14,000 tunnel requests due to bandwidth overload
16:23 &lt;jrandom&gt; (the "value" for that stat is how many tunnels were rejected at the event, and thats always 1, since an event is caused by a message)
16:27 &lt;jrandom&gt; ok, if there's nothing else on 1) Net status, lets slide on over to 2) Syndie status
16:27 &lt;jrandom&gt; I don't have much more to add to whats in the email regarding syndie, just wanted to give an update
16:28 &lt;jrandom&gt; ok, as such, unless there's something someone wants to bring up wrt syndie, lets jump on to ol' faithful, 3) ???
16:28 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
16:31  * tethra would like to say "thanks" (again) for .17, as it has been muchos improvement
16:33 &lt;jrandom&gt; glad to help, and there's more stuff on the way
16:33 &lt;jrandom&gt; ok, but if there's nothing else for toay's meeting...
16:33  * jrandom winds up
16:33  * jrandom *baf*s the meeting closed
</div>
