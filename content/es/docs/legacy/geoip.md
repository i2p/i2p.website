---
title: "Formatos de Archivo GeoIP"
description: "Especificaciones del formato de archivo GeoIP heredado para búsquedas de IP a país"
slug: "geoip"
aliases:
  - "/es/geoip"
  - "/es/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Resumen

> **NOTA: OBSOLETO** - Ahora soportamos tres formatos, en orden de preferencia: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) incluido con todas las instalaciones excepto paquetes de Debian y Android > - Maxmind geoip1 (GeoIP.dat) en el paquete geoip-database de Debian > - El formato IPv4 de Tor (geoip.txt) y el formato IPv6 personalizado (geoipv6.dat.gz) documentados a continuación, aún soportados pero no utilizados.

Esta página especifica el formato de los diversos archivos GeoIP, utilizados por el router para buscar un país para una IP.

## Formato de Nombre de País (countries.txt)

Este formato se genera fácilmente a partir de archivos de datos disponibles en muchas fuentes públicas. Por ejemplo:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Especificaciones de formato:**

- La codificación es UTF-8
- `#` en la columna 1 especifica una línea de comentario
- Las líneas de entrada son `CountryCode,CountryName`
- CountryCode es el código ISO de dos letras, en mayúsculas
- CountryName está en inglés

## Formato IPv4 (geoip.txt)

Este formato está tomado de Tor y se genera fácilmente a partir de archivos de datos disponibles en muchas fuentes públicas. Por ejemplo:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Especificaciones de formato:**

- La codificación es ASCII
- `#` en la columna 1 especifica una línea de comentario
- Las líneas de entrada son `FromIP,ToIP,CountryCode`
- FromIP y ToIP son representaciones de enteros sin signo de la IP de 4 bytes
- CountryCode es el código ISO de dos letras, en mayúsculas
- Las líneas de entrada deben estar ordenadas por FromIP numérico

## Formato IPv6 (geoipv6.dat.gz)

Este es un formato binario comprimido diseñado para I2P. El archivo está comprimido con gzip. Formato descomprimido:

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
**Notas:**

- Los datos deben estar ordenados (complemento a dos SIGNED long), sin solapamiento. Por lo tanto, el orden es `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- La clase `GeoIPv6.java` contiene un programa para generar este formato a partir de fuentes públicas como los datos GeoLite de Maxmind.
- La búsqueda GeoIP IPv6 es compatible a partir de la versión 0.9.8.
