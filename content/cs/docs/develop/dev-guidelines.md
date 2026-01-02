---
title: "Pokyny pro vývojáře a styl kódování"
description: "Kompletní návod pro přispívání do I2P: pracovní postup, cyklus vydání, styl kódování, logování, licencování a řešení problémů"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Nejprve si přečtěte [Průvodce pro nové vývojáře](/docs/develop/new-developers/).

## Základní pokyny a styl kódování

Většina z následujícího by měla být samozřejmostí pro každého, kdo pracoval na open source projektu nebo v komerčním programátorském prostředí. Následující se týká především hlavní vývojové větve i2p.i2p. Směrnice pro ostatní větve, pluginy a externí aplikace se mohou podstatně lišit; obraťte se na příslušného vývojáře pro bližší informace.

### Komunita

- Prosím, nepište jen kód. Pokud můžete, zapojte se i do dalších vývojových aktivit, včetně: vývojových diskusí a podpory na IRC a i2pforum.i2p; testování; hlášení chyb a odpovědí; dokumentace; revizí kódu; atd.
- Aktivní vývojáři by měli být pravidelně dostupní na IRC `#i2p-dev`. Buďte si vědomi aktuálního vývojového cyklu. Dodržujte milníky vydání, jako jsou zmrazení funkcí, zmrazení tagů a termín pro odevzdání kódu pro vydání.

### Cyklus vydání

Běžný cyklus vydání trvá 10–16 týdnů, čtyři vydání ročně. Následují přibližné termíny v rámci typického 13týdenního cyklu. Konkrétní termíny pro každé vydání stanovuje správce vydání po konzultaci s celým týmem.

- 1–2 dny po předchozím vydání: Začlenění do hlavní větve jsou povolena.
- 2–3 týdny po předchozím vydání: Termín pro přenos zásadních změn z jiných větví do hlavní větve.
- 4–5 týdnů před vydáním: Termín pro požadavky na nové odkazy na domovské stránce.
- 3–4 týdny před vydáním: Zmrazení funkcí. Termín pro zásadní nové funkce.
- 2–3 týdny před vydáním: Svolání projektové schůzky k přezkoumání požadavků na nové odkazy na domovské stránce, pokud existují.
- 10–14 dní před vydáním: Zmrazení řetězců. Žádné další změny přeložených (označených) řetězců. Odeslání řetězců do Transifexu, oznámení termínu překladu na Transifexu.
- 10–14 dní před vydáním: Termín pro funkce. Po tomto okamžiku pouze opravy chyb. Žádné další funkce, refaktoring ani úpravy.
- 3–4 dny před vydáním: Termín pro překlady. Stažení překladů z Transifexu a začlenění.
- 3–4 dny před vydáním: Termín pro začlenění. Po tomto okamžiku žádná začlenění bez povolení tvůrce vydání.
- Hodiny před vydáním: Termín pro kontrolu kódu.

### Git

- Mějte základní povědomí o distribuovaných systémech správy verzí, i když jste git dosud nepoužívali. Požádejte o pomoc, pokud ji potřebujete. Jakmile je změna odeslána, check-iny jsou navždy; neexistuje vrácení zpět. Buďte prosím opatrní. Pokud jste git dosud nepoužívali, začněte malými krůčky. Commitněte nějaké malé změny a uvidíte, jak to funguje.
- Otestujte své změny před jejich commitnutím. Pokud preferujete vývojový model commit‑před‑testováním, použijte vlastní vývojovou větev ve svém vlastním účtu a vytvořte MR, jakmile je práce hotová. Nerozbijte build. Nezpůsobujte regrese. V případě, že se to stane (stává se to), prosím nezmizíte na dlouhou dobu poté, co odešlete svou změnu.
- Pokud je vaše změna netriviální, nebo chcete, aby ji lidé otestovali, a potřebujete kvalitní testovací reporty, abyste věděli, zda byla vaše změna otestována či nikoli, přidejte komentář k commitu do `history.txt` a zvyšte revizi buildu v `RouterVersion.java`.
- Necommitujte zásadní změny do hlavní větve i2p.i2p pozdě v cyklu vydání. Pokud vám projekt zabere více než pár dní, vytvořte si vlastní větev v gitu ve svém vlastním účtu a proveďte vývoj tam, abyste neblokovali vydání.
- U velkých změn (obecně řečeno více než 100 řádků nebo dotýkajících se více než tří souborů) je commitněte do nové větve ve svém vlastním účtu na GitLabu, vytvořte MR a přiřaďte reviewera. Přiřaďte MR sobě. Mergněte MR sami, jakmile jej reviewer schválí.
- Nevytvářejte WIP větve v hlavním účtu I2P_Developers (kromě i2p.www). WIP patří do vašeho vlastního účtu. Když je práce hotová, vytvořte MR. Jediné větve v hlavním účtu by měly být pro skutečné forky, jako je bodové vydání.
- Vyvíjejte transparentním způsobem a s ohledem na komunitu. Commitujte často. Commitujte nebo mergujte do hlavní větve tak často, jak je to možné, při dodržení výše uvedených pokynů. Pokud pracujete na nějakém velkém projektu ve své vlastní větvi/účtu, informujte ostatní, aby mohli sledovat a provádět review/testování/komentáře.

### Styl kódování

- Styl kódování ve většině kódu je 4 mezery pro odsazení. Nepoužívejte tabulátory. Nepřeformátovujte kód. Pokud vaše IDE nebo editor chce vše přeformátovat, získejte nad ním kontrolu. Na některých místech je styl kódování odlišný. Používejte zdravý rozum. Napodobujte styl v souboru, který upravujete.
- Všechny nové veřejné a package-private třídy a metody vyžadují Javadocs. Přidejte `@since` číslo-vydání. Javadocs pro nové privátní metody jsou žádoucí.
- Pro jakékoliv přidané Javadocs nesmí existovat žádné chyby ani varování doclint. Spusťte `ant javadoc` s Oracle Java 14 nebo vyšší pro kontrolu. Všechny parametry musí mít řádky `@param`, všechny non-void metody musí mít řádky `@return`, všechny deklarované vyhazované výjimky musí mít řádky `@throws` a žádné HTML chyby.
- Třídy v `core/` (i2p.jar) a části i2ptunnel jsou součástí našeho oficiálního API. Existuje několik out-of-tree pluginů a dalších aplikací, které se na toto API spoléhají. Buďte opatrní, abyste neprovedli žádné změny, které by narušily kompatibilitu. Nepřidávejte metody do API, pokud nejsou obecně užitečné. Javadocs pro API metody by měly být jasné a úplné. Pokud přidáte nebo změníte API, aktualizujte také dokumentaci na webových stránkách (větev i2p.www).
- Označte řetězce pro překlad tam, kde je to vhodné, což platí pro všechny UI řetězce. Neměňte existující označené řetězce, pokud to není opravdu nutné, protože to naruší existující překlady. Nepřidávejte ani neměňte označené řetězce po zmrazení tagů ve vydávacím cyklu, aby měli překladatelé šanci aktualizovat před vydáním.
- Používejte generika a souběžné třídy, kde je to možné. I2P je vysoce multi-threadová aplikace.
- Buďte obeznámeni s běžnými úskalími Javy, které odhaluje FindBugs/SpotBugs. Spusťte `ant findbugs` pro více informací.
- Java 8 je vyžadována pro sestavení a spuštění I2P od vydání 0.9.47. Nepoužívejte třídy nebo metody Java 7 nebo 8 v embedded subsystémech: addressbook, core, i2ptunnel.jar (non‑UI), mstreaming, router, routerconsole (pouze news), streaming. Tyto subsystémy jsou používány Androidem a embedded aplikacemi, které vyžadují pouze Java 6. Všechny třídy musí být dostupné v Android API 14. Jazykové funkce Java 7 jsou v těchto subsystémech přijatelné, pokud jsou podporovány aktuální verzí Android SDK a kompilují se do kódu kompatibilního s Java 6.
- Try‑with‑resources nelze použít v embedded subsystémech, protože vyžaduje `java.lang.AutoCloseable` v runtime a to není dostupné až do Android API 19 (KitKat 4.4).
- Balíček `java.nio.file` nelze použít v embedded subsystémech, protože není dostupný až do Android API 26 (Oreo 8).
- Kromě výše uvedených omezení mohou být třídy, metody a konstrukce Java 8 použity pouze v následujících subsystémech: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (kromě news), SAM, susidns, susimail, systray.
- Autoři pluginů mohou vyžadovat jakoukoli minimální verzi Javy prostřednictvím souboru `plugin.config`.
- Explicitně převádějte mezi primitivními typy a třídami; nespoléhejte se na autoboxing/unboxing.
- Nepoužívejte `URL`. Použijte `URI`.
- Nechytejte `Exception`. Chytejte `RuntimeException` a checked výjimky individuálně.
- Nepoužívejte `String.getBytes()` bez argumentu UTF‑8 charset. Můžete také použít `DataHelper.getUTF8()` nebo `DataHelper.getASCII()`.
- Vždy specifikujte UTF‑8 charset při čtení nebo zápisu souborů. Utility `DataHelper` mohou být užitečné.
- Vždy specifikujte locale (například `Locale.US`) při použití `String.toLowerCase()` nebo `String.toUpperCase()`. Nepoužívejte `String.equalsIgnoreCase()`, protože locale nelze specifikovat.
- Nepoužívejte `String.split()`. Použijte `DataHelper.split()`.
- Nepřidávejte kód pro formátování dat a časů. Použijte `DataHelper.formatDate()` a `DataHelper.formatTime()`.
- Zajistěte, aby `InputStream`y a `OutputStream`y byly uzavřeny v finally blocích.
- Používejte `{}` pro všechny `for` a `while` bloky, i když mají jen jeden řádek. Pokud používáte `{}` pro buď `if`, `else`, nebo `if-else` blok, použijte je pro všechny bloky. Umístěte `} else {` na jeden řádek.
- Specifikujte pole jako `final` všude, kde je to možné.
- Neukládejte `I2PAppContext`, `RouterContext`, `Log` nebo jakékoli jiné reference na router nebo context položky do statických polí.
- Nespouštějte vlákna v konstruktorech. Použijte `I2PAppThread` místo `Thread`.

### Logování

Následující pravidla platí pro router, webové aplikace a všechny pluginy.

- Pro všechny zprávy nezobrazené na výchozí úrovni logování (WARN, INFO a DEBUG), pokud zpráva není statický řetězec (bez zřetězení), vždy použijte `log.shouldWarn()`, `log.shouldInfo()` nebo `log.shouldDebug()` před voláním logu, abyste předešli zbytečnému vytváření objektů.
- Logovací zprávy, které mohou být zobrazeny na výchozí úrovni logování (ERROR, CRIT a `logAlways()`), by měly být stručné, jasné a srozumitelné i pro netechnického uživatele. To zahrnuje text důvodu výjimky, který může být také zobrazen. Zvažte překlad, pokud se chyba pravděpodobně stane (například při chybách odesílání formuláře). V opačném případě není překlad nutný, ale může být užitečné vyhledat a znovu použít řetězec, který je již jinde označen k překladu.
- Logovací zprávy nezobrazené na výchozí úrovni logování (WARN, INFO a DEBUG) jsou určeny pro použití vývojáři a nemají výše uvedené požadavky. Nicméně zprávy WARN jsou dostupné v záložce Android log a mohou pomoci uživatelům při ladění problémů, proto používejte zprávy WARN také s určitou opatrností.
- Logovací zprávy INFO a DEBUG by měly být používány střídmě, zejména v často prováděných částech kódu. I když jsou užitečné během vývoje, zvažte jejich odstranění nebo zakomentování po dokončení testování.
- Nelogujte do stdout nebo stderr (wrapper log).

### Licence

- Commitujte pouze kód, který jste napsali sami. Před commitnutím jakéhokoli kódu nebo knihoven JARů z jiných zdrojů zdůvodněte, proč je to nezbytné, ověřte kompatibilitu licence a získejte souhlas od správce vydání.
- Pokud získáte souhlas k přidání externího kódu nebo JARů a binární soubory jsou dostupné v jakémkoli balíčku Debianu nebo Ubuntu, musíte implementovat možnosti sestavení a balíčkování pro použití externího balíčku. Kontrolní seznam souborů k úpravě: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- U jakýchkoli obrázků commitnutých z externích zdrojů je vaší odpovědností nejprve ověřit kompatibilitu licence. Uveďte informace o licenci a zdroji v komentáři k commitu.

### Chyby

- Správa problémů je úkolem každého; prosím pomozte. Sledujte [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) pro problémy, se kterými můžete pomoci. Komentujte, opravujte a zavírejte problémy, pokud můžete.
- Noví vývojáři by měli začít opravováním problémů. Když máte opravu, připojte svůj patch k problému a přidejte klíčové slovo `review-needed`. Nezavírejte problém, dokud nebyl úspěšně zkontrolován a neověřili jste své změny. Jakmile to provedete hladce pro pár tiketů, můžete následovat běžný postup výše.
- Zavřete problém, když si myslíte, že jste ho opravili. Nemáme testovací oddělení, které by ověřovalo a zavíralo tikety. Pokud si nejste jisti, že jste ho opravili, zavřete ho a přidejte poznámku "Myslím, že jsem to opravil, prosím otestujte a znovu otevřete, pokud je to stále nefunkční". Přidejte komentář s číslem dev buildu nebo revizí a nastavte milník na další vydání.
