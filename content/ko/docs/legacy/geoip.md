---
title: "GeoIP 파일 형식"
description: "IP 국가 조회를 위한 레거시 GeoIP 파일 형식 사양"
slug: "geoip"
aliases:
  - "/ko/geoip"
  - "/ko/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 개요

> **참고: 사용 중단** - 이제 우선순위에 따라 세 가지 형식을 지원합니다: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) Debian 패키지와 Android를 제외한 모든 설치에 번들로 제공 > - Maxmind geoip1 (GeoIP.dat) Debian geoip-database 패키지에서 > - 아래에 문서화된 IPv4 Tor 형식 (geoip.txt)과 사용자 정의 IPv6 형식 (geoipv6.dat.gz), 여전히 지원되지만 사용되지 않음.

이 페이지는 router가 IP에 대한 국가를 조회하는 데 사용되는 다양한 GeoIP 파일의 형식을 명시합니다.

## 국가 이름 (countries.txt) 형식

이 형식은 많은 공개 소스에서 사용할 수 있는 데이터 파일로부터 쉽게 생성됩니다. 예를 들어:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**형식 사양:**

- 인코딩은 UTF-8입니다
- 1열의 `#`은 주석 라인을 지정합니다
- 항목 라인은 `CountryCode,CountryName` 형식입니다
- CountryCode는 ISO 2글자 코드, 대문자입니다
- CountryName은 영어로 작성됩니다

## IPv4 (geoip.txt) 형식

이 형식은 Tor에서 차용한 것으로, 많은 공개 소스에서 제공하는 데이터 파일로부터 쉽게 생성할 수 있습니다. 예를 들어:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**형식 사양:**

- 인코딩은 ASCII입니다
- 첫 번째 열의 `#`은 주석 줄을 지정합니다
- 항목 줄은 `FromIP,ToIP,CountryCode` 형식입니다
- FromIP와 ToIP는 4바이트 IP의 부호 없는 정수 표현입니다
- CountryCode는 대문자로 된 ISO 두 글자 코드입니다
- 항목 줄은 숫자 FromIP 순으로 정렬되어야 합니다

## IPv6 (geoipv6.dat.gz) 형식

이는 I2P용으로 설계된 압축된 바이너리 형식입니다. 파일은 gzip으로 압축되어 있습니다. 압축 해제된 형식:

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
**참고사항:**

- 데이터는 정렬되어야 하며 (SIGNED long twos complement), 중복이 없어야 합니다. 따라서 순서는 `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`입니다.
- `GeoIPv6.java` 클래스에는 Maxmind GeoLite 데이터와 같은 공개 소스에서 이 형식을 생성하는 프로그램이 포함되어 있습니다.
- IPv6 GeoIP 조회는 0.9.8 릴리스부터 지원됩니다.
