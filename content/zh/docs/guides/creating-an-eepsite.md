---
title: "创建 I2P Eepsite（I2P 内部网站）"
description: "了解如何使用内置的 Jetty Web 服务器在 I2P 网络上创建并托管您自己的网站"
lastUpdated: "2025-11"
toc: true
---

## 什么是 Eepsite（I2P 上的隐藏网站）？

**eepsite** 是仅存在于 I2P 网络中的网站（I2P 内部网站）。与可通过明网（clearnet）访问的传统网站不同，eepsite 只能通过 I2P 访问，为站点运营者和访问者提供匿名性与隐私保护。Eepsites 使用 `.i2p` 伪顶级域名，并可通过特殊的 `.b32.i2p` 地址或在 I2P 地址簿中注册的人类可读名称进行访问。

所有 Java I2P 部署都预装并预配置了 [Jetty](https://jetty.org/index.html)，一款轻量级的基于 Java 的 Web 服务器。这使您能够在几分钟内轻松开始托管自己的 eepsite——无需额外安装任何软件。

本指南将带你逐步完成使用 I2P 内置工具创建并配置你的第一个 eepsite（I2P 上的匿名网站）的过程。

---

## 步骤 1：访问隐藏服务管理器

隐藏服务管理器（也称为 I2P Tunnel Manager）是用于配置所有 I2P 服务器和客户端 tunnels 的地方，包括 HTTP 服务器（eepsites）。

1. 打开你的 [I2P Router Console](http://127.0.0.1:7657)
2. 前往 [隐藏服务管理器](http://127.0.0.1:7657/i2ptunnelmgr)

你应该会看到隐藏服务管理器界面显示: - **状态消息** - 当前 tunnel 和客户端状态 - **全局 Tunnel 控制** - 用于一次性管理所有 tunnels 的按钮 - **I2P 隐藏服务** - 已配置的服务器 tunnels 列表

![隐藏服务管理器](/images/guides/eepsite/hidden-services-manager.png)

默认情况下，你会看到一个已配置但未启动的 **I2P Web 服务器** 条目。这是一个已预先配置、可供你使用的 Jetty Web 服务器。

---

## 步骤 2：配置你的 Eepsite（I2P 上的匿名网站）服务器设置

在隐藏服务列表中点击 **I2P Web 服务器** 条目以打开服务器配置页面。你可以在这里自定义你的 eepsite 设置。

![Eepsite 服务器设置](/images/guides/eepsite/webserver-settings.png)

### 配置选项详解

**Name** - 这是你的 tunnel 的内部标识符 - 在你运行多个 eepsites 时，这有助于分辨哪个是哪个 - 默认: "I2P webserver"

**Description** - 对你的 eepsite 的简要描述，供你自己参考 - 仅在 Hidden Services Manager（隐藏服务管理器）中对你可见 - 示例: "My eepsite" 或 "Personal blog"

**自动启动 Tunnel** - **重要**：选中此复选框可在 I2P router 启动时自动启动您的 eepsite - 确保在 router 重启后无需人工干预，您的站点仍保持可用 - 建议：**启用**

**目标（主机和端口）** - **主机**：您的 Web 服务器运行所在的本地地址（默认：`127.0.0.1`） - **端口**：您的 Web 服务器监听的端口（默认：Jetty 使用 `7658`） - 如果您使用的是预装的 Jetty Web 服务器，**请将这些保持为默认值** - 仅在您在其他端口上运行自定义 Web 服务器时才需要更改

**网站主机名** - 这是你的 eepsite 的人类可读 `.i2p` 域名 - 默认：`mysite.i2p`（占位符） - 你可以注册一个自定义域名，例如 `stormycloud.i2p` 或 `myblog.i2p` - 如果你只想使用自动生成的 `.b32.i2p` 地址（供 outproxies（出口代理）使用），请留空 - 有关如何申领自定义主机名，请参见下文的[注册你的 I2P 域名](#registering-your-i2p-domain)

**Local Destination** - 这是你的 eepsite 的唯一加密标识（Destination 地址） - 在首次创建 tunnel 时自动生成 - 可以把它看作你的网站在 I2P 上的永久“IP 地址” - 那串很长的字母数字字符串是你的网站 `.b32.i2p` 地址的编码形式

**私钥文件** - 你的 eepsite 私钥的存放位置 - 默认：`eepsite/eepPriv.dat` - **请确保此文件安全** - 任何能够访问此文件的人都可以冒充你的 eepsite - 切勿共享或删除此文件

### 重要说明

黄色警告框提醒你：要启用二维码生成或注册认证功能，必须配置一个带有 `.i2p` 后缀的网站主机名（例如，`mynewsite.i2p`）。

---

## 步骤 3：高级网络选项（可选）

如果你在配置页面向下滚动，你会发现高级网络选项。**这些设置是可选的** - 默认设置对大多数用户来说效果良好。不过，你可以根据你的安全需求和性能需求进行调整。

### Tunnel 长度选项

![Tunnel 长度与数量选项](/images/guides/eepsite/tunnel-options.png)

**Tunnel 长度** - **默认**: 3 跳 tunnel（高匿名性） - 控制请求在到达你的 eepsite 之前要经过多少个 router 跳 - **跳数越多 = 匿名性越高，但性能更慢** - **跳数越少 = 性能更快，但匿名性降低** - 选项范围为 0–3 跳，并可设置可变范围（variance） - **建议**: 除非有特定的性能需求，请保持为 3 跳

**Tunnel 变动范围** - **默认**：0 跳数变动（无随机化，性能稳定） - 为提升安全性，在 tunnel 长度上加入随机化 - 示例："0-1 hop variance" 表示 tunnels 将随机为 3 或 4 跳 - 提高不可预测性，但可能导致加载时间不一致

### Tunnel 数量选项

**数量 (入站/出站 tunnels)** - **默认**: 2 个入站、2 个出站 tunnels (标准带宽与可靠性) - 控制为你的 eepsite 分配的并行 tunnels 数量 - **更多 tunnels = 更好的可用性与负载处理能力，但资源占用更高** - **更少的 tunnels = 更低的资源占用，但冗余降低** - 大多数用户的建议值：2/2（默认） - 高流量站点使用 3/3 或更高可能更有利

**备份数量** - **默认**: 0 个备份 tunnels（通道）（无冗余，不增加资源占用） - 主 tunnels 故障时自动启用的待机 tunnels - 提高可靠性，但会消耗更多带宽和 CPU - 大多数个人 eepsites（I2P 站点）不需要备份 tunnels

### POST 限制

![POST 限制配置](/images/guides/eepsite/post-limits.png)

如果你的 eepsite 包含表单（联系表单、评论区、文件上传等），可以配置 POST 请求限制以防止滥用：

**每个客户端的限制** - **每个周期**: 来自单个客户端的最大请求数（默认：每 5 分钟 6 次） - **封禁时长**: 封禁滥用客户端的持续时间（默认：20 分钟）

**总限制** - **总量**：所有客户端合计的最大 POST 请求数（默认：每5分钟20次） - **封禁时长**：超过限制时拒绝所有 POST 请求的持续时间（默认：10分钟）

**POST 限制周期** - 用于衡量请求速率的时间窗口 (默认: 5 分钟)

这些限制有助于防范垃圾信息、拒绝服务攻击以及对自动化表单提交的滥用。

### 何时调整高级设置

- **高流量社区站点**: 增加 tunnel 数量 (3-4 条入站/出站)
- **性能关键型应用**: 将 tunnel 长度降至 2 跳 (存在隐私权衡)
- **需要最大匿名性**: 保持 3 跳，增加 0-1 的随机偏差
- **存在正当高频使用的表单**: 相应提高 POST 限制
- **个人博客/作品集**: 使用全部默认设置

---

## 步骤 4：向你的 Eepsite（I2P 内部网站）添加内容

现在你的 eepsite 已经配置完成，你需要将你的网站文件（HTML、CSS、图像等）添加到 Web 服务器的文档根目录中。其位置会因操作系统、安装类型以及 I2P 实现而有所不同。

### 查找您的文档根目录

**网站根目录**（通常称为 `docroot`）是存放你的网站全部文件的文件夹。你的 `index.html` 文件应直接放在该文件夹中。

#### Java I2P（标准发行版）

**Linux** - **标准安装**: `~/.i2p/eepsite/docroot/` - **软件包安装（作为服务运行）**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **标准安装**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - 典型路径: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Windows 服务安装**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - 典型路径: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **标准安装**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+（I2P 增强型发行版）

I2P+ 使用与 Java I2P 相同的目录结构。请根据您的操作系统，按照上面的路径进行操作。

#### i2pd (C++ 实现)

**Linux/Unix** - **默认**: `/var/lib/i2pd/eepsite/` 或 `~/.i2pd/eepsite/` - 请检查你的 `i2pd.conf` 配置文件，在你的 HTTP 服务器 tunnel 下查看实际的 `root` 设置

**Windows** - 在 i2pd 安装目录中检查 `i2pd.conf`

**macOS** - 通常位于： `~/Library/Application Support/i2pd/eepsite/`

### 添加您的网站文件

1. **前往你的站点根目录**，使用文件管理器或终端
2. **将你的网站文件创建或复制**到 `docroot` 文件夹中
   - 至少创建一个 `index.html` 文件（这是你的主页）
   - 按需添加 CSS、JavaScript、图像和其他资源
3. **像为任何网站那样组织子目录**：
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### 快速开始：简单的 HTML 示例

如果你刚开始使用，请在你的 `docroot` 文件夹中创建一个基本的 `index.html` 文件：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### 权限 (Linux/Unix/macOS)

如果你以服务或不同用户身份运行 I2P，请确保 I2P 进程对您的文件具有读取权限：

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### 提示

- **默认内容**: 首次安装 I2P 时，`docroot` 目录中已经包含示例内容 - 你可以随意替换
- **静态站点效果最好**: 虽然 Jetty 支持 Servlet 和 JSP，简单的 HTML/CSS/JavaScript 站点最易于维护
- **外部 Web 服务器**: 高级用户可以在不同端口上运行自定义的 Web 服务器（Apache、Nginx、Node.js 等），并将 I2P tunnel 指向它们

---

## 第 5 步：启动你的 Eepsite

既然你的 eepsite（I2P 站点）已经配置完成并且有了内容，现在是时候启动它，并让它在 I2P 网络上可访问了。

### 启动 Tunnel

1. **返回到 [隐藏服务管理器](http://127.0.0.1:7657/i2ptunnelmgr)**
2. 在列表中找到你的 **I2P Web 服务器** 条目
3. 在控制列中点击 **启动** 按钮

![运行 Eepsite](/images/guides/eepsite/eepsite-running.png)

### 等待 Tunnel 建立

点击“开始”后，你的 eepsite tunnel 将开始构建。这个过程通常需要 **30-60 秒**。请留意状态指示器：

- **红灯** = Tunnel 启动/构建中
- **黄灯** = Tunnel 部分已建立
- **绿灯** = Tunnel 完全运行并就绪

当你看到**绿色指示灯**时，你的 eepsite 已在 I2P 网络上线！

### 访问你的 Eepsite

点击正在运行的 eepsite 旁边的 **Preview** 按钮。这会在浏览器中打开一个新标签页，显示你的 eepsite 地址。

您的 eepsite 有两种类型的地址：

1. **Base32 地址 (.b32.i2p)**: 一个看起来像这样的较长的加密地址：
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - 这是你的 eepsite（I2P 上的隐藏网站）的永久、基于密码学生成的地址
   - 它无法更改，并且与你的私钥绑定
   - 即使没有域名注册也始终可用

2. **人类可读的域名（.i2p）**：如果你设置了网站主机名（例如，`testwebsite.i2p`）
   - 仅在完成域名注册后可用（见下一节）
   - 更易记忆和分享
   - 映射到你的 .b32.i2p 地址

**Copy Hostname** 按钮可让你快速复制你的完整 `.b32.i2p` 地址以便分享。

---

## ⚠️ 重要：务必备份你的私钥

在继续之前，你**必须备份**你的 eepsite（I2P 上的网站）的私钥文件。这因多种原因而至关重要：

### 为什么要备份你的密钥？

**你的私钥（`eepPriv.dat`）就是你的 eepsite（I2P 内部网站）的身份。** 它决定你的 `.b32.i2p` 地址，并证明你对 eepsite 的所有权。

- **密钥 = .b32 address（.b32 地址）**: 您的私钥会通过数学方式生成您唯一的 .b32.i2p 地址
- **无法恢复**: 如果您丢失了密钥，您将永久失去该 eepsite 地址
- **不可更改**: 如果您注册了一个指向 .b32 address 的域名，**无法更新** - 注册是永久性的
- **迁移所需**: 迁移到新电脑或重新安装 I2P 需要此密钥，才能保持相同的地址
- **支持 Multihoming（多宿主部署）**: 要从多个地点运行您的 eepsite，需要在每台服务器上使用相同的密钥

### 私钥在哪里？

默认情况下，您的私钥存储在： - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (或 对于服务安装为 `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat`) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` 或 `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

您也可以在您的 tunnel 配置中的“Private Key File”项查看/更改此路径。

### 如何备份

1. **停止你的 tunnel** (可选，但更安全)
2. **复制 `eepPriv.dat`** 到安全的位置:
   - 外接 USB 驱动器
   - 加密的备份驱动器
   - 受密码保护的归档
   - 安全的云存储 (已加密)
3. **保留多份备份**，放在不同的物理地点
4. **切勿分享此文件** - 任何拥有它的人都可以冒充你的 eepsite

### 从备份恢复

要在新系统上或重新安装后恢复您的 eepsite：

1. 安装 I2P 并创建/配置你的 tunnel 设置
2. **停止 tunnel**，再复制密钥
3. 将你备份的 `eepPriv.dat` 复制到正确的位置
4. 启动 tunnel - 它将使用你原来的 .b32 地址

---

## 如果你不注册域名

**恭喜！** 如果你不打算注册自定义的 `.i2p` 域名，你的 eepsite（I2P 隐藏网站）现在已经完成并可以正常运行了。

你可以： - 与他人分享你的 `.b32.i2p` 地址 - 使用任何支持 I2P 的浏览器通过 I2P 网络访问你的网站 - 随时在 `docroot` 文件夹中更新你的网站文件 - 在隐藏服务管理器中监控你的 tunnel 状态

**如果你想要一个人类可读的域名** (例如 `mysite.i2p`，而不是冗长的 .b32 地址)，请继续到下一节。

---

## 注册您的 I2P 域名

人类可读的 `.i2p` 域名（例如 `testwebsite.i2p`）比冗长的 `.b32.i2p` 地址更容易记忆和分享。域名注册是免费的，并会将你选择的名称关联到你的 eepsite（I2P 隐藏站点）的加密地址。

### 先决条件

- 您的 eepsite（I2P 隐藏站点）必须处于绿灯状态
- 您必须在 tunnel（隧道）配置中设置 **Website Hostname**（步骤 2）
- 例如：`testwebsite.i2p` 或 `myblog.i2p`

### 步骤 1：生成认证字符串

1. **返回到你的 tunnel 配置**，在 Hidden Services Manager（隐藏服务管理器）中
2. 点击你的 **I2P webserver（I2P Web 服务器）** 条目以打开设置
3. 向下滚动，找到 **Registration Authentication（注册认证）** 按钮

![注册身份验证](/images/guides/eepsite/registration-authentication.png)

4. 点击 **Registration Authentication**
5. **复制完整的身份验证字符串**，该字符串显示在 "Authentication for adding host [yourdomainhere]" 项下。

认证字符串将如下所示：

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
该字符串包含： - 您的域名 (`testwebsite.i2p`) - 您的目标地址 (长的密码学标识符) - 一个时间戳 - 一个密码学签名，用于证明您拥有私钥

**请保存此身份验证字符串** - 在两个注册服务中都需要用到它。

### 步骤 2：在 stats.i2p 注册

1. **前往** [stats.i2p 添加密钥](http://stats.i2p/i2p/addkey.html) (在 I2P 内)

![stats.i2p 域名注册](/images/guides/eepsite/stats-i2p-add.png)

2. **粘贴认证字符串** 到 "Authentication String" 字段
3. **添加你的姓名** (可选) - 默认为 "Anonymous"
4. **添加描述** (推荐) - 简要描述你的 eepsite 是做什么的
   - 示例: "新的 I2P Eepsite", "个人博客", "文件共享服务"
5. **勾选 "HTTP Service?"** 如果这是一个网站 (大多数 eepsites 保持勾选)
   - 对于 IRC、NNTP、代理、XMPP、git 等请取消勾选
6. 点击 **Submit**

如果成功，您将看到一条确认信息，表明您的域名已被添加到 stats.i2p 的地址簿中。

### 步骤 3：在 reg.i2p 注册

为确保最大可用性，你还应当在 reg.i2p 服务上进行注册：

1. **前往** [reg.i2p Add Domain](http://reg.i2p/add)（在 I2P 内）

![reg.i2p 域名注册](/images/guides/eepsite/reg-i2p-add.png)

2. **将相同的认证字符串粘贴** 到 "Auth string（认证字符串）" 字段
3. **添加描述**（可选，但建议提供）
   - 这有助于其他 I2P 用户了解你的网站提供的内容
4. 点击 **Submit（提交）**

你应该会收到域名已注册的确认通知。

### 步骤 4：等待传播

在向这两个服务提交之后，你的域名注册信息将通过 I2P 网络的地址簿系统传播。

**传播时间线**: - **初始注册**: 在注册服务上立即生效 - **全网传播**: 数小时到 24+ 小时 - **完全可用**: 所有 routers 完成更新可能需要最长 48 小时

**这很正常！** I2P 地址簿系统会定期更新，而不是即时生效。你的 eepsite（I2P 隐藏站点）运行正常——其他用户只需收到更新后的地址簿即可。

### 验证您的域名

几小时后，你可以测试你的域名：

1. **打开一个新的浏览器标签页** 在你的 I2P 浏览器中
2. 尝试直接访问你的域名：`http://yourdomainname.i2p`
3. 如果能够加载，你的域名已注册并正在传播！

如果仍未生效： - 多等一会儿（地址簿会按其自己的时间表更新） - 你的 router 的地址簿可能需要时间同步 - 尝试重启你的 I2P router 以强制更新地址簿

### 重要说明

- **注册是永久的**：一旦注册并完成传播，你的域名将永久指向你的`.b32.i2p`地址
- **目标不可更改**：你无法更新域名所指向的`.b32.i2p`地址——这就是为什么备份`eepPriv.dat`至关重要
- **域名所有权**：只有私钥持有者才能注册或更新该域名
- **免费服务**：I2P上的域名注册是免费的、由社区运行且去中心化
- **多个注册商**：同时在 stats.i2p 和 reg.i2p 注册可以提高可靠性和传播速度

---

## 恭喜！

您的 I2P eepsite 现已全面可用，并已注册域名！

**后续步骤**: - 向你的 `docroot` 文件夹添加更多内容 - 将你的域名分享给 I2P 社区 - 妥善保管你的 `eepPriv.dat` 备份 - 定期监控你的 tunnel（隧道）状态 - 考虑加入 I2P 论坛或 IRC 来推广你的网站

欢迎来到 I2P 网络！🎉
