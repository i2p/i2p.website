---
title: "Stavové poznámky I2P k 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Týdenní aktualizace pokrývající obnovu služeb, pokrok v testování SSU a analýzu kryptografické vrstvy I2CP za účelem možného zjednodušení"
categories: ["status"]
---

Ahoj všichni, je tu zase ta část týdne

* Index

1) squid/www/cvs/dev.i2p obnoveno 2) testování SSU 3) kryptografie I2CP 4) ???

* 1) squid/www/cvs/dev.i2p restored

Po urputném boji s několika kolokačními servery se podařilo obnovit některé ze starých služeb – squid.i2p (jeden ze dvou výchozích výstupních proxy), www.i2p (bezpečný odkaz na www.i2p.net), dev.i2p (bezpečný odkaz na dev.i2p.net, kde jsou k nalezení archivy mailing listů, cvsweb a výchozí netDb seeds), a cvs.i2p (bezpečný odkaz na náš CVS server - cvs.i2p.net:2401). Můj blog je stále mimo provoz, ale jeho obsah se stejně ztratil, takže dříve či později bude potřeba začít znovu od začátku. Teď, když jsou tyto služby spolehlivě zpět online, je čas posunout se k ...

* 2) SSU testing

Jak je zmíněno v tom malém žlutém rámečku na konzoli každého routeru, zahájili jsme další kolo testování SSU v živé síti. Testy nejsou pro každého, ale pokud jste dobrodružné povahy a jste v pohodě s ruční konfigurací, podívejte se na podrobnosti uvedené na konzoli vašeho routeru (http://localhost:7657/index.jsp). Může proběhnout několik kol testování, ale neočekávám žádné zásadní změny SSU před vydáním 0.6 (0.6.1 přidá podporu pro ty, kteří nemohou přesměrovat své porty ani jiným způsobem přijímat příchozí UDP spojení).

* 3) I2CP crypto

Při opětovné práci na nové úvodní dokumentaci mám určitý problém obhájit dodatečnou vrstvu šifrování prováděnou v rámci I2CP SDK. Původním záměrem kryptografické vrstvy I2CP bylo poskytnout základní end-to-end ochranu přenášených zpráv a také umožnit klientům I2CP (tj. I2PTunnel, SAM bridge, I2Phex, azneti2p atd.) komunikovat přes nedůvěryhodné routery. Jak však implementace postupovala, end-to-end ochrana vrstvy I2CP se stala nadbytečnou, protože všechny klientské zprávy jsou routerem end-to-end šifrovány uvnitř garlic messages (garlic zprávy), přičemž je přiložen odesílatelův leaseSet a někdy i zpráva o stavu doručení. Tato garlic vrstva již poskytuje end-to-end šifrování od odesílatelova routeru k příjemcovu routeru - jediný rozdíl je v tom, že to nechrání proti tomu, když je sám ten router zlovolný.

Když se však podívám na předvídatelné případy použití, nedokážu přijít na smysluplný scénář, v němž by místní router nebyl důvěryhodný. Přinejmenším I2CP šifrování skrývá pouze obsah zprávy přenášené z routeru - router přesto musí vědět, na jakou destination (cílový identifikátor v I2P) má být odeslána. Pokud je to nutné, můžeme přidat SSH/SSL I2CP listener, aby I2CP klient a router mohli běžet na oddělených strojích, nebo lidé, kteří se do takové situace dostanou, mohou použít existující tunelovací nástroje.

Jen pro zopakování aktuálně používaného vrstvení kryptografie, máme:  * End-to-end vrstva ElGamal/AES+SessionTag v rámci I2CP, šifrující od
    destinace odesílatele k destinaci příjemce.  * Vrstva end-to-end garlic encryption routeru
    (ElGamal/AES+SessionTag), šifrující od routeru odesílatele k
    routeru příjemce.  * Vrstva šifrování pro oba příchozí a odchozí tunnel
    na skocích podél každého (ale ne mezi odchozím
    koncovým bodem a příchozí bránou).  * Transportní šifrovací vrstva mezi jednotlivými routery.

Chci být poměrně opatrný, pokud jde o odstranění jedné z těch vrstev, ale nechci plýtvat našimi prostředky na zbytečnou práci. Navrhuji odstranit první vrstvu šifrování I2CP (ale stále samozřejmě ponechat autentizaci používanou během navázání relace I2CP, autorizaci leaseSet a autentizaci odesílatele). Napadá někoho důvod, proč bychom ji měli zachovat?

* 4) ???

To je zatím asi vše, ale jako vždy se toho děje hodně. Ani tento týden není v plánu žádné setkání, ale pokud má někdo něco, co by chtěl probrat, neváhejte to poslat na mailing list (poštovní konferenci) nebo na fórum. Také, i když pročítám historii chatu (scrollback) na #i2p, obecné dotazy nebo připomínky by se měly posílat na mailing list, aby se do diskuse mohlo zapojit více lidí.

=jr
