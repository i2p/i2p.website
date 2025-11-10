---
title: "I2P Dev Meeting - October 24, 2006"
date: 2006-10-24
author: "jrandom"
description: "I2P development meeting log for October 24, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> badger, bar, cervantes, Complication, HotTuna, jrandom, tethra</p>

## Meeting Log

<div class="irc-log">
16:03 &lt;jrandom&gt; 0) hi
16:03 &lt;jrandom&gt; 1) Net status
16:03 &lt;jrandom&gt; 2) Syndie dev status
16:03 &lt;jrandom&gt; 3) ???
16:03 &lt;jrandom&gt; 0) hi
16:03  * jrandom waves
16:03  * Complication stumbles to somewhere within reach of keyboard (week's beginning was hell, but it's over now)
16:04 &lt;jrandom&gt; (hooray to hellish beginnings!)
16:04 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-October/001315.html
16:04 &lt;+Complication&gt; Hello
16:05 &lt;jrandom&gt; while y'all read the (short) notes, lets jump to 1) Net status
16:05  * jrandom has been connected to freshcoffee for 3 days now w/out discon, and it looks like both of the irc servers have a good number of users on them
16:06 &lt;jrandom&gt; stats.i2p is back too, and the tunnel success rate has been doing some odd jumps, but generally in good shape too
16:06 &lt;jrandom&gt; (though still in the 20-30 range)
16:06 &lt;jrandom&gt; ((which is much better than 5-10, but much worse than 60-80))
16:07 &lt;jrandom&gt; ok, anyone have anything to bring up for 1) net status?
16:08 &lt;+Complication&gt; Similar here, but no extra-persistent connections
16:08 &lt;+tethra&gt; other than applause, nothing from me!
16:08 &lt;+Complication&gt; I just wanted to drop a little line related to NTP issues
16:09 &lt;+Complication&gt; Basically, on Sunday, Oct 29, some times zones will jump off dailight saving time
16:09 &lt;jrandom&gt; (its going to suck)
16:10 &lt;+Complication&gt; I personally hope it doesn't cause anyone any problems, but I'm not well versed enough in NTP to be sure
16:10 &lt;+Complication&gt; So, just in case the recent NTP server sanity check (added with version .26) should inconvenience someone that night...
16:11 &lt;+Complication&gt; ...I thought it'd be better if I mentioned the configuration key using which it can be disabled (if need should exist)
16:11 &lt;+Complication&gt; (so folks who read status notes would know)
16:12 &lt;+Complication&gt; Disabling it can be done by entering the line "router.clockOffsetSanityCheck=false" into http://localhost:7657/configadvanced.jsp
16:12 &lt;+Complication&gt; But as mentioned, I do hope nobody needs that
16:13 &lt;+Complication&gt; It will be interesting to watch and see how the network behaves that night, though, as different time zones start switching
16:13 &lt;+Complication&gt; I'll certainly observe, in hope that if any anomaly is seen, perhaps it can be fixed by Spring :D
16:14 &lt;jrandom&gt; the minute-of will probably be pretty jumpy, but should heal shortly
16:14 &lt;+Complication&gt; ...and that's all I had. :)
16:14 &lt;jrandom&gt; but, hopefully it'll work out, and if not, as you say, there's spring :)
16:14 &lt;bar&gt; and should things indeed b0rk, there were two possible suggestions for future improvement that surfaced in the chat the other day:
16:15 &lt;bar&gt; "prevent skewed routers from forming subnets by handing over control to NTP if peers &lt;some number"
16:15 &lt;bar&gt; ...and "do not delete floodfill peer router infos from netdb if there are too few of them"
16:15 &lt;jrandom&gt; aye
16:16 &lt;+Complication&gt; Indeed, adjusting the required number of data points (available peer clock skews) which are required to deem peer skew measurements reliable
16:16 &lt;+Complication&gt; (oops, some redundancy in my last sentence)
16:17 &lt;+Complication&gt; ...and yes, the floodfill check. I take that no similar check exists currently?
16:18 &lt;jrandom&gt; right
16:18 &lt;+Complication&gt; Seems like some people, sometimes, either with luck or magic, may be managing to lose track of floodfill peers
16:19 &lt;jrandom&gt; that should certainly be remedied
16:19 &lt;jrandom&gt; (it hit some folks the other day, when one of 'em was null routed)
16:20 &lt;jrandom&gt; (if #floodfill == 0, perhaps randomly treat a few as floodfill)
16:20 &lt;+Complication&gt; If that's doable, possible also
16:21 &lt;+Complication&gt; Though, perhaps doing that in addition to keeping at least 2 (or something like that) floodfill peers would be a doubly safe bet
16:22 &lt;jrandom&gt; aye
16:25 &lt;jrandom&gt; ok, anyone have anything else for 1) net status?  or shall we move on over to 2) syndie dev status?
16:25 &lt;badger&gt; re irc stability: seeing much much much fewer reconnects at the server end.
16:25 &lt;badger&gt; you could almost call it a service :)
16:26 &lt;jrandom&gt; :)
16:28 &lt;jrandom&gt; ok, jumping on to 2) syndie dev status
16:28 &lt;jrandom&gt; lots of progress here, as mentioned in the status notes
16:28 &lt;jrandom&gt; there's also been a bunch of discussion on it here over the last few days
16:28 &lt;jrandom&gt; anyone have anything they want to bring up on that front?
16:30 &lt;@cervantes&gt; install something other than mspaint
16:30 &lt;jrandom&gt; heh
16:30 &lt;jrandom&gt; well, there's value in using *ugly* things to sketch - limits expectations
16:31 &lt;+fox&gt; &lt;HotTuna&gt; the links in the forumpost seem to be down ... some are anyway..
16:31 &lt;@cervantes&gt; I think that's mentioned in the posts
16:31 &lt;+fox&gt; &lt;HotTuna&gt; oh. . sorry
16:31 &lt;jrandom&gt; hottuna: they're mirrored @ dev.i2p.net/~jrandom/mockup/
16:31 &lt;@cervantes&gt; some should be mirrored further down
16:32 &lt;+Complication&gt; One question: so, do you think it's easier to (safely) implement limited HTML from ground up, without picking apart some web browser?
16:33  * jrandom just uploaded two more pics: dev.i2p.net/~jrandom/mockup/forum.png and blog.png (showing the discussion of the last few days regarding different ways to view a forum)
16:33 &lt;@cervantes&gt; most definitely easier to do that safely
16:33 &lt;+Complication&gt; (just being curious as to what's going in on the GUI side, having been somewhat unaware of it)
16:33 &lt;jrandom&gt; Complication: i've got nearly everything done for general formatting purposes already
16:33 &lt;@cervantes&gt; especially given the limited subset of html that syndie will support
16:34 &lt;+Complication&gt; Aha
16:34 &lt;jrandom&gt; (fonts, alignment, sizes, colors, images, links, lists (including nested), headers, paragraphs, html entities)
16:35 &lt;jrandom&gt; now, going in and doing divs for placement or tables requires substantially more work, but i'm not tackling that now
16:35 &lt;+Complication&gt; Sounds nice enough
16:36 &lt;@cervantes&gt; and of course the &lt;blink&gt; tag
16:36  * jrandom pelts cervantes with &dagger;
16:37 &lt;@cervantes&gt; ouch, skewered by an entity
16:37 &lt;jrandom&gt; we'll see though.  as it gets deployed and used, perhaps it'll be necessary to switch to a full blown html rendering engine
16:38  * jrandom wants the codebase to be as small as possible though, so there is less to debug and review for security and anonymity issues
16:39 &lt;+Complication&gt; Indeed, there are doubtless benefits to handling text/plain
16:40 &lt;+Complication&gt; (which hopefully only supports natural-language attacks ;P )
16:41 &lt;+Complication&gt; What are your opinions about the possibility of hashcash antispam measures? Too early to tell? Do you think they'd be easy to tack on later?
16:42 &lt;@cervantes&gt; well I guess using bbcode or wiki syntax would reduce the risk of markup injection in a full html engine
16:42 &lt;@cervantes&gt; *rendering engine
16:43 &lt;jrandom&gt; quite easy to tack on Complication - just a new public header (hashcalc'ed against the canonical syndie uri, verified on import, created on signing)
16:44  * Complication thought about some a few days back, but only lightly
16:44 &lt;jrandom&gt; the hashcash can be done at several levels too - per new channel (meta.syndie), per updated channel, or per post (perhaps even graduated against sizeof(post) or #msgs/day)
16:44 &lt;+Complication&gt; If one wanted to implement hashcash as proof of work, I wonder what the poster of the message would be best required to caclulate collisions against?
16:45 &lt;+Complication&gt; Aha, the uri... might be indeed
16:45 &lt;+Complication&gt; Oh, indeed
16:45 &lt;+Complication&gt; That's some things I didn't think about
16:48 &lt;jrandom&gt; cervantes: true enough
16:48 &lt;jrandom&gt; ok, anyone have anything else for 2) syndie dev status?
16:51 &lt;jrandom&gt; ok, if not, lets jump to 3) ???
16:51 &lt;jrandom&gt; anyone have anything else they want to bring up?
16:54 &lt;jrandom&gt; ok, if not...
16:54  * jrandom winds up
16:54  * jrandom *baf*s the meeting closed
</div>
