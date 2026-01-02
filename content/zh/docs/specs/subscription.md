---
title: "地址订阅源命令"
description: "用于地址簿订阅源的扩展，使主机名持有者能够更新并管理其记录"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## 概述

本规范通过加入命令扩展了 address subscription feed（地址订阅源），使名称服务器能够广播来自主机名持有者的条目更新。最初于[Proposal 112](/proposals/112-addressbook-subscription-feed-commands/)（2014年9月）中提出，于 0.9.26 版（2016年6月）中实现，并已在全网部署，状态为 CLOSED。

该系统自最初实现以来一直保持稳定且未发生变化，并在 I2P 2.10.0（Router API 0.9.65，2025 年 9 月）中继续以相同方式运行。

## 动机

此前，hosts.txt 订阅服务器仅以一种简单的 hosts.txt 格式发送数据：

```
example.i2p=b64destination
```
这种基本格式带来了几个问题：

- 主机名持有者无法更新与其主机名关联的 Destination（I2P 中的目的地标识）（例如，将签名密钥升级到更强的密码学算法类型）。
- 主机名持有者不能任意放弃其主机名。他们必须将相应的 Destination 私钥直接交给新的持有者。
- 无法验证某个子域名由对应的基础主机名控制。目前这仅由某些名称服务器分别强制执行。

## 设计

本规范为 hosts.txt 格式新增了命令行。借助这些命令，名称服务器可以扩展其服务以提供额外功能。实现本规范的客户端可以通过常规订阅流程监听这些功能。

所有命令都必须由相应的 Destination（目的地）签名。这确保只有在主机名持有者提出请求时才会进行更改。

## 安全影响

本规范不影响匿名性。

与丢失对 Destination（目标地址）密钥的控制相关的风险有所增加，因为获得该密钥的人可以使用这些命令对任何关联的主机名进行更改。不过，这并不比现状更糟，在现状下，获得一个 Destination 的人可以冒充某个主机名，并（部分地）接管其流量。通过赋予主机名持有者在认为 Destination 已被攻陷时更改与该主机名关联的 Destination 的能力，可以平衡这种增加的风险。而在当前系统中，这是不可能做到的。

## 规范

### 换行类型

有两种新的线条类型：

1. **Add 和 Change 命令：**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **删除命令：**

```
#!key1=val1#key2=val2...
```
#### 顺序

feed（提要）不一定是有序或完整的。例如，change 命令可能出现在 add 命令之前，或者在没有 add 命令的情况下出现。

键可以以任意顺序出现。不允许存在重复的键。所有键和值都区分大小写。

### 常用密钥

**所有命令都必须包含：**

**sig** : Base64 签名，使用来自目标（Destination）的签名密钥

**对第二个主机名和/或 destination（目标标识）的引用：**

**oldname** : 第二个主机名（新的或已更改的）

**olddest** : 第二个 Base64 destination（I2P 目标标识）（新的或已更改的）

**oldsig** : 第二个 Base64 签名，使用来自 olddest 的签名密钥

**其他常用键：**

**action** : 一个命令

**name** : 主机名，仅当其前面没有 `example.i2p=b64dest` 时才会出现

**dest** : Base64 destination（目标地址），仅当其前面未出现 `example.i2p=b64dest` 时才会出现

**date** : 自 Unix 纪元以来的秒数

**expires** : 自 Unix 纪元起的秒数

### 命令

除“Add”命令外，所有命令必须包含一个`action=command`键/值对。

为兼容旧版客户端，大多数命令前都加上 `example.i2p=b64dest`，如下所述。对于变更，均以新值为准。任何旧值都会包含在键/值部分中。

列出的键是必需的。所有命令可能包含此处未定义的其他键/值项。

#### 添加主机名

**以 example.i2p=b64dest 开头**：是的，这是新的主机名和目标地址。

**action** : 未包含，已隐含。

**sig** : 签名

示例：

```
example.i2p=b64dest#!sig=b64sig
```
#### 更改主机名

**以 example.i2p=b64dest 为前缀** : 是的，这是新的主机名和旧的 destination（目标标识）。

**操作** : changename

**oldname** : 旧的主机名，待替换

**sig** : 签名

示例：

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### 更改目标地址

**前面带有 example.i2p=b64dest** : 是的，这是旧的主机名和新的目标地址。

**action** : changedest

**olddest** : 旧的 Destination（目标地址），将被替换

**oldsig** : 使用 olddest 的签名

**sig** : 签名

示例：

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 添加主机名别名

**以 example.i2p=b64dest 开头** : 是的，这是新的（别名）主机名和旧的 Destination（目的地标识）。

**操作** : addname

**oldname** : 旧的主机名

**sig**：签名

示例：

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### 添加目标地址别名

(用于加密升级)

**以 example.i2p=b64dest 为前缀** : 是的，这是旧的主机名和新的（备用）destination（目标标识）。

**action** : adddest

**olddest** : 旧的目的地

**oldsig** : 使用 olddest 的签名

**sig** : 使用 dest 的签名

示例：

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 添加子域名

**以 subdomain.example.i2p=b64dest 开头** : 是的，这是新的子域名和 destination（目标）。

**操作** : addsubdomain

**oldname** : 更高层级的主机名 (example.i2p)

**olddest** : 更高层级的目标地址（例如 example.i2p）

**oldsig** : 使用 olddest 的签名

**sig** : 使用 dest 的签名

示例：

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 更新元数据

**以 example.i2p=b64dest 为前缀** : 是的，这是旧的主机名和目标地址。

**操作** : 更新

**sig** : 签名

(在此添加任何已更新的密钥)

示例：

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### 移除主机名

**需要以 example.i2p=b64dest 作为前缀** : 不，这些是在选项中指定的

**操作** : 删除

**name** : 主机名

**dest** : 目标

**sig** : 签名

示例：

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### 删除所有与此目标地址（Destination）相关的条目

**以 example.i2p=b64dest 作为前缀** : 否，这些是在选项中指定的

**操作** : removeall

**dest** : 目标

**sig** : 签名

示例：

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### 签名

所有命令必须由对应的 Destination（I2P 中的通信端点标识）签名。包含两个 Destination 的命令可能需要两个签名。

`oldsig` 始终是“内层”签名。在不存在 `oldsig` 或 `sig` 键的情况下进行签名和验证。`sig` 始终是“外层”签名。在存在 `oldsig` 键但不存在 `sig` 键的情况下进行签名和验证。

#### 签名输入

要生成用于创建或验证签名的字节流，请按如下方式序列化：

1. 移除 `sig` 键
2. 如果使用 `oldsig` 进行验证，也移除 `oldsig` 键
3. 仅用于 Add 或 Change 命令，输出 `example.i2p=b64dest`
4. 如果仍有任何键，输出 `#!`
5. 按 UTF-8 键对选项排序，若存在重复键则失败
6. 对每个键/值，输出 `key=value`，然后（如果不是最后一个键/值）再输出一个 `#`

**注意事项**

- 不要输出换行符
- 输出编码为 UTF-8
- 所有 destination（I2P 目的地标识）和签名的编码均为使用 I2P 字母表的 Base 64
- 键和值区分大小写
- 主机名必须为小写

#### 当前签名类型

自 I2P 2.10.0 起，以下用于 Destination（目标标识）的签名类型受支持：

- **EdDSA_SHA512_Ed25519** (Type 7): 自 0.9.15 起在 destinations（目的地）中最常见。使用 32 字节公钥和 64 字节签名。这是新建 destinations 的推荐签名类型。
- **RedDSA_SHA512_Ed25519** (Type 13): 仅适用于 destinations 和加密的 leasesets（自 0.9.39 起）。
- 旧类型（DSA_SHA1、ECDSA 变体）：仍受支持，但自 0.9.58 起针对新的 Router Identities 已弃用。

注意：自 I2P 2.10.0 起，后量子密码学选项已可用，但尚未成为默认的签名类型。

## 兼容性

在 hosts.txt 格式中，所有新增的行都通过行首注释字符（`#!`）实现，因此所有较旧的 I2P 版本都会将这些新命令视为注释并优雅地忽略它们。

当 I2P router 更新到新规范时，它们不会重新解释旧的注释，而会在随后获取其订阅源时开始监听新的命令。因此，名称服务器需要以某种方式持久化命令条目，或启用 ETag 支持，以便 router 能获取过去的所有命令。

## 实现状态

**初始部署:** 版本 0.9.26 (2016 年 6 月 7 日)

**当前状态：** 截至 I2P 2.10.0，稳定且未变化（Router API 0.9.65，2025 年 9 月）

**提案状态：** 已关闭 (已在全网成功部署)

**实现位置：** `apps/addressbook/java/src/net/i2p/addressbook/` 在 I2P Java router 中

**关键类:** - `SubscriptionList.java`: 管理订阅处理 - `Subscription.java`: 处理单个订阅源 - `AddressBook.java`: 地址簿的核心功能 - `Daemon.java`: 地址簿后台服务

**默认订阅 URL:** `http://i2p-projekt.i2p/hosts.txt`

## 传输详细信息

订阅使用支持条件 GET 的 HTTP：

- **ETag 头：** 支持高效的变更检测
- **Last-Modified 头：** 跟踪订阅更新时间
- **304 Not Modified：** 当内容未变更时，服务器应返回此状态
- **Content-Length：** 强烈建议在所有响应中包含该字段

I2P router 使用标准的 HTTP 客户端行为，并提供完善的缓存支持。

## 版本背景

**I2P 版本编号说明：** 自大约 1.5.0 版本（2021 年 8 月）起，I2P 从 0.9.x 的版本编号转为采用语义化版本（1.x、2.x 等）。不过，为了向后兼容，内部的 Router API 版本仍沿用 0.9.x 的编号。截至 2025 年 10 月，当前发布版为 I2P 2.10.0，对应的 Router API 版本为 0.9.65。

本规范文档最初为 0.9.49 版本（2021 年 2 月）编写，并且对当前的 0.9.65 版本（I2P 2.10.0）仍完全适用，因为自从在 0.9.26 中首次实现以来，订阅提要系统未发生任何变更。

## 参考资料

- [提案 112（原文）](/proposals/112-addressbook-subscription-feed-commands/)
- [官方规范](/docs/specs/subscription/)
- [I2P 命名文档](/docs/overview/naming/)
- [通用结构规范](/docs/specs/common-structures/)
- [I2P 源代码仓库](https://github.com/i2p/i2p.i2p)
- [I2P Gitea 仓库](https://i2pgit.org/I2P_Developers/i2p.i2p)

## 相关进展

尽管订阅源系统本身并未改变，I2P 的命名基础设施中以下相关进展可能会引起兴趣：

- **扩展的 Base32 名称** (0.9.40+): 支持加密的 leaseSet 使用 56+ 字符的 base32 地址。不影响订阅源格式。
- **.i2p.alt TLD 注册** (RFC 9476, 2023 年末): GANA 已正式将 .i2p.alt 注册为替代 TLD。未来的 router 更新可能会去除 .alt 后缀，但无需更改订阅命令。
- **后量子密码学** (2.10.0+): 可用但非默认。未来将考虑订阅源中的签名算法。
