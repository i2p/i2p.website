---
title: "I2P Dev Meeting - August 02, 2016"
date: 2016-08-02
author: "zzz"
description: "I2P development meeting log for August 02, 2016."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> nextloop, psi, poneyhot, sadie, str4d, trolly, xmpre, zzz</p>

## Meeting Log

<div class="irc-log">
21:00:01 &lt;zzz&gt; 0) Hi
21:00:01 &lt;zzz&gt; 1) HOPE report (zzz/sadie) http://zzz.i2p/topics/2152
21:00:01 &lt;zzz&gt; 2) 0.9.27 update (zzz) http://zzz.i2p/topics/2132
21:00:01 &lt;zzz&gt; 3) Summer of X update (sadie/str4d)
21:00:05 &lt;zzz&gt; 0) Hi
21:00:07 &lt;zzz&gt; hi
21:00:38 &lt;xmpre&gt; Hello
21:00:44 &lt;i2pr&gt; [Slack/str4d] Hi
21:00:56 &lt;zzz&gt; 1) HOPE report (zzz/sadie) http://zzz.i2p/topics/2152
21:01:32 &lt;zzz&gt; I've posted a brief trip report at that link. sadie, comraden1, gravy, or anybody who watched some of the videos, anything to add?
21:02:30 &lt;i2pr&gt; [Slack/str4d] I haven't watched the videos yet. Any ones I should earmark besides the Tor ones?
21:03:01 &lt;zzz&gt; I didn't see much more. Hopefully people will add some recommendations to the zzz.i2p thread
21:03:13 &lt;xmpre&gt; For those who may not be aware, where are the videos?
21:03:27 &lt;zzz&gt; hope.net presumably
21:03:56 &lt;zzz&gt; anything else on 1) ?
21:03:59 &lt;xmpre&gt; https://hope.net/watch.html
21:04:54 &lt;zzz&gt; 2) 0.9.27 update (zzz) http://zzz.i2p/topics/2132
21:05:57 &lt;zzz&gt; still looking at mid-sept. at the earliest. Not a lot of activity in mtn or big features. After I finish up the i2p summer stuff, I want to turn to NTCP2. So no rush for .27 atm, things are pretty stable
21:06:26 &lt;zzz&gt; anybody have any comments on .27 schedule or contents?
21:06:39 &lt;i2pr&gt; [Slack/str4d] I'll be turning my attention to NTCP2 about the same time
21:06:49 &lt;xmpre&gt; I had a suggestion to make multihoming easier, should I add that to trac?
21:06:59 &lt;xmpre&gt; essentially an export/import feature
21:07:11 &lt;zzz&gt; ok good. We still need a new tails person too, we all need to tweet about that
21:07:19 &lt;i2pr&gt; [Slack/str4d] I'd also like us to consider enabling SAM by default.
21:07:43 &lt;zzz&gt; xmpre, if it's obvious, trac is fine, if it needs some discussion, zzz.i2p might be better
21:07:48 &lt;i2pr&gt; [Slack/str4d] Or at least discuss the implications of doing so
21:08:06 &lt;xmpre&gt; Alright, zzz 
21:08:27 &lt;zzz&gt; lets put sam-by-default on next month's agenda, after the end of the summer app activity but before .27
21:08:40 &lt;i2pr&gt; [Slack/str4d] ACK
21:08:53 &lt;i2pr&gt; [Slack/str4d] In the meantime, people can think about it
21:09:21 &lt;i2pr&gt; [Slack/str4d] And e.g. compare it to whatever Tor's policy is on their control port
21:09:38 &lt;zzz&gt; added to http://zzz.i2p/topics/2149
21:10:03 &lt;zzz&gt; perhaps we would want auth or ssl to be on if it's on by default? not sure. I'll think about it
21:10:11 &lt;zzz&gt; anything else on 2) ?
21:10:58 &lt;psi&gt; (hi)
21:11:10 &lt;zzz&gt; speaking of next meeting, the CCC budget will be on the agenda, see link above, and please have your requirements ready for that meeting
21:11:13 &lt;i2pr&gt; [Slack/sadie] hi - I am swamped at work guys
21:11:33 &lt;zzz&gt; on to 3) ...
21:11:43 &lt;zzz&gt; 3) Summer of X update (sadie/str4d)
21:11:50 &lt;zzz&gt; sadie, str4d, what's the latest?
21:12:10 &lt;i2pr&gt; [Slack/str4d] Np Sadie, glad you can pop by if briefly :)
21:12:22 &lt;i2pr&gt; [Slack/str4d] Summer Dev is going really well, I think
21:12:47 &lt;i2pr&gt; [Slack/str4d] This month was publicly focused on our work with other applications
21:13:11 &lt;i2pr&gt; [Slack/str4d] (apps that we generally hadn't worked with before)
21:13:47 &lt;i2pr&gt; [Slack/str4d] I succeeded in getting I2P client support into Foolscap, the communication library used by Tahoe-LAFS
21:14:29 &lt;i2pr&gt; [Slack/str4d] So I expect us to be able to use upstream with I2P's grid in the near future, at least for clients
21:14:57 &lt;i2pr&gt; [Slack/str4d] Server-side support for I2P and Tor is planned for a later release
21:15:31 &lt;i2pr&gt; [Slack/str4d] I am also very close to having ZeroNet working over I2P as a proof of concept
21:16:01 &lt;i2pr&gt; [Slack/str4d] (which has also resulted in significant improvements to i2p.socket by psi and myself)
21:16:22 &lt;zzz&gt; ++psi
21:17:15 &lt;zzz&gt; on my side I've done plugin releases for i2phex, jwebcache, and orchid. There will be a syndie release in about a week (please update translations!) and another orchid release too
21:17:34 &lt;i2pr&gt; [Slack/str4d] Woo
21:17:45 &lt;zzz&gt; and maybe jircii, there's at least one person asking for it, if there's any others please holler
21:17:45 &lt;xmpre&gt; Thanks for the efforts on the standalone i2psnark, I have 1 instance working with i2pd
21:17:58 &lt;psi&gt; i2p.socket still needs some developer feedback, oh right and i have to remind myself to look at that ipfs ticket
21:18:44 &lt;i2pr&gt; [Slack/str4d] This next month is designated as time to work on our own apps, but I'd love to see more work with external developers too
21:18:59 &lt;zzz&gt; also a reminder to all to test these libs and standalone apps against i2pd also
21:19:02 &lt;i2pr&gt; [Slack/str4d] E.g. psi working with the IPFS devs :)
21:19:15 &lt;i2pr&gt; [Slack/str4d] :+1:
21:19:47 &lt;nextloop&gt; hello. most of the plugins are not on github. should i also get them there?
21:19:54 &lt;i2pr&gt; [Slack/str4d] If anyone is stuck for ideas, ping me and I'll give you the laundry list.
21:20:23 &lt;i2pr&gt; [Slack/str4d] Could be a good idea
21:20:29 &lt;zzz&gt; one thing that's unstaffed right now, and not sure if it should be, is building/signing standalone packages. kytv did some, ech did some, but we don't have consistent packaging or hosting of a lot of these
21:20:57 &lt;zzz&gt; for some, there aren't even polished build targets in the code
21:21:21 &lt;i2pr&gt; [Slack/str4d] Mmm
21:21:56 &lt;i2pr&gt; [Slack/str4d] I'll be working on migrating I2P-Bote to Gradle this month, as part of overhauling its general build process
21:22:10 &lt;xmpre&gt; I can start building/signing i2psnark standalone packages, I'm building Java I2P through bobthebuilder.i2p
21:22:18 &lt;zzz&gt; I don't want to be a maintainer for any of them. At most I want to do a quick plugin build after somebody else does the rest. But not much was happening, which I guess is the point of i2psummer.
21:22:19 &lt;trolly&gt; gradle?
21:23:26 &lt;zzz&gt; oh yeah, thanks to xmpre for getting bobthebuilder going. It was going a little too much yesterday... and I pushed -8 a few hours ago and haven't seen a build here yet. But I'm sure you'll get it running smoothly
21:23:49 &lt;zzz&gt; anything else on 3) ?
21:24:08 &lt;i2pr&gt; [Slack/str4d] One thing I'd like to do in the current website revamp is to barter advertise the apps we do have, and clearly indicate where volunteers could do good
21:24:13 &lt;xmpre&gt; Hmm, le tme check zzz 
21:24:16 &lt;i2pr&gt; [Slack/str4d] Better*
21:24:41 &lt;zzz&gt; for starters, check what's on i2pwiki
21:24:55 &lt;i2pr&gt; [Slack/str4d] I could also tie that into Summer Dev
21:25:14 &lt;poneyhot&gt; if I may have a few suggestions... don't post them in alphabetical order, no reason for anoncoin to be the first 
21:25:20 &lt;poneyhot&gt; or anonymous git hosting ..
21:25:22 &lt;zzz&gt; anything else for the meeting?
21:25:30 &lt;i2pr&gt; [Slack/str4d] But that would be as part of next month's blog post
21:25:45 &lt;zzz&gt; str4d, you have a july blog post coming soon?
21:25:47 &lt;i2pr&gt; [Slack/str4d] 4) Website layout revamp
21:26:06 &lt;i2pr&gt; [Slack/str4d] zzz, soon, yes. Next few days
21:26:09 &lt;zzz&gt; ok 4) website layout str4d go
21:26:49 &lt;i2pr&gt; [Slack/str4d] Elio Qoshi is making good progress with the website layout revamp
21:27:47 &lt;i2pr&gt; [Slack/str4d] He redid the Whonix website and is currently working with Tor on their branding and style guide, for reference
21:28:15 &lt;i2pr&gt; [Slack/str4d] (also worked for Mozilla)
21:29:08 &lt;zzz&gt; great
21:29:20 &lt;i2pr&gt; [Slack/str4d] The current aim is to reduce the walls of text (further from where I got them to), and also have a cohesive design between the landing page and inner pages (something the current design lacks)
21:30:27 &lt;i2pr&gt; [Slack/str4d] His current wireframe, to give you an idea, will be single-column content in the middle with equal whitespace gutters either side (in which in-page navigation and metadata will go like currently)
21:30:45 &lt;zzz&gt; ok. as we discussed the other day re: logos, it's good to know what goals you're feeding to the designer so we can evaluate the results in that context
21:31:06 &lt;zzz&gt; anything else on 4) ?
21:31:24 &lt;i2pr&gt; [Slack/str4d] On the front page, the (rather dreadful) list in the centre column is going to be replaced with friendlier call outs to specific apps and tasks
21:31:25 &lt;poneyhot&gt; does 4) include the 127.0.0.1 home page?
21:31:37 &lt;i2pr&gt; [Slack/str4d] honeypot, no
21:31:52 &lt;zzz&gt; anything else for the meeting?
21:32:05 &lt;i2pr&gt; [Slack/str4d] Oh, he just messaged me the first screenshot of his proposed front page design
21:32:26 &lt;i2pr&gt; [Slack/str4d] But I can't just share it to IRC, so will have to do so when I'm back at my computer
21:32:41 &lt;i2pr&gt; [Slack/str4d] Regarding the router console:
21:32:57 &lt;zzz&gt; ok 5) router console str4d go
21:33:03 &lt;i2pr&gt; [Slack/str4d] See the i2p.i2p.str4d.ui branch for progress
21:33:27 &lt;i2pr&gt; [Slack/str4d] The CSS has now been updated to match the backbend changes, and is at first draft
21:33:45 &lt;zzz&gt; poneyhot, did you have a meeting topic to add re: the console?
21:34:18 &lt;i2pr&gt; [Slack/str4d] (got a few local changes to push someone before this weekend if I get time)
21:34:18 &lt;i2pr&gt; [Slack/str4d] Feedback welcome
21:34:18 &lt;i2pr&gt; [Slack/str4d] Note however that this is only an intermediate step
21:34:30 &lt;zzz&gt; anything else on 5) ?
21:34:37 &lt;i2pr&gt; [Slack/str4d] None of the changes currently affect anything structural
21:34:48 &lt;poneyhot&gt; I have to check the changes 1st, I just dislike the alphabetical sort
21:34:49 &lt;i2pr&gt; [Slack/str4d] That is my plan to do in probably October
21:35:09 &lt;zzz&gt; oh, that's what you were referencing re: anoncoin, I get it
21:35:17 &lt;zzz&gt; anything else for the meeting?
21:35:29 &lt;poneyhot&gt; it looks like those are the most important things on i2p
21:35:35 &lt;i2pr&gt; [Slack/str4d] poneyhot, that may end up changing entirely
21:35:51 &lt;i2pr&gt; [Slack/str4d] Or not ^^
21:36:25 * zzz grabs the baffer Negan-style
21:36:26 &lt;i2pr&gt; [Slack/str4d] My goal is to have a refreshed and improved router console ready for CCC
21:36:58 &lt;xmpre&gt; I'd be happy to help test the new router console
21:37:09 &lt;xmpre&gt; (and I hope the annoying cookie errors will be fixed :p)
21:37:24 * zzz *bafs* the meeting closed
</div>
