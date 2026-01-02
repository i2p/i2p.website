---
title: "Typy MIME I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Přehled

Definice typů MIME pro běžné formáty souborů I2P.
Zahrňte definice do balíčků pro Debian.
Poskytněte obsluhu pro typ .su3 a případně další.


## Motivace

Aby bylo jednodušší osévat a instalovat pluginy při stahování s prohlížečem,
potřebujeme typ MIME a obsluhu pro soubory .su3.

Zatímco jsme u toho, po naučení se, jak psát soubory definice MIME podle standardu freedesktop.org, můžeme přidat definice pro další běžné
typy souborů I2P.
I když jsou méně užitečné pro soubory, které se obvykle nestahují, jako je
databáze blokovaných adresářů (hostsdb.blockfile), tyto definice umožní
soubory lépe identifikovat a ikony zobrazit při použití grafického
prohlížeče adresářů, jako je "nautilus" na Ubuntu.

Tím, že standardizujeme typy MIME, může každá implementace routeru napsat
obsluhu podle potřeby a soubor definice MIME může být sdílen mezi všemi
implementacemi.


## Návrh

Napište XML zdrojový soubor podle standardu freedesktop.org a zahrňte ho
do balíčků pro Debian. Soubor je "debian/(balíček).sharedmimeinfo".

Všechny typy MIME I2P začnou s "application/x-i2p-", kromě jrobin rrd.

Obsluhy pro tyto typy MIME jsou specifické pro aplikaci a zde nebudou
specifikovány.

Definice zahrneme také s Jetty a zahrneme je se softwarem pro osev nebo pokyny.


## Specifikace

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(obecný)	application/x-i2p-su3

.su3	(aktualizace routeru)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(osev)	application/x-i2p-su3-reseed

.su3	(novinky)		application/x-i2p-su3-news

.su3	(blokovací seznam)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Poznámky

Ne všechny formáty souborů uvedené výše jsou používány neveřejnými implementacemi routerů;
některé nemusí být dokonce dobře specifikovány. Avšak jejich zdokumentování zde
může umožnit budoucí konzistenci mezi implementacemi.

Některé přípony souborů jako ".config", ".dat" a ".info" se mohou překrývat s jinými
typy MIME. Tyto mohou být rozlišeny dodatečnými daty jako
plným názvem souboru, vzorem názvu souboru nebo magickými čísly.
Příklady naleznete v návrhu souboru i2p.sharedmimeinfo v vlákně zzz.i2p.

Důležité jsou typy .su3 a ty mají jak
jedinečnou příponu, tak robustní definice magických čísel.


## Migrace

Není použitelný.
