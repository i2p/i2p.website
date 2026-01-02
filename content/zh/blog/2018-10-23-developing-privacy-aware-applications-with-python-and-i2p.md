---
title: "使用 Python 和 I2P 开发注重隐私的应用程序"
date: 2018-10-23
author: "villain"
description: "使用 Python 进行 I2P 应用开发的基本概念"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/)（I2P）提供用于开发注重隐私的应用程序的框架。它是构建在常规互联网之上的虚拟网络，在其中，主机可以在不泄露其“真实”IP 地址的情况下交换数据。I2P 网络内部的连接是在称为*I2P destinations*（I2P 目标地址）的虚拟地址之间建立的。可以根据需要拥有任意数量的 destinations，甚至可以为每次连接使用一个新的 destination；它们不会向对端透露任何关于真实 IP 地址的信息。

本文介绍开发 I2P 应用程序时需要了解的基本概念。代码示例使用 Python 编写，并使用内置的异步框架 asyncio。

## 启用 SAM API 并安装 i2plib

I2P 为客户端应用程序提供了多种不同的 API。常规的客户端-服务器应用可以使用 I2PTunnel、HTTP 和 Socks 代理，Java 应用通常使用 I2CP。对于使用其他语言（例如 Python）进行开发，最佳选择是 [SAM](/docs/api/samv3/)。在原始的 Java 客户端实现中，默认禁用 SAM，因此需要将其启用。进入 Router Console，打开页面 "I2P internals" -> "Clients"。勾选 "Run at Startup"，点击 "Start"，然后 "Save Client Configuration"。

![启用 SAM API](https://geti2p.net/images/enable-sam.jpeg)

[C++ 实现 i2pd](https://i2pd.website) 默认启用 SAM。

我开发了一个用于 SAM API 的实用 Python 库，名为 [i2plib](https://github.com/l-n-s/i2plib)。你可以通过 pip 安装，或从 GitHub 手动下载源代码。

```bash
pip install i2plib
```
该库可与 Python 内置的[异步框架 asyncio](https://docs.python.org/3/library/asyncio.html)配合使用，因此请注意，代码示例来自在事件循环中运行的异步函数（协程）。关于 i2plib 用法的更多示例可在[源代码仓库](https://github.com/l-n-s/i2plib/tree/master/docs/examples)中找到。

## I2P 目标地址与会话创建

“I2P destination（I2P 目标标识）”从字面上说就是一组加密密钥和数字签名密钥。该集合中的公钥会发布到 I2P 网络，并用于代替 IP 地址建立连接。

以下是创建 [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination) 的方法：

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
base32 地址是一个哈希，用于让其他对等节点在网络中发现你的完整 Destination（I2P 目的地）。如果你计划在程序中将此 Destination 用作永久地址，请将 *dest.private_key.data* 中的二进制数据保存到本地文件。

现在你可以创建一个 SAM 会话，这从字面上说就是让 Destination 在 I2P 中上线：

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
重要说明：只要 *session_writer* 套接字保持打开，Destination（目的地标识）将保持在线。如果希望将其关闭，可以调用 *session_writer.close()*。

## 发起出站连接

现在，当该 Destination（目标）在线时，你可以使用它连接到其他对等节点。例如，可以按如下方式连接到 "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"，发送 HTTP GET 请求并读取响应（它是 "i2p-projekt.i2p" 的 Web 服务器）：

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
## 接受入站连接

虽然建立出站连接很简单，但在接受连接时有一个重要细节。新的客户端连接建立后，SAM API 会向套接字发送一段包含客户端 Destination（目标地址）的 base64 编码 ASCII 字符串。由于 Destination 和数据可能在同一个数据块中到达，你需要注意这一点。

一个简单的 PING-PONG 服务器大致如下所示。它接受入站连接，将客户端的 Destination（目标标识）保存到 *remote_destination* 变量中，并回送字符串 "PONG"：

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
## 更多信息

本文介绍一种类似 TCP 的流式协议的用法。SAM API 也提供了类似 UDP 的协议来发送和接收数据报。该功能将稍后添加到 i2plib 中。

这只是一些基础信息，但已经足以让你使用 I2P 开始自己的项目。Invisible Internet（不可见互联网）是用于开发各类注重隐私的应用程序的强大工具。网络本身不对设计施加任何限制，这些应用既可以采用客户端-服务器架构，也可以是 P2P。

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
