---
title: "I2P Dev Meeting - July 03, 2018"
date: 2018-07-03
author: "zzz"
description: "I2P development meeting log for July 03, 2018."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, str4d, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.35 release status (zzz)
20:00:00 &lt;zzz&gt; 2) NTCP2 update (zzz)
20:00:00 &lt;zzz&gt; 3) LS2 meeting announcement (zzz)
20:00:00 &lt;zzz&gt; 4) 2H 2018 funding program (zab/zzz)
20:00:00 &lt;zzz&gt; 5) Status scrum (zab)
20:00:05 &lt;zzz&gt; 0) Hi
20:00:07 &lt;zzz&gt; Hi
20:00:16 &lt;zlatinb&gt; hi
20:00:21 &lt;zzz&gt; 1) 0.9.35 release status (zzz)
20:00:42 &lt;zzz&gt; 35's been out for a week, no major complaints so far
20:01:03 &lt;zzz&gt; maven jars are up, I believe meeh will have android out shortly
20:01:20 &lt;zzz&gt; haven't heard from mhatta yet re: official debian
20:01:57 &lt;zzz&gt; anything else on 1) ?
20:02:44 &lt;zzz&gt; 2) NTCP2 update (zzz)
20:03:04 &lt;zzz&gt; we finished up the spec last week, and we have several routers live on the network
20:03:26 &lt;zzz&gt; i2pd is proceeding with their implementation and testing
20:03:30 &lt;eche|on&gt; good so far
20:03:52 &lt;zzz&gt; I have some cleanups to do, and I haven't tested the firewalled flavor yet, but things are going pretty well
20:04:21 &lt;zzz&gt; I also posted a quick FAQ today on our forums
20:04:43 &lt;zzz&gt; anything else on 2) ?
20:05:37 &lt;zzz&gt; 3) LS2 meeting announcement (zzz)
20:06:01 &lt;zzz&gt; we're going to follow the same process for the next proposal, which is 123 "LS2"
20:06:15 &lt;zzz&gt; also covering new crypto, service lookup, massive multihoming, and related topics
20:06:36 &lt;zzz&gt; the first meeting will be Monday July 9 at 7 PM UTC in #ls2
20:06:45 &lt;eche|on&gt; great task, lots of jobs to do
20:07:05 &lt;zzz&gt; yeah, have no idea how it's going to go, but we need to get started, been too long
20:07:30 &lt;zzz&gt; anything else on 3) ?
20:07:44 &lt;eche|on&gt; nope
20:08:23 &lt;zzz&gt; 4) 2H 2018 funding program (zab/zzz)
20:08:32 &lt;zzz&gt; announcement is up on i2pforum.i2p and zzz.i2p
20:08:42 &lt;zzz&gt; the program is open to new applicants
20:08:51 &lt;zzz&gt; deadline is Wednesday July 25
20:09:13 &lt;zzz&gt; if anybody has any questions, you can ask them now, or after the meeting
20:09:34 &lt;zzz&gt; anybody have any questions about the program?
20:09:38 &lt;eche|on&gt; one point: not the whole i2p team needs to approve new members (the team is not yet perfectly defined, as in team of noted persons on webpage or any other group)
20:10:13 &lt;zlatinb&gt; I would think at least those already on the paid program
20:10:42 &lt;zzz&gt; true, I guess collectively we need to approve... not that we need individual approval from each
20:10:45 &lt;eche|on&gt; yeah
20:10:50 &lt;zzz&gt; does that sound right?
20:10:58 &lt;eche|on&gt; just to want point this out to sharpen that point
20:11:12 &lt;zzz&gt; ok
20:11:26 &lt;zzz&gt; anything else on 4) ?
20:12:18 &lt;zzz&gt; 5) Status scrum (zlatinb)
20:12:24 &lt;zzz&gt; all yours zlatinb 
20:12:59 &lt;zlatinb&gt; hi.  Lets go around the room and do the usual : 1) what youve been doing last month 2) what you plan to do next month 3) any blockers or help needed
20:13:03 &lt;zlatinb&gt; zzz: go first
20:13:33 &lt;zzz&gt; 1) NTCP2 meetings, proposal, spec, implementation and testing; .35 release; bug fixes and triage
20:14:02 &lt;zzz&gt; merging NTCP2 into trunk; merging EdDSA updates from github to trunk; roadmap updates
20:14:30 &lt;zzz&gt; 2) NTCP2 testing, bug fixes, and other things for .36; start LS2 meetings, research, planning
20:14:39 &lt;zzz&gt; 3) no blockers
20:14:40 &lt;zzz&gt; EOT
20:14:55 &lt;zlatinb&gt; eche|on: what about you?
20:15:38 &lt;eche|on&gt; Doing the services in web, administer the forum, doing financial stuff, helping with the release
20:16:02 &lt;eche|on&gt; kepp doing that stuff, no blockers yet
20:16:23 &lt;zlatinb&gt; Irc2PGuest44785: meeh I know that is you, are you here?
20:16:43 &lt;zlatinb&gt; looks like no
20:16:48 &lt;zlatinb&gt; str4d: are you here?
20:17:01 &lt;str4d&gt; 1) NTCP2 design. 2) LS2 research and design. 3) I have no room for anything else.
20:17:19 &lt;zlatinb&gt; cool, good to see you man
20:17:49 &lt;zlatinb&gt; sadie isnt here, manas is exempt, so that leaves me:
20:17:49 &lt;zlatinb&gt; 1) lots and lots of profiling, experiments, capacity improvements
20:17:49 &lt;zlatinb&gt; 2
20:17:52 &lt;zlatinb&gt; havent decided yet
20:17:54 &lt;zlatinb&gt; 3) not really
20:18:14 &lt;zlatinb&gt; I think thats everyone
20:18:33 &lt;zlatinb&gt; zzz: back to you
20:18:37 &lt;zzz&gt; ok, that went quickly. anything else for the meeting?
20:20:01 * zzz baffs the meeting closed
</div>
