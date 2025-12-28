---
title: "Formats de fichiers GeoIP"
description: "Spécifications du format de fichier GeoIP hérité pour les recherches IP-vers-pays"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Aperçu

**REMARQUE : OBSOLÈTE** - Nous prenons désormais en charge trois formats, par ordre de préférence :

- Maxmind geoip2 (GeoLite2-Country.mmdb) fourni avec toutes les installations sauf les paquets Debian et Android
- Maxmind geoip1 (GeoIP.dat) dans le paquet Debian geoip-database
- Le format Tor IPv4 (geoip.txt) et le format IPv6 personnalisé (geoipv6.dat.gz) documentés ci-dessous, toujours pris en charge mais non utilisés.

Cette page spécifie le format des différents fichiers GeoIP, utilisés par le router pour associer un pays à une adresse IP.

## Format du nom de pays (countries.txt)

Ce format peut être facilement généré à partir de fichiers de données disponibles auprès de nombreuses sources publiques. Par exemple :

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Spécifications du format :**

- L'encodage est UTF-8
- Le '#' dans la colonne 1 indique une ligne de commentaire
- Les lignes d'entrée sont CountryCode,CountryName
- CountryCode est le code ISO à deux lettres, en majuscules
- CountryName est en anglais

## Format IPv4 (geoip.txt)

Ce format est emprunté à Tor et peut être facilement généré à partir de fichiers de données disponibles auprès de nombreuses sources publiques. Par exemple :

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Spécifications du format:**

- L'encodage est ASCII
- '#' en colonne 1 indique une ligne de commentaire
- Les lignes d'entrée sont FromIP,ToIP,CountryCode
- FromIP et ToIP sont des représentations entières non signées de l'IP sur 4 octets
- CountryCode est le code ISO à deux lettres, en majuscules
- Les lignes d'entrée doivent être triées par la valeur numérique de FromIP

## Format IPv6 (geoipv6.dat.gz)

Ceci est un format binaire compressé conçu pour I2P. Le fichier est compressé avec gzip. Format après décompression :

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
**REMARQUES:**

- Les données doivent être triées (long signé en complément à deux), sans chevauchement. L’ordre est donc 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- La classe GeoIPv6.java contient un programme pour générer ce format à partir de sources publiques telles que les données GeoLite de Maxmind.
- La recherche GeoIP IPv6 est prise en charge à partir de la version 0.9.8.
