---
title: "GeoIP-Dateiformate"
description: "Legacy GeoIP-Dateiformatspezifikationen für IP-zu-Land-Lookups"
slug: "geoip"
aliases:
  - "/de/geoip"
  - "/de/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Übersicht

> **HINWEIS: VERALTET** - Wir unterstützen jetzt drei Formate, in der Reihenfolge der Präferenz: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) mit allen Installationen gebündelt außer Debian-Paketen und Android > - Maxmind geoip1 (GeoIP.dat) im Debian geoip-database-Paket > - Das IPv4 Tor-Format (geoip.txt) und das benutzerdefinierte IPv6-Format (geoipv6.dat.gz), die unten dokumentiert sind, werden noch unterstützt, aber nicht verwendet.

Diese Seite spezifiziert das Format der verschiedenen GeoIP-Dateien, die vom router verwendet werden, um ein Land für eine IP zu ermitteln.

## Ländername (countries.txt) Format

Dieses Format lässt sich einfach aus Datendateien generieren, die von vielen öffentlichen Quellen verfügbar sind. Zum Beispiel:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Formatspezifikationen:**

- Kodierung ist UTF-8
- `#` in Spalte 1 kennzeichnet eine Kommentarzeile
- Eintragszeilen sind `CountryCode,CountryName`
- CountryCode ist der ISO-Zweibuchstabencode, Großbuchstaben
- CountryName ist auf Englisch

## IPv4 (geoip.txt) Format

Dieses Format ist von Tor übernommen und kann einfach aus Datendateien generiert werden, die von vielen öffentlichen Quellen verfügbar sind. Zum Beispiel:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Formatspezifikationen:**

- Kodierung ist ASCII
- `#` in Spalte 1 kennzeichnet eine Kommentarzeile
- Eintragszeilen sind `FromIP,ToIP,CountryCode`
- FromIP und ToIP sind vorzeichenlose Ganzzahl-Darstellungen der 4-Byte-IP
- CountryCode ist der ISO-Zwei-Buchstaben-Code, Großbuchstaben
- Eintragszeilen müssen nach numerischer FromIP sortiert sein

## IPv6 (geoipv6.dat.gz) Format

Dies ist ein komprimiertes Binärformat, das für I2P entwickelt wurde. Die Datei ist gzipped. Unkomprimiertes Format:

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
**Hinweise:**

- Daten müssen sortiert sein (SIGNED long Zweierkomplement), keine Überlappung. Die Reihenfolge ist also `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- Die Klasse `GeoIPv6.java` enthält ein Programm zur Generierung dieses Formats aus öffentlichen Quellen wie den Maxmind GeoLite-Daten.
- IPv6 GeoIP-Lookup wird ab Release 0.9.8 unterstützt.
