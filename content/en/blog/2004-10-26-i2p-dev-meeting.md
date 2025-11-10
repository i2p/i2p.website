---
title: "I2P Dev Meeting - October 26, 2004"
date: 2004-10-26
author: "jrandom"
description: "I2P development meeting log for October 26, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> deer, jrandom, lucky, modulus</p>

## Meeting Log

<div class="irc-log">
14:04 &lt;jrandom&gt; 0) hi
14:04 &lt;jrandom&gt; 1) Net status
14:04 &lt;jrandom&gt; 2) Streaming lib
14:04 &lt;jrandom&gt; 3) mail.i2p progress
14:05 &lt;jrandom&gt; 4) ???
14:05 &lt;jrandom&gt; 0) hi
14:05  * jrandom waves
14:05 &lt;jrandom&gt; weekly status notes posted to http://dev.i2p.net/pipermail/i2p/2004-October/000474.html
14:06  * jrandom will let y'all read ahead (damn you, read ahead!)
14:06 &lt;jrandom&gt; jumping in to 1) net status
14:07 &lt;jrandom&gt; i guess the email covers what i wanted to mention. nice fix wrt resume duck, and thanks for reporting it ardvark and ragnarok!
14:07 &lt;jrandom&gt; does anyone have anything they want to bring up about the network status?
14:08 &lt;modulus&gt; it rules.
14:08 &lt;deer&gt; &lt;postman&gt; hi
14:08 &lt;jrandom&gt; w3wt
14:09 &lt;jrandom&gt; there is something funky w/ lag going on lately though, but it seems to be the same as what we discussed last week
14:09 &lt;jrandom&gt; (especially since i haven't done any work on the core since then)
14:09 &lt;deer&gt; &lt;clayboy&gt; i think everybody agrees that it has been stable and usable.
14:09 &lt;deer&gt; &lt;clayboy&gt; i miss my 10-16 hours connected time on irc though, not important
14:10 &lt;deer&gt; &lt;jrandom2p&gt; i'm on for 20h here
14:10 &lt;deer&gt; &lt;jrandom2p&gt; but yeah, it varies (which hopefully agenda item 2) will help with)
14:10 &lt;deer&gt; &lt;clayboy&gt; i can hardly get&gt; 2h, but i always reconnect in an instant, so it's still usable
14:11 &lt;jrandom&gt; cool
14:11 &lt;jrandom&gt; still not good enough, but sufficient
14:11 &lt;jrandom&gt; (for the time being)
14:11 &lt;deer&gt; &lt;clayboy&gt; agreed
14:12 &lt;jrandom&gt; ok, anyone have anything else, or shall we move on to 2) streaming lib?
14:13 &lt;jrandom&gt; [consider us moved]
14:13 &lt;jrandom&gt; the email gives a rundown of how the progress is coming
14:14 &lt;jrandom&gt; the message sequences are 'correct' in most cases (matching the ones discussed before)
14:14 &lt;jrandom&gt; e.g. short request/response gets the requestee a response in a single round trip
14:15 &lt;jrandom&gt; i'm working on the profile=bulk right now, going through the sliding windows under lag and failure conditions
14:15 &lt;jrandom&gt; still some things to clean up, and nothing ready for use, but its progress
14:16 &lt;deer&gt; &lt;clayboy&gt; so is 0.4.2 with streaming lib en route for october? it seems like an unnecessary rush.
14:16 &lt;jrandom&gt; i dont think we'll have the streaming lib ready for final deployment by next week, no
14:17 &lt;jrandom&gt; so there'll be some schedule slippage, i'm not sure to what extent yet
14:17 &lt;deer&gt; &lt;duck&gt; any test classes we can run for kicks?
14:18 &lt;jrandom&gt; i havent committed the build.xml file yet to keep people from using it ;)  but i'll commit what i've got later tonight, and you can try out http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/apps/streaming/java/test/net/i2p/client/streaming/StreamSinkTest.java?rev=1.1&content-type=text/x-cvsweb-markup
14:19 &lt;deer&gt; &lt;duck&gt; h0t
14:19 &lt;jrandom&gt; one thing is that this new streaming lib doesn't use the old mode=guaranteed anymore since it has its own ACK/NACK setup
14:20 &lt;jrandom&gt; that means that after the lib works perfectly, there's still going to be some work to be done in the router itself, as the client sending tasks are designed for 'guaranteed' delivery, bundling a roundtrip message in the garlic to confirm session tag delivery
14:21 &lt;jrandom&gt; we don't actually have to fix that right away though - the bandwidth usage on that DeliveryStatusMessage is... trivial
14:21 &lt;jrandom&gt; but we'll want to sooner rather than later
14:22 &lt;jrandom&gt; ok, thats all i've got to say on that
14:22 &lt;jrandom&gt; anyone have anything to bring up wrt the streaming lib?
14:23 &lt;jrandom&gt; if not, 3) mail.i2p progress
14:23 &lt;jrandom&gt; postman, you 'round?
14:23 &lt;deer&gt; &lt;postman&gt; ya
14:24 &lt;jrandom&gt; any update for us, or shall we wait until there's more news?
14:24 &lt;deer&gt; &lt;postman&gt; ok
14:24 &lt;deer&gt; &lt;postman&gt; shall i?
14:24 &lt;jrandom&gt; the mic is yours
14:24 &lt;deer&gt; * gott awakens.
14:24 &lt;deer&gt; &lt;postman&gt; 1.) the in/out proxy facility is being installed/tested atm 
14:25 &lt;deer&gt; &lt;postman&gt; 2.) within the next 10 days we'll have a gateway service from and to the internet for emails
14:25 &lt;modulus&gt; cool!
14:25 &lt;jrandom&gt; cool^2!
14:25 &lt;deer&gt; &lt;clayboy&gt; indeed
14:25 &lt;deer&gt; &lt;postman&gt; 3.) the implementation will follow the ideas/concepts of the ideas.html document on my websote
14:25 &lt;deer&gt; &lt;gott&gt; bravo !
14:26 &lt;deer&gt; &lt;postman&gt; means: hashcash/recipient based quotas and all the fancy stuff
14:26 &lt;deer&gt; &lt;postman&gt; the service should not be abused by its fellow anonymous users
14:26 &lt;deer&gt; &lt;postman&gt; :)
14:26 &lt;deer&gt; &lt;postman&gt; well there'e another point
14:26 &lt;deer&gt; &lt;postman&gt; the question for webmail interfaces
14:26 &lt;deer&gt; &lt;postman&gt; right now i don't want to host itz on my servers
14:27 &lt;deer&gt; &lt;postman&gt; since i don't know about potential security problems
14:27 &lt;deer&gt; &lt;postman&gt; the system that runs now is verified by me - i know the source and the security risks
14:28 &lt;deer&gt; &lt;postman&gt; adding php and dynamic stuff and a webmail application FOR ALL users makes it much more difficult 
14:28 &lt;deer&gt; &lt;postman&gt; the idea ( thanks jr) is:
14:28 &lt;deer&gt; &lt;postman&gt; what if the user got his own webmail interface installed as aonthr optional jetty or whatever instance?
14:29 &lt;modulus&gt; like a pop3 -&gt; webmail thing?
14:29 &lt;jrandom&gt; 'zactly
14:29 &lt;deer&gt; &lt;postman&gt; and this local webmail application uses the postman.i2p tunnels to do smtp and pop3
14:29 &lt;modulus&gt; sounds good.
14:29 &lt;deer&gt; &lt;postman&gt; but i need help in evaluating
14:30 &lt;deer&gt; &lt;postman&gt; right now i am quite busy with real life stuff and the in/out proxies
14:30 &lt;jrandom&gt; (eww, real life!)
14:30 &lt;deer&gt; &lt;postman&gt; and i got a peanut sized brain - so i am not good in java at all
14:31 &lt;deer&gt; &lt;postman&gt; i need sbdy helping how this can be done as a local/optional service 
14:31 &lt;modulus&gt; may there be something that does this already on tcp? if so it could be used.
14:31 &lt;deer&gt; &lt;DrWoo&gt; postman: I doubt it's peanut sized, I think it takes walnut sized just to breath ;)
14:32 &lt;jrandom&gt; after a quick glance through hotscripts, i saw one that did pop3, though i dont know if it did authenticated smtp
14:32 &lt;deer&gt; &lt;postman&gt; modulus: i assume there's something in the wild that can be used / adapted - it would be sexy to let it run in an own jetty instance
14:32 &lt;jrandom&gt; i'm sure there is something out there, we just need an adventurous soul to go find it :)
14:32 &lt;deer&gt; &lt;postman&gt; jrandom2p: this can be hacked quite easily i think
14:33 &lt;jrandom&gt; exactly - in an ideal world, someone can just grab a mywebmail.war and save it to the webapps/ directory and jump into http://localhost:7657/mywebmail/
14:33 &lt;deer&gt; &lt;postman&gt; well, i leave this issue to you to think about it :)
14:33 &lt;modulus&gt; even if it's a stand-alone app, it should be fine, with i2ptunel
14:33 &lt;jrandom&gt; right modulus 
14:33 &lt;deer&gt; &lt;postman&gt; yep :)
14:34 &lt;jrandom&gt; and local&gt;&gt; remote, as the local side can do things like access your GPG keyrings or whatever
14:34 &lt;deer&gt; &lt;postman&gt; i will do anything thats needed to support such a system on the server side
14:34 &lt;modulus&gt; which hopefully would be very little.
14:36 &lt;deer&gt; &lt;postman&gt; of course there will be an official announcement as soon as internet access is available - so stay tuned - maybe there will be some progress on the webmail idea as well
14:36 &lt;deer&gt; &lt;postman&gt; so much for my department
14:36 &lt;deer&gt; * postman sits down again and sips on his coffee
14:36 &lt;modulus&gt; could you do something about filtering anon-revealing data?
14:36 &lt;jrandom&gt; kickass, thanks postman!  sounds exciting
14:36 &lt;modulus&gt; some MUAs are very misbehaved in this way.
14:37 &lt;deer&gt; &lt;postman&gt; modules: please look at the webpage - there is a multipage sermon about that
14:37 &lt;jrandom&gt; :)
14:37 &lt;modulus&gt; ok
14:37 &lt;jrandom&gt; http://www.postman.i2p/sec.html to start
14:37 &lt;modulus&gt; i read that, i just thought maybe some fields could be filtered.
14:37 &lt;modulus&gt; maybe i trust postman but not other ppl.
14:38 &lt;deer&gt; &lt;postman&gt; modulus: They ARE filtred
14:38 &lt;modulus&gt; ok, last time i treid it they weren't.
14:38 &lt;modulus&gt; sorry about that.
14:38 &lt;deer&gt; &lt;postman&gt; modulus: sec2.html describes WHAT headerlines are filtered or changed
14:38 &lt;deer&gt; &lt;postman&gt; modulus: what headerlines are you refrring to?
14:38 &lt;modulus&gt; from domain (IP) kind of thing
14:39 &lt;jrandom&gt; it would be good if a local webmail script did the filtering locally
14:39 &lt;jrandom&gt; (in addition to any filtering done @ smtp.postman.i2p)
14:39 &lt;deer&gt; &lt;postman&gt; modulus: lets talk about that in pm, ok? :)
14:40 &lt;deer&gt; &lt;postman&gt; jrandom2p: of course - i am happy about every client doing its homework
14:40 &lt;modulus&gt; sure, sorry.
14:41 &lt;jrandom&gt; ok, do we have anything else for mail.i2p discussions?
14:41 &lt;jrandom&gt; if not, 4) ???
14:41 &lt;deer&gt; * duck has something for #4
14:42 &lt;jrandom&gt; sup duck?
14:42 &lt;deer&gt; &lt;duck&gt; the HD of home.duck.i2p blew up
14:42 &lt;jrandom&gt; (d'oh)
14:42 &lt;deer&gt; &lt;duck&gt; luckily the hosting accounts were not really used, except for alexandria
14:42 &lt;deer&gt; &lt;duck&gt; did anybody here leach all the ebooks? :)
14:43 &lt;deer&gt; &lt;duck&gt; if so, I got some missing so msg me please
14:43 &lt;jrandom&gt; actually, i think thetower did
14:43 &lt;deer&gt; &lt;duck&gt; I know that hypercubus also has them
14:43 &lt;deer&gt; &lt;postman&gt; damn
14:43 &lt;jrandom&gt; i saw a mirror on his site a while back
14:43 &lt;deer&gt; &lt;postman&gt; :/
14:43 &lt;deer&gt; &lt;duck&gt; cool
14:43 &lt;jrandom&gt; i dont know if it has everything though, or how up to date it was
14:43 &lt;deer&gt; &lt;duck&gt; alexandria is now on http://duck.i2p/alexandria/
14:44 &lt;deer&gt; &lt;duck&gt; and I am going back to being ashamed
14:44 &lt;deer&gt; &lt;duck&gt; .
14:44 &lt;jrandom&gt; no need to be ashamed, you've provided a kickass free service!
14:45 &lt;jrandom&gt; perhaps now is the chance for some geocities.i2p site ;)
14:46 &lt;deer&gt; &lt;duck&gt; oh, I made a yodel webfrontend @ http://duck.i2p/yodel/
14:46 &lt;jrandom&gt; oh, one thing i didn't have in the agenda is BT related stuff.  i know dinoman is doing some hacking on that - perhaps he wants to mention something?
14:46 &lt;jrandom&gt; ah nice
14:48  * jrandom notes that thetower's alexandria mirror link 404s
14:48 &lt;deer&gt; &lt;gott&gt; I have something to suggest.
14:48 &lt;jrandom&gt; sup gott?
14:48 &lt;deer&gt; &lt;gott&gt; I think it would be a nice feature for 0.4.2 to add a link to one of the sitelists on pages such as thetower's, baffled or mine.
14:49 &lt;jrandom&gt; thats a good idea
14:49 &lt;jrandom&gt; perhaps all three
14:49 &lt;deer&gt; &lt;gott&gt; This is to (a) keep a list of active eepsites and (b) form an index for i2p similar to FIND / Dolphin
14:49 &lt;jrandom&gt; yours is nice w/ the links to the eepsites too
14:49 &lt;deer&gt; &lt;gott&gt; the one located at http://gott.i2p/sites.html is being kept up-to-date 
14:49 &lt;deer&gt; &lt;gott&gt; and the script is run every day
14:49 &lt;deer&gt; &lt;gott&gt; I can add optional descriptions to the links ( thanx to baffled's script )
14:50 &lt;deer&gt; &lt;gott&gt; which would make it an index
14:50 &lt;jrandom&gt; perhaps it'd be neat to have a "recently added" or "recently removed" marker too?
14:50 &lt;jrandom&gt; word
14:51 &lt;deer&gt; &lt;gott&gt; quite good.
14:51 &lt;deer&gt; &lt;gott&gt; that's all I had to say for now.
14:51 &lt;deer&gt; &lt;gott&gt; oh, another thing
14:51 &lt;deer&gt; &lt;gott&gt; snipsnap works well under i2p
14:52 &lt;deer&gt; &lt;gott&gt; so we might see kuro5hin-style eepsites being brought up sometime a la SCUM
14:52 &lt;jrandom&gt; kickass
14:52 &lt;deer&gt; &lt;gott&gt; *except more devious a la SCUM
14:52 &lt;jrandom&gt; a howto for setting that up would be great
14:52 &lt;deer&gt; &lt;gott&gt; you put the .war in webapps
14:52 &lt;deer&gt; &lt;gott&gt; it's pretty straightforward ;-)
14:53 &lt;deer&gt; &lt;polecat&gt; snipsnap...SCUM...?
14:53 &lt;jrandom&gt; its really that easy?  booyeah!
14:53 &lt;jrandom&gt; polecat - http://snipsnap.org/space/start
14:53 &lt;deer&gt; &lt;gott&gt; I have finished my discourse.
14:53 &lt;deer&gt; * gott retires.
14:53 &lt;jrandom&gt; thanks gott
14:54 &lt;jrandom&gt; nickster was using snipsnap for a while
14:54 &lt;jrandom&gt; ok, anyone have anything else to bring up?
14:55  * jrandom notes that we're near the hour mark even *without* newsbyte ;)
14:55 &lt;deer&gt; &lt;polecat&gt; I like pie!
14:55 &lt;deer&gt; &lt;gott&gt; I have another thing.
14:55 &lt;deer&gt; &lt;duck&gt; oh, orz is awake
14:55 &lt;deer&gt; &lt;gott&gt; I would like to announce that soon after 0.4.2 release I will publish an interview on jrandom on i2p-related things.
14:55 &lt;deer&gt; &lt;polecat&gt; I wasn't aware this a formal meeting.  Might mention my ideas about name servers...
14:56 &lt;deer&gt; &lt;duck&gt; I suggest all japanese ppl to check out his eepsite/ircserver
14:56 &lt;deer&gt; &lt;gott&gt; Nothing specific to be said on it until the questions are asked and answered but you have something to look forward to.
14:56 &lt;deer&gt; &lt;gott&gt; it will be on my eeplog and if jrandom thinks good enough, probably featured somewhere on i2p.net
14:57 &lt;deer&gt; * gott retires again.
14:57 &lt;deer&gt; &lt;postman&gt; modulus: 
14:57 &lt;jrandom&gt; yeah, orz's site and irc server work great, i just dont know what it says :)
14:58 &lt;modulus&gt; YES?
14:58 &lt;modulus&gt; sorry for caps.
14:58 &lt;deer&gt; &lt;DrWoo&gt; polecat: so about nameserver?
14:58 &lt;deer&gt; * gott unretires
14:58 &lt;deer&gt; &lt;gott&gt; duck: does he speak english ?
14:59 &lt;jrandom&gt; oh polecat, whats up?
14:59 &lt;jrandom&gt; polecat: we have our weekly meting every tuesday at 9p GMT
14:59 &lt;deer&gt; &lt;gott&gt; I assume he does to have set everything up so well.
14:59 &lt;jrandom&gt; (logs posted @ http://www.i2p/meetings once they're done ;)
15:00 &lt;deer&gt; &lt;polecat&gt; Yes.  Well I was thinking a name server might be a good idea.  But not DNS.  c.c  I had an idea for a server that did nothing but translate between Protocol Specific Addresses and human readable names.
15:00 &lt;jrandom&gt; so a URI--&gt;URL resolver, kinda?
15:01 &lt;deer&gt; &lt;polecat&gt; That would replace hosts.txt, and eventually replace DNS itself once it supports ipv4 and ipv6.
15:01 &lt;deer&gt; &lt;polecat&gt; name =&gt; hash in the case of i2p.  Like duck.i2p =&gt; gobbledygook
15:02 &lt;jrandom&gt; right right
15:02 &lt;deer&gt; &lt;polecat&gt; Trouble with DNS is it has "requirements" (i.e. hacks) like MX servers, and root hierarchy, and nasty stuff like that.  The hackiness of DNS puts even Usenet to shame.
15:03 &lt;deer&gt; &lt;polecat&gt; I was talking about this earlier, and someone mentioned http://distributeddns.sourceforge.net/
15:03 &lt;deer&gt; &lt;polecat&gt; I haven't had a chance to look at that site though.
15:05 &lt;jrandom&gt; there are lots of things to keep in mind when working through a naming system, and in turn, there are lots of tradeoffs to be made.  there have also been lots of discussions of improvements over the years (not just within i2p) to address many of the issues, but a concrete solution would be great
15:05 &lt;deer&gt; &lt;gott&gt; quite good, quite good.
15:07 &lt;jrandom&gt; i've got my own views, but thats where one of i2p's strong points comes out - my own views are irrelevent :)  any sort ofnaming srevice can be used by client apps, as all of that functionality is outside of the core scope
15:08 &lt;jrandom&gt; i know nano is working on something too - there's some entries @ nano.i2p, though i dont know how thats progressing
15:08 &lt;deer&gt; &lt;polecat&gt; Agreed; you could write clients to use a ddns server as much as you could write them to parse the local hosts.txt
15:08 &lt;deer&gt; &lt;gott&gt; jrandom: I dread the day when hosts.txt or equivalent naming system begins to show &lt;&lt;enlarge.your.penis.i2p&gt;&gt;
15:09 &lt;deer&gt; &lt;polecat&gt; Just might be easier; at the current standing only I2PTunnel has the ability to understand hosts.txt.  Plus if we're going to compete with ipv4 and ipv6 we can't compromise limited functionality when they don't.
15:10 &lt;jrandom&gt; a while back mihi factored out the naming hooks in i2ptunnel - anything that implements http://dev.i2p.net/javadoc/net/i2p/client/naming/NamingService.html can be used transparently
15:10 &lt;jrandom&gt; (and that includes I2PTunnel and SAM)
15:10 &lt;deer&gt; &lt;polecat&gt; Really?  I'll have to look at that too...
15:11 &lt;jrandom&gt; well, they trade off functionality for security and identity
15:11 &lt;deer&gt; &lt;polecat&gt; And also since i2p has such long hashes, for cryptographic security, having a name server is even more important since most people cannot remember the full i2p hash address.
15:11 &lt;jrandom&gt; e.g. the jackboots can kick down $domainOwner's door
15:11 &lt;jrandom&gt; (and someone can spoof dns without much trouble)
15:12 &lt;jrandom&gt; but having some sort of name --&gt; location resolution functionality is definitely important
15:13 &lt;deer&gt; &lt;polecat&gt; Without a centralized server, you can't have a unique human readable name anyway.  Even if they're cryptographically signed, they still can be duplicated on the part that is comprehensible to us.
15:14 &lt;lucky&gt; ugh.
15:14 &lt;lucky&gt; Why don't you have deer block gott out?
15:14 &lt;jrandom&gt; there are many tradeoffs
15:14 &lt;jrandom&gt; i've outlined my preference at http://dev.i2p.net/pipermail/i2p/2004-February/000135.html
15:15 &lt;jrandom&gt; but i'm not goingto write a naming service anytime soon, so whatever an implementer wants to do, they're free to :)
15:15 &lt;lucky&gt; heh.  I thought that was in response to the Gott question.
15:15 &lt;jrandom&gt; heh
15:15 &lt;jrandom&gt; naw, gott has been contributing positively as of late
15:16 &lt;jrandom&gt; ok, in any case polecat, you should put up an eepsite with your ideas
15:16 &lt;lucky&gt; god, what is the world coming to?
15:16 &lt;deer&gt; &lt;polecat&gt; I'm thinking of writing a naming service myself.  I'd like to know what everyone else prefers, and get as much guidance as possible how to implement it in a way that works really really well.
15:16 &lt;lucky&gt; Oh, how can i contribute?
15:16 &lt;lucky&gt; I know some java know.  Like variable assigning.
15:16 &lt;lucky&gt; And what ++j means
15:17 &lt;deer&gt; &lt;polecat&gt; Ugh... an eepsite...
15:17 &lt;deer&gt; &lt;polecat&gt; ++j is the post-increment operator on variable j?
15:18 &lt;jrandom&gt; polecat: you can post to the mailing list or forum, as well.  perhaps make a poll in the forum if you want to see what sort of preferences people have?
15:18 &lt;deer&gt; &lt;polecat&gt; Trouble is this computer I'm on gets reset into Windoze frequently, and so unless I put my eepsite on a vfat partition, I can't share its info between operating systems.
15:19 &lt;jrandom&gt; 'k, then its prolly best to have the naming stuff on the forum instead of an eepsite :)
15:20 &lt;deer&gt; &lt;polecat&gt; Where's the forum again...?
15:20 &lt;jrandom&gt; http://forum.i2p/
15:20 &lt;jrandom&gt; and http://forum.i2p.net/
15:20 &lt;jrandom&gt; (isnt naming wonderful?  :)
15:21 &lt;deer&gt; &lt;gott&gt; I have always contributed positively.
15:21 &lt;deer&gt; &lt;polecat&gt; Yes, except we all still wget the hosts.txt file from a centralized sources.  ;3
15:22  * jrandom uses cp, not wget ;)
15:22 &lt;jrandom&gt; ok, anyone have anything else to bring up?
15:23  * jrandom doesnt mean to shut down the naming discussion, its just that we can discuss that for weeks on end
15:23 &lt;deer&gt; &lt;DrWoo&gt; dinoman is working on a cvs server in i2p?
15:23 &lt;jrandom&gt; well, there already *is* a cvs server in i2p (cvs.i2p)
15:24 &lt;jrandom&gt; but thats right - dinoman was working on a full blown gforge in i2p iirc
15:24 &lt;deer&gt; &lt;DrWoo&gt; jrandom: sorryt,I mean a fully anonymous cvs ;)
15:25 &lt;jrandom&gt; hey, cvs.i2p is fully anonymous cvs :)  i2p is completely self hosting, but without all the goodies for adding on lots of other projects
15:25 &lt;jrandom&gt; (and having a gforge on i2p would Kick Ass)
15:26 &lt;deer&gt; &lt;DrWoo&gt; jrandom: doesn't cvs.i2p run on the public server?
15:26 &lt;deer&gt; &lt;polecat&gt; gforge... dunno that...
15:27 &lt;jrandom&gt; DrWoo: maaaybe ;)
15:27 &lt;jrandom&gt; DrWoo: but the key is that developers can be anonymous and develop for i2p through i2p
15:27 &lt;jrandom&gt; if the machine that cvs.i2p is physically located on is under attack, we can just move the destination somewhere else
15:28 &lt;deer&gt; &lt;polecat&gt; Yes, so while the i2p source itself is vulnerable to being confiscated by the Long Arm of the Law, its developers are immune to a certain extent through anonymity.
15:28 &lt;jrandom&gt; let 'em have the source, its free!  :)
15:29 &lt;deer&gt; &lt;DrWoo&gt; jrandom: ya, i see what you're saying, but it still is at the risk of something like the indymedia thing
15:30 &lt;jrandom&gt; if the jackboots kicked down the door of the colo where cvs.i2p is, i'd simply install cvs somewhere else, deploy a backup of the cvs there, and run an i2prouter with the cvs.i2p private key 
15:30 &lt;jrandom&gt; (and *not* tell peole that cvs.i2p == cvs.i2p.net ;)
15:32 &lt;jrandom&gt; ok, anyone else have soemthing to bring up for the meeting?
15:32 &lt;deer&gt; &lt;polecat&gt; Hee, that's pretty cool.
15:33 &lt;jrandom&gt; if not
15:33  * jrandom winds up
15:34  * jrandom *baf*s the meeting closed
</div>
