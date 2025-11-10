---
title: "I2P Dev Meeting - August 23, 2005"
date: 2005-08-23
author: "jrandom"
description: "I2P development meeting log for August 23, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> arcturus, ardvark, cervantes, gott, jrandom, lucky, modulus, susi23\_</p>

## Meeting Log

<div class="irc-log">
12:01 &lt;jrandom&gt; 0) hi
12:01 &lt;jrandom&gt; 1) 0.6.0.3 status
12:01 &lt;jrandom&gt; 2) IRC status
12:01 &lt;jrandom&gt; 3) susibt
12:01 &lt;jrandom&gt; 4) Syndie
12:01 &lt;jrandom&gt; 5) ???
12:01 &lt;jrandom&gt; 0) hi
12:01  * jrandom waves
12:01 &lt;lucky&gt; hi
12:02 &lt;jrandom&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2005-August/000857.html
12:02 &lt;lucky&gt; hihihihi
12:02 &lt;jrandom&gt; hi lucky 
12:02 &lt;jrandom&gt; ok, jumping into 1) 0.6.0.3 status
12:02 &lt;jrandom&gt; i think the biggest things worth mentioning wrt 0.6.0.3 are in the status notes, but beyond that, anyone have anything to bring up?
12:04 &lt;gott&gt; What's the deal with 'Unknown' ?
12:04 &lt;jrandom&gt; i'm not sure whether the ssu cwin improvements will come in 0.6.0.4 or will wait until 0.6.1 when we have better peer / configuration
12:04 &lt;jrandom&gt; gott: there are two paragraphs in the email related to that - do you have any specific questions beyond those?
12:05 &lt;jrandom&gt; or is there some point i could clarify?
12:05 &lt;gott&gt; No, I just haven't read the bloody email.
12:05 &lt;jrandom&gt; heh
12:05 &lt;jrandom&gt; well, scroll up five lines and read the bloody email ;)
12:06 &lt;jrandom&gt; ok, anyone else have any questions on 0.6.0.3?
12:07 &lt;jrandom&gt; if not, moving on to 2) IRC status
12:07 &lt;modulus&gt; sorry guys, but need to leave. later all.
12:08 &lt;jrandom&gt; beyond whats in the mail, postman/cervantes/arcturus: y'all have anything you want to bring up?
12:08 &lt;jrandom&gt; l8r modulus
12:08 &lt;+arcturus&gt; on 1)?
12:08 &lt;+arcturus&gt; oh sorry
12:08 &lt;gott&gt; Hmm.
12:08 &lt;+arcturus&gt; 2) it is now
12:09 &lt;gott&gt; How much upstream bandwidth does IRC over i2p usually take at the moment ?
12:09 &lt;+arcturus&gt; netsplits are history
12:09 &lt;+arcturus&gt; gott: i coudln't say that without compromising my router's anonymity
12:09 &lt;gott&gt; No, no, no.
12:10 &lt;jrandom&gt; not sure, my router with squid.i2p/dev.i2p/cvs.i2p/www.cvs/syndiemedia.i2p plus my irc and eepproxy uses on average 10-20KBps
12:10 &lt;gott&gt; Does it require a commercial line ?
12:10 &lt;jrandom&gt; nice1 arcturus
12:10 &lt;gott&gt; jrandom: I mean to say, to host.
12:10 &lt;jrandom&gt; gott: to operate a server or a client?
12:10 &lt;jrandom&gt; ah
12:10 &lt;+arcturus&gt; gott: i couldn't say that without compromising my router's anonymity
12:10 &lt;gott&gt; server.
12:10  * jrandom knows not.  probably less when you have just one ircd
12:10 &lt;gott&gt; So are you running a modified unrealircd ?
12:11 &lt;jrandom&gt; say, add a factor of 1.3 to the client usage for a single server
12:11 &lt;+arcturus&gt; i'd like to also add that inter-server lag is steady and very very low
12:11 &lt;gott&gt; I assume you are, since there doesn't seem to be a VERSION command
12:11 &lt;+arcturus&gt; i disabled version
12:12 &lt;gott&gt; Are your modifications open-source ?
12:12 &lt;+arcturus&gt; maybe we're running unreal, maybe we aren't :)
12:12 &lt;gott&gt; You should put them up so others can start their own private networks.
12:12 &lt;+arcturus&gt; i can't tell you without compromising security
12:12 &lt;gott&gt; security through obscurity, sweet.
12:12 &lt;jrandom&gt; word arcturus.  i'm seeing something like 0-2s lag on average (at the moment, less than irssi's lag detector)
12:12 &lt;+arcturus&gt; no, it's only one layer of security
12:13 &lt;+arcturus&gt; and it only serves as a deterrent, no substitute for technical security measures
12:15 &lt;jrandom&gt; arcturus: how goes with vanguard?
12:15 &lt;+arcturus&gt; i haven't coded on it lately, other projects have been occupying me, but there's a constant, steady pressure i feel to get around to finishing it :)
12:16 &lt;jrandom&gt; heh coo'
12:16 &lt;+arcturus&gt; vanguard will be most effective against bots, the hashcash measure is a separate deal
12:16 &lt;+arcturus&gt; i'm concerned about hashcash now though
12:17 &lt;+arcturus&gt; with the latest attacks against sha-1
12:17 &lt;+arcturus&gt; it won't be long before there are tools available to the masses
12:17 &lt;+arcturus&gt; unfortunately the standard hashcash implementation is based entirely on sha-1
12:17 &lt;susi23_&gt; Unable to find a javac compiler; // com.sun.tools.javac.Main is not on the classpath. // Perhaps JAVA_HOME does not point to the JDK
12:18 &lt;@cervantes&gt; ah made it
12:18 &lt;susi23_&gt; any ideas about this? JAVA_HOME points definitely to the right dir, javac is in PATH and callable
12:18 &lt;+arcturus&gt; susi23_: we're in a meeting atm :)
12:18 &lt;jrandom&gt; susi23_: OOM?
12:18 &lt;susi23_&gt; meeting? though its 8pm?
12:18 &lt;jrandom&gt; (precompile your jsps rather than letting jetty/tomcat do it, its faster ;)
12:19 &lt;jrandom&gt; yeah we moved it susi23_ :)
12:19 &lt;susi23_&gt; didn't know, sorry
12:19 &lt;jrandom&gt; hehe np, glad you made it for the meeting, your agenda item is up next ;)
12:20  * susi23_ sits down and listens
12:20 &lt;+arcturus&gt; so while i don't expect immediate problems with hashcash, i think it's feasible sha-1 could be seriously compromised soon
12:21 &lt;jrandom&gt; arcturus: hashcash with md5 would probably be fine
12:21 &lt;jrandom&gt; its just a PoW
12:21 &lt;+arcturus&gt; if anyone knows of any hashcash implementations based on sha256 or higher please met me know
12:21 &lt;+arcturus&gt; well PoW is pointless if there's little P in it :)
12:21 &lt;jrandom&gt; the size of the hash only matters when your hashcash reaches the size of the hash
12:23 &lt;jrandom&gt; (but, yeah, running against a truncated sha256 or 512 or whirlpool or whatever would be neat)
12:23 &lt;+arcturus&gt; i guess we could go ahead with the current implementation, perhaps we can design it so that we can swap it out easily later when we need to
12:24 &lt;jrandom&gt; (DTSTTCPW)
12:25 &lt;+arcturus&gt; because we will eventually need to drop sha-1, i'm sure of it :) and if we can't be reasonably certain a token was generated properly there's no reason to even be using hashcash
12:25 &lt;jrandom&gt; (its only for a PoW to get a nym on irc, not to get access to fort knox ;)
12:26 &lt;@cervantes&gt; there's some talk on the hashcash mailing list about implementing sha256
12:26 &lt;+arcturus&gt; it's not for a nym, it's for entry to the server
12:26 &lt;+arcturus&gt; cervantes: cool i'll check that
12:27 &lt;+arcturus&gt; jrandom: and it's not just PoW, the hashcash is what gives us a method to uniquely identify clients on the network, akin to being able to identify by IP, so that we can ban with precision
12:28 &lt;jrandom&gt; certainly those are renewed over time though, right?
12:28 &lt;jrandom&gt; e.g. a new PoW cert every 6 months (or 6h, or whatever)
12:28 &lt;+arcturus&gt; if a user doen't have to do any work to get their ID, that nullifies our ability to ban them
12:29 &lt;+arcturus&gt; i don't know of any reason to expire them automatically, only expire them manually if they violate terms of service
12:29 &lt;+arcturus&gt; no need to make people do unnecessary work for new IDs
12:29 &lt;jrandom&gt; eh, its just a passive PoW, they can run one cycle every 6 hours to regenerate a new one
12:29 &lt;jrandom&gt; but perhaps DTSTTCPW
12:30 &lt;+arcturus&gt; any hashcash genereated must be used within 24 hours or it is invalid
12:32 &lt;@cervantes&gt; just to reiterate the new server irc.freshcoffee.i2p needs to be added into your i2ptunnel console
12:32 &lt;jrandom&gt; coo'.  ok, anything else for 2) irc2p?
12:33 &lt;@cervantes&gt; (http://forum.i2p/viewtopic.php?t=911
12:33 &lt;@cervantes&gt; )
12:33 &lt;@cervantes&gt; &lt;-- done
12:34 &lt;+arcturus&gt; i don't have anything else to bore you all with :)
12:34 &lt;jrandom&gt; hehe
12:34 &lt;jrandom&gt; ok, 3) susibt
12:34 &lt;ardvark&gt; um, when I add the new server to my tunnel, do I have to restart i2p?
12:34 &lt;jrandom&gt; susi23_: p1ng
12:35 &lt;@cervantes&gt; ardvark: just the tunnel
12:35 &lt;@cervantes&gt; (ircproxy tunnel)
12:35 &lt;ardvark&gt; oh ok, I just added and saved, so that is not enuff then
12:36 &lt;jrandom&gt; right, unfortunately you need to stop and start that proxy
12:36 &lt;susi23_&gt; well
12:36 &lt;ardvark&gt; but i'll miss the meeting then ;)
12:37 &lt;susi23_&gt; susibt is a webapp (like susimail) to drop into your routers VM
12:37 &lt;susi23_&gt; it acts as a web frontend for i2p-bt
12:38 &lt;susi23_&gt; so you can manage your seeds, up- and download files etc.
12:38 &lt;jrandom&gt; w00t
12:39 &lt;susi23_&gt; the prob is, you need to start a btdownloadheadless.py for each seed... so you get lot of python processes to your many java threads :)
12:39 &lt;+arcturus&gt; that will be addressed in ducktorrent *cough*
12:39 &lt;jrandom&gt; heh
12:39  * jrandom holds breath
12:40 &lt;susi23_&gt; it even supports restart of seeds after router restart
12:40 &lt;@cervantes&gt; nice
12:40 &lt;jrandom&gt; wikked
12:40 &lt;susi23_&gt; future plans are automatic build of torrents and ui improvement
12:41 &lt;susi23_&gt; if you want to try it out, I recommend a separate jetty instance
12:41 &lt;susi23_&gt; so you don't have to fiddle with your router :)
12:41 &lt;susi23_&gt; download and installation instructions on http://susi.i2p
12:42 &lt;susi23_&gt; thats all *ping back to jr*
12:42 &lt;jrandom&gt; w3wt, gracias susi
12:42 &lt;jrandom&gt; ok, anyone have any questions & comments on that, or shall we jump on over to 4) syndie?
12:44 &lt;jrandom&gt; ok regarding syndi, i've posted a bunch to the list about it over the last day or two, and there'll be lots more activity
12:45 &lt;jrandom&gt; the main demo site for syndie is http://syndiemedia.i2p / http://66.111.51.110:8000/, but of course people are encouraged to download it and install it locally
12:45 &lt;jrandom&gt; i dont have too much to add at the moment on that frnt. unless anyone has any questions?
12:46 &lt;gott&gt; Why is it called syndie ?
12:46 &lt;gott&gt; is it a reference to 'syndicate' ?
12:47 &lt;jrandom&gt; yeah, its a generic syndication frontend (+ security, authentication, and anonymity awareness)
12:48 &lt;jrandom&gt; ok, if there's nothing else on 4), lets jump on over to 5) ???
12:48 &lt;jrandom&gt; anyone have anythin i2p related to bring up for the meeting?
12:51 &lt;jrandom&gt; ok, if there's nothing else
12:51  * jrandom winds up
12:52  * jrandom *baf*s the meeting closed
</div>
