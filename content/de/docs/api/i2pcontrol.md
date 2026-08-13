---
title: "I2PControl JSON-RPC"
description: "Remote Router-Verwaltungs-API über die I2PControl-Webapp"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# I2PControl API Dokumentation

-------------check add stuff--------------

I2PControl ist eine **JSON-RPC 2.0** API, die mit dem I2P router (seit Version 0.9.39) mitgeliefert wird. Sie ermöglicht die authentifizierte Überwachung und Steuerung des routers über strukturierte JSON-Anfragen.

> **Standardpasswort:** `itoopie` — dies ist die Werkseinstellung und **sollte sofort geändert werden** aus Sicherheitsgründen.

## 1. Übersicht & Zugriff

| Implementation             | Default Endpoint                 | Protocol | Enabled by Default                             | Notes                  |
|----------------------------|----------------------------------|----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP     | ❌ Muss über WebApps (Router Console) aktiviert werden | Gebündelte Webanwendung |
| i2pd (C++ implementation)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ Standardmäßig aktiviert                       | Verhalten des Legacy-Plugins |
---

Im Fall von Java I2P müssen Sie zu **Router Console → WebApps → I2PControl** gehen und es aktivieren (auf automatischen Start setzen). Sobald es aktiv ist, erfordern alle Methoden, dass Sie sich zuerst authentifizieren und ein Sitzungstoken erhalten.

## 2. JSON-RPC Format

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Alle Anfragen folgen der JSON-RPC 2.0 Struktur:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Eine erfolgreiche Antwort enthält ein `result`-Feld; bei einem Fehler wird ein `error`-Objekt zurückgegeben:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
oder

## 3. Authentifizierungsablauf

### Anfrage (Authentifizieren)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Erfolgreiche Antwort

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Feld       | Richtung  | Typ    | Beschreibung                                              |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | Anfrage   | long   | Von der Client angeforderte I2PControl-API-Version. Verwenden Sie `1`. |
| `Password` | Anfrage   | String | Passwort zur Authentifizierung gegenüber I2PControl.     |
| `API`      | Antwort   | long   | Primäre API-Version, die vom Server implementiert wird.  |
| `Token`    | Antwort   | String | Authentifizierungstoken für nachfolgende Anfragen.       |
---

Sie müssen diesen `Token` in allen nachfolgenden Anfragen in den `params` einschließen.

## 4. Methoden & Endpunkte

### 4.1 RouterInfo

---

Ruft wichtige Telemetriedaten über den router ab.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Anfrage-Beispiel**

#### Status Code Enum (`i2p.router.net.status`)

| Schlüssel                                    | Typ    | Beschreibung                                                             |
|---------------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                         | String | Freiformat, übersetzter Router-Status, zur Anzeige vorgesehen.           |
| `i2p.router.uptime`                         | long   | Betriebszeit des Routers in Millisekunden. Ältere i2pd-Versionen geben möglicherweise einen String zurück. |
| `i2p.router.version`                        | String | Vollständige Router-Version.                                            |
| `i2p.router.net.status`                     | long   | Netzwerkstatuscode; siehe Tabelle unten.                                |
| `i2p.router.net.bw.inbound.1s`              | double | Aktuelle eingehende Bandbreite in Bytes pro Sekunde.                    |
| `i2p.router.net.bw.inbound.15s`             | double | 15-Sekunden-Durchschnitt der eingehenden Bandbreite in Bytes pro Sekunde. |
| `i2p.router.net.bw.outbound.1s`             | double | Aktuelle ausgehende Bandbreite in Bytes pro Sekunde.                    |
| `i2p.router.net.bw.outbound.15s`            | double | 15-Sekunden-Durchschnitt der ausgehenden Bandbreite in Bytes pro Sekunde. |
| `i2p.router.net.tunnels.participating`      | long   | Anzahl der Tunnel, an denen dieser Router beteiligt ist.                 |
#### Statuscode-Enumeration (`i2p.router.net.status`)

| Code | Bedeutung                                             |
|------|-------------------------------------------------------|
| 0    | OK                                                    |
| 1    | TESTEN                                                |
| 2    | HINTER FIREWALL                                       |
| 3    | VERSTECKT                                             |
| 4    | WARNUNG: HINTER FIREWALL UND SCHNELL                 |
| 5    | WARNUNG: HINTER FIREWALL UND FLOODFILL               |
| 6    | WARNUNG: HINTER FIREWALL MIT EINGEHENDER TCP-VERBINDUNG |
| 7    | WARNUNG: HINTER FIREWALL, UDP DEAKTIVIERT             |
| 8    | FEHLER: I2CP                                          |
| 9    | FEHLER: UHRZEITABWEICHUNG                             |
| 10   | FEHLER: PRIVATE TCP-ADRESSE                           |
| 11   | FEHLER: SYMMETRISCHES NAT                             |
| 12   | FEHLER: UDP-PORT WIRD BEREITS VERWENDET               |
| 13   | FEHLER: KEINE AKTIVEN PEERS – ÜBERPRÜFEN SIE VERBINDUNG UND FIREWALL |
| 14   | FEHLER: UDP DEAKTIVIERT UND TCP NICHT GESCHALTEN      |
#### NetDB und Peer-Felder

| Schlüssel                                  | Typ     | Beschreibung                                        |
|-------------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`              | long    | Anzahl bekannter Peers, exklusive des lokalen Routers. |
| `i2p.router.netdb.activepeers`             | long    | Anzahl aktiver Peers.                            |
| `i2p.router.netdb.fastpeers`               | long    | Anzahl als schnell klassifizierter Peers.         |
| `i2p.router.netdb.highcapacitypeers`       | long    | Anzahl als hochkapazitiv klassifizierter Peers.   |
| `i2p.router.netdb.isreseeding`            | boolean | Gibt an, ob ein Re-Seed-Vorgang läuft.           |
**Antwortfelder (result)**   Laut der offiziellen Dokumentation (GetI2P):   - `i2p.router.status` (String) — ein für Menschen lesbarer Status   - `i2p.router.uptime` (long) — Millisekunden (oder String für ältere i2pd-Versionen) :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — Versionszeichenkette :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — eingehende Bandbreite in B/s :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — ausgehende Bandbreite in B/s :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — numerischer Statuscode (siehe Enum unten) :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — Anzahl der teilnehmenden tunnel :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — netDB Peer-Statistiken :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — ob Reseed aktiv ist :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — insgesamt bekannte Peers :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Parameter | Typ    | Beschreibung                  |
|-----------|--------|-------------------------------|
| `Stat`    | String | Name des Router-RateStat.     |
| `Period`  | long   | Rate-Periode in Millisekunden. |
Wird verwendet, um Ratenmetriken (z.B. Bandbreite, tunnel-Erfolg) über ein bestimmtes Zeitfenster abzurufen.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Anfrage-Beispiel**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Beispielantwort**

### 4.3 RouterManager

---

| Parameter          | Ergebnis            | Beschreibung                                                           |
|--------------------|-------------------|-----------------------------------------------------------------------|
| `Restart`          | null              | Startet einen sofortigen Neustart des Routers.                                |
| `RestartGraceful`  | null              | Startet neu, nachdem die genutzten Tunnel abgelaufen sind.                          |
| `Shutdown`         | null              | Startet eine sofortige Herunterfahrt des Routers.                               |
| `ShutdownGraceful` | null              | Fährt herunter, nachdem die genutzten Tunnel abgelaufen sind.                        |
| `Reseed`           | null              | Startet ein erneutes Reseeding des Routers.                                               |
| `FindUpdates`      | boolean oder String | Blockierend. Sucht nach einem signierten Router-Update.                        |
| `Update`           | String            | Blockierend. Startet ein signiertes Router-Update und gibt dessen Endstatus zurück. |
Administrative Aktionen durchführen.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Erlaubte Parameter / Methoden**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Anfrage-Beispiel**

### 4.4 NetworkSetting

**Erfolgreiche Antwort**

---

| Schlüssel                            | Akzeptierter Wert                                   | Beschreibung                                                  |
|--------------------------------------|-----------------------------------------------------|---------------------------------------------------------------|
| `i2p.router.net.ntcp.port`           | Zeichenkette, 1–65535                               | NTCP-Port; eine Änderung erfordert einen Neustart.           |
| `i2p.router.net.ntcp.hostname`       | Zeichenkette                                        | NTCP-Hostname; eine Änderung erfordert einen Neustart.       |
| `i2p.router.net.ntcp.autoip`         | `always`, `true` oder `false`                       | Automatische NTCP-Adressauswahl.                              |
| `i2p.router.net.ssu.port`            | Zeichenkette, 1–65535                               | SSU-Port; eine Änderung erfordert einen Neustart.            |
| `i2p.router.net.ssu.hostname`        | Zeichenkette                                        | Externer SSU-Hostname; eine Änderung erfordert einen Neustart.|
| `i2p.router.net.ssu.autoip`          | `ssu`, `local,ssu`, `upnp,ssu` oder `local,upnp,ssu`| Quellen für SSU-Adressermittlung.                             |
| `i2p.router.net.ssu.detectedip`      | null                                                | Schreibgeschützte ermittelte SSU-Adresse.                     |
| `i2p.router.net.upnp`                | Zeichenkette                                        | UPnP-Einstellung.                                             |
| `i2p.router.net.bw.share`            | Zeichenkette, 0–100                                 | Prozentsatz der Bandbreite für Teilnahmetunnel.               |
| `i2p.router.net.bw.in`               | Nichtnegative ganze Zahl als Zeichenkette           | Eingehende Bandbreitenbegrenzung in KiB/s.                    |
| `i2p.router.net.bw.out`              | Nichtnegative ganze Zahl als Zeichenkette           | Ausgehende Bandbreitenbegrenzung in KiB/s.                    |
| `i2p.router.net.laptopmode`          | Zeichenkette                                        | Einstellung für Laptop-Modus.                                 |
Netzwerkkonfigurationsparameter abrufen oder festlegen (Ports, UPnP, Bandbreitenanteil, etc.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Anfrage-Beispiel (aktuelle Werte abrufen)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Beispielantwort**

> Hinweis: i2pd-Versionen vor 2.41 können numerische Typen anstelle von Strings zurückgeben — Clients sollten beide verarbeiten können. :contentReference[oaicite:11]{index=11}

### 4.5 Erweiterte Einstellungen

---

| Parameter | Typ                 | Beschreibung                                                           |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | String              | Gibt eine Einstellung innerhalb eines `get`-Ergebnisobjekts zurück.                     |
| `getAll`  | n/a                 | Gibt die vollständige Konfigurationskarte innerhalb von `getAll` zurück.               |
| `set`     | Map<String, String> | Aktualisiert die angegebenen Einstellungen, ohne andere Schlüssel zu entfernen.            |
| `setAll`  | Map<String, String> | **Destructive:** ersetzt alle Einstellungen und entfernt nicht angegebene Schlüssel. |
Ermöglicht die Manipulation interner router-Parameter.

**Anfrage-Beispiel**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Antwort-Beispiel**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Standard JSON-RPC2 Fehlercodes

---

| Parameter | Typ | Beschreibung |
|-----------|--------|-----------------------------|
| `Echo`    | String | Wert, der als `Result` zurückgegeben wird. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### I2PControl spezifische Fehlercodes

Verwaltet I2PControl selbst. Der aktuelle Java-Handler unterstützt Passwortänderungen.

| Parameter             | Typ    | Beschreibung                                                                |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | String | Legt ein neues I2PControl-Kennwort fest und widerruft vorhandene Authentifizierungstoken. |
Das Ergebnis enthält `SettingsSaved`. Falls das Passwort geändert wurde, enthält das Ergebnis außerdem `"i2pcontrol.password": null`. Die Einstellungen für Listen-Adresse und Listen-Port aus dem alten eigenständigen Plugin sind im aktuellen Java-Handler nicht aktiv.

> **Standardpasswort:** `itoopie` — dies ist die Werkseinstellung und **sollte sofort geändert werden** aus Sicherheitsgründen.

## 5. Fehlercodes

### Standard-JSON-RPC2-Fehlercodes

| Code   | Bedeutung            |
|--------|----------------------|
| -32700 | JSON-Analysefehler   |
| -32600 | Ungültige Anfrage    |
| -32601 | Methode nicht gefunden |
| -32602 | Ungültige Parameter  |
| -32603 | Interner Fehler      |
### I2PControl-spezifische Fehlercodes

| Code   | Bedeutung                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | Ungültiges Passwort angegeben                                                                |
| -32002 | Kein Authentifizierungstoken übermittelt                                                        |
| -32003 | Authentifizierungstoken existiert nicht                                                       |
| -32004 | Das angegebene Authentifizierungstoken ist abgelaufen und wird entfernt                        |
| -32005 | Die verwendete Version der I2PControl-API wurde nicht angegeben, ist jedoch erforderlich         |
| -32006 | Die angegebene Version der I2PControl-API wird von I2PControl nicht unterstützt               |
> **Standardpasswort:** `itoopie` — dies ist die Werkseinstellung und **sollte sofort geändert werden** aus Sicherheitsgründen.

## 6. Verwendung und bewährte Praktiken

- Fügen Sie immer den `Token`-Parameter hinzu (außer bei der Authentifizierung).
- Ändern Sie das Standardpasswort (`itoopie`) bei der ersten Verwendung.
- Stellen Sie bei Java I2P sicher, dass die I2PControl-Webapp über WebApps aktiviert ist.
- Seien Sie auf geringfügige Abweichungen vorbereitet: einige Felder können je nach I2P-Version Zahlen oder Strings sein.
- Umbrechen Sie lange Status-Strings für eine anzeigefreundliche Ausgabe.

> **Standardpasswort:** `itoopie` — dies ist die Werkseinstellung und **sollte sofort geändert werden** aus Sicherheitsgründen.
