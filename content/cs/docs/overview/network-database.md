---
title: "Síťová databáze"
description: "Porozumění distribuované síťové databázi I2P (netDb) - specializované DHT pro kontaktní informace routerů a vyhledávání destinací"
slug: "network-database"
aliases:
  - "/cs/how_networkdatabase"
  - "/cs/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Přehled

I2P netDb je specializovaná distribuovaná databáze, obsahující pouze dva typy dat - kontaktní informace routerů (**RouterInfos**) a kontaktní informace destinací (**LeaseSets**). Každý kus dat je podepsán příslušnou stranou a ověřen kýmkoli, kdo ho používá nebo ukládá. Kromě toho data obsahují informace o aktuálnosti, což umožňuje zahodit irelevantní záznamy, nahradit starší záznamy novějšími a poskytuje ochranu proti určitým třídám útoků.

netDb je distribuována pomocí jednoduché techniky nazvané "floodfill", kde podmnožina všech routerů, nazývaná "floodfill routery", udržuje distribuovanou databázi.

---

## RouterInfo

Když se I2P router chce spojit s jiným routerem, potřebuje znát některé klíčové údaje - všechny jsou zabaleny a podepsány routerem do struktury nazvané "RouterInfo", která je distribuována s SHA256 identity routeru jako klíčem. Samotná struktura obsahuje:

- Identita routeru (šifrovací klíč, podpisový klíč a certifikát)
- Kontaktní adresy, na kterých je dosažitelný
- Kdy bylo toto publikováno
- Sada libovolných textových možností
- Podpis výše uvedeného, vygenerovaný podpisovým klíčem identity

### Očekávané možnosti

Následující textové možnosti, ačkoli nejsou striktně vyžadovány, se očekává, že budou přítomny:

- **caps** (Příznaky schopností - používané k označení účasti floodfill, přibližné šířky pásma a vnímané dosažitelnosti)
  - **D**: Střední přetížení (od verze 0.9.58)
  - **E**: Vysoké přetížení (od verze 0.9.58)
  - **f**: Floodfill
  - **G**: Odmítá všechny tunely (od verze 0.9.58)
  - **H**: Skrytý
  - **K**: Pod 12 KBps sdílené šířky pásma
  - **L**: 12 - 48 KBps sdílené šířky pásma (výchozí)
  - **M**: 48 - 64 KBps sdílené šířky pásma
  - **N**: 64 - 128 KBps sdílené šířky pásma
  - **O**: 128 - 256 KBps sdílené šířky pásma
  - **P**: 256 - 2000 KBps sdílené šířky pásma (od verze 0.9.20, viz poznámka níže)
  - **R**: Dosažitelný
  - **U**: Nedosažitelný
  - **X**: Nad 2000 KBps sdílené šířky pásma (od verze 0.9.20, viz poznámka níže)

"Shared bandwidth" == (share %) * min(in bw, out bw)

Pro kompatibilitu se staršími routery může router publikovat více písmen šířky pásma, například "PO".

Poznámka: hranice mezi třídami šířky pásma P a X může být buď 2000 nebo 2048 KBps, podle volby implementátora.

- **netId** = 2 (Základní kompatibilita sítě - router odmítne komunikovat s uzlem mající jiné netId)
- **router.version** (Používá se k určení kompatibility s novějšími funkcemi a zprávami)

Poznámky k R/U schopnostem: Router by obvykle měl publikovat schopnost R nebo U, pokud není stav dosažitelnosti aktuálně neznámý. R znamená, že router je přímo dosažitelný (nepotřebuje introducery, není za firewallem) na alespoň jedné transportní adrese. U znamená, že router NENÍ přímo dosažitelný na ŽÁDNÉ transportní adrese.

Zastaralé možnosti: - ~~coreVersion~~ (Nikdy nepoužíváno, odstraněno ve vydání 0.9.24) - ~~stat_uptime~~ = 90m (Nepoužíváno od verze 0.7.9, odstraněno ve vydání 0.9.24)

Tyto hodnoty používají ostatní routery pro základní rozhodnutí. Měli bychom se k tomuto routeru připojit? Měli bychom se pokusit směrovat tunnel přes tento router? Příznak schopnosti šířky pásma se používá pouze k určení, zda router splňuje minimální práh pro směrování tunelů. Nad minimálním prahem se inzerovaná šířka pásma nikde v routeru nepoužívá ani nedůvěřuje, kromě zobrazení v uživatelském rozhraní a pro ladění a analýzu sítě.

Platná čísla NetID:

| Použití | Číslo NetID |
|---------|-------------|
| Rezervováno | 0 |
| Rezervováno | 1 |
| Současná síť (výchozí) | 2 |
| Rezervované budoucí sítě | 3 - 15 |
| Forky a testovací sítě | 16 - 254 |
| Rezervováno | 255 |
### Další možnosti

Další textové možnosti zahrnují malý počet statistik o stavu routeru, které jsou agregovány weby jako [stats.i2p](http://stats.i2p/) pro analýzu výkonu sítě a ladění. Tyto statistiky byly vybrány tak, aby poskytly data klíčová pro vývojáře, jako jsou míry úspěšnosti budování tunelů, přičemž vyvažují potřebu takových dat s vedlejšími efekty, které by mohly vyplynout z odhalení těchto dat. Současné statistiky jsou omezeny na:

- Úspěšnost, odmítnutí a časové limity při budování průzkumných tunelů
- Hodinový průměr počtu zúčastněných tunelů

Tyto údaje jsou volitelné, ale pokud jsou zahrnuty, pomáhají při analýze výkonu celé sítě. Od API 0.9.58 jsou tyto statistiky zjednodušené a standardizované takto:

- Klíče opcí jsou stat_(název_statistiky).(období_statistiky)
- Hodnoty opcí jsou oddělené ';'
- Statistiky pro počty událostí nebo normalizovaná procenta používají 4. hodnotu; první tři hodnoty nejsou použité, ale musí být přítomné
- Statistiky pro průměrné hodnoty používají 1. hodnotu a oddělovač ';' není vyžadován
- Pro rovnoměrné vážení všech routerů v analýze statistik a pro dodatečnou anonymitu by routery měly tyto statistiky zahrnovat pouze po době provozu jedné hodiny nebo více, a pouze jednou z každých 16 publikování RI.

Příklad:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routery mohou publikovat dodatečná data o počtu záznamů ve své síťové databázi. Tyto údaje jsou volitelné, ale pokud jsou zahrnuty, pomáhají při analýze výkonu celé sítě.

Následující dvě možnosti by měly být zahrnuty floodfill routery v každém publikovaném RI:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Příklad:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Data publikovaná v uživatelském rozhraní routeru lze zobrazit, ale nejsou používána ani důvěryhodná pro žádný jiný router.

### Možnosti rodiny

Od verze 0.9.24 mohou routery deklarovat, že jsou součástí "rodiny", provozované stejnou entitou. Více routerů ze stejné rodiny nebude použito v jediném tunnelu.

Možnosti family jsou:

- **family** (Název rodiny)
- **family.key** Kód typu podpisu [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) rodiny (v ASCII číslicích) spojený s ':' spojeným se Signing Public Key v base 64
- **family.sig** Podpis ((název rodiny v UTF-8) spojeného s (32 bajtový router hash)) v base 64

### Vypršení RouterInfo

RouterInfos nemají nastavenou dobu vypršení. Každý router si může svobodně udržovat svou vlastní místní politiku pro vyvažování frekvence vyhledávání RouterInfo s využitím paměti nebo disku. V současné implementaci existují následující obecné politiky:

- Během první hodiny provozu nedochází k expiraci, protože persistentně uložená data mohou být stará.
- Nedochází k expiraci, pokud je k dispozici 25 nebo méně RouterInfos.
- S rostoucím počtem místních RouterInfos se doba expirace zkracuje ve snaze udržet rozumný počet RouterInfos. Doba expirace při méně než 120 routerech je 72 hodin, zatímco doba expirace při 300 routerech je kolem 30 hodin.
- RouterInfos obsahující [SSU](/docs/legacy/ssu/) introducery expirují přibližně za hodinu, protože seznam introducerů expiruje přibližně za tuto dobu.
- Floodfilly používají krátkou dobu expirace (1 hodina) pro všechny místní RouterInfos, protože platné RouterInfos budou často znovu publikovány.

### Trvalé ukládání RouterInfo

RouterInfos jsou pravidelně zapisovány na disk, takže jsou dostupné po restartu.

Může být žádoucí trvale ukládat Meta LeaseSets s dlouhými dobami expirace. Toto je závislé na implementaci.

### Viz také

- [Specifikace RouterInfo](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

Druhým typem dat distribuovaných v netDb je "LeaseSet" - dokumentující skupinu **vstupních bodů tunelů (leases)** pro konkrétní cílové místo klienta. Každý z těchto leasů specifikuje následující informace:

- Gateway router tunelu (specifikací jeho identity)
- ID tunelu na daném routeru pro odesílání zpráv (4bajtové číslo)
- Kdy vyprší platnost daného tunelu.

Samotný leaseSet je uložen v netDb pod klíčem odvozeným z SHA256 destinace. Jedna výjimka platí pro šifrované leaseSety (LS2) od verze 0.9.38. Pro DHT klíč se používá SHA256 typu byte (3) následovaný zaslepeným veřejným klíčem, který se poté rotuje obvyklým způsobem. Viz sekce Kademlia Closeness Metric níže.

Kromě těchto leasů leaseSet zahrnuje:

- Samotná destination (šifrovací klíč, podepisovací klíč a certifikát)
- Dodatečný veřejný šifrovací klíč: používá se pro end-to-end šifrování garlic zpráv
- Dodatečný veřejný podepisovací klíč: určený pro zrušení leaseSet, ale momentálně se nepoužívá.
- Podpis všech dat leaseSet, aby bylo zajištěno, že destination publikovala leaseSet.

- [Specifikace Lease](/docs/specs/common-structures/#struct_Lease)
- [Specifikace LeaseSet](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

Od verze 0.9.38 jsou definovány tři nové typy LeaseSets; LeaseSet2, MetaLeaseSet a EncryptedLeaseSet. Viz níže.

### Nepublikované LeaseSets

LeaseSet pro cíl používaný pouze pro odchozí spojení je *nepublikovaný*. Nikdy není odeslán k publikaci na floodfill router. "Klientské" tunely, jako jsou ty pro procházení webu a IRC klienty, jsou nepublikované. Servery budou stále schopny posílat zprávy zpět na tyto nepublikované cíle díky [I2NP storage zprávám](#leaseset-storage-to-peers).

### Odvolané LeaseSets

LeaseSet může být *odvolán* publikováním nového LeaseSet s nulovými leases. Odvolání musí být podepsána dodatečným podpisovým klíčem v LeaseSet. Odvolání nejsou plně implementována a není jasné, zda mají nějaké praktické využití. Toto je jediné plánované použití pro tento podpisový klíč, takže je v současnosti nepoužíván.

### LeaseSet2 (LS2)

Od verze 0.9.38 floodfilly podporují novou strukturu LeaseSet2. Tato struktura je velmi podobná staré struktuře LeaseSet a slouží ke stejnému účelu. Nová struktura poskytuje flexibilitu potřebnou pro podporu nových typů šifrování, více typů šifrování, možností, offline podpisových klíčů a dalších funkcí. Podrobnosti najdete v návrhu 123.

### Meta LeaseSet (LS2)

Od verze 0.9.38 podporují floodfills novou strukturu Meta LeaseSet. Tato struktura poskytuje stromovou strukturu v DHT pro odkazování na jiné LeaseSets. Pomocí Meta LeaseSets může web implementovat velké služby s více domovy, kde je pro poskytování společné služby používáno několik různých Destinations. Záznamy v Meta LeaseSet jsou Destinations nebo jiné Meta LeaseSets a mohou mít dlouhé doby vypršení, až 18,2 hodin. Pomocí této funkce by mělo být možné provozovat stovky nebo tisíce Destinations hostujících společnou službu. Podrobnosti viz návrh 123.

### Šifrované LeaseSets (LS1)

Tato sekce popisuje starý, nezabezpečený způsob šifrování leaseSetů pomocí pevného symetrického klíče. Viz níže pro verzi LS2 šifrovaných leaseSetů.

V *šifrovaném* LeaseSet jsou všechny Lease šifrovány samostatným klíčem. Lease mohou být dekódovány, a tedy cíl může být kontaktován, pouze těmi, kdo mají klíč. Neexistuje žádný příznak nebo jiná přímá indikace, že LeaseSet je šifrovaný. Šifrované LeaseSet nejsou široce používány a je to téma pro budoucí práci, aby se prozkoumalo, zda by mohlo být zlepšeno uživatelské rozhraní a implementace šifrovaných LeaseSet.

### Šifrované LeaseSety (LS2)

Od vydání 0.9.38 floodfilly podporují novou strukturu EncryptedLeaseSet. Destination je skrytá a floodfill vidí pouze zaslepený veřejný klíč a datum vypršení. Strukturu mohou dešifrovat pouze ti, kteří mají úplnou Destination. Struktura je uložena v DHT lokaci založené na hashi zaslepeného veřejného klíče, ne na hashi Destination. Podrobnosti viz návrh 123.

### Vypršení platnosti LeaseSet

Pro běžné LeaseSets je expirace čas nejpozdější expirace jeho leasů. Pro nové datové struktury LeaseSet2 je expirace specifikována v hlavičce. Pro LeaseSet2 by měla expirace odpovídat nejpozdější expiraci jeho leasů. Pro EncryptedLeaseSet a MetaLeaseSet se může expirace lišit a maximální expirace může být vynucena, což bude teprve určeno.

### Trvalé úložiště LeaseSet

Není vyžadováno trvalé ukládání dat LeaseSet, protože tak rychle expirují. Nicméně trvalé ukládání dat EncryptedLeaseSet a MetaLeaseSet s dlouhými expiracioními lhůtami může být vhodné.

### Výběr šifrovacího klíče (LS2)

LeaseSet2 může obsahovat více šifrovacích klíčů. Klíče jsou seřazeny podle preferencí serveru, nejvíce preferovaný je první. Výchozí chování klienta je vybrat první klíč s podporovaným typem šifrování. Klienti mohou použít jiné algoritmy výběru založené na podpoře šifrování, relativním výkonu a dalších faktorech.

---

## Bootstrapping

netDb je decentralizovaná, nicméně potřebujete alespoň jeden odkaz na peer, aby vás proces integrace propojil. Toho se dosáhne "reseedováním" vašeho routeru pomocí RouterInfo aktivního peera - konkrétně získáním jejich souboru `routerInfo-$hash.dat` a uložením do vašeho adresáře `netDb/`. Tyto soubory vám může poskytnout kdokoli - můžete je dokonce poskytovat dalším zpřístupněním vlastního adresáře netDb. Pro zjednodušení procesu dobrovolníci publikují své adresáře netDb (nebo jejich část) na běžné (non-i2p) síti a URL těchto adresářů jsou napevno zakódovány v I2P. Když se router spouští poprvé, automaticky stáhne data z jedné z těchto URL, vybrané náhodně.

---

## Floodfill

Floodfill netDb je jednoduchý distribuovaný úložný mechanismus. Algoritmus ukládání je prostý: pošli data nejbližšímu uzlu, který se inzeroval jako floodfill router. Když uzel ve floodfill netDb obdrží netDb úložiště od uzlu, který není ve floodfill netDb, pošle ho podmnožině floodfill netDb-uzlů. Vybrané uzly jsou ty nejbližší (podle [XOR-metriky](#kademlia-closeness-metric)) ke konkrétnímu klíči.

Určit, kdo je součástí floodfill netDb, je triviální - je to vystaveno v publikovaných routerInfo každého routeru jako schopnost.

Floodfills nemají žádnou centrální autoritu a netvoří "konsenzus" - pouze implementují jednoduchou DHT vrstvu.

### Přihlášení k floodfill routeru

Na rozdíl od Toru, kde jsou directory servery napevno zakódované a důvěryhodné, a provozované známými entitami, členové I2P floodfill peer sady nemusí být důvěryhodní a mění se v čase.

Pro zvýšení spolehlivosti netDb a minimalizaci dopadu netDb provozu na router je floodfill automaticky povoleno pouze na routerech, které jsou nakonfigurovány s vysokými omezeními šířky pásma. Routery s vysokými omezeními šířky pásma (které musí být ručně nakonfigurovány, protože výchozí hodnota je mnohem nižší) se předpokládá, že jsou na připojeních s nižší latencí a s větší pravděpodobností budou dostupné 24/7. Současná minimální sdílená šířka pásma pro floodfill router je 128 KBytes/sec.

Navíc musí router projít několika dalšími testy zdraví (čas fronty odchozích zpráv, zpoždění úloh atd.) předtím, než je automaticky povolena floodfill operace.

S aktuálními pravidly pro automatické přihlášení je přibližně 6 % routerů v síti floodfill routery.

Zatímco někteří peeři jsou manuálně nakonfigurováni jako floodfill, jiní jsou jednoduše vysokopásmové routery, které se automaticky nabídnou, když počet floodfill peerů klesne pod práh. To zabraňuje jakémukoli dlouhodobému poškození sítě ze ztráty většiny nebo všech floodfill v důsledku útoku. Na oplátku se tyto peery samy odhlásí z floodfill, když je příliš mnoho floodfill aktivních.

### Role floodfill routerů

Jediné služby floodfill routeru, které jsou navíc oproti službám běžných routerů, spočívají v přijímání netDb záznamů a odpovídání na netDb dotazy. Protože mají obecně vysokou šířku pásma, je pravděpodobnější, že se budou účastnit velkého počtu tunelů (tj. budou "relay" pro ostatní), ale toto není přímo spojeno s jejich službami distribuované databáze.

---

## Kademlia metrika blízkosti

netDb používá jednoduchou Kademlia XOR metriku k určení blízkosti. Pro vytvoření Kademlia klíče se vypočítá SHA256 hash RouterIdentity nebo Destination. Jedinou výjimkou jsou Encrypted LeaseSets (LS2) od verze 0.9.38. Pro DHT klíč se používá SHA256 z type byte (3) následovaného blinded public key a poté se rotuje obvyklým způsobem.

Modifikace tohoto algoritmu se provádí za účelem zvýšení nákladů na [Sybil útoky](#sybil-attack-partial-keyspace). Místo SHA256 hashe vyhledávaného nebo uloženého klíče se bere SHA256 hash 32-bytového binárního vyhledávacího klíče připojeného k UTC datu reprezentovanému jako 8-bytový ASCII řetězec yyyyMMdd, tj. SHA256(key + yyyyMMdd). Toto se nazývá "routing key" a mění se každý den o půlnoci UTC. Pouze vyhledávací klíč je tímto způsobem modifikován, ne hashe floodfill routerů. Denní transformace DHT se někdy nazývá "keyspace rotation", i když to není přísně vzato rotace.

Routing klíče se nikdy neposílají po síti v žádné I2NP zprávě, používají se pouze lokálně pro určení vzdálenosti.

---

## Segmentace síťové databáze - Poddatabáze

Tradičně se Kademlia-style DHT nezabývají zachováváním nespojitelnosti informací uložených na konkrétním uzlu v DHT. Například část informace může být uložena do jednoho uzlu v DHT a poté bezpodmínečně vyžádána zpět z tohoto uzlu. V rámci I2P a při použití netDb tomu tak není - informace uložené v DHT mohou být sdíleny pouze za určitých známých okolností, kdy je to "bezpečné". Toto opatření má zabránit třídě útoků, kdy se škodlivý aktér může pokusit asociovat klientský tunnel s routerem tím, že pošle store do klientského tunnelu a poté si jej přímo vyžádá zpět od podezřelého "Hostitele" klientského tunnelu.

### Struktura segmentace

I2P routery mohou implementovat účinné obrany proti této třídě útoků za předpokladu splnění několika podmínek. Implementace network database by měla být schopna sledovat, zda byl databázový záznam přijat přes client tunnel nebo přímo. Pokud byl přijat přes client tunnel, měla by také sledovat, přes který client tunnel byl přijat, pomocí lokální destination klienta. Pokud byl záznam přijat přes více client tunnelů, pak by netDb měla sledovat všechny destination, kde byl záznam pozorován. Měla by také sledovat, zda byl záznam přijat jako odpověď na vyhledání, nebo jako store.

V implementacích Java i C++ je toho dosaženo použitím jediné "hlavní" netDb pro přímé vyhledávání a floodfill operace. Tato hlavní netDb existuje v kontextu routeru. Poté je každému klientovi poskytnuta vlastní verze netDb, která se používá k zachycení databázových záznamů odeslaných do klientských tunelů a k odpovídání na vyhledávání poslaná do klientských tunelů. Nazýváme je "Klientské síťové databáze" nebo "Sub-databáze" a existují v kontextu klienta. NetDb provozovaná klientem existuje pouze po dobu životnosti klienta a obsahuje pouze záznamy, které komunikují s klientskými tunely. To znemožňuje překrývání záznamů odeslaných do klientských tunelů se záznamy odeslanými přímo do routeru.

Dodatečně musí být každý netDb schopen si pamatovat, zda byl databázový záznam přijat proto, že byl poslán na jednu z našich destinací, nebo proto, že jsme si ho vyžádali jako součást vyhledávání. Pokud byl databázový záznam přijat jako uložení, tedy když nám ho poslal nějaký jiný router, pak by netDb měl odpovídat na žádosti o záznam, když si jiný router vyhledá klíč. Pokud však byl přijat jako odpověď na dotaz, pak by netDb měl odpovědět na dotaz ohledně záznamu pouze v případě, že záznam již byl uložen na stejnou destinaci. Klient by nikdy neměl odpovídat na dotazy se záznamem z hlavního netDb, pouze ze své vlastní klientské síťové databáze.

Tyto strategie by měly být převzaty a použity v kombinaci, aby byly aplikovány obě. V kombinaci "segmentují" netDb a zabezpečují ji proti útokům.

---

## Mechanismy ukládání, ověřování a vyhledávání

### Ukládání RouterInfo k protějškům

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages obsahující místní RouterInfo se vyměňují s peery jako součást inicializace transportního spojení [NTCP](/docs/specs/ntcp2/) nebo [SSU](/docs/specs/ssu2/).

### Ukládání LeaseSet do peerů

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages obsahující místní leaseSet jsou pravidelně vyměňovány s protějšky jejich zabalením do garlic zprávy spolu s normálním provozem ze související Destination. To umožňuje odeslání úvodní odpovědi a pozdějších odpovědí na příslušný Lease, aniž by byly vyžadovány jakékoli leaseSet vyhledávání nebo aby komunikující Destinations musely vůbec publikovat leaseSets.

### Výběr Floodfill

DatabaseStoreMessage by měla být odeslána floodfill routeru, který je nejblíže aktuálnímu routing klíči pro RouterInfo nebo LeaseSet, který je ukládán. V současnosti je nejbližší floodfill nalezen vyhledáváním v lokální databázi. I když tento floodfill není ve skutečnosti nejbližší, rozešle jej "blíže" odesláním několika dalším floodfill routerům. To poskytuje vysokou míru odolnosti proti chybám.

V tradičním Kademlia by peer provedl vyhledávání "find-closest" před vložením položky do DHT k nejbližšímu cíli. Protože operace ověření má tendenci objevovat bližší floodfilly, pokud jsou přítomny, router rychle zlepší své znalosti o DHT "okolí" pro RouterInfo a LeaseSets, které pravidelně publikuje. Ačkoli I2NP nedefinuje zprávu "find-closest", pokud to bude nutné, router může jednoduše provést iterativní vyhledávání klíče s překlopeným nejméně významným bitem (tj. key ^ 0x01), dokud nebudou v DatabaseSearchReplyMessages přijímány žádní bližší peerové. To zajišťuje, že skutečně nejbližší peer bude nalezen i v případě, že vzdálenější peer měl netdb položku.

### Ukládání RouterInfo do Floodfills

Router publikuje svůj vlastní RouterInfo tím, že se přímo připojí k floodfill routeru a pošle mu [I2NP](/docs/specs/i2np/) DatabaseStoreMessage s nenulovým Reply Token. Zpráva není end-to-end garlic šifrovaná, protože se jedná o přímé spojení, takže neexistují žádné mezilehlé routery (a není třeba tato data skrývat). Floodfill router odpoví [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, s Message ID nastaveným na hodnotu Reply Token.

Za určitých okolností může router také odeslat RouterInfo DatabaseStoreMessage prostřednictvím průzkumného tunelu; například kvůli limitům připojení, nekompatibilitě připojení nebo snaze skrýt skutečnou IP adresu před floodfill uzlem. Floodfill uzel nemusí takové uložení přijmout v době přetížení nebo na základě jiných kritérií; zda explicitně prohlásit nepřímé ukládání RouterInfo za nezákonné je téma pro další studium.

### Úložiště LeaseSet do Floodfills

Ukládání LeaseSets je mnohem citlivější než u RouterInfos, protože router se musí postarat o to, aby LeaseSet nemohl být spojen s routerem.

Router publikuje lokální LeaseSet odesláním [I2NP](/docs/specs/i2np/) DatabaseStoreMessage s nenulovým Reply Token přes odchozí klientský tunel pro tuto Destination. Zpráva je end-to-end garlic šifrována pomocí Session Key Manager této Destination, aby byla zpráva skryta před odchozím koncovým bodem tunelu. Floodfill router odpoví [I2NP](/docs/specs/i2np/) DeliveryStatusMessage s Message ID nastaveným na hodnotu Reply Token. Tato zpráva je poslána zpět do jednoho z příchozích tunelů klienta.

### Flooding

Stejně jako každý router, floodfill používá různá kritéria pro ověření LeaseSet nebo RouterInfo před jejich lokálním uložením. Tato kritéria mohou být adaptivní a závislá na aktuálních podmínkách včetně současného zatížení, velikosti netDb a dalších faktorů. Veškeré ověření musí být provedeno před flooding.

Poté, co floodfill router obdrží DatabaseStoreMessage obsahující platný RouterInfo nebo LeaseSet, který je novější než ten dříve uložený v jeho lokální NetDb, "zaplavuje" jej. Pro zaplavení NetDb záznamu vyhledá několik (aktuálně 3) floodfill routerů nejblíže routing key NetDb záznamu. (Routing key je SHA256 Hash RouterIdentity nebo Destination s připojeným datem (yyyyMMdd).) Zaplavováním těch nejblíže klíči, ne nejblíže sobě, floodfill zajišťuje, že úložiště se dostane na správné místo, i když ukládající router neměl dobrou znalost DHT "sousedství" pro routing key.

Floodfill se pak přímo připojí ke každému z těchto peerů a pošle mu [I2NP](/docs/specs/i2np/) DatabaseStoreMessage s nulovým Reply Token. Zpráva není end-to-end garlic šifrovaná, protože se jedná o přímé spojení, takže neexistují žádné zprostředkující routery (a není ani potřeba tato data skrývat). Ostatní routery neodpovídají ani znovu nezaplavují, protože Reply Token je nula.

Floodfills nesmí provádět flood prostřednictvím tunnelů; DatabaseStoreMessage musí být odeslána přes přímé spojení.

Floodfilly nesmí nikdy zaplavit prošlý leaseSet nebo RouterInfo publikovaný před více než jednou hodinou.

### Vyhledávání RouterInfo a LeaseSet

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage se používá k vyžádání záznamu netDb od floodfill routeru. Vyhledávání se odesílají přes jeden z výchozích průzkumných tunelů routeru. Odpovědi jsou specifikovány tak, aby se vrátily přes jeden z příchozích průzkumných tunelů routeru.

Vyhledávání jsou obecně posílána paralelně ke dvěma "dobrým" (připojení neselže) floodfill routerům nejbližším k požadovanému klíči.

Pokud je klíč nalezen lokálně floodfill routerem, odpoví [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Pokud klíč není nalezen lokálně floodfill routerem, odpoví [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage obsahující seznam dalších floodfill routerů blízkých k danému klíči.

LeaseSet vyhledávání jsou garlic encrypted end-to-end od vydání 0.9.5. RouterInfo vyhledávání nejsou šifrována a jsou tak zranitelná vůči odposlouchávání výstupním koncovým bodem (OBEP) klientského tunelu. To je způsobeno nákladností ElGamal šifrování. Šifrování RouterInfo vyhledávání může být povoleno v budoucím vydání.

Od verze 0.9.7 budou odpovědi na vyhledávání LeaseSet (DatabaseStoreMessage nebo DatabaseSearchReplyMessage) šifrovány pomocí zahrnutí session klíče a tagu ve vyhledávání. Tím se odpověď skryje před inbound gateway (IBGW) odpovědního tunelu. Odpovědi na vyhledávání RouterInfo budou šifrovány, pokud povolíme šifrování vyhledávání.

(Reference: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sekce 2.2-2.3 pro níže uvedené termíny v kurzívě)

Vzhledem k relativně malé velikosti sítě a redundanci flooding je vyhledávání obvykle O(1) spíše než O(log n). Router má vysokou pravděpodobnost, že zná floodfill router dostatečně blízko klíči, aby získal odpověď na první pokus. Ve verzích před 0.8.9 používaly routery redundanci vyhledávání dva (to znamená, že dvě vyhledávání byla prováděna paralelně k různým uzlům) a nebylo implementováno ani *rekurzivní*, ani *iterativní* směrování pro vyhledávání. Dotazy byly zasílány *více trasami současně*, aby se *snížila pravděpodobnost selhání dotazu*.

Od verze 0.8.9 jsou implementována *iterativní vyhledávání* bez redundance vyhledávání. Jedná se o efektivnější a spolehlivější vyhledávání, které bude fungovat mnohem lépe, když nejsou známi všichni floodfill uzly, a odstraňuje vážné omezení růstu sítě. Jak síť roste a každý router zná pouze malou podmnožinu floodfill uzlů, vyhledávání se stanou O(log n). I když uzel nevrátí odkazy blíže ke klíči, vyhledávání pokračuje s dalším nejbližším uzlem, pro zvýšenou robustnost a prevenci škodlivého floodfill uzlu před vytvořením černé díry v části klíčového prostoru. Vyhledávání pokračuje, dokud není dosaženo celkového časového limitu vyhledávání nebo dokud není dotázán maximální počet uzlů.

*ID uzlů* jsou *ověřitelné* v tom, že používáme router hash přímo jak jako ID uzlu, tak jako klíč Kademlia. Nesprávné odpovědi, které nejsou blíže k vyhledávacímu klíči, jsou obecně ignorovány. Vzhledem k současné velikosti sítě má router *podrobné znalosti o okolí cílového prostoru ID*.

### Ověření úložiště RouterInfo

Poznámka: Ověřování RouterInfo je od verze 0.9.7.1 zakázáno, aby se zabránilo útoku popsanému v článku [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf). Není jasné, zda lze ověřování přepracovat tak, aby bylo možné jej provádět bezpečně.

Pro ověření úspěšného uložení router jednoduše počká asi 10 sekund, pak pošle vyhledávání jinému floodfill routeru blízko ke klíči (ale ne tomu, kterému bylo uložení odesláno). Vyhledávání jsou odesílána jedním z výstupních průzkumných tunelů routeru. Vyhledávání jsou end-to-end garlic šifrována, aby se zabránilo odposlouchávání výstupním koncovým bodem (OBEP).

### Ověření uložení LeaseSet

Pro ověření úspěšného uložení router jednoduše počká asi 10 sekund a pak pošle vyhledání jinému floodfill routeru blízkému ke klíči (ale ne tomu, kterému bylo uložení posláno). Vyhledání jsou posílána přes jeden z odchozích klientských tunelů pro cíl LeaseSet, který je ověřován. Pro zabránění odposlouchávání ze strany OBEP odchozího tunelu jsou vyhledání end-to-end garlic šifrována. Odpovědi jsou specifikovány tak, aby se vracely přes jeden z příchozích tunelů klienta.

Od verze 0.9.7 budou odpovědi pro vyhledávání RouterInfo i LeaseSet (DatabaseStoreMessage nebo DatabaseSearchReplyMessage) šifrovány, aby byla odpověď skryta před vstupní bránou (IBGW) odpovědního tunnelu.

### Průzkum

*Exploration* je speciální forma vyhledávání v netDb, kdy se router pokouší získat informace o nových routerech. Provádí to odesláním [I2NP](/docs/specs/i2np/) DatabaseLookup Message floodfill routeru, hledajíc náhodný klíč. Protože toto vyhledávání selže, floodfill by normálně odpověděl [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage obsahující hashe floodfill routerů blízkých danému klíči. To by nebylo užitečné, protože žádající router pravděpodobně tyto floodfilly již zná, a bylo by nepraktické přidat všechny floodfill routery do pole "nezahrnovat" DatabaseLookup Message. Pro exploration dotaz nastavuje žádající router speciální příznak v DatabaseLookup Message. Floodfill pak odpoví pouze s non-floodfill routery blízkými požadovanému klíči.

### Poznámky k odpovědím na vyhledávání

Odpověď na požadavek lookup je buď Database Store Message (při úspěchu) nebo Database Search Reply Message (při neúspěchu). DSRM obsahuje pole 'from' router hash pro označení zdroje odpovědi; DSM neobsahuje. Pole 'from' v DSRM není ověřeno a může být falšováno nebo neplatné. Neexistují žádné další odpovědní značky. Proto při vytváření více paralelních požadavků je obtížné sledovat výkonnost různých floodfill routerů.

---

## MultiHoming

Cíle mohou být hostovány na více routerech současně, pomocí stejných privátních a veřejných klíčů (tradičně uložených v souborech eepPriv.dat). Jelikož obě instance budou pravidelně publikovat své podepsané LeaseSets na floodfill peery, nejnověji publikovaný LeaseSet bude vrácen peerovi požadujícímu databázové vyhledání. Protože LeaseSets mají (maximálně) 10minutovou životnost, pokud konkrétní instance vypadne, výpadek bude trvat nejvýše 10 minut a obecně mnohem méně. Funkce multihoming byla ověřena a je používána několika službami v síti.

Od verze 0.9.38 podporují floodfilly novou strukturu Meta LeaseSet. Tato struktura poskytuje stromovou strukturu v DHT pro odkazování na další LeaseSety. Pomocí Meta LeaseSetů může stránka implementovat rozsáhlé multihomed služby, kde je několik různých Destinací použito k poskytování společné služby. Záznamy v Meta LeaseSetu jsou Destinace nebo další Meta LeaseSety a mohou mít dlouhé vypršení, až 18,2 hodin. Pomocí této funkce by mělo být možné provozovat stovky nebo tisíce Destinací hostujících společnou službu. Podrobnosti naleznete v návrhu 123.

---

## Analýza hrozeb

Také diskutováno na [stránce o modelu hrozeb](/docs/overview/threat-model/#floodfill).

Nepřátelský uživatel se může pokusit poškodit síť vytvořením jednoho nebo více floodfill routerů a jejich úpravou tak, aby poskytovaly špatné, pomalé nebo žádné odpovědi. Některé scénáře jsou popsány níže.

### Obecná mitigace prostřednictvím růstu

V síti je aktuálně kolem 1700 floodfill routerů. Většina následujících útoků se stane obtížnější nebo bude mít menší dopad, jak se velikost sítě a počet floodfill routerů zvýší.

### Obecná ochrana prostřednictvím redundance

Prostřednictvím flooding jsou všechny netDb záznamy uloženy na 3 floodfill routerech nejblíže ke klíči.

### Padělky

Všechny záznamy netDb jsou podepsané jejich tvůrci, takže žádný router nemůže padělit RouterInfo nebo LeaseSet.

### Pomalé nebo nereagující

Každý router udržuje rozšířenou sadu statistik v [peer profilu](/docs/overview/peer-selection/) pro každý floodfill router, pokrývající různé metriky kvality pro daný peer. Sada zahrnuje:

- Průměrná doba odezvy
- Procento dotazů zodpovězených s požadovanými daty
- Procento úložišť, která byla úspěšně ověřena
- Poslední úspěšné uložení
- Poslední úspěšné vyhledání
- Poslední odpověď

Pokaždé, když router potřebuje určit, který floodfill router je nejblíže ke klíči, používá tyto metriky k určení, které floodfill routery jsou "dobré". Metody a prahy používané k určení "dobroty" jsou relativně nové a podléhají dalšímu rozboru a vylepšování. Zatímco zcela nereagující router bude rychle identifikován a vyhneme se mu, routery, které jsou pouze občas škodlivé, může být mnohem těžší řešit.

### Sybil útok (úplný keyspace)

Útočník může provést [Sybil útok](https://www.freehaven.net/anonbib/cache/sybil.pdf) vytvořením velkého množství floodfill routerů rozložených po celém prostoru klíčů.

(V souvisejícím příkladu nedávno výzkumník vytvořil [velký počet Tor relayů](http://blog.torproject.org/blog/june-2010-progress-report).) Pokud by bylo úspěšné, mohlo by to být efektivním DOS útokem na celou síť.

Pokud se floodfills nechovají dostatečně špatně na to, aby byly označeny jako "špatné" pomocí výše popsaných metrik profilů uzlů, je to obtížný scénář k řešení. Odpověď sítě Tor může být v případě relay mnohem hbitější, protože podezřelé relay mohou být ručně odstraněny z konsensu. Níže jsou uvedeny některé možné odpovědi pro síť I2P, avšak žádná z nich není zcela uspokojivá:

- Sestavit seznam špatných hashe routerů nebo IP adres a oznámit seznam různými způsoby (zprávy v konzoli, webové stránky, fórum atd.); uživatelé by si museli seznam ručně stáhnout a přidat do svého lokálního "černého seznamu".
- Požádat všechny v síti, aby ručně povolili floodfill (bojovat proti Sybil útokům pomocí více Sybil útoků)
- Vydat novou verzi softwaru, která obsahuje hardcoded seznam "špatných" uzlů
- Vydat novou verzi softwaru, která vylepšuje metriky a prahové hodnoty profilů peerů, ve snaze automaticky identifikovat "špatné" peery.
- Přidat software, který diskvalifikuje floodfilly pokud je jich příliš mnoho v jednom IP bloku
- Implementovat automatický předplacený černý seznam kontrolovaný jedním jednotlivcem nebo skupinou. To by v podstatě implementovalo část Tor "consensus" modelu. Bohužel by to také dalo jednomu jednotlivci nebo skupině moc blokovat účast jakéhokoli konkrétního routeru nebo IP v síti, nebo dokonce úplně vypnout nebo zničit celou síť.

Tento útok se stává obtížnějším s rostoucí velikostí sítě.

### Sybil útok (částečný keyspace)

Útočník může provést [Sybil útok](https://www.freehaven.net/anonbib/cache/sybil.pdf) vytvořením malého počtu (8-15) floodfill routerů seskupených blízko v klíčovém prostoru a širokou distribucí RouterInfos pro tyto routery. Poté by všechna vyhledávání a ukládání pro klíč v daném klíčovém prostoru byla směrována na jeden z útočníkových routerů. Pokud by bylo úspěšné, mohlo by to být účinným DOS útokem například na konkrétní I2P Site.

Jelikož je prostor klíčů indexován kryptografickým (SHA256) hashem klíče, útočník musí použít metodu hrubé síly k opakovanému generování router hashů, dokud nemá dostatek hashů, které jsou dostatečně blízko klíči. Množství výpočetní síly potřebné k tomuto útoku, které závisí na velikosti sítě, není známo.

Jako částečná obrana proti tomuto útoku se algoritmus používaný k určení Kademlia "blízkosti" mění v čase. Namísto použití hash klíče (tj. H(k)) k určení blízkosti používáme hash klíče připojeného k aktuálnímu datovému řetězci, tj. H(k + YYYYMMDD). Funkce nazvaná "generátor routing klíče" to provádí a transformuje původní klíč na "routing klíč". Jinými slovy, celý prostor klíčů netDb se "otáčí" každý den o půlnoci UTC. Jakýkoliv útok na částečný prostor klíčů by musel být každý den znovu generován, protože po rotaci by útočící routery již nebyly blízko cílového klíče ani jeden druhému.

Tento útok se stává obtížnějším s růstem velikosti sítě. Nedávný výzkum však ukazuje, že rotace prostoru klíčů není obzvláště účinná. Útočník si může předpočítat množství hasher routerů předem a pouze několik routerů stačí k "zatmění" části prostoru klíčů během půl hodiny po rotaci.

Jedním důsledkem denní rotace keyspace je, že distribuovaná síťová databáze se může stát na několik minut po rotaci nespolehlivou -- vyhledávání selže, protože nový "nejbližší" router ještě neobdržel store. Rozsah tohoto problému a metody pro jeho zmírnění (například netDb "předání" o půlnoci) jsou tématem pro další studium.

### Bootstrap útoky

Útočník by se mohl pokusit nastartovat nové routery do izolované nebo většinově kontrolované sítě převzetím reseed webové stránky nebo oklamáním vývojářů, aby přidali jeho reseed webovou stránku do hardcoded seznamu v routeru.

Několik obran je možných a většina z nich je naplánována:

- Zakázat přepnutí z HTTPS na HTTP při reseedování. MITM útočník by mohl jednoduše zablokovat HTTPS a poté odpovědět na HTTP.
- Zahrnutí reseed dat do instalátoru

Implementované obranné mechanismy:

- Změna úlohy reseed tak, aby načítala podmnožinu RouterInfos z několika reseed stránek namísto používání pouze jedné stránky
- Vytvoření monitorovací služby reseed mimo síť, která pravidelně dotazuje reseed webové stránky a ověřuje, že data nejsou zastaralá nebo nekonzistentní s jinými pohledy na síť
- Od verze 0.9.14 jsou reseed data zabalena do podepsaného zip souboru a podpis je ověřen při stahování. Podrobnosti najdete ve [specifikaci su3](/docs/specs/updates/#su3).

### Zachycení dotazu

Viz také [lookup](#routerinfo-and-leaseset-lookup) (Reference: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sekce 2.2-2.3 pro níže uvedené termíny v kurzívě)

Podobně jako u bootstrap útoku se útočník používající floodfill router může pokusit "nasměrovat" protějšky na podmnožinu routerů, které ovládá, tím, že vrátí jejich reference.

Toto pravděpodobně nebude fungovat prostřednictvím průzkumu, protože průzkum je nízkofrekvenvční úloha. Routery získávají většinu svých peer referencí prostřednictvím běžné aktivity budování tunelů. Výsledky průzkumu jsou obecně omezeny na několik router hashů a každý průzkumový dotaz je směřován na náhodný floodfill router.

Od verze 0.8.9 jsou implementovány *iterativní vyhledávání*. Pro reference floodfill routerů vrácené v odpovědi [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage na vyhledávání jsou tyto reference následovány, pokud jsou blíže (nebo nejblíže) k vyhledávanému klíči. Žádající router nedůvěřuje tomu, že reference jsou blíže ke klíči (tj. jsou *ověřitelně správné*). Vyhledávání také nepřestane, když není nalezen bližší klíč, ale pokračuje dotazováním nejbližšího uzlu, dokud nedojde k timeout nebo není dosaženo maximálního počtu dotazů. Toto zabraňuje škodlivému floodfill routeru v "černé díře" části prostoru klíčů. Také denní rotace prostoru klíčů vyžaduje, aby útočník znovu vygeneroval router info v požadované oblasti prostoru klíčů. Tento design zajišťuje, že útok zachycení dotazů popsaný v [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) je mnohem obtížnější.

### Výběr Relay založený na DHT

(Reference: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sekce 3)

To nemá moc společného s floodfill, ale podívejte se na [stránku o výběru peerů](/docs/overview/peer-selection/) pro diskusi o zranitelnostech výběru peerů pro tunnely.

### Úniky informací

(Reference: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Sekce 3)

Tento dokument se zabývá slabostmi v DHT vyhledáváních "Finger Table" používaných systémy Torsk a NISAN. Na první pohled se nezdá, že by se tyto slabosti vztahovaly na I2P. Za prvé, použití DHT v systémech Torsk a NISAN se výrazně liší od použití v I2P. Za druhé, vyhledávání v síťové databázi I2P má pouze volnou souvislost s procesy [výběru peerů](/docs/overview/peer-selection/) a [budování tunelů](/docs/overview/tunnel-routing/); pro tunely se používají pouze dříve známí peerové. Také výběr peerů nesouvisí s žádným pojmem blízkosti DHT klíčů.

Některé z těchto věcí mohou být ve skutečnosti zajímavější, když se síť I2P výrazně rozroste. Právě teď každý router zná velkou část sítě, takže vyhledání konkrétní Router Info v síťové databázi není silným ukazatelem budoucího záměru použít tento router v tunelu. Možná až bude síť 100krát větší, bude vyhledávání více souviset s úmyslem. Samozřejmě, větší síť také ztěžuje Sybil útok.

Nicméně obecný problém úniku informací z DHT v I2P vyžaduje další zkoumání. Floodfill routery se nacházejí v pozici, kdy mohou pozorovat dotazy a shromažďovat informace. Určitě při úrovni *f* = 0,2 (20% škodlivých uzlů, jak je specifikováno v článku) očekáváme, že mnoho z Sybil hrozeb, které popisujeme ([zde](/docs/overview/threat-model/#sybil), [zde](#sybil-attack-full-keyspace) a [zde](#sybil-attack-partial-keyspace)), se stane problematickými z několika důvodů.

---

## Historie

[Přesunuto na diskusní stránku netdb](/docs/legacy/netdb/).

---

## Budoucí práce

End-to-end šifrování dodatečných netDb vyhledávání a odpovědí.

Lepší metody pro sledování odpovědí při vyhledávání.
