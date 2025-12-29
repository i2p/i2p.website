---
title: "LS2中的服务记录"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "已关闭"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## 状态
在2025-04-01的第二次评审中被批准；规格已更新；尚未实现。

## 概述

I2P缺乏一个集中的DNS系统。然而，地址簿与b32主机名系统相结合，使路由器能够查找完整的终点并获取租约集，租约集包含网关和密钥的列表，以便客户端可以连接到该终点。

因此，租约集有点像DNS记录。但目前没有设施可以查找该主机是否支持任何服务，无论是在该终点还是其他终点上，以类似于DNS SRV记录的方式支持服务[SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)。

第一个应用可能是点对点邮件。其他可能的应用：DNS、GNS、密钥服务器、证书颁发机构、时间服务器、BT、加密货币及其他点对点应用。

## 相关提案和替代方案

### 服务列表

LS2提案123 [Prop123](/proposals/123-new-netdb-entries/) 定义了“服务记录”，指示某个终点参与某项全球服务。填充路由器会将这些记录聚合成全球“服务列表”。
由于复杂性、认证缺乏、安全性和垃圾邮件问题，这一提案从未实现。

此提案不同之处在于，它提供了针对特定终点的服务查找，而不是针对某一全球服务的全球终点池。

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) 建议每个人都运行他们自己的DNS服务器。
这个提案是补充的，因为我们可以使用服务记录来指定GNS（或DNS）支持，以标准服务名为"domain"，端口为53。

### Dot well-known

在[DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102)中，建议通过对/.well-known/i2pmail.key的HTTP请求来查找服务。这要求每个服务都必须有相关的网站来托管密钥。大多数用户不运行网站。

一个解决方法是我们可以假设对一个b32地址的服务实际上运行在那个b32地址上。所以，寻找example.i2p的服务需要从http://example.i2p/.well-known/i2pmail.key进行HTTP获取，但针对aaa...aaa.b32.i2p的服务不需要该查找，可以直接连接。

但是这里有一个歧义，因为example.i2p也可以通过它的b32地址进行访问。

### MX记录

SRV记录只是MX记录的一种通用版本，适用于任何服务。
"_smtp._tcp" 是"MX"记录。
如果我们有SRV记录，就不需要MX记录，仅有MX记录不能为任何服务提供通用记录。

## 设计

服务记录位于LS2[LS2](/docs/specs/common-structures/)的选项部分。LS2的选项部分目前未使用。
不支持LS1。
类似于隧道带宽提案[Prop168](/proposals/168-tunnel-bandwidth/)，定义隧道构建记录的选项。

要查找特定主机名或b32的服务地址，路由器会获取租约集并在属性中查找服务记录。

该服务可能托管在与LS本身相同的终点上，也可能引用不同的主机名/b32。

如果服务的目标终点不同，则目标LS也必须包括一个服务记录，指向自己，表示它支持该服务。

设计不需要特定支持或缓存，也不需要填充路由器的任何改变。只有租约集发布者和查找服务记录的客户端必须支持这些更改。

建议进行轻微的I2CP和SAM扩展，以方便客户端检索服务记录。

## 详细说明

### LS2选项规格

LS2选项必须按键排序，因此签名是不变的。

定义如下：

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := 所需服务的符号名称。必须小写。例如："smtp"。
  允许的字符为[a-z0-9-]，不得以"-"开头或结尾。
  必须使用[REGISTRY](http://www.dns-sd.org/ServiceTypes.html)或Linux /etc/services中定义的标准标识符。
- proto := 所需服务的传输协议。必须小写，"tcp"或"udp"。
  "tcp"表示流式，"udp"表示可重传数据报。
  原始数据报和数据报2的协议指示符可能会在以后定义。
  允许的字符为[a-z0-9-]，不得以"-"开头或结尾。
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := 生存时间，整数秒。正整数。例如："86400"。
  建议至少为86400（一天），详细信息请参见下文的建议部分。
- priority := 目标主机的优先级，值越低越优先。非负整数。例如："0"。
  仅在多于一个记录时有用，但即使只有一个记录也需要。
- weight := 对于具有相同优先级的记录的相对权重。值越高，选中的概率越大。非负整数。例如："0"。
  仅在多于一个记录时有用，但即使只有一个记录也需要。
- port := 服务所在的I2CP端口。非负整数。例如："25"。
  支持端口0但不推荐使用。
- target := 提供该服务的终点的主机名或b32。有效的主机名如[NAMING](/docs/overview/naming/)。必须小写。
  例如："aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p"或"example.i2p"。
  除非主机名是“众所周知”的，即在官方或默认地址簿中，否则建议使用b32。
- appoptions := 特定于应用的任意文本，不得包含" "或","。编码为UTF-8。

### 示例：


在aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p的LS2中，指向一个SMTP服务器：

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

在aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p的LS2中，指向两个SMTP服务器：

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

在bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p的LS2中，指向自身作为SMTP服务器：

    "_smtp._tcp" "0 999999 25"

重定向电子邮件的可能格式（见下文）：

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"

### 限制：


LS2选项中使用的映射数据结构格式将键和值限制为最大255字节（而不是字符）。
对于b32目标，optionvalue约为67字节，因此只能容纳3条记录。
可能只有一两条记录带有长的appoptions字段，或者最多四或五条带有短的主机名。
这应该是足够的；多条记录应该是罕见的。

### 与[RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)的差异


- 没有尾部点
- 没有与proto一起的名称
- 需要小写
- 以逗号分隔的文本格式记录，而不是二进制DNS格式
- 不同的记录类型指示符
- 增加了appoptions字段

### 注意事项：


不允许使用通配符(如星号) (asterisk)._tcp 或 _tcp。
每个支持的服务必须有自己的记录。

### 服务名称注册

不在[REGISTRY](http://www.dns-sd.org/ServiceTypes.html)或Linux /etc/services中列出的非标准标识符可以被请求并添加到[LS2](/docs/specs/common-structures/)的共同结构说明中。

特定服务的appoptions格式也可以被添加到那里。

### I2CP规格

[I2CP](/docs/specs/i2cp/)协议必须扩展以支持服务查找。
需要关于服务查找的其他MessageStatusMessage和/或HostReplyMessage错误代码。
为了使查找功能通用，而不仅仅是特定于服务记录，
设计是支持所有LS2选项的检索。

实现：扩展HostLookupMessage以添加请求
LS2选项用于哈希、主机名和终点（请求类型2-4）。
扩展HostReplyMessage以在请求时添加选项映射。
通过其他错误代码扩展HostReplyMessage。

选项映射可以在客户端或路由器端缓存或负缓存，具体取决于实现。建议的最大时间是一小时，除非服务记录TTL较短。
服务记录可以缓存到应用、客户端或路由器指定的TTL。

规范扩展如下：

### 配置选项

将以下内容添加到[I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

要放入租约集的选项。仅适用于LS2。
nnn从0开始。选项值包含“key=value”。
（不包括引号）

例如：

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p

### HostLookup消息


- 查找类型2：哈希查找，请求选项映射
- 查找类型3：主机名查找，请求选项映射
- 查找类型4：终点查找，请求选项映射

对于查找类型4，第5项是一个Destination。

### HostReply消息


对于查找类型2-4，路由器必须获取租约集，
即使查找键在地址簿中。

如果成功，HostReply将包含租约集中的选项映射，并将其作为终点后的第5项。
如果映射中没有选项，或者租约集是版本1，
它仍然会作为一个空的映射（两个字节：0 0）被包含。
租约集中的所有选项将被包括在内，而不仅仅是服务记录选项。
例如，未来定义的参数的选项可能存在。

在租约集查找失败时，回复将包含一个新错误代码6（租约集查找失败）
且不会包含映射。
当返回错误代码6时，Destination字段可能会出现或不会出现。
如果地址簿中的主机名查找成功，
或者之前的查找成功且结果被缓存，
或者如果在查找消息中包含了终点（查找类型4），它将会出现。

如果不支持查找类型，
回复将包含一个新错误代码7（不支持的查找类型）。

### SAM规格

SAMv3_协议必须扩展以支持服务查找。

扩展NAMING LOOKUP如下：

NAMING LOOKUP NAME=example.i2p OPTIONS=true请求在回复中提供选项映射。

当OPTIONS=true时，NAME可以是完整的base64终点。

如果终点查找成功且租约集中有选项，
在回复中，继终点之后，
将会有一个或多个以OPTION:key=value形式的选项。
每个选项将有单独的OPTION:前缀。
包含租约集中的所有选项，而不仅仅是服务记录选项。
例如，未来定义的参数的选项可能存在。
例如：

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

检索到的所有键中包含 '='，以及键或值中包含换行符
的都被视为无效并将从回复中移除。

如果在租约集中找不到任何选项，或者如果租约集是版本1，
则响应将不包括任何选项。

如果查找中OPTIONS=true且找不到租约集，则将返回新结果值LEASESET_NOT_FOUND。

## 名称查找替代方案

考虑了一种替代设计，以支持对服务的完整主机名查找，例如_smtp._tcp.example.i2p，通过更新[NAMING](/docs/overview/naming/)以指定处理以'_'开头的主机名。
这被拒绝的原因有两个：

- 仍然需要I2CP和SAM更改以将TTL和端口信息传递给客户端。
- 这不会成为可以用于检索未来可能定义的其他LS2选项的一般设施。

## 建议

服务器应指定至少为86400的TTL，并且是应用程序的标准端口。

## 高级功能

### 递归查找

支持递归查找可能很有用，其中每个连续的租约集
被检查是否有指向另一个租约集的服务记录，像DNS一样。
这可能不是必要的，至少在初始实现中。

待办

### 特定于应用的字段

在服务记录中包含特定于应用的数据可能是有用的。
例如，example.i2p的运营者可能希望指示邮件应转发至example@mail.i2p。
“example@”部分需要在服务记录的一个单独字段中，
或从目标中剥离。

即使运营者运行自己的邮件服务，他可能希望指出邮件应发送至example@example.i2p。
大多数I2P服务由一个人运行。
因此，这里可能也有一个单独的字段会有所帮助。

待办 以通用方式实现

### 电子邮件的更改

此提案范围之外的问题。参见[DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102)进行讨论。

## 实施注意事项

服务记录的缓存可至TTL，具体取决于由路由器或应用程序实现。
是否持久缓存也依赖于具体实现。

查找还必须查找目标租约集并验证它是否包含"self"记录
，然后再将目标终点返回给客户端。

## 安全分析

由于租约集是签名的，租约集内的任何服务记录通过终点的签名密钥进行身份验证。

除非租约集被加密，服务记录是公开的且对填充路由器可见。
任何请求租约集的路由器将能够看到服务记录。

除"self"之外的SRV记录（即，指向其他主机名/b32目标的记录）
不需要目标主机名/b32的同意。
目前尚不清楚将服务重定向至任意终点是否可能促成某种攻击，或该攻击的目的是什么。
然而，此提案通过要求目标
也发布一个指向自己的"self" SRV记录来缓解此类攻击。实现者必须检查目标的租约集中是否有"self"记录。

## 兼容性

LS2：无问题。所有已知的实现当前都忽略LS2中的选项字段，并正确地跳过非空选项字段。
在LS2开发期间，已经通过Java I2P和i2pd进行测试验证。
LS2于2016年在0.9.38中实现，所有路由器实现均支持良好。
设计不需要特定支持或缓存，也不需要填充路由器的任何改变。

命名：'_'不是i2p主机名中的有效字符。

I2CP：查找类型2-4不应发送到低于支持的最小API版本（TBD）的路由器。

SAM：Java SAM服务器忽略附加的键/值对，如OPTIONS=true。
i2pd也应如此，有待验证。
SAM客户端只有在使用OPTIONS=true请求时才能获取回复中的附加值。
不应需要版本提升。

