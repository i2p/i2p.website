---
title: "Eine I2P Eepsite (Website im I2P-Netzwerk) erstellen"
description: "Erfahren Sie, wie Sie mithilfe des integrierten Jetty-Webservers Ihre eigene Website im I2P-Netzwerk erstellen und hosten"
lastUpdated: "2025-11"
toc: true
---

## Was ist ein Eepsite?

Eine **eepsite** ist eine Website, die ausschließlich im I2P-Netzwerk existiert. Im Gegensatz zu herkömmlichen Websites, die über das clearnet (öffentlich zugängliches Internet) erreichbar sind, sind eepsites nur über I2P erreichbar und bieten sowohl dem Seitenbetreiber als auch den Besuchern Anonymität und Privatsphäre. Eepsites verwenden die Pseudo-Top-Level-Domain `.i2p` und werden über spezielle `.b32.i2p`-Adressen oder über menschenlesbare Namen aufgerufen, die im I2P-Adressbuch registriert sind.

Alle Java-I2P-Installationen enthalten [Jetty](https://jetty.org/index.html), einen schlanken, Java-basierten Webserver, der bereits vorinstalliert und vorkonfiguriert ist. Das macht es einfach, innerhalb von Minuten Ihre eigene eepsite (I2P-Website) zu hosten - keine zusätzliche Softwareinstallation erforderlich.

Diese Anleitung führt Sie durch den Prozess der Erstellung und Konfiguration Ihrer ersten eepsite (eine über I2P erreichbare Website) mit den in I2P integrierten Werkzeugen.

---

## Schritt 1: Rufen Sie den Manager für versteckte Dienste auf

Der Hidden Services Manager (auch I2P Tunnel Manager genannt) ist der Ort, an dem Sie alle I2P-Server- und Client-tunnels konfigurieren, einschließlich HTTP-Servern (eepsites).

1. Öffnen Sie Ihre [I2P Router-Konsole](http://127.0.0.1:7657)
2. Navigieren Sie zum [Manager für versteckte Dienste](http://127.0.0.1:7657/i2ptunnelmgr)

Sie sollten die Oberfläche des Hidden Services Manager sehen, die Folgendes anzeigt: - **Statusmeldungen** - Aktueller Status von tunnel und Client - **Globale Steuerung für tunnel** - Schaltflächen zum gleichzeitigen Verwalten aller tunnels - **I2P-Verborgene Dienste** - Liste der konfigurierten Server-tunnels

![Manager für versteckte Dienste](/images/guides/eepsite/hidden-services-manager.png)

Standardmäßig sehen Sie einen vorhandenen Eintrag für den **I2P-Webserver**, der konfiguriert, aber nicht gestartet ist. Das ist der vorkonfigurierte Jetty-Webserver, der zur Verwendung bereit ist.

---

## Schritt 2: Konfigurieren Sie die Einstellungen Ihres Eepsite-Servers

Klicken Sie in der Liste der Hidden Services auf den Eintrag **I2P webserver**, um die Serverkonfigurationsseite zu öffnen. Hier passen Sie die Einstellungen Ihrer eepsite an.

![Eepsite Servereinstellungen](/images/guides/eepsite/webserver-settings.png)

### Erläuterung der Konfigurationsoptionen

**Name** - Dies ist ein interner Bezeichner für Ihren tunnel - Nützlich, wenn Sie mehrere eepsites betreiben, um den Überblick zu behalten, welche welche ist - Standard: "I2P webserver"

**Beschreibung** - Eine kurze Beschreibung Ihrer eepsite zur eigenen Orientierung - Nur für Sie im Hidden Services Manager (Verwaltung versteckter Dienste) sichtbar - Beispiel: "Meine eepsite" oder "Persönlicher Blog"

**Tunnel automatisch starten** - **Wichtig**: Aktivieren Sie dieses Kontrollkästchen, um Ihre eepsite automatisch zu starten, sobald Ihr I2P router startet - Stellt sicher, dass Ihre Website nach Neustarts des I2P router ohne manuelles Eingreifen verfügbar bleibt - Empfohlen: **Aktiviert**

**Ziel (Host und Port)** - **Host**: Die lokale Adresse, unter der Ihr Webserver läuft (Standard: `127.0.0.1`) - **Port**: Der Port, auf dem Ihr Webserver lauscht (Standard: `7658` für Jetty) - Wenn Sie den vorinstallierten Jetty-Webserver verwenden, **lassen Sie diese bei den Standardwerten** - Ändern Sie dies nur, wenn Sie einen benutzerdefinierten Webserver auf einem anderen Port betreiben

**Website-Hostname** - Dies ist der menschenlesbare `.i2p`-Domainname Ihrer eepsite - Standard: `mysite.i2p` (Platzhalter) - Sie können eine benutzerdefinierte Domain wie `stormycloud.i2p` oder `myblog.i2p` registrieren - Leer lassen, wenn Sie nur die automatisch generierte `.b32.i2p`-Adresse verwenden möchten (für outproxies (Ausgangsproxies)) - Siehe unten [Registrieren Ihrer I2P-Domain](#registering-your-i2p-domain) für Informationen dazu, wie Sie einen benutzerdefinierten Hostnamen registrieren

**Local Destination** (lokale Zielkennung) - Dies ist der eindeutige kryptografische Bezeichner Ihrer eepsite (Zieladresse) - Automatisch generiert, wenn der tunnel erstmals erstellt wird - Betrachten Sie dies als die permanente "IP-Adresse" Ihrer Website auf I2P - Die lange alphanumerische Zeichenfolge ist die `.b32.i2p`-Adresse Ihrer Website in kodierter Form

**Private-Schlüsseldatei** - Speicherort, an dem die privaten Schlüssel Ihrer eepsite gespeichert werden - Standard: `eepsite/eepPriv.dat` - **Bewahren Sie diese Datei sicher auf** - Jeder, der Zugriff auf diese Datei hat, kann sich als Ihre eepsite ausgeben - Geben Sie diese Datei niemals weiter oder löschen Sie sie

### Wichtiger Hinweis

Der gelbe Warnhinweis erinnert Sie daran, dass Sie zur Aktivierung der Funktionen zur QR-Code-Generierung oder Registrierungsauthentifizierung einen Website-Hostnamen mit der Endung `.i2p` konfigurieren müssen (z. B. `mynewsite.i2p`).

---

## Schritt 3: Erweiterte Netzwerkoptionen (optional)

Wenn Sie auf der Konfigurationsseite nach unten scrollen, finden Sie erweiterte Netzwerkoptionen. **Diese Einstellungen sind optional** - die Standardeinstellungen funktionieren für die meisten Benutzer gut. Sie können sie jedoch an Ihre Sicherheitsanforderungen und Leistungsanforderungen anpassen.

### Tunnel-Längenoptionen

![Optionen für Tunnel-Länge und -Anzahl](/images/guides/eepsite/tunnel-options.png)

**Tunnel-Länge** - **Standard**: 3-Hop tunnel (hohe Anonymität) - Steuert, wie viele Router-Hops eine Anfrage durchläuft, bevor sie Ihre eepsite erreicht - **Mehr Hops = höhere Anonymität, aber geringere Leistung** - **Weniger Hops = höhere Leistung, aber geringere Anonymität** - Optionen reichen von 0-3 Hops mit Varianz-Einstellungen - **Empfehlung**: Bei 3 Hops belassen, es sei denn, Sie haben spezielle Leistungsanforderungen

**Tunnel-Varianz** - **Standard**: 0 Hop-Varianz (keine Randomisierung, konstante Leistung) - Fügt der Tunnel-Länge eine Randomisierung hinzu, um die Sicherheit zu erhöhen - Beispiel: "0-1 Hop-Varianz" bedeutet, dass tunnels zufällig 3 oder 4 Hops lang sind - Erhöht die Unvorhersehbarkeit, kann jedoch zu uneinheitlichen Ladezeiten führen

### Optionen zur Anzahl der Tunnel

**Anzahl (eingehende/ausgehende Tunnels)** - **Standard**: 2 eingehende, 2 ausgehende tunnels (Standard-Bandbreite und -Zuverlässigkeit) - Bestimmt, wie viele parallele tunnels Ihrer eepsite zugewiesen sind - **Mehr tunnels = Bessere Verfügbarkeit und Lastbewältigung, aber höherer Ressourcenverbrauch** - **Weniger tunnels = Geringerer Ressourcenverbrauch, aber geringere Redundanz** - Empfohlen für die meisten Nutzer: 2/2 (Standard) - eepsites mit hohem Traffic können von 3/3 oder höher profitieren

**Anzahl der Backups** - **Standard**: 0 Backup tunnels (keine Redundanz, kein zusätzlicher Ressourcenverbrauch) - Standby tunnels, die aktiv werden, wenn primäre tunnels ausfallen - Erhöht die Zuverlässigkeit, verbraucht aber mehr Bandbreite und CPU - Die meisten persönlichen eepsites benötigen keine Backup tunnels

### POST-Grenzwerte

![Konfiguration der POST-Limits](/images/guides/eepsite/post-limits.png)

Wenn Ihre eepsite Formulare enthält (Kontaktformulare, Kommentarbereiche, Datei-Uploads usw.), können Sie Grenzwerte für POST-Anfragen konfigurieren, um Missbrauch zu verhindern:

**Grenzwerte pro Client** - **Pro Zeitraum**: Maximale Anzahl von Anfragen eines einzelnen Clients (Standard: 6 pro 5 Minuten) - **Sperrdauer**: Wie lange missbräuchliche Clients blockiert werden (Standard: 20 Minuten)

**Gesamtlimits** - **Gesamt**: Maximale Anzahl von POST-Anfragen aller Clients zusammen (Standard: 20 pro 5 Minuten) - **Sperrdauer**: Zeitraum, für den alle POST-Anfragen abgewiesen werden, wenn das Limit überschritten wurde (Standard: 10 Minuten)

**POST-Limit-Zeitraum** - Zeitfenster zur Messung der Anfrageraten (Standard: 5 Minuten)

Diese Beschränkungen helfen, Spam, Denial-of-Service-Angriffe und den Missbrauch automatisierter Formularübermittlungen zu verhindern.

### Wann erweiterte Einstellungen angepasst werden sollten

- **Community-Website mit hohem Traffic**: Erhöhe die Anzahl der tunnel (3-4 eingehend/ausgehend)
- **Performance-kritische Anwendung**: Reduziere die tunnel-Länge auf 2 Hops (Abwägung bei der Privatsphäre)
- **Maximale Anonymität erforderlich**: Behalte 3 Hops (Zwischenstationen) bei, füge 0-1 Varianz hinzu
- **Formulare mit legitimer hoher Nutzung**: Erhöhe die POST-Limits entsprechend
- **Persönlicher Blog/Portfolio**: Verwende alle Standardeinstellungen

---

## Schritt 4: Inhalte zu Ihrer Eepsite hinzufügen

Da Ihr eepsite nun konfiguriert ist, müssen Sie Ihre Website-Dateien (HTML, CSS, Bilder usw.) in das Document Root (Stammverzeichnis) des Webservers kopieren. Der Speicherort variiert je nach Betriebssystem, Installationsart und I2P-Implementierung.

### So finden Sie Ihr Document Root (Dokumentstammverzeichnis)

Das **Document-Root** (oft als `docroot` bezeichnet) ist der Ordner, in dem Sie alle Dateien Ihrer Website ablegen. Ihre Datei `index.html` sollte direkt in diesem Ordner liegen.

#### Java I2P (Standard-Distribution)

**Linux** - **Standardinstallation**: `~/.i2p/eepsite/docroot/` - **Paketinstallation (als Dienst ausgeführt)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **Standardinstallation**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - Typischer Pfad: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Installation als Windows-Dienst**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - Typischer Pfad: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **Standardinstallation**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (Erweiterte I2P-Distribution)

I2P+ verwendet die gleiche Verzeichnisstruktur wie Java I2P. Folgen Sie den oben genannten Pfaden entsprechend Ihrem Betriebssystem.

#### i2pd (C++-Implementierung)

**Linux/Unix** - **Standard**: `/var/lib/i2pd/eepsite/` oder `~/.i2pd/eepsite/` - Überprüfen Sie Ihre `i2pd.conf`-Konfigurationsdatei auf die tatsächliche `root`-Einstellung unter Ihrem HTTP-Server-tunnel

**Windows** - Prüfen Sie `i2pd.conf` in Ihrem i2pd-Installationsverzeichnis

**macOS** - Typischerweise: `~/Library/Application Support/i2pd/eepsite/`

### Hinzufügen Ihrer Website-Dateien

1. **Navigieren Sie zu Ihrem Dokumentstammverzeichnis** mithilfe Ihres Dateimanagers oder Terminals
2. **Erstellen oder kopieren Sie Ihre Website-Dateien** in den Ordner `docroot`
   - Erstellen Sie mindestens eine `index.html`-Datei (das ist Ihre Startseite)
   - Fügen Sie bei Bedarf CSS, JavaScript, Bilder und andere Assets hinzu
3. **Organisieren Sie Unterverzeichnisse** so, wie Sie es für jede Website tun:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### Schnellstart: Einfaches HTML-Beispiel

Wenn du gerade erst anfängst, erstelle eine einfache Datei `index.html` in deinem Ordner `docroot`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### Berechtigungen (Linux/Unix/macOS)

Wenn Sie I2P als Dienst oder unter einem anderen Benutzerkonto ausführen, stellen Sie sicher, dass der I2P-Prozess Lesezugriff auf Ihre Dateien hat:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### Tipps

- **Standardinhalt**: Wenn Sie I2P zum ersten Mal installieren, befindet sich bereits Beispielinhalt im Ordner `docroot` - Sie können ihn gerne ersetzen
- **Statische Websites funktionieren am besten**: Obwohl Jetty Servlets und JSP unterstützt, sind einfache HTML/CSS/JavaScript-Websites am leichtesten zu warten
- **Externe Webserver**: Fortgeschrittene Anwender können eigene Webserver (Apache, Nginx, Node.js usw.) auf unterschiedlichen Ports betreiben und den I2P tunnel auf diese verweisen

---

## Schritt 5: Ihre Eepsite starten

Jetzt, da Ihre eepsite konfiguriert ist und Inhalte enthält, ist es Zeit, sie zu starten und im I2P-Netzwerk zugänglich zu machen.

### Tunnel starten

1. **Kehren Sie zum [Manager für versteckte Dienste](http://127.0.0.1:7657/i2ptunnelmgr) zurück**
2. Suchen Sie den Eintrag Ihres **I2P-Webservers** in der Liste
3. Klicken Sie in der Spalte Control auf die Schaltfläche **Start**

![eepsite läuft](/images/guides/eepsite/eepsite-running.png)

### Warten auf den Tunnelaufbau

Nachdem Sie auf Start geklickt haben, wird Ihr eepsite tunnel aufgebaut. Dieser Vorgang dauert in der Regel **30-60 Sekunden**. Beobachten Sie die Statusanzeige:

- **Rotes Licht** = Tunnel wird gestartet/aufgebaut
- **Gelbes Licht** = Tunnel teilweise aufgebaut
- **Grünes Licht** = Tunnel voll funktionsfähig und bereit

Sobald du das **grüne Licht** siehst, ist deine eepsite im I2P-Netzwerk online!

### Auf Ihre Eepsite zugreifen

Klicken Sie auf die Schaltfläche **Preview** neben Ihrer laufenden eepsite. Dadurch öffnet sich ein neuer Browser-Tab mit der Adresse Ihrer eepsite.

Ihre eepsite hat zwei Arten von Adressen:

1. **Base32-Adresse (.b32.i2p)**: Eine lange kryptografische Adresse, die so aussieht:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - Dies ist die permanente, kryptografisch abgeleitete Adresse Ihrer eepsite
   - Sie kann nicht geändert werden und ist an Ihren privaten Schlüssel gebunden
   - Funktioniert immer, selbst ohne Domainregistrierung

2. **Menschenlesbare Domain (.i2p)**: Wenn Sie einen Website-Hostnamen festlegen (z. B. `testwebsite.i2p`)
   - Funktioniert erst nach der Domainregistrierung (siehe den nächsten Abschnitt)
   - Leichter zu merken und zu teilen
   - Verweist auf Ihre .b32.i2p-Adresse

Mit der Schaltfläche **Copy Hostname** können Sie Ihre vollständige `.b32.i2p`-Adresse schnell zum Weitergeben kopieren.

---

## ⚠️ Kritisch: Sichern Sie Ihren privaten Schlüssel

Bevor Sie fortfahren, **muss ein Backup der privaten Schlüsseldatei Ihrer eepsite erstellt werden**. Dies ist aus mehreren Gründen von entscheidender Bedeutung:

### Warum Ihren Schlüssel sichern?

**Ihr privater Schlüssel (`eepPriv.dat`) ist die Identität Ihrer eepsite.** Er bestimmt Ihre `.b32.i2p`-Adresse und weist die Inhaberschaft Ihrer eepsite nach.

- **Schlüssel = .b32-Adresse**: Ihr privater Schlüssel generiert mathematisch Ihre eindeutige .b32.i2p-Adresse
- **Kann nicht wiederhergestellt werden**: Wenn Sie Ihren Schlüssel verlieren, verlieren Sie die Adresse Ihrer eepsite dauerhaft
- **Kann nicht geändert werden**: Wenn Sie eine Domain registriert haben, die auf eine .b32-Adresse zeigt, **gibt es keine Möglichkeit, sie zu aktualisieren** - die Registrierung ist dauerhaft
- **Für die Migration erforderlich**: Der Umzug auf einen neuen Computer oder die Neuinstallation von I2P erfordert diesen Schlüssel, um dieselbe Adresse beizubehalten
- **Multihoming-Unterstützung**: (Betrieb eines Dienstes über mehrere Netzwerkpfade/Standorte) Das Betreiben Ihrer eepsite von mehreren Standorten erfordert denselben Schlüssel auf jedem Server

### Wo ist der private Schlüssel?

Standardmäßig wird Ihr privater Schlüssel gespeichert unter: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (oder `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat` für Service-Installationen) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` oder `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

Sie können diesen Pfad auch in Ihrer tunnel-Konfiguration unter "Private Key File" überprüfen/ändern.

### So erstellen Sie ein Backup

1. **Beenden Sie Ihren tunnel** (optional, aber sicherer)
2. **Kopieren Sie `eepPriv.dat`** an einen sicheren Ort:
   - Externer USB‑Datenträger
   - Verschlüsseltes Backup‑Laufwerk
   - Passwortgeschütztes Archiv
   - Sicherer Cloud‑Speicher (verschlüsselt)
3. **Bewahren Sie mehrere Backups auf** an verschiedenen physischen Standorten
4. **Geben Sie diese Datei niemals weiter** - jeder, der sie besitzt, kann sich als Ihre eepsite ausgeben

### Aus Sicherung wiederherstellen

So stellen Sie Ihre eepsite auf einem neuen System oder nach einer Neuinstallation wieder her:

1. Installiere I2P und erstelle/konfiguriere die Einstellungen für deinen tunnel
2. Stoppe den tunnel, bevor du den Schlüssel kopierst
3. Kopiere deine gesicherte `eepPriv.dat` an den richtigen Ort
4. Starte den tunnel - er verwendet deine ursprüngliche .b32-Adresse

---

## Wenn Sie keine Domain registrieren

**Herzlichen Glückwunsch!** Wenn Sie nicht vorhaben, einen benutzerdefinierten `.i2p`-Domainnamen zu registrieren, ist Ihre eepsite jetzt vollständig und einsatzbereit.

Du kannst: - Teile deine `.b32.i2p`-Adresse mit anderen - Greife über das I2P-Netzwerk mit jedem I2P-fähigen Browser auf deine Seite zu - Aktualisiere deine Website-Dateien jederzeit im Ordner `docroot` - Überwache deinen tunnel-Status im Hidden Services Manager

**Wenn du eine menschenlesbare Domain möchtest** (wie `mysite.i2p` statt einer langen .b32-Adresse), fahre mit dem nächsten Abschnitt fort.

---

## Registrierung Ihrer I2P-Domain

Eine menschenlesbare `.i2p`-Domain (wie `testwebsite.i2p`) ist viel leichter zu merken und zu teilen als eine lange `.b32.i2p`-Adresse. Die Domain-Registrierung ist kostenlos und verknüpft den von dir gewählten Namen mit der kryptografischen Adresse deiner eepsite (I2P-Website).

### Voraussetzungen

- Deine eepsite muss laufen und grün angezeigt werden
- In deiner tunnel-Konfiguration (Schritt 2) muss ein **Website-Hostname** festgelegt sein
- Beispiel: `testwebsite.i2p` oder `myblog.i2p`

### Schritt 1: Authentifizierungszeichenfolge generieren

1. **Kehren Sie zu Ihrer tunnel-Konfiguration zurück** im Manager für verborgene Dienste
2. Klicken Sie auf Ihren **I2P-Webserver**-Eintrag, um die Einstellungen zu öffnen
3. Scrollen Sie nach unten, um die Schaltfläche **Registrierungs-Authentifizierung** zu finden

![Authentifizierung bei der Registrierung](/images/guides/eepsite/registration-authentication.png)

4. Klicken Sie auf **Registration Authentication**
5. **Kopieren Sie die gesamte Authentifizierungszeichenfolge**, die für „Authentication for adding host [yourdomainhere]“ angezeigt wird

Die Authentifizierungszeichenfolge wird folgendermaßen aussehen:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
Diese Zeichenkette enthält: - Ihren Domainnamen (`testwebsite.i2p`) - Ihre Zieladresse (der lange kryptografische Bezeichner) - Einen Zeitstempel - Eine kryptografische Signatur, die nachweist, dass Sie den privaten Schlüssel besitzen

**Bewahre diese Authentifizierungszeichenfolge auf** - sie wird für beide Registrierungsdienste benötigt.

### Schritt 2: Bei stats.i2p registrieren

1. **Navigieren Sie zu** [stats.i2p Add Key](http://stats.i2p/i2p/addkey.html) (innerhalb von I2P)

![stats.i2p-Domainregistrierung](/images/guides/eepsite/stats-i2p-add.png)

2. **Fügen Sie die Authentifizierungszeichenkette ein** in das Feld "Authentication String"
3. **Fügen Sie Ihren Namen hinzu** (optional) - standardmäßig "Anonymous"
4. **Fügen Sie eine Beschreibung hinzu** (empfohlen) - beschreiben Sie kurz, worum es in Ihrer eepsite geht
   - Beispiel: "Neue I2P Eepsite", "Persönlicher Blog", "Dateifreigabedienst"
5. **"HTTP Service?" aktivieren**, wenn es sich um eine Website handelt (für die meisten eepsites aktiviert lassen)
   - Für IRC, NNTP, Proxys, XMPP, git usw. deaktivieren
6. Klicken Sie auf **Submit**

Wenn dies erfolgreich ist, sehen Sie eine Bestätigung, dass Ihre Domain dem stats.i2p-Adressbuch hinzugefügt wurde.

### Schritt 3: Bei reg.i2p registrieren

Um maximale Verfügbarkeit sicherzustellen, sollten Sie sich außerdem beim Dienst reg.i2p registrieren:

1. **Navigieren Sie zu** [reg.i2p Domain hinzufügen](http://reg.i2p/add) (innerhalb von I2P)

![reg.i2p Domain-Registrierung](/images/guides/eepsite/reg-i2p-add.png)

2. **Fügen Sie denselben Authentifizierungs-String ein** in das Feld "Auth string"
3. **Fügen Sie eine Beschreibung hinzu** (optional, aber empfohlen)
   - Dies hilft anderen I2P-Nutzern zu verstehen, was Ihre Website anbietet
4. Klicken Sie auf **Submit**

Sie sollten eine Bestätigung erhalten, dass Ihre Domain registriert wurde.

### Schritt 4: Auf die Verbreitung warten

Nach dem Einreichen bei beiden Diensten wird sich Ihre Domain-Registrierung über das Adressbuchsystem des I2P-Netzwerks verbreiten.

**Zeitplan der Verbreitung**: - **Erstregistrierung**: Sofort auf den Registrierungsdiensten - **Netzwerkweite Verbreitung**: Mehrere Stunden bis über 24 Stunden - **Volle Verfügbarkeit**: Kann bis zu 48 Stunden dauern, bis alle routers aktualisiert sind

**Das ist normal!** Das I2P-Adressbuchsystem aktualisiert sich in regelmäßigen Abständen, nicht sofort. Ihre eepsite funktioniert - andere Nutzer müssen lediglich das aktualisierte Adressbuch erhalten.

### Bestätigen Sie Ihre Domain

Nach einigen Stunden können Sie Ihre Domain testen:

1. **Öffne einen neuen Browser-Tab** in deinem I2P-Browser
2. Versuche, deine Domain direkt aufzurufen: `http://yourdomainname.i2p`
3. Wenn sie lädt, ist deine Domain registriert und wird im Netzwerk verbreitet!

Wenn es noch nicht funktioniert: - Warte länger (Adressbücher aktualisieren sich nach ihrem eigenen Zeitplan) - Das Adressbuch von deinem router benötigt eventuell Zeit, um sich zu synchronisieren - Versuche, deinen I2P router neu zu starten, um ein Adressbuch-Update zu erzwingen

### Wichtige Hinweise

- **Die Registrierung ist dauerhaft**: Sobald sie registriert und verbreitet wurde, verweist deine Domain dauerhaft auf deine `.b32.i2p`-Adresse
- **Ziel kann nicht geändert werden**: Du kannst nicht ändern, auf welche `.b32.i2p`-Adresse deine Domain zeigt - deshalb ist das Sichern von `eepPriv.dat` entscheidend
- **Domaininhaberschaft**: Nur der Inhaber des privaten Schlüssels kann die Domain registrieren oder aktualisieren
- **Kostenloser Dienst**: Die Domainregistrierung auf I2P ist kostenlos, von der Community betrieben und dezentral
- **Mehrere Registrare**: Die Registrierung sowohl bei stats.i2p als auch bei reg.i2p erhöht die Zuverlässigkeit und die Verbreitungsgeschwindigkeit

---

## Herzlichen Glückwunsch!

Ihre I2P eepsite ist jetzt mit einer registrierten Domain vollständig einsatzbereit!

**Nächste Schritte**: - Fügen Sie Ihrem `docroot`-Ordner mehr Inhalte hinzu - Teilen Sie Ihre Domain mit der I2P-Community - Bewahren Sie Ihr `eepPriv.dat`-Backup sicher auf - Überwachen Sie den tunnel-Status regelmäßig - Erwägen Sie, den I2P-Foren beizutreten oder auf IRC aktiv zu werden, um Ihre Website zu bewerben

Willkommen im I2P-Netzwerk! 🎉
