---
title: "通过 I2P 使用 Git（面向用户）"
date: 2020-03-06
author: "idk"
description: "通过 I2P 使用 Git"
categories: ["development"]
---

通过 I2P Tunnel（隧道）设置 git 访问的教程。这个 tunnel 将作为你在 I2P 上访问单个 git 服务的接入点。它是将 I2P 从 monotone 迁移到 Git 的整体工作的一部分。

## 在做任何其他事情之前：了解该服务向公众提供的功能

取决于 Git 服务的配置方式，它不一定会在同一地址上提供所有服务。以 git.idk.i2p 为例，它提供一个公共的 HTTP URL，以及一个供你的 Git SSH 客户端配置使用的 SSH URL。两者均可用于推送或拉取，但推荐使用 SSH。

## 首先：在 Git 服务上注册一个账户

要在远程 git 服务上创建你的仓库，请先在该服务注册一个用户账户。当然，也可以在本地创建仓库，然后将其推送到远程 git 服务，但大多数服务都会要求你拥有账户，并且先在服务器上为其创建对应的远程仓库。

## 第二步：创建一个用于测试的项目

为了确保设置流程正常工作，建议在服务器上创建一个用于测试的仓库。访问 i2p-hackers/i2p.i2p 仓库，并将其 fork（派生）到你的账户下。

## 第三步：设置你的 git 客户端 tunnel

要获得对服务器的读写访问权限，你需要为你的 SSH 客户端设置一个 tunnel。如果你只需要通过 HTTP/S 进行只读克隆，那么你可以跳过这些，直接使用 http_proxy 环境变量，把 git 配置为使用预先配置好的 I2P HTTP Proxy。例如：

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
要进行 SSH 访问，请从 http://127.0.0.1:7657/i2ptunnelmgr 启动 "New Tunnel Wizard"，并设置一个指向该 Git 服务的 SSH base32 地址的客户端 tunnel。

## 第四步：尝试克隆

现在你的 tunnel 已经设置就绪，你可以尝试通过 SSH 进行克隆：

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
你可能会遇到一个错误：远端意外断开连接。不幸的是，git 仍然不支持可续传的克隆。在此之前，有几种相当简单的处理方式。首要也是最简单的方法是尝试进行浅克隆（限制历史深度）：

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
完成浅克隆后，切换到仓库目录并运行，即可以可断点续传的方式获取其余部分：

```
git fetch --unshallow
```
此时，你仍然没有所有的分支。你可以通过运行以下命令来获取它们：

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## 面向开发者的建议工作流程

只要使用得当，版本控制才能发挥最佳效果！我们强烈建议采用 fork-first（先 fork）、feature-branch（功能分支）的工作流程：

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```