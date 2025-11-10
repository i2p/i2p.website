---
title: "I2P 于 2004-08-03 的状态说明"
date: 2004-08-03
author: "jr"
description: "每周 I2P 状态更新，涵盖 0.3.4 版本的性能表现、全新 Web 控制台的开发，以及各类应用项目"
categories: ["status"]
---

嗨，各位，我们先把这次状态更新搞定吧

## 索引：

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 状态

随着上周发布的 0.3.4 版本，新网络运行得相当不错——IRC 连接一次可以持续数小时，eepsite(I2P Site) 的获取看起来也相当可靠。吞吐量总体仍然较低，但略有改善（以前我通常看到稳定的 4-5KBps，现在我稳定能看到 5-8KBps）。oOo 发布了两个脚本，用于汇总 IRC 活动，包括消息往返时间和连接持续时间（基于 hypercubus 的 bogobot，最近已提交到 CVS）。

## 2) 列入 0.3.4.1 版本计划

使用 0.3.4 的大家应该都注意到了，我在日志记录方面*咳*有点啰嗦，这已在 cvs 中修正。另外，在写了一些用于压测 ministreaming 库的工具之后，我加入了一个 'choke'（背压机制），以防它吞噬大量内存（当尝试向某个流的缓冲区加入超过 128KB 的数据时会阻塞，这样在发送大文件时，你的 router 不会把整个文件加载到内存中）。我认为这将有助于缓解大家遇到的 OutOfMemory 问题，但我还会加入一些额外的监控/调试代码来验证。

## 3) 新的 Web 控制台 / I2PTunnel 控制器

除了上述针对 0.3.4.1 的修改之外，我们已经准备好了新 router 控制台的第一版，供大家测试。出于一些原因，我们暂时不会把它打包进默认安装，因此在几天后 0.3.4.1 修订版发布时，我们会提供如何让它运行的说明。如你所见，我在 Web 设计方面实在不行，而且正如许多人一直在说的那样，我应该停止在应用层上瞎折腾，把核心和 router 打磨得稳如磐石。因此，尽管这套新控制台已经具备了我们想要的许多优秀功能（通过一些简单的网页即可完整配置 router，提供简明易读的 router 健康状况概览，提供创建 / 编辑 / 停止 / 启动 不同的 I2PTunnel 实例的能力），我确实需要在 Web 方面很拿手的朋友来帮忙。

新 Web 控制台所使用的技术是标准的 JSP、CSS，以及用于向 router / I2PTunnels 查询数据并处理请求的简单 Java bean。它们都被打包成两个 .war 文件，并部署到一个集成的 Jetty Web 服务器中（需要通过 router 的 clientApp.* 行启动）。主 router 控制台的 JSP 和 bean 在技术上相当扎实，不过我为管理 I2PTunnel 实例构建的新 JSP 和 bean 有点临时拼凑。

## 4) 0.4 的内容

除了新的 Web 界面之外，0.4 版本还将包含 hypercubus 的新安装程序，不过我们还没有真正把它集成进去。我们还需要做一些更大规模的仿真（尤其是对诸如 IRC 和 outproxies（外部代理）之类的非对称应用的处理）。此外，我需要把一些更新提交到 kaffe/classpath，这样我们就能让新的 Web 基础设施在开源 JVM 上运行起来。再者，我还得整理一些文档（一个关于可扩展性，另一个是在几个常见场景下对安全性/匿名性的分析）。我们也希望把你们提出的所有改进都集成到新的 Web 控制台中。

哦，也请修复你帮忙发现的任何 bug :)

## 5) 其他开发活动

尽管基础 I2P 系统已经取得了许多进展，但这只是故事的一半——你们中的许多人正在应用和库方面开展出色的工作，让 I2P 更加有用。我在 scrollback（聊天记录回溯）里看到了一些关于谁在做什么的问题。为便于传播这些信息，下面是我所知道的一切（如果你正在做的项目未列出并且愿意分享、如果我有误，或者你想讨论你的进展，请直言！）

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

我现在能想到的大概就这些了——今晚稍晚的时候顺道来参加会议，聊聊一些事情吧。照例，GMT 晚上9点，在常用服务器上的 #i2p。

=jr
