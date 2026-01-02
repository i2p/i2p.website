---
title: "Entwicklerrichtlinien und Coding-Stil"
description: "End-to-End-Richtlinien für Beiträge zu I2P: Arbeitsablauf, Veröffentlichungszyklus, Programmierstil, Protokollierung, Lizenzierung und Problembehandlung"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Lesen Sie zuerst den [Leitfaden für neue Entwickler](/docs/develop/new-developers/).

## Grundlegende Richtlinien und Codierungsstil

Das meiste der folgenden Punkte sollte gesunder Menschenverstand für jeden sein, der an Open Source oder in einer kommerziellen Programmierumgebung gearbeitet hat. Das Folgende gilt hauptsächlich für den Hauptentwicklungszweig i2p.i2p. Richtlinien für andere Zweige, Plugins und externe Anwendungen können erheblich abweichen; wenden Sie sich an den entsprechenden Entwickler für weitere Hinweise.

### Gemeinschaft

- Bitte schreiben Sie nicht nur Code. Wenn möglich, beteiligen Sie sich an anderen Entwicklungsaktivitäten, einschließlich: Entwicklungsdiskussionen und Support auf IRC und i2pforum.i2p; Testen; Fehlerberichte und Antworten; Dokumentation; Code-Reviews; usw.
- Aktive Entwickler sollten regelmäßig auf IRC `#i2p-dev` verfügbar sein. Achten Sie auf den aktuellen Release-Zyklus. Halten Sie sich an Release-Meilensteine wie Feature Freeze, Tag Freeze und die Check-in-Deadline für ein Release.

### Veröffentlichungszyklus

Der normale Veröffentlichungszyklus beträgt 10–16 Wochen, vier Veröffentlichungen pro Jahr. Im Folgenden sind die ungefähren Fristen innerhalb eines typischen 13-Wochen-Zyklus aufgeführt. Die tatsächlichen Fristen für jede Veröffentlichung werden vom Release-Manager nach Rücksprache mit dem gesamten Team festgelegt.

- 1–2 Tage nach der vorherigen Veröffentlichung: Check-ins in den Trunk sind erlaubt.
- 2–3 Wochen nach der vorherigen Veröffentlichung: Frist für die Übertragung größerer Änderungen von anderen Branches in den Trunk.
- 4–5 Wochen vor der Veröffentlichung: Frist für die Anforderung neuer Startseiten-Links.
- 3–4 Wochen vor der Veröffentlichung: Feature Freeze. Frist für größere neue Funktionen.
- 2–3 Wochen vor der Veröffentlichung: Projektbesprechung abhalten, um neue Startseiten-Link-Anfragen zu prüfen, falls vorhanden.
- 10–14 Tage vor der Veröffentlichung: String Freeze. Keine weiteren Änderungen an übersetzten (getaggten) Strings. Strings zu Transifex pushen, Übersetzungsfrist auf Transifex ankündigen.
- 10–14 Tage vor der Veröffentlichung: Feature-Frist. Nach diesem Zeitpunkt nur noch Fehlerbehebungen. Keine weiteren Funktionen, Refactoring oder Aufräumarbeiten.
- 3–4 Tage vor der Veröffentlichung: Übersetzungsfrist. Übersetzungen von Transifex pullen und einchecken.
- 3–4 Tage vor der Veröffentlichung: Check-in-Frist. Nach diesem Zeitpunkt keine Check-ins mehr ohne Genehmigung des Release-Builders.
- Stunden vor der Veröffentlichung: Code-Review-Frist.

### Git

- Haben Sie ein grundlegendes Verständnis von verteilten Quellcode-Verwaltungssystemen, auch wenn Sie git noch nicht verwendet haben. Bitten Sie um Hilfe, wenn Sie sie benötigen. Einmal gepusht, sind Check-ins für immer; es gibt kein Rückgängigmachen. Bitte seien Sie vorsichtig. Wenn Sie git noch nicht verwendet haben, beginnen Sie mit kleinen Schritten. Checken Sie einige kleine Änderungen ein und sehen Sie, wie es läuft.
- Testen Sie Ihre Änderungen, bevor Sie sie einchecken. Wenn Sie das Check-in-vor-Test-Entwicklungsmodell bevorzugen, verwenden Sie Ihren eigenen Entwicklungszweig in Ihrem eigenen Konto und erstellen Sie einen MR, sobald die Arbeit abgeschlossen ist. Brechen Sie nicht den Build. Verursachen Sie keine Regressionen. Falls Sie es doch tun (es passiert), verschwinden Sie bitte nicht für längere Zeit, nachdem Sie Ihre Änderung gepusht haben.
- Wenn Ihre Änderung nicht trivial ist oder Sie möchten, dass Leute sie testen, und Sie gute Testberichte benötigen, um zu wissen, ob Ihre Änderung getestet wurde oder nicht, fügen Sie einen Check-in-Kommentar zu `history.txt` hinzu und erhöhen Sie die Build-Revision in `RouterVersion.java`.
- Checken Sie keine größeren Änderungen in den Haupt-i2p.i2p-Branch spät im Release-Zyklus ein. Wenn ein Projekt mehr als ein paar Tage dauern wird, erstellen Sie Ihren eigenen Branch in git, in Ihrem eigenen Konto, und führen Sie die Entwicklung dort durch, damit Sie keine Releases blockieren.
- Für große Änderungen (im Allgemeinen mehr als 100 Zeilen oder mehr als drei Dateien betreffend) checken Sie sie in einen neuen Branch in Ihrem eigenen GitLab-Konto ein, erstellen Sie einen MR und weisen Sie einen Reviewer zu. Weisen Sie den MR sich selbst zu. Mergen Sie den MR selbst, sobald der Reviewer ihn genehmigt.
- Erstellen Sie keine WIP-Branches im Haupt-I2P_Developers-Konto (außer für i2p.www). WIP gehört in Ihr eigenes Konto. Wenn die Arbeit abgeschlossen ist, erstellen Sie einen MR. Die einzigen Branches im Hauptkonto sollten für echte Forks sein, wie ein Point-Release.
- Führen Sie die Entwicklung transparent und mit der Community im Hinterkopf durch. Checken Sie häufig ein. Checken Sie ein oder mergen Sie in den Haupt-Branch so häufig wie möglich, unter Berücksichtigung der obigen Richtlinien. Wenn Sie an einem großen Projekt in Ihrem eigenen Branch/Konto arbeiten, lassen Sie es die Leute wissen, damit sie folgen und reviewen/testen/kommentieren können.

### Coding-Stil

- Der Coding-Stil verwendet in den meisten Teilen des Codes 4 Leerzeichen für die Einrückung. Verwenden Sie keine Tabs. Formatieren Sie Code nicht neu. Wenn Ihre IDE oder Ihr Editor alles neu formatieren möchte, behalten Sie die Kontrolle darüber. An manchen Stellen ist der Coding-Stil anders. Nutzen Sie gesunden Menschenverstand. Ahmen Sie den Stil der Datei nach, die Sie ändern.
- Alle neuen public- und package-private-Klassen und -Methoden benötigen Javadocs. Fügen Sie `@since` release-number hinzu. Javadocs für neue private Methoden sind wünschenswert.
- Für alle hinzugefügten Javadocs darf es keine doclint-Fehler oder -Warnungen geben. Führen Sie `ant javadoc` mit Oracle Java 14 oder höher aus, um zu prüfen. Alle Parameter müssen `@param`-Zeilen haben, alle nicht-void-Methoden müssen `@return`-Zeilen haben, alle als geworfen deklarierten Exceptions müssen `@throws`-Zeilen haben, und es darf keine HTML-Fehler geben.
- Klassen in `core/` (i2p.jar) und Teile von i2ptunnel sind Teil unserer offiziellen API. Es gibt mehrere externe Plugins und andere Anwendungen, die auf dieser API basieren. Seien Sie vorsichtig, keine Änderungen vorzunehmen, die die Kompatibilität brechen. Fügen Sie der API keine Methoden hinzu, es sei denn, sie sind von allgemeinem Nutzen. Javadocs für API-Methoden sollten klar und vollständig sein. Wenn Sie die API hinzufügen oder ändern, aktualisieren Sie auch die Dokumentation auf der Website (i2p.www branch).
- Markieren Sie Strings für die Übersetzung, wo es angebracht ist, was für alle UI-Strings gilt. Ändern Sie bestehende markierte Strings nicht, außer wenn es wirklich notwendig ist, da dies vorhandene Übersetzungen beschädigt. Fügen Sie nach dem tag freeze im Release-Zyklus keine markierten Strings hinzu oder ändern Sie diese nicht, damit Übersetzer die Möglichkeit haben, vor dem Release zu aktualisieren.
- Verwenden Sie Generics und Concurrent-Klassen, wo möglich. I2P ist eine hochgradig multi-threaded Anwendung.
- Machen Sie sich mit häufigen Java-Fallstricken vertraut, die von FindBugs/SpotBugs erkannt werden. Führen Sie `ant findbugs` aus, um mehr zu erfahren.
- Java 8 ist seit Release 0.9.47 erforderlich, um I2P zu bauen und auszuführen. Verwenden Sie keine Java-7- oder -8-Klassen oder -Methoden in eingebetteten Subsystemen: addressbook, core, i2ptunnel.jar (non‑UI), mstreaming, router, routerconsole (nur news), streaming. Diese Subsysteme werden von Android und eingebetteten Anwendungen verwendet, die nur Java 6 erfordern. Alle Klassen müssen in Android API 14 verfügbar sein. Java-7-Sprachfeatures sind in diesen Subsystemen akzeptabel, wenn sie von der aktuellen Version des Android SDK unterstützt werden und sie zu Java-6-kompatiblem Code kompilieren.
- Try‑with‑resources kann nicht in eingebetteten Subsystemen verwendet werden, da es `java.lang.AutoCloseable` in der Runtime erfordert, und dies ist erst ab Android API 19 (KitKat 4.4) verfügbar.
- Das `java.nio.file`-Paket kann nicht in eingebetteten Subsystemen verwendet werden, da es erst ab Android API 26 (Oreo 8) verfügbar ist.
- Abgesehen von den oben genannten Einschränkungen dürfen Java-8-Klassen, -Methoden und -Konstrukte nur in den folgenden Subsystemen verwendet werden: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (außer news), SAM, susidns, susimail, systray.
- Plugin-Autoren können über die `plugin.config`-Datei jede Mindest-Java-Version voraussetzen.
- Konvertieren Sie explizit zwischen primitiven Typen und Klassen; verlassen Sie sich nicht auf Autoboxing/Unboxing.
- Verwenden Sie nicht `URL`. Verwenden Sie `URI`.
- Fangen Sie nicht `Exception`. Fangen Sie `RuntimeException` und geprüfte Exceptions einzeln.
- Verwenden Sie nicht `String.getBytes()` ohne ein UTF‑8-Charset-Argument. Sie können auch `DataHelper.getUTF8()` oder `DataHelper.getASCII()` verwenden.
- Geben Sie immer ein UTF‑8-Charset an, wenn Sie Dateien lesen oder schreiben. Die `DataHelper`-Utilities können hilfreich sein.
- Geben Sie immer eine Locale (z. B. `Locale.US`) an, wenn Sie `String.toLowerCase()` oder `String.toUpperCase()` verwenden. Verwenden Sie nicht `String.equalsIgnoreCase()`, da keine Locale angegeben werden kann.
- Verwenden Sie nicht `String.split()`. Verwenden Sie `DataHelper.split()`.
- Fügen Sie keinen Code zum Formatieren von Datums- und Zeitangaben hinzu. Verwenden Sie `DataHelper.formatDate()` und `DataHelper.formatTime()`.
- Stellen Sie sicher, dass `InputStream`s und `OutputStream`s in finally-Blöcken geschlossen werden.
- Verwenden Sie `{}` für alle `for`- und `while`-Blöcke, auch wenn es nur eine Zeile ist. Wenn Sie `{}` für entweder den `if`-, `else`- oder `if-else`-Block verwenden, verwenden Sie es für alle Blöcke. Setzen Sie `} else {` auf eine einzelne Zeile.
- Geben Sie Felder wo immer möglich als `final` an.
- Speichern Sie `I2PAppContext`, `RouterContext`, `Log` oder andere Referenzen auf router- oder context-Elemente nicht in statischen Feldern.
- Starten Sie keine Threads in Konstruktoren. Verwenden Sie `I2PAppThread` anstelle von `Thread`.

### Protokollierung

Die folgenden Richtlinien gelten für den Router, Webapps und alle Plugins.

- Für alle Nachrichten, die nicht auf der Standard-Log-Ebene angezeigt werden (WARN, INFO und DEBUG), verwenden Sie immer `log.shouldWarn()`, `log.shouldInfo()` oder `log.shouldDebug()` vor dem Log-Aufruf, um unnötigen Object-Churn zu vermeiden – es sei denn, die Nachricht ist ein statischer String (keine Verkettung).
- Log-Nachrichten, die möglicherweise auf der Standard-Log-Ebene angezeigt werden (ERROR, CRIT und `logAlways()`), sollten kurz, klar und für einen nicht-technischen Benutzer verständlich sein. Dies schließt Ausnahme-Ursachentexte ein, die möglicherweise ebenfalls angezeigt werden. Erwägen Sie eine Übersetzung, wenn der Fehler wahrscheinlich auftritt (z. B. bei Formularübermittlungsfehlern). Andernfalls ist keine Übersetzung erforderlich, aber es kann hilfreich sein, nach einem String zu suchen, der bereits an anderer Stelle zur Übersetzung markiert ist, und diesen wiederzuverwenden.
- Log-Nachrichten, die nicht auf der Standard-Log-Ebene angezeigt werden (WARN, INFO und DEBUG), sind für die Verwendung durch Entwickler gedacht und unterliegen nicht den oben genannten Anforderungen. WARN-Nachrichten sind jedoch im Android-Log-Tab verfügbar und können Benutzern bei der Fehlerbehebung helfen, daher ist auch bei WARN-Nachrichten etwas Sorgfalt geboten.
- INFO- und DEBUG-Log-Nachrichten sollten sparsam verwendet werden, insbesondere in häufig durchlaufenen Code-Pfaden. Obwohl sie während der Entwicklung nützlich sind, sollten Sie in Betracht ziehen, sie nach Abschluss der Tests zu entfernen oder auszukommentieren.
- Loggen Sie nicht nach stdout oder stderr (Wrapper-Log).

### Lizenzen

- Checken Sie nur Code ein, den Sie selbst geschrieben haben. Bevor Sie Code oder Bibliotheks-JARs aus anderen Quellen einchecken, begründen Sie, warum dies notwendig ist, überprüfen Sie die Lizenzkompatibilität und holen Sie die Genehmigung des Release-Managers ein.
- Falls Sie die Genehmigung erhalten, externen Code oder JARs hinzuzufügen, und Binärdateien in einem Debian- oder Ubuntu-Paket verfügbar sind, müssen Sie Build- und Paketierungsoptionen implementieren, um stattdessen das externe Paket zu verwenden. Checkliste der zu ändernden Dateien: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Für alle Bilder, die aus externen Quellen eingecheckt werden, liegt es in Ihrer Verantwortung, zuerst die Lizenzkompatibilität zu überprüfen. Fügen Sie die Lizenz- und Quelleninformationen im Check-in-Kommentar hinzu.

### Fehler

- Die Verwaltung von Issues ist die Aufgabe aller; bitte helfen Sie mit. Überwachen Sie [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) auf Issues, bei denen Sie helfen können. Kommentieren Sie, beheben Sie und schließen Sie Issues, wenn Sie können.
- Neue Entwickler sollten damit beginnen, Issues zu beheben. Wenn Sie eine Lösung haben, fügen Sie Ihren Patch zum Issue hinzu und fügen Sie das Schlüsselwort `review-needed` hinzu. Schließen Sie das Issue nicht, bis es erfolgreich überprüft wurde und Sie Ihre Änderungen eingecheckt haben. Sobald Sie dies für ein paar Tickets reibungslos durchgeführt haben, können Sie dem normalen Verfahren oben folgen.
- Schließen Sie ein Issue, wenn Sie glauben, es behoben zu haben. Wir haben keine Testabteilung, um Tickets zu überprüfen und zu schließen. Wenn Sie nicht sicher sind, ob Sie es behoben haben, schließen Sie es und fügen Sie eine Notiz hinzu mit dem Text „Ich glaube, ich habe es behoben, bitte testen Sie es und öffnen Sie es erneut, falls es noch defekt ist". Fügen Sie einen Kommentar mit der Dev-Build-Nummer oder Revision hinzu und setzen Sie den Meilenstein auf das nächste Release.
