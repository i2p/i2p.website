---
title: "I2P-MIME-Typen"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Offen"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Überblick

Definieren Sie MIME-Typen für gängige I2P-Dateiformate.
Schließen Sie die Definitionen in Debian-Pakete ein.
Stellen Sie einen Handler für den .su3-Typ und möglicherweise andere bereit.


## Motivation

Um das Nachladen und die Plugin-Installation beim Herunterladen mit einem Browser zu erleichtern,
benötigen wir einen MIME-Typ und einen Handler für .su3-Dateien.

Während wir dabei sind, nachdem wir gelernt haben, wie man die MIME-Definitionsdatei schreibt,
nach dem freedesktop.org-Standard, können wir Definitionen für andere gängige I2P-Dateitypen hinzufügen.
Auch wenn sie für Dateien, die nicht gewöhnlich heruntergeladen werden, wie z.B. die Adressbuch-Blockdatei-Datenbank (hostsdb.blockfile), weniger nützlich sind,
ermöglichen diese Definitionen eine bessere Identifikation und Ikonifizierung von Dateien bei der Verwendung eines grafischen Verzeichnisbetrachters wie "nautilus" auf Ubuntu.

Durch die Standardisierung der MIME-Typen kann jede Router-Implementierung entsprechende Handler schreiben und die MIME-Definitionsdatei kann von allen Implementierungen geteilt werden.


## Design

Schreiben Sie eine XML-Quelldatei nach dem freedesktop.org-Standard und fügen Sie sie in Debian-Pakete ein. Die Datei heißt "debian/(package).sharedmimeinfo".

Alle I2P-MIME-Typen beginnen mit "application/x-i2p-", außer bei jrobin rrd.

Handler für diese MIME-Typen sind anwendungsspezifisch und werden hier nicht
spezifiziert.

Wir werden auch die Definitionen mit Jetty einschließen und sie mit
der Reload-Software oder -Anweisungen beifügen.


## Spezifikation

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Anmerkungen

Nicht alle oben aufgeführten Dateiformate werden von Nicht-Java-Router-Implementierungen verwendet;
einige sind möglicherweise nicht einmal gut spezifiziert. Die Dokumentation hier
könnte jedoch in Zukunft eine konzistente Umsetzung über verschiedene Implementierungen hinweg ermöglichen.

Einige Dateisuffixe wie ".config", ".dat" und ".info" könnten mit anderen
MIME-Typen überlappen. Diese können durch zusätzliche Daten wie
vollen Dateinamen, ein Dateinamensmuster oder Magic Numbers spezifiziert werden.
Siehe das in der zzz.i2p-Themenreihe 'draft i2p.sharedmimeinfo' für Beispiele.

Die wichtigen sind die .su3-Typen, und diese Typen haben sowohl
ein einzigartiges Suffix als auch robuste Magic-Number-Definitionen.


## Migration

Nicht anwendbar.

