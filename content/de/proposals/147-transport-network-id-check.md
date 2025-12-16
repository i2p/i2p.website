---
title: "Transportnetzwerk-ID-Prüfung"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Übersicht

NTCP2 (Vorschlag 111) lehnt Verbindungen von unterschiedlichen Netzwerk-IDs
in der Session Request-Phase nicht ab.
Die Verbindung muss derzeit in der Session Confirmed-Phase abgelehnt werden,
wenn Bob Alices RI überprüft.

Ähnlich verhält es sich bei SSU, das Verbindungen von unterschiedlichen Netzwerk-IDs
in der Session Request-Phase nicht ablehnt.
Die Verbindung muss derzeit nach der Session Confirmed-Phase abgelehnt werden,
wenn Bob Alices RI überprüft.

Dieser Vorschlag ändert die Session Request-Phase beider Transportprotokolle, um die Netzwerk-ID einzubeziehen, auf eine rückwärtskompatible Weise.

## Motivation

Verbindungen aus dem falschen Netzwerk sollten so schnell wie möglich abgelehnt und der Absender auf eine schwarze Liste gesetzt werden.

## Ziele

- Verhinderung der Kreuzkontamination von Testnetzen und geforkten Netzwerken

- Hinzufügen der Netzwerk-ID zum NTCP2- und SSU-Handshake

- Für NTCP2,
  der Empfänger (eingehende Verbindung) sollte in der Lage sein zu erkennen, dass die Netzwerk-ID unterschiedlich ist, damit er die IP des Peers auf eine schwarze Liste setzen kann.

- Für SSU,
  der Empfänger (eingehende Verbindung) kann in der Session Request-Phase keine schwarze Liste führen, da die eingehende IP gefälscht sein könnte. Es reicht aus, die Kryptographie des Handshakes zu ändern.

- Verhinderung des Resamplings vom falschen Netzwerk

- Muss rückwärtskompatibel sein

## Nicht-Ziele

- NTCP 1 wird nicht mehr verwendet und wird daher nicht geändert.

## Design

Für NTCP2,
würde das XORen eines Wertes nur dazu führen, dass die Verschlüsselung fehlschlägt, und der Empfänger hätte nicht genug Informationen, um den Absender auf eine schwarze Liste zu setzen, daher wird dieser Ansatz nicht bevorzugt.

Für SSU,
werden wir die Netzwerk-ID irgendwo in der Session Request XORen.
Da dies rückwärtskompatibel sein muss, werden wir (id - 2) XORen,
damit es für den aktuellen Netzwerk-ID-Wert von 2 keine Auswirkung hat.

## Spezifikation

### Dokumentation

Fügen Sie die folgende Spezifikation für gültige Netzwerk-ID-Werte hinzu:

| Nutzung | NetID-Nummer |
|-------|--------------|
| Reserviert | 0 |
| Reserviert | 1 |
| Aktuelles Netzwerk (Standard) | 2 |
| Reservierte zukünftige Netzwerke | 3 - 15 |
| Forks und Testnetzwerke | 16 - 254 |
| Reserviert | 255 |

Die Java I2P-Konfiguration, um den Standard zu ändern, lautet "router.networkID=nnn".
Dokumentieren Sie dies besser und ermutigen Sie Forks und Testnetzwerke, diese Einstellung in ihre Konfiguration aufzunehmen.
Ermutigen Sie andere Implementierungen, diese Option zu implementieren und zu dokumentieren.

### NTCP2

Verwenden Sie das erste reservierte Byte der Optionen (Byte 0) in der Session Request-Nachricht, um die Netzwerk-ID zu enthalten, derzeit 2.
Es enthält die Netzwerk-ID.
Wenn es ungleich null ist, soll der Empfänger gegen das am wenigsten signifikante Byte der lokalen Netzwerk-ID prüfen.
Wenn sie nicht übereinstimmen, soll der Empfänger sofort die Verbindung trennen und die IP des Absenders auf eine schwarze Liste setzen.

### SSU

Für SSU, fügen wir ein XOR von ((netid - 2) << 8) in die HMAC-MD5-Berechnung ein.

Bestehende:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' bedeutet anfügen und '^' bedeutet exklusiv-oder.
  payloadLength ist ein 2-Byte-unsigned-Integer
  protocolVersion ist ein Byte 0x00
```

Neue:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' bedeutet anfügen, '^' bedeutet exklusiv-oder, '<<' bedeutet Linksschiebe.
  payloadLength ist ein zwei Byte langer unsigned-Integer, Big Endian
  protocolVersion ist zwei Byte 0x0000, Big Endian
  netid ist ein zwei Byte langer unsigned-Integer, Big Endian, zulässige Werte sind 2-254
```

### Resampling

Fügen Sie einen Parameter ?netid=nnn zum Abruf der reseed su3-Datei hinzu.
Aktualisieren Sie die reseed-Software, um auf die netid zu prüfen. Wenn sie vorhanden ist und nicht gleich "2", sollte der Abruf mit einem Fehlercode abgelehnt werden, vielleicht 403.
Fügen Sie eine Konfigurationsoption zur reseed-Software hinzu, damit eine alternative netid für Test- oder geforkte Netzwerke konfiguriert werden kann.

## Anmerkungen

Wir können Testnetzwerke und Forks nicht dazu zwingen, die Netzwerk-ID zu ändern.
Das Beste, was wir tun können, ist Dokumentation und Kommunikation.
Wenn wir Kreuzkontaminationen mit anderen Netzwerken entdecken, sollten wir versuchen,
die Entwickler oder Betreiber zu kontaktieren, um die Wichtigkeit der Änderung der Netzwerk-ID zu erklären.

## Probleme

## Migration

Dies ist rückwärtskompatibel für den aktuellen Netzwerk-ID-Wert von 2.
Falls Personen Netzwerke (Test oder andere) mit einem anderen Netzwerk-ID-Wert betreiben,
ist diese Änderung rückwärts-inkompatibel.
Wir sind jedoch nicht darüber informiert, dass dies jemand tut.
Wenn es sich nur um ein Testnetzwerk handelt, ist es kein Problem, alle Router auf einmal zu aktualisieren.
