---
title: "Форматы файлов GeoIP"
description: "Спецификации устаревшего формата файлов GeoIP для поиска страны по IP-адресу"
slug: "geoip"
aliases:
  - "/ru/geoip"
  - "/ru/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Обзор

> **ПРИМЕЧАНИЕ: УСТАРЕЛО** - Мы теперь поддерживаем три формата, в порядке предпочтения: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) входит в комплект всех установок, кроме пакетов Debian и Android > - Maxmind geoip1 (GeoIP.dat) в пакете Debian geoip-database > - Формат IPv4 Tor (geoip.txt) и пользовательский формат IPv6 (geoipv6.dat.gz), документированные ниже, все еще поддерживаются, но не используются.

Эта страница описывает формат различных файлов GeoIP, используемых router'ом для определения страны по IP-адресу.

## Формат названий стран (countries.txt)

Этот формат легко создается из файлов данных, доступных из многих публичных источников. Например:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Спецификации формата:**

- Кодировка UTF-8
- `#` в первой колонке обозначает строку комментария
- Строки записей имеют формат `КодСтраны,НазваниеСтраны`
- КодСтраны — это двухбуквенный код ISO в верхнем регистре
- НазваниеСтраны на английском языке

## Формат IPv4 (geoip.txt)

Этот формат заимствован из Tor и легко генерируется из файлов данных, доступных из многих публичных источников. Например:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Спецификации формата:**

- Кодировка ASCII
- `#` в первом столбце обозначает строку комментария
- Строки записей имеют формат `FromIP,ToIP,CountryCode`
- FromIP и ToIP представляют собой беззнаковые целые числа 4-байтового IP
- CountryCode — это двухбуквенный ISO-код страны в верхнем регистре
- Строки записей должны быть отсортированы по числовому значению FromIP

## Формат IPv6 (geoipv6.dat.gz)

Это сжатый двоичный формат, разработанный для I2P. Файл сжат gzip. Несжатый формат:

```text
Bytes 0-9: Magic number "I2PGeoIPv6"
Bytes 10-11: Version (0x0001)
Bytes 12-15 Options (0x00000000) (future use)
Bytes 16-23: Creation date (ms since 1970-01-01)
Bytes 24-xx: Optional comment (UTF-8) terminated by zero byte
Bytes xx-255: null padding
Bytes 256-: 18 byte records:
    8 byte from (/64)
    8 byte to (/64)
    2 byte ISO country code LOWER case (ASCII)
```
**Примечания:**

- Данные должны быть отсортированы (SIGNED long дополнение до двойки), без перекрытий. Таким образом, порядок: `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- Класс `GeoIPv6.java` содержит программу для генерации данного формата из публичных источников, таких как данные Maxmind GeoLite.
- Поиск IPv6 GeoIP поддерживается начиная с версии 0.9.8.
