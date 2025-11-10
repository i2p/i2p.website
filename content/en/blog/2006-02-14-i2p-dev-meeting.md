---
title: "I2P Dev Meeting - February 14, 2006"
date: 2006-02-14
author: "jrandom"
description: "I2P development meeting log for February 14, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cervantes, Complication, duck, frosk, jrandom, void</p>

## Meeting Log

<div class="irc-log">
15:39 &lt;jrandom&gt; 0) hi
15:39 &lt;jrandom&gt; 1) Net status
15:39 &lt;jrandom&gt; 2) 0.6.1.10
15:39 &lt;jrandom&gt; 3) Syndie activity
15:39 &lt;jrandom&gt; 4) ???
15:39 &lt;jrandom&gt; 0) hi
15:39  * jrandom waves
15:39 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-February/001260.html
15:39 &lt;jrandom&gt; (I'm a lil late with that, so I'll give y'all a minute to skim through those brief notes)
15:40 &lt;+Complication&gt; hello
15:40 &lt;@cervantes&gt; 'lo
15:41 &lt;jrandom&gt; well, its brief enough, so lets just jump on in to 1) Net status
15:41 &lt;jrandom&gt; I don't have anything to add to this one, anyone have something on it to discuss?
15:41 &lt;@cervantes&gt; &lt;jrandom&gt; (damn flakey net connection)
15:41 &lt;+Complication&gt; A bit congested occasionally, but graphs suggest it's nothing new
15:42 &lt;jrandom&gt; heh cervantes, well, thats due to one of my roommates using limewire, not i2p ;)
15:43 &lt;@cervantes&gt; we've had various server problems too with irc and postman's tracker over the past couple of weeks - postman has done a lot of migrations, so things should be more stable for folk
15:43 &lt;+Complication&gt; It must be hard letting them do that, but I guess... such is life :O
15:43 &lt;+Complication&gt; do that=use limewire
15:44 &lt;+Complication&gt; This morning, tracker.postman.i2p was refusing connections, though
15:44 &lt;jrandom&gt; Complication: disk was full, fixed now
15:44 &lt;jrandom&gt; (new machines have their new quirks)
15:46 &lt;jrandom&gt; ok, anyone have anything else on 1) Net status?
15:46 &lt;jrandom&gt; otherwise, lets shimmy on over to 2) 0.6.1.10
15:47 &lt;jrandom&gt; As mentioned, we're going to have a new backwards incompatible release in a few days
15:48 &lt;jrandom&gt; while it alone won't revolutionize our performance, it will improve a few key metrics to get us on our way
15:48 &lt;jrandom&gt; there are also a whole bunch of bug fixes in there too
15:49 &lt;@cervantes&gt; will zzz's server tunnel improvements make the fold?
15:49 &lt;jrandom&gt; oh, and there's that whole improved anonymity thing... ya know, sine qua non
15:50 &lt;jrandom&gt; cervantes: probably not, haven't heard much since that post to zzz.i2p last week.  i did do some minor bugfixes in cvs though (to should support lighttpd, etc), but we won't have zzz's persistent connections
15:50 &lt;jrandom&gt; (yet)
15:51 &lt;@frosk&gt; what DH key size/etc did you land on?
15:51 &lt;@cervantes&gt; yeah, I saw those newline issues a few weeks ago, but I held off changing them because of zzz's impending improvements
15:51 &lt;jrandom&gt; ah, for the moment we'll be sticking with 2048bit crypto with small exponents
15:52 &lt;@frosk&gt; so some lower cpu consumption can be expected?
15:52 &lt;jrandom&gt; aye
15:53 &lt;@frosk&gt; excellente
15:53 &lt;jrandom&gt; switching to 1024bit would cut another order of magnitude to the CPU load, but would require some reworking of the tunnel creation structures (1024bit asym isn't large enough to convey the data we need to convey).  
15:54 &lt;jrandom&gt; we may explore that in the future though, but this next release should substantially cut down cpu overhead
15:54 &lt;jrandom&gt; I've also disabled the TCP transport, because I'm a mean and vicious person
15:55 &lt;@frosk&gt; do you expect any more incompatible upgrades before 1.0?
15:55 &lt;jrandom&gt; hope not
15:55  * cervantes must be a danish cartoonist
15:55 &lt;@frosk&gt; i don't think we'll miss tcp :)
15:55 &lt;@cervantes&gt; I mean jrandom must be
15:55 &lt;@cervantes&gt; ;-)
15:55  * jrandom watches the embassy burn
15:56 &lt;jrandom&gt; ok, anyone have anything else on 2) 0.6.1.10?
15:56 &lt;void&gt; why wouldn't it support lighttpd earlier?
15:56 &lt;jrandom&gt; (ah, as an aside, there have also been some interesting improvements to the streaming lib for 0.6.1.10, such as tcp-style fast retransmit, etc, so we'll see how that helps)
15:57 &lt;@cervantes&gt; void: malformed headers
15:57 &lt;jrandom&gt; void: bug where we weren't standards compliant
15:57 &lt;void&gt; ah, are these inconsistent newline bugs also fixed?
15:58 &lt;void&gt; and what about the null character one? are you waiting for zzz's persistent connection patch?
15:58 &lt;jrandom&gt; the newline bug is the malformed header, and is fixed
15:58 &lt;jrandom&gt; no news on the null character one
15:59 &lt;void&gt; ok
16:00 &lt;jrandom&gt; ok, if there's nothing else on 2, lets swing on by 3) Syndie activity briefly
16:00 &lt;jrandom&gt; well, I don't really have much to add...
16:01 &lt;jrandom&gt; (I /did/ say briefly)
16:01 &lt;jrandom&gt; so lets jump on to 4) ???
16:01 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
16:01 &lt;+fox&gt; &lt;duck&gt; too busy reading Syndie to comment
16:01 &lt;jrandom&gt; ;)
16:02  * Complication is too busy issuing meaningless signatures to comment :D
16:05 &lt;jrandom&gt; ok cool.  just another reminder for people to stay away from CVS for the next day or two until the release, as CVS HEAD is going to get the _PRE branch's changes, and the _PRE branch is going to be retired
16:05  * jrandom winds up
16:05  * jrandom *baf*s the meeting closed
</div>
