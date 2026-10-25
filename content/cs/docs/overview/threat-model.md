---
title: "Model hrozeb I2P"
description: "Analýza útoků uvažovaných v návrhu I2P a zavedených protiopatření"
slug: "threat-model"
aliases:
  - "/cs/how_threatmodel"
  - "/cs/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## Co myslíme pojmem "Anonymní"?

Vaši úroveň anonymity lze popsat jako "jak těžké je pro někoho zjistit informace, které nechcete, aby věděl" — kdo jste, kde se nacházíte, s kým komunikujete, nebo dokonce kdy komunikujete. "Dokonalá" anonymita zde není užitečný koncept — software vás neučiní nerozeznatelným od lidí, kteří nepoužívají počítače nebo nejsou na internetu. Místo toho pracujeme na poskytování dostatečné anonymity pro uspokojení skutečných potřeb kohokoli, komu můžeme — od těch, kteří jednoduše prohlížejí webové stránky, po ty, kteří si vyměňují data, až po ty, kteří se bojí odhalení mocnými organizacemi nebo státy.

Otázka, zda I2P poskytuje dostatečnou anonymitu pro vaše konkrétní potřeby, je složitá, ale tato stránka vám snad pomůže na ni odpovědět tím, že prozkoumá, jak I2P funguje při různých útocích, abyste si mohli rozhodnout, zda splňuje vaše požadavky.

Vítáme další výzkum a analýzu odolnosti I2P vůči hrozbám popsaným níže. Je zapotřebí více přehledů existující literatury (z velké části zaměřené na Tor) a původní práce zaměřené na I2P.

---

## Shrnutí síťové topologie

I2P vychází z myšlenek mnoha [dalších](/docs/overview/comparison/) systémů, ale při studiu související literatury je třeba mít na paměti několik klíčových bodů:

- **I2P je bezplatný route mixnet** — tvůrce zprávy explicitně definuje cestu, kterou budou zprávy odesílány (odchozí tunnel), a příjemce zprávy explicitně definuje cestu, kterou budou zprávy přijímány (příchozí tunnel).
- **I2P nemá oficiální vstupní a výstupní body** — všichni účastníci se plně podílejí na míchání, a neexistují žádné síťové vstupní nebo výstupní proxy (nicméně na aplikační vrstvě existuje několik proxy).
- **I2P je plně distribuované** — neexistují žádné centrální kontroly nebo autority. Bylo by možné upravit některé routery tak, aby provozovaly mix kaskády (budování tunnelů a poskytování klíčů potřebných k řízení přeposílání na koncovém bodě tunnelu) nebo profilování a výběr založené na adresáři, to vše bez narušení kompatibility se zbytkem sítě, ale dělat to samozřejmě není nutné (a může dokonce poškodit anonymitu).

Máme zdokumentované plány na implementaci netriviálních zpoždění a strategií dávkového zpracování, jejichž existence je známa pouze konkrétnímu uzlu nebo tunnel bráně, která zprávu přijímá, což umožní převážně nízkolatentní mixnet poskytovat krycí provoz pro komunikaci s vyšší latencí (např. email). Jsme si však vědomi toho, že jsou potřebná významná zpoždění pro poskytnutí smysluplné ochrany a že implementace takových zpoždění bude významnou výzvou. V tuto chvíli není jasné, zda tyto funkce zpoždění skutečně implementujeme.

Teoreticky mohou routery podél cesty zprávy vložit libovolný počet přeskoků před předáním zprávy dalšímu uzlu, i když současná implementace to nedělá.

---

## Model hrozeb

Design I2P začal v roce 2003, nedlouho po příchodu [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/) a [Tor](https://www.torproject.org/). Náš design značně těží z výzkumu publikovaného v té době. I2P využívá několik technik onion routingu, takže nadále těžíme z významného akademického zájmu o Tor.

Na základě útoků a analýz uvedených v [literatuře o anonymitě](http://freehaven.net/anonbib/topic.html) (především [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)) následující text stručně popisuje širokou škálu útoků i mnoho obranných mechanismů I2P. Tento seznam aktualizujeme o nové útoky, jakmile jsou identifikovány.

Jsou zde zahrnuty některé útoky, které mohou být specifické pro I2P. Na všechny tyto útoky nemáme dobré odpovědi, nicméně pokračujeme ve výzkumu a zlepšování našich obran.

Navíc jsou mnohé z těchto útoků výrazně snazší, než by měly být, kvůli skromné velikosti současné sítě. Přestože si uvědomujeme určitá omezení, která je třeba řešit, I2P je navrženo tak, aby podporovalo stovky tisíc nebo miliony účastníků. Jak budeme pokračovat v šíření povědomí a rozšiřování sítě, tyto útoky se stanou mnohem obtížnějšími.

Stránky [porovnání sítí](/docs/overview/comparison/) a [terminologie "garlic"](/docs/overview/garlic-routing/) mohou být také užitečné k prostudování.

### Útoky hrubou silou

Útok hrubou silou může být proveden globálním pasivním nebo aktivním protivníkem, který sleduje všechny zprávy procházející mezi všemi uzly a pokouší se korelovat, která zpráva následuje kterou cestu. Provedení tohoto útoku proti I2P by mělo být netriviální, protože všechny uzly v síti často odesílají zprávy (jak end to end zprávy, tak zprávy síťové údržby), navíc end to end zpráva mění velikost a data podél své cesty. Kromě toho externí protivník nemá přístup ani k samotným zprávám, protože komunikace mezi routery je šifrovaná i proudová (což činí dvě zprávy o velikosti 1024 bajtů nerozlišitelnými od jedné zprávy o velikosti 2048 bajtů).

Nicméně silný útočník může použít hrubou sílu k detekci trendů — pokud může poslat 5GB dat na I2P destinaci a monitorovat síťové připojení všech, může eliminovat všechny peery, kteří neobdrželi 5GB dat. Existují techniky k odražení tohoto útoku, ale mohou být prohibitivně nákladné (viz: [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)'s mimics nebo konstantní rychlost přenosu). Většinu uživatelů tento útok neznepokojuje, protože náklady na jeho provedení jsou extrémní (a často vyžadují nezákonnou činnost). Nicméně útok je stále možný, například pozorovatelem u velkého ISP nebo na internetovém výměnném bodě. Ti, kdo se chtějí bránit proti tomuto útoku, by měli přijmout příslušná protiopatření, jako je nastavení nízkých limitů šířky pásma a používání nezveřejněných nebo šifrovaných leaseSets pro I2P stránky. Další protiopatření, jako jsou netriviální zpoždění a omezené trasy, nejsou v současnosti implementována.

Jako částečná obrana proti jednomu routeru nebo skupině routerů, které se snaží směrovat veškerý provoz sítě, obsahují routery omezení týkající se toho, kolik tunnelů může být směrováno přes jednoho peer. Jak síť roste, tato omezení podléhají dalším úpravám. Další mechanismy pro hodnocení, výběr a vyhýbání se peer jsou popsány na stránce výběru peer.

### Útoky založené na časování

Zprávy I2P jsou jednosměrné a nemusí nutně znamenat, že bude odeslána odpověď. Aplikace běžící nad I2P však budou s největší pravděpodobností mít rozpoznatelné vzorce ve frekvenci svých zpráv — například HTTP požadavek bude malá zpráva s velkou sekvencí odpovědních zpráv obsahujících HTTP odpověď. Pomocí těchto dat a širokého pohledu na topologii sítě může být útočník schopen vyloučit některá spojení jako příliš pomalá na to, aby jimi zpráva prošla.

Tento druh útoku je mocný, ale jeho použitelnost na I2P není zřejmá, protože variace v prodlevách zpráv způsobené frontováním, zpracováváním zpráv a omezováním často dosáhnou nebo překročí čas potřebný k předání zprávy podél jediného spoje — i když útočník ví, že odpověď bude odeslána ihned po přijetí zprávy. Existují však některé scénáře, které odhalí poměrně automatické odpovědi — streaming knihovna to dělá (s SYN+ACK), stejně jako message režim garantovaného doručení (s DataMessage+DeliveryStatusMessage).

Bez čištění protokolů nebo vyšší latence mohou globální aktivní protivníci získat podstatné informace. Proto by lidé znepokojení těmito útoky mohli zvýšit latenci (použitím netriviálních zpoždění nebo strategií dávkování), zahrnout čištění protokolů nebo jiné pokročilé techniky směrování tunelů, ale ty nejsou v I2P implementovány.

Reference: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Útoky průsečíkem

Útoky na průsečíky proti systémům s nízkou latencí jsou extrémně silné — útočník periodicky navazuje kontakt s cílem a sleduje, které uzly jsou v síti. Časem, jak dochází ke změnám uzlů, útočník získá významné informace o cíli pouhým nalezením průsečíků množin uzlů, které jsou online, když zpráva úspěšně projde. Náklady tohoto útoku se zvyšují s růstem sítě, ale v některých scénářích může být proveditelný.

Shrnutí: pokud je útočník současně na obou koncích vašeho tunelu, může být úspěšný. I2P nemá úplnou obranu proti tomuto typu útoku pro komunikaci s nízkou latencí. Jedná se o inherentní slabinu onion routingu s nízkou latencí. Tor poskytuje [podobné upozornění](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting).

Částečné obranné mechanismy implementované v I2P:

- [Přísné řazení](/docs/specs/tunnel-implementation/#ordering) peerů
- Profilování peerů a výběr z malé skupiny, která se mění pomalu
- Omezení počtu tunnelů směrovaných přes jediný peer
- Zabránění peerům ze stejného /16 IP rozsahu v tom, aby byli členy jediného tunnelu
- Pro I2P weby nebo jiné hostované služby podporujeme současný hosting na více routerech, neboli multihoming

I celkově vzato tyto obranné mechanismy nejsou úplným řešením. Také jsme udělali některá návrhová rozhodnutí, která mohou významně zvýšit naši zranitelnost:

- Nepoužíváme "guard nodes" s nízkou šířkou pásma
- Používáme tunnel pooly složené z několika tunnelů a provoz se může přesouvat z tunnelu na tunnel.
- Tunnely nejsou dlouhodobé; nové tunnely se budují každých 10 minut.
- Délky tunnelů jsou konfigurovatelné. Zatímco 3-hop tunnely jsou doporučeny pro plnou ochranu, několik aplikací a služeb používá ve výchozím nastavení 2-hop tunnely.

V budoucnu by to mohlo být možné pro peers, kteří si mohou dovolit značná zpoždění (podle netriviálních strategií zpoždění a dávkování). Navíc to je relevantní pouze pro destinace, o kterých vědí i jiní lidé — soukromá skupina, jejíž destinace je známa pouze důvěryhodným peers, se nemusí obávat, protože protivník je nemůže "pingovat" k provedení útoku.

Odkaz: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Útoky typu Denial of Service

Existuje celá řada útoků typu denial of service (odmítnutí služby) dostupných proti I2P, z nichž každý má různé náklady a důsledky:

**Útok chamtivého uživatele:** Jedná se jednoduše o lidi, kteří se snaží spotřebovat významně více zdrojů, než jsou ochotni přispět. Obranou proti tomuto je:

- Nastavit výchozí hodnoty tak, aby většina uživatelů poskytovala zdroje síti. V I2P uživatelé směrují provoz ve výchozím nastavení. Na rozdíl od [jiných sítí](/docs/overview/comparison/) více než 95 % uživatelů I2P předává provoz pro ostatní.
- Poskytovat snadné možnosti konfigurace, aby uživatelé mohli zvýšit svůj příspěvek (procento sdílení) do sítě. Zobrazovat snadno srozumitelné metriky jako „poměr sdílení", aby uživatelé viděli, co přispívají.
- Udržovat silnou komunitu s blogy, fóry, IRC a dalšími prostředky komunikace.

**Útok hladomorem:** Nepřátelský uživatel se může pokusit poškodit síť vytvořením značného počtu peerů v síti, kteří nejsou identifikováni jako subjekty pod kontrolou stejné entity (jako u Sybil). Tyto uzly se pak rozhodnou neposkytovat síti žádné prostředky, což způsobí, že existující peeři musí prohledávat větší databázi sítě nebo žádat více tunnelů, než by mělo být nutné. Alternativně mohou uzly poskytovat přerušovanou službu tím, že periodicky zahazují vybraný provoz nebo odmítají připojení k určitým peerům. Toto chování může být nerozeznatelné od chování silně zatíženého nebo selhávajícího uzlu. I2P řeší tyto problémy udržováním profilů peerů, pokusem o identifikaci těch s nedostatečným výkonem a jejich jednoduchým ignorováním, nebo jejich vzácným používáním. Významně jsme vylepšili schopnost rozpoznávat a vyhýbat se problematickým peerům; stále jsou však v této oblasti potřebné značné úsilí.

**Flooding attack:** Nepřátelský uživatel se může pokusit zaplavit síť, peer, cíl nebo tunnel. Zaplavení sítě a peer je možné a I2P nedělá nic pro zabránění standardnímu zaplavení na IP vrstvě. Zaplavení cíle zprávami zasláním velkého množství na různé brány příchozích tunnel cíle je možné, ale cíl to pozná jak z obsahu zprávy, tak proto, že testy tunnel selžou. Totéž platí pro zaplavení pouze jediného tunnel. I2P nemá obranu proti síťovému flooding útoku. Pro útok zaplavení cíle a tunnel cíl identifikuje, které tunnel nereagují, a vytvoří nové. Nový kód by také mohl být napsán pro přidání ještě více tunnel, pokud si klient přeje zvládnout větší zátěž. Pokud je naopak zátěž větší, než s jakou si klient dokáže poradit, může instruovat tunnel, aby omezily počet zpráv nebo bajtů, které by měly předávat (jakmile bude implementována pokročilá operace tunnel).

**Útok na zatížení CPU:** V současnosti existují některé metody, jak lze na dálku požádat peer o provedení kryptograficky nákladné operace, a nepřátelský útočník by je mohl využít k zahlcení daného peer velkým množstvím takových požadavků ve snaze přetížit CPU. Jak používání dobrých inženýrských postupů, tak potenciálně vyžadování netriviálních certifikátů (např. HashCash) připojených k těmto nákladným požadavkům by mělo problém zmírnit, ačkoliv tu může být prostor pro útočníka využít různé chyby v implementaci.

**DOS útok na floodfill:** Nepřátelský uživatel se může pokusit poškodit síť tím, že se stane floodfill routerem. Současné obranné mechanismy proti nespolehlivým, přerušovaným nebo škodlivým floodfill routerům jsou slabé. Floodfill router může poskytovat špatné nebo žádné odpovědi na vyhledávání a může také zasahovat do komunikace mezi floodfill routery. Některé obranné mechanismy a profilování peerů jsou implementovány, ale je toho ještě mnoho k dokončení. Pro více informací viz [stránka o síťové databázi](/docs/specs/common-structures/).

### Útoky značkování

Útoky označováním — úprava zprávy tak, aby mohla být později identifikována dále na cestě — jsou samy o sobě v I2P nemožné, protože zprávy procházející tunely jsou podepsané. Pokud je však útočník inbound tunnel gateway a zároveň účastníkem dále v tomto tunelu, mohou ve spolupráci identifikovat skutečnost, že jsou ve stejném tunelu (a před přidáním jedinečných hop id a dalších aktualizací mohli spolupracující peeři ve stejném tunelu tuto skutečnost rozpoznat bez jakéhokoliv úsilí). Útočník v outbound tunnel a jakékoliv části inbound tunnel však nemohou spolupracovat, protože šifrování tunelu doplňuje a upravuje data samostatně pro inbound a outbound tunely. Vnější útočníci nemohou dělat nic, protože spojení jsou šifrovaná a zprávy podepsané.

### Útoky rozdělením sítě

Útoky rozdělení sítě — hledání způsobů, jak oddělit (technicky nebo analyticky) účastníky v síti — je důležité mít na paměti při jednání s mocným protivníkem, protože velikost sítě hraje klíčovou roli při určování vaší anonymity. Technické rozdělení pomocí přerušení spojení mezi účastníky za účelem vytvoření fragmentovaných sítí řeší vestavěná network database I2P, která udržuje statistiky o různých účastnících tak, aby bylo možné využít jakákoli existující spojení k jiným fragmentovaným částem pro uzdravení sítě. Pokud však útočník odpojí všechna spojení k nekontrolovaným účastníkům a v podstatě izoluje cíl, žádné uzdravení pomocí network database to nevyřeší. V tom okamžiku může router pouze doufat, že si všimne, že významný počet dříve spolehlivých účastníků se stal nedostupným, a upozorní klienta, že je dočasně odpojen (tento detekční kód není v současnosti implementován).

Rozdělování sítě analyticky hledáním rozdílů v chování routerů a destinací a jejich následné seskupování je také velmi silný útok. Například útočník [sklízející](#harvesting-attacks) síťovou databázi bude vědět, kdy má konkrétní destinace 5 příchozích tunelů ve svém LeaseSet, zatímco ostatní mají pouze 2 nebo 3, což umožňuje protivníkovi potenciálně rozdělit klienty podle počtu vybraných tunelů. Další rozdělení je možné při práci s netriviálními zpožděními a strategiemi dávkového zpracování, protože brány tunelů a konkrétní uzly s nenulovými zpožděními budou pravděpodobně vyčnívat. Tato data jsou však vystavena pouze těmto konkrétním uzlům, takže pro efektivní rozdělení na základě této záležitosti by útočník musel kontrolovat významnou část sítě (a i tak by to bylo pouze pravděpodobnostní rozdělení, protože by nevěděl, které další tunely nebo zprávy mají tato zpoždění).

Také diskutováno na [stránce síťové databáze](/docs/specs/common-structures/) (bootstrap útok).

### Útoky předchůdců

Predecessor attack spočívá v pasivním shromažďování statistik ve snaze zjistit, kteří peerové jsou 'blízko' k cíli tím, že se účastní jejich tunnelů a sledují předchozí nebo následující hop (pro odchozí nebo příchozí tunnely). Postupem času, pomocí dokonale náhodného vzorku peerů a náhodného uspořádání, by útočník mohl vidět, který peer se statisticky objevuje jako 'bližší' více než ostatní, a tento peer by zároveň byl místem, kde se nachází cíl.

I2P se tomuto vyhýbá čtyřmi způsoby: zaprvé, peeři vybraní k účasti v tunelech nejsou náhodně vzorkováni napříč sítí — jsou odvozeni z algoritmu pro výběr peerů, který je rozděluje do úrovní. Zadruhé, se [striktním uspořádáním](/docs/specs/tunnel-implementation/#ordering) peerů v tunelu skutečnost, že se peer objevuje častěji, neznamená, že je zdrojem. Zatřetí, s permutovanou délkou tunelu (ve výchozím nastavení není povoleno) dokonce i 0 hop tunely mohou poskytovat věrohodné popírání, protože občasná variace gateway bude vypadat jako normální tunely. Začtvrté, s omezenými trasami (neimplementováno), pouze peer s omezeným spojením k cíli bude kdy kontaktovat cíl, zatímco útočníci narazí pouze na tuto gateway.

Současná metoda budování tunnelů byla speciálně navržena pro boj proti útoku předchůdce. Viz také [průsečíkový útok](#intersection-attacks).

Reference: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), což je aktualizace [předchozího článku o útoku z roku 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf).

### Útoky typu Harvesting

"Harvesting" znamená sestavování seznamu uživatelů provozujících I2P. Může být použito pro právní útoky a k podpoře dalších útoků tak, že jednoduše provozujete peer, sledujete, ke komu se připojuje, a shromažďujete všechny odkazy na ostatní peery, které dokážete najít.

I2P samo o sobě není navrženo s účinnými obrannými mechanismy proti tomuto útoku, protože existuje distribuovaná síťová databáze obsahující právě tyto informace. Následující faktory činí útok v praxi poněkud obtížnějším:

- Růst sítě ztíží získání daného podílu sítě
- Floodfill routery implementují limity dotazů jako ochranu před DOS útoky
- "Skrytý režim", který brání routeru publikovat své informace do netDb (ale také mu brání předávat data), se nyní široce nepoužívá, ale mohl by se používat.

V budoucích implementacích by základní a komplexní omezené trasy snížily sílu tohoto útoku, protože "skryté" uzly nepublikují své kontaktní adresy v síťové databázi — pouze tunely, přes které lze k nim dosáhnout (stejně jako jejich veřejné klíče atd.).

V budoucnu by routery mohly použít GeoIP k identifikaci, zda se nacházejí v určité zemi, kde by identifikace jako I2P uzel byla riziková. V takovém případě by router mohl automaticky povolit skrytý režim nebo zavést jiné omezené směrovací metody.

### Identifikace prostřednictvím analýzy provozu

Sledováním provozu do a z routeru může škodlivý ISP nebo státní firewall identifikovat, že počítač provozuje I2P. Jak bylo diskutováno [výše](#harvesting-attacks), I2P není specificky navrženo ke skrytí toho, že počítač provozuje I2P. Nicméně několik návrhových rozhodnutí učiněných při návrhu transportní vrstvy a protokolů činí identifikaci I2P provozu do jisté míry obtížnou:

- Náhodný výběr portu
- Point-to-Point šifrování veškerého provozu
- DH výměna klíčů bez protokolových bajtů nebo jiných nešifrovaných konstantních polí
- Současné použití transportů TCP i UDP. UDP může být pro některá zařízení Deep Packet Inspection (DPI) mnohem obtížnější sledovat.

V blízké budoucnosti plánujeme přímo řešit problémy s analýzou provozu dalším maskováním transportních protokolů I2P, možná včetně:

- Padding na transportní vrstvě na náhodné délky, zejména během handshake připojení
- Studium signatur distribuce velikostí paketů a další padding podle potřeby
- Vývoj dalších transportních metod, které napodobují SSL nebo jiné běžné protokoly
- Přezkoumání padding strategií na vyšších vrstvách, aby se zjistilo, jak ovlivňují velikosti paketů na transportní vrstvě
- Přezkoumání metod implementovaných různými státními firewally pro blokování Tor
- Přímá spolupráce s experty na DPI a obfuskaci

Reference: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Sybil útoky

Sybil popisuje kategorii útoků, kde protivník vytváří libovolně velké množství spolupracujících uzlů a používá jejich zvýšený počet k podpoře dalších útoků. Například, pokud je útočník v síti, kde jsou peers vybíráni náhodně a chce mít 80% šanci být jedním z těchto peers, jednoduše vytvoří pětkrát více uzlů, než je v síti, a hodí kostkou. Když je identita zdarma, může být Sybil velmi účinnou technikou pro mocného protivníka. Primární technikou k řešení tohoto problému je jednoduše učinit identitu "ne zdarma" — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (mezi ostatními) využívá skutečnost, že IP adresy jsou omezené, zatímco IIP použil [HashCash](http://www.hashcash.org/) k "naúčtování" za vytvoření nové identity. V současné době nemáme implementovanou žádnou konkrétní techniku pro řešení Sybil útoku, ale zahrnujeme zástupné certifikáty v datových strukturách router a destination, které mohou obsahovat HashCash certifikát odpovídající hodnoty, když je to potřeba (nebo nějaký jiný certifikát prokazující vzácnost).

Požadování HashCash certifikátů na různých místech má dva hlavní problémy:

- Zachování zpětné kompatibility
- Klasický HashCash problém — výběr HashCash hodnot, které představují smysluplné důkazy práce na výkonných strojích, přičemž jsou stále proveditelné na slabších strojích jako jsou mobilní zařízení.

Různá omezení počtu routerů v daném IP rozsahu omezují zranitelnost vůči útočníkům, kteří nemají schopnost umístit stroje do několika IP bloků. To však není smysluplná obrana proti mocnému protivníkovi.

Viz [stránku síťové databáze](/docs/specs/common-structures/) pro další diskusi o Sybil útocích.

### Útoky vyčerpáním buddies

(Reference: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Sekce 5.2)

Odmítáním přijímat nebo přeposílat požadavky na vytvoření tunnelu, kromě spolupracujícímu partneru, může router zajistit, že tunnel je vytvořen zcela z jeho sady spolupracujících routerů. Šance na úspěch se zvyšují, pokud existuje velký počet spolupracujících routerů, tj. [Sybil útok](#sybil-attacks). To je do jisté míry zmírněno našimi metodami profilování partnerů používanými k monitorování výkonu partnerů. Nicméně toto je mocný útok, když se počet routerů blíží *f* = 0,2, nebo 20% škodlivých uzlů, jak je specifikováno v dokumentu. Škodlivé routery by také mohly udržovat připojení k cílovému routeru a poskytovat vynikající propustnost pro provoz přes tato připojení ve snaze manipulovat profily spravované cílem a vypadat atraktivně. Další výzkum a obrana mohou být nezbytné.

### Kryptografické útoky

Používáme silnou kryptografii s dlouhými klíči a předpokládáme bezpečnost průmyslově standardních kryptografických primitiv používaných v I2P. Bezpečnostní funkce zahrnují okamžité odhalení pozměněných zpráv na cestě, neschopnost dešifrovat zprávy, které vám nejsou adresovány, a obranu proti útokům typu man-in-the-middle. Velikosti klíčů zvolené v roce 2003 byly v té době docela konzervativní a stále jsou delší než ty používané v [jiných anonymizačních sítích](https://torproject.org/). Nemyslíme si, že současné délky klíčů jsou naší největší slabinou, zejména pro tradiční protivníky na nestatní úrovni; chyby a malá velikost sítě jsou mnohem znepokojivější. Samozřejmě, všechny kryptografické algoritmy se časem stanou zastaralými kvůli příchodu rychlejších procesorů, kryptografickému výzkumu a pokrokům v metodách jako rainbow tables, clustery herního hardwaru atd. Bohužel, I2P nebylo navrženo s jednoduchými mechanismy pro prodloužení klíčů nebo změnu sdílených tajných hodnot při zachování zpětné kompatibility.

Upgrade různých datových struktur a protokolů pro podporu delších klíčů bude nakonec nutné řešit, a bude to velký úkol, stejně jako to bude pro [ostatní](https://torproject.org/). Doufejme, že pečlivým plánováním dokážeme minimalizovat narušení a implementovat mechanismy, které usnadní budoucí přechody.

V budoucnu bude několik I2P protokolů a datových struktur podporovat bezpečné doplňování zpráv na libovolné velikosti, takže zprávy by mohly mít konstantní velikost nebo by garlic zprávy mohly být náhodně modifikovány tak, aby některé cloves vypadaly, že obsahují více subcloves, než ve skutečnosti obsahují. V současné době však garlic, tunnel a end to end zprávy obsahují jednoduché náhodné doplnění.

### Floodfill útoky na anonymitu

Kromě floodfill DOS útoků popsaných [výše](#denial-of-service-attacks) jsou floodfill routery jedinečně postaveny k tomu, aby se dozvěděly o účastnících sítě, kvůli své roli v netDb a vysoké frekvenci komunikace s těmito účastníky. To je částečně zmírněno tím, že floodfill routery spravují pouze část celkového prostoru klíčů a prostor klíčů se denně rotuje, jak je vysvětleno na [stránce databáze sítě](/docs/specs/common-structures/). Specifické mechanismy, kterými routery komunikují s floodfills, byly pečlivě navrženy. Tyto hrozby by však měly být dále studovány. Specifické potenciální hrozby a odpovídající obranná opatření jsou tématem pro budoucí výzkum.

### Další útoky na síťovou databázi

Nepřátelský uživatel se může pokusit poškodit síť vytvořením jednoho nebo více floodfill routerů a jejich úpravou tak, aby poskytovaly špatné, pomalé nebo žádné odpovědi. Několik scénářů je probráno na [stránce network database](/docs/specs/common-structures/).

### Útoky na centrální zdroje

Existuje několik centralizovaných nebo omezených zdrojů (některé uvnitř I2P, jiné ne), které by mohly být napadeny nebo použity jako vektor pro útoky. Absence jrandom od listopadu 2007, následovaná ztrátou hostingové služby i2p.net v lednu 2008, zdůraznila četné centralizované zdroje ve vývoji a provozu sítě I2P, z nichž většina je nyní distribuována. Útoky na externě dostupné zdroje hlavně ovlivňují schopnost nových uživatelů nás najít, nikoliv provoz samotné sítě.

- Webová stránka je zrcadlena a používá DNS round-robin pro externí veřejný přístup.
- Routery nyní podporují [více externích reseed umístění](/docs/overview/faq/#reseed), avšak může být potřeba více reseed hostů a zpracování nespolehlivých nebo škodlivých reseed hostů může vyžadovat zlepšení.
- Routery nyní podporují více umístění souborů pro aktualizace. Škodlivý aktualizační host by mohl poskytnout obrovský soubor; je třeba omezit velikost.
- Routery nyní podporují více výchozích důvěryhodných podepisovatelů aktualizací.
- Routery nyní lépe zpracovávají více nespolehlivých floodfill peerů. Škodlivé floodfilly vyžadují další studium.
- Kód je nyní uložen v distribuovaném systému správy verzí.
- Routery spoléhají na jediného news hostitele, ale je zde napevno zakódovaná záložní URL ukazující na jiného hostitele. Škodlivý news host by mohl poskytnout obrovský soubor; je třeba omezit velikost.
- [Služby pojmenovacího systému](/docs/overview/naming/), včetně poskytovatelů odběru adresářů, služeb pro přidávání hostitelů a jump služeb, mohou být škodlivé. Podstatné ochrany pro odběry byly implementovány ve verzi 0.6.1.31, s dalšími vylepšeními v následujících verzích. Nicméně všechny pojmenovací služby vyžadují určitou míru důvěry; viz [stránka o pojmenování](/docs/overview/naming/) pro podrobnosti.
- Zůstáváme závislí na DNS službě pro i2p2.de; ztráta této služby by způsobila podstatné narušení naší schopnosti přilákat nové uživatele a zmenšila by síť (v krátkodobém až střednědobém horizontu), stejně jako ztráta i2p.net.

### Vývojové útoky

Tyto útoky nejsou zaměřeny přímo na síť, ale místo toho se zaměřují na její vývojový tým buď zaváděním právních překážek pro kohokoli, kdo přispívá k vývoji softwaru, nebo použitím všech dostupných prostředků k přesvědčení vývojářů, aby software podvrhli. Tradiční technická opatření nemohou tyto útoky porazit, a pokud by někdo ohrozil život nebo živobytí vývojáře (nebo dokonce jen vydal soudní příkaz spolu se zákazem mluvení pod hrozbou vězení), měli bychom velký problém.

Nicméně existují dvě techniky, které pomáhají bránit se proti těmto útokům:

- Všechny komponenty sítě musí být open source, aby umožnily inspekci, ověření, úpravy a vylepšení. Pokud je vývojář kompromitován, jakmile si toho komunita všimne, měla by požadovat vysvětlení a přestat přijímat práci tohoto vývojáře. Všechny checkins do našeho distribuovaného systému správy zdrojového kódu jsou kryptograficky podepsané a tvůrci vydání používají systém důvěryhodných seznamů k omezení úprav pouze na ty předem schválené.
- Vývoj prostřednictvím samotné sítě, který umožňuje vývojářům zůstat anonymní, ale přitom zabezpečit vývojový proces. Veškerý I2P vývoj může probíhat prostřednictvím I2P — pomocí distribuovaného systému správy zdrojového kódu, IRC chatu, veřejných webových serverů, diskuzních fór (forum.i2p) a stránek pro distribuci softwaru, všechno dostupné v rámci I2P.

Také udržujeme vztahy s různými organizacemi, které nabízejí právní poradenství, pokud by byla potřeba jakákoli obhajoba.

### Útoky na implementaci (chyby)

Ať se snažíme sebevíc, většina netriviálních aplikací obsahuje chyby v návrhu nebo implementaci a I2P není výjimkou. Mohou existovat chyby, které by mohly být zneužity k útoku na anonymitu nebo bezpečnost komunikace probíhající přes I2P neočekávaným způsobem. Abychom pomohli odolat útokům proti návrhu nebo používaným protokolům, zveřejňujeme všechny návrhy a dokumentaci a žádáme o kontrolu a kritiku s nadějí, že mnoho očí systém vylepší. Nevěříme v bezpečnost skrze utajení.

Navíc je kód zpracováván stejným způsobem, s malou averzi vůči přepracování nebo zahození něčeho, co nesplňuje potřeby softwarového systému (včetně snadnosti úprav). Dokumentace návrhu a implementace sítě a softwarových komponent je základní součástí bezpečnosti, protože bez ní je nepravděpodobné, že by vývojáři byli ochotni věnovat čas naučení se software natolik, aby dokázali identifikovat nedostatky a chyby.

Náš software pravděpodobně obsahuje chyby související zejména s odmítnutím služby prostřednictvím chyb nedostatku paměti (OOM), problémy s cross-site scripting (XSS) v konzoli routeru a další zranitelnosti vůči nestandardním vstupům prostřednictvím různých protokolů.

I2P je stále malá síť s malou vývojářskou komunitou a téměř žádným zájmem ze strany akademických nebo výzkumných skupin. Proto nám chybí analýza, kterou mohly obdržet [jiné anonymizační sítě](https://torproject.org/). Nadále hledáme lidi, kteří se [zapojí](/get-involved/) a pomohou.

---

## Další obranné mechanismy

### Seznamy blokovaných

Do určité míry by I2P mohl být vylepšen tak, aby se vyhnul peerům provozovaným na IP adresách uvedených v seznamu blokovaných adres. Několik takových seznamů je běžně dostupných ve standardních formátech, obsahujících anti-P2P organizace, potenciální protivníky na státní úrovni a další.

Pokud se aktivní peers skutečně objevují v aktuálním blocklist, blokování pouze podmnožinou peers by mělo tendenci segmentovat síť, zhoršovat problémy s dostupností a snižovat celkovou spolehlivost. Proto bychom se chtěli dohodnout na konkrétním blocklist a ve výchozím nastavení jej povolit.

Blokované seznamy jsou pouze částí (možná malou částí) celé řady obran proti škodlivému chování. Velkou měrou systém profilování dobře měří chování routerů, takže nemusíme nic v netDb důvěřovat. Lze však udělat více. Pro každou z oblastí v seznamu výše můžeme provést zlepšení v detekci škodlivého chování.

Pokud je blocklist hostován na centrálním místě s automatickými aktualizacemi, síť je zranitelná vůči [útoku na centrální zdroj](#central-resource-attacks). Automatické přihlášení k odběru seznamu dává poskytovateli seznamu moc vypnout I2P síť. Úplně.

V současnosti je s naším softwarem distribuován výchozí blocklist, který obsahuje pouze IP adresy minulých zdrojů DOS útoků. Neexistuje žádný automatický mechanismus aktualizace. Pokud by určitý rozsah IP adres implementoval vážné útoky na I2P síť, museli bychom požádat lidi, aby svůj blocklist aktualizovali ručně prostřednictvím mimopásmových mechanismů, jako jsou fóra, blogy atd.
