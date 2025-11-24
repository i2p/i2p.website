---
title: "ECIES-Tunnel"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Hinweis
Netzwerkbereitstellung und -tests laufen.
Unterliegt geringfügigen Änderungen.
Siehe [SPEC](/en/docs/spec/) für die offizielle Spezifikation.


## Übersicht

Dieses Dokument schlägt Änderungen an der Verschlüsselung von Tunnel-Bau-Nachrichten
mit kryptographischen Primitiven vor, die in [ECIES-X25519](/en/docs/spec/ecies/) eingeführt wurden.
Es ist ein Teil des Gesamtkonzepts
[Prop156](/en/proposals/156-ecies-routers/) zur Umstellung von Routern von ElGamal zu ECIES-X25519-Schlüsseln.

Für die Übergangsphase des Netzwerks von ElGamal + AES256 zu ECIES + ChaCha20
sind Tunnel mit gemischten ElGamal- und ECIES-Routern erforderlich.
Es werden Spezifikationen für den Umgang mit gemischten Tunnelhops bereitgestellt.
Es werden keine Änderungen am Format, der Verarbeitung oder der Verschlüsselung von ElGamal-Hops vorgenommen.

ElGamal-Tunnel-Ersteller müssen pro Hop ephemere X25519-Schlüsselpaaren erstellen und
dieser Spezifikation folgen, um Tunnel mit ECIES-Hops zu erstellen.

Dieser Vorschlag spezifiziert Änderungen, die für den ECIES-X25519-Tunnelbau erforderlich sind.
Für einen Überblick über alle Änderungen, die für ECIES-Router erforderlich sind, siehe Vorschlag 156 [Prop156](/en/proposals/156-ecies-routers/).

Dieser Vorschlag behält die gleiche Größe für Tunnel-Bau-Aufzeichnungen bei,
wie es für die Kompatibilität erforderlich ist. Kleinere Bauaufzeichnungen und Nachrichten werden
zu einem späteren Zeitpunkt umgesetzt - siehe [Prop157](/en/proposals/157-new-tbm/).


### Kryptographische Primitiven

Es werden keine neuen kryptographischen Primitiven eingeführt. Die für diesen Vorschlag erforderlichen Primitiven sind:

- AES-256-CBC wie in [Cryptography](/en/docs/spec/cryptography/)
- STREAM ChaCha20/Poly1305-Funktionen:
  ENCRYPT(k, n, plaintext, ad) und DECRYPT(k, n, ciphertext, ad) - wie in [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) und [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH-Funktionen - wie in [NTCP2](/en/docs/spec/ntcp2/) und [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - wie in [NTCP2](/en/docs/spec/ntcp2/) und [ECIES-X25519](/en/docs/spec/ecies/)

Andere an anderer Stelle definierte Noise-Funktionen:

- MixHash(d) - wie in [NTCP2](/en/docs/spec/ntcp2/) und [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - wie in [NTCP2](/en/docs/spec/ntcp2/) und [ECIES-X25519](/en/docs/spec/ecies/)


### Ziele

- Erhöhung der Geschwindigkeit von kryptographischen Operationen
- Ersetzung von ElGamal + AES256/CBC durch ECIES-Primitiven für Tunnel-Bau-Anfrage- und -Antwortaufzeichnungen
- Keine Änderung der Größe der verschlüsselten Bau-Anfrage- und -Antwortaufzeichnungen (528 Bytes) zur Kompatibilität
- Keine neuen I2NP-Nachrichten
- Beibehaltung der verschlüsselten Bauaufzeichnungsgröße zur Kompatibilität
- Hinzufügen von Forward Secrecy für Tunnel-Bau-Nachrichten
- Hinzufügen von authentifizierter Verschlüsselung
- Erkennung der Neuanordnung von Hops in Bau-Anfrageaufrufen
- Erhöhung der Zeitstempelauflösung, damit die Größe des Bloom-Filters reduziert werden kann
- Hinzufügen eines Feldes für den Tunnelauslauf, um variable Tunnellebensdauern zu ermöglichen (nur All-ECIES-Tunnel)
- Hinzufügen eines erweiterbaren Optionsfeldes für zukünftige Funktionen
- Wiederverwendung bestehender kryptographischer Primitiven
- Verbesserung der Sicherheit von Tunnel-Bau-Nachrichten, wo möglich, unter Beibehaltung der Kompatibilität
- Unterstützung von Tunneln mit gemischten ElGamal/ECIES-Peers
- Verbesserung der Verteidigung gegen "Tagging"-Angriffe auf Bau-Nachrichten
- Hops müssen den Verschlüsselungstyp des nächsten Hops nicht kennen, bevor die Bau-Nachricht verarbeitet wird, da sie zu diesem Zeitpunkt möglicherweise nicht die RI des nächsten Hops haben
- Maximierung der Kompatibilität mit dem aktuellen Netzwerk
- Keine Änderung der Tunnel-Bau-AES-Anforderungs-/Antwortverschlüsselung für ElGamal-Router
- Keine Änderung der Tunnel-AES-"Layer"-Verschlüsselung, siehe dafür [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Weiterhin Unterstützung sowohl für 8-Aufzeichnungs-TBM/TBRM als auch für variable Größe VTBM/VTBRM
- Kein "Flag Day"-Upgrade des gesamten Netzwerks erforderlich


### Nicht-Ziele

- Vollständige Neugestaltung der Bau-Nachrichten, die einen "Flag Day" erfordern würde
- Verkürzung von Tunnel-Bau-Nachrichten (erfordert All-ECIES-Hops und einen neuen Vorschlag)
- Verwendung von Tunnel-Bau-Optionen, wie in [Prop143](/en/proposals/143-build-message-options/) definiert, nur für kleine Nachrichten erforderlich
- Bidirektionale Tunnel - siehe dafür [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Kleinere Tunnel-Bau-Nachrichten - siehe dafür [Prop157](/en/proposals/157-new-tbm/)


## Bedrohungsmodell

### Designziele

- Keine Hops dürfen den Ursprung des Tunnels bestimmen können.

- Mittlere Hops dürfen weder die Richtung des Tunnels noch ihre Position im Tunnel bestimmen können.

- Keine Hops können Inhalte anderer Anfragen- oder Antwortaufrufe lesen, außer
  den verkürzten Router-Hash und den ephemeren Schlüssel für den nächsten Hop

- Kein Teilnehmer des Antworttunnels eines ausgehenden Baus kann Antwortaufrufe lesen.

- Kein Mitglied des ausgehenden Tunnels eines eingehenden Baus kann Anfragenaufrufe lesen,
  außer dass OBEP den verkürzten Router-Hash und den ephemeren Schlüssel für IBGW sehen kann




### Tagging-Angriffe

Ein Hauptziel des Tunnel-Bau-Designs ist es, es schwieriger zu machen,
für kolludierende Router X und Y zu wissen, dass sie sich in einem einzelnen Tunnel befinden.
Wenn sich Router X bei Hop m und Router Y bei Hop m+1 befindet, werden sie es offensichtlich wissen.
Aber wenn sich Router X bei Hop m und Router Y bei Hop m+n mit n>1 befindet, sollte dies viel schwieriger sein.

Tagging-Angriffe sind, wenn der Mittel-Hop-Router X die Tunnel-Bau-Nachricht so verändert,
dass der Router Y die Änderung erkennen kann, wenn die Bau-Nachricht dort ankommt.
Das Ziel ist, dass jede geänderte Nachricht von einem Hop zwischen X und Y gelöscht wird, bevor sie Router Y erreicht.
Bei Änderungen, die vor Router Y nicht gelöscht werden, sollte der Tunnel-Ersteller die Beschädigung in der Antwort erkennen
und den Tunnel verwerfen.

Mögliche Angriffe:

- Ändern eines Bauaufzeichnung
- Ersetzen eines Bauaufzeichnung
- Hinzufügen oder Entfernen eines Bauaufzeichnung
- Neuanordnung der Bauaufzeichnungen





TODO: Verhindert das aktuelle Design alle diese Angriffe?






## Design

### Noise-Protokoll-Framework

Dieser Vorschlag enthält die Anforderungen gemäß dem Noise-Protokoll-Framework
[NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11).
Im Noise-Jargon ist Alice der Initiator und Bob der Antwortende.

Dieser Vorschlag basiert auf dem Noise-Protokoll Noise_N_25519_ChaChaPoly_SHA256.
Dieses Noise-Protokoll verwendet folgende Primitiven:

- Einweg-Handshake-Muster: N
  Alice überträgt ihren statischen Schlüssel nicht an Bob (N)

- DH-Funktion: X25519
  X25519 DH mit einer Schlüssellänge von 32 Bytes wie in [RFC-7748](https://tools.ietf.org/html/rfc7748) angegeben.

- Cipher-Funktion: ChaChaPoly
  AEAD_CHACHA20_POLY1305 wie in [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8 spezifiziert.
  12-Byte-Nonce, wobei die ersten 4 Bytes auf Null gesetzt werden.
  Identisch mit dem in [NTCP2](/en/docs/spec/ntcp2/).

- Hash-Funktion: SHA256
  Standard 32-Byte-Hash, bereits umfassend in I2P verwendet.


Erweiterungen des Frameworks
``````````````````````````

Keine.


### Handshake-Muster

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload

Der Bauantrag ist identisch mit dem Noise-N-Muster.
Dies ist auch identisch mit der ersten (Session Request) Nachricht im XK-Muster, das in [NTCP2](/en/docs/spec/ntcp2/) verwendet wird.


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Anforderungsverschlüsselung

Bauanfrageaufzeichnungen werden vom Tunnel-Ersteller erstellt und asymmetrisch an den individuellen Hop verschlüsselt.
Diese asymmetrische Verschlüsselung von Anfragenaufzeichnungen ist derzeit ElGamal, wie in [Cryptography](/en/docs/spec/cryptography/) definiert,
und enthält eine SHA-256-Prüfsumme. Dieses Design ist nicht vorwärts-geheim.

Das neue Design verwendet das einseitige Noise-Muster "N" mit ephemeren-statischen DH von ECIES-X25519, mit einem HKDF, und
ChaCha20/Poly1305 AEAD für Vorwärts-Geheimheit, Integrität und Authentifizierung.
Alice ist die Tunnelbau-Anfrage-Stellerin. Jeder Hop im Tunnel ist ein Bob.


(Security-Eigenschaften der Payload)

  ```text

N:                      Authentifizierung   Vertraulichkeit
    -> e, es                  0                2

    Authentifizierung: Keine (0).
    Diese Payload könnte von jeder Partei, einschließlich eines aktiven Angreifers, gesendet worden sein.

    Vertraulichkeit: 2.
    Verschlüsselung an einen bekannten Empfänger, Vorwärts-Geheimnis nur bei Kompromittierung des Senders, anfällig für Wiederholung. Diese Payload ist nur auf der Grundlage von DHs
    verschlüsselt, die den statischen Schlüsselpaaren des Empfängers involvieren. Wenn der statische
    private Schlüssel des Empfängers kompromittiert wird, selbst zu einem späteren Zeitpunkt, kann diese Payload
    entschlüsselt werden. Diese Nachricht kann auch wiederholt werden, da es keinen
    ephemeren Beitrag vom Empfänger gibt.

    "e": Alice generiert ein neues ephemeres Schlüsselpaar und speichert es in der e
         Variable, schreibt den ephemeren öffentlichen Schlüssel als Klartext in den
         Nachrichtenpuffer und hasht den öffentlichen Schlüssel zusammen mit dem alten h, um einen neuen h abzuleiten.

    "es": Ein DH wird zwischen dem ephemeren Schlüsselpaar von Alice und dem
          statischen Schlüsselpaar von Bob durchgeführt. Das Ergebnis wird zusammen mit dem alten ck gehasht, um einen neuen ck und k abzuleiten, und n wird auf Null gesetzt.





  ```



### Antwortverschlüsselung

Bauantwortaufzeichnungen werden vom Ersteller und symmetrisch an den Ersteller verschlüsselt.
Diese symmetrische Verschlüsselung von Antwortaufzeichnungen ist derzeit AES mit einer vorangestellten SHA-256-Prüfsumme.
und enthält eine SHA-256-Prüfsumme. Dieses Design ist nicht vorwärts-geheim.

Das neue Design wird ChaCha20/Poly1305 AEAD für Integrität und Authentifizierung verwenden.


### Rechtfertigung

Der ephemere öffentliche Schlüssel in der Anfrage muss nicht mit AES
oder Elligator2 verschleiert werden. Der vorherige Hop ist der einzige, der ihn sehen kann, und dieser Hop
weiß, dass der nächste Hop ECIES ist.

Antwortaufzeichnungen benötigen keine vollständige asymmetrische Verschlüsselung mit einem weiteren DH.



## Spezifikation



### Bauanfrageaufzeichnungen

Verschlüsselte Bauanfrageaufzeichnungen sind sowohl für ElGamal als auch für ECIES 528 Bytes groß, um die Kompatibilität sicherzustellen.


Antragsruf unverschlüsselt (ElGamal)
`````````````````````````````````````````

Zum leichteren Verständnis, dies ist die aktuelle Spezifikation der Tunnel-Bauanfrageaufzeichnung für ElGamal-Router, entnommen aus [I2NP](/en/docs/spec/i2np/).
Die unverschlüsselten Daten werden mit einem nicht-Null-Byte vorangestellt und dem SHA-256-Hash der Daten vor der Verschlüsselung,
wie in [Cryptography](/en/docs/spec/cryptography/) definiert.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 222 Bytes

  ```dataspec


bytes     0-3: tunnel ID zum Empfang von Nachrichten, nicht null
  bytes    4-35: lokale Router-Identitätshaush
  bytes   36-39: nächste Tunnel-ID, nicht null
  bytes   40-71: nächste Router-Identitätshaush
  bytes  72-103: AES-256-Tunnellage-Schlüssel
  bytes 104-135: AES-256-Tunnel-IV-Schlüssel
  bytes 136-167: AES-256-Antwort-Schlüssel
  bytes 168-183: AES-256-Antwort-IV
  byte      184: flags
  bytes 185-188: Anfragezeit (in Stunden seit dem Epochenbeginn, abgerundet)
  bytes 189-192: nächste Nachrichten-ID
  bytes 193-221: nicht interpretierter / zufälliger Puffer




  ```


Antragsruf verschlüsselt (ElGamal)
`````````````````````````````````````

Zum leichteren Verständnis, dies ist die aktuelle Spezifikation der Tunnel-Bauanfrageaufzeichnung für ElGamal-Router, entnommen aus [I2NP](/en/docs/spec/i2np/).

Verschlüsselte Größe: 528 Bytes

  ```dataspec


bytes    0-15: gekürztes Identitätshaush des Hops
  bytes  16-528: ElGamal verschlüsselte Bauanfrageaufzeichnung




  ```




Antragsruf unverschlüsselt (ECIES)
```````````````````````````````````````

Dies ist die vorgeschlagene Spezifikation der Tunnel-Bauanfrageaufzeichnung für ECIES-X25519-Router.
Zusammenfassung der Änderungen:

- Entfernen des ungenutzten 32-Byte-Router-Hashs
- Änderungsanfragezeit von Stunden zu Minuten
- Hinzufügen eines Expirationsfelds für zukünftige variable Tunnelzeit
- Mehr Platz für Flags hinzufügen
- Zuordnung für zusätzliche Bauoptionen hinzufügen
- AES-256-Antwort-Schlüssel und IV werden für die eigene Antwort-Aufzeichnung des Hops nicht verwendet
- Unverschlüsselte Aufzeichnung ist länger, da es weniger Verschlüsselungsoverhead gibt


Die Antragsaufzeichnung enthält keine ChaCha-Antwortschlüssel.
Diese Schlüssel werden aus einem KDF gewonnen. Siehe unten.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 464 Bytes

  ```dataspec


bytes     0-3: tunnel ID zum Empfang von Nachrichten, nicht null
  bytes     4-7: nächste Tunnel-ID, nicht null
  bytes    8-39: nächste Router-Identitätshaush
  bytes   40-71: AES-256-Tunnellage-Schlüssel
  bytes  72-103: AES-256-Tunnel-IV-Schlüssel
  bytes 104-135: AES-256-Antwort-Schlüssel
  bytes 136-151: AES-256-Antwort-IV
  byte      152: flags
  bytes 153-155: mehr flags, unbenutzt, auf 0 gesetzt für Kompatibilität
  bytes 156-159: Anfragezeit (in Minuten seit dem Epochenbeginn, abgerundet)
  bytes 160-163: Anfrageablauf (in Sekunden seit Erstellung)
  bytes 164-167: nächste Nachrichten-ID
  bytes   168-x: Tunnel-Bau-Optionen (Zuordnung)
  bytes     x-x: andere Daten, wie durch Flags oder Optionen impliziert
  bytes   x-463: zufälliger Puffer




  ```

Das Flags-Feld ist das gleiche wie in [Tunnel-Creation](/en/docs/spec/tunnel-creation/) definiert und enthält folgende::

 Bit-Reihenfolge: 76543210 (Bit 7 ist das MSB)
 bit 7: wenn gesetzt, Nachrichten von jedem zulassen
 bit 6: wenn gesetzt, Nachrichten an jeden zulassen, und die Antwort an den
        angegebenen nächsten Hop in einer Tunnel-Bau-Antwortnachricht senden
 bits 5-0: undefiniert, muss auf 0 gesetzt werden für Kompatibilität mit zukünftigen Optionen

Bit 7 zeigt an, dass der Hop ein Eingangsgateway (IBGW) sein wird. Bit 6
zeigt an, dass der Hop ein Ausgangspunkt (OBEP) sein wird. Wenn weder das eine noch das andere gesetzt ist,
wird der Hop ein Zwischen-Teilnehmer sein. Beide können nicht gleichzeitig gesetzt sein.

Die Anfrageablauf ist für zukünftige variable Tunneldauer.
Gegenwärtig wird nur der Wert 600 (10 Minuten) unterstützt.

Die Tunnel-Bau-Optionen sind eine Zuordnung, wie in [Common](/en/docs/spec/common-structures/) definiert.
Dies ist für zukünftige Verwendung. Keine Optionen sind derzeit definiert.
Wenn die Zuordnung leer ist, sind dies zwei Bytes 0x00 0x00.
Die maximale Größe der Zuordnung (einschließlich der Längenfelder) beträgt 296 Bytes,
und der maximale Wert des Längenfeldes der Zuordnung beträgt 294.



Antragsruf verschlüsselt (ECIES)
`````````````````````````````````````

Alle Felder sind Big-Endian, außer dem ephemeren öffentlichen Schlüssel, der Little-Endian ist.

Verschlüsselte Größe: 528 Bytes

  ```dataspec


bytes    0-15: gekürztes Identitätshaush des Hops
  bytes   16-47: ephemerer X25519-öffentlicher Schlüssel des Senders
  bytes  48-511: mit ChaCha20 verschlüsselte Bauanfrageaufzeichnung
  bytes 512-527: Poly1305 MAC




  ```



### Bauantwortaufzeichnungen

Verschlüsselte Bauantwortaufzeichnungen sind sowohl für ElGamal als auch für ECIES 528 Bytes groß, um die Kompatibilität sicherzustellen.


Antwortaufzeichnung unverschlüsselt (ElGamal)
`````````````````````````````````````
ElGamal-Antworten werden mit AES verschlüsselt.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 528 Bytes

  ```dataspec


bytes   0-31: SHA-256-Hash von Bytes 32-527
  bytes 32-526: zufällige Daten
  byte     527: antwort

  Gesamtlänge: 528




  ```


Antwortaufzeichnung unverschlüsselt (ECIES)
`````````````````````````````````````
Dies ist die vorgeschlagene Spezifikation der Tunnel-Bauantwortaufzeichnung für ECIES-X25519-Router.
Zusammenfassung der Änderungen:

- Hinzufügen einer Zuordnung für Bauantwortoptionen
- Unverschlüsselte Aufzeichnung ist länger, da es weniger Verschlüsselungsoverhead gibt

ECIES-Antworten werden mit ChaCha20/Poly1305 verschlüsselt.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 512 Bytes

  ```dataspec


bytes    0-x: Tunnel-Bau-Antwortoptionen (Zuordnung)
  bytes    x-x: andere Daten, wie durch Optionen impliziert
  bytes  x-510: zufälliger Puffer
  byte     511: Antwort-Byte




  ```

Die Tunnel-Bau-Antwortoptionen sind eine Zuordnung, wie in [Common](/en/docs/spec/common-structures/) definiert.
Dies ist für zukünftige Verwendung. Keine Optionen sind derzeit definiert.
Wenn die Zuordnung leer ist, sind dies zwei Bytes 0x00 0x00.
Die maximale Größe der Zuordnung (einschließlich der Längenfelder) beträgt 511 Bytes,
und der maximale Wert des Längenfeldes der Zuordnung beträgt 509.

Das Antwort-Byte ist einer der folgenden Werte
wie in [Tunnel-Creation](/en/docs/spec/tunnel-creation/) definiert, um Fingerabdrücke zu vermeiden:

- 0x00 (akzeptieren)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Antwortaufzeichnung verschlüsselt (ECIES)
```````````````````````````````````

Verschlüsselte Größe: 528 Bytes

  ```dataspec


bytes   0-511: mit ChaCha20 verschlüsselte Bauantwortaufzeichnung
  bytes 512-527: Poly1305 MAC




  ```

Nach dem vollständigen Übergang zu ECIES-Aufzeichnungen gelten die gleichen Regeln für die Bereichspufferung wie für Anfragenaufzeichnungen.


### Symmetrische Verschlüsselung von Aufzeichnungen

Gemischte Tunnel sind zulässig und notwendig für den Übergang von ElGamal zu ECIES.
Während der Übergangsphase wird eine zunehmende Anzahl von Routern unter ECIES-Schlüsseln sein.

Die symmetrische Kryptographie-Vorverarbeitung wird folgendermaßen ablaufen:

- "Verschlüsselung":

  - Cipher im Entschlüsselungsmodus ausführen
  - Anforderungsaufzeichnungen werden in der Vorverarbeitung proaktiv entschlüsselt (verbergen von verschlüsselten Anforderungsaufzeichnungen)

- "Entschlüsselung":

  - Cipher im Verschlüsselungsmodus ausführen
  - Anforderungsaufzeichnungen werden durch Teilnehmerhops verschlüsselt (Offenlegung der nächsten Klartext-Anforderungsaufzeichnung)

- ChaCha20 hat keine "Modi", wird aber einfach dreimal ausgeführt:

  - einmal in der Vorverarbeitung
  - einmal durch den Hop
  - einmal bei der endgültigen Antwortverarbeitung

Wenn gemischte Tunnel verwendet werden, müssen Tunnel-Ersteller die symmetrische Verschlüsselung
der Bauanfrageaufzeichnung auf den Verschlüsselungstyp des aktuellen und vorherigen Hops stützen.

Jeder Hop wird seinen eigenen Verschlüsselungstyp für die Verschlüsselung von Bauantwortaufzeichnungen und den anderen
Aufzeichnungen in der VariableTunnelBuildMessage (VTBM) verwenden.

Auf dem Antwortpfad muss der Endpunkt (Sender) die [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) Schritt-für-Schritt-Verschlüsselung rückgängig machen, wobei jeder Hop seinen Antwortschlüssel verwendet.

Als erläuterndes Beispiel, betrachten wir einen ausgehenden Tunnel mit ECIES, umgeben von ElGamal:

- Sender (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Alle Bauanfrageaufzeichnungen sind im verschlüsselten Zustand (mit ElGamal oder ECIES).

Der AES256/CBC-Cipher, wenn er verwendet wird, wird weiterhin für jede Aufzeichnung verwendet, ohne dass er über mehrere Aufzeichnungen hinweg verkettet wird.

Ebenso wird ChaCha20 verwendet, um jede Aufzeichnung zu verschlüsseln, nicht streaming über die gesamte VTBM.

Die Anforderungsaufzeichnungen werden vom Sender (OBGW) vorverarbeitet:

- Die Aufzeichnung von H3 wird unter Verwendung von "verschlüsselt":

  - H2's Antwortschlüssel (ChaCha20)
  - H1's Antwortschlüssel (AES256/CBC)

- Die Aufzeichnung von H2 wird unter Verwendung von "verschlüsselt":

  - H1's Antwortschlüssel (AES256/CBC)

- Die Aufzeichnung von H1 wird ohne symmetrische Verschlüsselung ausgegeben

Nur H2 überprüft das Antwortverschlüsselungs-Flag und sieht, dass es durch AES256/CBC gefolgt wird.

Nachdem jeder Hop die Aufzeichnungen bearbeitet hat, befinden sich die Aufzeichnungen im entschlüsselten Zustand:

- Die Aufzeichnung von H3 wird unter Verwendung von "entschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)

- Die Aufzeichnung von H2 wird unter Verwendung von "entschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20-Poly1305)

- Die Aufzeichnung von H1 wird unter Verwendung von "entschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20)
  - H1's Antwortschlüssel (AES256/CBC)

Der Tunnel-Ersteller, auch bekannt als Eingangsendpunkt (IBEP), nachbearbeitet die Antwort:

- Die Aufzeichnung von H3 wird unter Verwendung von "verschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)

- Die Aufzeichnung von H2 wird unter Verwendung von "verschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20-Poly1305)

- Die Aufzeichnung von H1 wird unter Verwendung von "verschlüsselt":

  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20)
  - H1's Antwortschlüssel (AES256/CBC)


### Anforderungsaufzeichnungs-Schlüssel (ECIES)

Diese Schlüssel sind explizit in ElGamal-Bauanfrageaufzeichnungen enthalten.
Für ECIES-Bauanfrageaufzeichnungen sind die Tunnelschlüssel und AES-Antwortschlüssel enthalten,
aber die ChaCha-Antwortschlüssel werden aus dem DH-Austausch abgeleitet.
Siehe [Prop156](/en/proposals/156-ecies-routers/) für Details zu den statischen ECIES-Router-Schlüsseln.

Unten ist eine Beschreibung, wie die zuvor in Anforderungsaufzeichnungen übertragenen Schlüssel abgeleitet werden.


KDF für Initial ck und h
````````````````````````

Dies ist standardmäßiger [NOISE](https://noiseprotocol.org/noise.html) für das Muster "N" mit einem standardisierten Protokollnamen.

  ```text

Dies ist das "e"-Nachrichtenmuster:

  // Protokollname festlegen.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 Bytes, US-ASCII-kodiert, keine NULL-Terminierung).

  // Hash h definieren = 32 Bytes
  // Auf 32 Bytes auffüllen. Nicht hashen, da es nicht mehr als 32 Bytes sind.
  h = protocol_name || 0

  Definiere ck = 32-Byte-Verschlüsselungs-Schlüssel. Kopiere die h-Daten zu ck.
  Setze chainKey = h

  // MixHash(null-Prolog)
  h = SHA256(h);

  // bis hierhin kann alles von allen Routern vorkalkuliert werden.




  ```


KDF für Anwendungsaufzeichnung
````````````````````````````````

ElGamal-Tunnel-Ersteller generieren ein ephemeres X25519-Schlüsselpaar für jeden
ECIES-Hop im Tunnel und verwenden das oben beschriebene Schema für die Verschlüsselung ihrer Bauanfrageaufzeichnung.
ElGamal-Tunnel-Ersteller verwenden das vor dieser Spezifikation definierte Schema für die Verschlüsselung zu ElGamal-Hops.

ECIES-Tunnel-Ersteller müssen zu jedem der ElGamal-Hop-öffentlichen Schlüssel unter Verwendung
des in [Tunnel-Creation](/en/docs/spec/tunnel-creation/) definierten Schemas verschlüsseln. ECIES-Tunnel-Ersteller werden das oben beschriebene Schema zur Verschlüsselung an ECIES-Hops verwenden.

Das bedeutet, dass Tunnel-Hops nur verschlüsselte Aufzeichnungen mit ihrem eigenen Verschlüsselungstyp sehen werden.

Für ElGamal- und ECIES-Tunnel-Ersteller werden sie eindeutige ephemere X25519-Schlüsselpaaren
pro Hop für die Verschlüsselung an ECIES-Hops erzeugen.

**WICHTIG**:
Ephemere Schlüssel müssen eindeutig pro ECIES-Hop und pro Bauaufzeichnung sein.
Das Nichtverwendung einzigartiger Schlüssel öffnet einen Angriffsvektor, mit dem kolludierende Hops bestätigen können, dass sie sich im gleichen Tunnel befinden.


  ```dataspec


// Jedes Hop's X25519 statisches Schlüsselpaar (hesk, hepk) von der Router-Identität
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || unten bedeutet anhängen
  h = SHA256(h || hepk);

  // bis hierhin, kann alles von jedem Router vorkalkuliert werden
  // für alle eingehenden Bauanfragen

  // Sender generiert ein X25519 ephemeres Schlüsselpaar pro ECIES-Hop in der VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Ende des "e"-Nachrichtenmusters.

  Dies ist das "es"-Nachrichtenmuster:

  // Noise es
  // Absender führt ein X25519 DH mit dem statischen öffentlichen Schlüssel des Hops durch.
  // Jeder Hop sucht die Aufzeichnung mit seinem gekürzten Identitätshaush,
  // und extrahiert den ephemeren Schlüssel des Senders, der der verschlüsselten Aufzeichnung vorausgeht.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly Parameter verschlüsseln/entschlüsseln
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Für Antwortaufzeichnungs-KDF speichern
  chainKey = keydata[0:31]

  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  plaintext = 464-Byte-Bauanfragendaten
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Ende des "es"-Nachrichtenmusters.

  // MixHash(ciphertext)
  // Für Antwortaufzeichnungs-KDF speichern
  h = SHA256(h || ciphertext)





  ```

``replyKey``, ``layerKey`` und ``layerIV`` müssen weiterhin in ElGamal-Aufzeichnungen enthalten sein
und können zufällig generiert werden.


### Anforderungsaufzeichnungs-Verschlüsselung (ElGamal)

Wie in [Tunnel-Creation](/en/docs/spec/tunnel-creation/) definiert.
Es gibt keine Änderungen an der Verschlüsselung für ElGamal-Hops.




### Antwortaufzeichnungs-Verschlüsselung (ECIES)

Die Antwortaufzeichnung ist ChaCha20/Poly1305-verschlüsselt.

  ```dataspec


// AEAD-Parameter
  k = chainkey aus der Bauanfrage
  n = 0
  plaintext = 512-Byte-Bauantwortdaten
  ad = h aus der Bauanfrage

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### Antwortaufzeichnungs-Verschlüsselung (ElGamal)

Wie in [Tunnel-Creation](/en/docs/spec/tunnel-creation/) definiert.
Es gibt keine Änderungen an der Verschlüsselung für ElGamal-Hops.



### Sicherheitsanalyse

ElGamal bietet keine Vorwärtsgeheimnis für Tunnel-Bau-Nachrichten.

AES256/CBC steht in etwas besserem Ruf, da es nur einem theoretischen Abschwächung durch einen
bekannten Klartext 'biclique'-Angriff ausgesetzt ist.

Der einzige bekannte praktische Angriff gegen AES256/CBC ist ein Padding-Orakel-Angriff, wenn der IV dem Angreifer bekannt ist.

Ein Angreifer müsste die ElGamal-Verschlüsselung des nächsten Hops durchbrechen, um die AES256/CBC-Schlüsselinformationen (Antwortschlüssel und IV) zu erhalten.

ElGamal ist deutlich CPU-intensiver als ECIES, was zu einer potenziellen Ressourcenauslastung führen kann.

ECIES, verwendet mit neuen ephemeren Schlüsseln pro Bauanfrageaufzeichnung oder VariableTunnelBuildMessage, bietet Vorwärtsgeheimnis.

ChaCha20Poly1305 bietet AEAD-Verschlüsselung, die es dem Empfänger ermöglicht, die Nachrichtenintegrität zu überprüfen, bevor der Versuch der Entschlüsselung unternommen wird.


## Begründung

Dieses Design maximiert die Wiederverwendung bestehender kryptographischer Primitiven, Protokolle und Codes.
Dieses Design minimiert das Risiko.




## Implementierungshinweise

* Ältere Router überprüfen nicht den Verschlüsselungstyp des Hops und werden ElGamal-verschlüsselte
  Aufzeichnungen senden. Einige neuere Router sind fehlerhaft und werden verschiedene Arten von fehlerhaften Aufzeichnungen senden.
  Implementierer sollten diese Aufzeichnungen erkennen und vor dem DH-Vorgang ablehnen, wenn möglich, um den CPU-Verbrauch zu reduzieren.


## Probleme



## Migration

Siehe [Prop156](/en/proposals/156-ecies-routers/).



