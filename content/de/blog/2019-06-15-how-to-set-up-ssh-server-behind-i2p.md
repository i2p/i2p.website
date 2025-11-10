---
title: "So richten Sie einen SSH-Server hinter I2P für den persönlichen Zugriff ein"
date: 2019-06-15
author: "idk"
description: "SSH über I2P"
---

# So richten Sie einen SSH-Server hinter I2P für den persönlichen Zugriff ein

Dies ist ein Tutorial, wie man einen I2P tunnel einrichtet und anpasst, um aus der Ferne auf einen SSH-Server zuzugreifen, entweder mit I2P oder i2pd. Vorerst wird angenommen, dass Sie Ihren SSH-Server über einen Paketmanager installieren und dass er als Dienst läuft.

Überlegungen: In dieser Anleitung setze ich einiges voraus. Diese müssen je nach den Komplikationen, die in Ihrer konkreten Umgebung auftreten, angepasst werden, insbesondere wenn Sie zur Isolierung VMs oder Container verwenden. Dabei wird davon ausgegangen, dass der I2P router und der SSH-Server auf demselben localhost laufen. Sie sollten neu erzeugte SSH-Hostschlüssel verwenden, entweder durch die Verwendung eines frisch installierten sshd oder indem Sie alte Schlüssel löschen und ihre Neuerzeugung erzwingen. Zum Beispiel:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Verwenden Sie die Weboberfläche von Java I2P, navigieren Sie zum [Manager für versteckte Dienste](http://127.0.0.1:7657/i2ptunnelmgr) und starten Sie den tunnel-Assistenten.

#### Tunnel Wizard

Da Sie diesen tunnel für den SSH-Server einrichten, müssen Sie den tunnel-Typ "Server" auswählen.

**Screenshot-Platzhalter:** Verwenden Sie den Assistenten, um einen "Server" tunnel zu erstellen

Sie sollten es später feinabstimmen, aber der Standard-Tunnel-Typ ist für den Einstieg am einfachsten.

**Screenshot-Platzhalter:** Von der „Standard“-Variante

Geben Sie eine aussagekräftige Beschreibung an:

**Screenshot-Platzhalter:** Beschreiben Sie, wozu er dient

And tell it where the SSH server will be available.

**Screenshot-Platzhalter:** Geben Sie als Ziel den zukünftigen Standort Ihres SSH-Servers an

Überprüfen Sie die Ergebnisse und speichern Sie Ihre Einstellungen.

**Screenshot-Platzhalter:** Speichern Sie die Einstellungen.

#### Advanced Settings

Kehren Sie nun zum Hidden Services Manager zurück und sehen Sie sich die verfügbaren erweiterten Einstellungen an. Eine Sache, die Sie auf jeden Fall ändern sollten, ist, die Konfiguration auf interaktive Verbindungen statt auf Bulk-Verbindungen (Massenübertragungen) einzustellen.

**Screenshot-Platzhalter:** Konfigurieren Sie Ihren tunnel für interaktive Verbindungen

Außerdem können diese weiteren Optionen die Leistung beim Zugriff auf Ihren SSH-Server beeinflussen. Wenn Ihnen Ihre Anonymität nicht ganz so wichtig ist, könnten Sie die Anzahl der Hops (Zwischenstationen) verringern. Wenn Sie Geschwindigkeitsprobleme haben, könnten mehr tunnel helfen. Ein paar Backup-tunnel sind wahrscheinlich eine gute Idee. Eventuell müssen Sie das ein wenig feinjustieren.

**Screenshot-Platzhalter:** Wenn Ihnen Anonymität nicht wichtig ist, dann verringern Sie die Tunnel-Länge.

Starten Sie abschließend den tunnel neu, damit alle Ihre Einstellungen wirksam werden.

Eine weitere interessante Einstellung, besonders wenn Sie sich entscheiden, eine hohe Anzahl von tunnels zu betreiben, ist "Reduce on Idle", welche die Anzahl der laufenden tunnels reduziert, wenn der Server über einen längeren Zeitraum inaktiv war.

**Screenshot-Platzhalter:** Bei Inaktivität reduzieren, wenn Sie eine hohe Anzahl von tunnels gewählt haben

### Using i2pd

Mit i2pd erfolgt die gesamte Konfiguration über Dateien statt über eine Weboberfläche. Um für i2pd einen tunnel für einen SSH‑Dienst zu konfigurieren, passen Sie die folgenden Beispieleinstellungen an Ihre Anforderungen an Anonymität und Leistung an und kopieren Sie sie in tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Schritt 1: I2P tunnel für SSH-Server einrichten

Je nachdem, wie du auf deinen SSH-Server zugreifen möchtest, willst du vielleicht ein paar Einstellungen anpassen. Neben den offensichtlichen SSH-Hardening-Maßnahmen, die du auf allen SSH-Servern umsetzen solltest (Public-Key-Authentifizierung, keine Anmeldung als root, etc.), gilt: Wenn dein SSH-Server auf keiner anderen Adresse als deinem Server tunnel lauschen soll, solltest du AddressFamily auf inet und ListenAddress auf 127.0.0.1 setzen.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Wenn Sie sich dafür entscheiden, für Ihren SSH-Server einen anderen Port als 22 zu verwenden, müssen Sie den Port in Ihrer I2P tunnel-Konfiguration ändern.

## Step Three: Set up I2P tunnel for SSH Client

Sie müssen die I2P router console des SSH-Servers aufrufen können, um Ihre Client-Verbindung zu konfigurieren. Ein praktischer Vorteil dieses Setups ist, dass die anfängliche Verbindung zum I2P tunnel authentifiziert ist, was das Risiko etwas verringert, dass Ihre erste Verbindung zum SSH-Server durch einen Man-in-the-Middle-Angriff (MITM) abgefangen oder manipuliert wird, wie es in Trust-On-First-Use (Vertrauen beim ersten Kontakt) Szenarien ein Risiko darstellt.

### Verwendung von Java I2P

#### Tunnel-Assistent

Zuerst starten Sie den Konfigurationsassistenten für tunnel über den Manager für versteckte Dienste und wählen Sie einen Client-tunnel aus.

**Platzhalter für Screenshot:** Verwenden Sie den Assistenten, um einen Client-Tunnel zu erstellen

Wählen Sie als Nächstes den Standardtyp für den tunnel. Diese Konfiguration werden Sie später noch feinabstimmen.

**Screenshot placeholder:** Von der Standardvariante

Geben Sie eine gute Beschreibung an.

**Screenshot-Platzhalter:** Geben Sie eine aussagekräftige Beschreibung

Das ist der einzige etwas knifflige Teil. Gehe in der I2P router-Konsole zum Hidden Services Manager und finde beim SSH-Server tunnel die base64 "local destination". Du musst einen Weg finden, diese Information in den nächsten Schritt zu kopieren. Ich schicke sie mir normalerweise per [Tox](https://tox.chat) selbst, jede Off-the-Record-Methode sollte für die meisten ausreichend sein.

**Screenshot-Platzhalter:** Finden Sie die destination (Zieladresse innerhalb von I2P), zu der Sie eine Verbindung herstellen möchten

Sobald die Base64-Destination, zu der Sie eine Verbindung herstellen möchten, an Ihr Client-Gerät übermittelt wurde, fügen Sie sie anschließend in das Feld „Client Destination“ ein.

**Screenshot-Platzhalter:** Ziel anfügen

Legen Sie schließlich einen lokalen Port fest, mit dem sich Ihr SSH-Client verbinden soll. Dieser lokale Port wird mit der base64 destination (Base64-kodierte I2P-Destination) und damit dem SSH-Server verbunden.

**Screenshot-Platzhalter:** Wählen Sie einen lokalen Port

Entscheiden Sie, ob es automatisch starten soll.

**Platzhalter für Screenshot:** Entscheiden Sie, ob es automatisch gestartet werden soll

#### Erweiterte Einstellungen

Wie zuvor sollten Sie die Einstellungen so ändern, dass sie für interaktive Verbindungen optimiert sind. Außerdem sollten Sie, wenn Sie Client-Whitelisting auf dem Server einrichten möchten, das Optionsfeld "Schlüssel generieren, um eine persistente Client-tunnel-Identität zu aktivieren" aktivieren.

**Screenshot-Platzhalter:** Konfigurieren Sie ihn so, dass er interaktiv ist

### Using i2pd

Sie können dies einrichten, indem Sie die folgenden Zeilen zu Ihrer tunnels.conf hinzufügen und sie entsprechend Ihren Anforderungen an Leistung und Anonymität anpassen.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Es gibt viele Möglichkeiten, einen SSH-Client so einzurichten, dass er sich mit Ihrem Server im I2P-Netzwerk verbindet, aber es gibt ein paar Dinge, die Sie tun sollten, um Ihren SSH-Client für die anonyme Nutzung abzusichern. Zunächst sollten Sie ihn so konfigurieren, dass er sich gegenüber dem SSH-Server ausschließlich mit einem einzigen, spezifischen Schlüssel authentifiziert, um nicht das Risiko einzugehen, Ihre anonymen und nicht-anonymen SSH-Verbindungen miteinander zu verknüpfen.

Stellen Sie sicher, dass Ihre $HOME/.ssh/config die folgenden Zeilen enthält:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Alternativ könnten Sie einen .bash_alias-Eintrag erstellen, um Ihre Optionen durchzusetzen und automatisch eine Verbindung zu I2P herzustellen. Sie verstehen das Prinzip: Sie müssen IdentitiesOnly durchsetzen und eine Identity-Datei angeben.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Das ist mehr oder weniger optional, aber ziemlich cool und verhindert, dass jeder, der zufällig auf Ihre Destination (Zieladresse) stößt, erkennen kann, dass Sie einen SSH-Dienst hosten.

Zuerst rufen Sie die persistente Destination (Zieladresse) für den Client tunnel ab und übermitteln Sie sie an den Server.

**Screenshot-Platzhalter:** Client-Destination abrufen

Fügen Sie die Base64-Destination des Clients der Destination-Whitelist des Servers hinzu. Nun können Sie nur noch von genau diesem Client-Tunnel aus eine Verbindung zum Server-Tunnel herstellen, und niemand sonst kann sich mit dieser Destination verbinden.

**Screenshot-Platzhalter:** Und fügen Sie es in die Server-Whitelist ein

Gegenseitige Authentifizierung ist die beste Wahl.

**Hinweis:** Die im ursprünglichen Beitrag referenzierten Bilder müssen dem Verzeichnis `/static/images/` hinzugefügt werden: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
