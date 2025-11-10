---
title: "增加 IPv6 MTU"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "已关闭"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## 概述

本提案建议将最大 SSU IPv6 MTU 从 1472 增加到 1488。
已在 0.9.28 版本中实现。

## 动机

IPv4 MTU 必须是 16 的倍数，加 12。IPv6 MTU 必须是 16 的倍数。

当 IPv6 支持首次增加时，我们将最大 IPv6 MTU 设置为 1472，低于 IPv4 MTU 的 1484。这是为了简化操作并确保 IPv6 MTU 低于现有的 IPv4 MTU。现在 IPv6 支持已经稳定，我们可以将 IPv6 MTU 设置得高于 IPv4 MTU。

典型的接口 MTU 是 1500，因此我们可以合理地将 IPv6 MTU 增加 16 到 1488。

## 设计

将最大值从 1472 更改为 1488。

## 规范

在 SSU 概述中的“Router Address”和“MTU”部分，将最大 IPv6 MTU 从 1472 更改为 1488。

## 迁移

我们预计路由器会如往常一样将连接 MTU 设置为本地和远程 MTU 的最小值。不需要版本检查。

如果确定需要版本检查，我们将为此更改设置最低版本级别为 0.9.28。
