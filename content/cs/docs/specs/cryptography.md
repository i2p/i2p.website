---
title: "Specifikace nízkoúrovňové kryptografie"
description: "Podrobnosti nízké úrovně kryptografických algoritmů používaných v I2P"
slug: "cryptography"
aliases:
  - "/cs/how_cryptography"
  - "/cs/how_cryptography/"
category: "Design"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Přehled

> **Poznámka:** Tento dokument je převážně zastaralý. Aktuální specifikace naleznete v následujících dokumentech: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Tato stránka specifikuje nízkoúrovňové detaily kryptografie v I2P.

V rámci I2P se používá několik kryptografických algoritmů. V původním návrhu I2P byl jen jeden algoritmus každého typu - jeden symetrický algoritmus, jeden asymetrický algoritmus, jeden algoritmus pro podepisování a jeden hashovací algoritmus. Neexistovalo žádné opatření pro přidávání dalších algoritmů nebo migraci na algoritmy s vyšší bezpečností.

V posledních letech jsme přidali framework pro podporu více primitivů a kombinací způsobem kompatibilním se staršími verzemi. Četné algoritmy podpisů s různými délkami klíčů a podpisů jsou definovány "typy podpisů". Schémata end-to-end šifrování využívající kombinaci asymetrického a symetrického šifrování s různými délkami klíčů jsou definována "typy šifrování".

Různé protokoly a datové struktury v I2P obsahují pole pro specifikaci typu podpisu a/nebo typu šifrování. Tato pole spolu s definicemi typů definují délky klíčů a podpisů a kryptografické primitivy potřebné k jejich použití. Definice typů podpisů a šifrování jsou ve [specifikaci Common Structures](/docs/specs/common-structures).

Původní I2P protokoly NTCP, SSU a ElGamal/AES+SessionTags používají kombinaci ElGamal asymetrického šifrování a AES symetrického šifrování. Novější protokoly NTCP2 a ECIES-X25519-AEAD-Ratchet používají kombinaci X25519 výměny klíčů a ChaCha20/Poly1305 symetrického šifrování.

- ECIES-X25519-AEAD-Ratchet nahradilo ElGamal/AES+SessionTags.
- NTCP2 nahradilo NTCP.
- SSU2 nahradilo SSU.
- Vytváření tunelů X25519 nahradilo vytváření tunelů ElGamal.

## Asymetrické šifrování

Původní asymetrický šifrovací algoritmus v I2P je ElGamal. Novější algoritmus, používaný na několika místech, je ECIES X25519 DH výměna klíčů.

Právě probíhá migrace veškerého použití ElGamal na X25519.

NTCP (s ElGamal) byl migrován na NTCP2 (s X25519). ElGamal/AES+SessionTag je migrováno na ECIES-X25519-AEAD-Ratchet.

### X25519

Podrobnosti o používání X25519 najdete v [NTCP2](/docs/specs/ntcp2) a [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal se používá na několika místech v I2P:

- Pro šifrování zpráv TunnelBuild mezi routery
- Pro end-to-end šifrování (destination-to-destination) jako součást ElGamal/AES+SessionTag pomocí šifrovacího klíče v leaseSet
- Pro šifrování některých netDb úložišť a dotazů odeslaných floodfill routerům jako součást ElGamal/AES+SessionTag (destination-to-router nebo router-to-router).

Pro 2048bitové ElGamal šifrování a dešifrování používáme běžná prvočísla podle IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). ElGamal v současnosti používáme pouze k zašifrování IV a session key v jednom bloku, následovaném AES šifrovaným obsahem pomocí tohoto klíče a IV.

Nešifrovaný ElGamal obsahuje:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data) je SHA256 dat, která jsou zašifrována v ElGamal bloku, a je mu předřazen náhodný nenulový byte. Tento byte je skutečně náhodný od verze 0.9.28; před tím to bylo vždy 0xFF. Možná by mohl být v budoucnu použit pro příznaky. Data zašifrovaná v bloku mohou být dlouhá až 222 bytů. Jelikož zašifrovaná data mohou obsahovat značné množství nul, pokud je čistý text menší než 222 bytů, doporučuje se, aby vyšší vrstvy vyplnily čistý text na 222 bytů náhodnými daty. Celková délka: typicky 255 bytů.

Šifrovaný ElGamal obsahuje:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Každá šifrovaná část je doplněna nulami na přesnou velikost 257 bajtů. Celková délka: 514 bajtů. Při typickém použití vyšší vrstvy doplní nešifrovaná data na 222 bajtů, což má za následek nešifrovaný blok o velikosti 255 bajtů. Ten je zakódován jako dva 256bajtové šifrované části a před každou částí je na této vrstvě jeden bajt nulového doplnění.

Viz ElGamal kód [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

Sdílené prvočíslo je Oakley prvočíslo pro 2048 bitové klíče [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
nebo jako hexadecimální hodnota:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Používání 2 jako generátoru.

#### Krátký exponent {#exponent}

Zatímco standardní velikost exponentu je 2048 bitů (256 bajtů) a I2P PrivateKey má plných 256 bajtů, v některých případech používáme krátkou velikost exponentu 226 bitů (28,25 bajtů). To by mělo být bezpečné pro použití s Oakley prvočísly [vanOorschot1996] [BENCHMARKS].

Také [Koshiba2004] to zjevně podporuje, podle tohoto vlákna sci.crypt [SCI.CRYPT]. Zbytek PrivateKey je doplněn nulami.

Před vydáním 0.9.8 všechny routery používaly krátký exponent. Od vydání 0.9.8 64bitové x86 routery používají plný 2048bitový exponent. Všechny routery nyní používají plný exponent kromě malého počtu routerů na velmi pomalém hardware, které nadále používají krátký exponent kvůli obavám ohledně zatížení procesoru. Přechod na delší exponent pro tyto platformy je tématem pro další studium.

#### Zastaralost

Zranitelnost sítě vůči ElGamal útoku a dopad přechodu na delší bitovou délku má být studován. Může být velmi obtížné učinit jakoukoliv změnu zpětně kompatibilní.

## Symetrické šifrování

Původní symetrický šifrovací algoritmus v I2P je AES. Novější algoritmus, používaný na několika místech, je Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Právě probíhá migrace veškerého použití AES na ChaCha20/Poly1305.

NTCP (s AES) byl migrován na NTCP2 (s ChaCha20/Poly1305). ElGamal/AES+SessionTag je migrován na ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

Pro podrobnosti o použití ChaCha20/Poly1305 viz [NTCP2](/docs/specs/ntcp2) a [ECIES](/docs/specs/ecies).

### AES

AES se používá pro symetrické šifrování v několika případech:

- Pro šifrování SSU transportu (viz sekce "Transports") po DH výměně klíčů
- Pro end-to-end (destination-to-destination) šifrování jako součást ElGamal/AES+SessionTag
- Pro šifrování některých netDb uložení a dotazů odeslaných na floodfill routery jako součást ElGamal/AES+SessionTag (destination-to-router nebo router-to-router).
- Pro šifrování periodických testovacích zpráv tunelů odeslaných z routeru k sobě samému, přes jeho vlastní tunely.

Používáme AES s 256bitovými klíči a 128bitovými bloky v režimu CBC. Používané vyplňování je specifikováno v IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, sekce 8.1 (pro typ bloku 02)). V tomto případě vyplňování sestává z pseudonáhodně generovaných oktetů pro dosažení 16bajtových bloků. Konkrétně viz kód CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) a implementaci Cryptix AES [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), stejně jako vyplňování, které najdete ve funkci ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Zastarávání

Zranitelnost sítě vůči AES útoku a dopad přechodu na delší bitovou délku má být studován. Může být poměrně obtížné učinit jakoukoliv změnu zpětně kompatibilní.

## Podpisy {#sig}

Četné algoritmy podpisů s různými délkami klíčů a podpisů jsou definovány typy podpisů. Je relativně snadné přidat další typy podpisů.

EdDSA-SHA512-Ed25519 je aktuální výchozí algoritmus pro podpisy. DSA, který byl původním algoritmem před tím, než jsme přidali podporu pro typy podpisů, se v síti stále používá.

### DSA

Podpisy jsou generovány a ověřovány pomocí 1024 bitového [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) (L=1024, N=160), jak je implementováno v [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). DSA bylo zvoleno, protože je pro podpisy mnohem rychlejší než ElGamal.

#### SEED

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Čítač

```
33
```
#### DSA prvočíslo (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA kvocient (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA generátor (g)

1024 bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey má 1024 bitů. SigningPrivateKey má 160 bitů.

#### Zastaralost

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) doporučuje minimum (L=2048, N=224) pro použití po roce 2010. Toto může být částečně zmírněno "kryptoperíodou", neboli životností daného klíče.

Prvočíslo bylo vybráno v roce 2003 a osoba, která toto číslo vybrala (TheCrypto), již není vývojářem I2P. Proto nevíme, zda je zvolené prvočíslo 'silné prvočíslo'. Pokud bude v budoucnu zvoleno větší prvočíslo, mělo by to být silné prvočíslo a zdokumentujeme proces jeho konstrukce.

## Nové algoritmy podpisu

Od verze 0.9.12 router podporuje další algoritmy podpisů, které jsou bezpečnější než 1024-bitové DSA. První použití bylo pro Destinations; podpora pro Router Identities byla přidána ve verzi 0.9.16. Existující Destinations nelze migrovat ze starých na nové podpisy; nicméně existuje podpora pro jeden tunnel s několika Destinations, což poskytuje způsob, jak přejít na novější typy podpisů. Typ podpisu je zakódován v Destination a Router Identity, takže nové algoritmy podpisů nebo křivky mohou být kdykoliv přidány.

Aktuálně podporované typy podpisů jsou následující:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (není široce používáno)
- ECDSA-SHA512-P521 (není široce používáno)
- EdDSA-SHA512-Ed25519 (výchozí od verze 0.9.15)
- RedDSA-SHA512-Ed25519 (od verze 0.9.39)

Další typy podpisů se používají pouze na aplikační vrstvě, především pro podepisování a ověřování su3 souborů. Tyto typy podpisů jsou následující:

- RSA-SHA256-2048 (není široce používané)
- RSA-SHA384-3072 (není široce používané)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (od verze 0.9.25; není široce používané)

### ECDSA

ECDSA používá standardní NIST křivky a standardní SHA-2 hashe.

Nové destinace jsme migrovali na ECDSA-SHA256-P256 v časovém období verzí 0.9.16 - 0.9.19. Použití pro Router Identity je podporováno od verze 0.9.16 a migrace existujících routerů proběhla v roce 2015.

### RSA

Standardní RSA PKCS#1 v1.5 (RFC 2313) s veřejným exponentem F4 = 65537.

RSA se nyní používá pro podepisování veškerého důvěryhodného obsahu mimo síť, včetně aktualizací routerů, reseeding, pluginů a novinek. Podpisy jsou vloženy do formátu "su3" [UPDATES]. Doporučují se 4096-bitové klíče a používají je všichni známí podepisovatelé. RSA se nepoužívá ani se neplánuje použití v žádných síťových Destinations nebo Router Identities.

### EdDSA 25519

Standardní EdDSA používající křivku 25519 a standardní 512-bitové SHA-2 hashe.

Podporováno od verze 0.9.15.

Destinace a identity routerů byly migrovány koncem roku 2015.

### RedDSA 25519

Standardní EdDSA používající křivku 25519 a standardní 512-bitové SHA-2 hashe, ale s různými soukromými klíči a menšími úpravami podpisu. Pro šifrované leaseSet. Podrobnosti najdete v [EncryptedLeaseSet](/docs/specs/encryptedleaseset) a [Red25519](/docs/specs/red25519).

Podporováno od verze 0.9.39.

## Hashe

Hashe jsou používány v algoritech pro podpisy a jako klíče v síťové DHT.

Starší algoritmy pro podepisování používají SHA1 a SHA256. Novější algoritmy pro podepisování používají SHA512. DHT používá SHA256.

### SHA256

DHT hashe v rámci I2P jsou standardní SHA256.

#### Zastaralost

Zranitelnost sítě vůči útoku SHA-256 a dopad přechodu na delší hash má být prostudován. Může být velmi obtížné učinit jakoukoli změnu zpětně kompatibilní.

## Transporty

Na nejnižší vrstvě protokolu je komunikace mezi routery chráněna zabezpečením transportní vrstvy.

NTCP2 připojení používají X25519 Diffie-Hellman a ChaCha20/Poly1305 ověřené šifrování.

SSU a zastaralé NTCP transporty používají 256bajtovou (2048bitovou) výměnu klíčů Diffie-Hellman se stejným sdíleným prvočíslem a generátorem, jak je specifikováno výše pro ElGamal, následovanou symetrickým šifrováním AES, jak je popsáno výše.

SSU je plánováno k migraci na SSU2 (s X25519 a ChaCha20/Poly1305).

Všechny transporty poskytují dokonalé forward secrecy [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) na transportních spojeních.

### NTCP2 připojení {#tcp}

NTCP2 spojení používají X25519 Diffie-Hellman a ChaCha20/Poly1305 ověřené šifrování a framework protokolu Noise [Noise](https://noiseprotocol.org/noise.html).

Podrobnosti a odkazy naleznete ve specifikaci NTCP2 [NTCP2](/docs/specs/ntcp2).

### UDP připojení {#udp}

SSU (UDP transport) šifruje každý paket pomocí AES256/CBC s explicitním IV i MAC (HMAC-MD5-128) poté, co se dohodne na dočasném session klíči prostřednictvím 2048 bitové Diffie-Hellman výměny, station-to-station autentizace s DSA klíčem druhého routeru, navíc každá síťová zpráva má svůj vlastní hash pro místní kontrolu integrity.

Podrobnosti najdete ve specifikaci SSU.

VAROVÁNÍ - I2P's HMAC-MD5-128 používaný v SSU je zjevně nestandardní. Zjevně dřívější verze SSU používala HMAC-SHA256, a poté byla z výkonnostních důvodů přepnuta na MD5-128, ale velikost 32-bajtového bufferu zůstala beze změny. Pro podrobnosti viz HMACGenerator.java a poznámky ke stavu z 05.07.2005.

### NTCP spojení

NTCP se již nepoužívá, byl nahrazen NTCP2.

NTCP spojení byla vyjednána s implementací 2048 Diffie-Hellman, využívající identitu routeru k pokračování se station to station dohodou, následovanou některými šifrovanými poli specifickými pro protokol, přičemž všechna následující data byla šifrována pomocí AES (jak výše). Primárním důvodem pro provedení DH vyjednávání namísto použití ElGamalAES+SessionTag je, že poskytuje '(dokonalé) forward secrecy' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy), zatímco ElGamalAES+SessionTag nikoli.

## Reference

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Benchmarky Crypto++, původně na http://www.eskimo.com/~weidai/benchmarks.html (nyní nedostupné), zachráněno z http://www.archive.org/, datováno 23. dubna 2008.
- [Common](/docs/specs/common-structures) - Specifikace společných struktur
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, str. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
