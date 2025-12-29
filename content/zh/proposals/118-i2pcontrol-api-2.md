---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rejected"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## 概述

本提案概述了I2PControl的API2。

本提案已被拒绝，不会实施，因为它破坏了向后兼容性。
详情请参见讨论主题链接。

### 开发人员提示！

所有RPC参数现在都将是小写。这*将会*破坏与API1实现的向后兼容性。这样做的目的是为使用>=API2的用户提供最简单、最连贯的API。

## API 2 规范

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### 参数

**`"id"`**

请求的ID编号。用于识别哪个回复是由哪个请求触发的。

**`"method_name"`**

正被调用的RPC名称。

**`"auth_token"`**

会话认证令牌。除'authenticate'调用外，需在每个RPC中提供。

**`"method_parameter_value"`**

方法参数。用于提供方法的不同变体，如'get'、'set'等类似的变体。

**`"result_value"`**

RPC返回的值。其类型和内容取决于方法及该方法。


### 前缀

RPC命名方案类似于在CSS中的做法，为不同的API实现（i2p, kovri, i2pd）提供供应商前缀:

```text
XXX.YYY.ZZZ
i2p.XXX.YYY.ZZZ
i2pd.XXX.YYY.ZZZ
kovri.XXX.YYY.ZZZ
```

使用供应商特定前缀的整体理念是允许一定的灵活性，让实现创新而不必等待其他实现趋同。如果所有实现都已实现某个RPC，则可以移除多个前缀，并将其作为核心RPC包含在下一个API版本中。


### 方法阅读指南

 * **rpc.method**

   * *parameter* [参数类型]:  [null], [number], [string], [boolean],
     [array] 或 [object]。 [object] 是一个 {key:value} 映射。

返回:
```text
"return_value" [string] // 这是RPC调用返回的值
```


### 方法

* **authenticate** - 提供正确的密码后，此方法为您提供进一步访问的令牌和支持的API级别列表。

  * *password* [string]: 此i2pcontrol实现的密码

    返回:
```text
    [object]
    {
      "token" : [string], // 需在所有其他RPC方法中提供的令牌
      "api" : [[int],[int], ...]  // 支持的API级别列表。
    }
```

* **control.** - 控制i2p

  * **control.reseed** - 开始重新播种

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

  * **control.restart** - 重启i2p实例

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

  * **control.restart.graceful** - 温和地重启i2p实例

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

  * **control.shutdown** - 关闭i2p实例

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

  * **control.shutdown.graceful** - 温和地关闭i2p实例

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

  * **control.update.find** - **阻塞** 搜索签名更新

    * \[nil\]: 不需要参数

    返回:
```text
      true [boolean] // 仅当有签名更新可用时为真
```

  * **control.update.start** - 开始更新过程

    * \[nil\]: 不需要参数

    返回:
```text
      [nil]
```

* **i2pcontrol.** - 配置i2pcontrol

  * **i2pcontrol.address** - 获取/设置i2pcontrol侦听的IP地址。

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: 将其设置为类似于"0.0.0.0"或"192.168.0.1"的IP地址

    返回:
```text
      [nil]
```

  * **i2pcontrol.password** - 更改i2pcontrol密码。

    * *set* [string]: 将新密码设置为此字符串

    返回:
```text
      [nil]
```

  * **i2pcontrol.port** - 获取/设置i2pcontrol侦听的端口。

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      7650 [number]
```

    * *set* [number]: 更改i2pcontrol侦听的端口

    返回:
```text
      [nil]
```

* **settings.** - 获取/设置i2p实例设置

  * **settings.advanced** - 高级设置

    * *get*  [string]: 获取此设置的值

    返回:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    返回:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: 设置此设置的值
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    返回:
```text
      [nil]
```

  * **settings.bandwidth.in** - 入站带宽设置
  * **settings.bandwidth.out** - 出站带宽设置

    * *get* [nil]: 不需要设置此参数。

    返回:
```text
      0 [number]
```

    * *set* [number]: 设置带宽限制

    返回:
```text
     [nil]
```

  * **settings.ntcp.autoip** - 获取NTCP的IP自动检测设置

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - 获取NTCP主机名

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: 设置新主机名

    返回:
```text
      [nil]
```

  * **settings.ntcp.port** - NTCP端口

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      0 [number]
```

    * *set* [number]: 设置新的NTCP端口。

    返回:
```text
      [nil]
```

    * *set* [boolean]: 设置NTCP IP自动检测

    返回:
```text
      [nil]
```

  * **settings.ssu.autoip** - 配置SSU的IP自动检测设置

    * *get* [nil]: 不需要设置此参数。

    返回:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - 配置SSU主机名

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: 设置新的SSU主机名

    返回:
```text
      [nil]
```

  * **settings.ssu.port** - SSU端口

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      0 [number]
```

    * *set* [number]: 设置新的SSU端口。

    返回:
```text
      [nil]
```

    * *set* [boolean]: 设置SSU IP自动检测

    返回:
```text
      [nil]
```

  * **settings.share** - 获取带宽共享百分比

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      0 [number] // 带宽共享百分比 (0-100)
```

    * *set* [number]: 设置带宽共享百分比 (0-100)

    返回:
```text
      [nil]
```

  * **settings.upnp** - 启用或禁用UPNP

    * *get* [nil]: 不需要设置此参数。

    返回:
```text
      true [boolean]
```

    * *set* [boolean]: 设置SSU IP自动检测

    返回:
```text
      [nil]
```

* **stats.** - 从i2p实例获取统计信息

  * **stats.advanced** - 此方法提供对实例中保留的所有统计信息的访问。

    * *get* [string]:  要提供的高级统计信息的名称
    * *Optional:* *period* [number]:  请求统计信息的时间段

  * **stats.knownpeers** - 返回已知的对等端数量
  * **stats.uptime** - 返回自路由器启动以来的毫秒时间
  * **stats.bandwidth.in** - 返回入站带宽（最好在上一秒）
  * **stats.bandwidth.in.total** - 返回自上次重启以来接收的字节数
  * **stats.bandwidth.out** - 返回出站带宽（最好在上一秒）
  * **stats.bandwidth.out.total** - 返回自上次重启以来发送的字节数
  * **stats.tunnels.participating** - 返回当前参与的隧道数量
  * **stats.netdb.peers.active** - 返回最近与之通信的对等端数量
  * **stats.netdb.peers.fast** - 返回“快速”对等端的数量
  * **stats.netdb.peers.highcapacity** - 返回“高容量”对等端的数量
  * **stats.netdb.peers.known** - 返回已知对等端的数量

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      0.0 [number]
```

* **status.** - 获取i2p实例状态

  * **status.router** - 获取路由器状态

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      "status" [string]
```

  * **status.net** - 获取路由器网络状态

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - i2p实例当前是否是洪泛填充

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      true [boolean]
```

  * **status.isreseeding** - i2p实例当前是否正在重新播种

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      true [boolean]
```

  * **status.ip** - 该i2p实例检测到的公共IP

    * *get* [null]: 不需要设置此参数。

    返回:
```text
      "0.0.0.0" [string]
```
