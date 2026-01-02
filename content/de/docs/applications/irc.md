---
title: "IRC über I2P"
description: "Vollständiger Leitfaden zu I2P IRC-Netzwerken, Clients, Tunneln und Server-Einrichtung (aktualisiert 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Überblick

**Wichtige Punkte**

- I2P bietet **Ende-zu-Ende-Verschlüsselung** für IRC-Verkehr durch seine Tunnel. **Deaktivieren Sie SSL/TLS** in IRC-Clients, es sei denn, Sie nutzen einen Outproxy zum Clearnet.
- Der vorkonfigurierte **Irc2P** Client-Tunnel lauscht standardmäßig auf **127.0.0.1:6668**. Verbinden Sie Ihren IRC-Client mit dieser Adresse und diesem Port.
- Verwenden Sie nicht den Begriff "router‑provided TLS". Nutzen Sie stattdessen "I2Ps native Verschlüsselung" oder "Ende-zu-Ende-Verschlüsselung".

## Schnellstart (Java I2P)

1. Öffne den **Hidden Services Manager** unter `http://127.0.0.1:7657/i2ptunnel/` und stelle sicher, dass der **Irc2P**-Tunnel **läuft**.
2. Stelle in deinem IRC-Client **Server** = `127.0.0.1`, **Port** = `6668`, **SSL/TLS** = **aus** ein.
3. Verbinde dich und tritt Kanälen wie `#i2p`, `#i2p-dev`, `#i2p-help` bei.

Für **i2pd**-Nutzer (C++ Router) erstellen Sie einen Client-Tunnel in `tunnels.conf` (siehe Beispiele unten).

## Netzwerke und Server

### IRC2P (main community network)

- Föderierte Server: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- Der **Irc2P**-Tunnel unter `127.0.0.1:6668` verbindet sich automatisch mit einem dieser Server.
- Typische Channels: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Server: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Hauptsprachen: Russisch und Englisch. Web-Frontends existieren auf einigen Hosts.

## Client setup

### Recommended, actively maintained

- **WeeChat (Terminal)** — starke SOCKS-Unterstützung; einfach zu skripten.
- **Pidgin (Desktop)** — wird weiterhin gepflegt; funktioniert gut unter Windows/Linux.
- **Thunderbird Chat (Desktop)** — unterstützt ab ESR 128+.
- **The Lounge (selbst gehostetes Web)** — moderner Web-Client.

### IRC2P (Haupt-Community-Netzwerk)

- **LimeChat** (kostenlos, Open Source).
- **Textual** (kostenpflichtig im App Store; Quellcode verfügbar zum Selbstbauen).

### Ilita-Netzwerk

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protokoll: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- Verschlüsselung: **aus**
- Benutzername/Nick: beliebig

#### Thunderbird Chat

- Kontotyp: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- SSL/TLS: **aus**
- Optional: Kanäle beim Verbinden automatisch betreten

#### Dispatch (SAM v3)

Beispiel für `config.toml`-Standardeinstellungen:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Irc2P Client-Tunnel: **127.0.0.1:6668** → Upstream-Server auf **Port 6667**.
- Hidden Services Manager: `http://127.0.0.1:7657/i2ptunnel/`.

### Empfohlen, aktiv gewartet

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Separater Tunnel für Ilita (Beispiel):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### macOS-Optionen

- **SAM aktivieren** in Java I2P (standardmäßig deaktiviert) unter `/configclients` oder `clients.config`.
- Standardwerte: **127.0.0.1:7656/TCP** und **127.0.0.1:7655/UDP**.
- Empfohlene Kryptografie: `SIGNATURE_TYPE=7` (Ed25519) und `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 mit ElGamal-Fallback) oder nur `4` für ausschließlich moderne Systeme.

### Beispielkonfigurationen

- Java I2P Standard: **2 eingehend / 2 ausgehend**.
- i2pd Standard: **5 eingehend / 5 ausgehend**.
- Für IRC: **2–3 jeweils** ist ausreichend; explizit setzen für konsistentes Verhalten über router hinweg.

## Client-Einrichtung

- **Aktivieren Sie SSL/TLS nicht** für interne I2P-IRC-Verbindungen. I2P bietet bereits Ende-zu-Ende-Verschlüsselung. Zusätzliches TLS erzeugt Overhead ohne Anonymitätsgewinn.
- Verwenden Sie **persistente Schlüssel** für eine stabile Identität; vermeiden Sie es, Schlüssel bei jedem Neustart neu zu generieren, außer zu Testzwecken.
- Wenn mehrere Anwendungen IRC nutzen, bevorzugen Sie **separate Tunnel** (nicht gemeinsam genutzt), um dienstübergreifende Korrelation zu reduzieren.
- Falls Sie Fernsteuerung (SAM/I2CP) zulassen müssen, binden Sie diese an localhost und sichern Sie den Zugriff mit SSH-Tunneln oder authentifizierten Reverse-Proxys.

## Alternative connection method: SOCKS5

Einige Clients können sich über I2P's SOCKS5-Proxy verbinden: **127.0.0.1:4447**. Für beste Ergebnisse sollte ein dedizierter IRC-Client-Tunnel auf Port 6668 bevorzugt werden; SOCKS kann Identifikatoren auf Anwendungsebene nicht bereinigen und könnte Informationen preisgeben, wenn der Client nicht für Anonymität ausgelegt ist.

## Troubleshooting

- **Keine Verbindung möglich** — stellen Sie sicher, dass der Irc2P-Tunnel läuft und der Router vollständig gebootstrappt ist.
- **Hängt bei Auflösung/Beitritt** — überprüfen Sie, dass SSL **deaktiviert** ist und der Client auf **127.0.0.1:6668** verweist.
- **Hohe Latenz** — I2P hat konstruktionsbedingt eine höhere Latenz. Halten Sie die Tunnel-Anzahl moderat (2–3) und vermeiden Sie schnelle Reconnect-Schleifen.
- **Verwendung von SAM-Apps** — bestätigen Sie, dass SAM aktiviert ist (Java) oder nicht durch eine Firewall blockiert wird (i2pd). Langlebige Sessions werden empfohlen.

## Appendix: Ports and naming

- Gängige IRC-Tunnel-Ports: **6668** (Irc2P-Standard), **6667** und **6669** als Alternativen.
- `.b32.i2p`-Hostnamen: 52-Zeichen-Standardform; erweiterte 56+-Zeichen-Formen existieren für LS2/erweiterte Zertifikate. Verwenden Sie `.i2p`-Hostnamen, es sei denn, Sie benötigen explizit b32-Adressen.
