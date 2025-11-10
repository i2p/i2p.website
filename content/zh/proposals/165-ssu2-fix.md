---
title: "I2P 提议 #165: SSU2 修复"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "开放"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

由 weko, orignal, the Anonymous 和 zzz 提议。


### 概述

本文档建议对 SSU2 进行更改，以应对利用 SSU2 漏洞攻击 I2P 的问题。主要目标是提升安全性，防止分布式拒绝服务 (DDoS) 攻击和去匿名化尝试。

### 威胁模型

攻击者创建新的假 RIs（路由器不存在）：是普通 RI，但他使用真实 Bob 路由器的地址、端口、s 和 i 密钥，然后攻击整个网络。当我们试图连接到这个（我们认为是真实的）路由器时，我们作为 Alice 可以连接到这个地址，但我们无法确定它是否用真实的 Bob 的 RI 进行了操作。这是可能的，并被用于分布式拒绝服务攻击（创建大量这样的 RIs 并攻击网络），这也可以通过诬陷好的路由器而不诬陷攻击者的路由器来更容易进行去匿名攻击，如果我们禁止具有许多 RIs 的 IP（而不是更好地分配隧道构建给这些 RIs 作为一个路由器）。

### 可能的修复

#### 1. 在支持旧路由器的情况下修复

.. _overview-1:

概述
^^^^^^^^

支持与旧路由器的 SSU2 连接的解决方法。

行为
^^^^^^^^^

Bob 的路由器配置文件应该有一个“已验证”标志，默认情况下对所有新路由器为 false（尚无配置文件）。当“已验证”标志为 false 时，我们从不与 Bob 使用 SSU2 作为 Alice 进行连接——我们无法确定 RI 的真实性。如果 Bob 使用 NTCP2 或 SSU2 连接到我们（Alice）或我们（Alice）曾使用 NTCP2 连接到 Bob（在这些情况下我们可以验证 Bob 的 RouterIdent）——标志设置为 true。

问题
^^^^^^^^

因此，存在使用假 SSU2-only RI 进行攻击的问题：我们无法自己验证它并被迫等待真实路由器连接我们。

#### 2. 在连接创建期间验证 RouterIdent

.. _overview-2:

概述
^^^^^^^^

为 SessionRequest 和 SessionCreated 添加“RouterIdent”块。

RouterIdent 块的可能格式
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 字节标志，32 字节 RouterIdent。Flag_0：0 表示接收者的 RouterIdent；1 表示发送者的 RouterIdent。

行为
^^^^^^^^

Alice （应(1)，可以(2)）在负载中发送 RouterIdent 块 Flag_0 = 0 和 Bob 的 RouterIdent。Bob （应(3)，可以(4)）检查是否是他的 RouterIdent，如果不是：终止会话并说明“错误的 RouterIdent”原因，如果是他的 RouterIdent：发送带有 1 的 Flag_0 和 Bob 的 RouterIdent 的 RI 块。

使用 (1) 时，Bob 不支持旧路由器。使用 (2) 时，Bob 支持旧路由器，但可能成为试图使用假 RIs 建立连接的路由器的 DDoS 攻击目标。使用 (3) 时，Alice 不支持旧路由器。使用 (4) 时，Alice 支持旧路由器，并使用混合方案：旧路由器使用修复 1，新路由器使用修复 2。如果 RI 显示新版本，但在连接中我们没有接收到 RouterIdent 块——终止并移除 RI。

.. _problems-1:

问题
^^^^^^^^

攻击者可以将他的假路由器伪装为旧版本，使用 (4) 时，我们无论如何都在等待“已验证”，如修复 1。

备注
^^^^^

可用 4 字节 siphash-of-the-hash，一些 HKDF 或其他东西来代替 32 字节 RouterIdent，这应当足够。

#### 3. Bob 设置 i = RouterIdent

.. _overview-3:

概述
^^^^^^^^

Bob 使用他的 RouterIdent 作为 i 密钥。

.. _behavior-1:

行为
^^^^^^^^

Bob （应(1)，可以(2)）使用他自己的 RouterIdent 作为 SSU2 的 i 密钥。

Alice 使用 (1) 时仅在 i = Bob 的 RouterIdent 时连接。Alice 使用 (2) 时使用混合方案（修复 3 和 1）：如果 i = Bob 的 RouterIdent，我们可以建立连接，否则我们应首先验证它（见修复 1）。

使用 (1) 时，Alice 不支持旧路由器。使用 (2) 时，Alice 支持旧路由器。

.. _problems-2:

问题
^^^^^^^^

攻击者可以将他的假路由器伪装为旧版本，使用 (2) 时我们无论如何都在等待“已验证”，如修复 1。

.. _notes-1:

备注
^^^^^

为节省 RI 大小，最好添加处理 i 密钥未指定的情况。如果指定了，则 i = RouterIdent。在这种情况下，Bob 不支持旧路由器。

#### 4. 为 SessionRequest 的 KDF 添加一个 MixHash

.. _overview-4:

概述
^^^^^^^^

将 MixHash(Bob 的标识哈希)添加到“SessionRequest”消息的 NOISE 状态，例如：
h = SHA256 (h || Bob 的标识哈希)。
它必须是用作 ENCRYPT 或 DECRYPT 的 ad 的最后一个 MixHash。
必须引入附加的 SSU2 标头标志“验证 Bob 的标识”= 0x02。

.. _behavior-4:

行为
^^^^^^^^

- Alice 使用来自 Bob 的 RouterInfo 的 Bob 标识哈希添加 MixHash，并将其用作 ENCRYPT 的 ad，并设置“验证 Bob 的标识”标志。
- Bob 检查“验证 Bob 的标识”标志，并使用自有标识哈希添加 MixHash 并用作 DECRYPT 的 ad。如果 AEAD/Chacha20/Poly1305 失败，Bob 则关闭会话。

与旧路由器的兼容性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice 必须检查 Bob 的路由器版本，如果其满足支持此提议的最低版本，则添加此 MixHash 并设置“验证 Bob 的标识”标志。如果路由器较旧，Alice 不添加 MixHash 并不设置“验证 Bob 的标识”标志。
- Bob 检查“验证 Bob 的标识”标志并在其被设置时添加此 MixHash。旧路由器不设置此标志，并且不应添加此 MixHash。

.. _problems-4:

问题
^^^^^^^^

- 攻击者可以将伪造的路由器声明为旧版本。在某些情况下，旧路由器应该谨慎使用，并在通过其他方式验证后使用。

### 向后兼容性

在修复中进行了描述。

### 当前状态

i2pd: 修复 1。
