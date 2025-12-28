---
title: "Vývoj aplikací"
description: "Proč psát aplikace specifické pro I2P, klíčové koncepty, možnosti vývoje a jednoduchý průvodce pro začátečníky"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Proč psát kód specifický pro I2P?

Existuje několik způsobů, jak používat aplikace v I2P. Pomocí [I2PTunnel](/docs/api/i2ptunnel/) můžete používat běžné aplikace, aniž byste museli programovat explicitní podporu I2P. To je velmi efektivní pro scénáře klient-server, kde potřebujete se připojit k jediné webové stránce. Můžete jednoduše vytvořit tunnel pomocí I2PTunnel pro připojení k této webové stránce, jak je znázorněno na obrázku 1.

Pokud je vaše aplikace distribuovaná, bude vyžadovat připojení k velkému množství uzlů. Při použití I2PTunnel budete muset vytvořit nový tunel pro každý uzel, se kterým se chcete spojit, jak je znázorněno na obrázku 2. Tento proces lze samozřejmě automatizovat, ale provozování mnoha instancí I2PTunnel vytváří velkou režii. Kromě toho u mnoha protokolů budete muset donutit všechny používat stejnou sadu portů pro všechny uzly — např. pokud chcete spolehlivě provozovat DCC chat, každý se musí dohodnout, že port 10001 je Alice, port 10002 je Bob, port 10003 je Charlie a tak dále, protože protokol obsahuje informace specifické pro TCP/IP (host a port).

Obecné síťové aplikace často odesílají množství dodatečných dat, která mohou být použita k identifikaci uživatelů. Názvy hostitelů, čísla portů, časová pásma, znakové sady atd. jsou často odesílány bez informování uživatele. Proto navržení síťového protokolu specificky s ohledem na anonymitu může zabránit kompromitaci identit uživatelů.

Při určování způsobu interakce nad I2P je třeba zvážit také aspekty efektivity. Streamovací knihovna a nástroje na ní postavené pracují s handshaky podobnými TCP, zatímco základní I2P protokoly (I2NP a I2CP) jsou striktně založené na zprávách (jako UDP nebo v některých případech čisté IP). Důležitým rozlišením je, že u I2P probíhá komunikace přes dlouhou silně zaplněnou síť — každá end-to-end zpráva bude mít nezanedbatelné latence, ale může obsahovat datové části o velikosti až několika KB. Aplikace, která potřebuje jednoduché požadavky a odpovědi, se může zbavit jakéhokoli stavu a snížit latenci způsobenou inicializačními a ukončovacími handshaky použitím datagramů (best effort) bez nutnosti řešit detekci MTU nebo fragmentaci zpráv.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
Shrnutí, několik důvodů pro psaní kódu specifického pro I2P:

- Vytvoření velkého množství I2PTunnel instancí spotřebovává nezanedbatelné množství zdrojů, což je problematické pro distribuované aplikace (pro každého peer je vyžadován nový tunnel).
- Obecné síťové protokoly často odesílají velké množství dodatečných dat, která mohou být použita k identifikaci uživatelů. Programování přímo pro I2P umožňuje vytvoření síťového protokolu, který takové informace neprozrazuje, a udržuje tak uživatele anonymní a v bezpečí.
- Síťové protokoly navržené pro použití na běžném internetu mohou být na I2P neefektivní, což je síť s mnohem vyšší latencí.

I2P podporuje standardní [rozhraní pro pluginy](/docs/plugins/) pro vývojáře, aby mohly být aplikace snadno integrovány a distribuovány.

Aplikace napsané v Javě a přístupné/spustitelné pomocí HTML rozhraní přes standardní webapps/app.war mohou být zváženy k zařazení do distribuce I2P.

## Důležité koncepty

Při používání I2P je třeba se přizpůsobit několika změnám:

### Destinace

Aplikace běžící na I2P posílá zprávy z jedinečného kryptograficky zabezpečeného koncového bodu — „destination" (cíle) — a přijímá do něj zprávy. Ve smyslu TCP nebo UDP by destination mohl být (z velké části) považován za ekvivalent dvojice název hostitele plus číslo portu, i když existuje několik rozdílů.

- I2P destination sama o sobě je kryptografický konstrukt — všechna data na ni odeslaná jsou šifrována, jako by byl universálně nasazen IPsec s (anonymizovanou) lokací koncového bodu podepsanou, jako by byl universálně nasazen DNSSEC.
- I2P destinace jsou mobilní identifikátory — mohou být přesunuty z jednoho I2P routeru na jiný (nebo mohou dokonce operovat v režimu „multihome" — pracovat na více routerech současně). To se výrazně liší od světa TCP nebo UDP, kde jeden koncový bod (port) musí zůstat na jediném hostu.
- I2P destinace jsou nepřehledné a velké — na pozadí obsahují 2048bitový ElGamal veřejný klíč pro šifrování, 1024bitový DSA veřejný klíč pro podepisování a certifikát proměnné velikosti, který může obsahovat proof of work nebo zaslepená data.

Existují způsoby, jak odkazovat na tyto velké a nepohodlné destinace pomocí krátkých a přehledných názvů (např. "irc.duck.i2p"), ale tyto techniky nezaručují globální unikátnost (protože jsou uloženy lokálně v databázi na počítači každého uživatele) a současný mechanismus není příliš škálovatelný ani bezpečný (aktualizace seznamu hostitelů jsou spravovány pomocí "odběrů" jmenných služeb). Možná jednou vznikne bezpečný, lidsky čitelný, škálovatelný a globálně unikátní systém pojmenování, ale aplikace by na něm neměly být závislé. [Další informace o systému pojmenování](/docs/overview/naming/) jsou k dispozici.

Zatímco většina aplikací nepotřebuje rozlišovat protokoly a porty, I2P je *podporuje*. Komplexní aplikace mohou specifikovat protokol, zdrojový port a cílový port na základě jednotlivých zpráv, aby multiplexovaly provoz na jedné destinaci. Podrobnosti naleznete na [stránce o datagramech](/docs/api/datagrams/). Jednoduché aplikace fungují tak, že naslouchají "všem protokolům" na "všech portech" destinace.

### Anonymita a důvěrnost

I2P má transparentní end-to-end šifrování a autentizaci pro všechna data přenášená přes síť — pokud Bob posílá na Alicinu destinaci, může ji přijmout pouze Alicina destinace, a pokud Bob používá datagramovou nebo streamovací knihovnu, Alice má jistotu, že data poslala Bobova destinace.

Samozřejmě, I2P transparentně anonymizuje data odesílaná mezi Alicí a Bobem, ale nedělá nic pro anonymizaci obsahu toho, co si posílají. Například pokud Alice pošle Bobovi formulář se svým celým jménem, občanskými průkazy a čísly platebních karet, I2P s tím nemůže nic udělat. Protokoly a aplikace by proto měly mít na paměti, jaké informace se snaží chránit a jaké informace jsou ochotny odhalit.

### I2P datagramy mohou mít až několik KB

Aplikace využívající I2P datagramy (ať už základní nebo s možností odpovědi) lze v podstatě chápat z hlediska UDP — datagramy jsou neuspořádané, s best effort doručením a bezstavové — ale na rozdíl od UDP se aplikace nemusí starat o detekci MTU a mohou jednoduše odesílat velké datagramy. Zatímco horní limit je nominálně 32 KB, zpráva je fragmentována pro přenos, což snižuje spolehlivost celku. Datagramy nad přibližně 10 KB se v současnosti nedoporučují. Podrobnosti naleznete na [stránce o datagramech](/docs/api/datagrams/). Pro mnoho aplikací je 10 KB dat dostačujících pro celý požadavek nebo odpověď, což jim umožňuje transparentně fungovat v I2P jako UDP-like aplikace bez nutnosti implementovat fragmentaci, opětovné odesílání atd.

## Možnosti vývoje

Existuje několik způsobů přenosu dat přes I2P, každý s vlastními výhodami a nevýhodami. Streaming lib je doporučené rozhraní, které používá většina I2P aplikací.

### Streaming Lib

[Kompletní streaming knihovna](/docs/specs/streaming/) je nyní standardním rozhraním. Umožňuje programování pomocí socketů podobných TCP, jak je vysvětleno v [průvodci vývojem pro Streaming](#developing-with-the-streaming-library).

### BOB

BOB je [Basic Open Bridge](/docs/legacy/bob/), umožňující aplikaci v jakémkoliv jazyce vytvářet streamovací spojení do a z I2P. V současné době postrádá podporu UDP, ale podpora UDP je plánována v blízké budoucnosti. BOB také obsahuje několik nástrojů, jako je generování klíčů destinací a ověřování, zda adresa odpovídá specifikacím I2P. Aktuální informace a aplikace využívající BOB naleznete na této [I2P Stránce](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM se nedoporučuje. SAM V2 je v pořádku, SAM V3 se doporučuje.*

SAM je protokol [Simple Anonymous Messaging](/docs/legacy/sam/), který umožňuje aplikaci napsané v jakémkoli jazyce komunikovat s SAM bridge přes obyčejný TCP socket a nechat tento bridge multiplexovat veškerý její I2P provoz, transparentně koordinovat šifrování/dešifrování a zpracování založené na událostech. SAM podporuje tři styly provozu:

- streamy, pro případy kdy Alice a Bob chtějí posílat data spolehlivě a ve správném pořadí
- odpověditelné datagramy, pro případy kdy Alice chce poslat Bobovi zprávu, na kterou může Bob odpovědět
- čisté datagramy, pro případy kdy Alice chce vyždímat co nejvíce šířky pásma a výkonu, a Bobovi nezáleží na tom, zda je odesílatel dat ověřený či ne (např. přenášená data jsou sama o sobě autentizovaná)

SAMv3 sleduje stejný cíl jako SAM a SAM V2, ale nevyžaduje multiplexování/demultiplexování. Každý I2P stream je obsluhován vlastním socketem mezi aplikací a SAM mostem. Kromě toho mohou být datagramy odesílány a přijímány aplikací prostřednictvím datagramové komunikace s SAM mostem.

[SAM V2](/docs/legacy/samv2/) je nová verze používaná aplikací imule, která opravuje některé problémy v [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) je používán aplikací imule od verze 1.4.0.

### I2PTunnel

Aplikace I2PTunnel umožňuje aplikacím vytvářet specifické TCP-podobné tunely k protějškům vytvořením buď I2PTunnel 'klientských' aplikací (které naslouchají na konkrétním portu a připojují se ke konkrétní I2P destinaci, kdykoli je otevřen socket na tento port) nebo I2PTunnel 'serverových' aplikací (které naslouchají na konkrétní I2P destinaci a kdykoli obdrží nové I2P připojení, předávají ho na konkrétního TCP hosta/port). Tyto streamy jsou 8-bitově čisté a jsou autentizovány a zabezpečeny pomocí stejné streaming knihovny, kterou používá SAM, ale vytváření více unikátních instancí I2PTunnel s sebou nese nezanedbatelnou režii, protože každá má svou vlastní unikátní I2P destinaci a svou vlastní sadu tunelů, klíčů atd.

### SOCKS

I2P podporuje SOCKS V4 a V5 proxy. Odchozí spojení fungují dobře. Příchozí (server) a UDP funkčnost může být neúplná a neotestovaná.

### Ministreaming

*Odstraněno*

Dříve existovala jednoduchá knihovna „ministreaming", ale nyní ministreaming.jar obsahuje pouze rozhraní pro plnou streaming knihovnu.

### Datagramy

*Doporučeno pro aplikace podobné UDP*

[Knihovna Datagram](/docs/api/datagrams/) umožňuje odesílání paketů podobných UDP. Je možné použít:

- Odpověditelné datagramy
- Surové datagramy

### I2CP

*Nedoporučuje se*

[I2CP](/docs/specs/i2cp/) je sám o sobě protokol nezávislý na programovacím jazyce, ale pro implementaci I2CP knihovny v jiném jazyce než Java je potřeba napsat značné množství kódu (šifrovací rutiny, marshalling objektů, asynchronní zpracování zpráv atd.). I když by někdo mohl napsat I2CP knihovnu v C nebo jiném jazyce, bylo by pravděpodobně užitečnější použít místo toho SAM knihovnu v C.

### Webové aplikace

I2P je dodáván s webovým serverem Jetty a konfigurace pro použití serveru Apache je jednoduchá. Měla by fungovat jakákoli standardní technologie webových aplikací.

## Začněte s vývojem — Jednoduchý průvodce

Vývoj s I2P vyžaduje funkční instalaci I2P a vývojové prostředí dle vašeho výběru. Pokud používáte Javu, můžete začít vývoj se [streaming library](#developing-with-the-streaming-library) nebo datagram library. Při použití jiného programovacího jazyka lze využít SAM nebo BOB.

### Vývoj se Streaming knihovnou

Níže je zkrácená a modernizovaná verze příkladu z původní stránky. Pro kompletní příklad viz starší stránku nebo naše Java příklady v kódové základně.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Příklad kódu: základní server přijímající data.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Příklad kódu: klient se připojuje a odesílá řádek.*
