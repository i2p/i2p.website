---
title: "Network Database Discussion"
description: "Historical notes on floodfill, Kademlia experiments, and future tuning for the netDb"
slug: "netdb"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

NOTE: The following is a discussion of the history of netdb implementation and is not current information.
See [the main netdb page](/docs/overview/network-database) for current documentation.


## History {#status}

The netDb is distributed with a simple technique called "floodfill".
Long ago, the netDb also used the Kademlia DHT as a fallback algorithm. However,
it did not work well in our application, and it was completely disabled
in release 0.6.1.20.

*(Adapted from a post by jrandom in the old Syndie, Nov. 26, 2005)*

The floodfill netDb is really just a simple and perhaps temporary measure,
using the simplest possible algorithm - send the data to a peer in the
floodfill netDb, wait 10 seconds, pick a random peer in the netDb and ask them
for the entry to be sent, verifying its proper insertion / distribution. If the
verification peer doesn't reply, or they don't have the entry, the sender
repeats the process. When the peer in the floodfill netDb receives a netDb
store from a peer not in the floodfill netDb, they send it to all of the peers
in the floodfill netDb.

At one point, the Kademlia
search/store functionality was still in place. The peers
considered the floodfill peers as always being 'closer' to every key than any
peer not participating in the netDb. We fell back on the Kademlia
netDb if the floodfill peers fail for some reason or another.
However, Kademlia was then disabled completely (see below).

More recently, Kademlia was partially reintroduced in late 2009, as a way
to limit the size of the netdb each floodfill router must store.


### The Introduction of the Floodfill Algorithm

Floodfill was introduced in release 0.6.0.4, keeping Kademlia as a backup algorithm.

*(Adapted from posts by jrandom in the old Syndie, Nov. 26, 2005)*

As I've often said, I'm not particularly bound to any specific technology -
what matters to me is what will get results. While I've been working through
various netDb ideas over the last few years, the issues we've faced in the last
few weeks have brought some of them to a head. On the live net,
with the netDb redundancy factor set to 4 peers (meaning we keep sending an
entry to new peers until 4 of them confirm that they've got it) and the
per-peer timeout set to 4 times that peer's average reply time, we're
**still** getting an average of 40-60 peers sent to before 4 ACK the store.
That means sending 36-56 times as many messages as should go out, each using
tunnels and thereby crossing 2-4 links. Even further, that value is heavily
skewed, as the average number of peers sent to in a 'failed' store (meaning
less than 4 people ACKed the message after 60 seconds of sending messages out)
was in the 130-160 peers range.

This is insane, especially for a network with only perhaps 250 peers on it.

The simplest answer is to say "well, duh jrandom, it's broken. fix it", but
that doesn't quite get to the core of the issue. In line with another current
effort, it's likely that we have a substantial number of network issues due to
restricted routes - peers who cannot talk with some other peers, often due to
NAT or firewall issues. If, say, the K peers closest to a particular netDb
entry are behind a 'restricted route' such that the netDb store message could
reach them but some other peer's netDb lookup message could not, that entry
would be essentially unreachable. Following down those lines a bit further and
taking into consideration the fact that some restricted routes will be created
with hostile intent, its clear that we're going to have to look closer into a
long term netDb solution.

There are a few alternatives, but two worth mentioning in particular. The
first is to simply run the netDb as a Kademlia DHT using a subset of the full
network, where all of those peers are externally reachable. Peers who are not
participating in the netDb still query those peers but they don't receive
unsolicited netDb store or lookup messages. Participation in the netDb would
be both self-selecting and user-eliminating - routers would choose whether to
publish a flag in their routerInfo stating whether they want to participate
while each router chooses which peers it wants to treat as part of the netDb
(peers who publish that flag but who never give any useful data would be
ignored, essentially eliminating them from the netDb).

Another alternative is a blast from the past, going back to the DTSTTCPW
(Do The Simplest Thing That Could Possibly Work)
mentality - a floodfill netDb, but like the alternative above, using only a
subset of the full network. When a user wants to publish an entry into the
floodfill netDb, they simply send it to one of the participating routers, wait
for an ACK, and then 30 seconds later, query another random participant in the
floodfill netDb to verify that it was properly distributed. If it was, great,
and if it wasn't, just repeat the process. When a floodfill router receives a
netDb store, they ACK immediately and queue off the netDb store to all of its
known netDb peers. When a floodfill router receives a netDb lookup, if they
have the data, they reply with it, but if they don't, they reply with the
hashes for, say, 20 other peers in the floodfill netDb.

Looking at it from a network economics perspective, the floodfill netDb is
quite similar to the original broadcast netDb, except the cost for publishing
an entry is borne mostly by peers in the netDb, rather than by the publisher.
Fleshing this out a bit further and treating the netDb like a blackbox, we can
see the total bandwidth required by the netDb to be:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```

where:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```

Plugging in a few values:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```

That, in turn, scales linearly with N (at 100,000 peers, the netDb must
be able to handle netDb store messages totaling 2.5MBps, or, at 300 peers,
7.6KBps).

While the floodfill netDb would have each netDb participant receiving only a
small fraction of the client generated netDb stores directly, they would all
receive all entries eventually, so all of their links should be capable of
handling the full recvKBps. In turn, they'll all need to send
`(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` to keep the other
peers in sync.

A floodfill netDb would not require either tunnel routing for netDb operation
or any special selection as to which entries it can answer 'safely', as the
basic assumption is that they are all storing everything. Oh, and with regards
to the netDb disk usage required, its still fairly trivial for any modern
machine, requiring around 11MB for every 1000 peers `(N * (L + 1) * S)`.

The Kademlia netDb would cut down on these numbers, ideally bringing them to K
over M times their value, with K = the redundancy factor and M being the number
of routers in the netDb (e.g. 5/100, giving a recvKBps of 126KBps and 536MB at
100,000 routers). The downside of the Kademlia netDb though is the increased
complexity of safe operation in a hostile environment.

What I'm thinking about now is to simply implement and deploy a floodfill netDb
in our existing live network, letting peers who want to use it pick out other
peers who are flagged as members and query them instead of querying the
traditional Kademlia netDb peers. The bandwidth and disk requirements at this
stage are trivial enough (7.6KBps and 3MB disk space) and it will remove the
netDb entirely from the debugging plan - issues that remain to be addressed
will be caused by something unrelated to the netDb.

How would peers be chosen to publish that flag saying they are a part of the
floodfill netDb? At the beginning, it could be done manually as an advanced
config option (ignored if the router is not able to verify its external
reachability). If too many peers set that flag, how do the netDb participants
pick which ones to eject? Again, at the beginning it could be done manually as
an advanced config option (after dropping peers which are unreachable). How do
we avoid netDb partitioning? By having the routers verify that the netDb is
doing the flood fill properly by querying K random netDb peers. How do routers
not participating in the netDb discover new routers to tunnel through? Perhaps
this could be done by sending a particular netDb lookup so that the netDb
router would respond not with peers in the netDb, but with random peers outside
the netDb.

I2P's netDb is very different from traditional load bearing DHTs - it only
carries network metadata, not any actual payload, which is why even a netDb
using a floodfill algorithm will be able to sustain an arbitrary amount of
I2P Site/IRC/bt/mail/syndie/etc data. We can even do some optimizations as I2P
grows to distribute that load a bit further (perhaps passing bloom filters
between the netDb participants to see what they need to share), but it seems we
can get by with a much simpler solution for now.

One fact may be worth digging
into - not all leaseSets need to be published in the netDb! In fact, most
don't need to be - only those for destinations which will be receiving
unsolicited messages (aka servers). This is because the garlic wrapped
messages sent from one destination to another already bundles the sender's
leaseSet so that any subsequent send/recv between those two destinations
(within a short period of time) work without any netDb activity.

So, back at those equations, we can change L from 5 to something like 0.1
(assuming only 1 out of every 50 destinations is a server). The previous
equations also brushed over the network load required to answer queries from
clients, but while that is highly variable (based on the user activity), it's
also very likely to be quite insignificant as compared to the publishing
frequency.

Anyway, still no magic, but a nice reduction of nearly 1/5th the bandwidth/disk
space required (perhaps more later, depending upon whether the routerInfo
distribution goes directly as part of the peer establishment or only through
the netDb).


### The Disabling of the Kademlia Algorithm

Kademlia was completely disabled in release 0.6.1.20.

*(Adapted from an IRC conversation with jrandom 11/07)*

Kademlia requires a minimum level of service that the baseline could not offer (bandwidth, cpu),
even after adding in tiers (pure kad is absurd on that point).
Kademlia just wouldn't work. It was a nice idea, but not for a hostile and fluid environment.


### Current Status

The netDb plays a very specific role in the I2P network, and the algorithms
have been tuned towards our needs. This also means that it hasn't been tuned
to address the needs we have yet to run into. I2P is currently
fairly small (a few hundred routers).
There were some calculations that 3-5 floodfill routers should be able to handle
10,000 nodes in the network.
The netDb implementation more than adequately meets our
needs at the moment, but there will likely be further tuning and bugfixing as
the network grows.


### Update of Calculations 03-2008

Current numbers:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```

where:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```

Changes in assumptions:

- L is now about .5, compared to .1 above, due to the popularity of i2psnark
  and other apps.
- F is about .33, but bugs in tunnel testing are fixed in 0.6.1.33, so it will get much better.
- Since netDb is about 2/3 5K routerInfos and 1/3 2K leaseSets, S = 4K.
  RouterInfo size is shrinking in 0.6.1.32 and 0.6.1.33 as we remove unnecessary stats.
- R = tunnel build period: 0.2 was a very low - it was maybe 0.7 -
  but build algorithm improvements in 0.6.1.32 should bring it down to about 0.2
  as the network upgrades. Call it 0.5 now with half the network at .30 or earlier.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```

This just accounts for the stores - what about the queries?


### The Return of the Kademlia Algorithm?

*(Adapted from the I2P meeting Jan. 2, 2007)*

The Kademlia netDb just wasn't working properly.
Is it dead forever or will it be coming back?
If it comes back, the peers in the Kademlia netDb would be a very limited subset
of the routers in the network (basically an expanded number of floodfill peers, if/when the floodfill peers
cannot handle the load).
But until the floodfill peers cannot handle the load (and other peers cannot be added that can), it's unnecessary.


### The Future of Floodfill

*(Adapted from an IRC conversation with jrandom 11/07)*

Here's a proposal: Capacity class O is automatically floodfill.
Hmm.
Unless we're sure, we might end up with a fancy way of DDoS'ing all O class routers.
This is quite the case: we want to make sure the number of floodfill is as small as possible while providing sufficient reachability.
If/when netDb requests fail, then we need to increase the number of floodfill peers, but atm, I'm not aware of a netDb fetch problem.
There are 33 "O" class peers according to my records.
33 is a /lot/ to floodfill to.

So floodfill works best when the number of peers in that pool is firmly limited?
And the size of the floodfill pool shouldn't grow much, even if the network itself gradually would?
3-5 floodfill peers can handle 10K routers iirc (I posted a bunch of numbers on that explaining the details in the old syndie).
Sounds like a difficult requirement to fill with automatic opt-in,
especially if nodes opting in cannot trust data from others.
e.g. "let's see if I'm among the top 5",
and can only trust data about themselves (e.g. "I am definitely O class, and moving 150 KB/s, and up for 123 days").
And top 5 is hostile as well. Basically, it's the same as the tor directory servers - chosen by trusted people (aka devs).
Yeah, right now it could be exploited by opt-in, but that'd be trivial to detect and deal with.
Seems like in the end, we might need something more useful than Kademlia, and have only reasonably capable peers join that scheme.
N class and above should be a big enough quantity to suppress risk of an adversary causing denial of service, I'd hope.
But it would have to be different from floodfill then, in the sense that it wouldn't cause humongous traffic.
Large quantity? For a DHT based netDb?
Not necessarily DHT-based.


### Floodfill TODO List {#todo}

NOTE: The following is not current information.
See [the main netdb page](/docs/overview/network-database) for the current status and a list of future work.

The network was down to only one floodfill for a couple of hours on March 13, 2008
(approx. 18:00 - 20:00 UTC),
and it caused a lot of trouble.

Two changes implemented in 0.6.1.33 should reduce the disruption caused
by floodfill peer removal or churn:

1. Randomize the floodfill peers used for search each time.
   This will get you past the failing ones eventually.
   This change also fixed a nasty bug that would sometimes drive the ff search code insane.
2. Prefer the floodfill peers that are up.
   The code now avoids peers that are shitlisted, failing, or not heard from in
   half an hour, if possible.

One benefit is faster first contact to an I2P Site (i.e. when you had to fetch
the leaseset first). The lookup timeout is 10s, so if you don't start out by
asking a peer that is down, you can save 10s.

There *may* be anonymity implications in these changes.
For example, in the floodfill **store** code, there are comments that
shitlisted peers are not avoided, since a peer could be "shitty" and then
see what happens.
Searches are much less vulnerable than stores -
they're much less frequent, and give less away.
So maybe we don't think we need to worry about it?
But if we want to tweak the changes, it would be easy to
send to a peer listed as "down" or shitlisted anyway, just not
count it as part of the 2 we are sending to
(since we don't really expect a reply).

There are several places where a floodfill peer is selected - this fix addresses only one -
who a regular peer searches from [2 at a time].
Other places where better floodfill selection should be implemented:

1. Who a regular peer stores to [1 at a time]
   (random - need to add qualification, because timeouts are long)
2. Who a regular peer searches to verify a store [1 at a time]
   (random - need to add qualification, because timeouts are long)
3. Who a ff peer sends in reply to a failed search (3 closest to the search)
4. Who a ff peer floods to (all other ff peers)
5. The list of ff peers sent in the NTCP every-6-hour "whisper"
   (although this may not longer be necessary due to other ff improvements)

Lots more that could and should be done:

- Use the "dbHistory" stats to better rate a floodfill peer's integration
- Use the "dbHistory" stats to immediately react to floodfill peers that don't respond
- Be smarter on retries - retries are handled by an upper layer, not in
  FloodOnlySearchJob, so it does another random sort and tries again,
  rather than purposefully skipping the ff peers we just tried.
- Improve integration stats more
- Actually use integration stats rather than just floodfill indication in netDb
- Use latency stats too?
- More improvement on recognizing failing floodfill peers

Recently completed:

- [In Release 0.6.3]
  Implement automatic opt-in
  to floodfill for some percentage of class O peers, based on analysis of the network.
- [In Release 0.6.3]
  Continue to reduce netDb entry size to reduce floodfill traffic -
  we are now at the minimum number of stats required to monitor the network.
- [In Release 0.6.3]
  Manual list of floodfill peers to exclude
  ([blocklists](/docs/overview/threat-model#blocklist) by router ident)
- [In Release 0.6.3]
  Better floodfill peer selection for stores:
  Avoid peers whose netDb is old, or have a recent failed store,
  or are forever-shitlisted.
- [In Release 0.6.4]
  Prefer already-connected floodfill peers for RouterInfo stores, to
  reduce number of direct connections to floodfill peers.
- [In Release 0.6.5]
  Peers who are no longer floodfill send their routerInfo in response
  to a query, so that the router doing the query will know he
  is no longer floodfill.
- [In Release 0.6.5]
  Further tuning of the requirements to automatically become floodfill
- [In Release 0.6.5]
  Fix response time profiling in preparation for favoring fast floodfills
- [In Release 0.6.5]
  Improve blocklisting
- [In Release 0.7]
  Fix netDb exploration
- [In Release 0.7]
  Turn blocklisting on by default, block the known troublemakers
- [Several improvements in recent releases, a continuing effort]
  Reduce the resource demands on high-bandwidth and floodfill routers

That's a long list but it will take that much work to
have a network that's resistant to DOS from lots of peers turning the floodfill switch on and off.
Or pretending to be a floodfill router.
None of this was a problem when we had only two ff routers, and they were both up
24/7. Again, jrandom's absence has pointed us to places that need improvement.

To assist in this effort, additional profile data for floodfill peers are
now (as of release 0.6.1.33) displayed on the "Profiles" page in
the router console.
We will use this to analyze which data are appropriate for
rating floodfill peers.

The network is currently quite resilient, however
we will continue to enhance our algorithms for measuring and reacting to the performance and reliability
of floodfill peers. While we are not, at the moment, fully hardened to the potential threats of
malicious floodfills or a floodfill DDOS, most of the infrastructure is in place,
and we are well-positioned to react quickly
should the need arise.
