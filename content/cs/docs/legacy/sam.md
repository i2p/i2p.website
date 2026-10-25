---
title: "SAM V1 Specifikace"
description: "Starší protokol Simple Anonymous Messaging verze 1 (zastaralý)"
slug: "sam"
aliases:
  - "/cs/docs/api/sam"
  - "/cs/docs/api/sam/"
  - "/cs/sam"
  - "/cs/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Varování - Zastaralé - Nepodporované - Použijte [SAMv3](/docs/api/samv3)

Níže je specifikována verze 1 jednoduchého klientského protokolu pro interakci s I2P. Novější alternativy: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Jazykové knihovny pro SAMv1 API

- C
- C#
- Perl
- Python

Knihovny jsou v zdrojovém repozitáři I2P.

### I2P 0.9.14 Změny

Hlášená verze zůstává "1.0".

- DEST GENERATE nyní podporuje parametr SIGNATURE_TYPE.
- Parametr MIN v HELLO VERSION je nyní nepovinný.
- Parametry MIN a MAX v HELLO VERSION nyní podporují jednociferné verze jako "3".

## Protokol verze 1

Klientská aplikace komunikuje s SAM bridge, který se stará o veškerou I2P funkcionalité (pomocí streaming lib pro virtuální proudy, nebo I2CP přímo pro asynchronní zprávy).

Veškerá komunikace mezi klientem a SAM bridge je nešifrovaná a neautentizovaná přes jeden TCP socket. Přístup k SAM bridge by měl být chráněn pomocí firewallů nebo jiných prostředků (možná může mít bridge ACL seznam povolených IP adres, ze kterých přijímá připojení).

Všechny tyto SAM zprávy jsou odesílány na jednom řádku v prostém ASCII, ukončené znakem nového řádku (\\n). Formátování zobrazené níže slouží pouze pro čitelnost, a zatímco první dvě slova v každé zprávě musí zůstat ve svém specifickém pořadí, pořadí párů klíč=hodnota se může měnit (např. "ONE TWO A=B C=D" nebo "ONE TWO C=D A=B" jsou obě dokonale platné konstrukce). Navíc je protokol citlivý na velikost písmen.

SAM zprávy jsou interpretovány v UTF-8. Páry klíč=hodnota musí být odděleny jednou mezerou. Hodnoty mohou být uzavřeny v uvozovkách, pokud obsahují mezery, např. klíč="dlouhý text hodnoty". Neexistuje žádný mechanismus escapování.

Komunikace může mít tři odlišné formy:

- [Virtuální proudy](/docs/api/streaming)
- [Odpověditelné datagramy](/docs/specs/datagrams#repliable) (zprávy s polem FROM)
- [Anonymní datagramy](/docs/specs/datagrams#raw) (surové anonymní zprávy)

## SAM Connection Handshake

Žádná SAMv3 komunikace nemůže probíhat, dokud se klient a bridge nedohodnou na verzi protokolu, což se provádí tak, že klient pošle HELLO a bridge odpoví HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
a

```
HELLO REPLY RESULT=$result VERSION=1.0
```
Od I2P 0.9.14 je parametr MIN volitelný. Parametr MAX musí být poskytnut a musí být větší nebo roven "1" a menší než "2" pro použití verze 1.

Hodnota RESULT může být jedna z následujících:

- `OK`
- `NOVERSION`

## SAM Sessions

SAM session je vytvořena tak, že klient otevře socket k SAM bridge, provede handshake a odešle zprávu SESSION CREATE, a session se ukončí, když je socket odpojen.

Každá I2P Destination může být současně použita pouze pro jednu SAM relaci a může používat pouze jednu z těchto forem (zprávy přijaté prostřednictvím jiných forem jsou zahozeny).

Zpráva SESSION CREATE odeslaná klientem na bridge je následující:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION určuje, jaká destinace má být použita pro odesílání a přijímání zpráv/streamů. Pokud je zadán $name, SAM bridge prohledává své vlastní lokální úložiště (soubor sam.keys) pro přidruženou destinaci (a soukromý klíč). Pokud neexistuje žádná asociace odpovídající danému jménu, vytvoří novou. Pokud je destinace specifikována jako TRANSIENT, vždy vytvoří novou.

Poznamenejte, že DESTINATION je identifikátor, *nikoli* Base 64 kódovaná data. Pro specifikaci Destination musíte použít [SAM V3](/docs/api/samv3).

DIRECTION lze specifikovat pouze pro STREAM relace, čímž se most informuje, že klient bude buď vytvářet nebo přijímat streamy, nebo obojí. Pokud není specifikováno, předpokládá se BOTH. Pokus o vytvoření odchozího streamu při DIRECTION=RECEIVE by měl vyústit v chybu a příchozí streamy při DIRECTION=CREATE budou ignorovány.

Další zadané možnosti by měly být předány do konfigurace I2P relace, pokud nejsou interpretovány SAM bridge (např. "tunnels.depthInbound=0"). Tyto možnosti jsou dokumentovány níže.

SAM bridge by měl být už nakonfigurován s tím, se kterým routerem má komunikovat přes I2P (ačkoli v případě potřeby může existovat způsob, jak toto nastavení přepsat, např. i2cp.tcp.host=localhost a i2cp.tcp.port=7654).

Po přijetí zprávy o vytvoření relace odpoví SAM bridge zprávou o stavu relace následovně:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
Hodnota RESULT může být jedna z:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Pokud není v pořádku, MESSAGE by měla obsahovat člověkem čitelné informace o tom, proč nelze vytvořit relaci.

Všimněte si, že se nevydá žádné varování, pokud není $name nalezeno a místo toho je vytvořena přechodná destinace. Všimněte si, že skutečná přechodná base 64 destinace není uvedena v odpovědi; je to $name nebo TRANSIENT jak bylo dodáno v SESSION CREATE. Pokud potřebujete tyto funkce, musíte použít [SAM V3](/docs/api/samv3).

## SAM virtuální streamy

Virtuální streamy jsou garantovány být odeslány spolehlivě a ve správném pořadí, s oznámením o selhání a úspěchu jakmile je k dispozici.

Po navázání relace s STYLE=STREAM mohou jak klient, tak SAM bridge asynchronně posílat různé zprávy tam a zpět pro správu streamů, jak je uvedeno níže:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Toto vytvoří nové virtuální spojení z lokálního cíle k zadanému uzlu a označí ho jedinečným ID s rozsahem session. Jedinečné ID je ASCII base 10 celé číslo od 1 do (2^31-1).

$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

SAM bridge musí na toto odpovědět zprávou o stavu proudu:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Hodnota RESULT může být jedna z následujících:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

Pokud je RESULT OK, uvedená destinace je aktivní a autorizovala připojení; pokud připojení nebylo možné (timeout, atd.), RESULT bude obsahovat příslušnou chybovou hodnotu (doprovázenu volitelnou lidsky čitelnou zprávou MESSAGE).

Na přijímací straně SAM bridge jednoduše upozorní klienta následovně:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Toto sděluje klientovi, že daná destinace s ním vytvořila virtuální spojení. Následující datový proud bude označen daným jedinečným ID, což je ASCII base 10 celé číslo od -1 do -(2^31-1).

$destination je base 64 kódování [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bytů v binárním formátu), v závislosti na typu podpisu.

Když chce klient odeslat data přes virtuální spojení, postupuje následovně:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Toto přidá zadaná data do bufferu, který se odesílá protějšku přes virtuální spojení. Velikost odesílání $numBytes určuje, kolik 8bitových bajtů je zahrnuto za novým řádkem, což může být 1 až 32768 (32KB).

SAM bridge se pak bude snažit doručit zprávu co nejrychleji a nejefektivněji, případně seskupí více SEND zpráv dohromady. Pokud dojde k chybě při doručování dat nebo pokud vzdálená strana ukončí spojení, SAM bridge informuje klienta:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Hodnota RESULT může být jedna z následujících:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Pokud bylo připojení řádně ukončeno druhou stranou, $result je nastaveno na OK. Pokud $result není OK, MESSAGE může obsahovat popisnou zprávu, například "peer unreachable", atd. Kdykoli by klient chtěl ukončit připojení, pošle SAM bridge zprávu o ukončení:

```
STREAM CLOSE
       ID=$id
```
Bridge poté uklidí vše potřebné a zahodí toto ID - žádné další zprávy na něm již nemohou být odesílány ani přijímány.

Pro druhou stranu komunikace, kdykoli peer odešle nějaká data a jsou dostupná pro klienta, SAM bridge je okamžitě doručí:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Všechny proudy jsou implicitně uzavřeny při přerušení spojení mezi SAM bridge a klientem.

## SAM Repliable Datagrams

Ačkoliv I2P inherentně neobsahuje adresu FROM, pro snadné použití je poskytována dodatečná vrstva jako odpověditelné datagramy - neseřazené a nespolehlivé zprávy o velikosti až 31 744 bajtů, které zahrnují adresu FROM (ponechávají až 1 KB pro hlavičkový materiál). Tato adresa FROM je interně autentizována SAMem (využívá podpisový klíč cíle k ověření zdroje) a zahrnuje ochranu proti opakovanému přehrání.

Minimální velikost je 1. Pro nejlepší spolehlivost doručování se doporučuje maximální velikost přibližně 11 KB.

Po navázání SAM relace s STYLE=DATAGRAM může klient poslat SAM bridge:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Když datagram dorazí, most jej doručí klientovi prostřednictvím:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bajtů v binárním formátu), v závislosti na typu podpisu.

SAM bridge nikdy nevystavuje klientovi autentizační hlavičky nebo jiná pole, pouze data, která poskytl odesílatel. Toto pokračuje, dokud není relace ukončena (klientem, který ukončí spojení).

## SAM anonymní datagramy

Maximálním využitím šířky pásma I2P umožňuje SAM klientům odesílat a přijímat anonymní datagramy, přičemž autentifikaci a informace pro odpověď ponechává na samotných klientech. Tyto datagramy jsou nespolehlivé a neuspořádané a mohou mít až 32768 bajtů.

Minimální velikost je 1. Pro nejlepší spolehlivost doručení je doporučená maximální velikost přibližně 11 KB.

Po navázání SAM relace se STYLE=RAW může klient odeslat SAM bridge:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

Když dorazí surový datagram, most jej doručí klientovi prostřednictvím:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funkčnost SAM Utility

Následující zpráva může být použita klientem pro dotazování SAM bridge na překlad jmen:

```
NAMING LOOKUP
       NAME=$name
```
na což je odpovězeno

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
Hodnota RESULT může být jedna z následujících:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Pokud NAME=ME, pak odpověď bude obsahovat cíl používaný aktuální relací (užitečné pokud používáte TRANSIENT cíl). Pokud $result není OK, MESSAGE může obsahovat popisnou zprávu, jako "bad format", atd.

$destination je base 64 kódování [Destination](/docs/specs/common-structures#type_Destination), které má 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

Veřejné a soukromé base64 klíče mohou být vygenerovány pomocí následující zprávy:

```
DEST GENERATE
```
na kterou je odpovězeno

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Od I2P 0.9.14 je podporován volitelný parametr SIGNATURE_TYPE. Hodnota SIGNATURE_TYPE může být libovolný název (např. ECDSA_SHA256_P256, nerozlišuje velká/malá písmena) nebo číslo (např. 1), které je podporováno [Key Certificates](/docs/specs/common-structures#type_Certificate). Výchozí hodnota je DSA_SHA1.

$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

$privkey je base 64 kódování zřetězení [Destination](/docs/specs/common-structures#type_Destination) následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey) následovaným [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), což je 884 nebo více base 64 znaků (663 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

## Hodnoty RESULT

Toto jsou hodnoty, které může obsahovat pole RESULT, s jejich významem:

| Hodnota | Význam |
|-------|---------|
| `OK` | Operace byla úspěšně dokončena |
| `CANT_REACH_PEER` | Peer existuje, ale nelze se k němu připojit |
| `DUPLICATED_DEST` | Zadaná Destination je již používána |
| `I2P_ERROR` | Obecná I2P chyba (např. odpojení I2CP atd.) |
| `INVALID_KEY` | Zadaný klíč není platný (špatný formát atd.) |
| `KEY_NOT_FOUND` | Jmenný systém nemůže vyřešit zadané jméno |
| `PEER_NOT_FOUND` | Peer nelze nalézt v síti |
| `TIMEOUT` | Časový limit při čekání na událost (např. odpověď peer) |
## Možnosti Tunnel, I2CP a Streaming

Tyto volby mohou být předány jako páry name=value na konci řádku SAM SESSION CREATE.

Všechny relace mohou zahrnovat [I2CP možnosti jako jsou délky tunelů](/docs/protocol/i2cp#options). STREAM relace mohou zahrnovat [možnosti Streaming lib](/docs/api/streaming#options). Podívejte se na tyto reference pro názvy možností a výchozí hodnoty.

## Poznámky k Base 64

Kódování Base 64 musí používat standardní I2P Base 64 abecedu "A-Z, a-z, 0-9, -, ~".

## Implementace klientských knihoven

Klientské knihovny jsou k dispozici pro C, C++, C#, Perl a Python. Tyto se nacházejí v adresáři apps/sam/ v I2P Source Package.

## Výchozí nastavení SAM

Výchozí SAM port je 7656. SAM není ve výchozím nastavení v I2P routeru povolen; musí být spuštěn ručně nebo nakonfigurován pro automatické spuštění na stránce konfigurace klientů v konzoli routeru nebo v souboru clients.config.
