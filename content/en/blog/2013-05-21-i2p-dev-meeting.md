---
title: "I2P Dev Meeting - May 21, 2013"
date: 2013-05-21
author: "hottuna"
description: "I2P development meeting log for May 21, 2013."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, eche|on, hottuna, Mathiasdm, Meeh, zzz</p>

## Meeting Log

<div class="irc-log">
19:56:52  &lt;hottuna&gt; Hi@all && (welt||welterde||weltende)
19:57:24  &lt;eche|on&gt; ;-)
20:00:33  &lt;iRelay&gt; &lt;jenkins@kytv&gt; Starting build #182 for job I2P
20:01:11  &lt;hottuna&gt; Mathiasdm, Meeh, postman, str4d, _sponge, KillYourTV, Complication
20:01:19  &lt;hottuna&gt; Alright, lets get this meeting started
20:01:33  &lt;eche|on&gt; meeting? hmm
20:01:33  &lt;hottuna&gt; Agenda:
20:01:39  &lt;hottuna&gt; * New bounty system
20:01:44  &lt;hottuna&gt; * New bounties
20:01:49  &lt;hottuna&gt; * Misc?
20:02:21  &lt;hottuna&gt; __New bounty system___
20:03:25  &lt;hottuna&gt; During this summer I'll have some time over for I2P development, but I also have to pay my rent which is why a new bounty system or at least a new set of bounties and sub-bounties will be suggested
20:03:51  &lt;dg&gt; \o
20:04:37  &lt;iRelay&gt; &lt;jenkins@kytv&gt; Project I2P build #182:SUCCESS in 4 min 7 sec: http://jenkins.killyourtv.i2p/job/I2P/182/
20:05:00  &lt;hottuna&gt; after discussing the idea with eche|on, it seems like the best option for payed work is via the bounty system
20:05:44  &lt;hottuna&gt; to make it work I'll suggest at least one large bounty and then create sub-bounties for it
20:06:27  &lt;hottuna&gt; the sub bounties will be created and closed on a bi-weekly schedule
20:06:41  &lt;hottuna&gt; (preferably by holding a meeting like this when a sub bounty is to be closed)
20:07:27  &lt;eche|on&gt; you know my opinion, and so I just wait for input ;-)
20:07:35  &lt;hottuna&gt; Currently the i2p project has a lot of funds which aren't doing us any good
20:08:10  &lt;hottuna&gt; and allowing me to contribute to some much needed problem areas in i2p should be a good thing overall
20:08:51  &lt;hottuna&gt; Does anyone have any questions or feedback at this idea?
20:09:26  &lt;hottuna&gt; I've talked to zzz, eche|on, postman and Mathiasdm earlier and they have approved
20:10:07  &lt;hottuna&gt; I've tried to reach welt/welterde/weltende, _sponge, badger and KillYourTV but have not gotten any response from them
20:10:23  &lt;iRelay&gt; &lt;jenkins@kytv&gt; Project I2P UnitTests build #153:SUCCESS in 5 min 36 sec: http://jenkins.killyourtv.i2p/job/UnitTests/153/
20:10:35  &lt;hottuna&gt; But I'd like to know what the rest of the inhabitants of #i2p-dev think about the idea
20:10:52  &lt;dg&gt; I agree that we should be doing something with the funds
20:11:08  &lt;dg&gt; An organized method of doing so is useful, I don't disagree at all so I'm remaining mute
20:12:04  &lt;hottuna&gt; dg, does this seem like a good way of doing something useful?
20:13:00  &lt;dg&gt; yes. The bounty system already works, we should build upon it
20:13:19  &lt;zzz&gt; you're proposing using existing funds? euros or BTC?
20:13:21  &lt;hottuna&gt; As far as bounty amounts go,  325 per bi-weekly sub-bounty is what I need to cover my basic costs of living
20:13:47  &lt;hottuna&gt; euros are safer and simpler for me
20:14:07  &lt;hottuna&gt; but maybe parts could be payed in btc
20:14:42  &lt;hottuna&gt; in any case the bounty should be set in euros and then possibly payed out in btc
20:14:47  &lt;zzz&gt; eche|on, whats our balances?
20:15:27  &lt;hottuna&gt; and to answer your question, Im proposing using existing funds
20:15:27  &lt;eche|on&gt; http://echelon.i2p/donations/index.html - still on those sums
20:15:32  &lt;iRelay&gt; Title: Donations (at echelon.i2p)
20:15:40  &lt;eche|on&gt; so ~28k and 626 BTC
20:16:47  &lt;dg&gt; hottuna: What work will you be performing?
20:17:22  &lt;zzz&gt; appx. how many hours a week are you proposing to work?
20:17:35  &lt;hottuna&gt; that is point two on the agenda, but i'm primarily thinking about improving on our floodfill issues
20:17:57  &lt;hottuna&gt; 40 h/week. So full time.
20:18:56  &lt;zzz&gt; so round numbers, 8 euros/hour
20:19:18  &lt;zzz&gt; nope. 4 euros/hour
20:19:20  &lt;hottuna&gt; in my mind that sounds reasonable/cheap
20:19:35  &lt;zzz&gt; 325/80
20:20:13  &lt;zzz&gt; mcdonalds isn't hiring? :)
20:20:35  &lt;hottuna&gt; i think burger king has payed me more an hour :P
20:21:06  &lt;eche|on&gt; you worked for a burger king? hell,... I should have visited your working office^^
20:21:35  &lt;zzz&gt; appx. how many weeks you propose to work?
20:21:56  &lt;hottuna&gt; lets see.. this will be a rough number
20:23:19  &lt;hottuna&gt; I should manage at least 8, but it could be more or less than that
20:24:10  &lt;zzz&gt; so a 1300 euro commitment from us
20:24:24  &lt;hottuna&gt; yeah
20:24:49  &lt;hottuna&gt; more than that would have to be discussed in a meeting
20:25:18  &lt;zzz&gt; anybody remember what we paid jrandom monthly?
20:26:08  &lt;hottuna&gt; let's see what the internet archive says
20:26:10  &lt;eche|on&gt; less. ~500$ IMHO
20:26:39  &lt;zzz&gt; he was more of a hippie than tuna is :)
20:26:50  &lt;hottuna&gt; $465 USD/month
20:27:11  &lt;hottuna&gt; I'm hippying as hard as I can damnit!
20:27:52  &lt;dg&gt; hippy harder!!
20:28:49  &lt;hottuna&gt; alright, so does anyone have any objections or questions?
20:29:15  &lt;zzz&gt; no objection
20:29:41  &lt;Mathiasdm&gt; sounds good
20:30:25  &lt;dg&gt; ditto
20:30:54  &lt;hottuna&gt; Alright. Then we are all happy about this
20:31:32  &lt;hottuna&gt; For the record: As no complaints have been raised, we'll proceed with the new bounty system.
20:31:47  &lt;hottuna&gt; __New bounties__
20:32:34  &lt;hottuna&gt; The floodfill system has some issues, including attack resistance and scalability.
20:33:02  &lt;hottuna&gt; Replacing it is the first bounty that I will suggest.
20:33:30  &lt;hottuna&gt; I've talked to zzz about some alternatives
20:33:47  &lt;hottuna&gt; and step one appears to be to move to a kademlia based netdb
20:34:30  &lt;hottuna&gt; zzz has in fact already started by implementing kademlia in i2psnark
20:34:59  &lt;hottuna&gt; this is probably a good base for for a netdb network
20:35:53  &lt;hottuna&gt; there are some modifications that can be made to kad to make it more probabilistic and avoid the worst aspects of eclipse and sybil attacks.
20:36:01  &lt;zzz&gt; I'm not sure "replace" is the right word. And also not sure it's the top of my list. Our ff system is actually in pretty good shape right now. But I'm not sure how much you want to get into discussing it now.
20:36:27  &lt;zzz&gt; A reasonable sub-bounty may be just to analyze the current situation and make proposals
20:36:41  &lt;hottuna&gt; replace would be a long term goal, initially adding a second netdb backend would be the goal
20:36:58  &lt;hottuna&gt; yeah, replace is the wrong word.
20:37:09  &lt;zzz&gt; but sure, the UCSD folks highlighted some issues.
20:37:35  &lt;zzz&gt; ignoring vulnerabilities for a moment, I think we're actually good for a couple years of growth w/o changes
20:38:06  &lt;Mathiasdm&gt; 22:37 &lt;zzz&gt; A reasonable sub-bounty may be just to analyze the current  situation and make proposals &lt;-- sounds like a good idea if it's time-boxed
20:38:53  &lt;hottuna&gt; spending two weeks on an analysis might be overkill, but having a meeting and discussing the alternatives after a week might be good
20:38:55  &lt;zzz&gt; what's _not_ realistic is replacing ffs with R5N this summer.
20:39:09  &lt;hottuna&gt; zzz, agreed
20:41:24  &lt;hottuna&gt; there might also be a need for some work surrounding development like multirouter support
20:41:24  &lt;hottuna&gt; which would make development easier
20:41:24  &lt;zzz&gt; fyi for everybody, the netdb roadmap in my head is 1) encrypted lookup responses and 2) migrate the snark kad back to router
20:41:24  &lt;Meeh&gt; like the ideas
20:41:35  &lt;Meeh&gt; ./roadmap
20:41:49  &lt;dg&gt; yeah
20:44:21  &lt;hottuna&gt; I don't think that 2 full weeks are needed for this
20:44:27  &lt;Meeh&gt; yea
20:45:21  &lt;dg&gt; "alternative exploration"?
20:45:30  &lt;Meeh&gt; as in the exploration tunnels right or?
20:45:30  &lt;zzz&gt; depends how long before your head explodes
20:45:37  &lt;zzz&gt; what else on your list?
20:45:45  &lt;hottuna&gt; "alternative exploration" = {what technology?, if dht-which?, what code-base?}
20:46:03  &lt;hottuna&gt; maybe one week, and if I have time to spare I'll start with the multirouter stuff.
20:47:09  &lt;hottuna&gt; I'm not sure, but some of the bounties like ipv6 will have to be completed soon as ipv6 looks to be actually deployed now
20:47:40  &lt;dg&gt; zzz is working on ipv6 a load but he my appreciate help
20:48:12  &lt;eche|on&gt; I try to add IPv6 on my root server for I2P use.
20:48:15  &lt;hottuna&gt; Resolving issues regarging an openitp submission has been suggested by zzz
20:48:22  &lt;eche|on&gt; as soon as I find time to understand and get it up...
20:48:57  &lt;Meeh&gt; I have a dev server that I can let developers into for testing.. It have multiple ipv6 adresses
20:49:00  &lt;hottuna&gt; having us accepted into OpenITP would be a major thing for us
20:49:07  &lt;Meeh&gt; Could setup more of them now for testing
20:49:22  &lt;eche|on&gt; and now gone for a good night time...
20:49:25  &lt;zzz&gt; here's my list: IPv6 (incl. testing), Crypto (see trac wiki), OpenITP prep (see trac wiki), NTCP and SSU protocol obfuscation (old zzz.i2p post, Lance James might be able to help), other state firewall resistance, Symmetric NATs (ticket #873), ...
20:49:32  &lt;iRelay&gt; http://trac.i2p2.i2p/ticket/873 - (accepted defect) - Port changing .. obscurely
20:49:40  &lt;Meeh&gt; zzz: want access to a ipv6 server for testing?
20:49:51  &lt;dg&gt; hottuna: major thing, yes, but, in case you (or others) are not aware: OpenITP are not long term funders. They fund short, achievable goals to improve projects "quickly".
20:51:05  &lt;zzz&gt; Meeh yes, in a couple weeks. I'd like to see the minor fix in 0.9.5 to ignore published IPv6 addresses get out there before we start publishing them
20:51:24  &lt;zzz&gt; s/0.9.5/0.9.6/
20:51:24  &lt;hottuna&gt; crypto is another thing that I know a bit about, so my time might be well spent there
20:51:27  &lt;iRelay&gt; zzz meant: Meeh yes, in a couple weeks. I'd like to see the minor fix in 0.9.6 to ignore published IPv6 addresses get out there before we start publishing them
20:51:48  &lt;Meeh&gt; ok :) I can setup multiple too if needed
20:51:51  &lt;hottuna&gt; maybe if we're lucky I'll be somewhat done with the floodfill system by the time zzz is done with ipv6
20:51:58  &lt;Meeh&gt; got a /48 net
20:52:14  &lt;hottuna&gt; that way we could both attack the crypto problem
20:52:21  &lt;zzz&gt; heck what about i2pcpp
20:52:37  &lt;dg&gt; orion is 404 atm
20:52:48  &lt;Meeh&gt; sindu might help there when he got time, great C coder
20:52:59  &lt;Meeh&gt; talked about it earlier, know him from RL
20:53:26  &lt;hottuna&gt; that sounds interesting
20:53:49  &lt;zzz&gt; if orion is at least willing to accept help, that's a big step - he wasn't before -
20:53:52  &lt;hottuna&gt; but I think that I should spend time where makes the most difference which in my mind is floodfills/ipv6 and crypto
20:54:11  &lt;hottuna&gt; *it
20:54:14  &lt;zzz&gt; sure, my list doesn't necessarily match your skills or interest
20:54:29  &lt;Meeh&gt; also, he should get some creds for spreading the i2p stickers around Oslo, Norway. He have placed it all around the city
20:54:44  &lt;Meeh&gt; hottuna: if you want, send more.. soon emtpy again:P
20:55:11  &lt;zzz&gt; oh yeah, hottuna if you aren't coming to DEFCON I need some too
20:55:30  &lt;hottuna&gt; im planning on coming to defcon
20:55:44  &lt;hottuna&gt; i havent bought any plane tickets yet, but I will soon.
20:55:47  &lt;zzz&gt; oh hella yes.
20:56:23  &lt;Meeh&gt; hottuna: if you got files, I might be able to get some free printups myself
20:56:43  &lt;hottuna&gt; the files are in the i2p.graphics branch
20:56:46  &lt;Meeh&gt; if you got the sticker in png/ai/whatever format
20:56:49  &lt;Meeh&gt; ok thanks
20:57:00  &lt;hottuna&gt; if im remembering correctly
20:57:16  &lt;hottuna&gt; alright.
20:57:51  &lt;hottuna&gt; Is everyone ok with the first bounty being for the floodfill system?
20:58:02  &lt;dg&gt; aye
20:58:25  &lt;Meeh&gt; yepp
20:58:50  &lt;Mathiasdm&gt; ok, so first 1 week of research into the options, followed by implementation (currently most likely kademlia)? sounds good
20:59:06  &lt;hottuna&gt; yes, that's the idea
21:01:56  &lt;hottuna&gt; ok
21:03:15  &lt;hottuna&gt; For the record: The first bounty to be introduced is adding a new netdb backend.  The first sub bounty should be divided into alternative exploration, multirouter research and discussion with you guys
21:03:26  &lt;hottuna&gt; __Misc__
21:04:38  &lt;hottuna&gt; How is the website deployment going?
21:09:27  &lt;hottuna&gt; Everyone died?
21:09:31  &lt;hottuna&gt; str4d?
21:12:57  &lt;Mathiasdm&gt; oh
21:13:04  &lt;Mathiasdm&gt; I was curious :)
21:14:22  &lt;hottuna&gt; did I miss anything exciting?
21:14:29  &lt;Mathiasdm&gt; only this:
21:14:32  &lt;Mathiasdm&gt; 23:10 -!- hottuna [hottuna@irc2p] has quit [Quit: leaving]
21:14:32  &lt;Mathiasdm&gt; 23:12 &lt;+Mathiasdm&gt; oh
21:14:35  &lt;Mathiasdm&gt; 23:13 &lt;+Mathiasdm&gt; I was curious :)
21:15:12  &lt;hottuna&gt; Alright, if no one knows, let's see next week
21:15:38  * hottuna baf's with the meeting ending hammer
21:19:59  * Mathiasdm lurks onward :)
</div>
