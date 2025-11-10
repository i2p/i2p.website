---
title: "I2P Status Notes for 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Weekly I2P status update covering 0.3.4 release performance, new web console development, and various application projects"
categories: ["status"]
---

hi y'all, lets get this status update out of the way

## Index:
1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 status

With last week's 0.3.4 release, the new net is performing pretty well - irc connections are lasting for several hours at a time and eepsite(I2P Site) retrieval seems to be pretty reliable. Throughput is still generally low, though slightly improved (I used to see a consistent 4-5KBps, now I consistently see a 5-8KBps). oOo has posted up a pair of scripts summarizing the irc activity, including round trip message time and connection lifetime (based off hypercubus's bogobot, which was recently committed to CVS)

## 2) On deck for 0.3.4.1

As everyone on 0.3.4 has noticed, I was *cough* a little verbose in my logging, which has been remedied in cvs. In addition, after writing up some tools to stress the ministreaming lib, I've added in a 'choke' so that it won't gobble up truckloads of memory (it will block when trying to add more than 128KB of data into a stream's buffer, so that when sending a large file, your router doesn't get that entire file loaded in memory). I think this will help with the OutOfMemory problems people have been seeing, but I'm going to add some additional monitoring / debugging code to verify this.

## 3) New web console / I2PTunnel controller

In addition to the above modifications for 0.3.4.1, we've got the first pass of the new router console ready for some testing. For a few reasons, we're not going to bundle it as part of the default install quite yet, so there will be instructions on how to get it running when the 0.3.4.1 rev comes out in a few days. As you've seen, I'm really horrible with web design, and as many of you have been saying, I should stop farting around with the app layer and get the core and router rock solid. So, while the new console has much of the good functionality we want (configure the router entirely through some simple web pages, offer a quick and readable summary of the health of the router, expose the ability to create / edit / stop / start different I2PTunnel instances), I really need some help from people who are good with the web side of things.

Technologies used in the new web console are standard JSP, CSS, and simple java beans that query the router / I2PTunnels for data and process requests. They're all bundled into a pair of .war files and deployed into an integrated Jetty webserver (which needs to be started through the router's clientApp.* lines). The main router console JSPs and beans are pretty technically solid, though the new JSPs and beans I built for managing I2PTunnel instances are kind of kludgey.

## 4) 0.4 stuff

Beyond the new web interface, the 0.4 release will include hypercubus' new installer which we haven't really integrated yet. We also need to do some more large scale simulations (especially handling of asymmetric applications like IRC and outproxies). In addition, there are some updates I need to get pushed through to kaffe/classpath so we can get the new web infrastructure going on open source JVMs. Plus I've got to put together some more docs (one on scalability and another analyzing the security/anonymity under a few common scenarios). We also want to have all of the improvements you come up with integrated into the new web console.

Oh, and fix whatever bugs you help find :)

## 5) Other development activities

While there has been a lot of progress being made on the base I2P system, thats only half the story - lots of you are doing some great work on applications and libraries to make I2P useful. I've seen some questions in the scrollback regarding who is working on what, so to help get that info out there, here's everything I know about (if you're working on something not listed and you want to share, if I'm mistaken, or if you want to discuss your progress, please speak up!)

### Active development:
- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:
- swarming file transfer / BT (devs: nickster)

### Paused development:
- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Thats all I can think of for now - swing on by the meeting later tonight to chat 'bout stuff. As always, 9p GMT on #i2p on the usual servers.

=jr