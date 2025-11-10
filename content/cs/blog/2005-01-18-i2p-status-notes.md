---
title: "Poznámky ke stavu I2P ze dne 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující stav sítě, návrh směrování pomocí tunnel pro verzi 0.5, i2pmail.v2 a bezpečnostní opravu azneti2p_0.2"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

* Index

1) Stav sítě 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, není tu moc co hlásit - věci pořád fungují stejně jako minulý týden, velikost sítě je pořád dost podobná, možná o něco větší. Nějaké pěkné nové stránky se objevují - podrobnosti viz fórum [1] a orion [2].

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Díky pomoci postman, dox, frosk a cervantes (a všem, kdo přenesli data přes své routers ;), jsme shromáždili statistiky velikosti zpráv za celý den [3]. Jsou tam dvě sady statistik – výška a šířka zvětšení. To bylo motivované snahou prozkoumat dopad různých strategií paddingu zpráv (vyplňování) na zatížení sítě, jak je vysvětleno [4] v jednom z návrhů pro 0.5 tunnel routing. (ooOOoo hezké obrázky).

Děsivé na tom, co jsem v tom našel, když jsem se tím probíral, bylo, že i při použití docela jednoduchých ručně laděných hranic paddingu (výplně) by padding na ty pevné velikosti stejně vedl k promrhání více než 25 % šířky pásma. Jo, já vím, tohle dělat nebudeme. Možná vy všichni dokážete vymyslet něco lepšího, když se prohrabete těmi surovými daty.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

Vlastně nás ten odkaz [4] přivádí ke stavu plánů pro směrování tunnel ve verzi 0.5.  Jak Connelly uvedl [5], v poslední době probíhá na IRC hodně diskusí o některých návrzích, do nichž polecat, bla, duck, nickster, detonate a další přispívají návrhy a zvídavými otázkami (ok, a rýpanci ;).  Po něco málo více než týdnu jsme narazili na potenciální zranitelnost v [4], týkající se protivníka, který byl nějakým způsobem schopen převzít inbound tunnel gateway (vstupní bránu pro inbound tunnel) a zároveň ovládal jeden z dalších uzlů později v tom tunnel.  Ačkoli ve většině případů by to samo o sobě neodhalilo koncový bod a s růstem sítě by to bylo pravděpodobnostně těžké provést, pořád je to na nic (tm).

A do hry vstupuje [6].  To odstraňuje tento problém, umožňuje nám mít tunnel libovolné délky a vyřeší světový hlad [7].  Nicméně to otevírá další problém, kdy by útočník mohl vytvářet smyčky v rámci tunnel, ale na základě návrhu [8], který loni předložil Taral ohledně session tags (identifikátory relace) používaných u ElGamal/AES, můžeme minimalizovat způsobené škody použitím řady synchronizovaných pseudonáhodných generátorů čísel [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] hádejte, které tvrzení je nepravdivé? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Nedělejte si starosti, pokud to výše zní matoucí - díváte se na vnitřnosti některých zapeklitých návrhových problémů, které se otevřeně rozebírají. Pokud to výše *nezní* matoucí, ozvěte se, protože vždy hledáme další hlavy, které s námi tohle proberou :)

Každopádně, jak jsem zmiňoval na mailing listu [10], dál bych rád implementoval druhou strategii [6], abychom dořešili zbývající detaily.  Aktuální plán pro 0.5 je dát dohromady všechny zpětně nekompatibilní změny - nové šifrování pro tunnel, atd - a vydat to jako 0.5.0, a až se to v síti ustálí, přejít k dalším částem 0.5 [11], například upravit pooling strategy (seskupovací strategii) tak, jak je popsáno v návrzích, a vydat to jako 0.5.1.  Doufám, že se nám stále podaří stihnout 0.5.0 do konce měsíce, ale uvidíme.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

Nedávno postman zveřejnil návrh akčního plánu pro e‑mailovou infrastrukturu nové generace [12] a vypadá to fakt skvěle. Samozřejmě si můžeme vysnít ještě další vychytávky, ale v mnoha ohledech má velmi povedenou architekturu. Podívejte se na to, co je zatím zdokumentováno [13], a dejte postmanovi vědět, co si o tom myslíte!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Jak jsem psal na mailing listu [14], původní plugin azneti2p pro azureus měl vážnou chybu, která narušovala anonymitu. Problém spočíval v tom, že u smíšených torrentů, kde někteří uživatelé jsou anonymní a jiní nikoli, anonymní uživatelé kontaktovali neanonymní uživatele /přímo/ místo přes I2P. Paul Gardner a ostatní vývojáři azureusu reagovali velmi rychle a okamžitě vydali záplatu. Problém, který jsem zaznamenal, se již v azureus v. 2203-b12 + azneti2p_0.2 nevyskytuje.

Neprošli jsme zatím kód a neprovedli jeho audit kvůli případným problémům s anonymitou, takže "používejte na vlastní riziko" (Na druhou stranu říkáme totéž o I2P, před vydáním verze 1.0). Pokud se na to cítíte, vím, že vývojáři Azureusu by ocenili více zpětné vazby a hlášení chyb k zásuvnému modulu. Samozřejmě budeme informovat, pokud se dozvíme o jakýchkoli dalších problémech.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Děje se toho hodně, jak vidíte. Myslím, že to je asi vše z mé strany, ale prosím zastavte se na schůzce za 40 minut, pokud je ještě něco, co byste chtěli probrat (nebo pokud si prostě chcete zanadávat na výše uvedené)

=jr
