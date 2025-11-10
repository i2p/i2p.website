---
title: "I2P Dev Meeting - February 15, 2005"
date: 2005-02-15
author: "jrandom"
description: "I2P development meeting log for February 15, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bla\_, cervantes, cneal92\_, jrandom, polecat, postman, smeghead, ugha2p</p>

## Meeting Log

<div class="irc-log">
13:07 &lt;jrandom&gt; 0) hi
13:07 &lt;jrandom&gt; 1) Net status
13:07 &lt;jrandom&gt; 2) 0.5 status
13:07 &lt;jrandom&gt; 3) i2p-bt 0.1.7
13:07 &lt;jrandom&gt; 4) ???
13:07 &lt;jrandom&gt; 0) hi
13:07  * jrandom waves
13:07 &lt;+ugha2p&gt; jrandom: Is irc.duck.i2p also available on the testnet and linked to this network?
13:07 &lt;+ugha2p&gt; To this IRC network
13:07 &lt;jrandom&gt; weekly status notes posted @ http://dev.i2p.net/pipermail/i2p/2005-February/000575.html
13:07 &lt;ant&gt; &lt;Sonium_&gt; Bonjour, sa cette fois de la semaine encore,
13:07 &lt;jrandom&gt; no ugha2p 
13:08 &lt;ant&gt; &lt;Sonium_&gt; are you speaking french jrandom ?
13:08 &lt;jrandom&gt; heh, yeah, proof that babelfish has its limits ;)
13:08 &lt;jrandom&gt; lol, yeah, people were saying babelfish was turning out ok french before, but aparently not this time ;)
13:09 &lt;+ugha2p&gt; Hi fellow I2Pers.
13:09 &lt;ant&gt; &lt;fedo2p&gt; hi 
13:09 &lt;jrandom&gt; anyway, lets get this underway before we netsplit again 
13:09 &lt;jrandom&gt; 1) net status
13:09 &lt;jrandom&gt; see the email for an update
13:10 &lt;jrandom&gt; it seems that while irc has been pretty bumpy, as has some outproxy activity, bt has been doing pretty well
13:11 &lt;jrandom&gt; i don't really have much more to add beyond that though - anyone have any comments/questions/concerns?
13:12 &lt;ant&gt; &lt;Sonium_&gt; will 0.5 be released this friday?
13:12 &lt;jrandom&gt; heh good question, I suppose that can bring us on to 2) 0.5 status
13:12 &lt;jrandom&gt; yes, 0.5 will be released this friday
13:13 &lt;jrandom&gt; the test network is doing pretty well with the latest updates, but there's still some doc and minor cleanups left to do.  i'm also going to try to get the latest jetty in there, but we'll see
13:14 &lt;ant&gt; &lt;Sonium_&gt; a question for a native english speaker: what is the semantical difference between "it will be released" and "it is going to be released" ?
13:14 &lt;bla_&gt; Routing seems to be a little bit of a problem sometimes; in, say 5-10% of the cases, I have to reload a page, because the tunnel isn't working well
13:14 &lt;smeghead&gt; i'd like to request that everyone involved in bittorrent activity voluntarily cease until 0.5 is released on friday since the surge in bt traffic is ruining the rest of the network traffic, especially irc
13:15 &lt;jrandom&gt; Sonium: the later is more definitive, but same general idea
13:15 &lt;bla_&gt; smeghead: I'd agree, but 0.5 will not solve the load problem, will it?
13:15 &lt;smeghead&gt; eepsites are affected too, not just irc
13:16 &lt;ant&gt; &lt;Sonium_&gt; ok, than it missunderstood the usage till now
13:16 &lt;+ugha2p&gt; jrandom: Will it be doing a better job with interactive traffic?
13:16 &lt;jrandom&gt; 0.5 will change a lot of dynamics, and should be able to more cleanly handle load balancing, as we can now differentiate between the different causes of tunnel rejection
13:16 &lt;ant&gt; &lt;Sonium_&gt; I better would have listened up at school
13:16 &lt;jrandom&gt; ugha2p: yes, substantially
13:17 &lt;+ugha2p&gt; Ah, cool.
13:17 &lt;jrandom&gt; otoh, there will be an overal increase in bandwidth usage for many situations, though we will improve upon that later as things progress
13:18 &lt;smeghead&gt; and someone please let our new french speaking users know about this and ask them to hold off the bt stuff until friday
13:18 &lt;ant&gt; &lt;BS314159&gt; smeghead: it's three days. I'm sure you can come up with something else to do for three days
13:19  * jrandom could poke open an inproxy to spaetz's 0.5 ircd :)
13:20 &lt;jrandom&gt; perhaps a simpler solution would be to suggest bt users take advantage of the capacity to reduce network load by reducing their tunnel length
13:21 &lt;jrandom&gt; (both on the inbound tunnels, as configured with the bt command line, and on outbound tunnels, as configured on http://localhost:7657/configclients.jsp )
13:21 &lt;polecat&gt; Yeah, they don't need so much anonymity as obscurity.  It's us illegal alien ferrets that need the 2 hop thingy.
13:21 &lt;bla_&gt; jrandom: A possible solution, bt-0.1.8, wiith default tunnels length of 1, was mentioned before here on the channel. Duck, you here?
13:22 &lt;polecat&gt; Does i2p-bt use SAM, or does it use an i2ptunnel session?
13:23 &lt;jrandom&gt; hmm, otoh there are a whole set of new i2cp session options we'll want exposed in the i2p-bt, so i'll need to get in touch with duck about an updated release anyway 
13:23 &lt;jrandom&gt; polecat: SAM
13:23 &lt;smeghead&gt; BS314159: i'm a contributor to not only i2p codebase, but also i2p-bt, this bt traffic is preventing me from communicating with the other devs and impeding our efforts to improve everyone's experience, have some consideration please
13:23 &lt;smeghead&gt; BS314159: is it more important for you to torrent than it is for us to develop
13:23 &lt;smeghead&gt; ?
13:23 &lt;smeghead&gt; polecat: sam
13:23 &lt;cervantes&gt; make 0.1.8 shop all it's users to the mpaa and we'll all stick with 0.1.7
13:23 &lt;smeghead&gt; bla_: there probably won't be a 0.1.8, we've got 0.2.0 in cvs now, a new codebase based on bt 3.9.1
13:23 &lt;jrandom&gt; heh cervantes 
13:23 &lt;jrandom&gt; ooOOo nice
13:24 &lt;jrandom&gt; perhaps thats a good segue from 2) 0.5 status to 3) i2p-bt :)
13:24 &lt;jrandom&gt; smeghead/duck, how goes?  
13:25 &lt;ant&gt; &lt;Sonium_&gt; google knows 167 links to www.i2p.org
13:25 &lt;bla_&gt; jrandom: Maybe the upgrade timeline should be reiterated: take yer eepsite offline on Thursday evening (UTC), upgrade on Friday, and fire up the eepsite when a sufficient number of users have upgraded
13:26 &lt;ant&gt; &lt;Sonium_&gt; erm .net
13:26 &lt;smeghead&gt; all the bt mods in 0.1.7 have been integrated into the new 0.2.0 codebase
13:26 &lt;smeghead&gt; but we have to write a completely new sam interface, we can't use the one from 0.1.7
13:27 &lt;jrandom&gt; ah ok
13:27 &lt;smeghead&gt; if there's anyone with python socket experience that would like to help *cough*connelly
13:28 &lt;polecat&gt; All that's happening in SAM is the addition of stream level choking, right?
13:28 &lt;jrandom&gt; polecat: no protocol changes yet (to my knowledge), just porting
13:28 &lt;smeghead&gt; please get in touch with duck
13:28 &lt;ant&gt; &lt;MANCOM&gt; anything new on azneti2p?
13:28 &lt;smeghead&gt; the 0.2.0 client will handle multiple torrents all in one instance, you won't have to open multiple sessions anymore
13:29 &lt;jrandom&gt; (yay!)
13:29 &lt;polecat&gt; Reeeally?
13:29 &lt;smeghead&gt; and hopefully we can get it all working over a single sam session to further reduce network clutterage
13:29 &lt;bla_&gt; smeghead: Nice! Will you also port the text-onlu bttrackmany?
13:29 &lt;polecat&gt; Can it run in the background?
13:29 &lt;jrandom&gt; MANCOM: I haven't heard any news, and unfortunately haven't had time to audit the updates
13:29 &lt;polecat&gt; How much memory does it sit on?
13:29 &lt;smeghead&gt; bla_: yes i believe so
13:30 &lt;smeghead&gt; polecat: using btdownloadheadless.py it's a background process
13:31 &lt;polecat&gt; A single SAM session is possible: the peerwire and tracker protocol can be divined by both the client and server.
13:31 &lt;polecat&gt; smeghead: Yes, but what if I want to add a torrent to that process?
13:32 &lt;smeghead&gt; polecat: and it shouldn't use significantly more memory than the comparable number of 0.1.7 instances do
13:34 &lt;jrandom&gt; polecat: its a port of the mainline BT, it works just like the mainline BT.  someone could add new and better features, but lets start with a plain port first ;)
13:36 &lt;bla_&gt; (Connection rollercoaster ride, again...)
13:36 &lt;jrandom&gt; (this is why I lightly edit the meeting logs ;)
13:37 &lt;bla_&gt; jrandom: :)
13:37 &lt;jrandom&gt; wb
13:37 &lt;polecat&gt; smeghead: Yes, but what if I want to add a torrent to that process?
13:38 &lt;+ugha2p&gt; jrandom: No, it must be because you're censoring the netsplits.
13:38 &lt;jrandom&gt; polecat: its a port of the mainline BT, it works just like the mainline BT.  someone could add new and better features, but lets start with a plain port first ;)
13:38 &lt;jrandom&gt; hey, if i censor the netsplits, they dont happen!  
13:38  * jrandom buries head in sand
13:40 &lt;smeghead&gt; but i will use this opportunity to again ask bt users to hold off until friday please
13:41 &lt;bla_&gt; Right, if there's anyone who speaks French here, you don't have to say anything now, but please add a message to the effect of what smeghead asks to the French sections of forum.i2p ...
13:42 &lt;+polecat&gt; At any rate, I've missed the chance to say but, I was thinking of instead of a bt client in C++, I could just fix the mldonkey bittorrent plugin, and use that.
13:42 &lt;ant&gt; &lt;dm&gt; I speak french.
13:43 &lt;ant&gt; &lt;dm&gt; awww shit, I was supposed to not say anything.
13:43  * jrandom flings mud at dm
13:43 &lt;bla_&gt; dm: Could you add those messages?
13:43 &lt;smeghead&gt; there's nothing wrong with torrenting, but then again such a sudden increase in the number of i2p users wasn't expected and clearly the 0.4.x network can't handle it well
13:43 &lt;+polecat&gt; Unless someone else had an idea for something better I could waste my time on.  :/
13:44 &lt;ant&gt; &lt;dm&gt; don't have i2p on here, I'm afraid. I can translate english-&gt;french if u msg me what needs to be said.
13:44 &lt;jrandom&gt; polecat: perhaps help out getting the upcoming i2p-bt to work as you'd like?
13:44 &lt;jrandom&gt; dm: forum.i2p.net/
13:44 &lt;+polecat&gt; jrandom: I think the main bt isn't very useful myself, and is doomed to be a stopping block for multiple torrent system, unless they switch to a client/server UI.
13:44 &lt;+polecat&gt; Which I might add, mldonkey/mlnet has already done.
13:44 &lt;smeghead&gt; polecat: mldonkey is a horrid, horrid mess, please help on the i2p-bt project or the azureus-i2p project, they could use a hand
13:44 &lt;ant&gt; &lt;BS314159&gt; polecat: I think it's a waste of time to reimplement i2p-bt in a faster language, given the overhead in I2P
13:45 &lt;+polecat&gt; And I was planning to do with this stupid C++ client thingy o' mine.
13:45 &lt;jrandom&gt; polecat: so put on a gui, giving you the benefit of the underlying i2p-bt code
13:45 &lt;ant&gt; &lt;BS314159&gt; but having the use of the MLDonkey interface might be a very good thing
13:46 &lt;+polecat&gt; Azareus doesn't separate UI from file transfer I dun' think.  :/
13:46 &lt;smeghead&gt; polecat: you need to try bt 3.9.1, it's a multitorrent client now
13:48 &lt;+polecat&gt; Does it allow you to quit the UI without quitting swarming your files?
13:48 &lt;jrandom&gt; there are some features that it doesnt do well, that azureus does well, though there are also some environments where azureus isn't the right solution
13:48 &lt;ant&gt; &lt;jnymo&gt; has azureus released a compatable binary for the plugin?
13:48 &lt;jrandom&gt; polecat: no.  but adding that is trivial compared to writing a new bt client
13:48 &lt;jrandom&gt; jnymo: yes, they have a beta azneti2p
13:49 &lt;smeghead&gt; polecat: it could easily be modified to do so, very easily in fact
13:49 &lt;jrandom&gt; polecat: just modify the existing bt daemon to allow other processes (aka your new GUI) to tell it to do things
13:49 &lt;+polecat&gt; Well, perhaps...
13:49 &lt;+polecat&gt; You think so?
13:49 &lt;+polecat&gt; Maybe if I wrote a UI that was just an RPC socket protocol, and then... I'd have to write a whole client to grok that protocol...
13:50 &lt;smeghead&gt; polecat: you don't have to write a new ui, mod the existing i2p-bt 0.2.0 ui to do it, it's simple
13:50 &lt;+polecat&gt; Maybe we could separate the UI part of bt and the daemon part, and run those pieces as separate processes without having to rewrite too much code!
13:50 &lt;+polecat&gt; Okay.
13:50 &lt;+polecat&gt; I have one more question though...
13:51 &lt;smeghead&gt; polecat: don't reinvent the wheel because something lacks trivial features
13:51 &lt;smeghead&gt; polecat: you haven't looked at the i2p-bt codebase at all have you? the ui is completely separate
13:51 &lt;+polecat&gt; If bittorrent 3.9.1 is out, why are we using version 0.2.0 in i2p?  o.o 
13:51 &lt;jrandom&gt; heh
13:51 &lt;jrandom&gt; i2p-bt 0.2.0 == bt 3.9.1 :)
13:51 &lt;+polecat&gt; I looked at the codebase a while ago.  It was quite convoluted and obfuscated.
13:51 &lt;jrandom&gt; (i2p-bt 0.1.* == bt 3.4.something i think)
13:51 &lt;+polecat&gt; Oh, you have different versioning.
13:52 &lt;+polecat&gt; Is i2p-bt on CVS?
13:52 &lt;smeghead&gt; polecat: 0.2.0 is a new branch in cvs i created yesterday, it's i2p-bt, the official bt version it's based on is 3.9.1 which will be bittorrent 4.0 when it's out of beta
13:52 &lt;jrandom&gt; http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p-bt/
13:52 &lt;smeghead&gt; i2p-bt 0.1.7 is bt 3.4.2 based
13:52 &lt;+polecat&gt; Thanks.
13:52 &lt;+polecat&gt; Wait.
13:53 &lt;cervantes&gt; at which point we'll call it version 0.3.0 :P
13:53 &lt;+polecat&gt; I meant CVS, not the "ooh lookit the pretty website CVS"
13:53 &lt;jrandom&gt; cvs -d :pserver:anoncvs@cvs.i2p.net/cvsroot co i2p-bt
13:53 &lt;+polecat&gt; CVSROOT= is noticeably absent on those cvs-cgi thingies I've noticed.
13:53 &lt;jrandom&gt; or, if you have the CVS proxy locally, cvs -d :pserver:anoncvs@localhost/cvsroot co i2p-bt
13:54 &lt;smeghead&gt; polecat: convoluted? btdownloadgui.py is all the gui code, how can you get more cleanly separated than that?
13:54  * polecat whews, and doesn't feel a burning desire to bitch about CVS now.
13:54 &lt;ant&gt; &lt;dm&gt; ugh, that was painful, haven't written anything in french for years! http://forum.i2p.net/viewtopic.php?p=1238#1238
13:55 &lt;jrandom&gt; thanks dm
13:56 &lt;ant&gt; &lt;dm&gt; np
13:57 &lt;smeghead&gt; it probably says something obscene
13:58 &lt;ant&gt; &lt;dm&gt; hehehhe
13:58 &lt;+polecat&gt; Alright, so I have to write btdaemon.py, which is the gui - all gui stuff.  And also btdaemongui.py, which is the gui - all daemon stuff.
13:58 &lt;ant&gt; &lt;BS314159&gt; if it's sufficiently obscene, it may serve our purposes just fine
13:58 &lt;ant&gt; &lt;fedo2p&gt; good job dm ;)
13:58 &lt;jrandom&gt; heh
13:58 &lt;jrandom&gt; r0x0r polecat
13:59 &lt;+polecat&gt; Sigh, I hate to emerge wxwindows though, it's a big library I don't normally use.  Oh well.
13:59 &lt;smeghead&gt; polecat: 0.2.0 is gtk based, no more wxwidgets
13:59 &lt;jrandom&gt; ok, lots of bt work to do, perhaps we can discuss further on the list/forum/wiki/#i2p-bt as necessary?
13:59 &lt;+polecat&gt; If I'm gonna be hackin', I best get the toolz
14:00 &lt;+polecat&gt; Oh I forgot about that channel.  :)
14:00 &lt;smeghead&gt; polecat: get bittorrent 3.9.1 beta and read the docs
14:01 &lt;smeghead&gt; #i2p-bt, right
14:01 &lt;smeghead&gt; there's even people there
14:02 &lt;jrandom&gt; heh ok, lots of exciting bt stuff.  anything else for 3) i2p-bt, or shall we move on to 4) ???
14:03 &lt;jrandom&gt; ok, moving to 4) ???
14:03 &lt;jrandom&gt; anyone else have anything else to bring up for the meeting?
14:03 &lt;ant&gt; &lt;jnymo&gt; threshold crytography rules
14:04 &lt;cervantes&gt; ??? = http://forum.i2p/viewtopic.php?p=1237
14:04 &lt;ant&gt; &lt;BS314159&gt; proxies to the web are not cool. What about proxies to new versions of I2P, or other anonymnets?
14:04 &lt;ant&gt; &lt;BS314159&gt; and by not cool I mean not safe to run
14:04 &lt;ant&gt; &lt;jnymo&gt; they aren't run by everyone, BS
14:05 &lt;ant&gt; &lt;BS314159&gt; I know that
14:05 &lt;cervantes&gt; Forum member of the week is &lt;tadaa!&gt; jrandom
14:05 &lt;ant&gt; &lt;BS314159&gt; I'm thinking about upgrades
14:05 &lt;jrandom&gt; lol thanks cervantes 
14:06 &lt;ant&gt; &lt;BS314159&gt; Not now, but eventually, would it be possible to have a large number of routers act as inter-version proxies?
14:06 &lt;ant&gt; &lt;BS314159&gt; and would that remove the timing attack without downtime?
14:06 &lt;ant&gt; &lt;jnymo&gt; forced upgrades are necessary
14:07 &lt;ant&gt; &lt;BS314159&gt; I disagree
14:07 &lt;jrandom&gt; BS314159: I2NP over i2ptunnel over I2P would be, painful.  though perhaps one of the "outproxies" could point at some inproxy 
14:07 &lt;jrandom&gt; BS314159: while forced upgrades aren't generally necessary, they are here.  period.  we need it, because I didn't forsee all of the changes we need for 0.5
14:08 &lt;ant&gt; &lt;BS314159&gt; I'm not saying new versions should be backwards-compatible
14:08 &lt;cervantes&gt; jrandom: well lets be honest...you're the one that does 98% of the work ;-)
14:09 &lt;ant&gt; &lt;BS314159&gt; I'm just trying to come up with a way to allow non-nimble I2P users to upgrade without timing attacks or downtime
14:10 &lt;jrandom&gt; BS314159: can't be done for the 0.5 release.  later releases we can be careful.  but for this one, its a drop dead cutoff.  
14:10 &lt;ant&gt; &lt;jnymo&gt; automatic update may be better in the future
14:10 &lt;ant&gt; &lt;BS314159&gt; I'm speaking about the far future.
14:10 &lt;ant&gt; &lt;jnymo&gt; is auto-update too insecure?
14:10 &lt;jrandom&gt; cervantes: nah, only 95% of the infrastructure, but there's a lot more goin' on than just i2p/{core,router}/ :)
14:11 &lt;jrandom&gt; jnymo: 0 click update == insecure.  1 click == safe.
14:11 &lt;cervantes&gt; jrandom: yes it's begun to pickup over the last couple of months thankfully ;-)
14:11 &lt;ant&gt; &lt;jnymo&gt; and a line that says "you need to update.. countdown in * days"
14:12 &lt;jrandom&gt; aye, lots of people [http://www.i2p.net/team] have been doing kickass shit
14:13 &lt;jrandom&gt; BS314159: definitely lots we can do for later updates, perhaps we can discuss concrete impls as they approach :)
14:13 &lt;jrandom&gt; ok, anyone else have anything to bring up for the meeting?
14:13 &lt;ant&gt; &lt;MANCOM&gt; could we have some kind of autospeed feature (like with the azureus plugin that measures ping times) in i2p that adjusts the maximum (upload-)bandwidth?
14:14 &lt;ant&gt; &lt;MANCOM&gt; it would help keep bandwidth up and latency down
14:14 &lt;jrandom&gt; oh, interesting
14:14  * cervantes is working on a 1-2 click update feature for the i2p toolbar
14:14 &lt;cervantes&gt; although I'm having problems with hashing atm....so it's probably a few weeks away.
14:15 &lt;ant&gt; &lt;jnymo&gt; cervantes++
14:15 &lt;jrandom&gt; MANCOM: if you could doc up how it'd work and look, and post that on the forum, that'd be great.  if its simple enough, might even make it into 0.5
14:15 &lt;cervantes&gt; in which time a dozen people will come up with a glut of better solutions
14:16 &lt;jrandom&gt; heh
14:16 &lt;cneal92_&gt; :D
14:17 &lt;ant&gt; &lt;MANCOM&gt; well, i'll try
14:17 &lt;ant&gt; &lt;cervantes&gt; but it already detects when there's a new release out, and can point you at the relevant download link...
14:17 &lt;ant&gt; &lt;cervantes&gt; which I may roll with initially
14:18 &lt;jrandom&gt; cool cervantes
14:18 &lt;jrandom&gt; thanks MANCOM
14:18 &lt;ant&gt; &lt;jnymo&gt; you could just put the "graceful restart" button to upgrade, after the update is already in the directory
14:19 &lt;ant&gt; &lt;jnymo&gt; or call it "upgrade"
14:19 &lt;ant&gt; &lt;jnymo&gt; and put the restart function in there
14:19 &lt;ant&gt; &lt;jnymo&gt; though i'm probably stating the obvious
14:19 &lt;jrandom&gt; right, we need perhaps a dozen lines of code to fetch http://dev.i2p/i2p/i2pupdate.zip, verify it, then restart
14:20 &lt;jrandom&gt; ok, anyone else have anything to bring up for the meeting?
14:20 &lt;ant&gt; &lt;cervantes&gt; well I can already get the toolbar to download an update into the i2p folder AND trigger a graceful restart...but so far I haven't been able to get it verify the download's integrity
14:21 &lt;jrandom&gt; cervantes: ah, that part should be easy - at a later date, we'll have the update itself be self-verifying
14:21 &lt;jrandom&gt; (aka signed, verified by the router before installation)
14:21 &lt;ant&gt; &lt;cervantes&gt; jrandom: that would be cool.
14:21 &lt;ant&gt; &lt;jnymo&gt; ooh
14:22 &lt;ant&gt; &lt;cervantes&gt; perhaps it will be enough then that I trigger the download and then pop a "do you wish to restart" yes/no requester
14:22 &lt;ant&gt; &lt;cervantes&gt; so someone can verify manually if desired
14:23 &lt;ant&gt; &lt;cervantes&gt; (it already displays what the sha1 _should_ be)
14:23 &lt;jrandom&gt; hehe
14:23 &lt;ant&gt; &lt;jnymo&gt; how bout, "click here to autodownload on availability"
14:25 &lt;cervantes&gt; I'd rather avoid auto downloads
14:25 &lt;ant&gt; &lt;jnymo&gt; hmf.. microsoft does it ;)
14:26 &lt;cervantes&gt; but by all means alert the user that a download exists and offer a "download now" button
14:26 &lt;jrandom&gt; right, 1 click at the least.  we can automatically /notify/ on update availability, but autoinstall is not ok
14:26 &lt;jrandom&gt; (er, what cervantes said)
14:27 &lt;ant&gt; &lt;jnymo&gt; now, how do 10000 people update? how bout integrating i2p-bt at one point?
14:27 &lt;jrandom&gt; yes, and flying ponies
14:28 &lt;ant&gt; &lt;jnymo&gt; good enough for me
14:29 &lt;jrandom&gt; ok cool... if there's nothing else...
14:29 &lt;+postman&gt; damn missed the meeting :/
14:29  * cervantes gets back to coding his vapourware
14:29 &lt;jrandom&gt; heh you're at the buzzer, in case there's something you want to bring up postman :)
14:30 &lt;+postman&gt; no thanks
14:30 &lt;+polecat&gt; Microsoft?  =)  I have gentoo doing it.
14:30  * jrandom winds up
14:30 &lt;+postman&gt; ooops
14:30  * jrandom *baf*s the meeting closed
</div>
