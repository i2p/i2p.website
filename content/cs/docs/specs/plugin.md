---
title: "Formát balíčku zásuvného modulu"
description: ".xpi2p / .su3 pravidla balení pro zásuvné moduly I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Přehled

I2P pluginy jsou podepsané archivy, které rozšiřují funkčnost routeru. Dodávají se jako soubory `.xpi2p` nebo `.su3`, instalují se do `~/.i2p/plugins/<name>/` (nebo na Windows do `%APPDIR%\I2P\plugins\<name>\`) a běží s plnými oprávněními routeru bez sandboxingu (bez izolace).

### Podporované typy zásuvných modulů

- Webové aplikace konzole
- Nové eepsites s cgi-bin, webovými aplikacemi
- Motivy konzole
- Překlady konzole
- Programy v Javě (v rámci procesu nebo v samostatné JVM)
- Shell skripty a nativní binární soubory

### Bezpečnostní model

**KRITICKÉ:** Zásuvné moduly běží ve stejné JVM se stejnými oprávněními jako I2P router. Mají neomezený přístup k: - souborovému systému (čtení a zápis) - API routeru a internímu stavu - síťovým připojením - spouštění externích programů

Zásuvné moduly by měly být považovány za plně důvěryhodný kód. Uživatelé musí před instalací ověřit zdroje a podpisy zásuvných modulů.

---

## Formáty souborů

### Formát SU3 (důrazně doporučeno)

**Stav:** Aktivní, preferovaný formát od I2P 0.9.15 (září 2014)

Formát `.su3` poskytuje: - **RSA-4096 podpisové klíče** (oproti DSA-1024 v xpi2p) - Podpis uložený v hlavičce souboru - Magické číslo: `I2Psu3` - Lepší dopředná kompatibilita

**Struktura:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Formát XPI2P (starší, nedoporučovaný)

**Stav:** Podporováno kvůli zachování zpětné kompatibility, nedoporučuje se pro nové zásuvné moduly

Formát `.xpi2p` používá starší kryptografické podpisy: - **Podpisy DSA-1024** (zastaralé dle NIST-800-57) - 40bajtový podpis DSA předřazený souboru ZIP - Vyžaduje pole `key` v plugin.config

**Struktura:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Postup migrace:** Při migraci z xpi2p na su3 uveďte během přechodu obě `updateURL` i `updateURL.su3`. Moderní routery (0.9.15+) automaticky upřednostňují SU3.

---

## Struktura archivu a plugin.config

### Požadované soubory

**plugin.config** - Standardní konfigurační soubor I2P s páry klíč–hodnota

### Povinné vlastnosti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Příklady formátu verzí:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Platné oddělovače: `.` (tečka), `-` (pomlčka), `_` (podtržítko)

### Volitelné vlastnosti metadat

#### Zobrazit informace

- `date` - Datum vydání (časové razítko typu long v Javě)
- `author` - Jméno vývojáře (doporučeno `user@mail.i2p`)
- `description` - Popis v angličtině
- `description_xx` - Lokalizovaný popis (xx = kód jazyka)
- `websiteURL` - Domovská stránka zásuvného modulu (`http://foo.i2p/`)
- `license` - Identifikátor licence (např. "Apache-2.0", "GPL-3.0")

#### Aktualizovat konfiguraci

- `updateURL` - Umístění aktualizace XPI2P (zastaralé)
- `updateURL.su3` - Umístění aktualizace SU3 (formát aktualizačního balíčku I2P) (preferované)
- `min-i2p-version` - Minimální požadovaná verze I2P
- `max-i2p-version` - Maximální kompatibilní verze I2P
- `min-java-version` - Minimální verze Javy (např. `1.7`, `17`)
- `min-jetty-version` - Minimální verze Jetty (použijte `6` pro Jetty 6+)
- `max-jetty-version` - Maximální verze Jetty (použijte `5.99999` pro Jetty 5)

#### Chování instalace

- `dont-start-at-install` - Výchozí hodnota `false`. Pokud `true`, vyžaduje ruční spuštění
- `router-restart-required` - Výchozí hodnota `false`. Informuje uživatele, že je po aktualizaci nutný restart
- `update-only` - Výchozí hodnota `false`. Selže, pokud zásuvný modul ještě není nainstalován
- `install-only` - Výchozí hodnota `false`. Selže, pokud zásuvný modul již existuje
- `min-installed-version` - Minimální verze vyžadovaná pro aktualizaci
- `max-installed-version` - Maximální verze, kterou lze aktualizovat
- `disableStop` - Výchozí hodnota `false`. Skryje tlačítko Stop, pokud `true`

#### Integrace konzole

- `consoleLinkName` - Text odkazu na liště přehledu konzole
- `consoleLinkName_xx` - Lokalizovaný text odkazu (xx = kód jazyka)
- `consoleLinkURL` - Cíl odkazu (např. `/appname/index.jsp`)
- `consoleLinkTooltip` - Text při najetí myší (podporováno od 0.7.12-6)
- `consoleLinkTooltip_xx` - Lokalizovaný text nápovědy
- `console-icon` - Cesta k ikoně 32x32 (podporováno od 0.9.20)
- `icon-code` - Base64-kódované 32x32 PNG pro pluginy bez webových zdrojů (od 0.9.25)

#### Požadavky na platformu (pouze pro zobrazení)

- `required-platform-OS` - Požadavek na operační systém (není vynuceno)
- `other-requirements` - Dodatečné požadavky (např. "Python 3.8+")

#### Správa závislostí (neimplementováno)

- `depends` - Závislosti zásuvného modulu oddělené čárkou
- `depends-version` - Požadavky na verze závislostí
- `langs` - Obsah jazykového balíčku
- `type` - Typ zásuvného modulu (app/theme/locale/webapp)

### Substituce proměnných v aktualizační adrese URL

**Stav funkce:** K dispozici od I2P 1.7.0 (0.9.53)

Jak `updateURL`, tak `updateURL.su3` podporují platformově specifické proměnné:

**Proměnné:** - `$OS` - Operační systém: `windows`, `linux`, `mac` - `$ARCH` - Architektura: `386`, `amd64`, `arm64`

**Příklad:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Výsledek na Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Tím je možné mít u platformně specifických sestavení jediný soubor plugin.config.

---

## Struktura adresářů

### Standardní rozložení

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Účely adresáře

**console/locale/** - Soubory JAR obsahující balíčky lokalizačních prostředků pro základní překlady I2P - překlady specifické pro zásuvné moduly by měly být v `console/webapps/*.war` nebo `lib/*.jar`

**console/themes/** - Každá podsložka obsahuje kompletní motiv konzole - Automaticky přidáno do vyhledávací cesty motivů

**console/webapps/** - soubory `.war` pro integraci s konzolí - Spouští se automaticky, pokud nejsou zakázány v `webapps.config` - Název WAR nemusí odpovídat názvu pluginu

**eepsite/** - Kompletní eepsite s vlastní instancí Jetty - Vyžaduje konfiguraci `jetty.xml` se substitucí proměnných - Viz příklady pluginů zzzot a pebble

**lib/** - JAR knihovny pluginu - Zadejte do classpath (cesta ke třídám) prostřednictvím `clients.config` nebo `webapps.config`

---

## Konfigurace webové aplikace

### Formát webapps.config

Standardní konfigurační soubor I2P, který určuje chování webové aplikace.

**Syntaxe:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Důležité poznámky:** - Před verzí routeru 0.7.12-9 použijte kvůli kompatibilitě `plugin.warname.startOnLoad` - Před verzí API 0.9.53 fungoval classpath pouze tehdy, když se warname shodoval s názvem pluginu - Od verze 0.9.53+ funguje classpath pro libovolný název webové aplikace

### Osvědčené postupy pro webové aplikace

1. **Implementace ServletContextListener**
   - Implementujte `javax.servlet.ServletContextListener` pro úklid prostředků
   - Nebo přepište `destroy()` v servletu
   - Zajistí korektní ukončení během aktualizací a při zastavení routeru

2. **Správa knihoven**
   - Sdílené JARy umisťujte do `lib/`, ne do WARu
   - Odkazujte přes classpath (vyhledávací cesta tříd) v `webapps.config`
   - Umožňuje samostatnou instalaci/aktualizaci pluginů

3. **Vyhněte se konfliktům knihoven**
   - Nikdy nepřibalujte JARy Jetty, Tomcat ani se servletovým API
   - Nikdy nepřibalujte JARy ze standardní instalace I2P
   - Zkontrolujte sekci classpath kvůli standardním knihovnám

4. **Požadavky na kompilaci**
   - Nezahrnujte zdrojové soubory `.java` ani `.jsp`
   - Předkompilujte všechny JSP, abyste předešli zpoždění při spuštění
   - Nelze předpokládat dostupnost kompilátorů pro Java/JSP

5. **Kompatibilita se Servlet API**
   - I2P podporuje Servlet 3.0 (od 0.9.30)
   - **Skenování anotací NENÍ podporováno** (@WebContent)
   - Je nutné poskytnout tradiční deskriptor nasazení `web.xml`

6. **Verze Jetty**
   - Aktuální: Jetty 9 (I2P 0.9.30+)
   - Použijte `net.i2p.jetty.JettyStart` pro abstrakci
   - Chrání před změnami v API Jetty

---

## Konfigurace klienta

### Formát clients.config

Definuje klienty (služby) spouštěné pomocí zásuvného modulu.

**Základní klient:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Klient s funkcemi Zastavit/Odinstalovat:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Reference vlastností

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Nahrazování proměnných

Následující proměnné jsou nahrazeny v `args`, `stopargs`, `uninstallargs` a `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Spravovaní vs. nespravovaní klienti

**Spravovaní klienti (Doporučeno, od verze 0.9.4):** - Instanciováni pomocí ClientAppManager - Udržují reference a sledování stavu - Snazší správa životního cyklu - Lepší správa paměti

**Nespravovaní klienti:** - Spouštěni routerem, bez sledování stavu - Musí korektně zvládat vícenásobná volání start/stop - K koordinaci používejte statický stav nebo PID soubory - Voláno při vypnutí routeru (od verze 0.7.12-3)

### ShellService (od verze 0.9.53 / 1.7.0)

Generalizované řešení pro spouštění externích programů s automatickým sledováním stavu.

**Funkce:** - Spravuje životní cyklus procesu - Komunikuje s ClientAppManager (správcem klientských aplikací) - Automatická správa PID - Víceplatformní podpora

**Použití:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Pro skripty specifické pro platformu:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternativa (starší):** Napište Java wrapper (obalovací vrstva), který zjišťuje typ operačního systému, a zavolejte `ShellCommand` s příslušným souborem `.bat` nebo `.sh`.

---

## Postup instalace

### Postup instalace pro uživatele

1. Uživatel vloží adresu URL zásuvného modulu na stránku konfigurace zásuvných modulů konzole routeru (`/configplugins`)
2. Router stáhne soubor zásuvného modulu
3. Ověření podpisu (selže, pokud je klíč neznámý a je povolen striktní režim)
4. Kontrola integrity archivu ZIP
5. Rozbalit a parsovat `plugin.config`
6. Ověření kompatibility verzí (`min-i2p-version`, `min-java-version` atd.)
7. Detekce konfliktu názvu webové aplikace
8. Zastavení stávajícího zásuvného modulu v případě aktualizace
9. Validace adresáře (musí být pod `plugins/`)
10. Rozbalit všechny soubory do adresáře zásuvného modulu
11. Aktualizovat `plugins.config`
12. Spustit zásuvný modul (pokud není nastaveno `dont-start-at-install=true`)

### Zabezpečení a důvěra

**Správa klíčů:** - Model důvěry „first-key-seen“ (důvěra v první spatřený klíč) pro nové podepisovatele - Předinstalované jsou pouze klíče jrandom a zzz - Od verze 0.9.14.1 jsou neznámé klíče ve výchozím nastavení odmítány - Pokročilá konfigurační volba může toto chování pro účely vývoje přepsat

**Omezení instalace:** - Archivy se smějí rozbalit pouze do adresáře pluginů - Instalátor odmítá cesty mimo `plugins/` - Pluginy mohou po instalaci přistupovat k souborům i jinde - Žádné sandboxování ani izolace oprávnění

---

## Mechanismus aktualizace

### Proces kontroly aktualizací

1. Router čte `updateURL.su3` (preferované) nebo `updateURL` z plugin.config
2. Požadavek HTTP HEAD nebo částečný GET k načtení bajtů 41–56
3. Extrahovat řetězec verze ze vzdáleného souboru
4. Porovnat s nainstalovanou verzí pomocí VersionComparator
5. Je-li novější, vyzvat uživatele nebo ji automaticky stáhnout (dle nastavení)
6. Zastavit zásuvný modul
7. Nainstalovat aktualizaci
8. Spustit zásuvný modul (pokud se uživatelská předvolba nezměnila)

### Srovnání verzí

Verze jsou parsovány jako komponenty oddělené tečkou/pomlčkou/podtržítkem: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Maximální délka:** 16 bajtů (musí odpovídat hlavičce SUD/SU3)

### Osvědčené postupy pro aktualizace

1. Při každém vydání zvyšte verzi
2. Otestujte postup aktualizace z předchozí verze
3. Zvažte `router-restart-required` pro zásadní změny
4. Během migrace poskytněte jak `updateURL`, tak `updateURL.su3`
5. Pro testování použijte příponu čísla sestavení (`1.2.3-456`)

---

## Classpath a standardní knihovny

### Vždy k dispozici v Classpath (seznam cest, kde JVM hledá třídy)

Následující JARy z `$I2P/lib` jsou v I2P 0.9.30+ vždy v classpath (vyhledávací cestě pro třídy):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Zvláštní poznámky

**commons-logging.jar:** - Prázdný od 0.9.30 - Před 0.9.30: Apache Tomcat JULI - Před 0.9.24: Commons Logging + JULI - Před 0.9: Pouze Commons Logging

**jasper-compiler.jar:** - Prázdné od Jetty 6 (0.9)

**systray4j.jar:** - Odstraněno ve verzi 0.9.26

### Není na Classpath (musí být uvedeno)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Specifikace Classpath (seznam cest k třídám v Javě)

**V souboru clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**V webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Důležité:** Od verze 0.7.13-3 je classpath (vyhledávací cesta pro třídy) vázán na vlákno, nikoli na celou JVM. U každého klienta uveďte úplný classpath.

---

## Požadavky na verzi Javy

### Aktuální požadavky (říjen 2025)

**I2P 2.10.0 a starší:** - Minimální: Java 7 (vyžadováno od verze 0.9.24, leden 2016) - Doporučeno: Java 8 nebo novější

**I2P 2.11.0 a novější (PŘIPRAVUJE SE):** - **Minimálně: Java 17+** (oznáměno v poznámkách k vydání 2.9.0) - Poskytnuto upozornění dvě vydání dopředu (2.9.0 → 2.10.0 → 2.11.0)

### Strategie kompatibility zásuvných modulů

**Pro maximální kompatibilitu (až do I2P 2.10.x včetně):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Pro funkce Javy 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Pro funkce Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Příprava na 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Osvědčené postupy kompilace

**Při kompilaci s novějším JDK pro starší cílovou verzi:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Tím se zabrání použití rozhraní API, která nejsou dostupná v cílové verzi Javy.

---

## Komprese Pack200 - ZASTARALÉ

### Kritická aktualizace: Nepoužívejte Pack200

**Stav:** ZASTARALÉ A ODSTRANĚNO

Původní specifikace důrazně doporučovala kompresi Pack200 (formát komprese pro JAR balíčky) pro snížení velikosti o 60–65 %. **To již neplatí.**

**Časová osa:** - **JEP 336:** Pack200 označen jako zastaralý v Javě 11 (září 2018) - **JEP 367:** Pack200 odstraněn v Javě 14 (březen 2020)

**Oficiální specifikace aktualizací I2P uvádí:** > "Soubory JAR a WAR v zipu už nejsou komprimovány pomocí pack200, jak je popsáno výše pro soubory 'su2', protože novější běhová prostředí Javy už pack200 nepodporují."

**Co dělat:**

1. **Odstraňte pack200 z procesů sestavení okamžitě**
2. **Použijte standardní kompresi ZIP**
3. **Zvažte alternativy:**
   - ProGuard/R8 pro zmenšení kódu
   - UPX pro nativní binární soubory
   - Moderní kompresní algoritmy (zstd, brotli), pokud je k dispozici vlastní dekompresor

**Pro stávající pluginy:** - Staré routers (0.7.11-5 až po Java 10) stále umí rozbalit pack200 - Nové routers (Java 11+) neumí rozbalit pack200 - Znovu vydávejte pluginy bez komprese pack200

---

## Podpisové klíče a zabezpečení

### Generování klíčů (formát SU3)

Použijte skript `makeplugin.sh` z repozitáře i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Klíčové údaje:** - Algoritmus: RSA_SHA512_4096 - Formát: certifikát X.509 - Uložení: formát úložiště klíčů Java

### Podepisování zásuvných modulů

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Osvědčené postupy pro správu klíčů

1. **Vygenerujte jednou, chraňte navždy**
   - Routers odmítají duplicitní názvy klíčů s odlišnými klíči
   - Routers odmítají duplicitní klíče s odlišnými názvy klíčů
   - Aktualizace jsou odmítnuty, pokud se klíč a název neshodují

2. **Bezpečné ukládání**
   - Bezpečně zálohujte úložiště klíčů
   - Používejte silnou heslovou frázi
   - Nikdy neukládejte do systému správy verzí

3. **Rotace klíčů**
   - Není podporována současnou architekturou
   - Plánujte dlouhodobé používání klíčů
   - Zvažte vícepodpisová schémata pro týmový vývoj

### Zastaralé podepisování DSA (XPI2P)

**Stav:** Funkční, ale zastaralé

Podpisy DSA-1024 používané formátem xpi2p: - 40bajtový podpis - veřejný klíč o délce 172 znaků base64 - NIST-800-57 doporučuje jako minimum (L=2048, N=224) - I2P používá slabší (L=1024, N=160)

**Doporučení:** Místo toho použijte SU3 s RSA-4096.

---

## Pokyny pro vývoj pluginů

### Základní osvědčené postupy

1. **Dokumentace**
   - Poskytněte srozumitelný soubor README s pokyny k instalaci
   - Zdokumentujte konfigurační volby a výchozí hodnoty
   - Zahrňte seznam změn ke každému vydání
   - Uveďte požadované verze I2P/Java

2. **Optimalizace velikosti**
   - Zahrňte pouze nezbytné soubory
   - Nikdy nepřibalujte router JARy
   - Oddělte instalační vs. aktualizační balíčky (knihovny v lib/)
   - ~~Použijte kompresi Pack200~~ **ZASTARALÉ - Použijte standardní ZIP**

3. **Konfigurace**
   - Nikdy neupravujte `plugin.config` za běhu
   - Použijte samostatný konfigurační soubor pro nastavení za běhu
   - Zdokumentujte požadovaná nastavení pro router (SAM porty, tunnels, atd.)
   - Respektujte stávající nastavení uživatele

4. **Využití prostředků**
   - Vyhněte se agresivní spotřebě šířky pásma ve výchozím nastavení
   - Zaveďte rozumné limity využití procesoru
   - Při ukončení uvolněte prostředky
   - Používejte daemon threads (vlákna na pozadí) tam, kde je to vhodné

5. **Testování**
   - Otestovat instalaci/aktualizaci/odinstalaci na všech platformách
   - Otestovat aktualizace z předchozí verze
   - Ověřit zastavení/opětovné spuštění webové aplikace během aktualizací
   - Otestovat s minimální podporovanou verzí I2P

6. **Souborový systém**
   - Nikdy nezapisujte do `$I2P` (může být pouze pro čtení)
   - Data za běhu zapisujte do `$PLUGIN` nebo `$CONFIG`
   - Pro zjištění umístění adresářů použijte `I2PAppContext`
   - Nepředpokládejte umístění `$CWD`

7. **Kompatibilita**
   - Neduplikujte standardní třídy I2P
   - Rozšiřujte třídy, pokud je to nutné; nenahrazujte je
   - Zkontrolujte `min-i2p-version`, `min-jetty-version` v plugin.config
   - Testujte se staršími verzemi I2P, pokud je podporujete

8. **Obsluha ukončení**
   - Implementujte správné `stopargs` v souboru clients.config
   - Zaregistrujte shutdown hooks (háčky pro ukončení): `I2PAppContext.addShutdownTask()`
   - Ošetřete vícečetná volání spuštění/zastavení korektně
   - Nastavte všechna vlákna do režimu daemon (démon)

9. **Bezpečnost**
   - Ověřujte veškerý externí vstup
   - Nikdy nevolejte `System.exit()`
   - Respektujte soukromí uživatelů
   - Dodržujte zásady bezpečného programování

10. **Licencování**
    - Jasně uveďte licenci zásuvného modulu
    - Dodržujte licence přibalených knihoven
    - Zahrňte požadované uvedení autorství
    - Poskytněte přístup ke zdrojovému kódu, je-li to vyžadováno

### Pokročilé úvahy

**Zpracování časových pásem:** - Router nastaví časové pásmo JVM na UTC - Skutečné časové pásmo uživatele: `I2PAppContext` vlastnost `i2p.systemTimeZone`

**Detekce adresáře:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Číslování verzí:** - Použijte semantické verzování (major.minor.patch) - Přidejte číslo sestavení pro testování (1.2.3-456) - Zajistěte monotónní zvyšování při aktualizacích

**Přístup ke třídám routeru:** - Obecně se vyhněte závislostem na `router.jar` - Místo toho používejte veřejná API v `i2p.jar` - Budoucí verze I2P mohou omezit přístup ke třídám routeru

**Prevence pádů JVM (historické):** - Opraveno ve verzi 0.7.13-3 - Správně používejte ClassLoader (načítací mechanismus tříd) - Vyhněte se aktualizaci souborů JAR v běžícím zásuvném modulu - Navrhněte podporu restartu při aktualizaci, pokud je to nutné

---

## Zásuvné moduly pro Eepsite

### Přehled

Pluginy mohou poskytovat plnohodnotné eepsites s vlastními instancemi Jetty a I2PTunnel.

### Architektura

**Nepokoušejte se:** - Instalovat do existujícího eepsite - Slučovat s výchozím eepsite routeru - Předpokládat dostupnost jediného eepsite

**Místo toho:** - Spusťte novou instanci I2PTunnel (pomocí CLI) - Spusťte novou instanci Jetty - Nakonfigurujte obě v `clients.config`

### Ukázková struktura

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Nahrazování proměnných v jetty.xml

Použijte proměnnou `$PLUGIN` pro cesty:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router provádí nahrazení během spuštění zásuvného modulu.

### Příklady

Referenční implementace: - **zzzot plugin** - torrentový tracker - **pebble plugin** - blogová platforma

Obojí je k dispozici na stránce pluginů uživatele zzz (interní v I2P).

---

## Integrace konzole

### Odkazy na přehledovém panelu

Přidat kliknutelný odkaz do souhrnného panelu konzole routeru:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Lokalizované verze:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Ikony konzole

**Obrazový soubor (od 0.9.20):**

```properties
console-icon=/myicon.png
```
Cesta relativní k `consoleLinkURL`, pokud je uvedena (od verze 0.9.53), jinak relativní k názvu webové aplikace.

**Vložená ikona (od verze 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Vygenerujte pomocí:

```bash
base64 -w 0 icon-32x32.png
```
Nebo v Javě:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Požadavky: - 32x32 pixelů - formát PNG - zakódováno v Base64 (bez zalomení řádků)

---

## Internacionalizace

### Balíčky překladů

**Pro základní překlady I2P:** - Umístěte soubory JAR do `console/locale/` - Obsahují balíčky prostředků pro stávající aplikace I2P - Pojmenování: `messages_xx.properties` (xx = kód jazyka)

**Pro překlady specifické pro zásuvné moduly:** - Zahrňte do `console/webapps/*.war` - Nebo zahrňte do `lib/*.jar` - Použijte standardní mechanismus Java ResourceBundle

### Lokalizované řetězce v souboru plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Podporovaná pole: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Překlad motivu konzole

Motivy v `console/themes/` se automaticky přidávají do vyhledávací cesty motivů.

---

## Platformově specifické zásuvné moduly

### Přístup s oddělenými balíčky

Použijte různé názvy pluginů pro každou platformu:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Přístup založený na nahrazování proměnných

Jediný plugin.config s proměnnými platformy:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
V clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Detekce operačního systému za běhu

Přístup v jazyce Java k podmíněnému provádění:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Řešení problémů

### Časté problémy

**Zásuvný modul se nespouští:** 1. Zkontrolujte kompatibilitu s verzí I2P (`min-i2p-version`) 2. Ověřte verzi Javy (`min-java-version`) 3. Zkontrolujte logy routeru kvůli chybám 4. Ověřte, že všechny požadované JARy jsou v classpath (třídní cesta v Javě)

**Webová aplikace není přístupná:** 1. Ověřte, že `webapps.config` ji nezakazuje 2. Zkontrolujte kompatibilitu verze Jetty (`min-jetty-version`) 3. Ověřte, že je přítomen soubor `web.xml` (prohledávání anotací není podporováno) 4. Zkontrolujte konflikty v názvech webových aplikací

**Aktualizace selhává:** 1. Ověřte, že se řetězec verze zvýšil 2. Zkontrolujte, že podpis odpovídá podpisovému klíči 3. Ujistěte se, že název zásuvného modulu odpovídá nainstalované verzi 4. Zkontrolujte nastavení `update-only`/`install-only`

**Externí program nelze zastavit:** 1. Použijte ShellService pro automatické řízení životního cyklu 2. Implementujte správné zpracování `stopargs` 3. Zkontrolujte vyčištění souboru s PID 4. Ověřte ukončení procesu

### Protokolování ladění

Povolit ladicí protokolování v routeru:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Zkontrolujte protokoly:

```
~/.i2p/logs/log-router-0.txt
```
---

## Referenční informace

### Oficiální specifikace

- [Specifikace zásuvného modulu](/docs/specs/plugin/)
- [Formát konfigurace](/docs/specs/configuration/)
- [Specifikace aktualizace](/docs/specs/updates/)
- [Kryptografie](/docs/specs/cryptography/)

### Historie verzí I2P

**Aktuální vydání:** - **I2P 2.10.0** (8. září 2025)

**Hlavní vydání od 0.9.53:** - 2.10.0 (září 2025) - oznámení o Java 17+ - 2.9.0 (červen 2025) - upozornění na Java 17+ - 2.8.0 (říjen 2024) - testování postkvantové kryptografie - 2.6.0 (květen 2024) - blokování I2P-over-Tor - 2.4.0 (prosinec 2023) - vylepšení zabezpečení NetDB - 2.2.0 (březen 2023) - řízení přetížení - 2.1.0 (leden 2023) - vylepšení sítě - 2.0.0 (listopad 2022) - transportní protokol SSU2 - 1.7.0/0.9.53 (únor 2022) - ShellService, nahrazování proměnných - 0.9.15 (září 2014) - zaveden formát SU3

**Číslování verzí:** - řada 0.9.x: do verze 0.9.53 včetně - řada 2.x: od verze 2.0.0 (zavedení SSU2)

### Zdroje pro vývojáře

**Zdrojový kód:** - Hlavní repozitář: https://i2pgit.org/I2P_Developers/i2p.i2p - Zrcadlo na GitHubu: https://github.com/i2p/i2p.i2p

**Příklady pluginů:** - zzzot (BitTorrent tracker) - pebble (blogová platforma) - i2p-bote (bezserverový e-mail) - orchid (klient Tor) - seedless (výměna peerů)

**Nástroje pro sestavení:** - makeplugin.sh - Generování a podepisování klíčů - Nachází se v repozitáři i2p.scripts - Automatizuje vytváření a ověřování su3

### Podpora komunity

**Fóra:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (pouze uvnitř I2P)

**IRC/Chat:** - #i2p-dev na OFTC - I2P IRC v rámci sítě

---

## Příloha A: Kompletní příklad plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Příloha B: Úplný příklad souboru clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Příloha C: Úplný příklad webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Příloha D: Kontrolní seznam migrace (z 0.9.53 na 2.10.0)

### Požadované změny

- [ ] **Odstranit kompresi Pack200 (formát komprese JAR v Javě) z procesu sestavení**
  - Odstranit úlohy pack200 ze skriptů Ant/Maven/Gradle
  - Znovu vydat stávající zásuvné moduly bez pack200

- [ ] **Zkontrolovat požadavky na verzi Javy**
  - Zvážit vyžadování Javy 11+ pro nové funkce
  - Naplánovat požadavek na Javu 17+ v I2P 2.11.0
  - Aktualizovat `min-java-version` v plugin.config

- [ ] **Aktualizovat dokumentaci**
  - Odstranit zmínky o Pack200
  - Aktualizovat požadavky na verzi Javy
  - Aktualizovat zmínky o verzích I2P (0.9.x → 2.x)

### Doporučené změny

- [ ] **Posilte kryptografické podpisy**
  - Přejděte z XPI2P na SU3, pokud jste tak dosud neučinili
  - Používejte klíče RSA-4096 pro nové zásuvné moduly

- [ ] **Využijte nové funkce (pokud používáte 0.9.53+)**
  - Použijte proměnné `$OS` / `$ARCH` pro aktualizace specifické pro platformu
  - Použijte ShellService (služba shellu) pro externí programy
  - Použijte vylepšený classpath webové aplikace (funguje pro libovolný název WAR)

- [ ] **Otestovat kompatibilitu**
  - Otestovat na I2P 2.10.0
  - Ověřit s Javou 8, 11, 17
  - Zkontrolovat na Windows, Linuxu, macOS

### Volitelná vylepšení

- [ ] Správně implementovat ServletContextListener
- [ ] Přidat lokalizované popisy
- [ ] Dodat ikonu konzole
- [ ] Zlepšit obsluhu ukončování
- [ ] Přidat komplexní logování
- [ ] Napsat automatizované testy
