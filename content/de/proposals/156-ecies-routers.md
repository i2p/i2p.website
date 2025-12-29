---
title: "ECIES-Router"
nummer: "156"
autor: "zzz, original"
erstellt: "2020-09-01"
zuletzt aktualisiert: "2025-03-05"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2950"
zielversion: "0.9.51"
toc: true
---

## Hinweis
Netzwerkbereitstellung und -test in Arbeit.
Änderungen vorbehalten.
Status:

- ECIES-Router implementiert ab 0.9.48, siehe [Common](/docs/specs/common-structures/).
- Tunnelaufbau implementiert ab 0.9.48, siehe [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- Verschlüsselte Nachrichten an ECIES-Router implementiert ab 0.9.49, siehe [ECIES-ROUTERS](/docs/specs/ecies/).
- Neue Tunnel-Build-Nachrichten implementiert ab 0.9.51.


## Übersicht


### Zusammenfassung

Router-Identitäten enthalten derzeit einen ElGamal-Verschlüsselungsschlüssel.
Dies war seit den Anfängen von I2P der Standard.
ElGamal ist langsam und muss an allen Stellen, an denen es verwendet wird, ersetzt werden.

Die Vorschläge für LS2 [Prop123](/proposals/123-new-netdb-entries/) und ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
(jetzt spezifiziert in [ECIES](/docs/specs/ecies/)) definierten den Ersatz von ElGamal durch ECIES
für Destinationen.

Dieser Vorschlag definiert den Ersatz von ElGamal durch ECIES-X25519 für Router.
Dieser Vorschlag bietet einen Überblick über die notwendigen Änderungen.
Die meisten Details finden sich in anderen Vorschlägen und Spezifikationen.
Siehe den Referenzabschnitt für Links.


### Ziele

Siehe [Prop152](/proposals/152-ecies-tunnels/) für zusätzliche Ziele.

- Ersetze ElGamal durch ECIES-X25519 in Router-Identitäten
- Wiederverwendung vorhandener kryptografischer Primitive
- Verbesserung der Sicherheit von Tunnelaufbau-Nachrichten, wo möglich, bei gleichzeitiger Wahrung der Kompatibilität
- Unterstützung von Tunneln mit gemischten ElGamal/ECIES-Peers
- Maximierung der Kompatibilität mit dem aktuellen Netzwerk
- Kein Upgrade des gesamten Netzwerks am "Flag Day" erforderlich
- Schrittweise Einführung zur Risikominimierung
- Neue, kleinere Tunnelaufbau-Nachricht


### Nicht-Ziele

Siehe [Prop152](/proposals/152-ecies-tunnels/) für zusätzliche Nicht-Ziele.

- Keine Anforderungen für Dual-Key-Router
- Schichtverschlüsselungsänderungen, hierzu siehe [Prop153](/proposals/153-chacha20-layer-encryption/)


## Design


### Schlüsselposition und Kryptotyp

Für Destinationen befindet sich der Schlüssel im Leaseset, nicht in der Destination, und
wir unterstützen mehrere Verschlüsselungstypen im selben Leaseset.

All das ist für Router nicht erforderlich. Der Verschlüsselungsschlüssel des Routers
befindet sich in seiner Router-Identität. Siehe die Spezifikation der allgemeinen Strukturen [Common](/docs/specs/common-structures/).

Für Router ersetzen wir den 256 Byte ElGamal-Schlüssel in der Router-Identität
durch einen 32 Byte X25519-Schlüssel und 224 Byte Padding.
Dies wird durch den Kryptotyp im Schlüsselzertifikat angezeigt.
Der Kryptotyp (wie im LS2 verwendet) ist 4.
Dies zeigt einen Little-Endian-32-Byte-X25519-Public-Key an.
Dies ist die Standardkonstruktion, wie sie in der Spezifikation der allgemeinen Strukturen definiert ist [Common](/docs/specs/common-structures/).

Dies ist identisch mit der Methode, die für ECIES-P256
für Kryptotypen 1-3 im Vorschlag 145 [Prop145](/proposals/145-ecies/) vorgeschlagen wurde.
Obwohl dieser Vorschlag nie angenommen wurde, bereiteten sich die Entwickler der Java-Implementierung vor,
indem sie an mehreren Stellen in der Codebasis Prüfungen hinzufügten. Die meisten dieser Arbeiten wurden Mitte 2019 abgeschlossen.


### Tunnelaufbau-Nachricht

Um ECIES anstelle von ElGamal zu verwenden, sind mehrere Änderungen an der Tunnel-Erstellungsspezifikation [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
erforderlich. Darüber hinaus werden wir Verbesserungen an den Tunnelaufbau-Nachrichten vornehmen,
um die Sicherheit zu erhöhen.

In Phase 1 werden wir das Format und die Verschlüsselung der
Build-Request-Record und Build-Response-Record für ECIES-Schritte ändern.
Diese Änderungen sind mit vorhandenen ElGamal-Routern kompatibel.
Diese Änderungen sind in Vorschlag 152 [Prop152](/proposals/152-ecies-tunnels/) definiert.

In Phase 2 fügen wir eine neue Version der
Build-Request-Message, Build-Reply-Message,
Build-Request-Record und Build-Response-Record hinzu.
Die Größe wird zur Effizienzreduzierung verkleinert.
Diese Änderungen müssen von allen Schritten in einem Tunnel unterstützt werden, und alle Schritte müssen ECIES sein.
Diese Änderungen sind in Vorschlag 157 [Prop157](/proposals/157-new-tbm/) definiert.


### End-to-End-Verschlüsselung

#### Geschichte

Im ursprünglichen Design von Java I2P gab es einen einzigen ElGamal-Session-Key-Manager (SKM),
der vom Router und all seinen lokalen Destinationen gemeinsam genutzt wurde.
Da ein gemeinsamer SKM Informationen durchsickern konnte und Korrelationen durch Angreifer ermöglichte,
wurde das Design geändert, um separate ElGamal-SKM für den Router und jede Destination zu unterstützen.
Das ElGamal-Design unterstützte nur anonyme Absender;
der Absender sendete nur einmalige Schlüssel, keinen statischen Schlüssel.
Die Nachricht war nicht an die Identität des Absenders gebunden.

Dann entwarfen wir den ECIES-Ratchet-SKM in
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/), jetzt spezifiziert in [ECIES](/docs/specs/ecies/).
Dieses Design wurde unter Verwendung des Noise "IK"-Musters spezifiziert, das den statischen Schlüssel des Absenders in der ersten Nachricht einschloss. Dieses Protokoll wird für ECIES (Typ 4) Destinationen verwendet.
Das IK-Muster erlaubt keine anonymen Absender.

Daher nahmen wir in den Vorschlag eine Möglichkeit auf, auch anonyme Nachrichten
an einen Ratchet-SKM zu senden, indem ein nullgefüllter statischer Schlüssel verwendet wird. Dies simulierte ein Noise "N"-Muster,
jedoch auf eine kompatible Weise, sodass ein ECIES-SKM sowohl anonyme als auch nicht-anonyme Nachrichten empfangen konnte.
Die Absicht war es, den Nullschlüssel für ECIES-Router zu verwenden.


#### Anwendungsfälle und Bedrohungsmodelle

Der Anwendungsfall und das Bedrohungsmodell für Nachrichten, die an Router gesendet werden, unterscheiden sich wesentlich von
denen für End-to-End-Nachrichten zwischen Destinationen.


Anwendungsfall und Bedrohungsmodell der Destination:

- Nicht-anonym von/zu Destinationen (Absender schließt statischen Schlüssel ein)
- Effiziente Unterstützung von anhaltendem Datenverkehr zwischen Destinationen (voller Handshake, Streaming und Tags)
- Immer durch ausgehende und eingehende Tunnel gesendet
- Verbergen alle identifizierenden Merkmale vor OBEP und IBGW, was Elligator2-Codierung von Ephermeralschlüsseln erfordert.
- Beide Teilnehmer müssen denselben Verschlüsselungstyp verwenden


Anwendungsfall und Bedrohungsmodell des Routers:

- Anonyme Nachrichten von Routern oder Destinationen (Absender schließt keinen statischen Schlüssel ein)
- Nur für verschlüsselte Datenbankabfragen und -speicherungen, in der Regel für Floodfills
- Gelegentliche Nachrichten
- Mehrere Nachrichten sollten nicht korreliert werden
- Immer durch ausgehenden Tunnel direkt zu einem Router gesendet. Keine eingehenden Tunnel verwendet
- OBEP weiß, dass es die Nachricht an einen Router weiterleitet und kennt dessen Verschlüsselungstyp
- Die beiden Teilnehmer können unterschiedliche Verschlüsselungstypen haben
- Antworten auf Datenbankabfragen sind einmalige Nachrichten, die den Antwortschlüssel und das Tag in der Datenbankabfrage-Nachricht verwenden
- Bestätigungen von Datenbankspeicherungen sind einmalige Nachrichten, die eine gebündelte Lieferstatusnachricht verwenden


Nicht-Ziele des Router-Anwendungsfalls:

- Keine Notwendigkeit für nicht-anonyme Nachrichten
- Keine Notwendigkeit, Nachrichten durch eingehende Erkundungstunnel zu senden (ein Router veröffentlicht keine Erkundungsleasese)
- Keine Notwendigkeit für anhaltenden Nachrichtenverkehr unter Verwendung von Tags
- Keine Notwendigkeit, "dual key" Session Key Manager laufen zu lassen, wie in [ECIES](/docs/specs/ecies/) für Destinationen beschrieben. Router haben nur einen öffentlichen Schlüssel.


#### Design-Schlussfolgerungen

Der ECIES-Router-SKM benötigt nicht einen vollständigen Ratchet-SKM, wie für Destinationen in [ECIES](/docs/specs/ecies/) spezifiziert.
Es gibt keine Anforderungen für nicht-anonyme Nachrichten im IK-Muster.
Das Bedrohungsmodell erfordert keine Elligator2-codierten Ephermeralschlüssel.

Daher wird der Router-SKM das Noise-"N"-Muster verwenden, das gleiche, das in [Prop152](/proposals/152-ecies-tunnels/) für den Tunnelaufbau spezifiziert ist.
Er wird dasselbe Nutzlastformat verwenden, wie in [ECIES](/docs/specs/ecies/) für Destinationen spezifiziert.
Der Nullstatikschlüssel (kein Binding oder Sitzung) Modus von IK, wie in [ECIES](/docs/specs/ecies/) spezifiziert, wird nicht verwendet.

Antworten auf Abfragen werden mit einem Ratchet-Tag verschlüsselt, falls in der Abfrage angefordert.
Dies ist dokumentiert in [Prop154](/proposals/154-ecies-lookups/), jetzt spezifiziert in [I2NP](/docs/specs/i2np/).

Das Design ermöglicht es dem Router, einen einzigen ECIES-Session-Key-Manager zu haben.
Es besteht keine Notwendigkeit, "dual key" Session Key Manager laufen zu lassen, wie
in [ECIES](/docs/specs/ecies/) für Destinationen beschrieben.
Router haben nur einen öffentlichen Schlüssel.

Ein ECIES-Router hat keinen ElGamal-Statischen-Schlüssel.
Der Router benötigt trotzdem eine Implementierung von ElGamal, um Tunnel
durch ElGamal-Router zu bauen und verschlüsselte Nachrichten an ElGamal-Router zu senden.

Ein ECIES-Router KANN einen Teil-ElGamal-Session-Key-Manager benötigen, um
ElGamal-getaggte Nachrichten, die als Antworten auf NetDB-Suchen
von pre-0.9.46-Floodfill-Routern gesendet wurden, zu empfangen, da diese Router
keine Implementierung von ECIES-getaggten Antworten, wie in [Prop152](/proposals/152-ecies-tunnels/) spezifiziert, haben.
Andernfalls darf ein ECIES-Router keine verschlüsselte Antwort von einem
pre-0.9.46-Floodfill-Router anfordern.

Dies ist optional. Entscheidungen können bei verschiedenen I2P-Implementierungen
unterschiedlich ausfallen und können von der Menge des Netzwerks abhängen, die auf
0.9.46 oder höher aktualisiert wurde.
Zum aktuellen Zeitpunkt sind etwa 85% des Netzwerks auf 0.9.46 oder höher.


## Spezifikation

X25519: Siehe [ECIES](/docs/specs/ecies/).

Router-Identität und Schlüsselzertifikat: Siehe [Common](/docs/specs/common-structures/).

Tunnelaufbau: Siehe [Prop152](/proposals/152-ecies-tunnels/).

Neue Tunnelaufbau-Nachrichten: Siehe [Prop157](/proposals/157-new-tbm/).


### Anfragenverschlüsselung

Die Anfragenverschlüsselung ist die gleiche wie die, die in [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) und [Prop152](/proposals/152-ecies-tunnels/) spezifiziert ist,
unter Verwendung des Noise-"N"-Musters.

Antworten auf Abfragen werden mit einem Ratchet-Tag verschlüsselt, falls in der Abfrage angefordert.
Datenbankabfrage-Anforderungsnachrichten enthalten den 32-Byte-Antwortschlüssel und das 8-Byte-Antwort-Tag
wie in [I2NP](/docs/specs/i2np/) und [Prop154](/proposals/154-ecies-lookups/) spezifiziert. Der Schlüssel und das Tag werden verwendet, um die Antwort zu verschlüsseln.

Tag-Sets werden nicht erstellt.
Das Zero Static Key Schema, das in
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) und [ECIES](/docs/specs/ecies/) spezifiziert ist, wird nicht verwendet.
Ephemerschlüssel werden nicht Elligator2-codiert.

Im Allgemeinen werden dies Neue Sitzungsnachrichten sein und mit einem Nullstatikschlüssel
(kein Binding oder Sitzung) gesendet, da der Absender der Nachricht anonym ist.


#### KDF für Initiale ck und h

Dies ist Standard [NOISE](https://noiseprotocol.org/noise.html) für Muster "N" mit einem Standardprotokollnamen.
Dies ist dasselbe wie in [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) und [Prop152](/proposals/152-ecies-tunnels/) für Tunnelaufbau-Nachrichten spezifiziert.


  ```text

Dies ist das "e"-Nachrichtenmuster:

  // Protokollname definieren.
  Setze protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 Bytes, US-ASCII kodiert, keine NULL-Beendigung).

  // Hash h = 32 Bytes definieren
  // Auf 32 Bytes auffüllen. NICHT hashieren, da es nicht mehr als 32 Bytes sind.
  h = protocol_name || 0

  Chaining-Key ck = 32 Byte definieren. Kopiere die h-Daten nach ck.
  Setze chainKey = h

  // MixHash(null-Prequel)
  h = SHA256(h);

  // bis hierhin können alle Router vorkalkulieren.


  ```


#### KDF für Nachricht

Nachrichtenersteller generieren für jede Nachricht ein ephemeres X25519-Schlüsselpaar.
Ephemerschlüssel müssen pro Nachricht einzigartig sein.
Dies ist dasselbe wie in [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) und [Prop152](/proposals/152-ecies-tunnels/) für Tunnelaufbau-Nachrichten spezifiziert.


  ```dataspec


// Statisches Schlüsselpaar (hesk, hepk) des Zielrouters von der Router-Identität
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || unten bedeutet anfügen
  h = SHA256(h || hepk);

  // bis hierhin können alle Router für alle eingehenden Nachrichten vorkalkulieren

  // Absender generiert ein ephemeres X25519-Schlüsselpaar
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Ende vom "e"-Nachrichtenmuster.

  Dies ist das "es"-Nachrichtenmuster:

  // Noise es
  // Absender führt ein X25519-DH mit dem statischen öffentlichen Schlüssel des Empfängers durch.
  // Der Zielrouter extrahiert den einmaligen Schlüssel des Absenders vor dem verschlüsselten Datensatz.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly-Parameter zur Ver-/Entschlüsselung
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Chain-Key wird nicht verwendet
  //chainKey = keydata[0:31]

  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  Klartext = 464-Byte-Build-Anforderungsdatensatz
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Ende vom "es"-Nachrichtenmuster.

  // MixHash(ciphertext) ist nicht erforderlich
  //h = SHA256(h || ciphertext)


  ```


#### Nutzlast

Die Nutzlast ist dasselbe Blockformat, wie in [ECIES](/docs/specs/ecies/) und [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) definiert.
Alle Nachrichten müssen einen DateTime-Block zur Wiederholungsprävention enthalten.


### Antwortverschlüsselung

Antworten auf Datenbankabfrage-Nachrichten sind Datenbankspeicher- oder Datenbanksuchantwort-Nachrichten.
Sie sind als Bestehende-Sitzungs-Nachrichten verschlüsselt mit
dem 32-Byte-Antwortschlüssel und 8-Byte-Antwort-Tag,
wie in [I2NP](/docs/specs/i2np/) und [Prop154](/proposals/154-ecies-lookups/) spezifiziert.


Es gibt keine expliziten Antworten auf Datenbankspeicher-Nachrichten. Der Absender kann seine
eigene Antwort als Knoblauch-Nachricht an sich selbst bündeln, die eine Lieferstatusnachricht enthält.


## Rechtfertigung

Dieses Design maximiert die Wiederverwendung bestehender kryptografischer Primitive, Protokolle und Codes.

Dieses Design minimiert das Risiko.


## Implementierungsnotizen

Ältere Router überprüfen den Verschlüsselungstyp des Routers nicht und senden ElGamal-verschlüsselte
Aufbaudatensätze oder Netznachrichten.
Einige neuere Router sind fehlerhaft und senden verschiedene Typen fehlerhafter Aufbaudatensätze.
Einige neuere Router können nicht-anonyme (volle Ratchet) Netzdb-Nachrichten senden.
Implementierer sollten diese Datensätze und Nachrichten
so früh wie möglich erkennen und zurückweisen, um die CPU-Auslastung zu reduzieren.


## Probleme

Vorschlag 145 [Prop145](/proposals/145-ecies/) könnte eventuell umgeschrieben werden, um größtenteils
kompatibel mit Vorschlag 152 [Prop152](/proposals/152-ecies-tunnels/) zu sein.


## Migration

Die Implementierung, das Testen und die Einführung werden mehrere Veröffentlichungen und
etwa ein Jahr in Anspruch nehmen. Die Phasen sind wie folgt. Die Zuordnung
jeder Phase zu einer bestimmten Veröffentlichung ist TBD und hängt vom
Entwicklungstempo ab.

Details der Implementierung und Migration können für
jede I2P-Implementierung variieren.


### Grundlagen Point-to-Point

ECIES-Router können Verbindungen zu und Verbindungen von ElGamal-Routern empfangen.
Dies sollte jetzt möglich sein, da mehrere Prüfungen Mitte 2019 zum Abschluss des Vorschlags 145 [Prop145](/proposals/145-ecies/)
in die Java-Codebasis integriert wurden.
Sicherstellen, dass in den Codebasen nichts vorhanden ist,
was Punkt-zu-Punkt-Verbindungen zu Nicht-ElGamal-Routern verhindert.

Korrektheitsprüfungen des Codes:

- Sicherstellen, dass ElGamal-Router keine AEAD-verschlüsselten Antworten auf Datenbankabfrage-Nachrichten anfordern
  (wenn die Antwort zurück durch einen Erkundungstunnel zum Router kommt)
- Sicherstellen, dass ECIES-Router keine AES-verschlüsselten Antworten auf Datenbankabfragen anfordern
  (wenn die Antwort zurück durch einen Erkundungstunnel zum Router kommt)

Bis zu späteren Phasen, wenn Spezifikationen und Implementierungen vollständig sind:

- Sicherstellen, dass Tunnelaufbauten nicht von ElGamal-Routern durch ECIES-Router versucht werden.
- Sicherstellen, dass ElGamal-verschlüsselte Nachrichten nicht von ElGamal-Routern an ECIES-Floodfill-Router gesendet werden.
  (Datenbankabfragen und -speicher)
- Sicherstellen, dass ECIES-verschlüsselte Nachrichten nicht von ECIES-Routern an ElGamal-Floodfill-Router gesendet werden.
  (Datenbankabfragen und -speicher)
- Sicherstellen, dass ECIES-Router nicht automatisch Floodfill werden.

Es sollten keine Änderungen erforderlich sein.
Zielveröffentlichung, falls Änderungen erforderlich: 0.9.48


### NetDB-Kompatibilität

Sicherstellen, dass ECIES-Routerinfos bei ElGamal-Floodfills gespeichert und von ihnen abgerufen werden können.
Dies sollte jetzt möglich sein, da Mitte 2019 mehrere Prüfungen in die Java-Codebasis integriert wurden
zum Abschluss von Vorschlag 145 [Prop145](/proposals/145-ecies/).
Sicherstellen, dass in den Codebasen nichts vorhanden ist,
was die Speicherung von Nicht-ElGamal-RouterInfos in der Netzwerkdatenbank verhindert.

Es sollten keine Änderungen erforderlich sein.
Zielveröffentlichung, falls Änderungen erforderlich: 0.9.48


### Tunnelaufbau

Implementieren des Tunnelaufbaus, wie im Vorschlag 152 [Prop152](/proposals/152-ecies-tunnels/) definiert.
Beginnen Sie damit, dass ein ECIES-Router Tunnel mit allen ElGamal-Schritten baut;
verwendet seinen eigenen Aufbauanfrage-Datensatz für einen eingehenden Tunnel zum Testen und Debuggen.

Dann Test und Unterstützung von ECIES-Routern, die Tunnel mit einer Mischung aus
ElGamal- und ECIES-Schritten bauen.

Dann den Tunnelaufbau durch ECIES-Router ermöglichen.
Es sollte keine minimale Versionsprüfung notwendig sein, es sei denn, es wurden nach einer Veröffentlichung inkompatible Änderungen
am Vorschlag 152 vorgenommen.

Zielveröffentlichung: 0.9.48, Ende 2020


### Ratchet-Nachrichten an ECIES-Floodfills

Implementieren und Testen des Empfangs von ECIES-Nachrichten (mit nullstatischem Schlüssel) durch ECIES-Floodfills,
wie im Vorschlag 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) definiert.
Implementieren und Testen des Empfangs von AEAD-Antworten auf Datenbankabfragen durch ECIES-Router.

Aktivieren Sie automatisch Floodfill durch ECIES-Router.
Dann ermöglichen Sie das Senden von ECIES-Nachrichten an ECIES-Router.
Es sollte keine minimale Versionsprüfung notwendig sein, es sei denn, es wurden nach einer Veröffentlichung inkompatible Änderungen
an Vorschlag 152 vorgenommen.

Zielveröffentlichung: 0.9.49, Anfang 2021.
ECIES-Router können automatisch Floodfill werden.


### Umstellung und Neue Installationen

Neue Installationen werden als Standard ab der Veröffentlichung 0.9.49 auf ECIES eingestellt.

Allmähliches Umstellen aller Router, um das Risiko und die Störung des Netzwerks zu minimieren.
Verwenden Sie vorhandene Codes, die für die Sig-Type-Migration vor einigen Jahren erstellt wurden.
Dieser Code gibt jedem Router eine kleine zufällige Wahrscheinlichkeit, sich bei jedem Neustart umzustellen.
Nach mehreren Neustarts wird ein Router wahrscheinlich auf ECIES umgestellt haben.

Das Kriterium für den Beginn der Umstellung ist, dass ein ausreichender Teil des Netzwerks,
vielleicht 50%, Tunnel durch ECIES-Router bauen kann (0.9.48 oder höher).

Bevor aggressiv das gesamte Netzwerk umgestellt wird, muss die überwiegende Mehrheit
(vielleicht 90% oder mehr) in der Lage sein, Tunnel durch ECIES-Router zu bauen (0.9.48 oder höher)
UND Nachrichten an ECIES-Floodfills zu senden (0.9.49 oder höher).
Dieses Ziel wird wahrscheinlich für die Veröffentlichung der Version 0.9.52 erreicht.

Die Umstellung wird mehrere Veröffentlichungen dauern.

Zielveröffentlichung:
0.9.49 für neue Router, die standardmäßig auf ECIES eingestellt sind;
0.9.49, um langsam mit der Umstellung zu beginnen;
0.9.50 - 0.9.52, um die Umstellungsrate wiederholt zu erhöhen;
Ende 2021, damit der Großteil des Netzwerks umgestellt ist.


### Neue Tunnelaufbau-Nachricht (Phase 2)

Implementieren und Testen der neuen Tunnelaufbau-Nachricht, wie im Vorschlag 157 [Prop157](/proposals/157-new-tbm/) definiert.
Rollen Sie die Unterstützung in der Veröffentlichung 0.9.51 aus.
Führen Sie zusätzliche Tests durch, und aktivieren Sie die Funktion anschließend in der Veröffentlichung 0.9.52.

Das Testen wird schwierig sein.
Bevor dies weitgehend getestet werden kann, muss ein guter Teil des Netzwerks es unterstützen.
Bevor es breit nützlich ist, muss die Mehrheit des Netzwerks es unterstützen.
Falls nach dem Testen Änderungen an Spezifikationen oder Implementierungen erforderlich sind,
könnte dies die Einführung um eine zusätzliche Veröffentlichung verzögern.

Zielveröffentlichung: 0.9.52, Ende 2021.


### Umstellung abgeschlossen

Zu diesem Zeitpunkt werden Router, die älter als eine bestimmte Version TBD sind,
nicht in der Lage sein, Tunnel durch die meisten Peers zu bauen.

Zielveröffentlichung: 0.9.53, Anfang 2022.


