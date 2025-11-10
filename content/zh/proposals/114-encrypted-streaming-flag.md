---
title: "'加密' 流媒体标志"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "需要研究"
thread: "http://zzz.i2p/topics/1795"
---

## 概述

本提案涉及在流媒体中添加一个标志，以指定正在使用的端到端加密类型。

## 动机

高负载应用程序可能会遇到 ElGamal/AES+SessionTags 标签的短缺。

## 设计

在流媒体协议中的某个地方添加一个新标志。如果数据包带有此标志，则意味着有效载荷通过私钥和对等方的公钥的密钥进行了 AES 加密。这可以消除大蒜（ElGamal/AES）加密和标签短缺的问题。

可以通过 SYN 针对每个数据包或每个流设置。
