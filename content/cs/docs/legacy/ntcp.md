---
title: "NTCP (TCP založené na NIO)"
description: "Starší TCP transport pro I2P založený na Java NIO, nahrazen NTCP2"
slug: "ntcp"
aliases:
  - "/cs/docs/transport/ntcp"
  - "/cs/docs/transport/ntcp/"
  - "/cs/docs/ntcp"
  - "/cs/docs/ntcp/"
  - "/cs/ntcp"
  - "/cs/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

ZASTARALÉ, JIŽ NEPODPOROVÁNO. Ve výchozím nastavení zakázáno od verze 0.9.40 2019-05. Podpora odstraněna od verze 0.9.50 2021-05. Nahrazeno protokolem [NTCP2](/docs/specs/ntcp2). NTCP je transportní protokol založený na Java NIO, který byl představen v I2P verzi 0.6.1.22. Java NIO (new I/O) netrpí problémy se starým TCP transportem, kdy bylo potřeba 1 vlákno na každé spojení. NTCP-over-IPv6 je podporováno od verze 0.9.8.

Ve výchozím nastavení NTCP používá IP/Port automaticky detekovanou pomocí SSU. Když je povoleno v config.jsp, SSU upozorní/restartuje NTCP při změně externí adresy nebo při změně stavu firewallu. Nyní můžete povolit příchozí TCP bez statické IP nebo služby dyndns.

NTCP kód v I2P je relativně lehký (1/4 velikosti SSU kódu), protože používá podkladový Java TCP transport pro spolehlivé doručování.

## Specifikace adresy router {#ra}

Následující vlastnosti jsou uloženy v síťové databázi.

- **Název transportu:** NTCP
- **host:** IP (IPv4 nebo IPv6).
  Zkrácená IPv6 adresa (s "::") je povolena.
  Názvy hostitelů byly dříve povoleny, ale od verze 0.9.32 jsou zastaralé. Viz návrh 141.
- **port:** 1024 - 65535

## Specifikace protokolu NTCP

### Standardní formát zprávy

Po navázání spojení přenáší NTCP transport jednotlivé I2NP zprávy s jednoduchým kontrolním součtem. Nešifrovaná zpráva je kódována následovně:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Data jsou poté šifrována pomocí AES/256/CBC. Session key pro šifrování se vyjednává během navazování spojení (pomocí Diffie-Hellman 2048 bit). Navazování spojení mezi dvěma routery je implementováno ve třídě EstablishState a je podrobně popsáno níže. IV pro AES/256/CBC šifrování je posledních 16 bajtů předchozí šifrované zprávy.

Je vyžadováno 0-15 bajtů výplně, aby celková délka zprávy (včetně šesti bajtů velikosti a kontrolního součtu) byla násobkem 16. Maximální velikost zprávy je v současnosti 16 KB. Proto je maximální velikost dat v současnosti 16 KB - 6, nebo 16378 bajtů. Minimální velikost dat je 1.

### Formát zprávy pro synchronizaci času

Jeden zvláštní případ je zpráva metadata, kde sizeof(data) je 0. V tomto případě je nešifrovaná zpráva kódována jako:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Celková délka: 16 bajtů. Zpráva synchronizace času je odesílána přibližně v 15minutových intervalech. Zpráva je šifrována stejně jako standardní zprávy.

### Kontrolní součty

Standardní zprávy a zprávy synchronizace času používají kontrolní součet Adler-32 definovaný ve [specifikaci ZLIB](http://tools.ietf.org/html/rfc1950).

### Časový limit nečinnosti

Časový limit nečinnosti a uzavření připojení je na uvážení každého koncového bodu a může se lišit. Současná implementace snižuje časový limit, když se počet připojení blíží nakonfigurovanému maximu, a zvyšuje časový limit, když je počet připojení nízký. Doporučený minimální časový limit je dvě minuty nebo více a doporučený maximální časový limit je deset minut nebo více.

### Výměna RouterInfo

Po navázání spojení a následně každých 30-60 minut by si oba routery měly obecně vyměnit RouterInfos pomocí DatabaseStoreMessage. Alice by však měla zkontrolovat, zda první zpráva ve frontě není DatabaseStoreMessage, aby neodeslala duplicitní zprávu; to je často případ při připojování k floodfill routeru.

### Sekvence navázání spojení

Ve stavu establish probíhá 4fázová sekvence zpráv pro výměnu DH klíčů a podpisů. V prvních dvou zprávách dochází k 2048bitové Diffie Hellman výměně. Poté se vyměňují podpisy kritických dat pro potvrzení spojení.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH výměna klíčů {#DH}

Počáteční 2048-bitová DH výměna klíčů používá stejné sdílené prvočíslo (p) a generátor (g) jako ty, které se používají pro I2P [ElGamal šifrování](/docs/specs/cryptography#elgamal).

Výměna klíčů DH se skládá z několika kroků, které jsou zobrazeny níže. Mapování mezi těmito kroky a zprávami posílanými mezi I2P routery je označeno tučně.

1. Alice vygeneruje tajné celé číslo x. Poté vypočítá `X = g^x mod p`.
2. Alice pošle X Bobovi **(Zpráva 1)**.
3. Bob vygeneruje tajné celé číslo y. Poté vypočítá `Y = g^y mod p`.
4. Bob pošle Y Alice. **(Zpráva 2)**
5. Alice nyní může vypočítat `sessionKey = Y^x mod p`.
6. Bob nyní může vypočítat `sessionKey = X^y mod p`.
7. Alice i Bob nyní mají sdílený klíč `sessionKey = g^(x*y) mod p`.

SessionKey se poté používá k výměně identit v **Zprávě 3** a **Zprávě 4**. Délka exponentu (x a y) pro DH výměnu je dokumentována na [stránce o kryptografii](/docs/specs/cryptography#exponent).

#### Detaily klíče relace

32bytový klíč relace je vytvořen následovně:

1. Vezměte vyměněný DH klíč, reprezentovaný jako pozitivní pole bajtů BigInteger minimální délky (doplněk do dvou big-endian)
2. Pokud je nejvýznamnější bit 1 (tj. array[0] & 0x80 != 0), přidejte na začátek bajt 0x00, jako v reprezentaci Java BigInteger.toByteArray()
3. Pokud je toto pole bajtů větší nebo rovno 32 bajtům, použijte prvních (nejvýznamnějších) 32 bajtů
4. Pokud je toto pole bajtů menší než 32 bajtů, připojte bajty 0x00 pro rozšíření na 32 bajtů. *(mizivě nepravděpodobné)*

#### Zpráva 1 (Požadavek relace)

Toto je DH požadavek. Alice již má Bobovu [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), IP adresu a port, jak jsou obsaženy v jeho [Router Info](/docs/specs/common-structures#struct_RouterInfo), která byla publikována do [network database](/docs/overview/network-database). Alice pošle Bobovi:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Obsah:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Poznámky:**

- Bob ověří HXxorHI pomocí svého vlastního router hashe. Pokud se ověření nezdaří, Alice kontaktovala špatný router a Bob ukončí spojení.

#### Zpráva 2 (Relace vytvořena)

Toto je DH odpověď. Bob pošle Alici:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Nešifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Šifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Poznámky:**

- Alice může ukončit spojení, pokud je časový posun s Bobem příliš vysoký, jak je vypočítán pomocí tsB.

#### Zpráva 3 (Potvrzení relace A)

Toto obsahuje identitu Alice routeru a podpis kritických dat. Alice pošle Bobovi:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Nešifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Šifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Poznámky:**

- Bob ověří podpis a při selhání ukončí spojení.
- Bob může ukončit spojení, pokud je časové zkreslení s Alice příliš vysoké podle výpočtu pomocí tsA.
- Alice použije posledních 16 bajtů šifrovaného obsahu této zprávy jako IV pro další zprávu.
- Do vydání 0.9.15 byla router identity vždy 387 bajtů, podpis byl vždy 40bajtový DSA podpis a výplň byla vždy 15 bajtů. Od vydání 0.9.16 může být router identity delší než 387 bajtů a typ a délka podpisu jsou odvozeny z typu [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) v Alice [Router Identity](/docs/specs/common-structures#struct_RouterIdentity). Výplň je podle potřeby na násobek 16 bajtů pro celý nešifrovaný obsah.
- Celková délka zprávy nemůže být určena bez částečného dešifrování pro přečtení Router Identity. Protože minimální délka Router Identity je 387 bajtů a minimální délka Signature je 40 (pro DSA), minimální celková velikost zprávy je 2 + 387 + 4 + (délka podpisu) + (výplň na 16 bajtů), nebo 2 + 387 + 4 + 40 + 15 = 448 pro DSA. Příjemce by mohl přečíst toto minimální množství před dešifrováním k určení skutečné délky Router Identity. Pro malé Certificates v Router Identity to bude pravděpodobně celá zpráva a v zprávě nebudou žádné další bajty vyžadující dodatečnou operaci dešifrování.

#### Zpráva 4 (Potvrzení relace B)

Toto je podpis kritických dat. Bob pošle Alici:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Nešifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Šifrovaný obsah:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Poznámky:**

- Alice ověří podpis a při selhání ukončí spojení.
- Bob použije posledních 16 bajtů šifrovaného obsahu této zprávy jako IV pro následující zprávu.
- Do verze 0.9.15 byl podpis vždy 40 bajtový DSA podpis a padding byl vždy 8 bajtů. Od verze 0.9.16 jsou typ a délka podpisu odvozeny z typu [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) v Bobově [Router Identity](/docs/specs/common-structures#struct_RouterIdentity). Padding je podle potřeby na násobek 16 bajtů pro celý nešifrovaný obsah.

#### Po navázání spojení

Spojení je navázáno a mohou být vyměňovány standardní zprávy nebo zprávy synchronizace času. Všechny následující zprávy jsou šifrovány pomocí AES s dohodnutým DH session klíčem. Alice použije posledních 16 bytů šifrovaného obsahu zprávy #3 jako další IV. Bob použije posledních 16 bytů šifrovaného obsahu zprávy #4 jako další IV.

### Zkontrolovat zprávu o připojení

Alternativně, když Bob obdrží připojení, mohlo by to být kontrolní připojení (možná vyvolané tím, že Bob požádal někoho o ověření svého naslouchacího procesu). Check Connection se v současnosti nepoužívá. Pro pořádek jsou však kontrolní připojení formátována následovně. Kontrolní info připojení obdrží 256 bajtů obsahujících:

- 32 bajtů neinterpretovaných, ignorovaných dat
- 1 bajt velikosti
- tolik bajtů, kolik tvoří IP adresu místního routeru (jak je dosažitelný vzdálenou stranou)
- 2 bajtové číslo portu, na kterém byl místní router dosažen
- 4 bajtový i2p síťový čas známý vzdálené straně (sekundy od epochy)
- neinterpretovaná výplňová data, až do bajtu 223
- xor hash identity místního routeru a SHA256 bajtů 32 až 223

Kontrola připojení je od verze 0.9.12 zcela zakázána.

## Diskuse

Nyní na [NTCP diskuzní stránce](/docs/discussions/ntcp).

## Budoucí práce {#future}

- Maximální velikost zprávy by měla být zvýšena na přibližně 32 KB.

- Sada pevných velikostí paketů může být vhodná pro další skrytí fragmentace dat před externími protivníky, ale padding pro tunnel, garlic a end-to-end by měl být dostatečný pro většinu potřeb do té doby.
  Nicméně v současnosti neexistuje žádné ustanovení pro padding nad rámec další 16-bajtové hranice, aby se vytvořil omezený počet velikostí zpráv.

- Využití paměti (včetně paměti jádra) pro NTCP by mělo být porovnáno s tím pro SSU.

- Mohou být zprávy pro navázání spojení nějak náhodně doplněny, aby se zmařila
  identifikace I2P provozu na základě velikostí počátečních paketů?
