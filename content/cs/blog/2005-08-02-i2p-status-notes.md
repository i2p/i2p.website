---
title: "Poznámky ke stavu I2P k 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Opožděná aktualizace zahrnující stav vydání verze 0.6, systém PeerTest, SSU introductions, opravy webového rozhraní I2PTunnel a mnet přes I2P"
categories: ["status"]
---

Ahoj všichni, dnes opožděné poznámky,

* Index:

1) stav verze 0.6 2) PeerTest 3) SSU introductions 4) I2PTunnel webové rozhraní 5) mnet přes i2p 6) ???

* 1) 0.6 status

As you've all seen, we pushed out the 0.6 release a few days ago, and on the whole, things have been going fairly well. Some of the transport improvements since 0.5.* have exposed issues with the netDb implementation, but fixes for much of that is in testing now (as the 0.6-1 build) and will be deployed as 0.6.0.1 fairly shortly. We've also run into some problems with different NAT and firewall setups, as well as MTU issues with some users - issues that weren't present in the smaller test network due to fewer testers. Workarounds have been added in for the worst offenders, but we've got a long term solution coming up soon - peer tests.

* 2) PeerTest

S verzí 0.6.1 nasadíme nový systém pro společné testování a konfiguraci veřejných IP adres a portů. Je integrován do jádra protokolu SSU a bude zpětně kompatibilní. V zásadě umožní, aby se Alice zeptala Boba, jaká je její veřejná IP adresa a číslo portu, a následně Bob požádá Charlieho, aby potvrdil její správnou konfiguraci, nebo aby zjistil, jaké omezení brání správnému fungování. Tato technika není na síti ničím novým, ale je novým přírůstkem do kódové základny i2p a měla by odstranit nejčastější konfigurační chybu.

* 3) SSU introductions

Jak je popsáno ve specifikaci protokolu SSU, bude k dispozici funkce, která lidem za firewally a NATy umožní plně se zapojit do sítě, i když by jinak nemohli přijímat nevyžádané UDP zprávy. Nebude to fungovat ve všech možných situacích, ale pokryje to většinu. Mezi zprávami popsanými ve specifikaci SSU a zprávami potřebnými pro PeerTest existují podobnosti, takže až bude specifikace o tyto zprávy aktualizována, možná budeme moci přibalit introductions (mechanismus zprostředkovaného uvedení spojení pro uzly za NAT/firewallem) ke zprávám PeerTest. V každém případě tyto introductions nasadíme ve verzi 0.6.2 a i to bude zpětně kompatibilní.

* 4) I2PTunnel web interface

Někteří lidé si všimli a nahlásili různé zvláštnosti na webovém rozhraní I2PTunnel a smeghead začal připravovat potřebné opravy – možná by je mohl podrobněji vysvětlit a uvést i předpokládaný termín jejich dokončení?

* 5) mnet over i2p

Ačkoliv jsem nebyl na kanálu, když probíhaly diskuse, z logů se zdá, že icepick dělal nějaké úpravy, aby mnet běžel nad i2p - což umožní distribuovanému úložišti dat mnet nabízet odolné publikování obsahu při anonymním provozu. O postupu na této frontě toho moc nevím, ale vypadá to, že icepick dělá dobré pokroky při propojování s I2P přes SAM a twisted; možná nás ale icepick může blíže informovat?

* 6) ???

OK, děje se toho mnohem víc než je uvedeno výše, ale už mám zpoždění, takže bych měl přestat psát a tuhle zprávu prostě odeslat. Dnes večer se budu moct na chvíli připojit, takže pokud bude někdo online, mohli bychom si dát schůzku kolem 21:30, nebo tak nějak (až se k tomu dostanete ;) v #i2p na obvyklých irc serverech {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

Děkujeme za vaši trpělivost a pomoc s posunem věcí kupředu!

=jr
