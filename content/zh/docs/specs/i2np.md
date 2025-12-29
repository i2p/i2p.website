---
title: "I2P 网络协议 (I2NP)"
description: "I2P 内部 router 之间的消息格式、优先级和大小限制。"
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

I2P 网络协议（I2NP）定义了 routers（路由器）如何交换消息、选择传输协议，并在保持匿名性的同时混合流量。它运行在 **I2CP**（客户端 API）与传输协议（**NTCP2** 和 **SSU2**）之间。

I2NP 是位于 I2P 传输协议之上的一层。它是一个 router 到 router 的协议，用于: - 网络数据库查询与应答 - 创建 tunnel - 加密的 router 和客户端数据消息

I2NP 消息既可以点对点发送至另一台 router，也可以通过 tunnels 匿名地发送至该 router。

router 使用本地优先级将出站任务入队。优先级数值越高，越先处理。高于标准 tunnel 数据优先级（400）的任何任务都会被视为紧急。

### 当前传输协议

I2P 现在适用于 IPv4 和 IPv6，并使用 **NTCP2**（TCP）和 **SSU2**（UDP）。这两种传输采用: - **X25519** 密钥交换（Noise 协议框架） - **ChaCha20/Poly1305** 认证加密（AEAD） - **SHA-256** 哈希

**已移除的旧版传输:** - NTCP (原始 TCP) 已在 Java router 的 0.9.50 版本 (2021 年 5 月) 中移除 - SSU v1 (原始 UDP) 已在 Java router 的 2.4.0 版本 (2023 年 12 月) 中移除 - SSU v1 已在 i2pd 的 2.44.0 版本 (2022 年 11 月) 中移除

截至2025年，网络已完全过渡到基于 Noise（加密握手协议框架）的传输方式，不再支持任何旧版传输。

---

## 版本编号系统

**重要：** I2P 使用双重版本编号体系，必须清楚理解：

### 发布版本（面向用户）

以下是用户可见并可下载的版本: - 0.9.50 (2021 年 5 月) - 最后一个 0.9.x 版本 - **1.5.0** (2021 年 8 月) - 首个 1.x 版本 - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (贯穿 2021-2022 年) - **2.0.0** (2022 年 11 月) - 首个 2.x 版本 - 2.1.0 至 2.9.0 (贯穿 2023-2025 年) - **2.10.0** (2025 年 9 月 8 日) - 当前版本

### API 版本 (协议兼容性)

以下是在 RouterInfo 属性的 "router.version" 字段中发布的内部版本号： - 0.9.50（2021 年 5 月） - **0.9.51**（2021 年 8 月） - 面向 1.5.0 发行版的 API 版本 - 0.9.52 至 0.9.66（并持续到 2.x 系列发行版） - **0.9.67**（2025 年 9 月） - 面向 2.10.0 发行版的 API 版本

**要点：** 没有任何编号为 0.9.51 到 0.9.67 的版本发布。这些编号仅作为 API 版本标识存在。I2P 从 0.9.50 版本直接跳到 1.5.0。

### 版本映射表

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**即将发布：** 2.11.0 版本（计划于 2025 年 12 月发布）将要求 Java 17+，并默认启用后量子密码学。

---

## 协议版本

所有 router 必须在 RouterInfo（router 信息记录）的属性中的 "router.version" 字段里发布其 I2NP 协议版本。该版本字段是 API 版本，用于指示对各类 I2NP 协议特性的支持程度，并不一定等同于实际的 router 版本。

如果替代（非 Java）的 routers 希望发布有关实际 router 实现的任何版本信息，必须在另一项属性中进行。除下文列出的版本外，允许使用其他版本。支持情况将通过数值比较来确定；例如，0.9.13 意味着支持 0.9.12 的功能。

**注意：** 属性 "coreVersion" 已不再在 router 信息中发布，且从未用于确定 I2NP 协议版本。

### API 版本功能摘要

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**注意：** 还存在与传输相关的特性和兼容性问题。详情请参阅 NTCP2 和 SSU2 的传输文档。

---

## 消息头部

I2NP 使用逻辑上的 16 字节头部结构，而现代传输协议（NTCP2 和 SSU2）采用精简的 9 字节头部，省略了冗余的长度和校验和字段。这些字段在概念上仍然等价。

### 头部格式比较

**标准格式（16 字节）：**

用于旧版 NTCP 传输，以及当 I2NP 消息被嵌入到其他消息中时 (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**SSU 的短格式（已废弃，5 字节）：**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**NTCP2、SSU2 以及 ECIES-Ratchet Garlic Cloves (蒜瓣) 的短格式 (9 字节)：**

用于现代传输协议以及采用 ECIES（椭圆曲线集成加密方案）加密的 garlic 消息（I2P 的多消息捆绑机制）。

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### 首部字段详细信息

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### 实现说明

- 在通过 SSU（已弃用）传输时，仅包含类型和 4 字节的过期时间
- 在通过 NTCP2 或 SSU2 传输时，使用 9 字节的短格式
- 当 I2NP 消息被包含在其他消息（Data, TunnelData, TunnelGateway, GarlicClove）内时，需要标准的 16 字节头部
- 自 0.8.12 版本起，为提高效率，协议栈的某些环节禁用了校验和验证，但为兼容性仍需生成校验和
- 短格式的过期时间为无符号，将在 2106 年 2 月 7 日发生回绕。该日期之后，必须加上一个偏移量才能得到正确的时间
- 为了与旧版本兼容，即使可能不会进行验证，也应始终生成校验和

---

## 大小限制

Tunnel 消息将 I2NP 负载分片为固定大小的片段：
- **首个分片：** 约 956 字节
- **后续分片：** 每个约 996 字节
- **最大分片数：** 64（编号 0-63）
- **最大负载：** 约 61,200 字节（61.2 KB）

**计算：** 956 + (63 × 996) = 63,704 字节（理论最大值），由于开销，实际上限约为 61,200 字节。

### 历史背景

旧版传输协议具有更严格的帧大小限制: - NTCP: 16 KB 帧 - SSU: 约 32 KB 帧

NTCP2 支持约 65 KB 的帧，但 tunnel 的分片限制仍然适用。

### 应用数据注意事项

Garlic messages（Garlic 消息）可能会捆绑 LeaseSets、Session Tags（会话标签）或加密的 LeaseSet2 变体，从而减少用于有效载荷数据的空间。

**建议：** 为确保可靠投递，数据报应保持在 ≤ 10 KB。接近 61 KB 上限的消息可能会出现： - 因分片与重组导致的时延增加 - 更高的投递失败概率 - 更易受到流量分析

### 分片技术细节

每个 tunnel 消息固定为 1,024 字节 (1 KB)，并包含： - 4 字节的 tunnel ID - 16 字节的初始化向量 (IV) - 1,004 字节的加密数据

在加密数据中，tunnel 消息携带已分片的 I2NP 消息，并附带分片头，指示： - 分片编号 (0-63) - 是否为首个分片或后续分片 - 用于重组的整体消息 ID

第一个分片包含完整的 I2NP 消息头部（16 字节），留给负载的空间约为 956 字节。后续分片不包含该消息头部，从而每个分片可携带约 996 字节的负载。

---

## 常见消息类型

router 会根据消息类型和优先级来调度出站工作。优先级值越高，越先被处理。以下数值与当前 Java I2P 的默认设置一致（截至 API 版本 0.9.67）。

**注意：** 优先级与实现相关。若需权威的优先级取值，请参阅 Java I2P 源代码中的 `OutNetMessage` 类文档。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**保留的消息类型：** - 类型 0：保留 - 类型 4-9：保留用于将来使用 - 类型 12-17：保留用于将来使用 - 类型 224-254：保留用于实验性消息 - 类型 255：保留用于将来扩展

### 消息类型说明

- 控制平面消息 (DatabaseLookup、TunnelBuild 等) 通常通过**exploratory tunnels** (探索型 tunnel) 传输，而不是通过 client tunnels (客户端 tunnel)，从而可以独立设定优先级
- 优先级数值是近似的，并可能因实现而异
- TunnelBuild (21) 和 TunnelBuildReply (22) 已弃用，但仍然实现以兼容超长 tunnels (>8 跳)
- 标准的 tunnel 数据优先级为 400；高于该值的都视为紧急
- 当前网络中的典型 tunnel 长度为 3-4 跳，因此大多数 tunnel 构建使用 ShortTunnelBuild (218 字节记录) 或 VariableTunnelBuild (528 字节记录)

---

## 加密与消息封装

Routers 经常在传输前封装 I2NP 消息，从而形成多层加密。DeliveryStatus 消息可能是：1. 被封装在 GarlicMessage 中（加密） 2. 位于 DataMessage 内 3. 位于 TunnelData 消息中（再次加密）

每一跳只解密它的那一层；最终目的地才会揭示最内层的有效载荷。

### 加密算法

**遗留（正逐步淘汰）:** - ElGamal/AES + SessionTags（会话标签） - ElGamal-2048 用于非对称加密 - AES-256 用于对称加密 - 32 字节的 session tags

**当前（自 API 0.9.48 起为标准）：** - ECIES-X25519 + ChaCha20/Poly1305 AEAD，具备棘轮式前向保密 - Noise 协议框架（用于 destinations（目标端点） 的 Noise_IK_25519_ChaChaPoly_SHA256） - 8 字节的会话标签（由 32 字节缩减） - 用于前向保密的 Signal Double Ratchet 算法 - 在 API 版本 0.9.46（2020）引入 - 自 API 版本 0.9.58（2023）起对所有 routers 强制启用

**未来 (自 2.10.0 起为测试版):** - 使用 MLKEM (后量子密钥封装算法, ML-KEM-768) 与 X25519 组合的后量子混合密码学 - 结合经典与后量子密钥协商的混合棘轮 - 与 ECIES-X25519 向后兼容 - 将在 2.11.0 版本 (2025 年 12 月) 中成为默认

### ElGamal Router 弃用

**重要:** 自 API 版本 0.9.58（发行版 2.2.0，2023 年 3 月）起，ElGamal routers 已被弃用。由于当前建议用于查询的最低 floodfill（I2P 中负责 netDb 存储与分发的特殊节点）版本为 0.9.58，各实现无需为 ElGamal floodfill routers 实现加密。

**然而：** 为了向后兼容，仍然支持 ElGamal（埃尔加马尔）目的地。使用 ElGamal 加密的客户端仍可通过 ECIES（椭圆曲线集成加密方案） routers 进行通信。

### ECIES-X25519-AEAD-Ratchet 详细信息

这是 I2P 的加密规范中的加密类型 4。它提供：

**关键特性：** - 通过棘轮机制实现前向保密（每条消息使用新密钥） - 降低会话标签存储开销（8 字节 vs. 32 字节） - 多种会话类型（新建会话、已有会话、一次性） - 基于 Noise 协议 Noise_IK_25519_ChaChaPoly_SHA256 - 集成 Signal 的双棘轮算法

**密码学原语:** - X25519 用于 Diffie-Hellman 密钥交换 - ChaCha20 用于流加密 - Poly1305 用于消息认证 (AEAD) - SHA-256 用于哈希 - HKDF 用于密钥派生

**会话管理:** - 新会话: 使用静态 Destination（I2P 终端地址标识）密钥进行初始连接 - 现有会话: 后续消息使用会话标签 - 一次性会话: 单消息会话，以降低开销

有关完整的技术细节，请参见 [ECIES 规范](/docs/specs/ecies/) 和 [提案 144](/proposals/144-ecies-x25519-aead-ratchet/)。

---

## 通用结构

以下结构是多个 I2NP（I2P 网络协议）消息中的组成元素。它们并非完整的消息。

### BuildRequestRecord (构建请求记录) (ElGamal)

**已弃用。** 仅在当前网络中，当一个 tunnel 包含 ElGamal router 时才会使用。有关现代格式，请参见 [ECIES Tunnel Creation](/docs/specs/implementation/)。

**用途：** 一组多条记录中的一条，用于请求在 tunnel 中创建一跳。

**格式：**

使用 ElGamal 和 AES 加密（总计 528 字节）:

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamal 加密结构（528 字节）：

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
明文结构（加密前为 222 字节）:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**注意：** - ElGamal-2048 加密会生成一个 514 字节的块，但会移除两个填充字节（位于位置 0 和 257），最终得到 512 字节 - 字段细节见 [Tunnel 创建规范](/docs/specs/implementation/) - 源代码：`net.i2p.data.i2np.BuildRequestRecord` - 常量：`EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord（构建请求记录） (ECIES-X25519 长格式)

适用于 ECIES-X25519 router（基于 X25519 的 ECIES 加密方案），在 API 版本 0.9.48 中引入。使用 528 字节，以与混合 tunnel 保持向后兼容。

**格式：**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**总大小：** 528 字节（与 ElGamal 相同以保持兼容性）

有关明文结构和加密细节，请参阅 [ECIES Tunnel Creation](/docs/specs/implementation/)。

### BuildRequestRecord (ECIES-X25519 短格式)

仅适用于 ECIES-X25519 routers，自 API 版本 0.9.51（发行版 1.5.0）起。这是当前的标准格式。

**格式:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**总大小:** 218 字节（比 528 字节减少 59%）

**关键区别：** 短记录通过 HKDF（密钥派生函数）派生所有密钥，而不是在记录中显式包含它们。这包括： - 层密钥（用于 tunnel 加密） - IV（初始向量）密钥（用于 tunnel 加密） - 回复密钥（用于构建回复） - 回复 IV（用于构建回复）

所有密钥均通过 Noise 协议的 HKDF 机制，从 X25519 密钥交换得到的共享秘密中派生。

**优势：** - 4 条短记录可装入一个 tunnel 消息 (873 字节) - 采用 3 条消息完成的 tunnel 构建，而不是为每条记录分别发送消息 - 降低带宽占用和延迟 - 与长格式具有相同的安全属性

有关设计动机，请参见[提案 157](/proposals/157-new-tbm/)，完整规范请参见[ECIES Tunnel 创建](/docs/specs/implementation/)。

**源代码：** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - 常量：`ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### 构建响应记录 (ElGamal)

**已弃用。** 仅当 tunnel 包含 ElGamal router 时使用。

**用途：** 用于对构建请求进行响应的多条记录集合中的一条记录。

**格式：**

加密（528 字节，与 BuildRequestRecord 大小相同）:

```
bytes 0-527 :: AES-encrypted record
```
未加密的结构：

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**回复代码:** - `0` - 接受 - `30` - 拒绝 (带宽超出)

有关 reply 字段的详细信息，请参见 [Tunnel Creation Specification](/docs/specs/implementation/)。

### BuildResponseRecord（构建响应记录） (ECIES-X25519)

适用于 ECIES-X25519（基于 Curve25519 的 ECIES 加密套件） routers，API 版本 0.9.48+。与对应请求大小相同（长为 528，短为 218）。

**格式：**

长格式（528 字节）:

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
短格式（218 字节）：

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**明文结构（两种格式）：**

包含一个 Mapping 结构（I2P 的键值格式），其中包括： - 应答状态码（必需） - 可用带宽参数（"b"）（可选，添加于 API 0.9.65） - 用于未来扩展的其他可选参数

**回复状态码:** - `0` - 成功 - `30` - 拒绝: 带宽超限

有关完整规范，请参阅 [ECIES Tunnel Creation](/docs/specs/implementation/)。

### GarlicClove（蒜瓣消息单元） (ElGamal/AES)

**警告：** 这是用于 ElGamal 加密的大蒜消息中蒜瓣的格式。ECIES-AEAD-X25519-Ratchet 大蒜消息及其蒜瓣的格式有显著不同。有关现代格式，请参见 [ECIES 规范](/docs/specs/ecies/)。

**针对 routers（API 0.9.58+）已弃用，仍支持用于目的地。**

**格式：**

未加密：

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**注意：** - 蒜瓣绝不会被分片 - 当传递指令标志字节的第一位为0时，该蒜瓣不加密 - 当第一位为1时，该蒜瓣会被加密（功能尚未实现） - 最大长度由所有蒜瓣的总长度和GarlicMessage的最大长度共同决定 - 证书可能会用于借助HashCash来为路由"付费"（未来的可能性） - 实践中使用的消息：DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage可以包含GarlicMessage（嵌套的garlic），但在实践中并不使用

请参阅 [Garlic Routing（大蒜路由）](/docs/overview/garlic-routing/) 以获取概念性概览。

### GarlicClove (ECIES-X25519-AEAD-Ratchet)（I2P garlic encryption 消息中的“蒜瓣”单元）

适用于 ECIES-X25519 的 router 和目标，API 版本 0.9.46+。这是当前的标准格式。

**关键差异:** ECIES garlic 使用的是一种完全不同的结构，它基于 Noise 协议的块，而不是显式的 clove（子消息）结构。

**格式：**

ECIES garlic 消息（I2P 中将多条消息封装在一起的消息形式）包含一系列块：

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**块类型：** - `0` - Garlic Clove Block (包含一条 I2NP 消息) - `1` - 日期时间块 (时间戳) - `2` - 选项块 (传递选项) - `3` - 填充块 - `254` - 终止块 (未实现)

**蒜瓣块 (类型 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**与 ElGamal 格式的关键差异：** - 使用 4 字节过期时间（自 Unix 纪元以来的秒数），而非 8 字节的 Date - 无证书字段 - 封装在具有类型和长度的块结构中 - 整条消息使用 ChaCha20/Poly1305 AEAD 加密 - 通过 ratcheting（棘轮机制）进行会话管理

有关 Noise 协议框架和数据块结构的详尽信息，请参见 [ECIES 规范](/docs/specs/ecies/)。

### 蒜瓣投递指令

此格式同时用于 ElGamal 和 ECIES 的蒜瓣。它规定了如何投递所包含的消息。

**严重警告：** 本规范仅适用于 Garlic Cloves（蒜瓣）内部的投递指令。"投递指令" 也用于 Tunnel 消息中，但其格式有显著不同。有关 tunnel 投递指令，请参见 [Tunnel 消息规范](/docs/specs/implementation/)。切勿混淆这两种格式。

**格式：**

会话密钥和延迟未使用且从不出现，因此可能的三种长度为: - 1 字节 (LOCAL) - 33 字节 (ROUTER 和 DESTINATION) - 37 字节 (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**典型长度:** - 本地投递: 1 字节 (仅标志) - ROUTER / DESTINATION（目的地）投递: 33 字节 (标志 + 哈希) - TUNNEL 投递: 37 字节 (标志 + 哈希 + tunnel ID)

**投递类型描述：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**实现说明：** - 会话密钥加密尚未实现，标志位始终为 0 - 延迟尚未完全实现，标志位始终为 0 - 对于 TUNNEL 传递，哈希标识网关 router，tunnel ID 指定哪个入站 tunnel - 对于 DESTINATION（目的地标识）传递，哈希为该 Destination 公钥的 SHA-256 - 对于 ROUTER 传递，哈希为该 router 身份的 SHA-256

---

## I2NP 消息

适用于所有 I2NP 消息类型的完整消息规范。

### 消息类型概览

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**保留:** - 类型 0: 保留 - 类型 4-9: 保留供将来使用 - 类型 12-17: 保留供将来使用 - 类型 224-254: 保留用于实验性消息 - 类型 255: 保留用于未来扩展

---

### DatabaseStore（数据库存储，类型 1）

**用途：** 未经请求的数据库存储，或对成功的 DatabaseLookup（数据库查询）消息的响应。

**内容：** 未压缩的 LeaseSet、LeaseSet2、MetaLeaseSet 或 EncryptedLeaseSet，或压缩的 RouterInfo。

**使用回复令牌的格式：**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**回复令牌 == 0 时的格式：**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**注意：** - 出于安全考虑，当消息是通过某个 tunnel 接收时，将忽略回复字段 - 该 key 是 RouterIdentity（路由器标识）或 Destination（目标标识）的“真实”哈希，而不是 routing key（路由键） - 类型 3、5 和 7（LeaseSet2（LeaseSet 第二版）变体）在 0.9.38 版本（API 0.9.38）中添加。详情参见 [Proposal 123](/proposals/123-new-netdb-entries/) - 这些类型应仅发送给 API 版本为 0.9.38 或更高的 routers - 作为减少连接数的优化：如果类型为 LeaseSet，且包含回复令牌、回复 tunnel ID 非零，并且在该 LeaseSet 中存在与该回复网关/tunnelID 对匹配的租约，则接收方可以将回复重新路由到该 LeaseSet 中的任何其他租约 - **RouterInfo（路由器信息结构）gzip 格式：** 为了隐藏 router 的操作系统和实现，可通过将修改时间设为 0、OS 字节设为 0xFF，并按照 RFC 1952 将 XFL 设为 0x02（最大压缩，最慢算法），以匹配 Java router 实现。前 10 个字节：`1F 8B 08 00 00 00 00 00 02 FF`

**源代码：** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (用于 RouterInfo 结构) - `net.i2p.data.LeaseSet` (用于 LeaseSet 结构)

---

### DatabaseLookup（数据库查找，类型 2）

**目的：** 在网络数据库（netDb）中查找某项的请求。响应要么是 DatabaseStore，要么是 DatabaseSearchReply。

**格式：**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**回复加密模式：**

**注意:** 自 API 0.9.58 起，ElGamal routers 已弃用。由于现在推荐查询的 floodfill 最低版本为 0.9.58，各实现无需为 ElGamal floodfill routers 实现加密。ElGamal destinations（目标地址）仍然受支持。

标志位4（ECIESFlag）与第1位（encryptionFlag）配合使用，用于确定应答的加密模式：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**无加密（标志位 0,0）：**

reply_key、tags 和 reply_tags 不存在。

**ElG（ElGamal 加密算法）到 ElG（标志 0,1） - 已弃用：**

自 0.9.7 起受支持，自 0.9.58 起已弃用。

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES（椭圆曲线集成加密方案）到 ElG（ElGamal 加密）（标志位 1,0） - 已弃用：**

自 0.9.46 起受支持，自 0.9.58 起已弃用。

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
该回复是根据[ECIES Specification](/docs/specs/ecies/)定义的 ECIES（椭圆曲线集成加密方案）Existing Session（现有会话）消息：

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES（基于椭圆曲线的集成加密方案）到 ECIES (标志位 1,0) - 当前标准:**

ECIES（椭圆曲线集成加密方案）目标或 router 向 ECIES router 发送一次查找请求。自 0.9.49 起受支持。

与上面的 "ECIES to ElG" 格式相同。查找消息的加密在 [ECIES Routers](/docs/specs/ecies/#routers) 中定义。请求方是匿名的。

**ECIES（椭圆曲线集成加密方案）到 ECIES，使用 DH（Diffie-Hellman 密钥交换）（标志位 1,1） - 未来：**

尚未完全定义。请参阅 [Proposal 156](/proposals/156-ecies-routers/)。

**注意：** - 在 0.9.16 之前，键可能对应 RouterInfo（路由器信息）或 LeaseSet（相同的键空间，无标志可区分） - 只有当响应通过 tunnel 传输时，加密的回复才有用 - 如果实现了替代的 DHT 查找策略，包含的标签数量可能大于 1 - 查找键和排除键是"真实"的哈希，而不是路由键 - 自 0.9.38 起，可能返回类型 3、5 和 7（LeaseSet2 变体）。参见 [提案 123](/proposals/123-new-netdb-entries/) - **探索性查找说明：** 探索性查找被定义为返回一组接近该键的非 floodfill 哈希。然而，实现存在差异：Java 确实会为 RI 查找搜索键，并在存在时返回一个 DatabaseStore（数据库存储消息）；i2pd 则不会。因此，不建议对先前接收到的哈希使用探索性查找

**源代码:** - `net.i2p.data.i2np.DatabaseLookupMessage` - 加密: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply（数据库搜索回复） (类型 3)

**用途：** 对失败的 DatabaseLookup（数据库查找）消息的响应。

**内容：** 与所请求键最接近的 router 哈希列表。

**格式：**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**注意：** - 'from' 哈希未经认证，不能被信任 - 返回的对等节点哈希不一定比正在被查询的 router 更接近该键。对于常规查询的回复，这有助于发现新的 floodfills（泛洪填充节点）以及为了稳健性进行"反向"搜索（距离该键更远） - 对于探索查询，键通常是随机生成的。响应中的非-floodfill peer_hashes 可通过优化算法选择（例如，选择接近但不一定是最近的对等节点），以避免对整个本地数据库进行低效的排序。也可以使用缓存策略。这取决于具体实现 - **典型返回的哈希数量：** 3 - **建议返回的哈希数量上限：** 16 - 查询键、对等节点哈希以及 'from' 哈希都是"真实"的哈希，而不是 routing keys（路由键） - 如果 num 为 0，表示未找到更近的对等节点（死路）

**源代码：** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (传递状态) (类型 10)

**用途：** 一个简单的消息确认。通常由消息发起方创建，并与消息本身一起封装在一个Garlic Message（I2P中的“蒜瓣消息”，用于将多条子消息封装为一条）中，由目的端返回。

**内容：** 已投递消息的 ID 以及创建时间或到达时间。

**格式：**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**注意：** - 时间戳始终由创建者设置为当前时间。不过，代码中对此有多处用法，将来可能会新增 - 此消息还用作 SSU 中的会话建立确认。在这种情况下，消息 ID 设置为随机数，“到达时间”设置为当前的全网 ID，即 2（即 `0x0000000000000002`） - DeliveryStatus（I2NP 中用于确认投递状态的消息类型）通常被包装在 GarlicMessage（I2P 的“garlic”消息封装）中，通过 tunnel 发送，以在不暴露发送者的情况下提供确认 - 用于 tunnel 测试以测量时延和可靠性

**源代码：** - `net.i2p.data.i2np.DeliveryStatusMessage` - 用于：`net.i2p.router.tunnel.InboundEndpointProcessor` 进行 tunnel 测试

---

### GarlicMessage（类型 11）

**警告：** 这是用于使用 ElGamal 加密的 garlic 消息（I2P 中的聚合消息机制）的格式。ECIES-AEAD-X25519-Ratchet garlic 消息的格式有显著不同。有关现代格式，请参见 [ECIES Specification](/docs/specs/ecies/)。

**用途：** 用于封装多个加密的 I2NP 消息。

**内容：** 解密后，由一系列 Garlic Cloves（I2P 中“Garlic”消息的子单元，指单个封装消息）及附加数据组成，也称为 Clove Set。

**加密格式：**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**解密数据 (Clove Set，蒜瓣集合):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
**注意：** - 未加密时，数据包含一个或多个 Garlic Cloves（Garlic 路由中的“蒜瓣”单元） - AES 加密块会填充到至少 128 字节；加上 32 字节的 Session Tag，已加密消息的最小大小为 160 字节；再加上 4 字节长度字段，Garlic Message（Garlic 路由消息）的最小大小为 164 字节 - 实际最大长度小于 64 KB（对于 tunnel 消息，实际限制约为 61.2 KB） - 参见 [ElGamal/AES Specification](/docs/legacy/elgamal-aes/) 以了解加密细节 - 参见 [Garlic Routing](/docs/overview/garlic-routing/) 以获取概念性概览 - AES 加密块的 128 字节最小尺寸目前不可配置 - 在发送时，消息 ID 通常设置为随机数，在接收时似乎会被忽略 - 证书可能用于 HashCash 来“支付”路由（未来的可能性） - **ElGamal 加密结构：** 32 字节 Session Tag + 经过 ElGamal 加密的会话密钥 + 经过 AES 加密的负载

**对于 ECIES-X25519-AEAD-Ratchet 格式（当前的 router 标准）：**

参见 [ECIES 规范](/docs/specs/ecies/) 和 [提案 144](/proposals/144-ecies-x25519-aead-ratchet/)。

**源代码：** - `net.i2p.data.i2np.GarlicMessage` - 加密：`net.i2p.crypto.elgamal.ElGamalAESEngine`（已弃用） - 现代加密：`net.i2p.crypto.ECIES` 包

---

### TunnelData (类型 18)

**用途：** 从 tunnel 的网关或参与者发送到下一个参与者或端点的消息。数据为固定长度，包含经分片、成批打包、填充并加密的 I2NP 消息。

**格式：**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**有效载荷结构 (1024 字节):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**注意：** - 每一跳都会将 TunnelData 的 I2NP 消息 ID 设置为一个新的随机数 - tunnel 消息格式（在加密数据中）定义见 [Tunnel 消息规范](/docs/specs/implementation/) - 每一跳使用 AES-256 的 CBC 模式解密一层 - 每一跳都会使用解密后的数据更新 IV（初始化向量） - 总大小恰好为 1,028 字节（4 字节的 tunnelId + 1024 字节的数据） - 这是 tunnel 流量的基本单位 - TunnelData 消息承载分片后的 I2NP 消息（GarlicMessage, DatabaseStore 等）

**源代码：** - `net.i2p.data.i2np.TunnelDataMessage` - 常量：`TunnelDataMessage.DATA_LENGTH = 1024` - 处理：`net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (类型 19)

**用途:** 在 tunnel 的入站网关处封装另一条 I2NP 消息并送入该 tunnel。

**格式：**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**说明：** - 负载是带有标准16字节头部的 I2NP 消息 - 用于将消息从本地 router 注入到 tunnels 中 - 如有必要，网关会对所含消息进行分片 - 分片后，这些分片会被封装为 TunnelData（隧道数据）消息 - TunnelGateway（隧道网关）从不在网络上传输；它是在 tunnel 处理之前使用的内部消息类型

**源代码：** - `net.i2p.data.i2np.TunnelGatewayMessage` - 处理： `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage（数据消息，类型 20）

**用途：** 由 Garlic Messages（Garlic消息，I2P中用于将多条消息打包在一起的结构）和 Garlic Cloves（Clove子消息，打包中的单元）用于封装任意数据（通常为端到端加密的应用数据）。

**格式：**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**注意：** - 此消息不包含路由信息，且绝不会以"未封装"的形式发送 - 仅在 Garlic messages（Garlic 消息）内部使用 - 通常包含端到端加密的应用数据（HTTP、IRC、电子邮件等） - 数据通常是 ElGamal/AES 或 ECIES 加密的有效载荷 - 由于 tunnel 消息分片限制，最大实际长度约为 61.2 KB

**源代码：** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (类型 21)

**已弃用。** 请使用 VariableTunnelBuild（类型 23）或 ShortTunnelBuild（类型 25）。

**目的：** 8 跳的固定长度 tunnel 构建请求。

**格式：**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**注意事项：** - 自 0.9.48 起，可能包含 ECIES-X25519 BuildRequestRecords（构建请求记录）。详见 [ECIES Tunnel 创建](/docs/specs/implementation/) - 详见 [Tunnel 创建规范](/docs/specs/implementation/) - 此消息的 I2NP message ID 必须按照 Tunnel 创建规范进行设置 - 尽管在当前网络中很少见（已被 VariableTunnelBuild（可变长度 Tunnel 构建消息）取代），它仍可能用于非常长的 tunnels，且尚未被正式弃用 - 为了兼容性，Routers 仍必须实现此功能 - 固定的 8-记录格式缺乏灵活性，并会在较短的 tunnels 上浪费带宽

**源代码：** - `net.i2p.data.i2np.TunnelBuildMessage` - 常量：`TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply（类型 22）

**已弃用。** 使用 VariableTunnelBuildReply (类型 24) 或 OutboundTunnelBuildReply (类型 26)。

**用途:** 固定长度的 tunnel 构建回复，适用于 8 个跳点。

**格式：**

格式与 TunnelBuildMessage 相同，但使用 BuildResponseRecords 代替 BuildRequestRecords。

```
Total size: 8 × 528 = 4,224 bytes
```
**注意事项：** - 自 0.9.48 起，可能包含 ECIES-X25519 BuildResponseRecords（构建响应记录）。参见 [ECIES Tunnel 创建](/docs/specs/implementation/) - 详见 [Tunnel 创建规范](/docs/specs/implementation/) - 此消息的 I2NP 消息 ID 必须按照 Tunnel 创建规范进行设置 - 虽然在当前网络中很少见（已被 VariableTunnelBuildReply（可变 Tunnel 构建回复）取代），但它仍可能用于非常长的 tunnel，且尚未被正式弃用 - Routers 仍须实现以保持兼容性

**源代码:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (类型 23)

**目的：** 适用于 1-8 跳的可变长度的 tunnel 构建。同时支持 ElGamal 和 ECIES-X25519 routers。

**格式：**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**说明：** - 自 0.9.48 起，可能包含 ECIES-X25519 BuildRequestRecords。参见 [ECIES Tunnel Creation](/docs/specs/implementation/) - 在 router 版本 0.7.12 (2009 年) 中引入 - 不应发送给版本早于 0.7.12 的 tunnel 参与者 - 详情参见 [Tunnel Creation Specification](/docs/specs/implementation/) - I2NP message ID 必须根据 tunnel 创建规范进行设置 - **典型记录数：** 4 (用于 4 跳 tunnel) - **典型总大小：** 1 + (4 × 528) = 2,113 字节 - 这是适用于 ElGamal routers 的标准 tunnel 构建消息 - ECIES routers 通常改用 ShortTunnelBuild (type 25)

**源代码：** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (类型 24)

**目的：** 用于 1-8 跳的可变长度 tunnel 构建应答。支持 ElGamal 和 ECIES-X25519 routers。

**格式：**

与 VariableTunnelBuildMessage 格式相同，使用 BuildResponseRecords 而非 BuildRequestRecords。

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**注意：** - 自 0.9.48 起，可能包含 ECIES-X25519 BuildResponseRecords（构建响应记录）。参见 [ECIES Tunnel Creation](/docs/specs/implementation/) - 于 router 版本 0.7.12（2009 年）引入 - 不应发送给版本早于 0.7.12 的 tunnel 参与者 - 参见 [Tunnel Creation Specification](/docs/specs/implementation/) 获取详细信息 - 必须根据 Tunnel 创建规范设置 I2NP 消息 ID - **典型记录数：** 4 - **典型总大小：** 2,113 字节

**源代码：** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild（短 tunnel 构建，类型 25）

**用途：** 仅针对 ECIES-X25519 routers 的简短 tunnel 构建消息。于 API 版本 0.9.51（发布 1.5.0，2021 年 8 月）中引入。这是 ECIES（椭圆曲线集成加密方案） tunnel 构建的现行标准。

**格式:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```

**源代码：** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - 常量：`ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply（出站 tunnel 构建应答，类型 26）

**用途：** 从新的 tunnel 的出站端点发送给发起方。仅适用于 ECIES-X25519 routers。在 API 版本 0.9.51 中引入（发行版 1.5.0，2021 年 8 月）。

**格式：**

与 ShortTunnelBuildMessage 相同的格式，其中使用 ShortBuildResponseRecords 而不是 ShortBuildRequestRecords。

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**说明：** - 在 router 版本 0.9.51（发行版 1.5.0，2021 年 8 月）中引入 - 完整规范见 [ECIES Tunnel Creation](/docs/specs/implementation/) - **典型记录数量：** 4 - **典型总大小：** 873 字节 - 该回复由出站端点（OBEP）通过新创建的出站 tunnel 发送回 tunnel 创建者 - 用于确认所有跳点已接受该 tunnel 构建

**源代码:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## 参考资料

### 官方规范

- **[I2NP 规范](/docs/specs/i2np/)** - 完整的 I2NP 消息格式规范
- **[通用结构](/docs/specs/common-structures/)** - I2P 中使用的数据类型和结构
- **[Tunnel 创建](/docs/specs/implementation/)** - ElGamal 的 Tunnel 创建（已弃用）
- **[ECIES Tunnel 创建](/docs/specs/implementation/)** - ECIES-X25519 的 Tunnel 创建（当前）
- **[Tunnel 消息](/docs/specs/implementation/)** - Tunnel 消息格式与传递说明
- **[NTCP2 规范](/docs/specs/ntcp2/)** - TCP 传输协议
- **[SSU2 规范](/docs/specs/ssu2/)** - UDP 传输协议
- **[ECIES 规范](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet 加密
- **[密码学规范](/docs/specs/cryptography/)** - 底层密码学原语
- **[I2CP 规范](/docs/specs/i2cp/)** - 客户端协议规范
- **[数据报规范](/docs/api/datagrams/)** - Datagram2 和 Datagram3 格式

### 提案

- **[提案 123](/proposals/123-new-netdb-entries/)** - 新的 netDB 条目 (LeaseSet2、EncryptedLeaseSet、MetaLeaseSet)
- **[提案 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet 加密
- **[提案 154](/proposals/154-ecies-lookups/)** - 加密的数据库查询
- **[提案 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[提案 157](/proposals/157-new-tbm/)** - 更小的 tunnel 构建消息 (短格式)
- **[提案 159](/proposals/159-ssu2/)** - SSU2 传输
- **[提案 161](/zh/proposals/161-ri-dest-padding/)** - 可压缩填充
- **[提案 163](/proposals/163-datagram2/)** - Datagram2 和 Datagram3
- **[提案 167](/proposals/167-service-records/)** - LeaseSet 服务记录参数
- **[提案 168](/proposals/168-tunnel-bandwidth/)** - Tunnel 构建带宽参数
- **[提案 169](/proposals/169-pq-crypto/)** - 后量子混合密码学

### 文档

- **[Garlic Routing](/docs/overview/garlic-routing/)**（I2P 中的分层式消息打包与路由技术） - 分层消息捆绑
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - 已弃用的加密方案
- **[Tunnel 实现](/docs/specs/implementation/)** - 分片与处理
- **[网络数据库（netDb）](/docs/specs/common-structures/)** - 分布式哈希表
- **[NTCP2 传输](/docs/specs/ntcp2/)** - TCP 传输规范
- **[SSU2 传输](/docs/specs/ssu2/)** - UDP 传输规范
- **[技术简介](/docs/overview/tech-intro/)** - I2P 架构概览

### 源代码

- **[Java I2P 代码仓库](https://i2pgit.org/I2P_Developers/i2p.i2p)** - 官方 Java 实现
- **[GitHub 镜像](https://github.com/i2p/i2p.i2p)** - Java I2P 的 GitHub 镜像
- **[i2pd 代码仓库](https://github.com/PurpleI2P/i2pd)** - C++ 实现

### 关键源代码位置

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - I2NP 消息实现 - `core/java/src/net/i2p/crypto/` - 加密实现 - `router/java/src/net/i2p/router/tunnel/` - tunnel 处理 - `router/java/src/net/i2p/router/transport/` - 传输实现

**常量与数值：** - `I2NPMessage.MAX_SIZE = 65536` - I2NP 消息的最大大小 - `I2NPMessageImpl.HEADER_LENGTH = 16` - 标准头部大小 - `TunnelDataMessage.DATA_LENGTH = 1024` - Tunnel 消息负载 - `EncryptedBuildRecord.RECORD_SIZE = 528` - 长构建记录 - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - 短构建记录 - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - 每次构建的最大记录数

---

## 附录 A：网络统计与当前状态

### 网络组成（截至 2025 年 10 月）

- **routers 总数：** 大约 60,000-70,000（有波动）
- **Floodfill routers:** 大约 500-700 个活跃
- **加密类型：**
  - ECIES-X25519：>95% 的 routers
  - ElGamal：<5% 的 routers（已弃用，仅遗留用途）
- **传输采用情况：**
  - SSU2：>60% 为主要传输
  - NTCP2：~40% 为主要传输
  - 旧版传输（SSU1、NTCP）：0%（已移除）
- **签名类型：**
  - EdDSA (Ed25519)：绝大多数
  - ECDSA：占比较小
  - RSA：不允许（已移除）

### Router 的最低要求

- **API 版本：** 0.9.16+ (用于与网络保持 EdDSA 兼容性)
- **建议的最低版本：** API 0.9.51+ (ECIES 短 tunnel 构建)
- **适用于 floodfills 的当前最低版本：** API 0.9.58+ (ElGamal router 弃用)
- **即将生效的要求：** Java 17+ (自 2.11.0 版本起，2025 年 12 月)

### 带宽要求

- **最低要求：** 128 KBytes/sec（N 标志或更高），用于 floodfill
- **推荐：** 256 KBytes/sec（O 标志）或更高
- **Floodfill 要求：**
  - 最低 128 KB/sec 带宽
  - 稳定的在线率（建议 >95%）
  - 低延迟（与对等节点 <500ms）
  - 通过健康检查（队列时间、作业延迟）

### Tunnel 统计信息

- **典型 tunnel 长度:** 3-4 跳
- **最大 tunnel 长度:** 8 跳 (理论值，极少使用)
- **典型 tunnel 生命周期:** 10 分钟
- **tunnel 构建成功率:** >85%，适用于连接良好的 routers
- **tunnel 构建消息格式:**
  - ECIES routers: ShortTunnelBuild (218 字节记录)
  - 混合 tunnels: VariableTunnelBuild (528 字节记录)

### 性能指标

- **Tunnel 构建时间:** 1-3 秒 (典型)
- **端到端延迟:** 0.5-2 秒 (典型，总计 6-8 跳)
- **吞吐量:** 受 tunnel 带宽限制 (通常每个 tunnel 为 10-50 KB/sec)
- **最大数据报大小:** 建议 10 KB (理论最大值 61.2 KB)

---

## 附录 B：已弃用和已移除的功能

### 已完全移除（不再受支持）

- **NTCP 传输协议** - 已在 0.9.50 版本中移除（2021 年 5 月）
- **SSU v1 传输协议** - 已在 Java I2P 的 2.4.0 版本中移除（2023 年 12 月）
- **SSU v1 传输协议** - 已在 i2pd 的 2.44.0 版本中移除（2022 年 11 月）
- **RSA 签名类型** - 自 API 0.9.28 起不再允许

### 已弃用（受支持但不建议使用）

- **ElGamal routers** - 自 API 0.9.58 (2023 年 3 月) 起已弃用
  - 仍支持 ElGamal 目的地，以保持向后兼容性
  - 新的 routers 应仅使用 ECIES-X25519
- **TunnelBuild (类型 21)** - 已弃用，改为使用 VariableTunnelBuild 和 ShortTunnelBuild
  - 仍对超长 tunnels (>8 跳) 提供实现
- **TunnelBuildReply (类型 22)** - 已弃用，改为使用 VariableTunnelBuildReply 和 OutboundTunnelBuildReply
- **ElGamal/AES 加密** - 已弃用，改为使用 ECIES-X25519-AEAD-Ratchet
  - 仍用于旧版目的地
- **Long ECIES BuildRequestRecords (528 字节)** - 已弃用，改为使用短格式 (218 字节)
  - 仍用于包含 ElGamal 跳点的混合 tunnels

### 旧版支持时间线

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## 附录 C：未来发展

### 后量子密码学

**状态：** 自 2.10.0 版本（2025 年 9 月）起为 Beta，将在 2.11.0（2025 年 12 月）中成为默认

**实现:** - 混合方案，结合传统的 X25519 与后量子的 MLKEM (ML-KEM-768) - 与现有的 ECIES-X25519 基础设施保持向后兼容 - 使用 Signal Double Ratchet (Signal 双棘轮)，并同时采用传统和 PQ (后量子) 密钥材料 - 详情参见 [Proposal 169](/proposals/169-pq-crypto/)

**迁移路径：** 1. 版本 2.10.0 (2025 年 9 月)：作为测试版选项提供 2. 版本 2.11.0 (2025 年 12 月)：默认启用 3. 未来版本：最终将成为必需

### 计划中的功能

- **IPv6 改进** - 更好的 IPv6 支持和过渡机制
- **每个 tunnel 限速** - 针对每个 tunnel 的细粒度带宽控制
- **增强的度量指标** - 更好的性能监控和诊断
- **协议优化** - 降低开销并提升效率
- **改进的 floodfill 选择** - 更好的网络数据库分布

### 研究领域

- **Tunnel 长度优化** - 基于威胁模型的动态 tunnel 长度
- **高级填充** - 提升对流量分析的抵抗能力
- **新的加密方案** - 为量子计算威胁做准备
- **拥塞控制** - 更好地处理网络负载
- **移动端支持** - 针对移动设备和网络的优化

---

## 附录 D：实现指南

### 面向新实现

**最低要求：** 1. 支持 API 版本 0.9.51+ 的特性 2. 实现 ECIES-X25519-AEAD-Ratchet 加密 3. 支持 NTCP2 和 SSU2 传输协议 4. 实现 ShortTunnelBuild 消息（218 字节记录） 5. 支持 LeaseSet2 变体（类型 3、5、7） 6. 使用 EdDSA 签名（Ed25519）

**推荐：** 1. 支持后量子混合密码学 (自 2.11.0 起) 2. 实现每个 tunnel(隧道) 的带宽参数 3. 支持 Datagram2 和 Datagram3 格式(数据报) 4. 在 LeaseSets(租约集) 中实现服务记录选项 5. 遵循 /docs/specs/ 上的官方规范

**非必需：** 1. ElGamal router 支持（已弃用） 2. 旧版传输支持（SSU1, NTCP） 3. Long ECIES BuildRequestRecords（构建请求记录）（用于纯 ECIES tunnels 的 528 字节） 4. TunnelBuild/TunnelBuildReply 消息（使用 Variable 或 Short 变体）

### 测试与验证

**协议符合性:** 1. 测试与官方 Java I2P router 的互操作性 2. 测试与 i2pd C++ router 的互操作性 3. 根据规范验证消息格式 4. 测试 tunnel 建立/拆除循环 5. 使用测试向量验证加密/解密

**性能测试：** 1. 测量 tunnel 构建成功率（应 >85%） 2. 使用不同的 tunnel 长度进行测试（2-8 跳） 3. 验证分片与重组 4. 在负载下进行测试（多个并发的 tunnels） 5. 测量端到端延迟

**安全测试：** 1. 验证加密实现 (使用测试向量) 2. 测试重放攻击防护 3. 验证消息过期处理 4. 针对格式错误的消息进行测试 5. 验证随机数生成的正确性

### 常见实现陷阱

1. **令人困惑的投递指令格式** - garlic clove（蒜瓣子消息）与 tunnel 消息
2. **错误的密钥派生** - 短构建记录的 HKDF 用法
3. **消息 ID 处理** - 在 tunnel 构建中未正确设置
4. **分片问题** - 未遵守 61.2 KB 的实际限制
5. **字节序错误** - Java 对所有整数使用大端序
6. **过期处理** - 短格式将在 2106 年 2 月 7 日回绕
7. **校验和生成** - 即使不验证也仍然需要
