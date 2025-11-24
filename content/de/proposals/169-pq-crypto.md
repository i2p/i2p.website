---
title: "Post-Quantum Crypto-Protokolle"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Offen"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Überblick

Während die Forschung und der Wettbewerb um geeignete Post-Quanten- (PQ) Kryptografie seit einem Jahrzehnt voranschreiten, sind die Entscheidungen erst kürzlich klarer geworden.

Wir begannen 2022 mit der Untersuchung der Implikationen der PQ-Kryptografie [FORUM](http://zzz.i2p/topics/3294).

TLS-Standards haben in den letzten zwei Jahren Unterstützung für Hybridverschlüsselung hinzugefügt und werden jetzt für einen erheblichen Teil des verschlüsselten Verkehrs im Internet verwendet, dank der Unterstützung in Chrome und Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST hat kürzlich die empfohlenen Algorithmen für Post-Quanten-Kryptografie finalisiert und veröffentlicht [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Mehrere gängige Kryptografie-Bibliotheken unterstützen jetzt die NIST-Standards oder werden bald Unterstützung veröffentlichen.

Sowohl [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) als auch [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) empfehlen, dass die Migration sofort beginnen sollte. Siehe auch die NSA-PQ-FAQ von 2022 [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P sollte ein Vorreiter in Sachen Sicherheit und Kryptografie sein. Jetzt ist die Zeit, die empfohlenen Algorithmen zu implementieren. Mit unserem flexiblen Krypto- und Signatur-Typsystem werden wir Typen für Hybrid-Krypto sowie für PQ- und Hybridsignaturen hinzufügen.


## Ziele

- Auswahl von PQ-resistenten Algorithmen
- Hinzufügen von PQ-only und hybriden Algorithmen zu I2P-Protokollen, wo es angemessen ist
- Definition mehrerer Varianten
- Auswahl der besten Varianten nach Implementierung, Tests, Analyse und Forschung
- Unterstützung schrittweise und mit Abwärtskompatibilität hinzufügen


## Nicht-Ziele

- Einwegverschlüsselungsprotokolle (Noise N) nicht ändern
- Nicht von SHA256 abweichen, nicht kurzfristig durch PQ bedroht
- Die endgültig bevorzugten Varianten zu diesem Zeitpunkt nicht auswählen


## Bedrohungsmodell

- Router am OBEP oder IBGW, möglicherweise in Kollaboration, speichern Knoblauch-Nachrichten zur späteren Entschlüsselung (Vorwärtsgeheimnis)
- Netzwerkbeobachter speichern Transportnachrichten zur späteren Entschlüsselung (Vorwärtsgeheimnis)
- Netzwerkteilnehmer fälschen Signaturen für RI, LS, Streaming, Datagramme oder andere Strukturen


## Betroffene Protokolle

Wir werden die folgenden Protokolle ändern, grob in der Reihenfolge der Entwicklung. Die Gesamtumsetzung wird wahrscheinlich von Ende 2025 bis Mitte 2027 dauern. Siehe den Abschnitt „Prioritäten und Rollout“ unten für Details.


| Protokoll / Funktion | tatus |
| -------------------- | ----- |
| Hybrid MLKEM Ratchet und LS | enehmi |
| Hybrid MLKEM NTCP2 | inige |
| Hybrid MLKEM SSU2 | inige |
| MLDSA SigTypes 12-14 | orschl |
| MLDSA Dests | eteste |
| Hybrid SigTypes 15-17 | orläuf |
| Hybrid Dests |  |




## Design

Wir werden die NIST FIPS 203 und 204 Standards [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) unterstützen, die auf CRYSTALS-Kyber und CRYSTALS-Dilithium (Versionen 3.1, 3 und älter) basieren, aber NICHT kompatibel mit ihnen sind.



### Schlüsselaustausch

Wir werden hybriden Schlüsselaustausch in den folgenden Protokollen unterstützen:

| Proto | Noise-Typ | Unterstützt nur | ?  Unterstützt |
| ----- | --------- | --------------- | -------------- |
| NTCP2 | XK | nein | ja |
| SSU2 | XK | nein | ja |
| Ratchet | IK | nein | ja |
| TBM | N | nein | nein |
| NetDB | N | nein | nein |


PQ KEM bietet nur flüchtige Schlüssel und unterstützt nicht direkt statische Key-Handshakes wie Noise XK und IK.

Noise N verwendet keinen bidirektionalen Schlüsselaustausch und ist daher nicht für Hybridverschlüsselung geeignet.

Daher werden wir nur hybride Verschlüsselung für NTCP2, SSU2 und Ratchet unterstützen. Wir werden die drei ML-KEM-Varianten wie in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definieren, für insgesamt 3 neue Verschlüsselungstypen.
Hybride Typen werden nur in Kombination mit X25519 definiert.

Die neuen Verschlüsselungstypen sind:

| Typ | Code |
| --- | ---- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


Der Overhead wird beträchtlich sein. Die typischen Nachrichtengrößen 1 und 2 (für XK und IK) liegen derzeit bei etwa 100 Byte (vor jeglichem zusätzlichen Payload). Dies wird sich je nach Algorithmus um 8x bis 15x erhöhen.


### Signaturen

Wir werden PQ- und Hybridsignaturen in den folgenden Strukturen unterstützen:

| Typ | Unterstützt nur | ?  Unterstützt |
| --- | --------------- | -------------- |
| RouterInfo | ja | a |
| LeaseSet | ja | a |
| Streaming SYN/SYNACK/Close | ja | a |
| Repliable Datagrams | ja | a |
| Datagram2 (prop. 163) | ja | a |
| I2CP create session msg | ja | a |
| SU3 files | ja | a |
| X.509 certificates | ja | a |
| Java keystores | ja | a |



So werden wir sowohl PQ-only als auch Hybridsignaturen unterstützen. Wir werden die drei ML-DSA Variationen wie in [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definieren, drei Hybridvarianten mit Ed25519 und drei PQ-only Varianten mit Prehash nur für SU3-Dateien, für insgesamt 9 neue Signaturtypen.
Hybride Typen werden nur in Kombination mit Ed25519 definiert.
Wir werden die standardmäßige ML-DSA verwenden, NICHT die Pre-Hash-Varianten (HashML-DSA), außer für SU3-Dateien.

Wir werden die "hedged" oder randomisierte Signaturvariante verwenden, nicht die "deterministische" Variante, wie in [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Abschnitt 3.4 definiert. Dies stellt sicher, dass jede Signatur unterschiedlich ist, selbst bei gleichen Daten, und bietet zusätzlichen Schutz vor Seitenkanalangriffen. Siehe den Abschnitt Implementierungshinweise unten für zusätzliche Details zur Auswahl des Algorithmus einschließlich Codierung und Kontext.


Die neuen Signaturtypen sind:

| Typ | ode |
| --- | --- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


X.509-Zertifikate und andere DER-Codierungen verwenden die in [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/) definierten zusammengesetzten Strukturen und OIDs.

Der Overhead wird beträchtlich sein. Die typischen Ziel- und Routeridentity-Größen von Ed25519 liegen bei 391 Byte. Diese werden sich je nach Algorithmus um das 3,5- bis 6,8-fache erhöhen. Ed25519-Signaturen sind 64 Byte. Diese werden sich je nach Algorithmus um das 38- bis 76-fache erhöhen. Typische signierte RouterInfo, LeaseSet, repliable Datagrams und signierte Streaming-Nachrichten sind etwa 1KB. Diese werden sich je nach Algorithmus um das 3- bis 8-fache erhöhen.

Da die neuen Zugriffs- und Routeridentity-Typen kein Padding enthalten, sind sie nicht komprimierbar. Die Größe von Zielen und Routeridentitäten, die in der Übertragung gzip-komprimiert sind, wird sich je nach Algorithmus um das 12- bis 38-fache erhöhen.



### Rechtlich zulässige Kombinationen

Für Ziele sind die neuen Signaturtypen mit allen Verschlüsselungstypen im LeaseSet kompatibel. Setzen Sie den Verschlüsselungstyp im Schlüsselzertifikat auf NONE (255).

Für RouterIdentitäten ist der ElGamal-Verschlüsselungstyp veraltet. Die neuen Signaturtypen sind nur mit X25519 (Typ 4) Verschlüsselung kompatibel. Die neuen Verschlüsselungstypen werden in den Router-Adressen angezeigt. Der Verschlüsselungstyp im Schlüsselzertifikat bleibt bei Typ 4.



### Erforderliche neue Kryptografie

- ML-KEM (früher CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (früher CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (früher Keccak-256) [FIPS202]_ Nur für SHAKE128 verwendet
- SHA3-256 (früher Keccak-512) [FIPS202]_
- SHAKE128 und SHAKE256 (XOF-Erweiterungen zu SHA3-128 und SHA3-256) [FIPS202]_

Testvektoren für SHA3-256, SHAKE128 und SHAKE256 sind bei [NIST-VECTORS]_ vorhanden.

Beachten Sie, dass die Java bouncycastle Bibliothek all dies unterstützt. C++ Bibliotheksunterstützung ist in OpenSSL 3.5 [OPENSSL]_ enthalten.


### Alternativen

Wir werden [FIPS205]_ (Sphincs+) nicht unterstützen, es ist wesentlich langsamer und größer als ML-DSA. Wir werden den kommenden FIPS206 (Falcon) nicht unterstützen, da er noch nicht standardisiert ist. Wir werden NTRU oder andere PQ-Kandidaten, die von NIST nicht standardisiert wurden, nicht unterstützen.


Rosenpass
```````````

Es gibt einige Forschungen [PQ-WIREGUARD]_ zur Anpassung von Wireguard (IK) für reine PQ-Kryptografie, aber es gibt mehrere offene Fragen in diesem Papier. Später wurde dieser Ansatz als Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_ für PQ Wireguard implementiert.

Rosenpass verwendet einen Noise KK-ähnlichen Handshake mit vorgeteilten Classic McEliece 460896 statischen Schlüsseln (jeweils 500 KB) und Kyber-512 (im Wesentlichen MLKEM-512) flüchtigen Schlüsseln. Da die Classic McEliece Chiffratexttypen nur 188 Bytes haben und die Kyber-512 öffentlichen Schlüssel und Chiffratexttypen vernünftig sind, passen beide Handshake-Nachrichten in eine Standard-UDP-MTU. Der Ausgangsschlüssel (osk) vom PQ KK-Handschlag wird als Eingangs-vorgeteilter Schlüssel (psk) für den Standard-Wireguard IK-Handshake verwendet. Daher gibt es insgesamt zwei vollständige Handshakes, einen reinen PQ und einen reinen X25519.

Wir können keine dieser Methoden verwenden, um unsere XK- und IK-Handshakes zu ersetzen, weil:

- Wir können kein KK ausführen, Bob hat nicht den statischen Schlüssel von Alice
- 500 KB statische Schlüssel sind viel zu groß
- Wir wollen keine zusätzliche Round-Trip

Das Whitepaper enthält viele gute Informationen, und wir werden es für Ideen und Inspiration überprüfen. TODO.



## Spezifikation

### Allgemeine Strukturen

Aktualisieren Sie die Abschnitte und Tabellen im Dokument „Allgemeine Strukturen“ [COMMON](https://geti2p.net/spec/common-structures) wie folgt:


Öffentlicher Schlüssel
````````````````

Die neuen Typen für öffentliche Schlüssel sind:

| Typ | Öffentlicher Schl | ssellä | e Sei |
| --- | ----------------- | ------ | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM768_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM1024_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM512 | 800 | 0.9.xx | Siehe |
| MLKEM768 | 1184 | 0.9.xx | Siehe |
| MLKEM1024 | 1568 | 0.9.xx | Siehe |
| MLKEM512_CT | 768 | 0.9.xx | Siehe |
| MLKEM768_CT | 1088 | 0.9.xx | Siehe |
| MLKEM1024_CT | 1568 | 0.9.xx | Siehe |
| NONE | 0 | 0.9.xx | Siehe |


Hybride öffentliche Schlüssel sind der X25519-Schlüssel.
KEM öffentliche Schlüssel sind die flüchtigen PQ-Schlüssel, die von Alice zu Bob gesendet werden.
Codierung und Byte-Reihenfolge sind in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert.

MLKEM*_CT-Schlüssel sind keine echten öffentlichen Schlüssel, sie sind der "Chiffrat", der von Bob zu Alice im Noise-Handshake gesendet wird.
Sie sind hier der Vollständigkeit halber aufgeführt.



Privatschlüssel
````````````````

Die neuen Typen für Privatschlüssel sind:

| Typ | Privatschlüssellän | e Seit | Verw |
| --- | ------------------ | ------ | ---- |
| MLKEM512_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM768_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM1024_X25519 | 32 | 0.9.xx | Siehe |
| MLKEM512 | 1632 | 0.9.xx | Siehe |
| MLKEM768 | 2400 | 0.9.xx | Siehe |
| MLKEM1024 | 3168 | 0.9.xx | Siehe |


Hybride Privatschlüssel sind die X25519-Schlüssel.
KEM-Privatschlüssel sind nur für Alice.
KEM-Codierung und Byte-Reihenfolge sind in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert.




Signaturöffentlicher Schlüssel
````````````````

Die neuen Typen für signaturöffentliche Schlüssel sind:

| Typ | Länge (Bytes) | eit | erwen |
| --- | ------------- | --- | ----- |
| MLDSA44 | 1312 | 0.9.xx | Siehe |
| MLDSA65 | 1952 | 0.9.xx | Siehe |
| MLDSA87 | 2592 | 0.9.xx | Siehe |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Siehe |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Siehe |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Siehe |
| MLDSA44ph | 1344 | 0.9.xx | Nur f |
| MLDSA65ph | 1984 | 0.9.xx | Nur f |
| MLDSA87ph | 2624 | 0.9.xx | Nur f |


Hybride Signaturöffentliche Schlüssel sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie in [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Codierung und Byte-Reihenfolge sind in [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.


Signaturprivatschlüssel
`````````````````

Die neuen Typen für Signaturprivatschlüssel sind:

| Typ | Länge (Bytes) | eit | erwen |
| --- | ------------- | --- | ----- |
| MLDSA44 | 2560 | 0.9.xx | Siehe |
| MLDSA65 | 4032 | 0.9.xx | Siehe |
| MLDSA87 | 4896 | 0.9.xx | Siehe |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Siehe |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Siehe |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Siehe |
| MLDSA44ph | 2592 | 0.9.xx | Nur f |
| MLDSA65ph | 4064 | 0.9.xx | Nur f |
| MLDSA87ph | 4928 | 0.9.xx | Nur f |


Hybride Signaturprivatschlüssel sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie in [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Codierung und Byte-Reihenfolge sind in [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.


Signatur
````````

Die neuen Signaturtypen sind:

| Typ | Länge (Bytes) | eit | erwen |
| --- | ------------- | --- | ----- |
| MLDSA44 | 2420 | 0.9.xx | Siehe |
| MLDSA65 | 3309 | 0.9.xx | Siehe |
| MLDSA87 | 4627 | 0.9.xx | Siehe |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Siehe |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Siehe |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Siehe |
| MLDSA44ph | 2484 | 0.9.xx | Nur f |
| MLDSA65ph | 3373 | 0.9.xx | Nur f |
| MLDSA87ph | 4691 | 0.9.xx | Nur f |


Hybride Signaturen sind die Ed25519-Signatur gefolgt von der PQ-Signatur, wie in [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Hybride Signaturen werden durch Überprüfung beider Signaturen verifiziert und fehlschlagen, wenn eine davon fehlschlägt.
Codierung und Byte-Reihenfolge sind in [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.



Schlüsselzertifikate
`````````````````

Die neuen Typen für Signaturöffentliche Schlüssel sind:

| Typ | Code-Typ | Gesamtlänge öffentliche | Schlüs | l Sei |
| --- | -------- | ----------------------- | ------ | ----- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Siehe |
| MLDSA65 | 13 | 1952 | 0.9.xx | Siehe |
| MLDSA87 | 14 | 2592 | 0.9.xx | Siehe |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Siehe |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Siehe |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Siehe |
| MLDSA44ph | 18 | n/a | 0.9.xx | Nur f |
| MLDSA65ph | 19 | n/a | 0.9.xx | Nur f |
| MLDSA87ph | 20 | n/a | 0.9.xx | Nur f |




Die neuen Crypto-Publik-Schlüsseltypen sind:

| Typ | Code-Typ | Gesamtlänge öffentliche | Schlü | el Se |
| --- | -------- | ----------------------- | ----- | ----- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Siehe |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Siehe |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Siehe |
| NONE | 255 | 0 | 0.9.xx | Siehe |



Hybride Schlüsseltypen werden NIE in Schlüsselzertifikate aufgenommen; nur in Leasesets.

Bei Zielen mit hybriden oder PQ-Signaturtypen verwenden Sie NONE (Typ 255) für den Verschlüsselungstyp, aber es gibt keinen Krypto-Schlüssel, und der gesamte 384-Byte-Hauptabschnitt ist für den Signatur-Schlüssel.


Zielgrößen
``````````````````

Hier sind die Längen für die neuen Zieltypen. Der Enc-Typ ist für alle NONE (Typ 255) und die Länge des Verschlüsselungsschlüssels wird als 0 behandelt. Der gesamte 384-Byte-Abschnitt wird für den ersten Teil des signaturöffentlichen Schlüssels verwendet. HINWEIS: Dies unterscheidet sich von der Spezifikation für den ECDSA_SHA512_P521 und die RSA-Signaturtypen, bei denen wir den 256-Byte ElGamal-Schlüssel im Ziel beibehielten, obwohl er ungenutzt war.

Kein Padding. Gesamtlänge ist 7 + Gesamtlänge des Schlüssels. Die Länge des Schlüsselzertifikates ist 4 + überschüssige Schlüssellänge.

Beispiel für einen 1319-Byte Ziel-Byte-Stream für MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]



| Typ | Code-Typ | Gesamtlänge öffentliche | Schlüs | l Haup | Üb |
| --- | -------- | ----------------------- | ------ | ------ | --- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |




RouterIdent-Größen
``````````````````

Hier sind die Längen für die neuen Zieltypen. Der Enc-Typ ist für alle X25519 (Typ 4). Der gesamte 352-Byte-Abschnitt nach dem X28819 öffentlichen Schlüssel wird für den ersten Teil des signaturöffentlichen Schlüssels verwendet. Kein Padding. Gesamtlänge ist 39 + Gesamtlänge des Schlüssels. Die Länge des Schlüsselzertifikats ist 4 + überschüssige Schlüssellänge.

Beispiel für einen 1351-Byte Router-Identity-Byte-Stream für MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]



| Typ | Code-Typ | Gesamtlänge öffentliche | Schlüs | l Haup | Üb |
| --- | -------- | ----------------------- | ------ | ------ | --- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |




### Handshake-Muster

Handshakes verwenden [Noise]_ Handshake-Muster.

Die folgende Buchstaben-Zuordnung wird verwendet:

- e = einmaliger flüchtiger Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload
- e1 = einmaliger flüchtiger PQ-Schlüssel, gesendet von Alice zu Bob
- ekem1 = der KEM Chiffrat, gesendet von Bob zu Alice

Die folgenden Modifikationen zu XK und IK für hybrides Vorwärtsgeheimnis (hfs) sind wie in [Noise-Hybrid]_ Abschnitt 5 spezifiziert:

```dataspec

XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 und ekem1 sind verschlüsselt. Siehe Musterdefinitionen unten.
  HINWEIS: e1 und ekem1 haben unterschiedliche Größen (anders als X25519)

```

Das e1-Muster ist wie folgt definiert, wie in [Noise-Hybrid]_ Abschnitt 4 spezifiziert:

```dataspec

Für Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  Für Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)


```


Das ekem1-Muster ist wie folgt definiert, wie in [Noise-Hybrid]_ Abschnitt 4 spezifiziert:

```dataspec

Für Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  Für Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)


```




### KDF für Noise Handshake

Probleme
``````

- Sollten wir die Hash-Funktion des Handshakes ändern? Siehe [Choosing-Hash]_.
  SHA256 ist nicht anfällig für PQ, aber wenn wir unsere Hash-Funktion verbessern wollen, dann jetzt, während wir andere Dinge ändern.
  Der aktuelle IETF SSH-Vorschlag [SSH-HYBRID]_ ist die Verwendung von MLKEM768 mit SHA256 und MLKEM1024 mit SHA384. Dieser Vorschlag enthält eine Diskussion über die Sicherheitsüberlegungen.
- Sollten wir aufhören, 0-RTT-Ratchet-Daten (außer dem LS) zu senden?
- Sollten wir den Ratchet von IK auf XK umstellen, wenn wir keine 0-RTT-Daten senden?


Überblick
````````

Dieser Abschnitt gilt sowohl für IK- als auch für XK-Protokolle.

Der hybride Handshake ist in [Noise-Hybrid]_ definiert. Die erste Nachricht, von Alice zu Bob, enthält e1, den Kapselschlüssel, vor der Nachrichten-Payload. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie EncryptAndHash() darauf auf (als Alice) oder DecryptAndHash() (als Bob). Dann verarbeiten Sie die Nachrichten-Payload wie gewohnt.

Die zweite Nachricht, von Bob zu Alice, enthält ekem1, den Chiffrat, vor der Nachrichten-Payload. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie EncryptAndHash() darauf auf (als Bob) oder DecryptAndHash() (als Alice). Dann berechnen Sie den kem_shared_key und rufen MixKey(kem_shared_key) auf. Dann verarbeiten Sie die Nachrichten-Payload wie gewohnt.


Definierte ML-KEM Operationen
`````````````````````````

Wir definieren die folgenden Funktionen, die den kryptografischen Bausteinen entsprechen, die in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert sind.

(encap_key, decap_key) = PQ_KEYGEN()
    Alice erstellt die Einkapselungs- und Entkapselungsschlüssel
    Der Einkapselungsschlüssel wird in Nachricht 1 gesendet.
    encap_key und decap_key Größen variieren je nach ML-KEM Variante.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob berechnet den Chiffrat und den gemeinsamen Schlüssel, indem er den Chiffrat, den er in Nachricht 1 empfängt, verwendet.
    Der Chiffrat wird in Nachricht 2 gesendet.
    Die Chiffratgröße variiert je nach ML-KEM Variante.
    Der kem_shared_key ist immer 32 Byte.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice berechnet den geteilten Schlüssel, indem sie den Chiffrat, den sie in Nachricht 2 empfängt, verwendet.
    Der kem_shared_key ist immer 32 Byte.

Beachten Sie, dass sowohl der encap_key als auch der ciphertext innerhalb von ChaCha/Poly Blöcken in den Noise Handshake Nachrichten 1 und 2 verschlüsselt sind.
Sie werden als Teil des Handshake-Prozesses entschlüsselt werden.

Der kem_shared_key wird mit MixHash() in den Kettenschlüssel gemischt.
Siehe unten für Details.


Alice KDF für Nachricht 1
`````````````````````````

Für XK: Nach dem 'es'-Nachrichtenmuster und vor der Payload hinzufügen:

ODER

Für IK: Nach dem 'es'-Nachrichtenmuster und vor dem 's'-Nachrichtenmuster hinzufügen:

```text
Dies ist das "e1"-Nachrichtenmuster:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  Ende des "e1"-Nachrichtenmusters.

  HINWEIS: Für den nächsten Abschnitt (Payload für XK oder statischer Schlüssel für IK),
  bleiben die keydata und der Kettenschlüssel gleich,
  und n beträgt jetzt 1 (anstatt 0 für nicht-hybrid).

```


Bob KDF für Nachricht 1
`````````````````````````

Für XK: Nach dem 'es'-Nachrichtenmuster und vor der Payload hinzufügen:

ODER

Für IK: Nach dem 'es'-Nachrichtenmuster und vor dem 's'-Nachrichtenmuster hinzufügen:

```text
Dies ist das "e1"-Nachrichtenmuster:

  // DecryptAndHash(encap_key_section)
  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  Ende des "e1"-Nachrichtenmusters.

  HINWEIS: Für den nächsten Abschnitt (Payload für XK oder statischer Schlüssel für IK),
  bleiben die keydata und der Kettenschlüssel gleich,
  und n beträgt jetzt 1 (anstatt 0 für nicht-hybrid).

```


Bob KDF für Nachricht 2
`````````````````````````

Für XK: Nach dem 'ee'-Nachrichtenmuster und vor der Payload hinzufügen:

ODER

Für IK: Nach dem 'ee'-Nachrichtenmuster und vor dem 'se'-Nachrichtenmuster hinzufügen:

```text
Dies ist das "ekem1"-Nachrichtenmuster:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Ende des "ekem1"-Nachrichtenmusters.

```


Alice KDF für Nachricht 2
`````````````````````````

Nach dem 'ee'-Nachrichtenmuster (und vor dem 'ss'-Nachrichtenmuster für IK) hinzufügen:

```text
Dies ist das "ekem1"-Nachrichtenmuster:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Ende des "ekem1"-Nachrichtenmusters.

```


KDF für Nachricht 3 (nur für XK)
`````````````````````````````````
unverändert


KDF für split()
```````````````
unverändert



### Ratchet

Aktualisieren Sie die ECIES-Ratchet-Spezifikation [ECIES](https://geti2p.net/spec/ecies) wie folgt:


Noise-Identifikatoren
```````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"



1b) Neues Sitzungsformat (mit Bindung)
`````````````````````````````````````

Änderungen: Aktuelle Ratchetn enthält den statischen Schlüssel im ersten ChaCha-Abschnitt,
und die Payload im zweiten Abschnitt. Mit ML-KEM gibt es jetzt drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Öffentlichen Schlüssel. Der zweite Abschnitt enthält den statischen Schlüssel. Der dritte Abschnitt enthält die Payload.


Verschlüsseltes Format:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Neuer Sitzungs-Flüchtiger Öffentlicher Schlüssel    |
  +             32 Bytes                  +
  |     Codiert mit Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 verschlüsselte Daten   |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +    (MAC) für encap_key Abschnitt        +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Statischer Schlüssel           +
  |       ChaCha20 verschlüsselte Daten   |
  +             32 Bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +    (MAC) für Statischer Schlüssel Abschnitt       +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Abschnitt            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +         (MAC) für Payload Abschnitt     +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+


```

Entschlüsseltes Format:

```dataspec
Payload Teil 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Teil 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Statischer Schlüssel               +
  |                                       |
  +      (32 Bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Teil 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Abschnitt            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Größen:

| Typ | Typcode | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
| --- | ------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


Beachten Sie, dass die Payload einen DateTime-Block enthalten muss, sodass die minimale Payload-Größe 7 ist. Die minimalen Nachrichten1-Größen können entsprechend berechnet werden.



1g) Neues Sitzungs-Antwortformat
````````````````````````````

Änderungen: Aktueller Ratchet hat eine leere Payload für den ersten ChaCha-Abschnitt, und die Payload im zweiten Abschnitt. Mit ML-KEM gibt es jetzt drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Chiffrat. Der zweite Abschnitt hat eine leere Payload. Der dritte Abschnitt enthält die Payload.


Verschlüsseltes Format:

```dataspec
+----+----+----+----+----+----+----+----+
  |       Sitzungs-Tag   8 Bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Flüchtiger Öffentlicher Schlüssel           +
  |                                       |
  +            32 Bytes                   +
  |     Codiert mit Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 verschlüsselter ML-KEM Chiffrat  |
  +      (siehe Tabelle unten für Länge)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +  (MAC) für Chiffrat Abschnitt         +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +  (MAC) für Schlüssel Abschnitt (keine Daten)      +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Abschnitt            +
  |       ChaCha20 verschlüsselte Daten         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Nachrichten-Authentifizierungs-Code |
  +         (MAC) für Payload Abschnitt     +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+


```

Entschlüsseltes Format:

```dataspec
Payload Teil 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM Chiffrat               +
  |                                       |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Teil 2:

  leer

  Payload Teil 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Abschnitt            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Größen:

| Typ | Typcode | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
| --- | ------- | ----- | --------- | ------------- | ------------- | --------- | ------- |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


Beachten Sie, dass Nachrichten 2 normalerweise eine nicht null Payload haben, die Ratchet-Spezifikation [ECIES](https://geti2p.net/spec/ecies) dies jedoch nicht erfordert, sodass die minimale Payload-Größe 0 ist. Die minimalen Nachrichten 2-Größen können entsprechend berechnet werden.



### NTCP2

Aktualisieren Sie die NTCP2-Spezifikation [NTCP2](https://geti2p.net/spec/ntcp2) wie folgt:


Noise-Identifikatoren
``````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


1) Sitzungsanfrage
``````````````````

Änderungen: Aktuelles NTCP2 enthält nur die Optionen im ChaCha-Abschnitt. Mit ML-KEM wird auch der verschlüsselte PQ-öffentliche Schlüssel im ChaCha-Abschnitt enthalten sein.


Roh-Inhalte:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        verschleiert mit RH_B           +
  |       AES-CBC-256-verschlüsselter X         |
  +             (32 Bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly-Rahmen (MLKEM)            |
  +      (siehe Tabelle unten für Länge)     +
  |   k definiert in KDF für Nachricht 1      |
  +   n = 0                               +
  |   siehe KDF für zugeordnete Daten         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly-Rahmen (Optionen)          |
  +         32 Bytes                      +
  |   k definiert in KDF für Nachricht 1      |
  +   n = 0                               +
  |   siehe KDF für zugeordnete Daten         |
  +----+----+----+----+----+----+----+----+
  |     unverschlüsselte authentifizierte         |
  ~         Padding (optional)            ~
  |     Länge definiert im Optionsblock   |
  +----+----+----+----+----+----+----+----+

  Wie zuvor, außer dass ein zweiter ChaChaPoly-Rahmen hinzugefügt wird


```

Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht dargestellt):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               Optionen                 |
  +              (16 Bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unverschlüsselte authentifizierte         |
  +         Padding (optional)            +
  |     Länge definiert im Optionsblock   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+



```

Größen:

| Typ | Typcode | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
| --- | ------- | ----- | --------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.


2) Sitzung erstellt
``````````````````

Änderungen: Aktuelles NTCP2 enthält nur die Optionen im ChaCha-Abschnitt. Mit ML-KEM wird auch der verschlüsselte PQ-öffentliche Schlüssel im ChaCha-Abschnitt enthalten sein.


Roh-Inhalte:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        verschleiert mit RH_B           +
  |       AES-CBC-256-verschlüsselter Y         |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly-Rahmen (MLKEM)            |
  +   Verschlüsselte und authentifizierte Daten    +
  -      (siehe Tabelle unten für Länge)     -
  +   k definiert in KDF für Nachricht 2      +
  |   n = 0; siehe KDF für zugeordnete Daten  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly-Rahmen (Optionen)          |
  +   Verschlüsselte und authentifizierte Daten    +
  -           32 Bytes                    -
  +   k definiert in KDF für Nachricht 2      +
  |   n = 0; siehe KDF für zugeordnete Daten  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unverschlüsselte authentifizierte         |
  +         Padding (optional)            +
  |     Länge definiert im Optionsblock   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Wie zuvor, außer dass ein zweiter ChaChaPoly-Rahmen hinzugefügt wird

```

Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht dargestellt):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Chiffrat           |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               Optionen                 |
  +              (16 Bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unverschlüsselte authentifizierte         |
  +         Padding (optional)            +
  |     Länge definiert im Optionsblock   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Größen:

| Typ | Typcode | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
| --- | ------- | ----- | --------- | ------------- | ------------- | --------- | ------- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.



3) Bestätigte Sitzung
```````````````````

Unverändert


Schlüsselableitungsfunktion (KDF) (für Datenphase)
``````````````````````````````````````````````

Unverändert




### SSU2

Aktualisieren Sie die SSU2-Spezifikation [SSU2](https://geti2p.net/spec/ssu2) wie folgt:


Noise-Identifikatoren
``````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


Langer Header
`````````````
Der lange Header ist 32 Bytes. Er wird vor der Erstellung einer Sitzung verwendet, für Token Request, SessionRequest, SessionCreated und Retry. Er wird auch für Peer Test- und Hole Punch-Nachrichten außerhalb einer Sitzung verwendet.

TODO: Wir könnten das Versionsfeld intern verwenden und 3 für MLKEM512 und 4 für MLKEM768 verwenden. Machen wir das nur für Typen 0 und 1 oder für alle 6 Typen?


Vor der Header-Verschlüsselung:

```dataspec

+----+----+----+----+----+----+----+----+
  |      Zielverbindungskennung        |
  +----+----+----+----+----+----+----+----+
  |   Paketnummer   |Typ| Ver| ID |Flag|
  +----+----+----+----+----+----+----+----+
  |        Quellverbindungskennung         |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Zielverbindungskennung :: 8 Bytes, unsignierte big endian integer

  Paketnummer :: 4 Bytes, unsignierte big endian integer

  Typ :: Der Nachrichtentyp = 0, 1, 7, 9, 10, oder 11

  Ver :: Die Protokollversion, gleich 2
         TODO Wir könnten das Versionsfeld intern verwenden und 3 für MLKEM512 und 4 für MLKEM768 verwenden.

  ID :: 1 Byte, die Netzwerk-ID (derzeit 2, außer in Testnetzwerken)

  Flag :: 1 Byte, ungenutzt, auf 0 für zukünftige Kompatibilität einstellen

  Quellverbindungskennung :: 8 Bytes, unsignierte big endian integer

  Token :: 8 Bytes, unsignierte big endian integer

```


Kurzer Header
`````````````
Unverändert


Sitzungsanfrage (Typ 0)
```````````````````````

Änderungen: SSU2 enthält aktuell nur die Blockdaten im ChaCha-Abschnitt.
Mit ML-KEM enthält der ChaCha-Abschnitt auch den verschlüsselten PQ-öffentlichen Schlüssel.


Roh-Inhalte:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Lange Header-Bytes 0-15, ChaCha20     |
  +  verschlüsselt mit Bob intro key         +
  |    Siehe Header-Verschlüsselungs-KDF          |
  +----+----+----+----+----+----+----+----+
  |  Lange Header-Bytes 16-31, ChaCha20    |
  +  verschlüsselt mit Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 verschlüsselt           +
  |       mit Bob intro key n=0          |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 verschlüsselte Daten (MLKEM)     |
  +          (Länge variiert)              +
  |  k definiert in KDF für Sitzungsanfrage |
  +  n = 0                                +
  |  siehe KDF für zugeordnete Daten          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 verschlüsselte Daten (Payload)   |
  +          (Länge variiert)              +
  |  k definiert in KDF für Sitzungsanfrage |
  +  n = 0                                +
  |  siehe KDF für zugeordnete Daten          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 Bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht dargestellt):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Zielverbindungskennung        |
  +----+----+----+----+----+----+----+----+
  |   Paketnummer   |Typ| Ver| ID |Flag|
  +----+----+----+----+----+----+----+----+
  |        Quellverbindungskennung         |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise-Payload (Blockdaten)        |
  +          (Länge variiert)              +
  |     siehe unten für erlaubte Blöcke      |
  +----+----+----+----+----+----+----+----+


```

Größen, ohne IP-Overhead:

| Typ | Typcode | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
| --- | ------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | zu groß |  |  |  |  |


Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4,
und die Unterstützung wird in den Router-Adressen angegeben.

Minimale MTU für MLKEM768_X25519: Etwa 1316 für IPv4 und 1336 für IPv6.



Sitzung erstellt (Typ 1)
````````````````````````
Änderungen: SSU2 enthält aktuell nur die Blockdaten im ChaCha-Abschnitt.
Mit ML-KEM wird auch der verschlüsselte PQ-öffentliche Schlüssel im ChaCha-Abschnitt enthalten sein.


Roh-Inhalte:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Lange Header-Bytes 0-15, ChaCha20     |
  +  verschlüsselt mit Bob intro key und     +
  | abgeleitetem Schlüssel, siehe Header-Verschlüsselungs-KDF|
  +----+----+----+----+----+----+----+----+
  |  Lange Header-Bytes 16-31, ChaCha20    |
  +  verschlüsselt mit abgeleitetem Schlüssel n=0       +
  |  Siehe Header-Verschlüsselungs-KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 verschlüsselt           +
  |       mit abgeleitetem Schlüssel n=0            |
  +              (32 Bytes)               +
  |       Siehe Header-Verschlüsselungs-KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 Daten (MLKEM)               |
  +   Verschlüsselte und authentifizierte Daten    +
  |  länge variiert                        |
  +  k definiert in KDF für Sitzung erstellt +
  |  n = 0; siehe KDF für zugeordnete Daten   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 Daten (Payload)             |
  +   Verschlüsselte und authentifizierte Daten    +
  |  länge variiert                        |
  +  k definiert in KDF für Sitzung erstellt +
  |  n = 0; siehe KDF für zugeordnete Daten   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 Bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht dargestellt):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Zielverbindungskennung        |
  +----+----+----+----+----+----+----+----+
  |   Paketnummer   |Typ| Ver| ID |Flag|
  +----+----+----+----+----+----+----+----+
  |        Quellverbindungskennung         |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 Bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Chiffrat           |
  +      (siehe Tabelle unten für Länge)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise-Payload (Blockdaten)        |
  +          (Länge variiert)              +
  |      siehe unten für erlaubte Blöcke     |
  +----+----+----+----+----+----+----+----+

```

Größen, ohne IP-Overhead:

| Typ | Typcode | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
| --- | ------- | ----- | --------- | ------------- | ------------- | --------- | ------ |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | zu groß |  |  |  |  |


Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4,
und die Unterstützung wird in den Router-Adressen angegeben.

Minimale MTU für MLKEM768_X25519: Etwa 1316 für IPv4 und 1336 für IPv6.


Bestätigte Sitzung (Typ 2)
`````````````````````````
Unverändert



KDF für Datenphase
```````````````````
Unverändert



Relay und Peer Test
```````````````````

Relay-Blöcke, Peer-Test-Blöcke und Peer-Test-Nachrichten enthalten alle Signaturen. Leider sind PQ-Signaturen größer als die MTU. Es gibt keinen aktuellen Mechanismus, um Relay- oder Peer-Test-Blöcke oder Nachrichten über mehrere UDP-Pakete hinweg zu fragmentieren. Das Protokoll muss erweitert werden, um Fragmentierung zu unterstützen. Dies wird in einem separaten Vorschlag TBD geschehen. Bis dies abgeschlossen ist, wird Relay und Peer Test nicht unterstützt.


Probleme
``````

Wir könnten das Versionsfeld intern verwenden und 3 für MLKEM512 und 4 für
