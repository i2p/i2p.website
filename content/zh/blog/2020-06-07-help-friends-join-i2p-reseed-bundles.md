---
title: "通过分享 Reseed Bundles（重播种包），帮助你的朋友加入 I2P"
date: 2020-06-07
author: "idk"
description: "创建、交换和使用引导包（reseed bundles）"
categories: ["reseed"]
---

大多数新的 I2P router 在 reseed service（网络初始节点获取服务）的帮助下通过引导加入网络。然而，与 I2P 网络其余部分强调去中心化和不可封锁的连接相反，reseed service 是中心化的，并且相对容易被封锁。如果一个新的 I2P router 无法引导，它可以使用一个现有的 I2P router 生成一个可用的 "Reseed bundle"（离线引导包），从而在不依赖 reseed service 的情况下完成引导。

拥有一个可用的 I2P 连接的用户可以通过生成一个 reseed 文件（用于引导的种子文件），并通过秘密或未被封锁的通道将其传递给对方，从而帮助被封锁的 router 加入网络。事实上，在许多情况下，已经连接的 I2P router 完全不会受到 reseed 封锁的影响，所以**周围有可用的 I2P router 意味着现有的 I2P router 可以通过为新的 I2P router 提供一种隐蔽的引导方式来帮助其加入**。

## 生成 Reseed Bundle（引导包）

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## 从文件进行 Reseed 操作

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
