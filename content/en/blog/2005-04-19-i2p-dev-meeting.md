---
title: "I2P Dev Meeting - April 19, 2005"
date: 2005-04-19
author: "@jrandom"
description: "I2P development meeting log for April 19, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, cervantes, defnax, jrandom, maestro^, polecat, protokol, Ragnarok, Teal`c</p>

## Meeting Log

<div class="irc-log">
14:05 &lt;@jrandom&gt; 0) hi
14:05 &lt;@jrandom&gt; 1) Net status
14:05 &lt;@jrandom&gt; 2) SSU status
14:05 &lt;@jrandom&gt; 3) Roadmap update
14:05 &lt;@jrandom&gt; 4) Q status
14:05 &lt;@jrandom&gt; 5) ???
14:05 &lt;@jrandom&gt; 0) hi
14:05  * jrandom waves
14:05 &lt;@jrandom&gt; weekly status notes (posted a sec ago) up @ http://dev.i2p.net/pipermail/i2p/2005-April/000708.html
14:06  * maestro^ beatboxes
14:06 &lt;+cervantes&gt; evening
14:06 &lt;+protokol&gt; susi23: you there?
14:06 &lt;@jrandom&gt; while y'all read those exciting notes, lets jump on in to 1) net status
14:06 &lt;+protokol&gt; oops, meeting
14:07 &lt;@jrandom&gt; i dont really have much to add beyond what it says though.  new release tomorrow, most likely, with the fixes incorporated so far, as well as some neat new contributions
14:08 &lt;@jrandom&gt; anyone have any comments or concerns w/ the net status &&/|| the upcoming 0.5.0.7?
14:10 &lt;@jrandom&gt; if not, moving on to 2) SSU status
14:10 &lt;+maestro^&gt; i've been getting some of these errors: Wanted to build 2 tunnels, but throttled down to 0, due to concurrent requests (cpu overload?)
14:10 &lt;@jrandom&gt; ah, yeah, thats the tunnel throttling issue
14:10 &lt;+protokol&gt; will it support ftp?
14:10 &lt;@jrandom&gt; its a bit... overzealous
14:10 &lt;+protokol&gt; jk jk
14:10 &lt;@jrandom&gt; !thwap protokol 
14:10 &lt;+maestro^&gt; heh, ok
14:12 &lt;@jrandom&gt; ok, as for SSU, there's been a bunch of updates in the last week, and still further changes locally not yet committed
14:13 &lt;@jrandom&gt; i havent been making any history.txt entries for the updates though, since its not used by anyone yet, so only people on the i2p-cvs list get to read the exciting details ;)
14:14 &lt;@jrandom&gt; otoh, in the last few days after things have been pretty much working, while streamlining its operation i've found some choke points in the SDK
14:14 &lt;@jrandom&gt; (and in the jobQueue).  i've pulled those out now, locally, and testing continues.
14:15 &lt;@jrandom&gt; we may have some alphas for the SSU transport this week, more likely this weekend though
14:15 &lt;@jrandom&gt; not much more i have to say on that - anyone have any questions?
14:16 &lt;+Ragnarok&gt; how much impact did the choke points have?
14:17 &lt;@jrandom&gt; well, it varies - i'm measuring the impact upon the live net now, but on my local ssu network, two minor tweaks gave more than an order of magnitude improvement
14:17 &lt;@jrandom&gt; but i don't expect that to occur on the live net
14:17 &lt;+Ragnarok&gt; yikes
14:18 &lt;+Ragnarok&gt; heh, ok
14:18 &lt;@jrandom&gt; (at least, not until we move to 0.6 ;)
14:20 &lt;@jrandom&gt; ok, following that lead, lets move to 3) Roadmap update
14:21 &lt;@jrandom&gt; as mentioned in the notes, the dates and revs on the roadmap have been moved around.  0.5.1 dropped, with the further tunnel modifications pushed to 0.6.1
14:21 &lt;+cervantes&gt; 3) Roadmap Skew
14:21 &lt;@jrandom&gt; heh
14:22 &lt;@jrandom&gt; yeah, when you run a fast CPU, it skews the clock more frequently.  similary... ;)
14:22 &lt;@jrandom&gt; ^ry^rly
14:23 &lt;+cervantes&gt; ooh is that a hint of an ego? I never would have thought! :)
14:23 &lt;@jrandom&gt; but yeah, unfortunately, a 0.6 rev in april just isnt going to happen
14:23 &lt;@jrandom&gt; hehe
14:23 &lt;@jrandom&gt; cervantes: dont worry, its tempered by the fact that its taken 2 years to get this far ;)
14:25 &lt;@jrandom&gt; we will probably have some -X builds for people to brea^Wtest SSU on the live net while i'm offline, but there won't be a 0.6 rev until i'm back
14:25 &lt;@jrandom&gt; (and, like last year, i have no idea how long it'll take to get hooked up again, but hopefully less than a month)
14:25 &lt;+cervantes&gt; heh, if anyone here is a little deserving of self-appreciation then I guess it would be you ;-)
14:26 &lt;+polecat&gt; Where you going, jrandom ?
14:27 &lt;+cervantes&gt; $somewhere
14:27 &lt;@jrandom&gt; dunno
14:27 &lt;@jrandom&gt; (thankfully, $somewhere is a runtime expression ;)
14:27 &lt;+cervantes&gt; jrandom: do you envisage a months downtime?
14:27 &lt;+maestro^&gt; jr: walk around the neighborhood and setup a wireless relay network from someone else's link ;]
14:27 &lt;@jrandom&gt; depends on the internet situation where i end up cervantes.
14:28 &lt;@jrandom&gt; i'm quite likely to hop online occationally of course, though
14:28 &lt;+protokol&gt; polecat: lol
14:28 &lt;+cervantes&gt; I would have though you would have got the relocation class method pretty slick by now
14:28 &lt;Teal`c&gt; lets move to .6 now and work the bugs out as we go along
14:28 &lt;+cervantes&gt; *thought
14:28 &lt;+cervantes&gt; cool, Teal'c you can do Q&A
14:29 &lt;@jrandom&gt; Teal`c: "work the bugs out" == fix the code == (have a coder who knows the code to fix it)
14:29 &lt;Teal`c&gt; ya, I'd like that.
14:29 &lt;Teal`c&gt; I know some perl
14:29  * cervantes sets bugzilla&gt; tealc@mail.i2p
14:29 &lt;@jrandom&gt; word Teal`c, we can always use some help testing
14:30 &lt;@jrandom&gt; especially in automation of tests
14:31 &lt;@jrandom&gt; ok, anything else on 3) or shall we move to 4) Q status
14:31 &lt;+polecat&gt; I see.  Good luck getting stable Internet back.
14:31 &lt;+ant&gt; &lt;jrandom&gt; hrm, aum seems to be sleeping still
14:31 &lt;@jrandom&gt; thanks. i'm sure i'll find a way ;)
14:32 &lt;@jrandom&gt; ok, I don't really have much more to add beyond whats in the status notes
14:32 &lt;@jrandom&gt; aum's code is in cvs now though, so the hardcore can grab it and start hacking
14:32 &lt;+maestro^&gt; shweet
14:33 &lt;@jrandom&gt; yeah, definitely.  currently things are all GPL (since one component links against I2PTunnel), but I hear aum is working on some refactoring so it'll end up LGPL
14:34 &lt;@jrandom&gt; (but dont ask me what the implications of licensing is when it comes to xmlrpc ;)
14:34 &lt;@jrandom&gt; ok, anyone have anything on 4) to bring up?
14:36 &lt;@jrandom&gt; ok, if not, moving on to 5) ???
14:36 &lt;@jrandom&gt; anyone have anything else to bring up for the meeting?
14:36 &lt;+polecat&gt; I would like to say a few words for this occasion.
14:37 &lt;+polecat&gt; Hinkle finkle dinkle doo.
14:37 &lt;@jrandom&gt; mmmhmm.
14:37 &lt;@jrandom&gt; ok, anyone have anything to bring up in a human language?  :)
14:38 &lt;defnax&gt; what moving on 5?
14:39 &lt;+maestro^&gt; long live spacerace! long live i2p!
14:39 &lt;@jrandom&gt; hmm defnax?
14:41 &lt;defnax&gt; on 5 o'clock in the morning?
14:41 &lt;defnax&gt; in 5 hours?
14:41 &lt;+cervantes&gt; wrt xmlrpc, copyright is retained on the specification, but no restrictions placed upon implementation
14:42 &lt;@jrandom&gt; defnax: agenda item 5: "???", where we discuss other issues
14:43 &lt;+maestro^&gt; jr: have you committed those optimization changes?
14:43 &lt;@jrandom&gt; cervantes: my jab related to the question of whether using a GPL'ed app's xmlrpc API is viral (but merely a rhetorical question)
14:43 &lt;@jrandom&gt; maestro^: nope
14:43  * jrandom tests before committing
14:43 &lt;+maestro^&gt; excellent! whats your eta on that?
14:44 &lt;@jrandom&gt; later tonight, maybe, else tomorrow for the release
14:45 &lt;@jrandom&gt; ok, if there's nothing else
14:45  * jrandom winds up
14:45  * jrandom *baf*s the meeting closed
</div>
