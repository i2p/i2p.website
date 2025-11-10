---
title: "I2P Dev Meeting - March 22, 2005"
date: 2005-03-22
author: "@jrandom"
description: "I2P development meeting log for March 22, 2005."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> ant, bla, cervantes, detonate, duck, frosk, jdot, jrandom, mihi, Ragnarok</p>

## Meeting Log

<div class="irc-log">
13:01 &lt;@jrandom&gt; 0) hi
13:01 &lt;@jrandom&gt; 1) 0.5.0.3
13:01 &lt;@jrandom&gt; 2) batching
13:01 &lt;@jrandom&gt; 3) updating
13:01 &lt;@jrandom&gt; 4) ???
13:01 &lt;@jrandom&gt; 0) hi
13:01  * jrandom waves
13:01 &lt;@jrandom&gt; the just-now-posted weekly status notes are up @ http://dev.i2p.net/pipermail/i2p/2005-March/000654.html
13:02 &lt;+detonate&gt; hi
13:02 &lt;+cervantes&gt; 'lo
13:02 &lt;@jrandom&gt; jumpin' right in to 1) 0.5.0.3
13:02 &lt;@jrandom&gt; the release came out a few days ago, and reports have been positive
13:02 &lt;+cervantes&gt; jrandom: let us know when the blue dancing dwarves climb onto your monitor and we'll stop the meeting early
13:03 &lt;@jrandom&gt; heh cervantes 
13:03 &lt;@jrandom&gt; (thank Bob for editable meeting logs ;)
13:04 &lt;@jrandom&gt; i dont really have much to add wrt 0.5.0.3 than whats in that message
13:04 &lt;@jrandom&gt; anyone have any comments/questions/concerns on it?
13:04 &lt;bla&gt; jrandom: Any new measurements on the fast-peers-selection code?
13:05 &lt;@jrandom&gt; ah, i knew there was something else in 0.5.0.3 that i had neglected ;)
13:06 &lt;@jrandom&gt; i dont have any hard metrics yet, but anecdotally the fast peer selection has found the peers that i know explicitly to be 'fast' (e.g. routers on the same box, etc)
13:07 &lt;bla&gt; jrandom: Sometimes, eepsites still require a number of retries to find a good tunnel to use
13:07 &lt;@jrandom&gt; reports have come in for fairly reasonable throughput rates on occation as well (in the 10-20KBps range), but thats still not frequent (we still have the parameters tuned down)
13:08 &lt;+ant&gt; &lt;Connelly&gt; oops there's a meeting
13:09 &lt;@jrandom&gt; hmm, yes, i've found that reliability still isn't where it need to be.  retrying more than once really isn't a solution though - if a site doesnt load after 1 retry, give it 5-10m before retrying
13:09 &lt;@jrandom&gt; what i've seen on the net though is some not-infrequent-enough transport layer delay spikes
13:10 &lt;@jrandom&gt; e.g. taking 5-20+ seconds just to flush a 1-2KB message through a socket
13:10 &lt;@jrandom&gt; tie that up with a 5 hop path (2 hop tunnels) and you can run into trouble
13:11 &lt;@jrandom&gt; thats actually part of whats driving the batching code - reducing the # of messages to be sent
13:13 &lt;@jrandom&gt; ok, anyone else have any questions/comments/concerns on 0.5.0.3?
13:13 &lt;bla&gt; jrandom: Looks good. I will ask more about it in the next "section"
13:14 &lt;@jrandom&gt; w3rd, ok, perhaps we can move on there then - 2) batching
13:15 &lt;@jrandom&gt; the email and my blog (jrandom.dev.i2p&lt;/spam&gt;) should describe the basics of whats planned
13:15 &lt;@jrandom&gt; and, well, really its some pretty basic stuff
13:15 &lt;@jrandom&gt; the current preprocessor we have was the simplest possible one to implement (class name: TrivialPreprocessor) ;)
13:16 &lt;@jrandom&gt; this new one has some tunable parameters for batching frequency, as well as some outbound tunnel affinity within individual tunnel pools (where we try to select the same outbound tunnel for subsequent requests for up to e.g. 500ms, so that we can optimize the batching)
13:17 &lt;@jrandom&gt; that's about all i have to add on that though - any questions/comments/concerns?  
13:18 &lt;bla&gt; Does this require all participating nodes to run the new preprocessor, or can a mix of Trivial/NewOne coexist?
13:18 &lt;+Ragnarok&gt; this will add .5 s to latency, right?
13:19 &lt;@jrandom&gt; bla: nah, this preprocessor is only used on the tunnel gateway, and its up to that gateway to decide how or whether to batch
13:20 &lt;@jrandom&gt; Ragnarok: not usually - message 1 may be delayed for up to .5s, but messages 2-15 get transferred much faster than they would have otherwise.  its also a simple threshold - as soon as a full tunnel message worth of data is available, its flushed
13:20 &lt;+Ragnarok&gt; cool
13:20 &lt;+Ragnarok&gt; how much overhead does it save?
13:21 &lt;@jrandom&gt; substantial ;)
13:21 &lt;+Ragnarok&gt; substantial is good, if vague :P
13:21 &lt;@jrandom&gt; look on your http://localhost:7657/oldstats.jsp#tunnel.smallFragments
13:21 &lt;@jrandom&gt; compare that to #tunnel.fullFragments
13:22 &lt;bla&gt; jrandom: Does this concern endpoint-&gt;IB-gateway communication only? 
13:22 &lt;@jrandom&gt; with batching, the ratio of full to small will go up, and the # of pad bytes in the small will go down
13:23 &lt;@jrandom&gt; bla: hmm, it concerns all tunnel gateways, whether inbound or outbound
13:24 &lt;mihi&gt; full fragments: lifetime average value: 1,00 over 1.621,00 events
13:24 &lt;bla&gt; jrandom: ok
13:24 &lt;mihi&gt; can there be a frational number of fragments?
13:24 &lt;@jrandom&gt; full: 1.00 over 807,077.00 events small: 746.80 over 692,682.00 events
13:25 &lt;@jrandom&gt; heh mihi
13:25 &lt;@jrandom&gt; (that small: 746 means that on those 692k messages, 746 out of 996 bytes were wasted pad bytes!)
13:26 &lt;@jrandom&gt; well, not quite wasted - they served their purpose
13:26 &lt;+detonate&gt; needless overhead anyway
13:27 &lt;@jrandom&gt; yep, much of which we should be able to shed with the batching preprocessor
13:28 &lt;@jrandom&gt; unfortunately, that won't be bundled in the next release
13:28 &lt;@jrandom&gt; but it will be bundled in the 0.5.0.6 rev (or perhaps 0.5.1)
13:28 &lt;@jrandom&gt; erm, 0.5.0.5, or 0.5.1
13:28  * jrandom gets confused with #s
13:29 &lt;bla&gt; jrandom: How come not?
13:29 &lt;+cervantes&gt; hash and pills...damn
13:30 &lt;@jrandom&gt; !thwap cervantes 
13:30 &lt;@jrandom&gt; bla: there's a bug in 0.5.0.3 (and before) where the fragmented message handler will cause subsequent fragments within the same tunnel message to be discarded
13:31 &lt;@jrandom&gt; if we deployed the batching preprocessor directly, we'd have a substantial number of lost messages
13:31 &lt;@jrandom&gt; its not a worry, we've got other neat stuff up our sleeves though, so this coming 0.5.0.4 won't be totally boring ;)
13:31 &lt;bla&gt; jrandom: Ah, so that
13:32 &lt;bla&gt; jrandom: Ah, so that is why we have to do that after 0.5.0.4 is mainstream.. I see. Thnx.
13:33 &lt;@jrandom&gt; yeah, it'd be nice if the fragment handler was able to deal with it, and it does, generally, it just releases the byte buffer too soon, zeroing out subsequent fragments (oops)
13:33 &lt;@jrandom&gt; ok, anything else on 2), or shall we move on to 3) updating?
13:35 &lt;@jrandom&gt; ok, as mentioned in the status notes (and discussed for a while in various venues), we're going to add some functionality for simple and safe updating that doesn't require the end user to go to the website, read the mailing list, or read the topic in the channel :)
13:36 &lt;+detonate&gt; cool
13:36 &lt;@jrandom&gt; smeghead has put together some code to help automate and secure the process, working with cervantes to tie in with fire2pe as well as the normal routerconsole
13:37 &lt;@jrandom&gt; the email lists the general description of whats going to be available, and while most of it is functional, there are still a few pieces not yet fully hashed out
13:37 &lt;@jrandom&gt; unlike the batching, this /will/ be available in the next rev, though people won't be able to make much use of it until 0.5.0.5 (when it comes time to update)
13:39 &lt;+Ragnarok&gt; so... what's the cool stuff for 5.0.4, then?
13:42 &lt;@jrandom&gt; with the update code comes the ability to pull announcement data, displaying e.g. a snippet of news on the top of the router console.  in addition to that, as part of the update code we've got a new reliable download component which works either directly or through the eepproxy, retrying and continuing along the way.  perhaps there'll be some relatd features built off that, but no promises
13:42 &lt;+Ragnarok&gt; neat
13:43 &lt;@jrandom&gt; ok, anyone else have any questions/comments/concerns on 3) updating?
13:45 &lt;@jrandom&gt; if not, moving on to 4) ???
13:45 &lt;@jrandom&gt; anything else anyone wants to bring up?  i'm sure i've missed soem things
13:45 &lt;+detonate&gt; i2p's known to work with the sun jvm in OpenBSD 3.7 :)
13:45 &lt;@jrandom&gt; nice!
13:47 &lt;bla&gt; What is the status on the UDP transport?
13:48 &lt;+detonate&gt; udp is going to be messy, i think it would be better to steal the pipelining code from bt and adapt it ;)
13:48 &lt;@jrandom&gt; *cough*
13:49 &lt;@jrandom&gt; i dont expect there to be much trouble, but there's certainly work to be done
13:49 &lt;@jrandom&gt; how the queueing policy operates, as well as the bw throttling for admission to the queue will be interesting
13:50 &lt;bla&gt; Who was doing that prelim work?
13:50 &lt;@jrandom&gt; bla: detonate and mule
13:50 &lt;+detonate&gt; yeah.. i've been slacking off the last month or so though
13:50 &lt;bla&gt; detonate: I assume you jest, with your BT remark?
13:51 &lt;+detonate&gt; i'm half-serious
13:51 &lt;+detonate&gt; you could at least cut the thread count for the transport in half if you did that
13:51  * jrandom flings a bucket of mud at detonate 
13:51 &lt;jdot&gt; woohoo.  my router is now running on my dedicated server rather than my POS cable connection.
13:51 &lt;@jrandom&gt; nice1 jdot 
13:52 &lt;@jrandom&gt; we'll be able to get by with 3-5 threads in the transport layer for all comm with all peers
13:52 &lt;bla&gt; detonate: But half is not going to cut it, when the net becomes large (&gt; couple hundred nodes)
13:52 &lt;jdot&gt; with 1000GB of b/w at its disposal
13:53 &lt;jdot&gt; unforunately j.i2p and the chat.i2p will be down for a few more hours while i migrate things
13:53 &lt;duck&gt; detonate: addressbook on halt too?
13:53 &lt;+detonate&gt; yeah, it's on halt too
13:54 &lt;+detonate&gt; the only thing that isn't on halt is the monolithic profile storage, i was meaning to get that working later today
13:54 &lt;@jrandom&gt; w3rd
13:54 &lt;+detonate&gt; then i2p won't fragment the drive massively
13:54 &lt;jdot&gt; jrandom: as far as BW limits go, are they averages?
13:54 &lt;+frosk&gt; modern filesystems don't fragment, silly
13:55 &lt;+detonate&gt; ntfs does
13:55 &lt;@jrandom&gt; jdot: the bandwidth limits are strict token buckets
13:55 &lt;@jrandom&gt; jdot: if you set the burst duration out, thats how long of a period it averages out through
13:56 &lt;@jrandom&gt; (well, 2x burst == period)
13:56 &lt;@jrandom&gt; ((ish))
13:56 &lt;jdot&gt; hmmm...  well i have 1000GB and want i2p to be able to take up to 800GB/mo....
13:56 &lt;+ant&gt; &lt;mihi&gt; detonate: ntfs stores really small files in mft which means nealy no fragmentation
13:57 &lt;jdot&gt; and i dont care what it bursts to
13:57 &lt;+detonate&gt; well, when you run the defragmenter, it spends 10 minutes moving all 6000 profiles around.. so they must fragment
13:58 &lt;@jrandom&gt; jdot: hmm, well, 800GB is probably more than it'll want to push anyway, so you can probably go without limits ;)  
13:58 &lt;@jrandom&gt; otoh, if you could describe a policy that you'd like implemented, we might be able to handle it
13:58 &lt;jdot&gt; jrandom: i'll do that for now and see how it works
13:58 &lt;bla&gt; detonate: NTFS, IIRC, is a journalling FS. So even a monolotic file will get fragmented if you write small portions to it 
13:58 &lt;+detonate&gt; everything gets written at once
13:59 &lt;+detonate&gt; and read at once
13:59 &lt;bla&gt; detonate: Ok. I see.
13:59 &lt;jdot&gt; jrandom: well, lets wait until we figure out if it'll even be a problem.
13:59 &lt;bla&gt; detonate: Good work in that case!
13:59 &lt;+detonate&gt; i'd be interested in knowing how much usage there really is if you leave it uncapped
14:00 &lt;+detonate&gt; on a good connection
14:00 &lt;jdot&gt; i'm interested too!
14:00 &lt;@jrandom&gt; my colo routers run uncapped, though cpu constrained
14:00 &lt;+Ragnarok&gt; can you use a bitbucket to average over a month?
14:00 &lt;jdot&gt; jrandom: cpu contrianed?  what kind of cpu?
14:01 &lt;@jrandom&gt; 4d transfer 3.04GB/2.73GB
14:01 &lt;+detonate&gt; hmm, was expecting less
14:01 &lt;@jrandom&gt; jdot: cpu constrained because i run 3 routers on it, plus a few other jvms, sometimes profiling
14:01 &lt;+detonate&gt; must be those bt people
14:01 &lt;+detonate&gt; once the batching stuff is online, it would be interesting to see how that changes
14:02 &lt;@jrandom&gt; detonate: some of that transfer is also me pushing 50MB files between itself ;)
14:02 &lt;+detonate&gt; heh
14:02 &lt;jdot&gt; ahh.  ok.  well, we'll see how this system does.  its an AMD XP 2400 w/ 512MB and a 10Mbit connection
14:02 &lt;@jrandom&gt; Ragnarok: token buckets dont really work that way
14:02 &lt;@jrandom&gt; jdot: word, yeah, this is a p4 1.6 iirc
14:03 &lt;@jrandom&gt; Ragnarok: in a token bucket, every (e.g.) second you add in some tokens, according to the rate.  if the bucket is full (size = burst period), the tokens are discarded
14:04 &lt;@jrandom&gt; whenever you want to transfer data, you need to get a sufficient amount of tokens
14:04 &lt;@jrandom&gt; (1 token = 1 byte)
14:04 &lt;+Ragnarok&gt; I know how they work... what happens if you just make the bucket really big?
14:05 &lt;+detonate&gt; then you never stop sending data
14:05 &lt;+detonate&gt; if it's infinite in size
14:05 &lt;+detonate&gt; err, and it's filled with tokens
14:05 &lt;@jrandom&gt; if its really big, it may go out and burst to unlimited rates after low usage
14:06 &lt;@jrandom&gt; though perhaps thats desired in some cases
14:07 &lt;@jrandom&gt; the thing is, you can't just set the token bucket to 800GB, as that wouldnt constrain the total amount transferred
14:08 &lt;+detonate&gt; you need a field there where you can set the number of tokens per second, then you can just divide the bandwidth usage per month by the number of seconds
14:08 &lt;+detonate&gt; :)
14:10 &lt;@jrandom&gt; thats the same as just setting the rate averaged over the month, which would be unbalanced.  but, anyway, lots of scenarios available - if anyone has any that address their needs that can't be met with whats available, please, get in touch
14:10 &lt;+Ragnarok&gt; but if you set the rate to the average you want... I think 308 kB/s here, and then set the bitbucket to something very larger... why doesn't that work?
14:11 &lt;+Ragnarok&gt; s/larger/large/
14:12 &lt;+detonate&gt; well, you could set it so that it never sends more than 800GB/44000 in a 60 second burst period
14:12 &lt;+detonate&gt; 44000 being roughly the number of minutes in a month
14:13 &lt;@jrandom&gt; the bucket size / burst duration describes how much we'll send without constraint, and most people /do/ want constraints, so the router doesnt gobble 10mbps for 5 minutes while draining the bucket (or whatever)
14:14 &lt;@jrandom&gt; an additional throttle of tokens coming out of the bucket is also possible (and should that throttle have its own token bucket, and that bucket have its own throttle, etc)
14:16 &lt;+Ragnarok&gt; I thought the bucket only got paid into when there was bandwidth not being used
14:16 &lt;@jrandom&gt; tokens are added to the bucket at a constant rate (e.g. 64k tokens per second)
14:17 &lt;@jrandom&gt; anything that wants bandwidth always asks the bucket
14:18 &lt;+Ragnarok&gt; ah.. ok
14:19 &lt;@jrandom&gt; ok cool, anyone else have anything they want to bring up for the meeting?
14:21 &lt;@jrandom&gt; ok if not
14:21  * jrandom winds up
14:21  * jrandom *baf*s the meeting closed
</div>
