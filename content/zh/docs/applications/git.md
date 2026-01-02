---
title: "Git over I2P"
description: "将 Git 客户端连接到 I2P 托管的服务,例如 i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

在 I2P 内部克隆和推送仓库使用的 Git 命令与您已经熟悉的完全相同——您的客户端只是通过 I2P tunnel 连接,而不是通过 TCP/IP。本指南将介绍如何设置账户、配置 tunnel 以及处理慢速链接的问题。

> **快速入门：** 只读访问可以通过 HTTP 代理实现：`http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`。按照以下步骤配置 SSH 读/写访问。

## 1. 创建账户

选择一个 I2P Git 服务并注册：

- I2P 内部：`http://git.idk.i2p`
- 明网镜像：`https://i2pgit.org`

注册可能需要人工审核；请查看首页获取相关说明。审核通过后，fork 或创建一个代码仓库，以便进行测试。

## 2. 配置 I2PTunnel 客户端（SSH）

1. 打开 router console → **I2PTunnel** 并添加一个新的 **Client** tunnel。
2. 输入服务的 destination(Base32 或 Base64)。对于 `git.idk.i2p`,你可以在项目主页找到 HTTP 和 SSH destinations。
3. 选择一个本地端口(例如 `localhost:7442`)。
4. 如果你计划频繁使用该 tunnel,请启用自动启动。

界面将确认新隧道并显示其状态。当隧道运行时,SSH 客户端可以连接到所选端口上的 `127.0.0.1`。

## 3. 通过 SSH 克隆

使用 tunnel 端口配合 `GIT_SSH_COMMAND` 或 SSH 配置段：

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
如果第一次尝试失败（隧道可能会很慢），请尝试浅克隆：

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
配置 Git 以获取所有分支：

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### 性能优化建议

- 在隧道编辑器中添加一到两个备份隧道以提高弹性。
- 对于测试或低风险的仓库，你可以将隧道长度减少到 1 跳，但要注意匿名性的权衡。
- 在你的环境中保留 `GIT_SSH_COMMAND` 或在 `~/.ssh/config` 中添加一个条目:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
然后使用 `git clone git@git.i2p:namespace/project.git` 进行克隆。

## 4. 工作流程建议

采用 GitLab/GitHub 上常见的 fork-and-branch 工作流程：

1. 设置上游远程仓库：`git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. 保持你的 `master` 分支同步：`git pull upstream master`
3. 为更改创建功能分支：`git checkout -b feature/new-thing`
4. 将分支推送到你的 fork：`git push origin feature/new-thing`
5. 提交合并请求,然后从上游快进你的 fork 的 master 分支。

## 5. 隐私提醒

- Git 以本地时区存储提交时间戳。要强制使用 UTC 时间戳：

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
当隐私很重要时，使用 `git utccommit` 而不是 `git commit`。

- 如果担心匿名性问题,请避免在提交消息或仓库元数据中嵌入明网 URL 或 IP 地址。

## 6. 故障排除

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
对于高级场景（镜像外部仓库、分发 bundle），请参阅配套指南：[Git bundle 工作流程](/docs/applications/git-bundle/) 和 [在 I2P 上托管 GitLab](/docs/guides/gitlab/)。
