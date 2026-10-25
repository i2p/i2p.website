---
title: "Specifikace SAM V2"
description: "Legacy Simple Anonymous Messaging protokol verze 2 (zastaralý)"
slug: "samv2"
aliases:
  - "/cs/docs/api/samv2"
  - "/cs/docs/api/samv2/"
  - "/cs/samv2"
  - "/cs/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Varování - Zastaralé - Nepodporované - Použijte [SAMv3](/docs/api/samv3)

Níže je specifikována verze 2 jednoduchého klientského protokolu pro interakci s I2P.

SAM V2 byl představen ve vydání I2P 0.6.1.31. Významné rozdíly oproti SAM V1 jsou označeny "\*\*\*". Alternativy: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Změny ve verzi 2

SAM V2 bylo představeno ve verzi I2P 0.6.1.31. Oproti verzi 1 poskytuje SAM v2 způsob správy několika socketů na stejné I2P destinaci *paralelně*, tj. klient nemusí čekat na úspěšné odeslání dat na jednom socketu před odesláním dat na jiném socketu. Všechna data procházejí stejným socketem klient\<--\>SAM. Pro více socketů viz [SAM V3](/docs/api/samv3).

### Změny v I2P 0.9.14

Hlášená verze zůstává "2.0".

- DEST GENERATE nyní podporuje parametr SIGNATURE_TYPE.
- Parametr MIN v HELLO VERSION je nyní volitelný.
- Parametry MIN a MAX v HELLO VERSION nyní podporují jednociferné verze jako "3".

## Protokol verze 2

Klientská aplikace komunikuje s SAM bridge, který zajišťuje veškerou I2P funkcionalnost (pomocí streaming lib pro virtuální streamy, nebo I2CP přímo pro asynchronní zprávy).

Veškerá komunikace mezi klientem a SAM bridge je nešifrovaná a neautentizovaná přes jediný TCP socket. Přístup k SAM bridge by měl být chráněn pomocí firewallů nebo jiných prostředků (možná může mít bridge ACL seznamy pro IP adresy, od kterých přijímá připojení).

Všechny tyto SAM zprávy se posílají na jediném řádku v prostém ASCII, ukončené znakem nového řádku (\\n). Formátování zobrazené níže je pouze pro čitelnost, a zatímco první dvě slova v každé zprávě musí zůstat ve svém specifickém pořadí, pořadí párů klíč=hodnota se může měnit (např. "ONE TWO A=B C=D" nebo "ONE TWO C=D A=B" jsou obě dokonale platné konstrukce). Navíc je protokol citlivý na velikost písmen.

SAM zprávy jsou interpretovány v UTF-8. Páry klíč=hodnota musí být odděleny jednou mezerou. Hodnoty mohou být uzavřeny v dvojitých uvozovkách, pokud obsahují mezery, např. klíč="dlouhý text hodnoty". Neexistuje žádný mechanismus escapování.

Komunikace může mít tři odlišné formy:

- [Virtuální proudy](/docs/api/streaming)
- [Datagramy s možností odpovědi](/docs/specs/datagrams#repliable) (zprávy s polem FROM)
- [Anonymní datagramy](/docs/specs/datagrams#raw) (surové anonymní zprávy)

## SAM Connection Handshake

Žádná SAM komunikace nemůže probíhat, dokud se klient a most nedohodnou na verzi protokolu, což se děje tak, že klient pošle HELLO a most odpoví HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
a

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
Od verze I2P 0.9.14 je parametr MIN volitelný. Parametr MAX musí být poskytnut a musí být větší nebo roven "2" a menší než "3" pro použití verze 2.

Hodnota RESULT může být jedna z následujících:

- `OK`
- `NOVERSION`

## SAM Sessions

SAM session je vytvořena klientem otevřením socketu k SAM bridge, provedením handshaku a odesláním zprávy SESSION CREATE, a session se ukončí při odpojení socketu.

Každá I2P Destination může být použita pouze pro jednu SAM relaci současně a může používat pouze jednu z těchto forem (zprávy přijaté prostřednictvím jiných forem jsou zahozeny).

Zpráva SESSION CREATE odeslaná klientem na bridge je následující:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION specifikuje, jaká destinace by měla být použita pro odesílání a přijímání zpráv/proudů. Je-li zadán $name, SAM bridge prohledá své vlastní lokální úložiště (soubor sam.keys) pro přidruženou destinaci (a soukromý klíč). Pokud neexistuje žádné přidružení odpovídající tomuto názvu, vytvoří nové. Je-li destinace specifikována jako TRANSIENT, vždy vytvoří novou.

Všimněte si, že DESTINATION je identifikátor, *ne* data kódovaná v Base 64. Pro specifikaci Destination musíte použít [SAM V3](/docs/api/samv3).

DIRECTION lze specifikovat pouze pro STREAM relace, čímž se bridge instruuje, že klient bude buď vytvářet nebo přijímat streamy, nebo oboje. Pokud není specifikováno, předpokládá se BOTH. Pokus o vytvoření odchozího streamu při DIRECTION=RECEIVE by měl vyústit v chybu a příchozí streamy při DIRECTION=CREATE budou ignorovány.

Další zadané možnosti by měly být předány do konfigurace I2P relace, pokud nejsou interpretovány SAM mostem (např. "tunnels.depthInbound=0"). Tyto možnosti jsou dokumentovány níže.

SAM bridge by měl být již nakonfigurován s informací o tom, přes který router má komunikovat přes I2P (ačkoli v případě potřeby může existovat způsob, jak toto nastavení přepsat, např. i2cp.tcp.host=localhost a i2cp.tcp.port=7654).

Po obdržení zprávy vytvoření relace odpoví SAM bridge zprávou o stavu relace následovně:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
Hodnota RESULT může být jedna z následujících:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Pokud není v pořádku, MESSAGE by měla obsahovat lidsky čitelné informace o tom, proč nemohla být relace vytvořena.

Všimněte si, že se nevydává žádné varování, pokud není $name nalezen a místo toho se vytvoří přechodný cíl. Všimněte si, že skutečný přechodný base 64 cíl není uveden v odpovědi; je to $name nebo TRANSIENT jak bylo zadáno v SESSION CREATE. Pokud potřebujete tyto funkce, musíte použít [SAM V3](/docs/api/samv3).

## SAM Virtual Streams

Virtuální proudy jsou garantovány k spolehlivému odeslání ve správném pořadí, s oznámením o selhání a úspěchu, jakmile je k dispozici.

Po navázání relace s STYLE=STREAM mohou jak klient, tak SAM bridge asynchronně posílat různé zprávy tam a zpět pro správu streamů, jak je uvedeno níže:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Toto vytvoří nové virtuální spojení z lokální destinace k zadanému peeru a označí jej unikátním ID platným v rámci relace. Unikátní ID je ASCII celé číslo v desítkové soustavě od 1 do (2^31-1).

$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

SAM bridge na toto odpoví zprávou o stavu streamu:

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

Pokud je RESULT OK, zadaná destinace je dostupná a autorizovala spojení; pokud nebylo spojení možné (timeout, atd.), RESULT bude obsahovat příslušnou chybovou hodnotu (doprovázenu volitelnou MESSAGE čitelnou pro člověka).

Na straně příjemce SAM bridge jednoduše upozorní klienta následovně:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Toto říká klientovi, že daná destinace s ním vytvořila virtuální spojení. Následující datový proud bude označen daným jedinečným ID, což je ASCII base 10 celé číslo od -1 do -(2^31-1).

$destination je base 64 kódování [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

Když chce klient poslat data přes virtuální spojení, postupuje následovně:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Toto požádá SAM bridge o přidání zadaných dat do bufferu odesílaného k protějšku přes virtuální spojení. Velikost odesílaných dat $numBytes udává, kolik 8bitových bajtů je zahrnuto za novým řádkem, což může být 1 až 32768 (32KB).

**\*\*\* SAM bridge okamžitě odpovídá:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** kde $bufferState může být:

- `BUFFER_FULL` - Buffer SAM obsahuje 32 nebo více KB dat k odeslání a následující požadavky SEND selžou
- `READY` - Buffer SAM není plný a další požadavek SEND bude úspěšný

**\*\*\*** a $result je jeden z:

- `OK` - data byla úspěšně uložena do bufferu
- `FAILED` - buffer byl plný, žádná data nebyla uložena do bufferu

**\*\*\*** Pokud SAM bridge odpověděl s BUFFER_FULL, pošle další zprávu, jakmile bude jeho buffer opět dostupný:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** Když je výsledek OK, SAM bridge se pak bude snažit doručit zprávu co nejrychleji a nejefektivněji, možná spojí více SEND zpráv dohromady. Pokud dojde k chybě při doručování dat nebo pokud vzdálená strana uzavře spojení, SAM bridge to oznámí klientovi:

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

Pokud bylo spojení čistě ukončeno druhou stranou, $result je nastaven na OK. Pokud $result není OK, MESSAGE může obsahovat popisnou zprávu, jako je "peer unreachable", atd. Kdykoli chce klient uzavřít spojení, pošle SAM bridge zprávu o ukončení:

```
STREAM CLOSE
       ID=$id
```
Bridge pak vyčistí co potřebuje a zahodí toto ID - žádné další zprávy na něm již nemohou být odesílány nebo přijímány.

Pro druhou stranu komunikace, kdykoli peer odešle nějaká data a jsou dostupná pro klienta, SAM bridge je okamžitě doručí:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** S SAM verzí 2.0 však musí klient nejprve říct SAM bridge, kolik příchozích dat je povoleno pro celou relaci, odesláním zprávy:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** kde $limit může být:

- `NONE` - SAM bridge bude pokračovat v naslouchání a doručování příchozích dat (stejné chování jako ve verzi 1.0)
- celé číslo (menší než 2^64) - počet přijatých bytů, po kterých SAM bridge přestane naslouchat na příchozím streamu. Kdykoli je klient připraven přijmout více bytů ze streamu, musí znovu poslat takovou zprávu s větším $limit.

**\*\*\*** Klient musí odesílat takové STREAM RECEIVE zprávy poté, co bylo navázáno spojení s protějškem, tj. poté, co klient obdržel "STREAM CONNECTED" nebo "STREAM STATUS RESULT=OK" ze SAM bridge.

Všechny streamy jsou implicitně uzavřeny ukončením spojení mezi SAM bridge a klientem.

## SAM Repliable Datagrams

Ačkoli I2P inherentně neobsahuje FROM adresu, pro snadnější použití je poskytována dodatečná vrstva jako repliable datagramy - neuspořádané a nespolehlivé zprávy o velikosti až 31744 bajtů, které obsahují FROM adresu (zbývá až 1KB pro hlavičkový materiál). Tato FROM adresa je interně autentizována SAMem (využívá podpisový klíč destinace k ověření zdroje) a zahrnuje prevenci opakování.

Minimální velikost je 1. Pro nejlepší spolehlivost doručení je doporučená maximální velikost přibližně 11 KB.

Po navázání SAM relace s STYLE=DATAGRAM může klient odeslat SAM bridge:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Když datagram dorazí, bridge ho doručí klientovi prostřednictvím:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více base 64 znaků (387 nebo více bytů v binárním formátu), v závislosti na typu podpisu.

SAM bridge nikdy nevystavuje klientovi autentizační hlavičky nebo jiná pole, pouze data, která poskytl odesílatel. Toto pokračuje až do uzavření relace (když klient ukončí spojení).

## SAM anonymní datagramy

Díky maximálnímu využití šířky pásma I2P umožňuje SAM klientům odesílat a přijímat anonymní datagramy, přičemž autentizaci a informace o odpovědi nechává na samotných klientech. Tyto datagramy jsou nespolehlivé a neuspořádané a mohou mít až 32768 bajtů.

Minimální velikost je 1. Pro nejlepší spolehlivost doručování je doporučená maximální velikost přibližně 11 KB.

Po navázání SAM session s STYLE=RAW může klient poslat SAM bridge:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

Když dorazí nezpracovaný datagram, bridge jej doručí klientovi prostřednictvím:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funkcionalita SAM Utility

Následující zpráva může být použita klientem k dotazování SAM bridge na překlad názvů:

```
NAMING LOOKUP
       NAME=$name
```
na které se odpovídá pomocí

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

Pokud NAME=ME, pak odpověď bude obsahovat cíl používaný aktuální relací (užitečné pokud používáte TRANSIENT cíl). Pokud $result není OK, MESSAGE může obsahovat popisnou zprávu, jako například "bad format", atd.

$destination je base 64 reprezentace [Destination](/docs/specs/common-structures#type_Destination), která má 516 nebo více base 64 znaků (387 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

Veřejné a soukromé base64 klíče lze vygenerovat pomocí následující zprávy:

```
DEST GENERATE
```
na kterou je odpovězeno pomocí

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Od verze I2P 0.9.14 je podporován volitelný parametr SIGNATURE_TYPE. Hodnota SIGNATURE_TYPE může být jakýkoliv název (např. ECDSA_SHA256_P256, nerozlišuje velká a malá písmena) nebo číslo (např. 1), které je podporováno [Key Certificates](/docs/specs/common-structures#type_Certificate). Výchozí je DSA_SHA1.

$destination je base 64 [Destination](/docs/specs/common-structures#type_Destination), což je 516 nebo více base 64 znaků (387 nebo více bytů v binární podobě), v závislosti na typu podpisu.

$privkey je base 64 kódování zřetězení [Destination](/docs/specs/common-structures#type_Destination) následovaného [Private Key](/docs/specs/common-structures#type_PrivateKey) následovaným [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), což je 884 nebo více base 64 znaků (663 nebo více bajtů v binární podobě), v závislosti na typu podpisu.

## Hodnoty RESULT

Toto jsou hodnoty, které může obsahovat pole RESULT, s jejich významem:

| Hodnota | Význam |
|---------|--------|
| `OK` | Operace byla úspěšně dokončena |
| `CANT_REACH_PEER` | Protějšek existuje, ale není dosažitelný |
| `DUPLICATED_DEST` | Zadaná destinace je již používána |
| `I2P_ERROR` | Obecná I2P chyba (např. odpojení I2CP apod.) |
| `INVALID_KEY` | Zadaný klíč není platný (špatný formát apod.) |
| `KEY_NOT_FOUND` | Jmenný systém nedokáže rozložit zadané jméno |
| `PEER_NOT_FOUND` | Protějšek nelze nalézt v síti |
| `TIMEOUT` | Vypršel časový limit při čekání na událost (např. odpověď protějška) |
## Možnosti tunnel, I2CP a streamování

Tyto možnosti mohou být předány jako páry název=hodnota na konci řádku SAM SESSION CREATE.

Všechny relace mohou zahrnovat [I2CP možnosti jako jsou délky tunelů](/docs/protocol/i2cp#options). STREAM relace mohou zahrnovat [možnosti Streaming lib](/docs/api/streaming#options). Podívejte se na tyto reference pro názvy možností a výchozí hodnoty.

## Poznámky k Base 64

Kódování Base 64 musí používat standardní I2P Base 64 abecedu "A-Z, a-z, 0-9, -, ~".

## Implementace klientských knihoven

Klientské knihovny jsou dostupné pro C, C++, C#, Perl a Python. Tyto se nacházejí v adresáři apps/sam/ v balíčku zdrojových kódů I2P. Některé mohou být starší a nebyly aktualizovány pro podporu SAMv2.

## Výchozí nastavení SAM

Výchozí SAM port je 7656. SAM není ve výchozím nastavení povolen v I2P Router; musí být spuštěn ručně nebo nakonfigurován pro automatické spuštění na stránce konfigurace klientů v router konzoli nebo v souboru clients.config.
