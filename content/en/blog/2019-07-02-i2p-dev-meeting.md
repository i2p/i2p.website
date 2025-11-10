---
title: "I2P Dev Meeting - July 02, 2019"
date: 2019-07-02
author: "zzz"
description: "I2P development meeting log for July 02, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> eyedeekay, meeh, sadie, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.40 release status remaining items (mhatta, nextloop)
20:00:00 &lt;zzz&gt; 2) 0.9.41 release status (zzz)
20:00:00 &lt;zzz&gt; 3) LS2 status (zzz)
20:00:00 &lt;zzz&gt; 4) I2P Browser "labs" project status (meeh)
20:00:00 &lt;zzz&gt; 5) muwire.i2p console home page request (zlatinb)
20:00:00 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:00:03 &lt;zzz&gt; 0) Hi
20:00:05 &lt;zzz&gt; hi
20:00:12 &lt;zlatinb&gt; hi
20:00:31 &lt;zzz&gt; 1) 0.9.40 release status remaining items (mhatta, nextloop)
20:00:42 &lt;zzz&gt; still no word from mhatta or nextloop, sadly
20:00:59 &lt;zzz&gt; I've made repeated attempts to find a new deb maintainer, no luck so far
20:01:09 &lt;zzz&gt; anything else on 1) ?
20:01:35 &lt;zzz&gt; 2) 0.9.41 release status (zzz)
20:01:46 &lt;sadie__&gt; hi
20:01:54 &lt;eyedeekay&gt; Hi
20:02:09 &lt;zzz&gt; we're wrapping up the review period. I expect to have in-net updates tomorrow morning, with other things to follow
20:02:44 &lt;zzz&gt; and then we'll do it all again for 42
20:03:06 &lt;zzz&gt; anything else on 2) ?
20:03:48 &lt;zzz&gt; 3) LS2 status (zzz)
20:04:01 &lt;zzz&gt; we're making slow but steady progress
20:04:11 &lt;zzz&gt; .41 has support for per-client auth
20:04:22 &lt;zzz&gt; garlic farm is also progressing, slowly
20:04:46 &lt;zzz&gt; we plan one new I2CP message for .42 to pass blinding info from the client to the router
20:05:12 &lt;zzz&gt; we're continuing to make headway on proposal 144 for new encryption, but it's really difficult
20:05:42 &lt;zzz&gt; I hope to have a good spec for 144 in a couple of months, maybe have some test code out there late this year
20:05:55 &lt;zzz&gt; as always our meetings are mondays 6:30 PM UTC in #ls2, all welcome
20:06:07 &lt;zzz&gt; anything else on 3) ?
20:06:37 &lt;zzz&gt; 4) I2P Browser "labs" project status (meeh)
20:06:45 &lt;zzz&gt; meeh what's the latest on the browser?
20:07:38 &lt;zzz&gt; ok I guess he's not here
20:07:51 &lt;zzz&gt; 5) muwire.i2p console home page request (zlatinb)
20:08:01 &lt;zlatinb&gt; hi
20:08:07 &lt;zzz&gt; http://zzz.i2p/topics/2722
20:08:11 &lt;zzz&gt; tell us about your site please
20:09:30 &lt;zlatinb&gt; MuWire is a general purpose file-sharing application which works on top of i2p.  The site contains download links, screenshots and general information about the application.
20:10:05 &lt;zlatinb&gt; I believe MW is of general interest and usefulness to the i2p community; it has been growing quickly and drawing lots of interest.
20:10:22 &lt;zzz&gt; anybody have any comments about this request? for it? against it?
20:10:41 &lt;zzz&gt; or any questions?
20:11:39 &lt;zzz&gt; I support the request, I think it's a cool application that is only useful if it has lots of users, and we can help that by putting it on the console
20:11:55 &lt;zzz&gt; sadie__, ? eyedeekay ?
20:12:23 &lt;sadie__&gt; I support the request
20:12:30 &lt;eyedeekay&gt; I also support it.
20:12:49 &lt;zzz&gt; super. hearing no objections, we'll stick it in for .42
20:12:54 &lt;zzz&gt; anything else on 5) ?
20:13:41 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:13:45 &lt;zzz&gt; take it away zab
20:14:15 &lt;zlatinb&gt; Hi, lets do the scrum in parallel.  Please say in a few words : 1) what have you been doing since the last scrum 2) what you plan to do next month 3) if you have any blockers or need help.  When done, say EOT
20:15:38 &lt;zzz&gt; 1) bug fixes, per-client authentication, garlic farm, new encryption, more bug fixes, getting ready for the release, early work on new things for .42
20:15:39 &lt;zlatinb&gt; me: 1) just a small tweak to the RouterContext api to allow custom log manager 2) Have more Router/RouterContext changes Id like to do to make things better for embedding the router.  May also work on garlic farm if that opens up. 3) No blockers really, just would be nice to have Maven streamlined
20:15:41 &lt;zlatinb&gt; EOT
20:16:41 &lt;zzz&gt; 1a) lots of android bug fixes and cleanups 2) .41 release, config split for .42, new i2cp message for .42, prop 144 new encryption work
20:17:20 &lt;sadie__&gt; I continued to work on the console - updated logo added to both themes. Traveled to Tunis for RightsCon and made more connections in the community. Community outreach, testing, going through tickets and getting used to tx. 
20:17:37 &lt;zzz&gt; 2a) getting ready for defcon, more garlic farm work, working with #ls2 team on tunnel building for routers with new encryption
20:17:45 &lt;sadie__&gt; next month Threat model update, user research and persona creation, funding outreach 
20:17:45 &lt;eyedeekay&gt; I have been working on split tunnel configuration, recently it's been testing on multiple platforms. I made a webextension to improve how browsing works on Android by automatically configuring the browser, wrote/mirrored a bunch of blog posts, and worked on the web site. 2) Finish testing split tunnels and get them into the router for .42. Work with meeh on the browser. 3) no blockers EOT
20:17:46 &lt;sadie__&gt; EOT
20:18:01 &lt;zzz&gt; 3) no blockers, EOT
20:18:15 &lt;zlatinb&gt; thanks, thats I believe everyone &lt;/scrum&gt;
20:18:22 &lt;meeh&gt; I'm writing
20:18:24 &lt;meeh&gt; moment
20:18:37 &lt;zzz&gt; ok
20:21:29 &lt;meeh&gt; I've been working mainly on the browser, also looked into the maven dependencies issue, documentation and also looked into how much of a hassle it would be to build the browser for android so we can deprecate the internal one in our app.
20:22:29 &lt;zzz&gt; meeh was that 1) ? please give 2) and 3) followed by EOT
20:25:34 &lt;meeh&gt; 1) yea, above 2) browser: get user documentation ready, make current features stable, finish the rebranding specially in terms of icons and graphics. osx launcher: finish the torrent snark share feature. android: finish the evaluation of how much hassle a port of the browser would be - tor does the same now, and given we're using much of the same and build scripts it's maybe doable. and lastly, for the donations 
20:26:39 &lt;meeh&gt; 3) no blockers, and no help needed beyond always happy to accept PRs for browser stuff and specially android stuff which I'm not really skilled at
20:27:03 &lt;zzz&gt; EOT?
20:27:07 &lt;meeh&gt; EOT
20:27:14 &lt;zzz&gt; ok thanks meeh
20:27:22 &lt;zzz&gt; so that's it for 6) scrum
20:27:34 &lt;zzz&gt; let's circle back to 4) I2P Browser (meeh)
20:28:06 &lt;zzz&gt; could you please give us a status if there's anything more to add than what was in your scrum?
20:28:56 &lt;zzz&gt; last release, next release, stability, features, ... ?
20:30:21 &lt;meeh&gt; I think we have coverd most of the icon graphics in the browser project, however we also got some images (I specially recall the onboarding wizard now) needs to be repaced with something, same goes for text. Also the last week showed that it takes roughly 1-2days (up to 48hrs) for us to react on a security issue (that was, from when I had time until it was built)
20:34:05 &lt;meeh&gt; developer documentation shoud be enough for a while, the user documentation is soon done, trying to not rip off too much from places like mozilla and such in the attempt. Our approach to modifications to the fork is to place most of our logic and features into i2pbutton  - and only do what's really needed in the firefox source, and which so far seem to work well.This also includes translations since firefox 
20:34:05 &lt;meeh&gt; provide their own so the only left out to translate are i2p spesific strings
20:35:01 &lt;zzz&gt; ok thanks for the update. ANything else on 4) ?
20:35:07 &lt;zzz&gt; any questions about the browser?
20:35:16 &lt;meeh&gt; thoughts about moving to a new ESR release is ... bob-bob positive, meaning, I'm quite unsure if it can be done automatic, however the few places that need a patch or two is starting to get really well known for me
20:35:56 &lt;meeh&gt; next release should not be that long, it depends a bit on how much the team wish to fuel the fire in the coming weeks
20:36:35 &lt;zzz&gt; yeah we have to weigh the priorities. I think we're learning more about how much effort it would be to do this for real
20:36:46 &lt;zzz&gt; anything else on 4) ?
20:36:50 &lt;meeh&gt; I really don't have a schedule on that beyond when some new/current feature is done or more done, and/or any security patches are released for android
20:36:53 &lt;meeh&gt; ffirefox**
20:38:10 &lt;zzz&gt; anything else on 4) ?
20:39:05 &lt;zzz&gt; anything else for the meeting?
20:39:54 &lt;zzz&gt; thanks everybody
20:40:01 * zzz *bafs* the meeting closed
</div>
