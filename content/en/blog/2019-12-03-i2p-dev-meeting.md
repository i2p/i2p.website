---
title: "I2P Dev Meeting - December 03, 2019"
date: 2019-12-03
author: "zzz"
description: "I2P development meeting log for December 03, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> eyedeekay, meeh, sadie, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) I2P Browser project status (sadie, meeh, idk)
20:00:00 &lt;zzz&gt; 2) Outproxy use cases / status (sadie)
20:00:00 &lt;zzz&gt; 3) 0.9.44 release status (zzz)
20:00:00 &lt;zzz&gt; 4) Status scrum (zlatinb)
20:00:10 &lt;sadie__&gt; hi
20:00:20 &lt;zzz&gt; 0) Hi
20:00:22 &lt;zzz&gt; hi
20:00:47 &lt;zzz&gt; 1) I2P Browser project status (sadie, meeh, idk)
20:00:49 &lt;zlatinb&gt; hi
20:01:00 &lt;meeh&gt; hi
20:01:23 &lt;zzz&gt; sadie, what's the latest on the I2P Browser project? and feel free to delegate any parts of your answer to idk and meeh
20:01:32 &lt;eyedeekay&gt; Hi
20:03:02 &lt;meeh&gt; The biggest news is probably that our next release is now is based upon ESR 68 and not 60, and our extensions is in the progress to be ported into the source since mozilla removes some of our current used api in later versions
20:03:27 &lt;zzz&gt; and when is that release scheduled?
20:03:47 &lt;meeh&gt; It's also the first release which should be signed by our new EV code signing certificate so no more scary warnings
20:03:54 &lt;meeh&gt; in two three days
20:04:06 &lt;meeh&gt; let's say 6th
20:04:15 &lt;zzz&gt; ok so this will be beta 8 I think?
20:04:26 &lt;meeh&gt; yea that's correct
20:04:27 &lt;eyedeekay&gt; Yes beta 8
20:04:43 &lt;zzz&gt; super. anything else to add sadie__ eyedeekay ?
20:05:08 &lt;eyedeekay&gt; Besides that we now also enable the suite of I2P applications, snark, susimail, etc.
20:05:19 &lt;sadie__&gt; yes - we will have an updated MVP and roadmap available as well
20:05:54 &lt;zzz&gt; when will those be posted?
20:05:56 &lt;meeh&gt; and we will in time, release replacements with modern standards for at least susimail and addressbook to start with
20:06:14 &lt;meeh&gt; that was not for this release doh, but in later releases
20:06:47 &lt;sadie__&gt; those should be on the site middle of next week, along with the updated project name and branding direction
20:07:15 &lt;meeh&gt; one news not directly linked to the browser is that we now also have a Rack "runner" which directly talks to I2PSocket and don't require the user to port it via some local tcp port
20:07:25 &lt;zzz&gt; nice. care to leak the new name or you going to hold off until it's up on the site?
20:07:34 &lt;meeh&gt; so it makes it possible to run for example Ruby on Rails directly towards I2PSocket 
20:07:57 &lt;sadie__&gt; We are holding off until the site is updated =)
20:08:12 &lt;zzz&gt; nice meeh, always better to avoid going out-and-back via a standard socket
20:08:51 &lt;zzz&gt; sounds like great progress
20:09:01 &lt;zzz&gt; anything else on 1) ? anybody have any questions?
20:10:31 &lt;zzz&gt; 2) Outproxy use cases / status (sadie)
20:10:41 &lt;zzz&gt; sadie__, whats the latest on this research effort?
20:10:44 &lt;sadie__&gt; The outproxy turnkey solution has been put on hold until I can acquire the resources needed for proper information gathering to complete the MVP.  This research will not resume until next year. General use outproxy discussion will resume in the coming weeks. At this point the priority for the our proxy should be investigating and improving performance issues.   
20:11:45 &lt;zzz&gt; ok, re: the project's outproxy, what's the status on investigation and improvement?
20:12:10 &lt;zzz&gt; meeh you have any info on that?
20:12:17 &lt;sadie__&gt; meeh can comment of that effort better than I 
20:12:28 &lt;meeh&gt; Also since the topic is outproxy, the jruby gem I made also have a simple single threaded outproxy that can run as a i2p plugin for that matter
20:12:33 &lt;meeh&gt; found here https://github.com/mikalv/ji2p-jruby/blob/master/bin/simple_outproxy
20:13:08 &lt;zzz&gt; but what about the current outproxy?
20:13:09 &lt;meeh&gt; also I've started splitting the gem up, so you don't need to bundle cluster support and such for a simple i2p plugin not having anything to do with such
20:13:13 &lt;meeh&gt; because it's gotten quite big
20:13:41 &lt;meeh&gt; yea, I've had some cable and switch upgrades which was a bottleneck for the public outproxy
20:13:52 &lt;zzz&gt; I've started keeping track of every outproxy fetch, success or failure, on a postit. Today's success rate is only 75%
20:14:26 &lt;zzz&gt; sadie says it's a priority, so what do you plan to do next?
20:14:39 &lt;meeh&gt; the next browser release beta 8, sorry I forgot to mention before, will have many more destinations pointing to the same service as we believe the destinations in themself are the next bottleneck
20:14:56 &lt;meeh&gt; so not only false.i2p and my tor bridge, but more like in the count of 20
20:15:30 &lt;meeh&gt; I will also switch the proxy software with a custom made elixir/erlang software for that, which I wrote back some months ago
20:15:45 &lt;meeh&gt; also found here https://github.com/mikalv/i2p-outproxy-elixir
20:16:00 &lt;zzz&gt; have you considered switching from i2pd to java? I think there's some major issues with running it on i2pd
20:16:14 &lt;meeh&gt; I got some uncommited changes I'll push before I do the switch, and anyone can use this to run their own. I'll make better docs for that as well 
20:16:25 &lt;meeh&gt; I use both currently
20:16:29 &lt;meeh&gt; both java and i2pd
20:16:39 &lt;zzz&gt; ok
20:16:40 &lt;meeh&gt; it should be four routers all having the two dest
20:16:51 &lt;meeh&gt; pointing to the same http proxy endpoint
20:17:05 &lt;zzz&gt; do you have a conclusion yet on which provides better service?
20:17:17 &lt;meeh&gt; the i2pd's are setup with like 100 tunnels compared to java's 16 tunnel limit
20:17:49 &lt;meeh&gt; no sorry not yet, but that's something I've put in my todo list of things I should do in near future
20:18:21 &lt;zzz&gt; ok, I encourage the team to use a measurement-based approach to making improvements. don't just shotgun it and change everything
20:18:51 &lt;meeh&gt; yea, I've done that before and learned from it - so no worry, measurement-based it is
20:18:55 &lt;zzz&gt; anything else on 2) sadie__ ?
20:19:09 &lt;sadie__&gt; no
20:19:22 &lt;zzz&gt; anybody have any questions on 2) ?
20:20:19 &lt;zzz&gt; 3) 0.9.44 release status
20:20:29 &lt;zzz&gt; ok we got the 0.9.44 release out on Sunday
20:21:00 &lt;zzz&gt; it fixes a nasty issue in the way new encryption types are handled. Everybody should upgrade as soon as they can
20:21:12 &lt;meeh&gt; for android it's published on google play, fdroid and on our download page where the latter includes gpg signature and website updated
20:21:33 &lt;zzz&gt; great. how about mavencentral?
20:22:03 &lt;meeh&gt; yea, it's a required dependency of the above, so when I've done the above I must already have done mavencentral
20:22:07 &lt;zzz&gt; it's available for in-net updates now. About 10% of the network has upgraded already
20:22:38 &lt;zzz&gt; I also did the PPA and deb repo on sunday
20:22:58 &lt;zzz&gt; so I think that's most of it
20:23:05 &lt;zzz&gt; no complaints so far
20:23:24 &lt;zzz&gt; unfortunately, the bandwidth tester is pretty much completely broken
20:23:51 &lt;zzz&gt; something changed in the test pool lately, and the way we were doing the handshake stopped working
20:24:10 &lt;zzz&gt; I spent the last day and a half working on it, and I got it going again
20:24:40 &lt;zzz&gt; if anybody sees stuff like this is broken, please file a ticket. It's a shame we didn't realize it was busted before the release
20:25:29 &lt;meeh&gt; we got a new (standalone) donation page just around the corner also, which would enable more ways to donate, also recurring paypal etc
20:25:39 &lt;zzz&gt; so that's about all I have on .44. We're just getting started on .45 and putting the plan together, but I expect the 45 release will be in February
20:25:44 &lt;meeh&gt; and it looks **nice**
20:25:48 &lt;meeh&gt; with capital letters
20:25:56 &lt;zzz&gt; ok meeh, great
20:26:02 &lt;zzz&gt; anything else on 3) ?
20:27:02 &lt;zzz&gt; 4) status scrum
20:27:06 &lt;zzz&gt; go ahead zlatinb 
20:27:31 &lt;zlatinb&gt; hi, very briefly: 1) what youve been doing last month 2) what you plan to do next month 3) any blockers or do you need help 4) EOT
20:28:31 &lt;zlatinb&gt; me: 1) fixed the scriptable filter writing to disk every 10 seconds, investigated servlet 3.0 support (broken for inner classes) 2) packaging MW as a router plugin 3) no blockers 
20:28:35 &lt;zlatinb&gt; EOT
20:28:49 &lt;zzz&gt; 1) .44 release, bug fixes, prop. 144 (ratchet) coding and testing; fixed a bad tunnel bug causing slow startup, got a new version of zzzot out with drzed's help
20:29:28 &lt;zzz&gt; 1 (cont) lots of work testing reseeds and working with reseeders to get things un-broken; tested and removed open trackers also
20:30:09 &lt;meeh&gt; done: jruby gem for interacting and/or controlling the router embedded or standalone, initial kubernetes support for either HA destinations or cluster testing of i2p, many many firefox patches either written by scratch or ported from tor browser, outproxy improvements, and a new mail application with the attent to replace susimail one day
20:30:19 &lt;meeh&gt; initial work on the last one*
20:30:23 &lt;zzz&gt; 2) bug fixes, prop. 144 testing, more work on improving performance, 36C3
20:30:46 &lt;sadie__&gt; Last month has been working on css light theme changes that are in the latest release, responding to Usability Lab for UX Study funding for router console, and driving product decisions for the future of the browser. Next month, will be post install guide, and more css work, browser management and developemnt
20:30:56 &lt;zzz&gt; 3) no blockers; 4) EOT
20:31:10 &lt;sadie__&gt; no blockers, EOT
20:31:15 &lt;eyedeekay&gt; 1) I have been working on opening up the I2P Browser experience to more of I2P's overall capabilities and adjusting the organization/look-and-feel of the router console and home pages. 2) Next month I'll be  working on more browser feature improvements, more SAM tutorials, and more router console UI improvements. 3) no blockers EOT.
20:31:48 &lt;zlatinb&gt; thanks, thats everyone I think &lt;/scrum&gt;
20:32:08 &lt;zzz&gt; super, anything else on 4) ? anybody have any questions?
20:32:24 &lt;zzz&gt; or any other topics for the meeting?
20:32:28 &lt;meeh&gt; next month: release beta 8 of the browser, figure out how we can use the osslsigncode software to sign windows binaries on unix systems, switch outproxy software, continue the work of the new mail app, and finish the changes for the jruby gem
20:33:16 &lt;zzz&gt; EOT meeh?
20:33:32 &lt;meeh&gt; yea, EOT.
20:34:16 &lt;zzz&gt; ok. A reminder there will be no meeting next month as we'll be recovering from 36C3. If anybody would like to join our meetings at 36C3, come find our table
20:34:32 &lt;zzz&gt; I'm sure I will tweet out the approximate location
20:34:48 &lt;sadie__&gt; and we will have a new banner for the table!
20:34:48 &lt;meeh&gt; we can probably publish some public notes from the meeting as well?
20:34:58 &lt;meeh&gt; that's from ccc
20:34:59 &lt;zzz&gt; any other topics for the meeting, while I look for the baffer?
20:35:28 &lt;zzz&gt; you volunteering meeh?
20:35:41 &lt;meeh&gt; I can try do that yea
20:35:59 &lt;sadie__&gt; I will do a report for ccc
20:36:35 &lt;zzz&gt; ok, I found the *baffer* so I guess that's about it for today
20:36:46 &lt;zzz&gt; see you all in person in 4 weeks
20:37:10 &lt;zzz&gt; whups, 3 1/2 weeks
20:37:24 * zzz *bafs* the meeting closed
</div>
