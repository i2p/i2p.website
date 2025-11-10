---
title: "新的 I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "多个新的 I2P router 实现正在涌现，包括用 Rust 开发的 emissary 和用 Go 开发的 go-i2p，为嵌入式集成和网络多样性带来新的可能性。"
---

对于 I2P 的开发来说，这是一个令人振奋的时期；我们的社区正在壮大，如今已有多个全新的、完全可用的 I2P router 原型陆续涌现！我们对这一进展感到非常兴奋，也很高兴能与您分享这一消息。

## 这对网络有什么帮助？

编写 I2P routers 有助于证明我们的规范文档确实可用于实现新的 I2P routers，使代码能够被新的分析工具分析，并总体提升网络的安全性和互操作性。多个 I2P routers 意味着潜在缺陷不再一致，对某个 router 的攻击可能对另一款 router 无效，从而避免单一生态问题。不过，从长期来看，也许最令人兴奋的前景是嵌入。

## 什么是嵌入？

在 I2P 的语境中，嵌入是一种将 I2P router 直接包含到另一款应用中、而无需在后台运行独立的 router 的方式。这可以让 I2P 更易于使用，从而通过提高软件的可访问性来促进网络的增长。Java 和 C++ 都存在在各自生态系统之外难以使用的问题：其中，C++ 需要脆弱的手写 C 绑定；而对 Java 来说，从非 JVM 应用与 JVM 应用通信则是一件令人头疼的事。

虽然在许多方面这种情况很正常，但我认为可以加以改进，以使 I2P 更易于使用。其他编程语言对这些问题有更优雅的解决方案。当然，我们应当始终考虑并采用针对 Java 和 C++ routers 的现有指南。

## 使者从黑暗中现身

与我们团队完全独立地，一位名为 altonen 的开发者开发了一个用 Rust 编写的 I2P 实现，名为 emissary。虽然它还相当新，而且我们对 Rust 不太熟悉，但这个颇具吸引力的项目前景光明。祝贺 altonen 创建了 emissary，我们对此印象深刻。

### Why Rust?

使用 Rust 的主要原因基本上与使用 Java 或 Go 的原因相同。Rust 是一种具有内存管理功能的编译型编程语言，并且拥有庞大且高度活跃的社区。Rust 还提供了用于生成 C 编程语言绑定的高级特性，这些绑定相比其他语言更易于维护，同时仍然继承了 Rust 强大的内存安全特性。

### Do you want to get involved with emissary?

emissary 由 altonen 在 GitHub 上开发。您可以在此找到该仓库：[altonen/emissary](https://github.com/altonen/emissary)。Rust 也缺乏与流行的 Rust 网络库兼容的、完善的 SAMv3 客户端库，编写一个 SAMv3 库是一个很好的起点。

## go-i2p is getting closer to completion

大约 3 年来，我一直在开发 go-i2p，尝试将一个尚处于萌芽阶段的库打造成使用纯 Go（另一种内存安全语言）编写的、功能完备的 I2P router。在过去的约 6 个月里，为了提升性能、可靠性和可维护性，它经历了大幅度的重构。

### Why Go?

虽然 Rust 和 Go 具有许多相同的优势，但在很多方面 Go 学起来要简单得多。多年来，已经有用于在 Go 语言中使用 I2P 的优秀库和应用程序，其中包括对 SAMv3.3 库最完整的实现。但如果没有我们可以自动管理的 I2P router(例如嵌入式 router)，这仍然会给用户带来障碍。go-i2p 的目的就是弥合这一差距，并为使用 Go 的 I2P 应用开发者消除所有不便之处。

### 为什么选择 Rust？

go-i2p 在 GitHub 上开发，目前主要由 eyedeekay 负责，并欢迎社区在 [go-i2p](https://github.com/go-i2p/) 贡献。该命名空间下有许多项目，例如：

#### Router Libraries

我们构建了这些库，用于生成我们的 I2P router 库。它们被拆分为多个各自聚焦的代码仓库，便于审阅，并使其对其他想要构建实验性、定制化 I2P router 的人也有用。

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

嗯，如果你想在 XBox 上运行 I2P，有一个处于休眠状态的项目来编写一个 [I2P router in C#](https://github.com/PeterZander/i2p-cs)。其实听起来挺不错的。如果这也不是你的偏好，你可以像 altonen 那样，开发一个全新的 I2P router。

### 你想参与emissary吗？

你可以出于任何原因编写一个 I2P router；I2P 是一个自由的网络，但弄清楚为什么要这样做会对你有所帮助。你是否想赋能某个社区、认为某个工具很适合 I2P，或者想尝试一种策略？先明确你的目标，以便确定该从哪里开始，以及一个 "finished" 状态会是什么样子。

### Decide what language you want to do it in and why

以下是你可能选择一种语言的几个理由：

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

不过，以下是一些你可能不会选择那些语言的理由：

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

There are hundreds of programming languages and we welcome maintained I2P libraries and routers in all of them. Choose your trade-offs wisely and begin.

## go-i2p 离完成越来越近

无论你想用 Rust、Go、Java、C++ 或其他语言开展工作，欢迎在 Irc2P 上的 #i2p-dev 与我们联系。从那里开始，我们会引导你加入与 router 相关的专门频道。我们也在 ramble.i2p 的 f/i2p、reddit 的 r/i2p，以及 GitHub 和 git.idk.i2p 上活跃。期待尽快收到你的消息。
