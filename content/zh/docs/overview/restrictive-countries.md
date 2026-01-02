---
title: "严格/限制性国家"
description: "I2P 在对路由或匿名工具有限制的司法管辖区中的行为表现(隐藏模式和严格列表)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

I2P的这个实现(本站分发的Java实现)包含一个"严格国家列表",用于在法律可能限制为他人提供路由服务的地区调整router行为。虽然我们不知道有禁止使用I2P的司法管辖区,但有几个国家/地区对中继流量有广泛的禁令。位于"严格"国家/地区的router会自动进入隐藏模式。

该项目在做出这些决定时参考了民权和数字权利组织的研究。特别是，自由之家（Freedom House）正在进行的研究为我们的选择提供了依据。一般指导原则是纳入公民自由（CL）评分为 16 分或以下，或互联网自由评分为 39 分或以下（不自由）的国家。

## 隐藏模式概述

当路由器被置于隐藏模式时,其行为会发生三个关键变化:

- 它不会将 RouterInfo 发布到 netDb。
- 它不接受参与隧道。
- 它拒绝与同一国家的路由器建立直接连接。

这些防御措施使得路由器更难以被可靠地枚举,并降低了违反当地禁止为他人中继流量规定的风险。

## 严格国家列表(截至2024年)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
如果您认为某个国家应该被添加到或从严格列表中移除,请提交一个 issue:https://i2pgit.org/i2p/i2p.i2p/

参考：自由之家 – https://freedomhouse.org/
