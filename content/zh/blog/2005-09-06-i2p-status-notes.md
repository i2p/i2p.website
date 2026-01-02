---
title: "2005-09-06 的 I2P 状态说明"
date: 2005-09-06
author: "jr"
description: "每周更新涵盖 0.6.0.5 版本成功发布、floodfill netDb 性能、Syndie 在 RSS 和 pet names（Petname 命名系统）方面的进展，以及新的 susidns 地址簿管理应用"
categories: ["status"]
---

大家好，

* Index

1) 网络状态 2) Syndie 状态 3) susidns 4) ???

* 1) Net status

正如许多人所见，在短暂的 0.6.0.4 修订版之后，0.6.0.5 版本已于上周发布。到目前为止，可靠性大幅提升，网络规模也比以往任何时候都大。虽然仍有改进空间，但看起来新的 netDb 正按设计运行。我们甚至已经验证了回退机制——当 floodfill 节点无法连通时，routers 会回退到 kademlia netDb（基于 Kademlia 的网络数据库），而在前几天出现这种情况时，IRC 和 eepsite(I2P Site) 的可靠性并未显著降低。

我确实收到一个关于新 netDb 的工作原理的提问，并已在我的博客[2]上发布了答案[1]。一如既往，如果有人对这类事情有任何疑问，请随时转给我，无论是在列表上还是私下、在论坛上，甚至在你的博客上 ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

正如你可以从 syndiemedia.i2p（以及 http://syndiemedia.i2p.net/）看到的那样，最近有了不少进展，包括 RSS、pet names（昵称体系）、管理控制，以及开始合理地使用 css。Isamoor 的大部分建议已经部署，Adam 的也一样，所以如果有人有希望在其中看到的内容，请给我发个消息！

Syndie 现在已经非常接近测试版（beta），届时它将作为默认 I2P 应用之一发布，同时也会打包为独立版本，因此任何帮助都将不胜感激。随着今天最新的新增内容（在 cvs 中），为 Syndie 定制皮肤也变得轻而易举 - 你只需在你的 i2p/docs/ 目录中创建一个新文件 syndie_standard.css，指定的样式就会覆盖 Syndie 的默认设置。关于这方面的更多信息可以在我的博客 [2] 找到。

* 3) susidns

Susi 又为我们迅速做出了一个 Web 应用程序 - susidns [3]。它作为用于管理地址簿应用的简单界面 - 其条目、订阅等。它看起来相当不错，所以希望我们很快就能将它作为默认应用之一发布，但在此之前，你可以很轻松地从她的 eepsite(I2P 站点) 获取它，保存到你的 webapps 目录，重启你的 router，就可以开始使用了。

[3] http://susi.i2p/?page_id=13

* 4) ???

虽然我们一直专注于客户端应用这一侧（并将继续这样做），但我仍将大量时间投入到网络的核心运行上，而且一些令人兴奋的功能即将到来 - 借助 introductions（引介）实现防火墙和 NAT 穿越、改进的 SSU 自动配置、更高级的对等节点排序与选择，甚至还有一些简单的受限路由处理。在网站方面，HalfEmpty 也对我们的样式表做了一些改进（耶！）。

总之，最近事情很多，不过我现在只有时间先提到这些。欢迎在 UTC 时间晚上8点的会议上顺道过来打个招呼 :)

=jr
