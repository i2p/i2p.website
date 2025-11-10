---
title: "I2P Dev Meeting - April 12, 2005"
date: 2005-04-12
author: "jrandom"
description: "I2P development meeting log for April 12, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bla, cervantes, defnax, detonate, frosk, gott, hummingbird, jdot, jrandom, mancom, Ragnarok</p>

## Meeting Log

<div class="irc-log">
14:05 &lt;jrandom&gt; 0) hi
14:05 &lt;jrandom&gt; 1) Net status
14:05 &lt;jrandom&gt; 2) SSU status
14:05 &lt;jrandom&gt; 3) Bayesian peer profiling
14:05 &lt;jrandom&gt; 4) Q status
14:05 &lt;jrandom&gt; 5) ???
14:05 &lt;hummingbird&gt; 7) Profit
14:06 &lt;jrandom&gt; damn, i messed up y'all's agenda :)
14:06 &lt;jrandom&gt; hi
14:06 &lt;jrandom&gt; weekly status notes posted /before/ the meeting up @ http://dev.i2p.net/pipermail/i2p/2005-April/000683.html
14:06 &lt;gott&gt; jrandom: try it again
14:06 &lt;+cervantes&gt; never mind, this meeting gott off onto a bad footing anyway
14:06 &lt;jrandom&gt; *cough*
14:06 &lt;jrandom&gt; jumping in to 1) Net status
14:07 &lt;jrandom&gt; the big problem we were seeing with the netDb has been fixed and confirmed dead in the wild
14:07 &lt;jrandom&gt; there are still some other issues, but it seems on the whole to be fairly reasonable
14:08 &lt;frosk&gt; any idea what's causing the weird dnfs sometimes?
14:08 &lt;gott&gt; confirm; I can get my illegal porn at record speeds for i2p now.
14:08 &lt;+cervantes&gt; seems like that might be a hard one to pin down
14:08 &lt;jrandom&gt; sneaking suspicion that its some confusion related to the throttle on the tunnel building
14:09 &lt;jrandom&gt; pulling out those throttles will probably address it, but could be painful for users with slow CPUs
14:09 &lt;jrandom&gt; otoh, perhaps we could make them optional, or someone could write some smarter throttling code
14:10 &lt;frosk&gt; i see
14:10 &lt;+cervantes&gt; the throttle seems much more pro-active than previous versions on my system
14:10 &lt;jrandom&gt; yeah, we delay tunnel building when there are too many outstanding - before we just said "ok, we need to build X tunnels.  build 'em"
14:10 &lt;+cervantes&gt; can we not make the threshold tweakable?
14:11 &lt;jrandom&gt; aye, that we can
14:11 &lt;gott&gt; jrandom: optional
14:11 &lt;gott&gt; so users with thin i2p servents can still be productive
14:12 &lt;jrandom&gt; my attention is focused elsewhere at the moment, so if someone wants to dig into that, the key method is TunnelPoolManager.allocateBuilds
14:12 &lt;jrandom&gt; (or if no one jumps at it, i can toss in some tweaks when the next build comes out)
14:13 &lt;+cervantes&gt; ........@    &lt;-- tumbleweed
14:13 &lt;jrandom&gt; :)
14:13 &lt;jrandom&gt; anyone have anything else for 1) net status, or shall we move on to 2) SSU?
14:14  * gott mutters something about too much talk and too little action when it comes to the i2p community
14:14 &lt;+cervantes&gt; perhaps in the future we can introduce performance profiles into the console
14:14 &lt;gott&gt; jrandom does too much on the development side.
14:14 &lt;+cervantes&gt; so people can choose a preset batch of config options for high/med/low spec systems
14:15 &lt;jrandom&gt; ooh good idea cervantes, there's lots of room for variants.  while we want to automatically tune ourselves as best we can, it may be easier for humans to do it
14:15 &lt;+cervantes&gt; since there are many that seem to be using low spec machines and modem connections atm
14:15 &lt;gott&gt; cervantes: yeah, excellent idea.
14:15 &lt;+cervantes&gt; I should publish my fire2pe todo list...it has lots of shit like that in it ;-)
14:16 &lt;gott&gt; based on processor and network speed primarily ?
14:16 &lt;jrandom&gt; a site with a pseudonymous todo list would be nice
14:16 &lt;gott&gt; that is a good idea.
14:16 &lt;+cervantes&gt; well the bandwidth limiter should ideally take care of net speed
14:16 &lt;gott&gt; in typical google-fashion, have a bunch of 'thin i2p servents' in your LAN.
14:17 &lt;+cervantes&gt; jrandom: ugha.i2p?
14:17 &lt;jrandom&gt; perhaps
14:19 &lt;jrandom&gt; ok, anything else for 1) net status?
14:19  * jrandom moves us on to 2) SSU
14:19 &lt;jrandom&gt; Lots of progress on the UDP front (SSU == Secure Semireliable UDP)
14:19 &lt;gott&gt; someone should alias 'i2pwiki.i2p' to that
14:20 &lt;+cervantes&gt; I guess that's up to ugha ;-)
14:20 &lt;jrandom&gt; the general overview of whats up is in the email, and a lot more technical details (and a pretty picture ;) is up on my blog
14:21 &lt;+ant&gt; &lt;godmode0&gt; udp is safe ?
14:21 &lt;+ant&gt; &lt;godmode0&gt; how :)
14:21 &lt;jrandom&gt; http://dev.i2p/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html &lt;-- how
14:22 &lt;+ant&gt; &lt;godmode0&gt; hehe
14:22 &lt;+ant&gt; &lt;godmode0&gt; i2p not found  right ip my computer
14:22 &lt;jrandom&gt; sorry, if you don't have i2p installed, change "dev.i2p" to "dev.i2p.net"
14:22 &lt;+ant&gt; &lt;godmode0&gt; have installled
14:23 &lt;+ant&gt; &lt;godmode0&gt; but not work
14:23 &lt;jrandom&gt; ok, perhaps we can debug that after the meeting 
14:23 &lt;+ant&gt; &lt;godmode0&gt; oops in meeting again sorry
14:23 &lt;jrandom&gt; hehe np
14:25 &lt;jrandom&gt; anyway, as i said, the general plan of how things are going is in the email
14:25 &lt;jrandom&gt; anyone have any questions/comments/concerns wrt SSU?
14:26 &lt;+Ragnarok&gt; will throughput/latency be much different than the tcp transport?
14:27 &lt;jrandom&gt; my hope is that the cause of the lag spikes will be addressed, but i'm not making any particular predictions.
14:28 &lt;jrandom&gt; if we can keep latency in the same ballpark as it is now and get rid of the spikes, we can jack back up the throughput
14:29 &lt;+Ragnarok&gt; cool
14:29 &lt;gott&gt; will there be documentation on the implementation provided on i2p.net ?
14:30 &lt;jrandom&gt; much of my time when i go offline to move will be writing up docs to be put on the website, yes
14:30 &lt;gott&gt; awesome \m/
14:30 &lt;jrandom&gt; we do have some pretty good implementation docs at the code level for the core and router, but no great overall router architecture docs yet
14:31 &lt;jrandom&gt; anyway, if there's nothing else on 2) SSU, lets shimmy on over to 3) Bayesian peer profiling
14:32 &lt;jrandom&gt; we got a brief update from bla earlier this evening, as shown in the status notes
14:32 &lt;+bla&gt; I'm still here though... ;)
14:33 &lt;jrandom&gt; bla may atcually still be around to give us any further thoughts or answer questions -
14:33 &lt;jrandom&gt; ah, there you are
14:33 &lt;defnax&gt; jrandom : what do you think about anounce i2p bittorrent Tracker, for security i think is not good or?, 
14:34 &lt;+bla&gt; The IRC discussion quoted by jrandom shows the general idea. Summarized: 
14:34 &lt;jrandom&gt; defnax: perhaps we can discuss that further in 5) 
14:34 &lt;defnax&gt; ok i can wait 
14:34 &lt;+bla&gt; The eventual idea is to use both round-trip-time information obtained from explicit tunnels tests, and implicit information from client-tunnel tests, into one node-speed estimation framework
14:35 &lt;+bla&gt; For now, I use information obtained from explicit tunnel tests only, as for those tests, all participating peers are known.
14:36 &lt;+bla&gt; A naive Bayesian classifier framework will be used to estimate a peer's speed, given the tunnels in which it has participated (in any position), and how fast those tunnels were
14:36 &lt;+bla&gt; In order to compare things to a "ground truth", I've obtained "actual" peer speeds as listed in the status notes
14:37 &lt;+bla&gt; Results are very prelim. But http://theland.i2p/estspeed.png shows the correlation between actual speeds, and speeds inferred using the Bayesian framework
14:37 &lt;+bla&gt; Well. Any questions or comments?
14:38 &lt;jrandom&gt; comment: looks promising.  
14:38 &lt;+ant&gt; &lt;BS314159&gt; it seems like the total tunnel speed provides a hard lower bound on the speed of every participating peer
14:38 &lt;+detonate&gt; comment: seem to be a few outliers
14:38 &lt;+ant&gt; &lt;BS314159&gt; is that incorporated?
14:39 &lt;jrandom&gt; BS314159: total tunnel speed?  oh, do you mean the testing node's net connection?
14:40 &lt;+bla&gt; BS314159: That does provide a lower bound, yes. This is not addressed yet, but will be: The naive Bayesian framework enables weighting different samples (RTT measurements) to different degrees. Very fast RTTs will be weighted by a larger factor in the future
14:40 &lt;+ant&gt; &lt;BS314159&gt; I mean the total bandwidth of a given tunnel
14:40 &lt;+bla&gt; BS: The results show _latency_ measurements, for now
14:40 &lt;+ant&gt; &lt;BS314159&gt; right.
14:41 &lt;+ant&gt; &lt;BS314159&gt; nevermind, then
14:41 &lt;jrandom&gt; ah, right, certainly.  throughput measurements will require further modifications to test with different size messages
14:41 &lt;jrandom&gt; otoh, the implicit tunnel tests are driven by larger messages (typically 4KB, since thats the streaming lib fragmentation size)
14:42 &lt;+bla&gt; detonate: Yes, there are outliers. There will always be _some_ (that's inherent to estimation, and modeling in general). However, the separation between really slow and really fast clients (putting a threshold at around 400 ms), is ok-ish
14:42 &lt;+detonate&gt; ok
14:43 &lt;+bla&gt; jrandom: Indeed. Once I get that working (in not a Java buff...), I'll also test using the larger messages
14:43 &lt;+bla&gt; detonate: Now, I'd like to make the separation between fast and really-fast peers in a better way.
14:43 &lt;jrandom&gt; cool, i'll see if i can bounce you a modified TestJob for that
14:44 &lt;+bla&gt; I'll report when I have new results.
14:44 &lt;jrandom&gt; kickass
14:45 &lt;jrandom&gt; ok cool, anyone else have anything for 3) Bayesian peer profiling?
14:46 &lt;jrandom&gt; if not, moving on to 4) Q status
14:46 &lt;jrandom&gt; As mentioned in the email, rumor has it Aum is making progress on a new web interface
14:47 &lt;jrandom&gt; i don't know much about it, or the status details on the rest of the Q updates, but i'm sure we'll hear more soon
14:48 &lt;jrandom&gt; anyone have anything on Q to bring up?  or shall we make this a rapid fire agenda item and move on to 5) ???
14:49 &lt;jrandom&gt; [consider us moved]
14:49 &lt;jrandom&gt; ok, anyone have anything else to bring up for the meeting?
14:50 &lt;jrandom&gt; defnax: announcing an i2p tracker to people in the i2p community would be great.  to the outside world it might be a bit rough, since we aren't at 0.6 yet
14:50 &lt;gott&gt; Yes.
14:50 &lt;jrandom&gt; (or 1.0 ;)
14:50 &lt;gott&gt; I have some information to bring up on userland documentation efforts.
14:51 &lt;+mancom&gt; just for the record: on mancom.i2p there is a c# implementation of Q's client api (in its first incarnation)
14:51 &lt;jrandom&gt; oh cool, sup gott
14:51 &lt;jrandom&gt; ah nice1 mancom
14:51 &lt;gott&gt; I have previously written userland documentation for 0.4 i2p.
14:52 &lt;jrandom&gt; which i unforutnately obsoleted by changing a whole bunch of stuff :(
14:52 &lt;gott&gt; But it is entirely out-of-date with current i2p.
14:52 &lt;gott&gt; Accordingly, I am very interested in writing a defacto set of documentation that we can either (a) bundle with i2p or (b) have access via i2p.
14:53 &lt;jrandom&gt; wikked.  docs to bundle with i2p (localized to the user's language, etc) would be great
14:53 &lt;+cervantes&gt; cool
14:53 &lt;gott&gt; I don't suggest bundling, but it is still a possible option, as a user can't access eepsites to read the manual if he doesn't know how to use or configure i2p ;-)
14:53 &lt;gott&gt; Okay.
14:53 &lt;gott&gt; But is it overkill ?
14:53 &lt;+ant&gt; &lt;BS314159&gt; what respectable program comes without man pages?
14:53 &lt;+cervantes&gt; and is it worth waiting til 1.0?
14:54 &lt;gott&gt; That is another question.
14:54 &lt;jrandom&gt; since development is fairly fluid, it might be worth focusing on context-specific help, rather than an overall user guide
14:54 &lt;gott&gt; BS314159: these are not manpages, as it will be platform-independent. Probably HTML.
14:54 &lt;+cervantes&gt; how much more structural changes are we due before then
14:54 &lt;jrandom&gt; for instance, it'd be nice to have better docs describing what the different config options *mean*, what their implications are, etc.
14:55 &lt;gott&gt; Okay, so I shall write an english and french localisation of a manual for i2p.
14:55 &lt;+jdot&gt; actually, we could use the inproxy to access the documentation even w/o i2p being installed.
14:55 &lt;gott&gt; Two major questions :
14:55 &lt;jrandom&gt; those could be kept up to date by virtue of being *in* the interface itself
14:55 &lt;+cervantes&gt; yeah context help would rock
14:55 &lt;gott&gt; (1) Bundled or accessible via manual.i2p ?
14:55 &lt;gott&gt; (2) For which version ?
14:55 &lt;gott&gt; yes
14:55 &lt;jrandom&gt; gott: i'm not sure it'd be wise to build a user guide yet
14:55 &lt;gott&gt; that's a great idea
14:56 &lt;gott&gt; do you mean to use the auto-update function to update the usermanual ?
14:56 &lt;gott&gt; jrandom: okay
14:56 &lt;gott&gt; but then how do you suggest context-specific help ?
14:56 &lt;jrandom&gt; oh, we can certainly deploy updates to the docs with the update process
14:56 &lt;+cervantes&gt; if/when it's time to do a manual then perhaps a manual.war can be dropped into a user's webapps folder if they want local access to the docs
14:57 &lt;gott&gt; I am thinking of a user-manual.
14:57 &lt;gott&gt; or a HOWTO.
14:57 &lt;gott&gt; I have no idea what you mean by context-specific help.
14:57 &lt;gott&gt; it's pretty straightforward.
14:57 &lt;jrandom&gt; gott: for instance, a set of human (non-ubergeek) readable info explaining wtf things on /config.jsp mean.  that info would go *on* /config.jsp, or on an html page reachable from that config.jsp
14:58 &lt;jrandom&gt; a user-manual or howto would be great, but not until 1.0
14:59 &lt;jrandom&gt; there's already some work on that front in the forum @ http://forum.i2p.net/viewtopic.php?t=385
14:59 &lt;gott&gt; jrandom: yes.
14:59 &lt;gott&gt; well.
14:59 &lt;gott&gt; the information on config.jsp is pretty straightfoward already 
15:00 &lt;jrandom&gt; otoh, we see questions about what bandwidth limits actually do, how the burst rates work, etc here all the time.  it'd be great to have the answers on the page, rather than have people ask
15:00 &lt;gott&gt; heh
15:00 &lt;jrandom&gt; gott: its straightforward to you because you've been using i2p for almost two years
15:00 &lt;gott&gt; nevermind, 'configtunnels.jsp' could use some work.
15:00 &lt;gott&gt; okay.
15:00 &lt;+cervantes&gt; straightforward to the initiated perhaps, a n00b would be lost
15:01 &lt;gott&gt; this is, then, a more up-to-date selection of tasks :
15:01 &lt;+cervantes&gt; not sure the best way to present the help from an interface perspective
15:01 &lt;gott&gt; (1) Context-specific help on the webpages localised to user's language. A configuration variable can be set for the language interface, by default, loaded from $LANG path variable on linux
15:02 &lt;gott&gt; I'm not sure how java figures out the default locale under windows.
15:02 &lt;gott&gt; But this is a good start to localisation and documentation writing.
15:03 &lt;gott&gt; (2) For version 1.0, a HOWTO _accessed_ via i2p
15:03 &lt;gott&gt; I don't suggest bundling the HOWTO, as that is just overkill. Would be nice to keep i2p as small as possible, hmm ?
15:03 &lt;jrandom&gt; dood, its html.  its tiny.  even if its huge, html compresses *really* well
15:03 &lt;jrandom&gt; having a local manual would be very much preferred
15:03 &lt;jrandom&gt; especially since we can push updates
15:03  * gott shrugs
15:04 &lt;gott&gt; I suppose.
15:04 &lt;gott&gt; I just find it silly.
15:04 &lt;gott&gt; when you can just download it via the web.
15:04 &lt;gott&gt; but on the other hand, if the user can't figure out how to use i2p
15:04 &lt;gott&gt; he can't.
15:04 &lt;+ant&gt; &lt;Synonymous2&gt; Is aum around, i was looking at the specs for QuarterMaster
15:04 &lt;+ant&gt; &lt;Synonymous2&gt; * In order to help client-side searching, all data items are accompanied
15:04 &lt;+ant&gt; &lt;Synonymous2&gt;    by a simple metadata schema - so far, just consisting of:
15:04 &lt;+ant&gt; &lt;Synonymous2&gt;     - key - text name of key
15:04 &lt;+jdot&gt; put it on www.i2p.net so it is accessible via the intarweb and i2p.
15:04 &lt;+jdot&gt; and always up to date
15:05 &lt;gott&gt; yeah.
15:05 &lt;gott&gt; well, just use the update mechanism.
15:05 &lt;gott&gt; okay.
15:05 &lt;gott&gt; so, finalising :
15:05 &lt;jrandom&gt; sure, we can put it on the website too.  we can spam it all over the net if it helps ;)
15:05 &lt;+ant&gt; &lt;Synonymous2&gt; I am wondering if Aum can implement the datastore so the metadata are seperated incase he wants to upgrade the storage system.  Remember when Freenet wanted to change the storage system but was stuck
15:05 &lt;gott&gt; 1 : Localised interface and context-specific help.
15:05 &lt;gott&gt; 2 : Localised HOWTO for version 1.0
15:05 &lt;+ant&gt; &lt;Synonymous2&gt; oopse is this the meeting :)
15:05 &lt;gott&gt; Any additions ?
15:06 &lt;gott&gt; the HOWTO will cover a lot of extra i2p-network features.
15:06 &lt;gott&gt; where to get the latest porn ( j/k )
15:06 &lt;+ant&gt; &lt;BS314159&gt; manpage! :-)
15:06 &lt;gott&gt; manpages aren't platform-independent
15:06 &lt;jrandom&gt; cool, including things like Q, i2ptunnel, feedspace, i2p-bt, etc would be great for a howto
15:06 &lt;+cervantes&gt; the installer could be localised too I guess...
15:06 &lt;gott&gt; the i2p network has a hilariously large amount of french users
15:07 &lt;+Ragnarok&gt; you should clearly write the addressbook documentation I've never gotten around to :)
15:07 &lt;gott&gt; I'm sure they would appreciate a localised interface so they don't have to look at the disgusting english language
15:07 &lt;+cervantes&gt; hey it's mostly french already
15:07 &lt;gott&gt; true.
15:07 &lt;gott&gt; good ideas.
15:08 &lt;gott&gt; well, that is all I had to say.
15:08 &lt;jrandom&gt; ok cool, thanks gott, nice initiative
15:08 &lt;gott&gt; for now, I shall start on the context-specific stuff
15:08 &lt;jrandom&gt; Synonymous2: I'm not sure what Aum is doing on that front
15:08 &lt;jrandom&gt; bitchin'
15:08 &lt;gott&gt; and then, when a localisation option is added, the localised languages 
15:08 &lt;+bla&gt; gott: Je _deteste_ Anglais! ;)
15:09 &lt;gott&gt; moi aussi
15:09 &lt;+ant&gt; &lt;Synonymous2&gt; Q, i2ptunnel, feedspace, i2p-bt, etc would be great for a howto, i think the wiki article should be updated for i2p to add this, i'll do that
15:09 &lt;+cervantes&gt; ewll you have william the conquerer to blame for that
15:09 &lt;jrandom&gt; heh
15:09 &lt;gott&gt; a wiki is good, but also non-official.
15:09 &lt;gott&gt; the manual has the element of certification.
15:09 &lt;gott&gt; it is more reassuring.
15:10 &lt;+ant&gt; &lt;Synonymous2&gt; if ppl want to come and look that would be helpful too, the freenet wikipedia article is also good describing the tools for freenet.  As well, I see that the Freenet webpage is released under the GNU FDL, if i2p.net could do the same (or public domain) I could copy some stuff to wikipedia :)) if you want to do that
15:10 &lt;+cervantes&gt; we'd still be speaking anglo-saxon otherwise
15:10 &lt;jrandom&gt; everything i do which i 'have rights to' is released implicitly into the public domain
15:11 &lt;+ant&gt; &lt;Synonymous2&gt; i thought it was, if you can put that as a blurb on the webpage that would be great at your convience, the ppl at wikipedia are anal bout copyright :&gt;
15:11 &lt;+ant&gt; &lt;Synonymous2&gt; :)))
15:11 &lt;gott&gt; jrandom: all the localisation I write will be public domain
15:11 &lt;jrandom&gt; otoh, outright copying the text is, er, not too helpful, as your copies will be out of date - just link to it, the web is there for a reason
15:11 &lt;gott&gt; I don't give a damn about any licenses.
15:12 &lt;gott&gt; also, last question :
15:12 &lt;+ant&gt; &lt;Synonymous2&gt; i was going to copy a few things like the chart and some graphics hehe
15:12 &lt;gott&gt; where are the .jsp for the router located ?
15:12 &lt;jrandom&gt; gott: http://dev.i2p/cgi-bin/cvsweb.cgi/apps/routerconsole/jsp/
15:13 &lt;gott&gt; ah
15:13 &lt;gott&gt; so, locally, they are in a .jar ?
15:13 &lt;jrandom&gt; gott: routerconsole.war
15:13 &lt;jrandom&gt; but you can't really edit them there, as they're precompiled into java
15:13  * gott nods
15:13 &lt;gott&gt; Sure.
15:14 &lt;gott&gt; Though, that's an inconvenience.
15:14 &lt;gott&gt; when localisation comes out, that might be changed ?
15:14 &lt;jrandom&gt; yep.  lots of options though.  if you work out the html that the jsps should render as, we can wire it in
15:14 &lt;+cervantes&gt; Synonymous: http://www.i2p.net/licenses
15:15 &lt;gott&gt; so you can have language packs
15:15  * gott nods
15:15 &lt;gott&gt; for now, it is just hardcoded
15:15 &lt;jrandom&gt; localization in java works by loading up per-language properties files with resources
15:15 &lt;gott&gt; but later on, it should be less restricted, I suggest
15:15 &lt;jrandom&gt; right right
15:16 &lt;gott&gt; awesome.
15:16 &lt;gott&gt; well, I'll use anonymous CVS then ;-)
15:16 &lt;jrandom&gt; bitchin'
15:16 &lt;+ant&gt; &lt;BS314159&gt; bla: is your raw data available anywhere?
15:16 &lt;jrandom&gt; bla has recently disconnected, but we'll see about getting some data available
15:17 &lt;gott&gt; btw, do we have anyone running i2p on openbsd ?
15:17 &lt;+ant&gt; &lt;BS314159&gt; it's be fun to let people try their own estimators
15:17 &lt;+ant&gt; &lt;BS314159&gt; sister:...23?
15:17 &lt;jrandom&gt; gott: yeah, i think detonate is
15:18 &lt;+ant&gt; &lt;BS314159&gt; ack
15:18 &lt;+ant&gt; &lt;BS314159&gt; cross-post
15:18 &lt;+ant&gt; &lt;BS314159&gt; curses!
15:18 &lt;gott&gt; is it even possible ? what are the java limitations regarding openbsd and i2p ?
15:18 &lt;gott&gt; okay.
15:18 &lt;jrandom&gt; BS314159: yeah, there's some good info about modifying your estimators up in the forum
15:18 &lt;+cervantes&gt; long meeting
15:18 &lt;gott&gt; if I ever have time, I might get it running and setup a port.
15:18 &lt;gott&gt; but that is long off and someone will probably do it before me ;-)
15:18 &lt;jrandom&gt; cervantes: check the logs, we've broken 2h before ;)
15:19 &lt;jrandom&gt; ok, anyone else have anything for the meeting?
15:20 &lt;jrandom&gt; if not
15:20  * jrandom winds up
15:20  * jrandom *baf*s the meeting closed
</div>
