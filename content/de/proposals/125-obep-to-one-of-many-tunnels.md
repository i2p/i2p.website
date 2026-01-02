---
title: "OBEP-Lieferung an 1-von-N oder N-von-N-Tunnel"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Offen"
thread: "http://zzz.i2p/topics/2099"
toc: true
---

## Überblick

Dieser Vorschlag umfasst zwei Verbesserungen zur Steigerung der Netzwerkleistung:

- Delegieren der IBGW-Auswahl an das OBEP, indem ihm eine Liste von Alternativen anstelle einer einzigen Option bereitgestellt wird.

- Ermöglichen des Multicast-Paket-Routings am OBEP.


## Motivation

Im Fall der direkten Verbindung ist die Idee, die Verbindungskongestion zu verringern, indem dem OBEP Flexibilität gewährt wird, wie es sich mit IBGWs verbindet. Die Fähigkeit, mehrere Tunnel anzugeben, ermöglicht es uns auch, Multicast am OBEP zu implementieren (indem die Nachricht an alle angegebenen Tunnel geliefert wird).

Eine Alternative zum Delegationsteil dieses Vorschlags wäre es, durch einen [LeaseSet](http://localhost:63465/docs/specs/common-structures/#leaseset)-Hash zu senden, ähnlich zur bestehenden Möglichkeit, einen Ziel-[RouterIdentity]-Hash anzugeben. Dies würde zu einer kleineren Nachricht und einem potenziell neueren LeaseSet führen. Jedoch:

1. Es würde das OBEP zu einer Suche zwingen

2. Das LeaseSet könnte nicht zu einer Floodfill veröffentlicht worden sein, sodass die Suche fehlschlagen würde.

3. Das LeaseSet könnte verschlüsselt sein, sodass das OBEP die Leases nicht erhalten könnte.

4. Das Angeben eines LeaseSets offenbart dem OBEP das [Destination](/docs/specs/common-structures/#destination) der Nachricht, das sie sonst nur durch Scraping aller LeaseSets im Netzwerk entdecken könnten, um einen Lease-Abgleich zu finden.


## Design

Der Urheber (OBGW) würde einige (alle?) der Ziel [Leases](http://localhost:63465/docs/specs/common-structures/#lease) in die Lieferanweisungen [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) einfügen, anstatt nur einen auszuwählen.

Das OBEP würde einen dieser Tunnel zur Lieferung auswählen. Das OBEP würde, wenn verfügbar, einen auswählen, zu dem es bereits verbunden ist oder den es bereits kennt. Dies würde den OBEP-IBGW-Pfad schneller und zuverlässiger machen und die Gesamtzahl der Netzwerkverbindungen reduzieren.

Wir haben einen unbenutzten Liefertyp (0x03) und zwei verbleibende Bits (0 und 1) in den Flags für [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions), die wir nutzen können, um diese Funktionen zu implementieren.


## Sicherheitsimplikationen

Dieser Vorschlag ändert nicht die Menge der Informationen, die über das Zielziel (Destination) des OBGW oder deren Sicht auf das NetDB geleakt werden:

- Ein Angreifer, der das OBEP kontrolliert und LeaseSets aus dem NetDB scrapt, kann bereits bestimmen, ob eine Nachricht an ein bestimmtes Ziel gesendet wird, indem er nach dem [TunnelId](http://localhost:63465/docs/specs/common-structures/#tunnelid)- / [RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification)-Paar sucht. Im schlimmsten Fall könnte die Anwesenheit mehrerer Leases im TMDI es schneller machen, einen Abgleich in der Datenbank des Gegners zu finden.

- Ein Angreifer, der ein bösartiges Ziel (Destination) betreibt, kann bereits Informationen über die Sicht eines verbundenden Opfers auf das NetDB gewinnen, indem er LeaseSets mit unterschiedlichen eingehenden Tunneln zu verschiedenen Floodfills veröffentlicht und beobachtet, durch welche Tunnel das OBGW sich verbindet. Aus ihrer Sicht ist die Auswahl des Tunnels durch das OBEP funktionell identisch mit der Auswahl durch das OBGW.

Das Multicast-Flag leakt die Tatsache, dass das OBGW an die OBEPs multicastet. Dies erzeugt einen Leistungs-vs.-Privatheits-Kompromiss, der bei der Implementierung höherer Protokolle berücksichtigt werden sollte. Da es ein optionales Flag ist, können Benutzer die geeignete Entscheidung für ihre Anwendung treffen. Es könnte jedoch Vorteile haben, wenn dies das Standardverhalten für kompatible Anwendungen ist, da ein breiter Einsatz durch eine Vielzahl von Anwendungen die Informationsleckage darüber, aus welcher spezifischen Anwendung eine Nachricht stammt, reduzieren würde.


## Spezifikation

Die First Fragment Delivery Instructions [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) würden wie folgt modifiziert:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 Byte
       Bit-Reihenfolge: 76543210
       Bits 6-5: Liefertyp
                 0x03 = TUNNELS
       Bit 0: Multicast? Wenn 0, an einen der Tunnel liefern
                          Wenn 1, an alle Tunnel liefern
                          Auf 0 setzen für die Kompatibilität mit zukünftigen Verwendungen, wenn
                          der Liefertyp nicht TUNNELS ist

Count ::
       1 Byte
       Optional, vorhanden, wenn der Liefertyp TUNNELS ist
       2-255 - Anzahl der folgenden id/hash-Paare

Tunnel ID :: `TunnelId`
To Hash ::
       36 Bytes pro Stück
       Optional, vorhanden, wenn der Liefertyp TUNNELS ist
       id/hash-Paare

Gesamtlänge: Typische Länge ist:
       75 Bytes für Count 2 TUNNELS-Lieferung (unfragmentierte Tunnel-Nachricht);
       79 Bytes für Count 2 TUNNELS-Lieferung (erster Fragment)

Rest der Lieferanweisungen unverändert
```


## Kompatibilität

Die einzigen Peers, die die neue Spezifikation verstehen müssen, sind die OBGWs und die OBEPs. Wir können diese Änderung deshalb mit dem bestehenden Netzwerk kompatibel machen, indem wir ihre Verwendung an die Ziel-I2P-Version [VERSIONS](/docs/specs/i2np/#protocol-versions) knüpfen:

* Die OBGWs müssen beim Aufbau ausgehender Tunnel kompatible OBEPs basierend auf der in ihrem [RouterInfo](http://localhost:63465/docs/specs/common-structures/#routerinfo) beworbenen I2P-Version auswählen.

* Peers, die die Zielversion bewerben, müssen das Parsen der neuen Flags unterstützen und dürfen die Anweisungen nicht als ungültig ablehnen.

