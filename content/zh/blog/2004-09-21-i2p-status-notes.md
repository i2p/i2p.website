---
title: "I2P 状态说明（2004-09-21）"
date: 2004-09-21
author: "jr"
description: "每周 I2P 状态更新，涵盖开发进展、TCP 传输改进以及新的 userhosts.txt 功能"
categories: ["status"]
---

嗨，大家，这周简单更新一下

## 索引

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) 开发状态

过去一周网络相当稳定，因此我得以把时间专注于 0.4.1 版本的发布 - 重构 TCP 传输并添加对检测 IP 地址的支持，同时移除那个旧的 "target changed identities" 提示（目标身份已变更）。这也应该让 dyndns 记录不再必要。

对于处在 NAT（网络地址转换）或防火墙之后的用户来说，它不会是理想的“零点击”设置——他们仍然需要进行端口转发，才能接收入站的 TCP 连接。不过，它应该更不容易出错。我会尽力保持向后兼容，但在这方面我不作任何保证。等准备就绪后会有更多消息。

## 2) 新的 userhosts.txt 与 hosts.txt 的比较

在下一个版本中，我们将加入长期以来被频繁请求的功能：支持两个 hosts.txt 文件——一个会在升级期间（或从 `http://dev.i2p.net/i2p/hosts.txt` 获取时）被覆盖，另一个则由用户在本地维护。在下一个版本（或 CVS HEAD）中，你可以编辑文件 "userhosts.txt"，系统在查找任何条目前会先检查它，再检查 hosts.txt——请将你的本地更改放在那里，因为更新过程会覆盖 hosts.txt（但不会覆盖 userhosts.txt）。

## 3) ???

如前所述，本周只有一些简短的笔记。大家还有其他想要提出的事项吗？几分钟后顺道来参加会议吧。

=jr
