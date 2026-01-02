---
title: "GeoIP-Dateiformate"
description: "Spezifikationen des veralteten GeoIP-Dateiformats für IP-zu-Land-Abfragen"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Überblick

**HINWEIS: VERALTET** - Wir unterstützen jetzt drei Formate, in der bevorzugten Reihenfolge:

- Maxmind geoip2 (GeoLite2-Country.mmdb) wird mit allen Installationen gebündelt, außer bei Debian-Paketen und Android
- Maxmind geoip1 (GeoIP.dat) im Debian-Paket geoip-database
- Das IPv4-Tor-Format (geoip.txt) und das benutzerdefinierte IPv6-Format (geoipv6.dat.gz), unten dokumentiert, werden weiterhin unterstützt, aber nicht verwendet.

Diese Seite legt das Format der verschiedenen GeoIP-Dateien fest, die vom router verwendet werden, um für eine IP-Adresse das Land nachzuschlagen.

## Format des Ländernamens (countries.txt)

Dieses Format lässt sich leicht aus Datendateien generieren, die bei vielen öffentlichen Quellen erhältlich sind. Zum Beispiel:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Formatspezifikationen:**

- Die Zeichenkodierung ist UTF-8
- '#' in Spalte 1 kennzeichnet eine Kommentarzeile
- Eintragszeilen sind CountryCode,CountryName
- CountryCode ist der ISO-Zweibuchstabencode, in Großbuchstaben
- CountryName ist auf Englisch

## IPv4 (geoip.txt) Format

Dieses Format wurde von Tor übernommen und kann leicht aus Datendateien generiert werden, die von vielen öffentlichen Quellen verfügbar sind. Zum Beispiel:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Formatspezifikationen:**

- Die Kodierung ist ASCII
- '#' in Spalte 1 kennzeichnet eine Kommentarzeile
- Eintragszeilen haben das Format FromIP,ToIP,CountryCode
- FromIP und ToIP sind vorzeichenlose Ganzzahl-Darstellungen der 4-Byte-IP-Adresse
- CountryCode ist der zweibuchstabige ISO-Code, in Großbuchstaben
- Eintragszeilen müssen nach dem numerischen FromIP sortiert sein

## IPv6 (geoipv6.dat.gz) Format

Dies ist ein komprimiertes Binärformat, das für I2P entwickelt wurde. Die Datei ist gzip-komprimiert. Dekomprimiertes Format:

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
**HINWEISE:**

- Die Daten müssen sortiert sein (SIGNIERTER long-Wert im Zweierkomplement), keine Überschneidungen. Die Reihenfolge ist also 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- Die Klasse GeoIPv6.java enthält ein Programm, um dieses Format aus öffentlichen Quellen wie den Maxmind-GeoLite-Daten zu generieren.
- Die IPv6-GeoIP-Abfrage wird seit Version 0.9.8 unterstützt.
