---
title: "Šifrování ChaCha pro vrstvy v tunelech"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Přehled

Tento návrh navazuje na a vyžaduje změny z návrhu 152: ECIES Tunnels.

Pouze tunely postavené přes uzly podporující formát BuildRequestRecord pro ECIES-X25519 tunely mohou implementovat tuto specifikaci.

Tato specifikace vyžaduje formát Tunnel Build Options pro indikaci typu šifrování tunelové vrstvy a přenášení klíčů pro vrstvy AEAD.

### Cíle

Cíle tohoto návrhu jsou:

- Nahradit AES256/ECB+CBC ChaCha20 pro zavedené IV tunelu a šifrování vrstev
- Použít ChaCha20-Poly1305 pro meziuzlovou AEAD ochranu
- Být neodhalitelný stávajícími účastníky tunelové vrstvy
- Neměnit celkovou délku tunelové zprávy

### Zpracování Zavedené Tunelové Zprávy

Tato sekce popisuje změny pro:

- Přepřipravování a šifrování výstupní a vstupní brány
- Šifrování účastníků a postprocessing
- Šifrování a postprocessing výstupního a vstupního koncového bodu

Pro přehled současného zpracování tunelových zpráv viz specifikace [Tunnel Implementation](/docs/tunnels/implementation/).

Jsou diskutovány pouze změny pro směrovače podporující ChaCha20 šifrování vrstev.

Nejsou zvažovány žádné změny pro smíšené tunely s AES šifrováním vrstev, dokud nebude možné navrhnout bezpečný protokol pro konverzi 128bitového AES IV na 64bitový ChaCha20 nonce. Bloom filtry zaručují jedinečnost pro celé IV, ale první polovina jedinečných IV může být identická.

To znamená, že šifrování vrstev musí být jednotné pro všechny uzly v tunelu a zavedené použitím možností budování tunelu během procesu vytvoření tunelu.

Všechny brány a účastníci tunelů budou muset udržovat Bloom filtr pro validaci dvou nezávislých nonce.

Po celou dobu se v tomto návrhu zmiňovaný ``nonceKey`` nahrazuje ``IVKey`` používaným v AES šifrování vrstev.
Generuje se pomocí stejného KDF z návrhu 152.

### AEAD Šifrování Mezizranných Zpráv

Pro každý pár následných uzlů bude potřeba generovat dodatečný jedinečný ``AEADKey``.
Tento klíč budou používat následující uzly pro šifrování a dešifrování vnitřních ChaCha20 šifrovaných tunelových zpráv pomocí ChaCha20-Poly1305.

Tunelové zprávy budou muset snížit délku vnitřního šifrovaného rámce o 16 bajtů, aby se uvolnilo místo pro Poly1305 MAC.

AEAD nemůže být použito přímo na zprávy, protože iterativní dešifrování je požadované výstupními tunely. Iterativní dešifrování lze nyní dosáhnout pouze použitím ChaCha20 bez AEAD.

.. raw:: html

  {% highlight lang='dataspec' -%}
+----+----+----+----+----+----+----+----+
  |    ID Tunelu      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | pokrač. tunnelNonce |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  | pokrač. obfsNonce  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Šifrovaná Data              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  ID Tunelu :: `TunnelId`
         4 bajty
         ID následného uzlu

  tunnelNonce ::
         8 bajtů
         nonce tunelové vrstvy

  obfsNonce ::
         8 bajtů
         nonce šifrování tunelové vrstvy

  Šifrovaná Data ::
         992 bajtů
         šifrovaná tunelová zpráva

  Poly1305 MAC ::
         16 bajtů

  celková velikost: 1028 bajtů
```

Vnitřní uzly (s předcházejícími a následujícími uzly) budou mít dva ``AEADKeys``, jeden pro dešifrování AEAD vrstvy předcházejícího uzlu a šifrování AEAD vrstvy následujícího uzlu.

Všichni účastníci vnitřních uzlů tedy budou mít ve svých záznamech BuildRequestRecords zahrnutých 64 dodatečných bajtů klíčového materiálu.

Výstupní koncový bod a vstupní brána budou potřebovat pouze 32 dodatečných bajtů klíčových dat, protože mezi sebou nešifrují tunelovou vrstvu.

Výstupní brána generuje svůj klíč ``outAEAD``, který je stejný jako klíč ``inAEAD`` prvního výstupního uzlu.

Vstupní koncový bod generuje svůj klíč ``inAEAD``, který je stejný jako klíč ``outAEAD`` posledního vstupního uzlu.

Vnitřní uzly obdrží ``inAEADKey`` a ``outAEADKey``, které budou použity pro AEAD dešifrování příchozích zpráv a šifrování odchozích zpráv.

Jako příklad, ve tunelu s vnitřními uzly OBGW, A, B, OBEP:

- ``inAEADKey`` pro uzel A je stejný jako ``outAEADKey`` pro OBGW
- ``inAEADKey`` pro uzel B je stejný jako ``outAEADKey`` pro A
- ``outAEADKey`` pro uzel B je stejný jako ``inAEADKey`` pro OBEP

Klíče jsou jedinečné pro dvojice uzlů, takže ``inAEADKey`` pro OBEP bude jiný než ``inAEADKey`` pro A, ``outAEADKey`` pro A jiný než ``outAEADKey`` pro B, atd.

### Zpracování Zpráv Brány a Tvořitele Tunelů

Brány budou fragmentovat a zabalení zpráv stejným způsobem, přičemž si vyhrazují místo za rámcem s fragmentací pokynů pro Poly1305 MAC.

Vnitřní zprávy I2NP obsahující AEAD rámce (včetně MAC) mohou být rozděleny přes fragmenty, ale jakékoliv vynechané fragmenty povedou k neúspěšnému AEAD dešifrování (neúspěšné ověření MAC) v koncovém bodě.

### Předzpracování a Šifrování Brány

Když tunely podporují šifrování vrstev ChaCha20, brány vygenerují dva 64bitové nonce pro každou sadu zpráv.

Vstupní tunely:

- Šifrování IV a tunelových zpráv pomocí ChaCha20
- Použití 8bajtových ``tunnelNonce`` a ``obfsNonce`` vzhledem k životnosti tunelů
- Použití 8bajtového ``obfsNonce`` pro šifrování ``tunnelNonce``
- Zničení tunelu před 2^(64 - 1) - 1 sadami zpráv: 2^63 - 1 = 9,223,372,036,854,775,807

  - Omezení počtu nonce, aby se předešlo kolizi 64bitových nonce
  - Velmi nepravděpodobné, že by omezení nonce bylo kdy dosaženo, vzhledem k tomu, že by to bylo přes ~15,372,286,728,091,294 zpráv/sekundu pro 10minutové tunely

- Nastavení Bloomova filtru na základě rozumného počtu očekávaných prvků (128 zpráv/sekundu, 1024 zpráv/sekundu? Bude stanoveno později)

Vstupní brána tunelu (IBGW) zpracovává zprávy přijaté z výstupního koncového bodu jiného tunelu (OBEP).

V tomto bodě je vnější vrstva zpráv zašifrována pomocí šifrování point-to-point transport. Záhlaví I2NP zpráv jsou viditelná na tunelové vrstvě pro OBEP a IBGW. Vnitřní zprávy I2NP jsou zabaleny do Garlic cloves, zašifrované pomocí end-to-end sezení šifrování.

IBGW předzpracovává zprávy do vhodně formátovaných tunelových zpráv a šifruje je takto:

```text

// IBGW generuje náhodné nonce, zajišťuje, že se v jeho Bloomově filtru nenachází žádná kolize pro každý nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW zašifruje každou z předzpracovaných tunelových zpráv pomocí ChaCha20 s jeho tunnelNonce a layerKey
  encMsg = ChaCha20(msg = tunnel msg, nonce = tunnelNonce, key = layerKey)

  // ChaCha20-Poly1305 zašifruje každý datový rámec s už zašifrovanou zprávou pomocí tunnelNonce a outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

Formát tunelové zprávy se lehce změní, s použitím dvou 8bajtových nonce namísto 16bajtového IV. ``obfsNonce`` použité pro šifrování nonce je připojeno k 8bajtovému ``tunnelNonce`` a je šifrováno každým uzlem pomocí zašifrovaného ``tunnelNonce`` a jeho ``nonceKey``.

Poté, co sada zpráv prošla předčasným dešifrováním pro každý uzel, výstupní brána ChaCha20-Poly1305 AEAD zašifruje šifrovou část každé tunelové zprávy pomocí ``tunnelNonce`` a svého ``outAEADKey``.

Výstupní tunely:

- Iterativní dešifrování tunelových zpráv
- ChaCha20-Poly1305 zašifruje předčasně dešifrované tunelové zprávy
- Použití stejných pravidel pro šifrování vrstvy pro nonce jako vstupní tunely
- Generování náhodných nonce jednou pro sadu odeslaných tunelových zpráv

```text


// Pro každou sadu zpráv vygenerujte jedinečné, náhodné nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Pro každý uzel zašifruje ChaCha20 předchozí tunnelNonce s nonce aktuálního uzlu
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = hop's nonceKey)

  // Pro každý uzel ChaCha20 "dešifruje" tunelovou zprávu s aktuálním tunnelNonce uzlu a layerKey
  decMsg = ChaCha20(msg = tunnel msg(s), nonce = tunnelNonce, key = hop's layerKey)

  // Pro každý uzel ChaCha20 "dešifruje" obfsNonce s zašifrovaným tunnelNonce aktuálního uzlu a nonceKey
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = hop's nonceKey)

  // Po zpracování uzlu, ChaCha20-Poly1305 zašifruje každý decrypted frame tunelové zprávy s zašifrovaným tunnelNonce prvního uzlu a inAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = first hop's encrypted tunnelNonce, key = first hop's inAEADKey / GW outAEADKey)
```

### Zpracování Účastníků

Účastníci budou sledovat odeslané zprávy stejným způsobem, používající decaying Bloom filtry.

Tunelové nonces budou muset být šifrovány jednou za uzel, aby se zabránilo potvrzovacím útokům ze strany nesoudržných, společně jedoucích uzlů.

Uzel zašifruje obdržené nonce, aby zabránil potvrzovacím útokům mezi předcházejícími a následujícími uzly, tj. nesoudržné, společně jedoucí uzly by nemohly zjistit, že patří do stejného tunelu.

Pro validaci příchozích ``tunnelNonce`` a ``obfsNonce`` účastníci kontrolují každý nonce zvlášť ve svém Bloom filtru pro duplikáty.

Po validaci účastník:

- ChaCha20-Poly1305 dešifruje každé AEAD šifrované datové rámce tunelové zprávy s přijatým ``tunnelNonce`` a jeho ``inAEADKey``
- ChaCha20 zašifruje ``tunnelNonce`` s jeho ``nonceKey`` a přijatým ``obfsNonce``
- ChaCha20 zašifruje každé datové rámy tunelové zprávy s zašifrovaným ``tunnelNonce`` a jeho ``layerKey``
- ChaCha20-Poly1305 zašifruje každé datové rámy tunelové zprávy zašifrované ``tunnelNonce`` a jeho ``outAEADKey`` 
- ChaCha20 zašifruje ``obfsNonce`` s jeho ``nonceKey`` a zašifrovaným ``tunnelNonce``
- Odešle dvojiček {``nextTunnelId``, zašifrovaný (``tunnelNonce`` || ``obfsNonce``), AEAD ciphertext || MAC} na další uzel.

```text

// Pro ověření by tunelové uzly měly zkontrolovat Bloomův filtr pro jedinečnost každého přijatého nonce
  // Po ověření, rozbalte AEAD rámec(y) dešifrováním každého rámce zašifrované tunelové zprávy
  // s přijatým tunnelNonce a inAEADKey 
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = received encMsg \|\| MAC, nonce = received tunnelNonce, key = inAEADKey)

  // Zašifrujte tunnelNonce pomocí obfsNonce a hop's nonceKey
  tunnelNonce = ChaCha20(msg = received tunnelNonce, nonce = received obfsNonce, key = nonceKey)

  // Zašifrujte každé datové rámy tunelové zprávy s zašifrovaným tunnelNonce a hop's layerKey
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Pro AEAD ochranu také zašifrujte každé datové rámy zprávy s zašifrovaným tunnelNonce a hop's outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // Zašifrujte obdržené obfsNonce s zašifrovaným tunnelNonce a hop's nonceKey
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Zpracování Vstupního Koncového Bodu

Pro tunely ChaCha20 bude použit následující schéma k dešifrování každé tunelové zprávy:

- Validace přijatých ``tunnelNonce`` a ``obfsNonce`` nezávisle proti jeho Bloom filtru
- ChaCha20-Poly1305 dešifrovat zašifrované datové rámy s přijatým ``tunnelNonce`` a ``inAEADKey``
- ChaCha20 dešifrovat zašifrované datové rámy s přijatým ``tunnelNonce`` & hop's ``layerKey``
- ChaCha20 dešifrovat ``obfsNonce`` s hop's ``nonceKey`` a přijatým ``tunnelNonce`` k získání předchozího ``obfsNonce``
- ChaCha20 dešifrovat přijaté ``tunnelNonce`` s hop's ``nonceKey`` a dešifrovaným ``obfsNonce`` k získání předchozího ``tunnelNonce``
- ChaCha20 dešifrovat zašifrovaná data s dešifrovaným ``tunnelNonce`` & předchozího uzlu ``layerKey``
- Opakujte kroky pro nonce a dešifrování vrstvy pro každý uzel v tunelu zpět na IBGW
- AEAD dešifrování rámců je potřeba pouze v první iteraci

```text

// Pro první iteraci ChaCha20-Poly1305 dešifruje každé datové rámy zprávy + MAC
  // s použitím přijatého tunnelNonce a inAEADKey
  msg = encTunMsg \|\| MAC
  tunnelNonce = received tunnelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Opakujte pro každý uzel v tunelu zpět na IBGW
  // Pro každý iteraci dešifruje ChaCha20 každý uzlový vrstvový šifrování na každém datovém rámci zprávy
  // Nahraďte přijatý tunnelNonce dešifrovaným tunnelNonce z předchozí iterace pro každý uzel
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Bezpečnostní Analýza pro Šifrování Tunelových Vrstv ChaCha20+ChaCha20-Poly1305

Přechod z AES256/ECB+AES256/CBC na ChaCha20+ChaCha20-Poly1305 má několik výhod a nových bezpečnostních úvah.

Největší bezpečnostní úvahou je zajištění, aby nonce ChaCha20 a ChaCha20-Poly1305 byly jedinečné pro každou zprávu po dobu životnosti použitého klíče.

Nepoužití jedinečných nonce se stejným klíčem na různé zprávy narušuje ChaCha20 a ChaCha20-Poly1305.

Použití přiloženého ``obfsNonce`` umožňuje IBEP dešifrovat ``tunnelNonce`` pro šifrování vrstvy každého uzlu a obnovit předchozí nonce.

``obfsNonce`` spolu s ``tunnelNonce`` neodhaluje žádné nové informace pro tunelové uzly, protože ``obfsNonce`` je šifrováno s použitím zašifrovaného ``tunnelNonce``. To také umožňuje IBEP obnovit předchozí ``obfsNonce`` podobně jako obnovení ``tunnelNonce``.

Největší bezpečnostní výhodou je, že neexistují žádné potvrzovací nebo orákulové útoky proti ChaCha20, a použití ChaCha20-Poly1305 mezi uzly přidává AEAD ochranu proti manipulaci se šifrovým textem od mimořádných útočníků prostředníka (MitM).

Existují praktické orákulové útoky proti AES256/ECB + AES256/CBC, když se klíč opakovaně používá (jako v šifrování tunelové vrstvy).

Orákulové útoky proti AES256/ECB nebudou fungovat kvůli použití dvojitého šifrování a šifrování je nad jediným blokem (tunel IV).

Útoky polštářkovými orákuly proti AES256/CBC nebudou fungovat, protože se nepoužívá žádné polstrování. Pokud se délka tunelové zprávy někdy změní na non-mod-16 délky, AES256/CBC nebude stále zranitelné kvůli odmítnutým duplicitním IV.

Oba útoky jsou také blokovány tím, že se nepovolují opakované orákulové volání s použitím stejného IV, jelikož jsou odmítány duplicitní IV.

## Reference

* [Tunnel-Implementation](/docs/tunnels/implementation/)
