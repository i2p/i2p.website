---
title: "I2P в Maven Central"
date: 2016-06-13
author: "str4d"
description: "Клиентские библиотеки I2P теперь доступны в Maven Central!"
categories: ["summer-dev"]
---

Мы почти на середине месяца API в рамках Summer Dev и добиваемся значительного прогресса по ряду направлений. Я рад сообщить, что первое из них готово: клиентские библиотеки I2P теперь доступны в Maven Central!

Это должно значительно упростить Java-разработчикам использование I2P в своих приложениях. Вместо того чтобы получать библиотеки из текущей установки, они могут просто добавить I2P в список зависимостей. Обновление до новых версий также станет гораздо проще.

## Как их использовать

Есть две библиотеки, о которых вам нужно знать:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Добавьте один или оба из них в список зависимостей вашего проекта — и всё готово!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Для других систем сборки см. страницы Maven Central для библиотек core и streaming.

Разработчикам под Android следует использовать I2P Android client library, которая содержит те же библиотеки, а также Android-специфические вспомогательные компоненты. В ближайшее время я обновлю её, чтобы она зависела от новых библиотек I2P, чтобы кроссплатформенные приложения могли нативно работать как с I2P Android, так и с настольным I2P.

## Get hacking!

Посмотрите наше руководство по разработке приложений, чтобы получить помощь в начале работы с этими библиотеками. Вы также можете пообщаться с нами о них в канале #i2p-dev в IRC. А если вы начнете их использовать, сообщите нам, над чем вы работаете, с хештегом #I2PSummer в Twitter!
