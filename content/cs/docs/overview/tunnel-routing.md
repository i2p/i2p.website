---
title: "Směrování tunelů"
description: "Přehled terminologie, konstrukce a provozu I2P tunnelů"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Přehled

Tato stránka obsahuje přehled terminologie a fungování I2P tunnelů s odkazy na technicky podrobnější stránky, detaily a specifikace.

Jak bylo stručně vysvětleno v [úvodu](/docs/overview/intro/), I2P vytváří virtuální "tunnely" - dočasné a jednosměrné cesty přes sekvenci routerů. Tyto tunnely jsou klasifikovány buď jako příchozí tunnely (kde vše, co je do nich vloženo, směřuje k tvůrci tunnelu) nebo odchozí tunnely (kde tvůrce tunnelu odesílá zprávy od sebe pryč). Když chce Alice poslat zprávu Bobovi, (obvykle) ji pošle jedním ze svých existujících odchozích tunnelů s instrukcemi pro koncový bod tohoto tunnelu, aby ji přeposlal na gateway router jednoho z Bobových aktuálních příchozích tunnelů, který ji následně předá Bobovi.

![Alice se připojuje přes svůj odchozí tunnel k Bobovi prostřednictvím jeho příchozího tunnelu](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Slovník tunnel

- **Tunnel gateway** - první router v tunelu. U příchozích tunelů je to ten, který je uveden v LeaseSet publikovaném v [síťové databázi](/docs/overview/network-database/). U odchozích tunelů je gateway původní router. (např. A i D výše)

- **Tunnel endpoint** - poslední router v tunnel. (např. C i F výše)

- **Účastník tunelu** - všechny routery v tunelu kromě brány nebo koncového bodu (např. jak B, tak E výše)

- **n-Hop tunnel** - tunnel s určitým počtem mezirouterových skoků, např.:
  - **0-hop tunnel** - tunnel, kde je gateway zároveň koncovým bodem
  - **1-hop tunnel** - tunnel, kde gateway komunikuje přímo s koncovým bodem
  - **2-(nebo více)-hop tunnel** - tunnel, kde je alespoň jeden mezilehlý účastník tunnelu. (výše uvedený diagram zahrnuje dva 2-hop tunnely - jeden odchozí od Alice, jeden příchozí k Bobovi)

- **Tunnel ID** - [4bajtové celé číslo](/docs/specs/common-structures/#type_TunnelId) odlišné pro každý hop v tunelu a jedinečné mezi všemi tunely na routeru. Vybráno náhodně tvůrcem tunelu.

---

## Informace o budování tunelu

Routery vykonávající tři role (gateway, participant, endpoint) dostávají různé části dat v počáteční [Tunnel Build Message](/docs/specs/tunnel-creation/) k plnění svých úkolů:

**Tunnel gateway získává:**

- **tunnel encryption key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování zpráv a instrukcí k dalšímu uzlu
- **tunnel IV key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro dvojité šifrování IV k dalšímu uzlu
- **reply key** - [AES veřejný klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování odpovědi na požadavek o vytvoření tunnel
- **reply IV** - IV pro šifrování odpovědi na požadavek o vytvoření tunnel
- **tunnel id** - 4bytové celé číslo (pouze příchozí brány)
- **next hop** - který router je další v cestě (pokud se nejedná o 0-hop tunnel a brána není zároveň koncovým bodem)
- **next tunnel id** - ID tunnel na dalším uzlu

**Všichni zprostředkující účastníci tunnel obdrží:**

- **tunnel encryption key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování zpráv a instrukcí pro další hop
- **tunnel IV key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro dvojité šifrování IV pro další hop
- **reply key** - [AES veřejný klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování odpovědi na požadavek na vytvoření tunnel
- **reply IV** - IV pro šifrování odpovědi na požadavek na vytvoření tunnel
- **tunnel id** - 4 bytové celé číslo
- **next hop** - který router je další v cestě
- **next tunnel id** - ID tunnel na dalším hopu

**Koncový bod tunelu získá:**

- **tunnel encryption key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování zpráv a instrukcí do koncového bodu (sám sebe)
- **tunnel IV key** - [AES privátní klíč](/docs/specs/common-structures/#type_SessionKey) pro dvojité šifrování IV do koncového bodu (sám sebe)
- **reply key** - [AES veřejný klíč](/docs/specs/common-structures/#type_SessionKey) pro šifrování odpovědi na požadavek na vybudování tunnel (pouze odchozí koncové body)
- **reply IV** - IV pro šifrování odpovědi na požadavek na vybudování tunnel (pouze odchozí koncové body)
- **tunnel id** - 4bytové celé číslo (pouze odchozí koncové body)
- **reply router** - příchozí brána tunnel pro odeslání odpovědi (pouze odchozí koncové body)
- **reply tunnel id** - tunnel ID odpovídajícího router (pouze odchozí koncové body)

Podrobnosti jsou ve [specifikaci vytváření tunnelů](/docs/specs/tunnel-creation/).

---

## Sdružování tunnelů

Několik tunnelů pro určitý účel může být seskupeno do "tunnel pool", jak je popsáno ve [specifikaci tunnelů](/docs/specs/tunnel-implementation/#tunnel.pooling). To poskytuje redundanci a dodatečnou šířku pásma. Pool používané samotným routerem se nazývají "exploratory tunnels". Pool používané aplikacemi se nazývají "client tunnels".

---

## Délka tunnel

Jak bylo zmíněno výše, každý klient požaduje, aby mu jeho router poskytl tunnely zahrnující alespoň určitý počet hopů. Rozhodnutí o tom, kolik routerů mít ve svých odchozích a příchozích tunnelech, má důležitý vliv na latenci, propustnost, spolehlivost a anonymitu poskytovanou I2P - čím více peerů musí zprávy projít, tím déle trvá, než se dostanou na místo, a tím větší je pravděpodobnost, že jeden z těchto routerů předčasně selže. Čím méně routerů je v tunnelu, tím snazší je pro protivníka provádět útoky analýzou provozu a narušit něčí anonymitu. Délky tunnelů jsou specifikovány klienty prostřednictvím [možností I2CP](/docs/specs/i2cp/#options). Maximální počet hopů v tunnelu je 7.

### 0-hop tunnely

Bez vzdálených routerů v tunnelu má uživatel velmi základní věrohodné popírání (protože nikdo neví jistě, že peer, který jim zprávu poslal, ji jen nepřeposílal jako součást tunnelu). Nicméně by bylo poměrně snadné provést útok statistickou analýzou a všimnout si, že zprávy cílené na konkrétní destinaci jsou vždy posílány přes jediný gateway. Statistická analýza proti odchozím 0-hop tunnelům je složitější, ale mohla by ukázat podobné informace (ačkoli by byla trochu obtížnější k provedení).

### 1-hop tunnels

Při použití pouze jednoho vzdáleného routeru v tunelu má uživatel jak věrohodnou popiratelnost, tak základní anonymitu, pokud nečelí vnitřnímu protivníkovi (jak je popsáno v [modelu hrozeb](/docs/overview/threat-model/)). Pokud by však protivník provozoval dostatečný počet routerů tak, že jediný vzdálený router v tunelu je často jedním z těchto kompromitovaných routerů, byl by schopen provést výše uvedený útok statistickou analýzou provozu.

### 2-hop tunnely

Se dvěma nebo více vzdálenými routery v tunelu se náklady na provedení útoku analýzou provozu zvyšují, protože by muselo být kompromitováno mnoho vzdálených routerů, aby mohl být útok proveden.

### 3-hop (nebo více) tunnely

Aby se snížila náchylnost k [některým útokům](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), pro nejvyšší úroveň ochrany se doporučuje 3 nebo více skoků. [Nedávné studie](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) také ukazují, že více než 3 skoky nepřináší další ochranu.

### Výchozí délky tunelů

Router používá ve výchozím nastavení 2-hop tunnely pro své exploratory tunnels. Výchozí nastavení klientských tunnelů je určeno aplikací pomocí [I2CP opcí](/docs/specs/i2cp/#options). Většina aplikací používá ve výchozím nastavení 2 nebo 3 hopy.

---

## Testování tunelů

Všechny tunnely jsou periodicky testovány jejich tvůrcem odesláním DeliveryStatusMessage přes odchozí tunnel směrem k jinému příchozímu tunnelu (testují se tak oba tunnely najednou). Pokud některý z nich neuspěje v několika po sobě jdoucích testech, je označen jako nefunkční. Pokud byl používán pro klientův příchozí tunnel, vytvoří se nový leaseSet. Selhání testů tunelů se také projeví v [hodnocení kapacity v peer profilu](/docs/overview/peer-selection/#capacity).

---

Vytváření tunelů je řešeno pomocí [garlic routing](/docs/overview/garlic-routing/) - Tunnel Build Message je odeslána routeru s požadavkem, aby se účastnil tunelu (poskytnutím všech příslušných informací, jak je uvedeno výše, spolu s certifikátem, který je momentálně 'null' certifikát, ale bude podporovat hashcash nebo jiné neplacené certifikáty, když to bude nutné). Tento router předá zprávu dalšímu uzlu v tunelu. Podrobnosti jsou ve [specifikaci vytváření tunelů](/docs/specs/tunnel-creation/).

## Vytváření tunnelů

---

Vícevrstvé šifrování je zpracováno pomocí [garlic encryption](/docs/overview/garlic-routing/) tunelových zpráv. Podrobnosti jsou ve [specifikaci tunelu](/docs/specs/tunnel-implementation/). IV každého uzlu je šifrováno samostatným klíčem, jak je tam vysvětleno.

## Šifrování tunelů

---

---

## Budoucí práce

- Mohly by být použity další techniky testování tunelů, jako je garlic wrapping více testů do cloves, testování jednotlivých účastníků tunelu samostatně, atd.

- Přechod na výchozí nastavení 3-hop exploratory tunnels.

- V některé vzdálené budoucí verzi mohou být implementovány možnosti specifikující nastavení poolingu, míchání a generování chaff.

- V budoucí vzdálené verzi mohou být implementována omezení na množství a velikost zpráv povolených během životnosti tunelu (např. ne více než 300 zpráv nebo 1 MB za minutu).

---

## Viz také

- [Specifikace tunnel](/docs/specs/tunnel-implementation/)
- [Specifikace vytváření tunnel](/docs/specs/tunnel-creation/)
- [Jednosměrné tunnely](/docs/legacy/unidirectional/)
- [Specifikace zpráv tunnel](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP možnosti](/docs/specs/i2cp/#options)
