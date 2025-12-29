---
title: "ECIES Routery"
number: "156"
author: "zzz, originál"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## Poznámka
Síťové nasazení a testování probíhá.
Podléhá revizi.
Stav:

- ECIES Routery implementovány od verze 0.9.48, viz [Common](/docs/specs/common-structures/).
- Vytváření tunelů implementováno od verze 0.9.48, viz [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- Šifrované zprávy pro ECIES routery implementovány od verze 0.9.49, viz [ECIES-ROUTERS](/docs/specs/ecies/).
- Nové zprávy pro stavbu tunelů implementovány od verze 0.9.51.


## Přehled


### Shrnutí

Identifikátory routerů aktuálně obsahují šifrovací klíč ElGamal.
Toto je standard od počátků I2P.
ElGamal je pomalý a je potřeba jej nahradit ve všech místech, kde je používán.

Návrhy na LS2 [Prop123](/proposals/123-new-netdb-entries/) a ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
(nyní specifikován v [ECIES](/docs/specs/ecies/)) definovaly náhradu ElGamal ECIES
pro Destinace.

Tento návrh definuje náhradu ElGamal ECIES-X25519 pro routery.
Tento návrh poskytuje přehled nezbytných změn.
Většina podrobností je v jiných návrzích a specifikacích.
Viz sekci reference pro odkazy.


### Cíle

Viz [Prop152](/proposals/152-ecies-tunnels/) pro další cíle.

- Nahradit ElGamal ECIES-X25519 v Identifikátorech routerů
- Opětovné použití existujících kryptografických primitiv
- Zlepšit zabezpečení zpráv pro stavbu tunelů, kde je to možné, při zachování kompatibility
- Podpora tunelů se smíšenými ElGamal/ECIES partnery
- Maximalizace kompatibility se současnou sítí
- Nevyžaduje "flag day" upgrade celé sítě
- Postupné nasazení pro minimalizaci rizika
- Nová, menší zpráva pro stavbu tunelů


### Necíle

Viz [Prop152](/proposals/152-ecies-tunnels/) pro další necíle.

- Není potřeba routerů s dvojitým klíčem
- Změny vrstvy šifrování, pro to viz [Prop153](/proposals/153-chacha20-layer-encryption/)


## Návrh


### Umístění klíče a typ šifrování

Pro Destinace je klíč v leasesetu, nikoliv v Destination, a
podporujeme více typů šifrování ve stejném leasesetu.

Nic z toho není požadováno pro routery. Šifrovací klíč routeru
je v jeho Identitě routeru. Viz specifikace běžných struktur [Common](/docs/specs/common-structures/).

Pro routery nahradíme 256bitový ElGamal klíč v Identitě routeru
32bitovým X25519 klíčem a 224 bajtů wyplněné.
Toto bude indikováno typem šifrování v certifikátu klíče.
Typ šifrování (stejný jako použitý v LS2) je 4.
To indikuje malý-endian 32-bajtový X25519 veřejný klíč.
Toto je standardní konstrukce definovaná ve specifikaci běžných struktur [Common](/docs/specs/common-structures/).

Toto je identické s metodou navrhnutou pro ECIES-P256
pro typy šifrování 1-3 v návrhu 145 [Prop145](/proposals/145-ecies/).
I když tento návrh nebyl nikdy přijat, vývojáři Java implementace se připravili
na typy šifrování v certifikátech klíče Identity routeru přidáním kontrol
na několika místech ve zdrojovém kódu. Většina této práce byla dokončena v polovině roku 2019.


### Zpráva pro stavbu tunelu

Pro použití ECIES namísto ElGamal je potřeba několik změn ve specifikaci vytváření tunelu [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies).
Kromě toho provedeme zlepšení v zabezpečení zpráv pro stavbu tunelů.

Ve fázi 1 změníme formát a šifrování
Záznamu žádosti o stavbu a Záznamu odpovědi o stavbě pro ECIES přeskoky.
Tyto změny budou kompatibilní s existujícími ElGamal routery.
Tyto změny jsou definovány v návrhu 152 [Prop152](/proposals/152-ecies-tunnels/).

Ve fázi 2 přidáme novou verzi
Zprávy žádosti o stavbu, Zprávy odpovědi o stavbě,
Záznamu žádosti o stavbu a Záznamu odpovědi o stavbě.
Velikost bude snížena pro efektivitu.
Tyto změny musí být podporovány všemi přeskoky v tunelu a všechny přeskoky musí být ECIES.
Tyto změny jsou definovány v návrhu 157 [Prop157](/proposals/157-new-tbm/).


### Šifrování End-to-End

#### Historie

V původním návrhu Java I2P existoval jediný Správce ElGamal klíčů relace (SKM),
který sdílel router a všechny jeho lokální Destinace.
Protože sdílený SKM by mohl vyzradit informace a umožnit korelaci útočníky,
byl návrh změněn, aby podporoval samostatné ElGamal SKM pro router a každou Destinaci.
ElGamal návrh podporoval pouze anonymní odesílatele;
odesílatel posílal pouze efemérní klíče, nikoliv statický klíč.
Zpráva nebyla svázána s identitou odesílatele.

Poté jsme navrhli ECIES Ratchet SKM v
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/), nyní specifikovaném v [ECIES](/docs/specs/ecies/).
Tento návrh byl specifikován pomocí Noise "IK" vzoru, který zahrnoval statický klíč odesílatele v první zprávě. Tento protokol se používá pro ECIES (typ 4) Destinace.
IK vzor neumožňuje anonymní odesílatele.

Proto jsme do návrhu zahrnuli způsob, jak také posílat anonymní zprávy
Ratchet SKM, pomocí nulou vyplněného statického klíče. Toto simulovalo Noise "N" vzor,
ale kompatibilním způsobem, takže ECIES SKM mohl přijímat jak anonymní, tak neanonymní zprávy.
Úmysl byl použít nulový klíč pro ECIES routery.


#### Použití a model hrozeb

Použití a model hrozeb pro zprávy posílané routerům se velmi liší od
toho pro end-to-end zprávy mezi Destinacemi.


Použití a model hrozeb Destinace:

- Neanonymní od/do destinací (odesílatel zahrnuje statický klíč)
- Efektivně podporovat udržovaný provoz mezi destinacemi (plné handshake, streaming, a značky)
- Vždy posíláno přes výchozí a cílové tunely
- Skrytí všech identifikujících charakteristik před OBEP a IBGW, vyžadující Elligator2 kódování efemérních klíčů.
- Oba účastníci musí používat stejný typ šifrování


Použití a model hrozeb Routeru:

- Anonymní zprávy od routerů nebo destinací (odesílatel nezahrnuje statický klíč)
- Pouze pro šifrované databázové dotazy a uložené soubory, obvykle do floodfills
- Příležitostné zprávy
- Více zpráv by se nemělo korelovat
- Vždy posíláno přes výchozí tunel přímo k routeru. Žádné příchozí tunely nepoužity
- OBEP ví, že předává zprávu routeru a zná jeho typ šifrování
- Dva účastníci mohou mít různé typy šifrování
- Odpovědi na databázové dotazy jsou jednorázové zprávy používající odpovědní klíč a značku v databázové dotazovací zprávě
- Potvrzení databázových úložek jsou jednorázové zprávy používající připojenou zprávu o stavu doručení


Necíle použití routeru:

- Není potřeba neanonymních zpráv
- Není potřeba posílat zprávy přes příchozí průzkumné tunely (router nezveřejňuje průzkumné leasesety)
- Není potřeba pro trvalý provoz zpráv používající značky
- Není potřeba provozovat "dvojité klíče" Správce klíčů relace, jak je popsáno v [ECIES](/docs/specs/ecies/) pro Destinace. Routery mají pouze jeden veřejný klíč.


#### Závěry návrhu

ECIES Router SKM nepotřebuje plný Ratchet SKM, jak je specifikováno v [ECIES](/docs/specs/ecies/) pro Destinace.
Není požadavek na neanonymní zprávy pomocí IK vzoru.
Model hrozeb nevyžaduje Elligator2 kódované efemérní klíče.

Proto bude router SKM používat Noise "N" vzor, stejný jako specifikovaný
v [Prop152](/proposals/152-ecies-tunnels/) pro stavbu tunelů.
Bude používat stejný formát dat jako specifikovaný v [ECIES](/docs/specs/ecies/) pro Destinace.
Nulový statický klíč (bez vazby nebo relace) mód IK specifikovaný v [ECIES](/docs/specs/ecies/) nebude použit.

Odpovědi na dotazy budou šifrovány ratchet tagem, pokud budou vyžádány v dotazu.
To je dokumentováno v [Prop154](/proposals/154-ecies-lookups/), nyní specifikováno v [I2NP](/docs/specs/i2np/).

Návrh umožňuje routeru mít jediného ECIES Správce klíčů relace.
Není potřeba provozovat "dvojité klíče" Správce klíčů relace, jak
je popsáno v [ECIES](/docs/specs/ecies/) pro Destinace.
Routery mají pouze jeden veřejný klíč.

ECIES router nemá statický klíč ElGamal.
Router stále potřebuje implementaci ElGamal ke stavbě tunelů
přes ElGamal routery a posílání šifrovaných zpráv do ElGamal routerů.

ECIES router MŮŽE vyžadovat částečného Správce klíčů relace ElGamal k
příjmu ElGamal-označených zpráv přijatých jako odpovědi na NetDB dotazy
od pre-0.9.46 floodfill routerů, jelikož tyto routery nemají
implementaci ECIES-označených odpovědí, jak je specifikováno v [Prop152](/proposals/152-ecies-tunnels/).
Pokud ne, ECIES router nemusí žádat šifrovanou odpověď od
pre-0.9.46 floodfill routeru.

Toto je volitelné. Rozhodnutí se může lišit v různých implementacích I2P
a může záviset na tom, kolik sítě bylo upgradováno na
verzi 0.9.46 nebo vyšší.
K dnešnímu datu je přibližně 85% sítě ve verzi 0.9.46 nebo vyšší.


## Specifikace

X25519: Viz [ECIES](/docs/specs/ecies/).

Identita routeru a certifikát klíče: Viz [Common](/docs/specs/common-structures/).

Výstavba tunelů: Viz [Prop152](/proposals/152-ecies-tunnels/).

Nová zpráva o stavbě tunelů: Viz [Prop157](/proposals/157-new-tbm/).


### Šifrování žádostí

Šifrování žádostí je stejné jako specifikováno v [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) a [Prop152](/proposals/152-ecies-tunnels/),
používající Noise "N" vzor.

Odpovědi na dotazy budou šifrovány ratchet tagem, pokud budou vyžádány v dotazu.
Zprávy žádosti o databázový dotaz obsahující 32-bajtový odpovědní klíč a 8-bajtový odpovědní tag
jak je specifikováno v [I2NP](/docs/specs/i2np/) a [Prop154](/proposals/154-ecies-lookups/). Klíč a tag jsou používány k šifrování odpovědi.

Tag sety nejsou vytvářeny.
Nulový statický klíčový schéma specifikovaný v
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) a [ECIES](/docs/specs/ecies/) nebude použit.
Efemérní klíče nebudou Elligator2-kódovány.

Obecně se bude jednat o Nové zprávy relace a budou posílány s nulovým statickým klíčem
(bez vazby nebo relace), jelikož odesílatel zprávy je anonymní.


#### KDF pro počáteční ck a h

Toto je standard [NOISE](https://noiseprotocol.org/noise.html) pro vzor "N" s běžně používaným názvem protokolu.
Toto je stejné jako specifikováno v [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) a [Prop152](/proposals/152-ecies-tunnels/) pro zprávy o stavbě tunelů.


  ```text

Toto je "e" vzor zprávy:

  // Definovat protocol_name.
  Nastavit protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bajtů, US-ASCII kodované, bez nulového ukončení).

  // Definovat Hash h = 32 bajty
  // Pad na 32 bajtů. NEHASHovat to, protože nemá více než 32 bajtů.
  h = protocol_name || 0

  Definovat ck = 32 bajtový řetězový klíč. Zkopírovat data h do ck.
  Nastavit chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // až do této chvíle, toto může být předpočítáno všemi routery.


  ```


#### KDF pro zprávy

Tvořitelé zprávy generují efemérní X25519 klíčový pár pro každou zprávu.
Efemérní klíče musí být unikátní pro každou zprávu.
Toto je stejné jako specifikováno v [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) a [Prop152](/proposals/152-ecies-tunnels/) pro zprávy o stavbě tunelů.


  ```dataspec


// Statický klíčový pár X25519 cílového routeru (hesk, hepk) z Identity routeru
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || níže znamená příložit
  h = SHA256(h || hepk);

  // až do této chvíle, toto může být předpočítáno každým routerem
  // pro všechny příchozí zprávy

  // Odesílatel generuje efemérní X25519 klíčový pár
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Konec "e" vzoru zprávy.

  Toto je "es" vzor zprávy:

  // Noise es
  // Odesílatel provádí X25519 DH s cílovým statickým veřejným klíčem.
  // Cílový router
  // extrahuje efemérní klíč odesílatele před šifrovaným záznamem.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parametry ChaChaPoly pro šifrování/dešifrování
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Řetězový klíč není použit
  //chainKey = keydata[0:31]

  // Parametry AEAD
  k = keydata[32:63]
  n = 0
  plaintext = 464 bajtů záznamu o žádosti o stavbu
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Konec "es" vzoru zprávy.

  // MixHash(ciphertext) není vyžadován
  //h = SHA256(h || ciphertext)


  ```


#### Obsah

Obsah má stejný blokový formát jako definován v [ECIES](/docs/specs/ecies/) a [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Všechny zprávy musí obsahovat DateTime blok pro prevenci přehrání.


### Šifrování odpovědí

Odpovědi na zprávy o databázových dotazech jsou Databázové úložiště nebo Databázové vyhledávací odpovědi.
Jsou šifrovány jako Zprávy o existující relaci se
32-bajtovým odpovědním klíčem a 8-bajtovým odpovědním tagem
jak je specifikováno v [I2NP](/docs/specs/i2np/) a [Prop154](/proposals/154-ecies-lookups/).


Neexistují žádné explicitní odpovědi na zprávy o Databázovém úložišti. Odesílatel může spojit svou
vlastní odpověď jako Garlic Message pro sebe, obsahující zprávu o stavu doručení.


## Zdůvodnění

Tento návrh maximalizuje opětovné použití existujících kryptografických primitiv, protokolů a kódu.

Tento návrh minimalizuje riziko.


## Implementační poznámky

Starší routery nekontrolují typ šifrování routeru a budou posílat šifrované ElGamal
stavbové záznamy nebo netdb zprávy.
Některé nedávné routery obsahují chyby a budou posílat různé typy nesprávně tvarovaných stavbových záznamů.
Některé nedávné routery mohou posílat neanonymní (plný ratchet) netdb zprávy.
Implementátoři by měli detekovat a odmítat tyto záznamy a zprávy
co nejdříve, aby snížili použití CPU.


## Problémy

Návrh 145 [Prop145](/proposals/145-ecies/) může nebo nemusí být přepracován, aby byl většinově kompatibilní s
Návrhem 152 [Prop152](/proposals/152-ecies-tunnels/).


## Migrace

Implementace, testování a zavedení bude trvat několik vydání
a přibližně jeden rok. Fáze jsou následující. Přidělení
každé fáze do konkrétního vydání je bude stanoveno a závisí na
rychlosti vývoje.

Podrobnosti o implementaci a migraci se mohou lišit pro
každou implementaci I2P.


### Základní bodované spojení

ECIES routery mohou se připojovat k a přijímat spojení z ElGamal routerů.
Toto by mělo být možné nyní, protože do kódu Java byly již vloženy
kontroly v reakci na nedokončený návrh 145 [Prop145](/proposals/145-ecies/) do poloviny roku 2019.
Ujistit se, že nic v kódu nebrání bodovaným spojením s ne-ElGamal routery.

Kontroly správnosti kódu:

- Ujistit se, že ElGamal routery nežádají AEAD-šifrované odpovědi na Databázové dotazovací zprávy
  (když se odpověď vrátí exploratorním tunelem k routeru)
- Ujistit se, že ECIES routery nežádají AES-šifrované odpovědi na Databázové dotazovací zprávy
  (když se odpověď vrátí exploratorním tunelem k routeru)

Dokud nejsou specifikace a implementace kompletní:

- Ujistit se, že stavby tunelů nejsou pokoušeny ElGamal routery přes ECIES routery.
- Ujistit se, že šifrované ElGamal zprávy nejsou posílány ElGamal routery do ECIES floodfill routerů.
  (Databázové dotazy a Databázové úložiště)
- Ujistit se, že šifrované ECIES zprávy nejsou posílány ECIES routery do ElGamal floodfill routerů.
  (Databázové dotazy a Databázové úložiště)
- Ujistit se, že ECIES routery automaticky nepřevádějí na floodfill.

Žádné změny by neměly být vyžadovány.
Cílové vydání, pokud jsou požadovány změny: 0.9.48


### Kompatibilita NetDB

Ujistit se, že ECIES router infos mohou být uložené do a získávány z ElGamal floodfills.
Toto by mělo být možné nyní, protože do kódu Java byly již vloženy
kontroly v reakci na nedokončený návrh 145 [Prop145](/proposals/145-ecies/) do poloviny roku 2019.
Ujistit se, že nic v kódu nebrání ukládání ne-ElGamal RouterInfos v síťové databázi.

Žádné změny by neměly být vyžadovány.
Cílové vydání, pokud jsou požadovány změny: 0.9.48


### Výstavba tunelů

Implementace výstavby tunelů jak je definována v návrhu 152 [Prop152](/proposals/152-ecies-tunnels/).
Začněte tím, že ECIES router staví tunely se všemi ElGamal přeskoky;
použijte jeho vlastní záznam o žádosti o stavbu pro příchozí tunel k testování a ladení.

Poté otestujte a podportujte ECIES routery stavící tunely se směsí
ElGamal a ECIES přeskoků.

Poté umožněte výstavbu tunelů přes ECIES routery.
Není nutná žádná minimální verifikační kontrola verze, pokud nejsou po vydání provedeny neslučitelné změny
návrhu 152.

Cílové vydání: 0.9.48, pozdní rok 2020


### Ratchet zprávy pro ECIES floodfills

Implementace a testování přijetí ECIES zpráv (s nulovým statickým klíčem) ECIES floodfills,
jak je definováno v návrhu 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Implementace a testování přijetí AEAD odpovědí na Databázové dotazovací zprávy ECIES routery.

Umožnění automatického floodfill připojení ECIES routery.
Poté umožněte odesílání ECIES zpráv do ECIES routerů.
Není nutná žádná minimální verifikační kontrola verze, pokud nejsou po vydání provedeny neslučitelné změny
návrhu 152.

Cílové vydání: 0.9.49, začátek roku 2021.
ECIES routery mohou automaticky převádět na floodfill.


### Rekeying a nové instalace

Nové instalace budou ve výchozím nastavení ECIES od vydání 0.9.49.

Postupně změňte klíče všech routerů, aby se minimalizovalo riziko a přerušení sítě.
Použijte existující kód, který prováděl změnu klíčů pro migraci typu signatur před lety.
Tento kód dává každému routeru malou náhodnou šanci změny klíčů při každém restartu.
Po několika restartech robot pravděpodobně změnil klíč na ECIES.

Kritérium pro zahájení změny klíče je, že dostatečná část sítě,
možná 50%, může stavět tunely přes ECIES routery (verze 0.9.48 nebo vyšší).

Před agresivním změnou klíčů celé sítě musí většina
(možná 90% nebo více) schopna stavět tunely přes ECIES routery (verze 0.9.48 nebo vyšší)
A posílat zprávy do ECIES floodfills (verze 0.9.49 nebo vyšší).
Tento cíl pravděpodobně bude dosažen pro vydání verze 0.9.52.

Změna klíčů bude trvat několik vydání.

Cílové vydání:
0.9.49 pro nové routery jako výchozí ECIES;
0.9.49 pomalu začít změnu klíčů;
0.9.50 - 0.9.52 opakovaně zvyšovat rychlost změny klíčů;
pozdní rok 2021 pro většinu sítě, aby byla klíčovaná.


### Nová zpráva pro stavbu tunelů (Fáze 2)

Implementovat a otestovat novou zprávu pro stavbu tunelů, jak je definováno v návrhu 157 [Prop157](/proposals/157-new-tbm/).
Zavést podporu s vydáním 0.9.51.
Provést další testování, poté povolit ve vydání 0.9.52.

Testování bude obtížné.
Předtím, než to může být široce testováno, musí dobrá část sítě to podporovat.
Než to bude široce užitečné, většina sítě to musí podporovat.
Pokud budou po testování vyžadovány změny specifikace nebo implementace,
tato implementace bude zpožděna o další vydání.

Cílové vydání: 0.9.52, pozdní 2021.


### Rekeying dokončeno

V tomto okamžiku nebudou moci routery starší než některá verze TBD
stavět tunely přes většinu partnerů.

Cílové vydání: 0.9.53, začátek 2022.


## Odkazy

* [Common](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [ECIES-ROUTERS](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
* [Prop145](/proposals/145-ecies/)
* [Prop152](/proposals/152-ecies-tunnels/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop154](/proposals/154-ecies-lookups/)
* [Prop157](/proposals/157-new-tbm/)
* [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
