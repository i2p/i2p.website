---
title: "I2P 2004-10-12 的状态说明"
date: 2004-10-12
author: "jr"
description: "每周 I2P 状态更新，涵盖 0.4.1.2 版本发布、动态限速实验、0.4.2 流式传输库开发，以及电子邮件讨论"
categories: ["status"]
---

大家好，到了我们每周更新的时间了

## 索引：

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

新的 0.4.1.2 版本已经发布几天了，一切基本符合预期——不过新的看门狗组件出现了一些小问题，导致它在情况很糟时会选择直接终止你的 router，而不是重启它。正如我今天早些时候提到的，我正在寻找愿意使用新的统计日志工具并向我发送一些数据的人，对此我将不胜感激。

## 2) 0.4.1.3

在 0.4.2 发布之前还会有另一个版本，因为我希望在继续推进之前网络尽可能稳固。我目前正在尝试对 tunnel 参与进行动态限流：当 routers 遭遇流量淹没，或其 tunnel 比平时更慢时，指示它们以概率方式拒绝请求。这些概率和阈值根据正在记录的统计数据动态计算：如果你 10 分钟的 tunnel 测试时间大于 60 分钟的 tunnel 测试时间，则以 60minRate/10minRate 的概率接受该 tunnel 请求（而如果你当前的 tunnels 数量大于 60 分钟的平均 tunnels 数量，则以 p=60mRate/curTunnels 接受它）。

另一个潜在的限速机制是沿着前述思路平滑带宽 - 当我们的带宽使用出现突增时，以概率方式拒绝 tunnels。总之，这一切的目的都是帮助分散网络使用量，并将 tunnels 在更多人之间更均衡地分布。我们在负载均衡方面遇到的主要问题是容量的*过剩*过于严重，因此，我们那些“该死，我们慢了，拒绝吧”的触发器从未被触发。这些新的概率式机制有望将快速变化控制在可控范围内。

I don't have any specific plan for when the 0.4.1.3 release will be out - maybe the weekend. The data people send in (from above) should help determine whether this will be worthwhile, or if there are other avenues more worthwhile.

## 3) 0.4.2

正如我们在上周的会议中讨论的那样，我们已经调整了 0.4.2 和 0.4.3 的发布安排 - 0.4.2 将发布新的流式传输库，而 0.4.3 将发布 tunnel 更新。

我一直在重新审阅有关 TCP 流式特性的文献，发现对于 I2P 有一些值得关注的有趣话题。具体来说，我们较高的往返时延（RTT）使我们更倾向于采用类似 XCP 的方案，并且我们或许应该在各种形式的 explicit congestion notification（显式拥塞通知）上更为激进，不过我们无法利用诸如时间戳选项之类的机制，因为我们的时钟可能存在长达一分钟的偏差。

另外，我们还要确保可以优化 streaming lib（流式传输库）以便处理短时连接（原生 TCP 在这方面相当不擅长） - 例如，我希望能够确切地说仅用三条消息就发送小型（<32KB）的 HTTP GET 请求以及小型（<32KB）的响应:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
总之，这方面目前还没有写出多少代码；协议层面看起来相当类似于 TCP，而数据包则有点像是将 human 的提案与旧提案合并而成。若有人有任何建议或想法，或者希望协助实现，请与我们联系。

## 4) 邮件讨论

关于 I2P 内部（以及与 I2P 外部之间）的电子邮件，已有一些有趣的讨论——postman 已把一组想法发布到网上，并正在征求意见。在 #mail.i2p 上也有相关讨论。或许我们可以请 postman 给我们更新一下进展？

## 5) ???

目前就这些。几分钟后过来参加会议，带上你的意见 :)

=jr
