---
title: "Formatos de Arquivo GeoIP"
description: "Especificações do formato de arquivo GeoIP legado para consultas de IP para país"
slug: "geoip"
aliases:
  - "/pt/geoip"
  - "/pt/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Visão Geral

> **NOTA: OBSOLETO** - Agora suportamos três formatos, em ordem de preferência: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) incluído em todas as instalações exceto pacotes Debian e Android > - Maxmind geoip1 (GeoIP.dat) no pacote Debian geoip-database > - O formato IPv4 Tor (geoip.txt) e o formato IPv6 personalizado (geoipv6.dat.gz) documentado abaixo, ainda suportado mas não utilizado.

Esta página especifica o formato dos vários arquivos GeoIP, usados pelo router para consultar o país de um IP.

## Formato do Nome do País (countries.txt)

Este formato é facilmente gerado a partir de arquivos de dados disponíveis de muitas fontes públicas. Por exemplo:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Especificações de formato:**

- A codificação é UTF-8
- `#` na coluna 1 especifica uma linha de comentário
- As linhas de entrada são `CountryCode,CountryName`
- CountryCode é o código ISO de duas letras, em maiúsculas
- CountryName está em inglês

## Formato IPv4 (geoip.txt)

Este formato é emprestado do Tor e é facilmente gerado a partir de arquivos de dados disponíveis em muitas fontes públicas. Por exemplo:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Especificações de formato:**

- A codificação é ASCII
- `#` na coluna 1 especifica uma linha de comentário
- As linhas de entrada são `FromIP,ToIP,CountryCode`
- FromIP e ToIP são representações de inteiros sem sinal do IP de 4 bytes
- CountryCode é o código ISO de duas letras, em maiúsculas
- As linhas de entrada devem ser ordenadas por FromIP numérico

## Formato IPv6 (geoipv6.dat.gz)

Este é um formato binário comprimido projetado para I2P. O arquivo está comprimido com gzip. Formato descomprimido:

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

- Os dados devem estar ordenados (SIGNED long complemento de dois), sem sobreposição. Então a ordem é `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- A classe `GeoIPv6.java` contém um programa para gerar este formato a partir de fontes públicas como os dados Maxmind GeoLite.
- A consulta GeoIP IPv6 é suportada a partir da versão 0.9.8.
