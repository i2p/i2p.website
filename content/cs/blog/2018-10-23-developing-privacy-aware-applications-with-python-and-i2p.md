---
title: "Vývoj aplikací dbajících na ochranu soukromí s využitím Pythonu a I2P"
date: 2018-10-23
author: "villain"
description: "Základní principy vývoje aplikací pro I2P v Pythonu"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) poskytuje rámec pro vývoj aplikací respektujících soukromí. Je to virtuální síť fungující nad běžným internetem, ve které mohou uzly vyměňovat data, aniž by odhalovaly své "skutečné" IP adresy. Spojení uvnitř sítě I2P se navazují mezi virtuálními adresami nazývanými *I2P destinations*. Je možné mít tolik destinations, kolik je potřeba, dokonce používat pro každé spojení novou destination; druhé straně neprozrazují žádné informace o skutečné IP adrese.

Tento článek popisuje základní pojmy, které je třeba znát při vývoji aplikací pro I2P. Ukázky kódu jsou napsány v Pythonu s využitím vestavěného asynchronního frameworku asyncio.

## Povolení SAM API a instalace i2plib

I2P poskytuje klientským aplikacím mnoho různých rozhraní API. Běžné klient-server aplikace mohou používat I2PTunnel, HTTP a SOCKS proxy, aplikace v jazyce Java obvykle používají I2CP. Pro vývoj v jiných jazycích, jako je Python, je nejlepší možností [SAM](/docs/api/samv3/). SAM je ve výchozím nastavení v původní implementaci Java klienta zakázán, takže jej musíme povolit. Přejděte do Router Console, na stránku "I2P internals" -> "Clients". Zaškrtněte "Run at Startup" a klikněte na "Start", poté "Save Client Configuration".

![Povolit SAM API](https://geti2p.net/images/enable-sam.jpeg)

[C++ implementace i2pd](https://i2pd.website) má ve výchozím nastavení povolený SAM.

Vyvinul jsem užitečnou knihovnu v Pythonu pro SAM API nazvanou [i2plib](https://github.com/l-n-s/i2plib). Nainstalovat ji můžete pomocí nástroje pip nebo si ručně stáhnout zdrojový kód z GitHubu.

```bash
pip install i2plib
```
Tato knihovna pracuje s vestavěným [asynchronním frameworkem asyncio](https://docs.python.org/3/library/asyncio.html) v Pythonu, proto mějte na paměti, že ukázky kódu pocházejí z asynchronních funkcí (korutin), které běží uvnitř smyčky událostí. Další příklady použití i2plib najdete v [repozitáři se zdrojovým kódem](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## Vytvoření I2P Destination (cílové identity) a relace

I2P destination (I2P destinace) je doslova sada šifrovacích klíčů a klíčů pro kryptografický podpis. Veřejné klíče z této sady jsou publikovány do sítě I2P a používají se k navazování spojení místo IP adres.

Takto vytvoříte [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
Adresa ve formátu base32 je hash, který ostatní uzly používají k nalezení vaší úplné Destination (identifikátoru cíle v I2P) v síti. Pokud plánujete tuto Destination používat jako trvalou adresu ve svém programu, uložte binární data z *dest.private_key.data* do lokálního souboru.

Nyní můžete vytvořit relaci SAM, což doslova znamená uvést Destination (cílovou adresu) online v I2P:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Důležitá poznámka: Destination zůstane online, dokud zůstane socket *session_writer* otevřený. Pokud chcete Destination vypnout, můžete zavolat *session_writer.close()*.

## Navazování odchozích spojení

Nyní, když je Destination (cíl v I2P) online, můžete ji použít k připojení k ostatním peerům. Například takto se připojíte k "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", odešlete požadavek HTTP GET a přečtete odpověď (jde o webový server "i2p-projekt.i2p"):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## Přijímání příchozích spojení

Zatímco navazování odchozích spojení je triviální, při přijímání příchozích spojení je tu jeden důležitý detail. Po připojení nového klienta pošle SAM API do socketu ASCII řetězec s Destination klienta v kódování Base64. Protože Destination a data mohou přijít v jednom bloku, měli byste s tím počítat.

Takto vypadá jednoduchý PING-PONG server. Přijme příchozí spojení, uloží klientovu Destination do proměnné *remote_destination* a odešle zpět řetězec "PONG":

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## Další informace

Tento článek popisuje použití streamovacího protokolu podobného TCP. SAM API také poskytuje protokol podobný UDP pro odesílání a přijímání datagramů. Tato funkce bude do i2plib přidána později.

Jde jen o základní informace, ale stačí k tomu, abyste mohli začít svůj vlastní projekt s využitím I2P. Invisible Internet (Neviditelný internet) je skvělý nástroj pro vývoj nejrůznějších aplikací zaměřených na ochranu soukromí. Síť neklade na návrh žádná omezení; tyto aplikace mohou být jak klient–server, tak i P2P.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
