---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Rejected"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## 概述

本提案涉及一种新型LeaseSet格式，支持更新的加密类型。

## 动机

I2P通道中使用的端到端加密具有独立的加密和签名密钥。签名密钥在通道Destination中，已通过KeyCertificates扩展以支持更新的签名类型。然而，加密密钥是LeaseSet的一部分，其中不包含任何证书。因此，有必要实施新的LeaseSet格式，并添加支持以在netDb中存储它。

一个好消息是，一旦实施LS2，所有现有的Destinations都可以利用更现代的加密类型；能够获取和读取LS2的路由器将保证支持任何随之引入的加密类型。

## 规范

基本的LS2格式如下：

- dest
- 发布时间戳 (8字节)
- 过期时间 (8字节)
- 子类型 (1字节) (常规，加密，元数据，或服务)
- 标志 (2字节)

- 子类型特定部分：
  - 常规的加密类型、加密密钥和租赁
  - 加密的blob
  - 服务的属性、散列、端口、撤销等

- 签名
