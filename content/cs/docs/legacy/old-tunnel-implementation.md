---
title: "Implementace starého tunelu"
description: "Historická dokumentace původní implementace tunnelů I2P před verzí 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/cs/docs/historical/tunnel-alt"
  - "/cs/docs/historical/tunnel-alt/"
  - "/cs/tunnel"
  - "/cs/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Poznámka: Zastaralé - NEPOUŽÍVÁ SE! Nahrazeno ve verzi 0.6.1.10 - viz [současná implementace](/docs/specs/tunnel-implementation) pro aktivní specifikaci.**

## 1) Přehled tunnelů {#tunnel.overview}

V rámci I2P jsou zprávy předávány jedním směrem přes virtuální tunnel partnerů, pomocí jakýchkoli dostupných prostředků pro předání zprávy dalšímu uzlu. Zprávy přicházejí na bránu tunnelu, jsou zabaleny pro cestu a předány dalšímu uzlu v tunnelu, který zprávu zpracuje a ověří její platnost a pošle ji dalšímu uzlu, a tak dále, dokud nedosáhne koncového bodu tunnelu. Tento koncový bod vezme zprávy zabalené bránou a předá je podle instrukcí - buď jinému routeru, jinému tunnelu na jiném routeru, nebo lokálně.

Tunnely fungují všechny stejně, ale mohou být rozděleny do dvou různých skupin - příchozí tunnely a odchozí tunnely. Příchozí tunnely mají nedůvěryhodnou bránu, která předává zprávy směrem dolů k tvůrci tunnelu, který slouží jako koncový bod tunnelu. U odchozích tunnelů slouží tvůrce tunnelu jako brána, předávající zprávy ven ke vzdálenému koncovému bodu.

Tvůrce tunnel přesně vybírá, kteří peerové se budou podílet na tunnel, a poskytuje každému z nich potřebná konfigurační data. Mohou se lišit délkou od 0 hopů (kde gateway je zároveň koncovým bodem) až po 7 hopů (kde je 6 peerů za gateway a před koncovým bodem). Záměrem je ztížit jak účastníkům, tak třetím stranám určit délku tunnel, nebo dokonce spolupracujícím účastníkům určit, zda jsou vůbec součástí stejné tunnel (s výjimkou situace, kdy spolupracující peerové jsou v tunnel vedle sebe). Zprávy, které byly poškozeny, jsou také zahozeny co nejdříve, což snižuje zatížení sítě.

Kromě jejich délky existují další konfigurovatelné parametry pro každý tunnel, které lze použít, například omezení velikosti nebo frekvence doručovaných zpráv, jak má být použito vyplňování, jak dlouho má být tunnel v provozu, zda vkládat chaff zprávy, zda používat fragmentaci a jaké strategie dávkování mají být případně použity.

V praxi se pro různé účely používá série tunnel poolů - každá místní klientská destinace má svou vlastní sadu inbound tunnelů a outbound tunnelů, nakonfigurovanou tak, aby splňovala její potřeby anonymity a výkonu. Navíc router sám udržuje sérii poolů pro účast v network database a pro správu samotných tunnelů.

I2P je ze své podstaty paketově spínaná síť, i s těmito tunnely, což jí umožňuje využívat výhod více tunnelů běžících paralelně, zvyšuje odolnost a vyrovnává zátěž. Mimo základní vrstvu I2P je k dispozici volitelná end-to-end streaming knihovna pro klientské aplikace, která poskytuje TCP-podobný provoz, včetně přeuspořádávání zpráv, retransmise, řízení přetížení atd.

## 2) Provoz tunnel {#tunnel.operation}

Provoz tunnel má čtyři odlišné procesy, které provádějí různí peerové v tunnel. Nejprve tunnel gateway akumuluje určitý počet tunnel zpráv a předpracovává je na něco vhodného pro doručení tunnel. Dále tento gateway zašifruje tato předpracovaná data a poté je předá prvnímu uzlu. Tento peer a následující účastníci tunnel odbalí vrstvu šifrování, ověří integritu zprávy a poté ji předají dalšímu peerovi. Nakonec zpráva dorazí na koncový bod, kde jsou zprávy seskupené gateway znovu rozděleny a předány dál podle požadavku.

Tunnel ID jsou 4bajtová čísla používaná na každém uzlu - účastníci vědí, na které tunnel ID mají naslouchat zprávám a s jakým tunnel ID je mají předat na další uzel. Tunnely samotné jsou krátkodobé (v současnosti 10 minut), ale v závislosti na účelu tunnelu, a ačkoli následné tunnely mohou být vybudovány pomocí stejné sekvence uzlů, tunnel ID každého uzlu se změní.

### 2.1) Předzpracování zpráv {#tunnel.preprocessing}

Když chce gateway doručit data tunelem, nejprve shromáždí nulu nebo více I2NP zpráv (ne více než 32KB), vybere, kolik výplně bude použito, a rozhodne, jak by měla být každá I2NP zpráva zpracována koncovým bodem tunelu, přičemž tato data zakóduje do surové tunelové zátěže:

- 2 bajtové nepodepsané celé číslo specifikující počet výplňových bajtů
- tolik náhodných bajtů
- série nula nebo více párů { instrukce, zpráva }

Instrukce jsou kódovány následovně:

- 1 bajtová hodnota:
  ```
  bity 0-1: typ doručení
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: zpoždění zahrnuto?  (1 = ano, 0 = ne)
     bit 3: fragmentováno?  (1 = ano, 0 = ne)
     bit 4: rozšířené možnosti?  (1 = ano, 0 = ne)
  bity 5-7: rezervováno
  ```
- pokud byl typ doručení TUNNEL, 4 bajtové tunnel ID
- pokud byl typ doručení TUNNEL nebo ROUTER, 32 bajtový router hash
- pokud je příznak zpoždění zahrnuto pravdivý, 1 bajtová hodnota:
  ```
     bit 0: typ (0 = striktní, 1 = náhodný)
  bity 1-7: exponent zpoždění (2^hodnota minut)
  ```
- pokud je příznak fragmentováno pravdivý, 4 bajtové ID zprávy a 1 bajtová hodnota:
  ```
  bity 0-6: číslo fragmentu
     bit 7: je poslední?  (1 = ano, 0 = ne)
  ```
- pokud je příznak rozšířených možností pravdivý:
  ```
  = 1 bajtová velikost možnosti (v bajtech)
  = tolik bajtů
  ```
- 2 bajtová velikost I2NP zprávy

I2NP zpráva je zakódována ve své standardní podobě a předzpracovaný obsah musí být doplněn na násobek 16 bajtů.

### 2.2) Zpracování gateway {#tunnel.gateway}

Po předzpracování zpráv do paddovaného payload gateway zašifruje payload osmi klíči, sestaví blok kontrolního součtu, aby každý peer mohl kdykoli ověřit integritu payload, a také blok pro end-to-end ověření, aby endpoint tunelu mohl ověřit integritu bloku kontrolního součtu. Konkrétní detaily následují.

Použité šifrování je takové, že dešifrování vyžaduje pouze průchod dat pomocí AES v CBC režimu, výpočet SHA256 určité pevné části zprávy (bajty 16 až $size-144) a vyhledání prvních 16 bajtů tohoto hashe v bloku kontrolního součtu. Je definován pevný počet skoků (8 peerů), abychom mohli zprávu ověřit bez prozrazení pozice v tunnel nebo bez toho, aby se zpráva neustále "zmenšovala" při odstraňování vrstev. Pro tunnel kratší než 8 skoků se tvůrce tunnel ujme místa přebytečných skoků a dešifruje pomocí svých klíčů (pro odchozí tunnel se to provádí na začátku a pro příchozí tunnel na konci).

Nejtěžší část šifrování spočívá v sestavení bloku propletených kontrolních součtů, což v podstatě vyžaduje zjištění, jak bude vypadat hash užitečného obsahu v každém kroku, náhodné uspořádání těchto hashů a následné vytvoření matice toho, jak bude každý z těchto náhodně uspořádaných hashů vypadat v každém kroku. Gateway samotná se musí tvářit, že je jedním z účastníků v bloku kontrolních součtů, aby první skok nemohl poznat, že předchozí skok byla gateway. Pro lepší představu:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
Ve výše uvedeném je P[7] stejné jako původní data procházející tunelem (předpracované zprávy) a V[7] je prvních 16 bajtů SHA256 z eH[0-7], jak je vidí peer7 po dešifrování. Pro buňky v matici "výše" než hash je jejich hodnota odvozena šifrováním buňky pod ní klíčem pro peer pod ní, přičemž se používá konec sloupce nalevo od ní jako IV. Pro buňky v matici "níže" než hash se rovnají buňce nad nimi, dešifrované klíčem aktuálního peera, přičemž se používá konec předchozího šifrovaného bloku na tomto řádku.

S touto randomizovanou maticí kontrolních bloků bude každý peer schopen najít hash užitečného obsahu, nebo pokud tam není, zjistit, že je zpráva poškozena. Zapletení pomocí CBC režimu zvyšuje obtížnost označování samotných kontrolních bloků, ale stále je možné, že takové označování zůstane krátce nedetekováno, pokud sloupce po označených datech již byly použity ke kontrole užitečného obsahu u peera. V každém případě koncový bod tunelu (peer 7) ví s jistotou, zda byl některý z kontrolních bloků označen, protože by to poškodilo verifikační blok (V[7]).

IV[0] je náhodná 16bajtová hodnota a IV[i] je prvních 16 bajtů z H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Nepoužíváme stejný IV podél cesty, protože by to umožnilo triviální kolizi, a používáme hash dešifrované hodnoty k propagaci IV, abychom ztížili únik klíčů. IV_WHITENER je pevná 16bajtová hodnota.

Když gateway chce odeslat zprávu, exportuje správný řádek pro peer, který je prvním hopem (obvykle řádek peer1.recv) a předá ho celý.

### 2.3) Zpracování účastníka {#tunnel.participant}

Když účastník v tunnelu obdrží zprávu, dešifruje vrstvu se svým tunnel klíčem pomocí AES256 v CBC režimu s prvními 16 bajty jako IV. Poté vypočítá hash toho, co vidí jako payload (bajty 16 až $size-144) a vyhledá těchto prvních 16 bajtů tohoto hashe v dešifrovaném bloku kontrolního součtu. Pokud se nenajde žádná shoda, zpráva se zahodí. V opačném případě se IV aktualizuje tak, že se dešifruje, tato hodnota se XORuje s IV_WHITENER a nahradí se prvními 16 bajty jejího hashe. Výsledná zpráva se pak předá dalšímu peeru ke zpracování.

Pro zabránění replay útokům na úrovni tunelu si každý účastník udržuje přehled o IV obdržených během životnosti tunelu a odmítá duplikáty. Potřebné využití paměti by mělo být minimální, protože každý tunel má pouze velmi krátkou životnost (momentálně 10 minut). Konstantní 100KBps přes tunel s plnými 32KB zprávami by dalo 1875 zpráv, vyžadující méně než 30KB paměti. Gateways a endpoints zpracovávají replay sledováním ID zpráv a expirací I2NP zpráv obsažených v tunelu.

### 2.4) Zpracování koncového bodu {#tunnel.endpoint}

Když zpráva dosáhne koncového bodu tunelu, ten ji dešifruje a ověří jako normální účastník. Pokud má blok kontrolního součtu platnou shodu, koncový bod poté vypočítá hash samotného bloku kontrolního součtu (jak je vidět po dešifrování) a porovná jej s dešifrovaným ověřovacím hashem (posledních 16 bajtů). Pokud se tento ověřovací hash neshoduje, koncový bod si všimne pokusu o označení ze strany jednoho z účastníků tunelu a možná zprávu zahodí.

V tomto okamžiku má koncový bod tunelu předpracovaná data odeslaná bránou, která pak může analyzovat na obsažené I2NP zprávy a přeposlat je podle požadavků v jejich doručovacích instrukcích.

### 2.5) Padding {#tunnel.padding}

Možných je několik strategií pro vyplňování tunnelů, každá má své vlastní výhody:

- Bez doplňování
- Doplnění na náhodnou velikost
- Doplnění na pevnou velikost
- Doplnění na nejbližší KB
- Doplnění na nejbližší exponenciální velikost (2^n bajtů)

*Které použít? žádné padding je nejefektivnější, náhodné padding je to, co máme nyní, pevná velikost by buď byla extrémní plýtvání nebo nás donutila implementovat fragmentaci. Padding na nejbližší exponenciální velikost (jako Freenet) se zdá slibný. Možná bychom měli shromáždit nějaké statistiky o síti ohledně velikosti zpráv, pak zjistit, jaké náklady a výhody by vznikly z různých strategií?*

### 2.6) Fragmentace tunnelu {#tunnel.fragmentation}

Pro různá schémata vyplňování a míchání může být z hlediska anonymity užitečné rozdělit jedinou I2NP zprávu na více částí, přičemž každá je doručena samostatně prostřednictvím různých tunnel zpráv. Koncový bod může, ale nemusí podporovat tuto fragmentaci (zahazování nebo uchovávání fragmentů podle potřeby), a zpracování fragmentace nebude implementováno okamžitě.

### 2.7) Alternativy {#tunnel.alternatives}

#### 2.7.1) Nepoužívat blok kontrolního součtu {#tunnel.nochecksum}

Jednou alternativou k výše uvedenému procesu je úplné odstranění bloku kontrolního součtu a nahrazení ověřovacího hash jednoduchým hash užitečného obsahu. To by zjednodušilo zpracování na tunnel gateway a ušetřilo by 144 bytů šířky pásma na každém hopu. Na druhé straně by útočníci uvnitř tunnelu mohli triviálně upravit velikost zprávy na takovou, která je snadno sledovatelná spolupracujícími vnějšími pozorovateli spolu s pozdějšími účastníky tunnelu. Poškození by také způsobilo plýtvání celou šířkou pásma potřebnou pro předání zprávy. Bez ověřování per-hop by bylo také možné spotřebovávat nadměrné síťové zdroje vybudováním extrémně dlouhých tunnelů nebo vybudováním smyček do tunnelu.

#### 2.7.2) Úprava zpracování tunelu za běhu {#tunnel.reroute}

Zatímco jednoduchý algoritmus směrování tunelů by měl být dostačující pro většinu případů, existují tři alternativy, které lze prozkoumat:

- Zpozdit zprávu v tunelu na libovolném uzlu buď po určitou dobu nebo na náhodné období. Toho by bylo možné dosáhnout nahrazením hashe v kontrolním součtu například prvními 8 bajty hashe, následovanými nějakými instrukcemi pro zpoždění. Alternativně by instrukce mohly říct účastníkovi, aby skutečně interpretoval surové užitečné zatížení tak, jak je, a buď zprávu zahodil nebo ji pokračoval v předávání po cestě (kde by byla interpretována koncovým bodem jako chaff zpráva). Pozdější část by vyžadovala, aby brána upravila svůj šifrovací algoritmus tak, aby vytvořil čistý text užitečného zatížení na jiném uzlu, ale neměl by to být velký problém.

- Umožnit routerům účastnícím se tunelu znovu promíchat zprávu před
  jejím předáním - přesměrovat ji přes jeden z vlastních odchozích tunelů
  tohoto uzlu, s instrukcemi pro doručení k dalšímu skoku. Toto by mohlo být
  použito buď kontrolovaně (s instrukcemi po cestě, jako jsou výše uvedená
  zpoždění) nebo probabilisticky.

- Implementovat kód pro tvůrce tunnelu k předefinování "dalšího kroku" peera v
  tunnelu, což umožní další dynamické přesměrování.

#### 2.7.3) Používejte obousměrné tunnely {#tunnel.bidirectional}

Současná strategie používání dvou oddělených tunelů pro příchozí a odchozí komunikaci není jedinou dostupnou technikou a má důsledky pro anonymitu. Na pozitivní straně, používáním oddělených tunelů se snižuje množství dopravních dat vystavených analýze účastníkům tunelu - například vrstevníci v odchozím tunelu z webového prohlížeče by viděli pouze provoz HTTP GET požadavku, zatímco vrstevníci v příchozím tunelu by viděli užitečný obsah doručovaný tunelem. U obousměrných tunelů by všichni účastníci měli přístup k informaci, že například 1KB bylo odesláno jedním směrem a poté 100KB druhým směrem. Na negativní straně, používání jednosměrných tunelů znamená, že existují dvě sady vrstevníků, které je třeba profilovat a zohlednit, a je nutné věnovat dodatečnou pozornost zvýšené rychlosti predecessor útoků. Proces sdružování a budování tunelů popsaný níže by měl minimalizovat obavy z predecessor útoku, i když kdyby to bylo žádoucí, nebylo by příliš složité vybudovat příchozí i odchozí tunely podél stejných vrstevníků.

#### 2.7.4) Použití menší velikosti bloku {#tunnel.smallerhashes}

V současné době naše použití AES omezuje velikost bloku na 16 bajtů, což zároveň poskytuje minimální velikost pro každý ze sloupců kontrolního bloku. Pokud by byl použit jiný algoritmus s menší velikostí bloku, nebo by jinak umožnil bezpečné sestavení kontrolního bloku s menšími částmi hashe, mohlo by stát za to to prozkoumat. 16 bajtů používaných nyní v každém hopu by mělo být více než dostačující.

## 3) Budování tunelů {#tunnel.building}

Při budování tunnel musí tvůrce odeslat požadavek s potřebnými konfiguračními daty každému ze skoků, poté počkat na odpověď potenciálního účastníka, který sdělí, zda souhlasí nebo nesouhlasí. Tyto zprávy s požadavky na tunnel a jejich odpovědi jsou zabaleny pomocí garlic encryption, takže je může dešifrovat pouze router, který zná klíč, a cesta vedoucí oběma směry je také směrována prostřednictvím tunnel. Při vytváření tunnelů je třeba mít na paměti tři důležité rozměry: jaké peer uzly se používají (a kde), jak se odesílají požadavky (a přijímají odpovědi), a jak se udržují.

### 3.1) Výběr uzlů {#tunnel.peerselection}

Kromě dvou typů tunelů - příchozích a odchozích - existují dva styly výběru peerů používané pro různé tunely - exploratory a klientské. Exploratory tunely se používají jak pro údržbu síťové databáze, tak pro údržbu tunelů, zatímco klientské tunely se používají pro end-to-end klientské zprávy.

#### 3.1.1) Výběr peer pro průzkumné tunely {#tunnel.selection.exploratory}

Průzkumné tunnely jsou budovány z náhodného výběru peerů z podmnožiny sítě. Konkrétní podmnožina se liší podle místního routeru a podle toho, jaké jsou jeho potřeby pro směrování tunelů. Obecně jsou průzkumné tunnely budovány z náhodně vybraných peerů, kteří jsou v kategorii profilu peera "neselhávaící, ale aktivní". Sekundárním účelem tunelů, kromě pouhého směrování tunelů, je najít nevyužité peery s vysokou kapacitou, aby mohly být povýšeny pro použití v klientských tunelech.

#### 3.1.2) Výběr protějšků pro klientský tunnel {#tunnel.selection.client}

Klientské tunnely jsou budovány s přísnějšími požadavky - lokální router vybírá uzly ze své kategorie profilů "rychlé a vysokokapacitní", aby výkon a spolehlivost splnily potřeby klientské aplikace. Existuje však několik důležitých detailů nad rámec tohoto základního výběru, kterých je třeba se držet v závislosti na anonymitních potřebách klienta.

Pro některé klienty, kteří se obávají, že protivníci provedou předchůdcový útok, může výběr tunelů udržovat partnery vybrané ve striktním pořadí - pokud jsou A, B a C v tunelu, hop po A je vždy B a hop po B je vždy C. Méně striktní pořadí je také možné, které zajišťuje, že zatímco hop po A může být B, B nikdy nemůže být před A. Další možnosti konfigurace zahrnují schopnost, aby byly pevné pouze brány příchozích tunelů a koncové body odchozích tunelů, nebo aby se rotovaly podle rychlosti MTBF.

### 3.2) Doručení požadavku {#tunnel.request}

Jak bylo zmíněno výše, jakmile tvůrce tunnelu ví, kteří peeři by měli být do tunnelu zahrnuti a v jakém pořadí, tvůrce sestaví sérii zpráv s požadavky na tunnel, z nichž každá obsahuje potřebné informace pro daného peera. Například účastnické tunnely dostanou 4-bajtové tunnel ID, na kterém mají přijímat zprávy, 4-bajtové tunnel ID, na kterém mají zprávy odesílat, 32-bajtový hash identity dalšího skoku a 32-bajtový layer klíč používaný k odstranění vrstvy z tunnelu. Samozřejmě odchozí koncové body tunnelů nedostávají žádné informace o "dalším skoku" nebo "dalším tunnel ID". Příchozí tunnel gateways však dostávají 8 layer klíčů v pořadí, v jakém mají být šifrovány (jak je popsáno výše). Pro umožnění odpovědí obsahuje požadavek náhodný session tag a náhodný session klíč, kterým může peer garlic zašifrovat své rozhodnutí, stejně jako tunnel, do kterého má být tento garlic odeslán. Kromě výše uvedených informací mohou být zahrnuty různé klientsky specifické možnosti, jako je jaké omezování na tunnel uplatnit, jaké strategie pro padding nebo dávkování použít, atd.

Po vytvoření všech požadavkových zpráv jsou tyto zabaleny pomocí garlic encryption pro cílový router a odeslány přes exploratory tunnel. Po obdržení daný peer určí, zda může nebo chce participovat, vytvoří odpověď a jak zabalí pomocí garlic encryption, tak směruje tunnel odpověď s dodanými informacemi. Po obdržení odpovědi u tvůrce tunnel je tunnel považován za platný na tomto hopu (pokud byl přijat). Jakmile všichni peerové přijmou, tunnel je aktivní.

### 3.3) Sdružování {#tunnel.pooling}

Pro umožnění efektivního provozu si router udržuje řadu poolů tunelů, z nichž každý spravuje skupinu tunelů používaných pro specifický účel s vlastní konfigurací. Když je pro daný účel potřeba tunnel, router náhodně vybere jeden z příslušného poolu. Celkově existují dva exploratory tunnel pooly - jeden inbound a jeden outbound - každý používající výchozí nastavení pro průzkum routeru. Kromě toho existuje pár poolů pro každou místní destinaci - jeden inbound a jeden outbound tunnel. Tyto pooly používají konfiguraci specifikovanou při připojení místní destinace k routeru, nebo výchozí nastavení routeru, pokud není specifikována.

Každý pool má ve své konfiguraci několik klíčových nastavení, která definují kolik tunnelů držet aktivních, kolik záložních tunnelů udržovat v případě selhání, jak často tunnely testovat, jak dlouhé by tunnely měly být, zda by tyto délky měly být randomizované, jak často by měly být stavěny náhradní tunnely, stejně jako jakákoli další nastavení povolená při konfiguraci jednotlivých tunnelů.

### 3.4) Alternativy {#tunnel.building.alternatives}

#### 3.4.1) Teleskopické budování {#tunnel.building.telescoping}

Jedna otázka, která může vyvstat ohledně použití průzkumných tunelů pro odesílání a přijímání zpráv o vytváření tunelů, je jak to ovlivňuje zranitelnost tunelu vůči útokům předchůdce. Zatímco koncové body a brány těchto tunelů budou náhodně distribuovány po síti (možná dokonce včetně tvůrce tunelu v této množině), další alternativou je použít samotné cesty tunelů k předávání požadavků a odpovědí, jak se to dělá v [TOR](https://www.torproject.org/). To však může vést k únikům během vytváření tunelu, což umožňuje uzlům zjistit, kolik skoků je později v tunelu, sledováním časování nebo počtu paketů při budování tunelu. Mohly by být použity techniky k minimalizaci tohoto problému, jako je použití každého ze skoků jako koncových bodů (podle [2.7.2](#tunnel.reroute)) pro náhodný počet zpráv před pokračováním v budování dalšího skoku.

#### 3.4.2) Neprůzkumné tunnely pro správu {#tunnel.building.nonexploratory}

Druhou alternativou k procesu budování tunelů je poskytnout routeru další sadu neprůzkumných vstupních a výstupních poolů, které se použijí pro požadavky a odpovědi tunelů. Za předpokladu, že router má dobře integrovaný pohled na síť, to by nemělo být nutné, ale pokud by byl router nějakým způsobem rozdělen, použití neprůzkumných poolů pro správu tunelů by snížilo únik informací o tom, které peery jsou v routerově oddílu.

## 4) Omezování tunnel {#tunnel.throttling}

Přestože tunnely v rámci I2P připomínají síť s přepínáním okruhů, vše v I2P je striktně založeno na zprávách - tunnely jsou pouze účetními triky, které pomáhají organizovat doručování zpráv. Nepředpokládá se žádná spolehlivost nebo pořadí zpráv a opakované přenosy jsou ponechány vyšším úrovním (např. klientská streamovací knihovna I2P). To umožňuje I2P využít techniky omezování dostupné jak pro sítě s přepínáním paketů, tak pro sítě s přepínáním okruhů. Například každý router může sledovat klouzavý průměr toho, kolik dat každý tunnel používá, kombinovat to se všemi průměry používanými ostatními tunnely, kterých se router účastní, a být schopen přijmout nebo odmítnout další požadavky na účast v tunnelu na základě své kapacity a využití. Na druhou stranu každý router může jednoduše zahazovat zprávy, které překračují jeho kapacitu, využívaje výzkum používaný na běžném internetu.

## 5) Míšení/dávkování {#tunnel.mixing}

Jaké strategie by měly být použity na gateway a na každém hopu pro zpoždění, přeřazení, přesměrování nebo padding zpráv? Do jaké míry by to mělo být prováděno automaticky, kolik by mělo být konfigurováno jako nastavení per tunnel nebo per hop a jak by měl tvůrce tunnelu (a následně uživatel) řídit tuto operaci? Vše toto zůstává neznámé a bude vypracováno pro budoucí vydání.
