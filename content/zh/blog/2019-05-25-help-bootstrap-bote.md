---
title: "如何通过帮助 I2P-Bote 引导（bootstrap）来参与志愿服务"
date: 2019-05-20
author: "idk"
description: "帮助引导 I2P-Bote！"
categories: ["development"]
---

帮助人们进行私密通信的一个简单方法，是运行一个 I2P-Bote 节点，它可以供新的 I2P-Bote 用户用来 bootstrap（引导）他们自己的 I2P-Bote 节点。不幸的是，直到现在，搭建一个 I2P-Bote bootstrap 节点的流程一直比它本该的更晦涩。其实这非常简单！

**什么是 I2P-bote？**

I2P-bote 是一个构建在 i2p 之上的私人消息系统，它具备额外的功能，使外界更难以辨别所传输消息的相关信息。基于此，它可以在容忍高延迟的情况下安全地传递私人消息，并且当发送方离线时，无需依赖集中式中继来发送消息。这与几乎所有其他流行的私人消息系统形成对比：后者要么要求双方同时在线，要么依赖于半可信的服务，在发送方离线时代为转发消息。

或者，通俗地说：它的使用方式类似于电子邮件，但没有电子邮件在隐私方面的缺陷。

**第一步：安装 I2P-Bote**

I2P-Bote 是一个 I2P 插件，安装非常容易。原始说明可在 [bote eepSite, bote.i2p](http://bote.i2p/install/) 找到（eepSite 指 I2P 内部网站），但如果你想在明网阅读，以下说明由 bote.i2p 提供：

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**第二步：获取你的 I2P-Bote 节点的 base64 地址**

这一步可能会让人卡住，但别担心。尽管相关说明不太好找，其实操作并不复杂，而且根据你的具体情况，有多种工具和选项可供使用。对于想以志愿者身份帮助运行引导节点的人来说，最佳方法是从 Bote tunnel 使用的私钥文件中提取所需信息。

**密钥在哪里？**

I2P-Bote 会将其目标密钥存储在一个文本文件中；在 Debian 上，该文件位于 `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`。在非 Debian 系统中，当 i2p 由用户安装时，密钥位于 `$HOME/.i2p/i2pbote/local_dest.key`，而在 Windows 上，文件位于 `C:\ProgramData\i2p\i2pbote\local_dest.key`。

**方法 A: 将明文密钥转换为 base64 destination（以 Base64 编码的目标地址）**

为了将明文密钥转换为 Base64 destination（目标地址），需要获取该密钥，并仅将其中的 destination 部分分离出来。为了正确完成此操作，必须执行以下步骤：

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

有许多应用程序和脚本可以为您执行这些步骤。以下是其中的一部分，但远非完整列表：

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

这些功能在许多 I2P 应用开发库中也可用。

**捷径：**


由于你的 Bote 节点的本地 Destination（I2P 的地址标识）是 DSA Destination，因此更快的做法是直接将 local_dest.key 文件截断为前 516 字节。要轻松实现这一点，在 Debian 上配合 I2P 运行 I2P-Bote 时运行以下命令：

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
或者，如果 I2P 是在你的用户账户下安装的：

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**方法 B：进行查询**

如果这看起来有点繁琐，你也可以使用任意可用的 base32 地址查询方式，查询你的 Bote 连接的 base32 地址，从而找到其 base64 Destination（目标标识）。

你的 Bote 节点的 base32 地址可以在 Bote 插件应用下的 "Connection"（连接）页面查看，位于 [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**第三步：联系我们！**

**更新 built-in-peers.txt 文件以包含你的新节点**

Now that you've got the correct destination for your I2P-Bote node, the final step is to add yourself to the default peers list for [I2P-Bote here](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) here. You can do this by forking the repository, adding yourself to the list with your name commented out, and your 516-char destination directly below it, like this:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
并提交一个 Pull Request（拉取请求）。就这么简单，所以请帮助让 i2p 保持活力、去中心化且可靠。
