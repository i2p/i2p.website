---
title: "Unsichtbares Multihoming"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Öffnen"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Überblick

Dieser Vorschlag umreißt ein Design für ein Protokoll, das es einem I2P-Client, -Service oder externen Balancer-Prozess ermöglicht, mehrere Router transparent zu verwalten, die eine einzelne [Destination](http://localhost:63465/docs/specs/common-structures/#destination) hosten.

Der Vorschlag spezifiziert derzeit keine konkrete Implementierung. Er könnte als Erweiterung zu [I2CP](/docs/specs/i2cp/) oder als neues Protokoll implementiert werden.

## Motivation

Multihoming bezeichnet die Verwendung mehrerer router zur Bereitstellung derselben Destination. Die aktuelle Methode für Multihoming mit I2P besteht darin, dieselbe Destination unabhängig auf jedem router zu betreiben; der router, der von Clients zu einem bestimmten Zeitpunkt verwendet wird, ist derjenige, der zuletzt ein leaseSet veröffentlicht hat.

Das ist ein Hack und wird vermutlich nicht für große Websites im großen Maßstab funktionieren. Angenommen, wir hätten 100 Multihoming-Router mit jeweils 16 Tunnels. Das wären 1600 LeaseSet-Veröffentlichungen alle 10 Minuten oder fast 3 pro Sekunde. Die Floodfills würden überlastet werden und Drosselungen würden einsetzen. Und das ist, bevor wir überhaupt den Lookup-Traffic erwähnen.

Proposal 123 löst dieses Problem mit einem meta-LeaseSet, das die 100 echten LeaseSet-Hashes auflistet. Eine Suche wird zu einem zweistufigen Prozess: zuerst die Suche nach dem meta-LeaseSet und dann nach einem der benannten LeaseSets. Dies ist eine gute Lösung für das Problem des Lookup-Traffics, aber allein betrachtet entsteht dadurch ein erhebliches Datenschutzleck: Es ist möglich zu bestimmen, welche Multihoming-Router online sind, indem man das veröffentlichte meta-LeaseSet überwacht, da jedes echte LeaseSet einem einzelnen Router entspricht.

Wir benötigen eine Möglichkeit für einen I2P-Client oder -Service, eine einzelne Destination über mehrere router zu verteilen, auf eine Art und Weise, die von der Verwendung eines einzelnen routers nicht zu unterscheiden ist (aus der Perspektive des LeaseSet selbst).

## Design

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Stellen Sie sich die folgende gewünschte Konfiguration vor:

- Eine Client-Anwendung mit einem Destination.
- Vier Router, die jeweils drei eingehende Tunnel verwalten.
- Alle zwölf Tunnel sollten in einem einzigen LeaseSet veröffentlicht werden.

### Single-client

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
```
### Definitionen

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
```
### Überblick auf hoher Ebene

- Lade oder generiere ein Destination.

- Öffne eine Sitzung mit jedem Router, die an die Destination gebunden ist.

- Regelmäßig (etwa alle zehn Minuten, aber mehr oder weniger basierend auf der
  Tunnel-Verfügbarkeit):

- Erhalten Sie die schnelle Stufe von jedem Router.

- Nutze die Obermenge von Peers, um Tunnel zu/von jedem Router zu erstellen.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Sammle die Menge der aktiven eingehenden Tunnel von allen aktiven Routern und erstelle ein LeaseSet.

- Veröffentliche das LeaseSet über einen oder mehrere der Router.

### Einzelner Client

Um diese Konfiguration zu erstellen und zu verwalten, benötigt der Client die folgende neue Funktionalität zusätzlich zu dem, was derzeit von [I2CP](/docs/specs/i2cp/) bereitgestellt wird:

- Einem Router mitteilen, Tunnel zu erstellen, ohne ein LeaseSet für sie zu erstellen.
- Eine Liste der aktuellen Tunnel im Inbound-Pool abrufen.

Zusätzlich würde die folgende Funktionalität erhebliche Flexibilität ermöglichen, wie der Client seine Tunnel verwaltet:

- Den Inhalt der Fast-Tier eines routers abrufen.
- Einem router mitteilen, einen eingehenden oder ausgehenden tunnel mit einer gegebenen Liste von
  Peers zu erstellen.

### Multi-Client

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Allgemeiner Client-Prozess

**Session erstellen** - Erstellt eine Session für die angegebene Destination.

**Session Status** - Bestätigung, dass die Session eingerichtet wurde und der Client nun mit dem Aufbau von Tunneln beginnen kann.

**Get Fast Tier** - Fordere eine Liste der Peers an, durch die der Router derzeit Tunnel aufbauen würde.

**Peer List** - Eine Liste von Peers, die dem Router bekannt sind.

**Tunnel Erstellen** - Anfordern, dass der Router einen neuen Tunnel durch die angegebenen Peers aufbaut.

**Tunnel Status** - Das Ergebnis eines bestimmten Tunnel-Aufbaus, sobald es verfügbar ist.

**Get Tunnel Pool** - Anfrage einer Liste der aktuellen Tunnel im eingehenden oder ausgehenden Pool für die Destination.

**Tunnel-Liste** - Eine Liste der Tunnel für den angeforderten Pool.

**LeaseSet veröffentlichen** - Anfrage, dass der Router das bereitgestellte LeaseSet durch einen der ausgehenden Tunnel für das Ziel veröffentlicht. Kein Antwortstatus ist erforderlich; der Router sollte weiterhin Wiederholungsversuche unternehmen, bis er zufrieden ist, dass das LeaseSet veröffentlicht wurde.

**Send Packet** - Ein ausgehendes Paket vom Client. Gibt optional einen outbound tunnel an, durch den das Paket gesendet werden muss (sollte?).

**Send Status** - Informiert den Client über den Erfolg oder Misserfolg beim Senden eines Pakets.

**Paket Empfangen** - Ein eingehendes Paket für den Client. Optional wird der eingehende Tunnel angegeben, über den das Paket empfangen wurde(?)

## Security implications

Aus Sicht der Router ist dieses Design funktional äquivalent zum Status quo. Der Router baut weiterhin alle Tunnel auf, pflegt seine eigenen Peer-Profile und setzt die Trennung zwischen Router- und Client-Operationen durch. In der Standardkonfiguration ist es völlig identisch, da Tunnel für diesen Router aus seiner eigenen Fast Tier aufgebaut werden.

Aus der Perspektive der netDB ist ein einzelnes LeaseSet, das über dieses Protokoll erstellt wurde, identisch zum Status quo, da es bereits vorhandene Funktionalität nutzt. Bei größeren LeaseSets mit bis zu 16 Leases könnte es jedoch für einen Beobachter möglich sein zu bestimmen, dass das LeaseSet multihomed ist:

- Die aktuelle maximale Größe des Fast-Tiers beträgt 75 Peers. Das Inbound Gateway
  (IBGW, der im Lease veröffentlichte Knoten) wird aus einem Bruchteil des Tiers
  ausgewählt (zufällig pro tunnel pool nach Hash partitioniert, nicht nach Anzahl):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Das bedeutet, dass die IBGWs im Durchschnitt aus einer Gruppe von 20-30 Peers stammen werden.

- In einer single-homed Konfiguration würde ein vollständiges 16-tunnel leaseSet 16 IBGWs haben,
  die zufällig aus einer Gruppe von bis zu (sagen wir) 20 Peers ausgewählt werden.

- In einem 4-Router-Multihomed-Setup mit der Standardkonfiguration würde ein vollständiges 16-tunnel LeaseSet 16 IBGWs haben, die zufällig aus einem Set von höchstens 80 Peers ausgewählt werden, wobei es wahrscheinlich einen Anteil gemeinsamer Peers zwischen den Routern gibt.

Daher könnte es mit der Standardkonfiguration durch statistische Analyse möglich sein herauszufinden, dass ein LeaseSet von diesem Protokoll generiert wird. Es könnte auch möglich sein herauszufinden, wie viele Router es gibt, obwohl die Auswirkungen der Fluktuation in den schnellen Stufen die Wirksamkeit dieser Analyse reduzieren würden.

Da der Client die volle Kontrolle darüber hat, welche Peers er auswählt, könnte diese Informationsleckage durch die Auswahl von IBGWs aus einer reduzierten Menge von Peers reduziert oder eliminiert werden.

## Compatibility

Dieses Design ist vollständig rückwärtskompatibel mit dem Netzwerk, da es keine Änderungen am LeaseSet-Format gibt. Alle Router müssten über das neue Protokoll Bescheid wissen, aber das ist kein Problem, da sie alle von derselben Entität kontrolliert würden.

## Performance and scalability notes

Die obere Grenze von 16 Leases pro LeaseSet wird durch diesen Vorschlag nicht verändert. Für Destinations, die mehr Tunnel als diese benötigen, gibt es zwei mögliche Netzwerkmodifikationen:

- Erhöhung der oberen Grenze für die Größe von LeaseSets. Dies wäre am einfachsten
  zu implementieren (obwohl es immer noch eine umfassende Netzwerkunterstützung erfordern würde, bevor
  es weit verbreitet eingesetzt werden könnte), könnte aber aufgrund der größeren
  Paketgrößen zu langsameren Lookups führen. Die maximal mögliche LeaseSet-Größe wird durch die MTU der
  zugrunde liegenden Transports definiert und liegt daher bei etwa 16kB.

- Implementiere Proposal 123 für abgestufte LeaseSets. In Kombination mit diesem Vorschlag könnten die Destinations für die Sub-LeaseSets über mehrere Router verteilt werden, wodurch sie effektiv wie mehrere IP-Adressen für einen Clearnet-Dienst fungieren.

## Acknowledgements

Dank an psi für die Diskussion, die zu diesem Vorschlag geführt hat.
