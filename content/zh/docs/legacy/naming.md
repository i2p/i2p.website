---
title: "命名讨论"
description: "关于 I2P 命名模型的历史性争论，以及为何拒绝了类 DNS 的全局方案"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **背景：** 本页汇集并存档了 I2P 早期设计阶段的长期争论。它解释了为何该项目更倾向于使用本地信任的地址簿，而不是采用类 DNS 的查询或多数投票式注册表。关于当前的使用指导，请参见[命名文档](/docs/overview/naming/)。

## 已放弃的备选方案

I2P 的安全目标排除了常见的命名方案：

- **DNS 风格解析。** 在查询路径上的任何解析器都可能伪造或审查应答。即便有 DNSSEC（DNS 安全扩展），被攻陷的注册商或证书颁发机构（CA）仍然是单点故障。在 I2P 中，destinations（目标标识）*就是*公钥—劫持一次查询就会彻底攻陷一个身份。
- **基于投票的命名。** 对手可以批量创建无限数量的身份（女巫攻击 Sybil attack），并让热门名称在投票中“胜出”。基于工作量证明（Proof-of-Work，PoW）的缓解措施会抬高成本，但会引入沉重的协调开销。

相反，I2P 刻意将命名维持在传输层之上。捆绑的命名库提供了一个服务提供者接口（SPI），从而允许替代方案并存——由用户决定他们信任哪些地址簿或跳转服务。

## 本地与全局名称 (jrandom, 2005)

- I2P 中的名称是**在本地唯一且便于人类阅读**。你的 `boss.i2p` 可能与他人的 `boss.i2p` 不一致，这是设计使然。
- 如果恶意行为者诱骗你更改某个名称背后对应的 Destination（I2P 中服务的公钥标识），他们就能实质上劫持该服务。拒绝全局唯一性可以防止这类攻击。
- 将名称视为书签或即时通讯昵称——你可以通过订阅特定地址簿或手动添加密钥，来选择你信任的 Destination。

## 常见异议与回应 (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## 已讨论的效率改进思路

- 提供增量更新（仅包含自上次获取后新增的目标地址）。
- 在完整的 hosts 文件之外提供补充源（`recenthosts.cgi`）。
- 探索可脚本化的工具（例如 `i2host.i2p`），用于合并源或按信任级别过滤。

## 要点

- 安全性优先于全局共识：本地维护的地址簿可最大限度降低劫持风险。
- 通过命名 API，多种命名方式可以并存——由用户决定信任什么。
- 完全去中心化的全局命名仍然是一个未解决的研究问题；在安全性、人类可记忆性与全局唯一性之间的权衡，仍然反映了 [Zooko’s triangle（Zooko 三角）](https://zooko.com/distnames.html)。

## 参考资料

- [命名文档](/docs/overview/naming/)
- [Zooko 的《名称：去中心化、安全、人类可读：三者取其二》](https://zooko.com/distnames.html)
- 示例增量订阅源：[stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
