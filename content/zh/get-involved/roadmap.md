---
title: "I2P 开发路线图"
description: "I2P 网络的当前开发计划和历史里程碑"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P 采用增量开发模型**，大约每 13 周发布一次。此路线图涵盖了桌面版和 Android 版 Java 的发布，路径统一为单一的稳定版本发布路径。

**最后更新日期：**  2025 年 8 月

</div>

## 🎯 即将发布版本

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### 版本 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
目标：2025 年 12 月上旬
</div>

- 混合 PQ MLKEM Ratchet 最终版本，默认启用（提案 169）
- Jetty 12，要求 Java 17 以上
- 继续推进 PQ（传输）工作（提案 169）
- I2CP 查找支持 LS 服务记录参数（提案 167）
- 每隧道限制
- 适合 Prometheus 的统计子系统
- SAM 支持 Datagram 2/3

</div>

---

## 📦 最近发布版本

### 2025 发布版本

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**版本 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2025 年 9 月 8 日</span>

- i2psnark 支持 UDP 跟踪器（提案 160）
- I2CP LS 服务记录参数（部分）（提案 167）
- I2CP 异步查找 API
- 混合 PQ MLKEM Ratchet Beta（提案 169）
- 继续工作在 PQ（传输）（提案 169）
- 隧道构建带宽参数（提案 168）第二部分（处理）
- 继续工作在每隧道限制
- 移除未使用的传输 ElGamal 代码
- 移除古老的 SSU2 "活跃限制" 代码
- 移除古老的统计日志支持
- 统计/图表子系统清理
- 隐藏模式改进和修复

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**版本 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2025 年 6 月 2 日</span>

- Netdb 地图
- 实现 Datagram2, Datagram3（提案 163）
- 开始工作在 LS 服务记录参数（提案 167）
- 开始工作在 PQ（提案 169）
- 继续工作在每隧道限制
- 隧道构建带宽参数（提案 168）第一部分（发送）
- 默认使用 /dev/random 做 PRNG 在 Linux 上
- 移除冗余的 LS 渲染代码
- 显示 HTML 中的变更日志
- 减少 HTTP 服务器线程使用
- 修复自动泛洪填充注册
- 包装器更新到 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**版本 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2025 年 3 月 29 日</span>

- 修复 SHA256 损坏 bug

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**版本 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2025 年 3 月 17 日</span>

- 修复 Java 21 以上安装失败问题
- 修复 "环回" bug
- 修复出站客户端隧道的隧道测试
- 修复安装到含有空格的路径
- 更新过时的 Docker 容器和库
- 控制台通知气泡
- SusiDNS 排序为最新
- 在 Noise 中使用 SHA256 池
- 控制台深色主题修复与改进
- .i2p.alt 支持

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**版本 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2025 年 2 月 3 日</span>

- 路由器信息发布改进
- 提高 SSU2 ACK 效率
- 提高 SSU2 重复中继消息处理
- 更快/可变的查找超时时间
- LS 过期改进
- 更改对称 NAT 限制
- 强制在更多表单中使用 POST
- SusiDNS 深色主题修复
- 带宽测试清理
- 新增赣语翻译
- 增加库尔德语 UI 选项
- 新 Jammy 构建
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 2024 发布版本</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 10 月 8 日</span>

- i2ptunnel HTTP 服务器减少线程使用
- I2PTunnel 中的通用 UDP 隧道
- I2PTunnel 中的浏览器代理
- 网站迁移
- 修复隧道变黄的问题
- 控制台 /netdb 重构

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 8 月 6 日</span>

- 修复控制台中 iframe 尺寸问题
- 将图表转换为 SVG
- 捆绑翻译状态报告

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 7 月 19 日</span>

- 减少 netdb 内存使用
- 移除 SSU1 代码
- 修复 i2psnark 临时文件泄漏和卡顿
- 提高 i2psnark 中的 PEX 效率
- 控制台图表的 JS 刷新
- 图表渲染改进
- Susimail JS 搜索
- 提高 OBEP 消息处理效率
- 提高本地目标 I2CP 查找效率
- 修复 JS 变量作用域问题

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 5 月 15 日</span>

- 修复 HTTP 截断
- 如果检测到对称 NAT，发布 G 功能
- 更新至 rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 5 月 6 日</span>

- NetDB DDoS 缓解
- Tor 黑名单
- Susimail 修复和搜索
- 继续移除 SSU1 代码
- 更新至 Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2024 年 4 月 8 日</span>

- 控制台 iframe 改进
- 重新设计 i2psnark 带宽限制器
- i2psnark 和 susimail 的 JavaScript 拖放功能
- i2ptunnel SSL 错误处理改进
- i2ptunnel 持久化 HTTP 连接支持
- 开始移除 SSU1 代码
- SSU2 中继标签请求处理改进
- SSU2 对等测试修复
- Susimail 改进（加载、markdown、HTML 邮件支持）
- 隧道对等选择调整
- 更新 RRD4J 至 3.9
- 更新 gradlew 至 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**版本 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 发布于 2023 年 12 月 18 日</span>

- NetDB 上下文管理/分段 NetDB
- 通过降低超载路由器的优先级处理拥塞能力
- 复兴 Android 辅助库
- i2psnark 本地种子文件选择器
- NetDB 查找处理器修复
- 禁用 SSU1
- 禁止未来发布的路由器
- SAM 修复
- susimail 修复
- UPnP 修复

</div>

---

### 2023-2022 发布版本

<details>
<summary>点击展开 2023-2022 发布版本</summary>

**版本 2.3.0** — 发布于 2023 年 6 月 28 日

- 隧道对等选择改进
- 用户可配置的黑名单过期
- 限制来自同一来源的快速查找爆发
- 修复重放检测信息泄漏
- 多宿主 leaseSets 的 NetDB 修复
- 在接收为存储之前已作为回复接收的 leaseSets 的 NetDB 修复

**版本 2.2.1** — 发布于 2023 年 4 月 12 日

- 打包修复

**版本 2.2.0** — 发布于 2023 年 3 月 13 日

- 隧道对等选择改进
- 流重放修复

**版本 2.1.0** — 发布于 2023 年 1 月 10 日

- SSU2 修复
- 隧道构建拥塞修复
- SSU 对等测试和对称 NAT 检测修复
- 修复损坏的 LS2 加密 leaseSets
- 禁用 SSU 1 的选项（初步）
- 可压缩填充（提案 161）
- 新增控制台对等状态选项卡
- 为 SOCKS 代理添加 torsocks 支持以及其他 SOCKS 改进和修复

**版本 2.0.0** — 发布于 2022 年 11 月 21 日

- SSU2 连接迁移
- SSU2 即时确认
- 默认启用 SSU2
- i2ptunnel 中的 SHA-256 摘要代理认证
- 更新 Android 构建流程以使用现代 AGP
- 跨平台（桌面）I2P 浏览器自动配置支持

**版本 1.9.0** — 发布于 2022 年 8 月 22 日

- SSU2 对等测试和中继实现
- SSU2 修复
- SSU MTU/PMTU 改进
- 为少部分路由器启用 SSU2
- 添加死锁检测器
- 更多证书导入修复
- 修复 i2psnark DHT 在路由器重启后重启

**版本 1.8.0** — 发布于 2022 年 5 月 23 日

- 路由器家族修复和改进
- 软重启修复
- SSU 修复和性能改进
- I2PSnark 独立修复和改进
- 避免对受信家族的 Sybil 惩罚
- 减少隧道构建回复超时
- UPnP 修复
- 移除 BOB 源
- 证书导入修复
- Tomcat 9.0.62
- 重构以支持 SSU2（提案 159）
- SSU2 基础协议的初始实现（提案 159）
- Android 应用的 SAM 授权弹出窗口
- 改善 i2p.firefox 中自定义目录安装的支持

**版本 1.7.0** — 发布于 2022 年 2 月 21 日

- 移除 BOB
- 新的 i2psnark 种子文件编辑器
- i2psnark 独立修复和改进
- NetDB 可靠性改进
- 在系统托盘中添加弹出消息
- NTCP2 性能改进
- 当第一跳失败时删除出站隧道
- 在多次客户端隧道构建失败后回退到探索性隧道
- 恢复隧道同 IP 限制
- 重构 i2ptunnel UDP 支持到 I2CP 端口
- 继续 SSU2 工作，开始实现（提案 159）
- 创建 I2P 浏览器配置文件的 Debian/Ubuntu 包
- 创建 I2P 浏览器配置文件插件
- 记录 Android 应用的 I2P
- i2pcontrol 改进
- 插件支持改进
- 新的本地出代理插件
- IRCv3 消息标记支持

</details>

---

### 2021 发布版本

<details>
<summary>点击展开 2021 发布版本</summary>

**版本 1.6.1** — 发布于 2021 年 11 月 29 日

- 加速钥匙转换路由器到 ECIES
- SSU 性能改进
- 改善 SSU 对等测试的安全性
- 在新安装向导中添加主题选择
- 继续 SSU2 工作（提案 159）
- 发送新的隧道构建消息（提案 157）
- 在 IzPack 安装程序中包括自动浏览器配置工具
- 使分叉和执行插件可管理
- 文档化 jpackage 安装流程
- 完成并记录 Go/Java 插件生成工具
- Reseed 插件用于自签名 HTTPS Reseed

**版本 1.5.0** — 发布于 2021 年 8 月 23 日

- 加速钥匙转换路由器到 ECIES
- 开始 SSU2 工作
- 实现新隧道构建消息（提案 157）
- 支持 dmg 和 exe 自动更新
- 新的原生 OSX 安装程序
- 内置 I2P 
