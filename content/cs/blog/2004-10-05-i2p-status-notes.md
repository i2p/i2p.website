---
title: "Poznámky ke stavu I2P k 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání 0.4.1.1, analýzu statistik sítě, plány streaming library pro 0.4.2 a přibalený eepserver"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

## Rejstřík:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 stav

Po dost problematickém vydání 0.4.1 (a následné rychlé aktualizaci 0.4.1.1) se zdá, že je síť zpátky v normálu - v tuto chvíli je aktivních padesát a něco peerů (uzlů) a jak irc, tak eepsites(I2P Sites) jsou dostupné. Většinu potíží způsobilo nedostatečné testování nového transportu mimo laboratorní podmínky (např. sockety se v podivných chvílích rozbíjely, docházelo k nadměrným prodlevám apod.). Příště, až bude potřeba provést změny na této vrstvě, to před vydáním otestujeme ve větším rozsahu.

## 2) Pěkné obrázky

Během posledních několika dní proběhlo v CVS velké množství aktualizací a jednou z novinek byla nová komponenta pro zaznamenávání statistik, která nám umožňuje jednoduše vytahovat surová statistická data v okamžiku, kdy vznikají, místo abychom se museli zabývat hrubými průměry shromážděnými na /stats.jsp. S ní jsem sledoval několik klíčových statistik na několika routerech a postupně se blížíme k odhalení zbývajících problémů se stabilitou. Surové statistiky jsou poměrně objemné (20hodinový běh na duckově stroji vygeneroval téměř 60MB dat), ale od toho máme pěkné grafy - `http://dev.i2p.net/~jrandom/stats/`

Osa Y u většiny z nich je v milisekundách, zatímco osa X je v sekundách. Je zde několik zajímavých věcí, které stojí za zmínku. Za prvé, client.sendAckTime.png je poměrně dobrým přiblížením zpoždění jednoho round tripu (doba cesty tam a zpět), protože ack message (potvrzovací zpráva) je odeslána spolu s užitečnými daty a poté se vrací celou trasou přes tunnel - proto měla naprostá většina z téměř 33,000 úspěšně odeslaných zpráv čas round tripu pod 10 sekund. Pokud se pak podíváme na client.sendsPerFailure.png spolu s client.sendAttemptAverage.png, vidíme, že 563 neúspěšných odeslání bylo téměř vždy provedeno s maximálním počtem opakování, který povolujeme (5 s 10s soft timeoutem na pokus a 60s hard timeoutem), zatímco většina ostatních pokusů uspěla na první nebo druhý pokus.

Dalším zajímavým obrázkem je client.timeout.png, který vrhá značné pochyby na hypotézu, kterou jsem měl - že k selháním při odesílání zpráv docházelo v souvislosti s nějakým druhem místního přetížení. Vykreslená data ukazují, že využití příchozí šířky pásma se při výskytech selhání výrazně lišilo, nevyskytovaly se žádné konzistentní špičky v čase zpracování lokálního odesílání a zdánlivě nebyl žádný vzorec ve vztahu k tunnel test latency.

Soubory dbResponseTime.png a dbResponseTime2.png jsou podobné souboru client.sendAckTime.png, až na to, že odpovídají zprávám netDb místo end‑to‑end klientských zpráv.

Soubor transport.sendMessageFailedLifetime.png ukazuje, jak dlouho lokálně podržíme zprávu, než ji z nějakého důvodu označíme za neúspěšnou (například protože vypršela její platnost nebo protože peer, na který míří, je nedostupný). Některým selháním se nelze vyhnout, ale tento obrázek ukazuje významný počet selhání hned po lokálním timeoutu odesílání (10s). Existuje několik věcí, které s tím můžeme udělat: - zaprvé, můžeme udělat shitlist (seznam dočasně blokovaných) adaptivnější- exponenciálně prodlužovat dobu, po kterou je peer na shitlistu, namísto pevného intervalu 4 minut. (to už bylo zaneseno do CVS) - zadruhé, můžeme zprávy předem označit jako selhané ve chvíli, kdy to vypadá, že by stejně selhaly. Abychom toho dosáhli, necháváme každé spojení sledovat svou rychlost odesílání a kdykoli je do jeho fronty přidána nová zpráva, pokud počet bajtů už zařazených ve frontě dělený rychlostí odesílání přesahuje zbývající čas do vypršení platnosti, zprávu okamžitě označíme za selhanou. Tuto metriku možná budeme moci použít i při rozhodování, zda přes daný peer přijmout další požadavky na tunnel.

Každopádně, přejděme k dalšímu hezkému obrázku - transport.sendProcessingTime.png. Na něm vidíte, že tento konkrétní stroj je jen zřídka zodpovědný za větší zpoždění - obvykle 10-100 ms, i když se někdy objeví špičky až na 1 s nebo více.

Každý bod zobrazený v tunnel.participatingMessagesProcessed.png představuje, kolik zpráv bylo předáno skrze tunnel, kterého se router účastnil. V kombinaci s průměrnou velikostí zprávy nám to dává odhadované zatížení sítě, které uzel přebírá pro ostatní.

Poslední obrázek je tunnel.testSuccessTime.png, který ukazuje, jak dlouho trvá poslat zprávu ven jedním tunnel a přes jiný příchozí tunnel ji dostat zpět domů, což nám dává odhad, jak dobré jsou naše tunnels.

Dobře, to už je prozatím hezkých obrázků dost. Data si můžete vygenerovat sami s jakýmkoli vydáním po 0.4.1.1-6 nastavením konfigurační vlastnosti routeru "stat.logFilters" na čárkami oddělený seznam názvů statistik (názvy vezměte ze stránky /stats.jsp). To se zapisuje do stats.log, který můžete zpracovat pomocí

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
který to rozdělí na samostatné soubory pro každou statistiku, vhodné pro načtení do vašeho oblíbeného nástroje (např. gnuplot).

## 3) 0.4.1.2 a 0.4.2

Od vydání 0.4.1.1 proběhlo mnoho aktualizací (úplný seznam viz historie), ale zatím bez kritických oprav. Tyto aktualizace nasadíme v příštím opravném vydání 0.4.1.2 později tento týden poté, co budou vyřešeny některé dosud otevřené chyby související s automatickou detekcí IP.

Dalším hlavním úkolem v té chvíli bude dosáhnout verze 0.4.2, která je nyní plánována jako zásadní přepracování zpracování tunnelů. Bude to spousta práce – revidovat šifrování a zpracování zpráv, stejně jako sdružování tunnelů –, ale je to poměrně kritické, protože útočník by v současnosti mohl poměrně snadno provést některé statistické útoky proti tunnelům (např. útok typu predecessor s náhodným pořadím tunnelů nebo sběr z netDb).

dm nicméně nastolil otázku, zda by dávalo smysl udělat nejprve streamingovou knihovnu (v současnosti plánovanou pro vydání 0.4.3). Výhodou by bylo, že by se síť stala spolehlivější a měla by lepší propustnost, což by povzbudilo další vývojáře, aby se pustili do vývoje klientských aplikací. Jakmile by to bylo hotové, mohl bych se poté vrátit k přepracování tunnelů a řešit (pro uživatele neviditelné) bezpečnostní problémy.

Technicky vzato jsou dva úkoly plánované pro 0.4.2 a 0.4.3 ortogonální a obě se stejně udělají, takže se nezdá, že by na jejich prohození byla nějaká velká nevýhoda. Přikláním se k názoru dm a pokud někdo nepřijde s důvody, proč nechat 0.4.2 jako aktualizaci pro tunnel a 0.4.3 jako streaming lib, prohodíme je.

## 4) Dodávaný eepserver

Jak bylo uvedeno v poznámkách k vydání verze 0.4.1, přibalili jsme software a konfiguraci potřebné k provozu eepsite(I2P Site) ihned po instalaci - stačí jednoduše vložit soubor do adresáře ./eepsite/docroot/ a sdílet I2P destinaci nalezenou na konzoli routeru.

Několik lidí mě ale upozornilo na mé nadšení pro soubory .war - většina aplikací bohužel vyžaduje o něco víc práce než jen zkopírovat soubor do adresáře ./eepsite/webapps/. Dal jsem dohromady stručný návod na spuštění blogovacího enginu blojsom a můžete se podívat, jak to vypadá, na webu detonate.

## 5) ???

To je zatím asi všechno – zaskočte na schůzku za 90 minut, pokud to chcete probrat.

=jr
