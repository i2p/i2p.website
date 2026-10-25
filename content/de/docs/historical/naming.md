---
title: "Naming-Diskussion"
description: "Historische Debatte über I2Ps Namensmodell und warum globale DNS-ähnliche Systeme abgelehnt wurden"
slug: "naming"
aliases:
  - "/de/docs/legacy/naming"
  - "/de/docs/legacy/naming/"
  - "/de/naming_discussion"
  - "/de/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

HINWEIS: Das Folgende ist eine Diskussion über die Gründe hinter dem I2P-Benennungssystem, häufige Argumente und mögliche Alternativen. Siehe [die Benennungsseite](/docs/naming) für die aktuelle Dokumentation.

## Verworfene Alternativen

Die Namensgebung innerhalb von I2P war von Anfang an ein viel diskutiertes Thema mit Befürwortern aus dem gesamten Spektrum der Möglichkeiten. Angesichts von I2Ps inhärentem Bedarf nach sicherer Kommunikation und dezentraler Operation ist jedoch das traditionelle DNS-Stil-Namensystem eindeutig ausgeschlossen, ebenso wie "Mehrheitsregeln"-Abstimmungssysteme.

I2P fördert jedoch nicht die Verwendung von DNS-ähnlichen Diensten, da der Schaden durch die Übernahme einer Website enorm sein kann - und unsichere Ziele haben keinen Wert. DNSsec selbst fällt immer noch auf Registrare und Zertifizierungsstellen zurück, während bei I2P Anfragen, die an ein destination gesendet werden, nicht abgefangen oder die Antwort gefälscht werden können, da sie mit den öffentlichen Schlüsseln des destination verschlüsselt sind, und ein destination selbst ist nur ein Paar öffentlicher Schlüssel und ein Zertifikat. DNS-artige Systeme hingegen ermöglichen es jedem der Nameserver im Lookup-Pfad, einfache Denial-of-Service- und Spoofing-Angriffe durchzuführen. Das Hinzufügen eines Zertifikats, das die Antworten als von einer zentralisierten Zertifizierungsstelle signiert authentifiziert, würde viele der feindlichen Nameserver-Probleme beheben, würde aber Replay-Angriffe sowie Angriffe durch feindliche Zertifizierungsstellen offen lassen.

Abstimmungsbasierte Namensvergabe ist ebenfalls gefährlich, insbesondere angesichts der Wirksamkeit von Sybil-Angriffen in anonymen Systemen - der Angreifer kann einfach eine beliebig hohe Anzahl von Peers erstellen und mit jedem "abstimmen", um einen bestimmten Namen zu übernehmen. Proof-of-Work-Methoden können verwendet werden, um Identitäten kostenpflichtig zu machen, aber während das Netzwerk wächst, wird die erforderliche Last, jeden zu kontaktieren, um Online-Abstimmungen durchzuführen, unrealistisch, oder falls nicht das gesamte Netzwerk abgefragt wird, können unterschiedliche Antwortgruppen erreichbar sein.

Wie beim Internet jedoch hält I2P das Design und den Betrieb eines Benennungssystems aus der (IP-ähnlichen) Kommunikationsschicht heraus. Die mitgelieferte Benennungsbibliothek enthält eine einfache Service-Provider-Schnittstelle, in die sich [alternative Benennungssysteme](#alternatives) einklinken können, wodurch Endnutzer bestimmen können, welche Art von Benennungs-Kompromissen sie bevorzugen.

## Diskussion

Siehe auch [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Kommentare von jrandom

(angepasst von einem Beitrag im alten Syndie, 26. November 2005)

F: Was ist zu tun, wenn sich einige Hosts nicht auf eine Adresse einigen können und wenn einige Adressen funktionieren, andere aber nicht? Wer ist die richtige Quelle für einen Namen?

A: Das geht nicht. Das ist tatsächlich ein kritischer Unterschied zwischen Namen in I2P und der Funktionsweise von DNS - Namen in I2P sind menschenlesbar, sicher, aber **nicht global eindeutig**. Das ist beabsichtigt und ein inhärenter Teil unserer Sicherheitsanforderungen.

Wenn ich Sie irgendwie davon überzeugen könnte, das mit einem Namen verknüpfte Ziel zu ändern, würde ich erfolgreich die Seite "übernehmen", und unter keinen Umständen ist das akzeptabel. Stattdessen machen wir Namen **lokal eindeutig**: sie sind das, was *Sie* verwenden, um eine Seite zu bezeichnen, genau wie Sie Dinge nennen können, wie Sie wollen, wenn Sie sie zu den Lesezeichen Ihres Browsers oder der Kontaktliste Ihres IM-Clients hinzufügen. Wen Sie "Chef" nennen, könnte jemand anderes "Sally" nennen.

Namen werden niemals sicher menschenlesbar und global eindeutig sein.

### Kommentare von zzz

Das Folgende von zzz ist eine Überprüfung mehrerer häufiger Beschwerden über I2Ps Benennungssystem.

- **Ineffizienz:** Die gesamte hosts.txt wird heruntergeladen (falls sie sich geändert hat, da eepget die etag- und last-modified-Header verwendet). Sie ist derzeit etwa 400K groß für fast 800 Hosts.

Das stimmt, aber das ist nicht viel Datenverkehr im Kontext von I2P, das selbst extrem ineffizient ist (floodfill-Datenbanken, enormer Verschlüsselungsaufwand und Padding, garlic routing, usw.). Wenn Sie alle 12 Stunden eine hosts.txt-Datei von jemandem herunterladen würden, ergibt das durchschnittlich etwa 10 Bytes/sec.

Wie es in I2P üblich ist, gibt es hier einen grundlegenden Kompromiss zwischen Anonymität und Effizienz. Einige würden sagen, dass die Verwendung der etag- und last-modified-Header gefährlich ist, weil sie preisgeben, wann Sie die Daten zuletzt angefordert haben. Andere haben vorgeschlagen, nur spezifische Schlüssel anzufordern (ähnlich wie es Jump-Services tun, aber auf automatisierte Weise), möglicherweise auf weitere Kosten der Anonymität.

Mögliche Verbesserungen wären ein Ersatz oder eine Ergänzung zum address book (siehe i2host.i2p), oder etwas Einfaches wie das Abonnieren von http://example.i2p/cgi-bin/recenthosts.cgi anstatt http://example.i2p/hosts.txt. Wenn ein hypothetisches recenthosts.cgi beispielsweise alle Hosts der letzten 24 Stunden verteilen würde, könnte das sowohl effizienter als auch anonymer sein als die aktuelle hosts.txt mit last-modified und etag.

Eine Beispielimplementierung ist auf stats.i2p unter http://stats.i2p/cgi-bin/newhosts.txt verfügbar. Dieses Skript gibt ein Etag mit einem Zeitstempel zurück. Wenn eine Anfrage mit dem If-None-Match etag eingeht, gibt das Skript NUR neue Hosts seit diesem Zeitstempel zurück, oder 304 Not Modified falls es keine gibt. Auf diese Weise gibt das Skript effizient nur die Hosts zurück, die dem Abonnenten nicht bekannt sind, in einer mit dem Adressbuch kompatiblen Weise.

Die Ineffizienz ist also kein großes Problem und es gibt mehrere Möglichkeiten, die Dinge ohne radikale Änderungen zu verbessern.

- **Nicht Skalierbar:** Die 400K hosts.txt (mit linearer Suche) ist im Moment noch nicht so groß und wir können wahrscheinlich um das 10- oder 100-fache wachsen, bevor es ein Problem wird.

Was den Netzwerkverkehr betrifft, siehe oben. Aber solange Sie nicht eine langsame Echtzeitabfrage über das Netzwerk für einen Schlüssel durchführen werden, müssen Sie den gesamten Schlüsselsatz lokal gespeichert haben, zu Kosten von etwa 500 Bytes pro Schlüssel.

- **Erfordert Konfiguration und "Vertrauen":** Das standardmäßige Adressbuch ist nur auf http://www.i2p2.i2p/hosts.txt abonniert, welches selten aktualisiert wird, was zu einer schlechten Erfahrung für neue Benutzer führt.

Das ist durchaus beabsichtigt. jrandom möchte, dass ein Benutzer einem hosts.txt-Anbieter "vertraut", und wie er gerne sagt: "Vertrauen ist kein boolescher Wert". Der Konfigurationsschritt versucht, Benutzer dazu zu bringen, über Vertrauensfragen in einem anonymen Netzwerk nachzudenken.

Als weiteres Beispiel listet die Fehlerseite "I2P Site Unknown" im HTTP Proxy einige Jump-Dienste auf, aber "empfiehlt" keinen bestimmten davon, und es liegt am Benutzer, einen auszuwählen (oder auch nicht). jrandom würde sagen, wir vertrauen den aufgelisteten Anbietern genug, um sie aufzulisten, aber nicht genug, um automatisch den Schlüssel von ihnen zu holen.

Wie erfolgreich das ist, bin ich mir nicht sicher. Aber es muss eine Art Vertrauenshierarchie für das Namensystem geben. Alle gleich zu behandeln könnte das Risiko einer Entführung erhöhen.

- **Es ist kein DNS**

Leider würden Echtzeitabfragen über I2P das Surfen im Web erheblich verlangsamen.

Außerdem basiert DNS auf Abfragen mit begrenztem Caching und Time-to-Live, während I2P-Schlüssel dauerhaft sind.

Sicher, wir könnten es zum Laufen bringen, aber warum? Es passt einfach nicht gut.

- **Nicht zuverlässig:** Es hängt von spezifischen Servern für Adressbuch-Abonnements ab.

Ja, es hängt von einigen Servern ab, die Sie konfiguriert haben. Innerhalb von I2P kommen und gehen Server und Dienste. Jedes andere zentralisierte System (zum Beispiel DNS-Root-Server) hätte das gleiche Problem. Ein vollständig dezentralisiertes System (jeder ist autoritativ) ist möglich, indem man eine "jeder ist ein Root-DNS-Server"-Lösung implementiert oder durch etwas noch Einfacheres, wie ein Skript, das jeden aus Ihrer hosts.txt zu Ihrem Adressbuch hinzufügt.

Menschen, die für vollständig autoritäre Lösungen eintreten, haben jedoch im Allgemeinen die Probleme von Konflikten und Hijacking nicht durchdacht.

- **Umständlich, nicht in Echtzeit:** Es ist ein Flickwerk aus hosts.txt-Anbietern, Schlüssel-hinzufügen-Webformular-Anbietern, Jump-Service-Anbietern, I2P-Site-Status-Reportern. Jump-Server und Abonnements sind mühsam, es sollte einfach wie DNS funktionieren.

Siehe die Abschnitte zu Zuverlässigkeit und Vertrauen.

Zusammenfassend ist das aktuelle System also nicht völlig kaputt, ineffizient oder nicht skalierbar, und Vorschläge, "einfach DNS zu verwenden", sind nicht gut durchdacht.

## Alternativen

Der I2P-Quellcode enthält mehrere erweiterbare Namenssysteme und unterstützt Konfigurationsoptionen, um Experimente mit Namenssystemen zu ermöglichen.

- **Meta** - ruft zwei oder mehr andere Benennungssysteme in einer bestimmten Reihenfolge auf. Standardmäßig werden PetName und dann HostsTxt aufgerufen.
- **PetName** - Sucht in einer petnames.txt-Datei. Das Format für diese Datei ist NICHT dasselbe wie bei hosts.txt.
- **HostsTxt** - Sucht in den folgenden Dateien, in dieser Reihenfolge:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Jeder Host ist in einer separaten Datei in einem addressDb/-Verzeichnis aufgelistet.
- **Eepget** - führt eine HTTP-Suchanfrage an einen externen Server durch - muss nach der HostsTxt-Suche mit Meta gestapelt werden. Dies könnte das Jump-System ergänzen oder ersetzen. Beinhaltet In-Memory-Caching.
- **Exec** - ruft ein externes Programm für die Suche auf, ermöglicht zusätzliche Experimente mit Suchschemata, unabhängig von Java. Kann nach HostsTxt oder als einziges Benennungssystem verwendet werden. Beinhaltet In-Memory-Caching.
- **Dummy** - wird als Fallback für Base64-Namen verwendet, schlägt andernfalls fehl.

Das aktuelle Benennungssystem kann mit der erweiterten Konfigurationsoption `i2p.naming.impl` geändert werden (Neustart erforderlich). Siehe `core/java/src/net/i2p/client/naming` für Details.

Jedes neue System sollte mit HostsTxt gestapelt werden oder lokale Speicherung und/oder die Adressbuch-Abonnement-Funktionen implementieren, da das Adressbuch nur die hosts.txt-Dateien und deren Format kennt.

## Zertifikate

I2P-Ziele enthalten ein Zertifikat, jedoch ist dieses Zertifikat derzeit immer null. Bei einem null-Zertifikat sind base64-Ziele immer 516 Bytes lang und enden mit "AAAA", was im Adressbuch-Zusammenführungsmechanismus und möglicherweise an anderen Stellen überprüft wird. Außerdem gibt es keine verfügbare Methode, um ein Zertifikat zu generieren oder es zu einem Ziel hinzuzufügen. Diese müssen daher aktualisiert werden, um Zertifikate zu implementieren.

Eine mögliche Verwendung von Zertifikaten ist für [Arbeitsnachweis](/get-involved/todo#hashcash).

Eine andere Möglichkeit ist, dass "Subdomains" (in Anführungszeichen, weil es so etwas eigentlich nicht gibt, I2P verwendet ein flaches Benennungssystem) von den Schlüsseln der Domain zweiter Ebene signiert werden.

Mit jeder Zertifikatsimplementierung muss die Methode zur Überprüfung der Zertifikate einhergehen. Vermutlich würde dies im Adressbuch-Merge-Code geschehen. Gibt es eine Methode für mehrere Arten von Zertifikaten oder mehrere Zertifikate?

Das Hinzufügen eines Zertifikats, das die Antworten als von einer zentralisierten Zertifizierungsstelle signiert authentifiziert, würde viele der Probleme mit feindlichen Nameservern lösen, aber Replay-Angriffe sowie Angriffe durch feindliche Zertifizierungsstellen weiterhin offen lassen.
