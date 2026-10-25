---
title: "旧 Tunnel 实现"
description: "I2P在0.6.1.10版本之前原始tunnel实现的历史文档"
slug: "old-tunnel-implementation"
aliases:
  - "/zh/docs/historical/tunnel-alt"
  - "/zh/docs/historical/tunnel-alt/"
  - "/zh/tunnel"
  - "/zh/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**注意：已废弃 - 不再使用！在 0.6.1.10 版本中被替换 - 请参阅[当前实现](/docs/specs/tunnel-implementation)获取有效规范。**

## 1) Tunnel 概述 {#tunnel.overview}

在I2P中，消息通过由对等节点组成的虚拟tunnel单向传递，使用任何可用的方式将消息传递给下一跳。消息到达tunnel的网关，被打包用于路径传输，然后转发给tunnel中的下一跳，下一跳处理并验证消息的有效性，然后发送给再下一跳，如此继续，直到到达tunnel端点。该端点接收由网关打包的消息，并按指示转发它们——要么转发给另一个router，要么转发给另一个router上的另一个tunnel，或者在本地处理。

tunnel的工作原理都相同，但可以分为两个不同的组别 - inbound tunnel和outbound tunnel。inbound tunnel有一个不受信任的网关，将消息向下传递给tunnel创建者，tunnel创建者充当tunnel端点。对于outbound tunnel，tunnel创建者充当网关，将消息传出到远程端点。

tunnel的创建者精确选择哪些节点将参与该tunnel，并为每个节点提供必要的配置数据。tunnel的长度可以从0跳（gateway同时也是端点）到7跳（在gateway之后和端点之前有6个节点）不等。其设计意图是让参与者或第三方都难以确定tunnel的长度，甚至让共谋的参与者也无法确定他们是否属于同一个tunnel（除非共谋的节点在tunnel中彼此相邻）。被损坏的消息也会尽快丢弃，以减少网络负载。

除了长度之外，每个tunnel还有其他可配置的参数可以使用，例如对传输消息的大小或频率进行限流、如何使用填充、tunnel应该运行多长时间、是否注入干扰消息、是否使用分片，以及应该采用什么样的批处理策略（如果有的话）。

在实践中，会使用一系列的tunnel池来服务于不同的目的 - 每个本地客户端目标都有自己的一套入站tunnel和出站tunnel，配置以满足其匿名性和性能需求。此外，router本身还维护一系列池用于参与网络数据库和管理tunnel本身。

I2P本质上是一个分组交换网络，即使使用这些tunnel，也允许它利用并行运行的多个tunnel，从而增强弹性并平衡负载。在核心I2P层之外，还有一个可选的端到端流传输库供客户端应用程序使用，它提供类似TCP的操作，包括消息重排序、重传、拥塞控制等功能。

## 2) Tunnel 操作 {#tunnel.operation}

tunnel 操作包含四个不同的过程，由 tunnel 中的各个节点承担。首先，tunnel gateway 收集若干 tunnel 消息并将其预处理为适合 tunnel 传输的格式。接下来，该 gateway 对预处理的数据进行加密，然后转发给第一跳。该节点以及后续的 tunnel 参与者会解除一层加密，验证消息的完整性，然后将其转发给下一个节点。最终，消息到达端点，由 gateway 打包的消息被重新分离出来并按照请求进行转发。

Tunnel ID是在每一跳使用的4字节数字 - 参与者知道应该监听哪个tunnel ID的消息，以及应该使用哪个tunnel ID转发到下一跳。Tunnel本身是短暂的（目前为10分钟），但根据tunnel的用途，尽管后续的tunnel可能使用相同的对等节点序列构建，但每一跳的tunnel ID都会发生变化。

### 2.1) 消息预处理 {#tunnel.preprocessing}

当网关想要通过tunnel传输数据时，它首先收集零个或多个I2NP消息（不超过32KB），选择使用多少填充，并决定每个I2NP消息应该如何被tunnel端点处理，将这些数据编码到原始tunnel载荷中：

- 2字节无符号整数，指定填充字节数量
- 相应数量的随机字节
- 一系列零个或多个 { 指令, 消息 } 对

指令编码如下：

- 1字节值：
  ```
  bits 0-1: 传递类型
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: 包含延迟？ (1 = true, 0 = false)
     bit 3: 分片？ (1 = true, 0 = false)
     bit 4: 扩展选项？ (1 = true, 0 = false)
  bits 5-7: 保留
  ```
- 如果传递类型是TUNNEL，则为4字节tunnel ID
- 如果传递类型是TUNNEL或ROUTER，则为32字节router哈希
- 如果包含延迟标志为true，则为1字节值：
  ```
     bit 0: 类型 (0 = 严格, 1 = 随机)
  bits 1-7: 延迟指数 (2^值 分钟)
  ```
- 如果分片标志为true，则为4字节消息ID，以及1字节值：
  ```
  bits 0-6: 分片编号
     bit 7: 是最后一个？ (1 = true, 0 = false)
  ```
- 如果扩展选项标志为true：
  ```
  = 1字节选项大小（字节数）
  = 对应字节数的数据
  ```
- I2NP消息的2字节大小

I2NP 消息以其标准形式编码，预处理的负载必须填充到 16 字节的倍数。

### 2.2) 网关处理 {#tunnel.gateway}

在将消息预处理为填充载荷后，gateway使用八个密钥对载荷进行加密，构建一个校验和块，使每个peer都能随时验证载荷的完整性，同时还构建一个端到端验证块供tunnel端点验证校验和块的完整性。具体细节如下。

所使用的加密方式使得解密只需要用AES在CBC模式下处理数据，计算消息特定固定部分的SHA256哈希值（第16字节到第$size-144字节），然后在校验块中搜索该哈希值的前16个字节。定义了固定的跳数（8个节点），这样我们可以在不泄露tunnel中位置信息的情况下验证消息，也避免了消息在剥离层次时持续"收缩"。对于少于8跳的tunnel，tunnel创建者将替代多余的跳数，使用他们的密钥进行解密（对于出站tunnel，这在开始时完成，对于入站tunnel，则在结束时完成）。

加密中的难点是构建那个纠缠的校验和块，这实质上需要找出载荷在每个步骤中的哈希值会是什么样子，随机排列这些哈希值，然后构建一个矩阵来表示每个随机排列的哈希值在每个步骤中的样子。gateway本身必须假装它是校验和块中的一个对等节点，这样第一跳就无法判断前一跳是gateway。为了更好地理解这一点：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
在上述过程中，P[7] 与通过 tunnel 传输的原始数据（预处理的消息）相同，V[7] 是 peer7 解密后看到的 eH[0-7] 的 SHA256 的前 16 个字节。对于矩阵中"高于"哈希值的单元格，它们的值是通过使用下方节点的密钥对其下方的单元格进行加密得出的，使用其左侧列的末尾作为 IV。对于矩阵中"低于"哈希值的单元格，它们等于其上方的单元格，由当前节点的密钥解密，使用该行上前一个加密块的末尾作为 IV。

通过这个随机化的校验块矩阵，每个节点都能够找到载荷的哈希值，或者如果不存在，则知道消息已损坏。通过使用CBC模式进行纠缠增加了对校验块本身进行标记的难度，但如果被标记数据之后的列已经在某个节点上用于检查载荷，那么这种标记仍可能短暂地不被检测到。无论如何，tunnel端点（节点7）可以确定地知道是否有任何校验块被标记，因为这会损坏验证块（V[7]）。

IV[0] 是一个随机的 16 字节值，IV[i] 是 H(D(IV[i-1], K[i-1]) xor IV_WHITENER) 的前 16 字节。我们不在路径中使用相同的 IV，因为这会允许trivial collusion（简单共谋），我们使用解密值的哈希来传播 IV，以阻碍密钥泄露。IV_WHITENER 是一个固定的 16 字节值。

当网关想要发送消息时，它会导出对应第一跳节点的正确行（通常是 peer1.recv 行）并完整转发。

### 2.3) 参与者处理 {#tunnel.participant}

当tunnel中的参与者收到消息时，他们使用AES256在CBC模式下用他们的tunnel密钥解密一层，前16个字节作为IV。然后他们计算所看到的载荷（第16字节到第$size-144字节）的哈希值，并在解密的校验和块中搜索该哈希值的前16个字节。如果没有找到匹配项，消息将被丢弃。否则，通过解密IV来更新IV，将该值与IV_WHITENER进行异或运算，并用其哈希值的前16个字节替换它。然后将生成的消息转发给下一个对等节点进行处理。

为了防止tunnel级别的重放攻击，每个参与者都会跟踪在tunnel生命周期内收到的IV，拒绝重复的IV。所需的内存使用量应该很少，因为每个tunnel只有很短的生命周期（目前是10分钟）。通过一个tunnel以恒定100KBps速度传输完整32KB消息将产生1875条消息，需要不到30KB的内存。Gateway和endpoint通过跟踪tunnel中包含的I2NP消息的消息ID和过期时间来处理重放。

### 2.4) 端点处理 {#tunnel.endpoint}

当消息到达tunnel端点时，它们会像普通参与者一样解密和验证消息。如果校验和块有有效匹配，端点随后计算校验和块本身的哈希值（解密后看到的），并将其与解密的验证哈希值（最后16个字节）进行比较。如果该验证哈希值不匹配，端点会记录tunnel参与者之一的标记尝试，并可能丢弃该消息。

此时，tunnel 端点拥有由网关发送的预处理数据，然后可以将其解析为包含的 I2NP 消息，并根据其传递指令的要求转发它们。

### 2.5) 填充 {#tunnel.padding}

有几种tunnel填充策略可供选择，每种都有其自身的优点：

- 无填充
- 填充到随机大小
- 填充到固定大小
- 填充到最接近的KB
- 填充到最接近的指数大小（2^n字节）

*应该使用哪种方式？无填充是最高效的，随机填充是我们现在使用的，固定大小要么造成极大浪费，要么迫使我们实现分片。填充到最接近的指数大小（类似Freenet）看起来很有前景。也许我们应该收集一些网络上消息大小的统计数据，然后看看不同策略会带来什么成本和收益？*

### 2.6) Tunnel 分片 {#tunnel.fragmentation}

对于各种填充和混合方案，从匿名性角度来看，将单个I2NP消息分割成多个部分可能是有用的，每个部分通过不同的tunnel消息单独传送。端点可能支持也可能不支持这种分片（根据需要丢弃或保留分片），处理分片功能不会立即实现。

### 2.7) 替代方案 {#tunnel.alternatives}

#### 2.7.1) 不使用校验和块 {#tunnel.nochecksum}

上述过程的一个替代方案是完全移除校验和块，并用负载的普通哈希值替换验证哈希。这将简化 tunnel 网关的处理过程，并在每一跳节省144字节的带宽。另一方面，tunnel 内的攻击者可以轻易地将消息大小调整为一个容易被串通的外部观察者以及后续 tunnel 参与者追踪的大小。损坏还会导致传递消息所需的整个带宽的浪费。没有逐跳验证，也可能通过构建极长的 tunnel 或在 tunnel 中构建循环来消耗过多的网络资源。

#### 2.7.2) 中途调整 tunnel 处理 {#tunnel.reroute}

虽然简单的 tunnel 路由算法对大多数情况应该是足够的，但还有三种可以探索的替代方案：

- 在 tunnel 内的任意跳延迟消息，可以是指定的时间量或随机时间段。这可以通过用例如哈希值的前8字节替换校验和块中的哈希值来实现，然后跟随一些延迟指令。或者，指令可以告诉参与者按原样解释原始载荷，并要么丢弃消息，要么继续将其转发到路径下一跳（在那里端点会将其解释为chaff消息）。后一部分需要网关调整其加密算法，以在不同的跳上产生明文载荷，但这应该不会有太大麻烦。

- 允许参与 tunnel 的 router 在转发消息之前重新混合消息 - 通过该对等节点自己的出站 tunnel 之一来反弹消息，携带传递到下一跳的指令。这可以以受控方式使用（使用如上述延迟等途中指令）或概率性使用。

- 为tunnel创建者实现代码，以重新定义对等节点在tunnel中的"下一跳"，允许进一步的动态重定向。

#### 2.7.3) 使用双向 tunnel {#tunnel.bidirectional}

当前使用两个独立tunnel进行入站和出站通信的策略并非唯一可用的技术，并且确实存在匿名性方面的影响。从积极的一面来看，通过使用独立的tunnel，它减少了暴露给tunnel参与者进行分析的流量数据——例如，来自网页浏览器的出站tunnel中的对等节点只会看到HTTP GET的流量，而入站tunnel中的对等节点会看到沿tunnel传递的载荷。使用双向tunnel时，所有参与者都能够获知例如一个方向发送了1KB数据，然后另一个方向发送了100KB数据的事实。从消极的一面来看，使用单向tunnel意味着需要分析和考虑两组对等节点，并且必须采取额外的谨慎措施来应对前驱攻击速度的增加。下面概述的tunnel池化和构建过程应该能够最小化对前驱攻击的担忧，不过如果需要的话，沿着相同的对等节点构建入站和出站tunnel也不会有太大麻烦。

#### 2.7.4) 使用更小的块大小 {#tunnel.smallerhashes}

目前，我们使用 AES 将块大小限制为 16 字节，这反过来为校验和块的每一列提供了最小大小。如果使用具有更小块大小的其他算法，或者能够安全地使用更小的哈希部分构建校验和块，那么可能值得探索。现在每一跳使用的 16 字节应该是足够的。

## 3) Tunnel 构建 {#tunnel.building}

在构建tunnel时，创建者必须向每个跳数发送包含必要配置数据的请求，然后等待潜在参与者回复表示他们同意或不同意。这些tunnel请求消息及其回复都经过garlic encryption包装，只有知道密钥的router才能解密，而且双向传输路径也通过tunnel路由。在生成tunnel时需要记住三个重要维度：使用什么对等节点（以及在哪里使用），如何发送请求（以及接收回复），以及如何维护它们。

### 3.1) 对等节点选择 {#tunnel.peerselection}

除了两种类型的 tunnel - inbound 和 outbound - 还有两种用于不同 tunnel 的对等节点选择方式 - exploratory 和 client。Exploratory tunnel 用于网络数据库维护和 tunnel 维护，而 client tunnel 用于端到端的客户端消息传输。

#### 3.1.1) 探索性 tunnel 节点选择 {#tunnel.selection.exploratory}

探索性 tunnel 是从网络子集中随机选择的对等节点构建的。特定的子集因本地 router 以及其 tunnel 路由需求而异。一般来说，探索性 tunnel 是由随机选择的对等节点构建的，这些节点属于对等节点的"未失效但活跃"配置文件类别。除了单纯的 tunnel 路由之外，tunnel 的第二个目的是发现未充分利用的高容量对等节点，以便将其提升为客户端 tunnel 使用。

#### 3.1.2) 客户端 tunnel 节点选择 {#tunnel.selection.client}

客户端tunnel的构建有着更严格的要求集合——本地router会从其"快速且高容量"配置文件类别中选择对等节点，以确保性能和可靠性能够满足客户端应用程序的需求。然而，除了这种基本选择之外，还有几个重要的细节需要遵循，具体取决于客户端的匿名性需求。

对于一些担心对手发动前驱攻击的客户端，tunnel 选择可以保持对等节点按严格顺序选择——如果 A、B 和 C 在一个 tunnel 中，A 之后的跳跃点始终是 B，B 之后的跳跃点始终是 C。也可以采用不太严格的排序，确保虽然 A 之后的跳跃点可能是 B，但 B 永远不能在 A 之前。其他配置选项包括仅将入站 tunnel 网关和出站 tunnel 端点设为固定，或按 MTBF 频率轮换。

### 3.2) 请求传递 {#tunnel.request}

如上所述，一旦tunnel创建者知道哪些节点应该加入tunnel以及它们的顺序，创建者就会构建一系列tunnel请求消息，每个消息都包含该节点所需的必要信息。例如，参与的tunnel将被给予4字节的tunnel ID用于接收消息，4字节的tunnel ID用于发送消息，下一跳身份的32字节哈希，以及用于从tunnel中移除一层的32字节层密钥。当然，出站tunnel端点不会被给予任何"下一跳"或"下一个tunnel ID"信息。然而，入站tunnel网关会按照应该加密的顺序被给予8个层密钥（如上所述）。为了允许回复，请求包含一个随机会话标签和一个随机会话密钥，节点可以用它们来garlic加密其决定，以及应该发送该garlic的tunnel。除了上述信息外，还可能包含各种客户端特定选项，例如对tunnel施加什么限流、使用什么填充或批处理策略等。

在构建所有请求消息后，它们会被garlic加密包装发送给目标router，并通过探索性tunnel发出。收到消息后，该对等节点确定是否能够或愿意参与，创建回复消息，并使用提供的信息对响应进行garlic包装和tunnel路由。当tunnel创建者收到回复时，该tunnel在该跳跃上被认为是有效的（如果被接受）。一旦所有对等节点都接受了，tunnel就变为活跃状态。

### 3.3) 池化 {#tunnel.pooling}

为了实现高效运行，router 维护一系列 tunnel 池，每个池管理一组用于特定目的的 tunnel，并具有各自的配置。当需要某个用途的 tunnel 时，router 会从相应的池中随机选择一个。总体而言，有两个探索性 tunnel 池 - 一个入站和一个出站 - 每个都使用 router 的探索默认设置。此外，每个本地目的地都有一对池 - 一个入站和一个出站 tunnel。这些池使用本地目的地连接到 router 时指定的配置，如果未指定则使用 router 的默认设置。

每个池在其配置中都有几个关键设置，定义了要保持多少个活跃的tunnel、在故障情况下维护多少个备用tunnel、测试tunnel的频率、tunnel的长度、这些长度是否应该随机化、替换tunnel的构建频率，以及配置单个tunnel时允许的任何其他设置。

### 3.4) 替代方案 {#tunnel.building.alternatives}

#### 3.4.1) 望远镜式构建 {#tunnel.building.telescoping}

关于使用探索性 tunnel 发送和接收 tunnel 创建消息的一个可能出现的问题是，这如何影响 tunnel 对前驱攻击的脆弱性。虽然这些 tunnel 的端点和网关将在网络中随机分布（甚至可能包括 tunnel 创建者在该集合中），但另一种替代方案是使用 tunnel 路径本身来传递请求和响应，就像在 [TOR](https://www.torproject.org/) 中所做的那样。然而，这可能会在 tunnel 创建过程中导致泄露，允许对等节点通过监控 tunnel 构建时的时序或数据包计数来发现 tunnel 后续有多少跳。可以使用一些技术来最小化这个问题，比如在继续构建下一跳之前，将每个跳用作端点（参见 [2.7.2](#tunnel.reroute)）处理随机数量的消息。

#### 3.4.2) 用于管理的非探索性 tunnel {#tunnel.building.nonexploratory}

tunnel构建过程的第二个替代方案是为router提供一组额外的非探索性入站和出站池，将这些池用于tunnel请求和响应。假设router对网络有良好的整合视图，这应该是不必要的，但如果router在某种程度上被分割，使用非探索性池进行tunnel管理将减少关于router分区中有哪些对等节点的信息泄露。

## 4) Tunnel 限流 {#tunnel.throttling}

尽管I2P内的tunnel与电路交换网络相似，但I2P内的一切都严格基于消息传递 - tunnel仅仅是帮助组织消息传递的记账技巧。不对消息的可靠性或顺序做任何假设，重传由更高层处理（例如I2P的客户端层流式传输库）。这使得I2P能够利用包交换和电路交换网络都可用的限流技术。例如，每个router可以跟踪每个tunnel使用数据量的移动平均值，将其与该router参与的所有其他tunnel使用的平均值相结合，并能够根据其容量和利用率接受或拒绝额外的tunnel参与请求。另一方面，每个router可以简单地丢弃超出其容量的消息，利用在普通互联网上使用的研究成果。

## 5) 混合/批处理 {#tunnel.mixing}

在网关和每个跳点应该使用什么策略来延迟、重新排序、重新路由或填充消息？这些操作应该在多大程度上自动完成，多少应该配置为每个 tunnel 或每个跳点的设置，以及 tunnel 的创建者（进而是用户）应该如何控制这些操作？所有这些都是未知的，留待未来版本中解决。
