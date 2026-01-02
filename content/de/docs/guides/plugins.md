---
title: "Benutzerdefinierte Plugins installieren"
description: "Installation, Aktualisierung und Entwicklung von Router-Plugins"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Das Plugin-Framework von I2P ermöglicht es Ihnen, den Router zu erweitern, ohne die Kerninstallation zu verändern. Verfügbare Plugins umfassen E-Mail, Blogs, IRC, Speicher, Wikis, Überwachungstools und mehr.

> **Sicherheitshinweis:** Plugins laufen mit denselben Berechtigungen wie der Router. Behandeln Sie Downloads von Drittanbietern genauso, wie Sie jedes signierte Software-Update behandeln würden – überprüfen Sie die Quelle vor der Installation.

## 1. Plugin installieren

1. Kopieren Sie die Download-URL des Plugins von der Projektseite.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Öffnen Sie die [Plugin-Konfigurationsseite](http://127.0.0.1:7657/configplugins) der Router-Konsole.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Fügen Sie die URL in das Installationsfeld ein und klicken Sie auf **Install Plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

Der Router lädt das signierte Archiv herunter, überprüft die Signatur und aktiviert das Plugin sofort. Die meisten Plugins fügen Konsolenlinks oder Hintergrunddienste hinzu, ohne einen Router-Neustart zu erfordern.

## 2. Warum Plugins wichtig sind

- Ein-Klick-Verteilung für Endbenutzer—keine manuellen Änderungen an `wrapper.config` oder `clients.config`
- Hält das Kern-`i2pupdate.su3`-Bundle klein, während große oder Nischen-Features bei Bedarf bereitgestellt werden
- Optionale plugin-spezifische JVMs bieten Prozessisolierung, wenn erforderlich
- Automatische Kompatibilitätsprüfungen mit der Router-Version, Java-Laufzeitumgebung und Jetty
- Update-Mechanismus entspricht dem des Routers: signierte Pakete und inkrementelle Downloads
- Console-Integrationen, Sprachpakete, UI-Themes und Nicht-Java-Anwendungen (über Skripte) werden alle unterstützt
- Ermöglicht kuratierte „App-Store"-Verzeichnisse wie `plugins.i2p`

## 3. Installierte Plugins verwalten

Verwenden Sie die Steuerungselemente im [I2P Router Plugin](http://127.0.0.1:7657/configclients.jsp#plugin), um:

- Ein einzelnes Plugin auf Updates prüfen
- Alle Plugins auf einmal prüfen (wird automatisch nach Router-Upgrades ausgelöst)
- Verfügbare Updates mit einem Klick installieren  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Autostart für Plugins aktivieren/deaktivieren, die Dienste registrieren
- Plugins sauber deinstallieren

## 4. Erstellen Sie Ihr eigenes Plugin

1. Überprüfen Sie die [Plugin-Spezifikation](/docs/specs/plugin/) für Anforderungen an Paketierung, Signierung und Metadaten.
2. Verwenden Sie [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh), um eine bestehende Binärdatei oder Webapp in ein installierbares Archiv zu verpacken.
3. Veröffentlichen Sie sowohl Installations- als auch Update-URLs, damit der Router zwischen Erstinstallationen und inkrementellen Upgrades unterscheiden kann.
4. Stellen Sie Prüfsummen und Signaturschlüssel prominent auf Ihrer Projektseite bereit, um Benutzern bei der Überprüfung der Authentizität zu helfen.

Suchst du nach Beispielen? Durchsuche den Quellcode von Community-Plugins auf `plugins.i2p` (zum Beispiel das `snowman`-Beispiel).

## 5. Bekannte Einschränkungen

- Das Aktualisieren eines Plugins, das einfache JAR-Dateien ausliefert, kann einen Router-Neustart erfordern, da der Java-Class-Loader Klassen zwischenspeichert.
- Die Konsole zeigt möglicherweise einen **Stop**-Button an, auch wenn das Plugin keinen aktiven Prozess hat.
- Plugins, die in einer separaten JVM gestartet werden, erstellen ein `logs/`-Verzeichnis im aktuellen Arbeitsverzeichnis.
- Beim ersten Auftreten wird ein Signer-Key automatisch als vertrauenswürdig eingestuft; es gibt keine zentrale Signierungsinstanz.
- Windows hinterlässt manchmal leere Verzeichnisse nach der Deinstallation eines Plugins.
- Die Installation eines Plugins, das nur für Java 6 ausgelegt ist, auf einer Java 5 JVM meldet „Plugin ist beschädigt" aufgrund der Pack200-Komprimierung.
- Theme- und Übersetzungs-Plugins sind weitgehend ungetestet.
- Autostart-Flags bleiben bei nicht verwalteten Plugins nicht immer erhalten.

## 6. Anforderungen & Best Practices

- Plugin-Unterstützung ist verfügbar in I2P **0.7.12 und neuer**.
- Halten Sie Ihren Router und Plugins auf dem neuesten Stand, um Sicherheitsupdates zu erhalten.
- Liefern Sie prägnante Release-Notes mit, damit Benutzer verstehen, was sich zwischen Versionen ändert.
- Hosten Sie Plugin-Archive wenn möglich über HTTPS innerhalb von I2P, um die Offenlegung von Clearnet-Metadaten zu minimieren.

## 7. Weiterführende Literatur

- [Plugin-Spezifikation](/docs/specs/plugin/)
- [Client-Anwendungs-Framework](/docs/applications/managed-clients/)
- [I2P-Scripts-Repository](https://github.com/i2p/i2p.scripts/) für Paketierungs-Werkzeuge
