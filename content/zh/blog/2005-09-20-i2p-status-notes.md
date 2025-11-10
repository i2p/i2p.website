---
title: "I2P 状态说明（2005-09-20）"
date: 2005-09-20
author: "jr"
description: "每周更新：涵盖 0.6.0.6 版本发布成功（包含 SSU introductions）、I2Phex 0.1.1.27 安全更新，以及 colo（机房托管）迁移完成"
categories: ["status"]
---

大家好，又到星期二了

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) 迁移 4) ???

* 1) 0.6.0.6

随着上周六发布的 0.6.0.6 版本，我们在正式网络上已经投入了一批新组件，大家升级得很棒——截至几小时前，已有将近 250 台 routers 完成升级！网络运行情况也很不错，introductions（引入）到目前为止工作正常——你可以通过 http://localhost:7657/oldstats.jsp 跟踪你自己的 introduction 活动，查看 udp.receiveHolePunch 和 udp.receiveIntroRelayResponse（还包括 udp.receiveRelayIntro，针对位于 NAT（网络地址转换）之后的用户）。

顺便说一下，"Status: ERR-Reject" 现在其实并不是一个错误，所以也许我们应该把它改为 "Status: OK (NAT)"？

最近有一些关于 Syndie 的 bug 报告。最新的一个 bug 是：如果你一次让它下载太多条目，它将无法与远程对等节点同步（因为我当时愚蠢地使用了 HTTP GET 而不是 POST）。我会为 EepGet 添加对 POST 的支持，但在此期间，试着每次只拉取 20 或 30 篇帖子。顺便说一句，也许有人可以为 remote.jsp 页面写一段 JavaScript，实现“从该用户获取所有帖子”，自动勾选其博客中的所有复选框？

坊间传言，OSX 现在已经能开箱即用；而在 0.6.0.6-1 中，x86_64 在 Windows 和 Linux 上也能正常运行。我还没听说过新的 .exe 安装程序有任何问题报告，所以这要么意味着进展顺利，要么就是完全失败了 :)

* 2) I2Phex 0.1.1.27

鉴于有报告称源码与legion打包的0.1.1.26中所包含的内容存在差异，并且考虑到对闭源本地启动器安全性的担忧，我已经着手将一个使用 launch4j [1] 构建的新的 i2phex.exe 添加到 cvs，并在 i2p 文件归档 [2] 上提供了从 cvs 构建的最新版本。至于legion在发布之前是否对其源代码做过其他修改，或者他公开的源代码是否确实与其构建的版本一致，目前尚不清楚。

出于安全考虑，我不推荐使用 legion 的闭源启动器，也不推荐使用 0.1.1.26 发行版。I2P 网站 [2] 上的发行版包含来自 cvs 的最新代码，未作修改。

你可以通过先检出并构建 I2P 代码，然后检出 I2Phex 代码，最后运行 "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (密码：anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

那个 zip 中的 i2phex.exe 在 Windows 上只需直接运行即可使用，或在 *nix/osx 上通过 "java -jar i2phex.exe" 运行。它依赖 I2Phex 安装在紧邻 I2P 的目录中 - (例如 C:\Program Files\i2phex\ 和 C:\Program Files\i2p\)，因为它会引用 I2P 的一些 jar 文件。

我并不会接手维护 I2Phex，但当 cvs 有更新时，我会把 I2Phex 的后续发行版发布到网站上。如果有人愿意制作一个我们可以发布的网页来描述/介绍它（sirup，你在吗？），并包含指向 sirup.i2p、有用的论坛帖子以及 legion 的活跃对等节点列表的链接，那就太好了。

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip 以及     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (由我的密钥签名)

* 3) migration

我们已经为 I2P 服务更换了 colo boxes（机房托管服务器），但现在在新机器上一切应该都已完全正常运行——如果你看到什么不对劲的地方，请告诉我！

* 4) ???

最近在 i2p 邮件列表上有很多有趣的讨论，比如 Adam 新做的很不错的 SMTP 代理/过滤器，还有 syndie 上的一些好帖子（在 http://gloinsblog.i2p 看过 gloin 的皮肤吗？）。我目前正在针对一些长期存在的问题做一些更改，但这些还不会很快完成。如果有人还有其他想要提出并讨论的内容，欢迎在 GMT 晚上8点来 #i2p 的会议（大约还有10分钟左右）。

=jr
