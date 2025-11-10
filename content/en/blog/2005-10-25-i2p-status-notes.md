---
title: "I2P Status Notes for 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Weekly update covering network growth to 400-500 peers, Fortuna PRNG integration, GCJ native compilation support, i2psnark lightweight torrent client, and tunnel bootstrap attack analysis"
categories: ["status"]
---

Hi y'all, more news from the front

* Index
1) Net status
2) Fortuna integration
3) GCJ status
4) i2psnark returns
5) More on bootstrapping
6) Virus investigations
7) ???

* 1) Net status

The past week has been pretty good on the net - things seem fairly stable, throughput normal, and the net continues to grow into the 4-500 peer range. There have been some significant improvements since the 0.6.1.3 release too, and as they affect performance and reliability, I expect we'll have a 0.6.1.4 release later this week.

* 2) Fortuna integration

Thanks to Casey Marshall's quick fix [1], we've been able to integrate GNU-Crypto's Fortuna [2] pseduorandom number generator. This removes the cause of much frustration with the blackdown JVM, and lets us work smoothly with GCJ. Integrating Fortuna into I2P was one of the main reasons smeghead developed "pants" (an 'ant' based 'portage'), so we've now had another successful pants usage :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html
[2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

As mentioned on the list [3], we can now run the router and most clients seamlessly with GCJ [4]. The web console itself still isn't working fully yet, so you need to do your own router configuration with router.config (though it should Just Work and fire up your tunnels after a minute or so). I'm not entirely sure of how GCJ will fit into our release plans, though I'm currently leaning towards distributing pure java but supporting both java & natively compiled versions. Its a bit of a pain to have to build and distribute lots of different builds for different OSes and library versions, etc. Does anyone have any strong feelings on that front?

Another positive feature of GCJ support is the ability to use the streaming lib from C/C++/Python/etc. I don't know if anyone is working on that sort of integration, but it'd probably be worthwhile, so if you're interested on hacking on that front, please let me know!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html
[4] http://gcc.gnu.org/java/

* 4) i2psnark returns

While i2p-bt was the first bittorrent client ported to I2P that got a lot of use, eco was first to the punch with his port of snark [5] a long while back. It unfortunately didn't stay up to date or maintain compatability with the other anonymous bittorrent clients, so it kind of dissapeared for a while. Last week however, I was having some trouble dealing with performance issues somewhere in the i2p-bt<->sam<->streaming lib<->i2cp chain, so I jumped over to mjw's original snark code and did a simple port [6], replacing any java.net.*Socket calls with I2PSocket* calls, InetAddresses with Destinations, and URLs with EepGet calls. The result is a tiny command line bittorrent client (about 60KB compiled) that we will now ship with the I2P release.

Ragnarok has already started hacking into it to improve upon its block selection algorithm, and we'll hopefully get both a web interface and multitorrent capabilities on it in before the 0.6.2 release. If you're interested in helping, get in touch! :)

[5] http://klomp.org/snark/
[6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

The mailing list has been pretty active lately, with Michael's new simulations and analysis of the tunnel construction. The discussion is still going on, with some good ideas from Toad, Tom, and polecat, so check it out if you want to get some input into the tradeoffs for some anonymity related design issues we'll be revamping for the 0.6.2 release [7].

For those interested in some eyecandy, Michael has your fix too, with a simulation of how likely the attack can identify you - as a function of the percentage of the network they control [8], and as a function of how active your tunnel is [9]

(nice work Michael, thanks!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html
    (follow the "i2p tunnel bootstrap attack" thread)
[8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png
[9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

There has been some discussion about some potential malware issues being distributed with a particular I2P enabled application, and Complication has done a great job digging into it. The data is out there, so you can make your own view. [10]

Thanks Complication for all your research into it!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Lots and lots going on, as you can see, but as I'm already late for the meeting, I should probably save this and send it off, 'eh? See you in #i2p :)

=jr