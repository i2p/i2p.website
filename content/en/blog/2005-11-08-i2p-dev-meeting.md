---
title: "I2P Dev Meeting - November 08, 2005"
date: 2005-11-08
author: "jrandom"
description: "I2P development meeting log for November 08, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, dust, frosk, jrandom, reliver, tealc\_, ZipTie</p>

## Meeting Log

<div class="irc-log">
15:21 &lt;jrandom&gt; 0) hi
15:21 &lt;jrandom&gt; 1) Net status / short term roadmap
15:21 &lt;jrandom&gt; 2) I2Phex
15:21 &lt;jrandom&gt; 3) I2P-Rufus
15:21 &lt;jrandom&gt; 4) I2PSnarkGUI
15:21 &lt;jrandom&gt; 5) Syndie
15:22 &lt;jrandom&gt; 6) ???
15:22 &lt;jrandom&gt; 0) hi
15:22  * jrandom waves
15:22 &lt;jrandom&gt; weekly status notes up at http://dev.i2p.net/pipermail/i2p/2005-November/001206.html
15:22  * bar mumbles greetings from behind his/her false(?) beard
15:23 &lt;jrandom&gt; ok, jumping into 1) Net status / short term roadmap
15:23 &lt;jrandom&gt; Not much to say beyond whats in the mail - hopefully a new release later this week, or this weekend
15:24 &lt;jrandom&gt; there are some new optimizations in cvs which should help improve reliability, and its worked pretty well in the tests i've done, but it probably won't have much of an impact until it gets widespread deployment
15:25 &lt;jrandom&gt; I also haven't picked an arbitrary throughput level I want to reach before continuing on to 0.6.2, though my gut instinct tells me that optimizations should continue until I can justify the choke points by per-router hop delays
15:26 &lt;jrandom&gt; right now, however, that isn't our choke point, so there's still work to be done.
15:26 &lt;jrandom&gt; I don't have much more to add on that front - anyone have any questions/comments/concerns?
15:28 &lt;jrandom&gt; ok, if not, moving on to 2) I2Phex
15:28 &lt;jrandom&gt; I don't have much more to add here beyond whats been said in the email.  There have been a bunch of discussions on the forum too, though, so swing by there for more news and ranting 
15:31 &lt;jrandom&gt; ok, if not, jumping on over to 3) I2P-Rufus
15:31 &lt;jrandom&gt; this bullet point was really just me repeating a rumor, but we'll see how things go
15:32 &lt;jrandom&gt; Rawn / defnax: do you have anything to add?
15:35 &lt;tealc_&gt; whats i2p-rufus ?
15:35 &lt;jrandom&gt; a port of the rufus bittorrent client for I2P (http://rufus.sourceforge.net/)
15:36 &lt;jrandom&gt; ok, if there's nothing else, we can jump to another quick rumor reportage - 4) I2PSnarkGUI
15:37 &lt;jrandom&gt; I don't have much to add to this beyond saying "hey, cool" :)
15:38 &lt;+bar&gt; yeah, looks nice
15:38 &lt;@frosk&gt; snark is Y.A. BT client?
15:38 &lt;jrandom&gt; yeah, but snark is a bittorrent client bundled with I2P :)
15:38 &lt;@frosk&gt; oh yeah, right :)
15:38 &lt;jrandom&gt; (currently a command line tool, but multitorrent and web interface is on the way, though not imminent)
15:39 &lt;+fox&gt; &lt;ZipTie&gt; who was doing the work for the rarest-first fetching strategy for snark? did that ever get done?
15:39 &lt;jrandom&gt; yeah, Ragnarok implemented that
15:39 &lt;jrandom&gt; its in the current I2PSnark
15:39 &lt;+fox&gt; &lt;ZipTie&gt; cool
15:40 &lt;jrandom&gt; aye, quite
15:41 &lt;+fox&gt; &lt;ZipTie&gt; is i2p-bt going to be decomissioned then in favor of either rufus or snark?
15:41 &lt;jrandom&gt; thats for users to decide
15:42 &lt;+fox&gt; &lt;ZipTie&gt; or maintainability :)
15:42 &lt;jrandom&gt; personally, I think if snark gets a web interface, integrated with the router console, multitorrent capabilities, and offers equivilant performance as the others, it'll be in good shape
15:43 &lt;jrandom&gt; but really, what you mention is the key - who does the maintenance and development is the driving force
15:43  * jrandom does not maintain python apps
15:44 &lt;jrandom&gt; ok, if there's nothing else on 4, lets move on to 5) Syndie
15:45 &lt;jrandom&gt; I've been doing some usability research into how best to proceed, and I think we've got a pretty viable UI on the way, but if you've got an opinion, post it up on syndie or the forum and we can hopefully take it into consideration
15:46 &lt;tealc_&gt; ahh, i thought i2phex was java.. the stuff on the forums offers .exe installers and .exe's in zips
15:47 &lt;jrandom&gt; i2phex is java
15:47 &lt;jrandom&gt; and the .exe works with any platform that java works on
15:47 &lt;jrandom&gt; java -jar i2phex.exe
15:47 &lt;jrandom&gt; (yes, really)
15:49 &lt;jrandom&gt; (cough)
15:49 &lt;jrandom&gt; dust: anything to add re: syndie stuff?
15:50 &lt;dust&gt; nope
15:50 &lt;jrandom&gt; ok cool.  unless anyone else has anything on it, lets jump to ol' faithful: 6) ???
15:50 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
15:53 &lt;+fox&gt; &lt;reliver&gt; is the paella ready ? ;-)
15:53  * jrandom grabs a spork
15:54 &lt;jrandom&gt; (on that note...)
15:54 &lt;+fox&gt; &lt;reliver&gt; and the cat still smells like cats ;?)
15:54  * jrandom windos up
15:54  * jrandom *baf*s the meeting closed
</div>
