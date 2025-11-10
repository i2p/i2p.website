---
title: "I2P Dev Meeting - November 29, 2005"
date: 2005-11-29
author: "jrandom"
description: "I2P development meeting log for November 29, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, c3rvantes, cat-a-puss, cervantes, Complication, jrandom, legion, Pseudonym</p>

## Meeting Log

<div class="irc-log">
15:25 &lt;jrandom&gt; 0) hi
15:25 &lt;jrandom&gt; 1) Net status and 0.6.1.6
15:25 &lt;jrandom&gt; 2) Syndie
15:25 &lt;jrandom&gt; 3) I2P Rufus 0.0.4
15:25 &lt;jrandom&gt; 4) ???
15:25 &lt;jrandom&gt; 0) hi
15:25  * jrandom waves
15:25 &lt;jrandom&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2005-November/001234.html
15:26  * bar hands jrandom a baf
15:26 &lt;c3rvantes&gt; not yet!
15:26  * jrandom winds up
15:26 &lt;jrandom&gt; er...
15:26 &lt;jrandom&gt; lets hit the first few agenda items first :)  1) Net status and 0.6.1.6
15:27 &lt;jrandom&gt; lots of things have been updated in the last few releases, but the network still seems reasonably stable.  
15:28 &lt;jrandom&gt; we've had some serious spikes in router participation on a few routers, though thats pretty harmless
15:28 &lt;+legion&gt; cool, I agree net status is getting better. Also yeah why not drop tcp for 0.6.1.7
15:28 &lt;jrandom&gt; (er, spikes in tunnel participation, that is)
15:29 &lt;@cervantes&gt; you're not kidding
15:29 &lt;jrandom&gt; not sure legion.  there may be some users out there limited to tcp only, but i seem to recall that there was only one or maybe two of those
15:29 &lt;+legion&gt; well I've noticed with 0.6.1.5 the router would sometimes restart on its own.
15:29 &lt;+Complication&gt; Mine's been swinging withint reasonable limits, 100 to 250 participating tunnels
15:29 &lt;jrandom&gt; I can't think of any great reason to keep it, and I can think of a few to drop it
15:30 &lt;jrandom&gt; cool Complication
15:30 &lt;jrandom&gt; (those numbers are fairly average, according to stats.i2p/, but remember, numbers like that can damage anonymity, so shouldn't really be given out, especially not in logged meetings ;)
15:30 &lt;+Complication&gt; My old Celeron is still auto-restarting every 10 hours or so
15:30 &lt;+Complication&gt; Otherwise it's better connected than ever before
15:30 &lt;Pseudonym&gt; what are the reasons to drop it?
15:31 &lt;+Complication&gt; TCP is expensive
15:31 &lt;@cervantes&gt; my router is shagged out
15:31 &lt;+Complication&gt; In terms of threads per connections
15:31 &lt;@cervantes&gt; Complication: multiply that by 10 and you get my router's current range ;-)
15:31 &lt;+legion&gt; Mines been swinging within 200-400 participating tunnels, so it seems better than ever.
15:32 &lt;+Complication&gt; cervantes: ouchie ouchie
15:32 &lt;+Complication&gt; I've seen a freak accident which caused 2000 participating tunnels, but that was in Summer
15:32 &lt;jrandom&gt; Pseudonym: performance (cpu/memory, better scheduling due to our semireliable requirements), maintainability, more effective shitlisting
15:32 &lt;+Complication&gt; A single spike which never repeated again
15:32 &lt;+legion&gt; yeah, with some past versions there were such spikes
15:32 &lt;jrandom&gt; Complication: we've had&gt; 2000 tunnel spikes with this last rev
15:33 &lt;jrandom&gt; but hopefully 0.6.1.7 will take care of that
15:33 &lt;+legion&gt; Well those are some good reasons to drop tcp :)
15:33 &lt;jrandom&gt; but, again, the spikes in tunnel participation is fine, as most of them aren't used
15:34 &lt;@cervantes&gt; Pseudonym: there only seems to be one or two routers still using tcp on the network
15:34 &lt;jrandom&gt; it may also be a good idea to drop tcp in this rev too, since it doesn't have other major changes.  that way we can see how it affects things pretty clearly
15:34 &lt;jrandom&gt; (and can reenable it if necessary)
15:35 &lt;Pseudonym&gt; if there are only two routers using it, I can't imagine it would have much effect either way
15:35 &lt;Pseudonym&gt; (except for there being two less routers on the network)
15:35 &lt;@cervantes&gt; 2 disgruntled customers
15:35 &lt;jrandom&gt; well, the transport does show up in some odd situations, which is one of the reasons i want to disable it :)
15:35 &lt;+Complication&gt; I hope they won't take it very personally
15:36 &lt;+Complication&gt; It's really nasty of certain ISP's to filter UDP.
15:36 &lt;+Complication&gt; Nasty, and completely senseless.
15:36 &lt;jrandom&gt; (e.g. when a router is hosed, people mark their SSU transport as failing, and as such, they fall back on the tcp transport)
15:36  * Pseudonym loves his ISP.  no restrictions
15:37 &lt;+Complication&gt; So without TCP, one would see how UDP handles it alone?
15:37 &lt;+Complication&gt; "with no auxiliary wheels" :P
15:37 &lt;+legion&gt; huh so how do we get around such nasty filtering without tcp?
15:38 &lt;jrandom&gt; exactly Complication :)
15:38 &lt;jrandom&gt; legion: we don't
15:38 &lt;jrandom&gt; (restricted routes)
15:38 &lt;+Complication&gt; Well, aren't there a number of useful apps besides file-sharing programs, which also use UDP packets sized above DNS packets?
15:39 &lt;+legion&gt; :( doesn't sound good
15:39 &lt;+Complication&gt; Sized similarly to the smallest packet size I2P uses?
15:39 &lt;jrandom&gt; eh legion, its not a problem
15:39 &lt;jrandom&gt; Complication: streaming protocols
15:39 &lt;+Complication&gt; One cannot block UDP directly, ever, without crippling DNS.
15:39 &lt;+Complication&gt; One can limit the packet size.
15:40 &lt;+legion&gt; ok, it did sound like it could be
15:40 &lt;+Complication&gt; VoIP?
15:40 &lt;jrandom&gt; it'd be a problem if it were widespread - if the internet community in general banned udp
15:40 &lt;+Complication&gt; Hmm, does VoIP use big or small packets?
15:40 &lt;jrandom&gt; but if its just a few isps, we can treat them like restricted routes
15:40 &lt;+Complication&gt; Or did you mean more like... video spreaming?
15:40 &lt;+legion&gt; I'd think it'd use a mix of both
15:41 &lt;jrandom&gt; both Complication, RTSP runs over UDP, and real runs over RTSP iirc
15:41 &lt;+Complication&gt; s/p/s
15:42 &lt;+legion&gt; So on to the next item?
15:42 &lt;+Complication&gt; cat /etc/services | grep -c udp
15:42 &lt;+Complication&gt; 227
15:43 &lt;jrandom&gt; I'm still not sure if we'll drop tcp in 0.6.1.7, but probably.  
15:43 &lt;jrandom&gt; aye, anyone have anything else on 1)?  if not, lets jump on to 2) Syndie
15:43 &lt;+Complication&gt; Meaning, there are at least 227 apps (some possibly obsolete or LAN apps) which use UDP
15:44 &lt;jrandom&gt; bah, this is the intarweb.  all you need is proxied HTTP access
15:44 &lt;jrandom&gt; I don't have much to add to 2) beyond whats in the mail (and whats on Syndie)
15:44 &lt;+legion&gt; I'm convinced, yeah drop it. :)
15:44 &lt;jrandom&gt; anyone have anything re: syndie they want to bring up?
15:45 &lt;+legion&gt; I've nothing to say about 2) either.
15:45  * Complication is reading "how Syndie works"
15:46 &lt;+Complication&gt; One little UI effect, keeps surprising me. :D
15:46 &lt;+Complication&gt; When I expand a thread of messages, it always gets me by surprise that the active message moves to become the topmost in the list. :P
15:47 &lt;+Complication&gt; But you can proabably safely ignore that. I'm just very picky, and a creature of habit. :P
15:47 &lt;@cervantes&gt; the threading model is something that's being discussed at length
15:47 &lt;@cervantes&gt; ;-)
15:47 &lt;+Complication&gt; I'll get used to it. :)
15:48 &lt;+Complication&gt; cervantes: in Syndie? I gotta find that thread. :)
15:48 &lt;@cervantes&gt; I don't like that either - but it could well change
15:48 &lt;jrandom&gt; yeah, thats kind of kooky I suppose
15:48 &lt;+legion&gt; yeah
15:48 &lt;@cervantes&gt; "subject: syndie threading"
15:49 &lt;+Complication&gt; Besides, if the expanded message were the bottom-most, it *would* have to move anyway.
15:49 &lt;+Complication&gt; 'Cause otherwise it'd be stuck there.
15:50 &lt;jrandom&gt; well, the nav at the bottom shows 10 *threads* at a time, not 10 messages.  so it could expand the bottom thread
15:50  * cervantes is testing some different threading UI style implementations atm
15:51 &lt;jrandom&gt; wikked
15:51 &lt;jrandom&gt; yeah, ideally we'll be able to switch them around in css, or if not, on the server side
15:52 &lt;@cervantes&gt; or rather "threading navigation styles"
15:53 &lt;@cervantes&gt; hmm my tests use pure html nested unnordered lists by default
15:53 &lt;@cervantes&gt; you can layer on as much css and javascript as your need or want
15:53 &lt;jrandom&gt; any eta on when we can see some mockups?
15:53 &lt;@cervantes&gt; (however it's only a proof of concept, not an actual ui implementation)
15:54 &lt;@cervantes&gt; I do most of my coding during I2P meetings ;-)
15:54 &lt;jrandom&gt; heh
15:54 &lt;@cervantes&gt; perhaps the first mockup will be ready this evening
15:54  * jrandom schedules daily meetings
15:54 &lt;jrandom&gt; wikked
15:54 &lt;@cervantes&gt; curses :)
15:55 &lt;jrandom&gt; ok, anyone have anything else for 2) syndie?
15:55 &lt;jrandom&gt; if not, lets move on to 3) I2P Rufus 0.0.4
15:56 &lt;jrandom&gt; I don't have much to add beyond whats in the mail - Rawn/defnax, y'all around?
15:56 &lt;+legion&gt; so how good is 0.0.4? What problems remain if any?
15:57  * jrandom hasn't a clue
15:58 &lt;+legion&gt; Maybe one of its users can answer. Does it seem good and stable?
15:58 &lt;jrandom&gt; ok, seems Rawn and defnax are away atm.  if anyone has any questions/comments/concerns regarding I2P Rufus, swing on by the forum and post 'em away
15:58 &lt;+legion&gt; darn, guess we'll have to.
15:59 &lt;+legion&gt; on to 4)?
15:59 &lt;jrandom&gt; aye, so it seems.  ok, 4) ??? 
15:59 &lt;+Complication&gt; I haven't tried I2P Rufus, unfortunately.
16:00 &lt;jrandom&gt; anyone have anything else they want to bring up?
16:00 &lt;jrandom&gt; (c'mon, we've got to drag this out so cervantes can do some more work!)
16:00 &lt;+legion&gt; yeah, what sort of interesting stuff is coming down the pipe?
16:00 &lt;+bar&gt; is there anywhere i could read more about "restricted routes"?
16:00 &lt;+bar&gt; (i *have* searched)
16:01 &lt;+legion&gt; Maybe we could even discuss i2phex?
16:01 &lt;jrandom&gt; http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/techintro.html?rev=HEAD
16:01  * cervantes poises his mouse over the close button
16:01 &lt;jrandom&gt; er, #future.restricted
16:02 &lt;jrandom&gt; plus the how_* pages & todo
16:02 &lt;jrandom&gt; (on the web)
16:02 &lt;+Complication&gt; Heh, I2P seems to have skipped a build :D
16:02 &lt;+Complication&gt; :D
16:02 &lt;+bar&gt; thanks
16:02 &lt;+Complication&gt; -    public final static long BUILD = 1;
16:02 &lt;+Complication&gt; +    public final static long BUILD = 3;
16:03 &lt;jrandom&gt; legion: some hacking on the netDb, performance mods, restricted routes, streaming improvements, eepproxy improvements, tunnel improvements, etc.  lots of stuff, but nothing ready yet
16:03 &lt;+legion&gt; huh, odd
16:03 &lt;jrandom&gt; anything to bring up re: i2phex legion?
16:03 &lt;jrandom&gt; Complication: yeah, intended.  I forgot to increase it for BUILD = 2
16:03 &lt;+Complication&gt; (not that it matters for anything, just wondering if I've seen this rare occasion before :)
16:04 &lt;+legion&gt; sweet, sounds great, thanks!
16:04 &lt;jrandom&gt; oh, that reminds me... it'd be cool if someone wanted to dig into looking at revamping our webpage
16:05  * jrandom doesnt want to think about it, but its got to be done sooner or later
16:05 &lt;+legion&gt; yeah, there is
16:05 &lt;+legion&gt; would it be worthwhile to update i2phex at this point to the latest phex cvs code?
16:06 &lt;+Complication&gt; Not sure, I haven't heard from Redzara recently
16:06 &lt;jrandom&gt; last I recall, redzara was waiting on gregorz's updates to phex
16:06 &lt;jrandom&gt; (so we could have a fairly clean update/extension)
16:08 &lt;+legion&gt; huh, then why have i2phex?
16:08 &lt;+Complication&gt; Just in case?
16:08 &lt;jrandom&gt; hmm?
16:08 &lt;jrandom&gt; i2phex is an extension to phex
16:08 &lt;+legion&gt; Seems like they wanted there to just be phex with a i2p extension
16:09 &lt;jrandom&gt; extension, as in, modification to a very small number of bits
16:09 &lt;jrandom&gt; er, s/bits/components/.  so we can easily update the code whenever the phex devs fix things
16:10 &lt;+legion&gt; if so then it shouldn't take much work for me to update it to the latest cvs code, though I know it will.
16:10 &lt;jrandom&gt; last I heard in the forum was that the plan is to have I2Phex and Phex be separate applications, but they'd share a majority of code
16:10 &lt;jrandom&gt; aye legion, that'd be great, but last I heard, Gregor hadn't finished the modifications to Phex yet
16:11 &lt;jrandom&gt; (which is what redzara was waiting on)
16:11 &lt;+legion&gt; ah I see
16:11 &lt;jrandom&gt; so, the alternative is to either help Gregor out or continue modifying the existing I2Phex codebase
16:12 &lt;+legion&gt; well then if I don't wait and just update i2phex with new code, there would be no need for redzara continue
16:12 &lt;jrandom&gt; well, not really. 
16:12 &lt;jrandom&gt; updating I2Phex to the current Phex code would be great, yes
16:13 &lt;jrandom&gt; but as soon as the Phex developers update their Phex code, we're out of sync again
16:13 &lt;+legion&gt; ok, I'll probably get to it sometime tonight or within a couple days.
16:13 &lt;jrandom&gt; wikked
16:13 &lt;+legion&gt; That is fine.
16:14 &lt;+legion&gt; Really I'm not looking to have i2phex remain in sync with phex code, it's just that it sounds like the cvs contains fixes which i2phex could certainly use.
16:15 &lt;+legion&gt; Also I'm really looking to drop out any phex code and features which i2phex doesn't need.
16:15 &lt;jrandom&gt; cool
16:16 &lt;+legion&gt; As to any new features and fixing anything that is still not working like the upload queues... Well I've already looked into getting the webcaches working, but have much more to do.
16:17 &lt;jrandom&gt; word.  yeah, phex used to have working gwebcache support, but sirup disabled it, as it wasn't necessary at first
16:17 &lt;+legion&gt; I do plan on adding jeti to i2phex eventually.
16:17 &lt;jrandom&gt; neat
16:18  * jrandom has never used jeti, and I hope it stays an optional component, but supporting more things is cool
16:18 &lt;+legion&gt; Yeah it can be optionally, users will be able to download a jeti2phex ;)
16:19 &lt;jrandom&gt; word
16:19 &lt;+legion&gt; There still is much we can do with i2phex, though it is working great as it is.
16:20 &lt;+legion&gt; So far keeping a client connected, up and running for 24/7 is possible and easy.
16:21 &lt;jrandom&gt; yeah, I've had some good success with it... "backing up my licensed recordings"
16:21 &lt;+legion&gt; heh :)
16:22 &lt;jrandom&gt; ok, anyone else have anything for the meeting?
16:23  * cervantes wheels in the chinese gong
16:23 &lt;+legion&gt; Seems like I'm forgetting something... hmm
16:24 &lt;+legion&gt; Oh yeah, any ideas on how we can reduce the amount of memory i2p and i2phex consumes?
16:25 &lt;+Complication&gt; Well, the TCP transport takes a bit
16:25 &lt;jrandom&gt; one could run both in the same jvm
16:25 &lt;+Complication&gt; If that is going, it will free a bit
16:26 &lt;@cervantes&gt; take some ramsticks out of your machine
16:26 &lt;cat-a-puss&gt; anyone with any experence with javolution know if it would help? http://javolution.org/
16:26 &lt;jrandom&gt; (clients.config in the i2p install dir defines the main class and arguments to launch clients)
16:26 &lt;+legion&gt; So if we ran both in the same jvm and when tcp goes, could we bring it down to under 50mb?
16:27 &lt;jrandom&gt; no idea legion.  depends on what you mean by 50MB as well.  RSS/VSS/etc
16:27 &lt;jrandom&gt; I really wouldn't recommend running both in one JVM though, unless you keep both running all the time, since shutting down one would kill the other
16:27 &lt;@cervantes&gt; legion: limiting bandwith and capping participants might also help
16:27 &lt;jrandom&gt; aye, what cervantes said
16:28 &lt;cat-a-puss&gt; it would seem to me that if we know exactly how many of some type of object we are eventually likely to use, it would help prevent overzellous jvm allocation
16:28 &lt;+Complication&gt; Right, it makes those different allocations, which I've never really managed to make sense of
16:28 &lt;jrandom&gt; aye, we do some of that cat-a-puss (see net.i2p.util.ByteCache)
16:29 &lt;+Complication&gt; (but as said, Java is a very new thing to me)
16:29 &lt;jrandom&gt; I've glanced at javolution before, but it seems to have made a lot of progress.  i'll give 'er another look
16:30 &lt;cat-a-puss&gt; jrandom:I know some people at my work use it and are happy with it, though they don't care about memory allocation
16:31 &lt;jrandom&gt; well, it really wouldn't save any memory, but would help cut down on GC churn
16:31 &lt;+legion&gt; Well I personally don't care much about memory allocation, however many people do.
16:31 &lt;jrandom&gt; ooh, and its BSD licensed too
16:31 &lt;cat-a-puss&gt; right
16:31 &lt;jrandom&gt; legion: memory allocation means performance
16:32 &lt;+legion&gt; er, oh, memory consumption then
16:33 &lt;+legion&gt; Many people are so very happy with utorrent because of it's very small memory footprint.
16:33 &lt;jrandom&gt; ah, oh, yeah.  we can tweak it down the line, but since i2p runs within the default jvm sizes, i'm not too worried (as we've got lots of room for tweaking)
16:34 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:35 &lt;+legion&gt; nah I'm good...
16:37  * jrandom winds up
16:37  * jrandom *baf*s the meeting closed
</div>
