---
title: "I2P 状态说明（2005-06-28）"
date: 2005-06-28
author: "jr"
description: "每周更新：涵盖 SSU 传输协议的部署计划、单元测试悬赏的完成与许可方面的考量，以及 Kaffe Java 的状态"
categories: ["status"]
---

Hi y'all, weekly update time again

* Index

1) SSU 状态 2) 单元测试状态 3) Kaffe 状态 4) ???

* 1) SSU status

SSU 传输又取得了一些进展，我目前的想法是，经过更多实网测试后，我们应该能够在不太拖延的情况下发布为 0.6。首个 SSU 版本不会支持那些无法在防火墙上开放端口或调整其 NAT（网络地址转换）设置的用户，但该支持会在 0.6.1 中推出。等 0.6.1 发布、完成测试并表现出色（即 0.6.1.42）后，我们将推进到 1.0。

我个人倾向于随着 SSU transport（SSU 传输）逐步推广而彻底放弃 TCP 传输，这样用户就不必同时启用两者（同时转发 TCP 和 UDP 端口），开发者也无需维护不必要的代码。对此大家有没有强烈的看法？

* 2) Unit test status

正如上周提到的，Comwiz 已出面认领单元测试悬赏的第一阶段（Comwiz 太棒了！也感谢 duck 和 zab 为悬赏提供资金！）。代码已提交到 CVS，取决于你的本地设置，你可以通过进入 i2p/core/java 目录并运行 "ant test junit.report"（大约等一个小时……），然后查看 i2p/reports/core/html/junit/index.html 来生成 junit 和 clover 报告。另一方面，你也可以运行 "ant useclover test junit.report clover.report"，并查看 i2p/reports/core/html/clover/index.html。

这两组测试的缺点，归根结底在于那种统治阶级称之为“版权法”的愚蠢概念。Clover 是一款商业产品，不过 cenqua 那边的人允许开源开发者免费使用（而且他们也友好地同意向我们授予一份许可）。要生成 Clover 报告，你需要在本地安装 Clover - 我把 clover.jar 放在 ~/.ant/lib/ 里，就在我的许可文件旁边。大多数人并不需要 Clover，而既然我们会在网上发布这些报告，不安装它也不会造成任何功能上的损失。

另一方面，当我们把单元测试框架本身纳入考虑时，我们又被版权法的另一面所掣肘 - junit 采用 IBM Common Public License 1.0 发布，而根据 FSF [1] 的说法，它与 GPL 并不兼容。现在，虽然我们自己没有任何 GPL 代码（至少在核心或 router 中没有），回顾我们的许可政策 [2]，我们在具体许可方式上的目标，是让尽可能多的人能够使用正在被创建的成果，因为匿名需要同伴。

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

鉴于有些人令人费解地以 GPL 发布软件，我们有必要努力确保他们能够不受限制地使用 I2P。至少，这意味着我们不能让我们对外提供的实际功能依赖于受 CPL 许可的代码（例如 junit.framework.*）。我也希望把这一点扩展到单元测试，但 junit 似乎是测试框架的通用语言（而且考虑到我们的资源，我不认为说“嘿，我们自己做一个公共领域的单元测试框架吧！”会有任何理智可言）。

综上所述，我的想法是：我们会在 CVS 中捆绑 junit.jar，并在运行单元测试时使用它，但单元测试本身不会被构建进 i2p.jar 或 router.jar，也不会包含在发布版本中。必要时，我们可能会另外提供一组 jar 包（i2p-test.jar 和 router-test.jar），但这些将不能被采用 GPL 许可（GNU General Public License）的应用程序使用（因为它们依赖于 junit）。

=jr
