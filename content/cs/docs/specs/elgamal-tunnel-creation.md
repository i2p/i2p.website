---
title: "Specifikace vytváření tunelů (ElGamal)"
description: "Starší specifikace budování tunelů založená na ElGamal, nahrazená X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/cs/tunnel-alt-creation"
  - "/cs/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Přehled {#tunnelcreate-overview}

POZNÁMKA: ZASTARALÉ - Toto je specifikace vytváření tunelů ElGamal. Aktuální metodu najdete ve [specifikaci vytváření tunelů X25519](/docs/specs/tunnel-creation-ecies).

Tento dokument specifikuje detaily šifrovaných zpráv pro vytváření tunnelů pomocí metody "neinteraktivního teleskopování". Pro přehled procesu, včetně metod výběru a řazení peerů, viz dokument o vytváření tunnelů [TUNNEL-IMPL](/docs/specs/tunnel-implementation).

Vytvoření tunelu je dosaženo jedinou zprávou předávanou podél cesty peerů v tunelu, přepsanou na místě a přenášenou zpět k tvůrci tunelu. Tato jediná zpráva tunelu se skládá z proměnného počtu záznamů (až 8) - jeden pro každý potenciální peer v tunelu. Jednotlivé záznamy jsou asymetricky (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) šifrované tak, aby je mohl číst pouze konkrétní peer podél cesty, zatímco na každém skoku je přidána dodatečná symetrická vrstva šifrování (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) tak, aby byl asymetricky šifrovaný záznam odhalen pouze ve vhodnou chvíli.

### Počet záznamů {#number}

Ne všechny záznamy musí obsahovat platná data. Zpráva pro sestavení 3-hop tunnel může například obsahovat více záznamů, aby se skutečná délka tunnel skryla před účastníky. Existují dva typy zpráv pro sestavení. Původní Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) obsahuje 8 záznamů, což je více než dostatečné pro jakoukoliv praktickou délku tunnel. Novější Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) obsahuje 1 až 8 záznamů. Původce může vybalancovat velikost zprávy s požadovanou mírou obfuskace délky tunnel.

V současné síti má většina tunnelů délku 2 nebo 3 hopů. Současná implementace používá 5záznamový VTBM pro budování tunnelů o 4 hopech nebo méně a 8záznamový TBM pro delší tunnely. 5záznamový VTBM (který po fragmentaci se vejde do tří 1KB tunnel zpráv) snižuje síťový provoz a zvyšuje úspěšnost budování, protože menší zprávy se s menší pravděpodobností ztrácejí.

Odpověď musí být stejného typu a délky jako zpráva pro sestavení.

### Specifikace záznamu požadavku {#tunnelcreate-requestrecord}

Také specifikováno ve specifikaci I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Čistý text záznamu, viditelný pouze pro hop, který je dotazován:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Pole dalšího tunnel ID a hash identity dalšího routeru se používají k určení dalšího skoku v tunnelu, ačkoli pro koncový bod odchozího tunnelu určují, kam má být odeslána přepsaná odpověď na vytvoření tunnelu. Kromě toho další message ID určuje ID zprávy, které by zpráva (nebo odpověď) měla použít.

Klíč tunnel vrstvy, tunnel IV klíč, klíč odpovědi a IV odpovědi jsou každý náhodné 32-bajtové hodnoty generované tvůrcem, pro použití pouze v tomto záznamu žádosti o sestavení.

Pole flags obsahuje následující:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit 7 označuje, že hop bude inbound gateway (IBGW). Bit 6 označuje, že hop bude outbound endpoint (OBEP). Pokud není nastaven žádný z bitů, hop bude intermediate participant. Oba nemohou být nastaveny současně.

#### Vytvoření záznamu požadavku

Každý hop dostane náhodné Tunnel ID, nenulové. Jsou vyplněny aktuální a další-hop Tunnel ID. Každý záznam dostane náhodný tunnel IV klíč, reply IV, layer klíč a reply klíč.

#### Šifrování záznamů požadavků {#encryption}

Tento cleartext záznam je zašifrován ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) s veřejným šifrovacím klíčem hopu a naformátován do 528 bajtového záznamu:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
V 512-bytovém šifrovaném záznamu obsahují ElGamal data byty 1-256 a 258-513 z 514-bytového ElGamal šifrovaného bloku [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Dva výplňové byty z bloku (nulové byty na pozicích 0 a 257) jsou odstraněny.

Protože cleartext používá celé pole, není potřeba žádné další padding kromě `SHA256(cleartext) + cleartext`.

Každý 528-bajtový záznam je poté iterativně zašifrován (pomocí AES dešifrování, s odpovědním klíčem a odpovědním IV pro každý hop), takže identita routeru bude v čitelné podobě pouze pro příslušný hop.

### Zpracování hopů a šifrování {#tunnelcreate-hopprocessing}

Když hop obdrží TunnelBuildMessage, prohledá záznamy v něm obsažené a hledá takový, který začíná vlastním identity hash (zkráceným na 16 bajtů). Poté dešifruje ElGamal blok z tohoto záznamu a získá chráněný cleartext. V tomto okamžiku se ujistí, že požadavek na tunnel není duplikát tím, že vloží AES-256 reply klíč do Bloom filtru. Duplikáty nebo neplatné požadavky jsou zahozeny. Záznamy, které nejsou označeny aktuální hodinou, nebo předchozí hodinou pokud je krátce po začátku hodiny, musí být zahozeny. Například vezměte hodinu v časovém razítku, převeďte na celý čas, poté pokud je více než 65 minut pozadu nebo 5 minut napřed od aktuálního času, je neplatný. Bloom filtr musí mít trvání alespoň jednu hodinu (plus několik minut pro povolení posunu hodin), takže duplikované záznamy v aktuální hodině, které nejsou odmítnuty kontrolou časového razítka hodiny v záznamu, budou odmítnuty filtrem.

Poté, co se rozhodnou, zda budou souhlasit s účastí v tunnel nebo ne, nahradí záznam, který obsahoval požadavek, zašifrovaným blokem odpovědi. Všechny ostatní záznamy jsou zašifrovány pomocí AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) s přiloženým klíčem odpovědi a IV. Každý je zašifrován pomocí AES/CBC samostatně se stejným klíčem odpovědi a IV odpovědi. CBC režim není pokračován (zřetězen) napříč záznamy.

Každý hop zná pouze svou vlastní odpověď. Pokud souhlasí, bude tunnel udržovat až do vypršení, i když nebude používán, protože nemůže vědět, zda souhlasily i všechny ostatní hopy.

#### Specifikace Reply Record {#tunnelcreate-replyrecord}

Poté, co aktuální hop přečte svůj záznam, nahradí jej odpovědním záznamem udávajícím, zda souhlasí s účastí v tunnel, a pokud ne, klasifikuje svůj důvod odmítnutí. Toto je jednoduše 1 bajtová hodnota, kde 0x0 znamená, že souhlasí s účastí v tunnel, a vyšší hodnoty znamenají vyšší úrovně odmítnutí.

Definovány jsou následující kódy odmítnutí:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Aby se před protějšky skryly jiné příčiny, jako je vypnutí routeru, současná implementace používá TUNNEL_REJECT_BANDWIDTH pro téměř všechna odmítnutí.

Odpověď je zašifrována AES session klíčem doručeným v zašifrovaném bloku, doplněna 495 bajty náhodných dat pro dosažení plné velikosti záznamu. Padding je umístěn před stavovým bajtem:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Toto je také popsáno ve specifikaci I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### Příprava zprávy pro vytvoření tunnelu {#tunnelcreate-requestpreparation}

Při vytváření nové Tunnel Build Message musí být nejprve sestaveny všechny Build Request Records a asymetricky šifrovány pomocí ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Každý záznam je pak preventivně dešifrován pomocí odpovědních klíčů a IV předchozích hopů v cestě, za použití AES [CRYPTO-AES](/docs/specs/cryptography#AES). Toto dešifrování by mělo být spuštěno v opačném pořadí, aby se asymetricky šifrovaná data objevila v čitelné podobě na správném hopu poté, co je jejich předchůdce zašifruje.

Přebytečné záznamy, které nejsou potřebné pro jednotlivé požadavky, jsou jednoduše vyplněny náhodnými daty tvůrcem.

### Doručení zprávy o vytvoření tunelu {#tunnelcreate-requestdelivery}

Pro odchozí tunnely se doručování provádí přímo od tvůrce tunnelu k prvnímu uzlu, přičemž se TunnelBuildMessage zabalí, jako by byl tvůrce jen dalším uzlem v tunnelu. Pro příchozí tunnely se doručování provádí prostřednictvím existujícího odchozího tunnelu. Odchozí tunnel obecně pochází ze stejného poolu jako nový tunnel, který se buduje. Pokud v tomto poolu není k dispozici žádný odchozí tunnel, použije se odchozí exploratory tunnel. Při spuštění, když ještě neexistuje žádný odchozí exploratory tunnel, se použije falešný 0-hop odchozí tunnel.

### Zpracování koncového bodu zprávy pro výstavbu tunnelu {#tunnelcreate-endpointhandling}

Pro vytvoření odchozího tunelu, když požadavek dosáhne odchozího koncového bodu (jak je určeno příznakem 'povolit zprávy komukoliv'), skok je zpracován obvyklým způsobem, šifruje odpověď místo záznamu a šifruje všechny ostatní záznamy, ale protože neexistuje žádný 'další skok', na který by se TunnelBuildMessage přeposlala, místo toho umístí šifrované záznamy odpovědi do TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) nebo VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (typ zprávy a počet záznamů se musí shodovat s požadavkem) a doručí ji do reply tunelu specifikovaného v záznamu požadavku. Tento reply tunel přepošle Tunnel Build Reply Message zpět tvůrci tunelu, stejně jako u jakékoli jiné zprávy [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). Tvůrce tunelu ji poté zpracuje, jak je popsáno níže.

Reply tunnel byl vybrán tvůrcem následovně: Obecně se jedná o příchozí tunnel ze stejného poolu jako nový odchozí tunnel, který se buduje. Pokud v tomto poolu není k dispozici žádný příchozí tunnel, použije se příchozí exploratory tunnel. Při startu, kdy ještě neexistuje žádný příchozí exploratory tunnel, se použije falešný 0-hop příchozí tunnel.

Pro vytvoření inbound tunnel, když požadavek dorazí do inbound endpoint (také známého jako tvůrce tunelu), není potřeba generovat explicitní Tunnel Build Reply Message a router zpracovává každou z odpovědí následovně.

### Zpracování zprávy odpovědi na vytvoření tunnel {#tunnelcreate-replyprocessing}

Pro zpracování záznamů odpovědí musí tvůrce jednoduše AES dešifrovat každý záznam jednotlivě, použitím reply key a IV každého hopu v tunnelu po peer (v opačném pořadí). Tím se odhalí odpověď specifikující, zda souhlasí s účastí v tunnelu nebo proč odmítají. Pokud všichni souhlasí, tunnel je považován za vytvořený a může být okamžitě používán, ale pokud kdokoliv odmítne, tunnel je zahozen.

Souhlasy a odmítnutí jsou zaznamenány v profilu každého peer [PEER-SELECTION](/docs/overview/peer-selection), aby byly použity při budoucích hodnoceních kapacity tunnel daného peer.

## Historie a poznámky {#tunnelcreate-notes}

Tato strategie vznikla během diskuze na I2P mailing listu mezi Michaelem Rogersem, Matthew Toselandem (toad) a jrandom ohledně predecessor útoku. Viz [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Byla představena ve verzi 0.6.1.10 dne 2006-02-16, což bylo naposledy, kdy byla v I2P provedena změna nekompatibilní se starší verzí.

Poznámky:

- Toto řešení nebrání dvěma nepřátelským protějškům uvnitř tunelu označit jeden nebo více záznamů požadavků nebo odpovědí, aby zjistili, že se nacházejí ve stejném tunelu, ale takové jednání může být tvůrcem tunelu odhaleno při čtení odpovědi, což způsobí označení tunelu jako neplatného.

- Tento návrh neobsahuje proof of work pro asymetricky
  šifrovanou sekci, ačkoli by 16bajtový hash identity mohl být zkrácen na polovinu a
  druhá polovina nahrazena hashcash funkcí s náklady až 2^64.

- Tento návrh sám o sobě nebrání dvěma nepřátelským peerům uvnitř tunnelu v použití časových informací k určení, zda se nacházejí ve stejném tunnelu. Mohlo by pomoci použití dávkového a synchronizovaného doručování požadavků (seskupování požadavků a jejich odeslání v (ntp-synchronizovanou) minutu). Avšak takový přístup umožňuje peerům 'označit' požadavky jejich zpožděním a pozdějším odhalením tohoto zpoždění v tunnelu, i když možná by fungovalo zahazování požadavků nedoručených v malém časovém okně (ačkoli by to vyžadovalo vysoký stupeň synchronizace hodin). Alternativně by možná jednotlivé skoky mohly vložit náhodné zpoždění před předáním požadavku dále?

- Existují nějaké neškodlivé metody označování požadavku?

- Časové razítko s rozlišením jedné hodiny se používá pro prevenci opakovaných útoků. Omezení nebylo vynucováno až do vydání verze 0.9.16.

## Budoucí práce {#future}

- V současné implementaci ponechává odesílatel jeden záznam prázdný
  pro sebe. Tak zpráva s n záznamy může vybudovat pouze tunnel s n-1 skoky.
  To se zdá být nutné pro příchozí tunnely (kde předposlední skok
  může vidět hash prefix pro další skok), ale ne pro odchozí tunnely.
  Toto je třeba prozkoumat a ověřit. Pokud je možné použít
  zbývající záznam bez kompromitování anonymity, měli bychom tak učinit.

- Další analýza možných útoků označováním a časováním popsaných ve výše uvedených poznámkách.

- Používejte pouze VTBM; nevybírejte staré peery, které to nepodporují.

- Build Request Record nespecifikuje životnost tunnel nebo vypršení;
  každý hop vyprší tunnel po 10 minutách, což je konstanta pevně zakódovaná
  v celé síti. Mohli bychom použít bit v poli flag a vzít 4 (nebo 8)
  bajtů z paddingu pro specifikaci životnosti nebo vypršení. Žadatel
  by tuto možnost specifikoval pouze pokud by ji všichni účastníci podporovali.

## Reference {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
