---
title: "I2P Dev Meeting - October 01, 2019"
date: 2019-10-01
author: "zzz"
description: "I2P development meeting log for October 01, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> chisana, echelon, eyedeekay, meeh, nextloop, sadie, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.42 release status (zzz)
20:00:00 &lt;zzz&gt; 2) I2P Browser "labs" project status (sadie, meeh)
20:00:00 &lt;zzz&gt; 3) Outproxy use cases / status (sadie)
20:00:00 &lt;zzz&gt; 4) 0.9.43 development status (zzz)
20:00:00 &lt;zzz&gt; 5) Proposals status (zzz)
20:00:00 &lt;zzz&gt; 6) Status scrum (zlatinb)
20:00:05 &lt;meeh&gt; hi
20:00:05 &lt;zzz&gt; 0) Hi
20:00:08 &lt;zzz&gt; hi
20:00:16 &lt;zlatinb&gt; hi
20:00:18 &lt;nextloop&gt; Hi
20:00:23 &lt;sadie__&gt; hi
20:00:49 &lt;zzz&gt; 1) 0.9.42 release status (zzz)
20:01:12 &lt;zzz&gt; 42 release was 5 weeks ago, I believe the only remaining items as of a month ago were the client lib and a new bote android release, and the deb/ubuntu official
20:01:19 &lt;zzz&gt; those are all done
20:01:41 &lt;zzz&gt; not much else to say about .42, which seems to be running well
20:01:46 &lt;zzz&gt; anything else on 1) ?
20:02:29 &lt;zzz&gt; 2) I2P Browser "labs" project status (sadie, meeh)
20:02:37 &lt;eyedeekay&gt; Hi everybody
20:02:45 &lt;meeh&gt; we're in route on all the tasks, I've also started the initial patching of ESR68 which would be our new beta by 31 dec.
20:02:46 &lt;zzz&gt; sadie, meeh, what can you tell us about this new project and product, what's the status?
20:03:01 &lt;chisana_&gt; hi
20:03:02 &lt;sadie__&gt; Beta 7 will be released October 23 or immediately after 0.9.43 is tagged. As of today, we are on track with the roadmap items for the upcoming release. A tentative roadmap for future releases has been created, taking us up until June 2020 
20:03:04 &lt;zzz&gt; what is the next task, or next release meeh?
20:03:07 * chisana_ lurks
20:03:13 &lt;meeh&gt; oct 23
20:03:33 &lt;meeh&gt; or as soon as 0.9.43 is out on that date or after
20:03:36 &lt;meeh&gt; depends on us
20:03:50 &lt;zzz&gt; can you two please tell us where the roadmap is, and what's going to be in beta 7?
20:04:39 &lt;sadie__&gt; The items on the Roadmap are on track as of taday
20:05:00 &lt;zzz&gt; is the roadmap posted anywhere where people can look at it?
20:06:27 &lt;meeh&gt; the next release would for the most contain bugfixes, stability patches, better initial dialog window "backend"
20:06:35 &lt;eyedeekay&gt; These are the items that are also on the project roadmap for 9.43.
20:07:17 &lt;meeh&gt; if mozilla has any patches we should include by that time, those will be added as well
20:07:18 &lt;zzz&gt; ok, so the roadmap for beta 7 is on the i2p roadmap on our website, people can look at it there
20:07:29 &lt;sadie__&gt; yes
20:07:36 &lt;zzz&gt; is the roadmap through June 2020 posted anywhere for people to look at it?
20:07:56 &lt;sadie__&gt; not yet
20:07:57 &lt;eyedeekay&gt; Not yet, can be soon.
20:08:17 &lt;zzz&gt; ok. anybody have any questions for the browser team?
20:09:03 &lt;zzz&gt; anything else on 2)? anything else the team wants to say about the browser?
20:09:26 &lt;sadie__&gt; please test, join the mailing list!
20:09:44 &lt;zzz&gt; want to plug how to subscribe to the mailing list sadie?
20:10:02 &lt;meeh&gt; available at http://lists.i2p or https://lists.i2p.email
20:10:17 &lt;zzz&gt; great
20:10:20 &lt;sadie__&gt; sure - everything you need can be found on the site https://geti2p.net/en/browser/develop
20:10:25 &lt;zzz&gt; anything else on 2)?
20:11:01 &lt;zzz&gt; 3) Outproxy use cases / status (sadie)
20:11:13 &lt;zzz&gt; sadie, tell us about the outproxy project status please
20:11:16 &lt;sadie__&gt; Open Outproxy MVP has been made, we are almost there with the Friends and Family MVP, but still need to gather more information around admin, logging and reporting requirements. Meetings will resume week of October 21.  
20:12:06 &lt;sadie__&gt; I have some new ideas / thoughts about how to handle admin, and more research to do ahead of the next meeting
20:12:15 &lt;zzz&gt; by "made" you don't mean that we've finished development I hope... and could you define MVP for everybody please?
20:12:40 &lt;sadie__&gt; Minimal Viable Product
20:13:03 &lt;sadie__&gt; no - we are still working on requirements in a few areas
20:13:16 &lt;zzz&gt; so by 'made' you mean a list of requirements, right?
20:13:32 &lt;sadie__&gt; correct!
20:14:10 &lt;zzz&gt; where can people see that list, and what's the best way for people to get feedback to you about it?
20:15:05 &lt;sadie__&gt; I will update trac, and invite people to join in the conversation there
20:15:40 &lt;zzz&gt; please tell everybody where on trac they will be able to see it?
20:16:07 &lt;sadie__&gt; one moment
20:17:04 &lt;zzz&gt; while you're looking, I'll comment that the target for this is next year... not for .43 or .44
20:17:14 &lt;zzz&gt; for the implementation, that is
20:17:46 &lt;zzz&gt; any questions or comments about the outproxy project, while she's looking?
20:19:00 &lt;sadie__&gt; #2472 was where we began the discussion 
20:19:00 &lt;zzz&gt; anything else on 3) ?
20:19:59 &lt;zzz&gt; ok, so you'll put the requirements list up on ticket 2472 and that's where you would like feedback, right?
20:20:17 &lt;sadie__&gt; correct
20:20:27 &lt;zzz&gt; super
20:20:56 &lt;zzz&gt; 4) 0.9.43 development status (zzz)
20:21:19 &lt;zzz&gt; the website has the roadmap for .43, including the browser items for beta 7, as previously mentioned
20:21:46 &lt;zzz&gt; we're 5 weeks in on the development for .43, with a release expected about 3 weeks from today
20:22:12 &lt;zzz&gt; things are going well, with some IPv6 fixes, and more work on making encrypted ls2 easier to use
20:22:52 &lt;zzz&gt; anybody else want to tell us what you're working on for .43, besides the browser beta 7?
20:23:36 &lt;zzz&gt; tag freeze will be a week from tomorrow, and I'll update transifex at that time and let everybody know to start translating
20:23:42 &lt;zlatinb&gt; hopefully Ill get around to testing servlet 3.0 annotation scanning
20:24:12 &lt;zzz&gt; ok, yeah, I'd like to finish that if you need it, or can it if you don't :)
20:24:18 &lt;meeh&gt; improving the jlinked build of ours, which is related to browser stuff doh, but still on the java codebase
20:24:42 &lt;sadie__&gt; IDK and I are working on a new set up wizard and new website menu navigation has been done. I will make more cosmetic changes to console css
20:24:47 &lt;meeh&gt; I'll guess we look into more on that topic as well as the addressbook is broken when using jlink
20:25:13 &lt;zlatinb&gt; yeah and plugins too - but those are probably going to stay broken for a while
20:25:19 &lt;zzz&gt; oh, and we'll be working on android fixes for 43 next week
20:26:38 &lt;zzz&gt; I don't think you want to bother enabling router plugins for the browser, but maybe others are pushing you for it? worth investigating further
20:27:04 &lt;zzz&gt; anything else on 4) ?
20:28:21 &lt;zzz&gt; 5) Proposals status (zzz)
20:28:45 &lt;zzz&gt; the sole focus of the #ls2 proposals team in the last month has been prop. 144 - new encryption
20:29:02 &lt;zzz&gt; we're getting close to a complete and consistent spec, and we've started writing some test code
20:30:01 &lt;zzz&gt; I expect some of that code to get into the java .44 release - not .43 - but it's going to be early next year before it's really finished up in the live net
20:30:20 &lt;zzz&gt; and then perhaps another few releases to shake out the bugs
20:30:45 &lt;zzz&gt; but it's exciting as we are close to replacing one of the original and very slow crypto algorithms, ElGamal
20:31:28 &lt;zzz&gt; I expect we'll then turn to another part of the ElGamal replacement, with proposal 152, for how we do tunnel builds
20:31:46 &lt;zzz&gt; but we could decide to work on "SSU2" as well... we haven't talked about it
20:31:56 &lt;zzz&gt; those would be for mid-to-late next year I'd guess
20:32:33 &lt;zzz&gt; the team is working well together and we've been working on 144 for almost a year, so we'll all be very happy to be done with it in the coming months
20:32:43 &lt;zzz&gt; any questions on these or any other proposals?
20:33:19 &lt;zzz&gt; anything else on 5) ?
20:34:00 &lt;zzz&gt; 6) status scrum (zlatinb)
20:34:04 &lt;zzz&gt; take it away zab
20:34:29 &lt;zlatinb&gt; Hi, briefly describe 1) what youve been doing last month 2) what you plan to do next month 3) any blockers or help needed?  Say EOT when finished
20:34:59 &lt;meeh&gt; Its been quite much initial work on the browser project, both due to the integration of the router and the learning experience of the whole Firefox codebase, build system and architecture to get to a level that we can say we got things under control. Were about to have nightly builds and CI ready for both the esr60 and esr68 branches as well as pull requests that we might receive.
20:35:01 &lt;meeh&gt; The artifact builds are also a goal to archive, which would enable people with weaker hardware to download parts of the Firefox build to reducing the heaviest compile operations, and the development less of a hassle. Also been looking into unit and regression testing for the browser to avoid stupid bugs and to make the product more stable and reliable.
20:35:01 &lt;meeh&gt; Were also closing in to having our customized build scripts thats not based upon tors perl build script base, both to support remote builds and the fact that were not many knowing perl. Beyond this Ive also done some reading and research in the legal system here for running our organization. Initial work on the logging policy of project servers. 
20:35:05 &lt;meeh&gt; EOT
20:35:18 &lt;zlatinb&gt; me: 1) testnet-ing jogger patches, some jlink work 2) more testnet, servlet 3.0 3) no blockers EOT
20:35:20 &lt;sadie__&gt; Attended Our Networks last weekend in Toronto, drew up new set up wizard to be implemented in the release by IDK, getting more cosmetic css changes decided on for the next release, moving outproxy and browser consensus along, community outreach and more UX funding has been applied for. Next month, will be focusing on funding options , new PR strategies, 36c3 outreach, getting an intro to I2P slide 
20:35:20 &lt;sadie__&gt; deck finished for future talks that we can all use, susi mail improvements, and continuing to work on browser and outproxy. EOT
20:35:32 &lt;zzz&gt; 1) bug fixes, IPv6, ls2 encryption, proposal 144
20:36:06 &lt;eche|on&gt; server running, the same, no blockers
20:36:25 &lt;zzz&gt; 2) bug fixes, IPv6, ls2 encryption, proposal 144 spec and test code, prep and release 0.9.43, more outproxy meetings and definition
20:36:48 &lt;zzz&gt; 3) no blockers, EOT
20:37:11 &lt;zlatinb&gt; scrum.setTimeout(60*1000);
20:37:25 &lt;zzz&gt; eyedeekay?
20:37:35 &lt;eyedeekay&gt; just a moment
20:37:55 &lt;eyedeekay&gt; I've been working on upgrading the bandwidth wizard to make it work better with the I2P browser and in general appear more modern and less confusing. I've also been working on organizing, de-duplicating, and improving SAM libraries and making small changes to the browser. Next month I'll be helping with the browser mostly, but I have a few things I may propose in i2ptunnel as well. No blockers.
20:38:41 &lt;zzz&gt; sadie__, or eyedeekay, have a link to an Our Networks trip report for people to read?
20:38:48 &lt;meeh&gt; no blockers, most of mentioned tasks are continuing (I'll keep on working on them in the future)
20:39:16 &lt;sadie__&gt; not - we need to get that done. It will be on the site blog
20:39:29 &lt;eyedeekay&gt; I'll put mine up on the blog this week.
20:39:47 &lt;zlatinb&gt; thanks, I think thats everyone, scrum end
20:40:03 &lt;zzz&gt; that's it for 6)
20:40:21 &lt;zzz&gt; anybody else have any questions or comments or something to add? There's definitely a lot going on!
20:41:11 &lt;zzz&gt; anything else for the meeting?
20:41:21 * zzz looks for the baffer
20:42:05 &lt;zzz&gt; there it is...
20:42:15 * zzz *bafs* the meeting closed
</div>
