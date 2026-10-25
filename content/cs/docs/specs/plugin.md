---
title: "Specifikace pluginů"
description: ".xpi2p / .su3 pravidla balení pro I2P pluginy"
slug: "plugin"
aliases:
  - "/cs/plugin_spec"
  - "/cs/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Přehled

Tento dokument specifikuje formát souboru .xpi2p (podobně jako Firefox .xpi), ale s jednoduchým popisným souborem plugin.config namísto XML souboru install.rdf. Tento formát souborů se používá jak pro počáteční instalace pluginů, tak pro aktualizace pluginů.

Navíc tento dokument poskytuje stručný přehled o tom, jak router instaluje pluginy, a zásady a směrnice pro vývojáře pluginů.

Základní formát souboru .xpi2p je stejný jako soubor i2pupdate.sud (formát používaný pro aktualizace routeru), ale instalátor umožní uživateli nainstalovat addon i v případě, že ještě nezná klíč podepisovatele.

Od vydání 0.9.15 je podporován formát souboru SU3 a je preferován. Tento formát umožňuje silnější podpisové klíče.

> **Poznámka:** Nedoporučujeme již distribuovat pluginy ve formátu xpi2p. Použijte formát su3.

Standardní adresářová struktura umožní uživatelům instalovat následující typy doplňků:

- Console webapps
- Nový eepsite s cgi-bin, webapps
- Témata konzole
- Překlady konzole
- Java programy
- Java programy v samostatné JVM
- Jakýkoli shell skript nebo program

Plugin nainstaluje všechny své soubory do `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` ve Windows). Instalátor zabrání instalaci kamkoli jinam, ačkoli plugin může při běhu přistupovat ke knihovnám jinde.

Toto by mělo být chápáno pouze jako způsob, jak usnadnit instalaci, odinstalaci a aktualizaci a jak omezit základní konflikty mezi pluginy.

Jakmile je však plugin spuštěn, v podstatě neexistuje žádný bezpečnostní model. Plugin běží ve stejném JVM a se stejnými oprávněními jako router a má plný přístup k souborovému systému, routeru, spouštění externích programů atd.

## Detaily

foo.xpi2p je soubor podepsané aktualizace (sud) obsahující následující:

Standardní .sud hlavička připojená na začátek zip souboru, obsahující následující:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Zip soubor obsahující následující:

### soubor plugin.config

Tento soubor je povinný. Je to standardní konfigurační soubor I2P obsahující následující vlastnosti:

#### Požadované vlastnosti

Následující čtyři vlastnosti jsou povinné. První tři musí být identické s těmi v nainstalovaném pluginu pro aktualizační plugin.

-   **name** - Bude nainstalován pod tímto názvem adresáře. Pro nativní pluginy můžete chtít samostatné názvy v různých balíčcích - například foo-windows a foo-linux.
-   **key** - Veřejný DSA klíč jako 172 B64 znaků končících na '='. Vynechejte pro SU3 formát.
-   **signer** - doporučuje se yourname@mail.i2p
-   **version** - Musí být ve formátu, který dokáže parsovat VersionComparator, např. 1.2.3-4. Maximálně 16 bytů (musí odpovídat sud verzi). Platné oddělovače čísel jsou '.', '-' a '_'. Toto musí být vyšší než verze v nainstalovaném pluginu pro aktualizační plugin.

#### Vlastnosti zobrazení

Hodnoty následujících vlastností jsou zobrazeny v /configplugins v konzole routeru, pokud jsou přítomny:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` doporučeno
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Kontrola aktualizací zkontroluje bajty 41-56 na této URL pro zjištění, zda je dostupná novější verze. Od verze 1.7.0 (0.9.53) je možné použít proměnné `$OS` a `$ARCH` v URL. Nedoporučuje se. Nepoužívejte, pokud jste předtím nedistribuovali pluginy ve formátu xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - Umístění aktualizačního souboru ve formátu su3, od verze 0.9.15. Od verze 1.7.0 (0.9.53) je možné použít proměnné `$OS` a `$ARCH` v URL.
-   **description** - v angličtině
-   **description_xx** - pro jazyk xx
-   **license** - Licence pluginu
-   **disableStop=true** - Výchozí hodnota false. Pokud je true, tlačítko stop se nezobrazí. Použijte, pokud nejsou žádné webové aplikace a žádní klienti se stopargs.

#### Vlastnosti odkazů v souhrnném panelu konzole

Následující vlastnosti se používají pro přidání odkazu na souhrnný panel konzole:

-   **consoleLinkName** - bude přidán do souhrnného panelu
-   **consoleLinkName_xx** - pro jazyk xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - podporováno od verze 0.7.12-6
-   **consoleLinkTooltip_xx** - jazyk xx od verze 0.7.12-6

#### Vlastnosti ikony konzole

Následující volitelné vlastnosti lze použít k přidání vlastní ikony do konzole:

-   **console-icon** - podporováno od verze 0.9.20. Pouze pro webapps. Cesta k 32x32 obrázku, např. /icon.png. Od verze 1.7.0 (API 0.9.53), pokud je zadáno consoleLinkURL, je cesta relativní k této URL. Jinak je relativní k názvu webapps. Platí pro všechny webapps v pluginu.
-   **icon-code** - podporováno od verze 0.9.25. Poskytuje ikonu konzole pro pluginy bez webových zdrojů. B64 řetězec vytvořený voláním `net.i2p.data.Base64 encode FILE` na soubor png obrázku 32x32.

#### Vlastnosti instalátoru

Následující vlastnosti jsou používány instalátorem pluginů:

-   **type** - app/theme/locale/webapp/... (neimplementováno, pravděpodobně není nutné)
-   **min-i2p-version** - Minimální verze I2P, kterou tento plugin vyžaduje
-   **max-i2p-version** - Maximální verze I2P, na které bude tento plugin fungovat
-   **min-java-version** - Minimální verze Java, kterou tento plugin vyžaduje
-   **min-jetty-version** - podporováno od verze 0.8.13, použijte 6 pro Jetty 6 webapps
-   **max-jetty-version** - podporováno od verze 0.8.13, použijte 5.99999 pro Jetty 5 webapps
-   **required-platform-OS** - neimplementováno - možná bude pouze zobrazeno, ne ověřeno
-   **other-requirements** - neimplementováno, např. python x.y - není ověřováno instalátorem, pouze zobrazeno uživateli
-   **dont-start-at-install=true** - Výchozí false. Nespustí plugin při instalaci nebo aktualizaci.
-   **router-restart-required=true** - Výchozí false. Nerestartuje router nebo plugin při aktualizaci, pouze informuje uživatele, že je restart vyžadován.
-   **update-only=true** - Výchozí false. Pokud true, selže pokud instalace neexistuje.
-   **install-only=true** - Výchozí false. Pokud true, selže pokud instalace existuje.
-   **min-installed-version** - pro aktualizaci, pokud instalace existuje
-   **max-installed-version** - pro aktualizaci, pokud instalace existuje
-   **depends=plugin1,plugin2,plugin3** - neimplementováno
-   **depends-version=0.3.4,,5.6.7** - neimplementováno

#### Vlastnosti překladu

-   **langs=xx,yy,Klingon,...** - (neimplementováno) (yy je vlajka země)

### Adresáře a soubory aplikace

Každý z následujících adresářů nebo souborů je volitelný, ale něco tam musí být, jinak to nebude nic dělat:

**console/**

-   **locale/** - Pouze jar soubory obsahující nové resource bundle (překlady) pro aplikace v základní instalaci I2P. Bundle pro tento plugin by měly být umístěny v console/webapp/foo.war nebo lib/foo.jar
-   **themes/** - Nové témata pro router console. Umístěte každé téma do podsložky.
-   **webapps/** - (Viz důležité poznámky níže o webapps) .war soubory - Tyto budou spuštěny během instalace, pokud nejsou zakázány v webapps.config. Název war souboru nemusí být stejný jako název pluginu. Neduplikujte názvy war souborů ze základní instalace I2P.
-   **webapps.config** - Stejný formát jako webapps.config routeru. Používá se také k specifikaci dalších jar souborů v $PLUGIN/lib/ nebo $I2P/lib pro classpath webové aplikace, pomocí `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Poznámka:** Před vydáním 1.7.0 (API 0.9.53) byla řádka classpath načtena pouze pokud warname bylo stejné jako název pluginu. Od API 0.9.53 bude nastavení classpath fungovat pro jakékoliv warname.

> **Poznámka:** Před verzí routeru 0.7.12-9 router hledal `plugin.warname.startOnLoad` místo `webapps.warname.startOnLoad`. Pro kompatibilitu se staršími verzemi routeru by plugin, který chce zakázat war, měl obsahovat oba řádky.

**eepsite/**

(Viz důležité poznámky níže o eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - Instalátor bude muset provést substituci proměnných pro nastavení cesty. Umístění a název tohoto souboru ve skutečnosti nezáleží, pokud je nastaven v clients.config - může být vhodnější umístit ho o úroveň výše.

**lib/**

Umístěte zde všechny jar soubory a specifikujte je v řádku classpath v console/webapps.config a/nebo clients.config

### soubor clients.config

Tento soubor je volitelný a specifikuje klienty, kteří budou spuštěni při spuštění pluginu. Používá stejný formát jako soubor clients.config routeru. Viz specifikace konfiguračního souboru clients.config pro více informací o formátu a důležitých detailech o tom, jak jsou klienti spouštěni a zastavováni.

-   **clientApp.0.stopargs=foo bar stop baz** - Pokud je přítomno, třída bude zavolána s těmito argumenty pro zastavení klienta. Všechny úlohy zastavení jsou volány s nulovým zpožděním. Poznámka: Router nemůže určit, zda vaši nespravovaní klienti běží nebo ne.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Pokud je přítomno, třída bude zavolána s těmito argumenty těsně před smazáním $PLUGIN. Všechny úlohy odinstalace jsou volány s nulovým zpožděním.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Spouštěč pluginu provede náhradu proměnných v řádcích args a stopargs následovně:
    -   `$I2P` - základní instalační adresář I2P
    -   `$CONFIG` - konfigurační adresář I2P (typicky ~/.i2p)
    -   `$PLUGIN` - instalační adresář tohoto pluginu (typicky ~/.i2p/plugins/appname)
    -   `$OS` - hostitelský operační systém ve formě `windows`, `linux`, `mac`
    -   `$ARCH` - hostitelská architektura ve formě `386`, `amd64`, `arm64`

(Viz důležité poznámky níže o spouštění shell skriptů nebo externích programů)

## Úlohy instalátoru pluginů

Toto uvádí, co se stane, když je plugin nainstalován systémem I2P.

1.  Soubor .xpi2p je stažen.
2.  Podpis .sud je ověřen proti uloženým klíčům. Od verze 0.9.14.1, pokud neexistuje odpovídající klíč, instalace selže, pokud není nastavena pokročilá vlastnost routeru, která umožňuje všechny klíče.
3.  Ověří se integrita zip souboru.
4.  Extrahuje se soubor plugin.config.
5.  Ověří se verze I2P, aby se ujistilo, že plugin bude fungovat.
6.  Zkontroluje se, že webapps neduplikují existující aplikace $I2P.
7.  Zastaví se existující plugin (pokud je přítomen).
8.  Ověří se, že instalační adresář ještě neexistuje, pokud update=false, nebo se zeptá na přepsání.
9.  Ověří se, že instalační adresář existuje, pokud update=true, nebo se zeptá na vytvoření.
10. Plugin se rozbalí do appDir/plugins/name/
11. Plugin se přidá do plugins.config

## Úlohy pro spuštění pluginu

Toto uvádí, co se stane při spuštění pluginů. Nejprve se zkontroluje plugins.config, aby se zjistilo, které pluginy je třeba spustit. Pro každý plugin:

1.  Zkontrolovat clients.config a načíst a spustit každou položku (přidat nakonfigurované jar soubory do classpath).
2.  Zkontrolovat console/webapp a console/webapp.config. Načíst a spustit požadované položky (přidat nakonfigurované jar soubory do classpath).
3.  Přidat console/locale/foo.jar do translation classpath, pokud je přítomen.
4.  Přidat console/theme do vyhledávací cesty pro témata, pokud je přítomen.
5.  Přidat odkaz na souhrnný panel.

## Poznámky ke konzolové webové aplikaci

Konzolové webové aplikace s úlohami na pozadí by měly implementovat ServletContextListener (viz seedless nebo i2pbote jako příklady), nebo přepsat destroy() v servletu, aby mohly být zastaveny. Od verze routeru 0.7.12-3 budou konzolové webové aplikace vždy zastaveny před jejich restartováním, takže se nemusíte starat o více instancí, pokud toto uděláte. Také od verze routeru 0.7.12-3 budou konzolové webové aplikace zastaveny při vypnutí routeru.

Nezahrnujte knihovní jar soubory do webové aplikace; umístěte je do lib/ a vložte classpath do webapps.config. Poté můžete vytvořit samostatné pluginy pro instalaci a aktualizaci, kde plugin pro aktualizaci neobsahuje knihovní jar soubory.

Nikdy nezahrnujte Jetty, Tomcat nebo servlet jar soubory do vašeho pluginu, protože mohou být v konfliktu s verzí v instalaci I2P. Dávejte pozor, abyste nezahrnovali žádné konfliktní knihovny.

Nezahrnujte soubory .java nebo .jsp; jinak je Jetty při instalaci znovu zkompiluje, což zvýší čas spuštění. Ačkoli většina instalací I2P bude mít v classpath funkční Java a JSP kompilátor, toto není zaručeno a nemusí to fungovat ve všech případech.

Prozatím musí mít webapp, která potřebuje přidat soubory classpath v $PLUGIN, stejný název jako plugin. Například webapp v pluginu foo musí být pojmenována foo.war.

Ačkoli I2P podporuje Servlet 3.0 od verze 0.9.30, NEPODPORUJE skenování anotací pro @WebContent (bez souboru web.xml). Bylo by potřeba několik dalších runtime jar souborů, které neposkytujeme ve standardní instalaci. Pokud potřebujete podporu pro @WebContent, kontaktujte vývojáře I2P.

## Poznámky k eepsite

Není jasné, jak nainstalovat plugin do existujícího eepsite. Router nemá návaznost na eepsite a ten může nebo nemusí běžet, a může jich být více než jeden. Lepší je spustit vlastní instanci Jetty a instanci I2PTunnel pro zcela nový eepsite.

Může vytvořit nový I2PTunnel (podobně jako to dělá i2ptunnel CLI), ale samozřejmě se nezobrazí v gui i2ptunnel, to je jiná instance. Ale to je v pořádku. Pak můžete spustit a zastavit i2ptunnel a jetty společně.

Takže nespoléhejte na to, že router automaticky sloučí toto s nějakým existujícím eepsite. Pravděpodobně se to nestane. Spusťte nový I2PTunnel a Jetty z clients.config. Nejlepšími příklady jsou pluginy zzzot a pebble.

Jak dostat substituci cesty do jetty.xml? Podívejte se na příklady v pluginech zzzot a pebble.

## Poznámky k spuštění/zastavení klienta

Od verze 0.9.4 router podporuje "řízené" plugin klienty. Řízení plugin klienti jsou vytvářeni a spouštěni pomocí `ClientAppManager`. ClientAppManager udržuje referenci na klienta a přijímá aktualizace o stavu klienta. Řízení plugin klienti jsou preferováni, protože je mnohem jednodušší implementovat sledování stavu a spouštět a zastavovat klienta. Je také mnohem jednodušší vyhnout se statickým referencím v kódu klienta, které by mohly vést k nadměrnému využití paměti poté, co je klient zastaven. Podívejte se na specifikaci konfiguračního souboru clients.config pro více informací o psaní řízeného klienta.

Pro "nespravované" plugin klienty nemá router žádný způsob, jak monitorovat stav klientů spuštěných prostřednictvím clients.config. Autor pluginu by měl gracefully zpracovat vícenásobné volání start nebo stop, pokud je to možné, udržováním statické tabulky stavu nebo použitím PID souborů atd. Vyhněte se logování nebo výjimkám při vícenásobných startech nebo stopech. To platí také pro volání stop bez předchozího start. Od verze routeru 0.7.12-3 budou pluginy zastaveny při vypnutí routeru, což znamená, že všichni klienti se stopargs v clients.config budou zavoláni, bez ohledu na to, zda byli dříve spuštěni nebo ne.

## Poznámky k Shell skriptům a externím programům

Pro spuštění shell skriptů nebo jiných externích programů napište malou Java třídu, která zkontroluje typ OS a poté spustí ShellCommand buď na .bat nebo .sh soubor, který poskytnete. Obecné řešení pro tento problém bylo přidáno v I2P 1.7.0/0.9.53, "ShellService", která provádí sledování stavu pro jeden příkaz a komunikuje s ClientAppManagerem.

Externí programy se nezastaví při zastavení routeru a druhá kopie se spustí při startu routeru. Toto lze obvykle zmírnit použitím ShellService pro sledování stavu. Pokud to nevyhovuje vašemu případu použití, můžete napsat wrapper třídu nebo shell skript, který provádí obvyklé uložení PID do PID souboru a kontroluje ho při startu.

## Ostatní pokyny pro pluginy

-   Podívejte se na monotone větev i2p.scripts nebo na jakýkoli z ukázkových pluginů na zzz stránce pro shell skript makeplugin.sh. Ten automatizuje většinu úkolů pro generování klíčů, vytváření su3 souborů pluginů a ověřování. Tento skript byste měli začlenit do procesu sestavení vašeho pluginu.
-   Pack200 pro jar a war soubory je pro pluginy silně doporučeno, obecně zmenšuje pluginy o 60-65%. Příklad najdete v jakémkoli z ukázkových pluginů na zzz stránce. Rozbalování Pack200 je podporováno na routerech 0.7.11-5 nebo vyšších, což jsou v podstatě všechny routery, které pluginy vůbec podporují.
-   Pluginy nesmí pokoušet zapisovat kamkoli do $I2P, protože může být pouze pro čtení, a není to tak jako tak dobrá praxe.
-   Pluginy mohou zapisovat do $CONFIG, ale doporučuje se udržovat soubory pouze v $PLUGIN. Všechny soubory v $PLUGIN budou při odinstalaci smazány.
-   $CWD může být kdekoli; nepředpokládejte, že je na konkrétním místě, nepokoušejte se číst nebo zapisovat soubory relativně k $CWD. Pro ShellService je vždy stejné jako $PLUGIN.
-   Java programy by měly zjistit, kde jsou, pomocí directory getterů v I2PAppContext.
-   Adresář pluginu je `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, nebo vložte $PLUGIN argument do řádku args v clients.config.
-   Všechny konfigurační soubory musí být v UTF-8.
-   Pro spuštění v samostatném JVM použijte ShellCommand s `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Jako alternativu k stopargs v clients.config může Java klient zaregistrovat shutdown hook s `I2PAppContext.addShutdownTask()`. Ale to by nevypnulo plugin při aktualizaci, takže stopargs je doporučeno. Také nastavte všechna vytvořená vlákna do daemon režimu.
-   Nezahrnujte třídy duplikující ty ve standardní instalaci. V případě potřeby třídy rozšiřte.
-   Pozor na různé definice classpath v wrapper.config mezi starými a novými instalacemi.
-   Klienti odmítnou duplicitní klíče s různými názvy klíčů, duplicitní názvy klíčů s různými klíči a různé klíče nebo názvy klíčů v aktualizačních balíčcích. Chraňte své klíče. Generujte je pouze jednou.
-   Nemodifikujte soubor plugin.config za běhu, protože bude přepsán při aktualizaci. Použijte jiný konfigurační soubor v adresáři pro ukládání běhové konfigurace.
-   Obecně by pluginy neměly vyžadovat přístup k $I2P/lib/router.jar. Nepřistupujte k třídám routeru, pokud neděláte něco speciálního.
-   Protože každá verze musí být vyšší než ta předchozí, mohli byste vylepšit svůj build skript tak, aby přidal číslo sestavení na konec verze.
-   Pluginy nesmí nikdy volat `System.exit()`.
-   Prosím respektujte licence splněním licenčních požadavků pro jakýkoli software, který balíte.
-   Router nastavuje JVM časové pásmo na UTC. Pokud plugin potřebuje znát skutečné časové pásmo uživatele, je uloženo routerem ve vlastnosti I2PAppContext `i2p.systemTimeZone`.

## Cesty ke třídám

Následující jar soubory v $I2P/lib lze považovat za součást standardní classpath pro všechny instalace I2P, bez ohledu na to, jak staré nebo nové je původní instalace.

Všechna nedávná veřejná API v i2p jar souborech mají v Javadocs uvedeno číslo since-release. Pokud váš plugin vyžaduje určité funkce dostupné pouze v nejnovějších verzích, nezapomeňte nastavit vlastnosti min-i2p-version, min-jetty-version, nebo obě, v souboru plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Následující jar soubory v $I2P/lib lze předpokládat jako přítomné ve všech instalacích I2P, bez ohledu na to, jak staré nebo nové je původní instalace, ale nemusí být nutně v classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Cokoliv neuvedené výše nemusí být přítomno v classpath každého, i když to máte v classpath ve VAŠÍ verzi i2p. Pokud potřebujete jakýkoliv jar neuvedený výše, přidejte $I2P/lib/foo.jar do classpath specifikované v clients.config nebo webapps.config ve vašem pluginu.

Dříve byla položka classpath specifikovaná v clients.config přidána do classpath pro celou JVM. Avšak od verze 0.7.13-3 byl tento problém vyřešen pomocí class loaderů a nyní, jak bylo původně zamýšleno, je specifikovaná classpath v clients.config pouze pro konkrétní vlákno. Proto specifikujte kompletní požadovanou classpath pro každého klienta.

## Poznámky k verzi Javy

I2P vyžaduje Javu 7 od vydání 0.9.24 (leden 2016). I2P vyžadovalo Javu 6 od vydání 0.9.12 (duben 2014). Všichni uživatelé I2P s nejnovější verzí by měli používat JVM 1.7 (7.0).

Pokud váš plugin **nevyžaduje verzi 1.7**:

-   Ujistěte se, že všechny soubory java a jsp jsou kompilovány s source="1.6" target="1.6".
-   Ujistěte se, že všechny přibalené knihovní jar soubory jsou také pro verzi 1.6 nebo nižší.

Pokud váš plugin **vyžaduje verzi 1.7**:

-   Poznamenejte si to na vaší stránce pro stahování.
-   Přidejte min-java-version=1.7 do vašeho plugin.config

V každém případě **musíte** nastavit bootclasspath při kompilaci s Java 8, abyste zabránili pádům za běhu.

## JVM crashuje při aktualizaci

Poznámka - toto všechno by mělo být nyní opraveno.

JVM má tendenci havarovat při aktualizaci jar souborů v pluginu, pokud byl tento plugin spuštěn od startu I2P (i když byl plugin později zastaven). Toto mohlo být opraveno implementací class loaderu ve verzi 0.7.13-3, ale nemusí.

Nejbezpečnější je navrhnout váš plugin s jar souborem uvnitř war souboru (pro webovou aplikaci), nebo vyžadovat restart po aktualizaci, nebo neaktualizovat jar soubory ve vašem pluginu.

Kvůli způsobu, jakým fungují class loadery uvnitř webové aplikace, _může_ být bezpečné mít externí jary, pokud zadáte classpath v webapps.config. Je potřeba více testování, aby se to ověřilo. Nezadávejte classpath s 'falešným' klientem v clients.config, pokud je potřeba pouze pro webovou aplikaci - místo toho použijte webapps.config.

Nejméně bezpečné a zjevně zdrojem většiny pádů jsou klienti s plugin jary specifikovanými v classpath v clients.config.

Nic z toho by nemělo být problémem při počáteční instalaci - nikdy byste neměli potřebovat restart pro počáteční instalaci pluginu.

## Reference

-   [Specifikace konfiguračního souboru](/docs/specs/configuration)
-   [DSA kryptografie](/docs/specs/cryptography#DSA)
-   [Specifikace aktualizací](/docs/specs/updates)
