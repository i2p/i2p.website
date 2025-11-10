---
title: "Setkání vývojářů I2P - 8. června 2004"
date: 2004-06-08
author: "duck"
description: "Zápis z vývojářské schůzky I2P ze dne 8. června 2004."
categories: ["meeting"]
---

## Stručné shrnutí

<p class="attendees-inline"><strong>Přítomni:</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## Zápis ze schůzky

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; čas schůzky 21:02:33 &lt;duck&gt; zápis je na http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; ale udělal jsem chybu v číslování 21:02:45 &lt;duck&gt; takže první bod 5 bude přeskočen 21:02:53 &lt;hypercubus&gt; hurá! 21:03:03  * duck si dává do piva led 21:03:14  * mihi by přejmenoval první #5 na #4 ;) 21:03:27 &lt;hypercubus&gt; ale ne, příští týden prostě mějme dva body 4 ;-) 21:03:37  * duck přejmenovává 'hypercubus' na 'mihi' 21:03:48 &lt;hypercubus&gt; hurá! 21:03:49 &lt;duck&gt; ok 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; je v kanálu Nightblade? 21:04:39 &lt;duck&gt; (nečinný     : 0 dní 0 hodin 0 min 58 s) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck si znovu bere mikrofon 21:06:15 &lt;duck&gt; Nightblade napsal knihovnu SAM pro C / C++ 21:06:23 &lt;duck&gt; mně se to přeloží.. ale to je vše, co můžu říct :) 21:06:37 &lt;mihi&gt; žádné testovací případy? ;) 21:07:06 &lt;duck&gt; pokud jsou tu nějací uživatelé rFfreebsd, Nightblade by o vás mohl mít zájem 21:07:08 &lt;ugha_node&gt; Volání strstr mě v tom kódu fakt rozčilovala. ;) 21:07:27 &lt;ugha_node&gt; duck: Co je to rFfreebsd? 21:07:42 &lt;duck&gt; takhle jsem napsal freebsd 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; Škoda, že -F nefunguje s rm. 21:08:30 &lt;duck&gt; ugha_node: je to pod BSD licencí; tak to oprav 21:08:41 &lt;fvw&gt; to mi zní rozumně :). Bohužel jsem před časem odinstaloval svůj poslední freebsd stroj. Mám                  účty na strojích jiných lidí, a jsem ochotný spouštět testy. 21:08:43 &lt;ugha_node&gt; duck: Možná jo. :) 21:08:50 &lt;duck&gt; (zatracení BSD hipíci) 21:09:09 &lt;duck&gt; ach, hezké a krátké, franku 21:09:17 &lt;duck&gt; ještě nějaké komentáře k libsam? 21:09:49 &lt;duck&gt; fvw: hádám, že se ti Nightblade ozve, pokud bude něco potřebovat 21:09:50  * fvw brblá nad zcela normálním chováním unixu, které mu zabíjí irc klienta. 21:10:02 &lt;duck&gt; ale protože jeho e-mail byl týden starý, možná na něco přišel 21:10:17 &lt;mihi&gt; fvw: ? 21:10:24 &lt;fvw&gt; jo, jestli mě někdo chtěl vzít za slovo, nějak mi to uniklo. Klidně                  pošlete e‑mail nebo tak něco. 21:10:42  * duck přeskakuje k #2 21:10:46 &lt;hypercubus&gt; ehm, kam? ;-) 21:10:54 &lt;duck&gt; 2) procházet i2p a běžný web jedním prohlížečem 21:10:57 &lt;fvw&gt; čerstvá instalace, ještě jsem neřekl svému zsh, aby neposílal HUP věcem na pozadí.                  &lt;/offtopic&gt;

21:11:09 &lt;fvw&gt; hypercubus: myslím, že jsem na seznamu uživatelů veřejného mailing listu. fvw.i2p@var.cx
21:12:11 &lt;duck&gt; bylo tam něco o přidání všech TLD do seznamu výjimek pro proxy ve vašem prohlížeči
21:12:23 &lt;fvw&gt; vyžaduje to diskusi? Myslím, že to bylo v podstatě vyřešeno na                  mailing listu.
21:12:24 &lt;duck&gt; myslím, že je to ošklivý hack
21:12:36 &lt;fvw&gt; ano, to bylo zmíněno. Vítej zpátky.
21:12:47 &lt;duck&gt; fvw: vlákno jsem nečetl :)
21:13:12 &lt;duck&gt; dobře, pokud o tom nechcete diskutovat, přejděte k #3
21:13:19 &lt;duck&gt; * 3) chatovací kanál
21:13:23 &lt;hypercubus&gt; skript od cervantese funguje perfektně na Konqueroru 3.2.2, Firefoxu 0.8 a                         Opeře 7.51, vše pro Gentoo s KDE 3.2.2
21:13:39  * mihi umísťuje vlajku na #4
21:13:55 &lt;duck&gt; #i2p-chat je zde alternativní kanál pro off-topic chat a lehkou podporu
21:14:08 &lt;duck&gt; nevím, kdo to zaregistroval
21:14:12 &lt;hypercubus&gt; já
21:14:17 &lt;duck&gt; tak radši opatrně :)
21:14:22 &lt;fvw&gt; ehm, žádná #4 není, jen dvě #5 :)
21:14:33 &lt;hypercubus&gt; budu mít štěstí, jestli si na heslo vzpomenu, až ho budu potřebovat ;-)
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Kanál: #i2p-chat
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Kontakt: hypercubus <<ONLINE>>

21:14:33 &lt;mihi&gt; [22:27] -ChanServ-    Alternativa: cervantes &lt;&lt;ONLINE&gt;&gt; 21:14:37 &lt;mihi&gt; [22:27] -ChanServ-   Registrováno: před 4 dny (0h 2m 41s) 21:15:12 &lt;hypercubus&gt; dal jsem pár důvěryhodným lidem op práva pro případy, kdy nejsem nablízku a                         je problém 21:15:24 &lt;duck&gt; zní to dobře 21:15:39 &lt;duck&gt; může to být trochu přehnané 21:15:51 &lt;hypercubus&gt; na IRC nikdy nevíš ;-) 21:15:55 &lt;duck&gt; ale poté, co se sem přidala ta protogirl, jsem si říkal, že by bylo dobré                   tenhle kanál uklidit 21:16:03 &lt;hypercubus&gt; heh 21:16:27 &lt;hypercubus&gt; stejně to někdy v příštích pár měsících určitě budeme potřebovat 21:16:34 &lt;duck&gt; jups 21:16:48 &lt;duck&gt; a pak nás lidi z freenode vykopnou  21:16:55 &lt;hypercubus&gt; ;-) 21:17:13 &lt;duck&gt; nemají rádi nic, co není napsané v jejich „kampf“ 21:17:16 &lt;duck&gt; ehm 21:17:44  * duck přejde na $nextitem a aktivuje mihiho breakpoint 21:17:47 &lt;hypercubus&gt; myslel jsem, že propojení nového kanálu s podporou by to pro                         freenode zlegitimizovalo 21:18:47 &lt;duck&gt; hypercubus: možná budeš překvapen 21:19:04 &lt;hypercubus&gt; *ehm* přiznávám, že jsem si nepřečetl všechny zásady... 21:19:24 &lt;duck&gt; je to ruská ruleta 21:19:39 &lt;hypercubus&gt; hmm, nemyslel jsem, že by to bylo až tak vážné 21:19:52  * duck je negativní 21:19:54 &lt;hypercubus&gt; no, podívám se, co s tím můžeme udělat 21:20:09 &lt;fvw&gt; promiňte, asi mi něco uniklo. Proč by nás freenode vyhodil? 21:20:21  * duck se dívá na timeout čítač pro mihiho breakpoint 21:20:32 &lt;duck&gt; fvw: zaměřují se na vývojářské kanály 21:20:35 &lt;mihi&gt; ? 21:20:53 &lt;mihi&gt; duck: breakpoint se spouští na /^4).*/ 21:21:01 &lt;duck&gt; mihi: ale žádná #4 není 21:21:06 &lt;fvw&gt; no a? i2p je tak v alfě, že teď je i podpora vlastně vývoj. 21:21:11 &lt;fvw&gt; (a ne, tohle mě necitujte) 21:21:36 &lt;duck&gt; fvw: možná nejsi obeznámen s typy diskusí, které se skutečně                   vedly na IIP 21:21:38 &lt;hypercubus&gt; jo, ale máme na to *2* kanály 21:21:45 &lt;duck&gt; a které se pravděpodobně budou odehrávat v kanálech #i2p 21:22:04 &lt;duck&gt; jsem si docela jistý, že to freenode neocení. 21:22:10 &lt;Nightblade&gt; už jsem tady 21:22:49 &lt;hypercubus&gt; darujeme jim mixér na margaritu nebo tak něco 21:22:49 &lt;mihi&gt; duck: k čemu se vztahuješ? ty flood útoky? nebo #cl? nebo co? 21:23:08 &lt;fvw&gt; diskuse na IIP nebo diskuse na #iip? Na #iip jsem neviděl nic kromě                  vývoje a podpory. A diskuse na IIP by se přesunuly do I2P, ne                  #i2p@freenode. 21:23:09 &lt;duck&gt; všelijaké politicky nekorektní řeči 21:23:36 &lt;fvw&gt; existují stroje na margaritu? Ó, to chci. 21:23:54 &lt;duck&gt; no nic 21:24:38 &lt;hypercubus&gt; máme se vrátit k bodu 2)? 21:24:58 &lt;duck&gt; hypercubus: co chceš dodat k proxy v prohlížeči? 21:25:18 &lt;hypercubus&gt; ups, číslo 1... když nás právě poctil svojí přítomností nightblade ;-) 21:25:33 &lt;duck&gt; Nightblade: vzali jsme si svobodu 'probrat' libsam 21:25:42 &lt;Nightblade&gt; Ok, řeknu pár slov 21:25:48 &lt;hypercubus&gt; ale jo, teď mě napadá, že jsem měl ještě něco k té záležitosti s                         prohlížečem, co se na seznamu neprobíralo 21:25:56 &lt;duck&gt; Nightblade: fvw nám řekl, že by mohl pomoci s nějakým                   testováním na freebsd 21:26:20 &lt;fvw&gt; Už nemám stroj s freebsd, ale mám účty na strojích s freebsd, dejte mi testovací případy a rád je spustím. 21:27:02 &lt;Nightblade&gt; Začal jsem pracovat na C++ dht, která používá Libsam (C).  Zatím jsem                         se nedostal nijak zvlášť daleko, i když na tom hodně                         pracuji.  teď si uzly v dht mohou navzájem "pingovat" přes sam                         data message 21:27:09 &lt;Nightblade&gt; přitom jsem našel pár drobných chyb v libsam 21:27:18 &lt;Nightblade&gt; kvůli nim někdy v budoucnu zveřejním novou verzi 21:27:51 &lt;ugha_node&gt; Nightblade: Mohl bys prosím odstranit ta volání 'strstr' z libsam? :) 21:27:52 &lt;Nightblade&gt; testovací případ je: zkuste to zkompilovat a nahlaste mi chyby 21:28:01 &lt;Nightblade&gt; co je špatně na strstr 21:28:21 &lt;ugha_node&gt; Není určená k použití místo strcmp. 21:28:38 &lt;Nightblade&gt; jo a taky se chystám portovat libsam na Windows, ale to není                         v dohledné budoucnosti 21:29:07 &lt;Nightblade&gt; je na tom, jak to používám, něco špatně, kromě estetiky? 21:29:15 &lt;Nightblade&gt; můžete mi poslat změny nebo říct, co byste raději udělali 21:29:19 &lt;Nightblade&gt; to se zkrátka zdálo jako nejjednodušší způsob 21:29:21 &lt;ugha_node&gt; Nightblade: Ničeho jsem si nevšiml. 21:29:32 &lt;fvw&gt; strcmp je samozřejmě efektivnější než strstr. 21:29:36 &lt;ugha_node&gt; Ale jen jsem to proletěl. 21:30:20 &lt;ugha_node&gt; fvw: Občas lze zneužít věci, které používají strstr místo                        strcmp, ale tohle není ten případ. 21:31:22 &lt;Nightblade&gt; jo, teď vidím místa, kde to můžu změnit 21:31:28 &lt;fvw&gt; to taky, ale předpokládám, že by sis toho všiml. Ve skutečnosti bys                  musel použít strncmp, abys těm exploitům zabránil. Ale to není podstatné. 21:31:31 &lt;Nightblade&gt; nepamatuju si, proč jsem to udělal takhle 21:31:57 &lt;ugha_node&gt; fvw: Souhlasím. 21:32:27 &lt;Nightblade&gt; aha, teď už vím proč 21:32:40 &lt;Nightblade&gt; je to líný způsob, jak nemuset zjišťovat délku pro strncmp 21:32:49 &lt;duck&gt; heh 21:32:52 &lt;ugha_node&gt; Nightblade: Heheh. 21:33:01 &lt;fvw&gt; použij min(strlen(foo), sizeof(*foo)) 21:33:04 &lt;hypercubus&gt; může začít výprask? 21:33:15 &lt;fvw&gt; Myslel jsem, že nejdřív přijde orální sex? *uhýbá* 21:33:32 &lt;fvw&gt; dobře, další bod, myslím. Hypercube měl poznámku k proxy? 21:33:38 &lt;hypercubus&gt; heh 21:33:54 &lt;duck&gt; sem s tím! 21:34:03 &lt;Nightblade&gt; provedu změny do příští verze – některé z nich                         alespoň změním 21:34:25 &lt;hypercubus&gt; ok, tohle se v kanálu před pár týdny krátce probíralo,                         ale myslím, že stojí za to se k tomu vrátit 21:34:48 &lt;deer&gt; * Sugadude se dobrovolně hlásí k provedení orálního sexu. 21:34:59 &lt;hypercubus&gt; místo přidávání TLD do blokovacího seznamu prohlížeče nebo používání                         proxy skriptu je tu třetí možnost 21:35:29 &lt;hypercubus&gt; která by z hlediska anonymity neměla mít stejné nevýhody jako ty                         dva přístupy 21:36:17 &lt;fvw&gt; kterou vám prozradím za super nízkou cenu 29,99 $? Tak už to vyklop! 21:36:27 &lt;hypercubus&gt; a tou by bylo, aby eeproxy přepisoval příchozí HTML stránky tak, aby                         stránku vložil do framesetu...  21:36:58 &lt;hypercubus&gt; hlavní frame by obsahoval požadovaný HTTP obsah, ten druhý                         frame by sloužil jako ovládací lišta 21:37:13 &lt;hypercubus&gt; a umožňoval by vám libovolně zapínat/vypínat proxy 21:37:40 &lt;hypercubus&gt; a také by vás upozornil, třeba barevnými okraji nebo jiným                         upozorněním, že procházíte neanonymně 21:37:54 &lt;fvw&gt; jak zabráníte tomu, aby si i2p web (s JavaScriptem apod.) nevypnul                  anonymitu? 21:37:59  * duck se snaží aplikovat jrandom-skill-level-of tolerance 21:37:59 &lt;hypercubus&gt; nebo že odkaz na stránce eepsite vede na RealWeb(tm) 21:38:04 &lt;duck&gt; super! udělej to! 21:38:16 &lt;fvw&gt; stejně budete muset udělat něco jako fproxy, nebo udělat něco,                  co není ovládané prohlížečem, pro přepínání. 21:38:29 &lt;ugha_node&gt; fvw: Přesně tak. 21:39:10 &lt;hypercubus&gt; proto to sem znovu házím, třeba bude mít někdo                         nápady, jak to zabezpečit 21:39:31 &lt;hypercubus&gt; ale podle mě je to něco, co bude většina koncových                         uživatelů i2p hodně potřebovat 21:39:33 &lt;hypercubus&gt; *uživatelé 21:40:04 &lt;hypercubus&gt; protože přístupy typu TLD/proxy skript/vyhrazený prohlížeč jsou                         na běžného uživatele internetu příliš 21:40:29 &lt;fvw&gt; Z dlouhodobého hlediska si myslím, že nejlepší je něco jako fproxy. Ale to                  rozhodně není priorita, a upřímně si nemyslím, že prohlížení webů bude                  killer aplikace i2p. 21:40:42 &lt;Sonium&gt; Co je vlastně netDb? 21:40:59 &lt;duck&gt; Sonium: databáze známých routerů 21:41:10 &lt;hypercubus&gt; fproxy je pro většinu uživatelů příliš těžkopádný 21:41:32 &lt;Sonium&gt; neohrožuje taková databáze anonymitu? 21:41:39 &lt;hypercubus&gt; podle mě je to část důvodu, proč se freenet nikdy neuchytil mimo                         vývojářskou komunitu 21:41:41 &lt;fvw&gt; hypercube: ne nutně. proxy autoconfiguration ("pac") to může udělat tak                  jednoduché, že stačí vyplnit jednu hodnotu v nastavení prohlížeče. Myslím, že                  bychom neměli podceňovat, že v dohledné době budou všichni uživatelé i2p                  aspoň trochu počítačově zdatní. (navzdory všem důkazům na                  freenet-support) 21:42:00 &lt;ugha_node&gt; Sonium: Ne, 'zlí hoši' by ty informace stejně mohli nasbírat ručně. 21:42:21 &lt;Sonium&gt; ale když je NetDb dole, je dole i i2p, že? 21:42:29 &lt;fvw&gt; hypercubus: Ani ne, myslím, že za to spíš může fakt, že to od začátku 0.5 vůbec                  nefungovalo. &lt;/offtopic time="once again"&gt;

21:42:44 &lt;fvw&gt; Sonium: můžeš mít víc než jednu netdb (kdokoli může jednu provozovat)
21:42:58 &lt;hypercubus&gt; už máme pac a i když to z technického hlediska funguje skvěle, realisticky to                         neochrání anonymitu avg. jog
21:43:03 &lt;hypercubus&gt; *avg. joe
21:43:22 &lt;ugha_node&gt; fvw: Ehm.. Každý router má vlastní netDb.
21:43:42 &lt;duck&gt; ok. Za chvíli odpadnu. Nezapomeňte po dokončení schůzku *baff* uzavřít
21:43:52 &lt;ugha_node&gt; I2P už nemá žádné centrální závislosti.
21:44:07 &lt;hypercubus&gt; ok, jen jsem chtěl tuhle myšlenku formálně dostat do logů ;-)
21:44:30 &lt;fvw&gt; ugha_node: ok, tedy publikovaná netdb. Ve skutečnosti (zatím) neprovozuju uzel, s                  terminologií nejsem úplně v obraze.
21:44:34 &lt;ugha_node&gt; Hmm. Nechtěl mihi něco říct?
21:45:05  * fvw dává duckovi čokoládu s kávovou příchutí, aby ho udržel vzhůru a v chodu ještě o chvilku            déle.
21:45:07 &lt;mihi&gt; ne :)
21:45:21 &lt;mihi&gt; je duck síťové zařízení? ;)
21:45:25 &lt;ugha_node&gt; mihi: mimochodem, vezmeš si odměnu za zvýšení velikosti okna?
21:45:28  * fvw dává duckovi čokoládu s příchutí alkoholu, aby ho definitivně vypnul.
21:45:30 &lt;hypercubus&gt; ve švédštině
21:45:52 &lt;mihi&gt; ugha_node: jaká odměna?
21:46:00 &lt;hypercubus&gt; dobře, tak tedy k bodu 5), rant-a-rama? ;-)
21:46:13 &lt;ugha_node&gt; mihi: http://www.i2p.net/node/view/224
21:46:27  * duck sní trochu fvwovy čokolády
21:47:16 &lt;mihi&gt; ugha_node: rozhodně ne; promiň
21:47:36 &lt;ugha_node&gt; mihi: Eh, dobře. :(
21:48:33  * mihi se před časem pokusil zbastlit "staré" streaming api, ale to bylo příliš            zabugované...
21:48:53 &lt;mihi&gt; ale IMHO by bylo snazší opravit tamto než opravovat to moje...
21:49:21 &lt;ugha_node&gt; Heh.
21:49:42 &lt;hypercubus&gt; tak skromný
21:49:46 &lt;mihi&gt; protože už v sobě má nějakou (rozbitou) "reordering" podporu
21:50:49 &lt;Sonium&gt; jde nějak požádat deer, aby zjistil, kolik lidí je na kanálu i2p-#i2p?
21:51:01 &lt;duck&gt; ne
21:51:08 &lt;hypercubus&gt; kdepak, ale můžu to přidat do bogobot
21:51:08 &lt;Sonium&gt; :/
21:51:11 &lt;Nightblade&gt; !list
21:51:13 &lt;deer&gt; &lt;duck&gt; 10 lidí
21:51:13 &lt;hypercubus&gt; až dodělám instalátor ;-)
21:51:24 &lt;Sonium&gt; !list
21:51:32 &lt;Sonium&gt; o_O
21:51:35 &lt;mihi&gt; Sonium ;)
21:51:38 &lt;ugha_node&gt; Tohle není fserv kanál!
21:51:39 &lt;Sonium&gt; to byl trik!
21:51:40 &lt;ugha_node&gt; :)
21:51:41 &lt;hypercubus&gt; mělo by to být !who
21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown
21:51:48 &lt;cervantes&gt; ups, zmeškal jsem schůzku
21:51:57 &lt;ugha_node&gt; !list
21:52:01 &lt;Nightblade&gt; !who
21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom
21:52:17 &lt;mihi&gt; !who !has !the !list ?
21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands
21:52:33 &lt;Nightblade&gt; !ban fvw!*@*
21:52:42 &lt;mihi&gt; !ban *!*@*
21:52:50 &lt;hypercubus&gt; tuším, že dopadne soudcovské kladívko
21:52:51 &lt;duck&gt; zní to jako dobrý čas to ukončit
21:52:55 &lt;Sonium&gt; mimochodem, měl bys také implementovat příkaz !8 jako má chanserv
21:52:59 &lt;fvw&gt; správně, když to máme vyřešené, tak zavř... ano. to.
21:53:00  * hypercubus je jasnovidec
21:53:05 &lt;duck&gt; *BAFF*
21:53:11 &lt;Nightblade&gt; !baff
21:53:12 &lt;hypercubus&gt; moje vlasy, moje vlasy
21:53:24  * fvw ukazuje na hypercube a směje se. Tvoje vlasy! Tvoje vlasy! </div>
