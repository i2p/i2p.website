---
title: "IRC over I2P"
description: "I2P IRC 网络、客户端、隧道和服务器设置完整指南（2025年更新）"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

**关键要点**

- I2P 通过其隧道为 IRC 流量提供**端到端加密**。在 IRC 客户端中**禁用 SSL/TLS**，除非你正在通过出口代理连接到明网。
- 预配置的 **Irc2P** 客户端隧道默认监听 **127.0.0.1:6668**。将你的 IRC 客户端连接到该地址和端口。
- 不要使用术语"router‑provided TLS"。使用"I2P's native encryption"或"end‑to‑end encryption"。

## 快速入门（Java I2P）

1. 在 `http://127.0.0.1:7657/i2ptunnel/` 打开 **Hidden Services Manager**，确保 **Irc2P** 隧道正在**运行**。
2. 在你的 IRC 客户端中，设置 **server** = `127.0.0.1`，**port** = `6668`，**SSL/TLS** = **off**。
3. 连接并加入频道，如 `#i2p`、`#i2p-dev`、`#i2p-help`。

对于 **i2pd** 用户(C++ router),在 `tunnels.conf` 中创建一个 client tunnel(参见下面的示例)。

## 网络和服务器

### IRC2P (main community network)

- 联邦服务器:`irc.postman.i2p:6667`、`irc.echelon.i2p:6667`、`irc.dg.i2p:6667`。
- **Irc2P** tunnel 位于 `127.0.0.1:6668`,会自动连接到其中一个服务器。
- 典型频道:`#i2p`、`#i2p-chat`、`#i2p-dev`、`#i2p-help`。

### Ilita network

- 服务器：`irc.ilita.i2p:6667`、`irc.r4sas.i2p:6667`、`irc.acetone.i2p:6667`、`rusirc.ilita.i2p:6667`。
- 主要语言：俄语和英语。部分主机提供网页前端。

## Client setup

### Recommended, actively maintained

- **WeeChat（终端）** — 强大的 SOCKS 支持；易于编写脚本。
- **Pidgin（桌面）** — 仍在维护中；在 Windows/Linux 上运行良好。
- **Thunderbird Chat（桌面）** — 在 ESR 128+ 版本中受支持。
- **The Lounge（自托管网页）** — 现代化的网页客户端。

### IRC2P (主社区网络)

- **LimeChat**（免费、开源）。
- **Textual**（在 App Store 付费购买；可获取源代码自行构建）。

### Ilita 网络

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- 协议：**IRC**
- 服务器：**127.0.0.1**
- 端口：**6668**
- 加密：**关闭**
- 用户名/昵称：任意

#### Thunderbird Chat

- 账户类型:**IRC**
- 服务器:**127.0.0.1**
- 端口:**6668**
- SSL/TLS:**关闭**
- 可选:连接时自动加入频道

#### Dispatch (SAM v3)

`config.toml` 默认配置示例:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Irc2P 客户端隧道:**127.0.0.1:6668** → 上游服务器端口 **6667**。
- 隐藏服务管理器:`http://127.0.0.1:7657/i2ptunnel/`。

### 推荐使用，积极维护中

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
为 Ilita 创建独立隧道(示例):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### macOS 选项

- **启用 SAM** 在 Java I2P 中(默认关闭),位置:`/configclients` 或 `clients.config`。
- 默认值:**127.0.0.1:7656/TCP** 和 **127.0.0.1:7655/UDP**。
- 推荐加密:`SIGNATURE_TYPE=7`(Ed25519)和 `i2cp.leaseSetEncType=4,0`(ECIES‑X25519 带 ElGamal 回退)或仅 `4`(仅现代加密)。

### 配置示例

- Java I2P 默认值:**2 条入站 / 2 条出站**。
- i2pd 默认值:**5 条入站 / 5 条出站**。
- 对于 IRC:**每个方向 2–3 条**即足够;建议明确设置以确保不同 router 间的行为一致性。

## 客户端设置

- **不要为内部 I2P IRC 连接启用 SSL/TLS**。I2P 已经提供端到端加密。额外的 TLS 会增加开销,但不会带来匿名性提升。
- 使用**持久密钥**以保持稳定的身份;除非是测试,否则避免在每次重启时重新生成密钥。
- 如果多个应用使用 IRC,建议使用**独立隧道**(非共享)以减少跨服务关联。
- 如果必须允许远程控制(SAM/I2CP),请绑定到 localhost 并通过 SSH 隧道或经过身份验证的反向代理来保护访问。

## Alternative connection method: SOCKS5

一些客户端可以通过 I2P 的 SOCKS5 代理连接：**127.0.0.1:4447**。为获得最佳效果，建议在 6668 端口使用专用的 IRC 客户端隧道；SOCKS 无法清理应用层标识符，如果客户端不是为匿名性设计的，可能会泄露信息。

## Troubleshooting

- **无法连接** — 确保 Irc2P 隧道正在运行且路由器已完全引导。
- **卡在解析/加入** — 再次检查 SSL 已**禁用**且客户端指向 **127.0.0.1:6668**。
- **高延迟** — I2P 在设计上就是高延迟的。保持适度的隧道数量(2-3 个)并避免快速重连循环。
- **使用 SAM 应用** — 确认 SAM 已启用(Java)或未被防火墙阻止(i2pd)。建议使用长期会话。

## Appendix: Ports and naming

- 常见 IRC 隧道端口：**6668**（Irc2P 默认端口）、**6667** 和 **6669** 作为备用端口。
- `.b32.i2p` 主机名：52 字符标准形式；LS2/高级证书存在扩展的 56+ 字符形式。除非明确需要 b32 地址，否则请使用 `.i2p` 主机名。
