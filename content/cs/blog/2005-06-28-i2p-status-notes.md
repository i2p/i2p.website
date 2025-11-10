---
title: "Stavové poznámky I2P k 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Týdenní aktualizace zaměřená na plány nasazení SSU transportu, dokončení odměnového programu na jednotkové testy a licenční úvahy a na stav Kaffe Java"
categories: ["status"]
---

Ahoj všichni, je tu zase čas na týdenní aktualizaci

* Index

1) Stav SSU 2) Stav jednotkových testů 3) Stav Kaffe 4) ???

* 1) SSU status

U transportu SSU došlo k dalšímu pokroku a můj aktuální názor je, že po dalším testování v živé síti budeme moci nasadit jako verzi 0.6 bez většího prodlení. První vydání SSU nebude zahrnovat podporu pro lidi, kteří nemohou otevřít port ve firewallu nebo upravit svůj NAT, ale to bude nasazeno ve verzi 0.6.1. Až bude 0.6.1 venku, otestovaná a bude šlapat jako hodinky (alias 0.6.1.42), přejdeme na 1.0.

Můj osobní sklon je zcela vypustit TCP transport v průběhu zavádění SSU transportu, aby lidé nemuseli mít aktivní oba (přesměrovávat jak porty TCP, tak UDP) a aby vývojáři nemuseli udržovat kód, který není nezbytný. Má na to někdo silný názor?

* 2) Unit test status

Jak bylo zmíněno minulý týden, Comwiz se přihlásil o první fázi odměny za jednotkové testy (hurá, Comwiz! díky také duck & zab za financování odměny!). Kód byl zkomitován do CVS a v závislosti na vašem lokálním nastavení možná budete moci vygenerovat junit a clover reporty tak, že přejdete do adresáře i2p/core/java a spustíte "ant test junit.report" (počkáte asi hodinu...) a poté zobrazíte i2p/reports/core/html/junit/index.html. Případně můžete spustit "ant useclover test junit.report clover.report" a zobrazit i2p/reports/core/html/clover/index.html.

Nevýhoda u obou sad testů souvisí s tím pošetilým konceptem, kterému vládnoucí třída říká "autorské právo". Clover je komerční produkt, i když lidé z cenqua umožňují jeho bezplatné používání vývojářům open source (a laskavě souhlasili, že nám udělí licenci). Abyste mohli generovat reporty Clover, musíte mít Clover nainstalovaný lokálně - já mám clover.jar v ~/.ant/lib/, vedle svého licenčního souboru. Většina lidí Clover potřebovat nebude, a protože budeme reporty zveřejňovat na webu, k žádné ztrátě funkčnosti tím, že ho nenainstalujete, nedojde.

Na druhé straně však narážíme na opačnou stránku autorského práva, když vezmeme v úvahu samotný framework pro jednotkové testy – junit je vydán pod licencí IBM Common Public License 1.0, která podle FSF [1] není kompatibilní s GPL. Ačkoli sami nemáme žádný kód pod GPL (alespoň ne v jádru nebo v routeru), při pohledu zpět na naši licenční politiku [2] je naším cílem v konkrétnostech toho, jak věci licencujeme, umožnit co největšímu počtu lidí používat to, co vzniká, protože anonymita má ráda společnost.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Protože někteří lidé nepochopitelně uvolňují software pod licencí GPL, dává smysl, abychom se snažili umožnit jim používat I2P bez omezení. Přinejmenším to znamená, že nesmíme připustit, aby skutečná funkcionalita, kterou zpřístupňujeme, byla závislá na kódu pod licencí CPL (např. junit.framework.*). Rád bych to rozšířil tak, aby se to vztahovalo i na jednotkové testy, ale junit se zdá být lingua franca testovacích frameworků (a nemyslím si, že by bylo byť vzdáleně rozumné říct "hej, pojďme si postavit vlastní public domain (volné dílo) framework pro jednotkové testy!", vzhledem k našim prostředkům).

S ohledem na to všechno navrhuji následující. Zahrneme junit.jar do CVS a použijeme ho, když lidé spustí jednotkové testy, ale samotné jednotkové testy nebudou sestaveny do i2p.jar ani router.jar a nebudou součástí vydání. Případně můžeme zpřístupnit dodatečnou sadu JAR souborů (i2p-test.jar a router-test.jar), pokud to bude nutné, ale ty by nebyly použitelné aplikacemi licencovanými pod GPL (protože závisejí na junit).

=jr
