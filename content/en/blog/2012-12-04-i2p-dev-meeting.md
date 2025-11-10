---
title: "I2P Dev Meeting - December 04, 2012"
date: 2012-12-04
author: "lillith"
description: "I2P development meeting log for December 04, 2012."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, hottuna, KillYourTV, lillith, Meeh, psi, str4d, weltende, zzz</p>

## Meeting Log

<div class="irc-log">
20:18:53  * KillYourTV has noticed that we're 17 minutes into the meeting...and we're off to a quiet start...
20:19:31  &lt;lillith&gt; i was wondering that, did i also get the wrong time or something?
20:20:23  * dg is waiting for self to be free
20:20:30  &lt;dg&gt; some stuff needs wrapping up first
20:20:33  &lt;dg&gt; sorry
20:20:39  &lt;dg&gt; you guys can start without me if you need to
20:23:07  * KillYourTV 's mostly going to be an observer due to his rather insignificant & unimportant roles...
20:23:15  &lt;KillYourTV&gt; ...so start times matter not.
20:23:39  &lt;Meeh&gt; I will be here, but I can wait until dg is ready
20:23:42  &lt;str4d&gt; I wonder if it would be possible to have two IRC leaf connections to the same leaf to reduce netsplits...
20:23:48  &lt;dg&gt; As long as nobody's becoming annoyed, I'll wait a little longer
20:23:59  &lt;dg&gt; Hopefully $task won't be too much longer
20:24:02  &lt;str4d&gt; (without doubling up on messages)
20:24:05  &lt;dg&gt; str4d: not without srs mods to IRCd
20:24:16  &lt;dg&gt; (or i2p hax?)
20:24:22  * KillYourTV nices his tasks to give more CPU time to dg
20:25:07  &lt;str4d&gt; There are already I2P mods for the IRCd so why not redundancy?
20:25:50  &lt;dg&gt; actually
20:25:50  &lt;str4d&gt; I guess it depends on the IRCd
20:26:04  &lt;dg&gt; I kind of see the amount of IRC splits as a way of measuring network health
20:26:19  &lt;dg&gt; For me, it says something about tunnel success :-P
20:27:07  &lt;str4d&gt; Speaking of which.
20:27:30  &lt;KillYourTV&gt; I don't know what mods were applied and why they were needed. (Back in the day ngircd needed a brief mod for b32 displaying...but with webirc it's not needed (and they're not displayed here anyway))
20:28:00  &lt;str4d&gt; -_-
20:49:54  &lt;psi&gt; orion: re: c++ i2p you mind if i add a build system to your code? probably scons
20:54:16  &lt;dg&gt; I'm ready
20:54:27  &lt;dg&gt; Sorry for the delay, folks
20:55:01  * dg pings #i2p-dev
21:03:16  &lt;str4d&gt; o/ dg
21:04:09  &lt;hottuna&gt; 'lo dg
21:05:07  &lt;iRelay&gt; &lt;weltende@freenode&gt; *waves*
21:05:53  &lt;psi&gt; yay
21:05:56  * psi timed out
21:11:17  &lt;hottuna&gt; ready dg?
21:13:23  &lt;dg&gt; sorry, I d/c'd
21:13:26  &lt;dg&gt; What did I miss?
21:13:26  &lt;dg&gt; &lt;+iRelay&gt; &lt;weltende@freenode&gt; *waves*
21:13:26  &lt;dg&gt;  chanserv gives voice to psi
21:13:26  &lt;dg&gt; &lt;+psi&gt; yay
21:13:26  &lt;dg&gt;  +psi timed out
21:13:26  &lt;dg&gt;  s-771 is now known as s-77
21:13:26  &lt;dg&gt; &lt;+dg&gt; yay!
21:13:26  &lt;dg&gt; &lt;+dg&gt; Everyone woke up for me&lt;3
21:13:27  &lt;dg&gt; &lt;+dg&gt; weltende: Any news regarding mailing list? plz have some for me
21:13:27  &lt;Meeh&gt; *waves*
21:13:27  &lt;hottuna&gt; I dont think you missed anything
21:13:27  &lt;psi&gt; yup
21:13:27  &lt;dg&gt; alrighty
21:13:27  &lt;dg&gt; So, weltende: ..
21:14:37  &lt;iRelay&gt; &lt;weltende@freenode&gt; not really.. no time so far
21:14:47  &lt;iRelay&gt; &lt;weltende@freenode&gt; kytv could do it.. he has root access to the box I had in mind afair ;-)
21:14:50  * dg waits a few minutes
21:15:41  * dg pokes KillYourTV
21:17:30  &lt;iRelay&gt; &lt;weltende@freenode&gt; dg: and more cowbell!
21:17:34  &lt;iRelay&gt; &lt;weltende@freenode&gt; err.. structure
21:18:02  * dg was never any good at that, but he'll try
21:18:12  * dg moves on
21:18:15  &lt;dg&gt; KillYourTV: ping when back
21:18:21  &lt;dg&gt; So, status updates.
21:18:40  * str4d has ~40 mins, so GTFG fg ;P
21:18:40  &lt;KillYourTV&gt; hmm? I didn't realize I had root but I can to throw some time at it (coursework & moving has taken up a considerable bit of time)
21:18:40  &lt;dg&gt; Are they worth bringing back since we have the meetings (and hopefully the summaries of them, but they're not working out right now)?
21:19:15  &lt;str4d&gt; dg, who would the status updates be for?
21:19:22  &lt;str4d&gt; s/for/aimed at/
21:19:25  &lt;iRelay&gt; str4d meant: dg, who would the status updates be aimed at?
21:19:34  &lt;dg&gt; Well, I assume the previous ones which jrandom maintained were for those who wanted a TL;DR of the meetings
21:20:06  &lt;dg&gt; Perhaps what we did with the last meeting (on the website) where the results were summarized at the top of the page
21:20:31  &lt;hottuna&gt; They would be nice for the sake of community-building, but also a bit of work.
21:20:49  * dg doesn't think it's a necessity as such but it'd be nice to say what the meeting accomplished/decided
21:21:32  &lt;hottuna&gt; Would anyone like to do it?
21:22:01  &lt;str4d&gt; On the site revamp I've taken the status updates as "blog entries"
21:22:05  &lt;str4d&gt; So it might be better to write those, or structure the status updates as such.
21:22:20  &lt;hottuna&gt; that sounds pretty good
21:22:57  &lt;str4d&gt; (And since the blog will end up with RSS or whatever, that can then be used to feed into any other distribution lines that are desired)
21:23:24  &lt;psi&gt; point 1: to consider, CCC
21:23:27  &lt;lillith&gt; i was thinking after a meeting we could have a new thread on zzz.i2p, to allow people to reply with any follow up things from what has been discussed
21:23:30  &lt;psi&gt; how will "this side" organize?
21:23:55  &lt;hottuna&gt; I support the blog idea, however someone would have to do it.
21:24:50  &lt;psi&gt; oh damn lag
21:25:27  &lt;str4d&gt; And the status updates don't need to necessarily be too "minutes-y", since the meetings section of the revamp is where actual minutes should go (and I'm thinking that the minutes could be put into a feed as well, while the full logs are displayed with the minutes on the site)
21:26:10  &lt;zzz&gt; dg, fyi, jr's status updates were sent out hours before each meeting, and they were not minutes of the previous meeting
21:26:55  &lt;str4d&gt; Ah, thanks zzz - so more of a general get-everyone-up-to-speed-before-the-meeting update.
21:27:10  &lt;zzz&gt; correct
21:27:39  &lt;zzz&gt; dg, fyi, jr's status updates were sent out hours before each meeting, and they were not minutes of the previous meeting
21:28:00  &lt;dg&gt; zzz: ah ok, it was a tl;dr of the $week?
21:28:03  &lt;dg&gt; &lt;+dg&gt; Moving on?
21:28:03  &lt;dg&gt; &lt;+dg&gt; psi: ccc is on the agenda :)
21:28:03  &lt;dg&gt; --- aquarium (grenze@irc2p) has joined #i2p-dev
21:28:06  &lt;dg&gt; --- w8rabbit (w8rabbit@irc2p) has quit (Killed (nickserv (Nick kill enforced)))
21:28:06  &lt;zzz&gt; &lt;str4d&gt; Ah, thanks zzz - so more of a general get-everyone-up-to-speed-before-the-meeting update.
21:28:06  &lt;zzz&gt; &lt;zzz&gt; correct
21:28:09  &lt;dg&gt; &lt;+dg&gt; Next topic: * PR management role (http://zzz.i2p/topics/1299)
21:28:09  &lt;dg&gt; &lt;+dg&gt; I don't know if the guy who posted that is here..
21:28:09  &lt;str4d&gt; dg, repost: And the status updates don't need to necessarily be too "minutes-y", since the meetings section of the revamp is where actual minutes should go (and I'm thinking that the minutes could be put into a feed as well, while the full logs are displayed with the minutes on the site)
21:28:24  &lt;str4d&gt; Yes he is - orion?
21:28:34  &lt;hottuna&gt; dg, would you be willing to write a status update before meetings in the blog?
21:29:16  &lt;str4d&gt; (he's in-chan at least)
21:29:23  &lt;str4d&gt; And FTR this is the guy working on I2PCPP
21:30:15  * psi is compiling i2pcpp
21:31:12  &lt;psi&gt; i am also looking at the code as well
21:32:58  &lt;psi&gt; i've got a SConstruct file
21:36:03  &lt;dg&gt; damn rats eating the cables
21:36:03  &lt;dg&gt; [repost]
21:36:03  &lt;dg&gt; &lt;+psi&gt; i've got a SConstruct file
21:36:05  &lt;dg&gt; &lt;+dg&gt; str4d:
21:36:05  &lt;dg&gt; &lt;+dg&gt; * Website revamp updates
21:36:05  &lt;dg&gt; &lt;+dg&gt; Anything?
21:36:08  &lt;dg&gt; [/repost]
21:36:12  &lt;str4d&gt; dg, need m0ar stables
21:36:15  &lt;str4d&gt; =P
21:36:21  &lt;dg&gt; :(
21:36:36  &lt;str4d&gt; dg, I've got per-net urls working
21:36:59  &lt;dg&gt; oh nice, progress
21:37:02  &lt;dg&gt; How did you do it?
21:37:06  * psi note to self don't compile with -j8 on a machine with 4 cores
21:37:13  &lt;str4d&gt; So in the page files, if you put &lt;a href="http://{{ i2pconv(trac.i2p2.i2p) }}/"&gt; it will convert to trac.i2p2.de
21:37:32  &lt;str4d&gt; And likewise for any other sites that have (hardcoded) known public urls.
21:37:39  &lt;str4d&gt; Otherwise it appends .to
21:38:16  &lt;str4d&gt; dg, problem was that Flask was caching filters applied to strings.
21:38:19  &lt;str4d&gt; So it was eval-ed on first template read and then stored.
21:38:39  &lt;iRelay&gt; &lt;weltende@freenode&gt; psi: unless it does multiple threads per core ;)
21:38:43  &lt;str4d&gt; Turning the filter into a context processor (so the func is eval-ed on every request) did the job.
21:38:46  &lt;dg&gt; Oh, ha
21:39:34  &lt;str4d&gt; I can try generalize the function so you pass in the entire URL and it finds and changes the domain bit, if people would prefer to use it that way.
21:39:45  &lt;str4d&gt; But it Works For Now (TM)
21:40:01  &lt;dg&gt; psi:
21:40:04  &lt;dg&gt; * CCC workshop/lightning talk discussion
21:40:28  &lt;psi&gt; yes
21:40:39  * psi reviews zzz.i2p link
21:40:58  &lt;str4d&gt; (aside: Once I get some free time (after getting the bugs out of the feed mechanism) I'd like to work out the download mirroring stuff with welterde.)
21:42:36  &lt;iRelay&gt; &lt;weltende@freenode&gt; str4d: well.. should be simple enough.. text file in mtn with list of all http, ftp mirrors..
21:44:32  &lt;iRelay&gt; &lt;weltende@freenode&gt; (and in the backend just an rsync master site, from which all mirrors pull)
21:44:40  &lt;hottuna&gt; did we choose a lightning talk topic?
21:44:40  &lt;psi&gt; ok regarding CCC there is 0% chance for me to get the required docs to get there in time
21:44:40  &lt;psi&gt; also... lots of "other stuff"
21:44:40  &lt;psi&gt; in general I am overloaded due to finals
21:44:40  &lt;psi&gt; also lag
21:45:31  &lt;str4d&gt; welterde, I guessed so, but I'm not familiar with the current mirror setup.
21:47:26  &lt;str4d&gt; The other thing, of course, is migrating the rest of the old pages across (and tidying up nav layout)
21:48:06  &lt;dg&gt; &lt;+psi&gt; ok regarding CCC there is 0% chance for me to get the required docs to get there in time
21:48:06  &lt;dg&gt; &lt;+psi&gt; also... lots of "other stuff"
21:48:06  &lt;dg&gt; &lt;+psi&gt; in general I am overloaded due to finals
21:48:06  &lt;dg&gt; &lt;+psi&gt; also lag
21:48:06  &lt;dg&gt; &lt;+dg&gt; Could probably ask the audience who has used i2p before
21:48:09  &lt;dg&gt; &lt;+iRelay&gt; &lt;weltende@freenode&gt; (and in the backend just an rsync master site, from which all mirrors pull)
21:48:09  &lt;dg&gt; &lt;+dg&gt; psi: yeah, ech and welt are going though afaik
21:48:11  &lt;dg&gt; &lt;+str4d&gt; welterde, I guessed so, but I'm not familiar with the current mirror setup.
21:51:57  &lt;str4d&gt; Okay, heading off o/
21:52:13  &lt;dg&gt; bye o/
21:52:28  &lt;dg&gt; We really should have started earlier
21:52:31  &lt;dg&gt; g'damnit
21:52:47  &lt;str4d&gt; I'll see if I can be back in time for the end, but no guarantees.
21:53:35  &lt;dg&gt; alright, stenography
21:53:42  * dg pokes Meeh
21:54:01  &lt;psi&gt; we need a generic interface for making transports
21:54:04  &lt;psi&gt; (imo)
21:54:23  &lt;psi&gt; s/need/should\ have/
21:54:26  &lt;iRelay&gt; psi meant: we should\ have a generic interface for making transports
21:55:08  &lt;Meeh&gt; I'm here, sorry just got disturbed with a phone call, back now
21:55:16  &lt;dg&gt; afaik there's something called "restricted routes" but I don't know how they work
21:55:19  &lt;Meeh&gt; *catchin up/reading log*
21:55:22  &lt;dg&gt; (nor have they been implemented..?)
21:55:28  &lt;dg&gt; Meeh: there isn't too much to read.. :(
21:55:50  &lt;psi&gt; dg no docs on that?
21:56:10  &lt;dg&gt; psi: mention on www.i2p2.i2p is all I found under roadmap or something..
21:56:47  &lt;psi&gt; if anyone happens to remember what "restricted routes" are/were please speak up
21:56:50  &lt;lillith&gt; dg, as i understand it restricted routes are like 'darknet mode' on freenet, you only connect via trusted peers
21:56:57  &lt;psi&gt; ah
21:57:16  &lt;dg&gt; ah
21:57:31  &lt;lillith&gt; i think :)
21:57:34  &lt;psi&gt; sounds like that could be it
21:58:11  &lt;dg&gt; matches the name
21:58:33  &lt;lillith&gt; it's been mentioned on zzz.i2p recently iirc
21:59:40  &lt;psi&gt; if someone who does know for sure from way back when a "confirmation" would be great
22:01:31  &lt;lillith&gt; http://zzz.i2p/topics/114
22:04:31  * dg reads
22:04:31  &lt;lillith&gt; it's not what i meant, but it explains pretty thoroughly
22:06:02  &lt;Meeh&gt; just wondering, where are we in the meeting?
22:06:13  &lt;Meeh&gt; what's current topic
22:06:16  &lt;dg&gt; We're kind of floating around, Meeh
22:06:23  &lt;Meeh&gt; ah ok
22:06:31  &lt;dg&gt; "* Hide I2P traffic. Like Tor, hide so it looks like SSL traffic, or something. (Considering countries where darknets is illegal) "
22:06:41  &lt;dg&gt; (We started late and thus sucking)
22:08:10  &lt;Meeh&gt; yea, we should think about possible alternative transport for countries blocking and making darknets illegal
22:09:47  &lt;lillith&gt; well to start with: how distinctive is i2p traffic now?
22:09:50  &lt;hottuna&gt; I think we ought to play something like that the same way tor does
22:09:50  &lt;hottuna&gt; and deploy it not before it is needed
22:09:50  &lt;hottuna&gt; as to prolong any arms-race
22:09:50  &lt;hottuna&gt; but we haven't been blocked anywhere yet
22:09:50  &lt;hottuna&gt; as far as I know
22:10:05  &lt;dg&gt; (yet)
22:10:25  &lt;dg&gt; Also, the lack of this sort of "protection" i.e system keeps some away from i2p
22:10:32  &lt;psi&gt; in general a generic transport api would be a developer's goldmine
22:10:32  &lt;hottuna&gt; we have a lot of random data, but none of the headers of ssl
22:10:57  &lt;dg&gt; obfsproxy is amazing but we don't need something of that level
22:11:48  &lt;psi&gt; some interface that you'd implement that does your version of data transport wether it's over goats or http+ssl
22:11:50  &lt;iRelay&gt; &lt;weltende@freenode&gt; psi: we already have a generic transport api ;)
22:11:54  &lt;lillith&gt; i2p can't really be 'too secure'
22:12:02  &lt;hottuna&gt; a transport api would be a good idea, and would allow for rapid development of needed transports
22:12:14  &lt;psi&gt; we do eh?
22:12:36  &lt;psi&gt; i need to look at the code closer
22:12:56  &lt;psi&gt; either it's not sticking out well or i over looked it or it's not there
22:13:03  &lt;Meeh&gt; yea, yet.. it's a matter of time
22:13:36  &lt;iRelay&gt; &lt;weltende@freenode&gt; router/java/src/net/i2p/router/transport/Transport.java is the interface you have implement
22:13:36  &lt;dg&gt; certainly not, lillith
22:13:46  &lt;dg&gt; although i2p is already a lot of crypto
22:14:17  &lt;hottuna&gt; i think obfsproxy is horrible, and it's tacked onto tor in the most frankenstein-y fashion possible
22:14:40  &lt;dg&gt; I don't like their pluggable transports but the tech is cool
22:14:48  &lt;dg&gt; (emulating Skype is one cool thing)
22:17:27  &lt;psi&gt; iirc obsproxy can be counter productive
22:17:33  &lt;hottuna&gt; i've gotta go
22:17:46  &lt;psi&gt; due to it emulating a survalence network
22:17:53  * psi spelling
22:18:00  &lt;dg&gt; bye
22:19:55  &lt;psi&gt; i've got to part for now as well
22:20:27  &lt;dg&gt; I think we can just call it a day now and have it next week/sometime soon(er)
22:20:34  &lt;dg&gt; Kind of fucked this one up
22:21:04  &lt;iRelay&gt; &lt;weltende@freenode&gt; sounds like a plan
22:21:07  &lt;psi&gt; it's best to have a predefine meeting structure
22:21:54  &lt;dg&gt; yeah
22:26:10  &lt;Meeh&gt; disconnected...
22:26:29  &lt;Meeh&gt; 23:10:30 &lt;+psi&gt; in general a generic transport api would be a developer's goldmine
22:26:32  &lt;Meeh&gt; 23:10:31 &lt;hottuna&gt; we have a lot of random data, but none of the headers of ssl
22:26:35  &lt;Meeh&gt; 23:13:01 &lt;+Meeh&gt; yea, yet.. it's a matter of time
22:26:38  &lt;Meeh&gt; 23:13:15 &lt;+Meeh&gt; so why make people offline from i2p for a while.. better safe than sorry
22:26:41  &lt;Meeh&gt; what did I miss?
22:27:11  &lt;psi&gt; Meeh: meeting adjurned for now
22:27:11  * psi spelling
22:27:58  &lt;psi&gt; &lt;dg&gt; certainly not, lillith
22:27:58  &lt;Meeh&gt; ah, lame.. meeting next week?
22:28:10  * psi lag
22:28:55  &lt;lillith&gt; Meeh, to be decided, maybe before since this one wasn't a great success
22:29:25  &lt;Meeh&gt; true true, next week then
</div>
