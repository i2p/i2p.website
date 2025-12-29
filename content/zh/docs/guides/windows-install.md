---
title: "在 Windows 上安装 I2P"
description: "选择你的 Windows 安装方式：Easy Install Bundle（简易安装包）或标准安装"
lastUpdated: "2025-11"
toc: true
---

## 选择您的安装方式

在 Windows 上安装 I2P 有两种方式。请根据你的需求选择最合适的方法：

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">

<div style="border: 2px solid #22c55e; border-radius: 8px; padding: 1.5rem; background: var(--background-secondary);">

### 🚀 Easy Install Bundle (Recommended)

**Best for most users**

✅ All-in-one installer
✅ Java included (no separate install)
✅ Firefox profiles included
✅ Fastest setup

**Choose this if:**
- You want the simplest installation
- You don't have Java installed
- You're new to I2P

<a href="#easy-install-bundle" style="display: inline-block; background: #22c55e; color: white; padding: 0.75rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 1rem;">Easy Install Guide →</a>

</div>

<div style="border: 2px solid #1e40af; border-radius: 8px; padding: 1.5rem; background: var(--background-secondary);">

### ⚙️ Standard Installation

**For advanced users**

📦 Java-based JAR installer
🔧 More control over installation
💾 Smaller download size

**Choose this if:**
- You already have Java installed
- You want more control
- You prefer the traditional method

<a href="#standard-installation" style="display: inline-block; background: #1e40af; color: white; padding: 0.75rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 1rem;">Standard Install Guide →</a>

</div>

</div>
---

## 简易安装包

### 什么是 Easy Install Bundle（简易安装套件）？

**I2P 简易安装包**是 Windows 用户的推荐安装方式。这个一体化安装程序包含开始使用 I2P 所需的一切：

- **I2P Router** - I2P 的核心软件
- **内置 Java 运行时** - 无需单独安装 Java
- **Firefox 配置文件与扩展** - 针对 I2P 优化的浏览器配置文件与扩展，用于安全浏览
- **简易安装程序** - 无需手动配置
- **自动更新** - 让你的 I2P 软件保持最新

这个测试版安装程序通过直接捆绑 Java 来简化安装流程，因此您无需另行下载或配置 Java。

---

## 步骤 1：选择语言

启动 Easy Install Bundle 安装程序后，您会看到语言选择界面。

![语言选择](/images/guides/windows-install/language-selection.png)

1. **从下拉菜单中选择你偏好的语言**
   - 可用语言包括英语、德语、西班牙语、法语，以及许多其他语言
2. 点击 **OK** 继续

安装程序界面将在后续的所有步骤中使用您选择的语言。

---

## 步骤 2：接受许可协议

接下来，您将看到 I2P 的许可证信息。Easy Install Bundle 包含采用多种自由和开源许可证的组件。

![许可协议](/images/guides/windows-install/license-agreement.png)

**继续安装**：1. 查看许可条款（可选但推荐） 2. 点击**我同意**以接受许可条款并继续 3. 如果不希望安装，请点击**取消**

---

## 步骤 3：选择安装文件夹

现在，您将选择在计算机上安装 I2P 的位置。

![安装文件夹选择](/images/guides/windows-install/installation-folder.png)

**安装选项**:

1. **使用默认位置**（推荐）
   - 默认路径：`C:\Users\[YourUsername]\AppData\Local\I2peasy\`
   - 这会将 I2P 安装在你的用户配置文件目录中
   - 更新不需要管理员权限

2. **选择自定义位置**
   - 单击**浏览...**以选择其他文件夹
   - 如果你想安装到不同的驱动器上，这会很有用
   - 确保你对所选文件夹具有写入权限

**空间要求**: - 安装程序会显示所需的空间大小 (通常少于 1 GB) - 确保所选驱动器上有足够的可用空间

3. 点击**Install**以开始安装过程

安装程序现在会将所有必要的文件复制到您选择的位置。这可能需要几分钟。

---

## 第 4 步：完成安装并启动 I2P

安装完成后，您将看到完成界面。

![安装完成](/images/guides/windows-install/installation-complete.png)

安装向导确认 "I2P - i2peasy 已安装在您的计算机上。"

**重要**: 请确认已勾选 **"Start I2P?"** 复选框（默认情况下应已勾选）。

- **已勾选** (推荐): 当你点击 Finish 时，I2P 会自动启动
- **未勾选**: 你需要稍后从开始菜单或桌面快捷方式手动启动 I2P

单击 **完成** 以完成安装并启动 I2P。

---

## 接下来会发生什么

在勾选“启动 I2P？”后点击“完成”：

1. **I2P Router 启动** - I2P router（I2P 路由器进程）开始在后台运行
2. **系统托盘图标出现** - 在 Windows 系统托盘（右下角）中查找 I2P 图标
3. **Router 控制台打开** - 您的默认浏览器会自动打开到 I2P Router Console（通常为 `http://127.0.0.1:7657`）
4. **初始连接** - I2P 将开始连接到网络并构建 tunnels（首次启动可能需要 5-10 分钟）

**恭喜！** I2P 现已在您的 Windows 计算机上安装并运行。

---

## 推荐：端口转发（可选但很重要）

虽然并非严格要求，**端口转发会显著提升你的 I2P 使用体验**，因为它使你的 router 能与其他 I2P routers 更高效地通信。没有端口转发，你仍然可以使用 I2P，但性能会降低，对网络的贡献也会减少。

### 为什么要进行端口转发？

- **更好的连通性**: 允许来自其他 I2P routers 的入站连接
- **更快融入**: 帮助你更快地融入网络
- **网络贡献**: 使你成为 I2P 网络中更好的参与者
- **性能提升**: 通常会带来更好的 tunnel 可靠性和速度

### 查找你的 I2P 端口

首先，您需要确定 I2P 正在使用的是哪个端口（默认情况下会随机分配）。

1. **找到 I2P 图标**，它位于屏幕右下角的 Windows 系统托盘（通知区域）中

![I2P 系统托盘菜单](/images/guides/windows-install/system-tray-menu.png)

2. **右键单击 I2P 图标** 以打开上下文菜单
3. **单击 "Launch I2P Browser"** 以打开 I2P router 控制台

菜单还显示了如下实用选项： - **网络：处于防火墙后** - 显示您当前的网络状态 - **配置 I2P 系统托盘** - 自定义托盘图标设置 - **停止 I2P** / **立即停止 I2P** - 关停选项

### 查找您的端口号

当 I2P 浏览器打开后，你需要检查 I2P 正在使用哪些端口：

1. **进入网络配置页面**:
   - 在浏览器中访问 [I2P Router 网络配置](http://127.0.0.1:7657/confignet)
   - 或从 router 控制台侧边栏进入: **Configuration → Network**

2. **向下滚动** 到端口配置部分

![I2P 端口配置](/images/guides/windows-install/port-configuration.png)

3. **注意所示的端口号**:

**UDP 配置**:    - **UDP 端口**: 此处显示的端口（示例：`13697`）    - 默认情况下，此项设置为“Specify Port”（指定端口），并随机分配一个端口号

**TCP 配置**:    - **外部可达的 TCP 端口**：通常设置为使用与 UDP 相同的端口    - 在上述示例中："使用为 UDP 配置的相同端口（当前为 13697）"

**重要**: 你需要在你的 router/防火墙上，将 **UDP 和 TCP 都** 在同一个端口号上进行端口转发（本例中为端口 `13697`）。

### 如何进行端口转发

由于各个 router 和防火墙各不相同，我们无法提供通用的说明。不过，[portforward.com](https://portforward.com/) 提供了针对数千种 router 型号的详细指南：

1. 访问 **[portforward.com](https://portforward.com/)**
2. 选择你的 router 厂商和型号
3. 按照逐步指南进行端口转发
4. 在 I2P 配置中显示的端口号上同时转发 **UDP 和 TCP** 协议

**通用步骤** (因 router 而异): - 登录到你的 router 管理界面 (通常为 `192.168.1.1` 或 `192.168.0.1`) - 找到 "Port Forwarding" (端口转发) 或 "Virtual Servers" (虚拟服务器) 部分 - 为你的 I2P 端口号创建新的端口转发规则 - 同时设置 UDP 和 TCP 协议 - 将该规则指向你计算机的本地 IP 地址 - 保存配置

在设置好端口转发后，I2P 应该会在系统托盘菜单中从 "Network: Firewalled" 变为 "Network: OK"（这可能需要几分钟）。

---

## 后续步骤

- **等待网络集成**: 给 I2P 5-10 分钟以接入网络并建立 tunnels
- **配置浏览器**: 使用随附的 Firefox 配置文件进行 I2P 浏览
- **设置端口转发**: 参阅 [portforward.com](https://portforward.com/) 获取特定于 router 的关于如何转发 I2P 所使用端口的说明
- **探索 router 控制台**: 了解 I2P 的功能、服务和配置选项
- **访问 eepsites（I2P 内部网站）**: 尝试通过 I2P 网络访问 `.i2p` 网站
- **阅读文档**: 查看 [I2P 文档](/docs/) 以了解更多信息

欢迎来到 I2P 网络！🎉

---

## 标准安装

### 什么是标准安装？

**标准 I2P 安装** 是在 Windows 上安装 I2P 的传统方法。不同于 Easy Install Bundle（简易安装包），此方法需要你：

- **单独安装 Java** - 在安装 I2P 之前下载并安装 Java 运行时环境（JRE）
- **运行 JAR 安装程序** - 使用基于 Java 的图形安装程序
- **手动配置** - 自行设置浏览器配置（可选）

此方法适用于： - 已经安装了 Java 的用户 - 希望对安装过程有更多控制的高级用户 - 偏好传统安装方式的用户 - 无法与 Easy Install Bundle（简易安装包）兼容的系统

---

## 先决条件

在安装 I2P 之前，需确保系统已安装 Java。

### Java 要求

- **Java 版本**: 需要 Java 8 (1.8) 或更高版本
- **推荐**: Java 11 或更高版本（LTS，长期支持）
- **类型**: Java 运行环境 (JRE) 或 Java 开发工具包 (JDK)

### 安装 Java

如果你尚未安装 Java，你可以从多个来源下载：

**选项 1：Oracle Java** - 官方来源：[java.com/download](https://www.java.com/download) - 最广泛使用的发行版

**选项 2：OpenJDK** - 开源实现: [openjdk.org](https://openjdk.org) - 免费且开源

**选项 3: Adoptium (Eclipse Temurin)** - 推荐的替代方案：[adoptium.net](https://adoptium.net) - 免费、开源，并提供维护良好的 LTS 版本

**验证 Java 是否已安装**: 1. 打开命令提示符 (按 `Windows + R`, 输入 `cmd`, 按 Enter) 2. 输入: `java -version` 3. 你应该会看到显示 Java 版本的输出

---

## 第 1 步: 安装 Java

在安装 I2P 之前，你需要在系统上安装 Java。

1. **选择一个 Java 发行版**:
   - **Oracle Java**: [java.com/download](https://www.java.com/download)
   - **OpenJDK**: [openjdk.org](https://openjdk.org)
   - **Adoptium**: [adoptium.net](https://adoptium.net)

2. **下载 Windows 安装程序**，适用于你选择的发行版

3. **运行安装程序**，并按照安装提示进行操作

4. **验证安装**:
   - 打开命令提示符
   - 输入 `java -version` 并按 Enter 键
   - 确认已安装 Java 8 或更高版本

安装好 Java 后，你就可以开始安装 I2P 了。

---

## 第 2 步：下载并启动 I2P 安装程序

1. **下载 I2P 安装程序**:
   - 访问 [I2P 下载页面](/downloads/)
   - 下载 **Windows 安装程序**（JAR 文件）：`i2pinstall_X.X.X.jar`
   - 将其保存到便于查找的位置（例如：Downloads 文件夹）

2. **启动安装程序**:
   - 双击已下载的 JAR 文件以启动安装程序
   - 如果双击无效，右键单击该文件并选择 "打开方式 → Java(TM) Platform SE binary"
   - 或者，打开命令提示符并运行: `java -jar i2pinstall_X.X.X.jar`

## 第 3 步：选择您的语言

启动安装程序后，您将看到“语言选择”对话框。

![语言选择](/images/guides/windows-standard-install/language-selection.png)

1. **选择你的首选语言**，从下拉菜单中
   - 可用语言包括英语、德语、西班牙语、法语，以及许多其他语言
2. 点击 **OK** 以继续

安装程序会在所有后续步骤中使用您选择的语言。

---

## 步骤 4：欢迎使用 I2P 安装程序

![欢迎界面](/images/guides/windows-standard-install/welcome-screen.png)

这是安装过程中的**第 1 步（共 8 步）**。

单击 **Next** 继续安装。

---

## 步骤 5：接受许可协议

![许可协议](/images/guides/windows-standard-install/license-agreement.png)

这是安装过程中的**第 2 步（共 8 步）**。

单击**Next**以接受许可协议并继续。

---

## 步骤 6：选择安装路径

选择您希望在计算机上安装 I2P 的位置。

![安装路径](/images/guides/windows-standard-install/installation-path.png)

**默认安装路径**: `C:\Program Files (x86)\i2p\`

你可以选择： - 使用默认位置（推荐） - 点击**浏览...**以选择其他文件夹

这是安装过程中的**第3步（共8步）**。

单击**下一步**以继续。

**注意**: 如果这是你第一次安装 I2P，你会看到一个确认创建目录的弹出窗口：

![目录创建弹出窗口](/images/guides/windows-standard-install/directory-creation-popup.png)

单击 **OK** 以创建安装目录。

---

## 步骤 7：选择安装包

选择要安装的组件。

![选择包](/images/guides/windows-standard-install/select-packs.png)

**重要**: 请确保同时勾选这两个组件: - **Base** (必选) - I2P 核心软件 (27.53 MB) - **Windows Service** (推荐) - 开机时自动启动 I2P

**Windows 服务** 选项确保 I2P 会在计算机启动时自动运行，因此您无需每次手动启动它。

这是安装过程中的**第 4 步（共 8 步）**。

点击**下一步**以继续。

---

## 第 8 步：安装进度

安装程序现在将把文件复制到您的系统。

![安装进度](/images/guides/windows-standard-install/installation-progress.png)

您将看到两个进度条： - **软件包安装进度**：显示当前正在安装的软件包 - **总体安装进度**：显示总体进度（例如，"2 / 2"）

这是安装过程中的**第5步（共8步）**。

等待安装完成，然后点击 **下一步**。

---

## 步骤 9：设置快捷方式

配置要在何处创建 I2P 快捷方式。

![设置快捷方式](/images/guides/windows-standard-install/setup-shortcuts.png)

**快捷方式选项**: - ✓ **在开始菜单中创建快捷方式** (推荐) - ✓ **在桌面上创建额外的快捷方式** (可选)

**程序组**: 选择或创建用于快捷方式的文件夹名称 - 默认: `I2P` - 您可以选择现有的程序组或创建一个新的

**为以下对象创建快捷方式**: - **当前用户** - 只有你可以访问这些快捷方式 - **所有用户** - 系统中的所有用户都可以访问这些快捷方式 (需要管理员权限)

这是安装过程中的**第 6 步（共 8 步）**。

单击 **下一步** 以继续。

---

## 第 10 步：安装完成

安装已完成！

![安装完成](/images/guides/windows-standard-install/installation-complete.png)

您将看到： - ✓ **安装已成功完成** - **将会在以下位置创建卸载程序**: `C:\Program Files (x86)\i2p\Uninstaller`

这是**第 8/8 步**——安装过程中的最后一步。

点击**完成**以结束。

---

## 接下来会发生什么

点击“完成”后：

1. **I2P Router 启动** - 如果你安装了 Windows 服务，I2P 将会自动启动
2. **Router 控制台打开** - 你的默认网络浏览器将打开并访问 I2P Router 控制台，地址为 `http://127.0.0.1:7657`
3. **初始连接** - I2P 将开始连接到网络并构建 tunnels（首次启动可能需要 5-10 分钟）

**恭喜！** I2P 现已安装在您的 Windows 计算机上。

---

## 手动启动 I2P

如果 I2P 未能自动启动，或者将来你需要手动启动它，你有两种方法：

### 选项 1：开始菜单

![Windows 开始菜单](/images/guides/windows-standard-install/start-menu.png)

1. 打开 **Windows 开始菜单**
2. 导航到 **I2P** 文件夹
3. 选择以下启动选项之一：
   - **I2P router console** - 在浏览器中打开 router 控制台
   - **Start I2P (no window)** - 在后台静默启动 I2P
   - **Start I2P (restartable)** - 启动具有自动重启功能的 I2P

你也可以访问 **Open I2P Profile Folder (service)** 来查看 I2P 的配置文件。

### 选项 2：Windows 服务

![Windows 服务](/images/guides/windows-standard-install/windows-services.png)

1. 按下 **Windows + R** 打开运行对话框
2. 输入 `services.msc` 并按 Enter 键
3. 向下滚动找到 **I2P Service**
4. 右键单击 **I2P Service** 并选择：
   - **启动** - 启动 I2P 服务
   - **停止** - 停止 I2P 服务
   - **重新启动** - 重新启动 I2P 服务
   - **属性** - 配置服务设置 (启动类型等)

通过 Windows 服务的方法有助于将 I2P 作为后台服务进行管理，尤其是在你已将其安装为 Windows 服务时。

---

## 后续步骤

- **等待接入**: 给 I2P 5-10 分钟接入网络并建立 tunnels
- **配置端口转发**: 请参阅[端口转发指南](#recommended-port-forwarding-optional-but-important) 获取说明
- **配置浏览器**: 将你的网页浏览器设置为使用 I2P 的 HTTP 代理
- **探索 router 控制台**: 了解 I2P 的功能、服务和配置选项
- **访问 eepsites（I2P 内部网站）**: 尝试通过 I2P 网络访问 `.i2p` 网站
- **阅读文档**: 查看 [I2P 文档](/docs/) 了解更多信息

欢迎来到 I2P 网络！🎉
