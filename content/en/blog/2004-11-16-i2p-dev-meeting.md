---
title: "I2P Dev Meeting - November 16, 2004"
date: 2004-11-16
author: "jrandom"
description: "I2P development meeting log for November 16, 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, dinoman, DrWoo, duck, jrandom, postman, Ragnarok, susi23, wiht</p>

## Meeting Log

<div class="irc-log">
13:05 &lt;jrandom&gt; 0) hi
13:05 &lt;jrandom&gt; 1) Congestion
13:05 &lt;jrandom&gt; 2) Streaming
13:05 &lt;+dinoman&gt; pgforge's key has changed :/ sorry
13:05 &lt;jrandom&gt; 3) BT
13:05 &lt;jrandom&gt; 4) ???
13:05 &lt;jrandom&gt; ah cool, we can do some magic for that
13:05 &lt;jrandom&gt; 0) hi
13:05  * jrandom waves
13:05 &lt;ant&gt; &lt;lucky&gt; hi
13:05 &lt;jrandom&gt; weekly status notes up @ http://dev.i2p.net/pipermail/i2p/2004-November/000489.html
13:05 &lt;wiht&gt; Hello.
13:06 &lt;jrandom&gt; (and we got the notes posted *before* the meeting.  w00t)
13:06 &lt;jrandom&gt; might as well jump on in to 1) Congestion
13:07 &lt;jrandom&gt; for people who have been hanging around the channel the last few days, you've heard lots of discussions about wtf has been going on, and both this email and duck's post earlier should cover it generally
13:07 &lt;jrandom&gt; that said, does anyone have any questions / comments / concerns that they'd like to raise/discuss?
13:09 &lt;wiht&gt; What do you mean by "wild peer selection"?
13:10 &lt;jrandom&gt; the way our current tunnel building works unfortunately lets things stabalize around the fast peers
13:10 &lt;jrandom&gt; if those fast peers don't fail occationally, we simply use them, period, rather than explore beyond them in our tunnel building
13:11 &lt;jrandom&gt; that means that when they *do* fail later on, we have pretty much no idea how much capacity the rest of the network has, and as such, choose peers fairly arbitrarily
13:11 &lt;+DrWoo&gt; jrandom: what is in the pipeline to use the capacity better?
13:12 &lt;jrandom&gt; DrWoo: the 0.4.3 release will include a new way of pooling tunnels so that we can have more 'experimental' backup tunnels (allowing us to learn more about the network without sacrificing performance)
13:13 &lt;jrandom&gt; more aggressive load balancing through ATM-style reservations are also in the pipeline, but aren't plotted at a particular release yet (aka we'll do it when we need it)
13:14 &lt;ant&gt; &lt;Connelly&gt; bleh
13:14 &lt;ant&gt; &lt;Connelly&gt; no meeting yet?
13:14 &lt;jrandom&gt; (ATM-style reservations, as in, keep track of how much bandwidth tunnels use, on average, multiply that by the number of tunnels we participate in, and compare that to our bandwidth limits / capacity, using that comparison to accept / reject further tunnel requests)
13:15 &lt;jrandom&gt; Connelly: started 10m ago, status notes posted on the list ;)
13:15 &lt;+DrWoo&gt; jrandom: what impact will that have on performance?
13:15 &lt;+DrWoo&gt; local pc performance
13:15  * wiht wonders how many different protocols are being used on the I2P network besides HTTP, IRC, and BT.
13:16 &lt;jrandom&gt; DrWoo: the 0.4.3 pooling will give us greater resiliance (less failures), and the reservations will allow for more capacity-based load sharing (aka reduce contention)
13:16 &lt;jrandom&gt; neither of those are particularly latency based though
13:17 &lt;jrandom&gt; wiht: those three are the main ones used to my knowledge, though some ugly stuff is done over HTTP
13:17 &lt;jrandom&gt; thats actually an interesting issue, wrt irc and congestion
13:18 &lt;jrandom&gt; what was really killing irc.duck.i2p the other day was the fact that during congestion, duck's irc server still had to pump out 20x the number of messages it received
13:19 &lt;jrandom&gt; add on the automatic message resending every.10.seconds.with.no.backoff, and that grows to 120 messages for every line of text ;)
13:19 &lt;jrandom&gt; basically what i'm saying is, a decentralized chat protocol would be Good ;)
13:19 &lt;+DrWoo&gt; is there such a beast?
13:20 &lt;jrandom&gt; (though the new streaming lib will get rid of that 6x overhead)
13:20 &lt;+dinoman&gt; is there a good one
13:20 &lt;jrandom&gt; i dont know if anyone has evaluated something ala SILC for i2p within the last year
13:20 &lt;susi23&gt; pop3 and smtp are _awfully_ slow on i2p
13:21 &lt;ant&gt; &lt;duck&gt; silc == irc+somecrypto
13:21 &lt;susi23&gt; (as answer on the question, which protocols are used too)
13:21 &lt;jrandom&gt; ah, i thought silc got away from the ircd concept
13:21 &lt;jrandom&gt; oh, shit, right, i forgot about those two :)
13:21 &lt;wiht&gt; susi23: Yes, I forgot that we have mail on I2P now.
13:21 &lt;ant&gt; &lt;duck&gt; not far atleast
13:21 &lt;jrandom&gt; 'k
13:21 &lt;ant&gt; &lt;protok0l&gt; meeting?
13:22 &lt;ant&gt; &lt;lucky&gt; rite now protok0l 
13:22 &lt;ant&gt; &lt;protok0l&gt; k
13:22 &lt;jrandom&gt; ok, do we have anything else for 1) congestion?
13:23 &lt;jrandom&gt; if not, moving on to 2) streaming
13:23 &lt;jrandom&gt; [see the email]
13:24 &lt;jrandom&gt; i've kept all the streaming lib updates out of the history.txt, but you can watch whats going on via the cvs list
13:24 &lt;jrandom&gt; (if you're crazy)
13:24 &lt;jrandom&gt; i dont really have anythign else to add though.  so, any questions/comments/concerns?  
13:25 &lt;+postman&gt; just one
13:25 &lt;+postman&gt; thanks :)
13:25 &lt;ant&gt; &lt;protok0l&gt; what speed increase will there be
13:25 &lt;jrandom&gt; hehe you're supposed to wait until you *get* the software postman ;)
13:25 &lt;jrandom&gt; protokol: some.  varies.  
13:25 &lt;+postman&gt; jrandom: i would bet on you blindfold
13:26 &lt;+DrWoo&gt; jrandom: I'm going to ask you what you hate, is there an ETA on the new streaming lib, the current situation obviously is a point of vulnerability?
13:27 &lt;jrandom&gt; if tests this week go well, we can pencil in next week
13:27 &lt;jrandom&gt; there'll be services up and running on the new streaming lib before then though, so that we can test it under load conditions
13:28 &lt;wiht&gt; As I recall, you are using a simulated network for the tests. Is that still true?
13:29 &lt;jrandom&gt; for some of them, yeah
13:29 &lt;jrandom&gt; when i dont use the sim, i just run it on the live net
13:30 &lt;jrandom&gt; (because i like to abuse your bandwdith ;)
13:30 &lt;susi23&gt; you're welcome ;)
13:30 &lt;+dinoman&gt; hehe turn it on a see if it blows up?
13:31 -!- x is now known as fidd
13:31 &lt;jrandom&gt; pretty much - i've got some logging code that essentially dumps the streaming packet headers, allowing me to make sure everything is sent properly and various situations are handled as they should be
13:32 &lt;jrandom&gt; the sim'ed tests are more involved though, with perhaps a half dozen unit tests w/ various runtime params
13:33 &lt;wiht&gt; How well do the simulation tests reflect observed network usage?
13:33 &lt;jrandom&gt; pretty well, as the simulation code is the same as the live network code
13:34 &lt;jrandom&gt; i dont have the lag and drop injection perfect in the sim though, but its in the ballpark
13:35 &lt;ant&gt; &lt;cat-a-puss&gt; will the new streaming lib use the same interface? Or will Java apps have to do something new?
13:35 &lt;wiht&gt; Thanks for clarifying that.
13:36 &lt;jrandom&gt; cat-a-puss: same interface.  there are a few additional config options that you might want to tack on when building an I2PSocketManager, but thats a good ol' properties map
13:36 &lt;ant&gt; &lt;cat-a-puss&gt; k
13:37 &lt;jrandom&gt; k, anything else, or shall we jump to 3) BT?
13:38 &lt;jrandom&gt; duck: ping
13:38 &lt;@duck&gt; *quack
13:38 &lt;@duck&gt; Last week I reported that we had BitTorrent on I2P working. There has been some 
13:38 &lt;@duck&gt; confusion but it is anonymous both for trackers and for clients (seeders and leechers).
13:38 &lt;@duck&gt; Updates since last week:
13:38 &lt;@duck&gt; GUI work (wxPython), included tracker, bugfixes.
13:39 &lt;@duck&gt; full list at http://dev.i2p/cgi-bin/cvsweb.cgi/~checkout~/i2p-bt/CHANGES.txt?rev=HEAD
13:39 &lt;@duck&gt; also the code is at the CVS on cvs.i2p
13:39 &lt;@duck&gt; and got a dedicated eepsite: http://duck.i2p/i2p-bt/
13:39 &lt;@duck&gt; The included tracker is very spartanic and you still have to provide the
13:39 &lt;@duck&gt; torrents themself somewhere; so DrWoo, thetower and me have been looking at 
13:39 &lt;@duck&gt; several alternatives which offer features like suprnova, until I got nuts.
13:39 &lt;@duck&gt; *flierp*
13:40 &lt;jrandom&gt; w00t
13:40 &lt;@duck&gt; Finally bytemonsoon is selected, the original is ugly, but DrWoo has been fixing that,
13:40 &lt;@duck&gt; The idea is to improve it some more and release it as an I2P ready tracker solution,
13:40 &lt;@duck&gt; see: http://brittanyworld.i2p/bittorrent/
13:40 &lt;@duck&gt; meeting the requirements at: http://duck.i2p/i2p-bt/txt/bytemonsoon.txt
13:40 &lt;@duck&gt; .
13:40 &lt;jrandom&gt; kickass
13:40 &lt;+DrWoo&gt; you can check out a couple of small test files on a the nice tracker duck fixed up
13:41 &lt;+DrWoo&gt; there's nothing big to gum up the net heh
13:41 &lt;jrandom&gt; what, you dont want us to download more episodes of Lost?  :)
13:41 &lt;@duck&gt; if thetower's is up..
13:42 &lt;jrandom&gt; the bytemonsoon port is looking really nice.
13:42 &lt;+DrWoo&gt; I can't get thetower right now here
13:42 &lt;+DrWoo&gt; jrandom: it really seems to provide most anything you'd need
13:42 &lt;+dinoman&gt; what kind of speed r ppl seeing?
13:43 &lt;@duck&gt; ~5kb/s per peer
13:43 &lt;+DrWoo&gt; dino: from this side it looks like 4-10K per peer
13:43 &lt;@duck&gt; (optimistically, ofcourse there are those shitty adsl folks)
13:44 &lt;+dinoman&gt; wow better then i thought
13:44 &lt;@duck&gt; til i2p crashes; see 1)
13:44 &lt;jrandom&gt; heh
13:44 &lt;+DrWoo&gt; dinoman: in other works, it should look pretty impressive with a swarm
13:44 &lt;@duck&gt; there have been various calls for improving the GUI
13:45 &lt;+DrWoo&gt; dinoman: and some 0 hop peers ;)
13:45 &lt;@duck&gt; not many takers on it though
13:45 &lt;jrandom&gt; duck (& gang): what can we do to help?
13:45 &lt;@duck&gt; you: get the new streaming lib ready
13:46 &lt;@duck&gt; gang: look at the todo: http://duck.i2p/i2p-bt/txt/todo.txt
13:46 &lt;@duck&gt; lucky is working on a howto
13:47 &lt;@duck&gt; DrWoo: anything else?
13:47 &lt;jrandom&gt; nice
13:47 &lt;+DrWoo&gt; jrandom: can you talk a bit about where you stand regarding the importance (or not) of file sharing(and other popular services currently run over the internet) and what it's means to to I2P's anonymity prospects.
13:47 &lt;ant&gt; &lt;lucky&gt; i am?
13:48 &lt;ant&gt; &lt;lucky&gt; oh
13:48 &lt;ant&gt; &lt;lucky&gt; i am
13:48 &lt;ant&gt; &lt;lucky&gt; :)
13:48 &lt;+DrWoo&gt; duck: there's always something else heh
13:48 &lt;jrandom&gt; file sharing is critical to I2P's success, as its realistically the largest potential pool of users to blend into our anonymity set
13:49 &lt;ant&gt; &lt;lucky&gt; uh oh.
13:49 &lt;ant&gt; &lt;lucky&gt; So that means i should really, really, work on that howto then.
13:49 &lt;jrandom&gt; without a viable large-file-transfer system, we've got to do some wonders for engaging user apps
13:50 &lt;jrandom&gt; which we are doing - susi's and postman's work is quite promising
13:50 &lt;jrandom&gt; but the market for anonymous email is much less than the market for safe file transfer
13:51 &lt;jrandom&gt; while I2P itself scales to whatever size (if things are as we hope ;), we need a large anonymity set to support anything wortwhile 
13:51 &lt;jrandom&gt; &lt;/my $0.02&gt;
13:52 &lt;@duck&gt; what do you think about default settings for those filesharing apps?
13:52 &lt;jrandom&gt; that i dont know
13:53 &lt;@duck&gt; or isn't that really relevant yet giving todays possibilities
13:54 &lt;+DrWoo&gt; duck: there may be some 'thinking outside the box' needed to get over some bumps along the way?
13:54 &lt;jrandom&gt; 1 hop tunnels may be relevent for the BT-ers, prior to 0.4.3
13:57 &lt;jrandom&gt; ok, do we have anything else for 3) BT?
13:57 &lt;@duck&gt; notme
13:57 &lt;+DrWoo&gt; thanks to duck and the dudes
13:58 &lt;+DrWoo&gt; that was pretty awesome work
13:58 &lt;jrandom&gt; aye, y'all are doing a kickass job
13:58 &lt;+dinoman&gt; i did not do it
13:58 &lt;jrandom&gt; (i love watching the --spew 1 on the btdownloadheadless :)
13:58 &lt;@duck&gt; dinoman: you started it
13:58 &lt;+Ragnarok&gt; headless spew... sounds dirty
13:59 &lt;+DrWoo&gt; dino: pushing the effort along is a real contribution
13:59  * Ragnarok will put together a patch for the command line option stuff on the todo list
13:59 &lt;jrandom&gt; w00t
14:00 &lt;ant&gt; &lt;dm&gt; Don't forget anonymous WWW, that's a big one as well.
14:00 &lt;jrandom&gt; dm: yeah, perhaps thousands or tens of thousands, but not the draw of millions
14:01 &lt;jrandom&gt; (for outproxy stuff, imho)
14:01 &lt;jrandom&gt; ok, if there's nothing else, moving on to good ol' fashioned 4) ???
14:01 &lt;jrandom&gt; anything not yet raised that should be?
14:02 &lt;wiht&gt; postman: What is the status of the mail system? How well is it working, especially with respect to communications outside the I2P network?
14:02 &lt;+DrWoo&gt; dm: it's all part of life's rich pageant :)
14:03 &lt;ant&gt; &lt;dm&gt; a lotta people use da web
14:03 &lt;ant&gt; &lt;dm&gt; (they just installed surfcontrol at my workplace) ;)
14:03 &lt;jrandom&gt; aye, anonymous www hosting will be critical for those who really need i2p, though they probably won't be the anonymity set necessary 
14:03 &lt;jrandom&gt; ah, lame
14:04 &lt;jrandom&gt; wiht: if he's not around, i can say that in and outproxy has worked pretty well for me - none lost yet
14:04 &lt;jrandom&gt; (and checking my mail takes a few seconds, but biff tells me when i need to anyway)
14:05 &lt;jrandom&gt; ok, is there anything else?
14:06 &lt;ant&gt; &lt;dm&gt; are you baffing the meeting?
14:07 &lt;jrandom&gt; seems like it
14:07  * jrandom winds up
14:07  * jrandom *baf*s the meeting closed
</div>
