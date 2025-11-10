---
title: "I2P Dev Meeting - June 06, 2017"
date: 2017-06-06
author: "zzz"
description: "I2P development meeting log for June 06, 2017."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> backup, lazygravy, manas, psi, str4d, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:18 &lt;zzz&gt; 0) Hi
20:00:18 &lt;zzz&gt; 1) 0.9.31 update (zzz)
20:00:18 &lt;zzz&gt; 2) UI branch status - (str4d)
20:00:18 &lt;zzz&gt; 3) I2P Summer Dev plans - (str4d)
20:00:18 &lt;zzz&gt; 4) EdDSA update - (str4d)
20:00:18 &lt;zzz&gt; 5) 34C3 planning (zzz/echelon)
20:00:18 &lt;zzz&gt; 6) Regular Reseed Operator Meetings (manas)
20:00:24 &lt;zzz&gt; 0) Hi
20:00:26 &lt;manas&gt; Hello :)
20:00:26 &lt;zzz&gt; hi
20:00:34 &lt;psi&gt; ohay
20:00:40 &lt;i2pr&gt; [Slack/str4d] Hi
20:00:58 &lt;zzz&gt; 1) 0.9.31 update (zzz)
20:01:00 &lt;backup&gt; Hi
20:01:37 &lt;zzz&gt; ok, checkin deadline in 3 1/2 weeks, we are on schedule, however most of the roadmap for 31 (which was pushed from 29 and 30) will be pushed again
20:01:54 &lt;zzz&gt; tag freeze was yesterday
20:02:03 &lt;zzz&gt; anything else on 1) ?
20:02:23 &lt;backup&gt; I sent out some reseed updates today
20:02:26 &lt;psi&gt; any noteworth changes for i2pd in .31?
20:03:01 &lt;zzz&gt; dont know whats going on in i2pd, but no i2np changes
20:03:15 &lt;zzz&gt; most of 31 will be the UI stuff (see item 2)
20:03:21 &lt;zzz&gt; anything else on 1) ?
20:03:51 &lt;psi&gt; kk
20:03:51 &lt;i2pr&gt; [Slack/str4d] The new website front-page CSS will also be landing at the same time
20:04:07 &lt;manas&gt; str4d: cool
20:04:28 &lt;zzz&gt; 2) UI branch status - (str4d)
20:04:31 &lt;zzz&gt; str4d go
20:04:33 &lt;i2pr&gt; [Slack/str4d] (and hopefully some inner CSS too, but depends on Elio's schedule)
20:04:55 &lt;i2pr&gt; [Slack/str4d] UI branch is merged!
20:05:36 &lt;i2pr&gt; [Slack/str4d] A few people have been reviewing and giving feedback; thanks for that
20:05:39 &lt;zzz&gt; I encourage everyone to test, and add their issues or non-issues to ticket #1996
20:05:59 &lt;zzz&gt; str4d, be sure to bump rev when you make changes so the comments make sense
20:06:26 &lt;i2pr&gt; [Slack/str4d] K
20:06:32 &lt;zzz&gt; anything else on 2) ?
20:06:59 &lt;i2pr&gt; [Slack/str4d] Most of the bugs have been addressed; if I get time I will try to respond to the subjective points
20:07:42 &lt;zzz&gt; 3) I2P Summer Dev plans - (str4d)
20:07:46 &lt;zzz&gt; str4d go
20:08:14 &lt;i2pr&gt; [Slack/str4d] Summer Dev launched a day late due to a website merge issue, but it's up!
20:08:46 &lt;i2pr&gt; [Slack/str4d] Now comes the fun part: working on related tasks
20:09:32 &lt;i2pr&gt; [Slack/str4d] I'll post the list of ideas to the Dev forum so people can see what is suggested
20:09:39 &lt;zzz&gt; I believe you had two meetings about it already...
20:09:57 &lt;manas&gt; I've got a script for parallel rsync transfers over Tor, I was going to rework it to run transfers over I2P :)
20:09:58 &lt;i2pr&gt; [Slack/str4d] One, no one showed up to the one last week
20:10:02 &lt;zzz&gt; what are you looking for people to do to help out?
20:10:35 &lt;zzz&gt; also, what's the PR plan?
20:11:32 &lt;i2pr&gt; [Slack/str4d] PR plan is to have a new blog post about an aspect of summer dev every couple of weeks
20:11:44 &lt;i2pr&gt; [Slack/str4d] But that heavily depends on things being worked on
20:12:07 &lt;i2pr&gt; [Slack/str4d] Metrics collection is the big one
20:12:36 &lt;manas&gt; I read the transcript from the first meeting, seems to be technical stuff that I don't really know at this point :P
20:12:45 &lt;zzz&gt; great. anything else on 3) ?
20:13:12 &lt;i2pr&gt; [Slack/str4d] Main thing is making progress
20:13:24 &lt;manas&gt; Metrics collection would be good, maybe a Java plugin where I can enter in a destination and it collects metrics and/or runs speedtests?
20:13:39 &lt;manas&gt; Not sure what was the planned direction for that
20:13:41 &lt;i2pr&gt; [Slack/str4d] Potentially, yeah
20:13:50 &lt;manas&gt; that would be cool
20:14:02 &lt;i2pr&gt; [Slack/str4d] My planned direction is metrics.torproject.org
20:14:21 &lt;i2pr&gt; [Slack/str4d] Obviously not those specific metrics
20:14:30 &lt;manas&gt; Right
20:14:41 &lt;i2pr&gt; [Slack/str4d] But a similar setup for us
20:14:59 &lt;i2pr&gt; [Slack/str4d] The key metric is tunnel / network performance
20:15:39 &lt;zzz&gt; nice goal, but everything that's easy in tor is hard for us, they have centralized control
20:15:40 &lt;i2pr&gt; [Slack/str4d] So it would be really helpful for someone to have a look at the tests that Tor runs with their bwauth code
20:15:55 &lt;i2pr&gt; [Slack/str4d] Agreed
20:16:02 &lt;manas&gt; Yeah. I think you mentioned somewhere about Tor's privacy-respecting practices for metrics collection. If there's some documentation/papers about that, it would be good to read up on
20:16:06 &lt;i2pr&gt; [Slack/str4d] But metrics is inherently going to be centralised
20:16:34 &lt;i2pr&gt; [Slack/str4d] There are some papers on freehaven.net/anonbib
20:16:45 &lt;zzz&gt; anything else on 3) ?
20:16:54 &lt;manas&gt; Thanks, I will take a look
20:16:55 &lt;i2pr&gt; [Slack/str4d] But not sure how much about their specific setup
20:17:12 &lt;i2pr&gt; [Slack/str4d] The other thing for this month is proposal work
20:17:36 &lt;zzz&gt; 4) EdDSA update - (str4d)
20:17:39 &lt;zzz&gt; str4d go
20:17:40 &lt;i2pr&gt; [Slack/str4d] I listed a bunch of proposals in the launch blog post that I thought were relevant
20:17:48 &lt;i2pr&gt; [Slack/str4d] zzz, not so fast
20:17:57 &lt;i2pr&gt; [Slack/str4d] I'm on my phone, not fast typing
20:18:20 &lt;i2pr&gt; [Slack/str4d] 3) cont.
20:18:53 &lt;i2pr&gt; [Slack/str4d] I'll be reviewing and working on proposals the rest of this month
20:19:09 &lt;i2pr&gt; [Slack/str4d] But I'd really like to see a blog post or two about some of them
20:19:18 &lt;zzz&gt; how are proposals related to summer dev which is item 3) ?
20:19:43 &lt;i2pr&gt; [Slack/str4d] Summer Dev is about speed
20:20:07 &lt;i2pr&gt; [Slack/str4d] We have several open proposals that are performance related
20:20:42 &lt;i2pr&gt; [Slack/str4d] And I'd like to see some of them communicated to the wider community
20:20:48 &lt;zzz&gt; ok
20:20:55 &lt;zzz&gt; anything else on 3) ?
20:20:56 &lt;i2pr&gt; [Slack/str4d] This would be a great task for someone newer, in fact
20:21:12 &lt;i2pr&gt; [Slack/str4d] Taking the time to read the proposal
20:21:18 &lt;i2pr&gt; [Slack/str4d] Read surrounding docs
20:21:28 &lt;i2pr&gt; [Slack/str4d] And then digest it into a blog post
20:21:37 &lt;manas&gt; str4d: task would mean reading proposals, understanding and simplifying/explaining them in a blog post?
20:21:44 &lt;manas&gt; oops your messages just came in, lag
20:21:46 &lt;manas&gt; :)
20:21:49 &lt;i2pr&gt; [Slack/str4d] Yep!
20:21:54 &lt;manas&gt; I will take a look at those proposals, str4d 
20:22:02 &lt;manas&gt; I would find that interesting
20:22:13 &lt;i2pr&gt; [Slack/str4d] Conveying what the proposal is, and why it is important for both performance and privacy
20:22:27 &lt;manas&gt; Yeah, that would be a good set of blog posts :)
20:22:37 &lt;manas&gt; and hopefully fruitful discussions would follow
20:22:45 &lt;i2pr&gt; [Slack/str4d] Exactly ;)
20:23:09 &lt;zzz&gt; anything else on 3) ?
20:23:16 &lt;i2pr&gt; [Slack/str4d] Okay, *now* I'm done with 3)
20:23:31 &lt;zzz&gt; 4) EdDSA update - (str4d)
20:23:34 &lt;zzz&gt; str4d go
20:23:43 &lt;i2pr&gt; [Slack/str4d] No movement here
20:24:04 &lt;i2pr&gt; [Slack/str4d] The branch was updated a while back with the latest code from my library
20:24:19 &lt;i2pr&gt; [Slack/str4d] But with the UI stuff, I haven't had time to review it
20:24:27 &lt;zzz&gt; carry over to next meeting, or is this item done or irrelevant?
20:25:07 &lt;i2pr&gt; [Slack/str4d] Main issue is making sure the semantic changes to the sigtypes don't break anything unexpected
20:26:07 &lt;i2pr&gt; [Slack/str4d] If someone did want to help, that would be nice, but I'd put Summer Dev higher on the priorities
20:26:32 &lt;i2pr&gt; [Slack/str4d] So I'd table for now
20:26:51 &lt;zzz&gt; carry over to next meeting, or is this item done or irrelevant?
20:27:05 &lt;i2pr&gt; [Slack/str4d] I just said
20:27:21 &lt;i2pr&gt; [Slack/str4d] Table for now, so not done nor irrelevant, but take off the agenda
20:27:27 &lt;zzz&gt; dunno what I should do with "table". Put it on agenda or not?
20:27:53 &lt;zzz&gt; ok, so test2 branch is burned, if I do any branch work I'll make a new one
20:28:02 &lt;zzz&gt; ok anything else on 4) ?
20:29:01 &lt;zzz&gt; 5) 34C3 planning (zzz/echelon)
20:29:25 &lt;zzz&gt; I don't believe ech is around. Just an early warning that we'll have budget meeting next month or august
20:29:33 &lt;manas&gt; alright
20:29:56 &lt;i2pr&gt; [Slack/str4d] ACK
20:29:57 &lt;zzz&gt; we have plenty of money to hand out, but as always we reward the contributors
20:30:16 &lt;zzz&gt; so help the project and it will help you
20:30:18 &lt;manas&gt; I was looking at flights & a hotel. Got it mostly figured out
20:30:21 &lt;zzz&gt; now is the time
20:30:26 &lt;lazygravy&gt; (especially with the crazy price of btc)
20:30:36 &lt;zzz&gt; more in the next meetings
20:30:45 &lt;manas&gt; Hotels seem to be filling up quick so if people are planning on going it's good to start looking into it ASAP
20:30:52 &lt;zzz&gt; yup
20:30:57 &lt;zzz&gt; anything else on 5) ?
20:31:03 &lt;i2pr&gt; [Slack/str4d] +1
20:32:01 &lt;zzz&gt; 6) Regular Reseed Operator Meetings (manas)
20:32:03 &lt;zzz&gt; manas go
20:32:26 &lt;manas&gt; http://zzz.i2p/topics/2341-meeting-reseed-operators-13-june-8-pm-utc-in-i2p-reseed - planning our first reseed meeting in #i2p-reseed next week, 13 June at 8PM UTC
20:32:46 &lt;manas&gt; Those are the general points of discussion, I'll be summarizing the threads referred to
20:32:59 &lt;manas&gt; See you next week, thanks :)
20:33:12 &lt;zzz&gt; great, thanks for setting that up, I encourage everyone to attend
20:33:18 &lt;zzz&gt; anything else on 6) ?
20:33:26 &lt;manas&gt; That's all
20:34:21 &lt;lazygravy&gt; Would it be out of line to circle back to (3)?
20:34:35 &lt;manas&gt; sup gravy
20:34:45 &lt;lazygravy&gt; I'm interested in the collection side str4d, could we schedule some time to talk about it? Preferably on a weekend
20:34:47 &lt;zzz&gt; 3) gravy go
20:35:00 &lt;manas&gt; Could hold a discussion in #i2p-science?
20:35:45 &lt;lazygravy&gt; manas: as long as we have a scheduled time :)
20:36:01 &lt;lazygravy&gt; don't need to decide a time now. I just wanted to get it out there
20:36:06 &lt;manas&gt; Yeah
20:36:48 &lt;manas&gt; I'd find that interesting
20:37:01 &lt;zzz&gt; anything else on 3) ?
20:37:43 &lt;lazygravy&gt; nothing more from me
20:37:48 &lt;zzz&gt; anything else for the meeting?
20:37:56 * zzz hunts for the baffer
20:39:02 * zzz *b*a*f*s* the meeting closed
</div>
