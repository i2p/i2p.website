---
title: "Bittorrent přes I2P"
description: "Specifikace protokolu pro BitTorrent klienty a trackery na I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Na I2P existuje několik bittorrent klientů a trackerů. Protože I2P adresování používá Destination namísto IP a portu, jsou potřeba menší změny v tracker a klientském softwaru pro provoz na I2P. Tyto změny jsou specifikovány níže. Pozorně si všimněte pokynů pro kompatibilitu se staršími I2P klienty a trackery.

Tato stránka specifikuje detaily protokolu společné všem klientům a trackerům. Konkrétní klienti a trackery mohou implementovat další jedinečné funkce nebo protokoly.

Vítáme další porty klientského a tracker softwaru do I2P.

---

## Obecné pokyny pro vývojáře

Většina non-Java bittorrent klientů se připojí k I2P přes [SAMv3](/docs/api/samv3/). SAM sessions (nebo uvnitř I2P, tunnel pools nebo sady tunnelů) jsou navrženy jako dlouhodobé. Většina bittorrent klientů bude potřebovat pouze jednu session, vytvořenou při spuštění a uzavřenou při ukončení. I2P se liší od Tor, kde mohou být okruhy rychle vytvářeny a zahazovány. Pečlivě zvažte a poraďte se s vývojáři I2P před návrhem vaší aplikace tak, aby používala více než jednu nebo dvě simultánní sessions, nebo je rychle vytvářela a zahazovala. Bittorrent klienti nesmí vytvářet unikátní session pro každé spojení. Navrhněte svého klienta tak, aby používal stejnou session pro oznámení i klientská spojení.

Také se prosím ujistěte, že nastavení vašeho klienta (a pokyny pro uživatele ohledně nastavení routeru, nebo výchozí nastavení routeru pokud router dodáváte) povede k tomu, že vaši uživatelé budou přispívat do sítě více zdrojů, než kolik spotřebovávají. I2P je peer-to-peer síť a síť nemůže přežít, pokud populární aplikace uvrhne síť do trvalého přetížení.

Neposkytujte podporu pro bittorrent přes I2P outproxy do clearnet, protože bude pravděpodobně zablokován. Poraďte se s operátory outproxy ohledně pokynů.

Implementace routerů Java I2P a i2pd jsou nezávislé a mají menší rozdíly v chování, podpoře funkcí a výchozích nastaveních. Prosím testujte vaši aplikaci s nejnovější verzí obou routerů.

i2pd SAM je ve výchozím nastavení povolen; Java I2P SAM nikoliv. Poskytněte svým uživatelům instrukce, jak povolit SAM v Java I2P (přes /configclients v konzoli routeru), a/nebo poskytněte uživateli dobrou chybovou zprávu, pokud počáteční připojení selže, např. "ujistěte se, že I2P běží a rozhraní SAM je povoleno".

Java I2P a i2pd routery mají různé výchozí hodnoty pro počet tunnelů. Výchozí hodnota pro Java je 2 a výchozí hodnota pro i2pd je 5. Pro většinu aplikací s nízkou až střední šířkou pásma a nízkým až středním počtem připojení je dostačující hodnota 3. Prosím, specifikujte počet tunnelů ve zprávě SESSION CREATE, abyste získali konzistentní výkon s Java I2P a i2pd routery.

I2P podporuje více typů podpisů a šifrování. Kvůli kompatibilitě I2P ve výchozím nastavení používá staré a neefektivní typy, takže všichni klienti by měli specifikovat novější typy.

Při použití SAM je typ podpisu specifikován v příkazech DEST GENERATE a SESSION CREATE (pro přechodné). Všichni klienti by měli nastavit SIGNATURE_TYPE=7 (Ed25519).

Typ šifrování je specifikován v příkazu SAM SESSION CREATE nebo v i2cp options. Je povoleno více typů šifrování. Někteří trackeři podporují ECIES-X25519, někteří podporují ElGamal a někteří podporují oba. Klienti by měli nastavit i2cp.leaseSetEncType=4,0 (pro ECIES-X25519 a ElGamal), aby se mohli připojit k oběma.

Podpora DHT vyžaduje SAM v3.3 PRIMARY a SUBSESSIONS pro TCP a UDP přes stejnou session. To bude vyžadovat značné vývojové úsilí na straně klienta, pokud není klient napsán v Javě. i2pd v současnosti nepodporuje SAM v3.3. libtorrent v současnosti nepodporuje SAM v3.3.

Bez podpory DHT můžete chtít automaticky oznamovat konfigurovatelný seznam známých otevřených trackerů, aby fungovaly magnet odkazy. Poraďte se s uživateli I2P ohledně informací o aktuálně fungujících otevřených trackerech a udržujte své výchozí nastavení aktuální. Podpora rozšíření i2p_pex také pomůže zmírnit nedostatek podpory DHT.

Pro více pokynů vývojářům ohledně zajištění, aby vaše aplikace používala pouze potřebné zdroje, se prosím podívejte na [specifikaci SAMv3](/docs/api/samv3/) a [náš návod pro zabalení I2P s vaší aplikací](/docs/applications/embedding/). Kontaktujte vývojáře I2P nebo i2pd pro další pomoc.

---

## Oznámení

Klienti obecně zahrnují falešný parametr port=6881 v announce, kvůli kompatibilitě se staršími trackery. Trackery mohou parametr port ignorovat a neměly by jej vyžadovat.

Parametr ip je base 64 klientského [Destination](/docs/specs/common-structures/#struct_Destination), používající I2P Base 64 abecedu [A-Z][a-z][0-9]-~. [Destinations](/docs/specs/common-structures/#struct_Destination) mají 387+ bajtů, takže Base 64 má 516+ bajtů. Klienti obvykle připojují ".i2p" k Base 64 Destination pro kompatibilitu se staršími trackery. Trackery by neměly vyžadovat připojené ".i2p".

Ostatní parametry jsou stejné jako ve standardním bittorrent.

Aktuální Destinations pro klienty mají 387 nebo více bytů (516 nebo více v Base 64 kódování). Rozumné maximum, které lze prozatím předpokládat, je 475 bytů. Protože tracker musí dekódovat Base64 pro doručení kompaktních odpovědí (viz níže), tracker by pravděpodobně měl dekódovat a odmítnout špatné Base64 při oznámení.

Výchozí typ odpovědi je nekompaktní. Klienti mohou požádat o kompaktní odpověď s parametrem compact=1. Tracker může, ale není povinen, vrátit kompaktní odpověď na požádání. Poznámka: Všechny populární trackery nyní podporují kompaktní odpovědi a alespoň jeden vyžaduje compact=1 v announce. Všichni klienti by měli požadovat a podporovat kompaktní odpovědi.

Vývojářům nových I2P klientů se důrazně doporučuje implementovat oznámení přes jejich vlastní tunnel namísto HTTP klientské proxy na portu 4444. Takový postup je efektivnější a umožňuje trackeru vynucování cílové destinace (viz níže).

Specifikace pro UDP oznámení byla dokončena v červnu 2025. Podpora v různých I2P klientech a trackerech bude postupně zaváděna později v roce 2025. Další informace naleznete níže.

---

## Nekompaktní odpovědi trackeru

Poznámka: Zastaralé. Všechny populární trackery nyní podporují kompaktní odpovědi a alespoň jeden vyžaduje compact=1 v announce. Všichni klienti by měli požadovat a podporovat kompaktní odpovědi.

Nekompaktní odpověď je stejná jako ve standardním bittorrentu, s I2P "ip". Jedná se o dlouhý base64-kódovaný "DNS řetězec", pravděpodobně s příponou ".i2p".

Trackery obecně zahrnují falešný klíč portu nebo používají port z oznámení kvůli kompatibilitě se staršími klienty. Klienti musí parametr portu ignorovat a neměli by ho vyžadovat.

Hodnota klíče ip je base 64 klientského [Destination](/docs/specs/common-structures/#struct_Destination), jak je popsáno výše. Trackery obecně připojují ".i2p" k Base 64 Destination, pokud nebylo v announce ip, kvůli kompatibilitě se staršími klienty. Klienti by neměli vyžadovat připojené ".i2p" v odpovědích.

Ostatní klíče a hodnoty odpovědi jsou stejné jako ve standardním bittorrentu.

---

## Kompaktní odpovědi trackeru

V kompaktní odpovědi je hodnota klíče slovníku "peers" jeden byte string, jehož délka je násobkem 32 bytů. Tento řetězec obsahuje zřetězené [32-bytové SHA-256 hashe](/docs/specs/common-structures/#type_Hash) binárních [Destinations](/docs/specs/common-structures/#struct_Destination) peerů. Tento hash musí být vypočítán trackerem, pokud se nepoužívá vynucování destination (viz níže), v takovém případě může být hash dodaný v HTTP hlavičkách X-I2P-DestHash nebo X-I2P-DestB32 převeden na binární a uložen. Klíč peers může chybět nebo může mít hodnota peers nulovou délku.

Ačkoli je podpora kompaktních odpovědí volitelná jak pro klienty, tak pro trackery, je vysoce doporučována, protože snižuje nominální velikost odpovědi o více než 90 %.

---

## Vynucení destination

Někteří, ale ne všichni, I2P bittorrent klienti oznamují přes své vlastní tunnely. Trackery si mohou zvolit zabránění spoofingu tím, že to budou vyžadovat a ověřovat klientovu [Destination](/docs/specs/common-structures/#struct_Destination) pomocí HTTP hlaviček přidaných I2PTunnel HTTP Server tunelem. Hlavičky jsou X-I2P-DestHash, X-I2P-DestB64 a X-I2P-DestB32, které jsou různými formáty pro stejnou informaci. Tyto hlavičky nemohou být klientem zfalšovány. Tracker vynucující destinations nemusí vůbec vyžadovat parametr ip announce.

Vzhledem k tomu, že několik klientů používá HTTP proxy místo svého vlastního tunelu pro oznámení, vynucování cílové destinace zabrání použití těmito klienty, dokud nebudou tito klienti převedeni na oznamování přes svůj vlastní tunnel.

Bohužel, jak síť roste, tak bude růst i množství škodlivosti, takže očekáváme, že všechny trackery budou nakonec vynucovat destinations. Vývojáři trackerů i klientů by to měli očekávat.

---

## Oznámit názvy hostitelů

Názvy hostitelů pro URL oznámení v torrent souborech obecně následují [standardy pojmenování I2P](/docs/overview/naming/). Kromě názvů hostitelů z adresářů adres a ".b32.i2p" Base 32 názvů hostitelů by měl být podporován také úplný Base 64 Destination (s připojeným ".i2p" nebo bez něj). Neotevřené trackery by měly rozpoznat svůj vlastní název hostitele v kterémkoli z těchto formátů.

Pro zachování anonymity by klienti obecně měli ignorovat announce URL adresy v torrent souborech, které nejsou I2P.

---

## Klientská připojení

Spojení klient-klient používají standardní protokol přes TCP. Neexistují žádní známí I2P klienti, kteří v současnosti podporují uTP komunikaci.

I2P používá 387+ bajtové [Destinations](/docs/specs/common-structures/#struct_Destination) pro adresy, jak je vysvětleno výše.

Pokud klient má pouze hash cíle (například z kompaktní odpovědi nebo PEX), musí provést vyhledávání zakódováním pomocí Base 32, připojením ".b32.i2p" a dotazem na Naming Service, který vrátí úplný Destination, pokud je k dispozici.

Pokud má klient úplnou Destination protějšku, kterou obdržel v nekompaktní odpovědi, měl by ji použít přímo při navazování spojení. Nepřevádějte Destination zpět na Base 32 hash pro vyhledávání, je to velmi neefektivní.

---

## Prevence cross-network

Pro zachování anonymity obecně I2P bittorrent klienti nepodporují oznámení nebo připojení k protějškům mimo I2P. I2P HTTP outproxy často blokují oznámení. Nejsou známé žádné SOCKS outproxy podporující bittorrent provoz.

Aby se zabránilo používání klienty mimo I2P prostřednictvím HTTP inproxy, I2P trackery často blokují přístupy nebo ohlášení, která obsahují HTTP hlavičku X-Forwarded-For. Trackery by měly odmítat standardní síťová ohlášení s IPv4 nebo IPv6 IP adresami a nedoručovat je v odpovědích.

---

## PEX

I2P PEX je založeno na ut_pex. Jelikož se nezdá, že by byla k dispozici formální specifikace ut_pex, může být nutné pro pomoc nahlédnout do zdrojového kódu libtorrent. Jedná se o rozšiřující zprávu, identifikovanou jako "i2p_pex" v [rozšiřujícím handshaku](http://www.bittorrent.org/beps/bep_0010.html). Obsahuje bencoded slovník s až 3 klíči: "added", "added.f" a "dropped". Hodnoty added a dropped jsou každá jednotlivým byte řetězcem, jehož délka je násobkem 32 bytů. Tyto byte řetězce jsou zřetězené SHA-256 hashe binárních [Destinations](/docs/specs/common-structures/#struct_Destination) peerů. Jedná se o stejný formát jako hodnota slovníku peers v kompaktním formátu odpovědi i2p specifikovaném výše. Hodnota added.f, pokud je přítomna, je stejná jako v ut_pex.

---

## DHT

Podpora DHT je zahrnuta v klientu i2psnark od verze 0.9.2. Předběžné rozdíly od [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) jsou popsány níže a mohou se změnit. Kontaktujte vývojáře I2P, pokud chcete vyvinout klienta podporujícího DHT.

Na rozdíl od standardní DHT nepoužívá I2P DHT bit v options handshake nebo PORT zprávu. Je inzerována pomocí rozšiřující zprávy, identifikované jako "i2p_dht" v [extension handshake](http://www.bittorrent.org/beps/bep_0010.html). Obsahuje bencoded slovník se dvěma klíči, "port" a "rport", oba celá čísla.

UDP (datagram) port uvedený v kompaktních informacích o uzlu se používá pro příjem datagramů s možností odpovědi (podepsaných). Používá se pro dotazy, kromě oznámení. Říkáme tomu "query port". Jedná se o hodnotu "port" ze zprávy rozšíření. Dotazy používají [I2CP](/docs/specs/i2cp/) protokol číslo 17.

Kromě tohoto UDP portu používáme druhý datagramový port rovný query portu + 1. Ten se používá k přijímání nepodepsaných (raw) datagramů pro odpovědi, chyby a oznámení. Tento port poskytuje zvýšenou efektivitu, protože odpovědi obsahují tokeny odeslané v dotazu a nemusí být podepsány. Nazýváme ho "response port". Toto je hodnota "rport" z rozšiřující zprávy. Musí být 1 + query port. Odpovědi a oznámení používají [I2CP](/docs/specs/i2cp/) protokol číslo 18.

Kompaktní informace o peerovi má 32 bajtů (32bajtový SHA256 Hash) místo 4bajtové IP + 2bajtového portu. Neexistuje port peera. V odpovědi je klíč "values" seznamem řetězců, z nichž každý obsahuje jednu kompaktní informaci o peerovi.

Kompaktní informace o uzlu má 54 bajtů (20bajtové Node ID + 32bajtový SHA256 Hash + 2bajtový port) místo 20bajtového Node ID + 4bajtové IP + 2bajtového portu. V odpovědi je klíč "nodes" jediný bajtový řetězec se zřetězenými kompaktními informacemi o uzlech.

Požadavek na bezpečné ID uzlu: Aby byly různé DHT útoky obtížnější, prvních 4 bajty ID uzlu se musí shodovat s prvními 4 bajty hashe cíle a další dva bajty ID uzlu se musí shodovat s dalšími dvěma bajty hashe cíle exclusive-ORovanými s portem.

V torrent souboru je klíč "nodes" slovníku trackerless torrent zatím TBD. Mohl by to být seznam 32bajtových binárních řetězců (SHA256 hashe) namísto seznamu seznamů obsahujících řetězec hostitele a celé číslo portu. Alternativy: Jediný bajtový řetězec se zřetězenými hashi, nebo seznam pouze řetězců.

---

## Datagram (UDP) Trackery

Specifikace pro UDP announces v I2P byla finalizována v červnu 2025. Podpora v různých I2P klientech a trackerech bude postupně zaváděna během roku 2025. Rozdíly oproti [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) jsou dokumentovány ve [specifikaci UDP announce](/docs/specs/udp-announces/). Specifikace také vyžaduje podporu pro [nové formáty Datagram 2/3](/docs/specs/datagrams/).

---

## Dodatečné informace

Předběžná specifikace pro výpočet povolené rychlé sady je uvedena v [Návrhu 172](/proposals/172-bep6-allowed-fast)

---

## Další informace

- I2P bittorrent standardy se obecně diskutují na [zzz.i2p](http://zzz.i2p/).
- Graf současných možností tracker softwaru je [také dostupný tam](http://zzz.i2p/files/trackers.html).
- [I2P bittorrent FAQ](http://forum.i2p/viewtopic.php?t=2068)
- [DHT na I2P diskuze](http://zzz.i2p/topics/812)
