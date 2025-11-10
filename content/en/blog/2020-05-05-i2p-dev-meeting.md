---
title: "I2P Dev Meeting - May 05, 2020"
date: 2020-05-05
author: "eyedeekay"
description: "I2P development meeting log for May 05, 2020."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, eyedeekay, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
22:00:09 &lt;eyedeekay&gt; Hi everybody, welcome to the meeting for the first Tuesday of the month, and the final meeting before the 0.9.46 release. Who else is in attendance?
22:00:27 &lt;zzz&gt; hi
22:00:28 &lt;zlatinb&gt; hi
22:01:02 &lt;eyedeekay&gt; 0) Hi 
22:01:02 &lt;eyedeekay&gt; 1) 0.9.46 status/release 
22:01:03 &lt;eyedeekay&gt; 2) git migration status 
22:01:03 &lt;eyedeekay&gt; 3) reseeds
22:01:03 &lt;eyedeekay&gt; 4) misc
22:03:07 &lt;eyedeekay&gt; This is the last IRC meeting before the release of 0.9.46, tag freeze is in about a week so translated strings must be finished by then. Any remaining changes must be submitted by the final deadline on the 22nd of this month.
22:03:58 &lt;eyedeekay&gt; We are on track to do this release on time as far as I know.
22:04:15 &lt;eyedeekay&gt; For my part, In the 0.9.46 cycle, I've continued on organizational, cosmetic, and UI changes to the applications, focusing on i2ptunnel mostly. I have also been working on a tunnel rotation setting for i2ptunnel, which I will be ready to check in soon. I doubt that I will finish dynamic tunnel allocation for i2ptunnel in time for 0.9.46.
22:04:21 &lt;eyedeekay&gt; Anyone have anything to add?
22:04:38 &lt;zzz&gt; yes
22:04:52 &lt;zzz&gt; the two headline items, streaming improvements and finishing ratchet, are done
22:05:01 &lt;eyedeekay&gt; Excellent!
22:05:03 &lt;zzz&gt; testing of ratchet with i2pd is going well
22:05:08 &lt;zzz&gt; good early reports on streaming
22:05:17 &lt;zzz&gt; tweaks will continue right up to the release
22:05:28 &lt;zzz&gt; I'm now focusing mostly on bug fixes, all over
22:05:55 &lt;zzz&gt; should be on track for a release early the week of the 25th
22:05:57 &lt;zzz&gt; eot
22:06:05 &lt;eyedeekay&gt; Very good. For people following along on #ls2, this has been very exciting to watch.
22:06:22 &lt;eyedeekay&gt; zlatinb, anything on your end?
22:07:29 &lt;zlatinb&gt; just lots of streaming work, to either continue or be applied to ssu in 47
22:07:52 &lt;eyedeekay&gt; Cool then. Moving on to 2)
22:08:14 &lt;eyedeekay&gt; 2) git migration status
22:08:14 &lt;eyedeekay&gt; Git has been prepared for general use, it has been moved into a datacenter, faster hardware, and a faster connection. Settings for a new git i2ptunnel have largely been decided upon, but not checked in. New gitlab signups will be presented with a basic terms-of-service. If they cannot comply with those TOS, the option of self-hosting git services is clearly outlined. It has backups, and it has both HTTPS and .oni
22:08:14 &lt;eyedeekay&gt; o support gittorrent is still ongoing, as is the trac ticket migration. As long as we continue to use trac for issues for the time being, I believe Git is ready for full-time use if we transition after this release.
22:10:16 &lt;eyedeekay&gt; mtn history remains a sticking point for some interesting repositories
22:15:23 &lt;eyedeekay&gt; So sorry, pidgin crashed on me.
22:15:23 &lt;eyedeekay&gt; Where were we?
22:15:38 &lt;zzz&gt; "mtn history remains..."
22:20:14 &lt;eyedeekay&gt; Thank you zzz.
22:21:03 &lt;eyedeekay&gt; I don't think I have much else to say about git from my end. If no one else has any comments, we can move on to reseeds
22:21:03 &lt;eyedeekay&gt; timeout 1min
22:21:03 &lt;eyedeekay&gt; Oh right I didn't mention the HTTPS url. Our git is visible at i2pgit.org
22:21:05 &lt;eyedeekay&gt; Moving on, topic 3) reseeds
22:21:05 &lt;eyedeekay&gt; zzz you have the floor
22:21:18 &lt;zzz&gt; wait
22:21:25 &lt;eyedeekay&gt; OK
22:21:31 &lt;zzz&gt; may I have an opportunity to add some thoughts on 2) ?
22:21:37 &lt;eyedeekay&gt; Sure
22:21:51 &lt;zzz&gt; thank you
22:22:11 &lt;zzz&gt; first of all, I'm getting better at git and gitlab, and I submitted 3 MRs to muwire this weekend
22:22:21 &lt;zzz&gt; two went well, one not as much, but we're learning
22:22:30 &lt;zzz&gt; feeling much more comfortable
22:22:52 &lt;zzz&gt; second: as mentioned I think last meeting, we would greatly benefit from a plan and a schedule on the migration
22:23:00 &lt;zzz&gt; I don't think one is posted anywhere
22:23:23 &lt;zzz&gt; in particular what branches when, and so on
22:23:23 &lt;zzz&gt; eot
22:27:42 &lt;eyedeekay&gt; Oh shoot that did not make it to the thread. We did discuss a schedule which included shifting things that were not i2p.i2p to git before i2p.i2p itself. That needs to be made available before we finish the transition. I will post it tonight. Thank you zzz for the reminder and for giving git a chance.
22:27:42 &lt;eyedeekay&gt; Anything else on 2) from anybody?
22:28:58 &lt;eyedeekay&gt; OK then 3) reseeds
22:29:04 &lt;zzz&gt; thank you
22:29:16 &lt;zzz&gt; I want to put out an urgent call for more reseeds
22:29:33 &lt;zzz&gt; meeh runs 3 of our 10, and all 3 were down for about two weeks. One came back.
22:29:43 &lt;zzz&gt; and the other two are still down, for different reasons
22:29:52 &lt;zzz&gt; he is unresponsive
22:30:12 &lt;zzz&gt; it's not a good situation. If they're still down in 2 weeks I'll remove them before the release
22:30:16 &lt;zzz&gt; and we'll be down to 7 or 8
22:30:39 &lt;zzz&gt; reseeds that are down result in a terrible new-user experience, it's unacceptable
22:31:12 &lt;zzz&gt; anybody that wants to run one please contact me
22:31:24 &lt;fug&gt; make running reseeds easier, then people will run them
22:31:26 &lt;zzz&gt; it would be nice to have one from biglybt or other i2p-adjacent organizations
22:31:45 &lt;zzz&gt; sure, could always be better
22:32:08 &lt;zzz&gt; unfortunately the person managing our reseeds and the software vanished last year, so that's unstaffed also
22:32:11 &lt;eyedeekay&gt; fug what qualifies as easier? That would be a job for me, I'm the Go guy, I'd be happy to dockerize it or make it checkinstallable or go get-able or whatever.
22:32:16 &lt;zzz&gt; EOT
22:32:44 &lt;zzz&gt; reseed plugin he also left half-done
22:32:47 &lt;fug&gt; eyedeekay: docker image would be good
22:33:03 &lt;eyedeekay&gt; Cool, I'll post it here in a day or two.
22:33:29 &lt;fug&gt; but something like a simple, single application that would do the reseeding with little to no required setup would be even better
22:35:50 &lt;eyedeekay&gt; That's pretty close to what the Go reseed is, although I'll admit there are some rough edges. I'll start with Docker.
22:36:01 &lt;eyedeekay&gt; Anything else on 3)?
22:36:23 &lt;zzz&gt; no. thanks for adding it to the agenda
22:36:48 &lt;eyedeekay&gt; You're welcome, no problem. 4) misc
22:39:29 &lt;eyedeekay&gt; I want to thank dr|zed for contributing the improved CSS for my personal web sites, I really appreciate the thought that was put into it. I also managed to get a little design advice on my WebExtension. Anybody doing something cool or exciting?
22:40:53 &lt;eyedeekay&gt; (That hasn't been mentioned elsewhere?)
22:42:04 &lt;eyedeekay&gt; timeout 1m
22:43:47 &lt;eyedeekay&gt; If no one else has anything to add, I'm going to go ahead and close the meeting.
22:44:49 &lt;eyedeekay&gt; All right *bafs*. Thanks everybody for coming and contributing to the meeting, see you around IRC
</div>
