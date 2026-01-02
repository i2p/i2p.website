---
title: "GitLab über I2P betreiben"
description: "GitLab innerhalb von I2P mit Docker und einem I2P-Router bereitstellen"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Das Hosting von GitLab innerhalb von I2P ist unkompliziert: Führen Sie den GitLab-Omnibus-Container aus, exponieren Sie ihn auf Loopback und leiten Sie den Datenverkehr durch einen I2P-Tunnel weiter. Die folgenden Schritte entsprechen der Konfiguration, die für `git.idk.i2p` verwendet wird, funktionieren aber für jede selbst gehostete Instanz.

## 1. Voraussetzungen

- Debian oder eine andere Linux-Distribution mit installiertem Docker Engine (`sudo apt install docker.io` oder `docker-ce` aus Dockers Repository).
- Ein I2P-router (Java I2P oder i2pd) mit ausreichend Bandbreite, um deine Benutzer zu bedienen.
- Optional: eine dedizierte VM, damit GitLab und der router von deiner Desktop-Umgebung isoliert bleiben.

## 2. GitLab-Image herunterladen

```bash
docker pull gitlab/gitlab-ce:latest
```
Das offizielle Image wird auf Basis von Ubuntu-Layern erstellt und regelmäßig aktualisiert. Prüfen Sie das [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile), falls Sie zusätzliche Sicherheit benötigen.

## 3. Entscheidung zwischen Bridging und I2P-Only

- **Nur-I2P**-Instanzen kontaktieren niemals Clearnet-Hosts. Benutzer können Repositories von anderen I2P-Diensten spiegeln, aber nicht von GitHub/GitLab.com. Dies maximiert die Anonymität.
- **Überbrückte** Instanzen greifen über einen HTTP-Proxy auf Clearnet-Git-Hosts zu. Dies ist nützlich, um öffentliche Projekte in I2P zu spiegeln, deanonymisiert jedoch die ausgehenden Anfragen des Servers.

Wenn Sie den Bridged-Modus wählen, konfigurieren Sie GitLab so, dass es einen I2P-HTTP-Proxy verwendet, der auf dem Docker-Host gebunden ist (zum Beispiel `http://172.17.0.1:4446`). Der Standard-Router-Proxy lauscht nur auf `127.0.0.1`; fügen Sie einen neuen Proxy-Tunnel hinzu, der an die Docker-Gateway-Adresse gebunden ist.

## 4. Starten Sie den Container

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- Binde die veröffentlichten Ports an Loopback; die I2P-Tunnel werden sie bei Bedarf verfügbar machen.
- Ersetze `/srv/gitlab/...` durch Speicherpfade, die zu deinem Host passen.

Sobald der Container läuft, besuchen Sie `https://127.0.0.1:8443/`, legen Sie ein Administrator-Passwort fest und konfigurieren Sie die Kontoeinschränkungen.

## 5. GitLab über I2P verfügbar machen

Erstellen Sie drei I2PTunnel **Server**-Tunnel:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Konfigurieren Sie jeden Tunnel mit angemessenen Tunnellängen und Bandbreite. Für öffentliche Instanzen sind 3 Hops mit 4–6 Tunneln pro Richtung ein guter Ausgangspunkt. Veröffentlichen Sie die resultierenden Base32/Base64-Ziele auf Ihrer Startseite, damit Benutzer Client-Tunnel konfigurieren können.

### Destination Enforcement

Wenn Sie HTTP(S)-Tunnel verwenden, aktivieren Sie die Zielerzwingung, damit nur der vorgesehene Hostname den Dienst erreichen kann. Dies verhindert, dass der Tunnel als generischer Proxy missbraucht wird.

## 6. Maintenance Tips

- Führen Sie `docker exec gitlab gitlab-ctl reconfigure` aus, wenn Sie GitLab-Einstellungen ändern.
- Überwachen Sie die Festplattennutzung (`/srv/gitlab/data`) – Git-Repositories wachsen schnell.
- Sichern Sie Konfigurations- und Datenverzeichnisse regelmäßig. GitLabs [Backup-Rake-Tasks](https://docs.gitlab.com/ee/raketasks/backup_restore.html) funktionieren innerhalb des Containers.
- Erwägen Sie, einen externen Monitoring-tunnel im Client-Modus einzurichten, um sicherzustellen, dass der Dienst vom breiteren Netzwerk aus erreichbar ist.

## 6. Wartungstipps

- [I2P in Ihre Anwendung einbetten](/docs/applications/embedding/)
- [Git über I2P (Client-Anleitung)](/docs/applications/git/)
- [Git-Bundles für Offline-/langsame Netzwerke](/docs/applications/git-bundle/)

Eine gut konfigurierte GitLab-Instanz bietet einen kollaborativen Entwicklungs-Hub vollständig innerhalb von I2P. Halten Sie den Router gesund, bleiben Sie mit GitLab-Sicherheitsupdates auf dem neuesten Stand und koordinieren Sie sich mit der Community, wenn Ihre Nutzerbasis wächst.
