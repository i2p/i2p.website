---  
title: "Vyhledávání v databázi z cílů ECIES"  
number: "154"  
author: "zzz"  
created: "2020-03-23"  
lastupdated: "2021-01-08"  
status: "Closed"  
thread: "http://zzz.i2p/topics/2856"  
target: "0.9.46"  
implementedin: "0.9.46"  
toc: true
---  

## Poznámka  
ECIES to ElG je implementováno v 0.9.46 a fáze návrhu je uzavřena. Viz [I2NP](/docs/specs/i2np/) pro oficiální specifikaci. Tento návrh může být stále používán jako pozadí pro informace. ECIES to ECIES s přiloženými klíči je implementováno od verze 0.9.48. Sekce ECIES-to-ECIES (odvozené klíče) může být znovu otevřena nebo začleněna do budoucího návrhu.  

## Přehled  

### Definice  

- AEAD: ChaCha20/Poly1305  
- DLM: I2NP Database Lookup Message  
- DSM: I2NP Database Store Message  
- DSRM: I2NP Database Search Reply Message  
- ECIES: ECIES-X25519-AEAD-Ratchet (návrh 144)  
- ElG: ElGamal  
- ENCRYPT(k, n, payload, ad): Jak je definováno v [ECIES](/docs/specs/ecies/)  
- LS: Leaseset  
- lookup: I2NP DLM  
- reply: I2NP DSM nebo DSRM  

### Shrnutí  

Při odesílání DLM pro LS do floodfill, DLM obvykle specifikuje, že odpověď musí být označena, zašifrována AES a odeslána tunelem do cíle. Podpora pro AES-zašifrované odpovědi byla přidána v 0.9.7.  

AES-zašifrované odpovědi byly specifikovány v 0.9.7, aby se minimalizovala velká kryptografická zátěž ElG, a protože znovu použitá funkce tagů/AES v ElGamal/AES+SessionTags. Avšak AES odpovědi mohou být zfalšovány na IBEP, protože neexistuje žádná autentifikace, a odpovědi nejsou dopředu tajné.  

S cíli [ECIES](/docs/specs/ecies/) je záměr návrhu 144, že cíle již nepodporují 32-bytové tagy a AES dešifrování. Specifika byla záměrně neobsažena v tomto návrhu. Tento návrh dokumentuje novou možnost v DLM požadovat ECIES-zašifrované odpovědi.  

### Cíle  

- Nové vlajky pro DLM, když je požadována zašifrovaná odpověď tunelem do ECIES cíle  
- Pro odpověď, přidat dopřednou tajnost a autentifikaci odesílatele odolnou proti kompromitaci klíče požadovatele (cíl)  
- Zachovat anonymitu požadovatele  
- Minimalizovat kryptografickou zátěž  

### Necíle  

- Žádná změna v šifrování nebo bezpečnostních vlastnostech vyhledávání (DLM). Vyhledávání má dopřednou tajnost pouze pro kompromitaci požadovatele. Šifrování je ke statickému klíči floodfill.
- Žádná problém s dopřednou tajností nebo autentifikací odesílatele odolným proti kompromitaci klíče respondenta (floodfill). Floodfill je veřejná databáze a odpoví na vyhledávání od kohokoliv.
- Nenavrhovat ECIES směrovače v tomto návrhu. Kde je veřejný klíč X25519 směrovače TBD.  

## Alternativy  

Při absenci definovaného způsobu, jak zašifrovat odpovědi na ECIES cíle, existuje několik alternativ:  

1) Nepožadovat zašifrované odpovědi. Odpovědi budou nezašifrované.  
Java I2P aktuálně používá tento přístup.  

2) Přidat podporu pro 32-bytové tagy a AES-zašifrované odpovědi pro ECIES-only cíle,  
a požadovat AES-zašifrované odpovědi jako obvykle. i2pd aktuálně používá tento přístup.  

3) Požadovat AES-zašifrované odpovědi jako obvykle, ale zahrnout je zpět skrze průzkumné tunely do směrovače.  
Java I2P aktuálně používá tento přístup v některých případech.  

4) Pro duální ElG a ECIES cíle,  
požadovat AES-zašifrované odpovědi jako obvykle. Java I2P aktuálně používá tento přístup.  
i2pd ještě neimplementoval duální kryptografické cíle.  

## Návrh  

- Nový formát DLM přidá bit do pole vlajek k určení ECIES-zašifrovaných odpovědí.  
  ECIES-zašifrované odpovědi budou využívat formát zprávy [ECIES](/docs/specs/ecies/) Existing Session s předem připojeným tagem a ChaCha/Poly užitečným zatížením a MAC.  

- Definovat dvě varianty. Jednu pro ElG směrovače, kde není možná DH operace,  
  a jednu pro budoucí ECIES směrovače, kde je možná DH operace a může poskytnout
  další bezpečnost. Pro další studium.  

DH není možné pro odpovědi od ElG směrovačů, protože nezveřejňují
veřejný klíč X25519.  

## Specifikace  

Ve specifikaci [I2NP](/docs/specs/i2np/) DLM (DatabaseLookup) provést následující změny.  

Přidat bit vlajky 4 "ECIESFlag" pro nové možnosti šifrování.  

```text
flags ::
       bit 4: ECIESFlag
               před vydáním 0.9.46 ignorováno
               jako od vydání 0.9.46:
               0  => odeslat nezašifrovanou nebo ElGamal odpověď
               1  => odeslat ChaCha/Poly zašifrovanou odpověď s použitím přiloženého klíče
                     (zda je tag přiložen, závisí na bitu 1)
```

Bit vlajky 4 je použit v kombinaci s bitem 1 k určení režimu šifrování odpovědi.
Bit vlajky 4 musí být nastaven pouze při odesílání do směrovačů verze 0.9.46 nebo vyšší.

V tabulce níže,  
"DH n/a" znamená, že odpověď není zašifrována.  
"DH ne" znamená, že klíče odpovědi jsou zahrnuty v požadavku.  
"DH ano" znamená, že klíče odpovědi jsou odvozeny z DH operace.  

=============  =========  =========  ======  ===  =======
Flag bits 4,1  From Dest  To Router  Reply   DH?  poznámky
=============  =========  =========  ======  ===  =======
0 0            Jakýkoli   Jakýkoli   žádné šifrování  n/a  aktuální
0 1            ElG        ElG        AES     ne   aktuální
0 1            ECIES      ElG        AES     ne   obcházení i2pd
1 0            ECIES      ElG        AEAD    ne   tento návrh
1 0            ECIES      ECIES      AEAD    ne   0.9.49
1 1            ECIES      ECIES      AEAD    ano  budoucí
=============  =========  =========  ======  ===  =======

### ElG to ElG  

ElG cíl odešle vyhledávání do ElG směrovače.  

Menší změny v specifikaci pro kontrolu nové vlajky 4.  
Žádné změny ve stávajícím binárním formátu.  

Generování klíče požadovatele (objasnění):  

```text
reply_key :: CSRNG(32) 32 bajty náhodných dat
  reply_tags :: Každý je CSRNG(32) 32 bajty náhodných dat
```

Formát zprávy (přidat kontrolu ECIESFlag):  

```text
reply_key ::
       32 bajty `SessionKey` big-endian
       zahrnuty pouze pokud encryptionFlag == 1 AND ECIESFlag == 0, pouze jako od vydání 0.9.7

  tags ::
       1 bajt `Integer`
       platné rozmezí: 1-32 (typicky 1)
       počet odpovědních tagů, které následují
       pouze zahrnuty pokud encryptionFlag == 1 AND ECIESFlag == 0, pouze jako od vydání 0.9.7

  reply_tags ::
       jeden nebo více 32bajtových `SessionTag`s (typicky jeden)
       pouze zahrnuty pokud encryptionFlag == 1 AND ECIESFlag == 0, pouze jako od vydání 0.9.7
```

### ECIES to ElG  

ECIES cíl odešle vyhledávání do ElG směrovače.  
Podporováno od 0.9.46.  

Pole reply_key a reply_tags jsou předefinovány pro ECIES-zašifrovanou odpověď.  

Generování klíče požadovatele:  

```text
reply_key :: CSRNG(32) 32 bajty náhodných dat
  reply_tags :: Každý je CSRNG(8) 8 bajtů náhodných dat
```

Formát zprávy: Předefinovat pole reply_key a reply_tags takto:

```text
reply_key ::
       32-bajtový ECIES `SessionKey` big-endian
       zahrnut pouze pokud encryptionFlag == 0 AND ECIESFlag == 1, pouze od vydání 0.9.46

  tags ::
       1 bajt `Integer`
       požadovaná hodnota: 1
       počet odpovědních tagů, které následují
       pouze zahrnut pokud encryptionFlag == 0 AND ECIESFlag == 1, pouze od vydání 0.9.46

  reply_tags ::
       8-bajtový ECIES `SessionTag`
       pouze zahrnut pokud encryptionFlag == 0 AND ECIESFlag == 1, pouze od vydání 0.9.46
```

Odpověď je ECIES Existing Session zprávou, jak je definováno v [ECIES](/docs/specs/ecies/).  

```text
tag :: 8-bajtový reply_tag

  k :: 32-bajtový session key
     Odpověď_key.

  n :: 0

  ad :: 8-bajtový reply_tag

  payload :: Plaintext data, DSM nebo DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### ECIES to ECIES (0.9.49)  

ECIES cíl nebo směrovač odešle vyhledávání do ECIES směrovače, s přiloženými odpovědními klíči.
Podporováno od 0.9.49.  

ECIES směrovače byly představeny ve verzi 0.9.48, viz [Prop156](/proposals/156-ecies-routers/).  
Od verze 0.9.49, ECIES cíle a směrovače mohou používat stejný formát jako v sekci "ECIES to ElG", uvedený výše, s odpovědními klíči zahrnutými v požadavku.  
Vyhledávání použije "one time format" v [ECIES](/docs/specs/ecies/)  
protože je požadovatel anonymní.  

Pro novou metodu s odvozenými klíči, viz další sekci.  

### ECIES to ECIES (budoucí)  

ECIES cíl nebo směrovač odešle vyhledávání do ECIES směrovače, a odpovědní klíče jsou odvozeny z DH.
Není plně definováno nebo podporováno, implementace je TBD.  

Vyhledávání použije "one time format" v [ECIES](/docs/specs/ecies/)  
protože je požadovatel anonymní.  

Předefinovat pole reply_key takto. Neexistují žádné přidružené tagy.  
Tagy budou generovány v KDF níže.  

Tato sekce je neúplná a vyžaduje další studium.  

```text
reply_key ::
       32-bajtový X25519 efemérní `PublicKey` požadovatele, little-endian
       pouze zahrnut pokud encryptionFlag == 1 AND ECIESFlag == 1, pouze jako od vydání 0.9.TBD
```

Odpověď je ECIES Existing Session zprávou, jak je definováno v [ECIES](/docs/specs/ecies/).  
Viz [ECIES](/docs/specs/ecies/) pro všechny definice.  

```text
// Alice's X25519 efemérní klíče
  // aesk = Alice efemérní soukromý klíč
  aesk = GENERATE_PRIVATE()
  // aepk = Alice efemérní veřejný klíč
  aepk = DERIVE_PUBLIC(aesk)
  // Bob's X25519 statické klíče
  // bsk = Bob soukromý statický klíč
  bsk = GENERATE_PRIVATE()
  // bpk = Bob veřejný statický klíč
  // bpk je buď součástí RouterIdentity, nebo publikován v RouterInfo (TBD)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey z ???
  sdílené tajemství = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chainKey z Payload Section
  2) k ze KDF New Session nebo split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Výstup 1: nepoužitý
  nepoužité = keydata[0:31]
  // Výstup 2: Řetěz klíč pro inicializaci nové
  // session tag a symetrické klíče ratchety
  // pro Alice do Bob přenosy
  ck = keydata[32:63]

  // session tag a symetrické klíče chainKeys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: 8-bajtový tag, jak je generován z RATCHET_TAG() v [ECIES](/docs/specs/ecies/)

  k :: 32-bajtový klíč, jak je generován z RATCHET_KEY() v [ECIES](/docs/specs/ecies/)

  n :: Indikátor tagu. Typicky 0.

  ad :: 8-bajtový tag

  payload :: Plaintext data, DSM nebo DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### Formát odpovědi  

Toto je zpráva existujícího sezení,  
stejná jako v [ECIES](/docs/specs/ecies/), zkopírováno níže pro referenci.  

```text
+----+----+----+----+----+----+----+----+
  |  Session Tag                       |
  +----+----+----+----+----+----+----+----+
  |                                   |
  +        Payload Section            +
  |     ChaCha20 zašifrovaná data     |
  ~                                   ~
  |                                   |
  +                                   +
  |                                   |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Obnova autentizačního kódu |
  +               (MAC)                 +
  |               16 bajtů              |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bajtů, plaintext  

  Payload Section zašifrovaná data :: zbývající data mínus 16 bajtů  

  MAC :: Poly1305 obnova autentizačního kódu, 16 bajtů
```

## Odůvodnění  

Parametry šifrování odpovědi ve vyhledávání, poprvé představené v 0.9.7,  
jsou určitým porušením vrstvení. Je to tak kvůli efektivitě.  
Ale také protože vyhledávání je anonymní.  

Mohli bychom udělat formát vyhledávání generický, jako s polem typu šifrování,  
ale to je pravděpodobně více problémů, než stojí za to.  

Výše uvedený návrh je nejjednodušší a minimalizuje změnu formátu vyhledávání.  

## Poznámky  

Vyhledávání v databázi a obchody do ElG směrovačů musí být ElGamal/AESSessionTag šifrované  
jako obvykle.  

## Problémy  

Další analýza je vyžadována k zajištění dvou možností ECIES odpovědí.  

## Migrace  

Žádné problémy se zpětnou kompatibilitou. Směrovače se směrovač.verze 0.9.46 nebo vyšší  
v jejich RouterInfo musí podporovat tuto funkci.  
Směrovače nesmí odeslat DatabaseLookup s novými vlajkami směrem ke směrovačům s verzí nižší než 0.9.46.  
Pokud je databázová vyhledávací zpráva s nastaveným bitem 4 a nezapnutým bitem 1 omylem odeslána do  
směrovače bez podpory, pravděpodobně ignoruje dodaný klíč a tag, a  
odesílá odpověď nezašifrovanou.
