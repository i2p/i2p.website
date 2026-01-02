---
title: "Leitfaden zur Fehlerbehebung für den I2P Router"
description: "Umfassender Leitfaden zur Fehlerbehebung bei häufigen Problemen mit dem I2P router, einschließlich Konnektivitäts-, Leistungs- und Konfigurationsproblemen"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P router fallen am häufigsten aus aufgrund von **Problemen mit der Portweiterleitung**, **unzureichender Bandbreitenzuweisung** und **ungenügender Bootstrap-Zeit**. Diese drei Faktoren machen über 70 % der gemeldeten Probleme aus. Der router benötigt nach dem Start mindestens **10-15 Minuten**, um sich vollständig ins Netzwerk zu integrieren, **mindestens 128 KB/s Bandbreite** (256 KB/s empfohlen) und eine korrekte **UDP/TCP-Portweiterleitung**, um einen nicht durch eine Firewall blockierten Status zu erreichen. Neue Nutzer erwarten häufig sofortige Konnektivität und starten zu früh neu, was den Integrationsfortschritt zurücksetzt und einen frustrierenden Kreislauf erzeugt. Dieser Leitfaden bietet detaillierte Lösungen für alle wesentlichen I2P-Probleme, die die Versionen 2.10.0 und höher betreffen.

Die Anonymitätsarchitektur von I2P tauscht inhärent Geschwindigkeit gegen Privatsphäre ein, indem sie mehrstufig verschlüsselte tunnels nutzt. Das Verständnis dieses grundlegenden Designs hilft Nutzern, realistische Erwartungen zu setzen und Probleme effektiv zu beheben, statt normales Verhalten fälschlicherweise als Probleme zu interpretieren.

## Router startet nicht oder stürzt sofort ab

Die häufigsten Startfehler entstehen durch **Portkonflikte**, **Inkompatibilität der Java-Version** oder **beschädigte Konfigurationsdateien**. Überprüfen Sie, ob bereits eine andere I2P-Instanz läuft, bevor Sie tiefergehende Probleme untersuchen.

**Prüfen Sie, ob keine in Konflikt stehenden Prozesse vorhanden sind:**

Linux: `ps aux | grep i2p` oder `netstat -tulpn | grep 7657`

Windows: Task-Manager → Details → nach java.exe mit i2p in der Befehlszeile suchen

macOS: Aktivitätsanzeige → nach "i2p" suchen

Falls ein Zombie-Prozess existiert, beenden Sie ihn: `pkill -9 -f i2p` (Linux/Mac) oder `taskkill /F /IM javaw.exe` (Windows)

**Java-Versionskompatibilität prüfen:**

I2P 2.10.0+ erfordert **mindestens Java 8**, empfohlen wird Java 11 oder neuer. Überprüfen Sie, dass Ihre Installation "mixed mode" (nicht "interpreted mode") anzeigt:

```bash
java -version
```
Sollte anzeigen: OpenJDK oder Oracle Java, Version 8+, "mixed mode" (gemischter Modus)

**Vermeiden:** GNU GCJ, veraltete Java-Implementierungen, ausschließlich interpretierte Modi

**Häufige Portkonflikte** treten auf, wenn mehrere Dienste um die Standard-Ports von I2P konkurrieren. Die router‑Konsole (7657), I2CP (7654), SAM (7656) und der HTTP‑Proxy (4444) müssen verfügbar sein. Prüfen Sie auf Konflikte: `netstat -ano | findstr "7657 4444 7654"` (Windows) oder `lsof -i :7657,4444,7654` (Linux/Mac).

**Beschädigung der Konfigurationsdatei** äußert sich durch sofortige Abstürze mit Parser-Fehlern in den Protokollen. Router.config erfordert **UTF-8-Codierung ohne BOM (Byte Order Mark)**, verwendet `=` als Trennzeichen (nicht `:`) und verbietet bestimmte Sonderzeichen. Sichern Sie die Datei und prüfen Sie sie anschließend: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Um die Konfiguration zurückzusetzen und die Identität beizubehalten: I2P stoppen, router.keys und das Verzeichnis keyData sichern, router.config löschen, neu starten. Der router erzeugt die Standardkonfiguration neu.

**Java-Heap-Zuweisung zu gering** führt zu Abstürzen durch OutOfMemoryError (Speichermangel-Fehler). Bearbeiten Sie wrapper.config und erhöhen Sie `wrapper.java.maxmemory` von den Standardwerten 128 oder 256 auf **mindestens 512** (1024 für routers mit hoher Bandbreite). Dazu ist ein vollständiges Herunterfahren, 11 Minuten warten und anschließend ein Neustart erforderlich - ein Klick auf "Restart" in der Konsole wendet die Änderung nicht an.

## Behebung des Status "Network: Firewalled"

Der Firewalled-Status bedeutet, dass der router keine direkten eingehenden Verbindungen empfangen kann und daher auf introducers (Vermittlerknoten für eingehende Verbindungen) angewiesen ist. Obwohl der router in diesem Zustand funktioniert, **verschlechtert sich die Leistung erheblich**, und der Beitrag zum Netzwerk bleibt minimal. Um den Non-Firewalled-Status zu erreichen, ist eine korrekt konfigurierte Portweiterleitung erforderlich.

**Der router wählt zufällig einen Port** zwischen 9000 und 31000 für die Kommunikation. Finden Sie Ihren Port unter http://127.0.0.1:7657/confignet - suchen Sie nach "UDP Port" und "TCP Port" (in der Regel dieselbe Nummer). Sie müssen **sowohl UDP als auch TCP** weiterleiten, um eine optimale Leistung zu erreichen, obwohl UDP allein grundlegende Funktionalität ermöglicht.

**Automatische UPnP-Portweiterleitung aktivieren** (einfachste Methode):

1. Rufen Sie http://127.0.0.1:7657/confignet auf
2. Aktivieren Sie "Enable UPnP"
3. Speichern Sie die Änderungen und starten Sie den router neu
4. Warten Sie 5-10 Minuten und prüfen Sie, ob sich der Status von "Network: Firewalled" zu "Network: OK" ändert

UPnP erfordert Router-Unterstützung (standardmäßig auf den meisten Consumer-Routern aktiviert, die nach 2010 hergestellt wurden) und eine ordnungsgemäße Netzwerkkonfiguration.

**Manuelle Portweiterleitung** (erforderlich, wenn UPnP fehlschlägt):

1. Notieren Sie Ihren I2P-Port unter http://127.0.0.1:7657/confignet (z. B. 22648)
2. Ermitteln Sie Ihre lokale IP-Adresse: `ipconfig` (Windows), `ip addr` (Linux), Systemeinstellungen → Netzwerk (macOS)
3. Rufen Sie die Admin-Oberfläche Ihres Routers auf (typischerweise 192.168.1.1 oder 192.168.0.1)
4. Navigieren Sie zu Portweiterleitung (möglicherweise unter Erweitert, NAT oder Virtuelle Server)
5. Erstellen Sie zwei Regeln:
   - Externer Port: [Ihr I2P-Port] → Interne IP: [Ihr Computer] → Interner Port: [derselbe] → Protokoll: **UDP**
   - Externer Port: [Ihr I2P-Port] → Interne IP: [Ihr Computer] → Interner Port: [derselbe] → Protokoll: **TCP**
6. Speichern Sie die Konfiguration und starten Sie Ihren Router bei Bedarf neu

**Überprüfen Sie die Portweiterleitung** nach der Einrichtung mit Online-Prüftools. Wenn die Erkennung fehlschlägt, prüfen Sie die Firewall-Einstellungen - sowohl die Systemfirewall als auch die Firewall der Antivirensoftware müssen den I2P‑Port zulassen.

**Alternative für Hidden mode (verborgener Modus)** für restriktive Netzwerke, in denen Portweiterleitung unmöglich ist: Aktivieren unter http://127.0.0.1:7657/confignet → "Hidden mode" ankreuzen. Der router bleibt hinter einer Firewall, optimiert jedoch für diesen Zustand, indem er ausschließlich SSU introducers verwendet. Die Performance wird langsamer sein, bleibt aber funktionsfähig.

## Router steckt im Status "Starting" oder "Testing" fest

Diese vorübergehenden Zustände während des initialen Bootstraps lösen sich typischerweise innerhalb von **10-15 Minuten bei Neuinstallationen** oder **3-5 Minuten bei etablierten routers**. Vorzeitiges Eingreifen verschlimmert Probleme oft.

**"Network: Testing"** zeigt an, dass der router die Erreichbarkeit über verschiedene Verbindungstypen prüft (direkt, introducers (Vermittlerknoten), mehrere Protokollversionen). Das ist **in den ersten 5-10 Minuten normal** nach dem Start. Der router testet mehrere Szenarien, um die optimale Konfiguration zu ermitteln.

**"Rejecting tunnels: starting up"** erscheint während der Bootstrap-Phase, wenn der router noch nicht über ausreichende Peer-Informationen verfügt. Der router beteiligt sich nicht am Weiterleitungsverkehr, bis er ausreichend integriert ist. Diese Meldung sollte nach 10–20 Minuten verschwinden, sobald die netDb mit 50+ routers gefüllt ist.

**Uhrzeitabweichung macht Erreichbarkeitstests zunichte.** I2P erfordert, dass die Systemzeit höchstens **±60 Sekunden** von der Netzwerkzeit abweicht. Eine Abweichung von mehr als 90 Sekunden führt zur automatischen Ablehnung von Verbindungen. Synchronisieren Sie Ihre Systemuhr:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Systemsteuerung → Datum und Uhrzeit → Internetzeit → Jetzt aktualisieren → Automatische Synchronisierung aktivieren

macOS: Systemeinstellungen → Datum & Uhrzeit → "Datum und Uhrzeit automatisch einstellen" aktivieren

Nach der Korrektur der Uhrzeitabweichung starten Sie I2P vollständig neu, um eine ordnungsgemäße Integration sicherzustellen.

**Unzureichende Bandbreitenzuweisung** verhindert erfolgreiche Tests. Der router benötigt ausreichende Kapazität zum Aufbau von Test tunnels. Konfigurieren Sie dies unter http://127.0.0.1:7657/config:

- **Minimal funktionsfähig:** Eingehend 96 KB/sec, Ausgehend 64 KB/sec
- **Empfohlener Standard:** Eingehend 256 KB/sec, Ausgehend 128 KB/sec  
- **Optimale Leistung:** Eingehend 512+ KB/sec, Ausgehend 256+ KB/sec
- **Freigabe-Prozentsatz:** 80% (ermöglicht dem router, dem Netzwerk Bandbreite beizutragen)

Eine geringere Bandbreite kann funktionieren, verlängert jedoch die Integrationszeit von Minuten auf Stunden.

**Beschädigte netDb** infolge unsachgemäßen Herunterfahrens oder aufgrund von Festplattenfehlern verursacht endlose Testschleifen. Der router kann die Tests ohne gültige Peer-Daten nicht abschließen:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Löschen Sie den Inhalt von `%APPDATA%\I2P\netDb\` oder `%LOCALAPPDATA%\I2P\netDb\`

**Firewall blockiert reseed (Erstverteilung von Peer-Informationen)** verhindert das Auffinden erster Gegenstellen. Während der Initialisierungsphase lädt I2P router-Informationen von HTTPS-Reseed-Servern. Unternehmens- oder ISP-Firewalls können diese Verbindungen blockieren. Konfigurieren Sie den reseed-Proxy unter http://127.0.0.1:7657/configreseed, wenn Sie hinter restriktiven Netzwerken arbeiten.

## Langsame Geschwindigkeiten, Timeouts und Fehler beim tunnel-Aufbau

Das Design von I2P führt aufgrund von Multi-Hop-Verschlüsselung, Paket-Overhead und der Unvorhersehbarkeit der Routen inhärent zu **3-10x geringeren Geschwindigkeiten als im Clearnet**. Beim Aufbau eines tunnel werden mehrere routers durchlaufen, wobei jeder zusätzliche Latenz verursacht. Dieses Verständnis verhindert, normales Verhalten fälschlicherweise als Probleme zu missdeuten.

**Typische Leistungserwartungen:**

- Surfen auf .i2p-Sites: Anfangs 10–30 Sekunden pro Seitenaufruf, schneller nach dem tunnel-Aufbau
- Torrenting über I2PSnark: 10–100 KB/s pro Torrent, abhängig von Seedern und Netzbedingungen  
- Große Dateidownloads: Geduld nötig – Megabyte-Dateien können Minuten dauern, Gigabyte Stunden
- Erste Verbindung am langsamsten: Der tunnel-Aufbau dauert 30–90 Sekunden; nachfolgende Verbindungen nutzen bestehende tunnels

**Erfolgsrate des Tunnelaufbaus** ist ein Indikator für die Gesundheit des Netzwerks. Prüfen Sie unter http://127.0.0.1:7657/tunnels:

- **Über 60 %:** Normaler, stabiler Betrieb
- **40-60 %:** Grenzwertig, erwägen Sie eine Erhöhung der Bandbreite oder eine Reduzierung der Last
- **Unter 40 %:** Problematisch - weist auf unzureichende Bandbreite, Netzwerkprobleme oder eine schlechte Peerauswahl hin

**Erhöhen Sie die Bandbreitenzuweisung** als erste Optimierung. Die meisten Geschwindigkeitsprobleme entstehen durch Bandbreitenmangel. Erhöhen Sie die Limits schrittweise unter http://127.0.0.1:7657/config und überwachen Sie die Diagramme unter http://127.0.0.1:7657/graphs.

**Für DSL/Kabel (1-10 Mbps Verbindungen):** - Eingehend: 400 KB/sec - Ausgehend: 200 KB/sec - Freigabe: 80% - Speicher: 384 MB (edit wrapper.config)

**Für schnelle (10-100+ Mbit/s) Verbindungen:** - Eingehend: 1500 KB/s   - Ausgehend: 1000 KB/s - Anteil: 80-100% - Speicher: 512-1024 MB - Erwägen: Teilnehmende tunnels auf 2000-5000 erhöhen unter http://127.0.0.1:7657/configadvanced

**Optimieren Sie die tunnel-Konfiguration** für bessere Leistung. Greifen Sie unter http://127.0.0.1:7657/i2ptunnel auf die spezifischen tunnel-Einstellungen zu und bearbeiten Sie jeden tunnel:

- **Tunnel-Anzahl:** Erhöhen von 2 auf 3-4 (mehr Pfade verfügbar)
- **Backup-Anzahl:** Auf 1-2 setzen (schnelles Failover, falls ein Tunnel ausfällt)
- **Tunnel-Länge:** Standardmäßig bieten 3 Sprünge ein gutes Gleichgewicht; eine Reduzierung auf 2 verbessert die Geschwindigkeit, verringert aber die Anonymität

**Native Kryptobibliothek (jbigi)** bietet 5-10x bessere Leistung als reine Java-Verschlüsselung. Überprüfen Sie unter http://127.0.0.1:7657/logs, ob sie geladen ist - achten Sie auf "jbigi loaded successfully" oder "Using native CPUID implementation". Falls nicht vorhanden:

Linux: Normalerweise automatisch erkannt und aus ~/.i2p/jbigi-*.so geladen Windows: Prüfen Sie, ob sich jbigi.dll im I2P-Installationsverzeichnis befindet Falls nicht vorhanden: Build-Tools installieren und aus dem Quellcode kompilieren oder vorkompilierte Binärdateien aus offiziellen Repositories herunterladen

**Den router durchgehend in Betrieb halten.** Jeder Neustart setzt die Einbindung zurück und erfordert 30–60 Minuten, um das tunnel-Netzwerk und die Peer-Beziehungen wieder aufzubauen. Stabile router mit hoher Uptime werden bei der Auswahl für den tunnel-Aufbau bevorzugt, was die Leistung durch positive Rückkopplung verbessert.

## Hohe CPU- und Speicherauslastung

Übermäßige Ressourcennutzung weist typischerweise auf **unzureichende Speicherzuweisung**, **fehlende native Kryptobibliotheken** oder **zu starke Beteiligung am Netzwerk** hin. Gut konfigurierte routers sollten während aktiver Nutzung 10-30% CPU verbrauchen und eine stabile Speicherauslastung unter 80% des zugewiesenen Heaps beibehalten.

**Speicherprobleme äußern sich wie folgt:** - Speicherdiagramme mit flachem Plateau (dauerhaft am Maximum) - Häufige Garbage Collection (Speicherbereinigung; Sägezahnmuster mit starken Einbrüchen) - OutOfMemoryError in den Logs - Router reagiert unter Last nicht mehr - Automatisches Herunterfahren aufgrund von Ressourcenerschöpfung

**Java-Heap-Zuweisung erhöhen** in wrapper.config (erfordert vollständiges Herunterfahren):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Kritisch:** Nach dem Bearbeiten von wrapper.config müssen Sie **vollständig herunterfahren** (nicht neu starten), 11 Minuten auf ein ordnungsgemäßes Beenden warten und anschließend wieder starten. Die Schaltfläche "Restart" in der Router-Konsole lädt die Wrapper-Einstellungen nicht neu.

**CPU-Optimierung erfordert eine native Kryptografie-Bibliothek.** Reine Java-BigInteger-Operationen verbrauchen 10-20x mehr CPU als native Implementierungen. Überprüfen Sie den jbigi-Status beim Start unter http://127.0.0.1:7657/logs. Ohne jbigi schnellt die CPU-Auslastung während des tunnel-Aufbaus und bei Verschlüsselungsvorgängen auf 50-100 % hoch.

**Last durch teilnehmende tunnel reduzieren** wenn der router überlastet ist:

1. Öffne http://127.0.0.1:7657/configadvanced
2. Setze `router.maxParticipatingTunnels=1000` (Standardwert 8000)
3. Verringere den Freigabeanteil auf http://127.0.0.1:7657/config von 80 % auf 50 %
4. Deaktiviere den floodfill-Modus, falls aktiviert: `router.floodfillParticipant=false`

**Begrenzen Sie die I2PSnark-Bandbreite und die Anzahl gleichzeitiger Torrents.** Die Nutzung von Torrents beansprucht erhebliche Ressourcen. Unter http://127.0.0.1:7657/i2psnark:

- Aktive Torrents auf maximal 3-5 begrenzen
- "Up BW Limit" und "Down BW Limit" auf angemessene Werte setzen (jeweils 50-100 KB/sec)
- Torrents stoppen, wenn sie nicht aktiv benötigt werden
- Das gleichzeitige Seeden von Dutzenden Torrents vermeiden

**Überwachen Sie die Ressourcennutzung** über die integrierten Diagramme unter http://127.0.0.1:7657/graphs. Der Arbeitsspeicher sollte Luft nach oben haben, kein Plateau. CPU-Spitzen während des tunnel-Aufbaus sind normal; anhaltend hohe CPU-Auslastung weist auf Konfigurationsprobleme hin.

**Für Systeme mit stark eingeschränkten Ressourcen** (Raspberry Pi, alte Hardware) ziehen Sie **i2pd** (C++-Implementierung) als Alternative in Betracht. i2pd benötigt ~130 MB RAM gegenüber 350+ MB bei Java I2P und nutzt ~7 % CPU gegenüber 70 % unter ähnlicher Last. Beachten Sie, dass i2pd keine integrierten Anwendungen besitzt und externe Tools erfordert.

## I2PSnark-Torrent-Probleme

Die Integration von I2PSnark in die I2P router-Architektur setzt das Verständnis voraus, dass **Torrent-Aktivitäten vollständig von der Gesundheit der router tunnel abhängen**. Torrents starten erst, wenn der router eine ausreichende Integration mit 10+ aktiven Peers und funktionierenden tunnels erreicht hat.

**Wenn Torrents bei 0 % feststecken, deutet das typischerweise auf Folgendes hin:**

1. **Router nicht vollständig integriert:** Warten Sie 10–15 Minuten nach dem Start von I2P, bevor Sie Torrent-Aktivität erwarten
2. **DHT deaktiviert:** Aktivieren Sie es unter http://127.0.0.1:7657/i2psnark → Konfiguration → "Enable DHT" aktivieren (standardmäßig seit Version 0.9.2 aktiviert)
3. **Ungültige oder tote Tracker:** I2P-Torrents erfordern I2P-spezifische Tracker - Clearnet-Tracker funktionieren nicht
4. **Unzureichende tunnel-Konfiguration:** Erhöhen Sie die Anzahl der tunnels in I2PSnark → Konfiguration → Abschnitt Tunnels

**I2PSnark tunnels für bessere Leistung konfigurieren:**

- Eingehende Tunnel: 3-5 (Standard: 2 für Java I2P, 5 für i2pd)
- Ausgehende Tunnel: 3-5  
- Tunnel-Länge: 3 Sprünge (für mehr Geschwindigkeit auf 2 reduzieren, weniger Anonymität)
- Tunnel-Anzahl: 3 (sorgt für konstante Leistung)

**Unverzichtbare I2P-Torrent-Tracker** zum Hinzufügen: - tracker2.postman.i2p (primär, am zuverlässigsten) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Entfernen Sie alle clearnet (offenes Internet; non-.i2p) Tracker - sie bieten keinen Mehrwert und erzeugen Verbindungsversuche, die in einem Timeout enden.

**"Torrent not registered"-Fehler** treten auf, wenn die Kommunikation mit dem Tracker fehlschlägt. Right-click torrent → "Start" erzwingt ein erneutes Anmelden beim Tracker. Wenn das Problem weiterhin besteht, prüfen Sie die Erreichbarkeit des Trackers, indem Sie in einem I2P-konfigurierten Browser http://tracker2.postman.i2p aufrufen. Ausgefallene Tracker sollten durch funktionierende Alternativen ersetzt werden.

**Keine Peers verbinden sich** trotz Erfolg beim Tracker deutet auf Folgendes hin: - Router durch Firewall blockiert (bessert sich mit Portweiterleitung, aber nicht erforderlich) - Unzureichende Bandbreite (auf 256+ KB/s erhöhen)   - Swarm zu klein (manche Torrents haben 1-2 Seeder; Geduld erforderlich) - DHT deaktiviert (für Peer-Erkennung ohne Tracker aktivieren)

**Aktivieren Sie DHT und PEX (Peer Exchange – Peeraustausch)** in der I2PSnark-Konfiguration. DHT ermöglicht die Peer-Suche ohne Abhängigkeit von einem Tracker. PEX entdeckt Peers über verbundene Peers und beschleunigt dadurch die Schwarm-Erkennung.

**Beschädigung heruntergeladener Dateien** tritt aufgrund der integrierten Integritätsprüfung von I2PSnark nur selten auf. Wenn erkannt:

1. Rechtsklick auf den Torrent → "Check" erzwingt das Neu-Berechnen der Hashes aller Pieces (Teilstücke)
2. Beschädigte Torrent-Daten löschen (die .torrent-Datei bleibt erhalten)  
3. Rechtsklick → "Start", um mit Piece-Verifizierung erneut herunterzuladen
4. Festplatte auf Fehler prüfen, falls die Beschädigung weiterhin besteht: `chkdsk` (Windows), `fsck` (Linux)

**Überwachtes Verzeichnis funktioniert nicht** erfordert eine korrekte Konfiguration:

1. I2PSnark-Konfiguration → "Watch directory" (Überwachungsordner): Absoluten Pfad festlegen (z. B. `/home/user/torrents/watch`)
2. Stellen Sie sicher, dass der I2P-Prozess Leseberechtigungen hat: `chmod 755 /path/to/watch`
3. .torrent-Dateien im Überwachungsordner ablegen - I2PSnark fügt sie automatisch hinzu
4. "Auto start" konfigurieren: Prüfen, ob Torrents unmittelbar nach dem Hinzufügen gestartet werden sollen

**Leistungsoptimierung beim Torrenting:**

- Gleichzeitig aktive Torrents begrenzen: Maximal 3–5 bei Standardverbindungen
- Wichtige Downloads priorisieren: Torrents mit niedriger Priorität vorübergehend anhalten
- Dem router mehr Bandbreite zuweisen: Mehr Bandbreite = bessere Torrent-Leistung
- Geduld haben: Torrenting über I2P ist von Natur aus langsamer als BitTorrent im Clearnet
- Nach dem Herunterladen seeden: Das Netzwerk gedeiht durch Reziprozität

## Konfiguration und Fehlerbehebung für Git über I2P

Git-Operationen über I2P erfordern entweder eine **SOCKS-Proxy-Konfiguration** oder **dedizierte I2P tunnels** für den SSH/HTTP-Zugriff. Das Design von Git geht von Verbindungen mit niedriger Latenz aus, was die Architektur von I2P mit hoher Latenz zu einer Herausforderung macht.

**Git so konfigurieren, dass es einen I2P-SOCKS-Proxy verwendet:**

Bearbeiten Sie ~/.ssh/config (falls nicht vorhanden, erstellen):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Dies leitet alle SSH-Verbindungen zu .i2p-Hosts über den SOCKS-Proxy von I2P (Port 4447). Die ServerAlive-Einstellungen halten die Verbindung während der I2P-Latenz aufrecht.

Konfigurieren Sie Git global für HTTP/HTTPS-Git-Operationen:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Hinweis: `socks5h` führt die DNS-Auflösung über den Proxy durch - entscheidend für .i2p-Domains.

**Dedizierten I2P tunnel für Git-SSH erstellen** (zuverlässiger als SOCKS):

1. Öffne http://127.0.0.1:7657/i2ptunnel
2. "Neuer Client tunnel" → "Standard"
3. Konfigurieren:
   - Name: Git-SSH  
   - Typ: Client
   - Port: 2222 (lokaler Port für Git-Zugriff)
   - Ziel: [your-git-server].i2p:22
   - Automatischer Start: Aktiviert
   - Anzahl der tunnel: 3-4 (mehr für höhere Zuverlässigkeit)
4. Speichern und tunnel starten
5. SSH so konfigurieren, dass der tunnel verwendet wird: `ssh -p 2222 git@127.0.0.1`

**SSH-Authentifizierungsfehler** über I2P entstehen meist durch:

- Schlüssel nicht zum ssh-agent hinzugefügt: `ssh-add ~/.ssh/id_rsa`
- Falsche Berechtigungen der Schlüsseldatei: `chmod 600 ~/.ssh/id_rsa`
- Tunnel läuft nicht: Prüfe unter http://127.0.0.1:7657/i2ptunnel, ob der Status grün ist
- Git-Server erfordert einen bestimmten Schlüsseltyp: Erstelle einen ed25519-Schlüssel, wenn RSA fehlschlägt

**Zeitüberschreitungen bei Git-Operationen** stehen im Zusammenhang mit den Latenzeigenschaften von I2P:

- Git-Timeout erhöhen: `git config --global http.postBuffer 524288000` (500 MB Puffer)
- Grenzwert für niedrige Geschwindigkeit erhöhen: `git config --global http.lowSpeedLimit 1000` und `git config --global http.lowSpeedTime 600` (wartet 10 Minuten)
- Für den initialen Checkout einen flachen Klon verwenden: `git clone --depth 1 [url]` (lädt nur den neuesten Commit, schneller)
- In Zeiten geringer Aktivität klonen: Netzwerküberlastung beeinträchtigt die I2P-Leistung

**Langsame git clone/fetch-Operationen** sind der Architektur von I2P inhärent. Ein 100‑MB‑Repository kann über I2P 30–60 Minuten dauern, im Gegensatz zu Sekunden im Clearnet. Strategien:

- Verwenden Sie flache Klone: `--depth 1` reduziert die anfängliche Datenübertragung deutlich
- Rufen Sie inkrementell ab: Statt eines vollständigen Klons rufen Sie spezifische Branches ab: `git fetch origin branch:branch`
- Erwägen Sie rsync über I2P: Für sehr große Repositories kann rsync eine bessere Leistung liefern
- Erhöhen Sie die Anzahl der tunnels: Mehr tunnels sorgen für einen höheren Durchsatz bei lang andauernden großen Übertragungen

**"Connection refused"-Fehler** weisen auf eine tunnel-Fehlkonfiguration hin:

1. Überprüfe, ob der I2P router läuft: Öffne http://127.0.0.1:7657
2. Bestätige, dass der tunnel aktiv und grün ist unter http://127.0.0.1:7657/i2ptunnel
3. Teste den tunnel: `nc -zv 127.0.0.1 2222` (sollte eine Verbindung herstellen, wenn der tunnel funktioniert)
4. Prüfe, ob das Ziel erreichbar ist: Rufe die HTTP-Oberfläche des Ziels im Browser auf, falls verfügbar
5. Überprüfe die tunnel-Protokolle unter http://127.0.0.1:7657/logs auf spezifische Fehler

**Bewährte Vorgehensweisen für Git über I2P:**

- Lassen Sie den I2P router durchgehend laufen, um stabilen Git-Zugriff zu gewährleisten
- Verwenden Sie SSH-Schlüssel statt Passwortauthentifizierung (weniger interaktive Eingabeaufforderungen)
- Konfigurieren Sie persistente tunnels statt kurzlebiger SOCKS-Verbindungen
- Erwägen Sie, einen eigenen I2P-Git-Server zu betreiben, um mehr Kontrolle zu haben
- Dokumentieren Sie Ihre .i2p-Git-Endpunkte für Mitwirkende

## Zugriff auf eepsites und Auflösung von .i2p-Domains

Der häufigste Grund, warum Nutzer nicht auf .i2p-Sites zugreifen können, ist eine **falsche Browser-Proxy-Konfiguration**. I2P-Sites existieren nur innerhalb des I2P-Netzwerks und erfordern die Weiterleitung über den HTTP-Proxy von I2P.

**Proxy-Einstellungen des Browsers exakt konfigurieren:**

**Firefox (empfohlen für I2P):**

1. Menü → Einstellungen → Netzwerkeinstellungen → Schaltfläche "Einstellungen"
2. Wählen Sie "Manuelle Proxy-Konfiguration"
3. HTTP-Proxy: **127.0.0.1** Port: **4444**
4. SSL-Proxy: **127.0.0.1** Port: **4444**  
5. SOCKS-Proxy: **127.0.0.1** Port: **4447** (optional, für SOCKS-Apps)
6. Aktivieren Sie "DNS über Proxy bei Verwendung von SOCKS v5"
7. OK klicken, um zu speichern

**Kritische about:config-Einstellungen in Firefox:**

Navigieren Sie zu `about:config` und ändern Sie:

- `media.peerconnection.ice.proxy_only` = **true** (verhindert IP-Leaks über WebRTC)
- `keyword.enabled` = **false** (verhindert, dass .i2p-Adressen zu Suchmaschinen umgeleitet werden)
- `network.proxy.socks_remote_dns` = **true** (DNS über den Proxy)

**Chrome/Chromium-Einschränkungen:**

Chrome verwendet systemweite Proxyeinstellungen statt anwendungsspezifischer. Unter Windows: Einstellungen → nach "proxy" suchen → "Proxy-Einstellungen Ihres Computers öffnen" → HTTP konfigurieren: 127.0.0.1:4444 und HTTPS: 127.0.0.1:4445.

Besserer Ansatz: Verwenden Sie die Erweiterungen FoxyProxy oder Proxy SwitchyOmega für selektives .i2p-Routing.

**"Website Not Found In Address Book"-Fehler** bedeuten, dass dem router die kryptografische Adresse der .i2p-Domain fehlt. I2P verwendet lokale Adressbücher anstelle eines zentralisierten DNS. Lösungen:

**Methode 1: jump services (Sprung-Dienste) verwenden** (am einfachsten für neue Websites):

Rufen Sie http://stats.i2p auf und suchen Sie nach der Website. Klicken Sie auf den addresshelper-Link: `http://example.i2p/?i2paddresshelper=base64destination`. Ihr Browser zeigt "In Adressbuch speichern?" - bestätigen Sie, um es hinzuzufügen.

**Methode 2: Adressbuch-Abonnements aktualisieren:**

1. Navigieren Sie zu http://127.0.0.1:7657/dns (SusiDNS)
2. Klicken Sie auf die Registerkarte "Subscriptions"  
3. Überprüfen Sie die aktiven Abonnements (Standard: http://i2p-projekt.i2p/hosts.txt)
4. Fügen Sie empfohlene Abonnements hinzu:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Klicken Sie auf "Update Now", um eine sofortige Aktualisierung der Abonnements zu erzwingen
6. Warten Sie 5-10 Minuten auf die Verarbeitung

**Methode 3: Verwenden Sie base32-Adressen** (funktioniert immer, wenn die Website online ist):

Jede .i2p-Website hat eine Base32-Adresse: 52 zufällige Zeichen, gefolgt von .b32.i2p (z. B. `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Base32-Adressen umgehen das Adressbuch - der router führt eine direkte kryptografische Auflösung durch.

**Häufige Fehler bei der Browserkonfiguration:**

- Versuch, HTTPS auf nur-HTTP-Seiten zu verwenden: Die meisten .i2p-Seiten verwenden nur HTTP - der Aufruf von `https://example.i2p` schlägt fehl
- `http://`-Präfix vergessen: Der Browser könnte statt einer Verbindung eine Suche starten - immer `http://example.i2p` verwenden
- WebRTC aktiviert: Kann die echte IP-Adresse preisgeben - über die Firefox-Einstellungen oder Erweiterungen deaktivieren
- DNS nicht über Proxy geleitet: Clearnet-DNS kann .i2p nicht auflösen - DNS-Abfragen müssen über einen Proxy geleitet werden
- Falscher Proxy-Port: 4444 für HTTP (nicht 4445, das ist der HTTPS-Outproxy (Proxy zum Zugriff auf das Clearnet))

**Router nicht vollständig integriert** verhindert den Zugriff auf alle Seiten. Überprüfen Sie, ob die Integration ausreichend ist:

1. Prüfe, ob http://127.0.0.1:7657 "Network: OK" oder "Network: Firewalled" anzeigt (nicht "Network: Testing")
2. "Active peers" zeigt mindestens 10 an (optimal 50+)  
3. Keine Meldung "Rejecting tunnels: starting up"
4. Warte nach dem Start des router volle 10-15 Minuten, bevor du mit .i2p-Zugriff rechnest

**Konfiguration von IRC und E-Mail-Clients** folgt ähnlichen Proxy-Mustern:

**IRC:** IRC-Clients verbinden sich mit **127.0.0.1:6668** (IRC-Proxy-tunnel von I2P). Deaktivieren Sie die Proxy-Einstellungen des IRC-Clients - die Verbindung zu localhost:6668 wird bereits über I2P weitergeleitet.

**E-Mail (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Kein SSL/TLS (Verschlüsselung wird durch den I2P tunnel übernommen) - Zugangsdaten aus der Kontoregistrierung bei postman.i2p

Alle diese tunnels müssen auf http://127.0.0.1:7657/i2ptunnel den Status "running" (grün) anzeigen.

## Installationsfehler und Paketprobleme

Paketbasierte Installationen (Debian, Ubuntu, Arch) schlagen gelegentlich fehl aufgrund von **Repository-Änderungen**, **abgelaufenen GPG-Schlüsseln** oder **Abhängigkeitskonflikten**. Die offiziellen Repositories wurden in neueren Versionen von deb.i2p2.de/deb.i2p2.no (end-of-life) auf **deb.i2p.net** umgestellt.

**Debian/Ubuntu-Repository auf den aktuellen Stand aktualisieren:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Fehler bei der Überprüfung von GPG-Signaturen** treten auf, wenn Repository-Schlüssel ablaufen oder geändert werden:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**Dienst startet nach der Paketinstallation nicht** geht meist auf Probleme mit AppArmor-Profilen unter Debian/Ubuntu zurück:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Berechtigungsprobleme** bei paketinstalliertem I2P:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Java-Kompatibilitätsprobleme:**

I2P 2.10.0 erfordert **mindestens Java 8**. Ältere Systeme haben möglicherweise Java 7 oder älter:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Fehler in der Wrapper-Konfiguration** verhindern den Dienststart:

Der Speicherort von Wrapper.config variiert je nach Installationsmethode: - Benutzerinstallation: `~/.i2p/wrapper.config` - Paketinstallation: `/etc/i2p/wrapper.config` oder `/var/lib/i2p/wrapper.config`

Häufige Probleme mit wrapper.config:

- Falsche Pfade: `wrapper.java.command` muss auf eine gültige Java-Installation verweisen
- Unzureichender Speicher: `wrapper.java.maxmemory` zu niedrig eingestellt (auf 512+ erhöhen)
- Falscher Speicherort der PID-Datei: `wrapper.pidfile` muss auf einen beschreibbaren Speicherort verweisen
- Fehlende Wrapper-Binärdatei: Auf einigen Plattformen fehlt ein vorkompilierter Wrapper (runplain.sh als Fallback verwenden)

**Aktualisierungsfehler und beschädigte Updates:**

Aktualisierungen der Router-Konsole schlagen aufgrund von Netzwerkunterbrechungen gelegentlich während des Downloads fehl. Manuelles Update-Verfahren:

1. Laden Sie i2pupdate_X.X.X.zip von https://geti2p.net/en/download herunter
2. Überprüfen Sie, dass die SHA256-Prüfsumme dem veröffentlichten Hash entspricht
3. Kopieren Sie es in das I2P-Installationsverzeichnis als `i2pupdate.zip`
4. Starten Sie den router neu - erkennt und entpackt das Update automatisch
5. Warten Sie 5-10 Minuten auf die Installation des Updates
6. Überprüfen Sie die neue Version unter http://127.0.0.1:7657

**Migration von sehr alten Versionen** (vor 0.9.47) auf aktuelle Versionen kann aufgrund inkompatibler Signaturschlüssel oder entfernter Funktionen fehlschlagen. Schrittweise Aktualisierungen erforderlich:

- Versionen älter als 0.9.9: Aktuelle Signaturen können nicht überprüft werden - manuelles Update nötig
- Versionen mit Java 6/7: Java muss vor dem Update von I2P auf 2.x aktualisiert werden
- Große Versionssprünge: Zuerst auf eine Zwischenversion aktualisieren (0.9.47 ist ein empfohlener Zwischenstopp)

**Wann das Installationsprogramm statt eines Pakets verwenden:**

- **Pakete (apt/yum):** Am besten für Server, automatische Sicherheitsupdates, Systemintegration, systemd-Verwaltung
- **Installationsprogramm (.jar):** Am besten für Installation auf Benutzerebene, Windows, macOS, benutzerdefinierte Installationen, Verfügbarkeit der neuesten Version

## Beschädigung und Wiederherstellung von Konfigurationsdateien

Die dauerhafte Speicherung der I2P-Konfiguration beruht auf mehreren kritischen Dateien. Beschädigungen sind typischerweise die Folge von **unsachgemäßem Herunterfahren**, **Festplattenfehlern** oder **Fehlern bei manueller Bearbeitung**. Das Verständnis der Zwecke dieser Dateien ermöglicht eine gezielte Reparatur statt einer vollständigen Neuinstallation.

**Kritische Dateien und ihre Zwecke:**

- **router.keys** (516+ bytes): Kryptografische Identität des routers - geht sie verloren, wird eine neue Identität erstellt
- **router.info** (automatisch erzeugt): Veröffentlichte router-Informationen - kann gefahrlos gelöscht werden, wird neu erzeugt  
- **router.config** (Text): Hauptkonfiguration - Bandbreite, Netzwerkeinstellungen, Voreinstellungen
- **i2ptunnel.config** (Text): tunnel-Definitionen - client/server tunnels, Schlüssel, Ziele
- **netDb/** (Verzeichnis): Peer-Datenbank - router-Informationen für Netzwerkteilnehmer
- **peerProfiles/** (Verzeichnis): Leistungsstatistiken zu Peers - beeinflussen die tunnel-Auswahl
- **keyData/** (Verzeichnis): Zielschlüssel für eepsites und Dienste - bei Verlust ändern sich die Adressen
- **addressbook/** (Verzeichnis): Lokale .i2p-Hostname-Zuordnungen

**Vollständige Sicherungsprozedur** vor Änderungen:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Anzeichen einer Beschädigung der Router.config:**

- Router startet nicht, mit Parse-Fehlern in den Logs
- Einstellungen werden nach einem Neustart nicht beibehalten
- Unerwartete Standardwerte erscheinen  
- Verstümmelte Zeichen beim Anzeigen der Datei

**Beschädigte router.config reparieren:**

1. Vorhandene Datei sichern: `cp router.config router.config.broken`
2. Dateicodierung prüfen: Muss UTF-8 ohne BOM sein
3. Syntax prüfen: Schlüssel verwenden den Trenner `=` (nicht `:`), keine nachgestellten Leerzeichen bei Schlüsseln, `#` nur für Kommentare
4. Häufige Beschädigungen: Nicht-ASCII-Zeichen in Werten, Probleme mit Zeilenenden (CRLF vs LF)
5. Wenn nicht reparierbar: router.config löschen - router erzeugt eine Standarddatei unter Beibehaltung der Identität

**Zwingend beizubehaltende router.config-Einstellungen:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**Verlorene oder ungültige router.keys** erstellt eine neue router-Identität. Dies ist akzeptabel, es sei denn:

- Betrieb von floodfill (verliert floodfill-Status)
- Hosten von eepsites mit veröffentlichter Adresse (verliert Kontinuität)  
- Etablierter Ruf im Netzwerk

Ohne Backup ist keine Wiederherstellung möglich – neu erstellen: router.keys löschen, I2P neu starten, neue Identität wird erstellt.

**Wichtiger Unterschied:** router.keys (Identität) gegenüber keyData/* (Dienste). Der Verlust von router.keys ändert die router-Identität. Der Verlust von keyData/mysite-keys.dat ändert die .i2p-Adresse deiner eepsite - katastrophal, wenn die Adresse bereits veröffentlicht wurde.

**Schlüssel für eepsite/Dienst separat sichern:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Beschädigung von NetDb und peerProfiles:**

Symptome: Keine aktiven Peers, tunnels lassen sich nicht aufbauen, "Database corruption detected" in den Logs

Sichere Lösung (alles wird automatisch reseeded/neu aufgebaut):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Diese Verzeichnisse enthalten nur zwischengespeicherte Netzwerkinformationen - das Löschen erzwingt einen frischen Bootstrap, führt jedoch zu keinem Verlust kritischer Daten.

**Präventionsstrategien:**

1. **Immer ordnungsgemäß herunterfahren:** `i2prouter stop` verwenden oder den "Shutdown"-Button der router console - niemals zwangsweise beenden
2. **Automatisierte Backups:** Wöchentlicher Cron-Job sichert ~/.i2p auf ein separates Laufwerk
3. **Überwachung der Laufwerksgesundheit:** SMART-Status regelmäßig prüfen - ausfallende Laufwerke beschädigen Daten
4. **Ausreichend Speicherplatz:** Mindestens 1+ GB frei halten - volle Laufwerke führen zu Datenbeschädigungen
5. **USV empfohlen:** Stromausfälle während Schreibvorgängen beschädigen Dateien
6. **Versionskontrolle kritischer Konfigurationen:** Ein Git-Repository für router.config, i2ptunnel.config ermöglicht Rollbacks

**Dateiberechtigungen sind wichtig:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Häufige Fehlermeldungen erklärt

Die Protokollierung von I2P liefert spezifische Fehlermeldungen, die Probleme genau identifizieren. Das Verständnis dieser Meldungen beschleunigt die Fehlerbehebung.

**"No tunnels available"** erscheint, wenn der router noch nicht genügend tunnels für den Betrieb aufgebaut hat. Dies ist **in den ersten 5-10 Minuten** nach dem Start normal. Wenn es länger als 15 Minuten anhält:

1. Überprüfen, dass Aktive Peers > 10 unter http://127.0.0.1:7657
2. Prüfen, ob die Bandbreitenzuweisung ausreichend ist (mindestens 128 KB/s)
3. Erfolgsrate der tunnel unter http://127.0.0.1:7657/tunnels prüfen (sollte >40% sein)
4. Protokolle auf Gründe für abgelehnte tunnel-Aufbauten prüfen

**"Clock skew detected"** oder **"NTCP2 disconnect code 7"** bedeutet, dass die Systemzeit um mehr als 90 Sekunden vom Netzwerkkonsens abweicht. I2P erfordert **±60 Sekunden Genauigkeit**. Verbindungen zu einem router, dessen Zeit abweicht, werden automatisch abgelehnt.

Sofort beheben:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** oder **"Tunnel build timeout exceeded"** bedeutet, dass der tunnel-Aufbau durch die peer chain (Kette von Gegenstellen) nicht innerhalb des Timeout-Fensters (typischerweise 60 Sekunden) abgeschlossen wurde. Ursachen:

- **Langsame Peers:** Router hat nicht reagierende Teilnehmer für einen tunnel ausgewählt
- **Netzüberlastung:** I2P-Netzwerk weist hohe Auslastung auf
- **Unzureichende Bandbreite:** Ihre Bandbreitenbegrenzungen verhindern den rechtzeitigen tunnel-Aufbau
- **Überlasteter router:** Zu viele teilnehmende tunnels verbrauchen Ressourcen

Lösungen: Bandbreite erhöhen, Anzahl teilnehmender tunnels reduzieren (`router.maxParticipatingTunnels` unter http://127.0.0.1:7657/configadvanced), Portweiterleitung für eine bessere Peer-Auswahl aktivieren.

**"Router is shutting down"** oder **"Graceful shutdown in progress"** erscheint während des normalen Herunterfahrens oder der Wiederherstellung nach einem Absturz. Ein geordnetes Herunterfahren kann **bis zu 10 Minuten** dauern, da der router tunnels schließt, Gegenstellen benachrichtigt und den Zustand speichert.

Wenn der Shutdown-Zustand länger als 11 Minuten anhält, Beendigung erzwingen:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** weist auf die Erschöpfung des Heap-Speichers hin. Unmittelbare Lösungen:

1. wrapper.config bearbeiten: `wrapper.java.maxmemory=512` (oder höher)
2. **Vollständiges Herunterfahren erforderlich** - ein Neustart wendet die Änderung nicht an
3. 11 Minuten auf vollständiges Herunterfahren warten  
4. router neu starten
5. Speicherzuweisung unter http://127.0.0.1:7657/graphs überprüfen - sollte Reserven anzeigen

**Verwandte Speicherfehler:**

- **"GC overhead limit exceeded":** Zu viel Zeit wird mit der Garbage Collection verbracht - Heap vergrößern
- **"Metaspace" (Speicherbereich für Java-Klassenmetadaten):** Java-Klassen-Metadatenbereich erschöpft - `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M` hinzufügen

**Windows-spezifisch:** Kaspersky Antivirus begrenzt den Java-Heap auf 512MB, unabhängig von den Einstellungen in wrapper.config - deinstallieren oder I2P zu den Ausnahmen hinzufügen.

**"Connection timeout"** oder **"I2CP Error - port 7654"**, wenn Anwendungen versuchen, sich mit dem router zu verbinden:

1. Überprüfen, ob der router läuft: http://127.0.0.1:7657 sollte antworten
2. I2CP-Port prüfen: `netstat -an | grep 7654` sollte LISTENING anzeigen
3. Sicherstellen, dass die localhost-Firewall dies erlaubt: `sudo ufw allow from 127.0.0.1`  
4. Überprüfen, ob die Anwendung den richtigen Port verwendet (I2CP=7654, SAM=7656)

**"Certificate validation failed"** oder **"RouterInfo corrupt"** beim Reseed:

Hauptursachen: Uhrzeitabweichung (zuerst beheben), beschädigte netDb, ungültige Reseed-Zertifikate

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Database corruption detected"** weist auf Datenkorruption auf Datenträger-Ebene in netDb oder peerProfiles hin:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Überprüfen Sie den Zustand des Datenträgers mit SMART-Tools - wiederkehrende Datenkorruption deutet auf ein ausfallendes Speichermedium hin.

## Plattformspezifische Herausforderungen

Verschiedene Betriebssysteme stellen spezifische Herausforderungen bei der I2P-Bereitstellung dar, die mit Berechtigungen, Sicherheitsrichtlinien und der Systemintegration zusammenhängen.

### Probleme mit Berechtigungen und Diensten unter Linux

Als Paket installiertes I2P läuft als Systembenutzer **i2psvc** (Debian/Ubuntu) oder **i2p** (andere Distributionen) und erfordert bestimmte Berechtigungen:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Grenzwerte für Dateideskriptoren** beeinflussen, wie viele Verbindungen ein router verarbeiten kann. Standardgrenzwerte (1024) sind für router mit hoher Bandbreite unzureichend:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**AppArmor-Konflikte**, die unter Debian/Ubuntu häufig auftreten, verhindern den Start des Dienstes:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**SELinux-Probleme** unter RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Fehlerbehebung bei SystemD-Diensten:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Störungen durch Windows-Firewall und Antivirenprogramme

Windows Defender und Antivirenprodukte von Drittanbietern stufen I2P aufgrund von Mustern im Netzwerkverhalten häufig als verdächtig ein. Eine korrekte Konfiguration verhindert unnötige Blockierungen, während die Sicherheit gewahrt bleibt.

**Windows Defender Firewall konfigurieren:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Ersetzen Sie den Port 22648 durch Ihren tatsächlichen I2P-Port von http://127.0.0.1:7657/confignet.

**Spezifisches Problem mit Kaspersky Antivirus:** Kasperskys "Application Control" begrenzt den Java-Heap unabhängig von den Einstellungen in wrapper.config auf 512MB. Dies führt zu einem OutOfMemoryError bei routers mit hoher Bandbreite.

Lösungen: 1. Fügen Sie I2P zu den Ausnahmen in Kaspersky hinzu: Einstellungen → Zusätzlich → Bedrohungen und Ausnahmen → Ausnahmen verwalten 2. Oder deinstallieren Sie Kaspersky (für den I2P‑Betrieb empfohlen)

**Allgemeine Hinweise zu Antivirensoftware von Drittanbietern:**

- I2P-Installationsverzeichnis zu den Ausnahmen hinzufügen  
- %APPDATA%\I2P und %LOCALAPPDATA%\I2P zu den Ausnahmen hinzufügen
- javaw.exe von der Verhaltensanalyse ausschließen
- Funktionen von "Network Attack Protection" deaktivieren, die mit I2P-Protokollen in Konflikt geraten könnten

### macOS Gatekeeper blockiert die Installation

macOS Gatekeeper verhindert das Ausführen unsignierter Anwendungen. I2P-Installationsprogramme sind nicht mit einer Apple Developer ID signiert, was Sicherheitswarnungen auslöst.

**Gatekeeper für das I2P-Installationsprogramm umgehen:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Das Starten nach der Installation** kann weiterhin Warnmeldungen auslösen:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Gatekeeper niemals dauerhaft deaktivieren** - Sicherheitsrisiko für andere Anwendungen. Verwende nur dateispezifische Umgehungen.

**Konfiguration der macOS-Firewall:**

1. Systemeinstellungen → Sicherheit & Datenschutz → Firewall → Firewall-Optionen
2. Klicken Sie auf "+", um ein Programm hinzuzufügen  
3. Navigieren Sie zur Java-Installation (z. B. `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Hinzufügen und auf "Eingehende Verbindungen erlauben" setzen

### Probleme mit der Android-I2P-App

Beschränkungen der Android-Versionen und Ressourcenbegrenzungen bringen einzigartige Herausforderungen mit sich.

**Mindestanforderungen:** - Android 5.0+ (API-Level 21+) erforderlich für aktuelle Versionen - 512MB RAM mindestens, 1GB+ empfohlen   - 100MB Speicher für App + router-Daten - Hintergrund-App-Einschränkungen für I2P deaktiviert

**App stürzt sofort ab:**

1. **Android-Version prüfen:** Einstellungen → Über das Telefon → Android-Version (muss 5.0+ sein)
2. **Alle I2P-Versionen deinstallieren:** Nur eine Variante installieren:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Mehrere Installationen führen zu Konflikten
3. **App-Daten löschen:** Einstellungen → Apps → I2P → Speicher → Daten löschen
4. **Neu installieren aus sauberem Zustand**

**Batterieoptimierung beendet den router:**

Android beendet Apps im Hintergrund aggressiv, um Akku zu sparen. I2P muss davon ausgenommen werden:

1. Einstellungen → Akku → Akkuoptimierung (oder Akkunutzung der App)
2. I2P suchen → Nicht optimieren (oder Hintergrundaktivität zulassen)
3. Einstellungen → Apps → I2P → Akku → Hintergrundaktivität zulassen + Einschränkungen entfernen

**Verbindungsprobleme auf Mobilgeräten:**

- **Bootstrap erfordert WLAN:** Das initiale reseed (Erstabruf der Netzwerkdaten) lädt erhebliche Datenmengen herunter - verwenden Sie WLAN, nicht Mobilfunk
- **Netzwerkänderungen:** I2P verträgt Netzwerkwechsel nicht gut - starten Sie die App nach einem WLAN/Mobilfunk-Wechsel neu
- **Bandbreite für Mobilgeräte:** Konfigurieren Sie konservativ auf 64-128 KB/sec, um Ihr Mobilfunkdatenvolumen nicht zu erschöpfen

**Leistungsoptimierung für Mobilgeräte:**

1. I2P-App → Menü → Einstellungen → Bandbreite
2. Geeignete Limits festlegen: 64 KB/sec eingehend, 32 KB/sec ausgehend für Mobilfunk
3. Teilnehmende tunnels (virtuelle Datenkanäle) reduzieren: Einstellungen → Erweitert → Max. teilnehmende tunnels: 100-200
4. "I2P bei ausgeschaltetem Bildschirm stoppen" aktivieren, um den Akku zu schonen

**Torrent-Nutzung unter Android:**

- Auf höchstens 2-3 gleichzeitige Torrents begrenzen
- DHT-Aggressivität reduzieren  
- WiFi nur für Torrents verwenden
- Langsamere Geschwindigkeiten auf mobiler Hardware in Kauf nehmen

## Reseed- und Bootstrap-Probleme

Neue I2P-Installationen erfordern **Reseeding** (Initialisierung der Peerliste) - das Abrufen anfänglicher Peerinformationen von öffentlichen HTTPS-Servern, um dem Netzwerk beizutreten. Reseeding-Probleme führen dazu, dass Benutzer ohne Peers und ohne Netzwerkzugang steckenbleiben.

**"Keine aktiven Peers" nach einer Neuinstallation** deutet typischerweise auf einen fehlgeschlagenen Reseed (Initialbefüllung der netDb) hin. Symptome:

- Bekannte Peers: 0 oder bleibt unter 5
- "Network: Testing" bleibt länger als 15 Minuten bestehen
- Protokolle zeigen "Reseed failed" oder Verbindungsfehler zu Reseed-Servern (Bootstrap-Server für den anfänglichen netDb-Download)

**Warum das Reseed (Initialbefüllung der netDb) fehlschlägt:**

1. **Firewall blockiert HTTPS:** Unternehmens-/ISP-Firewalls blockieren Verbindungen zu Reseed-Servern (Port 443)
2. **SSL-Zertifikatsfehler:** Dem System fehlen aktuelle Stammzertifikate
3. **Proxy erforderlich:** Netzwerk erfordert einen HTTP-/SOCKS-Proxy für externe Verbindungen
4. **Uhrzeitabweichung:** Die Validierung von SSL-Zertifikaten schlägt fehl, wenn die Systemzeit falsch ist
5. **Geografische Zensur:** Einige Länder/ISPs blockieren bekannte Reseed-Server

**Manuelles Reseed (Neubezug der Router-Informationen zur Initialisierung der netDb) erzwingen:**

1. Rufen Sie http://127.0.0.1:7657/configreseed auf
2. Klicken Sie auf "Save changes and reseed now"  
3. Überwachen Sie http://127.0.0.1:7657/logs auf "Reseed got XX router infos"
4. Warten Sie 5-10 Minuten, bis die Verarbeitung abgeschlossen ist
5. Prüfen Sie http://127.0.0.1:7657 - die bekannten Peers sollten auf 50+ ansteigen

**Reseed-Proxy konfigurieren** für restriktive Netzwerke:

http://127.0.0.1:7657/configreseed → Proxy-Konfiguration:

- HTTP-Proxy: [proxy-server]:[port]
- Oder SOCKS5: [socks-server]:[port]  
- Aktivieren Sie "Use proxy for reseed only" (Reseed = Neuaufbau der Peer-Liste)
- Anmeldedaten, falls erforderlich
- Speichern und Reseed erzwingen

**Alternative: Tor-Proxy für Reseed (initiales Laden der netDb):**

Wenn der Tor Browser oder der Tor-Daemon läuft:

- Proxy-Typ: SOCKS5
- Host: 127.0.0.1
- Port: 9050 (Standard-SOCKS-Port von Tor)
- Aktivieren und Reseed starten (Netzwerk-Bootstrapping)

**Manuelles Reseed über su3-Datei** (letzter Ausweg):

Wenn alle automatischen Reseeds fehlschlagen, beschaffen Sie die Reseed-Datei out-of-band (außerhalb des regulären Kanals):

1. i2pseeds.su3 von einer vertrauenswürdigen Quelle über eine uneingeschränkte Verbindung herunterladen (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. I2P vollständig beenden
3. i2pseeds.su3 in das Verzeichnis ~/.i2p/ kopieren  
4. I2P starten - extrahiert und verarbeitet die Datei automatisch
5. i2pseeds.su3 nach der Verarbeitung löschen
6. Prüfen, ob die Anzahl der Peers unter http://127.0.0.1:7657 steigt

**SSL-Zertifikatsfehler während des Reseeds (Erstbefüllung der netDb):**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Lösungen:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Seit über 30 Minuten bei 0 bekannten Peers festhängend:**

Signalisiert ein vollständiges Scheitern des Reseed (Erstbezug der netDb-Daten zur Initialisierung des router). Reihenfolge zur Fehlerbehebung:

1. **Systemzeit auf Korrektheit prüfen** (häufigstes Problem - ZUERST beheben)
2. **HTTPS-Konnektivität testen:** Versuche, https://reseed.i2p.rocks im Browser aufzurufen - wenn das fehlschlägt, liegt ein Netzwerkproblem vor
3. **I2P-Protokolle prüfen** unter http://127.0.0.1:7657/logs auf spezifische reseed-Fehler (reseed: initiales Bootstrapping, Herunterladen der netDb-Peerliste)
4. **Andere reseed-URL ausprobieren:** http://127.0.0.1:7657/configreseed → benutzerdefinierte reseed-URL hinzufügen: https://reseed-fr.i2pd.xyz/
5. **Manuelle su3-Datei-Methode verwenden**, wenn automatisierte Versuche ausgeschöpft sind

**Reseed-Server gelegentlich offline:** I2P enthält mehrere fest kodierte Reseed-Server. Wenn einer ausfällt, versucht der router automatisch andere. Ein vollständiger Ausfall aller Reseed-Server ist äußerst selten, aber möglich.

**Derzeit aktive reseed servers (Server, die neue Router beim ersten Start mit netDb-Daten versorgen)** (Stand: Oktober 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Als benutzerdefinierte URLs hinzufügen, wenn es Probleme mit den Standard-URLs gibt.

**Für Nutzer in stark zensierten Regionen:**

Erwägen Sie, Snowflake/Meek bridges (Tor-Bridges mittels Pluggable Transports) über Tor für das anfängliche reseed (erste netDb-Befüllung) zu verwenden und anschließend auf direktes I2P umzuschalten. Oder beziehen Sie i2pseeds.su3 per Steganographie, E-Mail oder USB von außerhalb der Zensurzone.

## Wann man zusätzliche Hilfe in Anspruch nehmen sollte

Dieser Leitfaden deckt die überwiegende Mehrheit der I2P-Probleme ab, aber einige Probleme erfordern die Aufmerksamkeit von Entwicklern oder die Expertise der Community.

**Wenden Sie sich an die I2P-Community, wenn:**

- Router stürzt reproduzierbar ab, nachdem alle Schritte zur Fehlerbehebung befolgt wurden
- Speicherlecks führen zu stetigem Wachstum über den zugewiesenen Heap hinaus
- Tunnel-Erfolgsquote bleibt trotz angemessener Konfiguration unter 20%  
- Neue Fehler in den Protokollen, die in diesem Leitfaden nicht abgedeckt sind
- Entdeckte Sicherheitslücken
- Funktionswünsche oder Verbesserungsvorschläge

**Bevor Sie Hilfe anfordern, sammeln Sie Diagnosedaten:**

1. I2P-Version: http://127.0.0.1:7657 (z. B., "2.10.0")
2. Java-Version: `java -version` Ausgabe
3. Betriebssystem und Version
4. Router-Status: Netzwerkzustand, Anzahl aktiver Peers, teilnehmende tunnels
5. Bandbreitenkonfiguration: Eingehende/ausgehende Limits
6. Portweiterleitungsstatus: Hinter Firewall oder OK
7. Relevante Logauszüge: Letzte 50 Zeilen, die Fehler zeigen, von http://127.0.0.1:7657/logs

**Offizielle Supportkanäle:**

- **Forum:** https://i2pforum.net (clearnet, öffentliches Internet) oder http://i2pforum.i2p (innerhalb von I2P)
- **IRC:** #i2p auf Irc2P (irc.postman.i2p über I2P) oder irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p für Community-Diskussionen
- **Bug-Tracker:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues für bestätigte Fehler
- **Mailingliste:** i2p-dev@lists.i2p-projekt.de für Entwicklungsfragen

**Realistische Erwartungen sind wichtig.** I2P ist durch sein grundlegendes Design langsamer als clearnet (offenes Internet) - Multi-Hop-verschlüsselte tunnel erzeugen inhärente Latenz. Ein funktionierender I2P router mit Seitenladezeiten von 30 Sekunden und Torrent-Geschwindigkeiten von 50 KB/sec **funktioniert ordnungsgemäß**, ist nicht defekt. Nutzer, die clearnet-Geschwindigkeiten erwarten, werden unabhängig von jeder Optimierung der Konfiguration enttäuscht sein.

## Fazit

Die meisten I2P-Probleme lassen sich auf drei Kategorien zurückführen: unzureichende Geduld während der Bootstrap-Phase (10-15 Minuten erforderlich), unzureichende Ressourcenzuweisung (mindestens 512 MB RAM, 256 KB/sec Bandbreite) oder falsch konfigurierte Portweiterleitung. Das Verständnis der verteilten Architektur von I2P und seines auf Anonymität ausgerichteten Designs hilft Nutzerinnen und Nutzern, erwartetes Verhalten von tatsächlichen Problemen zu unterscheiden.

Der "Firewalled"-Status des router ist zwar suboptimal, verhindert die Nutzung von I2P jedoch nicht - er begrenzt nur den Beitrag zum Netzwerk und verschlechtert die Leistung leicht. Neue Nutzer sollten **Stabilität vor Optimierung** priorisieren: Den router mehrere Tage lang ununterbrochen laufen lassen, bevor sie erweiterte Einstellungen anpassen, da sich die Integration mit zunehmender Betriebszeit von selbst verbessert.

Bei der Fehlersuche überprüfen Sie immer zuerst die Grundlagen: korrekte Systemzeit, ausreichende Bandbreite, durchgehend laufender router und 10+ aktive Peers. Die meisten Probleme lassen sich durch die Behebung dieser Grundlagen lösen, statt obskure Konfigurationsparameter anzupassen. I2P belohnt Geduld und kontinuierlichen Betrieb mit verbesserter Leistung, da der router im Laufe von Tagen und Wochen an Betriebszeit Reputation aufbaut und die Auswahl der Peers optimiert.
