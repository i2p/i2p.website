---
title: "I2P 2004-08-31 状态说明"
date: 2004-08-31
author: "jr"
description: "每周 I2P 状态更新，涵盖网络性能下降、0.3.5 版本发布计划、文档需求，以及 Stasher DHT（分布式哈希表）进展"
categories: ["status"]
---

好了，各位男生女生，又到星期二啦！

## 索引:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

嗯，想必大家都注意到了，尽管网络上的用户数量基本保持稳定，过去几天性能却显著下降。其根源是对等节点选择和消息传递代码中一系列缺陷，这些缺陷在上周发生的一次小规模的拒绝服务（DoS）攻击时被暴露出来。结果就是，基本上每个人的 tunnels 都在持续失败，这还产生了一点滚雪球效应。所以，不，这不只是你一个人的问题——对我们其他人来说网络也糟透了 ;)

不过好消息是，我们很快就修复了这些问题，而且这些修复自上周起就已经在 CVS 中了，但在下一个版本发布之前，大家的网络体验仍然会很糟。就此而言……

## 2) 0.3.5 和 0.4

尽管下一个版本将包含我们为 0.4 版本计划的所有内容 (新的安装程序、新的 Web 界面标准、新的 i2ptunnel 接口、系统托盘 (systray) & Windows 服务、线程改进、错误修复等)，但上一个版本随着时间推移出现退化的情况很能说明问题。我希望我们在发布节奏上更为缓慢一些，给它们留出更充分的推广部署时间，也让各种小毛病得以及时暴露。虽然模拟器可以探索基础情况，但它没有办法模拟我们在真实网络上看到的那些自然的网络问题 (至少目前还不行)。

因此，下一次发布将是 0.3.5 —— 希望它会是 0.3.* 系列中的最后一个版本，但也不一定，如果出现其他问题的话。回顾我在六月离线期间网络的运行情况，大约两周后状况开始恶化。因此，我的想法是，在我们能够至少连续两周保持高度可靠性之前，先暂缓将版本标记提升到下一个 0.4 发布级别。当然，这并不意味着在此期间我们不会开展工作。

总之，正如上周所说，hypercubus 正在埋头推进新的安装系统，一边应付我把东西改来改去，还得为一些稀奇古怪的系统提供支持。我们应该能在接下来的几天里把这些事情敲定，并发布 0.3.5 版本。

## 3) docs

在 0.4 之前的那两周 "测试窗口" 期间，我们需要做的一件重要事情是尽可能全面地完善文档。我想知道的是，你觉得我们的文档缺少哪些内容 - 你有哪些问题需要我们来解答？虽然我很想说 "好的，现在就去写那些文档"，但我还是现实一点，所以我只想请你帮忙指出这些文档应该讨论哪些内容。

例如，我目前正在编写的文档之一是对威胁模型的修订，我现在会将其描述为一系列用例，阐释 I2P 如何满足不同个体的需求，其中包括所需的功能、该用户所担心的攻击者，以及他们如何自我防护。

如果你认为你的问题不需要用一整篇文档来解答，只需把它表述为一个问题，我们就可以把它添加到常见问题（FAQ）中。

## 4) stasher 更新

Aum 今天早些时候到频道里，带来了一个更新（而我则不断向他提问）：

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
所以，如你所见，已经有了非常多的进展。即便密钥是在 DHT（分布式哈希表）层之上进行验证，那也真是太酷了（依我拙见）。加油，aum！

## 5) ???

好吧，我要说的就这么多（这也不错，因为会议马上就要开始了）... 顺道过来，想说什么就说！

=jr
