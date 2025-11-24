---
title: "Tunely ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Ukončeno"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Poznámka
Nasazení a testování sítě probíhá.
Podléhá drobným úpravám.
Podívejte se na [SPEC](/en/docs/spec/) pro oficiální specifikaci.


## Přehled

Tento dokument navrhuje změny v šifrování zpráv na sestavení tunelů
používající kryptografické primitivy zavedené v [ECIES-X25519](/en/docs/spec/ecies/).
Je to část celkového návrhu
[Prop156](/en/proposals/156-ecies-routers/) pro konverzi routerů z ElGamal na ECIES-X25519 klíče.

Pro účely přechodu sítě z ElGamal + AES256 na ECIES + ChaCha20 jsou nutné
tunely s mixem ElGamal a ECIES routerů.
Poskytují se specifikace pro zpracování smíšených skoků v tunelu.
Nezmění se formát, zpracování ani šifrování skoků ElGamal.

Tvořitelé tunelů ElGamal budou muset vytvořit efemérní páry klíčů X25519 pro každý skok a
následovat tuto specifikaci pro vytváření tunelů obsahujících skoky ECIES.

Tento návrh specifikuje změny potřebné pro sestavování tunelů ECIES-X25519.
Pro přehled všech změn potřebných pro routery ECIES se podívejte na návrh 156 [Prop156](/en/proposals/156-ecies-routers/).

Tento návrh zachovává stejnou velikost záznamů sestavení tunelu,
jak je požadováno pro kompatibilitu. Menší záznamy a zprávy budou implementovány později - viz [Prop157](/en/proposals/157-new-tbm/).


### Kryptografické primitivy

Nejsou zavedeny žádné nové kryptografické primitivy. Primitivy potřebné k implementaci tohoto návrhu jsou:

- AES-256-CBC jako v [Cryptography](/en/docs/spec/cryptography/)
- STREAM ChaCha20/Poly1305 funkce:
  ENCRYPT(k, n, plaintext, ad) a DECRYPT(k, n, ciphertext, ad) - jako v [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) a [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH funkce - jako v [NTCP2](/en/docs/spec/ntcp2/) a [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - jako v [NTCP2](/en/docs/spec/ntcp2/) a [ECIES-X25519](/en/docs/spec/ecies/)

Další funkce Noise definované jinde:

- MixHash(d) - jako v [NTCP2](/en/docs/spec/ntcp2/) a [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - jako v [NTCP2](/en/docs/spec/ntcp2/) a [ECIES-X25519](/en/docs/spec/ecies/)


### Cíle

- Zvýšit rychlost kryptografických operací
- Nahradit ElGamal + AES256/CBC primitivy ECIES pro záznamy BuildRequestRecords a BuildReplyRecords.
- Nezměnit velikost šifrovaných BuildRequestRecords a BuildReplyRecords (528 bajtů) pro kompatibilitu
- Nepřidávat nové zprávy I2NP
- Uchovat velikost šifrovaného záznamu pro kompatibilitu
- Přidat přechodnou utajitelnost pro zprávy o sestavení tunelu
- Přidat autentizované šifrování
- Detekovat přeskupení skoků BuildRequestRecords
- Zvýšit rozlišení časové značky tak, aby bylo možné zmenšit velikost Bloomova filtru
- Přidat pole pro dobu expirace tunelu, aby bylo možné mít různé životnosti tunelů (pouze tunely ECIES)
- Přidat pole s rozšiřitelnými možnostmi pro budoucí funkce
- Znovu použít existující kryptografické primitivy
- Zlepšit bezpečnost zpráv o sestavení tunelu, kdykoli je to možné, při zachování kompatibility
- Podporovat tunely se smíšenými ElGamal/ECIES účastníky
- Zlepšit obranu proti „tagovacím“ útokům na sestavovací zprávy
- Skoky nemusí vědět typ šifrování dalšího skoku před zpracováním sestavovací zprávy,
  protože nemusí mít identitu příjemce dalšího skoku (RI) v ten čas
- Maximalizovat kompatibilitu se současnou sítí
- Nezměnit šifrování požadavků/odpovědí s tunel build AES pro ElGamal routery
- Nezměnit tunel AES „vrstvěnné“ šifrování, pro to viz [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Pokračovat v podpoře obou 8-záznamového TBM/TBRM a proměnné velikosti VTBM/VTBRM
- Nevyžadovat „flag day“ upgrade na celou síť


### Nicht-Cíle

- Úplný redesign zpráv o sestavení tunelu vyžadující „flag day“.
- Zmenšování zpráv o sestavení tunelu (vyžaduje všechny skoky ECIES a nový návrh)
- Použití možností sestavení tunelu, jak je definováno v [Prop143](/en/proposals/143-build-message-options/), vyžadovány pouze pro malé zprávy
- Obousměrné tunely - pro to viz [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Menší zprávy o sestavení tunelu - pro to viz [Prop157](/en/proposals/157-new-tbm/)


## Model hrozby

### Cíle návrhu

- Žádné skoky nejsou schopny určit autora tunelu.

- Střední skoky nesmí být schopny určit směr tunelu
  nebo svou pozici v tunelu.

- Žádné skoky nemohou číst žádný obsah jiných záznamů požadavků nebo odpovědí, kromě
  zkráceného hash routeru a efemérního klíče pro další skok

- Žádný člen odpovědního tunelu pro odchozí sestavení nemůže číst žádné odpovědní záznamy.

- Žádný člen odchozího tunelu pro příchozí sestavení nemůže číst žádné záznamy požadavků,
  kromě toho, že OBEP může vidět zkrácený hash routeru a efemérní klíč pro IBGW




### Tagovací útoky

Hlavním cílem návrhu stavby tunelu je ztížit
koluzním routerům X a Y zjistit, zda jsou v jednom tunelu.
Pokud je router X na skoku m a router Y na skoku m+1, budou samozřejmě vědět.
Pokud je však router X na skoku m a router Y na skoku m+n pro n>1, mělo by to být mnohem obtížnější.

Tagovací útoky jsou případy, kdy router uprostřed X změní zprávu o sestavení tunelu tak, aby
router Y mohl detekovat úpravu, když zpráva o sestavení dorazí.
Cílem je, aby jakákoliv upravená zpráva byla routerem mezi X a Y zrušena dřív, než dorazí k routeru Y.
Pro modifikace, které nejsou zrušeny před routerem Y, by měl tvůrce tunelu detekovat poškození v odpovědi
a tunel odmítnout.

Možné útoky:

- Změnění záznamu o stavbě
- Náhrada záznamu o stavbě
- Přidání nebo odstranění záznamu o stavbě
- Přeskupení záznamů o stavbě


TODO: Zabraňuje současný návrh všem těmto útokům?




## Návrh

### Noise Protocol Framework

Tento návrh poskytuje požadavky založené na Noise Protocol Framework
[NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11).
V řeči Noise je Alice iniciátor a Bob je příjemce.

Tento návrh je založen na Noise protokolu Noise_N_25519_ChaChaPoly_SHA256.
Tento Noise protokol používá následující primitivy:

- Vzor jednostranného handshake: N
  Alice nepředává svůj statický klíč Bobovi (N)

- DH Funkce: X25519
  X25519 DH s délkou klíče 32 bajtů, jak je specifikováno v [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Šifrovací funkce: ChaChaPoly
  AEAD_CHACHA20_POLY1305, jak je specifikováno v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8.
  12 bajtový nonce, první 4 bajty jsou nastaveny na nulu.
  Identické tomu v [NTCP2](/en/docs/spec/ntcp2/).

- Hash funkce: SHA256
  Standardní hash o délce 32 bajtů, již široce používán v I2P.


Doplňky k Frameworku
````````````````````````````````

Žádné.


### Vzory handshake

Handshaky používají vzory handshake [Noise](https://noiseprotocol.org/noise.html).

Použitá mapování písmen:

- e = efemérní klíč
- s = statický klíč
- p = payload zprávy

Záznam požadavku je identický vzoru Noise N.
To je také identické první (požadavek na relaci) zprávě ve vzoru XK používané v [NTCP2](/en/docs/spec/ntcp2/).


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Šifrování požadavku

Záznamy požadavků na sestavení tunelu jsou vytvořeny autorem tunelu a asymetricky šifrovány pro každý skok.
Toto asymetrické šifrování záznamů požadavků je v současnosti ElGamal, jak je definováno v [Cryptography](/en/docs/spec/cryptography/)
a obsahuje SHA-256 kontrolní součet. Tento návrh není přechodně tajný.

Nový návrh použije jednosměrný Noise vzor "N" s ECIES-X25519 efemérně-statickým DH, s HKDF, a
ChaCha20/Poly1305 AEAD pro přechodnou tajnost, integritu a autentizaci.
Alice je autor požadavku na sestavení tunelu. Každý skok v tunelu je Bob.


(Vlastnosti bezpečnosti Payloadu)

  ```text

N:                      Autentizace   Důvěrnost
    -> e, es                  0                2

    Autentizace: Žádná (0).
    Tento payload mohl být odeslán jakoukoliv stranou, včetně aktivního útočníka.

    Důvěrnost: 2.
    Šifrování pro známého příjemce, přechodná tajnost pouze pro kompromitaci odesílatele,
    zranitelné vůči opakování. Tento payload je zašifrován na základě DHs
    zahrnujících statickou klíčovou dvojici příjemce. Pokud by statický
    soukromý klíč příjemce byl kompromitován, byť i v pozdějším datu, tento
    payload může být dešifrován. Tato zpráva může být také opakována, protože
    neexistuje efemérní přispění od příjemce.

    "e": Alice vygeneruje nový efemérní klíčový pár a uloží jej do proměnné e,
         zapíše efemérní veřejný klíč jako prostý text do bufferu zprávy, a
         hašuje veřejný klíč spolu se starým h pro derivaci nového h.

    "es": Provede se DH mezi Aliceiným efemérním klíčovým párem a
          Bobovým statickým klíčovým párem. Výsledek se hašuje spolu
          se starým ck pro derivaci nového ck a k, a n je nastaveno na nulu.





  ```



### Šifrování odpovědi

Záznamy odpovědí se vytvářejí tvůrcem skoků a symetricky šifrují pro tvůrce.
Toto symetrické šifrování odpovědí je v současnosti AES s předřazeným SHA-256 kontrolním součtem.
a obsahuje SHA-256 kontrolní součet. Tento návrh není přechodně tajný.

Nový návrh použije ChaCha20/Poly1305 AEAD pro integritu a autentizaci.


### Oprávnění

Efemérní veřejný klíč v požadavku nemusí být skrýván pomocí AES
nebo Elligator2. Předchozí skok je jediný, kdo jej může vidět, a ten skok
ví, že další skok je ECIES.

Odpovědní záznamy nevyžadují plné asymetrické šifrování s dalším DH.



## Specifikace



### Záznamy požadavků na sestavení

Šifrované BuildRequestRecords mají 528 bajtů pro ElGamal i ECIES, pro kompatibilitu.


Záznam požadavku nešifrovaný (ElGamal)
`````````````````````````````````````````

Pro referenci, toto je současná specifikace záznamu BuildRequestRecord pro ElGamal routery, převzatá z [I2NP](/en/docs/spec/i2np/).
Nešifrovaná data jsou předsuňována nenulovým bajtem a SHA-256 hashem dat před šifrováním,
jak je definováno v [Cryptography](/en/docs/spec/cryptography/).

Všechna pole jsou big-endian.

Velikost nešifrovaného: 222 bajtů

  ```dataspec


bytes     0-3: ID tunelu ke přijímání zpráv jako, nenulové
  bytes    4-35: místní hash identity routeru
  bytes   36-39: ID dalšího tunelu, nenulové
  bytes   40-71: hash identity dalšího routeru
  bytes  72-103: AES-256 klíč tunelové vrstvy
  bytes 104-135: AES-256 klíč IV tunelové vrstvy
  bytes 136-167: AES-256 klíč odpovědi
  bytes 168-183: AES-256 IV odpovědi
  byte      184: příznaky
  bytes 185-188: čas požadavku (v hodinách od epochy, zaokrouhlen dolů)
  bytes 189-192: další ID zprávy
  bytes 193-221: neinterpetovaná / náhodná výplň




  ```


Záznam požadavku šifrovaný (ElGamal)
`````````````````````````````````````

Pro referenci, toto je současná specifikace záznamu BuildRequestRecord pro ElGamal routery, převzatá z [I2NP](/en/docs/spec/i2np/).

Velikost šifrovaného: 528 bajtů

  ```dataspec


bytes    0-15: Zkrácený hash identity skoku
  bytes  16-528: ElGamal šifrovaný BuildRequestRecord




  ```




Záznam požadavku nešifrovaný (ECIES)
```````````````````````````````````````

Toto je navrhovaná specifikace záznamu BuildRequestRecord pro routery ECIES-X25519.
Shrnutí změn:

- Odstranění nepoužívaného 32-bajtového router hash
- Změna času požadavku z hodin na minuty
- Přidání pole expirace pro budoucí proměnné časy tunelu
- Přidání více místa pro příznaky
- Přidání Mapování pro dodatečné možnosti sestavení
- AES-256 odpovědní klíč a IV nejsou použity pro odpovědní záznam skoku
- Nešifrovaný záznam je delší, protože je méně režie šifrování


Záznam o požadavku neobsahuje žádné ChaCha odpovědní klíče.
Ty klíče jsou odvozeny z KDF. Viz níže.

Všechna pole jsou big-endian.

Velikost nešifrovaného: 464 bajtů

  ```dataspec


bytes     0-3: ID tunelu ke přijímání zpráv jako, nenulové
  bytes     4-7: ID dalšího tunelu, nenulové
  bytes    8-39: hash identity dalšího routeru
  bytes   40-71: AES-256 klíč tunelové vrstvy
  bytes  72-103: AES-256 klíč IV tunelové vrstvy
  bytes 104-135: AES-256 klíč odpovědi
  bytes 136-151: AES-256 IV odpovědi
  byte      152: příznaky
  bytes 153-155: více příznaků, nepoužívané, nastavit na 0 pro kompatibilitu
  bytes 156-159: čas požadavku (v minutách od epochy, zaokrouhlen dolů)
  bytes 160-163: expirace požadavku (v sekundách od vytvoření)
  bytes 164-167: další ID zprávy
  bytes   168-x: možnosti sestavení tunelu (Mapování)
  bytes     x-x: další data, jak je naznačeno příznaky nebo možnostmi
  bytes   x-463: náhodná výplň




  ```

Pole příznaků je stejné jako je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/) a obsahuje následující::

 Pořadí bitů: 76543210 (bit 7 je MSB)
 bit 7: pokud je nastaven, dovolit zprávy od kohokoli
 bit 6: pokud je nastaven, dovolit zprávy kdekoli, a odeslat odpověď na
        specifikovaný další skok v odpovědní zprávě o sestavení tunelu
 bity 5-0: Nedefinováno, musí být nastaveno na 0 pro kompatibilitu s budoucími možnostmi

Bit 7 znamená, že skok bude příchozí bránou (IBGW). Bit 6
signalizuje, že skok bude výstupním koncovým bodem (OBEP). Pokud není nastaven žádný bit,
skok bude středním účastníkem. Oba nemohou být nastaveny současně.

Pole expirace požadavku je pro budoucí variabilní trvání tunelu.
Prozatím je podporovaná hodnota pouze 600 (10 minut).

Možnosti sestavení tunelu jsou Mapování, jak je definováno v [Common](/en/docs/spec/common-structures/).
Toto je pro budoucí použití. Žádné možnosti nejsou v současnosti definovány.
Pokud je struktura Mapování prázdná, jedná se o dva bajty 0x00 0x00.
Maximální velikost Mapování (včetně délkového pole) je 296 bajtů,
a maximální hodnota délkového pole Mapování je 294.



Záznam požadavku šifrovaný (ECIES)
```````````````````````````````````````

Všechna pole jsou big-endian kromě efemérního veřejného klíče, který je little-endian.

Velikost šifrovaného: 528 bajtů

  ```dataspec


bytes    0-15: Zkrácený hash identity skoku
  bytes   16-47: Odesílatelův efemérní X25519 veřejný klíč
  bytes  48-511: ChaCha20 šifrovaný BuildRequestRecord
  bytes 512-527: Poly1305 MAC




  ```



### Záznamy odpovědí na sestavení

Šifrované BuildReplyRecords mají 528 bajtů pro ElGamal i ECIES, pro kompatibilitu.


Záznam odpovědi nešifrovaný (ElGamal)
`````````````````````````````````````
ElGamal odpovědi jsou šifrovány s AES.

Všechna pole jsou big-endian.

Velikost nešifrovaného: 528 bajtů

  ```dataspec


bytes   0-31: SHA-256 Hash bajtů 32-527
  bytes 32-526: náhodná data
  byte     527: odpověď

  celková délka: 528




  ```


Záznam odpovědi nešifrovaný (ECIES)
`````````````````````````````````````
Toto je navrhovaná specifikace záznamu BuildReplyRecord pro routery ECIES-X25519.
Shrnutí změn:

- Přidání Mapování pro možnosti odpovědi
- Nešifrovaný záznam je delší, protože je méně režie šifrování

ECIES odpovědi jsou šifrovány s ChaCha20/Poly1305.

Všechna pole jsou big-endian.

Velikost nešifrovaného: 512 bajtů

  ```dataspec


bytes    0-x: Možnosti odpovědi při sestavení tunelu (Mapování)
  bytes    x-x: další data, jak je naznačeno možnostmi
  bytes  x-510: Náhodná výplň
  byte     511: Bajt odpovědi




  ```

Možnosti odpovědi při sestavení tunelu jsou struktura Mapování, jak je definováno v [Common](/en/docs/spec/common-structures/).
Toto je pro budoucí použití. Žádné možnosti nejsou v současnosti definovány.
Pokud je struktura Mapování prázdná, jedná se o dva bajty 0x00 0x00.
Maximální velikost Mapování (včetně délkového pole) je 511 bajtů,
a maximální hodnota délkového pole Mapování je 509.

Odpověď je jedním z následujících hodnot
jak je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/) pro zabránění fingerprintingu:

- 0x00 (přijmout)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Záznam odpovědi šifrovaný (ECIES)
```````````````````````````````````

Velikost šifrovaného: 528 bajtů

  ```dataspec


bytes   0-511: ChaCha20 šifrovaný BuildReplyRecord
  bytes 512-527: Poly1305 MAC




  ```

Po plném přechodu na ECIES záznamy zůstávají pravidla distribuce na vyžádání stejná jako pro záznamy požadavků.


### Symetrické šifrování záznamů

Smíšené tunely jsou povoleny a nezbytné pro přechod z ElGamal na ECIES.
Během přechodného období bude stále více routerů klíčem pod klíči ECIES.

Symetrická kryptografie se bude provádět stejným způsobem:

- „šifrování“:

  - šifra spuštěná v režimu dešifrování
  - záznamy požadavků se budou prediktivně dešifrovat v přípravě (skrývání šifrovaných záznamů požadavků)

- „dešifrování“:

  - šifra spuštěná v režimu šifrování
  - záznamy požadavků se zašifrují (odkrývání dalšího záznamu prostého textu požadavku) účastnickými skoky

- ChaCha20 nemá „režimy“, takže se jednoduše používá třikrát:

  - jednou v přípravě
  - jednou skokem
  - jednou při finálním zpracování odpovědi

Když se používají smíšené tunely, tvůrci tunelů budou muset založit symetrické šifrování
BuildRequestRecord na současném a předchozím typu šifrování skoku.

Každý skok použije svůj vlastní typ šifrování pro šifrování BuildReplyRecords a ostatních
záznamů v VariableTunnelBuildMessage (VTBM).

Na cestě odpovědi bude koncový bod (odesílatel) potřebovat zrušit [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), použitím každého odpovědního klíče skoku.

Pro objasňující příklad, podívejme se na výstupní tunel s ECIES obklopený ElGamal:

- Odesílatel (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Všechny BuildRequestRecords jsou ve svém šifrovaném stavu (používající ElGamal nebo ECIES).

AES256/CBC šifra, když je použita, je stále použita pro každý záznam, bez řetězení přes více záznamů.

Stejně tak ChaCha20 bude použit pro šifrování každého záznamu, ne stream přes celý VTBM.

Záznamy požadavků jsou předzpracovány Odesílatelem (OBGW):

- H3's záznam je „šifrován“ použitím:

  - H2's odpovědního klíče (ChaCha20)
  - H1's odpovědního klíče (AES256/CBC)

- H2's záznam je „šifrován“ použitím:

  - H1's odpovědního klíče (AES256/CBC)

- H1's záznam jde ven bez symetrického šifrování

Pouze H2 kontroluje příznak šifrování odpovědi a vidí, že záznam následuje AES256/CBC.

Po zpracování každým skokem jsou záznamy ve „dešifrovaném“ stavu:

- H3's záznam je „dešifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)

- H2's záznam je „dešifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)
  - H2's odpovědního klíče (ChaCha20-Poly1305)

- H1's záznam je „dešifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)
  - H2's odpovědního klíče (ChaCha20)
  - H1's odpovědního klíče (AES256/CBC)

Tvůrce tunelu, alias Koncový bod vstupu (IBEP), po zpracování odpovědi:

- H3's záznam je „šifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)

- H2's záznam je „šifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)
  - H2's odpovědního klíče (ChaCha20-Poly1305)

- H1's záznam je „šifrován“ použitím:

  - H3's odpovědního klíče (AES256/CBC)
  - H2's odpovědního klíče (ChaCha20)
  - H1's odpovědního klíče (AES256/CBC)


### Klíče záznamů požadavků (ECIES)

Tyto klíče jsou explicitně zahrnuty v ElGamal BuildRequestRecords.
Pro ECIES BuildRequestRecords jsou klíče tunelů a AES odpovědní klíče zahrnuty,
ale ChaCha odpovědní klíče jsou odvozeny z výměny DH.
Podívejte se na [Prop156](/en/proposals/156-ecies-routers/) pro detaily statických ECIES klíčů routerů.

Níže je popis, jak odvodit klíče, které byly dříve přenášeny v záznamech o požadavcích.


KDF pro počáteční ck a h
````````````````````````

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro vzor "N" se standardním jménem protokolu.

  ```text

Toto je „e“ vzor zprávy:

  // Definovat jméno protokolu.
  Nastavit protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bajtů, US-ASCII kódováno, bez ukončení NULL).

  // Definovat Hash h = 32 bajty
  // Vyplnit do 32 bajtů. Nehašovat, protože to není více než 32 bajtů.
  h = protocol_name || 0

  Definovat ck = 32 bajtový propojující klíč. Zkopírovat data z h do ck.
  Nastavit chainKey = h

  // MixHash(null prolog)
  h = SHA256(h);

  // až do této chvíle, to všechno může být předpočítáno všemi routery.




  ```


KDF pro záznam požadavku
``````````````````````````

Tvůrci tunelů ElGamal generují efemérní klíčový pár X25519 pro každý
ECIES skok v tunelu, a používají výše uvedený návrh pro šifrování jejich BuildRequestRecord.
Tvůrci tunelů ElGamal použijí schéma před touto specifikací pro šifrování k ElGamal skokům.

Tvůrci tunelů ECIES budou muset zašifrovat každému ElGamal skoku veřejným klíčem pomocí
schématu definovaného v [Tunnel-Creation](/en/docs/spec/tunnel-creation/). Tvůrci tunelů ECIES použijí výše uvedené schéma pro šifrování
k ECIES skokům.

To znamená, že skoky tunelů uvidí pouze šifrované záznamy svého vlastního typu šifrování.

Pro tvůrce tunelů ElGamal a ECIES, budou generovat unikátní efemérní klíčové páry X25519
pro každý ECIES skok pro šifrování k ECIES skokům.

**DŮLEŽITÉ**:
Efemérní klíče musí být unikátní pro každý ECIES skok a pro každý záznam sestavení.
Neschopnost používat unikátní klíče otevírá vektor útoku pro sestavu skoků, které mohou potvrdit, že jsou ve stejném tunelu.


  ```dataspec


// Statický klíčový pár X25519 pro každý hop (hesk, hepk) z identity routeru
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || níže znamená přidat
  h = SHA256(h || hepk);

  // až do této chvíle, to všechno může být předpočítáno každým routerem
  // pro všechny příchozí požadavky sestavení

  // Odesílatel generuje efemérní klíčový pár X25519 pro každý ECIES skok ve VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Konec „e“ vzoru zprávy.

  Toto je „es“ vzor zprávy:

  // Noise es
  // Odesílatel provádí X25519 DH s veřejným klíčem Hopu.
  // Každý Hop, najde záznam s jejich zkráceným hash identitou,
  // a extrahuje Odesílatelův efemérní klíč předcházející šifrovanému záznamu.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parametry ChaChaPoly pro šifrování/dešifrování
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Uložit pro KDF odpovědního záznamu
  chainKey = keydata[0:31]

  // Parametry AEAD
  k = keydata[32:63]
  n = 0
  plaintext = 464 bajtový záznam požadavku na sestavení
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Konec „es“ vzoru zprávy.

  // MixHash(ciphertext)
  // Uložit pro KDF odpovědního záznamu
  h = SHA256(h || ciphertext)





  ```

``replyKey``, ``layerKey`` a ``layerIV`` musí být stále zahrnuty uvnitř ElGamal záznamů,
a mohou být generovány náhodně.


### Šifrování záznamu požadavku (ElGamal)

Jak je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Žádné změny v šifrování pro ElGamal skoky.




### Šifrování záznamu odpovědi (ECIES)

Záznam odpovědi je ChaCha20/Poly1305 šifrovaný.

  ```dataspec


// Parametry AEAD
  k = chainkey z požadavku sestavení
  n = 0
  plaintext = 512 bajtový záznam odpovědi na sestavení
  ad = h z požadavku sestavení

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### Šifrování záznamu odpovědi (ElGamal)

Jak je definováno v [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Žádné změny v šifrování pro ElGamal skoky.



### Analýza bezpečnosti

ElGamal neposkytuje přechodnou tajnost pro zprávy o sestavení tunelu.

AES256/CBC je v mírně lepším stavu, je pouze zranitelné teoretickému oslabování
známým `biclique` útokem.

Jediný známý praktický útok proti AES256/CBC je padding oracle útok, když IV je znám útočníkovi.

Útočník by musel rozlousknout šifrování dalšího skoku ElGamal, aby získal informace o AES256/CBC (odpovědní klíč a IV).

ElGamal je výrazně více náročný na CPU než ECIES, vedoucí k potenciálnímu vyčerpání zdrojů.

ECIES, v kombinaci s novými efemérními klíči na BuildRequestRecord nebo VariableTunnelBuildMessage, poskytuje přechodnou tajnost.

ChaCha20Poly1305 poskytuje AEAD šifrování, umožňující příjemci ověřit integritu zprávy před pokusem o dešifrování.


## Oprávnění

Tento návrh maximalizuje opětovné použití existujících kryptografických primitivů, protokolů a kódu.
Tento návrh minimalizuje riziko.




## Poznámky k implementaci

* Starší routery nekontrolují typ šifrování skoku a odešlou záznamy šifrované pomocí ElGamal.
  Některé nedávné routery jsou chybné a mohou odesílat různé typy chybných záznamů.
  Implementátoři by měli detekovat a odmítnout tyto záznamy před operací DH
  pokud je to možné, pro snížení využívání CPU.


## Problémy



## Migrace

Viz [Prop156](/en/proposals/156-ecies-routers/).




## Reference

.. [Common]
    {{ spec_url('common-structures') }}

.. [Cryptography]
   {{ spec_url('cryptography') }}

.. [ECIES-X25519]
   {{ spec_url('ecies') }}

.. [I2NP]
   {{ spec_url('i2np') }}

.. [NOISE]
    https://noiseprotocol.org/noise.html

.. [NTCP2]
   {{ spec_url('ntcp2') }}

.. [Prop119]
   {{ proposal_url('119') }}

.. [Prop143]
   {{ proposal_url('143') }}

.. [Prop153]
    {{ proposal_url('153') }}

.. [Prop156]
    {{ proposal_url('156') }}

.. [Prop157]
    {{ proposal_url('157') }}

.. [SPEC]
   {{ spec_url('tunnel-creation-ecies') }}

.. [Tunnel-Creation]
   {{ spec_url('tunnel-creation') }}

.. [Multiple-Encryption]
   https://en.wikipedia.org/wiki/Multiple_encryption

.. [RFC-7539]
   https://tools.ietf.org/html/rfc7539

.. [RFC-7748]
   https://tools.ietf.org/html/rfc7748
