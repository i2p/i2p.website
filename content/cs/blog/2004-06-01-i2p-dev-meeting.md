---
title: "Setkání vývojářů I2P - 1. června 2004"
date: 2004-06-01
author: "duck"
description: "Zápis z vývojářské schůzky I2P ze dne 1. června 2004."
categories: ["meeting"]
---

## Stručné shrnutí

<p class="attendees-inline"><strong>Přítomní:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Záznam ze schůzky

<div class="irc-log"> [22:59] &lt;duck&gt; Tue Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; ahoj všichni! [23:00] &lt;mihi&gt; ahoj duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; můj návrh: [23:00] * Masterboy se připojil k #i2p

[23:00] &lt;duck&gt; 1) pokrok v kódu
[23:00] &lt;duck&gt; 2) vybraný obsah
[23:00] &lt;duck&gt; 3) stav testnetu
[23:00] &lt;duck&gt; 4) odměny
[23:00] &lt;duck&gt; 5) ???
[23:00] &lt;Masterboy&gt; ahoj:)
[23:00] &lt;duck&gt; .
[23:01] &lt;duck&gt; protože je jrandom pryč, budeme to muset udělat sami
[23:01] &lt;duck&gt; (Vím, že loguje a ověřuje naši nezávislost)
[23:01] &lt;Masterboy&gt; žádný problém:P
[23:02] &lt;duck&gt; pokud nejsou s programem problémy, navrhuji, abychom se ho drželi
[23:02] &lt;duck&gt; i když s tím moc nenadělám, když se ho držet nebudete :)
[23:02] &lt;duck&gt; .
[23:02] &lt;mihi&gt; ;)
[23:02] &lt;duck&gt; 1) pokrok v kódu
[23:02] &lt;duck&gt; do cvs nebylo odesláno moc kódu
[23:02] &lt;duck&gt; tento týden jsem vyhrál trofej: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus ještě nemá cvs účet
[23:03] &lt;Masterboy&gt; a kdo něco odeslal?
[23:03] &lt;duck&gt; dělá někdo nějaké tajné programování?
[23:03] * Nightblade se připojil k #I2P

[23:03] &lt;hypercubus&gt; BrianR pracoval na nějakých věcech
[23:04] &lt;hypercubus&gt; mám možná 20 % instalátoru 0.4 nabastlených
[23:04] &lt;duck&gt; hypercubus: jestli něco máš, tak pošli diffy a $dev to za tebe commitne
[23:04] &lt;duck&gt; samozřejmě platí přísné licenční podmínky
[23:05] &lt;duck&gt; hypercubus: super, nějaké problémy / věci hodné zmínky?
[23:06] &lt;hypercubus&gt; zatím ne, ale budu asi potřebovat pár lidí z BSD, aby otestovali shell skripty předinstalátoru
[23:06] * duck obrací pár kamenů
[23:06] &lt;Nightblade&gt; je to čistě textové
[23:07] &lt;mihi&gt; duck: který z nich jsi na duck_trophy.jpg?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk má freebsd, taky můj ISP má freebsd, ale jejich konfigurace je tak trochu rozbitá
[23:07] &lt;Nightblade&gt; myslím můj webhostingový ISP, ne Comcast
[23:08] &lt;duck&gt; mihi: ten vlevo s brýlemi. wilde je ten vpravo, co mi podává trofej
[23:08] * wilde mává
[23:08] &lt;hypercubus&gt; máš na výběr... pokud máš nainstalovanou javu, můžeš předinstalátor úplně přeskočit...    pokud javu nainstalovanou nemáš, můžeš spustit linuxový binární nebo win32 binární předinstalátor (konzolový režim), nebo    generický *nix skriptový předinstalátor (konzolový režim)
[23:08] &lt;hypercubus&gt; hlavní instalátor ti dává na výběr mezi konzolovým režimem a pěkným GUI režimem
[23:08] &lt;Masterboy&gt; brzy nainstaluju freebsd, takže časem zkusím i ten instalátor
[23:09] &lt;hypercubus&gt; ok, dobré... nevěděl jsem, jestli to používá někdo jiný než jrandom
[23:09] &lt;Nightblade&gt; na freebsd se java spouští jako "javavm" spíš než "java"
[23:09] &lt;hypercubus&gt; postavená ze zdrojů od Sunu?
[23:09] &lt;mihi&gt; freebsd podporuje symbolické odkazy ;)
[23:10] &lt;hypercubus&gt; každopádně binární předinstalátor je hotový na 100 %
[23:10] &lt;hypercubus&gt; kompiluje se gcj do nativního kódu
[23:11] &lt;hypercubus&gt; jen se zeptá na instalační adresář a stáhne ti JRE
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; cool
[23:11] &lt;hypercubus&gt; jrandom balí vlastní JRE pro i2p

[23:12] <deer> <j> .
[23:12] <Nightblade> pokud nainstaluješ Javu z freebsd ports collection, používáš nějaký wrapper skript nazvaný    javavm
[23:12] <deer> <r> .
[23:12] <hypercubus> každopádně tahle věc bude téměř úplně automatizovaná
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <duck> r: nech toho
[23:12] <deer> <r> .
[23:12] <deer> <m> .
[23:13] <deer> <m> pitomej IRC server, nepodporuje pipelining :(
[23:13] <duck> hypercubus: máš pro nás nějaké ETA?
[23:14] <deer> <m> ups, problém je "Nick change too fast" :(
[23:14] <hypercubus> pořád očekávám, že budu hotový do méně než měsíce, dřív než 0.4 dozraje k vydání
[23:14] <hypercubus> ale momentálně kompiluju nový OS pro svůj vývojový systém, takže to potrvá pár dní    než se vrátím k instalátoru ;-)
[23:14] <hypercubus> ale nebojte
[23:15] <duck> ok. takže příští týden další novinky :)
[23:15] <duck> nějaké další kódování hotové?
[23:15] <hypercubus> snad... pokud mě zase nepodělá dodavatel elektřiny
[23:16] * duck se přesouvá na #2
[23:16] <duck> * 2) doporučený obsah
[23:16] <duck> tento týden spousta streamovaného audia (ogg/vorbis)
[23:16] <duck> baffled provozuje svůj egoplay stream a já provozuju stream taky
[23:16] <Masterboy> a funguje to docela dobře
[23:17] <duck> na našem webu najdete informace, jak to používat
[23:17] <hypercubus> máš pro nás nějaké hrubé statistiky?
[23:17] <duck> pokud používáte přehrávač, který tam není uveden, a přijdete na to, jak ho použít, pošlete mi je a já je    doplním
[23:17] <Masterboy> ducku, kde je na tvém webu odkaz na stream od baffleda?
[23:17] <Masterboy> :P
[23:17] <duck> hypercubus: 4kB/s jde docela dobře
[23:18] <duck> a s ogg to není zas taaak špatné
[23:18] <hypercubus> ale pořád se zdá, že to je průměrná rychlost?
[23:18] <duck> moje pozorování je, že to je maximum
[23:18] <duck> ale je to celé o ladění konfigurace
[23:19] <hypercubus> nějaký nápad, proč se zdá, že to je maximum?
[23:19] <hypercubus> a nemluvím tu jen o streamování
[23:19] <hypercubus> ale i o stahování
[23:20] <Nightblade> včera jsem stahoval nějaké větší soubory (pár megabajtů) z duckovy hostingové    služby a taky jsem měl tak 4kb–5kb
[23:20] <duck> myslím, že je to rtt
[23:20] <Nightblade> ty Chips filmy
[23:20] <hypercubus> 4–5 se zdá být zlepšení oproti ~3, které jsem dostával konzistentně od té doby, co používám i2p

[23:20] &lt;Masterboy&gt; 4-5kb není špatné..
[23:20] &lt;duck&gt; s windowsize 1 se moc nezrychlíš..
[23:20] &lt;duck&gt; windowsize&gt;1 odměna: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: možná k tomu můžeš něco říct?
[23:21] &lt;hypercubus&gt; ale je to pozoruhodně stabilních 3 kbps
[23:21] &lt;mihi&gt; na čem? windowsize&gt;1 s ministreamingem: jsi kouzelník, jestli se ti to podaří ;)
[23:21] &lt;hypercubus&gt; žádné výkyvy na ukazateli šířky pásma... poměrně hladká křivka
[23:21] &lt;duck&gt; mihi: proč je to tak stabilní na 4kb/s
[23:21] &lt;mihi&gt; nemám tušení. nic neslyším :(
[23:22] &lt;duck&gt; mihi: u všech přenosů přes i2ptunnel
[23:22] &lt;Masterboy&gt; mihi, musíš nakonfigurovat ogg streaming plugin..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; ne, uvnitř i2ptunnel není žádné omezení rychlosti. musí to být v routeru...
[23:23] &lt;duck&gt; můj odhad: max velikost paketu: 32kB, 5 sekund rtt: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; zní to pravděpodobně
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; další obsah:
[23:25] * hirvox se připojil k #i2p

[23:25] &lt;duck&gt; je nový eepsite od Naughtious
[23:25] &lt;duck&gt; anonynanny.i2p
[23:25] &lt;duck&gt; klíč je commitnutý do CVS a dal ho na Ughův wiki
[23:25] * mihi slyší "sitting in the ..." - duck++
[23:25] &lt;Nightblade&gt; zkus otevřít dva nebo tři streamy rychlostí 4 kb, pak budeš moct říct, jestli je to    v routeru nebo ve streaming lib (knihovna pro streamování)
[23:26] &lt;duck&gt; Naughtious: jsi tam? řekni něco o svém plánu :)
[23:26] &lt;Masterboy&gt; četl jsem, že poskytuje hosting
[23:26] &lt;duck&gt; Nightblade: zkusil jsem 3 paralelní stahování z baffled a dostával jsem 3–4 kB na každé
[23:26] &lt;Nightblade&gt; aha
[23:27] &lt;mihi&gt; Nightblade: jak to pak poznáš?
[23:27] * mihi má rád poslech v "stop&go" režimu ;)
[23:27] &lt;Nightblade&gt; no, jestli je v routeru nějaké omezení, které mu dovolí najednou obsloužit jen 4 kb
[23:27] &lt;Nightblade&gt; nebo jestli je to něco jiného
[23:28] &lt;hypercubus&gt; může někdo vysvětlit ten anonynanny web? momentálně mi neběží i2p router
[23:28] &lt;mihi&gt; hypercubus: jen wiki nebo něco takového
[23:28] &lt;duck&gt; instalace Plone CMS, otevřená registrace účtů
[23:28] &lt;duck&gt; umožňuje nahrávání souborů a věci kolem webu
[23:28] &lt;duck&gt; přes webové rozhraní
[23:28] &lt;Nightblade&gt; další věc by byla otestovat propustnost "repliable datagramu", který je pokud vím    stejný jako streamy, ale bez ACKů
[23:28] &lt;duck&gt; nejspíš hodně jako Drupal
[23:28] &lt;hypercubus&gt; jo, Plone jsem už provozoval
[23:29] &lt;duck&gt; Nightblade: přemýšlel jsem o použití Airhooku na jejich správu
[23:29] &lt;duck&gt; ale zatím jen základní úvaha
[23:29] &lt;hypercubus&gt; je obsah wiki libovolný, nebo se to zaměřuje na něco konkrétního?
[23:29] &lt;Nightblade&gt; myslím, že Airhook je pod GPL
[23:29] &lt;duck&gt; protokol
[23:29] &lt;duck&gt; ne kód
[23:29] &lt;Nightblade&gt; aha :)
[23:30] &lt;duck&gt; hypercubus: chce kvalitní obsah a umožní ti ho poskytovat :)
[23:30] &lt;Masterboy&gt; nahraj ten nejlepší pr0n sám sebe, co máš, hypere ;P
[23:30] &lt;duck&gt; ok
[23:30] * Masterboy se o to taky pokusí
[23:30] &lt;hypercubus&gt; jo, kdokoli provozuje otevřený wiki, si přímo říká o kvalitní obsah ;-)
[23:31] &lt;duck&gt; ok
[23:31] * duck přechází k #3
[23:31] &lt;duck&gt; * 3) stav testnetu
[23:31] &lt;Nightblade&gt; Airhook elegantně zvládá přerušované, nespolehlivé nebo zpožděné sítě  &lt;-- hehe, ne zrovna    optimistický popis I2P!
[23:31] &lt;duck&gt; jak to šlo?
[23:32] &lt;duck&gt; pojďme diskuzi o datagramu přes i2p nechat až na konec
[23:32] &lt;tessier&gt; rád běhám po otevřených wiki a odkazuju na tohle: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] &lt;tessier&gt; Airhook je boží
[23:32] &lt;tessier&gt; Díval jsem se na něj i kvůli stavbě p2p sítě.
[23:32] &lt;Nightblade&gt; přijde mi to spolehlivé (#3)
[23:32] &lt;Nightblade&gt; nejlepší, co jsem zatím viděl
[23:33] &lt;duck&gt; jo
[23:33] &lt;mihi&gt; funguje dobře - aspoň pro stop&go audio streamování
[23:33] &lt;duck&gt; na IRC vidím docela působivé uptimy
[23:33] &lt;hypercubus&gt; souhlas... vidím mnohem víc modrých "chlápků" v mé konzoli routeru
[23:33] &lt;Nightblade&gt; mihi: posloucháš techno? :)
[23:33] &lt;duck&gt; ale těžko říct, protože se zdá, že bogobot nezvládá spojení, která přejdou přes 00:00
[23:33] &lt;tessier&gt; audio streamování mi funguje skvěle, ale načítání webů často vyžaduje víc pokusů
[23:33] &lt;Masterboy&gt; mám dojem, že i2p běží velmi dobře po 6 hodinách používání; v 6. hodině jsem použil IRC    7 hodin a tak můj router běžel 13 hodin
[23:33] &lt;duck&gt; (*nápověda*)
[23:34] &lt;hypercubus&gt; duck: eh... heheh
[23:34] &lt;hypercubus&gt; to bych asi mohl opravit
[23:34] &lt;hypercubus&gt; máš logování nastavené na denní?
[23:34] &lt;duck&gt; hypercubus++
[23:34] &lt;hypercubus&gt; myslím rotaci logů
[23:34] &lt;duck&gt; jo, ano
[23:34] &lt;duck&gt; duck--
[23:34] &lt;hypercubus&gt; proto
[23:34] &lt;Nightblade&gt; byl jsem celý den v práci, zapnul počítač, spustil i2p a během pár minut jsem byl na duckově IRC serveru
    vdk pár minut
[23:35] &lt;duck&gt; vidím nějaké divné DNFy
[23:35] &lt;duck&gt; i při připojování na mé vlastní eepsites
[23:35] &lt;duck&gt; (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] &lt;duck&gt; myslím, že tohle teď způsobuje většinu problémů
[23:35] &lt;hypercubus&gt; bogoparser analyzuje jen uptimy, které proběhnou celé v rámci jednoho log souboru... takže pokud    log soubor pokrývá jen 24 hodin, nikdo se neukáže jako připojený déle než 24 hodin
[23:35] &lt;duck&gt; Masterboy a ughabugha to myslím měli taky...
[23:36] &lt;Masterboy&gt; jo
[23:36] &lt;duck&gt; (oprav to a příští týden vyhraješ trofej na jistotu!)
[23:37] &lt;deer&gt; &lt;mihi&gt; bogobot je nadšený? ;)
[23:37] &lt;Masterboy&gt; zkusil jsem svůj web a někdy když dám refresh, vezme to jinou trasu? a musím    čekat, než se to načte, ale nikdy nečekám ;P zmáčknu to znovu a ukáže se to hned
[23:37] &lt;deer&gt; &lt;mihi&gt; ups, sry. zapomněl jsem, že je to gated...
[23:38] &lt;duck&gt; Masterboy: dělají time-outy 61 sekund?
[23:39] &lt;duck&gt; mihi: bogobot je teď nastaven na týdenní rotace
[23:39] * mihi opustil IRC ("ahoj a ať se vám setkání vydaří")
[23:40] &lt;Masterboy&gt; promiň, nezkontroloval jsem to; na svém webu když se k němu hned nedostanu, prostě dám refresh    a načte se to okamžitě..
[23:40] &lt;duck&gt; hm
[23:40] &lt;duck&gt; no, je potřeba to opravit
[23:41] &lt;duck&gt; .... #4
[23:41] &lt;Masterboy&gt; myslím, že trasa není pokaždé stejná
[23:41] &lt;duck&gt; * 4) odměny
[23:41] &lt;duck&gt; Masterboy: lokální spojení by měla být zkrácená
[23:42] &lt;duck&gt; wilde měl nějaké nápady ohledně odměn... jsi tu?
[23:42] &lt;Masterboy&gt; možná je to bug ve výběru peerů
[23:42] &lt;wilde&gt; nejsem si jistý, že to bylo do programu, upřímně
[23:42] &lt;duck&gt; oh
[23:42] &lt;wilde&gt; ok, ale myšlenky byly asi takové:
[23:42] &lt;Masterboy&gt; myslím, že až půjdeme ven, systém odměn bude fungovat líp
[23:43] &lt;Nightblade&gt; masterboy: ano, pro každé spojení jsou dva tunnels, aspoň tak to chápu z čtení router.config
[23:43] &lt;wilde&gt; mohli bychom tenhle měsíc udělat menší propagaci i2p a trochu navýšit fond odměn
[23:43] &lt;Masterboy&gt; vidím, že projekt Mute jde dobře - dostali 600 $ a zatím toho moc nenakódovali ;P
[23:44] &lt;wilde&gt; zaměřit se na komunity kolem svobody, kryptografy apod.
[23:44] &lt;Nightblade&gt; nemyslím si, že jrandom chce reklamu
[23:44] &lt;wilde&gt; ne veřejnou pozornost ve stylu Slashdotu, ne
[23:44] &lt;hypercubus&gt; to jsem pozoroval taky
[23:44] &lt;Masterboy&gt; chci to znovu popohnat - až půjdeme veřejně ven, systém bude fungovat mnohem líp ;P
[23:45] &lt;wilde&gt; Masterboy: odměny by třeba mohly urychlit vývoj myi2p
[23:45] &lt;Masterboy&gt; a jak řekl jr, žádná veřejnost do 1.0 a jen trocha pozornosti po 0.4
[23:45] &lt;Masterboy&gt; *psal
[23:46] &lt;wilde&gt; když budeme mít třeba 500+ $ za odměnu, lidi by z toho mohli pár týdnů reálně žít
[23:46] &lt;hypercubus&gt; háček je v tom, že i když zacílíme na malou vývojářskou komunitu, jako třeba *ehm* vývojáře Mute, ti    kluci by o i2p mohli šířit slovo dál, než by se nám líbilo
[23:46] &lt;Nightblade&gt; někdo by si opravováním bugů v i2p mohl udělat kariéru
[23:46] &lt;hypercubus&gt; a příliš brzy
[23:46] &lt;wilde&gt; odkazy na i2p už jsou na mnoha veřejných místech
[23:46] &lt;Masterboy&gt; když dáš google, i2p najdeš

[23:47] <hypercubus> obskurní veřejná místa ;-) (viděl jsem ten i2p odkaz na freesite... mám štěstí, že se ta zatracená freesite vůbec načetla!)
[23:47] <wilde> http://en.wikipedia.org/wiki/I2p
[23:47] <Masterboy> ale souhlasím, že žádná propagace, dokud nebude hotová 0.4
[23:47] <Masterboy> co???????
[23:47] <wilde> http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] <Masterboy> protol0l odvádí skvělou práci ;P
[23:48] <Masterboy> ;))))))
[23:48] <hypercubus> pěkný překlep ;-)
[23:48] <wilde> ok, každopádně souhlasím, že bychom měli I2P zatím držet v soukromí (jr, přečti si tenhle log ;)
[23:49] <Masterboy> kdo to udělal?
[23:49] <Masterboy> myslím, že diskuse týmu Freenet přitáhla víc pozornosti..
[23:50] <Masterboy> a jr, který diskutuje s toadem, dává široké veřejnosti spoustu informací..
[23:50] <Masterboy> takže stejně jako v ughas wiki – za to můžeme všichni obvinit jr ;P
[23:50] <wilde> ok, každopádně uvidíme, jestli dokážeme přitáhnout nějaké $, aniž bychom přitáhli /.
[23:50] <Masterboy> souhlas
[23:50] <hypercubus> mailinglist vývojářů Freenet rozhodně nenazývám „širokou veřejností“ ;-)
[23:50] <wilde> .
[23:51] <hypercubus> wilde: budeš mít spoustu $ dřív, než si myslíš ;-)
[23:51] <wilde> ale no tak, i moje máma odebírá freenet-devl
[23:51] <duck> moje máma to čte přes gmame
[23:51] <deer> <clayboy> freenet-devl se tady vyučuje ve školách
[23:52] <wilde> .
[23:52] <Masterboy> takže uvidíme víc odměn, až půjdeme na stabilní 0.4..
[23:53] <Masterboy> to bude za 2 měsíce ;P
[23:53] <wilde> kam se poděl ten duck?
[23:53] <duck> díky, wilde
[23:53] <hypercubus> i tak, jako dosud jediný žadatel o odměnu musím říct, že peníze za odměnu neměly žádný vliv na moje rozhodnutí tu výzvu přijmout
[23:54] <wilde> hehe, měly by, kdyby to bylo 100×
[23:54] <duck> jsi na tenhle svět až moc dobrý
[23:54] <Nightblade> haha
[23:54] * duck se přesouvá na #5
[23:54] <hypercubus> wilde, $100 pro mě neznamená ani hovno ;-)
[23:54] <duck> 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] <duck> tessier: máš s tím nějaké zkušenosti z praxe
[23:55] <duck> (http://www.airhook.org/)
[23:55] * Masterboy to zkusí :P
[23:56] <duck> implementace v Javě (nevím, jestli to vůbec funguje) http://cvs.ofb.net/airhook-j/
[23:56] <duck> implementace v Pythonu (bordel, dřív to fungovalo) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck otevírá ventil na výlevy
[23:58] <Nightblade> ta v Javě je taky pod GPL
[23:58] <duck> portněte to na pubdomain
[23:58] <hypercubus> amen
[23:58] <Nightblade> celá dokumentace protokolu má jen asi 3 stránky – nemůže to být tak těžké
[23:59] <Masterboy> nic není těžké
[23:59] <Masterboy> jen to není snadné
[23:59] <duck> nemyslím si ale, že je to plně specifikované
[23:59] * hypercubus bere masterboyovi koláčky štěstí
[23:59] <duck> možná se budeš muset ponořit do C kódu kvůli referenční implementaci
[00:00] <Nightblade> udělal bych to sám, ale teď jsem zaneprázdněný jinými i2p věcmi
[00:00] <Nightblade> (a taky svou prací na plný úvazek)
[00:00] <hypercubus> duck: možná na to vypsat odměnu?
[00:00] <Nightblade> už je
[00:00] <Masterboy> ?
[00:00] <Masterboy> ahh Pseudonyms
[00:00] <duck> dalo by se to použít na 2 úrovních
[00:00] <duck> 1) jako transport vedle TCP
[00:01] <duck> 2) jako protokol pro zpracování datagramů uvnitř i2cp/sam
[00:01] <hypercubus> to si pak zaslouží vážné zvážení
[00:01] <hypercubus> </obvious>

[00:02] &lt;Nightblade&gt; duck: všiml jsem si, že repliable datagram (datagram s možností odpovědi) v SAM má maximální velikost 31kb, zatímco    stream má maximální velikost 32kb - což mě vede k myšlence, že destination odesílatele (I2P adresa) se posílá s každým paketem v    režimu repliable datagram, a u stream režimu jen na začátku - 
[00:02] &lt;Masterboy&gt; no, airhook cvs není moc aktuální..
[00:03] &lt;Nightblade&gt; což mě vede k názoru, že by bylo neefektivní stavět protokol nad repliable    datagrams přes sam
[00:03] &lt;duck&gt; velikost zprávy airhooku je 256 bajtů, u i2cp je to 32kb, takže budeš muset aspoň něco změnit
[00:04] &lt;Nightblade&gt; vlastně, pokud bys ten protokol chtěl dělat v SAM, mohl bys prostě použít anonymní datagram    a zajistit, aby první paket obsahoval destination odesílatele.... bla bla bla - mám spoustu nápadů, ale nemám    dost času je napsat
[00:06] &lt;duck&gt; zase na druhou stranu budeš mít problémy s ověřováním podpisů
[00:06] &lt;duck&gt; takže ti někdo může posílat falešné pakety
[00:06] &lt;Masterboy&gt; téma:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; pravda
[00:08] &lt;Nightblade&gt; ale kdybys poslal odpověď na tu destination a nepřišlo žádné potvrzení, věděl bys, že je to    podvrh
[00:08] &lt;Nightblade&gt; musel by tam být handshake
[00:08] &lt;duck&gt; ale budeš na to potřebovat handshaky na aplikační úrovni
[00:08] &lt;Nightblade&gt; ne, vlastně ne
[00:09] &lt;Nightblade&gt; prostě to dát do knihovny pro přístup k SAM
[00:09] &lt;Nightblade&gt; to je ale špatný způsob, jak to dělat
[00:09] &lt;Nightblade&gt; dělat to tak
[00:09] &lt;duck&gt; mohl bys také použít oddělené tunnels
[00:09] &lt;Nightblade&gt; mělo by to být ve streaming lib
[00:11] &lt;duck&gt; jo. dává to smysl
[00:12] &lt;duck&gt; ok
[00:12] &lt;duck&gt; připadám si nějak *baff*-ně
[00:13] &lt;Nightblade&gt; jo
[00:13] * duck *baffs* </div>
