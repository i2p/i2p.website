---
title: "I2P Dev Meeting - February 01, 2005"
date: 2005-02-01
author: "jrandom"
description: "I2P development meeting log for February 01, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, cervantes, DrWoo, jrandom, MANCOM, polecat, postman, protokol, smeghead</p>

## Meeting Log

<div class="irc-log">
13:06 &lt;jrandom&gt; 0) hi
13:06 &lt;jrandom&gt; 1) 0.5 status
13:06 &lt;jrandom&gt; 2) nntp
13:06 &lt;jrandom&gt; 3) tech proposals
13:06 &lt;jrandom&gt; 4) ???
13:06 &lt;jrandom&gt; 0) hi
13:06  * jrandom waves
13:06 &lt;+postman&gt; hi jr
13:07  * postman waves
13:07 &lt;jrandom&gt; w3wt there is life out there :)
13:07 &lt;jrandom&gt; weekly status notes posted up @ http://i2p.net/pipermail/i2p/2005-February/000561.html
13:07 &lt;ant&gt; * dm waves
13:08 &lt;jrandom&gt; while y'all read that email, we can jump into 1) 0.5 status
13:08 &lt;MANCOM&gt; hi
13:09 &lt;jrandom&gt; lots of progress over the last week, all the new crypto is in and tested, and now all of the router's tunnel operation is done through the new tunnel pools
13:10 &lt;jrandom&gt; there are still some parts of the router i chopped out while doing the update, such as the tie in to request leases from clients or periodically test the tunnels, but those shouldn't be too difficult
13:11 &lt;jrandom&gt; the code is not compatible with the live net, and is on a separate branch in cvs, so people can still pull cvs HEAD and work with the latest 
13:12 &lt;+polecat&gt; Dook I finally looked at that page, and I still don't understand how we can avoid mixmaster style redundancy to protect from tunnel detection attacks.
13:12 &lt;+protokol&gt; yey
13:12 &lt;+polecat&gt; I imagine it works very well though.  :)
13:12 &lt;+protokol&gt; are you throwing in any other cool compatibility-breaking stuff?
13:13 &lt;+protokol&gt; the tunnel pool has to do with treads, right?
13:13 &lt;jrandom&gt; polecat: we don't verify at every hop, but we have a fixed message size to prevent useful tagging (and everything is encrypted at each hop)
13:14 &lt;jrandom&gt; protokol: i'm considering http://www.i2p/todo#sessionTag
13:14 &lt;+polecat&gt; So how to prevent multiple hops passing around bogus messages, and causing a DoS?
13:15 &lt;jrandom&gt; but no, the pools aren't the threading issue, the pools just let us safely manage the tunnels so that we don't get those "Lease expired" messages and can configure the length on a per-client basis
13:15 &lt;jrandom&gt; polecat: they'll fail at the endpoint, and the creator will detect the failure and move off it
13:16 &lt;+protokol&gt; jrandom: aside from any difficulty, i think any anon-improving features should go in ASAP
13:16 &lt;+polecat&gt; w00t!  Synchronized PRNG!  First application I've ever seen of that idea!
13:17 &lt;ant&gt; &lt;dm&gt; what does PRNG stand for?
13:17 &lt;ant&gt; &lt;dm&gt; if I may ask :)
13:18 &lt;jrandom&gt; protokol: agreed, thats what 0.5 is for :)  there aren't any other i2p-layer low hanging fruit, but there's always improvements that can be made at the app and lib layers (e.g. i2ptunnel filtering, etc)
13:18 &lt;jrandom&gt; dm: PseudoRandom Number Generator
13:18 &lt;ant&gt; &lt;dm&gt; cool, thanks
13:20 &lt;+protokol&gt; so youre saying that after this, its mostly speed and reliability tweaking?
13:21 &lt;+protokol&gt; and why has IRC been sucking lately
13:21 &lt;jrandom&gt; protokol: prior to 2.0 for the core and router, yes
13:21 &lt;+protokol&gt; i cant seem to connect to ducks server
13:21 &lt;+protokol&gt; yey
13:21  * jrandom doesnt know, we've seen perhaps 5 bulk disconnects in the last day or so, perhaps something on the server side
13:22 &lt;jrandom&gt; there's lots to be tweaked though, especially in the streaming lib after 0.5 is deployed
13:23 &lt;+polecat&gt; That whole UDP thing.
13:24 &lt;jrandom&gt; ah, the streaming lib shouldn't need changes for the 0.6 release, beyond the ones we do for the 0.5 rev
13:25 &lt;jrandom&gt; ok, thats all i have to bring up wrt 0.5 status - anyone have anything else on it?
13:27 &lt;jrandom&gt; if not, moving on to 2) nntp
13:27 &lt;jrandom&gt; nntp.fr.i2p is up, check it out :)
13:28 &lt;jrandom&gt; it doesnt seem like LonelyGuy is around, but he can be reached at http://fr.i2p/.  there are also configuration instructions for slrn on my blog, and jdot found that thunderbird can be fairly safe (though i dont know what config jdot used)
13:30 &lt;smeghead&gt; LonelyGuy? :)
13:30 &lt;cervantes&gt; did someone also test Pan?
13:30 &lt;jrandom&gt; hes been on here occationally
13:30 &lt;+polecat&gt; I wouldn't waste too much time on nntp, but as long as it has user managed access control it's fine.
13:30 &lt;jrandom&gt; (lonelyguy, not pan ;)
13:30 &lt;smeghead&gt; i thought his name was LazyGuy
13:31 &lt;jrandom&gt; is it LazyGuy?
13:31 &lt;jrandom&gt; i know we've had both...
13:31 &lt;jrandom&gt; you're right, lazyguy
13:31  * jrandom !stabs self
13:31 &lt;jrandom&gt; cervantes: i think LazyGuy tried it out, i dont know the config or result though
13:32 &lt;cervantes&gt; I thought it was LimeyGuy?
13:33  * jrandom awaits SnarkeyGuy's comments
13:33 &lt;smeghead&gt; he's French
13:35 &lt;jrandom&gt; ok, i dont have anything more to add beyond that, so unless anyone has any questions, moving on to 3) tech proposals
13:35 &lt;cervantes&gt; smeghead: you're thinking of ParesseuxGuy
13:36 &lt;jrandom&gt; orion has put together some good descriptions and ideas for a few of the messier issues up at 1) 0.5 status
13:36 &lt;jrandom&gt; 2) nntp
13:36 &lt;jrandom&gt; 3) tech proposals
13:36 &lt;jrandom&gt; erg
13:36 &lt;jrandom&gt; damn ^C^V
13:36 &lt;jrandom&gt; up at http://ugha.i2p/I2pRfc that is
13:37 &lt;jrandom&gt; so next time you want to discuss how you've got a killer naming idea, go to http://ugha.i2p/I2pRfc/I2pRfc0001ResourceNameMetadata
13:39 &lt;jrandom&gt; i dont really have much more to add beyond that. its a wiki, get wikiing :)
13:39 &lt;+polecat&gt; Yay.
13:39 &lt;+postman&gt; jrandom: ohh, cool i think i need to add a few ...
13:40 &lt;jrandom&gt; cool postman, thought you would :)  there's a template up there for new ones
13:41 &lt;+postman&gt; jrandom: gimme a lil time (first things first) but i will contribute :)
13:41 &lt;jrandom&gt; w3rd
13:41 &lt;+polecat&gt; ResourceNameMetadata, forming it is relatively trivial.  The trick is figuring out how to /get/ it from other people.
13:42 &lt;jrandom&gt; polecat: as postman said, first things first.
13:42 &lt;+polecat&gt; But if I had a solution, I'd be wikiing now wouldn't I.  :)
13:42 &lt;jrandom&gt; heh
13:42 &lt;jrandom&gt; discussion of the tradeoffs of /how/ to distribute prior to deciding /what/ to distribute is premature
13:43 &lt;jrandom&gt; there's room for lots of 'em though, so anyone should feel free to post up ideas that aren't fully worked through yet even (though fully functional ones with implementations would be cool too ;)
13:44 &lt;jrandom&gt; ok, unless there's something else on that, perhaps we can swing on to good ol' 4) ???
13:44 &lt;jrandom&gt; anyone have anything else to bring up?
13:45 &lt;jrandom&gt; smeghead: is there anything people can do to help out work through the gcj issues, or is it stalled on their prng?
13:46 &lt;+polecat&gt; What to distribute is just a signed dict.  Simple as that.
13:46 &lt;+polecat&gt; Yeah probably a good idea.
13:46 &lt;+polecat&gt; I'm STILL working on the skeleton for my i2p bt client, though would very much appreciate advice at any stage.
13:46 &lt;smeghead&gt; i think i've found a solution
13:46 &lt;smeghead&gt; in gnu crypto, there's a fortuna impl. since last summer
13:46 &lt;jrandom&gt; nice polecat 
13:46 &lt;jrandom&gt; oh cool smeghead 
13:46 &lt;+polecat&gt; smeghead: Hee, the $150 is as good as yours.
13:47 &lt;smeghead&gt; i can whip up a gnu-crypto.jar that contains only the classes needed for Fortuna
13:47 &lt;+polecat&gt; My working notes so far are at http://polecat.i2p/bittorrent.plan.doc
13:47 &lt;smeghead&gt; if we shipped the whole gnu-crypto.jar it's about 500 KB, too big really
13:47 &lt;+polecat&gt; Don't let the .doc scare you, it's in text/plain.
13:48 &lt;+polecat&gt; Fortuna doesn't use SecureRandom to do random things?
13:48 &lt;jrandom&gt; yowza, yeah 500KB is a bit excessive, but glancing at http://www.gnu.org/software/gnu-crypto/, it looks like something we could integrate safely (as we'd only be linking to it, not modifying)
13:48 &lt;smeghead&gt; SecureRandom was never the problem
13:48 &lt;jrandom&gt; polecat: fortuna /feeds/ secureRandom :)
13:49 &lt;smeghead&gt; jrandom: it would be easy to make a custom .jar, probably around 50KB
13:49 &lt;smeghead&gt; (rough estimate mind you)
13:49 &lt;smeghead&gt; i could make an ant build to custom package it on demand even
13:50 &lt;jrandom&gt; smeghead: wanna dig 'er into i2p/apps/fortuna/ ?
13:50 &lt;smeghead&gt; will do
13:50 &lt;jrandom&gt; kickass!
13:51 &lt;smeghead&gt; after that, assuming gcj will finally be spitting out random numbers, there will probably be more testing of various i2p functionality
13:51 &lt;+polecat&gt; What's the license?
13:51 &lt;jrandom&gt; we can then work some voodo in net.i2p.util.RandomSource to either use SecureRandom or fortuna (if its found, etc)
13:51 &lt;smeghead&gt; lgpl
13:51 &lt;+polecat&gt; Cool.
13:51 &lt;smeghead&gt; true, SecureRandom would be unnecessary
13:52 &lt;jrandom&gt; yeah, there's still lots to do to get it gcjing, but its a great start
13:52 &lt;jrandom&gt; in the profiles i've done on the live net, reseeding the PRNG takes a good portion of the cpu load
13:52 &lt;smeghead&gt; if anyone is into writing tests
13:52 &lt;smeghead&gt; but i probably don't have to finish that sentence
13:52 &lt;jrandom&gt; hehe
13:53 &lt;smeghead&gt; i will ask the gnu crypto maintainer about this impl., because i googled for info on it and searched their mailing list archives and there's not a peep on it
13:54 &lt;smeghead&gt; and their cvs commit logs aren't too enlightening either
13:54 &lt;jrandom&gt; 'k good idea
13:54 &lt;smeghead&gt; i hope it works
13:54 &lt;smeghead&gt; it's in kaffe cvs btw
13:54 &lt;smeghead&gt; your version should have it even
13:55 &lt;jrandom&gt; hmm, ah, yeah from the gnu-crypto import
13:55 &lt;smeghead&gt; gnu.security.prng.Fortuna
13:55 &lt;jrandom&gt; the 'kaffe' provider still uses their old sha1prng iirc
13:55 &lt;jrandom&gt; cool
13:56 &lt;MANCOM&gt; what is the status of the .net sam stuff? should one start getting into it or are major changes to be expected?
13:56 &lt;smeghead&gt; MANCOM: it needs testing, i'll be writing some unit tests for it soon
13:56 &lt;smeghead&gt; this gcj thing has kinda put that on hold
13:57 &lt;smeghead&gt; MANCOM: i don't expect there'll be any changes to the API at all, so it should be safe to code against
13:58 &lt;smeghead&gt; changes behind the API are likely, but you as a client don't need to know that :)
13:59 &lt;MANCOM&gt; :)
13:59 &lt;jrandom&gt; there may be some later updates that are relevent if you build apps that do large bulk transfer
14:00 &lt;jrandom&gt; but if you're just transferring a 10s of KB at a time, it should be fine
14:00 &lt;smeghead&gt; ok if the Java client's API changes, then the sam-sharp's will too :)
14:01 &lt;MANCOM&gt; i can't argue against that
14:02 &lt;jrandom&gt; ok, does anyone have anytihng else to bring up for the meeting?
14:02  * cervantes lowers big ben into the channel
14:03 &lt;+DrWoo&gt; note: nice work jrandom
14:03 &lt;smeghead&gt; nice pun cervantes
14:03  * jrandom groans
14:04 &lt;MANCOM&gt; i read that you don't want to advertise i2p too much before v0.5, is that true?
14:04 &lt;jrandom&gt; MANCOM: before 0.6.  yes
14:04 &lt;jrandom&gt; MANCOM: 0.5 will improve anonymity and help users control their performance better.  0.6 will let thousands+ concurrent users operate safely
14:04 &lt;MANCOM&gt; ah. 0.6. ok.
14:05 &lt;jrandom&gt; gracias doc, lots of progress :)
14:05 &lt;+polecat&gt; Whee, here's looking forward to 0.6...
14:05 &lt;+DrWoo&gt; :)
14:06 &lt;jrandom&gt; agreed polecat, agreed :)
14:06  * jrandom winds up
14:06  * jrandom *baf*s the meeting closed
</div>
