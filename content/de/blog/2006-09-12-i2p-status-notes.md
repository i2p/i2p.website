---
title: "I2P-Statusnotizen für 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Release 0.6.1.25 mit Verbesserungen der Netzwerkstabilität, I2PSnark-Optimierungen und einer umfassenden Neugestaltung von Syndie mit verteilten Offline-Foren"
categories: ["status"]
---

Hallo zusammen, hier sind unsere *hust* wöchentlichen Statusnotizen

* Index:

1) 0.6.1.25 und Netzstatus 2) I2PSnark 3) Syndie (was/warum/wann) 4) Syndie Krypto-Fragen 5) ???

* 1) 0.6.1.25 and net status

Neulich haben wir die Version 0.6.1.25 veröffentlicht, einschließlich der im letzten Monat angesammelten Vielzahl von Bugfixes, sowie die Arbeiten von zzz an I2PSnark und die Bemühungen von Complication, unseren Zeitsynchronisationscode etwas robuster zu machen. Im Moment scheint das Netzwerk ziemlich stabil zu sein, auch wenn IRC in den letzten Tagen etwas holprig war (aus Gründen, die nicht mit I2P zusammenhängen). Da vielleicht die Hälfte des Netzwerks bereits auf die neueste Version aktualisiert wurde, haben sich die Erfolgsraten beim tunnel-Aufbau nicht wesentlich verändert, wobei der Gesamtdurchsatz gestiegen zu sein scheint (wahrscheinlich aufgrund einer größeren Zahl von Leuten, die I2PSnark verwenden).

* 2) I2PSnark

Die von zzz vorgenommenen Aktualisierungen an I2PSnark umfassten Protokolloptimierungen sowie Änderungen an den Weboberflächen, wie im Verlaufsprotokoll [1] beschrieben. Seit der Veröffentlichung 0.6.1.25 gab es ebenfalls einige kleine Updates für I2PSnark, und vielleicht kann zzz uns während des Treffens heute Abend einen Überblick über den aktuellen Stand geben.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Wie ihr alle wisst, habe ich mich darauf konzentriert, Syndie zu überarbeiten, auch wenn "revamp" vielleicht nicht das richtige Wort ist. Vielleicht kann man das, was derzeit bereitgestellt ist, als "Proof of Concept" (Machbarkeitsnachweis) betrachten, da das neue Syndie von Grund auf neu entworfen und neu implementiert wurde, auch wenn viele Konzepte erhalten geblieben sind. Wenn ich im Folgenden auf Syndie verweise, meine ich das neue Syndie.

* 3.1) What is Syndie

Syndie ist auf der grundlegendsten Ebene ein System zum Betrieb verteilter Foren im Offline-Modus. Auch wenn seine Struktur zu einer großen Zahl unterschiedlicher Konfigurationen führt, werden die meisten Anforderungen erfüllt, indem man aus jedem der folgenden drei Kriterien eine Option auswählt:  - Forentypen:    - Einzelautor (typischer Blog)    - Mehrere Autoren (Multi-Author-Blog)**    - Offen (Newsgroups, wobei Einschränkungen möglich sind, sodass nur      autorisierte** Nutzer neue Threads eröffnen können, während jeder      diese neuen Threads kommentieren kann)  - Sichtbarkeit:    - Jeder kann alles lesen    - Nur autorisierte* Personen können Beiträge lesen, aber einige Metadaten sind sichtbar    - Nur autorisierte* Personen können Beiträge lesen oder überhaupt wissen, wer postet    - Nur autorisierte* Personen können Beiträge lesen, und niemand weiß, wer      postet  - Kommentare/Antworten:    - Jeder kann kommentieren oder private Antworten an den Autor/Inhaber      des Forums senden    - Nur autorisierte** Personen können kommentieren, und jeder kann private      Antworten senden    - Niemand kann kommentieren, aber jeder kann private Antworten senden    - Niemand kann kommentieren, und niemand kann private Antworten senden

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** Das Posten, Aktualisieren und/oder Kommentieren wird autorisiert, indem jenen    Nutzern asymmetrische private Schlüssel zur Verfügung gestellt werden, mit denen sie die Beiträge signieren, wobei der    entsprechende öffentliche Schlüssel in den Metadaten des Forums als    berechtigt zum Posten, Verwalten oder Kommentieren im Forum enthalten ist.  Alternativ können die    signierenden öffentlichen Schlüssel einzelner berechtigter Nutzer in    den Metadaten aufgeführt sein.

Einzelne Beiträge können viele verschiedene Elemente enthalten:  - Beliebig viele Seiten, mit out of band data (außerhalb des Hauptkanals übermittelte Daten) für jede Seite, die
    den Content-Typ, die Sprache usw. angeben.  Beliebige Formatierungen können verwendet werden, da es
    der Client-Anwendung obliegt, den Inhalt sicher darzustellen - Nur-Text
    muss unterstützt werden, und Clients, die dazu in der Lage sind, sollten HTML unterstützen.  - Beliebig viele Anhänge (ebenfalls mit out of band data, die den
    Anhang beschreiben)  - Ein kleines Avatarbild für den Beitrag (wenn nicht angegeben, wird das
    Standard-Avatar des Autors verwendet)  - Eine Menge von Verweisen auf andere Beiträge, Foren, Archive, URLs usw. (die
    die zum Veröffentlichen, Verwalten oder Lesen der referenzierten
    Foren erforderlichen Schlüssel enthalten können)

Im Großen und Ganzen arbeitet Syndie auf der *Inhaltsebene* - einzelne Beiträge befinden sich in verschlüsselten ZIP-Dateien, und die Teilnahme am Forum bedeutet schlicht, diese Dateien zu teilen. Es gibt keine Abhängigkeiten davon, wie die Dateien übertragen werden (über I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), aber einfache Werkzeuge zur Aggregation und Verteilung werden mit der Standardveröffentlichung von Syndie gebündelt.

Die Interaktion mit den Syndie-Inhalten erfolgt auf verschiedene Weisen. Erstens gibt es eine skriptfähige, textbasierte Schnittstelle, die grundlegende Vorgänge über die Kommandozeile sowie interaktives Lesen aus, Schreiben in, Verwalten und Synchronisieren der Foren ermöglicht. Zum Beispiel ist das Folgende ein einfaches Skript, um einen neuen „Nachricht des Tages“-Beitrag zu erzeugen -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Leiten Sie das einfach per Pipe durch die ausführbare Datei syndie, und die Sache ist erledigt: cat motd-script | ./syndie > syndie.log

Außerdem wird an einer grafischen Syndie-Benutzeroberfläche gearbeitet, die die sichere Darstellung von Nur-Text und HTML-Seiten umfasst (natürlich mit Unterstützung für die transparente Integration in die Funktionen von Syndie).

Anwendungen, die auf Syndies altem „sucker“-Code basieren, werden das Scraping und das Umschreiben normaler Webseiten und Websites ermöglichen, sodass sie als ein- oder mehrseitige Syndie-Beiträge verwendet werden können, einschließlich Bildern und anderer Ressourcen als Anhänge.

In Zukunft sind Firefox/Mozilla-Plugins geplant, die sowohl Syndie-formatierte Dateien als auch Syndie-Verweise erkennen und importieren sowie die lokale Syndie-GUI darüber benachrichtigen, dass ein bestimmtes Forum, Thema, Schlagwort, Autor oder Suchergebnis in den Fokus gerückt werden soll.

Natürlich werden im Laufe der Zeit wahrscheinlich weitere Anwendungen oder alternative Implementierungen entwickelt, da Syndie im Kern eine Inhaltsschicht mit einem definierten Dateiformat und kryptografischen Algorithmen ist.

* 3.2) Why does Syndie matter?

Ich habe in den letzten Monaten mehrere Leute fragen hören, warum ich an einem Forum-/Blogging-Tool arbeite - was hat das mit der Bereitstellung starker Anonymität zu tun?

Die Antwort: *alles*.

Kurz zusammengefasst:  - Das Design von Syndie als anonymitätssensible Client‑Anwendung sorgfältig
    vermeidet die komplexen Probleme der Datensensitivität, wie sie nahezu jede
    Anwendung, die nicht mit Blick auf Anonymität entwickelt wurde, mit sich bringt.
  - Durch das Arbeiten auf der Inhaltsebene ist Syndie nicht von der
    Leistung oder Zuverlässigkeit verteilter Netzwerke wie I2P, Tor oder
    Freenet abhängig, auch wenn es sie, wo sinnvoll, nutzen kann.
  - Dadurch kann es vollständig mit kleinen Ad‑hoc‑Mechanismen für
    die Verteilung von Inhalten arbeiten - Mechanismen, deren Bekämpfung
    für mächtige Angreifer den Aufwand möglicherweise nicht wert ist (da der 'Nutzen' der Überführung
    nur einiger Dutzend Personen die Kosten für die Durchführung der
    Angriffe wahrscheinlich übersteigen würde)
  - Das impliziert, dass Syndie selbst dann nützlich sein wird, wenn es nicht von ein paar Millionen
    Menschen genutzt wird - kleine, voneinander unabhängige Gruppen sollten ihr eigenes privates
    Syndie‑Verteilungsschema einrichten, ohne dass dafür irgendeine Interaktion mit
    oder auch nur die Kenntnisnahme durch andere Gruppen erforderlich ist.
  - Da Syndie nicht auf Echtzeit‑Interaktion angewiesen ist, kann es sogar
    Anonymitätssysteme und Techniken mit hoher Latenz nutzen, um die
    Angriffe zu vermeiden, denen alle Systeme mit niedriger Latenz ausgesetzt sind (wie etwa
    passive Schnittmengenangriffe, passive und aktive Timing‑Angriffe sowie
    aktive Blending‑Angriffe (Mischangriffe)).

Insgesamt bin ich der Ansicht, dass Syndie für die Kernaufgabe von I2P (starke Anonymität für diejenigen bereitzustellen, die sie benötigen) sogar noch wichtiger ist als der router. Es ist nicht das Maß aller Dinge, aber ein wichtiger Schritt.

* 3.3) When can we use Syndie?

Obwohl bereits viel Arbeit abgeschlossen wurde (einschließlich fast der gesamten Textoberfläche und eines großen Teils der GUI), bleibt noch Arbeit zu tun. Die erste Syndie-Version wird die folgende Basisfunktionalität enthalten:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

Das Kriterium, nach dem ich das veröffentlichen werde, wird "voll funktionsfähig" sein. Otto Normalverbraucher wird sich nicht mit einer textbasierten App abgeben, aber ich hoffe, dass sich ein paar Geeks darauf einlassen.

Künftige Versionen werden Syndies Leistungsumfang in mehreren Dimensionen verbessern:  - Benutzeroberfläche:   - SWT-basierte GUI   - Webbrowser-Plugins   - Web-Scrape-Text-UI (ruft Seiten ab und schreibt sie um)   - IMAP/POP3/NNTP-Leseschnittstelle  - Unterstützung für Inhalte   - Reiner Text   - HTML (sichere Darstellung innerhalb der GUI, nicht im Browser)   - BBCode (?)  - Syndizierung   - Feedspace, Feedtree und andere Synchronisationswerkzeuge mit niedriger Latenz   - Freenet (Speichern von .snd-Dateien unter CHK@s und Archiven, die sich auf
    die .snd-Dateien unter SSK@s und USK@s beziehen)   - E-Mail (Versand über SMTP/mixmaster/mixminion, Lesen über
    procmail/etc)   - Usenet (Versand über NNTP oder Remailer, Lesen über (per Proxy)
    NNTP)  - Volltextsuche mit Lucene-Integration  - Erweiterung von HSQLDB für vollständige Datenbankverschlüsselung  - Zusätzliche Heuristiken zur Archivverwaltung

Was wann herauskommt, hängt davon ab, wann die Dinge erledigt werden.

* 4) Open questions for Syndie

Derzeit ist Syndie mit den standardmäßigen kryptografischen Primitiven von I2P implementiert - SHA256, AES256/CBC, ElGamal2048, DSA. Das letzte davon ist jedoch der Ausreißer, da es 1024-Bit öffentliche Schlüssel verwendet und von (dem rapide schwächer werdenden) SHA1 abhängt. Ein Gerücht aus der Praxis ist die Erweiterung von DSA um SHA256, und obwohl das machbar ist (wenn auch noch nicht standardisiert), bietet es nur 1024-Bit öffentliche Schlüssel.

Da Syndie noch nicht breit ausgerollt wurde und es keine Bedenken hinsichtlich der Abwärtskompatibilität gibt, haben wir den Luxus, die Krypto-Primitiven auszutauschen. Eine Überlegung ist, statt DSA auf ElGamal2048- oder RSA2048-Signaturen zu setzen, während eine andere Überlegung in Richtung ECC geht (mit ECDSA-Signaturen und ECIES asymmetrischer Verschlüsselung), möglicherweise auf den Sicherheitsniveaus 256 Bit oder 521 Bit (entsprechend 128-Bit- bzw. 256-Bit-Schlüsselgrößen bei symmetrischen Verfahren).

Was die patentrechtlichen Fragen in Bezug auf ECC (Elliptische-Kurven-Kryptographie) angeht, scheinen diese nur für bestimmte Optimierungen (Punktkompression) und Algorithmen relevant zu sein, die wir nicht benötigen (EC MQV). Es gibt nicht viel an Java-Unterstützung, obwohl die bouncycastle lib anscheinend etwas Code hat. Allerdings wäre es wahrscheinlich nicht viel Aufwand, kleine Wrapper für libtomcrypt, openssl oder crypto++ hinzuzufügen, so wie wir es für libGMP getan haben (wodurch wir jbigi erhalten haben).

Gibt es dazu Anmerkungen?

* 5) ???

Weiter oben gibt es eine Menge zu verarbeiten, weshalb ich (auf Vorschlag von cervantes) diese Statusnotizen so früh verschicke. Wenn ihr Kommentare, Fragen, Bedenken oder Vorschläge habt, schaut doch heute Abend um 20:00 UTC auf irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p bei #i2p vorbei zu unserem *hust* wöchentlichen Treffen!

=jr
