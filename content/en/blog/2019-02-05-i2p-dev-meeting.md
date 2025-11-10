---
title: "I2P Dev Meeting - February 05, 2019"
date: 2019-02-05
author: "zzz"
description: "I2P development meeting log for February 05, 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> echelon, idk, R4SAS, sadie, zlatinb, zzz</p>

## Meeting Log

<div class="irc-log">
20:00:00 &lt;zzz&gt; 0) Hi
20:00:00 &lt;zzz&gt; 1) 0.9.38 release status (zzz)
20:00:00 &lt;zzz&gt; 2) 0.9.39 dev status (zzz)
20:00:00 &lt;zzz&gt; 3) LS2 status (zzz)
20:00:00 &lt;zzz&gt; 4) Status scrum (zlatinb)
20:00:03 &lt;zzz&gt; 0) Hi
20:00:05 &lt;zzz&gt; hi
20:00:11 &lt;zzz&gt; 1) 0.9.38 release status (zzz)
20:00:13 &lt;zlatinb&gt; hi
20:00:21 &lt;sadie_&gt; hi
20:00:26 &lt;zzz&gt; ok, two weeks since we released 38, the network is about half updated
20:00:42 &lt;zzz&gt; we're using it to test LS2 stuff (more about that later)
20:00:51 &lt;eche|offf&gt; hi
20:00:55 &lt;zzz&gt; haven't heard any major complaints or problems
20:01:31 &lt;zzz&gt; we also have the new firefox profile installer and mac installer out there, haven't seen any bugs about those either
20:02:22 &lt;zzz&gt; so all seems to be going smoothly. 38 will be in ubuntu disco and debian buster.
20:02:28 &lt;zzz&gt; anything else on 1) ?
20:02:36 &lt;eche|offf&gt; nope
20:03:16 &lt;zzz&gt; 2) 0.9.39 dev status (zzz)
20:03:46 &lt;zzz&gt; we're 2 weeks into an 8 week cycle, with a release mid-to-late March. We've propped in the un-pluginized i2pcontrol json-rpc2 code
20:04:06 &lt;zzz&gt; lots more changes for LS2 going in
20:04:32 &lt;zzz&gt; fix for HTTP websockets. Lots of bug fixes and performance improvements going in now
20:04:59 &lt;zzz&gt; and some things to make the debian builds work better on disco/buster
20:05:15 &lt;R4SAS&gt; + update in overwriting User-Agent for outproxy?
20:05:26 &lt;zzz&gt; I expect to get any more big changes in by mid-february, then we can work more on bug fixes
20:05:52 &lt;zzz&gt; R4SAS, not familiar with that, have a ticket number for me?
20:07:03 &lt;R4SAS&gt; I read about that few days ago on that channel
20:07:19 &lt;zzz&gt; also, what console changes happen in 38 is not clear, I'm working with the design team to understand what's possible in the time remaining
20:07:41 &lt;eche|offf&gt; in 39
20:07:46 &lt;zzz&gt; R4SAS, drzed asked me to change the clearnet user-agent from 52 to 60 to match current TBB, and I did so
20:07:52 &lt;zzz&gt; yeah, 39, thx eche|offf 
20:08:09 &lt;zzz&gt; anything else on 2) ? anything I'm forgetting?
20:08:55 &lt;zzz&gt; oh, I have some changes in for better outproxy selection, got some initial feedback on it, have to test some more
20:10:00 &lt;zzz&gt; 3) LS2 status
20:10:22 &lt;zzz&gt; it's been a lot of work. we had our 26th weekly meeting yesterday!
20:10:50 &lt;zzz&gt; the portions of proposal 123 that are in 38 are working, but we aren't sure they're working perfectly, more testing is required
20:11:04 &lt;zzz&gt; the specs on the website have been updated to match
20:11:47 &lt;zzz&gt; we also have new proposals 144 and 145 posted, to define the new crypto that's made possible by LS2
20:11:54 &lt;eche|offf&gt; half of year, congrats
20:12:16 &lt;zzz&gt; more of proposal 123 will make its way into 39
20:12:53 &lt;zzz&gt; we're deep into the issues of blinding and encryption in the LS2 meetings, to prevent snooping by the floodfills, and we're getting close
20:13:04 &lt;zzz&gt; not clear if that will make it into 39 or not yet
20:13:39 &lt;zzz&gt; everybody's welcome to join us and sing along, in #ls2 on Mondays at 7:30 PM UTC
20:13:53 &lt;zzz&gt; any questions or other things on 3) ?
20:15:15 &lt;zzz&gt; 4) status scrum (zlatinb)
20:15:19 &lt;zzz&gt; take it away zlatinb 
20:15:32 &lt;zlatinb&gt; Hi.  Lets do the scrum in parallel.  Please describe in few words: 1) what have you been doing since last scrum 2) what you plan to do for the next month 3) any blockers or if you need help.  When youre done, say EOT
20:15:38 &lt;zlatinb&gt; Everyone, go!
20:16:09 &lt;zlatinb&gt; me: 1) work on the firefox profile installer, liasing with monero on i2p-zero, jogger tix
20:16:40 &lt;eche|offf&gt; done the i2p financial stuff, setup new webserver, put it online, working as before, no blockers. currently fiddle with debian buster and java 11 :-/
20:16:52 &lt;zzz&gt; 1) LS2, bugs, 35C3, 38 release, i2pcontrol, debian stuff, performance improvements, bugs, bugs, bugs
20:17:01 &lt;zlatinb&gt; 2) more jogger tix, research into jlink for i2p-zero style installer for us
20:17:05 &lt;zlatinb&gt; 3) not that I can see atm
20:17:18 &lt;zlatinb&gt; EOT
20:18:45 &lt;zzz&gt; 2) LS2, bugs, renew my GPG key, testing, work on 39, maybe an orchid release? I'm sure there's more I'm forgetting
20:18:46 &lt;sadie_&gt; Working with new contacts at NGO's ( usability and user research) , website UX improvements , updating docs, EOT
20:18:51 &lt;zzz&gt; 3) no blockers
20:18:52 &lt;zzz&gt; EOT
20:20:03 &lt;zlatinb&gt; thats it for the scrum I guess
20:20:31 &lt;zzz&gt; 2a) implement a disable NTCP1 option :)
20:21:10 &lt;zzz&gt; ok, I see a few of us didn't show, we will flog them later :)
20:21:19 &lt;eche|offf&gt; hehe
20:21:21 &lt;zzz&gt; anything else for the meeting?
20:21:41 &lt;eche|offf&gt; and I am currently lost in ant, deb-src and strange errors with ascii
20:21:46 &lt;idk&gt; I am here I just got distracted. Plugging away at the browser is all.
20:22:08 &lt;zzz&gt; oh hi idk. take your time for a full 1/2/3 please
20:23:22 &lt;zzz&gt; and I'd like to publicly welcome you to the team!
20:24:49 &lt;zzz&gt; idk, please give us your 1/2/3
20:24:55 &lt;idk&gt; Thanks, I'm glad I have the oppourtunity to help. OK so yesterday I worked through the issues I was having with rbm in building the browser from source. Those seem to have been mostly resolved by meeh. Today I've been working on browser extensions and examining what exactly I can and cannot do with webextensions to harden the browser.
20:25:54 &lt;zzz&gt; ^^ that was 1)
20:25:55 &lt;zlatinb&gt; (2 is what you plan to do next month, 3 is if you have any blockers)
20:27:17 &lt;idk&gt; My bad. Next month I plan to work on implementing some form of tor-like isolation for i2p browser connections on a session-to-session basis, if I don't get to it sooner. I don't anticipate any blockers of a substantial nature, just that webextensions are limited.
20:28:00 &lt;zzz&gt; super, thanks
20:28:21 &lt;zzz&gt; ok, that's it for 4), unless meeh is around
20:28:28 &lt;zzz&gt; anything else for the meeting?
20:28:33 &lt;eche|offf&gt; btw, as long as build issues on buster/jdk11 not resolved, I cannot build any tests more
20:29:09 &lt;eche|offf&gt; (which is not a big issue)
20:29:24 &lt;zzz&gt; that's ticket #2410, right?
20:29:30 &lt;eche|offf&gt; yeah
20:29:36 &lt;eche|offf&gt; got a bit further today^
20:29:41 &lt;zzz&gt; ok, will take a look soon
20:29:52 &lt;zzz&gt; anything else for the meeting?
20:30:04 * zzz warms up the baffer
20:31:05 * zzz *bafs* the meeting closed
</div>
