---
title: "I2P Dev Meeting - November 05, 2019"
date: 2019-11-05
author: "zzz"
description: "I2P development meeting log for November 05, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, eyedeekay, lbt, sadie, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.43 release status (zzz)
20:00:00 &lt;zzz&gt; 2) I2P Browser project status (sadie, meeh)
20:00:00 &lt;zzz&gt; 3) Outproxy use cases / status (sadie)
20:00:00 &lt;zzz&gt; 4) 0.9.44 development status (zzz)
20:00:00 &lt;zzz&gt; 5) Proposals status (zzz)
20:00:00 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:00:04 &lt;zzz&gt; 0) Hi
20:00:06 &lt;zzz&gt; hi
20:00:10 &lt;sadie_&gt; hi
20:00:25 &lt;zzz&gt; 1) 0.9.43 release status (zzz)
20:00:38 &lt;zzz&gt; 43 has been out a couple weeks, no serious issues so far
20:01:02 &lt;zzz&gt; the remaining items are the official f-droid (nextloop) and official debian (mhatta)
20:01:08 &lt;eyedeekay&gt; hi
20:01:37 &lt;zzz&gt; any other outstanding issues with the 43 release?
20:03:01 &lt;zzz&gt; 2) I2P Browser project status (sadie, meeh)
20:03:16 &lt;zzz&gt; meeh, sadie, what's the latest info on the browser?
20:04:49 &lt;sadie_&gt; Beta 7 has been released
20:05:10 &lt;eyedeekay&gt; I2P Browser was Beta 7 was released yesterday, along with an updated road-map. This is the second-to-last release which will be based on firefox 60. We fixed some bugs and implemented continuous integration, as well as developed a revised and updated plan for the future of the browser as a product.
20:05:11 &lt;sadie_&gt; the notes can be found on the project website.
20:05:35 &lt;zzz&gt; the release date is wrong on the site FYI
20:05:51 &lt;eyedeekay&gt; Oh shoot, sorry I missed that. Will change it immediately.
20:06:03 &lt;sadie_&gt; We have also been working on the roadmap, which can also be found on the project website
20:06:29 &lt;zzz&gt; what can you tell us about upcoming beta 8? what's in it, when will it be out?
20:07:40 &lt;sadie_&gt; beta 8 will be out at the end of November. 
20:08:19 &lt;zzz&gt; anybody have any questions about the browser? meeh you have anything to add?
20:08:27 &lt;eyedeekay&gt; Beta 8 will be released at the end of November, it will be the final version based on Firefox 60. We're preparing for some architectural changes which will make applications more visible, you'll start to see the beginnings of that in Beta 8, as well as more feedback in the browser about the readiness of the bundled router.
20:08:53 &lt;sadie_&gt; we are working on a better landing page, an HTTP proxy readiness indicator , and dynamic themes
20:09:20 &lt;zzz&gt; sounds great, I hope everybody gives beta 7 a try
20:09:45 &lt;zzz&gt; anything else on 2) ?
20:11:00 &lt;zzz&gt; 3) Outproxy use cases / status (sadie)
20:11:17 &lt;zzz&gt; sadie_, what's the latest on this topic?
20:11:32 &lt;sadie_&gt; We have brought the requirements document along as far as I feel we can without now doing more user research. 
20:11:38 &lt;sadie_&gt; Mid month I will reconnect with the person who inspired the turnkey outproxy solution. We can evaluate the requirements document that has been created, and begin to address the user research questions more thoroughly. The requirements for this solution are part of the deliverables for the next release.We have brought the requirements document along as far as I feel we can without now doing more user
20:11:38 &lt;sadie_&gt;  research. 
20:12:41 &lt;zzz&gt; ok, to be clear we're only working on requirements during the 44 timeframe. Any implementation would be in 45 or later, right?
20:12:53 &lt;sadie_&gt; correct
20:13:32 &lt;zzz&gt; ok, anything else you want to add? Anybody have any questions about the outproxy research?
20:14:01 &lt;zzz&gt; anything else on 3) ?
20:15:01 &lt;zzz&gt; 4) 0.9.44 development status (zzz)
20:15:23 &lt;zzz&gt; we're two weeks in to the .44 cycle, with lots of new code checked in
20:15:52 &lt;zzz&gt; almost all is the implementation of proposal 144, new encryption for destinations
20:16:07 &lt;zzz&gt; I expect to start interoperability testing with chisana_ soon
20:16:35 &lt;zzz&gt; and should be ready for brave testers in a couple weeks
20:16:57 &lt;zzz&gt; but it will be quite a while before we're using it by default, perhaps 6-12 months
20:17:23 &lt;zzz&gt; lots of testing and other changes needed to make it solid
20:17:59 &lt;zzz&gt; the other major thing I have queued up for .44 is some SSU performance improvements, spurred on by our prolific trac ticker 'jogger'
20:18:17 &lt;zzz&gt; sadie_, eyedeekay, meeh, anything you'd like to add on what you're working on for .44 ?
20:19:34 &lt;zzz&gt; anything else on 4) ?
20:19:35 &lt;sadie_&gt; router console /home changes, website long term strategy 
20:20:45 &lt;zzz&gt; 5) Proposals status (zzz)
20:21:05 &lt;zzz&gt; not much else to say here, 99% of the focus is on 144.
20:21:30 &lt;zzz&gt; next up is probably 152, 153, or maybe even a new SSU 2 proposal
20:21:47 &lt;zzz&gt; I don't expect much progress on any of that until the new year
20:21:58 &lt;zzz&gt; any questions on proposals?
20:22:06 &lt;zzz&gt; anything else on 5) ?
20:23:01 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:23:12 &lt;zzz&gt; I think zlatinb said he couldn't make it today
20:23:32 &lt;eche|on&gt; new server with new hardware and new IPs, migrating services from one server to another with time. no blockers
20:23:41 &lt;zzz&gt; so everybody you know the drill, please say 1) what you did last month 2) what you're doing next month; 3) any blockers
20:23:52 &lt;zzz&gt; and end with EOT
20:24:49 &lt;zzz&gt; me: 1) got the .44 release out, lots of work on new encryptoin; 2) more work on new encryption, SSU performance improvements, bug fixes; 3) no blockers; EOT
20:25:11 &lt;zzz&gt; sadie_, meeh, eyedeekay, please go in parallel
20:25:48 &lt;sadie_&gt; Last month and the upcoming month I will continue to work on I2P browser, keep refining the router console light theme, and develop a long term strategy for website with IDK. Outproxy product management and requirements gathering will continue. Proposals for research and development: proposals to improve UX and usability studies have been submitted or are otherwise being written. Presentation and wo
20:25:48 &lt;sadie_&gt; rkshops for conferences have started for 2020.
20:27:01 &lt;zzz&gt; last call eyedeekay meeh zlatinb 
20:27:11 &lt;eyedeekay&gt; 1) I have been working on things that go into the browser or which are intended to help the browser. 2) Going to work on improving the organization of some of the router console home pages as well as implement some of the browser design improvements. 3 No blockers EOT
20:27:53 &lt;zzz&gt; ok, presuming EOTs from eche|on and sadie_ ... anything else on 6) ?
20:28:02 &lt;sadie_&gt; yes
20:28:34 &lt;zzz&gt; any other topics or questions for the meeting?
20:28:59 &lt;eche|on&gt; what abouit bote?
20:29:04 &lt;eche|on&gt; any sign from str4d?
20:29:28 &lt;zzz&gt; I've seen an occasional RT on twitter, so he's alive
20:29:59 &lt;zzz&gt; thats all I know
20:30:26 &lt;zzz&gt; other than what's in the tickets
20:30:27 &lt;eche|on&gt; ok
20:30:38 &lt;zzz&gt; anything else about bote?
20:31:01 &lt;zzz&gt; anything else for the meeting?
20:31:22 &lt;lbt&gt; A "thank you" to all of you :)
20:31:48 &lt;zzz&gt; you're welcome lbt, thanks for joining the meeting
20:31:54 &lt;eyedeekay&gt; You're welcome friend :)
20:33:00 * zzz *bafs* the meeting closed
</div>
