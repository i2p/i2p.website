---
title: "命名与地址簿"
description: "I2P 如何将人类可读的主机名映射到目标地址"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P 地址是长的加密密钥。命名系统在这些密钥之上提供了一个更友好的层，**而不引入中央权威机构**。所有名称都是**本地的**——每个 router 独立决定主机名指向哪个目的地。

> **需要背景知识？** [命名讨论](/docs/legacy/naming/)文档记录了原始设计辩论、替代方案以及 I2P 去中心化命名背后的哲学基础。

---

## 1. 组件

I2P 的命名层由几个独立但相互协作的子系统组成：

1. **命名服务** – 将主机名解析为 destination，并处理 [Base32 主机名](#base32-hostnames)。
2. **HTTP 代理** – 将 `.i2p` 查询传递给 router，并在名称未知时建议跳转服务。
3. **主机添加服务** – 以 CGI 样式表单将新条目追加到本地地址簿中。
4. **跳转服务** – 远程辅助工具，为提供的主机名返回 destination。
5. **地址簿** – 使用本地信任的"信任网络"定期获取并合并远程主机列表。
6. **SusiDNS** – 基于网页的用户界面，用于管理地址簿、订阅和本地覆盖设置。

这种模块化设计让用户可以定义自己的信任边界，并根据自己的偏好自动化命名过程的多少部分。

---

## 2. 命名服务

router的命名API（`net.i2p.client.naming`）通过可配置属性`i2p.naming.impl=<class>`支持多个后端。每个实现可能提供不同的查找策略，但都共享相同的信任和解析模型。

### 2.1 Hosts.txt (legacy format)

传统模式使用三个按顺序检查的纯文本文件：

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

每一行存储一个 `hostname=base64-destination` 映射。这种简单的文本格式仍然完全支持导入/导出,但由于在主机列表超过几千个条目后性能较差,它不再是默认格式。

---

### 2.2 Blockfile Naming Service (default backend)

在 **0.8.8 版本**中引入的 Blockfile 命名服务现在是默认后端。它用基于跳表(skiplist)的高性能磁盘键值存储(`hostsdb.blockfile`)替代了平面文件,实现了大约 **10 倍**的查找速度提升。

**主要特点：** - 在一个二进制数据库中存储多个逻辑地址簿（私有、用户和hosts）。- 保持与传统hosts.txt导入/导出的兼容性。- 支持反向查找、元数据（添加日期、来源、注释）和高效缓存。- 使用相同的三层搜索顺序：私有 → 用户 → hosts。

这种方法在保持向后兼容性的同时,显著提高了解析速度和可扩展性。

---

### 2.1 Hosts.txt（传统格式）

开发者可以实现自定义后端，例如：- **Meta** – 聚合多个命名系统。- **PetName** – 支持存储在 `petnames.txt` 中的 petname（个人名称）。- **AddressDB**、**Exec**、**Eepget** 和 **Dummy** – 用于外部或后备解析。

blockfile 实现仍然是通用场景下**推荐**的后端，因为其性能和可靠性表现出色。

---

## 3. Base32 Hostnames

Base32 主机名（`*.b32.i2p`）的功能类似于 Tor 的 `.onion` 地址。当你访问一个 `.b32.i2p` 地址时：

1. router 解码 Base32 载荷。
2. 它直接从密钥重建目标地址——**无需地址簿查找**。

这保证了即使不存在可读性好的主机名，仍然可以访问。在**0.9.40 版本**中引入的扩展 Base32 名称支持 **LeaseSet2** 和加密目的地。

---

## 4. Address Book & Subscriptions

地址簿应用程序通过 HTTP 获取远程主机列表,并根据用户配置的信任规则在本地合并它们。

### 2.2 Blockfile 命名服务（默认后端）

- 订阅是指向 `hosts.txt` 或增量更新源的标准 `.i2p` URL。
- 更新会定期获取(默认每小时一次)并在合并前进行验证。
- 冲突按照**先到先得**原则解决,遵循以下优先级顺序:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`。

#### Default Providers

自 **I2P 2.3.0 (2023年6月)** 起,包含两个默认的订阅提供者: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

这种冗余提高了可靠性,同时保留了本地信任模型。用户可以通过 SusiDNS 添加或删除订阅。

#### Incremental Updates

增量更新通过 `newhosts.txt` 获取(取代了旧的 `recenthosts.cgi` 概念)。此端点提供高效的基于 **ETag** 的增量更新——仅返回自上次请求以来的新条目,或在未更改时返回 `304 Not Modified`。

---

### 2.3 替代后端和插件

- **Host-add services**（`add*.cgi`）允许手动提交名称到目标地址的映射。在接受之前始终验证目标地址。
- **Jump services** 使用适当的密钥响应，并可以通过 HTTP 代理使用 `?i2paddresshelper=` 参数进行重定向。
  常见示例：`stats.i2p`、`identiguy.i2p` 和 `notbob.i2p`。
  这些服务**不是可信权威机构**——用户必须自行决定使用哪个服务。

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS 可在以下地址访问：`http://127.0.0.1:7657/susidns/`

您可以：- 查看和编辑本地地址簿。- 管理和设置订阅优先级。- 导入/导出主机列表。- 配置获取计划。

**I2P 2.8.1 新增功能（2025年3月）：** - 添加了"按最新排序"功能。 - 改进了订阅处理（修复了 ETag 不一致问题）。

所有更改都保持**本地**——每个 router 的地址簿都是唯一的。

---

## 3. Base32 主机名

根据 RFC 9476，I2P 已于 **2025 年 3 月（I2P 2.8.1）** 向 GNUnet 编号分配机构（GANA）注册了 **`.i2p.alt`**。

**目的：** 防止配置错误的软件意外泄露 DNS 信息。

- 符合 RFC 9476 标准的 DNS 解析器**不会转发** `.alt` 域名到公共 DNS。
- I2P 软件将 `.i2p.alt` 视为等同于 `.i2p`,在解析过程中会去除 `.alt` 后缀。
- `.i2p.alt` **并非**旨在取代 `.i2p`;它是一种技术保障措施,而非品牌重塑。

---

## 4. 地址簿与订阅

- **Destination 密钥：** 516–616 字节（Base64）  
- **主机名：** 最多 67 个字符（包括 `.i2p`）  
- **允许的字符：** a–z、0–9、`-`、`.`（不允许连续两个点，不允许大写字母）  
- **保留：** `*.b32.i2p`  
- **ETag 和 Last-Modified：** 积极使用以最小化带宽消耗  
- **平均 hosts.txt 大小：** 约 800 个主机占用约 400 KB（示例数据）  
- **带宽使用：** 如果每 12 小时获取一次，约 10 字节/秒

---

## 8. Security Model and Philosophy

I2P 有意牺牲全局唯一性以换取去中心化和安全性——这是 **Zooko's Triangle（佐科三角）** 的直接应用。

**核心原则：** - **无中心化权威：** 所有查询都在本地进行。   - **抵御 DNS 劫持：** 查询使用目标公钥加密。   - **防止女巫攻击：** 无投票或基于共识的命名机制。   - **不可变映射：** 一旦本地关联建立，就无法被远程覆盖。

基于区块链的命名系统（例如 Namecoin、ENS）已经探索过解决佐科三角的全部三个方面，但 I2P 有意避免使用它们，原因是延迟、复杂性以及与其本地信任模型在理念上不兼容。

---

## 9. Compatibility and Stability

- 在 2023–2025 年间，没有任何命名功能被弃用。
- Hosts.txt 格式、跳转服务、订阅以及所有命名 API 实现均保持功能正常。
- I2P 项目在引入性能和安全改进（NetDB 隔离、Sub-DB 分离等）的同时，严格保持**向后兼容性**。

---

## 10. Best Practices

- 仅保留可信的订阅源；避免使用大型、未知的主机列表。
- 在升级或重新安装之前备份 `hostsdb.blockfile` 和 `privatehosts.txt`。
- 定期检查跳转服务并禁用任何你不再信任的服务。
- 请记住：你的地址簿定义了你所看到的 I2P 世界——**每个主机名都是本地的**。

---

### Further Reading

- [命名讨论](/docs/legacy/naming/)  
- [Blockfile 规范](/docs/specs/blockfile/)  
- [配置文件格式](/docs/specs/configuration/)  
- [命名服务 Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
