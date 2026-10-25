---
title: "Định dạng tệp GeoIP"
description: "Đặc tả định dạng tệp GeoIP cũ cho việc tra cứu IP sang quốc gia"
slug: "geoip"
aliases:
  - "/vi/geoip"
  - "/vi/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Tổng quan

> **LƯU Ý: ĐÃ LỖI THỜI** - Chúng tôi hiện hỗ trợ ba định dạng, theo thứ tự ưu tiên: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) được đóng gói với tất cả các bản cài đặt trừ gói Debian và Android > - Maxmind geoip1 (GeoIP.dat) trong gói geoip-database của Debian > - Định dạng IPv4 Tor (geoip.txt) và định dạng IPv6 tùy chỉnh (geoipv6.dat.gz) được ghi lại bên dưới, vẫn được hỗ trợ nhưng không sử dụng.

Trang này chỉ định định dạng của các tệp GeoIP khác nhau, được router sử dụng để tra cứu quốc gia của một IP.

## Định dạng Tên Quốc gia (countries.txt)

Định dạng này có thể được tạo ra dễ dàng từ các tệp dữ liệu có sẵn từ nhiều nguồn công khai. Ví dụ:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Đặc tả định dạng:**

- Mã hóa là UTF-8
- `#` ở cột 1 xác định một dòng chú thích
- Các dòng mục nhập có dạng `CountryCode,CountryName`
- CountryCode là mã ISO hai chữ cái, viết hoa
- CountryName là bằng tiếng Anh

## Định dạng IPv4 (geoip.txt)

Định dạng này được mượn từ Tor và có thể dễ dàng tạo ra từ các tập tin dữ liệu có sẵn từ nhiều nguồn công khai. Ví dụ:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**Đặc tả định dạng:**

- Mã hóa là ASCII
- `#` ở cột 1 chỉ định một dòng bình luận
- Các dòng mục là `FromIP,ToIP,CountryCode`
- FromIP và ToIP là biểu diễn số nguyên không dấu của IP 4-byte
- CountryCode là mã ISO hai chữ cái, viết hoa
- Các dòng mục phải được sắp xếp theo FromIP số

## Định dạng IPv6 (geoipv6.dat.gz)

Đây là định dạng nhị phân nén được thiết kế cho I2P. File được nén bằng gzip. Định dạng sau khi giải nén:

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
**Ghi chú:**

- Dữ liệu phải được sắp xếp (SIGNED long bù hai), không có chồng lấn. Vậy thứ tự là `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- Lớp `GeoIPv6.java` chứa một chương trình để tạo định dạng này từ các nguồn công khai như dữ liệu Maxmind GeoLite.
- Tra cứu GeoIP IPv6 được hỗ trợ từ phiên bản 0.9.8.
