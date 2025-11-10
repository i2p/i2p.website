---
title: "I2P Dev Meeting - December 07, 2004"
date: 2004-12-07
author: "@duck"
description: "I2P development meeting log for December 07, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bushka, clayboy, dinoman, duck, Frooze, mule, postman, protokol, Ragnarok, slart, ugha2p</p>

## Meeting Log

<div class="irc-log">
22:00:00 &lt;@duck&gt; Tue Dec  7 21:00:00 UTC 2004
22:00:04 &lt;@duck&gt; I2P meeting time
22:00:05 &lt;Frooze&gt; i just made Frooze up for i2p.  i don't even know what a 'frooze' is.
22:00:21 &lt;@duck&gt; as announced on http://dev.i2p.net/pipermail/i2p/2004-December/000509.html
22:00:29 &lt;@duck&gt; Agenda:
22:00:29 &lt;@duck&gt; 0) hi
22:00:29 &lt;@duck&gt; 1) 0.4.2.3
22:00:29 &lt;@duck&gt; 2) i2p-bt
22:00:29 &lt;@duck&gt; 3) #idlerpg
22:00:29 &lt;@duck&gt; 4) ???
22:00:32 &lt;@duck&gt; .
22:01:09 &lt;@duck&gt; 0) hi
22:01:15 &lt;clayboy&gt; hi
22:01:16 &lt;@duck&gt; jrandom called in sick
22:01:20 &lt;+ugha2p&gt; Hi.
22:01:30 &lt;@duck&gt; plus msged me that he'd probably not make it
22:01:39 &lt;+protokol&gt; http://www.google.com/search?q=frooze
22:01:41 &lt;@duck&gt; so we'll see and just start
22:01:46 &lt;clayboy&gt; hope he gets better quick
22:02:06 &lt;@duck&gt; 1) 0.4.2.3
22:02:16 &lt;@duck&gt; new release will be out Real Soon
22:02:31 &lt;@duck&gt; so tomorrow or thursday.
22:02:41 &lt;@duck&gt; there has been quite a few bugfixes
22:03:24 &lt;+ugha2p&gt; Do newer CVS revisions also fix the memory/CPU issues?
22:03:29 &lt;clayboy&gt; a few of us have been following the cvs builds, it's working very nicely
22:03:33 &lt;@duck&gt; most streaming lib, sam bridge, etc
22:04:17 &lt;+ugha2p&gt; I've been experiencing some uncommon loads from I2P.
22:04:23 &lt;clayboy&gt; i think those were fixed many revisions ago, ugha2p
22:04:41 &lt;+ugha2p&gt; (Running -7)
22:04:51 &lt;clayboy&gt; oh, hm
22:04:52 &lt;@duck&gt; ugha2p: dont see anything about that in the history
22:05:48 &lt;+protokol&gt; you know what would be nice (if not feasable/worth it) is an RSS feed of the changelog
22:05:48 &lt;@duck&gt; ok
22:05:49 &lt;+ugha2p&gt; That's strange.
22:06:01 &lt;+protokol&gt; ;-)
22:06:17 &lt;@duck&gt; maybe file a bugzilla item
22:06:25 &lt;@duck&gt; or dunno
22:06:34 &lt;+ugha2p&gt; The Java process consumes 100% of CPU for about half of the time.
22:07:18 &lt;+ugha2p&gt; So, you don't know anything about the issue? Do your routers behave OK?
22:07:24 &lt;dinoman&gt; yea it is high for me to -6
22:08:24 &lt;@duck&gt; top/uptime info is behaving weird for me since my nptl upgrade, so cant say
22:09:03 &lt;+ugha2p&gt; Ok, maybe we should move on?
22:09:07 &lt;@duck&gt; ok
22:09:14 &lt;@duck&gt; 2) i2p-bt
22:09:24 &lt;+ugha2p&gt; And ask jrandom when he is about to release 0.4.2.3
22:09:40 &lt;+ugha2p&gt; It has worked fine for me with NPTL.
22:09:45 &lt;@duck&gt; ugha2p: he said tomorrow or thursday
22:09:58 &lt;+ugha2p&gt; Right.
22:09:59 &lt;@duck&gt; yesterday I released a new i2p-bt
22:10:23 &lt;@duck&gt; I gained some new understanding of the whole 'buffer' concept
22:10:42 &lt;@duck&gt; plus there were some previous pending patches from Ragnarok
22:11:13 &lt;mule&gt; duck: congratulations, good work!
22:11:15 &lt;@duck&gt; also the slice size is increased, which means that instead of sending 32KB each time, it sends 128KB
22:11:29 &lt;@duck&gt; which should keep the queue filled
22:11:47 &lt;+ugha2p&gt; Yeah, thanks, duck. :)
22:11:56 &lt;@duck&gt; DrWoo and others filed some GUI feature requests
22:12:23 &lt;@duck&gt; but I never use the GUI myself, wouldnt know wxpython and probably dont care too much :)
22:12:31 &lt;+Ragnarok&gt; fitting each slice into a single message didn't work as well as expected?
22:12:57 &lt;clayboy&gt; many seeded torrents on http://brittanyworld.i2p/bittorrent/ if anyone want to try (with i2p 0.4.2.2-7 and i2p-bt 0.1.3)
22:13:10 &lt;@duck&gt; Ragnarok: it is a bit of a guess
22:13:27 &lt;@duck&gt; it gives much higher throughput values on local transfers
22:13:51 &lt;+ugha2p&gt; Maybe we should wait for someone to port a full-featured client instead?
22:14:10 &lt;+Ragnarok&gt; hm, ok
22:14:13 &lt;@duck&gt; we can all wait :)
22:14:37 &lt;clayboy&gt; BitTorrent _is_ "full featured", it's the only client i use for bt (also off i2p) :)
22:15:15 &lt;+ugha2p&gt; clayboy: Not really. :)
22:16:02 &lt;@duck&gt; personally I prefer things with sound defaults
22:16:17 &lt;@duck&gt; take mldonkey, you can change 1 million things and most users have no idea what they do
22:16:50 &lt;@duck&gt; this leads to user-myths, like i2p users hitting 'Reseed' all the time, or reinstalling if it doesnt work
22:17:01 &lt;+ugha2p&gt; If you aren't willing to find out, then you shouldn't be using Linux anyway. :)
22:17:04 &lt;@duck&gt; which kills kittens
22:17:28 &lt;slart&gt; what about bittornado?
22:17:43 &lt;+Ragnarok&gt; I suppose I could be tempted to write a pygtk gui, but I've got a lot of other stuff to do, and I'm not sure what people want
22:17:45 &lt;+protokol&gt; azureus?
22:17:57 &lt;@duck&gt; part of me is ofcourse making up excuses not to do things
22:18:03 &lt;+protokol&gt; azureus supports plugins
22:18:10 &lt;@duck&gt; protokol: well, write a plugin
22:18:32 &lt;+protokol&gt; heh
22:18:40 &lt;slart&gt; bittornado is based off the offical bt isnt it?
22:18:50 &lt;+protokol&gt; easier said than done
22:18:52 &lt;@duck&gt; slart: I have looked at it and wept
22:19:07 &lt;@duck&gt; it has some improvements, which might be useful
22:19:17 &lt;@duck&gt; but on the other hand it made the whole thing way more complex
22:19:22 &lt;@duck&gt; without cleaning up the original code
22:19:36 &lt;+Ragnarok&gt; gah
22:19:56 &lt;@duck&gt; the GUI feature that you can specify a torrent if no arguments are given is taken from it and added to i2p-bt
22:20:11 &lt;clayboy&gt; let's get the basic bittorrent working excellently before worrying about these fluffy gui things :)
22:20:46 &lt;@duck&gt; slart: probably some other things can be used too; someone just has to do it (properly)
22:21:23 &lt;+ugha2p&gt; clayboy: Well, I think it already does work excellently. :)
22:21:53 &lt;slart&gt; the abc client uses tornado (i think)
22:22:15 &lt;clayboy&gt; i feel like we have still to do some really heavy-duty testing to see how much data can really be pushed through i2p-bt
22:22:21 &lt;bushka&gt; yes it does slart.
22:23:49 &lt;@duck&gt; depending on how those work, you might be able to port the i2p-bt changes to them quite easily
22:24:41 &lt;@duck&gt; please give it a try and report back
22:25:47 &lt;@duck&gt; .
22:25:55 &lt;@duck&gt; any other i2p-bt / bittorrent comments?
22:26:08 &lt;slart&gt; python :S
22:26:41 &lt;+ugha2p&gt; .
22:26:51 &lt;@duck&gt; slart: if you dont like python, you can give porting azureus a try
22:27:00 &lt;+ugha2p&gt; slart: What about it?
22:27:06 &lt;slart&gt; how many people could we get seeding somthing like a linux is for speed testing?
22:27:15 &lt;slart&gt; *iso
22:27:34 &lt;@duck&gt; lets try that after the new i2p release
22:27:57 &lt;@duck&gt; (since pulling an i2p router build from cvs is quite a challenge for most)
22:28:17 &lt;+protokol&gt; eh
22:28:54 &lt;@duck&gt; pl
22:28:57 &lt;@duck&gt; err, ok
22:29:10 &lt;@duck&gt; 3) #idlerpg
22:29:22 &lt;@duck&gt; found this funny irc rpg game
22:29:36 &lt;@duck&gt; you dont have to do anything for it, just idle 
22:29:56 &lt;+ugha2p&gt; Well, you do have to LOGIN. ;)
22:30:04 &lt;@duck&gt; ah ;)
22:30:18 &lt;mule&gt; cvs update -dP :)
22:30:18 &lt;mule&gt; ant dist updater :)
22:30:20 &lt;+postman&gt; it's the most hilarious thing i've ever seen, but i LIKE it :)
22:30:30 &lt;+protokol&gt; there should be prizes
22:30:45 &lt;@duck&gt; on ircnet it has 779 online players 
22:30:46 &lt;+ugha2p&gt; duck: I was thinking, that it could potentially be a reason not to upgrade.
22:30:52 &lt;+protokol&gt; give yodels for winning stuff or reaching levels
22:31:03 &lt;+ugha2p&gt; Although I'm not sure if people on I2P could be that childish. :)
22:31:14 &lt;+protokol&gt; i know duck has like $10000 in yodels
22:31:18 &lt;@duck&gt; protokol: yeah, I have to see how those quests work
22:31:39 &lt;@duck&gt; maybe we can do some fun stuff with it
22:31:42 &lt;@duck&gt; ugha2p: what do you mean?
22:31:49 &lt;ant&gt; * cervantes is not going to do another 40 days without restarting his router
22:32:08 &lt;@duck&gt; ugha2p: oh, not update because of the game :)
22:32:18 &lt;+protokol&gt; Linux: If you can't fix it without restarting, you can't fix it.
22:32:20 &lt;@duck&gt; well, I'll put it on pause while my router restarts
22:32:24 &lt;+ugha2p&gt; :)
22:32:33 &lt;@duck&gt; so if you sync it well, you wont lose
22:32:35 &lt;@duck&gt; hehe
22:32:55 &lt;ant&gt; &lt;cervantes&gt; thats good... since your router restarts all the time :P
22:33:16 &lt;@duck&gt; thats called dedicated testing :)
22:33:20 &lt;ant&gt; &lt;cervantes&gt; I guess that throws roulette into the equation too
22:33:23 &lt;@duck&gt; ok
22:33:38 &lt;@duck&gt; .
22:33:49 &lt;+ugha2p&gt; .
22:34:05 &lt;@duck&gt; 5) ???
22:34:08 &lt;@duck&gt; s/5/4/
22:34:12 &lt;@duck&gt; open mike!
22:34:23 &lt;+postman&gt; .
22:34:53 &lt;mule&gt; with a bit of tweaking you can two routers. one for the game only, which you upgrade only every year
22:34:53 &lt;@duck&gt; questions? comments? suggestions?
22:35:38 &lt;ant&gt; &lt;mahes&gt; Hi, i have a general non-dev question
22:36:08 &lt;@duck&gt; shoot
22:36:08 &lt;+ugha2p&gt; Thanks for holding the meeting, duck.
22:36:50 &lt;ant&gt; &lt;mahes&gt; if i set up an eepsite , how can be reached with an address like i.e mahes.i2p
22:36:59 &lt;+protokol&gt; i have a consern
22:37:44 &lt;+protokol&gt; (start the battle) i think .i2p is a shitty TLD for many reasons
22:38:19 &lt;+ugha2p&gt; mahes: What do you mean 'how'? People will configure their browsers to use the eepproxy, and just enter http://mahes.i2p/ onto their address bar.
22:38:19 &lt;+protokol&gt; i think we should use one that is a) one syllable b) can be pronounced like a word c) does not include a number'
22:38:46 &lt;+ugha2p&gt; protokol: Like .eep?
22:39:07 &lt;@duck&gt; mahes:: to get a 'nice name' to point to your eepsite, it has to be present in your hosts.txt file
22:39:37 &lt;+protokol&gt; ugha2p: sure
22:40:01 &lt;+ugha2p&gt; protokol: You can make a proposal on the mailing list.
22:40:03 &lt;@duck&gt; you can post it on the eepsite announcement forum so others can get it too
22:40:09 &lt;+ugha2p&gt; It'll probably be considered once we have MyI2P.
22:40:35 &lt;+protokol&gt; heh, ill try but jr shot it down for some reason already
22:41:06 &lt;ant&gt; &lt;mahes&gt; well. i am just a user...  ok, so i just publish mahes.i2p=hhfbwer8328... and it will just spread
22:41:32 &lt;@duck&gt; it doesnt spread automatically, ppl need to get it into their hosts.txt somehow
22:41:39 &lt;ant&gt; &lt;mahes&gt; ok
22:41:52 &lt;@duck&gt; but announce it on the forum and it is more likely to :)
22:42:34 &lt;@duck&gt; .
22:43:18 &lt;@duck&gt; lets give it a *baf*
22:43:20 &lt;+ugha2p&gt; .
22:43:30  * ugha2p is waiting for the baffer.
22:43:38  * duck winds up
22:43:45  * duck *baf*s the meeting closed
</div>
