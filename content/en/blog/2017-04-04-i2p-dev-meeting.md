---
title: "I2P Dev Meeting - April 04, 2017"
date: 2017-04-04
author: "zzz"
description: "I2P development meeting log for April 04, 2017."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> atoi, echelon, manas, orignal, randomrng, str4d, z3r0fox, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:05 &lt;zzz&gt; 0) Hi
20:00:05 &lt;zzz&gt; 1) 0.9.30 update (zzz)
20:00:05 &lt;zzz&gt; 2) UI branch status - (str4d)
20:00:05 &lt;zzz&gt; 3) I2P Summer Dev plans - (str4d)
20:00:05 &lt;zzz&gt; 4) EdDSA update - (str4d)
20:00:09 &lt;zzz&gt; 0) Hi
20:00:12 &lt;zzz&gt; hi
20:00:28 &lt;manas&gt; Hello
20:00:33 &lt;eche|on&gt; hi
20:01:00 &lt;zzz&gt; 1) 0.9.30 update (zzz)
20:01:24 &lt;zzz&gt; ok, things going well, testers are finding some problems which is great. Jetty 9 going pretty smoothly so far
20:01:35 &lt;z3r0fox&gt; Hi! o/
20:01:54 &lt;zzz&gt; I've identified the plugins that need updating on zzz.i2p... for best results those need to be rebuilt before the release
20:01:56 &lt;eche|on&gt; mostly yes
20:02:04 &lt;eche|on&gt; except for old jetty config files
20:02:24 &lt;zzz&gt; glad that we are doing it now so we will be ready for stretch and zesty
20:02:36 &lt;eche|on&gt; yes
20:02:56 &lt;zzz&gt; thanks to echelon and others for testing. Will probably mark a dev build as -rc sooner than usual to get more testing
20:03:12 &lt;eche|on&gt; ok
20:03:20 &lt;orignal_&gt; hi
20:03:34 &lt;zzz&gt; I have set the checkin deadline for friday april 28, release first week of may
20:03:54 &lt;zzz&gt; anything else on 1) ?
20:04:15 &lt;atoi&gt; when will Java have GOST signatures?
20:04:41 &lt;eche|on&gt; 2019
20:05:01 &lt;zzz&gt; atoi we haven't agreed to the proposal yet, if we do, best guess late next year due to priorities
20:05:02 &lt;eche|on&gt; bu fine with 1, good we have postponed UII
20:05:54 &lt;zzz&gt; but I've made some other proposals (136 and 137) to make the introduction of new sig types easier
20:06:00 &lt;zzz&gt; anything else on 1) ?
20:06:02 &lt;atoi&gt; can't wait to have GOST working 
20:07:22 &lt;zzz&gt; 2) UI branch status - (str4d)
20:07:35 &lt;zzz&gt; str4d, what's the latest on your ui branch?
20:07:53 &lt;str4d&gt; UI branch has been relatively stable for the last few weeks
20:08:28 &lt;zzz&gt; plan is to prop in early may for .31 ?
20:08:57 &lt;str4d&gt; There's some theme updates I need to integrate and push addressing some feedback, but in terms of structure it's basically there
20:09:08 &lt;str4d&gt; Yeah
20:09:13 &lt;zzz&gt; ok great
20:09:19 &lt;zzz&gt; anything else on 2) ?
20:09:24 &lt;eche|on&gt; cant wait to test it^^
20:10:00 &lt;str4d&gt; If anyone wants to test but doesn't want the hassle of building, I'll throw up an i2pupdate.zip once these next theme changes are in
20:10:18 &lt;eche|on&gt; I wait for prop...
20:11:02 &lt;zzz&gt; 3) I2P Summer Dev plans - (str4d)
20:11:19 &lt;zzz&gt; str4d what are the plans?
20:11:47 &lt;str4d&gt; Okay, sadie and I threw around some ideas, and what shook out was that for this Summer Dev, we should focus on speed
20:12:37 &lt;str4d&gt; Because a) it's a logical extension of last year (we made it easier for apps to use I2P, but now we need to make them *want* to), and b) it covers about half of our existing roadmap already
20:13:37 &lt;zzz&gt; ok, where might we find these plans, and how do we find people to do them?
20:14:06 &lt;str4d&gt; sadie took notes from my rambling, so I'll pester her for them :)
20:14:18 &lt;str4d&gt; I'm basically thinking this means:
20:14:51 &lt;str4d&gt; - Push forward the various proposals that affect speed (LS2, newer E2E encryption, massive multihoming)
20:15:24 &lt;str4d&gt; - Get something running similar to Tor's bwauth that we can use to start collecting metrics specifically about network speed
20:16:27 &lt;manas&gt; I was thinking of writing some code to test I2P speeds with different programs (rsync, torrents, sftp etc)
20:16:34 &lt;str4d&gt; - Expose tunnel selection through I2CP (a la psi's lua stuff)
20:16:51 &lt;manas&gt; I can share that if it will be useful/interesting
20:16:51 &lt;randomrng&gt; massive multihoming &lt;3
20:17:00 &lt;zzz&gt; sounds good. should we put this on the agenda for next month's meeting to get an update?
20:17:00 &lt;str4d&gt; - ElGamal speedups for the short term
20:17:17 &lt;str4d&gt; Yep.
20:17:35 &lt;zzz&gt; I note that most of what's on the .30 roadmap, set only 3 months ago at CCC, is total fiction and will be pushed out. I'll be updating it shortly.
20:18:10 &lt;zzz&gt; anything else on 3) ?
20:18:16 &lt;str4d&gt; We have two months until it will officially start. I'll continue chatting with sadie to flesh out a plan, but what we *really* need is people to pick things they want to work on
20:18:32 &lt;str4d&gt; manas already has a head-start there ;P
20:18:35 &lt;orignal_&gt; what kind of speedup?
20:18:48 &lt;str4d&gt; orignal_, the table precomputation
20:18:48 &lt;manas&gt; :)
20:19:03 &lt;orignal_&gt; mine or something else?
20:19:09 &lt;zzz&gt; if you and sadie document a framework and options that will help people pick things
20:19:22 &lt;str4d&gt; +1
20:19:30 &lt;zzz&gt; anything else on 3) ?
20:19:35 &lt;str4d&gt; orignal_, Won't be yours, because that directly leverages OpenSSL which we don't have access to
20:19:52 &lt;orignal_&gt; I mean basis
20:20:03 &lt;orignal_&gt; not implementation
20:20:28 &lt;str4d&gt; Oh, yes likely based on yours (although I'd want to understand the mathematics myself)
20:21:03 &lt;zzz&gt; 4) EdDSA update - (str4d)
20:21:10 &lt;orignal_&gt; good to know  :)
20:21:13 &lt;zzz&gt; str4d, what's going on with EdDSA?
20:21:39 &lt;str4d&gt; I just pushed EdDSA-Java 0.2.0, over a year after the last release
20:22:28 &lt;orignal_&gt; what's a difference?
20:22:37 &lt;str4d&gt; Includes various cleanups, the soon-to-be-standard encoding for PKI, fixed JCA naming, a Security Provider, and should actually be constant-time now thanks to a third party that had it audited
20:22:59 &lt;str4d&gt; I've pulled the code into i2p.i2p.zzz.test2
20:23:26 &lt;orignal_&gt; any speed improvements?
20:23:30 &lt;str4d&gt; But what it now needs is testing to check that everything still works fine
20:23:45 &lt;zzz&gt; how much testing have you done?
20:23:58 &lt;str4d&gt; orignal_, speed decrease in signing due to making it constant-time (but not that much)
20:24:06 &lt;str4d&gt; zzz, the EdDSA code itself is well-tested
20:24:20 &lt;orignal_&gt; constrant time of signing or verifing?
20:24:32 &lt;zzz&gt; I'm still a skeptic about constant-time, but if we don't do it everybody will complain
20:24:39 &lt;str4d&gt; signing (verifying has never been constant-time, as there's no secret info)
20:25:01 &lt;zzz&gt; str4d, you targeting 31 or 30?
20:25:02 &lt;str4d&gt; What I *haven't* tested yet is how it interacts with the rest of I2P, specifically relating to the JCA naming fixes
20:25:39 &lt;zzz&gt; as I posted on zzz.i2p I think it's a fool's errand to chase the naming guidelines from some RFC
20:25:47 &lt;str4d&gt; Probably too close to 30 to pull in as we're using the code directly instead of the library
20:25:50 &lt;orignal_&gt; the performance botlleneck is verification
20:26:22 &lt;str4d&gt; For my library, it made sense to fix things before 0.2.0 because there wasn't a Provider before, so no one was using the JCA names
20:26:26 &lt;zzz&gt; str4d, the prop will also be merge hell due to the javadoc changes you made that I already fixed in .29, wont be fun
20:27:14 &lt;str4d&gt; Okay, sounds like the plan is to merge i2p.i2p into .test2, fix the merge conflicts, then get people testing it
20:27:25 &lt;zzz&gt; but we've always had a provider. your changes in test2 tended to prefer some github PR over what I already did to accomplish the same thing, so I'm a little skeptical about the whole thing
20:27:42 &lt;zzz&gt; you could prop that way if you want, or just defer the pain until the prop the other way
20:28:23 &lt;str4d&gt; Yes, but if we're honest, I doubt anyone was using it
20:28:31 &lt;zzz&gt; as I said, I defer to you, it's originally your code, but I still want to stare at it
20:29:11 &lt;zzz&gt; I have one router with a EdDSA family key to test. can't remember what format. Remember I made all these fixes almost 4 months ago, since then we've been waiting for you and your RFC friends :)
20:29:11 &lt;str4d&gt; (who wasn't already directly importing i2p.jar, and would already have migrations to do when they upgrade)
20:29:32 &lt;zzz&gt; anything else on 4) ?
20:30:08 &lt;str4d&gt; Not from me :)
20:30:13 * zzz looks for the baffer
20:30:19 &lt;zzz&gt; anything else for the meeting?
20:31:20 &lt;str4d&gt; Tor's next tor-dev meeting in September-ish is likely to be in Montreal
20:31:33 &lt;orignal_&gt; when?
20:31:53 &lt;z3r0fox&gt; Neat
20:31:55 &lt;str4d&gt; ------------------------------------^
20:31:56 &lt;zzz&gt; anything else for the meeting?
20:32:14 &lt;str4d&gt; I'm planning on going
20:32:28 &lt;zzz&gt; thinking of switching teams?
20:32:47 &lt;str4d&gt; Just aiming to influence them ;)
20:33:14 &lt;zzz&gt; save yourself the plane ticket money, that's not going to happen
20:33:24 &lt;manas&gt; Ya Montreal is nice :)
20:33:27 &lt;str4d&gt; Also hoping that, as Summer Dev will have just finished, we'll have some nice speed improvements to talk about there
20:34:28 * zzz *BAFS*** the meeting closed
</div>
