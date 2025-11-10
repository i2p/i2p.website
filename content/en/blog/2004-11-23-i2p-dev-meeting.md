---
title: "I2P Dev Meeting - November 23, 2004"
date: 2004-11-23
author: "jrandom"
description: "I2P development meeting log for November 23, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> jrandom, lba, postman, Ragnarok</p>

## Meeting Log

<div class="irc-log">
13:03 &lt;jrandom&gt; 0) hi
13:03 &lt;jrandom&gt; 1) Net status
13:03 &lt;jrandom&gt; 2) Streaming lib
13:04 &lt;jrandom&gt; 3) 0.4.2
13:04 &lt;jrandom&gt; 4) Addressbook.py 0.3.1
13:04 &lt;jrandom&gt; 5) ??? 
13:04 &lt;jrandom&gt; 0) hi
13:04  * jrandom waves
13:04 &lt;+postman&gt; hi :)
13:04 &lt;jrandom&gt; weekly status notes posted up to http://dev.i2p.net/pipermail/i2p/2004-November/000490.html
13:05 &lt;jrandom&gt; well, might as well jump on in to 1) net status
13:05 &lt;jrandom&gt; i dont have much to add to this that wasn't in the email
13:05 &lt;jrandom&gt; anyone have anything they want to bring up wrt the network status over the last week?
13:06 &lt;jrandom&gt; if not, we can jump on down to 2) streaming lib
13:06 &lt;jrandom&gt; there's lots of info in the mail about this, so i'll let y'all digest a bit
13:07 &lt;jrandom&gt; while the new lib will improve lots of things, the most important (imho) is its resiliance and handling of congestion
13:08 &lt;jrandom&gt; especially the latter, as we've seen how things get funky with the old lib under heavy congestion
13:08 &lt;jrandom&gt; there's also a lot of things left out of the lib though, places for people to experiment and optimize further
13:09 &lt;jrandom&gt; anyone have any questions wrt this, or have we been beating a dead horse by discussing it each week for the last month?  ;)
13:10 &lt;+Ragnarok&gt; we'll call that a yes
13:10 &lt;jrandom&gt; heh
13:10 &lt;jrandom&gt; ok, moving on to 3) 0.4.2
13:10 &lt;jrandom&gt; out real soon, just doing some minor updates to the install process at the moment
13:11 &lt;+postman&gt; yesss
13:11 &lt;+postman&gt; :)
13:11 &lt;jrandom&gt; the updated install proc will be a bit nicer for people, addressing the most common user errors
13:12 &lt;jrandom&gt; (since no one ever reads the text on the router console ;)
13:12 &lt;jrandom&gt; but that should be ready in the next day or two, so with some testing we should have a release out by friday
13:12 &lt;jrandom&gt; (if not sooner)
13:13 &lt;jrandom&gt; as i mentioned in the mail though, its both backwards compatbile and /not/ backwards compatible
13:13 &lt;+Ragnarok&gt; awesome
13:13 &lt;jrandom&gt; does anyone have any strong preferences as to how we should do that tap dance?
13:13 &lt;jrandom&gt; should we just push out 0.4.2 and let people upgrade when they notice they cant reach any eepsites?
13:14 &lt;jrandom&gt; (or will they uninstall it and say "dood i2p sux0rz")
13:14  * jrandom neither
13:15 &lt;+Ragnarok&gt; I'd say mark it as not compatible.  It's always better to be explicit.
13:15 &lt;jrandom&gt; well, the docs and announcement will say not compatible, mandatory upgrade in big bold letters
13:16 &lt;+Ragnarok&gt; no reason to send mixed messages, then
13:16 &lt;jrandom&gt; aye
13:16 &lt;jrandom&gt; though we would be able to tunnel route through those old peers
13:16 &lt;jrandom&gt; i dunno, we've got a few days to finalize the decision anyway
13:17 &lt;jrandom&gt; just something to think about, and a WARNING to people that they'll NEED TO UPGRADE TO 0.4.2 
13:17 &lt;jrandom&gt; :)
13:18 &lt;jrandom&gt; ok, anyone have any questions/comments/concerns wrt 0.4.2, or shall we move on to 4) addressbook.py?
13:18 &lt;jrandom&gt; consider us moved
13:18 &lt;jrandom&gt; Ragnarok: wanna give us an update?
13:20 &lt;+Ragnarok&gt; sure.  Minor update released yesterday.  Fixes some bugs on windows, and doesn't violently die if the proxy isn't there.  Only really notable thing is that this will probably be the last release for this version, barring a giant bug.
13:20 &lt;jrandom&gt; ok cool
13:21 &lt;jrandom&gt; avoiding violent death is always a nice feature to have
13:21 &lt;lba&gt; hi folks
13:21 &lt;+Ragnarok&gt; I'm planning on redesigning (just designing, really) it from the ground up based on jrandom's thoughts from the mailing list.  Possibly in java too, if I can figure out the xml parsing and http stuff I'll have to do.
13:21 &lt;jrandom&gt; wikked :)
13:21 &lt;jrandom&gt; 'lo lba
13:22 &lt;+Ragnarok&gt; well, that's all.  Carry on.
13:22 &lt;jrandom&gt; cool, thanks for the update
13:22 &lt;jrandom&gt; ok if there's nothing else on that, we can move on at a blazing pace to 5) ???
13:22 &lt;jrandom&gt; anyone else have something they want to bring up?
13:23 &lt;+Ragnarok&gt; anyone else here?
13:23 &lt;jrandom&gt; heh, yeah, we dont have our usual malcontents ;)
13:24 &lt;jrandom&gt; then again, they'll show up to read the logs on the site later [yeah, i mean *YOU*]
13:24 &lt;jrandom&gt; ok, i think thats probably the shortest meeting we've had in over a year
13:25 &lt;jrandom&gt; might as well wraper 'er up
13:25  * jrandom winds up
13:25  * jrandom *baf*s the meeting closed
</div>
