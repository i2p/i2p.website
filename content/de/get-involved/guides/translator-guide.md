---
title: "Übersetzungsleitfaden"
description: "Helfen Sie mit, I2P für Benutzer weltweit zugänglich zu machen, indem Sie die Routerkonsole und die Website übersetzen"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Überblick

Helfen Sie mit, I2P für Benutzer auf der ganzen Welt zugänglich zu machen, indem Sie die I2P-Routerkonsole und Website in Ihre Sprache übersetzen. Übersetzung ist ein fortlaufender Prozess, und Beiträge jeder Größe sind wertvoll.

## Übersetzungsplattform

Wir verwenden **Transifex** für alle I2P-Übersetzungen. Dies ist die einfachste und empfohlene Methode für neue und erfahrene Übersetzer.

### Einstieg mit Transifex

1. **Erstellen Sie ein Konto** bei [Transifex](https://www.transifex.com/)
2. **Treten Sie dem I2P-Projekt bei**: [I2P auf Transifex](https://explore.transifex.com/otf/I2P/)
3. **Bitten Sie um Beitritt** zu Ihrem Sprachteam (oder fordern Sie eine neue Sprache an, falls nicht gelistet)
4. **Beginnen Sie mit der Übersetzung**, sobald sie genehmigt wurde

### Warum Transifex?

- **Benutzerfreundliche Oberfläche** - Keine technischen Kenntnisse erforderlich
- **Translation Memory** - Schlägt Übersetzungen basierend auf vorheriger Arbeit vor
- **Zusammenarbeit** - Arbeiten Sie mit anderen Übersetzern in Ihrer Sprache zusammen
- **Qualitätskontrolle** - Überprüfungsprozess gewährleistet Genauigkeit
- **Automatische Updates** - Änderungen werden mit dem Entwicklungsteam synchronisiert

## Was ist zu übersetzen

### Routerkonsole (Priorität)

Die I2P-Routerkonsole ist die Hauptschnittstelle, die Benutzer beim Ausführen von I2P nutzen. Ihre Übersetzung hat den unmittelbarsten Einfluss auf das Benutzererlebnis.

**Wichtige Bereiche zur Übersetzung:**

- **Hauptschnittstelle** - Navigation, Menüs, Schaltflächen, Statusmeldungen
- **Konfigurationsseiten** - Beschreibungen und Optionen der Einstellungen
- **Hilfedokumentation** - Eingebaute Hilfedateien und Tooltips
- **Nachrichten und Updates** - Anfangs-Newsfeed, der Benutzern angezeigt wird
- **Fehlermeldungen** - Benutzerseitige Fehler- und Warnmeldungen
- **Proxy-Konfigurationen** - HTTP-, SOCKS- und Tunnel-Setup-Seiten

Alle Übersetzungen der Routerkonsole werden auf Transifex im `.po` (gettext) Format verwaltet.

## Übersetzungsrichtlinien

### Stil und Ton

- **Klar und prägnant** - I2P behandelt technische Konzepte; halten Sie die Übersetzungen einfach
- **Konsistente Terminologie** - Verwenden Sie die gleichen Begriffe durchgehend (prüfen Sie das Translation Memory)
- **Formal vs. Informell** - Folgen Sie den Konventionen Ihrer Sprache
- **Formatierung beibehalten** - Platzhalter wie `{0}`, `%s`, `<b>tags</b>` intakt lassen

### Technische Überlegungen

- **Codierung** - Verwenden Sie immer UTF-8-Codierung
- **Platzhalter** - Übersetzen Sie keine Variablen-Platzhalter (`{0}`, `{1}`, `%s`, etc.)
- **HTML/Markdown** - Erhalten Sie HTML-Tags und Markdown-Formatierungen
- **Links** - Belassen Sie URLs unverändert, es sei denn, es gibt eine lokalisierte Version
- **Abkürzungen** - Überlegen Sie, ob Sie sie übersetzen oder das Original behalten (z.B. "KB/s", "HTTP")

### Testen Ihrer Übersetzungen

Falls Sie Zugang zu einem I2P-Router haben:

1. Laden Sie die neuesten Übersetzungsdateien von Transifex herunter
2. Platzieren Sie diese in Ihrer I2P-Installation
3. Starten Sie die Routerkonsole neu
4. Überprüfen Sie die Übersetzungen im Kontext
5. Melden Sie etwaige Probleme oder Verbesserungen

## Hilfe erhalten

### Community-Unterstützung

- **IRC-Kanal**: `#i2p-dev` auf I2P IRC oder OFTC
- **Forum**: I2P-Entwicklungsforen
- **Transifex-Kommentare**: Stellen Sie Fragen direkt zu Übersetzungsstrings

### Häufige Fragen

**F: Wie oft sollte ich übersetzen?**
Übersetzen Sie in Ihrem eigenen Tempo. Selbst das Übersetzen einiger Strings hilft. Das Projekt ist fortlaufend.

**F: Was ist, wenn meine Sprache nicht aufgelistet ist?**
Fordern Sie eine neue Sprache auf Transifex an. Wenn Bedarf besteht, wird das Team sie hinzufügen.

**F: Kann ich alleine übersetzen oder benötige ich ein Team?**
Sie können alleine beginnen. Wenn mehr Übersetzer zu Ihrer Sprache hinzukommen, können Sie zusammenarbeiten.

**F: Wie weiß ich, was übersetzt werden muss?**
Transifex zeigt Fertigstellungsprozentsätze an und hebt nicht übersetzte Strings hervor.

**F: Was, wenn ich mit einer bestehenden Übersetzung nicht einverstanden bin?**
Schlagen Sie Verbesserungen in Transifex vor. Prüfer werden die Änderungen bewerten.

## Erweitert: Manuelle Übersetzung (Optional)

Für erfahrene Übersetzer, die direkten Zugriff auf Quell-Dateien wünschen:

### Anforderungen

- **Git** - Versionskontrollsystem
- **POEdit** oder Texteditor - Zum Bearbeiten von `.po` Dateien
- **Grundlegende Befehlszeilenkenntnisse**

### Prozess

1. **Repository klonen**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Übersetzungsdateien finden**:
   - Routerkonsole: `apps/routerconsole/locale/`
   - Suchen nach `messages_xx.po` (wobei `xx` ihr Sprachcode ist)

3. **Übersetzungen bearbeiten**:
   - Verwenden Sie POEdit oder einen Texteditor
   - Speichern Sie mit UTF-8-Codierung

4. **Lokal testen** (falls I2P installiert ist)

5. **Änderungen einreichen**:
   - Erstellen Sie eine Merge-Anfrage auf [I2P Git](https://i2pgit.org/)
   - Oder teilen Sie Ihre `.po` Datei mit dem Entwicklungsteam

**Hinweis**: Die meisten Übersetzer sollten Transifex verwenden. Manuelle Übersetzung ist nur für diejenigen, die mit Git und Entwicklungsworkflows vertraut sind.

## Vielen Dank

Jede Übersetzung hilft, I2P für Benutzer weltweit zugänglicher zu machen. Ob Sie einige Strings oder ganze Abschnitte übersetzen, Ihr Beitrag hat einen echten Einfluss darauf, Menschen dabei zu helfen, ihre Privatsphäre online zu schützen.

**Bereit zu starten?** [Treten Sie I2P auf Transifex bei →](https://explore.transifex.com/otf/I2P/)
