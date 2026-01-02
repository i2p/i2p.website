---
title: "SSH-Tunnel erstellen, um remote auf I2P zuzugreifen"
description: "Erfahren Sie, wie Sie sichere SSH-Tunnel unter Windows, Linux und Mac erstellen, um auf Ihren entfernten I2P-Router zuzugreifen"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Ein SSH-Tunnel bietet eine sichere, verschlüsselte Verbindung, um auf die Konsole Ihres entfernten I2P-Routers oder andere Dienste zuzugreifen. Diese Anleitung zeigt Ihnen, wie Sie SSH-Tunnels auf Windows-, Linux- und Mac-Systemen erstellen.

## Was ist ein SSH-Tunnel?

Ein SSH-Tunnel ist eine Methode, Daten und Informationen sicher über eine verschlüsselte SSH-Verbindung zu leiten. Man kann es sich wie eine geschützte "Pipeline" durch das Internet vorstellen - Ihre Daten bewegen sich durch diesen verschlüsselten Tunnel, wodurch verhindert wird, dass jemand sie unterwegs abfängt oder liest.

SSH-Tunneling ist besonders nützlich für:

- **Zugriff auf entfernte I2P-Router**: Verbindung zu Ihrer I2P-Konsole auf einem entfernten Server herstellen
- **Sichere Verbindungen**: Der gesamte Datenverkehr ist Ende-zu-Ende verschlüsselt
- **Umgehung von Einschränkungen**: Zugriff auf Dienste auf entfernten Systemen, als wären sie lokal
- **Portweiterleitung**: Einen lokalen Port auf einen entfernten Dienst abbilden

Im Kontext von I2P kannst du einen SSH-Tunnel verwenden, um auf deine I2P-Router-Konsole (üblicherweise auf Port 7657) auf einem entfernten Server zuzugreifen, indem du sie auf einen lokalen Port auf deinem Computer weiterleitest.

## Voraussetzungen

Bevor Sie einen SSH-Tunnel erstellen, benötigen Sie:

- **SSH-Client**:
  - Windows: [PuTTY](https://www.putty.org/) (kostenloser Download)
  - Linux/Mac: Integrierter SSH-Client (über Terminal)
- **Remote-Server-Zugriff**:
  - Benutzername für den Remote-Server
  - IP-Adresse oder Hostname des Remote-Servers
  - SSH-Passwort oder schlüsselbasierte Authentifizierung
- **Verfügbarer lokaler Port**: Wählen Sie einen ungenutzten Port zwischen 1-65535 (7657 wird üblicherweise für I2P verwendet)

## Den Tunnel-Befehl verstehen

Der SSH-Tunnel-Befehl folgt diesem Muster:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Parameter erklärt**: - **local_port**: Der Port auf Ihrem lokalen Rechner (z. B. 7657) - **destination_ip**: Normalerweise `127.0.0.1` (localhost auf dem entfernten Server) - **destination_port**: Der Port des Dienstes auf dem entfernten Server (z. B. 7657 für I2P) - **username**: Ihr Benutzername auf dem entfernten Server - **remote_server**: IP-Adresse oder Hostname des entfernten Servers

**Beispiel**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Dies erstellt einen Tunnel, bei dem: - Lokaler Port 7657 auf Ihrem Rechner weitergeleitet wird zu... - Port 7657 auf dem localhost des entfernten Servers (wo I2P läuft) - Verbindung als Benutzer `i2p` zum Server `20.228.143.58`

## SSH-Tunnel unter Windows erstellen

Windows-Benutzer können SSH-Tunnel mit PuTTY erstellen, einem kostenlosen SSH-Client.

### Step 1: Download and Install PuTTY

Laden Sie PuTTY von [putty.org](https://www.putty.org/) herunter und installieren Sie es auf Ihrem Windows-System.

### Step 2: Configure the SSH Connection

Öffnen Sie PuTTY und konfigurieren Sie Ihre Verbindung:

1. In der Kategorie **Session**:
   - Geben Sie die IP-Adresse oder den Hostnamen Ihres Remote-Servers in das Feld **Host Name** ein
   - Stellen Sie sicher, dass **Port** auf 22 gesetzt ist (Standard-SSH-Port)
   - Der Verbindungstyp sollte **SSH** sein

![PuTTY-Sitzungskonfiguration](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Navigieren Sie zu **Verbindung → SSH → Tunnel** in der linken Seitenleiste:

1. **Source-Port**: Geben Sie den lokalen Port ein, den Sie verwenden möchten (z.B. `7657`)
2. **Ziel**: Geben Sie `127.0.0.1:7657` ein (localhost:port auf dem entfernten Server)
3. Klicken Sie auf **Hinzufügen**, um den Tunnel hinzuzufügen
4. Der Tunnel sollte in der Liste "Weitergeleitete Ports" erscheinen

![PuTTY-Tunnel-Konfiguration](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Klicken Sie auf **Öffnen**, um die Verbindung herzustellen
2. Wenn Sie zum ersten Mal eine Verbindung herstellen, erscheint eine Sicherheitswarnung - klicken Sie auf **Ja**, um dem Server zu vertrauen
3. Geben Sie Ihren Benutzernamen ein, wenn Sie dazu aufgefordert werden
4. Geben Sie Ihr Passwort ein, wenn Sie dazu aufgefordert werden

![PuTTY-Verbindung hergestellt](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Sobald die Verbindung hergestellt ist, können Sie auf Ihre entfernte I2P-Konsole zugreifen, indem Sie einen Browser öffnen und zu `http://127.0.0.1:7657` navigieren

### Schritt 1: PuTTY herunterladen und installieren

Um eine erneute Konfiguration jedes Mal zu vermeiden:

1. Kehre zur Kategorie **Session** zurück
2. Gib einen Namen unter **Saved Sessions** ein (z.B. "I2P Tunnel")
3. Klicke auf **Save**
4. Beim nächsten Mal lade einfach diese Session und klicke auf **Open**

## Creating SSH Tunnels on Linux

Linux-Systeme haben SSH in das Terminal integriert, was die Erstellung von Tunneln schnell und unkompliziert macht.

### Schritt 2: SSH-Verbindung konfigurieren

Öffnen Sie ein Terminal und führen Sie den SSH-Tunnel-Befehl aus:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Ersetze**: - `7657` (erstes Vorkommen): Dein gewünschter lokaler Port - `127.0.0.1:7657`: Die Zieladresse und der Port auf dem entfernten Server - `i2p`: Dein Benutzername auf dem entfernten Server - `20.228.143.58`: Die IP-Adresse deines entfernten Servers

![Linux SSH tunnel creation](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Wenn Sie dazu aufgefordert werden, geben Sie Ihr Passwort ein. Sobald die Verbindung hergestellt ist, ist der Tunnel aktiv.

Greifen Sie auf Ihre entfernte I2P-Konsole unter `http://127.0.0.1:7657` in Ihrem Browser zu.

### Schritt 3: Tunnel konfigurieren

Der Tunnel bleibt aktiv, solange die SSH-Sitzung läuft. Um ihn im Hintergrund weiterlaufen zu lassen:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Zusätzliche Flags**: - `-f`: Führt SSH im Hintergrund aus - `-N`: Keine entfernten Befehle ausführen (nur Tunnel)

Um einen Hintergrund-Tunnel zu schließen, finden und beenden Sie den SSH-Prozess:

```bash
ps aux | grep ssh
kill [process_id]
```
### Schritt 4: Verbinden

Für bessere Sicherheit und Komfort verwenden Sie SSH-Schlüsselauthentifizierung:

1. Generiere ein SSH-Schlüsselpaar (falls du noch keines hast):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Kopieren Sie Ihren öffentlichen Schlüssel auf den entfernten Server:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Jetzt können Sie sich ohne Passwort verbinden:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Mac-Systeme verwenden denselben SSH-Client wie Linux, daher ist der Prozess identisch.

### Optional: Sitzung speichern

Öffnen Sie das Terminal (Programme → Dienstprogramme → Terminal) und führen Sie aus:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Ersetzen**: - `7657` (erstes Vorkommen): Ihr gewünschter lokaler Port - `127.0.0.1:7657`: Die Zieladresse und der Port auf dem Remote-Server - `i2p`: Ihr Benutzername auf dem Remote-Server - `20.228.143.58`: Die IP-Adresse Ihres Remote-Servers

![Mac SSH tunnel creation](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Geben Sie Ihr Passwort ein, wenn Sie dazu aufgefordert werden. Sobald die Verbindung hergestellt ist, greifen Sie auf Ihre Remote-I2P-Konsole unter `http://127.0.0.1:7657` zu

### Background Tunnels on Mac

Wie unter Linux kannst du den Tunnel im Hintergrund ausführen:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Verwendung des Terminals

Die Mac SSH-Schlüssel-Einrichtung ist identisch zu Linux:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Den Tunnel aktiv halten

Der häufigste Anwendungsfall - Zugriff auf Ihre entfernte I2P-Router-Konsole:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Öffnen Sie dann `http://127.0.0.1:7657` in Ihrem Browser.

### Verwendung von SSH-Keys (Empfohlen)

Mehrere Ports gleichzeitig weiterleiten:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Dies leitet sowohl Port 7657 (I2P-Konsole) als auch 7658 (ein anderer Dienst) weiter.

### Custom Local Port

Verwenden Sie einen anderen lokalen Port, falls 7657 bereits verwendet wird:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Greifen Sie stattdessen auf die I2P-Konsole unter `http://127.0.0.1:8080` zu.

## Troubleshooting

### Verwendung des Terminals

**Fehler**: "bind: Address already in use"

**Lösung**: Wählen Sie einen anderen lokalen Port oder beenden Sie den Prozess, der diesen Port verwendet:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Hintergrund-Tunnel auf Mac

**Fehler**: "Connection refused" oder "channel 2: open failed"

**Mögliche Ursachen**: - Der entfernte Dienst läuft nicht (prüfen Sie, ob der I2P-router auf dem entfernten Server läuft) - Firewall blockiert die Verbindung - Falscher Zielport

**Lösung**: Überprüfen Sie, ob der I2P-Router auf dem entfernten Server läuft:

```bash
ssh user@remote-server "systemctl status i2p"
```
### SSH-Schlüssel-Einrichtung auf Mac

**Fehler**: "Permission denied" oder "Authentication failed"

**Mögliche Ursachen**: - Falscher Benutzername oder Passwort - SSH-Schlüssel nicht korrekt konfiguriert - SSH-Zugriff auf dem Remote-Server deaktiviert

**Lösung**: Überprüfen Sie die Zugangsdaten und stellen Sie sicher, dass der SSH-Zugriff auf dem Remote-Server aktiviert ist.

### Tunnel Drops Connection

**Fehler**: Verbindung bricht nach einer Phase der Inaktivität ab

**Lösung**: Fügen Sie Keep-Alive-Einstellungen zu Ihrer SSH-Konfiguration (`~/.ssh/config`) hinzu:

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **SSH-Schlüssel verwenden**: Sicherer als Passwörter, schwerer zu kompromittieren
- **Passwort-Authentifizierung deaktivieren**: Sobald SSH-Schlüssel eingerichtet sind, Passwort-Login auf dem Server deaktivieren
- **Starke Passwörter verwenden**: Bei Verwendung von Passwort-Authentifizierung ein starkes, einzigartiges Passwort nutzen
- **SSH-Zugriff einschränken**: Firewall-Regeln konfigurieren, um SSH-Zugriff auf vertrauenswürdige IPs zu beschränken
- **SSH aktuell halten**: SSH-Client und Server-Software regelmäßig aktualisieren
- **Logs überwachen**: SSH-Logs auf dem Server auf verdächtige Aktivitäten überprüfen
- **Nicht-standardmäßige SSH-Ports verwenden**: Standard-SSH-Port (22) ändern, um automatisierte Angriffe zu reduzieren

## SSH-Tunnel unter Linux erstellen

### Zugriff auf die I2P-Konsole

Erstellen Sie ein Skript, um automatisch Tunnel einzurichten:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Machen Sie es ausführbar:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Mehrere Tunnel

Erstelle einen systemd-Dienst für die automatische Tunnel-Erstellung:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Hinzufügen:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
Aktivieren und starten:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Benutzerdefinierter lokaler Port

Erstellen Sie einen SOCKS-Proxy für dynamisches Forwarding:

```bash
ssh -D 8080 user@remote-server
```
Konfigurieren Sie Ihren Browser, um `127.0.0.1:8080` als SOCKS5-Proxy zu verwenden.

### Reverse Tunneling

Erlaube dem entfernten Server, auf Dienste auf deinem lokalen Rechner zuzugreifen:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Port bereits in Verwendung

Tunnel durch einen Zwischenserver:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH-Tunneling ist ein leistungsstarkes Werkzeug für den sicheren Zugriff auf entfernte I2P-router und andere Dienste. Egal ob Sie Windows, Linux oder Mac verwenden, der Prozess ist unkompliziert und bietet starke Verschlüsselung für Ihre Verbindungen.

Für zusätzliche Hilfe oder Fragen besuchen Sie die I2P-Community: - **Forum**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p auf verschiedenen Netzwerken - **Dokumentation**: [I2P Docs](/docs/)

*Anleitung ursprünglich erstellt von [Stormy Cloud](https://www.stormycloud.org), angepasst für die I2P-Dokumentation.*
