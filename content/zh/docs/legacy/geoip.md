---
title: "GeoIP 文件格式"
description: "用于IP到国家查询的传统GeoIP文件格式规范"
slug: "geoip"
aliases:
  - "/zh/geoip"
  - "/zh/geoip/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 概览

> **注意：已过时** - 我们现在支持三种格式，按优先级顺序： > > - Maxmind geoip2 (GeoLite2-Country.mmdb) 捆绑在除 Debian 软件包和 Android 之外的所有安装中 > - Maxmind geoip1 (GeoIP.dat) 在 Debian geoip-database 软件包中 > - IPv4 Tor 格式 (geoip.txt) 和自定义 IPv6 格式 (geoipv6.dat.gz) 如下所述，仍受支持但未使用。

本页面说明了各种 GeoIP 文件的格式，router 使用这些文件来查找 IP 地址对应的国家。

## 国家名称（countries.txt）格式

这种格式可以轻松地从许多公共来源提供的数据文件生成。例如：

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**格式规范：**

- 编码是 UTF-8
- 第1列的 `#` 指定注释行
- 条目行格式为 `CountryCode,CountryName`
- CountryCode 是 ISO 两字母代码，大写
- CountryName 是英文

## IPv4 (geoip.txt) 格式

这种格式借鉴自 Tor，可以很容易地从许多公共来源提供的数据文件中生成。例如：

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**格式规范：**

- 编码是 ASCII
- 第1列中的 `#` 表示注释行
- 条目行格式为 `FromIP,ToIP,CountryCode`
- FromIP 和 ToIP 是4字节IP的无符号整数表示
- CountryCode 是ISO两字母代码，大写
- 条目行必须按数字 FromIP 排序

## IPv6 (geoipv6.dat.gz) 格式

这是为I2P设计的压缩二进制格式。文件经过gzip压缩。解压缩后的格式：

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
**注意事项：**

- 数据必须排序（有符号长整型二进制补码），无重叠。所以顺序是 `80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF`。
- `GeoIPv6.java` 类包含一个程序，可以从公共数据源（如 Maxmind GeoLite 数据）生成此格式。
- 从 0.9.8 版本开始支持 IPv6 GeoIP 查找。
