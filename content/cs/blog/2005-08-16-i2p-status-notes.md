---
title: "Poznámky ke stavu I2P k 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Stručná aktualizace zahrnující stav PeerTest, přechod sítě Irc2P, pokrok Feedspace GUI a změnu času schůzky na 20:00 GMT"
categories: ["status"]
---

Ahoj všichni, dnes jen stručné poznámky

* Index:

1) stav PeerTestu
2) Irc2P
3) Feedspace
4) meta
5) ???

* 1) PeerTest status

Jak již bylo zmíněno, chystané vydání 0.6.1 bude obsahovat sérii testů pro pečlivější konfiguraci routeru a pro ověření dosažitelnosti (nebo pro upozornění, co je potřeba udělat), a přestože už je nějaký kód v CVS k dispozici pro dvě sestavení, stále zbývá několik doladění, než to bude fungovat tak hladce, jak je potřeba. V tuto chvíli provádím drobné úpravy testovacího postupu zdokumentovaného [1] tak, že přidávám další paket pro ověření dosažitelnosti Charlieho a oddaluji Bobovu odpověď Alici, dokud Charlie neodpoví. To by mělo snížit počet zbytečných stavů "ERR-Reject", které lidé vídají, protože Bob neodpoví Alici, dokud nebude mít Charlieho, který je k dispozici pro testování (a když Bob neodpoví, Alice jako stav uvidí "Unknown").

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Každopádně, jo, to je vše - verze 0.6.0.2-3 by měla vyjít zítra, jako vydání ji uvolníme až po důkladném otestování.

* 2) Irc2P

Jak bylo zmíněno na fóru [2], uživatelé I2P, kteří používají IRC, si musí aktualizovat konfiguraci, aby přešli na novou IRC síť. Duck bude dočasně offline kvůli [redacted] a místo toho, abychom doufali, že server během té doby nebude mít žádné potíže, postman a smeghead se chopili iniciativy a vybudovali pro vás novou IRC síť. Postman také zrcadlil Duckův tracker a i2p-bt web na [3], a myslím, že jsem na nové IRC síti zahlédl něco o tom, že susi spouští novou instanci IdleRPG (podívejte se do seznamu kanálů pro více informací).

Moje poděkování patří těm, kdo stáli za starou sítí i2pirc (duck, baffled, tým metropipe, postman) a těm, kdo stojí za novou sítí irc2p (postman, arcturus)! Zajímavé služby a obsah dělají I2P hodnotným a je na vás všech, abyste je vytvářeli!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Když už jsme u toho, nedávno jsem pročítal froskův blog a vypadá to, že je tu další pokrok na Feedspace - konkrétně na pěkném malém GUI. Vím, že to možná ještě není připravené k testování, ale jsem si jistý, že nám frosk pošle nějaký kód, až přijde čas. Jen tak mimochodem, taky jsem zaslechl zvěsti o dalším webovém blogovacím nástroji zaměřeném na anonymitu, který se chystá a bude se moct propojit s Feedspace, až bude připravený, ale znovu, jsem si jistý, že se o tom dozvíme víc informací, až to bude připravené.

* 4) meta

Protože jsem takový chamtivý parchant, rád bych posunul setkání trochu dřív - místo 9PM GMT zkusme 8PM GMT. Proč? Protože se to lépe hodí do mého rozvrhu ;) (nejbližší internetové kavárny nemají otevřeno moc dlouho).

* 5) ???

To je pro tuto chvíli asi vše - pokusím se být kvůli dnešnímu večernímu setkání poblíž internetové kavárny, takže se klidně zastavte na #i2p v *8*P GMT na /new/ IRC serverech {irc.postman.i2p, irc.arcturus.i2p}. Možná budeme mít changate bota napojeného na irc.freenode.net - chce ho někdo provozovat?

čau, =jr
