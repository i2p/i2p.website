---
title: "I2P Dev Meeting - March 03, 2020"
date: 2020-03-03
author: "eyedeekay"
description: "I2P development meeting log for March 03, 2020."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, eyedeekay, sadie, mikalv, zzz</p>

## Meeting Log

<div class="irc-log">
20:59:49 &lt;eyedeekay&gt; Hi everybody, about a minute until meeting time, who all is here?
20:00:33 &lt;eche|on&gt; Ok, it is time. Welcome to the IRC dev meeting 3rd march 2020. 
20:00:40 &lt;eche|on&gt; Agenda:
20:00:40 &lt;eche|on&gt; 0) Hi
20:00:40 &lt;eche|on&gt; 1) 0.9.45 release status 
20:00:40 &lt;eche|on&gt; 2) 0.9.46 plans
20:00:40 &lt;eche|on&gt; 3) I2P Android state/future
20:00:40 &lt;eche|on&gt; 4) MTN =&gt; Git plans
20:00:40 &lt;eche|on&gt; 5) misc - UX plans for 2020; donation page
20:01:28 &lt;eche|on&gt; so, as the old baffer is nearly unuseable for me, and I do not have a new one yet, lets start
20:01:31 &lt;eche|on&gt; 0) hi
20:01:33 &lt;nextloop&gt; hi!
20:01:38 &lt;eche|on&gt; I am here, eyedeekay is here, nextloop is here
20:01:40 &lt;zzz&gt; hi
20:02:21 &lt;eche|on&gt; ok, lets go on to 1)
20:02:36 &lt;eche|on&gt; 0.9.45 was released some days ago and it looks fine so far
20:02:42 &lt;eche|on&gt; any comments?
20:03:03 &lt;zzz&gt; all went smoothly on my side
20:03:11 &lt;nextloop&gt; what's the status of android?
20:03:16 &lt;zzz&gt; in-net, PPA, deb repo. No major reports so far
20:03:31 &lt;eche|on&gt; android still not done, see point 3
20:03:34 &lt;zzz&gt; I leave it to you to report maven/fdroid/android/mac, I have no insights on that
20:03:47 &lt;eche|on&gt; mac was built and put online
20:04:09 &lt;eche|on&gt; from my side it went well enough
20:04:13 &lt;eche|on&gt; hi sadie_ 
20:04:45 &lt;eche|on&gt; ok, and now go on to 2, the 0.9.46 plans
20:04:55 &lt;eche|on&gt; zzz: any plans for 0.9.46 on your roadmap?
20:05:17 &lt;sadie_&gt; hi
20:05:51 &lt;zzz&gt; rrd4j is in replacing jrobin
20:05:56 &lt;zzz&gt; about 30 checkins so far in a week
20:06:10 &lt;zzz&gt; orignal and I hope to finish up ratchet (prop. 144)
20:06:28 &lt;eche|on&gt; good pace, will slow down for sure. Will ratchet be in .46 or a maybe?
20:06:41 &lt;zzz&gt; jogger SSU fixes... maybe... maybe not...
20:07:23 &lt;zzz&gt; ratchet is in 45, it works, but a lot of the details aren't finished, hopefully will be for 46
20:07:36 &lt;eche|on&gt; ok, good.
20:08:15 &lt;zzz&gt; ratchet todo list http://zzz.i2p/topics/2639
20:08:49 &lt;eche|on&gt; whats the estimated timeframe for a 0.9.46 release? may?
20:08:50 &lt;zzz&gt; what's everybody else's plans?
20:09:15 &lt;eche|on&gt; eyedeekay, sadie, plan for 0.9.46 ?
20:09:18 &lt;eyedeekay&gt; My top priority is the readme located in the router console at this time, currently I am slightly blocked on a chat recommendation still but will resolve that soon. I'll be building on this to progressively work on our in-console help.
20:09:24 &lt;zzz&gt; late may is my proposal, subject to other's agreement
20:10:07 &lt;eche|on&gt; ok, late may looks good, will verify with others the next days.
20:10:20 &lt;eyedeekay&gt; I am happy with late May
20:10:32 &lt;mikalv_&gt; same
20:10:43 &lt;eche|on&gt; ok, any other notes on 0.9.46 plans?
20:10:51 &lt;eche|on&gt; comments, questions?
20:11:24 &lt;mikalv_&gt; no but we should land the android architecture support question now that we got everyone here
20:11:32 &lt;eche|on&gt; thats point 3 :-)
20:11:44 &lt;mikalv_&gt; basically google says: support x64 or drop the platform (if only provided 32bit)
20:11:47 &lt;eche|on&gt; wo which we come now after no one stood up for another question on point 2
20:11:56 &lt;mikalv_&gt; great
20:11:59 &lt;eche|on&gt; mikalv_: whats the state of android 0.9.45 ?
20:12:31 &lt;mikalv_&gt; I've built it, got google's complaint, and awaited this meeting for a administrative decision to what we should do
20:12:48 &lt;mikalv_&gt; if we should drop mips and such, or try produce the 64bit binaries for it
20:13:04 &lt;zzz&gt; whats your recommendation?
20:13:34 &lt;mikalv_&gt; once that's landed, we should be ready to release at any time if we remove it, and not sure if we need to produce the 64bit binaries as I've not tried that before
20:13:42 &lt;eche|on&gt; IMHO not much MIPS and x86 android devices available, so drop them for 0.9.45, but keep it on mind
20:13:57 &lt;sadie_&gt; For me ,Information architecture  review of  console and website , then Identity and values workshop with Ura and Simply Secure. Post install work, infrastructure and policy review
20:14:06 &lt;mikalv_&gt; I tried to get google play to somehow tell me how much they where used (the different architectures) but I couldn't find any metrics for it
20:14:10 &lt;zzz&gt; you have user stats mikal?
20:14:22 &lt;eche|on&gt; ok, sadie, point 2 addition, noted :-)
20:14:23 &lt;mikalv_&gt; the closest we get is a list of devices 
20:14:27 &lt;nextloop&gt; the architecture is just relevant for the NDK jbigi lib right?
20:14:35 &lt;mikalv_&gt; but then, we need to know what arch all the different devices is 
20:14:38 &lt;zzz&gt; sounds like an easy decision to me
20:14:40 &lt;eche|on&gt; yes, nextloop, mostly yes
20:14:44 &lt;mikalv_&gt; yes nextloop 
20:14:48 &lt;nextloop&gt; because it gets built from source every f-droid release
20:15:17 &lt;nextloop&gt; i never veryfied if it really gets used or uses the java fallback
20:15:25 &lt;eche|on&gt; ok
20:15:25 &lt;mikalv_&gt; but is that for the 64bit versions so the f-droid has binaries that don't exists in the gplay version?
20:16:24 &lt;nextloop&gt; it just runs the shell script i believe. whatever is built there gets built
20:16:50 &lt;eche|on&gt; mikalv_: please check the shell script/f-droid version, if 64 bit available, use it, else drop that architecture
20:17:24 &lt;mikalv_&gt; okay I'll do so then unless any objections
20:17:35 &lt;eyedeekay&gt; No objections from me.
20:17:40 &lt;mikalv_&gt; (?)
20:17:43 &lt;mikalv_&gt; great
20:17:46 &lt;eche|on&gt; now to the more interesting point: future of android I2P version. As bote is nearly dead and not in use, and no dev available, the use case for android I2P is gone
20:17:57 &lt;eche|on&gt; do we want a future android I2P release?
20:18:09 &lt;eche|on&gt; even without bote and nearly null use case?
20:18:16 &lt;eche|on&gt; eyedeekay: opinion? zzz?
20:18:28 &lt;zzz&gt; your premise is that the sole use case for the android router app is bote?
20:18:47 &lt;eche|on&gt; as the browser has other issues (as mikalv_ told me), what is left?
20:18:59 &lt;eyedeekay&gt; People are using Java I2P on Android for non-Bote things. There's a dude hosting Yacy on top of termux or some crazy nonsense like that. I don't want to stifle people.
20:19:03 &lt;eche|on&gt; beside being a simple router on small devices
20:19:18 &lt;zzz&gt; it's simply not true that browsing is broken
20:19:34 &lt;mikalv_&gt; its basically no "non technical" way to use the android version of today
20:19:39 &lt;eche|on&gt; ok, good, so your both vote for future of android
20:19:41 &lt;zzz&gt; right idk?
20:19:48 &lt;mikalv_&gt; you can tweak firefox in about:config which mozilla warns you to not do
20:20:06 &lt;eyedeekay&gt; Yes I think Android can have a future.
20:20:06 &lt;mikalv_&gt; but beyond that, it need some kind of life purpose in my point of view
20:20:45 &lt;eche|on&gt; but as I have seen also, android will change owner to eyedeekay, is that correct?
20:20:46 &lt;zzz&gt; what's behind this? does the team not want to support it?
20:20:51 &lt;eyedeekay&gt; Yes
20:21:00 &lt;eche|on&gt; O
20:21:01 &lt;eche|on&gt; ok
20:21:12 &lt;eche|on&gt; zzz: I try to figure opinions and ideas
20:21:26 &lt;eche|on&gt; and as it looks, eyedeekay will support androif for 0.9.46 and further on
20:21:35 &lt;eyedeekay&gt; I will continue to at least maintain Android builds, I will take ownership of it. I do wish to keep supporting it. Just to clarify
20:21:45 &lt;zzz&gt; I think android is important. Right now we're providing terrible support. We aren't fixing _any_ bugs and there's no new development
20:21:48 &lt;eche|on&gt; and as users seem to use it, it will be supported
20:22:12 &lt;zzz&gt; if we can't increase our support with the current team than we should hire somebody new to do it
20:22:33 &lt;eche|on&gt; ok
20:22:48 &lt;sadie_&gt; I have applied for support that I would suggest going to Android. No answer yet.
20:23:12 &lt;sadie_&gt; I think that Android is important
20:23:38 &lt;eche|on&gt; so android i2p will live on and we try to get better support for it, at least better than just supllying new releases
20:23:59 &lt;eche|on&gt; and if funding is available, get a dev on funds to support android dev
20:24:25 &lt;eche|on&gt; any questions, comments, hints on point 3 android?
20:25:43 &lt;eche|on&gt; ok, going on to topic 4) the forthcoming monotone to Git translation
20:26:20 &lt;eche|on&gt; we decided to drop monotone and use git instead, a translation plan is still in work to maintain best useability and features which are needed for I2P development
20:26:40 &lt;eche|on&gt; currently eyedeekay did setup a git server on http://git.idk.i2p and made a howto on https://github.com/eyedeekay/git-over-i2p/blob/master/GIT.md
20:27:02 &lt;eche|on&gt; we do work on getting trac into the git instance and migrate all the tickets into git
20:27:26 &lt;eche|on&gt; after that migration is done securly and verified, we decide on a date to switch
20:27:46 &lt;eche|on&gt; currently we do look out for testers of the guide and the git server inside of I2P 
20:28:03 &lt;eche|on&gt; and for sure: for more hints, tips, ideas, feature requests on this topic
20:28:07 &lt;eche|on&gt; so, please
20:28:12 &lt;eche|on&gt; eyedeekay: more comments on this?
20:28:39 &lt;eyedeekay&gt; I've also been working on adding SOCKS support to webtorrent, which will hopefully make it possible for us to use gittorrent as well in the near future.
20:29:19 &lt;eche|on&gt; nextloop: comments? as you do work the sync script currently?
20:29:49 &lt;zzz&gt; is muwire code set up and bridged to GH as we planned?
20:30:18 &lt;eyedeekay&gt; While my testing over the past few weeks has been successful, I would like it very much if people could review my guide and make comments where it could be clarified or simplified.
20:30:37 &lt;nextloop&gt; the topic of breaking connections during initial cloneing is solved by doing shallow clone and iterative unshallowing, am I right?
20:30:46 &lt;eche|on&gt; zzz: no idea yet, not yet worked on my side
20:30:55 &lt;eyedeekay&gt; Yes that works right now.
20:30:56 &lt;zzz&gt; idk?
20:31:13 &lt;eche|on&gt; yes, nextloop, that does help a bit, but even the depth of 1 version is still ~100 MB to fetch
20:31:37 &lt;eche|on&gt; with unshallowing it grows slightly bigger (4-5 times in my experiment)
20:31:49 &lt;zzz&gt; I have a question about user names on git.idk - do we need to pick a username unused on GH, or do we need to defensively register it on GH, to make it all work right?
20:32:12 &lt;nextloop&gt; zzz: github identifies the committers based on e-mail addresses.
20:32:17 &lt;zzz&gt; there was a report on zzz.i2p a while back that there are several fake zzz-i2p accounts on GH. is that a problem?
20:32:42 &lt;nextloop&gt; so if you add your email you use for i2p git to github the commit will be linked to your account
20:33:16 &lt;nextloop&gt; eyedeekay: is the regular torrent archive already in place? if i remember correctly you were working on that
20:33:48 &lt;eyedeekay&gt; Well it's generatable, but there's nothing scheduling it yet
20:34:32 &lt;zzz&gt; so I need to register on git.idk with a valid clearnet email address if I want to (before or after) register on GH? or that's a local setup thing?
20:34:55 &lt;zzz&gt; anyway, we're in the weeds here, sorry, I'll work with idk to figure it out
20:35:17 &lt;eyedeekay&gt; You don't need to pick an unused GH username AFAIK, you could work entirely from the gitlab instance and we wouldn't need github at all
20:35:17 &lt;eche|on&gt; clearnet email should be in this case the i2pmail.org address IMHO
20:35:46 &lt;nextloop&gt; zzz: yes for github you need to verify the email. use i2p-mail.org perhaps?
20:35:54 &lt;eche|on&gt; currently the plan is to use the gitlab (idk in i2p net git instance) for our work and sync to github
20:36:23 &lt;eche|on&gt; the trac tickets would be on in-net gitlab server
20:36:25 &lt;nextloop&gt; eyedeekay: i would be motivated to setup such an automatic archiving
20:36:27 &lt;zzz&gt; I just want to make sure it's not linked to some fake zzz account when it gets bridged to GH
20:36:47 &lt;eche|on&gt; (sorry for the hassle, gitlab and github are both servers with lots of features around git, both do nearly the same tasks)
20:37:18 &lt;eche|on&gt; valid point, zzz 
20:37:47 &lt;eche|on&gt; ok, before going into much deeper details, any more comments?
20:39:06 &lt;eche|on&gt; going on to topic 5 - misc topics. currently 2 from my side: a) donation page and b) UX plans for 2020
20:39:40 &lt;eche|on&gt; 5a) a new donation page is setup by mikalv_ on https://donate.i2p.io/ and those accounts are all benefits to the I2P company mikalv_ is running with torkel in norway
20:40:07 &lt;eche|on&gt; it is live and do collect donations from now on, soon (tm) it will be advertised on webpage and twitter
20:40:24 &lt;eche|on&gt; any comments on this? issues, problems?
20:41:29 &lt;eche|on&gt; 5)b) UX plans for 2020 - sadie is working with elio on a UX project, in whic elio has been granted funds to work on I2P UX 
20:41:42 &lt;eche|on&gt; sadie, any more information, plans, ideas, comments?
20:42:05 &lt;sadie_&gt; Information architecture  review of  console and website , then Identity and values workshop with Ura and Simply Secure will be the work for this month
20:42:41 &lt;sadie_&gt; We have received very good feedback on the set up wizard!
20:43:31 &lt;eyedeekay&gt; From me, the Browser project has been officially placed on hiatus. We pretty much couldn't have picked a worse time to attempt such a thing, as Mozilla's codebase has been changing drastically as we tried to work with it. The project will be revisited when we have less of a moving target. I will be making improvements to I2P and web browsing in less time-dominating projects.
20:43:36 &lt;sadie_&gt; So research, synthesis and documentation phase for now. 
20:44:03 &lt;zzz&gt; eyedeekay, status of beta 8, promised in 'a couple days' at the meeting a month ago?
20:44:24 &lt;eyedeekay&gt; It is cancelled. There was no use in creating it, as it will only be viable for a very short time.
20:44:35 &lt;eche|on&gt; thank you sadie, whats the timeframe for the whole project? end date 
20:44:56 &lt;eche|on&gt; eyedeekay: please announce that on webpage
20:45:21 &lt;eyedeekay&gt; Will do
20:45:22 &lt;sadie_&gt; End date projection for study is mid June
20:45:49 &lt;zzz&gt; if beta 8 would not have been viable for long, I assume beta 7 on our website is long since obsolete and should be removed, for sure
20:45:53 &lt;eche|on&gt; ok, and is there a rough idea at which timepoint UX enhancements will get into I2P code?
20:46:59 &lt;eche|on&gt; sadie?
20:47:28 &lt;eche|on&gt; zzz: that should be done with the announcement of the final end of the browser project
20:47:33 &lt;sadie_&gt; It will not be until after June. We need to go through the process first. If there are improvements we can execute on easily as they are suggested and approved we will.
20:47:35 &lt;zzz&gt; sadie_, is the funding organization for Ura public? and if so who?
20:47:46 &lt;mikalv_&gt; yes the browser project was unluckly started at the wrong time as mozilla rewrote basically everything in their codebase the same year
20:48:05 &lt;anonymousmaybe&gt; i2pbrowser currently has many security vulnerabilities didnt fixed since ages because it didnt catch up with TB/FF patched releases
20:48:09 &lt;mikalv_&gt; so each release had quite some different code than the previous one and so on
20:48:23 &lt;eche|on&gt; sadie_: ok, looks like early 0.9.47, maybe 0.9.48 will be first i2p version whcih will get changes of this project
20:48:25 &lt;sadie_&gt; The funding for this study is provided through usability lab. 
20:48:39 &lt;zzz&gt; which is OTF?
20:48:40 &lt;sadie_&gt; correct ech
20:48:47 &lt;mikalv_&gt; tbb had 10 people rewrite all their patches like three or four times in 2019
20:49:34 &lt;eche|on&gt; https://www.opentech.fund/labs/usability-lab/
20:49:45 &lt;sadie_&gt; OTF Resource Labs 
20:49:58 &lt;zzz&gt; would be good to get some thanks-tweets and a blog post out there if it's public, this is big news that we should be telling people about!
20:50:37 &lt;fug&gt; you should also tell people how you gutted the UI and removed docs
20:51:09 &lt;eche|on&gt; On a minor down side, the InternetFreedomFestival in Valencia, spain, was canclled due to high risk on the corona-virus. 
20:51:18 &lt;eche|on&gt; so new I2P participation in there
20:51:38 &lt;eche|on&gt; zzz: noted and will happen 
20:52:15 &lt;sadie_&gt; zzz, yes I have announced it on forum last week. PR rollout has been planned
20:52:26 &lt;eche|on&gt; any more comments, topics under topic 5) misc?
20:52:51 &lt;eche|on&gt; http://i2pforum.i2p/viewtopic.php?f=27&t=925
20:53:00 &lt;eche|on&gt; is the forum entry with news entries
20:53:10 &lt;fug&gt; zzz: github does detection based on the email specified in commits, said email needs to be registered with a github account, and registration requires sending a confirmation link to the email
20:53:33 &lt;fug&gt; zzz: so in case of your commits with .i2p mail, you won't be able to confirm them
20:53:55 &lt;anonymousmaybe&gt; any road map for i2prouter isolation? https://trac.i2p2.de/ticket/2132
20:54:47 &lt;eche|on&gt; i2p debian package split up is IMHO on hold currently
20:54:51 &lt;eyedeekay&gt; No road map on that yet.
20:55:02 &lt;anonymousmaybe&gt; ah sad..
20:55:22 &lt;eche|on&gt; AFAIK some discussion with the deb maintainer were made, with no productive outcome yet
20:56:02 &lt;anonymousmaybe&gt; ticket already there but no work done for it 
20:56:17 &lt;zzz&gt; no 45 for sid yet either, no news from mhatta
20:56:38 &lt;anonymousmaybe&gt; mikalv_ fixed trac filtering Tor/I2P users? 
20:56:42 &lt;fug&gt; there's https://github.com/tracboat/tracboat for trac-&gt;gitlab migration, has it been evaluated?
20:57:25 &lt;eche|on&gt; IMHO eyedeekay does trying tracboat for the migration, at least the name was mentioned
20:57:28 &lt;fug&gt; where is some information page that describes status of migration to git?
20:57:46 &lt;eche|on&gt; currently no page except for the howto and git server mentioned above
20:57:56 &lt;eche|on&gt; as we are still in early phase
20:58:17 &lt;fug&gt; you still should have a page for that info
20:58:21 &lt;eche|on&gt; noted to create a info page
20:58:22 &lt;mikalv_&gt; I hope it's fixed, has anyone had issues with it the past days?
20:58:38 &lt;eyedeekay&gt; trac? Not lately
20:58:49 &lt;eche|on&gt; yes, mikalv_, there was a user in here trying to push a ticket and got spam blocked
20:58:59 &lt;eche|on&gt; but ok, any other comment for dev meeting?
20:59:09 &lt;zzz&gt; outproxy is still a pile of crap but trac working well for me
20:59:20 &lt;mikalv_&gt; and now we're talking about trac's own system, and not the i2ptunnel right?
20:59:26 &lt;eche|on&gt; yes
20:59:43 &lt;eche|on&gt; uhh, the 60 min limit is here...
20:59:55 &lt;eche|on&gt; any further comments?
21:00:05 &lt;fug&gt; yes, info about developing i2p
21:00:16 &lt;fug&gt; should mention usage of new git instance instead of mtn that no one uses
21:00:45 &lt;eche|on&gt; will be done, if it is valid and verified to be done 100% 
21:01:24 &lt;eche|on&gt; If no other comment gets in, the timeframe of this IRC meeting getting nearly a 60 min, which is a soft border, I would like to close this meeting. Due to a missing appropriate buffer, I'll make a "plopp" sound.
21:01:45 &lt;eche|on&gt; so, ears up: "plopp"
21:01:56 &lt;sadie_&gt; mic drop
21:02:02 &lt;eche|on&gt; dev meeting over. thank you all for your time, ideas and comments
21:02:14 &lt;eche|on&gt; a log will be posted soon
21:02:14 &lt;sadie_&gt; thanks ech
</div>
