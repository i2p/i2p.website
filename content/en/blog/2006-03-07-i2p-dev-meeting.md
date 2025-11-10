---
title: "I2P Dev Meeting - March 07, 2006"
date: 2006-03-07
author: "jrandom"
description: "I2P development meeting log for March 07, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, Complication, dust, jrandom, susi23</p>

## Meeting Log

<div class="irc-log">
15:08 &lt;jrandom&gt; 0) hi
15:08 &lt;jrandom&gt; 1) Net status
15:08 &lt;jrandom&gt; 2) ???
15:08 &lt;jrandom&gt; 0) hi
15:08  * jrandom waves
15:08 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-March/001267.html
15:09  * jrandom gives y'all hours to read through that huge tome of notes
15:10  * Complication pretends not having noticed yet ;)
15:11 &lt;+Complication&gt; Hi :)
15:11 &lt;+susi23&gt; hi :)
15:12 &lt;jrandom&gt; well, might as well dig on in to 1) net status
15:12 &lt;jrandom&gt; The mail gives my general view of whats going on.  how does that line up with what y'all are seeing?
15:13 &lt;+Complication&gt; Throttling fixes seem to have increased reliability, but really suppressed bandwidth
15:13 &lt;+Complication&gt; Just a second, digging for the graph
15:14 &lt;+Complication&gt; http://complication.i2p/files/bw-week.png
15:14 &lt;+Complication&gt; High stretches are on non-latest, low stretches on latest
15:15 &lt;+Complication&gt; Same limiter settings, possibly more lax on stricter (latest) versions
15:16 &lt;+Complication&gt; But it's not much of a problem, since it does transfer
15:16 &lt;jrandom&gt; cool, reduced bandwidth usage is appropriate as you approach your actual bandwidth limit
15:17 &lt;+Complication&gt; Most of time, it seems to bounce back before the "sustained bandwidth" limit
15:17 &lt;+Complication&gt; Never touches the burst limit
15:18 &lt;+Complication&gt; (which, in itself, is sensible - it's the bouncing back before the sustained limit which concerns me)
15:19 &lt;bar&gt; i'm seeing pretty much what Complication is seeing. my total bw consumption is just 50% of my max settings. it used to be ~80% pre 0.6.1.11
15:19 &lt;jrandom&gt; is 200kbps your limiter rate, w/ 300kbps burst?
15:20 &lt;jrandom&gt; (just wondering how much time it used to spend in the burst)
15:20 &lt;jrandom&gt; reduced bandwidth usage though is one of the aims of the recent changes
15:21 &lt;+Complication&gt; ~225 sustained, ~325 burst
15:21 &lt;+Complication&gt; Hey, I could have...
15:22 &lt;+Complication&gt; Have I *interpreted* it wrong?
15:23 &lt;+Complication&gt; Forget it, I'm a fool... did the math wrong, it's not nearly as bad :O
15:23 &lt;jrandom&gt; insufficient data :)  it might be indicitive of a problem, but what you've described so far suggests things are behaving as desired
15:23 &lt;+Complication&gt; It's a bit on the conservative side, but not nearly as bad as I thought
15:24 &lt;+Complication&gt; According the Router Console (which measures in the same unit as the limiter) outbound total average is 2/3 of the sustained limit, and 1/2 of the burst limit
15:25 &lt;+Complication&gt; But inbound total average, I have to say, is only slightly above 1/3 sustained limit, and 1/4 burst limit
15:26 &lt;+Complication&gt; for example, assuming a sustained limit of 30, and a burst limit of 40, outbound would be 20 and inbound just above 10 (mostly due to lack of load)
15:26 &lt;jrandom&gt; cool
15:26 &lt;+Complication&gt; But the graph I misinterpreted, due to Kb/KB issues :O
15:27  * Complication wipes the graph from history
15:28 &lt;jrandom&gt; good eye though, definitely lemmie know when things sound funky
15:28 &lt;jrandom&gt; ok, anything else on 1) Net status?
15:28 &lt;jrandom&gt; if not, lets shimmy on over to 2) ???
15:28 &lt;jrandom&gt; anyone have anything else to discuss?
15:30 &lt;+Complication&gt; Well, there's been some jbigi testing, and apparently, someone got results which suggested the 64-bit version for Linux being slowish
15:31 &lt;+Complication&gt; They had it slower than pure Java, not sure if a measurement glitch or not :O
15:32 &lt;+Complication&gt; I couldn't repeat it
15:32 &lt;jrandom&gt; yeah, i wasn't sure exactly what .so they were using for the platform
15:32 &lt;+Complication&gt; Over here, it was about twice faster than pure Java
15:32 &lt;+dust&gt; my experiments with html as an additional message format in syndie is starting to work. my local 'sucker' can now retrieve web pages (with images) and store them as syndie posts
15:33 &lt;jrandom&gt; ah wikked dust 
15:33 &lt;+dust&gt; no css tho
15:33 &lt;+Complication&gt; But people on 32-bit spoke of it being *way* faster then pure Java (like 10x or similar)
15:35 &lt;bar&gt; hmm.. Complication, could it be that the current amd64 .so is for 32-bit systems only, and he tested it on a 64-bit OS?
15:36 &lt;+Complication&gt; bar: could be, since I tested it too on a 64-bit OS :O
15:36 &lt;jrandom&gt; iirc the amd64 was built to work on pure64 debian
15:37 &lt;+Complication&gt; Either way, some people suggested that importing a fresher gmp might help
15:37 &lt;bar&gt; just a stab in the dark, i'm no wiz at these things
15:37 &lt;jrandom&gt; eh, we use 4.1.4
15:37 &lt;+Complication&gt; Especially after they've done their soon-to-come version jump
15:38 &lt;+Complication&gt; Since I'm no gmp specialist, I couldn't tell much about it
15:38 &lt;jrandom&gt; (and the upcoming optimizations in gmp aren't likely to have substantial improvement)
15:38 &lt;+Complication&gt; Aside from "perhaps indeed"
15:38 &lt;jrandom&gt; improvements come from per-arch builds
15:40 &lt;+Complication&gt; In my test, provoked by their test, however the 64-bit athlon lib on a 64-bit Sempron, on a 64-bit Mandriva, however... does seem only marginally quicker than pure Java
15:40 &lt;+Complication&gt; (oh, and a 64-bit VM)
15:41 &lt;+Complication&gt; (marginally being twice)
15:41 &lt;jrandom&gt; hmm 'k
15:42 &lt;+Complication&gt; I'll try testing on more platform combinations, and tell if I find anything which seems worth relaying
15:43 &lt;jrandom&gt; cool, thanks
15:43 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
15:46 &lt;jrandom&gt; if not...
15:46  * jrandom winds up
15:47  * jrandom *baf*s the meeting closed
</div>
