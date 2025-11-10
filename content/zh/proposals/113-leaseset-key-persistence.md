---
title: "LeaseSet 密钥持久化"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "已关闭"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## 概述

本提案是关于在目前是临时的 LeaseSet 中持久化额外的数据。
已在 0.9.18 中实现。

## 动机

在 0.9.17 中，为 netDb 切片密钥添加了持久化功能，存储在 i2ptunnel.config 中。这有助于通过在重启后保持相同的切片来防止某些攻击，并且还可以防止可能的与路由器重启的关联。

还有另外两件事情更容易与路由器重启相关联：leaseset 加密和签名密钥。目前这些都没有被持久化。

## 提议的更改

私钥存储在 i2ptunnel.config 中，作为 i2cp.leaseSetPrivateKey 和 i2cp.leaseSetSigningPrivateKey。
