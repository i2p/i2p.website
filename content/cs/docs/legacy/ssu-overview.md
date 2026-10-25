---
title: "Secure Semireliable UDP (SSU)"
description: "Původní UDP transport používaný před SSU2 (zastaralý)"
slug: "ssu-overview"
aliases:
  - "/cs/udp"
  - "/cs/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**ZASTARALÉ** - SSU byl nahrazen SSU2. Podpora SSU byla odstraněna z i2pd ve verzi 2.44.0 (API 0.9.56) 2022-11. Podpora SSU byla odstraněna z Java I2P ve verzi 2.4.0 (API 0.9.61) 2023-12.

SSU (také nazývaný "UDP" ve většině I2P dokumentace a uživatelských rozhraní) byl jedním ze dvou [transportů](/docs/transport) implementovaných v I2P. Druhým je [NTCP2](/docs/specs/ntcp2). Podpora pro [NTCP](/docs/legacy/ntcp) byla odstraněna.

SSU bylo představeno v I2P vydání 0.6. Ve standardní I2P instalaci používá router jak NTCP, tak SSU pro odchozí spojení. SSU-over-IPv6 je podporováno od verze 0.9.8.

SSU je nazýváno "semispolehlivé", protože opakovaně přenáší nepotvrzené zprávy, ale pouze do maximálního počtu pokusů. Poté je zpráva zahozena.

## SSU služby

Stejně jako NTCP transport poskytuje SSU spolehlivý, šifrovaný, spojově orientovaný, point-to-point přenos dat. Unikátní pro SSU je, že také poskytuje služby detekce IP a NAT traversal, včetně:

- Kooperativní průchod NAT/firewall pomocí [introducer](#introduction)
- Detekce lokální IP kontrolou příchozích paketů a [peer testing](#peerTesting)
- Komunikace stavu firewallu a lokální IP a změn obojího do NTCP
- Komunikace stavu firewallu a lokální IP a změn obojího do routeru a uživatelského rozhraní

## Specifikace adresy routeru {#ra}

Následující vlastnosti jsou uloženy v síťové databázi.

- **Transport name:** SSU
- **caps:** [B,C,4,6] [Viz níže](#capabilities).
- **host:** IP (IPv4 nebo IPv6).
  Zkrácená IPv6 adresa (s "::") je povolena.
  Může nebo nemusí být přítomna při firewallu.
  Názvy hostů byly dříve povoleny, ale jsou zastaralé od verze 0.9.32. Viz návrh 141.
- **iexp[0-2]:** Vypršení tohoto introduceru.
  ASCII číslice, v sekundách od epochy.
  Přítomno pouze při firewallu, kdy jsou potřeba introducery.
  Volitelné (i když jsou přítomny další vlastnosti pro tento introducer).
  Od verze 0.9.30, návrh 133.
- **ihost[0-2]:** IP introduceru (IPv4 nebo IPv6).
  Názvy hostů byly dříve povoleny, ale jsou zastaralé od verze 0.9.32. Viz návrh 141.
  Zkrácená IPv6 adresa (s "::") je povolena.
  Přítomno pouze při firewallu, kdy jsou potřeba introducery.
  [Viz níže](#introduction).
- **ikey[0-2]:** Base 64 introduction key introduceru. [Viz níže](#key).
  Přítomno pouze při firewallu, kdy jsou potřeba introducery.
  [Viz níže](#introduction).
- **iport[0-2]:** Port introduceru 1024 - 65535.
  Přítomno pouze při firewallu, kdy jsou potřeba introducery.
  [Viz níže](#introduction).
- **itag[0-2]:** Tag introduceru 1 - (2^32 - 1)
  ASCII číslice.
  Přítomno pouze při firewallu, kdy jsou potřeba introducery.
  [Viz níže](#introduction).
- **key:** Base 64 introduction key. [Viz níže](#key).
- **mtu:** Volitelné. Výchozí a maximum je 1484. Minimum je 620.
  Musí být přítomno pro IPv6, kde je minimum 1280 a maximum 1488
  (maximum bylo 1472 před verzí 0.9.28).
  IPv6 MTU musí být násobek 16.
  (IPv4 MTU + 4) musí být násobek 16.
  [Viz níže](#mtu).
- **port:** 1024 - 65535
  Může nebo nemusí být přítomen při firewallu.

# Detaily protokolu

## Řízení přetížení {#congestioncontrol}

Potřeba SSU pouze pro částečně spolehlivé doručování, TCP-friendly operace a schopnost vysoké propustnosti umožňuje velkou volnost v řízení zahlcení. Algoritmus řízení zahlcení popsaný níže je navržen tak, aby byl efektivní z hlediska šířky pásma a zároveň jednoduchý na implementaci.

Pakety jsou plánovány podle politiky routeru a dbá se na to, aby se nepřekročila odchozí kapacita routeru ani naměřená kapacita vzdáleného uzlu. Naměřená kapacita funguje podobně jako pomalý start a vyhýbání se přetížení u TCP, s aditivními zvýšeními odesílací kapacity a multiplikativními sníženími při přetížení. Na rozdíl od TCP mohou routery vzdát některé zprávy po uplynutí určité doby nebo počtu opakovaných odeslání, zatímco pokračují v přenosu jiných zpráv.

Techniky detekce přetížení se také liší od TCP, protože každá zpráva má svůj vlastní jedinečný a nesekvenciální identifikátor a každá zpráva má omezenou velikost - maximálně 32KB. Pro efektivní přenos této zpětné vazby odesílateli příjemce pravidelně zahrnuje seznam plně ACKovaných identifikátorů zpráv a může také zahrnovat bitová pole pro částečně přijaté zprávy, kde každý bit představuje přijetí fragmentu. Pokud dorazí duplicitní fragmenty, zpráva by měla být znovu ACKována, nebo pokud zpráva stále nebyla plně přijata, bitové pole by mělo být znovu přeneseno s případnými novými aktualizacemi.

Současná implementace nevyplňuje pakety na určitou velikost, ale místo toho pouze umístí jeden fragment zprávy do paketu a odešle ho (přitom dává pozor, aby nepřekročila MTU).

### MTU {#mtu}

Od verze routeru 0.8.12 se pro IPv4 používají dvě hodnoty MTU: 620 a 1484. Hodnota MTU se upravuje na základě procenta paketů, které jsou přeposílány znovu.

Pro obě hodnoty MTU je žádoucí, aby (MTU % 16) == 12, takže část payload po 28-bytové IP/UDP hlavičce je násobkem 16 bytů, pro účely šifrování.

Pro malou hodnotu MTU je žádoucí efektivně zabalit 2646-bajtovou Variable Tunnel Build Message do několika paketů; s 620-bajtovým MTU se vejde pěkně do 5 paketů.

Na základě měření se 1492 hodí téměř pro všechny rozumně malé I2NP zprávy (větší I2NP zprávy mohou mít až 1900 až 4500 bajtů, což se stejně nevejde do MTU živé sítě).

Hodnoty MTU byly 608 a 1492 pro vydání 0.8.9 - 0.8.11. Velké MTU bylo 1350 před vydáním 0.8.9.

Maximální velikost přijímaného paketu je 1571 bajtů od vydání 0.8.12. Pro vydání 0.8.9 - 0.8.11 to bylo 1535 bajtů. Před vydáním 0.8.9 to bylo 2048 bajtů.

Od verze 0.9.2, pokud je MTU síťového rozhraní routeru menší než 1484, zveřejní to v síťové databázi a ostatní routery by to měly respektovat při navazování spojení.

Pro IPv6 je minimální MTU 1280. IPv6 IP/UDP hlavička má 48 bajtů, takže používáme MTU kde (MTU % 16 == 0), což platí pro 1280. Maximální IPv6 MTU je 1488. (maximum bylo 1472 před verzí 0.9.28).

### Limity velikosti zpráv {#max}

Zatímco maximální velikost zprávy je nominálně 32KB, praktický limit se liší. Protokol omezuje počet fragmentů na 7 bitů, neboli 128. Současná implementace však omezuje každou zprávu na maximálně 64 fragmentů, což je dostatečné pro 64 * 534 = 33,3 KB při použití MTU 608. Kvůli režii pro zabalené LeaseSet a klíče relace je praktický limit na úrovni aplikace přibližně o 6KB nižší, neboli kolem 26KB. Je nutná další práce na zvýšení limitu UDP transportu nad 32KB. Pro připojení používající větší MTU jsou možné větší zprávy.

## Časový limit nečinnosti

Časový limit nečinnosti a uzavření spojení je na uvážení každého koncového bodu a může se lišit. Současná implementace snižuje časový limit, když se počet spojení blíží nakonfigurovanému maximu, a zvyšuje časový limit, když je počet spojení nízký. Doporučený minimální časový limit je dvě minuty nebo více a doporučený maximální časový limit je deset minut nebo více.

## Klíče {#keys}

Veškeré použité šifrování je AES256/CBC s 32bytovými klíči a 16bytovými IV. Když Alice zahájí relaci s Bobem, MAC a session klíče jsou vyjednány jako součást DH výměny a poté jsou použity pro HMAC a šifrování. Během DH výměny je Bobův veřejně známý introKey použit pro MAC a šifrování.

Jak počáteční zpráva, tak následná odpověď používají introKey odpovídající strany (Bob) - odpovídající strana nepotřebuje znát introKey žádající strany (Alice). DSA podpisový klíč používaný Bobem by již měl být Alice znám, když ho kontaktuje, ačkoliv Alice's DSA klíč nemusí být Bobovi již znám.

Po přijetí zprávy příjemce kontroluje IP adresu a port "odesílatele" se všemi navázanými relacemi - pokud dojde ke shodě, MAC klíče této relace jsou testovány v HMAC. Pokud žádný z nich neprojde ověřením nebo pokud neexistují žádné odpovídající IP adresy, příjemce zkusí svůj introKey v MAC. Pokud se neověří, paket je zahozen. Pokud se ověří, je interpretován podle typu zprávy, ačkoliv pokud je příjemce přetížený, může být i tak zahozen.

Pokud mají Alice a Bob navázanou relaci, ale Alice z nějakého důvodu ztratí klíče a chce kontaktovat Boba, může kdykoliv jednoduše navázat novou relaci prostřednictvím SessionRequest a souvisejících zpráv. Pokud Bob ztratil klíč, ale Alice o tom neví, pokusí se ho nejprve popíchnout k odpovědi tím, že pošle DataMessage s nastaveným příznakem wantReply, a pokud Bob trvale neodpovídá, předpokládá, že je klíč ztracen, a naváže nový.

Pro DH key agreement se používá [RFC3526](http://www.faqs.org/rfcs/rfc3526.html) 2048bit MODP group (#14):

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Jedná se o stejné p a g používané pro I2P [ElGamal šifrování](/docs/specs/cryptography#elgamal).

## Prevence opakování útoků {#replay}

Prevence opakovaných útoků na SSU vrstvě probíhá odmítáním paketů s příliš starými časovými razítky nebo těch, které znovu používají IV. Pro detekci duplicitních IV se používá sekvence Bloomových filtrů, které se pravidelně "rozpadají", takže se detekují pouze nedávno přidaná IV.

MessageIds používané v DataMessages jsou definovány ve vrstvách nad SSU transportem a procházejí transparentně. Tyto ID nejsou v žádném konkrétním pořadí - ve skutečnosti jsou pravděpodobně zcela náhodné. SSU vrstva se nepokouší o prevenci opětovného přehrání messageId - vyšší vrstvy by to měly vzít v úvahu.

## Adresování {#addressing}

Pro kontaktování SSU peer je nutná jedna ze dvou sad informací: přímá adresa, když je peer veřejně dostupný, nebo nepřímá adresa, pro použití třetí strany k představení peer. Neexistuje žádné omezení počtu adres, které může peer mít.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Každá z adres může také vystavovat řadu možností - speciální schopnosti daného konkrétního peer. Pro seznam dostupných schopností viz [níže](#capabilities).

Adresy, možnosti a schopnosti jsou publikovány v [síťové databázi](/docs/overview/network-database).

## Přímé navázání relace {#direct}

Přímé navázání relace se používá, když není potřeba třetí strana pro překonání NAT. Sekvence zpráv je následující:

### Navázání spojení (přímé) {#establishDirect}

Alice se připojuje přímo k Bobovi. IPv6 je podporováno od verze 0.9.8.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Po přijetí zprávy SessionConfirmed pošle Bob malou [zprávu DeliveryStatus](/docs/specs/i2np#msg_DeliveryStatus) jako potvrzení. V této zprávě je 4-bajtové ID zprávy nastaveno na náhodné číslo a 8-bajtový "čas příchodu" je nastaven na aktuální ID platné v celé síti, což je 2 (tj. 0x0000000000000002).

Po odeslání stavové zprávy si uzly obvykle vyměňují [DatabaseStore zprávy](/docs/specs/i2np#msg_DatabaseStore) obsahující jejich [RouterInfos](/docs/specs/common-structures#struct_RouterInfo), avšak toto není povinné.

Nezdá se, že by typ stavové zprávy nebo její obsah měl význam. Byla původně přidána, protože zpráva DatabaseStore byla zpožděna o několik sekund; jelikož se store nyní odesílá okamžitě, možná by stavová zpráva mohla být eliminována.

## Úvod {#introduction}

Introduction klíče jsou doručovány prostřednictvím externího kanálu (network database), kde byly tradičně identické s router Hash až do vydání 0.9.47, ale od vydání 0.9.48 mohou být náhodné. Musí být použity při vytváření klíče relace. Pro nepřímou adresu musí peer nejprve kontaktovat relayhost a požádat jej o introduction k peeru známému na tomto relayhost pod daným tagem. Pokud je to možné, relayhost pošle zprávu adresovanému peeru s instrukcí, aby kontaktoval žádající peer, a také poskytne žádajícímu peeru IP adresu a port, na kterých se adresovaný peer nachází. Kromě toho musí peer navazující spojení již znát veřejné klíče peeru, ke kterému se připojuje (ale není nutné znát klíče jakéhokoli zprostředkujícího relay peer).

Nepřímé navázání relace prostřednictvím představení třetí stranou je nezbytné pro efektivní průchod NAT. Charlie, router za NAT nebo firewallem, který nepovoluje nevyžádané příchozí UDP pakety, nejprve kontaktuje několik peerů a některé z nich si vybere jako představitele. Každý z těchto peerů (Bob, Bill, Betty, atd.) poskytne Charliemu introduction tag - 4 bajtové náhodné číslo - které pak zveřejní jako metodu, jak ho kontaktovat. Alice, router který má Charlieho publikované kontaktní metody, nejprve pošle RelayRequest paket jednomu nebo více představitelům s žádostí, aby ji Charliemu představili (nabídne introduction tag k identifikaci Charlieho). Bob pak předá RelayIntro paket Charliemu obsahující Alicinu veřejnou IP adresu a číslo portu, poté pošle Alice zpět RelayResponse paket obsahující Charlieho veřejnou IP adresu a číslo portu. Když Charlie obdrží RelayIntro paket, pošle malý náhodný paket na Alicinu IP adresu a port (proděraví díru ve svém NAT/firewallu), a když Alice obdrží Bobův RelayResponse paket, začne nové úplné navázání relace se specifikovanou IP adresou a portem.

### Navázání spojení (nepřímé pomocí zprostředkovatele) {#establishIndirect}

Alice se nejprve připojí k introducer Bobovi, který přepošle požadavek Charliemu.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Po hole punch je relace navázána mezi Alice a Charliem stejně jako při přímém navázání.

### Poznámky k IPv6

IPv6 je podporováno od verze 0.9.8. Publikované adresy relay mohou být IPv4 nebo IPv6 a komunikace Alice-Bob může probíhat přes IPv4 nebo IPv6. Do verze 0.9.49 probíhá komunikace Bob-Charlie a Alice-Charlie pouze přes IPv4. Předávání pro IPv6 je podporováno od verze 0.9.50. Podrobnosti naleznete ve specifikaci.

Ačkoli byla specifikace změněna od verze 0.9.8, komunikace Alice-Bob přes IPv6 nebyla ve skutečnosti podporována až do verze 0.9.50. Dřívější verze Java routerů chybně publikovaly schopnost 'C' pro IPv6 adresy, i když ve skutečnosti nejednaly jako introducer přes IPv6. Proto by routery měly důvěřovat schopnosti 'C' u IPv6 adresy pouze v případě, že je verze routeru 0.9.50 nebo vyšší.

## Testování peerů {#peerTesting}

Automatizace kolaborativního testování dosažitelnosti pro peery je umožněna sekvencí PeerTest zpráv. Při správném provedení bude peer schopen určit svou vlastní dosažitelnost a může odpovídajícím způsobem aktualizovat své chování. Testovací proces je poměrně jednoduchý:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Každá ze zpráv PeerTest nese nonce identifikující samotnou testovací sérii, jak ji inicializovala Alice. Pokud Alice nedostane konkrétní zprávu, kterou očekává, bude ji odpovídajícím způsobem znovu odesílat, a na základě přijatých dat nebo chybějících zpráv pozná svou dosažitelnost. Různé koncové stavy, kterých může být dosaženo, jsou následující:

- Pokud neobdrží odpověď od Boba, bude přenos opakovat
  až do určitého počtu pokusů, ale pokud odpověď nikdy nedorazí,
  bude vědět, že její firewall nebo NAT je nějak špatně nakonfigurován
  a odmítá všechny příchozí UDP pakety, i když jsou přímou odpovědí na
  odchozí paket. Alternativně může být Bob nedostupný nebo není schopen
  přimět Charlieho k odpovědi.

- Pokud Alice neobdrží PeerTest zprávu s očekávaným nonce od třetí strany (Charlie), bude znovu přenášet svůj počáteční požadavek Bobovi až určitý počet krát, i kdyby již obdržela Bobovu odpověď. Pokud se Charlieho první zpráva stále nedostane, ale Bobova ano, ví, že je za NATem nebo firewallem, který odmítá nevyžádané pokusy o připojení a že přesměrování portů nefunguje správně (IP adresa a port, který Bob nabídl, by měl být přesměrován).

- Pokud Alice obdrží Bobovu PeerTest zprávu a obě Charlieovy
  PeerTest zprávy, ale uzavřené IP a čísla portů v Bobových
  a Charlieových druhých zprávách se neshodují, ví, že je
  za symetrickým NAT, který přepisuje všechny její odchozí pakety s
  různými 'from' porty pro každého kontaktovaného peera. Bude muset
  explicitně předat port a vždy mít tento port vystavený pro
  vzdálené připojení, ignorując další objevování portů.

- Pokud Alice obdrží Charlieho první zprávu, ale ne tu druhou,
  znovu odešle svou PeerTest zprávu Charliemu až určitý počet
  krát, ale pokud neobdrží odpověď, ví, že Charlie je buď
  zmatený nebo již není online.

Alice by měla vybrat Boba libovolně ze známých peerů, kteří se zdají být schopni účastnit se peer testů. Bob by zase měl vybrat Charlieho libovolně z peerů, které zná, kteří se zdají být schopni účastnit se peer testů a kteří jsou na jiné IP adrese než Bob i Alice. Pokud dojde k první chybové podmínce (Alice nedostane PeerTest zprávy od Boba), Alice se může rozhodnout označit nového peera jako Boba a zkusit to znovu s jiným nonce.

Alicin introdukční klíč je zahrnut ve všech PeerTest zprávách, takže Charlie ji může kontaktovat, aniž by znal jakékoli další informace. Od verze 0.9.15 musí mít Alice navázané spojení s Bobem, aby se zabránilo útokům typu spoofing. Alice nesmí mít navázané spojení s Charliem, aby byl peer test platný. Alice může následně navázat spojení s Charliem, ale není to vyžadováno.

### Poznámky k IPv6

Až do verze 0.9.26 je podporováno pouze testování IPv4 adres. Podporováno je pouze testování IPv4 adres. Proto musí veškerá komunikace Alice-Bob a Alice-Charlie probíhat přes IPv4. Komunikace Bob-Charlie však může probíhat přes IPv4 nebo IPv6. Adresa Alice, když je specifikována ve zprávě PeerTest, musí mít 4 bajty. Od verze 0.9.27 je podporováno testování IPv6 adres a komunikace Alice-Bob a Alice-Charlie může probíhat přes IPv6, pokud Bob a Charlie indikují podporu s možností 'B' ve své publikované IPv6 adrese. Podrobnosti viz [Proposal 126](/spec/proposals/126-ipv6-peer-testing).

Před vydáním verze 0.9.50 Alice pošle požadavek Bobovi pomocí existující relace přes transport (IPv4 nebo IPv6), který chce testovat. Když Bob obdrží požadavek od Alice přes IPv4, Bob musí vybrat Charlieho, který inzeruje IPv4 adresu. Když Bob obdrží požadavek od Alice přes IPv6, Bob musí vybrat Charlieho, který inzeruje IPv6 adresu. Skutečná komunikace Bob-Charlie může probíhat přes IPv4 nebo IPv6 (tj. nezávisle na typu adresy Alice).

Od verze 0.9.50, pokud je zpráva přes IPv6 pro IPv4 peer test, nebo (od verze 0.9.50) přes IPv4 pro IPv6 peer test, musí Alice zahrnout svou introdukční adresu a port.

Podrobnosti viz [Proposal 158](/spec/proposals/158).

## Přenosové okno, ACK a retransmise {#acks}

DATA zpráva může obsahovat ACK celých zpráv a částečné ACK jednotlivých fragmentů zprávy. Podrobnosti najdete v sekci data message na [stránce specifikace protokolu](/docs/legacy/ssu).

Podrobnosti strategií okenního mechanismu, potvrzování (ACK) a opětovného přenosu nejsou zde specifikovány. Pro aktuální implementaci se podívejte do Java kódu. Během fáze navazování spojení a pro testování peerů by routery měly implementovat exponenciální backoff pro opětovný přenos. Pro navázané spojení by routery měly implementovat nastavitelné přenosové okno, odhad RTT a timeout, podobně jako TCP nebo [streaming](/docs/api/streaming). Pro počáteční, minimální a maximální parametry se podívejte do kódu.

## Bezpečnost {#security}

UDP zdrojové adresy mohou být samozřejmě falšované. Kromě toho IP adresy a porty obsažené ve specifických SSU zprávách (RelayRequest, RelayResponse, RelayIntro, PeerTest) nemusí být legitimní. Také některé akce a odpovědi může být nutné omezit rychlostí.

Podrobnosti validace zde nejsou specifikovány. Implementátoři by měli přidat obranu tam, kde je to vhodné.

## Schopnosti uzlů {#capabilities}

Jedna nebo více capabilities může být publikována v možnosti "caps". Capabilities mohou být v libovolném pořadí, ale "BC46" je doporučené pořadí pro konzistenci napříč implementacemi.

**B** : Pokud adresa partnera obsahuje schopnost 'B', znamená to, že jsou ochotni a schopni účastnit se testování partnerů jako 'Bob' nebo 'Charlie'. Do verze 0.9.26 nebylo testování partnerů podporováno pro IPv6 adresy a schopnost 'B', pokud byla přítomna u IPv6 adresy, musela být ignorována. Od verze 0.9.27 je testování partnerů podporováno pro IPv6 adresy a přítomnost nebo absence schopnosti 'B' u IPv6 adresy indikuje skutečnou podporu (nebo její nedostatek).

**C** : Pokud adresa peer obsahuje schopnost 'C', znamená to, že je ochoten a schopen sloužit jako introducer přes tuto adresu - sloužit jako introducer Bob pro jinak nedosažitelného Charlie. Před vydáním 0.9.50 router v Javě nesprávně publikovaly schopnost 'C' pro IPv6 adresy, i když IPv6 introducer nebyly plně implementovány. Proto by router měly předpokládat, že verze před 0.9.50 nemohou fungovat jako introducer přes IPv6, i když je schopnost 'C' inzerována.

**4** : Od verze 0.9.50 označuje schopnost odchozího IPv4 připojení. Pokud je IP publikována v poli host, tato schopnost není nutná. Pokud se jedná o adresu s introducery pro IPv4 představování, mělo by být zahrnuto '4'. Pokud je router skrytý, '4' a '6' mohou být zkombinována v jedné adrese.

**6** : Od verze 0.9.50 označuje schopnost odchozího IPv6. Pokud je IP publikována v poli host, tato schopnost není nutná. Pokud se jedná o adresu s introducery pro IPv6 představení, '6' by mělo být zahrnuto (momentálně není podporováno). Pokud je router skrytý, '4' a '6' mohou být kombinovány v jediné adrese.

# Budoucí práce {#future}

Poznámka: Tyto problémy budou řešeny při vývoji SSU2.

- Analýza současného výkonu SSU, včetně posouzení úprav velikosti okna a dalších parametrů, a úprava implementace protokolu pro zlepšení výkonu, je tématem pro budoucí práci.

- Současná implementace opakovaně odesílá potvrzení pro stejné pakety,
  což zbytečně zvyšuje režii.

- Výchozí malá MTU hodnota 620 by měla být analyzována a případně zvýšena.
  Současná strategie úpravy MTU by měla být vyhodnocena.
  Vejde se streaming lib paket o velikosti 1730 bajtů do 3 malých SSU paketů? Pravděpodobně ne.

- Protokol by měl být rozšířen o výměnu MTU během nastavování.

- Rekeying není v současnosti implementován a nikdy nebude.

- Potenciální použití polí 'challenge' v RelayIntro a RelayResponse,
  a použití pole padding v SessionRequest a SessionCreated, není dokumentováno.

- Sada pevných velikostí paketů může být vhodná pro další skrytí fragmentace dat před externími útočníky, ale tunnel, garlic a end-to-end padding by mělo být dostatečné pro většinu potřeb až do té doby.

- Časy přihlášení v SessionCreated a SessionConfirmed se zdají být nepoužité nebo neověřené.

# Specifikace {#spec}

[Nyní na stránce specifikace SSU](/docs/legacy/ssu).
