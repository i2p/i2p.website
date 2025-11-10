---
title: "Gitlab-Setup über I2P"
date: 2020-03-16
author: "idk"
description: "Spiegle I2P-Git-Repositories und überbrücke Clearnet-Repositories für andere"
categories: ["development"]
---

Dies ist der Einrichtungsprozess, den ich für die Konfiguration von Gitlab und I2P verwende, wobei Docker zum Verwalten des Dienstes selbst zum Einsatz kommt. Gitlab lässt sich auf diese Weise sehr leicht auf I2P hosten; es kann ohne große Schwierigkeiten von einer einzelnen Person administriert werden. Diese Anleitung sollte auf jedem Debian-basierten System funktionieren und lässt sich problemlos auf jedes System übertragen, auf dem Docker und ein I2P router verfügbar sind.

## Abhängigkeiten und Docker

Da Gitlab in einem Container läuft, müssen wir auf unserem Hauptsystem nur die für den Container erforderlichen Abhängigkeiten installieren. Praktischerweise können Sie alles Nötige mit folgendem installieren:

```
sudo apt install docker.io
```
## Docker-Container abrufen

Sobald Sie Docker installiert haben, können Sie die für GitLab benötigten Docker-Container abrufen. *Führen Sie sie noch nicht aus.*

```
docker pull gitlab/gitlab-ce
```
## I2P-HTTP-Proxy für Gitlab einrichten (Wichtige Informationen, optionale Schritte)

Gitlab-Server innerhalb von I2P können mit oder ohne die Möglichkeit betrieben werden, mit Servern im Internet außerhalb von I2P zu interagieren. In dem Fall, dass es dem Gitlab-Server *nicht erlaubt* ist, mit Servern außerhalb von I2P zu interagieren, kann er nicht deanonymisiert werden, indem ein Git-Repository von einem Git-Server im Internet außerhalb von I2P geklont wird.

In dem Fall, dass es dem Gitlab-Server *erlaubt* ist, mit Servern außerhalb von I2P zu interagieren, kann er als "Bridge" für die Nutzer fungieren, die ihn dazu verwenden können, Inhalte außerhalb von I2P auf eine über I2P zugängliche Quelle zu spiegeln, allerdings *ist er in diesem Fall nicht anonym*.

**Wenn Sie eine nicht anonyme Gitlab-Instanz im Bridge-Modus mit Zugriff auf Web-Repositories möchten**, ist keine weitere Änderung erforderlich.

**Wenn Sie eine reine I2P-Gitlab-Instanz ohne Zugriff auf reine Web-Repositories haben möchten**, müssen Sie Gitlab so konfigurieren, dass es einen I2P HTTP-Proxy verwendet. Da der standardmäßige I2P HTTP-Proxy nur auf `127.0.0.1` lauscht, müssen Sie einen neuen für Docker einrichten, der auf der Host/Gateway-Adresse des Docker-Netzwerks lauscht, die üblicherweise `172.17.0.1` ist. Ich konfiguriere meinen auf Port `4446`.

## Starten Sie den Container lokal

Sobald Sie das eingerichtet haben, können Sie den Container starten und Ihre Gitlab-Instanz lokal verfügbar machen:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Besuchen Sie Ihre lokale GitLab-Instanz und richten Sie Ihr Admin-Konto ein. Wählen Sie ein starkes Passwort und konfigurieren Sie die Limits für Benutzerkonten entsprechend Ihren Ressourcen.

## Richten Sie Ihre Service tunnels ein und registrieren Sie einen Hostnamen

Sobald Sie Gitlab lokal eingerichtet haben, wechseln Sie zur I2P Router-Konsole. Sie müssen zwei Server tunnels einrichten, einen zur Gitlab-Web(HTTP)-Schnittstelle auf TCP-Port 8080 und einen zur Gitlab-SSH-Schnittstelle auf TCP-Port 8022.

### Gitlab Web(HTTP) Interface

Für die Weboberfläche verwenden Sie einen "HTTP" server tunnel. Von http://127.0.0.1:7657/i2ptunnelmgr starten Sie den "New Tunnel Wizard" und geben Sie die folgenden Werte ein:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Für die SSH-Schnittstelle verwenden Sie einen "Standard" server tunnel. Von http://127.0.0.1:7657/i2ptunnelmgr starten Sie den "New Tunnel Wizard" und geben Sie die folgenden Werte ein:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Wenn Sie entweder `gitlab.rb` geändert oder einen Hostnamen registriert haben, müssen Sie den GitLab-Dienst neu starten, damit die Einstellungen wirksam werden.
