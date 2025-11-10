---
title: "I2P Dev Meeting - December 21, 2004"
date: 2004-12-21
author: "@jrandom"
description: "I2P development meeting log for December 21, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bens, bob, detonate, dm, duck, Frooze, frosk, jrandom, kaji, Madman2003, modulus, mule, mule2, orion, Ragnarok, redzog, scintilla, susi23, ugha2p</p>

## Meeting Log

<div class="irc-log">
13:05 &lt;@jrandom&gt; 0) hi
13:05 &lt;@jrandom&gt; 1) 0.4.2.4 & 0.4.2.5
13:05 &lt;@jrandom&gt; 2) 0.5 strategy
13:05 &lt;@jrandom&gt; 3) naming
13:05 &lt;@jrandom&gt; 4) eepsite roundup
13:05 &lt;@jrandom&gt; 5) ???
13:06 &lt;@jrandom&gt; 0) hi
13:06  * jrandom waves
13:06 &lt;@jrandom&gt; weekly status notes posted a lil while ago @ http://dev.i2p.net/pipermail/i2p/2004-December/000528.html
13:07 &lt;@jrandom&gt; lets jump on in to 1) 0.4.2.4 & 0.4.2.5
13:08 &lt;@jrandom&gt; for those of you who have already upgraded to 0.4.2.5 - a good 1/3 of the network so far - thanks!
13:09 &lt;@jrandom&gt; i do try to keep a more calm pacing to the releases, but there were some things in 0.4.2.5 that really needed wider deployment
13:10 &lt;Madman2003&gt; 0.4.2.5 is working well for me when it comes to disconnects, but i don't run i2p 24/7(i had quite a few irc disconnects lately) and it's only been a few hours after the release
13:10 &lt;@jrandom&gt; as mentioned later on in the email, i dont have a planned date for when the next bugfix release will be, but we shall see
13:10 &lt;@jrandom&gt; ah great Madman2003 
13:10 &lt;@jrandom&gt; yeah, its definitely too early to tell about 0.4.2.5
13:11 &lt;frosk&gt; i used to see periods of high lag on .4, so far none of those with .5, but again, a bit early
13:11 &lt;frosk&gt; (i'm talking about irc lag, of course)
13:11 &lt;@jrandom&gt; the dns bug fixed could manifest itself in large numbers of peers running older releases failing at once, so the sooner people upgrade, the better
13:12 &lt;@duck&gt; is that related with the failures on those manually entering a hostname?
13:12 &lt;@jrandom&gt; yep
13:12 &lt;dm&gt; how useless is the windows system tray I2P icon!?!?
13:12 &lt;@duck&gt; ah, so that is why config.jsp is still friendly
13:13 &lt;Madman2003&gt; anyone have a clue why some still run pre 0.4.2.4 routers?(it's been out a while)
13:13 &lt;@jrandom&gt; dm: its more of a placeholder right now, plus a status icon saying "i2p is running"
13:13 &lt;dm&gt; They have a life? :)
13:13  * jrandom should resent that...
13:14 &lt;redzog&gt; is there a way to do soft-restarts from the command line?
13:14 &lt;@jrandom&gt; redzog: unfortunately not
13:14 &lt;redzog&gt; hmm, pity
13:14 &lt;@jrandom&gt; other than with wget, perhaps
13:14 &lt;redzog&gt; would make it easier to do automatic updates
13:14 &lt;+detonate&gt; i2prouter stop && i2prouter start :)
13:14 &lt;@jrandom&gt; no, nm, wget wouldnt work either
13:14 &lt;@jrandom&gt; (as the form requires interaction)
13:14 &lt;Madman2003&gt; i generally update trough cvs several times in between releases(at best once a day), only takes a few minutes
13:15 &lt;redzog&gt; lwp::simple could manage it
13:15 &lt;redzog&gt; just a POST
13:15 &lt;@jrandom&gt; redzog: support for that would be pretty cool
13:15 &lt;redzog&gt; I'll try to whip something up
13:15 &lt;@jrandom&gt; well, its more than just a post, you need to read the form presented to you then post those fields back
13:16 &lt;+detonate&gt; eventually releases will be further spaced though.. right?
13:16 &lt;@jrandom&gt; (there's a hidden flag to prevent people from doing things like &lt;img src="/configservice.jsp?action=restart"&gt;
13:16 &lt;redzog&gt; heh, right
13:16 &lt;@jrandom&gt; right detonate, t'wasn't planned to be this rapid, once a week at most
13:16 &lt;redzog&gt; does the nonce value change?
13:17 &lt;@jrandom&gt; if it didn't, it wouldnt be a nonce ;)
13:17 &lt;redzog&gt; hmm, seems so
13:17 &lt;redzog&gt; well, between sessions, between pageloads... ;)
13:17 &lt;redzog&gt; pageloads it is
13:17 &lt;@jrandom&gt; right
13:17 &lt;@jrandom&gt; ok, anyone have anything else wrt 0.4.2.4/0.4.2.5?
13:18 &lt;@jrandom&gt; i'm sur there'll be more discussion later after we've burnt in the new release more
13:18 &lt;dm&gt; oh, is this a meeting?
13:18 &lt;+detonate&gt; starting up seems to be a lot less smooth
13:18 &lt;+detonate&gt; than 2.3
13:18 &lt;@jrandom&gt; oh?  in what way detonate - cpu, lag, memory, time?
13:19 &lt;+detonate&gt; the list of peers takes forever to populate
13:19 &lt;+detonate&gt; and i get a huge number of shitlisted peers
13:19 &lt;+detonate&gt; also the i2ptunnel stuff sometimes hangs, but generally seems to take at least 2x as long to actually start up
13:19 &lt;+detonate&gt; once it's started things smooth out
13:19 &lt;+detonate&gt; it's odd
13:19 &lt;@jrandom&gt; hmm, what does it list for the cause on /logs.jsp#connectionlogs ?
13:20 &lt;ant&gt; &lt;BS314159&gt; I just did a graceful restart into 0.4.2.5. It took 120s to have Local Destinations
13:20 &lt;ant&gt; &lt;BS314159&gt; seems good
13:20 &lt;@jrandom&gt; cool BS314159 - thats pretty much the bare minimum, as we don't start i2ptunnel until 2 minutes after startup :)
13:20 &lt;+detonate&gt; there's nothing out of the ordinary
13:20 &lt;+detonate&gt; a shutdown exception
13:21 &lt;+detonate&gt; but i think i caused that
13:21 &lt;mule&gt; i have pulled over 300M through fcp for a movie with the last release. never been that good before. top rates beyond 40k. great work.
13:21 &lt;@jrandom&gt; wow, nice mule!
13:21 &lt;mule&gt; however i still have serious trouble with recovering from an IP change
13:21 &lt;@jrandom&gt; detonate: hmm, ok, i'd love to debug this further after the meeting or another time you have available
13:22 &lt;+detonate&gt; yeah
13:22 &lt;+detonate&gt; ok
13:22 &lt;dm&gt; tunnel lag: 364ms. What the fuck is going on , the tunnel lag is dropping 100-200ms on each release!
13:22 &lt;@jrandom&gt; ah mule, ok
13:22 &lt;@jrandom&gt; i've got an idea for how we could deal with those hung tcp connections - just toss on a 5m keepalive
13:23 &lt;@jrandom&gt; heh dm, dont worry, it'll get back up again ;)
13:23 &lt;frosk&gt; wow, i only have 261ms here :)
13:24 &lt;@jrandom&gt; ok, if there's nothing else, lets jump on to 2) 0.5 strategy
13:24 &lt;dm&gt; That can't be right...
13:25 &lt;+ugha2p&gt; Looks like I'm late for the meeting again.
13:26 &lt;@jrandom&gt; there's still a lot of work to be done with 0.5, but a broad outline of the process was included in that email
13:26  * jrandom sends ugha2p to the principal's office
13:27 &lt;@jrandom&gt; there are still some details left to be worked out on the tunnel pooling and creation, but i think we've got a few different offerings that will meet the needs of various user bases
13:28 &lt;@jrandom&gt; there'll be some good ol' fashioned documentation posted once most of the kinks in the design are hammered out for y'all's review
13:28 &lt;@jrandom&gt; (currently its taking up ~8 pages in the notebook, should compress well though)
13:29 &lt;kaji&gt; has the meeting started yet?
13:29 &lt;@jrandom&gt; but another one of the tasks listed for 0.5 is "deal with the bandwidth needs of the network", and i have no idea how to plan for that, so we'll play that by ear
13:29 &lt;@jrandom&gt; yes kaji, we're on 2) 0.5 strategy
13:30 &lt;@jrandom&gt; well, thats all i have to say about that at the moment, unless anyone has any questions/comments/concerns?
13:31 &lt;+ugha2p&gt; Wow, most of the routers have already upgraded.
13:31 &lt;+detonate&gt; is filtering http traffic to strip out javascript/etc in the roadmap?
13:31 &lt;+detonate&gt; for 0.5
13:31 &lt;+ugha2p&gt; detonate: No.
13:31 &lt;@jrandom&gt; detonate: 0.6
13:31 &lt;ant&gt; &lt;cat-a-puss&gt; WRT bandwidth, should we enable probabilistic tunnel length, and/or local biased tunnels, for bittorrent as in general BT users have a weaker threat modle?
13:32 &lt;@jrandom&gt; cat-a-puss: yes, definitely.  thats one of the big parts of the 0.5 release
13:32 &lt;+ugha2p&gt; detonate: Unless you implement it first. ;)
13:32 &lt;+detonate&gt; i was thinking about it
13:33 &lt;ant&gt; &lt;cat-a-puss&gt; will html filtering be conducted in a seperate process?
13:33 &lt;@jrandom&gt; i think michelle is looking at that too, so if you two wanted to work together (michelle is learning java) that'd rule
13:33 &lt;+detonate&gt; ok
13:33 &lt;@jrandom&gt; cat-a-puss: i know not.  
13:34 &lt;+ugha2p&gt; cat-a-puss: Why should it?
13:35 &lt;ant&gt; &lt;cat-a-puss&gt; (I ask because I was thinking of making a proxy that ran all incomming brouser traffic through clamav) That is GPLed so if we could include that in the filter, it would probably be good.
13:35 &lt;@jrandom&gt; cool cat-a-puss!
13:35 &lt;+ugha2p&gt; Some people already use Privoxy for I2P.
13:36 &lt;bens&gt; in general, I'm anti-including-stuff
13:36 &lt;susi23&gt; I would rather see people configuring their browsers right than promising to protect them from malicious code.
13:36 &lt;@jrandom&gt; susi23: no one configures their browser properly
13:36 &lt;@jrandom&gt; especially not joe sixpack
13:37 &lt;frosk&gt; one can wonder if Joe is even able to set a proxy for his browser
13:37 &lt;@jrandom&gt; my personal view is that something cgi-proxy like would be ideal
13:37 &lt;@jrandom&gt; exactly frosk
13:37 &lt;@jrandom&gt; with a cgi-proxy like interface (filtering according to their preferences, safe by default), even a drooling moron could use it
13:38 &lt;bens&gt; I suppose I2P needs multiple versions for multiple markets even more than MS Office
13:38 &lt;@jrandom&gt; 'tis why we have small components and push this stuff out of the router bens ;)  
13:38 &lt;Ragnarok&gt; a proxy auto config file would help
13:39 &lt;@jrandom&gt; Ragnarok: we have one, but there are still dangerous things that can be done with it
13:39 &lt;frosk&gt; maybe a specialized i2p browser even (if someone is drowning in free time ;)
13:39 &lt;susi23&gt; ragnarok: that one? http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/apps/proxyscript/i2pProxy.pac
13:39 &lt;@jrandom&gt; frosk: on the specialized i2p OS and hardware too, i suppose
13:40 &lt;frosk&gt; hehe, perfect
13:40 &lt;Ragnarok&gt; that's not in the install, though
13:40  * jrandom implements those in the specialized i2p universe
13:40 &lt;susi23&gt; . o O ( perhaps we should try to find a dedicated i2p planet too )
13:40 &lt;susi23&gt; . o O ( damn, too slow )
13:40 &lt;mule&gt; ok, we'll sell the hardware :)
13:40 &lt;frosk&gt; you know what they say, to create something from scratch, first create the universe
13:41 &lt;@jrandom&gt; w00t, now all we need are some investors..
13:41 &lt;bens&gt; seriously, a firefox autoconfigurator might be reasonable
13:41 &lt;@jrandom&gt; bens: the .pac susi linked to above should do the trick
13:41 &lt;bens&gt; not just for proxy; also for the security settings, homepage, etc.
13:41 &lt;@jrandom&gt; we can ship that with the install too, but its insufficient for people who need anonymity (and are not ubergeeks already)
13:42 &lt;@jrandom&gt; hmm, perhaps that sort of thing could go into cervantes' i2p xul app
13:43 &lt;@jrandom&gt; but thats getting further off topic from the 2) 0.5 strategy
13:43 &lt;@jrandom&gt; anyone else have anything for that, or shall we move on to 3) naming?
13:44 -!- Irssi: #i2p: Total of 40 nicks [2 ops, 0 halfops, 6 voices, 32 normal]
13:44 &lt;@jrandom&gt; consider us moved
13:44 &lt;@jrandom&gt; ok, aparently i kind of jumped the gun w/ the 2.0.1 ref of addressbook - Ragnarok, want to give us an update?
13:44 &lt;+ugha2p&gt; jrandom: Can we expect the dates on the roadmap to be correct?
13:45 &lt;@jrandom&gt; ugha2p: they currently reflect my best estimate
13:45 &lt;+ugha2p&gt; jrandom: Ok, right.
13:45 &lt;Ragnarok&gt; it's released now
13:45 &lt;@jrandom&gt; w00t
13:45 &lt;Ragnarok&gt; check ragnarok.i2p
13:45 &lt;Ragnarok&gt; I wasn't planning on releasing it yet, but jrandom forced my hand :)
13:46 &lt;@jrandom&gt; hehe
13:46 &lt;+ugha2p&gt; Ragnarok: Btw, you're missing a link from the homepage. :)
13:46 &lt;Ragnarok&gt; it's just a few bug fixes, nothing major, but it should deal better with some corner cases
13:46 &lt;@jrandom&gt; its on the top right ugha2p 
13:47 &lt;Ragnarok&gt; ugha2p: it's on the sidebar
13:47 &lt;Ragnarok&gt; I'll add links to the post as well, though :)
13:47 &lt;mule2&gt; "that'll be the day when i die". daily IP change to set the clock after.
13:48 &lt;Ragnarok&gt; anyway, if everyone could try it out, that'd be nice.  Bug reports are always appreciated
13:48 &lt;+ugha2p&gt; Ragnarok: Oh, that sidebar is seriously fucked in Opera.
13:48 &lt;mule2&gt; Lease expired 12773d ago
13:49 &lt;+ugha2p&gt; Ragnarok: Well, not really fucked, but just located at the end of the page.
13:49 &lt;@jrandom&gt; cool Ragnarok, thanks
13:49 &lt;Ragnarok&gt; your window's probably not wide enough
13:49 &lt;+ugha2p&gt; Ragnarok: Right, but it should work with any window size.
13:50 &lt;+ugha2p&gt; So you might want to fix it in the future. :)
13:50 &lt;Ragnarok&gt; ugha2p: should is an interesting choice of words :)
13:50 &lt;Frooze&gt; ah, wrong in mozilla 1.7 too.  my window is small though.
13:50 &lt;+ugha2p&gt; Why's that?
13:50 &lt;Frooze&gt; thanks ragnarok.  cool stuff.
13:51 &lt;Ragnarok&gt; I may fix it in the future, but it's really low on my priorities
13:51  * jrandom prefers addressbook updates to html fixes
13:52 &lt;Ragnarok&gt; anyhoo, any questions?
13:53 &lt;frosk&gt; thanks for addressbook, Ragnarok, sounds very useful
13:54 &lt;+ugha2p&gt; Is the documented way of loading addressbook the only way, or are there any less intrusive ones?
13:54 &lt;kaji&gt; i just installed it, it rocks
13:54 &lt;Ragnarok&gt; you can start it by hand using "java -jar addresbook.jar &lt;path to i2p/addressbook&gt;"
13:54 &lt;Ragnarok&gt; thank you :)
13:55 &lt;kaji&gt; oh, and i dled version 2.0.0 is there an update someware?
13:55 &lt;Ragnarok&gt; ok, I fixed the column, it was just a stupid mix of absolute and realitive sizes
13:56 &lt;Ragnarok&gt; yep, there's 2.0.1 up now on ragnarok.i2p
13:57 &lt;+ugha2p&gt; I'm getting "Failed to load Main-Class manifest attribute from" now, but never mind, I'll do a restart later.
13:57 &lt;Ragnarok&gt; whoops
13:58 &lt;Ragnarok&gt; that's my bad
13:58 &lt;Ragnarok&gt; I'll try to fix that soon
13:58 &lt;+ugha2p&gt; Ah, okay. :)
13:58 &lt;Ragnarok&gt; there will also be an easy to install .war version soon
13:59 &lt;dm&gt; jrandom: you are a machine
14:00 &lt;@jrandom&gt; wikked, thanks Ragnarok 
14:00 &lt;@jrandom&gt; susi23: ping?
14:00 &lt;susi23&gt; 1200ms
14:01 &lt;@jrandom&gt; !thwap
14:01 &lt;@jrandom&gt; anyway, wanna give us a rundown on whats up w/ susidns?
14:01 &lt;@jrandom&gt; or should that wait for later?
14:01 &lt;susi23&gt; do we have time for a more general discussion about naming stuff?
14:02 &lt;susi23&gt; what features we want in the future?
14:03 &lt;@jrandom&gt; some of my thoughts are posted up on http://dev.i2p.net/pipermail/i2p/2004-February/000135.html
14:03 &lt;@jrandom&gt; (for what general features)
14:04 &lt;@jrandom&gt; i think the hardest thing will be weaning people off globally unique human readable names, but with some good interfaces it should be doable
14:04 &lt;Ragnarok&gt; implementing the data structures you outlined in xml is one of my next goals
14:04 &lt;susi23&gt; ok, there is a small writing about attributes at http://susi.i2p/removablekeys.html
14:05 &lt;ant&gt; &lt;Jnymo&gt; wow.. pretty crowded in here tonight
14:05 &lt;bens&gt; ragnarok: have you checked out YAML? Might be easier
14:05 &lt;+ugha2p&gt; Jnymo: Yeah, we're trying to hold a meeting here.
14:05 &lt;Ragnarok&gt; YAML's name is far too apt
14:05 &lt;@jrandom&gt; cool susi23, though i think we'll definitely want to migrate away from the plain hosts.txt format
14:05 &lt;ant&gt; &lt;Quadn-werk&gt; addition of a command line graceful restart?
14:06 &lt;ant&gt; &lt;Jnymo&gt; ugha2p: ah
14:06 &lt;susi23&gt; are there any ideas how to keep names unique in the long run?
14:06 &lt;@jrandom&gt; one of the important parts of the data to be managed in the naming service is for an entry to be signed, requiring some hard structure (or careful xml)
14:07 &lt;@jrandom&gt; i dont believe in globally unique human, human readable, and secure names.
14:07 &lt;@jrandom&gt; (i bundle centralized & secure together)
14:07 &lt;@jrandom&gt; susi23: have you seen http://zooko.com/distnames.html ?
14:07 &lt;Ragnarok&gt; I think using an addressbook like system, the names will end up being mostly unique, since it's in the interest of the person claiming a name not to choose one that's already in use
14:08 &lt;@jrandom&gt; Ragnarok: we'll see.  perhaps
14:08 &lt;susi23&gt; i'll check this out
14:08 &lt;bens&gt; I suspect trusted authorities will emerge
14:08 &lt;Ragnarok&gt; well, there already is one
14:08 &lt;frosk&gt; hosts.txt? :)
14:09 &lt;Ragnarok&gt; jrandom's, yeah
14:09 &lt;@jrandom&gt; or if not trusted authorities, names that include the path to uniquely identify it
14:09 &lt;@jrandom&gt; (e.g. "the site orion.i2p calls 'frosk.i2p'")
14:10 &lt;@jrandom&gt; Derek Eddington had some posts along those lines in september - http://dev.i2p.net/pipermail/i2p/2004-September/000432.html
14:10 &lt;bens&gt; frosk.orion.i2p
14:10 &lt;@jrandom&gt; smtp.frosk.ns.orion.i2p
14:11  * jrandom starts building uucp bang paths
14:11 &lt;frosk&gt; hah
14:12 &lt;susi23&gt; ok, what now... how about a "naming roadmap"? :)
14:12 &lt;ant&gt; &lt;Jnymo&gt; you guys have swayed me away from an absolute distributed dns for i2p.. somewhat.. but ducks ideas started me thinking that a trust system might work.. like, a lookup could bring back a list of sites/files, and each could be listed with the amount of trust that the network gives it
14:12 &lt;susi23&gt; once we agreed what to do
14:12 &lt;@jrandom&gt; thats a good idea susi23, wanna write one up?
14:13 &lt;@jrandom&gt; trusting other people's trust has potential, but needs to be done very carefully
14:13 &lt;susi23&gt; I could do this, but I still have no idea WHAT we want to do. There are some decisions to make.
14:14 &lt;@jrandom&gt; (aka only according to the terms that you trust the peers along the chain to the trust author)
14:14 &lt;modulus&gt; there is or there should not be a "network trust" of a site, trust has to be user-centric always
14:14 &lt;@jrandom&gt; susi23: roadmap step 1: decide among $featureset
14:14 &lt;susi23&gt; Or at least we have to develop all ideas into a more precise concept.
14:14 &lt;ant&gt; &lt;Jnymo&gt; well, if it was explicitly simple.. like, if files i2p listed how many sites linked to siteinquestion.i2p
14:15 &lt;Ragnarok&gt; ok, the I've updated the addressbook package with an executable jar.
14:15 &lt;ant&gt; &lt;Jnymo&gt; er, files.i2p
14:15 &lt;@jrandom&gt; jnymo: that turns into a centralized authority - files.i2p
14:15 &lt;modulus&gt; not to say that you could poison the pool of links by establishing a shitload of sites.
14:16 &lt;modulus&gt; googlebombing on i2p
14:16 &lt;ant&gt; &lt;Jnymo&gt; true.. but files i2p could be decentralized
14:16 &lt;susi23&gt; ok, how about collection ideas/information/concepts until, lets say january
14:16 &lt;orion&gt; 'lo all. I see naming is on the table.. *again* :)
14:16 &lt;susi23&gt; then comes the decision phase, ok?
14:16 &lt;@jrandom&gt; sounds good - will you be the point of contact to gather that together?
14:16 &lt;Ragnarok&gt; sure
14:16 &lt;modulus&gt; doesn't matter if the trust aggregate is descentralized, trust has to emanate from the user. anything else can be poisoned imo.
14:17 &lt;susi23&gt; can't we take the mailinglist for this?
14:17 &lt;bob&gt; or perhaps ugha's wiki?
14:17 &lt;ant&gt; &lt;Jnymo&gt; agreed.. but what how to do that? put a little trust meter bar at the top of the web browser?
14:18 &lt;@jrandom&gt; the wiki would be good, we can gather links to all the previous discussions there
14:18 &lt;modulus&gt; jnyo: probably the most feasible solution is to bind to the first name encountered or something.
14:18 &lt;dm&gt; let's all give a hand of applause to jrandom for his wonderful project management
14:18 &lt;susi23&gt; fine
14:18 &lt;modulus&gt; but there are more ways than sausages.
14:19 &lt;susi23&gt; url to the wiki? (for the records)
14:19 &lt;ant&gt; * Jnymo claps
14:19 &lt;@jrandom&gt; ugha.i2p
14:19  * dm claps
14:19 &lt;susi23&gt; ok
14:19 &lt;susi23&gt; then I'm done and ping jrandom back ;)
14:20 &lt;ant&gt; &lt;Jnymo&gt; modulus: so, if i refer a link to someone else, i'm refering them to the site i first binded to.. that might work.. 
14:20 &lt;+ugha2p&gt; Looks like jrandom has ping timeouted.
14:20 &lt;@jrandom&gt; ok cool, anything else on nami^W nm, no more on naming.  on to the wiki
14:20 &lt;modulus&gt; anyway, if you're linking you'll probably want to put an absolute path in the link, not just a name
14:21 &lt;@jrandom&gt; moving forward to 4) eepsite roundup
14:21 &lt;dm&gt; dm.i2p is up and running
14:21 &lt;@jrandom&gt; cool
14:22 &lt;@jrandom&gt; ok, i dont really have much to add beyond whats mentioned in the mail
14:22 &lt;bob&gt; nice to see an influx of sites!  all speedy to access as well!
14:22 &lt;@jrandom&gt; aye, agreed bob
14:22 &lt;bob&gt; orion, thanks for your work.. I use your site daily.
14:22  * jrandom too, the 'last updated' is especially helpful
14:23 &lt;bob&gt; dm: :-)
14:24 &lt;@jrandom&gt; ok, if there's nothing more on that, we can jump to 5) ???
14:24 &lt;@jrandom&gt; is there anything else people want to bring up for the meeting?
14:24 &lt;ant&gt; &lt;Jnymo&gt; hows the net status?
14:24 &lt;ant&gt; &lt;Jnymo&gt; wrt 4.2.5?
14:25 &lt;@jrandom&gt; its looking good, but the release is only a few hours old, so too soon to tell
14:25 &lt;ant&gt; &lt;Jnymo&gt; oh, heh
14:25 &lt;ant&gt; &lt;Jnymo&gt; any fusenet news?
14:26 &lt;@jrandom&gt; (http://piespy.i2p/i2p/i2p-current.png heh)
14:26 &lt;frosk&gt; my work on i2pcontent has been largely put aside for some weeks, but the latest version of the document can be read at http://frosk.i2p/i2pcontent.html . if anyone is interested, do read, and do comment harshly if needs be (om irc when i'm not /away or mail to frosk@mail.i2p)
14:26 &lt;frosk&gt; i2pcontent/fusenet/anything ;)
14:26 &lt;ant&gt; &lt;Jnymo&gt; wordicus
14:28 &lt;@jrandom&gt; ok, if there's nothing else...
14:28 &lt;mule2&gt; tons of applause for all the excellent contributions
14:29 &lt;@jrandom&gt; aye, y'all are doing some kickass shit
14:29 &lt;frosk&gt; you too, jrandom :)
14:29 &lt;orion&gt; word.
14:29 &lt;orion&gt; yes, very much so, you too jrandom.
14:29 &lt;scintilla&gt; hear hear!
14:29 &lt;ant&gt; &lt;Jnymo&gt; yea, i noticed on the site, theres less info on how to help out
14:29 &lt;@jrandom&gt; sometimes kickass, sometimes ass kicked ;)
14:29 &lt;orion&gt; HIP HIP
14:30 &lt;ant&gt; &lt;Jnymo&gt; HORRAY
14:30  * orion smiles
14:30 &lt;Frooze&gt; downloaded eclipse today, to learn java over holiday, because y'all are so impressive.
14:30 &lt;@jrandom&gt; jnymo: many of the small easy-to-accomplish tasks have been done
14:30 &lt;@jrandom&gt; ooh wikked Frooze 
14:31 &lt;Frooze&gt; so, trouble on horizon.  heh
14:31 &lt;@jrandom&gt; jnymo: i really should collect some more of them though and post 'em
14:31 &lt;ant&gt; &lt;Jnymo&gt; jrandom: You still looking for someone to help out on alexandria.i2p?
14:31 &lt;@jrandom&gt; (take cover arizona!)
14:31  * jrandom is not involved in alexandria, but yes, i believe they are still looking for a librarian
14:31 &lt;ant&gt; &lt;Jnymo&gt; learn to swim, folks ;)
14:31  * orion loves pump up the volume references. Vague though they may be.
14:31 &lt;@duck&gt; yes we do
14:31 &lt;@jrandom&gt; :)
14:31 &lt;Ragnarok&gt; jrandom: where is the war actually supposed to go?
14:31 &lt;@jrandom&gt; (orion++)
14:32 &lt;@jrandom&gt; Ragnarok: i2p/webapps/addressbook.war
14:32 &lt;@jrandom&gt; (then restart the router)
14:32 &lt;ant&gt; &lt;Jnymo&gt; duck, you talkint to me?
14:32 &lt;Ragnarok&gt; cool.  I shall commence testing
14:32 &lt;@jrandom&gt; r0x0r
14:32 &lt;ant&gt; &lt;Jnymo&gt; duck: is alexandria on your site?
14:33 &lt;@duck&gt; duck.i2p/alexandria/
14:33 &lt;ant&gt; &lt;Jnymo&gt; word
14:34 &lt;@jrandom&gt; ok, if thats all, we can slide out of here @ the 90m mark..
14:34  * jrandom winds up
14:34  * jrandom *baf*s the meeting closed
</div>
