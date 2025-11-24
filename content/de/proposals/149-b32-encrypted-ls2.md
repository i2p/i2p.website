---
title: "B32 für verschlüsseltes LS2"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
---

## Hinweis
Netzwerkbereitstellung und -test in Arbeit.
Unterliegt geringfügigen Änderungen.
Siehe [SPEC](/docs/specs/b32-for-encrypted-leasesets/) für die offizielle Spezifikation.


## Übersicht

Standard Base 32 ("b32") Adressen enthalten den Hash des Ziels.
Dies funktioniert nicht für verschlüsseltes ls2 (Vorschlag 123).

Eine herkömmliche Base 32-Adresse kann nicht für ein verschlüsseltes LS2 (Vorschlag 123) verwendet werden,
da sie nur den Hash des Ziels enthält. Sie stellt nicht den nicht-verschleierten öffentlichen Schlüssel bereit.
Clients müssen den öffentlichen Schlüssel des Ziels, den Signaturtyp,
den verschleierten Signaturtyp und optional einen geheimen oder privaten Schlüssel kennen,
um das Leaseset abzurufen und zu entschlüsseln.
Daher reicht eine Base 32-Adresse allein nicht aus.
Der Client benötigt entweder das vollständige Ziel (das den öffentlichen Schlüssel enthält),
oder den öffentlichen Schlüssel selbst.
Wenn der Client das vollständige Ziel in einem Adressbuch hat und das Adressbuch
eine Rückwärtssuche nach Hash unterstützt, kann der öffentliche Schlüssel abgerufen werden.

Deshalb benötigen wir ein neues Format, das den öffentlichen Schlüssel statt des Hashes in
eine base32-Adresse einfügt. Dieses Format muss auch den Signaturtyp des
öffentlichen Schlüssels und den Signaturtyp des Verschleierungsschemas enthalten.

Dieser Vorschlag dokumentiert ein neues b32-Format für diese Adressen.
Während wir in Diskussionen auf dieses neue Format als "b33" Adresse verwiesen haben,
behält das tatsächliche neue Format das übliche ".b32.i2p" Suffix bei.

## Ziele

- Sowohl unverschleierte als auch verschleierte Signaturtypen einbeziehen, um zukünftige Verschleierungsschemata zu unterstützen
- Öffentliche Schlüssel unterstützen, die größer als 32 Bytes sind
- Sicherstellen, dass b32-Zeichen alle oder hauptsächlich zufällig sind, besonders am Anfang
  (wir möchten nicht, dass alle Adressen mit denselben Zeichen beginnen)
- Parsable
- Anzeigen, dass ein Verschleierungsgeheimnis und/oder ein pro-Client-Schlüssel erforderlich ist
- Prüfsumme hinzufügen, um Tippfehler zu erkennen
- Minimale Länge, Einhalten der maximalen DNS-Label-Länge von weniger als 63 Zeichen für den normalen Gebrauch
- Weiterhin base 32 für Unempfindlichkeit gegenüber Groß- und Kleinschreibung verwenden
- Beibehalten des üblichen ".b32.i2p"-Suffixes.

## Nicht-Ziele

- Keine Unterstützung für "private" Links, die ein Verschleierungsgeheimnis und/oder einen pro-Client-Schlüssel enthalten;
  dies wäre unsicher.


## Design

- Ein neues Format wird den unverschleierten öffentlichen Schlüssel, den unverschleierten Signaturtyp
  und den verschleierten Signaturtyp enthalten.
- Optional einen geheimen und/oder privaten Schlüssel enthalten, nur für private Links
- Verwendung des bestehenden ".b32.i2p"-Suffixes, jedoch mit längerer Länge.
- Eine Prüfsumme hinzufügen.
- Adressen für verschlüsselte Leasesets werden durch 56 oder mehr codierte Zeichen
  (35 oder mehr dekodierte Bytes) identifiziert, im Vergleich zu 52 Zeichen (32 Bytes) für herkömmliche Base 32-Adressen.


## Spezifikation

### Erstellung und Kodierung

Erstellen Sie einen Hostnamen aus {56+ Zeichen}.b32.i2p (35+ Zeichen in Binärform) wie folgt:

```text
Flagge (1 Byte)
    Bit 0: 0 für ein Byte Signaturtypen, 1 für zwei Byte Signaturtypen
    Bit 1: 0 für kein Geheimnis, 1 wenn ein Geheimnis erforderlich ist
    Bit 2: 0 für keine pro-Client-Authentifizierung,
           1 wenn ein privater Schlüssel des Clients erforderlich ist
    Bits 7-3: Ungenutzt, auf 0 gesetzt

  Public Key Signaturtyp (1 oder 2 Bytes wie in den Flags angegeben)
    Wenn 1 Byte, wird das obere Byte als null angenommen

  Verschlüsselte Schlüssel Signaturtyp (1 oder 2 Bytes wie in den Flags angegeben)
    Wenn 1 Byte, wird das obere Byte als null angenommen

  Öffentlicher Schlüssel
    Anzahl der Bytes wie durch den Signaturtyp impliziert
```

Nachbearbeitung und Prüfsumme:

```text
Erstelle die Binärdaten wie oben.
  Behandle die Prüfsumme als Little-Endian.
  Berechnen Prüfsumme = CRC-32(daten[3:end])
  daten[0] ^= (byte) prüfsumme
  daten[1] ^= (byte) (prüfsumme >> 8)
  daten[2] ^= (byte) (prüfsumme >> 16)

  hostname = Base32.encode(daten) || ".b32.i2p"
```

Alle ungenutzten Bits am Ende des b32 müssen 0 sein.
Es gibt keine ungenutzten Bits bei einer standardmäßigen 56 Zeichen (35 Byte) Adresse.


### Dekodierung und Verifizierung

```text
Entferne das ".b32.i2p" vom Hostnamen
  daten = Base32.decode(hostname)
  Berechne Prüfsumme = CRC-32(daten[3:end])
  Behandle die Prüfsumme als Little-Endian.
  flags = daten[0] ^ (byte) prüfsumme
  wenn 1 Byte Signaturtypen:
    public key sigtype = daten[1] ^ (byte) (prüfsumme >> 8)
    verschleierte Signaturtyp = daten[2] ^ (byte) (prüfsumme >> 16)
  ansonsten (2 Byte Signaturtypen) :
    public key sigtype = daten[1] ^ ((byte) (prüfsumme >> 8)) || daten[2] ^ ((byte) (prüfsumme >> 16))
    verschleierte Signaturtyp = daten[3] || daten[4]
  Analysiere den Rest basierend auf den Flags, um den öffentlichen Schlüssel zu erhalten
```


### Geheimnis- und Private Schlüssel-Bits

Die Geheimnis- und private Schlüssel-Bits werden verwendet, um Clients, Proxies oder andere
clientseitige Codes darauf hinzuweisen, dass das Geheimnis und/oder der private Schlüssel erforderlich sein wird,
um das Leaseset zu entschlüsseln. Bestimmte Implementierungen können den Benutzer dazu auffordern, die
erforderlichen Daten bereitzustellen, oder Verbindungsversuche ablehnen, wenn die erforderlichen Daten fehlen.


## Begründung

- XORing der ersten 3 Bytes mit dem Hash bietet eine begrenzte Prüfsummenfähigkeit,
  und stellt sicher, dass alle base32-Zeichen am Anfang zufällig sind.
  Nur wenige Flag- und Signaturtyp-Kombinationen sind gültig, sodass ein Tippfehler wahrscheinlich eine ungültige Kombination erzeugen und abgelehnt wird.
- Im üblichen Fall (1 Byte Signaturtypen, kein Geheimnis, keine pro-Client-Authentifizierung),
  wird der Hostname {56 Zeichen}.b32.i2p sein, dekodiert in 35 Bytes, wie bei Tor.
- Tors 2-Byte-Prüfsumme hat eine 1/64K False Negative Rate. Mit 3 Bytes, abzüglich einiger ignorierter Bytes,
  liegt unsere Annäherung bei 1 zu einer Million, da die meisten Flag-/Signaturtypkombinationen ungültig sind.
- Adler-32 ist eine schlechte Wahl für kleine Eingaben und zum Erkennen kleiner Änderungen.
  Verwenden Sie stattdessen CRC-32. CRC-32 ist schnell und weit verbreitet.

## Caching

Während dies nicht Teil dieses Vorschlags ist, müssen Router und/oder Clients die Zuordnung von
öffentlichem Schlüssel zu Ziel merken und cachen (vermutlich persistent), und umgekehrt.



## Hinweise

- Unterscheiden von alten und neuen Varianten durch Länge. Alte b32-Adressen sind immer {52 Zeichen}.b32.i2p. Neue sind {56+ Zeichen}.b32.i2p
- Tor-Diskussions-Thread: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- Erwarten Sie nicht, dass es jemals 2-Byte Signaturtypen geben wird, wir sind erst bei 13. Keine Implementierung jetzt notwendig.
- Neues Format kann, wenn gewünscht, in Sprunglinks verwendet werden (und von Sprungservern bedient), genau wie b32.


## Probleme

- Jede Geheimnis-, private Schlüssel- oder öffentlicher Schlüssel-Datenlänge, die länger als 32 Bytes wäre,
  würde die maximale DNS-Label-Länge von 63 Zeichen überschreiten. Browser kümmern sich wahrscheinlich nicht darum.


## Migration

Keine Probleme mit der Rückwärtskompatibilität. Längere b32-Adressen werden in alter Software
nicht in 32-Byte-Hashes umgewandelt.
