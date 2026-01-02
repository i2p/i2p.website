---
title: "Tunnel 路由"
description: "I2P tunnel 术语、构建和生命周期概述"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

I2P 构建临时的单向 tunnel——由按顺序排列的 router 组成的序列,用于转发加密流量。Tunnel 分为 **inbound**(消息流向创建者)或 **outbound**(消息流向远离创建者)两种类型。

典型的交换过程是这样的：Alice 的消息通过她的一条出站 tunnel 发出，指示出站端点将消息转发到 Bob 的某条入站 tunnel 的网关，然后 Bob 在其入站端点接收消息。

![Alice 通过她的出站 tunnel 连接到 Bob 的入站 tunnel](/images/tunnelSending.png)

- **A**: Outbound Gateway（Alice）
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint（Bob）

隧道具有固定的 10 分钟生命周期,并传输固定大小的 1024 字节消息(包含隧道头部为 1028 字节),以防止基于消息大小或时间模式的流量分析。

## 隧道术语表

- **Tunnel gateway（隧道网关）：** 隧道中的第一个 router。对于入站隧道，该 router 的身份会出现在已发布的 [LeaseSet](/docs/specs/common-structures/) 中。对于出站隧道，gateway 是发起的 router（上文中的 A 和 D）。
- **Tunnel endpoint（隧道端点）：** 隧道中的最后一个 router（上文中的 C 和 F）。
- **Tunnel participant（隧道参与者）：** 隧道中的中间 router（上文中的 B 和 E）。参与者无法确定其位置或隧道方向。
- **n-hop tunnel（n 跳隧道）：** router 之间的跳数。
  - **0-hop：** gateway 和 endpoint 是同一个 router——匿名性最低。
  - **1-hop：** gateway 直接连接到 endpoint——低延迟,低匿名性。
  - **2-hop：** 探索性隧道的默认设置;安全性/性能均衡。
  - **3-hop：** 推荐用于需要强匿名性的应用程序。
- **Tunnel ID（隧道 ID）：** 每个 router 和每一跳的 4 字节唯一整数,由创建者随机选择。每一跳接收和转发使用不同的 ID。

## 隧道构建信息

在隧道构建消息中，充当网关、参与者和端点角色的路由器会收到不同的记录。现代 I2P 支持两种方法：

- **ElGamal**（旧版，528字节记录）
- **ECIES-X25519**（当前版本，通过短隧道构建消息 – STBM 实现218字节记录）

### Information Distributed to Participants

**网关接收：** - Tunnel 层密钥（根据隧道类型使用 AES-256 或 ChaCha20 密钥） - Tunnel IV 密钥（用于加密初始化向量） - 应答密钥和应答 IV（用于构建应答加密） - Tunnel ID（仅入站网关） - 下一跳身份哈希和 tunnel ID（如果非终端节点）

**中间参与者接收：** - 其跃点的 tunnel 层密钥和 IV 密钥 - Tunnel ID 和下一跳信息 - 用于构建响应加密的回复密钥和 IV

**端点接收：** - Tunnel 层和 IV 密钥 - 应答 router 和 tunnel ID（仅限出站端点）- 应答密钥和 IV（仅限出站端点）

详细信息请参阅 [Tunnel Creation Specification](/docs/specs/implementation/) 和 [ECIES Tunnel Creation Specification](/docs/specs/implementation/)。

## Tunnel Pooling

Router 将 tunnel 分组为 **tunnel pool**（隧道池），以实现冗余和负载分配。每个池维护多个并行的 tunnel，当一个失败时可以进行故障转移。内部使用的池称为 **exploratory tunnel**（探索隧道），而特定应用的池称为 **client tunnel**（客户端隧道）。

每个目标地址维护独立的入站和出站池，通过 I2CP 选项进行配置（tunnel 数量、备份数量、长度和 QoS 参数）。Router 监控 tunnel 健康状况，运行定期测试，并自动重建失败的 tunnel 以维持池的规模。

## 隧道池

**0-hop Tunnels（零跳隧道）**：仅提供合理推诿性。流量始终在同一个 router 发起和终止——不建议用于任何匿名用途。

**1跳隧道**：针对被动观察者提供基本的匿名性,但如果对手控制了那个单跳节点则容易受到攻击。

**2跳隧道**：包含两个远程路由器，显著增加攻击成本。探索性隧道池的默认设置。

**3跳隧道（3-hop Tunnels）**：推荐用于需要强大匿名保护的应用程序。额外的跳数会增加延迟，但不会带来有意义的安全增益。

**默认设置**：路由器使用**2跳**探索性隧道和针对应用的**2或3跳**客户端隧道,在性能和匿名性之间取得平衡。

## 隧道长度

Router 会定期通过出站 tunnel 向入站 tunnel 发送 `DeliveryStatusMessage` 来测试 tunnel。如果测试失败,两条 tunnel 都会收到负面的配置文件权重。连续失败会将 tunnel 标记为不可用;然后 router 会重建一个替代 tunnel 并发布新的 LeaseSet。测试结果会反馈到对等节点容量指标中,供[对等节点选择系统](/docs/overview/tunnel-routing/)使用。

## 隧道测试

Routers 使用非交互式的**伸缩式**方法构建 tunnels：单个 Tunnel Build Message 逐跳传播。每一跳解密其记录，添加其回复，并转发消息。最后一跳通过不同的路径返回聚合的构建回复，防止关联。现代实现对 ECIES 使用 **Short Tunnel Build Messages (STBM)**，对传统路径使用 **Variable Tunnel Build Messages (VTBM)**。每条记录使用 ElGamal 或 ECIES-X25519 进行逐跳加密。

## 隧道创建

隧道流量使用多层加密。当消息穿过隧道时,每一跳都会添加或移除一层加密。

- **ElGamal tunnels:** 使用 AES-256/CBC 加密载荷,采用 PKCS#5 填充。
- **ECIES tunnels:** 使用 ChaCha20 或 ChaCha20-Poly1305 进行认证加密。

每个跳点有两个密钥：**层密钥**和 **IV 密钥**。路由器解密 IV，使用它来处理有效载荷,然后在转发之前重新加密 IV。这种双重 IV 方案可以防止消息标记。

出站网关预先解密所有层，使得端点在所有参与者添加加密后接收明文。入站 tunnel 以相反方向加密。参与者无法确定 tunnel 方向或长度。

## 隧道加密

- 动态隧道生命周期和自适应池大小调整以实现网络负载均衡
- 备用 tunnel 测试策略和单个跳点诊断
- 可选的工作量证明或带宽证书验证(在 API 0.9.65+ 中实现)
- 流量整形和填充数据插入研究以实现端点混合
- 持续淘汰 ElGamal 并迁移到 ECIES-X25519

## 持续开发

- [Tunnel 实现规范](/docs/specs/implementation/)
- [Tunnel 创建规范 (ElGamal)](/docs/specs/implementation/)
- [Tunnel 创建规范 (ECIES-X25519)](/docs/specs/implementation/)
- [Tunnel 消息规范](/docs/specs/implementation/)
- [Garlic 路由](/docs/overview/garlic-routing/)
- [I2P 网络数据库](/docs/specs/common-structures/)
- [节点评估与选择](/docs/overview/tunnel-routing/)
- [I2P 威胁模型](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag 加密](/docs/legacy/elgamal-aes/)
- [I2CP 选项](/docs/specs/i2cp/)
