---
title: "访问过滤器格式"
description: "tunnel 访问控制过滤器文件的语法"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

访问过滤器使 I2PTunnel 服务器运营者能够基于源 Destination（I2P 端点标识）以及最近的连接频率，允许、拒绝或限流入站连接。该过滤器是一个由规则组成的纯文本文件。文件自上而下读取，**第一个匹配的规则生效**。

> 过滤器定义的更改将在 **tunnel 重启时** 生效。某些构建可能会在运行时重新读取基于文件的列表，但请预期需要重启以确保更改被应用。

## 文件格式

- 每行一条规则。  
- 空行会被忽略。  
- `#` 表示注释，直至行尾。  
- 规则按顺序评估；采用第一个匹配。

## 阈值

**阈值**定义了在滚动时间窗口内，允许来自单个 Destination（I2P 端点标识）的连接尝试次数。

- **数值：** `N/S` 表示每 `S` 秒允许 `N` 个连接。例如：`15/5` 表示每 5 秒最多允许 15 个连接。在该时间窗口内，第 `N+1` 次尝试将被拒绝。  
- **关键字：** `allow` 表示不限制。`deny` 表示始终拒绝。

## 规则语法

规则采用以下形式：

```
<threshold> <scope> <target>
```
其中：

- `<threshold>` 是 `N/S`、`allow` 或 `deny`  
- `<scope>` 是 `default`、`explicit`、`file` 或 `record` 之一（见下文）  
- `<target>` 取决于作用域

### 默认规则

当没有其他规则匹配时生效。仅允许 **一条** 默认规则。如果省略，则未知的 Destination（目标地址）将被允许且不受限制。

```
15/5 default
allow default
deny default
```
### 显式规则

通过 Base32 地址（例如 `example1.b32.i2p`）或完整密钥来定位特定的 Destination（目标标识）。

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### 基于文件的规则

针对外部文件中列出的**所有** Destination（目标标识）。每行包含一个 Destination；允许 `#` 注释和空行。

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> 操作提示：某些实现会定期重新读取文件列表。如果你在 tunnel 运行期间编辑列表，变更被检测到前可能会有短暂延迟。重启即可立即生效。

### 录音器（渐进式控制）

一个**记录器**会监控连接尝试，并将超过阈值的 Destinations（I2P 中的目的地标识）写入文件。然后你可以在 `file` 规则中引用该文件，以对后续尝试施加限速或阻止。

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> 在依赖它之前，先确认你的构建对记录器的支持。使用 `file` 列表以保证行为一致。

## 求值顺序

先把具体规则放在前面，再放通用规则。一种常见的模式：

1. 对受信任的对等节点的显式允许  
2. 对已知滥用者的显式拒绝  
3. 基于文件的允许/拒绝列表  
4. 用于渐进式限速的记录器  
5. 作为兜底的默认规则

## 完整示例

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## 实现说明

- 访问过滤器在 tunnel 层运行，在应用处理之前，因此可以尽早拒绝滥用流量。  
- 将过滤器文件放到你的 I2PTunnel 配置目录中，并重启该 tunnel 以应用更改。  
- 如果你希望跨服务保持一致的策略，可以在多个 tunnel 之间共享基于文件的列表。
