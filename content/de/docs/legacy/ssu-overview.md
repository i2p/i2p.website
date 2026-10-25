---
title: "Secure Semireliable UDP (SSU)"
description: "Ursprünglicher UDP-Transport, der vor SSU2 verwendet wurde (veraltet)"
slug: "ssu-overview"
aliases:
  - "/de/udp"
  - "/de/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**VERALTET** - SSU wurde durch SSU2 ersetzt. SSU-Unterstützung wurde aus i2pd in Release 2.44.0 (API 0.9.56) 2022-11 entfernt. SSU-Unterstützung wurde aus Java I2P in Release 2.4.0 (API 0.9.61) 2023-12 entfernt.

SSU (auch als "UDP" in einem Großteil der I2P-Dokumentation und Benutzeroberflächen bezeichnet) war einer von zwei [Transportprotokollen](/docs/transport), die in I2P implementiert wurden. Das andere ist [NTCP2](/docs/specs/ntcp2). Die Unterstützung für [NTCP](/docs/legacy/ntcp) wurde entfernt.

SSU wurde in I2P Release 0.6 eingeführt. In einer Standard-I2P-Installation verwendet der router sowohl NTCP als auch SSU für ausgehende Verbindungen. SSU-über-IPv6 wird ab Version 0.9.8 unterstützt.

SSU wird als "semizuverlässig" bezeichnet, weil es unbestätigte Nachrichten wiederholt erneut überträgt, aber nur bis zu einer maximalen Anzahl von Versuchen. Danach wird die Nachricht verworfen.

## SSU Services

Wie der NTCP-Transport bietet SSU zuverlässigen, verschlüsselten, verbindungsorientierten, punkt-zu-punkt Datentransport. Einzigartig für SSU ist, dass es auch IP-Erkennung und NAT-Traversal-Dienste bereitstellt, einschließlich:

- Kooperative NAT/Firewall-Durchquerung mittels [introducers](#introduction)
- Lokale IP-Erkennung durch Inspektion eingehender Pakete und [peer testing](#peerTesting)
- Übermittlung des Firewall-Status und der lokalen IP sowie Änderungen daran an NTCP
- Übermittlung des Firewall-Status und der lokalen IP sowie Änderungen daran an den router und die Benutzeroberfläche

## Router-Adress-Spezifikation {#ra}

Die folgenden Eigenschaften werden in der netDb gespeichert.

- **Transport name:** SSU
- **caps:** [B,C,4,6] [Siehe unten](#capabilities).
- **host:** IP (IPv4 oder IPv6).
  Verkürzte IPv6-Adresse (mit "::") ist erlaubt.
  Kann vorhanden sein oder nicht, wenn durch Firewall geschützt.
  Host-Namen waren früher erlaubt, sind aber ab Release 0.9.32 veraltet. Siehe Vorschlag 141.
- **iexp[0-2]:** Ablaufzeit dieses Introducers.
  ASCII-Ziffern, in Sekunden seit der Epoche.
  Nur vorhanden wenn durch Firewall geschützt und Introducer erforderlich sind.
  Optional (auch wenn andere Eigenschaften für diesen Introducer vorhanden sind).
  Ab Release 0.9.30, Vorschlag 133.
- **ihost[0-2]:** IP des Introducers (IPv4 oder IPv6).
  Host-Namen waren früher erlaubt, sind aber ab Release 0.9.32 veraltet. Siehe Vorschlag 141.
  Verkürzte IPv6-Adresse (mit "::") ist erlaubt.
  Nur vorhanden wenn durch Firewall geschützt und Introducer erforderlich sind.
  [Siehe unten](#introduction).
- **ikey[0-2]:** Base 64 Introduction Key des Introducers. [Siehe unten](#key).
  Nur vorhanden wenn durch Firewall geschützt und Introducer erforderlich sind.
  [Siehe unten](#introduction).
- **iport[0-2]:** Port des Introducers 1024 - 65535.
  Nur vorhanden wenn durch Firewall geschützt und Introducer erforderlich sind.
  [Siehe unten](#introduction).
- **itag[0-2]:** Tag des Introducers 1 - (2^32 - 1)
  ASCII-Ziffern.
  Nur vorhanden wenn durch Firewall geschützt und Introducer erforderlich sind.
  [Siehe unten](#introduction).
- **key:** Base 64 Introduction Key. [Siehe unten](#key).
- **mtu:** Optional. Standard und Maximum ist 1484. Minimum ist 620.
  Muss für IPv6 vorhanden sein, wo das Minimum 1280 und das Maximum 1488 ist
  (Maximum war 1472 vor Version 0.9.28).
  IPv6 MTU muss ein Vielfaches von 16 sein.
  (IPv4 MTU + 4) muss ein Vielfaches von 16 sein.
  [Siehe unten](#mtu).
- **port:** 1024 - 65535
  Kann vorhanden sein oder nicht, wenn durch Firewall geschützt.

# Protokolldetails

## Congestion Control {#congestioncontrol}

SSUs Bedarf nach nur halbzuverlässiger Übertragung, TCP-freundlichem Betrieb und der Fähigkeit zu hohem Durchsatz ermöglicht einen großen Spielraum bei der Staukontrolle. Der unten beschriebene Staukontrollalgorithmus soll sowohl bandbreiteneffizient als auch einfach zu implementieren sein.

Pakete werden gemäß der router-Richtlinie geplant, wobei darauf geachtet wird, die ausgehende Kapazität des routers nicht zu überschreiten oder die gemessene Kapazität des entfernten Peers zu übersteigen. Die gemessene Kapazität funktioniert ähnlich wie TCPs Slow Start und Congestion Avoidance, mit additiven Erhöhungen der Sendekapazität und multiplikativen Verringerungen bei Überlastung. Anders als bei TCP können router nach einer bestimmten Zeit oder Anzahl von Übertragungswiederholungen bestimmte Nachrichten aufgeben, während sie andere Nachrichten weiterhin übertragen.

Die Techniken zur Stauerkennlung unterscheiden sich ebenfalls von TCP, da jede Nachricht ihre eigene eindeutige und nicht-sequentielle Kennung hat und jede Nachricht eine begrenzte Größe hat - höchstens 32KB. Um dieses Feedback effizient an den Sender zu übertragen, fügt der Empfänger regelmäßig eine Liste der vollständig bestätigten Nachrichten-Kennungen hinzu und kann auch Bitfelder für teilweise empfangene Nachrichten einschließen, wobei jedes Bit den Empfang eines Fragments repräsentiert. Wenn doppelte Fragmente ankommen, sollte die Nachricht erneut bestätigt werden, oder wenn die Nachricht noch nicht vollständig empfangen wurde, sollte das Bitfeld mit allen neuen Updates erneut übertragen werden.

Die aktuelle Implementierung füllt die Pakete nicht auf eine bestimmte Größe auf, sondern platziert einfach ein einzelnes Nachrichtenfragment in ein Paket und sendet es ab (dabei wird darauf geachtet, die MTU nicht zu überschreiten).

### MTU {#mtu}

Ab Router-Version 0.8.12 werden zwei MTU-Werte für IPv4 verwendet: 620 und 1484. Der MTU-Wert wird basierend auf dem Prozentsatz der Pakete angepasst, die erneut übertragen werden.

Für beide MTU-Werte ist es wünschenswert, dass (MTU % 16) == 12, damit der Payload-Teil nach dem 28-Byte IP/UDP-Header ein Vielfaches von 16 Bytes ist, für Verschlüsselungszwecke.

Für den kleinen MTU-Wert ist es wünschenswert, eine 2646-Byte Variable Tunnel Build Message effizient in mehrere Pakete zu packen; mit einer 620-Byte MTU passt sie schön in 5 Pakete.

Basierend auf Messungen passt 1492 zu nahezu allen angemessen kleinen I2NP-Nachrichten (größere I2NP-Nachrichten können bis zu 1900 bis 4500 Bytes groß sein, was ohnehin nicht in eine Live-Netzwerk-MTU passen würde).

Die MTU-Werte betrugen 608 und 1492 für die Versionen 0.8.9 - 0.8.11. Die große MTU war 1350 vor Version 0.8.9.

Die maximale Empfangspaketgröße beträgt seit Release 0.8.12 1571 Bytes. Für die Releases 0.8.9 - 0.8.11 waren es 1535 Bytes. Vor Release 0.8.9 waren es 2048 Bytes.

Ab Version 0.9.2 wird ein router, dessen Netzwerkschnittstellen-MTU weniger als 1484 beträgt, dies in der netDb veröffentlichen, und andere router sollten dies beim Aufbau einer Verbindung berücksichtigen.

Für IPv6 beträgt die minimale MTU 1280. Der IPv6 IP/UDP-Header ist 48 Bytes groß, daher verwenden wir eine MTU, bei der (MTU % 16 == 0) gilt, was für 1280 zutrifft. Die maximale IPv6 MTU beträgt 1488. (das Maximum war 1472 vor Version 0.9.28).

### Nachrichtengrößenbeschränkungen {#max}

Während die maximale Nachrichtengröße nominell 32KB beträgt, unterscheidet sich das praktische Limit. Das Protokoll begrenzt die Anzahl der Fragmente auf 7 Bits oder 128. Die aktuelle Implementierung begrenzt jedoch jede Nachricht auf maximal 64 Fragmente, was für 64 * 534 = 33,3 KB bei Verwendung der 608 MTU ausreicht. Aufgrund des Overheads für gebündelte LeaseSets und Session-Keys liegt das praktische Limit auf Anwendungsebene etwa 6KB niedriger, oder etwa 26KB. Weitere Arbeit ist notwendig, um das UDP-Transport-Limit über 32KB zu heben. Für Verbindungen mit der größeren MTU sind größere Nachrichten möglich.

## Leerlauf-Timeout

Die Leerlauf-Zeitüberschreitung und das Schließen von Verbindungen liegt im Ermessen jedes Endpunkts und kann variieren. Die aktuelle Implementierung verkürzt die Zeitüberschreitung, wenn sich die Anzahl der Verbindungen dem konfigurierten Maximum nähert, und verlängert die Zeitüberschreitung, wenn die Verbindungsanzahl niedrig ist. Die empfohlene Mindest-Zeitüberschreitung beträgt zwei Minuten oder mehr, und die empfohlene Höchst-Zeitüberschreitung beträgt zehn Minuten oder mehr.

## Schlüssel {#keys}

Alle verwendete Verschlüsselung ist AES256/CBC mit 32-Byte-Schlüsseln und 16-Byte-IVs. Wenn Alice eine Sitzung mit Bob initiiert, werden die MAC- und Sitzungsschlüssel als Teil des DH-Austauschs ausgehandelt und dann für den HMAC bzw. die Verschlüsselung verwendet. Während des DH-Austauschs wird Bobs öffentlich bekannter introKey für den MAC und die Verschlüsselung verwendet.

Sowohl die ursprüngliche Nachricht als auch die nachfolgende Antwort verwenden den introKey des Antwortenden (Bob) - der Antwortende muss den introKey des Anfragenden (Alice) nicht kennen. Der von Bob verwendete DSA-Signaturschlüssel sollte Alice bereits bekannt sein, wenn sie ihn kontaktiert, obwohl Alices DSA-Schlüssel Bob möglicherweise noch nicht bekannt ist.

Beim Empfang einer Nachricht überprüft der Empfänger die "from" IP-Adresse und den Port mit allen etablierten Sitzungen - falls es Übereinstimmungen gibt, werden die MAC-Schlüssel dieser Sitzung im HMAC getestet. Wenn keine davon verifiziert werden oder wenn es keine passenden IP-Adressen gibt, versucht der Empfänger seinen introKey im MAC. Wenn das nicht verifiziert, wird das Paket verworfen. Wenn es verifiziert, wird es entsprechend dem Nachrichtentyp interpretiert, obwohl es trotzdem verworfen werden kann, falls der Empfänger überlastet ist.

Wenn Alice und Bob eine etablierte Sitzung haben, aber Alice aus irgendeinem Grund die Schlüssel verliert und sie Bob kontaktieren möchte, kann sie jederzeit einfach eine neue Sitzung über die SessionRequest und verwandten Nachrichten etablieren. Wenn Bob den Schlüssel verloren hat, aber Alice das nicht weiß, wird sie zunächst versuchen, ihn zum Antworten zu bewegen, indem sie eine DataMessage mit gesetztem wantReply-Flag sendet, und wenn Bob kontinuierlich nicht antwortet, wird sie annehmen, dass der Schlüssel verloren ist und einen neuen etablieren.

Für die DH-Schlüsselvereinbarung wird [RFC3526](http://www.faqs.org/rfcs/rfc3526.html) 2048bit MODP-Gruppe (#14) verwendet:

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Dies sind dieselben p und g, die für I2Ps [ElGamal-Verschlüsselung](/docs/specs/cryptography#elgamal) verwendet werden.

## Replay-Schutz {#replay}

Replay-Prävention auf der SSU-Ebene erfolgt durch das Ablehnen von Paketen mit extrem alten Zeitstempeln oder solchen, die eine IV wiederverwenden. Um doppelte IVs zu erkennen, wird eine Sequenz von Bloom-Filtern eingesetzt, die periodisch "verfallen", sodass nur kürzlich hinzugefügte IVs erkannt werden.

Die messageIds, die in DataMessages verwendet werden, sind in Schichten oberhalb des SSU-Transports definiert und werden transparent weitergegeben. Diese IDs sind nicht in einer bestimmten Reihenfolge - tatsächlich sind sie wahrscheinlich völlig zufällig. Die SSU-Schicht unternimmt keinen Versuch zur Verhinderung von messageId-Wiederholungen - höhere Schichten sollten dies berücksichtigen.

## Adressierung {#addressing}

Um einen SSU-Peer zu kontaktieren, ist einer von zwei Informationssätzen erforderlich: eine direkte Adresse, wenn der Peer öffentlich erreichbar ist, oder eine indirekte Adresse, um eine dritte Partei zur Einführung des Peers zu verwenden. Es gibt keine Beschränkung für die Anzahl der Adressen, die ein Peer haben kann.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Jede der Adressen kann auch eine Reihe von Optionen bereitstellen - spezielle Fähigkeiten dieses bestimmten Peers. Für eine Liste der verfügbaren Fähigkeiten siehe [unten](#capabilities).

Die Adressen, Optionen und Fähigkeiten werden in der [Netzwerkdatenbank](/docs/overview/network-database) veröffentlicht.

## Direkte Session-Einrichtung {#direct}

Direkte Sitzungseinrichtung wird verwendet, wenn keine dritte Partei für NAT-Traversierung erforderlich ist. Die Nachrichtensequenz ist wie folgt:

### Verbindungsaufbau (Direkt) {#establishDirect}

Alice verbindet sich direkt mit Bob. IPv6 wird ab Version 0.9.8 unterstützt.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Nachdem die SessionConfirmed-Nachricht empfangen wurde, sendet Bob eine kleine [DeliveryStatus-Nachricht](/docs/specs/i2np#msg_DeliveryStatus) als Bestätigung. In dieser Nachricht wird die 4-Byte-Nachrichten-ID auf eine Zufallszahl gesetzt und die 8-Byte-"Ankunftszeit" wird auf die aktuelle netzwerkweite ID gesetzt, die 2 ist (d.h. 0x0000000000000002).

Nachdem die Statusnachricht gesendet wurde, tauschen die Peers normalerweise [DatabaseStore-Nachrichten](/docs/specs/i2np#msg_DatabaseStore) aus, die ihre [RouterInfos](/docs/specs/common-structures#struct_RouterInfo) enthalten, dies ist jedoch nicht erforderlich.

Es scheint nicht so, als ob der Typ der Statusnachricht oder deren Inhalt von Bedeutung wäre. Sie wurde ursprünglich hinzugefügt, weil die DatabaseStore-Nachricht um mehrere Sekunden verzögert wurde; da der Store nun sofort gesendet wird, könnte die Statusnachricht möglicherweise entfernt werden.

## Einführung {#introduction}

Introduction-Schlüssel werden über einen externen Kanal (die netDb) übermittelt, wo sie traditionell bis Release 0.9.47 identisch mit dem router Hash waren, aber seit Release 0.9.48 zufällig sein können. Sie müssen bei der Erstellung eines Session-Schlüssels verwendet werden. Für die indirekte Adresse muss der Peer zunächst den Relayhost kontaktieren und ihn um eine Einführung zu dem Peer bitten, der bei diesem Relayhost unter dem angegebenen Tag bekannt ist. Wenn möglich, sendet der Relayhost eine Nachricht an den adressierten Peer und teilt ihm mit, dass er den anfragenden Peer kontaktieren soll, und gibt dem anfragenden Peer auch die IP und den Port, unter dem sich der adressierte Peer befindet. Zusätzlich muss der Peer, der die Verbindung aufbaut, bereits die öffentlichen Schlüssel des Peers kennen, zu dem er sich verbindet (aber nicht notwendigerweise die eines zwischengeschalteten Relay-Peers).

Die indirekte Sitzungsetablierung mittels einer Drittpartei-Einführung ist für eine effiziente NAT-Durchquerung notwendig. Charlie, ein router hinter einem NAT oder einer Firewall, die unaufgeforderte eingehende UDP-Pakete nicht zulässt, kontaktiert zunächst einige Peers und wählt einige aus, die als Introducer fungieren sollen. Jeder dieser Peers (Bob, Bill, Betty, etc.) stellt Charlie einen Introduction Tag zur Verfügung - eine 4-Byte-Zufallszahl - die er dann öffentlich als Methode zur Kontaktaufnahme verfügbar macht. Alice, ein router der Charlies veröffentlichte Kontaktmethoden hat, sendet zunächst ein RelayRequest-Paket an einen oder mehrere der Introducer und bittet jeden, sie Charlie vorzustellen (wobei sie den Introduction Tag anbietet, um Charlie zu identifizieren). Bob leitet dann ein RelayIntro-Paket an Charlie weiter, das Alices öffentliche IP-Adresse und Portnummer enthält, und sendet Alice ein RelayResponse-Paket mit Charlies öffentlicher IP-Adresse und Portnummer zurück. Wenn Charlie das RelayIntro-Paket erhält, sendet er ein kleines zufälliges Paket an Alices IP-Adresse und Port (um ein Loch in sein NAT/Firewall zu stanzen), und wenn Alice Bobs RelayResponse-Paket erhält, beginnt sie eine neue vollständige bidirektionale Sitzungsetablierung mit der angegebenen IP-Adresse und dem Port.

### Verbindungsaufbau (Indirekt über einen Introducer) {#establishIndirect}

Alice verbindet sich zuerst mit dem Introducer Bob, der die Anfrage an Charlie weiterleitet.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Nach dem Hole Punch wird die Sitzung zwischen Alice und Charlie wie bei einer direkten Verbindung aufgebaut.

### IPv6 Hinweise

IPv6 wird ab Version 0.9.8 unterstützt. Veröffentlichte Relay-Adressen können IPv4 oder IPv6 sein, und die Alice-Bob-Kommunikation kann über IPv4 oder IPv6 erfolgen. Bis einschließlich Release 0.9.49 erfolgt die Bob-Charlie- und Alice-Charlie-Kommunikation nur über IPv4. Relaying für IPv6 wird ab Release 0.9.50 unterstützt. Details finden Sie in der Spezifikation.

Obwohl die Spezifikation ab Version 0.9.8 geändert wurde, wurde die Alice-Bob-Kommunikation über IPv6 erst ab Version 0.9.50 tatsächlich unterstützt. Frühere Versionen der Java-router veröffentlichten fälschlicherweise die 'C'-Fähigkeit für IPv6-Adressen, obwohl sie nicht tatsächlich als introducer über IPv6 fungierten. Daher sollten router der 'C'-Fähigkeit bei einer IPv6-Adresse nur vertrauen, wenn die router-Version 0.9.50 oder höher ist.

## Peer Testing {#peerTesting}

Die Automatisierung von kollaborativen Erreichbarkeitstests für Peers wird durch eine Sequenz von PeerTest-Nachrichten ermöglicht. Bei ordnungsgemäßer Ausführung kann ein Peer seine eigene Erreichbarkeit bestimmen und sein Verhalten entsprechend anpassen. Der Testprozess ist recht einfach:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Jede der PeerTest-Nachrichten trägt eine Nonce, die die Testserie selbst identifiziert, wie sie von Alice initialisiert wurde. Wenn Alice eine bestimmte Nachricht nicht erhält, die sie erwartet, wird sie entsprechend erneut senden, und basierend auf den empfangenen Daten oder den fehlenden Nachrichten wird sie ihre Erreichbarkeit kennen. Die verschiedenen Endzustände, die erreicht werden können, sind wie folgt:

- Falls sie keine Antwort von Bob erhält, wird sie bis zu einer bestimmten Anzahl von Malen erneut übertragen, aber wenn nie eine Antwort ankommt, wird sie wissen, dass ihre Firewall oder NAT irgendwie falsch konfiguriert ist und alle eingehenden UDP-Pakete ablehnt, selbst als direkte Antwort auf ein ausgehendes Paket. Alternativ könnte Bob offline sein oder nicht in der Lage, Charlie zur Antwort zu bewegen.

- Wenn Alice keine PeerTest-Nachricht mit der erwarteten Nonce von einer dritten Partei (Charlie) erhält, wird sie ihre ursprüngliche Anfrage an Bob bis zu einer bestimmten Anzahl von Malen erneut senden, selbst wenn sie bereits Bobs Antwort erhalten hat. Wenn Charlies erste Nachricht immer noch nicht durchkommt, aber Bobs schon, weiß sie, dass sie sich hinter einem NAT oder einer Firewall befindet, die unaufgeforderte Verbindungsversuche ablehnt und dass die Portweiterleitung nicht ordnungsgemäß funktioniert (die IP und der Port, die Bob angeboten hat, sollten weitergeleitet werden).

- Wenn Alice Bobs PeerTest-Nachricht und beide PeerTest-Nachrichten von Charlie erhält, aber die enthaltenen IP- und Portnummern in Bobs und Charlies zweiten Nachrichten nicht übereinstimmen, weiß sie, dass sie sich hinter einer symmetrischen NAT befindet, die alle ihre ausgehenden Pakete mit unterschiedlichen 'from'-Ports für jeden kontaktierten Peer umschreibt. Sie muss explizit einen Port weiterleiten und diesen Port immer für externe Verbindungen verfügbar halten, wobei sie weitere Port-Erkennungen ignoriert.

- Wenn Alice Charlies erste Nachricht erhält, aber nicht seine zweite,
  wird sie ihre PeerTest-Nachricht bis zu einer bestimmten Anzahl von
  Malen an Charlie weiterleiten, aber wenn keine Antwort erhalten wird,
  weiß sie, dass Charlie entweder verwirrt ist oder nicht mehr online ist.

Alice sollte Bob willkürlich aus bekannten Peers auswählen, die in der Lage zu sein scheinen, an Peer-Tests teilzunehmen. Bob wiederum sollte Charlie willkürlich aus Peers auswählen, die er kennt und die in der Lage zu sein scheinen, an Peer-Tests teilzunehmen und die sich auf einer anderen IP als sowohl Bob als auch Alice befinden. Wenn die erste Fehlerbedingung auftritt (Alice erhält keine PeerTest-Nachrichten von Bob), kann Alice entscheiden, einen neuen Peer als Bob zu bestimmen und es erneut mit einer anderen Nonce zu versuchen.

Alices Einführungsschlüssel ist in allen PeerTest-Nachrichten enthalten, damit Charlie sie kontaktieren kann, ohne zusätzliche Informationen zu kennen. Ab Version 0.9.15 muss Alice eine etablierte Verbindung mit Bob haben, um Spoofing-Angriffe zu verhindern. Alice darf keine etablierte Verbindung mit Charlie haben, damit der Peer-Test gültig ist. Alice kann später eine Verbindung mit Charlie aufbauen, aber das ist nicht erforderlich.

### IPv6 Hinweise

Bis Release 0.9.26 wird nur das Testen von IPv4-Adressen unterstützt. Nur das Testen von IPv4-Adressen wird unterstützt. Daher muss die gesamte Alice-Bob- und Alice-Charlie-Kommunikation über IPv4 erfolgen. Die Bob-Charlie-Kommunikation kann jedoch über IPv4 oder IPv6 erfolgen. Alices Adresse muss, wenn sie in der PeerTest-Nachricht angegeben wird, 4 Bytes betragen. Ab Release 0.9.27 wird das Testen von IPv6-Adressen unterstützt, und die Alice-Bob- und Alice-Charlie-Kommunikation kann über IPv6 erfolgen, wenn Bob und Charlie Unterstützung mit einer 'B'-Fähigkeit in ihrer veröffentlichten IPv6-Adresse anzeigen. Siehe [Proposal 126](/spec/proposals/126-ipv6-peer-testing) für Details.

Vor Version 0.9.50 sendet Alice die Anfrage an Bob über eine bestehende Sitzung über den Transport (IPv4 oder IPv6), den sie testen möchte. Wenn Bob eine Anfrage von Alice über IPv4 erhält, muss Bob einen Charlie auswählen, der eine IPv4-Adresse bewirbt. Wenn Bob eine Anfrage von Alice über IPv6 erhält, muss Bob einen Charlie auswählen, der eine IPv6-Adresse bewirbt. Die tatsächliche Bob-Charlie-Kommunikation kann über IPv4 oder IPv6 erfolgen (d.h. unabhängig von Alices Adresstyp).

Ab Version 0.9.50 muss Alice, wenn die Nachricht über IPv6 für einen IPv4-Peer-Test oder (ab Version 0.9.50) über IPv4 für einen IPv6-Peer-Test gesendet wird, ihre Einführungsadresse und den Port angeben.

Siehe [Proposal 158](/spec/proposals/158) für Details.

## Übertragungsfenster, ACKs und Wiederholungsübertragungen {#acks}

Die DATA-Nachricht kann ACKs vollständiger Nachrichten und partielle ACKs einzelner Fragmente einer Nachricht enthalten. Siehe den Abschnitt über Datennachrichten auf [der Protokollspezifikationsseite](/docs/legacy/ssu) für Details.

Die Details der Windowing-, ACK- und Retransmission-Strategien sind hier nicht spezifiziert. Siehe den Java-Code für die aktuelle Implementierung. Während der Aufbauphase und für Peer-Tests sollten router exponential backoff für die Retransmission implementieren. Für eine etablierte Verbindung sollten router ein anpassbares Übertragungsfenster, RTT-Schätzung und Timeout implementieren, ähnlich wie TCP oder [streaming](/docs/api/streaming). Siehe den Code für die anfänglichen, minimalen und maximalen Parameter.

## Sicherheit {#security}

UDP-Quelladressen können natürlich gefälscht werden. Zusätzlich können die IPs und Ports, die in spezifischen SSU-Nachrichten enthalten sind (RelayRequest, RelayResponse, RelayIntro, PeerTest), möglicherweise nicht legitim sein. Außerdem müssen bestimmte Aktionen und Antworten eventuell ratenbegrenzt werden.

Die Details der Validierung werden hier nicht spezifiziert. Implementierer sollten angemessene Schutzmaßnahmen hinzufügen.

## Peer-Fähigkeiten {#capabilities}

Eine oder mehrere Fähigkeiten können in der "caps"-Option veröffentlicht werden. Fähigkeiten können in beliebiger Reihenfolge stehen, aber "BC46" ist die empfohlene Reihenfolge für Konsistenz zwischen verschiedenen Implementierungen.

**B** : Wenn die Peer-Adresse die 'B'-Fähigkeit enthält, bedeutet das, dass sie bereit und in der Lage sind, an Peer-Tests als 'Bob' oder 'Charlie' teilzunehmen. Bis Version 0.9.26 wurde Peer-Testing für IPv6-Adressen nicht unterstützt, und die 'B'-Fähigkeit musste, falls bei einer IPv6-Adresse vorhanden, ignoriert werden. Ab Version 0.9.27 wird Peer-Testing für IPv6-Adressen unterstützt, und das Vorhandensein oder Fehlen der 'B'-Fähigkeit bei einer IPv6-Adresse zeigt die tatsächliche Unterstützung (oder fehlende Unterstützung) an.

**C** : Wenn die Peer-Adresse die 'C'-Fähigkeit enthält, bedeutet das, dass sie bereit und in der Lage sind, als introducer über diese Adresse zu fungieren - als introducer Bob für einen andernfalls unerreichbaren Charlie zu dienen. Vor der Version 0.9.50 haben Java-router fälschlicherweise die 'C'-Fähigkeit für IPv6-Adressen veröffentlicht, obwohl IPv6-introducer noch nicht vollständig implementiert waren. Daher sollten router davon ausgehen, dass Versionen vor 0.9.50 nicht als introducer über IPv6 fungieren können, auch wenn die 'C'-Fähigkeit beworben wird.

**4** : Ab Version 0.9.50 zeigt dies ausgehende IPv4-Fähigkeiten an. Wenn eine IP im Host-Feld veröffentlicht wird, ist diese Fähigkeit nicht erforderlich. Wenn dies eine Adresse mit introducers für IPv4-Einführungen ist, sollte '4' enthalten sein. Wenn der router versteckt ist, können '4' und '6' in einer einzigen Adresse kombiniert werden.

**6** : Ab Version 0.9.50 zeigt dies die ausgehende IPv6-Fähigkeit an. Wenn eine IP im Host-Feld veröffentlicht wird, ist diese Fähigkeit nicht erforderlich. Wenn dies eine Adresse mit Introducers für IPv6-Introductions ist, sollte '6' enthalten sein (derzeit nicht unterstützt). Wenn der Router versteckt ist, können '4' und '6' in einer einzigen Adresse kombiniert werden.

# Zukünftige Arbeiten {#future}

Hinweis: Diese Probleme werden bei der Entwicklung von SSU2 behoben.

- Die Analyse der aktuellen SSU-Leistung, einschließlich der Bewertung der Fenstergrößenanpassung und anderer Parameter, sowie die Anpassung der Protokollimplementierung zur Leistungsverbesserung ist ein Thema für zukünftige Arbeiten.

- Die aktuelle Implementierung sendet wiederholt Bestätigungen für dieselben Pakete,
  was den Overhead unnötig erhöht.

- Der standardmäßige kleine MTU-Wert von 620 sollte analysiert und möglicherweise erhöht werden.
  Die aktuelle MTU-Anpassungsstrategie sollte evaluiert werden.
  Passt ein 1730-Byte-Paket der Streaming-Bibliothek in 3 kleine SSU-Pakete? Wahrscheinlich nicht.

- Das Protokoll sollte erweitert werden, um MTUs während der Einrichtung auszutauschen.

- Rekeying ist derzeit nicht implementiert und wird es auch nie sein.

- Die potenzielle Verwendung der 'challenge'-Felder in RelayIntro und RelayResponse sowie die Verwendung des Padding-Feldes in SessionRequest und SessionCreated ist undokumentiert.

- Ein Satz fester Paketgrößen könnte geeignet sein, um die Datenfragmentierung vor externen Angreifern weiter zu verbergen, aber die tunnel-, garlic- und Ende-zu-Ende-Polsterung sollte für die meisten Bedürfnisse bis dahin ausreichend sein.

- Anmeldezeiten in SessionCreated und SessionConfirmed scheinen ungenutzt oder ungeprüft zu sein.

# Spezifikation {#spec}

[Jetzt auf der SSU-Spezifikationsseite](/docs/legacy/ssu).
