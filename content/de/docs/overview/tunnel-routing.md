---
title: "Tunnel-Routing"
description: "Überblick über I2P-Tunnel-Terminologie, -Aufbau und -Lebenszyklus"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Überblick

I2P baut temporäre, unidirektionale Tunnel – geordnete Sequenzen von Routern, die verschlüsselten Verkehr weiterleiten. Tunnel werden als **inbound** (Nachrichten fließen zum Ersteller hin) oder **outbound** (Nachrichten fließen vom Ersteller weg) klassifiziert.

Ein typischer Austausch leitet Alices Nachricht durch einen ihrer outbound tunnels, weist den outbound Endpunkt an, sie an das gateway eines von Bobs inbound tunnels weiterzuleiten, und dann empfängt Bob sie an seinem inbound Endpunkt.

![Alice verbindet sich durch ihren ausgehenden Tunnel mit Bob über seinen eingehenden Tunnel](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

Tunnels haben eine feste Lebensdauer von 10 Minuten und übertragen Nachrichten mit fester Größe von 1024 Bytes (1028 Bytes inklusive des Tunnel-Headers), um Traffic-Analyse auf Basis von Nachrichtengröße oder Zeitmustern zu verhindern.

## Tunnel-Vokabular

- **Tunnel gateway:** Erster Router in einem Tunnel. Bei eingehenden Tunneln erscheint die Identität dieses Routers im veröffentlichten [LeaseSet](/docs/specs/common-structures/). Bei ausgehenden Tunneln ist das Gateway der ursprüngliche Router (A und D oben).
- **Tunnel endpoint:** Letzter Router in einem Tunnel (C und F oben).
- **Tunnel participant:** Zwischengeschalteter Router in einem Tunnel (B und E oben). Participants können weder ihre Position noch die Tunnel-Richtung bestimmen.
- **n-hop tunnel:** Anzahl der Sprünge zwischen Routern.
  - **0-hop:** Gateway und Endpoint sind derselbe Router – minimale Anonymität.
  - **1-hop:** Gateway verbindet sich direkt mit dem Endpoint – niedrige Latenz, geringe Anonymität.
  - **2-hop:** Standard für explorative Tunnel; ausgewogenes Verhältnis von Sicherheit und Leistung.
  - **3-hop:** Empfohlen für Anwendungen, die starke Anonymität erfordern.
- **Tunnel ID:** 4-Byte-Ganzzahl, eindeutig pro Router und pro Hop, zufällig vom Ersteller gewählt. Jeder Hop empfängt und leitet mit unterschiedlichen IDs weiter.

## Tunnel-Build-Informationen

Router, die Gateway-, Participant- und Endpoint-Rollen übernehmen, erhalten unterschiedliche Datensätze innerhalb der Tunnel Build Message. Modernes I2P unterstützt zwei Methoden:

- **ElGamal** (veraltet, 528-Byte-Datensätze)
- **ECIES-X25519** (aktuell, 218-Byte-Datensätze über Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**Gateway empfängt:** - Tunnel-Schicht-Schlüssel (AES-256 oder ChaCha20-Schlüssel je nach Tunnel-Typ) - Tunnel-IV-Schlüssel (zur Verschlüsselung von Initialisierungsvektoren) - Reply-Schlüssel und Reply-IV (zur Verschlüsselung der Build-Antwort) - Tunnel-ID (nur Inbound-Gateways) - Next-Hop-Identity-Hash und Tunnel-ID (falls nicht terminal)

**Intermediate-Teilnehmer erhalten:** - Tunnel-Layer-Schlüssel und IV-Schlüssel für ihren Hop - Tunnel-ID und Informationen zum nächsten Hop - Reply-Schlüssel und IV für die Verschlüsselung der Build-Antwort

**Endpoints erhalten:** - Tunnel-Schicht- und IV-Schlüssel - Antwort-Router und Tunnel-ID (nur ausgehende Endpoints) - Antwortschlüssel und IV (nur ausgehende Endpoints)

Für vollständige Details siehe die [Tunnel Creation Specification](/docs/specs/implementation/) und [ECIES Tunnel Creation Specification](/docs/specs/implementation/).

## Tunnel Pooling

Router gruppieren Tunnel in **Tunnel-Pools** für Redundanz und Lastverteilung. Jeder Pool verwaltet mehrere parallele Tunnel, was ein Failover ermöglicht, wenn einer ausfällt. Intern verwendete Pools sind **exploratory tunnels**, während anwendungsspezifische Pools **client tunnels** sind.

Jedes Ziel verwaltet separate eingehende und ausgehende Pools, die durch I2CP-Optionen konfiguriert werden (Tunnelanzahl, Backup-Anzahl, Länge und QoS-Parameter). Router überwachen die Tunnel-Gesundheit, führen regelmäßige Tests durch und bauen ausgefallene Tunnel automatisch neu auf, um die Pool-Größe beizubehalten.

## Tunnel-Pooling

**0-hop Tunnels**: Bieten nur plausible Abstreitbarkeit. Der Datenverkehr stammt immer vom selben Router und endet dort – wird für jede anonyme Nutzung nicht empfohlen.

**1-hop Tunnels**: Bieten grundlegende Anonymität gegen passive Beobachter, sind jedoch anfällig, wenn ein Angreifer diesen einzelnen Hop kontrolliert.

**2-Hop-Tunnel**: Beinhalten zwei entfernte Router und erhöhen die Angriffskosten erheblich. Standard für explorative Pools.

**3-Hop-Tunnel**: Empfohlen für Anwendungen, die robusten Anonymitätsschutz erfordern. Zusätzliche Hops erhöhen die Latenz ohne nennenswerten Sicherheitsgewinn.

**Standardeinstellungen**: Router verwenden **2-Hop** exploratory tunnels und anwendungsspezifische **2 oder 3 Hop** client tunnels, um Leistung und Anonymität auszubalancieren.

## Tunnel-Länge

Router testen periodisch Tunnel, indem sie eine `DeliveryStatusMessage` durch einen ausgehenden Tunnel zu einem eingehenden Tunnel senden. Wenn der Test fehlschlägt, erhalten beide Tunnel eine negative Profilgewichtung. Aufeinanderfolgende Fehlschläge markieren einen Tunnel als unbrauchbar; der Router baut dann einen Ersatz auf und veröffentlicht ein neues LeaseSet. Die Ergebnisse fließen in die Peer-Kapazitätsmetriken ein, die vom [Peer-Auswahlsystem](/docs/overview/tunnel-routing/) verwendet werden.

## Tunnel-Tests

Router konstruieren Tunnel mithilfe einer nicht-interaktiven **Telescoping**-Methode: Eine einzelne Tunnel Build Message wird Hop für Hop weitergeleitet. Jeder Hop entschlüsselt seinen Datensatz, fügt seine Antwort hinzu und leitet die Nachricht weiter. Der letzte Hop sendet die aggregierte Build-Antwort über einen anderen Pfad zurück, um Korrelation zu verhindern. Moderne Implementierungen verwenden **Short Tunnel Build Messages (STBM)** für ECIES und **Variable Tunnel Build Messages (VTBM)** für Legacy-Pfade. Jeder Datensatz wird pro Hop mittels ElGamal oder ECIES-X25519 verschlüsselt.

## Tunnel-Erstellung

Tunnel-Verkehr verwendet mehrschichtige Verschlüsselung. Jeder Hop fügt eine Verschlüsselungsschicht hinzu oder entfernt sie, während Nachrichten den Tunnel durchlaufen.

- **ElGamal tunnels:** AES-256/CBC für Payloads mit PKCS#5-Padding.
- **ECIES tunnels:** ChaCha20 oder ChaCha20-Poly1305 für authentifizierte Verschlüsselung.

Jeder Hop hat zwei Schlüssel: einen **Layer-Schlüssel** und einen **IV-Schlüssel**. Router entschlüsseln die IV, verwenden sie zur Verarbeitung der Nutzdaten und verschlüsseln die IV dann erneut, bevor sie die Nachricht weiterleiten. Dieses doppelte IV-Schema verhindert Message-Tagging.

Ausgehende Gateways entschlüsseln alle Schichten im Voraus, sodass Endpunkte Klartext erhalten, nachdem alle Teilnehmer Verschlüsselung hinzugefügt haben. Eingehende Tunnel verschlüsseln in die entgegengesetzte Richtung. Teilnehmer können weder die Richtung noch die Länge des Tunnels bestimmen.

## Tunnel-Verschlüsselung

- Dynamische Tunnel-Lebensdauern und adaptive Pool-Größenanpassung für Netzwerk-Lastverteilung
- Alternative Tunnel-Teststrategien und individuelle Hop-Diagnosen
- Optional Proof-of-Work oder Bandwidth-Zertifikat-Validierung (implementiert in API 0.9.65+)
- Traffic Shaping und Chaff-Insertion-Forschung für Endpunkt-Mixing
- Fortgesetzte Ausmusterung von ElGamal und Migration zu ECIES-X25519

## Laufende Entwicklung

- [Tunnel Implementation Specification](/docs/specs/implementation/)
- [Tunnel Creation Specification (ElGamal)](/docs/specs/implementation/)
- [Tunnel Creation Specification (ECIES-X25519)](/docs/specs/implementation/)
- [Tunnel Message Specification](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Peer Profiling and Selection](/docs/overview/tunnel-routing/)
- [I2P Bedrohungsmodell](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag Encryption](/docs/legacy/elgamal-aes/)
- [I2CP-Optionen](/docs/specs/i2cp/)
