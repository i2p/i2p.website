---
title: "I2P Dev Meeting - March 04, 2016"
date: 2016-03-04
author: "zzz"
description: "I2P development meeting log for March 04, 2016."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> EinMByte, orignal\_, sadie, str4d, xcps\_, zzz</p>

## Meeting Log

<div class="irc-log">
15:00:05 &lt;zzz&gt; 0) hi
15:00:23 &lt;zzz&gt; 1) structure for these meetings
15:00:32 &lt;zzz&gt; 2) roadmap discussion
15:00:37 &lt;zzz&gt; 0) hi
15:00:41 &lt;zzz&gt; hi
15:00:54 &lt;str4d&gt; hi
15:01:02 &lt;xcps_&gt; hi!
15:01:27 &lt;orignal_&gt; what's up?
15:02:18 &lt;zzz&gt; please review the thread at http://zzz.i2p/topics/2021 and the current roadmap at http://i2p-projekt.i2p/en/get-involved/roadmap
15:02:27 &lt;zzz&gt; 1) structure for these meetings
15:03:22 &lt;zzz&gt; should we go straight into the roadmap or should we talk about high-level priorities first?
15:03:53 &lt;str4d&gt; I'd go with the latter first
15:04:41 &lt;zzz&gt; ok, so in the thread, I threw out two priorities - grow the network, and increase security
15:04:55 &lt;zzz&gt; how do those sound as high-level principles?
15:05:25 &lt;zzz&gt; let's first decide what's important
15:05:32 &lt;EinMByte&gt; They sound as expected, I think
15:05:48 &lt;EinMByte&gt; "grow the network" should be in the broad meaning, though
15:05:57 &lt;str4d&gt; I think those are great as broad themes
15:06:03 &lt;zzz&gt; anonimal threw out a whole bunch more in the thread, but that wasn't really what I was going for
15:06:13 &lt;xcps_&gt; increasing security should be always the most important imho
15:06:28 &lt;zzz&gt; other principles we should consider as we review the roadmap?
15:06:28 &lt;str4d&gt; What IMHO we need to do here is figure out what those actually mean in terms of potential deliverables
15:06:40 &lt;EinMByte&gt; So "grow the network" should also mean "increase research attention"
15:07:00 &lt;zzz&gt; grow the network means a huge variety of stuff - see the thread
15:07:09 &lt;str4d&gt; EinMByte, yah, I think I might have mentioned that in the thread
15:07:36 &lt;zzz&gt; we'll figure out what these mean shortly. at this minute let's agree on whats important.
15:07:58 &lt;str4d&gt; Usability is of big importance to me, and IMHO feeds into the above two areas
15:07:58 &lt;zzz&gt; everything is possible if we keep growing. once we stop growing we are dead
15:08:05 &lt;zzz&gt; agreed str4d 
15:08:41 &lt;str4d&gt; More immediately in terms of increasing our userbase, and more long-term in terms of increasing our public exposure, ease of use by researchers etc.
15:09:11 &lt;EinMByte&gt; Note also that growing is the only way to attract researchers
15:09:25 &lt;zzz&gt; more users bring more devs and more researchers and more content and and and
15:09:37 &lt;EinMByte&gt; Large networks are generally more interesting to study
15:10:05 &lt;EinMByte&gt; So I think we call all agree on those 2 priorities
15:10:16 &lt;zzz&gt; the bulk of our growth in the last year has been from vuze. Which is great but I'd love to have more 'native' growth also
15:10:43 &lt;zzz&gt; but maybe growth in embedded apps, or focusing on applications in general, is the easiest path to growth
15:10:48 &lt;str4d&gt; Yep
15:11:04 &lt;EinMByte&gt; zzz: For a lot of people, it's easier to use an application that runs I2P in the background and handles the configuration for them
15:11:12 &lt;sadie&gt; hi - a little late to the party
15:11:20 &lt;zzz&gt; hi sadie glad you made it
15:11:23 &lt;str4d&gt; That IMHO will come from usability improvements for both the UI and APIs
15:11:42 &lt;str4d&gt; The latter we have already been working on in various threads
15:11:48 &lt;zzz&gt; in some ways, it's the apps that are the UI experts, let them bundle i2p and expose (or hide) it as they see best
15:11:58 &lt;str4d&gt; Mmm
15:12:08 &lt;EinMByte&gt; str4d: That's a different solution to the same problem, yes. And I like it more because bundling I2P with everything doesn't scale IMHO
15:12:30 &lt;str4d&gt; That is kinda the approach I was taking with Android
15:13:04 &lt;EinMByte&gt; There needs to be a way to ensure that people don't have an I2P instance for every application
15:13:12 &lt;zzz&gt; ok, anything else on 1) or should we move on to looking at the roadmap itself?
15:14:00 &lt;str4d&gt; I think everyone here appears to be in rough agreement
15:14:08 &lt;str4d&gt; (no dissent at least :P)
15:14:14 &lt;zzz&gt; let me copy in the lines from the thread. Not as gospel, just for reference
15:14:25 &lt;zzz&gt; Grow the Network
15:14:25 &lt;zzz&gt; Includes: Marketing, joint projects, bundling more stuff, helping others bundle i2p, usability, website improvements, more translations, talks and presentations, articles and stories, UI, Android, Android apps, better GFW evasion, orchid, more libs and tools for client devs, better support for huge websites, supporting alternative router dev, alliances, speedups and efficiency, capacity, increasing limits, getting in
15:14:25 &lt;zzz&gt; to Debian, ...
15:14:25 &lt;zzz&gt; Increase security
15:14:25 &lt;zzz&gt; Includes: Crypto migration, subscription protocol, new transport protocols, pluggable transports, LS2, NTCP2, new DH, key revocation, key storage, code review, sybil, bug fixes, naming, SSL, ...
15:14:46 &lt;zzz&gt; ok, let's move on to 2) the roadmap itself
15:15:10 &lt;zzz&gt; url is http://i2p-projekt.i2p/en/get-involved/roadmap
15:15:50 &lt;zzz&gt; .25 is pretty much done, release in about 10 days, so let's look at the next 4 releases 26-29 for this year
15:16:00 &lt;zzz&gt; which should carry us thru to ccc
15:16:15 &lt;EinMByte&gt; If something is under 2017, e.g., does that mean we start looking into it only then, or does that mean we start the implementation at that point?
15:16:41 &lt;str4d&gt; In terms of things we *need* to do, I'd rank the crypto migration and sybil work as high up there
15:16:42 &lt;zzz&gt; 1mb, we certainly do want to get started on big 2017 things now, like new crypto/dh, ntcp2, etc
15:17:04 &lt;EinMByte&gt; Also, eclipse attacks are a problem right now, IMHO
15:17:05 &lt;zzz&gt; so the roadmap could include prepatory work for those
15:17:23 &lt;str4d&gt; EinMByte, yah, I was bundling that under Sybil
15:17:36 &lt;EinMByte&gt; The whole midnight rotation idea doesn't work and there should be better alternatives, I suppose
15:17:52 &lt;zzz&gt; agreed
15:18:05 &lt;EinMByte&gt; str4d: Sure, it's reasonable to classify them as the same type of attack
15:18:44 &lt;str4d&gt; EinMByte, I discussed this with a few people at RWC
15:18:48 &lt;str4d&gt; Got some thoughts, but hard to discuss right here
15:18:51 &lt;EinMByte&gt; zzz: So if we want to get started on NTCP2/... by 2017 we will need to plan preliminary work
15:18:58 &lt;zzz&gt; right 1mb
15:19:02 &lt;str4d&gt; Yep
15:19:20 &lt;str4d&gt; I want to have planning and research on the roadmap :)
15:19:28 &lt;zzz&gt; here's the issue. I should be working on 26 right now and I don't know what's in it
15:19:39 &lt;orignal_&gt; is it possible to add random padding to existsing NTCP?
15:20:01 &lt;str4d&gt; orignal_, not that I recall, but check the NTCP2 thread
15:20:02 &lt;zzz&gt; so let's spend 10 minutes planning 26, then we can move to the longer term
15:20:13 &lt;str4d&gt; k
15:20:14 &lt;zzz&gt; tell me what I should be doing today
15:20:30 &lt;EinMByte&gt; True, let's focus on that first
15:20:34 &lt;zzz&gt; ok let's see what's on the 25 list that didnt happen
15:20:50 &lt;zzz&gt; wrapper didnt happen, kytv is awol
15:20:54 &lt;EinMByte&gt; "crypto enhancements" is pretty broad
15:21:12 &lt;zzz&gt; what actually happened on crytpo enhancements were some 25519 speedups
15:21:34 &lt;zzz&gt; so the .25 list all actually is in there except wrapper
15:22:00 &lt;zzz&gt; but there's more to do on sybil so lets keep that on the 26 list
15:22:08 &lt;str4d&gt; Great
15:22:25 &lt;str4d&gt; We bumped GMP 6 to .26 because of the need for more testing
15:22:35 &lt;zzz&gt; what else on the 26 list now should be in there or moved
15:23:05 &lt;EinMByte&gt; Eventually preventing sybil will probably be a lot of work, so it seems long-term to me
15:23:10 &lt;EinMByte&gt; (in the sense that we need a good literature review first)
15:23:15 &lt;zzz&gt; orignal, yeah, ntcp w/ padding is ntcp2
15:23:21 &lt;str4d&gt; EinMByte, the Sybil detection tool isn't used for anything yet, that is where more planning is needed :)
15:23:49 &lt;zzz&gt; hottuna4 is unavailable for a month, not sure when that month is up, so gmp6 may or not make it into 26
15:24:02 &lt;str4d&gt; K
15:24:37 &lt;str4d&gt; Subscription protocol improvements for addressbook: that is something that would be very good to add in ASAP, so old Dest owners can migrate to Ed25519
15:24:37 &lt;EinMByte&gt; I think CRLs don't really need a question mark
15:24:47 &lt;str4d&gt; But how long will that actually take to do?
15:25:14 &lt;zzz&gt; we'll need some status update from tuna soon, I expect the deadline for propping big stuff for 26 would be late march / 1st week of april
15:26:10 * str4d still doesn't quite understand the CRL stuff, could zzz expand?
15:26:14 &lt;zzz&gt; 25 will have ability to read crls from disk, so we can include in the update
15:26:35 &lt;zzz&gt; but thats not so helpful because in an update we can just remove the cert and that does the same thign
15:26:56 &lt;zzz&gt; so to get crls out to ppl w/o having to do an update, we would put them in the feed
15:26:57 &lt;str4d&gt; I'm just trying to figure out the use case
15:27:09 &lt;zzz&gt; use case is somebody gets compromised
15:27:20 &lt;str4d&gt; Do we still not do cert pinning?
15:27:30 &lt;zzz&gt; no
15:27:56 &lt;zzz&gt; so i've done 90 % of it and just need to stick the crl into the namespace
15:28:46 &lt;zzz&gt; pinning is tricky and dangerous
15:29:05 &lt;zzz&gt; crypto cat did the 'pinning suicide'
15:29:17 &lt;zzz&gt; where they were pinned but an intermediate changed
15:30:49 &lt;zzz&gt; i don't think pinning replaces cls
15:30:51 &lt;zzz&gt; crls
15:31:21 &lt;zzz&gt; crls not just for ssl, there's reseed and update keys
15:31:58 &lt;zzz&gt; can we keep crls on the list for 26 then? it's almost done
15:32:20 &lt;str4d&gt; What I'm concerned re: pinning is that someone could do e.g. a Quantum Insert-like thing to redirect a reseed domain name, and just put up any valid SSL cert satisfying the domain name requirement, and the routers will accept it
15:33:05 &lt;str4d&gt; And re: CRLs, if we use that to disable a particular certificate, what does that certificate get replaced with?
15:33:25 &lt;zzz&gt; nothing. in the next release there would presumably be  a replacement
15:33:45 &lt;str4d&gt; This is getting a bit far into the weeds
15:34:07 &lt;str4d&gt; I think where I was going is we need to think this over a bit more
15:34:24 &lt;zzz&gt; ok so let's keep crls for 26 but let's discuss the details on it in the next week or two
15:34:30 &lt;zzz&gt; as it's not 100% clear
15:34:38 &lt;zzz&gt; moving on
15:34:42 &lt;zzz&gt; what else ont he 26 list
15:34:43 &lt;str4d&gt; mmk
15:34:50 &lt;EinMByte&gt; ok
15:35:08 &lt;zzz&gt; subscription protocol
15:35:28 &lt;zzz&gt; this is the key for crypto migration of sites
15:35:40 &lt;EinMByte&gt; hosts.txt replacement or what do you mean?
15:36:22 &lt;zzz&gt; yes this is the hosts.txt as a feed thing, with like foo.i2p=b64#sig=b64#cmd=alt ...
15:36:26 &lt;str4d&gt; EinMByte, amending the addressbook subscription protocol with signed key-value metadata
15:36:49 &lt;zzz&gt; proposal is pretty set, but on hold for 18 months or so
15:37:07 &lt;EinMByte&gt; Sure, although wouldn't the size of the hosts file grow too large
15:38:02 &lt;EinMByte&gt; Maybe add a since parameter, to exclude all hosts inserted before some given time
15:38:07 &lt;EinMByte&gt; (to avoid downloading the whole list even if it's not required)
15:38:22 &lt;zzz&gt; this was originally part of the crypto migration plan but it was hard and wasn't the most important part
15:38:49 &lt;zzz&gt; but it's the main thing remaining on crypto migration of signatures
15:39:26 &lt;str4d&gt; EinMByte, we kinda have that already with etag
15:39:28 &lt;zzz&gt; this is another one of those things that's proposed with a lot of specifics, but haven't quite got agreeement and so havent started
15:39:42 &lt;EinMByte&gt; str4d: Is it used, though?
15:39:46 &lt;str4d&gt; EinMByte, yes
15:40:00 &lt;EinMByte&gt; Oh, nvm. in that case
15:40:03 &lt;str4d&gt; This would be no different to the current setup
15:40:20 &lt;zzz&gt; so we'll on the 26 list and start on it asap. not sure if we can get far enough into it for 26 but I'll try. we need to review the thread on zzz.i2p
15:40:22 &lt;str4d&gt; but instead of domain name entries never repeating, they would now repeat in the "stream"
15:40:42 &lt;EinMByte&gt; Is there a particular reason why we need to keep the weird format, though?
15:41:05 &lt;EinMByte&gt; It would seem easier to me if we just used something standard
15:41:06 &lt;zzz&gt; maybe. compatibility with old clients. but we should review and decide for sure if that's important
15:41:20 &lt;zzz&gt; none have us have looked at this in maybe a year
15:41:28 &lt;zzz&gt; so we'll dust it off and take a looko
15:41:32 &lt;EinMByte&gt; zzz: Compatibily could be handled by also providing the old hosts.txt file for a while
15:41:41 &lt;str4d&gt; There's also the broader issue of what to do with e.g. all the "lost" names
15:41:53 &lt;str4d&gt; But that is outside the current discussion
15:41:57 &lt;zzz&gt; yup. we would also need to get the other impls involved
15:42:18 &lt;EinMByte&gt; str4d: I think that's something to decide on when we get a new naming system (if we ever do)
15:42:26 &lt;str4d&gt; For now, I want some way for currently-active domains to update their dests
15:42:26 &lt;zzz&gt; ok, it's staying on the list for 26 for now. next on the list - sybil stuff
15:42:45 &lt;zzz&gt; can we make sybil be automatic? Have you all read the philip winter paper I hope????
15:42:50 &lt;str4d&gt; And the sooner we get the core code in, the sooner we can turn it on in a year or so
15:43:50 &lt;EinMByte&gt; zzz: What paper? I missed something clearly
15:44:27 &lt;zzz&gt; check @__phw on twitter for link
15:45:02 &lt;zzz&gt; we are working with him thanks to a sadie introduction at ccc
15:45:03 &lt;EinMByte&gt; zzz: this: http://arxiv.org/pdf/1602.07787v1.pdf?
15:45:27 &lt;zzz&gt; if it was published in the last coulple weeks, thats it
15:45:59 &lt;EinMByte&gt; Well, it's an eprint from February this year
15:46:09 &lt;zzz&gt; i don't think we're ready for automatic. they arent really either
15:46:22 &lt;zzz&gt; they just spit out an email once a day to the dirauths
15:46:36 &lt;zzz&gt; it's all heuristic and magic on both sides
15:46:49 &lt;EinMByte&gt; So he probably put the eprint online after it got published
15:46:57 &lt;zzz&gt; so I'd like to push automatic stuff out to later in the year
15:47:07 &lt;str4d&gt; EinMByte, 25 Feb is the version I have
15:47:14 &lt;EinMByte&gt; zzz: So how exactly would that work in a decentralized setting?
15:47:44 &lt;str4d&gt; We need to do things from the bottom-up instead of the top-down
15:48:06 &lt;str4d&gt; ie. each router would need to include "potential Sybil candidates" in the peer profiles
15:48:13 &lt;zzz&gt; EinMByte, I don't know. it's hard
15:48:20 &lt;str4d&gt; based on e.g. online times etc.
15:48:30 &lt;EinMByte&gt; Detecting sybil attacks is doable I think, preventing them based on that detection is very hard in a decentralized network
15:48:30 &lt;EinMByte&gt; But I like the challenge
15:48:34 &lt;zzz&gt; we also need gravy who is working on a centralized redo of his setup
15:48:43 &lt;str4d&gt; There is also the possibility of having some kind of more centralized setup
15:48:45 &lt;str4d&gt; Yah, that
15:48:45 &lt;EinMByte&gt; str4d: At that point you need to start assigning trust to each router
15:48:52 &lt;EinMByte&gt; which itself would be a whole anti-sybil system
15:49:07 &lt;str4d&gt; And having routers subscribe to a list of potential sybils
15:49:07 &lt;zzz&gt; kinda like the dagon proposals
15:49:09 &lt;str4d&gt; EinMByte, that is basically what peer profiles are now though
15:49:31 &lt;str4d&gt; where "trust" is currently defined as "reliably routed well for me in the past"
15:49:42 &lt;EinMByte&gt; str4d: Yes, and they've caused a few attacks so far :)
15:50:15 &lt;str4d&gt; Yep
15:50:23 &lt;EinMByte&gt; Also, peer profiles don't really allow you exclude a peer from the network
15:50:31 &lt;EinMByte&gt; Sybil prevention would sort of allow that
15:50:35 &lt;str4d&gt; Peer profiling and peer selection is another of the things I think needs prioritisation
15:50:46 &lt;str4d&gt; EinMByte, they *can*
15:51:01 &lt;zzz&gt; so i propose to change the 26 sybil item to 'continued improvement' but move the 'automatic' part to later
15:51:01 &lt;str4d&gt; Not right now
15:51:11 &lt;str4d&gt; I'm just saying that is where we would put it
15:51:34 &lt;EinMByte&gt; str4d: Yes, that's possible.
15:51:37 &lt;str4d&gt; (in terms of putting Sybil detection and more advanced techniques into I2P's lexicon and architecture)
15:51:53 &lt;EinMByte&gt; In any case, I would not drop the decentralization. It's the nicest part of I2P imho
15:52:14 &lt;str4d&gt; Yep
15:52:27 &lt;EinMByte&gt; (and centralization also leads to various practical attacks anyway)
15:52:43 &lt;zzz&gt; lets move on. streaming improvements? not sure what that is, maybe just perennial 'make it better' item
15:52:49 &lt;str4d&gt; zzz, yep, we can continue to work on that routerconsole page, and then hook it into the peer profiles and selection once we decide on a strategy
15:53:00 &lt;zzz&gt; i can't think of what there is to do specifically on streaming. anybody?
15:53:01 &lt;EinMByte&gt; Sometimes adding a central authority can make your security proof easy, but cause security failure in practice
15:53:20 &lt;str4d&gt; Research and optimizations would be nice
15:53:28 &lt;EinMByte&gt; zzz: Any obvious improvements we could make there?
15:53:30 &lt;str4d&gt; That would be a good candidate for external research
15:53:46 &lt;zzz&gt; we really need a better test setup
15:53:51 &lt;EinMByte&gt; str4d: I agree.
15:53:55 &lt;zzz&gt; add delays / drops, reorder, etc
15:54:04 &lt;EinMByte&gt; We should probably extend our "open research questions" page with that and other stuff
15:54:40 &lt;zzz&gt; i don't have much blue sky things on my list of streaming stuff. it needs to to be test-result-driven
15:54:50 &lt;EinMByte&gt; There may be more improvement in the allocation of tunnels?
15:55:05 &lt;str4d&gt; zzz, there's some GH project that simulates "The Internet" with containers that can do that IIRC
15:55:08 &lt;zzz&gt; so how about we make this item be 'streaming test harness'
15:55:17 &lt;str4d&gt; Dunno how easy it would be tho, we would need a new JVM per container :P
15:55:25 &lt;str4d&gt; EinMByte, mmm
15:55:48 &lt;EinMByte&gt; str4d: shadow could be used, I think. Not sure if it could be integrated with Java but it's on the kovri TODO list
15:55:52 &lt;str4d&gt; That's not really streaming tho, that is at the datagram level
15:56:22 &lt;zzz&gt; the tunnel allocation thing is psi's idea to have the client pick tunnels
15:56:34 &lt;EinMByte&gt; str4d: Yes, I suspect there's more to optimize this
15:56:46 &lt;EinMByte&gt; zzz: I don't really think users are the best optimization algorithms, but maybe
15:57:10 &lt;zzz&gt; it's a violent corruption of our layering, and I don't see any way to do it. but that's what psi is proposing
15:57:19 &lt;EinMByte&gt; ... or probably "client" does not mean user
15:57:32 &lt;zzz&gt; client == client-side of i2cp
15:57:44 &lt;str4d&gt; The thing there is
15:57:54 &lt;str4d&gt; Tor does provide this ability via their Control Socket
15:57:58 &lt;EinMByte&gt; Ok so it does mean that
15:57:59 &lt;str4d&gt; And it is very useful for researchers
15:58:10 &lt;str4d&gt; But they also have a much flatter architecture
15:58:19 &lt;str4d&gt; Whereas we silo different clients from each other via I2CP
15:58:31 &lt;EinMByte&gt; zzz: I'd expect the router to have more relevant information. The client could pass any additional requirements
15:58:41 &lt;zzz&gt; we also have psi's lua hooks for researchers, that never got merged (either in java or kovri), but is still an option
15:59:14 &lt;zzz&gt; see right now the client side doesn't even know about tunnels, so it certainly doesn't have any ability to pick them
15:59:16 &lt;str4d&gt; Speaking to nickm at RWC, he said it was much easier for Tor to maintain a Control Socket interface than a plugin system
15:59:17 &lt;EinMByte&gt; I know that shadow is being used in practice by researchers
15:59:22 &lt;EinMByte&gt; Lua, I don't know
15:59:55 &lt;EinMByte&gt; zzz: So probably the same thing can be achieved by passing the relevant information over I2CP?
16:00:17 &lt;zzz&gt; 1mb, yes, but it would be really fugly
16:00:44 &lt;str4d&gt; We could always restrict it with a -research flag or something
16:00:54 &lt;str4d&gt; (in router.config)
16:01:06 &lt;str4d&gt; That way most users are not exposed to the fugly
16:01:13 &lt;zzz&gt; kovri/i2pd don't have those rigid API barriers between client/router yet, it's easier for the
16:01:20 &lt;zzz&gt; *them
16:01:28 &lt;str4d&gt; And we can define ".research" from the start to mean "We reserve the right to change these APIs"
16:01:44 &lt;str4d&gt; ie. researchers would need to use the .research flag along with a particular version
16:01:57 &lt;str4d&gt; Back to the actual topic of discussion:
16:01:59 &lt;EinMByte&gt; zzz: Re: tunnels. It depends. I think it would make sense to pass information about the intended usage of the tunnel.
16:02:20 &lt;zzz&gt; (FYI this meeting will go 25 more minutes max, to be continued sunday)
16:02:33 &lt;EinMByte&gt; zzz: It's mainly easier for us because shadow is written in C, I think
16:02:42 &lt;str4d&gt; I think this should be pushed into the "needs more research" category
16:02:44 &lt;zzz&gt; the trouble is its not just your tunnels that need to be picked but the far-end's tunnels
16:02:48 &lt;EinMByte&gt; Ok. Let's move on then.
16:03:08 &lt;zzz&gt; ok that's all that's on the 26 list now. What should be added?
16:03:11 &lt;EinMByte&gt; zzz: Doesn't the far-end handle that
16:03:36 &lt;zzz&gt; no, we source-route (i.e. pick the far-end lease out of it's leaseset for his inbound)
16:04:08 &lt;zzz&gt; look at the 27-29 list. what should be pulled in to 26 if anything?
16:04:44 &lt;str4d&gt; I want to start getting the prep work done for new LSs and the netdb
16:04:46 &lt;zzz&gt; here is where all the 'initial work on xxx for 2017' is, but also lots of 2016 stuff
16:05:23 &lt;EinMByte&gt; zzz: I misunderstood what you meant with far-end, nvm
16:05:31 &lt;str4d&gt; The sooner we get that settled down and into the codebase, the sooner the network will have broad support for it
16:06:42 &lt;EinMByte&gt; Note that we (kovri) want specifications
16:06:52 &lt;EinMByte&gt; Otherwise it will be hard to keep up with the implementation
16:07:31 &lt;zzz&gt; sure. anything that's a new specification, we need to all work on together
16:07:36 &lt;EinMByte&gt; str4d: Let's start by listing what LS2 should actually support
16:07:53 &lt;EinMByte&gt; (if that hasn't already been done)
16:09:40 &lt;zzz&gt; basically ls2 is only a couple of things
16:09:59 &lt;zzz&gt; add some space for flags 
16:10:09 &lt;zzz&gt; and enable future crypto
16:10:52 &lt;zzz&gt; but i have all those proposals about better multihoming, plus grothoff-like service lookup
16:11:00 &lt;zzz&gt; anycast
16:11:01 &lt;EinMByte&gt; Do we have specific list somewhere for reference?
16:11:11 &lt;zzz&gt; it's pulled together on zzz, sec
16:11:23 &lt;str4d&gt; EinMByte, I'm slowly working on pulling all that together on the website
16:11:41 &lt;zzz&gt; can we make that faster str4d ? like next week or two?
16:11:47 &lt;str4d&gt; That should go into the .26 list
16:11:50 &lt;str4d&gt; Hmm
16:11:53 &lt;str4d&gt; Possibly
16:11:59 &lt;str4d&gt; I need moar eyes on it
16:11:59 &lt;zzz&gt; without the proposals on a simple list this is way too hard
16:12:08 &lt;EinMByte&gt; str4d: Great. Actually for some of these things a wiki-functionality would be useful
16:12:24 &lt;EinMByte&gt; (idea is that it would go faster)
16:12:48 &lt;zzz&gt; for starters we need a list
16:12:50 &lt;str4d&gt; EinMByte, exactly
16:12:56 &lt;zzz&gt; lets not boil the ocean here
16:13:11 &lt;str4d&gt; I'm trying to move from requiring backend HTML to (currently) rST
16:13:31 &lt;str4d&gt; I need people to look over what I have to check that a) it is usable and b) it doesn't lose anything we currently have
16:13:39 &lt;str4d&gt; Currently it is applied to the spec docs only
16:13:40 &lt;zzz&gt; let's put the proposal thing on the list for 26 and we'll talk later about what that means. But we need forward progress on it asap.
16:13:55 &lt;str4d&gt; But the moment that is solidified, extending it to proposals is trivial
16:13:56 &lt;zzz&gt; i want them on the website. i don't care what form.
16:14:46 &lt;EinMByte&gt; I'm willing to review proposals, but it happens sometimes that I just don't find any text
16:15:10 &lt;EinMByte&gt; (some things on the website are sort of hidden, I think)
16:15:37 &lt;zzz&gt; right
16:16:05 &lt;zzz&gt; we need to move stuff from zzz.i2p to the website in some sort of organization
16:16:13 &lt;EinMByte&gt; str4d: Moving from HTML to something which can be easility converted to various formats is a good thing
16:16:28 &lt;EinMByte&gt; zzz: Yes, absolutely
16:16:35 &lt;str4d&gt; EinMByte, what I need reviewed is in i2p.www.str4d
16:16:36 &lt;EinMByte&gt; Maybe a fixed process for all proposals
16:16:57 &lt;zzz&gt; ok. it's on the list for 26. details to follow. str4d get to work. i wouldn't expect a lot of feedback. Just come up with a new system and we will all fall in line
16:17:02 &lt;str4d&gt; and on http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/
16:17:04 &lt;str4d&gt; EinMByte, if you want to work with me on nailing that down, I could get that finished maybe by .25
16:17:23 &lt;zzz&gt; what else for 26? we gotta wrap this up
16:17:36 &lt;str4d&gt; ( EinMByte, http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/spec specifically)
16:18:14 &lt;zzz&gt; this is very short term stuff. I need to know what to do on monday
16:18:27 &lt;zzz&gt; last call for 26
16:18:41 &lt;str4d&gt; I think the subscriptions stuff will take a while
16:18:49 &lt;str4d&gt; So I'd be happy with that being the main thing
16:18:52 &lt;zzz&gt; agreed. 
16:19:54 &lt;zzz&gt; ok. meeting on sunday same time. we will start with vrp/h1. please review ticket 1119 in advance. after that we will talk about 27-29, time permitting.
16:20:06 &lt;EinMByte&gt; str4d: Any of those that you think require most attention?
16:20:27 &lt;zzz&gt; we can also briefly circle back to 26 on sunday if necessary
16:20:43 &lt;str4d&gt; EinMByte, basically deciding whether the format for writing proposals is usable, and whether it limits what ends up on the website (in either HTML or TXT format)
16:20:45 &lt;zzz&gt; so agenda on sunday will be 1) vrp/h1/1119; 2) 26; 3) 27-29
16:20:57 &lt;zzz&gt; thanks everybody
16:21:25 * zzz *bafs* the meeting closed
16:27:50 &lt;EinMByte&gt; str4d: It is probably OK as long as it can be coverted to most other formats :)
</div>
