---
title: "I2P Dev Meeting - September 27, 2005"
date: 2005-09-27
author: "jrandom"
description: "I2P development meeting log for September 27, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> A123, brutus, Complication, gloin, jrandom, LevDavidovitch, mihi, mihi, mule, postman, Ragnarok, Sugadude, wiht</p>

## Meeting Log

<div class="irc-log">
16:14 &lt;jrandom&gt; 0) hi
16:14 &lt;jrandom&gt; 1) Net status
16:14 &lt;jrandom&gt; 2) 0.6.1
16:14 &lt;jrandom&gt; 3) ???
16:14 &lt;jrandom&gt; 0) hi
16:14  * jrandom waves
16:14 &lt;+Ragnarok&gt; ok, I'll hold my further questions
16:14 &lt;jrandom&gt; weekly status notes posted up at http://dev.i2p.net/pipermail/i2p/2005-September/000933.html
16:14 &lt;+Ragnarok&gt; hi :)
16:15 &lt;wiht&gt; Hello.
16:15 &lt;jrandom&gt; we can definitely dig into it further in 3?? if you'd prefer
16:15 &lt;+Ragnarok&gt; cool
16:15 &lt;jrandom&gt; ok, jumping into 1) Net status
16:15 &lt;jrandom&gt; in general, things seem pretty solid
16:16 &lt;A123&gt; Is the http outproxy run by just one router?
16:16 &lt;wiht&gt; I see 307 known nodes on my router console.
16:16 &lt;A123&gt; (I'm still a little hazy on how I2P works)
16:16 &lt;jrandom&gt; there are two outproxies configured by default, and a few others available not configured by default
16:16 &lt;wiht&gt; Has anyone's bandwidth been maxed out by the recent growth of the network?
16:17 &lt;jrandom&gt; well, my bandwidth usage has grown, a steady 30-40KBps on my routers
16:17 &lt;jrandom&gt; (to a steady 30-40, that is)
16:18 &lt;jrandom&gt; (i'm also running a few high traffic services, like squid.i2p ;)
16:19 &lt;A123&gt; Ever look at the logs?
16:19 &lt;jrandom&gt; of squid?  no, i have it set to not do any request logging
16:20 &lt;+Ragnarok&gt; remember, he could be lying :)
16:20 &lt;+Ragnarok&gt; thus, it's a stupid question to ask
16:20 &lt;jrandom&gt; (though that could be a lie, and may work for the FBI/etc, so don't abuse it ;)
16:20 &lt;A123&gt; I was just curious as to whether there was anything interesting in there :)
16:21 &lt;+mihi&gt; A123: run your own outproxy :)
16:21 &lt;gloin&gt; A123: setup a tor node.
16:21 &lt;A123&gt; Is it easy to set up?
16:21 &lt;jrandom&gt; not really
16:21 &lt;A123&gt; gloin, tor is explicitly not designed for file sharing, so I have little interest in it.
16:22 &lt;jrandom&gt; (an outproxy, that is.  tor is easy to set up)
16:22 &lt;A123&gt; Or at least, they've explicitly stated that they don't want people to use it for file sharing.
16:22 &lt;wiht&gt; jrandom, do you still want to wait for version 1.0 before a full public announcement of the I2P project's maturity?
16:23 &lt;+mihi&gt; A123: it is definitely harder than registering your nick with nickserv *hint* *hint*
16:23 &lt;A123&gt; Oh yeah, I sure don't want A123 to be taken :)
16:23 &lt;wiht&gt; If the network is doing well now, could it stand the addition of more users?
16:23 &lt;jrandom&gt; we'll need to do some outreach before 1.0 so that we can have some testing in larger environments
16:24 &lt;+Ragnarok&gt; maybe a preview release, or some such thing
16:24 &lt;wiht&gt; A beta release? Sounds like a good idea.
16:25 &lt;jrandom&gt; aye, that'll happen along side the website revamp, maybe before 0.6.2
16:25 &lt;jrandom&gt; (or maybe @ 0.6.2)
16:25 &lt;jrandom&gt; (website revamp being part of that critical path so we dont spend hours upon hours answering the same questions)
16:25 &lt;+Ragnarok&gt; well, with a little more end-user polish than just another beta
16:26 &lt;A123&gt; Is it possible for I2P-aware clients to configure tunnels themselves easily?
16:26 &lt;jrandom&gt; yes
16:26 &lt;A123&gt; I guess they could always do HTTP requests to the console...
16:26 &lt;+Ragnarok&gt; the router console also need a serious revamp.  It would be nice for the initial page to be more like an i2p portal, and move all the technical stuff a little farther in
16:26 &lt;jrandom&gt; its one of the properties they send when they connect to i2p
16:26 &lt;jrandom&gt; agreed Ragnarok
16:27 &lt;A123&gt; Hrm. The Azureus I2P plugin could have a bit of additional friendliness, then.
16:27 &lt;A123&gt; Or any friendliness at all.
16:27 &lt;jrandom&gt; agreed A123 ;)
16:27 &lt;jrandom&gt; (though they've done a great job showing the proof of work)
16:28 &lt;jrandom&gt; there have been a lot of great suggestions on the mailing list as of late regarding usability
16:28 &lt;jrandom&gt; many/most of which should be done prior to asking new users to try i2p out
16:28 &lt;A123&gt; From the console: "If you can't poke a hole in your NAT or firewall to allow unsolicited UDP packets to reach the router, as detected with the Status: ERR-Reject..."
16:28 &lt;A123&gt; Where would I see "Status: ERR-Reject"?
16:29 &lt;+Ragnarok&gt; it's nice that we're at the point where we can worry about usability :)
16:29 &lt;jrandom&gt; A123: on the left hand side of your router console, it says Status: OK (or Status: unknown, or something else)
16:29 &lt;+Complication&gt; In the Status field of the router console.
16:29 &lt;jrandom&gt; true 'nuff Ragnarok 
16:29 &lt;+Complication&gt; Hopefully you've got an OK or OK (NAT) there.
16:30 &lt;A123&gt; Complication, ah, thanks. Is that the thing that gets updated if you click on "Check network reachability..."?
16:30 &lt;wiht&gt; I hope that you will not have to break compatibility in future releases of I2P. Full network migration to a new version seems to have been painful in the past.
16:30 &lt;+Complication&gt; A123: yes, it should test again when you click
16:30 &lt;+Complication&gt; Doesn't happen instantly, though.
16:30 &lt;jrandom&gt; eh, they're not as painful as they used to be, but yeah, it'd be good if we can avoid it wiht
16:30 &lt;A123&gt; So I have to refresh the page?
16:30 &lt;A123&gt; Well, no, that would do another http post...
16:31 &lt;+Complication&gt; A123: it may take a minute to find a testing-suitable peer
16:31 &lt;+Complication&gt; 'cause you cannot test with those whom you're already speaking to
16:31 &lt;+Complication&gt; It could give false results.
16:32 &lt;+Complication&gt; So, it should show up when you view the router console sometime later.
16:32 &lt;+Complication&gt; Basically, in ideal circumstances, you shouldn not need to fire a peer test manually.
16:33 &lt;+Complication&gt; =shouldn't need
16:33 &lt;jrandom&gt; right, i2p now does a peer test automatically when certain events occur
16:33 &lt;jrandom&gt; (such as when someone tells you that your IP is something other than what you think it is)
16:33 &lt;A123&gt; I found that button completely unintuitive. I had no idea what it was updating and when, it never explicitly told me the results of the test...
16:34 &lt;A123&gt; The page wasn't automatically refreshing (I think), I can't do a reload in the browser...
16:34 &lt;jrandom&gt; reload should be safe
16:34 &lt;A123&gt; Surely that fires another test?
16:34 &lt;jrandom&gt; but yeah, the router console was designed more for technical reasons rather than usability
16:34 &lt;jrandom&gt; A123: it has a nonce to prevent that
16:34 &lt;+Complication&gt; That facet might benefit from a better explanation text in future
16:35 &lt;wiht&gt; Have we skipped 2) and gone to 3) already?
16:35 &lt;jrandom&gt; Complication: we'll probably drop it, since its unnecessary
16:35 &lt;jrandom&gt; no, still on 1
16:35 &lt;jrandom&gt; actually, anyone have anything else for 1) network status?
16:35 &lt;A123&gt; Ah, indeed, after a few times it complains about the nonce.
16:35 &lt;jrandom&gt; if not, moving on to 2) 0.6.1
16:35 &lt;A123&gt; "nonce" to non-geeks is just going to seem like a nonsense word.
16:36 &lt;A123&gt; :)
16:36  * Complication looks at graphs
16:36 &lt;+Complication&gt; No complaints about net status from here.
16:36 &lt;jrandom&gt; w3wt
16:37 &lt;A123&gt; Is there any reason that reseeding isn't automatic?
16:37 &lt;jrandom&gt; ok, i don't really have too much to mention regarding 0.6.1 beyond whats in the mail
16:37 &lt;gloin&gt; hmm.. shouldn't be the incoming and outoging traffic more or less symmetric?
16:37 &lt;A123&gt; Mine seems more or less symmetric.
16:37 &lt;jrandom&gt; A123: yes, though we may be able to do it safer
16:37 &lt;+Complication&gt; gloin: not if one's leeching or seeding ;)
16:37 &lt;+Ragnarok&gt; not if you're downloading stuff
16:38 &lt;A123&gt; Total: 3.74/4.09KBps (that's in/out)
16:39 &lt;gloin&gt; Complication: Is this a security problem? Shouldn't the 'foreign' traffic be reduced?
16:39 &lt;+Complication&gt; gloin: depends on what the criteria are
16:40 &lt;+Complication&gt; A person striving for utmost security clearly shouldn't be doing things which permit others to cause observable changes in their BW.
16:40 &lt;jrandom&gt; gloin: as we move to 1.0, we will stop publishing those stats
16:40 &lt;A123&gt; My ISP will still know them...
16:40 &lt;jrandom&gt; but yes, defending against local traffic analysis does require you to participate in other people's tunnels
16:41 &lt;+Complication&gt; (for a strict definition of "their BW", meaning "bandwidth use starting/ending at their node")
16:41 &lt;jrandom&gt; (or do sufficient chaff activity.  tarzan for instance has "mimics" for wasting bandwidth^W^Wdefending anonymity)
16:41 &lt;A123&gt; Hrm.
16:41 &lt;A123&gt; I'm on ADSL, with far more download ability than upload.
16:42 &lt;+Complication&gt; Many are.
16:42 &lt;A123&gt; When my download exceeds my upload, doesn't that imply that I'm downloading stuff?
16:43 &lt;wiht&gt; No, you could also be forwarding others' traffic.
16:43 &lt;+Complication&gt; I guess it would imply you are downloading something.
16:43 &lt;A123&gt; Does I2P cache data?
16:43  * wiht would like to be corrected if that's wrong.
16:43 &lt;+Complication&gt; Unless you are seeding as much as you're leeching.
16:43 &lt;jrandom&gt; i2p itself does not cache
16:43 &lt;+Complication&gt; A123: no caching occurs to my knowledge
16:43 &lt;jrandom&gt; though syndie, on the other hand, does.  
16:44 &lt;A123&gt; If there's no caching, then my download exceeding my upload must mean that I'm downloading something myself, right?
16:44 &lt;jrandom&gt; if you have large amounts of inbound trafffic but no current outbound traffic, you could just be running a syndie node
16:44 &lt;jrandom&gt; yes A123, given a small enough time frame
16:45 &lt;A123&gt; Since I could only usefully be downloading at the speed of my upload, after network buffers fill.
16:45 &lt;jrandom&gt; for a certain threat model, yes
16:45 &lt;A123&gt; Hrm.
16:45 &lt;jrandom&gt; (local passive attacker with sufficient resources, or a targetted local attacker, etc)
16:46 &lt;+Complication&gt; You could download faster, but it would increase your risk. (For which reason I have allocated up/down similar limits.)
16:46 &lt;A123&gt; Ah, good point, I can just limit my download speed.
16:46 &lt;@LevDavidovitch&gt; btw, you should limit both your dl and ul speed
16:47 &lt;+Complication&gt; But if someone targeted everyone who downloads more than uploads... they'd be targeting everyone and their granny.
16:47 &lt;wiht&gt; We are still having disconnection issues with IRC, it seems.
16:47 &lt;jrandom&gt; wiht: only a few people are
16:47 &lt;wiht&gt; OK.
16:47 &lt;@LevDavidovitch&gt; also reconnection is v FAST these days
16:48 &lt;jrandom&gt; (and nothing as bad as it was)
16:48 &lt;wiht&gt; I agree, reconnections are better.
16:48 &lt;jrandom&gt; aye, its nice to have our irc servers hosted on routers with reasonable bw limits :)
16:49 &lt;jrandom&gt; ((not that before was unreasonable, it was great, we just outgrew it))
16:49 &lt;A123&gt; Is there any technical reason why DCC isn't supported? It can be implemented similar to the nat module, right?
16:49 &lt;jrandom&gt; ok, anyone have anything for 2) 0.6.1?
16:49 &lt;jrandom&gt; yes A123, there are technical reasons why dcc isnt supported
16:50 &lt;@LevDavidovitch&gt; it'd have to be done client side, i think.
16:50 &lt;jrandom&gt; someone could implement an irc proxy with dcc support, but no one has
16:50 &lt;A123&gt; What are they? Or is that a long discussion?
16:50 &lt;jrandom&gt; dcc support requires knowing and interpretting the irc protocol, and rewriting the irc messages sent as necessary
16:50 &lt;@LevDavidovitch&gt; normal dcc uses arbitrary ports and all
16:50 &lt;jrandom&gt; (in particular, ctcp messages for establishing dcc connections)
16:50 &lt;A123&gt; Oh, that's what I meant to ask... Whether it was technically possible to do it as with a nat module (which does as you say).
16:51 &lt;jrandom&gt; i dont know what a nat module is?
16:51 &lt;@LevDavidovitch&gt; the nat uses some UDP weirdnesses.
16:52 &lt;@LevDavidovitch&gt; the nat traversal thing i think he means
16:52 &lt;jrandom&gt; ah, ok, yeah, its technically possible, but no one has volunteered to work on it (and i'm swamped)
16:52 &lt;A123&gt; No... At least for Linux, there's a masq module for iptables which will rewrite IRC packets with DCC CTCP requests.
16:53 &lt;@LevDavidovitch&gt; ah, i see
16:53 &lt;@LevDavidovitch&gt; maybe some of that code would be usable
16:53 &lt;@LevDavidovitch&gt; depends how intimate it is with the ipfilter thing
16:54 &lt;jrandom&gt; probably simpler to just extend I2PTunnelClient to interpret irc perhaps
16:54 &lt;A123&gt; http://www.koders.com/c/fidA6A89E1080590138EB211E694473DDDD098B6B75.aspx &lt;- Might be interesting, courtesy of Google.
16:54 &lt;jrandom&gt; (in the same way I2PTunnelHTTPClient extends it to interpret HTTP)
16:55 &lt;@LevDavidovitch&gt; not in most countries. 
16:55 &lt;@LevDavidovitch&gt; oops
16:56 &lt;jrandom&gt; A123: an os level filter would be a bit tough to deploy, but if someone wants to work on it, that'd be a good place to start
16:57 &lt;jrandom&gt; ok, anything else on 2) 0.6.1, or shall we move on to 3) ???
16:57 &lt;A123&gt; jrandom, it wouldn't really need to be OS level, would it? It would be coming through the IRC tunnel anyway...
16:58 &lt;jrandom&gt; actually, it wouldn't even work as an iptables filter.  it has to be done inside i2ptunnel or some other i2p-aware proxy
16:58 &lt;jrandom&gt; in any case, its a lot of work, and unless someone volunteers to do it, it'll never get done ;)
16:59 &lt;jrandom&gt; (it *woudl* be cool though)
16:59 &lt;A123&gt; Right.
16:59 &lt;A123&gt; I meant "like the iptables filter", not "using the iptables filter" :)
16:59 &lt;A123&gt; -the+a
16:59 &lt;A123&gt; +n
17:00 &lt;A123&gt; Hrm hrm.
17:00 &lt;@LevDavidovitch&gt; go forth I think
17:01 &lt;jrandom&gt; ok, on to 3) ??? 
17:01 &lt;jrandom&gt; (though one could probably say we've been on 3) all along ;)
17:01 &lt;jrandom&gt; anyone have anything else they want to bring up for the meeting?
17:01 &lt;+fox&gt; &lt;brutus&gt; on 3) bugzilla would be nice to have in shape before 1.0
17:01 &lt;wiht&gt; Speaking of the usability suggestions from the mailing list, have you incorporated any of them into I2P?
17:02 &lt;jrandom&gt; brutus: we used to have bugzilla, but no one used it
17:03 &lt;wiht&gt; I should say, are you still concentrating on the core I2P functionality and planning to focus on usability a little later?
17:03 &lt;A123&gt; I don't want to try it here, but I think that sending someone a DCC request at the moment would reveal to them your IP.
17:03 &lt;A123&gt; (Assuming your client knows your IP)
17:03 &lt;jrandom&gt; wiht: the last week i've been doing a lot of improvements to the streaming lib which should substantially improve usability
17:04 &lt;jrandom&gt; A123: the irc servers filter ctcp messages
17:04 &lt;jrandom&gt; (they've been modified)
17:04 &lt;A123&gt; Servers...
17:04 &lt;jrandom&gt; but yes, that does send your ip to the server (which it may discard, or may file into some NSA database)
17:04 &lt;jrandom&gt; so, dont send dcc requests
17:04 &lt;A123&gt; I don't really want the server admins knowing who I am, either :)
17:05 &lt;A123&gt; (In theory. I don't care now or with you guys)
17:05 &lt;A123&gt; It might be worth warning users about that.
17:05 &lt;jrandom&gt; there's a page on the wiki about a whole slew of issues iirc
17:05 &lt;jrandom&gt; (swing by ugha.i2p)
17:06 &lt;+fox&gt; &lt;mihi&gt; btw: are the irc2p servers connected via i2p or directly?
17:06 &lt;+Complication&gt; I'd assume i2p
17:06 &lt;+Complication&gt; Unless someone's gone mad meanwhile, and not notified me. :P
17:06 &lt;wiht&gt; jrandom, that's good, but what about the UI suggestions by Isamoor?
17:07 &lt;jrandom&gt; mihi: i believe they're done over i2p
17:08 &lt;jrandom&gt; wiht: the list of what i've been doing is available on http://dev.i2p/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD
17:09 &lt;jrandom&gt; there's a lot more to be done, and a lot more will be done, but i have only two hands
17:09 &lt;wiht&gt; Thank you, I will look there.
17:10 &lt;jrandom&gt; actually, i have something to bring up for the meeting...
17:10 &lt;A123&gt; What's the server/channel that fox is changating? Or do I misunderstand fox's purpose?
17:11 &lt;jrandom&gt; as mentioned on hq.postman.i2p, we've had over a full year of anonymous mail service through postman's servers!  
17:11  * jrandom cheers
17:11  * wiht does not want to seem ungrateful.
17:12 &lt;A123&gt; jrandom, have the spammers caught on yet?
17:12 &lt;jrandom&gt; A123: fox is a bridge to irc.freenode.net
17:12 &lt;A123&gt; (OK, it's a slow way to go about spamming...)
17:12 &lt;jrandom&gt; A123: doubt it, postman has antispam measures
17:12 &lt;jrandom&gt; inbound spam is a bit of a problem though ;)
17:13 &lt;jrandom&gt; (but my account there has been well filtered)
17:13 &lt;mule&gt; is it really that long. time passes ...
17:13 &lt;A123&gt; jrandom, ah, thanks.
17:13  * Complication looks if someone has finally dropped him a bear via e-mail
17:14 &lt;+fox&gt; &lt;brutus&gt; yeah, postman & cervantes deserve a medal, they're pulling some great weights around here
17:15 &lt;+fox&gt; &lt;brutus&gt; excellent services indeed
17:16 &lt;jrandom&gt; mos' def'.  as is mule with his outproxy and fproxy, orion with his site, and the rest of y'all with yer content :)
17:16 &lt;jrandom&gt; ok, anyone have anything else to bring up for the meeting?
17:16 &lt;wiht&gt; Speaking of content...
17:16 &lt;wiht&gt; It seems that we know what sites are up or not, but no easily accessible directory of sites.
17:17 &lt;A123&gt; My clock runs fast. Would it be possible for the "Updating clock offset to -316819ms from -304801ms" messages to be downgraded from "CRIT"? It's a little disconcerting.
17:17 &lt;wiht&gt; I was thinking of creating one where site admins can post what their site is about.
17:17 &lt;jrandom&gt; orion.i2p is pretty easily accessible...?
17:17 &lt;jrandom&gt; A123: hmm, perhaps
17:18 &lt;wiht&gt; It has a short description of sites' purposes?
17:18 &lt;+postman&gt; A123: spam is only a problem for incoming mail ( mail FROM the internet )
17:18 &lt;jrandom&gt; wiht: yeah, it does, though i dont know where they come from
17:18 &lt;+Complication&gt; wiht: no, orion doesn't seem to have that feature
17:18 &lt;wiht&gt; I will look again.
17:18 &lt;jrandom&gt; iirc jnymo used to maintain them
17:18 &lt;+postman&gt; A123: i2p mail  users can rarely spam themselves as well as they cannot spam internet targets
17:19 &lt;+Complication&gt; Sorry, meant to say it doesn't seem user-accessible.
17:19 &lt;wiht&gt; I was thinking of a directory that categorizes sites, something similar to dmoz.org.
17:19 &lt;A123&gt; wiht, as a brand new user, that sounds great.
17:19 &lt;+fox&gt; &lt;Sugadude&gt; wiht: Do we have enough sites to need to classify them?
17:19 &lt;A123&gt; wiht, but check Freenet for an excellent example of how not to do it.
17:20 &lt;jrandom&gt; a reliable categorized site would be neat.  or perhaps we can integrate it into syndie to let people tag and categorize their peer references (and share them)
17:20 &lt;jrandom&gt; (syndie already has a set of category tags for each bookmark, laying it out visually dmoz style wouldnt be hard)
17:20 &lt;jrandom&gt; and it'd be local &lt;--- fast
17:20 &lt;A123&gt; Or just get Google interested in i2p...
17:20 &lt;jrandom&gt; heh
17:24 &lt;jrandom&gt; ok, if there's nothing more for the meeting...
17:25  * jrandom winds up
17:25  * jrandom *baf*s the meeting closed
</div>
