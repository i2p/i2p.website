---
title: "I2P Mime 类型"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
---

## 概述

为常见的 I2P 文件格式定义 mime 类型。 在 Debian 软件包中包含定义。 为 .su3 类型及其他可能的类型提供处理程序。

## 动机

为了通过浏览器下载时使重新播种和插件安装更容易，我们需要一个用于 .su3 文件的 mime 类型和处理程序。

同时，在学习如何编写 mime 定义文件后，遵循 freedesktop.org 标准，我们可以为其他常见的 I2P 文件类型添加定义。虽然对于通常不下载的文件，如地址簿阻止文件数据库（hostsdb.blockfile），这些定义用处不大，但在使用如 Ubuntu 的 “nautilus” 等图形目录查看器时，这些定义将允许更好地识别和图标化文件。

通过标准化 mime 类型，每个路由器实现可以编写适当的处理程序，并且 mime 定义文件可以被所有实现共享。

## 设计

编写一个遵循 freedesktop.org 标准的 XML 源文件，并将其包含在 Debian 软件包中。文件名为 "debian/(package).sharedmimeinfo"。

所有 I2P mime 类型将以 "application/x-i2p-" 开头，除了 jrobin rrd。

这些 mime 类型的处理程序是特定于应用程序的，不会在这里指定。

我们还将与 Jetty 一起包含定义，并将其包含在重新播种软件或说明中。

## 规范

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin

## 注释

并非所有上面列出的文件格式都被非 Java 路由器实现使用；有些甚至可能没有明确规范。然而，在此记录它们可能会在未来实现跨实现的一致性。

一些文件后缀如 ".config", ".dat" 和 ".info" 可能会与其他 mime 类型重叠。可以通过附加数据如完整文件名、文件名模式或魔术数字来消除歧义。有关示例，请参见 zzz.i2p 线程中的草案 i2p.sharedmimeinfo 文件。

重要的是 .su3 类型，这些类型具有唯一的后缀和强大的魔术数字定义。

## 迁移

不适用。
