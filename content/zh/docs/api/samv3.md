---
title: "SAMv3"
description: "用于非 Java I2P 应用程序的简易匿名消息协议"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM 是一种用于与 I2P 交互的简单客户端协议。对于非 Java 应用程序连接到 I2P 网络，推荐使用 SAM 协议，并且多种路由器实现均支持该协议。Java 应用程序应直接使用流式 API 或 I2CP API。

SAM 版本 3 在 I2P 0.7.3 版本（2009 年 5 月）中引入，是一个稳定且受支持的接口。3.1 版本同样稳定，并支持签名类型选项，强烈推荐使用。更新的 3.x 版本支持更多高级功能。请注意，i2pd 目前不支持大多数 3.2 和 3.3 版本的功能。

替代方案：[SOCKS](/docs/api/socks)、[流式传输](/docs/api/streaming)、[I2CP](/docs/protocol/i2cp)、[BOB（已弃用）](/docs/api/bob)。已弃用的版本：[SAM V1](/docs/api/sam)、[SAM V2](/docs/api/samv2)。

## 已知的 SAM 库

警告：其中一些项目可能非常陈旧或不再受支持。除非下方另有说明，否则这些项目均未经 I2P 项目测试、审查或维护。请自行调研。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## 快速入门

要实现一个仅支持 TCP 的基本点对点应用程序，客户端必须支持以下命令：

- `HELLO VERSION MIN=3.1 MAX=3.1` - 所有后续操作都需要此命令
- `DEST GENERATE SIGNATURE_TYPE=7` - 用于生成我们的私钥和目标地址（destination）
- `NAMING LOOKUP NAME=...` - 将 .i2p 地址解析为 destination
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - STREAM CONNECT 和 STREAM ACCEPT 所必需
- `STREAM CONNECT ID=... DESTINATION=...` - 用于发起出站连接
- `STREAM ACCEPT ID=...` - 用于接受入站连接

## 开发者通用指南

### 应用程序设计

SAM 会话（或在 I2P 内部，隧道池或一组隧道）设计为长期存在。大多数应用程序只需要一个在启动时创建、退出时关闭的会话。I2P 与 Tor 不同，在 Tor 中，电路可能会被快速创建和丢弃。在设计应用程序以使用一个或两个以上的并发会话，或快速创建和丢弃会话之前，请仔细考虑并咨询 I2P 开发人员。大多数威胁模型并不需要为每个连接使用唯一的会话。

此外，请确保您的应用程序设置（以及向用户提供的关于路由器设置的指导，或如果您捆绑了路由器时的默认设置）将使您的用户向网络贡献的资源多于其消耗的资源。I2P 是一个点对点网络，如果某个流行的应用程序导致网络长期拥塞，网络将无法持续运行。

### 兼容性与测试

Java I2P 和 i2pd 路由器的实现是独立的，在行为、功能支持和默认设置方面存在一些细微差异。请使用这两个路由器的最新版本测试您的应用程序。

i2pd 的 SAM 功能默认已启用；而 Java I2P 的 SAM 功能则未启用。请向用户提供在 Java I2P 中启用 SAM 的说明（通过路由器控制台中的 /configclients 页面），和/或在初次连接失败时向用户提供清晰的错误提示，例如：“请确保 I2P 正在运行，并且 SAM 接口已启用”。

Java I2P 和 i2pd 路由器在隧道数量的默认设置上有所不同。Java I2P 的默认值是 2，而 i2pd 的默认值是 5。对于大多数低至中等带宽和低至中等连接数的场景，2 或 3 个隧道已足够。为了在 Java I2P 和 i2pd 路由器上获得一致的性能，请在 SESSION CREATE 消息中明确指定隧道数量。详见下文。

有关指导开发人员确保您的应用程序仅使用所需资源的更多信息，请参阅[将 I2P 嵌入您的应用程序的指南](/docs/applications/embedding)。

### 签名和加密类型

I2P 支持多种签名和加密类型。出于向后兼容性的考虑，SAM 默认使用旧的且效率较低的类型，因此所有客户端都应指定更新的类型。

签名类型在 DEST GENERATE 和 SESSION CREATE（用于临时密钥）命令中指定。所有客户端都应设置 `SIGNATURE_TYPE=7`（Ed25519）。

加密类型在 SESSION CREATE 命令中指定。允许多种加密类型。客户端应设置 `i2cp.leaseSetEncType=4`（仅用于 ECIES-X25519）或 `i2cp.leaseSetEncType=6,4`（用于支持 API 0.9.67 或更高版本的路由器，启用 MLKEM-768 和 ECIES-X25519）。

## 版本3的变更

### 版本 3.0 的变更

版本 3.0 在 I2P 0.7.3 版本中引入。SAM v2 提供了一种方式，可让多个套接字在同一个 I2P 目标地址上并行工作，即客户端在向一个套接字发送数据时，无需等待其成功传输完毕即可向另一个套接字发送数据。但所有数据都通过同一个客户端到 SAM 的套接字传输，这给客户端的管理带来了较大复杂性。

SAM v3 以不同的方式管理套接字：每个 *I2P 套接字* 对应一个唯一的客户端到 SAM 的套接字，这样处理起来要简单得多。这与 [BOB](/docs/api/bob) 类似。

SAM v3 还提供了一个 UDP 端口，用于通过 I2P 发送数据报，并能将来自 I2P 的数据报转发回客户端的数据报服务器。

### 版本 3.1 的变更

版本 3.1 在 Java I2P 0.9.14 版本（2014 年 7 月）中引入。由于 SAM 3.1 支持比 SAM 3.0 更好的签名类型，因此建议将其作为最低 SAM 实现版本。i2pd 也支持大多数 3.1 功能。

- DEST GENERATE 和 SESSION CREATE 现在支持 SIGNATURE_TYPE 参数。
- HELLO VERSION 中的 MIN 和 MAX 参数现在为可选。
- HELLO VERSION 中的 MIN 和 MAX 参数现在支持单数字版本号，例如 "3"。
- 桥接套接字现在支持 RAW SEND。

### 版本 3.2 的变更

版本 3.2 在 Java I2P 0.9.24 版本（2016 年 1 月）中引入。请注意，i2pd 目前不支持大多数 3.2 功能。

#### I2CP 端口和协议支持

- SESSION CREATE 选项 FROM_PORT 和 TO_PORT  
- SESSION CREATE STYLE=RAW 选项 PROTOCOL  
- STREAM CONNECT、DATAGRAM SEND 和 RAW SEND 选项 FROM_PORT 和 TO_PORT  
- RAW SEND 选项 PROTOCOL  
- DATAGRAM RECEIVED、RAW RECEIVED 以及被转发或接收的流和可回复数据报，包含 FROM_PORT 和 TO_PORT  
- RAW 会话选项 HEADER=true 会导致被转发的原始数据报前添加一行，内容为 PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn  
- 通过端口 7655 发送的数据报首行现在可以以任意 3.x 版本开头  
- 通过端口 7655 发送的数据报首行可包含 FROM_PORT、TO_PORT、PROTOCOL 中的任意选项  
- RAW RECEIVED 包含 PROTOCOL=nnn

#### SSL 和认证

- HELLO 参数中的 USER/PASSWORD 用于授权。参见[下方](#authorization)。
- 使用 AUTH 命令进行可选的授权配置。参见[下方](#authorization-configuration-sam-32-or-higher-optional-feature)。
- 控制套接字上可选的 SSL/TLS 支持。参见[下方](#ssl)。
- STREAM FORWARD 选项 SSL=true

#### 多线程

- 允许在同一会话 ID 上并发挂起 STREAM ACCEPT 操作。

#### 命令行解析和保持连接

- 可选命令 QUIT、STOP 和 EXIT 用于关闭会话和套接字。参见[下文](#quitstopexitinvisible-sam-32-or-higher-optional-features)。
- 命令解析将正确处理 UTF-8。
- 命令解析能可靠地处理引号内的空白字符。
- 命令行中可用反斜杠 '\\' 转义引号。
- 建议服务器将命令映射为大写，以便通过 telnet 测试。
- 允许空的选项值，例如 PROTOCOL 或 PROTOCOL=，具体取决于实现。
- 支持 PING/PONG 用于保活。见下文。
- 服务器可对 HELLO 或后续命令实施超时机制，具体取决于实现。

### 版本 3.3 的变更

版本 3.3 在 Java I2P 0.9.25 版本（2016 年 3 月）中引入。请注意，i2pd 目前不支持大多数 3.3 功能。

- 同一个会话可同时用于流、数据报和原始数据。传入的数据包和流将根据 I2P 协议和目标端口进行路由。参见下方的 [PRIMARY 会话部分](#sam-primary-sessions-v33-and-higher)。
- DATAGRAM SEND 和 RAW SEND 现在支持选项 SEND_TAGS、TAG_THRESHOLD、EXPIRES 和 SEND_LEASESET。参见下方的 [数据报发送部分](#sending-repliable-or-raw-datagrams)。

### 2025-04 更新

两项提案已于2025年4月在此被批准并纳入规范。没有版本变更来表明支持。一些实现尚未支持，而在其他实现中，支持仍处于初步阶段。

- 支持数据报 2/3（提案 163）。在 SESSION CREATE 和 SESSION ADD（子会话）中指定。见下文。
- 获取 leaseset 选项（提案 167）。通过 NAMING LOOKUP OPTIONS=true 指定。见下文。

## 版本 3 协议

### 简单匿名消息（SAM）版本3.3 规范概述

客户端应用程序与SAM桥接器通信，后者负责处理所有的I2P功能（使用[流式库](/docs/api/streaming)处理虚拟流，或直接使用[I2CP](/docs/protocol/i2cp)处理数据报）。

默认情况下，客户端与SAM桥之间的通信是未加密且未经认证的。SAM桥可能支持SSL/TLS连接；其配置和实现细节不在本规范的范围内。从SAM 3.2版本开始，初始握手过程中支持可选的身份验证用户名/密码参数，且桥接器可能会要求提供这些参数。

I2P 通信可以采取几种不同的形式：

- [虚拟流](/docs/api/streaming)
- [可回复且经过认证的数据报](/docs/specs/datagrams#repliable)（包含 FROM 字段的消息）
- [匿名数据报](/docs/specs/datagrams#raw)（原始匿名消息）
- [Datagram2](/docs/specs/datagrams#datagram2)（一种新的可回复且经过认证的格式）
- [Datagram3](/docs/specs/datagrams#datagram3)（一种新的可回复但未经认证的格式）

I2P 通信由 I2P 会话支持，每个 I2P 会话都绑定到一个地址（称为 destination）。一个 I2P 会话与上述三种类型之一相关联，除非使用[主会话](#sam-primary-sessions-v33-and-higher)，否则不能承载其他类型的通信。

### 编码与转义

所有这些 SAM 消息都以单行发送，并以换行符（\\n）结尾。在 SAM 3.2 之前，仅支持 7 位 ASCII 编码。从 SAM 3.2 开始，编码必须为 UTF-8。任何 UTF8 编码的键或值都应能正常工作。

本规范中显示的格式仅为了便于阅读，虽然每条消息的前两个单词必须保持其特定顺序，但 key=value 对的顺序可以改变（例如“ONE TWO A=B C=D”或“ONE TWO C=D A=B”都是完全有效的构造）。此外，该协议区分大小写。在下文中，以“->”开头的消息示例表示由客户端发送至SAM桥的消息，以“<-”开头的消息示例表示由SAM桥发送至客户端的消息。

基本命令或响应行采用以下形式之一：

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
仅对 SAM 3.2 中的某些新命令支持没有子命令的 COMMAND。

键值对必须用单个空格分隔。（自 SAM 3.2 起，允许多个空格）如果值包含空格，则必须用双引号括起来，例如 key="long value text"。（在 SAM 3.2 之前，某些实现中此功能不可靠）

在 SAM 3.2 之前，没有转义机制。从 SAM 3.2 开始，双引号可以用反斜杠 '\\' 进行转义，而反斜杠本身可以用两个反斜杠 '\\\\' 表示。

### 空值

从 SAM 3.2 开始，空的选项值（例如 KEY、KEY= 或 KEY=""）可能会被允许，具体取决于实现。

### 大小写敏感性

根据规范，该协议是区分大小写的。建议（但不是必须）服务器将命令映射为大写，以便通过 telnet 进行测试。例如，这将允许使用 "hello version" 命令。此行为取决于具体实现。请不要将键或值映射为大写，因为这会破坏 [I2CP](/docs/protocol/i2cp) 选项。

### SAM 连接握手

在客户端和网桥协商确定协议版本之前，无法进行任何 SAM 通信。协商过程通过客户端发送 HELLO 消息，网桥回复 HELLO REPLY 来完成：

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
和

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
从版本 3.1（I2P 0.9.14）开始，MIN 和 MAX 参数为可选。SAM 总是会在 MIN 和 MAX 约束条件下返回可能的最高版本；若未提供约束条件，则返回当前服务器版本。

如果 SAM 桥找不到合适的版本，它将回复：

```
<- HELLO REPLY RESULT=NOVERSION
```
如果发生某些错误，例如请求格式错误，它将回复：

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

服务器的控制套接字可选择性地提供 SSL/TLS 支持，具体取决于服务器和客户端的配置。实现方案也可能提供其他传输层；但这超出了协议定义的范围。

#### 授权

对于授权，客户端需将 USER="xxx" PASSWORD="yyy" 添加到 HELLO 参数中。建议但不是必须对用户名和密码使用双引号。用户名或密码中的双引号必须用反斜杠进行转义。如果失败，服务器将返回 I2P_ERROR 及错误信息。建议在需要授权的 SAM 服务器上启用 SSL。

#### 超时

服务器可能会为 HELLO 或后续命令实施超时，具体取决于实现。客户端应在连接后立即发送 HELLO 及下一个命令。

如果在收到 HELLO 之前发生超时，桥接器将回复：

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
然后断开连接。

如果在收到 HELLO 之后、下一个命令之前发生超时，桥接将回复：

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
然后断开连接。

### I2CP 端口和协议

从 SAM 3.2 开始，SAM 客户端发送方可以指定 [I2CP](/docs/protocol/i2cp) 端口和协议，并将其传递给 [I2CP](/docs/protocol/i2cp)，SAM 桥接器会将接收到的 [I2CP](/docs/protocol/i2cp) 端口和协议信息传递回 SAM 客户端。

对于 FROM_PORT 和 TO_PORT，有效范围是 0-65535，默认值为 0。

对于仅在 RAW 模式下可指定的 PROTOCOL，有效范围是 0-255，默认值为 18。

对于 SESSION 命令，指定的端口和协议是该会话的默认值。对于单个流或数据报，指定的端口和协议将覆盖会话的默认设置。对于接收到的流或数据报，所指示的端口和协议是根据 [I2CP](/docs/protocol/i2cp) 接收的值。

#### 与标准IP的重要区别

I2CP 端口用于 I2P 套接字和数据报。它们与连接到 SAM 的本地套接字无关。

- 端口 0 是有效的，具有特殊含义。
- 端口 1-1023 并无特殊或特权含义。
- 服务器默认在端口 0 上监听，表示“所有端口”。
- 客户端默认发送到端口 0，表示“任意端口”。
- 客户端默认从端口 0 发送，表示“未指定”。
- 服务器可以在端口 0 上运行一个服务，同时在更高端口上运行其他服务。如果是这样，端口 0 的服务为默认服务，当传入的套接字或数据报端口不匹配其他服务时，将连接到该服务。
- 大多数 I2P 目的地仅运行一个服务，因此你可以使用默认设置，忽略 I2CP 端口配置。
- 需要使用 SAM 3.2 或 3.3 才能指定 I2CP 端口。
- 如果你不需要指定 I2CP 端口，则无需使用 SAM 3.2 或 3.3；SAM 3.1 已足够。
- 协议 0 是有效的，表示“任意协议”。但不推荐使用，可能无法正常工作。
- I2P 套接字通过内部连接 ID 进行跟踪。因此，不需要 dest:port:dest:port:protocol 这个 5 元组保持唯一。例如，两个目的地之间可以存在多个具有相同端口的套接字。客户端在建立出站连接时，无需选择“空闲端口”。

如果你正在设计使用多个子会话的 SAM 3.3 应用程序，请仔细考虑如何有效使用端口和协议。更多信息请参见 [I2CP](/docs/protocol/i2cp) 规范。

### SAM 会话

SAM 会话由客户端向 SAM 桥接器打开套接字、执行握手并发送 SESSION CREATE 消息来创建，当套接字断开连接时，会话即终止。

每个注册的 I2P 目标都唯一关联一个会话 ID（或昵称）。会话 ID（包括主会话的子会话 ID）必须在 SAM 服务器上全局唯一。为防止与其他客户端发生 ID 冲突，最佳实践是由客户端随机生成 ID。

每个会话都唯一关联于：

- 客户端创建会话所用的套接字
- 其 ID（或昵称）

#### 会话创建请求

会话创建消息只能使用以下其中一种形式（通过其他形式接收到的消息将回复错误信息）：

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION 指定了用于发送和接收消息/数据流的目标地址。$privkey 是以下内容连接后的 Base64 编码：[目标地址（Destination）](/docs/specs/common-structures#type_Destination)，后跟[私钥（Private Key）](/docs/specs/common-structures#type_PrivateKey)，再跟[签名私钥（Signing Private Key）](/docs/specs/common-structures#type_SigningPrivateKey)，之后可选地包含[离线签名（Offline Signature）](/docs/specs/common-structures#struct_OfflineSignature)。该二进制数据长度至少为 663 字节，Base64 编码后至少为 884 字节，具体长度取决于签名类型。二进制格式详见“私钥文件”说明。有关目标地址密钥生成的更多说明，请参见下方关于[私钥（Private Key）](/docs/specs/common-structures#type_PrivateKey)的补充说明。

如果签名私钥全为零，则接下来是[离线签名](/docs/specs/common-structures#struct_OfflineSignature)部分。离线签名仅支持 STREAM 和 RAW 会话。离线签名不能使用 DESTINATION=TRANSIENT 创建。离线签名部分的格式如下：

1. 过期时间戳（4 字节，大端序，自纪元以来的秒数，将在 2106 年回绕）
2. 临时签名公钥的签名类型（2 字节，大端序）
3. 临时签名公钥（长度由临时签名类型指定）
4. 离线密钥对上述三个字段的签名（长度由目标签名类型指定）
5. 临时签名私钥（长度由临时签名类型指定）

如果目的地指定为 TRANSIENT，SAM 桥将创建一个新的目的地。从版本 3.1（I2P 0.9.14）开始，若目的地为 TRANSIENT，则支持可选参数 SIGNATURE_TYPE。SIGNATURE_TYPE 的值可以是 [密钥证书](/docs/specs/common-structures#type_Certificate) 中支持的任意名称（例如 ECDSA_SHA256_P256，不区分大小写）或数字（例如 1）。默认值为 DSA_SHA1，但这通常不是你想要的。对于大多数应用，请指定 SIGNATURE_TYPE=7。

$nickname 由客户端自行选择，不允许包含空白字符。

附加的选项将传递给 I2P 会话配置，除非由 SAM 桥接器解释（例如 outbound.length=0）。

Java I2P 和 i2pd 路由器在隧道数量上的默认值不同。Java 的默认值是 2，而 i2pd 的默认值是 5。对于大多数低至中等带宽和低至中等连接数的场景，2 或 3 个隧道已足够。请在 SESSION CREATE 消息中明确指定隧道数量，以在 Java I2P 和 i2pd 路由器上获得一致的性能，例如使用选项 inbound.quantity=3 outbound.quantity=3。这些及其他选项[在下方链接中有详细说明](#tunnel-i2cp-and-streaming-options)。

SAM 桥本身应该已经配置好了要通过哪个路由器在 I2P 上通信（不过如有需要，可能提供覆盖方式，例如 i2cp.tcp.host=localhost 和 i2cp.tcp.port=7654）。

#### 会话创建响应

收到会话创建消息后，SAM 桥将回复会话状态消息，如下所示：

如果创建成功：

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey 是 [Destination](/docs/specs/common-structures#type_Destination)、[Private Key](/docs/specs/common-structures#type_PrivateKey) 和 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) 的连接结果的 Base64 编码，之后可选地包含 [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature)。其二进制格式长度至少为 663 字节，Base64 编码后至少为 884 字节，具体长度取决于签名类型。二进制格式在 Private Key File 中有详细说明。

如果 SESSION CREATE 包含一个全零的签名私钥和一个[离线签名](/docs/specs/common-structures#struct_OfflineSignature)部分，则 SESSION STATUS 回复将包含相同格式的相同数据。详情请参见上面的 SESSION CREATE 部分。

如果该昵称已关联到一个会话：

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
如果该目的地已在使用中：

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
如果目标不是有效的私有目标密钥：

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
如果发生了其他错误：

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
如果不可行，MESSAGE 应包含人类可读的信息，说明会话无法创建的原因。

请注意，路由器会在响应 SESSION STATUS 之前先建立隧道。这可能需要几秒钟，或者在路由器启动期间或网络严重拥塞时，可能需要一分钟甚至更长时间。如果建立失败，路由器不会在几分钟内返回失败消息。因此，请勿设置过短的超时时间来等待响应，也不要中途中止会话并重试，尤其是在隧道正在建立的过程中。

SAM 会话的生命周期与其关联的套接字相同。当套接字关闭时，会话也随之终止，所有使用该会话的通信将同时中断。反之，当会话因任何原因终止时，SAM 桥接器也会关闭对应的套接字。

### SAM 虚拟流

虚拟流保证可靠且有序地发送，并在结果可用时立即通知成功或失败。

流（Streams）是两个 I2P 目的地之间的双向通信套接字，但必须由其中一方发起连接请求。此后，SAM 客户端使用 CONNECT 命令来发起此类请求。当 SAM 客户端希望监听来自其他 I2P 目的地的请求时，则使用 FORWARD / ACCEPT 命令。

### SAM 虚拟流：CONNECT

客户端通过以下方式请求连接：

- 通过SAM桥接打开一个新套接字
- 发送与上述相同的HELLO握手
- 发送STREAM CONNECT命令

#### 连接请求

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
这会从 ID 为 $nickname 的本地会话建立一条到指定对等方的新虚拟连接。

目标是 $destination，即 [目标地址](/docs/specs/common-structures#type_Destination) 的 Base64 编码，根据签名类型的不同，其长度为 516 个或更多 Base64 字符（二进制形式为 387 字节或更多）。

**注意：** 自2014年左右（SAM v3.1）起，Java I2P 已支持将主机名和 b32 地址用作 $destination，但此前未记录此功能。自 0.9.48 版本起，Java I2P 正式支持主机名和 b32 地址。i2pd 路由器自 2.38.0 版本（对应 0.9.50）起也支持主机名和 b32 地址。对于这两个路由器，“b32”支持均包含对用于隐藏目的地的扩展“b33”地址的支持。

#### 连接响应

如果传入 SILENT=true，SAM 桥接将不会在套接字上发送任何其他消息。如果连接失败，套接字将被关闭；如果连接成功，当前套接字中所有后续传输的数据都将被转发至已连接的 I2P 目标对等节点，并从该节点接收数据。

如果 SILENT=false（这是默认值），SAM 桥接器在转发或关闭套接字之前会向其客户端发送最后一条消息：

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 值可能是以下之一：

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
如果 RESULT 为 OK，所有通过当前套接字的剩余数据都将被转发至已连接的 I2P 目标对等体，反之亦然。如果连接无法建立（超时等），RESULT 将包含相应的错误值（可能附带一条可选的、人类可读的 MESSAGE），并且 SAM 桥接器将关闭该套接字。

路由器流连接的内部超时时间约为一分钟，具体取决于实现。不要设置短于该时间的超时来等待响应。

### SAM 虚拟流：ACCEPT

客户端通过以下方式等待传入的连接请求：

- 通过SAM桥接打开一个新套接字  
- 发送与上述相同的HELLO握手  
- 发送STREAM ACCEPT命令

#### 接受请求

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
这会使会话 ${nickname} 监听来自 I2P 网络的一个传入连接请求。当会话中存在活动的 FORWARD 时，不允许使用 ACCEPT。

从 SAM 3.2 开始，允许在同一会话 ID 上（甚至使用相同端口）进行多个并发的待处理 STREAM ACCEPT 操作。在 3.2 之前，并发的 ACCEPT 操作会因 ALREADY_ACCEPTING 而失败。注意：从版本 0.9.24（2016-01）起，Java I2P 也已在 SAM 3.1 上支持并发 ACCEPT 操作。i2pd 从版本 2.50.0（2023-12）起也已在 SAM 3.1 上支持并发 ACCEPT 操作。

#### 接受响应

如果传入 SILENT=true，SAM 桥接将不会在套接字上发送任何其他消息。如果接受连接失败，套接字将被关闭。如果接受连接成功，当前套接字中所有剩余的数据将被转发至已连接的 I2P 目标对等体，并从该对等体接收数据。为了可靠性，并能接收到传入连接的目的地信息，建议使用 SILENT=false。

如果 SILENT=false（这是默认值），SAM 桥接将返回以下响应：

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 值可能是以下之一：

```
OK
I2P_ERROR
INVALID_ID
```
如果结果不是 OK，SAM 桥接会立即关闭套接字。如果结果是 OK，SAM 桥接将开始等待来自其他 I2P 节点的入站连接请求。当请求到达时，SAM 桥接会接受该请求并执行以下操作：

如果传入了 SILENT=true，SAM 桥接将不会在客户端套接字上发出任何其他消息。当前套接字中传输的所有剩余数据都将被转发至已连接的 I2P 目标对等节点，或从该节点接收。

如果传入了 SILENT=false（这是默认值），SAM 桥会向客户端发送一条 ASCII 行，其中包含请求对等方的 base64 公钥地址，以及仅适用于 SAM 3.2 的附加信息：

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
在此以 '\\n' 结尾的行之后，所有通过当前套接字传输的剩余数据都将被转发至已连接的 I2P 目标对等体，反之亦然，直到其中一方关闭套接字为止。

#### 确定后的错误

在极少数情况下，SAM 桥可能在发送 RESULT=OK 后、但在连接到达并向客户端发送 $destination 行之前遇到错误。这些错误可能包括路由器关闭、路由器重启以及会话关闭。在这种情况下，当 SILENT=false 时，SAM 桥可能会（但不是必须，取决于具体实现）发送以下行：

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
然后立即关闭套接字。当然，这一行无法解码为有效的 Base 64 目标地址。

### SAM 虚拟流：FORWARD

客户端可以使用常规的套接字服务器，并等待来自 I2P 的连接请求。为此，客户端必须：

- 使用 SAM 桥接器打开一个新套接字
- 发送与上述相同的 HELLO 握手
- 发送转发命令

#### 转发请求

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
这使得会话 ${nickname} 监听来自 I2P 网络的入站连接请求。当会话上存在待处理的 ACCEPT 时，不允许 FORWARD 操作。

#### 转发响应

SILENT 默认为 false。无论 SILENT 为 true 或 false，SAM 桥始终会以 STREAM STATUS 消息进行响应。注意，这与 SILENT=true 时 STREAM ACCEPT 和 STREAM CONNECT 的行为不同。STREAM STATUS 消息如下：

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
RESULT 值可能是以下之一：

```
OK
I2P_ERROR
INVALID_ID
```
$host 是 SAM 将连接请求转发到的套接字服务器的主机名或 IP 地址。如果未提供，则 SAM 将使用发出转发命令的套接字的 IP 地址。

$port 是 SAM 将连接请求转发到的套接字服务器的端口号。此参数为必填项。

当来自 I2P 的连接请求到达时，SAM 桥接器会向 $host:$port 打开一个套接字连接。如果在 3 秒内被接受，SAM 将接受来自 I2P 的连接，然后：

如果传入了 SILENT=true，则所有通过获取到的当前套接字传输的数据都会被转发至已连接的 I2P 目标对等节点，反之亦然。

如果传递了 SILENT=false（这是默认值），SAM 桥会通过获取的套接字发送一条 ASCII 行，其中包含请求端的 base64 公钥目标地址，以及仅适用于 SAM 3.2 的附加信息：

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
在此以 '\\n' 结尾的行之后，所有通过该套接字传输的剩余数据将被转发至已连接的 I2P 目标对等体，直到其中一方关闭套接字为止。

从 SAM 3.2 开始，如果指定了 SSL=true，则转发套接字将通过 SSL/TLS 进行通信。

一旦“转发”套接字关闭，I2P路由器将停止监听传入的连接请求。

### SAM 数据报

SAMv3 提供了通过本地数据报套接字发送和接收数据报的机制。一些 SAMv3 实现还支持通过 SAM 桥接套接字使用较旧的 v1/v2 方式发送/接收数据报。以下将对这两种方式分别进行说明。

I2P 支持四种类型的数据报：

- 可回复且经过认证的数据报会在开头包含发送方的目的地，并包含发送方的签名，因此接收方可以验证发送方的目的地未被伪造，并可对数据报进行回复。新的 Datagram2 格式也是可回复且经过认证的。
- 新的 Datagram3 格式是可回复的，但未经认证。发送方的信息未经验证。
- 原始数据报不包含发送方的目的地，也没有签名。

为可回复和原始数据报定义了默认的 I2CP 端口。原始数据报的 I2CP 端口可以更改。

一种常见的协议设计模式是：客户端向服务器发送可回复的数据报，并包含某个标识符，服务器则返回一个包含该标识符的原始数据报，以便将响应与请求进行关联。这种设计模式消除了在回复中使用可回复数据报所带来的显著开销。所有I2CP协议和端口的选择都是特定于应用的，设计者应考虑这些问题。

另请参见下节中关于数据报MTU的重要说明。

#### 发送可回复或原始数据报

尽管 I2P 本身不包含“发件人地址”（FROM address），但为了使用方便，提供了一个额外的层，即“可回复的数据报”（repliable datagrams）——这是一种最大可达 31744 字节的无序且不可靠的消息，其中包含一个 FROM 地址（最多预留 1KB 用于头部信息）。该 FROM 地址由 SAM 在内部进行认证（利用目标地址的签名密钥来验证来源），并具备防止重放攻击的功能。

最小大小为 1。为了获得最佳的传输可靠性，建议的最大大小约为 11 KB。可靠性与消息大小成反比，甚至可能是指数级下降。

在通过 STYLE=DATAGRAM 或 STYLE=RAW 建立 SAM 会话后，客户端可以通过 SAM 的 UDP 端口（默认为 7655）发送可回复的或原始的数据报。

通过此端口发送的数据报的第一行必须采用以下格式。这整行内容（以空格分隔）实际上位于同一行，此处为清晰起见分行显示：

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 是 SAM 的版本号。从 SAM 3.2 开始，允许使用任何 3.x 版本。
- $nickname 是将要使用的 DATAGRAM 会话的 ID。
- 目标地址为 $destination，即 [Destination](/docs/specs/common-structures#type_Destination) 的 base64 编码，长度为 516 个或更多 base64 字符（二进制形式为 387 字节或更长），具体长度取决于签名类型。**注意：** 自约 2014 年（SAM v3.1）起，Java I2P 已支持将主机名和 b32 地址用作 $destination，但此前未正式记录。自 Java I2P 0.9.48 版本起，主机名和 b32 地址已获官方支持。目前 i2pd 路由器尚不支持主机名和 b32 地址，未来版本可能会增加支持。
- 所有选项均为每条数据报的设置，会覆盖 SESSION CREATE 中指定的默认值。
- 如果 SAM 服务器支持，版本 3.3 中的选项 SEND_TAGS、TAG_THRESHOLD、EXPIRES 和 SEND_LEASESET 将被传递给 [I2CP](/docs/protocol/i2cp)。详情请参阅 [I2CP 规范](/docs/protocol/i2cp#msg_SendMessageExpire)。SAM 服务器对这些选项的支持是可选的，不支持时将忽略它们。
- 本行以 '\\n' 结尾。

在将消息的剩余数据发送到指定目的地之前，SAM 会丢弃第一行。

有关发送可回复和原始数据报的替代方法，请参见[数据报发送和原始发送](#datagram-send-raw-send-v1v2-compatible-datagram-handling)（支持v1/v2的数据报处理）。

#### SAM 可回复数据报：接收数据报

如果在 SESSION CREATE 命令中未指定转发 PORT，则接收到的数据报将由 SAM 写入打开数据报会话的套接字。这是与 v1/v2 兼容的数据报接收方式。

当数据报到达时，桥接器通过以下消息将其传递给客户端：

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
源是 $destination，即 [目标](/docs/specs/common-structures#type_Destination) 的 Base64 编码，根据签名类型的不同，其长度为 516 个或更多 Base64 字符（二进制形式为 387 字节或更多）。

SAM 桥接不会向客户端暴露认证头或其他字段，仅传递发送方提供的数据。这种情况会一直持续，直到会话关闭（由客户端断开连接）。

#### 转发原始或可回复的数据报

创建数据报会话时，客户端可要求SAM将收到的消息转发至指定的 ip:port。方法是使用 PORT 和 HOST 选项发送 CREATE 命令：

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey 是 [目标地址](/docs/specs/common-structures#type_Destination)、[私钥](/docs/specs/common-structures#type_PrivateKey) 和 [签名私钥](/docs/specs/common-structures#type_SigningPrivateKey) 三者连接后的 Base64 编码，其后可选地跟随 [离线签名](/docs/specs/common-structures#struct_OfflineSignature)。该字符串长度为 884 个或更多 Base64 字符（二进制形式为 663 字节或更多），具体长度取决于签名类型。二进制格式在私钥文件规范中有详细说明。

RAW、DATAGRAM2 和 DATAGRAM3 数据报支持离线签名，但 DATAGRAM 不支持。详情请参见上面的 SESSION CREATE 部分以及下面的 DATAGRAM2/3 部分。

$host 是指 SAM 将把数据报转发到的报文服务器的主机名或 IP 地址。若未提供，SAM 将使用发出转发命令的套接字的 IP 地址。

$port 是数据报服务器的端口号，SAM 将向该端口转发数据报。如果未设置 $port，则数据报将不会被转发，而是以兼容 v1/v2 的方式在控制套接字上接收。

附加选项将传递给 I2P 会话配置，除非被 SAM 桥接器解释（例如 outbound.length=0）。这些选项[在下方有文档说明](#tunnel-i2cp-and-streaming-options)。

转发的可回复数据报始终以Base64编码的目标地址作为前缀，但Datagram3除外，详见下文。当收到一个可回复的数据报时，桥接器会向指定的主机:端口发送一个UDP数据包，其中包含以下数据：

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
转发的原始数据报会原封不动地转发到指定的主机:端口，且不带前缀。UDP 数据包包含以下数据：

```
$datagram_payload
```
从 SAM 3.2 开始，当在 SESSION CREATE 中指定 HEADER=true 时，转发的原始数据报将在前面添加一个如下所示的头部行：

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 Base64 编码，根据签名类型的不同，其长度为 516 个或更多 Base64 字符（二进制形式为 387 字节或更多）。

#### SAM 匿名（原始）数据报

充分发挥 I2P 带宽性能，SAM 允许客户端发送和接收匿名数据报，而将认证和回复信息的处理交由客户端自身完成。这些数据报是不可靠且无序的，最大长度可达 32768 字节。

最小大小为 1。为了获得最佳的传输可靠性，建议的最大大小约为 11 KB。

在通过 STYLE=RAW 建立 SAM 会话后，客户端可以通过 SAM 桥接以与[发送可回复或原始数据报](#sending-repliable-or-raw-datagrams)完全相同的方式发送匿名数据报。

接收数据报的这两种方式也适用于匿名数据报。

如果在 SESSION CREATE 命令中未指定转发 PORT，则接收到的数据报将由 SAM 写入打开数据报会话的套接字。这是与 v1/v2 兼容的数据报接收方式。

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
当需要将匿名数据报转发到某个主机:端口时，桥接器会向指定的主机:端口发送一条包含以下数据的消息：

```
$datagram_payload
```
从 SAM 3.2 开始，当在 SESSION CREATE 中指定 HEADER=true 时，转发的原始数据报将在前面添加一个如下所示的头部行：

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
对于发送匿名数据报的另一种方法，请参见 [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling)。

#### 数据报 2/3

数据报格式 2/3 是在 2025 年初指定的新格式。目前尚无已知的实现。请查阅相关实现文档以了解当前状态。更多信息请参见[规范说明](/docs/specs/datagrams)。

目前没有计划提升 SAM 版本来表明对 Datagram 2/3 的支持。这可能会带来问题，因为某些实现可能希望支持 Datagram 2/3，但不支持 SAM v3.3 的功能。任何版本变更都待定（TBD）。

Datagram2 和 Datagram3 都是可回复的，但只有 Datagram2 经过身份验证。

从 SAM 的角度来看，Datagram2 与可回复的数据报完全相同，两者都经过身份验证。只有 I2CP 格式和签名不同，但这对 SAM 客户端不可见。Datagram2 还支持离线签名，因此可用于离线签名的目标地址。

Datagram2 的目的是在不需要向后兼容性的新应用中取代可回复数据报（Repliable datagrams）。Datagram2 提供了可回复数据报所不具备的重放保护机制。如果需要向后兼容，一个应用可以在 SAM 3.3 PRIMARY 会话中同时支持 Datagram2 和可回复数据报。

Datagram3 可回复但未经认证。I2CP 格式中的 'from' 字段是一个哈希值，而非目的地。SAM 服务器发送给客户端的 $destination 将是一个 44 字节的 base64 哈希。要将其转换为可用于回复的完整目的地，请先将其 base64 解码为 32 字节的二进制数据，然后 base32 编码为 52 个字符，并附加 ".b32.i2p" 以进行 NAMING LOOKUP（命名查找）。与通常情况一样，客户端应维护自己的缓存，以避免重复进行 NAMING LOOKUP。

应用程序设计者应格外谨慎，并考虑未经认证的数据报所带来的安全影响。

#### V3 数据报 MTU 考虑事项

I2P 数据报可能大于典型的互联网 MTU（最大传输单元）1500 字节。本地发送的数据报以及以 516 字节以上的 base64 格式目标地址为前缀的可回复转发数据报，很可能超过该 MTU。然而，Linux 系统上的本地回环（localhost）MTU 通常要大得多，例如 65536。不同操作系统的本地回环 MTU 可能有所不同。I2P 数据报的大小永远不会超过 65536 字节。数据报的大小取决于具体的应用协议。

如果 SAM 客户端与 SAM 服务器位于本地且系统支持更大的 MTU，则数据报不会在本地分片。然而，如果 SAM 客户端位于远程，IPv4 数据报将会被分片，而 IPv6 数据报将会失败（IPv6 不支持 UDP 分片）。

客户端库和应用程序开发者应了解这些问题，并记录相关建议以避免碎片化并防止数据包丢失，特别是在远程 SAM 客户端-服务器连接中。

#### 数据报发送，原始发送（V1/V2 兼容的数据报处理）

在 SAM V3 中，发送数据报的首选方法是通过如上所述的 7655 端口上的数据报套接字。然而，可回复的数据报也可以通过 SAM 桥接套接字直接使用 DATAGRAM SEND 命令发送，具体用法见 [SAM V1](/docs/api/sam) 和 [SAM V2](/docs/api/samv2) 文档。

从 0.9.14 版本（版本 3.1）开始，可以使用 RAW SEND 命令通过 SAM 桥接套接字直接发送匿名数据报，具体用法详见 [SAM V1](/docs/api/sam) 和 [SAM V2](/docs/api/samv2) 文档。

从版本 0.9.24（版本 3.2）开始，DATAGRAM SEND 和 RAW SEND 可以包含参数 FROM_PORT=nnnn 和/或 TO_PORT=nnnn，以覆盖默认端口。从版本 0.9.24（版本 3.2）开始，RAW SEND 可以包含参数 PROTOCOL=nnn，以覆盖默认协议。

这些命令*不支持* ID 参数。数据报将被发送到最近创建的 DATAGRAM 或 RAW 风格的会话（视情况而定）。未来版本可能会增加对 ID 参数的支持。

DATAGRAM2 和 DATAGRAM3 格式*不*以兼容 V1/V2 的方式支持。

### SAM 主会话（V3.3 及更高版本）

*I2P 0.9.25 版本中引入了版本 3.3。*

*在此规范的早期版本中，PRIMARY 会话被称为 MASTER 会话。在 `i2pd` 和 `I2P+` 中，它们至今仍仅被称为 MASTER 会话。*

SAM v3.3 增加了对在同一主会话上运行流式传输、数据报和原始子会话的支持，并支持运行多个相同类型的子会话。所有子会话的流量都使用单一目的地或一组隧道。来自 I2P 的流量路由基于子会话的端口和协议选项。

要创建多路复用的子会话，您必须先创建一个主会话，然后将子会话添加到该主会话中。每个子会话必须具有唯一的 ID 以及唯一的监听协议和端口。子会话也可以从主会话中移除。

通过主会话（PRIMARY session）和多个子会话（subsessions）的组合，SAM 客户端可以在一组隧道上支持多个应用程序，或支持使用多种协议的单一复杂应用程序。例如，一个 BitTorrent 客户端可以建立一个用于点对点连接的流式子会话，同时建立数据报和原始子会话用于 DHT 通信。

#### 创建主会话

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM 桥将返回成功或失败，具体响应格式参见[标准 SESSION CREATE 的响应](#session-creation-response)。

不要在主会话（primary session）上设置 PORT、HOST、FROM_PORT、TO_PORT、PROTOCOL、LISTEN_PORT、LISTEN_PROTOCOL 或 HEADER 选项。您不得在主会话 ID 或控制套接字上发送任何数据。所有命令（如 STREAM CONNECT、DATAGRAM SEND 等）必须在独立的套接字上使用子会话 ID。

主会话（PRIMARY session）连接到路由器并构建隧道。当SAM桥接响应时，隧道已经建立完毕，此时会话已准备好添加子会话。所有与隧道参数（如长度、数量和昵称）相关的[I2CP](/docs/protocol/i2cp)选项都必须在主会话的SESSION CREATE命令中提供。

所有实用命令都在主会话中受支持。

当主会话关闭时，所有子会话也会随之关闭。

注意：在 0.9.47 版本之前，请使用 STYLE=MASTER。从 0.9.47 版本开始支持 STYLE=PRIMARY。为保持向后兼容，仍然支持 MASTER。

#### 创建子会话

使用创建 PRIMARY 会话所用的相同控制套接字：

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM 桥将返回成功或失败，响应格式与[标准 SESSION CREATE 的响应](#session-creation-response)相同。由于隧道已在主 SESSION CREATE 中建立，SAM 桥应立即响应。

不要在 SESSION ADD 上设置 DESTINATION 选项。子会话将使用主会话中指定的目的地。所有子会话都必须在控制套接字上添加，即在创建主会话的同一连接上。

多个子会话必须具有足够独特的选项，以确保传入的数据能够正确路由。特别是，同一类型的多个会话必须具有不同的 LISTEN_PORT 选项（对于 RAW 类型，还需要不同的 LISTEN_PROTOCOL）。如果 SESSION ADD 请求中的监听端口和协议与现有子会话重复，则会导致错误。

LISTEN_PORT 是本地 I2P 端口，即用于接收传入数据的（TO）端口。如果未指定 LISTEN_PORT，则将使用 FROM_PORT 的值。如果 LISTEN_PORT 和 FROM_PORT 均未指定，则传入路由将仅基于 STYLE 和 PROTOCOL。对于 LISTEN_PORT 和 LISTEN_PROTOCOL，0 表示任意值，即通配符。如果 LISTEN_PORT 和 LISTEN_PROTOCOL 均为 0，则此子会话将成为无法路由到其他子会话的传入流量的默认会话。传入的流式传输流量（协议 6）永远不会被路由到 RAW 子会话，即使其 LISTEN_PROTOCOL 为 0。RAW 子会话不得将 LISTEN_PROTOCOL 设置为 6。如果没有默认会话或匹配传入流量协议和端口的子会话，则该数据将被丢弃。

使用子会话ID，而不是主会话ID，来发送和接收数据。所有命令（如 STREAM CONNECT、DATAGRAM SEND 等）都必须使用子会话ID。

所有实用命令均支持在主会话或子会话上使用。v1/v2 数据报/原始数据的发送/接收不支持在主会话或子会话上使用。

#### 停止子会话

使用创建 PRIMARY 会话所用的相同控制套接字：

```
->  SESSION REMOVE
          ID=$nickname
```
这会从主会话中移除一个子会话。在 SESSION REMOVE 操作中不要设置任何其他选项。子会话必须在控制套接字上移除，即在创建主会话的同一连接上进行。子会话被移除后，将被关闭，且不能再用于发送或接收数据。

SAM 桥将返回成功或失败，具体响应格式参见[标准 SESSION CREATE 的响应](#session-creation-response)。

### SAM 工具命令

某些实用命令需要预先存在的会话，而某些则不需要。详见下文。

#### 主机名查找

客户端可以使用以下消息向SAM桥查询名称解析：

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
由以下内容回答

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
RESULT 值可能是以下之一：

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
如果 NAME=ME，则回复将包含当前会话使用的目标地址（在使用 TRANSIENT 地址时非常有用）。如果 $result 不是 OK，MESSAGE 可能会提供描述性信息，例如“格式错误”等。INVALID_KEY 意味着请求中的 $name 存在问题，可能是包含无效字符。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 Base64 编码，根据签名类型的不同，其长度为 516 个或更多 Base64 字符（二进制形式为 387 字节或更多）。

NAMING LOOKUP 并不要求必须先创建会话。然而，在某些实现中，未缓存且需要网络查询的 .b32.i2p 查找可能会失败，因为没有可用的客户端隧道来进行查找。

#### 名称查找选项

从路由器 API 0.9.66 开始，NAMING LOOKUP 已扩展以支持服务查找。不同实现的支持情况可能有所不同。更多详细信息请参见提案 167。

NAMING LOOKUP NAME=example.i2p OPTIONS=true 请求回复中包含选项映射。当 OPTIONS=true 时，NAME 可以是完整的 base64 目的地。

如果目标查找成功，并且leaseset中包含选项，则在回复中，目标地址之后将跟有一个或多个格式为OPTION:key=value的选项。每个选项都有独立的OPTION:前缀。回复中将包含leaseset中的所有选项，而不仅仅是服务记录选项。例如，未来定义的参数选项也可能存在。示例：

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

包含 '=' 的键，以及包含换行符的键或值，将被视为无效，相应的键值对将从响应中移除。如果在 leaseset 中未找到任何选项，或者 leaseset 为版本 1，则响应中将不包含任何选项。如果查询中包含 OPTIONS=true 且 leaseset 未找到，则将返回一个新的结果值 LEASESET_NOT_FOUND。

#### 目标密钥生成

可以使用以下消息生成公钥和私钥的base64编码：

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
由以下内容回答

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
从版本 3.1（I2P 0.9.14）开始，支持一个可选参数 SIGNATURE_TYPE。SIGNATURE_TYPE 的值可以是 [密钥证书](/docs/specs/common-structures#type_Certificate) 中支持的任意名称（例如 ECDSA_SHA256_P256，不区分大小写）或数字（例如 1）。默认值为 DSA_SHA1，而这通常不是你想要的。对于大多数应用，请指定 SIGNATURE_TYPE=7。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 Base64 编码，根据签名类型的不同，其长度为 516 个或更多 Base64 字符（二进制形式为 387 字节或更多）。

$privkey 是 [目标地址](/docs/specs/common-structures#type_Destination)、[私钥](/docs/specs/common-structures#type_PrivateKey) 和 [签名私钥](/docs/specs/common-structures#type_SigningPrivateKey) 三者连接后的 Base64 编码，其长度为 884 个或更多 Base64 字符（二进制形式为 663 字节或更多），具体长度取决于签名类型。二进制格式在私钥文件规范中有详细说明。

关于 256 字节二进制[私钥](/docs/specs/common-structures#type_PrivateKey)的说明：此字段自版本 0.6（2005 年）起已不再使用。SAM 实现可能会在此字段中发送随机数据或全零；如果 base64 中出现一串 AAAA，请勿惊慌。大多数应用程序将简单地存储 base64 字符串，并在 SESSION CREATE 时原样返回，或将其解码为二进制进行存储，然后在 SESSION CREATE 时再次编码。然而，应用程序也可以解码 base64，按照 PrivateKeyFile 规范解析二进制数据，丢弃其中 256 字节的私钥部分，然后在重新编码用于 SESSION CREATE 时用 256 字节的随机数据或全零替换。PrivateKeyFile 规范中的所有其他字段必须保留。这样做可以节省 256 字节的文件系统存储空间，但对大多数应用程序来说可能不值得为此费力。更多详细信息和背景请参见提案 161。

DEST GENERATE 不要求必须先创建会话。

DEST GENERATE 无法用于创建具有离线签名的目的地。

#### PING/PONG（SAM 3.2 或更高版本）

客户端或服务器均可发送：

```
PING[ arbitrary text]
```
在控制端口上，响应为：

```
PONG[ arbitrary text from the ping]
```
用于控制套接字的保持连接。如果在合理时间内未收到响应，任一方均可关闭会话和套接字，具体行为取决于实现。

如果等待客户端 PONG 响应时发生超时，桥接器可能会发送：

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
然后断开连接。

如果在等待桥接的 PONG 时发生超时，客户端可能会直接断开连接。

PING/PONG 不需要先创建会话。

#### QUIT/STOP/EXIT（SAM 3.2 或更高版本，可选功能）

命令 QUIT、STOP 和 EXIT 将关闭会话和套接字。此功能的实现是可选的，旨在方便通过 telnet 进行测试。在套接字关闭前是否返回任何响应（例如 SESSION STATUS 消息），取决于具体实现，不在本规范的范围之内。

QUIT/STOP/EXIT 不需要先创建会话。

#### 帮助（可选功能）

服务器可以实现 HELP 命令。此实现是可选的，旨在方便通过 telnet 进行测试。输出格式以及输出结束的检测方式由具体实现决定，不在本规范的范围之内。

HELP 不要求必须先创建会话。

#### 授权配置（SAM 3.2 或更高版本，可选功能）

使用 AUTH 命令进行授权配置。SAM 服务器可实现这些命令以支持凭据的持久化存储。通过非这些命令方式进行的身份验证配置则取决于具体实现，不在本规范的范围之内。

- AUTH ENABLE 启用后续连接的授权
- AUTH DISABLE 禁用后续连接的授权
- AUTH ADD USER="foo" PASSWORD="bar" 添加用户/密码
- AUTH REMOVE USER="foo" 删除该用户

建议但不是必须对用户名和密码使用双引号。用户名或密码中的双引号必须用反斜杠进行转义。如果失败，服务器将回复 I2P_ERROR 及相应消息。

AUTH 不要求必须先创建会话。

### RESULT 值

以下是 RESULT 字段可携带的值及其含义：

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
不同的实现可能在各种情况下返回哪个 RESULT 上不一致。

大多数带有 RESULT 的响应（除了 OK 之外）还会包含一条提供附加信息的 MESSAGE。该 MESSAGE 通常有助于调试问题。然而，MESSAGE 字符串依赖于具体实现，可能由 SAM 服务器根据当前区域设置进行翻译，也可能不翻译，且可能包含内部实现相关的详细信息（例如异常），并且可能会在不另行通知的情况下发生更改。尽管 SAM 客户端可以选择向用户显示 MESSAGE 字符串，但不应基于这些字符串做出程序化决策，因为这样做会非常脆弱。

### 隧道、I2CP 和流媒体选项

这些选项可以以 name=value 的形式在 SAM SESSION CREATE 命令行中传入。

所有会话都可以包含[I2CP 选项，例如隧道长度和数量](/docs/protocol/i2cp#options)。STREAM 会话还可以包含[流式传输库选项](/docs/api/streaming#options)。

请参阅相关文档以获取选项名称和默认值。所引用的文档针对的是 Java 路由器实现。默认值可能随时更改。选项名称和值区分大小写。其他路由器实现可能不支持所有选项，并且可能具有不同的默认值；详情请查阅相应路由器的文档。

### BASE 64 说明

Base 64 编码必须使用 I2P 标准的 Base 64 字母表 "A-Z, a-z, 0-9, -, ~"。

### 默认 SAM 设置

SAM 的默认端口是 7656。在 Java I2P 路由器中，SAM 默认未启用；必须在路由器控制台的“配置客户端”页面上手动启动，或配置为自动启动，也可在 clients.config 文件中进行配置。默认的 SAM UDP 端口是 7655，监听地址为 127.0.0.1。在 Java 路由器中，可通过在启动命令或 SESSION 行中添加参数 sam.udp.port=nnnnn 和/或 sam.udp.host=w.x.y.z 来修改这些设置。

其他路由器中的配置是特定于实现的。请参见[此处的 i2pd 配置指南](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/)。
