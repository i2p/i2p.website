---
title: "Instalace vlastních pluginů"
description: "Instalace, aktualizace a vývoj pluginů routeru"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P plugin framework umožňuje rozšířit router bez zásahu do základní instalace. Dostupné pluginy pokrývají e-mail, blogy, IRC, úložiště, wiki, monitorovací nástroje a další.

> **Bezpečnostní upozornění:** Pluginy běží se stejnými oprávněními jako router. Zacházejte se staženými soubory od třetích stran stejně, jako byste zacházeli s jakoukoli aktualizací podepsaného softwaru—před instalací ověřte zdroj.

## 1. Instalace pluginu

1. Zkopírujte URL pro stažení pluginu ze stránky projektu.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Otevřete [stránku konfigurace pluginů](http://127.0.0.1:7657/configplugins) v konzoli routeru.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Vložte URL do pole pro instalaci a klikněte na **Install Plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

Router stáhne podepsaný archiv, ověří podpis a plugin aktivuje okamžitě. Většina pluginů přidá odkazy v konzoli nebo služby na pozadí, aniž by vyžadovala restart routeru.

## 2. Proč na pluginech záleží

- Distribuce jedním kliknutím pro koncové uživatele—žádné ruční úpravy `wrapper.config` nebo `clients.config`
- Udržuje základní balík `i2pupdate.su3` malý a zároveň poskytuje velké nebo specializované funkce na vyžádání
- Volitelné JVM per plugin poskytují izolaci procesů v případě potřeby
- Automatické kontroly kompatibility s verzí routeru, Java runtime a Jetty
- Aktualizační mechanismus zrcadlí router: podepsané balíčky a inkrementální stahování
- Podporovány jsou console integrace, jazykové balíčky, UI témata a aplikace mimo Javu (přes skripty)
- Umožňuje kurátorované adresáře „app store", jako je `plugins.i2p`

## 3. Správa nainstalovaných pluginů

Použijte ovládací prvky na stránce [I2P Router Plugin](http://127.0.0.1:7657/configclients.jsp#plugin) k:

- Zkontrolovat aktualizace jednoho pluginu
- Zkontrolovat všechny pluginy najednou (spouští se automaticky po aktualizaci routeru)
- Nainstalovat všechny dostupné aktualizace jedním kliknutím  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Povolit/zakázat automatické spuštění pro pluginy, které registrují služby
- Čistě odinstalovat pluginy

## 4. Vytvořte si vlastní plugin

1. Projděte si [specifikaci pluginu](/docs/specs/plugin/) pro požadavky na balíčkování, podepisování a metadata.
2. Použijte [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) k zabalení existujícího binárního souboru nebo webové aplikace do instalovatelného archivu.
3. Zveřejněte URL adresy pro instalaci i aktualizaci, aby router mohl rozlišit mezi první instalací a postupnými upgrady.
4. Umístěte kontrolní součty a podpisové klíče viditelně na stránku vašeho projektu, abyste pomohli uživatelům ověřit autenticitu.

Hledáte příklady? Prohlédněte si zdrojový kód komunitních pluginů na `plugins.i2p` (například ukázku `snowman`).

## 5. Známá omezení

- Aktualizace pluginu, který obsahuje běžné JAR soubory, může vyžadovat restart routeru, protože Java class loader cachuje třídy.
- Konzole může zobrazovat tlačítko **Stop**, i když plugin nemá žádný aktivní proces.
- Pluginy spuštěné v samostatném JVM vytvoří adresář `logs/` v aktuálním pracovním adresáři.
- Při prvním výskytu je klíč podepisujícího automaticky důvěryhodný; neexistuje žádná centrální autorita pro podepisování.
- Windows někdy zanechává po odinstalaci pluginu prázdné adresáře.
- Instalace pluginu určeného pouze pro Java 6 na JVM Java 5 hlásí „plugin je poškozený" kvůli kompresi Pack200.
- Pluginy pro témata a překlady zůstávají z velké části netestované.
- Příznaky automatického startu ne vždy přetrvávají u nespravovaných pluginů.

## 6. Požadavky a doporučené postupy

- Podpora pluginů je dostupná v I2P **0.7.12 a novějších verzích**.
- Udržujte svůj router a pluginy aktuální, abyste získali bezpečnostní opravy.
- Dodávejte stručné poznámky k vydání, aby uživatelé pochopili, co se mezi verzemi změnilo.
- Pokud je to možné, hostujte archivy pluginů přes HTTPS uvnitř I2P, abyste minimalizovali vystavení metadat v čisté síti.

## 7. Další čtení

- [Specifikace pluginů](/docs/specs/plugin/)
- [Framework klientských aplikací](/docs/applications/managed-clients/)
- [Repozitář I2P skriptů](https://github.com/i2p/i2p.scripts/) pro balíčkovací utility
