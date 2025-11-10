---
title: "I2P Dev Meeting - October 18, 2005"
date: 2005-10-18
author: "jrandom"
description: "I2P development meeting log for October 18, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, blx, cervantes, dust, GregorK, jme___, jnymo, jrandom, mrflibble, nickless_head, Ragnarok, Rawn, redzara, tethra, vulpine</p>

## Meeting Log

<div class="irc-log">
16:10 &lt;jrandom&gt; 0) hi
16:10 &lt;jrandom&gt; 1) 0.6.1.3
16:10 &lt;jrandom&gt; 2) Freenet, I2P, and darknets (oh my)
16:10 &lt;jrandom&gt; 3) Tunnel bootstrap attacks
16:10 &lt;jrandom&gt; 4) I2Phex
16:10 &lt;jrandom&gt; 5) Syndie/Sucker
16:10 &lt;jrandom&gt; 6) ???
16:10 &lt;jrandom&gt; 0) hi
16:10  * jrandom waves
16:10 &lt;jrandom&gt; weekly status notes are up at http://dev.i2p.net/pipermail/i2p/2005-October/001017.html
16:10 &lt;dust&gt; yay, works now. thanks Gregor
16:10 &lt;cervantes&gt; hullo
16:11 &lt;+fox&gt; &lt;blx&gt; heloa
16:11 &lt;jrandom&gt; ok, jumping into 1) 0.6.1.3
16:11 &lt;jrandom&gt; y'all have updated at a pretty good clip, thanks!  
16:12 &lt;jrandom&gt; things seem to be in reasonable condition, but I don't have much to add beyond whats in the status notes
16:12 &lt;jrandom&gt; anyone have any questions/comments/concerns re: 0.6.1.3?
16:13 &lt;jrandom&gt; ok if not, lets jump on in to 2) Freenet, I2P, and darknets (oh my)
16:13 &lt;cervantes&gt; 609 known peers!
16:14 &lt;cervantes&gt; (w00t)
16:14 &lt;jrandom&gt; aye, network has been growin'
16:14 &lt;+fox&gt; &lt;blx&gt; oh my!
16:14  * cervantes is holding a sweepstake for how long until the big 1000
16:14 &lt;jrandom&gt; heh
16:14 &lt;tethra&gt; heheh
16:15 &lt;tethra&gt; are we betting with digital cash? ;)
16:15 &lt;cervantes&gt; but it show how solid i2p core has got lately that the user uptake has been accelerating
16:16 &lt;cervantes&gt; nah...jrandom has already unknowningly donated all his beer money for this year
16:16 &lt;jrandom&gt; hehe
16:16 &lt;jrandom&gt; ok, on 2), i'm not sure if i've got anything else to add to the subject (i think we've flogged that horse).  anyone have any questions/comments/concerns on it?
16:18 &lt;cervantes&gt; as you said, if nothing else it has stimulated some interesting semi-related security discussions ie 3)
16:18 &lt;jrandom&gt; if not, we can jump forward at a quick pace to 3) Tunnel bootstrap attacks
16:18 &lt;jrandom&gt; aye, that it has
16:19 &lt;jrandom&gt; the issue Michael brought up quantifies a general view i've had, but its nice to make it explicit
16:20 &lt;jrandom&gt; there's going to be some further discussion on the newer attack later this evening (once i can write up a reply), but the former doesn't seem to be much of a problem
16:21 &lt;jrandom&gt; does it make sense to people, or do people have any questions or concerns about it?
16:22 &lt;cervantes&gt; heh...that either means everyone is cool with it or they can't make head of tail of what the issues are
16:23 &lt;cervantes&gt; I'll put myself in the ignorance is bliss category
16:23 &lt;jrandom&gt; heh its basically an attack where the mean guys just happen to be the outbound endpoint of every tunnel you've ever built
16:23 &lt;jrandom&gt; now, when you're just starting up, "every tunnel you've ever built" is a very small number (eg. 0, 1, 2)
16:24 &lt;jrandom&gt; but after a few seconds, the number grows large enough to turn (c/n)^t into a really really small number
16:25 &lt;tethra&gt; (c/n)^t is...
16:25 &lt;jrandom&gt; (this is one of the reasons why we don't start up the i2cp listener - and hence, i2ptunnel/etc - until a little while after startup)
16:25 &lt;jrandom&gt; c == # of colluding peers (bad guys), n == # of peers in the network, t == # of tunnels you've built.
16:25 &lt;cervantes&gt; right...
16:25 &lt;tethra&gt; ah
16:26 &lt;jrandom&gt; so as t grows, the probability of successful attack gets really small
16:26 &lt;cervantes&gt; so for it to be even viable you'd have to start using your router for sensitive tasks within a couple of minutes of it starting up?
16:26 &lt;jrandom&gt; (or, in any case, smaller than the probability of taking over all hops in a tunnel)
16:26 &lt;tethra&gt; ahh, i see
16:27 &lt;jrandom&gt; cervantes: immediately, before the 3rd tunnel is built
16:27 &lt;jrandom&gt; (assuming you use 3 hop tunnels)
16:27 &lt;cervantes&gt; that's fairly improbable
16:28 &lt;cervantes&gt; just from a use case perspective
16:28 &lt;jrandom&gt; 'zactly.
16:28 &lt;jrandom&gt; and since we build more than 3 tunnels on startup before letting any clients run, its not just a probability issue
16:28 &lt;jrandom&gt; but its good to quanitify the attack anyway
16:29 &lt;cervantes&gt; is it worth letting the router churn for a bit longer to guard against any likelyhood?
16:30 &lt;cervantes&gt; or churn harder...
16:30 &lt;jrandom&gt; perhaps.  if we ignore connection establishment time as well as nonrandom peer selection, it has no likelihood
16:31 &lt;tethra&gt; that's cause for a "woot!" i take it?
16:32 &lt;jrandom&gt; aye, though from an engineering perspective, we shouldn't ignore those characteristics ;)  
16:32 &lt;jrandom&gt; so, for 0.6.2 we may want to look at it during the revamped tunnel peer selection / ordering implementation, to make sure its behaving Sanely
16:34 &lt;jrandom&gt; ok, if there's nothing else on 3), lets move on to 4) I2Phex
16:34 &lt;jrandom&gt; sirup isn't here, and i haven't seen striker on irc - redzara, you around?
16:36 &lt;+redzara&gt; yes
16:36 &lt;+redzara&gt; First pass is nearly completed : port Sirup's mod to lastest phex cvs.
16:36 &lt;jrandom&gt; nice1!
16:36 &lt;+redzara&gt; next : Second pass : diff from Sirup code to base phex code used in initial release, to be sure i don't forget anything :)
16:37 &lt;+redzara&gt; maybe terminated for this W.E.
16:37 &lt;jrandom&gt; wow that'd be great
16:37 &lt;+redzara&gt; Pass three : refactoring comm layer with GregorK
16:37 &lt;+fox&gt; &lt;GregorK&gt; hope you are aware that in latest Phex CVS the download code is not stable and the download file is not compatible with previous releases
16:38 &lt;jrandom&gt; this is i2p, we're used to instability :)
16:38 &lt;+fox&gt; &lt;GregorK&gt; :)
16:38 &lt;+redzara&gt; For the last pass, as I've currently no contact with GregorK, this sould be pretty hard :(
16:38 &lt;jrandom&gt; GregorK: what would you recommend for inegration?
16:39 &lt;+fox&gt; &lt;GregorK&gt; well you now have contact with me ;)
16:39 &lt;jrandom&gt; ah 'k redzara, the first two are big enough in any case :)
16:39 &lt;+redzara&gt; GregorK : hi man
16:40 &lt;+redzara&gt; GregorK : I've read carefully all codes
16:40 &lt;+fox&gt; &lt;GregorK&gt; I have a idea on how to build a layer... I can try to prepare it as good as i can and then we can see how good it fits and what needs to be changed
16:40 &lt;+fox&gt; &lt;GregorK&gt; all?? wow...
16:40 &lt;+redzara&gt; Gregork : yes, all !!
16:41 &lt;cervantes&gt; he even knows the size of your underwear
16:41 &lt;Rawn&gt; :D
16:41 &lt;+fox&gt; &lt;GregorK&gt; great... next time I'm shopping I just need to ask you... 
16:43 &lt;+fox&gt; &lt;GregorK&gt; what would be nice if we could maybe have someone from the i2phex team on the phex team too..
16:43 &lt;jrandom&gt; redzara: so, do you think we'll have a 0.1.2 I2Phex release with the results of your second pass before we get everything merged into a plugin layer in the mainline Phex?  or will that be all in one go?
16:43 &lt;+redzara&gt; Sorry, but I don't understand / speak /read / write english good enough to  laugh with what you have writed
16:43 &lt;+fox&gt; &lt;GregorK&gt; this would also help solve bugs that are on both sides
16:44 &lt;jrandom&gt; GregorK: hopefully we'll find a way that the I2P side is just a thin plugin in Phex though, right?
16:44 &lt;jrandom&gt; or do you think the two should stay separate?
16:44 &lt;+redzara&gt; jrandom : I think we could have an Phex 2.6.4 over I2P, for me I2Phex is down
16:45 &lt;jrandom&gt; down?
16:45 &lt;+fox&gt; &lt;GregorK&gt; i'm not sure if we can make it this way right from the start, but I think the major part of it could be separated into a plugin.
16:45 &lt;jrandom&gt; cool, yeah, its a lot of work, I'm sure
16:46 &lt;jrandom&gt; especially when you look at things like java.net.URL (which leaks DNS requests on instantiation, etc)
16:46 &lt;+redzara&gt; jrandom : down, endded
16:46 &lt;+Ragnarok&gt; grr
16:47 &lt;jrandom&gt; ok right redzara, one we can get everything working in Phex 2.6.4 over I2P, I agree, there wouldn't seem to be much of a need for an I2Phex
16:47 &lt;+fox&gt; &lt;GregorK&gt; right... I think Phex uses the apache URI class in some places to work around this.. but only when necessary
16:48 &lt;jrandom&gt; ah right, I remember playing around with that library, looks good
16:49 &lt;jrandom&gt; we'll definitely be helping audit things a bit for anonymity/security before pushing it for end users over i2p
16:49 &lt;jrandom&gt; (not to suggest there are any problems in Phex, just there are problems in every app, and hopefully we can help sort 'em out)
16:50 &lt;+fox&gt; &lt;GregorK&gt; for some things like Socket use and these things I have an idea on how to integrate it smothly... but other places like different features UDP and such... I'm not sure yet how to solve them best
16:50 &lt;+fox&gt; &lt;GregorK&gt; oh i'm sure there are many problems in phex. :)
16:50 &lt;jrandom&gt; ah, yeah sockets will be easy, but we may need to disable other things.  what is udp used for - quick queries?
16:51 &lt;+fox&gt; &lt;GregorK&gt; currently only bootstrapping
16:51 &lt;+fox&gt; &lt;GregorK&gt; UDP Host Cache.. a replacement for GWebCache
16:52 &lt;jrandom&gt; ahhh, ok.  
16:52 &lt;+redzara&gt; So we don't need it if we have a descent GwebCache ?
16:53 &lt;+fox&gt; &lt;GregorK&gt; yes... but the standard GWebCache have there security problems too...
16:53 &lt;+redzara&gt; GregorK : not inside I2P I think
16:54 &lt;jrandom&gt; oh, that part could be overcome - I2PSocket is authenticated - you know the 'destination' of the peer on the other end, so they couldn't say "I'm, er... whitehouse.gov.. yeah!"
16:54 &lt;jrandom&gt; but you're right, its soemthing that needs to be verified 
16:54 &lt;+fox&gt; &lt;GregorK&gt; also firewall to firewall transfers would be a UDP topic we like to implement once we find a volunteer :)
16:54 &lt;jrandom&gt; ah, well, I2P doesn't need firewall to firewall transfers - I2P exposes an entirely open end to end address space :)
16:55 &lt;jrandom&gt; but... ooh, thats something that might be useful
16:55 &lt;jrandom&gt; if Phex users had "0 hop tunnels", they'd get free NAT traversal/firewall to firewall transfers with pretty decent speed
16:55 &lt;+fox&gt; &lt;GregorK&gt; another one would be LAN broadcasts of queries and such... for easier sharing of contents in private networks
16:56 &lt;jrandom&gt; (0 hop tunnels offers a level of plausible deniability without requiring any intermediary peers to carry the trafffic)
16:57 &lt;jrandom&gt; hmm, lan broadcast is good, though i'm not sure if i2p would really need that (since its an anonymity risk to know where the other peer is :), so perhaps that feature could be disabled when using the I2P plugin?
16:58 &lt;cervantes&gt; *disabled by default
16:58 &lt;+fox&gt; &lt;GregorK&gt; well its not available yet.. but in this case user usually know each other anyway to build that private network..
16:58 &lt;jrandom&gt; oh right cervantes 
16:58 &lt;jrandom&gt; right right GregorK
16:59 &lt;+fox&gt; &lt;GregorK&gt; are there any changes regarding the user interface??
17:00 &lt;+bar&gt; well, we won't need flags :)
17:00 &lt;jrandom&gt; at the least, the ability to have a few configuration options related to I2P would be useful.
17:01 &lt;jrandom&gt; i think sirup was able to switch in some of the display to use I2P 'destinations' instead of showing IP + port numbers, so I think it was fine 
17:01 &lt;+redzara&gt; And what about bitzyNot for the moment, but flags and countries are unused
17:01 &lt;jrandom&gt; bitzy?
17:01 &lt;+redzara&gt; sorry, wrong coupy/paste :(
17:02 &lt;+fox&gt; &lt;GregorK&gt; can you provide a list of configuration options and optional features you need?
17:03 &lt;jrandom&gt; I'm sure we can get those to you.  a host+port that I2P is running on and a few drop downs regarding performance/anonymity tweaks should do it
17:03 &lt;jrandom&gt; we'll get you the details though
17:02 &lt;cervantes&gt; [x] Super transfer speed mode
17:02 &lt;+fox&gt; &lt;GregorK&gt; well bitzi is used to identify files.. is that an anonymity problem?
17:03 &lt;vulpine&gt; &lt;redzara&gt; GregorK : I'm preparing it, but basicly, thre is no changes
17:03 &lt;+fox&gt; &lt;GregorK&gt; :) ask your provider cervantes...
17:03 &lt;redzara&gt; GregorK : maybe, I'm working on it
17:04 &lt;cervantes&gt; GregorK: heh UK resident....no chance ;-)
17:04 &lt;+fox&gt; &lt;GregorK&gt; if you transfer files between 2 Phex instances on the same PC.. transfers are lightning fast ;)
17:05 &lt;cervantes&gt; cool...I have lots of cool movies I can share with myself :)
17:05 &lt;cervantes&gt; * strike that from the meeting notes *
17:06 &lt;bar&gt; jrandom touched the subject before, but, here's that crazy idea again:
17:06 &lt;+bar&gt; how 'bout integrating i2p into Phex, so that ordinary users have 0-hop tunnels?
17:07 &lt;+fox&gt; &lt;GregorK&gt; I think display of flags and IP+port comes from the HostAddress object.. which would be hidden from the new layer.. so you can display something else
17:07 &lt;+bar&gt; (for plausible deniability and udp firewall hole punching)
17:08 &lt;+fox&gt; &lt;GregorK&gt; not sure if I really understand what that means ;)
17:08 &lt;+bar&gt; probably me neither ;)
17:09 &lt;jrandom&gt; GregorK: essentially, it means that Phex users would talk to each other directly, but would get plausible deniability, as they could be talking indirectly
17:09 &lt;+bar&gt; jrandom, i'm sure you're catching my drift here, could you elaborate?
17:09 &lt;jrandom&gt; they'd also get I2P's NAT traversal thrown in for free, as well as data security and protection from sniffing by ISPs/etc
17:09 &lt;+redzara&gt; GregorK : so you have to strip all code related to host+port + IsLocalIP + Is PrivateIP + ...
17:10 &lt;jrandom&gt; on the other hand, (a BIG other hand), it wouldn't be able to talk to gnutella clients that don't run on top of I2P
17:10 &lt;jrandom&gt; (though eventually, they all will ;)
17:10 &lt;+fox&gt; &lt;GregorK&gt; Well I think the first step is - and that step is already big enough - to bring i2p and phex closer together.
17:10 &lt;jrandom&gt; agreed
17:10 &lt;+bar&gt; (damn, didn't think of that)
17:11 &lt;+bar&gt; yeah, def.
17:11 &lt;jrandom&gt; this is flying pony stuff.  lets get the practical things first
17:11 &lt;+fox&gt; &lt;GregorK&gt; and after we see how good that worked we can decide how we go further.. 
17:11 &lt;jrandom&gt; exactly
17:12 &lt;+fox&gt; &lt;GregorK&gt; redzara: I like to have two implementations of HostAddress one for i2p and on like the current.
17:14 &lt;+redzara&gt; Gregork : no pb, I've commented all code in my mod you could easyly build two implementations. Just let me finish the initial work please
17:14 &lt;+fox&gt; &lt;GregorK&gt; sure.. no problem..
17:14 &lt;jrandom&gt; :)  ok, so redzara, you think we may be able to get an alpha test of the new Phex-2.4.2 based version sometime next week?
17:15 &lt;jrandom&gt; (for the phase 2 part.  your phase 3 will take more work integrating with the mainline)
17:15 &lt;+redzara&gt; jrandom : next sems to be ok for me
17:16 &lt;jrandom&gt; ok great
17:16 &lt;+redzara&gt; s/next/next week/
17:16 &lt;jrandom&gt; ok, this is pretty exciting stuff, it'll be wonderful to get it going smoothly 
17:17 &lt;jrandom&gt; does anyone have anything else to bring up for 4) I2Phex, or shall we move on briefly to 5) Syndie/Sucker?
17:17 &lt;cervantes&gt; I2P will surely benefit from such killer apps
17:18 &lt;+fox&gt; &lt;GregorK&gt; btw there is a Phex CVS mailing list for all CVS changes in Phex... if that is of any help
17:18 &lt;jnymo&gt; *ehem*.. hell yes
17:18 &lt;jrandom&gt; ok great, thanks GregorK
17:18 &lt;jrandom&gt; definitely cervantes 
17:19 &lt;jrandom&gt; ok, on 5), I don't really have anything to add beyond whats there
17:19 &lt;jrandom&gt; dust: are you around?
17:19 &lt;+redzara&gt; GregorK : Thanks but handlingone version is far enough for me :)
17:19 &lt;jrandom&gt; hehe redzara 
17:19 &lt;dust&gt; I haven't had much spare time lately, but if I do I'm thinking I'll try to get a handle on this addresses.jsp thing, add 'RSS' in the protocol dropdown in there and then build a path through Updater, Sucker to BlogManager.
17:20 &lt;dust&gt; unless anyone have a better idea
17:20 &lt;jrandom&gt; kickass
17:20 &lt;jrandom&gt; that sounds perfect.
17:21 &lt;jrandom&gt; though, hmm, maybe it'd need an additional field (the "what blog to post it in" and "what tag prefix")...
17:21 &lt;jrandom&gt; maybe a separate form/table would make sense, though maybe not
17:22 &lt;dust&gt; oh, I thought addresses.jsp was for one blog only (since you have to login to get there?)
17:22 &lt;jrandom&gt; ah, true, good point
17:23 &lt;jrandom&gt; the updater part is kind of fuzzy, but you're right
17:23 &lt;dust&gt; (we'll figure it out when we get there)
17:23 &lt;jrandom&gt; aye
17:24  * jnymo thinks www.i2p.net could start up a 'merchandise cafe' type thing
17:24 &lt;jnymo&gt; with eyetoopie shirts that say "I am Jrandom" on them ;)
17:24  * mrflibble  is still catching up on the "flamewar",  which seems to be spiraling into  a proper flamewar :)
17:24 &lt;jrandom&gt; heh jnymo 
17:25 &lt;jrandom&gt; yeah, there's a lot of content in that thread
17:25 &lt;jrandom&gt; ok, maybe this gets us to 6) ???
17:25 &lt;jrandom&gt; anyone have anything else to bring up for the meeting?
17:25 &lt;+bar&gt; aye, just a quick note on the symmetric nat issue (been doin a lil snoopin'):
17:25 &lt;+nickless_head&gt; jrandom: I know the truth!
17:25 &lt;+fox&gt; &lt;blx&gt; kaffe?
17:25 &lt;mrflibble&gt; oops,  sorry jr
17:26 &lt;jnymo&gt; but seriously.. every open source project of any size has their own merchandise section
17:26 &lt;+nickless_head&gt; jrandom: I have definite proof you hacked the last.fm homepage!
17:26 &lt;+nickless_head&gt; (the what you get when you sign up section listed 'a pony')
17:26 &lt;jrandom&gt; jnymo: i think you're right, we will want to explore that avenue, might be a good method of fundraising too
17:27 &lt;jnymo&gt; jrandom: exactly
17:27  * mrflibble would buy the tshirt
17:27 &lt;+bar&gt; right, regarding symmetric nats,
17:27 &lt;+bar&gt; for what it's worth, i think that unlike for the already supported nats, there's no magic trick. the only way to do it properly, is to study and examine each and every symmetric nat's behaviour and use introducers for probing.
17:28 &lt;jrandom&gt; blx: the latest kaffe CVS is completely b0rked.  the crypto packages aren't in the source, the prng fails to initialize, and the url handlers can't deal with file:// :(
17:28 &lt;jnymo&gt; You probably wouldn't want to wear it in public until i2p has a few thousand users though ;)
17:28 &lt;+bar&gt; (i believe this is how e.g. Hamachi and Skype do udp hole punching from behind symmetric nats)
17:28 &lt;+nickless_head&gt; jnymo: cups would rule :)
17:28 &lt;+bar&gt; based on what i have read on the 'net so far, symmetric nat prediction algos pretty much suck.
17:28 &lt;jrandom&gt; hmm bar
17:28 &lt;mrflibble&gt; hehe, i wouldn't put my nick on it. oh, and i'm still allive/unarrested even though  i've got an IIP ttshirt
17:28 &lt;jrandom&gt; yeah, thats what i read too
17:29 &lt;+bar&gt; i will try gathering some more good, relevant reading material on this.
17:29 &lt;+redzara&gt; Small question : what was the common average percentage of bytes retransmitted in 0.6.1.3 ?
17:29 &lt;jrandom&gt; thanks bar
17:29 &lt;+fox&gt; &lt;jme___&gt; bar, the prediction they got are consistent ? 
17:29 &lt;+fox&gt; &lt;jme___&gt; bar, let me rephrase :)
17:29 &lt;+fox&gt; &lt;blx&gt; jrandom, i'm sad to hear
17:30 &lt;jrandom&gt; redzara: I unfortunately forgot to put that into the netDb.  I do see 2.6 and 3.8 right now though
17:30 &lt;jrandom&gt; blx: me too :(
17:30 &lt;+fox&gt; &lt;jme___&gt; bar, when you analyze the nat box behaviour and find a formula to predict it. does this always work for this nat box ? or later once it worked, once it fails ?
17:30 &lt;jrandom&gt; blx: i know they're doing some merging with classpath now though, so hopefully once thats sorted
17:30 &lt;+fox&gt; &lt;blx&gt; probably means i wont be joining the party
17:30 &lt;jrandom&gt; blx: are you kaffe-specific, or OSS/DFSG-specific?
17:31 &lt;+fox&gt; &lt;blx&gt; free software
17:31 &lt;+fox&gt; &lt;blx&gt; dfsg you could say
17:31 &lt;jnymo&gt; encase an i2p user wants to use a hosted server for i2p, what would be a liberal, cheap hosted services company to go with?
17:31 &lt;+bar&gt; jme___: hamachi is reportedly able to mediate 97% of all connection attempts. i guess there are some nats out there that show an almost random behaviour when it comes to assigning ports
17:32 &lt;jrandom&gt; ok, I'm sure we'll get something going blx.  kaffe used to work, and we don't depend upon anything sun specific
17:32 &lt;jrandom&gt; jnymo: i use sagonet.net, but they've cranked up their prices from 65/mo to 99/mo (but on a fast link w/ 1250GB/mo)
17:32 &lt;jrandom&gt; i know there are some cheap ones in germany too
17:33 &lt;+fox&gt; &lt;jme___&gt; bar, 97% would be terrific
17:33 &lt;jrandom&gt; redzara: what are you seeing for retransmission rate?
17:33 &lt;+bar&gt; jme___: yeah, so i guess most symmetric nats are predictable
17:33 &lt;+fox&gt; &lt;blx&gt; jrandom, i sure hope so. i'm really interested in this shit :)
17:33 &lt;+fox&gt; &lt;jme___&gt; bar, what would you do ? relay, udp hole punching, cnx reversal.. is there others thech ?
17:33 &lt;jnymo&gt; is 99 expensive, on average?
17:34 &lt;+redzara&gt; jrandom between 3;8 and 4.2
17:34 &lt;jrandom&gt; jme___: we're udp, no need for connection reversal :)
17:35 &lt;+bar&gt; jme___: i'm no expert, perhaps i'll have some more info for next week's meeting (but it sure smells like profiling + udp hole punching ;)
17:35 &lt;jrandom&gt; jnymo: for 1250GB, not really.  i've seen 60-120USD/mo for 50-100GB/mo
17:35 &lt;jrandom&gt; bar: perhaps UPnP would be a better way to go?
17:35 &lt;+fox&gt; &lt;jme___&gt; jrandom, even with udp it is usefull :)
17:35 &lt;+redzara&gt; jrandom : but only some node done major impact, maybe some olders
17:35 &lt;+fox&gt; &lt;jme___&gt; vulpine: ok
17:35 &lt;jrandom&gt; though that only helps the people who could control their NAT
17:36 &lt;+fox&gt; &lt;jme___&gt; upnp must be supported but it isnt exclusive to other means
17:36 &lt;jrandom&gt; well, we're doing everything we do now without any UPnP
17:36 &lt;+fox&gt; &lt;jme___&gt; because upnp isnt supported by all nat, far from it
17:36 &lt;jrandom&gt; right, e.g. an ISP's nat
17:36 &lt;+bar&gt; jrandom: if there are no security issues with upnp, i guess it can't hurt. though, hamachi doesn't use upnp
17:36 &lt;+fox&gt; &lt;jme___&gt; here by 'must' = to provide the max connectivity
17:37 &lt;+fox&gt; &lt;jme___&gt; ok going back to my c++ :)
17:38 &lt;jrandom&gt; right jme___, though if we can do symmetric hole punching in addition to cone/restrited hole punching, we're in great shape
17:38 &lt;jrandom&gt; l8s jme___
17:38 &lt;jrandom&gt; yeah, it'd be ideal if we didn't need it
17:39 &lt;jrandom&gt; ok, anyone have anything else to bring up for the meeting?
17:41 &lt;jrandom&gt; if not...
17:41  * jrandom winds up
17:41  * jrandom *baf*s the meeting closed
</div>
