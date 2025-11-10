---
title: "I2P Dev Meeting - January 31, 2006"
date: 2006-01-31
author: "jrandom"
description: "I2P development meeting log for January 31, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, cervantes, Complication, frosk, gloin, jrandom, Pseudonym, stealth, Sugadude, tethra</p>

## Meeting Log

<div class="irc-log">
15:19 &lt;jrandom&gt;  0) hi
15:19 &lt;jrandom&gt; 1) Net status
15:19 &lt;jrandom&gt; 2) 0.6.1.10 status
15:19 &lt;jrandom&gt; 3) ???
15:19  * jrandom waves
15:19 &lt;jrandom&gt; status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-January/001257.html
15:20 &lt;jrandom&gt; ok, jumping on in to 1) Net status
15:21 &lt;jrandom&gt; as mentioned in the mail, those on 0.6.1.9-0 (the full release) should have the same-ol'-same-ol'
15:21 &lt;jrandom&gt; though users on newer builds (those since 0.6.1.9-5 or newer) may have trouble
15:21 &lt;jrandom&gt; ("trouble" is perhaps an understatement...)
15:21 &lt;+Complication&gt; CVS -8 was a bit flaky, so running -2 instad (works nice enough)
15:22 &lt;gloin&gt; :-)
15:22 &lt;+Complication&gt; =instead
15:22 &lt;Pseudonym&gt; things seem unstable lately (I'm on 0.6.1.9-0)
15:22 &lt;jrandom&gt; cool, I was considering reverting the process changes but including dust's ircclient update and the i2ptunnel httpserver patch on head, but 0.6.1.10 probably isn't that far away
15:23 &lt;jrandom&gt; hmm Pseudonym, accessing eepsites, irc, or other services, or hosting them?
15:23 &lt;+Complication&gt; Unstable with -0? How does the problem exibit itself?
15:23 &lt;Pseudonym&gt; I notice IRC primarily (playing idlerpg)
15:24 &lt;jrandom&gt; ("playing" ;)
15:24 &lt;Pseudonym&gt; also, somtimes the router goes wonky and has to be restarted (no active peers)
15:24 &lt;Pseudonym&gt; heh
15:24 &lt;jrandom&gt; hmm, internet connectivity issues?
15:24 &lt;@frosk&gt; -0 is stable here, of course except for the twice-daily "router hung!" restarts
15:24 &lt;jrandom&gt; hrm frosk, real "router hung", or "router hung" due to leaseSet expiration?
15:25 &lt;Pseudonym&gt; internet connectivity is fine.  when I restart the i2p router it comes right back
15:25 &lt;+Complication&gt; My Cel300 also hangs after a while, but the periods have been increasing, and I'm not up-to-date on its reason
15:25 &lt;@frosk&gt; jrandom: lease expiration, i'm pretty sure
15:25 &lt;jrandom&gt; hmm 'k
15:26 &lt;jrandom&gt; pretty much all of that has been rewritten for the new creation and management code, so we'll see how it goes in 0.6.1.10
15:27 &lt;@frosk&gt; cool
15:27 &lt;@frosk&gt; i'll be glad to help test it
15:28 &lt;Pseudonym&gt; I don't need you to troubleshoot the problem right now.  I just wanted to add a datapoint about stability
15:28 &lt;jrandom&gt; wikked, once its stable locally I'll certainly need to recruit some help :)
15:28 &lt;jrandom&gt; cool, thanks Pseudonym 
15:28 &lt;jrandom&gt; ok, anyone else have something for 1) Net status?
15:30 &lt;jrandom&gt; if not, lets jump on in to 2) 0.6.1.10 status
15:30 &lt;jrandom&gt; as mentioned in the mail, rather than pile tweak upon tweak on the live net, we're going to go straight to the source
15:31 &lt;jrandom&gt; it won't be backwards compatible, so it will have a... bump, and while we'll roll up a few other backwards incompatible changes with it, there is the possibility for another one afterwards
15:32 &lt;jrandom&gt; more specifically, one idea I'm toying with is migrating to 1024bit ElGamal for the tunnel creation code, rather than 2048bit
15:32 &lt;jrandom&gt; but that may not be necessary.  it depends on how hard it hits us on the live net
15:34 &lt;jrandom&gt; if it does, it would just mean a network upgrade, but all destinations/etc would stay the same.
15:34 &lt;jrandom&gt; but, anyway, thats something to explore after 0.6.1.10 comes out
15:34 &lt;+Complication&gt; A loosely related question: is the key length in any way related to the tunnel-creation datastructure length?
15:34 &lt;jrandom&gt; yes
15:35 &lt;jrandom&gt; directly related: key length * 2 * max # hops == data structure size
15:36 &lt;jrandom&gt; (so, 256*2*8 = 4KB, which also happens to be the size of full streaming lib messages)
15:37 &lt;jrandom&gt; ((ElGamal has a 2x expansion factor))
15:38 &lt;+Complication&gt; Aha, thanks. :)
15:38 &lt;jrandom&gt; ah, one other thing re: the new spec.  during implementation I found one other data point I need (a 4 byte "reply message ID") which I've added to the spec locally, using some of the reserved bits
15:40 &lt;jrandom&gt; I'm hoping to get everything working in the next few days though, so perhaps there'll be some early (non-anonymous) testing by the weekend
15:40 &lt;jrandom&gt; but, of course, more info on that as it comes
15:41 &lt;jrandom&gt; ok, anyone have any questions/comments/concerns on the 0.6.1.10 stuff?
15:41 &lt;bar&gt; another loosely related question: during the rol out of .10, how about keeping i2p.net on .9 for a couple of days for all the auto updating folks?
15:41 &lt;bar&gt; rollout*
15:41 &lt;jrandom&gt; aye, definnitely
15:42 &lt;jrandom&gt; I'll probably have two or three routers on that box during the migration
15:42 &lt;jrandom&gt; and there will be loud warnings at least 5 days in advance of the release
15:42 &lt;bar&gt; smooth
15:42 &lt;+Complication&gt; This way it would be smoother indeed.
15:43 &lt;+Complication&gt; Forum seems a good channel. News box on the Router Console too...
15:43  * jrandom remembers the days when every release was backwards incompatible... we got a lot of practice then ;)
15:43 &lt;jrandom&gt; aye, forum, news box, list, website
15:43 &lt;+Complication&gt; So those who attend their machines would know.
15:43 &lt;tethra&gt; heheh
15:44 &lt;jrandom&gt; and those on 0.6.0.1 still, well, they're fscked anyway ;)
15:44 &lt;@frosk&gt; off with their heads
15:44 &lt;+Sugadude&gt; Totally un-related: Can we have more backwards incompatible changes more often to force these old routers out?
15:44 &lt;+Complication&gt; I think they just forgot I2P running :)
15:44 &lt;jrandom&gt; heh Sugadude
15:45 &lt;jrandom&gt; well, if they're compatible, we can make use of their resources, but if there's some reason why we can't, we should mark them as incompatible
15:47 &lt;jrandom&gt; ok, if there's nothing else on that, lets jump on over to our catch-all: 3) ???
15:47 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
15:48 &lt;tethra&gt; it says somewhere on the router console that users behind symmetric NATs aren't currently supported, is that going to change at some point soon? 
15:48 &lt;tethra&gt; or am i showing immense ignorance of something
15:49 &lt;+Complication&gt; Regarding webcache code... it seems I'm pretty much ready.
15:49 &lt;jrandom&gt; there are a few techniques to help users behind symetric nats, which bar has outlined on the list and the forum, though I don't know of any immediate progress on it
15:49 &lt;jrandom&gt; oh, nice1 Complication, lemmie know when to push the release :)
15:50 &lt;+Complication&gt; Got the watchdog aborting downloads reasonably, doing some testing and clean-up (it currently logs way more than decent)..
15:50 &lt;+Complication&gt; I have one webcache server up, awup has another... for some realistic testing, we may want to turn limiting on...
15:51 &lt;+Complication&gt; ...if I manage to encounter legion, I'll ask if he might be interested in running one too.
15:52 &lt;jrandom&gt; cool, even a single webcache would be a great start
15:52 &lt;+Complication&gt; And if anyone else wants to run the script (available from awup.i2p, Python script using SAM)... their references can be added, though currently adding refs to more "seed webcaches" does require a recompile of sources.
15:53 &lt;+Complication&gt; (not in a file but the header of GWebCacheContainer.java)
15:53  * gloin don't know what this webcache stuff is.
15:53 &lt;jrandom&gt; gloin: it lets you connect to i2phex without having to download an i2phex.hosts file the first time
15:54 &lt;+Complication&gt; gloin: for easier integration of I2PHex
15:55  * cervantes arrives late
15:55 &lt;+Complication&gt; And for later reconnecters (e.g. people who've run out of live peer refs) it can offer fresh refs
15:55 &lt;gloin&gt; ok.
15:57 &lt;+Complication&gt; Oh, offline again
15:58 &lt;stealth&gt; what about an automatic startup of i2phex after i2p has started ?
15:58 &lt;+Complication&gt; Seems like overkill
15:58 &lt;+Complication&gt; At current phase, at least
15:58 &lt;jrandom&gt; stealth: you can have the i2p router launch any java application you want by adding entries into your client.config file
15:59 &lt;+Complication&gt; Besides, I think I2Phex can be started before I2P runs
15:59 &lt;@frosk&gt; at any phase
15:59 &lt;+Complication&gt; Theoretically, it should keep trying to connect until I2P gets up
15:59 &lt;+Complication&gt; (haven't tested, though)
15:59 &lt;jrandom&gt; though remember, if you tell it to launch i2phex, when i2phex closes, chances are the i2phex client will kill the JVM (restarting your router)
16:00 &lt;+Complication&gt; Besides, one could script it fairly easily too...
16:00 &lt;+Complication&gt; e.g. "cd /home/i2p; sh i2prouter start; cd /home/i2phex; sleep 100; sh run.sh;"
16:00 &lt;+Complication&gt; (or however it was)
16:01 &lt;+Complication&gt; Sorry, /home/user/i2p more likely :)
16:01 &lt;cervantes&gt; don't forget to start /usr/games/tetris before the sleep 100
16:02 &lt;jrandom&gt; damn straight
16:02 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:03 &lt;stealth&gt; well I thought  about it just start the exe. the i2psnark solution with always on is better because people forget to share their files if they are not downloading...
16:04 &lt;jrandom&gt; aye, though I've yet to hear of a gnutella client that is thin enough (that could be integrated)
16:05 &lt;cervantes&gt; isn't the work being done on the current Phex to abstract the UI? perhaps the client eventually become skinny
16:05 &lt;+Complication&gt; I haven't read that part of Phex CVS
16:06 &lt;jrandom&gt; if phex could be run as a .war, that would indeed rule
16:06 &lt;cervantes&gt; isn't the=isn't there
16:06 &lt;cervantes&gt; I'm probably mistaken
16:06 &lt;+Complication&gt; Sirup certainly was working on an XML-RPC interface, but I'm not sure if Gregor & co are too
16:07 &lt;+Complication&gt; So I'm not sure if sirup ported it in, or started writing it from scratch
16:09 &lt;jrandom&gt; iirc he was just importing apache's xmlrpc lib and exposing some of i2phex's internals, but there hasn't been any work on that in probably 6-8 months, and it was never functional afaik
16:10 &lt;fox_&gt; &lt;tethra&gt; mutella is a web based gnutella client that is fairly lightweight, iirc. not sure if it will be any help, but heh, might be worth someone (more talented) checking it out.
16:10 &lt;fox_&gt; &lt;tethra&gt; might not be what is being looked for, though.
16:12 &lt;jrandom&gt; porting a new one is a chunk of work, especially a C/C++ one, unfortunately
16:12 &lt;+Complication&gt; I'm personally unlikely to tinker with XML-RPC. Attempting to catch various bugs... is in my near-term plans, though.
16:13  * Complication wants the rehash effect gone for good, since it's such a waste of time
16:13 &lt;jrandom&gt; ooh, perhaps thats triggered by timezone shift?
16:14 &lt;jrandom&gt; when the I2P SDK connects to the router, it gets the current I2P (NTP) time from it, and forces the SDK's JVM into UTC
16:14 &lt;+Complication&gt; Sounds unlikely... but at this stage, I can't exclude much
16:15 &lt;jrandom&gt; (and if the rehash depended upon ordering and file timestamps, perhaps the shift of a few hours would change that)
16:15 &lt;jrandom&gt; yeah, you've dug into a lot of it, just mentioning a possibility
16:15  * jrandom doesn't know anything about it beyond your bug reports :)
16:16 &lt;+Complication&gt; It occurs occasionally, and *seems* related to something happening when the "sharedlibrary" config file is being loaded/rewritten
16:16 &lt;+Complication&gt; Hmm, interesting possibility...
16:16 &lt;+Complication&gt; I've not dug enough to exclude that
16:18 &lt;jrandom&gt; ok, anyone else have something for the meeting?
16:19 &lt;jrandom&gt; if not...
16:19  * jrandom winds up
16:19  * bar wishes jrandom good luck with .10 and hands him a shiny baf
16:19 &lt;jrandom&gt; gracias :)
16:19  * jrandom *baf*s the meeting closed 
</div>
