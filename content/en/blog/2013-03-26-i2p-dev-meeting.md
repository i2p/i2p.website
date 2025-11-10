---
title: "I2P Dev Meeting - March 26, 2013"
date: 2013-03-26
author: "dg"
description: "I2P development meeting log for March 26, 2013."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, LaughingBuddha, lillith, Meeh, nom, orion, str4d, Umlaut, weltende</p>

## Meeting Log

<div class="irc-log">
21:01:00  &lt;dg&gt; So, who is here?
21:01:11  &lt;orion&gt; Me.
21:01:18  &lt;str4d&gt; o/
21:01:37  &lt;lillith-&gt; i'm here :)
21:02:10  &lt;dg&gt; eche|on, Meeh, KillYourTV, psi, hottuna
21:02:21  &lt;Umlaut&gt; count me in too (as a spectator)
21:02:28  * nom is listening, while coding on some side projects
21:02:39  &lt;dg&gt; Feel free to contribute if you feel you have something to add.
21:03:04  * dg waits a minute or two more
21:03:27  &lt;lillith&gt; rundown of topics in the meantime dg?
21:03:42  &lt;dg&gt; Topics:
21:03:45  &lt;dg&gt; * Motivating the community - "are bounties appropriate?"
21:03:45  &lt;dg&gt; * Managing money
21:03:46  &lt;dg&gt; ** Making the project "official" - benefits/negatives/how
21:04:24  &lt;lillith&gt; i had something to add *thinks*
21:04:31  &lt;dg&gt; hm?
21:06:37  * lillith can't remember... probably nothing too important anyway :)
21:09:14  * dg frowns at the lack of others
21:09:44  * LaughingBuddha spectates
21:10:27  &lt;dg&gt; Let's start then
21:10:54  * lillith remembered!
21:10:59  &lt;dg&gt; hm?
21:11:14  &lt;dg&gt; RN: ping
21:11:25  &lt;lillith&gt; as kytv|away pointed out, if we're deciding on voting we need some sort of elegibility criteria :)
21:11:49  &lt;dg&gt; aye
21:12:07  &lt;dg&gt; Let's get started
21:12:10  &lt;dg&gt; * Motivating the community - "are bounties appropriate?"
21:12:13  &lt;lillith&gt; i expect asdfsdafsdafsd wishes to be invluded int points 1+2 :)
21:12:24  &lt;orion&gt; Are bounties working?
21:12:43  &lt;dg&gt; Everything merged into one big argument last time over bounties, management and BTC so trying to spread it out this time & be dignified.
21:12:53  &lt;LaughingBuddha&gt; Who's the guy for bounties? eche|on?
21:13:00  &lt;lillith&gt; yep
21:13:11  &lt;LaughingBuddha&gt; Is he here?
21:13:11  &lt;str4d&gt; Determining if bounties are working depends on what the defined purpose of a bounty is.
21:13:11  &lt;dg&gt; define "working". Are they, IMO, bringing in the developers or fixes we need? No.
21:13:18  &lt;lillith&gt; he's in control of all money - point 2 :)
21:13:25  &lt;orion&gt; Then let's think of something else.
21:13:40  &lt;dg&gt; The bounty system does not seem to be working for even the bounties themselves.
21:13:54  &lt;lillith&gt; i think there should be some sort of benefit or incentive further than loving i2p
21:14:09  &lt;dg&gt; A lot of the links on the page are 404s too but that's an unrelated issue
21:14:12  &lt;str4d&gt; From the bounties page: " Instead, we are making use of a bounty system, whereby anyone can get support for working on something that people want implemented, and people who want to contribute to I2P can be assured that their support goes to what they care about."
21:14:12  &lt;lillith&gt; we have to draw people in then keep them with our charm and civility ;)
21:14:23  &lt;LaughingBuddha&gt; Not that I'm in the position to work on any of the bounties, but they seemed to quite vague last time i looked at them
21:14:30  &lt;LaughingBuddha&gt; to be*
21:14:37  &lt;orion&gt; The only thing that will draw attention to I2P is content.
21:14:45  &lt;dg&gt; eche|on posted his thoughts here - http://zzz.i2p/topics/1359 - if he could not attend.
21:14:48  &lt;nom&gt; imo bounties do not work, because a code base is only as good as its maintenance, and paying someone for 'completion' gives the wrong ideas/incentives about what we need in terms of developers, for code to be worth using on a distributed scale, it has to be continually worked on by motivated people. having one person create a code base, get paid and possibly disappear does nothing to benefit the community
21:14:51  &lt;iRelay&gt; Title: zzz.i2p: Managing the project (at zzz.i2p)
21:14:57  &lt;lillith&gt; str4d: instead, as opposed to...?
21:15:17  &lt;str4d&gt; From that statement above, the purpose of bounties would seem to be to finance one-off drives to get specific features implemented.
21:15:20  &lt;Umlaut&gt; are bounties appropriate? - I think it depends, imo bounties for devs, for particular project and where no contest/conmpetiotion is involved - in such cases they are appropriate
21:15:26  &lt;iRelay&gt; &lt;weltende@freenode&gt; nom: it worked in the past if you look at the bounty page..
21:15:30  &lt;dg&gt; str4d: Is that what we want?
21:15:41  &lt;LaughingBuddha&gt; nom: agreed
21:15:48  &lt;str4d&gt; Does that work? Somewhat.
21:16:03  &lt;str4d&gt; weltende, exactly. There are clear examples of bounties being taken.
21:16:18  &lt;dg&gt; http://www.i2p2.de/bounties.html
21:16:29  &lt;iRelay&gt; Title: Bounties - I2P (at www.i2p2.de)
21:16:34  &lt;str4d&gt; Bounty uptake IS slow, due to a lack of visibility/advertising/marketing/whatever, but the bounties are slowly getting taken.
21:16:41  &lt;dg&gt; I don't know if the bounties which are being fufilled are perhaps not being fufilled the way we want too.
21:17:03  &lt;str4d&gt; But, of the claimed bounties, not a single developer is currently with I2P.
21:17:10  &lt;dg&gt; For example: "Datastore over I2P" - "CLAIMED for 700 euro" - "duck, smeghead"
21:17:20  &lt;lillith&gt; perhaps, change bounties to ..... and maintain your work for a reasonable time
21:17:23  &lt;nom&gt; to get actual continuous development going, a better model is one of project/stipends, where people donate to a project with stated goals, and the people running that project pay the money out continuously to people who are actively working to accomplish those goals
21:17:34  &lt;dg&gt; The solution was, IMO, hacky, the bountry $$$ was rather high for the hack and the two developers for that bounty are nowhere to be found.
21:17:46  &lt;str4d&gt; dg: that's irrelevant - as per the current bounty outline, it is up to the donor to decide on the completion.
21:18:01  &lt;dg&gt; What if multiple donors exist?
21:18:08  &lt;str4d&gt; First donor.
21:18:11  &lt;orion&gt; I don't like bounties. IMO, the one way to draw developers in is to draw attention to I2P.
21:18:15  &lt;str4d&gt; (as per current outline)
21:18:21  &lt;iRelay&gt; &lt;weltende@freenode&gt; lillith: not really needed imho if it's in the core router..
21:18:25  &lt;str4d&gt; If a bounty is funded by I2P, then it does become relevant as I2P itself is the judge.
21:18:32  &lt;dg&gt; Oh. That doesn't seem right. :s.
21:18:54  &lt;orion&gt; IMO, the best way to draw attention to I2P is by providing content.
21:19:06  &lt;dg&gt; Right, but some of the bounties can lead to content.
21:19:13  &lt;str4d&gt; I'm not arguing for the current bounty system, just outlining it.
21:19:44  &lt;dg&gt; str4d: right, and thanks.
21:20:03  &lt;nom&gt; honestly i think a big part of the problem is that were conflating things that are directly part of the i2p code base, with things that are simply run ontop of i2p. ex translation vs datastore
21:20:03  &lt;str4d&gt; The biggest problem with a semi-anonymous project like I2P is developer retention. The current bounty model does nothing to help that.
21:20:42  &lt;dg&gt; I'm against the bounty system as it doesn't help the ecosystem we have, evidently (none of the developers are here today..) and I feel project funds could be better allocated.
21:20:57  &lt;nom&gt; a bounty/payment for one person to do one specific part of the code base is fine in theory, but they don't work for creating continuous development of apps/systems that run ontop of i2p
21:21:12  &lt;str4d&gt; I concur.
21:21:17  &lt;iRelay&gt; &lt;weltende@freenode&gt; dg: well.. if there aren't taken, then the money isn't spent..
21:21:54  &lt;dg&gt; weltende: The funds are in reserve, they cannot be spent as they are allocated for spending on $bounty.
21:21:57  &lt;nom&gt; like adding unit tests to i2p could be worth a bounty, but it would probably be better to make an arrangement with coders who will be paid a small amount continuously to keep adding more unit tests as needed
21:22:03  &lt;iRelay&gt; &lt;weltende@freenode&gt; if you however think that for a certain bounty the code isn't good enough or so.. it might be a good idea to specify more clearly in the bounty description what needs to be done
21:22:26  &lt;iRelay&gt; &lt;weltende@freenode&gt; dg: which is only a problem if we have to spend the money right away
21:23:01  &lt;iRelay&gt; &lt;weltende@freenode&gt; it's not reserved forever as you can see in the bounty page.. funds have gone back to the money pool before
21:23:21  &lt;dg&gt; weltende: I doubt we will ever be at the point where we NEED the funds allocated to bounties but it seems redundant.
21:23:44  &lt;str4d&gt; Fund allocation is beside the current point.
21:23:59  &lt;iRelay&gt; &lt;weltende@freenode&gt; dg: exactly my point
21:24:11  &lt;lillith&gt; dg: are competitions included in bounties or are they point 1.5?
21:24:14  &lt;str4d&gt; There will always be money, in one way or another.
21:24:26  &lt;str4d&gt; (Or not)
21:24:29  &lt;nom&gt; i think the datastore is a great example of where bounties shouldn't be used, for something as complex as a universal datastore to be viable, it has to be its own project with active developers, paying someone for completion will get you something that is marginally functional, but it will never improve
21:24:40  &lt;LaughingBuddha&gt; ^
21:24:40  &lt;str4d&gt; nom: agreed.
21:24:43  &lt;dg&gt; lillith: Competitions hadn't occurred to me but I suppose it would be the point after this.
21:24:46  &lt;Umlaut&gt; Let me refer to the i2p artwork contest for 29c3 - Was that really a dev project? Was it appropriate to use bounties in it? While there was no even strict criteria stated?
21:24:57  &lt;str4d&gt; The result will satisfy the bounty, but likely will not scale.
21:25:00  &lt;dg&gt; nom: Couldn't have said it better myself.
21:25:26  &lt;iRelay&gt; &lt;weltende@freenode&gt; nom: torrents were nothing but a bounty either..
21:25:34  &lt;LaughingBuddha&gt; Umlaut: i thought they were echelons personal funds?
21:25:54  &lt;Umlaut&gt; if I was willing to contribute to the contest, the bounty would rather discourage me?
21:26:01  &lt;lillith&gt; (most) bounties are set by users - between giving them a choice and them not donating at all, at least with a bounty they have some say in what happens
21:26:32  &lt;nom&gt; to put it another way... there are no bounties at google....
21:26:32  &lt;Umlaut&gt; LaughingBuddha really? then sorry, I wasn't aware about that
21:26:32  &lt;nom&gt; weltende yes but zzz is continuing to work on snark isn't he?
21:26:47  &lt;str4d&gt; If I2P had an established structure for spinning off projects (or acting as an umbrella for them) then that would be a different matter (but that ties in to the later point about "official"ness).
21:26:51  &lt;LaughingBuddha&gt; Umlaut: I might be mistaken but I thought i read that somewhere
21:27:04  &lt;str4d&gt; I think that bounties are useful, but not in the way that they are currently being marketed.
21:27:08  &lt;lillith&gt; LaughingBuddha: all i2p's funds are technically eche|on's personal money
21:27:11  &lt;dg&gt; nom: zzz was around anyway though. I think his motivations and such are different than gaining rewards and the bounty program has little to do with it. I do not believe he gained anything from the torrent bounty either.
21:27:18  &lt;str4d&gt; And that they shouldn't be the main focus.
21:27:21  &lt;iRelay&gt; &lt;weltende@freenode&gt; nom: yes.. but without the bounty there wouldn't have been a codebase to begin with.. (and he was not part of the bounty dev team)
21:27:21  &lt;dg&gt; We'll get to the money later..
21:27:40  &lt;LaughingBuddha&gt; lillith: Doesn't he "manage" it?
21:27:47  &lt;LaughingBuddha&gt; dg: ok
21:28:10  &lt;str4d&gt; weltende, you are making a good point.
21:28:14  &lt;lillith&gt; i2p is no legal entity, so it can't own anything. hence it is eche|on's personal money.
21:28:29  &lt;str4d&gt; Bounties are useful for kickstarting code, not for continued development.
21:28:36  &lt;LaughingBuddha&gt; lillith: I see
21:28:36  &lt;nom&gt; if you want continuous development you should pay developers continuously to work on things they want to work on. donating money to get something done is fine, but it shouldn't be given as a lump sum to whoever can get an 0.0.1 working first, it should be used to fund project development over time
21:28:39  &lt;lillith&gt; he could legally leave with it all one day (he wouldnt', but he could)
21:28:48  &lt;iRelay&gt; &lt;weltende@freenode&gt; nom: and I don't really see your point with no bounties at google.. the people that work for google get paid to work there..
21:28:52  &lt;lillith&gt; ^this
21:29:27  &lt;LaughingBuddha&gt; But it seems we agree with the first part of nom's statement. No?
21:29:30  &lt;lillith&gt; eg bounty of $X per month to work on something
21:29:45  &lt;LaughingBuddha&gt; Yeah
21:29:52  &lt;iRelay&gt; &lt;weltende@freenode&gt; or perhaps define milestones in the bounty?
21:29:56  &lt;Meeh&gt; Seems like a good solution
21:30:07  &lt;iRelay&gt; &lt;weltende@freenode&gt; (and upon reaching milestone $X you get $Y amount of money)
21:30:07  &lt;dg&gt; That sounds good.
21:30:14  &lt;LaughingBuddha&gt; milestones seem like a good idea
21:30:17  &lt;LaughingBuddha&gt; but they need to be clearly outlined
21:30:20  &lt;dg&gt; Milestones + continuous payment?
21:30:20  &lt;nom&gt; lol thats what my point was, they get paid, and they do work, and the work they do isn't directly connected with how they get paid. ofc if they stopped doing work, they would stop getting paid, but their not getting paid for completing a specific piece of code, their getting paid enough to live on and spend their lives coding
21:30:23  &lt;str4d&gt; Milestones is sort of like what the Unit Tests bounty currently has.
21:30:27  &lt;lillith&gt; is it eche|on we have to ask nicely to change the website etc?
21:30:38  &lt;dg&gt; no, website is in mtn
21:30:41  &lt;Umlaut&gt; nom I agree with your point, paying to the devs who are reliable and known for being good contributors
21:30:44  &lt;str4d&gt; lillith: no, anyone can change the website.
21:30:54  &lt;Meeh&gt; Or keep a part of the bounty as a "continued support" payment per month of the application/whatever
21:31:22  &lt;Meeh&gt; So we don't get outdated apps, libs, etc.
21:31:29  &lt;LaughingBuddha&gt; Would the project be judged at every milestone then?
21:31:44  &lt;dg&gt; LaughingBuddha: good point. Who by?
21:32:00  &lt;nom&gt; eh, milestones are just smaller bounties... a simpler solution is to have a pool of money for a project, and someone/group of someones who pay the money to people who are actively working on it
21:32:03  &lt;dg&gt; The "board"? (Againg, getting to this later).
21:32:10  &lt;LaughingBuddha&gt; Dev board?
21:32:10  &lt;LaughingBuddha&gt; yeah
21:32:29  &lt;nom&gt; generally you would end up with the dev board being the same people who are getting paid ofc...
21:32:46  &lt;lillith&gt; to make anything decided upon here 'official', is that as simple as someone checking an update to the website into mtn?
21:32:55  &lt;LaughingBuddha&gt; how many active devs are there working on the i2p codebase?
21:32:58  &lt;Umlaut&gt; also you need to take under consideration how the current donating system looks from the potential donor (someone new to i2p community especially) point of view
21:33:04  &lt;lillith&gt; LaughingBuddha: one
21:33:07  &lt;dg&gt; lillith: Kinda. And posting ot zzz.i2p. ;_;
21:33:15  &lt;dg&gt; The dev board determine the state of $project and decide if it should continue to get funding?
21:33:18  &lt;Umlaut&gt; i could be one of them
21:33:25  &lt;dg&gt; LaughingBuddha: 2, 3?
21:33:32  &lt;LaughingBuddha&gt; hmm
21:33:47  &lt;nom&gt; the board / employees model seems to work pretty well for 99% of the corporations in the world. you have a group of people who are the most committed and have already contributed a lot who manage the money, and you have people who join and contribute and get paid for their efforts based on the judgement of the long time contributors
21:33:54  &lt;LaughingBuddha&gt; What if we set up a board of min. 5 people who are knowledgeable on the subject?
21:34:01  &lt;LaughingBuddha&gt; Devs + Users
21:34:09  &lt;Umlaut&gt; and i would trust the system more if there was more than one person, something like mentioned already dev-board which handles the money
21:34:24  &lt;orion&gt; What if you had to pay to be on the board?
21:34:31  &lt;LaughingBuddha&gt; wut
21:34:38  &lt;nom&gt; (this only works tho if you can separate i2p proper projects, from projects that just run on i2p, which should not be managed by the i2p dev team itself)
21:34:38  &lt;str4d&gt; orion: not a good model.
21:34:47  &lt;str4d&gt; inb4 Russian oligarch takes over I2P
21:34:57  &lt;LaughingBuddha&gt; haha
21:35:06  &lt;nom&gt; inb4 already happened, zzz = vladimir
21:35:10  &lt;orion&gt; Pay in code.
21:35:29  &lt;LaughingBuddha&gt; And how do you measure how much you have to pay?
21:35:32  &lt;LaughingBuddha&gt; 200 lines of code?
21:35:35  &lt;lillith&gt; some people are big contributers without coding
21:35:46  &lt;orion&gt; No idea, just brainstorming.
21:35:49  &lt;nom&gt; like any oligarchy the only natural system is election by the existing board
21:35:49  &lt;str4d&gt; Exactly.
21:36:03  &lt;dg&gt; So, would the normal "dev" (team) board (coming up later) decide if $project is worth paying out to?
21:36:15  &lt;dg&gt; Overcomplication will lead to it not being done
21:36:22  &lt;lillith&gt; 3 tiers: inner circle, outer circle, others
21:36:30  &lt;LaughingBuddha&gt; lillith: i like that
21:36:37  &lt;lillith&gt; other = new/ unknown people
21:36:51  &lt;lillith&gt; outer circle = known/ trusted people
21:36:51  &lt;LaughingBuddha&gt; because we don't seem to have enough devs for a real judge panel
21:37:02  &lt;Umlaut&gt; dg I would think so as the devs should know *best* what project are most important/urgent/worth spending money on
21:37:05  &lt;lillith&gt; inner circle voted for by outer circle
21:37:20  &lt;nom&gt; its a hierarchy, the i2p project as a whole is more than just the i2p dev team, but they are the tip of the spear so to speak. they get / have the most donations / resources. but other projects built ontop of i2p wouldn't be managed by the i2p dev team, but could get funding from i2p proper
21:37:23  &lt;lillith&gt; kind like meetings but more structured hierachally
21:38:13  &lt;dg&gt; imo &lt;+dg&gt; Overcomplication will lead to it not being done
21:38:37  &lt;iRelay&gt; &lt;weltende@freenode&gt; +1
21:39:15  &lt;dg&gt; The whole (team/dev) "board" idea ties in nicely as we will be discussing this next anyway
21:39:22  &lt;dg&gt; Should we leave this for another time or ...?
21:39:28  &lt;nom&gt; in short, zzz eche and whoever else they consider to be part of the 'board' of i2p are in charge of the money/decisions (they already are), and other projects on i2p should be structured similarly with their own boards of decision makers. instead of bounties for a sub project (datastore, btc client, etc) the bountie should be given to the board for that project, and let them decide how to spend it to get things done
21:39:39  &lt;lillith&gt; so shall we get back on topic or has bouties been discussed to death?
21:40:49  &lt;nom&gt; and the decision to give a bounty to a board of devs for a project obviously has to be made by the board of i2p, that way you don't have 3 people show up, say their gonna do something, get the money and then never do it.
21:41:13  &lt;dg&gt; nom: +1
21:41:21  &lt;Meeh&gt; nom: +1
21:41:24  &lt;LaughingBuddha&gt; nom: I think it's payed out upon completion
21:41:34  &lt;iRelay&gt; &lt;str4d@freenode&gt; nom++
21:41:46  &lt;LaughingBuddha&gt; nom: +1
21:41:54  &lt;dg&gt; I think that's a good note to end on? :)
21:42:14  &lt;Meeh&gt; Agreed
21:42:24  &lt;nom&gt; in the future it would be better for donators to give directly to the sub project if a board/group already exists, instead of donating to eche to create a bounty. since if theres already a group working on it, they would be the best to determine how to use the money to accomplish those goals
21:42:53  &lt;dg&gt; ok, moving on
21:42:58  &lt;Umlaut&gt; nom that makes perfect sense
21:43:01  &lt;Umlaut&gt; nom++
21:43:11  * nom raises his glass, cheers mates
21:43:18  &lt;dg&gt; I feel we have covered "managing money" mostly and it comes under "making the project official" anyway
21:43:21  &lt;LaughingBuddha&gt; :)
21:43:21  &lt;dg&gt; So let's do the latter?
21:43:47  &lt;lillith&gt; clarify the position on money first for lurkers?
21:43:54  &lt;iRelay&gt; &lt;weltende@freenode&gt; for an e.V. we would at least 7 people who are willing to go public as members
21:43:55  &lt;LaughingBuddha&gt; Official = Register as Organisation?
21:44:26  &lt;dg&gt; LaughingBuddha: yes
21:44:29  &lt;Meeh&gt; in case register as a organization, in which country?
21:45:01  &lt;dg&gt; lillith: Bounty funds should go to teams assigned by the core I2P board.. if we go ahead with that.
21:45:04  &lt;dg&gt; Meeh: US, I assume?
21:45:07  &lt;Meeh&gt; that also need deanonymization of sertiant people
21:45:14  &lt;Umlaut&gt; ok so who are the brave souls to give up their anonymity (if that means going official)?
21:45:17  &lt;orion&gt; What did you guys decide on?
21:45:20  &lt;iRelay&gt; &lt;str4d@freenode&gt; Not necessarily the US
21:45:28  &lt;nom&gt; idk if 'offical' designation would really be all that useful... i honestly can't see what the benefit would be
21:45:31  &lt;lillith&gt; presumably the people have to be in the US too?
21:45:54  &lt;lillith&gt; nom: a legal entity to donate to
21:45:54  &lt;nom&gt; other than to put the project/people more on the radar of the powers that be...
21:46:06  &lt;Meeh&gt; I can give out my identity, so no problem for me.. But I guess I'm not allowed into the US, so yea.
21:46:17  &lt;orion&gt; Registration is stupid.
21:46:28  &lt;LaughingBuddha&gt; dg: What are the benefits?
21:46:39  &lt;orion&gt; Let's just spread out the money among different "accounts" managed by different people.
21:46:55  &lt;orion&gt; I.e, the eche|on account, the zzz account, the dg account, etc.
21:46:57  &lt;LaughingBuddha&gt; A wallet for each (sub)project?
21:47:04  &lt;dg&gt; LaughingBuddha: Managing the project's money under "I2P" and not a singular person, or persons. An official guise is far less suspicious and accountable.
21:47:09  &lt;orion&gt; No.
21:47:12  &lt;Umlaut&gt; Do you think that going official would bring some real benefits to the i2p-world?
21:47:14  &lt;iRelay&gt; &lt;weltende@freenode&gt; orion: not sure if the tax office might not find tht fishy
21:47:14  &lt;orion&gt; Just different "accounts".
21:47:32  * nom thinks the focus should be more on the logistics of the hierarchy of boards / democracy / voting thing. to actually have a system like that we would need either a well run website, or some sort of distributed system for it
21:47:35  &lt;LaughingBuddha&gt; dg: I see
21:47:46  &lt;iRelay&gt; &lt;weltende@freenode&gt; it would certainly bring a lot of paperwork
21:47:54  &lt;lillith&gt; Umlaut: no more complaining about eche|on holding the money
21:48:04  &lt;iRelay&gt; &lt;str4d@freenode&gt; nom++
21:48:13  &lt;iRelay&gt; * str4d@freenode clones nom's brain
21:48:14  &lt;dg&gt; nom: perhaps so, yeah. If we can arrange that, then we can come to a consensus on this..
21:48:44  &lt;orion&gt; For the record, if you guys want to do something that requires giving up anonymity, I will do it.
21:48:57  &lt;dg&gt; git clone http://git.repo.i2p/repo/nom.git
21:49:00  &lt;LaughingBuddha&gt; I'd consider it
21:49:03  &lt;iRelay&gt; &lt;str4d@freenode&gt; Going "official" is primarily a financial decision IMHO; it doesn't really contribute to the structure.
21:49:22  &lt;orion&gt; Even though I am opposed to the idea of going to the government, I will do it if that is what the project decides is best.
21:49:40  &lt;dg&gt; So, let's change the focus to the organizational structure
21:49:51  &lt;dg&gt; (As that supercedes this anyhow)
21:50:06  &lt;iRelay&gt; &lt;weltende@freenode&gt; str4d: well.. e.V. requires the members to vote for an board once a year... so we already have procedure for voting for the board then ;)
21:50:14  &lt;dg&gt; "The Debian project only allows voting to be done by 'Debian Developers' (where "$developer" = "any sort of contributor"). If there is any sort of voting system enabled here it would need to be limited in a similar fashion, otherwise the system would be ripe for abuse, allowing for a small but vocal clique to push its demands through."
21:50:21  &lt;dg&gt; Should we adopt a similar approach?
21:50:25  &lt;LaughingBuddha&gt; (for the e.V.)
21:50:44  &lt;lillith&gt; how much do you need to contribute to be a contributer?
21:50:59  &lt;iRelay&gt; &lt;str4d@freenode&gt; The problem with the "Debian Developers" approach is the number of developers I2P has (very few)
21:51:05  &lt;lillith&gt; ie is being active in #i2p-help enough?
21:51:25  &lt;Meeh&gt; we must find a definition on contributer
21:51:33  &lt;sigint&gt; for what?
21:51:36  * lillith does not read 'contributer' as 'code contributer'
21:51:55  &lt;dg&gt; str4d: "any sort of contributor".
21:51:59  &lt;lillith&gt; sigint: read scrollback on sighup ;)
21:52:10  &lt;sigint&gt; will do
21:52:12  &lt;iRelay&gt; &lt;str4d@freenode&gt; dg, yeah, just read that part *derp*
21:52:12  &lt;nom&gt; org structure is pretty simple in theory, just have a three tiered system of board members (elected by the existing board oligarchy), contributors (elected at large by the existing group of contributors), and users (everyone else, including people who /want/ to be seen as contributors, but havn't been around long enough for people generally to trust them)
21:52:27  &lt;lillith&gt; sighup's like your little brother ;)
21:52:39  &lt;Umlaut&gt; it all depends on the scale of contribution, reliability of the contributor and other factors
21:53:06  &lt;nom&gt; sorta like, royalty, nobility, and the commoners....
21:53:13  &lt;Umlaut&gt; reliability = being trusted by others
21:53:16  &lt;lillith&gt; maybe a good start will be starting with rough numbers and working from there?
21:53:31  &lt;Umlaut&gt; nom i'm actaually referring to what you have said
21:54:09  &lt;Umlaut&gt; not reliable = someone who promised to do something, raised some hope and then run away (with a bounty..)
21:54:24  &lt;nom&gt; hmm yah
21:55:35  &lt;dg&gt; nom: "existing"?
21:56:15  &lt;orion&gt; I gotta go. In closing I just want to say that having funds in one central location makes it easier to steal by oppressive governments, and that if we need to do something which requires giving up my anonymity, I will do it. Cya
21:56:26  &lt;nom&gt; perhaps, supreme court(board), senate(contributors) and house(users) would be better... the board has the real control over all the decisions, but they take into account the votes of the contributors who are trusted identities, and the votes of the general population of users too, but you don't weigh that too much as theres no real protection against people making tons of user idents to vote with
21:56:33  &lt;lillith&gt; bye orion :)
21:56:37  &lt;dg&gt; Should we cut now and continue this next week at the same time?
21:56:40  &lt;nom&gt; o/ orion
21:56:50  &lt;dg&gt; An hour is long, I don't want this to drag on.
21:57:04  &lt;orion&gt; Whatever you want.
21:57:07  &lt;lillith&gt; dg: i'm up for that
21:57:17  &lt;iRelay&gt; &lt;str4d@freenode&gt; I'm happy to continue next week.
21:57:26  &lt;lillith&gt; gives time to ponder what has already been said
21:57:29  &lt;nom&gt; sure, sounds good
21:57:31  &lt;iRelay&gt; &lt;str4d@freenode&gt; We need to think this over.
21:57:43  &lt;iRelay&gt; &lt;str4d@freenode&gt; And hopefully a few more people show up then ^_^
21:58:07  * nom thinks the main takeaway here is that we could use a site / system to have group decision making / voting on
21:58:07  &lt;lillith&gt; yes...
21:58:14  &lt;dg&gt; I agree, sounds good guys. I'll update the zzz.i2p topic soon (poke me if I don't in 24 hours).
21:58:25  &lt;dg&gt; thanks all. :)
21:58:29  &lt;LaughingBuddha&gt; Good session
21:58:32  * lillith picks up the baffer menacingly
21:58:42  &lt;dg&gt; ;) go
21:58:53  &lt;Umlaut&gt; thanks for letting me join
21:58:53  &lt;lillith&gt; *baf* meeting closed :)
21:59:04  &lt;Umlaut&gt; lights out!
21:59:06  &lt;lillith&gt; thank you, and goodnight :)
21:59:19  &lt;sigint&gt; Great. I joined in right at the end. I forgot that there even was one :|
21:59:22  &lt;nom&gt; inb4 massive well timed netsplit
21:59:25  &lt;sigint&gt; brb, reading backlog
21:59:28  &lt;sponge&gt; o/
21:59:40  &lt;Umlaut&gt; sigint timezone fail?
21:59:50  &lt;iRelay&gt; &lt;str4d@freenode&gt; o/ sponge.
21:59:50  &lt;sponge&gt; :-)
21:59:57  &lt;lillith&gt; sigint: same time next week ;) say anything you missed the chance to then :)
22:00:12  &lt;sponge&gt; orion wants to know about my ideas I see...
22:00:50  &lt;iRelay&gt; &lt;str4d@freenode&gt; I pointed him in your direction sponge - figured pooling the creative juices was a good idea.
22:01:05  &lt;sigint&gt; lillith: i hadn't explicitely planned on joining this meeting, but it would have been nice. no big deal though. i do have an idea that would be good to bring up in next week's meeting.
22:01:09  &lt;sponge&gt; Yes, excellent.
22:01:32  &lt;sponge&gt; I need people to help with my ideas... I have too many
22:01:35  &lt;sigint&gt; idea: offer btc rewards for security vulnerabilities
22:01:39  &lt;lillith&gt; sigint: it's dg you'll want to talk to on that then :)
22:01:41  &lt;iRelay&gt; &lt;str4d@freenode&gt; (And orions work on i2pcpp has proven that he is good at implementing stuff ^_^)
22:01:58  &lt;iRelay&gt; &lt;str4d@freenode&gt; sigint, post any ideas for next week in the zzz.i2p thread.
22:01:59  * lillith raises eyebrows
22:02:07  &lt;lillith&gt; vairy interesting
22:02:10  &lt;sigint&gt; will do
</div>
