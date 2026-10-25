---
title: "I2P: Škálovatelný framework pro anonymní komunikaci"
description: "Úvod do architektury a fungování I2P"
slug: "intro"
aliases:
  - "/cs/intro"
  - "/cs/intro/"
  - "/cs/how_intro"
  - "/cs/how_intro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

POZNÁMKA: Tento dokument původně napsal jrandom v roce 2003. I když se snažíme ho udržovat aktuální, některé informace mohou být zastaralé nebo neúplné. Sekce o transportu a kryptografii jsou aktuální k lednu 2025.

## Úvod

I2P je škálovatelná, samoorganizující se, odolná anonymní síťová vrstva s přepínáním paketů, na které může fungovat libovolný počet různých aplikací zaměřených na anonymitu nebo bezpečnost. Každá z těchto aplikací si může vytvořit vlastní kompromisy mezi anonymitou, latencí a propustností, aniž by se musela starat o správnou implementaci mixnet se svobodným směřováním, což jim umožňuje sloučit svou aktivitu s větším souborem anonymních uživatelů již běžících na I2P.

Dostupné aplikace již poskytují plný rozsah typických internetových aktivit — **anonymní** procházení webu, webhosting, chat, sdílení souborů, e-mail, blogování a syndikace obsahu, stejně jako několik dalších aplikací ve vývoji.

- Prohlížení webu: použití jakéhokoli existujícího prohlížeče, který podporuje použití proxy.
- Chat: IRC a další protokoly
- Sdílení souborů: [I2PSnark](#i2psnark) a další aplikace
- E-mail: [susimail](#i2pmail--susimail) a další aplikace
- Blog: použití jakéhokoli lokálního webového serveru nebo dostupných pluginů

Na rozdíl od webových stránek hostovaných v sítích pro distribuci obsahu jako [Freenet](#freenet) nebo [GNUnet](https://www.gnunet.org/en/), jsou služby hostované na I2P plně interaktivní — najdete zde tradiční vyhledávače ve stylu webu, diskusní fóra, blogy, na které můžete komentovat, stránky řízené databázemi a mosty pro dotazování statických systémů jako Freenet, aniž byste si je museli instalovat lokálně.

Se všemi těmito aplikacemi s povolenou anonymitou převezme I2P roli middlewaru orientovaného na zprávy — aplikace řeknou, že chtějí odeslat nějaká data na kryptografický identifikátor („destination") a I2P se postará o to, aby se tam dostaly bezpečně a anonymně. I2P také obsahuje jednoduchou [streaming](#streaming-library) knihovnu, která umožňuje, aby se anonymní best-effort zprávy I2P přenášely jako spolehlivé, uspořádané streamy, transparentně nabízející algoritmus řízení přetížení založený na TCP, který je vyladěn pro vysoký bandwidth delay product sítě. Ačkoli bylo k dispozici několik jednoduchých SOCKS proxy pro připojení stávajících aplikací do sítě, jejich hodnota byla omezená, protože téměř každá aplikace rutinně odhaluje to, co je v anonymním kontextu citlivou informací. Jediný bezpečný způsob je kompletně auditovat aplikaci, aby se zajistil správný provoz, a k tomu poskytujeme sérii API v různých jazycích, které lze použít k maximálnímu využití sítě.

I2P není výzkumný projekt — akademický, komerční nebo vládní — ale místo toho je to technické úsilí zaměřené na to, aby se udělalo cokoli nutného k poskytnutí dostatečné úrovně anonymity těm, kdo ji potřebují. Je v aktivním vývoji od začátku roku 2003 s jedním vývojářem na plný úvazek a oddanou skupinou přispěvatelů na částečný úvazek z celého světa. Veškerá práce na I2P je open source a volně dostupná na [webových stránkách](/), přičemž většina kódu je uvolněna přímo do veřejné domény, i když využívá několik kryptografických rutin pod BSD-style licencemi. Lidé pracující na I2P nekontrolují, pod čím lidé uvolňují klientské aplikace, a je dostupných několik aplikací pod GPL ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex a další). Financování I2P pochází výhradně z darů a v současné době neobdrží žádné daňové úlevy v žádné jurisdikci, protože mnoho vývojářů je samo anonymních.

---

## Provoz

### Přehled

Pro pochopení fungování I2P je nezbytné porozumět několika klíčovým konceptům. Zaprvé, I2P striktně odděluje software účastnící se sítě ("router") a anonymní koncové body ("destinace") spojené s jednotlivými aplikacemi. Skutečnost, že někdo provozuje I2P, obvykle není tajemství. Co je skryto, jsou informace o tom, co uživatel dělá, pokud vůbec něco, stejně jako o tom, ke kterému router je konkrétní destinace připojena. Koncoví uživatelé budou typicky mít na svém router několik místních destinací — například jednu pro proxy připojení k IRC serverům, další podporující uživatelův anonymní webserver ("I2P Site"), další pro instanci I2Phex, další pro torrenty atd.

Dalším klíčovým konceptem k pochopení je "tunnel". Tunnel je směrovaná cesta skrz explicitně vybraný seznam routerů. Používá se vrstvené šifrování, takže každý z routerů může dešifrovat pouze jednu vrstvu. Dešifrovaná informace obsahuje IP dalšího routeru spolu se šifrovanou informací, která má být předána dál. Každý tunnel má počáteční bod (první router, také známý jako "gateway") a koncový bod. Zprávy mohou být posílány pouze jedním směrem. Pro posílání zpráv zpět je vyžadován další tunnel.

![Inbound and outbound tunnel schematic](/images/tunnels.svg) *Obrázek 1: Existují dva typy tunnelů: příchozí a odchozí.*

Existují dva typy tunnelů: **"odchozí" tunnely** posílají zprávy pryč od tvůrce tunnelu, zatímco **"příchozí" tunnely** přinášejí zprávy k tvůrci tunnelu. Kombinací těchto dvou tunnelů mohou uživatelé posílat zprávy jeden druhému. Odesílatel ("Alice" na obrázku výše) nastaví odchozí tunnel, zatímco příjemce ("Bob" na obrázku výše) vytvoří příchozí tunnel. Gateway příchozího tunnelu může přijímat zprávy od jakéhokoli jiného uživatele a bude je posílat dál až k koncovému bodu ("Bob"). Koncový bod odchozího tunnelu bude muset poslat zprávu dál na gateway příchozího tunnelu. K tomu odesílatel ("Alice") přidá instrukce do své šifrované zprávy. Jakmile koncový bod odchozího tunnelu zprávu dešifruje, bude mít instrukce k přeposlání zprávy na správný příchozí gateway (gateway k "Bobovi").

Třetím klíčovým konceptem, který je třeba pochopit, je I2P **"network database"** (neboli "netDb") — pár algoritmů používaných ke sdílení síťových metadat. Dva typy přenášených metadat jsou **"routerInfo"** a **"leaseSets"** — routerInfo poskytuje routerům data potřebná pro kontaktování konkrétního routeru (jejich veřejné klíče, transportní adresy, atd.), zatímco leaseSet poskytuje routerům informace potřebné pro kontaktování konkrétní destinace. LeaseSet obsahuje několik "leases" (pronájmů). Každý z těchto pronájmů specifikuje tunnel gateway, který umožňuje dosažení konkrétní destinace. Úplné informace obsažené v pronájmu:

- Vstupní brána pro tunnel, která umožňuje dosáhnout konkrétního cíle.
- Čas, kdy tunnel vyprší.
- Pár veřejných klíčů pro možnost šifrování zpráv (pro odeslání přes tunnel a dosažení cíle).

Routery samy posílají své routerInfo přímo do netDb, zatímco leaseSety jsou odesílány přes odchozí tunnely (leaseSety musí být odesílány anonymně, aby se zabránilo korelaci routeru s jeho leaseSety).

Výše uvedené koncepty můžeme kombinovat k vytvoření úspěšných spojení v síti.

Pro vybudování svých vlastních příchozích a odchozích tunelů provede Alice vyhledávání v netDb za účelem shromáždění routerInfo. Tímto způsobem získává seznamy peerů, které může použít jako přeskoky ve svých tunelech. Poté může poslat zprávu o vybudování prvnímu přeskoku, požádat o konstrukci tunelu a požádat tento router, aby předal zprávu o konstrukci dále, dokud nebude tunel vybudován.

![Vyžádat informace o ostatních routerech](/images/netdb_get_routerinfo_1.svg)

![Build tunnel using router information](/images/netdb_get_routerinfo_2.svg) *Obrázek 2: Informace o routeru se používají k budování tunelů.*

Když Alice chce poslat zprávu Bobovi, nejprve vyhledá v netDb Bobův leaseSet, což jí poskytne jeho aktuální brány příchozích tunelů. Poté vybere jeden ze svých odchozích tunelů a pošle zprávu dolů s pokyny pro koncový bod odchozího tunelu, aby přeposlal zprávu na jednu z bran Bobových příchozích tunelů. Když koncový bod odchozího tunelu obdrží tyto pokyny, přepošle zprávu podle požadavku, a když ji obdrží brána Bobova příchozího tunelu, je přeposlána dolů tunelem k Bobovu routeru. Pokud chce Alice, aby jí Bob mohl na zprávu odpovědět, musí explicitně přenést svou vlastní destinaci jako součást samotné zprávy. To lze provést zavedením vyšší úrovně, což se děje v knihovně [streaming](#streaming-library). Alice také může zkrátit dobu odpovědi tím, že přiloží svůj nejnovější leaseSet ke zprávě, takže Bob nemusí provádět vyhledávání v netDb, když chce odpovědět, ale to je volitelné.

![Connect tunnels using LeaseSets](/images/netdb_get_leaseset.svg) *Obrázek 3: LeaseSets se používají k propojení odchozích a příchozích tunelů.*

Zatímco samotné tunnely mají vrstvené šifrování pro zabránění neoprávněnému odhalení peerům uvnitř sítě (stejně jako transportní vrstva sama brání neoprávněnému odhalení peerům mimo síť), je nutné přidat další end-to-end vrstvu šifrování pro skrytí zprávy před koncovým bodem odchozího tunnelu a bránou příchozího tunnelu. Toto "[garlic encryption](#garlic-messages)" umožňuje Alicinu routeru zabalit více zpráv do jediné "garlic message", šifrované na konkrétní veřejný klíč tak, aby prostředníci nemohli určit ani kolik zpráv je v garlic obsaženo, co tyto zprávy říkají, nebo kam jsou jednotlivé cloves určeny. Pro typickou end-to-end komunikaci mezi Alice a Bobem bude garlic šifrován na veřejný klíč publikovaný v Bobově leaseSet, což umožní zašifrovat zprávu bez vyzrazení veřejného klíče Bobovu vlastnímu routeru.

Dalším důležitým faktem, který je třeba mít na paměti, je, že I2P je zcela založeno na zprávách a některé zprávy se mohou cestou ztratit. Aplikace používající I2P mohou využít rozhraní orientovaná na zprávy a postarat se o vlastní řízení zahlcení a požadavky na spolehlivost, ale většina z nich by byla nejlépe obsluhována opětovným použitím poskytnuté knihovny [streaming](#streaming-library), aby mohly na I2P pohlížet jako na síť založenou na proudech.

---

### Tunnels

Vstupní i výstupní tunnely fungují podle podobných principů. Gateway tunnelu shromažďuje určitý počet zpráv tunnelu a nakonec je předzpracuje do něčeho vhodného pro doručení tunelem. Dále gateway tato předzpracovaná data zašifruje a předá je prvnímu uzlu. Tento uzel a následující účastníci tunnelu přidají vrstvu šifrování poté, co ověří, že se nejedná o duplikát, před předáním dalšímu uzlu. Nakonec zpráva dorazí do koncového bodu, kde jsou zprávy opět rozděleny a předány dále podle požadavku. Rozdíl spočívá v tom, co dělá tvůrce tunnelu — u vstupních tunnelů je tvůrce koncovým bodem a jednoduše dešifruje všechny přidané vrstvy, zatímco u výstupních tunnelů je tvůrce gateway a předem dešifruje všechny vrstvy tak, aby po přidání všech vrstev šifrování po jednotlivých uzlech zpráva dorazila v otevřené podobě do koncového bodu tunnelu.

Výběr konkrétních peers pro předávání zpráv a jejich konkrétní pořadí je důležité pro pochopení charakteristik anonymity i výkonu I2P. Zatímco network database (netDb) (níže) má svá vlastní kritéria pro výběr peers, které má dotazovat a na kterých má ukládat záznamy, tvůrci tunnelů mohou použít jakékoliv peers v síti v jakémkoliv pořadí (a dokonce i vícekrát) v jediném tunnelu. Pokud by byly dokonalé údaje o latenci a kapacitě globálně známé, výběr a pořadí by byly řízeny konkrétními potřebami klienta v souladu s jejich modelem hrozeb. Bohužel, údaje o latenci a kapacitě není triviální shromažďovat anonymně, a spoléhání se na nedůvěryhodné peers pro poskytování těchto informací má své vlastní vážné důsledky pro anonymitu.

Z pohledu anonymity by nejjednodušší technikou bylo náhodně vybrat uzly z celé sítě, náhodně je seřadit a používat tyto uzly v tomto pořadí navěky. Z pohledu výkonu by nejjednodušší technikou bylo vybrat nejrychlejší uzly s potřebnou volnou kapacitou, rozložit zátěž mezi různé uzly pro transparentní převzetí při selhání a znovu postavit tunel vždy, když se změní informace o kapacitě. Zatímco první přístup je křehký i neefektivní, druhý vyžaduje nedostupné informace a nabízí nedostatečnou anonymitu. I2P místo toho pracuje na nabízení řady strategií pro výběr uzlů spolu s měřícím kódem orientovaným na anonymitu pro organizaci uzlů podle jejich profilů.

Jako základ I2P neustále profiluje protějšky, se kterými interaguje, měřením jejich nepřímého chování — například když protějšek odpoví na netDb vyhledávání za 1,3 sekundy, tato latence round trip je zaznamenána v profilech všech routerů zapojených do obou tunelů (příchozího a odchozího), kterými prošla žádost a odpověď, stejně jako v profilu dotazovaného protějška. Přímé měření, jako je latence transportní vrstvy nebo přetížení, se nepoužívá jako součást profilu, protože může být manipulováno a spojeno s měřícím routerem, což je vystavuje triviálním útokům. Během shromažďování těchto profilů se pro každý spouští série výpočtů, které sumarizují jeho výkon — jeho latenci, kapacitu zvládat mnoho aktivit, zda jsou v současnosti přetížené, a jak dobře se zdají být integrovány do sítě. Tyto výpočty jsou pak porovnány pro aktivní protějšky, aby se routery uspořádaly do čtyř úrovní — rychlé a vysokokapacitní, vysokokapacitní, neselházající a selházající. Prahové hodnoty pro tyto úrovně jsou určovány dynamicky, a zatímco v současnosti používají poměrně jednoduché algoritmy, existují alternativy.

Pomocí těchto dat profilu je nejjednodušší rozumnou strategií výběru peerů náhodný výběr peerů z nejvyšší úrovně (rychlí a s vysokou kapacitou), což je v současnosti nasazeno pro klientské tunnely. Průzkumné tunnely (používané pro netDb a správu tunnelů) vybírají peery náhodně z úrovně "neselhaných" (která zahrnuje i routery z "lepších" úrovní), což umožňuje peeru vzorkovat routery šířeji, ve skutečnosti optimalizuje výběr peerů prostřednictvím randomizovaného [hill climbingu](https://en.wikipedia.org/wiki/Hill_climbing). Tyto strategie však umožňují únik informací týkajících se peerů v nejvyšší úrovni routeru prostřednictvím útoků predecessor a netDb harvesting. Na oplátku existuje několik alternativ, které sice nevyvážují zátěž tak rovnoměrně, ale řeší útoky prováděné konkrétními třídami protivníků.

Výběrem náhodného klíče a uspořádáním peerů podle jejich XOR vzdálenosti od něj se sníží množství uniklých informací při predecessor a harvesting útocích v závislosti na míře selhání peerů a obměně úrovně. Další jednoduchou strategií pro řešení netDb harvesting útoků je jednoduše fixovat příchozí tunnel gateway(s) a zároveň randomizovat peery dále v tunnelech. Pro řešení predecessor útoků ze strany protivníků, které klient kontaktuje, by také zůstaly fixované koncové body odchozích tunnelů. Výběr kterého peera fixovat na nejexponovanějším místě by samozřejmě musel mít časové omezení, protože všechny peery nakonec selžou, takže by to mohlo být buď reaktivně upraveno nebo proaktivně předcházeno tak, aby to napodobovalo naměřený průměrný čas mezi selháními ostatních routerů. Tyto dvě strategie lze následně kombinovat, použitím fixovaného exponovaného peera a XOR založeného uspořádání v rámci samotných tunnelů. Rigoróznější strategie by fixovala přesné peery a uspořádání potenciálního tunnelu, používajíc jednotlivé peery pouze pokud všichni souhlasí s účastí stejným způsobem pokaždé. To se liší od XOR založeného uspořádání v tom, že predecessor a successor každého peera je vždy stejný, zatímco XOR pouze zajišťuje, že se jejich pořadí nemění.

Jak bylo zmíněno dříve, I2P v současnosti (verze 0.8) zahrnuje výše uvedenou vícevrstvou náhodnou strategii s řazením založeným na XOR. Podrobnější diskuze o mechanismech zapojených do provozu tunelů, jejich správy a výběru peerů lze nalézt ve [specifikaci tunelů](/docs/specs/tunnel-implementation/).

---

### Network Database (netDb)

Jak bylo zmíněno dříve, I2P netDb funguje pro sdílení metadat sítě. Toto je podrobně popsáno na stránce [network database](/docs/specs/common-structures/), ale základní vysvětlení je k dispozici níže.

Všechny I2P routery obsahují lokální netDb, ale ne všechny routery se účastní DHT nebo odpovídají na vyhledávání leaseSet. Routery, které se účastní DHT a odpovídají na vyhledávání leaseSet, se nazývají 'floodfill'. Routery mohou být ručně nakonfigurovány jako floodfill, nebo se automaticky stanou floodfill, pokud mají dostatečnou kapacitu a splňují další kritéria pro spolehlivý provoz.

Ostatní I2P routery budou ukládat svá data a vyhledávat data zasíláním jednoduchých dotazů 'store' a 'lookup' do floodfill routerů. Pokud floodfill router obdrží dotaz 'store', rozšíří informace do ostatních floodfill routerů pomocí [Kademlia algoritmu](http://en.wikipedia.org/wiki/Kademlia). Dotazy 'lookup' v současnosti fungují jinak, aby se předešlo důležitému bezpečnostnímu problému. Když se provádí vyhledávání, floodfill router nepředá vyhledávání jiným uzlům, ale vždy odpoví sám (pokud má požadovaná data).

V síťové databázi jsou uloženy dva typy informací.

- **RouterInfo** ukládá informace o konkrétním I2P router a jak ho kontaktovat
- **LeaseSet** ukládá informace o konkrétní destinaci (např. I2P webová stránka, e-mailový server...)

Všechny tyto informace jsou podepsány publikující stranou a ověřeny jakýmkoliv I2P router, který informace používá nebo ukládá. Navíc data obsahují časové informace, aby se zabránilo ukládání starých záznamů a možným útokům. To je také důvod, proč I2P obsahuje nezbytný kód pro udržování správného času, občasně dotazuje některé SNTP servery (standardně [pool.ntp.org](http://www.pool.ntp.org/) round robin) a detekuje časový posun mezi router na transportní vrstvě.

Některé další poznámky jsou také důležité.

- **Nepublikované a šifrované leaseSety:**
  Někdo může chtít, aby se k destinaci dostali pouze konkrétní lidé. To je možné tím, že se destinace nepublikuje v netDb. Destinaci však budete muset přenést jinými prostředky. Toto je podporováno 'šifrovanými leaseSety'. Tyto leaseSety mohou dekódovat pouze lidé s přístupem k dešifrovacímu klíči.

- **Bootstrapping:**
  Bootstrapping netDb je poměrně jednoduché. Jakmile se router podaří získat jediný routerInfo dostupného peera, může dotazovat tento router na odkazy na další routery v síti. V současnosti řada uživatelů zveřejňuje své routerInfo soubory na webových stránkách, aby tyto informace zpřístupnili. I2P se automaticky připojí k jedné z těchto webových stránek, aby shromáždil routerInfo soubory a provedl bootstrap. I2P nazývá tento bootstrap proces "reseeding".

- **Škálovatelnost vyhledávání:**
  Vyhledávání v síti I2P je iterativní, nikoli rekurzivní. Pokud vyhledávání z floodfill selže, vyhledávání bude opakováno na další nejbližší floodfill. floodfill rekurzivně nepožádá jiný floodfill o data. Iterativní vyhledávání je škálovatelné pro velké DHT sítě.

---

### Transportní protokoly

Komunikace mezi routery musí poskytovat důvěrnost a integritu proti vnějším protivníkům a zároveň ověřovat, že kontaktovaný router je ten, který by měl danou zprávu obdržet. Podrobnosti o tom, jak routery komunikují s jinými routery, nejsou kritické — v různých obdobích byly použity tři samostatné protokoly k poskytnutí těchto základních potřeb.

I2P v současnosti podporuje dva transportní protokoly, [NTCP2](/docs/specs/ntcp2/) přes TCP a [SSU2](/docs/specs/ssu2/) přes UDP. Tyto nahradily předchozí verze protokolů, [NTCP](/docs/legacy/ssu/) a [SSU](/docs/legacy/ssu/), které jsou nyní zastaralé. Oba protokoly podporují IPv4 i IPv6. Díky podpoře transportů TCP i UDP může I2P efektivně procházet většinou firewallů, včetně těch určených k blokování provozu v restriktivních cenzoních režimech. NTCP2 a SSU2 byly navrženy tak, aby používaly moderní šifrovací standardy, zlepšily odolnost proti identifikaci provozu, zvýšily efektivitu a bezpečnost a učinily traversal NATu robustnější. Routery publikují každý podporovaný transport a IP adresu v síťové databázi. Routery s přístupem k veřejným IPv4 a IPv6 sítím obvykle publikují čtyři adresy, jednu pro každou kombinaci NTCP2/SSU2 s IPv4/IPv6.

[SSU2](/docs/specs/ssu2/) podporuje a rozšiřuje cíle SSU. SSU2 má mnoho podobností s jinými moderními protokoly založenými na UDP, jako jsou Wireguard a QUIC. Kromě spolehlivého přenosu síťových zpráv přes UDP poskytuje SSU2 specializované nástroje pro peer-to-peer, kooperativní detekci IP adresy, detekci firewallu a NAT traversal. Jak je popsáno ve [specifikaci SSU](/docs/legacy/ssu/):

> Cílem tohoto protokolu je poskytovat bezpečné, autentizované, polospolehlivé a neuspořádané doručování zpráv, přičemž odhaluje pouze minimální množství dat snadno rozpoznatelných třetími stranami. Měl by podporovat vysokostupňovou komunikaci stejně jako TCP-přátelské řízení zahlcení a může zahrnovat detekci PMTU. Měl by být schopen efektivně přesouvat hromadná data rychlostmi dostatečnými pro domácí uživatele. Kromě toho by měl podporovat techniky pro řešení síťových překážek, jako je většina NAT nebo firewallů.

[NTCP2](/docs/specs/ntcp2/) podporuje a rozšiřuje cíle NTCP. Poskytuje efektivní a plně šifrovaný přenos síťových zpráv přes TCP a odolnost proti identifikaci provozu pomocí moderních šifrovacích standardů.

I2P podporuje současně více transportů. Konkrétní transport pro odchozí spojení je vybrán pomocí "nabídek". Každý transport nabízí pro spojení a relativní hodnota těchto nabídek určuje prioritu. Transporty mohou odpovědět různými nabídkami v závislosti na tom, zda již existuje navázané spojení s protějškem.

Hodnoty nabídky (priority) jsou závislé na implementaci a mohou se lišit na základě podmínek provozu, počtu připojení a dalších faktorů. Routery také publikují své transportní preference pro příchozí spojení v síťové databázi jako transportní "náklady" pro každý transport a adresu.

---

### Kryptografie

I2P používá kryptografii na několika protokolových vrstvách pro šifrování, autentifikaci a ověřování. Hlavní protokolové vrstvy jsou: transporty, zprávy pro budování tunnel, šifrování tunnel vrstvy, zprávy síťové databáze netDb a end-to-end (garlic) zprávy. Původní návrh I2P používal malou sadu kryptografických primitiv, které byly v té době považovány za bezpečné. Patřily mezi ně ElGamal asymetrické šifrování, DSA-SHA1 podpisy, AES256/CBC symetrické šifrování a SHA-256 hashe. S rostoucím dostupným výpočetním výkonem a podstatným vývojem kryptografického výzkumu během let bylo potřeba, aby I2P upgradovala své primitivy a protokoly. Proto jsme přidali koncept "typů šifrování" a "typů podpisů" a rozšířili naše protokoly o tyto identifikátory a indikaci podpory. To nám umožňuje pravidelně aktualizovat a rozšiřovat síťovou podporu pro moderní kryptografii a připravit síť na nová primitiva do budoucna, aniž bychom porušili zpětnou kompatibilitu nebo vyžadovali "flag day" pro síťové aktualizace. Některé typy podpisů a šifrování jsou také rezervovány pro experimentální použití.

Současné primitiva používané ve většině vrstev protokolu jsou X25519 výměna klíčů, EdDSA podpisy, ChaCha20/Poly1305 autentizované symetrické šifrování a SHA-256 hashe. AES256 se stále používá pro šifrování tunnel vrstvy. Tyto moderní protokoly se používají pro naprostou většinu síťové komunikace. Starší primitiva včetně ElGamal, ECDSA a DSA-SHA1 jsou nadále podporována většinou implementací kvůli zpětné kompatibilitě při komunikaci se staršími routery. Některé staré protokoly byly označeny za zastaralé a/nebo kompletně odstraněny. V blízké budoucnosti začneme výzkum migrace na post-kvantové (PQ) nebo hybridní-PQ šifrování a podpisy k udržení našich robustních bezpečnostních standardů.

Tyto kryptografické primitiva jsou kombinována dohromady, aby poskytly vrstvené obrany I2P proti různým protivníkům. Na nejnižší úrovni je komunikace mezi routery chráněna zabezpečením transportní vrstvy. [Tunnel](#tunnels) zprávy předávané přes transporty mají své vlastní vrstvené šifrování. Různé další zprávy jsou předávány uvnitř "garlic messages", které jsou také šifrované.

#### Garlic Messages

Garlic zprávy jsou rozšířením "cibulovitého" vrstvového šifrování, které umožňuje, aby obsah jedné zprávy obsahoval více "hřebíčků" — plně vytvořené zprávy společně s jejich vlastními instrukcemi pro doručení. Zprávy jsou zabaleny do garlic zprávy vždy, když by zpráva jinak procházela v otevřeném textu přes uzel, který by neměl mít přístup k informacím — například když router chce požádat jiný router o účast v tunelu, zabalí požadavek do garlic, zašifruje tento garlic veřejným klíčem přijímajícího routeru a přepošle jej tunelem. Dalším příkladem je, když klient chce odeslat zprávu na cíl — router odesílatele zabalí tuto datovou zprávu (spolu s některými dalšími zprávami) do garlic, zašifruje tento garlic veřejným klíčem publikovaným v leaseSet příjemce a přepošle jej příslušnými tunely.

"Instrukce" připojené ke každému clove uvnitř šifrovací vrstvy zahrnují možnost požádat o místní přeposlání clove, na vzdálený router, nebo na vzdálený tunnel na vzdáleném routeru. V těchto instrukcích jsou pole umožňující peeru požádat o odložení doručení do určitého času nebo dokud není splněna určitá podmínka, ačkoli nebudou respektovány dokud nebudou nasazena [netriviální zpoždění](#variable-latency). Je možné explicitně směrovat garlic zprávy libovolný počet hopů bez budování tunnelů, nebo dokonce přesměrovávat zprávy tunnelu jejich zabalením do garlic zpráv a přeposíláním několik hopů před jejich doručením na další hop v tunnelu, ale tyto techniky nejsou v současné implementaci používány.

#### Značky relace

Jako nespolehlivý, neuspořádaný systém založený na zprávách používá I2P jednoduchou kombinaci asymetrických a symetrických šifrovacích algoritmů k zajištění důvěrnosti a integrity dat u garlic zpráv. Původní kombinace byla označována jako ElGamal/AES+SessionTags, ale to je přílišně podrobný způsob popisu jednoduchého použití 2048bitového ElGamal, AES256, SHA256 a 32bajtových nonce. Ačkoli je tento protokol stále podporován, většina sítě migrovala na nový protokol ECIES-X25519-AEAD-Ratchet. Tento protokol kombinuje X25519, ChaCha20/Poly1305 a synchronizovaný PRNG pro generování 32bajtových nonce. Oba protokoly budou níže stručně popsány.

#### ElGamal/AES+SessionTags

Když chce router poprvé zašifrovat garlic zprávu pro jiný router, zašifruje klíčový materiál pro AES256 session klíč pomocí ElGamal a připojí AES256/CBC zašifrovaný payload za tento zašifrovaný ElGamal blok. Kromě zašifrovaného payload obsahuje AES zašifrovaná sekce délku payload, SHA256 hash nezašifrovaného payload a také řadu "session tags" — náhodných 32-bajtových nonces. Až příště chce odesílatel zašifrovat garlic zprávu pro jiný router, místo ElGamal šifrování nového session klíče jednoduše vybere jeden z předchozích doručených session tags a AES zašifruje payload jako předtím, použitím session klíče použitého s daným session tag, s předponou samotného session tag. Když router obdrží garlic zašifrovanou zprávu, zkontroluje prvních 32 bajtů, zda se shodují s dostupným session tag — pokud ano, jednoduše AES dešifruje zprávu, ale pokud ne, ElGamal dešifruje první blok.

Každý session tag může být použit pouze jednou, aby se zabránilo interním protivníkům v zbytečném korelování různých zpráv jako pocházejících od stejných routerů. Odesílatel ElGamal/AES+SessionTag šifrované zprávy si vybírá, kdy a kolik tagů doručit, a předem zásobuje příjemce dostatečným množstvím tagů pro pokrytí salvy zpráv. Garlic zprávy mohou detekovat úspěšné doručení tagů zabalením malé dodatečné zprávy jako clove ("delivery status message") — když garlic zpráva dorazí k zamýšlenému příjemci a je úspěšně dešifrována, tato malá delivery status zpráva je jedním z odhalených cloves a obsahuje instrukce pro příjemce k odeslání clove zpět původnímu odesílateli (samozřejmě přes inbound tunnel). Když původní odesílatel obdrží tuto delivery status zprávu, ví, že session tagy zabalené v garlic zprávě byly úspěšně doručeny.

Session tagy mají samy o sobě velmi krátkou životnost, po které jsou zahozeny, pokud nejsou použity. Kromě toho je množství uložené pro každý klíč omezené, stejně jako počet samotných klíčů — pokud jich přijde příliš mnoho, mohou být zahozeny buď nové nebo staré zprávy. Odesílatel sleduje, zda zprávy používající session tagy procházejí, a pokud není dostatečná komunikace, může zahodit ty, které předtím považoval za správně doručené, a vrátit se zpět k plnému nákladnému ElGamal šifrování.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags vyžadovaly značnou režii v několika ohledech. Využití CPU bylo vysoké, protože ElGamal je poměrně pomalý. Šířka pásma byla nadměrná kvůli nutnosti doručovat velké množství session tagů předem a protože veřejné klíče ElGamal jsou velmi velké. Využití paměti bylo vysoké kvůli požadavku ukládat velké množství session tagů. Spolehlivost byla narušena ztrátou doručování session tagů.

ECIES-X25519-AEAD-Ratchet byl navržen k řešení těchto problémů. X25519 se používá pro výměnu klíčů. ChaCha20/Poly1305 se používá pro autentifikované symetrické šifrování. Šifrovací klíče jsou "dvojitě ratchetovány" nebo pravidelně rotovány. Session tagy jsou zmenšeny z 32 bajtů na 8 bajtů a jsou generovány pomocí PRNG. Protokol má mnoho podobností s Signal protokolem používaným v aplikacích Signal a WhatsApp. Tento protokol poskytuje podstatně nižší režii v CPU, RAM a šířce pásma.

Session tagy jsou generovány z deterministického synchronizovaného PRNG běžícího na obou koncích relace pro generování session tagů a session klíčů. PRNG je HKDF používající SHA-256 HMAC a je inicializován z výsledku X25519 DH. Session tagy nejsou nikdy předem přenášeny; jsou zahrnuty pouze se zprávou. Příjemce ukládá omezený počet session klíčů indexovaných podle session tagu. Odesílatel nepotřebuje ukládat žádné session tagy ani klíče, protože nejsou odesílány předem; mohou být generovány na vyžádání. Udržováním tohoto PRNG přibližně synchronizovaného mezi odesílatelem a příjemcem (příjemce předpočítává okno dalších např. 50 tagů) je odstraněna režie periodického sdružování velkého počtu tagů.

---

## Budoucnost

Protokoly I2P jsou efektivní na většině platforem, včetně mobilních telefonů, a jsou bezpečné pro většinu modelů hrozeb. Nicméně existuje několik oblastí, které vyžadují další zlepšení, aby vyhovovaly potřebám těch, kteří čelí mocným státem sponzorovaným protivníkům, a aby čelily hrozbám pokračujícího kryptografického pokroku a stále se zvyšující výpočetní síly. Dvě možné funkce, omezené trasy a proměnná latence, byly navrženy jrandomem v roce 2003. Ačkoli již neplánujeme implementaci těchto funkcí, jsou popsány níže.

### Provoz s omezenou trasou

I2P je překryvná síť navržená pro provoz na funkční síti s přepínáním paketů, která využívá princip end-to-end pro zajištění anonymity a bezpečnosti. Ačkoli internet již plně nepřijímá princip end-to-end (kvůli použití NAT), I2P vyžaduje, aby podstatná část sítě byla dosažitelná — může existovat řada uzlů na okrajích běžících s omezenými trasami, ale I2P neobsahuje vhodný algoritmus směrování pro degenerovaný případ, kdy je většina uzlů nedosažitelná. Fungovalo by však na síti využívající takový algoritmus.

Omezený provoz routingu, kde existují limity pro to, které uzly jsou přímo dostupné, má několik různých funkčních a anonymitních důsledků v závislosti na tom, jak jsou omezené trasy zpracovávány. Na nejzákladnější úrovni existují omezené trasy, když se uzel nachází za NAT nebo firewallem, který neumožňuje příchozí spojení. To bylo do značné míry vyřešeno integrací distribuovaného hole punching do transportní vrstvy, což umožňuje lidem za většinou NAT a firewallů přijímat nevyžádaná spojení bez jakékoliv konfigurace. To však neomezuje vystavení IP adresy uzlu routerům uvnitř sítě, protože se s uzlem mohou jednoduše seznámit prostřednictvím publikovaného introducera.

Kromě funkčního zpracování omezených tras existují dvě úrovně omezeného provozu, které lze použít k omezení odhalení vlastní IP adresy — použití router-specifických tunelů pro komunikaci a nabízení 'klientských routerů'. V prvním případě mohou routery buď vytvořit nový fond tunelů nebo znovu použít svůj explorační fond, přičemž publikují vstupní brány některých z nich jako součást svých routerInfo místo svých transportních adres. Když se s nimi chce peer spojit, uvidí tyto tunnel brány v netDb a jednoduše jim pošle příslušnou zprávu přes jeden z publikovaných tunelů. Pokud chce peer za omezenou trasou odpovědět, může tak učinit buď přímo (pokud je ochoten odhalit svou IP peeru) nebo nepřímo přes své odchozí tunely. Když se routery, ke kterým má peer přímé spojení, chtějí k němu dostat (například pro přeposílání tunnel zpráv), jednoduše upřednostní své přímé spojení před publikovanou tunnel bránou. Koncept 'klientských routerů' jednoduše rozšiřuje omezenou trasu tím, že nepublikuje žádné router adresy. Takový router by ani nemusel publikovat své routerInfo v netDb, pouze poskytovat své self signed routerInfo peerům, které kontaktuje (nutné pro předání veřejných klíčů routeru).

Existují kompromisy pro ty, kteří jsou za omezenými trasami, protože by se pravděpodobně méně často podíleli na tunnelech jiných lidí a routery, ke kterým jsou připojeni, by mohly odvodit vzorce provozu, které by jinak nebyly odhaleny. Na druhou stranu, pokud jsou náklady na toto odhalení nižší než náklady na zpřístupnění IP adresy, může to být smysluplné. To samozřejmě předpokládá, že peers, se kterými router za omezenou trasou komunikuje, nejsou nepřátelští — buď je síť dostatečně velká, že pravděpodobnost použití nepřátelského peera pro připojení je dostatečně malá, nebo se místo toho používají důvěryhodní (a možná dočasní) peers.

Omezené trasy jsou složité a celkový cíl byl do značné míry opuštěn. Několik souvisejících vylepšení výrazně snížilo jejich potřebu. Nyní podporujeme UPnP pro automatické otevírání portů firewallu. Podporujeme jak IPv4, tak IPv6. SSU2 vylepšil detekci adres, určování stavu firewallu a kooperativní NAT hole punching. SSU2, NTCP2 a kontroly kompatibility adres zajišťují, že se tunnel skoky mohou připojit před vybudováním tunelu. GeoIP a identifikace zemí nám umožňují vyhnout se peerům v zemích s restriktivními firewally. Podpora pro "skryté" routery za těmito firewally se zlepšila. Některé implementace také podporují připojení k peerům na overlay sítích, jako je Yggdrasil.

### Proměnná latence

I když se většina počátečních úsilí I2P zaměřila na komunikaci s nízkou latencí, od začátku byla navržena s ohledem na služby s variabilní latencí. Na nejzákladnější úrovni mohou aplikace běžící na I2P nabídnout anonymitu komunikace se střední a vysokou latencí, zatímco stále směšují své vzory provozu s provozem s nízkou latencí. Interně však může I2P nabídnout svou vlastní komunikaci se střední a vysokou latencí prostřednictvím garlic encryption — specifikováním, že zpráva má být odeslána po určitém zpoždění, v určitém čase, po průchodu určitého počtu zpráv nebo prostřednictvím jiné mix strategie. Díky vrstvenému šifrování by pouze router, kterému clove odhalil požadavek na zpoždění, věděl, že zpráva vyžaduje vysokou latenci, což umožní provozu ještě lépe se vmísit s provozem s nízkou latencí. Jakmile je splněna podmínka pro přenos, router držící clove (který sám by pravděpodobně byl garlic message) jej jednoduše přepošle podle požadavku — na router, do tunnel, nebo nejpravděpodobněji na vzdálenou klientskou destinaci.

Cíl služeb s proměnnou latencí vyžaduje významné zdroje pro mechanismy store-and-forward (uložení a předání), aby je bylo možné podporovat. Tyto mechanismy mohou být a jsou podporovány v různých aplikacích pro zasílání zpráv, jako je i2p-bote. Na síťové úrovni poskytují tyto služby alternativní sítě jako Freenet. Rozhodli jsme se, že tento cíl na úrovni I2P routeru nebudeme sledovat.

---

## Podobné systémy

Architektura I2P staví na konceptech middleware orientovaného na zprávy, topologii DHT, anonymitě a kryptografii svobodných route mixnetů a přizpůsobivosti packet switched sítí. Hodnota však nepochází z nových konceptů nebo algoritmů, ale z pečlivého inženýrství kombinujícího výsledky výzkumu existujících systémů a publikací. I když existuje několik podobných snah hodných zkoumání, jak pro technická, tak funkční srovnání, dva jsou zde zvláště vyzdvihnuty — Tor a Freenet.

Viz také [Stránka porovnání sítí](/docs/overview/comparison/). Upozorňujeme, že tyto popisy napsal jrandom v roce 2003 a nemusí být v současnosti přesné.

### Tor

*[webové stránky](https://www.torproject.org/)*

Na první pohled mají Tor a I2P mnoho funkčních a anonymitních podobností. Ačkoli vývoj I2P začal dříve, než jsme si byli vědomi raných snah o Tor, mnoho lekcí z původních projektů onion routing a ZKS bylo začleněno do návrhu I2P. Místo budování v podstatě důvěryhodného, centralizovaného systému s adresářovými servery má I2P samoorganizující se síťovou databázi, kde každý peer přebírá odpovědnost za profilování ostatních routerů, aby určil, jak nejlépe využít dostupné zdroje. Dalším klíčovým rozdílem je, že zatímco I2P i Tor používají vrstvené a uspořádané cesty (tunnely a circuits/streams), I2P je fundamentálně síť s přepínáním paketů, zatímco Tor je fundamentálně síť s přepínáním okruhů, což umožňuje I2P transparentně směrovat kolem přetížení nebo jiných síťových selhání, provozovat redundantní cesty a vyrovnávat zátěž dat napříč dostupnými zdroji. Zatímco Tor nabízí užitečnou funkcionalitu outproxy tím, že nabízí integrované objevování a výběr outproxy, I2P ponechává taková rozhodnutí na aplikační vrstvě na aplikacích běžících nad I2P — ve skutečnosti I2P dokonce externalizovalo samotnou TCP-podobnou streaming knihovnu na aplikační vrstvu, což umožňuje vývojářům experimentovat s různými strategiemi a využívat jejich doménové specifické znalosti k nabízení lepšího výkonu.

Z pohledu anonymity existuje mnoho podobností při porovnání základních sítí. Existuje však několik klíčových rozdílů. Při jednání s interním protivníkem nebo většinou externích protivníků vystavují I2P simplex tunnely polovinu dat o provozu oproti tomu, co by bylo vystaveno u Tor duplex okruhů pouhým pozorováním toků samotných — HTTP požadavek a odpověď by v Toru následovaly stejnou cestu, zatímco v I2P by pakety tvořící požadavek šly ven přes jeden nebo více outbound tunnelů a pakety tvořící odpověď by se vrátily přes jeden nebo více různých inbound tunnelů. Zatímco I2P strategie výběru a řazení peerů by měly dostatečně řešit predecessor útoky, pokud by byl nutný přechod na obousměrné tunnely, mohli bychom jednoduše vybudovat inbound a outbound tunnel podél stejných routerů.

Další problém s anonymitou se vyskytuje při použití teleskopické tvorby tunelů v Toru, protože jednoduché počítání paketů a měření časování při průchodu buněk okruhem přes uzel protivníka odhaluje statistické informace o tom, kde se protivník v okruhu nachází. I2P používá jednosměrnou tvorbu tunelů s jednou zprávou, takže tato data nejsou odhalena. Ochrana pozice v tunelu je důležitá, protože jinak by protivník byl schopen provést řadu mocných útoků typu predecessor, intersection a traffic confirmation.

Celkově se Tor a I2P vzájemně doplňují ve svém zaměření — Tor pracuje na poskytování vysokorychlostního anonymního internetového outproxingu, zatímco I2P pracuje na poskytování decentralizované odolné sítě jako takové. Teoreticky lze oba použít k dosažení obou účelů, ale vzhledem k omezeným vývojářským zdrojům mají oba své silné a slabé stránky. Vývojáři I2P zvážili kroky nezbytné k úpravě Toru tak, aby využíval design I2P, ale obavy o životaschopnost Toru v podmínkách nedostatku zdrojů naznačují, že architektura přepínání paketů I2P bude schopna efektivněji využívat vzácné zdroje.

### Freenet

*[webová stránka](http://www.freenetproject.org/)*

Freenet hrál velkou roli v počátečních fázích návrhu I2P — poskytl důkaz životaschopnosti živé pseudonymní komunity úplně obsažené v rámci sítě a demonstroval, že nebezpečí vlastní outproxy lze vyhnout. První zárodek I2P začal jako náhrada komunikační vrstvy pro Freenet, s pokusem o vyčlenění složitostí škálovatelné, anonymní a bezpečné point-to-point komunikace od složitostí distribuovaného datového úložiště odolného vůči cenzuře. Postupem času však některé problémy s anonymitou a škálovatelností vlastní algoritmům Frenentu objasnily, že se I2P měl soustředit výhradně na poskytování generické anonymní komunikační vrstvy, spíše než jako součást Frenentu. V průběhu let vývojáři Frenentu rozpoznali slabiny ve starším návrhu, což je vedlo k návrhu, že budou potřebovat "premix" vrstvu pro nabídnutí podstatné anonymity. Jinými slovy, Freenet potřebuje běžet nad mixnet jako je I2P nebo Tor, s "klientskými uzly" požadujícími a publikujícími data přes mixnet na "serverové uzly", které pak načítají a ukládají data podle heuristických algoritmů distribuovaného datového úložiště Frenentu.

Funkcionalita sítě Freenet je velmi komplementární k I2P, protože Freenet nativně poskytuje mnoho nástrojů pro provoz systémů se střední a vysokou latencí, zatímco I2P nativně poskytuje mixovací síť s nízkou latencí vhodnou pro zajištění přiměřené anonymity. Logika oddělení mixovací sítě od cenzuře odolného distribuovaného datového úložiště stále vypadá samozřejmě z pohledu inženýringu, anonymity, bezpečnosti a alokace zdrojů, takže doufejme, že tým Freenet bude pokračovat v úsilí tímto směrem, pokud nebude jednoduše znovu používat (nebo pomáhat zlepšovat, podle potřeby) existující mixovací sítě jako I2P nebo Tor.

---

## Příloha A: Aplikační vrstva

I2P samotné ve skutečnosti nedělá moc — jednoduše posílá zprávy do vzdálených cílů a přijímá zprávy určené pro místní cíle — většina zajímavé práce se odehrává ve vrstvách nad ním. Samo o sobě by mohlo být I2P vnímáno jako anonymní a bezpečná IP vrstva a přibalená [streaming knihovna](#streaming-library) jako implementace anonymní a bezpečné TCP vrstvy nad ní. Kromě toho [I2PTunnel](#i2ptunnel) poskytuje obecný TCP proxy systém buď pro vstup do I2P sítě nebo výstup z ní, plus celá řada síťových aplikací poskytuje další funkcionalitu pro koncové uživatele.

### Knihovna streamování

I2P streaming knihovnu lze chápat jako obecné streamovací rozhraní (zrcadlící TCP sockety) a implementace podporuje [sliding window protokol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) s několika optimalizacemi, aby se zohlednilo vysoké zpoždění přes I2P. Jednotlivé streamy mohou upravit maximální velikost paketu a další možnosti, ačkoli výchozí hodnota 4KB komprimovaných dat se zdá být rozumným kompromisem mezi náklady na šířku pásma při retransmisi ztracených zpráv a latencí při více zprávách.

Kromě toho, vzhledem k relativně vysokým nákladům na následné zprávy, byl protokol streaming knihovny pro plánování a doručování zpráv optimalizován tak, aby jednotlivé předávané zprávy mohly obsahovat co nejvíce dostupných informací. Například malá HTTP transakce proxovaná přes streaming knihovnu může být dokončena v jediné výměně zpráv — první zpráva sbalí SYN, FIN a malou datovou část (HTTP požadavek se obvykle vejde) a odpověď sbalí SYN, FIN, ACK a malou datovou část (mnoho HTTP odpovědí se vejde). Zatímco dodatečné ACK musí být přeneseno, aby HTTP serveru oznámilo, že SYN/FIN/ACK bylo přijato, místní HTTP proxy může doručit kompletní odpověď do prohlížeče okamžitě.

Celkově však streaming knihovna velmi připomíná abstrakci TCP se svými posuvnými okny, algoritmy řízení přetížení (jak pomalý start, tak vyhýbání se přetížení) a obecným chováním paketů (ACK, SYN, FIN, RST, atd.).

### Knihovna pojmenování a adresář

*Pro více informací viz stránka [Pojmenování a Adresář](/docs/overview/naming/).*

*Vyvinuto: mihi, Ragnarok*

Pojmenovávání v rámci I2P je často diskutovaným tématem od samého začátku s zastánci napříč spektrem možností. Nicméně, vzhledem k inherentnímu požadavku I2P na bezpečnou komunikaci a decentralizovaný provoz, je tradiční systém pojmenovávání ve stylu DNS jednoznačně vyloučen, stejně jako hlasovací systémy typu "rozhoduje většina". Místo toho I2P dodává generickou knihovnu pro pojmenovávání a základní implementaci navrženou pro práci s lokálním mapováním jmen na destinace, stejně jako volitelnou doplňkovou aplikaci nazvanou "Address Book". Address book je zabezpečený, distribuovaný a lidsky čitelný systém pojmenovávání řízený web-of-trust, který obětuje pouze požadavek na globální jedinečnost všech lidsky čitelných jmen tím, že vyžaduje pouze lokální jedinečnost. Zatímco všechny zprávy v I2P jsou kryptograficky adresované podle jejich destinace, různí lidé mohou mít lokální položky v address book pro "Alice", které odkazují na různé destinace. Lidé stále mohou objevovat nová jména importováním publikovaných address book od protějšků specifikovaných v jejich web of trust, přidáváním položek poskytnutých třetí stranou, nebo (pokud někteří lidé organizují řadu publikovaných address book pomocí registračního systému "kdo dřív přijde, ten dřív mele") si lidé mohou vybrat, že budou tyto address book považovat za name servery, čímž emulují tradiční DNS.

I2P však nepodporuje použití DNS-podobných služeb, protože škoda způsobená únosem stránky může být obrovská — a nezabezpečené destinace nemají žádnou hodnotu. DNSsec samotný se stále spoléhá na registrátory a certifikační autority, zatímco u I2P nemohou být požadavky odeslané na destinaci zachyceny ani odpověď zfalšována, protože jsou šifrovány veřejnými klíči destinace, a destinace samotná je jen pár veřejných klíčů a certifikát. DNS-stylové systémy na druhé straně umožňují kterémukoliv ze jmenných serverů na cestě vyhledávání provést jednoduché útoky odmítnutí služby a spoofing. Přidání certifikátu ověřujícího odpovědi jako podepsané nějakou centralizovanou certifikační autoritou by vyřešilo mnoho problémů s nepřátelskými jmennými servery, ale ponechalo by otevřené replay útoky stejně jako útoky nepřátelských certifikačních autorit.

Hlasovací styl pojmenování je také nebezpečný, zejména vzhledem k efektivitě Sybil útoků v anonymních systémech — útočník může jednoduše vytvořit libovolně vysoký počet peerů a "hlasovat" s každým z nich, aby převzal kontrolu nad daným jménem. Metody proof-of-work lze použít k tomu, aby identita nebyla zadarmo, ale jak síť roste, zátěž potřebná pro kontaktování všech za účelem provedení online hlasování je nepravděpodobná, nebo pokud není dotazována celá síť, mohou být dosažitelné různé sady odpovědí.

Stejně jako u Internetu však I2P udržuje návrh a provoz jmenovacího systému mimo (IP-podobnou) komunikační vrstvu. Přibalená knihovna pro jmenování obsahuje jednoduché rozhraní poskytovatele služeb, do kterého se mohou zapojit alternativní jmenovací systémy, což umožňuje koncovým uživatelům řídit, jaké kompromisy v jmenování preferují.

### I2PTunnel

*Vytvořeno: mihi*

I2PTunnel je pravděpodobně nejpopulárnější a nejuniverzálnější klientská aplikace I2P, která umožňuje obecné proxy služby jak do, tak z I2P sítě. I2PTunnel lze chápat jako čtyři samostatné proxy aplikace — „client" který přijímá příchozí TCP spojení a přeposílá je na dané I2P destination, „httpclient" (také „eepproxy") který funguje jako HTTP proxy a přeposílá požadavky na příslušné I2P destination (po dotazu na službu názvů, pokud je to nutné), „server" který přijímá příchozí I2P streaming spojení na destination a přeposílá je na daný TCP host+port, a „httpserver" který rozšiřuje „server" analýzou HTTP požadavků a odpovědí pro bezpečnější provoz. Existuje také dodatečná aplikace „socksclient", ale její použití se nedoporučuje z důvodů zmíněných dříve.

I2P sám o sobě není síť outproxy — obavy o anonymitu a bezpečnost inherentní v mix síti, která přeposílá data do a ze sítě, udržely design I2P zaměřený na poskytování anonymní sítě, která je schopna splnit potřeby uživatelů bez vyžadování externích zdrojů. Nicméně aplikace I2PTunnel "httpclient" nabízí možnost pro outproxy — pokud požadovaný hostname nekončí na ".i2p", vybere náhodnou destinaci z uživatelem poskytnuté sady outproxy a přepošle jim požadavek. Tyto destinace jsou jednoduše instance I2PTunnel "server" provozované dobrovolníky, kteří se výslovně rozhodli provozovat outproxy — nikdo není outproxy ve výchozím nastavení a provozování outproxy automaticky neříká ostatním lidem, aby přes vás proxy směřovali. I když outproxy mají inherentní slabiny, nabízejí jednoduchý důkaz konceptu pro používání I2P a poskytují určitou funkcionalitu pod modelem hrozeb, který může být pro některé uživatele dostatečný.

I2PTunnel umožňuje většinu používaných aplikací. "httpserver" směřující na webserver umožňuje komukoli provozovat vlastní anonymní webovou stránku (nebo "I2P Site") — webserver je součástí balíčku I2P pro tento účel, ale lze použít jakýkoli webserver. Každý může provozovat "client" směřující na jeden z anonymně hostovaných IRC serverů, z nichž každý provozuje "server" směřující na svůj místní IRCd a komunikuje mezi IRCd přes vlastní "client" tunely. Koncoví uživatelé také mají "client" tunely směřující na POP3 a SMTP destinace [I2Pmail](#i2pmail--susimail) (které jsou jednoduše "server" instance směřující na POP3 a SMTP servery), stejně jako "client" tunely směřující na CVS server I2P, což umožňuje anonymní vývoj. Někdy lidé dokonce provozovali "client" proxy pro přístup k "server" instancím směřujícím na NNTP server.

### I2PSnark

*I2PSnark vyvinut: jrandom a další, portován z [mjw](http://www.klomp.org/mark/)'s [Snark](http://www.klomp.org/snark/) klienta*

Dodávaný s instalací I2P, I2PSnark nabízí jednoduchý anonymní BitTorrent klient s možnostmi více torrentů současně, který zpřístupňuje všechny funkce prostřednictvím prostého HTML webového rozhraní.

### I2Pmail / Susimail

*Vyvinuto: postman, susi23, mastiejaner*

I2Pmail je spíše služba než aplikace — postman nabízí jak interní, tak externí e-mail s POP3 a SMTP službami prostřednictvím I2PTunnel instancí přistupujících k sérii komponent vyvinutých s mastiejaner, což umožňuje lidem používat jejich preferované e-mailové klienty k pseudonymnímu odesílání a přijímání pošty. Protože však většina e-mailových klientů odhaluje podstatné identifikační informace, I2P obsahuje webového klienta susimail od susi23, který byl vytvořen specificky s ohledem na potřeby anonymity I2P. Služba I2Pmail/mail.i2p nabízí transparentní filtrování virů i prevenci útoků typu denial of service s kvótami rozšířenými o hashcash. Navíc má každý uživatel kontrolu nad svou strategií dávkování před doručením prostřednictvím mail.i2p outproxies, které jsou oddělené od mail.i2p SMTP a POP3 serverů — jak outproxies, tak inproxies komunikují s mail.i2p SMTP a POP3 servery přímo přes I2P, takže kompromitování těchto neanonymních lokací neumožňuje přístup k e-mailovým účtům nebo vzorcům aktivity uživatele.
