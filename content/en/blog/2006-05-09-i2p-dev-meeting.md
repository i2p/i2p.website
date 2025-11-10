---
title: "I2P Dev Meeting - May 09, 2006"
date: 2006-05-09
author: "jrandom"
description: "I2P development meeting log for May 09, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> arse, cervantes, Complication, i, jrandom, roderick_spod1, tmp</p>

## Meeting Log

<div class="irc-log">
16:31 &lt;jrandom&gt; 0) hi
16:31 &lt;jrandom&gt; 1) Net status and 0.6.1.18
16:31 &lt;jrandom&gt; 2) baz
16:31 &lt;jrandom&gt; 3) ???
16:31 &lt;jrandom&gt; 0) hi
16:31  * jrandom waves
16:32 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-May/001288.html
16:32 &lt;jrandom&gt; while y'all read through that, lets jump on in to 1) Net status and 0.6.1.18
16:33 &lt;jrandom&gt; the past week has been pretty bumpy on irc & the net in general
16:33 &lt;+Complication&gt; Watching the graphs, but haven't noticed a perceivable change yet
16:33 &lt;+Complication&gt; Only the beginning too, of course
16:34 &lt;jrandom&gt; aye, its only been a few hours, with under 20% of the net upgraded
16:35 &lt;jrandom&gt; there are still a few big guns left to deploy on the net, but I'd like things to stabilize first before pushing out major changes
16:35 &lt;+Complication&gt; Indeed, it helps to see (as much as seeing is possible) what changes what, and in which direction
16:36 &lt;+Complication&gt; If one deploys everything at once, figuring out what worked may be very tough
16:38 &lt;tmp&gt; *sigh* 
16:38  * tmp dreams of IRC stability.
16:39 &lt;jrandom&gt; aye, on all fronts ;)
16:39 &lt;+fox&gt; &lt;roderick_spod1&gt; Roderick dreams of big tits.
16:39 &lt;jrandom&gt; (this is why we can filter the meeting logs... ;)
16:40 &lt;jrandom&gt; ok, anyone have anything else for 1) Net status and 0.6.1.18?
16:41 &lt;jrandom&gt; if not, lets hop on over to 2) 
16:42 &lt;jrandom&gt; not much more to add here, just giving a status update on some w32/w64 support
16:43 &lt;jrandom&gt; as mentioned in the mail, gcj doesn't really seem viable on mingw atm, though we might be able to pull some tricks
16:44 &lt;jrandom&gt; there is an older 3.4.4/3.4.5 gcj that works on mingw, but the classpath suport in there is pretty old.
16:45 &lt;jrandom&gt; (and even after stripping a bunch out of hsqldb, there are still some dependencies that 3.4.5 doesn't meet.  but maybe we can hack those out too... if necessary)
16:47 &lt;jrandom&gt; ok, if there's nothing else, lets move on over to 3) ???
16:47 &lt;jrandom&gt; anyone have anything else to bring up for the meeting?
16:48 &lt;cervantes&gt; just to say "nice one bar" for his cool donation 
16:48 &lt;+Complication&gt; Well, there was a question in the forum about uptimes presented in NetDB...
16:48  * Complication seconds that
16:49 &lt;+Complication&gt; 'bout the uptimes, if you recall, I fuzzified them slightly in March...
16:49 &lt;cervantes&gt; must have missed that amongst the odci.gov rants
16:50 &lt;tmp&gt; What on earth are you doing on that side roderick_spod?
16:50 &lt;jrandom&gt; aye Complication 
16:50 &lt;+Complication&gt; Well, since the question was raised, I wondered if they could be fuzzified further, or would it hurt ability to debug?
16:52 &lt;jrandom&gt; i'm not sure of the point - with careful analysis, all of the stat data can reveal a bunch of information
16:52 &lt;arse&gt; do you guys think the network periodicity is gonna subside
16:52 &lt;jrandom&gt; when its time, we will just turn off the stat publhshing whatsoever
16:52 &lt;+Complication&gt; We haven't recently had any router-restarting ones, but that's only recently...
16:52 &lt;jrandom&gt; arse: yes
16:52 &lt;+Complication&gt; (and partly because the watchdog lacks teeth)
16:54 &lt;+Complication&gt; True, it's pretty inevitable that during this phase, some info must be out there
16:55 &lt;jrandom&gt; also, the assumption they've made isn't correct, publishedTimeAgo is how long ago the router /received/ the netDb entry, not when it was signed
16:55 &lt;jrandom&gt; erm, wait, no, thats not true
16:56 &lt;jrandom&gt; never mind me.  yeah, it just adds a small variation
16:56 &lt;+Complication&gt; Heh, I'm trying to post a reply, but get "no post mode specified" currently
16:57 &lt;+Complication&gt; Yeah, there's delay involved, and besides, how often was this info published? Not very frequently, IIRC?
16:57 &lt;+Complication&gt; Basically, if I offered to somewhat decrease the precision there, would you mind?
16:58 &lt;jrandom&gt; a new signed entry is published eery 5-15 minutes, but that is only published to the netDb, not all peers
16:58 &lt;jrandom&gt; peers only get the updated one when they either search for it or they reconnect
16:59 &lt;jrandom&gt; but yeah, adding more variation is fine.  it'd affect stat.i2p's uptime plots, but as long as it keeps things reasonable, thats cool
17:01 &lt;+Complication&gt; I'll try to keep it reasonable, then :)
17:01 &lt;jrandom&gt; heh cool, thanks Complication 
17:04 &lt;jrandom&gt; *cough* (and consistent ;) ok, anyone have anything else for the meeting?
17:04 &lt;+Complication&gt; sidenote: neat, the "post mode" bug yielded to persistence, and I could post a reply too :)
17:05 &lt;jrandom&gt; w3rd Complication 
&lt;i&gt;offtopic messages snipped&lt;/i&gt;
17:08 &lt;jrandom&gt; ok, if there's nothing else...
17:08  * jrandom winds up
17:09  * jrandom *baf*s the meeting closed
</div>
