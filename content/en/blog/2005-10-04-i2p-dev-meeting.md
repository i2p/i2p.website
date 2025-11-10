---
title: "I2P Dev Meeting - October 04, 2005"
date: 2005-10-04
author: "jrandom"
description: "I2P development meeting log for October 04, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cat-a-puss, cervantes, Complication, jrandom, mancom, nickless_head, phedy, postman, protokol, Ragnarok</p>

## Meeting Log

<div class="irc-log">
16:16 &lt;jrandom&gt; 0) hi
16:16 &lt;jrandom&gt; 1) 0.6.1.1
16:16 &lt;jrandom&gt; 2) i2phex
16:16 &lt;@protokol&gt; speaking of, whats the news on legion and i2phex
16:16 &lt;jrandom&gt; 3) syndie
16:16 &lt;jrandom&gt; 4) ???
16:16 &lt;jrandom&gt; 0) hi
16:16  * jrandom waves
16:16 &lt;jrandom&gt; weekly status notes posted up to http://dev.i2p.net/pipermail/i2p/2005-October/000939.html
16:17 &lt;+postman&gt; hi
16:17 &lt;jrandom&gt; might as well jump into 1) 0.6.1.1
16:18 &lt;+postman&gt; ya
16:18 &lt;jrandom&gt; the network has been growing in number and in usage, but things have been doing pretty well
16:18 &lt;+postman&gt; .. apart from the irc servers
16:18 &lt;jrandom&gt; aye, thats an interesting one
16:19 &lt;jrandom&gt; (the irc servers are currently running an older rev, and we're still working on some debugging to understand exactly why things are the way they are)
16:19 &lt;+Ragnarok&gt; what happened?
16:20 &lt;jrandom&gt; hopefully we'll get the irc servers upgraded sooner rather than later, as there has been some good stuff lately
16:20 &lt;cervantes&gt; Ragnarok: server&lt;-&gt;server link is shakey under 1.1
16:20 &lt;+Ragnarok&gt; weird
16:20 &lt;jrandom&gt; 0.6.1.1, that is ;)
16:20 &lt;+Complication&gt; protokol: see forum, he finally opted for a sensible approach
16:20 &lt;+postman&gt; cervantes: don't mention the time travel, idiot
16:20 &lt;cervantes&gt; 0.6.1.x
16:20 &lt;+postman&gt; :)
16:21 &lt;cervantes&gt; oop
16:21 &lt;+postman&gt; jrandom: i hope i'll be able to build a test ircd this week
16:21 &lt;+postman&gt; jrandom: we could link to an instance run by you or cervantes 
16:22 &lt;jrandom&gt; aye, that'd be great.  we could even split off the different tunnels into different jvms, using different streaming libs and router versions, to isolate the issue further
16:23 &lt;jrandom&gt; it'd be cool if we could do that before 0.6.1.2, but if not, no big deal
16:24 &lt;jrandom&gt; ok, anyone else have anything for 1) 0.6.1.1?
16:24 &lt;+postman&gt; jrandom: apart from that: runs like hell
16:24 &lt;jrandom&gt; would that be a good hell or a bad hell?  :)
16:24 &lt;+postman&gt; a hell of a hell :)
16:25 &lt;+Complication&gt; Eh, managed to cause a few more errors (but those were really, really borderline stuff, router restart under a running i2phex.) Will send privately.
16:26 &lt;jrandom&gt; ah cool, thanks Complication 
16:26 &lt;+Complication&gt; (e.g. they probably won't hurt anyone in real life)
16:26 &lt;jrandom&gt; heh never underestimate people's ability to break things :)
16:27 &lt;cervantes&gt; or the ingenuity of fools in testing fool proof systems
16:27 &lt;+postman&gt; yea, make something fool proof and you'll be rewarded with a new kind of fool
16:28 &lt;jrandom&gt; hallelujah
16:29 &lt;jrandom&gt; ok, anything else for 1), or shall we move on to 2) i2phex
16:30 &lt;jrandom&gt; there has been a lot of discussion as of late, and legion has agreed to merge back the changes made into sirup's i2phex codebase.  
16:30 &lt;+postman&gt; move
16:30 &lt;jrandom&gt; this is quite cool, as it'll be great for us all to benefit from legion's hard work while remaining entirely open and secure
16:31 &lt;+Ragnarok&gt; what did he actually do?
16:33 &lt;jrandom&gt; latest changes include the addition of systray4j, striker's timeout updates, increased tunnel length defaults, some nsis and jni stuff, and a few other changes
16:33 &lt;+Ragnarok&gt; hm, ok
16:33 &lt;+postman&gt; jrandom: so there're a bunch of improvements - those will be kept tho?
16:34 &lt;jrandom&gt; certainly, all good stuff will be integrated into i2phex
16:34 &lt;jrandom&gt; there are a few things i'm not so sure of, but that'll be discussed with legion outside of the meeting ;)
16:35 &lt;+postman&gt; k
16:36 &lt;jrandom&gt; ok, anyone else have anything for 2) i2phex?  or shall we move on to 3) syndie?
16:37  * postman prepares his syndie500 franchising goods
16:37 &lt;jrandom&gt; heh
16:37 &lt;jrandom&gt; ok, Ragnarok, wanna give us the rundown on the latest?
16:37 &lt;+Ragnarok&gt; hm, ok
16:38 &lt;+Ragnarok&gt; Syndie will now get new posts from an archive automatically.  
16:38 &lt;+Ragnarok&gt; you can set which archives you want to get updates from, and set how often you do it in the syndie config file
16:39 &lt;+Ragnarok&gt; more details about that are in history.txt
16:39 &lt;+Ragnarok&gt; it needs a ui, but otherwise it's essentially done
16:39 &lt;+Ragnarok&gt; 'course, no one seems to be posting anything recently, so maybe it's not that useful :)
16:40 &lt;jrandom&gt; [insert field of dreams quote here]
16:40 &lt;jrandom&gt; thanks Ragnarok, this has been an oft requested feature
16:41 &lt;+Ragnarok&gt; cool
16:41 &lt;+Ragnarok&gt; happy to do it, wasn't really that much work
16:42 &lt;+Ragnarok&gt; mostly just scratching my own itch :)
16:42 &lt;cervantes&gt; oh wasn't it? or forget it then :P
16:42 &lt;cervantes&gt; or=oh
16:42 &lt;+postman&gt; (hush, the genius must not admit that it needs to work hard too)
16:42 &lt;+Ragnarok&gt; hehe
16:43 &lt;+Ragnarok&gt; anyway, if anyone's got bug reports/feature requests/boos/cheers/etc. let me know
16:43 &lt;jrandom&gt; (cheers!)
16:43 &lt;+Ragnarok&gt; next thing I'm thinking of is auto matically importing petnames seen in posts into the routers petname db, but that looks like it could be complicated...
16:44 &lt;+Ragnarok&gt; but, it would essentially allow syndie to replace addressbook
16:44 &lt;jrandom&gt; that would be Very Cool
16:44 &lt;+nickless_head&gt; yeah :)
16:45 &lt;+Ragnarok&gt; I just have to figure out how to get a list of petnames out of the archive
16:45 &lt;+Ragnarok&gt; everything else is trivial
16:45 &lt;+nickless_head&gt; ragnarok: are your  changes already in cvs? (too lazy to read the whole discussion) :)
16:45 &lt;+Ragnarok&gt; yeah
16:45 &lt;+nickless_head&gt; :happy:
16:45  * nickless_head considers cvs update
16:45 &lt;+Ragnarok&gt; have been since yesterday
16:45 &lt;+nickless_head&gt; nah, probably better to wait for the next release
16:45 &lt;jrandom&gt; perhaps get the petnames whenever they're rendered, exposed via the HTMLRenderer (in the addressReceived)
16:46 &lt;+Ragnarok&gt; ok, I'll look into that
16:46 &lt;jrandom&gt; cool, thanks Ragnarok 
16:47 &lt;+Ragnarok&gt; well, that's it from me, unless there's questions
16:49 &lt;jrandom&gt; wr0d.  ok, jumping on to 4) ??? 
16:49 &lt;jrandom&gt; anyone have anything else to bring up for the meeting?
16:49 &lt;cervantes&gt; aye
16:49  * nickless_head looks at cervantes interestedly
16:50 &lt;+fox&gt; &lt;mancom&gt; is there anything new on Q or feedspace?
16:50 &lt;+postman&gt; nickless_head: hey, he's mine - don't dare to stare at him like that :)
16:50 &lt;+nickless_head&gt; I'm not staring at him .. I'm looking at him interestedly.
16:51 &lt;cervantes&gt; After some deliberation I've revived the "Forum User of the Month" spot - and this month it deservedly has gone to Complication for outstanding forum contributions
16:51 &lt;+nickless_head&gt; congratulations complication!
16:51 &lt;+postman&gt; kudos :)
16:51 &lt;cervantes&gt; so he gets an avatar (whether he likes it or not) :P
16:51 &lt;+Complication&gt; Heh, I hope my blunders have been less outstanding. :O :D
16:52 &lt;@protokol&gt; oh yeah
16:52 &lt;jrandom&gt; w00t!  thanks Complication 
16:52 &lt;cervantes&gt; (which is active now)
16:52 &lt;@protokol&gt; hows that Yellow Submarine i2phex test going
16:52 &lt;@protokol&gt; any notable speeds or lack thereof?
16:52 &lt;+Complication&gt; It's going.
16:52 &lt;jrandom&gt; mancom: nothing new regarding Q or feedspace
16:53 &lt;+Complication&gt; No hyperfast speeds, but a guaranteed good-enough speed, I'd say.
16:53 &lt;jrandom&gt; protokol: last i heard was 10-20KBps, but thats just stuff on the forum
16:53 &lt;@protokol&gt; im downloading it right now
16:53  * nickless_head understands what postman implied
16:53  * nickless_head blushes
16:53 &lt;+Complication&gt; (also: I re-read part of the tech intro, and couldn't find flaw with the network comparisons. I think they're good enough.)
16:54 &lt;+postman&gt; nickless_head: LOL (sorry)
16:54  * Complication looks at the avatar and grins :D
16:54 &lt;+nickless_head&gt; postman: *GG* (no problem)
16:54 &lt;cat-a-puss&gt; Has anything been done in an effort to get "Amazon honor system" as an alternate method of collecting donations?
16:54 &lt;+Complication&gt; Spot on. :P
16:55 &lt;@protokol&gt; cat-a-puss: what do you mean?
16:55 &lt;jrandom&gt; not yet cat-a-puss, haven't seen wilde around
16:55 &lt;jrandom&gt; woah, hey phedy
16:55 &lt;phedy&gt; Hi jrandom.
16:55 &lt;cat-a-puss&gt; protokol: it's like pay-pal, except you can use an account you have with amazon.com to make payment
16:56 &lt;jrandom&gt; Complication: thanks re: the comparisons.  there are a few cleanups left, but its coming along
16:56 &lt;@protokol&gt; weak
16:56 &lt;+Complication&gt; (not that I know Tor or Freenet in decent degree, although I've used both)
16:57  * cat-a-puss is thinking of creating a bounty for helping finish the distributed search engine. 
16:57 &lt;jrandom&gt; (before putting the doc out on the normal website i'll run it by those folks for comment)
16:58 &lt;cervantes&gt; Complication: it's an art installation on a roundabout in London that causes havoc with the traffic ;-)
16:59 &lt;jrandom&gt; cat-a-puss: i've got to work out some other financial stuff soon anyway, so shall let you know asap
16:59 &lt;jrandom&gt; ok, anyone else have anything to bring up for the meeting?
16:59 &lt;cat-a-puss&gt; oh if we want documents translated to some other languages before 1.0, I may know people who could help with Spanish and Chinese.
16:59 &lt;cat-a-puss&gt; ok
16:59 &lt;jrandom&gt; kickass, that'd be great
17:00 &lt;+Complication&gt; cervantes: thanks for telling, I wasn't aware where such an, umm... effect occurred :D
17:00 &lt;jrandom&gt; there's a draft tech intro floating around in cvs, and we'll eventually want whatever our website redesign turns out to contain to be translated
17:03  * nickless_head goes to sleep
17:03 &lt;jrandom&gt; i suppose i should grab the baffer...
17:03 &lt;jrandom&gt; if there's nothing else
17:03  * jrandom winds up 
17:03  * jrandom *baf*s the meeting closed
</div>
