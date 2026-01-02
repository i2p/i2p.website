---
title: "Protokol Garlic Farm"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Otevřený"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Přehled

Toto je specifikace pro wire protokol Garlic Farm, založeného na JRaft, jeho kódu "exts" pro implementaci přes TCP a jeho aplikaci "dmprinter" [JRAFT](https://github.com/datatechnology/jraft). JRaft je implementace Raft protokolu [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

Nepodařilo se nám najít žádnou implementaci s dokumentovaným wire protokolem. Nicméně, implementace JRaft je dost jednoduchá na to, abychom mohli prozkoumat kód a následně dokumentovat jeho protokol. Tento návrh je výsledkem tohoto úsilí.

Toto bude backend pro koordinaci routerů, které publikují záznamy v Meta LeaseSet. Viz návrh 123.


## Cíle

- Malá velikost kódu
- Založeno na stávající implementaci
- Žádné serializované Java objekty nebo jakékoliv specifické Java funkce nebo kódování
- Jakékoliv zavádění je mimo rozsah. Předpokládá se, že alespoň jeden další server je pevně zakódován, nebo konfigurován mimo tento protokol.
- Podpora jak případů použití mimo i v rámci I2P.


## Návrh

Raft protokol není konkrétní protokol; definuje pouze stavový stroj. Proto dokumentujeme konkrétní protokol JRaft a zakládáme na něm náš protokol. K protokolu JRaft nedochází k žádným změnám kromě přidání autentizačního handshake.

Raft volí Leader, jehož úkolem je publikovat log. Log obsahuje Raft konfigurační data a Aplikační data. Aplikační data obsahují status každého Routeru Serveru a Destinaci pro Meta LS2 cluster. Servery používají společný algoritmus k určení publikátora a obsahu Meta LS2. Publikátorem Meta LS2 není nutně Raft Leader.


## Specifikace

Wire protokol je přes SSL sokety nebo ne-SSL I2P sokety. I2P sokety jsou proxy-ovány skrze HTTP Proxy. Neexistuje podpora pro clearnet ne-SSL sokety.

### Handshake a autentizace

Nedefinováno v JRaft.

Cíle:

- Uživatel/heslo autentizační metoda
- Verze identifikátor
- Identifikátor clusteru
- Rozšiřitelné
- Jednoduchost proxyingu při použití pro I2P sokety
- Nepřímo vystavovat server jako Garlic Farm server
- Jednoduchý protokol tak, aby nebyla nutná plná implementace webového serveru
- Kompatibilní s běžnými standardy, aby implementace mohly použít standardní knihovny, pokud je to žádoucí

Použijeme handshake podobné websocketu [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) a HTTP Digest autentizaci [RFC-2617](https://tools.ietf.org/html/rfc2617). RFC 2617 Basic autentizace není podporována. Při proxyingu skrze HTTP proxy, komunikujte s proxy podle specifikace v [RFC-2616](https://tools.ietf.org/html/rfc2616).

Přihlašovací údaje
``````````````````
Zda jsou uživatelská jména a hesla na clusteru nebo serveru, je závislé na implementaci.


HTTP Požadavek 1
```````````````

Vytvořitel pošle následující.

Všechny řádky jsou ukončeny CRLF, jak požaduje HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (jakékoliv jiné hlavičky jsou ignorovány)
  (prázdný řádek)

  CLUSTER je název clusteru (výchozí "farm")
  VERSION je verze Garlic Farm (aktuálně "1")
```


HTTP Odpověď 1
```````````````

Pokud cesta není správná, příjemce pošle standardní "HTTP/1.1 404 Not Found" odpověď, jak je popsáno v [RFC-2616](https://tools.ietf.org/html/rfc2616).

Pokud je cesta správná, příjemce pošle standardní "HTTP/1.1 401 Unauthorized" odpověď, obsahující WWW-Authenticate HTTP digest autentizační hlavičku, jak je v [RFC-2617](https://tools.ietf.org/html/rfc2617).

Obě strany pak uzavřou socket.


HTTP Požadavek 2
```````````````

Vytvořitel pošle následující, tak jak je uvedeno v [RFC-2617](https://tools.ietf.org/html/rfc2617) a [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Všechny řádky jsou ukončeny CRLF, jak požaduje HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (hlavičky Sec-Websocket-* pokud proxyováno)
  Authorization: (HTTP digest autentizační hlavička jak v RFC 2617)
  (jakékoliv jiné hlavičky jsou ignorovány)
  (prázdný řádek)

  CLUSTER je název clusteru (výchozí "farm")
  VERSION je verze Garlic Farm (aktuálně "1")
```


HTTP Odpověď 2
```````````````

Pokud autentizace není správná, příjemce pošle další standardní "HTTP/1.1 401 Unauthorized" odpověď, jak je uvedeno v [RFC-2617](https://tools.ietf.org/html/rfc2617).

Pokud je autentizace správná, příjemce pošle následující odpověď, jak je v [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Všechny řádky jsou ukončeny CRLF, jak požaduje HTTP.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (hlavičky Sec-Websocket-*)
  (jakékoliv jiné hlavičky jsou ignorovány)
  (prázdný řádek)
```

Po přijetí zůstane socket otevřený. Protokol Raft, jak je definováno níže, začíná na stejném socketu.


Cachování
`````````

Přihlašovací údaje musí být cachovány nejméně jednu hodinu, takže následné připojení může přejít přímo na "HTTP Požadavek 2" výše.


### Typy zpráv

Existují dva typy zpráv, požadavky a odpovědi. Požadavky mohou obsahovat Log Entries a jsou proměnlivé velikosti; odpovědi neobsahují Log Entries a jsou pevné velikosti.

Typy zpráv 1-4 jsou standardní RPC zprávy definované v Raft. To je jádro Raft protokolu.

Typy zpráv 5-15 jsou rozšířené RPC zprávy definované v JRaft, pro podporu klientů, dynamické změny serveru a efektivní synchronizaci logů.

Typy zpráv 16-17 jsou Log Compaction RPC zprávy definované v sekci 7 Raft.


| Zpráva | Číslo | Posláno kým | Posláno komu | Poznámky |
|--------|-------|-------------|--------------|----------|
| RequestVoteRequest | 1 | Kandidát | Follower | Standardní Raft RPC; nesmí obsahovat log entries |
| RequestVoteResponse | 2 | Follower | Kandidát | Standardní Raft RPC |
| AppendEntriesRequest | 3 | Lídér | Follower | Standardní Raft RPC |
| AppendEntriesResponse | 4 | Follower | Lídér / Klient | Standardní Raft RPC |
| ClientRequest | 5 | Klient | Lídér / Follower | Odpověď je AppendEntriesResponse; musí obsahovat pouze Application log entries |
| AddServerRequest | 6 | Klient | Lídér | Musí obsahovat jediné ClusterServer logové záznamy |
| AddServerResponse | 7 | Lídér | Klient | Lídér pošle také JoinClusterRequest |
| RemoveServerRequest | 8 | Follower | Lídér | Musí obsahovat jediné ClusterServer logové záznamy |
| RemoveServerResponse | 9 | Lídér | Follower | |
| SyncLogRequest | 10 | Lídér | Follower | Musí obsahovat jediný LogPack log entry |
| SyncLogResponse | 11 | Follower | Lídér | |
| JoinClusterRequest | 12 | Lídér | Nový server | Pozvánka k připojení; musí obsahovat jedinou Configuration logovou položku |
| JoinClusterResponse | 13 | Nový server | Lídér | |
| LeaveClusterRequest | 14 | Lídér | Follower | Příkaz k opuštění |
| LeaveClusterResponse | 15 | Follower | Lídér | |
| InstallSnapshotRequest | 16 | Lídér | Follower | Raft Sekce 7; Musí obsahovat jediný SnapshotSyncRequest log entry |
| InstallSnapshotResponse | 17 | Follower | Lídér | Raft Sekce 7 |


### Založení

Po HTTP handshaku je pořadí ustanovení následující:

```text
Nový server Alice          Náhodný Follower Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Pokud Bob říká, že je lídrem, pokračujte níže.
  Jinak musí Alice odpojit od Boba a připojit se k lídrovi.


  Nový server Alice          Lídér Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       NEBO InstallSnapshotRequest
  SyncLogResponse  ------->
  NEBO InstallSnapshotResponse
```

Sekvence odpojení:

```text
Follower Alice              Lídér Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Sekvence voleb:

```text
Kandidát Alice             Follower Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  Pokud Alice vyhraje volby:

  Lídér Alice               Follower Bob

  AppendEntriesRequest   ------->
  (heartbeat)
          <---------   AppendEntriesResponse
```


### Definice

- Zdroj: Identifikuje původce zprávy
- Cíl: Identifikuje příjemce zprávy
- Termíny: Viz Raft. Inicializováno na 0, zvyšuje se monotónně
- Indexy: Viz Raft. Inicializováno na 0, zvyšuje se monotónně


### Požadavky

Požadavky obsahují hlavičku a nula nebo více logových záznamů. Požadavky obsahují hlavičku s pevnou velikostí a volitelné Log Entries proměnlivé velikosti.


Hlavička požadavku
``````````````````

Hlavička požadavku má 45 bytů, jak následuje. Všechny hodnoty jsou unsigned big-endian.

```dataspec
Typ zprávy:      1 byte
  Zdroj:           ID, 4 bye integer
  Cíl:             ID, 4 byte integer
  Term:            Aktuální termín (viz poznámky), 8 byte integer
  Poslední termín Logu:    8 byte integer
  Poslední index Logu:     8 byte integer
  Commit Index:    8 byte integer
  Log entries velikost:  Celková velikost v bytech, 4 byte integer
  Log entries:     viz níže, celková délka jak je specifikována
```


#### Poznámky

V RequestVoteRequest, Term je kandidátův termín. Jinak je to aktuální termín lídra.

V AppendEntriesRequest, pokud je log entries velikost nula, tato zpráva je heartbeat (keepalive) zprávou.


Logové záznamy
`````````````

Log obsahuje nula nebo více logových záznamů. Každý logový záznam je následující. Všechny hodnoty jsou unsigned big-endian.

```dataspec
Term:           8 byte integer
  Hodnota typ:     1 byte
  Velikost záznamu:  V bytech, 4 byte integer
  Záznam:          délka jak specifikována
```


Obsah logu
``````````

Všechny hodnoty jsou unsigned big-endian.

| Typ hodnot logu | Číslo |
|-----------------|-------|
| Aplikace | 1 |
| Konfigurace | 2 |
| Clusterový server | 3 |
| LogPack | 4 |
| SnapshotSyncRequest | 5 |


#### Aplikace

Aplikační obsah je kódován UTF-8 [JSON](https://www.json.org/). Viz sekce Aplikační vrstva níže.


#### Konfigurace

To je používáno pro lídra k serializaci nové konfigurace clusteru a replikaci na peeru. Obsahuje nula nebo více konfigurací Clusterového serveru.


```dataspec
Index logu:  8 byte integer
  Poslední index Logu:  8 byte integer
  Data Clusterového serveru pro každý server:
    ID:                4 byte integer
    Délka dat Endpointu:  V bytech, 4 byte integer
    Data Endpointu:     ASCII string ve formátu "tcp://localhost:9001", délka jak specifikována
```


#### Clusterový server

Konfigurační informace pro server v clusteru. To je zahrnuto pouze ve zprávě AddServerRequest nebo RemoveServerRequest.

Když je používáno ve zprávě AddServerRequest:

```dataspec
ID:                4 byte integer
  Délka dat Endpointu:  V bytech, 4 byte integer
  Data Endpointu:     ASCII string ve formátu "tcp://localhost:9001", délka jak specifikována
```


Když je používáno ve zprávě RemoveServerRequest:

```dataspec
ID:                4 byte integer
```


#### LogPack

To je zahrnuto pouze ve zprávě SyncLogRequest.

Následující je před přenosem gzipped:


```dataspec
Délka dat indexu: V bytech, 4 byte integer
  Délka logových dat:   V bytech, 4 byte integer
  Data indexu:     8 byte pro každý index, délka jak specifikována
  Logová data:       délka jak specifikována
```


#### SnapshotSyncRequest

To je zahrnuto pouze ve zprávě InstallSnapshotRequest.

```dataspec
Poslední index logu:  8 byte integer
  Poslední termín Logu:   8 byte integer
  Délka konfiguračních dat: V bytech, 4 byte integer
  Konfigurační data:     délka jak specifikována
  Ofset:          Ofset údajů v databázi, V bytech, 8 byte integer
  Délka dat:        V bytech, 4 byte integer
  Data:            délka jak specifikována
  Je dokončeno:         1 pokud je dokončeno, 0 pokud není (1 byte)
```


### Odpovědi

Všechny odpovědi mají 26 bytů, jak následuje. Všechny hodnoty jsou unsigned big-endian.

```dataspec
Typ zprávy:   1 byte
  Zdroj:         ID, 4 byte integer
  Cíl:           Obvykle aktuální ID cíle (viz poznámky), 4 byte integer
  Term:          Aktuální termín, 8 byte integer
  Další index:     Inicializováno na poslední index logu lídra + 1, 8 byte integer
  Je přijato:    1 pokud přijato, 0 pokud ne (viz poznámky), 1 byte
```


Poznámky
````````

ID cíle je obvykle aktuální cíl pro tuto zprávu. Nicméně, pro AppendEntriesResponse, AddServerResponse, a RemoveServerResponse je to ID aktuálního lídra.

V RequestVoteResponse, Je přijato je 1 pro hlas pro kandidáta (žadatele), a 0 pro žádný hlas.


## Aplikační vrstva

Každý Server periodicky ukládá Aplikační data do logu v ClientRequest. Aplikační data obsahují status každého Routeru Serveru a Destinaci pro Meta LS2 cluster. Servery používají společný algoritmus k určení publikátora a obsahu Meta LS2. Server s "nejlepším" nedávným statusem v logu je Meta LS2 publisher. Publikátorem Meta LS2 není nutně Raft Leader.


### Obsah aplikačních dat

Aplikační obsah je kódován UTF-8 [JSON](https://www.json.org/), pro jednoduchost a rozšiřitelnost. Plná specifikace je TBD. Cílem je poskytnout dostatek dat k napsání algoritmu k určení "nejlepšího" routeru k publikování Meta LS2, a aby publisher měl dostatečné informace k zvážení Destinací v Meta LS2. Data budou obsahovat jak statistiky routeru, tak Destinace.

Data mohou volitelně obsahovat vzdálená data o zdraví ostatních serverů, a možnost získání Meta LS. Tato data nebudou podporována v první verzi.

Data mohou volitelně obsahovat informace o konfiguraci publikované administrátorským klientem. Tato data nebudou podporována v první verzi.

Pokud je uvedeno "name: value", to specifikuje klíč a hodnotu JSON mapy. Jinak je specifikace TBD.


Data clusteru (nejvyšší úroveň):

- cluster: Název Clusteru
- date: Datum těchto dat (long, ms od epochy)
- id: Raft ID (integer)

Konfigurační data (config):

- Jakékoliv konfigurační parametry

Status publikování MetaLS (meta):

- destination: MetaLS destinace, base64
- lastPublishedLS: pokud je přítomno, base64 kódování posledního publikovaného MetaLS
- lastPublishedTime: ve ms, nebo 0 pokud nikdy
- publishConfig: Status publikování config off/on/auto
- publishing: Status publikování MetaLS true/false

Data Routeru (router):

- lastPublishedRI: pokud přítomno, base64 kódování posledního publikovaného router info
- uptime: Doba běhu ve ms
- Prodleva úloh
- Průzkumné tunely
- Participující tunely
- Konfigurovaná šířka pásma
- Aktuální šířka pásma

Destinace (destinations):
List

Data destinace:

- destination: destinace, base64
- uptime: Doba běhu ve ms
- Konfigurované tunely
- Aktuální tunely
- Konfigurovaná šířka pásma
- Aktuální šířka pásma
- Konfigurované spojení
- Aktuální spojení
- Data blacklistu

Vzdálená data o smyslování routeru:

- Poslední verze RI viděná
- Čas získání LS
- Data testu spojení
- Nejbližší floodfills data profilu pro období včerejška, dneška a zítřka

Vzdálená data o smyslování destinace:

- Poslední verze LS viděná
- Čas získání LS
- Data testu spojení
- Nejbližší floodfills data profilu pro období včerejška, dneška a zítřka

Data smyslování Meta LS:

- Poslední verze viděná
- Čas získání
- Nejbližší floodfills data profilu pro období včerejška, dneška a zítřka


## Administrativní rozhraní

TBD, možná samostatný návrh. Není vyžadováno pro první vydání.

Požadavky administrativního rozhraní:

- Podpora pro více master destinací, tj. několik virtuálních clusterů (farem)
- Poskytnout kompletní přehled o stavu sdíleného clusteru - všechny statistiky publikované členy, kdo je aktuální lídr atd.
- Schopnost vynutit odstranění účastníka nebo lídra z clusteru
- Schopnost vynutit publikování metaLS (pokud je aktuální uzel publisher)
- Schopnost vyloučit heše z metaLS (pokud je aktuální uzel publisher)
- Funkce importu/exportu konfigurace pro hromadná nasazení


## Routerové rozhraní

TBD, možná samostatný návrh. i2pcontrol není vyžadován pro první vydání a podrobné změny budou zahrnuty do samostatného návrhu.

Požadavky pro Garlic Farm na API routeru (v-JVM java nebo i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // pravděpodobně ne v MVP
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // nebo podepsaný MetaLeaseSet? Kdo podepisuje?
- stopPublishingMetaLS(Hash masterHash)
- autentizace TBD?


## Odůvodnění

Atomix je příliš velký a neumožňuje přizpůsobení pro nás, abychom mohli směřovat protokol přes I2P. Také, jeho wire formát je nedokumentovaný a závisí na Java serializaci.


## Poznámky


## Problémy

- Neexistuje způsob, jak by klient mohl zjistit a připojit se k neznámému lídrovi. Bylo by to menší změna, aby Follower poslal Konfiguraci jako Log Entry v AppendEntriesResponse.


## Migrace

Žádné problémy se zpětnou kompatibilitou.


## Odkazy

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
