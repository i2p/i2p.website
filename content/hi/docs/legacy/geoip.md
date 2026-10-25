---
title: "GeoIP फ़ाइल प्रारूप"
description: "IP से देश लुकअप के लिए लेगेसी GeoIP फ़ाइल प्रारूप विनिर्देश"
slug: "geoip"
aliases:
  - "/hi/geoip"
  - "/hi/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## अवलोकन

> **नोट: अप्रचलित** - अब हम तीन फॉर्मेट्स का समर्थन करते हैं, प्राथमिकता के क्रम में: > > - Maxmind geoip2 (GeoLite2-Country.mmdb) सभी इंस्टॉल्स के साथ बंडल किया गया है सिवाय Debian packages और Android के > - Maxmind geoip1 (GeoIP.dat) Debian geoip-database package में > - IPv4 Tor format (geoip.txt) और custom IPv6 format (geoipv6.dat.gz) नीचे प्रलेखित है, अभी भी समर्थित है लेकिन अप्रयुक्त है।

यह पृष्ठ विभिन्न GeoIP फ़ाइलों के प्रारूप को निर्दिष्ट करता है, जो router द्वारा किसी IP के लिए देश की जानकारी खोजने के लिए उपयोग की जाती हैं।

## देश का नाम (countries.txt) प्रारूप

यह प्रारूप कई सार्वजनिक स्रोतों से उपलब्ध डेटा फाइलों से आसानी से उत्पन्न किया जा सकता है। उदाहरण के लिए:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**प्रारूप विशिष्टताएं:**

- एन्कोडिंग UTF-8 है
- कॉलम 1 में `#` एक टिप्पणी लाइन को निर्दिष्ट करता है
- एंट्री लाइनें `CountryCode,CountryName` हैं
- CountryCode ISO दो-अक्षर कोड है, बड़े अक्षरों में
- CountryName अंग्रेजी में है

## IPv4 (geoip.txt) प्रारूप

यह प्रारूप Tor से लिया गया है और कई सार्वजनिक स्रोतों से उपलब्ध डेटा फाइलों से आसानी से उत्पन्न किया जा सकता है। उदाहरण के लिए:

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**प्रारूप विनिर्देश:**

- Encoding ASCII है
- कॉलम 1 में `#` एक comment line को निर्दिष्ट करता है
- Entry lines `FromIP,ToIP,CountryCode` हैं
- FromIP और ToIP 4-byte IP के unsigned integer representations हैं
- CountryCode ISO two-letter code है, upper case में
- Entry lines को numeric FromIP के अनुसार sorted होना चाहिए

## IPv6 (geoipv6.dat.gz) प्रारूप

यह I2P के लिए डिज़ाइन किया गया एक संपीड़ित बाइनरी फॉर्मेट है। फ़ाइल gzipped है। Ungzipped फॉर्मेट:

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
**नोट्स:**

- डेटा को सॉर्ट किया जाना चाहिए (SIGNED long twos complement), कोई ओवरलैप नहीं। तो क्रम है `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`।
- `GeoIPv6.java` क्लास में Maxmind GeoLite डेटा जैसे सार्वजनिक स्रोतों से इस फॉर्मेट को जनरेट करने का प्रोग्राम है।
- IPv6 GeoIP लुकअप रिलीज़ 0.9.8 से समर्थित है।
