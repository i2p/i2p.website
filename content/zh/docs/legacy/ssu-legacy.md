---
title: "SSU 传输 (已弃用)"
description: "在 SSU2 之前使用的最初 UDP 传输"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **已弃用：** SSU (Secure Semi-Reliable UDP，安全的半可靠 UDP) 已被 [SSU2](/docs/specs/ssu2/) 取代。Java I2P 在 2.4.0 版（API 0.9.61）中移除了 SSU，i2pd 在 2.44.0（API 0.9.56）中也将其移除。本文档仅保留作历史参考。

## 亮点

- UDP 传输，提供加密、认证的 I2NP 消息点对点投递。
- 依赖 2048 位 Diffie–Hellman 握手（与 ElGamal 使用相同的素数）。
- 每个数据报携带一个 16 字节的 HMAC-MD5（非标准的截断变体）+ 16 字节的 IV，随后是经 AES-256-CBC 加密的有效载荷。
- 重放防护与会话状态在加密的有效载荷内进行跟踪。

## 消息头

```
[16-byte MAC][16-byte IV][encrypted payload]
```
使用的 MAC 计算：`HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))`，使用 32 字节的 MAC 密钥。负载长度以大端序 16 位表示，并在 MAC 计算中附加。协议版本默认为 `0`；netId 默认为 `2`（主网络）。

## 会话与 MAC 密钥

派生自 DH 共享秘密：

1. 将共享值转换为大端序字节数组（如果最高位被置位，则在前面加上 `0x00`）。
2. 会话密钥：前 32 个字节（如果更短则用零填充）。
3. MAC 密钥：第 33–64 个字节；如果不足，则改用共享值的 SHA-256 哈希。

## 状态

router 不再通告 SSU 地址。客户端应迁移至 SSU2 或 NTCP2 传输协议。历史实现可在较早的发行版中找到：

- 2.4.0 之前的 Java 源代码，位于 `router/transport/udp` 下
- 2.44.0 之前的 i2pd 源代码

有关当前 UDP 传输行为，请参阅 [SSU2 规范](/docs/specs/ssu2/)。
