---
title: "I2P 2006-08-01 状态说明"
date: 2006-08-01
author: "jr"
description: "Strong network performance with high I2PSnark transfer rates, NTCP transport stability, and eepsite reachability clarifications"
categories: ["status"]
---

大家好，今晚开会前先做个简短说明。我知道大家可能有各种问题或议题想提出，所以我们会采用比平时更灵活的形式。不过我先简单提几件事。

* Network status

看起来网络运行得相当不错，大量体量较大的 I2PSnark 传输都已完成，单个 routers 上也达到了相当可观的传输速率——我见过 650KBytes/sec 和 17,000 条参与的 tunnels，而且没有任何意外。低端配置的 routers 似乎也表现良好，使用 2 跳 tunnels 浏览 eepsites（I2P 站点）和 irc，平均只用不到 1KByte/sec 的带宽。

不过，并非对所有人来说一切都尽如人意，我们正致力于更新 router 的行为，以实现更一致且更可用的性能。

* NTCP

新的 NTCP 传输（“new” tcp）在解决了最初的磕磕碰碰之后表现相当不错。为回答一个常见问题，从长远来看，NTCP 和 SSU 都会继续运行——我们不会回到仅使用 TCP 的做法。

* eepsite(I2P Site) reachability

请记住，各位，eepsites(I2P Sites) 只有在运行它的人让它保持在线时才能访问——如果它们离线了，你就无能为力 ;) 不幸的是，过去几天 orion.i2p 一直无法访问，但网络肯定仍在正常运作——也许顺道去 inproxy.tino.i2p 或 eepsites(I2P Sites).i2p 满足你的网络调查需求。

总之，还有很多事情在进行中，不过现在在这里提到可能有点为时过早。当然，如果你有任何问题或疑虑，几分钟后就到 #i2p 参加我们*咳*每周的开发会议。

感谢您帮助我们向前迈进！=jr
