---
title: "Desenvolvendo aplicações focadas em privacidade com Python e I2P"
date: 2018-10-23
author: "villain"
description: "Conceitos básicos do desenvolvimento de aplicações para I2P com Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) fornece uma estrutura para o desenvolvimento de aplicações com foco em privacidade. É uma rede virtual que funciona sobre a Internet comum, na qual hosts podem trocar dados sem revelar seus endereços IP "reais". As conexões dentro da rede I2P são estabelecidas entre endereços virtuais chamados *I2P destinations* (destinos do I2P). É possível ter quantos destinos forem necessários e até usar um novo destino para cada conexão. Eles não revelam nenhuma informação sobre o endereço IP real para a outra parte.

Este artigo descreve os conceitos básicos que é preciso conhecer ao desenvolver aplicações I2P. Exemplos de código são escritos em Python utilizando o framework assíncrono integrado asyncio.

## Habilitando a SAM API e instalando o i2plib

I2P fornece várias APIs diferentes para aplicações cliente. Aplicações cliente-servidor comuns podem usar I2PTunnel, proxies HTTP e Socks; aplicações Java geralmente usam I2CP. Para desenvolver com outras linguagens, como Python, a melhor opção é [SAM](/docs/api/samv3/). SAM vem desativado por padrão na implementação original do cliente Java, então precisamos ativá-lo. Vá para a Router Console, página "I2P internals" -> "Clients". Marque "Run at Startup" e pressione "Start", depois "Save Client Configuration".

![Ativar SAM API](https://geti2p.net/images/enable-sam.jpeg)

[Implementação em C++ do i2pd](https://i2pd.website) possui o SAM habilitado por padrão.

Desenvolvi uma biblioteca Python útil para a SAM API chamada [i2plib](https://github.com/l-n-s/i2plib). Você pode instalá-la com o pip ou baixar manualmente o código-fonte do GitHub.

```bash
pip install i2plib
```
Esta biblioteca funciona com o [framework assíncrono asyncio](https://docs.python.org/3/library/asyncio.html) integrado ao Python, portanto, observe que os exemplos de código são retirados de funções assíncronas (corrotinas) que estão em execução dentro do loop de eventos. Exemplos adicionais de uso do i2plib podem ser encontrados no [repositório de código-fonte](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## I2P Destination e criação de sessão

O destino do I2P é literalmente um conjunto de chaves de criptografia e de assinatura digital. As chaves públicas desse conjunto são publicadas na rede I2P e são usadas para estabelecer conexões em vez de endereços IP.

É assim que se cria [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
O endereço base32 é um hash usado por outros pares para descobrir o seu Destination (destino no I2P) completo na rede. Se planeja usar esse Destination como um endereço permanente no seu programa, salve os dados binários de *dest.private_key.data* em um arquivo local.

Agora você pode criar uma sessão SAM, o que literalmente significa tornar a Destination online no I2P:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Nota importante: A Destination (Destino no I2P) permanecerá online enquanto o socket de *session_writer* permanecer aberto. Se desejar desativar, você pode chamar *session_writer.close()*.

## Estabelecendo conexões de saída

Agora que a Destination (identificador de destino no I2P) está online, você pode usá-la para se conectar a outros pares. Por exemplo, é assim que você se conecta a "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", envia uma requisição HTTP GET e lê a resposta (é o servidor web "i2p-projekt.i2p"):

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
## Aceitando conexões de entrada

Embora estabelecer conexões de saída seja trivial, ao aceitar conexões há um detalhe importante. Após a conexão de um novo cliente, a API SAM envia para o socket uma string ASCII contendo o Destination (destino no I2P) do cliente codificado em base64. Como o Destination e os dados podem vir em um único bloco, você deve estar ciente disso.

É assim que é um servidor PING-PONG simples. Ele aceita uma conexão de entrada, salva o Destino do cliente na variável *remote_destination* e envia de volta a string "PONG":

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
## Mais informações

Este artigo descreve o uso de um protocolo de streaming semelhante ao TCP. A SAM API também fornece um protocolo semelhante ao UDP para enviar e receber datagramas. Esse recurso será adicionado ao i2plib posteriormente.

Estas são apenas informações básicas, mas são suficientes para iniciar o seu próprio projeto com o uso do I2P. A Internet Invisível é uma ótima ferramenta para desenvolver todos os tipos de aplicações voltadas para a privacidade. Não há restrições de design impostas pela rede; essas aplicações podem ser cliente-servidor, assim como P2P.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
