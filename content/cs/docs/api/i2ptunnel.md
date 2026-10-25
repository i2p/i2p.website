---
title: "I2PTunnel"
description: "Nástroj pro komunikaci s I2P a poskytování služeb na I2P"
slug: "i2ptunnel"
aliases:
  - "/cs/i2ptunnel"
  - "/cs/i2ptunnel/"
  - "/cs/i2ptunnel_migration"
  - "/cs/i2ptunnel_migration/"
  - "/cs/i2ptunnel_services"
  - "/cs/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Přehled {#overview}

I2PTunnel je nástroj pro propojení se službami na I2P a jejich poskytování. Cíl I2PTunnel může být definován pomocí [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), nebo plného 516-bajtového destination klíče. Vytvořený I2PTunnel bude dostupný na vašem klientském počítači jako localhost:port. Pokud chcete poskytovat službu na síti I2P, jednoduše vytvoříte I2PTunnel na příslušnou ip_address:port. Pro službu bude vygenerován odpovídající 516-bajtový destination klíč a stane se dostupnou v celém I2P. Webové rozhraní pro správu I2PTunnel je dostupné na [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Výchozí služby {#default-services}

### Server Tunnely {#default-server-tunnels}

- **I2P Webserver** - Tunnel směřující na Jetty webserver běžící na [localhost:7658](http://localhost:7658) pro pohodlný a rychlý hosting na I2P.
  Kořenový adresář dokumentů je:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, což se rozbalí na: `C:\Users\**uživatelské_jméno**\AppData\Local\I2P\I2P Site\docroot`

### Klientské tunely {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - HTTP proxy používané pro anonymní prohlížení I2P a běžného internetu prostřednictvím I2P. Prohlížení internetu přes I2P využívá náhodné proxy specifikované volbou "Outproxies:".
- **Irc2P** - *localhost:6668* - IRC tunnel na výchozí anonymní IRC síť, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - SSH přístup k projektovému Git repozitáři
- **smtp.postman.i2p** - *localhost:7659* - SMTP služba poskytovaná postmanem na hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - Doprovodná POP služba postmana na hq.postman.i2p

## Konfigurace {#configuration}

[Konfigurace I2PTunnel](/docs/specs/configuration)

## Klientské režimy {#client-modes}

### Standardní {#client-modes-standard}

Otevře místní TCP port, který se připojuje ke službě (jako HTTP, FTP nebo SMTP) na cíli uvnitř I2P. Tunnel je směrován na náhodný host ze seznamu cílů oddělených čárkami (", ").

### HTTP {#client-mode-http}

HTTP-client tunnel. Tunnel se připojuje k cíli určenému URL adresou v HTTP požadavku. Podporuje proxying na internet, pokud je poskytnut outproxy. Odstraňuje z HTTP spojení následující hlavičky:

- **Accept\*:** (nezahrnuje "Accept" a "Accept-Encoding") protože se značně liší mezi prohlížeči a mohou být použity jako identifikátor.
- **Referer:**
- **Via:**
- **From:**

HTTP klientská proxy poskytuje řadu služeb pro ochranu uživatele a pro lepší uživatelský zážitek.

**Zpracování hlaviček požadavku:** - Odstranění hlaviček problematických z hlediska soukromí - Směrování na místní nebo vzdálený outproxy - Výběr outproxy, ukládání do mezipaměti a sledování dostupnosti - Vyhledávání cílů podle názvů hostitelů - Nahrazení hlavičky hostitele za b32 - Přidání hlavičky pro označení podpory transparentní dekomprese - Vynucení connection: close - Podpora proxy v souladu s RFC - Zpracování a odstranění hop-by-hop hlaviček v souladu s RFC - Volitelné digest a základní ověření uživatelského jména/hesla - Volitelné outproxy digest a základní ověření uživatelského jména/hesla - Ukládání všech hlaviček do vyrovnávací paměti před předáním pro vyšší efektivitu - Odkazy na jump servery - Zpracování jump odpovědí a formulářů (address helper) - Zpracování zaslepených b32 a formulářů pro přihlašovací údaje - Podpora standardních HTTP a HTTPS (CONNECT) požadavků

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

**Zpracování hlaviček odpovědi:** - Kontrola, zda dekomprimovat odpověď - Vynucení connection: close - RFC-kompatibilní zpracování a odstranění hop-by-hop hlaviček - Ukládání všech hlaviček do vyrovnávací paměti před předáním pro efektivitu

- **Content-Encoding:** x-i2p-gzip

**Odpovědi HTTP chyb:** - Pro mnoho běžných i méně běžných chyb, aby uživatel věděl, co se stalo - Více než 20 unikátních přeložených, stylovaných a formátovaných chybových stránek pro různé chyby - Interní webový server pro poskytování formulářů, CSS, obrázků a chyb

- X-Accept-Encoding není standardní header
- Neprovádí dechunk/chunk per-hop; předává chunking end-to-end
- Předává Transfer-Encoding header end-to-end
- Používá Content-Encoding, ne Transfer-Encoding, k určení per-hop kódování
- Zakazuje x-i2p gzipping když je nastaven Content-Encoding (ale to pravděpodobně nechceme dělat tak jako tak)
- Serverová strana gzipuje server-sent chunking, místo aby prováděla dechunk-gzip-rechunk a dechunk-gunzip-rechunk
- Gzipovaný obsah není následně chunkován. RFC 2616 vyžaduje, aby všechno Transfer-Encoding kromě "identity" bylo chunkováno.
- Protože není chunking venku (po) gzip, je těžší najít konec dat, což ztěžuje jakoukoliv implementaci keepalive.
- RFC 2616 říká, že Content-Length nesmí být odeslán pokud je přítomen Transfer-Encoding, ale my to děláme. Spec říká ignorovat Content-Length pokud je přítomen Transfer-Encoding, což prohlížeče dělají, takže to pro nás funguje.

#### Transparentní komprese odpovědí {#transparent-response-compression}

Komprese odpovědi i2ptunnel je požadována pomocí HTTP hlavičky:

- *Outproxy:* **User-Agent:** Používá user agent z nedávného vydání Firefox na Windows
- *Interní I2P použití:* **User-Agent:** MYOB/6.66 (AN/ON)

Serverová strana odstraní tuto hop-by-hop hlavičku před odesláním požadavku na webový server. Složitá hlavička se všemi q hodnotami není nutná; servery by měly jen hledat "x-i2p-gzip" kdekoli v hlavičce.

Serverová strana určuje, zda komprimovat odpověď na základě hlaviček přijatých od webserveru, včetně Content-Type, Content-Length a Content-Encoding, aby posoudila, zda je odpověď komprimovatelná a stojí za dodatečný výpočetní výkon procesoru. Pokud serverová strana komprimuje odpověď, přidá následující HTTP hlavičku:

- **Content-Encoding:** x-i2p-gzip

Pokud je tato hlavička přítomna v odpovědi, HTTP klientský proxy ji transparentně dekomprimuje. Klientská strana odstraní tuto hlavička a provede gunzip před odesláním odpovědi do prohlížeče. Všimněte si, že stále máme základní gzip kompresi na vrstvě I2CP, která je stále efektivní, pokud odpověď není komprimována na HTTP vrstvě.

Tento návrh a současná implementace porušují RFC 2616 v několika ohledech:

- X-Accept-Encoding není standardní hlavička
- Neprovádí dechunk/chunk na každém hopu; chunking prochází end-to-end
- Předává hlavičku Transfer-Encoding end-to-end
- K určení kódování na každém hopu používá Content-Encoding, nikoli Transfer-Encoding
- Zakazuje x-i2p gzipování, když je nastaven Content-Encoding (ale to pravděpodobně stejně nechceme dělat)
- Serverová strana gzipuje chunkování odesílané serverem, místo aby prováděla dechunk-gzip-rechunk a dechunk-gunzip-rechunk
- Gzipovaný obsah se následně nechunkuje. RFC 2616 vyžaduje, aby všechny Transfer-Encoding kromě "identity" byly chunkované.
- Protože mimo (po) gzip neexistuje žádné chunkování, je obtížnější najít konec dat, což ztěžuje jakoukoli implementaci keepalive.
- RFC 2616 říká, že Content-Length nesmí být odeslán, pokud je přítomno Transfer-Encoding, ale my ho posíláme. Specifikace říká, že pokud je přítomno Transfer-Encoding, má se Content-Length ignorovat, což prohlížeče dělají, takže nám to funguje.

Změny pro implementaci hop-by-hop komprese odpovídající standardům způsobem zpětně kompatibilním jsou tématem pro další studium. Jakákoliv změna dechunk-gzip-rechunk by vyžadovala nový typ kódování, možná x-i2p-gzchunked. To by bylo identické s Transfer-Encoding: gzip, ale muselo by být signalizováno odlišně z důvodů kompatibility. Jakákoliv změna by vyžadovala formální návrh.

#### Transparentní komprese požadavků {#transparent-request-compression}

Není podporováno, ačkoli POST by z toho měl prospěch. Všimněte si, že stále máme základní gzip kompresi na vrstvě I2CP.

#### Persistentnost {#persistence}

Klientské a serverové proxy v současnosti nepodporují RFC 2616 HTTP perzistentní sockety na žádném ze tří skoků (socket prohlížeče, I2P socket, socket serveru). Hlavičky Connection: close jsou vkládány na každém skoku. Změny pro implementaci perzistence jsou v současnosti zkoumány. Tyto změny by měly být kompatibilní se standardy a zpětně kompatibilní a nevyžadovaly by formální návrh.

#### Pipelining {#pipelining}

Klientské a serverové proxy v současnosti nepodporují HTTP pipelining podle RFC 2616 a nejsou žádné plány na jeho implementaci. Moderní prohlížeče nepodporují pipelining přes proxy, protože většina proxy jej nedokáže správně implementovat.

#### Kompatibilita {#compatibility}

Implementace proxy musí správně fungovat s jinými implementacemi na druhé straně. Klientské proxy by měly fungovat bez HTTP-aware serverové proxy (tj. standardní tunnel) na straně serveru. Ne všechny implementace podporují x-i2p-gzip.

#### User Agent {#user-agent}

V závislosti na tom, zda tunnel používá outproxy nebo ne, připojí následující User-Agent:

- *Outproxy:* **User-Agent:** Používá user agent z nedávného vydání Firefoxu na Windows
- *Interní použití I2P:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC klient {#client-mode-irc}

Vytvoří připojení k náhodnému IRC serveru zadanému seznamem cílů oddělených čárkami (", "). Z důvodů anonymity jsou povoleny pouze IRC příkazy z whitelist.

Následující seznam povolených příkazů je určen pro příkazy příchozí z IRC serveru do IRC klienta.

**Seznam povolených:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

- AUTHENTICATE
- CAP
- ERROR
- H
- JOIN
- KICK
- MODE
- NICK
- PART
- PING
- PROTOCTL
- QUIT
- TOPIC
- WALLOPS

Existuje také seznam povolených příkazů odchozích z IRC klienta na IRC server. Je poměrně rozsáhlý kvůli počtu IRC administrativních příkazů. Podrobnosti naleznete ve zdrojovém kódu IRCFilter.java.

Odchozí filtr také upravuje následující příkazy pro odstranění identifikačních informací: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

- NOTICE
- PART
- PING
- PRIVMSG
- QUIT
- USER

### SOCKS 4/4a/5 {#client-mode-socks}

Umožňuje používat I2P router jako SOCKS proxy.

### SOCKS IRC {#client-mode-socks-irc}

Umožňuje používání I2P routeru jako SOCKS proxy s whitelistem příkazů specifikovaným klientským režimem [IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Vytvoří HTTP tunnel a použije HTTP metodu požadavku "CONNECT" k vybudování TCP tunnelu, který se obvykle používá pro SSL a HTTPS.

### Streamr {#client-mode-streamr}

Vytváří UDP-server připojený k Streamr klientskému I2PTunnel. Streamr klientský tunnel se přihlásí k odběru od streamr serverového tunnelu.

![Streamr diagram](/images/I2PTunnel-streamr.png)

## Serverové režimy {#server-modes}

### Standardní {#server-mode-standard}

Vytvoří cíl na místní ip:port s otevřeným TCP portem.

### HTTP {#server-mode-http}

Vytvoří cíl k lokálnímu HTTP serveru ip:port. Podporuje gzip pro požadavky s Accept-encoding: x-i2p-gzip, odpovídá s Content-encoding: x-i2p-gzip na takový požadavek.

HTTP server proxy poskytuje řadu služeb, které usnadňují a zabezpečují hostování webových stránek a poskytují lepší uživatelský zážitek na straně klienta.

**Zpracování hlaviček požadavku:** - Validace hlaviček - Ochrana proti falšování hlaviček - Kontroly velikosti hlaviček - Volitelné odmítání inproxy a user-agent - Přidání X-I2P hlaviček, aby webserver věděl, odkud požadavek přišel - Nahrazení Host hlavičky pro usnadnění webserver vhosts - Vynucení connection: close - RFC-kompatibilní zpracování a odstranění hop-by-hop hlaviček - Ukládání všech hlaviček do vyrovnávací paměti před předáním kvůli efektivitě

- Validace hlaviček
- Ochrana proti podvržení hlaviček
- Kontrola velikosti hlaviček
- Volitelné odmítání inproxy a user-agent
- Přidání hlaviček X-I2P, aby webserver věděl, odkud požadavek přišel
- Nahrazení hlavičky Host pro snazší vhosts na webserveru
- Vynucení connection: close
- Zpracování a odstraňování hop-by-hop hlaviček v souladu s RFC
- Bufferování všech hlaviček před předáním pro vyšší efektivitu

**Ochrana proti DDoS:** - Omezování POST požadavků - Ochrana proti timeoutům a slowloris útokům - Dodatečné omezování probíhá ve streaming pro všechny typy tunelů

- Omezování POST požadavků
- Timeouty a ochrana proti slowloris
- Dodatečné omezování probíhá ve streamingu pro všechny typy tunnelů

**Zpracování hlaviček odpovědi:** - Odstranění některých hlaviček problematických z hlediska soukromí - Kontrola MIME typu a dalších hlaviček pro rozhodnutí o kompresi odpovědi - Vynucení connection: close - RFC-kompatibilní zpracování a odstranění hop-by-hop hlaviček - Ukládání všech hlaviček do vyrovnávací paměti před předáním pro efektivitu

- Odstraňování některých hlaviček problematických z hlediska soukromí
- Kontrola MIME typu a dalších hlaviček, zda komprimovat odpověď
- Vynucení connection: close
- Zpracování a odstraňování hop-by-hop hlaviček v souladu s RFC
- Bufferování všech hlaviček před průchodem pro efektivitu

**HTTP chybové odpovědi:** - Pro mnoho běžných i méně běžných chyb a při omezování, aby uživatel na straně klienta věděl, co se stalo

- U mnoha běžných i méně běžných chyb a při throttlingu, aby uživatel na straně klienta věděl, co se stalo

**Transparentní komprese odpovědí:** - Webový server a/nebo vrstva I2CP mohou komprimovat, ale webový server často nekomprimuje, a je nejefektivnější komprimovat na vysoké vrstvě, i když I2CP také komprimuje. HTTP server proxy spolupracuje s klientskou proxy pro transparentní kompresi odpovědí.

- Webový server a/nebo vrstva I2CP mohou komprimovat, ale webový server to často nedělá, a je nejefektivnější komprimovat na vysoké vrstvě, i když I2CP také komprimuje. Proxy HTTP serveru spolupracuje s proxy na straně klienta na transparentní komprimaci odpovědí.

### HTTP Bidirectional {#server-mode-http-bidir}

*Zastaralé*

Funguje jak jako I2PTunnel HTTP Server, tak jako I2PTunnel HTTP klient bez možností outproxy. Příkladem aplikace by byla webová aplikace, která provádí požadavky typu klient, nebo loopback testování I2P stránky jako diagnostický nástroj.

### IRC Server {#server-mode-irc}

Vytvoří destination, která filtruje registrační sekvenci klienta a předává klíč destination klienta jako hostname IRC serveru.

### Streamr {#server-mode-streamr}

Je vytvořen UDP-klient, který se připojuje k mediálnímu serveru. UDP-klient je spojen se serverem Streamr I2PTunnel.
