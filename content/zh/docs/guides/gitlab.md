---
title: "在 I2P 上运行 GitLab"
description: "使用 Docker 和 I2P router 在 I2P 内部署 GitLab"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

在 I2P 内托管 GitLab 非常简单:运行 GitLab omnibus 容器,在 loopback 上暴露服务,然后通过 I2P tunnel 转发流量。以下步骤反映了 `git.idk.i2p` 使用的配置,但适用于任何自托管实例。

## 1. 前置要求

- Debian 或其他已安装 Docker Engine 的 Linux 发行版（通过 `sudo apt install docker.io` 或从 Docker 官方仓库安装 `docker-ce`）。
- 一个具有足够带宽服务用户的 I2P router（Java I2P 或 i2pd）。
- 可选：一个专用虚拟机，以便将 GitLab 和 router 与桌面环境隔离。

## 2. 拉取 GitLab 镜像

```bash
docker pull gitlab/gitlab-ce:latest
```
官方镜像基于 Ubuntu 基础层构建,并定期更新。如果您需要额外保证,可以审查 [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile)。

## 3. 决定使用桥接模式还是纯I2P模式

- **仅 I2P** 实例永远不会联系明网主机。用户可以从其他 I2P 服务镜像仓库，但不能从 GitHub/GitLab.com 镜像。这最大化了匿名性。
- **桥接** 实例通过 HTTP 代理访问明网 Git 主机。这对于将公共项目镜像到 I2P 中很有用，但会使服务器的出站请求去匿名化。

如果您选择桥接模式，请配置 GitLab 使用绑定在 Docker 主机上的 I2P HTTP 代理（例如 `http://172.17.0.1:4446`）。默认的 router 代理仅监听 `127.0.0.1`；需要添加一个新的代理 tunnel 绑定到 Docker 网关地址。

## 4. 启动容器

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- 将发布的端口绑定到回环地址;I2P 隧道将根据需要暴露它们。
- 将 `/srv/gitlab/...` 替换为适合您主机的存储路径。

容器运行后,访问 `https://127.0.0.1:8443/`,设置管理员密码并配置账户限制。

## 5. 通过 I2P 暴露 GitLab

创建三个 I2PTunnel **服务器**隧道:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
为每个 tunnel 配置适当的 tunnel 长度和带宽。对于公共实例，3 跳配合每个方向 4-6 个 tunnel 是一个不错的起点。在您的着陆页上发布生成的 Base32/Base64 目标地址，以便用户可以配置客户端 tunnel。

### Destination Enforcement

如果您使用 HTTP(S) tunnel,请启用目的地强制验证,以便只有预期的主机名才能访问该服务。这可以防止 tunnel 被滥用为通用代理。

## 6. Maintenance Tips

- 每次更改 GitLab 设置时运行 `docker exec gitlab gitlab-ctl reconfigure`。
- 监控磁盘使用情况(`/srv/gitlab/data`)——Git 仓库增长很快。
- 定期备份配置和数据目录。GitLab 的 [备份 rake 任务](https://docs.gitlab.com/ee/raketasks/backup_restore.html) 可在容器内运行。
- 考虑在客户端模式下放置一个外部监控 tunnel,以确保服务可从更广泛的网络访问。

## 6. 维护提示

- [在你的应用程序中嵌入 I2P](/docs/applications/embedding/)
- [通过 I2P 使用 Git（客户端指南）](/docs/applications/git/)
- [用于离线/慢速网络的 Git bundles](/docs/applications/git-bundle/)

一个配置良好的 GitLab 实例可以在 I2P 内部提供一个完整的协作开发中心。保持 router 健康运行,及时更新 GitLab 安全补丁,并随着用户群体的增长与社区保持协调。
