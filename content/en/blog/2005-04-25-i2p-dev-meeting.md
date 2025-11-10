---
title: "I2P Dev Meeting - April 25, 2005"
date: 2005-04-25
author: "jrandom"
description: "I2P development meeting log for April 25, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cervantes, Complication, inkeystring, jdot, jrandom, lsmith, perv, spinky</p>

## Meeting Log

<div class="irc-log">
16:12 &lt;jrandom&gt; 0) hi
16:12 &lt;jrandom&gt; 1) Net status and 0.6.1.17
16:12 &lt;jrandom&gt; 2) I2Phex
16:13 &lt;jrandom&gt;  3) ???
16:13 &lt;jrandom&gt; 0) hi
16:13  * jrandom waves
16:13 &lt;@cervantes&gt; 'lo
16:13 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2006-April/001283.html
16:14 &lt;jrandom&gt; while y'all skim that, lets jump into 1) Net status 
16:14 &lt;jrandom&gt; so, as most of y'all have seen, we've got a new release out, and so far, the results have been pretty positive
16:15 &lt;@cervantes&gt; (yay!)
16:15 &lt;jrandom&gt; still not where we need to be, but it pretty much sorts out the main issues we were seeing
16:15 &lt;jrandom&gt; aye, 'tis nice to have halfway decent tunnel build rates again, at 2+ hop tunnels :)
16:16  * jrandom has 50%+ success rates on another router w/ 1hop tunnels
16:17 &lt;jrandom&gt; I think the last few changes in 0.6.1.17 should help avoid this sort of congestion collapse in the future as well
16:17 &lt;jrandom&gt; the user-visible result though is that we'll occationally see lease expirations, but rather than compounding itself, it'll back off
16:17  * cervantes sparks up azureus
16:18 &lt;+Complication&gt; This morning, I recorded client tunnel (length 2 +/- 1) success rates near 35%
16:18 &lt;+Complication&gt; Currently it's lower, since I tried making some modifications, and the latest of them wasn't so great :D
16:18 &lt;@cervantes&gt; jrandom: well done tracking that down - we were beginning to look like freenet for a bit :)
16:19 &lt;jrandom&gt; *cough* ;)
16:20 &lt;+fox&gt; &lt;inkeystring&gt; jrandom: would you mind briefly describing the backoff mechanism? i'm working on something like that for freenet 0.7 at the moment
16:21 &lt;jrandom&gt; inkeystring: we've had a transport layer backoff mechanism in place to cut down transmissions to a peer when the transport layer is overloaded, but that wasn't sufficient
16:21 &lt;@cervantes&gt; *cough* did I say freenet, I meant tor
16:21 &lt;+fox&gt; &lt;inkeystring&gt; :-)
16:22 &lt;jrandom&gt; inkeystring: the new change was to propogate that up to a higher level so that we stopped trying to build tunnels when our comm layer was saturated
16:22 &lt;jrandom&gt; (rather than sending more tunnel build attempts)
16:22 &lt;+fox&gt; &lt;inkeystring&gt; thanks - does the transport layer only back off when packets are lost, or is there some way for the receiver to control the flow?
16:23  * jrandom seems to recall discussing the impact of congestion *vs* routing w/ toad a few times (on irc and my old flog), though i don't recall any net-positive solution :/
16:23 &lt;jrandom&gt; the receiver can NACK, and we've got hooks for ECN, but they haven't been necessary
16:23 &lt;+fox&gt; &lt;inkeystring&gt; yeah the debate has resurfaced on freenet-dev :-) still no silver bullet
16:24 &lt;+fox&gt; &lt;inkeystring&gt; cool, thanks for the information
16:24 &lt;+Complication&gt; They're using UDP too these days, aren't they?
16:24 &lt;jrandom&gt; currently, the highly congested peers have trouble not with per-peer throttling, but with the breadth of the peer comm
16:24 &lt;+Complication&gt; (as the transport protocol)
16:24 &lt;+fox&gt; &lt;inkeystring&gt; breadth = number of peers?
16:24 &lt;jrandom&gt; yes
16:25 &lt;jrandom&gt; with the increased tunnel success rates, peers no longer need to talk to hundreds of peers just to get a tunnel built
16:25 &lt;jrandom&gt; so they can get by with just 20-30 peers
16:25 &lt;jrandom&gt; (directly connected peers, that is)
16:26 &lt;+fox&gt; &lt;inkeystring&gt; i guess that's good news for nat hole punching, keepalives etc?
16:26 &lt;jrandom&gt; otoh, w/ 2-300 active SSU connections, a 6KBps link is going to have trouble
16:26 &lt;jrandom&gt; aye
16:26 &lt;+fox&gt; &lt;inkeystring&gt; Complication: yes
16:27 &lt;+fox&gt; &lt;inkeystring&gt; (in the 0.7 alpha)
16:27 &lt;+Complication&gt; Aha, then they're likely facing some similar stuff
16:27 &lt;+Complication&gt; I hope someone finds the magic bullet :D
16:27 &lt;jrandom&gt; in a different way though.  the transport layer is a relatively easy issue
16:27 &lt;+fox&gt; &lt;inkeystring&gt; i think they might have reused some of the SSU code... or at least they talked about it
16:27 &lt;jrandom&gt; (aka well studied for 30+ years)
16:28 &lt;jrandom&gt; but i2p (and freenet) load balancing works at a higher level than point to point links, and has different requirements
16:28 &lt;+fox&gt; &lt;inkeystring&gt; yeah it's the interaction with routing that's tricky
16:29 &lt;jrandom&gt; aye, though i2p's got it easy (we don't need to find specific peers with the data in question, just anyone with capacity to participate in our tunnels)
16:30 &lt;+fox&gt; &lt;inkeystring&gt; so there's no efficiency loss if you avoid an overloaded peer...
16:30 &lt;+fox&gt; &lt;inkeystring&gt; whereas in freenet, routing around an overloaded peer could increase the path length
16:30 &lt;+fox&gt; &lt;inkeystring&gt; anyway sorry this is OT
16:31 &lt;jrandom&gt; np, though explaining why the changes in 0.6.1.17 affect our congestion collapse was relevent :)
16:31 &lt;jrandom&gt; ok, anyone else have anything for 1) Net status?
16:32 &lt;+Complication&gt; Well, as actually mentioned before, while running pure .17, I observed a noticable periodism in bandwidth and active peers
16:32 &lt;+Complication&gt; And a few other people seem to experience it too, though I've got no clue about how common it is
16:33 &lt;+Complication&gt; I've been wondering about its primary causes, mostly from the perspective of tunnel throttling, but no solution yet
16:33 &lt;+Complication&gt; I managed to get my own graphs to look flatter, but only at the cost of some overall deterioration
16:33 &lt;+Complication&gt; Tried modifications like:
16:34 &lt;+Complication&gt;&gt; _log.error("Allowed was " + allowed + ", but we were overloaded, so ended up allowing " + Math.min(allowed,1));
16:34 &lt;+Complication&gt; (this was to avoid it totally refraining from build attempts for its own tunnels)
16:35 &lt;jrandom&gt; ah right
16:35 &lt;+Complication&gt; (oh, and naturally the loglevel is wacky, since I changed those for testing)
16:35 &lt;jrandom&gt; we've got some code in there that tries to skew the periodicity a bit, but it isn't working quite right (obviously)
16:36  * perv just shot his system :(
16:36 &lt;+Complication&gt; But I tried some things like that, and tried reducing the growth factor for tunnel counts
16:36 &lt;perv&gt; is there an undelete for reiser4?
16:36 &lt;jrandom&gt; basically, if we just act as if tunnels expire (randomly) earlier than they actually do, it should help
16:36 &lt;+Complication&gt; Currently reading the big "countHowManyToBuild" function in TunnelPool.java :D
16:36 &lt;+Complication&gt; But I've not read it through yet
16:37 &lt;jrandom&gt; (though it'd obviously increase the tunnel build frequency, which prior to 0.6.1.17, wouldn't have been reasonable)
16:37 &lt;+Complication&gt; perv: there is something
16:37 &lt;jrandom&gt; hmm, putting a randomization in there would be tough Complication, as we call that function quite frequently
16:38  * perv considers salvaging and switching to gentoo
16:38 &lt;jrandom&gt; what i'd recommend would be to look at randomizing the expiration time of successfully built tunnels
16:38 &lt;+Complication&gt; perv: you're better off with reiser than ext3, certainly
16:38 &lt;+Complication&gt; perv: but I don't know it by heart
16:38 &lt;+Complication&gt; jrandom: true, sometimes it could overbuild this way
16:38 &lt;jrandom&gt; (so that the existing countHowManyToBuild thinks it needs them before it actually does)
16:38 &lt;+Complication&gt; (and sometimes it inevitably overbuilds, when tunnels break and it gets hasty)
16:40 &lt;+Complication&gt; Hmm, a possibility I've not considered...
16:41 &lt;+Complication&gt; Either way, playing with it too, but no useful observations yet
16:42 &lt;jrandom&gt; cool, i've got some tweaks i've been playing with on that, perhaps we can get those together for the next build to see how it works on the reasonably-viable net ;)
16:43 &lt;spinky&gt; Is there a stat where you can see the amount of overhead the i2p network adds to the application data?
16:43 &lt;jrandom&gt; "overhead" is such a loaded term... ;)
16:43 &lt;jrandom&gt; we call it the cost of anonymity ;)
16:43 &lt;spinky&gt; hehe
16:45 &lt;jrandom&gt; (aka not really.  application layer payload on a perfect net w/ 0 congestion & 1+1hops gets something like 70-80% efficiency for the endpoints)
16:45 &lt;jrandom&gt; ((last i measured))
16:45 &lt;jrandom&gt; but thats really lab conditions
16:45 &lt;jrandom&gt; live net is much more complicated
16:47 &lt;spinky&gt; Right, I meant just the amount of extra data used for setting up tunnels, keys, padding etc 
16:47 &lt;spinky&gt; ...compared to the application data transferred
16:47 &lt;jrandom&gt; depends on the message framing, congestion, tunnel build success rates, etc
16:48 &lt;jrandom&gt; a 2 hop tunnel can be built by the network bearing 20KB
16:48 &lt;+Complication&gt; I've wanted to test that sometimes, primarily with the goal of estimating the "wastefulness" of mass transfer applications like BitTorrent and I2Phex
16:48 &lt;+Complication&gt; But I never got around to doing a clean measurement between my two nodes
16:48 &lt;+Complication&gt; Some day, I'll get back to that, though
16:49 &lt;jrandom&gt; Complication: its pretty tough with chatty apps, much simpler to measure wget :)
16:49 &lt;+Complication&gt; How very true
16:50 &lt;+Complication&gt; In what I managed to try, no resemblance of precision was involved
16:54 &lt;jrandom&gt; ok, if there's nothing else on 1), lets slide on over to 2) I2Phex
16:55 &lt;jrandom&gt; Complication: whatcha upta?  :)
16:55 &lt;+Complication&gt; Well, yesterday's commit was a fix to certain problems which some people experienced with my silly first-run detector
16:56 &lt;+Complication&gt; The first-run detector is now less silly, and bar reported that it seemed to start behaving normally
16:56 &lt;+Complication&gt; However, since I2Phex seems runnable already in current network conditions,
16:56 &lt;+Complication&gt; I'll try finding the rehash bug too.
16:57 &lt;+Complication&gt; If I only can
16:57 &lt;jrandom&gt; cool, i know that one has been haunting you for months now 
16:57 &lt;+Complication&gt; What is interesting that mainline Phex may also have it, and locating + reading their observations is something I'll try doing too
16:58 &lt;jrandom&gt; but nice to hear the startup fix is in there
16:58 &lt;jrandom&gt; ah word
16:58 &lt;+Complication&gt; =is that
16:58 &lt;+Complication&gt; I can't confirm currently if mainline Phex has it or not, though - never seen it personally there
16:59 &lt;jrandom&gt; (intermittent bugs)--
16:59 &lt;+Complication&gt; It's difficult to cause in controlled fashion, and thus difficult to find
17:00 &lt;+Complication&gt; And on my side, that's about all currently
17:00 &lt;+Complication&gt; Later on, I was wondering if it would be worthwhile to limit the number of parallel peer contacting attempts I2Phex fires at a time
17:01 &lt;jrandom&gt; aye, likely
17:01 &lt;+Complication&gt; Since they'd create a whole bunch of NetDB lookups in a short time, and that could be potentially not-so-nice from an I2P router's perspective
17:02 &lt;jrandom&gt; and new destination contacts require elG instead of aes
17:02 &lt;+Complication&gt; But I've not read or written any actual code towards that goal yet
17:04 &lt;jrandom&gt; k np.  perhaps the mythical i2phex/phex merge'll bundle a solution :)
17:04 &lt;+Complication&gt; And on my part, that's about all the news from the I2Phex front...
17:04 &lt;jrandom&gt; cool, thanks for the update and the effort looking into things!
17:05 &lt;jrandom&gt; ok, lets jump on over to 3) ???
17:05 &lt;jrandom&gt; anyone have anything else to bring up for the meeting?
17:05 &lt;lsmith&gt; hello! i just want to commend the devs on the fantastic improvements with the latest release, my total bw reads 0.9/1.4 KBps and i remain connected to irc... it's...insanely cool :)
17:05 &lt;+Complication&gt; :D
17:06 &lt;jrandom&gt; thanks for your patience along the way - supporting low bw users is critical
17:06 &lt;@cervantes&gt; lsmith: that's really good to
17:06 &lt;@cervantes&gt; * Connection Reset
17:06 &lt;jrandom&gt; heh
17:07 &lt;lsmith&gt; :)
17:09 &lt;jrandom&gt; oh, one other thing of note is that zzz is back, and with 'im comes stats.i2p :)
17:09 &lt;jrandom&gt; [wewt]
17:11 &lt;+Complication&gt; A quite useful source of comparison data :)
17:11 &lt;jrandom&gt; mos' def'
17:11 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
17:13 &lt;jrandom&gt; if not...
17:13 &lt;jdot&gt; i have a post-baf question or two
17:13 &lt;jrandom&gt; heh ok, then lets get the baffer rollin' :)
17:13  * jrandom winds up...
17:13  * jrandom *baf*s the meeting closed
</div>
