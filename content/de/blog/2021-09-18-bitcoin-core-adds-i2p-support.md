---
title: "Bitcoin Core unterstützt jetzt I2P!"
date: 2021-09-18
author: "idk"
description: "Ein neuer Anwendungsfall und ein Signal für wachsende Akzeptanz"
categories: ["general"]
API_Translate: wahr
---

Ein seit Monaten vorbereitetes Ereignis: Bitcoin Core hat offizielle Unterstützung für I2P hinzugefügt! Bitcoin-over-I2P-Knoten können vollständig mit den übrigen Bitcoin-Knoten interagieren, wobei sie von Knoten unterstützt werden, die sowohl in I2P als auch im Clearnet aktiv sind, und sind damit vollwertige Teilnehmer im Bitcoin-Netzwerk. Es ist spannend zu sehen, dass große Communities wie Bitcoin die Vorteile erkennen, die I2P ihnen bringen kann, indem es Menschen auf der ganzen Welt Privatsphäre und Erreichbarkeit bietet.

## Funktionsweise

Die I2P-Unterstützung ist automatisch und erfolgt über die SAM API. Das ist außerdem eine spannende Nachricht, weil es einige der Dinge hervorhebt, in denen I2P besonders gut ist, etwa Anwendungsentwickler zu befähigen, I2P-Verbindungen programmatisch und bequem aufzubauen. Bitcoin-über-I2P-Nutzer können I2P ohne manuelle Konfiguration verwenden, indem sie die SAM API aktivieren und Bitcoin mit aktiviertem I2P ausführen.

## Ihren I2P Router konfigurieren

Um einen I2P Router so einzurichten, dass er anonyme Konnektivität für Bitcoin bereitstellt, muss die SAM API aktiviert werden. In Java I2P sollten Sie zu http://127.0.0.1:7657/configclients gehen und die SAM Application Bridge mit der Schaltfläche "Start" starten. Sie können die SAM Application Bridge außerdem standardmäßig aktivieren, indem Sie das Kontrollkästchen "Run at Startup" markieren und auf "Save Client Configuration" klicken.

Bei i2pd ist die SAM API normalerweise standardmäßig aktiviert, aber falls nicht, sollten Sie Folgendes einstellen:

```
sam.enabled=true
```
in Ihrer Datei i2pd.conf.

## Konfigurieren Ihres Bitcoin-Knotens für Anonymität und Konnektivität

Um Bitcoin selbst im anonymen Modus zu starten, ist weiterhin das Bearbeiten einiger Konfigurationsdateien im Bitcoin-Datenverzeichnis erforderlich, das unter Windows %APPDATA%\Bitcoin, unter Linux ~/.bitcoin und unter Mac OSX ~/Library/Application Support/Bitcoin/ zu finden ist. Außerdem ist mindestens Version 22.0.0 erforderlich, damit die I2P-Unterstützung vorhanden ist.

Nachdem Sie diese Anweisungen befolgt haben, sollten Sie einen privaten Bitcoin-Knoten haben, der I2P für I2P-Verbindungen und Tor für .onion- und Clearnet-Verbindungen verwendet, sodass alle Ihre Verbindungen anonym sind. Der Einfachheit halber sollten Windows-Benutzer ihr Bitcoin-Datenverzeichnis öffnen, indem sie das Startmenü öffnen und nach "Ausführen" suchen. Im Ausführen-Dialog geben Sie "%APPDATA%\Bitcoin" ein und drücken die Eingabetaste.

Erstellen Sie in diesem Verzeichnis eine Datei namens "i2p.conf." Unter Windows sollten Sie darauf achten, beim Speichern Anführungszeichen um den Dateinamen zu setzen, um zu verhindern, dass Windows der Datei eine Standard-Dateiendung hinzufügt. Die Datei sollte die folgenden I2P-bezogenen Bitcoin-Konfigurationsoptionen enthalten:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Als Nächstes sollten Sie eine weitere Datei namens "tor.conf." erstellen. Die Datei sollte die folgenden Tor-bezogenen Konfigurationsoptionen enthalten:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Schließlich müssen Sie diese Konfigurationsoptionen in Ihre Bitcoin-Konfigurationsdatei "einbinden", die im Datenverzeichnis den Namen "bitcoin.conf" trägt. Fügen Sie diese zwei Zeilen Ihrer Datei bitcoin.conf hinzu:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Jetzt ist Ihr Bitcoin-Knoten so konfiguriert, dass er nur anonyme Verbindungen verwendet. Um direkte Verbindungen zu entfernten Knoten zu ermöglichen, entfernen Sie die mit Folgendem beginnenden Zeilen:

```
onlynet=
```
Sie können dies tun, wenn Ihr Bitcoin-Knoten nicht anonym sein muss, und es hilft anonymen Nutzern, sich mit dem Rest des Bitcoin-Netzwerks zu verbinden.
