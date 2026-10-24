---
title: "Post-Quantum-Kryptographie-Protokolle"
aliases:
  - "/proposals/169-pq-crypto"
  - "/proposals/169-pq-crypto/"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Öffnen"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Status

| Protokoll / Funktion | Status |
|--------------------|--------|
| Ratchet | Vollständig in Java I2P und i2pd |
| NTCP2 | Beta Q1 2026 |
| SSU2 | Implementierung beginnt bald, Beta Q23 2026 |
| MLDSA SigTypes | Niedrige Priorität, wahrscheinlich 2027+ |
## Überblick

Während die Forschung und der Wettbewerb um geeignete Post-Quantum-(PQ-)Kryptographie seit einem Jahrzehnt voranschreiten, sind die Optionen erst kürzlich klar geworden.

Wir begannen 2022 mit der Untersuchung der Auswirkungen von PQ-Kryptographie [zzz.i2p](http://zzz.i2p/topics/3294).

TLS-Standards haben in den letzten zwei Jahren Unterstützung für hybride Verschlüsselung hinzugefügt und diese wird nun für einen erheblichen Teil des verschlüsselten Internetverkehrs verwendet, dank der Unterstützung in Chrome und Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST hat kürzlich die empfohlenen Algorithmen für Post-Quanten-Kryptographie finalisiert und veröffentlicht [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Mehrere gängige Kryptographie-Bibliotheken unterstützen nun die NIST-Standards oder werden in naher Zukunft Unterstützung dafür bereitstellen.

Sowohl [Cloudflare](https://blog.cloudflare.com/pq-2024/) als auch [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) empfehlen, dass die Migration sofort beginnen sollte. Siehe auch die NSA PQ FAQ von 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P sollte ein Vorreiter in Sicherheit und Kryptographie sein. Jetzt ist es an der Zeit, die empfohlenen Algorithmen zu implementieren. Mit unserem flexiblen Krypto-Typ- und Signatur-Typ-System werden wir Typen für hybride Kryptographie sowie für PQ- und hybride Signaturen hinzufügen.

## Ziele

- PQ-resistente Algorithmen auswählen
- PQ-only und hybride Algorithmen zu I2P-Protokollen hinzufügen, wo angemessen
- Mehrere Varianten definieren
- Beste Varianten nach Implementierung, Tests, Analyse und Forschung auswählen
- Unterstützung schrittweise und mit Rückwärtskompatibilität hinzufügen

## Nicht-Ziele

- Ändern Sie keine Einweg-(Noise N)-Verschlüsselungsprotokolle
- Entfernen Sie sich nicht von SHA256, kurzfristig nicht von PQ bedroht
- Wählen Sie die endgültigen bevorzugten Varianten zu diesem Zeitpunkt nicht aus

## Bedrohungsmodell

- Router am OBEP oder IBGW, möglicherweise in Absprache,
  speichern garlic-Nachrichten für spätere Entschlüsselung (Forward Secrecy)
- Netzwerkbeobachter
  speichern Transportnachrichten für spätere Entschlüsselung (Forward Secrecy)
- Netzwerkteilnehmer fälschen Signaturen für RI, LS, Streaming, Datagramme,
  oder andere Strukturen

## Betroffene Protokolle

Wir werden die folgenden Protokolle modifizieren, ungefähr in der Reihenfolge der Entwicklung. Die gesamte Einführung wird wahrscheinlich von Ende 2025 bis Mitte 2027 dauern. Siehe den Abschnitt Prioritäten und Einführung unten für Details.

| Protokoll / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Genehmigt 2025-06; beta 2025-08; Release 2025-11 |
| Hybrid MLKEM NTCP2 | Im Live-Netz getestet, Genehmigt 2026-02; beta Ziel 2026-05; Release Ziel 2026-08 |
| Hybrid MLKEM SSU2 | Genehmigt 2026-02; beta Ziel 2026-08; Release Ziel 2026-11 |
| MLDSA SigTypes 12-14 | Vorschlag ist stabil, aber möglicherweise erst 2027 finalisiert |
| MLDSA Dests | Im Live-Netz getestet, erfordert Netz-Upgrade für floodfill-Unterstützung |
| Hybrid SigTypes 15-17 | Vorläufig |
| Hybrid Dests | |
## Design

Wir werden die NIST FIPS 203 und 204 Standards [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) unterstützen, die auf CRYSTALS-Kyber und CRYSTALS-Dilithium (Versionen 3.1, 3 und älter) basieren, aber NICHT kompatibel damit sind.

### Schlüsselaustausch

Wir werden hybriden Schlüsselaustausch in den folgenden Protokollen unterstützen:

| Proto   | Noise Type | Nur PQ unterstützt? | Hybrid unterstützt? |
|---------|------------|---------------------|---------------------|
| NTCP2   | XK         | nein                | ja                  |
| SSU2    | XK         | nein                | ja                  |
| Ratchet | IK         | nein                | ja                  |
| TBM     | N          | nein                | nein                |
| NetDB   | N          | nein                | nein                |
PQ KEM stellt nur ephemere Schlüssel bereit und unterstützt nicht direkt statische Schlüssel-Handshakes wie Noise XK und IK.

Noise N verwendet keinen bidirektionalen Schlüsselaustausch und ist daher nicht für hybride Verschlüsselung geeignet.

Daher werden wir nur hybride Verschlüsselung für NTCP2, SSU2 und Ratchet unterstützen. Wir werden die drei ML-KEM-Varianten wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert verwenden, für insgesamt 3 neue Verschlüsselungstypen. Hybride Typen werden nur in Kombination mit X25519 definiert.

Die neuen Verschlüsselungstypen sind:

| Typ | Code |
|-----|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Der Overhead wird erheblich sein. Typische Nachrichtengrößen 1 und 2 (für XK und IK) betragen derzeit etwa 100 Bytes (vor zusätzlicher Nutzlast). Dies wird sich je nach Algorithmus um das 8- bis 15-fache erhöhen.

### Signaturen

Wir werden PQ- und Hybrid-Signaturen in den folgenden Strukturen unterstützen:

Wir werden also sowohl reine PQ- als auch hybride Signaturen unterstützen. Wir werden die drei ML-DSA-Varianten wie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert, drei hybride Varianten mit Ed25519 und drei reine PQ-Varianten mit Prehash nur für SU3-Dateien definieren, insgesamt 9 neue Signaturtypen. Hybride Typen werden nur in Kombination mit Ed25519 definiert. Wir werden das Standard-ML-DSA verwenden, NICHT die Pre-hash-Varianten (HashML-DSA), außer für SU3-Dateien.

| Typ | Unterstützt nur PQ? | Unterstützt Hybrid? |
|-----|---------------------|---------------------|
| RouterInfo | ja | ja |
| LeaseSet | ja | ja |
| Streaming SYN/SYNACK/Close | ja | ja |
| Repliable Datagrams | ja | ja |
| Datagram2 (prop. 163) | ja | ja |
| I2CP create session msg | ja | ja |
| SU3-Dateien | ja | ja |
| X.509-Zertifikate | ja | ja |
| Java keystores | ja | ja |
Wir werden die "hedged" oder randomisierte Signaturvariante verwenden, nicht die "deterministische" Variante, wie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Abschnitt 3.4 definiert. Dies stellt sicher, dass jede Signatur unterschiedlich ist, auch wenn sie über dieselben Daten erstellt wird, und bietet zusätzlichen Schutz vor Seitenkanalangriffen. Siehe den Abschnitt zu Implementierungshinweisen unten für weitere Details zu Algorithmusauswahlen einschließlich Kodierung und Kontext.

Die neuen Signaturtypen sind:

X.509-Zertifikate und andere DER-Kodierungen werden die zusammengesetzten Strukturen und OIDs verwenden, die im [IETF-Entwurf](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) definiert sind.

| Typ | Code |
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
Der Overhead wird erheblich sein. Typische Ed25519-Destination- und Router-Identity-Größen betragen 391 Bytes. Diese werden je nach Algorithmus um das 3,5- bis 6,8-fache ansteigen. Ed25519-Signaturen sind 64 Bytes groß. Diese werden je nach Algorithmus um das 38- bis 76-fache ansteigen. Typische signierte RouterInfo, leaseSet, beantwortbare Datagramme und signierte Streaming-Nachrichten sind etwa 1KB groß. Diese werden je nach Algorithmus um das 3- bis 8-fache ansteigen.

Da die neuen Destination- und Router-Identity-Typen keine Füllbytes enthalten werden, sind sie nicht komprimierbar. Die Größe von Destinations und Router-Identities, die während der Übertragung mit gzip komprimiert werden, wird sich je nach Algorithmus um das 12- bis 38-fache erhöhen.

Für Destinations werden die neuen Signaturtypen mit allen Verschlüsselungstypen im leaseSet unterstützt. Setzen Sie den Verschlüsselungstyp im Schlüsselzertifikat auf NONE (255).

### Gültige Kombinationen

Für RouterIdentities ist die ElGamal-Verschlüsselungsart veraltet. Die neuen Signaturtypen werden nur mit X25519 (Typ 4) Verschlüsselung unterstützt. Die neuen Verschlüsselungstypen werden in den RouterAddresses angegeben. Der Verschlüsselungstyp im Schlüsselzertifikat wird weiterhin Typ 4 sein.

Testvektoren für SHA3-256, SHAKE128 und SHAKE256 sind bei [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) verfügbar.

### Neue Kryptografie erforderlich

- ML-KEM (ehemals CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (ehemals CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (ehemals Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Nur für SHAKE128 verwendet
- SHA3-256 (ehemals Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 und SHAKE256 (XOF-Erweiterungen zu SHA3-128 und SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Beachten Sie, dass die Java bouncycastle-Bibliothek alle oben genannten unterstützt. C++-Bibliotheksunterstützung ist in OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/) verfügbar.

Wir werden [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+) nicht unterstützen, es ist viel viel langsamer und größer als ML-DSA. Wir werden das kommende FIPS206 (Falcon) nicht unterstützen, es ist noch nicht standardisiert. Wir werden NTRU oder andere PQ-Kandidaten, die nicht von NIST standardisiert wurden, nicht unterstützen.

### Alternativen

Es gibt einige Forschungsarbeiten [paper](https://eprint.iacr.org/2020/379.pdf) zur Anpassung von Wireguard (IK) für reine PQ-Kryptographie, aber es gibt mehrere offene Fragen in dieser Arbeit. Später wurde dieser Ansatz als Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) für PQ Wireguard implementiert.

### Rosenpass

Rosenpass verwendet einen Noise KK-ähnlichen Handshake mit vorab geteilten statischen Classic McEliece 460896 Schlüsseln (jeweils 500 KB) und Kyber-512 (im Wesentlichen MLKEM-512) ephemeren Schlüsseln. Da die Classic McEliece Chiffretexte nur 188 Bytes groß sind und die Kyber-512 öffentlichen Schlüssel und Chiffretexte angemessen sind, passen beide Handshake-Nachrichten in eine Standard-UDP-MTU. Der ausgegebene geteilte Schlüssel (osk) aus dem PQ KK Handshake wird als Eingabe-Vorabschlüssel (psk) für den Standard-Wireguard IK Handshake verwendet. Es gibt also insgesamt zwei vollständige Handshakes, einen rein PQ und einen rein X25519.

Wir können nichts davon tun, um unsere XK- und IK-Handshakes zu ersetzen, weil:

Es gibt viele gute Informationen im Whitepaper, und wir werden es auf Ideen und Inspiration hin durchgehen. TODO.

- Wir können KK nicht durchführen, Bob hat Alices statischen Schlüssel nicht
- 500KB statische Schlüssel sind viel zu groß
- Wir wollen keinen zusätzlichen Roundtrip

Aktualisieren Sie die Abschnitte und Tabellen im Common-Structures-Dokument [/docs/specs/common-structures/](/docs/specs/common-structures/) wie folgt:

## Spezifikation

### Gemeinsame Strukturen

Die neuen Public Key-Typen sind:

#### Probleme

Hybride öffentliche Schlüssel sind der X25519-Schlüssel. KEM-öffentliche Schlüssel sind der ephemere PQ-Schlüssel, der von Alice an Bob gesendet wird. Kodierung und Byte-Reihenfolge sind in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert.

| Typ | Public Key Länge | Seit | Verwendung |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM512 | 800 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM768 | 1184 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| NONE | 0 | 0.9.xx | Siehe Vorschlag 169, nur für Destinations mit PQ-Signaturtypen, nicht für RIs oder Leasesets |
MLKEM*_CT-Schlüssel sind nicht wirklich öffentliche Schlüssel, sie sind der "Ciphertext" (verschlüsselte Text), der von Bob an Alice im Noise-Handshake gesendet wird. Sie sind hier der Vollständigkeit halber aufgeführt.

Die neuen Private Key-Typen sind:

#### PrivateKey

Hybride private Schlüssel sind die X25519-Schlüssel. KEM private Schlüssel sind nur für Alice. KEM-Kodierung und Byte-Reihenfolge sind in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert.

| Typ | Private Schlüssellänge | Seit | Verwendung |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM512 | 1632 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM768 | 2400 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Siehe Vorschlag 169, nur für Handshakes, nicht für Leasesets, RIs oder Destinations |
Die neuen Signing Public Key-Typen sind:

#### SigningPublicKey

Hybride Signatur-Public-Keys sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie im [IETF-Entwurf](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) beschrieben. Kodierung und Byte-Reihenfolge sind in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.

| Typ | Länge (Bytes) | Seit | Verwendung |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65 | 1952 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87 | 2592 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44ph | 1344 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen |
| MLDSA65ph | 1984 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen |
| MLDSA87ph | 2624 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen |
Die neuen Typen von privaten Signaturschlüsseln sind:

#### SigningPrivateKey

Hybride private Signaturschlüssel bestehen aus dem Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie im [IETF-Entwurf](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) beschrieben. Kodierung und Byte-Reihenfolge sind in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.

| Typ | Länge (Bytes) | Seit | Verwendung |
|-----|---------------|------|------------|
| MLDSA44 | 2560 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65 | 4032 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87 | 4896 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44ph | 2592 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
| MLDSA65ph | 4064 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
| MLDSA87ph | 4928 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
Die neuen Signature-Typen sind:

Hybrid-Signaturen sind die Ed25519-Signatur gefolgt von der PQ-Signatur, wie im [IETF-Entwurf](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) beschrieben. Hybrid-Signaturen werden verifiziert, indem beide Signaturen verifiziert werden, und schlagen fehl, wenn eine der beiden fehlschlägt. Codierung und Byte-Reihenfolge sind in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.

#### Signatur

Die neuen Signing Public Key-Typen sind:

| Typ | Länge (Bytes) | Seit | Verwendung |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65 | 3309 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87 | 4627 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44ph | 2484 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
| MLDSA65ph | 3373 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
| MLDSA87ph | 4691 | 0.9.xx | Nur für SU3-Dateien, nicht für netDb-Strukturen. Siehe Vorschlag 169 |
Die neuen Crypto Public Key-Typen sind:

#### Schlüsselzertifikate

Hybride Signatur-Public-Keys sind der Ed25519-Schlüssel gefolgt vom PQ-Schlüssel, wie im [IETF-Entwurf](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) beschrieben. Kodierung und Byte-Reihenfolge sind in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) definiert.

| Typ | Typ-Code | Gesamte Länge des öffentlichen Schlüssels | Seit | Verwendung |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Siehe Vorschlag 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Nur für SU3-Dateien |
| MLDSA65ph | 19 | n/a | 0.9.xx | Nur für SU3-Dateien |
| MLDSA87ph | 20 | n/a | 0.9.xx | Nur für SU3-Dateien |
Für Ziele mit Hybrid- oder PQ-Signaturtypen verwenden Sie NONE (Typ 255) für den Verschlüsselungstyp, aber es gibt keinen Kryptoschlüssel, und der gesamte 384-Byte-Hauptbereich ist für den Signaturschlüssel vorgesehen.

| Typ | Typ-Code | Gesamte Länge des öffentlichen Schlüssels | Seit | Verwendung |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Siehe Vorschlag 169, nur für Leasesets, nicht für RIs oder Destinations |
| NONE | 255 | 0 | 0.9.xx | Siehe Vorschlag 169 |
Hybride Schlüsseltypen werden NIEMALS in Schlüsselzertifikaten eingeschlossen; nur in leaseSets.

Kein Padding. Die Gesamtlänge beträgt 7 + Gesamtschlüssellänge. Die Schlüsselzertifikatslänge beträgt 4 + überschüssige Schlüssellänge.

#### Destination-Größen

Hier sind die Längen für die neuen Destination-Typen. Der Verschlüsselungstyp für alle ist NONE (Typ 255) und die Verschlüsselungsschlüssellänge wird als 0 behandelt. Der gesamte 384-Byte-Bereich wird für den ersten Teil des öffentlichen Signaturschlüssels verwendet. HINWEIS: Dies unterscheidet sich von der Spezifikation für die ECDSA_SHA512_P521- und RSA-Signaturtypen, bei denen wir den 256-Byte ElGamal-Schlüssel in der Destination beibehalten haben, obwohl er nicht verwendet wurde.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Beispiel 1319-Byte Ziel-Byte-Stream für MLDSA44:

Beispiel eines 1351-Byte Router-Identity-Byte-Streams für MLDSA44:

| Typ | Typ Code | Gesamte Public Key Länge | Haupt | Überschuss | Gesamte Dest Länge |
|-----|----------|--------------------------|-------|------------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### RouterIdent-Größen

Hier sind die Längen für die neuen Destination-Typen. Der Enc-Typ für alle ist X25519 (Typ 4). Der gesamte 352-Byte-Bereich nach dem X25519 Public Key wird für den ersten Teil des Signing Public Key verwendet. Kein Padding. Die Gesamtlänge beträgt 39 + Gesamtschlüssellänge. Die Key Certificate-Länge beträgt 4 + überschüssige Schlüssellänge.

Handshakes verwenden [Noise Protocol](https://noiseprotocol.org/noise.html) Handshake-Muster.

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Typ | Typ-Code | Gesamte Public-Key-Länge | Haupt | Überschuss | Gesamte RouterIdent-Länge |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Die folgenden Änderungen an XK und IK für hybride Vorwärtsgeheimhaltung (hfs) sind wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 5 spezifiziert:

Das e1-Muster ist wie folgt definiert, wie in der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 angegeben:

#### KDF für split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Noise-Identifikatoren

Das ekem1-Muster ist wie folgt definiert, wie in der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 festgelegt:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Neues Session-Format (mit Bindung)

Dieser Abschnitt gilt sowohl für IK- als auch für XK-Protokolle.

### Handshake-Muster

Der hybride Handshake ist in der [Noise HFS Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) definiert. Die erste Nachricht von Alice an Bob enthält e1, den Kapselungsschlüssel, vor der Nachrichtennutzlast. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufe EncryptAndHash() darauf auf (als Alice) oder DecryptAndHash() (als Bob). Dann verarbeite die Nachrichtennutzlast wie gewohnt.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload
- e1 = einmaliger ephemerer PQ-Schlüssel, von Alice an Bob gesendet
- ekem1 = der KEM-Chiffretext, von Bob an Alice gesendet

Wir definieren die folgenden Funktionen, die den kryptographischen Bausteinen entsprechen, die wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert verwendet werden.

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### Noise Handshake KDF

#### 1b) Neues Session-Format (mit Bindung)

- Sollten wir die Handshake-Hash-Funktion ändern? Siehe [Vergleich](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 ist nicht anfällig für PQ, aber wenn wir unsere
  Hash-Funktion upgraden wollen, ist jetzt der richtige Zeitpunkt, während wir andere Dinge ändern.
  Der aktuelle IETF SSH-Vorschlag [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) ist, MLKEM768
  mit SHA256 und MLKEM1024 mit SHA384 zu verwenden. Dieser Vorschlag enthält
  eine Diskussion der Sicherheitsüberlegungen.
- Sollten wir aufhören, 0-RTT Ratchet-Daten (außer dem leaseSet) zu senden?
- Sollten wir Ratchet von IK zu XK wechseln, wenn wir keine 0-RTT-Daten senden?

#### Überblick

kem_shared_key = DECAPS(ciphertext, decap_key)

Beachten Sie, dass sowohl der encap_key als auch der ciphertext innerhalb von ChaCha/Poly-Blöcken in den Noise-Handshake-Nachrichten 1 und 2 verschlüsselt sind. Sie werden als Teil des Handshake-Prozesses entschlüsselt.

Die zweite Nachricht, von Bob an Alice, enthält ekem1, den Chiffretext, vor der Nachrichtennutzlast. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie EncryptAndHash() darauf auf (als Bob) oder DecryptAndHash() (als Alice). Dann berechnen Sie den kem_shared_key und rufen MixKey(kem_shared_key) auf. Anschließend verarbeiten Sie die Nachrichtennutzlast wie gewohnt.

#### Definierte ML-KEM-Operationen

Für XK: Nach dem 'es' Nachrichtenmuster und vor der Nutzlast, hinzufügen:

ODER

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Für IK: Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster hinzufügen:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

Für XK: Nach dem 'es' Nachrichtenmuster und vor der Nutzlast, hinzufügen:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

ODER

Der kem_shared_key wird mit MixHash() in den chaining key eingemischt. Siehe unten für Details.

#### Alice KDF für Nachricht 1

Für XK: Nach dem 'ee' Nachrichtenmuster und vor der Nutzlast, hinzufügen:

ODER

Für IK: Nach dem 'ee' Nachrichtenmuster und vor dem 'se' Nachrichtenmuster, füge hinzu:

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
#### Bob KDF für Nachricht 1

Für XK: Nach dem 'ee' Nachrichtenmuster und vor der Nutzlast, hinzufügen:

ODER

Für IK: Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster hinzufügen:

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
#### Bob KDF für Nachricht 2

Aktualisiere die ECIES-Ratchet-Spezifikation [/docs/specs/ecies/](/docs/specs/ecies/) wie folgt:

ODER

Verschlüsseltes Format:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF für Nachricht 2

Nach dem 'ee' Nachrichtenmuster (und vor dem 'ss' Nachrichtenmuster für IK), füge hinzu:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF für Nachricht 3 (nur XK)

unverändert

#### Noise-Identifikatoren

unverändert

### Ratchet

Änderungen: Der aktuelle Ratchet hat eine leere Nutzlast für den ersten ChaCha-Abschnitt und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Chiffretext. Der zweite Abschnitt hat eine leere Nutzlast. Der dritte Abschnitt enthält die Nutzlast.

#### Langer Header

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Kurzer Header

Änderungen: Der aktuelle ratchet enthielt den statischen Schlüssel im ersten ChaCha-Abschnitt und die Nutzdaten im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-öffentlichen Schlüssel. Der zweite Abschnitt enthält den statischen Schlüssel. Der dritte Abschnitt enthält die Nutzdaten.

Entschlüsseltes Format:

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

| Typ | Typ-Code | X-Länge | Nachricht 1 Länge | Nachricht 1 Verschl.-Länge | Nachricht 1 Entschl.-Länge | PQ-Schlüssel-Länge | pl-Länge |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Beachten Sie, dass die Payload einen DateTime-Block enthalten muss, daher beträgt die minimale Payload-Größe 7. Die minimalen Nachrichtengrößen für Message 1 können entsprechend berechnet werden.

#### 1g) Neues Session Reply Format

Änderungen: Das aktuelle NTCP2 enthält nur die Optionen im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

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

| Typ | Typ Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Beachten Sie, dass Nachricht 2 normalerweise eine Nutzdaten ungleich null haben wird, die ratchet-Spezifikation [/docs/specs/ecies/](/docs/specs/ecies/) erfordert dies jedoch nicht, daher beträgt die minimale Nutzdatengröße 0. Die minimalen Größen für Nachricht 2 können entsprechend berechnet werden.

### NTCP2

Aktualisieren Sie die NTCP2-Spezifikation [/docs/specs/ntcp2/](/docs/specs/ntcp2/) wie folgt:

#### Noise-Identifikatoren

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Rohe Inhalte:

Damit PQ und Nicht-PQ NTCP2 auf derselben Router-Adresse und demselben Port unterstützt werden können, verwenden wir das höchstwertige Bit des X-Werts (X25519 ephemeral public key), um zu kennzeichnen, dass es sich um eine PQ-Verbindung handelt. Dieses Bit ist bei Nicht-PQ-Verbindungen immer nicht gesetzt.

Hinweis: Das Versionsfeld im Optionsblock von Nachricht 1 muss auf 2 gesetzt werden, auch bei PQ-Verbindungen.

Für Bob nach der AES-Entschleierung von X: teste X[31] & 0x80. Wenn das Bit gesetzt ist, lösche es mit X[31] &= 0x7f und entschlüssele via Noise als PQ-Verbindung. Wenn das Bit nicht gesetzt ist, entschlüssele via Noise als normale Nicht-PQ-Verbindung wie üblich.

Für PQ NTCP2, das auf einer anderen router-Adresse und einem anderen Port beworben wird, ist dies nicht erforderlich.

Für weitere Informationen siehe den Abschnitt "Published Addresses" unten.

Unverschlüsselte Daten (Poly1305 auth tag nicht gezeigt):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
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
Hinweis: Typcodes sind nur für interne Verwendung. Router bleiben Typ 4, und die Unterstützung wird in den router-Adressen angezeigt.

Größen:

| Typ | Typ-Code | X-Länge | Msg 1-Länge | Msg 1 Enc-Länge | Msg 1 Dec-Länge | PQ-Schlüssel-Länge | opt-Länge |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

#### 2) SessionCreated

Rohe Inhalte:

Unverschlüsselte Daten (Poly1305 auth tag nicht gezeigt):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Größen:

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

| Typ | Typ-Code | Y-Länge | Nachricht-2-Länge | Nachricht-2-Enc-Länge | Nachricht-2-Dec-Länge | PQ-CT-Länge | opt-Länge |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

#### 3) SessionConfirmed

Unverändert

#### Key Derivation Function (KDF) (für Datenphase)

Unverändert

#### Veröffentlichte Adressen

Verwenden Sie in allen Fällen den NTCP2-Transportnamen wie gewohnt.

Verwenden Sie dieselbe Adresse und denselben Port wie im Nicht-PQ-Fall ohne Firewall. Es wird nur eine PQ-Variante unterstützt. Veröffentlichen Sie in der Router-Adresse v=2 (wie üblich) und den neuen Parameter pq=[3|4|5], um MLKEM 512/768/1024 anzugeben. Alice setzt das MSB des ephemeral key (key[31] & 0x80) in der Session-Anfrage, um anzugeben, dass dies eine hybride Verbindung ist. Siehe oben. Ältere Router ignorieren den pq-Parameter und verbinden wie üblich ohne PQ.

Firewall-geschützte Adressen (keine IP veröffentlicht): In der router-Adresse v=2 veröffentlichen (wie üblich). Es ist nicht erforderlich, einen pq-Parameter zu veröffentlichen.

Alice kann sich mit einem PQ Bob über die PQ-Variante verbinden, die Bob veröffentlicht, unabhängig davon, ob Alice pq-Unterstützung in ihren Router-Informationen bewirbt oder ob sie dieselbe Variante bewirbt.

In der aktuellen Spezifikation sind die Nachrichten 1 und 2 definiert, um eine "angemessene" Menge an Padding zu haben, wobei ein Bereich von 0-31 Bytes empfohlen wird und kein Maximum spezifiziert ist.

#### Maximaler Padding

Bis API 0.9.68 (Release 2.11.0) implementierte Java I2P ein Maximum von 256 Bytes Padding für Nicht-PQ-Verbindungen, jedoch war dies zuvor nicht dokumentiert. Ab API 0.9.69 (Release 2.12.0) implementiert Java I2P das gleiche maximale Padding für Nicht-PQ-Verbindungen wie für MLKEM-512. Siehe Tabelle unten.

Verwenden Sie die definierte Nachrichtengröße als maximales Padding, das heißt, das maximale Padding wird die Nachrichtengröße für PQ-Verbindungen verdoppeln, wie folgt:

Verwenden Sie die definierte Nachrichtengröße als maximales Padding; das heißt, das maximale Padding verdoppelt die Nachrichtengröße für PQ-Verbindungen, wie folgt:

| Message Max Padding | non-PQ (bis 0.9.68) | non-PQ (ab 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

Beachten Sie, dass MLKEM-1024 für SSU2 NICHT unterstützt wird, da die Schlüssel zu groß sind, um in ein Standard-1500-Byte-Datagramm zu passen.

#### Noise-Identifikatoren

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Der lange Header ist 32 Bytes groß. Er wird verwendet, bevor eine Sitzung erstellt wird, für Token Request, SessionRequest, SessionCreated und Retry. Er wird auch für sitzungsunabhängige Peer Test und Hole Punch Nachrichten verwendet.

#### Forward Secrecy

In den folgenden Nachrichten setzen Sie das ver (Version) Feld im langen Header auf 3 oder 4, um MLKEM-512 oder MLKEM-768 anzuzeigen.

In den folgenden Nachrichten setzen Sie das ver (Version) Feld im langen Header wie üblich auf 2, auch wenn MLKEM-512 oder MLKEM-768 unterstützt wird. Implementierungen können den Wert auch auf 3 oder 4 setzen, wenn die Gegenstelle dies unterstützt, aber das ist nicht notwendig. Implementierungen sollten jeden Wert von 2-4 akzeptieren.

- (0) Session Request
- (1) Session Created
- (9) Retry
- (10) Token Request
- (11) Hole Punch

Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht gezeigt):

- (7) Peer Test (Nachrichten außerhalb der Sitzung 5-7)

Größen, ohne IP-Overhead:

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angezeigt.

unverändert

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

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Neue Sitzungsgröße

unverändert

#### SessionRequest (Typ 0)

KDF-Änderung für Spoof-Schutz: Um die in Vorschlag 165 [Prop165]_ aufgeworfenen Probleme anzugehen, aber mit einer anderen Lösung, ändern wir die KDF für Session Request. Dies gilt nur für PQ-Sitzungen. Die KDF für Nicht-PQ-Sitzungen bleibt unverändert.

Roher Inhalt:

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Unverschlüsselte Daten (Poly1305 auth tag nicht gezeigt):

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
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht gezeigt):

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
Minimale MTU für MLKEM768_X25519: Etwa 1316 für IPv4 und 1336 für IPv6.

| Typ | Typ Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | zu groß | | | | |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

Änderungen: Aktuelles SSU2 enthält nur die Blockdaten im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

Unverschlüsselte Daten (Poly1305 auth tag nicht angezeigt):

#### SessionCreated (Typ 1)

Rohe Inhalte:

Unverschlüsselte Daten (Poly1305 auth tag nicht gezeigt):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Größen:

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

| Typ | Typ-Code | Y-Len | Msg 2-Len | Msg 2 Enc-Len | Msg 2 Dec-Len | PQ CT-Len | pl-Len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | zu groß | | | | |
Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

Änderungen: Aktuelles SSU2 enthält nur die Blockdaten im ChaCha-Abschnitt. Mit ML-KEM wird der ChaCha-Abschnitt auch den verschlüsselten PQ-Public-Key enthalten.

PQ-Signaturen: Relay-Blöcke, Peer-Test-Blöcke und Peer-Test-Nachrichten enthalten alle Signaturen. Leider sind PQ-Signaturen größer als die MTU. Es gibt derzeit keinen Mechanismus, um Relay- oder Peer-Test-Blöcke oder -Nachrichten über mehrere UDP-Pakete zu fragmentieren. Das Protokoll muss erweitert werden, um Fragmentierung zu unterstützen. Dies wird in einem separaten Vorschlag erfolgen, der noch zu bestimmen ist. Bis dies abgeschlossen ist, werden Relay und Peer Test nicht unterstützt.

#### SessionConfirmed (Typ 2)

unverändert

#### KDF für Datenphase

unverändert

#### Relay- und Peer-Test

Die folgenden Blöcke enthalten Versionsfelder. Sie bleiben Version 2 (für Kompatibilität mit einem nicht-PQ Bob) und werden nicht zu Version 3/4 für PQ geändert.

- SAMv3
- Bittorrent
- Entwicklerrichtlinien
- Benennung / Adressbuch / Jump-Server
- Andere Dokumente

Verwenden Sie in allen Fällen wie gewohnt den SSU2-Transportnamen. MLKEM-1024 wird nicht unterstützt.

#### Veröffentlichte Adressen

Verwenden Sie dieselbe Adresse/Port wie bei nicht-PQ, nicht-firewalled. Eine oder beide PQ-Varianten werden unterstützt. In der router-Adresse veröffentlichen Sie v=2 (wie üblich) und den neuen Parameter pq=[3|4|3,4], um MLKEM 512/768/beide anzuzeigen. Ältere router werden den pq-Parameter ignorieren und sich wie gewohnt nicht-pq verbinden.

Seien Sie vorsichtig, die MTU mit MLKEM768 nicht zu überschreiten. Die minimale MTU für SSU2 beträgt 1280, was der Größe von Nachricht 1 ohne Padding entspricht. Fügen Sie kein Padding in Nachricht 1 hinzu, wenn Alices oder Bobs MTU 1280 beträgt.

Firewalled-Adressen (keine IP veröffentlicht): In der router-Adresse v=2 veröffentlichen (wie üblich). Der pq-Parameter MUSS in firewalled-Adressen veröffentlicht werden, um relay zu unterstützen.

Alice kann sich mit einem PQ Bob über die PQ-Variante verbinden, die Bob veröffentlicht, unabhängig davon, ob Alice pq-Unterstützung in ihren router-Informationen bewirbt oder ob sie dieselbe Variante bewirbt.

In der aktuellen Spezifikation sind die Nachrichten 1 und 2 definiert, um eine "angemessene" Menge an Padding zu haben, wobei ein Bereich von 0-31 Bytes empfohlen wird und kein Maximum spezifiziert ist.

#### MTU

Wir könnten intern das Versionsfeld verwenden und 3 für MLKEM512 und 4 für MLKEM768 nutzen.

### Streaming

Für Nachrichten 1 und 2 würde MLKEM768 die Paketgrößen über die minimale MTU von 1280 hinaus vergrößern. Wahrscheinlich würde es einfach nicht für diese Verbindung unterstützt werden, wenn die MTU zu niedrig wäre.

### SU3-Dateien

Für Nachrichten 1 und 2 würde MLKEM1024 die Paketgrößen über die maximale MTU von 1500 hinaus vergrößern. Das würde eine Fragmentierung der Nachrichten 1 und 2 erfordern und wäre eine große Komplikation. Wahrscheinlich werden wir das nicht machen.

Relay und Peer Test: Siehe oben

TODO: Gibt es eine effizientere Möglichkeit, das Signieren/Verifizieren zu definieren, um das Kopieren der Signatur zu vermeiden?

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) Abschnitt 8.1 verbietet HashML-DSA in X.509-Zertifikaten und weist keine OIDs für HashML-DSA zu, aufgrund von Implementierungskomplexitäten und reduzierter Sicherheit.

### Andere Spezifikationen

Die neue maximale Destination-Größe wird 2599 betragen (3468 in Base64).

Beachten Sie, dass wir Ed25519-Signierung von SU3-Dateien nicht zulassen, und obwohl wir Ed25519ph-Signierung definiert haben, haben wir uns nie auf eine OID dafür geeinigt oder sie verwendet.

- Wenn Nachricht 1 weniger als 919 Bytes hat, ist es das aktuelle ratchet-Protokoll.
- Wenn Nachricht 1 größer oder gleich 919 Bytes ist, ist es wahrscheinlich MLKEM512_X25519.
  Versuche zuerst MLKEM512_X25519, und falls es fehlschlägt, versuche das aktuelle ratchet-Protokoll.

## Overhead-Analyse

### Schlüsselaustausch

Die normalen Signaturtypen sind für SU3-Dateien nicht erlaubt; verwenden Sie die ph (prehash) Varianten.

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Die neue maximale Destination-Größe wird 2599 sein (3468 in Base64).

Aktualisiere andere Dokumente, die Anleitungen zu Destination-Größen geben, einschließlich:

| Typ | Relative Geschwindigkeit |
|------|----------------|
| X25519 DH/keygen | Basislinie |
| MLKEM512 | 2,25x schneller |
| MLKEM768 | 1,5x schneller |
| MLKEM1024 | 1x (gleich) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4,9x DH = 22% langsamer |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5,3x DH = 32% langsamer |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% langsamer |
Größenzunahme (Bytes):

| Typ | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | Baseline | Baseline | Baseline |
| MLKEM512 | 29x schneller | 22x schneller | 17x schneller |
| MLKEM768 | 17x schneller | 14x schneller | 9x schneller |
| MLKEM1024 | 12x schneller | 10x schneller | 6x schneller |
### Signaturen

#### Größen

Geschwindigkeiten wie von [Cloudflare](https://blog.cloudflare.com/pq-2024/) berichtet:

| Typ | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (jede Nachricht) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | Grundlinie | Grundlinie |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Geschwindigkeiten

Aktualisiere andere Dokumente, die Anleitungen zu Destination-Größen geben, einschließlich:

| Typ | Relatives Geschwindigkeitszeichen | verifizieren |
|-----|-----------------------------------|--------------|
| EdDSA_SHA512_Ed25519 | Ausgangswert | Ausgangswert |
| MLDSA44 | 5x langsamer | 2x schneller |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Größenzunahme (Bytes):

| Typ | Relatives Geschwindigkeitszeichen | Verifikation | Schlüsselgenerierung |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | Basislinie | Basislinie | Basislinie |
| MLDSA44 | 4,6x langsamer | 1,7x schneller | 2,6x schneller |
| MLDSA65 | 8,1x langsamer | gleich | 1,5x schneller |
| MLDSA87 | 11,1x langsamer | 1,5x langsamer | gleich |
## Sicherheitsanalyse

Typische Größen oder Größenzunahmen für Schlüssel, Signatur, RIdent, Dest (Ed25519 als Referenz enthalten), unter der Annahme des X25519-Verschlüsselungstyps für RIs. Hinzugefügte Größe für eine Router Info, LeaseSet, antwortfähige Datagramme und jedes der beiden aufgelisteten Streaming-Pakete (SYN und SYN ACK). Aktuelle Destinations und Leasesets enthalten wiederholtes Padding und sind während der Übertragung komprimierbar. Neue Typen enthalten kein Padding und werden nicht komprimierbar sein, was zu einer deutlich höheren Größenzunahme während der Übertragung führt. Siehe Design-Abschnitt oben.

| Kategorie | So sicher wie |
|----------|---------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Geschwindigkeiten wie von [Cloudflare](https://blog.cloudflare.com/pq-2024/) berichtet:

Vorläufige Testergebnisse in Java:

| Algorithmus | Sicherheitskategorie |
|-------------|---------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signaturen

NIST-Sicherheitskategorien sind in der [NIST-Präsentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) Folie 10 zusammengefasst. Vorläufige Kriterien: Unsere minimale NIST-Sicherheitskategorie sollte 2 für Hybridprotokolle und 3 für reine PQ-Protokolle sein.

Dies sind alles Hybrid-Protokolle. Implementierungen sollten MLKEM768 bevorzugen; MLKEM512 ist nicht sicher genug.

| Algorithmus | Sicherheitskategorie |
|-------------|---------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Typ-Einstellungen

NIST-Sicherheitskategorien [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Dieser Vorschlag definiert sowohl hybride als auch reine PQ-Signaturtypen. MLDSA44 hybrid ist MLDSA65 rein-PQ vorzuziehen. Die Schlüssel- und Signaturgrößen für MLDSA65 und MLDSA87 sind wahrscheinlich zu groß für uns, zumindest zunächst.

NIST-Sicherheitskategorien [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

Obwohl wir 3 Krypto- und 9 Signaturtypen definieren und implementieren werden, planen wir, die Leistung während der Entwicklung zu messen und die Auswirkungen vergrößerter Strukturgrößen weiter zu analysieren. Wir werden auch weiterhin Entwicklungen in anderen Projekten und Protokollen erforschen und beobachten.

Nach einem Jahr oder mehr der Entwicklung werden wir versuchen, einen bevorzugten Typ oder Standard für jeden Anwendungsfall festzulegen. Die Auswahl erfordert Kompromisse zwischen Bandbreite, CPU-Leistung und geschätztem Sicherheitsniveau. Möglicherweise sind nicht alle Typen für alle Anwendungsfälle geeignet oder erlaubt.

Die vorläufigen Präferenzen sind wie folgt und können sich ändern:

Verschlüsselung: MLKEM768_X25519

## Implementierungshinweise

### Bibliotheksunterstützung

Signatures: MLDSA44_EdDSA_SHA512_Ed25519

Vorläufige Einschränkungen sind wie folgt, vorbehaltlich Änderungen:

### Signatur-Varianten

Verschlüsselung: MLKEM1024_X25519 nicht erlaubt für SSU2

Signaturen: MLDSA87 und Hybrid-Variante wahrscheinlich zu groß; MLDSA65 und Hybrid-Variante möglicherweise zu groß

### Zuverlässigkeit

Die Bibliotheken Bouncycastle, BoringSSL und WolfSSL unterstützen jetzt MLKEM und MLDSA. OpenSSL-Unterstützung wird in ihrer Version 3.5 am 8. April 2025 verfügbar sein [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Strukturgrößen

Die von Java I2P angepasste Noise-Bibliothek von southernstorm.com enthielt vorläufige Unterstützung für hybride Handshakes, aber wir haben sie als ungenutzt entfernt; wir werden sie wieder hinzufügen und aktualisieren müssen, um der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) zu entsprechen.

### NetDB

Wir werden die "hedged" oder randomisierte Signaturvariante verwenden, nicht die "deterministische" Variante, wie in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Abschnitt 3.4 definiert. Dies stellt sicher, dass jede Signatur unterschiedlich ist, auch wenn sie über dieselben Daten erstellt wird, und bietet zusätzlichen Schutz gegen Seitenkanalangriffe. Obwohl [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) spezifiziert, dass die "hedged" Variante der Standard ist, kann dies in verschiedenen Bibliotheken der Fall sein oder auch nicht. Implementierer müssen sicherstellen, dass die "hedged" Variante für die Signaturerstellung verwendet wird.

### Ratchet

#### Probleme

Wir verwenden den normalen Signierungsprozess (genannt Pure ML-DSA Signature Generation), der die Nachricht intern als 0x00 || len(ctx) || ctx || message kodiert, wobei ctx ein optionaler Wert der Größe 0x00..0xFF ist. Wir verwenden keinen optionalen Kontext. len(ctx) == 0. Dieser Prozess ist definiert in [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 Schritt 10 und Algorithm 3 Schritt 5. Beachten Sie, dass einige veröffentlichte Testvektoren möglicherweise das Setzen eines Modus erfordern, bei dem die Nachricht nicht kodiert wird.

Eine Größenerhöhung führt zu deutlich mehr tunnel-Fragmentierung für NetDB-Speicherungen, Streaming-Handshakes und andere Nachrichten. Prüfen Sie auf Leistungs- und Zuverlässigkeitsänderungen.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Finden und überprüfen Sie jeglichen Code, der die Bytegröße von Router-Infos und leasesets begrenzt.

Überprüfen und möglicherweise reduzieren der maximalen LS/RI, die im RAM oder auf der Festplatte gespeichert werden, um den Speicherplatzzuwachs zu begrenzen. Mindestbandbreitenanforderungen für floodfills erhöhen?

- Mehr als ein MLKEM
- ElG + ein oder mehrere MLKEM
- X25519 + ein oder mehrere MLKEM
- ElG + X25519 + ein oder mehrere MLKEM

Eine automatische Klassifizierung/Erkennung mehrerer Protokolle auf denselben tunneln sollte basierend auf einer Längenprüfung von Nachricht 1 (New Session Message) möglich sein. Mit MLKEM512_X25519 als Beispiel ist Nachricht 1 um 816 Bytes größer als das aktuelle ratchet-Protokoll, und die minimale Größe von Nachricht 1 (mit nur einer DateTime-Nutzlast) beträgt 919 Bytes. Die meisten Nachricht-1-Größen mit aktuellem ratchet haben eine Nutzlast von weniger als 816 Bytes, sodass sie als nicht-hybrid ratchet klassifiziert werden können. Große Nachrichten sind wahrscheinlich POSTs, die selten sind.

- Noise Hash Auswahl - bei SHA256 bleiben oder upgraden?
  SHA256 sollte noch weitere 20-30 Jahre gut sein, nicht durch PQ bedroht,
  Siehe [NIST Präsentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) und [NCCOE Präsentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Falls SHA256 gebrochen wird, haben wir schlimmere Probleme (netdb).
- NTCP2 separater Port, separate router Adresse
- SSU2 relay / peer Test
- SSU2 Versionsfeld
- SSU2 router Adresse Version

Die empfohlene Strategie ist also:

Dies sollte es uns ermöglichen, Standard-Ratchet und Hybrid-Ratchet effizient auf derselben Destination zu unterstützen, genau wie wir zuvor ElGamal und Ratchet auf derselben Destination unterstützt haben. Daher können wir viel schneller zum MLKEM-Hybrid-Protokoll migrieren, als wenn wir keine Dual-Protokolle für dieselbe Destination unterstützen könnten, da wir MLKEM-Unterstützung zu bestehenden Destinations hinzufügen können.

Die erforderlichen unterstützten Kombinationen sind:

Die folgenden Kombinationen können komplex sein und müssen NICHT unterstützt werden, können aber implementierungsabhängig unterstützt werden:

#### Geteilte Tunnels

Wir werden möglicherweise nicht versuchen, mehrere MLKEM-Algorithmen (zum Beispiel MLKEM512_X25519 und MLKEM_768_X25519) am selben Ziel zu unterstützen. Wählen Sie nur einen aus; dies hängt jedoch davon ab, dass wir eine bevorzugte MLKEM-Variante auswählen, damit HTTP-Client-tunnel eine verwenden können. Implementierungsabhängig.

#### Größe der neuen Sitzung

Wir KÖNNEN versuchen, drei Algorithmen (zum Beispiel X25519, MLKEM512_X25519 und MLKEM769_X25519) für dasselbe Ziel zu unterstützen. Die Klassifizierung und Wiederholungsstrategie könnten zu komplex sein. Die Konfiguration und Benutzeroberfläche für die Konfiguration könnten zu komplex sein. Implementierungsabhängig.

### NTCP2

Wir werden wahrscheinlich NICHT versuchen, ElGamal und Hybrid-Algorithmen am selben Ziel zu unterstützen. ElGamal ist veraltet, und ElGamal + Hybrid allein (ohne X25519) macht nicht viel Sinn. Außerdem sind sowohl ElGamal- als auch Hybrid New Session Messages groß, sodass Klassifizierungsstrategien oft beide Entschlüsselungen versuchen müssten, was ineffizient wäre. Implementierungsabhängig.

#### Verschleierung

Clients können dieselben oder unterschiedliche X25519 statische Schlüssel für die X25519 und die hybriden Protokolle auf denselben tunnels verwenden, implementierungsabhängig.

Die ECIES-Spezifikation erlaubt Garlic Messages in der New Session Message-Nutzlast, was die 0-RTT-Übertragung des ersten Streaming-Pakets ermöglicht, normalerweise ein HTTP GET, zusammen mit dem leaseSet des Clients. Die New Session Message-Nutzlast hat jedoch keine Forward Secrecy. Da dieser Vorschlag verstärkte Forward Secrecy für ratchet betont, können oder sollten Implementierungen die Einbeziehung der Streaming-Nutzlast oder der vollständigen Streaming-Nachricht bis zur ersten Existing Session Message verschieben. Dies würde zu Lasten der 0-RTT-Übertragung gehen. Strategien können auch vom Traffic-Typ oder tunnel-Typ abhängen, oder von GET vs. POST, zum Beispiel. Implementierungsabhängig.

MLKEM, MLDSA oder beide auf demselben Ziel werden die Größe der New Session Message drastisch erhöhen, wie oben beschrieben. Dies kann die Zuverlässigkeit der Zustellung von New Session Messages durch tunnel erheblich verringern, wo sie in mehrere 1024 Byte tunnel-Nachrichten fragmentiert werden müssen. Der Zustellungserfolg ist proportional zur exponentiellen Anzahl der Fragmente. Implementierungen können verschiedene Strategien verwenden, um die Größe der Nachricht zu begrenzen, auf Kosten der 0-RTT-Zustellung. Implementierungsabhängig.

Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

### SSU2

Wir setzen das MSB des ephemeral key (key[31] & 0x80) in der Session-Anfrage, um anzuzeigen, dass dies eine Hybrid-Verbindung ist. Dies ermöglicht es uns, sowohl Standard-NTCP als auch Hybrid-NTCP auf demselben Port zu betreiben. Nur eine Hybrid-Variante würde unterstützt und in der Router-Adresse beworben werden. Zum Beispiel v=2,3 oder v=2,4 oder v=2,5.

Als Bob testen, ob (X[31] & 0x80) != 0 nach der Entschleierung. Falls ja, ist es eine PQ-Verbindung.

Hinweis: Typcodes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

## Router-Kompatibilität

### Transport-Namen

Die minimal erforderliche router-Version für NTCP2-PQ ist noch zu bestimmen.

### Router-Verschlüsselungstypen

Wir verwenden das Versionsfeld im langen Header und setzen es auf 3 für MLKEM512 und 4 für MLKEM768. v=2,3,4 in der Adresse wäre ausreichend.

#### Verschleierung

Überprüfen und verifizieren, dass SSU2 MLDSA-signierte RI handhaben kann, die über mehrere Pakete (6-8?) fragmentiert sind.

#### Typ 5/6/7 Router

Hinweis: Type-Codes sind nur für den internen Gebrauch bestimmt. Router bleiben Typ 4, und die Unterstützung wird in den router-Adressen angezeigt.

#### Typ 4 Router

Verwenden Sie in allen Fällen die NTCP2- und SSU2-Transportnamen wie gewohnt.

### Router Sig. Typen

#### Empfehlungen

Wir haben mehrere Alternativen zu berücksichtigen:

Nicht empfohlen. Verwenden Sie nur die oben aufgeführten neuen Transporte, die zum router-Typ passen. Ältere router können sich nicht verbinden, keine tunnel durch sie bauen oder netDb-Nachrichten an sie senden. Es würde mehrere Veröffentlichungszyklen dauern, um zu debuggen und die Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird. Könnte die Einführung um ein Jahr oder mehr gegenüber den unten genannten Alternativen verlängern.

### LS Verschlüsselungstypen

#### Typ 12-17 Router

Empfohlen. Da PQ den X25519 static key oder N handshake-Protokolle nicht beeinflusst, könnten wir die Router als Typ 4 belassen und nur neue Transporte bewerben. Ältere Router könnten sich weiterhin verbinden, tunnel durch sie bauen oder netDb-Nachrichten an sie senden.

MLKEM-768 wird für Ratchet, NTCP2 und SSU2 empfohlen, da es die beste Balance zwischen Sicherheit und Schlüssellänge bietet.

### Dest. Sig. Typen

#### Typ 5-7 LS Keys

Ältere router verifizieren RIs und können daher keine Verbindung aufbauen, Tunnel durch sie erstellen oder netDb-Nachrichten an sie senden. Würde mehrere Release-Zyklen benötigen, um zu debuggen und Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird. Wären die gleichen Probleme wie beim enc. type 5/6/7 Rollout; könnte den Rollout um ein Jahr oder mehr gegenüber der oben aufgeführten type 4 enc. type Rollout-Alternative verlängern.

Nicht empfohlen. Verwenden Sie nur die oben aufgeführten neuen Transporte, die zum router-Typ passen. Ältere router können sich nicht verbinden, keine tunnel durch sie bauen oder netDb-Nachrichten an sie senden. Es würde mehrere Veröffentlichungszyklen dauern, um zu debuggen und die Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird. Könnte die Einführung um ein Jahr oder mehr gegenüber den unten genannten Alternativen verlängern.

## Prioritäten und Einführung

Keine Alternativen.

Destinations können mehrere Schlüsseltypen unterstützen, aber nur durch das Durchführen von Probeentschlüsselungen von Nachricht 1 mit jedem Schlüssel. Der Overhead kann durch das Führen von Zählern erfolgreicher Entschlüsselungen für jeden Schlüssel gemildert werden, wobei der am häufigsten verwendete Schlüssel zuerst versucht wird. Java I2P verwendet diese Strategie für ElGamal+X25519 auf derselben Destination.

Router verifizieren leaseSet-Signaturen und können daher nicht verbinden oder leaseSets für Ziele vom Typ 12-17 empfangen. Es würde mehrere Release-Zyklen dauern, um zu debuggen und Unterstützung sicherzustellen, bevor es standardmäßig aktiviert wird.

Keine Alternativen.

Die wertvollsten Daten sind der End-to-End-Verkehr, verschlüsselt mit ratchet. Als externer Beobachter zwischen tunnel-Hops ist das zweimal zusätzlich verschlüsselt, mit tunnel-Verschlüsselung und Transport-Verschlüsselung. Als externer Beobachter zwischen OBEP und IBGW ist es nur einmal zusätzlich verschlüsselt, mit Transport-Verschlüsselung. Als OBEP- oder IBGW-Teilnehmer ist ratchet die einzige Verschlüsselung. Da tunnels jedoch unidirektional sind, würde das Abfangen beider Nachrichten im ratchet-Handshake kollaborierende router erfordern, es sei denn, tunnels wurden mit OBEP und IBGW auf demselben router aufgebaut.

Das PQ-Bedrohungsmodell, bei dem die Authentifizierungsschlüssel in einem angemessenen Zeitraum (sagen wir ein paar Monate) gebrochen und dann die Authentifizierung nachgeahmt oder nahezu in Echtzeit entschlüsselt wird, ist noch viel weiter entfernt? Und dann wäre der Zeitpunkt gekommen, zu PQC-statischen Schlüsseln zu migrieren.

Die Arbeit an der MLDSA-Signaturunterstützung in I2P ist bis Ende 2027 oder 2028 ausgesetzt, abhängig von der Arbeit der Standardisierungsgremien bei der Auswahl von Algorithmen, möglicher Reduzierung der Schlüssel- und/oder Signaturgrößen sowie der Förderung der Industrieakzeptanz. Siehe [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) und [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Außerdem wird die Einführung von MLDSA in der Industrie durch die IETF, den CA/Browser Forum und Zertifizierungsstellen standardisiert. Zertifizierungsstellen benötigen zunächst Unterstützung durch Hardware-Sicherheitsmodule (HSM), die derzeit nicht verfügbar ist [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Wir erwarten, dass die IETF und der CA/Browser Forum Entscheidungen über konkrete Parameterwahl vorantreiben, einschließlich der Frage, ob zusammengesetzte Signaturen unterstützt oder vorgeschrieben werden sollen [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Meilenstein | Ziel |
|-------------|------|
| Ratchet beta | Ende 2025 |
| Besten Verschlüsselungstyp auswählen | Anfang 2026 |
| NTCP2 beta | Anfang 2026 |
| SSU2 beta | Mitte 2026 |
| Ratchet Produktion | Mitte 2026 |
| Ratchet Standard | Ende 2026 |
| Signatur beta | Ende 2026 |
| NTCP2 Produktion | Ende 2026 |
| SSU2 Produktion | Anfang 2027 |
| Besten Signaturtyp auswählen | Anfang 2027 |
| NTCP2 Standard | Anfang 2027 |
| SSU2 Standard | Mitte 2027 |
| Signatur Produktion | Mitte 2027 |
## Migration

Ratchet hat die höchste Priorität. Transports sind als nächstes dran. Signatures haben die niedrigste Priorität.

Die Signatur-Einführung wird auch ein Jahr oder mehr später als die Verschlüsselungs-Einführung erfolgen, da keine Rückwärtskompatibilität möglich ist. Außerdem wird die MLDSA-Adoption in der Industrie vom CA/Browser Forum und den Certificate Authorities standardisiert werden. CAs benötigen zuerst Hardware Security Module (HSM) Unterstützung, die derzeit nicht verfügbar ist [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Wir erwarten, dass das CA/Browser Forum die Entscheidungen über spezifische Parameterwahlen vorantreibt, einschließlich ob zusammengesetzte Signaturen unterstützt oder gefordert werden [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## Probleme

SHA256 sollte noch weitere 20–30 Jahre sicher sein und ist nicht durch PQ bedroht. Siehe [NIST-Präsentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) und [NCCOE-Präsentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Falls SHA256 gebrochen wird, haben wir weitaus größere Probleme (netDb).

## Referenzen

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
