---
title: "GeoIP Dosya Formatları"
description: "IP'den ülke sorgulamaları için eski GeoIP dosya biçimi spesifikasyonları"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Genel Bakış

**NOT: ARTIK GEÇERSİZ** - Artık tercih sırasına göre üç formatı destekliyoruz:

- Maxmind geoip2 (GeoLite2-Country.mmdb), Debian paketleri ve Android hariç tüm kurulumlarla birlikte gelir
- Maxmind geoip1 (GeoIP.dat), Debian geoip-database paketinde bulunur
- Aşağıda belgelenen IPv4 Tor biçimi (geoip.txt) ve özel IPv6 biçimi (geoipv6.dat.gz), hâlâ desteklenmektedir ancak kullanılmamaktadır.

Bu sayfa, router tarafından bir IP’nin ülkesini sorgulamak için kullanılan çeşitli GeoIP dosyalarının biçimini tanımlar.

## Ülke Adı (countries.txt) Biçimi

Bu biçim, pek çok kamuya açık kaynaktan erişilebilen veri dosyalarından kolayca oluşturulabilir. Örneğin:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Biçim özellikleri:**

- Kodlama UTF-8'dir
- 1. sütundaki '#' bir yorum satırını belirtir
- Girdi satırları CountryCode,CountryName biçimindedir
- CountryCode, iki harfli ISO kodudur, büyük harflerle yazılır
- CountryName İngilizcedir

## IPv4 (geoip.txt) Biçimi

Bu biçim Tor'dan alınmıştır ve birçok kamuya açık kaynaktan temin edilebilen veri dosyalarından kolayca oluşturulabilir. Örneğin:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Biçim spesifikasyonları:**

- Kodlama ASCII'dir
- 1. sütundaki '#' bir yorum satırını belirtir
- Kayıt satırları FromIP,ToIP,CountryCode şeklindedir
- FromIP ve ToIP, 4 baytlık IP'nin işaretsiz tamsayı gösterimleridir
- CountryCode, ISO iki harfli koddur, büyük harfli olmalıdır
- Kayıt satırları, sayısal FromIP değerine göre sıralanmış olmalıdır

## IPv6 (geoipv6.dat.gz) Formatı

Bu, I2P için tasarlanmış sıkıştırılmış bir ikili biçimdir. Dosya gzip ile sıkıştırılmıştır. Sıkıştırması açılmış biçim:

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
**Notlar:**

- Veriler sıralanmış olmalıdır (işaretli long ikinin tümleyeni), çakışma olmamalıdır. Sıralama şu şekildedir: 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- GeoIPv6.java sınıfı, Maxmind GeoLite verileri gibi kamuya açık kaynaklardan bu biçimi üretmek için bir program içerir.
- IPv6 GeoIP sorgulaması 0.9.8 sürümünden itibaren desteklenir.
