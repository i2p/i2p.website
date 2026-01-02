---
title: "Типы MIME I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Обзор

Определите типы MIME для общих форматов файлов I2P.
Включите определения в пакеты Debian.
Предоставьте обработчик для типа .su3 и, возможно, других.


## Мотивация

Чтобы упростить повторное содержание и установку плагинов при загрузке через браузер,
нам нужен тип MIME и обработчик для файлов .su3.

Тем более, изучив, как писать файл определения MIME,
следуя стандарту freedesktop.org, мы можем добавить определения для других
общих типов файлов I2P.
Хотя это менее полезно для файлов, которые обычно не загружаются, таких как
база данных адресной книги (hostsdb.blockfile), эти определения позволят
файлам быть лучше идентифицированными и снабженными иконками при использовании
графического просмотрщика каталогов, такого как "nautilus" на Ubuntu.

Стандартизируя типы MIME, каждая реализация роутера может писать обработчики
по мере необходимости, и файл определения MIME может быть использован всеми
реализациями.


## Дизайн

Напишите XML-файл источника, следуя стандарту freedesktop.org, и включите его
в пакеты Debian. Файл называется "debian/(package).sharedmimeinfo".

Все типы MIME I2P будут начинаться с "application/x-i2p-", за исключением jrobin rrd.

Обработчики для этих типов MIME специфичны для приложений и не будут
определены здесь.

Мы также включим определения в Jetty и добавим их в
программу повторного содержания или инструкцию.


## Спецификация

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Примечания

Не все перечисленные выше форматы файлов используются нереализациями на Java;
некоторые могут даже быть плохо определены. Однако, документирование их здесь
может способствовать консистентности между реализациями в будущем.

Некоторые суффиксы файлов, такие как ".config", ".dat" и ".info", могут
пересекаться с другими типами MIME. Их можно различать с помощью
дополнительных данных, таких как полное имя файла, шаблон имени файла или
магические числа.
Смотрите пример в черновике файла i2p.sharedmimeinfo в теме zzz.i2p.

Важными являются типы .su3, и эти типы имеют как уникальные
суффиксы, так и надежные определения магических чисел.


## Миграция

Неприменимо.
