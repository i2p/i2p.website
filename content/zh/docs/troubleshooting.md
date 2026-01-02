---
title: "I2P Router 故障排除指南"
description: "面向常见 I2P router 问题（包括连接性、性能和配置方面）的全面故障排除指南"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P router 最常见的故障原因是 **端口转发问题**、**带宽分配不足** 和 **引导时间不足**。这三项占已报告问题的 70% 以上。该 router 启动后至少需要 **10-15 分钟** 才能完全融入网络、至少 **128 KB/秒 的最低带宽**（建议 256 KB/秒），以及正确的 **UDP/TCP 端口转发**，才能达到非防火墙状态（未被防火墙阻挡）。新用户常常期望立即连通并过早重启，这会重置接入进度，形成令人沮丧的循环。本指南为 2.10.0 及更高版本中所有主要 I2P 问题提供了详细的解决方案。

I2P 的匿名架构通过多跳加密的 tunnel，从根本上以牺牲速度换取隐私。理解这一基本设计有助于用户设定合理预期并更有效地进行故障排查，而不是把正常行为误判为问题。

## Router 无法启动或立即崩溃

最常见的启动失败通常由**端口冲突**、**Java 版本不兼容**或**配置文件损坏**引起。在深入排查之前，先检查是否已有其他 I2P 实例正在运行。

**确认没有冲突的进程：**

Linux: `ps aux | grep i2p` 或 `netstat -tulpn | grep 7657`

Windows: 任务管理器 → 详细信息 → 查找命令行中包含 i2p 的 java.exe

macOS：活动监视器 → 搜索“i2p”

如果存在僵尸进程，杀死它：`pkill -9 -f i2p` (Linux/Mac) 或 `taskkill /F /IM javaw.exe` (Windows)

**检查 Java 版本兼容性：**

I2P 2.10.0+ 需要 **至少 Java 8**，推荐使用 Java 11 或更高版本。请确认您的安装显示为 "mixed mode"（而不是 "interpreted mode"）：

```bash
java -version
```
应显示：OpenJDK 或 Oracle Java，版本 8+，"mixed mode"

**避免：** GNU GCJ、过时的 Java 实现、仅解释执行模式

**常见端口冲突** 发生在多个服务争用 I2P 的默认端口时。router 控制台 (7657)、I2CP (7654)、SAM (7656) 和 HTTP 代理 (4444) 必须可用。检查是否存在冲突：`netstat -ano | findstr "7657 4444 7654"` (Windows) 或 `lsof -i :7657,4444,7654` (Linux/Mac)。

**配置文件损坏** 会表现为程序立即崩溃，并在日志中出现解析错误。Router.config 要求使用**无 BOM（字节序标记）的 UTF-8 编码**，以 `=` 作为分隔符（而不是 `:`），并禁止某些特殊字符。请先备份，然后检查：`~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS)。

在保留身份的情况下重置配置：停止 I2P，备份 router.keys 和 keyData 目录，删除 router.config，然后重启 I2P。router 会重新生成默认配置。

**Java 堆分配过低** 会导致 OutOfMemoryError（内存不足错误）崩溃。编辑 wrapper.config，将 `wrapper.java.maxmemory` 从默认的 128 或 256 提高到 **至少 512**（高带宽的 routers 建议 1024）。这需要完全关闭，等待 11 分钟，然后重新启动 - 在控制台点击 "Restart" 不会应用该更改。

## 排查并解决 "Network: Firewalled" 状态

防火墙状态意味着该 router 无法接收直接的入站连接，从而不得不依赖引介者。在这种状态下，尽管 router 仍可运行，**性能会显著下降**，且对网络的贡献依然微乎其微。要达到非防火墙状态，需要正确配置端口转发。

**router 会随机选择一个端口**（用于通信），范围在 9000-31000 之间。请在 http://127.0.0.1:7657/confignet 查看你的端口 - 查找 "UDP Port" 和 "TCP Port"（通常是相同的数值）。为获得最佳性能，你必须同时为 UDP 和 TCP 进行端口转发，不过仅转发 UDP 也能提供基本功能。

**启用 UPnP 自动端口转发**（最简单的方法）:

1. 访问 http://127.0.0.1:7657/confignet
2. 勾选 "Enable UPnP"
3. 保存更改并重启 router
4. 等待 5-10 分钟，并验证状态从 "Network: Firewalled" 变为 "Network: OK"

UPnP 需要 router 支持（在大多数 2010 年后制造的消费级 router 上默认启用）以及适当的网络配置。

**手动端口转发**（当 UPnP 失败时需要）：

1. 在 http://127.0.0.1:7657/confignet 中记下你的 I2P 端口（例如 22648）
2. 查找你的本地 IP 地址：`ipconfig`（Windows）、`ip addr`（Linux）、系统偏好设置 → 网络（macOS）
3. 访问你的 router 管理界面（通常为 192.168.1.1 或 192.168.0.1）
4. 找到“端口转发”（可能位于 Advanced、NAT 或 Virtual Servers 下）
5. 创建两条规则：
   - 外部端口：[你的 I2P 端口] → 内部 IP：[你的电脑] → 内部端口：[相同] → 协议：**UDP**
   - 外部端口：[你的 I2P 端口] → 内部 IP：[你的电脑] → 内部端口：[相同] → 协议：**TCP**
6. 保存配置，如果需要，重启你的 router

**验证端口转发**，在完成配置后使用在线检测工具。如果检测失败，请检查防火墙设置 - 系统防火墙和任何杀毒软件的防火墙都必须允许 I2P 端口。

**Hidden mode（隐藏模式）备选方案**，适用于无法进行端口转发的受限网络：在 http://127.0.0.1:7657/confignet 启用 → 勾选 "Hidden mode"。router 仍处于防火墙后，但会仅使用 SSU 引荐者来针对该状态进行优化。性能会更慢，但仍可正常使用。

## Router 卡在 "Starting" 或 "Testing" 状态

这些在初始引导期间出现的短暂状态通常会在**10-15 分钟（针对新安装）**或**3-5 分钟（针对已建立的 routers）**内自行解决。过早干预通常会使问题变得更糟。

**"Network: Testing"** 表示 router 正在通过各种连接类型（直连、introducers（引荐者）、多个协议版本）探测可达性。这在启动后的前 5-10 分钟内是正常现象。router 会测试多种场景以确定最佳配置。

**"Rejecting tunnels: starting up"** 会在引导阶段出现，因为 router 暂时缺少足够的对等节点信息。router 在充分融入网络之前不会参与转发流量。当 netDb 填充到包含 50+ routers 后（通常需 10-20 分钟），这条消息就会消失。

**时钟偏差会导致可达性测试失败。** I2P 要求系统时间与网络时间的差异在 **±60 秒** 内。差异超过 90 秒将导致自动拒绝连接。请同步您的系统时钟：

Linux： `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows：控制面板 → 日期和时间 → Internet 时间 → 立即更新 → 启用自动同步

macOS: 系统偏好设置 → 日期与时间 → 启用 "自动设置日期与时间"

在纠正时钟偏差后，完全重启 I2P，以确保正确集成。

**带宽分配不足**会阻止测试顺利进行。router 需要足够的带宽来构建测试 tunnel。请在 http://127.0.0.1:7657/config 进行配置：

- **最低可行：** 入站 96 KB/sec，出站 64 KB/sec
- **推荐标准：** 入站 256 KB/sec，出站 128 KB/sec  
- **最佳性能：** 入站 512+ KB/sec，出站 256+ KB/sec
- **共享百分比：** 80%（允许 router 向网络贡献带宽）

较低的带宽也许可行，但会将集成时间从几分钟延长到数小时。

**损坏的 netDb**（由于不当关机或磁盘错误）会导致持续的测试循环。缺少有效的对等节点数据时，router 无法完成测试：

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows：删除 `%APPDATA%\I2P\netDb\` 或 `%LOCALAPPDATA%\I2P\netDb\` 中的内容

**防火墙阻止 reseed（重新播种）** 会阻止获取初始对等节点。在引导（bootstrap）期间，I2P 会从 HTTPS reseed 服务器获取 router 信息。企业/ISP 防火墙可能会阻止这些连接。如果在受限网络下运行，请在 http://127.0.0.1:7657/configreseed 配置 reseed 代理。

## 速度缓慢、超时以及 tunnel 构建失败

由于多跳加密、数据包开销以及路由不可预测性，I2P 的设计天然会导致**比明网慢 3-10 倍**。一次 tunnel 构建会穿越多个 routers，每个都会增加延迟。理解这一点可避免将正常行为误判为问题。

**典型性能预期：**

- 浏览 .i2p 站点：起初页面加载需要 10-30 秒，在完成 tunnel 构建后会更快
- 通过 I2PSnark 下载种子：每个种子 10-100 KB/秒，具体取决于做种者数量和网络状况  
- 大型文件下载：需要耐心 - 兆字节级文件可能需要数分钟，千兆字节级文件可能需要数小时
- 第一次连接最慢：构建 tunnel 需要 30-90 秒；随后连接会使用现有的 tunnels

**Tunnel 构建成功率** 表示网络健康状况。请在 http://127.0.0.1:7657/tunnels 查看：

- **高于 60%：** 运行正常、健康
- **40-60%：** 临界，考虑增加带宽或降低负载
- **低于 40%：** 存在问题 - 表明带宽不足、网络问题或对等体选择不佳

**增加带宽分配** 作为首要优化措施。大多数速度慢的问题源于带宽不足。在 http://127.0.0.1:7657/config 逐步提高限值，并在 http://127.0.0.1:7657/graphs 监控图表。

**适用于 DSL/有线宽带 (1-10 Mbps 连接):** - 入站: 400 KB/秒 - 出站: 200 KB/秒 - 共享比例: 80% - 内存: 384 MB (编辑 wrapper.config)

**针对高速（10-100+ Mbps 连接）：** - 入站：1500 KB/sec   - 出站：1000 KB/sec - 共享：80-100% - 内存：512-1024 MB - 考虑：在 http://127.0.0.1:7657/configadvanced 将参与的 tunnels 增加到 2000-5000

**优化 tunnel 配置** 以获得更好的性能。在 http://127.0.0.1:7657/i2ptunnel 访问各个 tunnel 的设置，并编辑每个 tunnel：

- **Tunnel 数量：** 从 2 增加到 3-4（可用路径更多）
- **备份数量：** 设置为 1-2（当 tunnel 故障时可快速故障转移）
- **Tunnel 长度：** 默认 3 跳具有良好平衡；减少到 2 可提升速度但会降低匿名性

**原生加密库（jbigi）** 相比纯 Java 加密可带来 5-10 倍的性能提升。可在 http://127.0.0.1:7657/logs 验证是否已加载 - 查找 "jbigi loaded successfully" 或 "Using native CPUID implementation"。如果没有看到：

Linux：通常会自动检测并从 ~/.i2p/jbigi-*.so 加载 Windows：在 I2P 安装目录中检查 jbigi.dll 若缺失：安装构建工具并从源代码编译，或从官方软件仓库下载预编译二进制文件

**保持 router 持续运行。** 每次重启都会重置网络融入度，需要 30-60 分钟来重建 tunnel 网络和对等节点关系。高在线时长且稳定的 router 会在 tunnel 构建中被优先选择，从而对性能形成正向反馈。

## CPU 和内存占用过高

资源使用过高通常表明**内存分配不足**、**缺少本地加密库**，或**过度参与网络**。配置良好的 router 在活跃使用期间应占用 10-30% 的 CPU，并将内存占用稳定在已分配堆的 80% 以下。

**内存问题的表现为：** - 平顶型内存图（一直处于最大值） - 频繁的垃圾回收（锯齿形模式，伴随陡降） - 日志中出现 OutOfMemoryError - router 在负载下变得无响应 - 由于资源耗尽而自动关闭

**增大 Java 堆内存分配** 在 wrapper.config 中 (需要完全关闭):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**重要：** 编辑 wrapper.config 之后，您**必须完全关闭**（不是重启），等待 11 分钟以便正常终止，然后进行全新启动。Router 控制台中的 "Restart" 按钮不会重新加载 wrapper 配置。

**CPU 优化需要本地加密库。** 纯 Java 的 BigInteger（大整数类）运算比原生实现多消耗 10–20 倍的 CPU。启动期间请在 http://127.0.0.1:7657/logs 检查 jbigi 状态。没有 jbigi 时，在构建 tunnel 和执行加密操作期间，CPU 会飙升至 50-100%。

**降低参与的 tunnel 负载** 如果 router 不堪重负：

1. 访问 http://127.0.0.1:7657/configadvanced
2. 设置 `router.maxParticipatingTunnels=1000` (默认 8000)
3. 在 http://127.0.0.1:7657/config 将共享百分比从 80% 降低到 50%
4. 如果已启用，禁用 floodfill 模式：`router.floodfillParticipant=false`

**限制 I2PSnark（I2P 内置的 BitTorrent 客户端）的带宽和并发种子数量。** BitTorrent 传输会消耗大量资源。在 http://127.0.0.1:7657/i2psnark：

- 将活跃的种子数量限制为最多 3-5 个
- 将 "Up BW Limit" 和 "Down BW Limit" 设置为合理的数值 (每个 50-100 KB/秒)
- 在不需要时停止种子
- 避免同时为数十个种子做种

**监控资源使用情况**，可通过 http://127.0.0.1:7657/graphs 的内置图表完成。内存曲线应留有余量，而非顶部拉平。构建 tunnel（隧道）期间出现 CPU 峰值属正常；若 CPU 长时间保持高负载，则表明存在配置问题。

**对于资源严重受限的系统**（Raspberry Pi、老旧硬件），可以考虑使用 **i2pd**（C++ 实现）作为替代。i2pd 需要 ~130 MB RAM，而 Java I2P 需要 350+ MB；在类似负载下，其 CPU 使用率为 ~7%，而 Java I2P 为 70%。请注意，i2pd 不包含内置应用，需要配合外部工具。

## I2PSnark 种子问题

要理解 I2PSnark 与 I2P router 架构的集成，需要认识到：**种子下载完全取决于 router 的 tunnel 健康状况**。在 router 充分接入网络（与 10 个以上活跃对等节点互联）且 tunnel 正常工作之前，种子不会开始。

**种子下载卡在 0% 通常表示：**

1. **Router 尚未完全加入网络：** 在 I2P 启动后等待 10-15 分钟，再期望出现种子活动
2. **DHT 已禁用：** 在 http://127.0.0.1:7657/i2psnark → Configuration → 勾选 "Enable DHT"（自 0.9.2 版本起默认启用）
3. **无效或失效的跟踪器：** I2P 种子需要 I2P 专用的跟踪器 - 明网跟踪器无法工作
4. **tunnel 配置不足：** 在 I2PSnark Configuration → Tunnels 部分增加 tunnels

**配置 I2PSnark tunnels 以获得更佳性能:**

- 入站 tunnels：3-5（Java I2P 默认 2，i2pd 为 5）
- 出站 tunnels：3-5  
- tunnel 长度：3 跳（为提高速度可降至 2，但匿名性更低）
- tunnel 数量：3（可提供稳定的性能）

**必备的 I2P Torrent 追踪器** 建议包含： - tracker2.postman.i2p（首选，最可靠） - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

移除所有明网（非 .i2p）跟踪器 - 它们没有任何价值，并会导致连接尝试超时。

**"Torrent not registered" 错误** 通常发生在与跟踪器通信失败时。右键单击种子 → "Start" 可强制重新向跟踪器通告。若问题仍然存在，请在已配置 I2P 的浏览器中访问 http://tracker2.postman.i2p 以验证跟踪器是否可达。失效的跟踪器应更换为可用的替代项。

**没有对等节点连接**，即便追踪器成功，也可能表示： - Router 被防火墙阻挡（开启端口转发会改善，但并非必需） - 带宽不足（提高到 256+ KB/sec）   - 资源群（swarm）过小（有些种子只有 1–2 位做种者；需要耐心） - DHT（分布式哈希表）被禁用（启用以进行无追踪器的对等节点发现）

**启用 DHT 和 PEX（Peer Exchange，对等节点交换）** 在 I2PSnark 配置中。DHT（分布式哈希表）可在不依赖跟踪器的情况下发现对等节点。PEX 会从已连接的对等节点中发现更多对等节点，从而加速群体发现。

**已下载文件损坏** 借助 I2PSnark 的内置完整性校验，这种情况很少发生。若检测到：

1. 右键单击种子 → "Check" 将强制对所有分片重新计算哈希
2. 删除损坏的种子数据（保留 .torrent 文件）  
3. 右键单击 → "Start" 以带分片校验重新下载
4. 若损坏仍然存在，请检查磁盘是否有错误：`chkdsk` (Windows), `fsck` (Linux)

**监视目录不起作用** 需要正确配置：

1. I2PSnark 配置 → "监视目录"：设置绝对路径（例如：`/home/user/torrents/watch`）
2. 确保 I2P 进程具有读取权限：`chmod 755 /path/to/watch`
3. 将 .torrent 文件放入监视目录 - I2PSnark 会自动添加它们
4. 配置 "自动启动"：设置是否在添加后立即启动种子

**BT 下载性能优化：**

- 限制并发的活动种子：标准连接最多 3-5 个
- 优先处理重要下载：暂时停止低优先级种子
- 增加 router 的带宽分配：带宽越多 = 种子性能越好
- 请耐心等待：I2P 种子下载本质上比明网 BitTorrent 更慢
- 下载完成后请做种：网络靠互惠才能繁荣

## 通过 I2P 使用 Git 的配置与故障排除

通过 I2P 进行的 Git 操作需要 **SOCKS 代理配置** 或 **专用的 I2P tunnel**，以实现 SSH/HTTP 访问。Git 的设计假定低时延连接，因此在 I2P 的高时延架构上运行会面临挑战。

**将 Git 配置为使用 I2P 的 SOCKS 代理：**

编辑 ~/.ssh/config（如果不存在则创建）：

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
这会将所有指向 .i2p 主机的 SSH 连接通过 I2P 的 SOCKS 代理（端口 4447）进行路由。ServerAlive 设置可在 I2P 延迟期间保持连接。

对于通过 HTTP/HTTPS 进行的 Git 操作，请全局配置 Git：

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
注意：`socks5h` 通过代理进行 DNS 解析 - 这对 .i2p 域名至关重要。

**为 Git SSH 创建专用 I2P tunnel** (比 SOCKS 更可靠):

1. 访问 http://127.0.0.1:7657/i2ptunnel
2. "新建客户端 tunnel" → "Standard"
3. 配置：
   - 名称：Git-SSH  
   - 类型：Client
   - 端口：2222（用于 Git 访问的本地端口）
   - 目标： [your-git-server].i2p:22
   - 自动启动：启用
   - Tunnel 数量：3-4（数量更高更可靠）
4. 保存并启动 tunnel
5. 配置 SSH 使用 tunnel：`ssh -p 2222 git@127.0.0.1`

在 I2P 上的 **SSH 认证错误** 通常源于：

- 未将密钥添加到 ssh-agent：`ssh-add ~/.ssh/id_rsa`
- 密钥文件权限不正确：`chmod 600 ~/.ssh/id_rsa`
- Tunnel 未运行：在 http://127.0.0.1:7657/i2ptunnel 验证状态是否为绿色
- Git 服务器要求特定密钥类型：如果 RSA 失败，请生成 ed25519 密钥

**Git 操作超时** 与 I2P 的延迟特性有关：

- 提高 Git 超时时间：`git config --global http.postBuffer 524288000`（500MB 缓冲区）
- 提高低速限制：`git config --global http.lowSpeedLimit 1000` 和 `git config --global http.lowSpeedTime 600`（等待 10 分钟）
- 初次检出使用浅克隆：`git clone --depth 1 [url]`（仅获取最新提交，更快）
- 在低活跃时段进行克隆：网络拥塞会影响 I2P 性能

**git clone/fetch 操作较慢** 是 I2P 架构固有的。一个 100MB 的仓库在 I2P 上可能需要 30–60 分钟，而在明网（clearnet）上只需几秒。应对策略：

- 使用浅克隆：`--depth 1` 可显著减少初始数据传输量
- 增量获取：与其进行完整克隆，不如仅获取指定分支：`git fetch origin branch:branch`
- 考虑通过 I2P 使用 rsync：对于非常大的仓库，rsync 可能表现更好
- 增加 tunnel 数量：更多的 tunnel 可为持续的大规模传输提供更好的吞吐量

**"Connection refused" 错误** 表明 tunnel 配置错误:

1. 验证 I2P router 正在运行：检查 http://127.0.0.1:7657
2. 确认 tunnel 在 http://127.0.0.1:7657/i2ptunnel 上处于激活状态并显示为绿色
3. 测试 tunnel：`nc -zv 127.0.0.1 2222` (如果 tunnel 工作正常，应能连接)
4. 检查目标是否可达：如果可用，访问目标的 HTTP 接口
5. 在 http://127.0.0.1:7657/logs 查看 tunnel 日志，查找具体错误

**通过 I2P 使用 Git 的最佳实践：**

- 持续运行 I2P router，以确保稳定的 Git 访问
- 使用 SSH 密钥而非密码认证（减少交互式提示）
- 配置持久的 tunnels，而不是临时的 SOCKS 连接
- 考虑自行托管 I2P Git 服务器，以获得更好的控制
- 为协作者记录你的 .i2p Git 端点

## 访问 eepsites 并解析 .i2p 域名

用户无法访问 .i2p 站点最常见的原因是**浏览器代理配置不正确**。I2P 站点仅存在于 I2P 网络内部，必须通过 I2P 的 HTTP 代理进行路由。

**严格按如下配置浏览器代理设置：**

**Firefox (推荐用于 I2P):**

1. 菜单 → 设置 → 网络设置 → 设置按钮
2. 选择 "手动代理配置"
3. HTTP 代理: **127.0.0.1** 端口: **4444**
4. SSL 代理: **127.0.0.1** 端口: **4444**  
5. SOCKS 代理: **127.0.0.1** 端口: **4447** (可选，用于 SOCKS 应用)
6. 勾选 "使用 SOCKS v5 时代理 DNS"
7. 点击 OK 保存

**关键的 Firefox about:config 设置：**

前往 `about:config` 并修改：

- `media.peerconnection.ice.proxy_only` = **true** (防止 WebRTC 泄露 IP)
- `keyword.enabled` = **false** (防止 .i2p 地址被重定向到搜索引擎)
- `network.proxy.socks_remote_dns` = **true** (通过代理进行 DNS 解析)

**Chrome/Chromium 的局限性：**

Chrome 使用系统级代理设置，而非特定于应用程序的设置。在 Windows 上：设置 → 搜索“代理” → “打开计算机的代理设置” → 配置 HTTP: 127.0.0.1:4444 和 HTTPS: 127.0.0.1:4445。

更好的做法：使用 FoxyProxy 或 Proxy SwitchyOmega 扩展，对 .i2p 进行选择性路由。

**"Website Not Found In Address Book" 错误** 表示 router 缺少该 .i2p 域名的加密地址。I2P 使用本地地址簿，而不是集中式 DNS。解决方案：

**方法一：使用跳转服务** (对新站点最简单):

访问 http://stats.i2p 并搜索该站点。点击 addresshelper 链接：`http://example.i2p/?i2paddresshelper=base64destination`。你的浏览器会显示 "Save to addressbook?" - 确认以添加。

**方法 2：更新地址簿订阅：**

1. 访问 http://127.0.0.1:7657/dns (SusiDNS)
2. 点击 "Subscriptions" 选项卡  
3. 确认活动订阅 (默认: http://i2p-projekt.i2p/hosts.txt)
4. 添加推荐的订阅:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. 点击 "Update Now" 以立即强制更新订阅
6. 等待 5-10 分钟以完成处理

**方法 3：使用 base32 地址** (只要站点在线，就始终可用):

每个 .i2p 站点都有一个 Base32 地址：由 52 个随机字符加上后缀 .b32.i2p 组成（例如，`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`）。Base32 地址会绕过地址簿 - router 会直接进行基于密码学的查找。

**常见的浏览器配置错误：**

- 在仅支持 HTTP 的站点上尝试使用 HTTPS：大多数 .i2p 站点仅使用 HTTP - 尝试 `https://example.i2p` 会失败
- 忘记加上 `http://` 前缀：浏览器可能会搜索而不是连接 - 始终使用 `http://example.i2p`
- 启用 WebRTC：可能泄露真实 IP 地址 - 可通过 Firefox 设置或扩展禁用
- DNS 未通过代理：clearnet（明网）DNS 无法解析 .i2p - 必须通过代理发送 DNS 查询
- 代理端口错误：HTTP 用 4444（不是 4445，后者是到 clearnet 的 HTTPS outproxy（外部代理））

**Router 未完全集成** 将导致无法访问任何站点。请确认集成是否到位：

1. 检查 http://127.0.0.1:7657 是否显示 "Network: OK" 或 "Network: Firewalled"（不是 "Network: Testing"）
2. 活动对等节点应显示至少 10 个（50+ 为最佳）  
3. 没有 "Rejecting tunnels: starting up" 消息
4. 在 router 启动后，至少等待完整的 10-15 分钟，再期望能够访问 .i2p

**IRC 和电子邮件客户端配置** 遵循类似的代理模式：

**IRC:** 客户端连接到 127.0.0.1:6668（I2P 的 IRC 代理 tunnel（隧道））。请禁用 IRC 客户端的代理设置 - 到 localhost:6668 的连接已通过 I2P 进行代理。

**电子邮件 (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - 无 SSL/TLS (加密由 I2P tunnel 处理) - 使用在 postman.i2p 注册的账户凭据

所有这些 tunnels 必须在 http://127.0.0.1:7657/i2ptunnel 显示为"running"（绿色）状态。

## 安装失败与软件包问题

基于软件包的安装（Debian、Ubuntu、Arch）偶尔会因**仓库变更**、**GPG 密钥过期**或**依赖冲突**而失败。最近的版本中，官方软件源已从 deb.i2p2.de/deb.i2p2.no（已停止维护）变更为 **deb.i2p.net**。

**将 Debian/Ubuntu 软件源更新为最新：**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**GPG 签名验证失败** 会在软件仓库密钥过期或发生更换时出现：

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**在安装软件包后服务无法启动** 最常见的原因是 Debian/Ubuntu 上的 AppArmor 配置文件问题：

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**权限问题** 在通过软件包安装的 I2P 上：

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Java 兼容性问题：**

I2P 2.10.0 需要**至少 Java 8**。较旧的系统可能仅有 Java 7 或更早版本：

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Wrapper（Java 服务包装器）配置错误** 会阻止服务启动：

Wrapper.config 的位置因安装方式而异： - 用户安装：`~/.i2p/wrapper.config` - 软件包安装：`/etc/i2p/wrapper.config` 或 `/var/lib/i2p/wrapper.config`

常见 wrapper.config 问题：

- 路径不正确：`wrapper.java.command` 必须指向有效的 Java 安装
- 内存不足：`wrapper.java.maxmemory` 设置过低（提高到 512MB 以上）
- pid 文件位置错误：`wrapper.pidfile` 必须是可写位置
- 缺少 wrapper 二进制：某些平台没有预编译的 wrapper（使用 runplain.sh 作为后备）

**更新失败与损坏的更新：**

由于网络中断，Router 控制台的更新偶尔会在下载过程中失败。手动更新步骤：

1. 从 https://geti2p.net/en/download 下载 i2pupdate_X.X.X.zip
2. 验证 SHA256 校验和是否与发布的哈希一致
3. 将其复制到 I2P 安装目录，命名为 `i2pupdate.zip`
4. 重启 router - 会自动检测并解压更新
5. 等待 5-10 分钟完成更新安装
6. 在 http://127.0.0.1:7657 验证新版本

**从非常旧的版本迁移** (pre-0.9.47) 到当前版本可能会因为签名密钥不兼容或功能被移除而失败。需要逐步更新：

- 版本低于 0.9.9：无法验证当前签名 - 需要手动更新
- 运行在 Java 6/7 的版本：在将 I2P 更新到 2.x 之前必须先升级 Java
- 存在大版本跨越：先更新到中间版本（推荐以 0.9.47 作为过渡版本）

**何时使用安装程序，何时使用软件包：**

- **软件包 (apt/yum):** 最适合服务器、自动安全更新、系统集成、systemd 管理
- **安装程序 (.jar):** 最适合用户级安装、Windows、macOS、自定义安装、可获取最新版本

## 配置文件损坏与恢复

I2P 的配置持久化依赖若干关键文件。损坏通常源于**不当关机**、**磁盘错误**或**手动编辑失误**。理解这些文件的用途能实现外科式修复，而无需完全重新安装。

**关键文件及其用途:**

- **router.keys** (516+ 字节): router 的加密身份 - 丢失此文件会创建新的身份
- **router.info** (自动生成): 已发布的 router 信息 - 可安全删除，会重新生成  
- **router.config** (文本): 主配置 - 带宽、网络设置、首选项
- **i2ptunnel.config** (文本): tunnel 定义 - 客户端/服务器 tunnels、密钥、目的地
- **netDb/** (目录): 对等体数据库 - 网络参与者的 router 信息
- **peerProfiles/** (目录): 对等体性能统计 - 影响 tunnel 选择
- **keyData/** (目录): 面向 eepsites 和服务的目的地密钥 - 丢失会导致地址改变
- **addressbook/** (目录): 本地 .i2p 主机名映射

**完整备份流程**（修改前）：

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Router.config 损坏症状：**

- Router 无法启动，日志中有解析错误
- 重启后设置无法保存
- 出现了意外的默认值  
- 查看文件时出现乱码

**修复损坏的 router.config：**

1. 备份现有文件: `cp router.config router.config.broken`
2. 检查文件编码: 必须为 UTF-8 (无 BOM)
3. 验证语法: 键使用 `=` 作为分隔符 (不是 `:`)，键名后不得有尾随空格，`#` 仅用于注释
4. 常见损坏: 值中含有非 ASCII 字符，行结尾问题 (CRLF vs LF)
5. 若无法修复: 删除 router.config - router 会生成默认配置，并保留身份标识

**需要保留的关键 router.config 设置：**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**丢失或无效的 router.keys** 会创建新的 router 身份。这是可接受的，除非：

- 运行 floodfill（I2P 网络中的目录泛洪节点）（会失去 floodfill 身份）
- 托管使用已公开地址的 eepsites（I2P 隐匿站点）（会失去连续性）  
- 在网络中已建立的声誉

没有备份则无法恢复 - 生成新的：删除 router.keys，重启 I2P，会创建新的身份。

**关键区别：** router.keys（身份）vs keyData/*（服务）。丢失 router.keys 会改变 router 身份。丢失 keyData/mysite-keys.dat 会改变你的 eepsite 的 .i2p 地址 - 如果地址已发布，将是灾难性的。

**单独备份 eepsite/服务密钥：**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**NetDb 和 peerProfiles 数据损坏：**

症状：0 个活跃对等节点，无法构建 tunnels，日志中出现 "Database corruption detected"

安全的修复方法（全部将自动进行 reseed（重新引导）/重建）：

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
这些目录仅包含缓存的网络信息 - 删除它们会强制进行全新引导，但不会丢失任何关键数据。

**预防策略：**

1. **始终优雅关闭：** 使用 `i2prouter stop` 或 router 控制台 "Shutdown" 按钮 - 切勿强制终止进程
2. **自动备份：** 使用 cron 作业（定时任务）每周将 ~/.i2p 备份到独立磁盘
3. **磁盘健康监控：** 定期检查 SMART（自监测、分析与报告技术）状态 - 故障磁盘会损坏数据
4. **足够的磁盘空间：** 保持至少 1 GB 可用空间 - 磁盘写满会导致数据损坏
5. **建议使用 UPS（不间断电源）：** 写入过程中断电会损坏文件
6. **关键配置纳入版本控制：** 为 router.config、i2ptunnel.config 建立 Git 仓库，以便回滚

**文件权限很重要：**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## 常见错误消息解读

I2P 的日志记录会提供能精准定位问题的具体错误信息。理解这些信息能加快故障排查。

**"No tunnels available"** 会在 router 尚未构建足够的 tunnels 以供运行时出现。这在启动后**前 5-10 分钟内是正常的**。如果持续超过 15 分钟：

1. 在 http://127.0.0.1:7657 确认 Active Peers > 10
2. 检查带宽分配是否足够（至少 128 KB/秒）
3. 在 http://127.0.0.1:7657/tunnels 查看 tunnel 成功率（应 >40%）
4. 查看日志以了解 tunnel 构建被拒原因

**"Clock skew detected"** 或 **"NTCP2 disconnect code 7"** 表示系统时间与网络共识时间相差超过 90 秒。I2P 要求 **±60 秒的时间精度**。与时间偏离的 router 的连接会被自动拒绝。

立即修复：

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** 或 **"Tunnel build timeout exceeded"** 表示通过 peer chain（对等节点链）进行的 tunnel 构建未能在超时窗口内完成（通常为 60 秒）。可能原因：

- **对等节点缓慢：** Router 为 tunnel 选择了无响应的参与者
- **网络拥塞：** I2P 网络正在承受高负载
- **带宽不足：** 您的带宽限制导致无法及时构建 tunnel
- **router 过载：** 过多的参与中继的 tunnels 正在消耗资源

解决方案：提高带宽，减少参与的 tunnels（`router.maxParticipatingTunnels` 位于 http://127.0.0.1:7657/configadvanced），启用端口转发以改进对等节点选择。

**"Router is shutting down"** 或 **"Graceful shutdown in progress"** 会在正常关机或崩溃恢复过程中出现。由于 router 会关闭 tunnels、通知对等节点并持久化状态，优雅关闭可能需要**最长 10 分钟**。

如果在关闭状态卡住超过 11 分钟，请强制终止：

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** 表示堆内存耗尽。立即的解决方案：

1. 编辑 wrapper.config：`wrapper.java.maxmemory=512`（或更高）
2. **必须完全关闭** - 重启不会应用更改
3. 等待 11 分钟以彻底关闭  
4. 全新启动 router
5. 在 http://127.0.0.1:7657/graphs 验证内存分配 - 应显示余量

**相关的内存错误：**

- **"GC overhead limit exceeded":** 垃圾回收耗时过多 - 增大堆内存
- **"Metaspace":** Java 类元数据空间耗尽 - 添加 `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**仅限 Windows：** 无论 wrapper.config 的设置如何，卡巴斯基杀毒软件都会将 Java 堆限制为 512MB - 请卸载或将 I2P 添加到排除列表。

**"Connection timeout"** 或 **"I2CP Error - port 7654"** 当应用程序尝试连接到 router 时：

1. 验证 router 正在运行: http://127.0.0.1:7657 应该有响应
2. 检查 I2CP 端口: `netstat -an | grep 7654` 应显示 LISTENING
3. 确保本地主机防火墙允许: `sudo ufw allow from 127.0.0.1`  
4. 验证应用程序使用了正确端口 (I2CP=7654, SAM=7656)

在 reseed 期间出现 **"证书验证失败"** 或 **"RouterInfo 损坏"**（RouterInfo：路由信息对象）：

根因：时钟偏移（先修复）、损坏的 netDb、无效的 reseed（引导种子）证书

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Database corruption detected"** 表示在 netDb 或 peerProfiles 中存在磁盘级的数据损坏：

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
使用 SMART（自监测、分析与报告技术）工具检查磁盘健康状况 - 反复出现的数据损坏表明存储设备可能正在出现故障。

## 平台特定的挑战

不同的操作系统在 I2P 部署方面会带来与权限、安全策略和系统集成相关的独特挑战。

### Linux 权限与服务问题

通过软件包安装的 I2P 以系统用户 **i2psvc** (Debian/Ubuntu) 或 **i2p** (其他发行版) 的身份运行，需要特定权限：

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**文件描述符限制** 会影响router的连接承载能力。默认限制（1024）对于高带宽router来说不足：

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
在 Debian/Ubuntu 上常见的 **AppArmor 冲突** 会阻止服务启动：

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**SELinux 问题** 在 RHEL/CentOS/Fedora 上:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**SystemD（Linux 初始化系统）服务故障排查:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Windows 防火墙和杀毒软件干扰

Windows Defender 和第三方防病毒产品经常会因其网络行为模式而将 I2P 标记为可疑。通过正确配置，可以在保持安全性的同时避免不必要的阻断。

**配置 Windows Defender 防火墙：**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
将端口 22648 替换为你在 http://127.0.0.1:7657/confignet 上的实际 I2P 端口。

**Kaspersky 防病毒软件特定问题:** 无论 wrapper.config 如何设置，Kaspersky 的 "Application Control" 都会将 Java 堆限制为 512MB。这会在高带宽的 router 上导致 OutOfMemoryError。

解决方案：1. 将 I2P 添加到卡巴斯基的排除列表：Settings → Additional → Threats and Exclusions → Manage Exclusions 2. 或卸载卡巴斯基（为 I2P 正常运行所推荐）

**第三方防病毒通用指南：**

- 将 I2P 安装目录添加到排除项  
- 将 %APPDATA%\I2P 和 %LOCALAPPDATA%\I2P 添加到排除项
- 将 javaw.exe 从行为分析中排除
- 禁用可能干扰 I2P 协议的“Network Attack Protection”功能

### macOS Gatekeeper 阻止安装

macOS Gatekeeper（macOS 的应用安全机制）会阻止未签名的应用程序运行。I2P 安装程序未使用 Apple 开发者 ID 进行签名，从而触发安全警告。

**为 I2P 安装程序绕过 Gatekeeper：**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**安装后运行** 仍可能触发警告：

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**切勿永久禁用 Gatekeeper（macOS 应用安全机制）** - 会给其他应用带来安全风险。仅使用针对特定文件的绕过。

**macOS 防火墙配置：**

1. 系统偏好设置 → 安全性与隐私 → 防火墙 → 防火墙选项
2. 点击 "+" 以添加应用程序  
3. 导航到 Java 安装路径（例如：`/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`）
4. 添加并将其设置为 "允许传入连接"

### Android I2P 应用程序问题

Android 版本约束与资源限制带来了独特的挑战。

**最低要求:** - 当前版本需要 Android 5.0+（API 级别 21+） - 至少 512MB RAM, 推荐 1GB+   - 应用与 router 数据占用 100MB 存储空间 - 为 I2P 禁用后台应用限制

**应用程序立即崩溃：**

1. **检查 Android 版本：** 设置 → 关于手机 → Android 版本（必须为 5.0+）
2. **卸载所有 I2P 版本：** 仅安装其中一种：
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   同时安装多个会产生冲突
3. **清除应用数据：** 设置 → 应用 → I2P → 存储 → 清除数据
4. **从干净状态重新安装**

**电池优化导致 router 被杀死：**

Android 会为节省电量而激进地终止后台应用。I2P 需要被排除（豁免）：

1. 设置 → 电池 → 电池优化（或 应用电池使用情况）
2. 找到 I2P → 不优化（或 允许后台活动）
3. 设置 → 应用 → I2P → 电池 → 允许后台活动 + 取消限制

**移动端连接问题：**

- **Bootstrap（引导）需要 WiFi：** 初始 reseed（引导获取节点数据）会下载大量数据 - 请使用 WiFi，而非蜂窝网络
- **网络变更：** I2P 对网络切换处理不佳 - 在 WiFi/蜂窝网络切换后重启应用
- **移动端带宽：** 建议保守配置为 64-128 KB/秒，以避免耗尽蜂窝数据流量

**移动端性能优化：**

1. I2P 应用 → 菜单 → 设置 → 带宽
2. 针对蜂窝网络，设置合适的限制：入站 64 KB/sec，出站 32 KB/sec
3. 减少参与的 tunnels：设置 → 高级 → 参与的 tunnels 最大数：100-200
4. 启用 "Stop I2P when screen off" 以节省电量

**在 Android 上的 BT 下载：**

- 将同时进行的种子数量限制为最多 2–3 个
- 降低 DHT（分布式哈希表）的激进程度  
- 仅在进行种子传输时使用 WiFi
- 接受在移动设备上的较慢速度

## Reseed（重新播种）和 bootstrap（引导）问题

新的 I2P 安装需要 **reseeding**（从公共 HTTPS 服务器获取初始节点信息的网络引导过程），以便加入网络。Reseed 问题会让用户陷入 0 个节点且无法访问网络的状态。

**在全新安装后出现 "No active peers"** 通常表示 reseed（初始引导获取节点）失败。症状：

- 已知 peers（对等节点）: 为 0 或一直低于 5
- "Network: Testing" 持续超过 15 分钟
- 日志显示 "Reseed failed" 或与 reseed（引导）服务器的连接错误

**为什么 reseed（网络引导）会失败：**

1. **防火墙阻止 HTTPS：** 企业/ISP 防火墙阻止到 reseed server（I2P 引导服务器）的连接（端口 443）
2. **SSL 证书错误：** 系统缺少最新的根证书
3. **代理要求：** 网络要求通过 HTTP/SOCKS 代理进行外部连接
4. **时钟偏差：** 当系统时间不正确时，SSL 证书验证会失败
5. **地域封锁：** 某些国家/ISP 会封锁已知的 reseed servers

**强制手动执行 reseed（重新引导）:**

1. 访问 http://127.0.0.1:7657/configreseed
2. 点击 "Save changes and reseed now"  
3. 在 http://127.0.0.1:7657/logs 监控是否出现 "Reseed got XX router infos"
4. 等待 5-10 分钟进行处理
5. 检查 http://127.0.0.1:7657 - Known peers（已知对等节点）应增加到 50+

**配置 reseed（初始引导）代理** 用于受限网络:

http://127.0.0.1:7657/configreseed → 代理配置：

- HTTP 代理: [proxy-server]:[port]
- 或 SOCKS5: [socks-server]:[port]  
- 启用 "Use proxy for reseed only"（仅在 reseed（重新引导）时使用代理）
- 如有需要，提供凭据
- 保存并强制进行 reseed

**替代方案：用于 reseed（I2P 网络数据库的引导/重新播种）的 Tor 代理：**

如果 Tor Browser 或 Tor 守护进程正在运行：

- 代理类型：SOCKS5
- 主机：127.0.0.1
- 端口：9050（默认 Tor SOCKS 端口）
- 启用并进行 reseed（重新引导）

**通过 su3 文件手动 reseed（重新播种）** (最后手段):

当所有自动 reseed（重新播种）均失败时，通过带外方式获取 reseed 文件：

1. 在不受限制的连接上从可信来源下载 i2pseeds.su3 (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. 完全停止 I2P
3. 将 i2pseeds.su3 复制到 ~/.i2p/ 目录  
4. 启动 I2P - 会自动解压并处理该文件
5. 处理完成后删除 i2pseeds.su3
6. 在 http://127.0.0.1:7657 验证节点数量是否增加

**在 reseed（引导种子获取）期间的 SSL 证书错误：**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
解决方案：

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**超过 30 分钟仍然为 0 个已知节点：**

表示 reseed（为 netDb 获取初始 RouterInfo 的过程）完全失败。故障排查顺序：

1. **确认系统时间准确**（最常见的问题 - 请先修复）
2. **测试 HTTPS 连通性：** 在浏览器中尝试访问 https://reseed.i2p.rocks - 如果失败，则为网络问题
3. **检查 I2P 日志** 在 http://127.0.0.1:7657/logs 查看特定的 reseed（引导）错误
4. **尝试不同的 reseed URL：** http://127.0.0.1:7657/configreseed → 添加自定义 reseed URL: https://reseed-fr.i2pd.xyz/
5. **使用手动 su3 文件方法** 若自动化尝试已用尽

**Reseed servers（用于初始引导的服务器）偶尔离线：** I2P 内置多个硬编码的 reseed servers。如果其中一个不可用，router 会自动尝试其他的。所有 reseed servers 全部失效的情况极为罕见，但并非不可能。

**当前活跃的 reseed（引导）服务器** (截至2025年10月):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

如果默认配置存在问题，请添加为自定义 URL。

**对于身处网络审查严厉地区的用户:**

可以考虑通过 Tor 使用 Snowflake/Meek 桥进行初始 reseed（引导），随后在完成接入后切换为直接连接 I2P。或者从审查区域之外，通过隐写术、电子邮件或 U 盘获取 i2pseeds.su3。

## 何时寻求进一步的帮助

本指南涵盖了绝大多数 I2P 问题，但某些问题需要开发者的关注或社区的专业知识。

**在以下情况下，请向 I2P 社区寻求帮助：**

- 按所有故障排除步骤操作后，Router 仍持续崩溃
- 内存泄漏导致内存占用持续增长，超出已分配的堆大小
- 尽管配置得当，tunnel 成功率仍低于 20%  
- 日志中出现本指南未涵盖的新错误
- 发现安全漏洞
- 功能请求或增强建议

**在请求帮助之前，请先收集诊断信息：**

1. I2P 版本: http://127.0.0.1:7657 (例如, "2.10.0")
2. Java 版本: `java -version` 输出
3. 操作系统和版本
4. router 状态: 网络状态, 活跃对等节点数量, 参与的 tunnels
5. 带宽配置: 入站/出站限制
6. 端口转发状态: 被防火墙阻挡或 OK
7. 相关日志摘录: 来自 http://127.0.0.1:7657/logs 的显示错误的最后 50 行

**官方支持渠道:**

- **论坛:** https://i2pforum.net (明网) 或 http://i2pforum.i2p (I2P 网络内)
- **IRC:** #i2p 在 Irc2P 上 (irc.postman.i2p 经由 I2P) 或 irc.freenode.net (明网)
- **Reddit:** https://reddit.com/r/i2p 用于社区讨论
- **缺陷跟踪器:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues 用于已确认的缺陷
- **邮件列表:** i2p-dev@lists.i2p-projekt.de 用于开发相关问题

**合理预期很重要。** 由于其基础设计，I2P 比明网更慢——多跳加密的 tunnel 会带来固有时延。一个 I2P router 在页面加载需 30 秒、BT 速度只有 50 KB/秒的情况下，依然是**正常工作的**，并非故障。无论如何进行配置优化，期待明网速度的用户都会失望。

## 结论

大多数 I2P 问题源于三类情况：在引导阶段（bootstrap）缺乏耐心（需要 10–15 分钟）、资源分配不足（至少 512 MB 内存和 256 KB/秒带宽）、或端口转发配置错误。理解 I2P 的分布式架构和以匿名性为核心的设计，有助于用户区分预期行为与真正的问题。

router 的 "Firewalled" 状态虽然并不理想，但并不会阻止 I2P 的使用 - 只是会限制对网络的贡献，并使性能略有下降。新用户应当优先考虑**稳定性而非优化**：在调整高级设置之前，先让 router 连续运行数天，因为随着在线时长的增加，与网络的整合会自然改善。

排障时，务必先核查基础项：系统时间是否正确、带宽是否充足、router 是否持续运行，以及是否有 10 个以上的活跃对等节点。多数问题通过解决这些基础项即可排除，而不必去调整晦涩的配置参数。I2P 会随着持续运行而回报耐心：在数天乃至数周的在线时间里，router 会逐步累积声誉并优化对等节点选择，从而带来更好的性能。
