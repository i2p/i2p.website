---
title: "I2P Dev Meeting - January 17, 2006"
date: 2006-01-17
author: "jrandom"
description: "I2P development meeting log for January 17, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> b0unc3, cat-a-puss, cervantes, Complication, DoubtfulSalmon, dust, jme\___, jrandom, lordalbert, Pseudonym, tethra, wmpq, zzz</p>

## Meeting Log

<div class="irc-log">
15:40 &lt;jrandom&gt; 0) hi
15:40 &lt;jrandom&gt; 1) Net status and 0.6.1.9
15:40 &lt;jrandom&gt; 2) Tunnel creation crypto
15:40 &lt;jrandom&gt; 3) Syndie blogs
15:40 &lt;jrandom&gt; 4) ???
15:40 &lt;jrandom&gt; 0) hi
15:40  * jrandom waves
15:40 &lt;jrandom&gt; weekly status notes posted @ http://dev.i2p.net/pipermail/i2p/2006-January/001251.html
15:41 &lt;@cervantes&gt; pfff, good job i2p is more reliable than NASA
15:41 &lt;jrandom&gt; heh 
15:41 &lt;tethra&gt; haha
15:41 &lt;jrandom&gt; (though I am 20 minutes late... ;)
15:41 &lt;jrandom&gt; anyway, lets jump on in to 1) Net status and 0.6.1.9
15:42 &lt;wmpq&gt; NSA or NASA, not that diffrent are they?
15:42 &lt;@cervantes&gt; I said I2P not jrandom ;-)
15:42 &lt;jrandom&gt; good point cervantes ;)
15:42 &lt;tethra&gt; don't be silly, jrandom IS i2p! ;D
15:42 &lt;@cervantes&gt; oh I thought it was a way of thinking
15:42 &lt;wmpq&gt; [redact]
15:43 &lt;jrandom&gt; heh well, anyway, 0.6.1.9 is out and about, with 70% of the net upgraded (thanks y'all)
15:43 &lt;Pseudonym&gt; mmmm, tasty new release
15:44 &lt;+zzz&gt; client tunnel build success remains &lt;30%
15:44 &lt;jrandom&gt; I haven't heard many reports of substantially increased end to end throughput, though some routers are more than saturating T1 lines
15:44 &lt;+zzz&gt; down from ~40%
15:44 &lt;+Complication&gt; Bandwidth seems normal, a bit higher than on the last CVS before release. Peer counts look a big higher.
15:45 &lt;jrandom&gt; hmm, yeah, I'm not really worried about that zzz, since its all getting completely reworked for 0.6.2
15:45 &lt;+zzz&gt; avg BW up from ~12K to ~20K
15:45 &lt;jrandom&gt; 0.6.1.9 shouldn't pick peers more liable to agree (meaning, high capacity), but should instead focus on those who have higher throughput
15:46 &lt;+Complication&gt; Retransmission percentage (noted 7% on the night of release) has come down to 6 point something
15:46 &lt;jrandom&gt; aye, with routers pushing 1-300KBps, there's going to be a skew
15:46 &lt;jrandom&gt; hmm, thats a pretty crazy rate Complication, i've only seen 2-3%
15:46 &lt;jrandom&gt; (but I don't doubt what you see)
15:47 &lt;+Complication&gt; I'm maxing out my outbound, pretty much
15:47 &lt;+Complication&gt; (and I mean maxing out the line capacity)
15:47 &lt;jrandom&gt; ah, that'd do the trick
15:47 &lt;+zzz&gt; still getting NULLs before gets which results in 405 bad method, rate may be declining, hard to say for sure
15:48 &lt;jrandom&gt; yeah zzz, there are some things that need to be worked through in the streaming lib, but I probably won't get to that until after the 0.6.2 tunnel revamps
15:48 &lt;jrandom&gt; (but if someone wants to dig in further before that, that would rule, of course)
15:49 &lt;jrandom&gt; Complication: if you reduce your bw limiter to something like 70% of your line capacity, does the failure rate go back to a reasonable value?
15:49 &lt;+zzz&gt; I still think it was something that went in the code just before new years, so better to look at before those recent changes are forgotten :)
15:50 &lt;+zzz&gt; First seen Dec. 29
15:50 &lt;jrandom&gt; yeah zzz, it certainly was.  likely related to how we now honor timeouts.
15:51 &lt;+Complication&gt; jrandom: I'm actually trying that currently :)
15:51 &lt;+Complication&gt; Adjusted a few seconds before you asked, but won't know very soon, I guess
15:51 &lt;jrandom&gt; but there is substantial work that needs to be done in there to clean it up, and its more important to get the new tunnel creation code implemented (which will substantially improve tunnel build success rates, as well as add a whole set of anonymity improvements)
15:51 &lt;jrandom&gt; cool Complication, yeah, give it 3-6 hours 
15:51 &lt;jrandom&gt; (to clear out the old values / connections)
15:52 &lt;+zzz&gt; ~ 1% - 3% of GETs are corrupted atm
15:54 &lt;jrandom&gt; so do you suggest reverting the streaming lib changes (so that i2psnark will OOM all of its users in 12-48 hours) and put off further streaming lib rework until after the 0.6.2 tunnel work, or push out the 0.6.2 tunnel work for a week or two while revamping the streaming lib?
15:55 &lt;+zzz&gt; certainly don't revert
15:56 &lt;+zzz&gt; your call
15:56 &lt;+Complication&gt; It's a fairly sly bug, I can only say
15:58 &lt;jrandom&gt; there are other bugs in the streaming lib, so if I'm going to roll up my sleeves, I'd want to tackle them all together (since none of the remaining bugs are apparent).  
15:59 &lt;jrandom&gt; on the other hand, we'll have substantial bandwidth usage reduction, increased build success percentage, better anonymity, and an improved ability to monitor load balancing on the live net by going with the tunnel work first
15:59 &lt;Pseudonym&gt; if it's only a 1-3% failure rate on surfing, I'd say it can wait, but that's just my opinion.
16:00 &lt;jrandom&gt; I'm leaning towards doing the tunnel work first, since after deploying it, we can passively monitor the network while actively revamping the streaming lib
16:01 &lt;jrandom&gt; (I'd also like to build a GUI for editing/posting to Syndie, but that can wait until after both of those things are sorted ;)
16:01 &lt;+Complication&gt; That's what the rate is like, here too
16:02 &lt;+Complication&gt; (on my eepsite)
16:04 &lt;jrandom&gt; Ok, I think it'd be great if y'all can keep an eye on things to see if those rates changes, but in the meantime, I'll continue on with the tunnel revamp, after which will come the streaming lib revamp (both of which will be in place before 0.6.2)
16:05 &lt;jrandom&gt; (or, if somene wants to dig into the streaming lib [or see if there's some odd interaction with i2ptunnel], lemmie know!)
16:06 &lt;+Complication&gt; jrandom: out of curiosity, could one exclude i2ptunnel with a test app?
16:07 &lt;+Complication&gt; e.g. if something like jnymo's sample app would *also* receive nulls, that would clear i2ptunnel from the list of suspected causes?
16:07 &lt;jrandom&gt; one could wire up a thin (in-VM) I2PSocket implementation to do that, certainly 
16:07 &lt;+Complication&gt; Since, IIRC, that sample used the streaming lib directly...
16:08 &lt;+Complication&gt; (or pretty directly)
16:08 &lt;jrandom&gt; aye, of course if something using the streaming lib can duplicate it, it would exonerate i2ptunnel
16:10 &lt;+Complication&gt; Hmm, unless someone else gets first (I'll try finishing with the webcache thingy first) I might try emulating HTTP with something like that...
16:10 &lt;jrandom&gt; wikked, thanks Complication
16:10 &lt;jrandom&gt; ok, anything else on 1) Net status and 0.6.1.9?  
16:11 &lt;jrandom&gt; if not, lets mosey on over to 2) Tunnel creation crypto
16:11 &lt;+Complication&gt; Nah, it may lead to nothing useful, or I may stumble on halfway... but it's a possibility which intrigues me
16:11 &lt;jrandom&gt; aye, definitely worth exploring Complication
16:12 &lt;jrandom&gt; (and explorations do not have to have positive results to be worthwhile :)
16:12  * cervantes spots a "moo" exception in the source changes leading up to new year....perhaps that's the issue? :)
16:13 &lt;jrandom&gt; ok, there's a new tunnel creation crypto spec referenced in the email, based on the discussion toad, Michael, and myself had on the mailing list last october
16:14 &lt;jrandom&gt; give 'er a look and lemmie know your thoughts - it won't be deployed on the live net for a while, as there are other things that need to be implemented first, but its coming
16:14 &lt;+Complication&gt; Is "moo" a reserved word for Java? ;P
16:14 &lt;+zzz&gt; on 2) I'll help review references in status mail
16:14 &lt;+Complication&gt; On the tunnel crypto subject, do you mind checking if the following rephrase is decent - I'd just like to ensure I've understood it right...
16:14 &lt;jrandom&gt; thanks zzz
16:15 &lt;+Complication&gt; "Each hop encrypts all records with their reply key, which they decrypted from their record, using their ElGamal private key, and by encrypting in such fashion, reverses one layer of decryption (or should I say, encryption) done by the tunnel owner, rendering the next participants' record readable with the next participant's ElGamal private key?"
16:15 &lt;jrandom&gt; Complication: yes
16:15 &lt;+Complication&gt; Or is my rephrase plain wrong?
16:16 &lt;+fox&gt; &lt;jme___&gt; and way to complicated, if i may
16:16 &lt;jrandom&gt; its correct I believe, but yeah, too many clauses :)
16:16 &lt;+Complication&gt; I didn't think of a better way to visualize it. 'Twas hard enough that way. :P
16:16 &lt;jrandom&gt; (or jme___ are you saying the algorithm is too complicated?)
16:17 &lt;+fox&gt; &lt;jme___&gt; nope i tried rapidely to read the doc and give up as too many things require prior knowledge
16:17 &lt;+fox&gt; &lt;jme___&gt; on the other hand i didnt try much :) other things to do
16:17 &lt;jrandom&gt; Complication: http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/i2p/router/tunnel/BuildMessageProcessor.java?rev=HEAD
16:18 &lt;+fox&gt; &lt;jme___&gt; is this peer review a formality, or you are really worried/unsure of it ?
16:19 &lt;+Complication&gt; Well, it's always good to know what an underlying mechanism is doing...
16:19 &lt;jrandom&gt; I'm confident that it does what I intend for it to do, but I am sincerely interested if someone can see a problem
16:19 &lt;+fox&gt; &lt;jme___&gt; if the second i could spend the time, but my knowledge is old and not on top of my head
16:20 &lt;+fox&gt; &lt;jme___&gt; if not i trust :)
16:20 &lt;jrandom&gt; the notes section has some questions - http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt-creation.html?rev=HEAD#tunnelCreate.notes 
16:22 &lt;jrandom&gt; there's no rush, it'll probably be a week or two before this new crypto is actually used in the router 
16:22 &lt;@cervantes&gt; jrandom: on those, would there be much of a performance hit on injecting a random delay between hops?
16:22 &lt;@cervantes&gt; as that seems the most sensible option to prevent timing attacks
16:23 &lt;jrandom&gt; its tunnel creation, so a delay wouldn't hurt, though could cause premature lease set expiration under catastrophic failures
16:25 &lt;jrandom&gt; well, I'm not sure how effective those delays would be.  they may help substantially, but they may not.  live tunnels, however, can simply use blending to detect colluding peers on that tunnel anyway though, so I'm not sure it matters
16:25 &lt;+fox&gt; &lt;jme___&gt; ok rereading it
16:27 &lt;jrandom&gt; thanks.  ok, no rush, but if/when anyone has any thoughts, bounce 'em my way (or to the list, or to your blog, etc)
16:27 &lt;jrandom&gt; ok, anything else on 2, or shall we move on to 3) Syndie blogs?
16:29 &lt;jrandom&gt; (consider us moved)
16:29 &lt;jrandom&gt; ok, new neat bloggy stuff in syndie, dig in ;)
16:29 &lt;@cervantes&gt; v.cool
16:30 &lt;jrandom&gt; the groups on the left can contain links to arbitrary urls, as well as links to blogs, posts within blogs, or attachments to posts within blogs
16:30 &lt;jrandom&gt; there are a whole slew of enhancements possible, too, such as adding per-blog or per-tag styling for posts, icons, etc.  if someone wants to dig into that, it'd rule (and have a highly visible impact :)
16:31 &lt;@cervantes&gt; btw external links defined in comments should also have a title attribute set to the target url (as you have done on the left panel)
16:31 &lt;@cervantes&gt; comments/posts
16:32 &lt;jrandom&gt; ah, good idea
16:33 &lt;jrandom&gt; (net.i2p.syndie.sml.BlogPostInfoRenderer method renderLinks(...) :)
16:34 &lt;@cervantes&gt; *scribble*
16:35 &lt;jrandom&gt; what else do the syndie blogs need for them to offer a functional alternative to informational eepsites?  obviously, syndie is static content, so you can't do some things, but you can publish content and let people comment
16:36 &lt;jrandom&gt; are there particular customizations you want to be able to do?  if so, lemmie know
16:37 &lt;DoubtfulSalmon&gt; jrandom: updating existing content via script?
16:37 &lt;@cervantes&gt; archive by date
16:37 &lt;jrandom&gt; DoubtfulSalmon: via script?
16:37 &lt;jrandom&gt; cervantes: ah, like a little calendar widget, rather than the "5 older entries" links?
16:38 &lt;@cervantes&gt; yup
16:38 &lt;DoubtfulSalmon&gt; jrandom: say I want this file/text to replace that file/text. How do I do that?
16:38 &lt;jrandom&gt; ok cool, yeah, that should be really easy (if someone whips up the html :)
16:38 &lt;@cervantes&gt; or more simply "view last month's posts"
16:39 &lt;@cervantes&gt; jrandom: you just need a 7x6 table with some numbers in it ;-)
16:40 &lt;jrandom&gt; DoubtfulSalmon: changing content that has been published is an interesting direction.  across the board, it wouldn't always work, since it'd have to operate like usenet control messages (cancelling an old post, etc)
16:40 &lt;jrandom&gt; DoubtfulSalmon: on the other hand, you can simply post a new file/entry and change the links on the left hand side to point to the new file/entry
16:40 &lt;jrandom&gt; (that way, the old content is still there, but people are directed to the new content)
16:41 &lt;DoubtfulSalmon&gt; jrandom: yeah, it would be ok if the old content was still there, as long as everyone's links pointed to the new content, without them having to change their content.
16:41 &lt;jrandom&gt; building a full blown wiki out of it, essentially posting diffs with syndie rendering them result, is possible, but may be overkill
16:41 &lt;jrandom&gt; hmm, ok I see what you're saying
16:42 &lt;jrandom&gt; so, you want the ability to have redirectable links, rather than the existing links to exact versions of content
16:43 &lt;jrandom&gt; perhaps that could be done by linking to a blog's bookmark, and the exact version is found by loading that blog's current bookmarks and seeing where it points
16:44 &lt;jrandom&gt; otoh, the new version could be marked as a reply to the old post, so when people follow a link, they can follow it to the reply which replaces the content
16:44 &lt;jrandom&gt; (though thats probably not as seamless)
16:44 &lt;DoubtfulSalmon&gt; yeah: say I want to have a link to say: a current radar image, or somthing like that that will be upadated every 10 min. It's ok if the contet doesn't fly all over the net, but if someone else links to my page, the user should see the current image.
16:45 &lt;jrandom&gt; well, that depends on what they want to do - do they want to link to the image as it was when they referred to it, or do they want to link to the service that renders the image when the reader views it
16:45 &lt;+Complication&gt; cervantes: oddity of the day :D Last post in: http://forum.i2p/viewtopic.php?t=1199&start=15
16:46 &lt;+Complication&gt; Felt like it might be another of our robotic overlords :P
16:46 &lt;jrandom&gt; but its a good idea to support both concepts, and I don't think it'd be much trouble
16:46 &lt;@cervantes&gt; thnx
16:46 &lt;jrandom&gt; though it'd need a small extension to sml (e.g. [blog bloghash="ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=" bookmark="radar.png"])
16:47  * cervantes will upgrade forum defenses if we start to get a lot of them
16:47 &lt;@cervantes&gt; (already know how to stop that one)
16:47 &lt;DoubtfulSalmon&gt; jrandom: they should be able to link to both a static version of it, provided the syndicator has not deleted the content, as well as a generic url that points to whatever is the latest version
16:47 &lt;jrandom&gt; (which would look at ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c='s current meta post for bookmarks, pulling the exact uri from the one named "radar.png")
16:48 &lt;DoubtfulSalmon&gt; jrandom: could that be done now with something like: "View most recent one post in tag &lt;weird string&gt;"
16:48 &lt;jrandom&gt; ah, good point - yes, it could
16:49 &lt;jrandom&gt; that could even be restricted to "View most recent post by $author with tag $tag"
16:49 &lt;jrandom&gt; (so other people couldn't spoof it)
16:49 &lt;DoubtfulSalmon&gt; so maybe just put some sort of UI so the user does not have to see weird tags and what not
16:50 &lt;jrandom&gt; there's an example of how that looks up there, though I don't have the uri offhand... but yeah, is a link around the linked text
16:50 &lt;DoubtfulSalmon&gt; I assume all of that information can come in URL form.
16:51 &lt;jrandom&gt; but this is definitely complicated to write the source SML, which is why a GUI to create SML would be useful
16:51 &lt;jrandom&gt; they're attributes on the SML tags, not URLs
16:52 &lt;@cervantes&gt; and SML gui will be tricky without javascript
16:52 &lt;DoubtfulSalmon&gt; but you can bookmark a search result right?
16:52 &lt;jrandom&gt; what is a search result?
16:52 &lt;jrandom&gt; and what do you mean by bookmark?
16:52 &lt;@cervantes&gt; (or a browser extension ;-)
16:52 &lt;jrandom&gt; oh, browser side bookmarks,  yes
16:52 &lt;+Complication&gt; A filter result?
16:53 &lt;jrandom&gt; but those bookmarks are not generally shareable
16:53 &lt;DoubtfulSalmon&gt; er: a "get most resent 1 post by X with tag Y" 
16:53 &lt;jrandom&gt; (actually, most are, but its not universal, since they're URLs not URIs))
16:53 &lt;DoubtfulSalmon&gt; yeah, it would be good if other bolgs could link to those too
16:54 &lt;jrandom&gt; DoubtfulSalmon: they can, with sml
16:54 &lt;jrandom&gt; [blog tag="Y" bloghash="X"]
16:54 &lt;DoubtfulSalmon&gt; oh goodie
16:55 &lt;jrandom&gt; cervantes: javascript, or xul, or java, or some other OS-specific client app
16:57 &lt;@cervantes&gt; ah cool, so you don't mind a scripting or plugin dependancy
16:57 &lt;jrandom&gt; (when our website gets revamped for 0.6.2, syndie will definitely get a website explaining wtf this whole syndie thing is, and how it can do everything short of wash the dishes ;)
16:57 &lt;@cervantes&gt; (as long as it degrades gracefully)
16:57 &lt;jrandom&gt; cervantes: syndie should be function with lynx, but there's lots of room for rich clients
16:58 &lt;jrandom&gt; (s/function/functional/)
16:58 &lt;@cervantes&gt; right..so lynx uses would get an SML reference chart, but nothing more
16:58 &lt;jrandom&gt; aye, as we have now
16:58 &lt;jrandom&gt; though perhaps a simplified sml, dunno.
17:01 &lt;+Complication&gt; jrandom: do you think it might be even remotely plausible... that the null bug might be related to gzip encoding?
17:01 &lt;+Complication&gt; I was thinking of how to disable gzipping for my eepsite tunnel...
17:01 &lt;+Complication&gt; Or would that be entirely implausible?
17:01 &lt;@cervantes&gt; there was some http compressor stuff added just before new year in i2ptunnel
17:03 &lt;jrandom&gt; aye, it could - yo ucan disable it on the client side with i2ptunnel.gzip=false (on /configadvanced.jsp).  atm I don't think you can disable it in i2ptunnelhttpserver though
17:03 &lt;+zzz&gt; it's on the request side where there isn't any compression
17:03 &lt;+zzz&gt; server won't compess if client set to false
17:03 &lt;+Complication&gt; zzz: oh, right, I forgot that
17:04 &lt;jrandom&gt; (but without too much trouble you could add it to I2PTunnelHTTPServer [line 310, etc)
17:04  * Complication is a fool, and apologizes for that
17:04 &lt;@cervantes&gt; (or you could use a normal tunnel)
17:04 &lt;+Complication&gt; Aha, thanks...
17:05 &lt;jrandom&gt; hmm, though by the time the i2ptunnelhttpserver receives the GET, the null is already there
17:05 &lt;+zzz&gt; yup I did get orion moved back to HTTP tunnel which greatly helps load times for his pages since now compressed again
17:05 &lt;+Complication&gt; I somehow entirely forgot that gzipping starts when the client and server have *agreed* to do it
17:05 &lt;jrandom&gt; so it may be on the client side, but definitely not the server side
17:05 &lt;jrandom&gt; yeah zzz, its pretty insanely fast now :)
17:05 &lt;+zzz&gt; its on the _request_ side not the _response_ side - could be on either client or server side
17:06 &lt;jrandom&gt; true
17:09 &lt;jrandom&gt; ok, anyone else have anything on 3) Syndie blogs?
17:09 &lt;jrandom&gt; if not, lets jump on to 4) ???
17:09 &lt;jrandom&gt; anyone have anything else to bring up for the meeting?
17:10 &lt;cat-a-puss&gt; Complication: Java's gzip stream + I2P tunnels. Does NOT work and it's sun's bug
17:10 &lt;jrandom&gt; hmm cat-a-puss?  really?
17:10 &lt;+zzz&gt; HTTP persistent connections update: client side mostly done, server side making good progress, lots of bulletproofing and testing to do, est. completion 2-4 wks
17:10 &lt;jrandom&gt; nice1 zzz!
17:11 &lt;cat-a-puss&gt; jrandom: yeah I talked to you about that a long time ago, I could probably find the long explination as to why, but it's probably best to just document that somewhere as there is no reason to do it.
17:12 &lt;jrandom&gt; hmm I'm out of context, what exactly does not work?  what is sun's bug?  
17:14 &lt;dust&gt; i get weird logs like this: 21:21:59.816 WARN [%d0%a2%d1%4f] net.i2p.util.EepGet : ERR: status &lt;html&gt;
17:14 &lt;jrandom&gt; hmm, interesting
17:15 &lt;jrandom&gt; what tracker?
17:15 &lt;cat-a-puss&gt; jrandom: As I recall sun uses headerless zips and some magic number to tell that it's a zip stream. But the number just so happens to be negitive, so if you endup creating a zip stream within a zip stream for some reason, it reads the data out of the stream as a sequence of unsigned bytes and so the magic number gets converted to some other positive number. (I am probably missing some detail but that is the gist of it)
17:16 &lt;dust&gt; for example the  OSDevWithCVS_3E.pdf.torrent
17:17 &lt;dust&gt; d8:announce540:http://YRgrgTLGnbTq2aZOZDJQ...
17:17 &lt;jrandom&gt; hmm, I don't know anything about that, and I'm not sure how it'd affect gzip stream over i2ptunnel (if it /did/, they'd all fail, because we gzip evertthing)
17:19 &lt;jrandom&gt; ok cool dust, so postman's tracker.  hmm, are you on 0.6.1.9 dust?
17:20 &lt;cat-a-puss&gt; jrandom: yeah it's been almost a year now sense I had that problem so I don't remember too well, and I don't know if it is fixed in 1.5 but I did have a reall devil of a time trying to figure out why every normal type of stream would work, but as soon as I wrapped them in a compressed stream they would all fail.
17:20 &lt;dust&gt; yes
17:20 &lt;jrandom&gt; cat-a-puss: we've changed things dramatically for compression over i2p in the last year ;)
17:21 &lt;jrandom&gt; (and I don't personally use 1.5)
17:21 &lt;jrandom&gt; but we do our own zip encoding explicitly, rather than use their packaged stream (but for anonymity / efficiency reasons, not compatability)
17:22 &lt;@cervantes&gt; zzz: where exactly in the request does the null happen? right after GET?
17:22 &lt;+Complication&gt; Before, if I remember
17:23 &lt;+fox&gt; &lt;lordalbert&gt; hi
17:23 &lt;+Complication&gt; Sidenote: Celeron 300 shows twice lower retran. percentage than Sempron
17:23 &lt;jrandom&gt; 'lo lordalbert
17:23 &lt;jrandom&gt; cool Complication, 2-3% is reasonable (though I'd prefer lower, of course)
17:23 &lt;@cervantes&gt; would be interesting to fire off a load of HEAD requests or something...
17:24 &lt;jrandom&gt; yeah, a set of local tests would be great, though iirc Complication tried that a while back with no errors
17:24 &lt;+fox&gt; &lt;lordalbert&gt; can anyone make a anonymous tracker? I try it but i dont' understand how use the tunnel
17:24 &lt;+Complication&gt; cervantes: I once tried provoking it, with a recursive wget between my 2 nodes
17:24 &lt;+Complication&gt; Grew tired before it happened
17:25 &lt;@cervantes&gt; heh
17:26 &lt;+fox&gt; &lt;lordalbert&gt; 'lo b0unc3 ;)
17:26 &lt;+fox&gt; &lt;b0unc3&gt; lordalbert, :D
17:26 &lt;+Complication&gt; lordalbert: which part would you need advise about?
17:27 &lt;+Complication&gt; About setting up trackers, I unfortunately don't know.
17:27 &lt;+Complication&gt; About I2PTunnel, I could try explaining...
17:27 &lt;+fox&gt; &lt;lordalbert&gt; I have installed BTtracker, and it work perfectly
17:28 &lt;+Complication&gt; It should also be noted that, for the tracker to *remain* anonymous, it should likely run a pretty careful config
17:28 &lt;+fox&gt; &lt;lordalbert&gt; now, i'd like anonimise it
17:28 &lt;+fox&gt; &lt;lordalbert&gt; so
17:28 &lt;jrandom&gt; I'm sure we can help work through it after the meeting.  you shouldn't use generic trackers, you need one built for anonymity
17:28 &lt;+fox&gt; &lt;lordalbert&gt; i have just made a i2ptunnel
17:29 &lt;jrandom&gt; (e.g. the bytemonsoon modification that you can find on any of the i2p trackers, or in the cvs)
17:29 &lt;+fox&gt; &lt;lordalbert&gt; now, i'd like to know how use this tunnel. I have made a tunnel yet
17:29 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
17:30 &lt;jrandom&gt; lordalbert: http://localhost:7657/i2ptunnel/ should let you create an 'http server tunnel' pointing at your webserver/tracker, but your tracker will not work unless it has been modified for anonymous use
17:30 &lt;+fox&gt; &lt;lordalbert&gt; jrandom, what tracker i must use?
17:31 &lt;+Complication&gt; postman uses a modified version of ByteMonsoon, I think
17:32 &lt;jrandom&gt; i2p-bytemonsoon has been modified for anonymous use - there's a zip up @ http://i2p-bt.postman.i2p/, and there's the cvs in http://dev.i2p.net/cgi-bin/cvsweb.cgi/bytemonsoon/ but I really don't know much about it
17:32 &lt;+fox&gt; &lt;lordalbert&gt; isn't bytemonsoon obsolete?
17:32 &lt;jrandom&gt; if it works, its not obsolete.  it works
17:33 &lt;+fox&gt; &lt;lordalbert&gt; ok XD
17:33 &lt;jrandom&gt; there are many trackers out there, and if some developer wants to modify it to work safely and anonymously, that'd be great
17:33 &lt;+Complication&gt; May well be oldish... but definitely works with destkeys instead of IP's...
17:33 &lt;+Complication&gt; Can't tell about security and leakproofness
17:34 &lt;jrandom&gt; (it was modified by duck et al for anonymity and security)
17:34 &lt;+Complication&gt; But it's been up for a while, and seems to manage...
17:35 &lt;jrandom&gt; ok, if there's nothing else for the meeting...
17:36  * jrandom winds up
17:36  * jrandom *baf*S the meeting closed
</div>
