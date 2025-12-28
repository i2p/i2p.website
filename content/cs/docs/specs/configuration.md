---
title: "Konfigurace routeru"
description: "Konfigurační možnosti a formáty pro I2P routery a klienty"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Přehled

Tento dokument poskytuje komplexní technickou specifikaci konfiguračních souborů I2P používaných routerem a různými aplikacemi. Pokrývá specifikace formátů souborů, definice vlastností a implementační detaily ověřené na základě zdrojového kódu I2P a oficiální dokumentace.

### Rozsah

- Konfigurační soubory a formáty pro Router
- Konfigurace klientských aplikací
- Konfigurace pro I2PTunnel tunnel
- Specifikace formátů souborů a implementace
- Funkce specifické pro jednotlivé verze a označení za zastaralé

### Poznámky k implementaci

Konfigurační soubory se čtou a zapisují pomocí metod `DataHelper.loadProps()` a `storeProps()` v jádrové knihovně I2P. Formát souboru se výrazně liší od serializovaného formátu používaného v protokolech I2P (viz [Specifikace obecných struktur – mapování typů](/docs/specs/common-structures/#type-mapping)).

---

## Obecný formát konfiguračního souboru

Konfigurační soubory I2P používají upravený formát Java Properties s konkrétními výjimkami a omezeními.

### Specifikace formátu

Vychází z [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) s následujícími zásadními rozdíly:

#### Kódování

- **MUSÍ** používat kódování UTF-8 (NE ISO-8859-1 jako ve standardních Java Properties)
- Implementace: Pro všechny operace se soubory používá pomocnou funkci `DataHelper.getUTF8()`

#### Escape sekvence

- **ŽÁDNÉ** escape sekvence nejsou rozpoznávány (včetně zpětného lomítka `\`)
- Pokračování řádku **NENÍ** podporováno
- Znaky zpětného lomítka jsou považovány za doslovné

#### Znaky komentáře

- `#` začíná komentář na libovolné pozici na řádku
- `;` začíná komentář pouze pokud je v prvním sloupci
- `!` **NE** začíná komentář (na rozdíl od Java Properties)

#### Oddělovače klíč-hodnota

- `=` je **JEDINÝ** platný oddělovač klíč–hodnota
- `:` **NENÍ** rozpoznáván jako oddělovač
- Prázdné znaky **NEJSOU** rozpoznávány jako oddělovače

#### Zpracování bílých znaků

- Počáteční a koncové bílé znaky u klíčů **NEJSOU** ořezávány
- Počáteční a koncové bílé znaky u hodnot **JSOU** ořezávány

#### Zpracování řádků

- Řádky bez `=` jsou ignorovány (považovány za komentáře nebo prázdné řádky)
- Prázdné hodnoty (`key=`) jsou podporovány od verze 0.9.10
- Klíče s prázdnými hodnotami se běžně ukládají a načítají

#### Omezení znaků

**Klíče NESMÍ obsahovat**: - `#` (křížek) - `=` (znak rovná se) - `\n` (znak nového řádku) - Nesmí začínat znakem `;` (středník)

**Hodnoty NESMÍ obsahovat**: - `#` (symbol hash/pound) - `\n` (znak nového řádku) - Nesmí začínat ani končit znakem `\r` (návrat vozíku) - Nesmí začínat ani končit bílými znaky (automaticky ořezány)

### Řazení souborů

Konfigurační soubory nemusí být seřazeny podle klíče. Nicméně většina aplikací I2P řadí klíče abecedně při zápisu konfiguračních souborů pro usnadnění: - Ručních úprav - Operací diff ve verzovacích systémech - Čitelnosti pro člověka

### Podrobnosti implementace

#### Čtení konfiguračních souborů

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Chování**: - Čte soubory kódované v UTF-8 - Vynucuje všechna výše popsaná pravidla formátu - Ověřuje omezení znaků - Vrací prázdný objekt Properties, pokud soubor neexistuje - Vyvolá `IOException` při chybách čtení

#### Psaní konfiguračních souborů

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Chování**: - Zapisuje soubory v kódování UTF-8 - Řadí klíče abecedně (pokud není použito OrderedProperties) - Nastavuje oprávnění souborů na režim 600 (pouze čtení/zápis pro uživatele) od verze 0.8.1 - Vyvolává `IllegalArgumentException` při neplatných znacích v klíčích nebo hodnotách - Vyvolává `IOException` při chybách zápisu

#### Ověření formátu

Implementace provádí přísnou validaci: - Klíče a hodnoty se kontrolují na zakázané znaky - Neplatné položky vyvolávají výjimky při zápisových operacích - Čtení tiše ignoruje chybně formátované řádky (řádky bez `=`)

### Příklady formátu

#### Platný konfigurační soubor

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Příklady neplatné konfigurace

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Základní knihovna a konfigurace Routeru

### Konfigurace klientů (clients.config)

**Umístění**: `$I2P_CONFIG_DIR/clients.config` (starší) nebo `$I2P_CONFIG_DIR/clients.config.d/` (moderní)   **Konfigurační rozhraní**: konzole routeru na `/configclients`   **Změna formátu**: Verze 0.9.42 (srpen 2019)

#### Adresářová struktura (verze 0.9.42+)

Od verze 0.9.42 je výchozí soubor clients.config automaticky rozdělen na jednotlivé konfigurační soubory:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Chování při migraci**: - Při prvním spuštění po aktualizaci na verzi 0.9.42+ se monolitický soubor automaticky rozdělí - V rozdělených souborech mají vlastnosti předponu `clientApp.0.` - Zastaralý formát je nadále podporován kvůli zpětné kompatibilitě - Rozdělený formát umožňuje modulární balíčkování a správu zásuvných modulů

#### Formát vlastností

Řádky jsou ve tvaru `clientApp.x.prop=val`, kde `x` je číslo aplikace.

**Požadavky na číslování aplikací**: - MUSÍ začínat od 0 - MUSÍ být po sobě jdoucí (bez mezer) - Pořadí určuje sekvenci spouštění

#### Povinné vlastnosti

##### hlavní

- **Typ**: Řetězec (plně kvalifikovaný název třídy)
- **Povinné**: Ano
- **Popis**: V závislosti na typu klienta (spravovaný vs. nespravovaný) bude spuštěn konstruktor nebo metoda `main()` v této třídě
- **Příklad**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Volitelné vlastnosti

##### název

- **Typ**: Řetězec
- **Povinné**: Ne
- **Popis**: Název zobrazený v router console
- **Příklad**: `clientApp.0.name=Router Console`

##### args

- **Typ**: Řetězec (oddělený mezerou nebo tabulátorem)
- **Povinné**: Ne
- **Popis**: Argumenty předávané konstruktoru hlavní třídy nebo metodě main()
- **Uvozování**: Argumenty obsahující mezery nebo tabulátory lze uzavřít do uvozovek `'` nebo `"`
- **Příklad**: `clientApp.0.args=-d $CONFIG/eepsite`

##### zpoždění

- **Typ**: Integer (sekundy)
- **Povinné**: Ne
- **Výchozí**: 120
- **Popis**: Počet sekund čekání před spuštěním klienta
- **Přebíjí**: Přebito `onBoot=true` (nastaví zpoždění na 0)
- **Speciální hodnoty**:
  - `< 0`: Čekat, než router dosáhne stavu RUNNING, potom spustit ihned v novém vlákně
  - `= 0`: Spustit ihned ve stejném vlákně (výjimky se propagují do konzole)
  - `> 0`: Spustit po zpoždění v novém vlákně (výjimky jsou zaznamenány do logu, nepropagují se)

##### onBoot

- **Typ**: Boolean (logická hodnota)
- **Povinné**: Ne
- **Výchozí**: false
- **Popis**: Vynutí zpoždění 0 a přepíše explicitně zadané nastavení zpoždění
- **Použití**: Spustí kritické služby okamžitě při startu routeru

##### startOnLoad

- **Typ**: Boolean
- **Povinné**: Ne
- **Výchozí**: true
- **Popis**: Zda vůbec spustit klienta
- **Případ použití**: Zakázat klienty bez odstranění konfigurace

#### Vlastnosti specifické pro zásuvný modul

Tyto vlastnosti používají pouze zásuvné moduly (nikoli základní klienti):

##### stopargs

- **Typ**: String (oddělený mezerami nebo tabulátory)
- **Popis**: Argumenty předané pro zastavení klienta
- **Nahrazování proměnných**: Ano (viz níže)

##### uninstallargs

- **Typ**: Řetězec (oddělený mezerou nebo tabulátorem)
- **Popis**: Argumenty předávané při odinstalaci klienta
- **Substituce proměnných**: Ano (viz níže)

##### classpath (vyhledávací cesta pro třídy)

- **Typ**: Řetězec (cesty oddělené čárkami)
- **Popis**: Další položky classpath pro klienta
- **Nahrazování proměnných**: Ano (viz níže)

#### Substituce proměnných (pouze pro pluginy)

Následující proměnné se nahrazují v `args`, `stopargs`, `uninstallargs` a `classpath` u zásuvných modulů:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Poznámka**: Nahrazování proměnných se provádí pouze u pluginů, nikoli u klientů jádra.

#### Typy klientů

##### Spravovaní klienti

- Konstruktor se volá s parametry `RouterContext` a `ClientAppManager`
- Klient musí implementovat rozhraní `ClientApp`
- Životní cyklus řídí router
- Lze dynamicky spouštět, zastavovat a restartovat

##### Nespravovaní klienti

- Je volána metoda `main(String[] args)`
- Běží v samostatném vlákně
- Životní cyklus není spravován routerem
- Zastaralý typ klienta

#### Ukázková konfigurace

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Konfigurace protokolování (logger.config)

**Umístění**: `$I2P_CONFIG_DIR/logger.config`   **Konfigurační rozhraní**: konzole routeru na `/configlogging`

#### Reference vlastností

##### Konfigurace vyrovnávací paměti konzole

###### logger.consoleBufferSize

- **Typ**: Celé číslo
- **Výchozí**: 20
- **Popis**: Maximální počet logových zpráv ukládaných do vyrovnávací paměti v konzoli
- **Rozsah**: 1-1000 doporučeno

##### Formátování data a času

###### logger.dateFormat

- **Typ**: String (vzor SimpleDateFormat)
- **Výchozí**: Z místního nastavení systému
- **Příklad**: `HH:mm:ss.SSS`
- **Dokumentace**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Úrovně logování

###### logger.defaultLevel

- **Typ**: výčtový typ
- **Výchozí**: ERROR
- **Hodnoty**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Popis**: Výchozí úroveň protokolování pro všechny třídy

###### logger.minimumOnScreenLevel

- **Typ**: výčet
- **Výchozí**: CRIT
- **Hodnoty**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Popis**: Minimální úroveň pro zprávy zobrazované na obrazovce

###### logger.record.{class}

- **Typ**: výčtový typ
- **Hodnoty**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Popis**: Předefinování úrovně logování pro jednotlivé třídy
- **Příklad**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Možnosti zobrazení

###### logger.displayOnScreen

- **Typ**: logická hodnota
- **Výchozí**: true
- **Popis**: Zda zobrazovat zprávy logu v konzolovém výstupu

###### logger.dropDuplicates

- **Typ**: Logická hodnota
- **Výchozí hodnota**: true
- **Popis**: Zahazuje duplicitní po sobě jdoucí záznamy v logu

###### logger.dropOnOverflow

- **Typ**: Boolean
- **Výchozí**: false
- **Popis**: Zahazovat zprávy, když je vyrovnávací paměť plná (namísto blokování)

##### Chování vyprázdňování vyrovnávací paměti

###### logger.flushInterval

- **Typ**: Celé číslo (v sekundách)
- **Výchozí hodnota**: 29
- **Od**: Verze 0.9.18
- **Popis**: Jak často vyprazdňovat vyrovnávací paměť logu na disk

##### Konfigurace formátu

###### logger.format

- **Typ**: Řetězec (sekvence znaků)
- **Popis**: Šablona formátu logovací zprávy
- **Formátovací znaky**:
  - `d` = datum/čas
  - `c` = název třídy
  - `t` = název vlákna
  - `p` = priorita (úroveň logu)
  - `m` = zpráva
- **Příklad**: `dctpm` vytvoří [časové razítko] [třída] [vlákno] [úroveň] zpráva

##### Komprese (Verze 0.9.56+)

###### logger.gzip

- **Typ**: Boolean
- **Výchozí**: false
- **Od**: Verze 0.9.56
- **Popis**: Povolit kompresi gzip pro rotované soubory protokolu

###### logger.minGzipSize

- **Typ**: Celé číslo (v bajtech)
- **Výchozí**: 65536
- **Od**: verze 0.9.56
- **Popis**: Minimální velikost souboru pro aktivaci komprese (výchozí 64 KB)

##### Správa souborů

###### logger.logBufferSize

- **Typ**: Celé číslo (v bajtech)
- **Výchozí**: 1024
- **Popis**: Maximální počet zpráv, které se mají ukládat do vyrovnávací paměti před jejím vyprázdněním

###### logger.logFileName

- **Typ**: Řetězec (cesta k souboru)
- **Výchozí**: `logs/log-@.txt`
- **Popis**: Vzor pojmenování logovacího souboru (`@` se nahradí číslem rotace)

###### logger.logFilenameOverride

- **Typ**: Řetězec (cesta k souboru)
- **Popis**: Přepíše název logovacího souboru (zakáže vzor rotace)

###### logger.logFileSize

- **Typ**: Řetězec (velikost s jednotkou)
- **Výchozí**: 10M
- **Jednotky**: K (kilobajty), M (megabajty), G (gigabajty)
- **Příklad**: `50M`, `1G`

###### logger.logRotationLimit

- **Typ**: Celé číslo
- **Výchozí hodnota**: 2
- **Popis**: Nejvyšší číslo rotovaného souboru logu (log-0.txt až log-N.txt)

#### Příklad konfigurace

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Konfigurace pluginu

#### Konfigurace jednotlivého zásuvného modulu (plugins/*/plugin.config)

**Umístění**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Formát**: Standardní formát konfiguračního souboru I2P   **Dokumentace**: [Specifikace zásuvného modulu](/docs/specs/plugin/)

##### Povinné vlastnosti

###### název

- **Typ**: Řetězec
- **Povinné**: Ano
- **Popis**: Zobrazovaný název zásuvného modulu
- **Příklad**: `name=I2P Plugin Example`

###### klíč

- **Typ**: Řetězec (veřejný klíč)
- **Povinné**: Ano (vynechte u zásuvných modulů podepsaných pomocí SU3)
- **Popis**: Veřejný klíč používaný k ověření podpisu zásuvného modulu
- **Formát**: Podpisový klíč kódovaný v Base64

###### podepisovatel

- **Typ**: řetězec
- **Povinné**: Ano
- **Popis**: Identita signatáře pluginu
- **Příklad**: `signer=user@example.i2p`

###### verze

- **Typ**: String (formát VersionComparator)
- **Povinné**: Ano
- **Popis**: Verze pluginu pro kontrolu aktualizací
- **Formát**: sémantické verzování nebo vlastní porovnatelný formát
- **Příklad**: `version=1.2.3`

##### Vlastnosti zobrazení

###### datum

- **Typ**: Long (Unixové časové razítko v milisekundách)
- **Popis**: Datum vydání zásuvného modulu

###### autor

- **Typ**: String
- **Popis**: Jméno autora zásuvného modulu

###### websiteURL

- **Typ**: Řetězec (URL)
- **Popis**: URL webu zásuvného modulu

###### updateURL

- **Typ**: Řetězec (URL)
- **Popis**: URL pro kontrolu aktualizací zásuvného modulu

###### updateURL.su3

- **Type**: Řetězec (URL)
- **Since**: Verze 0.9.15
- **Description**: Aktualizační URL ve formátu SU3 (upřednostňováno)

###### popis

- **Typ**: String
- **Popis**: Anglický popis zásuvného modulu

###### description_{language}

- **Typ**: řetězec
- **Popis**: Lokalizovaný popis zásuvného modulu
- **Příklad**: `description_de=Deutsche Beschreibung`

###### licence

- **Typ**: řetězec
- **Popis**: Identifikátor licence zásuvného modulu
- **Příklad**: `license=Apache 2.0`

##### Instalační vlastnosti

###### nespouštět-při-instalaci

- **Typ**: logická hodnota
- **Výchozí**: false
- **Popis**: Zabrání automatickému spuštění po instalaci

###### Je vyžadován restart routeru

- **Typ**: Boolean
- **Výchozí**: false
- **Popis**: Vyžaduje restart routeru po instalaci

###### pouze pro instalaci

- **Typ**: Logická hodnota
- **Výchozí**: false
- **Popis**: Instalovat pouze jednou (bez aktualizací)

###### pouze pro aktualizace

- **Typ**: Boolean
- **Výchozí**: false
- **Popis**: Aktualizovat pouze stávající instalaci (bez čisté instalace)

##### Příklad konfigurace pluginu

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Globální konfigurace zásuvných modulů (plugins.config)

**Umístění**: `$I2P_CONFIG_DIR/plugins.config`   **Účel**: Globální povolení/zakázání nainstalovaných zásuvných modulů

##### Formát vlastnosti

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Název pluginu z plugin.config
- `startOnLoad`: Zda se má plugin spustit při spuštění routeru

##### Příklad

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Konfigurace webových aplikací (webapps.config)

**Umístění**: `$I2P_CONFIG_DIR/webapps.config`   **Účel**: Povolit/zakázat a konfigurovat webové aplikace

#### Formát vlastnosti

##### webapps.{name}.startOnLoad

- **Typ**: Boolean
- **Popis**: Zda spustit webovou aplikaci při spuštění routeru
- **Formát**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Typ**: Řetězec (cesty oddělené mezerou nebo čárkou)
- **Popis**: Další položky classpath pro webovou aplikaci
- **Formát**: `webapps.{name}.classpath=[paths]`

#### Nahrazování proměnných

Cesty podporují následující nahrazování proměnných:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Prohledávání classpathu (vyhledávací cesta pro třídy)

- **Základní webové aplikace**: Cesty relativní k `$I2P/lib`
- **Webové aplikace zásuvných modulů**: Cesty relativní k `$CONFIG/plugins/{appname}/lib`

#### Ukázková konfigurace

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Konfigurace routeru (router.config)

**Umístění**: `$I2P_CONFIG_DIR/router.config`   **Konfigurační rozhraní**: Konzole routeru na `/configadvanced`   **Účel**: Základní nastavení routeru a síťové parametry

#### Kategorie konfigurace

##### Konfigurace sítě

Nastavení šířky pásma:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Konfigurace transportu:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Chování routeru

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Konfigurace konzole

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Konfigurace času

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Poznámka**: Konfigurace routeru je rozsáhlá. Kompletní referenci vlastností najdete v konzoli routeru na `/configadvanced`.

---

## Konfigurační soubory aplikací

### Konfigurace adresáře (addressbook/config.txt)

**Umístění**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Aplikace**: SusiDNS   **Účel**: Rozlišení názvů hostitelů a správa knihy adres

#### Umístění souborů

##### router_addressbook

- **Výchozí**: `../hosts.txt`
- **Popis**: Hlavní adresář (celosystémové názvy hostitelů)
- **Formát**: Standardní formát souboru hosts

##### privatehosts.txt

- **Umístění**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Popis**: Soukromé mapování názvů hostitelů
- **Priorita**: Nejvyšší (přebíjí všechny ostatní zdroje)

##### userhosts.txt

- **Umístění**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Popis**: Uživatelem přidaná mapování názvů hostitelů
- **Správa**: Prostřednictvím rozhraní SusiDNS

##### hosts.txt

- **Umístění**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Popis**: Stažený veřejný adresář adres
- **Zdroj**: Odběrové kanály

#### Služba názvů

##### BlockfileNamingService (Výchozí od verze 0.8.8)

Formát úložiště: - **Soubor**: `hostsdb.blockfile` - **Umístění**: `$I2P_CONFIG_DIR/addressbook/` - **Výkon**: ~10x rychlejší vyhledávání než hosts.txt - **Formát**: Binární databázový formát

Zastaralá jmenná služba: - **Formát**: Prostý text hosts.txt - **Stav**: Zastaralé, ale stále podporované - **Případ použití**: Ruční úpravy, správa verzí

#### Pravidla pro názvy hostitelů

Názvy hostitelů v I2P musí splňovat:

1. **Požadavek na TLD**: Musí končit na `.i2p`
2. **Maximální délka**: Celkem 67 znaků
3. **Znaková sada**: `[a-z]`, `[0-9]`, `.` (tečka), `-` (spojovník)
4. **Velikost písmen**: Pouze malá
5. **Omezení začátku**: Nesmí začínat `.` ani `-`
6. **Zakázané vzory**: Nesmí obsahovat `..`, `.-` ani `-.` (od verze 0.6.1.33)
7. **Vyhrazeno**: Base32 názvy hostitelů `*.b32.i2p` (52 znaků base32.b32.i2p)

##### Platné příklady

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Neplatné příklady

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Správa odběrů

##### subscriptions.txt

- **Umístění**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Formát**: Jedna adresa URL na řádek
- **Výchozí**: `http://i2p-projekt.i2p/hosts.txt`

##### Formát odběrového kanálu (od verze 0.9.26)

Pokročilý formát kanálu s metadaty:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Vlastnosti metadat: - `added`: Datum, kdy byl název hostitele přidán (formát YYYYMMDD) - `src`: Identifikátor zdroje - `sig`: Volitelný podpis

**Zpětná kompatibilita**: Jednoduchý formát hostname=destination je nadále podporován.

#### Příklad konfigurace

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Konfigurace I2PSnarku (i2psnark.config.d/i2psnark.config)

**Umístění**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Aplikace**: I2PSnark BitTorrent klient   **Konfigurační rozhraní**: Webové GUI na http://127.0.0.1:7657/i2psnark

#### Struktura adresářů

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Hlavní konfigurace (i2psnark.config)

Minimální výchozí konfigurace:

```properties
i2psnark.dir=i2psnark
```
Další vlastnosti spravované přes webové rozhraní:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Konfigurace jednotlivého torrentu

**Umístění**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Formát**: Nastavení pro jednotlivé torrenty   **Správa**: Automatická (přes webové GUI)

Mezi vlastnosti patří: - Nastavení nahrávání/stahování specifická pro torrent - Priority souborů - Informace o trackeru - Limity peerů

**Poznámka**: Konfigurace torrentů se primárně spravují prostřednictvím webového rozhraní. Ruční úpravy se nedoporučují.

#### Uspořádání dat torrentu

Úložiště dat je oddělené od konfigurace:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Konfigurace I2PTunnel (i2ptunnel.config)

**Umístění**: `$I2P_CONFIG_DIR/i2ptunnel.config` (starší) nebo `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (moderní)   **Konfigurační rozhraní**: Router console na `/i2ptunnel`   **Změna formátu**: Verze 0.9.42 (srpen 2019)

#### Struktura adresářů (verze 0.9.42+)

Od verze 0.9.42 je výchozí soubor i2ptunnel.config automaticky rozdělen:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Zásadní rozdíl ve formátu**: - **Monolitický formát**: Vlastnosti s prefixem `tunnel.N.` - **Rozdělený formát**: Vlastnosti **NEJSOU** s prefixem (např. `description=`, nikoli `tunnel.0.description=`)

#### Chování při migraci

Při prvním spuštění po aktualizaci na 0.9.42: 1. Stávající i2ptunnel.config se načte 2. V i2ptunnel.config.d/ se vytvoří jednotlivé konfigurace pro každý tunnel 3. V rozdělených souborech jsou u vlastností odstraněny předpony 4. Původní soubor je zálohován 5. Starší formát je nadále podporován kvůli zpětné kompatibilitě

#### Konfigurační sekce

Konfigurace I2PTunnel je podrobně popsána v níže uvedené části [Referenční příručka konfigurace I2PTunnel](#i2ptunnel-configuration-reference). Popisy vlastností platí jak pro monolitický (`tunnel.N.property`), tak i pro dělený (`property`) formát.

---

## Referenční příručka ke konfiguraci I2PTunnel

Tato část poskytuje kompletní technickou referenci ke všem konfiguračním vlastnostem I2PTunnel. Vlastnosti jsou uvedeny v rozděleném formátu (bez prefixu `tunnel.N.`). Pro monolitický formát přidejte ke všem vlastnostem prefix `tunnel.N.`, kde N je číslo pro daný tunnel.

**Důležité**: Vlastnosti popsané ve tvaru `tunnel.N.option.i2cp.*` jsou implementovány v I2PTunnel a **NEJSOU** podporovány prostřednictvím jiných rozhraní, jako je protokol I2CP nebo SAM API.

### Základní vlastnosti

#### tunnel.N.description (popis)

- **Typ**: Řetězec
- **Kontext**: Všechny tunnels
- **Popis**: Člověku srozumitelný popis tunnelu pro zobrazení v UI
- **Příklad**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (název)

- **Typ**: Řetězec
- **Kontext**: Všechny tunnels
- **Povinné**: Ano
- **Popis**: Jedinečný identifikátor pro tunnel a zobrazovaný název
- **Příklad**: `name=I2P HTTP Proxy`

#### tunnel.N.type (typ)

- **Typ**: Výčet
- **Kontext**: Všechny tunnel
- **Povinné**: Ano
- **Hodnoty**:
  - `client` - Obecný klientský tunnel
  - `httpclient` - Klient HTTP proxy
  - `ircclient` - IRC klientský tunnel
  - `socksirctunnel` - SOCKS IRC proxy
  - `sockstunnel` - SOCKS proxy (verze 4, 4a, 5)
  - `connectclient` - Klient CONNECT proxy
  - `streamrclient` - Klient Streamr
  - `server` - Obecný serverový tunnel
  - `httpserver` - HTTP serverový tunnel
  - `ircserver` - IRC serverový tunnel
  - `httpbidirserver` - Obousměrný HTTP server
  - `streamrserver` - Streamr server

#### tunnel.N.interface (rozhraní)

- **Typ**: Řetězec (IP adresa nebo název hostitele)
- **Kontext**: Pouze pro Client tunnels
- **Výchozí**: 127.0.0.1
- **Popis**: Místní rozhraní, na které se má navázat pro příchozí připojení
- **Bezpečnostní poznámka**: Vázání na 0.0.0.0 umožňuje vzdálená připojení
- **Příklad**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Typ**: Celé číslo
- **Kontext**: Pouze klientské tunnels
- **Rozsah**: 1-65535
- **Popis**: Místní port, na kterém se naslouchá pro klientská spojení
- **Příklad**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Typ**: Řetězec (IP adresa nebo název hostitele)
- **Kontext**: Pouze server tunnels
- **Popis**: Místní server, na který se mají přeposílat připojení
- **Příklad**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Typ**: Celé číslo
- **Kontext**: Pouze serverové tunnels
- **Rozsah**: 1-65535
- **Popis**: Port na targetHost, ke kterému se připojit
- **Příklad**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Typ**: Řetězec (destinace oddělené čárkou nebo mezerou)
- **Kontext**: Pouze klientské tunnels
- **Formát**: `destination[:port][,destination[:port]]`
- **Popis**: I2P destinace, ke kterým se připojit
- **Příklady**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Typ**: Řetězec (IP adresa nebo název hostitele)
- **Výchozí**: 127.0.0.1
- **Popis**: adresa rozhraní I2CP pro I2P router
- **Poznámka**: Ignorováno při běhu v kontextu routeru
- **Příklad**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Typ**: celé číslo
- **Výchozí**: 7654
- **Rozsah**: 1-65535
- **Popis**: port I2CP routeru I2P
- **Poznámka**: Ignorováno při běhu v kontextu routeru
- **Příklad**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Typ**: Logická hodnota
- **Výchozí**: true
- **Popis**: Zda spustit tunnel při načtení I2PTunnel
- **Příklad**: `startOnLoad=true`

### Konfigurace proxy

#### tunnel.N.proxyList (proxyList)

- **Typ**: Řetězec (názvy hostitelů oddělené čárkami nebo mezerami)
- **Kontext**: Pouze proxy HTTP a SOCKS
- **Popis**: Seznam hostitelů outproxy
- **Příklad**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Konfigurace serveru

#### tunnel.N.privKeyFile (privKeyFile)

- **Type**: Řetězec (cesta k souboru)
- **Context**: Servery a trvalé klientské tunnels
- **Description**: Soubor obsahující soukromé klíče Destination (identifikátor cíle) pro trvalé použití
- **Path**: Absolutní nebo relativní vzhledem ke konfiguračnímu adresáři I2P
- **Example**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Typ**: Řetězec (název hostitele)
- **Kontext**: Pouze pro HTTP servery
- **Výchozí**: Base32 název hostitele cíle
- **Popis**: Hodnota hlavičky Host předaná lokálnímu serveru
- **Příklad**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Typ**: Řetězec (název hostitele)
- **Kontext**: Pouze servery HTTP
- **Popis**: Přepsání virtuálního hostitele pro konkrétní příchozí port
- **Případ použití**: Hostovat více webů na různých portech
- **Příklad**: `spoofedHost.8080=site1.example.i2p`

### Možnosti specifické pro klienta

#### tunnel.N.sharedClient (sharedClient)

- **Typ**: Boolean
- **Kontext**: Pouze client tunnels
- **Výchozí**: false
- **Popis**: Zda může být tento tunnel sdílen více klienty
- **Příklad**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Typ**: Boolean
- **Kontext**: Pouze klientské tunnels
- **Výchozí**: false
- **Popis**: Ukládat a znovu používat klíče destinace napříč restarty
- **Konflikt**: Vzájemně se vylučuje s `i2cp.newDestOnResume=true`
- **Příklad**: `option.persistentClientKey=true`

### Možnosti I2CP (implementace I2PTunnel)

**Důležité**: Tyto vlastnosti mají předponu `option.i2cp.`, ale jsou **implementovány v I2PTunnel**, nikoli ve vrstvě protokolu I2CP. Nejsou k dispozici prostřednictvím I2CP ani SAM API.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Typ**: Logická hodnota
- **Kontext**: Pouze klientské tunnely
- **Výchozí**: false
- **Popis**: Odloží vytvoření tunnelu až do prvního připojení
- **Scénář použití**: Šetří prostředky u zřídka používaných tunnelů
- **Příklad**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Typ**: Boolean
- **Kontext**: Pouze pro client tunnels
- **Výchozí**: false
- **Vyžaduje**: `i2cp.closeOnIdle=true`
- **Konflikt**: Vzájemně se vylučuje s `persistentClientKey=true`
- **Popis**: Vytvořit nový cíl po vypršení časového limitu nečinnosti
- **Příklad**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Typ**: Řetězec (base64-kódovaný klíč)
- **Kontext**: Pouze serverové tunnels
- **Popis**: Trvalý soukromý šifrovací klíč pro leaseset
- **Použití**: Zachovat konzistentní šifrovaný leaseset mezi restarty
- **Příklad**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Typ**: Řetězec (sigtype:base64)
- **Kontext**: Pouze pro serverové tunnels
- **Formát**: `sigtype:base64key`
- **Popis**: Trvalý soukromý klíč pro podepisování leaseset
- **Příklad**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Možnosti specifické pro server

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Typ**: Boolean
- **Kontext**: Pouze serverové tunnels
- **Výchozí**: false
- **Popis**: Použít jedinečnou místní IP pro každou vzdálenou I2P destinaci
- **Případ použití**: Sledovat IP klientů v serverových protokolech
- **Poznámka k zabezpečení**: Může snížit anonymitu
- **Příklad**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Typ**: Řetězec (název hostitele:port)
- **Kontext**: Pouze pro serverové tunnels
- **Popis**: Přepíše targetHost/targetPort pro příchozí port NNNN
- **Použití**: Směrování podle portu na různé lokální služby
- **Příklad**: `option.targetForPort.8080=localhost:8080`

### Konfigurace fondu vláken

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Typ**: Logická hodnota
- **Kontext**: Pouze pro serverové tunnels
- **Výchozí**: true
- **Popis**: Použít pool vláken pro zpracování spojení
- **Poznámka**: Vždy false pro standardní servery (ignorováno)
- **Příklad**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Typ**: Celé číslo
- **Kontext**: Pouze pro server tunnels
- **Výchozí**: 65
- **Popis**: Maximální velikost fondu vláken
- **Poznámka**: Ignorováno u standardních serverů
- **Příklad**: `option.i2ptunnel.blockingHandlerCount=100`

### Možnosti klienta HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Typ**: Boolean
- **Kontext**: Pouze pro klienty HTTP
- **Výchozí**: false
- **Popis**: Povolit SSL připojení k adresám .i2p
- **Příklad**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Typ**: Logická hodnota
- **Kontext**: Pouze klienti HTTP
- **Výchozí**: false
- **Popis**: Zakázat odkazy address helper (pomocník s adresami) v odpovědích proxy
- **Příklad**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Typ**: Řetězec (URL oddělené čárkami nebo mezerami)
- **Kontext**: pouze klienti HTTP
- **Popis**: Adresy URL Jump serverů (serverů poskytujících "jump" odkazy pro rozlišení názvů hostitelů)
- **Příklad**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Typ**: logická hodnota (Boolean)
- **Kontext**: pouze pro HTTP klienty
- **Výchozí**: false
- **Popis**: Předávat hlavičky Accept-* (kromě Accept a Accept-Encoding)
- **Příklad**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Typ**: Logická hodnota
- **Kontext**: Jen pro klienty HTTP
- **Výchozí**: false
- **Popis**: Předávat hlavičky Referer přes proxy
- **Poznámka k ochraně soukromí**: Může vést k úniku informací
- **Příklad**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Typ**: Booleovská hodnota
- **Kontext**: pouze klienti HTTP
- **Výchozí**: false
- **Popis**: Propouštět hlavičky User-Agent přes proxy
- **Poznámka k ochraně soukromí**: Může unikat informace o prohlížeči
- **Příklad**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Typ**: Boolean
- **Kontext**: Pouze klienti HTTP
- **Výchozí**: false
- **Popis**: Předávat hlavičky Via přes proxy
- **Příklad**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Typ**: Řetězec (destinace oddělené čárkou nebo mezerou)
- **Kontext**: Pouze klienti HTTP
- **Popis**: SSL výstupní proxy v rámci sítě pro HTTPS
- **Příklad**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Typ**: Boolean
- **Kontext**: Pouze HTTP klienti
- **Výchozí**: true
- **Popis**: Použít registrované lokální zásuvné moduly outproxy
- **Příklad**: `option.i2ptunnel.useLocalOutproxy=true`

### Autentizace klienta HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Typ**: výčtový typ
- **Kontext**: Pouze klienti HTTP
- **Výchozí**: `false`
- **Hodnoty**: `true`, `false`, `basic`, `digest`
- **Popis**: Vyžaduje lokální autentizaci pro přístup k proxy
- **Poznámka**: `true` je ekvivalentní `basic`
- **Příklad**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Typ**: Řetězec (32znakový hexadecimální řetězec malými písmeny)
- **Kontext**: pouze HTTP klienti
- **Vyžaduje**: `proxyAuth=basic` nebo `proxyAuth=digest`
- **Popis**: MD5 hash hesla pro uživatele USER
- **Zastaralé**: místo toho použijte SHA-256 (0.9.56+)
- **Příklad**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Typ**: Řetězec (64 znaků, hexadecimální, malými písmeny)
- **Kontext**: Pouze klienti HTTP
- **Vyžaduje**: `proxyAuth=digest`
- **Od verze**: Verze 0.9.56
- **Standard**: RFC 7616
- **Popis**: SHA-256 hash hesla pro uživatele USER
- **Příklad**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Autentizace outproxy (proxy z I2P do běžného internetu)

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Typ**: Boolean
- **Kontext**: Pouze pro HTTP klienty
- **Výchozí**: false
- **Popis**: Odesílat údaje pro ověření na outproxy (výstupní proxy)
- **Příklad**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Typ**: řetězec
- **Kontext**: pouze klienti HTTP
- **Vyžaduje**: `outproxyAuth=true`
- **Popis**: Uživatelské jméno pro ověření u outproxy (výstupní proxy)
- **Příklad**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Typ**: řetězec
- **Kontext**: pouze pro klienty HTTP
- **Vyžaduje**: `outproxyAuth=true`
- **Popis**: Heslo pro ověření u outproxy (výstupní proxy do clearnetu)
- **Zabezpečení**: Uloženo v prostém textu
- **Příklad**: `option.outproxyPassword=secret`

### Možnosti klienta SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Typ**: Řetězec (destinace oddělené čárkami nebo mezerami)
- **Kontext**: pouze pro klienty SOCKS
- **Popis**: Outproxy v rámci I2P pro nespecifikované porty
- **Příklad**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Typ**: Řetězec (destinace oddělené čárkami nebo mezerami)
- **Kontext**: pouze pro klienty SOCKS
- **Popis**: výstupní proxy v rámci sítě konkrétně pro port NNNN
- **Příklad**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Typ**: výčtový typ
- **Kontext**: pouze klienti SOCKS
- **Výchozí**: socks
- **Od**: verze 0.9.57
- **Hodnoty**: `socks`, `connect` (HTTPS)
- **Popis**: Typ konfigurované výstupní proxy
- **Příklad**: `option.outproxyType=connect`

### Možnosti serveru HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Typ**: Celé číslo
- **Kontext**: Pouze pro HTTP servery
- **Výchozí**: 0 (neomezeno)
- **Popis**: Maximální počet požadavků POST z jedné destinace za postCheckTime
- **Příklad**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Typ**: Celé číslo
- **Kontext**: Pouze HTTP servery
- **Výchozí**: 0 (neomezeno)
- **Popis**: Maximální počet požadavků POST ze všech destinací za postCheckTime
- **Příklad**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Typ**: Celé číslo (sekundy)
- **Kontext**: Pouze pro HTTP servery
- **Výchozí**: 300
- **Popis**: Časové okno pro kontrolu limitů POST
- **Příklad**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Typ**: celé číslo (sekundy)
- **Kontext**: pouze pro HTTP servery
- **Výchozí**: 1800
- **Popis**: Doba blokace po překročení limitu maxPosts pro jednu destinaci
- **Příklad**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Typ**: celé číslo (sekundy)
- **Kontext**: jen pro HTTP servery
- **Výchozí**: 600
- **Popis**: Doba trvání banu po překročení maxTotalPosts
- **Příklad**: `option.postTotalBanTime=1200`

### Možnosti zabezpečení HTTP serveru

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Typ**: Boolean
- **Kontext**: Pouze pro HTTP servery
- **Výchozí**: false
- **Popis**: Odmítat připojení, která zřejmě přicházejí přes inproxy (vstupní proxy)
- **Příklad**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Typ**: Logická hodnota
- **Kontext**: Pouze HTTP servery
- **Výchozí**: false
- **Od**: Verze 0.9.25
- **Popis**: Odmítá připojení s hlavičkou Referer
- **Příklad**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Typ**: Boolean
- **Kontext**: Pouze pro HTTP servery
- **Výchozí**: false
- **Od**: verze 0.9.25
- **Vyžaduje**: vlastnost `userAgentRejectList`
- **Popis**: Odmítne připojení, pokud User-Agent odpovídá
- **Příklad**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Typ**: Řetězec (řetězce pro porovnání oddělené čárkami)
- **Kontext**: Pouze HTTP servery
- **Od**: Verze 0.9.25
- **Rozlišování velikosti písmen**: Porovnávání rozlišující velikost písmen
- **Speciální**: "none" (od 0.9.33) odpovídá prázdnému User-Agent (HTTP hlavička identifikující klienta)
- **Popis**: Seznam vzorů User-Agent, které se mají odmítnout
- **Příklad**: `option.userAgentRejectList=Mozilla,Opera,none`

### Možnosti IRC serveru

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Typ**: Řetězec (vzor názvu hostitele)
- **Kontext**: pouze IRC servery
- **Výchozí**: `%f.b32.i2p`
- **Tokeny**:
  - `%f` = Úplný hash cíle v base32
  - `%c` = Zastřený hash cíle (viz cloakKey)
- **Popis**: Formát názvu hostitele odesílaný IRC serveru
- **Příklad**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Typ**: Řetězec (heslová fráze)
- **Kontext**: Pouze IRC servery
- **Výchozí**: Náhodné pro každou relaci
- **Omezení**: Bez uvozovek ani mezer
- **Popis**: Heslová fráze pro konzistentní maskování názvu hostitele
- **Případ použití**: Trvalé sledování uživatele napříč restarty/servery
- **Příklad**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Typ**: výčtový typ
- **Kontext**: pouze pro servery IRC
- **Výchozí**: user
- **Hodnoty**: `user`, `webirc`
- **Popis**: Metoda ověřování pro server IRC
- **Příklad**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Typ**: Řetězec (heslo)
- **Kontext**: Pouze pro servery IRC
- **Vyžaduje**: `method=webirc`
- **Omezení**: Bez uvozovek ani mezer
- **Popis**: Heslo pro autentizaci protokolu WEBIRC
- **Příklad**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Typ**: Řetězec (IP adresa)
- **Kontext**: Pouze pro servery IRC
- **Vyžaduje**: `method=webirc`
- **Popis**: Podvržená IP adresa pro protokol WEBIRC
- **Příklad**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Konfigurace SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Typ**: Boolean
- **Výchozí hodnota**: false
- **Kontext**: Všechny tunnels
- **Chování**:
  - **Servery**: Používat SSL pro připojení k místnímu serveru
  - **Klienti**: Vyžadovat SSL od místních klientů
- **Příklad**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Typ**: Řetězec (cesta k souboru)
- **Kontext**: Pouze client tunnels
- **Výchozí**: `i2ptunnel-(random).ks`
- **Cesta**: Relativní vůči `$(I2P_CONFIG_DIR)/keystore/`, pokud není absolutní
- **Automaticky generováno**: Vytvoří se, pokud neexistuje
- **Popis**: Soubor keystore (úložiště klíčů) obsahující soukromý klíč SSL
- **Příklad**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Typ**: Řetězec (heslo)
- **Kontext**: Pouze pro klientské tunnels
- **Výchozí**: changeit
- **Automaticky generováno**: Náhodné heslo, pokud je vytvořen nový keystore (úložiště klíčů)
- **Popis**: Heslo pro SSL keystore
- **Příklad**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Typ**: Řetězec (alias)
- **Kontext**: Pouze klientské tunnels
- **Automaticky generováno**: Vytvořeno, pokud je vygenerován nový klíč
- **Popis**: Alias pro soukromý klíč v úložišti klíčů
- **Příklad**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Typ**: Řetězec (heslo)
- **Kontext**: Pouze pro Client tunnels
- **Automaticky generováno**: Náhodné heslo, pokud je vytvořen nový klíč
- **Popis**: Heslo pro soukromý klíč v úložišti klíčů
- **Příklad**: `option.keyPassword=keypass123`

### Obecné možnosti I2CP a streamování

Všechny vlastnosti `tunnel.N.option.*` (které nejsou výše výslovně dokumentovány) jsou předávány rozhraní I2CP a streamovací knihovně s odstraněným prefixem `tunnel.N.option.`.

**Důležité**: Tato nastavení jsou oddělená od nastavení specifických pro I2PTunnel. Viz: - [Specifikace I2CP](/docs/specs/i2cp/) - [Specifikace streamingové knihovny](/docs/specs/streaming/)

Ukázkové možnosti streamování:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Kompletní příklad pro Tunnel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Historie verzí a časová osa funkcí

### Verze 0.9.10 (2013)

**Funkce**: Podpora prázdných hodnot v konfiguračních souborech - Klíče s prázdnými hodnotami (`key=`) jsou nyní podporovány - Dříve byly ignorovány nebo způsobovaly chyby při parsování

### Verze 0.9.18 (2015)

**Funkce**: Konfigurace intervalu vyprazdňování vyrovnávací paměti loggeru - Vlastnost: `logger.flushInterval` (výchozí 29 sekund) - Snižuje diskové I/O při zachování přijatelné latence zapisování do logu

### Verze 0.9.23 (listopad 2015)

**Zásadní změna**: Java 7 je minimální požadavek - podpora Javy 6 ukončena - vyžadováno pro další aktualizace zabezpečení

### Verze 0.9.25 (2015)

**Funkce**: Možnosti zabezpečení HTTP serveru - `tunnel.N.option.rejectReferer` - Odmítat požadavky s hlavičkou Referer - `tunnel.N.option.rejectUserAgents` - Odmítat vybrané hlavičky User-Agent - `tunnel.N.option.userAgentRejectList` - Vzory User-Agent k odmítnutí - **Případ použití**: Omezit webové roboty (crawlers) a nežádoucí klienty

### Verze 0.9.33 (leden 2018)

**Funkce**: Vylepšené filtrování User-Agentu - řetězec `userAgentRejectList` "none" odpovídá prázdnému User-Agentu - Další opravy chyb pro i2psnark, i2ptunnel, streaming, SusiMail

### Verze 0.9.41 (2019)

**Zrušení podpory**: BOB Protocol (protokol BOB) byl odstraněn z Androidu - uživatelé systému Android musí přejít na SAM (rozhraní Simple Anonymous Messaging) nebo I2CP

### Verze 0.9.42 (srpen 2019)

**Zásadní změna**: Rozdělení konfiguračních souborů - `clients.config` rozdělen do adresářové struktury `clients.config.d/` - `i2ptunnel.config` rozdělen do adresářové struktury `i2ptunnel.config.d/` - Automatická migrace při prvním spuštění po aktualizaci - Umožňuje modulární balíčkování a správu zásuvných modulů - Původní monolitický formát je nadále podporován

**Další funkce**: - vylepšení výkonu SSU - prevence propojování napříč sítěmi (Proposal 147) - počáteční podpora typu šifrování

### Verze 0.9.56 (2021)

**Funkce**: Vylepšení zabezpečení a protokolování - `logger.gzip` - Komprese Gzip pro rotované logy (výchozí: false) - `logger.minGzipSize` - Minimální velikost pro kompresi (výchozí: 65536 bajtů) - `tunnel.N.option.proxy.auth.USER.sha256` - Digest autentizace se SHA-256 (RFC 7616) - **Zabezpečení**: SHA-256 nahrazuje MD5 pro Digest autentizaci

### Verze 0.9.57 (leden 2023)

**Funkce**: Konfigurace typu SOCKS outproxy (výstupní proxy) - `tunnel.N.option.outproxyType` - Vyberte typ outproxy (socks|connect) - Výchozí: socks - Podpora HTTPS CONNECT pro HTTPS outproxy

### Verze 2.6.0 (červenec 2024)

**Zpětně nekompatibilní změna**: I2P-over-Tor zablokováno - Připojení z IP adres výstupních uzlů Tor jsou nyní odmítána - **Důvod**: zhoršuje výkon I2P, plýtvá prostředky výstupních uzlů Tor - **Dopad**: Uživatelé, kteří přistupují k I2P přes výstupní uzly Tor, budou blokováni - Nevýstupní uzly a klienti Tor nejsou ovlivněni

### Verze 2.10.0 (září 2025 - současnost)

**Hlavní funkce**: - **Post-kvantová kryptografie** k dispozici (volitelně přes Hidden Service Manager) - **Podpora UDP trackeru** pro I2PSnark ke snížení zátěže trackeru - **Stabilita Hidden Mode** vylepšení ke snížení vyčerpávání RouterInfo - Vylepšení sítě pro přetížené routery - Vylepšené procházení UPnP/NAT - Vylepšení NetDB s agresivním odstraňováním leaseset - Snížení pozorovatelnosti u událostí routeru

**Konfigurace**: Nebyly přidány žádné nové konfigurační vlastnosti

**Kritická nadcházející změna**: Příští vydání (pravděpodobně 2.11.0 nebo 3.0.0) bude vyžadovat Javu 17 nebo novější

---

## Zastarání a zpětně nekompatibilní změny

### Kritická zastarání

#### Přístup I2P-over-Tor (Verze 2.6.0+)

- **Stav**: BLOKOVÁNO od července 2024
- **Dopad**: Připojení z IP adres výstupních uzlů Toru jsou odmítána
- **Důvod**: Zhoršuje výkon sítě I2P, aniž by poskytovalo výhody v oblasti anonymity
- **Týká se**: Pouze výstupních uzlů Toru, nikoli přeposílacích uzlů (relay) ani běžných klientů Toru
- **Alternativa**: Používejte I2P nebo Tor samostatně, ne dohromady

#### Ověřování Digest (MD5)

- **Stav**: Zastaralé (použijte SHA-256)
- **Vlastnost**: `tunnel.N.option.proxy.auth.USER.md5`
- **Důvod**: MD5 je kryptograficky prolomený
- **Náhrada**: `tunnel.N.option.proxy.auth.USER.sha256` (od verze 0.9.56)
- **Časová osa**: MD5 je stále podporován, ale nedoporučuje se

### Změny v architektuře konfigurace

#### Monolitické konfigurační soubory (Verze 0.9.42+)

- **Dotčeno**: `clients.config`, `i2ptunnel.config`
- **Stav**: Zastaralé ve prospěch rozdělené adresářové struktury
- **Migrace**: Automatická při prvním spuštění po upgradu na 0.9.42
- **Kompatibilita**: Původní formát stále funguje (zpětně kompatibilní)
- **Doporučení**: Pro nové konfigurace používejte rozdělený formát

### Požadavky na verzi Javy

#### Podpora Javy 6

- **Ukončeno**: Verze 0.9.23 (listopad 2015)
- **Minimum**: Java 7 je vyžadována od verze 0.9.23

#### Požadavek na Javu 17 (nadcházející)

- **Stav**: KRITICKÁ NADCHÁZEJÍCÍ ZMĚNA
- **Cíl**: Další hlavní vydání po 2.10.0 (pravděpodobně 2.11.0 nebo 3.0.0)
- **Aktuální minimum**: Java 8
- **Vyžadovaná akce**: Připravte se na migraci na Javu 17
- **Časový plán**: Bude oznámen spolu s poznámkami k vydání

### Odebrané funkce

#### Protokol BOB (Android)

- **Odstraněno**: Verze 0.9.41
- **Platforma**: Pouze Android
- **Alternativa**: protokoly SAM nebo I2CP
- **Desktop**: BOB je stále dostupný na desktopových platformách

### Doporučené migrace

1. **Ověřování**: Přejít z MD5 na digest autentizaci se SHA-256
2. **Formát konfigurace**: Přejít na rozdělenou adresářovou strukturu pro klienty a tunnels
3. **Běhové prostředí Java**: Naplánovat aktualizaci na Java 17 před příštím hlavním vydáním
4. **Integrace s Tor**: Nesměrovat I2P přes výstupní uzly Toru

---

## Reference

### Oficiální dokumentace

- [Specifikace konfigurace I2P](/docs/specs/configuration/) - Oficiální specifikace formátu konfiguračního souboru
- [Specifikace zásuvných modulů I2P](/docs/specs/plugin/) - Konfigurace a balení zásuvných modulů
- [Společné struktury I2P - mapování typů](/docs/specs/common-structures/#type-mapping) - Formát serializace dat protokolu
- [Formát Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Specifikace základního formátu

### Zdrojový kód

- [Repozitář I2P Java Routeru](https://github.com/i2p/i2p.i2p) - zrcadlo na GitHubu
- [Gitea vývojářů I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - Oficiální repozitář zdrojových kódů I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Implementace I/O pro konfigurační soubory

### Komunitní zdroje

- [Fórum I2P](https://i2pforum.net/) - Aktivní komunitní diskuse a podpora
- [Web I2P](/) - Oficiální web projektu

### Dokumentace API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - Dokumentace API k metodám konfiguračních souborů

### Stav specifikace

- **Poslední aktualizace specifikace**: leden 2023 (verze 0.9.57)
- **Aktuální verze I2P**: 2.10.0 (září 2025)
- **Technická přesnost**: Specifikace zůstává přesná do verze 2.10.0 (bez zpětně nekompatibilních změn)
- **Údržba**: Živý dokument, aktualizovaný při změně formátu konfigurace
