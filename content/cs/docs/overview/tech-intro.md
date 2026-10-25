---
title: "I2P: Technický úvod"
description: "Technický úvod do architektury a fungování I2P"
slug: "tech-intro"
aliases:
  - "/cs/techintro"
  - "/cs/techintro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

POZNÁMKA: Tento dokument byl původně napsán jrandom v roce 2003. I když se snažíme jej udržovat aktuální, některé informace mohou být zastaralé nebo neúplné. Sekce o transportu a kryptografii jsou aktuální k lednu 2025.

## Úvod

I2P je škálovatelná, samoorganizující se, odolná paketově přepínaná anonymní síťová vrstva, na které může fungovat libovolný počet různých aplikací zaměřených na anonymitu nebo bezpečnost. Každá z těchto aplikací si může vytvořit vlastní kompromisy mezi anonymitou, latencí a propustností, aniž by se musela starat o správnou implementaci free route mixnet (svobodné směrovací míchací sítě), což jim umožňuje prolnout svou aktivitu s větší množinou anonymních uživatelů, kteří již běží na I2P.

Již dostupné aplikace poskytují plný rozsah typických internetových aktivit — **anonymní** prohlížení webu, webhosting, chat, sdílení souborů, e-mail, blogování a syndikaci obsahu, stejně jako několik dalších aplikací ve vývoji.

- Procházení webu: použití jakéhokoliv existujícího prohlížeče, který podporuje používání proxy.
- Chat: IRC a další protokoly
- Sdílení souborů: [I2PSnark](#i2psnark) a další aplikace
- E-mail: [susimail](#i2pmail--susimail) a další aplikace
- Blog: použití jakéhokoliv lokálního webového serveru nebo dostupných pluginů

Na rozdíl od webových stránek hostovaných v sítích pro distribuci obsahu jako [Freenet](#freenet) nebo [GNUnet](https://www.gnunet.org/en/), jsou služby hostované na I2P plně interaktivní — existují tradiční webové vyhledávače, diskusní fóra, blogy, na které můžete komentovat, stránky řízené databázemi a mosty pro dotazování statických systémů jako Freenet bez nutnosti lokální instalace.

Se všemi těmito aplikacemi s podporou anonymity převezme I2P roli middleware orientovaného na zprávy — aplikace říkají, že chtějí poslat nějaká data na kryptografický identifikátor ("destination") a I2P se postará o to, aby se tam dostala bezpečně a anonymně. I2P také obsahuje jednoduchou [streaming](#streaming-library) knihovnu, která umožňuje I2P anonymním best-effort zprávám přenášet se jako spolehlivé, uspořádané proudy, transparentně nabízející TCP algoritmus pro řízení zahlcení laděný pro vysoký bandwidth delay product sítě. Zatímco bylo k dispozici několik jednoduchých SOCKS proxy pro napojení existujících aplikací do sítě, jejich hodnota byla omezená, protože téměř každá aplikace běžně odhaluje to, co je v anonymním kontextu citlivou informací. Jediný bezpečný způsob je plně auditovat aplikaci, aby byla zajištěna správná funkce, a pro podporu v tom poskytujeme sérii API v různých jazycích, která lze použít pro maximální využití sítě.

I2P není výzkumný projekt — akademický, komerční nebo vládní — ale je to spíše inženýrské úsilí zaměřené na to, aby poskytl dostatečnou úroveň anonymity těm, kteří ji potřebují. Je aktivně vyvíjen od začátku roku 2003 s jedním vývojářem na plný úvazek a oddanou skupinou vývojářů na částečný úvazek z celého světa. Veškerá práce na I2P je open source a volně dostupná na [webových stránkách](/), přičemž většina kódu je uvolněna přímo do public domain (veřejné domény), ačkoli využívá několik kryptografických rutin pod BSD-style licencemi. Lidé pracující na I2P nekontrolují, pod jakými licencemi vydávají vývojáři klientské aplikace, a je k dispozici několik GPL aplikací ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex a další). Financování I2P pochází výhradně z darů a v současné době nepobírá žádné daňové úlevy v žádné jurisdikci, protože mnoho vývojářů je samo anonymních.

---

## Provoz

### Přehled

Pro pochopení fungování I2P je nezbytné porozumět několika klíčovým konceptům. Zaprvé, I2P striktně odděluje software účastnící se sítě (router) a anonymní koncové body ("destinations") spojené s jednotlivými aplikacemi. Skutečnost, že někdo provozuje I2P, obvykle není tajemství. To, co je skryto, jsou informace o tom, co uživatel dělá, pokud vůbec něco, a také k jakému routeru je konkrétní destination připojena. Koncoví uživatelé mají typicky několik lokálních destinations na svém routeru — například jednu pro proxy připojení k IRC serverům, druhou podporující uživatelův anonymní webserver ("I2P Site"), další pro instanci I2Phex, další pro torrenty atd.

Dalším klíčovým konceptem, kterému je třeba porozumět, je "tunnel". Tunnel je směrovaná cesta skrze výslovně vybraný seznam routerů. Používá se vrstvené šifrování, takže každý z routerů může dešifrovat pouze jednu vrstvu. Dešifrované informace obsahují IP adresu dalšího routeru spolu se šifrovanými informacemi, které mají být přeposlány. Každý tunnel má výchozí bod (první router, také známý jako "gateway") a koncový bod. Zprávy lze posílat pouze jedním směrem. Pro posílání zpráv zpět je potřeba další tunnel.

![Inbound and outbound tunnel schematic](/images/tunnels.svg) *Obrázek 1: Existují dva typy tunnelů: inbound a outbound.*

Existují dva typy tunelů: **"odchozí" tunely** odesílají zprávy pryč od tvůrce tunelu, zatímco **"příchozí" tunely** přinášejí zprávy k tvůrci tunelu. Kombinace těchto dvou tunelů umožňuje uživatelům posílat si navzájem zprávy. Odesílatel ("Alice" na výše uvedeném obrázku) nastavuje odchozí tunel, zatímco příjemce ("Bob" na výše uvedeném obrázku) vytváří příchozí tunel. Brána příchozího tunelu může přijímat zprávy od jakéhokoli jiného uživatele a bude je posílat dál až ke koncovému bodu ("Bob"). Koncový bod odchozího tunelu bude muset poslat zprávu dál k bráně příchozího tunelu. K tomu odesílatel ("Alice") přidá instrukce ke své zašifrované zprávě. Jakmile koncový bod odchozího tunelu dešifruje zprávu, bude mít instrukce k přeposlání zprávy správné příchozí bráně (bráně k "Bob").

Třetím klíčovým konceptem k pochopení je I2P **"network database"** (neboli "netDb") — pár algoritmů používaných ke sdílení síťových metadat. Dva typy přenášených metadat jsou **"routerInfo"** a **"leaseSets"** — routerInfo poskytuje routerům data nezbytná pro kontaktování konkrétního routeru (jejich veřejné klíče, transportní adresy, atd.), zatímco leaseSet poskytuje routerům informace nezbytné pro kontaktování konkrétní destinace. leaseSet obsahuje několik "leases" (pronájmů). Každý z těchto leases specifikuje tunnel gateway, která umožňuje dosažení konkrétní destinace. Úplné informace obsažené v lease:

- Příchozí brána pro tunnel, která umožňuje dosažení konkrétního cíle.
- Čas, kdy tunnel vyprší.
- Pár veřejných klíčů pro možnost šifrování zpráv (k odeslání přes tunnel a dosažení cíle).

Routery samy posílají své routerInfo do netDb přímo, zatímco leaseSets jsou posílány prostřednictvím odchozích tunnelů (leaseSets je třeba posílat anonymně, aby se zabránilo korelaci routeru s jeho leaseSets).

Můžeme kombinovat výše uvedené koncepty k vytvoření úspěšných spojení v síti.

Aby si Alice vybudovala své vlastní příchozí a odchozí tunnely, provede vyhledávání v netDb pro shromáždění routerInfo. Tímto způsobem získá seznamy peerů, které může použít jako přeskoky ve svých tunnelech. Poté může poslat build zprávu prvnímu přeskoku, požádat o konstrukci tunnelu a požádat ten router, aby poslal konstrukci zprávu dále, dokud nebude tunnel vybudován.

![Request information on other routers](/images/netdb_get_routerinfo_1.svg)

![Build tunnel using router information](/images/netdb_get_routerinfo_2.svg) *Obrázek 2: Informace o router jsou použity pro budování tunnel.*

Když Alice chce poslat zprávu Bobovi, nejprve provede vyhledávání v netDb, aby našla Bobův leaseSet, což jí poskytne jeho aktuální brány příchozích tunelů. Poté si vybere jeden ze svých odchozích tunelů a pošle zprávu dolů s instrukcemi pro koncový bod odchozího tunelu, aby předal zprávu jedné z bran Bobových příchozích tunelů. Když koncový bod odchozího tunelu obdrží tyto instrukce, předá zprávu podle požadavku, a když ji obdrží brána Bobova příchozího tunelu, je předána tunelem dolů k Bobovu routeru. Pokud chce Alice, aby jí Bob mohl na zprávu odpovědět, musí explicitně přenést svou vlastní destinaci jako součást samotné zprávy. To lze provést zavedením vyšší úrovně, což je implementováno v knihovně [streaming](#streaming-library). Alice může také zkrátit dobu odezvy tím, že připojí svůj nejnovější LeaseSet ke zprávě, takže Bob nemusí při odpovědi provádět vyhledávání v netDb, ale to je volitelné.

![Connect tunnels using LeaseSets](/images/netdb_get_leaseset.svg) *Obrázek 3: LeaseSety se používají k propojení odchozích a příchozích tunelů.*

Zatímco tunely samotné mají vrstvené šifrování pro zabránění neoprávněnému odhalení partnerům uvnitř sítě (stejně jako transportní vrstva sama brání neoprávněnému odhalení partnerům mimo síť), je nutné přidat další vrstvu end-to-end šifrování pro skrytí zprávy před koncovým bodem odchozího tunelu a bránou příchozího tunelu. Toto "garlic encryption" umožňuje Alice routeru zabalit více zpráv do jediné "garlic zprávy", zašifrované konkrétním veřejným klíčem, takže zprostředkující partneři nemohou určit ani kolik zpráv je v garlic obsaženo, co tyto zprávy říkají, nebo kam jsou jednotlivé "cloves" určeny. Pro typickou end-to-end komunikaci mezi Alice a Bobem bude garlic zašifrováno veřejným klíčem publikovaným v Bob's leaseSet, což umožňuje zašifrovat zprávu bez vydání veřejného klíče Bob's vlastnímu routeru.

Dalším důležitým faktem, který je třeba mít na paměti, je, že I2P je zcela založeno na zprávách a že některé zprávy mohou být cestou ztraceny. Aplikace využívající I2P mohou použít rozhraní orientované na zprávy a postarat se o vlastní potřeby řízení zahlcení a spolehlivosti, ale většina z nich by byla nejlépe obslužena opětovným použitím poskytované knihovny [streaming](#streaming-library) k pohledu na I2P jako na síť založenou na tocích.

---

### Tunnels

Příchozí i odchozí tunely fungují na podobných principech. Brána tunelu shromažďuje určitý počet zpráv tunelu a nakonec je předzpracuje do podoby vhodné pro doručení tunelem. Dále brána tato předzpracovaná data zašifruje a předá je prvnímu uzlu. Tento uzel a následující účastníci tunelu přidají vrstvu šifrování poté, co ověří, že se nejedná o duplikát, a pak je předají dalšímu uzlu. Nakonec zpráva dorazí do koncového bodu, kde jsou zprávy opět rozděleny a předány dále podle požadavku. Rozdíl vzniká v tom, co dělá tvůrce tunelu — u příchozích tunelů je tvůrce koncovým bodem a jednoduše dešifruje všechny přidané vrstvy, zatímco u odchozích tunelů je tvůrce bránou a předem dešifruje všechny vrstvy tak, aby po přidání všech vrstev šifrování pro jednotlivé uzly zpráva dorazila na koncový bod tunelu v čitelné podobě.

Výběr konkrétních peerů pro předávání zpráv a také jejich specifické pořadí je důležité pro pochopení charakteristik anonymity i výkonu I2P. Zatímco síťová databáze (network database, viz níže) má svá vlastní kritéria pro výběr peerů, které se mají dotazovat a na kterých se mají ukládat záznamy, tvůrci tunelů mohou používat jakékoli peery v síti v jakémkoli pořadí (a dokonce i jakýkoli počet krát) v rámci jediného tunelu. Pokud by byla globálně známa dokonalá data o latenci a kapacitě, výběr a pořadí by byly řízeny konkrétními potřebami klienta v souladu s jejich modelem hrozeb. Bohužel získávání dat o latenci a kapacitě anonymně není triviální a spoléhání na nedůvěryhodné peery pro poskytnutí těchto informací má své vlastní vážné důsledky pro anonymitu.

Z pohledu anonymity by nejjednodušší technikou bylo náhodně vybrat partnery z celé sítě, náhodně je seřadit a používat tyto partnery v tomto pořadí navždy. Z pohledu výkonu by nejjednodušší technikou bylo vybrat nejrychlejší partnery s potřebnou volnou kapacitou, rozložit zátěž napříč různými partnery pro zvládnutí transparentního přepínání při selhání a znovu vybudovat tunnel kdykoli se změní informace o kapacitě. Zatímco první přístup je křehký i neefektivní, druhý vyžaduje nedostupné informace a nabízí nedostatečnou anonymitu. I2P místo toho pracuje na nabídce řady strategií pro výběr partnerů spolu s kódem pro měření zohledňující anonymitu, který organizuje partnery podle jejich profilů.

Jako základ I2P neustále profiluje protějšky, se kterými interaguje, měřením jejich nepřímého chování — například když protějšek odpoví na netDb lookup za 1,3 sekundy, tato latence round trip je zaznamenána v profilech pro všechny routery zapojené do obou tunnelů (příchozího a odchozího), kterými prošel požadavek a odpověď, stejně jako do profilu dotazovaného protějška. Přímé měření, jako je latence transportní vrstvy nebo přetížení, se jako součást profilu nepoužívá, protože může být manipulováno a přidruženo k měřícímu routeru, což ho vystavuje triviálním útokům. Během shromažďování těchto profilů se na každém spouští série výpočtů pro shrnutí jeho výkonu — jeho latence, kapacity zvládat množství aktivity, zda je aktuálně přetížený a jak dobře se zdá být integrován do sítě. Tyto výpočty jsou pak porovnány pro aktivní protějšky za účelem uspořádání routerů do čtyř úrovní — rychlé a vysokokapacitní, vysokokapacitní, neselhaující a selhávající. Prahové hodnoty pro tyto úrovně jsou určovány dynamicky a ačkoli aktuálně používají poměrně jednoduché algoritmy, existují alternativy.

S využitím těchto profilových dat je nejjednodušší rozumná strategie výběru peerů náhodný výběr peerů z nejvyšší úrovně (rychlé a s vysokou kapacitou), což je v současnosti nasazeno pro klientské tunely. Průzkumné tunely (používané pro netDb a správu tunelů) vybírají peery náhodně z úrovně "neselhávaní" (která zahrnuje i routery z "lepších" úrovní), což umožňuje peeru vzorkovat routery šířeji, čímž v podstatě optimalizuje výběr peerů prostřednictvím randomizovaného [hill climbing](https://en.wikipedia.org/wiki/Hill_climbing). Tyto strategie samy o sobě však propouštějí informace týkající se peerů v nejvyšší úrovni routeru prostřednictvím útoků sběru předchůdců a netDb. Na oplátku existuje několik alternativ, které sice nevyvažují zátěž tak rovnoměrně, ale řeší útoky vedené určitými třídami protivníků.

Výběrem náhodného klíče a uspořádáním peerů podle jejich XOR vzdálenosti od něj se sníží množství uniklých informací při predecessor a harvesting útocích v závislosti na míře selhání peerů a fluktuaci úrovně. Další jednoduchou strategií pro řešení netDb harvesting útoků je jednoduše fixovat brány vstupního tunnelu, ale randomizovat peery dále v tunnelech. Pro řešení predecessor útoků u protivníků, které klient kontaktuje, by také zůstaly fixované koncové body odchozího tunnelu. Výběr toho, kterého peera fixovat na nejexponovanějším místě, by samozřejmě musel mít časové omezení, protože všichni peerové nakonec selžou, takže by to mohlo být buď reaktivně upraveno, nebo proaktivně zabráněno tak, aby napodobovalo naměřený průměrný čas mezi selháními jiných routerů. Tyto dvě strategie mohou být kombinovány, používat fixovaného exponovaného peera a XOR založené uspořádání v rámci samotných tunnelů. Rigidnější strategie by fixovala přesné peery a uspořádání potenciálního tunnelu, používala by jednotlivé peery pouze pokud všichni souhlasí s účastí stejným způsobem pokaždé. To se liší od XOR založeného uspořádání v tom, že predecessor a successor každého peera je vždy stejný, zatímco XOR pouze zajišťuje, že se jejich pořadí nemění.

Jak bylo zmíněno dříve, I2P v současnosti (verze 0.8) zahrnuje výše uvedenou vrstvovou náhodnou strategii s řazením založeným na XOR. Podrobnější diskuzi o mechanismech zapojených do provozu tunelů, správy a výběru peerů lze nalézt ve [specifikaci tunelů](/docs/specs/tunnel-implementation/).

---

### Network Database (netDb)

Jak bylo zmíněno dříve, I2P netDb slouží ke sdílení metadat sítě. To je podrobně popsáno na stránce [síťová databáze](/docs/specs/common-structures/), ale základní vysvětlení je k dispozici níže.

Všechny I2P routery obsahují lokální netDb, ale ne všechny routery se účastní DHT nebo odpovídají na dotazy pro leaseSet. Routery, které se účastní DHT a odpovídají na dotazy pro leaseSet, se nazývají 'floodfill'. Routery mohou být manuálně nakonfigurovány jako floodfill, nebo se automaticky stanou floodfill, pokud mají dostatečnou kapacitu a splňují další kritéria pro spolehlivý provoz.

Ostatní I2P routery budou ukládat svá data a vyhledávat data odesláním jednoduchých dotazů 'store' a 'lookup' do floodfill. Pokud floodfill router obdrží dotaz 'store', rozšíří informaci do ostatních floodfill routerů pomocí [algoritmu Kademlia](http://en.wikipedia.org/wiki/Kademlia). Dotazy 'lookup' v současnosti fungují odlišně, aby se předešlo důležitému bezpečnostnímu problému. Když je proveden lookup, floodfill router nepředá lookup ostatním uzlům, ale vždy odpoví sám za sebe (pokud má požadovaná data).

V síťové databázi jsou uloženy dva typy informací.

- **RouterInfo** ukládá informace o konkrétním I2P router a způsobu, jak jej kontaktovat
- **LeaseSet** ukládá informace o konkrétní destinaci (např. I2P webová stránka, e-mailový server...)

Všechny tyto informace jsou podepsány publikující stranou a ověřeny jakýmkoli I2P routerem, který informace používá nebo ukládá. Kromě toho data obsahují časové informace, aby se zabránilo ukládání starých záznamů a možným útokům. To je také důvod, proč I2P obsahuje potřebný kód pro udržování správného času, občas dotazuje některé SNTP servery (ve výchozím nastavení [pool.ntp.org](http://www.pool.ntp.org/) round robin) a detekuje časové odchylky mezi routery na transportní vrstvě.

Některé dodatečné poznámky jsou také důležité.

- **Nepublikované a šifrované leaseSet:**
  Někdo může chtít, aby určité místo bylo dostupné pouze konkrétním lidem. To je možné tím, že se místo nepublikuje v netDb. Budete však muset přenést místo jiným způsobem. Toto je podporováno pomocí 'šifrovaných leaseSet'. Tyto leaseSet mohou dekódovat pouze lidé s přístupem k dešifrovacímu klíči.

- **Bootstrapping:**
  Bootstrapping netDb je poměrně jednoduché. Jakmile se router dokáže připojit k jedinému routerInfo dostupného protějšku, může se tohoto router dotazovat na odkazy na další routery v síti. V současnosti řada uživatelů zveřejňuje své routerInfo soubory na webové stránce, aby tyto informace zpřístupnili. I2P se automaticky připojí k jedné z těchto webových stránek, aby shromáždil routerInfo soubory a provedl bootstrap. I2P tento bootstrap proces nazývá "reseeding".

- **Škálovatelnost vyhledávání:**
  Vyhledávání v síti I2P je iterativní, nikoliv rekurzivní. Pokud vyhledávání z floodfill selže, vyhledávání se zopakuje na další nejbližší floodfill. Floodfill nerekurzivně nepožádá jiný floodfill o data. Iterativní vyhledávání je škálovatelné pro velké DHT sítě.

---

### Transportní protokoly

Komunikace mezi routery musí poskytovat důvernost a integritu proti externím útočníkům, přičemž současně ověřuje, že kontaktovaný router je ten, který by měl danou zprávu obdržet. Konkrétní způsob, jakým routery komunikují s jinými routery, není kritický — tři různé protokoly byly v různých bodech použity k poskytnutí těchto základních potřeb.

I2P v současnosti podporuje dva transportní protokoly, [NTCP2](/docs/specs/ntcp2/) přes TCP a [SSU2](/docs/specs/ssu2/) přes UDP. Tyto nahradily předchozí verze protokolů, [NTCP](/docs/legacy/ssu/) a [SSU](/docs/legacy/ssu/), které jsou nyní zastaralé. Oba protokoly podporují jak IPv4, tak IPv6. Podporou jak TCP, tak UDP transportů může I2P efektivně procházet většinou firewallů, včetně těch určených k blokování provozu v restriktivních cenzurních režimech. NTCP2 a SSU2 byly navrženy tak, aby používaly moderní šifrovací standardy, zlepšily odolnost proti identifikaci provozu, zvýšily efektivitu a bezpečnost a učinily procházení NAT robustnějším. Routery publikují každý podporovaný transport a IP adresu v síťové databázi. Routery s přístupem k veřejným IPv4 a IPv6 sítím obvykle publikují čtyři adresy, jednu pro každou kombinaci NTCP2/SSU2 s IPv4/IPv6.

[SSU2](/docs/specs/ssu2/) podporuje a rozšiřuje cíle SSU. SSU2 má mnoho podobností s jinými moderními protokoly založenými na UDP, jako jsou Wireguard a QUIC. Kromě spolehlivého přenosu síťových zpráv přes UDP poskytuje SSU2 specializované funkce pro peer-to-peer detekci IP adres, detekci firewallů a NAT traversal založené na spolupráci. Jak je popsáno ve [specifikaci SSU](/docs/legacy/ssu/):

> Cílem tohoto protokolu je poskytovat bezpečné, autentizované, částečně spolehlivé a neuspořádané doručování zpráv, přičemž třetím stranám odhaluje pouze minimální množství snadno rozpoznatelných dat. Měl by podporovat komunikaci s vysokým stupněm propustnosti, stejně jako TCP-friendly řízení zahlcení a může zahrnovat detekci PMTU. Měl by být schopen efektivně přesouvat objemná data rychlostmi dostatečnými pro domácí uživatele. Kromě toho by měl podporovat techniky pro řešení síťových překážek, jako je většina NAT nebo firewallů.

[NTCP2](/docs/specs/ntcp2/) podporuje a rozšiřuje cíle NTCP. Poskytuje efektivní a plně šifrovaný přenos síťových zpráv přes TCP a odolnost proti identifikaci provozu pomocí moderních šifrovacích standardů.

I2P podporuje více transportů současně. Konkrétní transport pro odchozí spojení se vybírá pomocí "nabídek". Každý transport podává nabídku na spojení a relativní hodnota těchto nabídek určuje prioritu. Transporty mohou odpovědět různými nabídkami v závislosti na tom, zda již existuje navázané spojení s protějškem.

Hodnoty bid (priority) jsou závislé na implementaci a mohou se lišit na základě podmínek provozu, počtu připojení a dalších faktorů. Routery také publikují své transportní preference pro příchozí připojení v síťové databázi jako transportní "náklady" pro každý transport a adresu.

---

### Kryptografie

I2P používá kryptografii na několika protokolových vrstvách pro šifrování, autentifikaci a ověřování. Hlavní protokolové vrstvy jsou: transporty, zprávy pro budování tunelů, šifrování tunelové vrstvy, zprávy síťové databáze a end-to-end (garlic) zprávy. Původní návrh I2P používal malou sadu kryptografických primitiv, které byly v té době považovány za bezpečné. Patřily mezi ně ElGamal asymetrické šifrování, DSA-SHA1 podpisy, AES256/CBC symetrické šifrování a SHA-256 hashe. S rostoucím dostupným výpočetním výkonem a značným vývojem kryptografického výzkumu během let bylo potřeba, aby I2P upgradovalo své primitivy a protokoly. Proto jsme přidali koncept "typů šifrování" a "typů podpisů" a rozšířili naše protokoly tak, aby zahrnovaly tyto identifikátory a indikovaly podporu. To nám umožňuje periodicky aktualizovat a rozšiřovat síťovou podporu pro moderní kryptografii a připravit síť na budoucí primitivy, aniž bychom narušili zpětnou kompatibilitu nebo vyžadovali "den D" pro síťové aktualizace. Některé typy podpisů a šifrování jsou také rezervovány pro experimentální použití.

Současné primitiva používané ve většině vrstev protokolu jsou X25519 výměna klíčů, EdDSA podpisy, ChaCha20/Poly1305 ověřované symetrické šifrování a SHA-256 hashe. AES256 se stále používá pro šifrování tunnel vrstvy. Tyto moderní protokoly se používají pro naprostou většinu síťové komunikace. Starší primitiva včetně ElGamal, ECDSA a DSA-SHA1 nadále podporuje většina implementací kvůli zpětné kompatibilitě při komunikaci se staršími routery. Některé staré protokoly byly označeny jako zastaralé a/nebo zcela odstraněny. V blízké budoucnosti začneme výzkum migrace na post-kvantové (PQ) nebo hybridní-PQ šifrování a podpisy, abychom udrželi naše robustní bezpečnostní standardy.

Tyto kryptografické primitiva jsou kombinována dohromady, aby poskytly vrstvené obrany I2P proti různým protivníkům. Na nejnižší úrovni je komunikace mezi routery chráněna zabezpečením transportní vrstvy. Zprávy [tunelů](#tunnels) předávané přes transporty mají své vlastní vrstvené šifrování. Různé další zprávy jsou předávány uvnitř "garlic messages", které jsou také šifrované.

#### Garlic Messages

Garlic zprávy jsou rozšířením "cibulového" vrstveného šifrování, které umožňuje obsahu jedné zprávy obsahovat více "květů" — plně vytvořené zprávy spolu s jejich vlastními instrukcemi pro doručení. Zprávy jsou zabaleny do garlic zprávy, kdykoli by zpráva jinak procházela v nešifrovaném textu přes uzel, který by neměl mít přístup k informacím — například když router chce požádat jiný router o účast v tunnelu, zabalí požadavek do garlic zprávy, zašifruje tuto garlic zprávu veřejným klíčem přijímajícího routeru a předá ji přes tunnel. Dalším příkladem je, když klient chce poslat zprávu na určité místo — router odesílatele zabalí tuto datovou zprávu (spolu s některými dalšími zprávami) do garlic zprávy, zašifruje tuto garlic zprávu veřejným klíčem publikovaným v leaseSet příjemce a předá ji přes příslušné tunnely.

"Instrukce" připojené ke každému clove uvnitř šifrovací vrstvy zahrnují možnost požádat o přeposlání clove lokálně, na vzdálený router nebo do vzdáleného tunelu na vzdáleném routeru. V těchto instrukcích jsou pole, která umožňují peer požádat o odložení doručení až do určitého času nebo dokud nebude splněna určitá podmínka, ačkoliv tyto požadavky nebudou respektovány, dokud nebudou nasazena [netriviální zpoždění](#variable-latency). Je možné explicitně směrovat garlic zprávy libovolný počet hopů bez budování tunelů, nebo dokonce přesměrovat tunelové zprávy jejich zabalením do garlic zpráv a přeposlání několik hopů před jejich doručením k dalšímu hopu v tunelu, ale tyto techniky nejsou v současné implementaci používány.

#### Značky relace

Jako nespolehlivý, neuspořádaný systém založený na zprávách používá I2P jednoduchou kombinaci asymetrických a symetrických šifrovacích algoritmů k zajištění důvernosti a integrity dat v garlic zprávách. Původní kombinace byla označována jako ElGamal/AES+SessionTags, ale to je příliš podrobný způsob popisu jednoduchého použití 2048bit ElGamal, AES256, SHA256 a 32 bajtových nonces. Ačkoliv je tento protokol stále podporován, většina sítě přešla na nový protokol ECIES-X25519-AEAD-Ratchet. Tento protokol kombinuje X25519, ChaCha20/Poly1305 a synchronizovaný PRNG pro generování 32 bajtových nonces. Oba protokoly budou stručně popsány níže.

#### ElGamal/AES+SessionTags

Když chce router poprvé šifrovat garlic zprávu jinému routeru, zašifruje klíčový materiál pro AES256 session klíč pomocí ElGamal a připojí AES256/CBC šifrovaný payload za tento zašifrovaný ElGamal blok. Kromě šifrovaného payload obsahuje AES šifrovaná sekce délku payload, SHA256 hash nešifrovaného payload a také řadu "session tags" — náhodných 32bajtových nonces. Když chce odesílatel příště šifrovat garlic zprávu jinému routeru, místo ElGamal šifrování nového session klíče jednoduše vybere jeden z dříve doručených session tags a AES zašifruje payload jako předtím, pomocí session klíče používaného s daným session tag, s předponou samotného session tag. Když router obdrží garlic šifrovanou zprávu, zkontroluje prvních 32 bajtů, zda odpovídají dostupnému session tag — pokud ano, jednoduše AES dešifrují zprávu, ale pokud ne, ElGamal dešifrují první blok.

Každý session tag může být použit pouze jednou, aby se zabránilo vnitřním útočníkům zbytečně korelovat různé zprávy jako pocházející mezi stejnými routery. Odesílatel ElGamal/AES+SessionTag šifrované zprávy si volí, kdy a kolik tagů doručit, předem zásobí příjemce dostatečným množstvím tagů pro pokrytí salvě zpráv. Garlic zprávy mohou detekovat úspěšné doručení tagů spojením malé dodatečné zprávy jako clove ("delivery status message") — když garlic zpráva dorazí k zamýšlenému příjemci a je úspěšně dešifrována, tato malá delivery status zpráva je jedním z odhalených cloves a obsahuje instrukce pro příjemce, aby clove poslal zpět původnímu odesílateli (samozřejmě přes inbound tunnel). Když původní odesílatel obdrží tuto delivery status zprávu, ví, že session tagy spojené v garlic zprávě byly úspěšně doručeny.

Samotné session tags mají velmi krátkou životnost, po které jsou zahozeny, pokud se nepoužívají. Navíc je omezeno množství uložené pro každý klíč, stejně jako počet samotných klíčů — pokud jich přijde příliš mnoho, mohou být zahozeny buď nové nebo staré zprávy. Odesílatel sleduje, zda zprávy používající session tags procházejí, a pokud není dostatečná komunikace, může zahodit ty, které dříve považoval za správně doručené, a vrátit se zpět k úplnému nákladnému ElGamal šifrování.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags vyžadovalo značnou režii v několika ohledech. Využití CPU bylo vysoké, protože ElGamal je poměrně pomalý. Šířka pásma byla nadměrná, protože velké množství session tagů muselo být doručeno předem a protože veřejné klíče ElGamal jsou velmi velké. Využití paměti bylo vysoké kvůli požadavku ukládat velké množství session tagů. Spolehlivost byla narušena ztrátou doručování session tagů.

ECIES-X25519-AEAD-Ratchet byl navržen k řešení těchto problémů. X25519 se používá pro výměnu klíčů. ChaCha20/Poly1305 se používá pro autentizované symetrické šifrování. Šifrovací klíče jsou "dvojitě ratchetovány" nebo pravidelně rotovány. Tagy relací jsou sníženy z 32 bajtů na 8 bajtů a jsou generovány pomocí PRNG. Protokol má mnoho podobností se signálovým protokolem používaným v aplikacích Signal a WhatsApp. Tento protokol poskytuje podstatně nižší režii v oblasti CPU, RAM a šířky pásma.

Značky relace jsou generovány z deterministického synchronizovaného PRNG běžícího na obou koncích relace pro generování značek relace a klíčů relace. PRNG je HKDF používající SHA-256 HMAC a je inicializován z výsledku X25519 DH. Značky relace nejsou nikdy předem přenášeny; jsou pouze zahrnuty se zprávou. Příjemce ukládá omezený počet klíčů relace indexovaných podle značky relace. Odesílatel nemusí ukládat žádné značky relace nebo klíče, protože nejsou odesílány předem; mohou být generovány na vyžádání. Udržováním tohoto PRNG přibližně synchronizovaného mezi odesílatelem a příjemcem (příjemce předpočítává okno následujících např. 50 značek) se odstraní režie periodického balíčkování velkého počtu značek.

---

## Budoucnost

Protokoly I2P jsou efektivní na většině platforem, včetně mobilních telefonů, a bezpečné pro většinu modelů hrozeb. Existuje však několik oblastí, které vyžadují další vylepšení, aby vyhovovaly potřebám těch, kteří čelí mocným státem sponzorovaným protivníkům, a aby čelily hrozbám pokračujících kryptografických pokroků a stále rostoucího výpočetního výkonu. Dvě možné funkce, omezené trasy a variabilní latence, byly navrženy jrandom v roce 2003. I když již neplánujeme implementovat tyto funkce, jsou popsány níže.

### Omezený provoz tras

I2P je overlay síť navržená k provozu nad funkční paketově přepínanou sítí, která využívá principu end-to-end k nabízení anonymity a bezpečnosti. Ačkoli Internet již plně nerespektuje princip end-to-end (kvůli používání NAT), I2P vyžaduje, aby podstatná část sítě byla dosažitelná — může existovat řada peerů na okrajích sítě provozovaných s omezenými trasami, ale I2P neobsahuje vhodný směrovací algoritmus pro degenerovaný případ, kdy je většina peerů nedosažitelná. Fungovala by však nad sítí využívající takový algoritmus.

Omezený provoz tras, kde existují omezení týkající se toho, které protějšky jsou přímo dosažitelné, má několik různých funkčních a anonymitních důsledků v závislosti na tom, jak jsou omezené trasy zpracovávány. Na nejzákladnější úrovni existují omezené trasy, když je protějšek za NATem nebo firewallom, který nepovoluje příchozí spojení. To bylo z velké části vyřešeno integrací distribuovaného hole punching do transportní vrstvy, což umožňuje lidem za většinou NATů a firewallů přijímat nevyžádaná spojení bez jakékoli konfigurace. To však neomezuje vystavení IP adresy protějška routerům uvnitř sítě, protože se mohou jednoduše seznámit s protějškem prostřednictvím publikovaného introduceru.

Kromě funkčního zpracování omezených tras existují dvě úrovně omezeného provozu, které lze použít k omezení vystavení své IP adresy — použití tunelů specifických pro router pro komunikaci a nabízení 'klientských routerů'. U prvního přístupu mohou routery buď vybudovat nový fond tunelů, nebo znovu použít svůj průzkumný fond, přičemž publikují vstupní brány některých z nich jako součást svého routerInfo místo svých transportních adres. Když se s nimi chce peer spojit, vidí tyto tunelové brány v netDb a jednoduše jim pošle příslušnou zprávu přes jeden z publikovaných tunelů. Pokud chce peer za omezenou trasou odpovědět, může tak učinit buď přímo (pokud je ochoten vystavit svou IP adresu peer), nebo nepřímo přes své odchozí tunely. Když routery, ke kterým má peer přímá spojení, chtějí dosáhnout na něj (například pro přeposílání tunelových zpráv), jednoduše upřednostní své přímé spojení před publikovanou tunelovou bránou. Koncept 'klientských routerů' jednoduše rozšiřuje omezenou trasu tím, že nepublikuje žádné adresy routeru. Takový router by ani nemusel publikovat své routerInfo v netDb, pouze by poskytoval své vlastnoručně podepsané routerInfo peerům, které kontaktuje (nezbytné pro předání veřejných klíčů routeru).

Pro ty, kteří jsou za omezenými trasami, existují kompromisy, protože by se pravděpodobně méně často podíleli na tunelech jiných lidí a routery, ke kterým jsou připojeni, by mohly odvodit vzorce provozu, které by jinak nebyly odhaleny. Na druhou stranu, pokud jsou náklady na toto odhalení menší než náklady na zpřístupnění IP adresy, může to stát za to. To samozřejmě předpokládá, že peerové, se kterými router za omezenou trasou navazuje kontakt, nejsou nepřátelští — buď je síť dostatečně velká, že pravděpodobnost použití nepřátelského peera k připojení je dostatečně malá, nebo se místo toho používají důvěryhodní (a možná dočasní) peerové.

Omezené trasy jsou složité a celkový cíl byl z velké části opuštěn. Několik souvisejících vylepšení výrazně snížilo jejich potřebu. Nyní podporujeme UPnP pro automatické otevírání portů firewallu. Podporujeme jak IPv4, tak IPv6. SSU2 vylepšil detekci adres, určování stavu firewallu a kooperativní NAT hole punching. SSU2, NTCP2 a kontroly kompatibility adres zajišťují, že se skoky tunelu mohou připojit před vybudováním tunelu. GeoIP a identifikace zemí nám umožňují vyhnout se protějškům v zemích s restriktivními firewally. Podpora pro "skryté" routery za těmito firewally se zlepšila. Některé implementace také podporují připojení k protějškům na překryvných sítích jako je Yggdrasil.

### Proměnná latence

I když se většina počátečních snah I2P zaměřovala na komunikaci s nízkou latencí, byl od počátku navržen s ohledem na služby s proměnlivou latencí. Na nejzákladnější úrovni mohou aplikace běžící nad I2P nabídnout anonymitu komunikace se střední a vysokou latencí, zatímco stále prolínají své vzorce provozu s provozem s nízkou latencí. Interně však může I2P nabízet svou vlastní komunikaci se střední a vysokou latencí prostřednictvím garlic encryption — specifikováním, že zpráva má být odeslána po určitém zpoždění, v určitém čase, po průchodu určitého počtu zpráv nebo jiné mix strategie. S vrstvovým šifrováním by pouze router, kterému clove odhalil požadavek na zpoždění, věděl, že zpráva vyžaduje vysokou latenci, což umožňuje provozu se dále prolínat s provozem s nízkou latencí. Jakmile je splněna přenosová podmínka, router držící clove (který by sám o sobě pravděpodobně byl garlic zprávou) ji jednoduše přepošle podle požadavku — routeru, do tunelu nebo, nejpravděpodobněji, do vzdálené cílové destinace klienta.

Cíl služeb s proměnnou latencí vyžaduje značné zdroje pro mechanismy store-and-forward, které je podporují. Tyto mechanismy mohou být a jsou podporovány v různých aplikacích pro zasílání zpráv, jako je i2p-bote. Na síťové úrovni poskytují tyto služby alternativní sítě jako Freenet. Rozhodli jsme se tento cíl na úrovni I2P routeru nesledovat.

---

## Podobné systémy

Architektura I2P staví na konceptech message oriented middleware, topologii DHT, anonymitě a kryptografii free route mixnets a adaptabilitě packet switched sítí. Hodnota však nepramení z nových konceptů či algoritmů, ale z pečlivého inženýrství kombinujícího výsledky výzkumu stávajících systémů a prací. Ačkoli existuje několik podobných projektů hodných přezkoumání, jak z technického tak funkčního hlediska, dva jsou zde zvláště vytaženy — Tor a Freenet.

Viz také [Stránka porovnání sítí](/docs/overview/comparison/). Poznámka: tyto popisy napsal jrandom v roce 2003 a nemusí být v současnosti přesné.

### Tor

*[webová stránka](https://www.torproject.org/)*

Na první pohled mají Tor a I2P mnoho funkčních a anonymitních podobností. Ačkoli vývoj I2P začal dříve, než jsme si byli vědomi raných snah o Tor, mnoho ponaučení z původního onion routing a ZKS úsilí bylo integrováno do designu I2P. Místo budování v podstatě důvěryhodného, centralizovaného systému s directory servery má I2P samoorganizující se síťovou databázi, kde každý peer přebírá odpovědnost za profilování ostatních routerů, aby určil, jak nejlépe využít dostupné zdroje. Další klíčový rozdíl je, že zatímco I2P i Tor používají vrstvené a uspořádané cesty (tunnely a circuits/streams), I2P je fundamentálně packet switched síť, zatímco Tor je fundamentálně circuit switched síť, což umožňuje I2P transparentně směrovat kolem přetížení nebo jiných síťových selhání, provozovat redundantní cesty a rozložit data napříč dostupnými zdroji. Zatímco Tor nabízí užitečnou outproxy funkcionalitu prostřednictvím integrovaného objevování a výběru outproxy, I2P ponechává taková rozhodnutí na aplikační vrstvě na aplikacích běžících nad I2P — ve skutečnosti I2P dokonce externalizoval samotnou TCP-like streaming knihovnu do aplikační vrstvy, což umožňuje vývojářům experimentovat s různými strategiemi a využívat jejich doménově specifické znalosti pro nabídnutí lepšího výkonu.

Z hlediska anonymity existuje značná podobnost při porovnání základních sítí. Existuje však několik klíčových rozdílů. Při řešení vnitřního protivníka nebo většiny vnějších protivníků vystavují I2P simplex tunnely poloviční množství dat o provozu než by vystavily Tor duplex okruhy pouhým pozorováním toků samotných — HTTP požadavek a odpověď by v Tor následovaly stejnou cestu, zatímco v I2P by pakety tvořící požadavek odešly skrze jeden nebo více outbound tunnelů a pakety tvořící odpověď by se vrátily skrze jeden nebo více různých inbound tunnelů. Zatímco I2P strategie výběru a řazení peerů by měly dostatečně řešit predecessor útoky, pokud by bylo nutné přejít na obousměrné tunnely, mohli bychom jednoduše vybudovat inbound a outbound tunnel podél stejných routerů.

Další problém s anonymitou vzniká při použití teleskopické tvorby tunelů v síti Tor, protože jednoduché počítání paketů a měření časování při průchodu buněk obvodem přes uzel protivníka odhaluje statistické informace o tom, kde se protivník v obvodu nachází. I2P používá jednosměrnou tvorbu tunelů s jedinou zprávou, takže tato data nejsou odhalena. Ochrana pozice v tunelu je důležitá, protože protivník by jinak mohl provést sérii mocných útoků předchůdce, průsečíku a potvrzení provozu.

Celkově se Tor a I2P ve svém zaměření doplňují — Tor se snaží nabídnout vysokorychlostní anonymní internetové outproxying, zatímco I2P se zaměřuje na nabídku decentralizované odolné sítě jako takové. Teoreticky lze oba použít k dosažení obou účelů, ale vzhledem k omezeným vývojovým zdrojům mají oba své silné a slabé stránky. Vývojáři I2P zvažovali kroky nutné k úpravě Toru tak, aby využil design I2P, ale obavy o životaschopnost Toru v podmínkách nedostatku zdrojů naznačují, že packet switching architektura I2P bude schopna efektivněji využívat omezené zdroje.

### Freenet

*[webové stránky](http://www.freenetproject.org/)*

Freenet sehrál významnou roli v počátečních fázích návrhu I2P — poskytl důkaz životaschopnosti pulzující pseudonymní komunity zcela obsažené v rámci sítě a demonstroval, že nebezpečím inherentním v outproxies se lze vyhnout. První zárodek I2P začal jako náhradní komunikační vrstva pro Freenet, snažící se vydělil složitosti škálovatelné, anonymní a bezpečné point-to-point komunikace od složitostí distribuovaného datového úložiště odolného vůči cenzuře. Postupem času však některé problémy s anonymitou a škálovatelností inherentní v algoritmech Frenet jasně ukázaly, že zaměření I2P by mělo zůstat striktně na poskytování obecné anonymní komunikační vrstvy, spíše než jako součást Frenet. V průběhu let vývojáři Frenet rozpoznali slabiny ve starším návrhu, což je přimělo navrhnout, že budou vyžadovat "premix" vrstvu pro poskytnutí podstatné anonymity. Jinými slovy, Freenet potřebuje běžet na vrcholu mixnet jako je I2P nebo Tor, s "klientskými uzly" požadujícími a publikujícími data přes mixnet k "serverovým uzlům", které pak načítají a ukládají data podle heuristických distribuovaných algoritmů datového úložiště Frenet.

Funkčnost Frenet je velmi komplementární k I2P, protože Freenet nativně poskytuje mnoho nástrojů pro provoz systémů se střední a vysokou latencí, zatímco I2P nativně poskytuje mixnet s nízkou latencí vhodnou pro nabídnutí přiměřené anonymity. Logika oddělení mixnet od cenzurně odolného distribuovaného úložiště dat stále vypadá samozřejmě z pohledu inženýrství, anonymity, bezpečnosti a alokace zdrojů, takže doufejme, že tým Freenet bude pokračovat v úsilí tímto směrem, pokud ne jednoduše znovu použije (nebo pomůže zlepšit, podle potřeby) existující mixnets jako I2P nebo Tor.

---

## Příloha A: Aplikační vrstva

I2P samo o sobě ve skutečnosti nedělá mnoho — jednoduše posílá zprávy na vzdálené cíle a přijímá zprávy určené pro místní cíle — většina zajímavé práce se odehrává ve vrstvách nad ním. Samo o sobě by I2P mohlo být vnímáno jako anonymní a bezpečná IP vrstva a přibalená [streaming library](#streaming-library) jako implementace anonymní a bezpečné TCP vrstvy nad ní. Kromě toho [I2PTunnel](#i2ptunnel) poskytuje obecný TCP proxy systém pro vstup do I2P sítě nebo výstup z ní, plus různé síťové aplikace poskytují další funkcionalitu pro koncové uživatele.

### Streaming knihovna

I2P streaming library lze chápat jako obecné rozhraní pro streamování (zrcadlící TCP sockety) a implementace podporuje [sliding window protocol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) s několika optimalizacemi, které zohledňují vysoké zpoždění v síti I2P. Jednotlivé streamy mohou upravovat maximální velikost paketu a další možnosti, ačkoli výchozí hodnota 4KB komprimovaných dat se jeví jako rozumný kompromis mezi náklady na šířku pásma při opětovném přenášení ztracených zpráv a latencí více zpráv.

Navíc, vzhledem k relativně vysokým nákladům následných zpráv, byl protokol streaming knihovny pro plánování a doručování zpráv optimalizován tak, aby umožnil jednotlivým předávaným zprávám obsahovat co nejvíce dostupných informací. Například malá HTTP transakce proxovaná přes streaming knihovnu může být dokončena v jediné cestě tam a zpět — první zpráva sdružuje SYN, FIN a malou datovou část (HTTP požadavek se typicky vejde) a odpověď sdružuje SYN, FIN, ACK a malou datovou část (mnoho HTTP odpovědí se vejde). Přestože musí být přenesen dodatečný ACK, aby se HTTP serveru oznámilo, že SYN/FIN/ACK bylo přijato, lokální HTTP proxy může doručit úplnou odpověď do prohlížeče okamžitě.

Celkově však streaming knihovna velmi připomíná abstrakci TCP se svými posuvnými okny, algoritmy řízení zahlcení (jak slow start, tak congestion avoidance) a obecným chováním paketů (ACK, SYN, FIN, RST atd.).

### Knihovna jmen a adresář

*Pro více informací viz stránka [Názvy a adresář](/docs/overview/naming/).*

*Vyvinuli: mihi, Ragnarok*

Pojmenovávání v rámci I2P je často diskutované téma od samého začátku s obhájci napříč celým spektrem možností. Nicméně vzhledem k inherentní potřebě I2P pro bezpečnou komunikaci a decentralizovaný provoz je tradiční systém pojmenovávání ve stylu DNS jasně vyloučen, stejně jako hlasovací systémy "rozhoduje většina". Místo toho se I2P dodává s obecnou knihovnou pro pojmenovávání a základní implementací navrženou pro práci s lokálním mapováním jmen na destinace, stejně jako s volitelnou doplňkovou aplikací nazvanou "Address Book". Address book je web-of-trust řízený bezpečný, distribuovaný a lidsky čitelný systém pojmenovávání, který obětuje pouze požadavek, aby všechna lidsky čitelná jména byla globálně jedinečná, a vyžaduje pouze lokální jedinečnost. Zatímco všechny zprávy v I2P jsou kryptograficky adresovány podle jejich destinace, různí lidé mohou mít lokální záznamy v address book pro "Alice", které se vztahují k různým destinacím. Lidé mohou stále objevovat nová jména importováním publikovaných address book partnerů specifikovaných v jejich web of trust, přidáváním záznamů poskytnutých prostřednictvím třetí strany, nebo (pokud někteří lidé zorganizují sérii publikovaných address book pomocí registračního systému "kdo dřív přijde, dřív mele") si mohou lidé vybrat, že budou tyto address book považovat za jmenné servery, čímž emulují tradiční DNS.

I2P však nepodporuje používání služeb podobných DNS, protože škoda způsobená únosem stránky může být obrovská — a nezabezpečené destinace nemají žádnou hodnotu. DNSsec samotné stále spoléhá na registrátory a certifikační autority, zatímco s I2P nelze požadavky odeslané na destinaci zachytit ani padělat odpověď, protože jsou šifrované veřejnými klíči destinace a destinace sama je jen pár veřejných klíčů a certifikát. Systémy ve stylu DNS naproti tomu umožňují kterémukoli ze jmenných serverů na cestě vyhledávání provést jednoduché útoky typu denial of service a spoofing. Přidání certifikátu ověřujícího odpovědi jako podepsané nějakou centralizovanou certifikační autoritou by vyřešilo mnoho problémů s nepřátelskými jmennými servery, ale ponechalo by otevřené replay útoky i útoky nepřátelských certifikačních autorit.

Pojmenování stylem hlasování je také nebezpečné, zejména vzhledem k účinnosti Sybil útoků v anonymních systémech — útočník může jednoduše vytvořit libovolně vysoký počet uzlů a "hlasovat" s každým, aby převzal kontrolu nad daným názvem. Metody proof-of-work lze použít k tomu, aby identita nebyla zdarma, ale jak síť roste, zátěž potřebná k tomu, aby se kontaktoval každý pro provedení online hlasování je nereálná, nebo pokud se nedotazuje celá síť, mohou být dostupné různé sady odpovědí.

Stejně jako u internetu však I2P udržuje návrh a provoz jmenného systému mimo komunikační vrstvu (podobnou IP). Přibalená jmenná knihovna obsahuje jednoduché rozhraní poskytovatele služeb, do kterého se mohou připojit alternativní jmenné systémy, což umožňuje koncovým uživatelům řídit, jaké kompromisy v pojmenovávání preferují.

### I2PTunnel

*Vyvinuto: mihi*

I2PTunnel je pravděpodobně nejpopulárnější a nejuniverzálnější klientská aplikace I2P, která umožňuje generické proxy připojení jak do I2P sítě, tak z ní ven. I2PTunnel lze chápat jako čtyři samostatné proxy aplikace — „client" který přijímá příchozí TCP spojení a přeposílá je na zadanou I2P destinaci, „httpclient" (také známý jako „eepproxy") který funguje jako HTTP proxy a přeposílá požadavky na příslušnou I2P destinaci (po dotázání se jmenné služby, pokud je to nutné), „server" který přijímá příchozí I2P streaming spojení na destinaci a přeposílá je na zadaný TCP host+port, a „httpserver" který rozšiřuje „server" tím, že analyzuje HTTP požadavky a odpovědi pro bezpečnější provoz. Existuje také dodatečná aplikace „socksclient", ale její používání se nedoporučuje z důvodů zmíněných dříve.

I2P samo o sobě není síť outproxy — obavy o anonymitu a bezpečnost inherentní v mix síti, která přeposílá data do mixu a z něj, udržely design I2P zaměřený na poskytování anonymní sítě, která je schopna naplnit potřeby uživatele bez vyžadování externích zdrojů. Aplikace I2PTunnel "httpclient" však nabízí háček pro outproxying — pokud požadované hostname nekončí na ".i2p", vybere náhodnou destinaci z uživatelem poskytnuté sady outproxy a přepošle jim požadavek. Tyto destinace jsou jednoduše instance I2PTunnel "server" provozované dobrovolníky, kteří se výslovně rozhodli provozovat outproxy — nikdo není ve výchozím nastavení outproxy a provozování outproxy automaticky neřekne ostatním lidem, aby přes vás proxy směřovali. Ačkoli outproxy mají inherentní slabiny, nabízejí jednoduchý důkaz konceptu pro používání I2P a poskytují určitou funkcionalitu pod modelem hrozeb, který může být pro některé uživatele dostatečný.

I2PTunnel umožňuje většinu používaných aplikací. "httpserver" směřující na webserver umožňuje komukoli provozovat vlastní anonymní webovou stránku (nebo "I2P Site") — webserver je součástí I2P pro tento účel, ale lze použít jakýkoli webserver. Kdokoli může provozovat "client" směřující na jeden z anonymně hostovaných IRC serverů, z nichž každý provozuje "server" směřující na svůj místní IRCd a komunikuje mezi IRCd přes vlastní "client" tunnely. Koncoví uživatelé mají také "client" tunnely směřující na POP3 a SMTP cíle [I2Pmail](#i2pmail--susimail) (které jsou zase jednoduše "server" instance směřující na POP3 a SMTP servery), stejně jako "client" tunnely směřující na CVS server I2P, což umožňuje anonymní vývoj. Někdy lidé dokonce provozovali "client" proxy pro přístup k "server" instancím směřujícím na NNTP server.

### I2PSnark

*I2PSnark vyvinul: jrandom a další, portováno z [mjw](http://www.klomp.org/mark/)'s [Snark](http://www.klomp.org/snark/) klienta*

I2PSnark, dodávaný s instalací I2P, nabízí jednoduchý anonymní BitTorrent klient s možností více torrentů současně, který zpřístupňuje všechny funkce prostřednictvím jednoduchého HTML webového rozhraní.

### I2Pmail / Susimail

*Vyvinuto: postman, susi23, mastiejaner*

I2Pmail je spíše služba než aplikace — postman nabízí jak interní, tak externí e-mail s POP3 a SMTP službou prostřednictvím I2PTunnel instancí přistupujících k sérii komponent vyvinutých s mastiejanerem, což umožňuje lidem používat jejich preferované e-mailové klienty pro pseudonymní odesílání a přijímání pošty. Avšak jelikož většina e-mailových klientů odhaluje podstatné identifikační informace, I2P obsahuje webový susimail klient od susi23, který byl vytvořen speciálně s ohledem na anonymitní potřeby I2P. Služba I2Pmail/mail.i2p nabízí transparentní filtrování virů i prevenci denial of service útoků s hashcash rozšířenými kvótami. Kromě toho má každý uživatel kontrolu nad svou strategií dávkování před doručením prostřednictvím mail.i2p outproxies, které jsou oddělené od mail.i2p SMTP a POP3 serverů — jak outproxies, tak inproxies komunikují s mail.i2p SMTP a POP3 servery přímo prostřednictvím I2P, takže kompromitování těchto neanonymních míst neposkytuje přístup k e-mailovým účtům nebo vzorcům aktivit uživatele.
