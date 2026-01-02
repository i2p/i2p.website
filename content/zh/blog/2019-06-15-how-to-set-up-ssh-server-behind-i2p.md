---
title: "如何在 I2P 背后设置用于个人访问的 SSH 服务器"
date: 2019-06-15
author: "idk"
description: "通过 I2P 的 SSH"
---

# 如何在 I2P 背后设置用于个人访问的 SSH 服务器

本教程介绍如何设置并微调一个 I2P tunnel，从而通过 I2P 或 i2pd 远程访问 SSH 服务器。目前假设您会通过包管理器安装 SSH 服务器，并且它作为服务运行。

Considerations: In this guide, I'm assuming a few things. They will need to be adjusted depending on the complications that arise in your particular setup, especially if you use VM's or containers for isolation. This assumes that the I2P router and the ssh server are running on the same localhost. You should be using newly-generated SSH host keys, either by using a freshly installed sshd, or by deleting old keys and forcing their re-generation. For example:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

使用 java I2P 的 Web 界面，前往 [隐藏服务管理器](http://127.0.0.1:7657/i2ptunnelmgr)，并启动 tunnel 向导。

#### Tunnel Wizard

由于你正在为 SSH 服务器设置此 tunnel，你需要选择 "Server" tunnel 类型。

**截图占位符：** 使用向导创建“Server” tunnel

你应该稍后再进行微调，但 Standard tunnel 类型最容易上手。

**截图占位符：** “Standard” 类型

给它一个好的描述：


**截图占位符：** 说明其用途

并告诉它 SSH 服务器将在哪可用。

**截图占位符:** 将其指向你将来要部署的 SSH 服务器的位置

查看结果，并保存您的设置。

**截图占位符：** 保存设置。

#### Advanced Settings

现在返回 Hidden Services Manager（隐藏服务管理器），查看可用的高级设置。你肯定需要更改的一项是：将其设置为用于交互式连接，而不是批量连接。

**截图占位符:** 配置您的 tunnel 以支持交互式连接

此外，这些其他选项在访问你的 SSH 服务器时也会影响性能。如果你对匿名性没有那么在意，可以减少所经过的跳数。如果你遇到速度方面的问题，增大 tunnel 数量可能会有所帮助。配置几个备用 tunnel 可能是个好主意。你可能需要稍微微调一下。

**截图占位符：** 如果你不在意匿名性，就缩短 tunnel 长度。

最后，重启 tunnel 以使所有设置生效。

另一个值得关注的设置，尤其是在你选择运行大量的 tunnels 时，是 "Reduce on Idle"，它会在服务器长时间处于空闲状态时减少运行的 tunnels 数量。

**截图占位符：** 空闲时减少，如果你选择了较多的 tunnels

### Using i2pd

在 i2pd 中，所有配置都通过文件完成，而不是通过 Web 界面。要为 i2pd 配置一个 SSH 服务 tunnel，请根据您的匿名性和性能需求调整以下示例设置，并将这些设置复制到 tunnels.conf 中。

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## 步骤一：为 SSH 服务器设置 I2P tunnel

根据你打算如何访问你的 SSH 服务器，你可能需要对设置做一些更改。除了在所有 SSH 服务器上都应进行的那些显而易见的加固措施（如公钥认证、禁止 root 登录等）之外，如果你不希望你的 SSH 服务器在除你的 server tunnel 之外的任何地址上监听，你应将 AddressFamily 设置为 inet，并将 ListenAddress 设置为 127.0.0.1。

```
AddressFamily inet
ListenAddress 127.0.0.1
```
如果您选择为 SSH 服务器使用 22 以外的端口，则需要在您的 I2P tunnel 配置中更改该端口。

## Step Three: Set up I2P tunnel for SSH Client

为配置你的客户端连接，你需要能够查看该 SSH 服务器的 I2P router 控制台。此设置的一个优点是，首次连接 I2P tunnel 时会进行身份验证，在一定程度上降低了你与 SSH 服务器的初始连接遭受 MITM（中间人攻击）风险的可能性，而这在首次信任（Trust-On-First-Use, TOFU）场景中是一种风险。

### 使用 Java I2P

#### Tunnel 向导

首先，从隐藏服务管理器启动 tunnel 配置向导，并选择一个客户端 tunnel。

**截图占位符:** 使用向导创建客户端 tunnel

接下来，选择标准的 tunnel 类型。您稍后将对该配置进行微调。

**屏幕截图占位符：** 标准版

请为其提供一个好的描述。

**截图占位符：** 请提供一个好的描述

这是唯一稍微有点棘手的部分。前往 I2P router 控制台的隐藏服务管理器，找到 SSH 服务器 tunnel 的 base64 "local destination"。你需要想办法把这条信息复制到下一步。我通常通过 [Tox](https://tox.chat) 把它发给自己，对大多数人而言，任何 off-the-record（不留记录的）方式都足够了。

**截图占位符：** 找到你要连接的目标地址

一旦你找到要连接的 base64 Destination（I2P 目标标识），并将其传送到你的客户端设备上后，就把它粘贴到客户端 Destination 字段中。

**截图占位符：** 附上目标地址

最后，设置一个本地端口，供您的 SSH 客户端连接。该本地端口将连接到 Base64 目标地址，从而连接到 SSH 服务器。

**截图占位符：** 选择一个本地端口

决定是否要让它自动启动。

**截图占位符：** 决定是否希望其自动启动

#### 高级设置

像之前一样，您需要将设置调整为针对交互式连接进行优化。另外，如果您想在服务器上设置客户端白名单，应选中“生成密钥以启用持久的客户端 tunnel 标识”单选按钮。

**截图占位符:** 将其配置为交互式

### Using i2pd

您可以通过在 tunnels.conf 中添加以下行来完成设置，并根据您的性能与匿名性需求进行调整。

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

通过多种方式都可以设置 SSH 客户端以在 I2P 上连接到你的服务器，但为了匿名使用，你还应采取一些措施来保护你的 SSH 客户端。首先，你应将其配置为仅使用单一且特定的密钥向 SSH 服务器标识自身，从而避免你的匿名与非匿名 SSH 连接发生交叉关联的风险。

请确保您的 $HOME/.ssh/config 中包含以下几行：

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
或者，你可以添加一个 .bash_alias 条目，以强制应用你的选项并自动连接到 I2P。要点是：你需要强制启用 IdentitiesOnly，并提供一个身份文件。

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

这基本上是可选的，但它挺酷的，而且还能防止任何人即便偶然发现你的 destination（目的地），也看不出你在提供 SSH 服务。

首先，获取持久化的客户端 tunnel 的 Destination（目标地址），并将其发送到服务器。

**截图占位符：** 获取客户端目标地址

将客户端的 base64 destination（目标地址）添加到服务器的 destination 白名单中。现在，你将只能从那个特定的客户端 tunnel 连接到服务器 tunnel，其他任何人都无法连接到该 destination。

**Screenshot placeholder:** And paste it onto the server whitelist

双向认证才是王道。

**注意:** 原始帖子中引用的图像需要添加到 `/static/images/` 目录: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
