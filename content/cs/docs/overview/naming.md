---
title: "Pojmenování a Adresář"
description: "Jak I2P mapuje lidsky čitelná jména hostitelů na destinace"
slug: "naming"
aliases:
  - "/cs/docs/specs/naming"
  - "/cs/docs/specs/naming/"
  - "/cs/docs/naming"
  - "/cs/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Přehled

I2P je dodáván s generickou knihovnou pro pojmenování a základní implementací navrženou pro práci s lokálním mapováním jmen na destinace, stejně jako s doplňkovou aplikací nazvanou [address book](#address-book). I2P také podporuje [Base32 hostnames](#base32-names) podobné Tor .onion adresám.

Adresář je bezpečný, distribuovaný a lidsky čitelný systém pojmenovávání řízený sítí důvěry (web-of-trust), který obětuje pouze požadavek na globální jedinečnost všech lidsky čitelných jmen tím, že vyžaduje pouze místní jedinečnost. Zatímco všechny zprávy v I2P jsou kryptograficky adresovány podle svého cíle, různí lidé mohou mít v místním adresáři záznamy pro "Alice", které odkazují na různé cíle. Lidé stále mohou objevovat nová jména importováním publikovaných adresářů od vrstevníků uvedených v jejich síti důvěry, přidáváním záznamů poskytovaných třetí stranou, nebo (pokud někteří lidé organizují sérii publikovaných adresářů pomocí registračního systému "kdo dřív přijde, ten dřív mele") se mohou rozhodnout zacházet s těmito adresáři jako se jmennými servery, čímž napodobují tradiční DNS.

POZNÁMKA: Pro vysvětlení důvodů systému pojmenování I2P, běžné argumenty proti němu a možné alternativy viz stránku [diskuse o pojmenování](/docs/legacy/naming/).

---

## Komponenty systému pojmenování

V I2P neexistuje centrální autorita pro jména. Všechny názvy hostitelů jsou lokální.

Systém pojmenování je poměrně jednoduchý a většina jeho funkcí je implementována v aplikacích externích vůči routeru, ale dodávaných spolu s distribucí I2P. Součásti jsou:

1. Místní [názvová služba](#naming-services), která provádí vyhledávání a také zpracovává [Base32 názvy hostů](#base32-names).
2. [HTTP proxy](#http-proxy), která žádá router o vyhledávání a nasměruje uživatele na vzdálené jump služby pro pomoc s neúspěšným vyhledáváním.
3. HTTP [formuláře pro přidání hostů](#host-add-services), které umožňují uživatelům přidávat hosty do jejich místního hosts.txt
4. HTTP [jump služby](#jump-services), které poskytují vlastní vyhledávání a přesměrování.
5. Aplikace [adresář](#address-book), která slučuje externí seznamy hostů, získané přes HTTP, s místním seznamem.
6. Aplikace [SusiDNS](#susidns), která je jednoduché webové rozhraní pro konfiguraci adresáře a prohlížení místních seznamů hostů.

---

## Služby pojmenování

Všechny destinace v I2P jsou 516bajtové (nebo delší) klíče. (Přesněji řečeno, jedná se o 256bajtový veřejný klíč plus 128bajtový podpisový klíč plus 3 nebo více bajtový certifikát, který v Base64 reprezentaci má 516 nebo více bajtů. Nenulové [certifikáty](/docs/legacy/naming/#certificates) se nyní používají pro označení typu podpisu. Proto certifikáty v nedávno vygenerovaných destinacích mají více než 3 bajty.

Pokud aplikace (i2ptunnel nebo HTTP proxy) chce přistoupit k cíli podle jména, router provede velmi jednoduché místní vyhledání pro vyřešení tohoto jména.

### Jmenná služba Hosts.txt

Služba pojmenování hosts.txt provádí jednoduché lineární prohledávání textových souborů. Tato služba pojmenování byla výchozí až do vydání 0.8.8, kdy byla nahrazena službou pojmenování Blockfile. Formát hosts.txt se stal příliš pomalým poté, co soubor narostl na tisíce záznamů.

Provádí lineární vyhledávání ve třech místních souborech, v pořadí, aby našel názvy hostů a převedl je na 516-bajtový klíč cíle. Každý soubor je v jednoduchém [formátu konfiguračního souboru](/docs/specs/configuration/), s hostname=base64, jeden na řádek. Soubory jsou:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Blockfile Naming Service ukládá více "adresářů adres" v jednom databázovém souboru s názvem hostsdb.blockfile. Tato služba pojmenování je výchozí od verze 0.8.8.

Blockfile je jednoduše úložiště na disku pro několik seřazených map (páry klíč-hodnota), implementované jako skiplists. Formát blockfile je specifikován na [stránce Blockfile](/docs/specs/blockfile/). Poskytuje rychlé vyhledávání Destination v kompaktním formátu. Zatímco režie blockfile je značná, destination jsou uloženy v binární podobě místo v Base 64 jako ve formátu hosts.txt. Kromě toho blockfile poskytuje možnost ukládání libovolných metadat (jako datum přidání, zdroj a komentáře) pro každý záznam pro implementaci pokročilých funkcí adresáře. Požadavek na úložiště blockfile je mírné zvýšení oproti formátu hosts.txt a blockfile poskytuje přibližně 10x snížení času vyhledávání.

Při vytvoření importuje služba názvů záznamy ze tří souborů používaných službou názvů hosts.txt. Blokový soubor napodobuje předchozí implementaci udržováním tří map, které jsou prohledávány v pořadí: privatehosts.txt, userhosts.txt a hosts.txt. Také udržuje mapu pro reverzní vyhledávání, která umožňuje rychlé reverzní vyhledávání.

### Ostatní služby pro překlad jmen

Vyhledávání nerozlišuje velká a malá písmena. Použije se první shoda a konflikty nejsou detekovány. Při vyhledávání nejsou vynucována pravidla pojmenování. Vyhledávání jsou ukládána do cache na několik minut. Rozlišování Base 32 je [popsáno níže](#base32-names). Pro úplný popis API služby pojmenování viz [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). Toto API bylo výrazně rozšířeno ve verzi 0.8.7, aby poskytovalo přidávání a odebírání, ukládání libovolných vlastností s názvem hostitele a další funkce.

### Alternativní a experimentální služby pojmenování

Služba názvů je specifikována konfigurační vlastností `i2p.naming.impl=class`. Jiné implementace jsou možné. Například existuje experimentální zařízení pro vyhledávání v reálném čase (podobně jako DNS) přes síť v rámci routeru. Pro více informací viz [alternativy na diskusní stránce](/docs/legacy/naming/#alternatives).

HTTP proxy provádí vyhledávání prostřednictvím routeru pro všechna jména hostitelů končící na '.i2p'. V opačném případě předává požadavek na nakonfigurovaný HTTP outproxy. V praxi tedy musí všechna HTTP (I2P Site) jména hostitelů končit na pseudo-doménu nejvyšší úrovně '.i2p'.

Pokud se routeru nepodaří vyřešit název hostitele, HTTP proxy vrátí uživateli chybovou stránku s odkazy na několik "jump" služeb. Podrobnosti viz níže.

---

## .i2p.alt Domain

Dříve jsme [žádali o rezervaci TLD .i2p](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) podle postupů uvedených v [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). Tato žádost i všechny ostatní však byly zamítnuty a RFC 6761 bylo označeno za "chybu".

Po mnoha letech práce týmu GNUnet a dalších byla doména .alt vyhrazena jako TLD pro speciální použití v [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) koncem roku 2023. Ačkoli neexistují žádní oficiální registrátoři schválení IANA, zaregistrovali jsme doménu .i2p.alt u primárního neoficiálního registrátora [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). To nezabraňuje ostatním v používání této domény, ale mělo by to pomoci odradit od jejího použití.

Jednou z výhod .alt domény je, že teoreticky DNS resolvery nebudou předávat .alt požadavky, jakmile se aktualizují tak, aby vyhovovaly RFC 9476, a to zabrání únikům DNS. Kvůli kompatibilitě s .i2p.alt názvy hostitelů by měl být I2P software a služby aktualizovány tak, aby tyto názvy hostitelů zvládaly odstraněním .alt TLD. Tyto aktualizace jsou naplánovány na první polovinu roku 2024.

V současné době neexistují žádné plány učinit .i2p.alt preferovanou formou pro zobrazování a výměnu I2P hostnames. Toto je téma pro další výzkum a diskusi.

---

## Adresář

### Příchozí odběry a slučování

Aplikace adresáře pravidelně načítá soubory hosts.txt ostatních uživatelů a po několika kontrolách je slučuje s místním hosts.txt. Konflikty názvů se řeší podle pořadí "kdo dřív přijde, ten dřív mele".

Odebírání souboru hosts.txt jiného uživatele znamená, že mu udělujete určitou míru důvěry. Nechcete například, aby "unesl" novou stránku tím, že rychle zadá svůj vlastní klíč pro novou stránku dřív, než vám předá nový záznam host/klíč.

Z tohoto důvodu je jediným odběrem nakonfigurovaným ve výchozím nastavení `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, který obsahuje kopii souboru hosts.txt zahrnutého v I2P vydání. Uživatelé musí nakonfigurovat další odběry ve své místní aplikaci adresáře (prostřednictvím subscriptions.txt nebo [SusiDNS](#susidns)).

Některé další odkazy na předplatné veřejného adresáře:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Provozovatelé těchto služeb mohou mít různé zásady pro zařazování hostitelů do seznamu. Přítomnost v tomto seznamu neznamená doporučení.

### Pravidla pojmenování

Ačkoli v rámci I2P doufejme nejsou žádná technická omezení pro názvy hostitelů, adresář kontaktů vynucuje několik omezení pro názvy hostitelů importované z předplatného. Dělá to pro základní typografickou rozumnost a kompatibilitu s prohlížeči a také z bezpečnostních důvodů. Pravidla jsou v podstatě stejná jako ta v RFC2396 Section 3.2.2. Jakékoli názvy hostitelů porušující tato pravidla nemusí být propagovány na jiné routery.

Pravidla pojmenování:

- Jména jsou při importu převedena na malá písmena.
- Jména jsou kontrolována na konflikt s existujícími jmény v existujících souborech userhosts.txt a hosts.txt (ale ne privatehosts.txt) po převedení na malá písmena.
- Musí obsahovat pouze [a-z] [0-9] '.' a '-' po převedení na malá písmena.
- Nesmí začínat na '.' nebo '-'.
- Musí končit na '.i2p'.
- Maximálně 67 znaků včetně '.i2p'.
- Nesmí obsahovat '..'.
- Nesmí obsahovat '.-' nebo '-.' (od verze 0.6.1.33).
- Nesmí obsahovat '--' kromě 'xn--' pro IDN.
- Base32 názvy hostitelů (*.b32.i2p) jsou vyhrazeny pro base 32 použití a proto není dovoleno je importovat.
- Určité názvy hostitelů vyhrazené pro použití projektu nejsou povoleny (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p a další)
- Názvy hostitelů začínající na 'www.' jsou nedoporučovány a jsou odmítány některými registračními službami. Některé implementace adresáře automaticky odstraňují předpony 'www.' z vyhledávání. Registrace 'www.example.i2p' je tedy zbytečná a registrace různých destinací pro 'www.example.i2p' a 'example.i2p' způsobí, že 'www.example.i2p' bude pro některé uživatele nedostupné.
- Klíče jsou kontrolovány na platnost base64.
- Klíče jsou kontrolovány na konflikt s existujícími klíči v hosts.txt (ale ne privatehosts.txt).
- Minimální délka klíče 516 bajtů.
- Maximální délka klíče 616 bajtů (pro účely certifikátů do 100 bajtů).

Jakékoliv jméno přijaté prostřednictvím předplatného, které projde všemi kontrolami, je přidáno pomocí místní služby pojmenování.

Všimněte si, že symboly '.' v názvu hostitele nemají žádný význam a neoznačují žádnou skutečnou hierarchii názvů nebo důvěry. Pokud název 'host.i2p' již existuje, nic nebrání komukoli přidat název 'a.host.i2p' do svého hosts.txt a tento název může být importován do adresářů ostatních. Metody pro zamezení subdomén vlastníkům, kteří nejsou 'vlastníky' domény (certifikáty?), a žádoucnost a proveditelnost těchto metod jsou témata pro budoucí diskusi.

International Domain Names (IDN) také fungují v i2p (pomocí punycode formátu 'xn--'). Pro správné zobrazení IDN .i2p doménových jmen v adresním řádku Firefoxu přidejte 'network.IDN.whitelist.i2p (boolean) = true' v about:config.

Jelikož aplikace adresáře vůbec nepoužívá privatehosts.txt, v praxi je tento soubor jediné místo, kde je vhodné umístit soukromé aliasy nebo "domácká jména" pro stránky, které jsou již v hosts.txt.

### Pokročilý formát kanálu předplatného

Od verze 0.9.26 mohou weby s odběry a klienti podporovat pokročilý protokol pro hosts.txt kanály, který zahrnuje metadata včetně podpisů. Tento formát je zpětně kompatibilní se standardním formátem hosts.txt hostname=base64destination. Podrobnosti viz [specifikace](/docs/specs/subscription/).

### Odchozí odběry

Adresář kontaktů publikuje sloučený soubor hosts.txt do umístění (tradičně hosts.txt v domovském adresáři místního I2P Site) pro přístup ostatních k jejich odběrům. Tento krok je volitelný a je ve výchozím nastavení zakázán.

### Problémy s hostingem a HTTP transportem

Aplikace adresáře společně s eepget ukládá informace Etag a/nebo Last-Modified vrácené webovým serverem odběru. To výrazně snižuje požadovanou šířku pásma, protože webový server vrátí '304 Not Modified' při příštím načítání, pokud se nic nezměnilo.

Avšak celý soubor hosts.txt je stažen, pokud se změnil. Viz níže pro diskusi o tomto problému.

Serverům poskytujícím statický soubor hosts.txt nebo ekvivalentní CGI aplikaci se důrazně doporučuje doručovat hlavičku Content-Length a buď hlavičku Etag nebo Last-Modified. Také se ujistěte, že server doručuje odpověď '304 Not Modified', když je to vhodné. To dramaticky sníží šířku pásma sítě a sníží pravděpodobnost poškození dat.

---

## Přidat služby hostitele

Služba pro přidávání hostů je jednoduchá CGI aplikace, která přijímá hostname a Base64 klíč jako parametry a přidává je do svého lokálního souboru hosts.txt. Pokud se jiné routery přihlásí k odběru tohoto hosts.txt, nový hostname/klíč se rozšíří po síti.

Je doporučeno, aby služby pro přidávání hostitelů uplatňovaly minimálně omezení uložená aplikací adresáře uvedenou výše. Služby pro přidávání hostitelů mohou uplatňovat další omezení na názvy hostitelů a klíče, například:

- Omezení počtu 'subdomén'.
- Autorizace 'subdomén' prostřednictvím různých metod.
- Hashcash nebo podepsané certifikáty.
- Redakční kontrola názvů hostů a/nebo obsahu.
- Kategorizace hostů podle obsahu.
- Rezervace nebo zamítnutí určitých názvů hostů.
- Omezení počtu jmen registrovaných v daném časovém období.
- Zpoždění mezi registrací a publikací.
- Požadavek, aby byl host dostupný pro ověření.
- Vypršení platnosti a/nebo zrušení.
- Zamítnutí IDN spoofingu.

---

## Jump Services

Jump service je jednoduchá CGI aplikace, která přijímá hostname jako parametr a vrací 301 přesměrování na správnou URL s připojeným řetězcem `?i2paddresshelper=key`. HTTP proxy interpretuje připojený řetězec a použije tento klíč jako skutečnou destinaci. Navíc proxy tento klíč uloží do cache, takže address helper není potřebný až do restartu.

Poznamenejte, že stejně jako u předplatných, používání jump služby implikuje určitou míru důvěry, protože jump služba by mohla škodlivě přesměrovat uživatele na nesprávnou destinaci.

Pro poskytování nejlepší služby by se jump služba měla přihlásit k odběru od několika poskytovatelů hosts.txt, aby byl její místní seznam hostů aktuální.

---

## SusiDNS

SusiDNS je jednoduše webové rozhraní pro konfiguraci předplatného adresářů a přístup ke čtyřem souborům adresářů. Veškerou skutečnou práci vykonává aplikace 'address book'.

V současné době je v SusiDNS jen malé vynucování pravidel pojmenování adresáře, takže uživatel může lokálně zadat názvy hostitelů, které by byla zamítnuta pravidly předplatného adresáře.

---

## Base32 názvy

I2P podporuje Base32 hostnames podobné Tor .onion adresám. Base32 adresy jsou mnohem kratší a snáze se s nimi pracuje než s úplnými 516-znakovými Base64 Destinations nebo addresshelpers. Příklad: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

V Toru je adresa 16 znaků (80 bitů), což je polovina SHA-1 hashe. I2P používá 52 znaků (256 bitů) pro reprezentaci úplného SHA-256 hashe. Formát je {52 znaků}.b32.i2p. Tor má [návrh](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) na převod na identický formát {52 znaků}.onion pro své skryté služby. Base32 je implementováno v názvové službě, která dotazuje router přes I2CP k vyhledání leaseSet pro získání úplné destinace. Base32 vyhledávání bude úspěšné pouze když je destinace aktivní a publikuje leaseSet. Protože rozlišení může vyžadovat vyhledávání v síťové databázi, může trvat výrazně déle než lokální vyhledávání v adresáři.

Base32 adresy mohou být používány na většině míst, kde se používají hostnames nebo úplné destinations, existují však některé výjimky, kdy mohou selhat, pokud se jméno okamžitě nepřeloží. I2PTunnel například selže, pokud se jméno nepřeloží na destination.

---

## Rozšířené Base32 názvy

Rozšířené base 32 názvy byly představeny ve verzi 0.9.40 pro podporu šifrovaných lease setů. Adresy pro šifrované leaseSety jsou identifikovány 56 nebo více zakódovanými znaky, nepočítaje ".b32.i2p" (35 nebo více dekódovaných bajtů), ve srovnání s 52 znaky (32 bajtů) pro tradiční base 32 adresy. Viz návrhy 123 a 149 pro další informace.

Standardní Base 32 ("b32") adresy obsahují hash destinace. Toto nebude fungovat pro šifrované ls2 (návrh 123).

Nemůžete použít tradiční base 32 adresu pro šifrovaný LS2 (návrh 123), protože obsahuje pouze hash cílové destinace. Neposkytuje nezakrytý veřejný klíč. Klienti musí znát veřejný klíč destinace, typ podpisu, typ zakrytého podpisu a volitelný tajný nebo soukromý klíč pro načtení a dešifrování leaseset. Proto samotná base 32 adresa není dostačující. Klient potřebuje buď úplnou destinaci (která obsahuje veřejný klíč), nebo samotný veřejný klíč. Pokud má klient úplnou destinaci v adresáři a adresář podporuje zpětné vyhledávání podle hash, pak může být veřejný klíč získán.

Potřebujeme tedy nový formát, který vloží veřejný klíč místo hashe do base32 adresy. Tento formát musí také obsahovat typ podpisu veřejného klíče a typ podpisu schématu oslnění.

Tato sekce dokumentuje nový b32 formát pro tyto adresy. Zatímco jsme během diskuzí odkazovali na tento nový formát jako na "b33" adresu, skutečný nový formát si zachovává obvyklou příponu ".b32.i2p".

### Vytváření a kódování

Sestavte hostname ve formátu {56+ znaků}.b32.i2p (35+ znaků v binárním formátu) následovně. Nejprve sestavte binární data, která budou kódována do base 32:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Následné zpracování a kontrolní součet:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Všechny nepoužité bity na konci b32 musí být 0. Pro standardní 56znakovou (35 bajtovou) adresu nejsou žádné nepoužité bity.

### Dekódování a ověření

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bity tajného a soukromého klíče

Bity secret a private key se používají k indikaci klientům, proxy nebo jinému kód na straně klienta, že secret a/nebo private key bude potřebný k dešifrování leaseSetu. Konkrétní implementace mohou vyzvat uživatele k poskytnutí požadovaných dat nebo odmítnout pokusy o připojení, pokud požadovaná data chybí.

### Poznámky

- XORování prvních 3 bajtů s hashem poskytuje omezenou schopnost kontrolního součtu a zajišťuje, že všechny base32 znaky na začátku jsou randomizovány. Platné jsou pouze některé kombinace příznaků a typů podpisů, takže jakýkoli překlep pravděpodobně vytvoří neplatnou kombinaci a bude zamítnut.
- V obvyklém případě (1-bajtové typy podpisů, žádné tajemství, žádná autentifikace per-client) bude hostname {56 znaků}.b32.i2p, dekódováno na 35 bajtů, stejně jako Tor.
- 2-bajtový kontrolní součet Toru má míru falešných negativ 1/64K. Se 3 bajty, minus několik ignorovaných bajtů, se náš blíží 1 k milionu, protože většina kombinací příznaků/typů podpisů je neplatná.
- Adler-32 je špatná volba pro malé vstupy a pro detekci malých změn. Místo toho používáme CRC-32. CRC-32 je rychlý a široce dostupný.
- Ačkoli je to mimo rozsah této specifikace, routery a/nebo klienti si musí pamatovat a ukládat do cache (pravděpodobně trvale) mapování veřejného klíče na cíl a naopak.
- Rozlišit staré od nových variant podle délky. Staré b32 adresy jsou vždy {52 znaků}.b32.i2p. Nové jsou {56+ znaků}.b32.i2p
- Diskuzní vlákno Toru [je zde](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Neočekávejte, že se kdy stanou 2-bajtové typy podpisů, jsme teprve na 13. Není potřeba implementovat nyní.
- Nový formát lze použít v jump odkazech (a obsluhovaných jump servery), pokud je to žádoucí, stejně jako b32.
- Jakékoli tajemství, soukromý klíč nebo veřejný klíč delší než 32 bajtů by překročil maximální délku DNS labelu 63 znaků. Prohlížečům to pravděpodobně nevadí.
- Žádné problémy se zpětnou kompatibilitou. Delší b32 adresy se nepodaří převést na 32-bajtové hashe ve starém softwaru.
