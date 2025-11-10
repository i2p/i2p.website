---
title: "I2P Dev Meeting - September 20, 2005"
date: 2005-09-20
author: "jrandom"
description: "I2P development meeting log for September 20, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, Complication, forest, jrandom, Kefoo, postman, Ragnarok</p>

## Meeting Log

<div class="irc-log">
16:18 &lt;jrandom&gt; 0) hi
16:18 &lt;jrandom&gt; 1) 0.6.0.6
16:18 &lt;jrandom&gt; 2) I2Phex 0.1.1.27
16:18 &lt;jrandom&gt; 3) migration
16:18 &lt;jrandom&gt; 4) ???
16:18 &lt;jrandom&gt; 0) hi
16:18  * jrandom waves
16:18 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2005-September/000929.html
16:18 &lt;+postman&gt; hello
16:18 &lt;forest&gt; hi
16:18 &lt;jrandom&gt; lets jump on in to 1) 0.6.0.6
16:19 &lt;jrandom&gt; the status notes cover pretty much what i've got on my mind for 0.6.0.6.  anyone have any questions/concerns/comments to bring up?
16:19 &lt;+postman&gt; jrandom: observation:
16:19 &lt;+postman&gt; jrandom: much higher bandwidth consumption
16:20 &lt;+postman&gt; jrandom: all within the limits and running fine - but my routers really getting warm now
16:20  * nickless_head makes similar observation
16:20 &lt;jrandom&gt; aye, me too, i think its likely due to an increase in bt and i2phex traffic
16:20 &lt;+postman&gt; what increase, with just 80 active torrents on the tracker? :)
16:20 &lt;jrandom&gt; heh
16:21 &lt;+postman&gt; but its good to see, that the network does not crumble
16:21 &lt;+postman&gt; irc is pretty stable altho the router does 50k/s atm
16:21 &lt;jrandom&gt; mos' def'.  i'm not even logged into freenode anymore, as irc here is stable enough
16:22  * postman hands the mike back
16:22 &lt;jrandom&gt; cool, thanks.  i think there's definitely still room to go for bandwidth efficiency, but it seems reasonable atm
16:22 &lt;jrandom&gt; (hopefully the thing i'm working on will help, but more on that when its ready)
16:22 &lt;fox&gt; &lt;mihi&gt; you should definitely distinguish between OK (Nat) and Err (Nat)...
16:23 &lt;fox&gt; &lt;mihi&gt; or is your hole punching almighty?
16:23 &lt;jrandom&gt; heh
16:23 &lt;jrandom&gt; well, ERR-SymmetricNAT is and will continue to be an ERR
16:23 &lt;fox&gt; &lt;mihi&gt; or is it impossible to check whether it was successful?
16:24 &lt;fox&gt; &lt;mihi&gt; ok
16:24 &lt;jrandom&gt; but ERR-Reject is due to restricted cone, while full cone nats work fine
16:24 &lt;jrandom&gt; (since i2p uses only one source port for everyone, as long as you're on i2p you'll have a hole punched for the full cone)
16:25 &lt;jrandom&gt; still, it is better when people forward their ports so they don't need introducers, as that lets them also become introducers themselves
16:25 &lt;fox&gt; &lt;mihi&gt; as long as there are no nasty iptables rules (like drop UDP to 8887 from IP addresses divisable by 7 :) )
16:25 &lt;jrandom&gt; heh
16:26 &lt;jrandom&gt; and unfortunately, some people do have b0rked configurations like that (*cough*peerguardian*cough*)
16:26 &lt;jrandom&gt; someone the other day was wondering why i2p didn't work, even though they had their firewall dropping packets from all .edu peers
16:27 &lt;+Ragnarok&gt; .edu?  That's pretty random
16:27 &lt;jrandom&gt; yeah, made no sense to me, in so many ways
16:27 &lt;jrandom&gt; but, c'est la vie
16:27  * nickless_head sings: We don't need no education...
16:28 &lt;jrandom&gt; heh
16:28 &lt;jrandom&gt; ok, anyone else have anything on 1) 0.6.0.6?
16:29 &lt;jrandom&gt; if not, moving on to 2) i2phex 0.1.1.27
16:29 &lt;jrandom&gt; not much to say here beyond whats in the mail either...
16:30 &lt;+postman&gt; jrandom: there was no positive response in the mentioned forums either :(
16:31 &lt;+postman&gt; jrandom: i will forward your statusnotes and links - maybe the readers get the point
16:31 &lt;jrandom&gt; postman: people are of course able to use whatever they want, but I don't recommend the binary release from legion as the source doesn't match the binary, and the launcher is entirely closed source
16:32 &lt;jrandom&gt; now that we've got i2phex on a web accessible location, built from cvs, hopefully that will reduce people's reliance on that
16:33 &lt;jrandom&gt; (perhaps if you want to post the irc log from #i2p-chat an hour or two ago between legion and i, that might help explain the situation to people more completely)
16:34 &lt;jrandom&gt; ok, anyone else have anyhing on 2) i2phex, or shall we move on to 3) migration
16:34  * postman has a look
16:34 &lt;jrandom&gt; there's not much really to add for 3), its more of an fyi
16:34 &lt;jrandom&gt; so, perhaps we can jump quickly to 4) ???
16:34 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
16:35 &lt;+Complication&gt; Migration?
16:36 &lt;jrandom&gt; if you didn't notice, great :)
16:36 &lt;jrandom&gt; we moved from one colo to another
16:36 &lt;jrandom&gt; (cvs.i2p.net, dev.i2p.net, www.i2p.net, mail.i2p.net)
16:36 &lt;+Complication&gt; Oh, that migration. :)
16:36  * Complication is simply a bit slow today
16:39 &lt;+Complication&gt; By the way, 0.6.0.6 seems very nice... in the regard that my router didn't touch 0 participating tunnels in 54 hours.
16:39 &lt;+Complication&gt; Not even once.
16:39 &lt;jrandom&gt; nice
16:40 &lt;jrandom&gt; ok, if there's nothing else people want to bring up for the meeting...
16:40  * jrandom winds up
16:40 &lt;+postman&gt; jrandom: one thing
16:40  * jrandom stops winding
16:40 &lt;+postman&gt; jrandom: you just incremented the i2phex version - what if sirup plans another release?
16:40 &lt;jrandom&gt; postman: sirup uses the cvs
16:41 &lt;+postman&gt; jrandom: how about giving it a an additional tag
16:41 &lt;+postman&gt; ok, that's fine then
16:41 &lt;+postman&gt; :)
16:41  * postman is back in his cave
16:41 &lt;jrandom&gt; (developing code outside a source control system == crazy)
16:41  * Kefoo remembers how crazy it was developing inside a source control system, too
16:41 &lt;+postman&gt; jrandom: (it did not need to be YOUR's)
16:42 &lt;jrandom&gt; heh true enough Kefoo ;)
16:42 &lt;jrandom&gt; heh well, yeah... his just happens to be though ;)
16:43  * bar just set a new personal record of 156 concurrent udp connections (old record was 152)
16:43 &lt;jrandom&gt; cool, yeah, i saw 173 earlier today
16:44 &lt;+bar&gt; oh :) yeah the indtroducing is doing its thing fo' sure
16:44 &lt;Kefoo&gt; Not to backtrack, but is i2phex supossed to try connecting on startup? I've heard both yes and no.
16:44 &lt;+bar&gt; -d
16:44 &lt;jrandom&gt; wikked bar
16:44 &lt;jrandom&gt; Kefoo: afaik, no.
16:44 &lt;jrandom&gt; but, i'm no phex dev
16:45 &lt;Kefoo&gt; The only way I've found is to copy and paste the host keys into the program and connect to them manually
16:45 &lt;jrandom&gt; thats what i've done Kefoo
16:45 &lt;+postman&gt; wind ye up now, jrandom :)
16:45 &lt;Kefoo&gt; Ok, so I'm not making it harder than it should be
16:45 &lt;Kefoo&gt; I do that sometimes
16:46 &lt;jrandom&gt; Kefoo: if there's something easier, i'd like to hear about it :)
16:46 &lt;jrandom&gt; ok ok postman, you can go get your beer ;)
16:46  * jrandom winds up
16:46  * jrandom *baf*s the meeting closed
</div>
