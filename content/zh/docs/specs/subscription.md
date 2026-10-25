---
title: "地址簿订阅源命令"
description: "扩展地址订阅源规范，通过命令使域名服务器能够广播来自主机名持有者的条目更新。"
slug: "subscription"
aliases:
  - "/zh/docs/specs/subscription-spec"
  - "/zh/docs/specs/subscription-spec/"
category: "格式"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## 概述

此规范通过命令扩展了地址订阅源，使名称服务器能够广播来自主机名持有者的条目更新。在 0.9.26 版本中实现，最初在提案 112 中提出。

## 动机

之前，hosts.txt 订阅服务器只是以 hosts.txt 格式发送数据，格式如下：

```
example.i2p=b64destination
```
这样做存在几个问题：

- 主机名持有者无法更新与其主机名关联的 Destination（例如，将签名密钥升级为更强的类型）。
- 主机名持有者不能任意放弃其主机名；他们必须将相应的 Destination 私钥直接交给新持有者。
- 无法验证子域名是否由相应的基础主机名控制；这目前仅由一些域名服务器单独执行。

## 设计

本规范为 hosts.txt 格式添加了多个命令行。通过这些命令，域名服务器可以扩展其服务以提供多项附加功能。实现本规范的客户端将能够通过常规订阅过程监听这些功能。

所有命令行都必须由相应的 Destination 签名。这确保了只有在主机名持有者的请求下才会进行更改。

## 安全影响

此规范不会影响匿名性。

失去 Destination 密钥控制权的相关风险会增加，因为获得密钥的人可以使用这些命令对任何关联的主机名进行更改。但这并不比现状更严重，在现状下，获得 Destination 的人可以冒充主机名并（部分）接管其流量。增加的风险也通过给予主机名持有者更改与主机名关联的 Destination 的能力而得到平衡，以防他们认为 Destination 已被泄露；这在当前系统中是不可能的。

## 规范

### 新行类型

有两种新的行类型：

1. 添加和更改命令：

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. 移除命令：

   ```
   #!key1=val1#key2=val2 ...
   ```
#### 排序

数据流不一定是按顺序或完整的。例如，更改命令可能出现在添加命令之前的行，或者没有添加命令。

键可以按任意顺序排列。不允许重复的键。所有键和值都区分大小写。

### 常用密钥

所有命令中必需的：

**sig** : B64 签名，使用来自目标地址的签名密钥

对第二个主机名和/或目标的引用：

**oldname** : 第二个主机名（新的或已更改的）

**olddest** : 第二个 b64 目标地址（新的或已更改的）

**oldsig** : 第二个 b64 签名，使用来自 olddest 的签名密钥

其他常用键：

**action** : 一个命令

**name** : 主机名，仅在前面没有 `example.i2p=b64dest` 时才存在

**dest**：b64 destination，仅在未以 `example.i2p=b64dest` 开头时出现

**date** : 自纪元开始的秒数

**expires** : 从纪元开始的秒数

### 命令

除了"Add"命令之外，所有命令都必须包含一个 `action=command` 键值对。

为了与旧版客户端兼容，大多数命令都以 `example.i2p=b64dest` 为前缀，如下所述。对于更改操作，这些始终是新值。任何旧值都包含在键/值部分中。

列出的键是必需的。所有命令都可能包含此处未定义的其他键/值项。

#### 添加主机名

**以 example.i2p=b64dest 开头**：是的，这是新的主机名和目标地址。

**action** : 不包含，这是隐含的。

**sig** : 签名

示例：

```
example.i2p=b64dest#!sig=b64sig
```
#### 更改主机名

**以 example.i2p=b64dest 开头**：是的，这是新的主机名和旧的目标地址。

**action** : changename

**oldname** : 要被替换的旧主机名

**sig** : 签名

示例：

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### 更改目标

**以 example.i2p=b64dest 开头**：是的，这是旧的主机名和新的目标地址。

**action** : changedest

**olddest** : 旧的目标地址，将被替换

**oldsig** : 使用 olddest 的签名

**sig** : 签名

示例：

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 添加主机名别名

**前面是 example.i2p=b64dest**：是的，这是新的（别名）主机名和旧的目标地址。

**action** : addname

**oldname** : 旧主机名

**sig** : 签名

示例：

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### 添加目标地址别名

（用于加密升级）

**前面带有 example.i2p=b64dest**：是的，这是旧主机名和新的（备用）destination。

**action** : adddest

**olddest** : 旧目标地址

**oldsig** : 使用 olddest 的签名

**sig** : 使用目标地址的签名

示例：

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 添加子域名

**前面有 subdomain.example.i2p=b64dest**：是的，这是新的主机子域名和目标地址。

**action** : addsubdomain

**oldname** : 高级域名 (example.i2p)

**olddest** : 更高级别的目标地址（例如 example.i2p）

**oldsig** : 使用 olddest 的签名

**sig** : 使用 dest 的签名

示例：

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 更新元数据

**以 example.i2p=b64dest 开头**：是的，这是旧的主机名和目标地址。

**action** : update

**sig** : 签名

(在此处添加任何更新的密钥)

示例：

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### 移除主机名

**前面加上 example.i2p=b64dest**：否，这些在选项中指定

**action** : remove

**name** : 主机名

**dest** : 目标地址

**sig** : 签名

示例：

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### 删除此目标的所有项

**前面有 example.i2p=b64dest**：不，这些在选项中指定

**action** : removeall

**name** : 旧主机名，仅供参考

**dest** : 旧的dest，所有使用此dest的都会被删除

**sig** : 签名

示例：

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### 签名

所有命令都必须包含一个签名键值对 `sig=b64signature`，其中签名是使用目标签名密钥对其他数据进行签名的结果。

对于包含旧目标和新目标的命令，还必须包含 `oldsig=b64signature`，以及 oldname、olddest 或两者。

在添加或更改命令中，用于验证的公钥位于要添加或更改的目标地址中。

在某些添加或编辑命令中，可能会引用额外的目标地址，例如添加别名或更改目标地址或主机名时。在这种情况下，必须包含第二个签名，并且两个签名都应该被验证。第二个签名是"内部"签名，首先进行签名和验证（排除"外部"签名）。客户端应该采取必要的额外措施来验证和接受更改。

oldsig 始终是"内部"签名。在没有 'oldsig' 或 'sig' 键的情况下进行签名和验证。sig 始终是"外部"签名。在存在 'oldsig' 键但不存在 'sig' 键的情况下进行签名和验证。

#### 签名的输入

要生成用于创建或验证签名的字节流，请按以下方式序列化：

- 移除 "sig" 键
- 如果使用 oldsig 验证，还要移除 "oldsig" 键
- 仅对于 Add 或 Change 命令，输出 `example.i2p=b64dest`
- 如果还有剩余的键，输出 `#!`
- 按 UTF-8 键排序选项，如有重复键则失败
- 对于每个键/值对，输出 `key=value`，然后（如果不是最后一个键/值对）跟一个 `#`

注意事项：

- 不要输出换行符
- 输出编码为 UTF-8
- 所有目标和签名编码都使用 I2P 字母表的 Base 64 格式
- 键和值区分大小写
- 主机名必须为小写

## 兼容性

hosts.txt 格式中的所有新行都使用前导注释字符实现，因此所有较旧的 I2P 版本都会将新命令解释为注释。

当 I2P router 升级到新规范时，它们不会重新解释旧的注释，但会在后续获取订阅源时开始监听新命令。因此，名称服务器以某种方式持久化命令条目，或启用 etag 支持以便 router 可以获取所有过去的命令是很重要的。
