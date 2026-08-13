---
title: "I2PControl JSON-RPC"
description: "API pro vzdálenou správu routeru přes webovou aplikaci I2PControl"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# Dokumentace I2PControl API

-------------zkontrolovat přidání věcí--------------

I2PControl je **JSON-RPC 2.0** API dodávané s I2P routerem (od verze 0.9.39). Umožňuje autentifikované monitorování a ovládání routeru prostřednictvím strukturovaných JSON požadavků.

> **Výchozí heslo:** `itoopie` — toto je tovární výchozí nastavení a **mělo by být okamžitě změněno** z bezpečnostních důvodů.

## 1. Přehled a přístup

| Implementace               | Výchozí koncový bod                     | Protokol | Povoleno ve výchozím nastavení                 | Poznámky               |
|----------------------------|----------------------------------------|----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/`       | HTTP     | ❌ Musí být povoleno přes webové aplikace (konzole směrovače) | Dodávaná webová aplikace |
| i2pd (C++ implementace)    | `https://127.0.0.1:7650/`              | HTTPS    | ✅ Povoleno ve výchozím nastavení               | Chování staršího pluginu |
---

V případě Java I2P musíte jít do **Router Console → WebApps → I2PControl** a povolit ho (nastavit na automatické spuštění). Jakmile je aktivní, všechny metody vyžadují, abyste se nejprve autentifikovali a obdrželi token relace.

## 2. Formát JSON-RPC

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
Všechny požadavky dodržují strukturu JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Úspěšná odpověď obsahuje pole `result`; při selhání je vrácen objekt `error`:

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
nebo

## 3. Tok autentizace

### Požadavek (Autentifikace)

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
### Úspěšná odpověď

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
| Pole       | Směr      | Typ    | Popis                                                    |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | Požadavek | long   | Verze I2PControl API požadovaná klientem. Použijte `1`.  |
| `Password` | Požadavek | String | Heslo použité k ověření u I2PControl.                    |
| `API`      | Odpověď   | long   | Primární verze API implementovaná serverem.              |
| `Token`    | Odpověď   | String | Ověřovací token použitý pro následné požadavky.         |
---

Tento `Token` musíte zahrnout do všech následujících požadavků v `params`.

## 4. Metody a koncové body

### 4.1 RouterInfo

---

Získává klíčovou telemetrii o routeru.

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
**Příklad požadavku**

#### Status Code Enum (`i2p.router.net.status`)

| Klíč                                   | Typ    | Popis                                                                  |
|----------------------------------------|--------|------------------------------------------------------------------------|
| `i2p.router.status`                    | Řetězec| Volný formát, přeložený stav směrovače určený pro zobrazení.            |
| `i2p.router.uptime`                    | long   | Doba běhu směrovače v milisekundách. Starší verze i2pd mohou vracet řetězec. |
| `i2p.router.version`                   | Řetězec| Plná verze směrovače.                                                  |
| `i2p.router.net.status`                | long   | Kód síťového stavu; viz níže uvedená tabulka.                           |
| `i2p.router.net.bw.inbound.1s`         | double | Aktuální příchozí šířka pásma v bajtech za sekundu.                    |
| `i2p.router.net.bw.inbound.15s`        | double | Průměrná příchozí šířka pásma za 15 sekund v bajtech za sekundu.         |
| `i2p.router.net.bw.outbound.1s`        | double | Aktuální odchozí šířka pásma v bajtech za sekundu.                      |
| `i2p.router.net.bw.outbound.15s`       | double | Průměrná odchozí šířka pásma za 15 sekund v bajtech za sekundu.         |
| `i2p.router.net.tunnels.participating` | long   | Počet tunelů, ve kterých tento směrovač účinkuje.                       |
#### Výčet stavového kódu (`i2p.router.net.status`)

| Kód | Význam                                              |
|-----|-----------------------------------------------------|
| 0   | OK                                                  |
| 1   | TESTOVÁNÍ                                           |
| 2   | ZABLOKOVÁNO FIREWALLU                               |
| 3   | SKRYTÝ                                              |
| 4   | VAROVÁNÍ_ZABLOKOVÁNO_FIREWALLU_A_RYCHLÝ             |
| 5   | VAROVÁNÍ_ZABLOKOVÁNO_FIREWALLU_A_FLOODFILL           |
| 6   | VAROVÁNÍ_ZABLOKOVÁNO_FIREWALLU_S_PŘÍCHODNÝM_TCP      |
| 7   | VAROVÁNÍ_ZABLOKOVÁNO_FIREWALLU_A_UDP_VYPNUTO         |
| 8   | CHYBA_I2CP                                          |
| 9   | CHYBA_ROZDÍLU_V_ČASE                                |
| 10  | CHYBA_SOUKROMÉ_TCP_ADRESY                           |
| 11  | CHYBA_SYMETRICKÉ_NAT                                |
| 12  | CHYBA_UDP_PORT_UŽ_OBSAZEN                           |
| 13  | CHYBA_ŽÁDNÍ_AKTIVNÍ_PARTNEŘI_ZKONTROLUJTE_PŘIPOJENÍ_A_FIREWALL |
| 14  | CHYBA_UDP_VYPNUTO_A_TCP_NE nastaveno                |
#### Síťová databáze a pole protějšku

| Klíč                                 | Typ     | Popis                                              |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | Počet známých peerů, s výjimkou místního směrovače. |
| `i2p.router.netdb.activepeers`       | long    | Počet aktivních peerů.                             |
| `i2p.router.netdb.fastpeers`         | long    | Počet peerů klasifikovaných jako rychlé.           |
| `i2p.router.netdb.highcapacitypeers` | long    | Počet peerů klasifikovaných jako vysoké kapacity.  |
| `i2p.router.netdb.isreseeding`       | boolean | Udává, zda probíhá opětovné zasazování (reseed).   |
**Pole odpovědi (result)**   Podle oficiální dokumentace (GetI2P):   - `i2p.router.status` (String) — čitelný stav   - `i2p.router.uptime` (long) — milisekundy (nebo string pro starší i2pd) :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — řetězec verze :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — příchozí šířka pásma v B/s :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — odchozí šířka pásma v B/s :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — číselný stavový kód (viz výčet níže) :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — počet účastnických tunelů :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — statistiky peerů v netDb :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — zda je aktivní reseed :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — celkový počet známých peerů :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Parametr | Typ    | Popis                          |
|----------|--------|--------------------------------|
| `Stat`   | Řetězec| Název RateStat směrovače.       |
| `Period` | long   | Doba výpočtu v milisekundách.  |
Používá se k načtení metrik rychlosti (např. šířka pásma, úspěšnost tunnelů) během daného časového okna.

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
**Příklad požadavku**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Ukázková odpověď**

### 4.3 RouterManager

---

| Parametr            | Výsledek          | Popis                                                                 |
|---------------------|-------------------|----------------------------------------------------------------------|
| `Restart`           | null              | Spustí okamžité restartování směrovače.                               |
| `RestartGraceful`   | null              | Restartuje po vypršení platnosti zapojených tunelů.                  |
| `Shutdown`          | null              | Spustí okamžité vypnutí směrovače.                                    |
| `ShutdownGraceful`  | null              | Vypne po vypršení platnosti zapojených tunelů.                       |
| `Reseed`            | null              | Spustí reseedování směrovače.                                         |
| `FindUpdates`       | boolean nebo String | Blokující. Hledá podepsanou aktualizaci směrovače.                   |
| `Update`            | String            | Blokující. Spustí podepsanou aktualizaci směrovače a vrátí její konečný stav. |
Provádět administrativní akce.

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
**Povolené parametry / metody**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Příklad požadavku**

### 4.4 NetworkSetting

**Úspěšná odpověď**

---

| Klíč                            | Přijatá hodnota                                     | Popis                                                      |
|---------------------------------|-----------------------------------------------------|------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | Řetězec, 1–65535                                    | NTCP port; změna vyžaduje restart.                         |
| `i2p.router.net.ntcp.hostname`  | Řetězec                                             | NTCP hostname; změna vyžaduje restart.                     |
| `i2p.router.net.ntcp.autoip`    | `always`, `true` nebo `false`                       | Automatický výběr adresy NTCP.                             |
| `i2p.router.net.ssu.port`       | Řetězec, 1–65535                                    | SSU port; změna vyžaduje restart.                          |
| `i2p.router.net.ssu.hostname`   | Řetězec                                             | Externí SSU hostname; změna vyžaduje restart.              |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu` nebo `local,upnp,ssu`| Zdroje detekce adresy pro SSU.                             |
| `i2p.router.net.ssu.detectedip` | null                                                | Pouze pro čtení, zjištěná SSU adresa.                      |
| `i2p.router.net.upnp`           | Řetězec                                             | Nastavení UPnP.                                            |
| `i2p.router.net.bw.share`       | Řetězec, 0–100                                      | Procento šířky pásma dostupné pro účast v tunelech.        |
| `i2p.router.net.bw.in`          | Řetězec s nezáporným celým číslem                  | Limit vstupní šířky pásma v KiB/s.                         |
| `i2p.router.net.bw.out`         | Řetězec s nezáporným celým číslem                  | Limit výstupní šířky pásma v KiB/s.                        |
| `i2p.router.net.laptopmode`     | Řetězec                                             | Nastavení režimu notebooku.                                |
Získat nebo nastavit parametry konfigurace sítě (porty, upnp, sdílení šířky pásma, atd.)

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
**Příklad požadavku (získání aktuálních hodnot)**

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
**Ukázková odpověď**

> Poznámka: verze i2pd starší než 2.41 mohou vracet číselné typy namísto řetězců — klienti by měli zvládnout oba případy. :contentReference[oaicite:11]{index=11}

### 4.5 Pokročilé nastavení

---

| Parametr | Typ | Popis |
|-----------|-----|-------|
| `get` | Řetězec | Vrací jedno nastavení uvnitř objektu výsledku `get`. |
| `getAll` | n/a | Vrací kompletní mapu konfigurace uvnitř `getAll`. |
| `set` | Mapa&lt;Řetězec, Řetězec&gt; | Aktualizuje dodaná nastavení, aniž by odstranila ostatní klíče. |
| `setAll` | Mapa&lt;Řetězec, Řetězec&gt; | **Ničivé:** nahradí všechna nastavení a odstraní klíče, které nebyly poskytnuty. |
Umožňuje manipulaci s interními parametry routeru.

**Příklad požadavku**

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
**Příklad odpovědi**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Standardní chybové kódy JSON-RPC2

---

| Parametr | Typ | Popis |
|-----------|--------|-----------------------------|
| `Echo`    | Řetězec | Hodnota vrácená jako `Result`. |
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

### I2PControl specifické chybové kódy

Spravuje samotné I2PControl. Aktuální Java obsluha podporuje změnu hesla.

| Parametr                   | Typ    | Popis                                                                 |
|----------------------------|--------|-----------------------------------------------------------------------|
| `i2pcontrol.password`      | String | Nastaví nové heslo I2PControl a zruší stávající ověřovací tokeny.     |
Výsledek obsahuje `SettingsSaved`. Pokud bylo heslo změněno, výsledek také obsahuje `"i2pcontrol.password": null`. Nastavení listen-address a listen-port z běžného samostatného pluginu nejsou v aktuálním Java handleru aktivní.

> **Výchozí heslo:** `itoopie` — toto je tovární výchozí nastavení a **mělo by být okamžitě změněno** z bezpečnostních důvodů.

## 5. Kódy chyb

### Standardní kódy chyb JSON-RPC2

| Kód    | Význam               |
|--------|----------------------|
| -32700 | Chyba parsování JSON |
| -32600 | Neplatný požadavek    |
| -32601 | Metoda nenalezena    |
| -32602 | Neplatné parametry   |
| -32603 | Vnitřní chyba        |
### Specifické chybové kódy I2PControl

| Kód    | Význam                                                                                   |
|--------|------------------------------------------------------------------------------------------|
| -32001 | Bylo zadáno neplatné heslo                                                               |
| -32002 | Nebyl předložen žádný ověřovací token                                                     |
| -32003 | Ověřovací token neexistuje                                                               |
| -32004 | Zadaný ověřovací token vypršel a bude odstraněn                                          |
| -32005 | Verze I2PControl API nebyla uvedena, ale je vyžadována                                  |
| -32006 | Uvedená verze I2PControl API není službou I2PControl podporována                         |
> **Výchozí heslo:** `itoopie` — toto je tovární výchozí nastavení a **mělo by být okamžitě změněno** z bezpečnostních důvodů.

## 6. Použití a nejlepší postupy

- Vždy zahrňte parametr `Token` (kromě případů autentifikace).
- Při prvním použití změňte výchozí heslo (`itoopie`).
- Pro Java I2P se ujistěte, že je I2PControl webapp povolena přes WebApps.
- Buďte připraveni na drobné variace: některá pole mohou být čísla nebo řetězce v závislosti na verzi I2P.
- Zalamujte dlouhé stavové řetězce pro přívětivý výstup pro zobrazení.

> **Výchozí heslo:** `itoopie` — toto je tovární výchozí nastavení a **mělo by být okamžitě změněno** z bezpečnostních důvodů.
