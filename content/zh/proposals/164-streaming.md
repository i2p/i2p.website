---
title: "流媒体更新"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "已关闭"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## 概述

早于 API 0.9.58（2023 年 3 月发布）的 Java I2P 和 i2pd 路由器
易受流媒体 SYN 包重放攻击。
这是一个协议设计问题，而不是实现错误。

SYN 包是签名的，但从 Alice 发给 Bob 的初始 SYN 包的签名
并未绑定到 Bob 的身份，因此 Bob 可以存储并重放该包，
将其发送给某个受害者 Charlie。Charlie 会认为包来自
Alice 并对其作出回应。在大多数情况下，这是无害的，但
SYN 包可能包含初始数据（例如 GET 或 POST），
Charlie 会立即处理这些数据。

## 设计

解决方案是让 Alice 在签名的 SYN 数据中包含 Bob 的目标哈希。
Bob 在接收时验证该哈希与他的哈希匹配。

任何潜在的攻击受害者 Charlie
检查此数据并在不匹配其哈希时拒绝 SYN。

通过在 SYN 中使用 NACKs 选项字段存储哈希，
该更改具有向后兼容性，因为不期望在 SYN 包中包含 NACKs，
且目前被忽略。

所有选项均由签名覆盖，像往常一样，所以 Bob 不能
重写哈希。

如果 Alice 和 Charlie 是 API 0.9.58 或更新版本，Bob 的任何重放尝试都将被拒绝。

## 规范

更新 [Streaming 规范](/docs/specs/streaming/) 以添加以下部分：

### 防止重放

为了防止 Bob 通过存储来自 Alice 的有效签名 SYNCHRONIZE 包
并在稍后将其发送给受害者 Charlie 来使用重放攻击，
Alice 必须在 SYNCHRONIZE 包中包含 Bob 的目标哈希，如下所示：

.. raw:: html

  {% highlight lang='dataspec' %}
设定 NACK 计数字段为 8
  将 NACKs 字段设为 Bob 的 32 字节目标哈希

{% endhighlight %}

在接收到 SYNCHRONIZE 时，如果 NACK 计数字段为 8，
Bob 必须将 NACKs 字段解释为 32 字节的目标哈希，
并必须验证其与他的目标哈希匹配。
他还必须像往常一样验证包的签名，
因为它覆盖了整个包，包括 NACK 计数和 NACKs 字段。
如果 NACK 计数为 8 且 NACKs 字段不匹配，
Bob 必须丢弃该包。

这在版本 0.9.58 及更高版本中是必需的。
这与旧版本兼容，
因为不期望在 SYNCHRONIZE 包中包含 NACKs。
目标节点无法知道另一端运行的版本。

对于从 Bob 发给 Alice 的 SYNCHRONIZE ACK 包不需要更改；
不要在该包中包含 NACKs。

## 安全分析

此问题自 2004 年创建流媒体协议以来一直存在。
它是由 I2P 开发者内部发现的。
我们没有证据表明这个问题曾被利用过。
成功利用的实际机会可能会因应用层协议和服务的不同而广泛变化。
点对点应用程序可能比客户端/服务器应用程序更容易受到影响。

## 兼容性

无问题。已知的所有实现目前都忽略了 SYN 包中的 NACKs 字段。
即使它们没有忽略，并试图将其解释为
8 条不同消息的 NACKs，这些消息在 SYNCHRONIZE 握手期间不会存在，
且 NACKs 也毫无意义。

## 迁移

实现可以随时添加支持，无需协调。
Java I2P 和 i2pd 路由器在 API 0.9.58 中实现了这一点（2023 年 3 月发布）。

