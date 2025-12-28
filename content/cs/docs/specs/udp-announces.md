---
title: "UDP oznámení BitTorrentu"
description: "Specifikace protokolu pro oznámení trackeru BitTorrentu na bázi UDP v I2P"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Tato specifikace popisuje protokol pro UDP oznamování BitTorrentu v I2P. Celkovou specifikaci BitTorrentu v I2P najdete v [dokumentaci k BitTorrentu přes I2P](/docs/applications/bittorrent/). Pro pozadí a další informace o vývoji této specifikace viz [Návrh 160](/proposals/160-udp-trackers/).

Tento protokol byl formálně schválen 24. června 2025 a implementován v I2P verzi 2.10.0 (API 0.9.67), vydané 8. září 2025. Podpora UDP trackeru je v síti I2P aktuálně v provozu s několika produkčními trackery a plnou podporou klienta i2psnark.

## Návrh

Tato specifikace používá repliable datagram2, repliable datagram3 a surové datagramy, jak jsou definovány v [I2P Datagram Specification](/docs/api/datagrams/). Datagram2 a Datagram3 jsou variantami repliable datagrams (datagramů s možností odpovědi), definované v [Proposal 163](/proposals/163-datagram2/). Datagram2 přidává odolnost vůči replay útokům a podporu offline podpisů. Datagram3 je menší než starý formát datagramu, ale bez autentizace.

### BEP 15

Pro informaci je tok zpráv definovaný v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) následující:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
Fáze připojení je nutná k zabránění podvržení IP adresy. Tracker vrátí identifikátor spojení, který klient používá v následujících announces (oznámeních). Tento identifikátor spojení ve výchozím nastavení vyprší za jednu minutu u klienta a za dvě minuty u trackeru.

I2P používá stejný tok zpráv jako BEP 15, pro usnadnění integrace do stávajících kódových základen klientů podporujících UDP, kvůli efektivitě a také z bezpečnostních důvodů rozebraných níže:

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
To potenciálně poskytuje výraznou úsporu šířky pásma oproti oznámením přes streaming (TCP). Zatímco Datagram2 má zhruba stejnou velikost jako streaming SYN, odpověď raw (surová) je mnohem menší než streaming SYN ACK. Následné požadavky používají Datagram3 a následné odpovědi jsou raw.

Požadavky announce jsou typu Datagram3, takže tracker (sledovací server) nemusí udržovat velkou mapovací tabulku, která by přiřazovala ID připojení k cíli announce nebo k hashi. Místo toho může tracker kryptograficky generovat ID připojení z hashe odesílatele, aktuálního časového razítka (na základě určitého intervalu) a tajné hodnoty. Když je přijat požadavek announce, tracker ověří ID připojení a poté použije hash odesílatele z Datagram3 jako cíl odeslání.

### Doba trvání spojení

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) specifikuje, že identifikátor spojení vyprší za jednu minutu u klienta a za dvě minuty u trackeru. Není konfigurovatelný. To omezuje potenciální přínosy z hlediska efektivity, ledaže by klienti dávkovali announces (požadavky na tracker) tak, aby je všechny odeslali v rámci jednominutového okna. i2psnark v současnosti announces nedávkuje; rozprostírá je v čase, aby se předešlo špičkám provozu. Uvádí se, že pokročilí uživatelé provozují naráz tisíce torrentů a poslat tolik announces během jedné minuty není realistické.

Zde navrhujeme rozšířit connect response (odpověď na požadavek connect) o volitelné pole s dobou trvání spojení. Výchozí hodnota, pokud není uvedeno, je jedna minuta. V opačném případě klient použije zadanou dobu trvání v sekundách a tracker bude udržovat ID spojení ještě o jednu minutu déle.

### Kompatibilita s BEP 15

Tento návrh zachovává kompatibilitu s [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) v co největší možné míře, aby se omezily změny nutné v existujících klientech a trackerech.

Jedinou povinnou změnou je formát informací o peerech v announce response (odpovědi announce). Přidání pole lifetime v connect response (odpovědi connect) není povinné, ale je důrazně doporučeno kvůli efektivitě, jak je vysvětleno výše.

### Analýza zabezpečení

Důležitým cílem oznamovacího protokolu UDP je zabránit podvržení adresy. Klient musí skutečně existovat a zahrnout skutečný leaseSet. Musí mít příchozí tunnels, aby mohl přijmout Connect Response. Tyto tunnels mohou být zero-hop (bez prostředníků) a sestavené okamžitě, ale to by odhalilo tvůrce. Tento protokol tohoto cíle dosahuje.

### Problémy

Tento protokol nepodporuje blinded destinations (oslepené destinace v I2P), ale může být rozšířen tak, aby je podporoval. Viz níže.

## Specifikace

### Protokoly a porty

Datagram s možností odpovědi Datagram2 používá protokol I2CP 19; datagram s možností odpovědi Datagram3 používá protokol I2CP 20; surové datagramy používají protokol I2CP 18. Požadavky mohou být Datagram2 nebo Datagram3. Odpovědi jsou vždy surové. Starší formát datagramu s možností odpovědi ("Datagram1") používající protokol I2CP 17 se NESMÍ používat pro požadavky ani odpovědi; pokud jsou přijaty na portech pro požadavky/odpovědi, musí být zahazovány. Všimněte si, že Datagram1 (protokol I2CP 17) se stále používá pro protokol DHT (distribuovaná hashovací tabulka).

Požadavky používají I2CP „to port“ z oznamovací URL; viz níže. „From port“ u požadavku volí klient, ale měl by být nenulový a odlišný od portů používaných DHT, aby bylo možné odpovědi snadno klasifikovat. Trackery by měly odmítat požadavky přijaté na nesprávném portu.

Odpovědi používají I2CP "to port" z požadavku. "From port" v odpovědi je "to port" z požadavku.

### Oznamovací URL

Formát announce URL (oznamovací URL) není specifikován v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), ale stejně jako na clearnet (veřejný internet), mají UDP announce URL tvar "udp://host:port/path". Cesta se ignoruje a může být prázdná, ale na clearnet je obvykle "/announce". Část :port by měla být vždy přítomna; pokud je však část ":port" vynechána, použijte výchozí port I2CP 6969, jelikož to je běžný port na clearnet. Mohou být také připojeny parametry CGI &a=b&c=d; ty lze zpracovat a předat v požadavku announce, viz [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Pokud nejsou žádné parametry ani cesta, koncové / může být také vynecháno, jak je naznačeno v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Formáty datagramů

Všechny hodnoty jsou odesílány v síťovém pořadí bajtů (big endian). Neočekávejte, že pakety budou mít přesně určitou velikost. Budoucí rozšíření mohou velikost paketů zvětšit.

#### Žádost o připojení

Od klienta k trackeru. 16 bajtů. Musí jít o Datagram2 (druh datagramu v I2P) umožňující odpověď. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Odpověď na připojení

Od trackeru ke klientovi. 16 nebo 18 bajtů. Musí být v surové podobě. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), s výjimkou toho, co je uvedeno níže.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Odpověď MUSÍ být odeslána na I2CP "to port", který byl v požadavku přijat jako "from port".

Pole lifetime je nepovinné a udává dobu životnosti connection_id klienta v sekundách. Výchozí hodnota je 60 a minimální hodnota, pokud je zadána, je 60. Maximální hodnota je 65535, tedy přibližně 18 hodin. Tracker by měl udržovat connection_id o 60 sekund déle, než je doba životnosti klienta.

#### Požadavek na oznámení

Od klienta k trackeru. Minimálně 98 bajtů. Musí být datagram Datagram3 s možností odpovědi. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), pokud není uvedeno jinak níže.

connection_id je stejné, jako bylo přijato v odpovědi na připojení.

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
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Změny oproti [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- klíč je ignorován
- IP adresa se nepoužívá
- port se pravděpodobně ignoruje, ale musí být stejný jako I2CP from port
- sekce options, pokud je přítomna, je definována v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Odpověď MUSÍ být odeslána na I2CP "to port", který byl přijat jako "from port" v požadavku. Nepoužívejte port z announce request (oznamovacího požadavku).

#### Odpověď na oznámení

Z trackeru ke klientovi. Minimálně 20 bajtů. Musí být raw (surová binární data). Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) s výjimkami uvedenými níže.

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

- Namísto 6bajtového IPv4+portu nebo 18bajtového IPv6+portu vracíme data v podobě násobku 32bajtových "compact responses" obsahujících binární hashe peerů (SHA-256). Stejně jako u TCP compact responses port neuvádíme.

Odpověď MUSÍ být odeslána na I2CP „to port“, který byl v požadavku přijat jako „from port“. Nepoužívejte port z oznamovacího požadavku.

I2P datagramy mají velmi velkou maximální velikost kolem 64 KB; pro spolehlivé doručení by se však mělo vyhnout datagramům větším než 4 KB. Pro efektivní využití šířky pásma by trackery měly pravděpodobně omezit maximální počet peerů na asi 50, což odpovídá přibližně paketu o velikosti 1600 bajtů před režií na různých vrstvách, a po fragmentaci by se měl vejít do limitu užitečných dat dvou zpráv přenášených přes tunnel.

Stejně jako v BEP 15 zde není zahrnut počet následujících adres peerů (u BEP 15 IP/port, zde hashe). Ačkoli s tím BEP 15 nepočítá, bylo by možné definovat značku konce seznamu peerů složenou ze samých nul, která by signalizovala, že informace o peerech jsou úplné a že dále následují nějaká data rozšíření.

Aby bylo možné případné rozšíření v budoucnu, klienti by měli ignorovat 32bajtový hash složený samými nulami a veškerá následující data. Trackery by měly odmítat ohlášení pocházející z hashe složeného samými nulami, ačkoli tento hash už Java routers zakazují.

#### Sběr dat

Požadavek a odpověď scrape (operace trackeru pro získání souhrnných statistik o torrentu) podle [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) nejsou v této specifikaci povinné, ale lze je případně implementovat bez jakýchkoli změn. Klient musí nejprve získat ID připojení. Požadavek scrape je vždy repliable (na který lze odpovědět) Datagram3. Odpověď scrape je vždy raw (bez návratové adresy).

#### Chybová odpověď

Z trackeru ke klientovi. Minimálně 8 bajtů (pokud je zpráva prázdná). Musí být v surové podobě. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Rozšíření

Rozšiřující bity ani pole verze nejsou zahrnuty. Klienti a trackery by neměli předpokládat, že pakety mají určitou velikost. Tímto způsobem lze přidávat další pole, aniž by došlo k narušení kompatibility. V případě potřeby se doporučuje formát rozšíření definovaný v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Odpověď na connect je upravena tak, aby obsahovala volitelnou dobu platnosti Connection ID (identifikátoru spojení).

Pokud je vyžadována podpora blinded destination (kryptograficky „zaslepeného“ cíle), můžeme buď přidat zaslepenou 35bajtovou adresu na konec požadavku announce, nebo v odpovědích požadovat zaslepené hashe, a to ve formátu [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parametry budou upřesněny). Množinu zaslepených 35bajtových adres peerů lze přidat na konec odpovědi announce, za 32bajtovým hashem samých nul.

## Pokyny k implementaci

Viz výše uvedenou sekci Design pro diskusi o výzvách pro neintegrované, ne-I2CP klienty a trackery.

### Klienti

Pro daný název hostitele trackeru by měl klient upřednostnit UDP před HTTP URL a neměl by se ohlašovat oběma současně.

Klienti se stávající podporou BEP 15 by měli vyžadovat jen drobné úpravy.

Pokud klient podporuje DHT (distribuovaná hašovací tabulka) nebo jiné datagramové protokoly, měl by pravděpodobně zvolit jiný port jako „from port“ v požadavku, aby se odpovědi vracely na tento port a nemísily se se zprávami DHT. Klient jako odpovědi přijímá pouze surové datagramy. Trackery nikdy nepošlou klientovi repliable datagram2 (datagram verze 2, na který lze přímo odpovědět).

Klienti s výchozím seznamem opentrackers (veřejné trackery) by měli aktualizovat seznam a přidat UDP URL, jakmile je u známých opentrackers potvrzena podpora UDP.

Klienti mohou, ale nemusí implementovat retransmisi požadavků. Retransmise, jsou-li implementovány, by měly používat počáteční časový limit alespoň 15 sekund a pro každou retransmisi časový limit zdvojnásobit (exponenciální backoff).

Klienti musí po obdržení chybové odpovědi provést backoff (tj. dočasně vyčkat a snížit frekvenci opakování požadavků).

### Trackery

Trackery se stávající podporou BEP 15 by měly vyžadovat pouze drobné úpravy. Tato specifikace se liší od návrhu z roku 2014 tím, že tracker musí podporovat příjem repliable (s možností přímé odpovědi) datagram2 a datagram3 na stejném portu.

Aby se minimalizovaly nároky trackeru (sledovací server) na prostředky, je tento protokol navržen tak, aby odstranil jakoukoli potřebu, aby tracker ukládal mapování hashů klientů na ID připojení pro pozdější ověření. To je možné, protože paket požadavku announce je paket Datagram3 s možností odpovědi, takže obsahuje hash odesílatele.

Doporučená implementace je:

- Definujte aktuální epochu jako aktuální čas s rozlišením daným životností připojení, `epoch = now / lifetime`.
- Definujte kryptografickou hashovací funkci `H(secret, clienthash, epoch)`, která generuje 8bajtový výstup.
- Vygenerujte náhodnou konstantní tajnou hodnotu používanou pro všechna připojení.
- Pro odpovědi na připojení vygenerujte `connection_id = H(secret, clienthash, epoch)`
- Pro požadavky announce validujte obdržené ID připojení v aktuální epoše tak, že ověříte, zda `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Stav nasazení

Tento protokol byl schválen 24. června 2025 a od září 2025 je v síti I2P plně provozuschopný.

### Aktuální implementace

**i2psnark**: Plná podpora pro UDP tracker (server pro sledování peerů přes UDP) je zahrnuta ve verzi I2P 2.10.0 (API 0.9.67), vydané 8. září 2025. Všechny instalace I2P počínaje touto verzí zahrnují podporu UDP trackeru ve výchozím nastavení.

**zzzot tracker**: Verze 0.20.0-beta2 a novější podporují oznamování přes UDP. K říjnu 2025 jsou v provozu následující produkční trackery: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Poznámky ke kompatibilitě klientů

**Omezení SAM v3.3**: Externí klienti BitTorrentu používající SAM (Simple Anonymous Messaging) vyžadují podporu SAM v3.3 pro Datagram2/3. Tato podpora je k dispozici v Java I2P, ale aktuálně není podporována v i2pd (implementace I2P v C++), což může omezit přijetí u klientů založených na libtorrentu, jako je qBittorrent.

**Klienti I2CP**: Klienti používající přímo I2CP (např. BiglyBT) mohou implementovat podporu UDP trackeru bez omezení SAM.

## Reference

- **[BEP15]**: [Protokol UDP trackeru BitTorrentu](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Rozšíření protokolu UDP trackeru](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Specifikace datagramů I2P](/docs/api/datagrams/)
- **[Prop160]**: [Návrh UDP trackerů](/proposals/160-udp-trackers/)
- **[Prop163]**: [Návrh Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent přes I2P](/docs/applications/bittorrent/)
