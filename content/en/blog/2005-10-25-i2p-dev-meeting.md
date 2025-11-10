---
title: "I2P Dev Meeting - October 25, 2005"
date: 2005-10-25
author: "jrandom"
description: "I2P development meeting log for October 25, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cat-a-puss, cervantes, Complication, dust, jme\___, jnymo\_, jrandom, legion, Ragnarok, reliver, Romster, shardy, susi23</p>

## Meeting Log

<div class="irc-log">
16:24 &lt;jrandom&gt; 0) hi
16:24 &lt;jrandom&gt; 1) Net status
16:24 &lt;jrandom&gt; 2) Fortuna integration
16:24 &lt;jrandom&gt; 3) GCJ status
16:24 &lt;jrandom&gt; 4) i2psnark returns
16:24 &lt;jrandom&gt; 5) More on bootstrapping
16:24 &lt;jrandom&gt; 6) Virus investigations
16:24 &lt;jrandom&gt; 7) ???
16:24 &lt;jrandom&gt; 0) hi
16:24  * jrandom waves
16:24 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2005-October/001079.html
16:25  * susi23 waves back
16:26 &lt;jrandom&gt; lets jump on in to 1) net status
16:26 &lt;jrandom&gt; as I mentioned, things look pretty reasonable so far.  
16:26 &lt;+fox&gt; &lt;Romster&gt; ah meeting sweet
16:27 &lt;jrandom&gt; there is some good stuff coming down the line too, so we'll have a new release later this week
16:27 &lt;jrandom&gt; anyone have anything they want to bring up regarding 1) net status?
16:27 &lt;@cervantes&gt; omg 7 issues
16:27 &lt;+legion&gt; yup looking good :-)
16:27 &lt;jrandom&gt; busy week cervantes :)
16:28 &lt;@cervantes&gt; can only be good
16:28 &lt;+Complication&gt; Works relatively well, dev.i2p even - I can even pull CVS checkouts without EOF messages.
16:28 &lt;jrandom&gt; nice :)
16:28 &lt;+Complication&gt; Might have been release-related overloads, those last ones.
16:28 &lt;+Complication&gt; But I can't tell.
16:28 &lt;jrandom&gt; dev.i2p is on the latest build code too (-7), so it'll be hopefully performing substantially better than before
16:29 &lt;jrandom&gt; s/dev.i2p/cvs.i2p (etc)/
16:29 &lt;+legion&gt; forums.i2p also seems to be much better than before :)
16:29 &lt;@cervantes&gt; *ahem*
16:29 &lt;+fox&gt; &lt;Romster&gt; is i2p safe to let others join etc?
16:29 &lt;+Ragnarok&gt; ok, now I've got to try this miraculous "cvs checkout that works the first time"
16:30 &lt;+fox&gt; &lt;Romster&gt; since there is no known limits now
16:30 &lt;@cervantes&gt; that's because everyone's hammering i2p-list instead of posting to the forum 
16:30 &lt;+legion&gt; hmm you sure cervantes?
16:30 &lt;jrandom&gt; Romster: well, we've been growing at a pretty good pace lately, but we should hold off on public beta until 0.6.2
16:30 &lt;jrandom&gt; heh cervantes ;)
16:30 &lt;jrandom&gt; hush Ragnarok, you'll jinx it!
16:31 &lt;+Ragnarok&gt; wow... it's true.  I'm speechless
16:31 &lt;+fox&gt; &lt;Romster&gt; k jrandom
16:31 &lt;jrandom&gt; (man my eyes are watering from the curry my roomates are cooking downstairs)
16:31 &lt;jrandom&gt; nice1 Ragnarok 
16:32 &lt;+fox&gt; &lt;Romster&gt; lol now that's a strong curry
16:32 &lt;jrandom&gt; ok, if there's nothing else on 1), we can jump quickly through 2) Fortuna integration
16:32 &lt;jrandom&gt; (true that Romster)
16:32 &lt;+fox&gt; &lt;shardy&gt; yay for fortuna integration!
16:32 &lt;+fox&gt; &lt;Romster&gt; moving onto 2) :P
16:32 &lt;+fox&gt; &lt;Romster&gt; what is fortuna?
16:32 &lt;jrandom&gt; heh thought you'd like that shardy :)
16:32 &lt;+fox&gt; &lt;Romster&gt; i've been a bit behind the last month
16:32 &lt;+Complication&gt; PRNG algo, if I remember.
16:33 &lt;+Complication&gt; Supposedly a good one, or so they write. :P
16:34  * Complication knows nothing about its inner workings, though
16:34 &lt;jrandom&gt; shardy: I'd love if you could give it a look sometime
16:34 &lt;+fox&gt; &lt;shardy&gt; of course
16:34 &lt;+fox&gt; &lt;shardy&gt; you're using the gnu implementation?
16:34 &lt;jrandom&gt; Romster/Complication: there are some links in the email
16:34 &lt;jrandom&gt; yeah shardy - http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/core/java/src/gnu/crypto/prng/Fortuna.java
16:35 &lt;jrandom&gt; (integrated with http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/core/java/src/net/i2p/util/FortunaRandomSource.java )
16:36 &lt;jrandom&gt; we vary from the straight gnu-crypto implementation though, since we've already got AES256 and SHA256 code (Cryptix's and Bouncycastle's, respectively)
16:36 &lt;jrandom&gt; ok, anyway, this looks cool, as we've been hacking through getting that support in there for probably a year now
16:37 &lt;jrandom&gt; (fortuna integration was one of the main projects driving smeghead to build 'pants' ;)
16:37 &lt;jrandom&gt; if anyone has any questions/comments/concerns about it, please bounce 'em to the list
16:37 &lt;jrandom&gt; (or email, or forum, of course)
16:38 &lt;+fox&gt; &lt;Romster&gt; yeah where is smeghead hes not been around for awhile now
16:38 &lt;jrandom&gt; smeghead is [redacted] doing [redacted]
16:39 &lt;jrandom&gt; ok, moving on to 3) GCJ status
16:39 &lt;jrandom&gt; i2p works on GCJ!  [w00t!]
16:39 &lt;+susi23&gt; nice job
16:39 &lt;+legion&gt; sweet
16:39 &lt;jrandom&gt; at least, it does on GCJ 4.0.2 on linux 2.6.12.  I haven't tried any other platforms
16:40 &lt;jrandom&gt; yeah, the GCJ and GNU Classpath folks have worked wonders
16:40 &lt;jrandom&gt; it was really easy to get it building, the old static reference classes I remember weren't necessary
16:41 &lt;+Complication&gt; Which sounds quite positive, given Sun Java's less-than complete openness (with regard to distribution, if I remember correct).
16:41 &lt;jrandom&gt; there's a makefile shipped with I2P now, though for simplicity, I think we'll probably stick with distributing pure java, at least primarily
16:41 &lt;+susi23&gt; (next we try to run it on J2ME ;)
16:42 &lt;+fox&gt; &lt;Romster&gt; GCJ to take over Suns JVM&gt;
16:42 &lt;cat-a-puss&gt; how is preformance with GCJ?
16:42 &lt;jrandom&gt; aye, though sun is entirely open, and we /could/ distribute their JVM along side I2P, but their license prohibits distributing their JVM as a general purpose tool
16:42 &lt;jrandom&gt; cat-a-puss: comparable
16:42 &lt;jrandom&gt; most of the heavy work in i2p is already done by assembler code ;)
16:43 &lt;+fox&gt; &lt;Romster&gt; how would i2p go with C#/mono again with that jave to C# adition (forgot it's name)
16:43 &lt;+fox&gt; &lt;Romster&gt; i remember jrandom and i both tryed it out ages ago
16:43 &lt;jrandom&gt; no idea.  but if it works with gcj, it might work with ikvm - the mono jvm thing
16:44 &lt;+Ragnarok&gt; IKVM
16:44 &lt;+Ragnarok&gt; nm
16:44 &lt;+fox&gt; &lt;Romster&gt; ah tahts the one ikvm
16:44 &lt;+fox&gt; &lt;Romster&gt; much difereances with GCJ and IKVM and Sun's?
16:45 &lt;jrandom&gt; i've never used ikvm
16:45 &lt;+fox&gt; &lt;Romster&gt; i'm sure you have once with mono or was that eclipse?
16:45 &lt;+fox&gt; * Romster shrugs
16:45 &lt;jrandom&gt; and i2p as shipped doesn't currently support the router console, though it does support the router operation, i2ptunnel, and sam
16:46 &lt;+Ragnarok&gt; what's blocking the router console?
16:47 &lt;+susi23&gt; xerces, when I remember correctly
16:47 &lt;jrandom&gt; xerces stuff.  the xercesImpl shipped with i2p has sun.* dependencies, and when I naively tried to drop in the latest xerces, getting that and jdom and rome and the rest of jetty GCJed was b0rking
16:47 &lt;jrandom&gt; there are some additional requirements of the latest xerces, it seems
16:48 &lt;jrandom&gt; (for jar files we don't currently ship).  however, I'm sure we can track it down
16:49 &lt;+fox&gt; &lt;Romster&gt; jrandom is good at tracking down problems :)
16:49 &lt;jrandom&gt; even better at making problems
16:49 &lt;+fox&gt; * Romster featches a coffee
16:49 &lt;jrandom&gt; ok, anything else on 3) GCJ status?
16:49 &lt;jrandom&gt; or shall we move on to 4) i2psnark
16:50 &lt;jrandom&gt; consider us moved
16:50 &lt;jrandom&gt; ok, i2psnark is back (yay)
16:51 &lt;jrandom&gt; not much I have to add to whats in the mail... you have anything Ragnarok?
16:51 &lt;+Ragnarok&gt; nope
16:51 &lt;+susi23&gt; regarding web frontend
16:51 &lt;+Ragnarok&gt; more testing would be nice though, so everyone should try it :)
16:52 &lt;+susi23&gt; supporting it with susibt shouldn't be a problem
16:52 &lt;jrandom&gt; ooh give us the scoop susi23 :)  
16:52 &lt;jrandom&gt; nice
16:52 &lt;+fox&gt; &lt;jme___&gt; naive question, why spending time supporting old bt client while other (azureus) support full blown client ?
16:52 &lt;jrandom&gt; jme___: azureus *is* kickass
16:52 &lt;+susi23&gt; major release of susibt is scheduled for november :)
16:53 &lt;jrandom&gt; heh cool susi23 
16:53 &lt;+Complication&gt; To me, Azureus seemed terribly complex.
16:53 &lt;+Ragnarok&gt; azureus blows monkey chunks
16:53 &lt;+susi23&gt; for me, I always need a headless solution
16:53 &lt;+Ragnarok&gt; not to put too fine a point on it
16:53 &lt;+fox&gt; &lt;jme___&gt; ok :)
16:53 &lt;jrandom&gt; jme___: azureus is a bit heavyweight though, but is a great general purpose bt solution
16:53 &lt;+Complication&gt; (I personally could see the day I'd misconfigure something in it, and dent my anonymity.)
16:54 &lt;+fox&gt; &lt;jme___&gt; it make sense, just wanted to know
16:54 &lt;+fox&gt; &lt;Romster&gt; to me azerious never workd well i've moved to bitlord which does work
16:54 &lt;jrandom&gt; i do still plan on helping further improve the azneti2p plugin with the azureus folks, but i2psnark took literally less than 2 hours before I was swarming data
16:54 &lt;+legion&gt; Yeah azureus is just too big and complicated for i2p
16:54 &lt;+Complication&gt; If the goal is bundling a bt client along with i2p, a lightweight client sounds best.
16:54 &lt;+fox&gt; &lt;Romster&gt; KISS principal
16:54 &lt;+Ragnarok&gt; I like the official client best, but i2psnark has the major advantage of being simple enough for me to hack on
16:55 &lt;+legion&gt; thing is i2p doesn't need a heavyweight bittorrent client
16:55 &lt;jrandom&gt; yeah, its really clean code (with oddball gnu formatting ;)
16:55 &lt;+Ragnarok&gt; damn gnu
16:55 &lt;+Ragnarok&gt; worst brace style ever
16:55 &lt;jrandom&gt; heh
16:55 &lt;+fox&gt; &lt;Romster&gt; heh code reformatter :)
16:55 &lt;+Ragnarok&gt; jrandom won't let me :)
16:55 &lt;+Ragnarok&gt; well, for good reason
16:55 &lt;+fox&gt; &lt;jme___&gt; independance and simplicity are criteria i definitly agree with
16:56 &lt;+fox&gt; &lt;Romster&gt; will there be options to enable the bt-torrent program on each i2p node?
16:56 &lt;jrandom&gt; aye, it'd be nice if we can backport multitorrent, piece selection, and web capacity to mjw's mainline snark
16:56 &lt;+Ragnarok&gt; the simpler it is, the more likely it will be maintained
16:56 &lt;jrandom&gt; exaaactly Ragnarok 
16:57 &lt;+legion&gt; yeah backporting those would be killer
16:57 &lt;+fox&gt; &lt;Romster&gt; as a OT point here take a look at emules KAD network i think it's rather neat.
16:57 &lt;jrandom&gt; Romster: its now shipped with the build by default, but once we get it into susibt, it'll be on the top nav with the rest of the clients
16:58 &lt;+Ragnarok&gt; we need to be able to ship a .torrent maker as well, though.  And a tracker would be nice.
16:58 &lt;jrandom&gt; yeah, actually, snark has both of those, I just disabled them because i didn't want to maintain 'em :)
16:58 &lt;+legion&gt; hmm good point ragnarok
16:58 &lt;jrandom&gt; but getting them back in wouldn't be much trouble
16:59 &lt;+Ragnarok&gt; well, the torrent maker at least shouldn't be that bad
16:59 &lt;jrandom&gt; there's a Tracker.java too, and handling in the PeerAcceptor, but I threw out what wasn't necessary, so one would probably want to look back at http://klomp.org/snark/ for those
17:00 &lt;jrandom&gt; (and review http://dev.i2p/~jrandom/snark_diff.txt for changes)
17:00 &lt;+fox&gt; &lt;Romster&gt; since snarik is back it'll get worked on right :)
17:00 &lt;+legion&gt; actually when it comes to a tracker, it'd be better to come up with a distributed solution
17:00 &lt;+fox&gt; &lt;Romster&gt; snark*
17:00 &lt;jrandom&gt; porting code is easier than building a new distributed tracker legion ;)
17:00 &lt;+fox&gt; &lt;Romster&gt; legion, your your talking
17:00 &lt;+legion&gt; true, that
17:01 &lt;jrandom&gt; but I wouldn't be opposed to integrating a nice clean maintained anonymity-friendly distributed tracker solution :)
17:01 &lt;+fox&gt; &lt;Romster&gt; could be tacked onto the eepsites?
17:01  * jrandom spots a flying pony go past the window
17:01 &lt;+Ragnarok&gt; the official bt client has a kademlia based distributed tracker, but obviously that's only good as a design reference
17:01 &lt;+legion&gt; a place to start ;)
17:02 &lt;+fox&gt; &lt;Romster&gt; actually kademlia = emules KAD netowrk? hmm, if that's the case KAD would be ideal for a tracker but bootstraping is an issue
17:03 &lt;+Ragnarok&gt; they're based on the same algorithm, but they're not in any way compatable
17:03 &lt;+Ragnarok&gt; compatible, even
17:04 &lt;+Ragnarok&gt; doing something like emule's KAD for i2phex would be sort of interesting...
17:04 &lt;+Ragnarok&gt; anyway, flying ponies
17:04 &lt;jrandom&gt; :)
17:04 &lt;jrandom&gt; (agreed on both counts)
17:04 &lt;jrandom&gt; ok, anything else on 4) i2psnark?
17:05 &lt;+Ragnarok&gt; as long as we have something to make .torrent files, the existing trackers are fine
17:05 &lt;jrandom&gt; thats a good point - there's some commented out code in Snark's main I believe
17:05 &lt;+legion&gt; no I think the existing trackers are not fine :(
17:05 &lt;jrandom&gt; whats wrong with them legion?
17:05 &lt;cat-a-puss&gt; don't just hand uesrs a torrent file ether
17:05 &lt;+legion&gt; often have trouble accessing them
17:06 &lt;jrandom&gt; hmm cat-a-puss?  oh, you mean, we need to get a web interface to transparently swarm?
17:06 &lt;+legion&gt; sites get flooded with traffic
17:06 &lt;jrandom&gt; ah, thats i2p's issue, hopefully 0.6.1.4 will improve that
17:06 &lt;jrandom&gt; postman was telling me how he was getting tons of hits @ tracker.postman.i2p
17:06 &lt;jrandom&gt; i forget the #s offhand
17:06 &lt;cat-a-puss&gt; If we are handling both the swarming code and the code to get the torrent in the first place, might as well make it transparent for the user
17:07 &lt;jrandom&gt; orion.i2p/bt/ isn't really used though
17:07 &lt;jrandom&gt; (and tracker-fr seems lively)
17:07 &lt;+susi23&gt; with susibt I hope to include trackers rss feed, so you don't need to go on the trackers webpage anymore but get the torrents downloaded automatically :)
17:07 &lt;cat-a-puss&gt; also prevents confusing an i2p torrent with a non-anonymous one
17:07 &lt;+fox&gt; &lt;jme___&gt; http tracker for bt doesnt scale due to poorely designed protocol
17:07 &lt;+fox&gt; &lt;Romster&gt; router watchdog router hung hard restart wtf
17:07 &lt;+legion&gt; right, which is my point some trackers are flooded while others are idle
17:07 &lt;jrandom&gt; cat-a-puss: ah, yeah I'd love to integrate hooks from syndie into susibt :)
17:07 &lt;+fox&gt; &lt;jme___&gt; it can be easily fixed but break the compatibility with official bt protocol
17:08 &lt;+fox&gt; &lt;jme___&gt; it is the road followed by the dht tracker stuff
17:08 &lt;jrandom&gt; (and the other way around, so people can easily syndicate .torrent files, etc)
17:08 &lt;+Complication&gt; Romster: I get those, but the machine I get them on is borderline (300 MHz)
17:08 &lt;+fox&gt; &lt;Romster&gt; the distributed tracker is the solution to hammered trackers
17:08 &lt;jrandom&gt; legion: that can easily be remedied by people using different trackers :)
17:08 &lt;+fox&gt; &lt;Romster&gt; azerius DHT
17:08 &lt;jrandom&gt; code is expensive, using different URLs is cheap
17:08 &lt;+legion&gt; yeah, but they don't seem to be doing that do they?
17:09 &lt;jrandom&gt; but, yes, a distributed tracker would be great.  not on my roadmap though, but if someone gets it going, that would Rule.
17:09 &lt;+Complication&gt; In due time... surely someone can go distributed too.
17:09 &lt;+legion&gt; Instead of of posting torrents to tracker sites, they could post a bith and whatever details to their eepsite.
17:10 &lt;jrandom&gt; bith == hash?
17:10 &lt;+legion&gt; yeah, stands for bittorrent hash, not my term
17:10 &lt;+Complication&gt; In the beginning, though... a simple and solid client, in Java, bundled with the router... can solve many problems. (Perhaps even pull signed updates without overloading dev.i2p.)
17:11 &lt;+legion&gt; yeah, that would be great
17:11 &lt;jrandom&gt; aye Complication 
17:11 &lt;+fox&gt; &lt;Romster&gt; yeah torrent updates
17:11 &lt;+fox&gt; &lt;Romster&gt; ok next item ont he list :)
17:12 &lt;jrandom&gt; ok, 5) more on bootstrapping
17:12 &lt;+legion&gt; yeah lets move on
17:12 &lt;jrandom&gt; lots of interesting stuff on the list as of late, and no way am i going to summarize it all here :)
17:12 &lt;+fox&gt; &lt;Romster&gt; bootstraping the i2p router database?
17:12 &lt;jrandom&gt; anyone have any questions/comments/concerns they want to discuss about the thread?
17:12 &lt;jrandom&gt; Romster: see the list and/or email
17:12 &lt;+fox&gt; * Romster needs to read that list
17:13 &lt;jrandom&gt; aye, there's good stuff on there :)
17:13 &lt;+fox&gt; &lt;Romster&gt; i've been rather busy laterly
17:13 &lt;+Complication&gt; 26 messages to read through, can't comment yet
17:13 &lt;jrandom&gt; still no end result, but we're looking towards a new way of building tunnels for 0.6.2
17:14 &lt;+fox&gt; &lt;Romster&gt; a new way, is there a flay in the current method?
17:14 &lt;+fox&gt; &lt;Romster&gt; flaw*
17:14 &lt;jrandom&gt; Michael's analysis shows the attack is not really a problem now, as there are easier attacks on the alternatives
17:14 &lt;jrandom&gt; read the list ;)
17:14 &lt;+fox&gt; &lt;Romster&gt; arg later
17:14 &lt;+fox&gt; &lt;Romster&gt; this is now :)
17:15 &lt;+fox&gt; &lt;Romster&gt; i'm noramlly asleep at this time.
17:15 &lt;+fox&gt; &lt;Romster&gt; so i rearly get to be at a meeting
17:16 &lt;cat-a-puss&gt; can you post your ideas for a new way / existing / rejected ways in an email to the list so we can compare
17:16 &lt;+fox&gt; &lt;Romster&gt; so its todo with attack methods and tunnel creation i assume, without reading the list yet
17:16 &lt;cat-a-puss&gt; (that's for Jrandom)
17:16 &lt;jrandom&gt; cat-a-puss: i'm not sure if we've really hashed out an end result yet
17:16 &lt;+fox&gt; &lt;Romster&gt; be an idea cat-a-puss
17:17 &lt;+Complication&gt; Romster: yes, it was more-or-less about giving the endpoint of an exploratory tunnel less influence as a possible attacker
17:17 &lt;jrandom&gt; but http://dev.i2p.net/pipermail/i2p/2005-October/001073.html is the latest for what I see coming out of your suggestion
17:17 &lt;jrandom&gt; well, not influence - i2p is a free route mixnet - but less information
17:18 &lt;+Complication&gt; Yes, that would likely be a more correct term
17:18 &lt;jrandom&gt; (the above linked url is full of arm waving, no solid crypto figured out yet)
17:18 &lt;+fox&gt; &lt;Romster&gt; lesss = better for more robustness agenst attacks, i get what your geting at
17:18 &lt;jrandom&gt; ((but i think its all doable with existing techniques)
17:19 &lt;jrandom&gt; Romster: here's a plot of Michael's attack against the existing algorithm, with the X axist saying what % of the network is compromised - http://dev.i2p.net/~jrandom/fraction-of-attackers.png
17:20 &lt;jrandom&gt; (plain telescopic building would be off the chart before hitting x=200)
17:20 &lt;jrandom&gt; ((so what we have now is literally orders of magnitude better))
17:20 &lt;jrandom&gt; but we can improve upon that further
17:21 &lt;jrandom&gt; though there's also the garlic routing alternative too
17:21 &lt;jrandom&gt; anyway, yeah, more things to be hashed out, keep an eye on the list :)
17:21 &lt;+fox&gt; &lt;Romster&gt; ok i'll have a good read of that list later
17:22 &lt;+fox&gt; &lt;Romster&gt; and see if i can think of anything too add
17:22 &lt;jrandom&gt; cool
17:22 &lt;cat-a-puss&gt; would the "new" telescopic method be fast enough to do on demand construction?
17:22 &lt;jrandom&gt; I'm not sure we want that
17:22 &lt;jrandom&gt; its the O(1) vs O(N) issue
17:23 &lt;jrandom&gt; the new technique would allow tunnel creation without using the exploratory tunnels, leavng the exploratory tunnels for netDb operation 
17:23 &lt;jrandom&gt; (and for exploratory tunnel creation :)
17:24 &lt;+fox&gt; &lt;Romster&gt; hrmm would it be worthwhile screwing with the hackers by givving them heaps of false positives thereby masking the real source
17:24 &lt;+legion&gt; sounds good :)
17:24 &lt;+legion&gt; I'd think some screwing like that would be good
17:24 &lt;cat-a-puss&gt; jrandom: right, I was asking if doing do would speed things up enough, so that sometimes that last hops don't know they are the last hop, as disguesed on list.
17:25 &lt;+fox&gt; &lt;Romster&gt; exploratory tunnels to collect netDB router refereances?
17:25 &lt;jrandom&gt; romster: we are the hackers ;)  but yeah, if the false positives overwhelmed the true positives, it'd require substantially large number of attacks to get statistically significant data
17:26 &lt;jrandom&gt; hmm right cat-a-puss, but I'm not sure how that'd speed things up though, it'd move us from an O(1) to O(N) tunnel topology
17:26 &lt;jrandom&gt; or what do you mean by speed things up?
17:26 &lt;+fox&gt; &lt;Romster&gt; and if it got to the point of being detected it could then drop off and go silent forawhile?
17:26 &lt;jrandom&gt; using the new technique would reduce the failed tunnel creations, certainly
17:26 &lt;+fox&gt; &lt;Romster&gt; or mistearly change it's key and continue or something heh
17:26 &lt;jrandom&gt; romster: it'd probably be worth digging through the mails to review the attack ;)
17:27 &lt;+fox&gt; &lt;Romster&gt; yeah after sleep
17:27 &lt;+Complication&gt; Romster: afaik, it's a passive attack mostly, so the target can't detect it occurring
17:27 &lt;+fox&gt; &lt;Romster&gt; and fixing a friends pc i got sitting here
17:27 &lt;+fox&gt; &lt;Romster&gt; ah ic complication.
17:27 &lt;cat-a-puss&gt; jrandom: I'm not talking about the O(n) thing. I mean just waiting to construct a client tunnel until we need one for some apps, rather than just having them sit there all the time. 
17:28 &lt;+Complication&gt; (but I might be wrong, and those last 26 messages might have active components)
17:28 &lt;+fox&gt; &lt;Romster&gt; would a long term passive attack evently find the target?
17:28 &lt;+fox&gt; &lt;Romster&gt; i'll comment after i've read the list
17:28 &lt;jrandom&gt; ah cat-a-puss, we'll certainly improve the tunnel pooling for 0.6.2.  we currently only build the tunnel when we need it (giving ourselves a little time in case the creation fails)
17:28 &lt;+Complication&gt; Romster: well, persisting the attack beyond tunnel lifetime would require resources and patience
17:28 &lt;+fox&gt; &lt;Romster&gt; and understand it better
17:29 &lt;+Complication&gt; But time plays a part in every probability of success. You try long, you get more chances.
17:29 &lt;+fox&gt; &lt;Romster&gt; ah that's the idea tunnel life tiem be too short to actually have a worthwhile attack work.
17:29 &lt;jrandom&gt; each pool has a defined number of backup tunnels, and we by default build replacements between 60-120 seconds before an old one expires
17:29 &lt;+fox&gt; &lt;Romster&gt; time*
17:30 &lt;jrandom&gt; right Complication - each sample occurs only 'm' times every (c/n) tunnels
17:30 &lt;+fox&gt; &lt;Romster&gt; there is no interaction between each tunnel to gather stastics?
17:30 &lt;+fox&gt; &lt;Romster&gt; as one is about to die and another is being built
17:31 &lt;jrandom&gt; romster: the new tunnels do not talk to each other, no, but thats not the attack Michael has been describing
17:31 &lt;jrandom&gt; there are countless attacks out there, most of which we have dealt with, but whenever someone comes up with one that may have a bearing on I2P's operation, we want to analyze it further
17:31 &lt;+fox&gt; &lt;Romster&gt; must read the list, ok i'll leave it at that for now, anyone else got anything to say?
17:32 &lt;jrandom&gt; ok, if there's nothing else, lets move on to 6) virus investigations
17:32 &lt;+fox&gt; &lt;Romster&gt; actually one stastic i can see could be gathered is no 0 hop would mean that the next hop is not the end point so it could be ruled otu but with millions of nodes that analying technique would be useless
17:33 &lt;jrandom&gt; I don't have anything to add beyond whats been discussed on the forum
17:33 &lt;jrandom&gt; right Romster, there are predecessor attacks on tunnel length, which is one of the main things we're addressing in 0.6.2
17:33 &lt;+fox&gt; &lt;Romster&gt; virus, what virus, if it's linux it'll be nonexistant, but windows hmmm
17:34 &lt;+Complication&gt; Well, although I couldn't build a matching binary (hell knows hy) the final difference was small enough... to hopefully be useful to anyone interested in reading assembly code.
17:34 &lt;jrandom&gt; Romster: please, the weekly status notes should explain these agenda items, and the meeting is to discuss things /beyond/ whats in the notes ;)
17:35 &lt;+Complication&gt; I sure couldn't find anything obvious in there, but nor could I explain away all the difference.
17:35 &lt;@cervantes&gt; rtfml and rtff
17:35 &lt;+fox&gt; &lt;Romster&gt; yeah i haven't been upto speed for quite awhile, sorry about taht jrandom
17:35 &lt;@cervantes&gt; ;-)
17:35 &lt;jrandom&gt; aye, the fact that both a known safe bat file and the old one triggered the same detection code is substantial
17:35 &lt;+Complication&gt; Yes, that sort of eases doubts.
17:36 &lt;+Complication&gt; I guess the QBFC might have undocumented differences within the same version number (different builds?)
17:37  * jrandom has no idea, but its possibly just some OS interaction, or whatever.  I don't know, you've put up enough analysis for people to make their own informed decision
17:37 &lt;+Complication&gt; I think it's better that way.
17:37 &lt;+Complication&gt; Disassembly is really notably outside my usual playground.
17:37 &lt;jrandom&gt; legion: is there anything you want to mention about this, or should people just go through the forum if they want more info?
17:38 &lt;@cervantes&gt; can I just re-iterate what others have said on the forum, and thank Complication for the time and maticulous attempts he's put in to checking this issue out
17:38 &lt;jrandom&gt; aye, its much appreciated
17:38 &lt;+legion&gt; I've nothing to add, I feel that I've said way too much about it already
17:39 &lt;jrandom&gt; 'k understood.  ok, anyone else have anything to bring up on this, or shall we move on to 7) ???
17:39 &lt;jrandom&gt; [consider us moved]
17:40 &lt;+fox&gt; * Romster seconds that :)
17:40 &lt;+legion&gt; ok for 7)??? how about we take a moment to discuss i2phex
17:40 &lt;jrandom&gt; cool, good idea
17:40 &lt;+fox&gt; &lt;Romster&gt; since i'm using it right now even :)
17:40 &lt;@cervantes&gt; no no group hug first
17:40 &lt;jrandom&gt; redzara mentioned he was going to be at the meeting, but progress on the merge is going slow
17:41 &lt;+legion&gt; susi23 inquired about a headless version
17:41 &lt;jrandom&gt; ah cool, i saw your post on that
17:41 &lt;+fox&gt; &lt;Romster&gt; might i add the favourites list needs to be wider to cope with the longer i2p keys
17:42 &lt;+susi23&gt; (that's no must, I was just curious about it)
17:42 &lt;jrandom&gt; well, no one can remember base64 keys, so I'm not sure if you're missing much Romster ;)
17:42 &lt;jrandom&gt; (and the first few bytes should be enough to uniquely identify them)
17:42 &lt;+fox&gt; &lt;Romster&gt; starting i2phex with a server is the major problem i see so far
17:42 &lt;+legion&gt; Actually I'd like to see only like the first 12 characters of keys to displayed in the client
17:42 &lt;+fox&gt; &lt;Romster&gt; heh guess
17:42  * Complication is regrettably majorly busy, and can't do no xml-rpc
17:43 &lt;jrandom&gt; seems reasonable legion 
17:43 &lt;+fox&gt; &lt;Romster&gt; what about display as many characters to make the key unique
17:43 &lt;jnymo_&gt; I'm having good results with i2phex
17:44 &lt;jrandom&gt; cool jnymo_, i've been hearing good things too
17:44 &lt;+fox&gt; &lt;Romster&gt; so if 2 keys start with abc it'll be abcx
17:44 &lt;jnymo_&gt; 12 identical characters isn't likely, romster
17:44 &lt;+fox&gt; &lt;Romster&gt; true
17:44 &lt;+Complication&gt; Besides, simpler = quicker
17:44 &lt;+fox&gt; &lt;Romster&gt; but wouldnt need 12 if the keys are that far randomised
17:45 &lt;+Complication&gt; (not that there is much speed to gain from displaying things)
17:45 &lt;+legion&gt; Well maybe there could be a new host properties window, stating the full key and certain information like how much it is sharing and whatever
17:45 &lt;+susi23&gt; (netdb works great with 4 chars only for router ids)
17:45 &lt;+fox&gt; &lt;Romster&gt; or the database and using the keyname=base64 and only displaying the keyname
17:45 &lt;jrandom&gt; hmm, i thought there was already a peer info display legion?
17:46 &lt;jrandom&gt; legion: some things like that would be good to add to the mainline phex, most likely?
17:46 &lt;+legion&gt; hmm could be right...
17:46 &lt;jrandom&gt; (that way Gregor can maintain it ;)
17:46 &lt;+Complication&gt; Well, there's a "Browse host" function, but that may not be the exact same thing. (If it works.)
17:46 &lt;jrandom&gt; Complication: it does
17:46 &lt;jrandom&gt; (work, that is)
17:47 &lt;+Complication&gt; Seems to basically drop the host destkey into the search box
17:47 &lt;+Complication&gt; ...and runs a search.
17:48 &lt;jnymo_&gt; this may be an i2phex mainline issue, but I didn't see an ETA on i2phex downloads
17:48 &lt;+Complication&gt; Hmm... or actually, doesn't run a search.
17:48 &lt;+Complication&gt; Mine seems to wait until I manually start it.
17:48 &lt;+fox&gt; &lt;Romster&gt; whats the nearby i2phex running tickbox for?
17:49 &lt;+legion&gt; I see where there is plenty of room for improvement. ;)
17:49 &lt;jrandom&gt; yep :)
17:50 &lt;jrandom&gt; lots to be done, and the forum is a good place to post up ideas/suggestions/questions(/patches :)
17:50 &lt;+fox&gt; &lt;Romster&gt; despite it's ovous name
17:50 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
17:50 &lt;+fox&gt; &lt;Romster&gt; hmm good point
17:50 &lt;+fox&gt; &lt;Romster&gt; can't think of anything else
17:51 &lt;+fox&gt; &lt;Romster&gt; but anyone working on a distributed data store?
17:51  * cervantes checks his watch
17:51 &lt;+fox&gt; &lt;Romster&gt; like activtely
17:51 &lt;jrandom&gt; Romster: beyond syndie, no
17:51 &lt;jrandom&gt; (not to my knowledge, at least)
17:52 &lt;+legion&gt; well I was wondering about integrating a http download manager into i2p, would make downloading larger content from eepsites easier.
17:52 &lt;+fox&gt; &lt;Romster&gt; q and iphex and one or 2 others but i've not seen anything mentained for awhile now
17:52 &lt;@cervantes&gt; what's the status of feedspace...I haven't heard aught of it in a while
17:52 &lt;jrandom&gt; legion: that would be cool - there's a post about that on the forum too i think
17:53 &lt;+fox&gt; &lt;Romster&gt; ah feedspace another one
17:53 &lt;jnymo_&gt; if this was mentioned in the meeting already, nm.. but, is there news on i2p freenet colab?
17:53 &lt;jrandom&gt; cervantes: last i heard frosk was kind of busy, but if frosk is around, maybe he can tell us more :)
17:53 &lt;+legion&gt; Personally I'd like to see a i2p entropy colab.
17:54 &lt;+fox&gt; &lt;Romster&gt; i have ideas for a datastore, but it be a expansion to existing methods that are in use currently
17:54 &lt;+legion&gt; Given that q, feedspace and such don't seem to be going anywhere fast right now
17:54 &lt;jrandom&gt; jnymo_: I've bounced the freenet folks some code to run on our SSU transport,toad has been joining in on some of the discussions, but freenet won't be in a position for us to run it as a data store on top of i2p for a while (after their 0.7 release comes out, most likely)
17:54 &lt;+fox&gt; &lt;Romster&gt; i want to start a project but not go over what others have done already
17:54 &lt;+legion&gt; wonder if it'd be possible to port entropy to run over i2p...
17:54 &lt;jrandom&gt; legion: entropy would be good, but integration is kind of hard.  of course, people could run things like fproxy.i2p for entropy
17:55  * jrandom doesnt know entropy's transport code at all
17:55 &lt;+fox&gt; &lt;Romster&gt; i've put my irc client on hold, there is alot of them in progress already all i2p needs now is a datastore and it'll beat freenet with ease :)
17:55 &lt;jrandom&gt; (but perhaps that'd be a good way to get someone to hack on the GCJ SDK :)
17:56 &lt;jrandom&gt; Romster: helping out on other efforts is a lot more rewarding that starting brand new projects, as you get a lot more done with less effort :)
17:56 &lt;jnymo_&gt; ah.. congrats on the gcj port
17:56 &lt;+fox&gt; &lt;Romster&gt; entropy's is in c or C++ iirc
17:57 &lt;jrandom&gt; right Romster, which is why they'd be able to use I2P's SDK and streaming lib, built with GCJ into native libraries
17:57 &lt;+fox&gt; &lt;Romster&gt; jrandom true, but who :)
17:57 &lt;jrandom&gt; not I
17:57 &lt;+legion&gt; oh and on another issue, just like to mention that today I released a new version of my readme.html update for the i2p router console.
17:57 &lt;jrandom&gt; (the only way to get something you care about done is for *you* to do it :)
17:57 &lt;jrandom&gt; cool
17:57  * dust would like to see some kind of 'squid' syndication for offloading eepsites
17:58 &lt;jrandom&gt; dust: yeah totally, if we can get sucker into that position, that'd be ideal
17:58 &lt;jrandom&gt; e.g. I'd love to get the latest info from orion in syndie, local
17:58 &lt;+fox&gt; &lt;Romster&gt; build a proxy for squid to use :)
17:59 &lt;+legion&gt; I'd been putting it of in the hope that certain improvements to the python eepsitechecker would have been made by now.
17:59 &lt;dust&gt; ah, syndie
17:59 &lt;jrandom&gt; (thats actually what syndie is for - syndication to cut down on load)
17:59 &lt;dust&gt; _the_ answer
17:59 &lt;jrandom&gt; there's a python eepsite checker?
17:59 &lt;+fox&gt; &lt;Romster&gt; first i've heard about it
17:59 &lt;+legion&gt; yeah, it's what I use ;)
18:00 &lt;jrandom&gt; cool legion 
18:00 &lt;+legion&gt; really? It's been around for awhile
18:00 &lt;+fox&gt; &lt;Romster&gt; nice i'd like to check that out :)
18:00 &lt;@cervantes&gt; think someone ported baffled's script... can't remember who/when
18:00 &lt;+fox&gt; &lt;Romster&gt; i'm learning python
18:00 &lt;jrandom&gt; ah ok cervantes 
18:00 &lt;+fox&gt; &lt;Romster&gt; the hard way by examples and the manual :)
18:00 &lt;jrandom&gt; yeah, i'm lazy, i just use polecat.i2p/i2psurvey/ and orion.i2p/ :)
18:01 &lt;jrandom&gt; (no need for me to spider)
18:01 &lt;+legion&gt; if someone would care to work with me on it, I'd really like to get the code fixed and working with either python 2.3 or 2.4
18:01 &lt;+fox&gt; &lt;Romster&gt; i have 2.4 installed here
18:01 &lt;+Ragnarok&gt; I may have a look at it.  Got link?
18:01 &lt;+fox&gt; &lt;Romster&gt; actually think it's 2.4.1
18:02 &lt;+legion&gt; right now it has no py2exe compatibility and half of it works with each version, which means anyone running it needs to have both installed.
18:02  * jnymo_ would love to see an orion.i2p/I2PDirectory hybrid.. info, catagories, stats.. butter
18:02 &lt;+legion&gt; I'll archive it after the meeting and post a link to the forums
18:03 &lt;+Ragnarok&gt; ok
18:03 &lt;jrandom&gt; legion: hmm, do you see lots of people needing to run that though?  I mean, only a few people need to spider
18:03 &lt;+fox&gt; &lt;Romster&gt; both eck, might be a bit much for me to translate to the newer dunno untill i look at the code
18:03 &lt;jrandom&gt; (not that there's anything wrong with making it easy for those few people, that is :)
18:04 &lt;+fox&gt; &lt;Romster&gt; cold be disected and used todo other things too?
18:04 &lt;+legion&gt; Well thing is I can see where there could be some uses for everyone that runs i2p.
18:04 &lt;+fox&gt; &lt;Romster&gt; could*
18:04 &lt;jrandom&gt; hmm, I'm not so sure, could you explain how?
18:04 &lt;jrandom&gt; I mean, I don't want everyone to essentially DDoS every eepsite
18:05 &lt;+legion&gt; One of which would be a dynamic bookmarks page, that is auto generated every 12-24 hours or so.
18:05 &lt;jrandom&gt; ah, that is trivial in syndie (actually one of the main features - 'new blogs')
18:05 &lt;jrandom&gt; ((but of course, syndie doesn't have a great ui for that yet))
18:06 &lt;+fox&gt; &lt;Romster&gt; actually would only need a few to spider and throw it into a torrent/dht like database and sync that between nodes
18:06 &lt;jrandom&gt; right Romster (though that torrent/dht-like database to sync, or "syndi"cate, could be syndie ;)
18:06 &lt;+fox&gt; &lt;Romster&gt; could even be a hidden way to learn more i2p nodes and services
18:07 &lt;+fox&gt; &lt;Romster&gt; yeah or syndie
18:07 &lt;jrandom&gt; ok, anyone else have anything for the meeting?  the curry is getting cold ;)
18:08 &lt;+fox&gt; &lt;Romster&gt; if syndie is going tobe that great one could store static pages to cashe and the same with images
18:08 &lt;+fox&gt; &lt;reliver&gt; bon appetit, jrandom :-)
18:08 &lt;jrandom&gt; exactly romster, you can do that now 
18:09 &lt;jrandom&gt; ok, if there's nothing else...
18:09  * jrandom winds up
18:09  * jrandom *baf*s the meeting closed
</div>
