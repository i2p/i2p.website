---
title: "Android 应用发布"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 和 Bote 0.3 已在官方网站、Google Play 和 F-Droid 上发布。"
categories: ["press"]
---

自从我上一次发布关于我们 Android 开发的更新以来，已经过去了一段时间，这期间 I2P 发布了好几个版本，却没有相应的 Android 版本。终于，等待结束了！

## 新应用版本

I2P Android 和 Bote 的新版本已发布！它们可以从这些 URL 下载：

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

这些版本的主要变化是过渡到 Android 全新的 Material Design 设计系统。Material 让那些——姑且这么说——设计功力“极简”的应用开发者（比如我）更容易创建更好用的应用。I2P Android 还将其底层的 I2P router 更新到刚发布的 0.9.17 版。Bote 带来了若干新特性以及许多小改进；例如，现在你可以通过二维码添加新的电子邮件目标地址。

正如我在上一次更新中提到的，用于为应用签名的发布密钥已经更换。其原因在于我们需要更改 I2P Android 的包名。旧的包名（`net.i2p.android.router`）在 Google Play 上已被占用（我们至今仍不清楚是谁在使用它），而我们希望在所有 I2P Android 的发行版中使用相同的包名和签名密钥。这样做意味着用户最初可以从 I2P 网站安装应用，之后如果该网站被封锁，他们也可以通过 Google Play 升级它。Android 操作系统在包名发生变化时会将应用视为完全不同的应用，因此我们也借此机会提高了签名密钥的强度。

新签名密钥的指纹（SHA-256）为:

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

几个月前，我们在挪威的 Google Play 上发布了 I2P Android 和 Bote，以测试那里的发布流程。我们很高兴地宣布，这两款应用现已由[Privacy Solutions](https://privacysolutions.no/)在全球范围内发布。应用可在以下网址找到：

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

全球发布将分多个阶段进行，首先从我们已有翻译的国家/地区开始。一个显著的例外是法国；由于关于密码学代码的进口法规，我们目前无法在 Google Play 法国区分发这些应用。这与 TextSecure 和 Orbot 等其他应用遭遇的同样问题有关。

## F-Droid

F-Droid 用户们，别以为我们忘了你们！除了上述两个位置之外，我们还设置了自己的 F-Droid 仓库。如果你在手机上阅读这篇文章，[点击这里](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) 将其添加到 F-Droid（此功能仅在部分 Android 浏览器中有效）。或者，你也可以将下面的 URL 手动添加到你的 F-Droid 仓库列表中：

https://f-droid.i2p.io/repo

如果你想手动验证软件源签名密钥的指纹（SHA-256），或在添加软件源时手动输入该指纹，内容如下：

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
不幸的是，主 F-Droid 仓库中的 I2P 应用一直未能更新，因为我们的 F-Droid 维护者已失联。我们希望通过维护这个二进制仓库，能更好地支持我们的 F-Droid 用户，并让他们的应用保持最新。如果你已经从主 F-Droid 仓库安装了 I2P，想要升级时需要先卸载它，因为签名密钥会不同。我们 F-Droid 仓库中的应用与我们网站和 Google Play 上提供的 APK 完全相同，因此今后你可以使用上述任一来源进行升级。
