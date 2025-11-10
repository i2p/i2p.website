---
title: "Как стать волонтёром, помогая с bootstrap (начальной инициализацией) I2P-Bote"
date: 2019-05-20
author: "idk"
description: "Помогите с начальной инициализацией I2P-Bote!"
categories: ["development"]
---

Простой способ помочь людям общаться приватно — запустить узел I2P-Bote, который новые пользователи I2P-Bote смогут использовать для bootstrap (первичной инициализации) собственных узлов I2P-Bote. К сожалению, до сих пор процесс настройки bootstrap-узла I2P-Bote был куда более запутанным, чем следовало бы. На самом деле всё предельно просто!

**Что такое I2P-bote?**

I2P-bote — это система приватного обмена сообщениями, построенная на i2p, с дополнительными функциями, которые ещё больше затрудняют выявление сведений о передаваемых сообщениях. Благодаря этому её можно использовать для безопасной передачи приватных сообщений при высокой задержке и без зависимости от централизованного ретранслятора для отправки сообщений, когда отправитель отключается от сети. Это отличается от почти всех других популярных систем приватного обмена сообщениями, которые либо требуют одновременного нахождения обеих сторон онлайн, либо полагаются на частично доверенный сервис, передающий сообщения от имени отправителей, отключившихся от сети.

или, ELI5 (простыми словами): Им пользуются примерно как электронной почтой, но при этом отсутствуют характерные для электронной почты проблемы с конфиденциальностью.

**Шаг первый: установите I2P-Bote**

I2P-Bote — это плагин для I2P, и его установка очень проста. Оригинальные инструкции доступны на [eepSite bote, bote.i2p](http://bote.i2p/install/), но если вы хотите прочитать их в clearnet (обычном интернете), эти инструкции любезно предоставлены bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Шаг второй: Получите адрес в кодировке base64 вашего узла I2P-Bote**

На этом этапе можно застрять, но не переживайте. Хотя инструкции найти непросто, на деле всё довольно просто, и в вашем распоряжении есть несколько инструментов и вариантов, в зависимости от ваших обстоятельств. Для тех, кто хочет добровольно помогать в работе bootstrap nodes (узлы начальной инициализации), лучший способ — извлечь необходимую информацию из файла закрытого ключа, используемого bote tunnel.

**Где находятся ключи?**

I2P-Bote сохраняет свои ключи назначения в текстовом файле, который в Debian находится по адресу `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. В системах, отличных от Debian, где i2p установлен пользователем, ключ будет в `$HOME/.i2p/i2pbote/local_dest.key`, а в Windows файл будет находиться в `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Метод A: Преобразовать ключ в открытом виде в адрес назначения в base64**

Чтобы преобразовать ключ в виде открытого текста в base64 destination (адрес назначения в I2P), нужно взять ключ и отделить от него только часть destination. Чтобы сделать это правильно, необходимо выполнить следующие шаги:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Существует ряд приложений и скриптов, которые выполнят эти шаги за вас. Вот некоторые из них, но это далеко не полный список:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Эти возможности также доступны в ряде библиотек для разработки приложений I2P.

**Быстрый способ:**

Поскольку локальное назначение вашего узла Bote — это назначение DSA, быстрее всего просто усечь файл local_dest.key до первых 516 байт. Чтобы сделать это проще, выполните эту команду при работе I2P-Bote с I2P в Debian:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Или, если I2P установлен под вашим пользователем:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Метод B: Выполнить поиск**

Если это кажется слишком трудоёмким, вы можете узнать base64-назначение своего подключения Bote, сделав запрос его base32-адреса любым из доступных способов для поиска base32-адреса. base32-адрес вашего узла Bote доступен на странице "Connection" в приложении плагина Bote по адресу [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Шаг третий: Свяжитесь с нами!**

**Обновите файл built-in-peers.txt, добавив свой новый узел**

Теперь, когда у вас есть корректный destination (адрес в I2P) для вашего узла I2P-Bote, последний шаг — добавить себя в список пиров по умолчанию для [I2P-Bote здесь](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) здесь. Вы можете сделать это, сделав форк репозитория, добавив себя в список с вашим именем, закомментированным, и вашим 516-символьным destination прямо под ним, вот так:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
и отправив pull request. Вот и всё, так что помогайте поддерживать I2P живым, децентрализованным и надёжным.
