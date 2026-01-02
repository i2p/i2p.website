---
title: "Leitfaden für neue Übersetzer"
description: "So tragen Sie Übersetzungen zur I2P-Website und Router-Konsole über Transifex oder manuelle Methoden bei"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

Möchtest du helfen, I2P für mehr Menschen auf der ganzen Welt zugänglich zu machen? Übersetzungen sind einer der wertvollsten Beiträge, die du zum Projekt leisten kannst. Diese Anleitung führt dich durch die Übersetzung der Router-Konsole.

## Übersetzungsmethoden

Es gibt zwei Möglichkeiten, Übersetzungen beizutragen:

### Methode 1: Transifex (Empfohlen)

**Dies ist der einfachste Weg, I2P zu übersetzen.** Transifex bietet eine webbasierte Oberfläche, die das Übersetzen einfach und zugänglich macht.

1. Registrieren Sie sich bei [Transifex](https://www.transifex.com/otf/I2P/)
2. Beantragen Sie die Aufnahme in das I2P-Übersetzungsteam
3. Beginnen Sie direkt in Ihrem Browser mit dem Übersetzen

Keine technischen Kenntnisse erforderlich - einfach anmelden und mit dem Übersetzen beginnen!

### Methode 2: Manuelle Übersetzung

Für Übersetzer, die lieber mit Git und lokalen Dateien arbeiten, oder für Sprachen, die noch nicht auf Transifex eingerichtet sind.

**Voraussetzungen:** - Vertrautheit mit git-Versionsverwaltung - Texteditor oder Übersetzungstool (POEdit empfohlen) - Kommandozeilen-Tools: git, gettext

**Einrichtung:** 1. Tritt [#i2p-dev auf IRC](/contact/#irc) bei und stelle dich vor 2. Aktualisiere den Übersetzungsstatus im Wiki (frage im IRC nach Zugriff) 3. Klone das entsprechende Repository (siehe Abschnitte unten)

---

## Routerkonsole Übersetzung

Die Router-Konsole ist die Weboberfläche, die Sie beim Betrieb von I2P sehen. Ihre Übersetzung hilft Benutzern, die nicht mit Englisch vertraut sind.

### Transifex verwenden (Empfohlen)

1. Gehe zu [I2P auf Transifex](https://www.transifex.com/otf/I2P/)
2. Wähle das router console Projekt aus
3. Wähle deine Sprache
4. Beginne mit der Übersetzung

### Manuelle Router Console Übersetzung

**Voraussetzungen:** - Gleich wie bei der Website-Übersetzung (git, gettext) - GPG-Schlüssel (für Commit-Zugriff) - Unterzeichnete Entwicklervereinbarung

**Klone das Haupt-I2P-Repository:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Zu übersetzende Dateien:**

Die Router-Konsole hat ungefähr 15 Dateien, die übersetzt werden müssen:

1. **Kern-Interface-Dateien:**
   - `apps/routerconsole/locale/messages_*.po` - Hauptkonsolen-Meldungen
   - `apps/routerconsole/locale-news/messages_*.po` - Nachrichten-Meldungen

2. **Proxy-Dateien:**
   - `apps/i2ptunnel/locale/messages_*.po` - Tunnel-Konfigurationsoberfläche

3. **Anwendungs-Locales:**
   - `apps/susidns/locale/messages_*.po` - Adressbuch-Oberfläche
   - `apps/susimail/locale/messages_*.po` - E-Mail-Oberfläche
   - Weitere anwendungsspezifische Locale-Verzeichnisse

4. **Dokumentationsdateien:**
   - `installer/resources/readme/readme_*.html` - Installations-Readme
   - Hilfedateien in verschiedenen Apps

**Übersetzungsworkflow:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Reichen Sie Ihre Arbeit ein:** - Erstellen Sie einen Merge Request auf [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) - Oder teilen Sie Dateien mit dem Entwicklungsteam im IRC

---

## Übersetzungswerkzeuge

### POEdit (Sehr empfohlen)

[POEdit](https://poedit.net/) ist ein spezialisierter Editor für .po-Übersetzungsdateien.

**Funktionen:** - Visuelle Benutzeroberfläche für Übersetzungsarbeiten - Zeigt Übersetzungskontext an - Automatische Validierung - Verfügbar für Windows, macOS und Linux

### Texteditoren

Sie können auch jeden beliebigen Texteditor verwenden: - VS Code (mit i18n-Erweiterungen) - Sublime Text - vim/emacs (für Terminal-Nutzer)

### Qualitätsprüfungen

Vor dem Einreichen: 1. **Formatierung überprüfen:** Stellen Sie sicher, dass Platzhalter wie `%s` und `{0}` unverändert bleiben 2. **Übersetzungen testen:** Installieren und starten Sie I2P, um zu sehen, wie sie aussehen 3. **Konsistenz:** Halten Sie die Terminologie über alle Dateien hinweg einheitlich 4. **Länge:** Einige Zeichenketten haben Platzbeschränkungen in der Benutzeroberfläche

---

## Tipps für Übersetzer

### Allgemeine Richtlinien

- **Bleiben Sie konsistent:** Verwenden Sie durchgehend die gleichen Übersetzungen für häufige Begriffe
- **Formatierung beibehalten:** Bewahren Sie HTML-Tags, Platzhalter (`%s`, `{0}`) und Zeilenumbrüche
- **Kontext ist wichtig:** Lesen Sie den englischen Quelltext sorgfältig, um den Kontext zu verstehen
- **Fragen stellen:** Nutzen Sie IRC oder Foren, wenn etwas unklar ist

### Häufige I2P-Begriffe

Einige Begriffe sollten auf Englisch bleiben oder sorgfältig transliteriert werden:

- **I2P** - Keep as is
- **eepsite** - I2P-Website (kann in Ihrer Sprache eine Erklärung erfordern)
- **tunnel** - Verbindungspfad (Tor-Terminologie wie „circuit" vermeiden)
- **netDb** - Netzwerkdatenbank
- **floodfill** - Routertyp
- **destination** - I2P-Adressendpunkt

### Testen Ihrer Übersetzungen

1. Erstellen Sie I2P mit Ihren Übersetzungen
2. Ändern Sie die Sprache in den Einstellungen der Router-Konsole
3. Navigieren Sie durch alle Seiten, um zu überprüfen:
   - Text passt in UI-Elemente
   - Keine unleserlichen Zeichen (Kodierungsprobleme)
   - Übersetzungen ergeben im Kontext Sinn

---

## Häufig gestellte Fragen

### Warum ist der Übersetzungsprozess so komplex?

Der Prozess verwendet Versionskontrolle (git) und Standard-Übersetzungswerkzeuge (.po-Dateien), weil:

1. **Verantwortlichkeit:** Nachverfolgung, wer was und wann geändert hat
2. **Qualität:** Überprüfung von Änderungen, bevor sie veröffentlicht werden
3. **Konsistenz:** Aufrechterhaltung der richtigen Dateiformatierung und -struktur
4. **Skalierbarkeit:** Effiziente Verwaltung von Übersetzungen in mehreren Sprachen
5. **Zusammenarbeit:** Mehrere Übersetzer können an derselben Sprache arbeiten

### Benötige ich Programmierkenntnisse?

**Nein!** Wenn Sie Transifex verwenden, benötigen Sie nur: - Fließende Kenntnisse in Englisch und Ihrer Zielsprache - Einen Webbrowser - Grundlegende Computerkenntnisse

Für die manuelle Übersetzung benötigen Sie grundlegende Kommandozeilen-Kenntnisse, aber keine Programmierkenntnisse.

### Wie lange dauert es?

- **Router-Konsole:** Ungefähr 15-20 Stunden für alle Dateien
- **Wartung:** Ein paar Stunden pro Monat, um neue Zeichenketten zu aktualisieren

### Können mehrere Personen an einer Sprache arbeiten?

Ja! Koordination ist entscheidend: - Verwenden Sie Transifex für die automatische Koordination - Für manuelle Arbeit kommunizieren Sie im IRC-Kanal #i2p-dev - Teilen Sie die Arbeit nach Abschnitten oder Dateien auf

### Was ist, wenn meine Sprache nicht aufgeführt ist?

Fordern Sie es auf Transifex an oder kontaktieren Sie das Team im IRC. Das Entwicklungsteam kann eine neue Sprache schnell einrichten.

### Wie kann ich meine Übersetzungen vor dem Einreichen testen?

- Erstelle I2P aus dem Quellcode mit deinen Übersetzungen
- Installiere und führe es lokal aus
- Ändere die Sprache in den Konsoleneinstellungen

---

## Hilfe erhalten

### IRC-Support

Tritt [#i2p-dev auf IRC](/contact/#irc) bei für: - Technische Hilfe mit Übersetzungswerkzeugen - Fragen zur I2P-Terminologie - Koordination mit anderen Übersetzern - Direkte Unterstützung von Entwicklern

### Foren

- Übersetzungsdiskussionen im [I2P Forum](http://i2pforum.net/)
- Inside I2P: Übersetzungsforum auf zzz.i2p (erfordert I2P router)

### Dokumentation

- [Transifex-Dokumentation](https://docs.transifex.com/)
- [POEdit-Dokumentation](https://poedit.net/support)
- [gettext-Handbuch](https://www.gnu.org/software/gettext/manual/)

---

## Anerkennung

Alle Übersetzer werden genannt in: - Der I2P Router-Konsole (Info-Seite) - Website-Credits-Seite - Git-Commit-Verlauf - Veröffentlichungsankündigungen

Ihre Arbeit hilft Menschen auf der ganzen Welt direkt dabei, I2P sicher und privat zu nutzen. Vielen Dank für Ihren Beitrag!

---

## Nächste Schritte

Bereit zum Übersetzen?

1. **Wählen Sie Ihre Methode:**
   - Schnellstart: [Auf Transifex registrieren](https://www.transifex.com/otf/I2P/)
   - Manueller Ansatz: Treten Sie [#i2p-dev auf IRC](/contact/#irc) bei

2. **Klein anfangen:** Übersetzen Sie ein paar Zeichenketten, um sich mit dem Prozess vertraut zu machen

3. **Um Hilfe bitten:** Zögern Sie nicht, sich über IRC oder Foren zu melden

**Vielen Dank, dass Sie helfen, I2P für alle zugänglich zu machen!**
