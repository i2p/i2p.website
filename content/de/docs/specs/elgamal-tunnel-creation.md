---
title: "Tunnel-Erstellungsspezifikation (ElGamal)"
description: "Legacy ElGamal-basierte tunnel Build-Spezifikation, ersetzt durch X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/de/tunnel-alt-creation"
  - "/de/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Übersicht {#tunnelcreate-overview}

HINWEIS: VERALTET - Dies ist die ElGamal tunnel build Spezifikation. Siehe die [X25519 tunnel build Spezifikation](/docs/specs/tunnel-creation-ecies) für die aktuelle Methode.

Dieses Dokument spezifiziert die Details der verschlüsselten tunnel-Build-Nachrichten, die zur Erstellung von tunnels mit einer "nicht-interaktiven Teleskopierung"-Methode verwendet werden. Siehe das tunnel-Build-Dokument [TUNNEL-IMPL](/docs/specs/tunnel-implementation) für einen Überblick über den Prozess, einschließlich Peer-Auswahl und Anordnungsmethoden.

Die Tunnel-Erstellung wird durch eine einzige Nachricht bewerkstelligt, die entlang des Pfades der Peers im Tunnel weitergegeben, vor Ort umgeschrieben und an den Tunnel-Ersteller zurückübertragen wird. Diese einzelne Tunnel-Nachricht besteht aus einer variablen Anzahl von Datensätzen (bis zu 8) - einen für jeden potenziellen Peer im Tunnel. Einzelne Datensätze werden asymmetrisch (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) verschlüsselt, um nur von einem bestimmten Peer entlang des Pfades gelesen werden zu können, während eine zusätzliche symmetrische Verschlüsselungsebene (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) an jedem Hop hinzugefügt wird, um den asymmetrisch verschlüsselten Datensatz nur zum angemessenen Zeitpunkt freizulegen.

### Anzahl der Datensätze {#number}

Nicht alle Datensätze müssen gültige Daten enthalten. Die Build-Nachricht für einen 3-Hop-Tunnel kann beispielsweise mehr Datensätze enthalten, um die tatsächliche Länge des Tunnels vor den Teilnehmern zu verbergen. Es gibt zwei Arten von Build-Nachrichten. Die ursprüngliche Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) enthält 8 Datensätze, was mehr als ausreichend für jede praktische Tunnellänge ist. Die neuere Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) enthält 1 bis 8 Datensätze. Der Initiator kann zwischen der Größe der Nachricht und dem gewünschten Maß an Tunnellängen-Verschleierung abwägen.

Im aktuellen Netzwerk sind die meisten tunnel 2 oder 3 Hops lang. Die aktuelle Implementierung verwendet eine 5-Datensatz VTBM um tunnel mit 4 Hops oder weniger zu erstellen, und die 8-Datensatz TBM für längere tunnel. Die 5-Datensatz VTBM (die, wenn fragmentiert, in drei 1KB tunnel-Nachrichten passt) reduziert den Netzwerkverkehr und erhöht die Erfolgsrate beim Erstellen, da kleinere Nachrichten weniger wahrscheinlich verworfen werden.

Die Antwortnachricht muss denselben Typ und dieselbe Länge wie die Build-Nachricht haben.

### Request Record Spezifikation {#tunnelcreate-requestrecord}

Auch spezifiziert in der I2NP-Spezifikation [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Klartext des Datensatzes, nur für den angefragten Hop sichtbar:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Die Felder "next tunnel ID" und "next router identity hash" werden verwendet, um den nächsten Hop im tunnel anzugeben, obwohl sie bei einem ausgehenden tunnel-Endpunkt angeben, wohin die umgeschriebene tunnel-Erstellungsantwortnachricht gesendet werden soll. Zusätzlich gibt die "next message ID" die Nachrichten-ID an, die die Nachricht (oder Antwort) verwenden soll.

Der tunnel layer key, tunnel IV key, reply key und reply IV sind jeweils zufällige 32-Byte-Werte, die vom Ersteller generiert werden und nur für diesen Build-Request-Datensatz verwendet werden.

Das Flags-Feld enthält folgende Informationen:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit 7 zeigt an, dass der Hop ein inbound gateway (IBGW) sein wird. Bit 6 zeigt an, dass der Hop ein outbound endpoint (OBEP) sein wird. Wenn keines der beiden Bits gesetzt ist, wird der Hop ein Zwischenteilnehmer sein. Beide können nicht gleichzeitig gesetzt werden.

#### Erstellung von Anfrage-Datensätzen

Jeder Hop erhält eine zufällige Tunnel-ID, die nicht null ist. Die aktuellen und nächsten Hop-Tunnel-IDs werden ausgefüllt. Jeder Datensatz erhält einen zufälligen tunnel IV-Schlüssel, Antwort-IV, Schichtschlüssel und Antwortschlüssel.

#### Request Record Encryption {#encryption}

Dieser Klartext-Datensatz wird mit ElGamal 2048 verschlüsselt [CRYPTO-ELG](/docs/specs/cryptography#elgamal) unter Verwendung des öffentlichen Verschlüsselungsschlüssels des Hops und in einen 528 Byte Datensatz formatiert:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
Im 512-Byte verschlüsselten Datensatz enthalten die ElGamal-Daten die Bytes 1-256 und 258-513 des 514-Byte ElGamal verschlüsselten Blocks [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Die beiden Padding-Bytes aus dem Block (die Null-Bytes an den Positionen 0 und 257) werden entfernt.

Da der Klartext das gesamte Feld verwendet, ist keine zusätzliche Auffüllung über `SHA256(cleartext) + cleartext` hinaus erforderlich.

Jeder 528-Byte-Datensatz wird dann iterativ verschlüsselt (unter Verwendung von AES-Entschlüsselung, mit dem Antwortschlüssel und der Antwort-IV für jeden Hop), so dass die Router-Identität nur für den betreffenden Hop im Klartext vorliegt.

### Hop-Verarbeitung und Verschlüsselung {#tunnelcreate-hopprocessing}

Wenn ein Hop eine TunnelBuildMessage erhält, durchsucht er die darin enthaltenen Datensätze nach einem, der mit seinem eigenen Identity-Hash beginnt (auf 16 Bytes gekürzt). Anschließend entschlüsselt er den ElGamal-Block aus diesem Datensatz und ruft den geschützten Klartext ab. An diesem Punkt stellen sie sicher, dass die Tunnel-Anfrage kein Duplikat ist, indem sie den AES-256-Antwortschlüssel in einen Bloom-Filter einspeisen. Duplikate oder ungültige Anfragen werden verworfen. Datensätze, die nicht mit der aktuellen Stunde oder der vorherigen Stunde gestempelt sind (falls kurz nach der vollen Stunde), müssen verworfen werden. Zum Beispiel: Nimm die Stunde aus dem Zeitstempel, wandle sie in eine vollständige Zeit um, und wenn sie mehr als 65 Minuten zurück oder 5 Minuten voraus zur aktuellen Zeit liegt, ist sie ungültig. Der Bloom-Filter muss eine Dauer von mindestens einer Stunde haben (plus ein paar Minuten, um Uhrenabweichungen zu berücksichtigen), damit doppelte Datensätze in der aktuellen Stunde, die nicht durch Prüfung des Stunden-Zeitstempels im Datensatz abgelehnt werden, vom Filter abgelehnt werden.

Nachdem sie entschieden haben, ob sie der Teilnahme am tunnel zustimmen oder nicht, ersetzen sie den Datensatz, der die Anfrage enthielt, durch einen verschlüsselten Antwortblock. Alle anderen Datensätze werden mit AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) unter Verwendung des enthaltenen Antwortschlüssels und IV verschlüsselt. Jeder wird separat mit AES/CBC unter Verwendung desselben Antwortschlüssels und Antwort-IV verschlüsselt. Der CBC-Modus wird nicht über Datensätze hinweg fortgesetzt (verkettet).

Jeder Hop kennt nur seine eigene Antwort. Wenn er zustimmt, wird er den tunnel bis zum Ablauf aufrechterhalten, auch wenn er nicht genutzt wird, da er nicht wissen kann, ob alle anderen Hops zugestimmt haben.

#### Reply Record Spezifikation {#tunnelcreate-replyrecord}

Nachdem der aktuelle Hop seinen Datensatz gelesen hat, ersetzt er ihn durch einen Antwortdatensatz, der angibt, ob er der Teilnahme am Tunnel zustimmt oder nicht, und falls nicht, klassifiziert er seinen Ablehnungsgrund. Dies ist einfach ein 1-Byte-Wert, wobei 0x0 bedeutet, dass er der Teilnahme am Tunnel zustimmt, und höhere Werte höhere Ablehnungsgrade bedeuten.

Die folgenden Ablehnungscodes sind definiert:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Um andere Ursachen, wie das Herunterfahren des routers, vor Peers zu verbergen, verwendet die aktuelle Implementierung TUNNEL_REJECT_BANDWIDTH für fast alle Ablehnungen.

Die Antwort wird mit dem AES-Sitzungsschlüssel verschlüsselt, der ihr im verschlüsselten Block übermittelt wurde, und mit 495 Bytes zufälliger Daten aufgefüllt, um die vollständige Datensatzgröße zu erreichen. Das Padding wird vor dem Status-Byte platziert:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Dies wird auch in der I2NP-Spezifikation [BRR](/docs/specs/i2np#struct-buildrequestrecord) beschrieben.

### Tunnel Build Message Vorbereitung {#tunnelcreate-requestpreparation}

Beim Erstellen einer neuen Tunnel Build Message müssen zunächst alle Build Request Records erstellt und asymmetrisch mit ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal) verschlüsselt werden. Jeder Record wird dann vorausschauend mit den Antwortschlüsseln und IVs der Hops entschlüsselt, die früher im Pfad liegen, unter Verwendung von AES [CRYPTO-AES](/docs/specs/cryptography#AES). Diese Entschlüsselung sollte in umgekehrter Reihenfolge ausgeführt werden, damit die asymmetrisch verschlüsselten Daten im Klartext am richtigen Hop erscheinen, nachdem ihr Vorgänger sie verschlüsselt hat.

Die überschüssigen Datensätze, die nicht für einzelne Anfragen benötigt werden, werden vom Ersteller einfach mit zufälligen Daten gefüllt.

### Tunnel Build Message Delivery {#tunnelcreate-requestdelivery}

Für ausgehende tunnel wird die Zustellung direkt vom tunnel-Ersteller zum ersten Hop durchgeführt, wobei die TunnelBuildMessage so verpackt wird, als wäre der Ersteller nur ein weiterer Hop im tunnel. Für eingehende tunnel erfolgt die Zustellung über einen bestehenden ausgehenden tunnel. Der ausgehende tunnel stammt in der Regel aus demselben Pool wie der neue tunnel, der gebaut wird. Wenn in diesem Pool kein ausgehender tunnel verfügbar ist, wird ein ausgehender Erkundungs-tunnel verwendet. Beim Start, wenn noch kein ausgehender Erkundungs-tunnel existiert, wird ein falscher 0-Hop ausgehender tunnel verwendet.

### Tunnel Build Message Endpoint Handling {#tunnelcreate-endpointhandling}

Für die Erstellung eines ausgehenden tunnels wird, wenn die Anfrage einen ausgehenden Endpunkt erreicht (wie durch das 'allow messages to anyone' Flag bestimmt), der Hop wie üblich verarbeitet, wobei eine Antwort anstelle des Datensatzes verschlüsselt und alle anderen Datensätze verschlüsselt werden. Da es jedoch keinen 'nächsten Hop' gibt, an den die TunnelBuildMessage weitergeleitet werden kann, platziert er stattdessen die verschlüsselten Antwortdatensätze in eine TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) oder VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (der Nachrichtentyp und die Anzahl der Datensätze müssen mit denen der Anfrage übereinstimmen) und liefert sie an den im Anfragedatensatz angegebenen Antworttunnel. Dieser Antworttunnel leitet die Tunnel Build Reply Message zurück an den tunnel-Ersteller weiter, genau wie bei jeder anderen Nachricht [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). Der tunnel-Ersteller verarbeitet sie dann wie unten beschrieben.

Der Reply-Tunnel wurde vom Ersteller wie folgt ausgewählt: Im Allgemeinen ist es ein eingehender Tunnel aus demselben Pool wie der neue ausgehende Tunnel, der gebaut wird. Wenn kein eingehender Tunnel in diesem Pool verfügbar ist, wird ein eingehender Explorations-Tunnel verwendet. Beim Systemstart, wenn noch kein eingehender Explorations-Tunnel existiert, wird ein gefälschter 0-Hop eingehender Tunnel verwendet.

Für die Erstellung eines inbound tunnel, wenn die Anfrage den inbound endpoint (auch bekannt als tunnel creator) erreicht, ist es nicht erforderlich, eine explizite Tunnel Build Reply Message zu generieren, und der router verarbeitet jede der Antworten wie folgt.

### Tunnel Build Reply Message Processing {#tunnelcreate-replyprocessing}

Um die Antwort-Datensätze zu verarbeiten, muss der Ersteller einfach jeden Datensatz einzeln AES-entschlüsseln, wobei er den Antwortschlüssel und IV jedes Hops im tunnel nach dem Peer verwendet (in umgekehrter Reihenfolge). Dies legt dann die Antwort frei, die angibt, ob sie der Teilnahme am tunnel zustimmen oder warum sie ablehnen. Wenn alle zustimmen, gilt der tunnel als erstellt und kann sofort verwendet werden, aber wenn jemand ablehnt, wird der tunnel verworfen.

Die Zustimmungen und Ablehnungen werden im Profil jedes Peers [PEER-SELECTION](/docs/overview/peer-selection) vermerkt, um bei zukünftigen Bewertungen der Peer-tunnel-Kapazität verwendet zu werden.

## Geschichte und Hinweise {#tunnelcreate-notes}

Diese Strategie entstand während einer Diskussion in der I2P-Mailingliste zwischen Michael Rogers, Matthew Toseland (toad) und jrandom bezüglich des Predecessor-Angriffs. Siehe [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Sie wurde in Release 0.6.1.10 am 2006-02-16 eingeführt, was das letzte Mal war, dass eine nicht-rückwärtskompatible Änderung in I2P vorgenommen wurde.

Hinweise:

- Dieses Design verhindert nicht, dass zwei feindliche Peers innerhalb eines tunnels ein oder mehrere Anfrage- oder Antwortdatensätze markieren, um zu erkennen, dass sie sich im selben tunnel befinden, aber dies kann vom tunnel-Ersteller beim Lesen der Antwort erkannt werden, wodurch der tunnel als ungültig markiert wird.

- Dieses Design enthält keinen Proof-of-Work für den asymmetrisch verschlüsselten Abschnitt, obwohl der 16-Byte-Identity-Hash halbiert werden könnte, wobei die zweite Hälfte durch eine Hashcash-Funktion mit Kosten von bis zu 2^64 ersetzt wird.

- Dieses Design allein verhindert nicht, dass zwei feindliche Peers innerhalb eines tunnels Timing-Informationen verwenden, um zu bestimmen, ob sie sich im selben tunnel befinden. Die Verwendung von gestapelter und synchronisierter Anfragenzustellung könnte helfen (Anfragen sammeln und sie zur (ntp-synchronisierten) Minute versenden). Dies ermöglicht jedoch Peers, die Anfragen zu 'markieren', indem sie diese verzögern und die Verzögerung später im tunnel erkennen, obwohl das Verwerfen von Anfragen, die nicht in einem kleinen Zeitfenster zugestellt werden, funktionieren könnte (dies würde jedoch einen hohen Grad an Uhren-Synchronisation erfordern). Alternativ könnten vielleicht einzelne Hops eine zufällige Verzögerung einfügen, bevor sie die Anfrage weiterleiten?

- Gibt es nicht-fatale Methoden, um die Anfrage zu kennzeichnen?

- Der Zeitstempel mit einer Auflösung von einer Stunde wird zur Replay-Verhinderung verwendet. Die Beschränkung wurde erst ab Release 0.9.16 durchgesetzt.

## Zukünftige Arbeiten {#future}

- In der aktuellen Implementierung lässt der Originator einen Datensatz für sich selbst leer. Daher kann eine Nachricht mit n Datensätzen nur einen tunnel mit n-1 Hops aufbauen. Dies scheint für eingehende tunnels notwendig zu sein (wo der vorletzte Hop das Hash-Präfix für den nächsten Hop sehen kann), aber nicht für ausgehende tunnels. Dies ist zu erforschen und zu verifizieren. Falls es möglich ist, den verbleibenden Datensatz zu verwenden, ohne die Anonymität zu gefährden, sollten wir das tun.

- Weitere Analyse möglicher Tagging- und Timing-Angriffe, die in den
  obigen Hinweisen beschrieben werden.

- Verwende nur VTBM; wähle keine alten Peers aus, die es nicht unterstützen.

- Der Build Request Record spezifiziert keine tunnel-Lebensdauer oder -Ablaufzeit;
  jeder Hop lässt den tunnel nach 10 Minuten ablaufen, was eine netzwerkweite
  hartcodierte Konstante ist. Wir könnten ein Bit im Flag-Feld verwenden und 4 (oder 8)
  Bytes aus dem Padding nehmen, um eine Lebensdauer oder Ablaufzeit zu spezifizieren. Der Anforderer
  würde diese Option nur angeben, wenn alle Teilnehmer sie unterstützen würden.

## Referenzen {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
