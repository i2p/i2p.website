---
title: "Die Entstehung von Privacy Solutions"
date: 2014-08-15
author: "Meeh"
description: "Gründung der Organisation"
categories: ["press"]
---

Hallo zusammen!

Heute kündigen wir das Projekt Privacy Solutions an, eine neue Organisation, die I2P-Software entwickelt und wartet. Privacy Solutions umfasst mehrere neue Entwicklungsinitiativen, die darauf ausgelegt sind, die Privatsphäre, Sicherheit und Anonymität der Nutzer zu verbessern, basierend auf I2P-Protokollen und -Technologie.

Diese Maßnahmen umfassen:

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

Die Anfangsfinanzierung von Privacy Solutions wurde von den Unterstützern der Anoncoin- und Monero-Projekte bereitgestellt. Privacy Solutions ist eine in Norwegen ansässige gemeinnützige Organisation, die in den norwegischen staatlichen Registern eingetragen ist. (Vergleichbar mit US 501(c)3.)

Privacy Solutions plant, Fördermittel von der norwegischen Regierung für Netzwerkforschung zu beantragen, wegen BigBrother (darauf, was das ist, kommen wir später zurück) und der Coins, die planen, Niedriglatenz‑Netzwerke als primäre Transportschicht zu nutzen. Unsere Forschung wird Fortschritte in der Softwaretechnologie für Anonymität, Sicherheit und Privatsphäre unterstützen.

Zunächst ein wenig über das Abscond Browser Bundle. Das war zuerst ein Ein-Mann-Projekt von Meeh, aber später begannen Freunde, Patches zu schicken; das Projekt versucht nun, denselben einfachen Zugang zu I2P zu schaffen, den Tor mit seinem Browser-Bundle bietet. Unsere erste Version ist nicht mehr weit entfernt; es sind nur noch einige Gitian-Skriptaufgaben übrig, einschließlich der Einrichtung der Apple-Toolchain. Außerdem werden wir Monitoring mit PROCESS_INFORMATION (eine C-Struct, die wichtige Prozessinformationen über einen Prozess enthält) aus der Java-Instanz hinzufügen, um I2P zu überprüfen, bevor wir es als stabil einstufen. Sobald i2pd bereit ist, werden wir von der Java-Version darauf umstellen, und es ergibt keinen Sinn mehr, eine JRE im Bundle mitzuliefern. Weitere Informationen über das Abscond Browser Bundle finden Sie unter https://hideme.today/dev

Wir möchten außerdem über den aktuellen Stand von i2pd informieren. I2pd unterstützt jetzt bidirektionales Streaming, wodurch sich nicht nur HTTP, sondern auch dauerhafte Kommunikationskanäle nutzen lassen. Es wurde IRC-Unterstützung hinzugefügt. I2pd-Anwender können es auf dieselbe Weise wie Java I2P nutzen, um auf das I2P-IRC-Netzwerk zuzugreifen. I2PTunnel ist eine der Schlüsselfunktionen des I2P-Netzwerks und ermöglicht es Nicht-I2P-Anwendungen, transparent zu kommunizieren. Daher ist es eine essenzielle Funktion für i2pd und einer der wichtigsten Meilensteine.

Zu guter Letzt, wenn Sie mit I2P vertraut sind, kennen Sie wahrscheinlich Bigbrother.i2p, ein Metriksystem, das Meeh vor über einem Jahr entwickelt hat. Kürzlich haben wir festgestellt, dass Meeh tatsächlich 100Gb nicht duplizierter Daten von Knoten hat, die seit dem ersten Start berichten. Dies wird ebenfalls zu Privacy Solutions migriert und mit einem NSPOF backend (ohne Single Point of Failure) neu implementiert. Damit werden wir auch Graphite (http://graphite.wikidot.com/screen-shots) einsetzen. Das verschafft uns einen hervorragenden Überblick über das Netzwerk, ohne Datenschutzprobleme für unsere Endnutzer. Die Clients filtern alle Daten außer Land, router hash und Erfolgsrate beim tunnel-Aufbau. Der Name dieses Dienstes ist wie immer ein kleiner Witz von Meeh.

Wir haben die Neuigkeiten hier etwas gekürzt; wenn Sie an weiteren Informationen interessiert sind, besuchen Sie bitte https://blog.privacysolutions.no/ Wir befinden uns noch im Aufbau, und weitere Inhalte werden folgen!

Für weitere Informationen wenden Sie sich an: press@privacysolutions.no

Mit freundlichen Grüßen,

Mikal "Meeh" Villa
