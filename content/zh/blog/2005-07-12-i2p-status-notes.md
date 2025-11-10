---
title: "I2P 2005-07-12 状态说明"
date: 2005-07-12
author: "jr"
description: "每周更新，涵盖服务恢复、SSU 测试进展，以及对 I2CP 加密层的分析，评估潜在的简化"
categories: ["status"]
---

嗨，大家，又到了每周的这个时候了

* Index

1) squid/www/cvs/dev.i2p 已恢复 2) SSU 测试 3) I2CP 加密 4) ???

* 1) squid/www/cvs/dev.i2p restored

在几台机房托管的机器上折腾了好一阵之后，一些旧服务已经恢复 - squid.i2p（两个默认 outproxy（出口代理）之一）、www.i2p（一个指向 www.i2p.net 的安全链接）、dev.i2p（一个指向 dev.i2p.net 的安全链接，其中有邮件列表存档、cvsweb，以及默认的 netDb 种子）、以及 cvs.i2p（一个指向我们 CVS 服务器的安全链接 - cvs.i2p.net:2401）。我的博客仍然失踪，不过反正内容已经丢失，所以迟早都得重新开始。既然这些服务已经可靠地恢复在线，是时候继续转向...

* 2) SSU testing

正如每个人的 router 控制台上那个小黄框所提到的，我们已经开始了针对 SSU 的下一轮在真实网络上的测试。这些测试并不适合所有人，但如果你喜欢尝鲜并且对进行一些手动配置感到自如，请查看你的 router 控制台上提到的详细信息 (http://localhost:7657/index.jsp)。测试可能会进行好几轮，但我预计在 0.6 版本发布之前，SSU 不会有重大变化 (0.6.1 将为无法进行端口转发或以其他方式接收入站 UDP 连接的用户提供支持)。

* 3) I2CP crypto

在再次审阅新的入门文档时，我发现很难为 I2CP SDK 内进行的额外加密层提供充分的理由。I2CP 加密层的最初意图是为传输的消息提供基本的端到端保护，同时允许 I2CP clients（即 I2PTunnel、the SAM bridge、I2Phex、azneti2p 等）能够通过不受信任的 router（路由器）进行通信。然而，随着实现的推进，I2CP 层的端到端保护已变得多余，因为所有客户端消息都由 router 在 garlic messages（garlic 消息）中进行端到端加密，并捆绑发送方的 leaseSet（租约集合），有时还包含一个传送状态消息。这种 garlic 层已经在发送方的 router 与接收方的 router 之间提供了端到端加密——唯一的区别是，它无法防范该 router 本身是恶意的情况。

然而，从可预见的用例来看，我似乎想不出一个本地 router 不被信任的有效场景。至少，I2CP 加密只会隐藏从 router 传输出的消息内容 - router 仍然需要知道应将其发送到哪个 Destination（目标标识）。如有必要，我们可以添加一个 SSH/SSL I2CP 监听器，使 I2CP 客户端和 router 能在不同的机器上运行，或者有此类需求的人可以使用现有的隧道工具。

为重申目前使用的加密分层，我们有:
  * I2CP 的端到端 ElGamal/AES+SessionTag 层，从
    发送方的 Destination（目标）到接收方的 Destination 进行加密。
  * router 的端到端 garlic encryption 层
    (ElGamal/AES+SessionTag)，对从发送方的 router 到
    接收方的 router 的数据进行加密。
  * 同时适用于入站和出站
    tunnel 的 tunnel 加密层，在各自路径上的每一跳生效（但不包括出站
    端点与入站网关之间）。
  * 各 router 之间的传输加密层。

我希望在移除其中一层时相当谨慎，但我也不想因为做不必要的工作而浪费我们的资源。我的提议是移除第一层 I2CP 加密层（但当然仍然保留在 I2CP 会话建立期间使用的认证、leaseSet 授权以及发送方认证）。有没有人能提出我们应当保留它的理由？

* 4) ???

目前情况大致如此，不过一如既往，仍有许多工作在进行中。本周仍然没有会议，但如果有人有需要提出的事项，请不要犹豫，发送到邮件列表或在论坛上发帖。另外，尽管我会查看 #i2p 的聊天记录，一般性的问题或疑虑请改为发送到邮件列表，以便更多人参与讨论。

=jr
