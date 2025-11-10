---
title: "I2P Dev Meeting - October 31, 2006"
date: 2006-10-31
author: "jrandom"
description: "I2P development meeting log for October 31, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> burl, fedo, jrandom, koff, tethra</p>

## Meeting Log

<div class="irc-log">
15:33 &lt;jrandom&gt; 0) hi
15:33 &lt;jrandom&gt; 1) Net status
15:33 &lt;jrandom&gt; 2) Syndie dev status
15:33 &lt;jrandom&gt; 3) ???
15:33 &lt;jrandom&gt; 0) hi
15:33  * jrandom waves
15:33 &lt;jrandom&gt; weekly status notes up at http://dev.i2p.net/pipermail/i2p/2006-October/001316.html
15:33  * tethra waves back!
15:34 &lt;jrandom&gt; lets jump on in to 1) net status
15:34 &lt;jrandom&gt; no news on this front afaik... things seem stable
15:34 &lt;jrandom&gt; anyone have anything they want to bring up on it?
15:35 &lt;+tethra&gt; nothing here
15:36 &lt;jrandom&gt; ok lets jump on to 2) Syndie dev status then
15:37 &lt;jrandom&gt; as mentioned in the notes, i've been exploring some wysiwyg editor components, but it seems a big pain in the ass (no suprise), and no great solution exists afaik
15:38 &lt;jrandom&gt; so, right now my thoughts are to go with a basic editor with helpers like you see on forums like forum.i2p.net.  not wysiwyg, but helpful
15:39 &lt;+tethra&gt; makes sense. might wysiwyg be a progression later on, then?
15:39 &lt;jrandom&gt; of course, if someone tracks down a good small oss wysiwyg editor, i'd love to hear about it (though i've reviewed a dozen options)
15:39 &lt;jrandom&gt; aye, thats a great way for later enhancement
15:40 &lt;+tethra&gt; less of a jump between geek and non geek that way :)
15:40 &lt;+tethra&gt; (have you looked at Nvu?)
15:41 &lt;jrandom&gt; aye, huge, but promising
15:41 &lt;+tethra&gt; which others had you looked at?
15:42 &lt;+tethra&gt; out of interest
15:42 &lt;jrandom&gt; everything i could google into.  no list at hand
15:42 &lt;+tethra&gt; ah, right
15:44 &lt;koff&gt; Would it be useful to have a split view with the html at the bottom and a realtime updating rendering of the page at the top?
15:45 &lt;+tethra&gt; or maybe left/right (being able to choose would be lovely
15:45 &lt;+tethra&gt; )
15:45 &lt;jrandom&gt; aye, thats a good idea (not entirely realtime, but semi-realtime)
15:46 &lt;+tethra&gt; yeah, refresh button etc
15:46 &lt;jrandom&gt; perhaps on 5s idle or a button press
15:46 &lt;jrandom&gt; right
15:48 &lt;koff&gt; You could maybe even have two cursors, so you almost feel like you're navigating both at the same time?
15:48 &lt;+tethra&gt; that'd be a bit confusing :/
15:48 &lt;koff&gt; maybe :)
15:50 &lt;jrandom&gt; ok, anyone have anything else on 2) syndie dev status?
15:51 &lt;jrandom&gt; if not, lets move on to 3) ???
15:51 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
15:54 &lt;+fedo&gt; yeah Jr , can hope to have a "joe 6 pack"'s  guide to use syndie 1.0 ? ie : what we can do with that text mode console ...
15:55 &lt;+fedo&gt; i'll love to help to test syndie but i'm still unable to understand how to use syndie ! :)
15:55 &lt;jrandom&gt; fedo: does http://syndie.i2p.net/manual.html and http://syndie.i2p.net/features.html and http://syndie.i2p.net/usecases.html help?
15:55 &lt;jrandom&gt; is it a question of "what can you do with syndie", or "how can you do $x"?
15:55 &lt;+fedo&gt; hm not really Jr :-/
15:56 &lt;+fedo&gt; really, i try to do it ...
15:56 &lt;+fedo&gt; how i can use syndie ...
15:57 &lt;+fedo&gt; the text mode console is not a problem
15:57 &lt;jrandom&gt; how you can use syndie /to do what/?  or is that the question itself - why would you install and use syndie?
15:57 &lt;+fedo&gt; but what to do when i've installed Syndie is one :-s
15:57 &lt;jrandom&gt; ah
15:58 &lt;jrandom&gt; ok, think of syndie like a customized web browser - you install it so that you can participate in forums.  once you install it, you need to tell it what forums you want to participate in
15:59 &lt;jrandom&gt; the current 0.919b install will out of the box tie in to the syndie archive at http://syndie.i2p.net/archive/ - you can just install it, log in, and sync up
16:00 &lt;jrandom&gt; and once you've synced up, you can read posts to the various forums, post up replies, or post up to your own forum
16:01 &lt;+fedo&gt; Jr : i'm thinking that you could made a breif note to explain how to use Syndie : ie how to sync, how to fecth a post ...
16:02 &lt;+tethra&gt; (or even, an example repository (syndie.i2p.net ?) to sync to)
16:02 &lt;+tethra&gt; oh, didn't read above :/
16:02 &lt;+tethra&gt; nvm
16:03 &lt;jrandom&gt; fedo: good idea, i'll write one up
16:03  * fedo waves
16:05 &lt;jrandom&gt; ok cool, anyone have anything else for the meeting?
16:05 &lt;+fedo&gt; we know that you to enable the use of syndie on freenet : tell us how to do it ... (you know that i'm unable to find by reading the syndie's code :-/ )
16:05 &lt;+fedo&gt; ((help me :))
16:06 &lt;jrandom&gt; http://syndie.i2p.net/manual.html#syndicate_freenetpost
16:06 &lt;jrandom&gt; and http://syndie.i2p.net/manual.html#syndicate_getindex
16:07 &lt;+fedo&gt; many 'neurones' to burn but i'll  try :)
16:07 &lt;burl&gt; fedo: Complication has written a brief and pretty handy startup guide on the forum here: http://forum.i2p/viewtopic.php?p=8860#8860
16:08 &lt;jrandom&gt; ah right, thats a good one burl
16:08 &lt;+fedo&gt; thanks burl : i'll have a look to that note ;)
16:12 &lt;jrandom&gt; word, ok, if there's nothing else for the meeting...
16:12  * jrandom winds up
16:12  * jrandom *baf*s the meeting closed
</div>
