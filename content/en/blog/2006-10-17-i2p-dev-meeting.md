---
title: "I2P Dev Meeting - October 17, 2006"
date: 2006-10-17
author: "jrandom"
description: "I2P development meeting log for October 17, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, dm, jrandom, marlowe</p>

## Meeting Log

<div class="irc-log">
16:01 &lt;jrandom&gt; 0) hi
16:01 &lt;jrandom&gt; 1) Net status
16:01 &lt;jrandom&gt; 2) Syndie dev status
16:01 &lt;jrandom&gt; 3) ???
16:01 &lt;jrandom&gt; 0) hi
16:01  * jrandom waves
16:01 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-October/001314.html
16:02 &lt;+fox&gt; * dm waves
16:02 &lt;jrandom&gt; w3wt, ok, while y'all read that oh-so-fun missive, lets jump on to 1) net status
16:03 &lt;jrandom&gt; the net seems to be maintaining the steady state right now, though with a slight growth trend
16:04 &lt;jrandom&gt; there are some discussions on the big cpu-related issue on the forum, though no big win yet, afaics
16:04 &lt;jrandom&gt; anyone have anything to bring up re: 1) net status?
16:05 &lt;jrandom&gt; (the last full week w/ 0.6.1.26 seems to have gone well [yay])
16:06 &lt;+fox&gt; &lt;dm&gt; well, I better say something
16:06 &lt;+fox&gt; &lt;dm&gt; is there a consistent metric that is being used to monitor net status
16:06 &lt;+fox&gt; &lt;dm&gt; or is it just ad-hoc experiences?
16:07 &lt;+fox&gt; &lt;dm&gt; like is there an application out there that tries to connect to random places every day while measuring response times and failures.
16:07 &lt;jrandom&gt; i'm going largely by irc behavior, as well as the stats and activity on the routers i run (stats.i2p is down for a week or two, but it usually is a solid enchmark to run against)
16:08 &lt;+fox&gt; &lt;dm&gt; cool, I'll check that site out.
16:08 &lt;jrandom&gt; there are several people running stat monitoring apps - orion.i2p, tino.i2p, eepsites.i2p, as well as stats.i2p
16:09 &lt;+fox&gt; &lt;dm&gt; thank you!
16:09 &lt;jrandom&gt; np :)
16:09 &lt;jrandom&gt; ok, if there's nothing else on 1), lets jump on over to 2) syndie dev status
16:10 &lt;jrandom&gt; lots going on, as mentioned in the status notes (and you can finally see a non-hideous-looking website at syndie.i2p.net :)
16:11 &lt;+fox&gt; &lt;dm&gt; down at the moment?
16:11 &lt;+fox&gt; &lt;dm&gt; scratch that
16:11 &lt;+fox&gt; * dm shuts up
16:11 &lt;jrandom&gt; :)
16:12 &lt;marlowe&gt; jrandom, the diagram on the front page is very helpful
16:12 &lt;marlowe&gt; i know understand the concept behind syndie
16:12 &lt;+fox&gt; &lt;dm&gt; it's pretty as well
16:13 &lt;+fox&gt; &lt;dm&gt; but how do you access syndie without download/installing it? I remember you could do this before?
16:13 &lt;jrandom&gt; great, glad its clear marlowe - it can be a confusing concept in just text :)
16:13 &lt;jrandom&gt; dm: the old syndie (syndiemedia.i2p.net/) was web based, but this new one is, well, brand new, completely redesigned
16:14 &lt;+fox&gt; &lt;dm&gt; it's not web-based?
16:14 &lt;jrandom&gt; (and thanks to cervantes for turning my ugly ms-paint-style image into the slick pic you see there :)
16:14 &lt;jrandom&gt; no, its not web based - current release is actually text only, but work continues on a gui
16:14 &lt;jrandom&gt; http://syndie.i2p.net/roadmap.html
16:14 &lt;+fox&gt; &lt;dm&gt; text-only! wow. ok. downloading.
16:14 &lt;jrandom&gt; w3wt
16:15 &lt;jrandom&gt; one important thing you need to know to effectively use it is the location of a syndie archive that you can push posts to and pull posts from
16:15 &lt;+fox&gt; &lt;dm&gt; wow.. this is hardcore stuff. (Next Command:) hehhehe
16:15 &lt;jrandom&gt; there's currently one at http://syndie.i2p.net/archive - you can sync up with that via "menu syndicate" "getindex --archive http://syndie.i2p.net/archive" and "fetch" :)
16:16 &lt;jrandom&gt; its a fairly simple system, though with very specific design features
16:16 &lt;jrandom&gt; (and incredibly robust - it can run on anything :)
16:17 &lt;+fox&gt; &lt;dm&gt; there's something cool about really complex apps running with a text frontend
16:17 &lt;+fox&gt; &lt;dm&gt; anyway...
16:17 &lt;+fox&gt; * dm shuts up again
16:19  * jrandom hopes to bring us up to 1.0 sometime this month, so beta testing would be great
16:20 &lt;jrandom&gt; (kick the tires, tell me whats broken, etc)
16:20 &lt;jrandom&gt; 1.0 won't include the gui, of course, thats 2.0
16:20 &lt;+fox&gt; &lt;dm&gt; of course
16:21 &lt;jrandom&gt; ok, anyone have any comments/questions/suggestions/toenails on 2) Syndie dev status?
16:22 &lt;jrandom&gt; oh, one thing i wanted to bring up - as i posted in my syndie blog, we need a logo!  so, see urn:syndie:channel:d7:channel44:bF2lursCrXhSECJAEILhtXYqQ6o-TwjlEUNJLA5Nu8o=9:messageIdi1160962964161ee :)
16:23 &lt;+fox&gt; &lt;dm&gt; there's a good place to get free or semi-free very high quality logos
16:24 &lt;jrandom&gt; flickr?  :)
16:24 &lt;+fox&gt; &lt;dm&gt; http://www.worth1000.com/ &lt;--- photoshop geeks around try to outdo each other for a little fame and/or money
16:24 &lt;jrandom&gt; ah cool
16:25 &lt;+fox&gt; &lt;dm&gt; example of a previous 'contest' http://www.worth1000.com/cache/contest/contestcache.asp?contest_id=12170&start=1&end=10&display=photoshop
16:25 &lt;+fox&gt; * dm shuts up again
16:26 &lt;jrandom&gt; wikked, thanks dm
16:27 &lt;jrandom&gt; ok, if there's nothing on 2, lets jump to 3) ???
16:28 &lt;jrandom&gt; anyone have anything else for the meeting?
16:28 &lt;bar&gt; perhaps we should save that for the 1.99b version and have a little contest/bounty thing going to plug syndie 2.0?
16:28 &lt;jrandom&gt; ah, thats a good idea, since 1.* is going to be text anyway
16:30 &lt;bar&gt; think about it, i'm sure we can dig up some funding
16:30 &lt;+fox&gt; &lt;dm&gt; how's funding going anyway? 
16:31 &lt;+fox&gt; &lt;dm&gt; are you still doing this full-time jr?
16:31 &lt;jrandom&gt; aye, still getting by, thanks to some insanely generous contributors (thanks!)
16:31 &lt;jrandom&gt; http://www.i2p.net/halloffame
16:32 &lt;+fox&gt; &lt;dm&gt; ah yes.. the shoestring budget. I remember now
16:32 &lt;jrandom&gt; hehe
16:34 &lt;jrandom&gt; ok, anyone have anything else to bring up?
16:34 &lt;+fox&gt; &lt;dm&gt; just dropped you a c-bill. Make sure it's only used for alcohol or other frivolous uses.
16:34 &lt;+fox&gt; &lt;dm&gt; oh and keep my real name secret!
16:34 &lt;jrandom&gt; w00t!  thanks dm
16:36 &lt;jrandom&gt; ok, if there's nothing else...
16:36  * jrandom winds up
16:36  * jrandom *baf*s the meeting closed
</div>
