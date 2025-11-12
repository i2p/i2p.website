---
title: "I2P herunterladen"
description: "Laden Sie die neueste Version von I2P für Windows, macOS, Linux, Android und mehr herunter"
type: "Downloads"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: ## Einführung in I2P

I2P ist ein anonymer Overlay-Netzwerkdienst, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet Schutz gegen Überwachung und Traffic-Analyse, indem es den Datenverkehr durch ein verteiltes Netzwerk von Routern leitet.

### Hauptmerkmale

- **Anonymität**: I2P verbirgt die IP-Adressen der Benutzer, indem es den Datenverkehr durch mehrere verschlüsselte Tunnel leitet.
- **Dezentralisierung**: Es gibt keinen zentralen Punkt des Scheiterns, da das Netzwerk auf einer Vielzahl von Routern basiert.
- **Verschlüsselung**: Alle Daten werden mit Garlic-Verschlüsselung geschützt, um die Privatsphäre der Benutzer zu gewährleisten.

### Installation

Um I2P zu installieren, laden Sie das Installationspaket von der [offiziellen I2P-Website](https://geti2p.net) herunter und folgen Sie den Anweisungen für Ihr Betriebssystem. Nach der Installation starten Sie den I2P-Router und konfigurieren Sie Ihre Anwendungen, um das Netzwerk zu nutzen.

### Konfiguration

Die Konfiguration von I2P erfolgt über die Webkonsole, die unter `http://127.0.0.1:7657` erreichbar ist. Hier können Sie Einstellungen für Tunnel, Bandbreite und andere Optionen anpassen.

### Nutzung

Sobald der I2P-Router läuft, können Sie Anwendungen wie Webbrowser, E-Mail-Clients und Instant Messaging-Programme so konfigurieren, dass sie das I2P-Netzwerk nutzen. Dies ermöglicht es Ihnen, anonym auf eepsites zuzugreifen und mit anderen Benutzern zu kommunizieren.

### Unterstützung und Community

Für Unterstützung und weitere Informationen besuchen Sie die [I2P Community-Seite](https://geti2p.net/en/about/community). Hier finden Sie Dokumentationen, Foren und andere Ressourcen, um Ihnen bei der Nutzung von I2P zu helfen.
windows: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymer Overlay-Netzwerkdienst, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet eine Plattform für anonyme Kommunikation, indem es den Datenverkehr durch ein Netzwerk von freiwilligen Knoten leitet, die als "Router" bezeichnet werden.

## Hauptmerkmale

- **Anonymität**: I2P bietet Schutz der Privatsphäre durch Verschleierung der IP-Adressen der Benutzer.
- **Dezentralisierung**: Es gibt keinen zentralen Punkt des Scheiterns, da das Netzwerk auf vielen unabhängigen Routern basiert.
- **Verschlüsselung**: Alle Daten werden mit Garlic-Verschlüsselung gesichert, um die Vertraulichkeit zu gewährleisten.

## Wie I2P funktioniert

I2P verwendet ein System von "Tunneln", um Datenpakete anonym zu senden und zu empfangen. Ein Tunnel ist eine unidirektionale Kommunikationsverbindung, die aus mehreren Routern besteht. Daten werden in Form von "Garlic"-Paketen gesendet, die mehrere Nachrichten enthalten können, um die Analyse zu erschweren.

### Aufbau eines Tunnels

1. **Erstellung eines LeaseSets**: Der Benutzer erstellt ein LeaseSet, das die Informationen über die Tunnel enthält, die für die Kommunikation verwendet werden.
2. **Veröffentlichung im netDb**: Das LeaseSet wird im netDb (Netzwerkdatenbank) veröffentlicht, damit andere Benutzer es finden können.
3. **Datenübertragung**: Daten werden durch die Tunnel gesendet, wobei jeder Router nur den vorherigen und den nächsten Knoten kennt.

## Sicherheit und Datenschutz

I2P verwendet fortschrittliche Verschlüsselungstechniken, um die Sicherheit und Anonymität der Benutzer zu gewährleisten. Die Verwendung von NTCP2 und SSU (Secure Semireliable UDP) Protokollen ermöglicht eine sichere und zuverlässige Datenübertragung.

## Anwendungen von I2P

I2P unterstützt eine Vielzahl von Anwendungen, darunter:

- **Eepsites**: Anonyme Websites, die innerhalb des I2P-Netzwerks gehostet werden.
- **I2PTunnel**: Ermöglicht die Erstellung von verschlüsselten Tunneln für verschiedene Dienste.
- **SAMv3**: Eine API, die Entwicklern den Zugriff auf I2P-Funktionen ermöglicht.

## Fazit

I2P ist ein leistungsfähiges Werkzeug für diejenigen, die Anonymität und Sicherheit im Internet suchen. Durch die Nutzung eines dezentralisierten Netzwerks und fortschrittlicher Verschlüsselungstechniken bietet es eine robuste Plattform für anonyme Kommunikation.
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "Java erforderlich"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymes Overlay-Netzwerk, das auf dem Internet aufbaut. Es bietet eine anonyme Kommunikationsschicht, die es Anwendungen ermöglicht, sicher und privat zu kommunizieren. I2P ist besonders nützlich für Benutzer, die ihre Privatsphäre schützen möchten, während sie im Internet surfen oder Daten austauschen.

## Hauptkomponenten

- **Router**: Der I2P-Router ist das Herzstück des Netzwerks. Er verwaltet die Kommunikation zwischen den verschiedenen Knoten und sorgt dafür, dass Daten anonym übertragen werden.
- **Tunnel**: Daten werden durch Tunnels geleitet, die aus einer Reihe von Routern bestehen. Diese Tunnels verschleiern die Quelle und das Ziel der Daten.
- **leaseSet**: Ein leaseSet ist eine Sammlung von Informationen, die benötigt werden, um einen Tunnel zu erreichen. Es enthält die Identität des Ziels und die Details der Tunnels, die verwendet werden können.
- **netDb**: Die netDb (Netzwerkdatenbank) speichert Informationen über die verschiedenen Knoten und Tunnels im I2P-Netzwerk.
- **floodfill**: Floodfill-Knoten sind spezielle Router, die zusätzliche Informationen im netDb speichern und verteilen, um die Effizienz des Netzwerks zu verbessern.

## Kommunikation

I2P verwendet verschiedene Protokolle, um die Anonymität und Sicherheit der Kommunikation zu gewährleisten:

- **NTCP2**: Ein Protokoll, das für die verschlüsselte Kommunikation zwischen Routern verwendet wird.
- **SSU**: Ein weiteres Protokoll, das für die sichere und anonyme Übertragung von Datenpaketen sorgt.

## Anwendungen

I2P unterstützt eine Vielzahl von Anwendungen, darunter:

- **eepsite**: Eine anonyme Website, die über das I2P-Netzwerk gehostet wird.
- **I2PTunnel**: Ermöglicht die Erstellung von Tunnels für verschiedene Arten von Datenverkehr, z.B. HTTP oder IRC.
- **SAMv3**: Ein API, das Entwicklern ermöglicht, Anwendungen zu erstellen, die mit dem I2P-Netzwerk interagieren.

## Sicherheit

I2P verwendet **garlic encryption** (Knoblauch-Verschlüsselung), um die Daten zu schützen. Diese Technik verschlüsselt mehrere Nachrichten zusammen, um die Analyse des Datenverkehrs zu erschweren.

## Weitere Informationen

Besuchen Sie die [offizielle I2P-Website](https://geti2p.net) für mehr Details und Anleitungen zur Installation und Nutzung des Netzwerks.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: # Einführung in I2P

I2P, das Invisible Internet Project, ist ein anonymes Overlay-Netzwerk, das auf dem Internet aufbaut. Es bietet eine anonyme Kommunikationsschicht, die es Anwendungen ermöglicht, Nachrichten anonym und sicher zu senden und zu empfangen. I2P ist besonders nützlich für Benutzer, die ihre Privatsphäre schützen und ihre Online-Aktivitäten vor Überwachung verbergen möchten.

## Hauptkomponenten

- **Router**: Der I2P-Router ist das Herzstück des Netzwerks. Er verwaltet die Kommunikation zwischen den Knoten und sorgt für die Anonymität der Datenübertragung.
- **Tunnel**: Tunnel sind virtuelle Pfade, die durch das Netzwerk führen und die Anonymität der Kommunikation gewährleisten. Jeder Tunnel besteht aus mehreren Knoten, die als Zwischenstationen fungieren.
- **LeaseSet**: Ein LeaseSet ist eine Struktur, die Informationen über einen Tunnel enthält, einschließlich der Knoten, die daran beteiligt sind.
- **NetDb**: Die netDb ist die verteilte Datenbank des I2P-Netzwerks, die Informationen über Router und LeaseSets speichert.

## Kommunikation

I2P verwendet eine Technik namens "Garlic Encryption", um Nachrichten zu verschlüsseln. Diese Methode ermöglicht es, mehrere Nachrichten in einer einzigen verschlüsselten Einheit zu bündeln, was die Sicherheit und Anonymität erhöht.

### Protokolle

I2P unterstützt verschiedene Protokolle zur Kommunikation, darunter NTCP2 und SSU. Diese Protokolle sind speziell für die Anforderungen des anonymen Netzwerks optimiert.

- **NTCP2**: Ein Protokoll für die verschlüsselte Kommunikation zwischen Routern.
- **SSU**: Ein weiteres Protokoll, das für die Übertragung von Datenpaketen über das Netzwerk verwendet wird.

## Anwendungen

I2P bietet eine Vielzahl von Anwendungen, die auf seiner Plattform laufen können. Dazu gehören:

- **Eepsites**: Anonyme Websites, die nur über das I2P-Netzwerk zugänglich sind.
- **I2PTunnel**: Ein Dienst, der es ermöglicht, TCP/IP-Datenverkehr anonym über das I2P-Netzwerk zu leiten.
- **SAMv3**: Eine API, die Entwicklern den Zugriff auf I2P-Dienste ermöglicht.

## Fazit

I2P ist ein leistungsstarkes Werkzeug für Benutzer, die ihre Privatsphäre im Internet schützen möchten. Durch die Nutzung von I2P können Benutzer sicher und anonym kommunizieren, ohne Angst vor Überwachung oder Zensur zu haben.
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "Kein Java erforderlich - enthält Java-Laufzeitumgebung"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: wahr
links: ```
## Einführung in I2P

I2P ist ein anonymer Overlay-Netzwerkdienst, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet eine Plattform für verschiedene Anwendungen, einschließlich Web-Browsing, E-Mail, Chat und Dateifreigabe. I2P ist so konzipiert, dass es im Hintergrund läuft und die Privatsphäre der Benutzer schützt, indem es ihre IP-Adressen verbirgt.

### Wie funktioniert I2P?

I2P verwendet ein System von Routern und Tunneln, um Datenpakete durch das Netzwerk zu leiten. Jeder Benutzer betreibt einen Router, der mit anderen Routern kommuniziert, um ein dynamisches und dezentrales Netzwerk zu bilden. Daten werden in "Knoblauch"-Paketen verschlüsselt, die mehrere Nachrichten enthalten, um die Anonymität zu erhöhen.

#### Schlüsselkomponenten

- **Router**: Der Knotenpunkt, der Datenpakete sendet und empfängt.
- **Tunnel**: Virtuelle Pfade, die Daten durch das Netzwerk leiten.
- **leaseSet**: Eine Sammlung von Informationen, die benötigt wird, um einen Tunnel zu erreichen.
- **netDb**: Die verteilte Datenbank, die Informationen über Router und Tunnels speichert.

### Vorteile von I2P

- **Anonymität**: Verbirgt die IP-Adresse des Benutzers und verschleiert den Datenverkehr.
- **Sicherheit**: Verwendet starke Verschlüsselung, um Daten vor Abhören zu schützen.
- **Dezentralisierung**: Kein zentraler Kontrollpunkt, was die Zensurresistenz erhöht.

Weitere Informationen finden Sie in der [offiziellen I2P-Dokumentation](https://geti2p.net/de/docs).
```
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: ### Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymer Overlay-Netzwerk-Layer, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet Schutz vor Überwachung und Traffic-Analyse durch die Nutzung von **garlic encryption** und anderen fortschrittlichen Techniken.

#### Hauptkomponenten

- **Router**: Der Router ist das Herzstück von I2P und leitet den Datenverkehr durch das Netzwerk.
- **Tunnel**: Tunnel sind virtuelle Pfade, die den Datenverkehr anonym durch das Netzwerk leiten.
- **leaseSet**: Ein leaseSet ist eine Sammlung von Informationen, die benötigt werden, um einen Dienst innerhalb von I2P zu erreichen.

#### Netzwerkprotokolle

I2P verwendet mehrere Protokolle, um die Kommunikation zu ermöglichen:

- **NTCP2**: Ein Protokoll für die verschlüsselte Kommunikation zwischen Routern.
- **SSU**: Ein Protokoll, das für die Kommunikation über UDP verwendet wird.

#### Anwendungen

I2P unterstützt eine Vielzahl von Anwendungen, darunter:

- **eepsite**: Eine anonyme Website, die über das I2P-Netzwerk gehostet wird.
- **I2PTunnel**: Ermöglicht die Erstellung von Tunneln für verschiedene Dienste wie HTTP und IRC.

Weitere Informationen finden Sie in der [offiziellen I2P-Dokumentation](https://geti2p.net).
file: "i2pinstall_2.10.0.jar"
size: "~30M"
requirements: "Java 8 oder höher"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymes Overlay-Netzwerk, das auf der bestehenden Internet-Infrastruktur aufbaut. Es bietet eine anonyme Kommunikationsschicht, die es Benutzern ermöglicht, sicher und privat zu kommunizieren. I2P ist besonders nützlich für diejenigen, die ihre Privatsphäre schützen möchten, sei es aus persönlichen, politischen oder geschäftlichen Gründen.

## Wie funktioniert I2P?

I2P verwendet eine Technik namens "garlic encryption", um Daten in mehreren Schichten zu verschlüsseln. Diese Schichten werden dann über ein Netzwerk von Routern geleitet, die als "Tunnels" bezeichnet werden. Jeder Tunnel besteht aus mehreren "hops", die die Daten weiterleiten, ohne die Quelle oder das Ziel zu kennen.

### Hauptkomponenten von I2P

- **Router**: Ein Knoten im I2P-Netzwerk, der Daten weiterleitet.
- **Tunnel**: Ein Pfad durch das Netzwerk, der aus mehreren Routern besteht.
- **leaseSet**: Eine Struktur, die Informationen über einen Tunnel enthält.
- **netDb**: Die verteilte Datenbank, die Informationen über alle aktiven Router und Tunnels speichert.

## Vorteile von I2P

1. **Anonymität**: Durch die Verwendung von Tunnels und garlic encryption bleibt die Identität der Benutzer verborgen.
2. **Dezentralisierung**: I2P ist ein vollständig dezentralisiertes Netzwerk ohne zentrale Kontrollinstanz.
3. **Flexibilität**: Unterstützt verschiedene Anwendungen und Protokolle, einschließlich Web-Browsing, E-Mail und Dateifreigabe.

Weitere Informationen finden Sie auf der [offiziellen I2P-Website](https://geti2p.net).
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: ## Einführung in I2P

I2P ist ein anonymer Overlay-Netzwerk, das es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet eine Plattform für anonyme Kommunikation über das Internet und schützt die Privatsphäre der Benutzer durch die Verwendung von Techniken wie garlic encryption.

### Hauptkomponenten

- **Router**: Der Router ist das Herzstück des I2P-Netzwerks und leitet Datenpakete zwischen den Knoten.
- **Tunnel**: Tunnel sind virtuelle Pfade, die Datenpakete durch das Netzwerk leiten, um die Anonymität zu gewährleisten.
- **leaseSet**: Ein leaseSet ist eine Sammlung von Informationen, die benötigt werden, um einen Tunnel zu einem bestimmten Ziel aufzubauen.

### Kommunikation

I2P verwendet verschiedene Protokolle, um die Kommunikation zu ermöglichen:

- **NTCP2**: Ein Protokoll für die verschlüsselte Kommunikation zwischen Routern.
- **SSU**: Ein weiteres Protokoll für die verschlüsselte Kommunikation, das hauptsächlich für die Verbindung über UDP verwendet wird.

### Anwendungen

I2P unterstützt eine Vielzahl von Anwendungen, darunter:

- **eepsites**: Anonyme Websites, die innerhalb des I2P-Netzwerks gehostet werden.
- **I2PTunnel**: Ermöglicht die Weiterleitung von TCP/IP-Datenverkehr durch das I2P-Netzwerk.

### Weitere Informationen

Besuchen Sie die [offizielle I2P-Website](https://geti2p.net) für weitere Informationen und Anleitungen zur Installation und Nutzung von I2P.
file: "i2psource_2.10.0.tar.bz2"
size: "~33M"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: ```markdown
## Einführung in I2P

I2P ist ein anonymer Overlay-Netzwerk-Dienst, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet eine Plattform für anonyme Webdienste, die als "eepsites" bekannt sind, sowie für andere Anwendungen wie E-Mail, IRC und Dateifreigabe.

### Wie funktioniert I2P?

I2P verwendet ein System von "Tunneln", um Datenpakete anonym durch das Netzwerk zu leiten. Jeder Benutzer betreibt einen "router", der Daten über ein Netzwerk von freiwilligen Knoten sendet und empfängt. Diese Knoten sind in der Lage, Daten zu verschlüsseln und zu entschlüsseln, um die Privatsphäre der Benutzer zu schützen.

#### Tunnel und Verschlüsselung

Daten werden in "Tunneln" gesendet, die aus einer Reihe von Routern bestehen. Jeder Tunnel ist unidirektional, was bedeutet, dass separate Tunnel für eingehende und ausgehende Daten verwendet werden. Die Daten werden mit "garlic encryption" verschlüsselt, um die Sicherheit zu erhöhen.

#### Verteilung der Netzwerkdatenbank

Die Netzwerkdatenbank, bekannt als "netDb", speichert Informationen über die Knoten im Netzwerk. Einige Knoten, die als "floodfill" bezeichnet werden, sind speziell dafür verantwortlich, diese Informationen zu speichern und zu verteilen. Dies ermöglicht es dem Netzwerk, effizient zu arbeiten und die Anonymität der Benutzer zu wahren.

### Vorteile von I2P

- **Anonymität**: I2P bietet starke Anonymität durch die Verwendung von Tunneln und Verschlüsselung.
- **Sicherheit**: Die Verschlüsselungstechniken von I2P schützen die Daten vor Abhören und Manipulation.
- **Flexibilität**: I2P unterstützt eine Vielzahl von Anwendungen und Protokollen, was es zu einer vielseitigen Plattform für anonyme Kommunikation macht.

### Erste Schritte mit I2P

Um mit I2P zu beginnen, laden Sie die Software von der [offiziellen I2P-Website](https://geti2p.net) herunter und installieren Sie sie. Nach der Installation können Sie Ihren Router konfigurieren und mit der Nutzung des Netzwerks beginnen. Weitere Informationen finden Sie in der [I2P-Dokumentation](https://geti2p.net/de/docs).

### Fazit

I2P ist ein leistungsstarkes Werkzeug für anonyme Kommunikation im Internet. Mit seinen robusten Sicherheits- und Anonymitätsfunktionen ist es eine ausgezeichnete Wahl für Benutzer, die ihre Privatsphäre schützen möchten.
```
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymer Overlay-Netzwerk, das entwickelt wurde, um die Privatsphäre und Sicherheit der Kommunikation im Internet zu verbessern. Es ermöglicht Benutzern, anonym zu surfen, zu chatten und Dateien zu teilen, indem es den Datenverkehr durch ein verteiltes Netzwerk von Routern leitet.

## Hauptkomponenten

- **Router**: Ein Router ist ein Knoten im I2P-Netzwerk, der Datenpakete weiterleitet.
- **Tunnel**: Tunnel sind virtuelle Pfade, die Daten durch das Netzwerk leiten. Jeder Tunnel besteht aus mehreren Routern.
- **LeaseSet**: Ein LeaseSet ist eine Sammlung von Informationen, die benötigt werden, um einen Tunnel zu erreichen.
- **NetDb**: Die netDb (Netzwerkdatenbank) speichert Informationen über Router und LeaseSets.

## Kommunikation

I2P verwendet **garlic encryption** (Knoblauchverschlüsselung), um die Daten in mehrere Schichten zu verpacken, ähnlich wie bei einer Zwiebel. Dies bietet eine zusätzliche Sicherheitsebene, da die Daten auf ihrem Weg durch das Netzwerk mehrfach verschlüsselt werden.

## Protokolle

I2P unterstützt mehrere Protokolle, darunter **NTCP2** und **SSU**, die für die sichere Übertragung von Datenpaketen zwischen Routern verwendet werden. Das **SAMv3**-Protokoll ermöglicht es Anwendungen, mit dem I2P-Netzwerk zu interagieren.

## Anwendungen

- **Eepsites**: Eepsites sind Websites, die innerhalb des I2P-Netzwerks gehostet werden und nur über I2P zugänglich sind.
- **I2PTunnel**: I2PTunnel ist ein Dienst, der es ermöglicht, TCP/IP-Datenverkehr durch das I2P-Netzwerk zu leiten.
- **I2CP**: Das I2CP (I2P Control Protocol) ist das Protokoll, das von Anwendungen verwendet wird, um mit einem I2P-Router zu kommunizieren.

I2P bietet eine robuste Plattform für anonyme Kommunikation und ist ein wertvolles Werkzeug für Benutzer, die ihre Privatsphäre im Internet schützen möchten.
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+, mindestens 512 MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymer Overlay-Netzwerk-Dienst, der es Anwendungen ermöglicht, anonym und sicher zu kommunizieren. Es bietet eine dezentrale, peer-to-peer Architektur, die auf Datenschutz und Sicherheit ausgelegt ist.

## Hauptkomponenten

- **Router**: Der Router ist das Herzstück des I2P-Netzwerks. Er leitet Nachrichten zwischen verschiedenen Peers weiter.
- **Tunnel**: Tunnel sind virtuelle Pfade, die durch das Netzwerk verlaufen und die Anonymität der Kommunikation gewährleisten.
- **leaseSet**: Ein leaseSet ist ein Datensatz, der Informationen über einen Tunnel enthält, einschließlich der Verschlüsselungsschlüssel.
- **netDb**: Die netDb ist eine verteilte Datenbank, die Informationen über Router und leaseSets speichert.
- **floodfill**: Floodfill-Router sind spezielle Router, die eine größere Rolle bei der Verbreitung von netDb-Informationen spielen.

## Kommunikation

I2P unterstützt verschiedene Protokolle und Schnittstellen, um die Integration in bestehende Anwendungen zu erleichtern:

- **NTCP2** und **SSU**: Diese Protokolle werden für die verschlüsselte Kommunikation zwischen Routern verwendet.
- **SAMv3**: Eine API, die es Anwendungen ermöglicht, über das I2P-Netzwerk zu kommunizieren.
- **I2PTunnel**: Ein Dienst, der es ermöglicht, TCP/IP-Datenverkehr durch das I2P-Netzwerk zu leiten.

## Sicherheit

I2P verwendet **garlic encryption** (Knoblauch-Verschlüsselung), um Nachrichten in mehrere Schichten zu verpacken, was die Anonymität und Sicherheit der Kommunikation erhöht. Dies macht es schwierig für Angreifer, den Ursprung oder das Ziel einer Nachricht zu bestimmen.

## Nutzung

Um I2P zu nutzen, müssen Benutzer einen I2P-Router auf ihrem Gerät installieren. Dieser Router verbindet sich mit anderen Peers im Netzwerk und ermöglicht den Zugriff auf **eepsites** (anonyme Webseiten, die nur über I2P zugänglich sind).

Weitere Informationen finden Sie in der [offiziellen I2P-Dokumentation](https://geti2p.net).
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: # Einführung in I2P

I2P (The Invisible Internet Project) ist ein anonymes Netzwerk, das darauf abzielt, die Privatsphäre und Sicherheit der Kommunikation im Internet zu verbessern. Es ermöglicht Benutzern, anonym zu surfen, Nachrichten zu senden und Dienste zu hosten, die als "eepsites" bekannt sind.

## Hauptkomponenten

- **Router**: Der Router ist das Herzstück von I2P und verwaltet die Kommunikation zwischen den Knoten im Netzwerk.
- **Tunnel**: Tunnel sind verschlüsselte Kommunikationspfade, die von Routern verwendet werden, um Daten anonym zu übertragen.
- **leaseSet**: Ein leaseSet ist eine Sammlung von Informationen, die benötigt werden, um einen Tunnel zu einem bestimmten Ziel zu erreichen.
- **netDb**: Die netDb ist die verteilte Datenbank, die Informationen über alle aktiven Router und leaseSets im Netzwerk speichert.

## Kommunikation

I2P verwendet verschiedene Protokolle, um die Anonymität und Sicherheit der Datenübertragung zu gewährleisten:

- **NTCP2**: Ein Protokoll, das für die verschlüsselte Kommunikation zwischen Routern verwendet wird.
- **SSU**: Ein weiteres Protokoll, das für die verschlüsselte Kommunikation über UDP verwendet wird.

## Anwendungen

I2P bietet eine Vielzahl von Anwendungen, die die Anonymität und Sicherheit der Benutzer verbessern:

- **I2PTunnel**: Ein Tool, das es Benutzern ermöglicht, TCP/IP-Daten anonym über I2P zu senden.
- **SAMv3**: Eine API, die Entwicklern den Zugriff auf I2P-Funktionen ermöglicht.
- **I2CP**: Ein Protokoll, das die Kommunikation zwischen Anwendungen und dem I2P-Router ermöglicht.
- **I2NP**: Das Netzwerkprotokoll, das die Datenübertragung innerhalb von I2P regelt.

## Sicherheit

I2P verwendet **garlic encryption** (Knoblauch-Verschlüsselung), um die Daten in mehrere Schichten zu verpacken, was die Rückverfolgung erschwert. Dies bietet eine zusätzliche Sicherheitsebene für die Benutzer.

Weitere Informationen finden Sie auf der [offiziellen I2P-Website](https://geti2p.net).
primary: ## Einführung in I2P

Das Invisible Internet Project (I2P) ist ein anonymes Netzwerk, das darauf abzielt, die Privatsphäre und Sicherheit der Benutzer im Internet zu schützen. Es ermöglicht die anonyme Kommunikation und den Zugriff auf Inhalte, ohne dass die Identität der Benutzer offengelegt wird.

### Hauptkomponenten

- **Router**: Der I2P-Router ist die zentrale Komponente, die den Datenverkehr innerhalb des Netzwerks weiterleitet.
- **Tunnel**: Tunnel sind verschlüsselte Pfade, die den Datenverkehr durch das I2P-Netzwerk leiten.
- **LeaseSet**: Ein LeaseSet ist eine Struktur, die Informationen über die Tunnel eines Dienstes enthält.
- **NetDb**: Die netDb (Netzwerkdatenbank) speichert Informationen über verfügbare Router und Tunnel im Netzwerk.

### Kommunikation

I2P verwendet **garlic encryption** (Knoblauchverschlüsselung), um die Daten in mehrere Schichten zu verpacken, was die Anonymität und Sicherheit erhöht. Die Kommunikation erfolgt über verschiedene Protokolle wie **NTCP2** und **SSU**, die für die sichere Übertragung von Daten optimiert sind.

### Dienste

- **Eepsites**: Dies sind anonyme Websites, die im I2P-Netzwerk gehostet werden und über spezielle .i2p-Domänen zugänglich sind.
- **I2PTunnel**: Ein Dienst, der es ermöglicht, traditionelle Internetdienste über das I2P-Netzwerk zu nutzen.
- **SAMv3**: Ein API, das Entwicklern den Zugriff auf I2P-Funktionen ermöglicht.
- **I2CP**: Das I2P Control Protocol, das die Kommunikation zwischen Anwendungen und dem I2P-Router ermöglicht.

### Sicherheit

I2P bietet robuste Sicherheitsfunktionen, um die Privatsphäre der Benutzer zu schützen. Durch die Verwendung von **garlic encryption** und dynamischen Tunneln wird sichergestellt, dass der Datenverkehr schwer zu verfolgen ist.
name: "StormyCloud"
location: "Vereinigte Staaten"
url: "https://stormycloud.org"
resources: Um die Privatsphäre und Anonymität im Internet zu gewährleisten, nutzt I2P eine Kombination aus fortschrittlichen Techniken wie garlic encryption und verteilten Netzwerken. Benutzer können ihre Daten durch verschlüsselte Tunnel senden, die als "tunnels" bezeichnet werden, um sicherzustellen, dass ihre Kommunikation nicht zurückverfolgt werden kann. 

I2P-Router kommunizieren miteinander über das netDb (Netzwerkdatenbank), das Informationen über verfügbare Knoten und deren Status speichert. Floodfill-Knoten helfen bei der Verbreitung dieser Informationen im Netzwerk. 

Für die Verbindung mit dem I2P-Netzwerk stehen zwei Hauptprotokolle zur Verfügung: NTCP2 und SSU. Diese Protokolle ermöglichen es Routern, sich sicher zu verbinden und Daten auszutauschen. 

Benutzer können auch ihre eigenen eepsites (anonyme Websites) hosten, die über das I2P-Netzwerk zugänglich sind. Diese Seiten bieten eine zusätzliche Ebene der Anonymität, da sie nicht direkt über das herkömmliche Internet zugänglich sind. 

Um mit dem I2P-Netzwerk zu interagieren, können Entwickler das SAMv3 (Simple Anonymous Messaging) API verwenden, das eine einfache Schnittstelle für die Erstellung von Anwendungen bietet, die mit I2P kommunizieren. 

I2PTunnel ist ein weiteres wichtiges Werkzeug, das es Benutzern ermöglicht, verschiedene Dienste über das I2P-Netzwerk zu leiten, indem es als Proxy fungiert. 

Insgesamt bietet I2P eine robuste Plattform für anonyme Kommunikation und den Schutz der Privatsphäre im digitalen Zeitalter.
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
