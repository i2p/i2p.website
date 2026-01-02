---
title: "I2P: Škálovatelný framework pro anonymní komunikaci"
description: "Technický úvod do architektury a provozu I2P"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Úvod

I2P je škálovatelná, samospravující se a odolná paketově přepínaná anonymní síťová vrstva, na které může fungovat libovolný počet různých aplikací zaměřených na anonymitu nebo bezpečnost. Každá z těchto aplikací může provádět vlastní kompromisy mezi anonymitou, latencí a propustností, aniž by se musela starat o správnou implementaci mixnet se svobodným směrováním, což jim umožňuje splynout jejich aktivitu s větší množinou anonymních uživatelů již běžících nad I2P.

Již dostupné aplikace poskytují plnou škálu typických internetových aktivit — **anonymní** prohlížení webu, webhosting, chat, sdílení souborů, e-mail, blogování a sdílení obsahu, stejně jako několik dalších aplikací ve vývoji.

- **Prohlížení webu:** pomocí jakéhokoli existujícího prohlížeče, který podporuje proxy  
- **Chat:** IRC a další protokoly  
- **Sdílení souborů:** [I2PSnark](#i2psnark) a další aplikace  
- **E-mail:** [Susimail](#i2pmail) a další aplikace  
- **Blog:** pomocí jakéhokoli lokálního webového serveru nebo dostupných pluginů

Na rozdíl od webových stránek hostovaných v sítích pro distribuci obsahu jako [Freenet](/docs/overview/comparison#freenet) nebo [GNUnet](https://www.gnunet.org/), jsou služby hostované v I2P plně interaktivní — existují tradiční webové vyhledávače, diskuzní fóra, blogy, ke kterým můžete přidávat komentáře, stránky založené na databázích a mosty pro dotazování statických systémů jako Freenet bez nutnosti jejich lokální instalace.

Se všemi těmito aplikacemi s podporou anonymity funguje I2P jako **message-oriented middleware** (middleware orientované na zprávy) — aplikace specifikují data k odeslání na kryptografický identifikátor („destination"), a I2P zajistí jejich bezpečné a anonymní doručení. I2P také obsahuje jednoduchou [streaming library](#streaming) (knihovnu pro streamování), která umožňuje převést anonymní zprávy I2P s best-effort doručováním na spolehlivé, uspořádané datové toky, nabízející řízení přetížení založené na TCP a vyladěné pro vysoký bandwidth-delay product (součin šířky pásma a zpoždění) sítě.

Ačkoli byly vyvinuty jednoduché SOCKS proxy pro připojení existujících aplikací, jejich hodnota je omezená, protože většina aplikací uniká citlivé informace v anonymním kontextu. Nejbezpečnějším přístupem je **auditovat a přizpůsobit** aplikaci pro přímé použití I2P API.

I2P není výzkumný projekt — akademický, komerční ani vládní — ale inženýrské úsilí zaměřené na poskytování použitelné anonymity. Je neustále vyvíjen od začátku roku 2003 distribuovanou skupinou přispěvatelů z celého světa. Veškerá práce na I2P je **open source** na [oficiální webové stránce](https://geti2p.net/), primárně uvolněná do veřejné domény, přičemž některé komponenty jsou pod permisivními licencemi ve stylu BSD. K dispozici je několik klientských aplikací pod licencí GPL, jako například [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) a [I2PSnark](#i2psnark). Financování pochází výhradně z darů uživatelů.

---

## Provoz

### Overview

I2P jasně rozlišuje mezi routery (uzly účastnící se sítě) a destinacemi (anonymní koncové body pro aplikace). Samotné provozování I2P není tajné; co je skryté, je **co** uživatel dělá a který router jeho destinace používají. Koncoví uživatelé obvykle provozují několik destinací (např. jednu pro prohlížení webu, další pro hosting, další pro IRC).

Klíčovým konceptem v I2P je **tunnel** — jednosměrná šifrovaná cesta skrze sérii routerů. Každý router dešifruje pouze jednu vrstvu a dozví se pouze další hop. Tunnely vyprší každých 10 minut a musí být znovu vybudovány.

![Schéma vstupních a výstupních tunelů](/images/tunnels.png)   *Obrázek 1: Existují dva typy tunelů — vstupní (inbound) a výstupní (outbound).*

- **Odchozí tunely** odesílají zprávy pryč od tvůrce.  
- **Příchozí tunely** přinášejí zprávy zpět k tvůrci.

Kombinace těchto prvků umožňuje obousměrnou komunikaci. Například "Alice" používá odchozí tunnel k odeslání zprávy do příchozího tunnelu "Boba". Alice zašifruje svou zprávu s routovacími instrukcemi do Bobovy příchozí brány.

Dalším klíčovým konceptem je **síťová databáze** neboli **netDb**, která distribuuje metadata o routerech a cílech:

- **RouterInfo:** Obsahuje kontaktní informace routeru a klíčový materiál.  
- **LeaseSet:** Obsahuje informace potřebné ke kontaktování destinace (tunnel brány, časy vypršení, šifrovací klíče).

Routery publikují své RouterInfo přímo do netDb; LeaseSety jsou odesílány přes odchozí tunnely pro zajištění anonymity.

Pro vybudování tunelů Alice dotazuje netDb na záznamy RouterInfo pro výběr uzlů a odesílá šifrované zprávy pro vybudování tunelu hop-by-hop, dokud není tunel dokončen.

![Informace o routeru se používají k vytváření tunnelů](/images/netdb_get_routerinfo_2.png)   *Obrázek 2: Informace o routeru se používají k vytváření tunnelů.*

Pro odeslání Bobovi Alice vyhledá Bobův LeaseSet a použije jeden ze svých odchozích tunelů pro směrování dat přes vstupní bránu Bobova příchozího tunelu.

![LeaseSets spojují příchozí a odchozí tunely](/images/netdb_get_leaseset.png)   *Obrázek 3: LeaseSets spojují odchozí a příchozí tunely.*

Protože I2P je založeno na zprávách, přidává **end-to-end garlic encryption** (koncové šifrování cibulového typu) pro ochranu zpráv dokonce i před odchozím koncovým bodem nebo příchozí bránou. Garlic zpráva zabaluje více šifrovaných "cloves" (jednotlivých zpráv) pro skrytí metadat a zlepšení anonymity.

Aplikace mohou buď použít rozhraní zpráv přímo, nebo se spolehnout na [streamovací knihovnu](#streaming) pro spolehlivá připojení.

---

### Tunnels

Jak příchozí, tak odchozí tunely používají vrstvové šifrování, ale liší se v konstrukci:

- V **příchozích tunelech** tvůrce (koncový bod) dešifruje všechny vrstvy.
- V **odchozích tunelech** tvůrce (brána) předem dešifruje vrstvy, aby byla zajištěna srozumitelnost na koncovém bodě.

I2P profiluje uzly pomocí nepřímých metrik, jako je latence a spolehlivost, bez přímého dotazování. Na základě těchto profilů jsou uzly dynamicky seskupovány do čtyř úrovní:

1. Rychlý a s vysokou kapacitou  
2. Vysoká kapacita  
3. Nefungující  
4. Selhávající

Výběr uzlů pro tunel obvykle upřednostňuje uzly s vysokou kapacitou, náhodně vybrané pro vyvážení anonymity a výkonu, s dodatečnými strategiemi řazení založenými na XOR pro zmírnění predecessor útoků a sklízení netDb.

Pro podrobnější informace viz [Specifikace tunnelů](/docs/specs/implementation).

---

### Přehled

Routery účastnící se **floodfill** distribuované hash tabulky (DHT) ukládají a odpovídají na vyhledávání LeaseSet. DHT používá variantu [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Floodfill routery jsou vybírány automaticky, pokud mají dostatečnou kapacitu a stabilitu, nebo mohou být nakonfigurovány ručně.

- **RouterInfo:** Popisuje schopnosti routeru a jeho transporty.  
- **LeaseSet:** Popisuje tunely a šifrovací klíče cíle.

Všechna data v netDb jsou podepsána vydavatelem a opatřena časovým razítkem, aby se předešlo útokům opakováním nebo zastaralými záznamy. Synchronizace času je udržována pomocí SNTP a detekce časového posunu na transportní vrstvě.

#### Additional concepts

- **Nepublikované a šifrované LeaseSets:**  
  Destinace může zůstat soukromá tím, že nepublikuje svůj LeaseSet a sdílí ho pouze s důvěryhodnými protějšky. Přístup vyžaduje příslušný dešifrovací klíč.

- **Bootstrapping (reseeding):**  
  Pro připojení k síti si nový router stáhne podepsané RouterInfo soubory z důvěryhodných HTTPS reseed serverů.

- **Škálovatelnost vyhledávání:**  
  I2P používá **iterativní**, nikoli rekurzivní vyhledávání pro zlepšení škálovatelnosti a bezpečnosti DHT.

---

### Tunely

Moderní I2P komunikace využívá dva plně šifrované transporty:

- **[NTCP2](/docs/specs/ntcp2):** Šifrovaný protokol založený na TCP  
- **[SSU2](/docs/specs/ssu2):** Šifrovaný protokol založený na UDP

Oba jsou postaveny na moderním [Noise Protocol Framework](https://noiseprotocol.org/), který poskytuje silné ověření a odolnost vůči identifikaci provozu. Nahradily zastaralé protokoly NTCP a SSU (plně vyřazeny od roku 2023).

**NTCP2** nabízí šifrované, efektivní streamování přes TCP.

**SSU2** poskytuje spolehlivost založenou na UDP, procházení NAT a volitelné proražení firewallu (hole punching). SSU2 je koncepčně podobný WireGuard nebo QUIC, vyvažuje spolehlivost a anonymitu.

Routery mohou podporovat jak IPv4, tak IPv6 a publikují své transportní adresy a náklady v netDb. Transportní protokol spojení je vybírán dynamicky pomocí **systému nabídek**, který optimalizuje podle podmínek a existujících spojení.

---

### Síťová databáze (netDb)

I2P používá vrstvené šifrování pro všechny komponenty: transporty, tunely, garlic zprávy a síťovou databázi.

Aktuální primitiva zahrnují:

- X25519 pro výměnu klíčů  
- EdDSA (Ed25519) pro podpisy  
- ChaCha20-Poly1305 pro autentizované šifrování  
- SHA-256 pro hashování  
- AES256 pro šifrování vrstvy tunelů

Starší algoritmy (ElGamal, DSA-SHA1, ECDSA) zůstávají kvůli zpětné kompatibilitě.

I2P v současnosti zavádí hybridní post-kvantová (PQ) kryptografická schémata kombinující **X25519** s **ML-KEM** za účelem ochrany proti útokům typu "harvest-now, decrypt-later" (sklizeň nyní, dešifrování později).

#### Garlic Messages

Garlic zprávy rozšiřují onion routing seskupením více šifrovaných "cloves" s nezávislými pokyny pro doručení. To umožňuje flexibilitu směrování na úrovni zpráv a jednotné doplňování provozu.

#### Session Tags

Pro end-to-end šifrování jsou podporovány dva kryptografické systémy:

- **ElGamal/AES+SessionTags (zastaralé):**  
  Používá předem dodané session tags jako 32-bajtové nonces. Nyní zastaralé kvůli neefektivitě.

- **ECIES-X25519-AEAD-Ratchet (současný):**  
  Používá ChaCha20-Poly1305 a synchronizované PRNG založené na HKDF pro dynamické generování dočasných session klíčů a 8-bajtových tagů, čímž snižuje nároky na CPU, paměť a šířku pásma při zachování forward secrecy (dopředné utajení).

---

## Future of the Protocol

Klíčové oblasti výzkumu se zaměřují na udržení bezpečnosti proti protivníkům na státní úrovni a zavedení post-kvantové ochrany. Dva rané designové koncepty — **restricted routes** a **variable latency** — byly nahrazeny moderním vývojem.

### Restricted Route Operation

Původní koncepty omezeného směrování měly za cíl skrýt IP adresy. Tato potřeba byla do značné míry zmírněna:

- UPnP pro automatické přesměrování portů  
- Robustní průchod NAT v SSU2  
- Podpora IPv6  
- Kooperativní introducers a NAT hole-punching  
- Volitelné připojení přes overlay (např. Yggdrasil)

Moderní I2P tedy dosahuje stejných cílů praktičtěji bez složitého omezeného směrování.

---

## Similar Systems

I2P integruje koncepty z message-oriented middleware (middlewaru orientovaného na zprávy), DHT (distribuovaných hash tabulek) a mixnets (směšovacích sítí). Jeho inovace spočívá v kombinaci těchto prvků do použitelné, samoorganizující se platformy pro anonymitu.

### Transportní protokoly

*[Webová stránka](https://www.torproject.org/)*

**Tor** a **I2P** sdílejí cíle, ale liší se architektonicky:

- **Tor:** Přepínání okruhů; spoléhá na důvěryhodné adresářové autority. (~10 tis. přenosových uzlů)  
- **I2P:** Přepínání paketů; plně distribuovaná síť řízená DHT. (~50 tis. routerů)

Jednosměrné tunnely I2P odhalují méně metadat a umožňují flexibilní směrovací cesty, zatímco Tor se zaměřuje na anonymní **přístup k internetu (outproxying)**. I2P místo toho podporuje anonymní **hosting v síti**.

### Kryptografie

*[Webová stránka](https://freenetproject.org/)*

**Freenet** se zaměřuje na anonymní, trvalé publikování a získávání souborů. **I2P** naproti tomu poskytuje **komunikační vrstvu v reálném čase** pro interaktivní použití (web, chat, torrenty). Společně se oba systémy doplňují — Freenet poskytuje úložiště odolné proti cenzuře; I2P poskytuje anonymitu při přenosu dat.

### Other Networks

- **Lokinet:** IP-založená překryvná síť využívající motivované servisní uzly.  
- **Nym:** Mixnet nové generace zdůrazňující ochranu metadat s krycím provozem při vyšší latenci.

---

## Appendix A: Application Layer

I2P samo o sobě zajišťuje pouze přenos zpráv. Funkcionalita aplikační vrstvy je implementována externě prostřednictvím API a knihoven.

### Streaming Library {#streaming}

**Streaming library** (knihovna pro proudové přenosy) funguje jako TCP analogie v I2P, se slidingovým okénkovým protokolem a řízením zahlcení optimalizovaným pro anonymní přenos s vysokou latencí.

Typické vzory HTTP požadavků/odpovědí mohou často být dokončeny v jediném přenosu tam a zpět díky optimalizacím sdružování zpráv.

### Naming Library and Address Book

*Vyvinuli: mihi, Ragnarok*   Viz stránka [Naming and Address Book](/docs/overview/naming).

Systém pojmenování I2P je **lokální a decentralizovaný**, čímž se vyhýbá globálním názvům ve stylu DNS. Každý router udržuje lokální mapování lidsky čitelných názvů na destinace. Volitelné adresáře založené na síti důvěry mohou být sdíleny nebo importovány od důvěryhodných uzlů.

Tento přístup se vyhýbá centralizovaným autoritám a obchází zranitelnosti typu Sybil inherentní v globálních nebo hlasovacích systémech pojmenování.

### Provoz v omezeném režimu tras

*Vyvinul: mihi*

**I2PTunnel** je hlavní rozhraní klientské vrstvy umožňující anonymní TCP proxying. Podporuje:

- **Tunely klienta** (odchozí k I2P destinacím)  
- **HTTP klient (eepproxy)** pro ".i2p" domény  
- **Tunely serveru** (příchozí z I2P k lokální službě)  
- **Tunely HTTP serveru** (bezpečný proxy pro webové služby)

Outproxying (směrem k běžnému internetu) je volitelné, implementované dobrovolnicky provozovanými "serverovými" tunnely.

### I2PSnark {#i2psnark}

*Vyvinuto: jrandom a další — portováno ze [Snark](http://www.klomp.org/snark/)*

Součástí I2P je **I2PSnark**, anonymní BitTorrent klient podporující více torrentů současně s DHT a UDP, přístupný přes webové rozhraní.

### Tor

*Vyvinuli: postman, susi23, mastiejaner*

**I2Pmail** poskytuje anonymní e-mail prostřednictvím I2PTunnel připojení. **Susimail** je webový klient vytvořený speciálně pro zabránění únikům informací běžným u tradičních e-mailových klientů. Služba [mail.i2p](https://mail.i2p/) nabízí filtrování virů, [hashcash](https://en.wikipedia.org/wiki/Hashcash) kvóty a oddělení outproxy pro dodatečnou ochranu.

---
