---
title: "Über I2P"
description: "Erfahren Sie mehr über The Invisible Internet Project - ein vollständig verschlüsseltes, Peer-to-Peer-Overlay-Netzwerk für anonyme Kommunikation."
tagline: "Das Unsichtbare Internetprojekt"
type: "über"
layout: "über"
established: "2002"
---

Das Invisible Internet Project begann im Jahr 2002. Die Vision des Projekts war, dass das I2P-Netzwerk "volle Anonymität, Privatsphäre und Sicherheit auf höchstem Niveau bietet. Ein dezentralisiertes und Peer-to-Peer-Internet bedeutet, dass Sie sich keine Sorgen mehr darüber machen müssen, dass Ihr ISP Ihren Datenverkehr kontrolliert. Dies wird es den Menschen ermöglichen, nahtlose Aktivitäten durchzuführen und die Art und Weise zu verändern, wie wir Sicherheit und sogar das Internet betrachten, indem sie öffentliche Schlüsselverschlüsselung, IP-Steganographie und Nachrichtenauthentifizierung nutzen. Das Internet, das hätte sein sollen, wird bald da sein."

Seitdem hat sich I2P weiterentwickelt, um eine vollständige Suite von Netzwerkprotokollen zu spezifizieren und zu implementieren, die in der Lage sind, ein hohes Maß an Privatsphäre, Sicherheit und Authentifizierung für eine Vielzahl von Anwendungen bereitzustellen.

## Das I2P-Netzwerk

Das I2P-Netzwerk ist ein vollständig verschlüsseltes Peer-to-Peer-Overlay-Netzwerk. Ein Beobachter kann weder den Inhalt, die Quelle noch das Ziel einer Nachricht sehen. Niemand kann sehen, woher der Datenverkehr kommt, wohin er geht oder was der Inhalt ist. Zudem bieten I2P-Transporte Widerstand gegen Erkennung und Blockierung durch Zensoren. Da das Netzwerk auf Peers angewiesen ist, um den Datenverkehr zu leiten, ist die standortbezogene Blockierung eine Herausforderung, die mit dem Netzwerk wächst. Jeder Router im Netzwerk trägt dazu bei, das Netzwerk anonym zu machen. Außer in Fällen, in denen es unsicher wäre, beteiligt sich jeder am Senden und Empfangen von Netzwerkverkehr.

## Wie man sich mit dem I2P-Netzwerk verbindet

Die Kernsoftware (Java) enthält einen Router, der eine Verbindung mit dem Netzwerk einführt und aufrechterhält. Sie bietet auch Anwendungen und Konfigurationsoptionen, um Ihr Erlebnis und Ihren Arbeitsablauf zu personalisieren. Erfahren Sie mehr in unserer [Dokumentation](/docs/).

## Was kann ich im I2P-Netzwerk tun?

Das Netzwerk bietet eine Anwendungsebene für Dienste, Anwendungen und Netzwerkmanagement. Das Netzwerk hat auch ein eigenes einzigartiges DNS, das Self-Hosting und Spiegelung von Inhalten aus dem Internet (Clearnet) ermöglicht. Das I2P-Netzwerk funktioniert genauso wie das Internet. Die Java-Software beinhaltet einen BitTorrent-Client und E-Mail sowie eine statische Website-Vorlage. Andere Anwendungen können leicht zu Ihrer Router-Konsole hinzugefügt werden.

## Ein Überblick über das Netzwerk

I2P verwendet Kryptographie, um eine Vielzahl von Eigenschaften für die Tunnel, die es baut, und die Kommunikationen, die es transportiert, zu erreichen. I2P-Tunnel verwenden Transports, [NTCP2](/docs/specs/ntcp2/) und [SSU2](/docs/specs/ssu2/), um den über sie transportierten Datenverkehr zu verschleiern. Verbindungen sind von Router zu Router und von Client zu Client (Ende-zu-Ende) verschlüsselt. Vorwärtsgeheimnis wird für alle Verbindungen bereitgestellt. Da I2P kryptographisch adressiert ist, sind I2P-Netzwerkadressen selbstauthentifizierend und gehören nur dem Benutzer, der sie erzeugt hat.

Das Netzwerk besteht aus Peers ("Routern") und unidirektionalen eingehenden und ausgehenden virtuellen Tunneln. Router kommunizieren miteinander über Protokolle, die auf bestehenden Transportmechanismen (TCP, UDP) basieren, und leiten Nachrichten weiter. Client-Anwendungen haben ihre eigene kryptographische Kennung ("Destination"), die es ihnen ermöglicht, Nachrichten zu senden und zu empfangen. Diese Clients können sich mit jedem Router verbinden und die vorübergehende Zuweisung ("Lease") einiger Tunnel autorisieren, die zum Senden und Empfangen von Nachrichten über das Netzwerk verwendet werden. I2P hat seine eigene interne Netzwerkdatenbank (mit einer Modifikation des Kademlia DHT), um Routing- und Kontaktdaten sicher zu verteilen.

## Über Dezentralisierung und das I2P-Netzwerk

Das I2P-Netzwerk ist fast vollständig dezentralisiert, mit Ausnahme der sogenannten Reseed-Server. Dies dient zur Bewältigung des DHT (Distributed Hash Table) Bootstrap-Problems. Grundsätzlich gibt es keine gute und zuverlässige Möglichkeit, mindestens einen permanenten Bootstrap-Knoten zu vermeiden, den Nicht-Netzwerk-Teilnehmer finden können, um sich zu verbinden. Sobald ein Router mit dem Netzwerk verbunden ist, entdeckt er Peers, indem er "explorative" Tunnel baut; um jedoch die anfängliche Verbindung herzustellen, ist ein Reseed-Host erforderlich, um Verbindungen herzustellen und einen neuen Router in das Netzwerk aufzunehmen. Reseed-Server können erkennen, wenn ein neuer Router ein Reseed von ihnen heruntergeladen hat, aber sonst nichts über den Datenverkehr im I2P-Netzwerk.

## Vergleiche

Es gibt eine Vielzahl anderer Anwendungen und Projekte, die anonymer Kommunikation arbeiten, und I2P wurde von vielen ihrer Bemühungen inspiriert. Dies ist keine umfassende Liste von Anonymitätsressourcen - sowohl [freehavens Anonymity Bibliography](http://freehaven.net/anonbib/topic.html) als auch [GNUnets verwandte Projekte](https://www.gnunet.org/links/) erfüllen diesen Zweck gut. Dennoch stechen einige Systeme für einen weiteren Vergleich hervor. Erfahren Sie mehr darüber, wie I2P im Vergleich zu anderen Anonymitätsnetzwerken abschneidet, in unserer [detaillierten Vergleichsdokumentation](/docs/overview/comparison/).
