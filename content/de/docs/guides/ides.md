---
title: "I2P mit einer IDE verwenden"
description: "Einrichten von Eclipse und NetBeans für die Entwicklung von I2P mit Gradle und mitgelieferten Projektdateien"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> Der Haupt-I2P-Entwicklungszweig (<code>i2p.i2p</code>) wurde so eingerichtet, dass Entwickler zwei der häufig verwendeten IDEs für Java-Entwicklung einfach einrichten können: Eclipse und NetBeans. </p>

<h2>Eclipse</h2>

<p> Die Hauptentwicklungszweige von I2P (<code>i2p.i2p</code> und davon abgeleitete Branches) enthalten <code>build.gradle</code>, um den Branch einfach in Eclipse einzurichten. </p>

<ol> <li> Stellen Sie sicher, dass Sie eine aktuelle Version von Eclipse haben. Alles neuer als 2017 sollte funktionieren. </li> <li> Checken Sie den I2P-Branch in ein Verzeichnis aus (z.B. <code>$HOME/dev/i2p.i2p</code>). </li> <li> Wählen Sie "File → Import..." und dann unter "Gradle" die Option "Existing Gradle Project". </li> <li> Für "Project root directory:" wählen Sie das Verzeichnis, in das der I2P-Branch ausgecheckt wurde. </li> <li> Im Dialog "Import Options" wählen Sie "Gradle Wrapper" und klicken auf Continue. </li> <li> Im Dialog "Import Preview" können Sie die Projektstruktur überprüfen. Unter "i2p.i2p" sollten mehrere Projekte erscheinen. Klicken Sie auf "Finish". </li> <li> Fertig! Ihr Workspace sollte nun alle Projekte innerhalb des I2P-Branch enthalten, und deren Build-Abhängigkeiten sollten korrekt eingerichtet sein. </li> </ol>

<h2>NetBeans</h2>

<p> Die Haupt-I2P-Entwicklungszweige (<code>i2p.i2p</code> und davon abgeleitete Zweige) enthalten NetBeans-Projektdateien. </p>

<!-- Keep content minimal and close to original; will update later. -->
