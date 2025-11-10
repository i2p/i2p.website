---
title: "I2P Dev Meeting - March 01, 2005"
date: 2005-03-01
author: "@jrandom"
description: "I2P development meeting log for March 01, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bla, cervantes, cervantes2p, ddd, detonate, duck, jnymo, jrandom, MichElle, null, Ragnarok, smeghead, ugha2p</p>

## Meeting Log

<div class="irc-log">
13:05 &lt;@jrandom&gt; 0) hi
13:05 &lt;@jrandom&gt; 1) 0.5.0.1
13:05 &lt;@jrandom&gt; 2) roadmap
13:05 &lt;@jrandom&gt; 3) addressbook editor and config
13:05 &lt;@jrandom&gt; 4) i2p-bt
13:05 &lt;@jrandom&gt; 5) ???
13:05 &lt;@jrandom&gt; 0) hi
13:05  * jrandom waves
13:05 &lt;@duck&gt; hi
13:05 &lt;@jrandom&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2005-March/000616.html
13:05 &lt;null&gt; hi
13:05 &lt;@jrandom&gt; (yeah, i'm late this week, off with my head)
13:06 &lt;@jrandom&gt; while y'all speedreaders dig through that, perhaps we can jump into 1) 0.5.0.1
13:07 &lt;@jrandom&gt; 0.5.0.1 is out, and gets rid of the most ovious bugs from 0.5, but as we've seen, there's still work to be done
13:07 &lt;@jrandom&gt; (current cvs stands at 0.5.0.1-7, I expect at least -8 or -9 before we hit 0.5.0.2)
13:07 &lt;+ugha2p&gt; Hi.
13:08 &lt;+ugha2p&gt; Does CVS HEAD fix that 100% CPU issue?
13:08 &lt;@jrandom&gt; yes, -7 should get the last remnants of it
13:08 &lt;@duck&gt; Does CVS HEAD fix that OOM issue?
13:08 &lt;+detonate&gt; hi
13:08 &lt;@jrandom&gt; no, the OOM is still being tracked down
13:09 &lt;@jrandom&gt; actually... is there a Connelly in the house?
13:09 &lt;ant&gt; &lt;jrandom&gt; nope
13:09 &lt;@jrandom&gt; bugger
13:09 &lt;+ugha2p&gt; jrandom must be going crazy, he is having a dialogue with himself.
13:09 &lt;@jrandom&gt; ok, well, we can see what will be done to get rid of the OOM.  its definitely a show stopper, so there won't be a release until its resolved one way or another
13:10 &lt;+detonate&gt; just in time for the meeting
13:11 &lt;@jrandom&gt; thats about all i have to say for the 0.5.0.1 stuff - anyone else have anything they want to mention/ask/discuss?
13:12 &lt;+ugha2p&gt; jrandom: Err, I haven't actually seen the CPU issue with 0.5.0.1, but it happened twice when I tried 0.5.0.1-5. Am I missing something?
13:12 &lt;+ugha2p&gt; I downgraded back to 0.5.0.1 as a result.
13:13 &lt;+detonate&gt; i had a question, the shutdown seems to take a very long time, and the memory usage spikes by about 40mb during that time
13:13 &lt;+detonate&gt; was wondering if you knew why
13:14 &lt;+detonate&gt; the immediate one, obviously
13:14 &lt;@jrandom&gt; it could happen with 0.5.0.1, you just hadn't run into it.  
13:14 &lt;@jrandom&gt; (its not a common occurrence, and it only hits some people in odd situations)
13:14 &lt;@jrandom&gt; detonate: very long, as in, more than the usual 11-12 minutes?
13:14 &lt;+ugha2p&gt; Well, it hit me twice during a 8-hour period.
13:15 &lt;+detonate&gt; once all the participating tunnels are gone
13:15 &lt;+ugha2p&gt; jrandom: Is it supposed to use up all the CPU and lose all the leases until restarted when that bug occurs?
13:16 &lt;@jrandom&gt; ugha2p: thats a typical result from the bug, yes
13:16 &lt;+detonate&gt; hmm
13:17 &lt;@jrandom&gt; (it happens when the # of tunnel build requests consume sufficient CPU to exceed the time to satisfy a request, causing an additional request to be queued up, etc)
13:17 &lt;+ugha2p&gt; Must have been an extreme coincidence that it only happened to me while on 0.5.0.1-5.
13:18 &lt;@jrandom&gt; ugha2p: its happened to some people repeatably on 0.5.0.1-0, but is fixed in -7.  you can stick with -0 if you prefer, of course
13:18 &lt;cervantes&gt; it was a wonderous godsend
13:18 &lt;+ugha2p&gt; jrandom: I'll try out -7.
13:18 &lt;@jrandom&gt; cool
13:19 &lt;+ugha2p&gt; Although I'm already feeling guilty for giving a bumpy ride to the wiki users so far. :)
13:20 &lt;+ugha2p&gt; One more thing, have you documented the bulk/interactive tunnel types anywhere?
13:20 &lt;+ugha2p&gt; (Except for the source ;)
13:20 &lt;@jrandom&gt; in the changelog.  the only difference is a max window size of 1 message
13:20 &lt;+ugha2p&gt; Oh, okay.
13:21 &lt;@jrandom&gt; ok, anything else on 0.5.0.1, or shall we move on over to 2) roadmap?
13:21 &lt;@duck&gt; move on!
13:21 &lt;@jrandom&gt; consider us moved
13:22 &lt;@jrandom&gt; roadmap updated.  'n stuff.  see the page for details
13:22 &lt;cervantes&gt; eeh, duck ankle bites
13:23 &lt;@jrandom&gt; i'm thinking of pushing some of the strategies from 0.5.1 to 0.6.1 (so we get UDP faster), but we'll see
13:23 &lt;@jrandom&gt; anyone have any questions/comments/concerns/frisbees?
13:23 &lt;+detonate&gt; have you heard from mule lately?
13:23 &lt;+detonate&gt; speaking of udp
13:24 &lt;@jrandom&gt; nope, he was fairly ill last i heard from 'im
13:24 &lt;+detonate&gt; :/
13:24 &lt;jnymo&gt; udp would kick ass
13:25 &lt;@jrandom&gt; s/would/will/
13:25 &lt;@jrandom&gt; hopefully he's off having fun instead though :)
13:25 &lt;+ugha2p&gt; jrandom: What kind of changes would the bandwidth and performance tuning include?
13:26 &lt;jnymo&gt; so, udp basically means connectionless.. which means.. bigger network, right
13:26 &lt;+detonate&gt; udp introduces all sorts of difficulties along with that
13:26 &lt;@jrandom&gt; ugha2p: batching the tunnel message fragments to fit better into the fixed 1024byte tunnel messages, adding per-pool bw throttles, etc
13:27 &lt;+detonate&gt; but yeah
13:27 &lt;@jrandom&gt; detonate: it won't be so bad, the token bucket scheme we have now can handle async requests without a problem
13:27 &lt;@jrandom&gt; (we just obviously wouldn't use the BandwidthLimitedOutputStream, but would ask the FIFOBandwidthLimiter to allocate K bytes)
13:27 &lt;+ugha2p&gt; Would the first one really make much difference? Per-pool throttling doesn't sound urgent.
13:28 &lt;+detonate&gt; that's good then
13:28 &lt;@jrandom&gt; ugha2p: likely, yes.  you can see the exact #s involved by going to /oldstats.jsp#tunnel.smallFragments
13:29 &lt;bla&gt; detonate: How's progress on the reassembly?
13:29 &lt;+detonate&gt; really stalled
13:30 &lt;@jrandom&gt; ugha2p: though its largely dependent upon the type of activity, of course.  chatty comm has more to gain, but bulk comm already fills the fragments fully
13:30 &lt;+ugha2p&gt; jrandom: Ok.
13:30 &lt;+ugha2p&gt; Right.
13:31 &lt;+detonate&gt; i stopped working on it completely and started working on the addressbook-editor
13:31 &lt;+detonate&gt; there's probably a really efficient, well-researched way of doing that sort of thing, but i haven't come across it 
13:31 &lt;jnymo&gt; will upd mean people behind nats can get through now?
13:31 &lt;@jrandom&gt; some jnymo 
13:31 &lt;jnymo&gt; and use i2p?
13:32 &lt;@jrandom&gt; but first we need to get it to work with udp at all, then we start adding the firewall/nat punching, then the PMTU, etc
13:32 &lt;jnymo&gt; that'll be a boon
13:33 &lt;+detonate&gt; of course if anyone has suggestions on what to do, i'd appreciate them
13:33 &lt;+ugha2p&gt; jrandom: How would UDP help people behind NATs?
13:34 &lt;bla&gt; detonate: TCP (on the regular net) does reassembly. Can those concepts be carried over to the I2P UDP reassembly?
13:34 &lt;+detonate&gt; i haven't looked into how tcp does it
13:34 &lt;@jrandom&gt; ugha2p: there's a lot of trickery we can pull off with consistent port #s, etc.  lots of code & docs out there
13:35 &lt;@jrandom&gt; bla: we'll certainly be using some level of UDP reassembly along tcp-SACK lines
13:35 &lt;+detonate&gt; but if you're going to handle most of what tcp does, you might as well go the NIO route and actually use it
13:35 &lt;+detonate&gt; saving the hassle
13:35 &lt;@jrandom&gt; no, there's substantial reason for why we do want both some reassembly/retransmission and not tcp
13:36 &lt;+detonate&gt; well, the threads thing
13:36 &lt;@jrandom&gt; the transport layer will not need to be fully reliable or ordered, just semireliable and unordered
13:37 &lt;+ugha2p&gt; Can we also expect a drop in memory usage because of fewer threads?
13:37 &lt;@jrandom&gt; yes
13:37 &lt;+ugha2p&gt; A significant drop
13:38 &lt;+ugha2p&gt; ?
13:38 &lt;@jrandom&gt; substantially.  (as well as a drop in memory usage, based off whatever the current OOM is coming from ;)
13:38 &lt;+ugha2p&gt; Right.
13:39 &lt;@jrandom&gt; ok, anything else on 2) roadmap?
13:39 &lt;bla&gt; jrandom: Yeah.
13:40 &lt;bla&gt; jrandom: Will detonate be doing the UDP stuff now? Or else, who will?
13:40 &lt;@jrandom&gt; its a team effort for all who can contribute :)
13:40 &lt;+detonate&gt; heh, i plan on working on udp stuff more, it's less boring than watching tv
13:41 &lt;@jrandom&gt; heh w3wt
13:41 &lt;bla&gt; jrandom: I understand. But for a moment it looked like detonate dropped the project ;)
13:42 &lt;@jrandom&gt; its on the roadmap, it will be done
13:42 &lt;+detonate&gt; sorry for the confusion
13:43 &lt;@jrandom&gt; ok anyone else have anything on 2) roadmap, or shall we mosey on over to 3) addressbook stuff?
13:44 &lt;@jrandom&gt; ok, detonate wanna give us an overview/status report on the editor?
13:45 &lt;bla&gt; detonate: (np)
13:45 &lt;+detonate&gt; ok
13:45 &lt;+detonate&gt; the current state of the editor is here:
13:45 &lt;+detonate&gt; http://detonate.i2p/addressbook-editor/current-state.html
13:45 &lt;+detonate&gt; it still doesn't do any actual editing
13:45 &lt;+detonate&gt; and currently i'm working on the table at the bottom
13:46 &lt;+detonate&gt; i need to read a couple chapters of my jsp book, but after that, you should be able to use it to add/modify entries in the hosts.txt and subscriptions quite easily
13:47 &lt;+detonate&gt; i took a break from it the last 24 hours or so, so that's why there hasn't been much progress
13:47 &lt;+detonate&gt; that's pretty much all
13:47 &lt;@jrandom&gt; w3wt
13:48 &lt;bla&gt; detonate: Looks good
13:49 &lt;@jrandom&gt; yeah, mos' def', I'm looking forward to a way to manage the entries /other/ than just hcaking the hosts file
13:49 &lt;+detonate&gt; thanks
13:49 &lt;+detonate&gt; that's the first time i've used jsp for anything
13:50 &lt;@jrandom&gt; cool
13:51 &lt;@jrandom&gt; oh, i hadn't realized there was the overlap here for subscription management - perhaps smeghead's work can fit in with this as well
13:51 &lt;@jrandom&gt; smeghead: you 'round?  you seen this yet?
13:51 &lt;jnymo&gt; detonate: will there be collision detection and what not?
13:51 &lt;@smeghead&gt; actually i only hashed out some skeleton code on the addressbook console, nothing useful
13:51 &lt;+detonate&gt; yeah, i got tired of that, thank duck for suggesting the idea :)
13:51 &lt;@smeghead&gt; i got sidetracked on the TrustedUpdate thingy
13:52 &lt;@jrandom&gt; ah cool :)
13:53  * jrandom likes sidetracking to add new features 
13:53 &lt;bla&gt; smeghead: You mean 1-click updates of I2P from _within_ I2P?
13:53 &lt;@smeghead&gt; so luck, not laziness (at least this time :)
13:53 &lt;cervantes2p&gt; bla: 2 click at least ;-)
13:54 &lt;@jrandom&gt; bah, we can get it down to 1 (reject if bad sig/invalid/etc ;)
13:54 &lt;+detonate&gt; yeah, there will be collision detection, that's currently what i'm working on
13:54 &lt;@jrandom&gt; detonate: doesnt the addressbook itself take care of that?
13:54 &lt;@jrandom&gt; detonate: i thought what you're doing just edited the files?  
13:55 &lt;@jrandom&gt; (the files will be uniq'ed by the addressbook)
13:55 &lt;+detonate&gt; i mean, showing you the collisions from the logs and handling that
13:55 &lt;@jrandom&gt; ah
13:55 &lt;@jrandom&gt; ok cool
13:55 &lt;+detonate&gt; i assume that's what jnymo is talking about
13:55 &lt;Ragnarok&gt; hm, is there anything I can do to make your life easier? :)
13:55 &lt;+detonate&gt; so you can say "replace entry" with the colliding one of your choice
13:55 &lt;@jrandom&gt; nice!
13:58 &lt;@jrandom&gt; Ragnarok: iirc detonate was able to parse out the logfile pretty easily.  do you forsee that format changing?
13:58 &lt;jnymo&gt; detonate: pretty much, yea
13:58 &lt;jnymo&gt; now, is this tied into i2p tightly?  How easily can i put a link+key from my browser into my address book?
13:59 &lt;+detonate&gt; yeah, don't change the format, that'll break everything
13:59 &lt;Ragnarok&gt; the format is highly unlikely to change
14:00 &lt;Ragnarok&gt; though more things may get logged in the future
14:00 &lt;@jrandom&gt; jnymo: the eepproxy doesn't have any hooks into detonate's editor atm, but we could add something down the road
14:00 &lt;+detonate&gt; although if you modified the Conflict lines, that would make them easier to parse
14:00 &lt;cervantes2p&gt; possibly something my firefox plugin could do
14:00 &lt;+detonate&gt; right now there are lots of human readable words that get in the way
14:00 &lt;Ragnarok&gt; modify how?
14:00 &lt;@jrandom&gt; (for instance, perhaps i2paddresshelper might redirect to an editor page)
14:00 &lt;cervantes2p&gt; "click here to add this to your addressbook"
14:00 &lt;Ragnarok&gt; ah...  I want to be nice to the humans, though
14:00 &lt;+detonate&gt; &lt;date&gt;=&lt;host&gt;=&lt;source&gt;=&lt;new destination&gt; would be superior
14:01 &lt;@jrandom&gt; cervantes2p: that going to work like google's page rewriter?  :)
14:01 &lt;+detonate&gt; well, that's what the addressbook-editor is for :)
14:01 &lt;+detonate&gt; it's really not an issue, i've got it covered
14:01 &lt;cervantes2p&gt; jrandom: nah...just have it in the link context menu
14:01 &lt;@jrandom&gt; ooOOoo
14:01 &lt;+detonate&gt; as long as nothing changes radically, things should keep working smoothly
14:02 &lt;cervantes2p&gt; of course I could add a rewriter...but that's just breaks people's page layouts ;-)
14:02 &lt;+detonate&gt; oh, one thing you could do
14:02 &lt;+detonate&gt; because it conflicts with what i do
14:02 &lt;+detonate&gt; make sure all the entries for the hostnames are all-lowercase
14:02 &lt;+detonate&gt; since Legion.i2p is in there
14:02 &lt;cervantes2p&gt; I do want to add a "non i2p link highlighter"
14:02 &lt;+detonate&gt; and i run them all through toLowercase()
14:02 &lt;@jrandom&gt; ah that'd be neat cervantes2p 
14:03 &lt;@jrandom&gt; (be sure to only toLowercase the names, base64 is case sensitive ;)
14:03 &lt;+detonate&gt; yeah, only the names
14:04 &lt;jnymo&gt; context menu would be ideal
14:04 &lt;@jrandom&gt; (dont forget the flying ponies!)
14:04 &lt;Ragnarok&gt; I've made address comparisons non-case sensitive in my local branch... I should commit that...
14:04 &lt;+detonate&gt; /make all the hostnames lowercase
14:04 &lt;+detonate&gt;                 pair[0] = pair[0].toLowerCase();
14:05 &lt;+detonate&gt; there, in black and white
14:05 &lt;+detonate&gt; it just does the hostnames
14:05 &lt;@jrandom&gt; aye Ragnarok, give us the goods :)
14:05 &lt;jnymo&gt; why do i always feel i'm the one riding the flying ponies :(
14:06 &lt;@jrandom&gt; thats 'cause you're hoggin' 'em jnymo ;)
14:06 &lt;cervantes2p&gt; jnymo: don't discuss your domestic "arrangements" in a meeting
14:07 &lt;@jrandom&gt; ok, lots of cool stuff going on within the addressbook & editor.  any eta on when we can beta things detonate?  (this week, next week, etc)
14:07 &lt;jnymo&gt; heh
14:07 &lt;+detonate&gt; well, as soon as you can get it to work in jetty, you can put it in beta i think
14:07  * jnymo pulls out his p32-space-modulator
14:07 &lt;@jrandom&gt; it works in jetty
14:07 &lt;+detonate&gt; i have no idea how to get netbeans to precompile them and put them in the war
14:08 &lt;+detonate&gt; as long as people don't change the names of the files in config.txt, it should work hopefully without bugs
14:08 &lt;@jrandom&gt; ok, we can work you through ant to take care of things
14:08 &lt;+detonate&gt; ok
14:08 &lt;+detonate&gt; cool
14:08 &lt;cervantes2p&gt; detonate: do what I did, take jrandom's code....strip out everything you don't need, crowbar in your own code and run the ant build script ;-)
14:08 &lt;@jrandom&gt; heh
14:09 &lt;@smeghead&gt; detonate: i know a thing or two about ant, yell if ya get stuck
14:09 &lt;+detonate&gt; feel free to add it to your release
14:09 &lt;+detonate&gt; if you know how to do that
14:09 &lt;MichElle&gt; s/you don't need//
14:09 &lt;Ragnarok&gt; addressbook has a very simple build script, if you want to take a look at that
14:10 &lt;+detonate&gt; i need the section that precompiles jsps
14:10 &lt;+detonate&gt; that's missing from mine
14:10 &lt;+detonate&gt; although it does compile them, it just doesn't merge them, and the entry to test compile them isn't in build.xml
14:10 &lt;@jrandom&gt; detonate: check out the precompilejsp targets in routerconsole, that'll get you started
14:10 &lt;+detonate&gt; and i need to figure out where to put -source 1.3 etc in
14:10 &lt;@jrandom&gt; (and the &lt;war&gt; task)
14:11 &lt;+detonate&gt; yeah, we can sort things out later this evening
14:11 &lt;@jrandom&gt; aye
14:11 &lt;cervantes&gt; yup that's how I managed it...and I don't know ANY java or jsp ;-)
14:11 &lt;@jrandom&gt; ok, if there's nothing more on 3) addressbook stuff, moving on to 4) bt stuff
14:12 &lt;@jrandom&gt; duck/smeghead: wanna give us an update?
14:12 &lt;@duck&gt; k
14:12 &lt;@duck&gt; last week we spoke with Nolar from Azureus about fixing some compatibility problems
14:12 &lt;@duck&gt; with the release of 0.1.8 as result
14:12 &lt;@duck&gt; this week has been mostly about communication
14:12 &lt;@duck&gt; with fellow developers, with forum admins and with users
14:13 &lt;+detonate&gt; does anyone know if the aznet plugin can host torrents again?
14:13 &lt;@duck&gt; the FAQ has been updated based on input from the forum, thanks for those who contributed
14:13 &lt;@duck&gt; also there has been some miscommunication and confusion
14:13 &lt;@jrandom&gt; detonate: word on the street is yes
14:13 &lt;@duck&gt; like legions spork
14:13 &lt;+detonate&gt; excellent
14:13 &lt;@duck&gt; I believe that changing the name of it will prevent further problems there
14:13 &lt;@duck&gt; .
14:14 &lt;@jrandom&gt; r0xor duck
14:14  * MichElle applauds duck
14:14 &lt;MichElle&gt; duck: you work very hard
14:14 &lt;jnymo&gt; yea, why not i2p-bt_extractor or some shit?
14:15 &lt;@jrandom&gt; any word on the later 0.2 stuff, or is that to be addressed after 0.5.0.2/etc?
14:15 &lt;@smeghead&gt; don't applaud yet, you don't know what we're naming it&gt;;-}
14:15 &lt;@jrandom&gt; heh
14:15  * jnymo claps
14:15 &lt;@duck&gt; tell us!
14:15 &lt;@jrandom&gt; i2p-flying-pony-torrent
14:16 &lt;+detonate&gt; heh, are we hiding it now by changing the name?
14:16 &lt;MichElle&gt; again with the ponies
14:16 &lt;@smeghead&gt; it's top-secret for now, we don't want to get sued
14:16 &lt;jnymo&gt; what a debocle
14:17  * bla makes sign for MPAA: "Sue me, if you can..."
14:17 &lt;@smeghead&gt; duck and i have agreed 0.2 will be the first version with the new name
14:17 &lt;+detonate&gt; i2p-communism
14:17 &lt;@duck&gt; released spring 2006
14:17 &lt;@jrandom&gt; heh
14:17 &lt;@duck&gt; .
14:18 &lt;@smeghead&gt; based on my current workload and the fact that i'm moving this week, i don't expect to get any hacking done on 0.2 for a few days, i don't know what duck's near-term schedule is like
14:18 &lt;@duck&gt; been doing 8 hours of C++ pointer fixing
14:19 &lt;@duck&gt; so not much here either :)
14:19 &lt;@jrandom&gt; 'k but something we can perhaps look forward to along side 0.6 (or 0.5.1 if we're lucky?)
14:19 &lt;@jrandom&gt; yikes, fun fun fun
14:19 &lt;@duck&gt; before 2.0 atleast
14:19 &lt;@smeghead&gt; i'd estimate a month or so, just a wild guess, what do you think duck
14:19 &lt;@duck&gt; yeah
14:19 &lt;@jrandom&gt; cool
14:19 &lt;@duck&gt; ballpark
14:20 &lt;@smeghead&gt; the thing is we'd like to wait until the release of the official BT 4.0
14:20 &lt;@jrandom&gt; its ok, we know how schedules go ;)
14:20 &lt;@smeghead&gt; so we can sync 0.2 up-to-date with that
14:20 &lt;MichElle&gt; duck has many things on his plate, indeed
14:20 &lt;@smeghead&gt; 4.0 appears imminent
14:20 &lt;@jrandom&gt; ah, really smeghead?  cool
14:20 &lt;@duck&gt; smeghead: that is just the official excuse :)
14:20 &lt;MichElle&gt; but he is a hard worker
14:21 &lt;@duck&gt; I am for 5) ???
14:21 &lt;@jrandom&gt; almost there... 
14:21 &lt;@jrandom&gt; legion: any updates on your bt client?  progress, etc?
14:21 &lt;@smeghead&gt; source code?
14:22 &lt;@smeghead&gt; (in a zip, not an .exe)
14:22 &lt;cervantes&gt; so the next wave of releases then
14:22 &lt;@jrandom&gt; hmm, legion seems to be idle, ok perhaps we can get an update later
14:22 &lt;cervantes2p&gt; damn huge lag
14:23 &lt;@jrandom&gt; so, movin' on over to 5) ???
14:23 &lt;cervantes&gt; *ahem* w00t
14:23 &lt;@jrandom&gt; cervantes2p: nah, you're just slow ;)
14:23 &lt;@jrandom&gt; ok, anyone else have anything to bring up?
14:23 &lt;cervantes2p&gt; I said those things like 5 minutes ago
14:23 &lt;+ugha2p&gt; jrandom: The mailing list footer still uses the i2p.dnsalias.net address. Perhaps you should update it to reflect dev.i2p.net? :)
14:23  * cervantes2p feeds his router's hamster
14:24 &lt;@jrandom&gt; ah, yeah, prolly ugha2p 
14:24  * jrandom has some sysadmin work i've been avoiding for a while (like, oh, moving things to the new srever...)
14:24 &lt;MichElle&gt; I have a concern
14:24 &lt;MichElle&gt; regarding transparency
14:24 &lt;@jrandom&gt; sup MichElle?
14:25 &lt;MichElle&gt; for purposes of full transparency, I will declare here that identiguy has suggested jrandom could in fact be employed by the NSA
14:25 &lt;+detonate&gt; oh, i've noticed 190 routers, how close are we to the thread limit right now?
14:25  * jnymo wonders about other help people can do
14:25 &lt;jnymo&gt; (still looking into the php thing, duck ;)
14:25 &lt;@jrandom&gt; heh MichElle
14:25 &lt;MichElle&gt; his 'convenient' ability to work 24/7 on i2p is quite suspicious, indeed
14:25 &lt;MichElle&gt; anyway
14:25 &lt;MichElle&gt; that's all I wanted to say
14:25 &lt;MichElle&gt; keep your eyes on jrandom
14:26 &lt;MichElle&gt; his gentle and warm facade may be just that.
14:26 &lt;+ugha2p&gt; detonate: There are no theoretical thread limits, it will just consume all available resources until it crashes. :)
14:26 &lt;jnymo&gt; facade
14:26 &lt;@jrandom&gt; detonate: some OSes/ulimits may throttle @ 256, but win98 is already past the 100 TCP connections limit anyway
14:26 &lt;cervantes2p&gt; I can give a quick update on the firefox plugin. The I2P Mail notifier is working now, as is the news reader and basic router controls. I'm busy with tediously building configuration screens now ( http://freshcoffee.i2p/fire2pe_i2pmail_prefs.jpg )
14:27 &lt;jnymo&gt; MichElle, if the source code is sound, then who cares?
14:27 &lt;+detonate&gt; oh, is the firefox plugin released?
14:27 &lt;MichElle&gt; jnymo: it ruins the mood a little
14:27 &lt;cervantes2p&gt; and I want to implement a downloader/install service that ties into smeghead's new updater verifier before I release
14:27 &lt;ddd&gt; hi channel
14:28 &lt;+detonate&gt; ok
14:28 &lt;@jrandom&gt; w0ah! kickass cervantes2p 
14:28 &lt;@jrandom&gt; it looks really nice
14:28 &lt;+detonate&gt; hi ddd
14:28 &lt;cervantes2p&gt; but getting close now...probably another couple of weeks...
14:28 &lt;MichElle&gt; sort of like how running windows would still not be cool, even if microsoft open-sourced it
14:28 &lt;+detonate&gt; that plugin looks cool
14:28 &lt;MichElle&gt; back to the meeting, though ...
14:28 &lt;@smeghead&gt; TrustedUpdate may be done this week hopefully, before i move
14:28 &lt;@jrandom&gt; cool
14:29 &lt;ddd&gt; ?
14:29 &lt;ddd&gt; is i2p the only anonymous chat?
14:29 &lt;@jrandom&gt; hi ddd .  weekly dev meeting going on
14:30 &lt;cervantes2p&gt; 'lo ddd, we're just finishing a meeting...stick around we'll be done in a couple of minutes
14:30 &lt;ddd&gt; are there other projects like i2p?
14:30 &lt;@smeghead&gt; ddd: type /list then take your pick
14:30 &lt;ddd&gt; ok
14:30 &lt;ddd&gt; no i mean on other networks
14:30 &lt;@jrandom&gt; ok, anyone else have anything to bring up for 5) ???
14:30 &lt;@smeghead&gt; ddd: ask in #i2p-chat
14:30 &lt;ddd&gt; ok i let you guys finish
14:30 &lt;+detonate&gt; has anyone successfully run i2p in openbsd yet?
14:31 &lt;@jrandom&gt; ddd: http://www.i2p.net/how_networkcomparisons
14:31 &lt;ddd&gt; ok
14:31 &lt;+detonate&gt; i was thinking of starting that fiasco up again
14:31 &lt;@jrandom&gt; detonate: dunno
14:31 &lt;jnymo&gt; oh yea.. who was doing the bsd i2p distro, and which bsd was it?
14:31 &lt;@jrandom&gt; heh cool detonate, let us know how it goes
14:31 &lt;@jrandom&gt; jnymo: lioux packaged 'er up for fbsd
14:32 &lt;@smeghead&gt; i2p would never ship with openbsd :)
14:32 &lt;+detonate&gt; sure
14:32 &lt;jnymo&gt; woord..  wasn't someone going to do a i2p oriented distro?
14:32 &lt;+detonate&gt; yeah, there's a port in freebsd now
14:32 &lt;+detonate&gt; it's scary
14:32 &lt;+detonate&gt; heh, someone wanted to have a knoppix cd that ran i2p
14:32 &lt;@jrandom&gt; jnymo: after i2p is rock solid, it'd be worthwhile to explore packaging on distros/microdistros, yeah
14:32 &lt;+detonate&gt; who knows why
14:33 &lt;@smeghead&gt; jnymo: i remember that, i think it was going to be a knoppix/i2p, can't recall who was talking about it
14:33 &lt;@jrandom&gt; detonate: netcafe
14:33 &lt;+detonate&gt; ah
14:34 &lt;@jrandom&gt; ok, anything else for the meeting?
14:34 &lt;MichElle&gt; what the fuck is an i2p 'oriented' distro
14:34 &lt;MichElle&gt; tor, i2p, and freenet ?
14:34 &lt;MichElle&gt; there is no purpose
14:34 &lt;MichElle&gt; the bandwidth requirements cancel the programmes out
14:34 &lt;MichElle&gt; is jrandom theo de raadt ?
14:34 &lt;cervantes&gt; a slightly camp distribution
14:34 &lt;jnymo&gt; a completely anonymized distro
14:35 &lt;cervantes2p&gt; jrandom: I guess not :)
14:35 &lt;MichElle&gt; jrandom: nothing
14:35  * jrandom winds up
14:35  * jrandom *baf*s the meeting closed
</div>
