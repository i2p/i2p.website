---
title: "Entwicklung datenschutzbewusster Anwendungen mit Python und I2P"
date: 2018-10-23
author: "villain"
description: "Grundkonzepte der I2P-Anwendungsentwicklung mit Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) stellt ein Framework zur Entwicklung datenschutzfreundlicher Anwendungen bereit. Es ist ein virtuelles Netzwerk, das auf dem regulären Internet aufsetzt, in dem Hosts Daten austauschen können, ohne ihre „echten“ IP-Adressen preiszugeben. Verbindungen innerhalb des I2P-Netzwerks werden zwischen virtuellen Adressen aufgebaut, die als *I2P destinations* (virtuelle I2P-Zieladressen) bezeichnet werden. Es ist möglich, so viele solcher Zieladressen zu nutzen, wie benötigt werden, man kann sogar für jede Verbindung eine neue verwenden; sie geben der Gegenseite keinerlei Informationen über die reale IP-Adresse preis.

Dieser Artikel beschreibt grundlegende Konzepte, die man bei der Entwicklung von I2P-Anwendungen kennen sollte. Codebeispiele sind in Python geschrieben und verwenden das integrierte asynchrone Framework asyncio.

## Aktivieren der SAM-API und Installation von i2plib

I2P stellt viele verschiedene APIs für Client-Anwendungen zur Verfügung. Normale Client-Server-Anwendungen können I2PTunnel sowie HTTP- und Socks-Proxys verwenden, Java-Anwendungen verwenden in der Regel I2CP. Für die Entwicklung mit anderen Sprachen, etwa Python, ist [SAM](/docs/api/samv3/) die beste Option. SAM ist in der ursprünglichen Java-Client-Implementierung standardmäßig deaktiviert, daher müssen wir es aktivieren. Öffnen Sie in der Router Console die Seite "I2P internals" -> "Clients". Aktivieren Sie "Run at Startup" und klicken Sie auf "Start", anschließend auf "Save Client Configuration".

![SAM API aktivieren](https://geti2p.net/images/enable-sam.jpeg)

[C++-Implementierung i2pd](https://i2pd.website) hat SAM standardmäßig aktiviert.

Ich habe eine praktische Python-Bibliothek für die SAM API namens [i2plib](https://github.com/l-n-s/i2plib) entwickelt. Sie können sie mit pip installieren oder den Quellcode manuell von GitHub herunterladen.

```bash
pip install i2plib
```
Diese Bibliothek arbeitet mit dem in Python integrierten [asynchronen Framework asyncio](https://docs.python.org/3/library/asyncio.html), daher beachten Sie bitte, dass die Codebeispiele aus asynchronen Funktionen (Koroutinen) stammen, die innerhalb der Event Loop (Ereignisschleife) ausgeführt werden. Weitere Beispiele für die Nutzung von i2plib finden Sie im [Quellcode-Repository](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## I2P Destination (Zieladresse) und Sitzungserstellung

Eine I2P Destination (Zieladresse) ist buchstäblich ein Satz von Verschlüsselungs- und kryptografischen Signaturschlüsseln. Öffentliche Schlüssel aus diesem Satz werden im I2P-Netzwerk veröffentlicht und ersetzen IP-Adressen beim Aufbau von Verbindungen.

So erstellen Sie eine [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
Die base32-Adresse ist ein Hash, der von anderen Peers verwendet wird, um Ihre vollständige Destination (Zieladresse) im Netzwerk zu ermitteln. Wenn Sie planen, diese Destination als permanente Adresse in Ihrem Programm zu verwenden, speichern Sie die Binärdaten aus *dest.private_key.data* in einer lokalen Datei.

Jetzt können Sie eine SAM-Sitzung erstellen, was wörtlich bedeutet, die Destination (I2P-Identität) in I2P online zu stellen:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Wichtiger Hinweis: Die Destination bleibt online, solange der *session_writer*-Socket geöffnet bleibt. Wenn Sie sie abschalten möchten, können Sie *session_writer.close()* aufrufen.

## Herstellen ausgehender Verbindungen

Nun, da die Destination (Zieladresse) online ist, können Sie sie verwenden, um sich mit anderen Peers zu verbinden. Zum Beispiel verbinden Sie sich so mit "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", senden eine HTTP-GET-Anfrage und lesen die Antwort (das ist der Webserver von "i2p-projekt.i2p"):

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
## Eingehende Verbindungen akzeptieren

Während das Herstellen ausgehender Verbindungen trivial ist, gibt es beim Annehmen von Verbindungen ein wichtiges Detail. Nachdem sich ein neuer Client verbunden hat, sendet die SAM API eine ASCII-Zeichenkette mit der Base64-kodierten Destination des Clients an den Socket. Da Destination und Daten in einem einzigen Datenblock ankommen können, sollten Sie sich dessen bewusst sein.

So sieht ein einfacher PING-PONG-Server aus. Er akzeptiert eine eingehende Verbindung, speichert die Destination des Clients in der Variable *remote_destination* und sendet die Zeichenkette "PONG" zurück:

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
## Weitere Informationen

Dieser Artikel beschreibt die Verwendung eines TCP-ähnlichen Streaming-Protokolls. Die SAM API stellt außerdem ein UDP-ähnliches Protokoll zum Senden und Empfangen von Datagrammen bereit. Diese Funktion wird später zu i2plib hinzugefügt.

Dies sind nur grundlegende Informationen, aber sie reichen aus, um ein eigenes Projekt mit I2P zu starten. Das Invisible Internet ist ein großartiges Werkzeug, um alle Arten von datenschutzfreundlichen Anwendungen zu entwickeln. Es gibt keine Design-Einschränkungen durch das Netzwerk; diese Anwendungen können sowohl Client-Server als auch P2P sein.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
