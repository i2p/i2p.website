---
title: "I2P Status Notes for 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Weekly update covering 0.6.0.3 release improvements, Irc2P network status, susibt web frontend for i2p-bt, and Syndie secure blogging"
categories: ["status"]
---

Hi y'all, time for the weekly status notes again

* Index
1) 0.6.0.3 status
2) IRC status
3) susibt
4) Syndie
5) ???

* 1) 0.6.0.3 status

As mentioned the other day [1], we've got a new 0.6.0.3 release out there, ready for your enjoyment. Its a big improvement from the 0.6.0.2 release (its not uncommon to get several days without disconnect on irc - I've had 5 day uptimes broken by an upgrade), but there are a few things worth noting. Still, its not always like that - people with slow net connections run into troubles, but its progress.

One (very) common question has come up regarding the peer test code-"Why does it say Status: Unknown?" Unknown is *perfectly fine* - it is NOT indicitive of a problem. Also, if you see it sometimes go between "OK" and "ERR-Reject", that DOESN'T mean its ok - if you ever see ERR-Reject, that means its very likely that you've got a NAT or firewall issue. I know its confusing, and there'll be a release later with clearer status display (and automatic resolution, when possible), but for now, don't be suprised if I ignore you when you say "omg its broken!!!11 the status is Unknown!" ;)

(The cause for the excess Unknown status values is because we are ignoring peer tests where "Charlie" [2] is someone we already have an SSU session with, since that implies they'd be able to get through our NAT even if our NAT is broken)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html
[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

As mentioned above, the Irc2P operators have done a great job with their network, as latency is way down and reliability way up - I haven't seen a netsplit in days. There's also a new irc server on there, giving us 3 - irc.postman.i2p, irc.arcturus.i2p, and irc.freshcoffee.i2p. Perhaps one of the Irc2P folks can give us an update on their progress during the meeting?

* 3) susibt

susi23 (of susimail fame) is back with a pair of bt related tools - susibt [3] and a new tracker bot [4]. susibt is a web application (trivially deployable in your i2p jetty instance) for managing i2p-bt's operation. As her site says:

  SusiBT is a web frontend for i2p-bt. It integrates into your i2p
  router and allows for automatic up- and downloads, resumes after
  restart and some management functionality like file up- and
  download. Later versions of the application will support automatic
  build and upload of torrent files.

[3] http://susi.i2p/?page_id=31
[4] http://susi.i2p/?p=33

Can I hear a "w00t"?

* 4) Syndie

As mentioned on the list and in the channel, we've got a new client app for secure and authenticated blogging / content distribution. With Syndie, the "is your eepsite(I2P Site) up" question goes away, as you can read the content even when the site is down, but Syndie avoids all the ugly issues inherent in content distribution networks by focusing on the frontend. Anyway, its very much a work in progress, but if people want to get in and try it out, there's a public Syndie node at http://syndiemedia.i2p/ (also reachable on the web at http://66.111.51.110:8000/). Feel free to go in there and create a blog, or if you're feeling adventurous, blog up some comments/suggestions/concerns! Of course, patches are welcome, but so are feature suggestions, so let 'er rip.

* 5) ???

Saying lots going on is a bit of an understatement... beyond the above, I'm hacking on some improvements to SSU's congestion control (-1 is in cvs already), our bandwidth limiter, and the netDb (for the occational site unreachability), as well as debugging the CPU issue reported on the forum. I'm sure others are hacking on some cool things to report as well, so hopefully they'll swing by the meeting tonight to rant away :)

Anyway, see y'all tonight at 8pm GMT in #i2p on the usual servers!

=jr