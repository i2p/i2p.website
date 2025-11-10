---
title: "Poznámky o stavu I2P k 2006-05-02"
date: 2006-05-02
author: "jr"
description: "Zlepšení stavu sítě ve verzi 0.6.1.17, pokrok v probíhajícím přepracování Syndie a nadcházející optimalizace pro router"
categories: ["status"]
---

Ahoj všichni, úterý je tu zase jednou

* Index

1) Stav sítě 2) Stav Syndie 3) ???

* 1) Net status

With another week on 0.6.1.17 under our belt, several of the prime measurements of network health are staying in good shape. We are however seeing some of the remaining problems propogate up to the application layer, namely the recent rise in reconnections on the irc2p servers. Postman, cervantes, Complication, and myself have been digging through various aspects of the network's behavior as it relates to the user-visible performance, and we've tracked down and implemented a few improvements (current CVS HEAD is 0.6.1.17-4). We're still monitoring its behavior and experimenting with some tweaks before pushing it out as 0.6.1.18 though, but thats probably only a few days away.

* 2) Syndie status

Jak již bylo zmíněno, syndie prochází zásadní přestavbou. Když říkám zásadní, mám na mysli téměř kompletně přepracována a znovu implementována ;) Rámec je připraven (včetně průběžného testování pomocí gcj) a první části se dávají dohromady, ale do funkčního stavu je to ještě kus cesty. Jakmile se dostane do stavu, kdy více rukou může pomoci posunout ho dál (a, ehm, *používat ho*), bude k dispozici více informací, ale právě teď je přepracování syndie v podstatě odsunuto na vedlejší kolej, zatímco se pracuje na zlepšeních routeru.

* 3) ???

To je zatím asi všechno k hlášení - jako vždy, pokud máte něco, co chcete probrat, stavte se za pár minut na schůzce a řekněte ahoj!

=jr
