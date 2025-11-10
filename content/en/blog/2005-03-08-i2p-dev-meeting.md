---
title: "I2P Dev Meeting - March 08, 2005"
date: 2005-03-08
author: "@jrandom"
description: "I2P development meeting log for March 08, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, aum, bla, cervantes, detonate, duck, fedo, frosk, jrandom, legion, maestro^, mancom, named, postman, Ragnarok, septu_ssh</p>

## Meeting Log

<div class="irc-log">
13:06 &lt;@jrandom&gt; 0) hi
13:06 &lt;@jrandom&gt; 1) 0.5.0.2
13:06 &lt;@jrandom&gt; 2) mail.i2p updates
13:06 &lt;@jrandom&gt; 3) i2p-bt updates
13:06 &lt;legion&gt; so it's related to the irc servers?
13:06 &lt;@jrandom&gt; 4) ???
13:06 &lt;@jrandom&gt; 0) hi
13:06 &lt;@jrandom&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2005-March/000633.html
13:07 &lt;fedo&gt; hi
13:07 &lt;+postman&gt; hi
13:07 &lt;frosk&gt; goodday
13:07 &lt;@jrandom&gt; legion: no, related to i2p bugs, being worked on
13:07 &lt;bla&gt; hi
13:07 &lt;legion&gt; ok
13:07 &lt;@jrandom&gt; speaking bugs being worked on, lets jump on in to 1) 0.5.0.2 :)
13:07 &lt;cervantes&gt; 'lo
13:07 &lt;cervantes&gt; -- Disconnected
13:08 &lt;@jrandom&gt; heh
13:08 &lt;ant&gt; &lt;mihi&gt; hi all
13:08 &lt;@jrandom&gt; 0.5.0.2 is out, and while your irc connection may lag at times, it'll recover ;)
13:08 &lt;@jrandom&gt; woah heya mihi
13:09 &lt;cervantes&gt; hey mihi
13:09 &lt;@jrandom&gt; the status notes give a general overview of where things are and the most immediate priorities
13:10 &lt;@jrandom&gt; the scary thing I'm trying to track down can be seen on http://localhost:7657/oldstats.jsp#router.invalidMessageTime
13:10 &lt;bla&gt; As for me, I can say that 0.5.0.2 already improved realiability _vastly_ compared to 0.5.0.1: errors where destinations couldn't be contacted almost don't occur anymore 
13:10 &lt;@jrandom&gt; those numbers should be very very small, but they're not, unfortunately
13:10 &lt;@jrandom&gt; wikked bla 
13:11 &lt;@jrandom&gt; yeah, the 0.5.0.2 is definitely an improvement, and everyone should upgrade ASAP 
13:11 &lt;bla&gt; 375,932.22 in the last 10 minutes here....
13:11 &lt;@jrandom&gt; well, the particular value isn't really the problem, its their frequency
13:11 &lt;@jrandom&gt; (events per period)
13:12 &lt;@jrandom&gt; those messages can likely be attributed to 0.5 routers, and some of it to 0.5.0.1 routers, which is why I want people to upgrade ASAP
13:12 &lt;@jrandom&gt; it may be the case that its something else though, but I'd like to rule it out
13:12 &lt;bla&gt; jrandom: I get about 200 per hour here
13:13 &lt;@jrandom&gt; bla: i've currently got 93 this hour, but peak count much higher (thousands)
13:13 &lt;@jrandom&gt; anyway, this particular stat is published in the netdb
13:13 &lt;bla&gt; jrandom: How about excluding 0.5-0 from the net in software when releasing 0.5.0.3?
13:14 &lt;@jrandom&gt; so we can all look around and see what values other people have ;)
13:14 &lt;@duck&gt; 309,854.24 peak 5,473,314.59
13:15 &lt;@duck&gt; pasting the wrong one,  huh
13:15 &lt;@jrandom&gt; bla: definitely.  I added some code in the 0.5.0.2 rev to do soem forward compatability that 0.5.0.1 and 0.5 don't have
13:16 &lt;@jrandom&gt; duck: hard to have a nonintegral # of events ;)
13:16 &lt;bla&gt; jrandom: Good. At least that allows you to test your invalid-messages-are-due-to-0.5-0 hypothesis in a controlled manner
13:16 &lt;@jrandom&gt; bla: aye, though it'd be great if people updated before then ;)
13:17 &lt;@jrandom&gt; (so for those reading at home: http://www.i2p.net/download is your friend ;)
13:17 &lt;maestro^&gt; jr: those numbers for router.invalidMessageTime deviations in ms?
13:17 &lt;@jrandom&gt; maestro^: yes
13:18 &lt;@jrandom&gt; (aka some really insanely skewed values)
13:18 &lt;legion&gt; Here is a little network report [version|Number of nodes][0.5|6][0.5.0.1|39][0.5.0.2|107]
13:18 &lt;@jrandom&gt; yeah, y'all have been great about updating
13:18 &lt;legion&gt; So there is still a few people running 0.5 and many people running 0.5.0.1
13:18 &lt;maestro^&gt; so any idea where they might be lagging?
13:18 &lt;bla&gt; jrandom: Freenet has a flag in each release that specifies the minimum node version it will communicate with. Is the new forward-compat. code something like that?
13:19 &lt;@jrandom&gt; maestro^: many, many ideas for why 0.5 and 0.5.0.1 users are lagging.
13:19 &lt;@jrandom&gt; bla: similar
13:19 &lt;maestro^&gt; or is it clock drift on nodes?
13:20 &lt;@jrandom&gt; maestro^: clock skew, some serialization bugs, the 100% cpu bug
13:20 &lt;@jrandom&gt; ok, thats generally my focus atm, trying to get the message reliability back up
13:21 &lt;@jrandom&gt; anyone have any questions/comments/concerns on 0.5.0.2?
13:21 &lt;ant&gt; * mihi has a 0.4.2.5 router here on hd not started since dec 22th... but he thinks he'd better delete it...
13:21 &lt;@jrandom&gt; heh
13:21 &lt;@jrandom&gt; yeah, that wont talk to too many routers ;)
13:21  * postman got a backup copy of his last 0.4 installation :)
13:21 &lt;ant&gt; &lt;mihi&gt; question for me 'd be upgrade or delete.
13:22 &lt;@jrandom&gt; delete
13:22 &lt;@jrandom&gt; (backing up any destination keys)
13:22 &lt;@jrandom&gt; there is no upgrade procedure from pre-0.5 anymore
13:22 &lt;legion&gt; Perhaps releasing another update say 0.5.0.2-1 that only allows connections from 0.5.0.2 or newer, would be good?
13:22 &lt;@jrandom&gt; legion: that would segment the network
13:22 &lt;@jrandom&gt; people should juts upgrade.
13:23 &lt;@jrandom&gt; (and we should work around those that dont)
13:24 &lt;legion&gt; yeah until the people running outdated nodes updated ;)
13:24 &lt;@jrandom&gt; segmenting the network hurts us all, not just them
13:25 &lt;legion&gt; Maybe if there was a update notification in the router console or something that let them know they are running outdated versions?
13:25 &lt;@jrandom&gt; yeah, that'd certainly be pretty cool
13:25 &lt;@jrandom&gt; hopefully that can get tied in with the updater as well
13:26 &lt;legion&gt; yeah, I know, segmentation is bad...
13:26 &lt;@jrandom&gt; smeghead is working on some of the key components of that, though not sure if that includes the notification / download
13:26 &lt;@jrandom&gt; (so if anyone wants to help work on that, get in touch!)
13:27 &lt;@jrandom&gt; ok, movin' on to 2) mail.i2p updates
13:27 &lt;@jrandom&gt; postman: ping
13:27 &lt;+postman&gt; yes
13:27 &lt;bla&gt; jrandom: smeghead was doing some signing-related stuff IIRC (so that when you get an update notice, you at least know it's real, and not a phishing/spyware/crap thing)
13:28  * postman takes over the mike
13:28 &lt;legion&gt; hmm, maybe if there was a autoupdate feature built in, where updates would be downloaded through i2p and the nodes would simply download the update, then do a graceful restart.
13:28 &lt;@jrandom&gt; right bla
13:28 &lt;ant&gt; &lt;Gatak&gt; Oh, btw. Would I2P work behind nat even if you cannot open a port?
13:28 &lt;@jrandom&gt; Gatak: not yet.  some people will be able to at 0.6, others at 2.0
13:29 &lt;@jrandom&gt; legion: patches welcome
13:29 &lt;ant&gt; &lt;Gatak&gt; 2.0 heck, that is far on the future =)
13:29 &lt;@jrandom&gt; (http://www.i2p.net/roadmap#2.0 ;)
13:29 &lt;+postman&gt; erm, shall i start now?
13:29 &lt;aum&gt; morning all
13:30 &lt;@jrandom&gt; mic is all yours postman (sorry ;)
13:30 &lt;@jrandom&gt; 'lo aum, made it for the meeting
13:30 &lt;@jrandom&gt; (d'oh!  /me shuts up again)
13:30 &lt;cervantes&gt; Gatek: http://www.i2p.net/roadmap
13:30 &lt;+postman&gt; first, i wanted to say, that we reached 300 accounts registered at postman.i2p already
13:30 &lt;@jrandom&gt; w00t
13:30 &lt;+postman&gt; the number of mails from/to internet is growing steadily and once more proves that we need to move further
13:31 &lt;cervantes&gt; *squeeeel*
13:31 &lt;+postman&gt; after talking to jr some weeks ago we agreed upon the the release of v2mail together with I2P 1.0
13:31 &lt;+postman&gt; recent status is: the java based smtp proxy designed to run on every node is finished
13:31 &lt;@jrandom&gt; nice!
13:32 &lt;+postman&gt; the java based POP3 proxy is at 80% with just the maildir engine missing
13:32 &lt;+postman&gt; there will be a webmanager that needs some heavy tweaking still (15% done)
13:32 &lt;+postman&gt; the inter node communication is at 40% - we tested some datarecord exchanging with HTTP/XML
13:33 &lt;+postman&gt; seems to work quite well and fast even
13:33 &lt;+postman&gt; even if a relay node fails/was powered off for a few days, it'll be synced within a few minutes after going back onlione again
13:33 &lt;@jrandom&gt; wikked
13:33 &lt;+postman&gt; i think we're quite n track
13:34 &lt;+postman&gt; one thing is noteable
13:34 &lt;bla&gt; postman: Nice work man! One question: Many nodes cannot receive or send data on port 25 (not directly, anyway). Will node-owners be able to specify this (or will this be auto-detected)?
13:34 &lt;cervantes&gt; cool
13:34 &lt;+postman&gt; bla: later
13:34 &lt;+postman&gt; in v2mail there will be a locally run webapp
13:34 &lt;+postman&gt; with this you can manager your local proxies AND apply for an "relayaccount"
13:35 &lt;+postman&gt; this relayaccount will then be used to associate your addess/domain to the relays
13:35 &lt;+postman&gt; the relays will sync the information automatically
13:35 &lt;@jrandom&gt; cool
13:35 &lt;+postman&gt; even features like the addressbook / public keys and stuff will work with the LOCAL interface
13:36 &lt;+postman&gt; so the idea is to have one centralized manager where you can do all your mailstuff
13:36 &lt;+postman&gt; relevant data is transferred to ONE of the relays and then being synced between the relays
13:36 &lt;+postman&gt; and this webbased manager will run on your very node
13:37 &lt;+postman&gt; when your node is online, the relays will deliver mails queued for your destination/domain/address
13:37 &lt;+postman&gt; it will be delivered to your local smtp proxy
13:37 &lt;+postman&gt; you can even trigger the whole thing with ETRN :)
13:37 &lt;aum&gt; hi again
13:37 &lt;aum&gt; i'd like to raise a discussion point in this meeting, if it's ok
13:37 &lt;+postman&gt; so much for the future folks :)
13:37 &lt;+postman&gt; .
13:38 &lt;@jrandom&gt; sound bitchin postman 
13:38  * postman hands back the mike
13:38 &lt;@jrandom&gt; aum: great, should be some time at 4) 
13:38 &lt;+postman&gt; yeah, iam ecstatic :)
13:38 &lt;@jrandom&gt; postman: so for the normal user, the smtp proxy will have the local maildir, and the pop3 proxy will read/etc, right?
13:39 &lt;+postman&gt; yeah, the smtp proxy got a MDA
13:39 &lt;+postman&gt; and will deliver the mail into local maildirs
13:39 &lt;+postman&gt; even several accounts/users can be created locally
13:39 &lt;cervantes&gt; postman: will the relays keep track of your quotas etc and propogate such info between each other?
13:39 &lt;+postman&gt; and mapped to accounts of your domain
13:39 &lt;+postman&gt; cervantes: yes, they will
13:39 &lt;septu_ssh&gt; sorry, can I ask postman about payment/anti-spam mechanisms in the new model?
13:40 &lt;+postman&gt; septu_ssh: have you read any of the documents on the webpage?
13:40 &lt;+postman&gt; cervantes: it's not perfect real time
13:40 &lt;+postman&gt; cervantes: but i am fine with a few minutes update of quota information exchange
13:40 &lt;septu_ssh&gt; postman: in the queue for reading :/
13:40 &lt;septu_ssh&gt; but if it's doc'd, then it's fine
13:40 &lt;cervantes&gt; postman: yeah I figured
13:41 &lt;+postman&gt; septu_ssh: www.postman.i2p/inout.html
13:41 &lt;+postman&gt; septu_ssh: www.postman.i2p/mailv2.html
13:41 &lt;+postman&gt; cervantes: this is no drama really - the quota is a sane limit
13:41 &lt;cervantes&gt; postman: even someone being able to send  nrelays * quota recipients is no bad thing
13:41  * septu_ssh is bungle
13:41 &lt;+postman&gt; cervantes: yep
13:42 &lt;+postman&gt; the goal is just to stop anybody from really abusing the service
13:42 &lt;+postman&gt; in the tests i had 3 relays have been really fast 
13:42 &lt;@jrandom&gt; postman: i forget, will this have support for the local smtp relay talking directly to someone else's smtp relay, rather than bouncing through your nodes?
13:42 &lt;+postman&gt; cervantes: within 10 secs they have been synced :)
13:43 &lt;@jrandom&gt; (or perhaps thats just for later)
13:43 &lt;+postman&gt; jrandom: the i2p mail relays will be operated by several ppl and are the preferred dests for routing mail
13:43 &lt;cervantes&gt; postman: you could introduce an exponential delay to the send queue
13:43 &lt;cervantes&gt; if it becomes an issue
13:43 &lt;+postman&gt; jrandom: so sending to other destinations could be handy under certain circumstances
13:44 &lt;@jrandom&gt; aye, though dangerous under others
13:44 &lt;cervantes&gt; so the more mail you send the greater the time the mail gets queued for...should give the relays time to catch up
13:44 &lt;+postman&gt; jrandom: but if a node's owner discloses his IMIO destination he could be spammed w/o control :)
13:44 &lt;@jrandom&gt; exactly
13:44 &lt;@jrandom&gt; otoh, same goes if the i2p mail relays are hostile
13:45 &lt;+postman&gt; jrandom: indeed, it's a WOT like construction
13:45 &lt;@jrandom&gt; &lt;/tinFoil&gt;
13:45 &lt;+postman&gt; jrandom: i cannot stop a relay operator from distributing a quota of 0 for your address
13:45 &lt;@jrandom&gt; 'k great.  yeah, no need to worry about it for now
13:45 &lt;+postman&gt; :)
13:46 &lt;+postman&gt; ok
13:46 &lt;+postman&gt; .
13:46 &lt;@jrandom&gt; ok cool, thanks for the update.  some really exciting stuff
13:46 &lt;@jrandom&gt; ok, swinging on to 3) i2p-bt updates
13:46 &lt;@jrandom&gt; duck: ping
13:46 &lt;@duck&gt; hi
13:47 &lt;@duck&gt; Yesterday BitTorren 4.0.0 was released
13:47 &lt;ant&gt; &lt;dm&gt; sounds german
13:47 &lt;@duck&gt; which we more or less waited for before starting on 0.2
13:47 &lt;@duck&gt; wrote a tasklist / todo: http://pastebin.ca/raw/7037
13:47 &lt;@duck&gt; (sorry my www is currently down)
13:48 &lt;@jrandom&gt; cool
13:48 &lt;legion&gt; what sort of timetable are we talking about for 0.2?
13:48 &lt;@duck&gt; the goal was 4 weeks
13:49 &lt;legion&gt; cool
13:49 &lt;@duck&gt; as you can see RawServer (the part that communicates with i2p) is the biggest task
13:50 &lt;@duck&gt; .
13:50 &lt;@duck&gt; a quick poll:
13:50 &lt;legion&gt; yeah, I'm well aware of that :)
13:50 &lt;@duck&gt; who is planning to create an i2p-bt fork?
13:50 &lt;@jrandom&gt; cool, is there anything people can do to help?
13:50 &lt;@jrandom&gt; heh
13:51 &lt;ant&gt; &lt;dm&gt; i
13:51  * jrandom grabs a spoon
13:51 &lt;ant&gt; &lt;dm&gt; m wiling to hepl
13:51 &lt;legion&gt; i
13:51 &lt;ant&gt; &lt;dm&gt; m gay
13:51 &lt;legion&gt; I'm working on a fork
13:52 &lt;@duck&gt; good, then I know who not to take serious.
13:52 &lt;@duck&gt; really, I think it is silly; pooling resources might get you much further
13:53 &lt;@jrandom&gt; or perhaps if there are better ways to go, you can convince duck to work that way?
13:53 &lt;named&gt; I'm going to write a fork in qbasic, please take me seriously.
13:53 &lt;@duck&gt; I'll try to have the process more open, so others can see what is planned etc
13:53 &lt;ant&gt; &lt;dm&gt; your openness is not swaying us. FORK! FORK! FORK! FORK!
13:53 &lt;@duck&gt; if you have any other suggestions
13:54 &lt;ant&gt; * dm raises legion onto his shoulders.
13:54 &lt;legion&gt; hmm, that may be true, though with what I'm doing I doubt you want me polluting the main i2p-bt development process ;)
13:54 &lt;ant&gt; &lt;dm&gt; FORK! FORK! FORK! FORK!
13:54 &lt;@jrandom&gt; legion: what are you doing that duck wouldn't want to support?
13:55 &lt;@duck&gt; legion: congrats, if you google for 'i2p bittorrent', then an announcement of "Windows I2P Bittorrent Version 1.0" is #1
13:55 &lt;@jrandom&gt; jesus
13:56 &lt;bla&gt; jrandom: Yes?
13:56 &lt;+postman&gt; jrandom: yeah, they will rip this network's ass open soon :)
13:56 &lt;bla&gt; ;)
13:56 &lt;named&gt; 1.0? Damn, I'm using 0.1.8!
13:56 &lt;Ragnarok&gt; oy
13:57 &lt;legion&gt; omfg, really?! I cannot believe it... that's insane.
13:57 &lt;@duck&gt; anyway, I dont think that there is much new to say on this
13:57 &lt;legion&gt; my 1.0 release is based on 0.1.8 if you're running 0.1.8 you're fine.
13:58 &lt;@jrandom&gt; (and the 1.0 release is a .exe that no one has reviewed, ymmv)
13:58 &lt;legion&gt; I poorly named and numbered it sorry, again about that.
13:58 &lt;ant&gt; &lt;dm&gt; 1.0&gt;&gt; 0.1.8
13:58 &lt;ant&gt; &lt;dm&gt; any day of the week
13:59 &lt;@duck&gt; slightly related:
13:59 &lt;@jrandom&gt; ok, anything else on 3) i2p-bt, or shall we move on to 4) ???
13:59 &lt;+postman&gt; legion: when there will be sourcecode downloadable?
13:59 &lt;frosk&gt; "I2P-BT 0.1.8 works pretty fine and stable so far. I personally see no reason to update to I2P-BT 1.0" (seen on forum)
13:59  * jrandom sighs
13:59 &lt;@duck&gt; last month bram cohen held a talk about bittorrent on some university
14:00 &lt;@duck&gt; quite interesting: http://netnews.nctu.edu.tw/~gslin/tmp/050216-ee380-100.wmv.torrent
14:00 &lt;@duck&gt; (learned lessons about big p2p programs, plus some bittorrent details explained)
14:00 &lt;@duck&gt; .
14:01 &lt;@jrandom&gt; word
14:01 &lt;@duck&gt; postman: legion has released some sourcecode
14:01 &lt;ant&gt; &lt;dm&gt; is he the inventor of BT?
14:01 &lt;@duck&gt; but according to smeghead it isnt the same as the .exe
14:01 &lt;@jrandom&gt; dm: yes
14:01 &lt;legion&gt; There is a developer source you can download from http://legion.i2p/archives/Itorrent_1_x_Developer_Source.zip.bz2
14:02 &lt;+postman&gt; k, will have a look
14:02 &lt;ant&gt; &lt;dm&gt; is the exe a direct compile of that source?
14:03 &lt;legion&gt; though really the 1.0 source is really just 0.1.8 with a patch from smeghead, compiled and nicely packaged.
14:04  * cervantes walks over to 4)??? and waits for everyone to catch up
14:04 &lt;ant&gt; &lt;dm&gt; the question remains unanswered
14:04 &lt;ant&gt; &lt;dm&gt; Legion, did you or did you not, order a code red???
14:04 &lt;@jrandom&gt; *cough*
14:04 &lt;legion&gt; Perhaps we should get back on topic, my bt client discussion moved to #itorrent
14:05 &lt;@jrandom&gt; ok, 4) ???
14:05 &lt;@jrandom&gt; anything else people want to bring up?
14:05 &lt;@jrandom&gt; aum: you had something?
14:06 &lt;ant&gt; &lt;dm&gt; stasher is back?
14:06 &lt;legion&gt; I'm just seeing some funky behavior with 0.5.0.2 periods of heavy traffic...
14:06 &lt;aum&gt; yes
14:06 &lt;aum&gt; i'd like to raise the question of automated tunnel creation/management
14:07 &lt;ant&gt; &lt;dm&gt; go on
14:07 &lt;+detonate&gt; there's a null pointer exception in the systray thing in windows, i just noticed
14:07 &lt;aum&gt; it's 1337 that the web console now allows for humans to manually create/delete/manage tunnels
14:07 &lt;@jrandom&gt; detonate: could you toss 'er on the bugzilla?
14:07 &lt;aum&gt; but I also strongly believe that there should always be a reliable and convenient way for programs to manage tunels as well
14:08 &lt;@jrandom&gt; aum: no one disagrees.  we need it, and we will have it.  just not yet.
14:08 &lt;ant&gt; &lt;dm&gt; can't you do that through SAM?
14:08 &lt;aum&gt; i noticed on my recent return to i2p that the pysam library is no longer working
14:08 &lt;septu_ssh&gt; I have a quick question as well after aum
14:08 &lt;aum&gt; which was a disappointment
14:08 &lt;@jrandom&gt; the SAM protocol works, pysam doesnt
14:08 &lt;Ragnarok&gt; did it ever work?
14:09 &lt;aum&gt; correct
14:09 &lt;aum&gt; pysam used to work brilliantly
14:09 &lt;legion&gt; During such periods there are 1000+ tunnels my node is participating in and several seconds of lag and delay.
14:09 &lt;@jrandom&gt; legion: aye, the # of tunnels is because of older builds
14:09 &lt;cervantes&gt; ah mymodesty
14:09 &lt;cervantes&gt; eerm pymodesty
14:09 &lt;aum&gt; i'm presently writing a module 'i2ptunnel.py', which defines classes allowing easy tunnel management
14:10 &lt;legion&gt; so if older builds were not being connected to, the networking would be much smoother?
14:10 &lt;@jrandom&gt; 'k, i don't know if thats the right long term solution, but if it bridges the gap for you now, cool
14:10 &lt;@jrandom&gt; legion: those tunnels aren't the problem
14:11 &lt;aum&gt; well, the class interfaces can remain even though the underlying mechanism changes
14:11 &lt;@jrandom&gt; 'k
14:11 &lt;legion&gt; aren't they?
14:12 &lt;legion&gt; When there a few tunnels, there is very little lag and delay...
14:12 &lt;cervantes&gt; legion: sorry aum is just raising some questions, if you hang fire a minute
14:12 &lt;legion&gt; it just seems odd to me.
14:13 &lt;legion&gt; ok
14:13 &lt;@jrandom&gt; i just worry that we need to take into consideration whats been successful in the past - the web config works and is maintained because everyone uses it.  perhaps it'd be best to get whatever app you're working on working with manual tunnel creation *first*, that'd be more efficient?
14:13 &lt;@jrandom&gt; just so that there is always something that is using i2ptunnel.py, to stress it
14:13 &lt;aum&gt; we seem to be deadlocking
14:13 &lt;+detonate&gt; jrandom:sure
14:14 &lt;ant&gt; &lt;dm&gt; let's move on then
14:14 &lt;aum&gt; i don't want to invest time in developing my app till I've got a tunnel mgmt API I can rely on
14:14 &lt;septu_ssh&gt; \o. - point to raise 
14:14 &lt;cervantes&gt; realistically I can't imagine the tunnel interface will be revamped in the next couple of months though...
14:14 &lt;@jrandom&gt; but surely you see that we can add one trivially
14:14 &lt;cervantes&gt; so a stopgap solution is viable
14:15 &lt;named_&gt; Couldn't the web config have some kind of api that aum's program manipulates?
14:15 &lt;@jrandom&gt; named_: yes
14:16 &lt;@jrandom&gt; its trivial to add something in to allow safe control via URLs, but only makes sense if there's something that needs it
14:16 &lt;@jrandom&gt; otherwise it'll just rot
14:16 &lt;aum&gt; named_: that would be nice, and could work if there were a hardcoded password in config that client progs need to POST in along with tunnel control fields
14:16 &lt;cervantes&gt; personally I'd like to see the whole tunnel system completely revamped, if you include a tunnel management interface from the start then you won't have to worry about the extra effort needed to maintain a seperate interface
14:17 &lt;@jrandom&gt; aye, the proxies do need a bunch of work, which i've been hiding from as much as possible :)
14:17 &lt;aum&gt; SAM is good for some situations, bad for others
14:17 &lt;cervantes&gt; but that's somewhat down the line...
14:17 &lt;fedo&gt; (
14:18 &lt;@jrandom&gt; aum: but as a stopgap, couldn't you just use one of the three available methods?
14:18 &lt;cervantes&gt; ie if the webinterface itself uses the api then there's no maintenance overhead
14:18 &lt;@jrandom&gt; right.  the web interface uses the TunnelControllerGroup
14:19 &lt;aum&gt; SAM usage gets difficult when one wants to use existing libs that are extensively dependent on standard TCP sockets
14:19 &lt;aum&gt; jrandom: the I2PTunnel CLI doesn't work for opening server tunnels, so i'm presently writing code for using TunnelControllerGroup
14:19 &lt;@jrandom&gt; aum: exising libs need to be carefully audited.  for instance, the gzip utility itself exposes sensitive data
14:19 &lt;aum&gt; coding as we speak
14:21 &lt;@jrandom&gt; I'm certain that the CLI works for server tunnels, but using the TunnelControllerGroup is preferred, if you need it that way
14:21 &lt;@jrandom&gt; ok, anyone else have anything to bring up?
14:22 &lt;septu_ssh&gt; My question pertains to a distributed version of the hosts.txt, a DHT table is used currently for routerInfo, could this not be extended to a distributed version of DNS? The DNS DHT could contain mappings from www.bla.i2p to the eepsite SHA, and the entries would be signed by an 'I2P registrar'... comments? rebuttals?
14:22 &lt;mancom&gt; a question concerning the roadmap: is 0.6 still scheduled for april?
14:22 &lt;@jrandom&gt; septu_ssh: non-routing data goes in the netDb over my dead body ;)
14:23 &lt;septu_ssh&gt; jrandom: not the same db
14:23 &lt;septu_ssh&gt; a different distributed db
14:23 &lt;aum&gt; jrandom: did you see my bug report? the CLI 'server' command /does not work/
14:23 &lt;maestro^&gt; septu_ssh: there isnt any i2p registrar
14:23 &lt;@jrandom&gt; septu_ssh: there are many dangerous aspects of naming, with a few key tradeoffs.  have you seen the naming discussion on ugha.i2p?
14:24 &lt;@jrandom&gt; septu_ssh: ah, a DHT on top of I2P could certainly be used to distribute entries, though those names would not be secure, if they were treated as global entries
14:26 &lt;@jrandom&gt; aum: i used it daily up through a few weeks ago, did you see my reply?
14:26 &lt;@jrandom&gt; maestro^: thats the plan
14:26 &lt;@jrandom&gt; er, mancom:
14:26 &lt;cervantes&gt; aum: I have a reply to that i2plist mail from jr, has it not reached you yet, or does the issue remain?
14:26 &lt;septu_ssh&gt; the only reason why I suggest a 'registrar' is because collisions can take place otherwise
14:26 &lt;@jrandom&gt; septu_ssh: embrace collisions :)
14:26 &lt;@jrandom&gt; globally unique, human readable, distributed, and secure naming doesnt exist
14:27 &lt;septu_ssh&gt; it can also happen in host.txt if it is manually edited, but the problem remains the same
14:27 &lt;@jrandom&gt; drop the first parameter, and you're golden
14:27 &lt;aum&gt; jrandom: i did see your reply - and I /do/ have streaming.jar in my cp
14:27 &lt;septu_ssh&gt; postman manages a central node for mail, so there is some element of trust within the network, surely someone would trust a registrar to manage namespace?
14:27 &lt;@jrandom&gt; ok cool, and it still comes back with that stacktrace aum?
14:28 &lt;aum&gt; yes
14:28 &lt;@jrandom&gt; septu_ssh: postman only acts as a central element for postman's outproxies and inproxies
14:28  * Ragnarok really need to get around to writing that addressbook doc...
14:28 &lt;aum&gt; this is when i manually run the cli, do a genkeys, then do a 'server' using the privkeyfile generated by genkeys
14:28 &lt;@jrandom&gt; septu_ssh: no one will trust anyone to manage a namespace.  censorship == exert presure on that registrar.
14:28 &lt;maestro^&gt; everyone is really their own registrar
14:29 &lt;maestro^&gt; you trust your friends and they trust you
14:29 &lt;aum&gt; oh shit, i picked up an old classpath
14:29  * aum tests again
14:30 &lt;ant&gt; &lt;dm&gt; ok, I'll be the registrar.
14:31 &lt;ant&gt; &lt;dm&gt; I'll be as unbiased as I can... cool?
14:31 &lt;septu_ssh&gt; hmmm, ok, back to the proverbial drawing board then...
14:31 &lt;@jrandom&gt; septu_ssh: a good place to review is http://zooko.com/distnames.html :)
14:32 &lt;@jrandom&gt; everyone wants it, but what they want just isn't secure.  we have a solution that is, but we give up global uniqueness
14:33 &lt;septu_ssh&gt; hmmm, ok
14:33 &lt;@jrandom&gt; ok, anyone else have anything else to bring up for the meeting?
14:33 &lt;cervantes&gt; septu_ssh: http://forum.i2p.net/viewtopic.php?t=134
14:33 &lt;aum&gt; jrandom - ok, cli 'server' now works, but i never got a 'job number' for the tunnel
14:34 &lt;@jrandom&gt; hmm right, it runs forever
14:34 &lt;aum&gt; oh, i gotta do 'list' to get the job num
14:36 &lt;@jrandom&gt; ok cool, if there's nothing else...
14:36  * jrandom winds up
14:36  * jrandom *baf*s the meeting closed
</div>
