---
title: "I2P 2006-01-24 状态说明"
date: 2006-01-24
author: "jr"
description: "网络状态更新、0.6.2 版本的新 tunnel 构建流程，以及可靠性改进"
categories: ["status"]
---

大家好，星期二总会回来...

* Index

1) 网络状态 2) 新的构建流程 3) ???

* 1) Net status

The past week hasn't brought many changes to the network, with most users (77%) up on the latest release.  Still, there are some hefty changes coming down the path, related to the new tunnel building process, and these changes will cause some bumps for those helping to test the unrelease builds.  On the whole, however, those using the releases should continue to have a fairly reliable level of service.

* 2) New build process

作为 0.6.2 中对 tunnel 的改造的一部分，我们正在更改 router 内部使用的流程，以更好地适应不断变化的条件，并更合理地处理负载。这是集成新的节点选择策略与新的 tunnel 创建加密机制的前置步骤，并且完全向后兼容。不过，在此过程中我们也在清理 tunnel 构建流程中的一些权宜之计；尽管其中一些曾有助于掩盖某些可靠性问题，但它们可能导致了并不理想的匿名性与可靠性之间的权衡。具体来说，在发生灾难性故障时，它们会使用回退的单跳 tunnel；而新的流程将宁可表现为不可达，也不会使用回退 tunnel，这意味着用户将会看到更多的可靠性问题。至少，在导致 tunnel 可靠性问题的根源得到解决之前，这些问题将是可见的。

总之，目前构建过程还达不到可接受的可靠性，但一旦达到，我们会在后续版本中发布给大家。

* 3) ???

我知道还有几位正在开展不同的相关工作，不过我会让他们在觉得合适的时候再向我们通报消息。总之，几分钟后在会议上见，大家！

=jr
