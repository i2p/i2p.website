---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Přehled

Tento návrh přidává nový typ podpisu používající BLAKE2b-512 s personalizačními řetězci a saltem, aby nahradil SHA-512. Tím se eliminují tři třídy možných útoků.

## Motivace

Během diskusí a návrhu NTCP2 (návrh 111) a LS2 (návrh 123) jsme stručně zvažovali různé možné útoky a jak jim zabránit. Tři z těchto útoků jsou útoky na rozšíření délky, útoky mezi protokoly a identifikace duplicitních zpráv.

Pro NTCP2 i LS2 jsme se rozhodli, že tyto útoky nejsou přímo relevantní pro dané návrhy a jakákoli řešení byla v konfliktu s cílem minimalizovat nové primitivy. Také jsme zjistili, že rychlost hashovacích funkcí v těchto protokolech nebyla důležitým faktorem v našich rozhodnutích. Proto jsme řešení většinou odložili na samostatný návrh. Přestože jsme do specifikace LS2 přidali některé personalizační prvky, nevyžadovali jsme žádné nové hashovací funkce.

Mnoho projektů, jako například ZCash [ZCASH]_, používá hashovací funkce a algoritmy podpisu založené na novějších algoritmech, které nejsou zranitelné vůči následujícím útokům.

### Útoky na rozšíření délky

SHA-256 a SHA-512 jsou zranitelné vůči útokům na rozšíření délky (LEA) [LEA]_. To je případ, když jsou podepsána skutečná data, a ne hash dat. Ve většině I2P protokolů (streaming, datagramy, netdb a další) jsou podepisována skutečná data. Jednou výjimkou jsou soubory SU3, kde je podepisován hash. Další výjimkou jsou podepisované datagramy pro DSA (typ podpisu 0) pouze, kde je podepisován hash. Pro jiné typy podepisovaných datagramů jsou podepisována data.

### Útoky mezi protokoly

Podepisovaná data v I2P protokolech mohou být zranitelná vůči útokům mezi protokoly (CPA) kvůli nedostatku doménového oddělení. To umožňuje útočníkovi použít data přijatá v jednom kontextu (například podepsaný datagram) a prezentovat je jako platná, podepsaná data v jiném kontextu (například streamování nebo databáze sítě). Zatímco je nepravděpodobné, že podepsaná data z jednoho kontextu by byla analyzována jako platná data v jiném kontextu, je obtížné nebo nemožné analyzovat všechny situace, aby se vědělo s jistotou. Navíc, v některém kontextu, může být možné, aby útočník přiměl oběť podepsat speciálně vytvořená data, která by mohla být platnými daty v jiném kontextu. Opět je obtížné nebo nemožné analyzovat všechny situace, aby se vědělo s jistotou.

### Identifikace duplicitních zpráv

I2P protokoly mohou být zranitelné vůči identifikaci duplicitních zpráv (DMI). To může umožnit útočníkovi identifikovat, že dvě podepsané zprávy mají stejný obsah, i když jsou tyto zprávy a jejich podpisy zašifrovány. Zatímco je to kvůli šifrovacím metodám používaným v I2P nepravděpodobné, je obtížné nebo nemožné analyzovat všechny situace, aby se vědělo s jistotou. Použitím hashovací funkce, která poskytuje metodu přidání náhodného saltu, budou všechny podpisy odlišné, i když podepisujete stejná data. Zatímco Red25519, jak je definováno v návrhu 123, přidává náhodný salt do hashovací funkce, neřeší to problém pro nešifrované lease sety.

### Rychlost

I když to není hlavní motivace pro tento návrh, SHA-512 je relativně pomalý a rychlejší hashovací funkce jsou k dispozici.

## Cíle

- Zabraňte výše uvedeným útokům
- Minimalizujte použití nových kryptografických primitiv
- Používejte osvědčené, standardní kryptografické primitivy
- Používejte standardní křivky
- Používejte rychlejší primitivy, pokud jsou k dispozici

## Návrh

Změňte existující typ podpisu RedDSA_SHA512_Ed25519 tak, aby používal BLAKE2b-512 namísto SHA-512. Přidejte unikátní personalizační řetězce pro každý případ použití. Nový typ podpisu může být použit pro nezaslepené i zaslepené lease sety.

## Ospravedlnění

- BLAKE2b není zranitelný vůči LEA [BLAKE2]_.
- BLAKE2b poskytuje standardní způsob přidání personalizačních řetězců pro doménové oddělení
- BLAKE2b poskytuje standardní způsob přidání náhodného saltu k zamezení DMI.
- BLAKE2b je rychlejší než SHA-256 a SHA-512 (a MD5) na moderním hardwaru, podle [BLAKE2]_.
- Ed25519 je stále náš nejrychlejší typ podpisu, mnohem rychlejší než ECDSA, alespoň v Java.
- Ed25519 [ED25519-REFS]_ vyžaduje 512bitovou kryptografickou hashovací funkci. Neurčuje SHA-512. BLAKE2b je stejně vhodný pro hashovací funkci.
- BLAKE2b je široce dostupný v knihovnách pro mnoho programovacích jazyků, například Noise.

## Specifikace

Použijte nepodepsaný BLAKE2b-512, jak je uvedeno v [BLAKE2]_, se saltem a personalizací. Všechny použití BLAKE2b podpisů použijí 16znakový personalizační řetězec.

Při použití v podepisování RedDSA_BLAKE2b_Ed25519 je povolen náhodný salt, nicméně není nutný, protože algoritmus podpisu přidává 80 bajtů náhodných dat (viz návrh 123). Pokud je to žádoucí, při hašování dat pro výpočet r nastavte nový 16bajtový náhodný salt pro každý podpis. Při výpočtu S obnovte salt na výchozí hodnotu všech nul.

Při použití v ověřování RedDSA_BLAKE2b_Ed25519 nepoužívejte náhodný salt, použijte výchozí hodnotu všech nul.

Salt a personalizační funkce nejsou specifikovány v [RFC-7693]_; použijte tyto funkce, jak jsou specifikovány v [BLAKE2]_.

### Typ podpisu

Pro RedDSA_BLAKE2b_Ed25519 nahraďte hashovací funkci SHA-512 v RedDSA_SHA512_Ed25519 (typ podpisu 11, jak je definováno v návrhu 123) BLAKE2b-512. Žádné další změny.

Nepotřebujeme náhradu za EdDSA_SHA512_Ed25519ph (typ podpisu 8) pro soubory su3, protože předhašovaná verze EdDSA není zranitelná vůči LEA. EdDSA_SHA512_Ed25519 (typ podpisu 7) není podporován pro soubory su3.

=======================  ===========  ======  =====
        Typ              Typ kód    Od       Použití
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Pouze pro Router Identities, Destinations a šifrované lease sety; nikdy se nepoužívá pro Router Identities
=======================  ===========  ======  =====

### Společná datová délka struktury

Následující se vztahuje na nový typ podpisu.

==================================  =============
            Typ dat                  Délka    
==================================  =============
Hash                                     64      
Soukromý klíč                             32      
Veřejný klíč                              32      
Podpis                                   64      
==================================  =============

### Personalizace

Abychom poskytli doménové oddělení pro různá použití podpisů, použijeme funkci personalizace BLAKE2b.

Všechna použití BLAKE2b podpisů použijí 16znakový personalizační řetězec. Jakékoli nové použití musí být přidáno do tabulky zde s unikátní personalizací.

NTCP 1 a SSU handshake použití níže jsou pro podepisovaná data definovaná v samotném handshake. Podepsané RouterInfos v DatabaseStore Messages budou používat personalizaci NetDb Entry, stejně jako pokud jsou uloženy v NetDB.

==================================  ==========================
         Použití                      16 znaková personalizace
==================================  ==========================
I2CP SessionConfig                  "I2CP_SessionConf"
NetDB Entries (RI, LS, LS2)         "network_database"
NTCP 1 handshake                    "NTCP_1_handshake"
Podepisované datagramy              "sign_datagramI2P"
Streaming                           "streaming_i2psig"
SSU handshake                       "SSUHandshakeSign"
SU3 Files                           n/a, není podporováno
Jednotkové testy                    "test1234test5678"
==================================  ==========================

## Poznámky

## Problémy

- Alternativa 1: Návrh 146; Poskytuje odolnost vůči LEA
- Alternativa 2: Ed25519ctx v RFC 8032; Poskytuje odolnost vůči LEA a personalizaci. Standardizováno, ale někdo to používá? Viz [RFC-8032]_ a [ED25519CTX]_.
- Je "keyed" hashing užitečný pro nás?

## Migrace

Stejná jako u zavedení předchozích typů podpisů.

Plánujeme změnit nové routery z typu 7 na typ 12 jako výchozí. Plánujeme nakonec migrovat stávající routery z typu 7 na typ 12, pomocí "rekeying" procesu použitého po zavedení typu 7. Plánujeme změnit nové destinace z typu 7 na typ 12 jako výchozí. Plánujeme změnit nové šifrované destinace z typu 11 na typ 13 jako výchozí.

Podporujeme zaslepení z typů 7, 11 a 12 na typ 12. Nepodporujeme zaslepení typu 12 na typ 11.

Nové routery by mohly začít používat nový typ podpisu jako výchozí po několika měsících. Nové destinace by mohly začít používat nový typ podpisu jako výchozí po možná roce.

Pro minimální verzi routeru 0.9.TBD musí routery zajistit:

- Neukládejte (nebo nepřetahujte) RI nebo LS s novým typem podpisu do routerů mladších než verze 0.9.TBD.
- Při ověřování netdb store, nestahujte RI nebo LS s novým typem podpisu z routerů mladších než verze 0.9.TBD.
- Routery s novým typem podpisu v jejich RI se nesmí připojovat k routerům mladším než verze 0.9.TBD, buď s NTCP, NTCP2 nebo SSU.
- Streamingové spojení a podepisované datagramy nebudou fungovat na routery mladší než verze 0.9.TBD, ale není způsob, jak to zjistit, takže nový typ podpisu by neměl být používán jako výchozí po dobu několika měsíců nebo let po vydání 0.9.TBD.

## Odkazy

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "Vysoce rychlé vysoce bezpečné podpisy" od Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, a Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://en.wikipedia.org/wiki/Length_extension_attack

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
