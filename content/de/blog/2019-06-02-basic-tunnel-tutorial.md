---
title: "Grundlegendes Tutorial zu I2P Tunnels mit Bildern"
date: 2019-06-02
author: "idk"
description: "Grundlegende i2ptunnel-Einrichtung"
categories: ["tutorial"]
---

Obwohl der Java I2P router mit einem statischen Webserver, jetty, vorkonfiguriert ist, um die erste eepSite des Benutzers bereitzustellen, benötigen viele von ihrem Webserver umfangreichere Funktionen und möchten lieber eine eepSite mit einem anderen Server erstellen. Das ist natürlich möglich und tatsächlich ganz einfach, sobald man es einmal gemacht hat.

Auch wenn es leicht umzusetzen ist, sollten Sie vorher ein paar Dinge beachten. Entfernen Sie identifizierende Merkmale von Ihrem Webserver, etwa potenziell identifizierende Header und Standard-Fehlerseiten, die den Server-/Distributionstyp angeben. Weitere Informationen über Gefährdungen der Anonymität durch falsch konfigurierte Anwendungen finden Sie unter: [Riseup hier](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix hier](https://www.whonix.org/wiki/Onion_Services), [dieser Blogartikel zu einigen OpSec-Fehlern (operative Sicherheit)](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [und die I2P-Anwendungsseite hier](https://geti2p.net/docs/applications/supported). Auch wenn viele dieser Informationen sich auf Tor Onion Services beziehen, gelten dieselben Verfahren und Prinzipien für das Hosten von Anwendungen über I2P.

### Schritt Eins: Öffnen Sie den Tunnel-Assistenten

Rufen Sie die I2P-Weboberfläche unter 127.0.0.1:7657 auf und öffnen Sie den [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) (verweist auf localhost). Klicken Sie auf die Schaltfläche "Tunnel Wizard", um zu beginnen.

### Schritt zwei: Wählen Sie einen Server Tunnel

Der Assistent für tunnel ist sehr einfach. Da wir einen http-*Server* einrichten, müssen wir nur einen *Server* tunnel auswählen.

### Schritt Drei: Wählen Sie einen HTTP Tunnel

Ein HTTP tunnel ist der Typ von tunnel, der für die Bereitstellung von HTTP-Diensten optimiert ist. Er verfügt über aktivierte Filter- und Ratenbegrenzungsfunktionen, die speziell auf diesen Zweck zugeschnitten sind. Ein standardmäßiger tunnel kann ebenfalls funktionieren, aber wenn Sie einen standardmäßigen tunnel auswählen, müssen Sie sich um diese Sicherheitsfunktionen selbst kümmern. Eine ausführlichere Betrachtung der HTTP Tunnel-Konfiguration finden Sie im nächsten Tutorial.

### Schritt vier: Geben Sie einen Namen und eine Beschreibung an

Zu Ihrem eigenen Nutzen und damit Sie sich merken und unterscheiden können, wofür Sie den tunnel verwenden, geben Sie ihm einen aussagekräftigen Spitznamen und eine Beschreibung. Wenn Sie später zurückkehren und weitere Verwaltung vornehmen müssen, identifizieren Sie den tunnel auf diese Weise im Manager für versteckte Dienste.

### Schritt fünf: Host und Port konfigurieren

In diesem Schritt geben Sie den TCP-Port an, auf dem Ihr Webserver lauscht. Da die meisten Webserver auf Port 80 oder Port 8080 lauschen, zeigt das Beispiel dies. Wenn Sie alternative Ports oder virtuelle Maschinen oder Container verwenden, um Ihre Webdienste zu isolieren, müssen Sie möglicherweise den Host, den Port oder beides anpassen.

### Schritt Sechs: Entscheiden Sie, ob es automatisch gestartet werden soll

Ich kann mir keine Möglichkeit vorstellen, diesen Schritt näher zu erläutern.

### Schritt sieben: Überprüfen Sie Ihre Einstellungen

Sehen Sie sich abschließend die von Ihnen ausgewählten Einstellungen an. Wenn diese in Ordnung sind, speichern Sie sie. Falls Sie nicht ausgewählt haben, den tunnel automatisch zu starten, gehen Sie zum Manager für versteckte Dienste und starten Sie den tunnel manuell, wenn Sie Ihren Dienst verfügbar machen möchten.

### Anhang: Optionen zur Anpassung des HTTP-Servers

I2P stellt ein detailliertes Panel zur Verfügung, um den HTTP-Server tunnel auf individuelle Weise zu konfigurieren. Ich werde dieses Tutorial abschließen, indem ich sie alle durchgehe. Irgendwann.
