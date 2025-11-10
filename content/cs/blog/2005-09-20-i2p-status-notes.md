---
title: "Poznámky ke stavu I2P k 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Týdenní aktualizace shrnující úspěšné vydání 0.6.0.6 se zavedením SSU introductions, bezpečnostní aktualizaci I2Phex 0.1.1.27 a dokončení migrace do kolokace"
categories: ["status"]
---

Ahoj všichni, je zase úterý

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) migrace 4) ???

* 1) 0.6.0.6

S vydáním verze 0.6.0.6 minulou sobotu máme na živé síti v provozu spoustu nových komponent a vy všichni jste odvedli skvělou práci s aktualizací - před pár hodinami už téměř 250 routers přešlo na novou verzi! Síť se zdá být ve slušné kondici a introductions zatím fungují - svou vlastní aktivitu introductions můžete sledovat na http://localhost:7657/oldstats.jsp, kde se dívejte na udp.receiveHolePunch a udp.receiveIntroRelayResponse (stejně tak i udp.receiveRelayIntro, pro ty, kdo jsou za NATem).

Mimochodem, "Status: ERR-Reject" už vlastně není chyba, takže bychom to možná měli změnit na "Status: OK (NAT)"?

Objevilo se několik hlášení o chybách týkajících se Syndie. Nejnověji se vyskytuje chyba, kdy selže synchronizace se vzdálenými uzly, pokud požádáte o stažení příliš mnoha položek najednou (protože jsem pošetile použil HTTP GET místo POST). Do EepGet přidám podporu pro POST, ale zatím zkuste stahovat jen 20 nebo 30 příspěvků najednou. Mimochodem, možná by někdo mohl napsat JavaScript pro stránku remote.jsp, který by nabídl volbu "stáhnout všechny příspěvky od tohoto uživatele" a automaticky zaškrtal všechna zaškrtávací políčka na blogu daného uživatele?

Říká se, že OSX teď funguje bez problémů hned po instalaci a s verzí 0.6.0.6-1 je x86_64 funkční také na Windows i Linuxu. Neslyšel jsem žádné zprávy o problémech s novými instalátory .exe, takže to buď znamená, že vše probíhá hladce, nebo to selhává úplně :)

* 2) I2Phex 0.1.1.27

Na základě některých zpráv o rozdílech mezi zdrojovým kódem a tím, co bylo přibaleno v balíčku verze 0.1.1.26 od legiona, a také kvůli obavám o bezpečnost nativního spouštěče s uzavřeným zdrojovým kódem, jsem do cvs přidal nový i2phex.exe sestavený pomocí launch4j [1] a na i2p file archive [2] jsem sestavil nejnovější verzi z cvs. Není známo, zda legion provedl ve svém zdrojovém kódu před vydáním ještě nějaké další změny, nebo zda je jím zveřejněný zdrojový kód skutečně totožný s tím, co sám sestavil.

Z bezpečnostních důvodů nemohu doporučit používání ani legionova spouštěče s uzavřeným zdrojovým kódem, ani vydání 0.1.1.26. Vydání na webu I2P [2] obsahuje nejnovější kód z cvs, bez úprav.

Můžete reprodukovat sestavení tak, že nejprve provedete checkout (vyzvednutí z repozitáře) a sestavení kódu I2P, poté provedete checkout kódu I2Phex a nakonec spustíte "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (heslo: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

Soubor i2phex.exe uvnitř tohoto ZIP archivu je ve Windows použitelný prostým spuštěním, nebo na *nix/osx přes "java -jar i2phex.exe". Závisí však na tom, že je I2Phex nainstalován v adresáři vedle I2P - (např. C:\Program Files\i2phex\ a C:\Program Files\i2p\), protože odkazuje na některé JAR soubory I2P.

Nechystám se ujmout údržby I2Phexu, ale budu na web dávat budoucí vydání I2Phexu, kdykoli budou v cvs aktualizace. Pokud by někdo chtěl pracovat na webové stránce, kterou bychom mohli zveřejnit a která by jej popsala a představila (sirup, jsi tam?), s odkazy na sirup.i2p, užitečné příspěvky na fóru a legionův seznam aktivních peerů, bylo by to skvělé.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip a     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (podepsáno mým klíčem)

* 3) migration

Vyměnili jsme kolokační servery pro služby I2P, ale na novém stroji by teď mělo být vše plně v provozu - pokud narazíte na něco divného, dejte mi prosím vědět!

* 4) ???

V poslední době proběhla na i2p mailing listu spousta zajímavých diskusí – třeba o Adamově šikovném novém SMTP proxy/filtru a také o několika dobrých příspěvcích na syndie (viděli jste gloinův vzhled na http://gloinsblog.i2p?). Momentálně pracuji na změnách řešících některé dlouhodobé problémy, ale ty nejsou zatím na spadnutí. Pokud má někdo něco dalšího, co by chtěl vznést a probrat, stavte se na schůzce na #i2p ve 20:00 GMT (asi za 10 minut).

=jr
