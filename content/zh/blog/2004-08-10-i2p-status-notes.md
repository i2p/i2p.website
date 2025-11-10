---
title: "I2P 状态说明（2004-08-10）"
date: 2004-08-10
author: "jr"
description: "每周 I2P 状态更新，涵盖 0.3.4.1 版本的性能表现、outproxy（出站代理）负载均衡，以及文档更新"
categories: ["status"]
---

大家好，每周更新时间到了

## 索引:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 状态

我们前几天发布了 0.3.4.1 版本，运行情况相当不错。IRC 上的连接时间稳定地持续数小时，传输速率也很不错（前几天我使用 3 条并行流从一个 eepsite(I2P Site) 下载达到了 25KBps）。

One really cool feature added in with the 0.3.4.1 release (that I forgot to add to the release announcement) was mule's patch to allow the eepproxy to round robin non-i2p requests through a series of outproxies. The default is still just to use the squid.i2p outproxy, but if you go into your router.config and change the clientApp line to have:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
它会将每个 HTTP 请求随机通过列出的两个 outproxies（出口代理）之一进行路由（squid.i2p 和 www1.squid.i2p）。这样一来，如果有更多人运行 outproxies，你们就不会如此依赖 squid.i2p 了。当然，关于 outproxies 的担忧你们都已经听过了，但具备这种能力能给大家提供更多选择。

过去几个小时里出现了一些不稳定，但在 duck 和 cervantes 的帮助下，我已经定位了两个棘手的 bug，并且此刻正在测试修复。由于这些修复的改动较大，我预计在接下来一两天内，在验证结果之后发布 0.3.4.2。

## 2) 更新的文档

我们在让网站上的文档保持最新方面有些懈怠，尽管仍有一些较大的空白（例如 netDb 和 i2ptunnel 文档），不过我们最近更新了其中的一些（网络比较和常见问题）。随着我们逐步接近 0.4 和 1.0 的发布，如果大家能通读一下网站，看看哪些地方可以改进，我将不胜感激。

值得特别一提的是，名人堂已更新——我们终于把它同步更新，以体现大家的慷慨捐赠（谢谢！）在接下来的工作中，我们将使用这些资源来向开发者和其他贡献者支付报酬，并用于抵消产生的各项成本（例如托管服务提供商等）。

## 3) 0.4 进展

回顾上周的笔记，我们在 0.4 还有几项工作未完成，不过模拟进展相当顺利，而且多数 kaffe 的问题已经被发现。若大家能对 router 或客户端应用的不同方面进行深入测试，并提交你遇到的任何 bug，那就太好了。

## 4) ???

目前我就先说这些，感谢大家花时间帮助我们向前推进，我觉得我们正在取得很大进展。当然，如果还有人有其他想讨论的内容，欢迎现在就到#i2p的会议来...呃...就是现在 :)

=jr
