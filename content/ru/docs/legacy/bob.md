---
title: "BOB – Basic Open Bridge (базовый открытый мост)"
description: "Устаревший API для управления назначениями (устарело)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Предупреждение:** BOB поддерживает только устаревший тип подписи DSA-SHA1. Java I2P перестал включать BOB в состав дистрибутива в **1.7.0 (2022-02)**; он остался только на установках, впервые развернутых в версии 1.6.1 или более ранней, а также в некоторых сборках i2pd. Новые приложения **должны** использовать [SAM v3](/docs/api/samv3/).

## Привязки для языков программирования

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Примечания к протоколу

- `KEYS` обозначает destination (адрес назначения) в base64 (открытый и закрытый ключи).  
- `KEY` — это открытый ключ в base64.  
- Ответы `ERROR` имеют вид `ERROR <description>\n`.  
- `OK` обозначает завершение команды; необязательные данные следуют в той же строке.  
- Строки `DATA` выводят дополнительные данные до финального `OK`.

Команда `help` — единственное исключение: она может ничего не возвращать, чтобы обозначить «нет такой команды».

## Баннер подключения

BOB использует строки ASCII, завершаемые символом новой строки (LF или CRLF). При подключении он отправляет:

```
BOB <version>
OK
```
Текущая версия: `00.00.10`. Ранние сборки использовали шестнадцатеричные цифры в верхнем регистре и нестандартную нумерацию.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## Основные команды

> Для получения полного описания команд подключитесь с помощью `telnet localhost 2827` и выполните `help`.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## Сводка устареваний

- BOB (устаревший интерфейс приложений I2P) не поддерживает современные типы подписей, зашифрованные LeaseSets или возможности транспортного уровня.
- API заморожен; новые команды добавляться не будут.
- Приложения, которые всё ещё полагаются на BOB, должны перейти на SAM v3 как можно скорее.
