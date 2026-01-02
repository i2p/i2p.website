---
title: "I2P auf Debian und Ubuntu installieren"
description: "Vollständige Anleitung zur Installation von I2P auf Debian, Ubuntu und deren Derivaten unter Verwendung der offiziellen Repositories"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Das I2P-Projekt pflegt offizielle Pakete für Debian, Ubuntu und deren abgeleitete Distributionen. Diese Anleitung bietet umfassende Anleitungen zur Installation von I2P unter Verwendung unserer offiziellen Repositories.

---


## 🚀 Beta: Automatische Installation (Experimentell)

**Für fortgeschrittene Benutzer, die eine schnelle automatisierte Installation wünschen:**

Dieser Einzeiler erkennt automatisch Ihre Distribution und installiert I2P. **Mit Vorsicht verwenden** - überprüfen Sie das [Installationsskript](https://i2p.net/installlinux.sh) vor der Ausführung.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```
**Was dies tut:** - Erkennt Ihre Linux-Distribution (Ubuntu/Debian) - Fügt das entsprechende I2P-Repository hinzu - Installiert GPG-Schlüssel und erforderliche Pakete - Installiert I2P automatisch

⚠️ **Dies ist eine Beta-Funktion.** Wenn Sie die manuelle Installation bevorzugen oder jeden Schritt verstehen möchten, verwenden Sie die unten aufgeführten manuellen Installationsmethoden.

---

## Unterstützte Plattformen

Die Debian-Pakete sind kompatibel mit:

- **Ubuntu** 18.04 (Bionic) und neuer
- **Linux Mint** 19 (Tara) und neuer
- **Debian** Buster (10) und neuer
- **Knoppix**
- Andere Debian-basierte Distributionen (LMDE, ParrotOS, Kali Linux, etc.)

**Unterstützte Architekturen**: amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

Die I2P-Pakete funktionieren möglicherweise auch auf anderen Debian-basierten Systemen, die oben nicht ausdrücklich aufgeführt sind. Wenn Sie auf Probleme stoßen, [melden Sie diese bitte in unserem GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Installationsmethoden

Wählen Sie die Installationsmethode, die zu Ihrer Distribution passt:

- **Option 1**: [Ubuntu und Derivate](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, etc.)
- **Option 2**: [Debian und Debian-basierte Distributionen](#debian-installation) (einschließlich LMDE, Kali, ParrotOS)

---


## Ubuntu Installation

Ubuntu und seine offiziellen Derivate (Linux Mint, elementary OS, Trisquel, etc.) können das I2P PPA (Personal Package Archive) für eine einfache Installation und automatische Updates nutzen.

### Method 1: Command Line Installation (Recommended)

Dies ist die schnellste und zuverlässigste Methode zur Installation von I2P auf Ubuntu-basierten Systemen.

**Schritt 1: Das I2P PPA hinzufügen**

Öffnen Sie ein Terminal und führen Sie aus:

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Dieser Befehl fügt das I2P PPA zu `/etc/apt/sources.list.d/` hinzu und importiert automatisch den GPG-Schlüssel, der das Repository signiert. Die GPG-Signatur stellt sicher, dass die Pakete seit ihrem Build nicht manipuliert wurden.

**Schritt 2: Paketliste aktualisieren**

Aktualisieren Sie die Paketdatenbank Ihres Systems, um das neue PPA einzubeziehen:

```bash
sudo apt-get update
```
Dies ruft die neuesten Paketinformationen von allen aktivierten Repositorys ab, einschließlich des soeben hinzugefügten I2P PPA.

**Schritt 3: I2P installieren**

Jetzt I2P installieren:

```bash
sudo apt-get install i2p
```
Das war's! Fahren Sie mit dem Abschnitt [Konfiguration nach der Installation](#post-installation-configuration) fort, um zu erfahren, wie Sie I2P starten und konfigurieren.

### Method 2: Using the Software Center GUI

Wenn Sie eine grafische Benutzeroberfläche bevorzugen, können Sie das PPA über Ubuntu's Software Center hinzufügen.

**Schritt 1: Software & Aktualisierungen öffnen**

Starten Sie „Software und Aktualisierungen" aus Ihrem Anwendungsmenü.

![Software Center Menü](/images/guides/debian/software-center-menu.png)

**Schritt 2: Navigieren Sie zu Andere Software**

Wählen Sie den Tab "Andere Software" aus und klicken Sie auf die Schaltfläche "Hinzufügen" am unteren Rand, um ein neues PPA zu konfigurieren.

![Andere Software-Tab](/images/guides/debian/software-center-addother.png)

**Schritt 3: I2P PPA hinzufügen**

Im PPA-Dialogfeld eingeben:

```
ppa:i2p-maintainers/i2p
```
![Add PPA Dialog](/images/guides/debian/software-center-ppatool.png)

**Schritt 4: Repository-Informationen neu laden**

Klicken Sie auf die Schaltfläche „Neu laden", um die aktualisierten Repository-Informationen herunterzuladen.

![Reload Button](/images/guides/debian/software-center-reload.png)

**Schritt 5: I2P installieren**

Öffnen Sie die Anwendung "Software" aus Ihrem Anwendungsmenü, suchen Sie nach "i2p" und klicken Sie auf Installieren.

![Softwareanwendung](/images/guides/debian/software-center-software.png)

Sobald die Installation abgeschlossen ist, fahren Sie mit der [Konfiguration nach der Installation](#post-installation-configuration) fort.

---


## Debian Installation

Debian und dessen nachgelagerte Distributionen (LMDE, Kali Linux, ParrotOS, Knoppix, etc.) sollten das offizielle I2P Debian-Repository unter `deb.i2p.net` verwenden.

### Important Notice

**Unsere alten Repositories unter `deb.i2p2.de` und `deb.i2p2.no` haben das Ende ihrer Lebensdauer erreicht.** Falls Sie diese veralteten Repositories verwenden, folgen Sie bitte den untenstehenden Anweisungen, um zum neuen Repository unter `deb.i2p.net` zu migrieren.

### Prerequisites

Alle folgenden Schritte erfordern Root-Zugriff. Wechseln Sie entweder mit `su` zum Root-Benutzer oder stellen Sie jedem Befehl `sudo` voran.

### Methode 1: Installation über die Kommandozeile (Empfohlen)

**Schritt 1: Erforderliche Pakete installieren**

Stellen Sie sicher, dass Sie die notwendigen Tools installiert haben:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Diese Pakete ermöglichen sicheren HTTPS-Repository-Zugriff, Distributionserkennung und Dateidownloads.

**Schritt 2: Fügen Sie das I2P-Repository hinzu**

Der Befehl, den Sie verwenden, hängt von Ihrer Debian-Version ab. Bestimmen Sie zunächst, welche Version Sie verwenden:

```bash
cat /etc/debian_version
```
Vergleichen Sie dies mit den [Debian-Veröffentlichungsinformationen](https://wiki.debian.org/LTS/), um den Codenamen Ihrer Distribution zu identifizieren (z. B. Bookworm, Bullseye, Buster).

**Für Debian Bullseye (11) oder neuer:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Für Debian-Derivate (LMDE, Kali, ParrotOS, etc.) auf Bullseye-Äquivalent oder neueren Versionen:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Für Debian Buster (10) oder älter:**

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Für Debian-Derivate auf Buster-Äquivalent oder älter:**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Schritt 3: Repository-Signaturschlüssel herunterladen**

```bash
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
```
**Schritt 4: Den Schlüssel-Fingerabdruck überprüfen**

Überprüfen Sie vor dem Vertrauen des Schlüssels, ob sein Fingerabdruck mit dem offiziellen I2P-Signaturschlüssel übereinstimmt:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Überprüfen Sie, ob die Ausgabe diesen Fingerprint zeigt:**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **Fahren Sie nicht fort, wenn der Fingerabdruck nicht übereinstimmt.** Dies könnte auf einen kompromittierten Download hinweisen.

**Schritt 5: Repository-Schlüssel installieren**

Kopieren Sie den verifizierten Keyring in das System-Keyring-Verzeichnis:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Nur für Debian Buster oder älter** müssen Sie zusätzlich einen Symlink erstellen:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Schritt 6: Paketlisten aktualisieren**

Aktualisieren Sie die Paketdatenbank Ihres Systems, um das I2P-Repository einzubeziehen:

```bash
sudo apt-get update
```
**Schritt 7: I2P installieren**

Installieren Sie sowohl das I2P-Router-Paket als auch das Keyring-Paket (welches sicherstellt, dass Sie zukünftige Schlüssel-Updates erhalten):

```bash
sudo apt-get install i2p i2p-keyring
```
Großartig! I2P ist jetzt installiert. Fahren Sie mit dem Abschnitt [Konfiguration nach der Installation](#post-installation-configuration) fort.

Ich verstehe die Anweisungen. Ich bin bereit, den zu übersetzenden Text zu empfangen. Bitte geben Sie den Text an, den ich vom Englischen ins Deutsche übersetzen soll.

## Post-Installation Configuration

Nach der Installation von I2P müssen Sie den Router starten und einige anfängliche Konfigurationen vornehmen.

### Methode 2: Verwendung der Software Center GUI

Die I2P-Pakete bieten drei Möglichkeiten, den I2P-Router zu betreiben:

#### Option 1: On-Demand (Basic)

Starten Sie I2P bei Bedarf manuell mit dem `i2prouter`-Skript:

```bash
i2prouter start
```
**Wichtig**: Verwenden Sie **nicht** `sudo` und führen Sie dies nicht als root aus! I2P sollte als Ihr regulärer Benutzer ausgeführt werden.

So beenden Sie I2P:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Wenn Sie ein Nicht-x86-System verwenden oder der Java Service Wrapper auf Ihrer Plattform nicht funktioniert, nutzen Sie:

```bash
i2prouter-nowrapper
```
Auch hier gilt: Verwenden Sie **nicht** `sudo` und führen Sie dies nicht als root aus.

#### Option 3: System Service (Recommended)

Für die beste Erfahrung konfigurieren Sie I2P so, dass es automatisch beim Systemstart startet, noch vor der Anmeldung:

```bash
sudo dpkg-reconfigure i2p
```
Dies öffnet einen Konfigurationsdialog. Wählen Sie "Ja", um I2P als Systemdienst zu aktivieren.

**Dies ist die empfohlene Methode**, weil: - I2P automatisch beim Systemstart gestartet wird - Ihr Router eine bessere Netzwerkintegration aufrechterhält - Sie zur Netzwerkstabilität beitragen - I2P sofort verfügbar ist, wenn Sie es benötigen

### Initial Router Configuration

Nachdem I2P zum ersten Mal gestartet wurde, dauert es einige Minuten, bis es sich in das Netzwerk integriert hat. Konfigurieren Sie in der Zwischenzeit diese wichtigen Einstellungen:

#### 1. Configure NAT/Firewall

Für optimale Leistung und Netzwerkteilnahme leiten Sie die I2P-Ports durch Ihr NAT/Ihre Firewall weiter:

1. Öffnen Sie die [I2P Router Console](http://127.0.0.1:7657/)
2. Navigieren Sie zur [Netzwerkkonfigurationsseite](http://127.0.0.1:7657/confignet)
3. Notieren Sie die aufgelisteten Portnummern (normalerweise zufällige Ports zwischen 9000-31000)
4. Leiten Sie diese UDP- und TCP-Ports in Ihrem Router/Ihrer Firewall weiter

Wenn Sie Hilfe beim Port-Forwarding benötigen, bietet [portforward.com](https://portforward.com) routerspezifische Anleitungen.

#### 2. Adjust Bandwidth Settings

Die Standard-Bandbreiteneinstellungen sind konservativ. Passen Sie diese basierend auf Ihrer Internetverbindung an:

1. Besuchen Sie die [Konfigurationsseite](http://127.0.0.1:7657/config.jsp)
2. Suchen Sie den Abschnitt für Bandbreiteneinstellungen
3. Die Standardwerte sind 96 KB/s Download / 40 KB/s Upload
4. Erhöhen Sie diese Werte, wenn Sie eine schnellere Internetverbindung haben (z.B. 250 KB/s Download / 100 KB/s Upload für eine typische Breitbandverbindung)

**Hinweis**: Höhere Limits helfen dem Netzwerk und verbessern Ihre eigene Leistung.

#### 3. Configure Your Browser

Um auf I2P-Seiten (eepsites) und Dienste zuzugreifen, konfigurieren Sie Ihren Browser so, dass er den HTTP-Proxy von I2P verwendet:

Siehe unsere [Anleitung zur Browser-Konfiguration](/docs/guides/browser-config) für detaillierte Einrichtungsanleitungen für Firefox, Chrome und andere Browser.

---


## Debian-Installation

### Wichtiger Hinweis

- Stellen Sie sicher, dass I2P nicht als root läuft: `ps aux | grep i2p`
- Logs überprüfen: `tail -f ~/.i2p/wrapper.log`
- Überprüfen Sie, ob Java installiert ist: `java -version`

### Voraussetzungen

Wenn Sie während der Installation GPG-Schlüsselfehler erhalten:

1. Laden Sie den Schlüssel erneut herunter und überprüfen Sie den Fingerabdruck (Schritte 3-4 oben)
2. Stellen Sie sicher, dass die Keyring-Datei die richtigen Berechtigungen hat: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Installationsschritte

Wenn I2P keine Updates erhält:

1. Repository-Konfiguration überprüfen: `cat /etc/apt/sources.list.d/i2p.list`
2. Paketlisten aktualisieren: `sudo apt-get update`
3. Nach I2P-Updates suchen: `sudo apt-get upgrade`

### Migrating from old repositories

Wenn Sie die alten Repositories `deb.i2p2.de` oder `deb.i2p2.no` verwenden:

1. Entfernen Sie das alte Repository: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Folgen Sie den [Debian-Installations](#debian-installation)-Schritten oben
3. Aktualisieren Sie: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

## Next Steps

Jetzt, da I2P installiert ist und läuft:

- [Konfigurieren Sie Ihren Browser](/docs/guides/browser-config), um auf I2P-Seiten zuzugreifen
- Erkunden Sie die [I2P-Router-Konsole](http://127.0.0.1:7657/), um Ihren Router zu überwachen
- Erfahren Sie mehr über [I2P-Anwendungen](/docs/applications/), die Sie nutzen können
- Lesen Sie, [wie I2P funktioniert](/docs/overview/tech-intro), um das Netzwerk zu verstehen

Willkommen im Invisible Internet!
