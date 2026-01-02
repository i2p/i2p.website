---
title: "IPv6 Transportverbesserungen"
number: "158"
author: "zzz, orignal"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Closed"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
toc: true
---

## Hinweis
Netzwerkausbau und Testen im Gange.
Kleine Überarbeitungen vorbehalten.


## Übersicht

Dieser Vorschlag zielt darauf ab, Verbesserungen an den SSU- und NTCP2-Transports für IPv6 zu implementieren.


## Motivation

Da IPv6 weltweit wächst und IPv6-only-Konfigurationen (insbesondere mobil) häufiger werden,
müssen wir unsere Unterstützung für IPv6 verbessern und die Annahmen beseitigen, dass
alle Router IPv4-fähig sind.


### Konnektivitätsprüfung

Beim Auswählen von Peers für Tunnels oder beim Auswählen von OBEP/IBGW-Pfaden für das Routing von Nachrichten,
hilft es zu berechnen, ob Router A eine Verbindung zu Router B herstellen kann.
Im Allgemeinen bedeutet dies, dass festgestellt wird, ob A die Fähigkeit hat, ausgehend einen Transport und Adresstyp (IPv4/v6) zu nutzen,
der mit einer der von B beworbenen eingehenden Adressen übereinstimmt.

In vielen Fällen kennen wir jedoch A's Fähigkeiten nicht und müssen Annahmen treffen.
Wenn A versteckt oder hinter einer Firewall ist, werden die Adressen nicht veröffentlicht, und wir haben kein direktes Wissen -
also nehmen wir an, dass es IPv4-fähig ist und nicht IPv6-fähig.
Die Lösung besteht darin, zwei neue "Caps" oder Fähigkeiten zu den Router-Infos hinzuzufügen, um die ausgehende Fähigkeit für IPv4 und IPv6 anzuzeigen.


### IPv6-Vermittler

Unsere Spezifikationen [SSU](/docs/specs/ssu2/) und [SSU-SPEC](/docs/legacy/ssu/) enthalten Fehler und Inkonsistenzen darüber, ob
IPv6-Vermittler für IPv4-Vermittlungen unterstützt werden.
In jedem Fall wurde dies weder in Java I2P noch in i2pd jemals implementiert.
Dies muss korrigiert werden.


### IPv6-Vermittlungen

Unsere Spezifikationen [SSU](/docs/specs/ssu2/) und [SSU-SPEC](/docs/legacy/ssu/) machen deutlich, dass
IPv6-Vermittlungen nicht unterstützt werden.
Dies geschah unter der Annahme, dass IPv6 niemals hinter einer Firewall steht.
Dies ist eindeutig nicht wahr, und wir müssen die Unterstützung für Router hinter einer Firewall mit IPv6 verbessern.


### Vermittlungsdiagramme

Legende: ----- ist IPv4, ====== ist IPv6

Aktuell nur IPv4:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


IPv4-Vermittlung, IPv6-Vermittler

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

IPv6-Vermittlung, IPv6-Vermittler


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

IPv6-Vermittlung, IPv4-Vermittler

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Design

Es gibt drei Änderungen, die implementiert werden sollen.

- Hinzufügen von "4" und "6" Fähigkeiten zu den Router-Adressfähigkeiten, um ausgehende IPv4- und IPv6-Unterstützung anzuzeigen
- Hinzufügen der Unterstützung für IPv4-Vermittlungen über IPv6-Vermittler
- Hinzufügen der Unterstützung für IPv6-Vermittlungen über IPv4- und IPv6-Vermittler


## Spezifikation

### 4/6 Caps

Dies wurde ursprünglich ohne formellen Vorschlag implementiert, ist aber erforderlich für
IPv6-Vermittlungen, daher fügen wir es hier hinzu.
Siehe auch [CAPS](http://zzz.i2p/topics/3050).


Zwei neue Fähigkeiten "4" und "6" sind definiert.
Diese neuen Fähigkeiten werden dem "caps"-Feld in der Router-Adresse hinzugefügt, nicht den Router-Info-Caps.
Derzeit haben wir kein "caps"-Eigenschaft für NTCP2 definiert.
Eine SSU-Adresse mit Vermittlern ist definitionsgemäß gerade ipv4. Wir unterstützen überhaupt keine ipv6-Vermittlung.
Diese Vorschläge sind jedoch mit IPv6-Vermittlungen kompatibel. Siehe unten.

Darüber hinaus kann ein Router die Konnektivität über ein Overlay-Netzwerk wie I2P-over-Yggdrasil unterstützen,
möchte jedoch keine Adresse veröffentlichen oder diese Adresse hat kein Standard-IPv4- oder IPv6-Format.
Dieses neue Fähigkeitssystem sollte flexibel genug sein, um diese Netzwerke ebenfalls zu unterstützen.

Wir definieren die folgenden Änderungen:

NTCP2: Hinzufügen von "caps"-Feld

SSU: Unterstützung einer Router-Adresse ohne Host oder Vermittler, um ausgehende Unterstützung für
IPv4, IPv6 oder beides anzuzeigen.

Beide Transports: Definieren der folgenden Caps-Werte:

- "4": IPv4-Unterstützung
- "6": IPv6-Unterstützung

Mehrere Werte können in einer einzigen Adresse unterstützt werden. Siehe unten.
Mindestens einer dieser Caps ist obligatorisch, wenn kein "host"-Wert in der Router-Adresse enthalten ist.
Maximal einer dieser Caps ist optional, wenn ein "host"-Wert in der Router-Adresse enthalten ist.
Zusätzliche Transport-Caps können in Zukunft definiert werden, um Unterstützung für Overlay-Netzwerke oder andere Verbindungen anzuzeigen.


#### Anwendungsfälle und Beispiele

SSU:

SSU mit Host: 4/6 optional, niemals mehr als eins.
Beispiel: SSU caps="4" host="1.2.3.4" key=... port="1234"

SSU nur ausgehend für eines, das andere ist veröffentlicht: Nur Caps, 4/6.
Beispiel: SSU caps="6"

SSU mit Vermittlern: niemals kombiniert. 4 oder 6 ist erforderlich.
Beispiel: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

SSU versteckt: Nur Caps, 4, 6 oder 46. Mehrere sind erlaubt.
Keine Notwendigkeit für zwei Adressen, eine mit 4 und eine mit 6.
Beispiel: SSU caps="46"

NTCP2:

NTCP2 mit Host: 4/6 optional, niemals mehr als eins.
Beispiel: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

NTCP2 nur ausgehend für eines, das andere ist veröffentlicht: Caps, s, v nur, 4/6/y, mehrere sind erlaubt.
Beispiel: NTCP2 caps="6" i=... s=... v="2"

NTCP2 versteckt: Caps, s, v nur 4/6, mehrere sind erlaubt. Keine Notwendigkeit für zwei Adressen, eine mit 4 und eine mit 6.
Beispiel: NTCP2 caps="46" i=... s=... v="2"


### IPv6-Vermittler für IPv4

Die folgenden Änderungen sind erforderlich, um Fehler und Inkonsistenzen in den Spezifikationen zu korrigieren.
Wir haben dies auch als "Teil 1" des Vorschlags beschrieben.

#### Spezifikationsänderungen

[SSU](/docs/specs/ssu2/) sagt derzeit (IPv6-Anmerkungen):

IPv6 wird ab Version 0.9.8 unterstützt. Veröffentlichte Relay-Adressen können IPv4 oder IPv6 sein, und die Kommunikation zwischen Alice und Bob kann über IPv4 oder IPv6 erfolgen.

Fügen Sie folgendes hinzu:

Während die Spezifikation ab Version 0.9.8 geändert wurde, wurde die Kommunikation zwischen Alice und Bob über IPv6 tatsächlich erst ab Version 0.9.50 unterstützt.
Frühere Versionen von Java-Routern veröffentlichen fälschlicherweise die "C"-Fähigkeit für IPv6-Adressen,
obwohl sie tatsächlich nicht als Vermittler über IPv6 fungierten.
Daher sollten Router der "C"-Fähigkeit auf einer IPv6-Adresse nur vertrauen, wenn die Router-Version 0.9.50 oder höher ist.


[SSU-SPEC](/docs/legacy/ssu/) sagt derzeit (Relay-Anfrage):

Die IP-Adresse ist nur enthalten, wenn sie sich von der Quelladresse und dem Port des Pakets unterscheidet.
In der aktuellen Implementierung ist die IP-Länge immer 0 und der Port ist immer 0,
und der Empfänger sollte die Quelladresse und den Port des Pakets verwenden.
Diese Nachricht kann über IPv4 oder IPv6 gesendet werden. Wenn IPv6, muss Alice ihre IPv4-Adresse und ihren Port angeben.

Fügen Sie folgendes hinzu:

Die IP und der Port müssen angegeben werden, um eine IPv4-Adresse über IPv6 zu vermitteln, wenn diese Nachricht gesendet wird.
Dies wird ab Version 0.9.50 unterstützt.


### IPv6-Vermittlungen

Alle drei SSU-Relay-Nachrichten (RelayRequest, RelayResponse und RelayIntro) enthalten IP-Längenfelder,
um die Länge der (Alice, Bob oder Charlie) folgenden IP-Adresse anzuzeigen.

Daher ist keine Änderung des Nachrichtenformats erforderlich.
Nur Textänderungen in den Spezifikationen, die angeben, dass 16-Byte-IP-Adressen erlaubt sind.

Die folgenden Änderungen sind an den Spezifikationen erforderlich.
Wir haben dies auch als "Teil 2" des Vorschlags beschrieben.


#### Spezifikationsänderungen

[SSU](/docs/specs/ssu2/) sagt derzeit (IPv6-Anmerkungen):

Die Kommunikation zwischen Bob-Charlie und Alice-Charlie erfolgt nur über IPv4.

[SSU-SPEC](/docs/legacy/ssu/) sagt derzeit (Relay-Anfrage):

Es gibt keine Pläne, Relaying für IPv6 zu implementieren.

Ändern zu:

Relaying für IPv6 wird ab Veröffentlichung 0.9.xx unterstützt

[SSU-SPEC](/docs/legacy/ssu/) sagt derzeit (Relay Response):

Charlies IP-Adresse muss IPv4 sein, da das die Adresse ist, an die Alice die Session-Anfrage nach dem Hole-Punch senden wird.
Es gibt keine Pläne, Relaying für IPv6 zu implementieren.

Ändern zu:

Charlies IP-Adresse kann IPv4 oder, ab Veröffentlichung 0.9.xx, IPv6 sein.
Das ist die Adresse, an die Alice die Session-Anfrage nach dem Hole-Punch senden wird.
Relaying für IPv6 wird ab Veröffentlichung 0.9.xx unterstützt

[SSU-SPEC](/docs/legacy/ssu/) sagt derzeit (Relay Intro):

Alices IP-Adresse ist in der aktuellen Implementierung immer 4 Byte, da Alice versucht, Charlie über IPv4 zu verbinden.
Diese Nachricht muss über eine etablierte IPv4-Verbindung gesendet werden,
da dies die einzige Möglichkeit für Bob ist, Charlies IPv4-Adresse zu kennen, um sie in der Relay Response an Alice zurückzugeben.

Ändern zu:

Für IPv4 ist Alices IP-Adresse immer 4 Byte, da Alice versucht, Charlie über IPv4 zu verbinden.
Ab Veröffentlichung 0.9.xx wird IPv6 unterstützt, und Alices IP-Adresse kann 16 Byte sein.

Für IPv4 muss diese Nachricht über eine etablierte IPv4-Verbindung gesendet werden,
da dies die einzige Möglichkeit für Bob ist, Charlies IPv4-Adresse zu kennen, um sie in der Relay Response an Alice zurückzugeben.
Ab Veröffentlichung 0.9.xx wird IPv6 unterstützt, und diese Nachricht kann über eine etablierte IPv6-Verbindung gesendet werden.

Zusätzlich hinzufügen:

Ab Veröffentlichung 0.9.xx muss jede über Vermittler veröffentlichte SSU-Adresse "4" oder "6" im "caps"-Feld enthalten.


## Migration

Alle alten Router sollten die Eigenschaft "caps" in NTCP2 und unbekannte Fähigkeitszeichen in der SSU-Caps-Eigenschaft ignorieren.

Jede SSU-Adresse mit Vermittlern, die keinen "4"- oder "6"-Cap enthält, wird als für die IPv4-Vermittlung angenommen.
