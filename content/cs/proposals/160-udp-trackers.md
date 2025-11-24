```markdown
---
title: "UDP Trackery"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Stav

Schváleno při revizi 2025-06-24.
Specifikace je na [UDP specification](/en/docs/spec/udp-bittorrent-announces/).
Implementováno v zzzot 0.20.0-beta2.
Implementováno v i2psnark od API 0.9.67.
Prozkoumejte dokumentaci jiných implementací pro stav.


## Přehled

Tento návrh je pro implementaci UDP trackerů v I2P.


### Historie změn

Předběžný návrh pro UDP trackery v I2P byl zveřejněn na naší stránce specifikací bittorrent [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
v květnu 2014; to předcházelo našemu formálnímu procesu návrhů a nikdy nebyl implementován.
Tento návrh byl vytvořen na začátku roku 2022 a zjednodušuje verzi z roku 2014.

Protože tento návrh závisí na odpovědných datagramech, byl pozdržen, jakmile jsme
začali pracovat na návrhu Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) na začátku roku 2023.
Tento návrh byl schválen v dubnu 2025.

Verze tohoto návrhu z roku 2023 specifikovala dva režimy, "kompatibilitu" a "rychlý".
Další analýza ukázala, že rychlý režim by byl nebezpečný a navíc
by byl neefektivní pro klienty s velkým počtem torrentů.
Dále BiglyBT vyjádřil preferenci pro režim kompatibility.
Tento režim bude snadnější implementovat pro jakýkoli tracker nebo klient podporující
standard [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Ačkoli je režim kompatibility složitější implementovat od začátku
na straně klienta, máme již předběžný kód, který začal v roce 2023.

Proto je současná verze zde dále zjednodušena tím, že odstraní rychlý režim
a odstraní termín "kompatibilita". Současná verze přechází
k novému formátu Datagram2 a přidává odkazy na protokol oznámení UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Do odpovědi o spojení je také přidáno pole s dobou životnosti ID spojení,
pro rozšíření efektivity tohoto protokolu.


## Motivace

Jak se uživatelská základna obecně a počet uživatelů bittorrentu konkrétně stále rozrůstá,
musíme učinit trackery a oznámení efektivnější, aby trackery nebyly přetíženy.

Bittorrent navrhnul UDP trackery v BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) v roce 2008 a drtivá většina
trackerů na clearnetu je nyní pouze UDP.

Je obtížné vypočítat úspory šířky pásma datagramů vs. streamovací protokol.
Odpověď na požadavek je přibližně stejně velká jako streamovací SYN, ale náklad
je asi o 500 bajtů menší, protože HTTP GET má obrovský 600-bajtový
řetězec parametrů URL.
Surová odpověď je mnohem menší než streamovací SYN ACK, což poskytuje významné snížení
pro odchozí provoz trackeru.

Kromě toho by mělo dojít k specifickým implementačním úsporám paměti,
protože datagramy vyžadují mnohem menší stav v paměti než streamingové připojení.

Post-kvantové šifrování a podpisy, jak bylo zamýšleno v [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/), výrazně
zvýší režijní náklady na šifrované a podepsané struktury, včetně destinací,
leasesets, streamovacích SYN a SYN ACK. Je důležité minimalizovat tuto
režii, kde je to možné, před tím, než bude v I2P přijata PQ krypto.


## Design

Tento návrh používá odpovědný datagram2, odpovědný datagram3 a surové datagramy,
jak je definováno v [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/).
Datagram2 a Datagram3 jsou nové varianty odpovědných datagramů,
definované v Návrhu 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagram2 přidává odolnost proti opakování a podporu offline podpisu.
Datagram3 je menší než starý formát datagramu, ale bez autentizace.


### BEP 15

Pro referenci, tok zpráv definovaný v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) je následující:

```
Klient                        Tracker
    Požadavek spojení ------------->
      <-------------- Odpověď spojení
    Požadavek oznámení ------------->
      <-------------- Odpověď oznámení
    Požadavek oznámení ------------->
      <-------------- Odpověď oznámení
```

Fáze spojení je vyžadována k zabránění podvržení IP adresy.
Tracker vrací ID spojení, které klient používá v následujících oznámeních.
Toto ID spojení vyprší výchozí za jednu minutu u klienta a za dvě minuty u trackeru.

I2P použije stejný tok zpráv jako BEP 15,
pro snadné přijetí v existujících klientských kódových základnách podporujících UDP:
pro efektivnost a z bezpečnostních důvodů, které budou uvedeny níže:

```
Klient                        Tracker
    Požadavek spojení ------------->       (Odpovědný Datagram2)
      <-------------- Odpověď spojení   (Surový)
    Požadavek oznámení ------------->      (Odpovědný Datagram3)
      <-------------- Odpověď oznámení  (Surový)
    Požadavek oznámení ------------->      (Odpovědný Datagram3)
      <-------------- Odpověď oznámení  (Surový)
             ...
```

To potenciálně poskytuje velké úspory šířky pásma oproti
streamování (TCP) oznámení.
Zatímco Datagram2 je přibližně stejné velikosti jako streamovací SYN,
surová odpověď je mnohem menší než streamovací SYN ACK.
Následné požadavky používají Datagram3, a následující odpovědi jsou surové.

Požadavky na oznámení jsou Datagram3, aby tracker nemusel
udržovat velkou mapovací tabulku ID spojení vůči cílové oznámení nebo hash.
Místo toho může tracker generovat ID spojení kryptograficky
z hash odesílatele, aktuálního časového razítka (založeného na nějakém intervalu),
a tajné hodnoty.
Když je obdržen požadavek na oznámení, tracker ověří
ID spojení a pak použije
Datagram3 hash odesílatele jako cíl odesílání.


### Podpora Tracker/Klient

Pro integrovanou aplikaci (router a klient v jednom procesu, například i2psnark, a Java plugin ZzzOT),
nebo pro aplikaci založenou na I2CP (například BiglyBT),
by mělo být přímé implementovat a směrovat streamování a datagramový provoz odděleně.
Očekává se, že ZzzOT a i2psnark budou první tracker a klient, které implementují tento návrh.

Neintegrované trackery a klienti jsou diskutováni níže.


Trackery
````````

Existují čtyři známé implementace trackerů I2P:

- zzzot, integrovaný Java plugin routeru, provozovaný na opentracker.dg2.i2p a několika dalších
- tracker2.postman.i2p, provozovaný pravděpodobně za Java routerem a HTTP serverovým tunelem
- Starý C opentracker, přenesený zzz, s UDP podporou zakomentovanou
- Nový C opentracker, přenesený r4sas, provozovaný na opentracker.r4sas.i2p a možná dalších,
  provozovaný pravděpodobně za routerem i2pd a HTTP serverovým tunelem

Pro externí aplikaci trackeru, která v současné době používá HTTP serverový tunel pro příjem
požadavků na oznámení, může být implementace velmi obtížná.
Speciální tunel by mohl být vyvinut k překladu datagramů na lokální HTTP požadavky/odpovědi.
Nebo by mohl být navržen speciální tunel, který by zpracovával jak HTTP požadavky, tak datagramy
a předával by datagramy externímu procesu.
Tyto rozhodnutí o návrhu budou silně záviset na konkrétních implementacích routeru a trackeru,
a jsou mimo rozsah tohoto návrhu.


Klienti
```````
Externí torrent klienti založení na SAM jako například qbittorrent a další klienti založení na libtorrentu
by vyžadovali SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/), který není podporován i2pd.
To je také vyžadováno pro podporu DHT a je dostatečně složité, že žádný známý
torrent klient založený na SAMu jej neimplementoval.
Žádné implementace tohoto návrhu založené na SAM se nečekají brzy.


### Životnost spojení

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) specifikuje, že ID spojení vyprší za jednu minutu u klienta a za dvě minuty u trackeru.
Není to konfigurovatelné.
To omezuje možné zisky efektivity, pokud
klienti nesdružují oznámení, aby je uskutečnili všechny v rámci jednoho minutového okna.
i2psnark momentálně nesdružuje oznámení; rozděluje je, aby se vyhnul výbuchům provozu.
Uživatelé se zpráv zmiňují, že provozují tisíce torrentů najednou,
a rozdělit tak mnoho oznámení do jedné minuty není realistické.

Zde navrhujeme rozšířit odpověď na spojení o přidání volitelného pole s dobou životnosti spojení.
Výchozí hodnota, pokud není přítomna, je jedna minuta. Jinak, doba životnosti, která je specifikována
v sekundách, bude použita klientem, a tracker bude udržovat ID spojení o jednu minutu více.


### Kompatibilita s BEP 15

Tento návrh udržuje kompatibilitu s [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) co nejvíce
kladním způsobem, aby se omezily změny požadované v existujících klientech a trackerech.

Jedinou požadovanou změnou je formát informací o peeru v odpovědi na oznámení.
Přidání pole s dobou životnosti v odpovědi na spojení není povinné
ale je velmi doporučováno pro efektivitu, jak je uvedeno výše.



### Bezpečnostní analýza

Důležitým cílem UDP protokolu oznámení je zabránit podvržení adres.
Klient musí skutečně existovat a odeslat reálenderset.
Musí mít vstupní tunely pro přijetí odpovědi na spojení.
Tyto tunely mohou být nulové délky a okamžitě vytvořeny, ale to by
odhalilo tvůrce.
Tento protokol dosahuje tohoto cíle.



### Problémy

- Tento návrh nepodporuje zaslepené destinace,
  ale může být rozšířen, aby to umožnil. Viz níže.




## Specifikace

### Protokoly a porty

Odpovědný Datagram2 používá I2CP protokol 19;
odpovědný Datagram3 používá I2CP protokol 20;
Surové datagramy používají I2CP protokol 18.
Požadavky mohou být Datagram2 nebo Datagram3. Odpovědi jsou vždy surové.
Starší odpovědný datagram ("Datagram1") formát používající I2CP protokol 17
nesmí být použit pro požadavky nebo odpovědi; musí být upuštěny, pokud jsou přijaty
na požadavkových/odpovědních portech. Všimněte si, že Datagram1 protokol 17
je stále používán pro DHT protokol.

Požadavky používají port I2CP "to" z oznámení URL; viz níže.
Port "from" je vybrán klientem, ale měl by být nezáporný
a jiný než ty používané DHT, aby odpovědi
mohly být snadno klasifikovány.
Trackery by měly odmítnout požadavky přijaté na špatném portu.

Odpovědi používají port I2CP "to" z požadavku.
Port "from" je port "to" z požadavku.


### URL pro oznámení

Formát URL pro oznámení není specifikován v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html),
ale jako na internetu, UDP URL oznámení jsou formátu "udp://host:port/path".
Cesta je ignorována a může být prázdná, ale typicky je "/announce" na internetu.
Část :port by měla být vždy přítomna, nicméně,
pokud je část ":port" vynechána, použijte výchozí port I2CP 6969,
protože to je běžný port na internetu.
Mohou být také připojeny parametry cgi &a=b&c=d, které mohou být zpracovány
a poskytnuty v požadavku na oznámení, viz [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Pokud nejsou žádné parametry nebo cesta, může být taky vynechána koncová /
jak je naznačeno v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).


### Formáty datagramů

Všechny hodnoty jsou odeslány v síťovém pořadí byte (big endian).
Neočekávejte, že pakety budou přesně určité velikosti.
Budoucí rozšíření by mohla zvýšit velikost paketů.



Požadavek na spojení
`````````````````````

Klient na tracker.
16 bajtů. Musí být odpovědný Datagram2. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.


```
Offset  Velikost       Jméno            Hodnota
  0       64bit celé číslo  protocol_id     0x41727101980 // magická konstanta
  8       32bit celé číslo  akce            0 // spojení
  12      32bit celé číslo  transaction_id
```



Odpověď na spojení
`````````````````

Tracker na klienta.
16 nebo 18 bajtů. Musí být surová. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) vyjma níže uvedeného.


```
Offset  Velikost       Jméno            Hodnota
  0       32bit celé číslo  akce            0 // spojení
  4       32bit celé číslo  transaction_id
  8       64bit celé číslo  connection_id
  16      16bit celé číslo  lifetime        volitelný  // Změna z BEP 15
```

Odpověď musí být odeslána na port I2CP "to", který byl přijat jako port "from" v požadavku.

Pole lifetime je volitelné a označuje životnost klienta connection_id v sekundách.
Výchozí hodnota je 60 a minimum, pokud je specifikováno, je 60.
Maximum je 65535 nebo přibližně 18 hodin.
Tracker by měl udržovat connection_id po dobu 60 sekund více než životnost klienta.



Požadavek na oznámení
````````````````````

Klient na tracker.
98 bajtů minimálně. Musí být odpovědný Datagram3. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) s vyjma níže.

connection_id je, jak bylo přijato v odpovědi o spojení.



```
Offset  Velikost       Jméno            Hodnota
  0       64bit celé číslo  connection_id
  8       32bit celé číslo  akce            1     // oznámení
  12      32bit celé číslo  transaction_id
  16      20-bajtský řetězec  info_hash
  36      20-bajtský řetězec  peer_id
  56      64bit celé číslo  staženo
  64      64bit celé číslo  vlevo
  72      64bit celé číslo  nahráno
  80      32bit celé číslo  událost         0     // 0: žádná; 1: dokončeno; 2: začátek; 3: zastaveno
  84      32bit celé číslo  IP adresa        0     // výchozí
  88      32bit celé číslo  klíč
  92      32bit celé číslo  num_want       -1    // výchozí
  96      16bit celé číslo  port
  98      různé           možnosti          volitelný  // Jak je specifikováno v BEP 41
```

Změny z [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- klíč je ignorován
- port je pravděpodobně ignorován
- Sekce možností, pokud je přítomna, je definována v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Odpověď musí být odeslána na port I2CP "to", který byl přijat jako port "from" v požadavku.
Nepoužívejte port z požadavku na oznámení.



Odpověď na oznámení
``````````````````

Tracker na klienta.
20 bajtů minimálně. Musí být surová. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) s vyjma níže.



```
Offset  Velikost       Jméno            Hodnota
  0           32bit celé číslo  akce            1 // oznámení
  4           32bit celé číslo  transaction_id
  8           32bit celé číslo  interval
  12          32bit celé číslo  leechers
  16          32bit celé číslo  seeders
  20   32 * n 32-bajtský hash  binární hashe     // Změna z BEP 15
  ...                                          // Změna z BEP 15
```

Změny z [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Místo 6-bajtské IPv4+port nebo 18-bajtské IPv6+port, vracíme
  násobek 32-bajtových "kompaktních odpovědí" s SHA-256 binárními hash peery.
  Stejně jako s TCP kompaktními odpovědmi nepřidáváme port.

Odpověď musí být odeslána na port I2CP "to", který byl přijat jako port "from" v požadavku.
Nepoužívejte port z požadavku na oznámení.

I2P datagramy mají velmi velkou maximální velikost okolo 64 KB;
nicméně, pro spolehlivé doručení by se měly vyhnout datagramům větším než 4 KB.
Pro účinnost šířky pásma by trackery měly pravděpodobně omezit maximální počet peerů
na asi 50, což odpovídá okolo 1600 bajtů dokumentu před nadměrnými
vrstvami a mělo by být v rámci limitu užitečného zatížení dvou zpráv tunelu
po fragmentaci.

Stejně jako v BEP 15, není zahrnut počet peer adres
(IP/port pro BEP 15, hashe zde) k následování.
Ačkoli to není zvažováno v BEP 15, marker konce peerů
z celkových nul by mohl být definován, aby označoval, že informace o peeru je kompletní
a následují nějaké rozšiřující data.

Aby bylo možné budovat rozšíření v budoucnosti, klienti by měli ignorovat
32-bajtský hash všech nul a jakákoliv data, která následují.
Trackery by měly odmítat oznámení od kompletně nulového hashe,
i když tento hash je již zakázán Javovými routery.


Scrape
``````

Scrape požadavek/odpověď z [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) není povinná tímto návrhem,
ale může být implementována, pokud je to žádoucí, žádné změny nejsou potřeba.
Klient musí nejprve získat ID spojení.
Požadavek scrape je vždy odpovědný Datagram3.
Odpověď scrape je vždy surová.



Chybová odpověď
````````````````

Tracker na klienta.
8 bajtů minimálně (pokud je zpráva prázdná).
Musí být surová. Stejné jako v [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Žádné změny.

```

Offset  Velikost       Jméno            Hodnota
  0       32bit celé číslo  akce          3 // error
  4       32bit celé číslo  transaction_id
  8       řetězec          zpráva

```



## Rozšíření

Rozšiřující bity nebo pole verze nejsou zahrnuty.
Klienti a trackery by neměli předpokládat, že pakety budou určité velikosti.
Tímto způsobem mohou být přidána další pole bez narušení kompatibility.
Rozšířovací formát definovaný v [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) je doporučován, pokud je potřeba.

Odpověď na spojení je změněna, aby přidala volitelné pole životnosti ID spojení.

Pokud je potřeba podpora oslepených destinací, můžeme buď přidat
oslepenou 35-bajtovou adresu na konec požadavku na oznámení,
nebo požadovat oslepené hash odpovědí,
používající formát [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parametry TBD).
Sada oslepených 35-bajtových adres peerů může být přidána na konec odpovědi na oznámení,
po kompletně nulovém 32-bajtovém hashi.



## Pokyny pro implementaci

Viz sekce design výše pro diskusi o výzvách pro
neintegrované klienty a trackery nepoužívající I2CP.


### Klienti

Pro dané jméno hostitele trackeru by měl klient preferovat UDP nad HTTP URL,
a neměl by oznámit na oba.

Klienti s existující podporou BEP 15 by měli vyžadovat pouze malé úpravy.

Pokud klient podporuje DHT nebo jiné datagramové protokoly, měl by pravděpodobně
vybrat jiný port jako požadavkový "from port", aby odpovědi
přicházely zpět na tento port a nebyly smíchány s DHT zprávami.
Klient pouze přijímá surové datagramy jako odpovědi.
Trackery nikdy neodešlou odpovědný datagram2 klientovi.

Klienti s výchozím seznamem opentrackerů by měli aktualizovat seznam, aby
přidali UDP URL po té, co je známo, že opentrackery podporují UDP.

Klienti mohou nebo nemusí implementovat opakovaný přenos požadavků.
Opakování, pokud je implementováno, by mělo používat počáteční timeout
alespoň 15 sekund a zdvojnásobit timeout pro každé opakování
(exponenciální zádrž).

Klienti se musí stáhnout, pokud obdrží chybovou odpověď.


### Trackery

Trackery s existující podporou BEP 15 by měly vyžadovat pouze malé úpravy.
Tento návrh se liší od návrhu z roku 2014, v tom, že tracker
musí podporovat příjem odpovědného datagramu2 a datagramu3 na stejném portu.

Pro minimalizaci požadavků na zdroje trackeru,
tento protokol je navržen, aby eliminoval jakýkoli požadavek, že tracker
uchovává mapování hash klientů na ID spojení pro pozdější ověření.
To je možné, protože paket požadavku na oznámení je odpovědný
Datagram3 paket, takže obsahuje hash odesílatele.

Doporučená implementace je:

- Definovat aktuální epochu jako aktuální čas s rozlišením životnosti ID spojení,
  ``epoch = now / lifetime``.
- Definovat kryptografickou hašovací funkci ``H(secret, clienthash, epoch)``, která generuje
  8bajtový výstup.
- Generovat náhodnou konstantu secret použitou pro všechna spojení.
- Pro odpovědi na spojení generovat ``connection_id = H(secret,  clienthash, epoch)``
- Pro požadavky na oznámení ověřit přijaté ID spojení v aktuální epoše ověřením
  ``connection_id == H(secret, clienthash epoch) || connection_id == H(secret, clienthash, epoch - 1)``


## Migrace

Existující klienti nepodporují UDP URL oznámení a ignorují je.

Existující trackery nepodporují příjem odpovědných nebo surových datagramů, budou upuštěny.

Tento návrh je zcela dobrovolný. Ani klienti, ani trackery nejsou povinny jej kdykoli implementovat.



## Nasazení

První implementace se očekávají v ZzzOT a i2psnark.
Budou použity pro testování a ověření tohoto návrhu.

Ostatní implementace budou následovat, jakmile budou dokončeny testování a ověřování.




```
