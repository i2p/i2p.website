---
title: "GeoIP फ़ाइल प्रारूप"
description: "IP से देश की खोज के लिए लिगेसी GeoIP फ़ाइल फ़ॉर्मेट विनिर्देश"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## अवलोकन

**नोट: अप्रचलित** - अब हम प्राथमिकता के क्रम में तीन प्रारूपों का समर्थन करते हैं:

- Maxmind geoip2 (GeoLite2-Country.mmdb) सभी इंस्टॉलेशनों के साथ बंडल होता है, Debian पैकेजों और Android को छोड़कर
- Maxmind geoip1 (GeoIP.dat) Debian geoip-database पैकेज में
- नीचे प्रलेखित IPv4 Tor फॉर्मेट (geoip.txt) और कस्टम IPv6 फॉर्मेट (geoipv6.dat.gz), अब भी समर्थित हैं, लेकिन उपयोग नहीं किए जाते।

यह पृष्ठ विभिन्न GeoIP फ़ाइलों का प्रारूप निर्दिष्ट करता है, जिनका उपयोग router द्वारा किसी IP के लिए देश खोजने में किया जाता है।

## देश का नाम (countries.txt) प्रारूप

यह फ़ॉर्मेट कई सार्वजनिक स्रोतों से उपलब्ध डेटा फ़ाइलों से आसानी से तैयार किया जा सकता है। उदाहरण के लिए:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**प्रारूप विनिर्देश:**

- एन्कोडिंग UTF-8 है
- स्तंभ 1 में '#' एक टिप्पणी पंक्ति को दर्शाता है
- प्रविष्टि पंक्तियाँ CountryCode,CountryName होती हैं
- CountryCode ISO का दो-अक्षरीय कोड है, बड़े अक्षरों में
- CountryName अंग्रेज़ी में है

## IPv4 (geoip.txt) प्रारूप

यह फ़ॉर्मेट Tor से लिया गया है और इसे कई सार्वजनिक स्रोतों से उपलब्ध डेटा फ़ाइलों से आसानी से उत्पन्न किया जा सकता है। उदाहरण के लिए:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**प्रारूप विनिर्देश:**

- एन्कोडिंग ASCII में है
- पहले स्तंभ में '#' एक टिप्पणी पंक्ति को दर्शाता है
- प्रविष्टि पंक्तियाँ FromIP,ToIP,CountryCode हैं
- FromIP और ToIP 4-बाइट IP के unsigned integer (बिना चिन्ह वाला पूर्णांक) निरूपण हैं
- CountryCode ISO का दो-अक्षरीय कोड है, बड़े अक्षरों में
- प्रविष्टि पंक्तियाँ FromIP के संख्यात्मक मान के अनुसार क्रमबद्ध होनी चाहिए

## IPv6 (geoipv6.dat.gz) प्रारूप

यह I2P के लिए डिज़ाइन किया गया संपीड़ित बाइनरी फ़ॉर्मैट है। फ़ाइल gzipped (gzip से संपीड़ित) है। Ungzipped (gzip हटाने के बाद) फ़ॉर्मैट:

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
**टिप्पणियाँ:**

- डेटा को क्रमबद्ध होना चाहिए (SIGNED long twos complement; साइन किया हुआ long दो के पूरक प्रतिनिधित्व), कोई ओवरलैप नहीं। इसलिए क्रम 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF है।
- GeoIPv6.java क्लास में एक प्रोग्राम है जो Maxmind GeoLite डेटा जैसे सार्वजनिक स्रोतों से इस प्रारूप को उत्पन्न करता है।
- रिलीज़ 0.9.8 से IPv6 GeoIP लुकअप समर्थित है।
