---
title: "Směrování tunelu"
description: "Přehled terminologie I2P tunelů, jejich konstrukce a životního cyklu"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

I2P vytváří dočasné, jednosměrné tunnely — uspořádané sekvence routerů, které přeposílají šifrovaný provoz. Tunnely jsou klasifikovány jako **inbound** (zprávy směřují k tvůrci) nebo **outbound** (zprávy směřují pryč od tvůrce).

Typická výměna směruje Alicinu zprávu ven přes jeden z jejích odchozích tunnelů, instruuje odchozí koncový bod, aby ji přeposlal na bránu jednoho z Bobových příchozích tunnelů, a poté ji Bob přijme na svém příchozím koncovém bodě.

![Alice se připojuje přes svůj odchozí tunnel k Bobovi prostřednictvím jeho příchozího tunnelu](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

Tunnely mají pevnou životnost 10 minut a přenášejí zprávy s pevnou velikostí 1024 bajtů (1028 bajtů včetně hlavičky tunelu), aby se zabránilo analýze provozu na základě velikosti zpráv nebo časových vzorů.

## Slovník tunelů

- **Tunnel gateway:** První router v tunelu. U příchozích tunelů se identita tohoto routeru objevuje v publikovaném [LeaseSet](/docs/specs/common-structures/). U odchozích tunelů je gateway výchozí router (A a D výše).
- **Tunnel endpoint:** Poslední router v tunelu (C a F výše).
- **Tunnel participant:** Zprostředkující router v tunelu (B a E výše). Účastníci nemohou určit svou pozici ani směr tunelu.
- **n-hop tunnel:** Počet přeskoků mezi routery.
  - **0-hop:** Gateway a endpoint jsou stejný router – minimální anonymita.
  - **1-hop:** Gateway se připojuje přímo k endpointu – nízká latence, nízká anonymita.
  - **2-hop:** Výchozí nastavení pro průzkumné tunely; vyvážené zabezpečení/výkon.
  - **3-hop:** Doporučeno pro aplikace vyžadující silnou anonymitu.
- **Tunnel ID:** 4-bajtové celé číslo unikátní pro každý router a každý přeskok, náhodně vybrané tvůrcem. Každý přeskok přijímá a přeposílá na různých ID.

## Informace o vytváření tunelů

Routery plnící role gateway, participant a endpoint obdrží různé záznamy v rámci Tunnel Build Message. Moderní I2P podporuje dvě metody:

- **ElGamal** (starší verze, 528-bajtové záznamy)
- **ECIES-X25519** (aktuální, 218-bajtové záznamy prostřednictvím Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**Gateway obdrží:** - Klíč vrstvy tunelu (klíč AES-256 nebo ChaCha20 v závislosti na typu tunelu) - Klíč IV tunelu (pro šifrování inicializačních vektorů) - Klíč odpovědi a IV odpovědi (pro šifrování odpovědi při vytváření) - ID tunelu (pouze pro příchozí gateway) - Hash identity dalšího uzlu a ID tunelu (pokud není koncový)

**Zprostředkující účastníci obdrží:** - Klíč vrstvy tunnel a IV klíč pro jejich skok - ID tunnel a informace o dalším skoku - Klíč odpovědi a IV pro šifrování odpovědi na vytvoření

**Koncové body přijímají:** - Klíče vrstvy tunelu a IV - Router odpovědi a ID tunelu (pouze odchozí koncové body) - Klíč odpovědi a IV (pouze odchozí koncové body)

Pro úplné podrobnosti viz [Specifikace vytváření tunnelů](/docs/specs/implementation/) a [Specifikace vytváření ECIES tunnelů](/docs/specs/implementation/).

## Tunnel Pooling

Routery seskupují tunely do **fondů tunelů** (tunnel pools) pro redundanci a distribuci zátěže. Každý fond udržuje více paralelních tunelů, což umožňuje převzetí funkcí při selhání jednoho tunelu. Fondy používané interně jsou **exploratory tunnels**, zatímco fondy specifické pro aplikace jsou **client tunnels**.

Každá destinace udržuje oddělené příchozí a odchozí skupiny konfigurované pomocí I2CP voleb (počet tunelů, počet záloh, délka a QoS parametry). Routery monitorují stav tunelů, provádějí periodické testy a automaticky obnovují selhané tunely pro udržení velikosti skupiny.

## Sdružování tunelů

**0-hop tunely**: Nabízejí pouze věrohodné popření. Provoz vždy pochází a končí na stejném routeru — nedoporučuje se pro jakékoli anonymní použití.

**1-hop Tunnely**: Poskytují základní anonymitu proti pasivním pozorovatelům, ale jsou zranitelné, pokud protivník ovládá tento jediný hop.

**2-hop Tunnels**: Zahrnují dva vzdálené routery a výrazně zvyšují náklady na útok. Výchozí nastavení pro průzkumné fondy.

**3-hop Tunnely**: Doporučeno pro aplikace vyžadující robustní ochranu anonymity. Další přeskoky přidávají latenci bez smysluplného zvýšení bezpečnosti.

**Výchozí nastavení**: Routery používají **2-hop** průzkumné tunely a aplikačně specifické **2 nebo 3 hop** klientské tunely, což vyvažuje výkon a anonymitu.

## Délka tunelu

Routery pravidelně testují tunely odesláním `DeliveryStatusMessage` přes odchozí tunel do příchozího tunelu. Pokud test selže, oba tunely obdrží zápornou váhu v profilu. Po po sobě jdoucích selháních je tunel označen jako nepoužitelný; router poté sestaví náhradu a zveřejní nový LeaseSet. Výsledky vstupují do metrik kapacity uzlů používaných [systémem výběru uzlů](/docs/overview/tunnel-routing/).

## Testování tunelů

Routery konstruují tunnely pomocí neinteraktivní **teleskopické** metody: jedna Tunnel Build Message se šíří po jednotlivých hopech. Každý hop dešifruje svůj záznam, přidá svou odpověď a přepošle zprávu dál. Konečný hop vrací agregovanou odpověď o výstavbě tunnelu jinou cestou, čímž zabraňuje korelaci. Moderní implementace používají **Short Tunnel Build Messages (STBM)** pro ECIES a **Variable Tunnel Build Messages (VTBM)** pro starší cesty. Každý záznam je šifrován per-hop pomocí ElGamal nebo ECIES-X25519.

## Vytvoření tunelu

Provoz v tunelu používá vícevrstvé šifrování. Každý přeskok přidává nebo odstraňuje vrstvu šifrování, jak zprávy procházejí tunelem.

- **ElGamal tunnels:** AES-256/CBC pro datové části s PKCS#5 paddingem.
- **ECIES tunnels:** ChaCha20 nebo ChaCha20-Poly1305 pro autentizované šifrování.

Každý skok má dva klíče: **layer key** a **IV key**. Routery dešifrují IV, použijí jej ke zpracování datové části, poté IV znovu zašifrují před předáním. Toto dvojité schéma IV zabraňuje značkování zpráv.

Odchozí brány předem dešifrují všechny vrstvy, takže koncové body obdrží otevřený text poté, co všichni účastníci přidali šifrování. Příchozí tunely šifrují v opačném směru. Účastníci nemohou určit směr ani délku tunelu.

## Šifrování tunelů

- Dynamické životnosti tunelů a adaptivní velikost poolů pro vyvážení síťové zátěže
- Alternativní strategie testování tunelů a diagnostika jednotlivých hopů
- Volitelná validace proof-of-work nebo certifikátů šířky pásma (implementováno v API 0.9.65+)
- Výzkum tvarování provozu a vkládání chaff pro míchání koncových bodů
- Pokračující vyřazování ElGamal a migrace na ECIES-X25519

## Průběžný vývoj

- [Specifikace implementace tunelů](/docs/specs/implementation/)
- [Specifikace vytváření tunelů (ElGamal)](/docs/specs/implementation/)
- [Specifikace vytváření tunelů (ECIES-X25519)](/docs/specs/implementation/)
- [Specifikace zpráv tunelů](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Profilování a výběr peerů](/docs/overview/tunnel-routing/)
- [Model hrozeb I2P](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag šifrování](/docs/legacy/elgamal-aes/)
- [I2CP možnosti](/docs/specs/i2cp/)
