---
title: "Diskuse o tunelech"
description: "Historický průzkum strategií odsazování, fragmentace a budování tunelů"
slug: "tunnel"
aliases:
  - "/cs/docs/discussions/tunnel"
  - "/cs/docs/discussions/tunnel/"
  - "/cs/tunnel_discussion"
  - "/cs/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Poznámka: Tento dokument obsahuje starší informace o alternativách k současné implementaci tunnel v I2P a spekulace o budoucích možnostech. Pro aktuální informace se podívejte na [stránku o tunnel](/docs/specs/tunnel-implementation).

Tato stránka dokumentuje současnou implementaci vytváření tunelů od verze 0.6.1.10. Starší metoda vytváření tunelů, používaná před verzí 0.6.1.10, je zdokumentována na [staré stránce o tunelech](/docs/historical/tunnel-alt).

### Alternativy konfigurace {#config}

Kromě jejich délky mohou existovat další konfigurovatelné parametry pro každý tunnel, které lze použít, jako je omezení frekvence doručovaných zpráv, jak by mělo být použito padding, jak dlouho by měl být tunnel v provozu, zda vkládat chaff zprávy a jaké strategie dávkování by měly být použity, pokud vůbec nějaké. Žádné z těchto funkcí nejsou v současnosti implementovány.

### Alternativy vyplňování {#tunnel.padding}

Existuje několik strategií pro padding tunelů, každá má své vlastní výhody:

- Žádné doplňování
- Doplňování na náhodnou velikost
- Doplňování na pevnou velikost
- Doplňování na nejbližší KB
- Doplňování na nejbližší exponenciální velikost (2^n bytů)

Tyto strategie vyplňování mohou být použity na různých úrovních, řešíce vystavení informací o velikosti zprávy různým protivníkům. Po shromáždění a přezkoumání některých statistik ze sítě 0.4, stejně jako po prozkoumání kompromisů anonymity, začínáme s pevnou velikostí tunnel zprávy 1024 bajtů. V rámci tohoto však fragmentované zprávy samotné nejsou tunelem vůbec vyplňovány (ačkoli pro end-to-end zprávy mohou být vyplněny jako součást garlic wrapping).

### Alternativy fragmentace {#tunnel.fragmentation}

Pro zabránění protivníkům označovat zprávy podél cesty úpravou velikosti zpráv mají všechny tunnel zprávy pevnou velikost 1024 bytů. Pro přizpůsobení větších I2NP zpráv a také pro efektivnější podporu menších zpráv gateway rozděluje větší I2NP zprávy na fragmenty obsažené v každé tunnel zprávě. Endpoint se pokusí znovu sestavit I2NP zprávu z fragmentů po krátký časový úsek, ale podle potřeby je zahodí.

Routery mají velkou volnost v tom, jak jsou fragmenty uspořádány, zda jsou neefektivně uloženy jako samostatné jednotky, dávkově zpracovávány po krátké období pro vložení většího množství dat do 1024 bajtových tunnel zpráv, nebo příležitostně doplněny jinými zprávami, které chtěl gateway odeslat.

### Další alternativy {#tunnel.alternatives}

#### Upravit zpracování tunnel uprostřed toku {#tunnel.reroute}

Zatímco jednoduchý algoritmus směrování tunnel by měl být dostačující pro většinu případů, existují tři alternativy, které lze prozkoumat:

- Nechat jiný peer než koncový bod dočasně působit jako ukončovací
  bod pro tunel úpravou šifrování používaného na gateway, aby jim
  poskytl plaintext předzpracovaných I2NP zpráv. Každý peer by mohl zkontrolovat,
  zda má plaintext, a při přijetí zpracovat zprávu, jako by ho měl.
- Umožnit routerům účastnícím se tunelu znovu namíchat zprávu před
  jejím předáním - odrazit ji přes jeden z vlastních odchozích tunelů daného peera,
  s instrukcemi pro doručení na další hop.
- Implementovat kód pro tvůrce tunelu k předefinování "dalšího hopu" peera v
  tunelu, což umožní další dynamické přesměrování.

#### Použít obousměrné tunnely {#tunnel.bidirectional}

Současná strategie používání dvou oddělených tunelů pro příchozí a odchozí komunikaci není jedinou dostupnou technikou a má důsledky pro anonymitu. Na pozitivní straně, použitím oddělených tunelů se snižuje množství provozních dat vystavených analýze účastníkům tunelu - například účastníci odchozího tunelu z webového prohlížeče by viděli pouze provoz HTTP GET, zatímco účastníci příchozího tunelu by viděli data doručovaná tunelem. U obousměrných tunelů by všichni účastníci měli přístup k informaci, že např. byl odeslán 1KB v jednom směru a poté 100KB v opačném směru. Na negativní straně, použití jednosměrných tunelů znamená, že existují dvě skupiny účastníků, které je třeba profilovat a zohlednit, a je nutné věnovat další pozornost řešení zvýšené rychlosti predecessor útoků. Proces sdružování a budování tunelů popsaný níže by měl minimalizovat obavy z predecessor útoků, i když by při žádoucnosti nebylo příliš obtížné vybudovat příchozí i odchozí tunely podél stejných účastníků.

#### Komunikace přes zpětný kanál {#tunnel.backchannel}

V současné době jsou používané hodnoty IV náhodné hodnoty. Je však možné, aby tato 16bajtová hodnota byla použita k odesílání řídicích zpráv od gateway k endpointu, nebo u odchozích tunelů od gateway k jakémukoli z účastníků. Příchozí gateway by mohla zakódovat určité hodnoty do IV jednou, které by endpoint mohl obnovit (protože ví, že endpoint je také tvůrcem). U odchozích tunelů by tvůrce mohl doručit určité hodnoty účastníkům během vytváření tunelu (např. "pokud vidíte 0x0 jako IV, znamená to X", "0x1 znamená Y" atd.). Protože gateway na odchozím tunelu je také tvůrcem, může sestavit IV tak, aby jakýkoli z účastníků obdržel správnou hodnotu. Tvůrce tunelu by mohl dokonce dát gateway příchozího tunelu sérii IV hodnot, které by tato gateway mohla použít ke komunikaci s jednotlivými účastníky právě jednou (ačkoli by to mělo problémy týkající se detekce tajných dohod).

Tato technika by mohla být později použita k doručení zprávy uprostřed datového toku, nebo k umožnění vstupní gateway informovat koncový bod, že je vystaven DoS útoku nebo jinak brzy selže. V současné době neexistují žádné plány na využití tohoto zpětného kanálu.

#### Zprávy tunnel s proměnnou velikostí {#tunnel.variablesize}

Zatímco transportní vrstva může mít svou vlastní pevnou nebo variabilní velikost zpráv, s použitím vlastní fragmentace, tunnel vrstva může místo toho používat tunnel zprávy variabilní velikosti. Rozdíl je otázkou modelů hrozeb - pevná velikost na transportní vrstvě pomáhá snížit informace vystavené vnějším protivníkům (i když celková analýza toku stále funguje), ale pro interní protivníky (aka účastníci tunnel) je velikost zprávy vystavena. Tunnel zprávy pevné velikosti pomáhají snížit informace vystavené účastníkům tunnel, ale neskrývají informace vystavené tunnel koncovým bodům a bránám. Zprávy pevné velikosti typu end-to-end skrývají informace vystavené všem uzlům v síti.

Jak vždy, je to otázka toho, proti komu se I2P snaží chránit. Tunnel zprávy proměnné velikosti jsou nebezpečné, protože umožňují účastníkům použít velikost zprávy samotnou jako zadní kanál k ostatním účastníkům - např. pokud vidíte zprávu o velikosti 1337 bytů, jste ve stejném tunnel jako další spolupracující partner. I s pevnou sadou povolených velikostí (1024, 2048, 4096 atd.) tento zadní kanál stále existuje, protože partneři mohou použít frekvenci každé velikosti jako nosič (např. dvě zprávy o 1024 bytech následované zprávou o 8192). Menší zprávy sice způsobují režii hlaviček (IV, tunnel ID, hash část atd.), ale větší zprávy pevné velikosti buď zvyšují latenci (kvůli dávkování) nebo dramaticky zvyšují režii (kvůli odsazení). Fragmentace pomáhá amortizovat režii za cenu potenciální ztráty zpráv kvůli ztraceným fragmentům.

Časové útoky jsou také relevantní při posuzování účinnosti zpráv s pevnou velikostí, ačkoli k jejich účinnosti vyžadují značný přehled o vzorcích síťové aktivity. Nadměrné umělé zpoždění v tunnelu bude detekováno tvůrcem tunnelu kvůli pravidelným testům, což způsobí zrušení celého tunnelu a úpravu profilů partnerů v něm.

### Alternativy budování {#tunnel.building.alternatives}

Reference: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Stará metoda budování tunnelů {#tunnel.building.old}

Stará metoda budování tunnelů, používaná před verzí 0.6.1.10, je zdokumentována na [stránce starých tunnelů](/docs/historical/tunnel-alt). Jednalo se o metodu "vše najednou" nebo "paralelní", kdy byly zprávy zasílány paralelně všem účastníkům.

#### Jednorázové teleskopické budování {#tunnel.building.oneshot}

POZNÁMKA: Toto je současná metoda.

Jedna otázka, která vyvstala ohledně použití průzkumných tunelů pro odesílání a přijímání zpráv o vytváření tunelů, je to, jak to ovlivňuje zranitelnost tunelu vůči útokům předchůdce. Zatímco koncové body a brány těchto tunelů budou náhodně distribuovány napříč sítí (možná dokonce včetně tvůrce tunelu v této množině), další alternativou je použít samotné cesty tunelů k předávání požadavku a odpovědi, jak se to dělá v [Tor](https://www.torproject.org/). To však může vést k únikům během vytváření tunelu, což umožní protějškům zjistit, kolik skoků je později v tunelu, sledováním časování nebo počtu paketů při budování tunelu.

#### "Interaktivní" teleskopické budování {#tunnel.building.telescoping}

Vybudovat hopy jeden po druhém se zprávou skrz existující část tunelu pro každý. Má závažné problémy, protože uzly mohou počítat zprávy a určit svou pozici v tunelu.

#### Neprůzkumné tunnely pro správu {#tunnel.building.nonexploratory}

Druhou alternativou k procesu budování tunelů je poskytnout routeru dodatečnou sadu neprůzkumných příchozích a odchozích poolů, které se použijí pro žádost o tunel a odpověď. Za předpokladu, že router má dobře integrovaný pohled na síť, nemělo by to být nutné, ale pokud byl router nějakým způsobem rozdělen, použití neprůzkumných poolů pro správu tunelů by snížilo únik informací o tom, kteří protějšci jsou v routerově oddílu.

#### Doručení průzkumného požadavku {#tunnel.building.exploratory}

Třetí alternativa, používaná do verze I2P 0.6.1.10, garlic šifruje jednotlivé zprávy s požadavky na tunnel a doručuje je jednotlivým hopům individuálně, přenáší je prostřednictvím průzkumných tunnelů s odpověďmi přicházejícími zpět v samostatném průzkumném tunnelu. Tato strategie byla opuštěna ve prospěch výše popsané.

#### Více historie a diskuse {#history}

Před zavedením Variable Tunnel Build Message existovaly nejméně dva problémy:

1. Velikost zpráv (způsobená maximem 8 hopů, když typická délka tunnelu je 2 nebo 3 hopy...
   a současný výzkum ukazuje, že více než 3 hopy nezlepšuje anonymitu);
2. Vysoká míra neúspěšného vytváření, zejména u dlouhých (a průzkumných) tunnelů, protože všechny hopy se musí shodnout, jinak je tunnel zahozen.

VTBM opravil #1 a vylepšil #2.

Welterde navrhl úpravy paralelní metody, které by umožnily rekonfiguraci. Sponge navrhl použití nějakého druhu 'tokenů'.

Každý student stavby tunelů musí studovat historický záznam vedoucí k současné metodě, zejména různé zranitelnosti anonymity, které mohou existovat v různých metodách. Mailové archivy z října 2005 jsou obzvláště užitečné. Jak je uvedeno ve [specifikaci vytváření tunelů](/docs/specs/tunnel-creation), současná strategie vznikla během diskuse na I2P mailing listu mezi Michaelem Rogersem, Matthewem Toselandem (toad) a jrandom ohledně predecessor útoku.

#### Alternativy řazení peerů {#ordering}

Méně přísné uspořádání je také možné, což zajišťuje, že zatímco skok po A může být B, B nikdy nemůže být před A. Další možnosti konfigurace zahrnují schopnost fixovat pouze příchozí tunnel brány a odchozí tunnel koncové body, nebo je rotovat podle MTBF rychlosti.

## Míchání/Dávkování {#tunnel.mixing}

Jaké strategie by měly být použity na gateway a na každém hopu pro zpoždění, přeuspořádání, přesměrování nebo doplnění zpráv? Do jaké míry by to mělo být prováděno automaticky, kolik by mělo být konfigurováno jako nastavení pro jednotlivé tunnely nebo hopy, a jak by měl tvůrce tunnelu (a následně uživatel) řídit tuto operaci? To vše zůstává neznámé a bude vypracováno pro budoucí vydání.
