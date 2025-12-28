---
title: "Formáty souborů GeoIP"
description: "Specifikace zastaralého formátu souboru GeoIP pro vyhledávání země podle IP adres"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Přehled

**POZNÁMKA: ZASTARALÉ** - Nyní podporujeme tři formáty, v pořadí podle preferencí:

- Maxmind geoip2 (GeoLite2-Country.mmdb) je součástí všech instalací s výjimkou balíčků pro Debian a instalací pro Android
- Maxmind geoip1 (GeoIP.dat) v balíčku Debianu geoip-database
- Formát Tor pro IPv4 (geoip.txt) a vlastní formát pro IPv6 (geoipv6.dat.gz), popsané níže, jsou stále podporovány, ale nepoužívají se.

Tato stránka určuje formát různých souborů GeoIP, které router používá k vyhledání země podle IP adresy.

## Formát názvu země (countries.txt)

Tento formát lze snadno vytvořit z datových souborů dostupných z mnoha veřejných zdrojů. Například:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Specifikace formátu:**

- Kódování je UTF-8
- '#' v prvním sloupci označuje komentářový řádek
- Řádky záznamů mají formát CountryCode,CountryName
- CountryCode je dvoupísmenný kód ISO, psaný velkými písmeny
- CountryName je v angličtině

## Formát IPv4 (geoip.txt)

Tento formát je převzat z projektu Tor a lze jej snadno vygenerovat z datových souborů dostupných z mnoha veřejných zdrojů. Například:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Specifikace formátu:**

- Kódování je ASCII
- '#' v prvním sloupci označuje komentářový řádek
- Řádky záznamů mají tvar FromIP,ToIP,CountryCode
- FromIP a ToIP jsou neznaménkové celočíselné reprezentace 4bajtové IP adresy
- CountryCode je dvoupísmenný kód ISO, psaný velkými písmeny
- Řádky záznamů musí být seřazeny podle číselného FromIP

## Formát IPv6 (geoipv6.dat.gz)

Toto je komprimovaný binární formát navržený pro I2P. Soubor je komprimován pomocí gzipu. Formát po rozbalení:

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
**POZNÁMKY:**

- Data musí být seřazena (typ long se znaménkem, ve dvojkovém doplňku), bez překryvů. Pořadí je tedy 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- Třída GeoIPv6.java obsahuje program pro vygenerování tohoto formátu z veřejných zdrojů, jako jsou data Maxmind GeoLite.
- Vyhledávání GeoIP pro IPv6 je podporováno od verze 0.9.8.
