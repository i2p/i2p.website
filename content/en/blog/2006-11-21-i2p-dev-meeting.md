---
title: "I2P Dev Meeting - November 21, 2006"
date: 2006-11-21
author: "jrandom"
description: "I2P development meeting log for November 21, 2006."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> blx, Complication3, jrandom, koff, LeerokKitchen, LeerokLacerta, modulus, spaetz, tea, Walter, zzz</p>

## Meeting Log

<div class="irc-log">
15:02 &lt;jrandom&gt; 0) hi
15:02 &lt;jrandom&gt; 1) Net status
15:02 &lt;jrandom&gt; 2) Syndie dev status
15:02 &lt;jrandom&gt; 3) ???
15:02 &lt;jrandom&gt; 0) hi
15:02  * jrandom waves
15:02 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2006-November/001319.html
15:03 &lt;jrandom&gt; since that one is pretty short, lets jump on in to 1) net status
15:04 &lt;jrandom&gt; things are looking pretty good atm, network seems pretty steady
15:04 &lt;+zzz&gt; I invented a "peer capacity index"
15:04 &lt;+zzz&gt; on the dashboard...
15:04 &lt;+zzz&gt; so far not sure it is helpful though
15:04 &lt;jrandom&gt; ah yeah, sorry, metioned that one last week - looks quite useful, thanks!
15:05 &lt;jrandom&gt; interesting to see the disparity out there so clarly
15:05 &lt;+zzz&gt; the idea is the ratio of high-cap routers to low-cap routers, which is obviously important to tunnel build %
15:06 &lt;+zzz&gt; I'm removing routers from stats that I don't get a netdb update for in 1.5 hours but that seems too quick, I think it is skewing the stats
15:07 &lt;jrandom&gt; ah, ok, that would explain it.  are you still harvesting?
15:07 &lt;jrandom&gt; (or wget'ing from dev.i2p.net?)
15:08 &lt;+zzz&gt; yes
15:08 &lt;jrandom&gt; cool
15:08 &lt;+zzz&gt; netDb.harvestDirectly=false
15:08 &lt;+zzz&gt;   netDb.shouldHarvest=true, right?
15:09 &lt;jrandom&gt; so the stats we've had before were largely based on routers that were so bad the user shut them down & disapeared then?
15:09 &lt;jrandom&gt; right
15:10 &lt;+zzz&gt; it's always been 1.5 hours, but plotting the M/N/O routers, they seem to come and go when intuitively they should stay pretty constant
15:10 &lt;jrandom&gt; ah ok
15:10 &lt;+zzz&gt; you can see spikes/dips in all the data that last 1.5 hours :)
15:11 &lt;spaetz&gt; net seems pretty stable. Yep
15:12 &lt;+zzz&gt; thats all I have for that topic
15:12 &lt;spaetz&gt; I'd like to know if jrandom completely focuses on syndie nowadays or if he still looks at i2p dev.
15:12 &lt;spaetz&gt; or if this is just a bit on hte backburner temporarily
15:13  * jrandom completely focuses on syndie nowadays, but will work on i2p both when there are problems and once syndie is established
15:13  * spaetz thanks for the information
15:14  * spaetz is fine with this
15:15 &lt;jrandom&gt; w3wt.  yeah, steadystate means syndie dev can continue, but if there are problems, of course i reprioritize
15:15 &lt;jrandom&gt; ok, anyone have anything else on 1) net status?
15:15 &lt;Walter&gt; I have a random question.
15:15 &lt;jrandom&gt; hit me Walter 
15:17 &lt;Walter&gt; Assume you have 100Mb/s BW, what kind of server would you need to saturate it as an I2P node?
15:17 &lt;jrandom&gt; doesnt matter
15:17 &lt;jrandom&gt; i2p does not and will not saturate 100Mbps
15:18 &lt;Walter&gt; Assume one wanted to make use of available BW.
15:18 &lt;jrandom&gt; you would not.
15:19 &lt;spaetz&gt; I've got 150kbs up and down and it uses like 25% of a vserver (Dell shared with a dozen others)
15:19 &lt;jrandom&gt; that exceeds the capacity of the entire network
15:19 &lt;spaetz&gt; 25%CPU that is
15:19  * spaetz admits that's not really a precise answer and shuts up
15:20 &lt;jrandom&gt; the routers themselves have a mem v. throughput tradeoff, making it less likely that a router can even push&gt; 3-350KBps
15:20 &lt;jrandom&gt; (of course, that tradeoff can be tweake to allow higher rates, but thats not an issue)
15:21 &lt;jrandom&gt; using bandwidth is *BAD* unless that bandwidth is being used only when necessary
15:22 &lt;+zzz&gt; the network is averaging about 1.5 MBps (=12 Mbps) total traffic over the last 3 months
15:23 &lt;Walter&gt; I see.
15:24 &lt;+fox&gt; &lt;LeerokKitchen&gt; Field trip!
15:26 &lt;jrandom&gt; ok, if there's nothing else for 1) net status, lets jump on over to 2) syndie dev status
15:26 &lt;jrandom&gt; progress here continues, and i've been doing testing both on windows and linux
15:28 &lt;jrandom&gt; current battle is on the forum management interface, though since the text interface is already embedded, all functionality is already in place
15:29 &lt;jrandom&gt; not much more news to discuss on that front though
15:30 &lt;jrandom&gt; anyone have any questions/comments/concerns on 2) syndie dev status?
15:33 &lt;jrandom&gt; ok, lets jump on to 3) ???
15:33 &lt;jrandom&gt; y'all have anything else for the meeting?
15:34 &lt;+fox&gt; &lt;blx&gt; when will gpl java be usable with i2p=
15:34 &lt;+fox&gt; &lt;blx&gt; ?
15:35 &lt;Complication3&gt; I guess it depends on when gpl java will be usable on various distros
15:35 &lt;Complication3&gt; Or available for download from Sun
15:36 &lt;Complication3&gt; But it feels like a moot point, since it's the same Java which is usable already now
15:36 &lt;Complication3&gt; GPL would only let it be packaged more conveniently, and improved upon
15:37 &lt;jrandom&gt; (and i2p already works with gcj/kaffe, though not all of the client apps)
15:37  * Complication3 quickly reads backlog
15:37 &lt;jrandom&gt; ((and syndie works with gcj/kaffe completely))
15:38 &lt;+fox&gt; &lt;blx&gt; Compilation, thats what they want you to think ;)
15:38 &lt;+fox&gt; &lt;blx&gt; but ok, i got my question answered.
15:38 &lt;+fox&gt; &lt;blx&gt; Complication even. misread
15:39 &lt;Complication3&gt; blx: well, the sources are available already now, it's just that few read and compile them
15:39 &lt;jrandom&gt; (and you can even modify and use those modifications, you just can't distribute your mods)
15:40 &lt;koff&gt; when will i2p have the logging functionality suggested by the proposed laws i heard about?
15:41 &lt;jrandom&gt; never
15:41 &lt;+zzz&gt; hahahaha
15:41  * Complication3 suspects never :)
15:41 &lt;+fox&gt; &lt;blx&gt; what laws?
15:41  * jrandom assumes you refer to .de/.eu data retention issues
15:41 &lt;Complication3&gt; Someone in the forum talked of a (proposed) law in Germany
15:42 &lt;jrandom&gt; (and then the .us ones in a few years)
15:42 &lt;Complication3&gt; They could have spelled it out better though
15:42 &lt;jrandom&gt; aye, 'tis just proposed, but not a big suprise
15:43 &lt;Complication3&gt; I personally think: it's not like data retention laws aren't being broken left and right already
15:43 &lt;Complication3&gt; Breaking a dozen more of them? I personally wouldn't care much...
15:44 &lt;Complication3&gt; In short, I want to see how they're going to enforce it
15:44 &lt;tea&gt; like they did with napster : arrest everyone
15:45 &lt;Complication3&gt; If they manage to make a good try, something will need to be found to thwart that ("not in my country" peering principle for countries where insanity prevails)
15:45 &lt;+fox&gt; &lt;LeerokLacerta&gt; That reminds me of a song.
15:45 &lt;+fox&gt; &lt;LeerokLacerta&gt; http://2ch.ru/mu/src/1163070550597.mp3
15:46 &lt;tea&gt; turning all data traffic over to anonymous networks might help ...
15:47 &lt;Complication3&gt; Just ignoring them en masse has worked for plain ordinary pirates...
15:47 &lt;Complication3&gt; You can arrest one person ignoring you. Can't do that with several hundred thousand.
15:47 &lt;tea&gt; that's no argument for a german :)
15:47 &lt;+fox&gt; &lt;modulus&gt; you can
15:47 &lt;+fox&gt; &lt;modulus&gt; hitler did
15:48 &lt;Complication3&gt; That's only because nobody bothered removing him
15:48 &lt;jrandom&gt; *cough*
15:48 &lt;Complication3&gt; Had they taken up arms, it wouldn't have worked
15:48 &lt;Complication3&gt; (sorry, far off topic, yes)
15:48 &lt;tea&gt; still, one does feel important in being paranoid
15:48 &lt;+fox&gt; &lt;modulus&gt; that said i think i2p could comply with data retention laws without damaging anonimity, but there's no reason to do that.
15:48 &lt;jrandom&gt; ok, well, i think we've addressed the i2p-related issue there ;)
15:48 &lt;tea&gt; sry
15:49 &lt;jrandom&gt; aye modulus
15:49 &lt;jrandom&gt; (we already assume individual users are logging everything anyway, as are the isps)
15:49 &lt;+fox&gt; &lt;modulus&gt; right, so a DR-enabled i2p wouldn't be the end of the world
15:51 &lt;Complication3&gt; Someone would have to bother forking that, though... :P
15:52  * jrandom keeps my mouth shut ;)
15:52 &lt;jrandom&gt; ok, anyone have anything else for the meeting?
15:53 &lt;jrandom&gt; if not
15:53  * jrandom winds up
15:53  * jrandom *baf*s the meeting closed
</div>
