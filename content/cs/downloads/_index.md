---
title: "Stáhnout I2P"
description: "Stáhněte si nejnovější verzi I2P pro Windows, macOS, Linux, Android a další"
type: "stažení"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: Přeložte následující text z angličtiny do češtiny.

Dodržujte všechna pravidla formátování a technických termínů ze systémové zprávy.

Text k překladu:
windows: ```
## Instalace a konfigurace I2P

I2P je anonymní overlay síť, která umožňuje aplikacím bezpečně a anonymně komunikovat. Tento dokument vás provede procesem instalace a základní konfigurace I2P routeru.

### Požadavky

- Java 8 nebo novější
- 256 MB RAM
- 100 MB volného místa na disku

### Instalace

1. Stáhněte si nejnovější verzi I2P z [oficiálních stránek](https://geti2p.net).
2. Spusťte instalační soubor a postupujte podle pokynů na obrazovce.
3. Po dokončení instalace spusťte I2P router.

### Konfigurace

Po spuštění I2P routeru otevřete webový prohlížeč a přejděte na `http://127.0.0.1:7657`. Toto je konzole routeru, kde můžete spravovat nastavení a sledovat stav sítě.

#### Nastavení tunelů

Pro konfiguraci tunelů přejděte do sekce "I2PTunnel" v konzoli routeru. Zde můžete vytvářet a spravovat různé typy tunelů pro vaše aplikace.

#### Správa klíčů

I2P používá garlic encryption pro zabezpečení komunikace. Klíče můžete spravovat v sekci "Správa klíčů" v konzoli routeru.

### Další kroky

- Prozkoumejte [dokumentaci I2P](https://geti2p.net/docs) pro pokročilé konfigurace.
- Připojte se ke komunitě I2P na [fórech](https://geti2p.net/forums) pro podporu a diskusi.

```
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "Vyžadována Java"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: Při použití I2P je důležité pochopit, jak fungují různé komponenty, jako je router a tunel. Router je zodpovědný za směrování dat skrze síť, zatímco tunely slouží k přenosu šifrovaných zpráv mezi uživateli. Každý uživatel má svůj vlastní leaseSet, který obsahuje informace potřebné pro komunikaci. NetDb (databáze sítě) ukládá informace o dostupných routerech a jejich schopnostech. Floodfill routery hrají klíčovou roli při distribuci těchto informací v síti.

Pro zabezpečení komunikace I2P používá garlic encryption, což je technika, která umožňuje balení více zpráv do jedné šifrované kapsle. To zvyšuje anonymitu a efektivitu přenosu dat. NTCP2 a SSU jsou dva hlavní transportní protokoly, které I2P používá pro přenos dat mezi routery.

Pokud chcete hostovat vlastní eepsite (webová stránka v síti I2P), můžete použít I2PTunnel, který umožňuje přesměrování provozu z vaší lokální sítě do I2P. Pro vývojáře je k dispozici SAMv3 API, které poskytuje rozhraní pro interakci s I2P sítí.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: Při používání I2P je důležité pochopit, jak fungují routery a tunely. Routery v I2P síti fungují jako přenosové uzly, které směrují šifrované zprávy mezi uživateli. Každý uživatel má svůj vlastní router, který je zodpovědný za vytváření a údržbu tunelů. Tunely jsou jednosměrné cesty, které se skládají z několika routerů, a umožňují bezpečný přenos dat.

LeaseSet je struktura dat, která obsahuje informace o tunelu a je uložena v netDb (databáze sítě). Floodfill routery jsou speciální routery, které pomáhají distribuovat a ukládat LeaseSety v síti. Pro komunikaci mezi routery se používají protokoly NTCP2 a SSU, které zajišťují bezpečný přenos dat.

Pokud chcete hostovat vlastní eepsite (webová stránka v I2P), můžete použít I2PTunnel, který umožňuje přesměrování provozu z vašeho routeru na veřejný internet. Pro vývojáře je k dispozici SAMv3 API, které poskytuje rozhraní pro interakci s I2P sítí.

Garlic encryption (česnekové šifrování) je technika, která zajišťuje, že více zpráv může být šifrováno a odesláno jako jeden celek, což zvyšuje bezpečnost a efektivitu přenosu.
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "Není potřeba Java - obsahuje Java runtime"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: pravda
links: # Instalace I2P

I2P je anonymní overlay síť, která umožňuje aplikacím bezpečně a anonymně komunikovat. Tato příručka vám pomůže s instalací a konfigurací I2P na vašem systému.

## Požadavky

- Java 8 nebo novější
- 256 MB RAM
- 100 MB volného místa na disku

## Instalace

1. Stáhněte si nejnovější verzi I2P z [oficiálního webu](https://geti2p.net).
2. Spusťte instalační balíček a postupujte podle pokynů na obrazovce.
3. Po dokončení instalace spusťte I2P router pomocí příkazu `i2prouter start`.

## Konfigurace

Po spuštění I2P routeru otevřete webový prohlížeč a přejděte na `http://127.0.0.1:7657`. Tím se dostanete na konzoli routeru, kde můžete spravovat nastavení a sledovat aktivitu sítě.

### Nastavení tunelů

Pro vytvoření tunelu přejděte do sekce **I2PTunnel** a klikněte na **Create**. Vyberte typ tunelu a zadejte potřebné parametry.

### Správa leaseSet

LeaseSet je struktura, která obsahuje informace o tom, jak se připojit k určitému cíli v síti I2P. Spravujte své leaseSety v sekci **netDb**.

## Další zdroje

- [Oficiální dokumentace](https://geti2p.net/en/docs)
- [Fórum komunity](https://geti2p.net/en/forums)

Pokud máte jakékoli dotazy nebo potřebujete pomoc, neváhejte se obrátit na komunitu prostřednictvím fóra nebo IRC kanálu.
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: Poskytněte POUZE překlad, nic jiného:
file: "i2pinstall_2.10.0.jar"
size: "~30M"
requirements: "Java 8 nebo vyšší"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: Poskytujte POUZE překlad, nic jiného:
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: Poskytujte POUZE překlad, nic jiného:
file: "i2psource_2.10.0.tar.bz2"
size: "~33M"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: Poskytujte POUZE překlad, nic jiného:
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: ```
# Instalace I2P

I2P je anonymní overlay síť, která umožňuje aplikacím bezpečně a anonymně posílat zprávy mezi sebou. Je navržena tak, aby chránila uživatele před sledováním a cenzurou.

## Požadavky

- Java 8 nebo novější
- 256 MB RAM
- 100 MB volného místa na disku

## Kroky instalace

1. Stáhněte si instalační balíček z [oficiálních stránek I2P](https://geti2p.net).
2. Spusťte instalační program a postupujte podle pokynů na obrazovce.
3. Po dokončení instalace spusťte I2P router.

## Konfigurace

Po spuštění I2P routeru otevřete webový prohlížeč a přejděte na `http://127.0.0.1:7657`. Tato stránka je známá jako "Router Console" a umožňuje vám spravovat nastavení I2P.

### Nastavení tunelů

Pro vytvoření tunelu přejděte do sekce "I2PTunnel" v Router Console. Zde můžete konfigurovat různé typy tunelů podle vašich potřeb.

## Řešení problémů

Pokud narazíte na problémy, zkontrolujte logy v adresáři `logs/`. Můžete také navštívit [I2P fórum](https://forum.i2p) pro pomoc od komunity.

```
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+, minimálně 512 MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: Překlad textu:

# Instalace I2P na Linuxu

I2P je anonymní overlay síť, která umožňuje aplikacím bezpečně a anonymně komunikovat. Tato příručka vás provede procesem instalace I2P na Linuxu.

## Požadavky

- Java 8 nebo novější
- 256 MB RAM
- 100 MB volného místa na disku

## Instalace

1. Stáhněte si nejnovější verzi I2P z [oficiálních stránek](https://geti2p.net).
2. Otevřete terminál a přejděte do adresáře, kam jste stáhli instalační soubor.
3. Spusťte následující příkaz pro instalaci:

   ```bash
   sudo dpkg -i i2pinstall_1.9.0-1_all.deb
   ```

4. Po dokončení instalace spusťte I2P router pomocí příkazu:

   ```bash
   i2prouter start
   ```

5. Otevřete webový prohlížeč a přejděte na `http://127.0.0.1:7657` pro přístup k I2P router konzoli.

## Konfigurace

Po instalaci můžete konfigurovat I2P podle svých potřeb. Doporučujeme začít s nastavením tunelů a kontrolou `netDb` pro optimalizaci výkonu.

## Další kroky

- Prozkoumejte dostupné pluginy a rozšíření pro rozšíření funkcionality I2P.
- Připojte se ke komunitě I2P a zůstaňte informováni o nejnovějších aktualizacích a bezpečnostních doporučeních.

Tato příručka by vám měla pomoci začít s I2P na vašem Linuxovém systému. Pro podrobnější informace navštivte [dokumentaci I2P](https://geti2p.net/en/docs).
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: Překlad:

# Úvod do I2P

I2P (The Invisible Internet Project) je anonymní overlay síť, která umožňuje aplikacím bezpečně a soukromě komunikovat. Je navržena tak, aby chránila uživatele před sledováním a cenzurou. I2P poskytuje několik klíčových funkcí, včetně směrování zpráv přes decentralizovanou síť, šifrování koncových bodů a anonymní hosting služeb známých jako eepsites.

## Jak I2P funguje

I2P používá směrování na bázi tunelů, kde data procházejí přes několik routerů, než dosáhnou cíle. Každý router v síti má svůj vlastní leaseSet, který obsahuje informace potřebné pro směrování zpráv. Síťová databáze (netDb) uchovává tyto leaseSety a umožňuje routerům najít cestu k cílovým službám.

### Klíčové komponenty

- **Router**: Zařízení nebo software, který směruje data přes síť I2P.
- **Tunnel**: Virtuální cesta, kterou data procházejí, aby dosáhla svého cíle.
- **LeaseSet**: Datová struktura obsahující informace o dostupnosti a směrování služeb.
- **Floodfill**: Speciální routery, které pomáhají distribuovat a ukládat informace v netDb.

## Bezpečnostní funkce

I2P používá garlic encryption, což je technika, která umožňuje balení více zpráv do jednoho šifrovaného balíku. To zvyšuje bezpečnost a anonymitu uživatelů. Pro připojení k síti I2P se používají protokoly NTCP2 a SSU, které poskytují šifrované a autentizované spojení mezi routery.

## Použití I2P

I2P podporuje různé aplikace, včetně webových prohlížečů, e-mailových klientů a peer-to-peer sítí. Uživatelé mohou hostovat své vlastní eepsites nebo přistupovat k jiným službám v síti. I2P také nabízí rozhraní jako SAMv3 a I2CP pro vývojáře, kteří chtějí integrovat anonymní komunikaci do svých aplikací.

Pro více informací navštivte [oficiální dokumentaci I2P](https://geti2p.net).
primary: Poskytujte POUZE překlad, nic jiného:
name: "StormyCloud"
location: "Spojené státy"
url: "https://stormycloud.org"
resources: I2P je anonymní overlay síť, která umožňuje aplikacím bezpečně a anonymně komunikovat. Je navržena tak, aby chránila uživatele před sledováním a cenzurou. I2P poskytuje různé služby, včetně anonymního prohlížení webu, e-mailu, chatování a hostování webových stránek (eepsites).

## Jak I2P funguje

I2P používá směrování na základě tunelů, kde data jsou šifrována a přenášena přes několik routerů. Každý uživatel I2P provozuje router, který se připojuje k ostatním routerům v síti. Data jsou rozdělena do menších částí a odesílána přes různé tunely, což ztěžuje sledování zdroje a cíle komunikace.

### Klíčové komponenty I2P

- **Router**: Základní prvek sítě, který přenáší data mezi uživateli.
- **Tunnel**: Šifrovaná cesta, kterou data procházejí.
- **LeaseSet**: Informace o dostupnosti tunelů pro příjem dat.
- **netDb**: Distribuovaná databáze, která uchovává informace o routerech a tunelových konfiguracích.
- **Floodfill**: Speciální routery, které pomáhají distribuovat informace v síti.

### Protokoly a šifrování

I2P používá různé protokoly pro zajištění bezpečnosti a anonymity. NTCP2 a SSU jsou hlavní transportní protokoly, které umožňují šifrovanou komunikaci mezi routery. Garlic encryption je technika, která zvyšuje anonymitu tím, že kombinuje více zpráv do jedné šifrované jednotky.

## Použití I2P

I2P může být použit pro různé účely, včetně:

- **Anonymní prohlížení**: Přístup k eepsites, které jsou hostovány uvnitř I2P sítě.
- **E-mail**: Bezpečná a anonymní e-mailová komunikace.
- **Chatování**: Soukromé a šifrované chatovací služby.
- **Hostování webových stránek**: Vytváření a správa eepsites bez odhalení vaší identity.

Pro více informací navštivte [oficiální dokumentaci I2P](https://geti2p.net).
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
