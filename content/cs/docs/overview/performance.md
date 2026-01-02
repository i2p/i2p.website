---
title: "Výkon"
description: "Výkon sítě I2P: jak se chová dnes, historická vylepšení a nápady pro budoucí optimalizaci"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Výkon sítě I2P: Rychlost, připojení a správa zdrojů

Síť I2P je plně dynamická. Každý klient je znám ostatním uzlům a testuje lokálně známé uzly z hlediska dosažitelnosti a kapacity. Do lokální NetDB jsou ukládány pouze dosažitelné a výkonné uzly. Během procesu budování tunelů jsou z tohoto fondu vybírány nejlepší zdroje pro vytvoření tunelů. Protože testování probíhá nepřetržitě, fond uzlů se mění. Každý I2P uzel zná jinou část NetDB, což znamená, že každý router má k dispozici jinou sadu I2P uzlů pro použití v tunelech. I když dva routery mají stejnou podmnožinu známých uzlů, testy dosažitelnosti a kapacity pravděpodobně ukáží odlišné výsledky, protože ostatní routery mohou být právě pod zátěží ve chvíli, kdy jeden router testuje, ale mohou být volné, když testuje druhý router.

Toto popisuje, proč každý I2P uzel má různé uzly pro budování tunelů. Protože každý I2P uzel má odlišnou latenci a šířku pásma, tunely (které jsou postaveny přes tyto uzly) mají odlišné hodnoty latence a šířky pásma. A protože každý I2P uzel má vybudovány různé tunely, žádné dva I2P uzly nemají stejné sady tunelů.

Server/klient je označován jako „destination" (destinace) a každá destinace má alespoň jeden příchozí a jeden odchozí tunnel. Výchozí nastavení je 3 skoky na tunnel. To dává dohromady 12 skoků (12 různých I2P uzlů) pro úplnou cestu tam a zpět klient → server → klient.

Každý datový balíček je odeslán přes 6 dalších I2P uzlů, než dorazí na server:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

a na zpáteční cestě 6 různých I2P uzlů:

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Provoz v síti vyžaduje ACK před odesláním nových dat; je nutné počkat, až se ACK vrátí ze serveru: odeslat data, počkat na ACK, odeslat další data, počkat na ACK. Protože se RTT (Round Trip Time) skládá z latence každého jednotlivého I2P uzlu a každého připojení na této cestě tam a zpět, obvykle trvá 1–3 sekundy, než se ACK vrátí ke klientovi. Kvůli návrhu TCP a I2P transportu má datový paket omezenou velikost. Tyto podmínky společně stanovují limit maximální šířky pásma na tunel přibližně 20–50 kB/s. Pokud však má pouze jeden hop v tunelu k dispozici pouze 5 kB/s šířky pásma, celý tunel je omezen na 5 kB/s, nezávisle na latenci a dalších omezeních.

Šifrování, latence a způsob, jakým je tunel vybudován, činí jeho vytvoření poměrně náročným z hlediska využití CPU. To je důvod, proč destinace může mít maximálně 6 příchozích a 6 odchozích tunelů pro přenos dat. S maximem 50 kB/s na tunel může destinace využívat zhruba 300 kB/s celkového provozu (ve skutečnosti to může být více, pokud se používají kratší tunely s nízkou nebo žádnou anonymitou). Použité tunely jsou zahozeny každých 10 minut a jsou vybudovány nové. Tato změna tunelů a někdy i klienti, kteří se vypnou nebo ztratí připojení k síti, občas způsobí přerušení tunelů a spojení. Příklad toho lze vidět na IRC2P Network při ztrátě spojení (ping timeout) nebo při použití eepget.

S omezenou sadou cílových destinací a omezenou sadou tunelů na destinaci používá jeden I2P uzel pouze omezenou sadu tunelů napříč jinými I2P uzly. Pokud je například I2P uzel „hop1" v malém příkladu výše, vidí pouze jeden participating tunel vycházející z klienta. Pokud sečteme celou I2P síť, může být vybudován pouze poměrně omezený počet participating tunelů s omezeným množstvím šířky pásma celkem. Pokud tato omezená čísla rozdělíme na počet I2P uzlů, je k dispozici pouze zlomek dostupné šířky pásma/kapacity.

Aby zůstala zachována anonymita, jeden router by neměl být využíván celou sítí pro budování tunelů. Pokud by jeden router fungoval jako router tunelu pro všechny I2P uzly, stal by se velmi reálným centrálním bodem selhání a zároveň centrálním místem pro sbírání IP adres a dat od klientů. To je důvod, proč síť distribuuje provoz napříč uzly v procesu budování tunelů.

Dalším faktorem ovlivňujícím výkon je způsob, jakým I2P zpracovává mesh networking. Každý spojovací přeskok (hop-to-hop) využívá jedno TCP nebo UDP spojení na I2P uzlech. Při 1000 spojeních vidíme 1000 TCP spojení. To je docela hodně a některé domácí routery a routery pro malé kanceláře umožňují pouze malý počet spojení. I2P se snaží omezit tato spojení na méně než 1500 pro UDP a pro TCP typ. Tím se také omezuje množství provozu směrovaného přes I2P uzel.

Pokud je uzel dosažitelný a má nastavení šířky pásma >128 kB/s sdílené a je dosažitelný 24/7, měl by být po určité době použit pro účastnický provoz. Pokud je mezitím nedostupný, testování I2P uzlu prováděné jinými uzly jim sdělí, že není dosažitelný. To zablokuje uzel na ostatních uzlech nejméně na 24 hodin. Takže ostatní uzly, které otestovaly daný uzel jako nedostupný, nebudou tento uzel používat po dobu 24 hodin pro budování tunnelů. To je důvod, proč je váš provoz nižší po restartu/vypnutí vašeho I2P routeru minimálně po dobu 24 hodin.

Navíc další I2P uzly potřebují znát I2P router, aby ho mohly testovat z hlediska dostupnosti a kapacity. Tento proces lze urychlit, když interagujete se sítí, například používáním aplikací nebo návštěvou I2P stránek, což povede k budování více tunnelů a tím pádem k větší aktivitě a dostupnosti pro testování uzly v síti.

## Historie výkonu (vybrané)

V průběhu let došlo v I2P k řadě významných vylepšení výkonu:

### Native math

Implementováno prostřednictvím JNI vazeb na knihovnu GNU MP (GMP) pro zrychlení `modPow` třídy BigInteger, které dříve dominovalo spotřebě procesorového času. Časné výsledky ukázaly dramatické zrychlení v kryptografii s veřejným klíčem. Viz: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Dříve odpovědi často vyžadovaly vyhledání odesílatelova LeaseSet v síťové databázi. Zabalení odesílatelova LeaseSet do počátečního garlic zlepšuje latenci odpovědi. Nyní se to provádí selektivně (na začátku spojení nebo když se LeaseSet změní), aby se snížila režie.

### Nativní matematika

Některé validační kroky byly přesunuty dříve do transport handshake, aby byly špatné uzly odmítnuty dříve (špatné hodiny, špatný NAT/firewall, nekompatibilní verze), což šetří CPU a šířku pásma.

### Garlic wrapping "odpověď" LeaseSet (vyladěný)

Používejte kontextově orientované testování tunelů: vyhýbejte se testování tunelů, u kterých je známo, že procházejí data; upřednostňujte testování v nečinnosti. To snižuje režii a zrychluje detekci selhávajících tunelů.

### Efektivnější odmítání TCP

Zachování výběrů pro dané spojení snižuje doručování mimo pořadí a umožňuje knihovně streamingu zvětšovat velikosti oken, čímž zlepšuje propustnost.

### Úpravy testování tunelů

GZip nebo podobné pro rozsáhlé struktury (např. RouterInfo options) snižuje šířku pásma tam, kde je to vhodné.

### Trvalý výběr tunelu/leaseSetu

Náhrada za zjednodušený protokol "ministreaming". Moderní streaming zahrnuje selektivní ACK a řízení zahlcení přizpůsobené anonymnímu, zprávy orientovanému substrátu I2P. Viz: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Níže jsou uvedeny historicky zdokumentované nápady na potenciální vylepšení. Mnoho z nich je zastaralých, implementovaných nebo nahrazených architektonickými změnami.

### Komprimovat vybrané datové struktury

Zlepšit způsob, jakým routery vybírají uzly pro budování tunelů, aby se vyhnuly pomalým nebo přetíženým uzlům, přičemž zůstanou odolné vůči Sybil útokům ze strany silných protivníků.

### Protokol pro úplné streamování

Snižte zbytečné zkoumání, když je keyspace stabilní; upravte, kolik peerů je vráceno při vyhledávání a kolik souběžných prohledávání je prováděno.

### Session Tag tuning and improvements (legacy)

Pro starší schéma ElGamal/AES+SessionTag snižují chytřejší strategie expirace a doplňování návratů k ElGamal a plýtvání tagy.

### Lepší profilování a výběr peerů

Generovat tagy ze synchronizovaného PRNG osívaného během navázání nové relace, což snižuje per‑message režii oproti předem dodaným tagům.

### Ladění síťové databáze

Delší životnost tunelů ve spojení s opravami může snížit režii obnovy; vyvažte s anonymitou a spolehlivostí.

### Ladění a vylepšení Session Tag (legacy)

Odmítněte neplatné peery dříve a učiňte testování tunelů více kontextově orientované, aby se snížila kontence a latence.

### Migrace SessionTag na synchronizovaný PRNG (legacy)

Selektivní sdružování LeaseSet, komprimované možnosti RouterInfo a adopce plného streamovacího protokolu, to vše přispívá k lepšímu vnímanému výkonu.

# Důležité poznámky pro vývojáře

Prosím přečtěte si tuto stránku pečlivě před vývojem aplikací pro I2P.

## Architektura aplikací

### Používejte SAM nebo I2CP

Pro většinu aplikací doporučujeme používat [SAM (Simple Anonymous Messaging)](https://geti2p.net/docs/api/samv3) nebo [I2CP (I2P Client Protocol)](https://geti2p.net/docs/specs/i2cp/). SAM je jednodušší protokol podobný SOCKS a je dostupný v mnoha programovacích jazycích. I2CP poskytuje více možností konfigurace a kontroly, ale je složitější na použití.

### Nepoužívejte HTTP proxy pro non-HTTP provoz

HTTP proxy je určena pouze pro HTTP provoz. Nepoužívejte ji pro jiné protokoly. Použijte SAM, I2CP nebo SOCKS proxy místo toho.

### Nepoužívejte SOCKS proxy pro kritické aplikace

SOCKS proxy v I2P má určitá omezení a nemusí být vhodná pro všechny aplikace. Pro produkční nasazení doporučujeme používat SAM nebo I2CP.

## Bezpečnost a anonymita

### Mějte na paměti charakteristiky latence

I2P má vyšší latenci než běžný internet. Vaše aplikace by měla být navržena s ohledem na tuto latenci. Používejte vhodné timeouty a opakování.

### Neprozrazujte informace o uživateli

Vaše aplikace by neměla prozrazovat informace jako IP adresu uživatele, časové pásmo nebo jiné identifikující údaje. Buďte opatrní s metadaty.

### Používejte end-to-end šifrování

I2P poskytuje garlic encryption pro ochranu síťové vrstvy, ale pro citlivá data doporučujeme přidat další vrstvu end-to-end šifrování na aplikační úrovni.

## Výkon a škálovatelnost

### Optimalizujte pro I2P síť

I2P má jiné výkonnostní charakteristiky než běžný internet. Minimalizujte počet připojení, používejte connection pooling a implementujte vhodné strategie cachování.

### Testujte s realistickou zátěží

Testujte vaši aplikaci s realistickým množstvím provozu. I2P síť může mít odlišné chování pod zátěží.

## Kompatibilita

### Podporujte různé verze I2P

Různí uživatelé mohou používat různé verze I2P routeru. Navrhněte vaši aplikaci tak, aby byla kompatibilní s více verzemi.

### Dokumentujte závislosti

Jasně dokumentujte všechny závislosti a požadavky na verze pro vaši aplikaci.

Viz také:

- [Směrování tunelů](/docs/overview/tunnel-routing/)
- [Výběr peerů](/docs/overview/tunnel-routing/)
- [Transporty](/docs/overview/transport/)
- [Specifikace SSU2](/docs/specs/ssu2/) a [Specifikace NTCP2](/docs/specs/ntcp2/)
