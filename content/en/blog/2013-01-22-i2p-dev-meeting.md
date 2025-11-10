---
title: "I2P Dev Meeting - January 22, 2013"
date: 2013-01-22
author: "hottuna_"
description: "I2P development meeting log for January 22, 2013."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> christoph1, dg, eche|on, hottuna, lillith, RN, str4d, zzz</p>

## Meeting Log

<div class="irc-log">
20:07:05  &lt;hottuna_&gt; Alright, meeting-time?
20:07:27  &lt;str4d&gt; o/
20:08:28  &lt;RN-&gt; tjink so
20:08:41  &lt;hottuna_&gt; eche|on, zzz, dg: ping
20:09:46  &lt;hottuna_&gt; let's wait until 20:15 and see if dg shows up.
20:10:21  &lt;RN-&gt; did everyone read zzz homework assignment?
20:10:36  &lt;hottuna_&gt; yepyep
20:11:28  &lt;RN-&gt; was over my head
20:11:31  &lt;str4d&gt; Okay, looks like the three meeting topics are ugha.i2p, the website revamp and the crypto. Anything else we want to cover?
20:11:50  &lt;hottuna_&gt; I think that is more than enough
20:11:58  &lt;str4d&gt; Alright:
20:12:01  &lt;RN-&gt; read it tho
20:12:04  &lt;str4d&gt; (0) Say Hi.
20:12:11  &lt;str4d&gt; (1) Ugha.i2p
20:12:18  &lt;str4d&gt; (2) Website revamp
20:12:29  &lt;str4d&gt; (3) Crypto discussion
20:12:32  &lt;str4d&gt; (0) Say Hi.
20:12:35  &lt;str4d&gt; Hi!
20:13:00  &lt;RN-&gt; hi
20:13:07  &lt;hottuna_&gt; hello everybody!
20:14:44  &lt;RN-&gt; we waiting 4 zzz and ech?
20:15:21  &lt;hottuna_&gt; I think we can manage until the crypto part
20:15:27  &lt;str4d&gt; eche|on was around an hour ago; zzz tends to speak when he needs to.
20:15:27  &lt;RN-&gt; guess they r at end...
20:15:49  &lt;hottuna_&gt; weltende, welterde, eche|on: ping, re new website
20:15:52  &lt;hottuna_&gt; altight
20:15:58  &lt;RN-&gt; anyone got the baffer?
20:15:58  &lt;str4d&gt; And everyone else can turn up when they do ^_^
20:16:05  &lt;str4d&gt; (1) Ugha.i2p
20:16:05  &lt;hottuna_&gt; So.. ugha?
20:16:08  &lt;str4d&gt; o/
20:16:39  &lt;zzz&gt; here, standing by until 3), if it's reasonbly fast
20:16:52  &lt;hottuna_&gt; Alright, I posted a content-request page last week
20:16:52  &lt;hottuna_&gt; syndie/imule content was requested
20:16:59  &lt;hottuna_&gt; and has as far as I can see been submitted
20:17:18  * str4d can
20:17:29  &lt;str4d&gt; 't actually load ugha right now =P
20:17:41  &lt;str4d&gt; Do we know who runs ugha?
20:18:04  &lt;hottuna_&gt; I don't
20:18:23  &lt;hottuna_&gt; do we have any further ideas about what to change/add to ugha?
20:18:31  &lt;str4d&gt; Because it would be useful to get some proper spam protection if possible.
20:18:38  &lt;eche|on&gt; we do partly know/guess who runs it. but it will not be disclosured here
20:18:47  &lt;eche|on&gt; and owner did not respond yet
20:18:54  &lt;dg&gt; Okay, hey
20:18:57  &lt;str4d&gt; eche|on: fair enough.
20:18:57  &lt;eche|on&gt; ugha.i2p was cleaned from spam
20:19:09  &lt;str4d&gt; eche|on: how much work was that?
20:19:12  &lt;eche|on&gt; and I added a site about iMule and syndie, KillYourTV added a bit more
20:19:30  &lt;eche|on&gt; spam? a lot, it was&gt;200 or even&gt;400 spam messages to be removed
20:19:38  &lt;eche|on&gt; they appeared in 2 years time
20:20:09  &lt;str4d&gt; And just manually removed?
20:20:24  &lt;hottuna_&gt; did it appear over the inproxy?
20:20:35  &lt;dg&gt; I was wondering this
20:20:50  &lt;dg&gt; sorry for being late although I managed to get here :)
20:20:53  &lt;eche|on&gt; yea, str4d, click each spam site, click delete site, click yes, I want to remove, click next spam site
20:21:08  &lt;eche|on&gt; and IMHO it is on INproxy.
20:21:27  &lt;eche|on&gt; yeah, it is
20:21:58  &lt;eche|on&gt; http://ugha.i2p.to/RecentChanges
20:22:01  &lt;hottuna_&gt; alright, maybe it shouldnt be accessible over the inproxy?
20:22:15  &lt;RN-&gt; so... set read omly for inproxy?
20:22:15  &lt;eche|on&gt; maybe someone want to count the "delete" pictures ;-)
20:23:34  &lt;hottuna_&gt; is it possible to notify the admin via the the wiki?
20:23:45  &lt;eche|on&gt; guess not
20:23:48  &lt;hottuna_&gt; a read-only via inproxy rule would probably be good
20:23:51  &lt;hottuna_&gt; ok
20:24:06  &lt;hottuna_&gt; eche|on, but you know who? you could do it?
20:24:28  &lt;eche|on&gt; I cannot do anything on it, I am just a user like anyone else
20:24:43  &lt;dg&gt; The person obviously is not active.
20:24:46  &lt;dg&gt; So.. maybe still no.
20:24:51  &lt;eche|on&gt; all I can do is asking tino (i2p.to owner) to block it.
20:25:18  &lt;hottuna_&gt; is blocking it entirely an acceptable solution?
20:26:01  &lt;eche|on&gt; yes
20:26:05  &lt;dg&gt; not long term
20:26:30  &lt;RN-&gt; I agree with dg
20:26:44  &lt;eche|on&gt; it is a wiki. It needs active administration to remove unwatned content
20:26:44  &lt;hottuna_&gt; i think blocking it is acceptable.. since it only is of use to people who are already using i2p
20:26:57  &lt;eche|on&gt; but as we also have active spammers inside of I2P....
20:26:57  &lt;zzz&gt; tino's not going to take action unless the owner requests it
20:27:04  &lt;zzz&gt; at least, he shouldnt.
20:27:41  &lt;hottuna_&gt; eche|on, could you contact the owner?
20:27:52  &lt;eche|on&gt; currently I visit ugha.i2p daily and remove the spam
20:28:15  &lt;eche|on&gt; hottuna_: I did contact via IRC and email already. now it is time for person to react.
20:28:38  &lt;zzz&gt; if it continues to be an embarassment we can take it out of the router console, whether we have a replacement or not
20:28:41  &lt;eche|on&gt; you know, weve seen same problem with forum.i2p already. thats the problem inside of I2P
20:28:48  &lt;hottuna_&gt; regarding blocking from i2p.to?
20:29:02  &lt;eche|on&gt; regarding active admin jobs on it
20:29:25  &lt;hottuna_&gt; ok
20:29:58  &lt;hottuna_&gt; anyway, if you manage to get some response, ask about blocking
20:31:01  &lt;RN-&gt; tino is not only inproxy anymore
20:31:43  &lt;dg&gt; Yeah.
20:32:01  &lt;str4d&gt; Aside from the spam issue, is there any content that ugha should have/needs updated&gt;
20:32:29  &lt;dg&gt; Yes.
20:32:29  &lt;eche|on&gt; I had a look at the russian wiki. Thats a nice nice nice one
20:32:44  &lt;str4d&gt; From /Requests - "More advanced i2p config options and explanations." - hottuna_ you already added some of these, right?
20:32:44  &lt;eche|on&gt; it is really filled with good content and structured. but in russian.
20:32:44  &lt;str4d&gt; eche|on: link?
20:32:53  &lt;hottuna_&gt; what's the url for the russian wiki?
20:33:12  &lt;hottuna_&gt; str4d, yes. And I found a similar list on echelon.i2p
20:33:24  &lt;eche|on&gt; if I find it again...
20:34:10  &lt;eche|on&gt; imho rus.i2p
20:34:56  &lt;eche|on&gt; but more explanation about advanced config is nice
20:34:59  &lt;str4d&gt; Ooh, that *is* a nice wiki.
20:36:25  &lt;eche|on&gt; to sad I am a bit out of time, but if I get the chance, I do a few bits
20:36:32  &lt;RN-&gt; looks like it's using the same nice clean interface as cake why TV on his Cindy page
20:36:42  &lt;dg&gt; is it in english?
20:36:45  &lt;RN-&gt; I'll have to leave in about 10 minutes or less catch up with the rest of the meeting on my scroll back...
20:38:21  &lt;str4d&gt; Are there any other major points about ugha.i2p that need raising?
20:38:36  &lt;hottuna_&gt; no.
20:38:47  &lt;hottuna_&gt; I updated the request site
20:39:50  &lt;str4d&gt; The /I2pRfc page could do with updates, if it is/was ever planned to be authoritative (though the website is probably the better place for specs).
20:40:26  &lt;dg&gt; ugha.i2p has a lot of content which could be added or update
20:40:33  &lt;dg&gt; it seems to have more information about i2p's past and old tech documents than anywhere else
20:41:19  &lt;str4d&gt; Summary so far: spam is (currently) under control but needs active policing; there are numerous old pages that would be good to get updated (a good task for people who like writing).
20:41:34  &lt;hottuna_&gt; agreed.
20:41:41  &lt;str4d&gt; And if possible, the wiki should block edits from the inproxy.
20:41:56  &lt;str4d&gt; Anything else to add before we move on?
20:41:59  &lt;dg&gt; Is that all for the wiki then?
20:42:02  &lt;dg&gt; I don't think so
20:42:52  &lt;str4d&gt; dg: you want to do the honors? ^_^
20:43:11  &lt;dg&gt; Alright :3
20:43:15  &lt;dg&gt; thx
20:43:38  * str4d gets to talk lots in the next topic anyway =D
20:43:53  &lt;dg&gt; Okay, so the website revamp - I feel that the new design headed by str4d (he's doing the backend mostly but some CSS changes) brings a fresh look to i2p and can help refresh people's perspective and first impressions of it
20:44:00  &lt;dg&gt; The current one is rather stale, etc, etc..
20:44:11  &lt;dg&gt; I think that we should look into what needs completing in order to push it live
20:44:34  &lt;str4d&gt; What *must* be completed before pushing live:
20:44:37  &lt;dg&gt; Minor issues can be worked on when it's out there so the blockers we need to consider here?
20:44:48  &lt;str4d&gt; - translation tagging
20:45:01  &lt;str4d&gt; (well, not *must* but most at the very least)
20:45:17  &lt;str4d&gt; - checking that all site-internal links are updated and valid
20:45:36  &lt;str4d&gt; That's basically it.
20:45:56  &lt;hottuna_&gt; how is translation tagging done?
20:46:07  &lt;str4d&gt; I've already started on that, and have covered most of the site pages (if you leave out the docs, which are large on their own)
20:46:22  &lt;dg&gt; Latter isn't too hard. There's tools for it IIRC but I can go around clicking (take one for the team ;) if push comes to shove.
20:46:33  &lt;dg&gt; Explain translation tagging?
20:46:40  &lt;str4d&gt; hottuna_: Jinja2 template tags
20:46:40  &lt;str4d&gt; And gettext PO files
20:47:05  &lt;str4d&gt; &lt;h2&gt;{% trans %}A Gentle Introduction to How I2P Works{% endtrans %}&lt;/h2&gt;
20:47:08  &lt;str4d&gt; &lt;p&gt;{% trans -%}
20:47:08  &lt;str4d&gt; I2P is a project to build, deploy, and maintain a network supporting secure and anonymous
20:47:08  &lt;str4d&gt; communication. People using I2P are in control of the tradeoffs between anonymity, reliability,
20:47:11  &lt;str4d&gt; bandwidth usage, and latency. There is no central point in the network on which pressure can be
20:47:11  &lt;str4d&gt; exerted to compromise the integrity, security, or anonymity of the system. The network supports
20:47:11  &lt;str4d&gt; dynamic reconfiguration in response to various attacks, and has been designed to make use of
20:47:11  &lt;str4d&gt; additional resources as they become available. Of course, all aspects of the network are open and
20:47:11  &lt;str4d&gt; freely available.
20:47:15  &lt;str4d&gt; {%- endtrans %}&lt;/p&gt;
20:48:17  &lt;str4d&gt; The tagged blocks get extracted into a messages.pot which can then be translated like the routerconsole is.
20:48:36  &lt;str4d&gt; That's another task that I think *must* be done before launch:
20:48:57  &lt;str4d&gt; - Migrate old translated pages (e.g. /how_intro_fr) to PO files
20:49:53  &lt;hottuna_&gt; ok
20:49:56  &lt;hottuna_&gt; whats the mtn repo name?
20:50:04  &lt;hottuna_&gt; alright
20:50:08  &lt;str4d&gt; That one I can't do much about =P I've migrated one page as a test, but I can't verify the accuracy of the old translations (especially as there was nothing to keep things in sync between the static pages)
20:50:12  &lt;str4d&gt; i2p.www.revamp
20:51:02  * str4d starts up the test site again
20:52:33  &lt;str4d&gt; Okay, http://vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p/en/ is back up.
20:52:44  &lt;iRelay&gt; Title: I2P Anonymous Network (at vekw35szhzysfq7cwsly37coegsnb4rrsggy5k4wtasa6c34gy5a.b32.i2p)
20:52:59  &lt;str4d&gt; Something else I've done is added mobile support to the website - you can see it by narrowing your browser window below 768px
20:53:34  &lt;dg&gt; What are we doing about blog/
20:53:34  &lt;dg&gt; ?
20:53:45  &lt;str4d&gt; dg: what do you mean?
20:53:52  &lt;str4d&gt; (In what regard?)
20:54:04  &lt;dg&gt; Who will be blogging and how will we set it up? When will we blog also? :)
20:54:43  &lt;str4d&gt; At present the blog just contains the (old) release posts and the (much older) status posts.
20:54:54  &lt;str4d&gt; At the very least there will be the release posts as normal.
20:55:50  &lt;str4d&gt; That's a later issue though -  we need to actually get the site finished first!
20:56:09  &lt;hottuna_&gt; agreed
20:56:20  &lt;str4d&gt; Ticket #807 does have a few things in it which would be good to get done, but are not blockers
20:56:32  &lt;iRelay&gt; http://trac.i2p2.i2p/ticket/807 - (accepted enhancement) - Revamp of website
20:56:44  &lt;str4d&gt; They are somewhat spread out through the ticket, but some are:
20:57:02  &lt;str4d&gt; - fill out /about/glossary
20:57:21  &lt;str4d&gt; - improve blog/meetings layout and styling
20:58:17  &lt;str4d&gt; - fix or replace the theme
20:58:36  &lt;hottuna_&gt; re translation tagging: is """{{ _('Friends of I2P') }}""" tagable in a straight forward manner
20:59:03  &lt;str4d&gt; hottuna_: That already is tagged.
20:59:26  &lt;hottuna_&gt; just curious about syntax
20:59:29  &lt;str4d&gt; (That's the more compact notation)
20:59:39  &lt;hottuna_&gt; aah
20:59:42  &lt;str4d&gt; {{ }} inserts the result of the contained Python method
20:59:53  &lt;str4d&gt; _() is the gettext call in Python
21:00:00  &lt;str4d&gt; (well, the one that is imported into Jinja2
21:00:03  &lt;str4d&gt; )
21:00:19  &lt;hottuna_&gt; thanks
21:00:34  &lt;str4d&gt; {% trans %}{% endtrans %} is a more verbose tag, but it's the Jinja2 tag and supports any content between the tags.
21:00:49  &lt;str4d&gt; (whereas the _() one can't contain e.g. '
21:00:52  &lt;hottuna_&gt; what is left to tag?
21:01:13  &lt;str4d&gt; hottuna_: check the mtn log for details of what has been tagged, but IIRC:
21:01:44  &lt;str4d&gt; - get-involved/guides (I've tagged ides and dev-guidelines there)
21:01:55  &lt;str4d&gt; - misc/*
21:01:58  &lt;str4d&gt; - docs/*
21:02:09  &lt;str4d&gt; And then any blog posts that we want translated.
21:03:06  &lt;str4d&gt; (I've already migrated and tagged the 0.9.4 and 0.9.3 posts, and future posts can be tagged as well; earlier ones can be tagged as/when people can be bothered)
21:04:17  &lt;str4d&gt; Okay, we do need to get a move on in the meeting.
21:05:18  &lt;str4d&gt; Summary: site revamp is almost ready, help is appreciated getting the rest of the site tagged for translation and url-checked (can be done simultaneously) (thanks hottuna_ for offering to help (I assume that's what you are doing?))
21:05:45  &lt;str4d&gt; And other text/layout changes are appreciated but not blocking.
21:06:31  &lt;str4d&gt; Oh: and if anyone wants to get started on translating the pages (using the old translated pages as reference or for copy-paste), *please do so*.
21:06:34  &lt;str4d&gt; Anything else?
21:06:49  &lt;hottuna_&gt; ill have a look at tagging
21:07:48  &lt;str4d&gt; hottuna_: thanks. Leave get-involved/guides to me, as I've already started in there.
21:08:43  &lt;str4d&gt; dg: are you keeping an eye on the meeting (timeliness)?
21:09:02  &lt;dg&gt; oh, sorry
21:09:14  &lt;dg&gt; So we're done with website/
21:09:41  &lt;dg&gt; Crypto time :-D
21:10:16  &lt;dg&gt; Let me dig up the relevant topics
21:10:16  &lt;dg&gt; One moment
21:11:28  &lt;dg&gt; http://zzz.i2p/topics/1328 + http://zzz.i2p/topics/715
21:11:38  &lt;iRelay&gt; Title: zzz.i2p: Meeting [22nd January] (at zzz.i2p)
21:12:10  &lt;dg&gt; TL;DR: We need to be discussing which components of the i2p router need to be changed in order of priority (or as zzz put it, "to talk generally about which uses are more vulnerable than others"
21:12:10  &lt;dg&gt; )
21:12:17  &lt;dg&gt; (for the DSA change)
21:12:45  &lt;dg&gt; It's an apt time to discuss any other crypto changes that could be thrown in but right now, we should stick to what zzz suggested as it's a masssive rabbithole
21:12:52  &lt;hottuna_&gt; like noted in the tor cipher migration document we should strive to do changes where they are the most important and not necessarily the easiest
21:13:26  &lt;dg&gt; (https://gitweb.torproject.org/torspec.git/blob_plain/34ecac0fbac7f476bfcbf813767721fada62c17e:/proposals/ideas/xxx-crypto-migration.txt)
21:15:55  &lt;hottuna_&gt; in my mind the most important areas are those using potentially weak ciphers for longterm keys
21:16:39  &lt;dg&gt; hottuna_: I'm no crypto expert (and as such I'll stay out unless I know something) but aren't the longterm keys also the keys which could cause a flag day?
21:17:12  &lt;hottuna_&gt; changing most ciphers would cause a flag day
21:17:31  &lt;dg&gt; I was thinking all destinations being fucked
21:17:38  &lt;dg&gt; so yeah
21:17:41  &lt;hottuna_&gt; well basically
21:18:03  &lt;hottuna_&gt; i dont see a way around destinations being wrecked
21:19:03  &lt;hottuna_&gt; Im don't have a list of places where long-term keys are used
21:19:22  &lt;hottuna_&gt; but such a list and the corresponding cipher used should be created
21:21:04  &lt;str4d&gt; Agreed. We should also rank their perceived vulnerability.
21:21:11  &lt;str4d&gt; (This would make a good wiki page on Trac)
21:21:19  &lt;hottuna_&gt; yes.
21:22:02  &lt;hottuna_&gt; we should also create a list of ciphers that have been proven as safe (by the test of time) and are otherwise viable for us
21:22:17  &lt;str4d&gt; Section 2 of the Tor page basically applies to us as well.
21:22:20  &lt;hottuna_&gt; that list should include asymetric
21:22:55  &lt;zzz&gt; sounds good
21:23:11  &lt;hottuna_&gt; asymmetric* encryption, symmetric encryption, signatures and hmac ciphers that we trust
21:23:49  &lt;zzz&gt; how_cryptography page is a good reference
21:24:32  &lt;hottuna_&gt; str4d, did you start a wiki page or should I?
21:24:40  * str4d is doing so now
21:25:00  &lt;str4d&gt; /Crypto/CurrentSpecs sound alright?
21:25:09  &lt;str4d&gt; (For the summary table)
21:25:09  &lt;hottuna_&gt; sure
21:25:16  &lt;zzz&gt; DSA is a nice place to start analysis because it's easy to understand, and it's on the surface the weakest
21:26:15  &lt;hottuna_&gt; yes
21:27:01  &lt;hottuna_&gt; as for what is used where and what time periods which keys are used for I dont know much
21:28:56  &lt;zzz&gt; the OP on http://zzz.i2p/topics/715 has a list
21:29:03  &lt;zzz&gt; ~8 places we use DSA
21:29:05  &lt;iRelay&gt; Title: zzz.i2p: DSA 1024/160 Replacement (at zzz.i2p)
21:29:40  &lt;hottuna_&gt; the one with the longest validity is routerinfo?
21:30:23  &lt;str4d&gt; || '''Aspect/Location''' || '''Cipher used''' || '''Cipher details''' || ''' Perceived vulnerability''' || '''Comments'''
21:30:30  &lt;str4d&gt; Anything else that needs to go into the table?
21:30:30  &lt;zzz&gt; maybe dest. which isn't listed.
21:31:12  &lt;zzz&gt; theres both a dest key and a leaseset key I think the dest signs the leaseset and the leaseset key is unused
21:31:38  &lt;hottuna_&gt; str4d, validity period
21:32:24  &lt;zzz&gt; wouldnt be the end of the world to have a RI flag day but throwing out all 2500 in hosts.txt is another story
21:32:38  &lt;str4d&gt; Hmm... maybe the Perceived vulnerability / validity should be in a separate table then.
21:33:07  &lt;zzz&gt; datagrams is a problem, dests is a problem
21:33:22  &lt;hottuna_&gt; throwing out hosts is a huge issue. but it is also the most vulnerable key in my mind
21:34:37  &lt;zzz&gt; for each case we have to go farther though. not just how easy to break but what's the threat model / consequence.
21:35:08  &lt;hottuna_&gt; yes. maybe link to a separate page for each case?
21:35:26  &lt;str4d&gt; http://trac.i2p2.i2p/wiki/Crypto/CurrentSpecs now exists and has some basic content
21:35:33  &lt;iRelay&gt; Title: Crypto/CurrentSpecs  I2P (at trac.i2p2.i2p)
21:36:09  &lt;zzz&gt; and put that in perspective gven the size of the net, etc. e.g., we currently have a guy that claims he can shutdown an eepsite for 23 1/2 hours a day.
21:37:13  &lt;hottuna_&gt; christoph1, ?
21:37:25  &lt;dg&gt; Yikes.
21:37:28  &lt;str4d&gt; Mmm.
21:37:35  &lt;dg&gt; How does that work?
21:37:58  &lt;hottuna_&gt; eclipse attack on our floodfills
21:38:01  &lt;christoph1&gt; use enough precomputed routerinfos, put 10 bad nodes near the target hash block lookup
21:38:20  &lt;lillith&gt; why is it not 24 hours?
21:38:35  &lt;christoph1&gt; because midnight is a bit tricky
21:38:46  &lt;christoph1&gt; you can use another 10 to put in place for tomorrow
21:39:05  &lt;christoph1&gt; but there's still a period around the keyspace rotation where things are unstable
21:39:22  &lt;lillith&gt; so the router gets half an hour where the floodfills are uncertain?
21:39:33  &lt;christoph1&gt; (client can hit one of the good nodes by chance because it doesn't know all attackers jet
21:39:52  &lt;str4d&gt; The keys for the next day can be known in advance, so positioning malicious nodes could be planned in advance, no?
21:39:59  &lt;christoph1&gt; jep
21:40:22  &lt;christoph1&gt; still it seems around rotation it is somewhat unstable
21:40:49  &lt;str4d&gt; Anyway, this is somewhat off-track for this topic (sorry christoph1)
21:41:05  &lt;christoph1&gt; ack
21:43:08  &lt;str4d&gt; Okay, does anyone want to work on getting http://trac.i2p2.i2p/wiki/Crypto/CurrentSpecs filled out?
21:43:14  &lt;iRelay&gt; Title: Crypto/CurrentSpecs  I2P (at trac.i2p2.i2p)
21:43:26  &lt;zzz&gt; dg, please keep us on track, not drag us off it :)
21:43:42  &lt;hottuna_&gt; str4d, yeah. I just managed to log in :P
21:44:01  &lt;str4d&gt; Maybe we should quickly clarify what exactly we want on that page (my column headings are rather generic)
21:44:36  &lt;dg&gt; zzz: sory ;)
21:44:59  &lt;str4d&gt; First table: a summary of the crypto used in the router. Name, validity period, vulnerability... key length? Prime strength?
21:44:59  &lt;zzz&gt; m yfault too
21:45:48  &lt;str4d&gt; Second table: a list of every point in the router where crypto is used. Location and cipher name (of course). Usage details? What is important to know here?
21:46:27  &lt;str4d&gt; We can probably elaborate on separate pages for the second table if necessary (link the location name to a subpage)
21:47:41  &lt;hottuna_&gt; str4d, added subpage
21:48:06  &lt;str4d&gt; IMHO this should be a page that someone can glance at and understand the current state-of-play (whereas the site docs are the full specs)
21:48:32  &lt;str4d&gt; hottuna_: ah, I get what you mean by validity period now.
21:48:39  &lt;hottuna_&gt; :)
21:50:20  &lt;str4d&gt; hottuna_: there's already an entry for destinations - LeaseSet signing
21:50:29  &lt;hottuna_&gt; oh
21:50:29  &lt;hottuna_&gt; sorry
21:50:36  &lt;str4d&gt; (For the DSA part at least - I think you're thinking there of the encryption)
21:51:56  &lt;str4d&gt; Also, I'd call it "Security timescale" rather than "Validity period"
21:52:38  &lt;hottuna_&gt; yep
21:52:38  &lt;zzz&gt; FYI for everybody else - every RI and Dest has two keys, one for encryption and one for signing
21:53:11  &lt;hottuna_&gt; ok
21:53:11  &lt;hottuna_&gt; why?
21:53:32  &lt;zzz&gt; ElG was deemed far too slow for signing
21:54:44  &lt;str4d&gt; This might be a silly question, but how are the two keys "linked" verifiably?
21:55:23  &lt;zzz&gt; for both RI and Dest, the Hash covers both keys + the (usually null) Certificate
21:55:23  &lt;hottuna_&gt; a public key is derived from the private key
21:55:51  &lt;zzz&gt; change any of the 3 and you change the hash.
21:56:13  &lt;str4d&gt; Ah, k (you mean the Destination hash?)
21:56:23  &lt;str4d&gt; (i.e. the B64)
21:56:26  &lt;zzz&gt; yes
21:56:53  &lt;str4d&gt; Okay... the problem with upgrading the Destination crypto makes much more sense now...
21:56:59  &lt;zzz&gt; and for Dests, change any of the 3 and you need a new hosts.txt entry
21:58:34  &lt;zzz&gt; and (hint) non-null certs may be the path to upgrades w/ (partial) compatibility, i.e. not breaking gravity. That's what's covered further down in topic 715
21:59:39  &lt;str4d&gt; Yeah - that enables both to work alongside each other.
22:00:09  &lt;str4d&gt; But it still means that the end-to-end crypto for the old Destinations is untouched.
22:00:52  &lt;str4d&gt; The point where the Dest crypto key is most important is the leg between the OPEP and IBGW, right?
22:01:26  &lt;zzz&gt; not sure
22:01:53  &lt;zzz&gt; other complication is there used to be two layers of end-to-end crypto, one in the router and one in the client, and some keys are now unused
22:02:32  &lt;zzz&gt; ditto w/ signing keys... one was for LS revocation and is unused
22:02:46  &lt;zzz&gt; so that's another opportunity, maybe
22:03:29  &lt;str4d&gt; http://www.i2p2.i2p/how_intro seems to indicate that the ElGamal/AES+SessionTags is used for end-to-end router encryption.
22:04:37  &lt;zzz&gt; crypto is much harder to discuss than signing. theres the ElG wrapping the AES and the Tags, together with the DH exchange.
22:05:35  &lt;str4d&gt; Yes. But as far as e.g. LeaseSets go, we probably need to discuss both in tandem, no?
22:05:46  &lt;zzz&gt; I'd suggest not even trying to get into the crypto side today.
22:05:53  &lt;str4d&gt; Not today, no.
22:06:00  &lt;zzz&gt; maybe, maybe not
22:06:03  &lt;str4d&gt; So, back on topic *derp*
22:06:30  &lt;zzz&gt; you change one key, you change the hash. But as the Tor doc says, don't try to change everything just because you're changing one thing
22:06:33  &lt;str4d&gt; What is the issue with Datagram signing?
22:07:12  &lt;zzz&gt; it's using our signing algorithm, i.e. DSA. Which we use to sign everything. (including suds)
22:07:54  &lt;zzz&gt; which also isn't on the list on topic 715, and might be the longest-lived key of all
22:09:04  &lt;str4d&gt; Right, but the specific problem I'm guessing with Datagrams is ensuring that routers can still talk to each other
22:09:04  &lt;str4d&gt; ?
22:10:00  &lt;zzz&gt; right. change signing and you break all RI and LS lookup, and all signed end-to-end communication
22:10:51  &lt;zzz&gt; because almost everything is signed
22:11:41  &lt;str4d&gt; So really the only way to move forward with upgrading the signing algorithm is to ensure that every place it is used can handle multiple signing algorithms?
22:12:27  &lt;str4d&gt; The problem then becomes knowing what versions are supported by a router (and the partitioning problems from the Tor doc are relevant here).
22:12:30  &lt;zzz&gt; but then every dest would need two sets of tunnels, one for old and one for new, afaik
22:12:49  &lt;zzz&gt; there's two kinds of compatibility to consider.
22:13:19  &lt;str4d&gt; That's a good point&gt;_&lt;
22:13:42  &lt;zzz&gt; 1) "network" compatibility, i.e. can the RIs and LSs be stored and retrieved, can msgs get thru tunnels, even if the ffs or participants are down-rev;
22:14:21  &lt;zzz&gt; 2) end-to-end compatibility, can A talk to B. For that, seems like both A and B need to support the same things
22:15:43  &lt;str4d&gt; 2) is "easy" to handle for direct router-to-router communication, as the router versions are public knowledge. What about end-to-end communication?
22:17:24  &lt;zzz&gt; the other thing is an RI has a whole Properties in it, we can put whatever flags we want in there
22:17:27  &lt;str4d&gt; Where would a router need to look to determine if another router (such as an eepsite server) supports the new signatures?
22:17:30  &lt;zzz&gt; nothing like that for LS
22:18:01  &lt;zzz&gt; certs is the magic
22:18:48  &lt;zzz&gt; in a cert we can spec both crypto and signing algo, and store the extra bytes if it doesnt fit in the first 384
22:18:59  &lt;zzz&gt; again, that's the topic 715 stuff
22:19:53  &lt;zzz&gt; the cert has to start at byte 385 to not break 1)
22:20:54  &lt;zzz&gt; is that about enough for today? got out of this what you wanted?
22:21:09  &lt;hottuna_&gt; i think this is a beginning
22:21:34  &lt;hottuna_&gt; more specific issues and solutions cna be discussed and the wiki page used as an aid
22:23:50  &lt;str4d&gt; zzz: it's a good start - thank you =)
22:24:24  &lt;zzz&gt; lots of work ahead...
22:24:39  &lt;str4d&gt; Yes, but we have to start somewhere ^_^
22:24:54  &lt;hottuna_&gt; str4d, pushed tags for monotone.html
22:25:05  &lt;zzz&gt; I had one more topic for the mtg but only if welt welterde weltende is around
22:25:26  &lt;str4d&gt; hottuna_: the one under get-involved/guides? I'll drop the ones I'd started putting in then ^_^
22:25:37  &lt;hottuna_&gt; yes
22:26:00  &lt;hottuna_&gt; alright, are we done then?
22:26:11  &lt;dg&gt; I'd say so?
22:26:15  &lt;str4d&gt; I'd like to add a random point:
22:26:18  * dg had nothing to chime in with
22:26:21  &lt;dg&gt; not a crypto god
22:27:08  &lt;str4d&gt; I'd like to congratulate sponge on his efforts with Android - stock I2P now successfully runs on Android devices.
22:27:46  &lt;str4d&gt; And initial reports seem to indicate better performance and lower battery usage than I2P-Android
22:27:53  &lt;hottuna_&gt; that's quite the feat
22:28:04  &lt;hottuna_&gt; well done sponge
22:28:16  &lt;hottuna_&gt; i've gotta go now
22:28:23  &lt;hottuna_&gt; dg, will you strat the thread for next week?
22:28:27  &lt;dg&gt; spogne has done extremely well
22:28:56  &lt;dg&gt; Will do. Topics? Seems crypto needs to be a recurring topic for the next few weeks. :)
22:29:03  &lt;dg&gt; I should be here on time next week also
22:29:47  &lt;str4d&gt; If we can get the revamp tagged by then, we could potentially go live with the new site (though I would prefer to get actual translations in first)
22:30:18  &lt;str4d&gt; (Also depends on welterde being around)
22:30:25  &lt;hottuna_&gt; str4d, i think actual translations will take a very long time
22:30:52  &lt;hottuna_&gt; alright, nn ppl
22:30:59  &lt;str4d&gt; hottuna_: complete translations, yes. But there are already-translated pages (see www.i2p2/pages/translations) which would be quick to migrate.
22:31:07  &lt;str4d&gt; (For people who understand the language)
22:31:14  &lt;str4d&gt; o/ hottuna_
22:31:45  * str4d *baf*s the meeting closed.
</div>
