---
title: "I2P: Ein skalierbares Framework für anonyme Kommunikation"
description: "Technische Einführung in die I2P-Architektur und -Funktionsweise"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Einführung

I2P ist eine skalierbare, selbstorganisierende, widerstandsfähige paketvermittelte anonyme Netzwerkschicht, auf der beliebig viele verschiedene anonymitäts- oder sicherheitsbewusste Anwendungen betrieben werden können. Jede dieser Anwendungen kann ihre eigenen Kompromisse zwischen Anonymität, Latenz und Durchsatz treffen, ohne sich um die korrekte Implementierung eines free route mixnet kümmern zu müssen, wodurch sie ihre Aktivität mit der größeren Anonymitätsmenge der Benutzer vermischen können, die bereits auf I2P laufen.

Bereits verfügbare Anwendungen bieten die volle Bandbreite typischer Internet-Aktivitäten — **anonymes** Web-Browsing, Web-Hosting, Chat, Dateifreigabe, E-Mail, Blogging und Content-Syndication sowie mehrere weitere Anwendungen, die sich in der Entwicklung befinden.

- **Web-Browsing:** mit jedem bestehenden Browser, der einen Proxy unterstützt  
- **Chat:** IRC und andere Protokolle  
- **Dateifreigabe:** [I2PSnark](#i2psnark) und andere Anwendungen  
- **E-Mail:** [Susimail](#i2pmail) und andere Anwendungen  
- **Blog:** mit jedem lokalen Webserver oder verfügbaren Plugins

Im Gegensatz zu Websites, die in Content-Distribution-Netzwerken wie [Freenet](/docs/overview/comparison#freenet) oder [GNUnet](https://www.gnunet.org/) gehostet werden, sind die auf I2P gehosteten Dienste vollständig interaktiv – es gibt traditionelle Suchmaschinen im Web-Stil, Bulletin Boards, Blogs, auf denen man kommentieren kann, datenbankgestützte Websites und Brücken zur Abfrage statischer Systeme wie Freenet, ohne dass diese lokal installiert werden müssen.

Bei all diesen anonymitätsfähigen Anwendungen fungiert I2P als **nachrichtenorientierte Middleware** – Anwendungen geben Daten an, die an eine kryptografische Kennung (eine "destination") gesendet werden sollen, und I2P stellt sicher, dass diese sicher und anonym ankommen. I2P enthält auch eine einfache [Streaming-Bibliothek](#streaming), die es ermöglicht, I2Ps anonyme Best-Effort-Nachrichten als zuverlässige, geordnete Datenströme zu übertragen, mit TCP-basierter Überlastungskontrolle, die auf das hohe Bandbreiten-Verzögerungs-Produkt des Netzwerks abgestimmt ist.

Obwohl einfache SOCKS-Proxys entwickelt wurden, um bestehende Anwendungen anzubinden, ist ihr Nutzen begrenzt, da die meisten Anwendungen sensible Informationen in einem anonymen Kontext preisgeben. Der sicherste Ansatz ist es, die Anwendung zu **prüfen und anzupassen**, damit sie die I2P-APIs direkt verwendet.

I2P ist kein Forschungsprojekt – weder akademisch, kommerziell noch staatlich –, sondern eine technische Entwicklung, die darauf abzielt, nutzbare Anonymität bereitzustellen. Seit Anfang 2003 wird es kontinuierlich von einer verteilten Gruppe von Mitwirkenden weltweit entwickelt. Alle I2P-Arbeiten sind **Open Source** auf der [offiziellen Website](https://geti2p.net/), hauptsächlich als Public Domain veröffentlicht, wobei einige Komponenten unter freizügigen BSD-ähnlichen Lizenzen stehen. Mehrere GPL-lizenzierte Clientanwendungen sind verfügbar, wie z. B. [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) und [I2PSnark](#i2psnark). Die Finanzierung erfolgt ausschließlich durch Nutzerspenden.

---

## Betrieb

### Overview

I2P unterscheidet klar zwischen Routern (Knoten, die am Netzwerk teilnehmen) und Destinations (anonyme Endpunkte für Anwendungen). Der Betrieb von I2P selbst ist nicht geheim; verborgen bleibt **was** der Nutzer tut und welchen Router seine Destinations verwenden. Endnutzer betreiben typischerweise mehrere Destinations (z.B. eine fürs Web-Browsing, eine weitere fürs Hosting, eine andere für IRC).

Ein Schlüsselkonzept in I2P ist der **tunnel** — ein unidirektionaler verschlüsselter Pfad durch eine Reihe von Routern. Jeder Router entschlüsselt nur eine Schicht und erfährt nur den nächsten Hop. Tunnels laufen nach 10 Minuten ab und müssen neu aufgebaut werden.

![Schema für eingehende und ausgehende Tunnel](/images/tunnels.png)   *Abbildung 1: Es gibt zwei Arten von Tunneln – eingehende und ausgehende.*

- **Outbound tunnels** senden Nachrichten vom Ersteller weg.  
- **Inbound tunnels** bringen Nachrichten zum Ersteller zurück.

Die Kombination dieser ermöglicht bidirektionale Kommunikation. Zum Beispiel nutzt "Alice" einen ausgehenden Tunnel, um an "Bobs" eingehenden Tunnel zu senden. Alice verschlüsselt ihre Nachricht mit Routing-Anweisungen zu Bobs eingehendem Gateway.

Ein weiteres Schlüsselkonzept ist die **network database** oder **netDb**, die Metadaten über Router und Ziele verteilt:

- **RouterInfo:** Enthält Router-Kontaktinformationen und Schlüsselmaterial.
- **LeaseSet:** Enthält Informationen, die benötigt werden, um ein Ziel zu kontaktieren (tunnel gateways, Ablaufzeiten, Verschlüsselungsschlüssel).

Router veröffentlichen ihre RouterInfo direkt in der netDb; LeaseSets werden zur Wahrung der Anonymität durch ausgehende Tunnel gesendet.

Um Tunnel zu bauen, fragt Alice die netDb nach RouterInfo-Einträgen ab, um Peers auszuwählen, und sendet verschlüsselte Tunnel-Build-Nachrichten Hop-für-Hop, bis der Tunnel vollständig ist.

![Router-Informationen werden verwendet, um Tunnel zu bauen](/images/netdb_get_routerinfo_2.png)   *Abbildung 2: Router-Informationen werden verwendet, um Tunnel zu bauen.*

Um an Bob zu senden, schaut Alice Bobs LeaseSet nach und verwendet einen ihrer ausgehenden Tunnel, um Daten zum Gateway von Bobs eingehendem Tunnel zu routen.

![LeaseSets verbinden eingehende und ausgehende Tunnel](/images/netdb_get_leaseset.png)   *Abbildung 3: LeaseSets verbinden ausgehende und eingehende Tunnel.*

Da I2P nachrichtenbasiert ist, fügt es **End-to-End garlic encryption** hinzu, um Nachrichten selbst vor dem ausgehenden Endpunkt oder eingehenden Gateway zu schützen. Eine Garlic-Nachricht umhüllt mehrere verschlüsselte „Cloves" (Nachrichten), um Metadaten zu verbergen und die Anonymität zu verbessern.

Anwendungen können entweder die Nachrichtenschnittstelle direkt verwenden oder sich auf die [Streaming-Bibliothek](#streaming) für zuverlässige Verbindungen verlassen.

---

### Tunnels

Sowohl eingehende als auch ausgehende Tunnel verwenden geschichtete Verschlüsselung, unterscheiden sich jedoch im Aufbau:

- In **inbound tunnels** entschlüsselt der Ersteller (der Endpunkt) alle Schichten.
- In **outbound tunnels** entschlüsselt der Ersteller (das Gateway) die Schichten vorab, um Klarheit am Endpunkt zu gewährleisten.

I2P profiliert Peers anhand indirekter Metriken wie Latenz und Zuverlässigkeit ohne direktes Probing. Basierend auf diesen Profilen werden Peers dynamisch in vier Stufen gruppiert:

1. Schnell und hohe Kapazität
2. Hohe Kapazität
3. Nicht ausgefallen
4. Ausgefallen

Die Auswahl von Tunnel-Peers bevorzugt typischerweise Peers mit hoher Kapazität, die zufällig ausgewählt werden, um Anonymität und Leistung auszugleichen, mit zusätzlichen XOR-basierten Sortierungsstrategien zur Abwehr von Vorgängerangriffen und netDb-Harvesting.

Für tiefergehende Details siehe die [Tunnel-Spezifikation](/docs/specs/implementation).

---

### Übersicht

Router, die am **floodfill** Distributed Hash Table (DHT) teilnehmen, speichern und beantworten LeaseSet-Anfragen. Die DHT verwendet eine Variante von [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Floodfill-Router werden automatisch ausgewählt, wenn sie über ausreichende Kapazität und Stabilität verfügen, oder können manuell konfiguriert werden.

- **RouterInfo:** Beschreibt die Fähigkeiten und Transporte eines Routers.  
- **LeaseSet:** Beschreibt die Tunnel und Verschlüsselungsschlüssel eines Ziels.

Alle Daten in der netDb sind vom Herausgeber signiert und mit einem Zeitstempel versehen, um Replay- oder Stale-Entry-Angriffe zu verhindern. Die Zeitsynchronisation wird durch SNTP und Transport-Layer-Skew-Erkennung aufrechterhalten.

#### Additional concepts

- **Unveröffentlichte und verschlüsselte LeaseSets:**  
  Ein Ziel kann privat bleiben, indem es sein LeaseSet nicht veröffentlicht und es nur mit vertrauenswürdigen Peers teilt. Der Zugriff erfordert den entsprechenden Entschlüsselungsschlüssel.

- **Bootstrapping (reseeding):**  
  Um dem Netzwerk beizutreten, lädt ein neuer router signierte RouterInfo-Dateien von vertrauenswürdigen HTTPS-Reseed-Servern herunter.

- **Lookup-Skalierbarkeit:**  
  I2P verwendet **iterative**, nicht rekursive, Lookups, um die DHT-Skalierbarkeit und -Sicherheit zu verbessern.

---

### Tunnels

Moderne I2P-Kommunikation verwendet zwei vollständig verschlüsselte Transportprotokolle:

- **[NTCP2](/docs/specs/ntcp2):** Verschlüsseltes TCP-basiertes Protokoll  
- **[SSU2](/docs/specs/ssu2):** Verschlüsseltes UDP-basiertes Protokoll

Beide basieren auf dem modernen [Noise Protocol Framework](https://noiseprotocol.org/) und bieten starke Authentifizierung sowie Widerstandsfähigkeit gegen Traffic-Fingerprinting. Sie ersetzten die veralteten NTCP- und SSU-Protokolle (vollständig eingestellt seit 2023).

**NTCP2** bietet verschlüsseltes, effizientes Streaming über TCP.

**SSU2** bietet UDP-basierte Zuverlässigkeit, NAT-Traversierung und optionales Hole Punching. SSU2 ist konzeptionell ähnlich wie WireGuard oder QUIC und bringt Zuverlässigkeit und Anonymität in Einklang.

Router können sowohl IPv4 als auch IPv6 unterstützen und veröffentlichen ihre Transportadressen und -kosten in der netDb. Der Transport einer Verbindung wird dynamisch durch ein **Bietsystem** ausgewählt, das auf Bedingungen und bestehende Verbindungen optimiert.

---

### Netzwerk-Datenbank (netDb)

I2P verwendet mehrschichtige Verschlüsselung für alle Komponenten: Transporte, Tunnel, Garlic-Nachrichten und die netDb.

Aktuelle Primitiven umfassen:

- X25519 für Schlüsselaustausch  
- EdDSA (Ed25519) für Signaturen  
- ChaCha20-Poly1305 für authentifizierte Verschlüsselung  
- SHA-256 für Hashing  
- AES256 für tunnel Layer-Verschlüsselung

Legacy-Algorithmen (ElGamal, DSA-SHA1, ECDSA) bleiben aus Gründen der Abwärtskompatibilität erhalten.

I2P führt derzeit hybride Post-Quanten (PQ) kryptografische Verfahren ein, die **X25519** mit **ML-KEM** kombinieren, um „Harvest-now, decrypt-later"-Angriffe (Jetzt sammeln, später entschlüsseln) abzuwehren.

#### Garlic Messages

Garlic-Nachrichten erweitern Onion-Routing, indem sie mehrere verschlüsselte "Cloves" (Segmente) mit unabhängigen Zustellungsanweisungen gruppieren. Diese ermöglichen Routing-Flexibilität auf Nachrichtenebene und einheitliches Traffic-Padding.

#### Session Tags

Zwei kryptografische Systeme werden für die Ende-zu-Ende-Verschlüsselung unterstützt:

- **ElGamal/AES+SessionTags (veraltet):**  
  Verwendet vorab übermittelte Session-Tags als 32-Byte-Nonces. Aufgrund von Ineffizienz mittlerweile veraltet.

- **ECIES-X25519-AEAD-Ratchet (aktuell):**  
  Verwendet ChaCha20-Poly1305 und synchronisierte HKDF-basierte PRNGs, um ephemerale Session-Keys und 8-Byte-Tags dynamisch zu generieren, wodurch CPU-, Speicher- und Bandbreitenaufwand reduziert wird, während Forward Secrecy (Vorwärtsgeheimhaltung) erhalten bleibt.

---

## Future of the Protocol

Wichtige Forschungsbereiche konzentrieren sich auf die Aufrechterhaltung der Sicherheit gegen staatliche Gegner und die Einführung von Post-Quanten-Schutzmaßnahmen. Zwei frühe Designkonzepte – **restricted routes** und **variable latency** – wurden durch moderne Entwicklungen abgelöst.

### Restricted Route Operation

Die ursprünglichen Konzepte für eingeschränktes Routing zielten darauf ab, IP-Adressen zu verschleiern. Dieser Bedarf wurde weitgehend gemildert durch:

- UPnP für automatische Portweiterleitung  
- Robuste NAT-Durchquerung in SSU2  
- IPv6-Unterstützung  
- Kooperative Introducer und NAT-Hole-Punching  
- Optionale Overlay-Konnektivität (z.B. Yggdrasil)

Daher erreicht das moderne I2P die gleichen Ziele auf praktischere Weise ohne komplexes eingeschränktes Routing.

---

## Similar Systems

I2P integriert Konzepte aus nachrichtenorientierter Middleware, DHTs und Mixnets. Seine Innovation liegt darin, diese zu einer nutzbaren, selbstorganisierenden Anonymitätsplattform zu kombinieren.

### Transportprotokolle

*[Website](https://www.torproject.org/)*

**Tor** und **I2P** teilen gemeinsame Ziele, unterscheiden sich jedoch architektonisch:

- **Tor:** Verbindungsvermittelt; setzt auf vertrauenswürdige Verzeichnisbehörden. (~10k Relays)  
- **I2P:** Paketvermittelt; vollständig verteiltes DHT-gesteuertes Netzwerk. (~50k Router)

I2Ps unidirektionale Tunnel exponieren weniger Metadaten und ermöglichen flexible Routing-Pfade, während Tor sich auf anonymen **Internetzugang (Outproxying)** konzentriert. I2P unterstützt stattdessen anonymes **In-Network-Hosting**.

### Kryptographie

*[Website](https://freenetproject.org/)*

**Freenet** konzentriert sich auf anonymes, dauerhaftes Veröffentlichen und Abrufen von Dateien. **I2P** bietet im Gegensatz dazu eine **Echtzeit-Kommunikationsschicht** für interaktive Nutzung (Web, Chat, Torrents). Zusammen ergänzen sich die beiden Systeme – Freenet bietet zensurresistente Speicherung; I2P bietet Transportanonymität.

### Other Networks

- **Lokinet:** IP-basiertes Overlay unter Verwendung incentivierter Service-Nodes.  
- **Nym:** Mixnet der nächsten Generation mit Schwerpunkt auf Metadatenschutz durch Cover-Traffic bei höherer Latenz.

---

## Appendix A: Application Layer

I2P selbst kümmert sich nur um den Nachrichtentransport. Funktionalität auf Anwendungsebene wird extern durch APIs und Bibliotheken implementiert.

### Streaming Library {#streaming}

Die **Streaming-Bibliothek** fungiert als TCP-Analogon von I2P, mit einem Sliding-Window-Protokoll und Congestion Control, die für anonymen Transport mit hoher Latenz optimiert sind.

Typische HTTP-Anfrage-/Antwort-Muster können aufgrund von Nachrichtenbündelungsoptimierungen oft in einem einzigen Durchlauf abgeschlossen werden.

### Naming Library and Address Book

*Entwickelt von: mihi, Ragnarok*   Siehe die Seite [Benennung und Adressbuch](/docs/overview/naming).

Das Namenssystem von I2P ist **lokal und dezentralisiert** und vermeidet globale Namen im DNS-Stil. Jeder Router verwaltet eine lokale Zuordnung von lesbaren Namen zu Zielen. Optional können auf Web-of-Trust basierende Adressbücher mit vertrauenswürdigen Peers geteilt oder von diesen importiert werden.

Dieser Ansatz vermeidet zentrale Autoritäten und umgeht Sybil-Schwachstellen, die globalen oder abstimmungsbasierten Namenssystemen innewohnen.

### Eingeschränkter Routenbetrieb

*Entwickelt von: mihi*

**I2PTunnel** ist die Haupt-Client-Schnittstelle, die anonymes TCP-Proxying ermöglicht. Es unterstützt:

- **Client-Tunnel** (ausgehend zu I2P-Zielen)  
- **HTTP-Client (eepproxy)** für ".i2p"-Domains  
- **Server-Tunnel** (eingehend von I2P zu einem lokalen Dienst)  
- **HTTP-Server-Tunnel** (sichere Proxy-Bereitstellung von Webdiensten)

Outproxying (zum regulären Internet) ist optional und wird durch freiwillig betriebene "Server"-Tunnel implementiert.

### I2PSnark {#i2psnark}

*Entwickelt von: jrandom, et al — portiert von [Snark](http://www.klomp.org/snark/)*

Im I2P-Paket enthalten ist **I2PSnark**, ein anonymer Multi-Torrent-BitTorrent-Client mit DHT- und UDP-Unterstützung, der über eine Weboberfläche zugänglich ist.

### Tor

*Entwickelt von: postman, susi23, mastiejaner*

**I2Pmail** bietet anonyme E-Mail über I2PTunnel-Verbindungen. **Susimail** ist ein webbasierter Client, der speziell entwickelt wurde, um Informationslecks zu verhindern, die bei traditionellen E-Mail-Clients häufig vorkommen. Der [mail.i2p](https://mail.i2p/)-Dienst bietet Virenfilterung, [Hashcash](https://en.wikipedia.org/wiki/Hashcash)-Kontingente und Outproxy-Trennung für zusätzlichen Schutz.

---
