---
title: "I2P Dev Meeting - December 26, 2006"
date: 2006-12-26
author: "jrandom"
description: "I2P development meeting log for December 26, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> bar, Complication2, gloin, hottuna, jrandom</p>

## Meeting Log

<div class="irc-log">
15:02 &lt;jrandom&gt; 0) hi
15:02 &lt;jrandom&gt; 1) Net status
15:02 &lt;jrandom&gt; 2) Syndie 1.000a
15:02 &lt;jrandom&gt; 3) ???
15:02 &lt;jrandom&gt; 0) hi
15:02  * jrandom waves
15:02 &lt;jrandom&gt; weekly status notes up at http://dev.i2p.net/pipermail/i2p/2006-December/001324.html
15:03 &lt;jrandom&gt; lets jump on in to 1) net status
15:03 &lt;Complication2&gt; Oh, I entirely forgot it's a Tuesday
15:03 &lt;jrandom&gt; things are going pretty well, as mentioned, though my router finally had a restart after a 45 day uptime
15:04 &lt;jrandom&gt; (but frankly, i'd be quite happy if we could consistently get 1+ month uptimes :)
15:04 &lt;Complication2&gt; Net status is a bit flakier than before for me, but that's because one of my I2P routers is having a recurring (once about 10 days) problem
15:04 &lt;Complication2&gt; Other router is capable of pulling one-month uptimes, but it's not a very high-traffic router
15:05 &lt;Complication2&gt; Rather modest, in fact
15:05 &lt;jrandom&gt; stats.i2p has been showing a slightly reduced build success rate in the past week, but that may just be seasonal
15:07 &lt;+fox&gt; &lt;hottuna&gt; Ive been getting some weird wrapper log messages
15:07 &lt;+fox&gt; &lt;hottuna&gt; INFO   | jvm 1    | 2006/12/26 01:00:00 | 2006-dec-26 00:00:00 org.mortbay.util.RolloverFileOutputStream removeOldFiles
15:07 &lt;+fox&gt; &lt;hottuna&gt; INFO   | jvm 1    | 2006/12/26 01:00:00 | INFO: Log age 2006_09_26.request.log
15:07 &lt;+fox&gt; &lt;hottuna&gt; INFO   | jvm 1    | 2006/12/26 01:00:00 | 2006-dec-26 00:00:00 org.mortbay.util.RolloverFileOutputStream removeOldFiles
15:07 &lt;jrandom&gt; irc is still doing pretty well though, even with 3 hop tunnels
15:07 &lt;jrandom&gt; oh interesting hottuna, sounds like some verbose commons-logging stuff
15:08 &lt;jrandom&gt; (jetty uses their own logger, not ours)
15:08 &lt;+fox&gt; &lt;hottuna&gt; nothing to worry about then .. 
15:08 &lt;+fox&gt; &lt;hottuna&gt; but still ahven been running my router due to BW starvation
15:09 &lt;jrandom&gt; starvation being "not enough bw for i2p", or "i2p using too much bw"?
15:11 &lt;+fox&gt; &lt;hottuna&gt; Well, both but since Im running i2p to donate bw the first alternative fits me best
15:11 &lt;jrandom&gt; ah heh, ok
15:11 &lt;+fox&gt; &lt;hottuna&gt; I just started syndie for the first time and Im feling a bit overwhelmed, dont really know where to begin
15:11 &lt;+fox&gt; &lt;hottuna&gt; nice touch with adding the standard archive though
15:13 &lt;jrandom&gt; thanks :)  there's lots that we need to do to reduce the overwhelmed sensation, though lets do that in our jump to 2) Syndie 1.000a :)
15:13 &lt;jrandom&gt; 1.000a is out, download and enjoy!
15:14 &lt;jrandom&gt; out of box experience should basically be: install, start, "add the standard archive", tell Syndie to sync with the standard archive "now" (then hit save), and it'll start pulling messages
15:15 &lt;jrandom&gt; it'll add a line to that table below the save button, one per message and one per forum - right clicking on messages & forums brings them up, or you can browse via the Forum-&gt;Read all menu
15:15 &lt;bar&gt; congratulations on the syndie alpha release, you've been working long and hard on this. respect.
15:16 &lt;Complication2&gt; Same here. Impressive database and quite promising interface. :)
15:16 &lt;+fox&gt; &lt;hottuna&gt; Im using syndie right now and reading the epic syndie and i2p direction post
15:16 &lt;gloin&gt; btw, build.xml contains a hardcoded value: build.xml:    &lt;property name="swt.win32" value="../swt-I20061214-1445-win32-win32-x86/swt.jar" /&gt;
15:16 &lt;jrandom&gt; thanks, there's lots to do to get syndie where it needs to be, but its a start
15:17 &lt;+fox&gt; &lt;hottuna&gt; there is much work to be done on the usability front but still you have come a long way
15:17 &lt;jrandom&gt; gloin: aye, 3 of 'em (swt.win32, swt.osx, and swt.linux32) - they're only used for "ant dist"
15:18 &lt;Complication2&gt; does "ant" default to "ant clean jar", by the way?
15:18  * Complication2 checks
15:18 &lt;jrandom&gt; hottuna: thats where you (and y'all :) come in - my head is deep in the innards of syndie, so its often hard for me to get the right perspective for making syndie more usable
15:19 &lt;jrandom&gt; i need your opinions, feedback, and suggestions to improve things
15:19 &lt;Complication2&gt; Aha, dependency check and jar
15:19 &lt;Complication2&gt; (without the cleanup part)
15:19 &lt;jrandom&gt; right Complication2, no 'clean' by default
15:21 &lt;gloin&gt; does "ant dist" build versions for linux, win32 and so on?
15:21 &lt;jrandom&gt; gloin: yeah, building installers, .exe files, etc
15:22 &lt;jrandom&gt; if you just want to build and run syndie for your own use, "ant jar" and copy the lib/syndie.jar to your syndie install, or "ant run" to launch it in place
15:23 &lt;Complication2&gt; darn, I overlooked the "run" target then
15:23 &lt;jrandom&gt; (specifying the necessary -Dswt.dir=/blah flags, or placing them in the (new) file nbproject/private/private.properties as swt.dir=/blah/)
15:23 &lt;Complication2&gt; Cooked up a run.sh :D
15:24 &lt;Complication2&gt; two-liner, though, so nothing time-consuming
15:24 &lt;jrandom&gt; that works too :)
15:24 &lt;Complication2&gt; Yep, "ant run" worked nicely
15:24 &lt;gloin&gt; ant run seem to work, the install linux32.exe complains about missing swt.
15:24 &lt;Complication2&gt; Just tested
15:26 &lt;jrandom&gt; hmm gloin, and swt.jar exists in the installed syndie lib dir?
15:27 &lt;gloin&gt; yes.
15:28 &lt;jrandom&gt; and you're running "java -jar /some/path/to/that/syndie/bin/syndie.exe"?  or do you mean the linux installer?
15:29 &lt;gloin&gt; the installer was fine. it created the syndie-1.000a directory.
15:31 &lt;gloin&gt; Exception in thread "main" java.lang.UnsatisfiedLinkError: no swt-pi-gtk-3235 in java.library.path
15:33 &lt;Complication2&gt; One little question (I'm testing out the Linux binary)
15:33 &lt;jrandom&gt; hmm, did it create the libswt-pi-gtk-3235.so in /tmp/ gloin?
15:33 &lt;Complication2&gt; Where to obtain the public key "393F2DF9"?
15:33 &lt;jrandom&gt; thats a good question... 
15:34 &lt;gloin&gt; who? when?
15:34 &lt;gloin&gt; at the moment, theres no  libswt-pi-gtk-3235.so in /tmp/
15:35 &lt;jrandom&gt; gloin: the new swt (3.3M4) shipped with syndie extracts the native libs to /tmp/ when it can't find them
15:36 &lt;jrandom&gt; gloin: can you run (cd ~/syndie-1.000a/ ; java -cp lib/syndie.jar:lib/swt.jar:lib/hsqldb.jar syndie.gui.SWTUI ) and see if that finds them?
15:36 &lt;jrandom&gt; Complication2: it'll be up on the various keyservers and the website after the meeting
15:37 &lt;Complication2&gt; Thanks :)
15:37 &lt;jrandom&gt; (its on my keyrings which aren't accessible from my windows box)
15:37 &lt;Complication2&gt; Meanwhile, I found out using more conventional means that my download of the binary *did* abort early
15:37  * Complication2 fetches the end again
15:38 &lt;gloin&gt; no. Maybe I rebuild the the installer
15:39 &lt;jrandom&gt; gloin: could you check the swt.jar to make sure it contains the libswt-pi-gtk-3235.so (jar tvf lib/swt.jar)?
15:40 &lt;jrandom&gt; in any case, we'll keep on debugging as things come up
15:41 &lt;gloin&gt; it's not in it.
15:41 &lt;jrandom&gt; thats about it for syndie 1.000a - there will of course be updates over time, and they'll be announced in meetings or mails
15:42 &lt;jrandom&gt; (there are much smaller downloads for upgrading syndie than the full 4-5+MB ones - see syndie.i2p.net/downloads/)
15:42 &lt;+fox&gt; &lt;hottuna&gt; whats is the i2p syndie archives url on the i2p network ?
15:43 &lt;jrandom&gt; gloin: could you priv msg me the jar tvf output?
15:43 &lt;jrandom&gt; hottuna: http://archive.syndie.i2p/
15:43 &lt;+fox&gt; &lt;hottuna&gt; thank you
15:45 &lt;jrandom&gt; (note that archive.syndie.i2p / syndie.i2p.net:8080 are just instances of syndie with the built-in HTTP server running)
15:45 &lt;+fox&gt; &lt;hottuna&gt; oh :) wicked :)
15:45 &lt;+fox&gt; &lt;hottuna&gt; oh btw the syndie clock doesnt match the clock on my system
15:46 &lt;jrandom&gt; so, anyone can run their own syndie archive and let people sync off 'em - just give them a link to your archive (which you can do via irc/html/etc, or in syndie itself with an 'archive link'/reference)
15:46 &lt;jrandom&gt; syndie clock?
15:46 &lt;+fox&gt; &lt;hottuna&gt; or the time stamps on messages in syndie
15:47 &lt;+fox&gt; &lt;hottuna&gt; wait a second. . now they seem to be right..
15:47 &lt;+fox&gt; &lt;hottuna&gt; a restart later
15:52 &lt;gloin&gt; how do I build a headless archive server? I assume that the import.cgi is not 'supported' anymore?
15:53 &lt;jrandom&gt; right, import.cgi is incompatible with the latest - you can run a headless server with a normal syndie install by running syndie "--cli", causing it to run the text engine. 
15:55 &lt;jrandom&gt; the integrated http server can be run from the text engine via the 'httpserv' command (http://syndie.i2p.net/manual.html#general_httpserv )
15:55 &lt;gloin&gt; thanks a lot.
15:56 &lt;jrandom&gt; if you're going to be firing up your archive again, i should be thanking you :)
15:57 &lt;gloin&gt; puh.. even with a gui, it looks complicated :)
15:58 &lt;jrandom&gt; aye, y'all've got your work cut out for you - help make it usable and useful :)
15:59 &lt;jrandom&gt; we'll have lots more to cover as people start kicking the tires and issues start coming up, but for the time being, feel free to dig in, post away, and see whats going on
15:59 &lt;jrandom&gt; shimmying on over to 3) ???, anyone have anything else to bring up for the meeting?
16:00 &lt;Complication2&gt; Tested the Linux binary installer, runs nicely
16:00 &lt;Complication2&gt; It's only curious that when it tried creating a shortcut in the KDE menu, the shortcut ended up in the group "Development"
16:00 &lt;Complication2&gt; Along with NetBeans and stuff
16:01 &lt;Complication2&gt; I might be mistaken, but I think I recall it writing that it was going to try creating a group called Syndie...
16:01 &lt;jrandom&gt; ah, yeah.  izpack and the java packagers/installers are still working through the kde integration
16:02 &lt;Complication2&gt; Anyway, small detail
16:02 &lt;Complication2&gt; But wanted to mention just in case
16:02 &lt;jrandom&gt; it /should/ create a Syndie group, but as you can see, the kde menu doesn't have per-app folders (it has categories of apps, and then per-app folders)
16:02 &lt;jrandom&gt; hopefully to be fixed when izpack fixes it (its on their radar)
16:03 &lt;Complication2&gt; Right
16:03 &lt;Complication2&gt; Either way, the shortcut appeared, and the uninstaller shortcut appeared too
16:03 &lt;jrandom&gt; wewt
16:03 &lt;Complication2&gt; And the uninstalled worked nicely too (used it too since I typically compile from sources)
16:03 &lt;Complication2&gt; =uninstaller
16:04 &lt;bar&gt; i have two questions, slightly related to each other
16:04 &lt;bar&gt; 1. any plans yet on when to nuke the old syndie?
16:04 &lt;bar&gt; 2. could we have an i2p gateway, syndie.i2p, to syndie.i2p.net, or would that perhaps collide with the old syndie infrastructure?
16:05 &lt;Complication2&gt; On 2, I think it currently would collide
16:06 &lt;jrandom&gt; hmm, i actually haven't thought about that much.  i'm tempted to say "nuke it, move everyone to the new syndie now now now" :)
16:07 &lt;Complication2&gt; ...going to "http://archive.syndie.i2p" through "localhost:4444"
16:07 &lt;bar&gt; the reason i'm asking is, it's sometimes a bit of a pain having to use squid.i2p to access the syndie web pages
16:07 &lt;jrandom&gt; ah, understood.  ok, i can redirect syndie.i2p to point to syndie.i2p.net, and old-syndie users can still use syndiemedia.i2p
16:09 &lt;bar&gt; loverly :)
16:09 &lt;Complication2&gt; oh, you meant the web pages
16:10 &lt;Complication2&gt; I thought you meant the archive :)
16:10 &lt;bar&gt; correct Complication2, sorry for not being clear on that
16:10 &lt;gloin&gt; the own forum is the own identity?
16:11 &lt;Complication2&gt; There's definitely a default identity / pseudonym created in a new Syndie instance
16:11 &lt;Complication2&gt; I'm not sure if it auto-creates a forum
16:11 &lt;jrandom&gt; gloin: every identity has a forum (and every forum is owned by an identity)
16:12 &lt;jrandom&gt; a forum, in syndie, is just a public key
16:12 &lt;jrandom&gt; (as is an author)
16:12 &lt;Complication2&gt; I've forgotten how I went about doing it, and it was in October with the text interface anyway, I think :)
16:12 &lt;jrandom&gt; ((in the database and code, they're both called 'channels', but the ui talks about forums and authors/nyms))
16:13 &lt;bar&gt; on the topic of closing down the old syndie, may i suggest something along the lines of "keeping it online for another month but closing the archive for new posts, along with leaving an informative note"
16:14 &lt;gloin&gt; the gui let me create forums only. Does that  means, when I a want that you can post in my forum I authorize the jrandom forum and not the jrandom person?
16:15 &lt;Complication2&gt; Or perhaps even leaving it open for a short while after posting the note, so if someone desperately needs it at this stage (gasp!) they can exchange some data for a short while still
16:15 &lt;jrandom&gt; gloin: forums and identities are the same thing - when you create a new forum, you craete a new ientity (and to authorize jrandom the person to post in your forum, authorize jrandom's forum)
16:15 &lt;jrandom&gt; seems reasonable Complication2 & bar
16:17 &lt;jrandom&gt; gloin: this stuff is definitely not-obvious, and we need to do a lot of work on making it easier
16:21 &lt;Complication2&gt; Oops, I've not noticed multiple suggestions for I2Phex tuning by striker on the old Syndie
16:21  * Complication2 makes local copies
16:23 &lt;jrandom&gt; :)  the old syndie will still remain accessible at syndiemedia.i2p/ and syndie.i2p.net:8000/ 
16:23 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
16:25 &lt;gloin&gt; In the forum configuration I can set the privay level (all/auth/passphrase). But with each post I can set it, too. Which counts?
16:27 &lt;jrandom&gt; both count, though for the time being, i'd recommend keeping the forum privacy as 'public' (since i havent written up the gui for passphrase protected forums yet, only passphrase protected messages)
16:27 &lt;jrandom&gt; the forum privacy covers the forum's metadata (links to other sites, bundled keys, etc), while individual messages have their own policy
16:33 &lt;jrandom&gt; (syndie.i2p --&gt; syndie.i2p.net as of now, syndiemedia.i2p still points to syndie.i2p.net:8000/)
16:33 &lt;jrandom&gt; ok, if there isn't anything else for the meeting
16:33  * jrandom winds up
16:33  * jrandom *baf*s the meeting closed
</div>
