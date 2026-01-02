---
title: "创建和运行 I2P Reseed 服务器"
description: "完整指南：设置和运行 I2P reseed 服务器以帮助新 router 加入网络"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed 主机是 I2P 网络的关键基础设施,在引导过程中为新 router 提供初始节点组。本指南将引导您完成设置和运行自己的 reseed 服务器的过程。

## 什么是 I2P Reseed 服务器?

I2P reseed 服务器通过以下方式帮助新的 routers 集成到 I2P 网络中：

- **提供初始节点发现**：新 router 接收一组初始网络节点以建立连接
- **Bootstrap 恢复**：帮助难以维持连接的 router
- **安全分发**：重新种子化过程经过加密和数字签名，以确保网络安全

当新的 I2P router 首次启动时(或丢失了所有对等连接),它会联系 reseed 服务器下载初始的 router 信息集。这使得新 router 能够开始构建自己的 netDb 并建立 tunnel。

## 前置要求

开始之前，您需要：

- 一台 Linux 服务器(推荐 Debian/Ubuntu)并具有 root 访问权限
- 一个指向您服务器的域名
- 至少 1GB 内存和 10GB 磁盘空间
- 服务器上运行的 I2P router 以填充 netDb
- 基本熟悉 Linux 系统管理

## 准备服务器

### Step 1: Update System and Install Dependencies

首先，更新您的系统并安装所需的软件包：

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
这将安装: - **golang-go**: Go 编程语言运行时 - **git**: 版本控制系统 - **make**: 构建自动化工具 - **docker.io & docker-compose**: 用于运行 Nginx Proxy Manager 的容器平台

![安装所需软件包](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

克隆 reseed-tools 仓库并构建应用程序:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
`reseed-tools` 包提供了运行 reseed 服务器的核心功能。它负责处理：- 从本地网络数据库收集 router 信息 - 将 router info 打包成已签名的 SU3 文件 - 通过 HTTPS 提供这些文件

![克隆 reseed-tools 仓库](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

生成你的 reseed 服务器的 SSL 证书和私钥:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**重要参数**：- `--signer`：您的电子邮件地址（将 `admin@stormycloud.org` 替换为您自己的邮箱）- `--netdb`：您的 I2P router 的 netDb 路径 - `--port`：内部端口（建议使用 8443）- `--ip`：绑定到 localhost（我们将使用反向代理进行公共访问）- `--trustProxy`：信任来自反向代理的 X-Forwarded-For 头

该命令将生成：- 用于签名 SU3 文件的私钥 - 用于安全 HTTPS 连接的 SSL 证书

![SSL 证书生成](/images/guides/reseed/reseed_03.png)

### 步骤 1:更新系统并安装依赖项

**关键**：安全备份位于 `/home/i2p/.reseed/` 中生成的密钥：

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
将此备份存储在访问受限的安全加密位置。这些密钥对于您的 reseed 服务器的运行至关重要,应该妥善保护。

## Configuring the Service

### 步骤 2: 克隆并构建 Reseed 工具

创建一个 systemd 服务以自动运行 reseed 服务器:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**请记得替换** `admin@stormycloud.org` 为您自己的电子邮件地址。

现在启用并启动服务:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
检查服务是否正在运行:

```bash
sudo systemctl status reseed
```
![验证 reseed 服务状态](/images/guides/reseed/reseed_04.png)

### 步骤 3: 生成 SSL 证书

为了获得最佳性能,您可能需要定期重启 reseed 服务以刷新 router 信息:

```bash
sudo crontab -e
```
添加此行以每3小时重启一次服务:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

reseed 服务器运行在 localhost:8443 上,需要一个反向代理来处理公共 HTTPS 流量。我们推荐使用 Nginx Proxy Manager,因为它易于使用。

### 步骤 4：备份你的密钥

使用 Docker 部署 Nginx Proxy Manager:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
这将暴露：- **端口 80**：HTTP 流量 - **端口 81**：管理界面 - **端口 443**：HTTPS 流量

### Configure Proxy Manager

1. 在 `http://your-server-ip:81` 访问管理界面

2. 使用默认凭据登录:
   - **邮箱**: admin@example.com
   - **密码**: changeme

**重要提示**：首次登录后请立即更改这些凭据！

![Nginx Proxy Manager 登录](/images/guides/reseed/reseed_05.png)

3. 导航到 **Proxy Hosts** 并点击 **Add Proxy Host**

![添加代理主机](/images/guides/reseed/reseed_06.png)

4. 配置代理主机：
   - **域名**：您的 reseed 域名（例如，`reseed.example.com`）
   - **协议**：`https`
   - **转发主机名 / IP**：`127.0.0.1`
   - **转发端口**：`8443`
   - 启用 **缓存资源**
   - 启用 **拦截常见攻击**
   - 启用 **Websockets 支持**

![配置代理主机详细信息](/images/guides/reseed/reseed_07.png)

5. 在 **SSL** 标签页中:
   - 选择 **Request a new SSL Certificate** (Let's Encrypt)
   - 启用 **Force SSL**
   - 启用 **HTTP/2 Support**
   - 同意 Let's Encrypt 服务条款

![SSL证书配置](/images/guides/reseed/reseed_08.png)

6. 点击 **保存**

你的 reseed 服务器现在应该可以通过 `https://reseed.example.com` 访问

![成功的 reseed 服务器配置](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

一旦你的 reseed 服务器运行正常,请联系 I2P 开发者将其添加到官方 reseed 服务器列表中。

### 步骤 5：创建 Systemd 服务

请通过电子邮件向 **zzz**(I2P 首席开发者)提供以下信息:

- **I2P 邮箱**: zzz@mail.i2p
- **明网邮箱**: zzz@i2pmail.org

### 步骤 6：可选 - 配置定期重启

在您的邮件中包含:

1. **Reseed 服务器 URL**：完整的 HTTPS URL（例如，`https://reseed.example.com`）
2. **公共 reseed 证书**：位于 `/home/i2p/.reseed/`（附加 `.crt` 文件）
3. **联系邮箱**：用于服务器维护通知的首选联系方式
4. **服务器位置**：可选但有帮助（国家/地区）
5. **预期正常运行时间**：您对维护服务器的承诺

### Verification

I2P 开发者将验证您的 reseed 服务器是否:
- 正确配置并提供 router 信息
- 使用有效的 SSL 证书
- 提供正确签名的 SU3 文件
- 可访问且响应正常

一旦获得批准,您的 reseed 服务器将被添加到随 I2P router 分发的列表中,帮助新用户加入网络!

## Monitoring and Maintenance

### 安装 Nginx Proxy Manager

监控您的 reseed 服务:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### 配置代理管理器

密切关注系统资源：

```bash
htop
df -h
```
### Update Reseed Tools

定期更新 reseed-tools 以获取最新的改进：

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### 联系信息

如果通过 Nginx Proxy Manager 使用 Let's Encrypt,证书将自动续期。验证续期是否正常工作:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## 配置服务

### 必需信息

检查日志中的错误：

```bash
sudo journalctl -u reseed -n 50
```
常见问题：- I2P router 未运行或 netDb 为空 - 端口 8443 已被占用 - `/home/i2p/.reseed/` 目录的权限问题

### 验证

确保你的 I2P router 正在运行并已填充其 netDb：

```bash
ls -lh /home/i2p/.i2p/netDb/
```
你应该看到许多 `.dat` 文件。如果是空的,请等待你的 I2P router 发现对等节点。

### SSL Certificate Errors

验证您的证书是否有效:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### 检查服务状态

检查：- DNS 记录正确指向您的服务器 - 防火墙允许端口 80 和 443 - Nginx Proxy Manager 正在运行：`docker ps`

## Security Considerations

- **保护私钥安全**：切勿分享或暴露 `/home/i2p/.reseed/` 目录的内容
- **定期更新**：保持系统软件包、Docker 和 reseed-tools 为最新版本
- **监控日志**：留意可疑的访问模式
- **速率限制**：考虑实施速率限制以防止滥用
- **防火墙规则**：仅开放必要的端口（80、443、81 用于管理）
- **管理界面**：将 Nginx Proxy Manager 管理界面（端口 81）限制为仅受信任的 IP 访问

## Contributing to the Network

通过运行一个 reseed 服务器,您正在为 I2P 网络提供关键基础设施。感谢您为更加私密和去中心化的互联网做出贡献!

如有问题或需要帮助,请联系 I2P 社区: - **论坛**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: 各网络上的 #i2p - **开发**: [i2pgit.org](https://i2pgit.org)

---


*指南最初由 [Stormy Cloud](https://www.stormycloud.org) 创建,经改编用于 I2P 文档。*
