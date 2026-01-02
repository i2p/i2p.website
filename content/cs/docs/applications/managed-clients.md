---
title: "Spravovaní klienti"
description: "Jak aplikace spravované routerem integrují s ClientAppManager a mapovačem portů"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Přehled

Záznamy v [`clients.config`](/docs/specs/configuration/#clients-config) říkají routeru, které aplikace spustit při startu. Každý záznam může běžet jako **managed** klient (preferováno) nebo jako **unmanaged** klient. Managed klienti spolupracují s `ClientAppManager`, který:

- Vytváří instanci aplikace a sleduje stav životního cyklu pro router console
- Zpřístupňuje uživateli ovládací prvky start/stop a vynucuje čisté ukončení při vypnutí routeru
- Hostuje odlehčený **client registry** a **port mapper**, aby aplikace mohly objevovat vzájemné služby

Nespravované klienty jednoduše vyvolávají metodu `main()`; používejte je pouze pro starší kód, který nelze modernizovat.

## 2. Implementace Managed Client

Managed klienti musí implementovat buď `net.i2p.app.ClientApp` (pro aplikace určené uživatelům) nebo `net.i2p.router.app.RouterApp` (pro rozšíření routeru). Poskytněte jeden z níže uvedených konstruktorů, aby mohl manager dodat kontext a konfigurační argumenty:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
Pole `args` obsahuje hodnoty nakonfigurované v `clients.config` nebo v jednotlivých souborech v `clients.config.d/`. Pokud je to možné, rozšiřte pomocné třídy `ClientApp` / `RouterApp`, abyste zdědili výchozí propojení životního cyklu.

### 2.1 Lifecycle Methods

Očekává se, že spravovaní klienti implementují:

- `startup()` - provede inicializaci a okamžitě se vrátí. Musí alespoň jednou zavolat `manager.notify()` pro přechod ze stavu INITIALIZED.
- `shutdown(String[] args)` - uvolní zdroje a zastaví vlákna na pozadí. Musí alespoň jednou zavolat `manager.notify()` pro změnu stavu na STOPPING nebo STOPPED.
- `getState()` - informuje konzoli, zda aplikace běží, spouští se, zastavuje se nebo selhala

Manažer volá tyto metody, když uživatelé interagují s konzolí.

### 2.2 Advantages

- Přesné hlášení stavu v konzoli routeru
- Čisté restarty bez úniku vláken nebo statických odkazů
- Nižší paměťová náročnost po zastavení aplikace
- Centralizované logování a hlášení chyb prostřednictvím injektovaného kontextu

## 3. Unmanaged Clients (Fallback Mode)

Pokud nakonfigurovaná třída neimplementuje managed interface, router ji spustí vyvoláním `main(String[] args)` a nemůže sledovat výsledný proces. Konzole zobrazuje omezené informace a shutdown hooks se nemusí spustit. Tento režim vyhraďte pro skripty nebo jednorázové utility, které nemohou přijmout managed API.

## 4. Client Registry

Managed i unmanaged klienti se mohou registrovat u manageru, aby ostatní komponenty mohly získat referenci podle jména:

```java
manager.register(this);
```
Registrace používá návratovou hodnotu `getName()` klienta jako klíč registru. Známé registrace zahrnují `console`, `i2ptunnel`, `Jetty`, `outproxy` a `update`. K získání klienta použijte `ClientAppManager.getRegisteredApp(String name)` pro koordinaci funkcí (například konzole dotazující se Jetty na detaily stavu).

Poznámka: registr klientů a mapovač portů jsou oddělené systémy. Registr klientů umožňuje meziapolikační komunikaci pomocí vyhledávání podle jména, zatímco mapovač portů mapuje názvy služeb na kombinace host:port pro objevování služeb.

## 3. Nespravovaní klienti (režim návratu)

Mapovač portů nabízí jednoduchý adresář pro interní TCP služby. Registrujte loopback porty, aby spolupracovníci nemuseli používat natvrdo zakódované adresy:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Nebo s explicitním zadáním hostitele:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Vyhledávejte služby pomocí `PortMapper.getPort(String name)` (vrací -1, pokud není nalezena) nebo `getPort(String name, int defaultPort)` (vrací výchozí hodnotu, pokud není nalezena). Zkontrolujte stav registrace pomocí `isRegistered(String name)` a získejte registrovaný host pomocí `getActualHost(String name)`.

Běžné konstanty služby mapování portů z `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Konzole routeru (výchozí port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (výchozí port 4444)
- `SVC_HTTPS_PROXY` - HTTPS proxy (výchozí port 4445)
- `SVC_I2PTUNNEL` - Správce I2PTunnel
- `SVC_SAM` - SAM bridge (výchozí port 7656)
- `SVC_SAM_SSL` - SAM bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB bridge (výchozí port 2827)
- `SVC_EEPSITE` - Standardní eepsite (výchozí port 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tunnel (výchozí port 6668)
- `SVC_SUSIDNS` - SusiDNS

Poznámka: `httpclient`, `httpsclient` a `httpbidirclient` jsou typy tunelů i2ptunnel (používané v konfiguraci `tunnel.N.type`), nikoli konstanty služby pro mapování portů.

## 4. Registr klientů

### 2.1 Metody životního cyklu

Od verze 0.9.42 router podporuje rozdělení konfigurace do samostatných souborů v adresáři `clients.config.d/`. Každý soubor obsahuje vlastnosti pro jednoho klienta, přičemž všechny vlastnosti mají předponu `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Toto je doporučený přístup pro nové instalace a pluginy.

### 2.2 Výhody

Z důvodu zpětné kompatibility používá tradiční formát sekvenční číslování:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Povinné:** - `main` - Úplný název třídy implementující ClientApp nebo RouterApp, nebo obsahující statickou metodu `main(String[] args)`

**Volitelné:** - `name` - Zobrazované jméno pro router console (výchozí je název třídy) - `args` - Argumenty oddělené mezerami nebo tabulátory (podporuje řetězce v uvozovkách) - `delay` - Sekundy před spuštěním (výchozí 120) - `onBoot` - Vynutí `delay=0`, pokud je true - `startOnLoad` - Povoluje/zakazuje klienta (výchozí true)

**Specifické pro plugin:** - `stopargs` - Argumenty předané během vypnutí - `uninstallargs` - Argumenty předané během odinstalace pluginu - `classpath` - Čárkou oddělené dodatečné položky classpath

**Substituce proměnných pro pluginy:** - `$I2P` - Základní adresář I2P - `$CONFIG` - Adresář s konfigurací uživatele (např. ~/.i2p) - `$PLUGIN` - Adresář pluginu - `$OS` - Název operačního systému - `$ARCH` - Název architektury

## 5. Port Mapper

- Preferujte spravované klienty; vraťte se k nespravovaným pouze v případě absolutní nutnosti.
- Udržujte inicializaci a vypínání nenáročné, aby operace konzole zůstaly responzivní.
- Používejte popisné názvy registrů a portů, aby diagnostické nástroje (a koncoví uživatelé) pochopili, co služba dělá.
- Vyhýbejte se statickým singletonům - spoléhejte na vložený kontext a manager pro sdílení zdrojů.
- Volajte `manager.notify()` při všech změnách stavu pro udržení přesného stavu konzole.
- Pokud musíte běžet v samostatném JVM, zdokumentujte, jak se logy a diagnostika zobrazují v hlavní konzoli.
- Pro externí programy zvažte použití ShellService (přidáno ve verzi 1.7.0) pro získání výhod spravovaného klienta.

## 6. Formát konfigurace

Managed clients byly představeny ve **verzi 0.9.4** (17. prosince 2012) a zůstávají doporučenou architekturou k **verzi 2.10.0** (9. září 2025). Základní API zůstala stabilní s nulou breaking changes během tohoto období:

- Signatury konstruktorů nezměněny
- Metody životního cyklu (startup, shutdown, getState) nezměněny
- Registrační metody ClientAppManager nezměněny
- Registrační a vyhledávací metody PortMapper nezměněny

Významná vylepšení: - **0.9.42 (2019)** - adresářová struktura clients.config.d/ pro jednotlivé konfigurační soubory - **1.7.0 (2021)** - přidána ShellService pro sledování stavu externích programů - **2.10.0 (2025)** - aktuální vydání bez změn v API spravovaných klientů

Další hlavní vydání bude vyžadovat minimálně Java 17+ (požadavek na infrastrukturu, nikoli změna API).

## References

- [Specifikace clients.config](/docs/specs/configuration/#clients-config)
- [Specifikace konfiguračního souboru](/docs/specs/configuration/)
- [Index technické dokumentace I2P](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [Rozhraní ClientApp](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [Rozhraní RouterApp](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Alternativní Javadoc (stabilní)](https://docs.i2p-projekt.de/javadoc/)
- [Alternativní Javadoc (clearnet mirror)](https://eyedeekay.github.io/javadoc-i2p/)

> **Poznámka:** Síť I2P hostuje komplexní dokumentaci na adrese http://idk.i2p/javadoc-i2p/, která vyžaduje pro přístup I2P router. Pro přístup z běžného internetu použijte výše uvedené zrcadlo na GitHub Pages.
