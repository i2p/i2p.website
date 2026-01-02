---
title: "Desarrollo de aplicaciones conscientes de la privacidad con Python e I2P"
date: 2018-10-23
author: "villain"
description: "Conceptos básicos del desarrollo de aplicaciones de I2P con Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Proyecto de Internet Invisible](https://geti2p.net/) (I2P) proporciona un marco para desarrollar aplicaciones respetuosas de la privacidad. Es una red virtual que funciona sobre Internet convencional, en la que los anfitriones pueden intercambiar datos sin revelar sus direcciones IP "reales". Las conexiones dentro de la red I2P se establecen entre direcciones virtuales llamadas *destinos de I2P*. Es posible tener tantos destinos como se necesiten, incluso usar un destino nuevo para cada conexión; no revelan ninguna información sobre la dirección IP real a la otra parte.

Este artículo describe los conceptos básicos que se deben conocer al desarrollar aplicaciones de I2P. Los ejemplos de código están escritos en Python utilizando el framework asíncrono incorporado asyncio.

## Habilitación de la API SAM e instalación de i2plib

I2P proporciona muchas APIs diferentes para las aplicaciones cliente. Las aplicaciones cliente-servidor convencionales pueden usar I2PTunnel, proxies HTTP y SOCKS; las aplicaciones Java suelen usar I2CP. Para desarrollar con otros lenguajes, como Python, la mejor opción es [SAM](/docs/api/samv3/). SAM está deshabilitado de forma predeterminada en la implementación original del cliente Java, por lo que debemos habilitarlo. Vaya a Router Console, página "I2P internals" -> "Clients". Marque "Run at Startup" y presione "Start", luego "Save Client Configuration".

![Habilitar API SAM](https://geti2p.net/images/enable-sam.jpeg)

La [implementación en C++ i2pd](https://i2pd.website) tiene SAM habilitado por defecto.

He desarrollado una útil biblioteca de Python para la API SAM llamada [i2plib](https://github.com/l-n-s/i2plib). Puedes instalarla con pip o descargar manualmente el código fuente desde GitHub.

```bash
pip install i2plib
```
Esta biblioteca funciona con el [framework asíncrono asyncio](https://docs.python.org/3/library/asyncio.html) integrado en Python, así que ten en cuenta que los ejemplos de código se toman de funciones async (coroutines) que se ejecutan dentro del bucle de eventos. Se pueden encontrar ejemplos adicionales del uso de i2plib en el [repositorio de código fuente](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## I2P Destination (destino) y creación de sesión

I2P destination (destino de I2P) es literalmente un conjunto de claves de cifrado y de firma criptográfica. Las claves públicas de este conjunto se publican en la red de I2P y se usan para establecer conexiones en lugar de direcciones IP.

Así es como se crea [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
La dirección base32 es un hash que otros pares utilizan para descubrir tu Destination (destino en I2P) completo en la red. Si planeas usar este Destination como una dirección permanente en tu programa, guarda los datos binarios de *dest.private_key.data* en un archivo local.

Ahora puedes crear una sesión SAM, que literalmente significa poner la Destination en línea en I2P:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Nota importante: El Destino permanecerá en línea mientras el socket *session_writer* se mantenga abierto. Si desea desactivarlo, puede llamar a *session_writer.close()*."""

## Establecer conexiones salientes

Ahora que el Destino está en línea, puedes usarlo para conectarte con otros pares. Por ejemplo, así es como te conectas a "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", envías una solicitud HTTP GET y lees la respuesta (es el servidor web de "i2p-projekt.i2p"):

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
## Aceptación de conexiones entrantes

Aunque establecer conexiones salientes es trivial, cuando se aceptan conexiones hay un detalle importante. Después de que se conecta un nuevo cliente, SAM API envía al socket una cadena ASCII con la Destination del cliente codificada en base64. Dado que la Destination y los datos pueden llegar en un solo bloque, debe tenerlo en cuenta.

Así se ve un servidor PING-PONG simple. Acepta una conexión entrante, guarda la Destination (Destino de I2P) del cliente en la variable *remote_destination* y devuelve la cadena "PONG":

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
## Más información

Este artículo describe el uso de un protocolo de Streaming similar a TCP. SAM API también proporciona un protocolo similar a UDP para enviar y recibir datagramas. Esta funcionalidad se añadirá a i2plib más adelante.

Esto es solo información básica, pero es suficiente para comenzar tu propio proyecto usando I2P. Internet Invisible es una gran herramienta para desarrollar todo tipo de aplicaciones centradas en la privacidad. La red no impone restricciones de diseño; esas aplicaciones pueden ser tanto cliente-servidor como P2P.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
