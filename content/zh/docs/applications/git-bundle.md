---
title: "I2P 的 Git Bundle"
description: "使用 git bundle 和 BitTorrent 获取和分发大型代码仓库"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

当网络条件导致 `git clone` 不可靠时，你可以通过 BitTorrent 或任何其他文件传输方式将仓库作为 **git bundles** 分发。bundle 是一个包含完整仓库历史的单一文件。下载完成后，你可以从本地获取它，然后切换回上游远程仓库。

## 1. 开始之前

生成 bundle 需要**完整的** Git 克隆。使用 `--depth 1` 创建的浅克隆会静默生成看似正常但实际损坏的 bundle,当其他人尝试使用时会失败。始终从可信来源(GitHub 的 [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)、I2P Gitea 实例 [i2pgit.org](https://i2pgit.org),或通过 I2P 访问 `git.idk.i2p`)获取代码,并在创建 bundle 之前运行 `git fetch --unshallow` 将任何浅克隆转换为完整克隆(如有必要)。

如果您只是使用现有的捆绑包,只需下载即可。无需特殊准备。

## 2. 下载安装包

### Obtaining the Bundle File

使用 I2PSnark(I2P 内置的种子客户端)或其他兼容 I2P 的客户端(如安装了 I2P 插件的 BiglyBT)通过 BitTorrent 下载捆绑包文件。

**重要**:I2PSnark 仅适用于专为 I2P 网络创建的种子文件。标准明网种子文件不兼容,因为 I2P 使用 Destination(387+ 字节地址)而非 IP 地址和端口。

bundle 文件的位置取决于你的 I2P 安装类型:

- **用户/手动安装**（使用 Java 安装程序安装）：`~/.i2p/i2psnark/`
- **系统/守护进程安装**（通过 apt-get 或包管理器安装）：`/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT 用户可以在配置的下载目录中找到已下载的文件。

### Cloning from the Bundle

**标准方法**(适用于大多数情况):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
如果遇到 `fatal: multiple updates for ref` 错误(这是 Git 2.21.0 及更高版本中的已知问题,当全局 Git 配置包含冲突的 fetch refspec 时会出现),请使用手动初始化方法:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
或者,您可以使用 `--update-head-ok` 标志:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### 获取 Bundle 文件

从 bundle 克隆后,将你的克隆指向实时远程仓库,以便将来的拉取操作通过 I2P 或明网进行:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
或者用于访问明网：

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
要访问 I2P SSH，你需要在 I2P 路由器控制台中配置一个 SSH 客户端 tunnel（通常是端口 7670），指向 `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`。如果使用非标准端口：

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### 从捆绑包克隆

确保您的仓库完全是最新的，使用**完整克隆**（不是浅克隆）：

```bash
git fetch --all
```
如果你有一个浅克隆(shallow clone),请先转换它:

```bash
git fetch --unshallow
```
### 切换到实时远程环境

**使用 Ant 构建目标**（推荐用于 I2P 源代码树）：

```bash
ant git-bundle
```
这将创建 `i2p.i2p.bundle`(bundle 文件)和 `i2p.i2p.bundle.torrent`(BitTorrent 元数据)。

**直接使用 git bundle**:

```bash
git bundle create i2p.i2p.bundle --all
```
对于更有选择性的捆绑包:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

在分发之前务必验证 bundle:

```bash
git bundle verify i2p.i2p.bundle
```
这确认了 bundle 是有效的,并显示任何所需的前提 commit。

### 前置要求

将 bundle 及其 torrent 元数据复制到你的 I2PSnark 目录中:

**对于用户安装**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**对于系统安装**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark 会在几秒钟内自动检测并加载 .torrent 文件。访问 Web 界面 [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) 即可开始做种。

## 4. Creating Incremental Bundles

对于定期更新,创建增量包,仅包含自上次打包以来的新提交:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
如果用户已经有基础仓库，可以从增量包中获取：

```bash
git fetch /path/to/update.bundle
```
始终验证增量包显示预期的前置提交:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

当你从 bundle 获得一个可用的仓库后,就可以像对待其他 Git 克隆一样使用它:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
或者对于更简单的工作流程:

```bash
git fetch origin
git pull origin master
```
## 3. 创建 Bundle

- **弹性分发**:大型仓库可以通过 BitTorrent 共享,它能自动处理重试、分片验证和断点续传。
- **点对点引导**:新贡献者可以从 I2P 网络上的邻近节点引导克隆其仓库,然后直接从 Git 主机获取增量更改。
- **降低服务器负载**:镜像可以发布定期打包文件来减轻实时 Git 主机的压力,这对大型仓库或慢速网络环境特别有用。
- **离线传输**:打包文件可在任何文件传输方式上使用(USB 驱动器、直接传输、人肉网络),不仅限于 BitTorrent。

Bundles 不会取代实时远程仓库。它们只是为初始克隆或重大更新提供了一种更具弹性的引导方法。

## 7. Troubleshooting

### 生成 Bundle

**问题**：Bundle 创建成功，但其他人无法从 bundle 克隆。

**原因**:你的源代码克隆是浅克隆(使用 `--depth` 创建)。

**解决方案**:在创建 bundle 之前转换为完全克隆:

```bash
git fetch --unshallow
```
### 验证您的软件包

**问题**：从 bundle 克隆时出现 `fatal: multiple updates for ref` 错误。

**原因**:Git 2.21.0+ 与 `~/.gitconfig` 中的全局 fetch refspecs 存在冲突。

**解决方案**：1. 使用手动初始化：`mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. 使用 `--update-head-ok` 标志：`git fetch --update-head-ok /path/to/bundle '*:*'` 3. 删除冲突的配置：`git config --global --unset remote.origin.fetch`

### 通过 I2PSnark 分发

**问题**：`git bundle verify` 报告缺少前置条件。

**原因**:增量包或不完整的源代码克隆。

**解决方案**:要么获取前置提交(prerequisite commits),要么先使用基础包(base bundle),然后应用增量更新。
