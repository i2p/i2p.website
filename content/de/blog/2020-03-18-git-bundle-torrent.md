---
title: "Verwendung eines Git-Bundles zum Abrufen des I2P-Quellcodes"
date: 2020-03-18
author: "idk"
description: "Laden Sie den I2P-Quellcode über BitTorrent herunter"
categories: ["development"]
---

Das Klonen großer Software-Repositories über I2P kann schwierig sein, und die Verwendung von git kann dies manchmal noch erschweren. Glücklicherweise kann es das manchmal auch erleichtern. Git verfügt über den Befehl `git bundle`, mit dem sich ein git-Repository in eine Datei verwandeln lässt, die git anschließend an einem Ort auf Ihrer lokalen Festplatte als Quelle zum Klonen, Fetchen oder Importieren verwenden kann. Durch die Kombination dieser Fähigkeit mit BitTorrent-Downloads können wir unsere verbleibenden Probleme mit `git clone` lösen.

## Bevor Sie beginnen

Wenn Sie beabsichtigen, ein git-Bundle zu erzeugen, **müssen** Sie bereits eine vollständige Kopie des **git**-Repositorys besitzen, nicht des mtn-Repositorys. Sie können es von github oder von git.idk.i2p beziehen, aber ein flacher Klon (ein Klon mit --depth=1) *wird nicht funktionieren*. Er schlägt stillschweigend fehl und erzeugt etwas, das wie ein Bundle aussieht, aber wenn Sie versuchen, es zu klonen, schlägt es fehl. Wenn Sie nur ein vorgeneriertes git-Bundle abrufen, gilt dieser Abschnitt nicht für Sie.

## Abrufen des I2P-Quellcodes über Bittorrent

Jemand muss Ihnen eine Torrent-Datei oder einen Magnet-Link zu einem vorhandenen `git bundle` bereitstellen, das bereits für Sie erstellt wurde. Sobald Sie ein Bundle über BitTorrent erhalten haben, müssen Sie git verwenden, um daraus ein funktionsfähiges Repository zu erstellen.

## Verwendung von `git clone`

Das Klonen aus einem Git-Bundle ist ganz einfach, und zwar:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Wenn Sie den folgenden Fehler erhalten, versuchen Sie stattdessen, git init und git fetch manuell auszuführen:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Verwendung von `git init` und `git fetch`

Erstellen Sie zunächst ein Verzeichnis i2p.i2p, das in ein Git-Repository umgewandelt werden soll:

```
mkdir i2p.i2p && cd i2p.i2p
```
Als Nächstes initialisieren Sie ein leeres Git-Repository, in das die Änderungen zurückgeholt werden sollen:

```
git init
```
Abschließend das Repository aus dem Bundle abrufen:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Ersetzen Sie das Bundle-Remote durch das Upstream-Remote

Jetzt, da Sie ein Bundle haben, können Sie mit den Änderungen Schritt halten, indem Sie das Remote auf die Upstream-Repository-Quelle setzen:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Erzeugen eines Bundles

Folgen Sie zunächst dem Git-Leitfaden für Benutzer, bis Sie erfolgreich einen `--unshallow`ed Klon des i2p.i2p-Repositorys haben. Wenn Sie bereits einen Klon haben, stellen Sie sicher, dass Sie `git fetch --unshallow` ausführen, bevor Sie ein Torrent-Bundle erstellen.

Sobald Sie das haben, führen Sie einfach das entsprechende Ant-Target aus:

```
ant bundle
```
und kopieren Sie das resultierende Bundle in Ihr I2PSnark-Download-Verzeichnis. Zum Beispiel:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
In ein bis zwei Minuten wird I2PSnark den Torrent erkennen. Klicken Sie auf die Schaltfläche "Start", um mit dem Seeden des Torrents zu beginnen.
