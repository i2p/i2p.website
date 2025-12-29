---
title: "ChaCha Tunnel Layer Encryption"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Überblick

Dieser Vorschlag baut auf den Änderungen des Vorschlags 152: ECIES Tunnels auf und erfordert diese.

Nur Tunnel, die durch Hops aufgebaut werden, die das BuildRequestRecord-Format für ECIES-X25519-Tunnel unterstützen, können diese Spezifikation implementieren.

Diese Spezifikation erfordert das Tunnel Build Options-Format, um den Typ der Tunnel-Schicht-Verschlüsselung anzuzeigen und Layer-AEAD-Schlüssel zu übertragen.

### Ziele

Die Ziele dieses Vorschlags sind:

- Ersetzen von AES256/ECB+CBC durch ChaCha20 für etablierte Tunnel-IV und Layer-Verschlüsselung
- Verwendung von ChaCha20-Poly1305 für AEAD-Schutz zwischen den Hops
- Unsichtbarkeit von bestehender Tunnel-Schicht-Verschlüsselung für Nicht-Tunnel-Teilnehmer
- Keine Änderungen an der Gesamtlänge der Tunnel-Nachricht

### Verarbeitung von etablierten Tunnel-Nachrichten

Dieser Abschnitt beschreibt Änderungen an:

- Ausgangs- und Eingangsgateway-Vorverarbeitung + Verschlüsselung
- Teilnehmer-Verschlüsselung + Nachverarbeitung
- Ausgangs- und Eingangsendpunkt-Verschlüsselung + Nachverarbeitung

Für einen Überblick über die aktuelle Tunnel-Nachrichtenverarbeitung siehe die [Tunnel Implementation](/docs/specs/implementation/) Spezifikation.

Besprochen werden nur Änderungen für Router, die die ChaCha20-Schicht-Verschlüsselung unterstützen.

Es werden keine Änderungen für gemischte Tunnel mit AES-Schicht-Verschlüsselung in Betracht gezogen, bis ein sicheres Protokoll entwickelt werden kann, um eine 128-Bit-AES-IV in einen 64-Bit-ChaCha20-Nonce umzuwandeln. Bloomfilter gewährleisten die Einzigartigkeit für die volle IV, aber die erste Hälfte einzigartiger IVs könnte identisch sein.

Dies bedeutet, dass die Schicht-Verschlüsselung für alle Hops im Tunnel einheitlich sein muss und während des Tunnel-Erstellungsprozesses mithilfe von Tunnel-Build-Optionen festgelegt wird.

Alle Gateways und Tunnel-Teilnehmer müssen einen Bloomfilter pflegen, um die beiden unabhängigen Nonces zu validieren.

Der in diesem Vorschlag erwähnte ``nonceKey`` ersetzt den in der AES-Schicht-Verschlüsselung verwendeten ``IVKey``. Er wird mit dem gleichen KDF aus Vorschlag 152 erzeugt.

### AEAD-Verschlüsselung von Hop-zu-Hop-Nachrichten

Für jedes Paar aufeinanderfolgender Hops muss ein zusätzlicher einzigartiger ``AEADKey`` generiert werden. Dieser Schlüssel wird von aufeinanderfolgenden Hops verwendet, um die innerlich ChaCha20-verschlüsselte Tunnel-Nachricht mit ChaCha20-Poly1305 zu verschlüsseln und zu entschlüsseln.

Die Tunnel-Nachrichten müssen die Länge des inneren verschlüsselten Rahmens um 16 Bytes reduzieren, um dem Poly1305 MAC Platz zu bieten.

AEAD kann nicht direkt auf die Nachrichten angewendet werden, da von ausgehenden Tunneln eine iterative Entschlüsselung benötigt wird. Iterative Entschlüsselung kann nur, so wie sie jetzt verwendet wird, mit ChaCha20 ohne AEAD erreicht werden.

```text
+----+----+----+----+----+----+----+----+
  |    Tunnel ID      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | tunnelNonce cont. |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  |  obfsNonce cont.  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Encrypted Data              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  Tunnel ID :: `TunnelId`
         4 Bytes
         die ID des nächsten Hops

  tunnelNonce ::
         8 Bytes
         der Tunnel-Schicht-Nonce

  obfsNonce ::
         8 Bytes
         der Nonce der Tunnel-Schicht-Verschlüsselung

  Encrypted Data ::
         992 Bytes
         die verschlüsselte Tunnel-Nachricht

  Poly1305 MAC ::
         16 Bytes

  Gesamtgröße: 1028 Bytes
```

Innere Hops (mit vor- und nachfolgenden Hops) haben zwei ``AEADKeys``, einen zum Entschlüsseln der AEAD-Schicht des vorherigen Hops und einen zum Verschlüsseln der AEAD-Schicht zum folgenden Hop.

Alle internen Hop-Teilnehmer erhalten somit 64 zusätzliche Bytes an Schlüsseldaten in ihren BuildRequestRecords.

Das Ausgangs-Endpunkt und das Eingangs-Gateway benötigen nur zusätzliche 32 Bytes an Schlüsseldaten, da sie keine Nachrichten zwischen sich auf Tunnel-Schicht verschlüsseln.

Das Ausgangs-Gateway erzeugt seinen ``outAEAD``-Schlüssel, der derselbe ist wie der ``inAEAD``-Schlüssel des ersten ausgehenden Hops.

Der Eingangs-Endpunkt erzeugt seinen ``inAEAD``-Schlüssel, der derselbe ist wie der ``outAEAD``-Schlüssel des letzten eingehenden Hops.

Innere Hops erhalten einen ``inAEADKey`` und einen ``outAEADKey``, die verwendet werden, um eingehende Nachrichten zu AEAD-entschlüsseln und ausgehende Nachrichten zu verschlüsseln.

Als Beispiel in einem Tunnel mit inneren Hops OBGW, A, B, OBEP:

- A's ``inAEADKey`` ist derselbe wie der ``outAEADKey`` des OBGW
- B's ``inAEADKey`` ist derselbe wie A's ``outAEADKey``
- B's ``outAEADKey`` ist derselbe wie OBEP's ``inAEADKey``

Schlüssel sind eindeutig für Hop-Paare, daher wird OBEP's ``inAEADKey`` anders sein als A's ``inAEADKey``, A's ``outAEADKey`` anders als B's ``outAEADKey`` usw.

### Verarbeitung von Gateway- und Tunnel-Erstellernachrichten

Gateways fragmentieren und bündeln Nachrichten auf die gleiche Weise und reservieren Platz nach den Instruktions-Fragmentrahmen für den Poly1305 MAC.

Innere I2NP-Nachrichten, die AEAD-Rahmen (einschließlich des MAC) enthalten, können über Fragmente verteilt werden, aber jede verlorene Fragmente führen zur fehlgeschlagenen AEAD-Entschlüsselung (fehlgeschlagene MAC-Verifizierung) am Endpunkt.

### Gateway-Vorverarbeitung & Verschlüsselung

Wenn Tunnel die ChaCha20-Schicht-Verschlüsselung unterstützen, erzeugen Gateways zwei 64-Bit-Nonces pro Nachrichtensatz.

Eingehende Tunnel:

- Verschlüsseln den IV und die Tunnel-Nachricht(en) mit ChaCha20
- Verwenden 8-Byte ``tunnelNonce`` und ``obfsNonce`` aufgrund der Lebensdauer der Tunnel
- Verwenden einen 8-Byte ``obfsNonce`` für die ``tunnelNonce``-Verschlüsselung
- Zerstören den Tunnel, bevor 2^(64 - 1) - 1 Nachrichtensätze erreicht werden: 2^63 - 1 = 9.223.372.036.854.775.807

  - Nonce-Limit, um Kollisionen der 64-Bit-Nonces zu vermeiden
  - Nonce-Limit nahezu unmöglich zu erreichen, da dies über ~15.372.286.728.091.294 Nachrichten/Sekunde für 10-Minuten-Tunnel bedeuten würde

- Den Bloomfilter basierend auf einer vernünftigen Anzahl erwarteter Elemente abstimmen (128 msgs/sec, 1024 msgs/sec? TBD)

Das Eingangs-Gateway (IBGW) des Tunnels verarbeitet Nachrichten, die von einem anderen Tunnel-Ausgangs-Endpunkt (OBEP) empfangen wurden.

Zu diesem Zeitpunkt ist die äußerste Nachrichtenschicht mit Transportverschlüsselung Punkt-zu-Punkt verschlüsselt.
Die I2NP-Nachrichtenheader sind auf der Tunnel-Schicht für den OBEP und IBGW sichtbar.
Die inneren I2NP-Nachrichten sind in Garlic-Klaven verpackt, die mithilfe von End-zu-Ende-Sitzungsverschlüsselung verschlüsselt sind.

Das IBGW verarbeitet die Nachrichten zu den entsprechend formatierten Tunnel-Nachrichten vor und verschlüsselt sie wie folgt:

```text

// IBGW generiert zufällige Nonces, die keine Kollision in ihrem Bloom-Filter für jeden Nonce sicherstellen
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW ChaCha20 "verschlüsselt" jede der vorverarbeiteten Tunnel-Nachrichten mit ihrem tunnelNonce und layerKey
  encMsg = ChaCha20(msg = tunnel msg, nonce = tunnelNonce, key = layerKey)

  // ChaCha20-Poly1305 verschlüsselt jeden verschlüsselten Datenrahmen der Nachricht mit dem tunnelNonce und outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

Das Format der Tunnel-Nachrichten wird sich leicht ändern, indem zwei 8-Byte-Nonces anstelle einer 16-Byte-IV verwendet werden.
Der für die Verschlüsselung des Nonce verwendete ``obfsNonce`` wird dem 8-Byte ``tunnelNonce`` angehängt und wird von jedem Hop mithilfe des verschlüsselten ``tunnelNonce`` und dem ``nonceKey`` des Hops verschlüsselt.

Nachdem der Nachrichtensatz für jeden Hop vorab entschlüsselt wurde, verschlüsselt das Ausgangs-Gateway
die verschlüsselten Teile jeder Tunnel-Nachricht mit ChaCha20-Poly1305 AEAD unter Verwendung des ``tunnelNonce`` und seines ``outAEADKey``.

Ausgehende Tunnel:

- Iterativ entschlüsseln Tunnel-Nachrichten
- ChaCha20-Poly1305 verschlüsseln vorzeitig entschlüsselte Tunnel-Nachrichten verschlüsselte Rahmen
- Verwenden die gleichen Regeln für Schicht-Nonces wie eingehende Tunnel
- Generieren zufällige Nonces einmal pro Satz gesendeter Tunnel-Nachrichten

```text


// Für jeden Satz Nachrichten, generiere einzigartige, zufällige Nonces
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Für jeden Hop, ChaCha20 den vorherigen tunnelNonce mit dem IV-Schlüssel des aktuellen Hops
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = hop's nonceKey)

  // Für jeden Hop, ChaCha20 "entschlüsseln" die Tunnel-Nachricht mit dem aktuellen tunnelNonce und layerKey des Hops
  decMsg = ChaCha20(msg = tunnel msg(s), nonce = tunnelNonce, key = hop's layerKey)

  // Für jeden Hop, ChaCha20 "entschlüsseln" den obfsNonce mit dem verschlüsselten tunnelNonce und nonceKey des aktuellen Hops
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = hop's nonceKey)

  // Nach der Hop-Verarbeitung, ChaCha20-Poly1305 verschlüsseln jede Tunnel-Nachrichts "entschlüsselte" Datenrahmen mit dem ersten verschlüsselten tunnelNonce und inAEADKey des Hops
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = first hop's encrypted tunnelNonce, key = first hop's inAEADKey / GW outAEADKey)
```

### Teilnehmerverarbeitung

Teilnehmer werden wie bisher gesehene Nachrichten mit abklingenden Bloom-Filtern verfolgen.

Tunnel-Nonces müssen pro Hop einmal verschlüsselt werden, um Bestätigungsangriffe durch nicht aufeinanderfolgende, kolludierende Hops zu verhindern.

Hops werden den empfangenen Nonce verschlüsseln, um Bestätigungsangriffe zwischen vorherigen und nachfolgenden Hops zu verhindern, sodass kolludierende, nicht-aufeinanderfolgende Hops nicht erkennen können, dass sie zum gleichen Tunnel gehören.

Um den erhaltenen ``tunnelNonce`` und ``obfsNonce`` zu validieren, überprüfen Teilnehmer jeden Nonce einzeln auf Duplikate in ihrem Bloomfilter.

Nach der Validierung:

- ChaCha20-Poly1305 entschlüsselt jede Tunnel-Nachrichts AEAD-Verschlüsselungs-Frame mit dem erhaltenen ``tunnelNonce`` und ihrem ``inAEADKey``
- ChaCha20 verschlüsselt den ``tunnelNonce`` mit ihrem ``nonceKey`` und dem erhaltenen ``obfsNonce``
- ChaCha20 verschlüsselt den verschlüsselten Datenrahmen jeder Tunnel-Nachricht mit dem verschlüsselten ``tunnelNonce`` und ihrem ``layerKey``
- ChaCha20-Poly1305 verschlüsselt den verschlüsselten Datenrahmen jeder Tunnel-Nachricht mit dem verschlüsselten ``tunnelNonce`` und ihrem ``outAEADKey``
- ChaCha20 verschlüsselt den ``obfsNonce`` mit ihrem ``nonceKey`` und dem verschlüsselten ``tunnelNonce``
- Sendet das Tupel {``nextTunnelId``, encrypted (``tunnelNonce`` || ``obfsNonce``), AEAD ciphertext || MAC} an den nächsten Hop.

```text

// Zur Überprüfung sollten Tunnel-Hops den Bloom-Filter auf die Einzigartigkeit jedes empfangenen Nonce überprüfuntion
  // Nach der Verifizierung die AEAD-Frame(s) durch ChaCha20-Poly1305-Entschlüsselung jeder Tunnel-Nachricht's verschlüsseltem Frame
  // mit dem erhaltenen tunnelNonce und inAEADKey auspacken
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = received encMsg \|\| MAC, nonce = received tunnelNonce, key = inAEADKey)

  // ChaCha20 verschlüsseln den tunnelNonce mit dem obfsNonce und dem nonceKey des Hops
  tunnelNonce = ChaCha20(msg = received tunnelNonce, nonce = received obfsNonce, key = nonceKey)

  // ChaCha20 verschlüsseln jeden verschlüsselten Datenrahmen der Tunnel-Nachricht mit dem verschlüsselten tunnelNonce und dem layerKey des Hops
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Für AEAD-Schutz, zusätzlich ChaCha20-Poly1305 verschlüsseln jeden verschlüsselten Datenrahmen der Nachricht
  // mit dem verschlüsselten tunnelNonce und dem outAEADKey des Hops
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // ChaCha20 verschlüsseln den empfangenen obfsNonce mit dem verschlüsselten tunnelNonce und dem nonceKey des Hops
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Verarbeitung des Eingangs-Endpunkts

Für ChaCha20-Tunnel wird das folgende Schema zur Entschlüsselung jeder Tunnel-Nachricht verwendet:

- Validieren des empfangenen ``tunnelNonce`` und ``obfsNonce`` unabhängig gegen ihren Bloomfilter
- ChaCha20-Poly1305 entschlüsseln den verschlüsselten Datenrahmen mit dem erhaltenen ``tunnelNonce`` und ``inAEADKey``
- ChaCha20 entschlüsseln den verschlüsselten Datenrahmen mit dem erhaltenen ``tunnelNonce`` & dem ``layerKey`` des Hops
- ChaCha20 entschlüsseln den ``obfsNonce`` mit dem ``nonceKey`` des Hops und dem erhaltenen ``tunnelNonce``, um den vorherigen ``obfsNonce`` zu erhalten
- ChaCha20 entschlüsseln den erhaltenen ``tunnelNonce`` mit dem ``nonceKey`` des Hops und dem entschlüsselten ``obfsNonce``, um den vorherigen ``tunnelNonce`` zu erhalten
- ChaCha20 entschlüsseln die verschlüsselten Daten mit dem entschlüsselten ``tunnelNonce`` & dem ``layerKey`` des vorherigen Hops
- Wiederholen Sie die Schritte zur Nonce- und Schichtentschlüsselung für jeden Hop im Tunnel zurück zum IBGW
- Die AEAD-Frame-Entschlüsselung wird nur im ersten Durchlauf benötigt

```text

// Für die erste Runde, ChaCha20-Poly1305 entschlüsseln die verschlüsselten Datenrahmen + MAC jeder Nachricht
  // unter Verwendung des erhaltenen tunnelNonce und inAEADKey
  msg = encTunMsg \|\| MAC
  tunnelNonce = received tunnelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Wiederholen für jeden Hop im Tunnel zurück zum IBGW
  // Für jede Runde, ChaCha20 entschlüsseln jede Hop-Schichtverschlüsselung auf jedem Datenrahmen der Nachricht
  // Ersetzen Sie den erhaltenen tunnelNonce durch den im vorherigen Durchlauf entschlüsselten tunnelNonce für jeden Hop
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Sicherheitsanalyse für ChaCha20+ChaCha20-Poly1305 Tunnel-Schicht-Verschlüsselung

Der Wechsel von AES256/ECB+AES256/CBC zu ChaCha20+ChaCha20-Poly1305 bietet eine Reihe von Vorteilen und neue Sicherheitsüberlegungen.

Die größten Sicherheitsüberlegungen, die berücksichtigt werden müssen, sind, dass ChaCha20- und ChaCha20-Poly1305-Nonces für die Lebensdauer des verwendeten Schlüssels pro Nachricht einzigartig sein müssen.

Das Versäumnis, einzigartige Nonces mit demselben Schlüssel für verschiedene Nachrichten zu verwenden, führt zu einem Ausfall von ChaCha20 und ChaCha20-Poly1305.

Ein angehängter ``obfsNonce`` ermöglicht es dem IBEP, den ``tunnelNonce`` für die Schichtverschlüsselung jedes Hops zu entschlüsseln und den vorherigen Nonce wiederherzustellen.

Der ``obfsNonce`` zusammen mit dem ``tunnelNonce`` enthüllt keine neuen Informationen an die Tunnel-Hops,
da der ``obfsNonce`` mit dem verschlüsselten ``tunnelNonce`` verschlüsselt wird. Dies ermöglicht es dem IBEP auch, den vorherigen ``obfsNonce`` auf ähnliche Weise wie die Wiederherstellung des ``tunnelNonce`` wiederherzustellen.

Der größte Sicherheitsvorteil besteht darin, dass es keine Bestätigungs- oder Orangenangriffe gegen ChaCha20 gibt,
und die Verwendung von ChaCha20-Poly1305 zwischen den Hops bietet AEAD-Schutz gegen die Manipulation der Verschlüsselung durch
Außerhalb der BandmitM-Angreifer.

Es gibt praktische Orangenangriffe gegen AES256/ECB + AES256/CBC, wenn der Schlüssel erneut verwendet wird (wie in der Tunnel-Schicht-Verschlüsselung).

Die Orangenangriffe gegen AES256/ECB funktionieren nicht, aufgrund der doppelten Verschlüsselung und der Verschlüsselung über einen einzelnen Block (den Tunnel-IV).

Die Padding-Oracle-Angriffe gegen AES256/CBC funktionieren nicht, da kein Padding verwendet wird. Wenn sich die Tunnel-Nachrichtslänge jemals auf Nicht-mod-16-Längen änderte, wäre AES256/CBC aufgrund abgelehnter doppelter IVs immer noch nicht anfällig.

Beide Angriffe werden auch durch das Verbot mehrerer Oracle-Anfragen mit derselben IV blockiert, da doppelte IVs abgelehnt werden.

## Referenzen

* [Tunnel-Implementation](/docs/specs/implementation/)
