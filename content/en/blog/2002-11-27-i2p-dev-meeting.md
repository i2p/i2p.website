---
title: "I2P dev meeting"
date: 2002-11-27
author: "nop"
description: "I2P development meeting covering project updates and technical discussions"
categories: ["meeting"]
---

(Courtesy of the wayback machine http://www.archive.org/)

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> Aprogas, athena, bpb, crunchman, Disposable, Fairwitness, Gilles2Rais, hezekiah, Kyfhon, mateofree, nemesis, nop, ptsc, Rain, rda, xenode</p>

## Meeting Log

<div class="irc-log">
--- Log opened Tue Nov 26 22:43:56 2002
22:44 -!- Topic for #iip-dev: IIP meeting | logs: http://mids.student.utwente.nl/~mids/iip/ | sneak rc3 preview for unix http://mids.student.utwente.nl/~mids/iip/iip-1.1-rc3-mids1.tgz | please give feedback
22:44 [Users #iip-dev]
22:44 [ CwZ|away] [ Disposable] [ icepick] [ logger] [ pox] [ UserX]
22:44 -!- Irssi: #iip-dev: Total of 6 nicks [0 ops, 0 halfops, 0 voices, 6 normal]
22:44 -!- Irssi: Join to #iip-dev was synced in 2 secs
22:44 < logger> test
23:35 < nop> IIP dev meeting in 25 minutes, Special appearance by Capn' crunch aka John Draper
23:36 < Disposable> cool
23:36 < Disposable> the famous capncrunch
23:36 < Disposable> :P
23:36 < nop> yes
23:37 < nop> friend of mine
23:37 < nop> ;)
23:37 < Disposable> yeah?
23:37 < nop> he's working on porting iip to mac os 9
23:37 < Disposable>  cool
23:37 < ptsc> unfortunately i'm off to do laundry but will lurk
23:37 < nop> ok
23:37 < ptsc> nop, why not an os x.2 clean version?
23:37  * Disposable is listening to The Beets - Killer Tofu
23:37 < nop> what?
23:37 < nop> ptsc, we have os x versions
23:37 < Disposable> hmmm
23:37 < nop> we need os 9
23:38 < nop> because there are still a lot of people on it
23:38 < ptsc> ah, okay.  i was considering getting a mac that could run os x
23:38 < nop> yes
23:38 < nop> but only 20% of mac users have switched to X
23:38 < ptsc> in my case, i'd be switching to mac specifically *because* of x
23:39 < Disposable> lol
23:39 < Disposable> yeah
23:39 < Disposable> it looks so sweet
23:39 < Disposable> :)
23:39 < Disposable> i wunna try it
23:39 < Rain> "unix for users done right" some feel
23:39 < ptsc> i saw it at a friend's house who has been a mac freak for ages
23:39 < ptsc> and it just looks awesome
23:39 < ptsc> plus they brought back the NeXT-style file browser
23:39 < ptsc> which has always ruled
23:39 < ptsc> ok bbl
23:39 < Rain> "the first lickable interface", according to mr jobs.
23:40 < ptsc> ok bbl
23:41 < Disposable> :/
23:48 < Disposable> wb
--- Day changed Wed Nov 27 2002
00:00 < nemesis> blubb
00:00 < nemesis> 23 UTC
00:00 < nop> ok
00:00 < nop> welcome to the 21st iip meeting
00:01 < nop> on the agenda
00:01 < nop> 1) welcome
00:01 < nop> 2) why rc3 isn't released yet
00:01 < nop> 3) when will it be released
00:01 < nop> 4) OS 9 port by Cap'n Crunch
00:01 < nop> 5) Questions and comments
00:02 < nop> ok
00:02 < nop> welcome
00:02 < nop> :)
00:02 < nop> codeshark is out of the country on business, and will be back later this week
00:02 < nop> he's our release coordinator
00:02 < nop> and if he's not back shortly, mids and I will arrange the release candidate
00:02 < nop> and do it that way by friday
00:02 < Aprogas> one should only accept the function of release coordinator, if one knows to have time for that function
00:02 < nop> when will it be released, friday at latest
00:03 < nop> comments are saved for last
00:03 < nop> thnx though aprogas
00:03 < Aprogas> ok
00:03 < nop> ok, os 9 port, Cap'n Crunch has been working (along with his friend) on porting IIP to mac os 9 users
00:04 < nop> hopefully, he will be on here shortly to give us some detail
00:04 < nop> if not I'll send out an email
00:04 < nop> to iip-dev with the latest from him
00:04 < nop> oh speak of the devil
00:04 < crunchman> Ok,   I'm on
00:04 < nop> Hi crunch
00:04 < Aprogas> nop: that must be bpb in disguise
00:04 < nop> can you give us a quick detail of what's going on with os 9
00:04 < crunchman> Of course I didn't get the chance to read over the source so I can bring up my issues.
00:05 < nop> k
00:05 < crunchman> yes - I can.
00:05 < nop> the floor is yours, take it away
00:05 < crunchman> basically - the way IIP was written,  it's a CAAN OF WORMS if I have to use the structures you are already using.
00:06 < crunchman> There is NO discrete seperation between the GUI and the guts.
00:06 < crunchman> Let me explain.
00:06 < crunchman> It is VERY baised towards WinBlows.
00:06 < crunchman> As you know,  the Mac uses resources for the GUI components.
00:07 < crunchman> I need to examine the code now,   and would like to take a few mins to go over my notes,  so I can be more specific.
00:07 < nop> ok
00:07 < nop> either way, we can cover that later, but Crunch is working on the os 9, and we will aid him with what we can so that it may be not so tedious a task
00:08 < nop> reasons for the port, is only 20% of mac users have made the switch to os x
00:08 < nop> they still rely on os 9
00:08 < nop> so a lot of mac os users donated money towards this goal
00:08 < nop> and any other donations are welcome to assist crunch for his time on this project
00:09 < nop> questions and comments from iip users etc
00:09 < nop> ?
00:09  * Disposable is listening to Creedence Clearwater Revival - Fortunate Son
00:09 < Aprogas> comment: one should only accept the function of release coordinator, if one knows to have time for that function
00:09 < Rain> question: what will be new in rc3
00:09 < Rain> ?
00:09 < nop> mainly bug fixes, hold, I'll get the changelog
00:09 < Aprogas> /exec -o cat ChangeLog | head -200
00:10 < bpb> question: since when does IIP get donations?
00:10 < crunchman> bob cant get on
00:10 < nop> + iip1.1-rc3:
00:10 < nop> + - Display of version number for windows (menu option) and unix (command line).
00:10 < nop> + - Random number generation fix.
00:10 < nop> + - IIP network connections are no longer paused while in the setup screen.
00:10 < nop> + - Now exits if it can't bind to a socket at startup.
00:10 < nop> +   Windows now displays a message box informing that it can't bind to port.
00:10 < nop> + - Several bugfixes and one memory leak fixed.
00:10 < crunchman> i
00:10 < nop> +
00:10 < crunchman> im on phone - helping him
00:10 < crunchman> hold on
00:10 < nop> k
00:10 < nop> that is the changelog
00:11 < Aprogas> comment: women are always late
00:11 < crunchman> hold on - still on phone w/ bob
00:11 < Rain> ok, thanks.
00:11 < nop> haha
00:11 < nop> ok meeting is officially over
00:11 < bpb> if he can't get iip to work, he could connect to my node
00:11 < Aprogas> huh ?
00:12 < nop> I will resume talks with crunch in here
00:12 < athena> okay, so i can slap aprogas now?
00:12 < Aprogas> but maybe i still had questions or commens
00:12 < bpb> :)
00:12 < nop> aprogas
00:12 < nop> do you have any more questions
00:12 < Aprogas> am i being ignored?
00:12 < nop> or comments
00:12 < nop> that pertains to IIP
00:12 < Rain> is the "sneak release" the same as the final one, and will i dare running it on a public proxy at this stage?
00:12 < crunchman> meeting is over?  - but we havent even gotten on yet!
00:12 < Aprogas> where is mids?
00:12 < bpb> crunchman: that's nop for you...
00:12 < nop> crunch we can still talk in here
00:12 < Aprogas> no mids no meeting
00:12 < crunchman> Bob is trying to get on - and yet the meeting is now over?
00:12 < nop> rain sneak is the same yes
00:12 < nemesis> hm... nop, i use blackbox under windows xp, why theres no cmd line version of IIP out?
00:12 < nemesis> that i can use as an service..
00:12 < crunchman> bpb - I have no clue what you mean by "crunchman: that's nop for you"
00:12 < Aprogas> bpb means nothing with it
00:12 < Aprogas> he loves to confuse people
00:13 < nop> well, nemesis iip -d might be able to do that for you
00:13 < crunchman> still trying to get bob logged in.
00:13 < bpb> crunchman: he's cutting off the meeting after it hasn't begun
00:13 < nop> the "official" meeting is over
00:13 < Disposable> hehe
00:13 < nop> other than comments
00:13 < crunchman> sorry I couldn't get on sooner.
00:13 < Rain> ok, so i might as well de-install the rc2 proxy i recently installed today, and replace it with rc3, no risk?
00:13 < Aprogas> nop: will there be an rc4 or even rc5, and when are they expected, and when is iip 1.1 expected?
00:13 < nop> rc3 should be final before 1.1
00:13 < nop> unless
00:14 < Aprogas> of course the release candidate comes before the release
00:14 < crunchman> Could someone call bob on phone and help him
00:14 < nop> unless major bugs were found
00:14 < nemesis> hm....
00:14 < Aprogas> nop: why do i get the idea you forget what a rc is all the time ?
00:14 < nemesis> nop, must i shutdown my current iip for -d?
00:14 < Aprogas> nop: so when are 1.1 and 1.1-rc3 expected?
00:14  * bpb remembers when decentralized 2.0 was expected ;)
00:14 < nemesis> crunchman: help with what?
00:15 < crunchman> bob cant get on this IRC server.
00:15 < crunchman> I tried to help him - I gave up.
00:15  * Aprogas remembers saying that iip 1.1 would be released the day after freenet 0.5
00:15 < crunchman> I asked Lance to help him get on.
00:15 < Aprogas> crunchman: what kind of error does he get ?
00:15 < crunchman> When he's on...  he can give you guys an update in HIS progress.
00:16  * Disposable is listening to Creedence Clearwater Revival - Susie Q
00:16 < crunchman> I don't know - I didnt get chance to ask him - sorry.
00:16 < nemesis> waaaaaaaaaaaaaaaaaaaaaaah *crying*
00:16 < nemesis> mids
00:16 < nemesis> i have 5 iip process running...
00:16 < crunchman> I REALLY would like to go off and re-examine the IIP work I did - so I can answer intellegent questions on the issues I want to bring up.
00:16 < nemesis> fuck it *grrr*
00:16 < crunchman> but I want BOB up here first.
00:17 < crunchman> because he also has to explain HIS part in the project
00:17 < Aprogas> it would be useful if we would know what kind of problem he has with connecting to here
00:17 < crunchman> I think he will address the group on his "socket" problems.
00:17 < Aprogas> is he using his own isproxy or yours?
00:17 < crunchman> Nop is talking to him on the phone right now - i hope.;
00:18 < crunchman> Bob has a Mac...   I think he's using ircle
00:18 < crunchman> this is what I'm using right now.
00:18 < nop> I am
00:18 < nop> athena
00:18  * Kyfhon remembers trying that vile thing in an emulator
00:18 < Disposable> question: primary mac developeman will before os 9 ?
00:18 < nop> he's using athena
00:18 < crunchman> ok,  i'll be right back.
00:18 < nemesis> re....
00:18 < nemesis> are no pid implented in iip yet?
00:18 < nemesis> or cmd line output...
00:19 < nop> crunch, his inet connection is acting up
00:19 < nemesis> i always started a new instance with iip -d  or -h or -? and ?
00:19 < Aprogas> maybe he could come tomorrow, or at next week's meeting then
00:20 < bpb> well, captn crunch made a atleast celebrity appearance today.
00:20 < bpb> err
00:20 < Aprogas> never heard of him, im from the pentium generation
</div>