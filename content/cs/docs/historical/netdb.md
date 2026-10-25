---
title: "Diskuse o Network Database"
description: "Historické poznámky k floodfill, experimentům s Kademlia a budoucímu ladění netDb"
slug: "netdb"
aliases:
  - "/cs/docs/legacy/netdb"
  - "/cs/docs/legacy/netdb/"
  - "/cs/netdb_discussion"
  - "/cs/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

POZNÁMKA: Následující text je diskuze o historii implementace netDb a nejedná se o aktuální informace. Aktuální dokumentaci najdete na [hlavní stránce netDb](/docs/overview/network-database).

## Historie {#status}

NetDb je distribuována pomocí jednoduché techniky zvané "floodfill". Před dlouhou dobou netDb také používala Kademlia DHT jako záložní algoritmus. Nicméně ve našem použití nefungovala dobře a byla kompletně vypnuta ve verzi 0.6.1.20.

*(Upraveno z příspěvku od jrandom ve starém Syndie, 26. listopadu 2005)*

Floodfill netDb je ve skutečnosti jen jednoduchým a možná dočasným opatřením, používajícím nejjednodušší možný algoritmus - pošle data k peer uzlu ve floodfill netDb, počká 10 sekund, vybere náhodný peer uzel v netDb a požádá ho o odeslání záznamu, čímž ověří jeho správné vložení / distribuci. Pokud ověřovací peer uzel neodpoví, nebo nemá daný záznam, odesílatel proces opakuje. Když peer uzel ve floodfill netDb obdrží netDb store od peer uzlu, který není ve floodfill netDb, pošle jej všem peer uzlům ve floodfill netDb.

V jednom bodě byla funkcionalita vyhledávání/ukládání Kademlia stále na místě. Uzly považovaly floodfill uzly za vždy "bliže" ke každému klíči než jakýkoliv uzel, který se neúčastní netDb. Vrátili jsme se k Kademlia netDb, pokud floodfill uzly z nějakého důvodu selžou. Nicméně, Kademlia pak byla zcela vypnuta (viz níže).

Nedávno byl Kademlia částečně znovu zaveden koncem roku 2009 jako způsob, jak omezit velikost netDb, kterou musí každý floodfill router ukládat.

### Úvod do algoritmu Floodfill

Floodfill byl představen ve vydání 0.6.0.4, přičemž Kademlia zůstala jako záložní algoritmus.

*(Přizpůsobeno z příspěvků od jrandom ve starém Syndie, 26. listopadu 2005)*

Jak jsem často říkal, nejsem nijak zvlášť vázán na konkrétní technologii - záleží mi na tom, co přinese výsledky. Zatímco jsem v posledních letech pracoval na různých netDb nápadech, problémy, kterým jsme čelili v posledních týdnech, některé z nich přivedly k vrcholu. Na živé síti, s netDb faktorem redundance nastaveným na 4 peery (což znamená, že pokračujeme v odesílání záznamu novým peerům, dokud 4 z nich nepotvrdí, že ho mají) a časovým limitem na peer nastaveným na 4násobek průměrné doby odpovědi daného peeru, **stále** dostáváme průměr 40-60 peerů, kterým se odesílá, než 4 z nich potvrdí uložení. To znamená odesílání 36-56krát více zpráv, než by mělo vycházet, přičemž každá používá tunnely a tím pádem překračuje 2-4 spojení. Navíc je tato hodnota silně zkreslená, protože průměrný počet peerů, kterým se odesílá při 'neúspěšném' uložení (což znamená, že méně než 4 lidé potvrdili zprávu po 60 sekundách odesílání zpráv), byl v rozmezí 130-160 peerů.

To je šílené, zvlášť pro síť s pouhými asi 250 uzly.

Nejjednodušší odpovědí je říci "no jasně jrandom, je to rozbité. oprav to", ale to se nedostane k jádru problému. V souladu s další současnou snahou je pravděpodobné, že máme značný počet síťových problémů kvůli omezeným trasám - uzly, které nemohou komunikovat s některými jinými uzly, často kvůli problémům s NAT nebo firewallem. Pokud by, řekněme, K uzlů nejbližších ke konkrétnímu netDb záznamu bylo za 'omezenou trasou' tak, že by netDb store zpráva k nim mohla dorazit, ale netDb lookup zpráva od nějakého jiného uzla ne, tento záznam by byl v podstatě nedostupný. Pokud se vydáme touto cestou trochu dál a vezmeme v úvahu skutečnost, že některé omezené trasy budou vytvořeny s nepřátelským úmyslem, je jasné, že se budeme muset blíže podívat na dlouhodobé řešení netDb.

Existuje několik alternativ, ale dvě z nich stojí za zvláštní zmínku. První je jednoduše provozovat netDb jako Kademlia DHT pomocí podmnožiny celé sítě, kde všichni tito peři jsou externě dosažitelní. Peři, kteří se netDb neúčastní, stále dotazují tyto peery, ale neobdrží nevyžádané netDb store nebo lookup zprávy. Účast v netDb by byla jak samo-vybiravá, tak uživatelsky eliminující - routery by si volily, zda publikovat příznak ve svém routerInfo udávající, zda se chtějí účastnit, zatímco každý router si volí, které peery chce považovat za část netDb (peři, kteří tento příznak publikují, ale nikdy neposkytují žádná užitečná data, by byli ignorováni a v podstatě eliminováni z netDb).

Další alternativou je návrat do minulosti, zpět k mentalitě DTSTTCPW (Do The Simplest Thing That Could Possibly Work - Udělej nejjednodušší věc, která by mohla fungovat) - floodfill netDb, ale stejně jako alternativa výše, používající pouze podmnožinu celé sítě. Když uživatel chce publikovat záznam do floodfill netDb, jednoduše ho pošle jednomu z účastníků routerů, počká na ACK a poté za 30 sekund dotáže další náhodný účastník floodfill netDb, aby ověřil, že byl správně distribuován. Pokud ano, skvělé, a pokud ne, jednoduše proces opakuje. Když floodfill router obdrží netDb store, okamžitě odešle ACK a zařadí netDb store do fronty pro všechny své známé netDb peery. Když floodfill router obdrží netDb lookup, pokud má data, odpoví s nimi, ale pokud ne, odpoví s hashy pro řekněme 20 dalších peerů ve floodfill netDb.

Při pohledu z perspektivy síťové ekonomie je floodfill netDb velmi podobná původní broadcast netDb, až na to, že náklady na publikování záznamu nesou převážně uzly v netDb, nikoli samotný vydavatel. Když to rozvedeme trochu dále a budeme s netDb zacházet jako s černou skříňkou, můžeme vidět, že celková šířka pásma vyžadovaná netDb je:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
kde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Dosazení několika hodnot:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
To se zase škáluje lineárně s N (při 100 000 peerech musí netDb zvládnout netDb store zprávy celkem 2,5 MB/s, nebo při 300 peerech 7,6 KB/s).

Zatímco floodfill netDb by měla každého účastníka netDb přijímat pouze malou část netDb úložišť generovaných klienty přímo, všichni by nakonec obdrželi všechny záznamy, takže všechny jejich spojení by měly být schopné zvládnout plné recvKBps. Na oplátku budou všichni muset odeslat `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)`, aby udrželi ostatní peery synchronizované.

Floodfill netDb by nevyžadovalo ani směrování tunelů pro provoz netDb ani žádný speciální výběr ohledně toho, na které záznamy může "bezpečně" odpovídat, protože základním předpokladem je, že všechny ukládají vše. A pokud jde o požadované využití disku pro netDb, je to stále poměrně triviální pro jakýkoli moderní stroj, vyžaduje přibližně 11MB na každých 1000 peerů `(N * (L + 1) * S)`.

Kademlia netDb by tyto čísla snížila, ideálně by je přivedla na K krát M násobek jejich hodnoty, kde K = faktor redundance a M je počet routerů v netDb (např. 5/100, což dává recvKBps 126KBps a 536MB při 100 000 routerech). Nevýhodou Kademlia netDb je však zvýšená složitost bezpečného provozu v nepřátelském prostředí.

To, o čem teď přemýšlím, je jednoduše implementovat a nasadit floodfill netDb v naší existující živé síti, nechat peery, kteří ji chtějí používat, aby si vybrali jiné peery označené jako členové a dotazovali se jich místo dotazování tradičních Kademlia netDb peerů. Požadavky na šířku pásma a disk jsou v této fázi dostatečně triviální (7,6 KBps a 3 MB diskového prostoru) a odstraní to netDb úplně z plánu ladění - problémy, které zůstanou k řešení, budou způsobeny něčím nesouvisejícím s netDb.

Jak by byli vybráni peeři pro publikování příznaku říkajícího, že jsou součástí floodfill netDb? Na začátku by to mohlo být provedeno manuálně jako pokročilá konfigurační možnost (ignorováno, pokud router není schopen ověřit svou externí dostupnost). Pokud příliš mnoho peerů nastaví tento příznak, jak si účastníci netDb vybírají, které vyřadit? Opět, na začátku by to mohlo být provedeno manuálně jako pokročilá konfigurační možnost (po vyřazení peerů, kteří jsou nedostupní). Jak zabráníme rozdělení netDb? Tím, že routery ověří, že netDb správně provádí flood fill dotazováním K náhodných netDb peerů. Jak routery, které se neúčastní netDb, objeví nové routery pro tunelování? To by snad mohlo být provedeno zasláním konkrétního netDb vyhledávání, aby netDb router neodpověděl s peery v netDb, ale s náhodnými peery mimo netDb.

I2P netDb se velmi liší od tradičních zatížených DHT - nese pouze síťová metadata, nikoli skutečný obsah, což je důvod, proč i netDb používající floodfill algoritmus dokáže udržet libovolné množství dat I2P Site/IRC/bt/mail/syndie/atd. Dokonce můžeme provést některé optimalizace, jak I2P poroste, abychom toto zatížení trochu více distribuovali (možná předáváním bloom filtrů mezi účastníky netDb, aby viděli, co potřebují sdílet), ale zdá se, že prozatím se obejdeme s mnohem jednodušším řešením.

Jeden fakt stojí za prozkoumání - ne všechny leaseSets musí být publikovány v netDb! Ve skutečnosti většina z nich nepotřebuje být - pouze ty pro destinace, které budou přijímat nevyžádané zprávy (tedy servery). Je to proto, že garlic encryption zabalené zprávy posílané z jedné destinace do druhé již obsahují leaseSet odesílatele, takže jakékoli následné odesílání/přijímání mezi těmito dvěma destinacemi (v krátkém časovém období) funguje bez jakékoli aktivity netDb.

Takže zpět k těm rovnicím - můžeme změnit L z 5 na něco jako 0,1 (za předpokladu, že pouze 1 z každých 50 destinací je server). Předchozí rovnice také opomíjely zátěž sítě potřebnou k odpovídání na dotazy od klientů, ale i když je velmi proměnlivá (na základě aktivity uživatelů), je také velmi pravděpodobné, že bude zcela zanedbatelná ve srovnání s frekvencí publikování.

Každopádně, stále žádná magie, ale pěkné snížení téměř o 1/5 potřebné šířky pásma/místa na disku (možná později více, v závislosti na tom, zda distribuce routerInfo probíhá přímo jako součást navázání spojení s peer nebo pouze prostřednictvím netDb).

### Deaktivace algoritmu Kademlia

Kademlia byla kompletně zakázána ve verzi 0.6.1.20.

*(Upraveno z IRC konverzace s jrandom 11/07)*

Kademlia vyžaduje minimální úroveň služby, kterou základní řešení nemohlo poskytnout (šířka pásma, procesor), a to ani po přidání úrovní (čistá kad je v tomto bodě absurdní). Kademlia by prostě nefungovala. Byl to pěkný nápad, ale ne pro nepřátelské a proměnlivé prostředí.

### Aktuální stav

NetDb hraje velmi specifickou roli v síti I2P a algoritmy byly vyladěny podle našich potřeb. To také znamená, že nebyly vyladěny pro řešení potřeb, se kterými se ještě nesetkáváme. I2P je v současnosti poměrně malé (několik stovek routerů). Proběhly některé výpočty, že 3-5 floodfill routerů by mělo být schopno zvládnout 10 000 uzlů v síti. Implementace netDb v současnosti více než dostatečně splňuje naše potřeby, ale pravděpodobně dojde k dalšímu ladění a opravám chyb s růstem sítě.

### Aktualizace výpočtů 03-2008

Aktuální čísla:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
kde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Změny v předpokladech:

- L je nyní asi 0,5, ve srovnání s 0,1 výše, kvůli popularitě i2psnark
  a dalších aplikací.
- F je asi 0,33, ale chyby v testování tunnelů jsou opraveny ve verzi 0.6.1.33, takže se to výrazně zlepší.
- Protože netDb obsahuje asi 2/3 routerInfos o velikosti 5K a 1/3 leaseSets o velikosti 2K, S = 4K.
  Velikost RouterInfo se ve verzích 0.6.1.32 a 0.6.1.33 zmenšuje, protože odstraňujeme nepotřebné statistiky.
- R = doba vytváření tunnelu: 0,2 bylo velmi nízké - možná to bylo 0,7 -
  ale vylepšení algoritmu vytváření ve verzi 0.6.1.32 by to mělo snížit na asi 0,2
  jak se síť upgraduje. Označme to teď jako 0,5 s polovinou sítě na verzi .30 nebo starší.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
To se týká pouze úložišť - co ale dotazy?

### Návrat algoritmu Kademlia?

*(Upraveno ze schůzky I2P ze 2. ledna 2007)*

Kademlia netDb prostě nefungovala správně. Je navždy mrtvá, nebo se vrátí? Pokud se vrátí, uzly v Kademlia netDb by byly velmi omezenou podmnožinou routerů v síti (v podstatě rozšířený počet floodfill uzlů, pokud/když floodfill uzly nezvládnou zátěž). Ale dokud floodfill uzly zvládají zátěž (a nelze přidat další uzly, které by to zvládly), je to zbytečné.

### Budoucnost Floodfill

*(Upraveno z IRC konverzace s jrandom 11/07)*

Zde je návrh: Třída kapacity O je automaticky floodfill. Hmm. Pokud si nejsme jisti, mohli bychom skončit s efektním způsobem DDoS útoku na všechny routery třídy O. To je docela problém: chceme se ujistit, že počet floodfill je co nejmenší, zatímco poskytuje dostatečnou dostupnost. Pokud/když netDb požadavky selžou, pak potřebujeme zvýšit počet floodfill peerů, ale momentálně si nejsem vědom problému s načítáním netDb. Podle mých záznamů existuje 33 peerů třídy "O". 33 je /hodně/ na floodfill.

Takže floodfill funguje nejlépe, když je počet uzlů v tomto poolu pevně omezen? A velikost floodfill poolu by neměla moc růst, ani když by se síť sama postupně rozšiřovala? 3-5 floodfill uzlů dokáže zvládnout 10K routerů, pokud si správně pamatuji (zveřejnil jsem spoustu čísel vysvětlujících detaily ve starém syndie). Zní to jako obtížný požadavek k splnění pomocí automatického opt-in, zvláště pokud uzly, které se přihlašují, nemohou důvěřovat datům od ostatních. např. "podívejme se, jestli jsem mezi top 5", a mohou důvěřovat pouze datům o sobě samých (např. "rozhodně jsem třídy O, přenáším 150 KB/s a běžím už 123 dní"). A top 5 je také nepřátelské. V podstatě je to stejné jako tor directory servery - vybrané důvěryhodnými lidmi (alias vývojáři). Jo, právě teď by to mohlo být zneužito opt-in, ale to by bylo triviální detekovat a vyřešit. Zdá se, že nakonec možná budeme potřebovat něco užitečnějšího než Kademlia, a nechat se zapojit jen rozumně schopné uzly. Třída N a vyšší by měla být dostatečně velké množství na potlačení rizika, že protivník způsobí odmítnutí služby, doufám. Ale muselo by se to lišit od floodfill v tom smyslu, že by to nezpůsobovalo obrovský provoz. Velké množství? Pro DHT založenou netDb? Nemusí být nutně založeno na DHT.

### Seznam úkolů pro floodfill {#todo}

POZNÁMKA: Následující informace nejsou aktuální. Aktuální stav a seznam budoucí práce naleznete na [hlavní stránce netDb](/docs/overview/network-database).

Síť byla snížena na pouze jeden floodfill po dobu několika hodin dne 13. března 2008 (přibližně 18:00 - 20:00 UTC), což způsobilo mnoho problémů.

Dvě změny implementované ve verzi 0.6.1.33 by měly snížit narušení způsobené odstraněním nebo změnami floodfill peerů:

1. Náhodně vybírejte floodfill peery používané pro vyhledávání pokaždé.
   To vás nakonec dostane kolem těch nefunkčních.
   Tato změna také opravila ošklivou chybu, která někdy mohla dovést kód pro ff vyhledávání k šílenství.
2. Preferujte floodfill peery, které jsou aktivní.
   Kód se nyní vyhýbá peerům, kteří jsou na shitlistu, selhávají, nebo o kterých nebylo půl hodiny nic slyšet, pokud je to možné.

Jedna výhoda je rychlejší první kontakt s I2P Site (tj. když jste museli nejprve načíst leaseset). Timeout vyhledávání je 10s, taktakže pokud nezačnete dotazem na peer, který nefunguje, můžete ušetřit 10s.

V těchto změnách *mohou* být důsledky pro anonymitu. Například ve floodfill **store** kódu jsou komentáře, že shitlistovaní peerové nejsou vyhýbáni, protože peer by mohl být "shitty" a pak vidět, co se stane. Vyhledávání jsou mnohem méně zranitelná než ukládání - jsou mnohem méně častá a prozrazují méně informací. Takže možná si nemyslíme, že se o to musíme starat? Ale pokud chceme změny upravit, bylo by snadné poslat to peerovi uvedenému jako "down" nebo shitlistovanému stejně, jen to nepočítat jako součást těch 2, kterým posíláme (protože opravdu neočekáváme odpověď).

Existuje několik míst, kde je vybírán floodfill peer - tato oprava řeší pouze jedno - od koho běžný peer vyhledává [2 najednou]. Další místa, kde by měl být implementován lepší výběr floodfill:

1. Kam běžný peer ukládá [1 najednou]
   (náhodně - je třeba přidat kvalifikaci, protože timeouty jsou dlouhé)
2. Kam běžný peer vyhledává pro ověření uložení [1 najednou]
   (náhodně - je třeba přidat kvalifikaci, protože timeouty jsou dlouhé)
3. Koho floodfill peer posílá v odpovědi na neúspěšné vyhledávání (3 nejbližší k vyhledávání)
4. Kam floodfill peer posílá flood (všem ostatním floodfill peers)
5. Seznam floodfill peers posílaný v NTCP každých 6 hodin "šepot"
   (ačkoli to již nemusí být nutné díle jiným floodfill vylepšením)

Mnohem více toho, co by se mohlo a mělo udělat:

- Použít statistiky "dbHistory" k lepšímu hodnocení integrace floodfill peer
- Použít statistiky "dbHistory" k okamžité reakci na floodfill peers, které neodpovídají
- Být chytřejší při opakovaných pokusech - opakované pokusy jsou zpracovávány vyšší vrstvou, ne v
  FloodOnlySearchJob, takže to provede další náhodné řazení a zkusí to znovu,
  místo účelného přeskočení ff peers, které jsme právě vyzkoušeli.
- Více vylepšit statistiky integrace
- Skutečně používat statistiky integrace místo jen indikace floodfill v netDb
- Používat také statistiky latence?
- Další vylepšení v rozpoznávání selhávajících floodfill peers

Nedávno dokončeno:

- [Ve verzi 0.6.3]
  Implementovat automatické přihlášení
  do floodfill pro určité procento peers třídy O, založené na analýze sítě.
- [Ve verzi 0.6.3]
  Pokračovat ve snižování velikosti netDb záznamů pro snížení floodfill provozu -
  nyní jsme na minimálním počtu statistik potřebných pro monitorování sítě.
- [Ve verzi 0.6.3]
  Ruční seznam floodfill peers k vyloučení
  ([seznamy blokovaných](/docs/overview/threat-model#blocklist) podle router identifikátoru)
- [Ve verzi 0.6.3]
  Lepší výběr floodfill peers pro ukládání:
  Vyvarovat se peers, jejichž netDb je zastaralá, nebo měli nedávno neúspěšné uložení,
  nebo jsou trvale na černé listině.
- [Ve verzi 0.6.4]
  Upřednostňovat již připojené floodfill peers pro ukládání RouterInfo, aby se
  snížil počet přímých připojení k floodfill peers.
- [Ve verzi 0.6.5]
  Peers, kteří již nejsou floodfill, odesílají své routerInfo v odpovědi
  na dotaz, takže router provádějící dotaz bude vědět, že již
  není floodfill.
- [Ve verzi 0.6.5]
  Další ladění požadavků pro automatické stání se floodfill
- [Ve verzi 0.6.5]
  Oprava profilování času odpovědi v přípravě na upřednostňování rychlých floodfills
- [Ve verzi 0.6.5]
  Zlepšení blokování
- [Ve verzi 0.7]
  Oprava netDb průzkumu
- [Ve verzi 0.7]
  Zapnutí blokování ve výchozím nastavení, blokování známých problematických uzlů
- [Několik zlepšení v nedávných verzích, pokračující úsilí]
  Snížení požadavků na zdroje u vysokorychlostních a floodfill routerů

To je dlouhý seznam, ale bude potřeba tolik práce, abychom měli síť, která odolá DOS útokům od mnoha peerů, kteří zapínají a vypínají floodfill přepínač. Nebo předstírají, že jsou floodfill router. Nic z toho nebyl problém, když jsme měli pouze dva ff routery a oba byly v provozu 24/7. Opět, jrandomova nepřítomnost nám ukázala místa, která potřebují zlepšení.

Pro podporu tohoto úsilí jsou nyní (od verze 0.6.1.33) na stránce "Profily" v konzoli routeru zobrazena dodatečná profilová data pro floodfill peery. Tato data použijeme k analýze toho, která data jsou vhodná pro hodnocení floodfill peerů.

Síť je v současnosti poměrně odolná, nicméně budeme pokračovat ve vylepšování našich algoritmů pro měření a reakci na výkon a spolehlivost floodfill peerů. Ačkoli momentálně nejsme plně chráněni proti potenciálním hrozbám škodlivých floodfillů nebo floodfill DDOS, většina infrastruktury je na místě a jsme dobře připraveni rychle reagovat, pokud bude potřeba.
