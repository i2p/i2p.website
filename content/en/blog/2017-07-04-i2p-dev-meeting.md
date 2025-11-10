---
title: "I2P Dev Meeting - July 04, 2017"
date: 2017-07-04
author: "zzz"
description: "I2P development meeting log for July 04, 2017."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> backup, manas, orignal, R4SAS, str4d, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.31/.32 update (zzz)
20:00:00 &lt;zzz&gt; 2) 34C3 planning (zzz/echelon)
20:00:03 &lt;zzz&gt; 0) Hi
20:00:06 &lt;zzz&gt; Hi
20:00:27 &lt;backup&gt; Hi zzz
20:00:31 &lt;zzz&gt; 1) 0.9.31/.32 update (zzz)
20:00:45 &lt;str4d&gt; Hi
20:00:49 &lt;zzz&gt; OK, we pushed the release out a week, new checkin deadline this friday
20:00:53 &lt;R4SAS&gt; Hi
20:00:56 &lt;manas&gt; Hello
20:01:18 &lt;zzz&gt; we'll take a couple extra days for review, since it's so big, with a review deadline of next tuesday, and a build late tuesday or early wednesday
20:01:47 &lt;zzz&gt; that puts 0.9.32 release in early to mid September, more or less as planned
20:02:04 &lt;zzz&gt; everybody please test the latest dev build
20:02:11 &lt;zzz&gt; anything else on 1) ?
20:02:33 &lt;backup&gt; it is possible that you push the guide on zzz on how to use build dev's
20:02:55 &lt;manas&gt; 'ant updater' generates i2pupdate.zip
20:02:55 &lt;zzz&gt; there should be instructions on bobthebuilder.i2p maybe?
20:03:14 &lt;orignal_&gt; hi
20:03:16 &lt;zzz&gt; search around on zzz.i2p for how to subscribe to auto dev build updates
20:03:29 &lt;str4d&gt; There's probably already a guide there, but definitely we need to improve visibility of these kinds of things. It's part of my brief for the next phase of the website udpate
20:03:38 &lt;zzz&gt; or as manas says, ant updater, copy zip over, restart. done and done.
20:03:41 &lt;backup&gt; I mean something ready like KYTV did ? 
20:03:41 &lt;zzz&gt; anything else on 1) ?
20:03:49 &lt;backup&gt; would attract more testers...
20:04:06 &lt;str4d&gt; New website frontpage is up
20:04:10 &lt;str4d&gt; http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/en/
20:04:23 &lt;zzz&gt; let's stay on topic. anything else on 1) ?
20:04:34 &lt;str4d&gt; zzz, I *am* on topix
20:04:58 &lt;str4d&gt; I'd like to have this live around release time ideally
20:05:15 &lt;str4d&gt; But the blocker is working on the copy (front page text)
20:05:18 &lt;manas&gt; Loading
20:05:30 &lt;zzz&gt; 2) 34C3 planning (zzz/echelon)
20:05:38 &lt;manas&gt; looks nice so far
20:05:50 &lt;str4d&gt; Not going to force it though, would prefer it be right than on-time
20:05:59 &lt;zzz&gt; ok, I don't want to do much discussion about CCC now, but rather to schedule the budget meeting for either august or september
20:06:25 &lt;zzz&gt; is there anybody that needs to know how much the reimbursement will be before buying plane tickets? when are people buying tickets?
20:06:27 &lt;str4d&gt; Have ticket sale times been announced yet?
20:06:48 &lt;zzz&gt; no, and realistically, you'll have to buy plane tickets months before you know if you have a conference ticket, sadly
20:06:57 &lt;manas&gt; I'm tracking a couple of tickets, have not finalized yet
20:07:12 &lt;manas&gt; What will the process for ticket procurement be like?
20:07:19 &lt;zzz&gt; I'd expect at least as much reimbursement as last year, maybe more, due to BTC
20:07:25 &lt;manas&gt; eche|off kindly sent me at ticket last year
20:07:30 &lt;manas&gt; *a
20:07:34 &lt;zzz&gt; let's not discuss the conference ticket process now. that will be much later.
20:07:43 &lt;str4d&gt; I'll be flying from the UK, so will be significantly cheaper for me to reach it
20:07:44 &lt;manas&gt; okay :)
20:07:48 &lt;zzz&gt; I just want to set a budget meeting. August or September?
20:07:59 &lt;manas&gt; str4d: and a much shorter flight :D
20:08:09 &lt;manas&gt; When are ticket sales open?
20:08:16 &lt;zzz&gt; let's not discuss the conference ticket process now. that will be much later.
20:08:33 &lt;str4d&gt; August is probably safer
20:08:40 &lt;manas&gt; either month works with me
20:08:49 &lt;zzz&gt; most of the sales were in november iirc? you'll want to get plane tix much earlier. LEJ looks harder to get to than MUC
20:08:49 &lt;str4d&gt; Perhaps with some overflow built in?
20:09:05 &lt;zzz&gt; ok I'll put it on the agenda for next month's meeting
20:09:06 &lt;manas&gt; there are a couple of flights from MUC
20:09:07 &lt;manas&gt; to LEJ
20:09:14 &lt;manas&gt; if someone is flying in to MUC
20:09:19 &lt;manas&gt; okay
20:09:19 &lt;zzz&gt; anything else on 2) ?
20:10:14 &lt;zzz&gt; anything else for today's meeting?
20:10:56 &lt;str4d&gt; I've been discussing more performance stuff in #i2p-science with various people
20:11:05 &lt;manas&gt; new frontpage loaded, looks really nice str4d
20:11:12 &lt;str4d&gt; Make sure to lurk if you are interested and haven't already
20:11:22 &lt;manas&gt; I have been testing the UI, it looks good as well
20:11:43 &lt;zzz&gt; good stuff
20:11:45 &lt;str4d&gt; I've also pushed an update to Prop140 in light of the confusion it caused, starting to clarify that it is about the balancer protocol
20:11:58 &lt;str4d&gt; (so basically OnionBalance but compartmentalised)
20:12:07 &lt;R4SAS&gt; zzz, q. about bug in jks2pem
20:12:29 &lt;zzz&gt; ok, hard to restart that discussion after 6 weeks, but I'll try to get my head back in it
20:12:30 &lt;str4d&gt; Not complete, the protocol etc. still needs designing - see my comments on the zzz.i2p thread
20:12:35 &lt;zzz&gt; R4SAS, after the meeting please
20:12:44 &lt;zzz&gt; anything else for today's meeting?
20:12:44 &lt;R4SAS&gt; kk
20:12:50 &lt;str4d&gt; I also had a few comments on NTCP 2 from David Fifield, one of the PT people
20:13:36 &lt;zzz&gt; any progress on proposals is good, even if it's only every 6 months
20:13:44 &lt;str4d&gt; I updated the proposal with them, and will shortly post it for comment to the traffic-obf Google Group (which he said would be interested in this kind of thing)
20:13:53 &lt;zzz&gt; anything else for today's meeting? /me grabs the baffer
20:14:11 &lt;str4d&gt; One last thing
20:14:34 &lt;str4d&gt; F3real has been working away on differential privacy for statistics
20:14:49 &lt;str4d&gt; He sent me today his current patch file, which I will look at later this week
20:15:14 &lt;str4d&gt; (tl;dr binning and additive noise for stats, to make it safer to publish them without compromising privacy)
20:15:42 &lt;zzz&gt; tough topic, lots of room for research and experiments. hopefully lazygravy can get involved
20:15:54 &lt;zzz&gt; anything else for today's meeting?
20:15:59 &lt;str4d&gt; Early stages, but AFAIK they are our first new contributor coming in via Summer Dev! Woo!
20:16:43 &lt;str4d&gt; I did some research a week or two ago around Apache Kafka too, looks like it would be a useful platform for stats collection
20:17:06 &lt;str4d&gt; (suggested by lazygravy, seems several people I know through infosec companies use it)
20:17:27 &lt;zzz&gt; last call for today's meeting
20:17:28 &lt;str4d&gt; Will kick that around at some stage (probably after PETS - I still have to write my talk for that)
20:17:40 &lt;str4d&gt; Okay, okay, I'm done :P
20:18:29 * zzz **bafs** the meeting closed
</div>
