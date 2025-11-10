---
title: "I2P dev meeting"
date: 2002-11-20
author: "nop"
description: "I2P development meeting covering project updates and technical discussions"
categories: ["meeting"]
---

(Courtesy of the wayback machine http://www.archive.org/)

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> al-jabr, Chocolate, dd0c, Fairwitness, goc, hezekiah, mids, nemesis, Neo, nop, Robert, sanity, sinster, tarpY, tc, zic</p>

## Meeting Log

<div class="irc-log">
--- Log opened Tue Nov 19 23:51:34 2002
23:52 < logger> test
23:52 -!- mode/#iip-dev [+o mids] by Trent
23:52 -!- mode/#iip-dev [+v logger] by mids
23:53 -!- mode/#iip-dev [+oo nop UserX] by mids
23:57 <@mids> public IIP meeting in channel #iip-dev starting in 2.5 minutes
23:57 < nemesis> lol
23:57 < zic> anybody from Ukrain? message me! hehehe
23:58 -!- mode/#iip-dev [+o hezekiah] by mids
23:58 <@hezekiah> Hello again, mids!
23:58 < Robert> Hey Nemesis, have you seen http://www.bash.org/?top
23:58  * athena sees hezekiah in a whole new light :p
23:58 < nemesis> bash?
23:58 <@mids> Robert: they are down
23:58 <@mids> what!
23:58 <@mids> they are back!
--- Day changed Wed Nov 20 2002
00:00 <@mids> Tue Nov 19 23:00:00 UTC 2002
00:00 <@nop> welcome
00:00 <@nop> welcome
00:00 <@nop> to the 20th?
00:00 <@nop> IIP meeting
00:00 <@hezekiah> 20th!
00:00 <@mids> yes
00:00 <@nop> yes on the agenda today...
00:01 <@nop> mids...
00:01 <@mids> 1) welcome
00:02 <@mids> 2) getting rc3 out
00:02 <@mids> 3) sneak preview on rc3
00:02 <@mids> 4) snacks and drinks
00:02 <@mids> 5) questions
00:02 <@mids> .
00:02 <@nop> thnx
00:02 <@nop> ok
00:02 <@nop> so we are having rc3 officially released thursday
00:02 <@nop> please mark that in your calendars
00:02 <@mids> we hope :)
00:02 <@mids> (unless sourceforge is down again)
00:03 <@nop> right, did they fix the ro on nfs?
00:03 <@mids> yes
00:03 <@nop> was it their mistake?
00:03 < tarpY> i am here for the food
00:03 <@mids> it was announced on their status page btw
00:03 <@nop> ok
00:03 <@mids> maintenance
00:03 <@nop> gotcha
00:03 <@nop> probably doing backups
00:03 < tarpY> i wanted to order pizza off of the freenet and i found out they wont
00:03 <@nop> :)
00:03 < tarpY> where can i get food here
00:03 <@mids> tarpY: #muchnies-to-take-away
00:04 <@nop> ok
00:04 <@mids> what will be new in rc3:
00:04 <@nop> so Thursday we will get that out
00:04 <@nop> oh
00:04 <@nop> Mids, I believe you have the changelog handy
00:04 <@nop> if not
00:04 <@mids> me too
00:04 <@nop> I'll display
00:04 <@nop> ok
00:04 < sinster> will rc3 have a decent install script for *nix?
00:04 <@mids> - Display of version number for windows (menu option) and unix (command line).
00:04 <@mids> - Random number generation fix.
00:04 <@mids> - IIP network connections are no longer paused while in the setup screen.
00:04 <@mids> - Now exits if it can't bind to a socket at startup.
00:04 <@mids>   Windows now displays a message box informing that it can't bind to port.
00:04 <@mids> - Several bugfixes and one memory leak fixed.
00:04 <@mids> .
00:04 <@mids> sinster: no, that is what hezekiah is working on
00:05 <@mids> that will be 1.2
00:05 <@hezekiah> Not quite ...
00:05 <@nop> ok
00:05 < zic> are there plans for translating the (nice) faq @ help.invisiblenet.net ?
00:05 <@nop> anyone who wants to translate
00:05 <@nop> please do
00:05 < sinster> mids/hezekiah: will it add iip to /etc/rc.d/ so that it starts automatically?  just a suggestion
00:05 <@nop> we would very much appreciate it
00:05 <@nop> and have it on the site
00:05 < zic> will rc3 demand any mod in the FAQ?
00:06 <@mids> sinster: I got a script here... but that needs more testing
00:06 <@mids> sinster: maybe we'll add that with 1.1 final
00:06 <@hezekiah> sinster: that would not be distribution compatible, since different distros put startup stuff in different places.
00:06 <@mids> zic: no
00:06 < sinster> mids: yeah, make sure you test it on the major linux flavors, redhat, debian etc
00:06 <@nop> well, can we wait on quesitons
00:06 <@nop> please
00:06 < zic> my isproxy is scripted in /etc/init.d (debian), works perfectly
00:06 <@mids> oops
00:06 <@nop> till the questions and answers
00:06 < zic> sorry!
00:06 < zic> sorry!
00:06 <@hezekiah> Sorry.
00:06 <@nop> it gets confusing
00:06 <@nop> ;)
00:06 <@nop> sorry
00:06 < sinster> nop: ok
00:06 < tarpY> no translating everyone should speak english.
00:07 < sinster> nop: my bad
00:07 <@nop> no prob
00:07 <@mids> any questions on the changelog?
00:07 <@mids> no?
00:07 <@mids> nop: sneak preview?
00:07 <@nop> hold my relay just bit the dust
00:08 <@nop> wait till everyone comes back
00:08 <@mids> auch
00:08 <@nop> delay can be annoying in a meeting
00:08 <@nop> ;)
00:08 <@nop> everyone still here?
00:08 <@mids> seems like it
00:09 <@hezekiah> I didn't see anyone leave.
00:09 <@nop> ok
00:09 < zic> i am (does i matter? hehe)
00:09 <@nop> well there is a delay feature we have
00:09 <@nop> ;)
00:09 <@nop> ok
00:09 < al-jabr> I didn't either.
00:09 <@nop> guess my relay got kicked off the list for unreliability
00:09 <@nop> haha
00:09 <@mids> hehe
00:09  * Robert joins #muchnies-to-take-away while he waits...
00:09 <@mids> there we go
00:09 <@nop> yep
00:10 <@nop> there's another
00:10 <@nop> ;)
00:10 < al-jabr> there goes five.
00:10 <@hezekiah> We really need to do something about that. :(
00:10 < nemesis> erm
00:10 < nemesis> mids
00:10 <@nop> hezekiah: spread spectrum routing
00:11 < tc> is this glitches in the relay system?
00:11 <@nop> ;)
00:11 <@nop> my windows relay box crashed
00:11 <@nop> typical
00:11 < nemesis> for win2k / xp, thers in the future a build without gui
00:11 <@hezekiah> lol
00:11 < nemesis> or only gui to setup
00:11 < nemesis> and the rest as an daemon?
00:11 <@nop> it would be nice to have it as a service
00:11 <@nop> ;)
00:12 < nemesis> yes
00:12 < nemesis> ;)
00:12 <@nop> there is a program out there called service installer
00:13 <@nop> ok
00:13 <@nop> well
00:13 < nemesis> iip.exe --install
00:13 <@nop> no more delays
00:13 < nemesis> like apache for win
00:13 <@mids> is everybody already back?
00:14 <@nop> ok
00:15 <@nop> welcome baci
00:15 <@nop> back
00:15 < nemesis> matrix's neo? ;)
00:15 <@nop> ok
00:15 <@nop> I think they are back
00:16 <@mids> yes
00:16 <@nop> ok
00:16 <@nop> sneak preview
00:16 <@mids> I made a FLT-iip.1.1-rc3-pre1-mids-sneak-preview-screaner.tgz
00:16 <@mids> everybody with unix can test it
00:16 <@mids> no windows version yet
00:16 <@nop> I can make one right now
00:16 <@nop> if you want
00:16 < zic> lol
00:16 <@mids> http://mids.student.utwente.nl/~mids/iip/iip-1.1-rc3-mids1.tgz
00:16 < nemesis> thats ok
00:16 < nemesis> i wait
00:16 < zic> OGG or LAME audio?
00:17 <@mids> I am especially looking forward to reports on obscure unix versions
00:17 <@mids> like netbsd etc
00:17 < nemesis> i think, its not so important when a unix machine crash with 30 days uptime
00:17 <@mids> and macosx
00:17 < nemesis> as an windows machine with 3 days uptime ;)
00:17 < tc> mids:  is this change just in the isproxy or in any other relay stuff also?
00:17 <@nop> no
00:17 <@nop> you keep your settings
00:17 <@nop> did we test that it can install over the previous one
00:17 <@nop> hmm
00:18 <@nop> make a note
00:18 < zic> nemesis: but it would be cool if it never crashed. but let's kill the talking here. we are in a formal meeting
00:18 < nemesis> hehe
00:18 <@nop> ok
00:18 <@nop> if anyone wants to test if the upgrade process is trivial
00:18 < nemesis> don't test it on meeting days ;)
00:18 <@nop> then please go ahead
00:18 <@nop> and email or notify one of the devs of the results
00:18 <@mids> please test it next to your current relay
00:18 <@mids> and yes, please give feedback
00:19 <@mids> on what went wrong
00:19 <@mids> etc
00:19 <@nop> wb tarpY
00:19 <@nop> let's put that screener in the topic
00:19 < goc> is it possible to run isproxy-rc2 and isproxy-almost-rc3 simultaneously?
00:19 <@nop> yes
00:20 <@nop> different port settings
00:20 <@nop> and it's not hard at all
00:20 < goc> where's the conf file stored?
00:20 <@nop> but rc3 should be able to go over rc2
00:20 <@nop> you might have to do a -f /dir
00:20 <@nop> or you may have it go over the rc2 install
00:21 < tarpY> are you going to eventually remove the proxy and integrate it into a client?
</div>