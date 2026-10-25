---
title: "تنسيقات ملف GeoIP"
description: "مواصفات تنسيق ملف GeoIP القديم للبحث عن البلد من عنوان IP"
slug: "geoip"
aliases:
  - "/ar/geoip"
  - "/ar/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## نظرة عامة

> **ملاحظة: مُهمل** - نحن الآن ندعم ثلاثة تنسيقات، مرتبة حسب الأفضلية: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) مُرفق مع جميع عمليات التثبيت عدا حزم Debian وAndroid > - Maxmind geoip1 (GeoIP.dat) في حزمة Debian geoip-database > - تنسيق Tor للـ IPv4 (geoip.txt) والتنسيق المخصص للـ IPv6 (geoipv6.dat.gz) الموثق أدناه، لا يزال مدعوماً ولكن غير مستخدم.

تحدد هذه الصفحة تنسيق ملفات GeoIP المختلفة، التي يستخدمها الـ router للبحث عن بلد لعنوان IP معين.

## تنسيق اسم البلد (countries.txt)

يمكن إنتاج هذا التنسيق بسهولة من ملفات البيانات المتاحة من العديد من المصادر العامة. على سبيل المثال:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**مواصفات التنسيق:**

- الترميز هو UTF-8
- `#` في العمود الأول يحدد سطر تعليق
- أسطر الإدخال هي `CountryCode,CountryName`
- CountryCode هو رمز ISO المكون من حرفين، بأحرف كبيرة
- CountryName باللغة الإنجليزية

## تنسيق IPv4 (geoip.txt)

هذا التنسيق مستعار من Tor ويمكن توليده بسهولة من ملفات البيانات المتوفرة من العديد من المصادر العامة. على سبيل المثال:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**مواصفات التنسيق:**

- التشفير هو ASCII
- `#` في العمود 1 يحدد خط تعليق
- خطوط الإدخال هي `FromIP,ToIP,CountryCode`
- FromIP و ToIP هما تمثيلان بأرقام صحيحة غير موقعة لعنوان IP المكون من 4 بايت
- CountryCode هو رمز ISO المكون من حرفين، بأحرف كبيرة
- يجب ترتيب خطوط الإدخال حسب FromIP الرقمي

## تنسيق IPv6 (geoipv6.dat.gz)

هذا تنسيق ثنائي مضغوط مصمم لـ I2P. الملف مضغوط بـ gzip. التنسيق غير المضغوط:

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
**ملاحظات:**

- يجب أن تكون البيانات مرتبة (SIGNED long twos complement)، بدون تداخل. لذا الترتيب هو `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`.
- فئة `GeoIPv6.java` تحتوي على برنامج لإنتاج هذا التنسيق من مصادر عامة مثل بيانات Maxmind GeoLite.
- البحث في GeoIP للـ IPv6 مدعوم اعتباراً من الإصدار 0.9.8.
