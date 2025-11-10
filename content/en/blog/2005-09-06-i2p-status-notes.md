---
title: "I2P Status Notes for 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Weekly update covering 0.6.0.5 release success, floodfill netDb performance, Syndie progress with RSS and pet names, and new susidns addressbook management application"
categories: ["status"]
---

Hi y'all,

* Index
1) Net status
2) Syndie status
3) susidns
4) ???

* 1) Net status

As many have seen, the 0.6.0.5 release came out last week after a brief 0.6.0.4 rev, and so far, the reliability has been greatly improved, and the net has grown larger than ever. There is still some room for improvement, but it seems that the new netDb is performing as designed. We've even had the fallback tested out - when the floodfill peers are unreachable, routers fall back on the kademlia netDb, and the other day when that scenario occurred, irc and eepsite(I2P Site) reliability was not substantially diminished.

I did receive a question regarding how the new netDb works, and have posted up the answer [1] on my blog [2]. As always, if anyone has any questions on that sort of thing, please feel free to bounce it my way, either on or off list, on the forum, or even on your blog ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true
[2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

As you can see from syndiemedia.i2p (and http://syndiemedia.i2p.net/), there has been a lot of progress lately, including RSS, pet names, administrative controls, and the beginnings of reasonable css usage. Most of Isamoor's suggestions have been deployed as well, as have Adam's, so if anyone has anything in mind they'd like to see in there, please bounce me a note!

Syndie is now fairly close to beta, at which point it'll be shipped as one of the default I2P applications as well as packaged standalone, so any help would be greatly appreciated. With today's latest additions (in cvs), skinning Syndie is a snap too - you can just create a new file syndie_standard.css in your i2p/docs/ directory, and the styles specified will override Syndie's defaults. More info on that can be found on my blog [2].

* 3) susidns

Susi has whipped up yet another web application for us - susidns [3]. This serves as a simple interface for managing the addressbook app - its entries, subscriptions, etc. Its looking pretty good, so hopefully we'll be able to ship it as one of the default apps soon, but for now, its a snap to grab from her eepsite(I2P Site), save it to your webapps directory, restart your router, and you're good to go.

[3] http://susi.i2p/?page_id=13

* 4) ???

While we've certainly been focusing on the client app side of things (and will continue to do so), much of my time is still targetting the core operation of the network, and there's some exciting stuff coming down the pipe - firewall and NAT hopping with introductions, improved SSU autoconfiguration, advanced peer ordering and selection, and even some simple restricted route handling. On the website front, HalfEmpty has made some improvements to our stylesheets (yay!).

Anyway, lots going on, but thats about all I've got time to mention at the moment, but swing on by the meeting at 8p UTC and say hi :)

=jr