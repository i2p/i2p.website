---
title: "Git Bundles für I2P"
description: "Abrufen und Verteilen großer Repositories mit git bundle und BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Wenn Netzwerkbedingungen `git clone` unzuverlässig machen, können Sie Repositories als **Git-Bundles** über BitTorrent oder einen anderen Dateitransport verteilen. Ein Bundle ist eine einzelne Datei, die die gesamte Repository-Historie enthält. Nach dem Download führen Sie lokal einen Fetch daraus durch und wechseln dann zurück zum Upstream-Remote.

## 1. Bevor Sie beginnen

Das Erstellen eines Bundles erfordert einen **vollständigen** Git-Clone. Flache Clones, die mit `--depth 1` erstellt wurden, erzeugen stillschweigend fehlerhafte Bundles, die scheinbar funktionieren, aber fehlschlagen, wenn andere versuchen, sie zu verwenden. Laden Sie immer von einer vertrauenswürdigen Quelle herunter (GitHub unter [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), der I2P-Gitea-Instanz unter [i2pgit.org](https://i2pgit.org) oder `git.idk.i2p` über I2P) und führen Sie bei Bedarf `git fetch --unshallow` aus, um jeden flachen Clone in einen vollständigen Clone umzuwandeln, bevor Sie Bundles erstellen.

Wenn Sie nur ein vorhandenes Bundle verwenden, laden Sie es einfach herunter. Keine besondere Vorbereitung erforderlich.

## 2. Herunterladen eines Bundles

### Obtaining the Bundle File

Laden Sie die Bundle-Datei über BitTorrent mit I2PSnark (dem integrierten Torrent-Client in I2P) oder anderen I2P-kompatiblen Clients wie BiglyBT mit dem I2P-Plugin herunter.

**Wichtig**: I2PSnark funktioniert nur mit Torrents, die speziell für das I2P-Netzwerk erstellt wurden. Standard-Clearnet-Torrents sind nicht kompatibel, da I2P Destinations (387+ Byte Adressen) anstelle von IP-Adressen und Ports verwendet.

Der Speicherort der Bundle-Datei hängt von Ihrem I2P-Installationstyp ab:

- **Benutzer-/manuelle Installationen** (installiert mit Java-Installer): `~/.i2p/i2psnark/`
- **System-/Daemon-Installationen** (installiert via apt-get oder Paketmanager): `/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT-Benutzer finden heruntergeladene Dateien in ihrem konfigurierten Download-Verzeichnis.

### Cloning from the Bundle

**Standardmethode** (funktioniert in den meisten Fällen):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Wenn Sie auf `fatal: multiple updates for ref` Fehler stoßen (ein bekanntes Problem in Git 2.21.0 und später, wenn die globale Git-Konfiguration widersprüchliche Fetch-Refspecs enthält), verwenden Sie die manuelle Initialisierungsmethode:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternativ können Sie das Flag `--update-head-ok` verwenden:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Beschaffung der Bundle-Datei

Nachdem Sie vom Bundle geklont haben, richten Sie Ihren Klon auf das Live-Remote aus, damit zukünftige Fetches über I2P oder Clearnet erfolgen:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Oder für Clearnet-Zugriff:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Für I2P-SSH-Zugriff benötigen Sie einen SSH-Client-Tunnel, der in Ihrer I2P-Router-Konsole konfiguriert ist (typischerweise Port 7670) und auf `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p` zeigt. Bei Verwendung eines nicht standardmäßigen Ports:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Klonen aus dem Bundle

Stellen Sie sicher, dass Ihr Repository mit einem **vollständigen Klon** (nicht shallow) auf dem neuesten Stand ist:

```bash
git fetch --all
```
Wenn Sie einen Shallow Clone haben, konvertieren Sie ihn zuerst:

```bash
git fetch --unshallow
```
### Wechsel zur Live-Remote

**Verwendung des Ant-Build-Ziels** (empfohlen für den I2P-Quellbaum):

```bash
ant git-bundle
```
Dies erzeugt sowohl `i2p.i2p.bundle` (die Bundle-Datei) als auch `i2p.i2p.bundle.torrent` (BitTorrent-Metadaten).

**Git Bundle direkt verwenden**:

```bash
git bundle create i2p.i2p.bundle --all
```
Für selektivere Bundles:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Überprüfen Sie das Bundle immer vor der Verteilung:

```bash
git bundle verify i2p.i2p.bundle
```
Dies bestätigt, dass das Bundle gültig ist und zeigt alle erforderlichen vorausgesetzten Commits an.

### Voraussetzungen

Kopiere das Bundle und seine Torrent-Metadaten in dein I2PSnark-Verzeichnis:

**Für Benutzerinstallationen**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Für Systeminstallationen**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark erkennt und lädt .torrent-Dateien automatisch innerhalb von Sekunden. Greifen Sie auf die Weboberfläche unter [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) zu, um mit dem Seeden zu beginnen.

## 4. Creating Incremental Bundles

Für periodische Updates erstellen Sie inkrementelle Bundles, die nur neue Commits seit dem letzten Bundle enthalten:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Benutzer können aus dem inkrementellen Bundle abrufen, wenn sie bereits das Basis-Repository haben:

```bash
git fetch /path/to/update.bundle
```
Überprüfen Sie immer, dass inkrementelle Bundles die erwarteten vorausgesetzten Commits anzeigen:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Sobald Sie ein funktionierendes Repository aus dem Bundle haben, behandeln Sie es wie jeden anderen Git-Clone:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Oder für einfachere Arbeitsabläufe:

```bash
git fetch origin
git pull origin master
```
## 3. Ein Bundle erstellen

- **Resiliente Verteilung**: Große Repositories können über BitTorrent geteilt werden, das automatisch Wiederholungsversuche, Verifizierung einzelner Teile und Fortsetzung unterbrechter Downloads übernimmt.
- **Peer-to-peer Bootstrap**: Neue Mitwirkende können ihren Clone von nahegelegenen Peers im I2P-Netzwerk bootstrappen und anschließend inkrementelle Änderungen direkt von Git-Hosts abrufen.
- **Reduzierte Serverlast**: Mirrors können regelmäßige Bundles veröffentlichen, um die Last auf aktiven Git-Hosts zu verringern – besonders nützlich bei großen Repositories oder langsamen Netzwerkbedingungen.
- **Offline-Transport**: Bundles funktionieren über jeden Dateitransport (USB-Laufwerke, direkte Übertragungen, Sneakernet), nicht nur über BitTorrent.

Bundles ersetzen keine Live-Remotes. Sie bieten lediglich eine robustere Bootstrapping-Methode für initiale Klone oder größere Updates.

## 7. Troubleshooting

### Generieren des Bundles

**Problem**: Bundle-Erstellung erfolgreich, aber andere können nicht vom Bundle klonen.

**Ursache**: Ihr Quellklon ist flach (erstellt mit `--depth`).

**Lösung**: Vor dem Erstellen von Bundles in einen vollständigen Klon konvertieren:

```bash
git fetch --unshallow
```
### Verifizierung Ihres Bundles

**Problem**: `fatal: multiple updates for ref` beim Klonen aus einem Bundle.

**Ursache**: Git 2.21.0+ steht in Konflikt mit globalen Fetch-Refspecs in `~/.gitconfig`.

**Lösungen**: 1. Manuelle Initialisierung verwenden: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Das Flag `--update-head-ok` verwenden: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Konfliktverursachende Konfiguration entfernen: `git config --global --unset remote.origin.fetch`

### Verteilung über I2PSnark

**Problem**: `git bundle verify` meldet fehlende Voraussetzungen.

**Ursache**: Inkrementelles Bundle oder unvollständiger Quellcode-Klon.

**Lösung**: Entweder die erforderlichen Commits abrufen oder zuerst das Basis-Bundle verwenden und dann inkrementelle Updates anwenden.
