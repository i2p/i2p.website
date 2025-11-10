---
title: "I2P 2005-08-30 状态说明"
date: 2005-08-30
author: "jr"
description: "每周更新，涵盖 0.6.0.3 网络状态及 NAT 问题、floodfill netDb 部署，以及 Syndie 国际化进展"
categories: ["status"]
---

嗨，大家，又到了每周的那个时候了

* Index

1) 网络状态 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

0.6.0.3 发布一周以来，反馈总体不错，不过对一些人来说，日志和显示一直相当令人困惑。截止几分钟前，I2P 报告称仍有相当数量的用户错误配置了他们的 NAT 或防火墙——在 241 个对等节点中，有 41 个看到状态变为 ERR-Reject，而 200 个一直是 OK（当他们能获得明确的状态时）。这并不理想，但它有助于进一步聚焦需要完成的工作。

自发布以来，针对一些长期存在的错误情况已有若干修复，使当前的 CVS HEAD（CVS 主干的最新状态）达到 0.6.0.3-4，并很可能在本周晚些时候以 0.6.0.4 的形式发布。

* 2) floodfill netDb

正如我在博客 [2] 中讨论过的 [1]，我们正在试用一个新的、向后兼容的 netDb（I2P 网络数据库），它既将解决我们目前看到的受限路由情况（涉及 20% 的 routers），也会稍微简化一些内容。floodfill（洪泛填充） netDb 作为 0.6.0.3-4 的一部分部署，无需任何额外配置；其基本工作方式是，先在 floodfill 数据库中查询，若无结果再回退到现有的 Kademlia 数据库。如果有几位愿意帮忙试用一下，就升级到 0.6.0.3-4，试它一把吧！

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Syndie 的开发进展相当顺利，完整的远程联合发布功能已投入运行，并针对 I2P 的需求进行了优化（尽量减少 HTTP 请求次数，改为将结果和上传内容打包在 multipart（多部分）的 HTTP POST 中）。新的远程联合发布意味着你可以运行自己的本地 Syndie 实例，离线阅读和发帖，随后再将你的 Syndie 与他人的进行同步——拉取所有新的帖子并推送本地创建的帖子（可以成批、按博客或按帖子进行）。

一个公共的 Syndie 站点是 syndiemedia.i2p（也可以通过 Web 在 http://syndiemedia.i2p.net/ 访问），它的公共存档可通过 http://syndiemedia.i2p/archive/archive.txt 访问（将你的 Syndie node（Syndie 节点）指向该地址即可同步）。该 syndiemedia 的‘front page’默认已被过滤为只包含我的博客，但你仍然可以通过下拉菜单访问其他博客，并据此调整你的默认设置。（随着时间的推移，syndiemedia.i2p 的默认内容将变更为一组入门文章和博客，为进入 syndie 提供一个良好的起点。）

仍在进行的一项工作是对 Syndie 代码库的国际化。我已将本地副本修改为可以在任何机器上（其字符集 / 区域设置 / 等可能不同）正确处理任何内容（任何字符集 / 区域设置 / 等），并干净地提供数据，使用户的浏览器能够正确解析它。不过，我在 Syndie 使用的一个 Jetty 组件上遇到了问题，因为他们用于处理国际化多部分请求的类并不具备字符集感知。还没有 ;)

总之，这意味着一旦把国际化部分理顺，内容和博客在所有语言中都可以被渲染和编辑（当然，还不会被翻译）。在那之前，已创建的内容在国际化完成后可能会出问题（因为在签名的内容区域里有 UTF-8 字符串）。不过，尽管随意折腾吧，希望我今晚或明天就能把这些完成。

此外，仍在筹划中的一些 SML [3] 构想还包括一个 [torrent attachment="1"]我的文件[/torrent] 标签，它将提供一种一键方式，让人们在他们偏好的 BT 客户端（susibt、i2p-bt、azneti2p，甚至非 I2P 的 BT 客户端）中启动所附的种子。是否还需要其他类型的钩子（例如一个 [ed2k] 标签？），或者大家对在 Syndie 中推送内容有完全不同的天马行空的想法？

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

总之，最近有很多事情在进行中，10分钟后来 irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p 或 freenode.net 参加会议吧！

=jr
