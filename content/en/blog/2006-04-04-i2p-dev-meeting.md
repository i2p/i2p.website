---
title: "I2P Dev Meeting - April 04, 2006"
date: 2006-04-04
author: "jrandom"
description: "I2P development meeting log for April 04, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> BrianR\___, cervantes, Complication, frosk, jrandom, tethra</p>

## Meeting Log

<div class="irc-log">
16:21 &lt;jrandom&gt; 0) hi
16:21 &lt;jrandom&gt; 1) Net status and 0.6.1.14
16:21 &lt;jrandom&gt; 2) Syndie plotting
16:21 &lt;jrandom&gt; 3) Local jbigi optimizations
16:21 &lt;jrandom&gt; 4) ???
16:21 &lt;jrandom&gt; 0) hi
16:21  * jrandom waves
16:21 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-April/001275.html
16:21  * Complication reads
16:22 &lt;jrandom&gt; while y'all read that (briefly put together) post, lets jump on in to 1) Net status
16:23 &lt;@cervantes&gt; (forum back)
16:23 &lt;jrandom&gt; there are a few problems out there affecting use on 0.6.1.13, and most of tem have been tracked down and solved
16:24 &lt;Complication&gt; Over here, with the "fourth" CVS build, I noticed a change in my graphs
16:24 &lt;jrandom&gt; here are still a few kinks getting tested and revamped though, but a release should be out in the next few days
16:24 &lt;Complication&gt; In general, things moved towards more stability and less jumpyness
16:24 &lt;jrandom&gt; oh bugger, I forgot to increment it to -4 didn't I?
16:24 &lt;jrandom&gt; (ok, -5 will be out later this evening)
16:24 &lt;jrandom&gt; cool Complication 
16:25 &lt;Complication&gt; But my perceptions could be influenced by jbigi too, as I didn't take steps to exclude that
16:25 &lt;Complication&gt; Now, after a while, retransmission has edged down to 15% too
16:28 &lt;jrandom&gt; hmm, i'm also seeing my average ssu rto approach the 3s ceiling as well
16:28 &lt;jrandom&gt; (though very low retransmission still, under 5%)
16:29  * Complication takes a second look at it
16:29 &lt;Complication&gt; Let's say the raw average is a little over 1500
16:29 &lt;Complication&gt; (over here)
16:30 &lt;+fox&gt; &lt;BrianR___&gt; jrandom: Is there a de-facto "MTU" for i2p packets?
16:30 &lt;jrandom&gt; ah ok, perhapsas that inches up, the retransmission rate will go down
16:30 &lt;Complication&gt; I noticed mine start out with smaller MTUs, now it's upped some to 1350
16:30 &lt;jrandom&gt; BrianR___: yes, either 1350 or 608 (as shown on http://localhost:7657/peers.js)
16:31 &lt;jrandom&gt; if the failure rate is too high at the larger MTU, it falls back to the smaller MTU (and if its too low at the smaller MTU, it jumps up to the higher MTU)
16:31 &lt;+fox&gt; &lt;BrianR___&gt; jrandom: Now is that for the inside payload or the visible IP packets?
16:31 &lt;+fox&gt; &lt;BrianR___&gt; Ie, if I were to send a block of data over an I2P stream, what would be the ideal size for the chunks to minimize overhead?
16:31 &lt;jrandom&gt; that is for the UDP payload
16:32 &lt;jrandom&gt; streams are two layers up
16:32 &lt;jrandom&gt; (there's fragmentation for tunnels, and then fragmentation at the stream/i2cp level)
16:32 &lt;+fox&gt; &lt;BrianR___&gt; Yes... Is there an ideal size to minimize fragmentation?
16:32 &lt;jrandom&gt; the ideal block size of an app using the streaming lib is "large", so that the streaming lib can use the appropriate size.
16:33 &lt;jrandom&gt; (aka ignore the man behind the curtain)
16:33 &lt;+fox&gt; &lt;BrianR___&gt; Aah.. Maybe I should think about pipelining or something then..
16:34 &lt;+fox&gt; &lt;BrianR___&gt; I'm planning an app with lots of request/response traffic...
16:34 &lt;jrandom&gt; i'd recommend batching then to cut down on the chattyness
16:34 &lt;Complication&gt; Perhaps keeping traffic focused would help to some extent
16:37 &lt;jrandom&gt; ok, anyhing else on 1) Net status, or shall e shimmy on over to 2) Syndie plotting
16:38  * jrandom shimmies
16:39 &lt;jrandom&gt; this is largely a placeholder and cfp - there's going to be some substantial revamp to syndie, both in operaion and the ui, so if you've got some key features or use cases you think need to be addressed, get in touch
16:40 &lt;jrandom&gt; (more info will be of course forthcoming as things get fleshed out further)
16:42 &lt;jrandom&gt; thats all i've got to say on that for the moment, so, moving on over to 3) jbigi optimizations
16:42 &lt;@frosk&gt; and i had assumed "plotting" referred to some jrobin stuff in syndie :)
16:43 &lt;jrandom&gt; hehe
16:43 &lt;jrandom&gt; it'd be interesting to plot posts/day, posts/author, new authors/day, etc ;)
16:44 &lt;Complication&gt; Oh, on bit about Syndie (sorry, only now remembered)
16:44 &lt;Complication&gt; =one bit
16:44 &lt;@frosk&gt; which do you want, 0 or 1? :)
16:44 &lt;Complication&gt; Do you think it could be practical, or easy/difficult to separate favourite authors and blacklisted (spam)authors into two different lists?
16:45 &lt;Complication&gt; On addresses.jsp
16:45 &lt;jrandom&gt; oh, yeah without much trouble
16:46 &lt;jrandom&gt; thats a good idea for therevamp too, but perhaps we can get that into the 0.6.1.14 build
16:47 &lt;Complication&gt; Nah, it's not byting me, I just remembered something I noticed back then
16:47 &lt;Complication&gt; Anyway, jbigi gets faster on Linux/AMD64 when you compile locally and use GMP 4.2
16:48 &lt;jrandom&gt; cool
16:48 &lt;jrandom&gt; did you compare that w/ -O3 -m64 on GMP 4.1.2?
16:48 &lt;Complication&gt; And I'm a damn fool for going after way wrong compile flags :O
16:48 &lt;@cervantes&gt; the relevant link was http://forum.i2p/viewtopic.php?t=1523&start=30 btw
16:48 &lt;jrandom&gt; ah thanks cervantes 
16:48 &lt;Complication&gt; jrandom: I haven't compared yet, but will
16:49 &lt;Complication&gt; During next scheduled reboot
16:50 &lt;jrandom&gt; the jbigi build process is essentially "build GMP, then build jbigi.o, and link the two together", so any sort of optimizations people want to make on GMP can be made as the first step
16:50 &lt;@cervantes&gt; I've not seen much difference between -O3 and -O2 in any previous tests I've done, whether that's different under x86_64 ... *shrug*
16:50 &lt;jrandom&gt; aye, might be compiler rev dependent as well
16:50 &lt;jrandom&gt; (especially with all these 3.3/3.4/4.0/4.1 issues)
16:51 &lt;@cervantes&gt; just to re-iterate what I mentioned in that thread... we probably won't see windows64 optimised jbigi anytime soon
16:51 &lt;+fox&gt; &lt;BrianR___&gt; Does the i2p stream lib do payload compression?
16:52 &lt;Complication&gt; BrianR: yes
16:52 &lt;@cervantes&gt; unless someone has M$ VC 2005 w/64-bit SDK and fancies some heavy toil to get it to compile gmp
16:52 &lt;Complication&gt; At least to my knowledge
16:53 &lt;@cervantes&gt; (there was a project to port gmp into a vc project somewhere though)
16:53 &lt;jrandom&gt; cervantes: well, we've got one that /works/ for amd64/win, but it doesn't use the most out of the hardware ;)
16:53 &lt;jrandom&gt; (when my new box gets here though i may be able to tweak that, as its an amd64)
16:53 &lt;+fox&gt; &lt;BrianR___&gt; trying to figure if I should use a binary protocol to save bits or if zlib or something is going to smoosh up ascii protocol nice and small..
16:54 &lt;@cervantes&gt; coolio - unfortunately Mingw64 or cygwin64 doesn't seem to be on the near horizon...
16:54 &lt;jrandom&gt; BrianR___: premature optimization being the root of all evil, and all that jazz...
16:55 &lt;Complication&gt; at least partly human readable protocols are generally easier to debug, but I guess it depends what one's doing
16:56 &lt;Complication&gt; ('cause some things like encryption don't like being human-readable, no matter what :) )
16:57 &lt;Complication&gt; But if I2P does the encryption, and also compresses, good chances are that many things which occur on top of it, can be done with human-readable protos
16:58 &lt;jrandom&gt; aye
16:58 &lt;jrandom&gt; ok, anything else on 3) jbigi stuff?
16:58 &lt;jrandom&gt; if not, lets move to 4) ??? 
16:59 &lt;jrandom&gt; anyone have anything else for the meeting?
17:01 &lt;+tethra&gt; i recall hearing something about anonymous collaboration tools recently
17:01 &lt;+tethra&gt; care to elaborate on what kind, and whether they'll be syndie-esque or not?
17:02 &lt;@cervantes&gt; irc and syndie is an anonymous collaboration tool :)
17:02 &lt;jrandom&gt; hmm, not sure of what you refer to - or maybe you mean the actual planned syndie revamps?  :)
17:02 &lt;+tethra&gt; true.
17:02  * tethra isn't sure either, which is why he asked
17:02 &lt;+tethra&gt; there was talk of it on the forums - reasons for anonymity and stuff
17:03 &lt;+tethra&gt; i'll find the thread so i can get the quote
17:03 &lt;jrandom&gt; ah right
17:03 &lt;+tethra&gt; http://forum.i2p.net/viewtopic.php?t=1618
17:03 &lt;jrandom&gt; the use case thread
17:03 &lt;+tethra&gt;  - anonymously hosted & publicly reachable forums/boards/wikis 
17:03 &lt;+tethra&gt; yeah
17:04 &lt;+tethra&gt; is there going to be an i2wiki type project that is based around something like syndie or is it up to users?
17:04 &lt;jrandom&gt; there have been some good ideas in there, and some good feedback
17:05 &lt;jrandom&gt; the ability to edit syndie posts is an oft-requested feature, and with that, you could pull off a wiki w/ a rich editor
17:05 &lt;jrandom&gt; but, of course, nothing will exist in a vaccum - if someone believes that is necessary, someone should say "hey, a wiki is essential, and here's why"
17:06 &lt;jrandom&gt; there are an infinite number of apps that /can/ be built, but as we're aiming for strong anonymity and strong security, care must be taken in what is built
17:07 &lt;+tethra&gt; right
17:07 &lt;+tethra&gt; that said, some of the more difficult things to keep anonymous and secure might be better off being done by someone who is good at keeping things anonymous and secure, right?
17:08 &lt;jrandom&gt; likely so, though there is no cabal - anyone can learn
17:08 &lt;+tethra&gt; (key things, basically. not that i'm naming any, but hey.)
17:08 &lt;+tethra&gt; true
17:09 &lt;+tethra&gt; but learning at the cost of your own and other people's anonymity isn't the greatest way of doing it
17:10 &lt;jrandom&gt; everyone has to start somewhere, of course
17:10 &lt;+tethra&gt; (perhaps if someone made a sandbox type thing that allowed people to run $software and have people attack it and stuff that'd be good for someone who is new/inexperienced?)
17:10 &lt;+tethra&gt; yeah
17:14 &lt;jrandom&gt; ok, anyone else have anything for the meeting?
17:15 &lt;jrandom&gt; if not
17:15  * jrandom winds up
17:15 &lt;@cervantes&gt; *ahem*
17:15  * jrandom pauses
17:16 &lt;jrandom&gt; whats shakin' cerv? 
17:16 &lt;Complication&gt; Neat, I found a baf ;P
17:17 &lt;jrandom&gt; baf-blocked ;)
17:17 &lt;@cervantes&gt; hups srry, continue baffing
17:17  * jrandom resumes winding
17:18  * jrandom *baf*s the meeting closed
</div>
