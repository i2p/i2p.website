---
title: "SAM V3"
description: "Jednoduchý protokol pro anonymní zasílání zpráv pro aplikace I2P nevyužívající Javu"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM je jednoduchý klientský protokol pro komunikaci s I2P. SAM je doporučeným protokolem pro ne-Java aplikace, které se připojují k síti I2P, a je podporován více implementacemi routerů. Java aplikace by měly používat streamovací rozhraní nebo I2CP API přímo.

SAM verze 3 byla představena v I2P verzi 0.7.3 (květen 2009) a je to stabilní a podporované rozhraní. Verze 3.1 je také stabilní a podporuje volbu typu podpisu, což je důrazně doporučeno. Novější verze 3.x podporují pokročilé funkce. Poznámka: i2pd aktuálně nepodporuje většinu funkcí verzí 3.2 a 3.3.

Alternativy: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (zastaralé)](/docs/api/bob). Zastaralé verze: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Známé knihovny SAM

Upozornění: Některé z nich mohou být velmi staré nebo nepodporované. Žádné nejsou testovány, recenzovány ani udržovány projektem I2P, pokud není uvedeno jinak níže. Proveďte si vlastní výzkum.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Rychlý start

Pro implementaci základní aplikace pouze s TCP a komunikací typu peer-to-peer musí klient podporovat následující příkazy:

- `HELLO VERSION MIN=3.1 MAX=3.1` – Vyžadováno pro všechny zbývající příkazy
- `DEST GENERATE SIGNATURE_TYPE=7` – Pro generování našeho privátního klíče a cíle (destination)
- `NAMING LOOKUP NAME=...` – Pro převod .i2p adres na cíle (destinations)
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` – Vyžadováno pro příkazy STREAM CONNECT a STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` – Pro vytváření odchozích spojení
- `STREAM ACCEPT ID=...` – Pro přijímání příchozích spojení

## Obecné pokyny pro vývojáře

### Návrh aplikace

SAM relace (nebo uvnitř I2P sdružení tunelů či sady tunelů) jsou navrženy tak, aby trvaly dlouhou dobu. Většina aplikací bude potřebovat pouze jednu relaci, která se vytvoří při spuštění a ukončí při vypnutí. I2P se liší od Toru, kde mohou být cesty rychle vytvářeny a zahazovány. Pečlivě promyslete a před navržením aplikace, která bude používat více než jednu nebo dvě souběžné relace, nebo bude relace rychle vytvářet a zahazovat, se poraďte s vývojáři I2P. U většiny modelů hrozeb nebude vyžadována jedinečná relace pro každé spojení.

Dále se ujistěte, že nastavení vaší aplikace (a pokyny pro uživatele týkající se nastavení směrovače, případně výchozí nastavení směrovače, pokud je součástí vaší aplikace) povedou k tomu, že vaši uživatelé budou do sítě přispívat více zdroji, než kolik jich spotřebovávají. I2P je síť typu peer-to-peer a nemůže přežít, pokud oblíbená aplikace způsobí trvalé přetížení sítě.

### Kompatibilita a testování

Implementace směrovače Java I2P a i2pd jsou nezávislé a mají drobné rozdíly v chování, podpoře funkcí a výchozích nastaveních. Otestujte prosím svou aplikaci s nejnovější verzí obou směrovačů.

i2pd SAM je ve výchozím nastavení povolen; SAM v Java I2P není. Poskytněte svým uživatelům pokyny, jak povolit SAM v Java I2P (přes /configclients v konzoli směrovače), a/nebo uveďte uživatelsky přívětivou chybovou zprávu v případě selhání počátečního připojení, např. „ujistěte se, že běží I2P a že je povolen rozhraní SAM“.

Směrovače Java I2P a i2pd mají různá výchozí nastavení počtu tunelů. Výchozí hodnota pro Java je 2 a pro i2pd je 5. Pro většinu případů s nízkým až středním využitím šířky pásma a nízkým až středním počtem spojení je dostačující hodnota 2 nebo 3. Pro dosažení konzistentního výkonu se směrovači Java I2P a i2pd prosím uveďte požadovaný počet tunelů ve zprávě SESSION CREATE. Viz níže.

Další pokyny pro vývojáře, jak zajistit, že vaše aplikace používá pouze prostředky, které potřebuje, naleznete v [našem průvodci zabudováním I2P do vaší aplikace](/docs/applications/embedding).

### Typy podpisu a šifrování

I2P podporuje více typů podpisů a šifrování. Z důvodu zpětné kompatibility SAM ve výchozím nastavení používá starší a neefektivní typy, proto by všichni klienti měli zadat novější typy.

Typ podpisu je určen v příkazech DEST GENERATE a SESSION CREATE (pro přechodné spojení). Všichni klienti by měli nastavit `SIGNATURE_TYPE=7` (Ed25519).

Typ šifrování je určen v příkazu SESSION CREATE. Je povoleno více typů šifrování. Klienti by měli nastavit buď `i2cp.leaseSetEncType=4` (pouze pro ECIES-X25519) nebo `i2cp.leaseSetEncType=6,4` (pro MLKEM-768 a ECIES-X25519, pro směrovače podporující API 0.9.67 nebo vyšší).

## Změny ve verzi 3

### Změny ve verzi 3.0

Verze 3.0 byla představena v I2P verzi 0.7.3. SAM v2 poskytoval způsob, jak spravovat několik soketů na stejné I2P destinaci *paralelně*, tedy klient nemusel čekat na úspěšné odeslání dat na jednom soketu, než začal odesílat data na jiném soketu. Všechna data však procházela stejným soketem mezi klientem a SAM, což bylo pro klienta poměrně složité na správu.

SAM v3 spravuje sokety odlišným způsobem: každý *I2P soket* odpovídá jedinečnému soketu klient–SAM, což je mnohem jednodušší na zpracování. Toto je podobné jako u [BOB](/docs/api/bob).

SAM v3 také nabízí UDP port pro odesílání datagramů přes I2P a může přeposílat zpět I2P datagramy na datagramový server klienta.

### Změny ve verzi 3.1

Verze 3.1 byla představena v Java I2P verzi 0.9.14 (červenec 2014). SAM 3.1 je doporučenou minimální implementací SAM kvůli podpoře lepších typů podpisů ve srovnání s SAM 3.0. i2pd také podporuje většinu funkcí 3.1.

- Příkazy DEST GENERATE a SESSION CREATE nyní podporují parametr SIGNATURE_TYPE.
- Parametry MIN a MAX v příkazu HELLO VERSION jsou nyní volitelné.
- Parametry MIN a MAX v příkazu HELLO VERSION nyní podporují jednoduché číslo verze, například "3".
- Na mostním soketu je nyní podporován příkaz RAW SEND.

### Změny ve verzi 3.2

Verze 3.2 byla představena v Java I2P verzi 0.9.24 (leden 2016). Poznámka: i2pd aktuálně nepodporuje většinu funkcí verze 3.2.

#### Podpora portů a protokolů I2CP

- Možnosti SESSION CREATE FROM_PORT a TO_PORT
- Možnost PROTOCOL ve STYLE=RAW příkazu SESSION CREATE
- Možnosti FROM_PORT a TO_PORT u příkazů STREAM CONNECT, DATAGRAM SEND a RAW SEND
- Možnost PROTOCOL u příkazu RAW SEND
- DATAGRAM RECEIVED, RAW RECEIVED a přeposílané nebo přijaté proudy a odpovědní datagramy, včetně FROM_PORT a TO_PORT
- Možnost RAW session HEADER=true způsobí, že přeposílané raw datagramy budou na začátku obsahovat řádek s PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- První řádek datagramů odesílaných přes port 7655 nyní může začínat jakoukoli verzí 3.x
- První řádek datagramů odesílaných přes port 7655 může obsahovat některou z možností FROM_PORT, TO_PORT, PROTOCOL
- RAW RECEIVED obsahuje PROTOCOL=nnn

#### SSL a ověřování

- UŽIVATEL/HESLO v parametrech HELLO pro autorizaci. Viz [níže](#authorization).
- Volitelná konfigurace autorizace pomocí příkazu AUTH. Viz [níže](#authorization-configuration-sam-32-or-higher-optional-feature).
- Volitelná podpora SSL/TLS na řídicím soketu. Viz [níže](#ssl).
- Možnost STREAM FORWARD SSL=true

#### Vícevláknovost

- Souběžné čekající požadavky STREAM ACCEPT jsou na stejné relační ID povoleny.

#### Zpracování příkazové řádky a udržování spojení (keepalive)

- Volitelné příkazy QUIT, STOP a EXIT pro ukončení relace a soketu. Viz [níže](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- Zpracování příkazů správně podporuje UTF-8.
- Zpracování příkazů spolehlivě zpracovává bílé znaky uvnitř uvozovek.
- Zpětné lomítko '\\' může uvozovky na příkazovém řádku odescapeovat.
- Doporučuje se, aby server mapoval příkazy na velká písmena, aby usnadnil testování přes telnet.
- Prázdné hodnoty volby jako PROTOCOL nebo PROTOCOL= mohou být povoleny, záleží na implementaci.
- PING/PONG pro udržení spojení. Viz níže.
- Servery mohou implementovat časová období pro příkazy HELLO nebo následné příkazy, záleží na implementaci.

### Změny ve verzi 3.3

Verze 3.3 byla představena v Java I2P verzi 0.9.25 (březen 2016). Vezměte na vědomí, že i2pd aktuálně nepodporuje většinu funkcí verze 3.3.

- Stejné sezení může být použito současně pro proudy, datagramy a raw režim. Příchozí pakety a proudy budou směrovány na základě I2P protokolu a cílového portu. Viz [sekce PRIMARY níže](#sam-primary-sessions-v33-and-higher).
- Příkazy DATAGRAM SEND a RAW SEND nyní podporují možnosti SEND_TAGS, TAG_THRESHOLD, EXPIRES a SEND_LEASESET. Viz [sekce odesílání datagramů níže](#sending-repliable-or-raw-datagrams).

### Změny v roce 2025-04

Dva návrhy byly schváleny a začleněny do specifikace v dubnu 2025. Verze se nemění, aby byla naznačena podpora. Některé implementace ji ještě nepodporují a u jiných je podpora zatím předběžná.

- Podpora datagramu 2/3 (návrh 163). Určeno v SESSION CREATE a SESSION ADD (podrelace). Viz níže.
- Načítání možností leasesetu (návrh 167). Určeno pomocí NAMING LOOKUP OPTIONS=true. Viz níže.

## Protokol verze 3

### Specifikace rozhraní Jednoduché anonymní zprávy (SAM) verze 3.3 – přehled

Klientská aplikace komunikuje s mostem SAM, který zpracovává veškerou funkcionalitu I2P (s využitím [knihovny pro streamování](/docs/api/streaming) pro virtuální proudy nebo přímo [I2CP](/docs/protocol/i2cp) pro datagramy).

Ve výchozím nastavení je komunikace mezi klientem a SAM mostem nešifrovaná a bez ověření totožnosti. SAM most může podporovat SSL/TLS připojení; konfigurace a implementační detaily jsou mimo rozsah této specifikace. Od verze SAM 3.2 jsou ve výchozím handshake podporovány volitelné parametry pro ověření (uživatelské jméno/heslo), které mohou být mostem vyžadovány.

Komunikace v rámci I2P může probíhat několika odlišnými způsoby:

- [Virtuální proudy](/docs/api/streaming)
- [Odpovědné a ověřené datagramy](/docs/specs/datagrams#repliable) (zprávy s polem FROM)
- [Anonymní datagramy](/docs/specs/datagrams#raw) (surové anonymní zprávy)
- [Datagram2](/docs/specs/datagrams#datagram2) (nový formát odpovědných a ověřených zpráv)
- [Datagram3](/docs/specs/datagrams#datagram3) (nový formát odpovědných, ale neověřených zpráv)

Komunikace v rámci I2P je podporována I2P relacemi a každá I2P relace je vázána na adresu (označovanou jako cíl). Každá I2P relace je spojena s jedním ze tří výše uvedených typů a nemůže přenášet komunikaci jiného typu, pokud nepoužívá [hlavní relace](#sam-primary-sessions-v33-and-higher).

### Kódování a řídicí znaky

Všechny tyto zprávy SAM jsou odesílány na jednom řádku a končí znakem nového řádku (\\n). Před verzí SAM 3.2 byl podporován pouze 7bitový ASCII. Od verze SAM 3.2 musí být kódování UTF-8. Měly by fungovat všechny klíče a hodnoty kódované v UTF-8.

Formátování uvedené v této specifikaci níže je určeno pouze pro čitelnost. Zatímco první dvě slova každé zprávy musí zůstat ve stanoveném pořadí, pořadí dvojic klíč=hodnota může být změněno (např. „ONE TWO A=B C=D“ nebo „ONE TWO C=D A=B“ jsou obě platné konstrukce). Kromě toho je protokol citlivý na velikost písmen. Následující příklady zpráv jsou označeny šipkou „->“ pro zprávy odesílané klientem do SAM mostu a šipkou „<-“ pro zprávy odesílané SAM mostem ke klientovi.

Základní příkaz nebo odpověď má jednu z následujících podob:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
PŘÍKAZ bez PODPŘÍKAZU je podporován pouze pro některé nové příkazy v SAM 3.2.

Páry klíč=hodnota musí být odděleny jednou mezerou. (Od SAM 3.2 jsou povoleny i více mezer.) Pokud hodnoty obsahují mezery, musí být uzavřeny do dvojitých uvozovek, např. klíč="dlouhý text hodnoty". (Před verzí SAM 3.2 to v některých implementacích nefungovalo spolehlivě)

Před verzí SAM 3.2 neexistoval žádný mechanismus pro escapování. Od verze SAM 3.2 mohou být uvozovky escapovány zpětným lomítkem '\\' a samotné zpětné lomítko může být reprezentováno jako dvojice zpětných lomítek '\\\\'.

### Prázdné hodnoty

Počínaje SAM 3.2 jsou prázdné hodnoty volby, jako KEY, KEY= nebo KEY="", povoleny v závislosti na implementaci.

### Citlivost na velikost písmen

Protokol, jak je specifikován, rozlišuje velikost písmen. Doporučuje se (nikoli vyžaduje), aby server mapoval příkazy na velká písmena, aby bylo snazší testování pomocí telnetu. To by například umožnilo použití příkazu "hello version". Toto chování závisí na implementaci. Klíče ani hodnoty nesmí být mapovány na velká písmena, protože by to poškodilo možnosti [I2CP](/docs/protocol/i2cp).

### Připojovací handshake SAM

Žádná SAM komunikace nemůže proběhnout dříve, než se klient a most dohodnou na verzi protokolu, což je provedeno tak, že klient pošle HELLO a most pošle HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
a

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
Od verze 3.1 (I2P 0.9.14) jsou parametry MIN a MAX volitelné. SAM vždy vrátí nejvyšší možnou verzi v rámci omezení MIN a MAX, případně aktuální verzi serveru, pokud nejsou zadána žádná omezení.

Pokud most SAM nedokáže najít vhodnou verzi, odpoví:

```
<- HELLO REPLY RESULT=NOVERSION
```
Pokud dojde k nějaké chybě, například kvůli špatnému formátu požadavku, odpoví následovně:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

Řídicí socket serveru může volitelně nabízet podporu SSL/TLS, jak je nakonfigurováno na serveru a klientovi. Implementace mohou nabízet i další transportní vrstvy; toto je mimo rámec definice protokolu.

#### Autorizace

Pro autorizaci klient přidá do parametrů příkazu HELLO položky USER="xxx" PASSWORD="yyy". U uživatele a hesla se doporučuje (ale není vyžadováno) použít uvozovky. Uvozovka uvnitř uživatelského jména nebo hesla musí být ohraničena zpětným lomítkem. V případě chyby server odpoví zprávou I2P_ERROR a popisem chyby. Doporučuje se povolit SSL na všech SAM serverech, kde je vyžadována autorizace.

#### Časové limity

Servery mohou implementovat časová omezení pro příkaz HELLO nebo následné příkazy, v závislosti na implementaci. Klienti by měli po připojení rychle odeslat příkaz HELLO a následující příkaz.

Pokud dojde k vypršení časového limitu před přijetím zprávy HELLO, most odpoví:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
a poté se odpojí.

Pokud dojde k časovému limitu po přijetí zprávy HELLO, ale před příkazem následujícím po ní, odpoví most následujícím způsobem:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
a poté se odpojí.

### I2CP porty a protokol

Od verze SAM 3.2 může klient SAM zadat [I2CP](/docs/protocol/i2cp) porty a protokol, které mají být předány do [I2CP](/docs/protocol/i2cp), a most SAM předá přijaté informace o portu a protokolu [I2CP](/docs/protocol/i2cp) zpět klientovi SAM.

Pro FROM_PORT a TO_PORT je platný rozsah 0–65535, výchozí hodnota je 0.

Pro PROTOCOL, který lze zadat pouze pro RAW, je platný rozsah 0–255 a výchozí hodnota je 18.

U příkazů SESSION jsou zadané porty a protokol výchozími hodnotami pro danou relaci. U jednotlivých proudů nebo datagramů mají zadané porty a protokol přednost před výchozími hodnotami relace. U přijatých proudů nebo datagramů jsou uvedené porty a protokol takové, jak byly přijaty přes [I2CP](/docs/protocol/i2cp).

#### Důležité rozdíly od standardního IP

I2CP porty jsou určeny pro I2P sokety a datagramy. Nemají žádný vztah k místním soketům připojujícím se k SAM.

- Port 0 je platný a má speciální význam.
- Porty 1–1023 nejsou speciální ani privilegované.
- Servery naslouchají na portu 0 ve výchozím nastavení, což znamená „všechny porty“.
- Klienti odesílají na port 0 ve výchozím nastavení, což znamená „libovolný port“.
- Klienti odesílají z portu 0 ve výchozím nastavení, což znamená „nespecifikováno“.
- Servery mohou mít službu naslouchající na portu 0 a zároveň další služby naslouchající na vyšších portech. V takovém případě je služba na portu 0 výchozí a bude použita, pokud port příchozího socketu nebo datagramu neodpovídá žádné jiné službě.
- Většina cílů I2P má spuštěnou pouze jednu službu, takže můžete používat výchozí hodnoty a konfiguraci I2CP portů ignorovat.
- Pro zadání I2CP portů je vyžadován SAM 3.2 nebo 3.3.
- Pokud nepotřebujete I2CP porty, nepotřebujete SAM 3.2 ani 3.3; 3.1 je dostačující.
- Protokol 0 je platný a znamená „libovolný protokol“. Toto se nedoporučuje a pravděpodobně nebude fungovat.
- I2P sokety jsou sledovány pomocí interního identifikátoru spojení. Proto není vyžadováno, aby byla 5-tice dest:port:dest:port:protokol unikátní. Například může existovat více soketů se stejnými porty mezi dvěma cíli. Klienti nemusí vybírat „volný port“ pro odchozí spojení.

Pokud navrhujete aplikaci pro SAM 3.3 s více pods relacemi, důkladně zvažte, jak efektivně využívat porty a protokoly. Další informace naleznete ve specifikaci [I2CP](/docs/protocol/i2cp).

### SAM Relace

Relace SAM je vytvořena tak, že klient otevře socket k SAM mostu, provede handshake a pošle zprávu SESSION CREATE. Relace je ukončena po odpojení socketu.

Každá registrovaná I2P destinace je jedinečně spojena se session ID (nebo přezdívkou). Session ID, včetně subsession ID pro PRIMARY session, musí být globálně jedinečná na SAM serveru. Aby se předešlo možným kolizím ID s jinými klienty, je osvědčenou praxí, že klient generuje ID náhodně.

Každé sezení je jednoznačně spojeno s:

- socket, ze kterého klient vytváří relaci
- jeho ID (nebo přezdívka)

#### Žádost o vytvoření relace

Zpráva pro vytvoření relace může použít pouze jeden z těchto tvarů (zprávy přijaté v jiných tvarech jsou odpovězeny chybovou zprávou):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION určuje, který cíl má být použit pro odesílání a příjem zpráv/proudů. Hodnota $privkey je base64 řetězec vzniklý zřetězením [Destination](/docs/specs/common-structures#type_Destination), následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey) a [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), volitelně následovaného [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), což je 663 nebo více bajtů v binární podobě a 884 nebo více bajtů v base64, v závislosti na typu podpisu. Binární formát je specifikován v Private Key File. Další poznámky k [Private Key](/docs/specs/common-structures#type_PrivateKey) naleznete v sekci Generování klíčů cíle níže.

Pokud je privátní klíč pro podepisování tvořen samými nulami, následuje část [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature). Offline podpisy jsou podporovány pouze pro STREAM a RAW relace. Offline podpisy nelze vytvářet s nastavením DESTINATION=TRANSIENT. Formát části s offline podpisem je následující:

1. Časové razítko vypršení (4 bajty, big endian, sekundy od epochy, přeteče v roce 2106)  
2. Typ podpisu dočasného veřejného klíče pro podepisování (2 bajty, big endian)  
3. Dočasný veřejný klíč pro podepisování (délka dle specifikace typu dočasného podpisu)  
4. Podpis výše uvedených tří polí offline klíčem (délka dle specifikace typu podpisu cíle)  
5. Dočasný soukromý klíč pro podepisování (délka dle specifikace typu dočasného podpisu)

Pokud je cíl určen jako TRANSIENT, vytvoří SAM most nový cíl. Počínaje verzí 3.1 (I2P 0.9.14) je při použití přechodného cíle podporován volitelný parametr SIGNATURE_TYPE. Hodnota SIGNATURE_TYPE může být libovolný název (např. ECDSA_SHA256_P256, velikost písmen se nerozlišuje) nebo číslo (např. 1), které je podporováno [Key Certificates](/docs/specs/common-structures#type_Certificate). Výchozí hodnotou je DSA_SHA1, což obvykle nechcete. Pro většinu aplikací doporučujeme uvést SIGNATURE_TYPE=7.

$nickname je volba klienta. Mezery nejsou povoleny.

Další zadané možnosti jsou předány konfiguraci I2P relace, pokud nejsou interpretovány SAM mostem (např. outbound.length=0).

Směrovače Java I2P a i2pd mají různá výchozí nastavení počtu tunelů. Výchozí hodnota pro Java je 2 a pro i2pd je 5. Pro většinu případů s nízkým až středním využitím šířky pásma a nízkým až středním počtem spojení je dostačující hodnota 2 nebo 3. Pro dosažení konzistentního výkonu se směrovači Java I2P a i2pd prosím uveďte počty tunelů ve zprávě SESSION CREATE, například pomocí možností inbound.quantity=3 outbound.quantity=3. Tyto a další možnosti [jsou popsány v níže uvedených odkazech](#tunnel-i2cp-and-streaming-options).

SAM most by již měl být nakonfigurován s tím, se kterým routerem se má přes I2P komunikovat (i když v případě potřeby může existovat způsob, jak to přepsat, např. i2cp.tcp.host=localhost a i2cp.tcp.port=7654).

#### Odpověď na vytvoření relace

Po obdržení zprávy o vytvoření relace SAM most odpoví zprávou o stavu relace následujícím způsobem:

Pokud bylo vytvoření úspěšné:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
Hodnota $privkey je base 64 řetězec vzniklý zřetězením [Destination](/docs/specs/common-structures#type_Destination), následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey) a [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), volitelně následovaného [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), což je binárně 663 nebo více bajtů a v base 64 884 nebo více bajtů, v závislosti na typu podpisu. Binární formát je specifikován v Private Key File.

Pokud obsahovala zpráva SESSION CREATE podepisovací soukromý klíč tvořený samými nulami a sekci [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), odpověď SESSION STATUS bude obsahovat stejná data ve stejném formátu. Podrobnosti viz výše uvedená sekce SESSION CREATE.

Pokud je přezdívka již přidružena k relaci:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Pokud je cíl již používán:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Pokud cíl není platným privátním klíčem cíle:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Pokud došlo k jiné chybě:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Pokud to není v pořádku, mělo by pole MESSAGE obsahovat čitelné informace o tom, proč nelze relaci vytvořit.

Vezměte na vědomí, že směrovač vytváří tunely před tím, než odpoví zprávou SESSION STATUS. To může trvat několik sekund, nebo v případě spuštění směrovače či vážného přetížení sítě i minutu či déle. Pokud se operace nezdaří, směrovač neodpoví chybovou zprávou několik minut. Nenastavujte krátkou časovou prodlevu při čekání na odpověď. Nepřerušujte relaci během vytváření tunelů a nepokoušejte se o opakované připojení.

SAM relace žijí a zanikají spolu se spojením, ke kterému jsou přidruženy. Když je spojení uzavřeno, relace zaniká a veškerá komunikace pomocí této relace je okamžitě ukončena. A stejně tak opačně – když relace z nějakého důvodu zanikne, SAM most uzavře spojení.

### Virtuální proudy SAM

Virtuální proudy jsou zaručeně odesílány spolehlivě a ve správném pořadí, s oznámením o úspěchu nebo selhání, jakmile je to možné.

Streamy jsou obousměrné komunikační sokety mezi dvěma I2P cíli, ale jejich otevření musí být vyžádáno jednou ze stran. Poté jsou příkazy CONNECT používány SAM klientem pro takovou žádost. Příkazy FORWARD / ACCEPT jsou používány SAM klientem, když chce naslouchat žádostem přicházejícím z jiných I2P cílů.

### Virtuální proudy SAM: CONNECT

Klient požaduje připojení tímto způsobem:

- otevření nového soketu přes SAM most
- předání stejného uvítacího handshake jako výše
- odeslání příkazu STREAM CONNECT

#### Žádost o připojení

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Tímto se vytvoří nové virtuální spojení z místní relace, jejíž ID je $nickname, ke zvolenému protějšku.

Cílem je $destination, což je base 64 [Destination](/docs/specs/common-structures#type_Destination), tedy 516 nebo více znaků v base 64 (387 nebo více bajtů v binárním formátu), v závislosti na typu podpisu.

**POZNÁMKA:** Od roku 2014 (SAM v3.1) podporuje Java I2P také doménová jména a b32 adresy pro $destination, avšak tato funkce nebyla dříve zdokumentována. Doménová jména a b32 adresy jsou nyní oficiálně podporovány v Java I2P od verze 0.9.48. Směrovač i2pd podporuje doménová jména a b32 adresy od verze 2.38.0 (0.9.50). U obou směrovačů zahrnuje podpora „b32“ také rozšířené „b33“ adresy pro skryté destinace.

#### Odpověď na připojení

Pokud je zadáno SILENT=true, SAM most neodesílá žádné další zprávy přes socket. Pokud se připojení nezdaří, socket bude uzavřen. Pokud připojení uspěje, všechna zbývající data procházející aktuálním socketem jsou přeposílána z a do připojeného I2P cílového protějšku.

Pokud je SILENT=false, což je výchozí hodnota, SAM most pošle poslední zprávu svému klientovi před předáním nebo vypnutím soketu:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Hodnota RESULT může být jednou z následujících:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Pokud je VÝSLEDEK OK, veškerá zbývající data procházející aktuálním socketem jsou přeposílána z a do připojeného I2P cílového protějšku. Pokud nebylo možné spojení navázat (vypršení časového limitu atd.), bude VÝSLEDEK obsahovat příslušnou chybovou hodnotu (doprovázenou volitelnou lidsky čitelnou ZPRÁVOU) a SAM most uzavře socket.

Časový limit pro interní připojení streamu směrovače je přibližně jedna minuta, v závislosti na implementaci. Nenastavujte kratší časový limit pro čekání na odpověď.

### SAM Virtuální proudy: PŘIJMOUT

Klient čeká na příchozí požadavek na připojení tím, že:

- otevření nového soketu přes SAM most
- předání stejného uvítacího handshake jako výše
- odeslání příkazu STREAM ACCEPT

#### Přijmout požadavek

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Toto způsobí, že relace ${nickname} bude naslouchat jedné příchozí žádosti o připojení ze sítě I2P. Příkaz ACCEPT není povolen, pokud je v relaci aktivní příkaz FORWARD.

Od verze SAM 3.2 je povoleno více souběžných čekajících příkazů STREAM ACCEPT se stejným ID relace (dokonce i se stejným portem). Před verzí 3.2 by souběžné akceptování selhalo s chybou ALREADY_ACCEPTING. Poznámka: Java I2P také podporuje souběžné ACCEPT od verze SAM 3.1, a to od vydání 0.9.24 (2016-01). i2pd také podporuje souběžné ACCEPT na SAM 3.1 od vydání 2.50.0 (2023-12).

#### Přijmout odpověď

Pokud je nastaveno SILENT=true, SAM most nebude na socketu odesílat žádné další zprávy. Pokud selže přijetí spojení, socket bude uzavřen. Pokud je spojení úspěšně přijato, veškerá zbývající data procházející aktuálním socketem jsou přeposílána z a do připojeného partnerského uzlu v síti I2P. Pro zajištění spolehlivosti a pro příjem cílové adresy příchozích spojení se doporučuje nastavit SILENT=false.

Pokud je SILENT=false, což je výchozí hodnota, SAM most odpoví:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Hodnota RESULT může být jednou z následujících:

```
OK
I2P_ERROR
INVALID_ID
```
Pokud je výsledek NENÍ V POŘÁDKU, soket je okamžitě uzavřen SAM mostem. Pokud je výsledek V POŘÁDKU, SAM most začne čekat na příchozí požadavek spojení od jiného I2P protějšku. Když požadavek dorazí, SAM most jej přijme a:

Pokud bylo předáno SILENT=true, most SAM nevydá žádnou další zprávu na klientském socketu. Veškerá zbývající data procházející aktuálním socketem jsou přeposílána mezi aktuálním socketem a připojeným I2P protějškem.

Pokud byla předána hodnota SILENT=false, což je výchozí hodnota, SAM most pošle klientovi ASCII řádek obsahující base64 veřejný klíč destinace požadujícího protějšku a další informace pouze pro SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Po této řádce ukončené znakem '\\n' je všechna zbývající data procházející aktuálním socketem přeposílána mezi připojeným I2P protějškem, dokud jeden z protějšků socket neuzavře.

#### Chyby po OK

V některých vzácných případech může SAM most narazit na chybu po odeslání RESULT=OK, ale předtím, než přijde připojení a most odešle klientovi řádek $destination. Mezi tyto chyby mohou patřit vypnutí směrovače, restart směrovače a ukončení relace. V těchto případech může SAM most (pokud je SILENT=false), ale nemusí (záleží na implementaci), odeslat řádek:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
před okamžitým uzavřením soketu. Tento řádek samozřejmě nelze dekódovat jako platnou Base 64 destinaci.

### Virtuální proudy SAM: PŘESMĚROVÁNÍ

Klient může použít běžný soketový server a čekat na požadavky na připojení přicházející z I2P. K tomu musí klient:

- otevřete nový socket pomocí SAM mostu
- předejte stejný úvodní handshake HELLO jako výše
- odešlete příkaz pro přeposílání

#### Předat požadavek

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Tímto se relace ${nickname} nastaví na naslouchání příchozích požadavků na připojení ze sítě I2P. FORWARD není povolen, pokud je v relaci čekající ACCEPT.

#### Přeposlat odpověď

SILENT je ve výchozím nastavení false. Bez ohledu na to, zda je SILENT true nebo false, most SAM vždy odpoví zprávou STREAM STATUS. Všimněte si, že toto je odlišné chování od STREAM ACCEPT a STREAM CONNECT, když SILENT=true. Zpráva STREAM STATUS je:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Hodnota RESULT může být jednou z následujících:

```
OK
I2P_ERROR
INVALID_ID
```
$host je název hostitele nebo IP adresa socketového serveru, na který bude SAM přeposílat požadavky na připojení. Pokud není zadáno, SAM použije IP adresu socketu, který vydal příkaz pro přeposílání.

$port je číslo portu soketového serveru, na který bude SAM přeposílat požadavky na připojení. Tento parametr je povinný.

Když dorazí požadavek na připojení z I2P, SAM most otevře soketové připojení k $host:$port. Pokud je přijato do 3 sekund, SAM přijme připojení z I2P a poté:

Pokud bylo předáno SILENT=true, veškerá data procházející aktuálním soketem jsou přeposílána z a do připojeného partnerského uzlu I2P.

Pokud byla předána hodnota SILENT=false, což je výchozí hodnota, SAM most po získaném soketu pošle ASCII řádek obsahující base64 veřejný klíč destinace požadujícího protějšku a další informace pouze pro SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Po této řádce ukončené znakem '\\n' je všechna zbývající data procházející přes socket přeposílána mezi připojeným partnerským uzlem I2P, dokud jedna ze stran socket neuzavře.

Od verze SAM 3.2, pokud je zadáno SSL=true, předávací socket běží přes SSL/TLS.

Směrovač I2P přestane naslouchat příchozím požadavkům na připojení, jakmile je uzavřen soket „forwarding“.

### SAM Datagramy

SAMv3 poskytuje mechanismy pro odesílání a příjem datagramů přes místní datagramové sokety. Některé implementace SAMv3 také podporují starší způsob odesílání/příjmu datagramů přes soket mostu SAM ve verzích v1/v2. Oba způsoby jsou popsány níže.

I2P podporuje čtyři typy datagramů:

- Datagramy, které lze odpovědět a které jsou ověřené, jsou předřazeny cílem odesílatele a obsahují podpis odesílatele, takže příjemce může ověřit, že cíl odesílatele nebyl falšován, a může na datagram reagovat. Nový formát Datagram2 je také odpovídací a ověřený.
- Nový formát Datagram3 je odpovídací, ale není ověřený. Informace o odesílateli nejsou ověřeny.
- Syrové datagramy neobsahují cíl odesílatele ani podpis.

Výchozí I2CP porty jsou definovány pro oba typy – odpovědi i raw datagramy. I2CP port může být změněn pro raw datagramy.

Běžným návrhem protokolu je odesílání odpovědích datagramů na servery, včetně nějakého identifikátoru, a následná odpověď serveru pomocí syrového datagramu, který tento identifikátor obsahuje, aby bylo možné odpověď spárovat s požadavkem. Tento návrh eliminuje významný režijní výdaj odpovídajících datagramů v odpovědích. Všechny volby protokolů a portů I2CP jsou specifické pro danou aplikaci, a proto by navrhovatelé měli tyto otázky zohlednit.

Viz také důležité poznámky k MTU datagramu v níže uvedené části.

#### Odesílání replikovatelných nebo surových datagramů

Ačkoli I2P ve své podstatě neobsahuje adresu ODESÍLATELE, pro usnadnění použití je k dispozici dodatečná vrstva ve formě odpovědných datagramů – neseřazených a nespolehlivých zpráv o velikosti až 31744 bajtů, které zahrnují adresu ODESÍLATELE (přičemž až 1 KB je vyhrazeno pro hlavičková data). Tato adresa odesílatele je interně ověřována prostřednictvím SAM (s využitím podepisovacího klíče cíle k ověření zdroje) a zahrnuje ochranu proti opakovanému přehrání (replay prevention).

Minimální velikost je 1. Pro nejlepší spolehlivost doručení se doporučuje maximální velikost přibližně 11 KB. Spolehlivost je nepřímo úměrná velikosti zprávy, možná dokonce exponenciálně.

Po navázání SAM relace se STYLE=DATAGRAM nebo STYLE=RAW může klient přes UDP port SAMu (standardně 7655) posílat replikovatelné nebo surové datagramy.

První řádek datagramu odeslaného tímto portem musí mít následující formát. Vše je na jednom řádku (odděleno mezerami), zobrazeno na více řádcích pro přehlednost:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 je verze SAM. Počínaje SAM 3.2 je povolena libovolná verze 3.x.
- $nickname je ID relace DATAGRAM, která bude použita
- Cílem je $destination, což je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více znaků v base 64 (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu. **Poznámka:** Od přibližně roku 2014 (SAM v3.1) podporuje Java I2P také doménová jména a b32 adresy pro $destination, ale to nebylo dříve zdokumentováno. Doménová jména a b32 adresy jsou nyní oficiálně podporovány Java I2P od verze 0.9.48. Směrovač i2pd aktuálně doménová jména a b32 adresy nepodporuje; podpora může být přidána v budoucí verzi.
- Všechny volby jsou nastavení na úrovni jednotlivých datagramů, která přepisují výchozí hodnoty zadané v SESSION CREATE.
- Volby verze 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES a SEND_LEASESET budou předány [I2CP](/docs/protocol/i2cp), pokud jsou podporovány. Podrobnosti viz [specifikace I2CP](/docs/protocol/i2cp#msg_SendMessageExpire). Podpora těchto možností SAM serverem je volitelná – pokud nejsou podporovány, server je bude ignorovat.
- tento řádek je ukončen znakem '\\n'.

První řádek bude SAMem zahoděn před odesláním zbývajících dat zprávy do zadaného cíle.

Alternativní metodu pro odesílání odpovědných a surových datagramů naleznete v části [DATAGRAM SEND a RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### SAM replikovatelné datagramy: Příjem datagramu

Přijaté datagramy jsou SAMem zapisovány na socket, ze kterého byla datagramová relace otevřena, pokud není v příkazu SESSION CREATE zadán předávací PORT. Toto je způsob příjmu datagramů kompatibilní s verzemi v1/v2.

Když dorazí datagram, most ho doručí klientovi prostřednictvím zprávy:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
Zdrojem je $destination, což je base 64 [Destination](/docs/specs/common-structures#type_Destination), tedy 516 nebo více znaků v base 64 (387 nebo více bajtů v binárním formátu), v závislosti na typu podpisu.

SAM most nikdy nezveřejňuje klientovi autentizační hlavičky ani jiná pole, pouze data, která odesílatel poskytl. Toto pokračuje až do ukončení relace (kdy klient ukončí spojení).

#### Přeposílání syrových nebo odpovědných datagramů

Při vytváření relace datagramu může klient požádat SAM o přeposílání příchozích zpráv na zadanou IP adresu a port. Udělá to tak, že odešle příkaz CREATE s možnostmi PORT a HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
Hodnota $privkey je base 64 řetězec vzniklý zřetězením [Destination](/docs/specs/common-structures#type_Destination), následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey), následovaného [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) a volitelně následovaného [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), což dává 884 nebo více znaků v base 64 (663 nebo více bajtů v binární podobě), v závislosti na typu podpisu. Binární formát je specifikován v Private Key File.

Offline podpisy jsou podporovány pro RAW, DATAGRAM2 a DATAGRAM3 datagramy, ale ne pro DATAGRAM. Podrobnosti viz sekce VYTVOŘENÍ RELACE výše a sekce DATAGRAM2/3 níže.

$host je název hostitele nebo IP adresa serveru datagramů, na který bude SAM přeposílat datagramy. Pokud není zadáno, SAM použije IP adresu soketu, který vydal příkaz pro přeposílání.

$port je číslo portu datagramového serveru, na který bude SAM přeposílat datagramy. Pokud $port není nastaveno, datagramy NEbudou přeposílány, ale budou přijímány na řídicím soketu způsobem kompatibilním s verzí v1/v2.

Další zadané možnosti jsou předány konfiguraci I2P relace, pokud nejsou interpretovány SAM mostem (např. outbound.length=0). Tyto možnosti [jsou zdokumentovány níže](#tunnel-i2cp-and-streaming-options).

Přeposílané datagramy s odpovědí jsou vždy předřazeny base64 cílem, s výjimkou Datagram3, viz níže. Když dorazí datagram s odpovědí, most pošle na zadaný hostitel:port UDP paket obsahující následující data:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Předávané nezpracované datagramy jsou předávány tak, jak jsou, na zadaný hostitele:port bez předpony. UDP paket obsahuje následující data:

```
$datagram_payload
```
Od verze SAM 3.2, pokud je v příkazu SESSION CREATE zadán parametr HEADER=true, bude na předávaný nezpracovaný datagram přidán hlavičkový řádek následujícího tvaru:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination je base 64 hodnota [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více znaků v base 64 (387 nebo více bajtů v binárním tvaru), v závislosti na typu podpisu.

#### SAM anonymní (surové) datagramy

SAM umožňuje klientům využít maximální šířku pásma I2P a posílat a přijímat anonymní datagramy, přičemž ověřování a informace pro odpověď zůstávají na straně klienta. Tyto datagramy jsou nespolehlivé a neuspořádané a mohou mít až 32768 bajtů.

Minimální velikost je 1. Pro nejlepší spolehlivost doručení se doporučuje maximální velikost přibližně 11 KB.

Po navázání SAM relace se STYLE=RAW může klient přes most SAM odesílat anonymní datagramy zcela stejným způsobem jako při [odesílání odpovědných nebo surových datagramů](#sending-repliable-or-raw-datagrams).

Obě metody příjmu datagramů jsou dostupné i pro anonymní datagramy.

Přijaté datagramy jsou SAMem zapisovány na socket, ze kterého byla datagramová relace otevřena, pokud není v příkazu SESSION CREATE zadán předávací PORT. Toto je způsob příjmu datagramů kompatibilní s verzemi v1/v2.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Když mají být anonymní datagramy předány nějakému hostiteli:portu, most pošle určenému hostiteli:portu zprávu obsahující následující data:

```
$datagram_payload
```
Od verze SAM 3.2, pokud je v příkazu SESSION CREATE zadán parametr HEADER=true, bude na předávaný nezpracovaný datagram přidán hlavičkový řádek následujícího tvaru:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Pro alternativní metodu odesílání anonymních datagramů viz [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagram 2/3

Datagram 2/3 jsou nové formáty specifikované na začátku roku 2025. V současné době nejsou známy žádné implementace. Pro aktuální stav si ověřte dokumentaci konkrétní implementace. Další informace naleznete v [specifikaci](/docs/specs/datagrams).

V současné době neexistují žádné plány na zvýšení verze SAM, aby byla indikována podpora Datagram 2/3. To může být problematické, protože implementace mohou chtít podporovat Datagram 2/3, ale ne funkce SAM v3.3. Jakékoli změny verze jsou dosud nevyřízeny (TBD).

Datagram2 i Datagram3 jsou odpovědné. Pouze Datagram2 je ověřen.

Datagram2 je z pohledu SAM identický s odpověďovými datagramy. Oba jsou ověřené. Liší se pouze formát I2CP a podpis, ale to není pro klienty SAM viditelné. Datagram2 také podporuje offline podpisy, takže může být použit u cílů s offline podpisy.

Cílem je, aby Datagram2 nahradil replikovatelné datagramy u nových aplikací, které nepotřebují zpětnou kompatibilitu. Datagram2 poskytuje ochranu proti opakovanému přehrání, která u replikovatelných datagramů není k dispozici. Pokud je vyžadována zpětná kompatibilita, může aplikace podporovat jak Datagram2, tak replikovatelné datagramy, a to ve stejné relaci s primárními relacemi SAM 3.3.

Datagram3 je odpovědný, ale neověřený. Pole 'from' ve formátu I2CP je hash, nikoli cíl. $destination odeslaný ze serveru SAM klientovi bude 44místný base64 hash. Pro převod na plný cíl pro odpověď jej dekódujte z base64 na 32 bajtů binárních dat, poté zakódujte do base32 na 52 znaků a přidejte příponu ".b32.i2p" pro NAMING LOOKUP. Jak je zvykem, měli by klienti vést vlastní mezipaměť, aby se předešlo opakovaným dotazům NAMING LOOKUP.

Vývojáři aplikací by měli postupovat s extrémní opatrností a zvážit bezpečnostní důsledky neověřených datagramů.

#### Úvahy o MTU datagramu V3

Datagramy I2P mohou být větší než typická internetová MTU o velikosti 1500 bajtů. Místně odesílané datagramy a přeposílané odpovědné datagramy, které mají předponu ve formě base64 zakódovaného cíle o délce 516 a více bajtů, pravděpodobně tuto MTU překročí. Místní MTU na systémech Linux jsou však typicky mnohem větší, například 65536. Velikost místní MTU se může lišit podle operačního systému. Datagramy I2P nikdy nepřesáhnou velikost 65536. Velikost datagramu závisí na aplikačním protokolu.

Pokud je SAM klient místní vzhledem k SAM serveru a systém podporuje větší MTU, datagramy nebudou místně fragmentovány. Pokud je však SAM klient vzdálený, IPv4 datagramy budou fragmentovány a IPv6 datagramy selžou (IPv6 nepodporuje fragmentaci UDP).

Vývojáři klientských knihoven a aplikací by měli být obeznámeni s těmito problémy a dokumentovat doporučení, jak předejít fragmentaci a ztrátě paketů, zejména u vzdálených SAM připojení mezi klientem a serverem.

#### Odeslání datagramu, odeslání RAW (zpracování datagramů kompatibilní s verzí 1/2)

V SAM V3 je preferovaným způsobem odesílání datagramů použití datagramového soketu na portu 7655, jak je popsáno výše. Replikovatelné datagramy však mohou být odeslány přímo přes soket SAM mostu pomocí příkazu DATAGRAM SEND, jak je dokumentováno v [SAM V1](/docs/api/sam) a [SAM V2](/docs/api/samv2).

Počínaje verzí 0.9.14 (verze 3.1) mohou být anonymní datagramy odesílány přímo přes soket SAM mostu pomocí příkazu RAW SEND, jak je dokumentováno v [SAM V1](/docs/api/sam) a [SAM V2](/docs/api/samv2).

Počínaje verzí 0.9.24 (verze 3.2) mohou příkazy DATAGRAM SEND a RAW SEND obsahovat parametry FROM_PORT=nnnn a/nebo TO_PORT=nnnn, které přepíší výchozí porty. Počínaje verzí 0.9.24 (verze 3.2) může příkaz RAW SEND obsahovat parametr PROTOCOL=nnn, který přepíše výchozí protokol.

Tyto příkazy *nepodporují* parametr ID. Datagramy jsou odesílány do naposledy vytvořené relace typu DATAGRAM nebo RAW, podle potřeby. Podpora parametru ID může být přidána v budoucí verzi.

Formáty DATAGRAM2 a DATAGRAM3 nejsou podporovány kompatibilním způsobem pro V1/V2.

### SAM Hlavní relace (V3.3 a vyšší)

*Verze 3.3 byla představena ve vydání I2P 0.9.25.*

*V dřívější verzi této specifikace byly PRIMÁRNÍ relace označovány jako HLAVNÍ (MASTER) relace. V obou projektech `i2pd` a `I2P+` jsou stále označovány výhradně jako HLAVNÍ (MASTER) relace.*

SAM v3.3 přidává podporu pro spouštění streamování, datagramů a raw subsession na stejné primární session, stejně jako pro spouštění více subsession stejného typu. Veškerý provoz subsession využívá jednu destinaci, nebo sadu tunelů. Směrování provozu přes I2P je založeno na nastavení portu a protokolu pro jednotlivé subsession.

Pro vytvoření multiplexovaných dílčích relací musíte vytvořit primární relaci a poté přidat dílčí relace do primární relace. Každá dílčí relace musí mít jedinečné ID a jedinečný protokol a port pro naslouchání. Dílčí relace mohou být také z primární relace odstraněny.

Pomocí hlavní relace a kombinace podrelací může klient SAM podporovat více aplikací nebo jednu pokročilou aplikaci využívající různé protokoly přes jedinou sadu tunelů. Například klient BitTorrent může nastavit streamovací podrelaci pro peer-to-peer připojení a zároveň datagramové a syrové podrelace pro komunikaci přes DHT.

#### Vytvoření hlavní relace

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM most odpoví úspěchem nebo selháním, jak je uvedeno v [odpovědi na standardní SESSION CREATE](#session-creation-response).

Nenastavujte možnosti PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL nebo HEADER u primární relace. Nemůžete odesílat žádná data pomocí ID primární relace ani přes řídicí socket. Všechny příkazy, jako STREAM CONNECT, DATAGRAM SEND atd., musí používat ID dílčí relace (subsession ID) na samostatném socketu.

HLAVNÍ relace se připojí k routeru a vytvoří tunely. Jakmile odpoví SAM most, jsou tunely vytvořeny a relace je připravena na přidání podrelací. Všechny možnosti [I2CP](/docs/protocol/i2cp) týkající se parametrů tunelů, jako je délka, množství a přezdívka, musí být uvedeny při vytváření hlavní relace (SESSION CREATE).

Všechny příkazy nástrojů jsou podporovány v primární relaci.

Když je uzavřena primární relace, jsou uzavřeny také všechny podrelace.

POZNÁMKA: Před vydáním 0.9.47 používejte STYLE=MASTER. STYLE=PRIMARY je podporován od verze 0.9.47. Pro zpětnou kompatibilitu je stále podporován MASTER.

#### Vytvoření podrelace

Použití stejného ovládacího soketu, na kterém byla vytvořena HLAVNÍ relace:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM most odpoví úspěchem nebo selháním, jak je uvedeno v [odpovědi na standardní SESSION CREATE](#session-creation-response). Jelikož byly tunely již vytvořeny během prvního SESSION CREATE, měl by SAM most odpovědět okamžitě.

Nenastavujte možnost DESTINATION u příkazu SESSION ADD. Dílčí relace použije cíl určený v hlavní relaci. Všechny dílčí relace musí být přidány na řídicí soket, tedy na stejné připojení, na kterém byla vytvořena hlavní relace.

Více subsession musí mít dostatečně jedinečné možnosti, aby bylo možné správně směrovat příchozí data. Zejména více session stejného typu musí mít odlišné možnosti LISTEN_PORT (a/nebo LISTEN_PROTOCOL, pouze pro RAW). Pokus o SESSION ADD se stejným portem naslouchání a protokolem, který duplikuje existující subsession, vyústí v chybu.

LISTEN_PORT je místní I2P port, tedy přijímací (TO) port pro příchozí data. Pokud není LISTEN_PORT zadán, bude použita hodnota FROM_PORT. Pokud nejsou zadány ani LISTEN_PORT ani FROM_PORT, bude směrování příchozího provozu založeno výhradně na STYLE a PROTOCOL. Pro LISTEN_PORT a LISTEN_PROTOCOL znamená hodnota 0 jakoukoli hodnotu, tedy zástupný symbol (wildcard). Pokud jsou LISTEN_PORT i LISTEN_PROTOCOL rovny 0, bude tato podseda výchozí pro příchozí provoz, který není směrován do jiné podsedy. Příchozí provoz typu streamování (protokol 6) nebude nikdy směrován do RAW podsedy, i když je její LISTEN_PROTOCOL nastaven na 0. RAW podseda nesmí mít nastaven LISTEN_PROTOCOL na 6. Pokud neexistuje výchozí podseda ani žádná odpovídající podseda pro protokol a port příchozího provozu, budou tato data zahozena.

Použijte ID subsesze, nikoli primární ID relace, pro odesílání a příjem dat. Všechny příkazy, jako jsou STREAM CONNECT, DATAGRAM SEND atd., musí používat ID subsesze.

Všechny pomocné příkazy jsou podporovány v hlavní relaci nebo podrelaci. Odesílání/příjem v1/v2 datagramů/surových dat není podporováno v hlavní relaci ani v podrelacích.

#### Zastavení subsystému

Použití stejného ovládacího soketu, na kterém byla vytvořena HLAVNÍ relace:

```
->  SESSION REMOVE
          ID=$nickname
```
Tímto se odstraní subsesze z hlavní relace. Nastavujte žádné další možnosti při SESSION REMOVE. Subsesze musí být odstraněny na řídicí soketu, tedy na stejném připojení, na kterém byla hlavní relace vytvořena. Po odstranění subsesze je uzavřena a nemůže být použita k odesílání nebo příjmu dat.

SAM most odpoví úspěchem nebo selháním, jak je uvedeno v [odpovědi na standardní SESSION CREATE](#session-creation-response).

### Příkazy nástroje SAM

Některé pomocné příkazy vyžadují existující relaci, jiné ne. Viz podrobnosti níže.

#### Vyhledání názvu hostitele

Následující zpráva může být klientem použita k dotazování SAM mostu na překlad názvu:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
na kterou odpovídá

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
Hodnota RESULT může být jednou z následujících:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Pokud je NAME=ME, odpověď bude obsahovat cíl používaný aktuální relací (užitečné, pokud používáte dočasný cíl). Pokud $result není OK, MESSAGE může obsahovat popisnou zprávu, například „špatný formát“ atd. INVALID_KEY znamená, že je něco špatně s $name ve žádosti, pravděpodobně neplatné znaky.

$destination je base 64 hodnota [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více znaků v base 64 (387 nebo více bajtů v binárním tvaru), v závislosti na typu podpisu.

VYHLEDÁVÁNÍ JMEN NEvyžaduje, aby byla nejprve vytvořena relace. V některých implementacích však může selhat vyhledání .b32.i2p, které není v mezipaměti a vyžaduje dotaz do sítě, protože nejsou k dispozici žádné klientovské tunely pro vyhledání.

#### Možnosti vyhledávání názvů

NAMING LOOKUP byl rozšířen od verze API směrovače 0.9.66 o podporu vyhledávání služeb. Podpora se může lišit podle implementace. Další informace naleznete v návrhu 167.

NAMING LOOKUP NAME=example.i2p OPTIONS=true vyžaduje mapování možností v odpovědi. NAME může být úplný base64 cíl, pokud OPTIONS=true.

Pokud bylo vyhledání cíle úspěšné a pokud byly v leasesetu k dispozici možnosti, budou v odpovědi po cíli následovat jedna nebo více možností ve formě OPTION:klíč=hodnota. Každá možnost bude mít samostatnou předponu OPTION:. Zahrnuty budou všechny možnosti z leasesetu, nikoli pouze možnosti záznamu služby. Například mohou být přítomny i možnosti pro parametry definované v budoucnosti. Příklad:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Klíče obsahující '=' a klíče nebo hodnoty obsahující znak nového řádku jsou považovány za neplatné a dvojice klíč-hodnota budou z odpovědi odstraněny. Pokud nejsou v leasesetu nalezeny žádné možnosti, nebo pokud byl leaseset verze 1, odpověď nebude obsahovat žádné možnosti. Pokud bylo v dotazu uvedeno OPTIONS=true a leaseset nebyl nalezen, bude vrácena nová hodnota výsledku LEASESET_NOT_FOUND.

#### Generování klíče cíle

Veřejné a soukromé klíče ve formátu base64 lze vygenerovat pomocí následující zprávy:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
na kterou odpovídá

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Od verze 3.1 (I2P 0.9.14) je podporován volitelný parametr SIGNATURE_TYPE. Hodnota SIGNATURE_TYPE může být libovolný název (např. ECDSA_SHA256_P256, bez rozlišení velkých a malých písmen) nebo číslo (např. 1), které je podporováno [Key Certificates](/docs/specs/common-structures#type_Certificate). Výchozí hodnotou je DSA_SHA1, což NENÍ to, co chcete. Pro většinu aplikací prosím nastavte SIGNATURE_TYPE=7.

$destination je base 64 hodnota [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více znaků v base 64 (387 nebo více bajtů v binárním tvaru), v závislosti na typu podpisu.

Hodnota $privkey je base 64 řetězec vzniklý zřetězením [Destination](/docs/specs/common-structures#type_Destination), následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey) a [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), což představuje 884 nebo více znaků v base 64 (663 nebo více bajtů v binární podobě), v závislosti na typu podpisu. Binární formát je specifikován v dokumentu Private Key File.

Poznámky k 256bitovému binárnímu [soukromému klíči](/docs/specs/common-structures#type_PrivateKey): Toto pole není používáno od verze 0.6 (2005). Implementace SAM mohou v tomto poli posílat náhodná data nebo samé nuly; nemějte obavy, pokud se v base64 objeví řetězec AAAA. Většina aplikací bude jednoduše ukládat řetězec v base64 a při požadavku SESSION CREATE jej vrátí beze změny, případně jej dekóduje do binární podoby pro uložení a znovu zakóduje pro SESSION CREATE. Aplikace však mohou také dekódovat base64, zpracovat binární data podle specifikace PrivateKeyFile, odstranit 256bitovou část soukromého klíče a při opětovném kódování pro SESSION CREATE ji nahradit 256 byty náhodných dat nebo samými nulami. VŠECHNY ostatní položky ve specifikaci PrivateKeyFile musí být zachovány. Tím by se ušetřilo 256 bajtů místa na souborovém systému, ale pro většinu aplikací to pravděpodobně není obtíž stojící za to. Další informace a kontext naleznete v návrhu 161.

DEST GENERATE nevyžaduje, aby byla nejprve vytvořena relace.

DEST GENERATE nelze použít k vytvoření destinace s offline podpisy.

#### PING/PONG (SAM 3.2 nebo vyšší)

Klient nebo server mohou odeslat:

```
PING[ arbitrary text]
```
na řídicím portu, s odpovědí:

```
PONG[ arbitrary text from the ping]
```
slouží k udržení kontrolního soketu aktivního. Jakákoli strana může relaci a soket uzavřít, pokud v rozumné době (závisí na implementaci) nedojde k odpovědi.

Pokud dojde k vypršení časového limitu při čekání na PONG od klienta, může most odeslat:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
a poté se odpojte.

Pokud dojde k vypršení časového limitu při čekání na PONG od mostu, klient se může jednoduše odpojit.

PING/PONG nevyžadují, aby byla nejprve vytvořena relace.

#### QUIT/STOP/EXIT (SAM 3.2 nebo vyšší, volitelné funkce)

Příkazy QUIT, STOP a EXIT ukončí relaci a soket. Implementace je volitelná, usnadňuje testování přes telnet. To, zda je odeslána nějaká odpověď před uzavřením soketu (například zpráva SESSION STATUS), závisí na konkrétní implementaci a není předmětem této specifikace.

Příkazy QUIT/STOP/EXIT nevyžadují, aby byla nejprve vytvořena relace.

#### NÁPOVĚDA (volitelná funkce)

Servery mohou implementovat příkaz HELP. Implementace je volitelná, usnadňuje testování přes telnet. Formát výstupu a detekce konce výstupu jsou specifické pro danou implementaci a nejsou součástí této specifikace.

HELP nevyžaduje, aby byla nejprve vytvořena relace.

#### Nastavení autorizace (SAM 3.2 nebo vyšší, volitelná funkce)

Konfigurace autorizace pomocí příkazu AUTH. SAM server může tyto příkazy implementovat za účelem trvalého ukládání přihlašovacích údajů. Konfigurace ověřování jiným způsobem než pomocí těchto příkazů je specifická pro danou implementaci a není předmětem této specifikace.

- AUTH ENABLE povolí autorizaci pro následné připojení
- AUTH DISABLE zakáže autorizaci pro následné připojení
- AUTH ADD USER="foo" PASSWORD="bar" přidá uživatele a heslo
- AUTH REMOVE USER="foo" odstraní tohoto uživatele

Dvojité uvozovky pro uživatele a heslo jsou doporučeny, ale nejsou vyžadovány. Dvojité uvozovky uvnitř uživatelského jména nebo hesla musí být ohraničeny zpětným lomítkem. V případě chyby server odpoví zprávou I2P_ERROR a zprávou.

AUTH nevyžaduje, aby byla nejprve vytvořena relace.

### Hodnoty RESULT

Toto jsou hodnoty, které může pole RESULT obsahovat, včetně jejich významu:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Různé implementace se mohou lišit v tom, který výsledek (RESULT) je vrácen v různých scénářích.

Většina odpovědí s výsledkem jiným než OK bude obsahovat také zprávu (MESSAGE) s dodatečnými informacemi. Tato zpráva bude obvykle užitečná při odstraňování problémů. Zprávy MESSAGE však závisí na konkrétní implementaci, mohou být přeloženy serverem SAM do aktuální lokalizace nebo nemusí, mohou obsahovat interní implementační informace jako výjimky a mohou být bez předchozího upozornění změněny. Klienti SAM mohou zprávy MESSAGE zobrazovat uživatelům, ale neměli by na jejich základě dělat programová rozhodnutí, protože by to bylo zranitelné.

### Nastavení tunelu, I2CP a streamování

Tyto možnosti mohou být předány jako páry název=hodnota v řádku SAM SESSION CREATE.

Všechny relace mohou obsahovat [možnosti I2CP, jako jsou délky a počty tunelů](/docs/protocol/i2cp#options). STREAM relace mohou obsahovat [možnosti streamovací knihovny](/docs/api/streaming#options).

Podívejte se na tyto reference ohledně názvů a výchozích hodnot možností. Odkazovaná dokumentace je určena pro implementaci Java routeru. Výchozí hodnoty se mohou změnit. Názvy a hodnoty možností rozlišují velká a malá písmena. Ostatní implementace routerů nemusí podporovat všechny možnosti a mohou mít odlišné výchozí hodnoty; podrobnosti naleznete v dokumentaci konkrétního routeru.

### Poznámky k BASE64

Kódování Base 64 musí používat I2P standardní abecedu Base 64 "A-Z, a-z, 0-9, -, ~".

### Výchozí nastavení SAM

Výchozí port SAM je 7656. SAM není ve výchozím nastavení ve směrovači Java I2P povolen; musí být spuštěn ručně, nebo nakonfigurován ke spuštění automaticky na stránce konfigurace klientů v konzoli směrovače, případně v souboru clients.config. Výchozí UDP port SAM je 7655, naslouchá na adrese 127.0.0.1. Tyto hodnoty lze ve směrovači Java změnit přidáním argumentů sam.udp.port=nnnnn a/nebo sam.udp.host=w.x.y.z do spouštěcího příkazu nebo na řádku SESSION.

Konfigurace v jiných routerech závisí na konkrétní implementaci. Viz [návod k nastavení i2pd zde](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
