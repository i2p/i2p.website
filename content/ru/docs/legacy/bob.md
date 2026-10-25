---
title: "BOB - Basic Open Bridge"
description: "Устаревший API для управления назначениями"
slug: "bob"
aliases:
  - "/ru/docs/api/bob"
  - "/ru/docs/api/bob/"
  - "/ru/bob"
  - "/ru/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Предупреждение - Устарело

Не предназначен для использования новыми приложениями. BOB, как указано здесь, поддерживает только тип подписи DSA-SHA1. BOB не будет расширен для поддержки новых типов подписей или других расширенных функций. Новые приложения должны использовать [SAM V3](/docs/api/samv3).

Поддержка BOB была удалена из новых установок Java I2P начиная с версии 1.7.0 (2022-02). Она по-прежнему будет работать в Java I2P, изначально установленном как версия 1.6.1 или более ранняя, даже после обновлений, но она не поддерживается и может перестать работать в любой момент. BOB по-прежнему поддерживается i2pd по состоянию на 2025-05, но приложения всё равно должны перейти на SAMv3 по причинам, указанным выше. См. [документацию i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) для любых расширений API, задокументированного здесь, которые поддерживаются i2pd.

На данный момент большинство хороших идей из BOB были включены в SAMv3, который имеет больше функций и более широкое практическое применение. BOB может всё ещё работать на некоторых установках (см. выше), но он не получает передовых функций, доступных для SAMv3, и по сути не поддерживается, за исключением i2pd.

## Языковые библиотеки для BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Обзор

`KEYS` = пара ключей открытый+закрытый, они в формате BASE64

`KEY` = публичный ключ, также BASE64

`ERROR` как следует из названия возвращает сообщение `"ERROR "+DESCRIPTION+"\n"`, где `DESCRIPTION` — это описание того, что пошло не так.

`OK` возвращает `"OK"`, и если должны быть возвращены данные, они находятся на той же строке. `OK` означает, что команда завершена.

Строки `DATA` содержат информацию, которую вы запросили. Может быть несколько строк `DATA` на один запрос.

**ПРИМЕЧАНИЕ:** Команда help является ЕДИНСТВЕННОЙ командой, которая составляет исключение из правил... она может фактически ничего не возвращать! Это сделано намеренно, поскольку help является командой для ЧЕЛОВЕКА, а не для ПРИЛОЖЕНИЯ.

## Соединение и версия

Весь вывод статуса BOB осуществляется построчно. Строки могут завершаться \\n или \\r\\n в зависимости от системы. При подключении BOB выводит две строки:

```
BOB version
OK
```
Текущая версия: 00.00.10

Обратите внимание, что предыдущие версии использовали шестнадцатеричные цифры в верхнем регистре и не соответствовали стандартам версионирования I2P. Рекомендуется, чтобы последующие версии использовали только цифры 0-9.

### История версий

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Команды

**ОБРАТИТЕ ВНИМАНИЕ:** Для получения АКТУАЛЬНОЙ информации о командах ИСПОЛЬЗУЙТЕ встроенную команду помощи. Просто подключитесь через telnet к localhost 2827 и введите help, чтобы получить полную документацию по каждой команде.

Команды никогда не устаревают и не изменяются, однако время от времени добавляются новые команды.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
После настройки все TCP сокеты могут и будут блокироваться по мере необходимости, и не потребуется никаких дополнительных сообщений в/из командного канала. Это позволяет router контролировать поток без переполнения памяти (OOM), как это происходит с SAM, когда он задыхается, пытаясь протолкнуть множество потоков через один сокет - это не масштабируется при большом количестве соединений!

Что также приятно в этом конкретном интерфейсе, так это то, что написать что-либо для взаимодействия с ним намного проще, чем с SAM. После настройки не требуется никакой дополнительной обработки. Его конфигурация настолько проста, что для указания на какое-либо приложение можно использовать очень простые инструменты, такие как nc (netcat). Ценность заключается в том, что можно планировать время включения и выключения приложения, не изменяя само приложение и даже не останавливая его. Вместо этого вы буквально можете "отключить" destination и "подключить" его снова. Пока при запуске моста используются те же IP/порт адреса и ключи destination, обычное TCP-приложение не будет возражать и не заметит этого. Оно просто будет обмануто — destinations недоступны, и ничего не поступает.

## Примеры

В следующем примере мы настроим очень простое локальное loopback-соединение с двумя destination. Destination "mouth" будет службой CHARGEN из демона INET superserver. Destination "ear" будет локальным портом, к которому вы можете подключиться через telnet и наблюдать за красивым потоком ASCII-символов.

### Пример диалога сессии

Простой telnet 127.0.0.1 2827 работает.

- A = Приложение
- C = Ответ команды BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**ЗАПОМНИТЕ ВЫШЕУКАЗАННЫЙ КЛЮЧ НАЗНАЧЕНИЯ, У ВАС ОН БУДЕТ ДРУГОЙ!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
На данном этапе ошибки не было, destination с псевдонимом "mouth" настроен. Когда вы соединяетесь с предоставленным destination, вы фактически подключаетесь к службе `CHARGEN` на `19/TCP`.

Теперь перейдем ко второй половине, чтобы мы могли фактически связаться с этим назначением.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Теперь все, что нам нужно сделать, это подключиться по telnet к 127.0.0.1, порт 37337, отправить ключ назначения или адрес хоста из адресной книги, с которым мы хотим связаться. В данном случае мы хотим связаться с "mouth", все что нам нужно - это вставить ключ и все заработает.

**ПРИМЕЧАНИЕ:** Команда "quit" в командном канале НЕ отключает туннели, как в SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
После нескольких виртуальных миль этого потока данных нажмите `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Вот что произошло...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Вы также можете подключаться к I2P-сайтам!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Довольно круто, не так ли? Попробуйте другие известные I2P SITES, если хотите, несуществующие и т.д., чтобы понять, какой вывод ожидать в различных ситуациях. В основном рекомендуется игнорировать любые сообщения об ошибках. Они будут бессмысленны для приложения и представлены только для отладки человеком.

### Очистка

Теперь давайте освободим наши точки назначения, поскольку мы закончили с ними работу.

Сначала давайте посмотрим, какие псевдонимы назначений у нас есть.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Хорошо, вот они. Сначала давайте удалим "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Теперь удалим "ear", обратите внимание, что это происходит, когда вы набираете слишком быстро, и показывает, как выглядят типичные сообщения об ОШИБКАХ.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Тихий режим

Я не буду показывать пример принимающей стороны моста, поскольку это очень просто. Для неё есть две возможные настройки, которые переключаются командой "quiet".

По умолчанию режим НЕ тихий, и первые данные, поступающие в ваш слушающий сокет, — это destination, который устанавливает соединение. Это одна строка, состоящая из BASE64 адреса, за которым следует символ новой строки. Всё, что идёт после этого, предназначено для фактического использования приложением.

В тихом режиме представьте это как обычное интернет-соединение. Никаких дополнительных данных вообще не поступает. Это точно так же, как если бы вы были подключены к обычному интернету напрямую. Этот режим обеспечивает форму прозрачности, очень похожую на ту, что доступна на страницах настроек tunnel в консоли router, так что вы можете использовать BOB для направления destination на веб-сервер, например, и вам не придется вообще модифицировать веб-сервер.

## Преимущества BOB

Преимущество использования BOB для этого заключается в том, что обсуждалось ранее. Вы можете планировать случайное время работы приложения, перенаправлять на другую машину и т.д. Одним из применений может быть попытка запутать угадывание доступности router-to-destination. Вы можете останавливать и запускать destination с помощью совершенно другого процесса, создавая случайные периоды включения и выключения сервисов. Таким образом, вы будете только останавливать возможность связаться с таким сервисом, не беспокоясь о его завершении работы и перезапуске. Вы можете перенаправлять и указывать на другую машину в вашей локальной сети во время обновлений, или указывать на набор резервных машин в зависимости от того, что работает, и так далее. Только ваше воображение ограничивает то, что вы можете делать с BOB.
