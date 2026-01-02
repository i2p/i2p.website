---
title: "在 I2P 中使用 IDE"
description: "使用 Gradle 和捆绑项目文件为开发 I2P 配置 Eclipse 和 NetBeans"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: 文档
reviewStatus: "needs-review"
---

<p> 主要的 I2P 开发分支（<code>i2p.i2p</code>）已经配置完毕，使开发者能够轻松设置两个常用的 Java 开发 IDE：Eclipse 和 NetBeans。</p>

<h2>Eclipse</h2>

<p> 主要的 I2P 开发分支(<code>i2p.i2p</code> 及其派生分支)包含 <code>build.gradle</code> 文件,以便在 Eclipse 中轻松设置该分支。</p>

<ol> <li> 确保你安装了较新版本的 Eclipse。2017 年之后的任何版本都可以。 </li> <li> 将 I2P 分支检出到某个目录(例如 <code>$HOME/dev/i2p.i2p</code>)。 </li> <li> 选择"File → Import...",然后在"Gradle"下选择"Existing Gradle Project"。 </li> <li> 在"Project root directory:"中选择 I2P 分支检出到的目录。 </li> <li> 在"Import Options"对话框中,选择"Gradle Wrapper"并按 Continue。 </li> <li> 在"Import Preview"对话框中,你可以查看项目结构。在"i2p.i2p"下应该会出现多个项目。按"Finish"。 </li> <li> 完成!你的工作空间现在应该包含 I2P 分支中的所有项目,并且它们的构建依赖关系应该已正确设置。 </li> </ol>

<h2>NetBeans</h2>

<p> I2P 的主要开发分支(<code>i2p.i2p</code> 及其派生分支)包含 NetBeans 项目文件。</p>

<!-- Keep content minimal and close to original; will update later. -->


