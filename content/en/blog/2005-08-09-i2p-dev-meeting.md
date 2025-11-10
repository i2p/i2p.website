---
title: "I2P Dev Meeting - August 09, 2005"
date: 2005-08-09
author: "jrandom2p"
description: "I2P development meeting log for August 09, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bla, detonate, duck, jrandom, jrandom2p, luckypunk, postman, smeghead</p>

## Meeting Log

<div class="irc-log">
13:11 &lt;jrandom2p&gt; 0) hi
13:11 &lt;jrandom2p&gt; 1) 0.6.0.2
13:11 &lt;jrandom2p&gt; 2) roadmap update
13:11 &lt;jrandom2p&gt; 3) ???
13:11 &lt;jrandom2p&gt; 0) hi
13:11  * jrandom2p waves
13:11 &lt;+detonate&gt; hi
13:11 &lt;jrandom2p&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2005-August/000839.html
13:12 &lt;jrandom2p&gt; ok, jumping in briefly to [1-2] before the freeforall..
13:12 &lt;jrandom2p&gt; 1) 0.6.0.2
13:12 &lt;jrandom2p&gt; its out.  and stuff
13:12 &lt;jrandom2p&gt; anyone have any questions/comments/concerns w/ 0.6.0.2?
13:13 &lt;jrandom2p&gt; if not, moving on to 2) roadmap update
13:13 &lt;jrandom2p&gt; the, er, roadmap has been updated.  and stuff ;)
13:14 &lt;duck&gt; you aussie
13:14 &lt;+bla&gt; jrandom: There still are intermittent problems contacting a destination, even when it's normally up
13:14  * postman can second this
13:14  * detonate can third that
13:14 &lt;+bla&gt; jrandom: E.g., forum.i2p works fine, then after a few minutes it doesn't, and requires a few reloads
13:15  * bla firsted it ;)
13:15 &lt;jrandom2p&gt; hmm, aye, i've heard reports of that.  with 0.6.0.2 as well, right?
13:16 &lt;+postman&gt; indeed sir
13:16 &lt;+bla&gt; Yes, 0.6.0.2
13:16 &lt;+bla&gt; Could be netDb trouble, or poor selection of peers to put in tunnels (or something else)
13:16 &lt;jrandom2p&gt; 'k
13:17 &lt;jrandom2p&gt; the tunnel peer selection has been pretty bad lately, as has netDb store flooding
13:17 &lt;jrandom2p&gt; (see your /oldstats.jsp for tunnel request failure counts)
13:18 &lt;+bla&gt; Now that we use UDP/SSU, peer classification seems to be better than before: a number of peers I _know_ to be fast, usually show up under the "fast" section on the profile pafe
13:19 &lt;jrandom2p&gt; nice
13:19 &lt;jrandom2p&gt; 0.6.0.2 added some tunnel rejection code based on the netDb that it should have been doing before (refusing to join if we can't find the next hop), so the increase in rejections is expected
13:19 &lt;+bla&gt; Though I really should get going at the classification algorithms again... ;)
13:20 &lt;jrandom2p&gt; i've been doing profile/stat analysis, but no solid results yet
13:21 &lt;jrandom&gt; that would be cool bla :)
13:25 &lt;jrandom2p&gt; ok, anything else on 2) roadmpa update?  :)
13:26 &lt;jrandom2p&gt; if not, moving on to 3) ???
13:26 &lt;+detonate&gt; do you think it would be useful to shitlist peers with high failure/duprecv rates compared to the mode?
13:27 &lt;jrandom&gt; hmm, i'm not sure about that - if the failure/dup rates are too high to be useful, we should just transfer slowly and carefully
13:27 &lt;jrandom&gt; as long as messages are getting through, messages are getting through
13:28 &lt;jrandom&gt; there's a reason why we haven't used stats on direct peer communication as part of our profiling - depending upon them would make us vulnerable to some easy and powerful attacks (acting differently to different peers and see who uses you, etc)
13:29 &lt;+detonate&gt; hmm
13:29 &lt;+detonate&gt; ok
13:29 &lt;jrandom&gt; but perhaps we need to drop sessions for peers who are in such congested cons
13:29 &lt;+detonate&gt; good point
13:34 &lt;jrandom&gt; ok, anyone else have something to bring up for 3) ???
13:34 &lt;luckypunk&gt; o,oh, maybe you should wait ti leveryone is back
13:34 &lt;luckypunk&gt; before asking critical questions :P
13:35 &lt;jrandom2p&gt; bah, they've got the mailing list ;)
13:35 &lt;luckypunk&gt; well
13:35 &lt;luckypunk&gt; i guess this is the right place to whine
13:36 &lt;luckypunk&gt; I2P still uses a bit of CPU
13:36 &lt;luckypunk&gt; but not as much as before
13:36 &lt;luckypunk&gt; true, i haven't run it since the 5.0 days
13:36 &lt;luckypunk&gt; but yeah
13:36 &lt;luckypunk&gt; er
13:36 &lt;luckypunk&gt; 0.5.0
13:36 &lt;jrandom2p&gt; cool, which of your boxes works with it?
13:36 &lt;luckypunk&gt; er
13:36 &lt;luckypunk&gt; ffs
13:36 &lt;luckypunk&gt; i haven't used it since 0.6.0.0
13:36 &lt;luckypunk&gt; it works fine with the pentium 2
13:37 &lt;luckypunk&gt; the default nice value mens it tends to crashif i do anything too CPU intensive for too long as I2P gets CPU starved
13:38 &lt;+detonate&gt; hmm, i guess there could be a space in the router console network config to hardwire the introducers, once there are introducers, if the user prefers
13:39 &lt;jrandom2p&gt; are you on 0.6.0.2 now luckypunk?
13:39 &lt;@smeghead&gt; detonate: that's trusted route stuff... later on in the roadmap :)
13:39 &lt;luckypunk&gt; no
13:39 &lt;luckypunk&gt; i haven't run it since 0.6.0.0
13:39 &lt;@smeghead&gt; *restricted route
13:40 &lt;luckypunk&gt; but it's CPU use seemed much less.
13:40 &lt;+detonate&gt; heh, it should be there as soon as there's introducers :)
13:40 &lt;jrandom2p&gt; ah yeah detonate, the introducer selection could certainly be configurable, but it'll probably be a hidden advanced config option ;)
13:41 &lt;jrandom2p&gt; luckypunk: 0.6.0.1 cut out a lot of crypto, and 0.6.0.2 should help further.  give it a try sometime, it may handle it better
13:41 &lt;luckypunk&gt; ok
13:41 &lt;@smeghead&gt; what if an introducer doesn't want you selecting them all the time?
13:41 &lt;luckypunk&gt; i have the feeling I2P would on a dedicated mid range pentium now.
13:41 &lt;jrandom&gt; smeghead: then they say "fuck off, i'm not going to serve as an introducer for you"
13:42 &lt;jrandom&gt; and peers will have multiple introducers, so it'll be balanced
13:42 &lt;jrandom&gt; (and its only 2 packets to wire up a new peer, not all packets communicated)
13:44 &lt;+detonate&gt; if introducers worked differently you could do a majority vote between them to decide which ones are working, but as it stands that doesn't make sense
13:45 &lt;ant&gt; &lt;jme___&gt; q. where can i find a description of this voting system ?
13:45 &lt;jrandom&gt; majority doesnt make any sense
13:45  * jrandom doesnt trust voting any further than i can throw it
13:45 &lt;jrandom&gt; (especially in light of sybil)
13:45 &lt;jrandom&gt; an introducer is working if a new peer can contact you through it
13:47 &lt;+detonate&gt; what's the status of vanguard, that's sort of related
13:47 &lt;+detonate&gt; while smeghead is around
13:51 &lt;jrandom&gt; ok, if there isn't anything else...
13:51  * jrandom winds up 
13:51  * jrandom *baf*s the meeting closed
</div>
