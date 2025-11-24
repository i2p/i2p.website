---
title: "通讯录订阅提要命令"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "关闭"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## 注意
网络部署已完成。
请参阅 [SPEC](/docs/specs/subscription/) 获取官方规范。

## 概述

本提案旨在为地址订阅提要扩展命令，使名称服务器能够广播来自主机名持有者的条目更新。
已在 0.9.26 中实现。

## 动机

目前，hosts.txt 订阅服务器只是以 hosts.txt 格式发送数据，格式如下:

    ```text
    example.i2p=b64destination
    ```

这存在几个问题：

- 主机名持有者无法更新与其主机名关联的目的地（例如，为了升级签名密钥到更强类型）。
- 主机名持有者不能任意放弃他们的主机名；他们必须将相应的目的地私钥直接交给新拥有者。
- 无法验证子域名是否由相应的基本主机名控制；目前这只由某些名称服务器单独强制执行。

## 设计

此提案为 hosts.txt 格式添加了一些命令行。通过这些命令，名称服务器可以扩展其服务以提供许多附加功能。实现该提案的客户端将能够通过常规订阅过程收听这些功能。

所有命令行必须由相应的目的地签名。这确保了更改只有在主机名持有者的请求下才能进行。

## 安全影响

本提案对匿名性没有影响。

由于获得目的地密钥的人可以使用这些命令更改任何相关主机名，因此丢失目的地密钥的风险有所增加。但这并不比现状更严重，现状下，获得目的地的人可以假冒主机名并（部分）接管其流量。增加的风险也由于赋予主机名持有者更改与主机名关联的目的地的能力而得到平衡，以防他们认为目的地已被泄露；这在当前系统中是不可能的。

## 规范

### 新行类型

此提案增加了两种新行类型：

1. 添加和更改命令:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. 删除命令:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### 顺序
提要不一定是有顺序或完整的。例如，更改命令可以在添加命令之前的行上，或者没有添加命令。

键可以是任意顺序。不允许重复的键。所有键和值都区分大小写。

### 常用键

所有命令中必需的：

sig
  使用来自目的地的签名密钥的 B64 签名

引用第二个主机名和/或目的地：

oldname
  第二个主机名（新的或已更改的）
olddest
  第二个 b64 目的地（新的或已更改的）
oldsig
  使用来自 nolddest 的签名密钥的第二个 b64 签名

其他常用键：

action
  一条命令
name
  主机名，仅在未由 example.i2p=b64dest 前缀的情况下出现
dest
  b64 目的地，仅在未由 example.i2p=b64dest 前缀的情况下出现
date
  自纪元以来的秒数
expires
  自纪元以来的秒数

### 命令

除“添加”命令外，所有命令都必须包含一个“action=command”键/值。

为与旧版客户端兼容，大多数命令都由 example.i2p=b64dest 前缀，如下所述。对于更改，这些始终是新值。任何旧值都包含在键/值部分中。

列出的键是必需的。所有命令可能包含此处未定义的附加键/值条目。

#### 添加主机名
由 example.i2p=b64dest 前缀
  是的，这是新的主机名和目的地。
action
  不包含，隐含。
sig
  签名

示例:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### 更改主机名
由 example.i2p=b64dest 前缀
  是的，这是新的主机名和旧的目的地。
action
  changename
oldname
  要替换的旧主机名
sig
  签名

示例:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### 更改目的地
由 example.i2p=b64dest 前缀
  是的，这是旧的主机名和新的目的地。
action
  changedest
olddest
  要替换的旧目的地
oldsig
  使用 olddest 的签名
sig
  签名

示例:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 添加主机名别名
由 example.i2p=b64dest 前缀
  是的，这是新的（别名）主机名和旧的目的地。
action
  addname
oldname
  旧主机名
sig
  签名

示例:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### 添加目的地别名
（用于加密升级）

由 example.i2p=b64dest 前缀
  是的，这是旧的主机名和新的（替代）目的地。
action
  adddest
olddest
  旧的目的地
oldsig
  使用 olddest 的签名
sig
  使用 dest 的签名

示例:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 添加子域
由 subdomain.example.i2p=b64dest 前缀
  是的，这是新的主机子域名和目的地。
action
  addsubdomain
oldname
  更高级别的主机名（例如 example.i2p）
olddest
  更高级别的目的地（例如 example.i2p）
oldsig
  使用 olddest 的签名
sig
  使用 dest 的签名

示例:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 更新元数据
由 example.i2p=b64dest 前缀
  是的，这是旧的主机名和目的地。
action
  update
sig
  签名

（在此添加任何更新的键）

示例:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### 删除主机名
由 example.i2p=b64dest 前缀
  否，这些在选项中指定
action
  remove
name
  主机名
dest
  目的地
sig
  签名

示例:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### 删除与此目的地相关的所有
由 example.i2p=b64dest 前缀
  否，这些在选项中指定
action
  removeall
name
  旧主机名，仅作参考
dest
  旧的目的地，所有与此目的地相关的都将被删除
sig
  签名

示例:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

### 签名

所有命令必须包含签名键/值 “sig=b64signature”，使用目的地签名密钥对其他数据签名。

对于包含旧和新目的地的命令，必须还包括 oldsig=b64signature，并且要有 oldname、olddest 或两者。

在添加或更改命令中，验证的公钥位于要添加或更改的目的地。

在一些添加或编辑命令中，可能会引用一个额外的目的地，例如添加别名或更改目的地或主机名时。在这种情况下，必须包含第二个签名，并且两个签名都应被验证。第二个签名是“内部”签名，首先对其进行签名和验证（不包括“外部”签名）。客户端应采取任何必要的附加措施来验证和接受更改。

oldsig 始终是“内部”签名。在签名和验证时，不包含 'oldsig' 或 'sig' 键。sig 始终是“外部”签名。在包含 'oldsig' 键进行签名和验证时，不包含 'sig' 键。

#### 签名输入
为了生成字节流以创建或验证签名，请按以下方式序列化：

- 删除 "sig" 键
- 如果使用 oldsig 验证，还要删除 "oldsig" 键
- 仅用于添加或更改命令，
  输出 example.i2p=b64dest
- 如果存在任何键，输出 "#!"
- 按 UTF-8 键排序选项，如果发现重复键则失败
- 对于每个键/值，输出 key=value，后跟 '#'（如果不是最后一个键/值）

注意

- 不要输出换行符
- 输出编码为 UTF-8
- 所有目的地和签名编码为使用 I2P 字母表的 Base 64
- 键和值区分大小写
- 主机名必须为小写

## 兼容性

hosts.txt 格式中的所有新行均通过前导注释字符实现，因此所有旧版 I2P 版本会将新命令解释为注释。

当 I2P 路由器更新到新规范后，他们不会重新解释旧的注释，而会开始在后续获取订阅提要时监听新命令。因此，名称服务器必须以某种方式持久化命令条目，或启用 etag 支持，使路由器能够获取所有过去的命令。

