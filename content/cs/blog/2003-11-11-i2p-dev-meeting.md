---
title: "Setkání vývojářů I2P - 11. listopadu 2003"
date: 2003-11-11
author: "jrand0m"
description: "Vývojářské setkání I2P o stavu routeru, aktualizacích roadmapy, nativní implementaci modPow, GUI instalátoru a diskusích o licencích"
categories: ["meeting"]
---

(S laskavým svolením Wayback Machine http://www.archive.org/)

## Stručné shrnutí

<p class="attendees-inline"><strong>Přítomni:</strong> dish, dm, jrand0m, MrEcho, nop</p>

(zápis ze schůzky upraven tak, aby zakryl skutečnost, že iip se v půlce schůzky zhroutil a že nastala spousta timeoutů pingů, takže to nečtěte jako souvislé vyprávění)

## Záznam ze schůzky

<div class="irc-log"> [22:02] &lt;jrand0m&gt; program [22:02] &lt;jrand0m&gt; 0) přivítání [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) stav [22:02] &lt;jrand0m&gt; 1.2) změny v roadmapě [22:02] &lt;jrand0m&gt; 1.3) otevřené subprojekty [22:02] &lt;jrand0m&gt; 2) native modPow [22:03] &lt;jrand0m&gt; 2) GUI installer [22:03] &lt;jrand0m&gt; 3) IM [22:03] &lt;jrand0m&gt; 4) naming service [22:03] &lt;MrEcho&gt; viděl jsem ten .c kód [22:03] &lt;jrand0m&gt; 5) licencování [22:03] &lt;jrand0m&gt; 6) ostatní? [22:03] &lt;jrand0m&gt; 0) přivítání [22:03] &lt;jrand0m&gt; ahoj. [22:03] &lt;nop&gt; hi [22:03] &lt;jrand0m&gt; schůzka 2^6 [22:04] &lt;jrand0m&gt; máš nějaké body do programu, které bys tam přidal, nop? [22:04] &lt;jrand0m&gt; ok, 1.1) stav routeru [22:04] &lt;jrand0m&gt; jsme 0.2.0.3 a naposledy, co jsem slyšel, je to funkční [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; správně? [22:05] &lt;MrEcho&gt; mám to spuštěné .. vypadá to v pohodě [22:05] &lt;nop&gt; ne [22:05] &lt;jrand0m&gt; po vydání 0.2.0.3 byly drobné commity, nic na další vydání [22:05] &lt;nop&gt; jen se snažím dohnat [22:05] &lt;jrand0m&gt; supr [22:06] &lt;jrand0m&gt; s ohledem na zkušenosti a zpětnou vazbu z 0.2.0.x byla roadmapa upravena tak, aby běh byl méně náročný na prostředky [22:06] &lt;jrand0m&gt; (čili aby lidé mohli provozovat webservery / atd. a nesežralo jim to CPU) [22:06] &lt;jrand0m&gt; konkrétně (přesun na bod 1.2): http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; čeho jsem si všiml je, že většina routerů používá: TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; přechází to automaticky na phttp, nebo to zkusí nejdřív tcp [22:07] &lt;jrand0m&gt; hmm, většina routerů by měla podporovat PHTTP, a pokud mohou přijímat příchozí spojení, měla by podporovat i TCP [22:07] &lt;jrand0m&gt; pokud je to jen trochu možné, používá to TCP [22:07] &lt;jrand0m&gt; PHTTP má váhu asi 1000× „dražší“ než TCP [22:08] &lt;jrand0m&gt; (viz GetBidsJob, který se každého transportu ptá, kolik si myslí, že bude stát poslat zprávu peerovi) [22:08] &lt;jrand0m&gt; (a viz TCPTransport.getBid a PHTTPTransport.getBid pro použité hodnoty) [22:08] &lt;MrEcho&gt; ok [22:08] &lt;jrand0m&gt; používáš PHTTP často k odesílání a přijímání zpráv? [22:09] &lt;jrand0m&gt; (to může být znak, že tvůj TCP listener není dosažitelný) [22:09] &lt;MrEcho&gt; na své straně jsem nezadal URL [22:09] &lt;jrand0m&gt; aha, ok. [22:09] &lt;MrEcho&gt; ohh je [22:10] &lt;jrand0m&gt; ok, jo, moje routery mají k tobě otevřená TCP spojení [22:10] &lt;dm&gt; to jsou ale pohostinné. [22:10] * jrand0m je rád, že jste mě přiměli implementovat routerConsole.html, takže nemusíme kvůli tomuhle bordelu hrabat v logách [22:11] &lt;MrEcho&gt; je tam nějaký timeout, že když se nepřipojí přes tcp, tak to jde phttp? a jaké je časování [22:11] &lt;jrand0m&gt; ale každopádně, velká změna v roadmapě je, že 0.2.1 implementuje věci kolem AES+SessionTag [22:11] &lt;MrEcho&gt; nebo bychom to mohli mít v nastavení? [22:11] &lt;jrand0m&gt; pokud dostane TCP connection refused / host not found / atd., ten pokus hned ukončí a zkusí další dostupnou nabídku [22:12] &lt;MrEcho&gt; takže žádné opakování [22:12] &lt;jrand0m&gt; phttp má timeout 30 s (pokud si dobře pamatuju) [22:12] &lt;jrand0m&gt; není potřeba opakovat. buď máš otevřené TCP spojení a můžeš poslat data, nebo ne :) [22:12] &lt;MrEcho&gt; lol ok [22:13] &lt;MrEcho&gt; bude to potom zkoušet tcp pokaždé, nebo to přeskočí a půjde rovnou phttp pro další spojení? [22:13] &lt;jrand0m&gt; aktuálně to pokaždé zkusí tcp. [22:13] &lt;jrand0m&gt; transporty si zatím nevedou historii [22:13] &lt;MrEcho&gt; ok super [22:14] &lt;jrand0m&gt; (ale pokud peer selže 4×, dostane se na černou listinu na 8 minut) [22:14] &lt;MrEcho&gt; jakmile druhá strana dostane phttp zprávu, měla by se připojit k routeru, který zprávu poslal, přes tcp, že? [22:14] &lt;jrand0m&gt; správně. jakmile je navázáno nějaké tcp spojení, může ho použít. [22:14] &lt;jrand0m&gt; (ale pokud oba peery mají jen phttp, budou pochopitelně používat jen phttp) [22:15] &lt;MrEcho&gt; to by znamenalo, že nemohl navázat tcp spojení s ničím [22:15] &lt;MrEcho&gt; .. ale jo [22:16] &lt;MrEcho&gt; škoda, že se to nedá obejít [22:16] &lt;jrand0m&gt; ne, jeden z mých router nemá TCP adresu – jen PHTTP. ale navazuji TCP spojení s peery, kteří mají TCP adresy. [22:16] &lt;jrand0m&gt; (a pak mi mohou posílat zprávy po tom TCP spojení místo pomalejších PHTTP zpráv) [22:17] &lt;jrand0m&gt; nebo jsi myslel něco jiného? [22:17] &lt;MrEcho&gt; jo, popletl jsem to [22:17] &lt;jrand0m&gt; jasně, v pohodě [22:18] &lt;jrand0m&gt; takže, viz aktualizovaná roadmapa pro aktualizované informace o harmonogramu ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; ok, 1.3) otevřené subprojekty [22:19] &lt;jrand0m&gt; konečně jsem do wiki dal hromadu položek ze seznamu úkolů z mého palmpilotu na (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; takže pokud se nudíte a hledáte projekty na kódování... :) [22:19] &lt;MrEcho&gt; ty jo [22:20] &lt;MrEcho&gt; už mám 2 [22:20] &lt;dish&gt; Ty máš palmpilot, to je elita [22:20] &lt;MrEcho&gt; můj umřel [22:20] &lt;jrand0m&gt; mihi&gt; je tam položka ohledně I2PTunnel, popisující myšlenku, kterou jsem měl nedávno [22:20] &lt;MrEcho&gt; nevím, co s ním je [22:21] &lt;jrand0m&gt; jo, dřív jsem měl Palmy, ale tenhle mi byl nedávno darován pro věc ;) [22:21] &lt;dish&gt; Mohl by být na schůzce bod programu, kde bychom probrali, kdy naposledy userX něco napsal [22:21] &lt;MrEcho&gt; ta zatracená věc už se ani nezapne [22:21] &lt;MrEcho&gt; lol [22:22] &lt;jrand0m&gt; Nemyslím, že by UserX řekl cokoliv za poslední 4 nebo 5 měsíců ;) [22:22] &lt;MrEcho&gt; je to bot nebo co? [22:22] &lt;dish&gt; Co říkali před 5 měsíci? [22:22] &lt;MrEcho&gt; vsadím se, že je to bitchx běžící na nějakém stroji, ke kterému míval přístup .. a zapomněl na něj [22:22] &lt;jrand0m&gt; že se příští týden ozvou s komentáři k anonCommFramework (starý název i2p) ;) [22:23] &lt;dish&gt; haha [22:23] &lt;jrand0m&gt; ale předpokládám, že je zaneprázdněný. takový je život [22:23] &lt;jrand0m&gt; ok, 2) native modPow [22:23] &lt;MrEcho&gt; viděl jsem ten c kód [22:24] &lt;jrand0m&gt; dal jsem dohromady stub .c a Java třídu, abych ukázal, jak by se mohlo integrovat něco jako GMP nebo jiná MPI knihovna, ale očividně to nefunguje [22:25] &lt;jrand0m&gt; bylo by fajn, kdybychom měli malý balíček C tříd a k tomu triviální Java wrapper třídu, který bychom mohli zbuildit pro windows, osx, *bsd, linux a zabalit pod GPL

(zde vložte zásadní selhání iip)

[22:38] &lt;MrEcho&gt; poslední věc, co jsem viděl, byla: [13:25] &lt;jrand0m&gt; ok, 2) native modPow
[22:38] &lt;jrand0m&gt; ahoj, MrEcho
[22:38] &lt;jrand0m&gt; jo, vypadá to, že hlavní proxy spadla
[22:39] &lt;jrand0m&gt; dám tomu ještě 2 minuty, než to restartuju
[22:39] &lt;MrEcho&gt; k
[22:39] &lt;MrEcho&gt; za 25 $ jednorázově můžu získat plnou Javu na thenidus.net ... jeden z mých webů
[22:40] &lt;jrand0m&gt; 25 $? Oni si účtují za instalaci softwaru?
[22:40] &lt;MrEcho&gt; fakt nevím .. je to balíček
[22:40] &lt;MrEcho&gt; právě o tom mluvím s kámošem
[22:40] &lt;jrand0m&gt; nejsem si jistý, že je ten kód dost stabilní na to, abychom šli a pronajali hromadu míst v colo (colocation – umístění serverů) k nasazení routers. Zatím :)
[22:41] &lt;dm&gt; balíček čeho?
[22:41] &lt;MrEcho&gt; java - jsp
[22:41] &lt;jrand0m&gt; ok, posílám znovu, co jsem poslal předtím:
[22:41] &lt;jrand0m&gt; dal jsem dohromady stub .c a Java třídu, aby bylo vidět, jak by se dalo integrovat něco jako GMP nebo jiná MPI knihovna, ale očividně to nefunguje
[22:41] &lt;jrand0m&gt; dobré by bylo, kdybychom měli malý balík C tříd a k tomu triviální Java wrapper class (obalovací třída), které bychom mohli sestavit pro windows, osx, *bsd, linux a zabalit pod GPL (nebo méně restriktivní licencí)
[22:41] &lt;jrand0m&gt; nicméně s novou roadmapou, která dává AES+SessionTag jako můj aktuální úkol, to není tak kritické jako dřív.
[22:42] &lt;jrand0m&gt; pokud by s tím ale někdo chtěl pohnout, bylo by to super (a jsem si jistý, že jiný projekt, který všichni známe, by o takové balení stál)
[22:43] &lt;dm&gt; frazaa?
[22:43] &lt;jrand0m&gt; heh, svým způsobem ;)
[22:44] &lt;jrand0m&gt; ok, 3) gui installer
[22:44] &lt;jrand0m&gt; MrEcho&gt; hi
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; hehe
[22:44] &lt;MrEcho&gt; už to nějak postupuje
[22:44] &lt;jrand0m&gt; super
[22:44] &lt;MrEcho&gt; nic extra
[22:45] &lt;MrEcho&gt; mám pár fakt dobrých nápadů, jak to udělat fakt vymazlené .. ale to je ještě daleko
[22:45] &lt;jrand0m&gt; přemýšlel jsem, jestli by instalátor neměl přidat 1) možnost automaticky stáhnout seeds z http://.../i2pdb/ 2) automaticky stáhnout http://.../i2p/squid.dest a vytvořit i runSquid.bat/runSquid.sh?
[22:45] &lt;jrand0m&gt; jasně
[22:46] &lt;jrand0m&gt; jo, chceme, aby byl instalátor co nejjednodušší – jaké vychytávky jsi měl na mysli?
[22:46] &lt;MrEcho&gt; otázka je .. když uděláš java -jar installer   tak to jde ve výchozím stavu do non gui kvůli tomu, jak to máš udělané
[22:46] &lt;MrEcho&gt; jak to uděláme, aby když dvakrát klikneš na ten JAR soubor, nahrála se GUI
[22:47] &lt;jrand0m&gt; install.jar &lt;-- nongui,  installgui.jar &lt;-- gui
[22:47] &lt;jrand0m&gt; samostatný kód, samostatné balíčky
[22:47] &lt;MrEcho&gt; "fancy" ve smyslu věcí, kterých si možná ani nevšimneš .. ale bude to hezké a čisté
[22:47] &lt;jrand0m&gt; fajn
[22:47] &lt;MrEcho&gt; aha, ok
[22:48] &lt;jrand0m&gt; (nebo install &lt;-- gui installcli &lt;-- cli.  uvidíme, jak se to vyvine)
[22:49] &lt;jrand0m&gt; ještě něco k GUI, nebo přeskočíme na bod 4)?
[22:49] &lt;jrand0m&gt; (máš nějaký odhad časového rámce? žádný tlak, jen se ptám)
[22:51] &lt;MrEcho&gt; teď fakt nevím
[22:51] &lt;jrand0m&gt; super
[22:51] &lt;jrand0m&gt; ok, 4) IM
[22:51] &lt;jrand0m&gt; thecrypto tu není, takže.....
[22:51] &lt;jrand0m&gt; 5) služba názvů
[22:51] &lt;jrand0m&gt; wiht tu taky není...
[22:51] &lt;jrand0m&gt; ping
[22:52] &lt;dish&gt; máš špatně číslování agendy
[22:52] &lt;dish&gt; 3) IM
[22:52] &lt;jrand0m&gt; jo, kdysi jsem měl dva body s číslem 2
[22:52] &lt;dish&gt; 4) Pojmenování
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; (native modPow and gui installer)
[22:52] &lt;jrand0m&gt; vidíš, jsme dynamičtí a tak
[22:59] &lt;jrand0m&gt; ok, kvůli logům asi budu pokračovat
[22:59] &lt;jrand0m&gt; 6) licencování
[23:00] &lt;jrand0m&gt; přemýšlím o něčem méně restriktivním než GPL.  používáme nějaký kód pod MIT, plus jeden další soubor je pod GPL (ale to je jen base64 encoding a dá se snadno nahradit).  jinak je veškerý kód buď pod copyrightem mým, nebo thecrypto.
[23:00] * dish se dívá na mihi i2p tunnel část kódu
[23:01] &lt;jrand0m&gt; aha jasně, mihi to vydal jako gpl, ale klidně to může vydat i pod něčím jiným, pokud bude chtít
[23:01] &lt;jrand0m&gt; (ale i2ptunnel je v podstatě aplikace třetí strany a může si zvolit licenci, jakou chce)
[23:02] &lt;jrand0m&gt; (i když, protože i2p sdk je gpl, byl donucen být gpl)
[23:02] &lt;MrEcho&gt; sakra, konečně
[23:02] &lt;jrand0m&gt; nevím.  licencování není moje forte, ale kloním se minimálně k přechodu na lgpl
[23:02] * dish vydá těch 10–20 řádků změn v kódu I2P HTTP Client od mihi pod jakoukoli licenci, jakou má mihi
[23:03] &lt;jrand0m&gt; hehe :)
[23:06] &lt;jrand0m&gt; každopádně, 7) ostatní?
[23:07] &lt;jrand0m&gt; má někdo nějaké otázky / obavy / nápady ohledně i2p?
[23:07] &lt;dish&gt; Nech mě se zeptat
[23:07] &lt;dish&gt; Má I2P nějakou funkci 'group name'?
[23:07] &lt;jrand0m&gt; funkci 'group name'?
[23:07] &lt;dm&gt; team discovery channel!
[23:07] &lt;MrEcho&gt; lol
[23:08] &lt;dish&gt; Takže když chceš mít soukromou nebo oddělenou síť, ale některé routers se nějak promíchají, bez group name by se ty dvě sítě slily dohromady
[23:08] &lt;MrEcho&gt; myslí tím waste
[23:08] &lt;jrand0m&gt; aha
[23:08] &lt;dish&gt; nevím, proč bys to chtěl, ale jen se pro jistotu ptám
[23:08] &lt;jrand0m&gt; ano, na začátku návrhu sítě jsem si s tím pohrával
[23:09] &lt;jrand0m&gt; je to pokročilejší, než teď potřebujeme (nebo v relativně blízké budoucnosti [6–12 měsíců]), ale později to může být integrováno
[23:09] &lt;dish&gt; Nebo je to špatný nápad, protože je lepší udržet jednu velkou síť
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; heh dm
[23:10] &lt;nop&gt; drž hubu
[23:10] &lt;jrand0m&gt; ne, dish, to je dobrý nápad
[23:10] &lt;dm&gt; nop: drsňák?
[23:10] &lt;jrand0m&gt; to je v podstatě to, co přináší release 0.2.3 -- restricted routes (omezené trasy)
[23:10] &lt;jrand0m&gt; (aka máš malou soukromou (důvěryhodnou) sadu uzlů a nechceš, aby každý věděl, kdo to je, ale pořád s nimi chceš být schopen komunikovat)
[23:15] &lt;jrand0m&gt; ok, ještě něco?
[23:15] &lt;nop&gt; ne, jen si dělám srandu
[23:18] &lt;dm&gt; vtipálek?
[23:20] &lt;jrand0m&gt; ok, takže /zajímavé/ setkání, uprostřed s pár pády iip ;)
[23:21] * jrand0m *baf* ukončuje schůzku </div>
