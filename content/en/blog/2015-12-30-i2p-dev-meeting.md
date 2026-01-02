---
title: "I2P Dev Meeting - December 30, 2015"
date: 2015-12-30
author: "zzz"
description: "I2P development meeting log for December 30, 2015."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cacapo, comraden1, dg, eche\|on, hottuna, kytv, lazygravy, psi, str4d, zzz</p>

## Meeting Log

<div class="irc-log">
09:49:14  &lt;zzz&gt; 0) Hi
09:49:14  &lt;zzz&gt; 1) Meeting structure and goals
09:49:14  &lt;zzz&gt; 2) PR
09:49:14  &lt;zzz&gt; 3) Project Management
09:49:14  &lt;zzz&gt; 0) Hi
09:49:16  &lt;zzz&gt; Hi
09:49:30  &lt;zzz&gt; 1) Meeting structure and goals
09:49:30  &lt;zzz&gt; First of all I apologize for the horrendous time for this meeting for our North American folks.
09:49:30  &lt;zzz&gt; This will be a little different from our usual meeting structure because it's mostly in-person here at CCC.
09:49:31  &lt;zzz&gt; We will attempt to relay the highlights to IRC.
09:49:33  &lt;zzz&gt; We will also be taking notes here.
09:49:35  &lt;zzz&gt; Now let me give a preamble for this meeting.
09:49:49  &lt;zzz&gt; As you all should know, Sadie was a huge part of the organization and success of I2PCon in Toronto.
09:49:49  &lt;zzz&gt; We all saw her talent and enthusiasm in Toronto, and obviously she wants to do more for I2P going forward.
09:49:49  &lt;zzz&gt; As we got to work with her before and during the Con, we learned that she has extensive Project Management and PR experience,
09:49:49  &lt;zzz&gt; both with Tor and out in the real world.
09:49:49  &lt;zzz&gt; What I asked her to do after the Con was to get to know our project better, to understand our current structure and processes,
09:49:52  &lt;zzz&gt; and to come back with recommendations on what we could do better and how she could help us.
09:50:04  &lt;zzz&gt; Since then, she's had several long conference calls with tuna, me, str4d, psi, and others,
09:50:04  &lt;zzz&gt; and reviewed our website, trac, and current processes.
09:50:04  &lt;zzz&gt; Also, psi has named her Assistant PR Director and she is tweeting on the @GetI2P account and helping to get the word out about I2P.
09:50:06  &lt;zzz&gt; She is now ready to give us some recommendations.
09:50:06  &lt;zzz&gt; While my original question to her was "how can you help us?", the answer coming back is
09:50:06  &lt;zzz&gt; more like "here's the things we need to fix so I can effectively help",
09:50:08  &lt;zzz&gt; followed by the actual things she could do for us, or more precisely how we can all work together more effectively.
09:50:19  &lt;zzz&gt; What I'd like to do today is to hear her recommendations and discuss them each briefly.
09:50:19  &lt;zzz&gt; Many of these topics tend to spark long discussion and I'd like to contain that so we aren't here all day.
09:50:19  &lt;zzz&gt; For each recommendation, I'd like to get a commitment from one of you to follow up.
09:50:19  &lt;zzz&gt; If the recommendation is uncontroversial and we have consensus, that commitment would be to implement it.
09:50:20  &lt;zzz&gt; If it needs further research or we don't agree, that commitment would be to review our options and
09:50:21  &lt;zzz&gt; come up with a plan, or a counter proposal, or a list of options to be discussed at a future meeting.
09:50:23  &lt;zzz&gt; These commitments and due dates will be noted and tracked.
09:50:25  &lt;zzz&gt; I don't want to get bogged down on any one thing so I'll be looking for volunteers to follow up most things.
09:50:42  &lt;zzz&gt; I want to emphasize that I asked Sadie to do this and give us her opinion based on her previous experience.
09:50:42  &lt;zzz&gt; We may not agree but we should listen and carefully consider her recommendations.
09:50:42  &lt;zzz&gt; I2P is its own little snowflake and not everything may be appropriate for us,
09:50:42  &lt;zzz&gt; but she's gotten to know us pretty well this year, so let's hear what she's got.
09:50:43  &lt;zzz&gt; We will of course be able to take suggestions from others but I have a feeling that Sadie's got a lot of things covered already.
09:51:24  &lt;zzz&gt; We're going to first talk about PR and then Project Management.
09:51:24  &lt;zzz&gt; Both are very large topics and there will be overlap. But let's try to keep them as separated as we can.
09:51:54  &lt;zzz&gt; *** end of paste for topic 1), we will start in with 2) in a few minutes. thanks ***
09:58:39  &lt;hottuna&gt; str4d: heya we should have a talk about the DH stuff we're using
09:59:30  &lt;str4d&gt; hottuna, you referring to the NTCP and SSU handshakes?
09:59:55  &lt;hottuna&gt; i guess wherever DH is used
10:00:39  &lt;hottuna&gt; ok. lets talk about it after the meeting
10:00:47  &lt;str4d&gt; Sure
10:00:57  &lt;str4d&gt; According to http://trac.i2p2.i2p/wiki/Crypto/CurrentSpecs it's just NTCP and SSU
10:01:21  &lt;hottuna&gt; zzz will be reading the long note above to us now
10:01:48  &lt;str4d&gt; (I still need to update that page ahead of my talk)
10:04:10  &lt;psi&gt; i think i'm here
10:06:33  &lt;lazygravy&gt; psi: yes, zzz posted a long message just before you joined. talking IRL right now
10:07:57  &lt;hottuna&gt; So what we're looking to do is to get commitments from people to fix a bunch of different topics
10:08:25  &lt;hottuna&gt; Some of the stuff we're going to cover will be controversial and some not
10:08:47  &lt;hottuna&gt; the non-controversial topics we're hoping to just assign a to a person and have that handled
10:08:56  &lt;hottuna&gt; Onto Sadie and PR
10:09:16  &lt;hottuna&gt; gravy and sadie have been writing blogpost
10:09:29  &lt;hottuna&gt; and are looking for more content
10:10:21  &lt;hottuna&gt; a lot of content is lost in the commit messages
10:10:38  &lt;hottuna&gt; where the author of the commit does not really record the importance of the commit
10:11:24  &lt;str4d&gt; Rather than scanning commit messages, the best/easiest place to look is history.txt
10:11:30  &lt;hottuna&gt; ideally we would like to publish a blog post at least every 2 months to keep some sense of momentum is kept
10:12:08  &lt;str4d&gt; That still doesn't give an indication of importance, but is contextually easier to handle and sifts out the commit chaff that doesn't make it into history.txt
10:13:04  &lt;lazygravy&gt; str4d: the point is that there is so many cool things happening, and no way to find out without following i2p closely. it should be easier for people to see the cool stuff
10:13:47  &lt;str4d&gt; Perhaps what might help (this would be rather radical) could be to restructure history.txt to organize items by importance (major/minor/bugfix), more like a changelog (or have a parallel changelog file)
10:14:13  &lt;str4d&gt; since as-is, the history file is really just an easier-to-parse commit log
10:14:30  &lt;str4d&gt; That said, it *is* convenient, so maybe parallel info would be better (if harder to maintain)
10:14:38  * str4d stops getting bogged down in specifics
10:14:41  &lt;str4d&gt; :P
10:14:59  &lt;hottuna&gt; lazygravy could act as an editor and sort of delegate the responsibility of writing content when that is appropriate
10:15:14  &lt;str4d&gt; Certainly making it easier to know what is going on is a plus, and I think some of the higher-level organization topics will help this
10:15:33  &lt;str4d&gt; (ie. a blog post writer can look there for the high-level overview instead of the commit log)
10:15:56  &lt;psi&gt; sounds rather similar to pair programming
10:16:10  &lt;hottuna&gt; next topic within PR
10:16:29  &lt;hottuna&gt; regarding having a reseed campaign and attracting new developers
10:16:46  &lt;psi&gt; (or more like married couple programming, the programmer and the programmer's wife)
10:17:11  &lt;lazygravy&gt; str4d: i.e. WTF encrypted lease sets are, or a cool highlight of kytv's debian repo
10:17:15  &lt;hottuna&gt; we would like to involve torontocrypto to attract more reseed host s
10:17:23  &lt;lazygravy&gt; s/i.e./e.g./
10:17:24  &lt;iRelay&gt; lazygravy meant: str4d: e.g. WTF encrypted lease sets are, or a cool highlight of kytv's debian repo
10:18:25  &lt;hottuna&gt; We would like to generate a content package containing all info you would need to set up a reseed host should be available in one place
10:19:14  &lt;hottuna&gt; we need to articulate why reseeds are needed and important
10:19:18  &lt;str4d&gt; Mmm
10:19:42  &lt;str4d&gt; It could even be made as simple as "sudo apt-get i2p-reseed"
10:20:22  &lt;lazygravy&gt; str4d++
10:20:23  &lt;kytv&gt; I was thinking of making docker images so it can be completely plug-n-play:ed
10:20:47  &lt;psi&gt; the go reseed was excessively easy to set up and use
10:20:56  &lt;hottuna&gt; hottuna/I volunteered to write a few paragraphs about why reseeds are needed and what they do
10:21:07  &lt;hottuna&gt; kytv: that would be amazing
10:21:23  &lt;str4d&gt; kytv++
10:21:35  &lt;str4d&gt; Drop-and-go is the ideal
10:22:00  &lt;str4d&gt; Kinda like what was mentioned in one of the Tor talks yesterday, about how people could in future get a LetsEncrypt cert that comes with a free .onion
10:22:16  &lt;str4d&gt; (ie. the letsencrypt script sets up the Tor HS for the user)
10:22:38  &lt;kytv&gt; mdrollete's i2p-tools is available as a docker image, so maybe we (=I) could just polish up my I2P docker image (not yet advertised) so one could do it all by copy'n'pasting one command line and reseeding would "just work"
10:22:41  &lt;hottuna&gt; about developed onboarding, making the source code more accessible
10:22:42  &lt;str4d&gt; (that in itself would be super neat for I2P, but slightly different from what we need here)
10:22:55  &lt;comraden1&gt; kytv: docker for sure
10:23:01  &lt;hottuna&gt; str4d: could I convince you to add some links to the source code from geti2p.net?
10:23:04  &lt;str4d&gt; If reseeds are an appliance, it also makes it much easier to keep honest reseeds in sync
10:23:17  &lt;str4d&gt; hottuna, where?
10:23:18  &lt;lazygravy&gt; thought: we should get rid of the note from 0.7.6 on the download page
10:23:33  &lt;kytv&gt; (I'm more of an lxc guy but I'm learning docker so whatevs )
10:23:45  &lt;kytv&gt; ja
10:23:50  &lt;lazygravy&gt; kytv: docker seems "so hot" right now, so it might be best
10:23:54  &lt;hottuna&gt; wherever it makes sense
10:24:08  &lt;str4d&gt; I believe there is at least one link to kytv's ViewMTN, but that's inside I2P
10:24:11  &lt;hottuna&gt; but the idea is to make it easier to get a quick look at the soruce code
10:24:13  &lt;kytv&gt; Move all docs for ancient stuff to /attic or smth related
10:24:19  &lt;hottuna&gt; to attract developers
10:24:33  &lt;hottuna&gt; str4d outside i2p and ideally from geti2p.net is what we would want
10:24:36  &lt;str4d&gt; I could add links to the new devs page to the Github page, but they would need to be clearly marked as read-only
10:24:50  &lt;psi&gt; if you really want to attract devs we should make the github alive more
10:24:52  &lt;hottuna&gt; yeah.
10:25:57  &lt;str4d&gt; Is the new dev page where you want the links?
10:25:57  &lt;hottuna&gt; that sounds like a simple straight forward step to take
10:25:57  &lt;hottuna&gt; just add a read-only link to github
10:25:57  &lt;str4d&gt; hottuna, which? Links, or github alive more?
10:25:57  &lt;hottuna&gt; would be an improvement
10:25:57  &lt;str4d&gt; ahk
10:26:05  &lt;hottuna&gt; str4d: can I write your name next to that?
10:26:24  &lt;hottuna&gt; that item that is
10:26:38  &lt;str4d&gt; Sure. I assume all of these will get issues created on Trac
10:26:51  &lt;hottuna&gt; not sure if they will.
10:26:57  &lt;hottuna&gt; will ask zzz
10:27:09  &lt;str4d&gt; Well yeah, probably not worth it for the smaller tasks
10:27:20  &lt;str4d&gt; As long as I get the list sometime :P
10:27:26  &lt;hottuna&gt; ok
10:27:36  &lt;hottuna&gt; i think zzz will do a zzz.i2p writeup
10:28:22  &lt;kytv&gt; it'll almost certainly go to zzz.i2p but perhaps also as tickets on Trac
10:28:41  &lt;str4d&gt; k
10:28:50  * str4d pulls up todo list to start adding items
10:32:43  &lt;hottuna&gt; we're talking about which usecasdes we should promote i2p for
10:33:13  &lt;hottuna&gt; and the consesus seems to be  that we should promote usecases which we are good at. like bote
10:33:20  &lt;str4d&gt; Mmm
10:33:29  &lt;str4d&gt; We definitely need to push the peer-to-peer aspect
10:33:36  &lt;hottuna&gt; like torrents to potintiall
10:33:38  &lt;hottuna&gt; y
10:33:57  &lt;hottuna&gt; we would like to highlight these good uses on the main page
10:34:12  &lt;hottuna&gt; *what we would like to highlight
10:34:20  &lt;str4d&gt; That's something I2P should have a fundamental advantage with, due to the packet-switched nature and tunnel-level symmetry
10:34:33  &lt;hottuna&gt; yes. and there are other things we are good at
10:34:39  &lt;str4d&gt; And particularly apps that themselves inherently encourage contribution
10:34:41  &lt;hottuna&gt; and those things we should promote
10:35:05  &lt;hottuna&gt; and in the meantime we can keep on working on the things that we are not quite as good at
10:35:09  &lt;str4d&gt; (because I2P's need for contribution can then piggyback on the app's)
10:35:43  &lt;hottuna&gt; lazygravy, str4d, cacapo: could you work through the 3 best usecases for i2p
10:36:01  &lt;hottuna&gt; so that we then can present them properly on the frontpage
10:36:18  &lt;str4d&gt; Sure
10:37:03  &lt;cacapo&gt; yepp
10:37:08  &lt;hottuna&gt; when can you guys come back with something (recommendations or webstie changes)?
10:37:43  &lt;hottuna&gt; is a deadline for end of january ok?
10:37:55  &lt;cacapo&gt; ok
10:38:01  &lt;hottuna&gt; realting to PR: i2p.net becomes available soon
10:38:03  &lt;str4d&gt; Fine with me
10:39:04  &lt;eche|on&gt; 16.4.2016 it is for i2p,net
10:39:11  &lt;str4d&gt; I can say right now that if we are meaning "things that work well right now", you're really looking only at high-latency email (bote) and torrents. Soon we can add distributed datastorage too (once Tahoe gets native I2P client support)
10:39:24  * str4d is looking forward to i2p.net being recovered
10:39:33  &lt;eche|on&gt; tahoe will only be useable with parallel up/download
10:40:08  &lt;str4d&gt; I think it would be ideal to dovetail it with my proposal for dev services on i2p.i2p, have them parallel available in- and out-of-net
10:40:12  &lt;hottuna&gt; cacapo mentions i2p does not communicate a narrative about the project very well. or at all.
10:40:29  &lt;lazygravy&gt; str4d: tahoe has it's own UI problems... :/ (tho I adore it)
10:40:29  &lt;hottuna&gt; unlike to which has a lot of history and contextual history to it
10:41:03  &lt;str4d&gt; hottuna, what narrative does he mean?
10:41:09  &lt;hottuna&gt; relating to jake/snowden&/etc
10:41:42  &lt;str4d&gt; ah, narrative relating I2P history to world context?
10:41:43  &lt;hottuna&gt; comraden1: volunteers to do a writeup of the history of i2p
10:41:52  &lt;str4d&gt; (like the Tor HS talk did?)
10:42:05  &lt;eche|on&gt; history: zzz talk on i2pcon, my talk on 32c3
10:42:06  &lt;hottuna&gt; (didnt see that)
10:42:33  &lt;str4d&gt; also my talk at I2PCon had a bit
10:42:37  &lt;hottuna&gt; zzz, comraden1, lazygravy volunteered to do the actual writeup
10:42:41  &lt;hottuna&gt; psi: around?
10:42:53  &lt;psi&gt; yes
10:42:57  &lt;hottuna&gt; str4d: and so did Lance James' bit
10:43:34  &lt;str4d&gt; lazygravy, Tahoe UX should improve greatly once magic folders is released. UI-wise, still has work to do, but not as much as us :P
10:43:52  &lt;hottuna&gt; str4d, sadie, could the both of you help eachother out to do promo for the RWC talk?
10:44:03  &lt;hottuna&gt; ast call for PR related topics
10:44:06  &lt;hottuna&gt; Lest*
10:44:08  &lt;hottuna&gt; last*
10:44:49  &lt;hottuna&gt; alright, i'll take that as silence
10:44:50  &lt;str4d&gt; hottuna, yep, I'll keep in touch with Sadie
10:44:56  * str4d still has to prepare that talk :/
10:45:04  &lt;hottuna&gt; Onto the next topic. PROJECT MANAGEMENT
10:45:34  &lt;comraden1&gt; str4d: also "history of how i2p started". I'm thinking of navy researching onion routing -&gt; second generation onion router -&gt; tor
10:46:40  &lt;str4d&gt; comraden1, mmm, you'll probably find a lot of that in the early I2P meeting logs on the website
10:47:15  &lt;str4d&gt; If you do go rooting around in there, feel free to write quick summaries of the meetings that I can add to them :P
10:48:11  &lt;comraden1&gt; str4d: zzz mentioned that he has a lot of it in his head and wanted to write a rough draft. I'm going to edit and make sure it is perfect before we release it
10:48:45  &lt;str4d&gt; +1
10:49:19  &lt;dg&gt; I remember speaking about it with zzz ages ago; if he has logs of that, it might be helpful
10:49:22  &lt;hottuna&gt; we're talking about what the actual goals of the project are
10:49:54  &lt;hottuna&gt; and that they are important to have written down somewhere in order to be able to do meaningful project management
10:50:29  &lt;str4d&gt; Would make for a good about page
10:51:16  &lt;str4d&gt; I've wanted to merge the various intro pages, but we could actually leverage them separately
10:51:36  &lt;str4d&gt; Turn https://geti2p.net/en/about/intro into a brief overview of I2P, both the network and the project
10:51:38  &lt;iRelay&gt; Title: Intro - I2P (at geti2p.net)
10:51:59  &lt;str4d&gt; Then make https://geti2p.net/docs/how/intro the *actual* "how does I2P work" page
10:52:00  &lt;iRelay&gt; Title: A Gentle Introduction to How I2P Works - I2P (at geti2p.net)
10:52:10  &lt;str4d&gt; Kinda sorta what they appear to be now, but properly split
10:53:12  &lt;dg&gt; hottuna: Where can I find the blogposts?
10:53:22  &lt;dg&gt; hottuna: I can only see one (http://i2p-projekt.i2p/en/blog/2015/11/15/Community-Outreach)
10:53:25  &lt;iRelay&gt; Title: Community Outreach - Blog - I2P (at i2p-projekt.i2p)
10:54:38  &lt;lazygravy&gt; dg: they don't exist aside from that
10:54:55  &lt;lazygravy&gt; and that was mostly a POC IMO. Next one should be published on 10Jan2016 on CCC
10:58:32  &lt;hottuna&gt; we're talking about whether we want to be managed
10:58:46  &lt;hottuna&gt; dg, str4d, psi: do you have any thoughts about having your work managed?
10:59:11  &lt;psi&gt; by who and how much management?
10:59:17  &lt;hottuna&gt; by sadie
10:59:26  &lt;dg&gt; open to it
10:59:42  &lt;hottuna&gt; and having it be relaxed as in deadlines. but not enforced deadlines
10:59:46  &lt;hottuna&gt; things are done when they are done
11:00:11  &lt;hottuna&gt; but mentally attaching a deadline to them might be a helpful tool
11:00:11  &lt;dg&gt; done when they're done but a bit of pushing/motivation
11:00:40  &lt;psi&gt; no thoughts until i eat breakfast
11:00:47  &lt;hottuna&gt; or at the very least knowing that someone else knows that a given task  is on your pile
11:01:15  &lt;hottuna&gt; re project management: we'd like to get weekly/bi-weekly meetings up and runnning again
11:01:25  &lt;hottuna&gt; zzz has the goal of starting them up in february agin
11:01:27  &lt;hottuna&gt; again*
11:01:36  &lt;hottuna&gt; and then gradually handing them off to sadie
11:01:48  &lt;hottuna&gt; for that to happen sadie needs got on irc
11:01:56  &lt;str4d&gt; I'm good for it. I do tend to work better when I have someone(s) to bounce ideas off
11:03:23  &lt;hottuna&gt; zzz just committed to having a single roadmap written up by the end of february
11:03:23  &lt;hottuna&gt; splendid.
11:03:23  &lt;hottuna&gt; the consensus seems to be that being managed lightly is probably a good thing.
11:03:23  &lt;hottuna&gt; but anything heavy-handed would just turn this into work
11:03:23  &lt;str4d&gt; Sounds good. We can always adjust the level later once we have some experience with it.
11:03:23  * dg nods
11:03:23  &lt;hottuna&gt; *roadmap will be for end of jan, not feb
11:03:23  &lt;hottuna&gt; str4d: agreed
11:04:35  &lt;str4d&gt; FYI zzz, sadie and I will be meeting up at the beginning of March, would be good to keep that in mind re: things we can work on/discuss then.
11:05:52  &lt;hottuna&gt; re: trac tickets, sadie is volunteering to keep an eye on it and relay tickets to the right individual
11:06:05  &lt;dg&gt; Being able to observe our mechanics like trac/zzz.i2p/irc is important for Sadie to fully understand how we work anyway
11:06:16  &lt;dg&gt; Has she been able to do that w/o IRC access?
11:07:04  &lt;hottuna&gt; str4d: would you bi willing to help sadie out in that endeavour?
11:07:40  &lt;str4d&gt; I've had on my todo list for a while a weekly "look over new tickets" item, that I keep postponing because too much on
11:08:06  &lt;str4d&gt; But from next year, I'll endeavour to help sadie with that :)
11:08:49  &lt;str4d&gt; You may have noticed there's an "open" status now for tickets. I added that so we can differentiate between new tickets and ones we've seen but haven't had an opinion on necessarily
11:08:53  &lt;hottuna&gt; Last call for PROJECT MANAGEMENT topics
11:09:10  &lt;dg&gt; hottuna: see above
11:09:25  &lt;str4d&gt; My goal would be to have as few "new" tickets as possible, ie. moving them either to a relevant person/status, or "open" to at least acknowledge them as a valid ticket.
11:09:36  &lt;hottuna&gt; Last call for OTHER topics
11:09:48  &lt;hottuna&gt; dg: getting sadie on trac is key. and a requirement
11:10:00  &lt;hottuna&gt; I mean on IRC
11:10:17  &lt;dg&gt; okay
11:10:23  &lt;str4d&gt; I've had an IRC bouncer account for her for a while now
11:10:42  &lt;hottuna&gt; str4d: could we ask you to write up few items about what you learned about vulnerability response the the conf?
11:10:48  &lt;str4d&gt; All she needs is help getting her side connected, and she can then keep logs etc. without needing to stay connected all the time
11:11:40  &lt;str4d&gt; hottuna, you mean from talking to k8em0 at Kiwicon?
11:11:47  &lt;hottuna&gt; mhm
11:11:47  &lt;dg&gt; Also help with browser config/privoxy?
11:12:13  &lt;str4d&gt; I didn't learn a lot more than I already kinda knew, other than hearing in advance about the bug bounty program that Tor just announced
11:12:26  &lt;zzz&gt; we're proposing that we defer the VRP discussion to january
11:12:36  &lt;hottuna&gt; str4d: would making a tiny writeup make sense?
11:12:40  &lt;str4d&gt; k8em0 did say she was very impressed with our VRP ticket
11:12:45  &lt;hottuna&gt; like a zzz.i2p post?
11:12:55  &lt;hottuna&gt; or was it all kind of useless?
11:13:15  &lt;str4d&gt; Not useless, more confirming that our VRP ticket is on the right track
11:13:31  * zzz ******BAFFFFS***** the meeting closed, thanks everybody
</div>
