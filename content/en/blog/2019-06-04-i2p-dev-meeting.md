---
title: "I2P Dev Meeting - June 04, 2019"
date: 2019-06-04
author: "zzz"
description: "I2P development meeting log for June 04, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, eyedeekay, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:14 &lt;zzz&gt; 0) Hi
20:00:16 &lt;zzz&gt; hi
20:00:43 &lt;zzz&gt; 1) 0.9.40 release status remaining items (meeh, mhatta, nextloop, str4d)
20:00:43 &lt;zzz&gt; 2) Fixed i2pbote-android release status (meeh)
20:00:43 &lt;zzz&gt; 3) 0.9.41 dev status (zzz)
20:00:43 &lt;zzz&gt; 4) LS2 status (zzz)
20:00:43 &lt;zzz&gt; 5) I2P Browser "labs" project status (meeh)
20:00:43 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:01:03 &lt;zzz&gt; 1) 0.9.40 release status remaining items (meeh, mhatta, nextloop, str4d)
20:01:28 &lt;zzz&gt; I believe that Debian/Ubuntu and official f-droid remain?
20:01:41 &lt;zzz&gt; I did hear back from mhatta, but he didn't make any promises
20:02:04 &lt;zzz&gt; I have reached out to other Debian people to see if anybody else could do it, nothing yet
20:02:10 &lt;zzz&gt; nextloop you have an update for us?
20:02:53 &lt;eche|on&gt; i build test build for debian buster and stretch on echelon.i2p/update/
20:02:57 &lt;zzz&gt; anything else on 1) ?
20:03:29 &lt;zzz&gt; 2) Fixed i2pbote-android release status (meeh)
20:03:40 &lt;zzz&gt; mikalv, you have an update for us on bote?
20:04:52 &lt;zzz&gt; I believe we got the bote release out and it's working for people
20:04:58 &lt;zzz&gt; anything else on 2) ?
20:05:16 &lt;eyedeekay&gt; Nothing from me
20:05:30 &lt;zzz&gt; 3) 0.9.41 dev status (zzz)
20:05:45 &lt;zzz&gt; ok, we're a little bit more than halfway through the .41 dev cycle and it's going well
20:06:06 &lt;zzz&gt; big feature is the per-client authentication stuff for encrypted LS2
20:06:19 &lt;zzz&gt; we've also fixed a bug in large message handling that I think will help bote work better
20:06:55 &lt;eche|on&gt; we will see, test build available
20:06:56 &lt;zzz&gt; idk and I are working on splitting up the clients.config and i2ptunnel.config files, but it's looking like it will have to wait until .42
20:07:38 &lt;zzz&gt; for bote to see a difference it will probably have to get out to most of the network, as the bug could be hit by any router along the way
20:08:03 &lt;eche|on&gt; yeah
20:08:12 &lt;zzz&gt; the release is scheduled for the first week of July
20:08:33 &lt;zzz&gt; anything else on 3) ?
20:09:28 &lt;zzz&gt; 4) LS2 status (zzz)
20:09:58 &lt;zzz&gt; still going strong. We've had 42 weekly meetings so far and no end in sight, although we're spending more time on the new encryption (proposal 144) lately
20:10:19 &lt;zzz&gt; I already mentioned the per-client auth code that will be in 41.
20:10:54 &lt;zzz&gt; Garlic farm development for meta ls2 has been on hold for maybe 3 weeks, in favor of the client auth code, but we will be returning to it shortly
20:11:27 &lt;zzz&gt; I'm continuing to migrate specs from the proposals to the main specs part of our website
20:11:38 &lt;zzz&gt; as we get things implemented and tested
20:11:52 &lt;zzz&gt; our meetings are still 6:30 PM UTC on mondays in #ls2
20:12:11 &lt;zzz&gt; anything else on 4) ?
20:13:04 &lt;zzz&gt; 5) I2P Browser "labs" project status (mikalv)
20:13:15 &lt;zzz&gt; mikalv, how is the i2p browser going?
20:14:08 &lt;zzz&gt; I know a new beta release went out and it's getting some testing, but it doesn't work at all for some people?
20:15:04 &lt;zzz&gt; there's also a request for more documentation on our lab download page, and he said he would be getting to that soon, so keep an eye out
20:15:17 &lt;zzz&gt; ok, I guess mikalv isn't around, anything else on 5) ?
20:16:08 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:16:13 &lt;zzz&gt; take it away zlatinb 
20:16:42 &lt;zlatinb&gt; Hi lets do the usual - say 1) what youve been doing since last scrum 2) what you plan to do next month 3) if you have any blockers or need help
20:16:46 &lt;zlatinb&gt; end with EOT when done
20:17:08 &lt;zlatinb&gt; me: 1) some garlic farm, not much else 2) hopefully more garlic farm 3) no blockers
20:17:09 &lt;zlatinb&gt; EOT
20:17:17 &lt;eche|on&gt; doing the same as always, keepeing server alive, going on the same, no blocker, eot
20:17:30 &lt;zzz&gt; 1) garlic farm, ls2, and per-client auth; bug fixes
20:18:10 &lt;zzz&gt; 2) garlic farm, bug fixes, GMP 6.1.2, config file splitting, getting ready for 0.9.41 release
20:18:18 &lt;eyedeekay&gt; Split i2ptunnel configs and writing documentation/blogs, 2) more of that 3) no blockers eot
20:18:32 &lt;zzz&gt; 3) no blockers, EOT
20:18:44 &lt;zlatinb&gt; ok I think this is everyone, thanks
20:19:04 &lt;zzz&gt; ok, that was pretty quick, we're getting more efficient!
20:19:18 &lt;zzz&gt; anything else for the meeting today?
20:20:15 &lt;zzz&gt; oh, and congrats to eyedeekay who has signed a dev agreement and been granted mtn checkin privileges! while he's done quite a lot for us in the last few months, now he can do damage a lot faster!
20:20:37 &lt;eyedeekay&gt; :-D
20:20:38 &lt;zzz&gt; looking forward to having eyedeekay directly on the code base
20:21:07 * zzz looks for the baffer to swing at you
20:22:01 * zzz *bafs* the meeting closed
</div>
