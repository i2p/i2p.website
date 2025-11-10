---
title: "I2P Dev Meeting - January 25, 2005"
date: 2005-01-25
author: "jrandom"
description: "I2P development meeting log for January 25, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, cervantes, frosk, Jhor, jrandom, jrandom2p, postman, protokol, Ragnarok, smeghead, Teal`c, Tracker</p>

## Meeting Log

<div class="irc-log">
13:50 &lt;jrandom&gt; 0) hi
13:50 &lt;jrandom&gt; 1) 0.5 status
13:50 &lt;jrandom&gt; 2) sam.net
13:50 &lt;jrandom&gt; 3) gcj progress
13:50 &lt;jrandom&gt; 4) udp
13:50 &lt;jrandom&gt; 5) ???
13:50 &lt;jrandom&gt; 0) hi
13:50  * jrandom waves belatedly
13:51 &lt;jrandom&gt; weekly status notes posted up to http://dev.i2p.net/pipermail/i2p/2005-January/000560.html
13:51 &lt;+postman&gt; hi
13:51  * brachtus waves back
13:52  * cervantes waves a detention slip for tardiness
13:52 &lt;jrandom&gt; yeah yeah, blame the code for sucking me in
13:52 &lt;jrandom&gt; ok, jumping into 1) 0.5 status
13:53 &lt;jrandom&gt; lots of progress since last week - all the messy problems we had with the new crypto are resolved without much trouble
13:54 &lt;jrandom&gt; the latest http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD is very likely to be what we deploy in 0.5 and beyond, unless/until people find any problems with it
13:55 &lt;jrandom&gt; not sure if i have anything else to add beyond whats in the email
13:55 &lt;jrandom&gt; anyone have any questions/concerns?
13:56 &lt;Ragnarok&gt; what's performance going to be like?
13:56 &lt;jrandom2p&gt; (not me)
13:56 &lt;jrandom&gt; Ragnarok: tunnel performance should be much better
13:56 &lt;frosk&gt; any significant overhead compared to what we have today?
13:57 &lt;jrandom&gt; frosk: sometimes
13:57 &lt;jrandom&gt; frosk: when we can coallesce messages in a tunnel, the overhead will be minimal
13:58 &lt;jrandom&gt; however, when we cannot coallesce or when its not effective, there can be nontrivial waste
13:58 &lt;frosk&gt; i see
13:59 &lt;jrandom&gt; otoh, we're trimming some of the absurdities of our current i2np (where we currently prepend a 32 byte SHA256 before each I2NP message, even ones within garlic messages, etc)
13:59 &lt;jrandom&gt; the fragmentation and fixed size will be an issue we need to tune with, but there is lots of room to do so
14:01 &lt;jrandom&gt; ok, anytihng else on 0.5?
14:02 &lt;jrandom&gt; if not, moving on to 2) sam.net
14:02 &lt;jrandom&gt; smeghead has ported the java sam client lib to .net (yay!)
14:02 &lt;jrandom&gt; smeghead: wanna give us the rundown?
14:03 &lt;smeghead&gt; sure
14:03 &lt;smeghead&gt; i'm writing tests for it, should have those in cvs in the next couple of days
14:04 &lt;smeghead&gt; should work with .net/mono/portable.net
14:04 &lt;smeghead&gt; and c# and vb.net
14:05 &lt;frosk&gt; (and all of the other languages that works with .net i suppose)
14:05 &lt;cervantes&gt; (urgh)
14:05 &lt;smeghead&gt; the interface is dirt simple
14:05 &lt;smeghead&gt; just register listener methods with SamReader, or subclass SamBaseEventHandler and override methods as necessary
14:05 &lt;smeghead&gt; yes, i aim to make it fully CLR compatible
14:06 &lt;jrandom&gt; wikked
14:06 &lt;cervantes&gt; cool... smeg.net ;-)
14:06 &lt;frosk&gt; goodie
14:06 &lt;smeghead&gt; really not much else to it
14:06 &lt;+protokol&gt; CLR?
14:06 &lt;smeghead&gt; common language runtime
14:06 &lt;smeghead&gt; the .net equivalent of the JRE
14:07 &lt;+protokol&gt; JRE?
14:07 &lt;+protokol&gt; just kidding
14:07 &lt;jrandom&gt; !thwap protokol 
14:07 &lt;Ragnarok&gt; jrandom: how's the sam bridge holding up these days?  were all the bt related issues resolved?
14:08 &lt;Tracker&gt; I doubt it, i2p-bt can even drive my amd64 3000 mad, cpu-wise...
14:08 &lt;jrandom&gt; Ragnarok: i havent touched it lately.  there's still the outstanding choke issue that polecat came up with, but where the i2p-bt&lt;--&gt;sam bridge is getting off, i'm not sure
14:09 &lt;jrandom&gt; hmm, failed connections will force full ElGamal instead of AES
14:10 &lt;Ragnarok&gt; ok
14:10 &lt;jrandom&gt; we should be able to reduce some of that after 0.5, but only partially
14:12 &lt;Tracker&gt; Ok, the I2P will be good for anonymus trackers but not for anonymus clients. Just try to think what happens on a really popular torrent with some 1000 seeds and leechs.
14:12 &lt;jrandom&gt; ok, the sam.net stuff sounds cool, thanks again smeghead.  i'm looking forward to the unit tests and perhaps a demo app :)
14:12 &lt;ant&gt; &lt;Evil-Brotten&gt; hello everbody
14:12 &lt;smeghead&gt; a demo app, yes i'll do that too
14:13 &lt;smeghead&gt; i've ported yours in fact
14:13 &lt;jrandom&gt; Tracker: i2p can handle anonymous clients just fine, we just need to figure out whats wrong with the i2p-bt&lt;--&gt;sam bridge to reduce the full ElG's
14:13 &lt;smeghead&gt; they're just bug-ridden atm
14:13 &lt;ant&gt; &lt;Evil-Brotten&gt; deer?
14:13 &lt;jrandom&gt; hi Evil-Brotten
14:13 &lt;ant&gt; &lt;Evil-Brotten&gt; hello
14:14 &lt;jrandom&gt; weekly dev meeting going on, feel free to stick around.  deer is a gateway to i2p/iip
14:14 &lt;ant&gt; &lt;Evil-Brotten&gt; are you an i2p expert?
14:14 &lt;ant&gt; &lt;Evil-Brotten&gt; :P
14:14 &lt;ant&gt; &lt;Evil-Brotten&gt; ow, ok
14:14 &lt;ant&gt; &lt;cervantes&gt; Evil-Brotten: you can talk in #i2p-chat if you like while the meeting is ongoing
14:14 &lt;jrandom&gt; Tracker: we've got a lot to do before handling 1k-wide torrents
14:14 &lt;ant&gt; &lt;Evil-Brotten&gt; i was just trying to install your program, but i am having some problems
14:14 &lt;ant&gt; &lt;Evil-Brotten&gt; cool, i will ask there
14:15 &lt;jrandom&gt; wikked smeghead 
14:15 &lt;Tracker&gt; jrandom: I hope so, non-anonymus bt won't survive much longer...
14:15 &lt;frosk&gt; nonsense
14:15 &lt;jrandom&gt; "but exeem is anonymous!@#" &lt;/snark&gt;
14:15 &lt;Tracker&gt; jrandom: But that's a different story
14:15 &lt;ant&gt; &lt;MikeW&gt; what?
14:15 &lt;ant&gt; &lt;MikeW&gt; who said exeem is anonymous?
14:16 &lt;jrandom&gt; mikew: just the occational fanboy
14:16 &lt;jrandom&gt; Tracker: after 0.5 we're going to have a lot of work to do getting performance where we need it to be
14:16  * DrWoo notes that 'people' are fucking morons (sometimes)
14:16 &lt;Tracker&gt; jrandom: Yeah, installing spy-/adware isn't really what I would do ;)
14:16 &lt;jrandom&gt; heh
14:17 &lt;smeghead&gt; i happen to like people
14:17 &lt;smeghead&gt; they're good on toast
14:17 &lt;jrandom&gt; *chomp*
14:17 &lt;smeghead&gt; some need a little more butter than others
14:18 &lt;jrandom&gt; ok, i think thats 'bout it for 2) sam.net (unless anyone has something else to add?)
14:18 &lt;jrandom&gt; if not, moving on to 3) gcj progress
14:19 &lt;ant&gt; &lt;dm&gt; sam.net??
14:19 &lt;ant&gt; &lt;dm&gt; is it working?/
14:19 &lt;jrandom&gt; i've read in my backlog that smeghead has been making some good headway - wanna give us an update on how its going?
14:19 &lt;smeghead&gt; yes
14:20 &lt;ant&gt; &lt;dm&gt; cooooooool
14:20 &lt;smeghead&gt; i modified a few classes so the router compiles with gcj 3.4.3
14:20 &lt;smeghead&gt; i will submit the patch after the meeting
14:20 &lt;smeghead&gt; after that i and anyone who would like to help can get to work on making it run
14:21 &lt;jrandom&gt; nice
14:21  * frosk decorates smeghead with the Employee of the Week medal for sam.net _and_ gcj work
14:21 &lt;jrandom&gt; aye, v.cool
14:21 &lt;smeghead&gt; :)
14:22 &lt;Tracker&gt; frosk: better forum user of the week ;)
14:22 &lt;frosk&gt; i haven't read the forum this week, sorry :)
14:22 &lt;cervantes&gt; duck's glory has not yet expired ;-)
14:23  * jrandom is very much looking forward to seeing i2p gcj compatible
14:24 &lt;jrandom&gt; (and there's still that bounty on it, so people should get in touch with smeghead and get involved ;)
14:24 &lt;smeghead&gt; yes it would expand i2p's portability significantly
14:24 &lt;cervantes&gt; maybe we'll be able to squeeze something that resembles performance from the router :P
14:24 &lt;ant&gt; &lt;dm&gt; my 32-week run as hardest I2P worker ends at last...
14:25 &lt;jrandom&gt; i dont expect gcj to actually improve performance or reduce the memory footprint, but it'll work on OSes that sun doesn't release JVMs for and kaffe is b0rked on
14:25 &lt;jrandom&gt; (but if i'm wrong, cool!)
14:25 &lt;frosk&gt; anything that can make i2p run better without proprietary software is Good
14:26 &lt;jrandom&gt; agreed.  supporting both kaffe and gcj would be a Good Thing
14:27 &lt;jrandom&gt; ok, anything else on 3) gcj progress, or shall we move on?
14:27 &lt;smeghead&gt; installation would be easier too
14:27 &lt;Teal`c&gt; has gcj worked for anything besides 'hello world' examples ?
14:27 &lt;Ragnarok&gt; someone built eclipse with it
14:27 &lt;smeghead&gt; Teal`c: yes, i've used it for .exe's under mingw before in fact
14:27 &lt;smeghead&gt; yes, eclipse was running under gcj with red hat not to long ago
14:28 &lt;jrandom&gt; having the option of distributing gcj'ed executables, plain .jar installers, and bundled .jar+jvm will definitely be Good
14:29 &lt;jrandom&gt; ok, moving on to 4) udp
14:30 &lt;jrandom&gt; there was a recent post to the forum that i just wanted to draw people's attention to, asking (and answering) why udp is important
14:30 &lt;Tracker&gt; Yuck
14:30 &lt;jrandom&gt; (see http://forum.i2p.net/viewtopic.php?t=280 and comment if you have any suggestions/questions/concenrs)
14:31 &lt;jrandom&gt; yuck Tracker?
14:32 &lt;jrandom&gt; anyway, both mule and detonate are making some headway on the udp side.  detonate/mule: y'all have any updates to share?
14:32 &lt;Tracker&gt; UPD is evil here, while it works well within the country borders it really get's ugly when trying to use it on destinations outside our countrys.
14:32 &lt;jrandom&gt; hmm
14:32 &lt;Tracker&gt; Just my experience from 5 years online gaming...
14:33 &lt;jrandom&gt; we'll certainly need to take into account the congestion and mtu issues as they go out on the net
14:33 &lt;Tracker&gt; Somehow the two big backbones here don't like to router UPD very well and if only with very low priority.
14:34 &lt;Tracker&gt; Meaning pings between 5 and 20 seconds.
14:34 &lt;jrandom&gt; i'd be pretty suprised if there was an isp that didn't allow UDP at all (since we all use DNS)
14:34 &lt;Tracker&gt; And high packet loss
14:34 &lt;jrandom&gt; congestion control is certainly important
14:35 &lt;Tracker&gt; Why do you think I'm running my own caching dns with a very big cache for years ;)
14:35 &lt;jrandom&gt; heh
14:35 &lt;jrandom&gt; well, we will have the fallback of tcp for people who cannot use udp for some reason
14:36 &lt;jrandom&gt; but udp will be overwhelmingly preferred 
14:36 &lt;Tracker&gt; That's nice.
14:36 &lt;jrandom&gt; (meaning i hope there will only be perhaps 10 people using tcp out of 1m+ nodes ;)
14:37 &lt;jrandom&gt; but, again, that forum link explains why we need to do what we're doing, though if anyone can find a better way, i'm all ears
14:37 &lt;Tracker&gt; I guess I will be one of them.
14:37 &lt;jrandom&gt; perhaps.  
14:38 &lt;jrandom&gt; we'll see as 0.6 is deployed whether thats the case, or whether we'll be able to work around the issues your isp has
14:38 &lt;jrandom&gt; ok, anything else on udp?  or shall we move on to 5) ???
14:39 &lt;jrandom&gt; consider us moved
14:39 &lt;jrandom&gt; 5) ??
14:39 &lt;jrandom&gt; anyone have anything else to bring up?
14:40 &lt;Teal`c&gt; is the pizza here yet ?
14:40 &lt;Jhor&gt; anybody know where i should look to find/debug problems in bittorrent?
14:41 &lt;jrandom&gt; Jhor: in i2p-bt, a good place to start would likely be adding in some logging to tell you what BT messages are sent/received, so we know where its blocking/timing out/etc
14:41 &lt;jrandom&gt; (assuming you mean i2p-bt and not azneti2p?)
14:42 &lt;Jhor&gt; yeah, i2p-bt.  what are the different spew levels?
14:42 &lt;jrandom&gt; no idea, all i know is --spew 1
14:42 &lt;Jhor&gt; Ok, I'll try that
14:43  * Jhor prepares for a crash course in python
14:43 &lt;jrandom&gt; :)
14:44 &lt;jrandom&gt; ok, anybody else have something to discuss?
14:44  * cervantes wheels out the Strand Gong
14:44 &lt;jrandom&gt; we're around the 60m mark, so a pretty good rate
14:44 &lt;Teal`c&gt; when is udp due for general consumption ?
14:44 &lt;jrandom&gt; Teal`c: april
14:44 &lt;jrandom&gt; thats 0.6, we're still working on 0.5
14:45 &lt;Teal`c&gt; nice work.
14:46 &lt;jrandom&gt; progress, ever onwards
14:46  * jrandom winds up
14:46  * jrandom *baf*s the gong, closing the meeting
</div>
