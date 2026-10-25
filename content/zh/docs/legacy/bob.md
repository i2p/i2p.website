---
title: "BOB - 基本开放桥接"
description: "已弃用的目标地址管理 API"
slug: "bob"
aliases:
  - "/zh/docs/api/bob"
  - "/zh/docs/api/bob/"
  - "/zh/bob"
  - "/zh/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## 警告 - 已弃用

不适用于新应用程序。此处指定的 BOB 仅支持 DSA-SHA1 签名类型。BOB 不会扩展以支持新的签名类型或其他高级功能。新应用程序应使用 [SAM V3](/docs/api/samv3)。

从1.7.0版本（2022年2月）开始，Java I2P的新安装版本已移除BOB支持。在原本安装为1.6.1或更早版本的Java I2P中，即使经过更新，BOB仍可正常工作，但已不受支持且可能随时出现故障。截至2025年5月，i2pd仍支持BOB，但基于上述原因，应用程序仍应迁移至SAMv3。有关i2pd支持的此处记录API的任何扩展，请参阅[i2pd文档](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/)。

目前，BOB 的大部分优秀想法已被整合到 SAMv3 中，SAMv3 具有更多功能和更多实际应用。BOB 在某些安装中可能仍然有效（见上文），但它没有获得 SAMv3 可用的高级功能，基本上已不再受支持，除了 i2pd。

## BOB API 的语言库

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## 概述

`KEYS` = 密钥对 公钥+私钥，这些都是 BASE64 格式

`KEY` = 公钥，也是 BASE64 格式

如其含义所示，`ERROR` 返回消息 `"ERROR "+DESCRIPTION+"\n"`，其中 `DESCRIPTION` 是出错的内容。

`OK` 返回 `"OK"`，如果有数据需要返回，则在同一行显示。`OK` 表示命令已完成。

`DATA` 行包含您请求的信息。每个请求可能包含多个 `DATA` 行。

**注意：** help命令是唯一一个例外的命令...它实际上可以不返回任何内容！这是有意设计的，因为help是一个面向人类而不是应用程序的命令。

## 连接和版本

所有 BOB 状态输出都是按行输出的。行可能以 \\n 或 \\r\\n 结尾，这取决于系统。连接时，BOB 输出两行：

```
BOB version
OK
```
当前版本是：00.00.10

请注意，之前的版本使用大写十六进制数字，不符合I2P版本标准。建议后续版本仅使用0-9数字。

### 版本历史

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## 命令

**请注意：** 要获取命令的最新详细信息，请使用内置的帮助命令。只需 telnet 到 localhost 2827 并输入 help，即可获得每个命令的完整文档。

命令永远不会被废弃或更改，但是会不时添加新命令。

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
一旦设置完成，所有的TCP套接字可以并将根据需要进行阻塞，无需通过命令通道发送/接收任何额外的消息。这允许router对数据流进行节奏控制，而不会像SAM那样因尝试在一个套接字中推送大量输入或输出流而导致内存不足（OOM）错误——当你有大量连接时，这种方式无法扩展！

这个特定接口的另一个优点是，为它编写任何接口程序都比 SAM 容易得多。设置完成后无需进行其他处理。它的配置非常简单，甚至可以使用 nc (netcat) 这样的简单工具来指向某个应用程序。这样做的价值在于，你可以为应用程序安排上线和下线时间，而无需修改应用程序本身，甚至无需停止该应用程序。相反，你可以字面意思上"拔掉"目标地址，然后再"插回去"。只要在启动桥接时使用相同的 IP/端口地址和目标密钥，普通的 TCP 应用程序就不会在意，也不会注意到。它会被"欺骗"——目标地址无法到达，没有任何数据进入。

## 示例

在以下示例中，我们将设置一个非常简单的本地回环连接，包含两个目标。目标"mouth"将是来自INET超级服务器守护进程的CHARGEN服务。目标"ear"将是一个本地端口，你可以通过telnet连接进去，观看漂亮的ASCII测试文本输出。

### 示例会话对话

简单的 telnet 127.0.0.1 2827 命令可以正常工作。

- A = 应用程序
- C = BOB 的命令响应。

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**请记下上面的目标密钥，你的密钥会有所不同！**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
此时没有错误，已设置了一个昵称为"mouth"的目标。当你联系提供的目标时，实际上是连接到`19/TCP`上的`CHARGEN`服务。

现在处理另一半，这样我们就能实际联系到这个目标地址。

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
现在我们需要做的就是通过 telnet 连接到 127.0.0.1，端口 37337，发送我们想要联系的目标密钥或地址簿中的主机地址。在这种情况下，我们想要联系 "mouth"，我们只需要粘贴密钥，然后就可以了。

**注意：** 命令通道中的"quit"命令不会像SAM那样断开tunnel连接。

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
在这些输出信息滚动几个虚拟英里后，按下 `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
以下是发生的情况...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
您也可以连接到 I2P 站点！

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
很酷，不是吗？如果你愿意，可以尝试一些其他知名的I2P网站、不存在的网站等等，以了解在不同情况下会有什么样的输出。大多数情况下，建议你忽略任何错误消息。这些消息对应用程序来说是无意义的，只是为了方便人工调试而显示的。

### 清理

现在我们已经完成了所有操作，让我们关闭这些目标地址。

首先，让我们看看我们有哪些目标地址别名。

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
好的，它们在那里。首先，让我们删除"mouth"。

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
现在移除"ear"，请注意这是打字太快时会发生的情况，并向您展示典型的错误消息是什么样子的。

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## 静默模式

我不会费心展示bridge接收端的示例，因为它非常简单。它有两个可能的设置，可以通过"quiet"命令进行切换。

默认情况下并非静默模式，进入你的监听套接字的第一个数据是发起连接的目标地址。这是由 BASE64 地址组成的单行数据，后跟换行符。之后的所有内容才是应用程序实际需要处理的数据。

在静默模式下，可以将其视为常规的互联网连接。完全没有额外数据传入。就像你直接连接到常规互联网一样。这种模式提供了一种透明性形式，类似于 router 控制台 tunnel 设置页面中可用的功能，因此你可以使用 BOB 将目标指向一个 web 服务器，例如，而不需要对 web 服务器进行任何修改。

## BOB 的优势

使用BOB的优势如前所述。你可以为应用程序安排随机的运行时间，重定向到不同的机器等等。这样做的一个用途可能是想要干扰router到目标地址的在线状态猜测。你可以用一个完全不同的进程来停止和启动目标地址，从而在服务上制造随机的上线和下线时间。这样你只需要停止联系此类服务的能力，而不必费心关闭并重新启动它。你可以在进行更新时重定向并指向LAN上的不同机器，或者根据正在运行的内容指向一组备用机器等等。只有你的想象力限制了你可以用BOB做什么。
