---
title: "I2P 威胁模型"
description: "I2P 设计中考虑的攻击目录及其缓解措施"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. "匿名"的含义

I2P 提供*实用匿名性*，而非隐身。匿名性被定义为对手难以获取您希望保密的信息：您是谁、您在哪里或您与谁交流。绝对匿名是不可能的；相反，I2P 旨在在全球被动和主动对手面前提供**足够的匿名性**。

您的匿名性取决于您如何配置 I2P、如何选择节点和订阅，以及您暴露哪些应用程序。

---

## 2. 密码学与传输演进（2003 → 2025）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**当前加密套件 (Noise XK)：** - **X25519** 用于密钥交换   - **ChaCha20/Poly1305 AEAD** 用于加密   - **Ed25519 (EdDSA-SHA512)** 用于签名   - **SHA-256** 用于哈希和 HKDF   - 可选 **ML-KEM 混合模式** 用于后量子测试

所有 ElGamal 和 AES-CBC 的使用已被淘汰。传输完全采用 NTCP2（TCP）和 SSU2（UDP）；两者均支持 IPv4/IPv6、前向保密和 DPI 混淆。

---

## 3. 网络架构概述

- **自由路由混合网络:** 发送者和接收者各自定义自己的 tunnel。  
- **无中心权威:** 路由和命名是去中心化的;每个 router 维护本地信任。  
- **单向 tunnel:** 入站和出站是分开的(10分钟生命周期)。  
- **探索性 tunnel:** 默认2跳; 客户端 tunnel 2-3跳。  
- **Floodfill router:** 约55,000个节点中的约1,700个(约6%)维护分布式 NetDB。  
- **NetDB 轮换:** 密钥空间在UTC午夜每日轮换。  
- **子数据库隔离:** 自2.4.0版本起,每个客户端和 router 使用单独的数据库以防止关联。

---

## 4. 攻击类别与现有防御措施

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. 现代网络数据库（NetDB）

**核心事实（仍然准确）：** - 修改版 Kademlia DHT 存储 RouterInfo 和 LeaseSet。   - SHA-256 密钥哈希；向 2 个最近的 floodfill 并行查询，超时时间为 10 秒。   - LeaseSet 生命周期约为 10 分钟（LeaseSet2）或 18 小时（MetaLeaseSet）。

**新类型(自 0.9.38 起):** - **LeaseSet2 (类型 3)** – 支持多种加密类型,带时间戳。   - **EncryptedLeaseSet2 (类型 5)** – 用于私密服务的盲化目标地址(DH 或 PSK 认证)。   - **MetaLeaseSet (类型 7)** – 多宿主和扩展过期时间。

**重大安全升级 – Sub-DB 隔离 (2.4.0)：** - 防止 router 与客户端关联。   - 每个客户端和 router 使用独立的 netDb 分段。   - 已验证和审计 (2.5.0)。

---

## 6. 隐藏模式和受限路由

- **Hidden Mode（隐藏模式）：** 已实现（根据自由之家评分在严格国家自动启用）。  
    Router 不发布 RouterInfo 或转发流量。  
- **Restricted Routes（受限路由）：** 部分实现（仅基本的信任节点 tunnel）。  
    全面的可信对等节点路由仍在计划中（3.0+）。

权衡：更好的隐私 ↔ 减少对网络容量的贡献。

---

## 7. DoS 和 Floodfill 攻击

**历史背景：** 2013年加州大学圣巴巴拉分校的研究表明Eclipse攻击和Floodfill接管是可能的。**现代防御措施包括：** - 每日密钥空间轮换。 - Floodfill上限约500个，每个/16网段一个。 - 随机化存储验证延迟。 - 优先选择较新的router（2.6.0版本）。 - 自动注册修复（2.9.0版本）。 - 拥塞感知路由和lease节流（2.4.0+版本）。

Floodfill 攻击在理论上仍然可能,但在实践中更加困难。

---

## 8. 流量分析与审查

I2P 流量难以识别:没有固定端口,没有明文握手,并且使用随机填充。NTCP2 和 SSU2 数据包模仿常见协议并使用 ChaCha20 头部混淆。填充策略是基础的(随机大小),虚拟流量未实现(成本高)。自 2.6.0 版本起阻止来自 Tor 出口节点的连接(以保护资源)。

---

## 9. 持久性限制（已确认）

- 低延迟应用的时间关联攻击仍然是一个基本风险。
- 针对已知公共目的地的交集攻击依然强大。
- Sybil 攻击缺乏完整防御(HashCash 未强制执行)。
- 恒定速率流量和非平凡延迟仍未实现(计划于 3.0 版本)。

关于这些限制的透明性是有意为之的——它可以防止用户高估匿名性。

---

## 10. 网络统计 (2025)

- 全球约 55,000 个活跃 router（2013 年时为 7,000 个，呈上升趋势）
- 约 1,700 个 floodfill router（占比约 6%）
- 默认情况下 95% 参与 tunnel 路由
- 带宽等级：K（<12 KB/s）→ X（>2 MB/s）
- Floodfill 最低速率要求：128 KB/s
- Router 控制台需要 Java 8+（必需），下一周期计划支持 Java 17+

---

## 11. 开发与核心资源

- 官方网站：[geti2p.net](/)
- 文档：[Documentation](/docs/)  
- Debian 仓库：<https://deb.i2pgit.org>（2023年10月替代了 deb.i2p2.de）  
- 源代码：<https://i2pgit.org/I2P_Developers/i2p.i2p>（Gitea）+ GitHub 镜像  
- 所有发布版本均为签名的 SU3 容器（RSA-4096，zzz/str4d 密钥）  
- 无活跃邮件列表；社区通过 <https://i2pforum.net> 和 IRC2P 交流。  
- 更新周期：每 6-8 周发布稳定版本。

---

## 12. 自 0.8.x 以来的安全改进总结

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. 已知未解决或计划中的工作

- 全面的受限路由(可信对等节点路由) → 计划3.0版本。
- 用于抵抗时序分析的非平凡延迟/批处理 → 计划3.0版本。
- 高级填充和虚拟流量 → 未实现。
- HashCash身份验证 → 基础设施已存在但未激活。
- R5N DHT替代方案 → 仅有提案。

---

## 14. 重要参考资料

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [I2P 官方文档](/docs/)

---

## 15. 结论

I2P的核心匿名模型已经坚持了二十年：为了本地信任和安全性而放弃全局唯一性。从ElGamal到X25519，从NTCP到NTCP2，从手动reseed到Sub-DB隔离，该项目在不断演进的同时始终保持其深度防御和透明性的理念。

许多针对任何低延迟混合网络的攻击在理论上仍然是可能的,但 I2P 的持续加固使它们变得越来越不切实际。该网络比以往任何时候都更大、更快、更安全——但仍然坦诚地面对其局限性。
