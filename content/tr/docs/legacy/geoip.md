---
title: "GeoIP Dosya Formatları"
description: "IP'den ülkeye arama işlemleri için eski GeoIP dosya formatı belirtimleri"
slug: "geoip"
aliases:
  - "/tr/geoip"
  - "/tr/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Genel Bakış

> **NOT: ESKİMİŞ** - Artık tercih sırasına göre üç formatı destekliyoruz: > > - Debian paketleri ve Android hariç tüm kurulumlarla birlikte gelen Maxmind geoip2 (GeoLite2-Country.mmdb) > - Debian geoip-database paketindeki Maxmind geoip1 (GeoIP.dat) > - Aşağıda belgelenen IPv4 Tor formatı (geoip.txt) ve özel IPv6 formatı (geoipv6.dat.gz), hala destekleniyor ancak kullanılmıyor.

Bu sayfa, router tarafından bir IP için ülke aramak amacıyla kullanılan çeşitli GeoIP dosyalarının formatını belirtir.

## Ülke Adı (countries.txt) Formatı

Bu format, birçok halka açık kaynaktan edinilebilecek veri dosyalarından kolayca üretilebilir. Örneğin:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Format özellikleri:**

- Kodlama UTF-8'dir
- 1. sütundaki `#` bir yorum satırını belirtir
- Giriş satırları `ÜlkeKodu,ÜlkeAdı` formatındadır
- ÜlkeKodu, büyük harflerle yazılmış ISO iki harfli koddur
- ÜlkeAdı İngilizce'dir

## IPv4 (geoip.txt) Formatı

Bu format Tor'dan ödünç alınmıştır ve birçok genel kaynaktan edinilebilen veri dosyalarından kolayca oluşturulabilir. Örneğin:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Format özellikleri:**

- Kodlama ASCII'dir
- 1. sütunda `#` bir yorum satırını belirtir
- Giriş satırları `FromIP,ToIP,CountryCode` formatındadır
- FromIP ve ToIP, 4-byte IP'nin işaretsiz tamsayı temsilleridir
- CountryCode, ISO iki harfli kod, büyük harflerle
- Giriş satırları sayısal FromIP'ye göre sıralanmış olmalıdır

## IPv6 (geoipv6.dat.gz) Formatı

Bu, I2P için tasarlanmış sıkıştırılmış bir ikili formattır. Dosya gzip ile sıkıştırılmıştır. Sıkıştırması açılmış format:

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
**Notlar:**

- Veri sıralanmış olmalıdır (SIGNED long twos complement), çakışma olmamalıdır. Böylece sıralama şöyledir: `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- `GeoIPv6.java` sınıfı, Maxmind GeoLite verisi gibi herkese açık kaynaklardan bu formatı oluşturmak için bir program içerir.
- IPv6 GeoIP sorgulaması 0.9.8 sürümünden itibaren desteklenmektedir.
