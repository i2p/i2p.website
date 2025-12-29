---
title: "Leitfaden für neue Entwickler"
description: "Wie man anfängt, zu I2P beizutragen: Lernmaterialien, Quellcode, Build-Prozess, Ideen, Veröffentlichung, Community, Übersetzungen und Werkzeuge"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: Übersetzungsteil aktualisieren
---

Sie möchten also an I2P mitarbeiten? Großartig! Hier ist eine kurze Anleitung für den Einstieg – sei es zur Mitarbeit an der Website oder der Software, zur Entwicklung oder zur Erstellung von Übersetzungen.

Noch nicht bereit zum Programmieren? Versuche es zuerst mit [Mitmachen](/get-involved/).

## Lernen Sie Java kennen

Der I2P router und seine eingebetteten Anwendungen verwenden Java als Hauptentwicklungssprache. Wenn Sie keine Erfahrung mit Java haben, können Sie sich immer [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf) ansehen

Studieren Sie die Einführung zu "how", andere "how"-Dokumente, die technische Einführung und zugehörige Dokumente:

- Einführung: [Einführung in I2P](/docs/overview/intro/)
- Dokumentations-Hub: [Dokumentation](/docs/)
- Technische Einführung: [Technische Einführung](/docs/overview/tech-intro/)

Diese geben Ihnen einen guten Überblick darüber, wie I2P strukturiert ist und welche verschiedenen Funktionen es erfüllt.

## Den I2P-Code erhalten

Für die Entwicklung am I2P-Router oder den eingebetteten Anwendungen benötigen Sie den Quellcode.

### Unsere aktuelle Methode: Git

I2P verfügt über offizielle Git-Dienste und akzeptiert Beiträge via Git auf unserem eigenen GitLab:

- Innerhalb von I2P: <http://git.idk.i2p>
- Außerhalb von I2P: <https://i2pgit.org>

Klonen Sie das Haupt-Repository:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
Ein schreibgeschützter Mirror ist auch auf GitHub verfügbar:

- GitHub-Mirror: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## I2P erstellen

Um den Code zu kompilieren, benötigen Sie das Sun/Oracle Java Development Kit 6 oder höher, oder ein entsprechendes JDK (Sun/Oracle JDK 6 wird dringend empfohlen) sowie Apache Ant Version 1.7.0 oder höher. Wenn Sie am Haupt-I2P-Code arbeiten, wechseln Sie in das Verzeichnis `i2p.i2p` und führen Sie `ant` aus, um die Build-Optionen anzuzeigen.

Um Konsolenübersetzungen zu erstellen oder daran zu arbeiten, benötigen Sie die Werkzeuge `xgettext`, `msgfmt` und `msgmerge` aus dem GNU gettext-Paket.

Für die Entwicklung neuer Anwendungen siehe den [Leitfaden zur Anwendungsentwicklung](/docs/develop/applications/).

## Entwicklungsideen

Siehe die Projekt-TODO-Liste oder die Issue-Liste auf GitLab für Ideen:

- GitLab-Issues: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Bereitstellung der Ergebnisse

Siehe unten auf der Lizenzseite für die Anforderungen an Commit-Rechte. Sie benötigen diese, um Code in `i2p.i2p` einzubringen (nicht erforderlich für die Website!).

- [Lizenzseite](/docs/develop/licenses#commit)

## Lernen Sie uns kennen!

Die Entwickler sind auf IRC erreichbar. Sie können über verschiedene Netzwerke und im I2P-internen Netzwerk kontaktiert werden. Der übliche Anlaufpunkt ist `#i2p-dev`. Treten Sie dem Kanal bei und sagen Sie Hallo! Wir haben auch zusätzliche [Richtlinien für regelmäßige Entwickler](/docs/develop/dev-guidelines/).

## Übersetzungen

Übersetzer für Website und Router-Konsole: Siehe den [Leitfaden für neue Übersetzer](/docs/develop/new-translators/) für die nächsten Schritte.

## Werkzeuge

I2P ist Open-Source-Software, die hauptsächlich mit Open-Source-Werkzeugen entwickelt wird. Das I2P-Projekt hat kürzlich eine Lizenz für den YourKit Java Profiler erhalten. Open-Source-Projekte können eine kostenlose Lizenz erhalten, sofern YourKit auf der Projekt-Website referenziert wird. Bitte melden Sie sich, wenn Sie daran interessiert sind, die I2P-Codebasis zu profilieren.

YourKit unterstützt freundlicherweise Open-Source-Projekte mit seinen voll ausgestatteten Profilern. YourKit, LLC ist der Entwickler innovativer und intelligenter Tools zur Profilerstellung von Java- und .NET-Anwendungen. Werfen Sie einen Blick auf die führenden Softwareprodukte von YourKit:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
