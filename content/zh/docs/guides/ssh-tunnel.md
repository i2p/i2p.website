---
title: "创建 SSH 隧道以远程访问 I2P"
description: "学习如何在 Windows、Linux 和 Mac 上创建安全的 SSH tunnel 以访问您的远程 I2P router"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SSH 隧道提供了一个安全、加密的连接,用于访问您的远程 I2P router 控制台或其他服务。本指南向您展示如何在 Windows、Linux 和 Mac 系统上创建 SSH 隧道。

## 什么是 SSH 隧道?

SSH tunnel 是一种通过加密的 SSH 连接安全路由数据和信息的方法。可以将其想象为在互联网中创建一条受保护的"管道"——你的数据通过这条加密的 tunnel 传输,防止任何人在传输过程中拦截或读取数据。

SSH 隧道特别适用于:

- **访问远程 I2P router**: 连接到运行在远程服务器上的 I2P 控制台
- **安全连接**: 所有流量均经过端到端加密
- **绕过限制**: 访问远程系统上的服务,就像它们在本地一样
- **端口转发**: 将本地端口映射到远程服务

在 I2P 环境中,你可以使用 SSH tunnel 将远程服务器上的 I2P router console(通常在 7657 端口)转发到本地计算机的端口来访问它。

## 前置要求

在创建 SSH tunnel 之前,你需要:

- **SSH 客户端**:
  - Windows: [PuTTY](https://www.putty.org/) (免费下载)
  - Linux/Mac: 内置 SSH 客户端(通过终端)
- **远程服务器访问**:
  - 远程服务器的用户名
  - 远程服务器的 IP 地址或主机名
  - SSH 密码或基于密钥的身份验证
- **可用的本地端口**: 选择 1-65535 之间的未使用端口(7657 是 I2P 常用端口)

## 理解隧道命令

SSH 隧道命令遵循以下模式:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**参数说明**: - **local_port**: 本地机器上的端口(例如,7657) - **destination_ip**: 通常是 `127.0.0.1`(远程服务器上的 localhost) - **destination_port**: 远程服务器上服务的端口(例如,I2P 的 7657) - **username**: 远程服务器上的用户名 - **remote_server**: 远程服务器的 IP 地址或主机名

**示例**：`ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

这将创建一个隧道，其中：- 您本地机器上的端口 7657 转发到... - 远程服务器 localhost 上的端口 7657（I2P 运行所在位置）- 以用户 `i2p` 身份连接到服务器 `20.228.143.58`

## 在 Windows 上创建 SSH 隧道

Windows 用户可以使用 PuTTY(一个免费的 SSH 客户端)创建 SSH tunnel。

### Step 1: Download and Install PuTTY

从 [putty.org](https://www.putty.org/) 下载 PuTTY 并将其安装到您的 Windows 系统上。

### Step 2: Configure the SSH Connection

打开 PuTTY 并配置您的连接：

1. 在 **Session** 类别中：
   - 在 **Host Name** 字段中输入您远程服务器的 IP 地址或主机名
   - 确保 **Port** 设置为 22（默认 SSH 端口）
   - 连接类型应为 **SSH**

![PuTTY 会话配置](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

在左侧边栏中导航至 **Connection → SSH → Tunnels**:

1. **源端口**:输入您要使用的本地端口(例如 `7657`)
2. **目标地址**:输入 `127.0.0.1:7657`(远程服务器上的 localhost:端口)
3. 点击 **添加** 以添加 tunnel
4. tunnel 应该会出现在"转发端口"列表中

![PuTTY 隧道配置](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. 点击 **Open** 启动连接
2. 如果这是您第一次连接，将看到安全警告 - 点击 **Yes** 信任该服务器
3. 出现提示时输入您的用户名
4. 出现提示时输入您的密码

![PuTTY 连接已建立](/images/guides/ssh-tunnel/sshtunnel_3.webp)

连接成功后,您可以通过打开浏览器并访问 `http://127.0.0.1:7657` 来访问远程 I2P 控制台

### 步骤 1:下载并安装 PuTTY

为了避免每次都重新配置:

1. 返回到 **Session** 类别
2. 在 **Saved Sessions** 中输入一个名称（例如，"I2P Tunnel"）
3. 点击 **Save**
4. 下次只需加载此会话并点击 **Open**

## Creating SSH Tunnels on Linux

Linux 系统在终端中内置了 SSH,使得隧道创建快速而简单。

### 步骤 2:配置 SSH 连接

打开终端并运行 SSH tunnel 命令：

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**替换**：- `7657`（第一次出现）：您期望的本地端口 - `127.0.0.1:7657`：远程服务器上的目标地址和端口 - `i2p`：您在远程服务器上的用户名 - `20.228.143.58`：您的远程服务器 IP 地址

![Linux SSH tunnel 创建](/images/guides/ssh-tunnel/sshtunnel_4.webp)

当提示时,输入您的密码。连接后,tunnel 即处于活动状态。

在浏览器中访问您的远程 I2P 控制台，地址为 `http://127.0.0.1:7657`。

### 步骤 3:配置隧道

只要 SSH 会话保持运行,隧道就会保持活动状态。要让它在后台持续运行:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**附加参数**：- `-f`：在后台运行 SSH - `-N`：不执行远程命令(仅建立隧道)

要关闭后台隧道,找到并终止 SSH 进程:

```bash
ps aux | grep ssh
kill [process_id]
```
### 步骤 4：连接

为了更好的安全性和便利性,使用 SSH 密钥认证:

1. 生成 SSH 密钥对（如果你还没有）：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 将你的公钥复制到远程服务器：
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. 现在你可以无需密码连接：
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Mac 系统使用与 Linux 相同的 SSH 客户端,因此操作过程完全相同。

### 可选：保存您的会话

打开终端(应用程序 → 实用工具 → 终端)并运行:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**替换**：- `7657`（第一次出现）：你期望的本地端口 - `127.0.0.1:7657`：远程服务器上的目标地址和端口 - `i2p`：你在远程服务器上的用户名 - `20.228.143.58`：你的远程服务器的 IP 地址

![Mac SSH tunnel creation](/images/guides/ssh-tunnel/sshtunnel_5.webp)

出现提示时输入您的密码。连接后,在 `http://127.0.0.1:7657` 访问您的远程 I2P 控制台

### Background Tunnels on Mac

与 Linux 相同,你可以在后台运行隧道:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### 使用终端

Mac SSH 密钥设置与 Linux 相同:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### 保持隧道活跃

最常见的用例 - 访问您的远程 I2P router 控制台:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
然后在浏览器中打开 `http://127.0.0.1:7657`。

### 使用 SSH 密钥(推荐)

一次转发多个端口:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
这会同时转发端口 7657(I2P 控制台)和 7658(另一个服务)。

### Custom Local Port

如果 7657 端口已被占用,请使用不同的本地端口:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
请访问 I2P 控制台：`http://127.0.0.1:8080`。

## Troubleshooting

### 使用终端

**错误**："bind: Address already in use"

**解决方案**:选择不同的本地端口或终止占用该端口的进程:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Mac 上的后台隧道

**错误**："Connection refused" 或 "channel 2: open failed"

**可能原因**: - 远程服务未运行(检查远程服务器上的 I2P router 是否正在运行) - 防火墙阻止了连接 - 目标端口不正确

**解决方案**：验证远程服务器上的 I2P router 是否正在运行：

```bash
ssh user@remote-server "systemctl status i2p"
```
### 在 Mac 上设置 SSH 密钥

**错误**："Permission denied" 或 "Authentication failed"

**可能的原因**：- 用户名或密码不正确 - SSH 密钥配置不当 - 远程服务器上禁用了 SSH 访问

**解决方案**：验证凭据并确保远程服务器上已启用 SSH 访问。

### Tunnel Drops Connection

**错误**：闲置一段时间后连接断开

**解决方案**:在你的 SSH 配置文件(`~/.ssh/config`)中添加 keep-alive 设置:

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **使用 SSH 密钥**:比密码更安全,更难被攻破
- **禁用密码认证**:设置好 SSH 密钥后,在服务器上禁用密码登录
- **使用强密码**:如果使用密码认证,请使用强密码且不要重复使用
- **限制 SSH 访问**:配置防火墙规则,将 SSH 访问限制在可信 IP 范围内
- **保持 SSH 更新**:定期更新您的 SSH 客户端和服务器软件
- **监控日志**:检查服务器上的 SSH 日志,留意可疑活动
- **使用非标准 SSH 端口**:更改默认 SSH 端口(22)以减少自动化攻击

## 在 Linux 上创建 SSH 隧道

### 访问 I2P 控制台

创建一个脚本来自动建立 tunnel：

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
使其可执行:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### 多条隧道

创建一个 systemd 服务以实现自动创建 tunnel:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
添加:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
启用并启动:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### 自定义本地端口

创建用于动态转发的 SOCKS 代理:

```bash
ssh -D 8080 user@remote-server
```
将浏览器配置为使用 `127.0.0.1:8080` 作为 SOCKS5 代理。

### Reverse Tunneling

允许远程服务器访问本地机器上的服务:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### 端口已被占用

通过中间服务器建立隧道:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH 隧道是一个强大的工具,用于安全访问远程 I2P router 和其他服务。无论您使用 Windows、Linux 还是 Mac,这个过程都很简单,并为您的连接提供强加密。

如需更多帮助或有疑问,请访问 I2P 社区: - **论坛**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p 在各个网络上 - **文档**: [I2P Docs](/docs/)

---

I2P 路由器控制台

*本指南最初由 [Stormy Cloud](https://www.stormycloud.org) 创建,已改编用于 I2P 文档。*
