---
title: "Stavové poznámky I2P ze dne 2006-10-10"
date: 2006-10-10
author: "jr"
description: "vydání 0.6.1.26 s pozitivní odezvou, Syndie 0.910a se blíží k verzi 1.0, a vyhodnocení distribuovaného systému správy verzí pro Syndie"
categories: ["status"]
---

Ahoj všem, tento týden stručné poznámky ke stavu

* Index

1) 0.6.1.26 a stav sítě 2) Stav vývoje Syndie 3) Znovu k distribuované správě verzí 4) ???

* 1) 0.6.1.26 and network status

Před pár dny jsme vydali novou verzi 0.6.1.26, která zahrnuje spoustu vylepšení pro i2psnark od zzz a několik nových bezpečnostních kontrol NTP od Complication, a ohlasy byly pozitivní. Zdá se, že síť mírně roste bez nových zvláštních jevů, i když někteří lidé stále mají potíže se sestavováním svých tunnels (jak tomu bylo vždy).

* 2) Syndie development status

Neustále přibývají další a další vylepšení a aktuální alfa verze je 0.910a. Seznam funkcí pro 1.0 je v podstatě splněn, takže teď jde hlavně o opravování chyb a dokumentaci. Stavte se na #i2p, pokud chcete pomoci s testováním :)

Také na kanálu proběhly některé diskuse o návrzích GUI pro Syndie - meerboop přišel s pár skvělými nápady a pracuje na jejich zdokumentování. Syndie GUI je hlavní součástí vydání Syndie 2.0, takže čím dřív to rozjedeme, tím dřív ovládneme svě^W^W^W^W budeme moct vypustit Syndie na nic netušící masy.

There's also a new proposal in my Syndie blog regarding bug and feature request tracking using Syndie itself. For ease of access, I've made a plain text export of that post up on the web - page 1 is at <http://dev.i2p.net/~jrandom/bugsp1.txt> and page 2 is at <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

Jednou z věcí, které je u Syndie ještě potřeba vyřešit, je volba veřejného systému správy verzí a, jak už bylo dříve zmíněno, je nutná distribuovaná a offline funkčnost. Procházím zhruba půl tuctu open-sourceových systémů (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville), pročítám jejich dokumentaci, zkouším je a mluvím s jejich vývojáři. Momentálně se z hlediska funkčnosti a bezpečnosti jako nejlepší jeví monotone a bzr (u nedůvěryhodných repozitářů potřebujeme silnou kryptografii, abychom měli jistotu, že stahujeme pouze autentické změny) a těsná integrace kryptografie v monotone působí velmi lákavě. Pořád se ještě prokousávám několika stovkami stran dokumentace, ale podle toho, co jsem probíral s vývojáři monotone, to vypadá, že dělají všechno Správně.

Samozřejmě, bez ohledu na to, pro jaký dvcs (distribuovaný systém správy verzí) se nakonec rozhodneme, budou všechna vydání k dispozici ve formátu prostého tarballu (tar archivu) a patche budou přijímány k revizi v prostém formátu diff -uw. Přesto budu rád, když ti, kdo by zvažovali zapojení do vývoje, se podělí o své názory a preference.

* 4) ???

Jak vidíte, jako vždy se toho děje spousta. Na fóru také proběhla další diskuse v tom vlákně "solve world hunger", takže se na to podívejte na <http://forum.i2p.net/viewtopic.php?t=1910>

Pokud k tomu máte ještě co dodat, přijďte prosím dnes večer na naši vývojářskou schůzku na #i2p, nebo napište na fórum či mailing list!

=jr
