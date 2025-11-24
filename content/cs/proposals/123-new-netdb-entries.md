```markdown
---
title: "Nové záznamy netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Otevřený"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Stav

Části tohoto návrhu jsou hotové a implementovány ve verzích 0.9.38 a 0.9.39. Společné struktury, I2CP, I2NP a další specifikace byly nyní aktualizovány, aby odrážely změny, které jsou nyní podporované.

Dokončené části jsou stále předmětem drobných úprav. Jiné části tohoto návrhu jsou stále ve vývoji a podléhají výrazným úpravám.

Vyhledání služby (typy 9 a 11) je nízkou prioritou a není naplánováno, může být odděleno do samostatného návrhu.


## Přehled

Toto je aktualizace a agregace následujících 4 návrhů:

- 110 LS2
- 120 Meta LS2 pro masivní multihoming
- 121 Šifrované LS2
- 122 Neexistence ověřování vyhledávání služby (anycasting)

Tyto návrhy jsou většinou nezávislé, ale kvůli přehlednosti definujeme a používáme společný formát pro několik z nich.

Následující návrhy jsou poněkud související:

- 140 Neviditelný Multihoming (nekompatibilní s tímto návrhem)
- 142 Nová šablona šifrování (pro nové symetrické šifrování)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 pro šifrované LS2
- 150 Protokol Garlic Farm
- 151 ECDSA Blinding


## Návrh

Tento návrh definuje 5 nových typů DatabaseEntry a proces pro jejich ukládání a získávání z databáze sítě, stejně jako metodu pro jejich podepisování a ověřování těchto podpisů.

### Cíle

- Zpětně kompatibilní
- LS2 použitelné se starým stylem multihomingu
- Nejsou vyžadována žádná nová šifrování nebo primitiva pro podporu
- Zachovat oddělení šifrování a podepisování; podpora všech současných a budoucích verzí
- Umožnit volitelné offline podpisové klíče
- Snížit přesnost časových razítek pro snížení fingerprintingu
- Umožnit nové šifrování pro destinace
- Umožnit masivní multihoming
- Opravit více problémů s existujícími šifrovanými LS
- Volitelné oslepování k redukci viditelnosti pomocí floodfills
- Šifrované podporuje jak jedno-, tak více revokovatelná klíče
- Vyhledávání služeb pro snadnější vyhledávání outproxy, bootstrap DHT aplikací a další použití
- Nezničit nic, co se spoléhá na 32-bytové binární hashování destinace, např. bittorrent
- Přidat flexibilitu k leasesetům prostřednictvím vlastností, jako máme v routerinfos
- Umístit zveřejněné časové razítko a proměnnou expiraci do záhlaví, takže to funguje i v případě, že obsah je šifrovaný (neodvozovat časové razítko z nejbližšího pronájmu)
- Všechny nové typy žijí ve stejném DHT prostoru a na stejných místech jako existující leasesets, aby uživatelé mohli migrovat ze starého LS do LS2, nebo měnit mezi LS2, Meta a šifrovanými, aniž by změnili destinaci nebo hash.
- Stávající destinace může být převedena k použití offline klíčů, nebo zpět na online klíče, aniž by se změnila destinace nebo hash.

### Necíle / Mimo rozsah

- Nový algoritmus rotace DHT nebo generování sdíleného náhodného čísla
- Konkrétní nový typ šifrování a schéma end-to-end šifrování, které používá tento nový typ, by byly v samostatném návrhu. Nejsou zde specifikována ani diskutována nová šifrování.
- Nové šifrování pro RIs nebo tvorbu tunelů. To by bylo v samostatném návrhu.
- Metody šifrování, přenosu a přijímání I2NP DLM / DSM / DSRM zpráv. Nezměněno.
- Jak generovat a podporovat Meta, včetně backendové komunikace mezi routery, řízení, failoveru a koordinace. Podpora by mohla být přidána do I2CP, nebo i2pcontrol, nebo nového protokolu. To nemusí být standardizované.
- Jak skutečně implementovat a řídit delší expirační časy tunelů, nebo zrušit existující tunely. To je extrémně obtížné a bez toho nelze mít rozumné elegantní vypnutí.
- Změny hrozeb
- Offline formát úložiště nebo metody pro ukládání, načítání a sdílení dat.
- Implementační detaily zde nejsou diskutovány a jsou ponechány na jednotlivých projektech.

### Oprávnění

LS2 přidává pole pro změnu typu šifrování a pro budoucí změny protokolu.

Šifrované LS2 opravuje několik bezpečnostních problémů se stávajícími šifrovanými LS pomocí asymetrického šifrování celé sady pronájmů.

Meta LS2 poskytuje flexibilní, efektivní, účinný a rozsáhlý multihoming.

Záznam služby a seznam služeb poskytují anycastové služby jako vyhledávání názvu a bootstrapping DHT.

### Typy dat NetDB

Čísla typů se používají ve zprávách I2NP Database Lookup/Store.

Sloupec end-to-end se týká toho, zda jsou dotazy / odpovědi poslány do destinace v Garlic Message.

Existující typy:

            NetDB Data               Lookup Type   Store Type 
any                                       0           any     
LS                                        1            1      
RI                                        2            0      
exploratory                               3           DSRM    

Nové typy:

            NetDB Data               Lookup Type   Store Type   Std. LS2 Header?   Sent end-to-end?
LS2                                       1            3             yes                 yes
Šifrované LS2                             1            5             no                  no
Meta LS2                                  1            7             yes                 no
Záznam služby                           n/a           9             yes                 no
Seznam služeb                              4           11             no                 no

Poznámky
- Lookup typy jsou aktuálně bity 3-2 v zprávě Database Lookup. 
  Jakékoli další typy by vyžadovaly použití bitu 4.

- Všechny typy úložiště jsou liché, protože horní bity v poli typu zprávy Database Store 
  jsou ignorovány starými routery. Rádi bychom, aby analýza selhala jako LS než 
  jako zkomprimovaný RI.

- Měl by být typ explicitní, implicitní, nebo ani jedno v datech pokrytých podpisem?

### Proces Lookup/Store

Typy 3, 5 a 7 mohou být vráceny jako odpověď na standardní lookup leasesetu (typ 1). Typ 9 nikdy není vrácen jako odpověď na lookup. Typy 11 jsou vráceny jako odpověď na nový typ lookup služby (typ 11).

Pouze typ 3 může být poslán v klient na klient Garlic Message.

### Formát

Typy 3, 7 a 9 mají společný formát::

  Standardní LS2 záhlaví
  - jak je uvedeno níže

  Část specifická pro typ
  - jak je uvedeno níže v každé části

  Standardní LS2 podpis:
  - Délka jak je naznačeno typem podpisu klíče podepisování

Typ 5 (šifrovaný) nezačíná destinací a má jiný formát. Viz níže.

Typ 11 (seznam služeb) je agregace několika záznamů služeb a má jiný formát. Viz níže.

### Ochrana soukromí a bezpečnostní úvahy

TBD

## Standardní LS2 záhlaví

Typy 3, 7, a 9 používají standardní LS2 záhlaví, specifikované níže:

### Formát
::

  Standardní LS2 záhlaví:
  - Typ (1 bajt)
    Ve skutečnosti není v záhlaví, ale je součástí dat pokrytých podpisem.
    Vezměte z pole ve zprávě Database Store.
  - Destinace (387+ bajtů)
  - Zveřejněné časové razítko (4 bajty, big endian, sekundy od epochy, přetéká v roce 2106)
  - Vyprší (2 bajty, big endian) (posun od zveřejněného časového razítka v sekundách, max. 18,2 hodiny)
  - Příznaky (2 bajty)
    Pořadí bitů: 15 14 ... 3 2 1 0
    Bit 0: Pokud 0, žádné offline klíče; pokud 1, offline klíče
    Bit 1: Pokud 0, běžný zveřejněný leaseset.
           Pokud 1, nezveřejněný leaseset. Neměl by být zaplaven, zveřejněn, nebo
           odeslán jako odpověď na dotaz. Pokud tento leaseset vyprší, neprovádět
           dotaz na netdb pro nový, pokud není bit 2 také nastaven.
    Bit 2: Pokud 0, běžný zveřejněný leaseset.
           Pokud 1, bude tento encryptovaný leaseset oslepen a šifrován
           při zveřejnění. Pokud tento leaseset vyprší, dotaz na oslepené
           umístění v netdb pro nový. Pokud je tento bit nastaven na 1, také
           nastavte bit 1 na 1. Od vydání 0.9.42.
    Bity 3-15: Nastavit na 0 pro kompatibilitu s budoucími použitími
  - Pokud příznak označuje offline klíče, offline podpisová sekce:
    Vyprší časové razítko (4 bajty, big endian, sekundy od epochy, přetéká v 2106)
    Přechodný typ podpisu (2 bajty, big endian)
    Přechodný veřejný klíč podpisu (délka jak je naznačeno typem podpisu)
    Podpis vypršení časového razítka, typ přechodného podpisu a veřejný klíč,
    podle veřejného klíče destinace,
    délka jak je naznačeno typem podpisu veřejného klíče destinace.
    Tato sekce může, a měla by, být generována offline.

Oprávnění
- Nezveřejněný/zveřejněný: Pro použití při odeslání databázového úložiště end-to-end,
  odesílající router může chtít naznačit, že by tento leaseset neměl být
  odesílán ostatním. V současnosti používáme heuristiky k udržování tohoto stavu.

- Zveřejněný: Nahrazuje složitou logiku potřebnou k určení 'verze' leasesetu.
  V současnosti je verze expirací posledního vypršujícího pronájmu
  a publikační router musí tuto expiraci zvýšit nejméně o 1 ms, když
  publikuje leaseset, který jen odstraňuje starší pronájem.

- Vyprší: Umožňuje expiraci netdb záznamu dříve, než je expirace jeho posledního
  expirovaného pronájmu. Může být neužitečné pro LS2, kde jsou leasesety očekávány
  zůstat s maximální ekspirační dobou 11 minut, ale pro ostatní nové typy, to
  je nezbytné (viz Meta LS a Záznam služby níže).

- Offline klíče jsou volitelné, k redukci počáteční/povinné implementační složitosti.

### Problémy

- Mohli bychom snížit přesnost časového razítka ještě více (10 minut?), ale museli bychom přidat
  verzi. To by mohlo narušit multihoming, pokud bychom neměli šifrování, které
  zachovává pořadí? Pravděpodobně se neobejdeme bez časových razítek úplně.

- Alternativa: 3-bytové časové razítko (epocha / 10 minut), 1-bytová verze, 2-byty vyprší

- Je typ explicitní nebo implicitní v datech / podpisu? "Doménová" konstanta pro podpis?

Poznámky
- Routery by neměly zveřejňovat LS více než jednou za sekundu.
  Pokud to udělají, musí uměle zvýšit zveřejněné časové razítko o 1
  oproti předtím zveřejněnému LS.

- Routerové implementace by mohly kešovat přechodné klíče a podpis, aby se
  vyhlo ověřování pokaždé. Zvláště floodfills a routery na
  obou koncích dlouhožilých připojení, by mohly z toho profitovat.

- Offline klíče a podpisy jsou vhodné pouze pro dlouhožící destinace, 
  tj. servery, ne klienty.

## Nové typy DatabaseEntry

### LeaseSet 2

Změny oproti existujícímu LeaseSet:

- Přidat zveřejněné časové razítko, vypršené časové razítko, příznaky a vlastnosti
- Přidat typ šifrování
- Odstranit klíč pro zrušení

Lookup s
    Standardní LS příznak (1)
Store s
    Standardní LS2 typ (3)
Store na
    Hash destinace
    Tento hash je pak použit k generování denního "routing key", jako v LS1
Typická expirace
    10 minut, jako v běžném LS.
Zveřejněno
    Destinací

Formát
::
```
  Standardní LS2 záhlaví jak bylo specifikováno výše

  Typická LS2 část specifická pro typ
  - Vlastnosti (Mapování jak bylo specifikováno ve specifikaci společných struktur, 2 nulové bajty pokud žádné)
  - Počet sekcí klíčů, které budou následovat (1 bajt, max TBD)
  - Sekce klíčů:
    - Typ šifrování (2 bajty, big endian)
    - Délka šifrovacího klíče (2 bajty, big endian)
      Toto je explicitní, aby floodfills mohly analyzovat LS2 s neznámými typy šifrování.
    - Šifrovací klíč (počet bajtů určený)
  - Počet lease2 (1 bajt)
  - Lease2s (40 bajtů každý)
    Toto jsou pronájmy, ale s 4-bytovou místo 8-bytové expirace,
    sekundy od epochy (přetéká v 2106)
  
  Standardní LS2 podpis:
  - Podpis
    Pokud příznak naznačuje offline klíče, je podepsán přechodným veřejným klíčem,
    jinak destinací veřejným klíčem
    Délka jak je naznačena typem podpisu klíče podepisování
    Podpis je všechno výše.

Oprávnění
- Vlastnosti: Budoucí rozšíření a flexibilita.
  Umístěno jako první v případě, že je nutné pro analýzu zbývajících dat.

- Více párů typů/veřejných klíčů šifrování jsou určené ke snadnější aktualizaci na nové typy šifrování. Druhou cestou je publikovat několik leasesetů, možná za použití stejných tunelů, jako teď pro DSA a EdDSA destinace.
  Identifikace příchozího typu šifrování na tunelu může být provedena pomocí stávajícího mechanismu tagu sezení, a/nebo pokusného dešifrování pomocí každého klíče. Délky příchozích zpráv mohou také poskytnout náznak.

Diskuze
Tento návrh pokračuje ve využívání veřejného klíče v leasesetu pro šifrovací klíč end-to-end a ponechává pole veřejného klíče v destinaci nepoužité, jak je tomu nyní. Typ šifrování není specifikován v certifikátu klíče destinace, zůstane 0.

Jednou zamítnutou alternativou je specifikovat typ šifrování v certifikátu klíče destinace, použít veřejný klíč v destinaci a nepoužívat veřejný klíč v leasesetu. Neplánujeme to udělat.

Výhody LS2:

- Poloha skutečného veřejného klíče se nemění.
- Typ šifrování nebo veřejný klíč může se změnit bez změny destinace.
- Odstraňuje nepoužité pole pro zrušení
- Základní kompatibilita s jinými typy DatabaseEntry v tomto návrhu
- Umožňuje více typů šifrování

Nevýhody LS2:

- Poloha veřejného klíče a typu šifrování se liší od RouterInfo
- Udržuje nepoužitý veřejný klíč v leasesetu
- Vyžaduje implementaci napříč sítí; v alternativě by experimentální typy šifrování mohly být použity, pokud jsou povoleny floodfills (ale viz související návrhy 136 a 137 o podpoře experimentálních typů podpisů).
  Alternativní návrh by mohl být snadnější implementovat a testovat pro experimentální typy šifrování.



### Šifrované LS2

Cíle:

- Přidat oslepování
- Umožnit různé typy podpisů
- Nevyžadovat žádná nová kryptografická primitiva
- Šifrovat volitelně pro každé příjemce, odvolatelné
- Podpora šifrování standardního LS2 a Meta LS2 pouze

Šifrované LS2 nikdy není posláno v end-to-end garlic message.
Použijte standardní LS2 jako výše.

Změny oproti existujícímu šifrovanému LeaseSet:

- Šifrovat celé kvůli bezpečnosti
- Šifrovat bezpečně, ne pouze s AES.
- Šifrovat pro každého příjemce

Lookup s
    Standardní LS příznak (1)
Store s
    Šifrované LS2 typ (5)
Store na
    Hash oslepeného typu podpisu a oslepeného veřejného klíče
    Dva bajty typu podpisu (big endian, např. 0x000b) || oslepený veřejný klíč
    Tento hash je pak použit k generování denního "routing key", jako v LS1
Typická expirace
    10 minut, jako v běžném LS, nebo hodiny, jako v meta LS.
Zveřejněno
    Destinací

Definice
CSRNG(n)
    n-bytový výstup z kryptograficky bezpečného generátoru náhodných čísel.

H(p, d)
    SHA-256 hashová funkce, která bere personalizační řetězec p a data d, a
    produkuje výstup o délce 32 bajtů.

STREAM
    Průběžná šifra ChaCha20, jak je specifikováno ve [RFC-7539-S2.4]_, s počátečním čítačem nastaveným na 1. S_KEY_LEN = 32 a S_IV_LEN = 12.

SIG
    RedDSA podpisové schéma (odpovídající SigType 11) s klíčovým oslepováním. Má následující funkce:

DH
    X25519 veřejný klíčový dohodový systém. Soukromé klíče o délce 32 bajtů, veřejné klíče o délce 32 bajtů, produkce výstupů o délce 32 bajtů. Má následující funkce:

HKDF(salt, ikm, info, n)
    Kryptografická funkce derivace klíčů, která vezme nějaký vstupklíčový materiál ikm (který by měl mít dobrou entropii, ale nemusí být vyžadováno, aby to byl jednotně náhodný řetězec), sůl o délce 32 bajtů a kontextově specifikovanou hodnotu 'info', a produkuje výstup o délce n bajtů vhodný k používání jako klíčový materiál.

Formát

Šifrovaný LS2 formát sestává ze tří vnořených vrstev:

- Venkovní vrstva obsahuje nezbytné plaintext informace pro ukládání a načítání.
- Střední vrstva řeší autentizaci klienta.
- Vnitřní vrstva obsahuje skutečná data LS2.

Celkový formát vypadá::

    Vrstva 0 data + Enc(vrstva 1 data + Enc(vrstva 2 data)) + Podpis

Všimněte si, že šifrované LS2 je oslepené. Destinace není v záhlaví. Umístění úložiště DHT je SHA-256(sig type || oslepený veřejný klíč) a rotuje denně.

Nepoužívá standardní LS2 záhlaví specifikované výše.

#### Vrstva 0 (venkovní)
Typ
    1 bajt

Oslepený typ podpisu veřejného klíče
    2 bajty, big endian

Oslepený veřejný klíč
    Délka jak je naznačeno typem podpisu

Zveřejněné časové razítko
    4 bajty, big endian

Vyprší
    2 bajty, big endian

Příznaky
    2 bajty

Přechodná data klíče
    Jsou přítomná, pokud příznak naznačuje offline klíče

lenOuterCiphertext
    2 bajty, big endian

outerCiphertext
    lenOuterCiphertext bajtů

Podpis

#### Vrstva 1 (střední)
Příznaky

DH data klientské autentifikace

PSK data klientské autentifikace

innerCiphertext

#### Vrstva 2 (vnitřní)
Typ

Data

Oslepovací odvození klíče

Používáme následující schéma pro oslepování klíčů, založené na Ed25519 a ZCash RedDSA [ZCASH]_. Red25519 podpisy jsou přes Ed25519 křivku, používající SHA-512 pro hash.

Nepoužíváme Torův rend-spec-v3.txt dodatek A.2 [TOR-REND-SPEC-V3]_, který má podobné návrhové cíle, protože jeho oslepené veřejné klíče mohou být mimo podskupinu práva, s neznámými bezpečnostními implikacemi.

Přehled

- Podepisující veřejný klíč v neoslabené destinaci musí být Ed25519 (sig type 7) nebo Red25519 (sig type 11). žádné jiné typy podpisů nejsou podporovány
- Pokud je podepisující veřejný klíč offline, přechodný podepisující veřejný klíč musí být také Ed25519
- Oslepování je výpočetně jednoduché
- Používejte existující kryptografická primitiva
- Oslepené veřejné klíče nelze odzavit
- Oslepené veřejné klíče musí být na Ed25519 křivce a na podskupině práva
- Musíte znát podepisující veřejný klíč destinace (celá destinace není vyžadována) pro odvození oslepeného veřejného klíče
- Volitelně poskytnout dodatečné tajemství potřebné pro odvožení oslepeného veřejného klíče

Blinding odvození klíče

Blinding výpočty

Podepisování

Podepisování a ověřování výpočtů

Vrstva 1 šifrování

Per-klientská autorizace

Výhody a nevýhody jednotlivých metod autentizace a autorizace

Oslepené LS s Base 32 adresami

Oslepené LS s offline klíči

Poznámky

### Meta LS2

Záznam služby

Seznam služeb

Specifikace struktur Spec Změny

Nové typy NetDB

Nový typ podpisu

Spec šifrování změn požadovaných

I2NP Změny požadované

Database Lookup Message

Database Store Message

I2CP Změny požadované

Možnosti I2CP

Konfig Session

Vyžádat Leaseset Message

Vyžádat Variabilní Leaseset Message

Vytvořit Leaseset2 Message

Justifikace

Format

Možnosti I2CP pro ověření a šifrování

Zpráva Blinding Info Message

Dataset CLI Změny požadované

Změny požadované pro Streaming a Repliable Datagram

SAM V3 Změny požadované

BOB Změny požadované

Zveřejnění, Migrační a Kompatibilní požadavky

Rollout

Uznání

Reference

```
