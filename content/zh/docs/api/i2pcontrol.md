---
title: "I2PControl JSON-RPC"
description: "通过 I2PControl webapp 进行远程 router 管理的 API"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# I2PControl API 文档

-------------检查添加内容--------------

I2PControl 是一个与 I2P router 捆绑的 **JSON-RPC 2.0** API（自 0.9.39 版本起）。它通过结构化的 JSON 请求实现对 router 的认证监控和控制。

> **默认密码：** `itoopie` — 这是出厂默认密码，出于安全考虑**应当立即更改**。

## 1. 概览与访问

| 实现             | 默认端点                 | 协议 | 默认启用                             | 备注                  |
|------------------|--------------------------|------|------------------------------------|-----------------------|
| Java I2P (2.10.0+) | `http://127.0.0.1:7657/jsonrpc/` | HTTP | ❌ 必须通过 WebApps（路由器控制台）启用 | 捆绑的网页应用         |
| i2pd (C++ 实现)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ 默认启用                           | 传统插件行为 |
---

在 Java I2P 的情况下，您必须前往 **Router Console → WebApps → I2PControl** 并启用它（设置为自动启动）。一旦激活，所有方法都要求您首先进行身份验证并接收会话令牌。

## 2. JSON-RPC 格式

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
所有请求都遵循 JSON-RPC 2.0 结构：

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
成功的响应包含一个 `result` 字段；失败时，会返回一个 `error` 对象：

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
或

## 3. 认证流程

### 请求（身份验证）

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### 成功响应

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| 字段       | 方向      | 类型   | 描述                                                   |
|------------|-----------|--------|--------------------------------------------------------|
| `API`      | 请求      | long   | 客户端请求的 I2PControl API 版本。使用 `1`。           |
| `Password` | 请求      | String | 用于通过 I2PControl 进行身份验证的密码。               |
| `API`      | 响应      | long   | 服务器实现的主要 API 版本。                            |
| `Token`    | 响应      | String | 用于后续请求的身份验证令牌。                           |
---

您必须在所有后续请求的 `params` 中包含该 `Token`。

## 4. 方法和端点

### 4.1 RouterInfo

---

获取关于 router 的关键遥测数据。

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**请求示例**

#### 状态码枚举 (`i2p.router.net.status`)

| 键名                                    | 类型   | 说明                                                                  |
|----------------------------------------|--------|-----------------------------------------------------------------------|
| `i2p.router.status`                    | 字符串 | 自由格式、已本地化的路由器状态，用于显示。                             |
| `i2p.router.uptime`                    | long   | 路由器运行时间，单位为毫秒。旧版 i2pd 可能返回字符串。                |
| `i2p.router.version`                   | 字符串 | 完整的路由器版本号。                                                  |
| `i2p.router.net.status`                | long   | 网络状态码；见下表。                                                  |
| `i2p.router.net.bw.inbound.1s`         | double | 当前入站带宽，单位为字节/秒。                                         |
| `i2p.router.net.bw.inbound.15s`        | double | 15 秒平均入站带宽，单位为字节/秒。                                    |
| `i2p.router.net.bw.outbound.1s`        | double | 当前出站带宽，单位为字节/秒。                                         |
| `i2p.router.net.bw.outbound.15s`       | double | 15 秒平均出站带宽，单位为字节/秒。                                    |
| `i2p.router.net.tunnels.participating` | long   | 本路由器参与的隧道数量。                                              |
#### 状态码枚举 (`i2p.router.net.status`)

| Code | 含义                                             |
|------|--------------------------------------------------|
| 0    | 正常（OK）                                        |
| 1    | 测试中（TESTING）                                 |
| 2    | 被防火墙屏蔽（FIREWALLED）                        |
| 3    | 隐藏模式（HIDDEN）                                |
| 4    | 警告：防火墙屏蔽且节点速度较快（WARN_FIREWALLED_AND_FAST） |
| 5    | 警告：防火墙屏蔽且为floodfill节点（WARN_FIREWALLED_AND_FLOODFILL） |
| 6    | 警告：防火墙屏蔽但启用了入站TCP（WARN_FIREWALLED_WITH_INBOUND_TCP） |
| 7    | 警告：防火墙屏蔽且UDP已禁用（WARN_FIREWALLED_WITH_UDP_DISABLED） |
| 8    | I2CP错误（ERROR_I2CP）                            |
| 9    | 时钟偏差错误（ERROR_CLOCK_SKEW）                  |
| 10   | 私有TCP地址错误（ERROR_PRIVATE_TCP_ADDRESS）       |
| 11   | 对称型NAT错误（ERROR_SYMMETRIC_NAT）               |
| 12   | UDP端口已被占用（ERROR_UDP_PORT_IN_USE）           |
| 13   | 无活跃对等节点，请检查连接和防火墙（ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL） |
| 14   | UDP已禁用且TCP未设置（ERROR_UDP_DISABLED_AND_TCP_UNSET） |
#### NetDB 和节点字段

| Key                                  | 类型    | 说明                                              |
|--------------------------------------|---------|---------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | 已知对等体数量，不包括本地路由器。                 |
| `i2p.router.netdb.activepeers`       | long    | 活跃对等体数量。                                   |
| `i2p.router.netdb.fastpeers`         | long    | 被分类为“快速”的对等体数量。                       |
| `i2p.router.netdb.highcapacitypeers` | long    | 被分类为“高容量”的对等体数量。                    |
| `i2p.router.netdb.isreseeding`       | boolean | 是否正在执行重新种子（reseed）。                  |
**响应字段 (result)**   根据官方文档 (GetI2P)：   - `i2p.router.status` (String) — 人类可读的状态   - `i2p.router.uptime` (long) — 毫秒数（或旧版 i2pd 的字符串） :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — 版本字符串 :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — 入站带宽，单位 B/s :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — 出站带宽，单位 B/s :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — 数字状态码（见下方枚举） :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — 参与的 tunnel 数量 :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — netDB 节点统计 :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — 是否正在进行重新播种 :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — 已知节点总数 :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| 参数 | 类型 | 描述 |
|-----------|--------|------------------------------|
| `Stat`    | 字符串 | 路由器 RateStat 名称。 |
| `Period`  | 长整型 | 速率周期，单位为毫秒。 |
用于在给定时间窗口内获取速率指标（例如带宽、tunnel 成功率）。

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**请求示例**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**示例响应**

### 4.3 RouterManager

---

| 参数               | 结果              | 描述                                                                 |
|--------------------|-------------------|----------------------------------------------------------------------|
| `Restart`          | null              | 立即启动路由器重启。                                                  |
| `RestartGraceful`  | null              | 在参与的隧道过期后重启。                                              |
| `Shutdown`         | null              | 立即启动路由器关闭。                                                  |
| `ShutdownGraceful` | null              | 在参与的隧道过期后关闭。                                              |
| `Reseed`           | null              | 开始路由器重新种子（reseed）。                                        |
| `FindUpdates`      | boolean 或 String | 阻塞操作。搜索已签名的路由器更新。                                    |
| `Update`           | String            | 阻塞操作。启动已签名的路由器更新并返回其最终状态。                    |
执行管理操作。

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**允许的参数 / 方法**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**请求示例**

### 4.4 网络设置

**成功响应**

---

| 键                              | 可接受的值                                       | 说明                                                  |
|---------------------------------|--------------------------------------------------|-------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | 字符串, 1–65535                                  | NTCP 端口；更改需要重启。                             |
| `i2p.router.net.ntcp.hostname`  | 字符串                                           | NTCP 主机名；更改需要重启。                           |
| `i2p.router.net.ntcp.autoip`    | `always`, `true`, 或 `false`                     | NTCP 自动地址选择。                                   |
| `i2p.router.net.ssu.port`       | 字符串, 1–65535                                  | SSU 端口；更改需要重启。                              |
| `i2p.router.net.ssu.hostname`   | 字符串                                           | SSU 外部主机名；更改需要重启。                        |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu`, 或 `local,upnp,ssu` | SSU 地址发现来源。                                    |
| `i2p.router.net.ssu.detectedip` | null                                             | 只读的检测到的 SSU 地址。                             |
| `i2p.router.net.upnp`           | 字符串                                           | UPnP 设置。                                           |
| `i2p.router.net.bw.share`       | 字符串, 0–100                                    | 可用于参与隧道的带宽百分比。                          |
| `i2p.router.net.bw.in`          | 非负整数字符串                                   | 入站带宽限制，单位 KiB/s。                            |
| `i2p.router.net.bw.out`         | 非负整数字符串                                   | 出站带宽限制，单位 KiB/s。                            |
| `i2p.router.net.laptopmode`     | 字符串                                           | 笔记本模式设置。                                      |
获取或设置网络配置参数（端口、upnp、带宽共享等）

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**请求示例（获取当前值）**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**示例响应**

> 注意：i2pd 2.41 之前的版本可能返回数字类型而不是字符串——客户端应该处理两种类型。:contentReference[oaicite:11]{index=11}

### 4.5 高级设置

---

| 参数 | 类型 | 说明 |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | 字符串              | 在 `get` 结果对象中返回单个设置。 |
| `getAll`  | 不适用              | 在 `getAll` 中返回完整的配置映射。 |
| `set`     | 映射<字符串, 字符串> | 更新提供的设置，同时保留其他未提及的键。 |
| `setAll`  | 映射<字符串, 字符串> | **破坏性操作：** 替换所有设置并移除未提供的键。 |
允许操作内部 router 参数。

**请求示例**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**响应示例**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### 标准 JSON-RPC2 错误代码

---

| 参数    | 类型   | 描述                     |
|---------|--------|--------------------------|
| `Echo`  | 字符串 | 作为 `Result` 返回的值。 |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### I2PControl 特定错误代码

管理 I2PControl 本身。当前的 Java 处理程序支持更改密码。

| 参数                    | 类型   | 描述                                                                        |
|------------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password`  | 字符串 | 设置新的 I2PControl 密码，并撤销现有的认证令牌。                             |
结果包含 `SettingsSaved`。如果密码已更改，结果还会包含 `"i2pcontrol.password": null`。来自旧版独立插件的监听地址（listen-address）和监听端口（listen-port）设置在当前的 Java 处理程序中不生效。

> **默认密码：** `itoopie` — 这是出厂默认密码，出于安全考虑**应当立即更改**。

## 5. 错误代码

### 标准 JSON-RPC2 错误代码

| 代码   | 含义               |
|--------|--------------------|
| -32700 | JSON 解析错误      |
| -32600 | 无效请求           |
| -32601 | 方法未找到         |
| -32602 | 无效参数           |
| -32603 | 内部错误           |
### I2PControl 特定错误代码

| 代码   | 含义                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | 提供的密码无效                                                                |
| -32002 | 未提供身份验证令牌                                                        |
| -32003 | 身份验证令牌不存在                                                       |
| -32004 | 提供的身份验证令牌已过期，将被删除                        |
| -32005 | 使用的 I2PControl API 版本未指定，但必须指定 |
| -32006 | 指定的 I2PControl API 版本不受 I2PControl 支持               |
> **默认密码：** `itoopie` — 这是出厂默认密码，出于安全考虑**应当立即更改**。

## 6. 使用方法与最佳实践

- 始终包含 `Token` 参数（除了进行身份验证时）。
- 首次使用时更改默认密码（`itoopie`）。
- 对于 Java I2P，确保通过 WebApps 启用 I2PControl webapp。
- 准备应对细微差异：某些字段可能是数字或字符串，具体取决于 I2P 版本。
- 为显示友好的输出换行长状态字符串。

> **默认密码：** `itoopie` — 这是出厂默认密码，出于安全考虑**应当立即更改**。
