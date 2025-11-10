---
title: "I2P 2004-08-24 状态说明"
date: 2004-08-24
author: "jr"
description: "每周 I2P 状态更新，涵盖 0.3.4.3 版本发布、新的 router 控制台功能、0.4 的进展以及多项改进"
categories: ["status"]
---

大家好，今天有很多更新

## 索引

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 状态

0.3.4.3 版本在上周五发布，自那以后整体进展相当顺利。新引入的 tunnel 测试和对等点选择代码出现了一些问题，不过在发布后经过一些调整，已经相当稳定。我不确定 irc 服务器是否已经运行在新版本上，因此我们通常只能依靠使用 eepsites(I2P Sites) 和 http outproxies（出站代理）(squid.i2p 和 www1.squid.i2p) 进行测试。在 0.3.4.3 版本中，较大的 (>5MB) 文件传输仍然不够可靠，但在我的测试中，此后所做的修改进一步改善了情况。

网络规模也在增长——我们在今天早些时候达到了45个并发用户，并且在过去几天里一直稳定在38到44个用户的范围内（w00t）！这在目前来看是一个健康的数量，我也一直在监控整体网络活动，以留意潜在的风险。等到迁移到0.4版本时，我们希望逐步把用户基数提升到大约100 router的水平，并在进一步增长之前做更多测试。至少，从开发者的角度来说，这是我的目标。

### 1.1) timestamper

在 0.3.4.3 版本发布中的一项我完全忘了提及、但绝对棒极了的变化，是对 SNTP（简单网络时间协议）代码的更新。多亏 Adam Buckley 的慷慨，他同意以 BSD 许可证发布他的 SNTP 代码，我们已将旧的 Timestamper 应用合并进 I2P SDK 核心部分，并与我们的时钟完全集成。这意味着三件事： 1. 你可以删除 timestamper.jar（代码现在在 i2p.jar 中） 2. 你可以从你的配置中移除相关的 clientApp 行 3. 你可以更新你的配置以使用新的时间同步选项

router.config 中的新选项很简单，默认值应该已经足够好 (尤其如此，因为你们大多数人无意间已经在使用它们 :)

要设置要查询的 SNTP 服务器列表：

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
要禁用时间同步（仅当你是 NTP 专家，并且确信你的操作系统时钟*始终*正确 - 仅运行 "windows time" 并不足够）：

```
time.disabled=true
```
你不再需要拥有‘timestamper password’了，因为它已经全部直接集成到代码中（啊，BSD vs GPL 的乐趣 :)）

### 1.2) new router console authentication

这只与正在运行新的 router 控制台的用户相关，不过如果你让它在公共接口上监听，你可能会想利用其内置的 HTTP 基本认证。是的，HTTP 基本认证弱得可笑——它无法防住在你的网络上嗅探的人，或通过暴力破解闯入的人，但它能挡住随意的窥探者。总之，要使用它，只需添加这一行

```
consolePassword=blah
```
到你的 router.config。很遗憾，你将不得不重启 router，因为该参数只在启动时被传递给 Jetty 一次。

## 2) 0.4 status

我们在 0.4 版本发布上已经取得了很大进展，并希望在下周推出一些预发布版本。不过我们仍在敲定一些细节，因此目前还没有制定出可靠的升级流程。本次发布将保持向后兼容，所以升级应该不会太麻烦。总之，请密切关注动向，一旦一切准备就绪你就会知道。

### 1.1) 时间戳器

Hypercubus 正在将安装程序、系统托盘应用程序以及一些服务管理代码进行集成方面取得了很大进展。基本上，在 0.4 版本中，所有 Windows 用户都会自动看到一个小小的系统托盘图标（Iggy!），不过他们可以通过 Web 控制台将其禁用（以及/或者重新启用）。

此外，我们将捆绑 JavaService wrapper（服务包装器），这将使我们能够做各种很棒的事情，例如让 I2P 随系统启动（或不随系统启动）、在某些条件下自动重启、按需对 JVM 进行硬重启、生成堆栈跟踪，以及实现其他各种好用的功能。

### 1.2) 新的 router 控制台身份验证

0.4 版本中的一项重大更新将是对 jbigi 代码的全面改造，合并 Iakin 为 Freenet 所做的修改，以及 Iakin 的新“jcpuid”本地库（native library）。该 jcpuid 库仅适用于 x86 架构，并且配合一些新的 jbigi 代码，将决定要加载的‘正确’的 jbigi。为此，我们将只发布一个所有人通用的 jbigi.jar，并从中为当前机器选择‘正确’的版本。当然，用户仍然可以自行构建本地 jbigi，以覆盖 jcpuid 的选择（只需编译它并将其复制到你的 I2P 安装目录中，或将其命名为 "jbigi"，然后放入你的类路径（classpath）中的一个 .jar 文件内）。不过，由于这些更新，它*不*向后兼容——升级时，你必须要么重新构建你自己的 jbigi，要么删除你现有的本地库（以便让新的 jcpuid 代码选择正确的版本）。

### 2.3) i2paddresshelper

oOo 已制作了一个非常酷的辅助工具，让人们无需更新他们的 hosts.txt 就能浏览 eepsites（I2P 站点）。它已提交到 CVS，并将在下一个版本中部署，但大家可能需要相应地考虑更新链接（cervantes 已将 forum.i2p 的 [i2p] bbcode 更新为支持它，并提供了一个 "Try it [i2p]" 链接）。

基本上，你只需要为 eepsite（I2P 站点）创建一个链接，名称可以随意，然后再附加一个用于指定目标（Destination）的特殊 URL 参数：

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
在幕后，这样做相当安全——你无法伪造其他地址，而且该名称*不会*被写入 hosts.txt；不过，它会让你看到在 eepsites(I2P 站点) 上链接的图片等内容，而使用旧的 `http://i2p/base64/` 小技巧则无法做到。如果你想始终能够使用 "wowthisiscool.i2p" 访问该站点，你当然仍然需要将该条目添加到你的 hosts.txt（直到 MyI2P 地址簿发布为止，也就是 ;)）。

## 3) AMOC vs. restricted routes

Mule 一直在提出一些想法，并敦促我解释一些事情；在这个过程中，他确实让我在重新评估整个 AMOC 设想上取得了一些进展。具体来说，如果我们去掉我对传输层施加的一个约束 - 允许我们假定双向性 - 我们也许可以放弃整个 AMOC 传输，转而实现一些基础的 restricted route（受限路由）操作（为后续更高级的 restricted route 技术打下基础，比如受信任的对等体和多跳 router tunnels）。

如果我们采纳这种方案，这将意味着即便身处防火墙、NAT 等之后，人们也无需任何配置即可参与网络，同时还能提供受限路由的一些匿名性特性。相应地，这很可能会对我们的路线图带来一次大规模的调整，但如果我们能安全地实现，它将为我们节省大量时间，绝对值得做出这样的改变。

然而，我们不想仓促行事，并且在承诺走那条路径之前，需要仔细审查其对匿名性和安全性的影响。我们会在 0.4 发布并运行顺利之后再这么做，所以不必着急。

## 2) 0.4 状态

听说 aum 的进展不错 - 我不知道他是否会出席会议并提供更新，但他今天早上确实在 #i2p 给我们留了一段内容：

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
太棒了。

## 5) pages of note

我只是想指出两个新的可用资源，I2P 用户可能会想要看看——DrWoo 整理了一个网页，汇集了大量供希望匿名浏览的人参考的信息，而 Luckypunk 则发布了一篇操作指南，介绍他在 FreeBSD 上使用一些 JVM（Java 虚拟机）的经验。Hypercubus 还发布了关于测试尚未发布的服务与系统托盘集成的文档。

## 6) ???

好的，目前我想说的就这些——如果你还想提出其他话题，今晚 GMT 时间晚上9点过来参加会议吧。

=jr
