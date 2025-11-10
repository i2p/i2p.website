---
title: "I2P Dev Meeting - August 30, 2005"
date: 2005-08-30
author: "+bla"
description: "I2P development meeting log for August 30, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, bla, gloin, jrandom, laberhorst, nickless_head, redzara, ZULU</p>

## Meeting Log

<div class="irc-log">
13:03 &lt;+bla&gt; Is there a meeting today?
13:04 &lt;jrandom&gt; 0) hi
13:04 &lt;jrandom&gt; 1) Net status
13:04 &lt;jrandom&gt; 2) floodfill netDb
13:04 &lt;jrandom&gt; 3) Syndie
13:04 &lt;jrandom&gt; 4) ???
13:04 &lt;jrandom&gt; 0) hi
13:04 &lt;+bla&gt; ;)
13:04  * jrandom waves
13:04 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2005-August/000871.html
13:04 &lt;jrandom&gt; (yeah, i'm a few minutes late ;)
13:05 &lt;jrandom&gt; anyway, jumping into 1) net status
13:06 &lt;jrandom&gt; restricted routes suck, and we finally have some data as to how common they are (boo hiss)
13:06 &lt;jrandom&gt; but stil, the net seems fairly healthy, if you ignore all the worried reports of "omg it says status: Unknown!" ;)
13:07 &lt;gloin&gt; hmm.. where should be the document root for the i2p  included webserver?
13:07 &lt;jrandom&gt; $i2pInstallDir/eepsite/docroot/
13:07 &lt;gloin&gt; i2p/eepsite/docroot ?
13:07 &lt;jrandom&gt; anyone have any questions/comments/concerns regarding the net status outside of whats posted in the status notes?
13:08 &lt;gloin&gt; found it. it seems that the webserver won't deliver index.html automatically.
13:08 &lt;+bla&gt; jrandom: I have been doing some tests to check which nodes are selected in tunnels.
13:09 &lt;+bla&gt; jrandom: Mainly, as I've now implemented node-localization in the RouterInfo struct, I can see graphically (country flags) were tunnel participants are located.
13:09 &lt;+bla&gt; I am in Europe (no secret), and most of my tunnel participants are in Europe
13:09 &lt;jrandom&gt; gloin: it should serve up the index.html (thats what renders "Welcome to your Eepsite")
13:10 &lt;jrandom&gt; ooh nice1 bla!
13:10 &lt;redzara&gt; as some people have reported some low perf with UDP, maybe we could had a little perfmeter like iperf in I2P ?
13:11 &lt;redzara&gt; s/had/add
13:11 &lt;jrandom&gt; bla: so thats not just on the profiles.jsp page, but also on tunnels.jsp?  v.cool... screenshots, screenshots!  :)
13:11 &lt;gloin&gt; jrandom: now it works. strange.
13:11 &lt;+bla&gt; jrandom: I'll post some screenshots, but I first have to black out my own router-ID in the screenshots ;)
13:11 &lt;jrandom&gt; redzara: hmm, a command line utility to let people check their link quality, or a monitor for SSU performance?
13:11 &lt;jrandom&gt; heh bla
13:12 &lt;jrandom&gt; odd gloin 
13:13 &lt;gloin&gt; jrandom: btw, since I updated my pppoe i2p seems to be more stable.
13:13 &lt;jrandom&gt; nice, what was the problem with your net connection?  firmware update?
13:14 &lt;gloin&gt; jrandom: I lost all peers. But the internet connection was ok, but every peer failed. 
13:16 &lt;jrandom&gt; right, but what did you update about your pppoe settings?
13:17 &lt;gloin&gt; jrandom: I mean the linux ppppoe deamon.
13:18 &lt;jrandom&gt; ah ok
13:18 &lt;jrandom&gt; ok, anyone else have anything for 1) net status, or shall we move on to 2) floodfill netdb?
13:18 &lt;+bla&gt; http://theland.i2p/parttunnels.jpg
13:19 &lt;+bla&gt; http://theland.i2p/servertunnels.jpg
13:21 &lt;+bar&gt; (umm.. inaccessible?)
13:21 &lt;jrandom&gt; yeah, i'm having trouble reaching it too
13:21 &lt;fox&gt; &lt;godmode0&gt; i use pppoe never be at problem i2p
13:22  * jrandom will try later though
13:22 &lt;+bla&gt; jrandom: Well.. There's new network problem just there ;)
13:22 &lt;jrandom&gt; hehe
13:22 &lt;jrandom&gt; bla: are you on -4 or an earlier build?
13:23 &lt;+bla&gt; jrandom: I'm on -4
13:23 &lt;jrandom&gt; hmm, ok cool
13:23 &lt;jrandom&gt; ok, anyway, we can dig through that later
13:24 &lt;jrandom&gt; (if you could send me the netDb stats from /oldstats.jsp, that'd be great :)
13:25 &lt;jrandom&gt; ok, moving on to 2) floodfill netdb
13:26 &lt;jrandom&gt; there's lots of info posted to my blog on this topic
13:26 &lt;jrandom&gt; we've begun deploying a first pass, though there's still some work to be done
13:26 &lt;jrandom&gt; does anyone have any questions/comments/concerns on the plan?
13:27 &lt;+bla&gt; jrandom: Will the floodfill scale as log(N) (N=number of peers in the net), or linearly?
13:27 &lt;jrandom&gt; linearly with M (M= number of peers participating in the floodfill netdb)
13:28 &lt;jrandom&gt; well, M may be small enough that N is the dominant term
13:29 &lt;jrandom&gt; (in which case it'll be linearly with N)
13:29 &lt;jrandom&gt; which is not great, but until we have&gt; 10K eepsites, it doesnt matter
13:30 &lt;jrandom&gt; once we do, then we can go into more advanced algorithms for sharing the load between the floodfill participants
13:31 &lt;jrandom&gt; (note thats 10k eepsites, not users, since we don't really need to publish client leaseSets in the netdb)
13:32 &lt;+bla&gt; jrandom: Is there a reason why we still do publish the client destinations in the netDb?
13:32 &lt;+bla&gt; jrandom: Or, for that matter, why we still show off who our fast peers are in the netDb?
13:33 &lt;+bla&gt; jrandom: Removing both would slash the netDb data by a big factor
13:33 &lt;jrandom&gt; bla: to the former, no.  to the later, for me to debug (though i havent looked at that particular field recently)
13:33 &lt;jrandom&gt; aye, worth trying, perhaps in -5
13:36 &lt;jrandom&gt; ok coo', well, we'll see and hopefully get -5 out in the next few days
13:37 &lt;jrandom&gt; (maybe tomorrow)
13:37 &lt;jrandom&gt; ok, if there's nothing else on 2) floodfill netdb, lets move on to 3) syndie
13:38 &lt;jrandom&gt; i posted a bunch of info in the mail and on my blog, so rather than rehash them, does anyone have any questions / comments / concerns?
13:40  * jrandom really digs the remote syndication functionality, though its far from what we're hoping for with feedspace integration
13:41 &lt;jrandom&gt; (i havent been bothered to do freenet posting integration, though it would be quite easy to fire up a CLI and post all the entries in)
13:42 &lt;jrandom&gt; ok, if there's nothing else on 3) syndie, lets open 'er up to 4) ???
13:42 &lt;jrandom&gt; anyone have anything else i2p related to bring up?
13:42 &lt;redzara&gt; sure, where is the doc ;)
13:43 &lt;laberhorst&gt; just that my node under 0.6.x sonsumes up to 100% cpu load, but have to crosscheck it with linux on that line here
13:43 &lt;+nickless_head&gt; I think the i2pProxy.pac script should be in the jetty web folder by default.
13:43 &lt;jrandom&gt; nickless_head: i dont recommend i2pproxy.pac, as its a huge security risk
13:44 &lt;redzara&gt; 2 - could be have the latest build of jetty included in I2P ?
13:44 &lt;jrandom&gt; we've got 5.2.1 in i2p right now
13:44 &lt;jrandom&gt; er, 5.1.2
13:44 &lt;+nickless_head&gt; jrandom: it's the only thing available for separating between eepsites and websites in one browser without having to switch by hand afaik
13:45 &lt;jrandom&gt; i use switchproxy
13:45 &lt;jrandom&gt; (and i dont switch to non-anonymous browsing)
13:45 &lt;jrandom&gt; ((squid.i2p is fast enough for me))
13:45 &lt;+nickless_head&gt; Think of the slashdotters! :p
13:46 &lt;jrandom&gt; as i've said before, i have reservations about the viability of eepsites.  the security risks are tremendous
13:46 &lt;jrandom&gt; but, for those who don't care about those risks, perhaps an i2pproxy.pac makes sense.
13:47 &lt;+bla&gt; I strongly think that something that isn't secure by _default_, shouldn't be in I2P, as to not give new users a false sense of secutiry
13:48 &lt;jrandom&gt; agreed (though we do push i2pproxy.pac, we just dont tell people about it until we scare 'em enough ;)
13:49 &lt;+nickless_head&gt; I somehow can't believe that within the configuration of Mozilla there isn't a way to make sites only access resources from the same domain .. 
13:50 &lt;redzara&gt; sorry but IRC connection lost :( about jetty there is a fix about common logging and maybe this help me running my mvnforum in the same instance of I2P
13:50 &lt;redzara&gt; Jetty-5.1.5rc1 - 23 August 2005
13:52 &lt;jrandom&gt; ah cool, whats the problem exactly redzara?
13:52 &lt;jrandom&gt; nickless_head: if you find a way, let us know
13:52 &lt;redzara&gt; or maybe i could even only build my own I2P with the latest version of jetty
13:52 &lt;jrandom&gt; redzara: that you certainly can do - just drop in the jetty jar files into your i2p lib directory
13:53 &lt;redzara&gt; jrandom : everythime i try to start mvnforum in I2P, jetty failed to find apache common logging
13:53 &lt;+nickless_head&gt; Oh! I just noticed that the default i2pproxy.pac uses a mode which allows sites to switch proxy'ing to i2p on and off at runtime, which is protected by the TOTALLY SECURE AND UNBREAKABLE &lt;/sarcasm&gt; default password "passw0rd". Please, someone who knows about cvs change this.
13:54 &lt;jrandom&gt; redzara: thats in commons-logging.jar and commons-el.jar iirc, which should be in your lib dir and in your wrapper.config's classpath
13:54 &lt;jrandom&gt; nickless_head: yet another reason why i dont recommend anyone use it ;)
13:55 &lt;redzara&gt; yes i know, i'm not so n00b :)) i've to dig into again with this new version of jetty
13:56 &lt;jrandom&gt; cool, keep us updated
13:56 &lt;redzara&gt; np
13:57 &lt;fox&gt; * mihi guesses most i2p users will reveal their "real ip" to a java applet  anyway :)
13:57 &lt;fox&gt; &lt;mihi&gt; try http://www.stilllistener.com/checkpoint1/Java/ (and scroll down)
13:58  * jrandom sees lots of blank fields ;)
13:59 &lt;+bla&gt; fox: All one exposes is the relation between an IP and a particular client destination, where the client destination will change at every router restart.
13:59 &lt;jrandom&gt; bla: unless the user is on some site like e.g. http://i_have_illegal_stuff.i2p/
14:00 &lt;jrandom&gt; (exposing the clients IP "just once" is fatal enough ;)
14:00 &lt;+bla&gt; jrandom: Yes. 
14:00 &lt;+bla&gt; But then again, if you're serious about anonymous browsing, you'll use temporary HTTP proxies, and disable all things java, and plugins, and cookies, entirely
14:01 &lt;jrandom&gt; or use syndie :)
14:02 &lt;ZULU&gt; sorry for interruption,is duck.ip down ?
14:02 &lt;+bla&gt; jrandom: Is it time yet for general questions?
14:02 &lt;jrandom&gt; aye, we're on 4) ???
14:02 &lt;jrandom&gt; ZULU: yeah, duck is offline for the time being
14:03 &lt;+bla&gt; jrandom: I've edited the java-files that help profiles.jsp and tunnels.jsp generate the country-flags
14:04 &lt;+bla&gt; jrandom: However, where do I place images that I can actually LINK to, and that will work, on my local router (_not_ my eepsite)?
14:06 &lt;jrandom&gt; we need a "get.jsp?name" that dumps the contents of ./docs/'name' to the browser
14:06 &lt;jrandom&gt; (aka you need to have it in the .war right now, but with a tiny .jsp file, you could dump 'em in docs)
14:06 &lt;+bla&gt; jrandom: Ah, ok, so it wasn't my fault ;)
14:06 &lt;jrandom&gt; heh nope, blame me :)
14:09 &lt;jrandom&gt; ok, if there's nothing else for the meeting
14:09  * jrandom winds up
14:10  * jrandom *baf*s the meeting closed
</div>
