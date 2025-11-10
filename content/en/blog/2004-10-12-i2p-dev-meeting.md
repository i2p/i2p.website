---
title: "I2P Dev Meeting - October 12, 2004"
date: 2004-10-12
author: "jrandom"
description: "I2P development meeting log for October 12, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> deer, Janonymous, jrandom, modulus</p>

## Meeting Log

<div class="irc-log">
14:04 &lt;jrandom&gt; 0) hi
14:04 &lt;jrandom&gt; 1) 0.4.1.2
14:04 &lt;jrandom&gt; 2) 0.4.1.3
14:05 &lt;jrandom&gt; 3) 0.4.2
14:05 &lt;jrandom&gt; 4) mail discussions
14:05 &lt;jrandom&gt; 5) ???
14:05 &lt;jrandom&gt; 0) hi
14:05  * jrandom waves
14:05 &lt;Janonymous&gt; hello
14:05 &lt;jrandom&gt; lots of #s in our agenda this week
14:05 &lt;jrandom&gt; weekly status notes up @ http://i2p.net/pipermail/i2p/2004-October/000466.html
14:05 &lt;jrandom&gt; (posted a min or three ago)
14:05 &lt;deer&gt; * cervantes has brought a pillow
14:06 &lt;jrandom&gt; oh i hope it won't be that boring ;)
14:06 &lt;jrandom&gt; anyway, jumping on in to the good stuff: 1) 0.4.1.2
14:06 &lt;deer&gt; &lt;cervantes&gt; make me up after the statistal analysis section
14:06 &lt;jrandom&gt; the release is out and everyone should upgrade
14:06 &lt;jrandom&gt; heh
14:06 &lt;deer&gt; &lt;cervantes&gt; eerm wake
14:07 &lt;jrandom&gt; there are some bugs with the watchdog code, which will kill your router poorly (rather than restart it when bad stuff happens)
14:07 &lt;jrandom&gt; but hopefully those situations are few and far between
14:07 &lt;deer&gt; &lt;mule_iip&gt; nope :(
14:08 &lt;jrandom&gt; well, it varies by the user
14:08 &lt;jrandom&gt; i'm trying to find the cause, as its been around forever and its pretty annoying
14:08 &lt;jrandom&gt; (the actual hang, not the watchdog code that detects the hang)
14:09 &lt;jrandom&gt; the current CVS rev (0.4.1.2-1) has the 'meat' of the watchdog disabled - it monitors, but oesn't shut down the router
14:10 &lt;jrandom&gt; but 0.4.1.2 should be fine for everyone (except mule ;)
14:10 &lt;jrandom&gt; oh, as mentioned before, start up some logging and send me some data, per http://dev.i2p.net/pipermail/i2p/2004-October/000465.html
14:11 &lt;jrandom&gt; the more data the better - if you can leave it running overnight, that'd be great (a 20h run on duck's box generated ~60MB of data)
14:11 &lt;jrandom&gt; ok, moving on to 2) 0.4.1.3
14:12 &lt;jrandom&gt; well, there's not really anything i want to mention beyond wahts in the email
14:12 &lt;jrandom&gt; anyone have anything they want to say re: 0.4.1.3?
14:12 &lt;Janonymous&gt; nah
14:13 &lt;deer&gt; &lt;postman&gt; no
14:13 &lt;Janonymous&gt; backwards compatable?
14:13 &lt;jrandom&gt; certainly
14:13 &lt;jrandom&gt; ok, moving on to * 3) 0.4.2
14:14 &lt;jrandom&gt; again, another "see the email" :)
14:14 &lt;Janonymous&gt; xpc vs. tcp ??
14:14 &lt;jrandom&gt; i've never implemented a tcp stack before, so any guidance would be appreciated
14:15 &lt;jrandom&gt; xcp has better handling in networks with high delays
14:15 &lt;jrandom&gt; (for congestion control)
14:15 &lt;Janonymous&gt; does that include fec?
14:15 &lt;jrandom&gt; no
14:16 &lt;Janonymous&gt; k, cause I've been researching that some
14:17 &lt;jrandom&gt; cool
14:17 &lt;jrandom&gt; anything good you've found?
14:17 &lt;deer&gt; &lt;cervantes&gt; most GET requests are sub 32kb...and your average html page should be around that size...so I'd imagine eepsurfing will be much improved... - I wouldn't mind seeing an improvement in per-tunnel throughput though...will the new stack improve upon that?
14:17 &lt;Janonymous&gt; fec is used a lot for high latency/high throughput networks
14:18 &lt;deer&gt; &lt;mule_iip&gt; jrandom: nor have i, but i could tell a folk here to support you
14:18 &lt;Janonymous&gt; jrandom: some.. I'll report back
14:18 &lt;deer&gt; &lt;mule_iip&gt; at least it would be a good learning experience for him and another pair of eyes
14:18 &lt;jrandom&gt; great Janonymous 
14:18 &lt;jrandom&gt; oh kickass mule
14:18 &lt;jrandom&gt; cervantes: per-tunnel throughput would improve with&gt;1 message windows
14:19 &lt;jrandom&gt; (i expect we'll be able to even start with&gt;1 as a window size, depending upon what we can gleam from the router)
14:19 &lt;jrandom&gt; ((ecn++))
14:19 &lt;deer&gt; &lt;cervantes&gt; grand
14:20 &lt;jrandom&gt; ok, anything else on 0.4.2 stuff?
14:20 &lt;Janonymous&gt; fresh stack.. fresh laptop.. *drools*
14:21 &lt;jrandom&gt; heh
14:21 &lt;Janonymous&gt; yea
14:21 &lt;Janonymous&gt; one thing
14:22 &lt;Janonymous&gt; this will implement the new short handshake?
14:22 &lt;jrandom&gt; hmm?
14:22 &lt;jrandom&gt; we have the low-cpu TCP reconnection code in the 0.4.1 transport
14:22 &lt;Janonymous&gt; ah, in the email, you mention the alice-&gt; bob handshake
14:23 &lt;Janonymous&gt; ah
14:23 &lt;Janonymous&gt; still catching up
14:23 &lt;jrandom&gt; oh.  yeah, whatever 0.4.2 comes up with, it'll support a packet sequence like the one in the email
14:24 &lt;Janonymous&gt; k
14:24 &lt;jrandom&gt; we'll probably control it largely through socket options (e.g. set the stream to interactive and it sends asap, set the stream to bulk and it only sends when the buffer is full or itsflushed [or it needs to ack])
14:25 &lt;jrandom&gt; ok, swinging on to 4) mail discussion
14:25 &lt;jrandom&gt; postman - you 'round?
14:26 &lt;deer&gt; &lt;postman&gt; ya
14:26 &lt;jrandom&gt; word, wanna give us a run down / update wrt the mail stuff?
14:27 &lt;deer&gt; &lt;postman&gt; hmm, ok tho i am quite shy talking in front of that many ppl :)
14:27 &lt;jrandom&gt; heh just imagine we're all nak^H^H^Her... nm
14:28  * Janonymous gets popcorn out
14:28 &lt;deer&gt; &lt;postman&gt; since the 20th od september there is a SMTP/POP Service running - accessible with normal smtp/pop3 MUAs
14:29 &lt;deer&gt; &lt;postman&gt; i put quite some efforts in it in a way that i analyzed the potential risks that normal mail clients bear
14:29 &lt;Janonymous&gt; what about inproxies/outproxies?
14:29 &lt;deer&gt; &lt;postman&gt; put it all together on a website 
14:29 &lt;deer&gt; &lt;postman&gt; for those who haven't done so: www.postman.i2p
14:29  * Janonymous has not access to the network currently
14:30 &lt;deer&gt; &lt;postman&gt; there's a proposal on the website that tries to comprehend all the common problems dealing with anonymity and reliability of a mailservice when doing a bridging between i2p and internet
14:30 &lt;deer&gt; &lt;postman&gt; out/inproxy does not run yet but is in the planning
14:30 &lt;Janonymous&gt; I think I caught some of the discussion on the maillist or the forum
14:30 &lt;Janonymous&gt; out would be more dangerous than in, right?
14:31 &lt;deer&gt; &lt;postman&gt; first i want a commonly accepted concept
14:31 &lt;deer&gt; &lt;postman&gt; generally YES, but i think we found a way that spam and the likes won't be sent outward
14:31 &lt;jrandom&gt; what'd be neat is if the mx.postman.i2p in/outproxy could dispatch to different (or multiple redundant) pop3 accts
14:31 &lt;deer&gt; &lt;postman&gt; simply by putting a quota on every user trying to send mails out
14:32 &lt;jrandom&gt; (that way it wouldn't be tied to a particular mailhost)
14:32 &lt;deer&gt; &lt;postman&gt; jrandom2p: please explain further
14:33 &lt;Janonymous&gt; could the seperate mailhosts be syncronized too?
14:33 &lt;deer&gt; &lt;postman&gt; jrandom2p: it's a question of account based routing
14:33 &lt;jrandom&gt; right postman
14:33 &lt;jrandom&gt; probably lots of work, i dont know much about the MTAs you're working on
14:33 &lt;deer&gt; &lt;postman&gt; jrandom2p: the out/in proxy could easily handle more than one internal mailsystem - even could arrange a fallback kind of delivery 
14:34 &lt;jrandom&gt; 'k, great
14:34 &lt;Janonymous&gt; Q wrt in/out
14:34 &lt;deer&gt; &lt;postman&gt; janonymous: i did not understand your question - please explain
14:34  * jrandom dreams up uucp-style offline fetch from mx.postman :)
14:35 &lt;Janonymous&gt; would mandatory mailbox to mailbox encryption make in/out sending less dangerous?
14:35 &lt;deer&gt; &lt;postman&gt; jrandom: haha, uucp is not needed i think - maybe ETRN is sexier :)
14:35 &lt;deer&gt; &lt;postman&gt; janonymous: right now the system works only internaly - everyone is free to apply PGP or sth similiar
14:36 &lt;jrandom&gt; Janonymous: you should swing by www.postman.i2p - he's put up a chunk of ideas / issues on there
14:36 &lt;Janonymous&gt; mandatory encryption/signatures is also an antispam method I believe
14:36 &lt;deer&gt; &lt;Ragnarok&gt; would it be possible to serve the postman.i2p address book using LDAP?
14:36 &lt;Janonymous&gt; I will once my laptop comes in
14:37 &lt;deer&gt; &lt;postman&gt; rag: there's an addressbook already - it is based on SQL tho - a transfer to LDAP os possible
14:38 &lt;Janonymous&gt; = server hosted address book?
14:38 &lt;deer&gt; * postman invites everybody to contribute own ideas to the ideas/concepts html document
14:38 &lt;Janonymous&gt; will do postman
14:38 &lt;deer&gt; * cervantes spiders the address book and starts writing penis enlargement pharmacutical mails 
14:39 &lt;deer&gt; &lt;postman&gt; janonymous: well, ALL mailusers are SQL based - thus the "addressbook" is just a view on that table
14:39 &lt;deer&gt; &lt;postman&gt; cervantes: btw, every user can chose whether he wants to be visible or not
14:39 &lt;Janonymous&gt; ah
14:40 &lt;Janonymous&gt; how about selective groups ;)
14:40 &lt;deer&gt; &lt;cervantes&gt; postman: yup I've signed up already ;-)
14:40 &lt;deer&gt; &lt;postman&gt; cervantes: and since we HAVE a mailidentidy system , you cannot forge your senderaddress - we know it has been YOU :)
14:40 &lt;deer&gt; &lt;postman&gt; janonymous: yeah, it's planned for version 2.0 :)
14:41 &lt;deer&gt; &lt;cervantes&gt; postman: but I'll just spam every ircnym@postman.i2p ;-)
14:41 &lt;deer&gt; &lt;postman&gt; cervantes: this is technically possible, yes :)
14:42 &lt;deer&gt; &lt;postman&gt; cervantes: i hope you're able to deliver those pills too :)
14:42 &lt;Janonymous&gt; sounds like a much needed and long expected development for i2p
14:42 &lt;Janonymous&gt; the new email system
14:42 &lt;deer&gt; &lt;cervantes&gt; postman: and on the sender thing..the "Cervantes' penis enlargement elixir" would indicate the sender too :)
14:42 &lt;deer&gt; &lt;postman&gt; janonyous: i cannot tell about every detail implemented
14:43 &lt;deer&gt; &lt;postman&gt; jan: the website is best suited for this
14:43 &lt;deer&gt; &lt;postman&gt; cervantes: indeed - but this could be forged :)
14:43 &lt;Janonymous&gt; alrighty.. I'll get there asap
14:43 &lt;jrandom&gt; ok, great.  so, yeah, y'all should review whats up on www.postman.i2p and send in your ideas/comments
14:43 &lt;deer&gt; * postman nods and sits down again
14:44 &lt;jrandom&gt; (postman++)
14:44 &lt;jrandom&gt; ok that brings us to 5) ???
14:44 &lt;jrandom&gt; anyone have anything else they want to bring up?
14:44 &lt;jrandom&gt; (i2p related)
14:44 &lt;deer&gt; &lt;postman&gt; :)
14:44 &lt;Janonymous&gt; just a thought
14:45 &lt;Janonymous&gt; possible uses for I2P.. we know its a "distributed anonymous network layer"
14:45 &lt;deer&gt; &lt;Jake&gt; my node is down :( moving equipment to a different part of the house
14:46 &lt;Janonymous&gt; but what can that be used for.. particularly, those "common good" issues
14:46 &lt;Janonymous&gt; Oppressive third world countries, freedom of speech.. etc.. thats one of the primary things that got me so interested in i2p to start with
14:47 &lt;Janonymous&gt; and freenet for that matter
14:47 &lt;deer&gt; &lt;Jake&gt; oppressed 1st world countries like the u.s.
14:47 &lt;Janonymous&gt; so, I thought maybe some extrapolation on those issues, maybe starting on the forum, then some words on the site
14:48 &lt;jrandom&gt; we've got a lot of work to do before we can claim any relevence for people in china
14:48 &lt;Janonymous&gt; heh, yea, wouldn't want to make any false promises, but..
14:48  * jrandom will not say we're safe when there has been so little peer review (and there are still so many outstanding issues)
14:49 &lt;deer&gt; &lt;fidd&gt; how hard will it be for china to censor i2p?
14:49 &lt;deer&gt; &lt;cervantes&gt; I think applications will begin to surface more readily once the underlying network has stopped "shapeshifting"
14:49 &lt;Janonymous&gt; but those issues to me are one of the main things that makes i2p so exciting
14:49 &lt;jrandom&gt; fidd: censor has many definitions.  in the sense "stop specific content from being transferred", pretty much impossible, short of making i2p illegal
14:50 &lt;Janonymous&gt; how about, "detect i2p on networks in china"
14:50 &lt;Janonymous&gt; stego?
14:51 &lt;jrandom&gt; exciting, yes.  important?  yes.  necessary?  yes.  but since there's so much work to do before we're relevent, its just depressing to talk about it.
14:51 &lt;Janonymous&gt; my bad :) 
14:51 &lt;deer&gt; &lt;cervantes&gt; once the base network is solid, then we could probably do with some nice toys to play with  - eg filesharing apps, IM systems etc. Hopefully the userbase will swell at that point....before this happens there just won't be enough peers to guarantee anonymity for people who live in oppressive systems
14:52 &lt;jrandom&gt; its always important to keep your eyes on the real goals Janonymous, and i appreciate that
14:52 &lt;Janonymous&gt; yea, numbers of nodes has a lot to do with it
14:52 &lt;modulus&gt; imo until there is stego and things like random noise to defeat traffic analysis people in oppressive countries should stay away for a while.
14:53 &lt;deer&gt; &lt;cervantes&gt; no..they should stay here and help :)
14:53 &lt;modulus&gt; :-)
14:53  * jrandom will not describe in detail why those aspects won't be necessary, as the 3.0 rev will take care of 'em :)
14:53 &lt;modulus&gt; 3.0? sounds long-term ;-)
14:53 &lt;jrandom&gt; i have ~= 0 faith in stego transports for public networks
14:54 &lt;jrandom&gt; it aint tomorrow, thats for sure.
14:54 &lt;Janonymous&gt; word? huh
14:54 &lt;Janonymous&gt; jrandom: whys that (wrt stego)?
14:55 &lt;jrandom&gt; how to defeat stego on public networks with open source software: download the source, review the stego generation code, write detection code, deploy.
14:56 &lt;jrandom&gt; how to defeat stego on public networks with closed source software: kidnap the dev's family, subvert the code.  deploy.
14:56 &lt;Janonymous&gt; ah.. yea.. random inputs? eh.. I just read this article talking like it was the future or something
14:56 &lt;jrandom&gt; how to defeat stego on private networks:  laugh at the 5 people using it, and arrest 'em all.
14:56 &lt;modulus&gt; well, what about anonymous closed-source software? of course it could be a trojan ;-)
14:57 &lt;deer&gt; &lt;Jake&gt; jrandom: if you're ever kidnapped, you can let us know by telling us "my dog fido is really upset about the food he's eating today"
14:57 &lt;deer&gt; &lt;Jake&gt; that will be the giveaway and we'll know
14:57 &lt;deer&gt; &lt;cervantes&gt; %s!dev's family!jrandom
14:57 &lt;jrandom&gt; heh jake
14:58 &lt;Janonymous&gt; whens the eta for 4.2?
14:58 &lt;jrandom&gt; Janonymous: the #1 feature of anonymity or security software: snake oil.
14:58 &lt;jrandom&gt; 0.4.2?  sometime this month
14:58 &lt;jrandom&gt; prolly near the end
14:58 &lt;Janonymous&gt; heheh. 
14:58 &lt;jrandom&gt; 0.4.1.3 will prolly be out later this week or the weekend
14:58 &lt;deer&gt; &lt;cervantes&gt; Jake: that would never work, we'll juist think you've poisoned his dog
14:58 &lt;deer&gt; &lt;cervantes&gt; *just
14:58 &lt;Janonymous&gt; I should be back on the net in a week or two
14:59 &lt;jrandom&gt; r0x0r
14:59 &lt;jrandom&gt; ok, anyone else have something to bring up?
14:59 &lt;deer&gt; &lt;Jake&gt; cervantes :)
15:00 &lt;jrandom&gt; if not..
15:00  * jrandom winds up
15:00  * jrandom *baf*s the meeting closed
</div>
