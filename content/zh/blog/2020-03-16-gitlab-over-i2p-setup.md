---
title: "在 I2P 上设置 Gitlab"
date: 2020-03-16
author: "idk"
description: "为他人镜像 I2P Git 仓库并桥接 Clearnet（明网）仓库"
categories: ["development"]
---

这是我用于配置 Gitlab 和 I2P 的设置流程，使用 Docker 来管理服务本身。以这种方式在 I2P 上托管 Gitlab 非常容易，由一人管理也并不困难。这些说明适用于任何基于 Debian 的系统，并且可以很容易地移植到任何具备 Docker 和 I2P router 的系统上。

## 依赖项与 Docker

由于 Gitlab 在容器中运行，我们只需在主系统上安装容器所需的依赖项。方便的是，可以通过以下方式安装所需的一切：

```
sudo apt install docker.io
```
## 获取 Docker 容器

安装好 Docker 后，你可以获取 GitLab 所需的 Docker 容器。*先不要运行它们。*

```
docker pull gitlab/gitlab-ce
```
## 为 Gitlab 设置 I2P HTTP 代理（重要信息，可选步骤）

I2P 内的 Gitlab 服务器可以在有或没有与 I2P 之外的互联网服务器交互能力的情况下运行。若 Gitlab 服务器*不允许*与 I2P 之外的服务器交互，则无法通过从 I2P 之外的互联网上的 git 服务器克隆一个 git 仓库来对其进行去匿名化。

在 Gitlab 服务器被*允许*与 I2P 之外的服务器交互的情况下，它可以作为用户的"Bridge（桥接器）"，用户可以利用它将 I2P 之外的内容镜像到 I2P 可访问的源，不过在这种情况下它*并非匿名*。

**如果你想要一个桥接的、非匿名的 Gitlab 实例，并且能够访问 Web 仓库**，无需进一步修改。

**如果你想要一个仅 I2P 的 Gitlab 实例，且无法访问仅 Web 的仓库**，你需要将 Gitlab 配置为使用 I2P HTTP 代理。由于默认的 I2P HTTP 代理只在 `127.0.0.1` 上监听，你需要为 Docker 设置一个新的代理，使其监听 Docker 网络的主机/网关地址（通常是 `172.17.0.1`）。我把它配置在端口 `4446` 上。

## 在本地启动容器

完成这些设置之后，你可以启动容器，并在本地发布你的 Gitlab 实例：

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
访问您的本地 Gitlab 实例，并设置管理员账户。选择一个强密码，并配置用户账户上限，使其与您的资源相匹配。

## 设置你的 Service tunnels 并注册一个主机名

在本地设置好 Gitlab 之后，前往 I2P Router 控制台。您需要设置两条 server tunnel：一条指向运行在 TCP 端口 8080 上的 Gitlab Web（HTTP）接口，另一条指向运行在 TCP 端口 8022 上的 Gitlab SSH 接口。

### Gitlab Web(HTTP) Interface

对于 Web 界面，请使用 "HTTP" 服务器 tunnel。通过 http://127.0.0.1:7657/i2ptunnelmgr 启动 "New Tunnel Wizard"，并输入以下值：

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

对于 SSH 接口，使用 "Standard" 服务器 tunnel。从 http://127.0.0.1:7657/i2ptunnelmgr 启动 "New Tunnel Wizard"，并输入以下值:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

最后，如果你修改了 `gitlab.rb` 或者注册了一个主机名，则需要重新启动 GitLab 服务以使设置生效。
