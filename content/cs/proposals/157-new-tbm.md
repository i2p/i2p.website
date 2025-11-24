---
title: "Menší zprávy o stavbě tunelu"
number: "157"
author: "zzz, original"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Closed"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
---

## Poznámka
Implementováno od verze API 0.9.51.
Probíhá testování a nasazení v síti.
Předmět drobných úprav.
Pro konečnou specifikaci vizte [I2NP](/en/docs/spec/i2np/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).



## Přehled


### Shrnutí

Aktuální velikost zašifrovaných záznamů požadavků a odpovědí na konstrukci tunelu je 528.
U typických zpráv proměnných konstrukcí tunelu a odpovědí na proměnné konstrukce tunelu
je celková velikost 2113 bajtů. Tato zpráva je rozdělena na tři 1KB tunelové zprávy
pro zpětnou cestu.

Změny formátu 528-bajtového záznamu pro směrovače ECIES-X25519 jsou specifikovány v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).
Pro směs směrovačů ElGamal a ECIES-X25519 v tunelu musí velikost záznamu zůstat
528 bajtů. Avšak pokud jsou všechny směrovače v tunelu ECIES-X25519, je možné vytvořit nový, menší záznam konstrukce, protože šifrování ECIES-X25519 má mnohem menší režii
než ElGamal.

Menší zprávy by ušetřily šířku pásma. Také, pokud by se zprávy vešly do
jedné tunelové zprávy, zpětná cesta by byla třikrát účinnější.

Tento návrh definuje nové záznamy požadavků a odpovědí a nové zprávy požadavků a odpovědí na konstrukci.

Tvůrce tunelu a všechny přeskoky v vytvořeném tunelu musí používat ECIES-X25519, a alespoň verzi 0.9.51.
Tento návrh nebude užitečný, dokud většina směrovačů v síti nebude ECIES-X25519.
To se očekává na konci roku 2021.


### Cíle

Další cíle vizte [Prop152](/en/proposals/152-ecies-tunnels/) a [Prop156](/en/proposals/156-ecies-routers/).

- Menší záznamy a zprávy
- Zachovat dostatečný prostor pro budoucí možnosti, jak je definováno v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Vejít se do jedné tunelové zprávy pro zpětnou cestu
- Podporovat pouze přeskoky ECIES
- Zachovat vylepšení implementovaná v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Maximalizovat kompatibilitu se současnou sítí
- Skrýt příchozí stavební zprávy před OBEP
- Skrýt odchozí stavební odpovědní zprávy před IBGW
- Nepožadovat "vlajkový den" upgrade celé sítě
- Postupné zavádění k minimalizaci rizika
- Opětovné použití existujících kryptografických primitiv


### Nekritické cíle

Další nekritické cíle naleznete v [Prop156](/en/proposals/156-ecies-routers/).

- Neexistuje požadavek na směsné tunely ElGamal/ECIES
- Změny ve vrstvovém šifrování, viz [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Žádné zrychlení kryptografických operací. Předpokládá se, že ChaCha20 a AES jsou podobné,
  dokonce i s AESNI, alespoň pro malé velikosti dat v otázce.


## Návrh


### Záznamy

Viz přílohu pro výpočty.

Zašifrované záznamy požadavků a odpovědí budou mít 218 bajtů v porovnání s 528 bajty nyní.

Otevřené záznamy požadavků budou mít 154 bajtů,
v porovnání s 222 bajty pro záznamy ElGamal
a 464 bajty pro záznamy ECIES, jak je definováno v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Otevřené záznamy odpovědí budou mít 202 bajtů,
v porovnání s 496 bajty pro záznamy ElGamal
a 512 bajtů pro záznamy ECIES, jak je definováno v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Šifrování odpovědí bude ChaCha20 (NE ChaCha20/Poly1305),
takže otevřené záznamy nemusí být násobkem 16 bajtů.

Záznamy požadavků budou zmenšeny použitím HKDF k vytvoření
klíčů a IV vrstev a odpovědí, takže nemusí být výslovně zahrnuty v požadavku.


### Zprávy o stavbě tunelu

Obě budou "proměnné" s jedním bajtem čísla záznamů,
stejně jako u stávajících proměnných zpráv.

ShortTunnelBuild: Typ 25
````````````````````````````````

Typická délka (se 4 záznamy): 873 bajtů

Při použití pro stavbu příchozího tunelu
se doporučuje (ale není povinné), aby byla tato zpráva zašifrována česnekem autorem
cíleným na bránu pro příchozí (pokyny k doručení ROUTER),
aby byly skryty příchozí stavební zprávy před OBEP.
IBGW dešifruje zprávu,
vloží odpověď do odpovídajícího slotu
a odešle ShortTunnelBuildMessage na další přeskok.

Délka záznamu je zvolena tak, aby se STBM zašifrovaný česnekem vešel do
jedné tunelové zprávy. Viz níže uvedená příloha.



OutboundTunnelBuildReply: Typ 26
``````````````````````````````````````

Definujeme novou zprávu OutboundTunnelBuildReply.
Používá se pouze pro odchozí stavby tunelů.
Účel je skrýt odchozí stavební odpovědní zprávy před IBGW.
Musí být zašifrována česnekem OBEP, cílená na autora
(pokyny pro doručení TUNNEL).
OBEP dešifruje tunelovou stavební zprávu,
vytvoří OutboundTunnelBuildReply zprávu,
a vloží odpověď do pole obyčejného textu.
Ostatní záznamy vloží do jiných slotů.
Poté zprávu zašifruje česnekem směrem k autorovi s odvozenými symetrickými klíči.


Poznámky
```````

Zašifrováním OTBRM a STBM česnekem se také vyhneme jakýmkoli potenciálním
problémům s kompatibilitou na IBGW a OBEP spárovaných tunelů.




### Tok zprávy


  {% highlight %}
STBM: Krátká zpráva o stavbě tunelu (typ 25)
  OTBRM: Zpráva o odpovědi na stavbu odchozího tunelu (typ 26)

  Odchozí stavba A-B-C
  Odpověď stávajícím příchozím tunelem D-E-F

                  Nový Tunel
           STBM      STBM      STBM
  Vytvořitel ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | Zabaleno česnekem
                                            | OTBRM
                                            | (TUNNEL doručení)
                                            | od OBEP k
                                            | vytvořiteli
                Stávající Tunel             /
  Vytvořitel <-------F---------E-------- D <--/
                                     IBGW



  Příchozí Stavba D-E-F
  Odesláno stávajícím odchozím tunelem A-B-C

                Stávající Tunel
  Vytvořitel ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | Zabaleno česnekem (volitelné)
                                            | STBM
                                            | (ROUTER doručení)
                                            | od vytvořitele
                  Nový Tunel                | k IBGW
            STBM      STBM      STBM        /
  Vytvořitel <------ F <------ E <------ D <--/
                                     IBGW



{% endhighlight %}



### Šifrování záznamů

Šifrování záznamů požadavků a odpovědí: jak je definováno v [Prop152](/en/proposals/152-ecies-tunnels/) a [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Šifrování záznamů odpovědí pro jiné sloty: ChaCha20.


### Šifrování vrstev

V současnosti není plánována změna šifrování vrstev pro tunely vytvořené podle této specifikace; zůstane AES, jak je v současné době používáno pro všechny tunely.

Změna šifrování vrstvy na ChaCha20 je téma pro další výzkum.


### Nová Tunelová Datová Zpráva

V současné době není plánována změna 1KB Tunelové Datové Zprávy používané pro tunely
vytvořené podle této specifikace.

Může být užitečné zavést novou I2NP zprávu, která je větší nebo proměnlivě velká,
současně s tímto návrhem,
pro použití nad těmito tunely.
To by snížilo režii pro velké zprávy.
Toto je téma pro další výzkum.




## Specifikace


### Krátký záznam požadavku



Krátký nezakódovaný záznam požadavku
`````````````````````````````````````

Toto je navrhovaná specifikace pro BuildRequestRecord tunelu pro směrovače ECIES-X25519.
Shrnutí změn z [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Změnit nezakódovanou délku z 464 na 154 bajtů
- Změnit zakódovanou délku z 528 na 218 bajtů
- Odstranit klíče a IV vrstev a odpovědí, budou generovány ze split() a KDF


Záznam požadavku neobsahuje žádné ChaCha klíče odpovědí.
Tyto klíče jsou odvozeny z KDF. Viz níže.

Všechna pole jsou big-endian.

Nezakódovaná velikost: 154 bajtů.


  {% highlight lang='dataspec' %}

bytes     0-3: ID tunelu pro příjem zpráv jako, nenulové
  bytes     4-7: další ID tunelu, nenulové
  bytes    8-39: hash identity dalšího směrovače
  byte       40: vlajky
  bytes   41-42: více vlajek, nepoužité, nastavené na 0 pro kompatibilitu
  byte       43: typ šifrování vrstvy
  bytes   44-47: čas požadavku (v minutách od epochy, zaokrouhleno dolů)
  bytes   48-51: expirace požadavku (v sekundách od vytvoření)
  bytes   52-55: další ID zprávy
  bytes    56-x: volby konstrukce tunelu (Mapping)
  bytes     x-x: další data, jak je naznačeno vlajkami nebo volbami
  bytes   x-153: náhodné vycpávání (viz níže)

{% endhighlight %}


Pole vlajek je stejné, jak je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/) a obsahuje následující::

 Bitový pořadí: 76543210 (bit 7 je MSB)
 bit 7: pokud je nastaven, povolit zprávy od kohokoli
 bit 6: pokud je nastaven, povolit zprávy komukoli a odeslat odpověď na
        specifikovaný další přeskok v Zprávě o odpovědi na konstrukci tunelu
 bity 5-0: Nedefinováno, musí být nastavena na 0 pro kompatibilitu s budoucími možnostmi

Bit 7 naznačuje, že přeskok bude příchozí bránou (IBGW). Bit 6
naznačuje, že přeskok bude odchozím koncovým bodem (OBEP). Pokud není nastaven ani jeden z těchto bitů,
přeskok bude účastníkem ve střední části. Oba nemohou být nastaveny zároveň.

Typ šifrování vrstvy: 0 pro AES (jak v současných tunelech);
1 pro budoucnost (ChaCha?)

Expirace požadavku je pro budoucí proměnlivou dobu tunelu.
Prozatím je jediná podporovaná hodnota 600 (10 minut).

Tento klíč je vyžadován, protože na této vrstvě neexistuje DH pro stavební záznam.

Volby konstrukce tunelu je struktura Mapping, jak je definováno v [Common](/en/docs/spec/common-structures/).
Toto je pro budoucí použití. Žádné volby nejsou aktuálně definovány.
Pokud je struktura Mapping prázdná, jedná se o dva bajty 0x00 0x00.
Maximální velikost Mappingu (včetně pole délky) je 98 bajtů,
a maximální hodnota pole délky Mappingu je 96.



Zašifrovaný krátký záznam požadavku
`````````````````````````````````````

Všechna pole jsou big-endian kromě efemérního veřejného klíče, který je little-endian.

Zakódovaná velikost: 218 bajtů


  {% highlight lang='dataspec' %}

bytes    0-15: Zkrácený hash identity hopa
  bytes   16-47: Efemérní veřejný klíč odesílatele X25519
  bytes  48-201: ChaCha20 zašifrovaný ShortBuildRequestRecord
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### Krátký záznam odpovědi


Krátký nezakódovaný záznam odpovědi
`````````````````````````````````````
Toto je navrhovaná specifikace pro ShortBuildReplyRecord tunelu pro směrovače ECIES-X25519.
Shrnutí změn z [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Změnit nezakódovanou délku z 512 na 202 bajtů
- Změnit zakódovanou délku z 528 na 218 bajtů


Odpovědi ECIES jsou šifrovány pomocí ChaCha20/Poly1305.

Všechna pole jsou big-endian.

Nezakódovaná velikost: 202 bajtů.


  {% highlight lang='dataspec' %}

bytes    0-x: Možnosti odpovědi na konstrukci tunelu (Mapping)
  bytes    x-x: další data, jak je naznačeno možnostmi
  bytes  x-200: Náhodné vycpávání (viz níže)
  byte     201: Byte odpovědi

{% endhighlight %}

Možnosti odpovědi na konstrukci tunelu je struktura Mapping, jak je definováno v [Common](/en/docs/spec/common-structures/).
Toto je pro budoucí použití. Žádné volby nejsou aktuálně definovány.
Pokud je struktura Mapping prázdná, je to dvoubajtové 0x00 0x00.
Maximální velikost struktury Mapping (včetně pole délky) je 201 bajtů,
a maximální hodnota pole délky Mapping je 199.

Byte odpovědi je jednou z následujících hodnot
jak je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/) pro zabránění rozpoznávání otisků prstů:

- 0x00 (přijmout)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Zašifrovaný krátký záznam odpovědi
```````````````````````````````````

Zakódovaná velikost: 218 bajtů


  {% highlight lang='dataspec' %}

bytes   0-201: ChaCha20 zašifrovaný ShortBuildReplyRecord
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### KDF

Viz níže uvedená sekce KDF.




### ShortTunnelBuild
I2NP Typ 25

Tato zpráva je odeslána mezi střední přeskoky, OBEP a IBEP (vytvořitel).
Nesmí být odeslána do IBGW (místo toho použijte zabalenou česnekovým InboundTunnelBuild).
Při přijetí OBEP se transformuje na OutboundTunnelBuildReply,
zabalenou česnekem, a odesílá se autorovi.



  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 byte `Integer`
         Platné hodnoty: 1-8

  velikost záznamu: 218 bajtů
  celková velikost: 1+$num*218
{% endhighlight %}

Poznámky
`````
* Typický počet záznamů je 4, pro celkovou velikost 873.




### OutboundTunnelBuildReply
I2NP Typ 26

Tato zpráva je odesílána pouze OBEP směrem k IBEP (vytvořiteli) prostřednictvím existujícího příchozího tunelu.
Nesmí být odeslána žádnému jinému přeskoku.
Vždy je zašifrován česnekem.


  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         Celkový počet záznamů,
         1 byte `Integer`
         Platné hodnoty: 1-8

  ShortBuildReplyRecords ::
         Zašifrované záznamy
         délka: num * 218

  velikost zašifrovaného záznamu: 218 bajtů
  celková velikost: 1+$num*218
{% endhighlight %}

Poznámky
`````
* Typický počet záznamů je 4, pro celkovou velikost 873.
* Tato zpráva by měla být šifrována česnekem.



### KDF

Používáme ck z Noise stavu po šifrování/odšifrování záznamu o stavbě tunelu
k odvození následujících klíčů: klíč odpovědi, AES klíč vrstvy, AES klíč IV a klíč/tag odpovědi pro OBEP.

Klíč odpovědi:
Na rozdíl od dlouhých záznamů nemůžeme použít levou část ck pro klíč odpovědi, protože to není naposledy a bude použito později.
Klíč odpovědi je používán ke šifrování odpovědi pomocí AEAD/ChaCha20/Poly1305 a ChaCha20 k odpovědi na jiné záznamy.
Oba používají stejný klíč, nonce je pozice záznamu ve zprávě počínaje od 0.


  {% highlight lang='dataspec' %}
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  Klíč vrstvy:
  Klíč vrstvy je prozatím vždy AES, ale stejný KDF lze použít pro ChaCha20

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  Klíč IV pro ne-OBEP záznam:
  ivKey = keydata[0:31]
  protože je poslední

  Klíč IV pro OBEP záznam:
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  OBEP klíč/tag odpovědi česnekem:
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

{% endhighlight %}





## Zdůvodnění

Tento návrh maximalizuje opětovné použití stávajících kryptografických primitiv, protokolů a kódu.

Tento návrh minimalizuje riziko.

ChaCha20 je mírně rychlejší než AES pro malé záznamy, ve zkouškách na Javě.
ChaCha20 se vyhýbá požadavku na velikost dat jako násobek 16.


## Poznámky k implementaci

- Stejně jako u stávající proměnné zprávy o stavbě tunelu,
  zprávy menší než 4 záznamy nejsou doporučovány.
  Typické výchozí nastavení je 3 přeskoky.
  Příchozí tunely musí být postaveny s dalším záznamem pro
  autora, aby poslední přeskok nevěděl, že je poslední.
  Takže aby střední přeskoky nevěděly, zda je tunel příchozí nebo odchozí,
  odchozí tunely by měly být postaveny se 4 záznamy také.



## Otázky



## Migrace

Implementace, testování a zavádění bude trvat několik vydání
a přibližně jeden rok. Fáze jsou následující. Přiřazení
každé fáze ke konkrétnímu vydání je TBD a závisí na rychlosti
vývoje.

Podrobnosti implementace a migrace se mohou lišit pro
každou implementaci I2P.

Tvůrce tunelu musí zajistit, že všechny přeskoky ve vytvořeném tunelu jsou ECIES-X25519, A alespoň verze TBD.
Tvůrce tunelu NEUMÍTE být ECIES-X25519; může být ElGamal.
Pokud je však tvůrce ElGamal, odhaluje se nejbližšímu přeskoku jako tvůrce.
Takže v praxi by měly tyto tunely vytvářet pouze ECIES směrovače.

Není nutné, aby stávající tunel OBEP nebo IBGW byl ECIES nebo
nějaké konkrétní verze.
Nové zprávy jsou zabalené česnekem a nejsou viditelné v OBEP nebo IBGW
stávajícího tunelu.

Fáze 1: Implementace, není povolena ve výchozím nastavení

Fáze 2 (další vydání): Povolit ve výchozím nastavení

Neexistují žádné problémy s kompatibilitou zpětně. Nové zprávy mohou být odeslány pouze směrovačům, které je podporují.




## Příloha


Bez režie česnekem pro nešifrovaný příchozí STBM,
pokud nepoužíváme ITBM:



  {% highlight lang='text' %}
Aktuální velikost pro 4 sloty: 4 * 528 + režie = 3 tunelové zprávy

  Konstrukční zpráva pro 4 sloty, aby se vešla do jedné tunelové zprávy, jen ECIES:

  1024
  - 21 fragment hlavičky
  ----
  1003
  - 35 nezabalených ROUTERových pokynů doručení
  ----
  968
  - 16 I2NP hlavička
  ----
  952
  - 1 počet slotů
  ----
  951
  / 4 sloty
  ----
  237 Nová velikost zašifrovaného stavebního záznamu (vs. 528 nyní)
  - 16 trunciovaný hash
  - 32 efemérní klíč
  - 16 MAC
  ----
  173 maximální velikost otevřeného stavebního záznamu (vs. 222 nyní)



{% endhighlight %}


S režie česnekem pro 'N' vzorec šumu pro šifrování příchozího STBM,
pokud nepoužíváme ITBM:


  {% highlight lang='text' %}
Aktuální velikost pro 4 sloty: 4 * 528 + režie = 3 tunelové zprávy

  Česnekem šifrovaná konstrukční zpráva pro 4 sloty, aby se vešla do jedné tunelové zprávy, jen ECIES:

  1024
  - 21 fragment hlavičky
  ----
  1003
  - 35 nezabalených ROUTERových pokynů doručení
  ----
  968
  - 16 I2NP hlavička
  -  4 délka
  ----
  948
  - 32 bajtů efemérního klíče
  ----
  916
  - 7 bajtů DateTime blok
  ----
  909
  - 3 bajty česnekový blok režie
  ----
  906
  - 9 bajtů I2NP hlavička
  ----
  897
  - 1 bajt pokynů doručení ČESNEK LOKÁLNÍ
  ----
  896
  - 16 bajtů Poly1305 MAC
  ----
  880
  - 1 počet slotů
  ----
  879
  / 4 sloty
  ----
  219 Velikost nového zašifrovaného stavebního záznamu (vs. 528 nyní)
  - 16 zkrácený hash
  - 32 efemérní klíč
  - 16 MAC
  ----
  155 maximální velikost otevřeného stavebního záznamu (vs. 222 nyní)


{% endhighlight %}

Poznámky:

Aktuální velikost otevřeného stavebního záznamu před odstraněním nepotřebné vycpávky: 193

Odstranění úplného hash směrovače a generace klíčů/IV pomocí HKDF by uvolnilo dostatek prostoru pro budoucí možnosti.
Pokud je vše HKDF, požadovaný prostor otevřeného textu je asi 58 bajtů (bez žádných možností).

Česnekem zabalený OTBRM bude o něco menší než česnekem zabalený STBM,
protože dodací pokyny jsou LOKÁLNÍ, ne ROUTER,
neexistuje zahrnutý DATETIME blok a
používá 8-bajtový tag místo 32-bajtového efemérního klíče pro plné 'N' zprávy.



## Odkazy
