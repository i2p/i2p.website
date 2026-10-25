---
title: "Datagramy"
description: "Autentizované, odpověditelné a surové formáty zpráv nad I2CP"
slug: "datagrams"
aliases:
  - "/cs/datagrams"
  - "/cs/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Přehled datagramů {#overview}

Datagramy staví na základním [I2CP](/docs/specs/i2cp) a poskytují autentizované a odpověditelné zprávy ve standardním formátu. To umožňuje aplikacím spolehlivě přečíst adresu "od" z datagramu a vědět, že adresa skutečně poslala zprávu. Toto je nezbytné pro některé aplikace, protože základní I2P zpráva je zcela raw - nemá žádnou adresu "od" (na rozdíl od IP paketů). Navíc jsou zpráva a odesílatel autentizováni podpisem payload.

Datagramy, stejně jako [pakety streaming library](/docs/api/streaming), jsou konstrukt na úrovni aplikace. Tyto protokoly jsou nezávislé na nízkoúrovňových [transportech](/docs/overview/transport); protokoly jsou routerem převedeny na I2NP zprávy a kterýkoli protokol může být přenášen kterýmkoli transportem.

## Průvodce aplikacemi {#application}

Aplikace napsané v Javě mohou používat datagram API, zatímco aplikace v jiných jazycích mohou používat datagram podporu [SAM](/docs/api/samv3). Existuje také omezená podpora v i2ptunnel v [SOCKS proxy](/docs/api/socks), typech tunelů 'streamr' a třídách udpTunnel.

### Délka datagramu {#length}

Návrhář aplikace by měl pečlivě zvážit kompromis mezi odpovědními a neodpovědními datagramy. Také velikost datagramu bude ovlivňovat spolehlivost kvůli fragmentaci tunelu na 1KB tunnel zprávy. Čím více fragmentů zprávy, tím pravděpodobnější je, že jeden z nich bude zahozen některým mezilehlým uzlem. Zprávy větší než několik KB se nedoporučují. Nad přibližně 10 KB pravděpodobnost doručení dramaticky klesá.

[Viz stránku specifikace datagramů.](/docs/specs/datagrams)

Také si všimněte, že různé režie přidané nižšími vrstvami, zejména garlic messages, představují velkou zátěž pro občasné zprávy, jaké používá aplikace Kademlia-over-UDP. Implementace jsou v současnosti vyladěny pro častý provoz pomocí streaming knihovny.

### Číslo protokolu a porty I2CP {#protocol}

Standardní číslo I2CP protokolu pro podepsané (odpověditelné) datagramy je PROTO_DATAGRAM (17). Aplikace mohou nebo nemusí zvolit nastavení protokolu v I2CP hlavičce. Výchozí hodnota závisí na implementaci. Musí být nastavena pro demultiplexování datagramového a streaming provozu přijatého na stejné Destination.

Jelikož datagramy nejsou orientované na připojení, aplikace může vyžadovat čísla portů pro korelaci datagramů s konkrétními partnery nebo komunikačními relacemi, jak je tradiční u UDP přes IP. Aplikace mohou přidat porty 'from' a 'to' do I2CP (gzip) hlavičky jak je popsáno na [stránce I2CP](/docs/specs/i2cp#format).

V datagram API neexistuje metoda pro specifikaci, zda je datagram neopatřitelný odpovědí (raw) nebo opatřitelný odpovědí. Aplikace by měla být navržena tak, aby očekávala příslušný typ. Aplikace by měla používat číslo I2CP protokolu nebo port k indikaci typu datagramu. Čísla I2CP protokolů PROTO_DATAGRAM (podepsaný, také známý jako Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2 a PROTO_DATAGRAM3 jsou definována v I2PSession API pro tento účel. Běžný návrhový vzor v klient/server datagram aplikacích je použití podepsaných datagramů pro požadavek, který obsahuje nonce, a použití raw datagramu pro odpověď, přičemž se vrátí nonce z požadavku.

**Výchozí hodnoty:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Integrita dat {#integrity}

Integrita dat je zajištěna pomocí gzip CRC-32 kontrolního součtu implementovaného v [I2CP vrstvě](/docs/specs/i2cp#format). Autentizované datagramy (Datagram1 a Datagram2) také zajišťují integritu. V protokolu datagramů není žádné pole pro kontrolní součet.

### Zapouzdření paketů {#encapsulation}

Každý datagram je odeslán přes I2P jako jediná zpráva (nebo jako jednotlivý segment v [Garlic Message](/docs/overview/garlic-routing)). Zapouzdření zpráv je implementováno v základních vrstvách [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np) a [tunnel message](/docs/specs/tunnel-message). V datagram protokolu neexistuje žádný mechanismus oddělovače paketů nebo pole délky.

## Specifikace {#spec}

[Viz stránku specifikace datagramů.](/docs/specs/datagrams)
