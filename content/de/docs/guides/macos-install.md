---
title: "I2P auf macOS installieren (Der lange Weg)"
description: "Schritt-für-Schritt-Anleitung zur manuellen Installation von I2P und seinen Abhängigkeiten auf macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Was Sie benötigen

- Ein Mac mit macOS 10.14 (Mojave) oder neuer
- Administratorrechte zur Installation von Anwendungen
- Etwa 15-20 Minuten Zeit
- Internetverbindung zum Herunterladen der Installationsprogramme

## Übersicht

Dieser Installationsprozess hat vier Hauptschritte:

1. **Java installieren** - Laden Sie die Oracle Java Runtime Environment herunter und installieren Sie sie
2. **I2P installieren** - Laden Sie das I2P-Installationsprogramm herunter und führen Sie es aus
3. **I2P-App konfigurieren** - Richten Sie den Launcher ein und fügen Sie ihn zu Ihrem Dock hinzu
4. **I2P-Bandbreite konfigurieren** - Führen Sie den Einrichtungsassistenten aus, um Ihre Verbindung zu optimieren

## Teil Eins: Java installieren

I2P benötigt Java, um zu laufen. Wenn Sie bereits Java 8 oder neuer installiert haben, können Sie [zu Teil Zwei springen](#part-two-download-and-install-i2p).

### Step 1: Download Java

Besuchen Sie die [Oracle Java Download-Seite](https://www.oracle.com/java/technologies/downloads/) und laden Sie das macOS-Installationsprogramm für Java 8 oder höher herunter.

![Oracle Java für macOS herunterladen](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Suchen Sie die heruntergeladene `.dmg`-Datei in Ihrem Downloads-Ordner und doppelklicken Sie darauf, um sie zu öffnen.

![Java-Installer öffnen](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS zeigt möglicherweise eine Sicherheitsmeldung an, da das Installationsprogramm von einem identifizierten Entwickler stammt. Klicken Sie auf **Öffnen**, um fortzufahren.

![Erteilen Sie dem Installer die Berechtigung fortzufahren](/images/guides/macos-install/2-jre.png)

### Schritt 1: Java herunterladen

Klicken Sie auf **Installieren**, um den Java-Installationsprozess zu starten.

![Java-Installation starten](/images/guides/macos-install/3-jre.png)

### Schritt 2: Installationsprogramm ausführen

Der Installer wird Dateien kopieren und Java auf Ihrem System konfigurieren. Dies dauert in der Regel 1-2 Minuten.

![Warten Sie, bis das Installationsprogramm abgeschlossen ist](/images/guides/macos-install/4-jre.png)

### Schritt 3: Installation erlauben

Wenn Sie die Erfolgsmeldung sehen, ist Java installiert! Klicken Sie auf **Schließen**, um den Vorgang abzuschließen.

![Java-Installation abgeschlossen](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Nachdem Java installiert ist, können Sie den I2P Router installieren.

### Schritt 4: Java installieren

Besuchen Sie die [Downloads-Seite](/downloads/) und laden Sie das Installationsprogramm **I2P für Unix/Linux/BSD/Solaris** herunter (die `.jar`-Datei).

![I2P-Installer herunterladen](/images/guides/macos-install/0-i2p.png)

### Schritt 5: Warten Sie auf die Installation

Doppelklicken Sie auf die heruntergeladene Datei `i2pinstall_X.X.X.jar`. Der Installer wird gestartet und fordert Sie auf, Ihre bevorzugte Sprache auszuwählen.

![Wählen Sie Ihre Sprache](/images/guides/macos-install/1-i2p.png)

### Schritt 6: Installation abgeschlossen

Lesen Sie die Willkommensnachricht und klicken Sie auf **Weiter**, um fortzufahren.

![Installer-Einleitung](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

Der Installer zeigt einen wichtigen Hinweis zu Updates an. I2P-Updates sind **Ende-zu-Ende signiert** und verifiziert, auch wenn dieser Installer selbst nicht signiert ist. Klicken Sie auf **Weiter**.

![Wichtiger Hinweis zu Updates](/images/guides/macos-install/3-i2p.png)

### Schritt 1: I2P herunterladen

Lesen Sie die I2P-Lizenzvereinbarung (BSD-artige Lizenz). Klicken Sie auf **Weiter**, um zu akzeptieren.

![Lizenzvereinbarung](/images/guides/macos-install/4-i2p.png)

### Schritt 2: Installationsprogramm ausführen

Wählen Sie aus, wo I2P installiert werden soll. Der Standardspeicherort (`/Applications/i2p`) wird empfohlen. Klicken Sie auf **Weiter**.

![Installationsverzeichnis auswählen](/images/guides/macos-install/5-i2p.png)

### Schritt 3: Willkommensbildschirm

Lassen Sie alle Komponenten für eine vollständige Installation ausgewählt. Klicken Sie auf **Weiter**.

![Komponenten zur Installation auswählen](/images/guides/macos-install/6-i2p.png)

### Schritt 4: Wichtiger Hinweis

Überprüfen Sie Ihre Auswahl und klicken Sie auf **Weiter**, um die Installation von I2P zu starten.

![Installation starten](/images/guides/macos-install/7-i2p.png)

### Schritt 5: Lizenzvereinbarung

Der Installer kopiert die I2P-Dateien auf Ihr System. Dies dauert etwa 1-2 Minuten.

![Installation läuft](/images/guides/macos-install/8-i2p.png)

### Schritt 6: Installationsverzeichnis auswählen

Der Installer erstellt Startskripte zum Starten von I2P.

![Skripte zum Starten werden generiert](/images/guides/macos-install/9-i2p.png)

### Schritt 7: Komponenten auswählen

Der Installer bietet an, Desktop-Verknüpfungen und Menüeinträge zu erstellen. Treffen Sie Ihre Auswahl und klicken Sie auf **Weiter**.

![Verknüpfungen erstellen](/images/guides/macos-install/10-i2p.png)

### Schritt 8: Installation starten

Erfolg! I2P ist jetzt installiert. Klicken Sie auf **Fertig**, um den Vorgang abzuschließen.

![Installation abgeschlossen](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Lassen Sie uns nun I2P durch Hinzufügen zum Programme-Ordner und Dock einfach starten.

### Schritt 9: Dateien installieren

Öffnen Sie den Finder und navigieren Sie zu Ihrem **Programme**-Ordner.

![Öffne den Anwendungen-Ordner](/images/guides/macos-install/0-conf.png)

### Schritt 10: Startskripte generieren

Suchen Sie nach dem **I2P**-Ordner oder der Anwendung **Start I2P Router** in `/Applications/i2p/`.

![I2P-Launcher finden](/images/guides/macos-install/1-conf.png)

### Schritt 11: Installationsverknüpfungen

Ziehen Sie die Anwendung **Start I2P Router** in Ihr Dock für einfachen Zugriff. Sie können auch ein Alias auf Ihrem Schreibtisch erstellen.

![I2P zum Dock hinzufügen](/images/guides/macos-install/2-conf.png)

**Tipp**: Klicken Sie mit der rechten Maustaste auf das I2P-Symbol im Dock und wählen Sie **Optionen → Im Dock behalten**, um es dauerhaft zu fixieren.

## Part Four: Configure I2P Bandwidth

Wenn Sie I2P zum ersten Mal starten, durchlaufen Sie einen Einrichtungsassistenten, um Ihre Bandbreiteneinstellungen zu konfigurieren. Dies hilft dabei, die Leistung von I2P für Ihre Verbindung zu optimieren.

### Schritt 12: Installation abgeschlossen

Klicken Sie auf das I2P-Symbol in Ihrem Dock (oder doppelklicken Sie auf das Startprogramm). Ihr Standard-Webbrowser öffnet sich mit der I2P Router Console.

![I2P Router Console Willkommensbildschirm](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

Der Setup-Assistent begrüßt Sie. Klicken Sie auf **Weiter**, um mit der Konfiguration von I2P zu beginnen.

![Setup-Assistent Einführung](/images/guides/macos-install/1-wiz.png)

### Schritt 1: Ordner „Programme" öffnen

Wählen Sie Ihre bevorzugte **Oberflächensprache** und wählen Sie zwischen **hellem** oder **dunklem** Design. Klicken Sie auf **Weiter**.

![Sprache und Theme auswählen](/images/guides/macos-install/2-wiz.png)

### Schritt 2: I2P Launcher finden

Der Wizard erklärt den Bandbreitentest. Dieser Test verbindet sich mit dem **M-Lab**-Dienst, um Ihre Internetgeschwindigkeit zu messen. Klicken Sie auf **Weiter**, um fortzufahren.

![Bandwidth test explanation](/images/guides/macos-install/3-wiz.png)

### Schritt 3: Zum Dock hinzufügen

Klicken Sie auf **Test ausführen**, um Ihre Upload- und Download-Geschwindigkeiten zu messen. Der Test dauert etwa 30-60 Sekunden.

![Durchführen des Bandbreitentests](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Überprüfen Sie Ihre Testergebnisse. I2P wird Bandbreiteneinstellungen basierend auf Ihrer Verbindungsgeschwindigkeit empfehlen.

![Bandwidth-Testergebnisse](/images/guides/macos-install/5-wiz.png)

### Schritt 1: I2P starten

Wählen Sie aus, wie viel Bandbreite Sie mit dem I2P-Netzwerk teilen möchten:

- **Automatisch** (Empfohlen): I2P verwaltet die Bandbreite basierend auf Ihrer Nutzung
- **Begrenzt**: Legen Sie spezifische Upload-/Download-Limits fest
- **Unbegrenzt**: Teilen Sie so viel wie möglich (für schnelle Verbindungen)

Klicken Sie auf **Weiter**, um Ihre Einstellungen zu speichern.

![Bandbreitenfreigabe konfigurieren](/images/guides/macos-install/6-wiz.png)

### Schritt 2: Willkommens-Assistent

Ihr I2P-Router ist jetzt konfiguriert und läuft! Die Router-Konsole zeigt Ihren Verbindungsstatus an und ermöglicht Ihnen das Browsen von I2P-Sites.

## Getting Started with I2P

Nachdem I2P installiert und konfiguriert ist, können Sie:

1. **I2P-Seiten durchsuchen**: Besuchen Sie die [I2P-Homepage](http://127.0.0.1:7657/home), um Links zu beliebten I2P-Diensten zu sehen
2. **Browser konfigurieren**: Richten Sie ein [Browser-Profil](/docs/guides/browser-config) ein, um auf `.i2p`-Seiten zuzugreifen
3. **Dienste erkunden**: Entdecken Sie I2P-E-Mail, Foren, Filesharing und mehr
4. **Router überwachen**: Die [Konsole](http://127.0.0.1:7657/console) zeigt Ihren Netzwerkstatus und Statistiken an

### Schritt 3: Sprache und Theme

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Konfiguration**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Adressbuch**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Bandbreiteneinstellungen**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Wenn Sie Ihre Bandbreiteneinstellungen ändern oder I2P später neu konfigurieren möchten, können Sie den Willkommensassistenten erneut über die Router Console ausführen:

1. Gehen Sie zum [I2P Setup Wizard](http://127.0.0.1:7657/welcome)
2. Folgen Sie den Wizard-Schritten erneut

## Troubleshooting

### Schritt 4: Informationen zum Bandbreitentest

- **Java überprüfen**: Stellen Sie sicher, dass Java installiert ist, indem Sie `java -version` im Terminal ausführen
- **Berechtigungen überprüfen**: Stellen Sie sicher, dass der I2P-Ordner die richtigen Berechtigungen hat
- **Logs überprüfen**: Sehen Sie sich `~/.i2p/wrapper.log` auf Fehlermeldungen an

### Schritt 5: Bandbreitentest durchführen

- Stelle sicher, dass I2P läuft (prüfe die Router Console)
- Konfiguriere die Proxy-Einstellungen deines Browsers, um den HTTP-Proxy `127.0.0.1:4444` zu verwenden
- Warte nach dem Start 5-10 Minuten, bis sich I2P ins Netzwerk integriert hat

### Schritt 6: Testergebnisse

- Führen Sie den Bandbreitentest erneut aus und passen Sie Ihre Einstellungen an
- Stellen Sie sicher, dass Sie Bandbreite mit dem Netzwerk teilen
- Überprüfen Sie Ihren Verbindungsstatus in der Router Console

## Teil Zwei: I2P herunterladen und installieren

Um I2P von Ihrem Mac zu entfernen:

1. Beenden Sie den I2P-Router, falls er läuft
2. Löschen Sie den Ordner `/Applications/i2p`
3. Löschen Sie den Ordner `~/.i2p` (Ihre I2P-Konfiguration und -Daten)
4. Entfernen Sie das I2P-Symbol aus Ihrem Dock

## Next Steps

- **Treten Sie der Community bei**: Besuchen Sie [i2pforum.net](http://i2pforum.net) oder schauen Sie sich I2P auf Reddit an
- **Erfahren Sie mehr**: Lesen Sie die [I2P-Dokumentation](/en/docs), um zu verstehen, wie das Netzwerk funktioniert
- **Beteiligen Sie sich**: Erwägen Sie, zur [I2P-Entwicklung beizutragen](/en/get-involved) oder Infrastruktur zu betreiben

Herzlichen Glückwunsch! Sie sind jetzt Teil des I2P-Netzwerks. Willkommen im unsichtbaren Internet!

---

WICHTIG:  Stellen Sie KEINE Fragen, geben Sie keine Erklärungen und fügen Sie keine Kommentare hinzu. Auch wenn der Text nur eine Überschrift ist oder unvollständig erscheint, übersetzen Sie ihn wie er ist.
