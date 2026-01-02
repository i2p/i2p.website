---
title: "Разработка приложений, ориентированных на конфиденциальность, с использованием Python и I2P"
date: 2018-10-23
author: "villain"
description: "Основы разработки приложений для I2P на Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Проект Невидимый Интернет](https://geti2p.net/) (I2P) предоставляет платформу для разработки ориентированных на конфиденциальность приложений. Это виртуальная сеть, работающая поверх обычного Интернета, в которой узлы могут обмениваться данными, не раскрывая свои "реальные" IP-адреса. Соединения внутри сети I2P устанавливаются между виртуальными адресами, называемыми *I2P destinations* (назначениями I2P). Можно иметь столько destinations, сколько требуется, и даже использовать отдельное destination для каждого соединения; они не раскрывают другой стороне никакой информации о реальном IP-адресе.

Эта статья описывает основные понятия, которые необходимо знать при разработке приложений I2P. Примеры кода написаны на Python с использованием стандартной асинхронной библиотеки asyncio.

## Включение SAM API и установка i2plib

I2P предоставляет множество различных API для клиентских приложений. Обычные клиент-серверные приложения могут использовать I2PTunnel, HTTP- и Socks-прокси; приложения на Java обычно используют I2CP. Для разработки на других языках, например Python, наилучшим вариантом является [SAM](/docs/api/samv3/). SAM по умолчанию отключён в оригинальной реализации Java-клиента, поэтому его нужно включить. Перейдите в Router Console, страница "I2P internals" -> "Clients". Отметьте "Run at Startup" и нажмите "Start", затем "Save Client Configuration".

![Включить SAM API](https://geti2p.net/images/enable-sam.jpeg)

[C++-реализация i2pd](https://i2pd.website) имеет SAM включённым по умолчанию.

Я разработал удобную библиотеку Python для SAM API под названием [i2plib](https://github.com/l-n-s/i2plib). Вы можете установить её через pip или вручную скачать исходный код с GitHub.

```bash
pip install i2plib
```
Эта библиотека работает со встроенным в Python [асинхронным фреймворком asyncio](https://docs.python.org/3/library/asyncio.html), поэтому обратите внимание, что примеры кода взяты из асинхронных функций (корутин), которые выполняются внутри цикла событий. Дополнительные примеры использования i2plib можно найти в [репозитории исходного кода](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## I2P Destination (адрес назначения) и создание сеанса

I2P destination (адрес назначения в I2P) — в буквальном смысле это набор ключей шифрования и криптографической подписи. Открытые ключи из этого набора публикуются в сети I2P и используются для установления соединений вместо IP-адресов.

Вот как создать [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
Адрес base32 — это хеш, который используется другими пирами для обнаружения вашей полной Destination (идентификатор назначения) в сети. Если вы планируете использовать эту Destination как постоянный адрес в своей программе, сохраните бинарные данные из *dest.private_key.data* в локальный файл.

Теперь вы можете создать сеанс SAM, что буквально означает сделать Destination онлайн в I2P:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Важное замечание: Destination будет оставаться онлайн, пока сокет *session_writer* остается открытым. Если вы хотите отключить Destination, вызовите *session_writer.close()*."""

## Установление исходящих соединений

Теперь, когда Destination (назначение) в сети, вы можете использовать его для подключения к другим узлам. Например, вот как подключиться к "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", отправить HTTP-запрос GET и прочитать ответ (это веб-сервер "i2p-projekt.i2p"):

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
## Приём входящих соединений

Хотя установление исходящих соединений тривиально, при принятии входящих соединений есть один важный нюанс. После подключения нового клиента SAM API отправляет в сокет ASCII-строку с base64-кодированным Destination (адрес назначения) клиента. Поскольку Destination и данные могут прийти в одном фрагменте, следует иметь это в виду.

Вот как выглядит простой сервер PING-PONG. Он принимает входящее соединение, сохраняет Destination (идентификатор адреса в I2P) клиента в переменную *remote_destination* и отправляет обратно строку "PONG":

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
## Подробнее

В этой статье описывается использование протокола Streaming (потоковой передачи), подобного TCP. SAM API также предоставляет протокол, подобный UDP, для отправки и получения датаграмм. Эта возможность будет добавлена в i2plib позже.

Это лишь базовая информация, но её достаточно, чтобы начать собственный проект с использованием I2P. «Невидимый Интернет» — отличный инструмент для разработки всевозможных приложений, ориентированных на приватность. Сеть не накладывает ограничений на архитектуру: такие приложения могут быть как клиент–серверными, так и P2P.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
