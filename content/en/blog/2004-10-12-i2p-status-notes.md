---
title: "I2P Status Notes for 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Weekly I2P status update covering 0.4.1.2 release, dynamic throttling experiments, 0.4.2 streaming library development, and email discussions"
categories: ["status"]
---

Hi gang, time for our weekly update

## Index:
1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

The new 0.4.1.2 release has been out for a few days and things have been going pretty much as expected - there have been a few bumps with the new watchdog component though, causing it to kill your router when things are Bad rather than to restart it. As I mentioned earlier today, I'm looking for people to use the new stats logging tool to send me some data, so your help there would be greatly appreciated.

## 2) 0.4.1.3

There will be another release before 0.4.2 is out, as I want the network to be as solid as possible before moving on. What I'm experimenting with at the moment is a dynamic throttle on the tunnel participation - telling routers to probabalistically reject requests if they're flooded or their tunnels are slower than usual. These probabilities and thresholds are calculated dynamically from the stats being kept - if your 10 minute tunnel test time is greater than your 60 minute tunnel test time, accept the tunnel request with a probability of 60minRate/10minRate (and if your current # of tunnels is greater than your 60 minute average number of tunnels, accept it w/ p=60mRate/curTunnels).

Another potential throttle is to smooth the bandwidth along those lines - rejecting tunnels probabalistically when our bandwidth usage spikes. Anyway, the intent of all of this is to help spread out the network usage and balance the tunnels across more people. The main problem we've had with the load balancing has been an overwhelming *excess* of capacity, and as such none of our "damn we're slow, lets reject" triggers have been hit. These new probabalistic ones should hopefully keep rapid change in check.

I don't have any specific plan for when the 0.4.1.3 release will be out - maybe the weekend. The data people send in (from above) should help determine whether this will be worthwhile, or if there are other avenues more worthwhile.

## 3) 0.4.2

As we discussed in last week's meeting, we've switched around the 0.4.2 and 0.4.3 releases - 0.4.2 will be the new streaming lib, and 0.4.3 will be the tunnel update.

I've been rereviewing the literature for TCP's streaming functionality and there are some interesting topics of concern for I2P. Specifically, our high round trip time leans towards something like XCP, and we should probably be quite aggressive with various forms of explicit congestion notification, though we can't take advantage of something like the timestamp option, since our clocks can be skewed by up to a minute.

In addition, we'll want to make sure we can optimize the streaming lib to handle short lived connections (which vanilla TCP pretty much sucks at) - for instance, I want to be able to be able to send small (<32KB) HTTP GET requests and small (<32KB) replies in literally three messages:
```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```

Anyway, not much code has been cut on this yet, with the protocol side of things looking pretty much TCP-like and the packets somewhat like a merging of human's proposal and the old proposal. If anyone has any suggestions or ideas, or wants to help out with the implementation, please get in touch.

## 4) mail discussion

There have been some interesting discussions regarding email in (and out of) I2P - postman has put a set of ideas online and is looking for suggestions. There have also been related discussions on the #mail.i2p. Perhaps we can get postman to give us an update?

## 5) ???

Thats about it for the moment. Swing on by the meeting in a few minutes and bring your comments :)

=jr