---
title: "I2P Dev Meeting - October 19, 2004"
date: 2004-10-19
author: "jrandom"
description: "I2P development meeting log for October 19, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> deer\_, jrandom, modulus</p>

## Meeting Log

<div class="irc-log">
14:03 &lt;jrandom&gt; 1) 0.4.1.3
14:03 &lt;jrandom&gt; 2) Tunnel test time, and send processing time
14:03 &lt;jrandom&gt; 3) Streaming lib
14:03 &lt;jrandom&gt; 4) files.i2p
14:03 &lt;jrandom&gt; 5) ???
14:03 &lt;jrandom&gt; 0) hi
14:03  * jrandom waves
14:04 &lt;modulus&gt; hi hi
14:04 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2004-October/000469.html
14:04 &lt;deer_&gt; &lt;fidd&gt; howdy
14:04 &lt;jrandom&gt; i didn't spend much time on the notes, so they're pretty brief
14:05 &lt;jrandom&gt; but, c'est la vie
14:05 &lt;jrandom&gt; moving on to 1) 0.4.1.3
14:05 &lt;jrandom&gt; the release came out the other day and its been.. well... largely like before
14:05 &lt;jrandom&gt; working good enough for most things, but not as reliable as we'd like
14:06 &lt;jrandom&gt; throughput is still low, but thats a know issue to be dealt with in 0.4.2
14:06 &lt;jrandom&gt; as mentioned in the email, I dont expect there to be any more 0.4.1.* releases
14:07 &lt;jrandom&gt; I dont have much more to say on that - anyone have any comments / concerns?
14:07 &lt;deer_&gt; &lt;newsbyte&gt; yes: what about the freeze-up?
14:09 &lt;jrandom&gt; I'm not going to discount the possibility that your machine hung due to I2P, but I severely doubt it
14:09 &lt;jrandom&gt; no one else has ever reported that happening on any platform
14:09 &lt;deer_&gt; &lt;newsbyte&gt; well...it must be related to it somehow, if not directly, IMHO
14:09 &lt;deer_&gt; &lt;newsbyte&gt; maybe the java?
14:10 &lt;jrandom&gt; you're on 1.5 on w2k?
14:10 &lt;jrandom&gt; or 1.4.2_05?
14:10 &lt;deer_&gt; &lt;newsbyte&gt; nope, 1.5
14:10 &lt;jrandom&gt; ok
14:10 &lt;deer_&gt; &lt;newsbyte&gt; I can't exclude it's something else, ofcourse
14:11 &lt;deer_&gt; &lt;newsbyte&gt; could be coincidence it happend two times
14:11 &lt;jrandom&gt; well, we can discuss further how to find out the cause after the meeting if you'd like
14:11 &lt;deer_&gt; &lt;newsbyte&gt; but the last time..I dunno...nothing much else was running, then
14:11 &lt;deer_&gt; &lt;dinoman&gt; 1.5 on w2k works good for me :)
14:11 &lt;deer_&gt; &lt;newsbyte&gt; indeed, though
14:11 &lt;deer_&gt; &lt;newsbyte&gt; isn't there a simple debug log or something?
14:11 &lt;jrandom&gt; if it happens again, please send me wrapper.log and logs/log-router-*.txt
14:11 &lt;deer_&gt; &lt;newsbyte&gt; that might be usefull when it freezes
14:11 &lt;jrandom&gt; there are more logs than dirt ;)
14:12 &lt;jrandom&gt; ok cool dinoman
14:12 &lt;jrandom&gt; perhaps it was some interaction with your software firewall
14:12 &lt;deer_&gt; &lt;newsbyte&gt; maybe
14:12 &lt;jrandom&gt; but, yeah,bounce me logs if it happens again
14:12 &lt;jrandom&gt; (please :)
14:12 &lt;deer_&gt; &lt;newsbyte&gt; well, that  it would get blocked, I would understand
14:12 &lt;deer_&gt; &lt;newsbyte&gt; but a total freeze...dunno...was creepy
14:13 &lt;deer_&gt; &lt;newsbyte&gt; on the bright side: I've 27/63 now
14:13 &lt;jrandom&gt; great
14:13 &lt;jrandom&gt; ok, anyone else have any questions/comments/concerns with 0.4.1.3?
14:13 &lt;deer_&gt; &lt;newsbyte&gt; I'll guees I'll ask Whoo to guide my through the eep thingy
14:13 &lt;deer_&gt; &lt;dinoman&gt; just don't use it with Sygate Personal Firewall bad bad
14:13 &lt;deer_&gt; &lt;newsbyte&gt; why?
14:14 &lt;deer_&gt; &lt;dinoman&gt; crash
14:14 &lt;deer_&gt; &lt;newsbyte&gt; yes; you forgot 6) profit!!
14:14 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:14 &lt;deer_&gt; &lt;newsbyte&gt; crash?
14:14 &lt;deer_&gt; &lt;newsbyte&gt; ermm
14:14 &lt;jrandom&gt; dinoman: it crashes your OS?  the firewall?  I2P?
14:14 &lt;deer_&gt; &lt;newsbyte&gt; well, wouldn't that explain it, then? ;-)
14:15 &lt;jrandom&gt; newsbyte: are you running Sygate Personal Firewall?
14:15 &lt;deer_&gt; &lt;newsbyte&gt; indeed
14:15 &lt;deer_&gt; &lt;newsbyte&gt; well, not on my router
14:15 &lt;deer_&gt; &lt;newsbyte&gt; but on the puter, yes
14:15 &lt;deer_&gt; &lt;newsbyte&gt; seems we're on to something
14:16 &lt;deer_&gt; &lt;DrWoo&gt; newsbyte: /join #i2p-chat so jrandom can get through his meeting
14:16 &lt;deer_&gt; &lt;newsbyte&gt; though it doesn't crash/freeze immediately, apperently
14:16 &lt;deer_&gt; &lt;dinoman&gt; os it crashes windows
14:16 &lt;deer_&gt; &lt;newsbyte&gt; ?
14:16 &lt;deer_&gt; &lt;newsbyte&gt; jrand is already here
14:16 &lt;deer_&gt; &lt;dinoman&gt; sorry looked away
14:16 &lt;jrandom&gt; ok, perhaps we can look into what SPF is b0rking on
14:16 &lt;jrandom&gt; if there's nothing else on 0.4.1.3, moving on to 2) Tunnel test time, and send processing time
14:17 &lt;jrandom&gt; there was some discussion yesterday exploring some of the timeouts, and basically things just occationally take too long
14:17 &lt;jrandom&gt; i dont think the spikes you can see in http://dev.i2p.net/~jrandom/processingTime.png are legitimate though
14:18 &lt;jrandom&gt; well, they're real - it really does take that long
14:18 &lt;jrandom&gt; what i mean is, we should be able to get rid of them
14:18 &lt;jrandom&gt; some queueing is going to happen, but if we are more careful with what we accept, we should be able to reduce it
14:19 &lt;jrandom&gt; the delays are also likely due to some occational spikes in job processing time, which we can tune the fsck out of
14:20 &lt;jrandom&gt; in general though, the message queueing seems all right, even if it spikes up some tunnel tests
14:20 &lt;deer_&gt; &lt;newsbyte&gt; darn..I wish freenet and i2p could really merge...seems like progress would be a lot faster, possibly beneficial to both
14:20 &lt;deer_&gt; &lt;Ragnarok&gt; yeah, I don't see why fsck would be useful for jon processing :)
14:20 &lt;deer_&gt; &lt;Ragnarok&gt; s/jon/job/
14:21 &lt;jrandom&gt; there is much potential for collaboration, but the two projects have very different aims
14:21 &lt;jrandom&gt; !thwap Ragnarok
14:21 &lt;deer_&gt; &lt;newsbyte&gt; ermm
14:21 &lt;jrandom&gt; oh, one thing I mentioned yesterday 
14:21 &lt;deer_&gt; &lt;newsbyte&gt; I don't think the projects' goals, however, are all that different...
14:22 &lt;deer_&gt; &lt;DrWoo&gt; jrandom: technical goals
14:22 &lt;jrandom&gt; newsbyte: we can discuss that in 5) ??? or later if you prefer, we're on 2) right now
14:22 &lt;deer_&gt; &lt;DrWoo&gt; oops newsbyte: technical goals
14:22 &lt;deer_&gt; &lt;Ragnarok&gt; hehe
14:22 &lt;deer_&gt; &lt;newsbyte&gt; yes, and 3)profit! according to /. traditions!
14:22 &lt;deer_&gt; &lt;newsbyte&gt; :-)
14:22 &lt;deer_&gt; &lt;Demokritos&gt; I can't believe Tor is not backwards compatible from 0.0.8 to 0.0.8.1
14:23 &lt;jrandom&gt; with the tunnel testing, there is a floor to the test period - currently set to 5 seconds by default
14:23 &lt;jrandom&gt; the previous release had a hard limit of 30 seconds, but you can configure your own tunnel test time by updating http://localhost:7657/configadvanced.jsp and adding "router.tunnelTestMinimum=10000" (or whatever - that value is in milliseconds)
14:23 &lt;deer_&gt; &lt;newsbyte&gt; those seconds, are they alchimagical?
14:24 &lt;jrandom&gt; the 5s default should be fine though
14:24 &lt;deer_&gt; &lt;Demokritos&gt; I actually upgraded Tor the day before yesterday because it stopped working, and now the network is telling me again, I have a non compatible version... what the.. 
14:24 &lt;deer_&gt; &lt;Demokritos&gt; oh... hello everyone :)
14:24 &lt;jrandom&gt; newsbyte: the tunnel test time is MAX(avgTunnelTestTime*2, minTunnelTestTime)
14:25 &lt;jrandom&gt; (we have the minTunnelTestTime because otherwise a series of fast tests could cause a cascading failure)
14:26 &lt;jrandom&gt; more details can be found in http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD
14:26 &lt;deer_&gt; &lt;newsbyte&gt; hmm
14:26 &lt;deer_&gt; &lt;Demokritos&gt; this is really funny... a job agency wants me to use Internet Explorer, otherwise I'm not able to register an application
14:27 &lt;jrandom&gt; *cough* y'all realize these meeting logs go on the web, right?  :)
14:27 &lt;deer_&gt; &lt;Demokritos&gt; &lt;-- not too good in english
14:27 &lt;deer_&gt; &lt;newsbyte&gt; they do?!
14:27 &lt;deer_&gt; &lt;newsbyte&gt; Hi mum!
14:27 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:27 &lt;deer_&gt; &lt;Demokritos&gt; um, sorry. .I'm disturbing the meeting.. I'm off
14:28 &lt;jrandom&gt; naw, please stay, but discuss i2p stuff ;)
14:28 &lt;deer_&gt; &lt;newsbyte&gt; don't worry; disturbing is an art, just keep an eye on me, and you'll learn
14:28 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:28 &lt;jrandom&gt; ok, anything else on 2) Tunnel test time, and send processing time ?
14:28 &lt;deer_&gt; &lt;Ragnarok&gt; focus people
14:29 -!- znation [~znation@ip68-226-31-250.tc.ph.cox.net] has quit [Read error: 60 (Operation timed out)]
14:29 &lt;jrandom&gt; if not, moving on to 3) Streaming lib
14:29 &lt;jrandom&gt; as mentioned in the status notes, lots of progress
14:29 -!- znation [~znation@ip68-226-31-250.tc.ph.cox.net] has joined #i2p
14:29 &lt;deer_&gt; &lt;newsbyte&gt; done by you?
14:29 &lt;jrandom&gt; still not there yet, but I hope to be doing some live tests in the next week
14:30 &lt;jrandom&gt; i've been working on the streaming lib, yeah
14:30 &lt;jrandom&gt; i finally got it ping()ing earlier today ;)
14:30 &lt;deer_&gt; &lt;Ragnarok&gt; nice :)
14:31 &lt;jrandom&gt; ok, i dont really have anything else to add about that
14:31 &lt;jrandom&gt; anyone have any questions / comments / concerns?
14:31 &lt;deer_&gt; &lt;newsbyte&gt; ermm...speed?
14:31 &lt;jrandom&gt; speed is fine
14:31 &lt;deer_&gt; &lt;baffled&gt; what type of speed up/through put do you expect?
14:31 &lt;jrandom&gt; i expect significant throughput improvements
14:32 &lt;deer_&gt; &lt;newsbyte&gt; he expects a fine, he said
14:32 &lt;deer_&gt; &lt;newsbyte&gt; for speeding
14:32 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:32 &lt;jrandom&gt; in addition, for small request/response connections, the latency will be dramatically reduced
14:32 &lt;jrandom&gt; (cut in half)
14:32 &lt;deer_&gt; &lt;dinoman&gt; wow
14:32 &lt;deer_&gt; &lt;dinoman&gt; is that using udp?
14:33 &lt;jrandom&gt; the new lib exposes all the neat tunable parameters for normal TCP stacks too, so apps will be able to tweak out their own setup
14:33 &lt;jrandom&gt; no dinoman, this works on top of i2p's I2CP
14:33 &lt;deer_&gt; &lt;dinoman&gt; wow x2
14:33 &lt;jrandom&gt; (though we'll be writing similar code in a month or so to get the UDP transport..)
14:34 &lt;jrandom&gt; but, well, we'll see.
14:34 &lt;deer_&gt; &lt;newsbyte&gt; because...?
14:34 &lt;jrandom&gt; there's still a lot of work to do
14:34 &lt;jrandom&gt; because what?
14:34 &lt;deer_&gt; &lt;newsbyte&gt; well, can't tcp do it as well?
14:35 &lt;jrandom&gt; oh, why we're going to go UDP?  http://www.i2p.net/todo#transport
14:35 &lt;deer_&gt; &lt;newsbyte&gt; I remember the same discussion on freenet too, but they sticked to tcp as yet
14:35 &lt;jrandom&gt; plus TCP is a general purpose streaming transport - we can dramatically simplify it, since we can put up with a certain degree of out of order
14:35 &lt;deer_&gt; &lt;newsbyte&gt; not that all decisions they make are good ;-)
14:36 &lt;jrandom&gt; newsbyte: i've followed those discussions and we're going to go udp
14:36 &lt;jrandom&gt; (that doesnt mean freenet is wrong - they've got different constraints)
14:37 &lt;deer_&gt; &lt;Ragnarok&gt; i2p should not be compared too closely to freenet.  They're very different technically.
14:37 &lt;deer_&gt; &lt;newsbyte&gt; (or: they ARE wrong ;-)
14:37 &lt;jrandom&gt; i dont think their use of TCP right now is wrong, just as I dont think I2P's previous use of TCP is wrong.  progress requires small steps
14:38 &lt;deer_&gt; &lt;mule_iip&gt; newsbyte makes sure the meetings don't get too short
14:38 &lt;jrandom&gt; heh
14:38 &lt;deer_&gt; &lt;newsbyte&gt; yeah, nothing worse then short meetings
14:38 &lt;deer_&gt; &lt;newsbyte&gt; you can't eat all the popcorn and drink all the beer, then
14:38 &lt;jrandom&gt; ok, anything else on 3) Streaming lib ?
14:39 &lt;jrandom&gt; if not, 4) files.i2p
14:39 &lt;deer_&gt; &lt;Ragnarok&gt; I think we're cool
14:39 &lt;deer_&gt; &lt;newsbyte&gt; well, I know I am
14:39 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:39 &lt;deer_&gt; &lt;newsbyte&gt; and funny too
14:39 &lt;deer_&gt; &lt;newsbyte&gt; most of the time
14:39 &lt;deer_&gt; &lt;newsbyte&gt; and also annoying
14:39 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:39 &lt;jrandom&gt; well, i just wanted to point out files.i2p - a new search engine on i2p
14:40 &lt;deer_&gt; &lt;newsbyte&gt; ah, I see
14:40 &lt;deer_&gt; &lt;newsbyte&gt; I was hoping it would be about putting eepsites up
14:40 &lt;jrandom&gt; one interesting thing to note is that you can reach eepsites that aren't up anymore with it, since it caches
14:41 &lt;deer_&gt; &lt;baffled&gt; does it cache everything?
14:41 &lt;deer_&gt; &lt;newsbyte&gt; all searchengines thusfar are server-side?
14:41 &lt;deer_&gt; &lt;Ragnarok&gt; interesting.  Shouldn't be too hard, these days :).
14:41 &lt;jrandom&gt; baffled: caches text/html from what i can tell
14:42 &lt;deer_&gt; &lt;mule_iip&gt; at least it has limits on file size and types, so won't cache movies
14:42 &lt;deer_&gt; &lt;baffled&gt; Auh, that's what I thought not binary.
14:42 &lt;deer_&gt; &lt;newsbyte&gt; I mean, they are not in js, I suppose?
14:43 &lt;jrandom&gt; it uses nutch if anyone wants to look into it further.  or i'm sure we'll get the site author to put up a feedback form or something ;)
14:43 &lt;jrandom&gt; newsbyte: correct, this is just a normal website hosted anonymously
14:43 &lt;jrandom&gt; the site contains a search engine (like google)
14:44 &lt;jrandom&gt; anyway, i just wanted to mention it
14:44 &lt;jrandom&gt; there have also been a lot of blogs popping up lately, which imho is really cool
14:44 &lt;jrandom&gt; my 'eep' bookmark folder almost fills a screen :)
14:44 &lt;deer_&gt; &lt;Ragnarok&gt; hehe, myi2p is happening all by itself :)
14:45 &lt;jrandom&gt; you just have to bring up the sore points, dont ya ragnarok?  ;)
14:45 &lt;deer_&gt; &lt;Ragnarok&gt; sorry :)
14:46 &lt;jrandom&gt; ok, anyone have any questions/comments/concerns wrt files.i2p?
14:46 &lt;jrandom&gt; if not, let me move on to 4.1) biff
14:46  * jrandom almost forgot biff
14:46 &lt;jrandom&gt; postman, you arond?
14:47 &lt;deer_&gt; &lt;newsbyte&gt; I think he's biffed up
14:47 &lt;jrandom&gt; well, if not, biff is this new kickass mail notification bot
14:47 &lt;jrandom&gt; if you've got an email acct at mail.i2p, you can tell biff to notify you when you get new mail
14:47 &lt;deer_&gt; &lt;newsbyte&gt; does it has archives?
14:48 &lt;jrandom&gt; newsbyte: biff is just a notification bot, the mail is stored on the mail server (and accessed with your normal mail reader - kmail, etc)
14:48 &lt;jrandom&gt; see http://www.postman.i2p/
14:49 &lt;jrandom&gt; ok, so, yeah, go to the eepsite or check out #mail.i2p over there
14:49 &lt;deer_&gt; &lt;newsbyte&gt; I will, as soon as I get my eepsite on
14:49  * jrandom doesnt really know much more wrt biff - redirect any questions to postman
14:50 &lt;jrandom&gt; instead, we can move on to 5) ???
14:50 &lt;deer_&gt; &lt;newsbyte&gt; indeed
14:50 &lt;jrandom&gt; does anyone have anything else they want to bring up?
14:50 &lt;deer_&gt; * mule_iip raising hand to get voice: would like to recall my persistent FCP over I2P problems. but probably that can wait and will automagically be solved by 0.4.2.
14:50 &lt;deer_&gt; &lt;newsbyte&gt; yes, and the freeze
14:50 &lt;jrandom&gt; i hope so mule_iip
14:50 &lt;deer_&gt; &lt;mule_iip&gt; ok, will be your test platform :)
14:50 &lt;jrandom&gt; newsbyte: is there anything we need to discuss about it?  could you just email me your logs if it happens again?
14:51 &lt;jrandom&gt; ooh mule, that'd rule
14:51  * jrandom will definitelytake you up on that
14:51 &lt;deer_&gt; &lt;newsbyte&gt; well...can i still send those, if everything is frozen?
14:51 &lt;jrandom&gt; the files are written to disk.  
14:51 &lt;jrandom&gt; when you restart, send me the logs
14:51 &lt;deer_&gt; &lt;newsbyte&gt; I mean, in that case, I could send it now, since they should be somewhere 
14:51 &lt;jrandom&gt; (please)
14:51 &lt;deer_&gt; &lt;dinoman&gt; i was in the forum and see that the jabber service is gone. was thaat of us to anyone if it was i would like to run one if it would be cool?
14:51 &lt;jrandom&gt; the files rotate though newsbyte
14:52 &lt;jrandom&gt; duck and demonic_1 have had jabber servers at various times, but it seems most of the i2p IM activity has been on irc
14:52 &lt;deer_&gt; &lt;newsbyte&gt; the files rotate? surely it stores quite some data before it starts deleting?
14:53 &lt;jrandom&gt; newsbyte: ok, send me your logs, maybe it has something in it
14:53 &lt;deer_&gt; &lt;newsbyte&gt; good
14:53 &lt;deer_&gt; &lt;newsbyte&gt; ermm
14:54 &lt;deer_&gt; &lt;newsbyte&gt; darn
14:54 &lt;deer_&gt; &lt;newsbyte&gt; a lot of .logs
14:54 &lt;deer_&gt; &lt;dinoman&gt; ok
14:54 &lt;deer_&gt; &lt;newsbyte&gt; a noob is never gonna follow this
14:54 &lt;deer_&gt; &lt;newsbyte&gt; I guess you're right in not making a /. article yet
14:55 &lt;jrandom&gt; we're in no rush
14:55 &lt;deer_&gt; &lt;newsbyte&gt; log-router.txt?
14:55 &lt;jrandom&gt; wrapper.log and logs/log-router-*.txt
14:56 &lt;deer_&gt; &lt;newsbyte&gt; and the mailaddy to use would be...?
14:56 &lt;deer_&gt; &lt;fidd&gt; dinoman, a jabber server would be cool imo
14:56 &lt;jrandom&gt; jrandom@i2p.net
14:56 &lt;deer_&gt; &lt;newsbyte&gt; accessible by i2p, I hope?
14:56 &lt;deer_&gt; &lt;newsbyte&gt; ;-)
14:56 &lt;jrandom&gt; newsbyte: you can put your logs on your eepsite and msg me the url
14:57 &lt;jrandom&gt; or you can send mail to jrandom@mail.i2p
14:57 &lt;deer_&gt; &lt;newsbyte&gt; indeed!
14:57 &lt;deer_&gt; &lt;newsbyte&gt; a good idea!
14:57 &lt;deer_&gt; &lt;newsbyte&gt; there is only one little problem with it: It's not up yet
14:57 &lt;jrandom&gt; ok, anyone else have anything they want to bring up?
14:57 &lt;jrandom&gt; well, we can work on that newsbyte
14:57 &lt;jrandom&gt; (after the meeting)
14:59 &lt;deer_&gt; &lt;newsbyte&gt; thnks, but whoo is already helping
14:59 &lt;jrandom&gt; if there's nothing else...
14:59 &lt;deer_&gt; &lt;newsbyte&gt; we need a detailed howto/wiki/helpsite/something, though
14:59  * jrandom winds up
14:59 &lt;deer_&gt; &lt;Jake_&gt; i'd like to say, for the meeting, if a public release of i2p can be made before the u.s. election on november 2nd, this would go a long way to helping ensure a stable democracy 
14:59 &lt;deer_&gt; &lt;newsbyte&gt; what about 6)?
14:59 &lt;jrandom&gt; newsbyte: would you like to work on that?
15:00 &lt;jrandom&gt; newsbyte: i do agree it'd be great to get some more howtos and help info
15:00 &lt;deer_&gt; &lt;Ragnarok&gt; 6) There is no.... number 6
15:00 &lt;deer_&gt; &lt;newsbyte&gt; well, yeah, sort of, but it's a strange thing, with me
15:00 &lt;deer_&gt; &lt;newsbyte&gt; I'm pro-wiki and public thingy and free for everyone and all that
15:00 &lt;deer_&gt; &lt;newsbyte&gt; but my ego protests and wants minimal control
15:00 &lt;jrandom&gt; great
15:00 &lt;deer_&gt; &lt;newsbyte&gt; go figger
15:00 &lt;jrandom&gt; heh
15:01 &lt;jrandom&gt; well, if you'd like to make your own eepsite into a wiki you control, that'd be great too
15:01 &lt;deer_&gt; &lt;newsbyte&gt; indeed
15:01 &lt;jrandom&gt; though ugha.i2p has a pretty good uptime
15:01 &lt;deer_&gt; &lt;newsbyte&gt; I'll think about it
15:01 &lt;jrandom&gt; cool
15:02 &lt;deer_&gt; &lt;newsbyte&gt; 6 would be the freenet-i2p thingy
15:02  * jrandom winds up 
15:02  * jrandom *baf*s the meeting closed 
&lt;/div&gt;
{% endblock %}
</div>
