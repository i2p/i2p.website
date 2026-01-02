---
title: "Síťová databáze"
description: "Porozumění distribuované síťové databázi I2P (netDb) - specializovaná distribuovaná hashovací tabulka (DHT) pro kontaktní informace routerů a vyhledávání destinací"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Přehled

**netDb** je specializovaná distribuovaná databáze obsahující pouze dva typy dat: - **RouterInfos** – kontaktní informace routeru - **LeaseSets** – kontaktní informace destinace

Všechna data jsou kryptograficky podepsaná a ověřitelná. Každá položka obsahuje informace o liveness (živosti) pro vyřazování zastaralých položek a nahrazování neaktuálních, což chrání proti určitým třídám útoků.

Distribuce používá mechanismus **floodfill**, kde podmnožina routers udržuje distribuovanou databázi.

---

## 2. RouterInfo (informace o routeru)

Když routers potřebují kontaktovat jiné routers, vyměňují si balíčky **RouterInfo** obsahující:

- **Identita routeru** – šifrovací klíč, podpisový klíč, certifikát
- **Kontaktní adresy** – jak se spojit s routerem
- **Časové razítko publikace** – kdy byly tyto informace publikovány
- **Libovolné textové možnosti** – příznaky schopností a nastavení
- **Kryptografický podpis** – prokazuje pravost

### 2.1 Příznaky schopností

Routers uvádějí své schopnosti pomocí písmenných kódů ve svém RouterInfo (záznam informací o routeru):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Klasifikace šířky pásma

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Hodnoty ID sítě

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Statistiky RouterInfo

Routers zveřejňují volitelné statistiky stavu pro analýzu sítě: - Míry úspěchu/odmítnutí/vypršení časového limitu při sestavování Exploratory tunnel - 1hodinový průměr počtu účastnických tunnel

Statistiky se řídí formátem `stat_(statname).(statperiod)` s hodnotami oddělenými středníkem.

**Příklad statistik:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers mohou také publikovat: `netdb.knownLeaseSets` a `netdb.knownRouters`

### 2.5 Možnosti rodiny

Od verze 0.9.24 mohou routers deklarovat příslušnost k rodině (stejný provozovatel):

- **family**: Název rodiny
- **family.key**: Kód typu podpisu zřetězený s veřejným podpisovým klíčem kódovaným Base64
- **family.sig**: Podpis názvu rodiny a 32bajtového hashe routeru

Z jedné rodiny nebude v žádném jednotlivém tunnel použito více než jeden router.

### 2.6 Vypršení platnosti RouterInfo

- Žádné vypršení platnosti během první hodiny od spuštění
- Žádné vypršení platnosti při 25 nebo méně uložených RouterInfos
- Doba vypršení se zkracuje, jak roste místní počet (72 hodin při <120 routers; ~30 hodin při 300 routers)
- SSU introducers (zprostředkovatelé připojení) vyprší za ~1 hodinu
- Floodfills používají 1hodinové vypršení platnosti pro všechny místní RouterInfos

---

## 3. LeaseSet

**LeaseSets** dokumentují vstupní body pro tunnel pro konkrétní destinace a uvádějí:

- **Identita routeru brány tunnelu**
- **4bajtové ID tunnelu**
- **Čas vypršení platnosti tunnelu**

LeaseSets (struktury s údaji o dosažitelnosti cíle v I2P) zahrnují:
- **Destination** (identifikátor cíle) – šifrovací klíč, podpisový klíč, certifikát
- **Dodatečný veřejný šifrovací klíč** – pro end‑to‑end garlic encryption (technika sdružování zpráv v I2P)
- **Dodatečný veřejný podpisový klíč** – určen pro revokaci (aktuálně se nepoužívá)
- **Kryptografický podpis**

### 3.1 Varianty LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Vypršení platnosti LeaseSet

Běžné LeaseSets vyprší při nejpozdějším vypršení jejich lease (časově omezený záznam). Expirace LeaseSet2 je uvedena v hlavičce. Expirace u EncryptedLeaseSet a MetaLeaseSet se mohou lišit, s možným vynucením maximálního limitu.

---

## 4. Bootstrapping (inicializace)

Aby se router mohl začlenit do decentralizované netDb, je nutná alespoň jedna reference na peer. **Reseeding** (získání počátečních kontaktů) stahuje soubory RouterInfo (`routerInfo-$hash.dat`) z adresářů netDb dobrovolníků. Při prvním spuštění se automaticky stahuje z natvrdo zadaných URL vybraných náhodně.

---

## 5. Mechanismus Floodfill

floodfill netDb používá jednoduché distribuované ukládání: data se posílají nejbližšímu floodfill uzlu. Když uzly, které nejsou floodfill, posílají data k uložení, floodfill uzly je přepošlou podmnožině floodfill uzlů, které jsou nejblíže konkrétnímu klíči.

Účast v režimu floodfill je v RouterInfo označena jako příznak schopnosti (`f`).

### 5.1 Požadavky pro dobrovolné zapojení do Floodfill

Na rozdíl od natvrdo zabudovaných důvěryhodných adresářových serverů Toru je sada floodfillu (speciálních uzlů pro šíření netDb dat) v I2P **nedůvěryhodná** a v čase se mění.

Floodfill se automaticky aktivuje pouze na routers s vysokou šířkou pásma, které splňují tyto požadavky: - Minimálně 128 KBytes/sec sdílené šířky pásma (ručně nakonfigurované) - Musí projít dalšími testy stavu (čas fronty odchozích zpráv, zpoždění úloh)

Současné automatické opt-in (dobrovolné přihlášení) má za následek přibližně **6% účasti na floodfill v síti**.

Ručně nakonfigurované uzly floodfill existují souběžně s automatickými dobrovolníky. Když počet uzlů floodfill klesne pod práh, routers s vysokou šířkou pásma se automaticky přihlásí jako dobrovolníci. Když existuje příliš mnoho uzlů floodfill, zruší svůj status floodfill.

### 5.2 Role pro floodfill

Kromě přijímání zápisů do netDb a odpovídání na dotazy vykonávají floodfill uzly standardní funkce routeru. Jejich vyšší šířka pásma obvykle znamená větší zapojení do tunnel, ale to přímo nesouvisí s databázovými službami.

---

## 6. Metrika blízkosti v Kademlii

netDb používá měření vzdálenosti **ve stylu Kademlia** založené na XOR. Hash SHA256 z RouterIdentity (identita routeru) nebo Destination (cílová identita) vytváří klíč Kademlia (s výjimkou LS2 Encrypted LeaseSets, které používají SHA256 s typovým bajtem o hodnotě 3 a oslepený veřejný klíč).

### 6.1 Rotace klíčového prostoru

Aby se zvýšily náklady na útoky typu Sybil, namísto použití `SHA256(key)` systém používá:

```
SHA256(key + yyyyMMdd)
```
kde datum je osmibajtové ASCII datum UTC. Tím se vytvoří **směrovací klíč**, který se každý den o půlnoci UTC mění — což se nazývá **rotace klíčového prostoru**.

Směrovací klíče se nikdy nepřenášejí v I2NP zprávách; slouží pouze k lokálnímu určení vzdálenosti.

---

## 7. Segmentace síťové databáze

Tradiční Kademlia DHT nezachovávají nepropojitelnost uložených informací. I2P brání útokům, které spojují klientské tunnels s routers, implementací **segmentace**.

### 7.1 Strategie segmentace

Routers sledují: - Zda záznamy dorazily přes client tunnels nebo přímo - Pokud přes tunnel, který client tunnel/destinaci - Vícenásobné příchody přes tunnel se sledují - Rozlišují se odpovědi na uložení vs. na vyhledání

Obě implementace v Javě a C++ používají: - **"Hlavní" netDb** pro přímá vyhledávání/operace floodfill v kontextu routeru - **"Klientské síťové databáze"** nebo **"Podřízené databáze"** v klientských kontextech, zachycující záznamy zasílané do klientských tunnels

Klientské netDbs (databáze sítě) existují pouze po dobu životního cyklu klienta a obsahují jen záznamy z klientských tunnels. Záznamy z klientských tunnels se nesmí překrývat s těmi, které dorazí přímo.

Každá netDb sleduje, zda záznamy dorazily jako uložení (odpovídají na požadavky na vyhledávání) nebo jako odpovědi na vyhledávání (odpovídají pouze tehdy, pokud byly dříve uloženy pro stejný cíl). Klienti nikdy neodpovídají na dotazy pomocí záznamů hlavního netDb, pouze pomocí záznamů klientské síťové databáze.

Kombinované strategie **segmentují** netDb proti útokům na propojení klienta s routerem.

---

## 8. Ukládání, ověřování a vyhledávání

### 8.1 Ukládání RouterInfo u peerů

I2NP `DatabaseStoreMessage` obsahující lokální RouterInfo (informace o routeru) pro výměnu během inicializace transportního spojení NTCP nebo SSU.

### 8.2 Ukládání LeaseSet peerům

I2NP `DatabaseStoreMessage` obsahující lokální LeaseSet se periodicky vyměňují prostřednictvím zpráv šifrovaných pomocí garlic encryption, které jsou součástí provozu Destination (identifikátor cíle v I2P), což umožňuje odpovědi bez nutnosti vyhledávání LeaseSet.

### 8.3 Výběr floodfill

`DatabaseStoreMessage` odesílá na floodfill nejblíže aktuálnímu směrovacímu klíči. Nejbližší floodfill je nalezen prostřednictvím vyhledávání v místní databázi. I když ve skutečnosti nemusí být nejbližší, zaplavování jej rozšíří "blíže" tím, že jej odešle na více floodfill uzlů.

Tradiční Kademlia používá před vložením vyhledávání "find-closest". Zatímco I2NP takové zprávy nemá, routers mohou provádět iterativní vyhledávání s překlopeným nejméně významným bitem (`key ^ 0x01`), aby zajistily nalezení skutečně nejbližšího uzlu.

### 8.4 Ukládání RouterInfo do Floodfills

Routery publikují RouterInfo (informace o routeru) tak, že se přímo připojí k floodfillu a odešlou I2NP `DatabaseStoreMessage` s nenulovým Reply Tokenem (token pro odpověď). Zpráva není end-to-end garlic encrypted (přímé spojení, bez prostředníků). Floodfill odpoví `DeliveryStatusMessage` s použitím Reply Tokenu jako ID zprávy.

Routery mohou také posílat RouterInfo (datový záznam o routeru) přes průzkumný tunnel (limity připojení, nekompatibilita, skrývání IP). Floodfills mohou taková uložení během přetížení odmítnout.

### 8.5 Ukládání LeaseSet do Floodfillů

Ukládání LeaseSet je citlivější než RouterInfo. Routers musí zabránit přiřazení LeaseSet k sobě samým.

Routers publikují LeaseSet přes odchozí client tunnel pomocí `DatabaseStoreMessage` s Reply Token (odpovědní token), který je nenulový. Zpráva je end-to-end garlic encrypted pomocí Session Key Manager (správce klíčů relace) Destination (identifikátor cíle v I2P), takže ji nevidí výstupní endpoint odchozího tunnel. Floodfill odpoví `DeliveryStatusMessage`, která se vrací přes příchozí tunnel.

### 8.6 Proces zaplavování

Floodfill uzly (uzly udržující netdb) ověřují RouterInfo (metadata o routeru)/LeaseSet (informace pro směrování k destinaci) před lokálním uložením pomocí adaptivních kritérií závislých na zátěži, velikosti netdb (síťová databáze I2P) a dalších faktorech.

Po obdržení platnějších novějších dat je floodfill routery „floodují“ tak, že vyhledají 3 nejbližší floodfill routery ke směrovacímu klíči. Přímá spojení posílají I2NP `DatabaseStoreMessage` s nulovým Reply Token (odpovědním tokenem). Ostatní routery neodpovídají ani znovu „floodují“.

**Důležitá omezení:** - Floodfills nesmí šířit přes tunnels; pouze přímá spojení - Floodfills nikdy nešíří expirovaný LeaseSet ani RouterInfo zveřejněné před více než hodinou

### 8.7 Vyhledávání RouterInfo (informace o routeru) a LeaseSet

I2NP `DatabaseLookupMessage` požaduje záznamy z netdb (síťová databáze I2P) od floodfill routers (speciální routery replikující netdb). Vyhledávání se odesílají přes odchozí průzkumný tunnel; odpovědi uvádějí návratovou cestu přes příchozí průzkumný tunnel.

Vyhledávací dotazy se obvykle posílají dvěma „dobrým“ floodfill routerům, které jsou nejblíže požadovanému klíči, paralelně.

- **Lokální shoda**: obdrží odpověď I2NP `DatabaseStoreMessage`
- **Žádná lokální shoda**: obdrží I2NP `DatabaseSearchReplyMessage` s odkazy na jiné floodfill routery blízké hledanému klíči

Vyhledávání LeaseSet používají end-to-end garlic encryption (od verze 0.9.5). Vyhledávání RouterInfo nejsou šifrovaná kvůli výpočetní náročnosti ElGamal, což je činí zranitelnými vůči odposlechu na odchozím koncovém bodu.

Od verze 0.9.7 odpovědi na vyhledávací dotazy obsahují klíč relace a značku (tag), čímž je skrývají před vstupní bránou.

### 8.8 Iterativní vyhledávání

Před verzí 0.8.9: Dvě paralelní redundantní vyhledávání bez rekurzivního ani iterativního směrování.

Od verze 0.8.9: **Iterativní vyhledávání** je implementováno bez redundance—efektivnější, spolehlivější a vhodné pro neúplnou znalost floodfill. Jak sítě rostou a routers znají méně floodfill, vyhledávání se blíží složitosti O(log n).

Iterativní vyhledávání pokračuje i bez odkazů na bližší uzly, čímž se zabrání škodlivému black-holingu (záměrnému pohlcování provozu bez odezvy). Platí aktuální maximální počet dotazů i časový limit.

### 8.9 Ověření

**Ověřování RouterInfo (informace o routeru)**: Od verze 0.9.7.1 je deaktivováno, aby se zabránilo útokům popsaným ve studii "Practical Attacks Against the I2P Network".

**Ověření LeaseSet**: Routery čekají ~10 sekund, poté provedou vyhledání u jiného floodfill přes odchozí klientský tunnel. End-to-end garlic encryption to skrývá před odchozím koncovým bodem. Odpovědi se vracejí přes příchozí tunnels.

Od verze 0.9.7 se odpovědi šifrují pomocí session key/tag hiding (skrývání klíče/značky relace), takže jsou skryté před vstupní bránou.

### 8.10 Průzkum

**Průzkum** zahrnuje vyhledávání v netdb s náhodnými klíči pro nalezení nových routerů. Uzly floodfill odpovídají zprávou `DatabaseSearchReplyMessage`, která obsahuje hashe routerů, jež nejsou floodfill, blízké požadovanému klíči. Průzkumné dotazy nastavují speciální příznak v `DatabaseLookupMessage`.

---

## 9. MultiHoming (připojení k více sítím)

Destinations (cílový identifikátor v I2P) používající stejné soukromé/veřejné klíče (tradiční `eepPriv.dat`) lze provozovat na více routerech současně. Každá instance periodicky publikuje podepsané LeaseSets; nejnovější zveřejněný LeaseSet se vrací žadatelům o vyhledání. Při maximální době platnosti 10 minut pro LeaseSet trvají výpadky nanejvýš ~10 minut.

Od verze 0.9.38 **Meta LeaseSets** podporují rozsáhlé multihomed služby (služby s vícenásobným připojením k síti) využívající samostatné Destinace poskytující společné služby. Záznamy Meta LeaseSet jsou Destinace nebo jiné Meta LeaseSets s platností až 18,2 hodiny, což umožňuje, aby společné služby hostovaly stovky až tisíce Destinací.

---

## 10. Analýza hrozeb

Přibližně 1700 floodfill routerů je v současnosti v provozu. Růst sítě ztěžuje většinu útoků nebo snižuje jejich dopad.

### 10.1 Obecná zmírňující opatření

- **Růst**: Více floodfills ztěžuje útoky nebo snižuje jejich dopad
- **Redundance**: Všechny záznamy v netdb se ukládají prostřednictvím flooding (zaplavování) na 3 floodfill routers nejblíže ke klíči
- **Podpisy**: Všechny záznamy jsou podepsány tvůrcem; falšování je nemožné

### 10.2 Pomalé nebo nereagující Routers

Routers udržují rozšířené statistiky profilů uzlů pro floodfills:
- Průměrná doba odezvy
- Procento zodpovězených dotazů
- Procento úspěšnosti ověření uložení
- Poslední úspěšné uložení
- Poslední úspěšné vyhledání
- Poslední odpověď

Routers používají tyto metriky při určování "vhodnosti" pro výběr nejbližší floodfill. Zcela nereagující routers jsou rychle identifikovány a je jim vyhýbáno; částečně zlovolné routers představují větší výzvu.

### 10.3 Sybil útok (celý klíčový prostor)

Útočníci mohou za účelem účinného DOS útoku vytvořit početné routery typu floodfill rozmístěné napříč prostorem klíčů.

Pokud se chování nejeví natolik závadné, aby si zasloužilo označení "bad", možné reakce zahrnují: - Sestavování seznamů "bad" hashů/IP adres routerů a jejich oznamování prostřednictvím novinek v konzoli, webu a fóra - Celosíťové povolení floodfill ("bojovat proti Sybil (útok Sybil) ještě více Sybil") - Nové verze softwaru s natvrdo zakódovanými seznamy "bad" - Vylepšené metriky profilů peerů a prahové hodnoty pro automatickou identifikaci - Kvalifikace IP bloků vylučující více floodfillů v jediném IP bloku - Automatický blacklist založený na odběru (podobně jako konsenzus Toru)

Větší sítě to ztěžují.

### 10.4 Sybil útok (částečný klíčový prostor)

Útočníci mohou vytvořit 8–15 floodfill routers těsně seskupených v klíčovém prostoru. Všechny operace vyhledávání/ukládání pro tento klíčový prostor jsou směrovány na routery útočníka, což umožňuje útok DoS na konkrétní I2P stránky.

Jelikož klíčový prostor indexuje kryptografické hashe SHA256, útočníci musí použít hrubou sílu k vytvoření routerů s dostatečnou blízkostí.

**Obrana**: Algoritmus blízkosti Kademlia se v čase mění pomocí `SHA256(key + YYYYMMDD)`, každý den o půlnoci UTC. Tato **keyspace rotation** (rotace prostoru klíčů) vynucuje denní obnovu útoku.

> **Poznámka**: Nedávný výzkum ukazuje, že rotace prostoru klíčů není obzvlášť účinná—útočníci mohou předpočítat hashe routerů, takže k zastínění částí prostoru klíčů jim stačí jen několik routerů během půl hodiny po rotaci.

Důsledek denní rotace: distribuovaná netdb se po rotaci na několik minut stává nespolehlivou—dotazy selhávají, než nový nejbližší router obdrží stores (zprávy pro uložení).

### 10.5 Útoky při bootstrapu (počáteční inicializaci)

Útočníci by mohli převzít kontrolu nad reseed webovými stránkami (weby/servery poskytujícími bootstrap novým routerům) nebo přimět vývojáře k přidání nepřátelských reseed webových stránek, čímž by uváděli nové routery do izolovaných/většinově kontrolovaných sítí.

**Implementovaná obranná opatření:** - Načítat podmnožiny RouterInfo (informace o routeru) z více reseed sites (bootstrap serverů), nikoli z jediného serveru - Mimo-síťové monitorování reseed, které periodicky dotazuje servery - Od verze 0.9.14 jsou balíčky reseed dat poskytovány jako podepsané soubory ZIP s ověřením staženého podpisu (viz [specifikace su3](/docs/specs/updates))

### 10.6 Zachycení dotazů

Floodfill routery mohou "nasměrovat" protějšky na routery kontrolované útočníkem prostřednictvím vrácených referencí.

Nepravděpodobné prostřednictvím průzkumu kvůli nízké frekvenci; reference na peery se získávají hlavně běžným vytvářením tunnel.

Od verze 0.8.9 jsou implementována iterativní vyhledávání. Reference floodfill uvedené v `DatabaseSearchReplyMessage` se následují, pokud jsou blíže vyhledávacímu klíči. Požadující router nedůvěřuje blízkosti referencí. Vyhledávání pokračuje i když nejsou k dispozici bližší klíče, a to až do vypršení časového limitu/maximálního počtu dotazů, což brání škodlivému black-holingu (pohlcování provozu).

### 10.7 Úniky informací

Únik informací v DHT (distribuovaná hašovací tabulka) v I2P vyžaduje další prošetření. Floodfill routers pozorují dotazy a shromažďují informace. Při podílu škodlivých uzlů 20 % se dříve popsané hrozby Sybil (útok založený na mnohonásobné identitě) stávají problematickými z více důvodů.

---

## 11. Budoucí práce

- End-to-end šifrování (šifrování mezi koncovými body) dalších dotazů do netDb a jejich odpovědí
- Lepší metody sledování odpovědí na dotazy
- Metody zmírnění problémů se spolehlivostí při rotaci klíčového prostoru

---

## 12. Reference

- [Specifikace obecných struktur](/docs/specs/common-structures/) – struktury RouterInfo a LeaseSet
- [Specifikace I2NP](/docs/specs/i2np/) – typy databázových zpráv
- [Návrh 123: Nové záznamy v netDb](/proposals/123-new-netdb-entries) – specifikace LeaseSet2
- [Historická diskuse o netDb](/docs/netdb/) – historie vývoje a archivované diskuse
