---
title: "Streamované MTU pro cíle ECIES"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Poznámka
Probíhá nasazení a testování v síti.
Může dojít k drobným úpravám.


## Přehled


### Shrnutí

ECIES snižuje režii stávajících zpráv relace (ES) o přibližně 90 bajtů.
Proto můžeme zvýšit MTU o přibližně 90 bajtů pro ECIES spojení.
Viz the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Bez zvýšení MTU se v mnoha případech úspory režie příliš neprojeví,
protože zprávy budou i tak doplněny tak, aby využívaly dvě plné tunelové zprávy.

Tento návrh nevyžaduje žádné změny specifikací.
Je zveřejněn jako návrh pouze za účelem usnadnění diskuse a dosažení konsensu
ohledně doporučené hodnoty a podrobností implementace.


### Cíle

- Zvýšit sjednané MTU
- Maximalizovat využití 1 KB tunelových zpráv
- Neměnit streamovací protokol


## Návrh

Použijte existující možnost MAX_PACKET_SIZE_INCLUDED a dohodu o MTU.
Streamování pokračuje v používání minima poslaného a přijatého MTU.
Výchozí hodnota zůstává 1730 pro všechna spojení, bez ohledu na použité klíče.

Implementace jsou vyzývány, aby zahrnovaly možnost MAX_PACKET_SIZE_INCLUDED ve všech SYN paketech, v obou směrech,
i když to není požadavek.

Pokud je cíl pouze ECIES, použijte vyšší hodnotu (buď jako Alice, nebo Bob).
Pokud je cíl dvouklíčový, chování se může lišit:

Pokud je dvouklíčový klient mimo směrovač (v externí aplikaci),
možná nebude "vědět" o klíči použitým na vzdáleném konci a Alice může požádat
o vyšší hodnotu v SYN, zatímco maximální data v SYN zůstávají 1730.

Pokud je dvouklíčový klient uvnitř směrovače, informace o tom, jaký klíč
je používán, nemusí být klientovi známa.
Leaseset možná ještě nebyl načten nebo interní API rozhraní
nemusí snadno tuto informaci klientovi zpřístupnit.
Pokud informace je k dispozici, Alice může použít vyšší hodnotu;
jinak musí Alice použít standardní hodnotu 1730, dokud není sjednána.

Dvouklíčový klient jako Bob může poslat vyšší hodnotu v odpovědi,
i pokud od Alice nedostal žádnou hodnotu nebo hodnotu 1730;
nicméně, neexistuje ustanovení pro sjednávání směrem nahoru během streamování,
takže MTU by mělo zůstat na 1730.


Jak je uvedeno v the [Streaming API documentation](/docs/api/streaming/),
data v SYN paketech posílaných od Alice k Bobovi mohou překročit Bobovo MTU.
To je slabina streamovacího protokolu.
Proto musí dvouklíčoví klienti omezit data v odesílaných SYN paketech
na 1730 bajtů, zatímco posílají vyšší možnost MTU.
Jakmile Bob pošle vyšší MTU, Alice může zvýšit skutečnou maximální
užitečnou zátěž odesílaných dat.


### Analýza

Jak je popsáno v the [ECIES specification](/docs/specs/ecies/#overhead), režie ElGamal pro stávající zprávy relace je
151 bajtů a Ratchet režie je 69 bajtů.
Proto můžeme zvýšit MTU pro ratchet spojení o (151 - 69) = 82 bajtů,
z 1730 na 1812.


## Specifikace

Přidat následující změny a upřesnění do části Výběr a Sjednávání MTU v the [Streaming API documentation](/docs/api/streaming/).
Žádné změny v the [Streaming specification](/docs/specs/streaming/).


Výchozí hodnota možnosti i2p.streaming.maxMessageSize zůstává 1730 pro všechna spojení, bez ohledu na použité klíče.
Klienti musí použít minimum poslaného a přijatého MTU, jako obvykle.

Existují čtyři související MTU konstanty a proměnné:

- DEFAULT_MTU: 1730, beze změn, pro všechna spojení
- i2cp.streaming.maxMessageSize: výchozí 1730 nebo 1812, může být změněno v konfiguraci
- ALICE_SYN_MAX_DATA: Maximální data, která může Alice zahrnout do SYN paketu
- negotiated_mtu: Minimum z MTU Alice a Boba, které má být použito jako maximální velikost dat
  v SYN ACK od Boba k Alice a ve všech následných paketech posílaných oběma směry


Existuje pět případů, které je třeba zvážit:


### 1) Pouze ElGamal Alice
Žádná změna, 1730 MTU ve všech paketech.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize výchozí: 1730
- Alice může poslat MAX_PACKET_SIZE_INCLUDED v SYN, není požadováno pokud není != 1730


### 2) Pouze ECIES Alice
1812 MTU ve všech paketech.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize výchozí: 1812
- Alice musí poslat MAX_PACKET_SIZE_INCLUDED v SYN


### 3) Dvouklíčová Alice a ví, že Bob je ElGamal
1730 MTU ve všech paketech.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize výchozí: 1812
- Alice může poslat MAX_PACKET_SIZE_INCLUDED v SYN, není požadováno pokud není != 1730


### 4) Dvouklíčová Alice a ví, že Bob je ECIES
1812 MTU ve všech paketech.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize výchozí: 1812
- Alice musí poslat MAX_PACKET_SIZE_INCLUDED v SYN


### 5) Dvouklíčová Alice a Bobův klíč neznámý
Poslat 1812 jako MAX_PACKET_SIZE_INCLUDED v SYN paketu, ale omezit data SYN paketu na 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize výchozí: 1812
- Alice musí poslat MAX_PACKET_SIZE_INCLUDED v SYN


### Pro všechny případy

Alice a Bob vypočítají
negotiated_mtu, minimum z MTU Alice a Boba, které má být použito jako maximální velikost dat
v SYN ACK od Boba k Alice a ve všech následných paketech posílaných oběma směry.


## Odůvodnění

Viz the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) pro vysvětlení, proč je současná hodnota 1730.
Viz the [ECIES specification](/docs/specs/ecies/#overhead) pro vysvětlení, proč je režie ECIES o 82 bajtů menší než u ElGamal.


## Poznámky k implementaci

Pokud streamování vytváří zprávy optimální velikosti, je velmi důležité,
aby vrstva ECIES-Ratchet neprováděla padding nad rámec této velikosti.

Optimální velikost Garlic Message, aby se vešla do dvou tunelových zpráv,
včetně 16 bajtového Garlic Message I2NP záhlaví, 4 bajtové délky Garlic Message,
8 bajtového ES tagu a 16 bajtového MAC, je 1956 bajtů.

Doporučený paddingový algoritmus v ECIES je následující:

- Pokud by celková délka Garlic Message byla 1954-1956 bajtů,
  neprovádějte paddingový blok (není místo)
- Pokud by celková délka Garlic Message byla 1938-1953 bajtů,
  přidejte paddingový blok k dosažení přesně 1956 bajtů.
- Jinak vyplňte obvyklým způsobem, například náhodným množstvím 0-15 bajtů.

Podobné strategie by mohly být použity pro optimální velikost jedné tunelové zprávy (964)
a tří tunelových zpráv (2952), i když tyto velikosti by měly být vzácné v praxi.


## Otázky

Hodnota 1812 je předběžná. K potvrzení a případnému upravení.


## Migrace

Žádné problémy se zpětnou kompatibilitou.
To je existující možnost a sjednávání MTU je již součástí specifikace.

Starší cíle ECIES budou podporovat 1730.
Jakýkoli klient, který obdržel vyšší hodnotu, odpoví s 1730 a vzdálený konec
dohodne snížení, jak je obvyklé.


