---
title: "Kryptographie-Spezifikation auf niedriger Ebene"
description: "Details der kryptographischen Algorithmen, die in I2P verwendet werden, auf niedriger Ebene"
slug: "cryptography"
aliases:
  - "/de/how_cryptography"
  - "/de/how_cryptography/"
category: "Design"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Überblick

> **Hinweis:** Dieses Dokument ist größtenteils veraltet. Siehe die folgenden Dokumente für aktuelle Spezifikationen: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Diese Seite spezifiziert die technischen Details der Kryptographie in I2P.

Es werden mehrere kryptografische Algorithmen innerhalb von I2P verwendet. Im ursprünglichen Design von I2P gab es nur einen von jeder Art - einen symmetrischen Algorithmus, einen asymmetrischen Algorithmus, einen Signaturalgorithmus und einen Hash-Algorithmus. Es gab keine Vorkehrungen, um weitere Algorithmen hinzuzufügen oder zu sichereren zu migrieren.

In den letzten Jahren haben wir ein Framework hinzugefügt, um mehrere Primitive und Kombinationen auf rückwärtskompatible Weise zu unterstützen. Zahlreiche Signatur-Algorithmen mit unterschiedlichen Schlüssel- und Signaturlängen werden durch "signature types" (Signaturtypen) definiert. End-to-End-Verschlüsselungsverfahren, die eine Kombination aus asymmetrischer und symmetrischer Verschlüsselung mit unterschiedlichen Schlüssellängen verwenden, werden durch "encryption types" (Verschlüsselungstypen) definiert.

Verschiedene Protokolle und Datenstrukturen in I2P enthalten Felder zur Angabe des Signaturtyps und/oder Verschlüsselungstyps. Diese Felder definieren zusammen mit den Typdefinitionen die Schlüssel- und Signaturlängen sowie die kryptografischen Primitive, die für ihre Verwendung erforderlich sind. Die Definitionen der Signatur- und Verschlüsselungstypen finden sich in der [Common Structures Spezifikation](/docs/specs/common-structures).

Die ursprünglichen I2P-Protokolle NTCP, SSU und ElGamal/AES+SessionTags verwenden eine Kombination aus ElGamal asymmetrischer Verschlüsselung und AES symmetrischer Verschlüsselung. Neuere Protokolle NTCP2 und ECIES-X25519-AEAD-Ratchet verwenden eine Kombination aus X25519-Schlüsselaustausch und ChaCha20/Poly1305 symmetrischer Verschlüsselung.

- ECIES-X25519-AEAD-Ratchet hat ElGamal/AES+SessionTags ersetzt.
- NTCP2 hat NTCP ersetzt.
- SSU2 hat SSU ersetzt.
- X25519 tunnel-Erstellung hat ElGamal tunnel-Erstellung ersetzt.

## Asymmetrische Verschlüsselung

Der ursprüngliche asymmetrische Verschlüsselungsalgorithmus in I2P ist ElGamal. Der neuere Algorithmus, der an verschiedenen Stellen verwendet wird, ist ECIES X25519 DH-Schlüsselaustausch.

Wir sind dabei, die gesamte ElGamal-Nutzung auf X25519 zu migrieren.

NTCP (mit ElGamal) wurde zu NTCP2 (mit X25519) migriert. ElGamal/AES+SessionTag wird zu ECIES-X25519-AEAD-Ratchet migriert.

### X25519

Für Details zur X25519-Verwendung siehe [NTCP2](/docs/specs/ntcp2) und [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal wird an mehreren Stellen in I2P verwendet:

- Um router-zu-router TunnelBuild-Nachrichten zu verschlüsseln
- Für Ende-zu-Ende (destination-zu-destination) Verschlüsselung als Teil von ElGamal/AES+SessionTag unter Verwendung des Verschlüsselungsschlüssels im leaseSet
- Für die Verschlüsselung einiger netDb-Speicher und -Abfragen, die an floodfill router als Teil von ElGamal/AES+SessionTag gesendet werden (destination-zu-router oder router-zu-router).

Wir verwenden gemeinsame Primzahlen für 2048-Bit-ElGamal-Verschlüsselung und -Entschlüsselung, wie in IETF [RFC-3526](http://tools.ietf.org/html/rfc3526) angegeben. Derzeit verwenden wir ElGamal nur zur Verschlüsselung des IV und Sitzungsschlüssels in einem einzigen Block, gefolgt von der AES-verschlüsselten Nutzlast unter Verwendung dieses Schlüssels und IV.

Das unverschlüsselte ElGamal enthält:

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
Das H(data) ist der SHA256 der Daten, die im ElGamal-Block verschlüsselt sind, und wird von einem zufälligen Byte ungleich null vorangestellt. Dieses Byte ist seit Version 0.9.28 tatsächlich zufällig; davor war es immer 0xFF. Es könnte möglicherweise in Zukunft für Flags verwendet werden. Die im Block verschlüsselten Daten können bis zu 222 Bytes lang sein. Da die verschlüsselten Daten eine beträchtliche Anzahl von Nullen enthalten können, wenn der Klartext kleiner als 222 Bytes ist, wird empfohlen, dass höhere Schichten den Klartext mit zufälligen Daten auf 222 Bytes auffüllen. Gesamtlänge: typischerweise 255 Bytes.

Das verschlüsselte ElGamal enthält:

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
Jeder verschlüsselte Teil wird mit Nullen auf eine Größe von exakt 257 Bytes aufgefüllt. Gesamtlänge: 514 Bytes. Bei typischer Verwendung füllen höhere Schichten die Klartextdaten auf 222 Bytes auf, was zu einem unverschlüsselten Block von 255 Bytes führt. Dieser wird als zwei 256-Byte verschlüsselte Teile kodiert, und es gibt ein einzelnes Null-Byte als Auffüllung vor jedem Teil auf dieser Schicht.

Siehe den ElGamal-Code [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

Die gemeinsame Primzahl ist die Oakley-Primzahl für 2048-Bit-Schlüssel [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
oder als hexadezimaler Wert:

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
Verwende 2 als Generator.

#### Kurzer Exponent {#exponent}

Während die Standard-Exponentengröße 2048 Bits (256 Bytes) beträgt und der I2P PrivateKey volle 256 Bytes umfasst, verwenden wir in einigen Fällen die kurze Exponentengröße von 226 Bits (28,25 Bytes). Dies sollte sicher für die Verwendung mit den Oakley-Primzahlen sein [vanOorschot1996] [BENCHMARKS].

Außerdem unterstützt [Koshiba2004] dies anscheinend, laut diesem sci.crypt Thread [SCI.CRYPT]. Der Rest des PrivateKey wird mit Nullen aufgefüllt.

Vor Version 0.9.8 verwendeten alle router den kurzen Exponenten. Ab Version 0.9.8 verwenden 64-Bit-x86-router einen vollständigen 2048-Bit-Exponenten. Alle router verwenden nun den vollständigen Exponenten, mit Ausnahme einer kleinen Anzahl von routern auf sehr langsamer Hardware, die weiterhin den kurzen Exponenten verwenden, da sie sich Sorgen über die Prozessorbelastung machen. Der Übergang zu einem längeren Exponenten für diese Plattformen ist ein Thema für weitere Untersuchungen.

#### Veralterung

Die Anfälligkeit des Netzwerks für einen ElGamal-Angriff und die Auswirkungen der Umstellung auf eine längere Bit-Länge sollen untersucht werden. Es könnte sehr schwierig sein, eine solche Änderung rückwärtskompatibel zu gestalten.

## Symmetrische Verschlüsselung

Der ursprüngliche symmetrische Verschlüsselungsalgorithmus in I2P ist AES. Der neuere Algorithmus, der an verschiedenen Stellen verwendet wird, ist Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Wir sind dabei, die gesamte AES-Nutzung auf ChaCha20/Poly1305 zu migrieren.

NTCP (mit AES) wurde zu NTCP2 (mit ChaCha20/Poly1305) migriert. ElGamal/AES+SessionTag wird zu ECIES-X25519-AEAD-Ratchet migriert.

### ChaCha20/Poly1305

Für Details zur Verwendung von ChaCha20/Poly1305 siehe [NTCP2](/docs/specs/ntcp2) und [ECIES](/docs/specs/ecies).

### AES

AES wird für symmetrische Verschlüsselung verwendet, in mehreren Fällen:

- Für SSU transport-Verschlüsselung (siehe Abschnitt "Transports") nach DH-Schlüsselaustausch
- Für Ende-zu-Ende (destination-zu-destination) Verschlüsselung als Teil von ElGamal/AES+SessionTag
- Für Verschlüsselung einiger netDb-Speicherungen und -Abfragen, die an floodfill router als Teil von ElGamal/AES+SessionTag gesendet werden (destination-zu-router oder router-zu-router).
- Für Verschlüsselung periodischer tunnel-Testnachrichten, die vom router an sich selbst durch seine eigenen tunnel gesendet werden.

Wir verwenden AES mit 256-Bit-Schlüsseln und 128-Bit-Blöcken im CBC-Modus. Das verwendete Padding ist in IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, Abschnitt 8.1 (für Blocktyp 02)) spezifiziert. In diesem Fall besteht das Padding aus pseudozufällig generierten Oktetts, um 16-Byte-Blöcke zu erreichen. Siehe insbesondere den CBC-Code [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) und die Cryptix AES-Implementierung [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), sowie das Padding, das in der ElGamalAESEngine.getPadding-Funktion zu finden ist [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Veralterung

Die Anfälligkeit des Netzwerks für einen AES-Angriff und die Auswirkungen des Übergangs zu einer längeren Bitlänge sollen untersucht werden. Es könnte sehr schwierig sein, Änderungen rückwärtskompatibel zu gestalten.

## Signaturen {#sig}

Zahlreiche Signaturalgorithmen mit unterschiedlichen Schlüssel- und Signaturlängen werden durch Signaturtypen definiert. Es ist relativ einfach, weitere Signaturtypen hinzuzufügen.

EdDSA-SHA512-Ed25519 ist der aktuelle Standard-Signaturalgorithmus. DSA, der ursprüngliche Algorithmus bevor wir Unterstützung für Signaturtypen hinzufügten, wird immer noch im Netzwerk verwendet.

### DSA

Signaturen werden mit 1024 Bit [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) (L=1024, N=160) generiert und verifiziert, wie in [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java) implementiert. DSA wurde gewählt, weil es für Signaturen viel schneller ist als ElGamal.

#### SEED

160 Bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Zähler

```
33
```
#### DSA-Primzahl (p)

1024 Bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA-Quotient (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA-Generator (g)

1024 Bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
Der SigningPublicKey ist 1024 Bits groß. Der SigningPrivateKey ist 160 Bits groß.

#### Veralterung

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) empfiehlt ein Minimum von (L=2048, N=224) für die Verwendung nach 2010. Dies kann etwas durch die "Kryptoperiode" oder Lebensdauer eines bestimmten Schlüssels abgemildert werden.

Die Primzahl wurde 2003 gewählt, und die Person, die die Zahl ausgewählt hat (TheCrypto), ist derzeit kein I2P-Entwickler mehr. Daher wissen wir nicht, ob die gewählte Primzahl eine 'starke Primzahl' ist. Falls für zukünftige Zwecke eine größere Primzahl gewählt wird, sollte dies eine starke Primzahl sein, und wir werden den Konstruktionsprozess dokumentieren.

## Neue Signatur-Algorithmen

Ab Release 0.9.12 unterstützt der router zusätzliche Signatur-Algorithmen, die sicherer sind als 1024-Bit DSA. Die erste Verwendung erfolgte für Destinations; Unterstützung für Router Identities wurde in Release 0.9.16 hinzugefügt. Bestehende Destinations können nicht von alten zu neuen Signaturen migriert werden; es gibt jedoch Unterstützung für einen einzelnen tunnel mit mehreren Destinations, was eine Möglichkeit bietet, zu neueren Signaturtypen zu wechseln. Der Signaturtyp wird in der Destination und Router Identity kodiert, sodass neue Signatur-Algorithmen oder Kurven jederzeit hinzugefügt werden können.

Die derzeit unterstützten Signaturtypen sind wie folgt:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (nicht weit verbreitet)
- ECDSA-SHA512-P521 (nicht weit verbreitet)
- EdDSA-SHA512-Ed25519 (Standard seit Release 0.9.15)
- RedDSA-SHA512-Ed25519 (seit Release 0.9.39)

Zusätzliche Signaturtypen werden nur auf der Anwendungsschicht verwendet, hauptsächlich zum Signieren und Verifizieren von su3-Dateien. Diese Signaturtypen sind wie folgt:

- RSA-SHA256-2048 (nicht weit verbreitet)
- RSA-SHA384-3072 (nicht weit verbreitet)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (ab Version 0.9.25; nicht weit verbreitet)

### ECDSA

ECDSA verwendet die standardmäßigen NIST-Kurven und standardmäßige SHA-2-Hashes.

Wir migrierten neue Ziele zu ECDSA-SHA256-P256 im Veröffentlichungszeitraum von 0.9.16 - 0.9.19. Die Verwendung für Router Identities wird seit Version 0.9.16 unterstützt und die Migration bestehender router fand 2015 statt.

### RSA

Standard RSA PKCS#1 v1.5 (RFC 2313) mit dem öffentlichen Exponenten F4 = 65537.

RSA wird nun für die Signierung aller Out-of-Band vertrauenswürdigen Inhalte verwendet, einschließlich router-Updates, Reseeding, Plugins und Nachrichten. Die Signaturen sind im "su3"-Format eingebettet [UPDATES]. 4096-Bit-Schlüssel werden empfohlen und von allen bekannten Signierern verwendet. RSA wird nicht verwendet und ist auch nicht für die Verwendung in netzwerkinternen Destinations oder Router Identities geplant.

### EdDSA 25519

Standard EdDSA mit Kurve 25519 und standardmäßigen 512-Bit SHA-2-Hashes.

Unterstützt seit Release 0.9.15.

Destinations und Router Identities wurden Ende 2015 migriert.

### RedDSA 25519

Standard EdDSA mit Kurve 25519 und standardmäßigen 512-Bit SHA-2-Hashes, aber mit unterschiedlichen privaten Schlüsseln und geringfügigen Änderungen beim Signieren. Für verschlüsselte leaseSet. Siehe [EncryptedLeaseSet](/docs/specs/encryptedleaseset) und [Red25519](/docs/specs/red25519) für Details.

Unterstützt seit Release 0.9.39.

## Hashes

Hashes werden in Signaturalgorithmen und als Schlüssel in der DHT des Netzwerks verwendet.

Ältere Signaturalgorithmen verwenden SHA1 und SHA256. Neuere Signaturalgorithmen verwenden SHA512. Die DHT verwendet SHA256.

### SHA256

DHT-Hashes innerhalb von I2P sind Standard SHA256.

#### Veralterung

Die Verwundbarkeit des Netzwerks gegenüber einem SHA-256-Angriff und die Auswirkungen des Übergangs zu einem längeren Hash sollen untersucht werden. Es könnte sehr schwierig sein, eine solche Änderung rückwärtskompatibel zu gestalten.

## Transports

Auf der niedrigsten Protokollebene wird die Punkt-zu-Punkt-Kommunikation zwischen Routern durch die Sicherheit der Transportschicht geschützt.

NTCP2-Verbindungen verwenden X25519 Diffie-Hellman und ChaCha20/Poly1305 authentifizierte Verschlüsselung.

SSU und die veralteten NTCP-Transporte verwenden einen 256 Byte (2048 Bit) Diffie-Hellman-Schlüsselaustausch mit derselben gemeinsamen Primzahl und demselben Generator, wie oben für ElGamal spezifiziert, gefolgt von symmetrischer AES-Verschlüsselung wie oben beschrieben.

SSU soll zu SSU2 (mit X25519 und ChaCha20/Poly1305) migriert werden.

Alle Transporte bieten Perfect Forward Secrecy [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) auf den Transportverbindungen.

### NTCP2-Verbindungen {#tcp}

NTCP2-Verbindungen verwenden X25519 Diffie-Hellman und ChaCha20/Poly1305 authentifizierte Verschlüsselung sowie das Noise-Protokoll-Framework [Noise](https://noiseprotocol.org/noise.html).

Siehe die NTCP2-Spezifikation [NTCP2](/docs/specs/ntcp2) für Details und Referenzen.

### UDP-Verbindungen {#udp}

SSU (der UDP-Transport) verschlüsselt jedes Paket mit AES256/CBC mit sowohl einem expliziten IV als auch MAC (HMAC-MD5-128), nachdem ein ephemerer Sitzungsschlüssel durch einen 2048-Bit-Diffie-Hellman-Austausch vereinbart wurde, Station-zu-Station-Authentifizierung mit dem DSA-Schlüssel des anderen routers, plus jede Netzwerknachricht hat ihre eigene Prüfsumme für lokale Integritätsprüfung.

Siehe die SSU-Spezifikation für Details.

WARNUNG - I2Ps HMAC-MD5-128, das in SSU verwendet wird, ist anscheinend nicht standardkonform. Offenbar nutzte eine frühe Version von SSU HMAC-SHA256, und dann wurde aus Leistungsgründen auf MD5-128 umgestellt, aber die 32-Byte-Puffergröße blieb unverändert. Siehe HMACGenerator.java und die Statusnotizen vom 2005-07-05 für Details.

### NTCP-Verbindungen

NTCP wird nicht mehr verwendet, es wurde durch NTCP2 ersetzt.

NTCP-Verbindungen wurden mit einer 2048 Diffie-Hellman-Implementierung ausgehandelt, wobei die Identität des routers verwendet wurde, um mit einer Station-zu-Station-Vereinbarung fortzufahren, gefolgt von einigen verschlüsselten protokollspezifischen Feldern, wobei alle nachfolgenden Daten mit AES verschlüsselt wurden (wie oben). Der Hauptgrund für die DH-Verhandlung anstelle der Verwendung von ElGamalAES+SessionTag ist, dass sie '(perfekte) Forward Secrecy' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) bietet, während ElGamalAES+SessionTag dies nicht tut.

## Referenzen

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Crypto++ Benchmarks, ursprünglich unter http://www.eskimo.com/~weidai/benchmarks.html (jetzt nicht mehr verfügbar), gerettet von http://www.archive.org/, datiert vom 23. April 2008.
- [Common](/docs/specs/common-structures) - Spezifikation für gemeinsame Strukturen
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, S. 173-186
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
