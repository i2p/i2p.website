---
title: "Post-Quantum-Krypto-Protokolle"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Öffnen"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Übersicht

Während Forschung und Wettbewerb für geeignete Post-Quantum (PQ) Kryptographie seit einem Jahrzehnt voranschreiten, sind die Wahlmöglichkeiten erst kürzlich klar geworden.

Wir haben 2022 damit begonnen, die Auswirkungen von PQ-Kryptografie zu untersuchen [zzz.i2p](http://zzz.i2p/topics/3294).

TLS-Standards haben in den letzten zwei Jahren Unterstützung für hybride Verschlüsselung hinzugefügt und diese wird nun für einen erheblichen Anteil des verschlüsselten Traffics im Internet verwendet, da Chrome und Firefox sie unterstützen [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST hat kürzlich die empfohlenen Algorithmen für Post-Quantum-Kryptographie finalisiert und veröffentlicht [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Mehrere gängige Kryptographie-Bibliotheken unterstützen nun die NIST-Standards oder werden in naher Zukunft Unterstützung dafür bereitstellen.

Sowohl [Cloudflare](https://blog.cloudflare.com/pq-2024/) als auch [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) empfehlen, dass die Migration sofort beginnen sollte. Siehe auch die NSA PQ FAQ von 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P sollte führend in Sicherheit und Kryptographie sein. Jetzt ist der richtige Zeitpunkt, die empfohlenen Algorithmen zu implementieren. Mit unserem flexiblen Crypto-Type- und Signature-Type-System werden wir Typen für Hybrid-Crypto sowie für PQ- und Hybrid-Signaturen hinzufügen.

## Ziele

- Wählen Sie PQ-resistente Algorithmen aus
- Fügen Sie reine PQ- und Hybrid-Algorithmen zu I2P-Protokollen hinzu, wo angemessen
- Definieren Sie mehrere Varianten
- Wählen Sie die besten Varianten nach Implementierung, Tests, Analyse und Forschung aus
- Fügen Sie Unterstützung schrittweise und mit Rückwärtskompatibilität hinzu

## Nicht-Ziele

- Ändern Sie keine Einweg-Verschlüsselungsprotokolle (Noise N)
- Wechseln Sie nicht weg von SHA256, kurzfristig nicht durch PQ bedroht
- Wählen Sie die finalen bevorzugten Varianten zu diesem Zeitpunkt nicht aus

## Bedrohungsmodell

- Router am OBEP oder IBGW, möglicherweise in Absprache,
  speichern garlic-Nachrichten für spätere Entschlüsselung (Forward Secrecy)
- Netzwerkbeobachter
  speichern Transportnachrichten für spätere Entschlüsselung (Forward Secrecy)
- Netzwerkteilnehmer fälschen Signaturen für RI, LS, Streaming, Datagramme,
  oder andere Strukturen

## Betroffene Protokolle

Wir werden die folgenden Protokolle modifizieren, ungefähr in der Reihenfolge der Entwicklung. Die gesamte Einführung wird wahrscheinlich von Ende 2025 bis Mitte 2027 dauern. Siehe den Abschnitt Prioritäten und Einführung unten für Details.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Design

Wir werden die NIST FIPS 203 und 204 Standards [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) unterstützen, die auf CRYSTALS-Kyber und CRYSTALS-Dilithium (Versionen 3.1, 3 und älter) basieren, aber NICHT kompatibel mit diesen sind.

### Key Exchange

Wir werden hybriden Schlüsselaustausch in den folgenden Protokollen unterstützen:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM bietet nur ephemere Schlüssel und unterstützt nicht direkt statische Schlüssel-Handshakes wie Noise XK und IK.

Noise N verwendet keinen bidirektionalen Schlüsselaustausch und ist daher nicht für hybride Verschlüsselung geeignet.

Daher werden wir nur Hybrid-Verschlüsselung unterstützen, für NTCP2, SSU2 und Ratchet. Wir werden die drei ML-KEM-Varianten wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert verwenden, für insgesamt 3 neue Verschlüsselungstypen. Hybrid-Typen werden nur in Kombination mit X25519 definiert.

Die neuen Verschlüsselungstypen sind:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Der Overhead wird erheblich sein. Typische Nachrichten-Größen 1 und 2 (für XK und IK) liegen derzeit bei etwa 100 Bytes (vor jeder zusätzlichen Payload). Dies wird sich je nach Algorithmus um das 8- bis 15-fache erhöhen.

### Signatures

Wir werden PQ- und Hybrid-Signaturen in den folgenden Strukturen unterstützen:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Wir werden daher sowohl PQ-only als auch hybride Signaturen unterstützen. Wir werden die drei ML-DSA-Varianten wie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definieren, drei hybride Varianten mit Ed25519 und drei PQ-only-Varianten mit Prehash nur für SU3-Dateien, insgesamt also 9 neue Signaturtypen. Hybride Typen werden nur in Kombination mit Ed25519 definiert. Wir werden das Standard-ML-DSA verwenden, NICHT die Pre-Hash-Varianten (HashML-DSA), außer für SU3-Dateien.

Wir werden die "hedged" oder randomisierte Signatur-Variante verwenden, nicht die "deterministische" Variante, wie sie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Abschnitt 3.4 definiert ist. Dies stellt sicher, dass jede Signatur unterschiedlich ist, auch bei denselben Daten, und bietet zusätzlichen Schutz gegen Seitenkanalangriffe. Siehe den Implementierungshinweise-Abschnitt unten für weitere Details zu Algorithmus-Entscheidungen einschließlich Kodierung und Kontext.

Die neuen Signaturtypen sind:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
X.509-Zertifikate und andere DER-Kodierungen werden die zusammengesetzten Strukturen und OIDs verwenden, die in [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) definiert sind.

Der Overhead wird erheblich sein. Typische Ed25519-Destination- und Router-Identitätsgrößen betragen 391 Bytes. Diese werden je nach Algorithmus um das 3,5- bis 6,8-fache ansteigen. Ed25519-Signaturen sind 64 Bytes groß. Diese werden je nach Algorithmus um das 38- bis 76-fache ansteigen. Typische signierte RouterInfo, leaseSet, beantwortbare Datagramme und signierte Streaming-Nachrichten sind etwa 1KB groß. Diese werden je nach Algorithmus um das 3- bis 8-fache ansteigen.

Da die neuen Destination- und Router-Identity-Typen keine Padding enthalten werden, sind sie nicht komprimierbar. Die Größen von Destinations und Router-Identitys, die während der Übertragung mit gzip komprimiert werden, werden je nach Algorithmus um das 12- bis 38-fache zunehmen.

### Legal Combinations

Für Destinations werden die neuen Signaturtypen mit allen Verschlüsselungstypen im leaseSet unterstützt. Setzen Sie den Verschlüsselungstyp im Schlüsselzertifikat auf NONE (255).

Für RouterIdentities ist der ElGamal-Verschlüsselungstyp veraltet. Die neuen Signaturtypen werden nur mit X25519 (Typ 4) Verschlüsselung unterstützt. Die neuen Verschlüsselungstypen werden in den RouterAddresses angegeben. Der Verschlüsselungstyp im Schlüsselzertifikat wird weiterhin Typ 4 sein.

### New Crypto Required

- ML-KEM (früher CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (früher CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (früher Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Wird nur für SHAKE128 verwendet
- SHA3-256 (früher Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 und SHAKE256 (XOF-Erweiterungen zu SHA3-128 und SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Testvektoren für SHA3-256, SHAKE128 und SHAKE256 finden sich unter [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Beachten Sie, dass die Java bouncycastle-Bibliothek alle oben genannten Funktionen unterstützt. C++-Bibliotheksunterstützung ist in OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/) verfügbar.

### Alternatives

Wir werden [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+) nicht unterstützen, es ist viel viel langsamer und größer als ML-DSA. Wir werden das kommende FIPS206 (Falcon) nicht unterstützen, es ist noch nicht standardisiert. Wir werden NTRU oder andere PQ-Kandidaten, die nicht von NIST standardisiert wurden, nicht unterstützen.

### Rosenpass

Es gibt einige Forschung [paper](https://eprint.iacr.org/2020/379.pdf) zur Anpassung von Wireguard (IK) für reine PQ-Kryptographie, aber es gibt mehrere offene Fragen in diesem Paper. Später wurde dieser Ansatz als Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) für PQ Wireguard implementiert.

Rosenpass verwendet einen Noise KK-ähnlichen Handshake mit vorgeteilten Classic McEliece 460896 statischen Schlüsseln (je 500 KB) und Kyber-512 (im Wesentlichen MLKEM-512) ephemeren Schlüsseln. Da die Classic McEliece Chiffretexte nur 188 Bytes groß sind und die Kyber-512 öffentlichen Schlüssel und Chiffretexte angemessen sind, passen beide Handshake-Nachrichten in eine Standard-UDP-MTU. Der ausgegebene geteilte Schlüssel (osk) aus dem PQ KK Handshake wird als eingegebener vorgeteilter Schlüssel (psk) für den Standard-Wireguard IK Handshake verwendet. Es gibt also insgesamt zwei vollständige Handshakes, einen rein PQ und einen rein X25519.

Wir können nichts davon tun, um unsere XK- und IK-Handshakes zu ersetzen, weil:

- Wir können KK nicht durchführen, Bob hat nicht Alices statischen Schlüssel
- 500KB statische Schlüssel sind viel zu groß
- Wir wollen keine zusätzliche Roundtrip-Zeit

Es gibt viele gute Informationen in dem Whitepaper, und wir werden es auf Ideen und Inspiration hin überprüfen. TODO.

## Specification

### Schlüsselaustausch

Aktualisieren Sie die Abschnitte und Tabellen im Dokument für gemeinsame Strukturen [/docs/specs/common-structures/](/docs/specs/common-structures/) wie folgt:

### Signaturen

Die neuen Public Key-Typen sind:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Hybrid-Public-Keys sind der X25519-Schlüssel. KEM-Public-Keys sind der ephemere PQ-Schlüssel, der von Alice an Bob gesendet wird. Kodierung und Byte-Reihenfolge sind definiert in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

MLKEM*_CT-Schlüssel sind nicht wirklich öffentliche Schlüssel, sondern der "Chiffretext", der von Bob an Alice im Noise-Handshake gesendet wird. Sie sind hier der Vollständigkeit halber aufgeführt.

### Zulässige Kombinationen

Die neuen Private Key-Typen sind:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Hybrid private keys sind die X25519-Schlüssel. KEM private keys sind nur für Alice. KEM-Kodierung und Byte-Reihenfolge sind definiert in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Neue Kryptographie erforderlich

Die neuen Signing Public Key-Typen sind:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Hybride öffentliche Signaturschlüssel sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie in [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kodierung und Byte-Reihenfolge sind definiert in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Alternativen

Die neuen Signing Private Key-Typen sind:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hybride Signatur-Private-Schlüssel sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie in [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kodierung und Byte-Reihenfolge sind definiert in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Die neuen Signature-Typen sind:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hybride Signaturen sind die Ed25519-Signatur gefolgt von der PQ-Signatur, wie in [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Hybride Signaturen werden verifiziert, indem beide Signaturen überprüft werden und fehlschlagen, wenn eine der beiden fehlschlägt. Kodierung und Byte-Reihenfolge sind definiert in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Die neuen Signing Public Key-Typen sind:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Die neuen Crypto Public Key-Typen sind:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Hybride Schlüsseltypen sind NIEMALS in Schlüsselzertifikaten enthalten; nur in leaseSets.

Für Destinations mit Hybrid- oder PQ-Signaturtypen verwenden Sie NONE (Typ 255) für den Verschlüsselungstyp, aber es gibt keinen Krypto-Schlüssel, und der gesamte 384-Byte-Hauptbereich ist für den Signaturschlüssel bestimmt.

### Gemeinsame Strukturen

Hier sind die Längen für die neuen Destination-Typen. Der Enc-Typ für alle ist NONE (Typ 255) und die Verschlüsselungsschlüssellänge wird als 0 behandelt. Der gesamte 384-Byte-Abschnitt wird für den ersten Teil des öffentlichen Signaturschlüssels verwendet. HINWEIS: Dies unterscheidet sich von der Spezifikation für die ECDSA_SHA512_P521- und RSA-Signaturtypen, wo wir den 256-Byte-ElGamal-Schlüssel in der Destination beibehalten haben, obwohl er nicht verwendet wurde.

Kein Padding. Gesamtlänge beträgt 7 + Gesamtschlüssellänge. Key certificate-Länge beträgt 4 + überschüssige Schlüssellänge.

Beispiel 1319-Byte Destination-Byte-Stream für MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Hier sind die Längen für die neuen Destination-Typen. Enc-Typ für alle ist X25519 (Typ 4). Der gesamte 352-Byte-Abschnitt nach dem X25519 öffentlichen Schlüssel wird für den ersten Teil des öffentlichen Signaturschlüssels verwendet. Kein Padding. Gesamtlänge ist 39 + Gesamtschlüssellänge. Key Certificate-Länge ist 4 + überschüssige Schlüssellänge.

Beispiel eines 1351-Byte router identity Byte-Streams für MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

Handshakes verwenden [Noise Protocol](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload
- e1 = einmaliger ephemerer PQ-Schlüssel, von Alice an Bob gesendet
- ekem1 = der KEM-Chiffretext, von Bob an Alice gesendet

Die folgenden Modifikationen an XK und IK für hybride Forward Secrecy (hfs) sind wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 5 spezifiziert:

```
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

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Das e1-Muster ist wie folgt definiert, wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 spezifiziert:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Das ekem1-Muster ist wie folgt definiert, wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 spezifiziert:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- Sollten wir die Handshake-Hash-Funktion ändern? Siehe [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 ist nicht anfällig für PQ, aber wenn wir unsere
  Hash-Funktion upgraden möchten, ist jetzt der richtige Zeitpunkt, während wir andere Dinge ändern.
  Der aktuelle IETF SSH-Vorschlag [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) sieht vor, MLKEM768
  mit SHA256 und MLKEM1024 mit SHA384 zu verwenden. Dieser Vorschlag enthält
  eine Diskussion der Sicherheitsüberlegungen.
- Sollten wir aufhören, 0-RTT-Ratchet-Daten zu senden (außer dem LS)?
- Sollten wir den Ratchet von IK auf XK umstellen, wenn wir keine 0-RTT-Daten senden?

#### Overview

Dieser Abschnitt gilt sowohl für IK- als auch für XK-Protokolle.

Der Hybrid-Handshake ist definiert in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Die erste Nachricht, von Alice an Bob, enthält e1, den Kapselungsschlüssel, vor der Nachrichten-Nutzlast. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufe EncryptAndHash() darauf auf (als Alice) oder DecryptAndHash() (als Bob). Verarbeite dann die Nachrichten-Nutzlast wie üblich.

Die zweite Nachricht, von Bob an Alice, enthält ekem1, den Chiffretext, vor der Nachrichtennutzlast. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie EncryptAndHash() darauf auf (als Bob) oder DecryptAndHash() (als Alice). Berechnen Sie dann den kem_shared_key und rufen Sie MixKey(kem_shared_key) auf. Verarbeiten Sie dann die Nachrichtennutzlast wie gewohnt.

#### Defined ML-KEM Operations

Wir definieren die folgenden Funktionen entsprechend den kryptographischen Bausteinen, die wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert verwendet werden.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Beachten Sie, dass sowohl der encap_key als auch der ciphertext innerhalb von ChaCha/Poly-Blöcken in den Noise-Handshake-Nachrichten 1 und 2 verschlüsselt sind. Sie werden als Teil des Handshake-Prozesses entschlüsselt.

Der kem_shared_key wird mit MixHash() in den chaining key eingemischt. Siehe unten für Details.

#### Alice KDF for Message 1

Für XK: Nach dem 'es' Nachrichtenmuster und vor der Nutzlast hinzufügen:

ODER

Für IK: Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster, hinzufügen:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

Für XK: Nach dem 'es' Nachrichtenmuster und vor der Payload, hinzufügen:

ODER

Für IK: Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster, hinzufügen:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

Für XK: Nach dem 'ee' Nachrichtenmuster und vor der Nutzlast, hinzufügen:

ODER

Für IK: Nach dem 'ee' Nachrichtenmuster und vor dem 'se' Nachrichtenmuster, hinzufügen:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

Nach dem 'ee' Nachrichtenmuster (und vor dem 'ss' Nachrichtenmuster für IK), hinzufügen:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
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

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

unverändert

#### KDF for split()

unverändert

### SigningPrivateKey

Aktualisiere die ECIES-Ratchet-Spezifikation [/docs/specs/ecies/](/docs/specs/ecies/) wie folgt:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Änderungen: Das aktuelle Ratchet enthielt den statischen Schlüssel im ersten ChaCha-Abschnitt und die Payload im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Public-Key. Der zweite Abschnitt enthält den statischen Schlüssel. Der dritte Abschnitt enthält die Payload.

Verschlüsseltes Format:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Entschlüsseltes Format:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Größen:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Beachten Sie, dass die Payload einen DateTime-Block enthalten muss, daher beträgt die minimale Payload-Größe 7. Die minimalen Nachricht-1-Größen können entsprechend berechnet werden.

#### 1g) New Session Reply format

Änderungen: Der aktuelle ratchet hat eine leere Nutzlast für den ersten ChaCha-Abschnitt und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Chiffretext. Der zweite Abschnitt hat eine leere Nutzlast. Der dritte Abschnitt enthält die Nutzlast.

Verschlüsseltes Format:

```
+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Entschlüsseltes Format:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Größen:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Beachten Sie, dass Nachricht 2 normalerweise eine Nutzlast ungleich null haben wird, die ratchet-Spezifikation [/docs/specs/ecies/](/docs/specs/ecies/) erfordert dies jedoch nicht, sodass die minimale Nutzlastgröße 0 ist. Die minimalen Größen für Nachricht 2 können entsprechend berechnet werden.

### Signatur

Aktualisieren Sie die NTCP2-Spezifikation [/docs/specs/ntcp2/](/docs/specs/ntcp2/) wie folgt:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Änderungen: Das aktuelle NTCP2 enthält nur die Optionen im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

Rohe Inhalte:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht gezeigt):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Größen:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Hinweis: Typencodes sind nur für interne Verwendung bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angezeigt.

#### 2) SessionCreated

Änderungen: Das aktuelle NTCP2 enthält nur die Optionen im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

Roher Inhalt:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Unverschlüsselte Daten (Poly1305 Auth-Tag nicht angezeigt):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Größen:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

#### 3) SessionConfirmed

Unverändert

#### Key Derivation Function (KDF) (for data phase)

Unverändert

### Schlüsselzertifikate

Aktualisieren Sie die SSU2-Spezifikation [/docs/specs/ssu2/](/docs/specs/ssu2/) wie folgt:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

Der lange Header ist 32 Bytes groß. Er wird vor der Erstellung einer Session verwendet, für Token Request, SessionRequest, SessionCreated und Retry. Er wird auch für sessionlose Peer Test und Hole Punch Nachrichten verwendet.

TODO: Wir könnten intern das Versionsfeld verwenden und 3 für MLKEM512 und 4 für MLKEM768 nutzen. Machen wir das nur für die Typen 0 und 1 oder für alle 6 Typen?

Vor der Header-Verschlüsselung:

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

unverändert

#### SessionRequest (Type 0)

Änderungen: Das aktuelle SSU2 enthält nur die Blockdaten im ChaCha-Bereich. Mit ML-KEM wird der ChaCha-Bereich auch den verschlüsselten PQ-Public-Key enthalten.

Rohe Inhalte:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht angezeigt):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Größen, ohne IP-Overhead:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Hinweis: Type-Codes sind nur für die interne Verwendung bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angezeigt.

Minimale MTU für MLKEM768_X25519: Etwa 1316 für IPv4 und 1336 für IPv6.

#### SessionCreated (Type 1)

Änderungen: Das aktuelle SSU2 enthält nur die Blockdaten im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

Rohe Inhalte:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Unverschlüsselte Daten (Poly1305 Auth-Tag nicht gezeigt):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Größen, ohne IP-Overhead:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

Mindest-MTU für MLKEM768_X25519: Etwa 1316 für IPv4 und 1336 für IPv6.

#### SessionConfirmed (Type 2)

unverändert

#### KDF for data phase

unverändert

#### Probleme

Relay-Blöcke, Peer Test-Blöcke und Peer Test-Nachrichten enthalten alle Signaturen. Leider sind PQ-Signaturen größer als die MTU. Es gibt derzeit keinen Mechanismus, um Relay- oder Peer Test-Blöcke oder -Nachrichten über mehrere UDP-Pakete zu fragmentieren. Das Protokoll muss erweitert werden, um Fragmentierung zu unterstützen. Dies wird in einem separaten, noch zu bestimmenden Vorschlag erfolgen. Bis dies abgeschlossen ist, werden Relay und Peer Test nicht unterstützt.

#### Überblick

Wir könnten intern das Versionsfeld verwenden und 3 für MLKEM512 und 4 für MLKEM768 nutzen.

Für Nachrichten 1 und 2 würde MLKEM768 die Paketgrößen über die minimale MTU von 1280 hinaus erhöhen. Wahrscheinlich würde es einfach nicht für diese Verbindung unterstützt werden, wenn die MTU zu niedrig wäre.

Für Nachrichten 1 und 2 würde MLKEM1024 die Paketgrößen über die maximale MTU von 1500 hinaus vergrößern. Dies würde eine Fragmentierung der Nachrichten 1 und 2 erfordern und wäre eine große Komplikation. Wahrscheinlich werden wir das nicht umsetzen.

Relay und Peer Test: Siehe oben

### Zielgrößen

TODO: Gibt es einen effizienteren Weg, Signierung/Verifikation zu definieren, um das Kopieren der Signatur zu vermeiden?

### RouterIdent-Größen

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) Abschnitt 8.1 verbietet HashML-DSA in X.509-Zertifikaten und weist keine OIDs für HashML-DSA zu, aufgrund von Implementierungskomplexitäten und reduzierter Sicherheit.

Für PQ-only-Signaturen von SU3-Dateien verwenden Sie die in [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) definierten OIDs der non-prehash-Varianten für die Zertifikate. Wir definieren keine hybriden Signaturen von SU3-Dateien, da wir die Dateien möglicherweise zweimal hashen müssten (obwohl HashML-DSA und X2559 dieselbe Hash-Funktion SHA512 verwenden). Außerdem wäre das Verketten von zwei Schlüsseln und Signaturen in einem X.509-Zertifikat völlig nonstandard.

Beachten Sie, dass wir Ed25519-Signierung von SU3-Dateien nicht zulassen, und obwohl wir Ed25519ph-Signierung definiert haben, haben wir uns nie auf eine OID dafür geeinigt oder sie verwendet.

Die normalen sig-Typen sind für SU3-Dateien nicht zulässig; verwenden Sie die ph (prehash) Varianten.

### Handshake-Muster

Die neue maximale Destination-Größe wird 2599 sein (3468 in Base 64).

Aktualisieren Sie andere Dokumente, die Anleitungen zu Destination-Größen geben, einschließlich:

- SAMv3
- Bittorrent
- Entwicklerrichtlinien
- Benennung / Adressbuch / Jump-Server
- Andere Dokumentationen

## Overhead Analysis

### Noise Handshake KDF

Größenzunahme (Bytes):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Geschwindigkeit:

Geschwindigkeiten laut [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Vorläufige Testergebnisse in Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Größe:

Typische Schlüssel-, Sig-, RIdent-, Dest-Größen oder Größenzunahmen (Ed25519 als Referenz enthalten), unter der Annahme des X25519-Verschlüsselungstyps für RIs. Zusätzliche Größe für eine Router Info, LeaseSet, antwortfähige Datagramme und jedes der beiden Streaming-Pakete (SYN und SYN ACK) aufgeführt. Aktuelle Destinations und Leasesets enthalten wiederholte Polsterung und sind während der Übertragung komprimierbar. Neue Typen enthalten keine Polsterung und werden nicht komprimierbar sein, was zu einer viel höheren Größenzunahme während der Übertragung führt. Siehe Designabschnitt oben.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Geschwindigkeit:

Geschwindigkeiten wie berichtet von [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Vorläufige Testergebnisse in Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

NIST-Sicherheitskategorien sind zusammengefasst in [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) Folie 10. Vorläufige Kriterien: Unsere minimale NIST-Sicherheitskategorie sollte 2 für Hybridprotokolle und 3 für reine PQ-Protokolle sein.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Das sind alles hybride Protokolle. Wahrscheinlich sollte MLKEM768 bevorzugt werden; MLKEM512 ist nicht sicher genug.

NIST-Sicherheitskategorien [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Dieser Vorschlag definiert sowohl hybride als auch reine PQ-Signaturtypen. MLDSA44 hybrid ist MLDSA65 PQ-only vorzuziehen. Die Schlüssel- und Signaturgrößen für MLDSA65 und MLDSA87 sind wahrscheinlich zu groß für uns, zumindest anfangs.

NIST-Sicherheitskategorien [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Während wir 3 Krypto- und 9 Signaturtypen definieren und implementieren werden, planen wir, die Leistung während der Entwicklung zu messen und die Auswirkungen vergrößerter Strukturgrößen weiter zu analysieren. Wir werden auch weiterhin Entwicklungen in anderen Projekten und Protokollen erforschen und überwachen.

Nach einem Jahr oder mehr Entwicklungszeit werden wir versuchen, uns auf einen bevorzugten Typ oder Standard für jeden Anwendungsfall festzulegen. Die Auswahl wird Kompromisse zwischen Bandbreite, CPU-Leistung und geschätztem Sicherheitsniveau erfordern. Möglicherweise sind nicht alle Typen für alle Anwendungsfälle geeignet oder zugelassen.

Die vorläufigen Einstellungen sind wie folgt, vorbehaltlich Änderungen:

Verschlüsselung: MLKEM768_X25519

Signaturen: MLDSA44_EdDSA_SHA512_Ed25519

Die vorläufigen Einschränkungen sind wie folgt, änderungen vorbehalten:

Verschlüsselung: MLKEM1024_X25519 nicht erlaubt für SSU2

Signaturen: MLDSA87 und Hybrid-Variante wahrscheinlich zu groß; MLDSA65 und Hybrid-Variante möglicherweise zu groß

## Implementation Notes

### Library Support

Die Bouncycastle-, BoringSSL- und WolfSSL-Bibliotheken unterstützen jetzt MLKEM und MLDSA. OpenSSL-Unterstützung wird in ihrer Version 3.5 am 8. April 2025 verfügbar sein [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Die von Java I2P adaptierte southernstorm.com Noise-Bibliothek enthielt vorläufige Unterstützung für Hybrid-Handshakes, aber wir haben sie als ungenutzt entfernt; wir werden sie wieder hinzufügen und aktualisieren müssen, um [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) zu entsprechen.

### Signing Variants

Wir werden die "hedged" oder randomisierte Signaturvariante verwenden, nicht die "deterministische" Variante, wie sie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Abschnitt 3.4 definiert ist. Dies stellt sicher, dass jede Signatur unterschiedlich ist, auch wenn sie über dieselben Daten erfolgt, und bietet zusätzlichen Schutz vor Seitenkanalangriffen. Obwohl [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) spezifiziert, dass die "hedged" Variante der Standard ist, mag dies in verschiedenen Bibliotheken der Fall sein oder auch nicht. Implementierer müssen sicherstellen, dass die "hedged" Variante für die Signierung verwendet wird.

Wir verwenden den normalen Signierungsprozess (genannt Pure ML-DSA Signature Generation), der die Nachricht intern als 0x00 || len(ctx) || ctx || message kodiert, wobei ctx ein optionaler Wert der Größe 0x00..0xFF ist. Wir verwenden keinen optionalen Kontext. len(ctx) == 0. Dieser Prozess ist definiert in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithmus 2 Schritt 10 und Algorithmus 3 Schritt 5. Beachten Sie, dass einige veröffentlichte Testvektoren möglicherweise das Setzen eines Modus erfordern, bei dem die Nachricht nicht kodiert wird.

### Reliability

Eine Größenerhöhung führt zu deutlich mehr Tunnel-Fragmentierung bei NetDB-Speicherungen, Streaming-Handshakes und anderen Nachrichten. Überprüfen Sie auf Leistungs- und Zuverlässigkeitsänderungen.

### Structure Sizes

Finden und überprüfen Sie jeglichen Code, der die Bytegröße von Router-Infos und LeaseSets begrenzt.

### NetDB

Überprüfen und möglicherweise die maximale Anzahl der in RAM oder auf der Festplatte gespeicherten LS/RI reduzieren, um den Speicherzuwachs zu begrenzen. Mindest-Bandbreitenanforderungen für floodfills erhöhen?

### Ratchet

#### Definierte ML-KEM-Operationen

Auto-Klassifikation/Erkennung mehrerer Protokolle auf denselben Tunneln sollte basierend auf einer Längenprüfung von Nachricht 1 (New Session Message) möglich sein. Am Beispiel von MLKEM512_X25519 ist Nachricht 1 um 816 Bytes größer als das aktuelle Ratchet-Protokoll, und die minimale Größe von Nachricht 1 (mit nur einer DateTime-Nutzlast) beträgt 919 Bytes. Die meisten Nachricht-1-Größen mit aktuellem Ratchet haben eine Nutzlast von weniger als 816 Bytes, sodass sie als Nicht-Hybrid-Ratchet klassifiziert werden können. Große Nachrichten sind wahrscheinlich POSTs, die selten sind.

Die empfohlene Strategie ist also:

- Wenn Nachricht 1 weniger als 919 Bytes hat, ist es das aktuelle ratchet protocol.
- Wenn Nachricht 1 größer oder gleich 919 Bytes ist, ist es wahrscheinlich MLKEM512_X25519.
  Versuche zuerst MLKEM512_X25519, und falls es fehlschlägt, versuche das aktuelle ratchet protocol.

Dies sollte es uns ermöglichen, standard ratchet und hybrid ratchet effizient auf derselben Destination zu unterstützen, genau wie wir zuvor ElGamal und ratchet auf derselben Destination unterstützt haben. Daher können wir viel schneller zum MLKEM hybrid Protokoll migrieren, als wenn wir keine Dual-Protokolle für dieselbe Destination unterstützen könnten, da wir MLKEM-Unterstützung zu bestehenden Destinations hinzufügen können.

Die erforderlichen unterstützten Kombinationen sind:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Die folgenden Kombinationen können komplex sein und müssen NICHT unterstützt werden, können aber implementierungsabhängig unterstützt werden:

- Mehr als ein MLKEM
- ElG + ein oder mehr MLKEM
- X25519 + ein oder mehr MLKEM
- ElG + X25519 + ein oder mehr MLKEM

Wir versuchen möglicherweise nicht, mehrere MLKEM-Algorithmen (zum Beispiel MLKEM512_X25519 und MLKEM_768_X25519) am selben Ziel zu unterstützen. Wählen Sie nur einen aus; das hängt jedoch davon ab, dass wir eine bevorzugte MLKEM-Variante auswählen, damit HTTP-Client-Tunnel eine verwenden können. Implementierungsabhängig.

Wir KÖNNEN versuchen, drei Algorithmen (zum Beispiel X25519, MLKEM512_X25519 und MLKEM769_X25519) auf derselben Destination zu unterstützen. Die Klassifizierung und Wiederholungsstrategie könnten zu komplex sein. Die Konfiguration und Konfigurationsoberfläche könnten zu komplex sein. Implementierungsabhängig.

Wir werden wahrscheinlich NICHT versuchen, ElGamal und hybrid-Algorithmen auf derselben Destination zu unterstützen. ElGamal ist veraltet, und ElGamal + hybrid allein (ohne X25519) macht nicht viel Sinn. Außerdem sind sowohl ElGamal als auch Hybrid New Session Messages groß, sodass Klassifizierungsstrategien oft beide Entschlüsselungen versuchen müssten, was ineffizient wäre. Implementierungsabhängig.

Clients können dieselben oder unterschiedliche X25519 statische Schlüssel für die X25519 und die hybriden Protokolle auf denselben tunnels verwenden, implementierungsabhängig.

#### Alice KDF für Message 1

Die ECIES-Spezifikation erlaubt Garlic Messages in der New Session Message-Nutzlast, was eine 0-RTT-Zustellung des initialen Streaming-Pakets, normalerweise ein HTTP GET, zusammen mit dem leaseset des Clients ermöglicht. Jedoch hat die New Session Message-Nutzlast keine Forward Secrecy. Da dieser Vorschlag die verstärkte Forward Secrecy für ratchet betont, könnten oder sollten Implementierungen die Aufnahme der Streaming-Nutzlast oder der vollständigen Streaming-Nachricht bis zur ersten Existing Session Message aufschieben. Dies würde auf Kosten der 0-RTT-Zustellung gehen. Strategien können auch vom Traffic-Typ oder tunnel-Typ abhängen, oder zum Beispiel von GET vs. POST. Implementierungsabhängig.

#### Bob KDF für Nachricht 1

MLKEM, MLDSA oder beide auf demselben Ziel werden die Größe der New Session Message dramatisch erhöhen, wie oben beschrieben. Dies kann die Zuverlässigkeit der Zustellung von New Session Messages durch Tunnel erheblich verringern, wo sie in mehrere 1024-Byte-Tunnel-Nachrichten fragmentiert werden müssen. Der Zustellungserfolg ist proportional zur exponentiellen Anzahl der Fragmente. Implementierungen können verschiedene Strategien verwenden, um die Größe der Nachricht zu begrenzen, auf Kosten der 0-RTT-Zustellung. Implementierungsabhängig.

### Ratchet

Wir können das MSB des ephemeral key (key[31] & 0x80) in der Session-Anfrage setzen, um anzuzeigen, dass dies eine Hybrid-Verbindung ist. Dies würde es uns ermöglichen, sowohl Standard-NTCP als auch Hybrid-NTCP auf demselben Port zu betreiben. Nur eine Hybrid-Variante würde unterstützt und in der router address angekündigt werden. Zum Beispiel v=2,3 oder v=2,4 oder v=2,5.

Wenn wir das nicht tun, benötigen wir eine andere Transportadresse/Port und einen neuen Protokollnamen wie "NTCP1PQ1".

Hinweis: Type-Codes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angezeigt.

TODO

### SSU2

KANN unterschiedliche Transport-Adresse/Port benötigen, aber hoffentlich nicht, wir haben einen Header mit Flags für Nachricht 1. Wir könnten intern das Versionsfeld verwenden und 3 für MLKEM512 und 4 für MLKEM768 nutzen. Vielleicht würde einfach v=2,3,4 in der Adresse ausreichen. Aber wir brauchen Identifikatoren für beide neuen Algorithmen: 3a, 3b?

Überprüfen und verifizieren, dass SSU2 die über mehrere Pakete fragmentierte RI handhaben kann (6-8?). i2pd unterstützt derzeit nur maximal 2 Fragmente?

Hinweis: Typencodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

TODO

## Router Compatibility

### Transport Names

Wir werden wahrscheinlich keine neuen Transport-Namen benötigen, wenn wir sowohl Standard- als auch Hybrid-Varianten auf demselben Port betreiben können, mit Versions-Flags.

Falls wir neue Transport-Namen benötigen, wären dies:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Beachten Sie, dass SSU2 MLKEM1024 nicht unterstützen kann, da es zu groß ist.

### Router Enc. Types

Wir haben mehrere Alternativen zu berücksichtigen:

#### Bob KDF für Message 2

Nicht empfohlen. Verwenden Sie nur die neuen Transports, die oben aufgeführt sind und zum router-Typ passen. Ältere router können sich nicht verbinden, Tunnel durch sie bauen oder netDb-Nachrichten an sie senden. Würde mehrere Veröffentlichungszyklen benötigen, um zu debuggen und Support sicherzustellen, bevor es standardmäßig aktiviert wird. Könnte die Einführung um ein Jahr oder mehr gegenüber den unten stehenden Alternativen verlängern.

#### Alice KDF für Message 2

Empfohlen. Da PQ den X25519 Static Key oder N-Handshake-Protokolle nicht beeinflusst, könnten wir die Router als Typ 4 belassen und nur neue Transporte ankündigen. Ältere Router könnten sich weiterhin verbinden, Tunnel durch sie bauen oder netDb-Nachrichten an sie senden.

#### KDF für Message 3 (nur XK)

Typ-4-Router könnten sowohl NTCP2- als auch NTCP2PQ*-Adressen bekanntgeben. Diese könnten denselben statischen Schlüssel und andere Parameter verwenden oder auch nicht. Diese werden wahrscheinlich auf verschiedenen Ports laufen müssen; es wäre sehr schwierig, sowohl NTCP2- als auch NTCP2PQ*-Protokolle auf demselben Port zu unterstützen, da es keinen Header oder Rahmen gibt, der es Bob ermöglichen würde, die eingehende Session Request-Nachricht zu klassifizieren und zu rahmen.

Separate Ports und Adressen werden für Java schwierig, aber für i2pd unkompliziert sein.

#### KDF für split()

Typ-4-router könnten sowohl SSU2- als auch SSU2PQ*-Adressen bekanntgeben. Mit zusätzlichen Header-Flags könnte Bob den eingehenden Transport-Typ in der ersten Nachricht identifizieren. Daher könnten wir sowohl SSU2 als auch SSUPQ* auf demselben Port unterstützen.

Diese könnten als separate Adressen veröffentlicht werden (wie i2pd es bei früheren Übergängen getan hat) oder in derselben Adresse mit einem Parameter, der PQ-Unterstützung anzeigt (wie Java i2p es bei früheren Übergängen getan hat).

Wenn in derselben Adresse oder am selben Port in verschiedenen Adressen, würden diese denselben statischen Schlüssel und andere Parameter verwenden. Wenn in verschiedenen Adressen mit verschiedenen Ports, könnten diese denselben statischen Schlüssel und andere Parameter verwenden oder auch nicht.

Getrennte Ports und Adressen werden für Java schwierig sein, aber für i2pd unkompliziert.

#### Recommendations

TODO

### NTCP2

#### Noise-Identifikatoren

Ältere router verifizieren RIs und können daher keine Verbindung herstellen, Tunnel durch sie bauen oder netDb-Nachrichten an sie senden. Würde mehrere Release-Zyklen dauern, um zu debuggen und Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird. Wären dieselben Probleme wie beim enc. type 5/6/7 Rollout; könnte den Rollout um ein Jahr oder mehr gegenüber der oben aufgeführten type 4 enc. type Rollout-Alternative verlängern.

Keine Alternativen.

### LS Enc. Types

#### 1b) Neues Session-Format (mit Binding)

Diese können im LS mit älteren Typ-4-X25519-Schlüsseln vorhanden sein. Ältere Router werden unbekannte Schlüssel ignorieren.

Destinations können mehrere Schlüsseltypen unterstützen, aber nur durch Versuchsentschlüsselung der Nachricht 1 mit jedem Schlüssel. Der Overhead kann reduziert werden, indem Zähler für erfolgreiche Entschlüsselungen für jeden Schlüssel geführt und der am häufigsten verwendete Schlüssel zuerst versucht wird. Java I2P verwendet diese Strategie für ElGamal+X25519 auf derselben Destination.

### Dest. Sig. Types

#### 1g) Neues Session Reply Format

Router verifizieren leaseSet-Signaturen und können daher nicht verbinden oder leaseSets für Typ 12-17 Ziele empfangen. Würde mehrere Veröffentlichungszyklen dauern, um zu debuggen und Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird.

Keine Alternativen.

## Spezifikation

Die wertvollsten Daten sind der End-zu-End-Verkehr, verschlüsselt mit ratchet. Als externer Beobachter zwischen tunnel-Sprüngen ist das zweimal zusätzlich verschlüsselt, mit tunnel-Verschlüsselung und transport-Verschlüsselung. Als externer Beobachter zwischen OBEP und IBGW ist es nur einmal zusätzlich verschlüsselt, mit transport-Verschlüsselung. Als OBEP- oder IBGW-Teilnehmer ist ratchet die einzige Verschlüsselung. Da tunnels jedoch unidirektional sind, würde das Abfangen beider Nachrichten im ratchet-Handshake kollaboriererende router erfordern, es sei denn, tunnels wurden mit dem OBEP und IBGW auf demselben router aufgebaut.

Das derzeit besorgniserregendste PQ-Bedrohungsmodell ist die Speicherung von Datenverkehr heute zur Entschlüsselung in vielen, vielen Jahren (Forward Secrecy). Ein Hybridansatz würde davor schützen.

Das PQ-Bedrohungsmodell, bei dem die Authentifizierungsschlüssel in einem angemessenen Zeitraum (sagen wir ein paar Monate) gebrochen und dann die Authentifizierung nachgeahmt oder nahezu in Echtzeit entschlüsselt wird, ist noch viel weiter entfernt? Und das wäre der Zeitpunkt, an dem wir zu PQC-Statikschlüsseln migrieren möchten.

Die früheste PQ-Bedrohungsmodell ist also OBEP/IBGW, die Verkehr für spätere Entschlüsselung speichern. Wir sollten zuerst Hybrid-Ratchet implementieren.

Ratchet hat die höchste Priorität. Transports sind als nächstes dran. Signaturen haben die niedrigste Priorität.

Die Einführung von Signaturen wird auch ein Jahr oder länger nach der Einführung der Verschlüsselung erfolgen, da keine Rückwärtskompatibilität möglich ist. Außerdem wird die MLDSA-Einführung in der Industrie durch das CA/Browser Forum und Zertifizierungsstellen standardisiert werden. CAs benötigen zunächst Hardware-Sicherheitsmodul (HSM) Unterstützung, die derzeit nicht verfügbar ist [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Wir erwarten, dass das CA/Browser Forum Entscheidungen über spezifische Parameterwahlen vorantreibt, einschließlich der Frage, ob zusammengesetzte Signaturen unterstützt oder gefordert werden sollen [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Wenn wir sowohl alte als auch neue Ratchet-Protokolle in denselben Tunneln nicht unterstützen können, wird die Migration viel schwieriger.

Wir sollten in der Lage sein, einfach das eine und dann das andere zu versuchen, wie wir es mit X25519 getan haben, um es zu beweisen.

## Issues

- Noise Hash Auswahl - bei SHA256 bleiben oder upgraden?
  SHA256 sollte weitere 20-30 Jahre gut sein, nicht durch PQ bedroht,
  Siehe [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) und [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Wenn SHA256 geknackt wird, haben wir schlimmere Probleme (netDb).
- NTCP2 separater Port, separate router Adresse
- SSU2 relay / peer test
- SSU2 Versionsfeld
- SSU2 router Adressversion
