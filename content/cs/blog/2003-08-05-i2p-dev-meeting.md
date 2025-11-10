---
title: "Setkání vývojářů I2P, 5. srpna 2003"
date: 2003-08-05
author: "nop"
description: "52. setkání vývojářů I2P zaměřené na stav vývoje Javy, aktualizace v kryptografii a pokrok v SDK"
categories: ["meeting"]
---

<h2 id="quick-recap">Stručné shrnutí</h2>

<p class="attendees-inline"><strong>Přítomní:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Zápis ze schůzky</h2>

<div class="irc-log"> <nop>	ok, schůze zahájena <nop>	co je na programu -->	logger (logger@anon.iip) se připojil k #iip-dev -->	Anon02 (~anon@anon.iip) se připojil k #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Vítejte na N-tém iip-dev setkání. <hezekiah>	Co je na programu? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	synchronizováno na NTP stratum 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) se připojil k #iip-dev <hezekiah>	Právě jsem se synchronizoval s NIST. :) <mihi>	tahle synchronizace nepomůže se zpožděními iip ;) <jrand0m>	nop: věci, které chci probrat: stav vývoje v Javě, stav kryptografie v Javě, stav vývoje Pythonu, stav SDK, pojmenovací služba <hezekiah>	(My _už_ jdeme na pojmenovací službu?) <jrand0m>	ne design, ty kreténe, to je coova parketa.  jen mluv o věcech, 	  pokud je o čem mluvit. <hezekiah>	Ach *	jrand0m ukládá LART <jrand0m>	je ještě něco na programu? <jrand0m>	nebo se do toho pustíme? <hezekiah>	No, nenapadá mě nic dalšího. <hezekiah>	Ach! <hezekiah>	Ó! <jrand0m>	ok.  stav vývoje v Javě: <hezekiah>	Dobře. <--	mrflibble odešel (Ping timeout) <nop>	ok <nop>	program <nop>	1) Přivítání <jrand0m>	k dnešku existuje java klientské API a stub java router, 	  které spolu dokážou komunikovat.  Navíc je tu aplikace zvaná ATalk, 	  umožňující anonymní IM + přenos souborů. <nop>	2) výpadky IIP 1.1 <nop>	3) I2P <nop>	4) Konec s komentáři a tak *	jrand0m jde zpátky do rohu <nop>	sorry 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah dává jrand0movi oslí čepici, aby ji 	  nosil v rohu. ;-) <nop>	omlouvám se za to <nop>	nevšiml jsem si, že jsi tam začal <nop>	možná bych měl jít do rohu <hezekiah>	lol <jrand0m>	žádný strach.  bod 1) *	hezekiah podává nopovi taky oslí čepici. :) <nop>	ok vítejte všichni <nop>	blá blá <nop>	2) výpadky IIP 1.1 -->	mrflibble (mrflibble@anon.iip) se připojil k #iip-dev <hezekiah>	52. iip-dev setkání a všechny ty dobré kecy! <nop>	server měl nedávno problémy se sektory na pevném disku a byl 	  vyměněn <nop>	Plánuji ten zatracený server přesunout do stabilnějšího prostředí s 	  redundancí <nop>	a možná svěřit řízení více ircd serverů <nop>	nevím <nop>	to je na diskusi <--	Anon02 odešel (EOF From client) <nop>	doufejme, že teď naše servery zůstanou online, protože byl vyměněn harddisk <nop>	omlouvám se za nepříjemnosti, lidi <nop>	3) I2P - Jrand0me, je to tvoje <nop>	pojď z rohu, jrand0me *	hezekiah jde do rohu, stáhne jrand0ma 	  ze židle, dotáhne ho k řečništi, vezme mu oslí čepici a podá mu mikrofon. *	nop jde do toho rohu, aby zaujal jeho místo <hezekiah>	lol! <jrand0m>	sorry, jsem zpátky *	nop chytí oslí čepici od hezekiaha *	nop nasazuje si ji na hlavu *	nop tleská jrand0movi *	jrand0m jen sleduje show <jrand0m>	eh... um dobře <hezekiah>	jrand0m: i2p, stav Javy atd. Mluv, chlape! <jrand0m>	takže, k dnešku existuje java klientské API a stub java 	  router, které spolu dokážou mluvit.  Navíc je tu aplikace zvaná 	  ATalk umožňující anonymní IM + přenos souborů. <hezekiah>	Přenos souborů už teď!? <jrand0m>	si sr <hezekiah>	Ty jo. <hezekiah>	Jsem určitě pozadu. <jrand0m>	ale není to zrovna nejpůvabnější <hezekiah>	lol <jrand0m>	vezme soubor a hodí ho do zprávy <hezekiah>	Au. <nop>	jak dlouho trval 1,8 MB lokální přenos? <jrand0m>	Testoval jsem s 4K souborem a 1,8Mb souborem <jrand0m>	pár sekund <nop>	pěkné <nop>	:) <hezekiah>	Umí ty java věci už skutečné šifrování, nebo to pořád 	  předstírá? <nop>	falešné <nop>	to vím i já <nop>	:) <jrand0m>	Zahřál jsem to tím, že jsem nejdřív mluvil sám se 	  sebou [tj. jedno okno s druhým, ahoj], takže se to nemuselo potýkat s režií prvního elg <jrand0m>	jo, je to z velké části fingované <thecrypto>	většina šifrování je falešná <thecrypto>	na tom se ale pracuje <hezekiah>	Jasně. :) <jrand0m>	rozhodně. <jrand0m>	v tomhle ohledu, dáš nám update, thecrypto? <thecrypto>	no, teď mám hotový ElGamal a SHA256 <thecrypto>	teď pracuju na generování prvočísel pro DSA <thecrypto>	Pošlu 5 a pak si prostě jedno vybereme <hezekiah>	nop: Neměl jsi mít prvočísla pro použití s DSA? <thecrypto>	Máme také nějaké benchmarky ElGamalu a SHA256 <thecrypto>	A všechny jsou rychlé <jrand0m>	poslední benchmarky s elg: <jrand0m>	Průměrný čas generování klíče: 4437	celkem: 443759	min: 	  872	   max: 21110	   Generování/sekundu: 0 <jrand0m>	Průměrný čas šifrování    : 356	celkem: 35657	min: 	  431	   max: 611	   Šifrování Bps: 179 <jrand0m>	Průměrný čas dešifrování    : 983	celkem: 98347	min: 	  881	   max: 2143	   Dešifrování Bps: 65

<hezekiah>	min and max: are they in seconds? <jrand0m>	note that the Bps isn't really useful, as we only encrypt/decrypt 	  64 bytes <thecrypto>	ms <jrand0m>	no, sorry, those are all milliseconds <hezekiah>	Cool. :) <hezekiah>	And this is done in java? <thecrypto>	yes <thecrypto>	pure java <hezekiah>	OK. I am officiall impressed. :) <jrand0m>	100%.  P4 1.8 <thecrypto>	they are about the same on my 800 Mhz <hezekiah>	How can I do the same tests? <jrand0m>	sha256 benchmark: <jrand0m>	Short Message Time Average  : 0 total: 0	min: 0	max: 	  0  Bps: NaN <jrand0m>	Medium Message Time Average : 1 total: 130	min: 0	max: 	  10 Bps: 7876923 <jrand0m>	Long Message Time Average   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037 <thecrypto>	run the ElGamalBench program <hezekiah>	OK. <hezekiah>	I'll go find it. <jrand0m>	(short size: ~10 bytes, medium ~10KB, long ~ 1MB) <jrand0m>	java -cp i2p.jar ElGamalBench <jrand0m>	(after running "ant all") <hezekiah>	jrand0m: Thanks. :) <jrand0m>	np <thecrypto>	The NaN thing means it's so fast that we end up dividing by 0 	  it's so fast :) <hezekiah>	What's the sha bench? <jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) has joined #iip-dev <hezekiah>	OK. <jrand0m>	we'll probably want to move those to be main() methods of the 	  associated engines, but they're good where they are atm <hezekiah>	Let's see how fast all this is on an AMD K6-2 333MHz (which is 	  a chip not well know for its integer math.) <jrand0m>	heh <jrand0m>	ok so we have DSA and AES left, right? <jrand0m>	this is all wikked thecrypto.  nice work. <thecrypto>	yup <jrand0m>	can I nag you for an ETA on the other two?  ;) <hezekiah>	If this is anywhere near as fast on my box as it is on yours, 	  you have to show me how you do that. ;-) <thecrypto>	DSA should be done almost as soon as i have primes ready <nop>	hezekiah have you tried the sslcrypto for python <thecrypto>	copying some code around from the prime generator and things like 	  that and it's done <nop>	the one off that link <hezekiah>	nop: sslcrypto won't do us any good. <hezekiah>	nop: It doesn't implment ElGamal _or_ AES _or_ sha256. <thecrypto>	AES is mostly done except that there is some error somewhere that 	  i'm still trying to pick out and destroy, once i have that, it'll be done <jrand0m>	thecrypto> so by friday, DSA keygen, sign, verify, and AES encrypt, 	  decrypt for arbitrary size inputs? <nop>	the one on McNab's site does not? <thecrypto>	yeah <nop>	darn <thecrypto>	should be friday <thecrypto>	most likey thursday <jrand0m>	thecrypto> does that include the UnsignedBigInteger stuff? <thecrypto>	i'll be missing next weeks meeting because of summer camp, and 	  i'll be back after that <thecrypto>	jrand0m: prolly not <jrand0m>	ok. <jrand0m>	so for the time being, interoperability between java and python 	  is b0rked. <jrand0m>	for crypto, that is. ---	Notify: jeremiah is online (anon.iip). -->	jeremiah (~chatzilla@anon.iip) has joined #iip-dev <jrand0m>	(aka for signatures, keys, encryption, and decryption)

<nop>	hmm možná bychom se měli víc zaměřit na C/C++
<thecrypto>	no, až to rozchodíme úplně, můžeme pak zajistit, aby si Java i Python uměly navzájem povídat
<jrand0m>	až budeš pryč, podívám se na věci kolem bezznaménkových typů.
<jeremiah>	může mi někdo poslat historii? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Dej mi minutu. :)
<jrand0m>	nop> máme vývojáře pro C/C++?
<nop>	Mám jednoho člověka, ano
<nop>	a víme, že Hezekiah by to taky zvládl
<jrand0m>	nebo možná můžeme od hezekiaha + jeremiaha získat update stavu vývoje v Pythonu, abychom viděli, kdy budeme mít víc lidí pro vývoj v C/C++
<jrand0m>	jasně, samozřejmě. ale hez+jeremiah teď dělají na pythonu (že?)
<hezekiah>	Jo.
<--	mrflibble se odpojil (Ping timeout)
<hezekiah>	Tak trochu dávám chudákovi jeremiahovi pěkně zabrat.
<nop>	Jen jsem říkal, že pokud python nebude mít vysoké rychlosti
<hezekiah>	Python je hlavně pro mě, abych pochopil tuhle síť.
<nop>	ach
<hezekiah>	Až to v zásadě přiměju držet se kompletní specifikace, chci to předat jeremiahovi, ať s tím naloží, jak uzná za vhodné.
<hezekiah>	Není to zamýšlené jako špičková implementace té specifikace.
<hezekiah>	(Kdybych to chtěl, použil bych C++.)
<jeremiah>	no, pokud si dobře pamatuju, v aplikaci nejsou žádné opravdu procesorově náročné části, kromě kryptografie, a ideálně se to stejně bude řešit v C, že?
<jrand0m>	jasně, jeremiah. Všechno záleží na aplikaci
-->	mrflibble (mrflibble@anon.iip) se připojil k #iip-dev
<hezekiah>	jeremiah: Teoreticky.
<jrand0m>	tak kde jsme na python straně? klientské API, router jen lokálně, atd.?
<jeremiah>	pythoní implementace nám taky ukáže, jaké optimalizace bychom mohli udělat už od začátku... rád bych ji udržoval aktuální, případně pokud to půjde, i napřed před C implementací
<hezekiah>	jrand0m: OK. Tady je, co mám.
<hezekiah>	V _teorii_ by router měl umět zpracovat všechny ne‑admin zprávy od klienta.
<hezekiah>	Jenže ještě nemám klienta, takže jsem to nemohl ladit (tj. pořád jsou tam chyby).
<hezekiah>	Zrovna pracuju na klientovi.
<jrand0m>	'k. když dokážeš vypnout ověřování podpisů, měli bychom proti tomu teď být schopni spustit Java klienta
<hezekiah>	Doufám, že to bude hotové, kromě administrátorských zpráv, za den nebo dva.
<jrand0m>	můžeme to vyzkoušet po schůzce
<hezekiah>	jrand0m: OK.
<jeremiah>	Od poslední schůzky jsem hlavně řešil věci z reálného světa, můžu dělat na klientském API, jen jsem se snažil srovnat se v myšlení s hezekiahem
<jrand0m>	cool
<hezekiah>	jeremiah: Víš co, prostě počkej.
<hezekiah>	jeremiah: Asi na tebe teď házím příliš mnoho nových věcí, než abys to zvládl.
<jeremiah>	hezekiah: jasně, chtěl jsem říct, že bys měl asi prostě pokračovat a implementovat základní věci
<hezekiah>	jeremiah: Za chvilku se to stabilizuje a budeš to moct začít vylepšovat. (Je tam spousta komentářů TODO, se kterými by se hodila pomoc.)
<jeremiah>	a pak to můžu později rozšířit, až si udělám obrázek
<hezekiah>	Přesně tak.
<hezekiah>	Budeš udržovat všechen tenhle kód. :)
<jrand0m>	cool. takže odhad 1–2 týdny na funkční python router + klientské API?
<hezekiah>	Příští týden jedu na dovolenou, takže nejspíš.
<hezekiah>	Budeme mít brzy víc detailů ohledně router–router?
<jrand0m>	ne.
<jrand0m>	no, ano.
<jrand0m>	ale ne.
<hezekiah>	lol
<jeremiah>	hezekiah: na jak dlouho je ta dovolená?
<hezekiah>	1 týden.
<jeremiah>	ok
<jrand0m>	(aka jakmile vyjde SDK, 100 % mého času půjde do I2NP)
<hezekiah>	Doufám, že než odjedu na dovolenou, budu mít napsanou veškerou funkcionalitu mimo admin
<hezekiah>	.
<jrand0m>	ale pak krátce po návratu míříš na vysokou, že?
<hezekiah>	I2NP?
<hezekiah>	Jo.
<jrand0m>	síťový protokol
<hezekiah>	Po dovolené mám asi 1 týden.
<hezekiah>	Pak budu pryč.
<hezekiah>	A můj volný čas spadne jako kámen.
<jrand0m>	takže ten 1 týden by měl být jen ladění
<jeremiah>	Já na kódu můžu dělat i když bude hez pryč
<jrand0m>	jo
<jrand0m>	jak vypadá tvoje léto, jeremiah?
<hezekiah>	jeremiah: Možná bys mohl rozchodit ty admin funkce?

<thecrypto>	mám ještě měsíc poté, co se vrátím z dovolené, abych 	  mohl pracovat na věcech
<jrand0m>	mít život, nebo být jako zbytek z nás lůzrů?  :)
<jeremiah>	možná
<hezekiah>	100sers?
<hezekiah>	Co je to 100ser?
<jeremiah>	odjíždím na vysokou 22., jinak můžu vyvíjet
<mihi>	hezekiah: lůzr
<jeremiah>	a poslední týden před odjezdem budou všichni moji kamarádi pryč... takže 	  můžu přejít do hyper-dev módu
<hezekiah>	mihi: Aha!
<jrand0m>	hehe
<hezekiah>	OK. Tak kde jsme byli v programu?
<hezekiah>	tj. Co je dál?
<jrand0m>	stav SDK
<jrand0m>	SDK == jedna klientská implementace, lokální implementace routeru, aplikace a dokumentace.
<jrand0m>	Rád bych to měl venku do příštího úterý.
<hezekiah>	jeremiah: Ten backlog je na cestě. Promiň, že jsem na tebe zapomněl. :)
<jeremiah>	díky
<jrand0m>	ok, co tu není, takže věci kolem naming service (pojmenovávací služby) jsou asi trochu 	  mimo
<jrand0m>	naming service můžeme probrat, až vydá specifikaci, nebo 	  až bude nablízku
<jrand0m>	ok, to je vše k I2P věcem
<jrand0m>	má ještě někdo něco k I2P, nebo jdeme na:
<nop> 4) Konec s 	  komentáři a tak
<hezekiah>	Nic mě nenapadá.
<jrand0m>	Předpokládám, že všichni viděli 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto>	ne tady
<jrand0m>	(nop to sem dřív postnul)
<hezekiah>	To o tom chlapíkovi, co ho zatkli za odkazování na web o 	  výrobě bomb?
<jrand0m>	jo
<jrand0m>	souvislost s potřebou zprovoznit I2P co nejdřív by měla být zřejmá ;)
<hezekiah>	OK! jeremiah, ty logy jsou teď odeslané.
<jeremiah>	díky
<jrand0m>	má někdo nějaké otázky / komentáře / myšlenky / frisbee, 	  nebo máme rekordně krátkou schůzku?
*	thecrypto hází frisbee <--	logger odešel (vypršení časového limitu pingu)
<jrand0m>	sakra, dneska jste nějak potichu ;)
<mihi>	otázka:
<mihi>	kde mohou nedevelopeři získat váš java kód?
<jrand0m>	si sr?
<thecrypto>	zatím ne
<mihi>	404
<jrand0m>	to zveřejníme, jakmile budeme připraveni na vydání.  tj. 	  zdrojáky půjdou ven spolu se SDK
<jrand0m>	heh
<jrand0m>	jo, nepoužíváme SF
<hezekiah>	nop: Je možné, že někdy zprovozníme anonymní CVS?
<hezekiah>	čas?
<--	mrflibble odešel (vypršení časového limitu pingu)
<nop>	no, otevřel bych nestandardní port
<jrand0m>	hezekiah> budeme to mít, jakmile bude mít kód licenci GPL
<nop>	ale pracuju na viewcvs
<jrand0m>	tj. ne teď, protože GPL dokument zatím do kódu nebyl přidán
<hezekiah>	jrand0m: Je to ve všech adresářích s python kódem a všechny python 	  zdrojové soubory uvádějí licencování pod GPL-2.
<jrand0m>	hezekiah> je to na cathedralu?
<hezekiah>	Ano.
<jrand0m>	aha, jasně.  i2p/core/code/python ?  nebo jiný modul? *	jrand0m to tam ještě neviděl
<hezekiah>	Každý adresář s python kódem v sobě má soubor COPYING s 	  GPL-2 a každý zdrojový soubor má licenci nastavenou na GPL-2
<hezekiah>	Je to v i2p/router/python a i2p/api/python
<jrand0m>	'k
<jrand0m>	takže jo, do příštího úterý budeme mít SDK + veřejný přístup ke zdrojákům.
<hezekiah>	Super.
<hezekiah>	Nebo jak rád říkáš ty, wikked. ;-)
<jrand0m>	heh
<jrand0m>	nada mas?
<hezekiah>	nada mas? Co to znamená!?
<jeremiah>	nic víc
*	jrand0m navrhuje, abys ses na univerzitě naučil trochu španělštiny -->	mrflibble (mrflibble@anon.iip) se připojil k #iip-dev
<hezekiah>	Nějaké otázky?
<hezekiah>	Poprvé!
<--	ptm (~ptm@anon.iip) opustil #iip-dev (ptm)
<hezekiah>	Podruhé!
<--	mrflibble odešel (mr. flibble říká "konec hry, hoši")
<hezekiah>	Mluvte teď... nebo počkejte, až se vám bude chtít mluvit později!
<thecrypto>	dobře, budu ještě víc optimalizovat ElGamal, takže do budoucna 	  čekejte ještě rychlejší ElGamal benchmarky
<jrand0m>	prosím zaměř se na DSA a AES před laděním... prosííím :)
<thecrypto>	udělám to
<hezekiah>	Důvod, proč to dělá, je ten, že zase lidem působím 	  problémy. ;-)
<thecrypto>	dělám DSA prvočísla
-->	mrflibble (mrflibble@anon.iip) se připojil k #iip-dev
<thecrypto>	no, alespoň teď dělám program na generování DSA prvočísel
<hezekiah>	ElGamal v Javě nemá rád AMD K-6 II 333 MHz.
<hezekiah>	OK.
<hezekiah>	Kolo otázek končí!
<jrand0m>	ok hez, hotovo.  chceš si dát poradu ohledně zprovoznění java klienta 	  a práce na python routeru?
<hezekiah>	Uvidíme se příští týden, občané!
*	hezekiah třískne na stůl *baf*erem </div>
