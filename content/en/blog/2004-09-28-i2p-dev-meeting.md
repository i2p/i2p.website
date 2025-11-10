---
title: "I2P Dev Meeting - September 28, 2004"
date: 2004-09-28
author: "jrandom"
description: "I2P development meeting log for September 28, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> deer, duck, jrandom</p>

## Meeting Log

<div class="irc-log">
14:08 &lt;jrandom&gt; 0) hi
14:08 &lt;jrandom&gt; 1) New transport
14:08 &lt;jrandom&gt; 2) 0.4.1 status
14:08 &lt;jrandom&gt; 3) ???
14:08 &lt;jrandom&gt; 0) hi
14:08 &lt;duck&gt; hi
14:09 &lt;jrandom&gt; heya
14:09 &lt;deer&gt; &lt;ugha2p&gt; Hi.
14:09 &lt;deer&gt; &lt;pseudonym&gt; hi
14:09 &lt;jrandom&gt; weekly status notes posted up @ http://dev.i2p.net/pipermail/i2p/2004-September/000454.html
14:09 &lt;deer&gt; * ugha2p is looking for the weekly status notes.
14:09 &lt;jrandom&gt; (hey, i'm psychic)
14:10 &lt;jrandom&gt; ok, jumping in to 1) New transport
14:10 &lt;jrandom&gt; the message pretty much covers the main bits
14:11 &lt;jrandom&gt; its all working atm, but obviously wont talk to anyone else until the new release is out
14:12 &lt;jrandom&gt; i've kicked the tires on it a bit, but its pretty hard to simulate all the possible kooky network problems that occur at the transport level
14:12 &lt;deer&gt; &lt;pseudonym&gt; does it include windowsize?
14:12 &lt;deer&gt; &lt;ugha2p&gt; However, if you leave that blank, your router will let the first peer it contacts tell it what its IP address is, which it will then start listening on (after adding that to its own RouterInfo and placing that in the network database).
14:12 &lt;deer&gt; &lt;ugha2p&gt; Sounds like a potential security hole.
14:12 &lt;jrandom&gt; oh, no, this is just the inter-router transport, not the streaming lib, unfortunately
14:12 &lt;deer&gt; &lt;pseudonym&gt; ok
14:12 &lt;jrandom&gt; in a way ugha, yes
14:12 &lt;jrandom&gt; (which is why if people *can* set their IP, they should)
14:13 &lt;jrandom&gt; ugha: however, it only 'believes' someone if they have NO connections that work
14:13 &lt;deer&gt; &lt;ugha2p&gt; Shouldn't the router listen on 0.0.0.0 in any case?
14:13 &lt;jrandom&gt; but someone pretty smart could probabalistically do some evil things
14:14 &lt;jrandom&gt; ugha: it does that (almost always)
14:14 &lt;jrandom&gt; however, we need to know our IP address so we can put it in our RouterInfo
14:14 &lt;jrandom&gt; (since our RouterInfo is verified whenever we contact someone)
14:14 &lt;deer&gt; &lt;ugha2p&gt; Ah, ok.
14:15 &lt;deer&gt; &lt;ugha2p&gt; I'm sure there are ways to make this more secure (rely on more routers for detecting the IP), but I'm not sure if this is feasible.
14:15 &lt;jrandom&gt; yeah ugha, there's trouble down that path, but its a numbers game
14:16 &lt;deer&gt; &lt;ugha2p&gt; Anyhow, that was just a suggestion. We can move on.
14:16 &lt;jrandom&gt; (however, they could just sybil you and mess up whatever #s you're trying)
14:16 &lt;deer&gt; &lt;ugha2p&gt; Right.
14:17 &lt;deer&gt; &lt;ugha2p&gt; What if the router loses all connections (eg, network failure)?
14:17 &lt;deer&gt; &lt;ugha2p&gt; Does it redetect its IP?
14:18 &lt;jrandom&gt; the IP is transmitted as part of the protocol on all connection attempts, the peer just decides to honor it if 1) no ip was explicitly set 2) there are no active TCP connections
14:18 &lt;deer&gt; &lt;ugha2p&gt; (This would be the case with dynamic IPs)
14:18 &lt;jrandom&gt; right, it'll work fine with that
14:18 &lt;deer&gt; &lt;ugha2p&gt; Ah, ok.
14:19 &lt;jrandom&gt; (see ourAddressReceived(String addr) in TCPTransport.java for the details)
14:19 &lt;deer&gt; &lt;pseudonym&gt; what happens when reported IPs don't match?
14:19 &lt;jrandom&gt; pseudonym: if you already have active TCP connections, you ignore what other people tell you
14:20 &lt;jrandom&gt; if you dont have active TCP connections, you tear down the old listener and start up a new one with the new address given
14:20 &lt;jrandom&gt; (updating your routerInfo)
14:22 &lt;deer&gt; &lt;pseudonym&gt; if there are active conns, it seems like a mismatch should be a red flag
14:22 &lt;deer&gt; &lt;pseudonym&gt; (I'm not sure what to do with it)
14:22 &lt;jrandom&gt; if someone gives us the wrong IP address (and we *know* its the wrong IP address, since we already have the right one - that *works*) we ignore it
14:23 &lt;deer&gt; &lt;ugha2p&gt; Too bad we can no longer reduce the router's reliability ranking.
14:23 &lt;jrandom&gt; we can add that to the list of connection errors though
14:24 &lt;jrandom&gt; ugha: but we can shitlist 'em ;)
14:24 &lt;jrandom&gt; (and we do)
14:24 &lt;deer&gt; &lt;pseudonym&gt; how do we know the one we already have is "right"?  maybe the existing conns are from black hats
14:24 &lt;deer&gt; &lt;pseudonym&gt; especially if we have few or only recent conns
14:24 &lt;jrandom&gt; pseudonym: the existing connections are "right" in that they can send and receive data
14:24 &lt;deer&gt; &lt;ugha2p&gt; pseudonym: We can be sure when we get new inbound connections, although those can be spoofed as well.
14:25 &lt;jrandom&gt; right, if we're talking about someone concerned with an active IP spoofing attack in addition to sybil...
14:25 &lt;jrandom&gt; well, that person can simply set their IP address ;)
14:25 &lt;deer&gt; &lt;ugha2p&gt; :)
14:26 &lt;deer&gt; &lt;pseudonym&gt; but what's the likelyhood that the operator will even know what's happening
14:26 &lt;deer&gt; &lt;pseudonym&gt; if we get a lot of mismatches there should be some active alert
14:27 &lt;deer&gt; &lt;pseudonym&gt; (this may be something to worry about in a later release, but since it came up...)
14:27 &lt;jrandom&gt; we can add an explicit message to the list of connection errors
14:27 &lt;jrandom&gt; the only real concern here is that we're trying to prevent a restricted route from being formed
14:27 &lt;jrandom&gt; (and the extreme of that being a full network partition)
14:30 &lt;jrandom&gt; thats about all i can see us working to deal with for now, at least until the 2.0 rev when we need to worry beyond the restricted route
14:30 &lt;jrandom&gt; ok, anyone else have anything wrt the new transport?
14:31 &lt;jrandom&gt; if not, moving on to 2) 0.4.1 status
14:31 &lt;jrandom&gt; all the "necessary" stuff is done, but theres still some debugging and minor updates to get in
14:32 &lt;jrandom&gt; current target is a thursday release, but we'll see what gets added or removed from the rev ;)
14:33 &lt;jrandom&gt; one thing that would be cool is if someone could download a jetty install, check out the jetty.xml config file, and could write up some docs on how to run a jetty instance (for an eepsite/etc) with what is shipped with i2p
14:33 &lt;deer&gt; &lt;ugha2p&gt; Does 0.4.1 include other updates than the new TCP transport?
14:33 &lt;jrandom&gt; not really ugha :)
14:34 &lt;deer&gt; &lt;pseudonym&gt; is it backward compatible?
14:34 &lt;jrandom&gt; (see: www.i2p.net/roadmap )
14:34 &lt;jrandom&gt; no, it is not backwards compatible
14:34 &lt;deer&gt; &lt;ugha2p&gt; :)
14:36 &lt;jrandom&gt; ok, thats all ive got to mention wrt 0.4.1.. anything else on that?
14:36 &lt;jrandom&gt; if not, we're on to ol' faithful: 3) ???
14:36 &lt;deer&gt; &lt;ugha2p&gt; *silence*
14:37 &lt;jrandom&gt; anyone have anything else (i2p related) they want to bring up?
14:37 &lt;jrandom&gt; we're already twice as long as last week's meeting ;)
14:37 &lt;deer&gt; &lt;ugha2p&gt; Well, I could mention that thanks to cervantes, my Wiki now has an outproxy to the real world, through http://ugha.ath.cx/
14:38 &lt;deer&gt; * pseudonym is a troublemaker
14:38 &lt;jrandom&gt; ooh right, v.cool
14:38 &lt;jrandom&gt; s/outproxy/inproxy/ :)
14:38  * jrandom sends the troublemaker to the corner
14:38 &lt;deer&gt; &lt;ugha2p&gt; Right, inproxy. :)
14:40 &lt;jrandom&gt; ok, if there's nothing else
14:40 &lt;deer&gt; &lt;pseudonym&gt; I think the new mail service from the postmaster is pretty cool
14:40 &lt;jrandom&gt; oh, definitely agreed
14:40 &lt;deer&gt; &lt;pseudonym&gt; er, postman
14:41 &lt;deer&gt; * ugha2p has yet to sign up.
14:41 &lt;deer&gt; &lt;baffled&gt; has anyone heard anything of stasher recently?
14:41 &lt;jrandom&gt; its nice that it works with both telnet and kmail:)
14:41 &lt;jrandom&gt; naw baffled, havent heard a peep
14:42 &lt;deer&gt; &lt;baffled&gt; I guess aum needs a boot to the head.
14:42 &lt;deer&gt; &lt;ugha2p&gt; I would probably write a page about EepMailAnonymity, but I don't know too much about SMTP/POP3/IMAP/other e-mail-related stuff.
14:42 &lt;jrandom&gt; not the head, the butt ;)
14:43 &lt;jrandom&gt; ugha: www.postman.i2p has a few pages about that
14:43 &lt;deer&gt; &lt;ugha2p&gt; Ah.
14:43 &lt;deer&gt; &lt;baffled&gt; they may be the same.
14:45 &lt;deer&gt; * ugha2p taps his fingers waiting for the baf.
14:45 &lt;jrandom&gt; sorry, nearly passed out here (loong day)
14:46 &lt;jrandom&gt; anything else?  if not, we've got the forum and the list
14:46 &lt;duck&gt; thanks to Mi-Go we have an updated i2ptunnel page
14:46 &lt;duck&gt; it is almost perfect
14:46 &lt;jrandom&gt; ooh nice
14:46 &lt;duck&gt; but if someone has some improvements, you know where to find me
14:47  * jrandom traceroutes
14:47  * jrandom winds up
14:47  * jrandom *baf*s the meeting closed
</div>
