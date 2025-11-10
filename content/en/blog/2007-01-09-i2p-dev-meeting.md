---
title: "I2P Dev Meeting - January 09, 2007"
date: 2007-01-09
author: "jrandom"
description: "I2P development meeting log for January 09, 2007."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, jrandom, nony, tea, tethra, void, zzz</p>

## Meeting Log

<div class="irc-log">
15:07 &lt;jrandom&gt; 0) hi
15:07 &lt;jrandom&gt; 1) Net status
15:07 &lt;jrandom&gt; 2) I2Phex 0.1.1.38
15:07 &lt;jrandom&gt; 3) Syndie progress
15:07 &lt;jrandom&gt; 4) Syndie bug harvesting contest
15:07 &lt;jrandom&gt; 5) ???
15:07 &lt;jrandom&gt; 0) hi
15:07  * jrandom waves
15:07 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2007-January/001328.html
15:09 &lt;jrandom&gt; while y'all continue drooling over the macworld stuff, lets jump on in to 1) net status
15:09 &lt;jrandom&gt; i don't have anything to mention here this week, but felt bad not including the net status in the report, so here it is
15:09 &lt;jrandom&gt; anyone have anything to add regarding the network status?
15:09 &lt;+zzz&gt; I'm testing a couple of i2psnark tweaks, nothing major
15:10 &lt;jrandom&gt; ah cool, regarding the recent bug reports, or other goodies we can look forward to?
15:11 &lt;+zzz&gt; other - mostly better handling of torrents with&gt; 4 peers
15:11 &lt;jrandom&gt; wikked
15:11 &lt;+zzz&gt; also catching a couple of common OOM spots rather than dumping the whole JVM
15:12 &lt;tea&gt; sounds great, atm i2p-bt seems the best choice for "high"-speed torrents
15:12 &lt;+zzz&gt; i.e where it grabs a whole 256KB - 1MB chunk to store a piece
15:13 &lt;+zzz&gt; everybody pick a torrent and pile onto it to help me test :)
15:14 &lt;jrandom&gt; kickass, let us know when we should try things out zzz
15:14 &lt;tea&gt; shall someone redo 'casino royale' ? :)
15:14  * jrandom mentions that this meeting is logged and posted on the web ;)
15:15 &lt;+void&gt; oh, the meeting
15:15 &lt;tea&gt; no volunteers, then
15:16 &lt;jrandom&gt; ok cool, anyone have anything else for 1) Net status?
15:17 &lt;bar&gt; while we're mentioning i2psnark...
15:18 &lt;bar&gt; ...would it be possible to start, stop and restart i2psnark from the console?
15:18 &lt;bar&gt; (rather than restarting the whole router to kill the tunnels)
15:19 &lt;+zzz&gt; don't know - jrandom you have any thoughts?
15:20 &lt;jrandom&gt; bar: when you say stop and start, what does that entail beyond stopping and starting the inividual torrents?
15:21 &lt;bar&gt; killing the i2psnark tunnels that are draining my resources when not torrenting
15:22 &lt;bar&gt; (the tunnels don't die when you remove the .torrents, iirc)
15:22 &lt;jrandom&gt; ah, stopping the actual i2p destination for it.  doable without much trouble, the web interface has access to the SnarkManager
15:23 &lt;jrandom&gt; (an interim workaround could be to set the tunnel lengths to 0 until you need to use them again)
15:23 &lt;jrandom&gt; but you're right, that would be useful
15:23 &lt;+void&gt; you could change the tunnels to have 0 depth, although that would be error prone
15:23 &lt;+zzz&gt; good idea to provide a stop tunnel button on the web page, agreed
15:23  * jrandom !hi5s void
15:24 &lt;+void&gt; ack, i'm lagging *that* much?
15:24 &lt;jrandom&gt; I2PSnarkUtil already has a static .disconnect() too
15:25 &lt;jrandom&gt; (so calling that from the I2PSnarkServlet should be trivial)
15:25 &lt;jrandom&gt; zzz: you wanna hit that, or you want me to toss that in there?
15:27 &lt;+zzz&gt; I don't see a question there so take it
15:27 &lt;jrandom&gt; ok cool, shall do
15:27 &lt;jrandom&gt; ok, anyone have anything else on 1) Net status?
15:29 &lt;jrandom&gt; if not, lets hop over to 2) I2Phex 0.1.1.38
15:29 &lt;jrandom&gt; Complication: wanna pelt us with the low down?
15:31 &lt;jrandom&gt; afaik, there's a good summary of changes in the CVS and announcement (http://forum.i2p.net/viewtopic.php?t=2005)
15:33 &lt;tea&gt; is there a possibility of permantly changing the tunnel lengths ?
15:34 &lt;jrandom&gt; sure, i recall there's a place where you can set them in the i2phex config file by specifying the custom i2p options (though i don't recall the i2phex config file option to use at the moment)
15:35 &lt;bar&gt; tea: yes, in i2phex.cfg (i2pInboundLength, i2pInboundLengthVariance, i2pOutboundLength, i2pOutboundLengthVariance)
15:36 &lt;tea&gt; i was thinking of the option tab i2p-rufus has
15:37 &lt;tea&gt; could something like that be added ? 
15:38 &lt;jrandom&gt; i think complication said that'd be a good idea, so its probably pretty doable
15:38  * jrandom hasn't done any gui hacking in i2phex (though I'm sure if you sent in a patch, I'd make sure it went in :)
15:38 &lt;jrandom&gt; oh, nm, seems complication said 'e's working on it
15:39 &lt;jrandom&gt; http://forum.i2p.net/viewtopic.php?t=2005#9149
15:39 &lt;tea&gt; as an amateur rufus user i was pleased to see the pop up question 'allow zero hop connections ?', and be able to click no ...
15:42 &lt;jrandom&gt; aye.  ok, anyone have anything else on 2) I2Phex 0.1.1.38?
15:42 &lt;bar&gt; well, while we're at it, i think congratulations to the original Phex team on their 3.0 release are in order, it came out just the other day :)
15:43  * bar waves
15:43 &lt;jrandom&gt; aye, congrats ArneBab et al!
15:45 &lt;tea&gt; maybe they'll wave back one day ...
15:46 &lt;jrandom&gt; ArneBab and GregorK have had some good feedback on i2phex over the years 
15:46 &lt;+void&gt; the day that i2phex reaches version 3.0?
15:46 &lt;jrandom&gt; here's hopin :)
15:47 &lt;bar&gt; we'll be long gone by then, but yeah :)
15:48 &lt;jrandom&gt; ok, lets jump on over to 3) Syndie progress
15:48 &lt;jrandom&gt; lots of progress in the last week, including 1.001a hitting the street
15:50 &lt;jrandom&gt; though most of the discussion on that front is going on within syndie itself
15:50 &lt;jrandom&gt; so, if you're not on it yet, get on it and find out more :)
15:51 &lt;jrandom&gt; anyone have anything they'd like to discuss regarding syndie?
15:53 &lt;+void&gt; well, i just ran sync and it imported one unread message with a bunch of read ones
15:53 &lt;+void&gt; but i guess we'll debug that after the meeting?
15:54 &lt;jrandom&gt; hmm, aye, quite strange (i imported a few new messages recently, and they showed up as unread).  but yeah definitely need to dig some more into that
15:54 &lt;jrandom&gt; ok, lets hop on over to 4) Syndie bug harvesting contest
15:55 &lt;+void&gt; can you register anonymous egold accounts?
15:55 &lt;jrandom&gt; aye, no ID necessary
15:56 &lt;+void&gt; ah, cool
15:56 &lt;jrandom&gt; though, of course, they can freeze fraudulent accounts, and they do track all the transfers, and share the transfer data with Them
15:56 &lt;jrandom&gt; but it is more than sufficient to defend against most adversaries
15:57 &lt;+void&gt; yeah, naturally
15:58  * jrandom has found the bug reports and feature requests invaluable, and while I realize the $50USD doesn't come close to compensate the actual time involved, its hopefully a small token of thanks
15:58 &lt;jrandom&gt; I'm hoping we'll continue this contest every month
15:58 &lt;+void&gt; hehe
15:59 &lt;+void&gt; heheat least it's fun time
15:59 &lt;+void&gt; arg
16:00 &lt;jrandom&gt; does anyone have any questions regarding the contest, or suggestions, or frisbees?
16:01 &lt;+tethra&gt; contest?
16:01 &lt;+tethra&gt; (i am late)
16:01  * tethra reads up
16:01 &lt;+tethra&gt; cool :o
16:02 &lt;jrandom&gt; so get yer bug reports flowin' :)
16:03 &lt;jrandom&gt; ok, lets swing on over to 5) ???
16:03 &lt;+void&gt; they already are :)
16:03 &lt;+tethra&gt; yessir! ;)
16:03 &lt;jrandom&gt; aye, thanks!  (yes, I'm counting everything from jan1 to jan31 :)
16:03 &lt;jrandom&gt; ok, anyone have anything else to bring up for the meeting?
16:04 &lt;+fox&gt; &lt;nony&gt; does it run on java6?
16:04 &lt;tea&gt; sure
16:04 &lt;+tethra&gt; come to that, does it compile with gcj?
16:04 &lt;jrandom&gt; nony: i run it on java6 here, yes
16:04 &lt;jrandom&gt; tethra: aye, and runs ;)
16:04 &lt;+tethra&gt; excellent
16:04 &lt;+tethra&gt; ;)
16:04 &lt;+fox&gt; &lt;nony&gt; sweet
16:07 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:09 &lt;jrandom&gt; if not...
16:09  * jrandom winds up
16:09  * jrandom *baf*s the meeting closed
</div>
