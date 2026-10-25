---
title: "Diskuze o pojmenování"
description: "Historická debata o modelu pojmenování I2P a proč byly odmítnuty globální schémata ve stylu DNS"
slug: "naming"
aliases:
  - "/cs/docs/legacy/naming"
  - "/cs/docs/legacy/naming/"
  - "/cs/naming_discussion"
  - "/cs/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

POZNÁMKA: Následující text je diskusí o důvodech stojících za systémem jmenování I2P, běžných argumentech a možných alternativách. Aktuální dokumentaci najdete na [stránce o jmenování](/docs/naming).

## Zamítnuté alternativy

Pojmenovávání v rámci I2P je často diskutované téma od samého počátku s obhájci napříč spektrem možností. Avšak vzhledem k inherentní potřebě I2P pro bezpečnou komunikaci a decentralizovaný provoz je tradiční pojmenovávací systém ve stylu DNS jasně vyloučen, stejně jako hlasovací systémy typu "vítězí většina".

I2P však nepodporuje používání služeb podobných DNS, protože škoda způsobená únosem stránky může být obrovská - a nezabezpečené destinace nemají žádnou hodnotu. DNSsec sám stále spoléhá na registrátory a certifikační autority, zatímco u I2P nemohou být požadavky odeslané na destinaci zachyceny ani odpověď zfalšována, protože jsou šifrovány pomocí veřejných klíčů destinace, a destinace sama je pouze pár veřejných klíčů a certifikát. Systémy ve stylu DNS naproti tomu umožňují kterémukoli ze jmenných serverů na cestě vyhledávání provést jednoduché útoky typu odmítnutí služby a spoofingu. Přidání certifikátu ověřujícího odpovědi jako podepsané nějakou centralizovanou certifikační autoritou by vyřešilo mnoho problémů s nepřátelskými jmennými servery, ale ponechalo by otevřené replay útoky stejně jako útoky nepřátelských certifikačních autorit.

Pojmenovávání pomocí hlasování je také nebezpečné, zvláště vzhledem k účinnosti Sybil útoků v anonymních systémech - útočník může jednoduše vytvořit libovolně vysoký počet protistran a "hlasovat" s každou z nich, aby převzal daný název. Metody proof-of-work lze použít k tomu, aby identita nebyla zdarma, ale jak síť roste, zatížení potřebné ke kontaktování všech za účelem provedení online hlasování je neproveditelné, nebo pokud není dotazována celá síť, mohou být dosažitelné různé sady odpovědí.

Stejně jako u internetu však I2P udržuje návrh a provoz systému jmenování mimo komunikační vrstvu (podobnou IP). Přiložená knihovna pro jmenování obsahuje jednoduché rozhraní poskytovatele služeb, do kterého se mohou připojit [alternativní systémy jmenování](#alternatives), což umožňuje koncovým uživatelům rozhodnout, jaké kompromisy v oblasti jmenování preferují.

## Diskuze

Viz také [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Komentáře od jrandom

(převzato z příspěvku ve starém Syndie, 26. listopadu 2005)

Q: Co dělat, když se některé hosty neshodnou na jedné adrese a některé adresy fungují, jiné ne? Kdo je správným zdrojem názvu?

A: Neděláte to. Toto je ve skutečnosti zásadní rozdíl mezi jmény na I2P a tím, jak funguje DNS - jména v I2P jsou lidsky čitelná, bezpečná, ale **nejsou globálně jedinečná**. To je záměr a inherentní součást naší potřeby bezpečnosti.

Pokud bych vás nějak dokázal přesvědčit, abyste změnili cíl spojený s nějakým jménem, úspěšně bych si "převzal" stránku, a to za žádných okolností není přijatelné. Místo toho děláme jména **lokálně jedinečnými**: jsou to to, co *vy* používáte k označení stránky, stejně jako si můžete říkat věcem, jak chcete, když si je přidáte do záložek prohlížeče nebo do seznamu kontaktů vašeho IM klienta. Tomu, komu říkáte "Šéf", může někdo jiný říkat "Sára".

Jména nebudou nikdy bezpečně čitelná pro člověka a globálně jedinečná současně.

### Komentáře od zzz

Následující text od zzz je přehled několika běžných stížností na systém pojmenování I2P.

- **Neefektivnost:** Celý soubor hosts.txt se stahuje (pokud se změnil, protože eepget používá hlavičky etag a last-modified). Momentálně má přibližně 400K pro téměř 800 hostů.

Pravda, ale to není mnoho provozu v kontextu I2P, které je samo o sobě velmi neefektivní (floodfill databáze, obrovská režie šifrování a padding, garlic routing atd.). Pokud byste si stáhli soubor hosts.txt od někoho každých 12 hodin, průměrně to vyjde na asi 10 bajtů/sec.

Jak je obvykle v I2P zvykem, existuje zde zásadní kompromis mezi anonymitou a efektivitou. Někteří by řekli, že používání etag a last-modified hlaviček je riskantní, protože odhaluje, kdy jste naposledy požadovali data. Jiní navrhli požadovat pouze specifické klíče (podobně jako to dělají jump služby, ale automatizovaněji), možná za další cenu v anonymitě.

Možná vylepšení by zahrnovala náhradu nebo doplněk k address book (viz i2host.i2p), nebo něco jednoduchého jako přihlášení k odběru http://example.i2p/cgi-bin/recenthosts.cgi místo http://example.i2p/hosts.txt. Pokud by hypotetický recenthosts.cgi distribuoval všechny hostitele z posledních 24 hodin, například, mohlo by to být jak efektivnější, tak anonymnější než současný hosts.txt s last-modified a etag.

Vzorová implementace je na stats.i2p na adrese http://stats.i2p/cgi-bin/newhosts.txt. Tento skript vrací Etag s časovým razítkem. Když přijde požadavek s If-None-Match etag, skript vrací POUZE nové hosty od tohoto časového razítka, nebo 304 Not Modified, pokud žádné nejsou. Tímto způsobem skript efektivně vrací pouze hosty, které odběratel nezná, způsobem kompatibilním s adresářem.

Takže neefektivita není velkým problémem a existuje několik způsobů, jak věci zlepšit bez radikálních změn.

- **Není škálovatelný:** Soubor hosts.txt o velikosti 400K (s lineárním vyhledáváním) momentálně není tak velký a pravděpodobně můžeme růst 10x nebo 100x, než se to stane problémem.

Co se týče síťového provozu, viz výše. Ale pokud nehodláte provádět pomalý dotaz v reálném čase přes síť pro klíč, musíte mít celou sadu klíčů uloženou lokálně, za cenu přibližně 500 bajtů na klíč.

- **Vyžaduje konfiguraci a "důvěru":** Výchozí adresář je předplacen pouze na http://www.i2p2.i2p/hosts.txt, který se zřídka aktualizuje, což vede ke špatné uživatelské zkušenosti nových uživatelů.

Toto je zcela záměrné. jrandom chce, aby uživatel "důvěřoval" poskytovateli hosts.txt, a jak rád říká, "důvěra není boolean". Krok konfigurace se snaží přinutit uživatele, aby přemýšleli o otázkách důvěry v anonymní síti.

Jako další příklad, chybová stránka "I2P Site Unknown" v HTTP Proxy uvádí některé jump služby, ale žádnou konkrétní "nedoporučuje" a je na uživateli, aby si jednu vybral (nebo nevybral). jrandom by řekl, že uvedeným poskytovatelům důvěřujeme natolik, abychom je uvedli, ale ne natolik, abychom od nich automaticky získávali klíč.

Jak úspěšné to je, nejsem si jistý. Ale musí existovat nějaký druh hierarchie důvěry pro systém pojmenování. Zacházet se všemi stejně může zvýšit riziko únosu.

- **Není to DNS**

Bohužel by vyhledávání v reálném čase přes I2P významně zpomalilo procházení webu.

DNS je také založeno na vyhledávání s omezeným ukládáním do mezipaměti a time-to-live, zatímco I2P klíče jsou trvalé.

Jasně, mohli bychom to rozchodit, ale proč? Je to špatná volba.

- **Není spolehlivé:** Závisí na konkrétních serverech pro odběr adresáře.

Ano, závisí to na několika serverech, které máte nakonfigurované. V rámci I2P servery a služby přicházejí a odcházejí. Jakýkoli jiný centralizovaný systém (například DNS root servery) by měl stejný problém. Úplně decentralizovaný systém (každý je autoritativní) je možný implementací řešení "každý je root DNS server", nebo něčím ještě jednodušším, jako je skript, který přidá každého z vašeho hosts.txt do vaší adresní knihy.

Lidé obhajující všeobecně autoritativní řešení si však většinou důkladně nepromysleli problémy konfliktů a únosů.

- **Neohrabané, ne v reálném čase:** Je to mozaika poskytovatelů hosts.txt, poskytovatelů webových formulářů pro přidání klíčů, poskytovatelů jump služeb, hlašení stavu I2P Site. Jump servery a předplatná jsou obtížné, mělo by to fungovat jednoduše jako DNS.

Viz sekce spolehlivosti a důvěryhodnosti.

Takže shrnutí: současný systém není hrozně rozbitý, neefektivní nebo neškálovatelný a návrhy "prostě použít DNS" nejsou dobře promyšlené.

## Alternativy

Zdrojový kód I2P obsahuje několik připojitelných systémů pojmenování a podporuje možnosti konfigurace umožňující experimentování se systémy pojmenování.

- **Meta** - volá dva nebo více dalších systémů názvů v pořadí. Ve výchozím nastavení volá PetName a pak HostsTxt.
- **PetName** - Vyhledává v souboru petnames.txt. Formát tohoto souboru NENÍ stejný jako u hosts.txt.
- **HostsTxt** - Vyhledává v následujících souborech, v tomto pořadí:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Každý host je uveden v samostatném souboru v adresáři addressDb/.
- **Eepget** - provádí HTTP vyhledávací požadavek z externího serveru - musí být vrstvený za HostsTxt vyhledáváním s Meta. Může rozšířit nebo nahradit jump systém. Zahrnuje ukládání do mezipaměti v paměti.
- **Exec** - volá externí program pro vyhledávání, umožňuje další experimentování s vyhledávacími schématy, nezávisle na javě. Může být použit po HostsTxt nebo jako jediný systém názvů. Zahrnuje ukládání do mezipaměti v paměti.
- **Dummy** - používá se jako záložní řešení pro Base64 názvy, jinak selže.

Aktuální systém pojmenování lze změnit pomocí pokročilé konfigurační možnosti `i2p.naming.impl` (vyžaduje restart). Podrobnosti naleznete v `core/java/src/net/i2p/client/naming`.

Jakýkoli nový systém by měl být vrstvený s HostsTxt, nebo by měl implementovat lokální úložiště a/nebo funkce odběru adresáře, protože adresář zná pouze soubory hosts.txt a jejich formát.

## Certifikáty

I2P destinace obsahují certifikát, avšak v současnosti je tento certifikát vždy null. S null certifikátem jsou base64 destinace vždy dlouhé 516 bajtů a končí na "AAAA", což je kontrolováno v mechanismu slučování adresáře a případně i na jiných místech. Také není k dispozici žádná metoda pro generování certifikátu nebo jeho přidání do destinace. Takže tyto části bude třeba aktualizovat pro implementaci certifikátů.

Jedním z možných použití certifikátů je [proof of work](/get-involved/todo#hashcash).

Další je pro "subdomény" (v uvozovkách, protože ve skutečnosti něco takového neexistuje, I2P používá plochý systém pojmenování), aby byly podepsány klíči domény 2. úrovně.

S každou implementací certifikátu musí přijít i metoda pro ověřování certifikátů. Pravděpodobně by se to mělo stát v kódu pro slučování adresáře. Existuje metoda pro více typů certifikátů nebo více certifikátů?

Přidání certifikátu ověřujícího odpovědi jako podepsané nějakou centralizovanou certifikační autoritou by vyřešilo mnoho problémů s nepřátelskými nameservery, ale ponechalo by otevřené útoky typu replay a také útoky nepřátelských certifikačních autorit.
