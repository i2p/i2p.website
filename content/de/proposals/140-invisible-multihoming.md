---
title: "Unsichtbares Multihoming"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Offen"
thread: "http://zzz.i2p/topics/2335"
---

## Übersicht

Dieser Vorschlag umreißt ein Design für ein Protokoll, das es einem I2P-Client, Dienst oder externen Lastenausgleichsprozess ermöglicht, mehrere Router zu verwalten, die transparent ein einzelnes [Destination](http://localhost:63465/en/docs/specs/common-structures/#destination) hosten.

Der Vorschlag spezifiziert derzeit keine konkrete Implementierung. Es könnte als Erweiterung zu [I2CP](/en/docs/specs/i2cp/) oder als neues Protokoll implementiert werden.


## Motivation

Multihoming bedeutet, dass mehrere Router verwendet werden, um dasselbe Destination zu hosten. Die derzeitige Art, wie man mit I2P Multihoming betreibt, ist das Ausführen des gleichen Destinations auf jedem Router unabhängig; der Router, der zu jedem bestimmten Zeitpunkt von Clients verwendet wird, ist der letzte, der ein [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset) veröffentlicht.

Dies ist ein Hack und funktioniert vermutlich nicht für große Websites im Maßstab. Sagen wir, wir hätten 100 Multihoming-Router, jeder mit 16 Tunneln. Das sind 1600 LeaseSet-Veröffentlichungen alle 10 Minuten oder fast 3 pro Sekunde. Die Floodfills würden überfordert und Drosselungen würden aktiviert. Und das bevor wir überhaupt den Suchverkehr erwähnen.

[Proposal 123](/en/proposals/123-new-netdb-entries/) löst dieses Problem mit einem Meta-LeaseSet, das die 100 echten LeaseSet-Hashes auflistet. Eine Suche wird zu einem zweistufigen Prozess: zuerst das Meta-LeaseSet suchen und dann eines der benannten LeaseSets. Dies ist eine gute Lösung für das Problem des Suchverkehrs, aber alleine schafft es ein erhebliches Datenschutzleck: Es ist möglich, zu bestimmen, welche Multihoming-Router online sind, indem man das veröffentlichte Meta-LeaseSet überwacht, da jedes reale LeaseSet einem einzelnen Router entspricht.

Wir benötigen eine Möglichkeit für einen I2P-Client oder -Dienst, ein einzelnes Destination auf mehrere Router zu verteilen, auf eine Art, die ununterscheidbar von der Verwendung eines einzelnen Routers ist (aus der Perspektive des LeaseSet selbst).


## Design

### Definitionen

    Benutzer
        Die Person oder Organisation, die ihre Destination(s) multihomen möchte. Ein einzelnes Destination wird hier ohne allgemeine Einschränkung (WLOG) betrachtet.

    Client
        Die Anwendung oder der Dienst, der hinter dem Destination läuft. Es kann sich um eine Client-seitige, Server-seitige oder Peer-to-Peer-Anwendung handeln; wir bezeichnen es als Client im Sinne, dass es sich mit den I2P-Routern verbindet.

        Der Client besteht aus drei Teilen, die alle im gleichen Prozess sein können oder auf Prozesse oder Maschinen verteilt sein können (bei einer Mehrfach-Client-Konfiguration):

        Lastenausgleich
            Der Teil des Clients, der die Auswahl der Peers und den Tunnelaufbau verwaltet. Zu einem Zeitpunkt gibt es einen einzigen Lastenausgleich, der mit allen I2P-Routern kommuniziert. Es kann Ausfallersatz-Lastenausgleiche geben.

        Frontend
            Der Teil des Clients, der parallel betrieben werden kann. Jedes Frontend kommuniziert mit einem einzelnen I2P-Router.

        Backend
            Der Teil des Clients, der zwischen allen Frontends geteilt wird. Es gibt keine direkte Kommunikation mit einem I2P-Router.

    Router
        Ein I2P-Router, der vom Benutzer betrieben wird und an der Grenze zwischen dem I2P-Netzwerk und dem Netzwerk des Benutzers sitzt (ähnlich einem Edge-Gerät in Unternehmensnetzwerken). Er baut Tunnel unter dem Kommando eines Lastenausgleichs auf und leitet Pakete für einen Client oder ein Frontend.

### Überblick auf hoher Ebene

Stellen Sie sich die folgende gewünschte Konfiguration vor:

- Eine Client-Anwendung mit einem Destination.
- Vier Router, die jeweils drei eingehende Tunnel verwalten.
- Alle zwölf Tunnel sollten in einem einzigen LeaseSet veröffentlicht werden.

Einzel-Client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/

Multi-Client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/

### Allgemeiner Client-Prozess
- Laden oder generieren Sie ein Destination.

- Eröffnen Sie eine Sitzung mit jedem Router, gebunden an das Destination.

- Regelmäßig (etwa alle zehn Minuten, aber mehr oder weniger basierend auf der Lebensdauer der Tunnel):

  - Erhalten Sie die schnelle Ebene von jedem Router.

  - Verwenden Sie die Gesamtheit der Peers, um Tunnel zu/von jedem Router zu bauen.

    - Standardmäßig verwenden Tunnel zu/von einem bestimmten Router Peers aus der schnellen Ebene dieses Routers, aber dies wird nicht vom Protokoll erzwungen.

  - Sammeln Sie die Menge der aktiven eingehenden Tunnel von allen aktiven Routern und erstellen Sie ein LeaseSet.

  - Veröffentlichen Sie das LeaseSet über einen oder mehrere der Router.

### Unterschiede zu I2CP
Um diese Konfiguration zu erstellen und zu verwalten, benötigt der Client die folgende neue Funktionalität über das hinaus, was derzeit von [I2CP](/en/docs/specs/i2cp/) bereitgestellt wird:

- Weisen Sie einen Router an, Tunnel zu bauen, ohne ein LeaseSet dafür zu erstellen.
- Holen Sie sich eine Liste der aktuellen Tunnel im eingehenden Pool.

Zusätzlich würde die folgende Funktionalität erhebliche Flexibilität ermöglichen, wie der Client seine Tunnel verwaltet:

- Erhalten Sie den Inhalt der schnellen Ebene eines Routers.
- Weisen Sie einen Router an, einen eingehenden oder ausgehenden Tunnel unter Verwendung einer gegebenen Liste von Peers zu bauen.

### Protokollumriss

```
         Client                           Router

                    --------------------->  Erstellen Session
   Sitzungsstatus  <---------------------
                    --------------------->  Erhalten Fast Tier
          Peer List  <---------------------
                    --------------------->  Erstellen Tunnel
      Tunnelstatus  <---------------------
                    --------------------->  Erhalten Tunnel Pool
       Tunnel Liste  <---------------------
                    --------------------->  Veröffentlichen LeaseSet
                    --------------------->  Senden Paket
    Sende Status  <---------------------
 Paketempfang  <---------------------

### Nachrichten
    Erstellen Session
        Erstellen einer Sitzung für das gegebene Destination.

    Sitzungsstatus
        Bestätigung, dass die Sitzung eingerichtet wurde und der Client nun anfangen kann Tunnel zu bauen.

    Erhalten Fast Tier
        Fordern Sie eine Liste der Peers an, durch die der Router derzeit Tunnel bauen würde.

    Peer Liste
        Eine Liste von Peers, die dem Router bekannt sind.

    Erstellen Tunnel
        Fordern Sie an, dass der Router einen neuen Tunnel durch die angegebenen Peers baut.

    Tunnelstatus
        Das Ergebnis eines bestimmten Tunnelaufbaus, sobald es verfügbar ist.

    Erhalten Tunnel Pool
        Fordern Sie eine Liste der aktuellen Tunnel im eingehenden oder ausgehenden Pool für das Destination an.

    Tunnel Liste
        Eine Liste von Tunneln für den angeforderten Pool.

    Veröffentlichen LeaseSet
        Fordern Sie an, dass der Router das bereitgestellte LeaseSet über einen der ausgehenden Tunnel für das Destination veröffentlicht. Es ist kein Rückmeldestatus erforderlich; der Router sollte weiterhin versuchen, bis er zufrieden ist, dass das LeaseSet veröffentlicht wurde.

    Senden Paket
        Ein ausgehendes Paket vom Client. Optional wird ein ausgehender Tunnel angegeben, durch den das Paket gesendet werden muss (sollte?).

    Sende Status
        Informiert den Client über den Erfolg oder das Scheitern des Sendens eines Pakets.

    Paketempfang
        Ein eingehendes Paket für den Client. Optional wird der eingehende Tunnel angegeben, durch den das Paket empfangen wurde(?)


## Sicherheitsimplikationen

Aus der Perspektive der Router ist dieses Design funktional identisch mit dem Status quo. Der Router baut weiterhin alle Tunnel, pflegt seine eigenen Peer-Profile und erzwingt die Trennung zwischen Router- und Client-Operationen. In der Standardkonfiguration ist es komplett identisch, da Tunnel für diesen Router aus seiner eigenen schnellen Ebene gebaut werden.

Aus der Perspektive von netDB ist ein einzelnes LeaseSet, das über dieses Protokoll erstellt wurde, identisch mit dem Status quo, da es bereits bestehende Funktionalität nutzt. Allerdings, für größere LeaseSets, die sich 16 Leases nähern, könnte es für einen Beobachter möglich sein, zu erkennen, dass das LeaseSet multihomed ist:

- Die derzeit maximale Größe der schnellen Ebene beträgt 75 Peers. Das Inbound Gateway (IBGW, der Knoten, der in einem Lease veröffentlicht wird) wird aus einem Bruchteil der Ebene ausgewählt (zufällig partitioniert pro Tunnel-Pool durch Hash, nicht Zählung):

      1 Hop
          Die gesamte schnelle Ebene

      2 Hops
          Die Hälfte der schnellen Ebene
          (der Standard bis Mitte 2014)

      3+ Hops
          Ein Viertel der schnellen Ebene
          (3 ist der aktuelle Standard)

  Das bedeutet im Durchschnitt werden die IBGWs aus einem Satz von 20-30 Peers stammen.

- In einer single-homed Konfiguration hätte ein volles 16-Tunnel-LeaseSet 16 IBGWs, die zufällig aus einem Satz von bis zu (gesagt) 20 Peers ausgewählt werden.

- In einer 4-Router-multihomed Konfiguration unter Verwendung der Standardkonfiguration hätte ein volles 16-Tunnel-LeaseSet 16 IBGWs, die zufällig aus einem Satz von maximal 80 Peers ausgewählt werden, obwohl es wahrscheinlich einen Bruchteil gemeinsamer Peers zwischen Routern gibt.

Daher könnte es mit der Standardkonfiguration mittels statistischer Analyse möglich sein zu erkennen, dass ein LeaseSet durch dieses Protokoll generiert wird. Es könnte auch möglich sein herauszufinden, wie viele Router es gibt, obwohl die Auswirkungen von Churn auf die schnellen Ebenen die Effektivität dieser Analyse reduzieren würden.

Da der Client die volle Kontrolle darüber hat, welche Peers er auswählt, könnte diese Informationsleckage reduziert oder eliminiert werden, indem IBGWs aus einem reduzierten Satz von Peers ausgewählt werden.


## Kompatibilität

Dieses Design ist vollständig rückwärtskompatibel mit dem Netzwerk, da es keine Änderungen am [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset)-Format gibt. Alle Router müssten sich des neuen Protokolls bewusst sein, aber dies ist kein Problem, da sie alle von derselben Entität kontrolliert werden.


## Leistungs- und Skalierungsnotizen

Das obere Limit von 16 [Lease](http://localhost:63465/en/docs/specs/common-structures/#lease) pro LeaseSet bleibt von diesem Vorschlag unverändert. Für Destinations, die mehr Tunnel benötigen als dies, gibt es zwei mögliche Netzwerkmodifikationen:

- Erhöhung des oberen Limits der Größe von LeaseSets. Dies wäre das Einfachste umzusetzen (obwohl es noch umfassende Netzwerkunterstützung erfordern würde, bevor es breit eingesetzt werden könnte), könnte aber zu langsameren Suchvorgängen aufgrund der größeren Paketgrößen führen. Die maximal machbare LeaseSet-Größe wird durch die MTU der zugrunde liegenden Transports definiert und beträgt daher etwa 16kB.

- Implementierung von [Proposal 123](/en/proposals/123-new-netdb-entries/) für gestaffelte LeaseSets. In Kombination mit diesem Vorschlag könnten die Destinations für die Sub-LeaseSets über mehrere Router verteilt werden, was effektiv wie mehrere IP-Adressen für einen Clearnet-Dienst wirkt.


## Danksagungen

Danke an psi für die Diskussion, die zu diesem Vorschlag führte.
