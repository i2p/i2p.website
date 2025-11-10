---
title: "I2P Dev Meeting - May 05, 2015"
date: 2015-05-05
author: "zzz"
description: "I2P development meeting log for May 05, 2015."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> cacapo, dg, eche|on, hottuna, psi, str4d, xmz, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:23  &lt;zzz&gt; 0) Hi
20:00:23  &lt;zzz&gt; 1) Toronto meeting (Aug. 15-16) planning
20:00:27  &lt;zzz&gt; 0) Hi
20:00:29  &lt;zzz&gt; hi
20:00:35  &lt;eche|on&gt; hi
20:00:51  &lt;psi&gt; just about the time for the meeting?
20:00:53  &lt;zzz&gt; 1) Toronto meeting (Aug. 15-16) planning
20:01:03  &lt;dg&gt; hi
20:01:14  &lt;zzz&gt; 1a) review where we're at
20:01:19  &lt;zzz&gt; 1b) volunteers
20:01:32  &lt;zzz&gt; 1c) do we move forward
20:01:37  &lt;zzz&gt; 1a) review where we're at
20:02:00  &lt;zzz&gt; hottuna, please give us an update on the planning, venue, and projected costs
20:02:20  &lt;hottuna&gt; Hi@all
20:02:24  &lt;psi&gt; hi
20:02:50  &lt;str4d&gt; hi
20:02:53  &lt;hottuna&gt; So, we've reserved two 8-hour slots at hacklab in Toronto for the 15-16 Aug.
20:03:20  &lt;hottuna&gt; The slots are 150CAD each
20:03:46  &lt;hottuna&gt; This is the venue: https://hacklab.to/
20:03:48  &lt;iRelay&gt; Title: hacklab.to - Toronto's hacker collective (at hacklab.to)
20:04:07  &lt;hottuna&gt; The initial plan is to have two separate events.
20:04:37  &lt;xmz&gt; hi
20:04:44  &lt;hottuna&gt; 15Aug: I2P general presentation + I2P Cryptoparty
20:05:28  &lt;hottuna&gt; 16Aug: Have a technical presentation leading into discussions about various upcoming issues
20:06:10  &lt;hottuna&gt; Ideally I'd like to have a better itinerary for both of these days by the end of this meeting.
20:07:09  &lt;psi&gt; is lodging self serve or is that "taken care of"?
20:07:13  &lt;hottuna&gt; Additionally we've through J@torontocrypto secured a lounge-like space in a house in toronto for other/late-night planning/hacking/etc
20:07:55  &lt;hottuna&gt; psi, lodging can be offered for free at said lounge (which is a house on the opposite side of toronto)
20:08:14  &lt;xmz&gt; transport to and from lounge?
20:08:46  &lt;hottuna&gt; Public transit shouldn't be too bad. Something like a 25 minute subway ride.
20:08:46  &lt;xmz&gt; I guess we arrange our own. I'll have a car so I can ferry a few folks
20:08:54  &lt;eche|on&gt; 8h slots, times?
20:08:55  &lt;xmz&gt; oh that's not bad
20:09:11  &lt;eche|on&gt; cars in a city...
20:09:25  &lt;zzz&gt; ok thanks tuna, i'd like to open it up for questions and comments now, before we get into details on the agenda or volunteers
20:09:28  &lt;xmz&gt; you have a point there eche|on
20:09:42  &lt;xmz&gt; toronto traffic can be quite bad
20:10:01  &lt;eche|on&gt; 2 8h slots are fine, times of those? and I assume we come, sit down, get power and WiFi
20:10:03  &lt;zzz&gt; anybody have any general questions or comments?
20:10:14  &lt;eche|on&gt; and some technical stuff provided
20:10:18  &lt;dg&gt; will there be streams, and are we expecting on advertising this? if so, how?
20:10:54  &lt;hottuna&gt; eche|on, 8h slots: they're evening slots so I think we'd have to be out of hacklab sometime around 00:00
20:10:54  &lt;hottuna&gt; J has offered to organize the crypto party part of 15Aug.
20:11:23  &lt;eche|on&gt; midnight is fine, which makes it 4pm to 12pm
20:11:32  &lt;hottuna&gt; eche|on: power, wifi, chairs, tables, etc are available
20:11:32  &lt;xmz&gt; that's good
20:11:48  &lt;xmz&gt; if there's enough upstream available streaming is definitely an option
20:11:52  &lt;eche|on&gt; fine for me so far.
20:12:17  &lt;eche|on&gt; streaming is not such a big issue, we do have root server with traffic free to distribute, if we want
20:12:26  &lt;hottuna&gt; xmz, I'm not sure they have a crazy internet connection.
20:12:42  &lt;hottuna&gt; also streaming might not be acceptable for privacy reasons
20:12:56  &lt;hottuna&gt; and additionally would be quite a bit of work to organize
20:13:01  &lt;str4d&gt; Yah, that's a topic up for discussion
20:13:01  &lt;xmz&gt; yeah
20:13:14  &lt;dg&gt; how about advertisement?
20:13:19  &lt;eche|on&gt; yeah, I am not in favour of streama, just twitter and instagram^^
20:13:34  &lt;str4d&gt; But technically, it wouldn't be hard. We don't need 1080p upstream ^^
20:13:36  &lt;eche|on&gt; ads, we do ads on zzz and forum already, or what ads?
20:13:49  &lt;fox&gt; so first one to hack the public wifi AP wins?
20:13:57  &lt;hottuna&gt; dg, J has offered to do a bit of advertisment, and since he's done a few crypto parties in toronto, i think we'll have no issues drawing a crowd.
20:14:06  &lt;dg&gt; ads for general public, i'm not sure how big a following the hacklab have?
20:14:14  &lt;dg&gt; hottuna: thanks, that's what I was looking for
20:14:14  &lt;hottuna&gt; the i2p twitter/website be helpful too
20:14:30  &lt;dg&gt; I am pleasantly surprised by how many can attend
20:14:48  &lt;zzz&gt; "j" is eager to fire up the publicity, i've asked him (via tuna0 to hold off until we have this meeting, figure out who is doing PR on our side, and can do a coordinated announcment
20:14:52  &lt;hottuna&gt; fox, a guest network is available
20:14:54  &lt;eche|on&gt; I am in favour of a I2P even twith "some" guest
20:14:55  &lt;xmz&gt; yeah I'm glad it's being held in Toronto. if it were anywhere else it would be hard for me to attend.
20:15:09  &lt;dg&gt; it'd be great if he could come here too.
20:15:12  &lt;dg&gt; (j)
20:15:38  &lt;hottuna&gt; dg, J is distracted by meatspace today
20:15:56  &lt;hottuna&gt; the one thing J asked us for is an itinerary for Aug16
20:16:02  &lt;dg&gt; hottuna: I don't think it'd kill to setup a bouncer! He has been saying he'll come for a while
20:16:41  &lt;eche|on&gt; so, sa/su each 4pm to midnight
20:16:42  &lt;zzz&gt; anybody have any other general questions or comments, or any objections to doing this at all?
20:16:58  &lt;eche|on&gt; I vote for I2P lunch on sunday before hacklab
20:16:59  &lt;xmz&gt; no objections only encouragement here
20:17:06  &lt;xmz&gt; that's a good idea
20:17:15  &lt;psi&gt; it's effectively sa to monday morning right?
20:17:24  &lt;eche|on&gt; It would be nice to get some I2P folks together and meet, anything else, a surplus in my view
20:17:52  &lt;zzz&gt; let's avoid the temptation to discuss small details. For example, i suspect the hours may change, the agenda isn't yet set, we don't need to talk about bouncer setup
20:18:02  &lt;hottuna&gt; eche|on, yes - as far as I know. That window might be shifted an hour back or forth though.
20:18:16  &lt;eche|on&gt; yeah, it is ok
20:18:38  &lt;eche|on&gt; so the lodge  for lounge is for the night-swarmers to make through the night
20:18:41  &lt;psi&gt; hottuna: what is general talk vs technical talk?
20:19:03  &lt;hottuna&gt; psi, that is a good question. and something we will have to decide.
20:19:05  &lt;eche|on&gt; general talk: I2p, what it is, how it works, technical talk: what is the protocol
20:19:22  &lt;eche|on&gt; hottuna: but the lodge with sleeping plac is sa-mo, or?
20:19:30  &lt;hottuna&gt; for 15Aug, we'd like to target a more general crowd. So anything that non-i2p people would understand
20:19:31  &lt;xmz&gt; are there any guides/walkthroughs planned for people new to I2P?
20:19:33  &lt;dg&gt; s/kill/kill him/
20:19:34  &lt;str4d&gt; I won't be in attendance (as stated before), but I have no high-level objections
20:19:34  &lt;iRelay&gt; dg meant: hottuna: I don't think it'd kill him to setup a bouncer! He has been saying he'll come for a while
20:19:34  &lt;eche|on&gt; and the lounge does make noise to the sleeping guys?
20:20:06  &lt;hottuna&gt; xmz, a crypto party which basically is a group walktrhough/workshop is planned for 15Aug
20:20:14  &lt;xmz&gt; that's great
20:20:33  &lt;psi&gt; I want to do a short i2p app dev intro
20:21:16  &lt;psi&gt; we should really show off the ease of developing with i2p &lt;-- workshop idea
20:22:26  &lt;hottuna&gt; psi, and i2p app dev intro would be nice for 16Aug I suppose
20:22:30  &lt;str4d&gt; ++
20:22:43  &lt;str4d&gt; That would dovetail nicely with Android
20:22:45  &lt;hottuna&gt; eche|on, re lounge: I would like to confirm the details about it with J, Sat-Mon does sound appropriate
20:22:45  &lt;dg&gt; that would be nice psi
20:22:45  &lt;hottuna&gt; str4d, would you like to talk about android?
20:22:45  &lt;eche|on&gt; in this case I go into my own hotel room ;-)
20:22:45  &lt;psi&gt; i'd need to drag along a copy of monotone so we don't wait 5 hours for it to sync
20:22:45  &lt;zzz&gt; yeah i envision sat. as a public thing, and sun. as a dev meeting / hackathon, open to public but probably just us. Also we could do a 2nd public presentation on Sun. if the first is "sold out"
20:22:45  &lt;str4d&gt; hottuna: it's probably a good idea to do so, what with me being the de-facto Android project lead :P
20:22:46  &lt;eche|on&gt; sounds reasonable, zzz
20:23:15  &lt;hottuna&gt; str4d, I'll sign you up for 16Aug and talking about android then?
20:23:36  &lt;str4d&gt; Yah
20:24:12  &lt;hottuna&gt; psi, I signed you up for an i2p app dev intro. is that ok?
20:24:22  &lt;psi&gt; yes
20:24:29  &lt;zzz&gt; ok let me transition to 1b) volunteers
20:24:44  &lt;zzz&gt; we've never done this before. It's not going to happen unless somebody is in charge.
20:24:44  &lt;hottuna&gt; danke.
20:24:57  &lt;zzz&gt; No one person can do it all.
20:25:19  &lt;zzz&gt; We need somebody in overall charge of this, and several people to own various pieces.
20:25:20  &lt;eche|on&gt; people in charge, I vote for: hottuna local contact to book the venue and the lounge, I pay
20:25:49  &lt;zzz&gt; If anybody thinks this will be easy... think again
20:26:08  &lt;hottuna&gt; i'm up for continuing doing general coordination, which is what I've been doing this far.
20:26:13  &lt;zzz&gt; and if we don't find enough people to volunteer, let's cancel the whole thing now before we go speding money
20:26:32  &lt;zzz&gt; so here's my list from my post, which may be over the top too much, but we can start here:
20:26:47  &lt;zzz&gt; -  Overall Meeting Head Planner (??)
20:26:47  &lt;zzz&gt; - Finance (echelon)
20:26:47  &lt;zzz&gt; - PR / Marketing (psi)
20:26:47  &lt;zzz&gt; - Facilities / Logistics (hottuna)
20:26:47  &lt;zzz&gt; - Overall Schedule (??)
20:26:47  &lt;zzz&gt; - Crypto Party Planning (??)
20:26:49  &lt;zzz&gt; - Crypto Party Presentation (??)
20:26:51  &lt;zzz&gt; - Deep technical presentation (zzz)
20:26:53  &lt;zzz&gt; - i2pd presentation / planning session (orignal)
20:26:58  &lt;zzz&gt; - Android presentation / planning session (str4d via skype)
20:26:59  &lt;zzz&gt; - Roadmap / technical sessions lead (??)
20:27:01  &lt;zzz&gt; - Eating / drinking location picker (orignal)
20:27:03  &lt;zzz&gt; - Hotel / crash house picker (hottuna)
20:27:05  &lt;zzz&gt; - Snacks coordinator (echelon)
20:27:07  &lt;zzz&gt; - Stickers (echelon)
20:27:09  &lt;zzz&gt; - Video / audio recording (??)
20:27:53  &lt;eche|on&gt; I am in favour of not really planing much of the talks. we do have some volunteers in here to do some talks
20:28:18  &lt;zzz&gt; right. I don't want to do planning here at this meeting. I want to pick people in charge and let them do it
20:28:39  &lt;zzz&gt; and the overall person in charge can run all subsequent meetings
20:28:45  &lt;hottuna&gt; I'm volunteer for arranging the overall schedule too.
20:28:52  &lt;xmz&gt; cryptoparty planning will have to be co-ordinated with J right?
20:29:01  &lt;xmz&gt; or is he going to handle all of it
20:29:04  &lt;hottuna&gt; J has volunteered to organize the crypto party
20:29:17  &lt;zzz&gt; ok, so hottuna as the overall person in charge and the guy in charge of schedule?
20:29:52  &lt;str4d&gt; +1, he is best placed to keep track of it all
20:29:56  &lt;eche|on&gt; if he is up for it?
20:31:16  &lt;zzz&gt; ok hottuna?
20:31:16  &lt;hottuna&gt; im okay with that. it's probably easier that way
20:31:17  &lt;hottuna&gt; as for crypto party presentation, I'm not sure what it should contain
20:31:17  &lt;hottuna&gt; i am.
20:32:02  &lt;str4d&gt; hottuna: I assume this means you will definitely be in Toronto for the party? (It was in the air earlier)
20:32:02  &lt;zzz&gt; anybody ever been to a crypto party?
20:32:08  &lt;psi&gt; i have
20:32:22  &lt;psi&gt; as far as i can tell it's like a mini con
20:32:30  &lt;hottuna&gt; str4d, I'm planning to be in toronto. so unless some kind of disaster strikes I will be,
20:33:01  &lt;cacapo&gt; hi - echelon and i did a small cryptoparty at 29c3
20:33:16  &lt;zzz&gt; great. psi can we nominate you to work with J on both PR and the crypto party?
20:34:43  &lt;psi&gt; yup
20:34:43  &lt;psi&gt; (now that this is solid ima buy my travel stuff)
20:34:43  &lt;hottuna&gt; cacapo, eche|on: would you like to have part in the crypto party?
20:34:43  &lt;hottuna&gt; psi, do you have the contact details of J?
20:34:44  &lt;cacapo&gt; hottuna: sure I'm game
20:34:54  &lt;eche|on&gt; I was just a helper for I2P part, I will be in toronto, but mostly as a backup :-)
20:34:55  &lt;str4d&gt; hottuna: I assume this means you will definitely be in Toronto for the party? (It was in the air earlier) :P
20:34:56  &lt;str4d&gt; erk
20:34:58  &lt;str4d&gt; sry
20:35:10  &lt;psi&gt; hottuna: not at the moment
20:35:25  &lt;hottuna&gt; I'm not exactly sure about what has to be done. ideally you would coordinate that with J
20:35:28  &lt;psi&gt; hottuna: forward them to me when you have the chance
20:35:30  &lt;str4d&gt; psi: not solid until 1c)
20:35:38  &lt;zzz&gt; who would like to work on - or give - a presentation, on either day?
20:36:12  &lt;psi&gt; i'll help wingman a presentation if anyone needs it
20:36:13  &lt;zzz&gt; i can do one each day, but i think we should have several short ones, not one big one by one guy
20:36:28  &lt;eche|on&gt; right
20:37:37  &lt;zzz&gt; hottuna, looks like orignal had to leave, can you catch up with him later to see what he can volunteer for, maybe an i2pd presentation or technical session, or a trip to a bar/
20:38:13  &lt;hottuna&gt; zzz, so psi and str4d offered two technical ones for aug16
20:38:17  &lt;hottuna&gt; zzz, i'll try to catch up with orignal, yes.
20:38:23  &lt;zzz&gt; anybody else want to volunteer for anything at this time?
20:39:56  &lt;zzz&gt; ok it sounds to me like we have the important assignments made.
20:40:06  &lt;eche|on&gt; not much, Ill be around 1 or 2 days earlier and have a look around
20:40:23  &lt;zzz&gt; so 1c) does it sound like we have adequate staffing to proceed on this?
20:40:33  &lt;hottuna&gt; i'd say so.
20:40:48  &lt;eche|on&gt; are we more than 5 persons who will be around? ;-)
20:41:14  &lt;zzz&gt; I want to make sure we don't put too much on tuna's back. Let's all help out to make this a success
20:41:33  &lt;eche|on&gt; yeah, make a plan on zzz.i2p about the talks
20:41:35  &lt;zzz&gt; ok if tuna isn't panicked then I guess we're in good shape
20:41:52  &lt;hottuna&gt; I'm not panicked.
20:41:54  &lt;eche|on&gt; and hottuna should gimme the contact to pay
20:42:11  &lt;zzz&gt; I expect hottuna will run several more meetings over the coming weeks and months to get ready
20:42:15  &lt;hottuna&gt; eche|on, could that be done in cash in meatspace?
20:42:27  &lt;hottuna&gt; I think we'll need wiki-page to organize around.
20:42:40  &lt;eche|on&gt; cash is also OK, but all I can pay in advance is better, my credit/debit card is not really unlimited^^
20:42:53  &lt;psi&gt; i have a wiki that i can dedicate
20:42:57  &lt;psi&gt; potentially
20:43:00  &lt;zzz&gt; i want to add a 1d) financial support to the agenda
20:43:13  &lt;zzz&gt; 1d) financial support
20:43:32  &lt;hottuna&gt; may I suggest: https://trac.i2p2.de/wiki/MeetupToronto2015
20:43:33  &lt;eche|on&gt; we got money to give out.
20:43:49  &lt;zzz&gt; traditionally we've only reimbursed people $200 or so for conferences
20:44:19  &lt;zzz&gt; i hear some people may need significantly more in order to attend
20:44:28  &lt;eche|on&gt; str4d: your issue was mostly the money problem to attend?
20:44:44  &lt;str4d&gt; eche|on: no, timing
20:44:51  &lt;zzz&gt; what's the maximum we would be willing to give per-person? or alternatively, how much money would people need in order to attend?
20:44:51  &lt;eche|on&gt; ha, no, I do mix some names..
20:44:52  &lt;str4d&gt; (well, money too)
20:44:59  &lt;zzz&gt; $500? $1000? $2000?
20:45:11  &lt;eche|on&gt; IMHO flights from europe are 1200 both ways
20:45:19  &lt;eche|on&gt; and IMHO thats what kytv needs to attend
20:45:33  &lt;eche|on&gt; if he/she can stay somewhere $cheap and good
20:45:45  &lt;zzz&gt; if anybody has a hard number they need, speak up now
20:45:53  &lt;eche|on&gt; kytv: now is your time.
20:46:09  &lt;zzz&gt; or, how much do people think is reasonable?
20:46:27  &lt;eche|on&gt; I think, we can pay a lot of different stuff, but I would like to pay more on travel cost and less on having booze on the event
20:46:35  &lt;eche|on&gt; (is it pronounced booze?)
20:47:13  &lt;hottuna&gt; eche|on, having people over is more important yes.
20:47:16  &lt;psi&gt; hm
20:47:23  &lt;hottuna&gt; (it's booze, yes)
20:47:28  &lt;zzz&gt; or, another way to ask, how much should we spend total on this event?
20:48:01  &lt;eche|on&gt; currently on the list to pay for me: location, some snacks/coffee/coffebreak, a dinner/lunch for I2P.
20:48:20  &lt;psi&gt; all my costs would be just transit and i would need to figure that part out, probably air, maybe bus/train
20:48:43  &lt;zzz&gt; would $10K be out of line to spend?
20:48:50  &lt;eche|on&gt; I would pay kytv (and any other dedicated I2P contributor) 1200 for the flight, and each other up to 500, if they want it
20:49:20  &lt;hottuna&gt; eche|on, that sounds reasonable
20:49:25  &lt;str4d&gt; $10k would need to be heavily justified
20:49:33  &lt;eche|on&gt; and that would sum up to 10k roughly
20:50:04  &lt;str4d&gt; But with good justification, I wouldn't be against it
20:50:59  &lt;eche|on&gt; ok, 5k-10k in that area
20:51:24  &lt;hottuna&gt; should we re-imburse the complete travel costs do something like 50% or 75%?
20:51:27  &lt;zzz&gt; what about up to $1500 reimbursement for core team members, and up to $2500 for 'special cicrumstances', i.e. you really need it
20:51:36  &lt;eche|on&gt; I would pay up to 10k, the only issue: if we do this an regular base, it is a bit hard to pay 10k each year
20:51:38  &lt;hottuna&gt; eche|on, i think something closer to 5k then 10k would be easier to agree on
20:51:56  &lt;zzz&gt; eche|on, remind us, how much money do we have atm?
20:52:10  &lt;eche|on&gt; wait a sec
20:52:37  &lt;str4d&gt; On current HoF: 44.6k euro and 537.7 BTC
20:52:50  &lt;eche|on&gt; roughly 41k euro, 534 Bitcoin and 700 Litecoin on my side
20:53:19  &lt;eche|on&gt; 534 btc each 210, LTC is 1.2 each
20:53:52  &lt;fox&gt; person experience for cheap room and board motel 6 has gotten much nicer accross north america
20:53:59  &lt;xmz&gt; I can help out with setup/teardown etc.
20:54:50  &lt;hottuna&gt; what type of expenses would we like to reimburse a person for? total expense for the trip? only flights? flights+hotel?
20:55:02  &lt;fox&gt; inn type place are nice if you want breakfast though
20:55:22  &lt;zzz&gt; usually we just do it no-questions-asked, whatever you spent money on
20:56:13  &lt;str4d&gt; But given the scale of this expenditure, we probably do want to have some reasonable restrictions
20:56:33  &lt;eche|on&gt; I vote for travel expenses
20:56:34  &lt;zzz&gt; sure.
20:56:41  &lt;eche|on&gt; as the lounge is cheap and available
20:56:55  &lt;psi&gt; hottuna: so to clarify would i or would i not have to personally book a hotel
20:56:59  &lt;psi&gt; (For me)
20:57:04  &lt;xmz&gt; Could have some setup for accepting donations at the event
20:57:04  &lt;eche|on&gt; and food/drinks is same like @home, if you want to
20:57:25  &lt;hottuna&gt; psi: you would have to do the booking. book whatever you like. echelon will reimburse you
20:57:33  &lt;psi&gt; okay
20:57:45  &lt;zzz&gt; how about max of US$ 1K for north americans, 1500 euros max for europeans, 2000 euros max for 'special circumstances'
20:58:20  &lt;eche|on&gt; zzz: fligst US to CAD are &lt;1000$ ?
20:58:22  &lt;cacapo&gt; with 5K-10K and a lot of key persons in place why not call it a Summit - slightly more official
20:59:00  &lt;zzz&gt; shouldn't be more than $400
20:59:04  &lt;zzz&gt; but I haven't looked
20:59:12  &lt;zzz&gt; and it may be driving distance for some
20:59:44  &lt;zzz&gt; we've never reimbursed 100% for anybody
20:59:44  &lt;eche|on&gt; I want to note again and ask: if we do that amount, we need to clarify, the reimbursements for 32C3 and the next few events will be as usual ~200, if not some special stuff happens
21:00:03  &lt;hottuna&gt; eche|on, agreed
21:00:47  &lt;zzz&gt; I'm just throwing out proposals, somebody please agree/disagree too high/low
21:00:48  &lt;eche|on&gt; it is kinda unfair, but could be seen as a kind of advertising
21:01:00  &lt;eche|on&gt; zzz: I agree, with the added note
21:01:46  &lt;zzz&gt; look at it another way, i think we should spend at least 10% of our money a year. Maybe 15-20%.
21:02:04  &lt;eche|on&gt; hmm
21:02:19  &lt;zzz&gt; because 10 more years would be a long time at this
21:02:58  &lt;eche|on&gt; we got 7k donations in 2014 and spent 11k (in euro alone)
21:03:55  &lt;hottuna&gt; zzz, if wo do the percentile thing let's start low.
21:03:57  &lt;eche|on&gt; this year we got ~600 euro and spent 3k
21:04:21  &lt;eche|on&gt; 10% is nice for me currently
21:04:30  &lt;eche|on&gt; would need to convert some BT to  again...
21:04:31  &lt;zzz&gt; including btc we have ~150K euros
21:05:00  &lt;eche|on&gt; I call BTC somewhat "play-stuff" and unless they are in  in here, I do not really count them much.
21:05:30  &lt;eche|on&gt; sure, the exchange rate is 210 currently, but I will never be able to exchange 400 BTC at once.
21:05:38  &lt;hottuna&gt; I agree with eche|on. btc arent 100% reliable for doing that kind of math
21:06:10  &lt;eche|on&gt; so, with agreeing on max 10k for this event, Ill exchange some BTC
21:06:33  &lt;eche|on&gt; I just want to be on the safe side and have some kind of "reserve" in .
21:06:40  &lt;zzz&gt; you can offer people extra if they take rembursement in BTC
21:06:54  &lt;eche|on&gt; sure, I do this all the time. thats the benefit of BTC
21:07:08  &lt;eche|on&gt; you can pay folks with them, but you cannot rely on it.
21:07:50  &lt;hottuna&gt; eche|on, zzz, psi, dg: do we all agree on a 10k hard cap for expenses relating to this event?
21:07:53  &lt;eche|on&gt; but yeah, we do have the money
21:08:02  &lt;zzz&gt; ok how about this, we budget 10K euro for the total event. Actual per-person max depends on how many people go, "special cicrumstances" requests, etc.,  to be determined later
21:08:03  &lt;psi&gt; hard cap yes
21:08:20  &lt;hottuna&gt; zzz, sounds good.
21:08:44  &lt;eche|on&gt; Hmm, hard cap is interesting, but depends on the local costs for snacks^^
21:09:07  &lt;eche|on&gt; we can hard cap the expenses for people to attend.
21:09:15  &lt;eche|on&gt; and that would be 8 or 9k?
21:09:24  &lt;zzz&gt; but everybody be smart. You can't drive to Toronto and book a $400 a night hotel and expect to get it all covered
21:09:55  &lt;eche|on&gt; zzz: travel expenses, or travel&hotel?
21:10:23  &lt;zzz&gt; dunno
21:10:35  &lt;eche|on&gt; also: list of people to prefer (aka: people who already did a lot, people giving a talk, other)
21:10:38  &lt;hottuna&gt; eche|on, given that there is a lounge available for free Im not opposed to the idea of only travel expenses
21:10:47  &lt;zzz&gt; usually it's flight + hotel, but we've never come close to a full reimbursement before so it didn't matter
21:11:39  &lt;str4d&gt; I think 10k budget for now, do a roll call so we know who *will* be going, then we will be better placed to budget reimbursement
21:11:50  &lt;eche|on&gt; I sum my opiono: cap 8k for travel expenses of participants, with some level of importance to the people
21:12:00  &lt;zzz&gt; ok
21:12:32  &lt;str4d&gt; (roll call from core people)
21:12:34  &lt;zzz&gt; let's wrap it up for now, we'll ask people to email echelon with how much they would need later
21:12:37  &lt;hottuna&gt; eche|on, agreed.
21:12:51  &lt;hottuna&gt; alright
21:12:54  &lt;zzz&gt; ok everybody who is going and wants reimbursement from the project say 'aye'
21:12:56  &lt;zzz&gt; aye
21:13:02  &lt;eche|on&gt; aye ;-)
21:13:04  &lt;hottuna&gt; https://trac.i2p2.de/wiki/MeetupToronto2015 now contains some information.
21:13:12  &lt;psi&gt; aye
21:13:19  &lt;hottuna&gt; if you signed up for a responsibility, please help maintain this page
21:14:17  &lt;zzz&gt; ok eche|on, please check with kytv later and see how much he would need to attent
21:14:22  &lt;hottuna&gt; cacapo ??
21:14:24  &lt;zzz&gt; anything else on 1d?
21:14:47  &lt;cacapo&gt; hottuna: aye i'm going if I can wrestle down my boss
21:15:12  &lt;cacapo&gt; I'd happily take a small reimbursement in BTC
21:15:14  &lt;hottuna&gt; zzz, no
21:15:24  &lt;zzz&gt; it will take a few days to figure out who's going .
21:15:49  &lt;zzz&gt; for a couple people the reimbursement amount may enter into the decision, but for most probably not
21:15:59  &lt;zzz&gt; anything else on 1) ?
21:16:14  &lt;zzz&gt; any other (non-toronto) topics to discuss?
21:16:46  &lt;zzz&gt; first meeting in 6 months, gotta look for the baffer
21:17:15  &lt;zzz&gt; thanks to everybody and especially to the volunteers
21:17:26  &lt;zzz&gt; ahh there it is
21:17:40  &lt;eche|on&gt; great
21:17:49  &lt;eche|on&gt; time for bed now^^
21:17:52  * zzz *bafs* the meeting closed
</div>
