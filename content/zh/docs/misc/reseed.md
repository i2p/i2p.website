---
title: "Reseed 服务器"
description: "运行 reseed（引导种子）服务与替代性引导方法"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 关于 Reseed（引导）主机

新的 router 需要少量对等节点才能加入 I2P 网络。Reseed hosts（用于初始引导的主机）通过加密的 HTTPS 下载提供该初始引导集合。每个 reseed 包都由主机签名，防止未认证方篡改。已加入网络的 router 若其对等节点集变得陈旧，可能会偶尔进行 reseed。

### 网络引导流程

当 I2P router 首次启动或长时间离线后，需要 RouterInfo（路由信息）数据来连接到网络。由于该 router 尚无现有对等节点，它无法从 I2P 网络内部获取该信息。reseed（获取初始节点的引导）机制通过从受信任的外部 HTTPS 服务器提供 RouterInfo 文件，来解决这一引导问题。

reseed（初始种子获取）过程会以单个经加密签名的捆绑包形式提供 75–100 个 RouterInfo 文件。这可确保新的 routers 能够快速建立连接，同时不暴露于可能将其隔离到彼此独立且不受信任的网络分区中的中间人攻击。

### 当前网络状态

截至 2025 年 10 月，I2P 网络运行的 router 版本为 2.10.0（API 版本 0.9.67）。在 0.9.14 版本引入的 reseed（用于为新节点提供网络引导信息的机制）协议，其核心功能保持稳定，未发生变化。该网络维护着多台相互独立的 reseed 服务器，全球分布，以确保可用性与抗审查能力。

服务 [checki2p](https://checki2p.com/reseed) 每 4 小时监控所有 I2P reseed（节点引导）服务器，为 reseed 基础设施提供实时状态检查和可用性指标。

## SU3 文件格式规范

SU3 文件格式是 I2P 的 reseed（初始节点引入）协议的基础，提供带有密码学签名的内容分发。理解该格式对于实现 reseed 服务器和客户端至关重要。

### 文件结构

SU3 格式由三个主要组件组成：头部（40+ 字节）、内容（可变长度）和签名（长度由头部指定）。

#### 头部格式（至少包含字节 0–39）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Reseed（获取初始 netDb 的过程）专用的 SU3 参数

对于 reseed（引导）捆绑包，SU3 文件必须具有以下特性：

- **文件名**：必须完全为 `i2pseeds.su3`
- **内容类型**（第 27 字节）：0x03（RESEED）
- **文件类型**（第 25 字节）：0x00（ZIP）
- **签名类型**（第 8-9 字节）：0x0006（RSA-4096-SHA512）
- **版本字符串**：ASCII 编码的 Unix 时间戳（自 Unix 纪元起的秒数，date +%s 格式）
- **签名者 ID**：与 X.509 证书 CN 匹配的电子邮件风格标识符（CN 即 Common Name，通用名称）

#### 网络ID查询参数

自 0.9.42 版本起，routers 会在 reseed（初始引导）请求后附加 `?netid=2`。这可防止跨网络连接，因为测试网络使用不同的网络 ID。当前 I2P 生产网络使用网络 ID 2。

示例请求：`https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP 内容结构

内容部分（在头部之后、签名之前）包含一个标准的 ZIP 存档，并需满足以下要求：

- **压缩**: 标准 ZIP 压缩（DEFLATE）
- **文件数量**: 通常为 75-100 个 RouterInfo（路由器信息数据结构）文件
- **目录结构**: 所有文件必须位于顶层目录（无子目录）
- **文件命名**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64 字母表**: 必须使用 I2P 的修改版 base64 字母表

I2P 的 base64 字符集不同于标准 base64，它使用 `-` 和 `~` 代替 `+` 和 `/`，以确保与文件系统和 URL 兼容。

### 数字签名

签名覆盖整个文件，从字节0一直到内容部分的末尾。签名本身追加在内容之后。

#### 签名算法 (RSA-4096-SHA512)

1. 计算从字节 0 到内容末尾的 SHA-512 哈希值
2. 使用 "raw" RSA（指不带哈希/填充的裸 RSA，Java 术语为 NONEwithRSA）对该哈希进行签名
3. 如有必要，在签名前填充前导零，使其长度达到 512 字节
4. 将 512 字节的签名追加到文件末尾

#### 签名验证过程

客户端必须：

1. 读取字节0-11以确定签名类型和长度
2. 读取整个头部以定位内容边界
3. 在流式处理内容的同时计算SHA-512哈希
4. 从文件末尾提取签名
5. 使用签名者的RSA-4096公钥验证签名
6. 如果签名验证失败，则拒绝该文件

### 证书信任模型

Reseed（用于引导初始化 netDb 的过程）签名密钥以使用 RSA-4096 密钥的自签名 X.509 证书形式分发。这些证书包含在 I2P router 软件包的 `certificates/reseed/` 目录中。

证书格式： - **密钥类型**：RSA-4096 - **签名**：自签名 - **主题 CN**：必须与 SU3 头中的签名者 ID 匹配 - **有效期**：客户端应强制执行证书的有效期

## 运行 Reseed（补种）服务器

运营 reseed（引导种子）服务需要对安全性、可靠性以及网络多样性方面的要求给予细致关注。更多彼此独立的 reseed 服务器会提升韧性，并使攻击者或审查者更难阻止新的 router 加入。

### 技术要求

#### 服务器规格

- **操作系统**: Unix/Linux (Ubuntu, Debian, FreeBSD 已测试并推荐)
- **网络连接**: 需要静态 IPv4 地址，IPv6 建议但可选
- **CPU**: 至少 2 核心
- **RAM**: 至少 2 GB
- **带宽**: 每月约 15 GB
- **在线时间**: 需要 24/7 持续运行
- **I2P Router**: 持续运行且良好集成的 I2P router

#### 软件需求

- **Java**: JDK 8 或更高版本（从 I2P 2.11.0 开始将需要 Java 17+）
- **Web 服务器**: 具有反向代理支持的 nginx 或 Apache（由于 X-Forwarded-For 头部限制，Lighttpd 不再受支持）
- **TLS/SSL**: 有效的 TLS 证书（Let's Encrypt、自签名或商业 CA）
- **DDoS 防护**: fail2ban 或等效工具（强制要求，不可选）
- **Reseed 工具（引导获取网络节点）**: 来自 https://i2pgit.org/idk/reseed-tools 的官方 reseed-tools

### 安全需求

#### HTTPS/TLS 配置

- **Protocol**: 仅限 HTTPS，不支持回退到 HTTP
- **TLS Version**: 最低要求 TLS 1.2
- **Cipher Suites**: 必须支持与 Java 8+ 兼容的强密码套件
- **Certificate CN/SAN**: 必须与所提供的 URL 的主机名匹配
- **Certificate Type**: 如已与开发团队沟通，可使用自签名证书；或使用受认可的 CA（证书颁发机构）签发的证书

#### 证书管理

SU3 签名证书与 TLS 证书的用途不同：

- **TLS 证书** (`certificates/ssl/`): 保障 HTTPS 传输安全
- **SU3 签名证书** (`certificates/reseed/`): 为 reseed（引导）包签名

两份证书都必须提供给 reseed（引导）协调员（zzz@mail.i2p），以便纳入 router 软件包。

#### DDoS 和反爬虫防护

Reseed 服务器（用于初始引导网络的服务器）面临来自有缺陷的实现、僵尸网络以及试图爬取 netDb（网络数据库）的恶意行为者的周期性攻击。防护措施包括：

- **fail2ban**: 用于速率限制与攻击缓解的必需组件
- **捆绑多样性**: 向不同请求方提供不同的 RouterInfo（路由信息）集合
- **捆绑一致性**: 向来自同一 IP 且在可配置时间窗口内的重复请求交付相同的捆绑
- **IP 日志记录限制**: 不得公开日志或 IP 地址（隐私政策要求）

### 实现方法

#### 方法 1：官方 reseed-tools（用于 netDb 重新播种的工具）（推荐）

由 I2P 项目维护的官方实现。代码仓库：https://i2pgit.org/idk/reseed-tools

**安装**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
首次运行时，工具将生成: - `your-email@mail.i2p.crt` (SU3 签名证书) - `your-email@mail.i2p.pem` (SU3 签名私钥) - `your-email@mail.i2p.crl` (证书吊销列表) - TLS 证书和密钥文件

**功能**: - 自动生成 SU3 包 (350 种变体，每个包含 77 个 RouterInfos) - 内置 HTTPS 服务器 - 通过 cron 每 9 小时重建缓存 - 通过 `--trustProxy` 标志支持 X-Forwarded-For 请求头 - 兼容反向代理配置

**生产部署**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### 方法 2：Python 实现（pyseeder）

由 PurpleI2P 项目提供的替代实现: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### 方法三：Docker 部署

对于容器化环境，已有多种可直接用于 Docker 的实现：

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: 添加对 Tor onion service（洋葱服务）和 IPFS 的支持

### 反向代理配置

#### nginx 配置

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Apache 配置

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### 注册与协调

要将你的 reseed 服务器纳入官方 I2P 软件包：

1. 完成部署和测试
2. 将两份证书（SU3 签名和 TLS）发送给 reseed 协调员（reseed：网络引导种子分发）
3. 联系：zzz@mail.i2p 或 zzz@i2pmail.org
4. 在 IRC2P 上加入 #i2p-dev，与其他运营者协调

### 运维最佳实践

#### 监控与日志记录

- 启用 Apache/nginx 的 combined 日志格式用于统计
- 启用日志轮转（日志增长很快）
- 监控 bundle（打包产物）的生成成功率和重建耗时
- 跟踪带宽使用情况和请求模式
- 切勿公开 IP 地址或详细访问日志

#### 维护计划

- **每 9 小时**：重建 SU3（I2P 更新包格式）包缓存（通过 cron 自动化）
- **每周**：审查日志中的攻击模式
- **每月**：更新 I2P router 和 reseed-tools（用于初始化 netDb 的工具）
- **按需**：续订 TLS 证书（使用 Let's Encrypt 实现自动化）

#### 端口选择

- 默认：8443 (推荐)
- 可选：1024-49151 之间的任意端口
- 端口 443：需要 root 权限或端口转发 (建议使用 iptables 重定向)

端口转发示例：

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## 替代的重新播种方法

其他 bootstrap（引导初始化）选项可帮助处于受限网络环境中的用户：

### 基于文件的Reseed（引导）

在 0.9.16 版本中引入的基于文件的 reseed（引导种子）允许用户手动加载 RouterInfo（I2P router 的信息记录）包。这种方法对处于因审查而封锁了 HTTPS reseed 服务器的地区的用户尤其有用。

**流程**: 1. 受信任的联系人使用其 router 生成一个 SU3 包 2. 通过电子邮件、USB 驱动器或其他带外渠道传输该包 3. 用户将 `i2pseeds.su3` 放入 I2P 配置目录中 4. Router 在重启时会自动检测并处理该包

**文档**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**使用场景**: - 处在封锁了 reseed 服务器的国家级防火墙之后的用户 - 需要手动引导的隔离网络 - 测试与开发环境

### 使用 Cloudflare 代理的重新播种

通过 Cloudflare 的 CDN（内容分发网络）路由 reseed（引导）流量，可为处于审查严格地区的运营者带来多重优势。

**优势**: - 源站 IP 地址对客户端隐藏 - 通过 Cloudflare 的基础设施实现 DDoS 防护 - 通过边缘缓存实现地理负载分发 - 为全球用户提升性能

**实施要求**: - 在 reseed-tools 中启用 `--trustProxy` 标志 - 为 DNS 记录启用 Cloudflare 代理 - 正确处理 X-Forwarded-For 请求头

**重要注意事项**: - 适用 Cloudflare 端口限制（必须使用受支持的端口） - 维持 Same-client bundle（同一客户端分组/捆绑）一致性需要 X-Forwarded-For 支持 - SSL/TLS 配置由 Cloudflare 管理

**文档**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### 抗审查策略

Nguyen Phong Hoang（USENIX FOCI 2019）的研究识别出用于受审查网络的额外引导方法：

#### 云存储服务提供商

- **Box, Dropbox, Google Drive, OneDrive**: 通过公开链接托管 SU3 文件
- **优点**: 在不干扰合法服务的情况下难以被封锁
- **局限**: 需要手动向用户分发 URL

#### IPFS 分发

- 在 InterPlanetary File System（星际文件系统，IPFS）上托管 reseed 包（用于初始引导的种子包）
- 内容寻址存储可防止篡改
- 对下架尝试具有抗性

#### Tor 洋葱服务

- Reseed 服务器（用于获取初始节点信息的服务器）可通过 .onion 地址访问
- 能抵抗基于 IP 的封锁
- 需要在用户系统上运行 Tor 客户端

**研究文档**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### 已知对 I2P 实施封锁的国家

截至2025年，以下国家已确认封锁 I2P reseed 服务器（用于初始引导的种子服务器）： - 中国 - 伊朗 - 阿曼 - 卡塔尔 - 科威特

这些地区的用户应采用替代的引导方法或抗审查的 reseeding（重新获取初始节点信息）策略。

## 供实现者参考的协议细节

### Reseed（补种）请求规范

#### 客户端行为

1. **服务器选择**: router 维护一份硬编码的 reseed（引导）URL 列表
2. **随机选择**: 客户端从可用列表中随机选择服务器
3. **请求格式**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: 应该模拟常见浏览器（例如，"Wget/1.11.4"）
5. **重试逻辑**: 如果 SU3 请求失败，回退到索引页解析
6. **证书验证**: 将 TLS 证书与系统信任存储进行校验
7. **SU3 签名验证**: 将签名与已知的 reseed 证书进行校验

#### 服务器行为

1. **捆绑包选择**: 从 netDb 中选择 RouterInfos（router 信息集合）的伪随机子集
2. **客户端跟踪**: 根据源 IP 识别请求（遵循 X-Forwarded-For）
3. **捆绑包一致性**: 在时间窗口内（通常 8-12 小时）对重复请求返回相同的捆绑包
4. **捆绑包多样性**: 为了网络多样性，向不同客户端返回不同的捆绑包
5. **Content-Type**: `application/octet-stream` 或 `application/x-i2p-reseed`

### RouterInfo 文件格式

reseed 捆绑包中的每个 `.dat` 文件都包含一个 RouterInfo 结构（Router 信息结构）：

**文件命名**: `routerInfo-{base64-hash}.dat` - 哈希长度为 44 个字符，使用 I2P base64 字母表 - 示例: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**文件内容**: - RouterIdentity (router 身份标识) (router 哈希、加密密钥、签名密钥) - 发布时间戳 - router 地址（IP、端口、传输类型） - router 能力与选项 - 覆盖上述所有数据的签名

### 网络多样性要求

为防止网络中心化并启用女巫攻击检测：

- **不得提供完整的 NetDb（网络数据库）导出**: 切勿向单个客户端提供全部 RouterInfos（路由器信息记录）
- **随机抽样**: 每个包包含可用节点的不同子集
- **最小包大小**: 75 个 RouterInfos（由原来的 50 提高）
- **最大包大小**: 100 个 RouterInfos
- **时效性**: RouterInfos 应为近期（自生成起 24 小时内）

### IPv6 注意事项

**当前状态** (2025): - 一些 reseed 服务器（用于初始引导的服务器）在 IPv6 上无响应 - 出于可靠性考虑，客户端应优先或强制使用 IPv4 - 建议在新部署中启用 IPv6 支持，但并非关键

**实现说明**: 配置双栈服务器时，确保 IPv4 和 IPv6 的监听地址均能正常工作，或在无法正确支持 IPv6 时将其禁用。

## 安全性考虑

### 威胁模型

reseed（用于引导获取初始 netDb 数据）协议可防御：

1. **中间人攻击**: RSA-4096 签名可防止包被篡改
2. **网络分区**: 多个相互独立的 reseed 服务器可避免单点控制
3. **Sybil 攻击**: 包的多样性限制了攻击者隔离用户的能力
4. **审查**: 多台服务器和替代方法提供冗余

reseed 协议（用于引导加入网络的补种协议）并不能防御以下情况：

1. **reseed（初始引导）服务器被攻陷**: 如果攻击者掌握了reseed证书私钥
2. **网络完全封锁**: 如果某地区的所有reseed方法都被封锁
3. **长期监控**: reseed请求会暴露尝试加入I2P的IP地址

### 证书管理

**私钥安全**: - 在不使用时将 SU3 签名密钥离线存储 - 为密钥加密使用强密码 - 维护密钥和证书的安全备份 - 考虑在高价值部署中使用硬件安全模块（HSM）

**证书吊销**: - 证书吊销列表（CRLs）通过新闻提要分发 - 遭到泄露的证书可由协调者吊销 - Routers 随软件更新自动更新 CRLs

### 攻击缓解

**DDoS 防护**: - 针对过多请求的 fail2ban 规则 - 在 Web 服务器层面进行限流 - 按 IP 地址设置连接数上限 - 使用 Cloudflare 或类似的 CDN 作为额外一层防护

**防爬取措施**: - 对每个请求 IP 提供不同的包 - 按 IP 进行基于时间的包缓存 - 记录可表明抓取尝试的日志模式 - 就已检测到的攻击与其他运营者协同

## 测试与验证

### 测试你的 Reseed（引导）服务器

#### 方法 1: 全新安装 Router

1. 在全新系统上安装 I2P
2. 将你的 reseed（引导）URL 添加到配置中
3. 移除或禁用其他 reseed URL
4. 启动 router 并监控日志以确认 reseed 成功
5. 在 5-10 分钟内验证与网络的连接

预期的日志输出：

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### 方法 2：手动 SU3 验证

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### 方法 3：checki2p 监控

位于 https://checki2p.com/reseed 的服务会每 4 小时对所有已注册的 I2P reseed 服务器（引导服务器）进行自动化检查。其提供：

- 可用性监控
- 响应时间指标
- TLS 证书验证
- SU3（I2P 更新包格式）签名验证
- 历史正常运行时间数据

一旦您的 reseed（用于引导 I2P 网络的种子服务器）在 I2P 项目中注册，它将在 24 小时内自动出现在 checki2p 上。

### 常见问题的故障排除

**Issue**: "无法读取签名密钥" 在首次运行时 - **Solution**: 这是正常的。输入 'y' 以生成新密钥。

**问题**: Router 无法验证签名 - **原因**: 证书不在 router 的信任库中 - **解决方案**: 将证书放入 `~/.i2p/certificates/reseed/` 目录

**问题**：同一 bundle 被交付给不同客户端 - **原因**：X-Forwarded-For 请求头未被正确转发 - **解决方案**：启用 `--trustProxy` 并配置反向代理请求头

**问题**: "连接被拒绝" 错误 - **原因**: 端口无法从互联网访问 - **解决方案**: 检查防火墙规则，验证端口转发

**问题**: 在捆绑包重建期间 CPU 使用率高 - **原因**: 在生成 350+ 个 SU3（I2P 更新包格式）变体时的正常行为 - **解决方案**: 确保有足够的 CPU 资源，考虑降低重建频率

## 参考信息

### 官方文档

- **Reseed（初始节点引导）贡献者指南**: /guides/creating-and-running-an-i2p-reseed-server/
- **Reseed 策略要求**: /guides/reseed-policy/
- **SU3 规范**: /docs/specs/updates/
- **Reseed 工具仓库**: https://i2pgit.org/idk/reseed-tools
- **Reseed 工具文档**: https://eyedeekay.github.io/reseed-tools/

### 替代实现

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder（重新播种服务器）**: https://github.com/torbjo/i2p-reseeder

### 社区资源

- **I2P 论坛**: https://i2pforum.net/
- **Gitea 仓库**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: IRC2P 上的 #i2p-dev
- **状态监控**: https://checki2p.com/reseed

### 版本历史

- **0.9.14** (2014): 引入 SU3 reseed（重新引导）格式
- **0.9.16** (2014): 新增基于文件的 reseeding
- **0.9.42** (2019): 网络 ID 查询参数为必需项
- **2.0.0** (2022): 引入 SSU2 传输协议
- **2.4.0** (2024): NetDB 隔离与安全性改进
- **2.6.0** (2024): 已阻止 I2P-over-Tor 连接
- **2.10.0** (2025): 当前稳定版（截至 2025 年 9 月）

### 签名类型参考

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Reseed 标准（网络引导/重新播种）**: reseed 包必须使用 Type 6 (RSA-SHA512-4096).

## 致谢

感谢每一位 reseed 服务器运营者（提供初始路由信息的引导服务），你们让网络保持可访问且具备弹性。特别致谢以下贡献者和项目：

- **zzz**: 资深 I2P 开发者和 reseed（I2P 网络的初始引导/获取种子节点的机制）协调员
- **idk**: reseed-tools 的现任维护者兼发布经理
- **Nguyen Phong Hoang**: 研究抗审查的 reseeding 策略
- **PurpleI2P Team**: 替代性 I2P 实现与工具
- **checki2p**: 面向 reseed 基础设施的自动化监控服务

I2P 网络的去中心化 reseed（引导服务）基础设施体现了全球数十位运营者的协作努力，确保无论面临何种本地审查或技术障碍，新用户都能始终找到加入网络的途径。
