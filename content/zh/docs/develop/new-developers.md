---
title: "新开发者指南"
description: "如何开始为 I2P 做贡献：学习材料、源代码、构建、想法、发布、社区、翻译和工具"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: 更新翻译部分
---

所以你想开始为 I2P 做贡献？太好了！这里有一个快速指南，帮助你开始为网站或软件做贡献、进行开发或创建翻译。

还没准备好编程？先尝试[参与进来](/get-involved/)。

## 了解 Java

I2P router及其嵌入式应用程序使用Java作为主要开发语言。如果您没有Java经验,可以随时查看[Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

学习操作入门、其他"操作指南"文档、技术介绍以及相关文档：

- 介绍指南：[I2P 简介](/docs/overview/intro/)
- 文档中心：[文档](/docs/)
- 技术介绍：[技术简介](/docs/overview/tech-intro/)

这些将为您提供关于 I2P 结构以及其不同功能的良好概述。

## 获取 I2P 代码

对于 I2P router 或嵌入式应用程序的开发,您需要获取源代码。

### 我们当前的方式：Git

I2P 拥有官方的 Git 服务，并通过我们自己的 GitLab 接受贡献：

- I2P 内部：<http://git.idk.i2p>
- I2P 外部：<https://i2pgit.org>

克隆主仓库：

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
GitHub 上也提供只读镜像：

- GitHub 镜像：[github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## 构建 I2P

要编译代码,你需要 Sun/Oracle Java Development Kit 6 或更高版本,或等效的 JDK(强烈推荐使用 Sun/Oracle JDK 6)以及 Apache Ant 1.7.0 或更高版本。如果你正在处理主要的 I2P 代码,请进入 `i2p.i2p` 目录并运行 `ant` 来查看构建选项。

要构建或处理控制台翻译，您需要 GNU gettext 软件包中的 `xgettext`、`msgfmt` 和 `msgmerge` 工具。

对于新应用程序的开发，请参阅[应用程序开发指南](/docs/develop/applications/)。

## 开发想法

查看项目 TODO 列表或 GitLab 上的问题列表以获取想法：

- GitLab 问题：[i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## 提供结果

请参阅许可证页面底部了解提交权限要求。您需要这些权限才能将代码提交到 `i2p.i2p`（网站不需要！）。

- [许可证页面](/docs/develop/licenses#commit)

## 了解我们！

开发者们经常在 IRC 上活动。您可以在各种网络以及 I2P 内部网络上找到他们。通常可以在 `#i2p-dev` 频道找到他们。加入频道并打个招呼吧!我们还为常规开发者提供了额外的[指南](/docs/develop/dev-guidelines/)。

## 翻译

网站和路由器控制台翻译者：请查看[新翻译者指南](/docs/develop/new-translators/)了解后续步骤。

## 工具

I2P是开源软件,主要使用开源工具包开发。I2P项目最近获得了YourKit Java Profiler的许可证。开源项目有资格获得免费许可证,前提是在项目网站上引用YourKit。如果您有兴趣对I2P代码库进行性能分析,请与我们联系。

YourKit 慷慨地以其全功能分析器支持开源项目。YourKit, LLC 是用于分析 Java 和 .NET 应用程序的创新智能工具的创造者。了解一下 YourKit 的领先软件产品：

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
