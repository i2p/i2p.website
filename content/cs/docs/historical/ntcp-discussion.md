---
title: "Diskuse o NTCP"
description: "Historická diskuse o transportních protokolech NTCP vs SSU z března 2007"
slug: "ntcp-discussion"
aliases:
  - "/cs/docs/discussions/ntcp"
  - "/cs/docs/discussions/ntcp/"
  - "/cs/ntcp_discussion"
  - "/cs/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Následuje diskuse o NTCP, která se konala v březnu 2007. Nebyla aktualizována tak, aby odrážela současnou implementaci. Pro současnou specifikaci NTCP viz [stránku NTCP2](/docs/specs/ntcp2).

## Diskuze NTCP vs. SSU, březen 2007 {#ntcp-ssu}

### NTCP otázky

(upraveno z IRC diskuse mezi zzz a cervantes)

Proč je NTCP preferován před SSU, nemá NTCP vyšší režii a latenci? Má lepší spolehlivost.

Netrpí streaming lib přes NTCP klasickými problémy TCP-over-TCP? Co kdybychom měli opravdu jednoduchý UDP transport pro provoz pocházející ze streaming-lib? Myslím, že SSU byl zamýšlen jako takzvaný opravdu jednoduchý UDP transport - ale ukázal se jako příliš nespolehlivý.

### Analýza "NTCP je škodlivý" od zzz {#harmful}

Zveřejněno v novém Syndie, 25.3.2007. Toto bylo zveřejněno za účelem podnícení diskuze, neberte to příliš vážně.

**Shrnutí:** NTCP má vyšší latenci a režii než SSU a je pravděpodobnější, že selže při použití se streaming knihovnou. Provoz je však směrován s preferencí NTCP před SSU a toto je v současnosti natvrdo zakódováno.

#### Diskuse

V současnosti máme dva transporty, NTCP a SSU. Jak jsou aktuálně implementované, NTCP má nižší "bidy" než SSU, takže je preferovaný, kromě případu, kdy existuje navázané SSU spojení, ale neexistuje navázané NTCP spojení pro daný peer.

SSU je podobné NTCP v tom, že implementuje potvrzení, časové limity a opětovné přenosy. Nicméně SSU je I2P kód s přísnými omezeními na časové limity a dostupnými statistikami o dobách zpátečního přenosu, opětovných přenosech atd. NTCP je založeno na Java NIO TCP, což je černá skříňka a pravděpodobně implementuje RFC standardy, včetně velmi dlouhých maximálních časových limitů.

Většina provozu v rámci I2P pochází ze streaming-lib (HTTP, IRC, Bittorrent), což je naše implementace TCP. Jelikož transport na nižší úrovni je obecně NTCP kvůli nižším nabídkám, systém podléhá dobře známému a obávanému problému TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , kde vyšší i nižší vrstvy TCP provádějí retransmise současně, což vede ke kolapsu.

Na rozdíl od scénáře PPP přes SSH popsaného v odkazu výše, máme několik skoků pro nižší vrstvu, přičemž každý je pokryt NTCP spojením. Takže každá NTCP latence je obecně mnohem menší než latence streaming lib na vyšší vrstvě. To snižuje pravděpodobnost kolapsu.

Také jsou pravděpodobnosti kolapsu sníženy, když je nižší vrstva TCP pevně omezena nízkými timeouty a počtem opakovaných přenosů ve srovnání s vyšší vrstvou.

Vydání .28 zvýšilo maximální timeout streaming lib z 10 sec na 45 sec, což věci značně zlepšilo. SSU maximální timeout je 3 sec. NTCP maximální timeout je předpokládaně nejméně 60 sec, což je doporučení RFC. Neexistuje způsob, jak změnit NTCP parametry nebo monitorovat výkon. Kolaps NTCP vrstvy je [editor: text ztracen]. Možná by pomohl externí nástroj jako tcpdump.

Nicméně při spuštění .28 nedrží i2psnark hlášený upstream obecně na vysoké úrovni. Často klesá na 3-4 KBps před tím, než se zase vyšplhá nahoru. To je signál, že stále dochází k výpadkům.

SSU je také efektivnější. NTCP má vyšší režii a pravděpodobně vyšší doby odezvy. Při použití NTCP je poměr (výstup tunelu) / (výstup dat i2psnark) nejméně 3,5 : 1. Při spuštění experimentu, kde byl kód upraven tak, aby preferoval SSU (konfigurační volba i2np.udp.alwaysPreferred nemá v současném kódu žádný účinek), se poměr snížil na přibližně 3 : 1, což ukazuje na lepší efektivitu.

Podle statistik streaming lib byly věci výrazně vylepšeny - lifetime window size vzrostla z 6,3 na 7,5, RTT kleslo z 11,5s na 10s, sends per ack klesly z 1,11 na 1,07.

Že to bylo docela účinné, bylo překvapivé, vzhledem k tomu, že jsme měnili transport pouze pro první z celkem 3 až 5 hopů, které by odchozí zprávy podnikly.

Vliv na rychlosti odchozích dat u i2psnark nebyl jasný kvůli běžným výkyvům. Také pro experiment bylo zakázáno příchozí NTCP. Vliv na rychlosti příchozích dat u i2psnark nebyl jasný.

#### Návrhy

1. **1A)** To je snadné -
   Měli bychom obrátit priority nabídek tak, aby SSU bylo upřednostňováno pro veškerý provoz, pokud
   to dokážeme udělat bez způsobení všemožných dalších problémů. Tím se opraví
   konfigurační možnost i2np.udp.alwaysPreferred, aby fungovala (buď jako true
   nebo false).

2. **1B)** Alternativa k 1A), ne tak snadná -
   Pokud můžeme označit provoz aniž by to nepříznivě ovlivnilo naše cíle anonymity,
   měli bychom identifikovat provoz generovaný streaming-lib a nechat SSU vygenerovat
   nízkou nabídku pro tento provoz. Tato značka bude muset jít se zprávou přes každý
   hop, aby přeposílající routery také respektovaly SSU preferenci.

3. **2)** Další omezení SSU (snížení maximálních retransmisí z aktuálních
   10) je pravděpodobně rozumné pro snížení rizika kolapsu.

4. **3)** Potřebujeme další studium výhod vs. škod semi-spolehlivého protokolu
   pod streaming lib. Jsou retransmise přes jeden hop prospěšné
   a velkým přínosem nebo jsou horší než zbytečné?
   Mohli bychom udělat nový SUU (secure unreliable UDP), ale pravděpodobně by to nestálo za to. Mohli
   bychom možná přidat typ zprávy no-ack-required v SSU, pokud nechceme žádné
   retransmise vůbec u provozu streaming-lib. Jsou těsně ohraničené
   retransmise žádoucí?

5. **4)** Kód pro odesílání s prioritou ve verzi .28 je pouze pro NTCP. Dosud moje testování neukázalo velký užitek priority pro SSU, protože zprávy se neřadí do fronty dostatečně dlouho na to, aby priority měly nějaký význam. Ale je potřeba více testování.

6. **5)** Nový maximální timeout streaming lib 45s je pravděpodobně stále příliš nízký.
   TCP RFC uvádí 60s. Pravděpodobně by neměl být kratší než základní NTCP maximální timeout (předpokládá se 60s).

### Odpověď od jrandom {#jrandom-response}

Zveřejněno v novém Syndie, 27.3.2007

Celkově jsem otevřený experimentování s tímto, ale pamatujte si, proč je tam NTCP v první řadě - SSU selhalo při kolapsu přetížení. NTCP "prostě funguje", a zatímco míry retransmise 2-10% lze zvládnout v normálních single-hop sítích, to nám dává 40% míru retransmise s 2 hop tunely. Pokud započítáte některé z naměřených míry retransmise SSU, které jsme viděli ještě před implementací NTCP (10-30+%), dostaneme 83% míru retransmise. Možná tyto míry byly způsobeny nízkým 10sekundovým timeoutem, ale takové zvýšení by nás poškodilo (pamatujte, vynásobte 5 a máte polovinu cesty).

Na rozdíl od TCP nemáme žádnou zpětnou vazbu z tunnel, abychom věděli, zda zpráva dorazila - neexistují žádná potvrzení na úrovni tunnel. Máme sice end-to-end ACK, ale pouze u malého počtu zpráv (kdykoli distribuujeme nové session tagy) - z 1 553 591 klientských zpráv, které můj router odeslal, jsme se pokusili potvrdit pouze 145 207 z nich. Ostatní mohly tiše selhat nebo se dokonale podařit.

Nejsem přesvědčen argumentem TCP-over-TCP pro nás, zejména rozděleným napříč různými cestami, kterými přenášíme data. Měření na I2P mě samozřejmě mohou přesvědčit o opaku.

> *Maximální timeout pro NTCP je pravděpodobně alespoň 60 sekund, což je doporučení RFC. Neexistuje způsob, jak změnit parametry NTCP nebo sledovat výkon.*

Pravda, ale síťová připojení se dostanou na tuto úroveň pouze když se děje něco opravdu špatného - timeout pro retransmisi u TCP je často v řádu desítek nebo stovek milisekund. Jak poukazuje foofighter, mají 20+ let zkušeností a oprav chyb ve svých TCP stackech, plus miliardový průmysl optimalizující hardware a software tak, aby fungoval dobře podle toho, co dělají.

> *NTCP má vyšší režii a pravděpodobně vyšší doby odezvy. při používání NTCP > je poměr (tunnel output) / (i2psnark data output) alespoň 3.5 : 1. > Při spuštění experimentu, kdy byl kód upraven tak, aby preferoval SSU (konfigurační > možnost i2np.udp.alwaysPreferred nemá v současném kódu žádný účinek), se poměr > snížil na přibližně 3 : 1, což ukazuje na lepší efektivitu.*

Toto jsou velmi zajímavá data, nicméně spíše z hlediska zahlcení routeru než efektivity šířky pásma - museli byste porovnat 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct. Tento datový bod naznačuje, že v routeru je něco, co vede k nadměrnému lokálnímu zařazování zpráv, které jsou již přenášeny.

> *velikost životního okna vzrostla z 6,3 na 7,5, RTT kleslo z 11,5s na 10s, odesílání na ACK kleslo z 1,11 na 1,07.*

Pamatujte, že sends-per-ACK je pouze vzorek, nikoli úplný počet (protože se nesnažíme potvrzovat každé odeslání). Není to ani náhodný vzorek, ale místo toho více vzorkuje období nečinnosti nebo zahájení nárazové aktivity - trvalé zatížení nebude vyžadovat mnoho potvrzení.

Velikosti oken v tomto rozsahu jsou stále žalostně nízké na to, aby poskytly skutečný přínos AIMD, a stále příliš nízké na přenos jediného 32KB BT bloku (zvýšení spodní hranice na 10 nebo 12 by to pokrylo).

Přesto vypadá statistika wsize slibně - po jak dlouhou dobu byla udržována?

Ve skutečnosti pro účely testování se možná budete chtít podívat na StreamSinkClient/StreamSinkServer nebo dokonce TestSwarm v apps/ministreaming/java/src/net/i2p/client/streaming/ - StreamSinkClient je CLI aplikace, která odešle vybraný soubor na vybranou destinaci a StreamSinkServer vytvoří destinaci a zapíše všechna data, která mu jsou poslána (zobrazuje velikost a čas přenosu). TestSwarm kombinuje obojí - zaplavuje náhodnými daty kohokoliv, ke komu se připojí. To by vám mělo poskytnout nástroje pro měření udržované propustnosti přes streaming lib, na rozdíl od BT choke/send.

> *1A) Toto je jednoduché - > Měli bychom převrátit priority nabídek tak, aby SSU byl preferován pro veškerý provoz, pokud > to dokážeme udělat bez způsobení všech možných jiných problémů. Toto opraví > konfigurační možnost i2np.udp.alwaysPreferred tak, aby fungovala (buď jako true > nebo false).*

Respektování i2np.udp.alwaysPreferred je v každém případě dobrý nápad - klidně tento změnu commitněte. Pojďme však nejprve shromáždit trochu více dat před změnou preferencí, protože NTCP byl přidán kvůli řešení kolapsu zahlcení způsobeného SSU.

> *1B) Alternativa k 1A), ne tak snadná - > Pokud dokážeme označit provoz, aniž by to nepříznivě ovlivnilo naše cíle anonymity, měli > bychom identifikovat provoz generovaný streaming-lib > a nechat SSU vygenerovat nízkou nabídku pro tento provoz. Tato značka bude muset jít s > zprávou přes každý hop > tak, aby forwardující routery také respektovaly preference SSU.*

V praxi existují tři typy provozu - budování/testování tunelů, netDb dotazy/odpovědi a provoz streaming lib. Síť byla navržena tak, aby rozlišování těchto tří typů bylo velmi obtížné.

> *2) Další omezení SSU (snížení maximálních retransmisí ze současných > 10) je pravděpodobně rozumné pro snížení rizika kolapsu.*

Při 10 retransmisích jsme už v pěkné kaši, souhlasím. Jedna, možná dvě retransmise jsou rozumné z pohledu transportní vrstvy, ale pokud je druhá strana příliš přetížená na to, aby ACK stihla včas (i s implementovanou SACK/NACK schopností), moc toho udělat nemůžeme.

Z mého pohledu, abychom skutečně vyřešili hlavní problém, musíme se zabývat tím, proč se router tak zahlcuje, že nestíhá ACK včas (což, jak jsem zjistil, je způsobeno soubojem o CPU). Možná bychom mohli upravit některé věci ve zpracování routeru tak, aby přenos již existujícího tunnelu měl vyšší prioritu CPU než dešifrování nové žádosti o tunnel? I když musíme být opatrní, abychom se vyhnuli vyhladovění.

> *3) Potřebujeme další studium výhod a nevýhod semi-spolehlivého protokolu > pod streaming lib. Jsou retransmise přes jeden hop prospěšné > a velkým přínosem, nebo jsou horší než k ničemu? > Mohli bychom udělat nový SUU (secure unreliable UDP), ale pravděpodobně to nestojí za to. > Mohli bychom možná přidat typ zprávy bez požadavku ACK v SSU, pokud nechceme > žádné retransmise vůbec u provozu streaming-lib. Jsou těsně omezené > retransmise žádoucí?*

Stojí za zvážení - co kdybyschom jednoduše zakázali retransmissions v SSU? Pravděpodobně by to vedlo k mnohem vyšším rychlostem opakovaného odesílání ve streaming lib, ale možná ne.

> *4) Kód pro odesílání podle priority ve verzi .28 je pouze pro NTCP. Zatím moje testování neukázalo velké využití pro SSU priority, protože zprávy se nedrží ve frontě dostatečně dlouho na to, aby priority měly nějaký užitek. Ale je potřeba více testování.*

Existuje UDPTransport.PRIORITY_LIMITS a UDPTransport.PRIORITY_WEIGHT (respektované třídou TimedWeightedPriorityMessageQueue), ale v současnosti jsou váhy téměř všechny stejné, takže to nemá žádný účinek. To by se samozřejmě dalo upravit (ale jak zmiňujete, pokud nedochází k řazení do fronty, není to důležité).

> *5) Nový maximální timeout streaming lib 45s je pravděpodobně stále příliš nízký. TCP RFC > říká 60s. Pravděpodobně by neměl být kratší než základní NTCP maximální timeout > (předpokládaně 60s).*

Těch 45s je ale maximální timeout pro retransmisi streaming knihovny, ne timeout streamu. TCP v praxi má timeouty pro retransmisi o řády menší, i když ano, může dosáhnout 60s na linkách probíhajících přes nechráněné kabely nebo satelitní přenosy ;) Pokud bychom zvýšili timeout pro retransmisi streaming knihovny na např. 75 sekund, mohli bychom si zajít na pivo dříve, než se načte webová stránka (zvláště za předpokladu méně než 98% spolehlivého transportu). To je jeden z důvodů, proč preferujeme NTCP.

### Odpověď od zzz {#zzz-response}

Zveřejněno v novém Syndie, 2007-03-31

> *Při 10 retransmiticích už jsme v pěkné kaši, s tím souhlasím. Jedna, možná dvě > retransmitice jsou rozumné z hlediska transportní vrstvy, ale pokud je druhá strana > příliš zahlcená na to, aby ACK stihla včas (i s implementovanou SACK/NACK > schopností), moc s tím nezmůžeme.* > > *Podle mého názoru, abychom skutečně vyřešili hlavní problém, musíme se zaměřit > na to, proč se router tak zahlcuje, že nestihne ACK včas (což jsem zjistil, že > je kvůli soupeření o CPU). Možná můžeme v routeru přeorganizovat zpracování, > aby měla transmise již existujícího tunnelu vyšší CPU prioritu než dešifrování > nového požadavku na tunnel? Musíme si ale dát pozor, abychom se vyhnuli > vyhladovění.*

Jedna z mých hlavních technik shromažďování statistik je zapnout net.i2p.client.streaming.ConnectionPacketHandler=DEBUG a sledovat RTT časy a velikosti oken, jak procházejí. Abychom to na chvíli zobecnili, běžně vidíme 3 typy spojení: ~4s RTT, ~10s RTT a ~30s RTT. Cílem je snížit spojení s 30s RTT. Pokud je příčinou soupeření o CPU, možná pomůže nějaké přeuspořádání.

Snížení SSU max retrans z 10 je opravdu jen pokus naslepo, protože nemáme dobrá data o tom, zda se hroutíme, máme problémy s TCP-over-TCP, nebo co se děje, takže potřebujeme více dat.

> *Stojí za prozkoumání - co kdyby jsme jen zakázali retransmise SSU? Pravděpodobně by to vedlo k mnohem vyšším rychlostem opětovného odesílání v streaming knihovně, ale možná ne.*

Co nechápu, pokud byste to mohli rozvinout, jsou výhody SSU retransmisí pro provoz, který nepoužívá streaming-lib. Potřebují tunnel zprávy (například) používat polo-spolehlivý transport, nebo mohou používat nespolehlivý nebo tak-nějak-spolehlivý transport (maximálně 1 nebo 2 retransmise, například)? Jinými slovy, proč polo-spolehlivost?

> *(ale jak zmiňujete, pokud není žádné zařazování do fronty, nezáleží na tom).*

Implementoval jsem prioritní odesílání pro UDP, ale aktivovalo se přibližně 100 000krát méně často než kód na straně NTCP. Možná je to vodítko pro další vyšetřování nebo nápověda - nerozumím, proč by se to mělo tolikrát častěji hromadit u NTCP, ale možná je to nápověda, proč NTCP funguje hůře.

### Otázka zodpovězena uživatelem jrandom {#jrandom-followup}

Zveřejněno v novém Syndie, 2007-03-31

> *naměřené míry retransmise SSU, které jsme viděli před implementací NTCP > (10-30+%)* > > Může samotný router toto měřit? Pokud ano, mohl by být transport vybrán na > základě naměřeného výkonu? (tj. pokud SSU spojení k peeru zahazuje > nepřiměřené množství zpráv, upřednostnit NTCP při odesílání tomuto peeru)

Ano, v současnosti používá tuto statistiku jako chudákovu detekci MTU (pokud je míra retransmise vysoká, používá malou velikost paketů, ale pokud je nízká, používá velkou velikost paketů). Vyzkoušeli jsme několik věcí při prvním zavedení NTCP (a při prvním odchodu od původního TCP transportu), které by preferovaly SSU, ale snadno by selhaly pro daného peera, což by způsobilo návrat k NTCP. Nicméně, v tomto ohledu by se určitě dalo udělat více, i když se to rychle komplikuje (jak/kdy upravovat/resetovat nabídky, zda tyto preference sdílet mezi více peery nebo ne, zda je sdílet napříč více relacemi se stejným peerem (a jak dlouho), atd).

### Odpověď od foofighter {#foofighter}

Zveřejněno v novém Syndie, 2007-03-26

Pokud jsem to pochopil správně, hlavním důvodem ve prospěch TCP (obecně, jak starší, tak novější varianty) bylo, že si nemusíte dělat starosti s kódováním dobrého TCP stacku. Což není nemožně těžké udělat správně... jen že stávající TCP stacky mají 20letý náskok.

Pokud vím, není za preferencí TCP oproti UDP mnoho hluboké teorie, kromě následujících úvah:

- Síť pouze s TCP je velmi závislá na dosažitelných peerech (těch, kteří mohou přeposílat příchozí spojení přes svůj NAT)
- Přesto i když jsou dosažitelní peeři vzácní, jejich vysoká kapacita částečně zmírňuje problémy s topologickou omezeností
- UDP umožňuje "NAT hole punching", což lidem umožňuje být "tak trochu pseudo-dosažitelnými" (s pomocí introducerů), jinak by se mohli pouze připojovat ven
- "Stará" implementace TCP transportu vyžadovala mnoho vláken, což bylo zabijákem výkonu, zatímco "nový" TCP transport si vede dobře s málo vlákny
- Routery ze sady A se rozpadají při nasycení UDP. Routery ze sady B se rozpadají při nasycení TCP.
- "Cítí se" (jak ve smyslu, že existují nějaké náznaky, ale žádná vědecká data ani kvalitní statistiky), že A je rozšířenější než B
- Některé sítě přenášejí non-DNS UDP datagramy s přímo mizernou kvalitou, zatímco stále se trochu obtěžují přenášet TCP proudy.

Na tomto základě se zdá rozumné mít malou rozmanitost transportů (tolik, kolik je potřeba, ale ne více) v obou případech. Který by měl být hlavním transportem, závisí na jejich výkonu. Viděl jsem nepříjemné věci na své lince, když jsem se pokusil využít její plnou kapacitu s UDP. Ztráty paketů na úrovni 35%.

Rozhodně bychom mohli zkusit hrát si s prioritami UDP versus TCP, ale doporučoval bych v tom být opatrný. Doporučoval bych, aby se neměnily příliš radikálně najednou, nebo by to mohlo něco rozbít.

### Odpověď od zzz (pro foofighter) {#zzz-foofighter}

Zveřejněno na novém Syndie, 2007-03-27

> *Pokud vím, neexistuje moc hluboké teorie za preferencí TCP versus UDP, kromě následujících úvah:*

To jsou všechno platné námitky. Nicméně uvažujete o těchto dvou protokolech izolovaně, místo abyste přemýšleli o tom, který transportní protokol je nejlepší pro konkrétní protokol vyšší úrovně (tj. streaming lib nebo ne).

To, co říkám, je, že musíte vzít v úvahu streaming knihovnu.

Buď změnit preference pro všechny, nebo zacházet s provozem streamovacích knihoven odlišně.

To je přesně to, o čem mluví můj návrh 1B) - mít odlišnou prioritu pro provoz streaming-lib než pro provoz mimo streaming-lib (například zprávy pro budování tunnelů).

> *Na tomto pozadí se zdá rozumné mít malou rozmanitost transportů (tolik, kolik je potřeba, ale > ne víc) v obou případech. Který by měl být hlavní transport, > závisí na jejich výkonu. Viděl jsem ošklivé věci na své lince, když jsem > se pokusil využít její plnou kapacitu s UDP. Ztráty paketů na úrovni 35%.*

Souhlasím. Nová verze .28 možná zlepšila situaci ohledně ztráty paketů přes UDP, nebo možná ne.

Jeden důležitý bod - transportní kód si pamatuje selhání transportu. Takže pokud je UDP preferovaný transport, zkusí jej nejprve, ale pokud selže pro konkrétní cíl, při dalším pokusu pro tento cíl zkusí NTCP místo opětovného pokusu s UDP.

> *Rozhodně bychom mohli zkusit experimentovat s prioritami UDP versus TCP, ale doporučuji v tom opatrnost. Naléhavě doporučuji, aby se neměnily příliš radikálně najednou, jinak by to mohlo něco pokazit.*

Máme čtyři ovládací prvky - čtyři hodnoty nabídek (SSU a NTCP, pro již připojené a dosud nepřipojené). Mohli bychom například nastavit, aby SSU bylo preferováno před NTCP pouze pokud jsou oba připojeny, ale zkusit NTCP jako první, pokud není připojen žádný transport.

Druhý způsob, jak to udělat postupně, je přesunout pouze provoz streaming lib (návrh 1B), ale to by mohlo být složité a může mít dopady na anonymitu, nevím. Nebo možná přesunout provoz pouze pro první odchozí hop (tj. nepropagovat flag na další router), což vám dá pouze částečný užitek, ale mohlo by to být anonymnější a jednodušší.

## Výsledky diskuse {#results}

... a další související změny ve stejném časovém období (2007):

- Významné ladění parametrů streaming lib,
  které výrazně zvýšilo výkon odchozích spojení, bylo implementováno ve verzi 0.6.1.28
- Prioritní odesílání pro NTCP bylo implementováno ve verzi 0.6.1.28
- Prioritní odesílání pro SSU bylo implementováno uživatelem zzz, ale nikdy nebylo začleněno
- Pokročilé řízení nabídek transportu
  i2np.udp.preferred bylo implementováno ve verzi 0.6.1.29.
- Pushback pro NTCP bylo implementováno ve verzi 0.6.1.30, zakázáno ve verzi 0.6.1.31 kvůli obavám o anonymitu,
  a znovu povoleno s vylepšeními pro řešení těchto obav ve verzi 0.6.1.32.
- Žádný z zzz návrhů 1-5 nebyl implementován.
