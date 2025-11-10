---
title: "加速你的 I2P 网络"
date: 2019-07-27
author: "mhatta"
description: "提升你的 I2P 网络速度"
categories: ["tutorial"]
---

*本文直接改编自最初为 mhatta 的* [Medium 博客](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *所创作的材料。* *原帖的功劳应归于他。已在某些* *将 I2P 的旧版本当作当前版本的地方进行了更新，并进行了轻微的* *编辑。-idk*

I2P 刚启动后通常会显得有点慢。这确实如此，原因大家都知道：从本质上说，[garlic routing](https://en.wikipedia.org/wiki/Garlic_routing)（大蒜路由）为了保障你的隐私，会在你熟悉的上网体验之上增加一些开销；但这也意味着，对于许多甚至大多数 I2P 服务，你的数据默认需要经过 12 跳。

![在线匿名工具分析](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

此外，与 Tor 不同，I2P 的设计初衷主要是作为一个封闭网络。你可以轻松访问 [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) 或 I2P 内部的其他资源，但并不建议通过 I2P 访问 [clearnet（明网）](https://en.wikipedia.org/wiki/Clearnet_(networking)) 网站。I2P 存在少量 "outproxies（出口代理）"，它们类似于 [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)) 的出口节点，用于访问 clearnet，但大多数使用起来非常慢，因为前往 clearnet 实际上会在原本“入站 6 跳、出站 6 跳”的连接上再增加*额外*的一跳。

直到几个版本之前，这个问题甚至更难以应对，因为许多 I2P router 用户在为他们的 router 配置带宽设置时遇到困难。如果所有能做到的人都花时间正确调整他们的带宽设置，这不仅会改善你的连接，也会提升整个 I2P 网络。

## 调整带宽限制

由于 I2P 是一个点对点网络，您需要与其他对等节点共享一部分网络带宽。您可以在 "I2P Bandwidth Configuration" 中选择共享多少（I2P Router Console 的 "Applications and Configuration" 部分中的 "Configure Bandwidth" 按钮，或 http://localhost:7657/config）。

![I2P 带宽配置](https://geti2p.net/images/blog/bandwidthmenu.png)

如果你看到共享带宽限制为 48 KBps（这非常低），那么你可能尚未对默认的共享带宽进行调整。正如本博文所改编材料的原作者指出，I2P 的共享带宽默认限制非常低，直到用户进行调整；这样做是为了避免对用户的连接造成问题。

然而，由于许多用户可能不清楚究竟该调整哪些带宽设置，[I2P 0.9.38 版本](https://geti2p.net/en/download)引入了一个新安装向导。它包含一个带宽测试，能够自动检测（得益于 M-Lab 的 [NDT](https://www.measurementlab.net/tests/ndt/)）并据此调整 I2P 的带宽设置。

如果你想重新运行向导，例如在更换服务提供商之后，或者因为你在 0.9.38 版本之前安装了 I2P，你可以从 'Help & FAQ' 页面上的 'Setup' 链接重新启动它，或者直接访问 http://localhost:7657/welcome 打开该向导。

![你能找到 "Setup" 吗？](https://geti2p.net/images/blog/sidemenu.png)

使用向导很简单，只需一直点击 "Next"。有时 M-Lab 选定的测量服务器会宕机，导致测试失败。在这种情况下，点击 "Previous"（不要使用你的 Web 浏览器的 "back" 按钮），然后再试一次。

![带宽测试结果](https://geti2p.net/images/blog/bwresults.png)

## 持续运行 I2P

即使在调整了带宽之后，你的连接仍可能很慢。正如我所说，I2P 是一个 P2P 网络。你的 I2P router 需要一些时间才能被其他对等节点发现并融入 I2P 网络。如果你的 router 运行时间不够长，尚未充分融入网络，或者你过于频繁地非正常关闭，那么网络的速度会一直相当缓慢。另一方面，你的 I2P router 连续运行的时间越长，连接就会越快、越稳定，而且你在网络中的带宽份额也会得到更多利用。

然而，许多人可能无法让自己的 I2P router 持续保持在线。在这种情况下，你仍然可以在 VPS 等远程服务器上运行 I2P router，然后使用 SSH 端口转发。
