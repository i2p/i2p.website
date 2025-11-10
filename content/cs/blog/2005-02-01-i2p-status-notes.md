---
title: "Poznámky ke stavu I2P k 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující pokrok v šifrování tunnel ve verzi 0.5, nový NNTP server a technické návrhy"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní status

* Index

1) stav 0.5 2) nntp 3) technické návrhy 4) ???

* 1) 0.5 status

V oblasti verze 0.5 došlo k velkému pokroku, včera s velkou dávkou commitů. Většina routeru nyní používá nové tunnel encryption a tunnel pooling [1] a na testovací síti to funguje dobře. Stále zbývá integrovat několik klíčových částí a kód je samozřejmě zpětně nekompatibilní, ale doufám, že se nám podaří nasadit ve větším měřítku někdy příští týden.

Jak již bylo zmíněno, počáteční vydání 0.5 poskytne základ, na němž mohou fungovat různé strategie výběru/řazení peerů pro tunnel. Začneme se základní sadou konfigurovatelných parametrů pro průzkumné a klientské pooly, ale pozdější vydání pravděpodobně zahrnou další možnosti pro různé uživatelské profily.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Jak je zmíněno na LazyGuyově webu [2] a na mém blogu [3], máme na síti nový NNTP server v provozu, dostupný na adrese nntp.fr.i2p. Zatímco LazyGuy spustil několik skriptů suck [4] pro načtení několika mailing listů z gmane, obsah je z velké části od uživatelů I2P, pro ně a jimi vytvářený. jdot, LazyGuy a já jsme provedli průzkum, které newsové klienty lze používat bezpečně, a zdá se, že existují poměrně jednoduchá řešení. Pokyny ke spuštění slrn [5] pro anonymní čtení a odesílání příspěvků do diskusních skupin najdete na mém blogu.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion a další zveřejnili na wiki ugha [6] sérii RFC k různým technickým otázkám, aby pomohli rozpracovat některé složitější problémy na úrovni klientů a aplikací. Prosíme, používejte ji jako místo k diskusi o otázkách pojmenování, aktualizacích SAM, nápadech na swarming (rojení v P2P) a podobně - když tam něco zveřejníte, můžeme všichni spolupracovat, každý na svém, a dosáhnout lepšího výsledku.

[6] http://ugha.i2p/I2pRfc

* 4) ???

To je pro tuto chvíli všechno (což je ostatně dobře, protože schůzka za chvíli začíná). Jako vždy se podělte o své názory kdykoli a kdekoli :)

=jr
