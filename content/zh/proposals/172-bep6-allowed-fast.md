---
title: "快速扩展（BEP 6）允许使用目标哈希对等身份进行快速连接"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "草稿"
toc: true
---

## 概述

BEP 6（快速扩展）包含五个功能：**拥有全部 / 无任何内容**、**拒绝请求**、**建议** 和 **允许快速**。其线缆协议——协商位、消息ID和阻塞语义——与传输方式无关，可直接在I2P流式传输上运行。BEP 6 中唯一无法直接映射到 I2P 的部分是 **允许快速集合的生成**，因为该机制是基于对等方的 IPv4 地址定义的。而 I2P 对等方没有 IP 地址，它们通过 32 字节的目的地哈希来标识。

该提案标准化了一种I2P原生的“允许快速集”（Allowed Fast set）生成方式，使得所有I2P种子客户端在相同对等节点和种子情况下生成完全相同的允许快速集，从而使该功能在不同实现之间具有可用性且可验证。

## 动机

新的对等节点在获得前几个数据块后，BitTorrent 的“以牙还牙”机制才能逐步加速。在 I2P 网络上，这个加速过程比在明网（clearnet）上更慢：连接建立和数据块传输需要经过多个高延迟的跳转隧道，因此从建立连接到第一次互惠性“解阻塞”（unchoke）之间的时间窗口更长。允许的快速开始（Allowed Fast）机制直接针对这一时间窗口——即使在被阻塞（choked）状态下，初始节点仍被允许获取少量数据块，从而立即获得数据，并能更早开始回馈。

参考 BEP 6 使用对等方的 IPv4 地址来计算允许的快速集合，以确保*发送方*可以选择对*接收方*唯一的数据块（即一个用户即使拥有多个 IP 也无法获取多个集合）。在 I2P 上，对等方的目标哈希起到相同的绑定作用，并且在每条连接的两端都可获取，这使得该集合具有确定性且可本地验证——这是基于 IP 的方案无法提供的特性。

## 对 BEP 6 的修改

快速扩展协商和全部四种消息类型均未经更改地采用：

- 协商：最后一个保留字节的第三最低有效位，`reserved[7] |= 0x04`，两端均需设置
- 拥有全部 `<len=0x0001><op=0x0E>`，未拥有任何 `<len=0x0001><op=0x0F>`
- 建议片段 `<len=0x0005><op=0x0D><index>`
- 拒绝请求 `<len=0x000D><op=0x10><index><begin><length>`
- 允许快速请求 `<len=0x0005><op=0x11><index>`
- 每个请求都会产生一个且仅一个响应（数据块或拒绝）；拥塞控制不再隐式拒绝待处理请求

唯一的偏差在于允许的快速集合生成中，使用对等方目标哈希的字节替换了IP地址的字节。

### 偏差：使用哈希字节代替掩码 IP

参考 BEP 6，步骤 (1)：

```
x = 0xFFFFFF00 & ip
```
这会取对等方IPv4地址的三个字节，并将第四个字节置零。这是一种子网启发式方法：能够在同一个/24子网内获取多个IP的用户，不应获得多个允许的快速集合。

我们的 I2P 版本使用对等方 32 字节目标哈希的前四个字节来替换此值：

```
x = first 4 bytes of peer destination hash
```
与参考实现的区别：

> “那是IP的3个字节，后跟一个零。接着是你哈希值的4个字节。这与BEP 6不同，因为没有IP，并且不会将第4个字节置零。”

I2P 连接的两端已经知道对等方的目的地哈希（即建立连接时所使用的地址），因此无需额外的交换、NAT 发现或外部 IP 检测——而这些机制在 I2P 上本就不存在。

### 允许的快速生成算法

设 `hash` 为接收端对等体的 32 字节目标哈希，`infohash` 为 torrent 的 20 字节 infohash，`sz` 为 torrent 中的分片数量，`k` 为允许快速集（allowed fast set）中最终的分片数量（如 BEP 6 中所述为 10），`a` 为输出集：

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
备注：

- 目标哈希的4个字节替换了3个被掩码的IP字节。所有四个字节都携带哈希熵，没有字节被置零。
- 与BEP 6中一样，SHA1链生成一个长的伪随机序列，并划分为块索引；`k = 10` 与参考默认值一致。
- Allowed Fast消息仅为建议性质：接收方绝不能将其解释为发送方拥有该数据块，而仅表示发送方在被阻断时仍会提供该数据块。

## 优势

| 领域             | 优势                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 启动延迟         | 新的对等节点在被阻塞时即可拉取第一块数据，缩短了“以上传换下载”的启动过程，这在多跳 I2P 隧道中尤其有效，因为传统方式会更慢                                                                       |
| 确定性           | 该集合完全由目标哈希（destination hash）和 infohash 决定，因此任何实现都会计算出相同的集合 —— 与基于 IP 的 BEP 6 不同，在后者中，发送方对接收方 IP 地址的视图可能因 NAT 而不同                     |
| 可验证性         | 接收方对等节点知道自己的目标哈希，可本地重新计算并验证该集合，从而检测到行为异常的发送方                                                                                                       |
| 无需 IP 机制     | 无需 NAT 穿透、外部 IP 发现或子网启发式方法 —— 这些在 I2P 上均不可能或无意义                                                                                                                 |
| 身份绑定         | 每个目标地址仅允许一个快速集合。拥有多个目标地址的用户将为每个地址各获得一个集合 —— 这与明网中 IP 掩码提供的防作弊特性相同                                                                       |
| 隐私             | 在整个计算过程中，从不传输或暗示任何 IP 地址                                                                                                                                                 |
| 带宽             | 对大型种子，“全有 / 全无”（Have All / Have None）取代了完整的位字段；Reject 消息消除了冗余的重新请求                                                                                          |
## 实现考虑

- **对等体身份**：通过对等流连接（会话的目标）获取对等体的目标哈希，该值在连接两端使用相同。对于出站连接，使用你所连接的目标；对于入站连接，使用连接来源的目标。
- **协商**：在握手过程中发送 `reserved[7] |= 0x04`；仅当对等体的握手也设置了该位时，才发送 Fast Extension 消息；如果对等体在未协商的情况下发送 Fast Extension 消息，则关闭连接。
- **Have All / Have None**：在握手完成后立即发送 bitfield / Have All / Have None 中的**唯一一个**。种子端发送 Have All，下载初期尚未拥有任何分片时发送 Have None。
- **Allowed Fast 发送端**：仅宣告你实际拥有的分片；接收方可在此被阻塞（choked）状态下请求这些分片。应限制所“提供”的集合（例如，根据 BEP 6 建议，当某个对等体已持有超过 `k` 个分片时，拒绝其 allowed-fast 请求）。
- **Allowed Fast 接收端**：存储收到的集合；允许在被阻塞状态下请求这些分片；可选地，可通过你自己的目标哈希和 infohash 重新计算该集合，以验证其正确性，并忽略不在计算结果中的分片。
- **Reject**：每个请求**必须**收到且仅收到一个响应；当处于阻塞状态时，应显式拒绝所有不在 allowed fast 集合中的请求，而非静默忽略对等体。
- **集合大小**：为兼容性使用 `k = 10`；在高负载下，对等体可自由选择更小的 `k`，但两端都应仅宣告自己实际能提供的部分。
- **分片边界**：`index = y % sz` 必须使用 torrent 的总分片数 `sz`；忽略所有大于等于 `sz` 的索引（防御性处理），因为哈希链并未按分片范围进行截断。
- **向后兼容**：未协商 fast 位的客户端将完全看不到这些消息；无需其他协议更改。

## 参考实现

该算法小巧且自包含——用任何语言编写都只有几十行代码。下面三个示例在相同输入（`hash[0:4] ++ infohash`、SHA1 链、`y % sz`，上限 `k = 10`）下计算出完全相同的结果集。

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## 兼容性

- **线缆兼容**：协商位和消息格式与 clearnet BEP 6 字节级一致；只有集合生成的输入不同。
- **跨网络不互通**：I2P 客户端和 clearnet 客户端本来也无法互相连接；这种差异仅影响对等体身份字节，从不影响线缆格式。
- **在 I2P 内部**：任何实现此提议的客户端都能计算出相同的允许快速集合，并可交替地提供和验证它们。忽略 Allowed Fast 的客户端仅将其视为无操作建议，仅损失启动时的优势。

## 待解决的问题

1. 集合大小 `k` 应该固定为 10，还是根据负载自适应调整（例如在请求负载较高时减少）？BEP 6 允许后者。
2. 接收方是否应针对自身的目标哈希值验证该集合，并丢弃不匹配的索引（以防御有缺陷或恶意的发送方）？建议为“是”。
3. 应选择如图所示的前 4 字节 *前缀*（字节 0-3），还是最后 4 字节 —— 任意固定的 4 字节窗口都能提供相同的性质；而使用前缀可保持参考代码中的字节顺序自然（`hash[0:4]`）。

## 现有技术

- 参考：[BEP 6 快速扩展](https://www.bittorrent.org/beps/bep_0006.html)
- I2PSnark 参考实现：`apps/i2psnark/java/src/org/klomp/snark/PeerState.java` 中的 `PeerState.sendAllowedFast()` / `generateAllowedFastSet()`（自 0.9.71+ 版本起）
- 与 BEP 40（标准对等节点优先级）和 BEP 21（部分种子）协同工作，I2PSnark 已支持这两项扩展
