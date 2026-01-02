---
title: "GeoIP 文件格式"
description: "用于 IP 到国家查询的旧版 GeoIP（基于 IP 的地理定位）文件格式规范"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 概述

**注意：已过时** - 我们现在支持三种格式，按优先顺序排列：

- Maxmind 的 geoip2（GeoLite2-Country.mmdb）随所有安装一起打包提供，Debian 软件包和 Android 除外
- Maxmind 的 geoip1（GeoIP.dat）位于 Debian 的 geoip-database 软件包中
- 如下文所述的 IPv4 Tor 格式（geoip.txt）以及自定义的 IPv6 格式（geoipv6.dat.gz）仍受支持，但未使用

本页说明了各种 GeoIP 文件的格式，这些文件由 router 用于为某个 IP 查询所属国家/地区。

## 国家名称（countries.txt）格式

该格式可从许多公共来源提供的数据文件轻松生成。例如：

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**格式规范：**

- 编码为 UTF-8
- 第 1 列中的 '#' 表示注释行
- 条目行为 CountryCode,CountryName
- CountryCode 为 ISO 两位字母代码，使用大写
- CountryName 为英文

## IPv4 (geoip.txt) 格式

此格式借鉴自 Tor，并且可以从许多公开来源提供的数据文件轻松生成。例如：

```bash
$ wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
$ unzip GeoIPCountryCSV.zip
$ cut -d, -f3-5 < GeoIPCountryWhois.csv | sed 's/"//g' > geoip.txt
$ cut -d, -f5,6 < GeoIPCountryWhois.csv | sed 's/"//g' | sort | uniq > countries.txt
```
**格式规范：**

- 编码为 ASCII
- 第一列的 '#' 表示注释行
- 条目行的格式为 FromIP,ToIP,CountryCode
- FromIP 和 ToIP 是 4 字节 IP 的无符号整数表示
- CountryCode 是 ISO 两字母代码，使用大写
- 条目行必须按 FromIP 的数值排序

## IPv6 (geoipv6.dat.gz) 格式

这是为 I2P 设计的压缩二进制格式。该文件使用 gzip 压缩。解压后的格式：

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
**注意事项：**

- 数据必须按（有符号 long 的二进制补码）排序，且不得重叠。因此顺序为 80000000 ... FFFFFFFF 00000000 ... 7FFFFFFF。
- GeoIPv6.java 类包含一个程序，可从公共来源（例如 MaxMind 的 GeoLite 数据）生成此格式。
- 自 0.9.8 版本起支持 IPv6 GeoIP 查询。
