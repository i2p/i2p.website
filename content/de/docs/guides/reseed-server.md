---
title: "Erstellen und Betreiben eines I2P-Reseed-Servers"
description: "Vollständige Anleitung zum Einrichten und Betreiben eines I2P-reseed-Servers, um neuen Routern den Netzwerkbeitritt zu ermöglichen"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed-Hosts sind entscheidende Infrastruktur für das I2P-Netzwerk und versorgen neue Router während des Bootstrap-Prozesses mit einer initialen Gruppe von Knoten. Diese Anleitung führt Sie durch die Einrichtung und den Betrieb Ihres eigenen Reseed-Servers.

## Was ist ein I2P Reseed Server?

Ein I2P-Reseed-Server hilft dabei, neue Router in das I2P-Netzwerk zu integrieren, indem er:

- **Bereitstellung der initialen Peer-Erkennung**: Neue Router erhalten eine Anfangsgruppe von Netzwerkknoten, zu denen sie sich verbinden können
- **Bootstrap-Wiederherstellung**: Unterstützung von Routern, die Schwierigkeiten haben, Verbindungen aufrechtzuerhalten
- **Sichere Verteilung**: Der Reseeding-Prozess ist verschlüsselt und digital signiert, um die Netzwerksicherheit zu gewährleisten

Wenn ein neuer I2P-Router zum ersten Mal startet (oder alle seine Peer-Verbindungen verloren hat), kontaktiert er Reseed-Server, um einen initialen Satz von Router-Informationen herunterzuladen. Dies ermöglicht es dem neuen Router, seine eigene netDb aufzubauen und Tunnels zu etablieren.

## Voraussetzungen

Bevor Sie beginnen, benötigen Sie:

- Ein Linux-Server (Debian/Ubuntu empfohlen) mit Root-Zugriff
- Ein Domain-Name, der auf Ihren Server verweist
- Mindestens 1 GB RAM und 10 GB Festplattenspeicher
- Ein laufender I2P router auf dem Server, um die netDb zu befüllen
- Grundkenntnisse in der Linux-Systemadministration

## Vorbereitung des Servers

### Step 1: Update System and Install Dependencies

Aktualisieren Sie zunächst Ihr System und installieren Sie die erforderlichen Pakete:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Dies installiert: - **golang-go**: Go-Programmiersprache-Laufzeitumgebung - **git**: Versionsverwaltungssystem - **make**: Build-Automatisierungswerkzeug - **docker.io & docker-compose**: Container-Plattform zum Ausführen von Nginx Proxy Manager

![Installation der erforderlichen Pakete](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Klonen Sie das reseed-tools-Repository und erstellen Sie die Anwendung:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
Das `reseed-tools`-Paket stellt die Kernfunktionalität für den Betrieb eines Reseed-Servers bereit. Es verarbeitet: - Sammeln von Router-Informationen aus Ihrer lokalen Netzwerkdatenbank - Verpacken der Router-Informationen in signierte SU3-Dateien - Bereitstellen dieser Dateien über HTTPS

![Klonen des reseed-tools-Repository](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Generieren Sie das SSL-Zertifikat und den privaten Schlüssel Ihres Reseed-Servers:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Wichtige Parameter**: - `--signer`: Ihre E-Mail-Adresse (ersetzen Sie `admin@stormycloud.org` durch Ihre eigene) - `--netdb`: Pfad zur netDb Ihres I2P-Routers - `--port`: Interner Port (8443 wird empfohlen) - `--ip`: An localhost binden (wir werden einen Reverse Proxy für öffentlichen Zugriff verwenden) - `--trustProxy`: X-Forwarded-For-Headern vom Reverse Proxy vertrauen

Der Befehl generiert: - Einen privaten Schlüssel zum Signieren von SU3-Dateien - Ein SSL-Zertifikat für sichere HTTPS-Verbindungen

![SSL-Zertifikat-Generierung](/images/guides/reseed/reseed_03.png)

### Schritt 1: System aktualisieren und Abhängigkeiten installieren

**Kritisch**: Sichern Sie die generierten Schlüssel in `/home/i2p/.reseed/` sicher:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Speichern Sie dieses Backup an einem sicheren, verschlüsselten Ort mit eingeschränktem Zugriff. Diese Schlüssel sind für den Betrieb Ihres Reseed-Servers unerlässlich und sollten sorgfältig geschützt werden.

## Configuring the Service

### Schritt 2: Reseed Tools klonen und kompilieren

Erstelle einen systemd-Dienst, um den Reseed-Server automatisch auszuführen:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**Denken Sie daran, zu ersetzen** `admin@stormycloud.org` durch Ihre eigene E-Mail-Adresse.

Aktivieren und starten Sie nun den Dienst:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Überprüfen Sie, ob der Dienst läuft:

```bash
sudo systemctl status reseed
```
![Überprüfung des Reseed-Service-Status](/images/guides/reseed/reseed_04.png)

### Schritt 3: SSL-Zertifikat generieren

Für optimale Leistung sollten Sie den Reseed-Dienst regelmäßig neu starten, um die Router-Informationen zu aktualisieren:

```bash
sudo crontab -e
```
Fügen Sie diese Zeile hinzu, um den Dienst alle 3 Stunden neu zu starten:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

Der Reseed-Server läuft auf localhost:8443 und benötigt einen Reverse Proxy, um öffentlichen HTTPS-Traffic zu verarbeiten. Wir empfehlen Nginx Proxy Manager aufgrund seiner einfachen Bedienung.

### Schritt 4: Sichern Sie Ihre Schlüssel

Nginx Proxy Manager mit Docker bereitstellen:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
Dies exponiert: - **Port 80**: HTTP-Verkehr - **Port 81**: Admin-Oberfläche - **Port 443**: HTTPS-Verkehr

### Configure Proxy Manager

1. Greifen Sie auf die Admin-Oberfläche unter `http://your-server-ip:81` zu

2. Mit Standard-Zugangsdaten anmelden:
   - **E-Mail**: admin@example.com
   - **Passwort**: changeme

**Wichtig**: Ändern Sie diese Zugangsdaten sofort nach der ersten Anmeldung!

![Nginx Proxy Manager Login](/images/guides/reseed/reseed_05.png)

3. Navigieren Sie zu **Proxy Hosts** und klicken Sie auf **Add Proxy Host**

![Hinzufügen eines Proxy-Hosts](/images/guides/reseed/reseed_06.png)

4. Konfigurieren Sie den Proxy-Host:
   - **Domain Name**: Ihre Reseed-Domain (z. B. `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - Aktivieren Sie **Cache Assets**
   - Aktivieren Sie **Block Common Exploits**
   - Aktivieren Sie **Websockets Support**

![Konfigurieren der Proxy-Host-Details](/images/guides/reseed/reseed_07.png)

5. Im Tab **SSL**:
   - Wählen Sie **Request a new SSL Certificate** (Let's Encrypt)
   - Aktivieren Sie **Force SSL**
   - Aktivieren Sie **HTTP/2 Support**
   - Stimmen Sie den Let's Encrypt Nutzungsbedingungen zu

![SSL-Zertifikatskonfiguration](/images/guides/reseed/reseed_08.png)

6. Klicken Sie auf **Speichern**

Ihr Reseed-Server sollte nun unter `https://reseed.example.com` erreichbar sein

![Erfolgreiche Reseed-Server-Konfiguration](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Sobald Ihr Reseed-Server betriebsbereit ist, kontaktieren Sie die I2P-Entwickler, um ihn zur offiziellen Reseed-Server-Liste hinzufügen zu lassen.

### Schritt 5: Systemd-Dienst erstellen

Senden Sie eine E-Mail an **zzz** (I2P Lead Developer) mit den folgenden Informationen:

- **I2P E-Mail**: zzz@mail.i2p
- **Clearnet E-Mail**: zzz@i2pmail.org

### Schritt 6: Optional - Periodische Neustarts konfigurieren

Fügen Sie in Ihre E-Mail ein:

1. **Reseed-Server-URL**: Die vollständige HTTPS-URL (z.B. `https://reseed.example.com`)
2. **Öffentliches Reseed-Zertifikat**: Befindet sich unter `/home/i2p/.reseed/` (`.crt`-Datei anhängen)
3. **Kontakt-E-Mail**: Ihre bevorzugte Kontaktmethode für Benachrichtigungen zur Serverwartung
4. **Serverstandort**: Optional, aber hilfreich (Land/Region)
5. **Erwartete Verfügbarkeit**: Ihre Verpflichtung zur Wartung des Servers

### Verification

Die I2P-Entwickler werden überprüfen, dass Ihr Reseed-Server: - Ordnungsgemäß konfiguriert ist und Router-Informationen bereitstellt - Gültige SSL-Zertifikate verwendet - Korrekt signierte SU3-Dateien bereitstellt - Erreichbar und reaktionsfähig ist

Sobald genehmigt, wird Ihr Reseed-Server zur Liste hinzugefügt, die mit I2P-Routern verteilt wird, und hilft neuen Benutzern, dem Netzwerk beizutreten!

## Monitoring and Maintenance

### Nginx Proxy Manager installieren

Überwachen Sie Ihren Reseed-Dienst:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Proxy Manager konfigurieren

Behalten Sie die Systemressourcen im Auge:

```bash
htop
df -h
```
### Update Reseed Tools

Aktualisieren Sie die reseed-tools regelmäßig, um die neuesten Verbesserungen zu erhalten:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Kontaktinformationen

Wenn Sie Let's Encrypt über Nginx Proxy Manager verwenden, werden Zertifikate automatisch erneuert. Überprüfen Sie, ob die Erneuerung funktioniert:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Konfiguration des Dienstes

### Erforderliche Informationen

Prüfen Sie die Logs auf Fehler:

```bash
sudo journalctl -u reseed -n 50
```
Häufige Probleme: - I2P router läuft nicht oder die netDb ist leer - Port 8443 wird bereits verwendet - Berechtigungsprobleme mit dem Verzeichnis `/home/i2p/.reseed/`

### Verifizierung

Stellen Sie sicher, dass Ihr I2P-Router läuft und seine Netzwerkdatenbank gefüllt hat:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Sie sollten viele `.dat`-Dateien sehen. Falls leer, warten Sie, bis Ihr I2P-Router Peers entdeckt hat.

### SSL Certificate Errors

Überprüfen Sie, ob Ihre Zertifikate gültig sind:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Dienststatus überprüfen

Überprüfen Sie: - DNS-Einträge zeigen korrekt auf Ihren Server - Firewall erlaubt Ports 80 und 443 - Nginx Proxy Manager läuft: `docker ps`

## Security Considerations

- **Halten Sie Ihre privaten Schlüssel sicher**: Teilen oder exponieren Sie niemals den Inhalt von `/home/i2p/.reseed/`
- **Regelmäßige Updates**: Halten Sie Systempakete, Docker und reseed-tools aktuell
- **Überwachen Sie Logs**: Achten Sie auf verdächtige Zugriffsmuster
- **Rate Limiting**: Erwägen Sie die Implementierung von Rate Limiting, um Missbrauch zu verhindern
- **Firewall-Regeln**: Exponieren Sie nur notwendige Ports (80, 443, 81 für Admin)
- **Admin-Interface**: Beschränken Sie das Nginx Proxy Manager Admin-Interface (Port 81) auf vertrauenswürdige IPs

## Contributing to the Network

Indem Sie einen Reseed-Server betreiben, stellen Sie kritische Infrastruktur für das I2P-Netzwerk bereit. Vielen Dank, dass Sie zu einem privateren und dezentraleren Internet beitragen!

Bei Fragen oder für Unterstützung wenden Sie sich an die I2P-Community: - **Forum**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p in verschiedenen Netzwerken - **Entwicklung**: [i2pgit.org](https://i2pgit.org)

---

*Anleitung ursprünglich erstellt von [Stormy Cloud](https://www.stormycloud.org), angepasst für die I2P-Dokumentation.*
