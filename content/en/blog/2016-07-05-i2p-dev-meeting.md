---
title: "I2P Dev Meeting - July 05, 2016"
date: 2016-07-05
author: "zzz"
description: "I2P development meeting log for July 05, 2016."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, psi, sadie, str4d, Zerolag, zzz</p>

## Meeting Log

<div class="irc-log">
21:00:23 &lt;zzz&gt; 0) Hi
21:00:23 &lt;zzz&gt; 1) HOPE update (zzz) http://zzz.i2p/topics/1968
21:00:23 &lt;zzz&gt; 2) 0.9.27 update (zzz)
21:00:23 &lt;zzz&gt; 3) Summer of X update (sadie/str4d)
21:00:27 &lt;zzz&gt; 0) Hi
21:00:29 &lt;zzz&gt; hi
21:00:47 &lt;psi&gt; hi
21:00:48 &lt;zzz&gt; 1) HOPE update (zzz) http://zzz.i2p/topics/1968
21:00:48 &lt;i2pr&gt; [Slack/str4d] Hi
21:01:13 &lt;zzz&gt; ok, HOPE is in 2 1/2 weeks. The possible lunch meeting with Lance on Friday is still TBD
21:01:42 &lt;zzz&gt; please keep friday lunch open, I don't expect we will know if it's off or on until that week
21:01:49 &lt;zzz&gt; looking forward to seeing everybody there
21:01:54 &lt;zzz&gt; anything else on 1) ?
21:02:06 &lt;i2pr&gt; [Slack/str4d] I'm now guaranteed to not be there
21:02:20 &lt;i2pr&gt; [Slack/str4d] Timing has not been in my favour ;_;
21:02:51 &lt;psi&gt; i am not going to hope this year it seems
21:03:14 &lt;i2pr&gt; [Slack/sadie] I will be at HOPE
21:03:38 &lt;zzz&gt; 2) 0.9.27 update (zzz)
21:04:13 &lt;zzz&gt; .27 is progressing slowly, as expected. At this rate, the .27 release will be pushed from August to Sept.
21:04:31 &lt;zzz&gt; while we focus on X stuff, and perhaps, NTCP2
21:04:47 &lt;i2pr&gt; [Slack/str4d] Fine with me
21:04:50 &lt;zzz&gt; that OK with everybody?
21:05:02 &lt;dg&gt; There's nothing to rush on, so OK
21:05:09 &lt;dg&gt; ultimately we will release when we need to
21:05:28 &lt;zzz&gt; 26 seems really stable. The only thing is the bote class not found thing, which we're awaiting followup info for on trac
21:05:52 &lt;dg&gt; There was something to do with the Debian package which I found as an issue
21:05:56 &lt;i2pr&gt; [Slack/str4d] And that gives us a chance to get work done in August on plugins into .27
21:05:57 &lt;zzz&gt; and if it's what I think it is, we could fix it with a simple change and deb/ubuntu rebuild only
21:06:00 &lt;dg&gt; Will save it for a ticket though. 
21:06:12 &lt;zzz&gt; anything else on 2) ?
21:06:38 &lt;psi&gt; does .27 affect anything in i2pd?
21:07:19 &lt;zzz&gt; there's ipv6 peer testing, yes. i2pd shouldn't bump to 27 until it's supported
21:07:39 &lt;psi&gt; okay
21:07:50 &lt;zzz&gt; doesn't have to be on the java schedule though
21:07:53 &lt;zzz&gt; anything else on 2) ?
21:08:42 &lt;zzz&gt; 3) Summer of X update (sadie/str4d)
21:08:51 &lt;zzz&gt; sadie, str4d, what's going on?
21:08:52 &lt;i2pr&gt; [Slack/str4d] Not yet, I think?
21:08:55 &lt;i2pr&gt; [Slack/str4d] Ah yep
21:08:55 &lt;i2pr&gt; [Slack/str4d] No
21:10:30 &lt;zzz&gt; perils of using a relay for the meeting?
21:10:40 &lt;i2pr&gt; [Slack/str4d] I think it's been going well so far
21:10:55 &lt;i2pr&gt; [Slack/str4d] We're a month in now, and have had three (IIRC) blog posts out about it
21:11:46 &lt;zzz&gt; ok, what are we doing in july?
21:12:02 &lt;i2pr&gt; [Slack/str4d] Apps
21:12:05 &lt;i2pr&gt; [Slack/str4d] Outreach
21:12:15 &lt;i2pr&gt; [Slack/str4d] So I'll be working with Tahoe-LAFS
21:12:29 &lt;i2pr&gt; [Slack/str4d] On their I2P integration
21:13:12 &lt;zzz&gt; any volunteers to work on transmission and/or libtorrent? Those seem to be swamps of brokenness right now
21:13:14 &lt;i2pr&gt; [Slack/str4d] And also submitting a PR to update lightning Browser's I2P library
21:13:45 &lt;i2pr&gt; [Slack/str4d] Yeah, it's never too late to pick up another API
21:13:59 &lt;i2pr&gt; [Slack/str4d] Other projects I'd like to see us help this month:
21:14:02 &lt;zzz&gt; the outreach part is key, lets get the word out via twitter and email
21:14:08 &lt;psi&gt; what was done in transmission before?
21:14:31 &lt;zzz&gt; there's a i2p fork for transmission, see the zzz.i2p thread
21:14:33 &lt;i2pr&gt; [Slack/str4d] psi, SAM support
21:14:52 &lt;i2pr&gt; [Slack/str4d] In libtorrent
21:14:54 &lt;psi&gt; that was before libsam3 wasn't it?
21:14:58 &lt;psi&gt; i'd guess it has totally bit rotted
21:15:09 &lt;i2pr&gt; [Slack/str4d] (I keep forgetting transmission doesn't use that)
21:15:23 &lt;zzz&gt; sadie, what do you have planned for July PR?
21:15:31 &lt;i2pr&gt; [Slack/str4d] Mmm, a clean fork might be easier
21:15:58 &lt;i2pr&gt; [Slack/str4d] As I was saying, the other projects I have ideas for:
21:16:01 &lt;i2pr&gt; [Slack/str4d] - IPFS (Go and Python impls)
21:16:27 &lt;i2pr&gt; [Slack/str4d] - OpenBazaar (will soon use IPFS)
21:16:34 &lt;i2pr&gt; [Slack/str4d] - ZeroNet
21:17:02 &lt;i2pr&gt; [Slack/str4d] Any of these would be good candidates for someone to help out
21:17:33 &lt;villain&gt; hello i2peeps :) zzz: I've just sent a patch for the website, hope it will be delivered 
21:17:38 &lt;psi&gt; i have yet to figure out ipfs' contribution guide
21:17:45 &lt;zzz&gt; ok great. Anything else on 3) ? Sadie?
21:18:05 &lt;zzz&gt; thx villain, we're in the middle of a meeting, I'll look for it later
21:18:06 &lt;psi&gt; i'd love to get into IPFS but haven't figured out how.
21:18:25 &lt;Zerolag&gt; I'd love to get my hands on ZeroNet. See how well it goes over i2p.
21:18:28 &lt;i2pr&gt; [Slack/str4d] Psi, I can have a look this weekend at how they onboard
21:19:08 &lt;psi&gt; Zerolag: last time i checked adding i2p to zeronet should be pretty easy since they already have boilerplate for tor
21:19:11 &lt;i2pr&gt; [Slack/str4d] Zerolag, great! They are torrent-based, so would need modifying to our torrent spec
21:19:21 &lt;psi&gt; also, i2p.socket is getting there
21:19:33 &lt;i2pr&gt; [Slack/str4d] (to support clearnet and I2P torrents side by side)
21:19:54 &lt;psi&gt; zeronet uses mainline bittorrent?
21:20:01 &lt;i2pr&gt; [Slack/str4d] Not sure
21:20:17 &lt;psi&gt; i am pretty sure it doesn't but then again...
21:20:22 &lt;i2pr&gt; [Slack/str4d] (what impl they use)
21:20:36 &lt;zzz&gt; Anything else on 3) ? Sadie?
21:20:58 &lt;i2pr&gt; [Slack/str4d] psi, they user Bitcoin crypto and the bittorrent network
21:21:39 &lt;i2pr&gt; [Slack/str4d] I think Sadie might have double booked this meeting
21:21:49 &lt;zzz&gt; moving on then. anything else for the meeting?
21:22:21 &lt;zzz&gt; everybody ok with 9 PM again? I see echelon isn't here, maybe due to time change, maybe not
21:22:46 &lt;psi&gt; 9 pm works for me
21:22:46 &lt;Zerolag&gt; str4d alright, what is the i2p spec for torrent?
21:23:09 * zzz warms up the baffer
21:23:12 &lt;i2pr&gt; [Slack/str4d] Nothing else from me other than: pick a project and help them out! :-)
21:23:31 &lt;i2pr&gt; [Slack/str4d] 9pm is perfect for me
21:24:05 &lt;Zerolag&gt; I'll be here 9pm for sure
21:24:15 &lt;i2pr&gt; [Slack/str4d] Zerolag, see the I2P website (Docs -&gt; Apps -&gt; BitTorrent)
21:24:19 * zzz *baffffs* the meeting closed
</div>
