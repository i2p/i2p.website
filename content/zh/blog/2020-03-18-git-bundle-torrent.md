---
title: "使用 git bundle 获取 I2P 源代码"
date: 2020-03-18
author: "idk"
description: "通过 Bittorrent 下载 I2P 源代码"
categories: ["development"]
---

通过 I2P 克隆大型软件仓库可能比较困难，而使用 git 有时会让事情更难。好在，它有时也能让事情更容易。Git 提供了一个 `git bundle` 命令，可以把一个 git 仓库打包成一个文件，随后 git 可以从你本地磁盘上的某个位置对该文件执行 clone、fetch 或 import。将这一能力与 bittorrent 下载结合，我们就能解决使用 `git clone` 时剩下的问题。

## 在开始之前

如果你打算生成一个 git bundle（捆绑包），你**必须**已经拥有 **git** 仓库的完整副本，而不是 mtn 仓库。你可以从 github 或从 git.idk.i2p 获取它，但浅克隆（使用 --depth=1 进行的克隆）*将无法工作*。它会静默失败，创建看起来像是一个 bundle 的东西，但当你尝试克隆它时会失败。如果你只是获取一个预先生成的 git bundle，那么本节不适用于你。

## 通过 Bittorrent 获取 I2P 源代码

需要有人向你提供一个与他们已为你生成的现有 `git bundle` 相对应的种子文件或磁力链接。一旦你通过 BitTorrent 获得了该 bundle，你需要使用 git 从它创建一个可用的仓库。

## 使用 `git clone`

从 git bundle（Git 打包文件）克隆很简单，只需：

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
如果你遇到以下错误，请尝试改为手动使用 git init 和 git fetch：

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## 使用 `git init` 和 `git fetch`

首先，创建一个名为 i2p.i2p 的目录，以便将其变成一个 Git 仓库：

```
mkdir i2p.i2p && cd i2p.i2p
```
接下来，初始化一个空的 Git 仓库，以便将更改获取（fetch）回到其中：

```
git init
```
最后，从 bundle（打包文件）中获取仓库：

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## 将 bundle 远程替换为 upstream 远程

现在你已有一个捆绑包（bundle），可以通过将远程仓库（remote）设置为上游仓库地址来跟进后续更新：

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## 生成捆绑包

首先，请按照 Git 用户指南操作，直到你拥有一个已成功 `--unshallow` 的 i2p.i2p 仓库克隆。如果你已经有一个克隆，请确保在生成种子包之前运行 `git fetch --unshallow`。

准备好之后，只需运行相应的 ant 目标：

```
ant bundle
```
并将生成的包复制到你的 I2PSnark 下载目录。例如：

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
一两分钟后，I2PSnark 会自动发现该种子。点击 "Start" 按钮开始为该种子做种。
