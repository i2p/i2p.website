---
title: "I2P Dev Meeting - December 28, 2004"
date: 2004-12-28
author: "@jrandom"
description: "I2P development meeting log for December 28, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, cat-a-puss, frosk, jdot\__, jrandom, lektriK, mule, mule2, postman, scintilla</p>

## Meeting Log

<div class="irc-log">
13:06 &lt;@jrandom&gt; 0) hi
13:06 &lt;@jrandom&gt; 1) 0.4.2.5
13:06 &lt;@jrandom&gt; 2) 0.5
13:06 &lt;@jrandom&gt; 3) ???
13:06 &lt;@jrandom&gt; 0) hi
13:06  * jrandom waves
13:06 &lt;+postman&gt; *wave*
13:06 &lt;ant&gt; &lt;jnymo&gt; hello
13:06 &lt;@jrandom&gt; brief status notes posted up @ http://dev.i2p.net/pipermail/i2p/2004-December/000535.html
13:07 &lt;@jrandom&gt; jumping in to 1) 0.4.2.5
13:07 &lt;@jrandom&gt; as mentioned, things are pretty much working
13:08 &lt;+postman&gt; yeah, quite impressive
13:08 &lt;+postman&gt; no more lease timouts on my systems at all
13:08 &lt;@jrandom&gt; a lot of people have seen what you've seen jnymo, with 0 participating tunnels, largely in part to the increased efficiency & peer selection (where we now know to leech off postman's machine ;)
13:08 &lt;ant&gt; &lt;jnymo&gt; me too
13:08 &lt;@jrandom&gt; nice
13:08 &lt;ant&gt; &lt;jnymo&gt; and eepsites are snappy
13:09 &lt;+postman&gt; :)
13:09 &lt;ant&gt; &lt;jnymo&gt; thanks postman :)
13:09 &lt;+postman&gt; totsl bw is 29kb / 30.1kb/s
13:09 &lt;frosk&gt; everybody feels less loved, but in reality the love is just being put more efficiently to work
13:10 &lt;ant&gt; &lt;jnymo&gt; wow
13:10 &lt;@jrandom&gt; b1tchin postman 
13:10 &lt;mule2&gt; i don't think that is the preferred ideal. we'd better have some traffic through all nodes
13:10 &lt;ant&gt; &lt;jnymo&gt; i could handle that if people just loved me :(
13:10 &lt;+postman&gt; yep
13:10 &lt;mule2&gt; as kind of cover traffic
13:10 &lt;@jrandom&gt; mule2: its a matter of our load being much less than our network capacity
13:11 &lt;@jrandom&gt; i dont think we'll be able to keep the capacity greater than the load for long
13:11 &lt;ant&gt; &lt;jnymo&gt; mule2, postman is also act as i mixer.. so its hard to tell where you packets are going after they go in
13:11 &lt;@jrandom&gt; so i'm not too worried about not pushing any data through slower peers
13:12 &lt;mule2&gt; probably less perfect optimization would be good for anonymity
13:12 &lt;@jrandom&gt; otoh, it also gives incentive for more people to (implement &) use i2pcontent, so they can mirror as well as gain cover traffic ;)
13:12 &lt;jdot__&gt; i it a security issue that one router handles all(ish) tunnels?
13:13 &lt;@jrandom&gt; mule2: lets first get it as good as we can get it, then we can discuss proactively making it worse
13:13 &lt;@jrandom&gt; jdot__: we don't have one router handling all of the traffic, but we are seeing the grouping of routers who are on very fast connections (colo, etc) handling more than dialup/dsl/cable users
13:14 &lt;@jrandom&gt; plus the reduced tunnel failures means we're shifting & exploring less
13:14 &lt;mule2&gt; perhaps some traffic distribution would be possible, as long as we are far from the routers limits
13:14 &lt;@jrandom&gt; right, probabalistic tunnel rejection is in the router and can be enabled based on the router's bandwidth limits
13:15 &lt;ant&gt; &lt;jnymo&gt; yea, but such high throughput on postman's node makes it harder to analyze his node.. so it might be safer to send through him than for all nodes to do one KBs..
13:15 &lt;@jrandom&gt; (but if postman doesnt set any limits, we can't reject based on a % of that ;)
13:15 &lt;ant&gt; &lt;jnymo&gt; groupings of faster nodes cause something of a mix cascade structure, no?
13:15 &lt;@jrandom&gt; aye, that is one way to look at it
13:15 &lt;lektriK&gt; can I close the Start I2P window?
13:15  * postman is very sorry NOT to restrict his bandwidth
13:16 &lt;@jrandom&gt; lektriK: unfortunately, not really, unless you start i2p as a service (See http://localhost:7657/configservice.jsp)
13:16 &lt;@jrandom&gt; heh postman dont worry, we'll back off your router if/when we reach your router's capacity
13:17 &lt;lektriK&gt; Ok, it sais service started
13:17 &lt;lektriK&gt; can I close it now?
13:17 &lt;@jrandom&gt; lektriK: no/yes - you can shut down your router then start it again via start-&gt;run-&gt;"net start i2p"
13:18 &lt;mule2&gt; as it is, a few very big routers could handle all the tunnels, removing all cover traffic from all other routers. but lets continue with that after the meeting.
13:18 &lt;mule2&gt; don't want to complain about the network behaving to good :)
13:18 &lt;@jrandom&gt; hehe
13:20 &lt;@jrandom&gt; some further exploration will occur with 0.5, though there are anonymity related issues with spreading too far.  there'll be further details to be worked through on that for 0.5 though (and in the doc which might be ready next week as a first draft)
13:21 &lt;@jrandom&gt; anyway, anyone else have something to bring up for 0.4.2.5?  
13:21 &lt;@jrandom&gt; or shall we move on briefly to 2) 0.5?
13:21 &lt;+postman&gt; move
13:21 &lt;ant&gt; &lt;jnymo&gt; very stable... move
13:21 &lt;@jrandom&gt; consider us moved
13:22 &lt;@jrandom&gt; 2) 0.5
13:22 &lt;@jrandom&gt; yeah.  still work in progress.  more info when its ready.
13:22 &lt;ant&gt; &lt;Quadn-werk&gt; Sir Arthur C. Clarke is alive :P
13:22 &lt;ant&gt; &lt;Quadn-werk&gt; http://slashdot.org/articles/04/12/28/0120240.shtml?tid=99&tid=1
13:22 &lt;ant&gt; &lt;jnymo&gt; .5 is exciting
13:22 &lt;@jrandom&gt; ok, thats all i have to say on that - anyone have any questions / things to discuss about it?
13:23 &lt;@jrandom&gt; aye, there are definitely some important revamping going on, based on what we've learned over the last 16 months
13:23 &lt;@jrandom&gt; (or shit, 18)
13:23 &lt;+postman&gt; jrandom: so 0.5 will emnploy a new tunnel management system mostly?
13:23 &lt;ant&gt; &lt;Quadn-werk&gt; arg, i hope i didnt interrupt the meeting :/
13:23 &lt;+postman&gt; wow
13:23 &lt;ant&gt; &lt;Quadn-werk&gt; sorry heh
13:23 &lt;ant&gt; &lt;jnymo&gt; heh. i had a suggestion
13:24 &lt;@jrandom&gt; yeah postman, new management, pooling, and building
13:24 &lt;+postman&gt; quadn: look what you've done - your paste caused a netsplit :)
13:24 &lt;@jrandom&gt; you bastard!
13:24 &lt;ant&gt; &lt;Quadn-werk&gt; !
13:24 &lt;@jrandom&gt; sup jnymo?
13:24 &lt;+postman&gt; jrandom: will every tunnel be a separate local destination still?
13:25 &lt;@jrandom&gt; huzzawuzzah?
13:25 &lt;@jrandom&gt; there won't be any change to i2ptunnel in 0.5
13:25 &lt;+postman&gt; jrandom: ok
13:25 &lt;@jrandom&gt; (at least, i dont plan on any)
13:26 &lt;mule&gt; postman mounting an intersection attack?
13:26 &lt;ant&gt; &lt;jnymo&gt; for those who aren't getting /any/ bandwidth usage..  how bout letting routers build tunnels with them in it.. like ABCABCA
13:26 &lt;+postman&gt; mule: no, it was quadn's fault :)
13:26 &lt;ant&gt; &lt;jnymo&gt; and that would be a dummy tunnel
13:27 &lt;@jrandom&gt; jnymo: advertising a router as saying "hey i have excess bandwidth, use me" is a dangerous game
13:27 &lt;+postman&gt; jrandom: what issues will then be addressed by the redesign  ( in a nutshell )
13:27 &lt;ant&gt; &lt;jnymo&gt; not sure i meant that, jrandom
13:27 &lt;@jrandom&gt; but what it looks like now is that we'll have two sets of tunnels - the normal ones, and then exploratory ones, where the later are built from randomly selected non-failing peers
13:28 &lt;ant&gt; &lt;jnymo&gt; jrandom: i meant creating a dummy tunnel, and putting my self in the middle of that tunnel just to simulate some traffic
13:29 &lt;@jrandom&gt; postman: making it much harder to correllate peers in a tunnel, allowing clients to effectively choose their outbound tunnel length, and providing the options necessary for addressing the predecessor attack (with various tradeoffs)
13:29 &lt;@jrandom&gt; (oh, and improving performance by getting rid of a lot of modPow calls)
13:29 &lt;+postman&gt; ok thanks
13:29 &lt;ant&gt; &lt;jnymo&gt; postman: and per hop tunnel ids is a big one
13:30 &lt;+postman&gt; modpow?
13:30 &lt;@jrandom&gt; ah jnymo.  yeah, there's a lot of potential for various chaff traffic generation
13:30 &lt;ant&gt; &lt;jnymo&gt; that way, no two non-neighboring nodes can know there on the same tunnel, postman
13:30 &lt;@jrandom&gt; postman: modular exponentiation, heavy cpu usage & memory waste
13:31 &lt;ant&gt; &lt;jnymo&gt; jrandom: k cool
13:31 &lt;+postman&gt; k
13:31 &lt;scintilla&gt; jrandom, wrt to letting clients choose tunnel length: will there be anything in place to keep ppl from cranking it up to 99 (or whatever)?
13:31 &lt;ant&gt; &lt;jnymo&gt; cpu power
13:32 &lt;@jrandom&gt; when necessary we can add hashcash, but excessively long tunnels will just end up failing anyway
13:32 &lt;scintilla&gt; ah good point
13:32 &lt;@jrandom&gt; we could even add in some trickery - requiring that a tunnel have a valid tunnel message pumped through it within 60s of creation for it to be 'valid'
13:33 &lt;@jrandom&gt; (so if the tunnel was 20 hops long, it'd take them too long to build all those hops)
13:33 &lt;scintilla&gt; that's a great idea - that'll keep any such ridiculousness from lingering for very long
13:33 &lt;@jrandom&gt; but thats all vs the hackers.  normal users will just use the exposed interface
13:34 &lt;ant&gt; &lt;jnymo&gt; right, which you'll cap off somewhere right?
13:34 &lt;ant&gt; &lt;jnymo&gt; we'll get higher than the maximum 2 as it is now, right?
13:34 &lt;@jrandom&gt; right, like the # hops drop down on /configclients.jsp or /i2ptunnel/edit.jsp
13:35 &lt;@jrandom&gt; oh i thought the max was 3 now?  ok, but yeah, higher than 2 will be available
13:35 &lt;ant&gt; &lt;jnymo&gt; 3 tunnels, 2 hops
13:35 &lt;@jrandom&gt; ah 'k
13:35 &lt;@jrandom&gt; yeah, 0.5 will add in some important new tweaks, such as whether to randomize those lengths, as well as how much to randomize, etc
13:36 &lt;frosk&gt; the max is indeed 3
13:36 &lt;ant&gt; &lt;jnymo&gt; hmm
13:37 &lt;@jrandom&gt; ah its 3 on /configclients 2 on i2ptunnel
13:37 &lt;frosk&gt; is 0.5 still on track for january?
13:37 &lt;ant&gt; &lt;jnymo&gt; ah
13:37 &lt;@jrandom&gt; yeah frosk
13:37 &lt;frosk&gt; goodie
13:37 &lt;@jrandom&gt; i wont dawdle too much longer on the streaming lib, i promise ;)
13:37 &lt;frosk&gt; it just sounds like a lot of work :)
13:38 &lt;@jrandom&gt; its actually not so bad, the hard part is getting the algorithms right
13:38 &lt;@jrandom&gt; (details schmetails ;)
13:39 &lt;+postman&gt; frosk: and it's all on paper already
13:39 &lt;+postman&gt; :)
13:39 &lt;ant&gt; &lt;jnymo&gt; heh
13:39 &lt;frosk&gt; true :)
13:39 &lt;@jrandom&gt; mostly yeah ;)
13:39 &lt;@jrandom&gt; ok, anyone have anything else for 2) 0.5?
13:39 &lt;ant&gt; &lt;jnymo&gt; nada
13:39 &lt;frosk&gt; el zilcho
13:40 &lt;@jrandom&gt; 'k, swingin on to good old fashioned 3) ???
13:40 &lt;@jrandom&gt; hi
13:40 &lt;@jrandom&gt; anyone have anything else they want to bring up?
13:41 &lt;ant&gt; &lt;jnymo&gt; postman: there arent smtp/pop3 inproxies on i2pmail.org are there?
13:41 &lt;cat-a-puss&gt; I am still seeing weird delays on the client end...
13:41 &lt;+postman&gt; hrm no
13:41 &lt;frosk&gt; this is where i'd hand over the congratulatory bottle of wine for a fine year of development ;)
13:41 &lt;+postman&gt; jnymo: POP3 is only available for i2p users
13:41 &lt;@jrandom&gt; cat-a-puss: ah i missed those messages when you were around earlier
13:41 &lt;+postman&gt; jnymo: there IS a SMTP inproxy as MX for the domain i2pmail.org
13:42 &lt;@jrandom&gt; frosk: cheers
13:42 &lt;ant&gt; &lt;jnymo&gt; right right.. that's coo'..
13:42 &lt;cat-a-puss&gt; Like I can have two local Destinations and when one trys to connect to another there is a delay and it is not CPU bound
13:42 &lt;mule&gt; cat-a-puss: do you also hand over the bonus cheque ?
13:42  * postman donates a good whiskey 
13:42 &lt;@jrandom&gt; cat-a-puss: right, you saw a .5-1.0s delay right?
13:42 &lt;cat-a-puss&gt; mule: what?
13:42 &lt;cat-a-puss&gt; jrandom: yeah
13:43 &lt;@jrandom&gt; cat-a-puss: perfectly normal, part of the deferred syn
13:43 &lt;mule&gt; sorry, the comment was from frosk
13:43 &lt;ant&gt; * jnymo pulles out that crappy box wine
13:43 &lt;mule&gt; frosk: do you also hand over the bonus cheque ?
13:43 &lt;@jrandom&gt; (it waits a bit to send the SYN and the related ACK in case there is more data to bundle)
13:43 &lt;scintilla&gt; oh fyi, i should be receiving the book with the fortuna algorithm spec in it soon... in the meantime i've been experimenting with trying to gather entropy in java without destroying a machine
13:44 &lt;@jrandom&gt; ah kickass
13:44 &lt;ant&gt; &lt;jnymo&gt; mmm, someone was wanting to mount some attacks on i2p
13:44 &lt;ant&gt; &lt;jnymo&gt; who was that?
13:44 &lt;@jrandom&gt; connelly
13:44 &lt;cat-a-puss&gt; Is there a way to prevent that, or do I just have to try to avoid short lived connections where I can?
13:45 &lt;ant&gt; &lt;jnymo&gt; any word on that, jr?
13:45 &lt;@jrandom&gt; cat-a-puss: yeah there are some options you can pass when creating the I2PSocketManager, lemmie pull 'em up
13:46 &lt;@jrandom&gt; jnymo: its a long term intersection attack, so after a while he'll have data to help identify what routers particular eepsites are on.  i'm sure he's going to write up some summary data for us once he's got it
13:46 &lt;ant&gt; &lt;jnymo&gt; scintalla: what's the fortuna algorithm?
13:46 &lt;ant&gt; &lt;jnymo&gt; jrandom: aight
13:48 &lt;@jrandom&gt; cat-a-puss: i2p.streaming.initialResendDelay=50 i2p.streaming.connectDelay=100
13:48 &lt;scintilla&gt; it's a cryptographically secure pseudo-random number generator... something which is absolutely essential for trustworthy encryption
13:48 &lt;jdot__&gt; anyone volunteer for that attack yet?
13:48 &lt;@jrandom&gt; cat-a-puss: then be sure to flush() after write()ing to the I2PSocket
13:48 &lt;@jrandom&gt; jdot__: yeah, he has 7 volutneered sites
13:48 &lt;cat-a-puss&gt; jrandom: ok
13:49 &lt;ant&gt; &lt;jnymo&gt; wrt the great naming debate.. 
13:49 &lt;ant&gt; * jnymo snickers
13:49 &lt;@jrandom&gt; oh and i2p.streaming.initialAckDelay=1000
13:49 &lt;@jrandom&gt; or even =100
13:49  * jrandom flings mud at jnymo
13:50 &lt;ant&gt; &lt;jnymo&gt; i actually do work with x500 and my job lets me have free winSevers
13:50 &lt;ant&gt; &lt;jnymo&gt; so, perhaps i'll just set up a central DNS for testing purposes in a month or two
13:51 &lt;@jrandom&gt; heh, having a centralized naming server hosted on a .mil would be bloody hilarious 
13:51 &lt;ant&gt; &lt;jnymo&gt; though hacking i2p addresses into winserver may be non-trivial.. dunno
13:51 &lt;ant&gt; &lt;jnymo&gt; heh.. dnsalias is the ticket
13:52 &lt;@jrandom&gt; nano has done some really cool work, integrating dnsjava with i2p
13:52 &lt;ant&gt; &lt;jnymo&gt; ooooh
13:53 &lt;@jrandom&gt; check out nano.i2p for more details
13:53 &lt;ant&gt; &lt;jnymo&gt; and no one was going to tell me.. ah, thanks
13:53 &lt;@jrandom&gt; but, as mentioned last time, people should post up their thoughts and ideas about naming to the wiki
13:54 &lt;@jrandom&gt; ok, anyone else have something to bring up for the meeting?
13:55 &lt;ant&gt; &lt;jnymo&gt; nope
13:57 &lt;@jrandom&gt; ok in that case
13:57  * jrandom winds up
13:57  * jrandom *baf*s the meeting closed
</div>
