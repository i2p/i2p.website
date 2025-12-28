---
title: "Định dạng tập tin GeoIP"
description: "Đặc tả định dạng tệp GeoIP (cơ sở dữ liệu địa lý IP) kiểu cũ cho tra cứu IP theo quốc gia"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Tổng quan

**LƯU Ý: ĐÃ LỖI THỜI** - Chúng tôi hiện hỗ trợ ba định dạng, theo thứ tự ưu tiên:

- Maxmind geoip2 (GeoLite2-Country.mmdb) được đóng gói kèm theo tất cả các bản cài đặt, ngoại trừ các gói Debian và Android
- Maxmind geoip1 (GeoIP.dat) nằm trong gói Debian geoip-database
- Định dạng IPv4 của Tor (geoip.txt) và định dạng IPv6 tùy chỉnh (geoipv6.dat.gz) được mô tả bên dưới, vẫn được hỗ trợ nhưng không được sử dụng.

Trang này quy định định dạng của các tệp GeoIP khác nhau, được router dùng để tra cứu quốc gia cho một địa chỉ IP.

## Định dạng tên quốc gia (countries.txt)

Định dạng này có thể được tạo dễ dàng từ các tệp dữ liệu có sẵn từ nhiều nguồn công khai. Ví dụ:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Đặc tả định dạng:**

- Mã hóa ký tự là UTF-8
- '#' ở cột 1 chỉ định một dòng chú thích
- Các dòng mục có dạng CountryCode,CountryName
- CountryCode là mã ISO gồm hai chữ cái, viết hoa
- CountryName được viết bằng tiếng Anh

## Định dạng IPv4 (geoip.txt)

Định dạng này được mượn từ Tor và có thể được tạo ra dễ dàng từ các tệp dữ liệu có sẵn từ nhiều nguồn công khai. Ví dụ:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Đặc tả định dạng:**

- Mã hóa là ASCII
- '#' ở cột 1 chỉ định dòng chú thích
- Các dòng mục có dạng FromIP,ToIP,CountryCode
- FromIP và ToIP là dạng biểu diễn số nguyên không dấu của địa chỉ IP 4 byte
- CountryCode là mã gồm hai chữ cái theo ISO, viết hoa
- Các dòng mục phải được sắp xếp theo giá trị số của FromIP

## Định dạng IPv6 (geoipv6.dat.gz)

Đây là một định dạng nhị phân nén được thiết kế cho I2P. Tệp được nén gzip. Định dạng sau khi giải nén:

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
**Lưu ý:**

- Dữ liệu phải được sắp xếp (số long có dấu theo biểu diễn bù hai), không được chồng lấn. Vì vậy, thứ tự là 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- Lớp GeoIPv6.java chứa một chương trình để tạo ra định dạng này từ các nguồn công khai như dữ liệu Maxmind GeoLite.
- Tra cứu GeoIP IPv6 được hỗ trợ kể từ bản phát hành 0.9.8.
