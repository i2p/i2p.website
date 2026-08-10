---
title: "Schnelle Erweiterung (BEP 6) Ermöglicht schnelles Herunterladen mit Ziel-Hash-Peer-Identität"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Entwurf"
toc: true
---

## Übersicht

BEP 6 (Fast Extension) umfasst fünf Funktionen: **Have All / Have None**, **Reject Requests**, **Suggestions** und **Allowed Fast**. Das Wire-Protokoll — Aushandlungsbit, Nachrichten-IDs und Choke-Semantik — ist transportunabhängig und funktioniert unverändert über I2P-Streaming. Der einzige Teil von BEP 6, der nicht direkt auf I2P abgebildet werden kann, ist die **Allowed Fast Set Generation**, da diese anhand der IPv4-Adresse des Peers definiert ist. I2P-Peers besitzen keine IPs; sie werden durch 32-Byte lange Destination-Hashes identifiziert.

Dieser Vorschlag standardisiert die Erzeugung eines I2P-internen „Allowed Fast“-Sets, sodass alle I2P-Torrent-Clients für denselben Peer und dieselbe Torrent *identische* erlaubte Fast-Sets generieren, wodurch die Funktion zwischen verschiedenen Implementierungen nützlich (und überprüfbar) wird.

## Motivation

Neue Peers benötigen die ersten paar Teile, bevor das Tauschprinzip (tit-for-tat) von BitTorrent richtig in Schwung kommt. Auf I2P verläuft dieser Anstieg langsamer als im Klarnetz: Die Verbindungseinrichtung und die Übergabe von Teilen durchlaufen mehrere Hops über Tunnels mit hoher Latenz, wodurch das Zeitfenster zwischen Verbindungsaufbau und erster gegenseitiger Freigabe (unchoke) länger wird. „Allowed Fast“ greift dieses Zeitfenster direkt an – einem neu startenden Peer wird eine kleine Anzahl von Teilen erlaubt, selbst wenn er noch gedrosselt (choked) ist, sodass er sofort Daten erhält und früher mit dem Gegentausch beginnen kann.

Das Referenz-BEP 6 berechnet die erlaubte Fast-Set-Auswahl anhand der IPv4-Adresse des Peers, um sicherzustellen, dass der *Absender* Stücke auswählen kann, die für den *Empfänger* eindeutig sind (ein Benutzer mit vielen IPs kann nicht viele Sätze sammeln). Unter I2P übernimmt der Ziel-Hash des Peers dieselbe Bindungsfunktion und ist für beide Enden jeder Verbindung verfügbar, wodurch die Auswahl deterministisch und *lokal überprüfbar* wird – eine Eigenschaft, die das IP-basierte Verfahren nicht bieten kann.

## Änderungen an BEP 6

Die Verhandlung der Fast Extension und alle vier Nachrichtentypen werden unverändert übernommen:

- Verhandlung: drittes niederwertigste Bit des letzten reservierten Bytes, `reserved[7] |= 0x04`, beide Enden
- Have All `<len=0x0001><op=0x0E>`, Have None `<len=0x0001><op=0x0F>`
- Vorschlag Stück `<len=0x0005><op=0x0D><index>`
- Ablehnung der Anfrage `<len=0x000D><op=0x10><index><begin><length>`
- Erlaubt Schnell `<len=0x0005><op=0x11><index>`
- Jede Anfrage führt genau zu einer Antwort (Stück oder Ablehnung); Choke lehnt nicht mehr implizit ausstehende Anfragen ab

Die einzige Abweichung liegt bei der Erzeugung des Allowed-Fast-Sets, bei dem die IP-Bytes durch Bytes des Ziel-Hashs des Peers ersetzt werden.

### Abweichung: Hash-Bytes anstelle der maskierten IP

Siehe BEP 6, Schritt (1):

```
x = 0xFFFFFF00 & ip
```
Das nimmt drei Bytes der IPv4-Adresse des Peers und **setzt das 4. Byte auf Null**. Dies ist eine Subnetz-Heuristik: Benutzer, die mehrere IPs im selben /24-Netz erhalten können, sollten nicht mehrere erlaubte Fast-Sets erhalten.

Unsere I2P-Version ersetzt dies durch die ersten vier Bytes des 32-Byte-Destinations-Hashs des Peers:

```
x = first 4 bytes of peer destination hash
```
Der Unterschied zur Referenzimplementierung:

> „Das sind 3 Bytes der IP, gefolgt von einer Null. Du bist 4 Bytes des Hashs. Es unterscheidet sich von BEP 6, weil dort keine IP vorhanden ist und das 4. Byte nicht auf Null gesetzt wird.“

Beide Enden einer I2P-Verbindung kennen bereits den Ziel-Hash des Peers (dies ist die Adresse, zu der die Verbindung aufgebaut wurde), weshalb kein zusätzlicher Austausch, keine NAT-Erkennung und keine externe IP-Erkennung erforderlich sind – nichts davon existiert in I2P.

### Erlaubter schneller Generierungsalgorithmus

Sei `hash` der 32-Byte lange Ziel-Hash des empfangenden Peers, `infohash` der 20-Byte lange Infohash des Torrents, `sz` die Anzahl der Teile im Torrent, `k` die endgültige Anzahl der Teile in der erlaubten Fast-Set (10, wie in BEP 6), und `a` die Ausgabe-Menge:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Hinweise:

- 4 Bytes des Ziel-Hash ersetzen die 3 maskierten IP-Bytes. Alle vier Bytes tragen 
  Hash-Entropie; keines wird auf null gesetzt.
- Wie in BEP 6 erzeugt die SHA1-Kette eine lange, pseudorandomartige Sequenz, die in 
  Segmentindizes unterteilt ist; `k = 10` entspricht dem Referenzstandardwert.
- Die Allowed-Fast-Nachricht ist nur ein Hinweis: Der Empfänger DARF sie nicht so interpretieren, 
  dass der Sender das Segment besitzt – lediglich, dass der Sender das Segment senden wird, während er gedrosselt ist.

## Vorteile

| Bereich            | Vorteil                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Start-Latenz       | Neue Peers laden die ersten Stücke bereits während des Choking, wodurch die langsameren Tit-for-Tat-Anfangsphase über mehrhüpfige I2P-Tunnel verkürzt wird                                       |
| Determinismus      | Die Menge ist eine reine Funktion aus Ziel-Hash + Infohash, sodass jede Implementierung dieselbe Menge berechnet – anders als bei IP-basiertem BEP 6, wo die Sicht des Senders auf die IP des Empfängers abweichen kann (NAT) |
| Überprüfbarkeit    | Der empfangende Peer kennt seinen eigenen Ziel-Hash und kann die Menge lokal neu berechnen und überprüfen, wodurch fehlerhafte Sender erkannt werden können                                       |
| Keine IP-Technik   | Kein NAT-Traversieren, keine External-IP-Ermittlung oder Subnet-Heuristiken – alles Dinge, die auf I2P unmöglich oder bedeutungslos sind                                                      |
| Identitätsbindung  | Nur eine schnelle Menge pro Ziel erlaubt. Ein Nutzer mit vielen Zielen erhält jeweils eine eigene Menge – dieselbe Anti-Gaming-Eigenschaft, die die IP-Maske im Klarnetz bietet                     |
| Datenschutz        | Es wird niemals eine IP-Adresse übertragen oder in der Berechnung impliziert                                                                                                                   |
| Bandbreite         | „Have All“ / „Have None“ ersetzt den vollständigen Bitfeld-Status bei großen Torrents; „Reject“ beseitigt redundante Neuanfragen                                                               |
## Implementierungsüberlegungen

- **Peer-Identität**: Der Ziel-Hash des Peers wird aus der Streaming-Verbindung abgeleitet (das Ziel der Sitzung) und ist für beide Enden identisch. Bei ausgehenden Verbindungen verwende das Ziel, mit dem verbunden wurde; bei eingehenden Verbindungen das Ziel, von dem die Verbindung stammt.
- **Verhandlung**: Sende `reserved[7] |= 0x04` im Handshake; sende Fast Extension-Nachrichten nur, wenn der Peer im Handshake ebenfalls das Bit gesetzt hat; falls ein Peer Fast Extension-Nachrichten ohne vorherige Vereinbarung sendet, schließe die Verbindung.
- **Have All / Have None**: Sende unmittelbar nach dem Handshake genau eine der Nachrichten Bitfeld / Have All / Have None. Verwende Have All für Seeds, Have None bis zum ersten Stück.
- **Allowed Fast (Sendeseite)**: Werbe nur Stücke an, die du tatsächlich besitzt; der Empfänger darf diese auch bei unterdrückter Übertragung (choked) anfordern. Begrenze die *angebotene* Menge (z. B. lehne Allowed-Fast-Anfragen von einem Peer ab, der bereits mehr als `k` Stücke besitzt, gemäß BEP 6 Empfehlung).
- **Allowed Fast (Empfangsseite)**: Speichere die Menge; erlaube Anfragen für diese Stücke auch bei unterdrückter Übertragung; optional kann die Menge verifiziert werden, indem sie aus deinem eigenen Ziel-Hash und dem Info-Hash neu berechnet wird; ignoriere Stücke, die nicht in der berechneten Menge liegen.
- **Reject**: Jede Anfrage muss genau eine Antwort erhalten; bei Unterdrückung (choke) lehne alle Anfragen ab, die nicht im Allowed-Fast-Set liegen, anstatt den Peer stumm zu ignorieren.
- **Größe der Menge**: Verwende `k = 10` zur Kompatibilität; Peers dürfen unter Last einen niedrigeren `k`-Wert wählen, aber beide Seiten sollten nur das bewerben, was sie tatsächlich bereitstellen.
- **Stückgrenze**: `index = y % sz` muss die Gesamtanzahl der Stücke des Torrents (`sz`) verwenden; ignoriere Indizes ≥ sz (zur Sicherheit), da eine Hashkette nicht pro Stückbereich begrenzt ist.
- **Abwärtskompatibilität**: Clients, die das Fast-Bit nicht aushandeln, erhalten diese Nachrichten einfach nie; keine weiteren Protokolländerungen sind erforderlich.

## Referenzimplementierungen

Der Algorithmus ist klein und eigenständig – nur ein paar Dutzend Zeilen in jeder beliebigen Sprache. Alle drei Beispiele unten berechnen für identische Eingaben dieselbe Menge (`hash[0:4] ++ infohash`, SHA1-Kette, `y % sz`, mit `k = 10`).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Kompatibilität

- **Drahtkompatibel**: das Aushandlungsbit und die Nachrichtenformate sind byte-identisch mit dem Clearnet-BEP 6; nur die Eingabe für die Set-Generierung unterscheidet sich.
- **Nicht interoperabel über Netzwerke hinweg**: Ein I2P-Client und ein Clearnet-Client können ohnehin nicht miteinander verbinden; die Abweichung betrifft nur die Peer-Identitäts-Bytes, niemals das Drahtformat.
- **Innerhalb von I2P**: Jeder Client, der diesen Vorschlag implementiert, berechnet identische erlaubte Fast-Sets und kann diese wechselseitig bereitstellen und überprüfen. Clients, die „Allowed Fast“ ignorieren, behandeln es einfach als eine nicht verbindliche Empfehlung und verlieren lediglich den Startvorteil.

## Offene Fragen

1. Sollte die Set-Größe `k` bei 10 festgehalten werden oder lastadaptiv sein (z. B. kleiner bei starker Anfragebelastung), wie BEP 6 erlaubt?
2. Sollten Empfänger das Set gegenüber ihrem eigenen Ziel-Hash überprüfen und Indizes verwerfen, die nicht übereinstimmen (Schutz gegen fehlerhafte oder bösartige Sender)? Empfohlen: Ja.
3. Den 4-Byte-*Präfix* (Bytes 0–3) wählen, wie gezeigt, oder die *letzten* 4 Bytes – jedes feste 4-Byte-Fenster ergibt dieselben Eigenschaften; der Präfix behält die natürliche Byte-Reihenfolge des Referenzcodes bei (`hash[0:4]`).

## Stand der Technik

- Referenz: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- Referenzimplementierung in I2PSnark: `PeerState.sendAllowedFast()` /
  `generateAllowedFastSet()` in
  `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@seit 0.9.71+)
- Funktioniert zusammen mit BEP 40 (kanonische Peer-Priorität) und BEP 21 (teilweise Seeds), beide werden von I2PSnark unterstützt
