---
title: "I2P 状态说明（2006-09-12）"
date: 2006-09-12
author: "jr"
description: "0.6.1.25 版本发布：改进网络稳定性、优化 I2PSnark，并对 Syndie 进行全面重新设计，支持离线分布式论坛"
categories: ["status"]
---

大家好，这是我们的*咳*每周状态笔记

* Index:

1) 0.6.1.25 与网络状态 2) I2PSnark 3) Syndie（是什么/为什么/何时） 4) Syndie 加密问题 5) ???

* 1) 0.6.1.25 and net status

前几天我们发布了 0.6.1.25 版本，其中包含过去一个月积累的一大批缺陷修复，以及 zzz 在 I2PSnark 上的工作和 Complication 为让我们的时间同步代码更健壮所做的努力。当前网络看起来相当稳定，不过 IRC 在过去几天有些不太顺畅（原因与 I2P 无关）。随着网络中大约一半已升级到最新版本，tunnel 构建成功率变化不大，不过整体吞吐量似乎有所提高（可能是因为使用 I2PSnark 的人数增加）。

* 2) I2PSnark

zzz 对 I2PSnark 的更新包括协议优化以及 Web 界面更改，正如历史日志 [1] 中所述。自 0.6.1.25 版本发布以来，I2PSnark 也有一些小更新，也许 zzz 可以在今晚的会议上为我们概述一下最新进展。

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

As y'all know, my time has been focused on revamping Syndie, though "revamp" may not be the right word. Perhaps you can consider what is currently deployed as a "proof of concept", since the new Syndie has been redesigned and reimplemented from the ground up, though many concepts remain. When I refer to Syndie below, I'm talking about the new Syndie.

* 3.1) What is Syndie

Syndie 在最基本层面上，是一个用于运行离线分布式论坛的系统。尽管其结构可以产生大量不同的配置，但大多数需求都可以通过在以下三个标准中的每一项里选择一个选项来满足：  - 论坛类型：    - 单作者（典型博客）    - 多作者（多作者博客）**    - 开放（新闻组；不过可以加入限制，使得只有      获得授权** 的用户可以发布新主题，而任何人都可以对      这些新主题发表评论）  - 可见性：    - 任何人都可以阅读所有内容    - 只有获得授权* 的人可以阅读帖子，但会暴露部分元数据    - 只有获得授权* 的人可以阅读帖子，甚至才能知道是谁在      发帖    - 只有获得授权* 的人可以阅读帖子，且无人知道是谁在      发帖  - 评论/回复：    - 任何人都可以发表评论或向作者/论坛      所有者发送私密回复    - 只有获得授权** 的人可以发表评论，且任何人都可以发送私密      回复    - 无人可以发表评论，但任何人都可以发送私密回复    - 无人可以发表评论，也无人可以发送私密回复

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** 通过向这些用户提供用于为帖子签名的非对称私钥来实现对发帖、更新和/或评论的授权，其中相应的公钥会被包含在论坛的元数据中，并被标记为获准在该论坛发帖、管理或评论。或者，也可以在元数据中列出各个已授权用户的签名公钥。

单个帖子可以包含许多不同的元素：  - 任意数量的页面，每个页面都有带外数据来指定    内容类型、语言等。  可以采用任何格式，因为是否以及如何安全地呈现内容由    客户端应用程序决定 - 必须支持纯文本，且在可能的情况下客户端应支持 HTML。  - 任意数量的附件（同样有带外数据来描述该    附件）  - 帖子的小头像（如果未指定，则使用作者的    默认头像）  - 指向其他帖子、论坛、存档、URL 等的一组引用（其中    可能包含发帖、管理或阅读被引用论坛所需的    密钥）

总体而言，Syndie工作在*content layer*（内容层） - 单个帖子被封装在加密的zip文件中，而参与论坛意味着只需共享这些文件。对于文件的传输方式（通过 I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email）没有任何依赖，但标准的Syndie发行版会附带简单的聚合和分发工具。

与 Syndie 内容的交互将通过多种方式进行。首先，提供了一个可脚本化的基于文本的接口，支持以命令行和交互方式从论坛读取、向论坛写入、管理以及同步。例如，下面是一个用于生成新的“每日消息（message of the day, MOTD）”帖子的简单脚本 -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

只需通过管道将其传给 syndie 可执行文件即可完成：cat motd-script | ./syndie > syndie.log

此外，正在进行图形化 Syndie 界面的开发工作，其中包括对纯文本和 HTML 页面进行安全渲染（当然，也支持与 Syndie 的功能进行透明集成）。

基于 Syndie 旧版“sucker”（抓取器）代码的应用将能够对普通网页和网站进行抓取与重写，从而将其用作单页或多页的 Syndie 帖子，并可将图像和其他资源作为附件包含其中。

未来，firefox/mozilla 插件计划既能检测并导入 Syndie 格式的文件和 Syndie 引用，还能通知本地 Syndie GUI，将某个论坛、主题、标签、作者或搜索结果聚焦显示。

当然，由于 Syndie 在本质上是一个具有明确定义的文件格式和密码学算法的内容层，随着时间的推移，很可能会陆续出现其他应用或替代实现。

* 3.2) Why does Syndie matter?

在过去的几个月里，我听到好几个人问，为什么我在开发一个论坛/博客工具——这跟提供强匿名性有什么关系？

答案：*一切*。

简要总结如下：  - 作为对匿名性敏感的客户端应用，Syndie 的设计谨慎地避免了几乎所有未以匿名为出发点构建的应用所无法避免的复杂数据敏感性问题。  - 通过在内容层运行，Syndie 不依赖 I2P、Tor、或 Freenet 等分布式网络的性能或可靠性，但在合适的情况下可以加以利用。  - 通过这样做，它可以完全依靠用于内容分发的小型、临时机制来运作——对于强大的对手而言，这类机制也许不值得费力去对抗（因为“揪出”区区几十个人的“回报”很可能超过发动攻击的成本）。  - 这意味着，即便没有数百万人使用它，Syndie 仍然有用——彼此无关的小型群体应当各自建立私有的 Syndie 分发方案，而无需与任何其他群体发生交互，甚至无需被其知晓。  - 由于 Syndie 不依赖实时交互，它甚至可以利用高延迟的匿名系统和技术，以避免所有低延迟系统都易受其害的攻击（例如被动交集攻击、被动与主动时序攻击，以及主动混合攻击）。

总体而言，我认为 Syndie 对 I2P 的核心使命（为需要的人提供强匿名性）甚至比 router 更重要。它并非终极答案，但却是关键的一步。

* 3.3) When can we use Syndie?

尽管已经完成了大量工作（包括几乎所有的文本界面以及相当一部分图形用户界面（GUI）），但仍有工作尚待完成。Syndie 的首个发行版将包含以下基础功能：

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

我打算在发布它时采用的标准是“完全可用”。普通用户不会去折腾一个基于文本的应用，不过我希望有些极客会。

后续版本将在多个方面改进 Syndie 的功能:  - 用户界面:   - 基于 SWT 的 GUI   - Web 浏览器插件   - Web 抓取式文本界面 (拉取并重写页面)   - IMAP/POP3/NNTP 阅读接口  - 内容支持   - 纯文本   - HTML (在 GUI 内安全渲染，而非在浏览器中)   - BBCode (?)  - Syndication (内容联合发布)   - Feedspace、Feedtree 以及其他低延迟同步工具   - Freenet (在 CHK@s 存储 .snd 文件，并在 SSK@s 和 USK@s 上存放引用
     这些 .snd 文件的归档)   - Email (通过 SMTP/mixmaster/mixminion 发送，通过
     procmail/etc 阅读)   - Usenet (通过 NNTP 或匿名重发服务发送，通过 (代理的)
     NNTP 阅读)  - 集成 Lucene 的全文搜索  - 扩展 HSQLDB 以实现完整的数据库加密  - 额外的归档管理启发式策略

何时会产出什么，取决于事情完成的时间。

* 4) Open questions for Syndie

目前，Syndie 使用 I2P 的标准加密原语实现 - SHA256, AES256/CBC, ElGamal2048, DSA。不过，最后一种算法多少有些格格不入，因为它使用 1024 位公钥，并且依赖于（安全性正在迅速减弱的）SHA1。我从一线听到的一种声音是用 SHA256 来增强 DSA，虽然这可行（但尚未标准化），却仍然只能提供 1024 位公钥。

由于 Syndie 尚未对外发布，而且无需担心向后兼容性，我们可以从容地更换所用的密码学原语。一个思路是选择 ElGamal2048 或 RSA2048 签名以取代 DSA，另一种思路是转向 ECC（使用 ECDSA 签名和 ECIES 非对称加密），安全级别可能为 256 位或 521 位（分别对应 128 位和 256 位对称密钥强度）。

至于与 ECC（椭圆曲线密码）相关的专利问题，那些似乎只与某些特定的优化（point compression（点压缩））以及我们并不需要的算法（EC MQV（椭圆曲线 MQV 算法））有关。就 Java 支持而言，现成的内容并不多，尽管 bouncycastle lib 似乎有一些代码。不过，像我们对 libGMP 所做的那样（从而得到 jbigi），给 libtomcrypt、openssl 或 crypto++ 加上一层小的封装大概也不是什么难事。

对此有何看法？

* 5) ???

上面有很多内容需要消化，这也是为什么（根据 cervantes 的建议）我这么早就发出这些状态说明。如果你有任何评论、问题、顾虑或建议，今晚 UTC 时间 8 点请到 irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p 上的 #i2p 参加我们的 *cough* 每周会议！

=jr
