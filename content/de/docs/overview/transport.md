---
title: "Transport-Übersicht"
description: "Überblick über die Transportschicht von I2P für punkt-zu-punkt router-Kommunikation"
slug: "transport"
aliases:
  - "/de/transport"
  - "/de/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transports in I2P

Ein "Transport" in I2P ist eine Methode für direkte, punkt-zu-punkt Kommunikation zwischen zwei routern. Transports müssen Vertraulichkeit und Integrität gegen externe Angreifer bieten und gleichzeitig authentifizieren, dass der kontaktierte router derjenige ist, der eine bestimmte Nachricht erhalten soll.

I2P unterstützt mehrere Transporte gleichzeitig. Derzeit sind drei Transporte implementiert:

1. [NTCP](/docs/legacy/ntcp/), ein Java New I/O (NIO) TCP-Transport
2. [SSU](/docs/legacy/ssu/), oder Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), eine neue Version von NTCP

Jedes bietet ein "Verbindungs"-Paradigma mit Authentifizierung, Flusskontrolle, Bestätigungen und Neuübertragung.

- Zuverlässige Zustellung von [I2NP](/docs/specs/i2np/) Nachrichten. Transports unterstützen NUR die Zustellung von I2NP Nachrichten. Sie sind keine allgemeinen Datenleitungen.
- Die Zustellung von Nachrichten in der richtigen Reihenfolge wird NICHT von allen Transports garantiert.
- Verwaltung einer Sammlung von router-Adressen, eine oder mehrere für jeden Transport, die der router als seine globalen Kontaktinformationen veröffentlicht (die RouterInfo). Jeder Transport kann sich über eine dieser Adressen verbinden, die IPv4 oder (ab Version 0.9.8) IPv6 sein können.
- Auswahl des besten Transports für jede ausgehende Nachricht
- Warteschlangen für ausgehende Nachrichten nach Priorität
- Bandbreitenbegrenzung, sowohl ausgehend als auch eingehend, entsprechend der router-Konfiguration
- Aufbau und Abbau von Transport-Verbindungen
- Verschlüsselung der Punkt-zu-Punkt-Kommunikation
- Verwaltung von Verbindungslimits für jeden Transport, Implementierung verschiedener Schwellenwerte für diese Limits und Kommunikation des Schwellenwert-Status an den router, damit dieser betriebliche Änderungen basierend auf dem Status vornehmen kann
- Firewall-Port-Öffnung mit UPnP (Universal Plug and Play)
- Kooperative NAT/Firewall-Durchquerung
- Lokale IP-Erkennung durch verschiedene Methoden, einschließlich UPnP, Inspektion eingehender Verbindungen und Aufzählung von Netzwerkgeräten
- Koordination des Firewall-Status und der lokalen IP sowie Änderungen an beiden zwischen den Transports
- Kommunikation des Firewall-Status und der lokalen IP sowie Änderungen an beiden an den router und die Benutzeroberfläche
- Bestimmung einer Konsens-Uhr, die verwendet wird, um regelmäßig die router-Uhr zu aktualisieren, als Backup für NTP
- Verwaltung des Status für jeden Peer, einschließlich ob er verbunden ist, ob er kürzlich verbunden war und ob er beim letzten Versuch erreichbar war
- Qualifikation gültiger IP-Adressen nach einem lokalen Regelsatz
- Befolgen der automatisierten und manuellen Listen gesperrter Peers, die vom router verwaltet werden, und Verweigerung ausgehender und eingehender Verbindungen zu diesen Peers

---

Das Transport-Subsystem in I2P bietet die folgenden Dienste:

## Transport-Dienste

---

- Ein router hat keine veröffentlichten Adressen, daher wird er als "versteckt" betrachtet und kann keine eingehenden Verbindungen empfangen
- Ein router ist durch eine Firewall geschützt und veröffentlicht daher eine SSU-Adresse, die eine Liste kooperierender Peers oder "Introducer" enthält, die beim NAT-Traversal helfen (siehe [die SSU-Spezifikation](/docs/legacy/ssu/) für Details)
- Ein router ist nicht durch eine Firewall geschützt oder seine NAT-Ports sind offen; er veröffentlicht sowohl NTCP- als auch SSU-Adressen, die direkt zugängliche IP-Adressen und Ports enthalten.

Das Transport-Subsystem verwaltet eine Reihe von router-Adressen, von denen jede eine Transportmethode, IP und Port auflistet. Diese Adressen stellen die beworbenen Kontaktpunkte dar und werden vom router in der netDb veröffentlicht. Adressen können auch eine beliebige Menge zusätzlicher Optionen enthalten.

## Transport-Adressen

Jede Transportmethode kann mehrere router-Adressen veröffentlichen.

Typische Szenarien sind:

---

- Konfiguration der Transportpräferenzen
- Ob der Transport bereits mit dem Peer verbunden ist
- Die Anzahl der aktuellen Verbindungen im Vergleich zu verschiedenen Verbindungsgrenzwerten
- Ob kürzliche Verbindungsversuche zum Peer fehlgeschlagen sind
- Die Größe der Nachricht, da verschiedene Transporte unterschiedliche Größenbeschränkungen haben
- Ob der Peer eingehende Verbindungen für diesen Transport akzeptieren kann, wie in seiner RouterInfo angekündigt
- Ob die Verbindung indirekt (Introducer erforderlich) oder direkt wäre
- Die Transportpräferenz des Peers, wie in seiner RouterInfo angekündigt

Das Transportsystem übermittelt ausschließlich [I2NP messages](/docs/specs/i2np/). Der für eine Nachricht gewählte Transport ist unabhängig von den oberen Protokollschichten und Inhalten (Router- oder Client-Nachrichten, ob eine externe Anwendung TCP oder UDP zur Verbindung mit I2P verwendete, ob die obere Schicht [die streaming library](/docs/api/streaming/) oder [datagrams](/docs/api/datagrams/) nutzte, usw.).

## Transport-Auswahl

Für jede ausgehende Nachricht fordert das Transport-System "Gebote" von jedem Transport an. Der Transport mit dem niedrigsten (besten) Gebot gewinnt die Ausschreibung und erhält die Nachricht zur Zustellung. Ein Transport kann die Abgabe eines Gebots verweigern.

Ob ein Transport ein Gebot abgibt und mit welchem Wert, hängt von zahlreichen Faktoren ab:

Im Allgemeinen werden die Bid-Werte so gewählt, dass zwei router zu jedem Zeitpunkt nur durch einen einzigen Transport verbunden sind. Dies ist jedoch keine Anforderung.

- Ein TLS/SSH-ähnlicher Transport
- Ein "indirekter" Transport für Router, die nicht von allen anderen Routern erreichbar sind (eine Form von "eingeschränkten Routen")
- Tor-kompatible Pluggable Transports

---

Zusätzliche Transportprotokolle können entwickelt werden, einschließlich:

## Neue Transporte und zukünftige Arbeiten

Die Arbeit an der Anpassung der Standard-Verbindungslimits für jeden Transport geht weiter. I2P ist als "Mesh-Netzwerk" konzipiert, bei dem davon ausgegangen wird, dass sich jeder router mit jedem anderen router verbinden kann. Diese Annahme kann durch router gebrochen werden, die ihre Verbindungslimits überschritten haben, und durch router, die sich hinter restriktiven Stateful-Firewalls befinden (eingeschränkte Routen).

- Ein TLS/SSH-ähnlicher Transport
- Ein „indirekter“ Transport für Router, die nicht von allen anderen Routern erreichbar sind (eine Form von „eingeschränkten Routen“)
- Tor-kompatible einsetzbare Transportschichten

Die aktuellen Verbindungslimits sind für SSU höher als für NTCP, basierend auf der Annahme, dass die Speicheranforderungen für eine NTCP-Verbindung höher sind als die für SSU. Da sich NTCP-Puffer jedoch teilweise im Kernel befinden und SSU-Puffer auf dem Java-Heap liegen, ist diese Annahme schwer zu überprüfen.

Analysieren Sie [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) und sehen Sie, wie Transport-Layer-Padding die Situation verbessern könnte.

Analysieren Sie [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) und prüfen Sie, wie eine Auffüllung auf Transportschicht-Ebene die Dinge verbessern könnte.
