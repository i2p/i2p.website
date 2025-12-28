---
title: "Форматы файлов GeoIP"
description: "Спецификации устаревшего формата файла GeoIP для определения страны по IP-адресу"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Обзор

**ПРИМЕЧАНИЕ: УСТАРЕЛО** - Теперь мы поддерживаем три формата, в порядке предпочтения:

- Maxmind geoip2 (GeoLite2-Country.mmdb) поставляется в комплекте со всеми установками, за исключением пакетов Debian и Android
- Maxmind geoip1 (GeoIP.dat) в пакете Debian geoip-database
- Формат Tor для IPv4 (geoip.txt) и пользовательский формат для IPv6 (geoipv6.dat.gz), описанные ниже, по-прежнему поддерживаются, но не используются.

Эта страница описывает формат различных файлов GeoIP, используемых router для определения страны по IP-адресу.

## Формат названия страны (countries.txt)

Этот формат легко можно сгенерировать из файлов данных, доступных из многочисленных открытых источников. Например:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Спецификации формата:**

- Кодировка — UTF-8
- '#' в первом столбце обозначает строку комментария
- Строки записей имеют вид CountryCode,CountryName
- CountryCode — это двухбуквенный код ISO в верхнем регистре
- CountryName указывается на английском языке

## Формат IPv4 (geoip.txt)

Этот формат заимствован у Tor и легко генерируется из файлов данных, доступных из многих публичных источников. Например:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Спецификации формата:**

- Кодировка — ASCII
- '#' в первом столбце обозначает строку комментария
- Строки записей имеют вид FromIP,ToIP,CountryCode
- FromIP и ToIP — беззнаковые целочисленные представления 4-байтового IP
- CountryCode — это двухбуквенный код ISO в верхнем регистре
- Строки записей должны быть отсортированы по числовому значению FromIP

## Формат IPv6 (geoipv6.dat.gz)

Это сжатый двоичный формат, предназначенный для I2P. Файл сжат с помощью gzip. Формат после распаковки:

```
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

- Данные должны быть отсортированы (знаковый long в формате дополнительного кода), без перекрытий. Порядок такой: 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- Класс GeoIPv6.java содержит программу для генерации этого формата из публичных источников, таких как данные Maxmind GeoLite.
- Поиск GeoIP по IPv6 поддерживается начиная с релиза 0.9.8.
