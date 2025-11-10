---
title: "Poznámky ke stavu I2P k 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Analýza výkonu sítě, zkoumání úzkého hrdla CPU, plánování vydání Syndie 1.0 a vyhodnocení distribuované správy verzí"
categories: ["status"]
---

Ahoj všichni, tento týden opožděné poznámky ke stavu

* Index

1) Stav sítě 2) Stav vývoje pro router 3) Odůvodnění Syndie (pokračování) 4) Stav vývoje Syndie 5) Distribuovaný systém správy verzí 6) ???

* 1) Net status

V uplynulém týdnu či dvou byla situace na irc a dalších službách poměrně stabilní, i když dev.i2p/squid.i2p/www.i2p/cvs.i2p zaznamenaly několik potíží (kvůli dočasným problémům souvisejícím s operačním systémem). Zdá se, že je momentálně vše v ustáleném stavu.

* 2) Router dev status

Na druhé straně diskuse o Syndie stojí otázka "takže, co to znamená pro router?", a abych na ni odpověděl, dovolte mi stručně vysvětlit, kde se vývoj routeru nachází právě teď.

Celkově vzato podle mého názoru to, co brání routeru dosáhnout verze 1.0, není jeho anonymita, ale výkon. Jistě, existují oblasti anonymity, které lze zlepšit, ale i když na anonymní síť dosahujeme poměrně dobrého výkonu, náš výkon nestačí pro širší použití. Navíc zlepšení anonymity sítě nezlepší její výkon (ve většině případů, které mě napadají, zlepšení anonymity snižuje propustnost a zvyšuje latenci). Nejprve musíme vyřešit problémy s výkonem, protože pokud je výkon nedostatečný, je nedostatečný celý systém, bez ohledu na to, jak silné jsou jeho anonymizační techniky.

Tak co brzdí náš výkon? Kupodivu se zdá, že je to naše využití CPU. Než se pustíme do přesných důvodů, nejprve trochu pozadí.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Proto potřebujeme úrovně routers - některé globálně dosažitelné s vysokými limity šířky pásma (tier A), některé ne (tier B). To už je fakticky implementováno prostřednictvím informací o kapacitě v netDb a k době před dnem či dvěma byl poměr tier B k tier A přibližně 3 ku 1 (93 routers s cap L, M, N nebo O a 278 s cap K).

Nyní jsou v zásadě v tieru A dva omezené zdroje, které je třeba spravovat - šířka pásma a CPU. Šířku pásma lze řídit obvyklými prostředky (rozložit zátěž napříč širokým okruhem peerů, nechat některé peery zvládat extrémní objemy [např. ty na T3s], a odmítat nebo omezovat jednotlivé tunnels a spojení).

Správa využití CPU je obtížnější. Hlavní úzké hrdlo CPU pozorované na routers úrovně A je dešifrování požadavků na sestavení tunnel. Velké routers mohou být (a jsou) touto činností zcela vytíženy - například, dlouhodobý průměrný čas dešifrování tunnel na jednom z mých routers je 225ms, a dlouhodobá *průměrná* frekvence dešifrování požadavků na tunnel je 254 událostí za 60 sekund, tedy 4.2 za sekundu. Když tyto dvě hodnoty jednoduše vynásobíme, vychází, že 95% CPU je spotřebováno samotným dešifrováním požadavků na tunnel (a to nebere v úvahu špičky v počtech událostí). Ten router se přesto nějak dokáže současně účastnit 4-6000 tunnels, přičemž přijímá přibližně 80% dešifrovaných požadavků.

Bohužel, protože je CPU toho routeru tak silně zatíženo, musí zahazovat značný počet požadavků na sestavení tunnelu ještě dřív, než je vůbec možné je dešifrovat (jinak by požadavky čekaly ve frontě tak dlouho, že i kdyby byly přijaty, původní žadatel by je tak jako tak považoval za ztracené nebo za příliš přetížené na to, aby s nimi šlo cokoli dělat). V tomto světle vypadá 80% míra přijetí toho routeru mnohem hůř - za dobu své existence dešifroval kolem 250k požadavků (což znamená, že přijal zhruba 200k), ale ve frontě pro dešifrování musel kvůli přetížení CPU zahodit asi 430k požadavků (čímž se ta 80% míra přijetí mění na 30%).

Řešení se zdají vést ke snížení relevantní výpočetní náročnosti na CPU při dešifrování požadavků na tunnel. Pokud snížíme čas CPU o jeden řád, výrazně by to zvýšilo kapacitu routeru úrovně A, čímž by se snížil počet odmítnutí (jak explicitních, tak implicitních, kvůli zahazovaným požadavkům). To by zase zvýšilo míru úspěšnosti sestavování tunnelů, čímž by se snížila četnost vypršení platnosti lease, což by pak snížilo zátěž šířky pásma v síti způsobenou opětovným sestavováním tunnelů.

Jednou z metod, jak toho dosáhnout, by bylo změnit požadavky na vytvoření tunnelu z používání 2048bitového Elgamal na, řekněme, 1024bitový nebo 768bitový. Problém je ale v tom, že pokud prolomíte šifrování u zprávy s požadavkem na vytvoření tunnelu, znáte celou cestu tunnelu. I kdybychom se touto cestou vydali, kolik by nám to ve skutečnosti přineslo? Zlepšení doby dešifrování o jeden řád by mohlo být smeteno nárůstem o jeden řád v poměru úrovně B k úrovni A (aka problém černých pasažérů), a pak bychom uvízli, protože není možné přejít na 512bitový nebo 256bitový Elgamal (a ještě se po tom podívat do zrcadla ;)

Jednou z alternativ by bylo použít slabší kryptografii, ale zrušit ochranu proti útokům založeným na počítání paketů, kterou jsme zavedli s novým procesem sestavování tunnelu. To by nám umožnilo používat zcela efemérní vyjednané klíče v Toru podobném teleskopickém tunnelu (to by však opět vystavilo tvůrce tunnelu triviálním pasivním útokům založeným na počítání paketů, které identifikují službu).

Další myšlenkou je zveřejňovat a používat ještě detailnější údaje o zatížení v netDb, což klientům umožní přesněji rozpoznat situace, jako je ta výše uvedená, kdy router s vysokou propustností zahazuje 60 % zpráv s požadavky na tunnel, aniž by se na ně vůbec podíval. Existuje několik experimentů, které stojí za to tímto směrem provést, a lze je realizovat s plnou zpětnou kompatibilitou, takže bychom se jich měli brzy dočkat.

Takže to je to úzké hrdlo v routeru/síti, jak to dnes vidím. Jakékoli a veškeré návrhy, jak se s tím vypořádat, velmi oceníme.

* 3) Syndie rationale continued

Na fóru je obsáhlý příspěvek o Syndie a o tom, jak do toho zapadá - podívejte se na něj na <http://forum.i2p.net/viewtopic.php?t=1910>

Také bych rád vyzdvihl dva úryvky z dokumentace k Syndie, na které se pracuje. Nejprve z irc (a z dosud nezveřejněného FAQ):

<bar> otázka, nad kterou přemýšlím, je: kdo bude mít později        koule dost velké na to hostovat produkční servery/archivy Syndie?  <bar> nebudou stejně snadno dohledatelné jako eepsites(I2P Sites)        jsou dnes?  <jrandom> veřejné archivy Syndie nemají možnost        *číst* obsah zveřejněný na fórech, pokud fóra nezveřejní        klíče, které to umožní  <jrandom> a podívej se na druhý odstavec usecases.html  <jrandom> samozřejmě ti, kdo hostují archivy, pokud dostanou        zákonný příkaz odstranit fórum, to pravděpodobně udělají  <jrandom> (ale pak se lidé mohou přesunout do jiného        archivu, aniž by narušili provoz fóra)  <void> jo, měl bys zmínit, že migrace na        jiné médium bude bezproblémová  <bar> když se můj archiv zavře, můžu nahrát celé své fórum do nového        archivu, že?  <jrandom> přesně tak, bar  <void> během migrace můžou používat obě metody současně  <void> a kdokoli je schopný ta média synchronizovat  <jrandom> přesně tak, void

Příslušná sekce v (dosud nezveřejněném) souboru Syndie usecases.html je:

Zatímco mnoho různých skupin často chce organizovat diskuse do   online fóra, centralizovaná povaha tradičních fór   (webové stránky, BBS, atd.) může být problém. Například lze web   hostující fórum odstavit z provozu prostřednictvím útoků typu denial of service (odmítnutí služby)   nebo administrativním zásahem. Kromě toho jediný hostitel   představuje snadný bod ke sledování aktivity skupiny, takže i   když je fórum pseudonymní, tyto pseudonymy lze spojit s IP   adresou, která odeslala nebo četla jednotlivé zprávy.

Navíc, nejenže jsou fóra decentralizovaná, jsou organizována ad‑hoc způsobem, přesto jsou plně kompatibilní s jinými způsoby organizace. To znamená, že nějaká malá skupina lidí může provozovat své fórum pomocí jedné techniky (šíření zpráv jejich vkládáním na wiki), jiná může provozovat své fórum pomocí jiné techniky (zveřejňováním svých zpráv v distribuované hashovací tabulce, jako je OpenDHT, přesto pokud si je jeden člověk vědom obou technik, může ta dvě fóra navzájem synchronizovat. To umožní lidem, kteří si byli vědomi pouze wiki, komunikovat s lidmi, kteří si byli vědomi pouze služby OpenDHT, aniž by o sobě cokoli věděli. A ještě dál, Syndie umožňuje jednotlivým buňkám kontrolovat vlastní viditelnost při komunikaci napříč celou organizací.

* 4) Syndie dev status

V poslední době jsme u Syndie zaznamenali spoustu pokroku; účastníkům na IRC kanálu jsme rozdali 7 alfa verzí. Většina zásadních problémů ve skriptovatelném rozhraní byla vyřešena a doufám, že se nám podaří vydat Syndie 1.0 ještě tento měsíc.

Řekl jsem právě "1.0"? To si pište! Ačkoli Syndie 1.0 bude textová aplikace a svou použitelností se ani nebude moci srovnávat s jinými srovnatelnými textovými aplikacemi (například mutt nebo tin), nabídne kompletní škálu funkcí, umožní použít strategie syndikace založené na HTTP i souborech a, doufejme, ukáže potenciálním vývojářům schopnosti Syndie.

Právě teď mám předběžně naplánované vydání Syndie 1.1 (umožňující lidem lépe si uspořádat své archivy a čtenářské návyky) a možná i verzi 1.2, která integruje některé vyhledávací funkce (jak jednoduché vyhledávání, tak možná i fulltextové vyhledávání Lucene). Syndie 2.0 bude pravděpodobně první vydání s GUI (grafickým uživatelským rozhraním), přičemž zásuvný modul pro prohlížeč bude součástí verze 3.0. Podpora dalších archivů a sítí pro distribuci zpráv bude samozřejmě přibývat, jakmile budou implementovány (freenet, mixminion/mixmaster/smtp, opendht, gnutella atd.).

Uvědomuji si však, že Syndie 1.0 nebude tak přelomová, jak by si někteří přáli, protože textové aplikace jsou skutečně spíše pro geeky, ale rád bych se pokusil odnaučit nás zvyku nahlížet na "1.0" jako na finální vydání a místo toho ji vnímat jako začátek.

* 5) Distributed version control

Doposud se nějak prokousávám subversion jako systémem pro správu verzí pro Syndie, i když ve skutečnosti jsem opravdu zběhlý jen v CVS a clearcase. Je to proto, že jsem většinu času offline, a i když jsem online, vytáčené připojení je pomalé, takže lokální diff/revert/etc v subversion se docela hodil. Každopádně mě včera void pošťouchl s návrhem, abychom se místo toho podívali na některý z distribuovaných systémů.

Díval jsem se na ně před pár lety, když jsem zvažoval VCS (systém správy verzí) pro I2P, ale zavrhl jsem je, protože jsem nepotřeboval jejich offline funkcionalitu (tehdy jsem měl dobré připojení k internetu), takže se je učit nestálo za to. To už neplatí, takže se na ně teď dívám o něco podrobněji.

- From what I can see, darcs, monotone, and codeville are the top

Z kandidátů se verzovací systém darcs založený na patchech jeví obzvlášť atraktivně. Například mohu veškerou práci dělat lokálně a jen přes scp nahrát gzipované a gpgované rozdíly do adresáře Apache na dev.i2p.net, a lidé mohou přispívat vlastními změnami nahráním svých gzipovaných a gpgovaných rozdílů na místa dle vlastního výběru. Až přijde čas otagovat vydání, vytvořil bych darcs diff, který určuje sadu patchů obsažených ve vydání, a ten .gz/.gpg diff nahrál stejně jako ostatní (a samozřejmě také zveřejnit skutečné soubory tar.bz2, .exe a .zip ;)

A co je obzvlášť zajímavé, tyto gzipované/gpgované diffy (rozdílové soubory) lze zveřejňovat jako přílohy ke zprávám v Syndie, což umožňuje, aby se Syndie hostovala sama.

Má s těmihle věcmi někdo nějaké zkušenosti? Nějaké rady?

* 6) ???

Tentokrát jen 24 obrazovek textu (včetně příspěvku na fóru) ;) Bohužel se mi nepodařilo dorazit na schůzku, ale jako vždy budu rád, když se ozvete, pokud máte nějaké nápady nebo návrhy - stačí poslat na mailing list, na fórum, nebo se zastavit na IRC.

=jr
