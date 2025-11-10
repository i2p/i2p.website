---
title: "I2P Dev Meeting - September 08, 2010"
date: 2010-09-08
author: "@Mathiasdm"
description: "I2P development meeting log for September 08, 2010."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> </p>

## Meeting Log

<div class="irc-log">
22:02 &lt;@Mathiasdm&gt; okay
22:02 &lt;@Mathiasdm&gt; meeting time
22:03 &lt;@Mathiasdm&gt; 0) Hello
22:03 &lt;@Mathiasdm&gt; 1) Website content progress
22:03 &lt;@Mathiasdm&gt; 2) Website backend progress
22:03 &lt;@Mathiasdm&gt; 3) Location for dev discussion
22:03 &lt;@Mathiasdm&gt; 4) Task appointing + handling of disagreements
22:03 &lt;@Mathiasdm&gt; 5) Status updates
22:03 &lt;@Mathiasdm&gt; 6) Upcoming dev conferences
22:03 &lt;@Mathiasdm&gt; okay
22:03 &lt;@Mathiasdm&gt; 0) Hello
22:04 &lt;@Mathiasdm&gt; Welcome to the 208th dev meeting! (shamelessly stolen from badger :p)
22:04  * Mathiasdm pokes everyone
22:04 &lt;eche|on&gt; *poke*
22:04  * Mathiasdm pokes zzz, thanks for the op
22:06 &lt;@Mathiasdm&gt; hm, more poking needed to wake everyone up? zzz badger dr|z3d dream duck eche|on hottuna postman sponge superuser ReturningNovice (sorry :))
22:06 &lt;eche|on&gt; *POKE*
22:06 &lt;@Mathiasdm&gt; sorry, eche|on :p saw your poke
22:08 &lt;duck&gt; moin
22:08 &lt;@Mathiasdm&gt; moin duck
22:09 &lt;hawk&gt; * Mathiasd1 pokes welterde 
22:11 &lt;@Mathiasdm&gt; okay, waiting a bit longer then, since there's only 3 of us so far
22:11 &lt;@Mathiasdm&gt; anyone who wants to join in, just poke back
22:11 &lt;whitenoise&gt; *poke*
22:11 &lt;@zzz&gt; ack
22:12 &lt;@Mathiasdm&gt; aha, lead dev, good :)
22:13 &lt;@Mathiasdm&gt; and just to be sure as many people as possible can join in, waiting 2 more minutes and then starting
22:14 &lt;@Mathiasdm&gt; 1 more minute now
22:14 &lt;superuser&gt; mooin
22:15 &lt;@Mathiasdm&gt; right on time, superuser ;)
22:15 &lt;@Mathiasdm&gt; hi all
22:15 &lt;superuser&gt; ;-)
22:15 &lt;superuser&gt; hi Mathiasdm
22:15 &lt;superuser&gt; and all
22:15 &lt;@Mathiasdm&gt; 1) Website content progress
22:15 &lt;@Mathiasdm&gt; as we probably all know, I2P development is currently halted due to the specs overhaul
22:16  * Mathiasdm hands the hot potato to zzz, so he can talk about the specs overhaul progress
22:16 &lt;eche|on&gt; right
22:17 &lt;@zzz&gt; it's been 7 weeks, progress is slow. I'm working on i2cp right now, I've spent several hours on it already
22:17 &lt;@zzz&gt; need other ppl to chip in both on what they've promised to do, and on the stuff that is unclaimed
22:17 &lt;@zzz&gt; eot
22:18 &lt;@Mathiasdm&gt; okay
22:18  * Mathiasdm will get started again tomorrow, now dev environment is set up again
22:18 &lt;@Mathiasdm&gt; others having something to say about it, go ahead :)
22:19 &lt;@Mathiasdm&gt; guess not
22:19 &lt;@Mathiasdm&gt; hm
22:19 &lt;@Mathiasdm&gt; 2) Website backend progress
22:19 &lt;eche|on&gt; I think is is great form the peoples doing it.
22:19 &lt;@Mathiasdm&gt; oh
22:19 &lt;@Mathiasdm&gt; sorry :)
22:21 &lt;@Mathiasdm&gt; we're skipping 2) for now, unless welt comes in
22:21 &lt;@Mathiasdm&gt; 3) Location for dev discussion
22:22 &lt;@Mathiasdm&gt; this is related to http://zzz.i2p/topics/719
22:22 &lt;@Mathiasdm&gt; I quote:
22:22 &lt;@Mathiasdm&gt; "* Post developer discussions on zzz.i2p. What I mean is: IRC is a highly 'volatile' medium, where not everyone is online all the time, and not everyone logs. It's a great medium for a short discussion, but do consider posting a short write-up on zzz.i2p, so others can join in on the discussion."
22:22 &lt;eche|on&gt; dev discussion is a hard topic. IRC is nice, but not reliant neither an archive
22:22 &lt;@Mathiasdm&gt; yes, agreed
22:23 &lt;@Mathiasdm&gt; but there are many things to chose from
22:23 &lt;@Mathiasdm&gt; zzz.i2p, forum.i2p, mailing list
22:23 &lt;@Mathiasdm&gt; well, okay, 3 things :p
22:23 &lt;eche|on&gt; I would suggest some central point of archive
22:23 &lt;eche|on&gt; with a backup.
22:24 &lt;@Mathiasdm&gt; yes
22:24 &lt;@Mathiasdm&gt; but setting up distributed storage for this sounds like a hard thing :p
22:24 &lt;@Mathiasdm&gt; though mailing list is doable, I guess
22:25 &lt;@Mathiasdm&gt; mailing list is 'kinda distributed'
22:25 &lt;eche|on&gt; :-)
22:25 &lt;superuser&gt; isn't the website itself already distributed?
22:25 &lt;@Mathiasdm&gt; anyone else, ideas?
22:25 &lt;eche|on&gt; a mailinglist is a good solution, to
22:26 &lt;superuser&gt; could also go there
22:26 &lt;@Mathiasdm&gt; yes, but that doesn't include the forum, superuser 
22:26 &lt;eche|on&gt; rightm website is in monotone
22:26 &lt;@Mathiasdm&gt; true
22:26 &lt;superuser&gt; no, I don't mean the forum, but website itself
22:26 &lt;superuser&gt; aren't old dev meetings available there somewhere too?
22:26 &lt;@Mathiasdm&gt; but it's hard to discuss when you have to check your discussions into monotone :p
22:27 &lt;superuser&gt; true
22:27 &lt;@Mathiasdm&gt; perhaps with the new backend welt is working on, it'll be more doable
22:27 &lt;superuser&gt; would only be of interest for archiving, not for keeping discussing
22:28 &lt;@Mathiasdm&gt; for a temporary way, I would propose: if you keep a big discussion on IRC, post a few notes on _a_ persistent medium
22:29 &lt;@Mathiasdm&gt; be it zzz.i2p, mailing list or forum
22:29 &lt;@Mathiasdm&gt; I know, that's a bit vague
22:29 &lt;eche|on&gt; I vote mailinglist ++ 
22:29 &lt;@Mathiasdm&gt; hm, welt, are mailinglist instructions on the website somewhere?
22:29 &lt;superuser&gt; you mean welt's nntp service?
22:29 &lt;@Mathiasdm&gt; mailing list sounds good to me too, eche|on, but I wonder if it will work to get everyone to use it?
22:29 &lt;eche|on&gt; currently no ml available
22:29 &lt;@Mathiasdm&gt; yes, superuser 
22:29 &lt;@Mathiasdm&gt; er
22:29 &lt;@Mathiasdm&gt; or what was it
22:29 &lt;@Mathiasdm&gt; I think so
22:30 &lt;@Mathiasdm&gt; eche|on: welt set a few ml's up this summer
22:30 &lt;eche|on&gt; nntp is news server
22:30 &lt;@Mathiasdm&gt; but not widely used yet
22:30 &lt;@Mathiasdm&gt; yes, indeed, but there's a mailing list now too
22:30 &lt;@Mathiasdm&gt; but I don't have the location here
22:30 &lt;@Mathiasdm&gt; zzz, duck: opinions?
22:31 &lt;superuser&gt; I have no mailing list info so far, just seen welt's and Mathiasdm's and ReturningNovice's posts on news server
22:32 &lt;@zzz&gt; I'm not a big fan of an ML but I'll use it if ppl want. welt's seems to be a big secret atm
22:33 &lt;duck&gt; I think zzz.i2p is fine
22:33 &lt;@Mathiasdm&gt; imho anything not-irc would be useful (I like IRC, as said before, but too much dev discussions are unfolloweable)
22:33 &lt;eche|on&gt; zzz.i2p is fine, but: irc discussions needs to be copied intoi AND somehow a kind of backup would be nice
22:34 &lt;@Mathiasdm&gt; hm, maybe I can set s omething up like
22:34 &lt;@Mathiasdm&gt; er
22:34 &lt;@Mathiasdm&gt; what was it called
22:34 &lt;@Mathiasdm&gt; 2 or 3 years ago
22:34 &lt;@Mathiasdm&gt; trevorreznik.i2p?
22:36 &lt;@Mathiasdm&gt; how about: we keep using zzz.i2p, and we start using a mailing list, and try to make sure IRC discussions don't stay IRC-only?
22:36 &lt;duck&gt; all major design stuff is already on zzz.i2p
22:36 &lt;eche|on&gt; better: try keep using zzz.i2p and copy IRC into it.
22:36 &lt;duck&gt; I dont see your problem
22:37 &lt;superuser&gt; what if zzz one disappears
22:37 &lt;superuser&gt; s//?
22:37 &lt;duck&gt; dev/design
22:37 &lt;@Mathiasdm&gt; for example, everything sponge posts (just an example, sponge :p) about seedless and bob is often irc-only discussion
22:38 &lt;duck&gt; I dont think a mailinglist will result into sponge documenting his protocol and api
22:38 &lt;duck&gt; but sure, give it a try
22:39 &lt;@Mathiasdm&gt; nooo, that's not what I meant, duck 
22:39 &lt;@Mathiasdm&gt; as said, I don't care if it's on zzz.i2p or on mailing list
22:39 &lt;@Mathiasdm&gt; I just don't want it to be IRC-only, those discussions
22:39 &lt;@Mathiasdm&gt; but yes, you have a good point too
22:39 &lt;@Mathiasdm&gt; that some things will perhaps stay irc-only
22:39 &lt;duck&gt; then go talk to sponge
22:39 &lt;@Mathiasdm&gt; it was an example
22:40 &lt;duck&gt; (which you might be doing through this meeting ofc)
22:40 &lt;duck&gt; ok, understood
22:40 &lt;@Mathiasdm&gt; :)
22:41 &lt;@Mathiasdm&gt; okay, I guess if everyone just tries to post things on zzz.i2p (or mailing list -- but we'll wait for welt :p), that's settled
22:42 &lt;@Mathiasdm&gt; for now, at least
22:42 &lt;@Mathiasdm&gt; anyone have anything to add on this?
22:44 &lt;@Mathiasdm&gt; okay
22:44 &lt;@Mathiasdm&gt; next
22:44 &lt;@Mathiasdm&gt; 4) Task appointing + handling of disagreements
22:45 -!- Moru [kvirc@irc2p] has joined #i2p-dev
22:45 &lt;@Mathiasdm&gt; currently, tasks (displayed on http://www.i2p2.de/team.html ) are appointed/chosen by people simply changing the webpage
22:45 &lt;hawk&gt; &lt;preforce&gt; Title: Team - I2P (at www.i2p2.de)
22:45 &lt;@Mathiasdm&gt; so if you want to do a task, you just do it, and you add yourself to the webpage
22:45 &lt;@Mathiasdm&gt; which is good, I guess :)
22:46 &lt;eche|on&gt; if someone disagree: discussion in IRC/zzz.i2p
22:46 &lt;@Mathiasdm&gt; yes, disagreeing is the point
22:46 &lt;eche|on&gt; but people need checkin-rights to change, means: need som etrust from existant devs
22:46 &lt;@Mathiasdm&gt; there was disagreement this summer, and we didn't really handle that
22:46 &lt;@Mathiasdm&gt; true, eche|on 
22:47 &lt;@Mathiasdm&gt; how do we resolve a discussio if the people disagreeing can't come to agreement?
22:47 &lt;@Mathiasdm&gt; vote or something?
22:47 &lt;@Mathiasdm&gt; that's what I was wondering about
22:48 &lt;@Mathiasdm&gt; suggestions?
22:48 &lt;eche|on&gt; last line of defense was noted once
22:48 &lt;eche|on&gt; which was zzz
22:48 &lt;@Mathiasdm&gt; last line of defense?
22:48 &lt;@Mathiasdm&gt; ah
22:49 &lt;whitenoise&gt; what about a third better solution?
22:49 &lt;duck&gt; if all else fails; resort to zzz
22:49 &lt;eche|on&gt; but voting is a nice idea, but I think a solution will be found ahead
22:49 &lt;@Mathiasdm&gt; if the third solution is definitely better, the two parties will choose that one ;)
22:50 &lt;@Mathiasdm&gt; hm, okay
22:50 &lt;@Mathiasdm&gt; just out of curiosity, zzz, you agree to being 'the last line of defense'? :)
22:50 &lt;@Mathiasdm&gt; it sounds okay to me, but do you want that yourself?
22:51 &lt;@zzz&gt; not particularly. my rule is whoever is actually doing something is in charge. ppl that do nothing but talk and piss other ppl off are not.
22:52 &lt;@zzz&gt; there's plenty of work to go around.
22:53 &lt;@Mathiasdm&gt; okay :) sounds good
22:53 &lt;@Mathiasdm&gt; anyone have additional comments? if not, next item
22:53 &lt;superuser&gt; generally "the one who does it is in charge" sounds good
22:53 &lt;superuser&gt; but what if two parties actually do
22:53 &lt;superuser&gt; and still go in opposite directions?
22:54 &lt;superuser&gt; I guess in that case a voting mechanism would not be too uncool
22:54 &lt;@Mathiasdm&gt; true
22:54 &lt;@zzz&gt; if it's code I can pick. I'm definitely not the last line of defense for the website. welt and echelon are.
22:55 &lt;@Mathiasdm&gt; well, if discussion happens and a solution cannot be found, there can be a vote or someone (zzz, welt?) can pick
22:55 &lt;@zzz&gt; they would pick a winner by pulling privs from the loser.
22:56 &lt;@Mathiasdm&gt; *only if it's a nasty discussion, I would hope ;) friendly disagreements shouldn't result in losing privs :p
22:57 &lt;eche|on&gt; right
22:58 &lt;@Mathiasdm&gt; okay then
22:58 &lt;@Mathiasdm&gt; next point
22:58 &lt;@Mathiasdm&gt; if that's okay
22:58 &lt;@Mathiasdm&gt; 5) Status updates
22:58 &lt;eche|on&gt; ok
22:59 &lt;@Mathiasdm&gt; I will start 'collecting' status updates this weekend, I think
22:59 &lt;@Mathiasdm&gt; I was going to do so last week, but caught up in work
22:59 &lt;eche|on&gt; great. go ahead.
22:59 &lt;@Mathiasdm&gt; basically, simply 'what did you do last week?' and 'what are your plans for next week?'
23:00 &lt;@Mathiasdm&gt; and I'll post them a bit summarized on the website
23:00 &lt;@Mathiasdm&gt; suggestions are always welcome :)
23:00 &lt;@Mathiasdm&gt; okay, final point (added only a bit before starting the meeting)
23:00 &lt;@Mathiasdm&gt; 6) Upcoming dev conferences
23:01 &lt;@Mathiasdm&gt; -who's going to 27c3?
23:01 &lt;@Mathiasdm&gt; -who's going to brucon?
23:01 &lt;@Mathiasdm&gt; -any others?
23:02 &lt;@Mathiasdm&gt; I will certainly attend brucon, and most likely 27c3 for a day (and will stay in berlin for a few days)
23:02 &lt;whitenoise&gt; Mathiasdm, I added 1 more point 10 min. before the beginning.
23:02 &lt;@Mathiasdm&gt; oh? sorry, didn't see
23:03 &lt;@Mathiasdm&gt; okay, will do that in a minute, whitenoise 
23:03 &lt;whitenoise&gt; ok
23:03 &lt;whitenoise&gt; thanks
23:03 &lt;@Mathiasdm&gt; nobody remarks on dev conferences?
23:04 &lt;@Mathiasdm&gt; then: 7) Promoting the usage of the bittorrent protocol inside I2P: pros and cons
23:04  * Mathiasdm hands hot potato to whitenoise 
23:04 &lt;whitenoise&gt; Ok, so we discussed this a little bit with duck
23:05 &lt;whitenoise&gt; While it's a good way for cover traffic and network growth, it may lead to the notoriety of I2P as a illegal file-sharing network
23:05 &lt;eche|on&gt; I decided to not attend to 27c3
23:06 &lt;@Mathiasdm&gt; ah, too bad, eche|on 
23:06 &lt;@Mathiasdm&gt; true, whitenoise 
23:06 &lt;whitenoise&gt; On the other hand...
23:06 &lt;superuser&gt; I think, bt should not be empahsized more than other services, but i2p be promoted as general use network
23:07 &lt;superuser&gt; oh, he had not yet finished...
23:07 &lt;@Mathiasdm&gt; he might be lagging, give him a bit :)
23:08 &lt;whitenoise&gt; if we don't promote this protocol, in some not very near future, if the business model for selling digital media is not changed, the pressure on torrent users will be higher, so they will start looking for ways to hide
23:08 &lt;whitenoise&gt; which can lead to my first point (notoriety) anyway
23:08 &lt;whitenoise&gt; but it's doubtful, of course
23:08 &lt;Moru&gt; Hello! Excuse me for butting here... sad but true, promote it as filesharing and you will have loads more users and plenty of developers joining. Mabe even get funded by those that wants to use a safe filesharing platform.
23:09 &lt;@Mathiasdm&gt; simply promoting it would not do that, imho
23:09 &lt;@Mathiasdm&gt; and whitenoise, you are right about notoriety
23:09 &lt;@Mathiasdm&gt; but are we promoting it?
23:10 &lt;whitenoise&gt; Imo, right now we don't
23:10 &lt;@Mathiasdm&gt; and bittorrent in itself is not causing the notoriety, file sharing is (imho important distinction, but perhaps not in this discussion)
23:10 &lt;@Mathiasdm&gt; (and hi, Moru)
23:11 &lt;whitenoise&gt; Well, bittorrent is the most used way, that's why I talk about it
23:11 &lt;whitenoise&gt; of course, it may be emule or anything else
23:11 &lt;@Mathiasdm&gt; how would you see promoting it?
23:12 &lt;whitenoise&gt; For example, current simple users have some difficulties setting everything up
23:12 &lt;whitenoise&gt; We could make info about bittorrent more conspicuous
23:13 &lt;@Mathiasdm&gt; hm, yes
23:13 &lt;whitenoise&gt; description more simple
23:13 &lt;whitenoise&gt; and so on.
23:13 &lt;@Mathiasdm&gt; but that's (imho) more a general I2P problem
23:13 &lt;whitenoise&gt; maybe improve i2psnark a little
23:13 &lt;@Mathiasdm&gt; I2P could become a lot more conspicuous :p
23:13 &lt;whitenoise&gt; yes
23:14 &lt;whitenoise&gt; but doing it (as well as advertising it on twitter, for example) will surely attract some users
23:14 &lt;@Mathiasdm&gt; yes
23:14 &lt;@Mathiasdm&gt; well, I agree, and I hope we will more towards making everything clearer (better usability and such) in the near future
23:14 &lt;whitenoise&gt; so, the question is, I guess, what we should do and what we shouldn't
23:15 &lt;whitenoise&gt; improve description but don't advertise as a filesharing network, maybe?
23:15 &lt;@Mathiasdm&gt; what we should do (once development of 0.9 starts) is imho take a look at the 'pain points' of usability
23:15 &lt;eche|on&gt; laready got some ideas of those
23:17 &lt;@Mathiasdm&gt; yes, I2P description would help; console overhaul (perhaps? I don't know) would help
23:17 &lt;@Mathiasdm&gt; eche|on: didn't we have a .pdf with usability remarks from a conference you went?
23:17 &lt;eche|on&gt; hm
23:18 &lt;@zzz&gt; i have it
23:18 &lt;eche|on&gt; need to look for it, but we had some issues over all. 
23:18 &lt;@Mathiasdm&gt; have a link, zzz?
23:19 &lt;@Mathiasdm&gt; okay, we could focus on it a bit after the website specs?
23:20 &lt;@zzz&gt; http://zzz.i2p/files/petcon-usability-long.pdf
23:20 &lt;@Mathiasdm&gt; thx
23:20 &lt;eche|on&gt; thats a nice idea
23:21 &lt;@Mathiasdm&gt; okay then
23:21 &lt;@Mathiasdm&gt; other remarks or ideas, whitenoise?
23:21 &lt;whitenoise&gt; hm...
23:22 &lt;@Mathiasdm&gt; you are of course always free to start working on website usability improvements too
23:22 &lt;eche|on&gt;  just wait for some mails with contact data to pay out some money ;-)
23:23 &lt;whitenoise&gt; well, I guess we decided to improve usability in general without any accent on bittorrent, right?
23:23 &lt;whitenoise&gt; :-)
23:23 &lt;@Mathiasdm&gt; that looks like it, yes, whitenoise 
23:23 &lt;@Mathiasdm&gt; I will mail you my bank account, eche|on, just send me the money ;)
23:23 &lt;@Mathiasdm&gt; okay then
23:23 &lt;@Mathiasdm&gt; 8) cookies for everyone who attended
23:24 &lt;eche|on&gt; *g*
23:24 &lt;@Mathiasdm&gt; ===Meeting over===
23:24 &lt;@Mathiasdm&gt; thanks all :)
23:24 &lt;eche|on&gt; COOKIES!
23:25 &lt;@Mathiasdm&gt; don't eat all of them
23:25  * Mathiasdm pokes eche|on 
</div>
