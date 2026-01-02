---
title: "Přiřadit OBEPs k IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Přehled

Tento návrh přidává možnost I2CP pro odchozí tunely, která způsobuje, že tunely jsou
vybrány nebo postaveny při odeslání zprávy tak, že OBEP odpovídá jednomu z IBGW z LeaseSet pro cílovou Destinaci.


## Motivace

Většina I2P směrovačů používá formu zahazování paketů pro řízení přetížení. Referenční implementace používá strategii WRED, která bere v úvahu jak velikost zprávy, tak cestovní vzdálenost (viz [dokumentace tunnel throttling](/docs/specs/implementation/#tunnelthrottling)). Díky této strategii je primárním zdrojem ztráty paketů OBEP.


## Návrh

Při odeslání zprávy odesílatel vybere nebo postaví tunel s OBEP, který je stejný směrovač jako jeden z příjemcových IBGW. Tímto způsobem zpráva projde přímo z jednoho tunelu do druhého, aniž by bylo nutné ji posílat přes síť mezi tím.


## Bezpečnostní důsledky

Tento režim by fakticky znamenal, že příjemce vybírá odesílatelův OBEP. Aby byla zachována současná úroveň soukromí, způsobil by tento režim, že odchozí tunely by byly o jeden skok delší, než je určeno volbou outbound.length I2CP (přičemž poslední skok může být mimo rychlý stupeň odesílatele).


## Specifikace

Pro [specifikaci I2CP](/docs/specs/i2cp/) je přidána nová možnost I2CP:

    outbound.matchEndWithTarget
        Boolean

        Výchozí hodnota: závisí na konkrétním případě

        Pokud je pravda, směrovač vybere odchozí tunely pro zprávy odesílané během této
        relace tak, že OBEP tunelu je jeden z IBGW pro cílovou Destinaci. Pokud takový tunel
        neexistuje, směrovač ho postaví.


## Kompatibilita

Zpětná kompatibilita je zajištěna, protože směrovače mohou vždy zasílat zprávy samy sobě.


## Implementace

### Java I2P

Budování tunelů a odesílání zpráv jsou v současné době oddělené subsystémy:

- BuildExecutor zná pouze možnosti outbound.* odchozího poolu tunelů a nemá přehled o jejich použití.

- OutboundClientMessageOneShotJob může pouze vybrat tunel z existujícího
  poolu; pokud přijde klientská zpráva a nejsou žádné odchozí tunely, směrovač zprávu zahodí.

Implementace tohoto návrhu by vyžadovala navržení způsobu, jak tyto dva subsystémy interagují.

### i2pd

Testovací implementace byla dokončena.


## Výkon

Tento návrh má různé účinky na latenci, dobu trvání a ztrátu paketů:

- Je pravděpodobné, že ve většině případů by tento režim vyžadoval stavbu nového tunelu při první zprávě, místo použití stávajícího tunelu, což by přidávalo latenci.

- Pro standardní tunely může OBEP potřebovat najít a připojit se k IBGW,
  což by přidávalo latenci, která zvyšuje první dobu trvání (protože k tomu dochází po odeslání prvního paketu). Použitím tohoto režimu by OBEP musel najít a připojit se k IBGW během stavby tunelu, přičemž by přidával stejnou latenci, ale snižoval první dobu trvání (protože k tomu dochází před odesláním prvního paketu).

- Současný standardní VariableTunnelBuild má velikost 2641 bytů. Proto se očekává, že tento režim by vedl k nižší ztrátě paketů pro průměrnou velikost zpráv větší než tato.

Je zapotřebí další výzkum k prozkoumání těchto účinků, aby se rozhodlo, které standardní tunely by měly z tohoto režimu prospěch, pokud by byl povolen ve výchozím nastavení.
