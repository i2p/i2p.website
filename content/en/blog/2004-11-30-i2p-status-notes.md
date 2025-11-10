---
title: "I2P Status Notes for 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Weekly I2P status update covering 0.4.2 and 0.4.2.1 releases, mail.i2p developments, i2p-bt progress, and eepsite security discussions"
categories: ["status"]
---

Hi y'all

## Index
1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 and 0.4.2.1

Since we finally pushed out 0.4.2, the network's reliability and throughput shot up for a while, until we ran into the brand new bugs we created. IRC connections for most people are lasting for hours on end, though for some who have run into some of the problems, its been a bumpy ride. There have been a slew of fixes though, and later on tonight or early tomorrow we'll have a new 0.4.2.1 release ready for download.

## 2) mail.i2p

Earlier today I got slipped a note from postman saying he had some things he wanted to discuss - for more info, see the meeting logs (or if you're reading this before the meeting, swing on by).

## 3) i2p-bt

One of the downsides of the new release is that we're running into some trouble with the i2p-bt port. Some of the problems have been identified found and fixed in the streaming lib, but further work is necessary to get it where we need it to be.

## 4) eepsites(I2P Sites)

There has been some discussion over the months on the list, in the channel, and on the forum about some problems with how eepsites(I2P Sites) and the eepproxy work - recently some have mentioned problems with how and what headers are filtered, others have brought up the dangers of poorly configured browsers, and there's also DrWoo's page summarizing many of the risks. One particularly note worthy event is the fact that some people are actively working on applets that will hijack the user's computer if they do not disable applets. (SO DISABLE JAVA AND JAVASCRIPT IN YOUR BROWSER)

This, of course, leads to a discussion of how we can secure things. I've heard suggestions of building our own browser or bundling one with preconfigured secure settings, but lets be realistic - thats a lot more work than anyone here is going to bite into. However, there are three other camps:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

The first is pretty much like we have now, except we filter the content rendered through something like muffin or freenet's anonymity filter. The downside here is that it still exposes HTTP headers so we'd have to anonymize the HTTP side as well.

The second is much like you can see on `http://duck.i2p/` with the CGIproxy, or alternately as you can see in freenet's fproxy. This takes care of the HTTP side as well.

The third has its benefits and drawbacks - it lets us use much more compelling interfaces (as we can safely use some known safe javascript, etc), but has the downside of backwards incompatability. Perhaps a merge of this with a filter, allowing you to embed the macros in filtered html?

Anyway, this is an important development effort and addresses one of the most compelling uses of I2P - safe and anonymous interactive websites. Perhaps someone has some other ideas or info as to how we could get what is needed?

## 5) ???

Ok, I'm running late for the meeting, so I suppose I should sign this and send it on its way, 'eh?

=jr
[lets see if I get gpg to work right...]