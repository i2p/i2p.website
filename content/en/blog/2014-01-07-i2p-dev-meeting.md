---
title: "I2P Dev Meeting - January 07, 2014"
date: 2014-01-07
author: "zzz"
description: "I2P development meeting log for January 07, 2014."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> eche|on2, EinMByte, Giant, kytv, Meeh, str4d, TerraNullius, topiltzin, user, wowa, zzz</p>

## Meeting Log

<div class="irc-log">
20:02:10  &lt;zzz&gt; http://zzz.i2p/topics/1539
20:02:10  &lt;zzz&gt; 0) hi
20:02:10  &lt;zzz&gt; 1) jisko.i2p console home page submission http://zzz.i2p/topics/1539
20:02:10  &lt;zzz&gt; 2) i2pjump.i2p addition http://zzz.i2p/topics/1539
20:02:10  &lt;zzz&gt; 3) Host release files on i2p.no http://zzz.i2p/topics/1390
20:02:10  &lt;zzz&gt; 4) OpenITP audit manager http://zzz.i2p/topics/1533 post #4
20:02:11  &lt;zzz&gt; 5) anything else
20:02:13  &lt;zzz&gt; 6) baffer
20:02:19  &lt;zzz&gt; 0) hi
20:02:24  &lt;zzz&gt; hi
20:02:40  &lt;zzz&gt; 1) jisko.i2p console home page submission http://zzz.i2p/topics/1539
20:02:46  &lt;zzz&gt; Is the jisko op here?
20:03:35  &lt;zzz&gt; any comments on the jisko submission?
20:03:44  &lt;topiltzin&gt; +1
20:03:54  &lt;eche|on2&gt; add it.
20:04:28  &lt;zzz&gt; any objections?
20:07:05  &lt;str4d&gt; hi
20:07:11  &lt;str4d&gt; No objections here
20:07:13  &lt;zzz&gt; great, even jisko's competitor does not object...
20:07:13  &lt;str4d&gt; It's a good alternative to id3nt (which I need to spend some time on sometime)
20:07:13  &lt;str4d&gt; Hey, the more the merrier
20:07:13  &lt;zzz&gt; indeed. I'll add it to mtn
20:07:13  &lt;str4d&gt; Then if I go down, there are alternatives
20:07:13  &lt;zzz&gt; 2) i2pjump.i2p addition http://zzz.i2p/topics/1539
20:07:33  &lt;zzz&gt; I see tuna is not here but he claims he got all the tests to pass
20:07:41  &lt;zzz&gt; and he posted his code
20:07:46  &lt;zzz&gt; any objections?
20:07:54  &lt;zzz&gt; or comments?
20:08:22  &lt;eche|on2&gt; no objections so far
20:09:17  &lt;zzz&gt; there's this guy emailing grothoff saying he was "inspired" by the jump code
20:10:25  &lt;zzz&gt; hearing no objections, I'll ask tuna to add it to mtn since he has privs
20:10:31  &lt;zzz&gt; 3) Host release files on i2p.no http://zzz.i2p/topics/1390
20:10:39  &lt;zzz&gt; Meeh, are you here?
20:11:06  &lt;zzz&gt; we discussed at CCC, he said he almost certainly had the bandwidth
20:11:22  &lt;zzz&gt; are there any reasonable alternatives?
20:11:28  &lt;zzz&gt; google drive seems a little tacky
20:11:30  &lt;zzz&gt; thoughts?
20:11:50  &lt;eche|on2&gt; google drive is a bit ugly, right
20:12:08  &lt;eche|on2&gt; but it is quite hard to block.
20:12:23  &lt;eche|on2&gt; I would run a download host and a copy in google drive
20:12:36  &lt;eche|on2&gt; or somewhere else like Mega, Sharehosts,...
20:12:56  &lt;zzz&gt; str4d, what's the state of the pick-your-mirror code in the website?
20:13:51  &lt;str4d&gt; zzz: mirrors get added in a backend file, and are used to generate the file-specific list.
20:15:16  &lt;zzz&gt; oh, I forgot about the 'select alternate link'
20:15:19  &lt;str4d&gt; Path urls can contain the version if desired (so files can be organized on the server by version)
20:15:31  &lt;str4d&gt; The default is set in the backend code
20:16:05  &lt;zzz&gt; would 'alternate download locations' be better than 'select alternate link' ?
20:16:07  &lt;zzz&gt; or 'view mirror list'
20:16:27  &lt;zzz&gt; thats really nice I forgot that we worked on that a lot
20:17:08  &lt;str4d&gt; 'Any mirror' pick a mirror at random from the list.
20:17:08  &lt;Meeh&gt; zzz: here now!
20:17:15  &lt;zzz&gt; any objections to Meeh being the primary download location?
20:17:23  &lt;Meeh&gt; i2p.nu *
20:17:25  &lt;Meeh&gt; or i2p2.no
20:17:39  &lt;zzz&gt; oh it's not i2p.no?
20:17:40  &lt;eche|on2&gt; currently not, as long as it is not the only one
20:17:48  &lt;Meeh&gt; no sorry, I got i2p.nu, and i2p2.no
20:18:11  &lt;Meeh&gt; add "facebook" as a point on the meeting for me, got some nice news
20:18:41  &lt;zzz&gt; ok FB will be 5)
20:19:01  &lt;eche|on2&gt; the bad word...
20:19:12  &lt;eche|on2&gt; I just need to cough... *sorry*
20:20:03  &lt;zzz&gt; looks like you are already in the mirror list as download.i2p2.no, is that working?
20:20:07  &lt;zzz&gt; if you want to add i2p.nu also, fine, more the merrier, as long as you are around at update time, or somebody else has the password
20:20:41  &lt;zzz&gt; you can work with str4d on the urls?
20:21:19  &lt;Meeh&gt; yepp
20:21:34  &lt;zzz&gt; any other comments?
20:22:02  &lt;Meeh&gt; I need to check where download.i2p2.no points, might need to change it to another host, need to check I/O. and I can provide more urls if needed. other than that; no :)
20:22:38  &lt;zzz&gt; ok you have a couple weeks before the next release but better sooner than later to get everything right
20:22:48  &lt;str4d&gt; No comments from me
20:22:50  &lt;Meeh&gt; I got the domains, I say we can use it as you guys wish, meaning, just give me instructions on how you want it :P
20:23:14  &lt;kytv&gt; +1 for everything so far (and I'll be happy to continue to handle the uploading of the download files)
20:23:18  &lt;DarkestMatter&gt; I'm tinkering with Makefile.gcj, and I've ran into a snag brought on by my relative naivety of java & gcj. I'm getting a java.lang.NullPointerException brought on by missing jar.so's like ant-1.8.2.jar.so, which exist in a dir outside of $JAVA_HOME, and I'm guessing that that's the problem
20:23:26  &lt;zzz&gt; you and str4d can work the details if needed
20:23:42  &lt;zzz&gt; DarkestMatter, we are in the middle of a meeting if you would please wait about half an hour
20:23:45  &lt;DarkestMatter&gt; Where would I need to symlink the ACTUAL dir into under JAVA_HOME for the build process to find them?
20:24:06  &lt;zzz&gt; next on the agenda:
20:24:06  &lt;zzz&gt; 4) OpenITP audit manager http://zzz.i2p/topics/1533 post #4
20:24:29  &lt;zzz&gt; background: OpenITP is about to open up their submission process
20:24:38  &lt;zzz&gt; we need somebody in charge
20:24:56  &lt;zzz&gt; They said we should apply even if we aren't ready
20:24:59  &lt;zzz&gt; which we arent
20:25:28  &lt;zzz&gt; I've posted a 3-phase process in the post above
20:25:45  &lt;zzz&gt; where we submit, then get ready, then really submit and manage the audit
20:26:05  &lt;zzz&gt; at CCC we agreed fixing up the threat model is the most important
20:26:31  &lt;zzz&gt; Comments? Does anybody want to be in charge?
20:28:10  &lt;str4d&gt; The general plan looks sound.
20:29:48  &lt;zzz&gt; Suspecting that we would not have any volunteers, I discussed it with Brandon WIley, asking if we could pay him to do it. (He is currently consulting for zooko, whose company does audits). Thoughts?
20:30:05  &lt;topiltzin&gt; how much?
20:31:03  &lt;str4d&gt; I am happy to contribute to the audit, but will likely not have the time to manage it myself.
20:32:26  &lt;zzz&gt; I assume several thousand dollars at least
20:32:26  &lt;zzz&gt; much higher if we actually get audited although that probably wouldn't be until 2015
20:32:29  &lt;topiltzin&gt; it's probably better for an external party to do it even if it costs a few k
20:32:29  &lt;str4d&gt; If we pay him, we want to ensure that it is useful.
20:32:53  &lt;user&gt; that would incluse exactly what?
20:32:54  &lt;topiltzin&gt; if he's doing this for a living he is (most probably) going to do a better job than anyone of us
20:33:49  &lt;user&gt; ++1 external, and ++1 if it helps getting a better standing, review-wise
20:34:06  &lt;zzz&gt; I would want him to actually help us fix stuff, not just be a traditional "consultant" or preauditor who just points out problems
20:34:27  &lt;zzz&gt; Brandon is a busy guy but also a guy currently looking for money
20:34:56  &lt;user&gt; and would he help you fix?
20:34:58  &lt;zzz&gt; If you havent' seen it: http://www.kickstarter.com/projects/brandonwiley/operator-a-news-reader-that-circumvents-internet-c
20:35:52  &lt;zzz&gt; I asked him to look at our openitp audit page on trac
20:36:07  &lt;zzz&gt; http://trac.i2p2.i2p/wiki/OpenITPReview/Criteria
20:36:19  &lt;zzz&gt; and await openitp's announcement and submission process details
20:36:26  &lt;str4d&gt; I2P has never (to my knowledge) had a proper security expert. I think paying for one to get the groundwork for this right is a good idea (and probably long overdue).
20:36:27  &lt;user&gt; my opnion as an outsieder / user only, is that a few thousand $ should be ok, as long as it's &lt;10k and not just some makeup, but really thorough
20:36:42  &lt;zzz&gt; until that's published it's not worth getting into negotiations with him
20:36:53  &lt;zzz&gt; but Eleanor said any day...
20:37:51  &lt;zzz&gt; eche|on, what's our balance? ~$500K?
20:38:00  &lt;wowa&gt; If you want that I change  topic of http://zzz.i2p/topics/1546?
20:38:31  &lt;zzz&gt; wowa, we are in the middle of a meeting, please wait until we are done, thx
20:38:36  &lt;eche|on2&gt; zzz: roughly 500 BTC and 50k 
20:39:37  &lt;zzz&gt; sounds like people are positive about the idea. Sadly even if we hire him to be in charge, we need to find somebody to be in charge of him...
20:39:40  &lt;EinMByte&gt; Moin
20:42:42  &lt;zzz&gt; I don't think there's anything more to do until the OpenITP announcement, then we can ask if Brandon is interested, if so we will have to talk about again
20:42:49  &lt;zzz&gt; any other comments on 4)
20:42:49  &lt;EinMByte&gt; Did I miss the meeting?
20:42:49  &lt;str4d&gt; EinMByte: in progress
20:42:49  &lt;user&gt; Ein: Just the beginning
20:42:49  &lt;eche|on2&gt; ok, 493 BTC and 48k euro
20:42:49  &lt;EinMByte&gt; oh, okay
20:42:49  &lt;zzz&gt; last call on 4)
20:42:49  &lt;str4d&gt; No comments at this time.
20:42:49  &lt;str4d&gt; Other than, planning should start on the wiki
20:42:49  &lt;zzz&gt; str4d, let's discuss in NYC too
20:42:49  &lt;str4d&gt; zzz: yes.
20:42:49  &lt;zzz&gt; 5) facebook Meeh go
20:42:49  * str4d will move the 3-step plan to /wiki/OpenITPReview/Plan
20:42:49  &lt;Meeh&gt; ok
20:42:49  &lt;Meeh&gt; As I said to zzz on CCC, I now got control over the https://www.facebook.com/I2P page
20:42:49  &lt;EinMByte&gt; Good thing for publicity, I suppose
20:42:49  &lt;topiltzin&gt; way cool :)
20:42:49  &lt;EinMByte&gt; I personally avoid the thing, but obviously most people have facebook
20:42:49  &lt;Meeh&gt; and I used ~10$ and 15min of my time in between my dayjob, and likes rised from 150 to 300
20:42:49  &lt;eche|on2&gt; so far good, but I keep outof facebook
20:42:50  &lt;Meeh&gt; this was in less than 10 hours
20:42:56  &lt;EinMByte&gt; so it's definitely a good thing to get more users
20:43:02  &lt;Meeh&gt; you don't need a account to see the page
20:43:22  &lt;Meeh&gt; however, I think we need to be public there too, to get "big", more users
20:43:22  &lt;EinMByte&gt; Meeh: I know, was more referring to liking and the like
20:43:37  &lt;Meeh&gt; but, nobody here like facebook, nor got an account :P
20:44:04  &lt;Meeh&gt; so, I might have something from work, that I can reuse so we can have an i2p url for some selected which can login and post to facebook, via I2P
20:44:09  &lt;TerraNullius&gt; Hello, about 3) would it also be possible to host releases on github?
20:44:12  &lt;zzz&gt; Meeh, is that it or are you asking for discussion or...?
20:44:55  &lt;Meeh&gt; mostly info, but I think it could be a idea to have an discussion about reaching our users via "social media"
20:44:57  &lt;zzz&gt; TerraNullius, we are done with 3) for now, sorry, you can wait until after the meeting to discuss further
20:45:37  &lt;zzz&gt; Meeh, please discuss with orion, he's our head of publicity, I assume he has some ideas
20:45:43  &lt;EinMByte&gt; Meeh: obviously those new users will need to understand that using "social media" isn't without risks
20:45:54  &lt;zzz&gt; we can also brainstorm with him in NYC and get back to you
20:46:07  &lt;Meeh&gt; we need more contributors, content providers, users, +++, and as we can see the "corporate" world collects a lot of users from SM
20:46:32  &lt;Meeh&gt; EinMByte: ofc. but someone needs to tell them ;)
20:46:39  &lt;Meeh&gt; that's where we comes in
20:46:41  &lt;EinMByte&gt; very true
20:46:47  &lt;topiltzin&gt; and underground I2P parties :)
20:46:47  &lt;Giant&gt; Who would moderate i2p&lt;-&gt;fb? That will be spam central.
20:46:49  &lt;zzz&gt; you're paying people to like you?
20:46:56  &lt;topiltzin&gt; (until 6 am)
20:47:03  &lt;Meeh&gt; yes a little now just to see how much I could boost it
20:47:05  &lt;eche|on2&gt; zzz: yes, some folks do that
20:47:16  &lt;Meeh&gt; 22 friends and the rest from ads
20:47:23  &lt;zzz&gt; now all we need are firetrucks
20:48:11  &lt;Meeh&gt; Giant: read me again. "for some selected which can login" :)
20:48:16  &lt;Meeh&gt; selected is the keyworld
20:48:18  &lt;Meeh&gt; word*
20:48:24  &lt;zzz&gt; good job Meeh , let's all feed him some content. There's a couple pix from ccc too that you can post
20:48:25  &lt;zzz&gt; I have one from tuna but you'll have to crop off the people in the background
20:48:37  &lt;zzz&gt; anything else on 5) ?
20:48:51  &lt;Meeh&gt; Awsome, if someone can give me a link for it I will upload a gallery, including some from me
20:49:08  &lt;Meeh&gt; ye, I'll fix that
20:49:11  &lt;zzz&gt; ok just be sure to crop
20:49:26  &lt;zzz&gt; anything else for the meeting?
20:49:35  &lt;EinMByte&gt; yes
20:49:39  &lt;user&gt; why crop? are you on them in the background? ;)
20:49:46  &lt;EinMByte&gt; I'd like to propose a short discussion about GNS integration
20:50:16  &lt;EinMByte&gt; Are we still looking into that?
20:50:16  * str4d was about to mention that
20:50:27  &lt;Meeh&gt; user: it wasn't allowed to take pictures if not all agreed on it, and we can't find all ppl to ask if it's ok to publish
20:50:35  &lt;str4d&gt; GNS or others
20:50:35  &lt;zzz&gt; ok it could go all day so let's try 10 minutes
20:50:37  &lt;zzz&gt; 6) GNS EinMByte go
20:51:07  &lt;user&gt; Meeh: ah, ok. that makes sense
20:51:09  &lt;str4d&gt; EinMByte: looking into it, yes.
20:51:22  &lt;EinMByte&gt; Alright, so what approach are we going to take
20:51:25  &lt;EinMByte&gt; reimplement?
20:51:28  &lt;str4d&gt; No guarantees that it will happen, or be a direct integration (or even that it will be GNS).
20:51:40  &lt;EinMByte&gt; is there still some possibility of not having to rewrite?
20:51:46  &lt;str4d&gt; But what we have now is an ad-hoc "just works" mess.
20:52:16  &lt;EinMByte&gt; What about support from their side?
20:52:31  &lt;Meeh&gt; topiltzin: want to be a facebook star again? :) (wrt I2P, pictures, CCC)
20:52:34  &lt;EinMByte&gt; They seemed pretty "closed"...
20:53:02  &lt;topiltzin&gt; sure thing Meeh go for it :)
20:53:34  &lt;zzz&gt; spent hours and hours with Christian at CCC
20:54:19  &lt;EinMByte&gt; zzz: no results whatsoever from that?
20:54:30  &lt;str4d&gt; EinMByte: *if* we decide to use GNS as-is (and ignore the fact that by default its DHT is not anonymous), then we could hook it in for testing with ExecNamingService
20:54:33  &lt;str4d&gt; There's a defined API. We just write a script that can query that API, and run it from ExecNamingService.
20:54:33  &lt;str4d&gt; Simple. But not at all optimal.
20:54:42  &lt;zzz&gt; could be anything from 'they solve all our problems' to 'lets use some of it' to 'those are some good ideas' to wow, no thanks
20:55:08  &lt;zzz&gt; no results really. Other than we promised to look into it
20:55:37  &lt;zzz&gt; I think we need to understand what they are doing. Beyond that, nothing is decided
20:56:15  &lt;zzz&gt; atm I'm a skeptic on all things gnunet. Doesn't mean I couldn't be convinced.
20:56:31  &lt;str4d&gt; zzz forwarded me an interesting exchange about I2P naming, it mentioned several other techs besides GNS
20:57:39  &lt;EinMByte&gt; well, I suppose that (as you say zzz), there may be some problems with the ideas behind GNS
20:58:02  &lt;EinMByte&gt; That is: will our users be able to adapt
20:58:09  &lt;str4d&gt; DLV (DNSSEC Lookaside Validation), DNSCurve...
20:58:14  &lt;str4d&gt; There are more technologies out there than GNS
20:58:14  &lt;str4d&gt; I can see that many ideas in GNS have been developed from scratch, assuming nothing.
20:58:37  &lt;topiltzin&gt; boiling the oceans
20:58:44  &lt;zzz&gt; sure. It's been a long time since we discussed our naming system in the big context of the internet, the triangle, alternatives, etc, so that's a good thing
20:58:48  &lt;EinMByte&gt; Yes. Since we need an alternative to hosts.txt for sure, we might as well look into those alternatives
20:59:00  &lt;str4d&gt; Even things like how the local cache is stored encrypted, as a direct copy of the blocks obtained from the DHT
20:59:02  &lt;zzz&gt; but he is indeed trying to boil
20:59:37  &lt;str4d&gt; I ran a quick test, I can confirm that NamingServices can be distributed as plugins.
20:59:39  &lt;zzz&gt; we talked about a layer that hides the GNS ugliness that we would have to design and implement. However that may also hide some of the benefits.
20:59:59  &lt;str4d&gt; It only requires that the default NamingService is a MetaNamingService.
21:01:06  &lt;str4d&gt; Are there any downsides to making the install-default NamingService a MetaNamingService, and the default added NamingService to it BlockfileNamingService?
21:01:08  &lt;zzz&gt; let's wrap up 6), we aren't going to fix things here
21:01:08  &lt;zzz&gt; anything else on 6) ? anything else for the meeting?
21:01:15  &lt;str4d&gt; (Current default NS is BlockfileNamingService, and current default added NS to Meta is HostsTxt...)
21:01:26  &lt;EinMByte&gt; one more thing on 6:
21:01:30  &lt;str4d&gt; zzz: above proposal is I think part of 6
21:01:32  &lt;EinMByte&gt; str4d, you mention alternatives?
21:01:50  &lt;EinMByte&gt; if GNS doesn't work, we can always check out other things
21:01:54  &lt;EinMByte&gt; they might fit us better
21:02:25  &lt;str4d&gt; EinMByte: yes. I have no knowledge of these alternatives, but all ideas are worth consideration.
21:04:12  &lt;str4d&gt; zzz: I propose that we change to MNS in 0.9.10, there is no visible change to users, but then if people want to test a NS plugin they don't need to edit router.config
21:04:18  &lt;zzz&gt; ok, everybody keep working on these ideas big and little, thats how we make things better
21:04:35  &lt;EinMByte&gt; str4d: okay. I will try to find some time to look into them
21:04:48  &lt;EinMByte&gt; I suppose this closes 6?
21:04:54  &lt;zzz&gt; str4d, we can do it when we need to but no rush? needs more testing too. Maybe post a howto?
21:05:17  &lt;zzz&gt; ok you all can keep yakking but I gotta run
21:05:19  &lt;topiltzin&gt; I'll offer the contrarian view: our current naming system works just fine
21:05:27  &lt;EinMByte&gt; same here
21:05:30  &lt;topiltzin&gt; and has some benefits we want to keep
21:05:38  * str4d afk
21:06:06  * zzz *bafs* the meeting closed
</div>
