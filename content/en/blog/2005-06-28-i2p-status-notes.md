---
title: "I2P Status Notes for 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Weekly update covering SSU transport deployment plans, unit test bounty completion and licensing considerations, and Kaffe Java status"
categories: ["status"]
---

Hi y'all, weekly update time again

* Index
1) SSU status
2) Unit test status
3) Kaffe status
4) ???

* 1) SSU status

There has been some more progress on the SSU transport, and my current thinking will be that after some more live net testing, we'll be able to deploy as 0.6 without much delay. The first SSU release will not include support for people who cannot poke a hole in their firewall or adjust their NAT, but that will be rolled out in 0.6.1. After 0.6.1 is out, tested, and kicking ass (aka 0.6.1.42), we'll move on over to 1.0.

My personal leaning is towards dropping the TCP transport completely as the SSU transport rolls out so that people won't need to have both enabled (forwarding both TCP and UDP ports) and so that the coders won't need to maintain code that isn't necessary. Anyone have any strong feelings on this?

* 2) Unit test status

As mentioned last week, Comwiz has come forward to claim the first phase of the unit test bounty (yay Comwiz!  thanks duck & zab for funding the bounty too!). The code has been committed to CVS and, depending on your local setup, you may be able to generate the junit and clover reports by going into the i2p/core/java directory and running "ant test junit.report" (wait about an hour...) and view i2p/reports/core/html/junit/index.html. On the other hand, you can run "ant useclover test junit.report clover.report" and view i2p/reports/core/html/clover/index.html.

The downside to both sets of tests has to do with that foolish concept the ruling class calls "copyright law". Clover is a commercial product, though the folks over at cenqua allow its free use by open source developers (and they have kindly agreed to grant us a license). To generate the clover reports, you need to have clover installed locally - I have clover.jar in ~/.ant/lib/, next to my license file. Most people won't need clover, and since we'll be publishing the reports on the web, there is no loss of functionality by not installing it.

On the other hand, we're being bit by the other side of copyright law when we take into consideration the unit test framework itself - junit is released under the IBM Common Public License 1.0, which, according to the FSF [1], is not GPL compatible. Now, while we don't have any GPL code ourselves (at least not in the core or the router), looking back at our license policy [2], our aim in the particulars of how we license things is to allow as many people as possible to use what is being created, since anonymity loves company.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses
[2] http://www.i2p.net/licenses

Since some people inexplicably release software under the GPL, it makes sense for us to strive to allow them to use I2P without constraint. At the very least, that means we can't allow the actual functionality we expose to be dependent upon the CPL'ed code (e.g. junit.framework.*). I'd like to extend that to include the unit tests as well, but junit seems to be the lingua franca of testing frameworks (and I don't think it'd be anywhere near sane to say "hey, lets build our own public domain unit test framework!", given our resources).

Given all that, here's what I'm thinking. We'll bundle junit.jar in CVS and use it when people run the unit tests, but the unit tests themselves will not be built into i2p.jar or router.jar, and will not be pushed out in releases. We may expose an additional set of jars (i2p-test.jar and router-test.jar), if necessary, but those would not be usable by GPL'ed applications (since they depend upon junit).

=jr