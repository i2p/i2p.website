---
title: "I2P Dev Meeting - February 19, 2013"
date: 2013-02-19
author: "KillYourTV"
description: "I2P development meeting log for February 19, 2013."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> dg, hottuna, inscrutus, KillYourTV, lillith, Meeh, str4d</p>

## Meeting Log

<div class="irc-log">
20:25:01  &lt;KillYourTV&gt; Perhaps I'm in the minority but I think that if there are going to be meetings they *really* should start on time.
20:25:24  &lt;inscrutus&gt; Indeed
20:26:31  &lt;KillYourTV&gt; Not starting until 30-60 minutes after it _should have started_ looks bad, especially to outsiders that may be watching from the relayed networks.
20:27:21  &lt;inscrutus&gt; I don't remember who chaired last time.  Are we waiting for him?
20:28:11  &lt;lillith&gt; ^this
20:28:28  &lt;lillith&gt; inscrutus: dg is often late
20:32:22  &lt;hottuna&gt; KillYourTV, yeah. I agree
20:33:01  &lt;lillith&gt; we could just start without dg, if anyone wants to just go for it
20:36:27  &lt;inscrutus&gt; I believe ipv6 was one topic left over from last meeting...
20:50:56  &lt;dg&gt; It was.
20:51:07  &lt;dg&gt; Most of it can't be done without zzz though, or str4d
20:52:25  * dg apologizes for being late - been out of it
20:52:40  &lt;dg&gt; Topics were/are:
20:52:43  &lt;dg&gt; * Syndie documentation (lillith)
20:52:43  &lt;dg&gt; * Mailing list (meeh)
20:52:43  &lt;dg&gt; * Feeds (str4d)
20:52:43  &lt;dg&gt; * Thoughts (anyone)
20:52:54  &lt;dg&gt; Meeh, lillith?
20:53:03  &lt;dg&gt; if you guys aren't here.. shit.
21:18:01  &lt;Meeh&gt; dg: I'm here now, sorry
21:18:20  &lt;dg&gt; np, is lillith?
21:18:23  &lt;dg&gt; I'm sorry, not you ;)
21:18:27  &lt;Meeh&gt; dunno
21:18:49  &lt;inscrutus&gt; lillith was, about 45m ago
21:18:49  &lt;lillith&gt; i am
21:19:08  &lt;inscrutus&gt; I stand corrected
21:20:10  &lt;dg&gt; \o
21:20:22  &lt;dg&gt; Hi all, sorry for delay
21:20:42  &lt;dg&gt; lillith is going to be speaking about Syndie doumentation
21:21:35  &lt;lillith&gt; is this my cue or are we having a full schedule first?
21:21:49  &lt;dg&gt; I've given the full one ;)
21:21:52  &lt;dg&gt; maybe it was lost
21:21:59  &lt;dg&gt; &lt;+dg&gt; Topics were/are:
21:21:59  &lt;dg&gt; &lt;+dg&gt; * Syndie documentation (lillith)
21:21:59  &lt;dg&gt; &lt;+dg&gt; * Mailing list (meeh)
21:21:59  &lt;dg&gt; &lt;+dg&gt; * Feeds (str4d)
21:21:59  &lt;dg&gt; &lt;+dg&gt; * Thoughts (anyone)
21:21:59  &lt;dg&gt; &lt;+dg&gt; Meeh, lillith?
21:22:02  &lt;dg&gt; &lt;+dg&gt; if you guys aren't here.. shit.
21:22:21  &lt;lillith&gt; ahh okay :)
21:22:24  &lt;inscrutus&gt; I saw it via kytv relay only....
21:23:10  &lt;lillith&gt; right well since zzz and others have put so much work into syndie, i feel it is a shame that it is still so unused
21:24:01  &lt;lillith&gt; and since the gui is.. challenging for a begginer, i thought it may be a good idea to write/update the docs
21:24:47  &lt;lillith&gt; so now myself, KillYourTV, and aargh are working on a wiki
21:25:17  &lt;lillith&gt; hosted at *i don't have the b32 handy*
21:25:19  &lt;dg&gt; Wiki for exclusively Sundie?
21:25:23  &lt;dg&gt; s/Sundie/Syndie
21:25:54  &lt;lillith&gt; since it is a wiki i/we would appreciate if everyone could have a look and fix it if needed
21:26:01  &lt;lillith&gt; yes
21:26:16  &lt;Meeh&gt; I'm trying to make a map over the syndie archives at http://wiki.meeh.i2p/doku.php?id=syndie:known_archives
21:26:24  &lt;iRelay&gt; Title: syndie:known_archives [wiki.meeh.i2p] (at wiki.meeh.i2p)
21:26:43  &lt;lillith&gt; so, please do have a play on syndie and report back on f you feel the beginners guide is suitable for a short intro
21:26:50  &lt;dg&gt; A column for default or not may be useful
21:27:25  &lt;dg&gt; alright :)
21:27:44  &lt;lillith&gt; the current documentation is ufinished, so anthing we do is an improvement
21:28:27  &lt;lillith&gt; also KillYourTV: i assume the plan is to export the wiki into the official website at some point, is that correct and if so who do i need to speak to?
21:30:10  &lt;lillith&gt; Meeh: a column for filtering/blocking policy might be useful too
21:30:25  &lt;Meeh&gt; ok, but I don't know what to fill in there
21:31:03  &lt;dg&gt; ask around I suppose
21:31:26  &lt;Meeh&gt; gonna do it
21:31:53  &lt;dg&gt; thanks for giving Syndie some love lillith
21:32:01  &lt;lillith&gt; i'l tell you mine later, not here now :)
21:32:31  &lt;inscrutus&gt; lillith: is this the wiki b32? http://fomjl7cori4juycw55kdlczpgzzhme6nox6zykokuiov6t5lxhvq.b32.i2p/user_guide/
21:32:34  &lt;iRelay&gt; Title: Syndie Handbook (at fomjl7cori4juycw55kdlczpgzzhme6nox6zykokuiov6t5lxhvq.b32.i2p)
21:33:02  &lt;lillith&gt; dg: it's actually pretty good, even if it is buggy.
21:33:23  &lt;lillith&gt; inscrutus: it is :) thanks
21:33:54  &lt;KillYourTV&gt; lillith: yes, once finished all documentation will ultimately end up on the 'official' syndie site   (for now http://www.syndie.i2p/wiki/ will redirect to the wiki page)
21:33:57  &lt;iRelay&gt; Title: Syndie Documentation Project (at www.syndie.i2p)
21:35:14  &lt;inscrutus&gt; Ok, what's next, dg?
21:35:17  &lt;lillith&gt; so unless anyone else has anything to say on this, i can *baf* this topic :)
21:35:20  &lt;dg&gt; Meeh
21:35:31  &lt;dg&gt; (with mailing list)
21:35:43  &lt;dg&gt; lillith: thx :) - I'm enjoying reading the introduction
21:36:02  &lt;dg&gt; Meeh: Want to take the floor?
21:36:41  &lt;Meeh&gt; IIRC I'm waiting for weltende because I needed access to the router console for creating tunnels for making mailing list available inside i2p
21:37:42  &lt;Meeh&gt; and, we need to start to use it
21:38:36  &lt;inscrutus&gt; Is it a -dev mailinglist?  Or just general i2p?
21:38:39  &lt;dg&gt; zzz and user said they were going to hold off until an inner-i2p presence appeared
21:38:42  &lt;Meeh&gt; both
21:38:56  &lt;inscrutus&gt; ok
21:39:04  &lt;Meeh&gt; ok
21:39:25  &lt;Meeh&gt; weltende: any chance for creating tunnels for the mailing list?
21:39:25  &lt;Meeh&gt; soon
21:41:01  &lt;lillith&gt; Meeh: what is the intention for the mailing list? as in compared to zzz.i2p or irc or syndie
21:41:37  &lt;str4d2&gt; apologies for absence - internet fail
21:42:00  &lt;dg&gt; str4d :)
21:42:11  &lt;Meeh&gt; personaly, I'm unsure.. But it seemed liked we came to the conclution that we should start with the mailing list stuff again, as other open source projects do...
21:42:33  &lt;Meeh&gt; don't remember which meeting it was
21:43:08  &lt;inscrutus&gt; Maybe it would be a good idea to mirror the mailing list to Syndie or vice versa.  To avoid fragmentation
21:43:23  &lt;str4d2&gt; I'm unavailable in about 15 mins, btw
21:44:10  &lt;Meeh&gt; I like your idea inscrutus
21:44:41  &lt;str4d2&gt; (and can't make this meeting time in future)
21:45:11  &lt;str4d2&gt; that's a nice ideqla
21:45:14  &lt;str4d2&gt; idea*
21:45:53  &lt;dg&gt; It was suggested in the past, I believe it was going to be a part of Syndie anyhow.
21:46:04  &lt;dg&gt; Meeh: Anything more?
21:46:15  * lillith- really needs to remember to plug my laptop in.... reading scrollback on sighup...
21:47:11  &lt;Meeh&gt; no not really, I need to talk with weltende first
21:47:22  &lt;lillith-&gt; inscrutus: that was my next suggestion :)
21:47:41  &lt;dg&gt; Alright.
21:47:44  &lt;inscrutus&gt; :)
21:47:51  &lt;lillith-&gt; i think we could be 'dog-fooding' a little more
21:48:18  &lt;dg&gt; lillith-: ?
21:48:40  &lt;lillith-&gt; about the mailing list/syndie mirrorring
21:48:55  &lt;dg&gt; I'm not familiar with that expression
21:49:47  &lt;lillith-&gt; ahh the dog food principle of open source projects is, basically, use your own software
21:49:50  &lt;inscrutus&gt; it means to use your own product(s).  It comes from a dogfood maker whose ceo i believe ate his company's own dogfood to prove it's good
21:50:01  &lt;dg&gt; oh.. to eat our own dog food
21:50:04  &lt;dg&gt; I agree
21:50:15  &lt;lillith-&gt; if we expect others to use it, we should too
21:50:35  &lt;str4d2&gt; Mmm
21:51:01  &lt;str4d2&gt; My problem with Syndie is that I have NFI how to use it
21:51:12  &lt;dg&gt; I need to check it out again
21:51:12  &lt;dg&gt; Anyhow..
21:51:12  &lt;dg&gt; str4d2: You ok to do feeds now? After $next_thing, perhaps a new meeting time should be discussed. Not everyone is here though..
21:51:15  &lt;str4d2&gt; The interface is not very intuitive.
21:51:18  &lt;lillith-&gt; str4d2: have you looked at the docs?
21:51:57  &lt;str4d2&gt; Somewhat, but we shouldnt expect users to all do that
21:52:00  &lt;lillith-&gt; dg: surely that is the reason we need a new time...
21:52:30  &lt;dg&gt; kind of. zzz and others are missing due to IRL issues too though - which makes it harder to agree on a new time which works for everyone.
21:53:01  &lt;str4d2&gt; and I'm busynow, sorry
21:53:01  &lt;lillith-&gt; dg: we could have a new temporary time and revisit it in a few weeks.
21:53:38  &lt;lillith-&gt; tues 8.00 isn't great for dg, str4d2, or me
21:55:51  &lt;dg&gt; it doesn't :-/
22:03:14  &lt;lillith-&gt; has everyone gone to sleep or is that the end of the meeting?
22:03:29  &lt;dg&gt; Apparently sleep..
22:03:36  &lt;dg&gt; We'll open a thread on zzz.i2p about it?
22:03:39  * lillith- picks up the baffer menacingly
22:03:42  &lt;inscrutus&gt; I'm here, just don't have anything to add to meeting times
22:03:49  &lt;dg&gt; It's just us three.
22:05:25  * dg *bafs the meeting closed
22:05:28  &lt;lillith-&gt; okay well if no-one has anything to add then i'l do the honours
22:05:51  * lillith- *bafs* the meeting
22:06:10  &lt;lillith-&gt; damn you got there first ;)
</div>
