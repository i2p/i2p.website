---
title: "Formáty souborů GeoIP"
description: "Specifikace formátu starších GeoIP souborů pro vyhledávání IP adres podle zemí"
slug: "geoip"
aliases:
  - "/cs/geoip"
  - "/cs/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Přehled

> **POZNÁMKA: ZASTARALÉ** - Nyní podporujeme tři formáty, v pořadí podle preference: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) dodávaný se všemi instalacemi kromě Debian balíčků a Android > - Maxmind geoip1 (GeoIP.dat) v Debian balíčku geoip-database > - IPv4 Tor formát (geoip.txt) a vlastní IPv6 formát (geoipv6.dat.gz) zdokumentované níže, stále podporované, ale nepoužívané.

Tato stránka specifikuje formát různých GeoIP souborů, které router používá k vyhledání země pro IP adresu.

## Formát názvů zemí (countries.txt)

Tento formát lze snadno vygenerovat z datových souborů dostupných z mnoha veřejných zdrojů. Například:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Specifikace formátu:**

- Kódování je UTF-8
- `#` v prvním sloupci označuje řádek komentáře
- Řádky záznamů mají formát `CountryCode,CountryName`
- CountryCode je dvoupísmenný ISO kód, velkými písmeny
- CountryName je v angličtině

## IPv4 (geoip.txt) formát

Tento formát je převzat z Toru a lze jej snadno vygenerovat z datových souborů dostupných z mnoha veřejných zdrojů. Například:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Specifikace formátů:**

- Kódování je ASCII
- `#` ve sloupci 1 specifikuje komentář
- Řádky záznamů jsou `FromIP,ToIP,CountryCode`
- FromIP a ToIP jsou reprezentace 4-bajtové IP jako unsigned integer
- CountryCode je dvoupísmenný ISO kód, velkými písmeny
- Řádky záznamů musí být seřazeny podle numerického FromIP

## Formát IPv6 (geoipv6.dat.gz)

Toto je komprimovaný binární formát navržený pro I2P. Soubor je gzipovaný. Nekomprimovaný formát:

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
**Poznámky:**

- Data musí být seřazena (SIGNED long twos complement), bez překrývání. Pořadí je tedy `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- Třída `GeoIPv6.java` obsahuje program pro generování tohoto formátu z veřejných zdrojů, jako jsou data Maxmind GeoLite.
- Vyhledávání IPv6 GeoIP je podporováno od verze 0.9.8.
