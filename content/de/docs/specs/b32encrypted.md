---
title: "B32 für verschlüsselte leaseSets"
description: "Base-32-Adressformat für verschlüsselte LS2 leaseSets"
slug: "b32encrypted"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implementiert"
---

## Übersicht

Standard-Base-32 ("b32")-Adressen enthalten den Hash des Ziels. Dies funktioniert für verschlüsselte LS2 (LeaseSet2, neues leaseSet-Format; proposal 123) nicht.

Wir können für ein verschlüsseltes LS2 (proposal 123) keine traditionelle Base32-Adresse verwenden, da sie nur den Hash der Destination (Zieladresse) enthält. Sie liefert nicht den nicht-verblindeten öffentlichen Schlüssel. Clients müssen den öffentlichen Schlüssel der Destination, den Signaturtyp, den verblindeten Signaturtyp sowie ein optionales Secret (geheime Zeichenfolge) oder einen privaten Schlüssel kennen, um den leaseset abzurufen und zu entschlüsseln. Daher reicht eine Base32-Adresse allein nicht aus. Der Client benötigt entweder die vollständige Destination (die den öffentlichen Schlüssel enthält) oder den öffentlichen Schlüssel allein. Wenn der Client die vollständige Destination in einem Adressbuch hat und das Adressbuch einen Reverse-Lookup anhand des Hashes unterstützt, kann der öffentliche Schlüssel abgerufen werden.

Dieses Format setzt den öffentlichen Schlüssel anstelle des Hashes in eine Base32-Adresse. Dieses Format muss außerdem den Signaturtyp des öffentlichen Schlüssels und den Signaturtyp des Blinding-Verfahrens enthalten.

Dieses Dokument spezifiziert ein b32-Format für diese Adressen. Obwohl wir dieses neue Format in Diskussionen als "b33"-Adresse bezeichnet haben, behält das tatsächliche neue Format das übliche Suffix ".b32.i2p" bei.

## Implementierungsstatus

Vorschlag 123 (Neue netDB-Einträge) wurde in Version 0.9.43 (Oktober 2019) vollständig implementiert. Der verschlüsselte Funktionsumfang von LS2 (LeaseSet2, der zweite LeaseSet-Typ) ist bis einschließlich Version 2.10.0 (September 2025) stabil geblieben, ohne inkompatible Änderungen am Adressierungsformat oder an den kryptografischen Spezifikationen.

Wichtige Implementierungsmeilensteine: - 0.9.38: Floodfill-Unterstützung für Standard-LS2 mit Offline-Schlüsseln - 0.9.39: RedDSA-Signaturtyp 11 und grundlegende Verschlüsselung/Entschlüsselung - 0.9.40: Vollständige Unterstützung der B32-Adressierung (Proposal 149) - 0.9.41: X25519-basierte Authentifizierung pro Client - 0.9.42: Alle Blinding-Funktionen (Verblindung) betriebsbereit - 0.9.43: Vollständige Implementierung bekanntgegeben (Oktober 2019)

## Entwurf

- Das neue Format enthält den nicht verblindeten öffentlichen Schlüssel, den nicht verblindeten Signaturtyp und den verblindeten Signaturtyp.
- Gibt optional Anforderungen an Secret (gemeinsam genutztes Geheimnis) und/oder privaten Schlüssel für private Links an.
- Verwendet die vorhandene Endung ".b32.i2p", jedoch mit größerer Gesamtlänge.
- Enthält eine Prüfsumme zur Fehlererkennung.
- Adressen für verschlüsselte leaseSets werden anhand von 56 oder mehr kodierten Zeichen (35 oder mehr dekodierten Bytes) identifiziert, gegenüber 52 Zeichen (32 Bytes) bei traditionellen Base32-Adressen.

## Spezifikation

### Erstellung und Kodierung

Erstellen Sie einen Hostnamen der Form {56+ Zeichen}.b32.i2p (35+ Zeichen in Binärdarstellung) wie folgt:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Nachverarbeitung und Prüfsumme:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Alle ungenutzten Bits am Ende des b32 müssen 0 sein. Für eine Standardadresse mit 56 Zeichen (35 Byte) gibt es keine ungenutzten Bits.

### Dekodierung und Verifikation

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits geheimer und privater Schlüssel

Die Bits für den geheimen und den privaten Schlüssel werden verwendet, um Clients, Proxys oder anderem clientseitigen Code anzuzeigen, dass der geheime und/oder der private Schlüssel zum Entschlüsseln des leaseSet erforderlich sein wird. Bestimmte Implementierungen können den Benutzer auffordern, die erforderlichen Daten bereitzustellen, oder Verbindungsversuche ablehnen, wenn die erforderlichen Daten fehlen.

Diese Bits dienen lediglich als Indikatoren. Der geheime bzw. private Schlüssel darf niemals in der B32-Adresse selbst enthalten sein, da dies die Sicherheit gefährden würde.

## Kryptografische Details

### Verblindungsverfahren

Das Blinding-Verfahren verwendet RedDSA (Signaturschema) basierend auf Ed25519 und dem ZCash-Design und erzeugt Red25519-Signaturen über der Ed25519-Kurve unter Verwendung von SHA-512. Dieser Ansatz stellt sicher, dass geblendete öffentliche Schlüssel in der Untergruppe mit Primzahlordnung verbleiben und vermeidet die in einigen alternativen Designs vorhandenen Sicherheitsbedenken.

Verblindete Schlüssel rotieren täglich basierend auf dem UTC-Datum nach der Formel:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
Der Speicherort in der DHT (verteilte Hashtabelle) wird wie folgt berechnet:

```
SHA256(type_byte || blinded_public_key)
```
### Verschlüsselung

Das verschlüsselte leaseset verwendet die Stromchiffre ChaCha20 für die Verschlüsselung, die aufgrund ihrer überlegenen Leistung auf Geräten ohne AES-Hardwarebeschleunigung ausgewählt wurde. Die Spezifikation setzt HKDF zur Schlüsselableitung und X25519 für Diffie-Hellman-Operationen ein.

Verschlüsselte leaseSets haben eine dreischichtige Struktur: - Äußere Schicht: Metadaten im Klartext - Mittlere Schicht: Client-Authentifizierung (DH- oder PSK-Methoden) - Innere Schicht: eigentliche LS2-Daten mit Lease-Informationen

### Authentifizierungsmethoden

Die Client-spezifische Authentifizierung unterstützt zwei Methoden:

**DH-Authentifizierung**: Verwendet X25519 als Schlüsselaustauschverfahren. Jeder autorisierte Client übermittelt seinen öffentlichen Schlüssel an den Server, und der Server verschlüsselt die mittlere Schicht mithilfe eines aus ECDH abgeleiteten gemeinsamen Geheimnisses.

**PSK-Authentifizierung**: Verwendet Pre-Shared Keys (vorab geteilte Schlüssel) direkt zur Verschlüsselung.

Flag-Bit 2 in der B32-Adresse gibt an, ob eine clientbezogene Authentifizierung erforderlich ist.

## Zwischenspeicherung

Obwohl dies außerhalb des Geltungsbereichs dieser Spezifikation liegt, müssen router und Clients die Zuordnung vom öffentlichen Schlüssel zur Destination (Zielidentität) und umgekehrt speichern und zwischenspeichern (persistente Speicherung wird empfohlen).

Der Blockfile-Namensdienst, I2Ps standardmäßiges Adressbuchsystem seit Version 0.9.8, verwaltet mehrere Adressbücher mit einer dedizierten reverse-lookup map (Abbildung für Rückwärtssuche), die schnelle Abfragen nach Hash ermöglicht. Diese Funktionalität ist entscheidend für die Auflösung eines verschlüsselten leaseSet, wenn anfangs nur ein Hash bekannt ist.

## Signaturtypen

Seit I2P Version 2.10.0 sind die Signaturtypen 0 bis 11 definiert. Die Ein-Byte-Codierung bleibt der Standard, während die Zwei-Byte-Codierung zwar verfügbar ist, in der Praxis jedoch nicht verwendet wird.

**Häufig verwendete Typen:** - Typ 0 (DSA_SHA1): Veraltet für routers, unterstützt für Destinations (Zieladressen) - Typ 7 (EdDSA_SHA512_Ed25519): Aktueller Standard für router-Identitäten und Destinations - Typ 11 (RedDSA_SHA512_Ed25519): Ausschließlich für verschlüsselte LS2 leasesets mit Unterstützung für blinding (Adressverschleierung)

**Wichtiger Hinweis**: Nur Ed25519 (Typ 7) und Red25519 (Typ 11) unterstützen das für verschlüsselte leaseSets notwendige blinding (Verblindung). Andere Signaturtypen können mit dieser Funktion nicht verwendet werden.

Typen 9–10 (GOST-Algorithmen) bleiben reserviert, sind aber nicht implementiert. Die Typen 4–6 und 8 sind für Offline-Signaturschlüssel als "offline only" gekennzeichnet.

## Hinweise

- Alte und neue Varianten anhand der Länge unterscheiden. Alte b32-Adressen sind immer {52 chars}.b32.i2p. Neue sind {56+ chars}.b32.i2p
- Die base32-Codierung folgt den Vorgaben von RFC 4648; die Dekodierung ist groß-/kleinschreibungsunabhängig, und eine Ausgabe in Kleinbuchstaben wird bevorzugt
- Adressen können über 200 Zeichen lang sein, wenn Signaturtypen mit größeren öffentlichen Schlüsseln verwendet werden (z. B. ECDSA P521 mit 132-Byte-Schlüsseln)
- Das neue Format kann in jump links (Sprung-Links) verwendet werden (und von jump servers (Sprung-Servern) bereitgestellt werden), falls gewünscht, genau wie Standard-b32
- Verblindete Schlüssel rotieren täglich basierend auf dem UTC-Datum, um die Privatsphäre zu verbessern
- Dieses Format weicht von dem in Tors rend-spec-v3.txt, Anhang A.2, beschriebenen Ansatz ab, der potenzielle Sicherheitsimplikationen bei off-curve (außerhalb der Kurve) verblindeten öffentlichen Schlüsseln hat

## Versionskompatibilität

Diese Spezifikation ist für I2P Version 0.9.47 (August 2020) bis einschließlich Version 2.10.0 (September 2025) zutreffend. Während dieses Zeitraums gab es keine inkompatiblen Änderungen am B32-Adressformat, an der verschlüsselten LS2-Struktur oder an den kryptografischen Implementierungen. Alle mit 0.9.47 erstellten Adressen bleiben mit den aktuellen Versionen vollständig kompatibel.

## Referenzen

**CRC-32** - [CRC-32 (Wikipedia)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Prüfsumme des Stream Control Transmission Protocol](https://tools.ietf.org/html/rfc3309)

**I2P-Spezifikationen** - [Spezifikation für verschlüsseltes LeaseSet](/docs/specs/encryptedleaseset/) - [Vorschlag 123: Neue netDB-Einträge](/proposals/123-new-netdb-entries/) - [Vorschlag 149: B32 für verschlüsseltes LS2](/proposals/149-b32-encrypted-ls2/) - [Spezifikation gemeinsamer Strukturen](/docs/specs/common-structures/) - [Namensauflösung und Adressbuch](/docs/overview/naming/)

**Tor-Vergleich** - [Tor-Diskussionsthread (Designkontext)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Weitere Ressourcen** - [I2P-Projekt](/) - [I2P-Forum](https://i2pforum.net) - [Java-API-Dokumentation](http://docs.i2p-projekt.de/javadoc/)
