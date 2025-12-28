---
title: "Blockfile（块文件）规范"
description: "I2P 用于主机名解析的基于磁盘的 blockfile（块文件）存储格式"
slug: "blockfile"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 概述

本文档规定了 **I2P blockfile（块文件）文件格式**，以及由 **Blockfile Naming Service（Blockfile 命名服务）** 使用的 `hostsdb.blockfile` 中的表。   背景信息参见 [I2P 命名与地址簿](/docs/overview/naming)。

blockfile（块文件格式）以紧凑的二进制格式实现了**快速查找目标地址**。   与传统的 `hosts.txt` 系统相比：

- Destinations（目标地址）以二进制形式存储，而非 Base64。  
- 可附加任意元数据（例如：添加日期、来源、注释）。  
- 查找时间大约快 **10×**。  
- 磁盘使用量会小幅增加。

blockfile（块文件）是一种以**跳表**实现、存储在磁盘上的已排序映射（键值对）集合。它源自 [Metanotion Blockfile Database](http://www.metanotion.net/software/sandbox/block.html)。本规范首先定义文件结构，然后说明 `BlockfileNamingService` 如何使用它。

> Blockfile Naming Service（Blockfile 命名服务）在 **I2P 0.8.8** 中取代了旧的 `hosts.txt` 实现。   > 初始化时，它会从 `privatehosts.txt`、`userhosts.txt` 和 `hosts.txt` 中导入条目。

---

## Blockfile 格式

该格式由**1024 字节的页面**组成，每个页面前都有一个用于完整性校验的**魔数**。   页面从 1 开始编号：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Page</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Superblock (starts at byte 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Metaindex skiplist (starts at byte 1024)</td>
    </tr>
  </tbody>
</table>
所有整数使用**网络字节序（大端）**。   2 字节的值为无符号；4 字节的值（页号）为有符号，且必须为正数。

> **线程模型：** 该数据库设计为**单线程访问**；`BlockfileNamingService` 提供同步机制。

---

### 超级块格式

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number <code>0x3141de493250</code> (<code>"1A"</code> <code>0xde</code> <code>"I2P"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major version <code>0x01</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version <code>0x02</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File length (in bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag (<code>0x01</code> = yes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (max key/value pairs per span, 16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Page size (as of v1.2; 1024 before that)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### 跳表块页格式

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x536b69704c697374</code> (<code>"SkipList"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (total keys, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Spans (total spans, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Levels (total levels, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (as of v1.2; used for new spans)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### 跳级块页格式

每个层级都有其跨度，但并非所有跨度都对应某个层级。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x42534c6576656c73</code> (<code>"BSLevels"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages (<code>current height</code> × 4 bytes, lowest first)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remaining bytes unused</td>
    </tr>
  </tbody>
</table>
---

### 跳过、跨度、块、页面格式

键/值对在所有 span（区段）中按键排序。非第一个 span 不得为空。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x5370616e</code> (<code>"Span"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys (16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (current keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Span Continuation Block 页面格式

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x434f4e54</code> (<code>"CONT"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### 键值结构格式

键和值的**长度字段不得跨页**（全部 4 个字节必须位于同一页内）。   如果剩余空间不足，则最多填充 3 个字节，并在下一页的偏移 8 处继续。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Value length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key data → Value data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max length = 65535 bytes each</td>
    </tr>
  </tbody>
</table>
---

### 空闲列表块页格式

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x2366724c69737423</code> (<code>"#frList#"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages (0 – 252)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Free page numbers (4 bytes each)</td>
    </tr>
  </tbody>
</table>
---

### 空闲页块格式

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x7e2146524545217e</code> (<code>"~!FREE!~"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### 元索引

位于第 2 页。   映射 **US-ASCII 字符串** → **4 字节整数**。   键为跳表名称；值为页面索引。

---

## Blockfile（块文件）命名服务数据表

该服务定义了若干个跳表。每个 span（区段）最多支持 16 个条目。

---

### 属性跳表

`%%__INFO__%%` 包含一个条目：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>info</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A Properties object (UTF-8 String / String map) serialized as a Mapping</td>
    </tr>
  </tbody>
</table>
典型字段：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>version</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"4"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>created</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>upgraded</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch, since DB v2)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>lists</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma-separated host DBs (e.g. <code>privatehosts.txt,userhosts.txt,hosts.txt</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>listversion_*</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version of each DB (used to detect partial upgrades, since v4)</td>
    </tr>
  </tbody>
</table>
---

### 反向查找跳表

`%%__REVERSE__%%` 包含 **Integer → Properties** 条目（自 DB v2 起）。

- **Key:** Destination（I2P 目的地标识）的 SHA-256 哈希的前 4 字节。  
- **Value:** Properties 对象（序列化的 Mapping）。  
- 多个条目用于处理哈希冲突和多主机名的 Destination。  
- 每个属性 key = 主机名；value = 空字符串。

---

### 主机数据库跳表

每个 `hosts.txt`、`userhosts.txt` 和 `privatehosts.txt` 都将主机名映射到 Destination（I2P 目的地）。

版本 4 支持每个主机名对应多个 Destination（目标标识）（在 **I2P 0.9.26** 中引入）。   版本 3 的数据库会自动迁移。

#### 密钥

UTF-8 字符串 (主机名，小写，以 `.i2p` 结尾)

#### 值

- **版本 4：**  
  - 1 字节，表示属性/目的地对的数量  
  - 对于每一对：属性 → 目的地 (二进制)
- **版本 3：**  
  - 属性 → 目的地 (二进制)

#### DestEntry 属性

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>a</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Time added (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>m</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Last modified (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>notes</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User comments</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>s</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Source (file or subscription URL)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>v</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verified (<code>true</code>/<code>false</code>)</td>
    </tr>
  </tbody>
</table>
---

## 实现说明

Java 类 `BlockfileNamingService` 实现了本规范。

- 在 router 上下文之外，数据库将以**只读**方式打开，除非设置了 `i2p.naming.blockfile.writeInAppContext=true`。  
- 不适用于多实例或多 JVM 访问。  
- 维护三个主要的映射（`privatehosts`、`userhosts`、`hosts`），以及一个用于快速查找的反向映射。

---

## 参考资料

- [I2P 命名与地址簿文档](/docs/overview/naming/)  
- [通用结构规范](/docs/specs/common-structures/)  
- [Metanotion Blockfile（块文件）数据库](http://www.metanotion.net/software/sandbox/block.html)  
- [BlockfileNamingService JavaDoc](https://geti2p.net/javadoc/i2p/naming/BlockfileNamingService.html)
