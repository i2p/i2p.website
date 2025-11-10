---
title: "Stavové poznámky I2P k 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující degradaci výkonu sítě, plánování vydání verze 0.3.5, potřeby v oblasti dokumentace a pokrok projektu Stasher DHT"
categories: ["status"]
---

No jo, kluci a holky, zase je úterý!

## Rejstřík:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

No, jak jste si všichni všimli, zatímco počet uživatelů v síti zůstal docela stabilní, výkonnost se během posledních několika dní výrazně zhoršila. Příčinou byla série chyb v kódu pro výběr peerů a doručování zpráv, které se projevily, když minulý týden došlo k menšímu DoS útoku. Výsledkem bylo, že v podstatě všem tunnels soustavně selhávaly, což má trochu lavinový efekt. Takže ne, není to jen u vás - síť byla příšerná i pro nás ostatní ;)

Dobrou zprávou ale je, že jsme problémy poměrně rychle opravili a jsou v CVS už od minulého týdne, ale síť bude pro lidi pořád mizerná, dokud nevyjde příští vydání. A v této souvislosti...

## 2) 0.3.5 a 0.4

Zatímco příští vydání bude mít všechny novinky a vylepšení, které máme naplánované pro vydání 0.4 (nový instalátor, nový standard webového rozhraní, nové rozhraní I2PTunnel, oznamovací oblast & služba Windows, vylepšení práce s vlákny, opravy chyb atd.), bylo výmluvné, jak se poslední vydání v průběhu času zhoršovalo. Chci, abychom u těchto vydání postupovali pomaleji, dali jim čas na důkladnější nasazení a aby se případné mouchy projevily. Zatímco simulátor umí prozkoumat základy, nemá žádný způsob, jak simulovat přirozené síťové problémy, které vidíme v živé síti (alespoň zatím ne).

Proto bude příští verze 0.3.5 - doufejme poslední verze řady 0.3.*, ale možná ne, pokud se objeví další problémy. Když se ohlédnu za tím, jak síť fungovala, když jsem byl v červnu offline, věci se začaly zhoršovat asi po dvou týdnech. Proto si myslím, že bychom měli odložit povýšení na řadu 0.4, dokud nebudeme schopni udržet vysokou míru spolehlivosti alespoň po dobu dvou týdnů. To samozřejmě neznamená, že mezitím nebudeme pracovat.

Každopádně, jak bylo zmíněno minulý týden, hypercubus pilně pracuje na novém instalačním systému, vyrovnává se s tím, že věci pořád měním a vyžaduji podporu pro exotické systémy. Během několika příštích dní bychom to měli doladit, abychom během několika příštích dní mohli vydat verzi 0.3.5.

## 3) dokumentace

Jedna z důležitých věcí, které musíme během toho dvoutýdenního "testovacího okna" před verzí 0.4 udělat, je psát dokumentaci jako o život. Zajímá mě, co podle vás v naší dokumentaci chybí - jaké otázky máte, na které musíme odpovědět? Ačkoli bych rád řekl "dobře, teď běžte napsat ty dokumenty", jsem realista, takže vás jen prosím, abyste určili, o čem by ty dokumenty pojednávaly.

Například jeden z dokumentů, na kterém nyní pracuji, je revize modelu hrozeb, který nyní popisuji jako sérii případů použití vysvětlujících, jak může I2P sloužit potřebám různých jednotlivců, včetně funkcionality, útočníků, kterých se daná osoba obává, a způsobů, jak se brání.

Pokud se nedomníváte, že vaše otázka vyžaduje k zodpovězení plnohodnotný dokument, jednoduše ji formulujte jako otázku a můžeme ji přidat do FAQ.

## 4) stasher update

Aum se dnes dříve zastavil na kanálu s aktualizací (zatímco jsem ho zasypával otázkami):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Takže, jak vidíte, spousta, spousta pokroku. I když se klíče ověřují nad vrstvou DHT (distribuovaná hašovací tabulka), je to fakt hustý (podle mě). Jen do toho, aum!

## 5) ???

OK, to je všechno, co jsem chtěl říct (což je dobře, protože schůzka začíná za chvíli)... skočte kolem a řekněte, co chcete!

=jr
