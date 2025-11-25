---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Poznámka
Probíhá nasazení a testování sítě.
Předmětem drobných úprav.
Viz [SPEC](/en/docs/spec/ecies/) pro oficiální specifikaci.

Následující funkce nejsou implementovány k verzi 0.9.46:

- Bloky MessageNumbers, Options a Termination
- Odpovědi na úrovni protokolu
- Nulový statický klíč
- Multicast


## Přehled

Toto je návrh nového typu šifrování typu end-to-end od začátku I2P, který má nahradit ElGamal/AES+SessionTags [Elg-AES](/en/docs/spec/elgamal-aes/).

Opírá se o předchozí práci, jak následuje:

- Společné struktury specifikace [Common](/en/docs/spec/common-structures/)
- Specifikace [I2NP](/en/docs/spec/i2np/) včetně LS2
- ElGamal/AES+Session Tags [Elg-AES](/en/docs/spec/elgamal-aes/)
- Přehled nové asymetrické kryptografie http://zzz.i2p/topics/1768
- Přehled nízkoúrovňové kryptografie [CRYPTO-ELG](/en/docs/how/cryptography/)
- ECIES http://zzz.i2p/topics/2418
- [NTCP2](/en/docs/transport/ntcp2/) [Prop111](/en/proposals/111-ntcp2/)
- 123 Nové položky netDB
- 142 Nová šablona kryptografie
- [Noise](https://noiseprotocol.org/noise.html) protokol
- Dvojitý algoritmus ratchet [Signal](https://signal.org/docs/specifications/doubleratchet/)

Cílem je podpora nového šifrování pro komunikaci typu end-to-end, destination-to-destination.

Návrh použije Noise handshake a fázi dat, zahrnující dvojité ratchetování Signalu.

Všechny odkazy na Signal a Noise v tomto návrhu slouží pouze k poskytování základního kontextu.
Znalost protokolů Signal a Noise není vyžadována k pochopení nebo implementaci tohoto návrhu.


### Aktuální použití ElGamal

Jako připomínka,
veřejné klíče ElGamal velikosti 256 bajtů lze najít v následujících datových strukturách.
Odkazujte na specifikace společných struktur.

- V identitě routeru
  Toto je šifrovací klíč routeru.

- V Cíli
  Veřejný klíč cíle byl použit pro staré šifrování i2cp-to-i2cp,
  které bylo zakázáno ve verzi 0.6 a aktuálně se nepoužívá, s výjimkou
  IV pro šifrování LeaseSet, které je zastaralé.
  Místo toho je použit veřejný klíč v LeaseSet.

- V LeaseSet
  Toto je šifrovací klíč cíle.

- V LS2
  Toto je šifrovací klíč cíle.



### EncTypes v certifikátech klíče

Jako připomínka,
přidali jsme podporu typů šifrování, když jsme přidali podporu typů podpisů.
Pole typu šifrování je vždy nula, jak v Destinations, tak v RouterIdentities.
Zda to někdy změnit, je TBD.
Odkazujte na specifikace společných struktur [Common](/en/docs/spec/common-structures/).




### Použití Asymetrické kryptografie

Jako připomínka, používáme ElGamal pro:

1) Zprávy pro vytvoření tunelu (klíč je v RouterIdentity)
   Náhrada není pokryta v tomto návrhu.
   Viz návrh 152 [Prop152](/en/proposals/152-ecies-tunnels/).

2) Šifrování netdb a dalších I2NP zpráv mezi routery (Klíč je v RouterIdentity)
   Závisí na tomto návrhu.
   Vyžaduje návrh pro 1) také, nebo vložení klíče do RI možností.

3) Klient End-to-end ElGamal+AES/SessionTag (klíč je v LeaseSet, klíč Destination se nepoužívá)
   Náhrada JE pokryta v tomto návrhu.

4) Efemérní DH pro NTCP1 a SSU
   Náhrada není pokryta v tomto návrhu.
   Viz návrh 111 pro NTCP2.
   Neexistuje žádný současný návrh pro SSU2.


### Cíle

- Kompatibilní se staršími verzemi
- Vyžaduje a staví na LS2 (návrh 123)
- Využití nové kryptografie nebo primitiv přidaných pro NTCP2 (návrh 111)
- Nepožaduje nové kryptografie nebo primitiv pro podporu
- Zachování oddělení kryptografie a podepisování; podpora všech aktuálních a budoucích verzí
- Umožnění nového šifrování pro cíle
- Umožnění nového šifrování pro routery, ale pouze pro garlic zprávy - sestavení tunelů by byla samostatný návrh
- Nezničení nic, co spoléhá na 32-bytové binární hashování destinací, např. bittorrent
- Zachování 0-RTT doručování zpráv pomocí efemérně-statické DH
- Nepožadování ukládání zpráv do vyrovnávací paměti / fronty na této úrovni protokolu; nadále podporovat neomezené doručování zpráv v obou směrech bez čekání na odpověď
- Upgrade na efemérně-efemérní DH po 1 RTT
- Zachování zpracování zpráv mimo pořadí
- Zachování 256-bitové bezpečnosti
- Přidání forward secrecy
- Přidání autentizace (AEAD)
- Mnohem efektivnější CPU než ElGamal
- Nezávislost na Java jbigi pro efektivitu DH
- Minimalizace operací DH
- Mnohem efektivnější přenosové pásmo než ElGamal (514 bytů v bloku ElGamal)
- Podpora nová a staré kryptografie na stejném tunelu, pokud je to žádoucí
- Příjemce je schopen efektivně rozlišovat novou od staré kryptografie, která přichází po stejném tunelu
- Ostatní nemohou rozlišovat novou od staré nebo budoucí kryptografie
- Odstranění klasifikace délky nové vs. existující relace (podpora vycpávky)
- Nejsou zapotřebí žádné nové zprávy I2NP
- Nahrazení kontrolního součtu SHA-256 u AES užitečného zatížení pomocí AEAD
- Podpora vázání přenosových a přijímacích relací, aby potvrzení mohla probíhat v rámci protokolu, spíše než pouze mimo pásmo.
  To také umožní, aby odpovědi měly okamžitou úroveň forward secrecy.
- Umožnění end-to-end šifrování určitých zpráv (uložení RouterInfo), které v současnosti nezabezpečujeme kvůli zatížení CPU.
- Nezměnění I2NP Garlic Message
  nebo Garlic Message Delivery Instructions formátu.
- Odstranění nepoužívaných nebo redundantních polí v Garlic Clove Set a Clove formátech.

Odstranění několika problémů se session tagy, včetně:

- Nemožnosti použít AES do první odpovědi
- Nespolehlivosti a záseků, pokud se dodání tagu předpokládá
- Neefektivnosti přenosového pásma, zejména při prvním dodání
- Obrovské neefektivity úložiště pro ukládání tagů
- Obrovských režijních nákladů přenosového pásma na dodání tagů
- Vysoce složitých, obtížně implementovatelných
- Obtížného ladění pro různé případy použití
  (streamování vs. datagramy, server vs. klient, vysoké vs. nízké přenosové pásmo)
- Zranitelností vyčerpání paměti kvůli dodání tagů


### Nelze považovat za cíl / Mimo rozsah

- Změny formátu LS2 (návrh 123 je hotov)
- Nový algoritmus rotace DHT nebo generování sdíleného náhodného čísla
- Nové šifrování pro sestavení tunelu.
  Viz návrh 152 [Prop152](/en/proposals/152-ecies-tunnels/).
- Nové šifrování pro vrstvu tunelu.
  Viz návrh 153 [Prop153](/en/proposals/153-ecies-garlic/).
- Metody šifrování, přenosu a příjmu zpráv I2NP DLM / DSM / DSRM.
  Nezměněno.
- Žádná komunikace LS1-to-LS2 nebo ElGamal/AES-to-tento-návrh není podporována.
  Tento návrh je obousměrný protokol.
  Destinace mohou zpracovat zpětnou kompatibilitu publikováním dvou leasesetů
  pomocí stejných tunelů nebo umístit oba typy šifrování do LS2.
- Změny modelu ohrožení
- Podrobnosti o implementaci zde nejsou řešeny a jsou ponechány na každý projekt.
- (Optimistické) Přidání rozšíření nebo háčků na podporu multicast


### Zdůvodnění

ElGamal/AES+SessionTag byl naším jediným end-to-end protokolem asi 15 let,
prakticky bez úprav protokolu.
Nyní existují kryptografické primitivy, které jsou rychlejší.
Potřebujeme zvýšit bezpečnost protokolu.
Rovněž jsme vyvinuli heuristické strategie a alternativy, abychom minimalizovali
nezaplevelené využívání paměti a pásma protokolu, ale tyto strategie
jsou křehké, obtížné na ladění a činí protokol ještě náchylnějším
k poruchám, které by způsobily přerušení relace.

Přibližně za stejnou dobu období specifikace a související
dokumentace ElGamal/AES+SessionTag popisovaly, jak finančně nákladné je doručování session tagů,
a navrhovaly nahrazení doručování session tagů "synchronizovaným PRNG".
Synchronizovaný PRNG deterministicky generuje stejné tagy na obou koncích,
odvozené z běžného semene.
Synchronizovaný PRNG může být také označen jako "ratchet".
Tento návrh (konečně) specifikuje tento mechanismus ratchetů a eliminuje doručování tagů.

Pomocí ratchetu (synchronizovaného PRNG) pro generování
session tagů eliminujeme režii odesílání session tagů
v nové session zprávě a následujících zprávách, když je to žádoucí.
Pro typickou sadu tagů s 32 tagy to představuje 1 KB.
Tímto také eliminujeme úložiště session tagů na odesílající straně,
což snižuje požadavky na úložiště na polovinu.

Úplný obousměrný handshake, podobný Noise IK patternu, je potřebný pro zamezení útoků Key Compromise Impersonation (KCI).
Viz tabulka "Payload Security Properties" v [NOISE](https://noiseprotocol.org/noise.html).
Pro více informací o KCI viz článek https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf


### Model ohrožení

Model hrozby je poněkud odlišný od NTCP2 (návrh 111).
MitM uzly jsou OBEP a IBGW a předpokládá se, že mají plný přehled o
aktuální nebo historické globální NetDB, prostřednictvím kolaborace s floodfills.

Cílem je zabránit těmto MitM v klasifikaci provozu jako
nové a existující sessions zprávy, nebo jako nové kryptografické a staré kryptografické.



## Podrobný návrh

Tento návrh definuje nový end-to-end protokol, který nahradí ElGamal/AES+SessionTags.
Design využije Noise handshake a fázi dat, která začleňuje Signalův double ratchet.


### Přehled kryptografického návrhu

Existuje pět částí protokolu, které je třeba předesignovat:


- 1) Nové a stávající formáty kontejnerů Session
  jsou nahrazeny novými formáty.
- 2) ElGamal (256 byte veřejné klíče, 128 byte soukromé klíče) bude nahrazen
  ECIES-X25519 (32 byte veřejné a soukromé klíče)
- 3) AES bude nahrazen
  AEAD_ChaCha20_Poly1305 (dále zkráceno jako ChaChaPoly níže)
- 4) SessionTags budou nahrazeny ratchety,
  což je v podstatě kryptografický, synchronizovaný PRNG.
- 5) AES užitečné zatížení, jak je definováno ve specifikaci ElGamal/AES+SessionTags,
  bude nahrazeno blokovým formátem podobným tomu v NTCP2.

Každá z pěti změn má svou vlastní sekci níže.


### Nové kryptografické primitivy pro I2P

Stávající implementace routeru I2P budou vyžadovat implementaci následujících standardních kryptografických primitiv,
které nejsou vyžadovány pro aktuální I2P protokoly:

- ECIES (ale to je v podstatě X25519)
- Elligator2

Stávající implementace routeru I2P, které dosud neimplementovaly [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/)
  budou rovněž vyžadovat implementace pro:

- X25519 generování klíčů a DH
- AEAD_ChaCha20_Poly1305 (dále zkráceno jako ChaChaPoly níže)
- HKDF


### Crypto Type

Crypto typ (používaný v LS2) je 4.
To znamená little-endian 32-bytový X25519 veřejný klíč,
a end-to-end protokol specifikovaný zde.

Crypto typ 0 je ElGamal.
Crypto typy 1-3 jsou vyhrazeny pro ECIES-ECDH-AES-SessionTag, viz návrh 145 [Prop145](/en/proposals/145-ecies/).


### Noise Protocol Framework

Tento návrh poskytuje požadavky založené na Noise Protocol Framework
[NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11).
Noise má podobné vlastnosti jako protokol Station-To-Station
[STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), který je základem pro protokol [SSU](/en/docs/transport/ssu/). V terminologii Noise je Alice
iniciátor a Bob je respondent.

Tento návrh je založen na Noise protokolu Noise_IK_25519_ChaChaPoly_SHA256.
(Skutečný identifikátor pro iniciální funkci odvození klíče
je "Noise_IKelg2_25519_ChaChaPoly_SHA256"
pro indikaci rozšíření I2P - viz sekce KDF 1 níže)
Tento Noise protokol používá následující primitiva:

- Interaktivní Handshake Pattern: IK
  Alice okamžitě přenáší svůj statický klíč Bobovi (I)
  Alice zná Bobův statický klíč již dříve (K)

- Jednocestný Handshake Pattern: N
  Alice nepřenáší svůj statický klíč Bobovi (N)

- DH funkce: X25519
  X25519 DH s délkou klíče 32 bajtů, jak je specifikováno v [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Funktion šifry: ChaChaPoly
  AEAD_CHACHA20_POLY1305, jak je specifikováno v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8.
  12-bytový nonce s prvními 4 bajty nastavenými na nulu.
  Identické s tím v [NTCP2](/en/docs/transport/ntcp2/).

- Hash funkce: SHA256
  Standardní 32-bytový hash, již široce používaný v I2P.


Doplnění k Framework
````````````````````````

Tento návrh definuje následující vylepšení
Noise_IK_25519_ChaChaPoly_SHA256. Tyto postupují podle pokynů v
[NOISE](https://noiseprotocol.org/noise.html) sekce 13.

1) Efemérní klíče jsou kódovány pomocí [Elligator2](https://elligator.org/).

2) Odpověď je předponována s čitelným tagem.

3) Formát payloadu je definován pro zprávy 1, 2 a datovou fázi.
   Samozřejmě, toto není definováno v Noise.

Všechny zprávy zahrnují záhlaví [I2NP](/en/docs/spec/i2np/) Garlic Message.
Datová fáze používá šifrování podobné, ale neslučitelné s fázou dat Noise.


### Handshake Patterns

Handshakes používají [Noise](https://noiseprotocol.org/noise.html) handshake patterns.

Používá se následující mapování písmen:

- e = jednorázový efemérní klíč
- s = statický klíč
- p = užitečné zatížení zprávy

Jednorázové a nevázané relace jsou podobné Noise N patternu.

```dataspec

<- s
  ...
  e es p ->


```

Vázané relace jsou podobné Noise IK patternu.

```dataspec

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->


```


### Relace

Aktuálně je protokol ElGamal/AES+SessionTag jednosměrný.
Na této vrstvě protokolu příjemce nezná, odkud zpráva pochází.
Odchozí a příchozí relace nejsou spojeny.
Potvrzení jsou mimo pásmo pomocí zprávy DeliveryStatusMessage
(zabalené v GarlicMessage) ve hřebenu [clove].

Existuje značná neefektivita v jednosměrném protokolu.
Každá odpověď musí také využít drahou zprávu 'New Session'.
To způsobuje vyšší náklady na šířku pásma, CPU a paměť.

Existují také bezpečnostní slabiny v jednosměrném protokolu.
Všechny sessions jsou založeny na efemérně-statické DH.
Bez cesty zpět neexistuje způsob, jakým by Bob mohl "ratchetovat" svůj statický klíč
na efemérní klíč.
Bez znalosti odkud zpráva pochází, není žádný způsob, jak použít
přijatý efemérní klíč pro odchozí zprávy,
takže počáteční odpověď také využívá efemérně-statickou DH.

Pro tento návrh definujeme dva mechanismy pro vytvoření obousměrného protokolu -
"párování" a "vazbu".
Tyto mechanismy poskytují zvýšenou efektivitu a bezpečnost.


Kontext relace
``````````````````

Stejně jako u ElGamal/AES+SessionTags musí být všechny příchozí a odchozí relace ve daném kontextu, buď v kontextu routeru, nebo v kontextu pro konkrétní místní destinaci.
V Javě I2P se tento kontext nazývá Správce Klíčů Session Key Manager.

Relace by neměly být sdíleny mezi kontexty, protože by to umožňovalo korelaci mezi různými místními destinationemi nebo mezi místní destination a routerem.

Když daná destination podporuje jak ElGamal/AES+SessionTags, tak tento návrh, oba typy relací mohou sdílet kontext.
Viz oddíl 1c) níže.



Párování Příchozích a Odchozích Relací
`````````````````````````````````````

Když je na počátku (u Alice) vytvořena odchozí relace,
vytvoří se nová příchozí relace a je spárována s odchozí relací,
pokud se neočekává žádná odpověď (například hrubé datagramy).

Nová příchozí relace je vždy spárována s novou odchozí relací,
pokud není žádná požadována odpověď (například hrubé datagramy).

Pokud je požadována odpověď a vázána na cílovou destinaci nebo router,
nová odchozí relace je vázána na tuto destinaci nebo router,
a nahrazuje jakoukoliv předchozí odchozí relaci k této destinaci nebo routeru.

Párováním příchozích a odchozích relací získáme obousměrný protokol
s možností ratchetingu klíčů DH.



Vázání Relací a Destination
````````````````````````````

Existuje pouze jedna odchozí relace k dané destinaci nebo routeru.
Existuje několik aktuálních příchozích relací z určené destinace nebo routeru.
Obecně platí, že když je vytvořena nová příchozí relace a přijatým provozem je tato session potvrzením, ostatní budou relativně rychle označeny k vypršení, během minuty nebo tak.
Zkontroluje se přijímané hodnota (PN), a pokud nejsou v předchozí příchozí relaci žádné nepřijaté zprávy (v okně velikosti), předchozí relace může být okamžitě smazána.


Když je na počátku (u Alice) vytvořena odchozí relace,
je vázána na dálkovou Destination (Bob),
a jakákoli spojená příchozí relace bude také vázána na dálkovou Destination.
Jak se relace ratchetuje, zůstávají vázány na dálkovou Destination.

Když je u přijímače (u Boba) vytvořena příchozí relace,
může být vázána na dálkovou Destination, volitelně u Alici.
Pokud Alice zahrnuje informace o vázání (svůj statický klíč) ve zprávě New Session,
bude relace vázána na tuto destinaci,
a odchozí relace bude vytvořena a vázána na stejnou Destinaci.
Jak se relace ratchetuje, zůstávají vázány na dálkovou Destination.


Výhody Vázání a Párování
`````````````````````````````

V případě streamování očekáváme, že Alice a Bob využijí protokol následujícím způsobem:

- Alice spáruje svou novou odchozí relaci k nové příchozí relaci, obě vázané na dálkovou destination (Bob).
- Alice zahrnuje informace o vázání a podpis, a žádost o odpověď ve
  New Session zprávě poslané Bobovi.
- Bob spáruje svou novou příchozí relaci k nové odchozí relaci, obě vázané na dálkovou destination (Alice).
- Bob odesílá odpověď (ack) Alice ve spárování session, s ratchetem na nový DH klíč.
- Alice ratchetuje na novou odchozí relaci s Bobovým novým klíčem, spárováno na stávající příchozí session.

Vázáním příchozí relace na dálkovou Destination a spárováním příchozí relace
na odchozí relaci vázanou na stejnou Destination, jsme schopni dosáhnout dvou hlavních výhod:

1) Počáteční odpověď od Boba k Alici používá efemérně-efemérní DH

2) Poté, co Alice obdrží Boba odpověď a ratchet, všechny následné zprávy od Alice k Bobovi
používají efemérně-efemérní DH.


Potvrzení zpráv
``````````````

V ElGamal/AES+SessionTags, když je LeaseSet zabalen jako garlic clove,
nebo jsou doručeny tagy, odesílající router požaduje ACK.
Toto je samostatná garlic clove obsahující Zprávu o dodání.
Z důvodu dodatečné bezpečnosti je Zpráva o dodání zabalena ve Garlic Message.
Tento mechanismus je mimo pásmo z pohledu protokolu.

V novém protokolu, protože jsou inbound a outbound relace spárovány,
můžeme mít ACKs v pásmu. Žádná samostatná clove není vyžadována.

Explicitní ACK je jednoduše Existující Session zpráva bez I2NP bloku.
Nicméně, v většině případů lze vyhnout explicitnímu ACK, protože existuje zpětný provoz.
Mohlo by být vhodné pro implementace počkat krátkou chvíli (možná sto ms)
před odesláním explicitního ACK, aby se dal čas na odpověď na úroveň streamování nebo aplikace.

Implementační řešení také budou muset odložit jakékoliv odeslání ACK dokud nebude
I2NP block zpracován, protože Garlic Message může obsahovat záznam Database Store Message
s lease setem. Nedávný lease set bude nezbytný pro směrování ACK,
a dálková destinace (obsažená v lease set) bude nezbytná pro
ověření statického klíče vázání.


Časy vypršení relace
````````````````````

Odchozí relace by měly vždy vypršet dříve než příchozí relace.
Jakmile odchozí relace vyprší a je vytvořena nová, bude také vytvořena nová spárovaná příchozí
relace. Pokud existovala stará příchozí relace,
bude dovoleno vypršet.


### Multicast

TBD


### Definice
Definujeme následující funkce odpovídající použítým kryptografickým stavebním blokům.

ZEROLEN
    prázdné pole bajtů

CSRNG(n)
    n-bajtový výstup z kryptograficky bezpečného generátoru náhodných čísel.

H(p, d)
    SHA-256 hash funkce, která bere personalizační řetězec p a data d, a
    generuje výstup o délce 32 bajtů.
    Jak je definováno v [NOISE](https://noiseprotocol.org/noise.html).
    || níže znamená připojení.

    Použijte SHA-256 následovně::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    SHA-256 hash funkce, která bere předchozí hash h a nová data d,
    a generuje výstup o délce 32 bajtů.
    || níže znamená připojení.

    Použijte SHA-256 následovně::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    ChaCha20/Poly1305 AEAD, jak je specifikováno ve [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Šifruje plaintext pomocí klíče k a nonce n, který MUSÍ být unikátní pro
        klíč k.
        Asociovaná data ad jsou volitelná.
        Vrací ciphertext, který má stejné velikost jako plaintext + 16 bajtů pro HMAC.

        Celý ciphertext musí být nerozlišitelný od náhodného, pokud je klíč tajný.

    DECRYPT(k, n, ciphertext, ad)
        Dešifruje ciphertext pomocí klíče k a nonce n.
        Asociovaná data ad jsou volitelná.
        Vrací plaintext.

DH
    X25519 veřejný klíčový dohodovací systém. Soukromé klíče o délce 32 bajtů, veřejné klíče o délce 32 bajtů, produkuje výstupy o délce 32 bajtů. Má následující
    funkce:

    GENERATE_PRIVATE()
        Vygeneruje nový soukromý klíč.

    DERIVE_PUBLIC(privkey)
        Vrací veřejný klíč odpovídající zadanému soukromému klíči.

    GENERATE_PRIVATE_ELG2()
        Vygeneruje nový soukromý klíč, který mapuje na veřejný klíč vhodný pro Elligator2 kódování.
        Všimněte si, že polovina náhodně generovaných soukromých klíčů nebude vhodná a musí být vyřazena.

    ENCODE_ELG2(pubkey)
        Vrací Elligator2-kódovaný veřejný klíč odpovídající zadanému veřejnému klíči (inverzní mapování).
        Kódované klíče jsou malé endianové.
        Kódovaný klíč musí být 256 bitový nerozlišitelný od náhodných dat.
        Viz sekce Elligator2 níže pro specifikaci.

    DECODE_ELG2(pubkey)
        Vrací veřejný klíč odpovídající zadanému Elligator2-kódovanému veřejnému klíči.
        Viz sekce Elligator2 níže pro specifikaci.

    DH(privkey, pubkey)
        Generuje sdílené tajemství z daného soukromého a veřejného klíče.

HKDF(salt, ikm, info, n)
    Kryptografická funkce odvozování klíče, která bere určité klíčové vstupní materiály ikm (které
    by měly mít dobrý entropii, ale nejsou vyžadovány, aby byly jednotným náhodným řetězcem), sůl
    o délce 32 bajtů a kontextové 'info' hodnoty, a produkuje výstup
    o délce n bajtů vhodný pro použití jako klíčový materiál.

    Použijte HKDF, jak je specifikováno v [RFC-5869](https://tools.ietf.org/html/rfc5869), pomocí hashové funkce HMAC SHA-256
    jak je specifikováno v [RFC-2104](https://tools.ietf.org/html/rfc2104). To znamená, že SALT_LEN má maximálně 32 bajtů.

MixKey(d)
    Použijte HKDF() s předchozí chainKey a nová data d, a
    nastaví novou chainKey a k.
    Jak je definováno v [NOISE](https://noiseprotocol.org/noise.html).

    Použijte HKDF následovně::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Formát zprávy


Přehled stávajícího formátu zprávy
``````````````````````````````````

Garlic Message, jak je specifikováno v [I2NP](/en/docs/spec/i2np/) je následující.
Vzhledem k tomu, že designový cíl je, aby mezilehlé uzly nemohly rozlišovat mezi novou a starou kryptografií,
tento formát se nemění, i když je redundantní pole délky.
Formát je zobrazen s plným 16-bytovým záhlavím, i když
skutečné záhlaví může být v odlišném formátu v závislosti na použitému přenosu.

Po dešifrování data obsahují řadu Garlic Cloves a další
data, také známá jako Clove Set.

Viz [I2NP](/en/docs/spec/i2np/) pro podrobnosti a plnou specifikaci.


```dataspec

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+


```


Přehled formátu šifrovaných dat
````````````````````````````````

Aktuální formát zprávy, používaný více než 15 let, je ElGamal/AES+SessionTags.
V ElGamal/AES+SessionTags, existují dva formáty zpráv:

1) Nová relace:
- 514-bajtový blok ElGamal
- Blok AES (minimálně 128 bajtů, násobek 16)

2) Existující relace:
- 32-bajtový session tag
- Blok AES (minimálně 128 bajtů, násobek 16)

Minimální vyplnění na 128 je, jak je implementováno v Javě I2P, ale není vynuceno při přijetí.

Tyto zprávy jsou zapouzdřeny do I2NP garlic zprávy, která obsahuje
pole délky, takže délka je známa.

Všimněte si, že není definována žádná vyplňovací vyplňovaní do ne-mod-16 délky,
takže nová relace je vždy (mod 16 == 2),
a existující relace je vždy (mod 16 == 0).
To musíme opravit.

Příjemce nejprve zkusí vyhledat prvních 32 bajtů jako session tag.
Pokud je najde, dešifruje blok AES.
Pokud je nenajde a data jsou alespoň (514+16) dlouhá, zkusí dešifrovat blok ElGamal a pokud to uspěje, dešifruje blok AES.


Nové session tagy a srovnání se Signal
```````````````````````````````````````

V Signal Double Ratchet, obsahuje záhlaví:

- DH: Aktuální ratchet veřejného klíče
- PN: Délka předchozí řetězové zprávy
- N: Číslo zprávy

Signalovy "odesílací řetězce" jsou zhruba ekvivalentní našim sadám tagů.
Použitím session tagu můžeme většinu z toho eliminovat.

V Nové Session, klademe pouze veřejný klíč do nezašifrovaného záhlaví.

V Existující Session, používáme session tag pro záhlaví.
Session tag je spojen s aktuálním ratchet veřejným klíčem,
a číslem zprávy.

V obou, nová a Existující relace, PN a N jsou v zašifrovaném těle.

V Signal se věci neustále ratchetují. Nový DH veřejný klíč vyžaduje,
že příjemce ratchetuje a posílá nový veřejný klíč zpět, což také slouží
jako potvrzení pro přijatý veřejný klíč.
To by pro nás bylo příliš mnoho operací DH.
Takže oddělujeme potvrzení přijatého klíče a přenos nového veřejného klíče.
Každá zpráva používající session tag generovaný z nového DH veřejného klíče je potvrzení.
Nový veřejný klíč přenášíme, pouze pokud chceme přeskupit.

Maximální počet zpráv před tím, než musí DH ratchet, je 65535.

Při doručování session klíče odvozujeme "Set Tagů" z něj,
místo aby bylo potřeba doručit session tagy také.
Tag Set může mít až 65536 tagů.
Příjemci by však měli implementovat strategii "look-ahead", místo toho
aby generovali všechny možné tagy najednou.
Generujte pouze nejvýše N tagů za posledním dobrým tagem přijatým.
N může být maximálně 128, ale 32 nebo ještě méně může být lepší volbou.



### 1a) Nový formát session

Nová Session Jeden čas veřejného klíče (32 bytů)
Šifrovaná data a MAC (zbývající bajty)

Zpráva Nové Session může nebo nemusí obsahovat statický veřejný klíč odesílatele.
Je-li zahrnut, reverzní session je vázána na tento klíč.
Statický klíč by měl být zahrnut, pokud se očekávají odpovědi,
tj. pro streamování a repliable datagramy.
Neměl by být zahrnut pro hrubé datagramy.

Zpráva New Session je podobná jednocestnému Noise [NOISE](https://noiseprotocol.org/noise.html) patternu
"N" (pokud není statický klíč poslán),
nebo dvoucestnému patternu "IK" (pokud je statický klíč odeslán).



### 1b) Nový formát session (s vázáním)

Délka je 96 + délka payloadu.
Šifrovaný formát:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Efemérní Veřejný Klíč   |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Statický Klíč                 +
  |       ChaCha20 zašifrovaná data       |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro Sekci Statického Klíče     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitek Převodová     +
  |       ChaCha20 zašifrovaná data       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro Sekci Užitek Převodová     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Veřejný Klíč :: 32 bytes, malé endian, Elligator2, čitelný text

  Zašifrovaná data Statického Klíče :: 32 bytes

  Zašifrovaná data Sekce Užitek Převodová :: zbývající data bez 16 bajtů

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes


```


Nový Session Efemérní Klíč
```````````````````````````

Efemérní klíč je 32 bytes, kódován pomocí Elligator2.
Tento klíč se nikdy neopakuje; pro každou zprávu generujte nový klíč, včetně retransmisí.

Statický Klíč
````````````

Když je dešifrován, X25519 statický klíč Alice, 32 bytes.


Užitek Převodová
`````````

Zašifrovaná délka je zbytek dat.
Dešifrovaná délka je o 16 méně než zašifrovaná délka.
Payload musí obsahovat block DateTime a bude obvykle obsahovat jeden nebo více blocků Garlic Clove.
Viz sekce payloadu níže pro formát a další požadavky.



### 1c) Nový formát session (bez vázání)

Pokud se nevyžaduje odpověď, není odeslán žádný statický klíč.


Délka je 96 + délka užitku převodová.
Šifrovaný formát:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Efemérní Veřejný Klíč   |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Sekce Flags                 +
  |       ChaCha20 zašifrovaná data       |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +         (MAC) pro výše uvedenou sekci +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitek Převodová     +
  |       ChaCha20 zašifrovaná data       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro Sekci Užitek Převodová     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Veřejný Klíč :: 32 bytes, malé endian, Elligator2, čitelný text

  Zašifrovaná data Sekce Flags :: 32 bytes

  Zašifrovaná data Sekce Užitek Převodová :: zbývající data bez 16 bajtů

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes


```

Nový Session Efemérní Klíč
```````````````````````````

Aliceův efemérní klíč.
Efemérní klíč je 32 bytes, kódován pomocí Elligator2, malé endian.
Tento klíč se nikdy neopakuje; pro každou zprávu generujte nový klíč, včetně retransmisí.


Sekce Flags Dešifrovaná data
````````````````````````````

Sekce Flags neobsahuje nic.
Je vždy 32 bytes, protože musí být stejné délky
jako statický klíč pro New Session zprávy s vázáním.
Bob určuje, zda je to statický klíč nebo flags sekce
testováním, zda je všech 32 bajtů nulových.

TODO pokud bude potřebný nějaký flags?

Užitek Převodová
`````````

Zašifrovaná délka je zbytek dat.
Dešifrovaná délka je o 16 méně než zašifrovaná délka.
Payload musí obsahovat block DateTime a bude obvykle obsahovat jeden nebo více blocků Garlic Clove.
Viz sekce payloadu níže pro formát a další požadavky.




### 1d) Jeden-časový formát (žádné vázání ani session)

Pokud se očekává odeslání pouze jedné zprávy, není potřeba žádné nastavení session nebo statického klíče.


Délka je 96 + payload délka.
Šifrovaný formát:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Efemérní Veřejný Klíč            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Sekce Flags                 +
  |       ChaCha20 zašifrovaná data       |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +         (MAC) pro výše uvedenou sekci +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitek Převodová     +
  |       ChaCha20 zašifrovaná data       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro Sekci Užitek Převodová     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Veřejný Klíč :: 32 bytes, malé endian, Elligator2, čitelný text

  Zašifrovaná data Sekce Flags :: 32 bytes

  Zašifrovaná data Sekce Užitek Převodová :: zbývající data bez 16 bajtů

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes


```


Nový Session Jeden časový Klíč
``````````````````````````````

Jednorázový klíč je 32 bytes, kódován pomocí Elligator2, malé endian.
Tento klíč se nikdy neopakuje; pro každou zprávu generujte nový klíč,
včetně retransmisí.


Sekce Flags Dešifrovaná data
````````````````````````````````

Sekce Flags neobsahuje nic.
Je vždy 32 bytes, protože musí být stejné délky
jako statický klíč pro New Session zprávy s vazbou.
Bob určuje, zda je to statický klíč nebo sekce flags
testováním, zda je všech 32 bajtů nulových.

TODO pokud bude potřebný nějaký flags?

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             Samé nuly                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  nuly:: Samé nuly, 32 bytes.


```


Užitek Převodová
`````````

Zašifrovaná délka je zbytek dat.
Dešifrovaná délka je o 16 méně než zašifrovaná délka.
Užitek Převodová musí obsahovat block DateTime a bude obvykle obsahovat jeden nebo více blocků Garlic Clove.
Viz sekce payloadu níže pro formát a další požadavky.



### 1f) KDFs pro Novou Session Zprávu

KDF pro Iniciální ChainKey
````````````````````````````

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro IK s upraveným názvem protokolu.
Všimněte si, že používáme stejný inicializátor pro pattern IK (vázané relace)
a pro pattern N (nevázané relace).

Název protokolu je modifikován ze dvou důvodů.
Za prvé, k označení, že efemérní klíče jsou kódovány pomocí Elligator2,
a za druhé, k označení, že MixHash() je volán před druhou zprávou,
aby se smíchala hodnota tagu.

```text

Toto je "e" pattern zprávy:

  // Definujte protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bajtů, US-ASCII kódované, bez NULového ukončení).

  // Definujte Hash h = 32 bajtů
  h = SHA256(protocol_name);

  Definujte ck = 32-bajtový chaining klíč. Kopírujte data h do ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // až sem lze vše předpočítat Alica pro všechny odchozí spojení


```


KDF pro zašifrovaný obsah sekce Flags/Static Key
``````````````````````````````````````````````````

```text

Toto je "e" pattern zprávy:

  // Bobovy X25519 statické klíče
  // bpk je publikován v leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bobův statický veřejný klíč
  // MixHash(bpk)
  // || níže znamená připojení
  h = SHA256(h || bpk);

  // až sem lze vše předpočítat Bob pro všechny příchozí spojení

  // Aliciny X25519 efemérní klíče
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alicin efemérní veřejný klíč
  // MixHash(aepk)
  // || níže znamená připojení
  h = SHA256(h || aepk);

  // h se používá jako přidružená data pro AEAD ve zprávě New Session
  // Uchovávejte Hash h pro New Session Reply KDF
  // eapk je odesláno v nezašifrovaném textu na
  // začátek zprávy New Session
  elg2_aepk = ENCODE_ELG2(aepk)
  // Jak to dekóduje Bob
  aepk = DECODE_ELG2(elg2_aepk)

  Konec "e" pattern zprávy.

  Toto je "es" pattern zprávy:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parametry pro šifrování/dešifrování
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key sekce, ad)

  Konec "es" pattern zprávy.

  Toto je "s" pattern zprávy:

  // MixHash(ciphertext)
  // Uložit pro Payload sekce KDF
  h = SHA256(h || ciphertext)

  // Aliciny X25519 statické klíče
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  Konec "s" pattern zprávy.



```



KDF pro Payload sekci (s Aliciným statickým klíčem)
```````````````````````````````````````````````````

```text

Toto je "ss" pattern zprávy:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parametry pro šifrování/dešifrování
  // chainKey ze sekce Statický Klíč
  Set sharedSecret = X25519 DH výsledek
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  Konec "ss" pattern zprávy.

  // MixHash(ciphertext)
  // Uložit pro New Session Reply KDF
  h = SHA256(h || ciphertext)


```


KDF pro Payload Sekci (bez Aliciného statického klíče)
````````````````````````````````````````````````````

Všimněte si, že toto je Noise "N" pattern, ale používáme stejný "IK" inicializátor
jako u vázaných relací.

Nové Session zprávy nemohou být rozpoznány jako obsahující Alicin statický klíč nebo ne,
dokud není dešifrován statický klíč a zkontrolován, zda obsahuje pouze nuly.
Proto příjemce musí použít "IK" stavovou mašinu pro všechny
Nové Session zprávy.
Pokud je statický klíč samé nuly, "ss" pattern zprávy musí být přeskočeno.


```text

chainKey = ze sekce Flags/Static key
  k = ze sekce Flags/Static key
  n = 1
  ad = h ze sekce Flags/Static key
  ciphertext = ENCRYPT(k, n, payload, ad)


```



### 1g) Formát odpovědi na novou relaci

Jedna nebo více odpovědí na novou relaci může být zaslána jako reakce na jedinou zprávu New Session.
Každá odpověď je opatřena tagem, generovaným ze Session Tags pro relaci.

Odpověď na novou relaci je ve dvou částech.
První část je dokončení Noise IK handshake s předsunutým tagem.
Délka první části je 56 bytes.
Druhá část je payload datové fáze.
Délka druhé části je 16 + délka payloadu.

Celková délka je 72 + délka payloadu.
Šifrovaný formát:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Efemérní Veřejný Klíč           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro Sekci Klíč (bez dat)       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitek Převodová     +
  |       ChaCha20 zašifrovaná data       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +         (MAC) pro Sekci Užitek Převodová  +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, čitelný text

  Veřejný Klíč :: 32 bytes, malé endian, Elligator2, čitelný text

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes
         Upozornění: Data ChaCha20 plaintext jsou prázdná (ZEROLEN)

  Zašifrovaná data Sekce Užitek Převodová :: zbývající data minus 16 bytes

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes


```

Session Tag
```````````
Tag je generován v KDF pro Session Tags, jako iniciální
DH Inicializační KDF níže.
To koreluje odpověď na session.
Šifrovací Klíč ze DH Inicializace není použit.


Efemérní Klíč Odpovědi na Novou Session
````````````````````````````````````````
Bobův efemérní klíč.
Efemérní klíč je 32 bytes, kódovaný pomocí Elligator2, malé endian.
Tento klíč se nikdy neopakuje; pro každou zprávu generujte nový klíč, včetně retransmisí.


Užitek Převodová
`````````

Zašifrovaná délka je zbytek dat.
Dešifrovaná délka je o 16 méně než zašifrovaná délka.
Užitek Převodová obvykle obsahuje jeden nebo více blocků Garlic Clove.
Viz sekce payloadu níže pro formát a další požadavky.


KDF pro Odpovědní TagSet
``````````````````````````

Jeden nebo více tagů je vytvořeno z TagSet, který je inicializován pomocí
KDF níže, používající chainKey z New Session zprávy.

```text

// Generování tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)


```


KDF pro Zašifrovaný Obsah Sekce Klíč Odpovědi
``````````````````````````````````````````````

```text

// Klíče ze zprávy New Session
  // Aliciny X25519 klíče
  // apk a aepk jsou zaslány v původní zprávě New Session
  // ask = Alicin soukromý statický klíč
  // apk = Alicin veřejný statický klíč
  // aesk = Alicin efemérní soukromý klíč
  // aepk = Alicin efemérní veřejný klíč
  // Bobovy X25519 statické klíče
  // bsk = Bobův soukromý statický klíč
  // bpk = Bobův veřejný statický klíč

  // Generování tagu
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  Toto je "e" pattern zprávy:

  // Bobovy X25519 efemérní klíče
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bobův efemérní veřejný klíč
  // MixHash(bepk)
  // || níže znamená připojení
  h = SHA256(h || bepk);

  // elg2_bepk je zasláno v čitelném textu na
  // začátku zprávy Nové Session
  elg2_bepk = ENCODE_ELG2(bepk)
  // Jak ho dekóduje Bob
  bepk = DECODE_ELG2(elg2_bepk)

  Konec "e" pattern zprávy.

  Toto je "ee" pattern zprávy:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parametry pro šifrování/dešifrování
  // chainKey z původní New Session Payload Sekce
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Konec "ee" pattern zprávy.

  Toto je "se" pattern zprávy:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  Konec "se" pattern zprávy.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey je použit v ratchetu níže.


```


KDF pro Zašifrovaný Obsah Sekce Užitku
``````````````````````````````````````

Toto je jako první Existující Session zpráva,
po split, ale bez samostatného tagu.
Navíc používáme hash z výše uvedeného pro vázání
užitku na NSR zprávu.


```text

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parametry pro New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

```


### Poznámky

Více NSR zpráv může být zasláno jako odpověď, každá s unikátními efemérními klíči, v závislosti na velikosti odpovědi.

Alice a Bob musí používat nové efemérní klíče pro každou NS a NSR zprávu.

Alice musí obdržet jednu z Bobových NSR zpráv před odesláním Existující Session (ES) zpráv,
a Bob musí obdržet ES zprávu od Alice před odesláním ES zpráv.

``chainKey`` a ``k`` ze Sekce Užitku NSR jsou použity
jako vstupy pro iniciální ES DH ratchety (oba směry, viz DH Ratchet KDF).

Bob musí uchovat pouze Existující Relace pro ES zprávy přijaté od Alice.
Jakékoliv jiné vytvořené příchozí a odchozí relace (pro více NSR) by měly být
okamžitě po přijetí prvního ES zprávy od Alice pro danou relaci zničeny.



### 1h) Formát existující relace

Session tag (8 bytes)
Šifrovaná data a MAC (viz sekce 3 níže)


Formát
```````
Šifrované:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitek Převodová     +
  |       ChaCha20 zašifrovaná data       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, čitelný text

  Zašifrovaná data Sekce Užitek Převodová :: zbývající data bez 16 bajtů

  MAC :: Poly1305 ověřovací kód zprávy, 16 bytes


```


Užitek Převodová
`````````

Zašifrovaná délka je zbytek dat.
Dešifrovaná délka je o 16 méně než zašifrovaná délka.
Viz sekce payloadu níže pro formát a požadavky.


KDF
```

```text

Viz AEAD sekci níže.

  // AEAD parametry pro payload Existující Session
  k = 32-bytový session klíč spojený s tímto session tag
  n = Číslo zprávy N v aktuálním řetězci, jaké je uloženo s příslušným Session Tag.
  ad = session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)

```



### 2) ECIES-X25519


Formát: 32-bytové veřejné a soukromé klíče, malé-endian.

Odůvodnění: Používá se v [NTCP2](/en/docs/transport/ntcp2/).



### 2a) Elligator2

Ve standardních handshakes Noise zpráv, inicializační handshake zprávy v každém směru začínají
efemérními klíči, které se přenášejí v čitelném textu.
Protože platné klíče X25519 jsou rozlišitelné od náhod, Man-in-the-middle může tyto zprávy rozlišit od Existujících Session zpráv, které začínají náhodnými session tagy.
V [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/)), jsme použili nízko-režijní XOR funkci s použitím statického klíče mimo pásmo k obfuscování
klíče. Nicméně, model ohrožení je zde jiný; nechceme umožnit žádným MitM
jakýmikoli prostředky potvrdit cí destination provozu, nebo rozlišit
inicializační handshake zprávy od Existujících Session zpráv.

Proto je použit [Elligator2](https://elligator.org/) k transformování efemérních klíčů ve zprávách Nové Session a Nové Session Reply
tak, aby byly nerozlišitelné od jednotně náhodných řetězců.



Formát
``````

32-byte veřejné a soukromé klíče.
Zakódované klíče jsou malé endianové.

Jak je definováno v [Elligator2](https://elligator.org/), zakódované klíče jsou nerozlišitelné od 254 náhodných bitů.
Vyžadujeme 256 náhodných bitů (32 bytes). Proto jsou kódování a dekódování
definovány následujícím způsobem:

Kódování:

```text

Definice ENCODE_ELG2()

  // Kódování, jak je definováno ve specifikaci Elligator2
  encodedKey = encode(pubkey)
  // OR do 2 náhodných bitů do MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)

```


Dekódování:

```text

Definice DECODE_ELG2()

  // Maska 2 náhodných bitů z MSB
  encodedKey[31] &= 0x3f
  // Dekódování, jak je definováno ve specifikaci Elligator2
  pubkey = decode(encodedKey)

```




Odůvodnění
````````````

Je nezbytné zabránit, aby OBEP a IBGW klasifikovaly provoz.


Poznámky
````````

Elligator2 zdvojnásobuje střední čas generování klíče, protože polovina soukromých klíčů
výsledkem jsou veřejné klíče, které nejsou vhodné ke kódování pomocí Elligator2.
Také čas generování klíče není ohraničen exponeciálním rozdělením,
jak generátor musí neustále opakovat, dokud nenalezne vhodný pár klíčů.

Tato režie může být řízena generováním klíčů předem,
v samostatném vlákně, aby udržela pool vhodných klíčů.

Generátor provádí funkci ENCODE_ELG2() pro stanovení vhodnosti.
Proto by generátor měl uchovávat výsledek ENCODE_ELG2()
tak, aby jej nemusel znovu vypočítávat.

Navíc, nevhodné klíče mohou být přidány k poolu klíčů
používaných v [NTCP2](/en/docs/transport/ntcp2/), kde Elligator2 není používán.
Bezpečnostní otázky s tím spojené jsou
