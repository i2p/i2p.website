---
title: "I2P Dev Meeting - August 02, 2005"
date: 2005-08-02
author: "jrandom2p"
description: "I2P development meeting log for August 02, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bar, cervantes, duck, jrandom2p, lucky, mihi, protokol, smeghead, thetower</p>

## Meeting Log

<div class="irc-log">
13:53 &lt;jrandom2p&gt; ok, as i'm here, is there anyone interested in having a brief meeting wrt the notes (or something else)?
13:54 &lt;jrandom2p&gt; anything in the notes people are concerned with, thoughts not related to 'em that people want to bring up, or other issues relevent and timely?
13:54 &lt;@smeghead&gt; sure
13:54 &lt;+protokol&gt; is icepick here?
13:55 &lt;+protokol&gt; i am wondering if i2p-mnet is testable yet and/or an ETA on it
13:55 &lt;jrandom2p&gt; idle for 9 hours atm..
13:56 &lt;jrandom2p&gt; from the channel logs, it didnt sound workable, but he did get the basic SAM integration going
13:56 &lt;jrandom2p&gt; i'm sure we'll hear more when there's more to hear
13:56 &lt;+protokol&gt; cooool
13:57 &lt;jrandom2p&gt; smeghead: has -1 fixed your port migration issue?
13:57 &lt;@smeghead&gt; i haven't noticed any funny business
13:58 &lt;@smeghead&gt; in 3 days or so
13:58 &lt;@cervantes&gt; glad to say I haven't had a loss of service for a day or two
13:58 &lt;@smeghead&gt; i think i can call it fixed
13:58 &lt;jrandom2p&gt; wr0d
13:58 &lt;jrandom2p&gt; (^2)
13:59 &lt;@cervantes&gt; and thetower is only reconnecting every 4 minutes now...so the network health in general must be improving
13:59 &lt;jrandom2p&gt; heh
13:59 &lt;+thetower&gt; A fresh install seemed to fix the problem, but it was really quite disturbing and I never could find a good reason for it.
14:00 &lt;jrandom2p&gt; hmm
14:00 &lt;jrandom2p&gt; was it irc only, or were you losing many peers?
14:00 &lt;@cervantes&gt; gremlins
14:01 &lt;+thetower&gt; Is it possible that changing the router.config file without restarting i2p would have caused the crashes?
14:01 &lt;jrandom2p&gt; hmm, no, i change router.config often
14:01 &lt;jrandom2p&gt; or, is there a particular change you're concerned with?
14:02 &lt;@cervantes&gt; I remember copying over my jbigi lib once while the router was still running.... THAT caused problems ;-)
14:02 &lt;+thetower&gt; I set up some script to alter the bandwidth limits based on current network usage and I was wondering if that was causing the problem.
14:02 &lt;jrandom2p&gt; heh yeah cervantes, that'll always kill the router
14:03 &lt;jrandom2p&gt; ah ok, no, that shouldnt be a problem... though... if it altered the limits to be too small for messages to get through...
14:04 &lt;+thetower&gt; Well, it had fairly reasonable lower limits so I guess that wasn't it.
14:04 &lt;jrandom2p&gt; ok cool, just checkin~ :)
14:05 &lt;jrandom2p&gt; i suppose we'll have 0.6.0.1 tomorrow then, as -1 seems to be a pretty good improvement
14:05 &lt;jrandom2p&gt; it'll be backwards compat, etc, yadda yadda.
14:06 &lt;jrandom2p&gt; anything else y'all know that needs to get pushed out there?
14:06 &lt;jrandom2p&gt; whats the status with i2phex?
14:06 &lt;@smeghead&gt; maybe push the cvs hosts.txt to dev.i2p.net... the current one is months old
14:06 &lt;jrandom2p&gt; i did the other night iirc
14:07 &lt;@smeghead&gt; sirup hasn't been around in a couple of weeks
14:07 &lt;jrandom2p&gt; ooh, hmmm..
14:07 &lt;@smeghead&gt; it's summer though
14:07 &lt;@smeghead&gt; maybe on holiday or something
14:08 &lt;@cervantes&gt; or he's been bum-raped by the riaa
14:08 &lt;jrandom2p&gt; ah yeah, its up there (it was just cached on squid.i2p)
14:08 &lt;@smeghead&gt; riaaped?
14:09 &lt;jrandom2p&gt; ($Id: meeting141.html,v 1.2 2005-08-04 16:21:39 duck Exp $)
14:09 &lt;jrandom2p&gt; *cough*
14:09 &lt;+bar&gt; there are some things that need to be added to bugzilla, like i2p 0.6 and java 1.5
14:09 &lt;@smeghead&gt; ok
14:09 &lt;jrandom2p&gt; ah right, yeah i still havent gotten my laptop online yet (grr)
14:10 &lt;jrandom2p&gt; ((the weekly status notes needed to be burnt to cd... a 1KB cd...))
14:10 &lt;jrandom2p&gt; woah heya mihi
14:10 &lt;@duck&gt; hi mihi!
14:10 &lt;mihi&gt; hi all :)
14:10 &lt;@cervantes&gt; could be dm :)
14:10 &lt;jrandom2p&gt; heh
14:10 &lt;@smeghead&gt; indeed
14:10 &lt;@cervantes&gt; 'lo mihi
14:10 &lt;mihi&gt; seemed to require a bit of tweaking in the config file till my router believed that *only* 8887/udp is open...
14:11  * jrandom2p mentioned i2ptunnel in the status notes and mihi appears ;)
14:11 &lt;jrandom2p&gt; ah, hmm, the i2np.udp.fixedPort=true thing?
14:11 &lt;mihi&gt; hmm? was it there?
14:11  * mihi read status notes only quickly
14:11 &lt;mihi&gt; hmm... is that better solution?
14:12  * mihi just reset the port to 8887 and restarted hard until it did not change the port...
14:12 &lt;jrandom2p&gt; whats the tweak you did to your router.config to make it believe only 8886?
14:12 &lt;jrandom2p&gt; er, 8887
14:12 &lt;jrandom2p&gt; hah
14:12 &lt;@cervantes&gt; can we perhaps rename I2PTunnel as you suggested to something like I2PProxy...?
14:12 &lt;jrandom2p&gt; ok, yeah, use i2np.udp.fixedPort=true
14:12 &lt;jrandom2p&gt; (deployed in 0.6-1 and to be released asap as 0.6.0.1)
14:12 &lt;@cervantes&gt; it can get very confusing talking about "the tunnel config page"
14:13 &lt;+thetower&gt; Oh I have a question, isn't i2p supposed to automatically detect which udp port to use? And if so, is it supposed to be hard coded in the default router.config?
14:13 &lt;mihi&gt; hmmkay...
14:14 &lt;mihi&gt; seems that i2p changed the port once again
14:14 &lt;mihi&gt; expect me to be away soon :)
14:14 &lt;jrandom2p&gt; thetower: yes, it should automatically detect, but there are some funky tap dances that we~re going through at the moment 
14:14 &lt;@cervantes&gt; mihi: d'you have the latest cvs?
14:14 &lt;jrandom2p&gt; thats what the whole PeerTest thing is about (making it so that we always automatically configure it properly)
14:14 &lt;mihi&gt; nope.
14:14 &lt;@cervantes&gt; mihi: that would be why then :)
14:15 &lt;mihi&gt; only the version from i2pupdate.zip
14:15 &lt;@cervantes&gt; mihi: 0.6 has RandomPort (tm) functionality
14:15 &lt;jrandom2p&gt; heh
14:16 &lt;@cervantes&gt; :)
14:16 &lt;+ant&gt; * mihi 'd like FixedPorto functionality :)
14:16 &lt;+ant&gt; &lt;mihi&gt; and disconnected...
14:16 &lt;@cervantes&gt; then you'd need  0.6-1 FixedPort Pro
14:16 &lt;jrandom2p&gt; heh
14:16 &lt;jrandom2p&gt; ok, anyone else have something to bring up for the meeting?
14:16 &lt;@cervantes&gt; or wait for 0.6.0.1
14:17 &lt;jrandom2p&gt; how has the latency/throughput been, barring the intermittent reachability?
14:17 &lt;+ant&gt; &lt;mihi&gt; hmm. here is a cvs checkout from 2004-10-06. should try to update it :)
14:17 &lt;jrandom2p&gt; !thwap mihi
14:18 &lt;@cervantes&gt; I got i2pinstall.jar at 110k/sec from dev.i2p yesterday on a single stream
14:18 &lt;jrandom2p&gt; nice
14:19 &lt;@cervantes&gt; and 320k/sec using multiple
14:19 &lt;jrandom2p&gt; w0ah
14:19 &lt;jrandom2p&gt; 0hop, i assume
14:19 &lt;jrandom2p&gt; (dev.i2p is 0hop)
14:19 &lt;@cervantes&gt; yup
14:19 &lt;jrandom2p&gt; ((in case you couldn't tell ;)
14:19 &lt;@cervantes&gt; ;-)
14:19 &lt;+thetower&gt; download to:    GTA San Andreas
14:19 &lt;+thetower&gt; download rate:  28.51 kB/s
14:20 &lt;@cervantes&gt; that was from multiple sources though...
14:20 &lt;jrandom2p&gt; ah cool thetower 
14:20 &lt;@cervantes&gt; managed to push squid.i2p up to about 280
14:21 &lt;lucky&gt; jrandom2p :)
14:21 &lt;lucky&gt; would you push the new hosts.txt to the site
14:21 &lt;@cervantes&gt; lucky: tis done
14:21 &lt;jrandom2p&gt; yeah, once we can consistently pull that sort of rate cervantes, we'll need to add on some configurable delays to let people do 0hops safely
14:22 &lt;jrandom2p&gt; (so it delays AVG(tunnelTestTime/2) but doesnt waste bw or lose messages)
14:22 &lt;@cervantes&gt; to hide the fact that it's a 0 hop tunnel?
14:22 &lt;lucky&gt; i wonder if I2P will ever have speeds decent enough tha ti could let people log into my virtu-vax
14:23 &lt;jrandom2p&gt; yeah.  otherwise, if you say "hey i~m getting 300KBps from your site", you can pretty safely guess that its 2 0hop tunnels
14:23 &lt;jrandom2p&gt; (otoh, 1 to 2 to 3 to 4hops don't have such a dramatic cut)
14:23 &lt;@cervantes&gt; so will i2p effectively have a bandwidth cap
14:23 &lt;jrandom2p&gt; ((as once you force true tunnel operation, each intermediate hop isn't much))
14:24 &lt;jrandom2p&gt; nah cervantes, large windows + delays 
14:24  * cervantes cancels his plans for HDTV streaming anonymous pr0n
14:24 &lt;jrandom2p&gt; you can just have more messages in the air to get the same rate
14:25 &lt;@cervantes&gt; ah right
14:25 &lt;jrandom2p&gt; (but it'll take a few more rtts to get to the larger window, of course)
14:25 &lt;jrandom2p&gt; ok, anyone have anything else to bring up?
14:26 &lt;mihi&gt; bring up a *baf*er :)
14:26 &lt;@cervantes&gt; it's gone rusty with missuse
14:27 &lt;jrandom2p&gt; heh i suppose its time ;)
14:27  * jrandom2p winds up
14:27  * jrandom2p *baf*s the meeting closed
</div>
