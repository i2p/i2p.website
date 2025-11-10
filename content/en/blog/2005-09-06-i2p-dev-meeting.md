---
title: "I2P Dev Meeting - September 06, 2005"
date: 2005-09-06
author: "jrandom"
description: "I2P development meeting log for September 06, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> adamta, ardvark, bar, cervantes, jrandom, Pseudonym, Ragnarok, susi23</p>

## Meeting Log

<div class="irc-log">
13:04 &lt;jrandom&gt; 0) hi
13:04 &lt;jrandom&gt; 1) Net status
13:04 &lt;jrandom&gt; 2) Syndie status
13:04 &lt;jrandom&gt; 3) susidns
13:04 &lt;jrandom&gt; 4) ???
13:04 &lt;jrandom&gt; 0) hi
13:04  * jrandom waves
13:04 &lt;+bar&gt; salaam aleikum
13:04 &lt;jrandom&gt; status notes up @ http://dev.i2p.net/pipermail/i2p/2005-September/000888.html
13:04 &lt;+Ragnarok&gt; hi
13:04  * cervantes tips his hat
13:04 &lt;+fox&gt; * adamta waves back across the Irc2p/Freenode bridge
13:05 &lt;jrandom&gt; :)  ok, movin' in to 1) net status
13:05 &lt;@cervantes&gt; *** Disconnected
13:05 &lt;jrandom&gt; things seem to be going reasonably well from what i can see
13:05 &lt;jrandom&gt; heh
13:06  * cervantes concurs...only one netsplit in a few days
13:06 &lt;jrandom&gt; i know we do still have some problems when one's net con is heavily congested (causing messages to back up and fail, resulting in more elGamal and higher CPU usage)
13:06 &lt;@cervantes&gt; and my irc connection uptime is as long as my routers'
13:06 &lt;+Ragnarok&gt; same as usual for me.  Slow, but usable, with intermittent unreliability
13:07 &lt;jrandom&gt; nice, i have been seeing that too cervantes 
13:07 &lt;jrandom&gt; Ragnarok: unreliability with eepsites, irc, i2pbt, i2phex, mail, all of the above?  with 0.6.0.5 or earlier?
13:08 &lt;+Ragnarok&gt; mostly in the form of irc disconnects every few hours. 
13:08 &lt;+Ragnarok&gt; don't use a whole lot else, so I don't have much more information
13:08 &lt;jrandom&gt; hmm, do you have the bw limiter set?
13:08 &lt;+Ragnarok&gt; yeah
13:08 &lt;jrandom&gt; (as a reminder, -1 now means 16KBps)
13:09 &lt;+Ragnarok&gt; it's set to more than the default
13:09 &lt;jrandom&gt; ok cool, is it hitting that limit at all, and/or is that limit appropriate for your real net capacity?
13:09 &lt;+Ragnarok&gt; the limit is well below my real capacity, since setting it high seems to kill my wireless router
13:10 &lt;jrandom&gt; heh ok
13:10 &lt;+Ragnarok&gt; but my router doesn't seem to hit the limit anyway
13:11 &lt;+Ragnarok&gt; I can try to stress test it a bit, and keep better track
13:11 &lt;jrandom&gt; does the peak bw usage hit it though (per oldstats.jsp)?  i2p is pretty bursty, and congestion on a burst might cause an irc discon
13:11 &lt;jrandom&gt; cool, that'd be great.  i can only locally test so many situations, so any reports are appreciated
13:11 &lt;+Ragnarok&gt; which number am I looking for.  oldstats is pretty dense...
13:12 &lt;+Ragnarok&gt; s/./?/
13:12 &lt;jrandom&gt; heh, sorry - oldstats.jsp#bw.sendBps the 60s peak (the second number on the line)
13:14 &lt;+Ragnarok&gt; what are the units?  The number seems highly improbable
13:14 &lt;jrandom&gt; KBps, sorry
13:14 &lt;jrandom&gt; (its improperly named)
13:15 &lt;Pseudonym&gt; bits or bytes?
13:15 &lt;jrandom&gt; bytes
13:15 &lt;+Ragnarok&gt; unfortuneately, it must be wrong then
13:15 &lt;+Ragnarok&gt; the peak number is a small fraction of the limit, and of the current usage of the router
13:15 &lt;jrandom&gt; hmm, its pretty specific, counting sizeof(messages received)
13:16 &lt;jrandom&gt; (though the bw limiter itself works at a lower level, counting sizeof(packets received or sent)
13:16 &lt;+Ragnarok&gt; how bad is it if I cut & paste the line? :)
13:16 &lt;jrandom&gt; might be safer to msg it to me 
13:17 &lt;+Ragnarok&gt; wait, I was looking at the 60 m rate.  It still looks low, but at least it's higher than the current usage.
13:17 &lt;+Ragnarok&gt; sorry
13:17 &lt;+Ragnarok&gt; I'll /msg you more info
13:17 &lt;@cervantes&gt; Ragnarok: we'd instantly be able to determin your name, address and credit details from the netDB
13:17 &lt;jrandom&gt; heh
13:18 &lt;jrandom&gt; cervantes: thats why the netDb bw publishes only the *current* rate, not the peak ;)
13:18 &lt;jrandom&gt; (but yeah, giving out one's bw usage can be dangerous to an adversary)
13:19 &lt;jrandom&gt; ok, anyone else have anything to bring up wrt net status?
13:21 &lt;jrandom&gt; if not, moving on to 2) syndie status
13:22 &lt;jrandom&gt; lots of syndie progress, as outlined in the email and on my blog.  rather than repeating it here, anyone have anything to bring up on that front?
13:22 &lt;@cervantes&gt; Officiali2pApps++
13:23 &lt;+fox&gt; &lt;adamta&gt; I'm modifying the JSP files to use more structured/semantic markup so that it can be more flexibly styled with CSS.
13:23 &lt;+fox&gt; &lt;adamta&gt; I don't have anything to show yet, but I'll post on the mailing list when I have something ready.
13:23 &lt;+Ragnarok&gt; maybe a small description on what you think the common use case for syndie is might be nice.  I'm still a little unsure as to what it is, aside from a blog CMS
13:23 &lt;jrandom&gt; cool adamta - be sure to work with the latest codebase, as I went through and css'ed everything last night
13:24 &lt;jrandom&gt; (at a rought level, that is)
13:24 &lt;+fox&gt; &lt;adamta&gt; jrandom: Oops... I'd been working on an earlier version.
13:24 &lt;+fox&gt; &lt;adamta&gt; I'll `cvs update` and see what's changed, then.
13:24  * Ragnarok , asking for user docs.  Oh the hypocrisy
13:24 &lt;jrandom&gt; good call Ragnarok.  the use case is essentially '$myI2P.getUseCases()'
13:25 &lt;jrandom&gt; safe syndication and publication of content, rather than using eepsites
13:25 &lt;jrandom&gt; (as eepsites don't allow safe syndication, require more skill for publication, and require high availability of the operating node)
13:25 &lt;+Ragnarok&gt; how is it syndicated, though?
13:26 &lt;jrandom&gt; a good intro to syndie's aims is in the post http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000001&images=false&expand=true
13:27 &lt;jrandom&gt; syndication, right now, is done through http with explicitly specified syndication peers (either apache archives, other syndie instances, or freesites with syndie archives)
13:27  * cervantes just pulled apart the syndie css... it's sufficiently classes to do a varied amount of styling, but the markup itself isn't good for working in new themes
13:27 &lt;+Ragnarok&gt; oh, nice.  I don't think I've seen that
13:27 &lt;@cervantes&gt; *classes=classed
13:27 &lt;@cervantes&gt; adamta: I'd be interested in seeing what you come up with
13:28 &lt;jrandom&gt; cervantes: i'm no css wonk, so anyone inspired to improve upon it, restructure it, or revamp how the whole css/frontend works is very much appreciated :)
13:28 &lt;@cervantes&gt; just get rid of those damn tables :)
13:28 &lt;jrandom&gt; heh
13:30 &lt;+fox&gt; &lt;adamta&gt; cervantes+jrandom: Indeed. There's enough there for basic styling, like changing the colour scheme, but I'm trying to modify it to get rid of the tables and to provide enough semantic markup (nested &lt;div&gt;s for sections, header tags, and so forth, all with classes and IDs when it would be useful) so that a stylesheet can completely change the appearance to the user's liking.
13:30 &lt;@cervantes&gt; cool
13:30 &lt;jrandom&gt; kickass adamta!
13:31  * jrandom will not touch that side of things for a bit (i've got plenty to work on in the router :)
13:31 &lt;@cervantes&gt; on a semi related note the new routerconsole themes have been somewhat delayed by arcturus' *ahem* disappearence
13:31 &lt;jrandom&gt; heh d'oh
13:31 &lt;@cervantes&gt; I'm trying to pick up where he left off with some of the workflow tweaks
13:32 &lt;@cervantes&gt; but I don't have the JSP skills to do anything radical like fix the broken tunnel config screens
13:33 &lt;jrandom&gt; ah cool, any progress is good, and if you need help with anything in particular, i'm 'round
13:33 &lt;jrandom&gt; adamta: one thing to keep in mind is the multiple-style thing (using the author-selected but locally hosted style) ((check my recent blog posts for more info))
13:33 &lt;@cervantes&gt; having said that the new alternative theme is looking ok
13:33 &lt;jrandom&gt; nice
13:34 &lt;+fox&gt; &lt;adamta&gt; The new color scheme is definitely nicer, if that's what you're referring to (?).
13:35 &lt;@cervantes&gt; adamta: it would be cool if the author's can select a complete style from a set of templates for their particular blog
13:35 &lt;jrandom&gt; cervantes: do you think we should deploy those jsp/css changes arcturus bounced me before, or would you prefer to hold off until you've finished some more pieces of it?
13:36 &lt;@cervantes&gt; jrandom: I'm not sure what he gave you
13:36 &lt;@cervantes&gt; if you can sling them over to me I can compare...I have made additional markup changes since I last discussed things with him
13:37 &lt;jrandom&gt; cervantes: individual blog posts can now have per-blog style applied (causing e.g. class="s_detail_addressLink ss_minimal_detail_addressLink" to be used in the html, assuming the style specified is "minimal")
13:37 &lt;jrandom&gt; cool, i'll bounce 'em your way cervantes 
13:37 &lt;@cervantes&gt; ta
13:38 &lt;jrandom&gt; cervantes: a per-blog theme is a bit tougher - the LJ folks had to deal with it too, and came up with the compromise saying the list containing multiple blogs uses the reader's style preferences, while the list containing just one blog's posts uses the author's style preferences
13:38 &lt;jrandom&gt; we could publish a 'DefaultStyle: minimal' in the blog's metadata to allow the later
13:39 &lt;@cervantes&gt; yeah that was what I was imagining
13:39 &lt;+susi23&gt; (readers preferences should always override others)
13:39 &lt;+susi23&gt; (but thats an opinion :)
13:39 &lt;jrandom&gt; right, when the reader has explicit preferences
13:39 &lt;@cervantes&gt;  /ignore susi23
13:39 &lt;@cervantes&gt; sheet it didn't work
13:41 &lt;@cervantes&gt; if we make filter by blog more distinct form of navigation
13:42 &lt;@cervantes&gt; such as a side list
13:42 &lt;jrandom&gt; at the moment, the user's preferences are kind of integrated into the workflow, rather than off in a separate prefs page (e.g. a link to bookmark a blog, or ignore them, or hide/show images).  perhaps when we have multiple local styles, it'd be good to have a 'view style' drop down at the top
13:42 &lt;@cervantes&gt; then it will make style changes more pallatable
13:42 &lt;jrandom&gt; hmm yeah ,interblog navigation is going to be interesting
13:43 &lt;jrandom&gt; so you like how it was originally, with that list of blogs on the left hand side, rather than the drop down?
13:43 &lt;jrandom&gt; http://syndiemedia.i2p/viewattachment.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124769600000&attachment=0
13:44 &lt;@cervantes&gt; &lt;bluesky&gt;well that could be a template preference perhaps?&lt;/bluesky&gt;
13:44 &lt;jrandom&gt; hmm, i dont know if stylesheets can turn a list into a drop down, can it?
13:44 &lt;@cervantes&gt; navigation type: dropdown|sidelist|hierarchy  
13:44 &lt;@cervantes&gt; no
13:45 &lt;jrandom&gt; ok, yeah, that can be done in jsp & user preference though, no problem
13:45 &lt;jrandom&gt; (hierarchy?)
13:45 &lt;+susi23&gt; (sure, you can give the select a rows parameter)
13:45 &lt;@cervantes&gt; but if you abstract the markup into templates then you can have multiple user preference layouts
13:45 &lt;jrandom&gt; ah, true, as a multivalued list
13:45 &lt;jrandom&gt; (rather than an html list of links)
13:46 &lt;@cervantes&gt; (I was blueskying though)
13:46 &lt;jrandom&gt; right right cervantes (though it'd be nice if we can do as much templating as possible through css, since thats easier to deploy themes for)
13:46 &lt;jrandom&gt; ((especially with the new docs/syndie_standard.css))
13:46 &lt;@cervantes&gt; you might want to save that until version 2 and concentrate on more important aspects
13:47 &lt;+susi23&gt; (you could put all three variants in the html source and the users decides which divs we want to hide)
13:47 &lt;@cervantes&gt; right, if adamta sorts out the markup then you can probably do quite dramatic variations
13:47 &lt;jrandom&gt; aye, but i'm open for ideas for the default.  if there's a better way to nav, it'd be better to deploy that
13:47 &lt;jrandom&gt; good call susi23 
13:47 &lt;+susi23&gt; (k, not very elegant way ;)
13:47 &lt;@cervantes&gt; as in http://www.csszengarden.copm
13:48 &lt;@cervantes&gt; * http://www.csszengarden.com
13:48  * jrandom is glad i implemented ArchiveIndex as a separate object from Archive, so all this stuff is essentially just churning through the archive.txt textfile :)
13:49 &lt;jrandom&gt; ok, anyone have any further questions/comments/concerns wrt syndie?
13:50 &lt;jrandom&gt; (one thing to note is that the new petname stuff has a one-click export to the user's userhosts.txt file, dumping any i2p addresses there [but it doesn't import yet])
13:50 &lt;@cervantes&gt; nice work
13:50 &lt;jrandom&gt; gracias cervantes 
13:50 &lt;@cervantes&gt; you going to ever do anything on i2p core again? :)
13:50 &lt;jrandom&gt; heh
13:51  * jrandom has a pair of killer changes to the router coming up, giving us lots of capabilities
13:51 &lt;jrandom&gt; (but more on those when they're tested and ready for deployment)
13:51 &lt;@cervantes&gt; i2pponies.ar
13:51 &lt;@cervantes&gt; i2ponies.war
13:52 &lt;@cervantes&gt; hmm vnc refresh is slow tonight
13:52 &lt;+susi23&gt; (pony wars? poor ponies...)
13:52 &lt;jrandom&gt; heh
13:52 &lt;jrandom&gt; ok, moving on to 3) susidns
13:52 &lt;jrandom&gt; susi23: wanna give us a rundown?
13:52 &lt;+susi23&gt; well
13:53 &lt;+susi23&gt; there is not much to say... susidns is a very simple webapp giving you access to addressbook configuration and subscriptions files
13:53 &lt;+susi23&gt; and to your "addressbooks" namely hosts.txt, userhosts.txt and (if existing) your published addressbook
13:54 &lt;+susi23&gt; I added an introduction page and some explanations how addressbook works
13:54 &lt;+susi23&gt; (ok, how I think addressbok works ;)
13:54 &lt;jrandom&gt; w00t :)
13:54 &lt;+bar&gt; userhosts.txt?
13:54 &lt;+susi23&gt; as there've been user questions about this in the last weeks
13:54 &lt;+Ragnarok&gt; I'll send feedback, once I try it out :)
13:54 &lt;@cervantes&gt; cool, how ready is it?
13:54 &lt;+susi23&gt; sure
13:54 &lt;+susi23&gt; usable
13:55 &lt;ardvark&gt; i use addressbook, but have no userhosts.txt, or is userhosts.txt my personal/private eepsites?
13:55 &lt;jrandom&gt; ardvark: userhosts is for user specified custom overrides (it doesnt exist by default)
13:55 &lt;+susi23&gt; userhosts.txt is a 2nd hosts.txt file which is read by the NamingService
13:55 &lt;ardvark&gt; ok
13:55 &lt;+Ragnarok&gt; userhosts.txt is the one you can edit without fear of dataloss via race conditions :)
13:55 &lt;+susi23&gt; and yes people used this for private keys
13:56 &lt;+susi23&gt; (which is a bit dangerous now when you activate addressbook publication)
13:57 &lt;+susi23&gt; well, no magic here... thats all
13:57 &lt;+Ragnarok&gt; adding a privatehosts.txt or something, which is read by the NamingService but not addressbook would be trivial
13:57 &lt;+susi23&gt; true
13:57 &lt;@cervantes&gt; I would like to see that ;-)
13:58  * cervantes clutches his private keys ;-)
13:58 &lt;jrandom&gt; ooh, susidns intro page is nice :)
13:58 &lt;jrandom&gt; (cervantes/susi/ragnarok/et al: see the syndie pet name web interface too [you need to log in to see it])
13:58 &lt;+susi23&gt; as addressbooks publication is turned off by default there is no danger for normal people
13:58 &lt;jrandom&gt; right right
13:59 &lt;+Ragnarok&gt; I've asked this before, but is there anything I can do to make life easier for people writing addressbook frontends?
13:59  * cervantes has forgotten his login
13:59 &lt;jrandom&gt; cervantes: you can register again ;)
13:59 &lt;+Ragnarok&gt; so have I, probably
14:00 &lt;@cervantes&gt; wouldn't sushidns be a better name?
14:00  * cervantes ducks
14:00 &lt;+susi23&gt; ragnarok: how about a function to interupt the sleeping thread for immediate (user triggered) subscription update?
14:01 &lt;jrandom&gt; ooh, or a manual "fetch now" capabiliy
14:01  * susi23 slaps cervantes with a large trout.
14:01 &lt;+susi23&gt; yes, calling it dns is ridiculous here...but thats a historic name :)
14:01 &lt;@cervantes&gt; raw trout!
14:01  * cervantes grabs the soya sauce
14:01 &lt;+susi23&gt; (pervert!)
14:02 &lt;+susi23&gt; k, back to topic please ;)
14:02 &lt;+Ragnarok&gt; ok, I'll look into that
14:02 &lt;+susi23&gt; (don't drink at meetings!)
14:02  * jrandom hides my drink
14:03  * susi23 pings jrandom
14:03 &lt;jrandom&gt; ok cool, thanks susi, looks v.nice
14:03 &lt;jrandom&gt; ok, moving on to 4) ???
14:03 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
14:04 &lt;@cervantes&gt; if anyone has been experiencing any issues with irc2p please let the admins know
14:06 &lt;@cervantes&gt; #irc2p is the support channel
14:06 &lt;@cervantes&gt; or post to the forum
14:06 &lt;@cervantes&gt; jrandom: do you want a syndie forum btw? (or is that redundant)
14:07 &lt;@cervantes&gt; susi23: you're welcome to have one too, for you plethora of i2p apps ;-)
14:07 &lt;jrandom&gt; atm, i think we're ok without one, thanks though
14:07 &lt;jrandom&gt; the susiworld forum
14:09 &lt;jrandom&gt; ok, if there's nothing else
14:09  * jrandom winds up
14:09  * jrandom *baf*s the meeting closed
</div>
