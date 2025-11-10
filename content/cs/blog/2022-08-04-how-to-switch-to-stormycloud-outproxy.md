---
title: "Jak přejít na službu StormyCloud Outproxy"
date: 2022-08-04
author: "idk"
description: "Jak přejít na službu StormyCloud Outproxy"
categories: ["general"]
---

## Jak přepnout na službu StormyCloud Outproxy

**Nový profesionální outproxy (výstupní proxy server)**

For years, I2P has been served by a single default outproxy, `false.i2p` whose reliability has been degrading. Although several competitors have emerged to take up some of the slack, they are mostly unable to volunteer to serve the clients of an entire I2P implementation by default. However, StormyCloud, a professional, non-profit organization which runs Tor exit nodes, has started a new, professional outproxy service which has been tested by members of the I2P community and which will become the new default outproxy in the upcoming release.

**Kdo jsou StormyCloud**

Podle jejich vlastních slov je StormyCloud:

> Poslání společnosti StormyCloud Inc: Bránit přístup k internetu jako univerzální lidské právo. Tímto skupina chrání elektronické soukromí uživatelů a buduje komunitu podporou neomezeného přístupu k informacím, a tím i svobodné výměny myšlenek napříč hranicemi. To je zásadní, protože internet je nejmocnějším dostupným nástrojem pro dosažení pozitivních změn ve světě.

> Hardware: Vlastníme veškerý náš hardware a aktuálně kolokujeme v datovém centru Tier 4. Nyní máme uplink 10GBps s možností upgradu na 40GBps bez nutnosti větších změn. Máme vlastní ASN a IP adresní prostor (IPv4 & IPv6).

Chcete-li se o StormyCloud dozvědět více, navštivte jejich [webové stránky](https://www.stormycloud.org/).

Nebo je navštivte na [I2P](http://stormycloud.i2p/).

**Přepnutí na StormyCloud Outproxy v I2P**

Chcete-li přepnout na StormyCloud outproxy (výstupní proxy) *dnes*, můžete navštívit [Správce skrytých služeb](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0). Až tam budete, změňte hodnoty **Outproxies** a **SSL Outproxies** na `exit.stormycloud.i2p`. Jakmile to provedete, posuňte se na konec stránky a klikněte na tlačítko "Save".

**Děkujeme StormyCloud**

Rádi bychom poděkovali StormyCloud za dobrovolné poskytování vysoce kvalitních služeb outproxy (výstupní proxy) pro síť I2P.
