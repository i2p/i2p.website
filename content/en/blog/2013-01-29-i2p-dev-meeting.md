---
title: "I2P Dev Meeting - January 29, 2013"
date: 2013-01-29
author: "dg"
description: "I2P development meeting log for January 29, 2013."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, hottuna, str4d, zzz</p>

## Meeting Log

<div class="irc-log">
20:08:14  &lt;dg&gt; so hi all
20:08:33  &lt;dg&gt; we didn't really talk much about the agenda but we have some big stuff to discuss anyhow so no big deal
20:08:55  &lt;dg&gt; first topic is the new website design and the blockers for getting it live
20:08:58  &lt;dg&gt; so i'll hand over to str4d
20:09:09  * dg passes metaphorical spotlight to str4d 
20:09:20  &lt;str4d&gt; Hi!
20:09:27  &lt;str4d&gt; &lt;/ocd&gt;
20:10:07  &lt;str4d&gt; Right, well I haven't had as much time over the last week to work on it, but the site *can* go live if desired.
20:10:26  &lt;str4d&gt; The blockers (that I see) are tagging the documentation for translations.
20:10:37  &lt;str4d&gt; Oh, and fixing URLs - that actually is a blocker.
20:10:48  &lt;str4d&gt; (I've been doing them at the same time).
20:11:45  &lt;str4d&gt; I've done the rest of the site - we just need to go through every page of the documentation and repeat what I've been doing: add translation tags to each paragraph/heading/list item/whatever, and check/correct the site-internal URLs.
20:12:29  &lt;str4d&gt; The other bit that I consider a blocker is getting the old translations migrated to the new format, i.e. going through the old faq_lang.html etc. pages and copying their text into the .po files as appropriate.
20:12:55  &lt;dg&gt; Translation tagging IMHO isn't a true blocker but something we need to finish soon, I don't know how you guys feel about going live without translations fully done
20:13:14  &lt;str4d&gt; (I've done 1.2 pages for de and 1 page for es as an example, but it really needs to be someone who understands the language, so that the copy-paste can be verified)
20:14:00  &lt;str4d&gt; (since there is no guarantee that the two individual pages have the same content)
20:15:52  &lt;str4d&gt; Design-wise, I'm starting to be more inclined to just leave the modified duck's theme there; it's had praise from quite a few people, including a designer. I'm personally still not happy with it (e.g. I find it a bit hard to read the long text passages in the documentation), but I wouldn't call it a blocker.
20:16:09  &lt;dg&gt; I like it more or less
20:16:40  &lt;str4d&gt; Oh - one bad thing currently is that the mobile CSS I added seems to not work on mobiles *derp*
20:16:52  &lt;str4d&gt; (Though it works quite nicely on a narrowed desktop browser)
20:19:26  &lt;str4d&gt; That's really about it for the site, as far as I can think of - it's functioning nicely, and most of the groundwork is in place.
20:19:41  &lt;dg&gt; I'll go check out for any broken links later
20:19:52  &lt;dg&gt; I found some previously
20:20:17  &lt;str4d&gt; dg: my test site is running the latest version, so you can check there.
20:20:32  &lt;str4d&gt; The only broken links should be in /lang/doc/*
20:20:35  &lt;dg&gt; let me dig up the ticket
20:20:38  &lt;str4d&gt; Every other page should be fine.
20:20:45  &lt;str4d&gt; It's ticket #807
20:20:52  &lt;dg&gt; saved me some time :)
20:20:59  &lt;iRelay&gt; http://trac.i2p2.i2p/ticket/807 - (accepted enhancement) - Revamp of website
20:20:59  &lt;dg&gt; want to revisit this next week then?
20:23:38  &lt;dg&gt; Found one.
20:23:46  &lt;dg&gt; http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/docs/how/networkcomparisons from http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/docs/how/garlic-routing
20:23:49  &lt;str4d&gt; Oh, and /lang/misc/* hasn't been looked at either.
20:23:56  &lt;iRelay&gt; Title: Garlic Routing - I2P (at vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p)
20:24:06  &lt;dg&gt; Should be /en/comparison
20:24:12  &lt;dg&gt; sorry for pasting whole thing, won't do it again
20:24:15  &lt;dg&gt; eyerape
20:24:22  &lt;str4d&gt; dg: yep, that is a side-effect of my hypenating all the double-worded pages.
20:24:30  &lt;str4d&gt; Oh, that too.
20:25:09  &lt;dg&gt; /docs/how/garlic-routing has /docs/how/elgamalaes, should be /docs/how/elgamal-aes
20:25:16  &lt;dg&gt; i'll put them all into the ticket later
20:25:23  &lt;dg&gt; &lt;+dg&gt; want to revisit this next week then?
20:26:01  &lt;str4d&gt; I'm happy to. Anyone else want to comment? ^_^
20:27:18  &lt;Meeh&gt; http://meeh.i2p/viewmtn/viewmtn.py/
20:27:49  &lt;dg&gt; internal server error on http://meeh.i2p/viewmtn/viewmtn.py/branch/changes/i2p.i2p
20:28:45  &lt;Meeh&gt; yepp
20:28:48  &lt;Meeh&gt; working on it
20:28:55  &lt;dg&gt; I'll take it as a no, anyway
20:28:58  &lt;dg&gt; so onto .. crypto?
20:29:18  &lt;str4d&gt; One last question then: given the apparent level of apathy from people in here regarding copying over the old translations, would it be a better idea to just abandon them and upload the blank .po to Transifex?
20:29:44  &lt;dg&gt; Isn't Transifex reasonably active?
20:29:51  &lt;str4d&gt; The .po file will end up on Transifex anyway; I had just planned on it containing the old translations as a bit of a head start.
20:30:05  &lt;dg&gt; I'd say yes
20:30:48  &lt;str4d&gt; Any other votes?
20:32:38  &lt;str4d&gt; If we go with that, then I'll try and tag as many more pages as I have time for, and then I'll create .po files for the current website languages. Then someone with Transifex access can create an i2p.www subprojcet and upload them (KillYourTV?)
20:32:50  * psi reads scrollback
20:33:34  &lt;psi&gt; votes on a hackfest?
20:35:05  * psi reads more scrollback
20:39:01  &lt;str4d&gt; ...
20:39:04  * str4d doesn't like assuming, but assumes that no one has objections to that line of action.
20:39:04  &lt;dg&gt; too quiet&gt;.&gt;
20:39:04  &lt;str4d&gt; In that case, the old translations will be discarded from i2p.www.revamp (or maybe just left in the branch for now - if a translator really wants to they can find them for reference).
20:39:04  &lt;psi&gt; no formed opinion
20:39:14  &lt;SkinSystem&gt; hi, i heard k0e touches himself whilst watching granny pr0n
20:39:21  &lt;dg&gt; uh?
20:39:32  &lt;psi&gt;&gt;.&gt; #i2p-chat
20:40:45  &lt;str4d&gt; Right, that's it from me on the website.
20:49:59  &lt;dg&gt; well..
20:50:11  &lt;dg&gt; IDK if wait(str4d)
20:51:33  &lt;dg&gt; AFK, back soon
21:03:55  &lt;hottuna&gt; zzz, did you see the update of http://trac.i2p2.de/wiki/Crypto/CurrentSpecs ?
21:03:58  &lt;iRelay&gt; Title: Crypto/CurrentSpecs  I2P (at trac.i2p2.de)
21:07:36  &lt;zzz&gt; yeah you guys are doing a great job
21:08:13  &lt;hottuna&gt; do you think we are using asymmetric ciphers where they aren't needed?
21:08:23  &lt;hottuna&gt; and could be replaced by symmetric alternatives?
21:08:38  &lt;zzz&gt; I doubt we're using anything where it isn't needed
21:09:04  &lt;hottuna&gt; good
21:09:15  &lt;zzz&gt; the web page crypto section needs the symm/asymm crypto added ofc, right now it's only sigs
21:09:46  &lt;hottuna&gt; yeah. But one issue at a time
21:09:53  &lt;hottuna&gt; I think the signs are the most vulnerable anyway
21:10:07  &lt;zzz&gt; right. just as a one-liner placeholder is all I meant
21:20:19  &lt;hottuna&gt; zzz, sud signing should be fairly do-able as far as implementation and not having a flag day goes?
21:20:41  &lt;hottuna&gt; do-able as in possibly to change cipher for.
21:23:58  &lt;dg&gt; back
21:26:53  &lt;zzz&gt; i guess. we did su2 w/o incident, so why not su3, su4, ...
21:28:38  &lt;hottuna&gt; but before we should decide what cipher is the most viable
21:36:25  &lt;dg&gt; okay
21:36:33  &lt;dg&gt; since str4d_afk is gone.. uh
21:36:51  &lt;dg&gt; zzz, hottuna, do you want to discuss anything further or should we close the meeting? It seems like nobody else is around
21:40:29  &lt;dg&gt; a'ight
21:40:35  * dg bafs the meeting closed
21:41:11  &lt;hottuna&gt; thanks dg :)
21:41:55  &lt;dg&gt; str4d went MIA
21:45:03  &lt;dg&gt; anyway, np
23:00:32  &lt;str4d&gt; Sorry, connection went down and then I was AFK
</div>
