---
title: "I2P Status Notes for 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Weekly update covering 0.6.0.6 release success with SSU introductions, I2Phex 0.1.1.27 security update, and colo migration completion"
categories: ["status"]
---

Hi gang, its tuesday again

* Index:
1) 0.6.0.6
2) I2Phex 0.1.1.27
3) migration
4) ???

* 1) 0.6.0.6

With last saturday's 0.6.0.6 release, we've got a bunch of new pieces in play on the live net, and y'all have done a great job upgrading - as of a few hours ago, almost 250 routers have upgraded! The network seems to be doing well too, and introductions have so far been working - you can track your own introduction activity with the http://localhost:7657/oldstats.jsp, looking at the udp.receiveHolePunch and udp.receiveIntroRelayResponse (as well as udp.receiveRelayIntro, for those behind NATs).

btw, the "Status: ERR-Reject" now really isn't an error, so perhaps we should change it to "Status: OK (NAT)"?

There have been a few bug reports with Syndie. Most recently, there is a bug were it will fail to sync up with remote peers if you ask it to download too many entries at once (since I foolishly used HTTP GET instead of POST). I'll be adding support for POST to EepGet, but in the meantime, try pulling just 20 or 30 posts at a time. As an aside, perhaps someone can come up with the javascript for the remote.jsp page to say "fetch all posts from this user", automatically checking all of their blog's checkboxes?

Word on the street is that OSX works fine out of the box now, and with 0.6.0.6-1, x86_64 is operational too on both windows and linux. I haven't heard any reports of problems with the new .exe installers, so either that means its going well or failing completely :)

* 2) I2Phex 0.1.1.27

Prompted by some reports of differences between the source and what was bundled in legion's packaging of 0.1.1.26, as well as concern for the safety of the closed source native launcher, I've gone ahead and added a new launch4j [1] built i2phex.exe to cvs and built the latest from cvs on the i2p file archive [2]. It is unknown whether there are other changes made by legion to his source code prior to his release, or whether the source code he put out is in fact the same as what he built.

For security purposes, I cannot recommend the use of either legion's closed source launcher or the 0.1.1.26 release. The release on the I2P website [2] contains the latest code from cvs, without modification.

You can reproduce the build by first checking out and building the I2P code, then checking out the I2Phex code, then running "ant makeRelease":
  mkdir ~/devi2p ; cd ~/devi2p/
  cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login
# (pw: anoncvs)
  cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p
  cd i2p ; ant build ; cd ..
  cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex
  cd i2phex/build ; ant makeRelease ; cd ../..
  ls -l i2phex/release/i2phex-0.1.1.27.zip

The i2phex.exe inside that zip is usable on windows by simply running it, or on *nix/osx via "java -jar i2phex.exe". It does depend upon I2Phex being installed in a directory next to I2P - (e.g. C:\Program Files\i2phex\ and C:\Program Files\i2p\), as it references some of I2P's jar files.

I'm not stepping in to maintain I2Phex, but I will put future I2Phex releases on the website when there are updates to cvs. If someone wants to work on a webpage that we can put up to describe/introduce it (sirup, you out there?), with links to sirup.i2p, useful forum posts, legion's list of active peers, that'd be great.

[1] http://launch4j.sourceforge.net/
[2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip and
    http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (signed by my key)

* 3) migration

We've switched colo boxes for the i2p services, but everything should now be fully operational on the new machine - if you see something funky, please, let me know!

* 4) ???

There has been a lot of interesting discussion on the i2p list as of late, Adam's neat new smtp proxy/filter, as well as some good posts on syndie (seen gloin's skin on http://gloinsblog.i2p?) I'm working on some changes at the moment for some long standing issues, but those aren't imminent. If anyone has anything else they want to bring up and discuss, swing on by the meeting in #i2p at 8p GMT (in 10 minutes or so).

=jr