---
title: "UDP Trackery"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Zavřeno"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Stav

Schváleno při kontrole 2025-06-24. Specifikace je na [UDP specification](/docs/specs/udp-bittorrent-announces/). Implementováno v zzzot 0.20.0-beta2. Implementováno v i2psnark od API 0.9.67. Zkontrolujte dokumentaci dalších implementací pro stav.

## Přehled

Tento návrh je pro implementaci UDP trackerů v I2P.

### Change History

Předběžný návrh pro UDP trackery v I2P byl zveřejněn na naší [stránce specifikace bittorrent](/docs/applications/bittorrent/) v květnu 2014; tento návrh předcházel našemu formálnímu procesu návrhů a nikdy nebyl implementován. Tento návrh byl vytvořen začátkem roku 2022 a zjednodušuje verzi z roku 2014.

Jelikož tento návrh spoléhá na odpověditelné datagramy, byl pozastaven, jakmile jsme začali pracovat na [návrhu Datagram2](/proposals/163-datagram2/) na začátku roku 2023. Tento návrh byl schválen v dubnu 2025.

Verze tohoto návrhu z roku 2023 specifikovala dva režimy, "kompatibilní" a "rychlý". Další analýza odhalila, že rychlý režim by byl nezabezpečený a také by byl neefektivní pro klienty s velkým počtem torrentů. Navíc BiglyBT vyjádřil preferenci pro kompatibilní režim. Tento režim bude jednodušší implementovat pro jakýkoli tracker nebo klient podporující standardní [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Zatímco režim kompatibility je komplexnější na implementaci od nuly na straně klienta, máme pro něj předběžný kód, který jsme začali vyvíjet v roce 2023.

Proto byla současná verze zde dále zjednodušena pro odstranění rychlého režimu a odstranění termínu "kompatibilita". Současná verze přechází na nový formát Datagram2 a přidává odkazy na protokol UDP announce rozšíření [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Také je do odpovědi na připojení přidáno pole životnosti ID připojení, aby se rozšířily výkonnostní zisky tohoto protokolu.

## Motivation

Jak se uživatelská základna obecně a počet uživatelů bittorrentu konkrétně nadále zvyšuje, potřebujeme učinit trackery a oznámení efektivnějšími, aby trackery nebyly přetížené.

Bittorrent navrhl UDP trackery v BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) v roce 2008 a drtivá většina trackerů na clearnetu nyní používá pouze UDP.

Je obtížné vypočítat úspory šířky pásma u datagramů oproti streamovacímu protokolu. Odpověditelnýá žádost má přibližně stejnou velikost jako streamovací SYN, ale payload je asi o 500 bajtů menší, protože HTTP GET má obrovský 600bajtový řetězec URL parametrů. Samotná odpověď je mnohem menší než streamovací SYN ACK, což poskytuje významné snížení odchozího provozu trackeru.

Kromě toho by mělo dojít k implementačně specifickým úsporám paměti, protože datagramy vyžadují mnohem méně stavu v paměti než streamovací spojení.

Post-kvantové šifrování a podpisy podle návrhu v [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) podstatně zvýší režii šifrovaných a podepsaných struktur, včetně destinací, leaseSets, streaming SYN a SYN ACK. Je důležité tuto režii minimalizovat všude, kde je to možné, než bude PQ kryptografie v I2P přijata.

## Motivace

Tento návrh používá repliable datagram2, repliable datagram3 a raw datagramy, jak jsou definovány v [/docs/api/datagrams/](/docs/api/datagrams/). Datagram2 a Datagram3 jsou nové varianty repliable datagramů, definované v Návrhu 163 [/proposals/163-datagram2/](/proposals/163-datagram2/). Datagram2 přidává ochranu proti replay útokům a podporu offline podpisů. Datagram3 je menší než starý formát datagramu, ale bez autentifikace.

### BEP 15

Pro referenci je tok zpráv definovaný v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) následující:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
Fáze připojení je vyžadována pro zabránění IP address spoofingu. Tracker vrací connection ID, které klient používá v následujících announce zprávách. Toto connection ID vyprší ve výchozím nastavení za jednu minutu u klienta a za dvě minuty u trackeru.

I2P bude používat stejný tok zpráv jako BEP 15, pro snadné přijetí ve stávajících kódových základnách klientů schopných UDP: kvůli efektivitě a z bezpečnostních důvodů diskutovaných níže:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
Toto potenciálně poskytuje značné úspory šířky pásma oproti streamovacím (TCP) oznámením. Zatímco Datagram2 má přibližně stejnou velikost jako streamovací SYN, surová odpověď je mnohem menší než streamovací SYN ACK. Následující požadavky používají Datagram3 a následující odpovědi jsou surové.

Požadavky na announce jsou Datagram3, takže tracker nemusí udržovat velkou mapovací tabulku ID připojení k announce cíli nebo hash. Místo toho může tracker generovat ID připojení kryptograficky z hash odesílatele, aktuálního časového razítka (založeného na určitém intervalu) a tajné hodnoty. Když je přijat požadavek na announce, tracker validuje ID připojení a poté použije hash odesílatele Datagram3 jako cíl pro odeslání.

### Historie změn

Pro integrovanou aplikaci (router a klient v jednom procesu, například i2psnark a ZzzOT Java plugin), nebo pro aplikaci založenou na I2CP (například BiglyBT), by mělo být jednoduché implementovat a směrovat streaming a datagram provoz odděleně. ZzzOT a i2psnark by měly být první tracker a klient, které tento návrh implementují.

Neintegrované trackery a klienti jsou probrány níže.

#### Trackers

Existují čtyři známé implementace I2P trackerů:

- zzzot, integrovaný Java router plugin, běžící na opentracker.dg2.i2p a několika dalších
- tracker2.postman.i2p, běžící pravděpodobně za Java routerem a HTTP Server tunelem
- Starý C opentracker, portovaný uživatelem zzz, s komentovanou UDP podporou
- Nový C opentracker, portovaný uživatelem r4sas, běžící na opentracker.r4sas.i2p a možná dalších,
  běžící pravděpodobně za i2pd routerem a HTTP Server tunelem

Pro externí tracker aplikaci, která v současnosti používá HTTP server tunnel pro příjem announce požadavků, by mohla být implementace poměrně obtížná. Mohl by být vyvinut specializovaný tunnel pro překlad datagramů na lokální HTTP požadavky/odpovědi. Nebo by mohl být navržen specializovaný tunnel, který zpracovává jak HTTP požadavky, tak datagramy a který by předával datagramy externímu procesu. Tato návrhová rozhodnutí budou silně záviset na konkrétních implementacích routeru a trackeru a jsou mimo rozsah tohoto návrhu.

#### Clients

Externí SAM-based torrent klienti jako qbittorrent a další klienti založené na libtorrent by vyžadovali [SAM v3.3](/docs/api/samv3/), které není podporováno v i2pd. To je také vyžadováno pro podporu DHT a je dostatečně složité na to, aby to žádný známý SAM torrent klient neimplementoval. Žádné SAM-based implementace tohoto návrhu se neočekávají v blízké době.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) specifikuje, že connection ID vyprší za jednu minutu u klienta a za dvě minuty u trackeru. Není to konfigurovatelné. To omezuje potenciální zisky v efektivitě, pokud by klienti nesdružovali announces, aby je všechny provedli v rámci jednominutového okna. i2psnark v současnosti announces nesdružuje; rozkládá je v čase, aby se vyhnul nárazům provozu. Pokročilí uživatelé údajně provozují tisíce torrentů najednou a soustředění tolika announces do jedné minuty není realistické.

Zde navrhujeme rozšířit odpověď připojení o volitelné pole životnosti připojení. Výchozí hodnota, pokud není přítomna, je jedna minuta. V opačném případě bude klientem použita životnost specifikovaná v sekundách a tracker bude udržovat ID připojení o jednu minutu déle.

### Compatibility with BEP 15

Tento design zachovává kompatibilitu s [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) co nejvíce, aby omezil změny požadované v existujících klientech a trackerech.

Jedinou požadovanou změnou je formát informací o peerech v announce response. Přidání pole lifetime v connect response není povinné, ale je důrazně doporučeno kvůli efektivitě, jak je vysvětleno výše.

### BEP 15

Důležitým cílem UDP announce protokolu je zabránit padělání adres. Klient musí skutečně existovat a obsahovat skutečný leaseset. Musí mít příchozí tunely pro příjem Connect Response. Tyto tunely by mohly být zero-hop a vybudované okamžitě, ale to by odhalilo tvůrce. Tento protokol tohoto cíle dosahuje.

### Podpora Tracker/Client

- Tento návrh nepodporuje blinded destinations,
  ale může být rozšířen, aby tak činil. Viz níže.

## Návrh

### Protocols and Ports

Repliable Datagram2 používá I2CP protokol 19; repliable Datagram3 používá I2CP protokol 20; raw datagramy používají I2CP protokol 18. Požadavky mohou být Datagram2 nebo Datagram3. Odpovědi jsou vždy raw. Starší repliable datagram ("Datagram1") formát používající I2CP protokol 17 NESMÍ být používán pro požadavky nebo odpovědi; tyto musí být zahozeny, pokud jsou přijaty na request/reply portech. Poznámka: Datagram1 protokol 17 je stále používán pro DHT protokol.

Požadavky používají I2CP "to port" z announce URL; viz níže. "From port" požadavku je zvolen klientem, ale měl by být nenulový a jiný port než ty používané DHT, aby mohly být odpovědi snadno klasifikovány. Trackery by měly odmítat požadavky přijaté na nesprávném portu.

Odpovědi používají I2CP "to port" z požadavku. "From port" požadavku je "to port" z požadavku.

### Announce URL

Formát announce URL není specifikován v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), ale stejně jako na clearnetu mají UDP announce URL formu "udp://host:port/path". Cesta je ignorována a může být prázdná, ale na clearnetu je typicky "/announce". Část :port by měla být vždy přítomna, avšak pokud je část ":port" vynechána, použij výchozí I2CP port 6969, protože to je běžný port na clearnetu. Mohou být také připojeny cgi parametry &a=b&c=d, ty mohou být zpracovány a poskytnuty v announce požadavku, viz [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Pokud nejsou žádné parametry nebo cesta, koncové / může být také vynecháno, jak je naznačeno v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Životnost připojení

Všechny hodnoty jsou odesílány v síťovém bajtovém pořadí (big endian). Neočekávejte, že pakety budou mít přesně určitou velikost. Budoucí rozšíření by mohla zvětšit velikost paketů.

#### Connect Request

Klient ke trackeru. 16 bajtů. Musí být repliable Datagram2. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker ke klientovi. 16 nebo 18 bajtů. Musí být raw. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) kromě níže uvedených poznámek.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Odpověď MUSÍ být odeslána na I2CP "to port", který byl přijat jako "from port" požadavku.

Pole lifetime je volitelné a udává životnost connection_id klienta v sekundách. Výchozí hodnota je 60 a minimum, pokud je specifikováno, je 60. Maximum je 65535 nebo přibližně 18 hodin. Tracker by měl udržovat connection_id o 60 sekund déle než je životnost klienta.

#### Announce Request

Klient na tracker. Minimálně 98 bajtů. Musí být repliable Datagram3. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) kromě případů uvedených níže.

connection_id je takové, jak bylo přijato v odpovědi connect.

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Změny oproti [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- klíč je ignorován
- port je pravděpodobně ignorován
- Sekce options, pokud je přítomna, je definována v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Odpověď MUSÍ být odeslána na I2CP "to port", který byl přijat jako "from port" požadavku. Nepoužívejte port z announce požadavku.

#### Announce Response

Tracker ke klientovi. Minimálně 20 bajtů. Musí být surový. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) kromě níže uvedených poznámek.

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
Změny oproti [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Namísto 6-bajtové IPv4+port nebo 18-bajtové IPv6+port vracíme
  násobek 32-bajtových "kompaktních odpovědí" s binárními SHA-256 hashy peerů.
  Stejně jako u TCP kompaktních odpovědí nezahrnujeme port.

Odpověď MUSÍ být odeslána na I2CP "to port", který byl přijat jako "from port" požadavku. Nepoužívejte port z announce požadavku.

I2P datagramy mají velmi velkou maximální velikost přibližně 64 KB; nicméně pro spolehlivé doručení by se mělo vyhnout datagramům větším než 4 KB. Pro efektivní využití šířky pásma by trackery pravděpodobně měly omezit maximální počet peerů na přibližně 50, což odpovídá přibližně 1600 bajtovému paketu před režijními náklady na různých vrstvách a mělo by se vejít do limitu dvou-tunnel-message payload po fragmentaci.

Stejně jako v BEP 15, není zde uveden počet adres peerů (IP/port pro BEP 15, zde hashe), které následují. Ačkoliv to není v BEP 15 zamýšleno, mohl by být definován značkovač konce peerů obsahující samé nuly, který by indikoval, že informace o peerech jsou kompletní a následují nějaká rozšiřující data.

Aby bylo rozšíření možné v budoucnosti, klienti by měli ignorovat 32-bajtový hash složený ze samých nul a jakákoli data, která následují. Trackery by měly odmítat oznámení od hash složeného ze samých nul, ačkoli tento hash je již zakázán Java routery.

#### Scrape

Scrape request/response z [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) není tímto návrhem vyžadován, ale může být implementován podle potřeby, nejsou nutné žádné změny. Klient musí nejprve získat connection ID. Scrape request je vždy repliable Datagram3. Scrape response je vždy raw.

#### Trackery

Tracker ke klientovi. Minimálně 8 bajtů (pokud je zpráva prázdná). Musí být raw. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Rozšiřující bity nebo pole verze nejsou zahrnuty. Klienti a trackery by neměli předpokládat, že pakety budou mít určitou velikost. Tímto způsobem lze přidat další pole bez narušení kompatibility. Pokud je to vyžadováno, doporučuje se formát rozšíření definovaný v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Odpověď na připojení je upravena tak, aby přidala volitelnou životnost ID připojení.

Pokud je vyžadována podpora blinded destination, můžeme buď přidat blinded 35-bajtovou adresu na konec announce požadavku, nebo požadovat blinded hashe v odpovědích pomocí formátu [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parametry budou určeny později). Sada blinded 35-bajtových peer adres by mohla být přidána na konec announce odpovědi po 32-bajtovém hashi sestávajícím ze samých nul.

## Implementation guidelines

Viz sekci návrhu výše pro diskusi výzev pro neintegrované, non-I2CP klienty a trackery.

### Kompatibilita s BEP 15

Pro daný hostname trackeru by měl klient upřednostnit UDP před HTTP URL a neměl by oznamovat na obě.

Klienti s existující podporou BEP 15 by měli vyžadovat pouze malé úpravy.

Pokud klient podporuje DHT nebo jiné datagramové protokoly, měl by pravděpodobně vybrat jiný port jako „zdrojový port" požadavku, aby se odpovědi vrátily na tento port a nepomíchaly se s DHT zprávami. Klient přijímá pouze surové datagramy jako odpovědi. Trackery nikdy nepošlou klientovi odpověditelný datagram2.

Klienti s výchozím seznamem opentrackerů by měli aktualizovat seznam a přidat UDP URL poté, co je známo, že známé opentrackery podporují UDP.

Klienti mohou nebo nemusí implementovat opakované odesílání požadavků. Opakovaná odesílání, pokud jsou implementována, by měla používat počáteční timeout nejméně 15 sekund a zdvojnásobit timeout pro každé opakované odeslání (exponenciální backoff).

Klienti se musí stáhnout po obdržení chybové odpovědi.

### Analýza bezpečnosti

Trackery s existující podporou BEP 15 by měly vyžadovat pouze malé úpravy. Tento návrh se liší od návrhu z roku 2014 v tom, že tracker musí podporovat příjem repliable datagram2 a datagram3 na stejném portu.

Pro minimalizaci požadavků na zdroje trackeru je tento protokol navržen tak, aby eliminoval jakýkoli požadavek na to, aby tracker ukládal mapování hashů klientů na ID připojení pro pozdější validaci. To je možné, protože paket žádosti o oznámení je odpovídatelný Datagram3 paket, takže obsahuje hash odesílatele.

Doporučená implementace je:

- Definovat současnou epochu jako aktuální čas s rozlišením doby života spojení,
  ``epoch = now / lifetime``.
- Definovat kryptografickou hashovací funkci ``H(secret, clienthash, epoch)``, která generuje
  8bajtový výstup.
- Vygenerovat náhodnou konstantu secret použitou pro všechna spojení.
- Pro connect odpovědi vygenerovat ``connection_id = H(secret,  clienthash, epoch)``
- Pro announce požadavky validovat přijaté connection ID v současné epoše ověřením
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Stávající klienti nepodporují UDP announce URL a ignorují je.

Stávající trackery nepodporují příjem odpověditelných nebo surových datagramů, tyto budou zahozeny.

Tento návrh je zcela volitelný. Ani klienti, ani trackery nejsou povinny jej kdykoli implementovat.

## Rollout

První implementace se očekávají v ZzzOT a i2psnark. Budou použity pro testování a ověření tohoto návrhu.

Další implementace budou následovat podle potřeby po dokončení testování a ověření.
