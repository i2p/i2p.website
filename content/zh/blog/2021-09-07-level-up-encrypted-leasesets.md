---
title: "通过加密的 leaseSet（租约集）提升你的 I2P 技能"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "有人说 I2P 强调隐藏服务，我们在此审视对此的一种解读。"
categories: ["general"]
---

## 使用加密的 LeaseSets（租约集）提升你的 I2P 技能

过去人们常说 I2P 注重对隐藏服务的支持，这在许多方面确实如此。然而，这对用户、开发者以及隐藏服务管理员分别意味着什么，并不总是相同的。加密的 LeaseSets（租约集合）及其用例提供了一个独特且实用的窗口，使人们得以了解 I2P 如何使隐藏服务更灵活、更易于管理，以及 I2P 如何在隐藏服务概念之上进行扩展，从而为潜在且颇具价值的用例提供安全优势。

## 什么是 LeaseSet？

当你创建一个隐藏服务时，你会向 I2P NetDB 发布一个名为 "LeaseSet" 的条目。"LeaseSet" 用最简单的话来说，就是其他 I2P 用户用来确定你的隐藏服务在 I2P 网络中的“位置”的信息。它包含 "Leases"，这些 "Leases" 用于标识可用于到达你隐藏服务的 tunnels，以及你的 Destination（目的地标识）的公钥，客户端会用该公钥对消息进行加密。这种类型的隐藏服务，只要持有地址，任何人都可以访问，这可能是目前最常见的用例。

不过，有时你可能并不想让你的隐藏服务对任何人都可访问。有人把隐藏服务用作访问家用电脑上的 SSH 服务器的方式，或用来组建由 IoT 设备构成的网络。在这些情况下，让你的隐藏服务对 I2P 网络上的所有人可访问既没有必要，甚至可能适得其反。这就是 "Encrypted LeaseSets"（加密的 LeaseSet）派上用场的时候。

## 加密的 LeaseSets：极其隐蔽的服务

Encrypted LeaseSets 是以加密形式发布到 NetDB（网络数据库）中的 LeaseSets，其中的任何 Leases 或公钥都不可见，除非客户端拥有用于解密其中 LeaseSet 的密钥。只有与你共享密钥的客户端（适用于 PSK Encrypted LeaseSets），或将其密钥与你共享的客户端（适用于 DH Encrypted LeaseSets），才能看到该 destination，其他任何人都无法看到。

I2P 支持多种加密的 leaseSet 策略。决定采用哪一种时，理解每种策略的关键特性非常重要。如果一个加密的 leaseSet 采用“预共享密钥(PSK)”策略，那么服务器会生成一个（或多个）密钥，随后由服务器运营者与每个客户端共享。当然，这种交换必须通过带外渠道进行，例如可以在 IRC 上交换。这种加密的 leaseSet 方式有点像用密码登录 Wi‑Fi。不同的是，你“登录”的对象是一个隐藏服务。

如果一个 Encrypted LeaseSet 使用 Diffie-Hellman（DH）策略，那么密钥会在客户端生成。当一个 Diffie-Hellman 客户端连接到带有 Encrypted LeaseSet 的 destination（目标地址）时，必须先与服务器运营者共享其密钥。然后由服务器运营者决定是否授权该 DH 客户端。这种 Encrypted LeaseSets 版本有点像带有 `authorized_keys` 文件的 SSH。不同的是，你登录的是一个 Hidden Service（隐藏服务）。

通过加密你的 LeaseSet（租约集），你不仅使未授权用户无法连接到你的目的地，还使未授权的访问者甚至无法发现该 I2P 隐藏服务的真实目的地。某些读者可能已经为他们自己的加密 LeaseSet 想到了一个用例。

## 使用加密的 LeaseSets 安全地访问 router 控制台

一般而言，某项服务能够获取到的关于你设备的信息越复杂，将该服务暴露在互联网上，甚至是在类似 I2P 的隐藏服务网络中，就越危险。若你要公开此类服务，你需要用诸如密码之类的方式对其进行保护；或者，就 I2P 而言，更全面且更安全的选项可以是加密的 LeaseSet（I2P 中用于发布目的地可达性信息的数据结构）。

**在继续之前，请阅读并理解：如果在没有 Encrypted LeaseSet 的情况下执行以下步骤，您将使 I2P router 的安全性失效。没有 Encrypted LeaseSet，请勿通过 I2P 配置对您的 router 控制台的访问。此外，请不要将您的 Encrypted LeaseSet PSK（预共享密钥）与任何不受您控制的设备共享。**

其中一种适合通过 I2P 共享、但只能在使用加密的 LeaseSet 时共享的服务，就是 I2P router 控制台本身。使用加密的 LeaseSet 将某台机器上的 I2P router 控制台暴露到 I2P 上，就可以让另一台带有浏览器的机器管理该远程 I2P 实例。我发现这对于远程监控我常规的 I2P 服务很有用。它也可以用于监控长期做种的服务器，从而作为访问 I2PSnark 的一种方式。

尽管解释起来要花些时间，通过 Hidden Services Manager UI 设置加密 LeaseSet 其实很简单。

## 在“服务器”上

先在 http://127.0.0.1:7657/i2ptunnelmgr 打开隐藏服务管理器，并滚动到标为"I2P Hidden Services."的部分底部。使用主机"127.0.0.1"和端口"7657"创建一个新的隐藏服务，使用这些"Tunnel 加密选项"，并保存该隐藏服务。

然后，在 Hidden Services Manager 的主页中选择你新建的 tunnel。此时，Tunnel Cryptography Options 应已包含你的第一个预共享密钥。将其记下，以备下一步使用，并同时记录下该 tunnel 的 Encrypted Base32 Address。

## 在 "Client" 上

现在切换到将要连接该隐藏服务的客户端计算机，访问 http://127.0.0.1:7657/configkeyring 的 Keyring 配置页面，添加先前的密钥。首先，将来自服务器的 Base32 粘贴到标有“Full destination, name, Base32, or hash.”的字段中。接着，将来自服务器的预共享密钥粘贴到“Encryption Key”字段中。点击保存，即可使用加密的 LeaseSet 安全地访问该隐藏服务。

## 现在你已经准备好远程管理 I2P 了

正如你所见，I2P 为隐藏服务管理员提供了独特的能力，使他们能够从世界任何地方安全地管理其 I2P 连接。出于同样的原因，我保存在同一设备上的其他 Encrypted LeaseSets（加密的 LeaseSet）指向 SSH 服务器、我用于管理服务容器的 Portainer 实例，以及我个人的 NextCloud 实例。借助 I2P，真正私密、始终可达的自托管是可以实现的目标；事实上，我认为这正是我们独一无二、格外擅长的事情之一，这要归功于 Encrypted LeaseSets。借助它们，I2P 既可以成为保护自托管家庭自动化的关键，也可以成为一种更私密的点对点 Web 的骨干。
