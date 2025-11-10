---
title: "I2P 2004-07-20 状态说明"
date: 2004-07-20
author: "jr"
description: "每周状态更新，涵盖 0.3.2.3 版本发布、容量调整、网站更新和安全考虑"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, and the roadmap**

在上周发布 0.3.2.3 之后，大家的升级做得非常出色——现在只剩下两个还没跟上（一个停在 0.3.2.2，另一个还停在很早的 0.3.1.4 :)）。过去几天网络比平时更可靠——人们在 irc.duck.i2p 上一次能待上好几个小时，从 eepsites（I2P 网站）下载的大文件能够成功完成，而且总体上 eepsite（I2P 网站）的可达性相当不错。既然进展顺利，而我也想让大家保持警惕，我决定对一些基本概念做出改变，我们会在一两天内把它们随 0.3.3 版本部署。

鉴于有几个人对我们的时间表发表了意见，想知道我们是否能按我们之前公布的日期完成，我决定应该更新一下网站，以反映我在 palmpilot 里的路线图，所以我就这么做了 [1]。日期有所推迟，部分项目也做了调整，但计划仍与上个月讨论的一样 [2]。

0.4 将满足所提到的四项发布标准（功能性、安全性、匿名性和可扩展性），不过在 0.4.2 之前，仅有少数处于 NAT 和防火墙之后的用户能够参与；而在 0.4.3 之前，由于维护大量与其他 routers 的 TCP 连接所带来的开销，网络规模将存在一个有效上限。

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

在过去一周左右，#i2p 上的人们时不时听我抱怨我们的可靠性排名是完全任意的（以及这在最近几次发布中带来的痛苦）。因此我们彻底去除了“可靠性”这一概念，用对容量的度量来替代——“一个节点能为我们做多少？”这在节点选择和节点画像代码中引发了连锁反应（并且显然也影响到了 router 控制台），但除此之外，并没有太多改变。

关于此更改的更多信息可参见修订后的对等节点选择页面 [3]，而当 0.3.3 发布时，你们就能亲眼看到其影响（这几天我一直在试用它，微调了一些设置等）。

[3] http://www.i2p.net/redesign/how_peerselection

**3) 网站更新**

在过去一周里，我们在网站改版[4]方面取得了不少进展——简化导航、整理一些关键页面、导入旧内容，并撰写一些新的条目[5]。我们几乎已经准备好让网站正式上线了，但还有几件事需要完成。

Earlier today, duck went through the site and made an inventory of pages we're missing, and after this afternoon's updates, there are a few outstanding issues that I hope we can either address or get some volunteers to jump on:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

除此之外，我认为这个网站已经基本准备就绪，可以上线了。大家在这方面有什么建议或顾虑吗？

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) 攻击与防御**

Connelly has been coming up with a few new angles to try to poke holes in the network's security and anonymity, and in doing so he has come across some ways we can improve things. While some aspects of the techniques he described don't really match up with I2P, perhaps y'all can see ways they can be expanded upon to attack the network further? C'mon, give 'er a shot :)

**5) ???**

关于今晚的会议，我目前能想到的大概就这些——如果我有遗漏的地方，欢迎随时提出。总之，几分钟后在 #i2p 见。

=jr
