---
title: "I2P návrh č. 166: Identity/Host Aware Tunnel Types"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Otevřený"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Návrh na Host-Aware HTTP Proxy Tunnel Type

Toto je návrh na řešení „Shared Identity Problem“ v
konvenčním používání HTTP přes I2P zavedením nového typu HTTP proxy tunelu.
Tento typ tunelu má doplňkové chování, které má zabránit nebo omezit
užitečnost sledování prováděného potenciálními nepřátelskými operátory skrytých služeb proti cíleným uživatelským agentům (prohlížečům) a samotné I2P klientské aplikaci.

#### Co je to problém „Shared Identity“?

Problém „Shared Identity“ nastává, když uživatelský agent na
kryptograficky adresované překryvné síti sdílí kryptografickou
identitu s jiným uživatelským agentem. To nastává například, když
Firefox a GNU Wget jsou oba nakonfigurovány k použití stejného HTTP Proxy.

V tomto scénáři je možné, aby server sbíral a uložit
kryptografickou adresu (Destination) použitou k odpovědi na aktivitu. Může
ji považovat za „Fingerprint“, který je vždy 100% jedinečný, protože je
původem kryptografický. To znamená, že dohledatelnost pozorovaná
problémem sdílené identity je dokonalá.

Je to ale problém?
^^^^^^^^^^^^^^^^^^^^

Problém sdílené identity je problém, když uživatelské agenty, které mluví stejným protokolem, chtějí neodkazovatelnou identitu. [Bylo to poprvé uvedeno v
kontextu HTTP v tomto vláknu na Redditu](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/),
s odstraněnými komentáři přístupnými díky
[pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi).
*V té době* jsem byl jedním z nejaktivnějších respondentů a *v té době*
jsem věřil, že problém je malý. Za posledních 8 let se situace a můj
názor na ni změnil, nyní věřím, že hrozba představovaná
svázáním škodlivých cílů roste výrazně, jak více míst je
ve stavu „profilovat“ konkrétní uživatele.

Tento útok má velmi nízkou vstupní bariéru. Vyžaduje pouze, aby
operátor skryté služby provozoval více služeb. Pro útoky na
současné návštěvy (návštěva více webů současně), toto je
jediný požadavek. Pro nesoučasné spojování, jedna z těchto
služeb musí být služba, která hostí „účty“, které patří jedinému uživateli,
který je cílen sledováním.

V současné době bude každý operátor služby, který hostí
uživatelské účty, schopen korolovat je s aktivitou napříč jakýmikoli
stránkami, které ovládají, využitím problému sdílené identity. Mastodon,
Gitlab nebo dokonce jednoduchá fóra by mohla být útočníky v převleku, pokud
provozují více než jednu službu a mají zájem vytvořit profil pro
uživatele. Tento dohled by mohl být prováděn z pohnutek sledování,
finančního zisku nebo zpravodajských důvodů. V současné době existují
desítky hlavních operátorů, kteří by mohli provést tento útok a získat
z něj smysluplná data. V tuto chvíli jim většinou věříme, že
to neudělají, ale hráči, kteří se o naše názory nestarají, by se mohli
snadno objevit.

Toto je přímo spojeno s poměrně základní formou budování profilu na
čistém webu, kde organizace mohou korolovat interakce na jejich stránkách s
interakcemi na sítích, které ovládají. Na I2P, protože
kryptografická destinace je jedinečná, může tato technika někdy
být ještě spolehlivější, i když bez další síly geolokace.

Sdílená identita není užitečná proti uživateli, který používá I2P pouze
k maskování geolokace. Také ji nelze použít k rozlomení směrování I2P.
Je to jen problém kontextového řízení identity.

- Nelze pomocí problému sdílené identity geolokovat uživatele I2P.
- Nelze pomocí problému sdílené identity propojit sezení I2P, pokud nejsou současná.

Nicméně, je možné jej použít k degradaci anonymity uživatele
I2P za okolností, které jsou pravděpodobně velmi běžné. Jedním z
důvodů jejich častosti je, že povzbuzujeme používání Firefoxu, což je
webový prohlížeč, který podporuje „příchodové“ operace.

- Je *vždy* možné vytvořit otisk prstu z problému sdílené identity
  v *jakémkoli* webovém prohlížeči, který podporuje žádosti o
  prostředky třetích stran.
- Zakázání Javascriptu **nic** neřeší proti problému sdílené identity.
- Pokud lze navázat spojení mezi nesoučasnými sezeními jako
  „tradičním“ otiskem prohlížeče, pak může být sdílená
  identita aplikována přechodně, potenciálně umožňující
  nesoučasnou strategii propojení.
- Pokud je možné navázat spojení mezi činností na clearnetu a
  identitou I2P, například pokud je cíl přihlášen k webu s I2P a
  clearnet přítomností na obou stranách, může být sdílená identita
  aplikována přechodně, potenciálně umožňující úplnou
  deanonymizaci.

Jak vidíte vážnost problému sdílené identity v kontextu
I2P HTTP proxy závisí na tom, kde si myslíte (nebo spíše, jak si myslí
„uživatel“ s potenciálně neinformovanými očekáváními), že „kontextová identita“
pro aplikaci leží. Existuje několik možností:

1. HTTP je jak aplikace, tak i kontextová identita - Takto to funguje nyní.
   Všechny HTTP aplikace sdílejí identitu.
2. Proces je aplikace a kontextová identita - Takto to funguje, když aplikace
   používá API jako SAMv3 nebo I2CP, kde aplikace vytváří svou
   identitu a řídí její životnost.
3. HTTP je aplikace, ale host je kontextovou identitou - To je
   předmět tohoto návrhu, který zachází s každým Hostem jako potenciální
   „webovou aplikací“ a takto zachází s povrchem ohrožení.

Je to řešitelný?
^^^^^^^^^^^^^^^^^

Pravděpodobně není možné vytvořit proxy, která inteligentně
reaguje na každý možný případ, kdy by její provoz mohl oslabit
anonymitu aplikace. Nicméně, je možné sestavit proxy, která
inteligentně reaguje na konkrétní aplikaci, která se chová
předvídatelným způsobem. Například v moderních webových prohlížečích je
očekáváno, že uživatelé budou mít otevřeno více karet, kde budou
interagovat s více weby, které budou odlišeny podle názvu hostitele.

To nám umožňuje zlepšit chování HTTP Proxy pro tento typ
uživatelského agenta HTTP tím, že chování proxy odpovídá chování
uživatelského agenta přiřazením každého hosta ke svému vlastnímu
Destination při použití s HTTP Proxy. Tato změna znemožňuje použít
problém sdílené identity k získání otisku prstu, který by mohl být
použit k propojení aktivity klienta se 2 hostiteli, protože 2 hostitelé
již nebudou sdílet návratovou identitu.

Popis:
^^^^^^^^^^^^

Bude vytvořena nová HTTP Proxy a přidána do Správce skrytých služeb
(I2PTunnel). Nová HTTP Proxy bude fungovat jako „multiplexer“
I2PSocketManager. Sám multiplexer nemá žádný cílový bod. Každý
jednotlivý I2PSocketManager, který se stane součástí multiplexu, má svůj
vlastní místní cíl, a svůj vlastní tunelový pool. I2PSocketManagery jsou
vytvářeny na vyžádání multiplexerem, kde „požadavek“ je první
návštěva nového hostitele. Je možné optimalizovat vytváření
I2PSocketManagerů před jejich vložením do multiplexu vytvořením jednoho
nebo více dopředu a uložením je mimo multiplexer. To může zlepšit
výkon.

Další I2PSocketManager s vlastním cílem je nastaven jako nositel
„Outproxy“ pro libovolné stránky, které nemají I2P
Destination, například jakoukoli stránku na clearnetu. Toto účinně činí
veškeré používání Outproxy jednou Kontextovou identitou, s tou výhradou,
že konfigurace více Outproxy pro tunel způsobí normální
„Sticky“ rotaci outproxy, kde každé outproxy obdrží požadavky na
jedinou stránku. To je *téměř* ekvivalentní chování jako izolace
HTTP přes I2P proxy podle destinace, na čistém internetu.

Úvahy o zdrojích:
''''''''''''''''''''''''

Nová HTTP proxy vyžaduje více zdrojů ve srovnání se
stávající HTTP proxy. Bude:

- Potenciálně vytvářet více tunelů a I2PSocketManagerů
- Častěji vytvářet tunely

Každé z těchto úkolů vyžaduje:

- Místní výpočetní zdroje
- Síťové zdroje od vrstevníků

Nastavení:
'''''''''

Aby bylo minimalizováno dopad zvýšeného využití zdrojů, proxy by měla být
nastavena tak, aby používala co nejméně. Proxy, které jsou součástí
multiplexu (nikoliv rodičovská proxy) by měly být nastaveny na:

- Multiplexované I2PSocketManagery vytvářejí 1 tunel dovnitř, 1 tunel ven ve
  svých tunelových poolech
- Multiplexované I2PSocketManagery mají výchozí tři skoky.
- Zavřít sokety po 10 minutách neaktivity.
- I2PSocketManagery spuštěné Multiplexerem sdílejí životnost Multiplexeru.
  Multiplexované tunely nejsou „destruktovány“ dokud není rodičovský
  Multiplexer.

Diagramy:
^^^^^^^^^

Níže uvedený diagram představuje aktuální provoz HTTP proxy,
který odpovídá „Možnosti 1.“ v sekci „Je to problém“. Jak vidíte,
HTTP proxy interaguje s I2P stránkami přímo pouze s jedním cílem. V tomto
scénáři je HTTP jak aplikací, tak i kontextovou identitou.

```text
**Aktuální Situace: HTTP je Aplikace, HTTP je Kontextová Identita**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Prohlížeč <-> HTTP Proxy(jeden cíl)<->I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

Níže uvedený diagram představuje provoz hostitelově vědomé HTTP proxy,
který odpovídá „Možnosti 3.“ v sekci „Je to problém“. V tomto
scénáři je HTTP aplikace, ale Host definuje kontextovou identitu,
kde se každá I2P stránka propojuje s jinou HTTP proxy s jedinečným
cílem na hostitele. To brání operátorům více stránek být schopen
rozeznat, když stejná osoba navštíví více stránek, které provozují.

```text
**Po Změně: HTTP je Aplikace, Host je Kontextová Identita**
                                                        __-> I2PSocketManager(Destination A - pouze Outproxy) <--> i2pgit.org
                                                       /
   Prohlížeč <-> HTTP Proxy Multiplexer(Bez destinace) <---> I2PSocketManager(Destination B) <--> idk.i2p
                                                       \__-> I2PSocketManager(Destination C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager(Destination C) <--> git.idk.i2p
```

Stav:
^^^^^^^

Funkční implementace hostitelově vědomé proxy v Javě, která
odpovídá starší verzi tohoto návrhu, je dostupná v fork od idk pod
větví: i2p.i2p.2.6.0-browser-proxy-post-keepalive Odkaz v citacích. Je
pod těžkou revizí, s cílem rozdělit změny do menších
sekcí.

Implementace s různými schopnostmi byly napsány v Go za
použití knihovny SAMv3, mohou být užitečné pro začlenění do dalších
aplikací v Go nebo pro go-i2p, ale nejsou vhodné pro Java I2P.
Navíc chybí dobrá podpora pro interaktivní práci s
šifrovanými leaseSets.

Dodatky: ``i2psocks``
                      

Jednoduchý přístup ke izolaci jiných typů
klientů je možný bez implementace nového typu tunelu nebo
změny stávajícího kódu I2P kombinací stávajících nástrojů
I2PTunnel, které jsou již široce dostupné a testovány v
komunitě zaměřené na soukromí. Nicméně, tento přístup činí
obtížný předpoklad, který není pravdivý pro HTTP a také není pravdivý
pro mnoho jiných druhů potenciálních klientů I2P.

Přibližně následující skript vytvoří aplikaci orientovanou na SOCKS5
proxy a socksifikuje podkladový příkaz:

```sh
#! /bin/sh
prikaz_k_proxy="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $prikaz_k_proxy
```

Dodatky: ``příklad implementace útoku``
                                                  

[Příklad implementace útoku sdílené identity na HTTP
User-Agents](https://github.com/eyedeekay/colluding_sites_attack/) existuje už několik let. Další příklad je k dispozici ve
``simple-colluder`` podadresáři [idk's prop166
repozitáře](https://git.idk.i2p/idk/i2p.host-aware-proxy)
Tyto příklady jsou záměrně navrženy tak, aby demonstrovaly, že útok
funguje a vyžadovaly by úpravy (i když menší), aby se
přeměnil na skutečný útok.

