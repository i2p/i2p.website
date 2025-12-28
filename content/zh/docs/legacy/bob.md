---
title: "BOB – 基本开放桥"
description: "用于目标管理的已弃用 API（已弃用）"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **警告：** BOB 仅支持旧版 DSA-SHA1 签名类型。Java I2P 自 1.7.0（2022-02）起不再随附 BOB；它仅在最初从 1.6.1 或更早版本开始的安装中，以及某些 i2pd 构建中仍然存在。新的应用程序必须使用 [SAM v3](/docs/api/samv3/)。

## 语言绑定

- Go 语言 – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## 协议说明

- `KEYS` 表示一个 base64 destination（目标地址，公钥 + 私钥）。  
- `KEY` 是一个 base64 公钥。  
- `ERROR` 响应的格式为 `ERROR <description>\n`。  
- `OK` 表示命令已完成；可选数据紧随其后，位于同一行。  
- `DATA` 行会在最终的 `OK` 之前流式输出额外内容。

`help` 命令是唯一的例外：它可能什么也不返回，以表示“无此命令”。

## 连接横幅

BOB 使用以换行符结尾的 ASCII 行（LF 或 CRLF）。建立连接时它会输出：

```
BOB <version>
OK
```
当前版本：`00.00.10`。早期构建使用大写十六进制数字和非标准编号。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## 核心命令

> 如需完整的命令详情，请使用 `telnet localhost 2827` 进行连接并运行 `help`。

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## 弃用摘要

- BOB 不支持现代签名类型、加密的 LeaseSets（租约集）以及传输层特性。
- API 已冻结；不会再添加新的命令。
- 仍依赖 BOB 的应用应尽快迁移到 SAM v3。
