---
title: "I2P Dev Meeting - May 03, 2016"
date: 2016-05-03
author: "zzz"
description: "I2P development meeting log for May 03, 2016."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> eche|on, pr0ng, xmpre, xmz, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:46 &lt;zzz&gt; 0) Hi
20:00:46 &lt;zzz&gt; 1) Tails status (pr0ng) http://zzz.i2p/topics/2108
20:00:46 &lt;zzz&gt; 2) 0.9.26 planning update (zzz)
20:00:46 &lt;zzz&gt; 3) HOPE planning update (zzz) http://zzz.i2p/topics/1968
20:00:50 &lt;zzz&gt; 0) Hi
20:00:52 &lt;zzz&gt; hi
20:01:01 &lt;pr0ng&gt; Hey Eeepers
20:01:22 &lt;zzz&gt; 1) Tails status (pr0ng) http://zzz.i2p/topics/2108
20:01:32 &lt;zzz&gt; ok, a lot's happened on tails in the last month
20:01:33 &lt;pr0ng&gt; Hi zzz
20:01:47 &lt;Irc2PGuest33835&gt; hey
20:02:01 &lt;zzz&gt; 0.9.25 got into tails 2.3, and 0.9.26 may or may not line up with 2.4. pr0ng would you please give us a brief report?
20:02:51 &lt;pr0ng&gt; Not sure about the 'not line up' part - is that the I2p persistence support?
20:03:05 &lt;zzz&gt; i mean schedule-wise
20:03:36 &lt;pr0ng&gt; Basically, this release was taken from the deb.i2p.no repo and uploaded to Tail APT repo by 'anonym'
20:04:00 &lt;pr0ng&gt; I tested the release in isolation on the Tails image, fairly extensively
20:04:20 &lt;pr0ng&gt; I've been communicating with anonym to get a handle on what goes where and when
20:04:28 &lt;zzz&gt; and I told them you had tested it... perhaps that's why anonym did the rest?
20:04:48 &lt;pr0ng&gt; Very nice and accommodating individual, gave me lot's of advice and help
20:05:02 &lt;pr0ng&gt; I now have a handle on exactly how the release is tested and deployed
20:05:27 &lt;zzz&gt; is what happened for .25/2.3 the actual process, or are they expecting you to do more next time?
20:05:42 &lt;pr0ng&gt; Indeed. They took the .deb from I2P straight through
20:06:40 &lt;pr0ng&gt; There's a couple of scripts that dictate how I2P is deployed - they / anonym used those and I now know where they are and how to build/transfer for inclusion
20:07:29 &lt;zzz&gt; ok so you will be doing more next time
20:07:55 &lt;pr0ng&gt; They can take from the deb.i2p2.no or other methods - they are highlighting the persistence angle at the moment - I may need to do other to get that working next release, but I will find out for certain.
20:08:20 &lt;eche|on&gt; great so far
20:08:30 &lt;pr0ng&gt; c'est possible - looks like I'll be able to 'deliver' the release myself this time
20:08:33 &lt;zzz&gt; so you've now started to get into their oustanding issues, the first of which is persistence?
20:08:48 &lt;pr0ng&gt; indeed - I'm pleased it went through and I learnt the requirements
20:10:09 &lt;pr0ng&gt; indeed - I will be looking at the outstanding issues - the persistence element is more of a 'nice to have' it seems, but it was highlighted in our conversation.
20:10:24 &lt;zzz&gt; what would your deadline be for me to have 0.9.26 in deb.i2p2.no in order for you to get it into tails 2.4?
20:11:48 &lt;pr0ng&gt; I will need to determine that - that's something I can't be precise on atm
20:12:01 &lt;pr0ng&gt; I will certainly come back with an answer for that
20:12:13 &lt;zzz&gt; ok, let me know, even if just a guess.
20:12:22 &lt;zzz&gt; anything else on 1) ?
20:12:40 &lt;pr0ng&gt; I will, certainly.
20:12:52 &lt;pr0ng&gt; So far so good methinx.
20:13:04 &lt;zzz&gt; thanks again, you're doing great work, glad to have you on it
20:13:34 &lt;zzz&gt; 2) 0.9.26 planning update (zzz) 
20:13:36 &lt;pr0ng&gt; I'm glad to help - it's been a steep curve, but I'm much more comfortable with the process and the requirements. :)
20:14:11 &lt;zzz&gt; I've finished the major parts of .26 -- addressbook subscription protocol, and CRLs in the news feed. And we've propped GMP 6
20:14:48 &lt;xmz&gt; zzz: has anyone reported a working family config from using the java i2p console?
20:14:48 &lt;xmz&gt; zzz: I've never got it to work
20:14:50 &lt;zzz&gt; I'm turning to bug fixing now and that will be my focus until the release. I'm hot on the trail of a strange timer bug that I think is the root cause of some issues people are seeing
20:15:32 &lt;zzz&gt; xmz, other than me, I haven't heard any reports of failure or success
20:15:34 &lt;pr0ng&gt; apologies for my ignorance - is 'propped GMP 6' 'dropped libgmp'?
20:15:42 &lt;zzz&gt; if you're having issues, please open a ticket
20:15:57 &lt;xmz&gt; okay sure I will test in a bit and report
20:16:05 &lt;zzz&gt; propped = propagate = merge from another (development) branch
20:16:25 &lt;zzz&gt; at this point I haven't set a .26 date but late May or early june looks likely
20:16:40 &lt;pr0ng&gt; Ah. K. thanks for that :)
20:17:14 &lt;zzz&gt; thanks to eche|on for doing some dev builds. We'd really like to see somebody step up and do a real, automatic, dev build site
20:17:18 &lt;eche|on&gt; I vote for 2nd june week
20:17:50 &lt;zzz&gt; As some of you may have seen, I declared that we're slowing down our releases, from 6-8 weeks to 8-10. 
20:17:52 &lt;eche|on&gt; I want to, but my time is limited currently
20:18:32 &lt;eche|on&gt; yes, it is ok
20:18:32 &lt;zzz&gt; This is a byproduct of less testing, me doing a lot of stuff that kytv was doing, and a general reduction in activity all around
20:19:18 &lt;zzz&gt; there's also almost no participation in reviewing proposals and getting ready for the hard stuff coming up this year, esp. NTCP2 and related
20:20:10 &lt;zzz&gt; there's also the proposed 'summer of x' that I was hoping for an update from sadie on. If we do move forward with that, it's going to slow releases down a lot
20:20:47 &lt;zzz&gt; I can tell you there's nobody working ahead on .27 planning or coding at all right now
20:20:52 &lt;zzz&gt; anything else on 2) ?
20:21:52 &lt;zzz&gt; 3) HOPE planning update (zzz) http://zzz.i2p/topics/1968
20:22:32 &lt;zzz&gt; I have continued to fail at getting a commitment for meeting space from Lance for HOPE
20:22:51 &lt;zzz&gt; so I still can't give anybody guidance if you're making plans to attend
20:23:15 &lt;zzz&gt; sadie was going to meet with him last week, she hasn't responded to my query as to whether she got an answer from him
20:23:25 &lt;eche|on&gt; hmm
20:24:05 &lt;zzz&gt; If anybody has a hard date on when you need to know, speak up. I feel bad about nagging Lance but it isn't working at all
20:24:26 &lt;xmpre&gt; zzz: I have a jenkins server set up for i2pd, I could set one up for java i2p if there is interest?
20:24:44 &lt;zzz&gt; yeah xmpre, for sure
20:25:20 &lt;zzz&gt; anything else on 3) ?
20:27:05 &lt;eche|on&gt; zzz: I still got that ticket^^
20:27:15 &lt;zzz&gt; I saw in the scrollback above that str4d and sadie had issues with the standard meeting time, and something about shifting timezone base that I didn't understand. If you two want to negotiate with the europeans and come up with something that would work for everybody, please do
20:27:20 &lt;zzz&gt; anything else for the meeting?
20:27:55 &lt;pr0ng&gt; I'm planning to turn up at I2PCon-2 - are there any ideas on when/where for that?
20:28:28 &lt;pr0ng&gt; ... reading, did I miss that already!?
20:28:33 &lt;zzz&gt; I don't think there will be a i2pcon 2.
20:28:50 &lt;zzz&gt; perhaps a small meetup in Toronto in the fall, as a tiny facsimile
20:28:55 &lt;pr0ng&gt; Shame
20:29:11 &lt;zzz&gt; if you want to catch some i2p ppl in person, best shot is HOPE and CCC
20:29:18 * zzz warms up the baffer
20:29:31 &lt;pr0ng&gt; I'll pencil that in then.
20:29:54 * zzz *bafs* the meeting closed
</div>
