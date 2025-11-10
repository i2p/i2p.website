---
title: "I2P Dev Meeting - December 06, 2018"
date: 2018-12-06
author: "zzz"
description: "I2P development meeting log for December 06, 2018."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> alex, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.38 dev status (zzz)
20:00:00 &lt;zzz&gt; 2) LS2 status (zzz)
20:00:00 &lt;zzz&gt; 3) 35c3 state (echelon)
20:00:00 &lt;zzz&gt; 4) Status scrum (zlatinb)
20:00:03 &lt;zzz&gt; 0) Hi
20:00:05 &lt;zzz&gt; hi
20:00:08 &lt;zlatinb&gt; hi
20:00:13 &lt;zzz&gt; 1) 0.9.38 dev status (zzz)
20:00:32 &lt;zzz&gt; 38 is shaping up to be a very big release, we already have over 30k lines of diff
20:01:03 &lt;zzz&gt; checked in so far are the basics for the new wizard, the new geoip implementation, and initial LS2 support
20:01:26 &lt;zzz&gt; 37 is running very smoothly with 75% or more of the network running it, no NTCP2 problems reported
20:01:55 &lt;zzz&gt; the icons and CSS changes should start to show up next week
20:02:21 &lt;zzz&gt; our plans are for a late-january release. With a couple weeks off for the holidays, there's still a lot to do between now and then
20:02:26 &lt;zzz&gt; but it's all going smoothly so far
20:02:50 &lt;zzz&gt; I encourage all of you to test a dev build from bobthebuilder.i2p, or build it yourself
20:03:08 &lt;zzz&gt; we need testers as there's a lot of changes, we need to catch the issues now, not after the release
20:03:15 &lt;zzz&gt; anything else on 1) ?
20:04:16 &lt;zzz&gt; 2) LS2 status (zzz)
20:04:47 &lt;zzz&gt; we had our 19th weekly meeting yesterday. The basic LS2 part is done and I'm working on implementing it for 38
20:05:28 &lt;zzz&gt; right now we're doing two things in parallel - working on the encrypted LS2 spec, and starting work on proposal 144, which defines a new crypto and end-to-end protocol that relies on LS2
20:05:43 &lt;zzz&gt; encrypted LS2 should be wrapped up shortly.
20:06:24 &lt;zzz&gt; proposal 144, which we call ECIES-X25519-AEAD-ratchet, is quite complex and I think will take a month or two to shake out
20:06:41 &lt;zzz&gt; meetings are mondays 7:30 UTC in #ls2, all are welcome
20:06:55 &lt;zzz&gt; anything else on 2) ?
20:08:00 &lt;zzz&gt; 3) 35c3 state (echelon)
20:08:17 &lt;zzz&gt; I believe echelon can't make it here today
20:08:46 &lt;zzz&gt; I do know he's working on a tabletop banner solution, and sweets to give away, and he bought all our tickets
20:08:56 &lt;zzz&gt; so I think we're in good shape, see you all there in 3 weeks
20:09:01 &lt;zzz&gt; anything else on 3) ?
20:09:51 &lt;zzz&gt; oh, and a reminder, we will not have a meeting here on January 1, our meetings will be at CCC. The next meeting here will be Feb. 5
20:10:11 &lt;zzz&gt; 4) Status scrum (zlatinb)
20:10:15 &lt;zzz&gt; take it away zlatinb 
20:10:28 &lt;zlatinb&gt; Hi.  Were going to do the scrum in parallel as its easy to follow on IRC anyway.  Just start typing 1) what have you been up to the last month 2) what you plan to do next month 3) any blockers or help needed.  Finish your report with EOT
20:10:56 &lt;zzz&gt; ok lets see how this goes...
20:11:10 &lt;alex_the_designerr&gt; alex i really love hexagons here :  icon work is progressing as zzz mentioned in 1)
20:11:30 &lt;alex_the_designerr&gt; last month i did website updates and some logo work
20:11:48 &lt;zlatinb&gt; 1) Work on onboarding, mainly wizard, and windows firefox installer with IDK.  Got a signing certificate so our windows installers can be signed.  Small experimental hacks on snark
20:12:09 &lt;alex_the_designerr&gt; next month i will finalize the initial drop of the new website, land icons, and *hopefully* get a blessing on a new logo
20:12:21 &lt;zlatinb&gt; 2) Wrap up the windows firefox profile insttaller and the wizard work for 0.9.38
20:12:32 &lt;alex_the_designerr&gt; stretch goals of personas and patterns
20:13:01 &lt;alex_the_designerr&gt; no blockers, just hustle EOT
20:13:06 &lt;zlatinb&gt; 3) No blockers, but will need to work closely with zzz to get things in monotone in a meaningful way, also with meeh if were to reuse the firefox profiile in OSX
20:13:07 &lt;zlatinb&gt; EOT
20:13:09 &lt;zzz&gt; me: 1) wizard, geoip, ls2, prop. 144, bug fixes; 2) ls2, prop. 144, integrating changes from design team, bug fixes, prep for 35C3, 35C3, set up signing machine; 3) no blockers EOT
20:13:57 &lt;zlatinb&gt; anyone else from the team here?
20:14:30 &lt;zlatinb&gt; doesnt look like it.  Thats all from me on 4)
20:14:47 &lt;zzz&gt; ok, anybody have anything else for the meeting?
20:15:49 * zzz finds the baffer
20:16:06 * zzz *bafs* the meeting closed
</div>
