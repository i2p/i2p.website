---
title: "I2P Jpackages 迎来首次更新"
date: 2021-11-02
author: "idk"
description: "新的、更易于安装的软件包达到新里程碑"
categories: ["general"]
---

几个月前，我们发布了新软件包，希望通过让更多人更容易进行 I2P 的安装和配置，帮助新用户加入 I2P 网络。我们通过从外部 JVM 切换到 Jpackage，从安装流程中去掉了数十个步骤；同时为目标操作系统构建了标准软件包，并以操作系统可识别的方式对其进行签名，以确保用户安全。自那以后，jpackage 的 router 已达成一个新里程碑：它们即将迎来首次增量更新。这些更新将把 JDK 16 jpackage 替换为更新的 JDK 17 jpackage，并修复我们在发布后发现的一些小缺陷。

## 适用于 Mac OS 和 Windows 的通用更新

所有使用 jpackage 打包的 I2P 安装程序均包含以下更新：

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

请尽快更新。

## I2P Windows Jpackage 更新

仅适用于 Windows 的软件包将获得以下更新：

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

如需完整的更改列表，请参阅 i2p.firefox 中的 changelog.txt

## I2P Mac OS Jpackage 更新

仅限 Mac OS 的软件包获得以下更新：

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

有关开发的摘要，请参见 i2p-jpackage-mac 中的提交记录。
