---
title: "Router Console Konfigurationsanleitung"
description: "Eine umfassende Anleitung zum Verstehen und Konfigurieren der I2P Router Console"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: docs
---

Diese Anleitung bietet einen Überblick über die I2P Router Console und ihre Konfigurationsseiten. Jeder Abschnitt erklärt, was die Seite macht und wofür sie gedacht ist, und hilft Ihnen zu verstehen, wie Sie Ihren I2P Router überwachen und konfigurieren können.

## Zugriff auf die Router-Konsole

Die I2P Router Console ist die zentrale Anlaufstelle für die Verwaltung und Überwachung Ihres I2P Routers. Standardmäßig ist sie unter [I2P Router Console](http://127.0.0.1:7657/home) erreichbar, sobald Ihr I2P Router läuft.

![Router Console Home](/images/router-console-home.png)

Die Startseite zeigt mehrere wichtige Bereiche an:

- **Anwendungen** - Schnellzugriff auf integrierte I2P-Anwendungen wie E-Mail, Torrents, Hidden Services Manager und Webserver
- **I2P-Community-Seiten** - Links zu wichtigen Community-Ressourcen einschließlich Foren, Dokumentation und Projekt-Websites
- **Konfiguration und Hilfe** - Werkzeuge zur Konfiguration von Bandbreiteneinstellungen, Verwaltung von Plugins und Zugriff auf Hilferessourcen
- **Netzwerk- und Entwicklerinformationen** - Zugriff auf Graphen, Protokolle, technische Dokumentation und Netzwerkstatistiken

## Adressbuch

**URL:** [Address Book](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

Das I2P-Adressbuch funktioniert ähnlich wie DNS im Clearnet und ermöglicht es Ihnen, lesbare Namen für I2P-Ziele (eepsites) zu verwalten. Hier können Sie I2P-Adressen in Ihrem persönlichen Adressbuch anzeigen und hinzufügen.

Das Adressbuch-System funktioniert über mehrere Ebenen:

- **Lokale Einträge** - Ihre persönlichen Adressbücher, die nur auf Ihrem Router gespeichert werden
  - **Lokales Adressbuch** - Hosts, die Sie manuell hinzufügen oder für Ihre eigene Verwendung speichern
  - **Privates Adressbuch** - Adressen, die Sie nicht mit anderen teilen möchten; werden niemals öffentlich verteilt

- **Subscriptions** - Remote-Adressbuchquellen (wie `http://i2p-projekt.i2p/hosts.txt`), die das Adressbuch deines Routers automatisch mit bekannten I2P-Sites aktualisieren

- **Router Addressbook** - Das zusammengeführte Ergebnis Ihrer lokalen Einträge und Abonnements, durchsuchbar von allen I2P-Anwendungen auf Ihrem Router

- **Published Addressbook** - Optionales öffentliches Teilen Ihres Adressbuchs, damit andere es als Abonnementquelle nutzen können (nützlich, wenn Sie eine I2P-Seite betreiben)

Das Adressbuch fragt regelmäßig Ihre Abonnements ab und fügt Inhalte in Ihr Router-Adressbuch ein, sodass Ihre hosts.txt-Datei mit dem I2P-Netzwerk auf dem neuesten Stand bleibt.

## Konfiguration

**URL:** [Erweiterte Konfiguration](http://127.0.0.1:7657/configadvanced)

Der Konfigurationsbereich bietet über mehrere spezialisierte Registerkarten Zugriff auf alle Router-Einstellungen.

### Advanced

![Router Console Advanced Configuration](/images/router-console-config-advanced.png)

Die Seite für erweiterte Konfiguration bietet Zugriff auf systemnahe Router-Einstellungen, die für den normalen Betrieb normalerweise nicht benötigt werden. **Die meisten Benutzer sollten diese Einstellungen nicht ändern, sofern sie die jeweilige Konfigurationsoption und deren Auswirkungen auf das Router-Verhalten nicht verstehen.**

Hauptmerkmale:

- **Floodfill-Konfiguration** - Legen Sie fest, ob Ihr Router als Floodfill-Peer teilnimmt, der das Netzwerk unterstützt, indem er Informationen der Netzwerkdatenbank (netDb) speichert und verteilt. Dies kann mehr Systemressourcen verbrauchen, stärkt aber das I2P-Netzwerk.

- **Erweiterte I2P-Konfiguration** - Direkter Zugriff auf die `router.config`-Datei mit allen erweiterten Konfigurationsparametern, einschließlich:
  - Bandbreitenlimits und Burst-Einstellungen
  - Transport-Einstellungen (NTCP2, SSU2, UDP-Ports und Schlüssel)
  - Router-Identifikation und Versionsinformationen
  - Konsolenpräferenzen und Update-Einstellungen

Die meisten erweiterten Konfigurationsoptionen werden in der Benutzeroberfläche nicht angezeigt, da sie selten benötigt werden. Um die Bearbeitung dieser Einstellungen zu aktivieren, müssen Sie `routerconsole.advanced=true` manuell zu Ihrer `router.config`-Datei hinzufügen.

**Warnung:** Fehlerhafte Änderungen an erweiterten Einstellungen können die Leistung oder Konnektivität Ihres Routers negativ beeinflussen. Ändern Sie diese Einstellungen nur, wenn Sie wissen, was Sie tun.

### Bandwidth

**URL:** [Bandbreiten-Konfiguration](http://127.0.0.1:7657/config)

![Router Console Bandwidth-Konfiguration](/images/router-console-config-bandwidth.png)

Die Bandwidth-Konfigurationsseite ermöglicht es Ihnen zu steuern, wie viel Bandbreite Ihr Router zum I2P-Netzwerk beiträgt. I2P funktioniert am besten, wenn Sie Ihre Raten entsprechend der Geschwindigkeit Ihrer Internetverbindung konfigurieren.

**Wichtige Einstellungen:**

- **KBps In** - Maximale eingehende Bandbreite, die Ihr Router akzeptiert (Download-Geschwindigkeit)
- **KBps Out** - Maximale ausgehende Bandbreite, die Ihr Router verwendet (Upload-Geschwindigkeit)
- **Share** - Prozentsatz Ihrer ausgehenden Bandbreite, der für Participatory Traffic dediziert ist (hilft beim Routen von Traffic für andere)

**Wichtige Hinweise:**

- Alle Werte sind in **Bytes pro Sekunde** (KBps), nicht Bits pro Sekunde
- Je mehr Bandbreite Sie zur Verfügung stellen, desto mehr helfen Sie dem Netzwerk und verbessern Ihre eigene Anonymität
- Ihre Upload-Bandbreite (KBps Out) bestimmt Ihren Gesamtbeitrag zum Netzwerk
- Wenn Sie sich über die Geschwindigkeit Ihres Netzwerks unsicher sind, verwenden Sie den **Bandbreitentest**, um sie zu messen
- Höhere Bandbreite verbessert sowohl Ihre Anonymität als auch die Stärke des I2P-Netzwerks

Die Konfigurationsseite zeigt die geschätzte monatliche Datenübertragung basierend auf Ihren Einstellungen an und hilft Ihnen dabei, die Bandbreitenzuteilung entsprechend den Limits Ihres Internetvertrags zu planen.

### Client Configuration

**URL:** [Client-Konfiguration](http://127.0.0.1:7657/configclients)

![Router Console Client Configuration](/images/router-console-config-clients.png)

Die Client-Konfigurationsseite ermöglicht es Ihnen zu steuern, welche I2P-Anwendungen und -Dienste beim Start ausgeführt werden. Hier können Sie integrierte I2P-Clients aktivieren oder deaktivieren, ohne sie zu deinstallieren.

**Wichtige Warnung:** Seien Sie vorsichtig beim Ändern der Einstellungen hier. Die Router-Konsole und Anwendungs-Tunnel werden für die meisten Verwendungszwecke von I2P benötigt. Nur fortgeschrittene Benutzer sollten diese Einstellungen ändern.

**Verfügbare Clients:**

- **Application tunnels** - Das I2PTunnel-System, das Client- und Server-Tunnel verwaltet (HTTP-Proxy, IRC, etc.)
- **I2P Router Console** - Die webbasierte Administrationsoberfläche, die Sie gerade verwenden
- **I2P webserver (eepsite)** - Eingebauter Jetty-Webserver zum Hosten Ihrer eigenen I2P-Website
- **Open Router Console in web browser at startup** - Startet automatisch Ihren Browser mit der Konsolen-Startseite
- **SAM application bridge** - API-Brücke für Drittanbieter-Anwendungen zur Verbindung mit I2P

Jeder Client zeigt: - **Beim Start ausführen?** - Kontrollkästchen zum Aktivieren/Deaktivieren des automatischen Starts - **Steuerung** - Start/Stopp-Schaltflächen für sofortige Kontrolle - **Klasse und Argumente** - Technische Details darüber, wie der Client gestartet wird

Änderungen an der Einstellung „Beim Start ausführen?" erfordern einen Neustart des Routers, um wirksam zu werden. Alle Änderungen werden in `/var/lib/i2p/i2p-config/clients.config.d/` gespeichert.

### Erweitert

**URL:** [I2CP-Konfiguration](http://127.0.0.1:7657/configi2cp)

![Router Console I2CP-Konfiguration](/images/router-console-config-i2cp.png)

Die I2CP (I2P Client Protocol) Konfigurationsseite ermöglicht es Ihnen, zu konfigurieren, wie externe Anwendungen sich mit Ihrem I2P-Router verbinden. I2CP ist das Protokoll, das Anwendungen verwenden, um mit dem Router zu kommunizieren, um Tunnel zu erstellen und Daten über I2P zu senden/empfangen.

**Wichtig:** Die Standardeinstellungen funktionieren für die meisten Benutzer. Alle hier vorgenommenen Änderungen müssen auch in der externen Client-Anwendung konfiguriert werden. Viele Clients unterstützen weder SSL noch Authentifizierung. **Alle Änderungen erfordern einen Neustart, um wirksam zu werden.**

**Konfigurationsoptionen:**

- **Externe I2CP-Schnittstellen-Konfiguration**
  - **Aktiviert ohne SSL** - Standard-I2CP-Zugriff (Standard und am kompatibelsten)
  - **Aktiviert mit erforderlichem SSL** - Nur verschlüsselte I2CP-Verbindungen
  - **Deaktiviert** - Blockiert externe Clients bei der Verbindung über I2CP

- **I2CP Interface** - Die Netzwerkschnittstelle, auf der gelauscht werden soll (Standard: 127.0.0.1 nur für localhost)
- **I2CP Port** - Die Portnummer für I2CP-Verbindungen (Standard: 7654)

- **Autorisierung**
  - **Benutzername und Passwort erforderlich** - Authentifizierung für I2CP-Verbindungen aktivieren
  - **Benutzername** - Erforderlichen Benutzernamen für I2CP-Zugriff festlegen
  - **Passwort** - Erforderliches Passwort für I2CP-Zugriff festlegen

**Sicherheitshinweis:** Wenn Sie Anwendungen nur auf demselben Rechner wie Ihren I2P-Router ausführen, lassen Sie die Schnittstelle auf `127.0.0.1` gesetzt, um Fernzugriff zu verhindern. Ändern Sie diese Einstellungen nur, wenn Sie I2P-Anwendungen von anderen Geräten die Verbindung zu Ihrem Router ermöglichen müssen.

### Bandbreite

**URL:** [Netzwerkkonfiguration](http://127.0.0.1:7657/confignet)

![Router Console Network Configuration](/images/router-console-config-network.png)

Die Netzwerkkonfigurationsseite ermöglicht es Ihnen, zu konfigurieren, wie Ihr I2P-Router sich mit dem Internet verbindet, einschließlich IP-Adresserkennung, IPv4/IPv6-Einstellungen und Port-Einstellungen für sowohl UDP- als auch TCP-Transporte.

**Extern erreichbare IP-Adresse:**

- **Alle Auto-Erkennungsmethoden verwenden** - Erkennt Ihre öffentliche IP automatisch mit mehreren Methoden (empfohlen)
- **UPnP-IP-Adresserkennung deaktivieren** - Verhindert die Verwendung von UPnP zur Erkennung Ihrer IP
- **Lokale Netzwerkschnittstellen-IP-Adresse ignorieren** - Verwendet nicht Ihre lokale Netzwerk-IP
- **Nur SSU-IP-Adresserkennung verwenden** - Verwendet nur den SSU2-Transport zur IP-Erkennung
- **Versteckter Modus - IP nicht veröffentlichen** - Verhindert die Teilnahme am Netzwerkverkehr (reduziert Anonymität)
- **Hostname oder IP angeben** - Manuelle Festlegung Ihrer öffentlichen IP oder Ihres Hostnamens

**IPv4-Konfiguration:**

- **Eingehende Verbindungen deaktivieren (Firewalled)** - Aktivieren Sie diese Option, wenn Sie sich hinter einer Firewall, einem Heimnetzwerk, ISP, DS-Lite oder Carrier-Grade NAT befinden, die eingehende Verbindungen blockieren

**IPv6-Konfiguration:**

- **IPv4 gegenüber IPv6 bevorzugen** - Priorisiert IPv4-Verbindungen
- **IPv6 gegenüber IPv4 bevorzugen** - Priorisiert IPv6-Verbindungen (Standard für Dual-Stack-Netzwerke)
- **IPv6 aktivieren** - Erlaubt IPv6-Verbindungen
- **IPv6 deaktivieren** - Deaktiviert alle IPv6-Konnektivität
- **Nur IPv6 verwenden (IPv4 deaktivieren)** - Experimenteller IPv6-only-Modus
- **Eingehende Verbindungen deaktivieren (Firewalled)** - Prüfen Sie, ob Ihr IPv6 durch eine Firewall blockiert ist

**Aktion bei IP-Änderungen:**

- **Laptop-Modus** - Experimentelle Funktion, die Router-Identität und UDP-Port bei IP-Wechsel ändert, um die Anonymität zu erhöhen

**UDP-Konfiguration:**

- **Port angeben** - Einen bestimmten UDP-Port für SSU2-Transport festlegen (muss in Ihrer Firewall geöffnet werden)
- **Komplett deaktivieren** - Nur auswählen, wenn hinter einer Firewall, die alle ausgehenden UDP-Verbindungen blockiert

**TCP-Konfiguration:**

- **Port angeben** - Legt einen bestimmten TCP-Port für NTCP2-Transport fest (muss in Ihrer Firewall geöffnet werden)
- **Denselben Port wie für UDP verwenden** - Vereinfacht die Konfiguration durch Verwendung eines Ports für beide Transporte
- **Automatisch erkannte IP-Adresse verwenden** - Erkennt automatisch Ihre öffentliche IP-Adresse (zeigt „derzeit unbekannt" an, wenn noch nicht erkannt oder durch Firewall blockiert)
- **Immer automatisch erkannte IP-Adresse verwenden (Nicht durch Firewall geschützt)** - Am besten für Router mit direktem Internetzugang
- **Eingehende Verbindungen deaktivieren (Durch Firewall geschützt)** - Aktivieren Sie dies, wenn TCP-Verbindungen durch Ihre Firewall blockiert werden
- **Vollständig deaktivieren** - Nur auswählen, wenn Sie sich hinter einer Firewall befinden, die ausgehende TCP-Verbindungen drosselt oder blockiert
- **Hostname oder IP angeben** - Konfigurieren Sie manuell Ihre von außen erreichbare Adresse

**Wichtig:** Änderungen an den Netzwerkeinstellungen erfordern möglicherweise einen Router-Neustart, um vollständig wirksam zu werden. Eine ordnungsgemäße Port-Forwarding-Konfiguration verbessert die Leistung Ihres Routers erheblich und hilft dem I2P-Netzwerk.

### Client-Konfiguration

**URL:** [Peer-Konfiguration](http://127.0.0.1:7657/configpeer)

![Router Console Peer-Konfiguration](/images/router-console-config-peer.png)

Die Peer-Konfigurationsseite bietet manuelle Steuerungsmöglichkeiten zur Verwaltung einzelner Peers im I2P-Netzwerk. Dies ist eine erweiterte Funktion, die typischerweise nur zur Fehlerbehebung bei problematischen Peers verwendet wird.

**Manuelle Peer-Kontrollen:**

- **Router Hash** - Geben Sie den 44-stelligen Base64-Router-Hash des Peers ein, den Sie verwalten möchten

**Einen Peer manuell sperren / entsperren:**

Das Sperren eines Peers verhindert, dass dieser an von Ihnen erstellten Tunneln teilnimmt. Diese Aktion: - Verhindert, dass der Peer in Ihren Client- oder exploratory Tunnels verwendet wird - Tritt sofort in Kraft, ohne dass ein Neustart erforderlich ist - Bleibt bestehen, bis Sie den Peer manuell entsperren oder Ihren Router neu starten - **Peer bis zum Neustart sperren** - Blockiert den Peer temporär - **Peer entsperren** - Hebt die Sperre eines zuvor blockierten Peers auf

**Profilboni anpassen:**

Profil-Boni beeinflussen, wie Peers für die Tunnel-Teilnahme ausgewählt werden. Boni können positiv oder negativ sein: - **Schnelle Peers** - Werden für Client-Tunnel verwendet, die hohe Geschwindigkeit erfordern - **Hochkapazitäts-Peers** - Werden für einige Exploratory-Tunnel verwendet, die zuverlässiges Routing erfordern - Aktuelle Boni werden auf der Profilseite angezeigt

**Konfiguration:** - **Geschwindigkeit** - Geschwindigkeitsbonus für diesen Peer anpassen (0 = neutral) - **Kapazität** - Kapazitätsbonus für diesen Peer anpassen (0 = neutral) - **Peer-Boni anpassen** - Bonus-Einstellungen anwenden

**Anwendungsfälle:** - Sperren Sie einen Peer, der durchgehend Verbindungsprobleme verursacht - Schließen Sie vorübergehend einen Peer aus, den Sie für bösartig halten - Passen Sie Boni an, um leistungsschwache Peers herabzustufen - Beheben Sie Probleme beim Tunnel-Aufbau, indem Sie bestimmte Peers ausschließen

**Hinweis:** Die meisten Benutzer werden diese Funktion niemals verwenden müssen. Der I2P-Router verwaltet automatisch die Peer-Auswahl und -Profilerstellung basierend auf Leistungsmetriken.

### I2CP-Konfiguration

**URL:** [Reseed-Konfiguration](http://127.0.0.1:7657/configreseed)

![Router Console Reseed-Konfiguration](/images/router-console-config-reseed.png)

Die Reseed-Konfigurationsseite ermöglicht es Ihnen, Ihren Router manuell zu reseeden, falls das automatische Reseeding fehlschlägt. Reseeding ist der Bootstrapping-Prozess, der verwendet wird, um andere Router zu finden, wenn Sie I2P zum ersten Mal installieren oder wenn Ihr Router zu wenige Router-Referenzen übrig hat.

**Wann manuelles Reseed verwendet werden sollte:**

1. Wenn das Reseeding fehlgeschlagen ist, sollten Sie zuerst Ihre Netzwerkverbindung überprüfen
2. Wenn eine Firewall Ihre Verbindungen zu Reseed-Hosts blockiert, haben Sie möglicherweise Zugriff auf einen Proxy:
   - Der Proxy kann ein entfernter öffentlicher Proxy sein oder auf Ihrem Computer laufen (localhost)
   - Um einen Proxy zu verwenden, konfigurieren Sie den Typ, Host und Port im Abschnitt Reseeding-Konfiguration
   - Wenn Sie Tor Browser verwenden, führen Sie das Reseed darüber aus, indem Sie SOCKS 5, localhost, Port 9150 konfigurieren
   - Wenn Sie Tor über die Befehlszeile verwenden, führen Sie das Reseed darüber aus, indem Sie SOCKS 5, localhost, Port 9050 konfigurieren
   - Wenn Sie einige Peers haben, aber mehr benötigen, können Sie die I2P Outproxy-Option ausprobieren. Lassen Sie Host und Port leer. Dies funktioniert nicht für ein initiales Reseed, wenn Sie überhaupt keine Peers haben
   - Klicken Sie dann auf "Änderungen speichern und jetzt reseeden"
   - Die Standardeinstellungen funktionieren für die meisten Benutzer. Ändern Sie diese nur, wenn HTTPS durch eine restriktive Firewall blockiert wird und das Reseed fehlgeschlagen ist

3. Wenn Sie jemanden kennen und ihm vertrauen, der I2P betreibt, bitten Sie ihn, Ihnen eine reseed-Datei zu senden, die auf dieser Seite in seiner router console generiert wurde. Verwenden Sie dann diese Seite, um mit der erhaltenen Datei ein reseed durchzuführen. Wählen Sie zunächst die Datei unten aus. Klicken Sie dann auf "Reseed from file"

4. Wenn Sie jemanden kennen und ihm vertrauen, der Reseed-Dateien veröffentlicht, fragen Sie ihn nach der URL. Verwenden Sie dann diese Seite, um mit der erhaltenen URL zu reseeden. Geben Sie zunächst die URL unten ein. Klicken Sie dann auf „Reseed from URL"

5. Siehe [die FAQ](/docs/overview/faq/) für Anweisungen zum manuellen Reseeding

**Manuelle Reseed-Optionen:**

- **Reseed von URL** - Geben Sie eine ZIP- oder SU3-URL von einer vertrauenswürdigen Quelle ein und klicken Sie auf "Reseed von URL"
  - Das SU3-Format wird bevorzugt, da es als von einer vertrauenswürdigen Quelle signiert verifiziert wird
  - Das ZIP-Format ist nicht signiert; verwenden Sie eine ZIP-Datei nur von einer Quelle, der Sie vertrauen

- **Reseed von Datei** - Durchsuchen und Auswählen einer lokalen ZIP- oder SU3-Datei, dann auf „Reseed von Datei" klicken
  - Reseed-Dateien finden Sie unter [checki2p.com/reseed](https://checki2p.com/reseed)

- **Reseed-Datei erstellen** - Erstellt eine neue Reseed-ZIP-Datei, die Sie mit anderen teilen können, damit diese manuell reseeden können
  - Diese Datei wird niemals die Identität oder IP-Adresse Ihres eigenen Routers enthalten

**Reseeding-Konfiguration:**

Die Standardeinstellungen funktionieren für die meisten Benutzer. Ändern Sie diese nur, wenn HTTPS durch eine restriktive Firewall blockiert wird und das Reseed fehlgeschlagen ist.

- **Reseed-URLs** - Liste von HTTPS-URLs zu Reseed-Servern (Standardliste ist eingebaut und wird regelmäßig aktualisiert)
- **Proxy-Konfiguration** - Konfigurieren Sie HTTP/HTTPS/SOCKS-Proxy, falls Sie über einen Proxy auf Reseed-Server zugreifen müssen
- **URL-Liste zurücksetzen** - Stellt die Standard-Reseed-Serverliste wieder her

**Wichtig:** Manuelles Reseeding sollte nur in seltenen Fällen erforderlich sein, in denen das automatische Reseeding wiederholt fehlschlägt. Die meisten Benutzer werden diese Seite niemals benötigen.

### Netzwerkkonfiguration

**URL:** [Router Family Configuration](http://127.0.0.1:7657/configfamily)

![Router Console Router Family Konfiguration](/images/router-console-config-family.png)

Die Router Family Configuration Seite ermöglicht es Ihnen, Router-Familien zu verwalten. Router in derselben Familie teilen einen Family Key, der sie als von derselben Person oder Organisation betrieben kennzeichnet. Dies verhindert, dass mehrere von Ihnen kontrollierte Router für denselben Tunnel ausgewählt werden, was die Anonymität verringern würde.

**Was ist eine Router-Familie?**

Wenn Sie mehrere I2P-Router betreiben, sollten Sie diese als Teil derselben Familie konfigurieren. Dies gewährleistet: - Ihre Router werden nicht zusammen im selben Tunnelpfad verwendet - Andere Benutzer behalten die ordnungsgemäße Anonymität, wenn ihre Tunnel Ihre Router verwenden - Das Netzwerk kann die Tunnelbeteiligung angemessen verteilen

**Aktuelle Familie:**

Die Seite zeigt den aktuellen Router-Familiennamen an. Wenn Sie nicht Teil einer Familie sind, bleibt dieses Feld leer.

**Family Key exportieren:**

- **Exportieren Sie den geheimen Family-Schlüssel, um ihn in andere Router zu importieren, die Sie kontrollieren**
- Klicken Sie auf "Export Family Key", um Ihre Family-Schlüsseldatei herunterzuladen
- Importieren Sie diesen Schlüssel auf Ihren anderen Routern, um sie derselben Family hinzuzufügen

**Router-Familie verlassen:**

- **Nicht länger Mitglied der Familie sein**
- Klicken Sie auf "Familie verlassen", um diesen Router aus seiner aktuellen Familie zu entfernen
- Diese Aktion kann nicht rückgängig gemacht werden, ohne den Familienschlüssel erneut zu importieren

**Wichtige Überlegungen:**

- **Öffentliche Registrierung erforderlich:** Damit Ihre Familie netzwerkweit erkannt wird, muss Ihr Family-Key vom Entwicklungsteam in die I2P-Codebasis aufgenommen werden. Dadurch wird sichergestellt, dass alle Router im Netzwerk von Ihrer Familie wissen.
- **Kontaktieren Sie das I2P-Team**, um Ihren Family-Key registrieren zu lassen, wenn Sie mehrere öffentliche Router betreiben
- Die meisten Benutzer, die nur einen Router betreiben, werden diese Funktion niemals benötigen
- Die Family-Konfiguration wird hauptsächlich von Betreibern mehrerer öffentlicher Router oder Infrastrukturanbietern verwendet

**Anwendungsfälle:**

- Betrieb mehrerer I2P-Router für Redundanz
- Betrieb von Infrastruktur wie Reseed-Servern oder Outproxies auf mehreren Maschinen
- Verwaltung eines Netzwerks von I2P-Routern für eine Organisation

### Peer-Konfiguration

**URL:** [Tunnel-Konfiguration](http://127.0.0.1:7657/configtunnels)

![Router Console Tunnel-Konfiguration](/images/router-console-config-tunnels.png)

Die Tunnel-Konfigurationsseite ermöglicht es Ihnen, die Standardeinstellungen für Tunnel anzupassen, sowohl für exploratory tunnels (die für die Router-Kommunikation verwendet werden) als auch für Client-Tunnel (die von Anwendungen verwendet werden). **Die Standardeinstellungen funktionieren für die meisten Nutzer und sollten nur geändert werden, wenn Sie die Kompromisse verstehen.**

**Wichtige Warnhinweise:**

⚠️ **Anonymität vs. Leistung - Kompromiss:** Es gibt einen grundlegenden Kompromiss zwischen Anonymität und Leistung. Tunnel, die länger als 3 Hops sind (zum Beispiel 2 Hops + 0-2 Hops, 3 Hops + 0-1 Hops, 3 Hops + 0-2 Hops), oder eine hohe Anzahl + Backup-Anzahl, können die Leistung oder Zuverlässigkeit erheblich reduzieren. Eine hohe CPU- und/oder hohe ausgehende Bandbreitennutzung kann die Folge sein. Ändern Sie diese Einstellungen mit Vorsicht und passen Sie sie an, wenn Sie Probleme haben.

⚠️ **Persistenz:** Änderungen an den Exploratory Tunnel-Einstellungen werden in der Datei router.config gespeichert. Client Tunnel-Änderungen sind temporär und werden nicht gespeichert. Um permanente Client Tunnel-Änderungen vorzunehmen, siehe die [I2PTunnel-Seite](/docs/api/i2ptunnel).

**Exploratorische Tunnel:**

Exploratory Tunnels werden von Ihrem Router verwendet, um mit der netDb zu kommunizieren und am I2P-Netzwerk teilzunehmen.

Konfigurationsoptionen für sowohl Inbound als auch Outbound: - **Length** - Anzahl der Hops im Tunnel (Standard: 2-3 Hops) - **Randomization** - Zufällige Varianz in der Tunnellänge (Standard: 0-1 Hops) - **Quantity** - Anzahl der aktiven Tunnel (Standard: 2 Tunnel) - **Backup quantity** - Anzahl der Backup-Tunnel, die zur Aktivierung bereitstehen (Standard: 0 Tunnel)

**Client-Tunnel für I2P-Webserver:**

Diese Einstellungen steuern die Tunnel für den eingebauten I2P-Webserver (eepsite).

⚠️ **ANONYMITÄTSWARNUNG** - Einstellungen beinhalten 1-Hop-Tunnel. ⚠️ **LEISTUNGSWARNUNG** - Einstellungen beinhalten hohe Tunnelanzahlen.

Konfigurationsoptionen für sowohl Inbound als auch Outbound: - **Length** - Tunnel-Länge (Standard: 1 Hop für Webserver) - **Randomization** - Zufällige Varianz in der Tunnel-Länge - **Quantity** - Anzahl aktiver Tunnel - **Backup quantity** - Anzahl der Backup-Tunnel

**Client-Tunnel für gemeinsam genutzte Clients:**

Diese Einstellungen gelten für gemeinsam genutzte Client-Anwendungen (HTTP-Proxy, IRC usw.).

Konfigurationsoptionen für Inbound und Outbound: - **Length** - Tunnel-Länge (Standard: 3 Hops) - **Randomization** - Zufällige Varianz in der Tunnel-Länge - **Quantity** - Anzahl aktiver Tunnel - **Backup quantity** - Anzahl von Backup-Tunneln

**Tunnel-Parameter verstehen:**

- **Länge:** Längere Tunnel bieten mehr Anonymität, reduzieren jedoch Leistung und Zuverlässigkeit
- **Randomisierung:** Fügt Unvorhersehbarkeit zu Tunnelpfaden hinzu und verbessert die Sicherheit
- **Anzahl:** Mehr Tunnel verbessern Zuverlässigkeit und Lastverteilung, erhöhen jedoch die Ressourcennutzung
- **Backup-Anzahl:** Vorab erstellte Tunnel, die bereit sind, ausgefallene Tunnel zu ersetzen und die Ausfallsicherheit zu verbessern

**Best Practices:**

- Behalten Sie die Standardeinstellungen bei, sofern Sie keine spezifischen Anforderungen haben
- Erhöhen Sie die Tunnellänge nur, wenn Anonymität kritisch ist und Sie langsamere Performance akzeptieren können
- Erhöhen Sie Anzahl/Backup nur bei häufigen Tunnelausfällen
- Überwachen Sie die Router-Performance nach Änderungen
- Klicken Sie auf "Änderungen speichern", um Modifikationen anzuwenden

### Reseed-Konfiguration

**URL:** [UI-Konfiguration](http://127.0.0.1:7657/configui)

![Router Console UI Konfiguration](/images/router-console-config-ui.png)

Die UI-Konfigurationsseite ermöglicht es Ihnen, das Erscheinungsbild und die Zugänglichkeit Ihrer Router-Konsole anzupassen, einschließlich Theme-Auswahl, Spracheinstellungen und Passwortschutz.

**Router Console Theme:**

Wählen Sie zwischen dunklen und hellen Themes für die Router Console-Oberfläche: - **Dunkel** - Dunkelmodus-Theme (angenehmer für die Augen bei schlechten Lichtverhältnissen) - **Hell** - Hellmodus-Theme (traditionelles Erscheinungsbild)

Zusätzliche Theme-Optionen: - **Theme universell für alle Apps setzen** - Wendet das ausgewählte Theme auf alle I2P-Anwendungen an, nicht nur auf die Router-Konsole - **Mobile Konsole erzwingen** - Verwendet die mobiloptimierte Oberfläche auch in Desktop-Browsern - **E-Mail- und Torrent-Anwendungen in die Konsole einbetten** - Integriert Susimail und I2PSnark direkt in die Konsolenoberfläche, anstatt sie in separaten Tabs zu öffnen

**Router Console-Sprache:**

Wählen Sie Ihre bevorzugte Sprache für die Router-Konsolen-Oberfläche aus dem Dropdown-Menü aus. I2P unterstützt viele Sprachen, darunter Englisch, Deutsch, Französisch, Spanisch, Russisch, Chinesisch, Japanisch und weitere.

**Übersetzungsbeiträge willkommen:** Wenn Sie unvollständige oder falsche Übersetzungen bemerken, können Sie helfen, I2P zu verbessern, indem Sie zum Übersetzungsprojekt beitragen. Kontaktieren Sie die Entwickler in #i2p-dev auf IRC oder prüfen Sie den Übersetzungsstatusbericht (verlinkt auf der Seite).

**Router Console Passwort:**

Fügen Sie Benutzernamen- und Passwort-Authentifizierung hinzu, um den Zugriff auf Ihre Router-Konsole zu schützen:

- **Benutzername** - Geben Sie den Benutzernamen für den Konsolenzugriff ein
- **Passwort** - Geben Sie das Passwort für den Konsolenzugriff ein
- **Benutzer hinzufügen** - Erstellen Sie einen neuen Benutzer mit den angegebenen Anmeldedaten
- **Ausgewählte löschen** - Entfernen Sie vorhandene Benutzerkonten

**Warum ein Passwort hinzufügen?**

- Verhindert unbefugten lokalen Zugriff auf Ihre Router-Konsole
- Unverzichtbar, wenn mehrere Personen Ihren Computer nutzen
- Empfohlen, wenn Ihre Router-Konsole in Ihrem lokalen Netzwerk erreichbar ist
- Schützt Ihre I2P-Konfiguration und Datenschutzeinstellungen vor Manipulation

**Sicherheitshinweis:** Der Passwortschutz betrifft nur den Zugriff auf die Weboberfläche der Router-Konsole unter [I2P Router Console](http://127.0.0.1:7657). Er verschlüsselt weder den I2P-Verkehr noch hindert er Anwendungen daran, I2P zu nutzen. Wenn Sie der einzige Benutzer Ihres Computers sind und die Router-Konsole nur auf localhost lauscht (Standardeinstellung), ist ein Passwort möglicherweise nicht erforderlich.

### Router-Familien-Konfiguration

**URL:** [WebApp-Konfiguration](http://127.0.0.1:7657/configwebapps)

![Router Console WebApp-Konfiguration](/images/router-console-config-webapps.png)

Die WebApp-Konfigurationsseite ermöglicht es Ihnen, die Java-Webanwendungen zu verwalten, die innerhalb Ihres I2P-routers laufen. Diese Anwendungen werden vom webConsole-Client gestartet und laufen in derselben JVM wie der router, wodurch sie integrierte Funktionalität bereitstellen, die über die router-Konsole zugänglich ist.

**Was sind WebApps?**

WebApps sind Java-basierte Anwendungen, die sein können: - **Vollständige Anwendungen** (z.B. I2PSnark für Torrents) - **Front-ends für andere Clients**, die separat aktiviert werden müssen (z.B. Susidns, I2PTunnel) - **Webanwendungen ohne Weboberfläche** (z.B. Adressbuch)

**Wichtige Hinweise:**

- Eine Webapp kann vollständig deaktiviert werden oder nur vom Start beim Hochfahren ausgeschlossen werden
- Das Entfernen einer War-Datei aus dem Webapps-Verzeichnis deaktiviert die Webapp vollständig
- Allerdings werden die .war-Datei und das Webapp-Verzeichnis wieder erscheinen, wenn Sie Ihren Router auf eine neuere Version aktualisieren
- **Um eine Webapp dauerhaft zu deaktivieren:** Deaktivieren Sie sie hier, was die bevorzugte Methode ist

**Verfügbare WebApps:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Steuerung:**

Für jede Webapp: - **Beim Start ausführen?** - Kontrollkästchen zum Aktivieren/Deaktivieren des automatischen Starts - **Steuerung** - Start/Stopp-Schaltflächen für sofortige Kontrolle   - **Stopp** - Stoppt die aktuell laufende Webapp   - **Start** - Startet eine gestoppte Webapp

**Konfigurations-Buttons:**

- **Abbrechen** - Änderungen verwerfen und zur vorherigen Seite zurückkehren
- **WebApp-Konfiguration speichern** - Ihre Änderungen speichern und anwenden

**Anwendungsfälle:**

- Stoppe I2PSnark, wenn du keine Torrents verwendest, um Ressourcen zu sparen
- Deaktiviere jsonrpc, wenn du keinen API-Zugriff benötigst
- Stoppe Susimail, wenn du einen externen E-Mail-Client verwendest
- Stoppe Webapps vorübergehend, um Speicher freizugeben oder Probleme zu beheben

**Performance-Tipp:** Das Deaktivieren ungenutzter Webapps kann den Speicherverbrauch reduzieren und die Router-Performance verbessern, insbesondere auf Systemen mit begrenzten Ressourcen.

## Help

**URL:** [Hilfe](http://127.0.0.1:7657/help)

Die Hilfeseite bietet umfassende Dokumentation und Ressourcen, um Ihnen zu helfen, I2P effektiv zu verstehen und zu nutzen. Sie dient als zentrale Anlaufstelle für Fehlerbehebung, Lernen und Unterstützung.

**Was Sie finden werden:**

- **Schnellstart-Anleitung** - Wesentliche Informationen für neue Benutzer, die mit I2P beginnen
- **Häufig gestellte Fragen (FAQ)** - Antworten auf häufige Fragen zur I2P-Installation, -Konfiguration und -Nutzung
- **Fehlerbehebung** - Lösungen für häufige Probleme und Verbindungsschwierigkeiten
- **Technische Dokumentation** - Detaillierte Informationen über I2P-Protokolle, Architektur und Spezifikationen
- **Anwendungsleitfäden** - Anleitungen zur Verwendung von I2P-Anwendungen wie Torrents, E-Mail und versteckten Diensten
- **Netzwerkinformationen** - Verstehen, wie I2P funktioniert und was es sicher macht
- **Support-Ressourcen** - Links zu Foren, IRC-Kanälen und Community-Support

**Hilfe erhalten:**

Wenn Sie Probleme mit I2P haben: 1. Prüfen Sie die FAQ für häufig gestellte Fragen und Antworten 2. Sehen Sie sich den Abschnitt zur Fehlerbehebung für Ihr spezifisches Problem an 3. Besuchen Sie das I2P-Forum unter [i2pforum.i2p](http://i2pforum.i2p) oder [i2pforum.net](https://i2pforum.net) 4. Treten Sie dem IRC-Kanal #i2p für Community-Support in Echtzeit bei 5. Durchsuchen Sie die Dokumentation für detaillierte technische Informationen

**Tipp:** Die Hilfeseite ist immer über die Seitenleiste der Router-Konsole zugänglich, sodass Sie jederzeit problemlos Unterstützung finden können.

## Performance Graphs

**URL:** [Performance Graphs](http://127.0.0.1:7657/graphs)

![Router Console Performance Graphs](/images/router-console-graphs.png)

Die Seite „Performance-Graphen" bietet eine visuelle Echtzeitüberwachung der Leistung Ihres I2P-Routers und der Netzwerkaktivität. Diese Graphen helfen Ihnen, die Bandbreitennutzung, Peer-Verbindungen, den Speicherverbrauch und den allgemeinen Zustand des Routers zu verstehen.

**Verfügbare Graphen:**

- **Bandbreitennutzung**
  - **Low-Level-Senderate (Bytes/Sek.)** - Ausgehende Datenrate
  - **Low-Level-Empfangsrate (Bytes/Sek.)** - Eingehende Datenrate
  - Zeigt aktuelle, durchschnittliche und maximale Bandbreitenauslastung
  - Hilft zu überwachen, ob Sie sich Ihren konfigurierten Bandbreitengrenzen nähern

- **Aktive Peers**
  - **router.activePeers gemittelt über 60 Sek** - Anzahl der Peers, mit denen Sie aktiv kommunizieren
  - Zeigt den Zustand Ihrer Netzwerkverbindung
  - Mehr aktive Peers bedeuten in der Regel besseres Tunnel-Building und stärkere Netzwerkbeteiligung

- **Router-Speichernutzung**
  - **router.memoryUsed gemittelt über 60 Sek.** - JVM-Speicherverbrauch
  - Zeigt aktuelle, durchschnittliche und maximale Speichernutzung in MB an
  - Nützlich zur Identifizierung von Speicherlecks oder zur Bestimmung, ob die Java-Heap-Größe erhöht werden muss

**Graph-Anzeige konfigurieren:**

Passen Sie an, wie Diagramme angezeigt und aktualisiert werden:

- **Diagrammgröße** - Breite (Standard: 400 Pixel) und Höhe (Standard: 100 Pixel) festlegen
- **Anzeigezeitraum** - Anzuzeigender Zeitbereich (Standard: 60 Minuten)
- **Aktualisierungsintervall** - Wie oft die Diagramme aktualisiert werden (Standard: 5 Minuten)
- **Darstellungstyp** - Wahl zwischen Durchschnittswerten oder Ereignisanzeige
- **Legende ausblenden** - Legende aus Diagrammen entfernen, um Platz zu sparen
- **UTC** - UTC-Zeit anstelle der lokalen Zeit in Diagrammen verwenden
- **Persistenz** - Diagrammdaten auf Festplatte speichern für historische Analyse

**Erweiterte Optionen:**

Klicken Sie auf **[Select Stats]**, um auszuwählen, welche Statistiken grafisch dargestellt werden sollen: - Tunnel-Metriken (Build-Erfolgsrate, Tunnel-Anzahl, etc.) - netDb-Statistiken - Transport-Statistiken (NTCP2, SSU2) - Client-Tunnel-Performance - Und viele weitere detaillierte Metriken

**Anwendungsfälle:**

- Überwachen Sie die Bandbreite, um sicherzustellen, dass Sie Ihre konfigurierten Grenzwerte nicht überschreiten
- Überprüfen Sie die Peer-Konnektivität bei der Fehlersuche von Netzwerkproblemen
- Verfolgen Sie die Speichernutzung, um die Java-Heap-Einstellungen zu optimieren
- Identifizieren Sie Leistungsmuster im Zeitverlauf
- Diagnostizieren Sie Probleme beim Tunnel-Aufbau durch Korrelation der Graphen

**Tipp:** Klicken Sie auf „Einstellungen speichern und Graphen neu zeichnen", nachdem Sie Änderungen vorgenommen haben, um Ihre Konfiguration anzuwenden. Die Graphen werden automatisch basierend auf Ihrer Aktualisierungsverzögerung aktualisiert.
