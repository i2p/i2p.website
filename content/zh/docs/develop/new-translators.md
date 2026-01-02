---
title: "新译者指南"
description: "如何通过 Transifex 或手动方法为 I2P 网站和 router console（路由控制台）贡献翻译"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

想要帮助让 I2P 惠及全球更多的人吗?翻译是您能为项目做出的最有价值的贡献之一。本指南将引导您完成 router console 的翻译工作。

## 翻译方法

有两种方式可以贡献翻译：

### 方法1：Transifex（推荐）

**这是翻译 I2P 最简单的方法。** Transifex 提供了一个基于网页的界面,使翻译变得简单易用。

1. 在 [Transifex](https://www.transifex.com/otf/I2P/) 注册
2. 申请加入 I2P 翻译团队
3. 直接在浏览器中开始翻译

无需技术知识 - 只需注册即可开始翻译!

### 方法 2：手动翻译

对于喜欢使用 git 和本地文件工作的翻译人员,或者对于尚未在 Transifex 上设置的语言。

**要求：** - 熟悉 git 版本控制 - 文本编辑器或翻译工具（推荐使用 POEdit） - 命令行工具：git、gettext

**设置：** 1. 加入 [IRC 上的 #i2p-dev](/contact/#irc) 并介绍自己 2. 在 wiki 上更新翻译状态（在 IRC 中请求访问权限）3. 克隆相应的仓库（见下面的章节）

---

## 路由器控制台翻译

路由器控制台是运行 I2P 时看到的网页界面。翻译它可以帮助那些不熟悉英语的用户。

### 使用 Transifex（推荐）

1. 访问 [Transifex 上的 I2P](https://www.transifex.com/otf/I2P/)
2. 选择 router console 项目
3. 选择你的语言
4. 开始翻译

### 手动翻译路由器控制台

**前提条件：** - 与网站翻译相同（git、gettext） - GPG密钥（用于提交访问） - 已签署的开发者协议

**克隆 I2P 主仓库：**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**待翻译文件：**

路由器控制台大约有 15 个文件需要翻译:

1. **核心界面文件：**
   - `apps/routerconsole/locale/messages_*.po` - 主控制台消息
   - `apps/routerconsole/locale-news/messages_*.po` - 新闻消息

2. **代理文件：**
   - `apps/i2ptunnel/locale/messages_*.po` - Tunnel 配置界面

3. **应用程序语言包：**
   - `apps/susidns/locale/messages_*.po` - 地址簿界面
   - `apps/susimail/locale/messages_*.po` - 电子邮件界面
   - 其他应用程序特定的语言包目录

4. **文档文件：**
   - `installer/resources/readme/readme_*.html` - 安装说明文档
   - 各种应用程序中的帮助文件

**翻译工作流程：**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**提交您的工作：** - 在 [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) 上创建合并请求 - 或在 IRC 上与开发团队分享文件

---

## 翻译工具

### POEdit（强力推荐）

[POEdit](https://poedit.net/) 是一个专门用于 .po 翻译文件的编辑器。

**功能：** - 可视化翻译工作界面 - 显示翻译上下文 - 自动验证 - 支持 Windows、macOS 和 Linux

### 文本编辑器

您也可以使用任何文本编辑器： - VS Code（配合 i18n 扩展） - Sublime Text - vim/emacs（适合终端用户）

### 质量检查

提交前：1. **检查格式：** 确保占位符如 `%s` 和 `{0}` 保持不变 2. **测试您的翻译：** 安装并运行 I2P 以查看显示效果 3. **一致性：** 保持各文件术语的一致性 4. **长度：** 某些字符串在用户界面中有空间限制

---

## 翻译者提示

### 通用指南

- **保持一致性：** 在整个翻译过程中对常用术语使用相同的译法
- **保持格式：** 保留 HTML 标签、占位符（`%s`、`{0}`）和换行符
- **注重上下文：** 仔细阅读英文原文以理解上下文
- **提出问题：** 如果有不清楚的地方，可以使用 IRC 或论坛提问

### 常见 I2P 术语

某些术语应保持英文或谨慎音译：

- **I2P** - 保持不变
- **eepsite** - I2P网站(一种匿名网站)
- **tunnel** - 连接路径(避免使用Tor术语如"电路")
- **netDb** - 网络数据库
- **floodfill** - 一种router类型
- **destination** - I2P地址端点

### 测试您的翻译

1. 使用你的翻译构建 I2P
2. 在路由器控制台设置中更改语言
3. 浏览所有页面以检查:
   - 文本适合 UI 元素
   - 没有乱码字符(编码问题)
   - 翻译在上下文中有意义

---

## 常见问题

### 为什么翻译过程如此复杂？

该流程使用版本控制（git）和标准翻译工具（.po 文件），因为：

1. **问责制：** 跟踪谁在何时更改了什么
2. **质量：** 在更改上线之前进行审核
3. **一致性：** 维护正确的文件格式和结构
4. **可扩展性：** 高效管理多语言翻译
5. **协作：** 多个译者可以同时处理同一种语言

### 我需要编程技能吗？

**不需要！** 如果您使用 Transifex，您只需要：- 精通英语和您的目标语言 - 一个网页浏览器 - 基本的计算机技能

对于手动翻译，你需要基本的命令行知识，但不需要编写代码。

### 需要多长时间?

- **Router console（路由控制台）：** 所有文件大约需要 15-20 小时
- **维护：** 每月需要几小时来更新新字符串

### 多个人可以共同翻译一种语言吗?

是的！协调工作是关键：- 使用 Transifex 进行自动协调 - 对于手动工作，在 #i2p-dev IRC 频道中沟通 - 按章节或文件划分工作

### 如果我的语言没有列出怎么办？

在 Transifex 上请求或通过 IRC 联系团队。开发团队可以快速设置新语言。

### 在提交之前，我如何测试我的翻译？

- 使用你的翻译从源码构建 I2P
- 在本地安装并运行
- 在控制台设置中更改语言

---

## 获取帮助

### IRC 支持

加入 [IRC 上的 #i2p-dev](/contact/#irc) 获取：- 翻译工具的技术帮助 - I2P 术语相关问题解答 - 与其他翻译者协调 - 开发者的直接支持

### 论坛

- 在 [I2P Forums](http://i2pforum.net/) 上进行翻译讨论
- I2P 内部：zzz.i2p 上的翻译论坛（需要 I2P router）

### 文档

- [Transifex 文档](https://docs.transifex.com/)
- [POEdit 文档](https://poedit.net/support)
- [gettext 手册](https://www.gnu.org/software/gettext/manual/)

---

## 致谢

所有译者将获得署名，署名位置包括：
- I2P router 控制台（关于页面）
- 网站致谢页面
- Git 提交历史
- 发布公告

您的工作直接帮助世界各地的人们安全、私密地使用I2P。感谢您的贡献!

---

## 下一步

准备好开始翻译了吗？

1. **选择你的方式：**
   - 快速开始：[在 Transifex 上注册](https://www.transifex.com/otf/I2P/)
   - 手动方式：加入 [IRC 上的 #i2p-dev 频道](/contact/#irc)

2. **从小做起：** 先翻译几个字符串以熟悉流程

3. **寻求帮助：** 不要犹豫在 IRC 或论坛上寻求帮助

**感谢您帮助让 I2P 为每个人所用！**
