---
title: "I2P Dev Meeting - August 01, 2006"
date: 2006-08-01
author: "jrandom"
description: "I2P development meeting log for August 01, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, cervantes, Complication, frosk, jrandom, polecat, tethra, void</p>

## Meeting Log

<div class="irc-log">
16:02 &lt;jrandom&gt; ok, might as well get this rolling
16:03 &lt;jrandom&gt; hi, pre-meeting notes posted up at http://dev.i2p.net/pipermail/i2p/2006-August/001304.html
16:03 &lt;jrandom&gt; rather than have me essentially reread that message to y'all here, lets just skip to our standard ??? section -
16:04 &lt;jrandom&gt; anyone have anything they want to bring up and discuss?
16:04 &lt;@cervantes&gt; eerm
16:04  * cervantes scurries to read the post
16:05 &lt;+Complication&gt; With regard to network status, all fine over here...
16:05 &lt;+Complication&gt; But one question (actually relaying from forum) about the NTCP transport,
16:06 &lt;+Complication&gt; namely, does it sound likely that activating it could cause someone CPU load issues (they were on XP)?
16:06 &lt;@cervantes&gt; I have to say I've actually been seeing lower CPU usage since switching over :)
16:07 &lt;jrandom&gt; well, you can't *deactivate* it (unless you've been reading the source code and know the magic incantation ;)
16:07 &lt;+Complication&gt; The person who spoke of this problem (can't easily repeat it, and no big CPU use here) mentioned that their experience of high CPU usage seemed to correlate with NTCP
16:07 &lt;jrandom&gt; so, i assume they mean not accepting inbound ntcp connections
16:07 &lt;+polecat&gt; NTCP causes my router to instantly clock the CPU, and I repeated it twice before manually having to alter the config file to get a working router again.
16:07 &lt;jrandom&gt; (while still using outbound ntcp connections)
16:07 &lt;+Complication&gt; (over here it's only a tiny bit up from usual levels, and that's likely because of pumping *way* more data)
16:08 &lt;+Complication&gt; ( http://forum.i2p/viewtopic.php?t=1815 )
16:08 &lt;jrandom&gt; when you establish an ntcp connection, you do a heavyweight crypto calculation (or three)
16:08 &lt;jrandom&gt; if you are accepting inbound ntcp connections, you may get lots of inbound attempts at once, since there are hundreds of i2p routers out there
16:09 &lt;jrandom&gt; polecat: that wasn't ntcp's fault, it was the fault of a bad ntp server in the ntp pool
16:09 &lt;+polecat&gt; Yes.  So I can't handle that myself, apparantly.
16:09 &lt;jrandom&gt; (thanks to cervantes for tracking down that ntp server and getting the pool folks to !thwap 'em :)
16:10 &lt;jrandom&gt; ((and Complication for making it so we avoid those crazy bastards in the future :))
16:10 &lt;@cervantes&gt; heh I think their server watchdogs only work on weekdays ;-)
16:10 &lt;+Complication&gt; Well, the current avoidance is pretty limited
16:10 &lt;@cervantes&gt; http://www.pool.ntp.org/scores/216.52.237.153
16:11 &lt;+Complication&gt; I hope to get something more paranoid coded eventually
16:11 &lt;+polecat&gt; Oh, so enabling NTCP won't clock the CPU anymore?
16:11 &lt;jrandom&gt; (it never did polecat, 'twas a coincidence ;)
16:12 &lt;+Complication&gt; "clock" in which particular sense?
16:12 &lt;jrandom&gt; (see cervantes' link)
16:12  * polecat clocks Complication upside the head.
16:12 &lt;@cervantes&gt; whatcha smoking polecat
16:12 &lt;+Complication&gt; :P
16:12 &lt;+polecat&gt; Er, I mean, stole all clock cycles.  :)
16:13 &lt;+Complication&gt; If it jumped 30 seconds forward or backward, it could have lost many, many sessions, and resorted to all kinds of heavy, heavy crypto
16:13 &lt;+Complication&gt; That could steal plenty of CPU cycles, I think
16:13 &lt;+Complication&gt; Indeed, perhaps the person in the forum actually saw the same, and mis-correlated it? Have to ask...
16:13 &lt;jrandom&gt; ah.. well, bursts of valid inbound ntcp connections will cause bursts of cpu, while outbound-only ntcp will only try to talk to so many new ntcp peers at a time
16:14 &lt;jrandom&gt; there is nothing wrong with not enabling inbound ntcp.  
16:15 &lt;@cervantes&gt; Complication: the server was corrected mid-monday, so it might be worth seeing if they've had issues since then
16:15 &lt;jrandom&gt; ok, anyone else have something they want to discuss?
16:16 &lt;+Complication&gt; cervantes: indeed, could be worth a try
16:16 &lt;@cervantes&gt; I've had reports of some folk still losing leases periodically... is that a known problem?
16:16 &lt;+void&gt; how much does the ntcp implementation differ from ssu?
16:17 &lt;+polecat&gt; How do we tell if we lose leases?
16:18 &lt;jrandom&gt; void: there's a slightly higher per-message andwidth overhead in ntcp (though perhaps offset by the OS's likely-more-efficient reliable transmission implementation)
16:18 &lt;+Complication&gt; polecat: tunnels.jsp will show no tunnels for a particular tunnel pool (e.g. "shared clients")
16:18 &lt;jrandom&gt; cervantes: aye, our tunnel build success rates still aren't where they need to be
16:18 &lt;+void&gt; polecat: the router console says so
16:18 &lt;+Complication&gt; And like void says, the left sidebar of the console will tell so
16:19 &lt;+polecat&gt; I get those "No leases" messages a lot... that's what you mean, right?
16:19 &lt;@cervantes&gt; yup
16:20 &lt;+polecat&gt; That's usually what kills my IRC connection.  Thought it was normal!
16:21  * jrandom cringes
16:24 &lt;+tethra&gt; lol ;)
16:25 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:25 &lt;@cervantes&gt; jrandom: have you made any progress on syndie lately or have you had your hands full with ntcp/bug fixing/ISP hunting/bicycling ?
16:27 &lt;+tethra&gt; any news on feedspace, or should i just go to their eepsite?
16:28 &lt;jrandom&gt; when the live net hit the shitter i pushed syndie to the side.  but with the net moving back on track again, syndie has been reclaiming my time, and I hope to have a small cli system out shortly (with focused guis coming after that, based on user feedback)
16:28 &lt;jrandom&gt; (the implemented swt gui is in pretty good shape, but its probably best to start off with the cli to adjust expectations)
16:29  * jrandom hasn't heard any news on feedspace
16:29 &lt;@cervantes&gt; cool
16:29 &lt;jrandom&gt; frosk: any word?  :)
16:29 &lt;+polecat&gt; I'm glad you're working on syndie again.  The new one does sound pretty promising. Any thoughts on ACL for stuff such as deleting blogs from a node, or doing administrative account-independant tasks?
16:30 &lt;@cervantes&gt; &lt;jrandom&gt; DELETE FROM messages WHERE postedOn &lt;NOW()-14*24*60*60;
16:31 &lt;jrandom&gt; local archives will likely remain essentially trusted (since if you can access the local archive db, you can change the file however you want)
16:32 &lt;jrandom&gt; however, for shared blogs, yeah there's a whole set of crypto structures in place for authenticating and / or authorizing posts and changes
16:33 &lt;jrandom&gt; (but there'll be a way for people to view 'unauthorized' posts as well, but they'll be very much off to the side)
16:33 &lt;+polecat&gt; I'm sure once someone floods syndicates with thousands of giant blog posts, the technique to physically delete posts will be perfected.
16:34 &lt;+tethra&gt; heheh
16:35 &lt;jrandom&gt; physical deletion is trivial, its the question of what posts to accept in the first place ;)
16:36 &lt;jrandom&gt; (i have no interest in making syndie into a movie distriution platform, etc)
16:36 &lt;+polecat&gt; One cannot be sure of what one is accepting, until a sample has been accepted.  I envision something like allowing only a whitelist of blogs, and allowing new IDs on a trial basis before adding them, insta-deleting on spam betrayal.
16:36 &lt;jrandom&gt; aye
16:37 &lt;+polecat&gt; I'm more interested in its application for colluding streams of conversation together: we could make a BBS that had no central server, just a tag in common!
16:37 &lt;jrandom&gt; (manually allowing new ids, manually kickbanning ids that flood, etc)
16:37 &lt;jrandom&gt; there's even inherent support for that in the crypto polecat :)
16:37 &lt;+polecat&gt; Possibly a moderator signing approved messages for the BBS, and people collecting those approval lists from the moderator's blog.
16:38 &lt;+polecat&gt; Ooh excellent.
16:38 &lt;@frosk&gt; jrandom: been working on gui stuff lately, but it's been hard to combine with starting a new job :(
16:39  * cervantes contacts Human Resources to get frosk fired
16:40 &lt;jrandom&gt; ah cool, hopefully once syndie is out there pushing kludged http syndication we'll tempt you on it again ;)
16:40 &lt;@frosk&gt; at least my boss follows i2p development now :)
16:40  * jrandom waves to frosk's boss
16:40 &lt;@frosk&gt; oh yes, i'm still determined (damn it!) :)
16:40 &lt;jrandom&gt; (gives frosk more time off, we need 'im!)
16:41 &lt;@cervantes&gt; hopefully he won't read about how you've been posting classified company information onto your syndie blog
16:41 &lt;bar&gt; gui is good, we like gui. you're forgiven.
16:41 &lt;+Complication&gt; Hehe :)
16:41 &lt;@frosk&gt; it's weird to walk into his office and catch him reading syndie :)
16:41 &lt;jrandom&gt; hah awesome
16:42 &lt;+polecat&gt; Congratulations frosk, even if you get fired in shame and infamy, at least you showed one more person how cool syndie can be.
16:43 &lt;@frosk&gt; hehe yeah
16:43 &lt;+tethra&gt; haha
16:44 &lt;@frosk&gt; the gui (in swt) is/will be a testbed for all things feedspace, to kickstart it
16:44 &lt;jrandom&gt; r0x0r
16:45 &lt;+void&gt; jrandom: perhaps you should cross-post everything that goes onto the mailing lists to syndie as well?
16:45 &lt;jrandom&gt; we should totally merge it in with the syndie swt gui (basic paradigm is a browser, though not displaying html pages in the tabs)
16:46 &lt;+polecat&gt; That'd be nice.  I can't seem to get the mailing list anymore.
16:46 &lt;jrandom&gt; void: it'd be pretty easy for someone to write up a small shell script to pipe procmail into the syndie CLI
16:46 &lt;@cervantes&gt; are these fancy swt gui's tied into the applications? or are they tops for cli executables or use tcp etc etc 
16:46 &lt;@frosk&gt; that makes sense
16:46 &lt;jrandom&gt; (iirc there's a post in my blog a while back explaining how to use the syndie cli to insert posts)
16:47 &lt;+polecat&gt; Currently one can make RSS feeds to feed into syndie, though it's kind of cludgy still.
16:47 &lt;jrandom&gt; cervantes: jdbc in event handlers, inline with jni and msvc callouts, of course ;)
16:47  * jrandom ducks
16:48 &lt;+polecat&gt; Microsoft Visual Classes?
16:49 &lt;@cervantes&gt; jrandom: so anything that can talk SQL can administer syndie then
16:49 &lt;jrandom&gt; (from syndie's perspective, all of the functionality is basically implemented in lots of tiny cli apps which just update the jdbc database, and there's an swt ui to browse around the db)
16:51 &lt;+polecat&gt; And since the database has two interfaces, JDBC, and SQL, a client communicating in either protocol can screw with syndie.
16:51 &lt;jrandom&gt; cervantes: well, yes and no - there's a good portion of the database thats encrypted, so not all fields are readable
16:51 &lt;+void&gt; will the current web interface still be there?
16:51 &lt;jrandom&gt; (jdbc == sql)
16:51 &lt;jrandom&gt; void: no
16:51 &lt;+polecat&gt; I thought you said that JDBC wasn't a stupid human readable protocol?
16:51 &lt;+Complication&gt; jdbc == java database interface, perhaps a bit similar to odbc
16:51 &lt;jrandom&gt; ((jdbc ~= sql))
16:51 &lt;+Complication&gt; Something you talk SQL over
16:52 &lt;+void&gt; jrandom: what will happen to syndie.i2p/syndiemedia.i2p.net?
16:52 &lt;+polecat&gt; Oh.  Well I never liked SQL anyway, for the record.
16:52 &lt;@cervantes&gt; jrandom: so it's best to create a top for syndieTools (tm) than to try and leech the data yourself
16:53 &lt;jrandom&gt; void: time will tell.  likely they'll 1) serve as syndie's website/eepsite, 2) serve as a public archive of posts to syndicate with, and eventually, when a web interface is written, 3) serve up a web interface
16:53 &lt;+polecat&gt; Why not submit bytecode as database queries, instead of archaic COBOL statements?
16:53 &lt;jrandom&gt; aye cervantes
16:53 &lt;jrandom&gt; !lart polecat
16:54 &lt;+void&gt; hehehe
16:54 &lt;+polecat&gt; Ah, my secret weakness.
16:54 &lt;@cervantes&gt; * you have 6 larts left in your inventory, there is a door to the north and an unconsious polecat on the floor
16:54 &lt;jrandom&gt; cervantes: thats actually cli app #3 (extracting individual posts, which comes after app #2, listing individual posts (after #1, creating individual posts, and after #0, managing nyms)))
16:54 &lt;jrandom&gt; lol
16:54 &lt;+tethra&gt; haha
16:55 &lt;+Complication&gt; feature proposal: instead of bytecode, why not submit live $agency agents as database queries? ;P
16:56 &lt;+Complication&gt; Would be far easier to validate for safety :P
16:56 &lt;@cervantes&gt; jrandom: gotcha
16:56 &lt;+tethra&gt; do they act like carrier pigeons under the right climate, Complication? 
16:56 &lt;+Complication&gt; tethra: only if you manage to push them through the TCP stack intact :P
16:56 &lt;+polecat&gt; Yes, database queries over CPP!
16:57 &lt;+Complication&gt; I imagine that getting wrinkled in TCP might corrupt them
16:58 &lt;+Complication&gt; (sorry, should really keep jokes to #i2p-chat, but sometimes can't help)
16:58  * cervantes senses a baff is soon approaching
16:58 &lt;+Complication&gt; database queries as shellcode?
16:59 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:59 &lt;+polecat&gt; http://www.blug.linux.no/rfc1149/ &lt;- we could tunnel i2p over this, really.
16:59  * Complication would rather stick with SQL
17:00 &lt;+void&gt; jrandom: do other langauges than java have libraries for hsqldb databases?
17:01 &lt;+Complication&gt; Oo would seem likely to, since they seem to use it
17:01 &lt;+void&gt; looks like a "no" to me
17:01 &lt;+void&gt; oh, hmm
17:01 &lt;@cervantes&gt; openoffice uses it so I would guess so
17:01 &lt;+Complication&gt; But I'm not sure what OpenOffice is written in
17:01 &lt;jrandom&gt; not that i know of.  but someone could run syndie against another jdbc database (mysql, oracle, etc)
17:01 &lt;jrandom&gt; oo uses java
17:02 &lt;+void&gt; what exactly does openoffice use this database for?
17:02 &lt;+Complication&gt; But seems to only partially use it
17:02 &lt;jrandom&gt; void: for pdf generation and for their access-like database app
17:02 &lt;jrandom&gt; (among other things)
17:02 &lt;+Complication&gt; Given that it recommends an external JRE
17:02 &lt;+void&gt; okay
17:03 &lt;+void&gt; it's a pain in the ass to write portable sql though
17:03 &lt;+Complication&gt; if one doesn't do triggers or stored procedures, shouldn't be a big pain, though
17:04 &lt;jrandom&gt; eh, its not that bad, and easy to externalize
17:04 &lt;+void&gt; especially when aiming oracle ;)
17:05 &lt;jrandom&gt; actually, hsqldb supports pl/sql ;)
17:06 &lt;bar&gt; are there any other plans for this database, such as for stats, peer profiles, netdb..?
17:06 &lt;jrandom&gt; no, this is syndie only
17:06 &lt;bar&gt; ok
17:07 &lt;jrandom&gt; (though when we ship the hsqldb code, we can use it in i2p 'for free')
17:07 &lt;@cervantes&gt; since syndie is not an I2P application, just an application that can run over I2P correct?
17:07 &lt;jrandom&gt; aye cervantes, there is no dependency upon i2p
17:07 &lt;+Complication&gt; Good to keep Syndie portable, since it might have other transports besides I2P
17:07 &lt;bar&gt; right
17:08 &lt;+Complication&gt; However, I take it wouldn't be difficult to run many hsqldb instances on the same machine
17:08 &lt;+Complication&gt; So if other apps would need it, it seems they could just use it
17:08 &lt;jrandom&gt; trivial, and 0-cost if you just use the in-jvm dataase
17:08 &lt;+Complication&gt; (use their own instance, preferably)
17:10 &lt;+void&gt; there's no jdbc driver for sqlite?
17:11 &lt;jrandom&gt; dunno, never used it
17:11 &lt;+void&gt; ah, looks like there is *something*
17:13 &lt;jrandom&gt; ok, anything else for the meeting?
17:13 &lt;jrandom&gt; if not...
17:13  * jrandom dinws up
17:13  * jrandom steps back
17:13  * jrandom winds up
17:13  * jrandom *baf*s the meeting closed
</div>
