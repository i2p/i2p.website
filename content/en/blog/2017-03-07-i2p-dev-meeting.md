---
title: "I2P Dev Meeting - March 07, 2017"
date: 2017-03-07
author: "zzz"
description: "I2P development meeting log for March 07, 2017."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, manas, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:25 &lt;zzz&gt; 0) Hi
20:00:25 &lt;zzz&gt; 1) Tails maintainer (zzz) http://zzz.i2p/topics/2108
20:00:25 &lt;zzz&gt; 2) 0.9.30 update (zzz)
20:00:25 &lt;zzz&gt; 3) UI branch status - for .30 or .31? (str4d)
20:00:25 &lt;zzz&gt; 4) Jetty 9 branch status - for .30 or .31? (zzz)
20:00:30 &lt;zzz&gt; 0) Hi
20:00:32 &lt;zzz&gt; hi
20:00:50 &lt;manas&gt; Hello
20:00:54 &lt;zzz&gt; 1) Tails maintainer (zzz) http://zzz.i2p/topics/2108
20:01:16 &lt;zzz&gt; as most of you know, tails and I agreed to remove i2p from tails
20:01:34 &lt;zzz&gt; this will take effect in tails 2.12, due out in abut 6 weeks
20:01:43 &lt;eche|on&gt; hi
20:01:57 &lt;eche|on&gt; ok
20:01:59 &lt;zzz&gt; sad, but we had no other choice. If we get a volunteer to maintain it, we will reapply
20:02:08 &lt;zzz&gt; anything else on 1) ?
20:02:45 &lt;eche|on&gt; to bad, but not to be changed soon (tm)
20:03:07 &lt;manas&gt; Yeah. Too bad the guy at 33C3 didn't work out
20:03:30 &lt;zzz&gt; yup
20:03:40 &lt;zzz&gt; 2) 0.9.30 update (zzz)
20:04:23 &lt;zzz&gt; ok we're a week from the .29 release, our plan is for a standard 8-week cycle. Big changes in by mid-March, release late April
20:04:51 &lt;zzz&gt; there's a couple big props pending that we will cover in 3) and 4)
20:05:17 &lt;zzz&gt; anything else on 2) ?
20:05:51 &lt;eche|on&gt; Ill be gone 1st may
20:06:00 &lt;eche|on&gt; or better 30thapril-2nd may
20:07:00 &lt;zzz&gt; both of these props are important because it's difficult to go back. once we prop them, we have to get them to work before we can releawe
20:07:07 &lt;zzz&gt; *release
20:07:29 &lt;eche|on&gt; yeah
20:07:57 &lt;zzz&gt; 3) UI branch status - for .30 or .31? (str4d)
20:08:34 &lt;zzz&gt; this is an enormous change, although originally advertised as a minor refresh, and part 1 of several to update the console UI
20:08:54 &lt;zzz&gt; the diff is 77K lines, with 500+ files added, 200+ files changed
20:09:06 &lt;eche|on&gt; I would vote for 1 prop per release, not both in .30 
20:09:07 &lt;zzz&gt; str4d, what's the status, and do you want to prop it for .30 ?
20:09:27 &lt;eche|on&gt; and as jettty9 is more important, push ui to .31
20:11:07 &lt;zzz&gt; the key is we don't want to prop something if the author doesn't have time to fix problems before the release. Otherwise the release could be delayed indefinitely
20:11:39 &lt;eche|on&gt; yeah
20:11:46 &lt;zzz&gt; so whenever it's propped we need assurances from str4d that he will be available here to respond to issues
20:11:54 &lt;zzz&gt; str4d, what are your intentions?
20:12:15 &lt;eche|on&gt; is str4d around at all?
20:13:11 &lt;zzz&gt; dunno. I think this branch really got away from him, advertised as minor but became massive. I think he's been working on it for a year.
20:13:38 &lt;zzz&gt; I guess we'll have to follow up with str4d later
20:13:54 &lt;zzz&gt; anything else on 3) ?
20:14:03 &lt;manas&gt; He did say something about a branch recently
20:14:17 &lt;manas&gt; I have not tested it, I'll clone it
20:15:23 &lt;zzz&gt; it's... interesting. I'd say he went in a different direction from what I've been doing in the last several years. I can't predict what the general reaction will be.
20:15:42 &lt;zzz&gt; anything else on 3) ?
20:16:16 &lt;zzz&gt; 4) Jetty 9 branch status - for .30 or .31? (zzz)
20:17:03 &lt;zzz&gt; this is about 3k lines of diff. I have the standard builds working in my branch, and the build for stretch. I haven't tested the down-rev builds for wheezy/precise/jessie/trusty yet
20:17:35 &lt;zzz&gt; the pressing thing is that stretch won't have jetty 8. It appears that zesty, due out next month, won't either, unless it appears in backports
20:17:44 &lt;zzz&gt; but jetty 8 was eol in december
20:18:17 &lt;eche|on&gt; jetty8 will less likely appear in backports
20:18:20 &lt;zzz&gt; so the risk is that stretch or zesty will be released, and i2p won't work in them
20:18:42 &lt;zzz&gt; so I propose to prop my jetty9 branch in the next week, to be included in .30
20:19:21 &lt;eche|on&gt; yeah
20:19:29 &lt;zzz&gt; this will break, at least, the following plugins: bwschedule, i2pbote, i2pcontrol, zzzot. They will need at least a recompile, maybe a rewrite
20:19:33 &lt;eche|on&gt; thats what I propose, IF youu think you can do it
20:20:46 &lt;zzz&gt; I can recompile zzzot. Up to the authors of the other 3 (cacapo. str4d, hottuna2 respectively) if they can release
20:21:40 &lt;zzz&gt; I can do my side
20:22:07 &lt;zzz&gt; I think if we wait until .31 in june/july there will be a lot of unhappy package users
20:22:53 &lt;eche|on&gt; yeah
20:22:54 &lt;zzz&gt; so I plan to prop it in the next few days
20:23:00 &lt;zzz&gt; anything else on 4) ?
20:23:08 &lt;eche|on&gt; I will test
20:23:28 &lt;zzz&gt; anything else for the meeting?
20:24:25 * zzz warms up the baffer
20:24:30 &lt;eche|on&gt; not that I know of yet
20:25:27 * zzz *baffffs* the meeting closed
</div>
