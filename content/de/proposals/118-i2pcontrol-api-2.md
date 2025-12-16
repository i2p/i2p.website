---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Übersicht

Dieser Vorschlag umreißt API2 für I2PControl.

Dieser Vorschlag wurde abgelehnt und wird nicht implementiert, da er die Abwärtskompatibilität bricht.
Siehe den Diskussionsthread-Link für Details.

### Hinweis für Entwickler!

Alle RPC-Parameter werden jetzt in Kleinbuchstaben geschrieben. Dies *wird* die Abwärtskompatibilität mit API1-Implementierungen brechen. Der Grund dafür ist, den Nutzern von >=API2 die einfachstmögliche und kohärenteste API zu bieten.

## API 2 Spezifikation

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Parameter

**`"id"`**

Die ID-Nummer oder die Anfrage. Wird verwendet, um zu identifizieren, welche Antwort auf welche Anfrage hervorgebracht wurde.

**`"method_name"`**

Der Name des aufzurufenden RPC.

**`"auth_token"`**

Das Sitzungs-Authentifizierungstoken. Muss bei jedem RPC mitgeliefert werden, außer beim 'authenticate'-Aufruf.

**`"method_parameter_value"`**

Der Methodenparameter. Wird verwendet, um verschiedene Ausprägungen einer Methode anzubieten, wie 'get', 'set' und ähnliche Variationen.

**`"result_value"`**

Der Wert, den das RPC zurückgibt. Sein Typ und Inhalt hängen von der Methode und der konkreten Methode ab.

### Präfixe

Das RPC-Benennungsschema ähnelt dem, wie es in CSS gemacht wird, mit Anbieterpräfixen für die verschiedenen API-Implementierungen (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

Die Grundidee mit anbieter-spezifischen Präfixen ist es, etwas Spielraum zu bieten und Implementierungen zu erlauben, zu innovieren, ohne darauf warten zu müssen, dass jede andere Implementierung aufholt. Wenn ein RPC von allen Implementierungen implementiert wird, können seine zahlreichen Präfixe entfernt werden, und es kann als Kern-RPC in der nächsten API-Version aufgenommen werden.

### Methodenlese-Anleitung

 * **rpc.method**

   * *parameter* [Typ des Parameters]:  [null], [number], [string], [boolean],
     [array] oder [object]. [object] ist eine {key:value} Karte.

Gibt zurück:
```text
  "return_value" [string] // Dies ist der Wert, der durch den RPC-Aufruf zurückgegeben wird.
```

### Methoden

* **authenticate** - Wenn ein korrektes Passwort angegeben wird, liefert diese Methode Ihnen ein Token für weiteren Zugang und eine Liste unterstützter API-Level.

  * *password* [string]:  Das Passwort für diese i2pcontrol Implementierung

    Gibt zurück:
```text
    [object]
    {
      "token" : [string], // Der Token, der mit allen anderen RPC-Methoden mitgeliefert werden muss
      "api" : [[int],[int], ...]  // Eine Liste unterstützter API-Level.
    }
```

* **control.** - I2P steuern

  * **control.reseed** - Neubesamung starten

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

  * **control.restart** - I2P-Instanz neu starten

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

  * **control.restart.graceful** - I2P-Instanz sanft neu starten

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

  * **control.shutdown** - I2P-Instanz herunterfahren

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

  * **control.shutdown.graceful** - I2P-Instanz sanft herunterfahren

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

  * **control.update.find** - **BLOCKIEREND** Nach signierten Updates suchen

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      true [boolean] // Wahr, falls ein signiertes Update verfügbar ist
```

  * **control.update.start** - Update-Prozess starten

    * [nil]: Kein Parameter nötig

    Gibt zurück:
```text
      [nil]
```

* **i2pcontrol.** - I2PControl konfigurieren

  * **i2pcontrol.address** - Die IP-Adresse abfragen/festlegen, auf der I2PControl seinen Dienst anbietet.

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Dies wird eine IP-Adresse wie "0.0.0.0" oder "192.168.0.1" sein

    Gibt zurück:
```text
      [nil]
```

  * **i2pcontrol.password** - Das I2PControl-Passwort ändern.

    * *set* [string]: Das neue Passwort auf diesen String setzen

    Gibt zurück:
```text
      [nil]
```

  * **i2pcontrol.port** - Den Port abfragen/festlegen, auf dem I2PControl seinen Dienst anbietet.

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      7650 [number]
```

    * *set* [number]: Den Port ändern, auf dem I2PControl seinen Dienst anbietet

    Gibt zurück:
```text
      [nil]
```

* **settings.** - I2P-Instanzeinstellungen abfragen/festlegen

  * **settings.advanced** - Erweiterte Einstellungen

    * *get*  [string]: Den Wert dieser Einstellung abrufen

    Gibt zurück:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    Gibt zurück:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: Den Wert dieser Einstellung setzen
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Gibt zurück:
```text
      [nil]
```

  * **settings.bandwidth.in** - Eingehende Bandbreiteneinstellungen
  * **settings.bandwidth.out** - Ausgehende Bandbreiteneinstellungen

    * *get* [nil]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0 [number]
```

    * *set* [number]: Das Bandbreitenlimit festlegen

    Gibt zurück:
```text
     [nil]
```

  * **settings.ntcp.autoip** - Auto-IP-Erkennungseinstellung für NTCP abrufen

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - NTCP-Hostname abrufen

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Neuen Hostnamen festlegen

    Gibt zurück:
```text
      [nil]
```

  * **settings.ntcp.port** - NTCP-Port

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0 [number]
```

    * *set* [number]: Neuen NTCP-Port festlegen.

    Gibt zurück:
```text
      [nil]
```

    * *set* [boolean]: NTCP IP Auto-Erkennung festlegen

    Gibt zurück:
```text
      [nil]
```

  * **settings.ssu.autoip** - Konfiguriere die IP Auto-Erkennungseinstellung für SSU

    * *get* [nil]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - SSU-Hostname konfigurieren

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Neuen SSU-Hostnamen festlegen

    Gibt zurück:
```text
      [nil]
```

  * **settings.ssu.port** - SSU-Port

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0 [number]
```

    * *set* [number]: Neuen SSU-Port festlegen.

    Gibt zurück:
```text
      [nil]
```

    * *set* [boolean]: SSU IP Auto-Erkennung festlegen

    Gibt zurück:
```text
      [nil]
```

  * **settings.share** - Bandbreitenanteil in Prozent abrufen

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0 [number] // Bandbreitenanteil in Prozent (0-100)
```

    * *set* [number]: Bandbreitenanteil in Prozent festlegen (0-100)

    Gibt zurück:
```text
      [nil]
```

  * **settings.upnp** - UPNP aktivieren oder deaktivieren

    * *get* [nil]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      true [boolean]
```

    * *set* [boolean]: SSU IP Auto-Erkennung festlegen

    Gibt zurück:
```text
      [nil]
```

* **stats.** - Statistiken von der I2P-Instanz abrufen

  * **stats.advanced** - Diese Methode bietet Zugriff auf alle in der Instanz gespeicherten Statistiken.

    * *get* [string]:  Name der bereitzustellenden erweiterten Statistik
    * *Optional:* *period* [number]:  Der Zeitraum für die angeforderte Statistik

  * **stats.knownpeers** - Gibt die Anzahl der bekannten Peers zurück
  * **stats.uptime** - Gibt die Zeit in ms seit dem Start des Routers zurück
  * **stats.bandwidth.in** - Gibt die eingehende Bandbreite zurück (idealerweise für die letzte Sekunde)
  * **stats.bandwidth.in.total** - Gibt die Anzahl der empfangenen Bytes seit dem letzten Neustart zurück
  * **stats.bandwidth.out** - Gibt die ausgehende Bandbreite zurück (idealerweise für die letzte Sekunde)
  * **stats.bandwidth.out.total** - Gibt die Anzahl der gesendeten Bytes seit dem letzten Neustart zurück
  * **stats.tunnels.participating** - Gibt die Anzahl der derzeit beteiligten Tunnel zurück
  * **stats.netdb.peers.active** - Gibt die Anzahl der Peers zurück, mit denen wir kürzlich kommuniziert haben
  * **stats.netdb.peers.fast** - Gibt die Anzahl der 'schnellen' Peers zurück
  * **stats.netdb.peers.highcapacity** - Gibt die Anzahl der 'hohen Kapazität' Peers zurück
  * **stats.netdb.peers.known** - Gibt die Anzahl der bekannten Peers zurück

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0.0 [number]
```

* **status.** - I2P-Instanz-Status abrufen

  * **status.router** - Router-Status abrufen

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      "status" [string]
```

  * **status.net** - Router-Netzwerkstatus abrufen

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - Ist die I2P-Instanz derzeit ein Floodfill

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      true [boolean]
```

  * **status.isreseeding** - Ist die I2P-Instanz derzeit in der Neubesamung

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      true [boolean]
```

  * **status.ip** - Öffentliche IP-Adresse der I2P-Instanz ermittelt

    * *get* [null]: Dieser Parameter muss nicht gesetzt werden.

    Gibt zurück:
```text
      "0.0.0.0" [string]
```
