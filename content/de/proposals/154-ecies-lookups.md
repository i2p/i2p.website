---
title: "Datenbank-Abfragen von ECIES-Zielen"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Hinweis
ECIES zu ElG wurde in 0.9.46 implementiert und die Vorschlagsphase ist abgeschlossen.
Siehe [I2NP](/docs/specs/i2np/) für die offizielle Spezifikation.
Dieser Vorschlag kann dennoch für Hintergrundinformation herangezogen werden.
ECIES zu ECIES mit enthaltenen Schlüsseln ist ab Version 0.9.48 implementiert.
Der Abschnitt ECIES-zu-ECIES (abgeleitete Schlüssel) kann in einem zukünftigen Vorschlag
wiedereröffnet oder integriert werden.


## Überblick

### Definitionen

- AEAD: ChaCha20/Poly1305
- DLM: I2NP Database Lookup Message
- DSM: I2NP Database Store Message
- DSRM: I2NP Database Search Reply Message
- ECIES: ECIES-X25519-AEAD-Ratchet (Vorschlag 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): Wie definiert in [ECIES](/docs/specs/ecies/)
- LS: Leaseset
- lookup: I2NP DLM
- reply: I2NP DSM oder DSRM


### Zusammenfassung

Beim Senden eines DLM für ein LS an einen Floodfill gibt das DLM in der Regel an,
dass die Antwort markiert, AES-verschlüsselt und über einen Tunnel zum Ziel gesendet
werden soll. Unterstützung für AES-verschlüsselte Antworten wurde in 0.9.7 hinzugefügt.

AES-verschlüsselte Antworten wurden in 0.9.7 spezifiziert, um den großen Krypto-Overhead von ElG zu minimieren, da sie die Tags/AES-Funktionalität in ElGamal/AES+SessionTags wieder verwendeten. Allerdings können AES-Antworten am IBEP manipuliert werden, da es keine Authentifizierung gibt, und die Antworten sind nicht vorwärtsgeheim.

Mit [ECIES](/docs/specs/ecies/) Zielen ist die Absicht von Vorschlag 144, dass
die Ziele keine 32-Byte-Tags und AES-Entschlüsselung mehr unterstützen.
Die Einzelheiten wurden in diesem Vorschlag absichtlich nicht enthalten.

Dieser Vorschlag dokumentiert eine neue Option im DLM, um ECIES-verschlüsselte Antworten anzufordern.


### Ziele

- Neue Flags für DLM, wenn eine verschlüsselte Antwort über einen Tunnel zu einem ECIES-Ziel angefordert wird
- Für die Antwort, Hinzufügen von Vorwärtsgeheimnis und Senderauthentifizierung, die gegen
  die Kompromittierung des Schlüssels des Anfragenden (Ziel) resistent ist (KCI).
- Anonymität des Anfragenden aufrechterhalten
- Minimierung des Krypto-Overheads

### Nicht-Ziele

- Keine Änderung der Verschlüsselungs- oder Sicherheitsmerkmale der Abfrage (DLM).
  Die Abfrage hat Vorwärtsgeheimnis nur für die Kompromittierung des Anfragerschlüssels.
  Die Verschlüsselung erfolgt mit dem statischen Schlüssel des Floodfills.
- Keine Vorwärtsgeheimnis- oder Senderauthentifizierungsprobleme, die resistent sind gegen
  die Kompromittierung des Schlüssels des Antwortenden (Floodfill) (KCI).
  Der Floodfill ist eine öffentliche Datenbank und wird auf Anfragen von jedem antworten.
- Keine Gestaltung von ECIES-Routern in diesem Vorschlag.
  Wohin der X25519-öffentliche Schlüssel eines Routers geht, ist noch zu bestimmen.


## Alternativen

In Ermangelung eines definierten Weges, um Antworten an ECIES-Ziele zu verschlüsseln, gibt es mehrere Alternativen:

1) Keine verschlüsselten Antworten anfordern. Antworten werden unverschlüsselt sein.
Java I2P verwendet derzeit diesen Ansatz.

2) Unterstützung für 32-Byte-Tags und AES-verschlüsselte Antworten zu ausschließlich ECIES-Zielen hinzufügen
und AES-verschlüsselte Antworten wie gewohnt anfordern. i2pd verwendet derzeit diesen Ansatz.

3) AES-verschlüsselte Antworten wie gewohnt anfordern, sie jedoch über
Erkundungstunnel zurück zum Router leiten.
Java I2P verwendet diesen Ansatz derzeit in einigen Fällen.

4) Für duale ElG- und ECIES-Ziele,
AES-verschlüsselte Antworten wie gewohnt anfordern. Java I2P verwendet diesen Ansatz derzeit.
i2pd hat duale Krypto-Ziele noch nicht implementiert.


## Design

- Neues DLM-Format wird ein Bit zum Flags-Feld hinzufügen, um ECIES-verschlüsselte Antworten zu spezifizieren.
  ECIES-verschlüsselte Antworten werden das [ECIES](/docs/specs/ecies/) Existing Session Nachrichtenformat verwenden,
  mit einem vorangestellten Tag und einer ChaCha/Poly-Nutzlast und MAC.

- Zwei Varianten definieren. Eine für ElG-Router, wo ein DH-Vorgang nicht möglich ist,
  und eine für zukünftige ECIES-Router, bei denen ein DH-Vorgang möglich ist und zusätzliche Sicherheit bieten kann. Für weitere Studien.

DH ist nicht für Antworten von ElG-Routern möglich, da sie keinen
X25519-öffentlichen Schlüssel veröffentlichen.


## Spezifikation

Im [I2NP](/docs/specs/i2np/) DLM (DatabaseLookup) Spezifikation folgende Änderungen vornehmen.

Bit 4 "ECIESFlag" für die neuen Verschlüsselungsoptionen hinzufügen.

```text
flags ::
       bit 4: ECIESFlag
               vor Veröffentlichung 0.9.46 ignoriert
               ab Veröffentlichung 0.9.46:
               0  => unverschlüsselte oder ElGamal-Antwort senden
               1  => ChaCha/Poly-verschlüsselte Antwort mit eingeschlossenem Schlüssel senden
                     (ob Tag eingeschlossen ist, hängt von Bit 1 ab)
```

Flag-Bit 4 wird in Kombination mit Bit 1 verwendet, um den Antwort-Verschlüsselungsmodus zu bestimmen.
Flag-Bit 4 darf nur beim Senden an Router mit Version 0.9.46 oder höher gesetzt werden.


In der untenstehenden Tabelle bedeutet
"DH n/a", dass die Antwort nicht verschlüsselt ist.
"DH nein" bedeutet, dass die Antwortschlüssel in der Anfrage enthalten sind.
"DH ja" bedeutet, dass die Antwortschlüssel aus dem DH-Vorgang abgeleitet sind.


| Flag-Bits 4,1 | Von Ziel | Zu Router | Antwort | DH? | Anmerkungen |
|---------------|----------|-----------|---------|-----|-------------|
| 0 0            | Beliebig | Beliebig  | keine   | n/a | aktuell |
| 0 1            | ElG      | ElG       | AES     | nein| aktuell |
| 0 1            | ECIES    | ElG       | AES     | nein| i2pd-Workaround |
| 1 0            | ECIES    | ElG       | AEAD    | nein| dieser Vorschlag |
| 1 0            | ECIES    | ECIES     | AEAD    | nein| 0.9.49 |
| 1 1            | ECIES    | ECIES     | AEAD    | ja  | zukünftig |


### ElG zu ElG

ElG-Ziel sendet eine Abfrage an einen ElG-Router.

Geringfügige Änderungen an der Spezifikation, um auf das neue Bit 4 zu achten.
Keine Änderungen am bestehenden Binärformat.


Schlüsselerzeugung des Anfragenden (Klarstellung):

```text
reply_key :: CSRNG(32) 32 Byte Zufallsdaten
  reply_tags :: Jeder ist CSRNG(32) 32 Byte Zufallsdaten
```

Nachrichtenformat (Prüfung auf ECIESFlag hinzufügen):

```text
reply_key ::
       32 Byte `SessionKey` Big-Endian
       nur enthalten, wenn encryptionFlag == 1 UND ECIESFlag == 0, nur ab Veröffentlichung 0.9.7

  tags ::
       1 Byte `Integer`
       gültiger Bereich: 1-32 (typischerweise 1)
       die Anzahl der folgenden Antwort-Tags
       nur enthalten, wenn encryptionFlag == 1 UND ECIESFlag == 0, nur ab Veröffentlichung 0.9.7

  reply_tags ::
       eines oder mehrere 32 Byte `SessionTag`s (typischerweise eines)
       nur enthalten, wenn encryptionFlag == 1 UND ECIESFlag == 0, nur ab Veröffentlichung 0.9.7
```


### ECIES zu ElG

ECIES-Ziel sendet eine Abfrage an einen ElG-Router.
Unterstützt ab 0.9.46.

Die Felder reply_key und reply_tags sind für eine ECIES-verschlüsselte Antwort neu definiert.

Schlüsselerzeugung des Anfragenden:

```text
reply_key :: CSRNG(32) 32 Byte Zufallsdaten
  reply_tags :: Jeder ist CSRNG(8) 8 Byte Zufallsdaten
```

Nachrichtenformat:
Felder reply_key und reply_tags wie folgt neu definieren:

```text
reply_key ::
       32 Byte ECIES `SessionKey` Big-Endian
       nur enthalten, wenn encryptionFlag == 0 UND ECIESFlag == 1, nur ab Veröffentlichung 0.9.46

  tags ::
       1 Byte `Integer`
       erforderlicher Wert: 1
       die Anzahl der folgenden Antwort-Tags
       nur enthalten, wenn encryptionFlag == 0 UND ECIESFlag == 1, nur ab Veröffentlichung 0.9.46

  reply_tags ::
       ein 8 Byte ECIES `SessionTag`
       nur enthalten, wenn encryptionFlag == 0 UND ECIESFlag == 1, nur ab Veröffentlichung 0.9.46
```


Die Antwort ist eine ECIES Existing Session Nachricht, wie definiert in [ECIES](/docs/specs/ecies/).

```text
tag :: 8 Byte reply_tag

  k :: 32 Byte Sitzungsschlüssel
     Der reply_key.

  n :: 0

  ad :: Das 8 Byte reply_tag

  payload :: Klartextdaten, das DSM oder DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### ECIES zu ECIES (0.9.49)

ECIES-Ziel oder -Router sendet eine Abfrage an einen ECIES-Router, mit gebündelten Antwortschlüsseln.
Unterstützt ab 0.9.49.

ECIES-Router wurden in 0.9.48 eingeführt, siehe [Prop156](/proposals/156-ecies-routers/).
Ab 0.9.49 können ECIES-Ziele und -Router dasselbe Format wie im
Abschnitt "ECIES zu ElG" oben verwenden, mit Antwortschlüsseln, die in der Anfrage enthalten sind.
Die Abfrage wird das "one time format" in [ECIES](/docs/specs/ecies/) verwenden,
da der Anfragende anonym ist.

Für eine neue Methode mit abgeleiteten Schlüsseln, siehe den nächsten Abschnitt.


### ECIES zu ECIES (zukünftig)

ECIES-Ziel oder -Router sendet eine Abfrage an einen ECIES-Router, und die Antwortschlüssel werden aus dem DH abgeleitet.
Nicht vollständig definiert oder unterstützt, Implementierung noch festzulegen.

Die Abfrage wird das "one time format" in [ECIES](/docs/specs/ecies/) verwenden,
da der Anfragende anonym ist.

Feld reply_key wie folgt neu definieren. Es gibt keine zugehörigen Tags.
Die Tags werden im untenstehenden KDF generiert.

Dieser Abschnitt ist unvollständig und erfordert weitere Untersuchungen.


```text
reply_key ::
       32 Byte X25519 ephemerer `PublicKey` des Anfragenden, Little-Endian
       nur enthalten, wenn encryptionFlag == 1 UND ECIESFlag == 1, nur ab Veröffentlichung 0.9.TBD
```

Die Antwort ist eine ECIES Existing Session Nachricht, wie definiert in [ECIES](/docs/specs/ecies/).
Siehe [ECIES](/docs/specs/ecies/) für alle Definitionen.


```text
// Alices X25519 ephemere Schlüssel
  // aesk = Alice ephemerer privater Schlüssel
  aesk = GENERATE_PRIVATE()
  // aepk = Alice ephemerer öffentlicher Schlüssel
  aepk = DERIVE_PUBLIC(aesk)
  // Bobs X25519 statische Schlüssel
  // bsk = Bob privater statischer Schlüssel
  bsk = GENERATE_PRIVATE()
  // bpk = Bob öffentlicher statischer Schlüssel
  // bpk ist entweder Teil von RouterIdentity oder in RouterInfo veröffentlicht (TBD)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey from ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: unused
  unused = keydata[0:31]
  // Output 2: Der Ketten-Schlüssel zur Initialisierung des neuen
  // Sitzungstag- und symmetrischen Schlüssel-Ratchetes
  // für Alice zu Bob Übertragungen
  ck = keydata[32:63]

  // Sitzungstag- und symmetrische Schlüssel-Ratchet Schlüssel
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: 8 Byte Tag wie generiert von RATCHET_TAG() in [ECIES](/docs/specs/ecies/)

  k :: 32 Byte Schlüssel wie generiert von RATCHET_KEY() in [ECIES](/docs/specs/ecies/)

  n :: Der Index des Tags. Typischerweise 0.

  ad :: Der 8 Byte Tag

  payload :: Klartextdaten, das DSM oder DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### Antwortformat

Dies ist die vorhandene Sitzungsnachricht,
gleich wie in [ECIES](/docs/specs/ecies/), unten zur Referenz kopiert.

```text
+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
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
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes
```


## Begründung

Die Antwortverschlüsselungsparameter in der Abfrage, die erstmals in 0.9.7 eingeführt wurden, 
sind etwas von einer Schichtverletzung. Es wird auf diese Weise gemacht, aus Effizienzgründen.
Aber auch weil die Abfrage anonym ist.

Wir könnten das Abfrageformat generisch gestalten, wie mit einem Verschlüsselungstyp-Feld,
aber das wäre wahrscheinlich mehr Aufwand als es wert ist.

Der obige Vorschlag ist der einfachste und minimiert die Änderungen am Abfrageformat.


## Anmerkungen

Datenbankabfragen und Speichern zu ElG-Routern müssen wie gewohnt ElGamal/AESSessionTag-verschlüsselt sein.


## Probleme

Weitere Analysen zur Sicherheit der beiden ECIES-Antwortoptionen sind erforderlich.


## Migration

Keine Kompatibilitätsprobleme mit älteren Versionen. Router, die eine router.version von 0.9.46 oder höher
in ihrem RouterInfo angeben, müssen diese Funktion unterstützen.
Router dürfen keine DatabaseLookup mit den neuen Flags an Router mit einer Version von weniger als 0.9.46 senden.
Wenn eine Datenbank-Abfragenachricht mit Bit 4 gesetzt und Bit 1 nicht gesetzt irrtümlich an
einen Router ohne Unterstützung gesendet wird, wird dieser wahrscheinlich den bereitgestellten Schlüssel und Tag ignorieren und
die Antwort unverschlüsselt senden.
