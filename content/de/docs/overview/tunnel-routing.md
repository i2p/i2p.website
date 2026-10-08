---
title: "Tunnel-Routing"
description: "Überblick über I2P tunnel Terminologie, Aufbau und Betrieb"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Überblick

Diese Seite enthält einen Überblick über I2P tunnel-Terminologie und -Betrieb, mit Links zu technischeren Seiten, Details und Spezifikationen.

Wie kurz in der [Einführung](/docs/overview/intro/) erklärt, baut I2P virtuelle "tunnels" auf - temporäre und unidirektionale Pfade durch eine Sequenz von routern. Diese tunnels werden entweder als inbound tunnels klassifiziert (wo alles, was ihnen gegeben wird, zum Ersteller des tunnels geht) oder outbound tunnels (wo der tunnel-Ersteller Nachrichten von sich wegschiebt). Wenn Alice eine Nachricht an Bob senden möchte, sendet sie diese (typischerweise) über einen ihrer bestehenden outbound tunnels mit Anweisungen für den Endpunkt dieses tunnels, sie an den Gateway-router für einen von Bobs aktuellen inbound tunnels weiterzuleiten, der sie wiederum an Bob weitergibt.

![Alice verbindet sich über ihren ausgehenden Tunnel mit Bob über seinen eingehenden Tunnel](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Tunnel-Vokabular

- **Tunnel gateway** - der erste router in einem tunnel. Bei eingehenden tunnels ist dies derjenige, der im LeaseSet erwähnt wird, das in der [Netzwerkdatenbank](/docs/overview/network-database/) veröffentlicht ist. Bei ausgehenden tunnels ist das gateway der ursprüngliche router. (z.B. sowohl A als auch D oben)

- **Tunnel-Endpunkt** - der letzte router in einem tunnel. (z.B. sowohl C als auch F oben)

- **Tunnel-Teilnehmer** - alle Router in einem tunnel außer dem Gateway oder Endpunkt (z.B. sowohl B als auch E oben)

- **n-Hop tunnel** - ein tunnel mit einer bestimmten Anzahl von Router-zu-Router-Sprüngen, z.B.:
  - **0-hop tunnel** - ein tunnel, bei dem das Gateway auch der Endpunkt ist
  - **1-hop tunnel** - ein tunnel, bei dem das Gateway direkt mit dem Endpunkt kommuniziert
  - **2-(oder mehr)-hop tunnel** - ein tunnel, bei dem es mindestens einen zwischengeschalteten tunnel-Teilnehmer gibt. (das obige Diagramm enthält zwei 2-hop tunnels - einen ausgehenden von Alice, einen eingehenden zu Bob)

- **Tunnel ID** - Eine [4-Byte-Ganzzahl](/docs/specs/common-structures/#type_TunnelId), die für jeden Hop in einem tunnel unterschiedlich und unter allen tunnels auf einem router eindeutig ist. Wird zufällig vom tunnel-Ersteller gewählt.

---

## Tunnel-Build-Informationen

Router, die die drei Rollen (Gateway, Teilnehmer, Endpunkt) ausführen, erhalten unterschiedliche Datenteile in der anfänglichen [Tunnel Build Message](/docs/specs/tunnel-creation/), um ihre Aufgaben zu erfüllen:

**Das Tunnel-Gateway erhält:**

- **tunnel encryption key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln von Nachrichten und Anweisungen an den nächsten Hop
- **tunnel IV key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum doppelten Verschlüsseln des IV an den nächsten Hop
- **reply key** - ein [AES öffentlicher Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln der Antwort auf die tunnel Build-Anfrage
- **reply IV** - der IV zum Verschlüsseln der Antwort auf die tunnel Build-Anfrage
- **tunnel id** - 4-Byte-Integer (nur eingehende Gateways)
- **next hop** - welcher router der nächste im Pfad ist (außer dies ist ein 0-Hop-tunnel und das Gateway ist auch der Endpunkt)
- **next tunnel id** - Die tunnel ID am nächsten Hop

**Alle zwischenliegenden Tunnel-Teilnehmer erhalten:**

- **tunnel encryption key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln von Nachrichten und Anweisungen an den nächsten hop
- **tunnel IV key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum doppelten Verschlüsseln des IV an den nächsten hop
- **reply key** - ein [AES öffentlicher Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln der Antwort auf die tunnel-Build-Anfrage
- **reply IV** - das IV zum Verschlüsseln der Antwort auf die tunnel-Build-Anfrage
- **tunnel id** - 4-Byte-Integer
- **next hop** - welcher router der nächste im Pfad ist
- **next tunnel id** - Die tunnel-ID auf dem nächsten hop

**Der tunnel-Endpunkt erhält:**

- **tunnel encryption key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln von Nachrichten und Anweisungen an den Endpunkt (sich selbst)
- **tunnel IV key** - ein [AES privater Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum doppelten Verschlüsseln der IV an den Endpunkt (sich selbst)
- **reply key** - ein [AES öffentlicher Schlüssel](/docs/specs/common-structures/#type_SessionKey) zum Verschlüsseln der Antwort auf die tunnel build Anfrage (nur ausgehende Endpunkte)
- **reply IV** - die IV zum Verschlüsseln der Antwort auf die tunnel build Anfrage (nur ausgehende Endpunkte)
- **tunnel id** - 4-Byte-Ganzzahl (nur ausgehende Endpunkte)
- **reply router** - das eingehende Gateway des tunnels, über das die Antwort gesendet werden soll (nur ausgehende Endpunkte)
- **reply tunnel id** - Die tunnel ID des reply routers (nur ausgehende Endpunkte)

Details sind in der [tunnel creation specification](/docs/specs/tunnel-creation/) zu finden.

---

## Tunnel Pooling

Mehrere tunnel für einen bestimmten Zweck können in einen "tunnel pool" gruppiert werden, wie in der [tunnel-Spezifikation](/docs/specs/tunnel-implementation/#tunnel.pooling) beschrieben. Dies bietet Redundanz und zusätzliche Bandbreite. Die vom router selbst verwendeten Pools werden "exploratory tunnels" genannt. Die von Anwendungen verwendeten Pools werden "client tunnels" genannt.

---

## Tunnel-Länge

Wie oben erwähnt, verlangt jeder Client, dass sein router tunnels bereitstellt, die mindestens eine bestimmte Anzahl von Hops enthalten. Die Entscheidung darüber, wie viele router in den ausgehenden und eingehenden tunnels enthalten sein sollen, hat einen wichtigen Einfluss auf die Latenz, den Durchsatz, die Zuverlässigkeit und die Anonymität, die I2P bietet - je mehr Peers, durch die Nachrichten gehen müssen, desto länger dauert es, bis sie ankommen, und desto wahrscheinlicher ist es, dass einer dieser router vorzeitig ausfällt. Je weniger router in einem tunnel, desto einfacher ist es für einen Angreifer, Traffic-Analyse-Angriffe durchzuführen und die Anonymität einer Person zu durchbrechen. Tunnel-Längen werden von Clients über [I2CP-Optionen](/docs/specs/i2cp/#options) spezifiziert. Die maximale Anzahl von Hops in einem tunnel beträgt 7.

### 0-hop tunnels

Ohne entfernte router in einem tunnel hat der Benutzer nur eine sehr grundlegende plausible Abstreitbarkeit (da niemand sicher weiß, dass der Peer, der ihm die Nachricht gesendet hat, sie nicht einfach nur als Teil des tunnels weitergeleitet hat). Es wäre jedoch relativ einfach, einen statistischen Analyseangriff zu starten und zu bemerken, dass Nachrichten, die auf ein bestimmtes Ziel abzielen, immer über ein einziges Gateway gesendet werden. Statistische Analysen gegen ausgehende 0-Hop-tunnels sind komplexer, könnten aber ähnliche Informationen zeigen (wären jedoch etwas schwieriger durchzuführen).

### 1-Hop tunnels

Mit nur einem entfernten Router in einem tunnel hat der Benutzer sowohl plausible Abstreitbarkeit als auch grundlegende Anonymität, solange er nicht gegen einen internen Gegner antritt (wie im [Bedrohungsmodell](/docs/overview/threat-model/) beschrieben). Wenn der Gegner jedoch eine ausreichende Anzahl von Routern betreibt, sodass der einzelne entfernte Router im tunnel oft einer dieser kompromittierten Router ist, könnte er den oben beschriebenen statistischen Verkehrsanalyse-Angriff durchführen.

### 2-Hop-Tunnel

Bei zwei oder mehr remote routers in einem tunnel steigen die Kosten für die Durchführung einer Traffic-Analyse-Attacke, da viele remote routers kompromittiert werden müssten, um sie durchzuführen.

### 3-Hop (oder mehr) Tunnel

Um die Anfälligkeit für [bestimmte Angriffe](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) zu verringern, werden 3 oder mehr Hops für den höchsten Schutzgrad empfohlen. [Aktuelle Studien](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) kommen außerdem zu dem Schluss, dass mehr als 3 Hops keinen zusätzlichen Schutz bieten.

### Standard-Tunnel-Längen

Der router verwendet standardmäßig 2-Hop-tunnel für seine explorativen tunnel. Die Standard-Einstellungen für Client-tunnel werden von der Anwendung festgelegt, unter Verwendung von [I2CP-Optionen](/docs/specs/i2cp/#options). Die meisten Anwendungen verwenden standardmäßig 2 oder 3 Hops.

---

## Tunnel-Tests

Alle tunnel werden regelmäßig von ihrem Ersteller getestet, indem eine DeliveryStatusMessage durch einen ausgehenden tunnel gesendet wird, die für einen anderen eingehenden tunnel bestimmt ist (wodurch beide tunnel gleichzeitig getestet werden). Falls einer der tunnel mehrere aufeinanderfolgende Tests nicht besteht, wird er als nicht mehr funktionsfähig markiert. Wenn er für den eingehenden tunnel eines Clients verwendet wurde, wird ein neues leaseSet erstellt. Tunnel-Testfehler spiegeln sich auch in der [Kapazitätsbewertung im Peer-Profil](/docs/overview/peer-selection/#capacity) wider.

---

Die Tunnel-Erstellung wird durch [garlic routing](/docs/overview/garlic-routing/) abgewickelt, indem eine Tunnel Build Message an einen router gesendet wird, mit der Bitte, dass dieser am tunnel teilnimmt (wobei alle entsprechenden Informationen wie oben beschrieben sowie ein Zertifikat bereitgestellt werden, das derzeit ein 'null'-Zertifikat ist, aber bei Bedarf hashcash oder andere kostenpflichtige Zertifikate unterstützen wird). Dieser router leitet die Nachricht an den nächsten Hop im tunnel weiter. Details finden sich in der [tunnel creation specification](/docs/specs/tunnel-creation/).

## Tunnel-Erstellung

---

Mehrschichtige Verschlüsselung wird durch [garlic encryption](/docs/overview/garlic-routing/) von tunnel-Nachrichten behandelt. Details finden sich in der [tunnel-Spezifikation](/docs/specs/tunnel-implementation/). Der IV jedes Hops wird mit einem separaten Schlüssel verschlüsselt, wie dort erläutert.

## Tunnel-Verschlüsselung

---

---

## Zukünftige Arbeiten

- Andere Tunnel-Testtechniken könnten verwendet werden, wie zum Beispiel garlic wrapping einer Anzahl von Tests in Cloves, das separate Testen einzelner Tunnel-Teilnehmer, etc.

- Wechsel zu 3-Hop-Exploratory-Tunnel-Standards.

- In einer zukünftigen Version könnten Optionen zur Konfiguration der Pooling-, Mixing- und Chaff-Generierungseinstellungen implementiert werden.

- In einer zukünftigen Version könnten Limits für die Anzahl und Größe der Nachrichten implementiert werden, die während der Lebensdauer des tunnels erlaubt sind (z.B. nicht mehr als 300 Nachrichten oder 1MB pro Minute).

---

## Siehe auch

- [Tunnel-Spezifikation](/docs/specs/tunnel-implementation/)
- [Tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation/)
- [Unidirektionale tunnel](/docs/legacy/unidirectional/)
- [Tunnel-Nachrichten-Spezifikation](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP-Optionen](/docs/specs/i2cp/#options)
