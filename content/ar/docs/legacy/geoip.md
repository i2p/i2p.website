---
title: "تنسيقات ملفات GeoIP"
description: "مواصفات صيغة ملف GeoIP القديمة لعمليات البحث من عنوان IP إلى البلد"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## نظرة عامة

**ملاحظة: متقادم** - نحن الآن ندعم ثلاثة تنسيقات، مرتبة حسب الأفضلية:

- Maxmind geoip2 (GeoLite2-Country.mmdb) مُضمَّن مع جميع عمليات التثبيت باستثناء حزم Debian وAndroid
- Maxmind geoip1 (GeoIP.dat) في حزمة Debian geoip-database
- تنسيق Tor الخاص بـ IPv4 (geoip.txt) والتنسيق المخصص لـ IPv6 (geoipv6.dat.gz) الموثقان أدناه، لا يزالان مدعومين ولكن غير مستخدمين.

تحدد هذه الصفحة تنسيق ملفات GeoIP المختلفة، التي يستخدمها الـ router للبحث عن البلد المرتبط بعنوان IP.

## تنسيق اسم الدولة (countries.txt)

يمكن إنشاء هذا التنسيق بسهولة من ملفات بيانات متاحة من العديد من المصادر العامة. على سبيل المثال:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**مواصفات التنسيق:**

- الترميز هو UTF-8
- الرمز '#' في العمود 1 يُشير إلى سطر تعليق
- أسطر الإدخال هي CountryCode,CountryName
- CountryCode هو رمز ISO المكوّن من حرفين، بحروف كبيرة
- CountryName باللغة الإنجليزية

## تنسيق IPv4 (geoip.txt)

هذا التنسيق مُقتبس من Tor ويسهل توليده من ملفات بيانات متاحة من العديد من المصادر العامة. على سبيل المثال:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**مواصفات التنسيق:**

- الترميز هو ASCII
- يشير الرمز '#' في العمود 1 إلى سطر تعليق
- أسطر الإدخال هي FromIP,ToIP,CountryCode
- FromIP و ToIP هما تمثيلات عددية غير موقّعة لعنوان IP ذي 4 بايت
- CountryCode هو رمز ISO المكوّن من حرفين، بالأحرف الكبيرة
- يجب ترتيب أسطر الإدخال حسب قيمة FromIP الرقمية

## تنسيق IPv6 (geoipv6.dat.gz)

هذا تنسيق ثنائي مضغوط مصمم لـ I2P. الملف مضغوط بصيغة gzip. التنسيق بعد فك gzip:

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
**ملاحظات:**

- يجب ترتيب البيانات (long موقّع بتمثيل المتمم لاثنين)، دون أي تداخل. لذا يكون الترتيب 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF.
- تحتوي الفئة GeoIPv6.java على برنامج لتوليد هذا التنسيق من مصادر عامة مثل بيانات Maxmind GeoLite.
- يتم دعم استعلام GeoIP عبر IPv6 اعتبارًا من الإصدار 0.9.8.
