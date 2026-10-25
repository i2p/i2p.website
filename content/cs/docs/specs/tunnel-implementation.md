---
title: "Implementace tunnel"
description: "Specifikace provozu I2P tunnel, budování a zpracování zpráv"
slug: "tunnel-implementation"
aliases:
  - "/cs/docs/specs/implementation"
  - "/cs/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Tato stránka dokumentuje současnou implementaci tunnelů.

## Přehled tunnel {#tunnel.overview}

V rámci I2P jsou zprávy předávány jedním směrem skrze virtuální tunnel tvořený uzly, pomocí jakýchkoli dostupných prostředků k předání zprávy dalšímu uzlu. Zprávy dorazí na *gateway* tunnelu, kde jsou zabaleny a/nebo fragmentovány na tunnel zprávy pevné velikosti a předány dalšímu uzlu v tunnelu, který zprávu zpracuje, ověří její platnost a pošle ji dalšímu uzlu, a tak dále, dokud nedosáhne koncového bodu tunnelu. Tento *endpoint* vezme zprávy zabalené gateway a předá je podle instrukcí - buď jinému routeru, jinému tunnelu na jiném routeru, nebo lokálně.

Tunnely fungují všechny stejně, ale lze je rozdělit do dvou různých skupin - příchozí tunnely a odchozí tunnely. Příchozí tunnely mají nedůvěryhodnou bránu, která předává zprávy směrem dolů k tvůrci tunnelu, který slouží jako koncový bod tunnelu. U odchozích tunelů slouží tvůrce tunnelu jako brána, předávající zprávy ven ke vzdálenému koncovému bodu.

Tvůrce tunnelu vybírá přesně ty peery, kteří se budou tunnelu účastnit, a poskytuje každému z nich nezbytná konfigurační data. Mohou mít libovolný počet hopů. Záměrem je ztížit jak účastníkům, tak třetím stranám určení délky tunnelu, nebo dokonce spolupracujícím účastníkům určit, zda jsou vůbec součástí stejného tunnelu (s výjimkou situace, kdy jsou spolupracující peerové v tunnelu vedle sebe).

V praxi se používá série tunnel poolů pro různé účely - každá místní klientská destinace má svou vlastní sadu příchozích tunelů a odchozích tunelů, nakonfigurovaných tak, aby splňovaly její potřeby anonymity a výkonu. Kromě toho router sám udržuje sérii poolů pro účast v síťové databázi a pro správu samotných tunelů.

I2P je inherentně paketově přepínaná síť, dokonce i s těmito tunnely, což jí umožňuje využívat výhod více paralelně běžících tunnelů, čímž se zvyšuje odolnost a vyvažuje zatížení. Mimo základní vrstvu I2P je pro klientské aplikace k dispozici volitelná end-to-end streaming knihovna, která poskytuje TCP-podobné operace, včetně přeřazování zpráv, retransmise, řízení zahlcení atd.

Přehled terminologie I2P tunelů je [na stránce s přehledem tunelů](/docs/overview/tunnel-routing).

## Provoz tunelu (Zpracování zpráv) {#tunnel.operation}

### Přehled

Poté, co je tunnel vybudován, jsou [I2NP zprávy](/docs/specs/i2np) zpracovány a předány skrze něj. Provoz tunnelu má čtyři odlišné procesy, které jsou prováděny různými uzly v tunnelu.

1. Nejprve tunnel gateway nashromáždí určitý počet
   I2NP zpráv a předzpracuje je do tunnel zpráv pro
   doručení.
2. Dále tento gateway zašifruje tato předzpracovaná data a pak
   je předá prvnímu uzlu.
3. Tento uzel a následující účastníci tunnelu
   odstraní jednu vrstvu šifrování, ověří, že se nejedná o
   duplikát, a pak ji předají dalšímu uzlu.
4. Nakonec tunnel zprávy dorazí do koncového bodu, kde jsou I2NP zprávy
   původně sdružené gateway znovu sestaveny a předány dále podle
   požadavku.

Zprostředkující účastníci tunelu nevědí, zda se nacházejí v příchozím nebo odchozím tunelu; vždy "šifrují" pro další skok. Proto využíváme symetrické AES šifrování k "dešifrování" na odchozí bráně tunelu, takže prostý text je odhalen na odchozím koncovém bodě.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Zpracování Gateway {#tunnel.gateway}

#### Předzpracování zpráv {#tunnel.preprocessing}

Funkcí tunnel gateway je fragmentovat a zabalit [I2NP zprávy](/docs/specs/i2np) do tunnel zpráv s pevnou velikostí [tunnel messages](/docs/specs/tunnel-message) a tyto tunnel zprávy zašifrovat. Tunnel zprávy obsahují následující:

- 4bajtové Tunnel ID
- 16bajtový IV (inicializační vektor)
- Kontrolní součet
- Výplň, pokud je potřeba
- Jeden nebo více párů { instrukce doručení, fragment I2NP zprávy }

Tunnel ID jsou 4bytová čísla používaná na každém přeskoku - účastníci vědí, na které tunnel ID mají naslouchat zprávám a na které tunnel ID je mají předávat dalšímu přeskoku, přičemž každý přeskok si volí tunnel ID, na kterém zprávy přijímá. Tunnely samotné jsou krátkodobé (10 minut). I když jsou následné tunnely vybudovány pomocí stejné sekvence uzlů, tunnel ID každého přeskoku se změní.

Aby se zabránilo protivníkům označovat zprávy podél cesty úpravou velikosti zprávy, všechny tunnel zprávy mají pevnou velikost 1024 bajtů. Pro podporu větších I2NP zpráv i efektivnější zpracování menších zpráv gateway rozděluje větší I2NP zprávy na fragmenty obsažené v každé tunnel zprávě. Koncový bod se bude po krátkou dobu snažit znovu sestavit I2NP zprávu z fragmentů, ale podle potřeby je zahodí.

Podrobnosti jsou v [specifikaci tunnel zpráv](/docs/specs/tunnel-message).

### Šifrování brány

Po předzpracování zpráv do vyplněného payloadu gateway vytvoří náhodnou 16bajtovou IV hodnotu, iterativně ji a tunnel zprávu šifruje podle potřeby a předává tuple {tunnelID, IV, šifrovaná tunnel zpráva} dalšímu hop.

Způsob šifrování na gateway závisí na tom, zda se jedná o inbound nebo outbound tunnel. U inbound tunnelů jednoduše vyberou náhodný IV, postprocessingem jej aktualizují pro generování IV pro gateway a používají tento IV společně s vlastním layer klíčem k šifrování předzpracovaných dat. U outbound tunnelů musí iterativně dešifrovat (nešifrovaný) IV a předzpracovaná data pomocí IV a layer klíčů pro všechny hopsy v tunnelu. Výsledkem šifrování outbound tunnelu je, že když jej každý peer zašifruje, endpoint obnoví původní předzpracovaná data.

### Zpracování účastníka {#tunnel.participant}

Když peer obdrží tunnel zprávu, zkontroluje, že zpráva přišla ze stejného předchozího uzlu jako předtím (inicializuje se při příchodu první zprávy tunelem). Pokud je předchozí peer jiný router, nebo pokud byla zpráva již dříve viděna, zpráva je zahozena. Účastník poté zašifruje obdržené IV pomocí AES256/ECB s použitím svého IV klíče pro určení aktuálního IV, použije toto IV se svým vrstvovým klíčem účastníka k zašifrování dat, znovu zašifruje aktuální IV pomocí AES256/ECB s použitím svého IV klíče a poté předá tuple {nextTunnelId, nextIV, encryptedData} dalšímu uzlu. Toto dvojité šifrování IV (jak před, tak po použití) pomáhá řešit určitou třídu konfirmačních útoků.

Detekce duplicitních zpráv je řešena pomocí rozpadajícího se Bloom filtru na IV zpráv. Každý router udržuje jediný Bloom filtr obsahující XOR IV a prvního bloku přijaté zprávy pro všechny tunely, kterých se účastní, upravený tak, aby zahozoval viděné záznamy po 10-20 minutách (když tunely vyprší). Velikost bloom filtru a použité parametry jsou dostatečné k více než saturaci síťového připojení routeru se zanedbatelnou pravděpodobností falešně pozitivního výsledku. Jedinečná hodnota vkládaná do Bloom filtru je XOR IV a prvního bloku, aby se zabránilo nesekvenčním spolupracujícím peerům v tunelu označit zprávu jejím opětovným odesláním s prohozeným IV a prvním blokem.

### Zpracování koncového bodu {#tunnel.endpoint}

Po přijetí a ověření tunnel zprávy na posledním uzlu v tunnelu závisí způsob, jakým koncový bod obnoví data zakódovaná bránou, na tom, zda se jedná o inbound nebo outbound tunnel. Pro outbound tunnely koncový bod zašifruje zprávu pomocí svého layer klíče stejně jako jakýkoli jiný účastník, čímž odhalí předzpracovaná data. Pro inbound tunnely je koncový bod také tvůrcem tunnelu, takže může jednoduše iterativně dešifrovat IV a zprávu pomocí layer a IV klíčů každého kroku v opačném pořadí.

V tomto okamžiku má koncový bod tunelu předzpracovaná data odeslaná bránou, která pak může analyzovat na zahrnuté I2NP zprávy a předat je dále podle pokynů pro doručení.

## Budování tunelů {#tunnel.building}

Při budování tunnelu musí tvůrce odeslat požadavek s nezbytnými konfiguračními daty každému z hopů a čekat, až všichni souhlasí, než tunnel povolí. Požadavky jsou šifrovány tak, aby pouze peeři, kteří potřebují znát určitou informaci (jako je tunnel layer nebo IV klíč), měli tato data. Navíc pouze tvůrce tunnelu bude mít přístup k odpovědi peera. Při vytváření tunnelů je třeba mít na paměti tři důležité rozměry: jací peeři se používají (a kde), jak se požadavky odesílají (a odpovědi přijímají) a jak se udržují.

### Výběr peerů {#tunnel.peerselection}

Kromě dvou typů tunnelů - příchozích a odchozích - existují dva styly výběru peerů používané pro různé tunnely - průzkumné a klientské. Průzkumné tunnely se používají jak pro údržbu síťové databáze, tak pro údržbu tunnelů, zatímco klientské tunnely se používají pro end-to-end klientské zprávy.

#### Výběr peerů pro průzkumné tunnely {#tunnel.selection.exploratory}

Explorační tunnely jsou vybudovány z náhodného výběru peerů z podmnožiny sítě. Konkrétní podmnožina se liší podle lokálního routeru a podle toho, jaké jsou jeho potřeby pro tunnel routing. Obecně jsou explorační tunnely vybudovány z náhodně vybraných peerů, kteří jsou v kategorii profilu peera "nefunkční, ale aktivní". Sekundárním účelem tunnelů, kromě pouhého tunnel routingu, je najít nedostatečně využité peery s vysokou kapacitou, aby mohly být povýšeny pro použití v klientských tunnelech.

Exploratorní výběr peerů je dále diskutován na [stránce Profilování a výběr peerů](/docs/overview/peer-selection).

#### Výběr peerů pro klientský tunnel {#tunnel.selection.client}

Klientské tunnely jsou budovány s přísnějšími požadavky - místní router vybere protějšky ze své kategorie profilů "rychlé a vysoká kapacita", aby výkon a spolehlivost splňovaly potřeby klientské aplikace. Existuje však několik důležitých detailů nad rámec tohoto základního výběru, které by měly být dodržovány v závislosti na anonymitních potřebách klienta.

Výběr klientských peerů je dále probírán na [stránce o profilování a výběru peerů](/docs/overview/peer-selection).

#### Řazení uzlů v tunelech {#ordering}

Peery jsou v tunnelech uspořádány tak, aby se vypořádaly s [útokem předchůdce](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([aktualizace z roku 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

Pro zmaření predecessor útoku udržuje výběr tunnelů partnery seřazené ve striktním pořadí - pokud jsou A, B a C v tunnelu pro konkrétní tunnel pool, skok po A je vždy B a skok po B je vždy C.

Řazení je implementováno generováním náhodného 32-bajtového klíče pro každý tunnel pool při spuštění. Uzly by neměly být schopné uhodnout řazení, jinak by útočník mohl vytvořit dva router hashe daleko od sebe, aby maximalizoval šanci být na obou koncích tunnelu. Uzly jsou seřazeny podle XOR vzdálenosti SHA256 hashe (hash uzlu zřetězený s náhodným klíčem) od náhodného klíče:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Protože každý tunnel pool používá jiný náhodný klíč, řazení je konzistentní v rámci jednoho pool, ale ne mezi různými pool. Nové klíče se generují při každém restartu routeru.

### Doručení požadavku {#tunnel.request}

Multi-hop tunnel je vybudován pomocí jediné build zprávy, která je opakovaně dešifrována a předávána dále. V terminologii [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) se jedná o "neinteraktivní" teleskopické budování tunnelů.

Tato metoda přípravy, doručení a odpovědi na žádost o tunnel je [navržena](/docs/specs/tunnel-creation) tak, aby snížila počet odhalených předchůdců, omezila počet přenášených zpráv, ověřila správné připojení a vyhnula se útoku počítání zpráv při tradičním teleskopickém vytváření tunnelů. (Tato metoda, která posílá zprávy pro rozšíření tunnelu přes již vytvořenou část tunnelu, je v článku "Hashing it out" označována jako "interaktivní" teleskopické budování tunnelů.)

Podrobnosti o zprávách požadavků a odpovědí tunelů a jejich šifrování [jsou specifikovány zde](/docs/specs/tunnel-creation).

Protějšky mohou odmítnout žádosti o vytvoření tunelu z různých důvodů, přičemž jsou známy čtyři postupně závažnější typy odmítnutí: pravděpodobnostní odmítnutí (kvůli blížící se kapacitě routeru nebo v reakci na zahlcení požadavky), dočasné přetížení, přetížení šířky pásma a kritické selhání. Když jsou tyto čtyři typy přijaty, tvůrce tunelu je interpretuje, aby pomohl upravit svůj profil daného routeru.

Pro více informací o profilování peerů viz [stránka Profilování a výběr peerů](/docs/overview/peer-selection).

### Tunnel Pools {#tunnel.pooling}

Pro zajištění efektivního provozu si router udržuje sérii tunnel poolů, z nichž každý spravuje skupinu tunelů používaných pro konkrétní účel se svou vlastní konfigurací. Když je potřeba tunnel pro daný účel, router náhodně vybere jeden z příslušného poolu. Celkově existují dva průzkumné tunnel pooly - jeden příchozí a jeden odchozí - každý používající výchozí konfiguraci routeru. Navíc existuje pár poolů pro každou lokální destinaci - jeden příchozí a jeden odchozí tunnel pool. Tyto pooly používají konfiguraci specifikovanou při připojení lokální destinace k routeru prostřednictvím [I2CP](/docs/specs/i2cp), nebo výchozí nastavení routeru, pokud není specifikována.

Každý pool má ve své konfiguraci několik klíčových nastavení, která definují kolik tunnelů udržovat aktivních, kolik záložních tunnelů udržovat v případě selhání, jak dlouhé by tunnely měly být, zda by tyto délky měly být randomizované, stejně jako jakákoli jiná nastavení povolená při konfiguraci jednotlivých tunnelů. Možnosti konfigurace jsou specifikovány na [I2CP stránce](/docs/specs/i2cp).

### Délky tunnelů a výchozí hodnoty {#length}

[Na stránce s přehledem tunelů](/docs/overview/tunnel-routing#length).

### Předvídavá strategie budování a priority {#strategy}

Budování tunnelů je nákladné a tunnely vypršejí po pevně stanoveném čase od jejich vytvoření. Nicméně když pool vyčerpá tunnely, Destination je v podstatě mrtvá. Navíc úspěšnost budování tunnelů se může značně lišit v závislosti na místních i globálních síťových podmínkách. Proto je důležité udržovat předvídavou, adaptivní strategii budování, která zajistí úspěšné vytvoření nových tunnelů před tím, než jsou potřeba, aniž by se vytvářel nadbytek tunnelů, budovaly se příliš brzy, nebo spotřebovávalo příliš mnoho CPU či šířky pásma na vytváření a odesílání šifrovaných zpráv pro budování.

Pro každou n-tici {exploratory/client, in/out, délka, variance délky} router udržuje statistiky času potřebného pro úspěšné vybudování tunelu. Pomocí těchto statistik vypočítává, jak dlouho před vypršením tunelu by měl začít s pokusy o vybudování náhrady. Jak se blíží čas vypršení bez úspěšné náhrady, spouští více pokusů o vybudování paralelně a pak v případě potřeby zvýší počet paralelních pokusů.

Aby se omezila šířka pásma a využití CPU, router také omezuje maximální počet současně probíhajících pokusů o vybudování napříč všemi pooly. Kritická vybudování (ta pro průzkumné tunnely a pro pooly, kterým došly tunnely) mají prioritu.

## Omezování zpráv tunnel {#tunnel.throttling}

Ačkoli tunnely v rámci I2P připomínají síť s přepínáním okruhů, vše v I2P je striktně založeno na zprávách - tunnely jsou pouze účetní triky, které pomáhají organizovat doručování zpráv. Nepředpokládá se spolehlivost ani pořadí zpráv a opětovné přenosy jsou ponechány vyšším vrstvám (např. streamovací knihovně klientské vrstvy I2P). To umožňuje I2P využívat techniky regulace dostupné jak u sítí s přepínáním paketů, tak u sítí s přepínáním okruhů. Například každý router může sledovat klouzavý průměr množství dat, které každý tunnel používá, kombinovat ho se všemi průměry používanými ostatními tunnely, kterých se router účastní, a být schopen přijímat nebo odmítat další žádosti o účast v tunnelu na základě své kapacity a využití. Na druhou stranu každý router může jednoduše zahazovat zprávy, které jsou nad jeho kapacitu, čímž využívá výzkum používaný na běžném internetu.

V současné implementaci routery implementují strategii váženého náhodného předčasného zahazování (WRED). Pro všechny zúčastněné routery (interní účastník, příchozí brána a odchozí koncový bod) začne router náhodně zahazovat část zpráv, když se blíží k omezením šířky pásma. Jak se provoz blíží k limitům nebo je překračuje, více zpráv je zahozeno. U interního účastníka jsou všechny zprávy fragmentovány a doplněny a mají tedy stejnou velikost. Na příchozí bráně a odchozím koncovém bodě se však rozhodnutí o zahození provádí na úplné (sloučené) zprávě a velikost zprávy je brána v úvahu. Větší zprávy mají vyšší pravděpodobnost zahození. Také zprávy mají vyšší pravděpodobnost zahození na odchozím koncovém bodě než na příchozí bráně, protože tyto zprávy nejsou tak "daleko" ve své cestě, a proto jsou síťové náklady na zahození těchto zpráv nižší.

## Budoucí práce {#future}

### Míchání/Dávkování {#tunnel.mixing}

Jaké strategie by mohly být použity na gateway a na každém hopu pro zpoždění, přeuspořádání, přesměrování nebo doplnění zpráv? Do jaké míry by to mělo být prováděno automaticky, kolik by mělo být nakonfigurováno jako nastavení na tunnel nebo na hop, a jak by měl tvůrce tunnelu (a tím pádem uživatel) řídit tuto operaci? Vše toto zůstává neznámé a bude vyřešeno pro některou vzdálenou budoucí verzi.

### Vyplnění

Strategie paddingu lze použít na různých úrovních, čímž se řeší odhalení informací o velikosti zpráv různým protivníkům. Aktuální pevná velikost tunnel zprávy je 1024 bajtů. Avšak fragmentované zprávy samotné nejsou tunelem vůbec paddovány, ačkoliv u end-to-end zpráv mohou být paddovány jako součást garlic wrappingu.

### WRED

Strategie WRED mají významný dopad na end-to-end výkon a prevenci zhroucení sítě kvůli přetížení. Současná strategie WRED by měla být pečlivě vyhodnocena a vylepšena.
