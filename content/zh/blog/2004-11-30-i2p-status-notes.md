---
title: "I2P 2004-11-30 状态说明"
date: 2004-11-30
author: "jr"
description: "每周 I2P 状态更新，涵盖 0.4.2 和 0.4.2.1 版本发布、mail.i2p 的最新动态、i2p-bt 的进展，以及关于 eepsite 安全性的讨论"
categories: ["status"]
---

大家好

## 索引

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 和 0.4.2.1

自从我们终于发布了 0.4.2 之后，网络的可靠性和吞吐量一度大幅提升，直到我们遇到了自己引入的全新 bug。对大多数人而言，IRC 连接能持续好几个小时，不过对遇到这些问题的少数用户来说，这段时间并不太顺利。不过我们已经做了一大批修复，今晚稍晚或明天一早我们将发布新的 0.4.2.1 版本供下载。

## 2) mail.i2p

今天早些时候，postman 悄悄塞给我一张纸条，说他有些想讨论的事情 - 更多信息请查看会议记录（如果你在会前读到这条消息，顺道过来）。

## 3) i2p-bt

新版本的一个不足之处是，我们在 i2p-bt 的移植上遇到了一些问题。其中一些问题已经在 Streaming 库（流式传输库）中被识别并修复，但要使其达到我们的要求，还需要进一步的工作。

## 4) eepsites(I2P 站点)

在过去几个月里，邮件列表、频道和论坛上一直在讨论有关 eepsites(I2P Sites) 和 eepproxy 的工作方式存在的一些问题——最近，有人提到了关于如何过滤以及过滤哪些头信息的问题，也有人提出了配置不当的浏览器带来的危险，此外，还有 DrWoo 的页面总结了许多风险。一个尤其值得注意的事件是：一些人正在积极编写小程序（Applet），如果用户不禁用小程序，它们将劫持用户的计算机。（所以请在你的浏览器中禁用 JAVA 和 JAVASCRIPT）

这当然会引发关于我们如何保障安全的讨论。我听到过一些建议，比如开发我们自己的浏览器，或捆绑一个预先配置了安全设置的浏览器，但让我们现实一点——那要比这里任何人愿意投入的工作多得多。不过，还有三种其他思路：

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

第一个基本上与我们现在的做法差不多，只是我们会用类似 Muffin 或 Freenet 的匿名过滤器来过滤要呈现的内容。这里的缺点在于它仍然会暴露 HTTP 头部，因此我们还必须在 HTTP 层面进行匿名化。

第二种与在 `http://duck.i2p/` 上通过 CGIproxy 所见非常相似，或者类似于在 freenet 的 fproxy 中所见。它也会处理 HTTP 相关部分。

第三种方案有其利弊——它使我们能够使用更具吸引力的界面（因为我们可以安全地使用一些已知安全的JavaScript等），但其缺点是向后不兼容。也许把这一方案与过滤器合并，允许你在经过过滤的HTML中嵌入宏？

总之，这是一个重要的开发工作，并且针对 I2P 最具吸引力的用例之一——安全且匿名的交互式网站。也许有人有其他想法或信息，关于我们如何获得所需的条件？

## 5) ???

Ok, I'm running late for the meeting, so I suppose I should sign this and send it on its way, 'eh?

=jr [看看我能不能让 gpg 正常工作...]
