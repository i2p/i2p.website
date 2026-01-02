---
title: "NTCP 讨论"
description: "比较 NTCP 和 SSU 传输协议的历史说明与拟议的调优思路"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## NTCP 与 SSU 的讨论（2007 年 3 月）

### NTCP 问题

_改编自 zzz 与 cervantes 在 IRC 上的对话。_

- **为何在 NTCP 看起来会增加开销和延迟时，仍然让 NTCP 相比 SSU 具有更高优先级？**  
  与最初的 SSU 实现相比，NTCP 通常提供更高的可靠性。
- **通过 NTCP 进行流式传输会遭遇经典的 TCP-over-TCP 崩溃吗？**  
  有可能；但 SSU 原本旨在作为轻量级的 UDP 选项，实践中却被证明过于不可靠。

### “NTCP（I2P 的旧版传输协议）被认为有害” (zzz, 2007年3月25日)

摘要：NTCP 更高的时延和开销可能导致拥塞，然而路由选择更偏向 NTCP，因为其 bid scores（竞价分值）被硬编码为比 SSU 更低。该分析提出了若干要点：

- NTCP 当前的竞价值低于 SSU，因此 routers 更倾向于 NTCP，除非已建立 SSU 会话。
- SSU 通过严格受限的超时和统计来实现确认机制；NTCP 依赖 Java NIO TCP，采用可能更长的 RFC 风格超时。
- 大多数流量（HTTP、IRC、BitTorrent）使用 I2P 的 streaming 库，实际效果是在 NTCP 之上再叠加一层 TCP。当两层都进行重传时，可能出现拥塞崩溃。经典参考包括 [在 TCP 之上再跑 TCP 是个坏主意](http://sites.inka.de/~W1011/devel/tcp-tcp.html)。
- 在 0.8 版中，streaming 库的超时从 10 秒增加到 45 秒；SSU 的最大超时为 3 秒，而 NTCP 的超时被认为接近 60 秒（RFC 建议）。NTCP 的参数很难从外部检查。
- 2007 年的实地观测显示 i2psnark 的上传吞吐量呈振荡，暗示存在周期性的拥塞崩溃。
- 效率测试（强制偏好 SSU）将 tunnel 开销比从约 3.5:1 降至 3:1，并改进了 streaming 指标（窗口大小、RTT、发送/确认比）。

#### 2007 年讨论串中的提案

1. **切换传输优先级**，使 routers 更倾向于 SSU（恢复 `i2np.udp.alwaysPreferred`）。
2. **为 Streaming（流式库）流量打标签**，使 SSU 仅对带标签的消息降低竞价，且不损害匿名性。
3. **收紧 SSU 重传界限**，以降低崩溃（拥塞崩溃）风险。
4. **研究半可靠的下层承载**，以判断在 Streaming（流式库）之下进行重传是否总体上有利。
5. **审查优先级队列与超时设置**—例如，将 Streaming 超时提高到超过 45 s，以与 NTCP 保持一致。

### jrandom 的回复 (2007年3月27日)

关键反驳点：

- 之所以有 NTCP，是因为早期的 SSU 部署曾遭遇拥塞塌陷；即便是适度的每跳重传率，在多跳 tunnel 中也会呈爆炸式增长。
- 缺少 tunnel 级别的确认时，只有一部分消息会得到端到端投递状态；失败可能是静默的。
- TCP 的拥塞控制已历经数十年的优化；NTCP 通过成熟的 TCP 协议栈加以利用。
- 在偏好使用 SSU 时观察到的效率提升，可能反映的是 router 的排队行为，而非协议本身的固有优势。
- 更大的 streaming（流式传输）超时设置已在改善稳定性；在进行重大更改之前，建议先进行更多观察并收集数据。

这场讨论有助于完善后续的传输调优，但并不能反映现代的 NTCP2/SSU2 架构。
