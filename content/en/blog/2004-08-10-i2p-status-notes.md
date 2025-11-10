---
title: "I2P Status Notes for 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Weekly I2P status update covering 0.3.4.1 release performance, outproxy load balancing, and documentation updates"
categories: ["status"]
---

Hey everyone, weekly update time

## Index:
1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 status

Well, we've pushed out the 0.3.4.1 release the other day, and it has been doing pretty well. Connect times on irc have been consistently for multiple hours, and transfer rates are doing pretty good as well (I pulled 25KBps from one eepsite(I2P Site) the other day using 3 parallel streams).

One really cool feature added in with the 0.3.4.1 release (that I forgot to add to the release announcement) was mule's patch to allow the eepproxy to round robin non-i2p requests through a series of outproxies. The default is still just to use the squid.i2p outproxy, but if you go into your router.config and change the clientApp line to have:
```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
it will randomly route each HTTP request through one of the two outproxies listed (squid.i2p and www1.squid.i2p). With that, if there are a few more people running outproxies, y'all won't be so dependent upon the squid.i2p. Of course, you've all heard my concerns regarding outproxies, but having this capability gives people more options.

We have been seeing some instability over the last few hours, but with the help of duck and cervantes, I've identified two nasty bugs and am testing out fixes atm. The fixes are significant, so I do expect to have a 0.3.4.2 out in the next day or two, after I've verified the results.

## 2) Updated docs

We've been slacking a bit on getting the documentation on the site up to date, and while there are still a few big holes (e.g. the netDb and i2ptunnel docs), we've recently updated a few of them (network comparisons and the faq). As we are moving closer to the 0.4 and 1.0 releases, I would appreciate if people could go through the site and see what can be improved upon.

Of particular note is an updated Hall of Fame - we've finally got that sync'ed up to reflect the generous donations y'all have made (thanks!) As we move forward, we will be using these resources to compensate coders and other contributors, as well as to offset any costs incurred (e.g. hosting providers, etc).

## 3) 0.4 progress

Looking back at last week's notes, we've still got a few things left for 0.4, but the simulations have been going quite well, and the majority of the kaffe problems have been found. What would be great though is if people could hammer away at different aspects of the router or the client apps and file any bugs you come across.

## 4) ???

Thats all I've got to bring up at the moment - I appreciate the time y'all are taking to help move us forward, and I think we're making great progress. Of course, if anyone has anything else they want to talk about, swing on by the meeting in #i2p at... er... now :)

=jr