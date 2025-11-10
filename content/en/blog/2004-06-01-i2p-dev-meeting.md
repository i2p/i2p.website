---
title: "I2P Dev Meeting - June 01, 2004"
date: 2004-06-01
author: "duck"
description: "I2P development meeting log for June 01, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Meeting Log

<div class="irc-log">
[22:59] &lt;duck&gt; Tue Jun  1 21:00:00 UTC 2004
[23:00] &lt;duck&gt; hi folks!
[23:00] &lt;mihi&gt; hi duck
[23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html
[23:00] &lt;duck&gt; my proposal:
[23:00] * Masterboy has joined #i2p

[23:00] &lt;duck&gt; 1) code progress
[23:00] &lt;duck&gt; 2) featured content
[23:00] &lt;duck&gt; 3) testnet status
[23:00] &lt;duck&gt; 4) bounties
[23:00] &lt;duck&gt; 5) ???
[23:00] &lt;Masterboy&gt; hi:)
[23:00] &lt;duck&gt; .
[23:01] &lt;duck&gt; since jrandom is off we'll have to do it ourself
[23:01] &lt;duck&gt; (I know that he is logging and verifying our independency)
[23:01] &lt;Masterboy&gt; no problem:P
[23:02] &lt;duck&gt; unless there are problems with the agenda I propose that we stick to it
[23:02] &lt;duck&gt; though there aint much that I can do if you dont :)
[23:02] &lt;duck&gt; .
[23:02] &lt;mihi&gt; ;)
[23:02] &lt;duck&gt; 1) code progress
[23:02] &lt;duck&gt; not much code submitted to cvs
[23:02] &lt;duck&gt; I did win the trophy this week: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus has no cvs account yet
[23:03] &lt;Masterboy&gt; and who did submit something?
[23:03] &lt;duck&gt; anybody doing any secret coding?
[23:03] * Nightblade has joined #I2P

[23:03] &lt;hypercubus&gt; BrianR was working on some stuff
[23:04] &lt;hypercubus&gt; i've got maybe 20% of the 0.4 installer hacked out
[23:04] &lt;duck&gt; hypercubus: if you have stuff then provide diffs and $dev will commit for you
[23:04] &lt;duck&gt; ofcourse the strict license agreements apply
[23:05] &lt;duck&gt; hypercubus: cool, any issues / things worth mentioning?
[23:06] &lt;hypercubus&gt; not yet, but i'll probably need a couple of BSD people to test the preinstaller shell scripts
[23:06] * duck turns some stones
[23:06] &lt;Nightblade&gt; is it text-only
[23:07] &lt;mihi&gt; duck: which one is you on duck_trophy.jpg?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk has freebsd, also my isp has freebsd but their config is kind of screwed up
[23:07] &lt;Nightblade&gt; my web host isp that is, not comcast
[23:08] &lt;duck&gt; mihi: left one with the glasses. wilde is the right guy handing me the trophy
[23:08] * wilde waves
[23:08] &lt;hypercubus&gt; you have a choice... if you have java installed, you can skip the preinstaller altogether... 
  if you don't have java installed you can run the linux binary or win32 binary preinstaller (console mode), or a 
  generic *nix script preinstaller (console mode)
[23:08] &lt;hypercubus&gt; the main installer gives you the choice of using console mode or spiffy GUI mode
[23:08] &lt;Masterboy&gt; i will install freebsd soon so in the future i will give a try to the installer too
[23:09] &lt;hypercubus&gt; ok good... didn't know if anyone else besides jrandom was using it
[23:09] &lt;Nightblade&gt; freebsd java is invoked as "javavm" rather than "java"
[23:09] &lt;hypercubus&gt; as built from sun sources?
[23:09] &lt;mihi&gt; freebsd supports symlinks ;)
[23:10] &lt;hypercubus&gt; anyhow the binary preinstaller is 100% complete
[23:10] &lt;hypercubus&gt; compiles with gcj to native
[23:11] &lt;hypercubus&gt; it just asks you for the install dir, and it grabs a JRE for you
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; cool
[23:11] &lt;hypercubus&gt; jrandom's packaging a custom JRE for i2p

[23:12] &lt;deer&gt; &lt;j&gt; .
[23:12] &lt;Nightblade&gt; if you install java from the freebsd ports collection you use some wrapper script called 
  javavm
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;hypercubus&gt; anyhow this puppy will be almost completely automated
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;duck&gt; r: cut it
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;m&gt; .
[23:13] &lt;deer&gt; &lt;m&gt; stoopid irc server, does not support pipelining :(
[23:13] &lt;duck&gt; hypercubus: got any ETA for us?
[23:14] &lt;deer&gt; &lt;m&gt; oops, the problem is "Nick change too fast" :(
[23:14] &lt;hypercubus&gt; i still expect to be finished in under a month, before 0.4 is ripe for release
[23:14] &lt;hypercubus&gt; though at present i'm compiling a new OS for my dev system, so it'll be a couple of days 
  before i get back to the installer ;-)
[23:14] &lt;hypercubus&gt; no worries though
[23:15] &lt;duck&gt; ok. so more news next week :)
[23:15] &lt;duck&gt; any other coding done?
[23:15] &lt;hypercubus&gt; hopefully... unless the power company screws me again
[23:16] * duck moves to #2
[23:16] &lt;duck&gt; * 2) featured content
[23:16] &lt;duck&gt; lots of streaming audio (ogg/vorbis) done this week
[23:16] &lt;duck&gt; baffled is running his egoplay stream and I am running a stream too
[23:16] &lt;Masterboy&gt; and it works quite good
[23:17] &lt;duck&gt; on our site you can get info how to use it
[23:17] &lt;hypercubus&gt; got any rough stats for us?
[23:17] &lt;duck&gt; if you use a player not listed there and figure out how to use it, please send them to me and I'll 
  add
[23:17] &lt;Masterboy&gt; duck where is the link to baffleds stream on your site?
[23:17] &lt;Masterboy&gt; :P
[23:17] &lt;duck&gt; hypercubus: 4kB/s goes pretty well
[23:18] &lt;duck&gt; and with ogg it aint tooooo bad
[23:18] &lt;hypercubus&gt; but that still seems to be the avg. speed?
[23:18] &lt;duck&gt; my observation is that is the max
[23:18] &lt;duck&gt; but it is all config tweaking
[23:19] &lt;hypercubus&gt; any idea why that seems to be the max?
[23:19] &lt;hypercubus&gt; and i'm not just talking streaming here
[23:19] &lt;hypercubus&gt; but downloads too
[23:20] &lt;Nightblade&gt; i was downloading some big files yesterday (a couple megabytes) off of duck's hosting 
  service and i was getting about 4kb-5kb as well
[23:20] &lt;duck&gt; I think that it is the rtt
[23:20] &lt;Nightblade&gt; those Chips movies
[23:20] &lt;hypercubus&gt; 4-5 seems an improvement over the ~3 that i've gotten consistently since i started using i2p

[23:20] &lt;Masterboy&gt; 4-5kb is not bad..
[23:20] &lt;duck&gt; with a windowsize of 1 you dont get much faster..
[23:20] &lt;duck&gt; windowsize&gt;1 bounty: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: maybe you can comment?
[23:21] &lt;hypercubus&gt; but it is a remarkably consistent 3 kbps
[23:21] &lt;mihi&gt; on what? windowsize&gt;1 with ministreaming: you are a wizard if you manage that ;)
[23:21] &lt;hypercubus&gt; no hiccups on the bandwidth meter... a fairly smooth line
[23:21] &lt;duck&gt; mihi: on why it is so stable at 4kb/s
[23:21] &lt;mihi&gt; no idea. i don't hear any sound :(
[23:22] &lt;duck&gt; mihi: for all i2ptunnel transfers
[23:22] &lt;Masterboy&gt; mihi you need to config the ogg streaming plugin..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; no, there is no limit inside i2ptunnel regarding speed. it must be in the router...
[23:23] &lt;duck&gt; my thinking: max packet size: 32kB, 5 second rtt: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; sounds plausible
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; other content:
[23:25] * hirvox has joined #i2p

[23:25] &lt;duck&gt; there is a new eepsite from Naughtious
[23:25] &lt;duck&gt; anonynanny.i2p
[23:25] &lt;duck&gt; key is commited to cvs and he did put it on ugha's wiki
[23:25] * mihi is hearing "sitting in the ..." - duck++
[23:25] &lt;Nightblade&gt; see if you can open two or three streams at a 4kb speed then you will be able to tell if it 
  is in the router or the streaming lib
[23:26] &lt;duck&gt; Naughtious: you there? tell something about your plan :)
[23:26] &lt;Masterboy&gt; i have read that he provides hosting
[23:26] &lt;duck&gt; Nightblade: I did try 3 parallel downloads from baffled and I got 3-4kB each
[23:26] &lt;Nightblade&gt; i c
[23:27] &lt;mihi&gt; Nightblade: how can you tell that then?
[23:27] * mihi likes listening in "stop&go" mode ;)
[23:27] &lt;Nightblade&gt; well if there is some kind of limitation in the router that only lets it handle 4kb at once
[23:27] &lt;Nightblade&gt; or if it is something else
[23:28] &lt;hypercubus&gt; can someone explain this anonynanny site? i don't have a running i2p router atm
[23:28] &lt;mihi&gt; hypercubus: just a wiki or some sort of it
[23:28] &lt;duck&gt; plone CMS setup, open account creation
[23:28] &lt;duck&gt; allows file upload and website stuff
[23:28] &lt;duck&gt; through web interface
[23:28] &lt;Nightblade&gt; another thing to do would be to test the throughput of the "repliable datagram" which afaik 
  is the same as the streams but without acks
[23:28] &lt;duck&gt; likely a lot like drupal
[23:28] &lt;hypercubus&gt; yeah i've run plone before
[23:29] &lt;duck&gt; Nightblade: I have been thinking about using airhook to manage those
[23:29] &lt;duck&gt; but so far only some basic thought
[23:29] &lt;hypercubus&gt; anything goes for the wiki content, or does it center on something in particular?
[23:29] &lt;Nightblade&gt; i think airhook is GPLed
[23:29] &lt;duck&gt; the protocol
[23:29] &lt;duck&gt; not the code
[23:29] &lt;Nightblade&gt; ah :)
[23:30] &lt;duck&gt; hypercubus: he wants quality content, and lets you provide that :)
[23:30] &lt;Masterboy&gt; upload the best pr0n of yourself you have got hyper;P
[23:30] &lt;duck&gt; ok
[23:30] * Masterboy will try to do that too
[23:30] &lt;hypercubus&gt; yeah, anyone running an open wiki is just asking for quality content ;-)
[23:31] &lt;duck&gt; ok
[23:31] * duck moves to #3
[23:31] &lt;duck&gt; * 3) testnet status
[23:31] &lt;Nightblade&gt; Airhook gracefully handles intermittent, unreliable, or delayed networks  &lt;-- hehe not an 
  optimistic description of I2P!
[23:31] &lt;duck&gt; how has it been going?
[23:32] &lt;duck&gt; lets put the datagram over i2p discussion to the end
[23:32] &lt;tessier&gt; I love to run around to open wiki's and link to this: http://www.fissure.org/humour/pics/squirre
  l.jpg
[23:32] &lt;tessier&gt; airhook rocks
[23:32] &lt;tessier&gt; I've been looking at it for building a p2p network also.
[23:32] &lt;Nightblade&gt; it seems to be reliable to me (#3)
[23:32] &lt;Nightblade&gt; best i've seen so far
[23:33] &lt;duck&gt; yeah
[23:33] &lt;mihi&gt; works well - at least for stop&go audio streaming
[23:33] &lt;duck&gt; I see quite impressive uptimes on irc
[23:33] &lt;hypercubus&gt; agreed... seeing lots more blue guys in my router console
[23:33] &lt;Nightblade&gt; mihi: are you listening to techno ? :)
[23:33] &lt;duck&gt; but hard to tell since bogobot doesnt seem to handle connections that go over 00:00
[23:33] &lt;tessier&gt; audio streaming works great for me but loading websites often takes a number of tries
[23:33] &lt;Masterboy&gt; i have an opinion that i2p runs very good after 6 hours of use in the 6th hour i used the irc 
  for 7 hours and so my router was running for 13hours
[23:33] &lt;duck&gt; (*hint*)
[23:34] &lt;hypercubus&gt; duck: er... heheh
[23:34] &lt;hypercubus&gt; i could fix that i guess
[23:34] &lt;hypercubus&gt; do you have the logging set for daily?
[23:34] &lt;duck&gt; hypercubus++
[23:34] &lt;hypercubus&gt; log rotation that is
[23:34] &lt;duck&gt; oh yes
[23:34] &lt;duck&gt; duck--
[23:34] &lt;hypercubus&gt; that's why
[23:34] &lt;Nightblade&gt; I was at work all day and turned on my computer and started i2p and was on duck's irc server 
  in just a few minutes
[23:35] &lt;duck&gt; I have been seeing some weird DNFs
[23:35] &lt;duck&gt; even when connecting to my own eepsites
[23:35] &lt;duck&gt; (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] &lt;duck&gt; I think that is what causes most problems now
[23:35] &lt;hypercubus&gt; bogoparser will only analyze uptimes that occur wholly within a single logfile... so if the 
  logfile encompasses only 24 hours, nobody will show up as connected longer than 24 hours
[23:35] &lt;duck&gt; Masterboy and ughabugha did also have it I think...
[23:36] &lt;Masterboy&gt; yup
[23:36] &lt;duck&gt; (fix it and you will win next weeks trophy for sure!)
[23:37] &lt;deer&gt; &lt;mihi&gt; bogobot is excited? ;)
[23:37] &lt;Masterboy&gt; i tried my web site and sometimes when i hit refresh it takes the other route? and i have to 
  wait for it to load but i never wait;P i hit it again and it shows instantly
[23:37] &lt;deer&gt; &lt;mihi&gt; oops, sry. forgot that this is gated...
[23:38] &lt;duck&gt; Masterboy: do the timeouts take 61 seconds?
[23:39] &lt;duck&gt; mihi: bogobot set to weekly rotations now
[23:39] * mihi has quit IRC ("bye, and have a nice meeting")
[23:40] &lt;Masterboy&gt; sorry i didn't check it on my web site when i can't reatch it instantly i just hit refresh 
  and it loads instantly..
[23:40] &lt;duck&gt; hm
[23:40] &lt;duck&gt; well, it needs to be fixed
[23:41] &lt;duck&gt; .... #4
[23:41] &lt;Masterboy&gt; i think the route is given not the same eatch time
[23:41] &lt;duck&gt; * 4) bounties
[23:41] &lt;duck&gt; Masterboy: local connections should be cutted short
[23:42] &lt;duck&gt; wilde had some bounty thoughts... you there?
[23:42] &lt;Masterboy&gt; maybe it is a peer selection bug
[23:42] &lt;wilde&gt; I'm not sure that was for the agenda really
[23:42] &lt;duck&gt; oh
[23:42] &lt;wilde&gt; ok but the thoughts were something like:
[23:42] &lt;Masterboy&gt; i think then we go public the bounty system will work better
[23:43] &lt;Nightblade&gt; masterboy: yes there are two tunnels for each connection, or that is how i understand it 
  from reading the router.config
[23:43] &lt;wilde&gt; we could use this month to do some small advertising of i2p and increase the bounty pool a bit
[23:43] &lt;Masterboy&gt; i can see that the Mute project is going good - they got 600$ and they didn't code a lot yet;P
[23:44] &lt;wilde&gt; target against freedom communities, crypto people, etc
[23:44] &lt;Nightblade&gt; I don't think jrandom wants advertising
[23:44] &lt;wilde&gt; not public slashdot attention, no
[23:44] &lt;hypercubus&gt; that's what i've observed as well
[23:44] &lt;Masterboy&gt; i want to push it again - when we go public the system will work a lot better;P
[23:45] &lt;wilde&gt; Masterboy: bounties could speed up myi2p development for example
[23:45] &lt;Masterboy&gt; and as jr said no public till 1.0 and only some attention after 0.4
[23:45] &lt;Masterboy&gt; *wrote
[23:45] &lt;wilde&gt; when we have like $500+ for a bounty people could actually survive for some weeks
[23:46] &lt;hypercubus&gt; the tricky part is, even if we target a small dev community, like *cough* Mute devs, those 
  guys might spread the word about i2p further than we'd like
[23:46] &lt;Nightblade&gt; someone could make a career out of fixing i2p bugs
[23:46] &lt;hypercubus&gt; and too soon
[23:46] &lt;wilde&gt; i2p links are already in many public places
[23:46] &lt;Masterboy&gt; you google and you can find i2p

[23:47] &lt;hypercubus&gt; obscure public places ;-) (i saw the i2p link on a freesite... i'm lucky the damn freesite 
  even loaded!)
[23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p
[23:47] &lt;Masterboy&gt; but i agree that no advertising till 0.4 is done
[23:47] &lt;Masterboy&gt; wha???????
[23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] &lt;Masterboy&gt; protol0l does a great job;P
[23:48] &lt;Masterboy&gt; ;))))))
[23:48] &lt;hypercubus&gt; nice typo ;-)
[23:48] &lt;wilde&gt; ok anyway, I agree we should still keep I2P private (jr read this log ;)
[23:49] &lt;Masterboy&gt; who did that?
[23:49] &lt;Masterboy&gt; i think the Freenet crew discussion gave more attention..
[23:50] &lt;Masterboy&gt; and jr discussing with toad give a lot info to the big public..
[23:50] &lt;Masterboy&gt; so as in ughas wiki - we can all blame jr for that;P
[23:50] &lt;wilde&gt; ok anyway, we'll see if we can bring in some $ without bringing in /.
[23:50] &lt;Masterboy&gt; agreed
[23:50] &lt;hypercubus&gt; the freenet dev list is hardly what i call the "big public" ;-)
[23:50] &lt;wilde&gt; .
[23:51] &lt;hypercubus&gt; wilde: you'll have a lot of $ sooner than you think ;-)
[23:51] &lt;wilde&gt; oh come on, even my mum subscribe to freenet-devl
[23:51] &lt;duck&gt; my mum reads through gmame
[23:51] &lt;deer&gt; &lt;clayboy&gt; freenet-devl is being taught in schools here
[23:52] &lt;wilde&gt; .
[23:52] &lt;Masterboy&gt; so we will see more bounties after we go 0.4 stable..
[23:53] &lt;Masterboy&gt; that is after 2 months;P
[23:53] &lt;wilde&gt; where did that duck go?
[23:53] &lt;duck&gt; thanks wilde 
[23:53] &lt;hypercubus&gt; though as the only bounty claimant thus far, i have to say that the bounty money had no 
  bearing on my decision to take up the challenge
[23:54] &lt;wilde&gt; hehe, it would if it been 100x
[23:54] &lt;duck&gt; wyou are too good for the world
[23:54] &lt;Nightblade&gt; haha
[23:54] * duck moves to #5
[23:54] &lt;hypercubus&gt; wilde, $100 doesn't mean shit to me ;-)
[23:54] &lt;duck&gt; 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] &lt;duck&gt; tessier: got any real-world experience with it
[23:55] &lt;duck&gt; (http://www.airhook.org/)
[23:55] * Masterboy will try dis out:P
[23:56] &lt;duck&gt; java implementation (dunno if it even works) http://cvs.ofb.net/airhook-j/
[23:56] &lt;duck&gt; python implementation (a mess, did work in the past) http://cvs.sourceforge.net/viewcvs.py/khashmir
  /khashmir/airhook.py
[23:58] * duck opens the rant-valve
[23:58] &lt;Nightblade&gt; j one is also gpl
[23:58] &lt;duck&gt; port it to pubdomain
[23:58] &lt;hypercubus&gt; amen
[23:58] &lt;Nightblade&gt; the entire protocol doc is only about 3 pages - it can't be that hard
[23:59] &lt;Masterboy&gt; nothing is hard
[23:59] &lt;Masterboy&gt; it's just not easy
[23:59] &lt;duck&gt; I dont think that it is fully specced though
[23:59] * hypercubus takes away masterboy's fortune cookies
[23:59] &lt;duck&gt; you might need to dive into the C code for a reference implementation
[00:00] &lt;Nightblade&gt; I would do it myself but I am busy with other i2p stuff right now
[00:00] &lt;Nightblade&gt; (and also my full-time job)
[00:00] &lt;hypercubus&gt; duck: maybe a bounty for it?
[00:00] &lt;Nightblade&gt; there already is
[00:00] &lt;Masterboy&gt; ?
[00:00] &lt;Masterboy&gt; ahh Pseudonyms
[00:00] &lt;duck&gt; it could be used at 2 levels
[00:00] &lt;duck&gt; 1) as a transport besides TCP
[00:01] &lt;duck&gt; 2) as a protocol to handle datagrams inside i2cp/sam
[00:01] &lt;hypercubus&gt; that's worth serious consideration then
[00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: i noticed that the repliable datagram in SAM has a maximum size of 31kb, whereas the 
  stream has a maximum size of 32kb - making me think that the sender's destination is sent with each packet in 
  repliable datagram mode, and only at the beginning for a stream mode -
[00:02] &lt;Masterboy&gt; well airhook cvs is not very updated..
[00:03] &lt;Nightblade&gt; making me think that it would be inefficient to make a protocol on top of the repliable 
  datagrams through sam
[00:03] &lt;duck&gt; airhooks message size is 256 bytes, i2cp's is 32kb, so you need to atleast change a bit
[00:04] &lt;Nightblade&gt; actually if you wanted to do the protocol in SAM you could just use the anoymous datagram 
  and have the first packet contain the sender's destination.... blah blah blah - i have lots of ideas but not 
  enough time to code them
[00:06] &lt;duck&gt; then again you have to problems to verify signatures
[00:06] &lt;duck&gt; so someone could send fake packages to you
[00:06] &lt;Masterboy&gt; topic:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; true
[00:08] &lt;Nightblade&gt; but if you sent back to that destination and there was no acknowledgement you'd know it was 
  a faker
[00:08] &lt;Nightblade&gt; there woudl have to be a handshake
[00:08] &lt;duck&gt; but you'll need aapplication level handshakes for that
[00:08] &lt;Nightblade&gt; no not really
[00:09] &lt;Nightblade&gt; just put it in a library for accessing SAM
[00:09] &lt;Nightblade&gt; that is a bad way of doing though
[00:09] &lt;Nightblade&gt; doing it though
[00:09] &lt;duck&gt; you could also use seperated tunnels
[00:09] &lt;Nightblade&gt; it shuold be in the streaming lib
[00:11] &lt;duck&gt; yup. makes sense
[00:12] &lt;duck&gt; ok
[00:12] &lt;duck&gt; I am feeling *baff*-y
[00:13] &lt;Nightblade&gt; ja
[00:13] * duck *baffs*
</div>
