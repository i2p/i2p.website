---
title: "Zrušení používání hostitelů v adresách routeru"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Přehled

Od verze 0.9.32 aktualizace specifikace netdb ruší používání hostitelů v informacích o routeru,
přesněji v jednotlivých adresách routeru.
Ve všech implementacích I2P by publikující routery konfigurované s hostiteli měly před publikováním nahradit hostitele IP adresami,
a ostatní routery by měly ignorovat adresy s hostiteli.
Routery by neměly provádět DNS dotazy na publikované hostitele.


## Motivace

Hostitelé byli v adresách routeru povoleni od začátku I2P.
Ovšem, velmi málo routerů hostitele publikuje, protože to vyžaduje
veřejného hostitele (kterého má jen málo uživatelů) a manuální nastavení
(o které se málo uživatelů stará).
Nedávný vzorek ukázal, že 0.7 % routerů hostitele publikovalo.

Původním účelem hostitelů bylo pomoci uživatelům s často
se měnícími IP adresami a dynamickou DNS službou (jako http://dyn.com/dns/)
neztrácet konektivitu při změně IP adresy. Ovšem, tehdy
byla síť malá a doba expirace informací o routeru delší.
Také Java kód neměl funkční logiku pro restart routeru nebo
znovupublikování informací o routeru při změně lokální IP adresy.

Také, na začátku I2P nepodporovalo IPv6, takže složitost
překladu hostitele na buď IPv4 nebo IPv6 adresu neexistovala.

V Java I2P bylo vždy výzvou propagovat nakonfigurovaného
hostitele na obě publikované transporty, a situace se stala složitější
s IPv6.
Není jasné, zda by host s duální sítí měl či neměl publikovat jak hostitele, tak doslovnou
IPv6 adresu. Hostitel je publikován pro SSU adresu, ale ne pro NTCP adresu.

Nedávno byly DNS problémy nastíněny (jak nepřímo, tak přímo) výzkumem na
Georgia Tech. Výzkumníci provozovali velké množství floodfill s publikovanými hostiteli.
Okamžitým problémem bylo, že pro malé množství
uživatelů s možná nefunkčním lokálním DNS to zcela zastavilo I2P.

Větší problém bylo DNS obecně, a jak
DNS (buď aktivní nebo pasivní) mohlo být použito k velmi rychlému sečítání sítě,
zvláště pokud publikované routery byly floodfill.
Neplatní hostitelé nebo neodpovídající, pomalý či škodliví DNS respondéři mohli
být použiti k dalším útokům.
EDNS0 může poskytnout další scénáře pro sečítání nebo útoky.
DNS může také poskytnout útočné cesty založené na době dotazu,
prozrazení časů spojení mezi routery, pomoci při tvorbě grafů spojení,
odhadování provozu a dalších odvozování.

Také, skupina z Georgia Tech, vedená Davidem Dagonem, uvedla několik obav
s DNS v aplikacích zaměřených na soukromí. DNS dotazy jsou obecně prováděny
nižší úrovní knihovnou, kterou aplikace neovládá.
Tyto knihovny nebyly speciálně navrženy pro anonymitu;
nemusí poskytovat aplikaci jemné ovládání;
a jejich výstup může být analyzován.
Java knihovny mohou být obzvláště problematické, ale to není jen problém Javy.
Některé knihovny používají DNS ANY dotazy, které mohou být odmítnuty.
To vše je ještě znepokojivější vzhledem k rozšířené přítomnosti
pasivního sledování DNS a dotazů dostupných několika organizacím.
Všechny sledování a útoky DNS jsou mimo rámec pohledu
I2P routerů a vyžadují málo nebo žádné zdroje uvnitř sítě I2P,
a žádnou modifikaci stávajících implementací.

I když jsme ještě zcela nepromysleli možné problémy,
povrch útoku se zdá být velký. Existují jiné způsoby, jak
číslovat síť a shromažďovat související data, ale útoky přes DNS
by mohly být mnohem jednodušší, rychlejší a méně odhalitelné.

Implementace routerů by teoreticky mohly přejít na používání sofistikované
externí DNS knihovny, ale to by bylo značně složité, představovalo by to údržbovou zátěž,
a je to mimo hlavní odbornost vývojářů I2P.

Okamžité řešení implementované pro Java 0.9.31 zahrnovalo opravu problému se zastavením,
zvýšení doby ukládání do mezipaměti DNS a implementaci negativní mezipaměti DNS. Jestliže tedy
zvýšení doby mezipaměti snižuje původní výhody používání hostitelů v informacích o routeru.

Avšak tyto změny jsou pouze krátkodobá opatření a neřeší výše uvedené základní
problémy. Proto je nejjednodušším a nejkompletnějším řešením zakázat
hostitele v informacích o routerech, čímž se eliminují DNS dotazy pro ně.


## Design

Pro kód publikování informací o routeru mají implementátoři dvě možnosti: buď
zakázat/odstranit konfigurační volbu pro hostitele, nebo
převést nakonfigurované hostitele na IP adresy při publikování.
V obou případech by routery měly znovu publikovat ihned po změně jejich IP adresy.

Pro kód validace informací o routeru a připojení k transportu
by implementátoři měli ignorovat adresy routeru obsahující hostitele,
a použít ostatní publikované adresy obsahující IP adresy, pokud existují.
Pokud žádná adresa v informacích o routeru neobsahuje IP adresu, router
by se neměl připojit k publikovanému routeru.
Za žádných okolností by router neměl dělat DNS dotaz na publikovaného hostitele,
ať už přímo nebo prostřednictvím podřízené knihovny.


## Specifikace

Změňte specifikace NTCP a SSU transportu tak, aby určili, že parametr "host" musí být
IP adresa, nikoli hostitel, a že routery by měly ignorovat jednotlivé
adresy routerů, které obsahují hostitele.

To se také vztahuje na parametry "ihost0", "ihost1" a "ihost2" v adrese SSU.
Routery by měly ignorovat adresy zprostředkovatelů, které obsahují hostitele.


## Poznámky

Tento návrh neřeší hostitele pro reseed hosty.
I když jsou DNS dotazy pro reseed hosty mnohem méně časté,
stále by mohly být problémem. Pokud bude nutné, lze to jednoduše
opravit nahrazením hostitelů IP adresami v hardcodovaných seznamech URL;
nejsou potřeba žádné změny ve specifikacích nebo kódu.


## Migrace

Tento návrh může být implementován okamžitě, bez postupné migrace,
protože velmi málo routerů publikuje hostitele a ty, které ano, obvykle
nepublikují hostitele ve všech adresách.

Routery nemusí kontrolovat verzi publikovaného routeru
před rozhodnutím ignorovat hostitele, a není potřeba
koordinovaného vydání nebo společné strategie mezi
různými implementacemi routerů.

U těch routerů, které stále publikují hostitele, dostanou méně
příchozích připojení a mohou mít nakonec potíže s vytvářením
příchozích tunelů.

Pro další minimalizaci dopadů by implementátoři mohli začít ignorováním
adres routerů s hostiteli pouze pro floodfill routery,
nebo pro routery s publikovanou verzí menší než 0.9.32,
a ignorovat hostitele pro všechny routery v pozdějším vydání.
