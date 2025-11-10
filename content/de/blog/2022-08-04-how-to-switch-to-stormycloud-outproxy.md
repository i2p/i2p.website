---
title: "So wechseln Sie zum StormyCloud-Outproxy-Dienst"
date: 2022-08-04
author: "idk"
description: "So wechseln Sie zum StormyCloud-Outproxy-Dienst"
categories: ["general"]
API_Translate: wahr
---

## So wechseln Sie zum StormyCloud-Outproxy-Dienst

**Ein neuer professioneller Outproxy**

For years, I2P has been served by a single default outproxy, `false.i2p` whose reliability has been degrading. Although several competitors have emerged to take up some of the slack, they are mostly unable to volunteer to serve the clients of an entire I2P implementation by default. However, StormyCloud, a professional, non-profit organization which runs Tor exit nodes, has started a new, professional outproxy service which has been tested by members of the I2P community and which will become the new default outproxy in the upcoming release.

**Wer ist StormyCloud**

In ihren eigenen Worten ist StormyCloud:

> Die Mission von StormyCloud Inc: Den Zugang zum Internet als universelles Menschenrecht zu verteidigen. Dadurch schützt die Gruppe die digitale Privatsphäre der Nutzer und baut Gemeinschaft auf, indem sie einen uneingeschränkten Zugang zu Informationen und damit den freien Austausch von Ideen über Grenzen hinweg fördert. Dies ist entscheidend, weil das Internet das mächtigste verfügbare Werkzeug ist, um die Welt positiv zu verändern.

> Hardware: Wir besitzen unsere gesamte Hardware und sind derzeit per Colocation in einem Tier‑4‑Rechenzentrum untergebracht. Aktuell verfügen wir über einen 10GBps‑Uplink mit der Option, ohne großen Aufwand auf 40GBps aufzurüsten. Wir verfügen über ein eigenes ASN und einen eigenen IP‑Adressraum (IPv4 & IPv6).

Um mehr über StormyCloud zu erfahren, besuchen Sie deren [Website](https://www.stormycloud.org/).

Oder besuchen Sie sie unter [I2P](http://stormycloud.i2p/).

**Umstieg auf den StormyCloud Outproxy in I2P**

Um *heute* auf den StormyCloud-Outproxy (Ausgangs-Proxy) zu wechseln, können Sie [den Hidden Services Manager](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0) besuchen. Sobald Sie dort sind, sollten Sie den Wert von **Outproxies** und **SSL Outproxies** auf `exit.stormycloud.i2p` ändern. Nachdem Sie dies getan haben, scrollen Sie bis zum Ende der Seite und klicken Sie auf den Button "Save".

**Vielen Dank an StormyCloud**

Wir danken StormyCloud für die freiwillige Bereitstellung hochwertiger Outproxy-Dienste für das I2P-Netzwerk.
