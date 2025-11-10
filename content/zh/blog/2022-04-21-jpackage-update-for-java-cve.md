---
title: "针对 Java CVE-2022-21449 的 Jpackage 更新"
date: 2022-04-21
author: "idk"
description: "包含针对 Java CVE-2022-21449 修复的 Jpackage 捆绑包已发布"
categories: ["release"]
---

## 更新详情

新的 I2P Easy-Install 安装包已使用最新发布的 Java 虚拟机生成，该版本包含针对 CVE-2022-21449 “Psychic Signatures”的修复。建议 Easy-Install 安装包的用户尽快更新。当前的 OSX 用户将自动接收更新，Windows 用户应从我们的下载页面下载安装程序并正常运行安装程序。

在 Linux 上的 I2P router 使用宿主系统配置的 Java 虚拟机（JVM）。在这些平台上的用户应将 Java 降级到低于 Java 14 的稳定版本，以缓解该漏洞，直到软件包维护者发布更新。使用外部 JVM 的其他用户应尽快将 JVM 更新到已修复的版本。
