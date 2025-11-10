---
title: "I2P Dev Meeting - May 01, 2018"
date: 2018-05-01
author: "zzz"
description: "I2P development meeting log for May 01, 2018."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> anonymousmaybe, orignal, str4d, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.34 F-Droid status (str4d, meeh, nextloop)
20:00:00 &lt;zzz&gt; 2) 0.9.35 update (zzz)
20:00:00 &lt;zzz&gt; 3) NTCP2 update (zzz)
20:00:00 &lt;zzz&gt; 4) Status scrum (zab)
20:00:03 &lt;zzz&gt; 0) Hi
20:00:05 &lt;zzz&gt; hi
20:00:09 &lt;zzz&gt; 1) 0.9.34 F-Droid status (str4d, meeh, nextloop)
20:00:27 &lt;zlatinb&gt; hi
20:00:31 &lt;zzz&gt; ok I believe the only thing left for 34 is fdroid? you guys have a status?
20:00:35 &lt;orignal_&gt; hi
20:02:10 &lt;zzz&gt; ok, 3 weeks since the 34 release, lets hope it gets wrapped up soon
20:02:15 &lt;zzz&gt; anything else on 1) ?
20:03:01 &lt;zzz&gt; 2) 0.9.35 update (zzz)
20:03:08 &lt;zzz&gt; 35 is going well
20:03:29 &lt;zzz&gt; 3 weeks in, 7 weeks to go, 16K lines of diff so far. feature freeze in 1-2 weeks
20:03:57 &lt;zzz&gt; lots of good stuff in there so far. as always, need testers
20:04:12 &lt;zzz&gt; anything else on 2) ?
20:06:00 &lt;zzz&gt; 3) NTCP2 update (zzz)
20:06:20 &lt;zzz&gt; we had our 6th meeting yesterday and I did my weekly update to the proposal a couple hours ago, it's up on our site
20:06:45 &lt;zzz&gt; this pretty much wraps up the spec phase. It isn't pretty yet and it will certainly change, but the big stuff is decided
20:07:11 &lt;zzz&gt; we're now in the test implementation phase. each project should code up an implementation by the end of May, and we'll do interoperability testing in June
20:07:37 &lt;zzz&gt; we will of course continue updating the spec based on what we learn when we start coding
20:08:00 &lt;zzz&gt; so things are going quite well
20:08:15 &lt;zzz&gt; anything else on 3) ?
20:08:21 &lt;orignal_&gt; zzz, can you list out all crypto needed for ntcp2?
20:08:38 &lt;zzz&gt; please read the spec, let's not do it here, thanks
20:08:39 &lt;orignal_&gt; beside what's in I2P already
20:09:02 &lt;zzz&gt; or we can discuss n #ntcp2 after the meeting
20:09:34 &lt;orignal_&gt; it might be interesting for everybidy I thought
20:09:36 &lt;i2pr&gt; [Slack/str4d] Gah internet
20:09:41 &lt;zzz&gt; anything else on 3) ?
20:09:52 &lt;i2pr&gt; [Slack/str4d] Typing
20:10:07 &lt;i2pr&gt; [Slack/str4d] Now that we have a reasonably-stable draft spec, I'll see if I can clean it up a bit this weekend, and then I'll ask some of my cryptographer friends to look over it.
20:11:01 &lt;zzz&gt; ok
20:11:08 &lt;zzz&gt; anything else on 3) ?
20:12:02 &lt;zzz&gt; 4) Status scrum (zab)
20:12:06 &lt;zzz&gt; take it away zlatinb 
20:12:15 &lt;zlatinb&gt; Hi, before we start - Ive received funding requests from everyone except mhatta but thats due to PGP confusion
20:12:32 &lt;zlatinb&gt; so I will be sending out final approvals to ech later tonight
20:12:41 &lt;zlatinb&gt; and mhattas will end up being a little delayed
20:13:37 &lt;zlatinb&gt; ok lets start - going around the room, 1-2-3
20:13:37 &lt;zlatinb&gt; zzz: go
20:13:45 &lt;zzz&gt; ok 1) last month:
20:14:12 &lt;zzz&gt; 34 release, susimail folders, DNSoverhTTPS, SSL wizard, the group reviewed the PETS paper, new orchid release...
20:14:23 &lt;zzz&gt; NTCP2 spec, lots of meeting and planning, lots of bug fixes
20:14:30 &lt;zzz&gt; 2) next month:
20:14:51 &lt;zzz&gt; ntcp2 impl, ssl wizard finishing, lots of bug fixes, more planning and meetings
20:15:04 &lt;zzz&gt; 3) blockers: mhatta TAILS ready indication spec
20:15:06 &lt;zzz&gt; EOT
20:15:18 &lt;zlatinb&gt; ok.  str4d your turn
20:15:31 &lt;i2pr&gt; [Slack/str4d] 1) Past month:
20:15:56 &lt;i2pr&gt; [Slack/str4d] - Finished migrating I2P-Bote to the official Apache James Server release, got IMAP and SMTP working well enough to implement a service for relaying Zcash transactions, made a new release.
20:16:24 &lt;i2pr&gt; [Slack/str4d] - Finished XRDS article
20:16:33 &lt;i2pr&gt; [Slack/str4d] - Reviewed VRP draft update
20:16:40 &lt;i2pr&gt; [Slack/str4d] - Bugfixes
20:16:50 &lt;i2pr&gt; [Slack/str4d] - NTCP2 design / spec meetings
20:17:02 &lt;i2pr&gt; [Slack/str4d] - Implemented (almost all of) NTCP2 draft spec in Rust
20:17:07 &lt;i2pr&gt; [Slack/str4d] 2) Next month:
20:17:32 &lt;i2pr&gt; [Slack/str4d] - Implement last few NTCP2 corners in draft spec
20:17:46 &lt;i2pr&gt; [Slack/str4d] - Write harness to generate NTCP2 test vectors
20:17:55 &lt;i2pr&gt; [Slack/str4d] - Convince myself that SipHash is okay for length blinding
20:18:09 &lt;i2pr&gt; [Slack/str4d] - Write up AES blinding of ephemerals as a Noise extension
20:18:26 &lt;i2pr&gt; [Slack/str4d] - Work on Java implementation of Noise w/ zzz and meeh
20:18:39 &lt;i2pr&gt; [Slack/str4d] - Release stuff as necessary
20:19:32 &lt;i2pr&gt; [Slack/str4d] 3) Blockers: currently none; Friction: travel.
20:19:34 &lt;i2pr&gt; [Slack/str4d] EOT
20:20:00 &lt;zlatinb&gt; alright. meeh are you here?
20:20:49 &lt;zlatinb&gt; echelon? sadie?
20:21:31 &lt;zlatinb&gt; mhatta: you around by any chance?
20:22:06 &lt;zlatinb&gt; :(
20:22:11 &lt;anonymousmaybe&gt; sorry for interruption , but is there discussiom Q/A here ? or just listing stuff ?
20:22:39 &lt;zlatinb&gt; anonymousmaybe: SCRUM - listing stuff, discussion maybe later
20:22:39 &lt;zzz&gt; in about 30 seconds I will ask for other topics, stand by
20:23:01 &lt;zzz&gt; that it for you zlatinb ?
20:23:08 &lt;anonymousmaybe&gt; i c , thank you
20:23:09 &lt;zlatinb&gt; I guess so
20:23:36 &lt;zzz&gt; ok, maybe it's time for a stern email from you to everybody asking them to be here and be on time...
20:23:48 &lt;zzz&gt; ok thats it for 4)
20:23:57 &lt;zzz&gt; anything else for the meeting? anonymousmaybe you're up
20:24:51 &lt;anonymousmaybe&gt; i would like to ask about the implementation of DNSoverhTTPS,
20:25:34 &lt;zzz&gt; ok, that's a technical detail best discussed after the status meeting
20:25:46 &lt;zzz&gt; anything else for the meeting?
20:26:40 &lt;anonymousmaybe&gt; for me no
20:27:01 * zzz grabs the baffer
20:27:38 * zzz *bbbaffs* the meeting clased
</div>
