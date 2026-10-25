---
title: "Profilování a výběr uzlů"
description: "Jak I2P routery profilují a vybírají protějšky pro budování tunelů"
slug: "peer-selection"
aliases:
  - "/cs/how_peerselection"
  - "/cs/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Poznámka

Tato stránka popisuje Java I2P implementaci profilování a výběru partnerů (peer profiling and selection) k roku 2010. Ačkoliv je stále obecně přesná, některé detaily již nemusí být správné. Pokračujeme ve vývoji strategií blokování, zákazu a výběru, abychom řešili novější hrozby, útoky a síťové podmínky. Současná síť má více implementací routerů s různými verzemi. Jiné I2P implementace mohou mít zcela odlišné strategie profilování a výběru, nebo profilování nemusí používat vůbec.

## Přehled {#overview}

### Profilování peerů {#profiling}

**Profilování peerů** je proces shromažďování dat založený na **pozorovaném** výkonu ostatních routerů nebo peerů a klasifikace těchto peerů do skupin. Profilování **nepoužívá** žádné údaje o výkonu, které peer sám zveřejňuje v [síťové databázi](/docs/overview/network-database).

Profily se používají pro dva účely:

1. Výběr peerů pro přenos našeho provozu, což je probíráno níže
2. Výběr peerů ze skupiny floodfill routerů pro ukládání do síťové databáze a dotazy,
   což je probíráno na stránce [síťová databáze](/docs/overview/network-database)

### Výběr uzlů {#selection}

**Výběr peerů** je proces volby, které routery v síti chceme použít pro přenos našich zpráv (které peery požádáme o připojení do našich tunelů). K dosažení tohoto cíle sledujeme, jak každý peer funguje („profil" peera) a tato data používáme k odhadu jejich rychlosti, jak často budou schopni přijmout naše požadavky a zda se zdají být přetížené nebo jinak neschopné spolehlivě plnit to, s čím souhlasí.

Na rozdíl od některých jiných anonymních sítí se v I2P deklarované šířce pásma nevěří a používá se **pouze** k vyloučení peerů, kteří inzerují velmi nízkou šířku pásma nedostatečnou pro směrování tunelů. Veškerý výběr peerů se provádí prostřednictvím profilování. Tím se předchází jednoduchým útokům založeným na tom, že peeři deklarují vysokou šířku pásma, aby zachytili velké množství tunelů. Také to ztěžuje [timing útoky](/docs/overview/threat-model#timing).

Výběr uzlů se provádí poměrně často, protože router může udržovat velký počet klientských a průzkumných tunelů a životnost tunelu je pouze 10 minut.

### Další informace {#further-info}

Pro více informací si přečtěte článek [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) prezentovaný na [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1). Pro poznámky k drobným změnám od publikování článku viz [níže](#notes).

## Profily {#profiles}

Každý peer má o sobě shromážděnou sadu datových bodů, včetně statistik o tom, jak dlouho trvá, než odpoví na dotaz do síťové databáze, jak často jejich tunnely selhávají a kolik nových peerů nám jsou schopni představit, stejně jako jednoduché datové body, jako je kdy jsme od nich naposledy něco slyšeli nebo kdy došlo k poslední chybě komunikace.

Profily jsou poměrně malé, několik KB. Pro kontrolu využití paměti se doba vypršení profilu zkracuje s rostoucím počtem profilů. Profily jsou uchovávány v paměti až do vypnutí routeru, kdy jsou zapsány na disk. Při startu jsou profily načteny, takže router nemusí reinicializovat všechny profily, což umožňuje routeru rychle se znovu integrovat do sítě po spuštění.

## Souhrny uzlů {#summaries}

Zatímco profily samotné lze považovat za shrnutí výkonu peer, pro umožnění efektivního výběru peer rozdělujeme každé shrnutí na čtyři jednoduché hodnoty představující rychlost peer, jeho kapacitu, jak dobře je integrován do sítě a zda selhává.

### Rychlost {#speed}

Výpočet rychlosti jednoduše prochází profil a odhaduje, kolik dat můžeme poslat nebo přijmout v jednom tunnelu přes peer za minutu. Pro tento odhad se pouze dívá na výkon v předchozí minutě.

### Kapacita {#capacity}

Výpočet kapacity jednoduše projde profil a odhadne, kolik tunnelů by peer souhlasil s účastí během daného časového období. Pro tento odhad se podívá na to, kolik žádostí o vytvoření tunnelu peer přijal, odmítl a zahodil, a kolik ze schválených tunnelů později selhalo. Zatímco výpočet je časově vážený tak, že nedávná aktivita se počítá více než pozdější aktivita, mohou být zahrnuty statistiky až 48 hodin staré.

Rozpoznání a vyhnutí se nespolehlivým a nedostupným uzlům je kriticky důležité. Bohužel, protože budování a testování tunelů vyžaduje účast několika uzlů, je obtížné pozitivně identifikovat příčinu zahozené žádosti o vybudování nebo selhání testu. Router přiřazuje každému z uzlů pravděpodobnost selhání a používá tuto pravděpodobnost při výpočtu kapacity. Zahozené požadavky a selhání testů jsou váženy mnohem výše než odmítnutí.

## Organizace peerů {#organization}

Jak bylo zmíněno výše, projdeme profil každého peera, abychom došli k několika klíčovým výpočtům, a na jejich základě zorganizujeme každého peera do tří skupin - rychlý, vysoká kapacita a standardní.

Skupiny se vzájemně nevylučují ani nejsou nesouvisející:

- Peer je považován za "vysokou kapacitu", pokud jeho výpočet kapacity dosahuje nebo překračuje medián všech peerů.
- Peer je považován za "rychlý", pokud je již "vysokou kapacitou" a jeho výpočet rychlosti dosahuje nebo překračuje medián všech peerů.
- Peer je považován za "standardní", pokud není "vysokou kapacitou"

### Omezení velikosti skupiny {#group-limits}

Velikost skupin může být omezena.

- Rychlá skupina je omezena na 30 peerů.
  Pokud by jich bylo více, do skupiny jsou zařazeni pouze ti s nejvyšším hodnocením rychlosti.
- Skupina s vysokou kapacitou je omezena na 75 peerů (včetně rychlé skupiny).
  Pokud by jich bylo více, do skupiny jsou zařazeni pouze ti s nejvyšším hodnocením kapacity.
- Standardní skupina nemá pevný limit, ale je poněkud menší než počet RouterInfos
  uložených v lokální síťové databázi.
  Na aktivním routeru v dnešní síti může být přibližně 1000 RouterInfos a 500 profilů peerů
  (včetně těch v rychlých skupinách a skupinách s vysokou kapacitou).

## Přepočítání a stabilita {#recalculation}

Souhrny jsou přepočítávány a peers jsou přeřazováni do skupin každých 45 sekund.

Skupiny bývají poměrně stabilní, to znamená, že při každém přepočtu nedochází k velkému "míchání" v žebříčku. Peerové v rychlých a vysokokapacitních skupinách dostávají více tunnelů postavených skrze sebe, což zvyšuje jejich hodnocení rychlosti a kapacity, což posiluje jejich přítomnost ve skupině.

## Výběr peerů {#peer-selection}

Router vybírá protějšky z výše uvedených skupin pro budování tunelů.

### Výběr peerů pro klientské tunnely {#client-tunnels}

Klientské tunnely se používají pro aplikační provoz, například pro HTTP proxy a webové servery.

Pro snížení náchylnosti k [některým útokům](http://blog.torproject.org/blog/one-cell-enough) a zvýšení výkonu jsou peery pro budování klientských tunnelů vybírány náhodně z nejmenší skupiny, což je skupina "rychlých". Není zde žádná preference pro výběr peerů, kteří byli dříve účastníky tunnelu pro stejného klienta.

### Výběr protějšků pro průzkumné tunely {#exploratory-tunnels}

Exploratory tunnels se používají pro administrativní účely routeru, jako je provoz síťové databáze a testování klientských tunelů. Exploratory tunnels se také používají pro kontaktování dříve nepřipojených routerů, což je důvod, proč se nazývají "exploratory". Tyto tunely jsou obvykle nízkorychlostní.

Uzly pro stavbu exploratorních tunnelů jsou obecně vybírány náhodně ze standardní skupiny. Pokud je úspěšnost těchto pokusů o stavbu nízká ve sравnání s úspěšností stavby klientských tunnelů, router místo toho vybere vážený průměr uzlů náhodně ze skupiny s vysokou kapacitou. To pomáhá udržovat uspokojivou úspěšnost stavby i když je výkon sítě špatný. Neexistuje žádná preference k výběru uzlů, které byly dříve účastníky exploratorního tunnelu.

Jelikož standardní skupina zahrnuje velmi velkou podmnožinu všech peerů, o kterých router ví, exploratory tunely jsou v podstatě budovány prostřednictvím náhodného výběru ze všech peerů, dokud míra úspěšnosti budování neklesne příliš nízko.

### Omezení {#restrictions}

Aby se zabránilo některým jednoduchým útokům a kvůli výkonu platí následující omezení:

- Dva peers ze stejného /16 IP prostoru nesmí být ve stejném tunnelu.
- Peer se může účastnit maximálně 33% všech tunnelů vytvořených routerem.
- Peers s extrémně nízkou šířkou pásma se nepoužívají.
- Peers, u kterých nedávno selhal pokus o připojení, se nepoužívají.

### Řazení peerů v tunelech {#ordering}

Peers jsou uspořádány v tunnelech pro řešení [predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([aktualizace z roku 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)). Více informací naleznete na [stránce o tunnelech](/docs/specs/tunnel-implementation#ordering).

## Budoucí práce {#future}

- Pokračovat v analýze a ladění výpočtů rychlosti a kapacity podle potřeby
- Implementovat agresivnější strategii vyřazování, pokud bude nutné kontrolovat využití paměti s růstem sítě
- Vyhodnotit limity velikosti skupin
- Použít GeoIP data k zahrnutí nebo vyloučení určitých peerů, pokud je to nakonfigurováno

## Poznámky {#notes}

Pro ty, kteří čtou článek [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), mějte prosím na paměti následující drobné změny v I2P od publikování tohoto článku:

- Výpočet integrace stále není používán
- V článku se "skupiny" nazývají "úrovně"
- Úroveň "Selhávající" se již nepoužívá
- Úroveň "Neselhávající" se nyní nazývá "Standardní"

## Reference {#references}

- [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf)
- [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Entry Guards](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Paper](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tune-up for Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Low-resource Routing Attacks Against Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
