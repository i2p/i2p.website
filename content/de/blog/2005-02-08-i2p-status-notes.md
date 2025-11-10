---
title: "I2P Status Notes for 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Weekly I2P development status notes covering 0.4.2.6 updates, 0.5 tunnel progress with Bloom filters, i2p-bt 0.1.6, and Fortuna PRNG"
categories: ["status"]
---

Hallo zusammen, es ist wieder Zeit für ein Update

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

It doesn't seem like it, but its been over a month since the 0.4.2.6 release came out and things are still in pretty good shape.  There have been a series of pretty useful updates [1] since then, but no real show stopper calling for a new release to get pushed.  However, in the last day or two we've had some really good bugfixes sent in (thanks anon and Sugadude!), and if we weren't on the verge of the 0.5 release, I'd probably package 'er up and push 'er out.  anon's update fixes a border condition in the streaming lib which has been causing many of the timeouts seen in BT and other large transfers, so if you're feeling adventurous, grab CVS HEAD and try 'er out.  Or wait around for the next release, of course.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Lots and lots of progress on the 0.5 front (as anyone on the i2p-cvs list [2] can attest to).  All of the tunnel updates and various performance tweaks have been tested out, and while it doesn't include much in the way of the various [3] enforced ordering algorithms, it does get the basics covered.  We've also integrated a set of (BSD licensed) Bloom filters [4] from XLattice [5], allowing us to detect replay attacks without requiring any per-message memory usage and nearly 0ms overhead.  To accomodate our needs, the filters have been trivially extended to decay so that after a tunnel expires, the filter doesn't have the IVs we saw in that tunnel anymore.

Während ich versuche, so viel wie möglich in die 0.5‑Version hineinzupacken, ist mir auch klar, dass wir mit dem Unerwarteten rechnen müssen – das heißt, der beste Weg, sie zu verbessern, besteht darin, sie in Ihre Hände zu geben und daraus zu lernen, wie sie für Sie funktioniert (und nicht funktioniert). Um dabei zu helfen, werden wir, wie ich bereits erwähnt habe, eine 0.5‑Version veröffentlichen (hoffentlich in der nächsten Woche), die nicht abwärtskompatibel ist, und sie von dort aus weiter verbessern und eine 0.5.1‑Version erstellen, sobald sie bereit ist.

Looking back at the roadmap [6], the only thing being deferred to 0.5.1 is the strict ordering.  There'll also be improvements to the throttling and load balancing over time, I'm sure, but I expect we'll be tweaking that pretty much forever.  There have been some other things discussed that I've hoped to include in 0.5 though, like the download tool and the one-click update code, but it looks like those will be deferred as well.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck has patched up a new i2p-bt release (yay!), available at the usual locations, so get yours while its hot [7].  Between this update and anon's streaming lib patch, I pretty much saturated my uplink while seeding some files, so give it a shot.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Wie bereits im Meeting letzte Woche erwähnt, arbeitet smeghead in letzter Zeit unermüdlich an einer ganzen Reihe verschiedener Updates, und während er darum kämpft, I2P mit gcj zum Laufen zu bringen, sind in einigen JVMs wirklich schlimme PRNG (Pseudozufallszahlengenerator)-Probleme aufgetreten, was uns praktisch dazu zwingt, einen PRNG zu haben, auf den wir uns verlassen können. Nachdem wir von den GNU-Crypto-Leuten Rückmeldung erhalten haben, scheint deren Fortuna-Implementierung, obwohl sie bisher kaum eingesetzt wurde, am besten zu unseren Anforderungen zu passen. Möglicherweise schaffen wir es, sie in das 0.5-Release aufzunehmen, aber wahrscheinlicher ist, dass sie auf 0.5.1 verschoben wird, da wir sie so anpassen wollen, dass sie uns die erforderliche Menge an Zufallsdaten liefern kann.

* 5) ???

Es ist viel los, und in letzter Zeit gab es auch einen Aktivitätsschub im Forum [8], daher bin ich sicher, dass ich einiges verpasst habe. Wie auch immer, schaut in ein paar Minuten einfach beim Meeting vorbei und sagt, was euch auf dem Herzen liegt (oder lest einfach mit und streut ab und zu eine spitze Bemerkung ein)

=jr [8] http://forum.i2p.net/
