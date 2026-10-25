---
title: "SOCKS 代理"
description: "安全使用I2P的SOCKS tunnel"
slug: "socks"
aliases:
  - "/zh/socks"
  - "/zh/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS 和 SOCKS 代理 {#overview}

SOCKS 代理从 0.7.1 版本开始可以正常工作。支持 SOCKS 4/4a/5。通过在 i2ptunnel 中创建 SOCKS 客户端 tunnel 来启用 SOCKS。支持共享客户端和非共享客户端。由于没有 SOCKS 出口代理，所以用途有限。

正如[常见问题](/docs/overview/faq#socks)中所说：

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
引用2005年一封邮件中的内容：

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
希望我们能够简单地在I2P之上搭载任意客户端而不对其行为和暴露的协议进行安全性和匿名性审计，这种想法是幼稚的。几乎*每个*应用程序和协议都会违反匿名性，除非它是专门为此设计的，即便如此，其中大多数也会如此。这就是现实。专为匿名性和安全性设计的系统能更好地为最终用户服务。修改现有系统以在匿名环境中工作绝非易事，比简单使用现有I2P API的工作量要大几个数量级。

SOCKS 代理支持标准地址簿名称，但不支持 Base64 destinations。从 0.7 版本开始应该支持 Base32 哈希。它仅支持出站连接，即 I2PTunnel 客户端。UDP 支持已预留但尚未正常工作。按端口号选择出口代理的功能已预留。

## 另请参见 {#see-also}

- 第81次会议（2004年3月16日）和第82次会议（2004年3月23日）的会议记录。
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## 如果您确实让某些功能正常工作 {#working}

请告诉我们。并且请提供关于 SOCKS 代理风险的重要警告。
