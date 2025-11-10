---
title: "I2P Status Notes for 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Weekly I2P status update covering 0.3.4.3 release, new router console features, 0.4 progress, and various improvements"
categories: ["status"]
---

Hi everyone, lots of updates today

## Index
1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 status

The 0.3.4.3 release came out last Friday and things have been going pretty well since. There have been some problems with some newly introduced tunnel testing and peer selection code, but after some tweaking since the release, its pretty solid. I don't know if the irc server is on the new rev yet, so we generally have to rely on testing with eepsites(I2P Sites) and the http outproxies (squid.i2p and www1.squid.i2p). Large (>5MB) file transfers in the 0.3.4.3 release are still not reliable enough, but in my testing, the modifications since then have improved things further.

The network has been growing as well - we hit 45 concurrent users earlier today, and have been consistently in the 38-44 user range for a few days (w00t)! This is a healthy number for the moment, and I've been monitoring the overall network activity to watch for dangers. When moving to the 0.4 release, we're going to want to gradually increase the userbase up to around the 100 router mark and test some more before growing further. At least, thats my goal from a developer's perspective.

### 1.1) timestamper

One of the totally kickass things that changed with the 0.3.4.3 release that I completely forgot to mention was an update to the SNTP code. Thanks to the generosity of Adam Buckley, who has agreed to release his SNTP code under the BSD license, we have merged the old Timestamper app into the core I2P SDK and integrated it fully with our clock. This means three things:
1. you can delete the timestamper.jar (the code is in i2p.jar now)
2. you can remove the related clientApp lines from your config
3. you can update your config to use the new time sync options

The new options in the router.config are simple, and the default values should be good enough (especially true since the majority of you are unintentially using them :)

To set the list of SNTP servers to query:
```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```

To disable the time synchronization (only if you are an NTP guru and know that your OS's clock is *always* right - running "windows time" is NOT sufficient):
```
time.disabled=true
```

You don't need to have a 'timestamper password' anymore, since it is all integrated into the code directly (ah, the joys of BSD vs GPL :)

### 1.2) new router console authentication

This is only relevent for those of you running the new router console, but if you have it listening on a public interface, you may want to take advantage of the integrated basic HTTP authentication. Yes, basic HTTP authentication is absurdly weak - it won't protect against anyone who sniffs your network or brute forces their way in, but it'll keep out the casual sneak. Anyway, to use it, simply add the line

```
consolePassword=blah
```

to your router.config. You will, unfortunately, have to restart the router, as this parameter is fed into Jetty only once (during startup).

## 2) 0.4 status

We're making a lot of headway on the 0.4 release, and we hope to get some prerelease versions out there in the next week. We're still hammering out some details though, so we don't have a solid upgrade process put together yet. The release will be backwards compatible, so it shouldn't be too painful of an update. Anyway, keep an ear to the ground and you'll know when things are ready.

### 2.1) service & systray integration

Hypercubus is making lots of progress on integrating the installer, a systray application, and some service management code. Basically, for the 0.4 release all windows users will automatically have a small systray icon (Iggy!), though they will be able to disable (and/or reenable) that through the web console. In addition, we're going to be bundling the JavaService wrapper, which will let us do all sorts of cool things, such as run I2P on system boot (or not), auto-restart on some conditions, hard JVM restart on demand, generate stack traces, and all sorts of other goodies.

### 2.2) jbigi & jcpuid

One of the big updates in the 0.4 release will be an overhaul of the jbigi code, merging in the modifications Iakin made for Freenet as well as Iakin's new "jcpuid" native library. The jcpuid library works only on x86 architectures and, in tandem with some new jbigi code, will determine the 'right' jbigi to load. As such, we will be shipping a single jbigi.jar that everyone will have, and from it select the 'right' one for the current machine. People will of course still be able to build their own native jbigi, overriding what jcpuid wants (simply build it and copy it into your I2P installation directory, or name it "jbigi" and place it in a .jar file in your classpath). However, because of the updates, it is *not* backwards compatible - when upgrading, you must either rebuild your own jbigi or remove your existing native library (to let the new jcpuid code choose the right one).

### 2.3) i2paddresshelper

oOo has put together a really cool helper to let people browse eepsites(I2P Sites) without updating their hosts.txt. It is committed to CVS and will be deployed in the next release, but people may want to consider updating links accordingly (cervantes has updated forum.i2p's [i2p] bbcode to support it with a "Try it [i2p]" link).

Basically you just make a link to the eepsite(I2P Site) with whatever name you want, then tack on a special url parameter specifying the destination:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```

Behind the scenes, its pretty safe - you can't spoof some other address, and the name is *not* persisted in hosts.txt, but it will let you see images / etc linked to on eepsites(I2P Sites) that you wouldn't be able to with the old `http://i2p/base64/` trick. If you want to always be able to use "wowthisiscool.i2p" to reach that site, you will still of course have to add the entry to your hosts.txt (until the MyI2P address book is pushed out, that is ;)

## 3) AMOC vs. restricted routes

Mule has been throwing together some ideas and prodding me to explain some things, and in the process, he has been making some headway in getting me to reevaluate the whole AMOC idea. Specifically, if we drop one of the constraints I've placed on our transport layer - allowing us to assume bidirectionality - we may be able to scrap the whole AMOC transport, instead implementing some basic restricted route operation (leaving the foundations for more advanced restricted route techniques, like trusted peers and multihop router tunnels for later).

If we go this route, it would mean people would be able to participate in the network behind firewalls, NATs, etc with no configuration, as well as offer some of the restricted route anonymity properties. In turn, it would likely cause a big revamp to our roadmap, but if we can do it safely, it would save us a truckload of time and be well worth the change.

However, we don't want to rush it, and will need to review the anonymity and security implications carefully before committing to that path. We'll do so after 0.4 is out and going smoothly, so there is no rush.

## 4) stasher

Word on the street is that aum is making some good progress - I don't know if he'll be around for the meeting with an update, but he did leave us a snippet on #i2p this morning:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```

w00t.

## 5) pages of note

I just want to point out two new resources available that I2P users may want to check out - DrWoo has put together a page with a whole bunch of info for people who want to browse anonymously, and Luckypunk has posted up a howto describing his experiences with some JVMs on FreeBSD. Hypercubus also posted the docs on testing out the not-yet-released service & systray integration.

## 6) ???

Ok, thats all I've got to say at the moment - swing by the meeting tonight at 9p GMT if you'd like to bring something else up.

=jr